from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404
from datetime import date
from urllib.parse import urlsplit
from .models import Lead, SiteSettings
from .seo import REGIONS, FAQ_HOME, FAQ_PROCHISTKA, FAQ_SANTEHNIKA, REGION_SERVICE_META
import requests


def home(request):
    return render(request, 'home.html', {'faq': FAQ_HOME, 'social_text': 'Здравствуйте! Нужен мастер', 'nav_active': 'home'})


def prochistka(request):
    crumbs = [{'url': '/prochistka-kanalizatsii/', 'name': 'Прочистка канализации в Барановичах'}]
    return render(request, 'prochistka.html', {'faq': FAQ_PROCHISTKA, 'crumbs': crumbs, 'social_text': 'Здравствуйте! Нужна прочистка канализации', 'nav_active': 'prochistka'})


def santehnika(request):
    crumbs = [{'url': '/santekhnicheskie-raboty/', 'name': 'Услуги сантехника в Барановичах'}]
    return render(request, 'santehnika.html', {'faq': FAQ_SANTEHNIKA, 'crumbs': crumbs, 'social_text': 'Здравствуйте! Нужны сантехнические работы', 'nav_active': 'santehnika'})


def about(request):
    crumbs = [{'url': '/o-nas/', 'name': 'О мастере'}]
    return render(request, 'about.html', {'crumbs': crumbs, 'social_text': 'Здравствуйте! Пишу с сайта stepanych.by, нужен мастер', 'nav_active': 'about'})


def contacts(request):
    crumbs = [{'url': '/kontakty/', 'name': 'Контакты'}]
    return render(request, 'contacts.html', {'crumbs': crumbs, 'social_text': 'Здравствуйте! У меня вопрос по услугам', 'nav_active': 'contacts'})


def regions_index(request):
    crumbs = [{'url': '/santehnik/', 'name': 'Регионы выездов'}]
    return render(request, 'regions_index.html', {'crumbs': crumbs, 'social_text': 'Здравствуйте! Нужен мастер с выездом', 'nav_active': ''})


def region(request, slug):
    item = next((r for r in REGIONS if r['slug'] == slug), None)
    if not item:
        raise Http404
    faq = [
        {'q': f"Сколько стоит выезд в {item['acc']}?", 'a': f"{item['name']} — примерно {item['km']} км от Барановичей. Стоимость выезда зависит от расстояния и объёма работ: цену называем по телефону, до начала работ."},
        {'q': f"Как быстро вы приезжаете в {item['acc']}?", 'a': 'По договорённости, обычно в течение одного-двух дней. Аварийные случаи — по созвону, стараемся приехать быстрее.'},
        {'q': 'Какие работы вы выполняете на выезде?', 'a': 'Прочистка канализации и устранение засоров, а также сантехнические работы: смесители, сифоны, унитазы, подводка, стояки, отопление, водопровод.'},
    ]
    crumbs = [
        {'url': '/santehnik/', 'name': 'Регионы выездов'},
        {'url': f"/santehnik/{item['slug']}/", 'name': item['name']},
    ]
    return render(request, 'region.html', {'region': item, 'faq': faq, 'crumbs': crumbs, 'social_text': f"Здравствуйте! Нужна прочистка канализации или сантехработы в {item['name_prep']}", 'nav_active': ''})


def region_service(request, slug, service):
    item = next((r for r in REGIONS if r['slug'] == slug), None)
    meta = REGION_SERVICE_META.get(service)
    if not item or not meta:
        raise Http404
    faq = meta['faq'][:3] + [
        {'q': f"Сколько стоит выезд в {item['acc']}?", 'a': f"{item['name']} — примерно {item['km']} км от Барановичей. Стоимость выезда зависит от расстояния и объёма работ: цену называем по телефону, до начала работ."},
        {'q': f"Как быстро вы приезжаете в {item['acc']}?", 'a': 'По договорённости, обычно в течение одного-двух дней. Аварийные случаи — по созвону, стараемся приехать быстрее.'},
    ]
    crumbs = [
        {'url': f'/{service}/', 'name': meta['name']},
        {'url': f'/{service}/{slug}/', 'name': item['name']},
    ]
    ctx = {
        'region': item,
        'service': service,
        'meta': meta,
        'faq': faq,
        'crumbs': crumbs,
        'nav_active': meta['key'],
        'social_text': meta['social'].format(prep=item['name_prep']),
    }
    return render(request, 'region_service.html', ctx)


def robots(request):
    host = f'{request.scheme}://{request.get_host()}'
    txt = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /admin\n'
        'Disallow: /feedback\n'
        f'Sitemap: {host}/sitemap.xml\n'
    )
    return HttpResponse(txt, content_type='text/plain; charset=utf-8')


def sitemap(request):
    host = f'{request.scheme}://{request.get_host()}'
    urls = [
        ('/', '1.0'),
        ('/prochistka-kanalizatsii/', '0.9'),
        ('/santekhnicheskie-raboty/', '0.9'),
        ('/santehnik/', '0.8'),
        ('/o-nas/', '0.5'),
        ('/kontakty/', '0.5'),
    ]
    urls += [(f"/santehnik/{r['slug']}/", '0.7') for r in REGIONS]
    urls += [(f"/{s}/{r['slug']}/", '0.7') for r in REGIONS for s in ('prochistka-kanalizatsii', 'santekhnicheskie-raboty')]
    today = date.today().isoformat()
    items = ''.join(
        f'<url><loc>{host}{path}</loc><lastmod>{today}</lastmod><priority>{priority}</priority></url>'
        for path, priority in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'{items}</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml; charset=utf-8')


PHONE_CODES_2 = ('17', '25', '29', '33', '44')
PHONE_CODES_3 = ('152', '154', '156', '159', '162', '163', '164', '165', '171', '173', '174', '176', '177', '179', '212', '213', '214', '215', '216', '222', '223', '224', '225', '226', '232', '233', '234', '235', '236')


def back_url(request):
    referer = request.META.get('HTTP_REFERER', '')
    parts = urlsplit(referer)
    if not referer or (parts.netloc and parts.netloc != request.get_host()):
        return '/#order'
    query = f'?{parts.query}' if parts.query else ''
    return f'{parts.path}{query}#order'


def normalize_phone(raw):
    digits = ''.join(ch for ch in raw if ch.isdigit())
    if digits.startswith('8375') and len(digits) == 13:
        digits = digits[1:]
    elif digits.startswith('8') and len(digits) == 11:
        digits = digits[1:]
    if digits.startswith('0') and len(digits) == 10:
        digits = '375' + digits[1:]
    if len(digits) != 12 or not digits.startswith('375'):
        return ''
    if digits[3:5] not in PHONE_CODES_2 and digits[3:6] not in PHONE_CODES_3:
        return ''
    return '+' + digits


@require_POST
def feedback(request):
    settings_obj = SiteSettings.objects.first()
    if settings_obj and settings_obj.disable_leads:
        messages.error(request, 'Приём заявок временно остановлен.')
        return redirect(back_url(request))

    if request.POST.get('company', '').strip():
        messages.success(request, 'Заявка отправлена! Мы перезвоним вам в ближайшее время.')
        return redirect(back_url(request))

    phone_raw = request.POST.get('phone', '').strip()
    description = request.POST.get('description', '').strip()

    if not phone_raw or not description:
        messages.error(request, 'Пожалуйста, заполните все поля формы.')
        return redirect(back_url(request))

    phone = normalize_phone(phone_raw)
    if not phone:
        messages.error(request, 'Проверьте номер телефона: формат +375 (XX) XXX-XX-XX.')
        return redirect(back_url(request))

    site_phone = settings_obj.phone if settings_obj and settings_obj.phone else '+375292044963'
    if phone == normalize_phone(site_phone):
        messages.error(request, 'Это номер сайта, а не ваш. Укажите свой номер, чтобы мы могли перезвонить.')
        return redirect(back_url(request))

    lead = Lead.objects.create(phone=phone, description=description)

    if settings_obj and settings_obj.bot_token:
        text = f'Новая заявка с сайта stepanych.by\n\nТелефон: {phone}\n\nОписание: {description}'
        recipients = settings_obj.recipients_list.filter(is_active=True)
        for recipient in recipients:
            try:
                requests.post(
                    f'https://api.telegram.org/bot{settings_obj.bot_token}/sendMessage',
                    data={'chat_id': recipient.chat_id, 'text': text},
                    timeout=5,
                )
            except Exception:
                pass

    messages.success(request, 'Заявка отправлена! Мы перезвоним вам в ближайшее время.')
    return redirect(back_url(request))
