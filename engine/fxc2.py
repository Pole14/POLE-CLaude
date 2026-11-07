#!/usr/bin/env python3
"""Formato C v2: edición movida con textos nativos de TikTok y vídeo a pantalla completa (sin franjas negras).
Uso: fxc2.py base.mp4 fx.json out.mp4
- base.mp4: render de native7 (grabación + recuadros/círculos), sin textos.
- Recorta las franjas negras y amplía la grabación a 1080 de ancho; "cam" mueve la ventana vertical (0..420).
fx.json: {"tot", "fps", "cam":[[t,off],...], "zooms":[[t0,t1],...],
          "texts":[{t0,t1,y,size,lines,style:'box'|'ol',nopop}], "stickers":[{t0,t1,x,y,size,name}], "seo":"..."}
"""
import glob, json, math, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, ROOT + 'engine')
from tktext import render_block, outline_block

SRC, FX, OUT = sys.argv[1:4]
fx = json.load(open(FX))
W, H = 1080, 1920
FPS = fx.get('fps', 60)
FULL_H = 2340  # 1920 * 1080/886

EMO = {}
for f in glob.glob(ROOT + 'engine/emo/n_*.png'):
    EMO[os.path.basename(f)[2:-4]] = Image.open(f).convert('RGBA')
EMO['check'] = Image.open(ROOT + 'engine/emo/check.png').convert('RGBA')
for n, f in {'money': 'b42', 'scream': 'b41', 'shush': 'b40', 'party': 'b51', 'wink': 'b35', 'grin': 'b04'}.items():
    EMO[n] = Image.open(ROOT + f'engine/emo/{f}.png').convert('RGBA')


def ease(u):
    u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


def cam(t):
    k = fx.get('cam', [[0, 0]])
    if t <= k[0][0]: return k[0][1]
    for a, b in zip(k, k[1:]):
        if a[0] <= t <= b[0]:
            return a[1] + (b[1] - a[1]) * ease((t - a[0]) / max(1e-6, b[0] - a[0]))
    return k[-1][1]


def popk(dt, d=0.22):
    if dt < 0: return 0.0
    u = min(1.0, dt / d)
    return 0.86 + 0.14 * u + 0.07 * math.sin(u * math.pi)


def zoom_blur(img, k):
    if k <= 0.02: return img
    acc = None; n = 4
    for i in range(n):
        z = 1 + k * (0.035 + 0.025 * i)
        w2, h2 = int(W * z), int(H * z)
        sc = img.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
        a = np.asarray(sc, dtype=np.float32); acc = a if acc is None else acc + a
    return Image.fromarray((acc / n).astype(np.uint8))


_C = {}


def block(tx):
    key = (json.dumps(tx['lines']), tx['size'], tx.get('style', 'box'))
    if key not in _C:
        _C[key] = render_block(tx['lines'], tx['size'], 'box', EMO, 600) if tx.get('style', 'box') == 'box' else outline_block(tx['lines'], tx['size'], EMO)
    return _C[key]


def emo(name, size):
    return EMO[name].resize((size, size), Image.LANCZOS)


SEO = outline_block([fx['seo']], 36, EMO) if fx.get('seo') else None
tot = fx['tot']; n = int(round(tot * FPS))
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'fps={FPS},crop=886:1920:97:0,scale={W}:{FULL_H}:flags=lanczos',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
FR = W * FULL_H * 3; last = None
for i in range(n):
    t = i / FPS
    raw = dec.stdout.read(FR)
    if len(raw) < FR: raw = last
    last = raw
    big = Image.frombytes('RGB', (W, FULL_H), raw)
    off = int(round(cam(t)))
    fr = big.crop((0, off, W, off + H))
    for z0, z1 in fx.get('zooms', []):
        if z0 <= t <= z1:
            fr = zoom_blur(fr, math.sin(math.pi * (t - z0) / (z1 - z0)))
    fr = fr.convert('RGBA')
    if SEO: fr.alpha_composite(SEO, ((W - SEO.width) // 2, fx.get('seo_y', 300)))
    for s in fx.get('stickers', []):
        if s['t0'] <= t < s['t1']:
            k = popk(t - s['t0'], 0.18); sz = int(s['size'] * k)
            e = emo(s['name'], sz).rotate(6 * math.sin((t - s['t0']) * 4 + s['x'] / 50), resample=Image.BICUBIC, expand=True)
            fr.alpha_composite(e, (int(s['x'] - e.width / 2), int(s['y'] - e.height / 2 + 5 * math.sin(t * 5 + s['x'] / 40))))
    for tx in fx.get('texts', []):
        if tx['t0'] <= t < tx['t1']:
            im = block(tx); k = 1.0 if tx.get('nopop') else popk(t - tx['t0'])
            if k != 1.0: im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
            if im.width > 960:
                r = 960 / im.width; im = im.resize((960, int(im.height * r)), Image.BICUBIC)
            fr.alpha_composite(im, (int(W / 2 - im.width / 2), int(tx['y'] - im.height / 2)))
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait(); dec.kill()
print('ok', OUT)
