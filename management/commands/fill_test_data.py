import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from your_app.models import (
    SEOAndContent, Hero, Direction, WorkExample, Achievement,
    EducationItem, ContactInfo, Procedure, Testimonial,
    BlogPost, Event, AboutDoctor, UsefulInfo, ClinicLocation
)


class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"

    def handle(self, *args, **options):
        self.stdout.write("Начинаю заполнение тестовыми данными...")

        # --- SEOAndContent (только 1 запись) ---
        seo, _ = SEOAndContent.objects.get_or_create(pk=1)
        seo.meta_title = "Доктор Гвоздев — урогинеколог | Москва"
        seo.meta_description = "Лечение недержания, пролапса, свищей. Опыт более 18 лет. Автор методик."
        seo.save()
        self.stdout.write("✅ SEOAndContent создан")

        # --- Hero (главная секция) ---
        hero, _ = Hero.objects.get_or_create(pk=1)
        hero.title = "Добро пожаловать на сайт доктора Гвоздева М.Ю."
        hero.subtitle = "Врач-урогинеколог высшей категории, кандидат медицинских наук"
        hero.description = "<p>Специализируюсь на сложных случаях недержания мочи, пролапса тазовых органов, послеоперационных свищах и других проблемах женского здоровья.</p>"
        hero.cta_text = "Записаться на приём"
        # Видео не загружаем (требует файла), но можно добавить позже
        hero.save()
        self.stdout.write("✅ Hero создан")

        # --- Directions ---
        directions = [
            ("Консультирую и оперирую", "Полный спектр диагностики и хирургического лечения"),
            ("Недержание мочи", "Устранение стрессового, императивного и смешанного недержания"),
            ("Пролапс тазовых органов (ПОП)", "Реконструктивные операции без сеток"),
            ("Мочеполовые свищи", "Лечение после родовых и послеоперационных повреждений"),
            ("Кисты и дивертикулы", "Диагностика и удаление патологий мочевого пузыря"),
            ("Осложнения", "Коррекция последствий неудачных операций"),
            ("Второе мнение", "Консультация по сложным клиническим случаям"),
        ]
        for i, (title, desc) in enumerate(directions):
            Direction.objects.get_or_create(
                title=title,
                defaults={"description": desc, "order": i}
            )
        self.stdout.write("✅ Directions созданы")

        # --- WorkExamples ---
        for i in range(3):
            WorkExample.objects.get_or_create(
                title=f"Кейс {i+1}",
                defaults={
                    "public_title": f"Операция при пролапсе (пример {i+1})",
                    "description": f"<p>Пациентка, {50 + i} лет. Диагноз: пролапс III степени...</p>",
                    "is_published": True,
                    "order": i
                }
            )
        self.stdout.write("✅ WorkExamples созданы")

        # --- Achievements ---
        achievements = [
            ("18+ лет опыта", "Работаю в урогинекологии с 2006 года", "gold"),
            ("1500+ операций", "Более полутора тысяч успешных вмешательств", "blue"),
            ("Автор методик", "Разработал уникальные подходы к лечению свищей", "pink"),
        ]
        for i, (title, desc, color) in enumerate(achievements):
            Achievement.objects.get_or_create(
                title=title,
                defaults={
                    "description": f"<p>{desc}</p>",
                    "badge_color": color,
                    "order": i
                }
            )
        self.stdout.write("✅ Achievements созданы")

        # --- Education ---
        educations = [
            ("2006", "Окончил РНИМУ им. Н.И. Пирогова", "Специальность: акушерство и гинекология"),
            ("2008", "Ординатура по урогинекологии", "На базе НИИ акушерства и гинекологии"),
            ("2012", "Кандидат медицинских наук", "Тема диссертации: лечение мочеполовых свищей"),
        ]
        for i, (year, title, desc) in enumerate(educations):
            EducationItem.objects.get_or_create(
                year=year,
                title=title,
                defaults={"description": f"<p>{desc}</p>", "order": i}
            )
        self.stdout.write("✅ Education создано")

        # --- ContactInfo ---
        contact, _ = ContactInfo.objects.get_or_create(pk=1)
        contact.address = "г. Москва, ул. Профсоюзная, д. 123"
        contact.telegram_link = "https://t.me/dr_gvozdev"
        contact.whatsapp_link = "https://wa.me/79991234567"
        contact.email = "info@gvozdev-clinic.ru"
        contact.save()
        self.stdout.write("✅ ContactInfo создан")

        # --- Procedures ---
        procedures = [
            ("Операция при недержании", "Слинговые операции без использования сеток", "fa-syringe"),
            ("Коррекция пролапса", "Реконструкция связочного аппарата", "fa-hospital"),
            ("Лечение свищей", "Пластика мочеполовых свищей", "fa-stethoscope"),
        ]
        for i, (title, desc, icon) in enumerate(procedures):
            Procedure.objects.get_or_create(
                title=title,
                defaults={"description": f"<p>{desc}</p>", "icon": icon, "order": i}
            )
        self.stdout.write("✅ Procedures созданы")

        # --- Testimonials ---
        for i in range(3):
            Testimonial.objects.get_or_create(
                name=f"Анна {i+1}",
                age=45 + i,
                defaults={
                    "text": f"<p>Огромное спасибо доктору! После операции прошло уже полгода — всё отлично.</p>",
                    "order": i
                }
            )
        self.stdout.write("✅ Testimonials созданы")

        # --- BlogPosts (Дневник врача) ---
        for i in range(3):
            BlogPost.objects.get_or_create(
                title=f"Запись от 2026-01-{10 + i}",
                slug=f"post-{i+1}",
                defaults={
                    "content": f"<p>Сегодня провёл интересную операцию у пациентки с рецидивным пролапсом...</p>",
                    "is_published": True,
                    "order": i
                }
            )
        self.stdout.write("✅ BlogPosts созданы")

        # --- Events ---
        events = [
            ("Конференция по урогинекологии", "2026-03-15", "Москва, ЦВК «Экспоцентр»", "Выступление с докладом"),
            ("Мастер-класс для коллег", "2026-05-20", "Санкт-Петербург", "Практический курс по свищам"),
        ]
        for i, (title, date, loc, desc) in enumerate(events):
            Event.objects.get_or_create(
                title=title,
                date=date,
                defaults={
                    "location": loc,
                    "description": f"<p>{desc}</p>",
                    "order": i
                }
            )
        self.stdout.write("✅ Events созданы")

        # --- AboutDoctor ---
        about, _ = AboutDoctor.objects.get_or_create(pk=1)
        about.bio = "<p>Михаил Юрьевич Гвоздев — врач-урогинеколог высшей категории...</p>"
        about.experience_years = 18
        about.patents = "<p>Патент №RU123456: Способ лечения везико-влагалищных свищей</p>"
        about.awards = "<p>Лауреат премии «Лучший врач России» (2023)</p>"
        about.save()
        self.stdout.write("✅ AboutDoctor создан")

        # --- UsefulInfo ---
        useful, _ = UsefulInfo.objects.get_or_create(pk=1)
        useful.prep_consultation = "<p>При себе иметь паспорт и медицинские выписки.</p>"
        useful.prep_surgery = "<p>За 3 дня до операции — анализы крови, ЭКГ, консультация терапевта.</p>"
        useful.anesthesia_info = "<p>Используется спинальная или общая анестезия по показаниям.</p>"
        useful.postop_period = "<p>Выписка на 2–3 сутки. Швы рассасывающиеся.</p>"
        useful.save()
        self.stdout.write("✅ UsefulInfo создан")

        # --- ClinicLocations ---
        clinics = [
            ("Клиника на Профсоюзной", "г. Москва, ул. Профсоюзная, д. 123", "https://maps.google.com/?q=55.6,37.5"),
            ("Центр на Кутузовской", "г. Москва, Кутузовский проспект, д. 45", "https://maps.google.com/?q=55.7,37.6"),
        ]
        for i, (name, addr, link) in enumerate(clinics):
            ClinicLocation.objects.get_or_create(
                name=name,
                defaults={"address": addr, "map_link": link, "order": i}
            )
        self.stdout.write("✅ ClinicLocations созданы")

        self.stdout.write(self.style.SUCCESS("✅ Тестовые данные успешно загружены!"))