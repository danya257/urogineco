# initialize_db.py
import os
import django
from datetime import date, timedelta
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urogineco.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    SEOAndContent, Hero, AboutDoctor, UsefulInfo, ContactInfo,
    Procedure, ClinicLocation, Event, BlogPost
)

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='12345' 
        )
        print("✅ Суперпользователь создан")

def create_initial_data():
    # SEO
    SEOAndContent.load()

    # Hero
    if not Hero.objects.exists():
        Hero.objects.create(
            title="Доктор Гвоздев Михаил Юрьевич",
            subtitle="Врач-урогинеколог • Хирург высшей категории",
            description="<p>Более 200 успешно проведённых операций...</p>",
            cta_text="Записаться на приём"
        )

    # Процедуры
    procedures = [
        "Недержание мочи",
        "Пролапс тазовых органов (РОР)",
        "Урогенитальные свищи",
        "Киста и дивертикул уретры",
        "Осложнения после операций",
        "Второе мнение"
    ]
    for i, title in enumerate(procedures, 1):
        Procedure.objects.get_or_create(
            title=title,
            defaults={'description': f"<p>Информация о {title.lower()}.</p>", 'order': i}
        )

    # Остальное (минимум)
    AboutDoctor.load()
    UsefulInfo.load()
    ContactInfo.load()

    # Клиники
    if not ClinicLocation.objects.exists():
        ClinicLocation.objects.create(
            name="Клиника «ЕвроMed»",
            address="г. Москва, ул. Новокузнецкая, д. 35/1",
            order=1
        )

    # Мероприятия: 2 прошедших и 1 текущее
    today = date.today()
    
    # Прошедшее мероприятие 1
    event1, _ = Event.objects.get_or_create(
        title="Конференция по урогинекологии 2024",
        defaults={
            'date': today - timedelta(days=30),
            'location': "Москва, Конгресс-центр",
            'description': "<p>Ежегодная конференция по современным методам лечения недержания мочи.</p>",
            'order': 1
        }
    )
    
    # Прошедшее мероприятие 2
    event2, _ = Event.objects.get_or_create(
        title="Мастер-класс по хирургии тазового дна",
        defaults={
            'date': today - timedelta(days=15),
            'location': "Санкт-Петербург, Медицинский центр",
            'description': "<p>Практический мастер-класс для врачей по операциям при пролапсе.</p>",
            'order': 2
        }
    )
    
    # Текущее/будущее мероприятие
    event3, _ = Event.objects.get_or_create(
        title="Вебинар: Новые методики в урогинекологии",
        defaults={
            'date': today + timedelta(days=7),
            'location': "Онлайн",
            'description': "<p>Открытый вебинар для пациенток и специалистов.</p>",
            'link': "https://example.com/webinar",
            'order': 3
        }
    )

    # Запись в дневнике врача, привязанная к первому прошедшему мероприятию
    if not BlogPost.objects.filter(related_event=event1).exists():
        BlogPost.objects.create(
            title="Отчёт о конференции 2024",
            content="<p>Поделюсь впечатлениями от прошедшей конференции. Обсудили новые подходы к лечению...</p>",
            related_event=event1,
            is_published=True
        )
        print("✅ Запись в дневнике врача создана и привязана к мероприятию")

    print("✅ Базовые данные созданы")

if __name__ == '__main__':
    create_superuser()
    create_initial_data()