# initialize_db.py
import os
import django
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urogineco.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    SEOAndContent, Hero, AboutDoctor, UsefulInfo, ContactInfo,
    Procedure, ClinicLocation
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

    print("✅ Базовые данные созданы")

if __name__ == '__main__':
    create_superuser()
    create_initial_data()