from django.contrib import admin
from .models import SiteSettings, Lead


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
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
        ('Telegram уведомления', {
            'fields': ('bot_token', 'recipients')
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('phone', 'created_at')
    readonly_fields = ('phone', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('phone', 'description')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
