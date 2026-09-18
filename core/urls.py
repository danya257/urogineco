from django.urls import path
from . import views, legal_views

urlpatterns = [
    path('', views.home, name='home'),
    path('diary/', views.diary, name='diary'),
    path('add-review/', views.add_testimonial, name='add_review'),
    path('reviews/', views.reviews, name='reviews'),
    path('events/', views.events, name='events'),
    path('diary/report-<int:event_id>/', views.event_report, name='event_report'),

    # Правовые страницы (152-ФЗ и мед.дисклеймер)
    path('privacy/', legal_views.privacy, name='privacy'),
    path('consent/', legal_views.consent, name='consent'),
    path('disclaimer/', legal_views.disclaimer, name='disclaimer'),

    # Приём заявок с формы «Записаться на приём»
    path('lead/', legal_views.submit_lead, name='submit_lead'),
]
