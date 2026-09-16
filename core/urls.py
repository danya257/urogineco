from django.urls import path
from . import views, legal_views

urlpatterns = [
    path('', views.home, name='home'),
    path('diary/', views.diary, name='diary'),
    path('add-review/', views.add_testimonial, name='add_review'),
    path('reviews/', views.reviews, name='reviews'),
    path('events/', views.events, name='events'),

    # Разделы из ТЗ: операции, памятки, обо мне, вопрос-ответ
    path('operations/', views.diseases, name='diseases'),
    path('operations/<slug:slug>/', views.disease, name='disease'),
    path('patients/', views.memos, name='memos'),
    path('patients/<slug:slug>/', views.memo, name='memo'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('diary/report-<int:event_id>/', views.event_report, name='event_report'),

    # Правовые страницы (152-ФЗ и мед.дисклеймер)
    path('privacy/', legal_views.privacy, name='privacy'),
    path('consent/', legal_views.consent, name='consent'),
    path('disclaimer/', legal_views.disclaimer, name='disclaimer'),

    # Приём заявок с формы «Записаться на приём»
    path('lead/', legal_views.submit_lead, name='submit_lead'),
]
