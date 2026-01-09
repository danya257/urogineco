from django.shortcuts import render
from django.utils import timezone
from .models import *

def home(request):
    context = {
        'seo_info': SEOAndContent.load(),
        'hero': Hero.objects.first(),
        'directions': Direction.objects.all(),
        'work_examples': WorkExample.objects.filter(is_published=True),
        'achievements': Achievement.objects.all(),
        'education_items': EducationItem.objects.all(),
        'contact_info': ContactInfo.load(),
        'procedures': Procedure.objects.all().order_by('order'),
        'testimonials': Testimonial.objects.all().order_by('order'),
        'blog_posts': BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3], 
        'events': Event.objects.filter(date__gte=timezone.now()).order_by('date'),
        'about_doctor': AboutDoctor.load(),
        'useful_info': UsefulInfo.load(),
        'clinic_locations': ClinicLocation.objects.all(),
    }
    return render(request, 'index.html', context)

def diary(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'diary.html', {'blog_posts': posts, 'seo_info': SEOAndContent.load()})

def reviews(request):
    testimonials = Testimonial.objects.all().order_by('order')
    return render(request, 'reviews.html', {'testimonials': testimonials, 'seo_info': SEOAndContent.load()})

def events(request):
    from django.utils import timezone
    future_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    return render(request, 'events.html', {
        'future_events': future_events,
        'past_events': past_events,
        'seo_info': SEOAndContent.load()
    })