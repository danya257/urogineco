from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('diary/', views.diary, name='diary'),
    path('add-review/', views.add_testimonial, name='add_review'),
    path('reviews/', views.reviews, name='reviews'),
    path('events/', views.events, name='events'),
    path('diary/report-<int:event_id>/', views.event_report, name='event_report'),
]