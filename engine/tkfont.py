"""Texto nativo de TikTok (fuente "Classic") — calibrado el 8 nov 2026 contra un vídeo 1080p real.
Fuente: TikTok Sans variable (la oficial). Contorno: peso 690, opsz 36, trazo size/13, interlineado 1.1, interletrado -1,8 %.
La caja blanca NO se toca: sigue con tktext.render_block (TikTok Sans 600), Pol la da por perfecta.
- outline(lines, size, EMO): letras blancas con contorno negro .
- box(lines, size, EMO): estilo "fondo blanco": cada línea en su caja blanca redondeada, texto negro.
Las líneas aceptan emojis propios con |emo:nombre|.
"""
import os, re
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
_F = {}
WGHT = 690


def font(size, w=WGHT):
    k = (size, w)
    if k not in _F:
        f = ImageFont.truetype(D + 'fonts/tiktoksans_var.ttf', size); f.set_variation_by_axes([36, 100, w, 0]); _F[k] = f
    return _F[k]


def parse(line):
    out = []
    for p in re.split(r'(\|emo:\w+\|)', line):
        if not p: continue
        m = re.fullmatch(r'\|emo:(\w+)\|', p)
        out.append(('e', m.group(1)) if m else ('t', p))
    return out


TR = -0.018  # interletrado (fracción del tamaño), la Classic va algo más apretada


def _layout(line, f, size, tr=0.0):
    items = []; x = 0.0
    for k, v in parse(line):
        if k == 't':
            if tr:
                for ch in v:
                    items.append(('t', ch, x)); x += f.getlength(ch) + tr * size
            else:
                items.append(('t', v, x)); x += f.getlength(v)
        else:
            items.append(('e', v, x + size * 0.04)); x += size * 1.08
    return items, x


def outline(lines, size, EMO, sd=13):
    f = font(size); st = max(2, round(size / sd)); asc, desc = f.getmetrics(); lh = int(size * 1.1)
    rows = [_layout(l, f, size, TR) for l in lines]
    W = int(max(w for _, w in rows) + 2 * st + 24); H = int(lh * (len(rows) - 1) + asc + desc + 2 * st + 24)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (items, w) in enumerate(rows):
        bx = (W - w) / 2; by = 12 + st + i * lh
        for k, v, ox in items:
            if k == 't':
                d.text((bx + ox, by), v, font=f, fill='white', stroke_width=st, stroke_fill='black')
            else:
                e = EMO[v].resize((size, size), Image.LANCZOS)
                im.alpha_composite(e, (int(bx + ox), int(by + asc - size * 0.86)))
    return im


def box(lines, size, EMO, bg=(255, 255, 255, 255), fg=(18, 18, 18, 255)):
    f = font(size); asc, desc = f.getmetrics()
    padx = int(size * 0.30); lh = int(size * 1.22); r = int(size * 0.26)
    rows = [_layout(l, f, size) for l in lines]
    W = int(max(w for _, w in rows) + 2 * padx + 20); H = lh * len(rows) + 20
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (items, w) in enumerate(rows):
        x0 = (W - w) / 2 - padx; y0 = 10 + i * lh
        d.rounded_rectangle((x0, y0, x0 + w + 2 * padx, y0 + lh), r, fill=bg)
    for i, (items, w) in enumerate(rows):
        bx = (W - w) / 2; by = 10 + i * lh + (lh - (asc + desc)) / 2 + size * 0.02
        for k, v, ox in items:
            if k == 't':
                d.text((bx + ox, by), v, font=f, fill=fg)
            else:
                e = EMO[v].resize((size, size), Image.LANCZOS)
                im.alpha_composite(e, (int(bx + ox), int(by + asc - size * 0.86)))
    return im


# ---- Estilo "tt" (8 nov 2026, orden de Pol): TikTok Sans Bold estática, blanco #FFFFFF,
# contorno negro sólido #000000 de 3-5 px a 1080x1920 (nunca sombra), centrado, máx. 2 líneas.
# Resaltado contenido: palabras entre *asteriscos* en amarillo TikTok.
TT_FONT = D + 'fonts/TikTokSans36pt-Bold.ttf'
HL = (255, 214, 0, 255)
_TF = {}


def tt_font(size):
    if size not in _TF: _TF[size] = ImageFont.truetype(TT_FONT, size)
    return _TF[size]


def _tt_items(line, f, size):
    items = []; x = 0.0
    for k, v in parse(line):
        if k == 'e':
            items.append(('e', v, x + size * 0.04, None)); x += size * 1.08; continue
        for j, seg in enumerate(re.split(r'\*', v)):
            if not seg: continue
            col = HL if j % 2 else (255, 255, 255, 255)
            items.append(('t', seg, x, col)); x += f.getlength(seg)
    return items, x


def tt(lines, size, EMO, maxw=960, stroke=None, maxl=2):
    lines = lines[:maxl]
    while size > 30:
        f = tt_font(size)
        if max(_tt_items(l, f, size)[1] for l in lines) <= maxw: break
        size -= 2
    f = tt_font(size); st = stroke or (5 if size >= 96 else 4 if size >= 48 else 3)
    asc, desc = f.getmetrics(); lh = int(size * 1.14)
    rows = [_tt_items(l, f, size) for l in lines]
    W = int(max(w for _, w in rows) + 2 * st + 16); H = int(lh * (len(rows) - 1) + asc + desc + 2 * st + 16)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (items, w) in enumerate(rows):
        bx = (W - w) / 2; by = 8 + st + i * lh
        for k, v, ox, col in items:
            if k == 't':
                d.text((bx + ox, by), v, font=f, fill=col, stroke_width=st, stroke_fill=(0, 0, 0, 255))
            else:
                e = EMO[v].resize((size, size), Image.LANCZOS)
                im.alpha_composite(e, (int(bx + ox), int(by + asc - size * 0.86)))
    return im


# ---- Estilo "classic" (9 nov 2026): copia 1:1 del texto de TikTok del vídeo PREM100 de la competencia.
# TikTok Sans variable, peso medio (~600), blanco, contorno negro fino (~4 px a 1080), interlineado apretado.
def classic(lines, size, EMO, wght=600, stroke=4, lh=1.06, maxw=1000, maxl=3):
    lines = lines[:maxl]
    while size > 30:
        f = font(size, wght)
        if max(_layout(l, f, size)[1] for l in lines) <= maxw: break
        size -= 2
    f = font(size, wght); asc, desc = f.getmetrics(); L = int(size * lh)
    rows = [_layout(l, f, size) for l in lines]
    W = int(max(w for _, w in rows) + 2 * stroke + 16); H = int(L * (len(rows) - 1) + asc + desc + 2 * stroke + 16)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (items, w) in enumerate(rows):
        bx = (W - w) / 2; by = 8 + stroke + i * L
        for k, v, ox in items:
            if k == 't':
                d.text((bx + ox, by), v, font=f, fill='white', stroke_width=stroke, stroke_fill='black')
            else:
                e = EMO[v].resize((int(size * 1.0), int(size * 1.0)), Image.LANCZOS)
                im.alpha_composite(e, (int(bx + ox), int(by + asc - size * 0.86)))
    return im


# ---- Estilo "stack" (9 nov 2026): título apilado, cada línea con su tamaño (p. ej. HACOO grande / CUPÓN 120€ / (noviembre ✅) pequeño).
# Fuente a elegir (TikTok Sans Bold u Oswald Bold), blanco con contorno negro sólido.
def stack(lines, sizes, EMO, fontfile='TikTokSans36pt-Bold.ttf', maxw=980, gap=0.02):
    rows = []
    for l, s in zip(lines, sizes):
        while s > 30:
            f = ImageFont.truetype(D + 'fonts/' + fontfile, s)
            its, w = _tt_items(l, f, s)
            if w <= maxw: break
            s -= 2
        rows.append((its, w, f, s))
    st = lambda s: 6 if s >= 140 else 5 if s >= 96 else 4
    H = 16; ys = []
    for its, w, f, s in rows:
        asc, desc = f.getmetrics(); ys.append(H); H += int(asc + desc * 0.35 + 2 * st(s) + s * gap)
    H += 16
    W = int(max(w for _, w, _, _ in rows) + 40)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for (its, w, f, s), y in zip(rows, ys):
        bx = (W - w) / 2; asc, _ = f.getmetrics()
        for k, v, ox, col in its:
            if k == 't':
                d.text((bx + ox, y + st(s)), v, font=f, fill=col, stroke_width=st(s), stroke_fill=(0, 0, 0, 255))
            else:
                e = EMO[v].resize((s, s), Image.LANCZOS)
                im.alpha_composite(e, (int(bx + ox), int(y + st(s) + asc - s * 0.86)))
    return im
