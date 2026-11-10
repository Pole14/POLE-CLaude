#!/usr/bin/env python3
"""Formato "hero" (10 nov 2026): render directo desde la grabación a resolución nativa, con cámara.
Uso: hero.py rec.mp4 spec.json out.mp4   (sin audio; luego mux3.py)
spec: {tot, rmap:[[t,rec_t]], cam:[{t,z,p:[x,y],s:[x,y]}], punches:[t], shakes:[{t,amp}], flashes:[t],
       blurs:[{t,half,px}], spots:[{t0,t1,box,dim,fade}], rects:[{t0,t1,box,draw,w}], taps:[{t,x,y}],
       lines:[{t1,y,font,rows:[{at,text,size}]}], texts:[{t0,t1,y,size,text,font,tw}],
       counters:[{t0,t1,y,size,font,frm,to,dur}], bursts:[{t,x,y,emo,n,seed}], seo, seo_y}
Coordenadas "layout" = las de inspo (1080x1920, grabación a 1080 de ancho, recorte vertical OFF=150).
Cámara: el punto p (layout) cae en el punto s (pantalla) con zoom z. Marcas y focos siguen a la cámara; los textos no.
"""
import glob, json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, ROOT + 'engine')
import tkfont

REC, SPEC, OUT = sys.argv[1:4]
sp = json.load(open(SPEC))
W, H, FPS, OFF = 1080, 1920, 60, int(sp.get('off', 150))

EMO = {}
for f in glob.glob(ROOT + 'engine/emo/n_*.png'):
    EMO[os.path.basename(f)[2:-4]] = Image.open(f).convert('RGBA')
EMO['check'] = Image.open(ROOT + 'engine/emo/check.png').convert('RGBA')
HAND = Image.open(ROOT + 'engine/emo/tap_hand.png').convert('RGBA')

# ---- grabación en memoria (JPEG) ----
cap = cv2.VideoCapture(REC); RFPS = cap.get(cv2.CAP_PROP_FPS)
RW, RH = int(cap.get(3)), int(cap.get(4)); K = W / RW
FRAMES = []
while True:
    ok, fr = cap.read()
    if not ok: break
    FRAMES.append(cv2.imencode('.jpg', fr, [cv2.IMWRITE_JPEG_QUALITY, 97])[1])
_last = [-1, None]


def rec_frame(t):
    i = max(0, min(len(FRAMES) - 1, int(round(t * RFPS))))
    if _last[0] != i: _last[0] = i; _last[1] = cv2.cvtColor(cv2.imdecode(FRAMES[i], cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    return _last[1]


RX = [a for a, _ in sp['rmap']]; RY = [b for _, b in sp['rmap']]


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def smooth(u):
    u = max(0.0, min(1.0, u)); return u * u * u * (u * (6 * u - 15) + 10)


CAM = sp['cam']


def camera(t):
    if t <= CAM[0]['t']: a = b = CAM[0]; u = 0
    elif t >= CAM[-1]['t']: a = b = CAM[-1]; u = 0
    else:
        for i in range(len(CAM) - 1):
            if CAM[i]['t'] <= t < CAM[i + 1]['t']:
                a, b = CAM[i], CAM[i + 1]; u = smooth((t - a['t']) / (b['t'] - a['t'])); break
    g = lambda k, d: np.array(a.get(k, d), float) * (1 - u) + np.array(b.get(k, d), float) * u
    z = float(g('z', 1.0)); p = g('p', [540, 960]); s = g('s', [540, 960])
    for hp in sp.get('punches', []):
        x = t - hp
        if 0 <= x < 0.32: z *= 1 + 0.06 * (1 - x / 0.32) ** 2
    tx, ty = s[0] - z * p[0], s[1] - z * p[1]
    tx = min(0.0, max(W - z * W, tx)); ty = min(0.0, max(H - z * (RH * K - OFF), ty))
    for sh in sp.get('shakes', []):
        x = t - sh['t']
        if 0 <= x < 0.35:
            d = sh.get('amp', 10) * (1 - x / 0.35) ** 2
            tx += d * math.sin(x * 70); ty += d * math.cos(x * 53)
    return z, tx, ty


_C = {}


def deco(im):
    """Sombra suave + brillo en lo resaltado (amarillo)."""
    P = 44
    out = Image.new('RGBA', (im.width + 2 * P, im.height + 2 * P), (0, 0, 0, 0))
    a = np.array(im); al = a[..., 3]
    sh = Image.new('L', out.size, 0); sh.paste(Image.fromarray(al), (P, P + 6))
    sh = sh.filter(ImageFilter.GaussianBlur(13)).point(lambda v: int(min(255, v * 0.62)))
    out.paste(Image.new('RGBA', out.size, (0, 0, 0, 255)), (0, 0), sh)
    m = ((a[..., 0] > 200) & (a[..., 1] > 150) & (a[..., 2] < 110) & (al > 128)).astype(np.uint8) * 255
    if m.any():
        g = Image.new('L', out.size, 0); g.paste(Image.fromarray(m), (P, P))
        g = g.filter(ImageFilter.GaussianBlur(17)).point(lambda v: int(min(255, v * 0.85)))
        out.paste(Image.new('RGBA', out.size, (255, 200, 0, 255)), (0, 0), g)
    out.alpha_composite(im, (P, P))
    return out


_F = {}


def hline(text, size, font):
    """Una línea estilo TikTok (blanco, contorno negro) con un poco de aire entre letras; *resaltado* y |emo:x|."""
    from PIL import ImageFont
    fk = (font, size)
    if fk not in _F: _F[fk] = ImageFont.truetype(ROOT + 'fonts/' + (font or 'TikTokSans36pt-Bold.ttf'), size)
    f = _F[fk]; tr = size * sp.get('track', 0.03); st = int(max(3, min(7, round(size * 0.042))))
    items = []; x = 0.0; hl = False
    for tk in tokens(text):
        if tk == '*': hl = not hl; continue
        if tk.startswith('|emo:'):
            items.append(('e', tk[5:-1], x + size * 0.06)); x += size * 1.12; continue
        items.append(('t', tk, x, hl)); x += f.getlength(tk) + (tr if tk != ' ' else 0)
    asc, desc = f.getmetrics(); w = int(x + 2 * st + 24); h = int(asc + desc * 0.35 + 2 * st + 32 + size * 0.02)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for it in items:  # contorno primero, relleno después: las letras no se pisan
        if it[0] == 't': d.text((12 + st + it[2], 16 + st), it[1], font=f, fill=(0, 0, 0, 255), stroke_width=st, stroke_fill=(0, 0, 0, 255))
    for it in items:
        if it[0] == 't': d.text((12 + st + it[2], 16 + st), it[1], font=f, fill=tkfont.HL if it[3] else (255, 255, 255, 255))
        else: im.alpha_composite(EMO[it[1]].resize((size, size), Image.LANCZOS), (int(12 + st + it[2]), int(16 + st + asc - size * 0.86)))
    return im


def line_img(text, size, font):
    k = (text, size, font)
    if k not in _C:
        mw = sp.get('maxw', 930); s_ = size
        if font == 'classic':
            im = tkfont.classic([text if text.strip() else ' '], s_, EMO, maxw=mw)
            pad = Image.new('RGBA', (im.width + 16, im.height + 24), (0, 0, 0, 0)); pad.alpha_composite(im, (8, 12)); im = pad
        else:
            im = hline(text if text.strip() else ' ', s_, font)
            while im.width > mw + 40 and s_ > 30: s_ -= 4; im = hline(text, s_, font)
        _C[k] = deco(im)
    return _C[k]


def pop_img(im, u):
    if u >= 1: return im
    sc = 0.7 + 0.3 * ease(u) + 0.08 * math.sin(math.pi * u)
    r = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    if u < 0.5: r.putalpha(r.getchannel('A').point(lambda v: int(v * min(1.0, u * 2.4))))
    return r


def rect_layer(d, box, prog, width, S, col=(232, 20, 32, 255)):
    x0, y0, x1, y1 = box; p = ease(prog)
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    tot = 4 * p; path = [pts[0]]
    for k in range(4):
        f = min(1.0, max(0.0, tot - k))
        if f <= 0: break
        a, b = pts[k], pts[k + 1]; path.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    if len(path) > 1:
        d.line([(x * S, y * S) for x, y in path], fill=col, width=int(width * S), joint='curve')
        r = width * S / 2
        for x, y in path: d.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=col)


def circle_pts(box, prog, seed):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2 * 1.06, (y1 - y0) / 2 * 1.12
    rng = np.random.RandomState(seed); ph1, ph2 = rng.uniform(0, 6.28, 2)
    a0 = math.radians(-115 + rng.uniform(-15, 15)); sweep = math.radians(385) * ease(prog); n = max(2, int(140 * ease(prog)))
    pts = []
    for i in range(n + 1):
        a = a0 + sweep * i / n
        k = 1 + 0.035 * math.sin(2 * a + ph1) + 0.015 * math.sin(5 * a + ph2) + 0.05 * (i / 140)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


_SPOT = {}


def spot_alpha(box, z, tx, ty):
    """Máscara (pantalla) 1 fuera de la caja, 0 dentro, bordes suaves."""
    x0, y0, x1, y1 = [v * z + o for v, o in zip(box, (tx, ty, tx, ty))]
    m = Image.new('L', (W // 4, H // 4), 255)
    ImageDraw.Draw(m).rounded_rectangle((x0 / 4, y0 / 4, x1 / 4, y1 / 4), radius=7 * z, fill=0)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BILINEAR), np.float32) / 255


SEO = None
if sp.get('seo'):
    SEO = tkfont.tt([sp['seo']], sp.get('seo_size', 26), EMO, maxw=1040, stroke=2)
    SEO.putalpha(SEO.getchannel('A').point(lambda v: int(v * sp.get('seo_alpha', 0.5))))

TOKRE = __import__('re').compile(r'\|emo:\w+\||\*')


def tokens(line):
    out = []; i = 0
    for m in TOKRE.finditer(line):
        out += list(line[i:m.start()]); out.append(m.group(0)); i = m.end()
    return out + list(line[i:])


tot = sp['tot']; n = int(round(tot * FPS))
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
ONLY = [float(x) for x in os.environ.get('ONLY', '').split(',') if x]
for i in range(n):
    t = i / FPS
    if ONLY and not any(abs(t - o) < 0.5 / FPS for o in ONLY): continue
    src = rec_frame(float(np.interp(t, RX, RY)))
    z, tx, ty = camera(t)
    M = np.float32([[z * K, 0, tx], [0, z * K, ty - z * OFF]])
    arr = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_CUBIC if z * K >= 1 else cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
    # focos
    for s_ in sp.get('spots', []):
        if s_['t0'] <= t < s_['t1']:
            fd = s_.get('fade', 0.3); k = min(1.0, (t - s_['t0']) / fd, (s_['t1'] - t) / fd)
            a = spot_alpha(s_['box'], z, tx, ty) * (s_.get('dim', 0.5) * smooth(k))
            arr = (arr.astype(np.float32) * (1 - a[..., None])).astype(np.uint8)
    for b in sp.get('blurs', []):
        d = abs(t - b['t'])
        if d < b['half']:
            L = int(b['px'] * (1 - d / b['half']) ** 1.5)
            if L > 3:
                kk = np.zeros((L, 1), np.float32); kk[:] = 1.0 / L
                arr = cv2.filter2D(arr, -1, kk, borderType=cv2.BORDER_REFLECT)
    fr = Image.fromarray(arr).convert('RGBA')
    # marcas que siguen a la cámara (dibujadas ya en pantalla)
    S = 2; Lr = None
    P = lambda x, y: (x * z + tx, y * z + ty)
    for r in sp.get('rects', []):
        if r['t0'] <= t < r['t1']:
            if Lr is None: Lr = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); dr = ImageDraw.Draw(Lr)
            x0, y0 = P(r['box'][0], r['box'][1]); x1, y1 = P(r['box'][2], r['box'][3])
            fo = min(1.0, (r['t1'] - t) / 0.15)
            rect_layer(dr, (x0, y0, x1, y1), (t - r['t0']) / r.get('draw', 0.3), r.get('w', 10) * (0.6 + 0.4 * z), S, (232, 20, 32, int(255 * fo)))
    for j, c in enumerate(sp.get('circles', [])):
        if c['t0'] <= t < c['t1']:
            if Lr is None: Lr = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); dr = ImageDraw.Draw(Lr)
            x0, y0 = P(c['box'][0], c['box'][1]); x1, y1 = P(c['box'][2], c['box'][3])
            pts = [(x * S, y * S) for x, y in circle_pts((x0, y0, x1, y1), (t - c['t0']) / c.get('draw', 0.35), 11 + j)]
            wd = int(c.get('w', 8) * (0.6 + 0.4 * z) * S); col = (226, 32, 38, int(255 * min(1.0, (c['t1'] - t) / 0.15)))
            dr.line(pts, fill=col, width=wd, joint='curve')
            for q in (pts[0], pts[-1]): dr.ellipse((q[0] - wd / 2, q[1] - wd / 2, q[0] + wd / 2, q[1] + wd / 2), fill=col)
    if Lr is not None: fr.alpha_composite(Lr.resize((W, H), Image.LANCZOS))
    for tp in sp.get('taps', []):
        x = t - tp['t']; px, py = P(tp['x'], tp['y'])
        if 0 <= x < 0.45:
            u = x / 0.45; r = (18 + 56 * ease(u)) * z; a = int(210 * (1 - u))
            L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 255, 255, a // 2), outline=(90, 90, 90, a), width=4)
            fr.alpha_composite(L)
        if -0.4 <= x < 0.7:
            sc = 0.9 if 0 <= x < 0.12 else 1.0
            al = min(1.0, (x + 0.4) / 0.15, (0.7 - x) / 0.15)
            hs = int(165 * sc * (0.7 + 0.3 * z)); hi = HAND.resize((hs, hs), Image.LANCZOS)
            hi.putalpha(hi.getchannel('A').point(lambda q: int(q * max(0.0, al))))
            dx = int(60 * (1 - ease(min(1.0, (x + 0.4) / 0.34))))
            fr.alpha_composite(hi, (int(px - hs * 0.33 + dx), int(py - hs * 0.12 + dx)))
    # destello
    for fl in sp.get('flashes', []):
        x = t - fl
        if 0 <= x < 0.2:
            a = int(235 * (1 - x / 0.2) ** 2)
            fr.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, a)))
    if SEO: fr.alpha_composite(SEO, ((W - SEO.width) // 2, sp.get('seo_y', 190)))
    # emojis que saltan
    for bu in sp.get('bursts', []):
        x = t - bu['t']
        if 0 <= x < 1.25:
            rng = np.random.RandomState(bu.get('seed', 3))
            for j in range(bu.get('n', 10)):
                ang = rng.uniform(-math.pi * 0.95, -math.pi * 0.05); v = rng.uniform(650, 1250); sz = int(rng.uniform(74, 118)); rot = rng.uniform(-200, 200)
                ex = bu['x'] + math.cos(ang) * v * x; ey = bu['y'] + math.sin(ang) * v * x + 1500 * x * x
                al = min(1.0, x / 0.06, (1.25 - x) / 0.35)
                e = EMO[bu.get('emo', 'moneyfly')].resize((sz, sz), Image.LANCZOS).rotate(rot * x, resample=Image.BICUBIC, expand=True)
                e.putalpha(e.getchannel('A').point(lambda q: int(q * max(0.0, al))))
                if -sz < ex < W and -sz < ey < H: fr.alpha_composite(e, (int(max(0, ex - e.width / 2)), int(max(0, ey - e.height / 2))))
    # textos por líneas (cada línea entra cuando la dice la voz)
    for g in sp.get('lines', []):
        if not (g['rows'][0]['at'] <= t < g['t1']): continue
        y = g['y']; fo = min(1.0, (g['t1'] - t) / 0.12)
        for r in g['rows']:
            im = line_img(r['text'], r['size'], g.get('font'))
            h_eff = im.height - 88 - 32 + int(r['size'] * g.get('gap', 0.06))
            if t >= r['at']:
                pi = pop_img(im, (t - r['at']) / 0.2)
                if fo < 1: pi = pi.copy(); pi.putalpha(pi.getchannel('A').point(lambda v: int(v * fo)))
                fr.alpha_composite(pi, (int(W / 2 - pi.width / 2), int(y + im.height / 2 - pi.height / 2 - 44)))
            y += h_eff
    for tx_ in sp.get('texts', []):
        if not (tx_['t0'] <= t < tx_['t1']): continue
        text = tx_['text']
        if tx_.get('tw'):
            tk = tokens(text); k = int(len(tk) * min(1.0, (t - tx_['t0']) / tx_['tw']))
            if k < len(tk):
                text = ''.join(tk[:max(1, k)]) + '_'
                if text.count('*') % 2: text += '*'
            im = line_img(text, tx_['size'], tx_.get('font')); full = line_img(tx_['text'], tx_['size'], tx_.get('font'))
            fr.alpha_composite(im, (int(W / 2 - full.width / 2), int(tx_['y'] - 44)))
        else:
            im = line_img(text, tx_['size'], tx_.get('font')); pi = pop_img(im, (t - tx_['t0']) / 0.2)
            fr.alpha_composite(pi, (int(W / 2 - pi.width / 2), int(tx_['y'] + im.height / 2 - pi.height / 2 - 44)))
    for c in sp.get('counters', []):
        if not (c['t0'] <= t < c['t1']): continue
        u = ease((t - c['t0']) / c.get('dur', 0.5)); v = c['frm'] + (c['to'] - c['frm']) * u
        im = line_img('*' + f'{v:.2f}'.replace('.', ',') + '*' + (c.get('suffix', '') if u >= 1 else ''), c['size'], c.get('font'))
        sc = 1 + 0.12 * math.sin(math.pi * min(1.0, (t - c['t0']) / (c.get('dur', 0.5) + 0.25)))
        if abs(sc - 1) > 0.004: im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        fr.alpha_composite(im, (int(W / 2 - im.width / 2), int(c['y'] - im.height / 2)))
    if ONLY: fr.convert('RGB').save(OUT.replace('.mp4', f'_{t:.2f}.jpg'), quality=90); continue
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait()
print('ok', OUT)
