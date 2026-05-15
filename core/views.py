from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date

from .models import (
    Hero, AboutDoctor, UsefulInfo, ClinicLocation,
    Direction, WorkExample, Achievement, EducationItem,
    Procedure, Testimonial, BlogPost, Event,
)
from .forms import TestimonialForm


def home(request):
    today = date.today()

    procedures = Procedure.objects.all().order_by('order')
    testimonials = Testimonial.objects.filter(is_published=True).order_by('-created_at')[:6]
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]

    future_events = list(Event.objects.filter(date__gte=today).order_by('date')[:2])
    past_events = list(Event.objects.filter(date__lt=today).order_by('-date')[:2])

    event_ids = [e.id for e in future_events + past_events]
    diary_event_ids = set(
        BlogPost.objects.filter(related_event_id__in=event_ids, is_published=True)
        .values_list('related_event_id', flat=True)
    )
    for event in future_events + past_events:
        event.has_diary_entry = event.id in diary_event_ids

    context = {
        'hero': Hero.objects.first(),
        'directions': Direction.objects.all(),
        'work_examples': WorkExample.objects.filter(is_published=True),
        'achievements': Achievement.objects.all(),
        'education_items': EducationItem.objects.all(),
        'procedures': procedures,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
        'future_events': future_events,
        'past_events': past_events,
        'about_doctor': AboutDoctor.load(),
        'useful_info': UsefulInfo.load(),
        'clinic_locations': ClinicLocation.objects.all().order_by('order'),
    }
    return render(request, 'index.html', context)


def diary(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'diary.html', {'blog_posts': posts})


def reviews(request):
    qs = Testimonial.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'reviews.html', {
        'testimonials': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
    })


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
    future_events = list(Event.objects.filter(date__gte=today).order_by('date'))
    past_events = list(Event.objects.filter(date__lt=today).order_by('-date')[:2])

    event_ids = [e.id for e in future_events + past_events]
    diary_event_ids = set(
        BlogPost.objects.filter(related_event_id__in=event_ids, is_published=True)
        .values_list('related_event_id', flat=True)
    )
    for event in future_events + past_events:
        event.has_diary_entry = event.id in diary_event_ids

    return render(request, 'events.html', {
        'future_events': future_events,
        'past_events': past_events,
    })


def event_report(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    blog_post = BlogPost.objects.filter(related_event=event, is_published=True).first()
    return render(request, 'event_report.html', {
        'event': event,
        'blog_post': blog_post,
    })
