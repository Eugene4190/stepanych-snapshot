from .models import SiteSettings, Service, normalize_viber_link
from .seo import REGIONS


def form_draft(request):
    draft = request.session.pop('form_draft', None) or {}
    return {'form_phone': draft.get('phone', ''), 'form_description': draft.get('description', '')}


def site_logo(request):
    settings_obj = SiteSettings.objects.first()
    context = {'site_logo': '/static/img/emblem.png'}
    context['site_phone'] = '+375292044963'
    context['site_phone_display'] = '+375 (29) 204-49-63'
    context['site_viber'] = 'viber://chat?number=%2B375292044963'
    context['site_whatsapp'] = 'https://wa.me/375292044963'
    context['site_telegram'] = 'https://t.me/Yuramolq'
    context['social_text'] = 'Здравствуйте! Пишу с сайта stepanych.by, нужен мастер'
    context['services_menu'] = Service.objects.filter(is_active=True)
    context['regions'] = REGIONS
    context['disable_leads'] = False
    info_defs = [
        ('fa-file-contract', 'Официально', 'ИП, УНП 291568475'),
        ('fa-clock', 'Без выходных 9:00–23:00', 'аварии — по договорённости'),
        ('fa-credit-card', 'Оплата после работы', 'наличные и безнал для юр. и физ. лиц'),
        ('fa-map-marker-alt', 'Барановичи и вся область', 'любые населённые пункты по договорённости'),
    ]
    info_items = []
    for idx, (icon, dtitle, dtext) in enumerate(info_defs, start=1):
        title, text = dtitle, dtext
        if settings_obj:
            title = getattr(settings_obj, f'info{idx}_title', '') or dtitle
            text = getattr(settings_obj, f'info{idx}_text', '') or dtext
        info_items.append({'icon': icon, 'title': title, 'text': text})
    context['info_items'] = info_items
    if settings_obj:
        if settings_obj.logo:
            context['site_logo'] = settings_obj.logo.url
        if settings_obj.phone:
            context['site_phone'] = settings_obj.phone
        if settings_obj.phone_display:
            context['site_phone_display'] = settings_obj.phone_display
        if settings_obj.viber_link:
            context['site_viber'] = normalize_viber_link(settings_obj.viber_link)
        if settings_obj.whatsapp_link:
            context['site_whatsapp'] = settings_obj.whatsapp_link
        if settings_obj.telegram_link:
            context['site_telegram'] = settings_obj.telegram_link
        context['disable_leads'] = settings_obj.disable_leads
    return context
