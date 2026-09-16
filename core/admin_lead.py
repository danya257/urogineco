"""Регистрация модели Lead в админке — только чтение ключевых полей + отметка «обработано»."""
from django.contrib import admin
from .legal_models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'phone', 'is_processed', 'mail_sent', 'ip_address')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'phone', 'message')
    readonly_fields = (
        'name', 'phone', 'message', 'attachment', 'mail_sent',
        'consent_given', 'consent_at',
        'ip_address', 'user_agent',
        'created_at',
    )
    fields = (
        'created_at', 'name', 'phone', 'message', 'attachment', 'mail_sent',
        'consent_given', 'consent_at',
        'ip_address', 'user_agent',
        'is_processed', 'admin_note',
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False
