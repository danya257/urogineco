"""Модель заявки с формы «Записаться на приём» — фиксация согласия по 152-ФЗ."""
from django.db import models


class Lead(models.Model):
    """Заявка на запись — храним ПД пациента + отметку о согласии на обработку."""

    name = models.CharField('Имя', max_length=150)
    phone = models.CharField('Телефон / Telegram', max_length=100)
    message = models.TextField('Что беспокоит')
    attachment = models.FileField(
        'Вложение от пациентки', upload_to='leads/%Y/%m/', blank=True, null=True,
        help_text='Выписки, результаты обследований',
    )
    mail_sent = models.BooleanField('Письмо врачу отправлено', default=False)

    consent_given = models.BooleanField(
        'Согласие на обработку ПД',
        default=False,
        help_text='Чекбокс на форме подтверждён пользователем',
    )
    consent_at = models.DateTimeField('Дата согласия', auto_now_add=True)

    ip_address = models.GenericIPAddressField('IP отправителя', null=True, blank=True)
    user_agent = models.TextField('User-Agent браузера', blank=True)

    is_processed = models.BooleanField('Обработано', default=False)
    admin_note = models.TextField('Заметки администратора', blank=True)

    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка (запись на приём)'
        verbose_name_plural = 'Заявки (записи на приём)'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone} ({self.created_at:%d.%m.%Y %H:%M})'
