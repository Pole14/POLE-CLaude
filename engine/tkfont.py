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


def box(lines, size, EMO):
    f = font(size); asc, desc = f.getmetrics()
    padx = int(size * 0.30); lh = int(size * 1.22); r = int(size * 0.26)
    rows = [_layout(l, f, size) for l in lines]
    W = int(max(w for _, w in rows) + 2 * padx + 20); H = lh * len(rows) + 20
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (items, w) in enumerate(rows):
        x0 = (W - w) / 2 - padx; y0 = 10 + i * lh
        d.rounded_rectangle((x0, y0, x0 + w + 2 * padx, y0 + lh), r, fill=(255, 255, 255, 255))
    for i, (items, w) in enumerate(rows):
        bx = (W - w) / 2; by = 10 + i * lh + (lh - (asc + desc)) / 2 + size * 0.02
        for k, v, ox in items:
            if k == 't':
                d.text((bx + ox, by), v, font=f, fill=(18, 18, 18, 255))
            else:
                e = EMO[v].resize((size, size), Image.LANCZOS)
                im.alpha_composite(e, (int(bx + ox), int(by + asc - size * 0.86)))
    return im
