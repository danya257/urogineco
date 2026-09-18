"""Русская экранная типографика: неразрывные пробелы после коротких слов и перед тире."""
import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

NBSP = ' '
SHORT_WORDS = (
    'а|в|во|и|к|ко|о|об|обо|с|со|у|но|на|не|ни|по|от|до|за|из|изо|для|без|при|про|над|под|перед|через|или|что|как|же|ли|бы'
)
_short_re = re.compile(r'(?<![\w<>/="\'-])(' + SHORT_WORDS + r')\s+(?=[^\s<])', re.IGNORECASE)
_dash_re = re.compile(r'\s+(—|–)\s')
_num_re = re.compile(r'(\d)\s+(?=[а-яА-ЯёЁ%+])')
_split_re = re.compile(r'(<[^>]+>)')


def _typograph_text(chunk):
    chunk = _dash_re.sub(NBSP + r'\1 ', chunk)
    chunk = _short_re.sub(lambda m: m.group(1) + NBSP, chunk)
    chunk = _short_re.sub(lambda m: m.group(1) + NBSP, chunk)
    chunk = _num_re.sub(r'\1' + NBSP, chunk)
    return chunk


@register.filter(name='typo')
def typo(value):
    if value is None:
        return ''
    html = str(conditional_escape(value))
    parts = _split_re.split(html)
    out = [p if p.startswith('<') else _typograph_text(p) for p in parts]
    return mark_safe(''.join(out))


@register.filter(name='plain')
def plain(value):
    """Текст из rich-поля без тегов и HTML-сущностей, с типографикой."""
    import html as _html
    from django.utils.html import strip_tags
    return typo(_html.unescape(strip_tags(str(value or ''))).strip())


@register.filter(name='accent_title')
def accent_title(value):
    """Заголовок с акцентом: часть после «|» (или после первого предложения) — курсивом."""
    if not value:
        return ''
    raw = str(value)
    if '|' in raw:
        head, tail = raw.split('|', 1)
    else:
        m = re.match(r'^(.+?[.!?])\s+(.+)$', raw)
        if not m:
            return typo(raw)
        head, tail = m.group(1), m.group(2)
    return mark_safe(f'{typo(head.strip())} <em>{typo(tail.strip())}</em>')
