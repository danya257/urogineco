"""Админка для блоков, добавленных по ТЗ от 09.07.2026."""
from django.contrib import admin

from .models import HeroStat, DoctorLetter, HeroSlide, Disease, Memo, Faq, Publication


@admin.register(HeroStat)
class HeroStatAdmin(admin.ModelAdmin):
    list_display = ('order', 'value', 'label', 'is_visible')
    list_editable = ('value', 'label', 'is_visible')
    ordering = ('order',)


@admin.register(DoctorLetter)
class DoctorLetterAdmin(admin.ModelAdmin):
    fields = ('is_visible', 'greeting', 'intro', 'text', 'signature', 'photo', 'banner')


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('order', 'kind', 'title', 'is_visible')
    list_editable = ('kind', 'title', 'is_visible')
    ordering = ('order',)
    fieldsets = (
        (None, {'fields': ('kind', 'order', 'is_visible')}),
        ('Содержимое', {'fields': ('title', 'subtitle', 'image', 'video_file')}),
        ('Кнопка', {'fields': ('button_text', 'button_url')}),
    )


class FaqInline(admin.StackedInline):
    model = Faq
    extra = 0
    fields = ('order', 'question', 'answer', 'is_visible')


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('order', 'nav_title', 'counter', 'is_visible')
    list_editable = ('nav_title', 'counter', 'is_visible')
    ordering = ('order',)
    prepopulated_fields = {'slug': ('nav_title',)}
    inlines = [FaqInline]
    fieldsets = (
        (None, {'fields': ('nav_title', 'slug', 'order', 'is_visible', 'icon')}),
        ('Баннер', {'fields': ('title', 'subtitle', 'counter', 'banner')}),
        ('Видео', {'fields': ('video_file', 'video_url', 'video_poster', 'video_caption')}),
        ('Карточка на главной', {'fields': ('short_description',)}),
        ('Текст страницы', {'fields': (
            'lead', 'highlight_title', 'highlight_text',
            'advantages', 'benefits', 'appeal', 'details', 'about',
        )}),
        ('Связи', {'fields': ('memo',)}),
    )


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ('order', 'number', 'title', 'is_visible')
    list_editable = ('number', 'title', 'is_visible')
    ordering = ('order',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('order', 'question', 'disease', 'is_visible')
    list_editable = ('question', 'disease', 'is_visible')
    list_filter = ('disease',)
    ordering = ('order',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'is_visible')
    list_editable = ('title', 'is_visible')
    ordering = ('order',)
