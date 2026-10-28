import re
from urllib.parse import unquote

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


def normalize_viber_link(value):
    digits = re.sub(r'\D', '', unquote(value or ''))
    if not digits:
        return value
    return f'viber://chat?number=%2B{digits}'


def validate_contact_link(value):
    if value.startswith('viber://'):
        if len(value) <= len('viber://'):
            raise ValidationError('Введите ссылку вида viber://chat?number=…', code='invalid')
        return
    URLValidator(schemes=['http', 'https'])(value)


class SiteSettings(models.Model):
    phone = models.CharField(max_length=50, default='+375292044963', verbose_name='Контактный номер телефона')
    phone_display = models.CharField(max_length=50, default='+375 (29) 204-49-63', verbose_name='Номер телефона для отображения')
    viber_link = models.CharField(max_length=200, blank=True, default='viber://chat?number=%2B375292044963', verbose_name='Ссылка Viber', validators=[validate_contact_link])
    whatsapp_link = models.URLField(blank=True, default='https://wa.me/375292044963', verbose_name='Ссылка WhatsApp')
    telegram_link = models.URLField(blank=True, default='https://t.me/Yuramolq', verbose_name='Ссылка Telegram')
    bot_token = models.CharField(max_length=255, blank=True, verbose_name='Токен бота Telegram')
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name='Логотип сайта')
    disable_leads = models.BooleanField(default=False, verbose_name='Остановить приём заявок')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.viber_link = normalize_viber_link(self.viber_link)
        super().save(*args, **kwargs)


class TelegramRecipient(models.Model):
    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='recipients_list', verbose_name='Настройки сайта')
    chat_id = models.CharField(max_length=50, verbose_name='Chat ID')
    name = models.CharField(max_length=100, blank=True, verbose_name='Имя/описание')
    is_active = models.BooleanField(default=True, verbose_name='Получать уведомления')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    class Meta:
        verbose_name = 'Получатель уведомлений'
        verbose_name_plural = 'Получатели уведомлений'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name or self.chat_id


class Lead(models.Model):
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    description = models.TextField(verbose_name='Описание проблемы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.phone} - {self.created_at:%d.%m.%Y %H:%M}'


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL-идентификатор')
    short_description = models.TextField(verbose_name='Краткое описание')
    price_text = models.CharField(max_length=100, blank=True, verbose_name='Текст цены')
    description = models.TextField(blank=True, verbose_name='Полное описание')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title
