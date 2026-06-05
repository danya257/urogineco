# admin.py
from django.contrib import admin

from .models import (
    SEOAndContent, Hero, Direction, WorkExample, Achievement, EducationItem,
    ContactInfo, Procedure, Testimonial, BlogPost, Event,
    AboutDoctor, UsefulInfo, ClinicLocation, Lead,
)


# === Главная страница ===
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'description', 'image', 'cta_text', 'video_file']


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
        ('Дополнительно (не обязательно)', {
            'fields': ['icon', 'photo'],
            'classes': ['collapse'],
        }),
    )


# === Отзывы и дневник ===
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Отзывы пишут пациенты через сайт.
    Администратор может только модерировать (публиковать/снимать с публикации) и удалять."""

    list_display = ['name', 'age', 'short_text', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    list_editable = ['is_published']
    search_fields = ['name', 'text']
    ordering = ['-created_at']
    readonly_fields = ['name', 'age', 'text', 'photo', 'created_at']
    fields = ['name', 'age', 'text', 'photo', 'created_at', 'is_published']

    @admin.display(description='Отзыв')
    def short_text(self, obj):
        from django.utils.html import strip_tags
        plain = strip_tags(obj.text or '')
        return plain[:80] + ('…' if len(plain) > 80 else '')

    def has_add_permission(self, request):
        # Отзывы создаются только пользователями через форму на сайте
        return False


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Заявки на приём с сайта. Создаются только посетителями через форму."""
    list_display = ['name', 'phone', 'short_message', 'is_processed', 'created_at']
    list_filter = ['is_processed', 'created_at']
    list_editable = ['is_processed']
    search_fields = ['name', 'phone', 'message']
    ordering = ['-created_at']
    readonly_fields = ['name', 'phone', 'message', 'created_at']
    fields = ['name', 'phone', 'message', 'created_at', 'is_processed']

    @admin.display(description='Сообщение')
    def short_message(self, obj):
        text = obj.message or ''
        return text[:70] + ('…' if len(text) > 70 else '')

    def has_add_permission(self, request):
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_published', 'related_event']
    list_filter = ['is_published']
    list_editable = ['is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {"slug": ("title",)}


# === Мероприятия ===
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location']
    list_filter = ['date']
    search_fields = ['title', 'location']
    ordering = ['-date']


# === Синглтоны ===
@admin.register(SEOAndContent)
class SEOAndContentAdmin(admin.ModelAdmin):
    pass


@admin.register(UsefulInfo)
class UsefulInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(AboutDoctor)
class AboutDoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    pass


# === Прочее ===
@admin.register(ClinicLocation)
class ClinicLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'order']
    ordering = ['order']


@admin.register(WorkExample)
class WorkExampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'order']
    list_filter = ['is_published']
    ordering = ['order']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'badge_color', 'order']
    ordering = ['order']


@admin.register(EducationItem)
class EducationItemAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'order']
    ordering = ['order']
