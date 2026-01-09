import os
import django
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify  # Импортируем slugify для генерации slug

# --- Убедитесь, что путь к settings правильный ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))  # Папка проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urogineco.settings")  # Замените на имя вашего settings-модуля

# Настройка Django
django.setup()

# Импорт моделей после настройки Django
from core.models import (
    Procedure, Testimonial, BlogPost, Event, AboutDoctor, UsefulInfo
)

def populate():
    print("Запуск заполнения демонстрационных данных...")

    # --- Операции ---
    print("Заполняем 'Операции'...")
    Procedure.objects.all().delete()  # Очистить перед заполнением (опционально)
    procedures_data = [
        {
            "title": "Лечение недержания мочи (TVT-O)",
            "description": "<p>Минимально инвазивная операция с использованием синтетической сетки. Восстанавливает поддержку уретры. Высокая эффективность и минимальное время восстановления.</p>",
            "icon": "fas fa-procedures"
        },
        {
            "title": "Коррекция пролапса тазовых органов",
            "description": "<p>Восстановление анатомического положения опущенных органов (матки, влагалища). Используются собственные ткани или сетки.</p>",
            "icon": "fas fa-bed"
        },
        {
            "title": "Лечение мочеполовых свищей",
            "description": "<p>Сложная операция по ушиванию свища между мочевым пузырем и влагалищем. Высокий процент успеха при правильной диагностике.</p>",
            "icon": "fas fa-band-aid"
        },
        {
            "title": "Уретральная транспозиция",
            "description": "<p>Авторская методика доктора Гвоздева М.Ю. для лечения рецидивирующего недержания мочи. Уникальная техника с минимальной инвазивностью.</p>",
            "icon": "fas fa-syringe"
        },
        {
            "title": "Пластика уретрального дивертикула",
            "description": "<p>Хирургическое удаление дивертикула уретры и восстановление её целостности. Позволяет избавиться от инфекций и боли.</p>",
            "icon": "fas fa-cut"
        }
    ]
    for proc_data in procedures_data:
        Procedure.objects.get_or_create(
            title=proc_data["title"],
            defaults={
                "description": proc_data["description"],
                "icon": proc_data.get("icon", "")
            }
        )

    # --- Отзывы ---
    print("Заполняем 'Отзывы'...")
    Testimonial.objects.all().delete()
    testimonials_data = [
        {
            "name": "Елена",
            "age": 54,
            "text": "<p>После операции могу смеяться, бегать и не думать о прокладках. Спасибо вам огромное!</p>"
        },
        {
            "name": "Анна",
            "age": 48,
            "text": "<p>Долгие годы страдала от пролапса. После операции чувствую себя на 20 лет моложе. Рекомендую!</p>"
        },
        {
            "name": "Мария",
            "age": 61,
            "text": "<p>Свищ после родов был страшной проблемой. Доктор Гвоздев провёл успешную операцию. Теперь всё в порядке.</p>"
        }
    ]
    for test_data in testimonials_data:
        Testimonial.objects.get_or_create(
            name=test_data["name"],
            defaults={
                "age": test_data.get("age"),
                "text": test_data["text"]
            }
        )

    # --- Дневник врача ---
    print("Заполняем 'Дневник врача'...")
    BlogPost.objects.all().delete()
    blog_data = [
        {
            "title": "Операция №312: лечение недержания TVT-O",
            "content": "<p>Пациентка 52 лет обратилась с жалобами на стрессовое недержание. После комплексного обследования была проведена операция TVT-O. Операция прошла успешно. Пациентка выписана на следующий день без катетера.</p>",
        },
        {
            "title": "Клинический случай: сложный мочеполовой свищ",
            "content": "<p>Пациентка с рецидивирующим свищом после экстирпации матки. Была выполнена сложная пластика с использованием лоскута. Контрольная цистоскопия — без признаков свища.</p>",
        },
        {
            "title": "Новая методика уретральной транспозиции: анализ 50 случаев",
            "content": "<p>Анализ результатов 50 пациенток, которым была выполнена авторская методика. 97% пациенток отметили полное исчезновение симптомов недержания через 3 месяца после операции.</p>",
        }
    ]
    for blog_data_item in blog_data:
        BlogPost.objects.get_or_create(
            title=blog_data_item["title"],
            defaults={
                "content": blog_data_item["content"],
                "slug": slugify(blog_data_item["title"]),  # Добавлено: генерация slug из title
                "is_published": True,
                "published_date": timezone.now()
            }
        )

    # --- Мероприятия ---
    print("Заполняем 'Мероприятия'...")
    Event.objects.all().delete()
    events_data = [
        {
            "title": "Международная конференция по урогинекологии",
            "date": timezone.now().date() + timezone.timedelta(days=30),
            "location": "Москва, Россия",
            "description": "<p>Доктор Гвоздев выступит с докладом о новых методах лечения недержания мочи.</p>",
            "link": "https://example.com/conference"
        },
        {
            "title": "Выездной семинар по реконструктивной хирургии",
            "date": timezone.now().date() + timezone.timedelta(days=60),
            "location": "Санкт-Петербург, Россия",
            "description": "<p>Практический семинар для врачей по малоинвазивным методам коррекции пролапса.</p>",
            "link": "https://example.com/seminar"
        },
        {
            "title": "Участие в EUGA 2025",
            "date": timezone.now().date() + timezone.timedelta(days=120),
            "location": "Прага, Чехия",
            "description": "<p>Доктор представит результаты клинического исследования по авторской методике.</p>",
            "link": "https://euga.org"
        }
    ]
    for event_data in events_data:
        Event.objects.get_or_create(
            title=event_data["title"],
            defaults={
                "date": event_data["date"],
                "location": event_data["location"],
                "description": event_data.get("description", ""),
                "link": event_data.get("link", "")
            }
        )

    # --- О враче ---
    print("Заполняем 'О враче'...")
    about_doc, created = AboutDoctor.objects.get_or_create(
        pk=1,
        defaults={
            "bio": "<p><strong>Гвоздев Михаил Юрьевич</strong> — врач-урогинеколог высшей категории, доктор медицинских наук, автор 3 патентов. Специализируется на сложных реконструктивных операциях органов малого таза. Более 18 лет клинической практики. Член Европейского общества урогинекологов (EUGA).</p>",
            "experience_years": 18,
            "patents": "<p><strong>Патент №2734567:</strong> Устройство для транспозиции уретры при недержании мочи.</p>",
            "awards": "<p>Почётный доктор Российской Ассоциации Урогинекологов (2023).</p>"
        }
    )
    if not created:
        # Обновить, если запись уже существовала
        about_doc.bio = "<p><strong>Гвоздев Михаил Юрьевич</strong> — врач-урогинеколог высшей категории, доктор медицинских наук, автор 3 патентов. Специализируется на сложных реконструктивных операциях органов малого таза. Более 18 лет клинической практики. Член Европейского общества урогинекологов (EUGA).</p>"
        about_doc.patents = "<p><strong>Патент №2734567:</strong> Устройство для транспозиции уретры при недержании мочи.</p>"
        about_doc.awards = "<p>Почётный доктор Российской Ассоциации Урогинекологов (2023).</p>"
        about_doc.save()

    # --- Полезное ---
    print("Заполняем 'Полезное'...")
    useful_info, created = UsefulInfo.objects.get_or_create(
        pk=1,
        defaults={
            "analyses": "<p><strong>Для первичной консультации необходимы:</strong><ul><li>Общий анализ мочи</li><li>Бакпосев мочи</li><li>УЗИ органов малого таза (с остаточной мочой)</li><li>Цистоскопия (по показаниям)</li></ul></p>",
            "hospital_guide": "<p><strong>Памятка пациентке перед госпитализацией:</strong><ul><li>Взять с собой: паспорт, направление, выписки, список лекарств.</li><li>Не есть за 8 часов до операции, не пить за 4 часа.</li><li>Не использовать косметику, лак для ногтей, украшения.</li><li>После операции: не поднимать тяжести >3 кг, исключить секс на 6 недель.</li></ul></p>"
        }
    )
    if not created:
        # Обновить, если запись уже существовала
        useful_info.analyses = "<p><strong>Для первичной консультации необходимы:</strong><ul><li>Общий анализ мочи</li><li>Бакпосев мочи</li><li>УЗИ органов малого таза (с остаточной мочой)</li><li>Цистоскопия (по показаниям)</li></ul></p>"
        useful_info.hospital_guide = "<p><strong>Памятка пациентке перед госпитализацией:</strong><ul><li>Взять с собой: паспорт, направление, выписки, список лекарств.</li><li>Не есть за 8 часов до операции, не пить за 4 часа.</li><li>Не использовать косметику, лак для ногтей, украшения.</li><li>После операции: не поднимать тяжести >3 кг, исключить секс на 6 недель.</li></ul></p>"
        useful_info.save()

    print("Демонстрационные данные успешно добавлены!")


if __name__ == "__main__":
    populate()
