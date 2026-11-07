#!/usr/bin/env python3
"""Formato C: edición "loca" encima de un render de native7.
Uso: fxc.py base.mp4 fx.json out.mp4
fx.json: {"tot":12, "zooms":[[t0,t1],...], "texts":[{t0,t1,y,size,lines:[[txt,color]],rot,emo_l,emo_r}],
          "stickers":[{t0,t1,x,y,size,name}], "seo":"texto"}
Texto en 3D (relleno + extrusión + contorno), entrada con rebote; transiciones con zoom y desenfoque.
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SRC, FX, OUT = sys.argv[1:4]
fx = json.load(open(FX))
W, H, FPS = 1080, 1920, 30
FONT = ROOT + 'fonts/tmp_w700_latin.ttf'
COL = {'w': (255, 255, 255), 'y': (255, 214, 10), 'g': (60, 220, 90), 'r': (240, 40, 50)}
EMO = {}


def emo(name, size):
    k = (name, size)
    if k not in EMO:
        p = ROOT + f'engine/emo/n_{name}.png'
        if not os.path.exists(p):
            p = ROOT + f'engine/emo/{name}.png'
        EMO[k] = Image.open(p).convert('RGBA').resize((size, size), Image.LANCZOS)
    return EMO[k]


_TC = {}


def text3d(lines, size, emo_l=None, emo_r=None):
    key = (json.dumps(lines), size, emo_l, emo_r)
    if key in _TC:
        return _TC[key]
    f = ImageFont.truetype(FONT, size)
    depth = max(6, size // 11); st = max(5, size // 14)
    rows = []
    for txt, c in lines:
        w = int(f.getlength(txt)); h = int(size * 1.15)
        rows.append((txt, COL.get(c, COL['w']), w, h))
    ew = int(size * 1.15) if (emo_l or emo_r) else 0
    Wd = max(r[2] for r in rows) + 2 * ew + 2 * st + depth + 20
    Hd = sum(r[3] for r in rows) + 2 * st + depth + 20
    im = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = st + 10
    for txt, c, w, h in rows:
        x = (Wd - w - depth) // 2
        for k in range(depth, 0, -1):  # extrusión
            d.text((x + k, y + k), txt, font=f, fill=(25, 25, 25), stroke_width=st, stroke_fill=(10, 10, 10))
        d.text((x, y), txt, font=f, fill=c, stroke_width=st, stroke_fill=(10, 10, 10))
        y += h
    if emo_l:
        e = emo(emo_l, ew); im.alpha_composite(e, (0, max(0, (Hd - ew) // 2)))
    if emo_r:
        e = emo(emo_r, ew); im.alpha_composite(e, (Wd - ew, max(0, (Hd - ew) // 2)))
    _TC[key] = im
    return im


def pop(dt):
    if dt < 0: return 0
    if dt < 0.12: return 0.5 + 0.7 * dt / 0.12
    if dt < 0.24: return 1.2 - 0.2 * (dt - 0.12) / 0.12
    return 1.0


def zoom_blur(img, k):
    """k: 0..1 intensidad. Mezcla de varios zooms para efecto de desenfoque radial."""
    if k <= 0.01: return img
    acc = None; n = 5
    for i in range(n):
        z = 1 + k * (0.10 + 0.05 * i)
        w2, h2 = int(W * z), int(H * z)
        sc = img.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
        a = np.asarray(sc, dtype=np.float32)
        acc = a if acc is None else acc + a
    return Image.fromarray((acc / n).astype(np.uint8))


def seo_img(txt):
    f = ImageFont.truetype(ROOT + 'fonts/tmp_w600_latin.ttf', 34)
    w = int(f.getlength(txt)) + 20
    im = Image.new('RGBA', (w, 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 6), txt, font=f, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    return im


SEO = seo_img(fx['seo']) if fx.get('seo') else None
tot = fx['tot']; n = int(tot * FPS)
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
last = None
for i in range(n):
    t = i / FPS
    raw = dec.stdout.read(W * H * 3)
    if len(raw) < W * H * 3:
        raw = last
    last = raw
    fr = Image.frombytes('RGB', (W, H), raw)
    for z0, z1 in fx.get('zooms', []):
        if z0 <= t <= z1:
            p = (t - z0) / (z1 - z0); fr = zoom_blur(fr, math.sin(math.pi * p))
    fr = fr.convert('RGBA')
    if SEO: fr.alpha_composite(SEO, ((W - SEO.width) // 2, 285))
    for s in fx.get('stickers', []):
        if s['t0'] <= t < s['t1']:
            k = pop(t - s['t0']); sz = int(s['size'] * k)
            if sz < 4: continue
            e = emo(s['name'], sz).rotate(8 * math.sin((t - s['t0']) * 5 + s['x']), resample=Image.BICUBIC, expand=True)
            fr.alpha_composite(e, (int(s['x'] - e.width / 2), int(s['y'] - e.height / 2 + 6 * math.sin(t * 6 + s['x']))))
    for tx in fx.get('texts', []):
        if tx['t0'] <= t < tx['t1']:
            im = text3d(tx['lines'], tx['size'], tx.get('emo_l'), tx.get('emo_r'))
            k = pop(t - tx['t0']) if not tx.get('nopop') else 1.0
            rot = tx.get('rot', 0) + 2.0 * math.sin((t - tx['t0']) * 3.2)
            if k <= 0: continue
            im2 = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC).rotate(rot, resample=Image.BICUBIC, expand=True)
            if im2.width > 1040:
                r = 1040 / im2.width; im2 = im2.resize((1040, int(im2.height * r)), Image.BICUBIC)
            fr.alpha_composite(im2, (int(W / 2 - im2.width / 2), int(tx['y'] - im2.height / 2)))
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait(); dec.kill()
print('ok', OUT)
