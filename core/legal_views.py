"""Правовые страницы и приём заявок с формы записи."""
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .legal_models import Lead
from .models import ContactInfo

MAX_ATTACHMENT = 10 * 1024 * 1024
ALLOWED_EXT = {
    '.pdf', '.jpg', '.jpeg', '.png', '.heic', '.webp',
    '.doc', '.docx', '.rtf', '.txt', '.zip',
}


def _operator():
    return getattr(settings, 'OPERATOR_INFO', {})


def privacy(request):
    return render(request, 'legal/privacy.html', {'operator': _operator()})


def consent(request):
    return render(request, 'legal/consent.html', {'operator': _operator()})


def disclaimer(request):
    return render(request, 'legal/disclaimer.html', {'operator': _operator()})


def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _notify_doctor(lead):
    """Письмо врачу с текстом заявки и вложением пациентки."""
    to = (ContactInfo.load().email or '').strip()
    # По умолчанию Django шлёт на localhost:25 — без явно настроенного SMTP
    # запрос повиснет до таймаута, поэтому отправляем только при заданном логине.
    if not to or not getattr(settings, 'EMAIL_HOST_USER', ''):
        return False

    from django.core.mail import EmailMessage, get_connection

    body = f"""Новая заявка с сайта

Имя: {lead.name}
Контакт: {lead.phone}
Дата: {lead.created_at:%d.%m.%Y %H:%M}

Сообщение:
{lead.message}
"""
    try:
        connection = get_connection(timeout=10)
    except Exception:
        return False
    msg = EmailMessage(
        subject=f'Заявка с сайта — {lead.name}',
        body=body,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', to),
        to=[to],
        reply_to=[lead.phone] if '@' in lead.phone else None,
        connection=connection,
    )
    if lead.attachment:
        lead.attachment.open('rb')
        try:
            msg.attach(lead.attachment.name.rsplit('/', 1)[-1], lead.attachment.read())
        finally:
            lead.attachment.close()
    try:
        msg.send(fail_silently=False)
    except Exception:
        return False
    return True


@require_POST
def submit_lead(request):
    back = (request.POST.get('next') or '').strip()
    if not back.startswith('/') or back.startswith('//'):
        back = reverse('home')
    back += '#contact'

    # Ловушка для ботов: поле скрыто от людей
    if (request.POST.get('website') or '').strip():
        messages.success(request, 'Заявка принята. Мы свяжемся с вами в течение 24 часов.')
        return HttpResponseRedirect(back)

    name = (request.POST.get('name') or '').strip()
    phone = (request.POST.get('phone') or '').strip()
    message = (request.POST.get('message') or '').strip()
    consent_ok = request.POST.get('consent') == 'on'

    errors = []
    if not name:
        errors.append('Укажите, как к вам обращаться.')
    if not phone:
        errors.append('Укажите телефон или Telegram для связи.')
    if not message:
        errors.append('Коротко опишите, что беспокоит.')
    if not consent_ok:
        errors.append('Без согласия на обработку персональных данных заявку отправить нельзя.')

    upload = request.FILES.get('attachment')
    if upload:
        import os
        ext = os.path.splitext(upload.name)[1].lower()
        if ext not in ALLOWED_EXT:
            errors.append('Вложение: допустимы PDF, фото, документы Word, ZIP.')
        elif upload.size > MAX_ATTACHMENT:
            errors.append('Вложение больше 10 МБ — пришлите файл поменьше или ссылку.')

    if errors:
        request.session['lead_draft'] = {'name': name[:150], 'phone': phone[:100], 'message': message[:3000]}
        for e in errors:
            messages.error(request, e)
        return HttpResponseRedirect(back)

    lead = Lead.objects.create(
        name=name[:150],
        phone=phone[:100],
        message=message[:3000],
        attachment=upload,
        consent_given=True,
        ip_address=_client_ip(request),
        user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:1000],
    )
    if _notify_doctor(lead):
        Lead.objects.filter(pk=lead.pk).update(mail_sent=True)
    request.session.pop('lead_draft', None)
    messages.success(request, 'Заявка принята. Мы свяжемся с вами в течение 24 часов.')
    return HttpResponseRedirect(back)
