import io
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
FONTS = Path(__file__).resolve().parent / 'fonts'
SRC = Path(__file__).resolve().parent / 'src'
IMG = REPO / 'static' / 'img'

PHONE = '+375 (29) 204-49-63'

BG = (13, 43, 69)
RED = (226, 57, 57)
MUT = (159, 182, 212)

MONTS = {
    'ExtraBold': 'https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-ExtraBold.ttf',
    'SemiBold': 'https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-SemiBold.ttf',
    'Bold': 'https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf',
}
INTER_ZIP = 'https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip'
INTER_NAMES = ['Inter-ExtraBold.ttf', 'Inter-SemiBold.ttf', 'Inter-Regular.ttf']


def ensure_fonts():
    FONTS.mkdir(exist_ok=True)
    missing_m = [k for k in MONTS if not (FONTS / f'Montserrat-{k}.ttf').exists()]
    if missing_m:
        for k in missing_m:
            urllib.request.urlretrieve(MONTS[k], FONTS / f'Montserrat-{k}.ttf')
    missing_i = [n for n in INTER_NAMES if not (FONTS / n).exists()]
    if missing_i:
        data = urllib.request.urlopen(INTER_ZIP).read()
        zf = zipfile.ZipFile(io.BytesIO(data))
        for n in missing_i:
            name = next(i for i in zf.namelist() if i.endswith('/' + n) or i == n)
            (FONTS / n).write_bytes(zf.read(name))


def F(weight, size, fam='Montserrat'):
    return ImageFont.truetype(FONTS / f'{fam}-{weight}.ttf', size)


S = 1080


def tracked(d, cy, text, weight, size, fill, tr, maxw=1010):
    while True:
        font = F(weight, size)
        ws = [d.textlength(ch, font=font) for ch in text]
        total = sum(ws) + tr * (len(text) - 1)
        if total <= maxw or size <= 24:
            break
        size -= 2
    x = (S - total) / 2
    for ch, w in zip(text, ws):
        d.text((x, cy), ch, font=font, fill=fill, anchor='lm')
        x += w + tr
    return total


def emblem_masked():
    emb = Image.open(SRC / 'emblem-1024.png').convert('RGBA')
    mask = Image.new('L', emb.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, emb.size[0], emb.size[1]), fill=255)
    return emb, mask


def put_emblem(img, emb, mask, dsize, cy):
    e = emb.resize((dsize, dsize), Image.LANCZOS)
    m = mask.resize((dsize, dsize), Image.LANCZOS)
    img.paste(e, ((S - dsize) // 2, cy - dsize // 2), m)


def square_pill(d, cy, fs=58, pad=96, h=100):
    pf = F('Bold', fs)
    ws = [d.textlength(ch, font=pf) for ch in PHONE]
    total = sum(ws) + 4 * (len(PHONE) - 1)
    w = total + pad
    d.rounded_rectangle(((S - w) // 2, cy - h // 2, (S + w) // 2, cy + h // 2), radius=30, fill=RED)
    x = (S - total) / 2
    for ch, cw in zip(PHONE, ws):
        d.text((x, cy + 2), ch, font=pf, fill=(255, 255, 255), anchor='lm')
        x += cw + 4


def square_avr(emb, mask):
    img = Image.new('RGBA', (S, S), BG + (255,))
    d = ImageDraw.Draw(img)
    put_emblem(img, emb, mask, 310, 240)
    tracked(d, 458, 'СТЕПАНЫЧ', 'ExtraBold', 62, (255, 255, 255), 10)
    tracked(d, 578, 'ПРОЧИСТКА', 'ExtraBold', 84, (255, 255, 255), 5)
    tracked(d, 676, 'КАНАЛИЗАЦИИ', 'ExtraBold', 84, (255, 255, 255), 5)
    tracked(d, 766, 'САНТЕХНИЧЕСКИЕ РАБОТЫ', 'SemiBold', 40, MUT, 12)
    tracked(d, 826, 'МАСТЕР НА ЧАС', 'SemiBold', 40, MUT, 12)
    square_pill(d, 940)
    img.convert('RGB').save(IMG / 'square-avr.png', optimize=True)


def square_santehnika(emb, mask):
    img = Image.new('RGBA', (S, S), BG + (255,))
    d = ImageDraw.Draw(img)
    put_emblem(img, emb, mask, 310, 240)
    tracked(d, 458, 'СТЕПАНЫЧ', 'ExtraBold', 62, (255, 255, 255), 10)
    tracked(d, 578, 'САНТЕХНИЧЕСКИЕ', 'ExtraBold', 84, (255, 255, 255), 5)
    tracked(d, 676, 'РАБОТЫ', 'ExtraBold', 84, (255, 255, 255), 5)
    tracked(d, 766, 'СМЕСИТЕЛИ · СИФОНЫ · УНИТАЗЫ', 'SemiBold', 34, MUT, 5)
    tracked(d, 826, 'СТОЯКИ · ОТОПЛЕНИЕ · ВОДОПРОВОД', 'SemiBold', 34, MUT, 5)
    square_pill(d, 940)
    img.convert('RGB').save(IMG / 'square-santehnika.png', optimize=True)


def square_prochistka(emb, mask):
    img = Image.new('RGBA', (S, S), BG + (255,))
    d = ImageDraw.Draw(img)
    put_emblem(img, emb, mask, 190, 108)
    tracked(d, 238, 'СТЕПАНЫЧ', 'ExtraBold', 50, (255, 255, 255), 9)
    tracked(d, 318, 'ПРОЧИСТКА', 'ExtraBold', 68, (255, 255, 255), 5)
    w2 = tracked(d, 396, 'КАНАЛИЗАЦИИ', 'ExtraBold', 68, (255, 255, 255), 5)
    src = Image.open(SRC / 'mashinka-xl.jpg').convert('RGBA')
    w0, h0 = src.size
    crop = src.crop((int(0.14 * w0), int(0.12 * h0), int(0.87 * w0), int(0.86 * h0)))
    pw = int(round(w2))
    phh = int(round(pw / (crop.width / crop.height)))
    ph = crop.resize((pw, phh), Image.LANCZOS)
    mm = Image.new('L', ph.size, 0)
    ImageDraw.Draw(mm).rounded_rectangle((0, 0, ph.size[0], ph.size[1]), radius=20, fill=255)
    px, py = (S - pw) // 2, 455
    img.paste(ph, (px, py), mm)
    d = ImageDraw.Draw(img)
    pcy = py + phh + 12 + 47
    d.rounded_rectangle(((S - pw) // 2, pcy - 47, (S + pw) // 2, pcy + 47), radius=30, fill=RED)
    ps = 44
    while ps > 30:
        pf = F('Bold', ps)
        ws = [d.textlength(ch, font=pf) for ch in PHONE]
        total = sum(ws) + 4 * (len(PHONE) - 1)
        if total <= pw - 100:
            break
        ps -= 2
    x = (S - total) / 2
    for ch, cw in zip(PHONE, ws):
        d.text((x, pcy + 2), ch, font=pf, fill=(255, 255, 255), anchor='lm')
        x += cw + 4
    img.convert('RGB').save(IMG / 'square-prochistka.png', optimize=True)


def main():
    ensure_fonts()
    emb, mask = emblem_masked()
    square_avr(emb, mask)
    square_santehnika(emb, mask)
    square_prochistka(emb, mask)
    print('PHONE:', PHONE)
    print('regenerated: square-avr.png, square-santehnika.png, square-prochistka.png')


if __name__ == '__main__':
    main()
