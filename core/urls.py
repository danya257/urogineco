from django.urls import path
from . import views, cabinet

urlpatterns = [
    path('', views.home, name='home'),
    path('diary/', views.diary, name='diary'),
    path('add-review/', views.add_testimonial, name='add_review'),
    path('reviews/', views.reviews, name='reviews'),
    path('events/', views.events, name='events'),
    path('diary/report-<int:event_id>/', views.event_report, name='event_report'),
    path('submit-lead/', views.submit_lead, name='submit_lead'),

    # ===== Кабинет (простое управление сайтом) =====
    path('cabinet/vhod/', cabinet.cabinet_login, name='cabinet_login'),
    path('cabinet/vyhod/', cabinet.cabinet_logout, name='cabinet_logout'),
    path('cabinet/', cabinet.cabinet_home, name='cabinet'),
    path('cabinet/zayavki/', cabinet.cabinet_leads, name='cabinet_leads'),
    path('cabinet/zayavki/<int:lead_id>/', cabinet.cabinet_lead_toggle, name='cabinet_lead_toggle'),
    path('cabinet/otzyvy/', cabinet.cabinet_reviews, name='cabinet_reviews'),
    path('cabinet/otzyvy/<int:review_id>/<str:action>/', cabinet.cabinet_review_action, name='cabinet_review_action'),
    path('cabinet/kontakty/', cabinet.cabinet_contacts, name='cabinet_contacts'),
    path('cabinet/glavnyy/', cabinet.cabinet_hero, name='cabinet_hero'),
    path('cabinet/obo-mne/', cabinet.cabinet_about, name='cabinet_about'),
    path('cabinet/dnevnik/', cabinet.cabinet_diary, name='cabinet_diary'),
    path('cabinet/dnevnik/novaya/', cabinet.cabinet_diary_edit, name='cabinet_diary_new'),
    path('cabinet/dnevnik/<int:post_id>/', cabinet.cabinet_diary_edit, name='cabinet_diary_edit'),
    path('cabinet/dnevnik/<int:post_id>/udalit/', cabinet.cabinet_diary_delete, name='cabinet_diary_delete'),
]