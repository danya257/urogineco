# admin.py
from django.contrib import admin
from .models import *

# === Главная страница ===
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'description', 'image', 'cta_text', 'video_file']
    verbose_name = "Главный баннер"

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    ordering = ['order']

# === Медицинские разделы ===
@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    ordering = ['order']
    fieldsets = (
        ('Основное', {'fields': ['title', 'description']}),
        ('Дополнительно (не обязательно)', {'fields': ['icon', 'photo'], 'classes': ['collapse']}),
    )

# === Отзывы и дневник ===
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'order']
    ordering = ['order']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_published']
    list_filter = ['is_published']
    prepopulated_fields = {"slug": ("title",)}

# === Важное пациенткам ===
@admin.register(UsefulInfo)
class UsefulInfoAdmin(admin.ModelAdmin):
    verbose_name = "Важное пациенткам"
    verbose_name_plural = "Важное пациенткам"

# === О враче и контакты ===
@admin.register(AboutDoctor)
class AboutDoctorAdmin(admin.ModelAdmin):
    verbose_name = "Обо мне"

@admin.register(ClinicLocation)
class ClinicLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'order']
    ordering = ['order']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    verbose_name = "Контакты"

# === Прочее ===
admin.site.register(SEOAndContent)
admin.site.register(WorkExample)
admin.site.register(Achievement)
admin.site.register(EducationItem)
admin.site.register(Event)