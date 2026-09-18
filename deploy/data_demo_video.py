# -*- coding: utf-8 -*-
"""Демонстрационные ролики (Pexels, свободная лицензия) вместо ещё не снятого видео врача:
слайдер на главной, видеоплеер на странице заболевания и в ближайшем мероприятии."""
import os
from datetime import date
from django.core.files import File
from core.models import HeroSlide, Disease, Event

SRC = os.environ.get('DEMO_VIDEO', '')
BANNER = os.environ.get('TZ_MEDIA', '')


def put(field, path, name):
    if path and os.path.exists(path) and not field.name:
        with open(path, 'rb') as f:
            field.save(name, File(f), save=True)
        return True
    return False


HeroSlide.objects.all().delete()

slide1 = HeroSlide.objects.create(
    kind='video', order=0, is_visible=True,
    title='Гвоздев М.Ю.|д.м.н., профессор, урогинеколог',
    subtitle='Помогаю женщинам вернуть здоровье и качество жизни — деликатно и профессионально.',
    button_text='Записаться на консультацию', button_url='/#contact',
)
put(slide1.video_file, os.path.join(SRC, 'hero_demo.mp4'), 'hero-demo.mp4')
put(slide1.image, os.path.join(SRC, 'hero_poster.jpg'), 'hero-demo-poster.jpg')

slide2 = HeroSlide.objects.create(
    kind='image', order=1, is_visible=True,
    title='Мероприятия|и выездные приёмы',
    subtitle='Конференции, выступления, консультации и операции в регионах.',
    button_text='Расписание', button_url='/events/',
)
put(slide2.image, os.path.join(BANNER, 'image18.png'), 'slide-events.png')
print('слайды:', HeroSlide.objects.count())

d = Disease.objects.filter(slug='nederzhanie-mochi').first()
if d:
    put(d.video_file, os.path.join(SRC, 'disease_demo.mp4'), 'nederzhanie-demo.mp4')
    put(d.video_poster, os.path.join(SRC, 'disease_poster.jpg'), 'nederzhanie-demo-poster.jpg')
    d.video_caption = 'Демонстрационный ролик — заменим на ваше видео'
    d.save()
    print('видео на странице заболевания:', d.video_file.url if d.video_file else None)

e = Event.objects.filter(date__gte=date.today()).order_by('date').first()
if e:
    put(e.video_file, os.path.join(SRC, 'event_demo.mp4'), 'event-demo.mp4')
    print('видео в мероприятии:', e.title, e.video_file.url if e.video_file else None)
