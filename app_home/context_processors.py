from .models import SiteSettings, Service


def site_logo(request):
    settings_obj = SiteSettings.objects.first()
    context = {'site_logo': '/static/img/emblem.png'}
    context['site_phone'] = '+375292044963'
    context['site_phone_display'] = '+375 (29) 204-49-63'
    context['site_viber'] = 'viber://chat?number=%2B375292044963'
    context['site_whatsapp'] = 'https://wa.me/375292044963'
    context['site_telegram'] = 'https://t.me/Yuramolq'
    context['services_menu'] = Service.objects.filter(is_active=True)
    if settings_obj:
        if settings_obj.logo:
            context['site_logo'] = settings_obj.logo.url
        if settings_obj.phone:
            context['site_phone'] = settings_obj.phone
        if settings_obj.phone_display:
            context['site_phone_display'] = settings_obj.phone_display
        if settings_obj.viber_link:
            context['site_viber'] = settings_obj.viber_link
        if settings_obj.whatsapp_link:
            context['site_whatsapp'] = settings_obj.whatsapp_link
        if settings_obj.telegram_link:
            context['site_telegram'] = settings_obj.telegram_link
    return context
