# urogineco/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import date
from .models import *
from .forms import TestimonialForm  # ← будет создан ниже


def home(request):
    seo_info = SEOAndContent.load()
    hero = Hero.objects.first()
    contact_info = ContactInfo.load()
    about_doctor = AboutDoctor.load()
    useful_info = UsefulInfo.load()
    clinic_locations = ClinicLocation.objects.all().order_by('order')
    directions = Direction.objects.all()
    work_examples = WorkExample.objects.filter(is_published=True)
    achievements = Achievement.objects.all()
    education_items = EducationItem.objects.all()
    procedures = Procedure.objects.all().order_by('order')
    
    # Только опубликованные отзывы
    testimonials = Testimonial.objects.filter(is_published=True).order_by('-created_at')[:6]
    
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
    
    # Мероприятия
    all_events = Event.objects.all().order_by('-date')
    today = date.today()
    future_events = [e for e in all_events if e.date >= today]
    past_events = [e for e in all_events if e.date < today][:2]  # ← только 2 прошедших

    context = {
        'seo_info': seo_info,
        'hero': hero,
        'directions': directions,
        'work_examples': work_examples,
        'achievements': achievements,
        'education_items': education_items,
        'contact_info': contact_info,
        'procedures': procedures,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
        'future_events': future_events,
        'past_events': past_events,
        'about_doctor': about_doctor,
        'useful_info': useful_info,
        'clinic_locations': clinic_locations,
    }
    return render(request, 'index.html', context)


def diary(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'diary.html', {'blog_posts': posts, 'seo_info': SEOAndContent.load()})


def reviews(request):
    testimonials = Testimonial.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'reviews.html', {'testimonials': testimonials, 'seo_info': SEOAndContent.load()})


def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш отзыв отправлен на модерацию.')
            return redirect('home')
    else:
        form = TestimonialForm()
    return render(request, 'add_testimonial.html', {'form': form, 'seo_info': SEOAndContent.load()})


def events(request):
    today = date.today()
    future_events = Event.objects.filter(date__gte=today).order_by('date')
    past_events = Event.objects.filter(date__lt=today).order_by('-date')
    return render(request, 'events.html', {
        'future_events': future_events,
        'past_events': past_events,
        'seo_info': SEOAndContent.load()
    })


def event_report(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        blog_post = BlogPost.objects.get(related_event=event, is_published=True)
    except BlogPost.DoesNotExist:
        blog_post = None

    # Добавьте эту строку:
    contact_info = ContactInfo.load()

    return render(request, 'event_report.html', {
        'event': event,
        'blog_post': blog_post,
        'seo_info': SEOAndContent.load(),
        'contact_info': contact_info,
    })