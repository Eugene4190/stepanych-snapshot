from urllib.parse import quote

from django import template

register = template.Library()


@register.filter
def social_href(link, text):
    if not link or not text:
        return link
    if not link.startswith('http'):
        return link
    sep = '&' if '?' in link else '?'
    return f'{link}{sep}text={quote(text)}'
