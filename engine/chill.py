#!/usr/bin/env python3
"""Formato "chill" (receta de los virales, 8 nov 2026).
Uso: chill.py base.mp4 fx.json out.mp4
- base.mp4: render de native7 (grabación + círculos/recuadros), sin textos.
- Pantalla completa SIN franjas: recorta las franjas negras, amplía a 1080 de ancho y deja la ventana vertical FIJA (fx.off, 0..420).
- Sin zoom, sin paneo, sin pop: los textos entran de golpe. 'tw' = máquina de escribir (segundos) con cursor "_".
fx.json: {"tot", "fps", "off", "style":"box"|"ol",
          "texts":[{t0,t1,y,size,lines,style?,tw?}], "checks":{t0,y,size}, "seo":"...", "seo_y"}
"""
import glob, json, os, re, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, ROOT + 'engine')
from tktext import render_block, outline_block

SRC, FX, OUT = sys.argv[1:4]
fx = json.load(open(FX))
W, H = 1080, 1920
FPS = fx.get('fps', 60)
FULL_H = 2340
OFF = int(fx.get('off', 150))
STYLE = fx.get('style', 'box')

EMO = {}
for f in glob.glob(ROOT + 'engine/emo/n_*.png'):
    EMO[os.path.basename(f)[2:-4]] = Image.open(f).convert('RGBA')
EMO['check'] = Image.open(ROOT + 'engine/emo/check.png').convert('RGBA')
for n, f in {'money': 'b42', 'scream': 'b41', 'shush': 'b40', 'party': 'b51', 'wink': 'b35', 'grin': 'b04'}.items():
    EMO[n] = Image.open(ROOT + f'engine/emo/{f}.png').convert('RGBA')

TOK = re.compile(r'\|emo:\w+\|')


def tokens(line):
    out = []; i = 0
    for m in TOK.finditer(line):
        out += list(line[i:m.start()]); out.append(m.group(0)); i = m.end()
    return out + list(line[i:])


def partial(lines, n):
    res = []
    for ln in lines:
        tk = tokens(ln)
        if n <= 0: break
        res.append(''.join(tk[:n])); n -= len(tk)
    return res


_C = {}


def block(lines, size, style):
    key = (json.dumps(lines), size, style)
    if key not in _C:
        lines = [l if l.strip() else ' ' for l in lines]
        _C[key] = render_block(lines, size, 'box', EMO, 600) if style == 'box' else outline_block(lines, size, EMO)
    return _C[key]


SEO = outline_block([fx['seo']], 34, EMO) if fx.get('seo') else None
tot = fx['tot']; n = int(round(tot * FPS))
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'fps={FPS},crop=886:1920:97:0,scale={W}:{FULL_H}:flags=lanczos',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
FR = W * FULL_H * 3; last = None
CK = fx.get('checks')
for i in range(n):
    t = i / FPS
    raw = dec.stdout.read(FR)
    if len(raw) < FR: raw = last
    last = raw
    fr = Image.frombytes('RGB', (W, FULL_H), raw).crop((0, OFF, W, OFF + H)).convert('RGBA')
    if SEO: fr.alpha_composite(SEO, ((W - SEO.width) // 2, fx.get('seo_y', 250)))
    if CK and t >= CK['t0']:
        sz = CK.get('size', 120); e = EMO['check'].resize((sz, sz), Image.LANCZOS)
        for j in range(3):
            if t >= CK['t0'] + 0.12 * j:
                fr.alpha_composite(e, (int(W / 2 + (j - 1) * sz * 1.05 - sz / 2), int(CK['y'] - sz / 2)))
    for tx in fx.get('texts', []):
        if not (tx['t0'] <= t < tx['t1']): continue
        st = tx.get('style', STYLE); lines = tx['lines']
        if tx.get('tw'):
            ntot = sum(len(tokens(l)) for l in lines)
            k = int(ntot * min(1.0, (t - tx['t0']) / tx['tw']))
            if k < ntot:
                lines = partial(lines, max(1, k)); lines[-1] += '_'
        im = block(lines, tx['size'], st)
        if im.width > 980:
            r = 980 / im.width; im = im.resize((980, int(im.height * r)), Image.LANCZOS)
        # anclado arriba (para que la máquina de escribir crezca hacia abajo sin saltar)
        fr.alpha_composite(im, (int(W / 2 - im.width / 2), int(tx['y'])))
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait(); dec.kill()
print('ok', OUT)
