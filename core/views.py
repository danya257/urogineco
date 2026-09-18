from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date

from .models import (
    Hero, AboutDoctor, UsefulInfo, ClinicLocation,
    Direction, WorkExample, Achievement, EducationItem,
    Procedure, Testimonial, BlogPost, Event, HeroStat, DoctorLetter,
    Disease, Memo, Faq, HeroSlide, Publication,
)
from .forms import TestimonialForm

MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def _mark_diary_links(events):
    ids = [e.id for e in events]
    with_diary = set(
        BlogPost.objects.filter(related_event_id__in=ids, is_published=True)
        .values_list('related_event_id', flat=True)
    )
    for e in events:
        e.has_diary_entry = e.id in with_diary
    return events


def _calendar(future, past):
    """Список дат для быстрого перехода к мероприятию."""
    items = []
    for e in list(future) + list(past):
        items.append({
            'id': e.id,
            'day': e.date.day,
            'month': MONTHS[e.date.month - 1][:3],
            'year': e.date.year,
            'title': e.title,
            'is_past': e.date < date.today(),
        })
    return items


def _clinics_and_draft(request):
    """Общий хвост страниц по ТЗ: адреса клиник и форма записи."""
    return {
        'clinic_locations': ClinicLocation.objects.all().order_by('order'),
        'lead_draft': request.session.pop('lead_draft', None) or {},
        'contact_intro': True,
    }


def home(request):
    today = date.today()

    procedures = Procedure.objects.all().order_by('order')
    testimonials = Testimonial.objects.filter(is_published=True).order_by('-created_at')[:6]

    future_events = _mark_diary_links(list(Event.objects.filter(date__gte=today).order_by('date')[:2]))
    past_events = _mark_diary_links(list(Event.objects.filter(date__lt=today).order_by('-date')[:2]))
    for i, e in enumerate(future_events):
        e.expanded = (i == 0)

    context = {
        'hero': Hero.objects.first(),
        'hero_slides': HeroSlide.objects.filter(is_visible=True),
        'hero_stats': HeroStat.objects.filter(is_visible=True),
        'memos': Memo.objects.filter(is_visible=True),
        'faqs': Faq.objects.filter(is_visible=True, disease__isnull=True)[:6],
        'letter': DoctorLetter.load(),
        'directions': Direction.objects.all(),
        'work_examples': WorkExample.objects.filter(is_published=True),
        'achievements': Achievement.objects.all(),
        'education_items': EducationItem.objects.all(),
        'procedures': procedures,
        'testimonials': testimonials,
        'blog_posts': BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3],
        'future_events': future_events,
        'past_events': past_events,
        'about_doctor': AboutDoctor.load(),
        'useful_info': UsefulInfo.load(),
        'clinic_locations': ClinicLocation.objects.all().order_by('order'),
        'diseases': Disease.objects.filter(is_visible=True),
        'lead_draft': request.session.pop('lead_draft', None) or {},
    }
    return render(request, 'index.html', context)


def diary(request):
    qs = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    paginator = Paginator(qs, 3)
    page_obj = paginator.get_page(request.GET.get('page'))
    ctx = {
        'blog_posts': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'diary.html', ctx)


def reviews(request):
    qs = Testimonial.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    ctx = {
        'testimonials': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'publications': Publication.objects.filter(is_visible=True),
        'faq_groups': [
            {'disease': d, 'items': list(d.faqs.filter(is_visible=True))}
            for d in Disease.objects.filter(is_visible=True)
            if d.faqs.filter(is_visible=True).exists()
        ],
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'reviews.html', ctx)


def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо! Ваш отзыв отправлен на модерацию.')
            return redirect('reviews')
    else:
        form = TestimonialForm()
    return render(request, 'add_testimonial.html', {'form': form})


def events(request):
    today = date.today()
    future_events = _mark_diary_links(list(Event.objects.filter(date__gte=today).order_by('date')))
    past_all = _mark_diary_links(list(Event.objects.filter(date__lt=today).order_by('-date')))
    for i, e in enumerate(future_events):
        e.expanded = (i == 0)

    ctx = {
        'future_events': future_events,
        'past_events': past_all[:2],
        'past_rest': past_all[2:],
        'calendar': _calendar(future_events, past_all),
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'events.html', ctx)


def event_report(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    blog_post = BlogPost.objects.filter(related_event=event, is_published=True).first()
    return render(request, 'event_report.html', {
        'event': event,
        'blog_post': blog_post,
    })


def diseases(request):
    ctx = {
        'diseases': Disease.objects.filter(is_visible=True),
        'procedures': Procedure.objects.all().order_by('order'),
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'diseases.html', ctx)


def disease(request, slug):
    item = get_object_or_404(Disease, slug=slug, is_visible=True)
    ctx = {
        'disease': item,
        'diseases': Disease.objects.filter(is_visible=True),
        'faqs': item.faqs.filter(is_visible=True),
        'about_doctor': AboutDoctor.load(),
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'disease.html', ctx)


def memos(request):
    ctx = {
        'memos': Memo.objects.filter(is_visible=True),
        'useful_info': UsefulInfo.load(),
        'diseases': Disease.objects.filter(is_visible=True),
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'memos.html', ctx)


def memo(request, slug):
    item = get_object_or_404(Memo, slug=slug, is_visible=True)
    return render(request, 'memo.html', {
        'memo': item,
        'memos': Memo.objects.filter(is_visible=True).exclude(pk=item.pk),
        'diseases': Disease.objects.filter(is_visible=True),
    })


def about(request):
    ctx = {
        'about_doctor': AboutDoctor.load(),
        'achievements': Achievement.objects.all(),
        'education_items': EducationItem.objects.all(),
        'letter': DoctorLetter.load(),
        'hero': Hero.objects.first(),
        'hero_stats': HeroStat.objects.filter(is_visible=True),
        'diseases': Disease.objects.filter(is_visible=True),
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'about.html', ctx)


def faq(request):
    items = Faq.objects.filter(is_visible=True).select_related('disease')
    general = [f for f in items if f.disease_id is None]
    by_disease = {}
    for f in items:
        if f.disease_id:
            by_disease.setdefault(f.disease, []).append(f)
    ctx = {
        'general_faqs': general,
        'faq_groups': [{'disease': d, 'items': v} for d, v in by_disease.items()],
        'diseases': Disease.objects.filter(is_visible=True),
        'publications': Publication.objects.filter(is_visible=True),
    }
    ctx.update(_clinics_and_draft(request))
    return render(request, 'faq.html', ctx)
