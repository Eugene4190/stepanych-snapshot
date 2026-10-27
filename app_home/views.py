from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Lead, SiteSettings
import requests


def home(request):
    return render(request, 'home.html')


def prochistka(request):
    return render(request, 'prochistka.html')


def santehnika(request):
    return render(request, 'santehnika.html')


def about(request):
    return render(request, 'about.html')


def contacts(request):
    return render(request, 'contacts.html')


@require_POST
def feedback(request):
    phone = request.POST.get('phone', '').strip()
    description = request.POST.get('description', '').strip()

    if not phone or not description:
        messages.error(request, 'Пожалуйста, заполните все поля формы.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    lead = Lead.objects.create(phone=phone, description=description)

    settings_obj = SiteSettings.objects.first()
    if settings_obj and settings_obj.bot_token and settings_obj.recipients:
        text = f'Новая заявка с сайта stepanych.by\n\nТелефон: {phone}\n\nОписание: {description}'
        for chat_id in settings_obj.recipients.splitlines():
            chat_id = chat_id.strip()
            if not chat_id:
                continue
            try:
                requests.post(
                    f'https://api.telegram.org/bot{settings_obj.bot_token}/sendMessage',
                    data={'chat_id': chat_id, 'text': text},
                    timeout=5,
                )
            except Exception:
                pass

    messages.success(request, 'Заявка отправлена! Мы перезвоним вам в ближайшее время.')
    return redirect(request.META.get('HTTP_REFERER', '/'))
