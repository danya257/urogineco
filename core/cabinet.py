"""Кабинет — простой интерфейс управления сайтом для непрофессионала.

Цель: пожилой человек должен спокойно, без админки, видеть заявки,
модерировать отзывы и править тексты. Крупно, по одной задаче на экран.
"""
import re
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import strip_tags, linebreaks
from django.utils.text import slugify

from .models import Lead, Testimonial, ContactInfo, Hero, AboutDoctor, BlogPost
from .forms import ContactForm, HeroForm, AboutForm, DiaryPostForm

RICH_FIELDS = {'description', 'bio', 'patents', 'awards', 'content'}


def _is_staff(u):
    return u.is_active and u.is_staff


cabinet_required = user_passes_test(_is_staff, login_url='cabinet_login')


def html_to_text(html):
    """HTML -> простой текст (для показа в textarea при редактировании)."""
    if not html:
        return ''
    t = re.sub(r'(?i)</p\s*>', '\n\n', html)
    t = re.sub(r'(?i)<br\s*/?>', '\n', t)
    return strip_tags(t).strip()


def _save_rich(form, extra=None):
    """Сохраняет форму, превращая простой текст rich-полей обратно в HTML."""
    obj = form.save(commit=False)
    for f in RICH_FIELDS:
        if f in form.fields and hasattr(obj, f):
            setattr(obj, f, linebreaks(getattr(obj, f) or ''))
    if extra:
        extra(obj)
    obj.save()
    return obj


def _rich_initial(instance):
    if not instance:
        return {}
    return {f: html_to_text(getattr(instance, f, '')) for f in RICH_FIELDS
            if hasattr(instance, f)}


# ===================== Вход =====================
def cabinet_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('cabinet')
    error = ''
    if request.method == 'POST':
        user = authenticate(
            request,
            username=(request.POST.get('username') or '').strip(),
            password=request.POST.get('password') or '',
        )
        if user and user.is_staff:
            login(request, user)
            return redirect('cabinet')
        error = 'Неправильный логин или пароль. Попробуйте ещё раз.'
    return render(request, 'cabinet/login.html', {'error': error})


def cabinet_logout(request):
    logout(request)
    return redirect('cabinet_login')


# ===================== Главная Кабинета =====================
@cabinet_required
def cabinet_home(request):
    ctx = {
        'new_leads': Lead.objects.filter(is_processed=False).count(),
        'total_leads': Lead.objects.count(),
        'pending_reviews': Testimonial.objects.filter(is_published=False).count(),
        'diary_count': BlogPost.objects.count(),
    }
    return render(request, 'cabinet/dashboard.html', ctx)


# ===================== Заявки =====================
@cabinet_required
def cabinet_leads(request):
    return render(request, 'cabinet/leads.html', {
        'leads': Lead.objects.all(),
        'new_count': Lead.objects.filter(is_processed=False).count(),
    })


@cabinet_required
def cabinet_lead_toggle(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.is_processed = not lead.is_processed
    lead.save()
    return redirect('cabinet_leads')


# ===================== Отзывы =====================
@cabinet_required
def cabinet_reviews(request):
    return render(request, 'cabinet/reviews.html', {
        'reviews': Testimonial.objects.all().order_by('-created_at'),
    })


@cabinet_required
def cabinet_review_action(request, review_id, action):
    r = get_object_or_404(Testimonial, id=review_id)
    if action == 'publish':
        r.is_published = True
        r.save()
        messages.success(request, 'Отзыв теперь виден на сайте.')
    elif action == 'hide':
        r.is_published = False
        r.save()
        messages.success(request, 'Отзыв скрыт с сайта.')
    elif action == 'delete':
        r.delete()
        messages.success(request, 'Отзыв удалён.')
    return redirect('cabinet_reviews')


# ===================== Контакты =====================
@cabinet_required
def cabinet_contacts(request):
    obj = ContactInfo.load()
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Контакты сохранены.')
            return redirect('cabinet_contacts')
    else:
        form = ContactForm(instance=obj)
    return render(request, 'cabinet/form_page.html', {
        'form': form,
        'page_title': 'Мои контакты',
        'page_hint': 'Эти данные показываются в нижней части сайта и в кнопках связи.',
    })


# ===================== Главный экран (Hero) =====================
@cabinet_required
def cabinet_hero(request):
    obj = Hero.objects.first() or Hero()
    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            _save_rich(form)
            messages.success(request, 'Главный экран сохранён.')
            return redirect('cabinet_hero')
    else:
        form = HeroForm(instance=obj, initial=_rich_initial(obj))
    return render(request, 'cabinet/form_page.html', {
        'form': form,
        'page_title': 'Главный экран',
        'page_hint': 'Самый верх сайта: имя, подпись, кнопка и видео-визитка. '
                     'Чтобы на сайте появилось видео — загрузите файл .mp4 в поле «Видео-визитка». '
                     'Пока видео нет — показывается фотография.',
        'has_files': True,
    })


# ===================== Обо мне =====================
@cabinet_required
def cabinet_about(request):
    obj = AboutDoctor.load()
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=obj)
        if form.is_valid():
            _save_rich(form)
            messages.success(request, 'Раздел «Обо мне» сохранён.')
            return redirect('cabinet_about')
    else:
        form = AboutForm(instance=obj, initial=_rich_initial(obj))
    return render(request, 'cabinet/form_page.html', {
        'form': form,
        'page_title': 'Обо мне',
        'page_hint': 'Расскажите о себе простым текстом. Каждый абзац — с новой строки.',
    })


# ===================== Дневник =====================
@cabinet_required
def cabinet_diary(request):
    return render(request, 'cabinet/diary_list.html', {
        'posts': BlogPost.objects.all().order_by('-published_date'),
    })


@cabinet_required
def cabinet_diary_edit(request, post_id=None):
    post = get_object_or_404(BlogPost, id=post_id) if post_id else None
    if request.method == 'POST':
        form = DiaryPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            def finalize(obj):
                if not obj.published_date:
                    obj.published_date = date.today()
                if not obj.slug:
                    base = slugify(obj.title, allow_unicode=True) or 'zapis'
                    slug, i = base, 2
                    while BlogPost.objects.filter(slug=slug).exclude(pk=obj.pk).exists():
                        slug, i = f'{base}-{i}', i + 1
                    obj.slug = slug
            _save_rich(form, extra=finalize)
            messages.success(request, 'Запись сохранена.')
            return redirect('cabinet_diary')
    else:
        initial = {'content': html_to_text(post.content)} if post else {}
        form = DiaryPostForm(instance=post, initial=initial)
    return render(request, 'cabinet/diary_form.html', {
        'form': form,
        'post': post,
    })


@cabinet_required
def cabinet_diary_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Запись удалена.')
    return redirect('cabinet_diary')
