from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404
from datetime import date
from .models import Lead, SiteSettings
from .seo import REGIONS, FAQ_HOME, FAQ_PROCHISTKA, FAQ_SANTEHNIKA
import requests


def home(request):
    return render(request, 'home.html', {'faq': FAQ_HOME, 'social_text': 'Здравствуйте! Нужен мастер'})


def prochistka(request):
    crumbs = [{'url': '/prochistka-kanalizatsii/', 'name': 'Прочистка канализации в Барановичах'}]
    return render(request, 'prochistka.html', {'faq': FAQ_PROCHISTKA, 'crumbs': crumbs, 'social_text': 'Здравствуйте! Нужна прочистка канализации'})


def santehnika(request):
    crumbs = [{'url': '/santekhnicheskie-raboty/', 'name': 'Услуги сантехника в Барановичах'}]
    return render(request, 'santehnika.html', {'faq': FAQ_SANTEHNIKA, 'crumbs': crumbs, 'social_text': 'Здравствуйте! Нужны сантехнические работы'})


def about(request):
    crumbs = [{'url': '/o-nas/', 'name': 'О мастере'}]
    return render(request, 'about.html', {'crumbs': crumbs, 'social_text': 'Здравствуйте! Пишу с сайта stepanych.by, нужен мастер'})


def contacts(request):
    crumbs = [{'url': '/kontakty/', 'name': 'Контакты'}]
    return render(request, 'contacts.html', {'crumbs': crumbs, 'social_text': 'Здравствуйте! У меня вопрос по услугам'})


def regions_index(request):
    crumbs = [{'url': '/regiony/', 'name': 'Регионы выездов'}]
    return render(request, 'regions_index.html', {'crumbs': crumbs, 'social_text': 'Здравствуйте! Нужен мастер в Барановичах или районе'})


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
        {'url': '/regiony/', 'name': 'Регионы выездов'},
        {'url': f"/regiony/{item['slug']}/", 'name': item['name']},
    ]
    return render(request, 'region.html', {'region': item, 'faq': faq, 'crumbs': crumbs, 'social_text': f"Здравствуйте! Нужен мастер в {item['name_prep']}"})


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
        ('/regiony/', '0.8'),
        ('/o-nas/', '0.5'),
        ('/kontakty/', '0.5'),
    ]
    urls += [(f"/regiony/{r['slug']}/", '0.7') for r in REGIONS]
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


@require_POST
def feedback(request):
    settings_obj = SiteSettings.objects.first()
    if settings_obj and settings_obj.disable_leads:
        messages.error(request, 'Приём заявок временно остановлен.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    phone = request.POST.get('phone', '').strip()
    description = request.POST.get('description', '').strip()

    if not phone or not description:
        messages.error(request, 'Пожалуйста, заполните все поля формы.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

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
    return redirect(request.META.get('HTTP_REFERER', '/'))
