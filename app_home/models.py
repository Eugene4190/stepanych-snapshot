from django.db import models


class SiteSettings(models.Model):
    phone = models.CharField(max_length=50, default='+375292044963', verbose_name='Контактный номер телефона')
    phone_display = models.CharField(max_length=50, default='+375 (29) 204-49-63', verbose_name='Номер телефона для отображения')
    viber_link = models.URLField(blank=True, default='viber://chat?number=%2B375292044963', verbose_name='Ссылка Viber')
    whatsapp_link = models.URLField(blank=True, default='https://wa.me/375292044963', verbose_name='Ссылка WhatsApp')
    telegram_link = models.URLField(blank=True, default='https://t.me/Yuramolq', verbose_name='Ссылка Telegram')
    bot_token = models.CharField(max_length=255, blank=True, verbose_name='Токен бота Telegram')
    recipients = models.TextField(
        blank=True,
        verbose_name='Получатели уведомлений',
        help_text='Список chat_id получателей, по одному на строку'
    )
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name='Логотип сайта')
    disable_leads = models.BooleanField(default=False, verbose_name='Остановить приём заявок')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'


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
