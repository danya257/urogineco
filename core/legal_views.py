"""Правовые страницы и приём заявок с формы записи."""
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .legal_models import Lead


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


@require_POST
def submit_lead(request):
    back = reverse('home') + '#contact'

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

    if errors:
        request.session['lead_draft'] = {'name': name[:150], 'phone': phone[:100], 'message': message[:3000]}
        for e in errors:
            messages.error(request, e)
        return HttpResponseRedirect(back)

    Lead.objects.create(
        name=name[:150],
        phone=phone[:100],
        message=message[:3000],
        consent_given=True,
        ip_address=_client_ip(request),
        user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:1000],
    )
    request.session.pop('lead_draft', None)
    messages.success(request, 'Заявка принята. Мы свяжемся с вами в течение 24 часов.')
    return HttpResponseRedirect(back)
