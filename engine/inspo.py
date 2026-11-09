#!/usr/bin/env python3
"""Formato "inspo" (vídeo de @codigos_hacoo_ que Pol pasó el 9 nov 2026 como referencia).
Uso: inspo.py base.mp4 fx.json out.mp4
- base.mp4: render de native7 (solo tiempos/rmap, sin marcas ni zoom).
- Pantalla completa SIN franjas (Pol: "las franjas negras no"), ventana vertical fija fx.off.
- Textos TikTok (tkfont.tt: TikTok Sans Bold, blanco, contorno negro), tamaño normal, centrados.
- "blurs": transiciones con desenfoque de movimiento vertical [{t, half, px}].
- "circles": círculos rojos a mano que se dibujan solos [{t0, t1, box:[x0,y0,x1,y1], draw}] (coords de salida 1080x1920).
fx.json: {"tot","fps","off","texts":[{t0,t1,y,size,lines}],"blurs":[],"circles":[],"seo"?}
"""
import glob, json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, ROOT + 'engine')
import tkfont

SRC, FX, OUT = sys.argv[1:4]
fx = json.load(open(FX))
W, H = 1080, 1920
FPS = fx.get('fps', 60)
FULL_H = 2340
OFF = int(fx.get('off', 150))

EMO = {}
for f in glob.glob(ROOT + 'engine/emo/n_*.png'):
    EMO[os.path.basename(f)[2:-4]] = Image.open(f).convert('RGBA')
EMO['check'] = Image.open(ROOT + 'engine/emo/check.png').convert('RGBA')
for n, f in {'money': 'b42', 'scream': 'b41', 'shush': 'b40', 'party': 'b51', 'wink': 'b35', 'grin': 'b04'}.items():
    EMO[n] = Image.open(ROOT + f'engine/emo/{f}.png').convert('RGBA')

_C = {}


TSTYLE = fx.get('tstyle', 'tt')


def block(lines, size):
    k = (json.dumps(lines), size)
    if k not in _C:
        ls = [l if l.strip() else ' ' for l in lines]
        _C[k] = tkfont.classic(ls, size, EMO) if TSTYLE == 'classic' else tkfont.tt(ls, size, EMO, maxl=3)
    return _C[k]


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def circle_layer(box, prog, seed, width=9, col=(226, 32, 38, 255)):
    """Óvalo rojo hecho a mano (un poco torcido, con el final pasado de largo), dibujado hasta 'prog' (0..1)."""
    S = 2
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2 * 1.06, (y1 - y0) / 2 * 1.12
    rng = np.random.RandomState(seed)
    ph1, ph2 = rng.uniform(0, 6.28, 2)
    a0 = math.radians(-115 + rng.uniform(-15, 15))
    sweep = math.radians(385) * ease(prog)
    n = max(2, int(140 * ease(prog)))
    pts = []
    for i in range(n + 1):
        a = a0 + sweep * i / n
        k = 1 + 0.035 * math.sin(2 * a + ph1) + 0.015 * math.sin(5 * a + ph2) + 0.05 * (i / 140)
        pts.append(((cx + rx * k * math.cos(a)) * S, (cy + ry * k * math.sin(a)) * S))
    L = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    if len(pts) > 1:
        ImageDraw.Draw(L).line(pts, fill=col, width=width * S, joint='curve')
        r = width * S / 2
        for p in (pts[0], pts[-1]):
            ImageDraw.Draw(L).ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=col)
    return L.resize((W, H), Image.LANCZOS)


TOKRE = __import__('re').compile(r'\|emo:\w+\||\*')


def tokens(line):
    out = []; i = 0
    for m in TOKRE.finditer(line):
        out += list(line[i:m.start()]); out.append(m.group(0)); i = m.end()
    return out + list(line[i:])


def partial(lines, n):
    res = []
    for ln in lines:
        if n <= 0: break
        tk = tokens(ln); res.append(''.join(tk[:n])); n -= len(tk)
    return res


def arrow_solid(a, b, prog, width=15, col=(236, 28, 28, 255)):
    S = 2; (x0, y0), (x1, y1) = a, b; p = ease(prog)
    xe, ye = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    ang = math.atan2(y1 - y0, x1 - x0); hl, hw = 44, 30
    bx, by = xe - hl * math.cos(ang), ye - hl * math.sin(ang)
    L = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line([(x0 * S, y0 * S), (bx * S, by * S)], fill=col, width=width * S)
    nx, ny = -math.sin(ang), math.cos(ang)
    d.polygon([(xe * S, ye * S), ((bx + nx * hw) * S, (by + ny * hw) * S), ((bx - nx * hw) * S, (by - ny * hw) * S)], fill=col)
    return L.resize((W, H), Image.LANCZOS)


def arrow_layer(a, b, prog, seed, width=10, col=(226, 32, 38, 255)):
    """Flecha roja a mano de a (cola) a b (punta), dibujada hasta prog."""
    S = 2; rng = np.random.RandomState(seed)
    (x0, y0), (x1, y1) = a, b
    p = ease(prog); n = 30
    bend = rng.uniform(-0.12, 0.12)
    dx, dy = x1 - x0, y1 - y0
    pts = []
    for i in range(int(n * p) + 1):
        u = i / n
        off = math.sin(u * math.pi) * bend
        pts.append(((x0 + dx * u - dy * off) * S, (y0 + dy * u + dx * off) * S))
    L = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if len(pts) > 1:
        d.line(pts, fill=col, width=width * S, joint='curve')
    if p >= 0.98:
        ang = math.atan2(dy, dx); hl = 46
        for s_ in (+1, -1):
            a2 = ang + math.pi + s_ * 0.5
            d.line([(x1 * S, y1 * S), ((x1 + hl * math.cos(a2)) * S, (y1 + hl * math.sin(a2)) * S)], fill=col, width=width * S)
        r = width * S / 2
        d.ellipse((x1 * S - r, y1 * S - r, x1 * S + r, y1 * S + r), fill=col)
    return L.resize((W, H), Image.LANCZOS)


_LB = {}


def label_layer(text, size, col=(232, 24, 24, 255), rot=-10):
    k = (text, size, rot)
    if k not in _LB:
        from PIL import ImageFont
        f = ImageFont.truetype(ROOT + 'fonts/Caveat-Bold.ttf', size)
        w = int(f.getlength(text)) + 40; h = int(size * 1.5)
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).text((20, 0), text, font=f, fill=col)
        _LB[k] = im.rotate(-rot * -1, resample=Image.BICUBIC, expand=True)
    return _LB[k]


SEO = None
if fx.get('seo'):
    SEO = tkfont.tt([fx['seo']], fx.get('seo_size', 26), EMO, maxw=1040, stroke=2)
    SEO.putalpha(SEO.getchannel('A').point(lambda v: int(v * fx.get('seo_alpha', 0.45))))

tot = fx['tot']; n = int(round(tot * FPS))
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'fps={FPS},crop=886:1920:97:0,scale={W}:{FULL_H}:flags=lanczos',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
FR = W * FULL_H * 3; last = None
CIRC = fx.get('circles', [])
for i in range(n):
    t = i / FPS
    raw = dec.stdout.read(FR)
    if len(raw) < FR: raw = last
    last = raw
    arr = np.frombuffer(raw, np.uint8).reshape(FULL_H, W, 3)[OFF:OFF + H].copy()
    # transición: desenfoque de movimiento vertical, máximo en el corte
    for b in fx.get('blurs', []):
        d = abs(t - b['t'])
        if d < b['half']:
            L = int(b['px'] * (1 - d / b['half']) ** 1.5)
            if L > 3:
                k = np.zeros((L, 1), np.float32); k[:] = 1.0 / L
                arr = cv2.filter2D(arr, -1, k, borderType=cv2.BORDER_REFLECT)
    fr = Image.fromarray(arr).convert('RGBA')
    if SEO: fr.alpha_composite(SEO, ((W - SEO.width) // 2, fx.get('seo_y', 14)))
    for j, c in enumerate(CIRC):
        if c['t0'] <= t < c['t1']:
            fr.alpha_composite(circle_layer(c['box'], (t - c['t0']) / c.get('draw', 0.35), 7 + j, c.get('w', 9)))
    for j, a in enumerate(fx.get('arrows', [])):
        if a['t0'] <= t < a['t1']:
            pr = (t - a['t0']) / a.get('draw', 0.25)
            fr.alpha_composite(arrow_solid(a['a'], a['b'], pr, a.get('w', 15)) if a.get('solid') else arrow_layer(a['a'], a['b'], pr, 31 + j, a.get('w', 10)))
    for lb in fx.get('labels', []):
        if lb['t0'] <= t < lb['t1']:
            im = label_layer(lb['text'], lb.get('size', 72), rot=lb.get('rot', -10))
            fr.alpha_composite(im, (int(lb['x']), int(lb['y'])))
    for tx in fx.get('texts', []):
        if not (tx['t0'] <= t < tx['t1']): continue
        lines = tx['lines']
        if tx.get('tw'):
            ntot = sum(len(tokens(l)) for l in lines)
            k = int(ntot * min(1.0, (t - tx['t0']) / tx['tw']))
            if k < ntot:
                lines = partial(lines, max(1, k)); lines[-1] += '_'
                lines = [l + '*' if l.count('*') % 2 else l for l in lines]
            # anclado arriba para que no salte al crecer
            im = block(lines, tx['size']); full = block(tx['lines'], tx['size'])
            fr.alpha_composite(im, (int(W / 2 - im.width / 2), int(tx['y'] - full.height / 2)))
            continue
        im = block(tx['lines'], tx['size'])
        # 'y' = centro vertical del bloque
        fr.alpha_composite(im, (int(W / 2 - im.width / 2), int(tx['y'] - im.height / 2)))
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait(); dec.kill()
print('ok', OUT)
