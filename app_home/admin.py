from django.contrib import admin
from .models import SiteSettings, Lead, Service, TelegramRecipient


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
    list_display = ('phone', 'created_at')
    readonly_fields = ('phone', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('phone', 'description')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price_text', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active',)
    search_fields = ('title', 'short_description')
    ordering = ('sort_order', 'id')
