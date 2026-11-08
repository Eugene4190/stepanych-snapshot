from django.contrib import admin
from .models import SiteSettings, Lead, TelegramRecipient


class TelegramRecipientInline(admin.TabularInline):
    model = TelegramRecipient
    extra = 1


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'disable_leads')
    inlines = [TelegramRecipientInline]
    fieldsets = (
        ('Контакты', {
            'fields': ('phone', 'phone_display')
        }),
        ('Социальные сети', {
            'fields': ('viber_link', 'whatsapp_link', 'telegram_link')
        }),
        ('Лого', {
            'fields': ('logo',)
        }),
        ('Заявки', {
            'fields': ('disable_leads',)
        }),
        ('Тексты инфоплашки', {
            'fields': (('info1_title', 'info1_text'), ('info2_title', 'info2_text'), ('info3_title', 'info3_text'), ('info4_title', 'info4_text'))
        }),
        ('Telegram уведомления', {
            'fields': ('bot_token',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('phone', 'created_at', 'source')
    readonly_fields = ('phone', 'description', 'source', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('phone', 'description')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
