from pathlib import Path
from urllib.parse import quote

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def asset_url(path):
    full = Path(settings.BASE_DIR) / 'static' / path
    try:
        version = int(full.stat().st_mtime)
    except OSError:
        return f'/static/{path}'
    return f'/static/{path}?v={version}'


@register.filter
def social_href(link, text):
    if not link or not text:
        return link
    if not link.startswith('http'):
        return link
    sep = '&' if '?' in link else '?'
    return f'{link}{sep}text={quote(text)}'
