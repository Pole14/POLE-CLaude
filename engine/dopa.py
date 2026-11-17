#!/usr/bin/env python3
"""dopa.py spec.json out.mp4 — explicativo rápido "con dopamina" (16 nov 2026). Sin audio (se mezcla aparte, solo voz).
Fondo oscuro con brillo y partículas, chip de paso + barra de progreso en 4 tramos, subtítulos en fichas palabra a palabra (la activa salta y cambia de color),
precio que se tacha, móvil con la grabación dentro y zoom que sigue la acción, letras del código que saltan una a una, contador del total,
sello del descuento con sacudida, emojis que saltan y cierre corto. Todo sale de los tiempos de la voz."""
import glob, json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SP = json.load(open(sys.argv[1])); OUT = sys.argv[2]
W, H, FPS = 1080, 1920, 30
TH = {'bg0': [10, 16, 52], 'bg1': [34, 58, 150], 'acc': [255, 214, 10], 'acc2': [255, 122, 26], 'ok': [34, 197, 94], 'ink': [14, 16, 34], 'card': [255, 255, 255]}
TH.update(SP.get('theme', {})); TH = {k: tuple(v) for k, v in TH.items()}
_F = {}
def font(sz, name='Montserrat-900.ttf'):
    k = (sz, name)
    if k not in _F: _F[k] = ImageFont.truetype(ROOT + 'fonts/' + name, sz)
    return _F[k]
HEAD = 'Anton-Regular.ttf'
EMO = {os.path.basename(f)[2:-4]: Image.open(f).convert('RGBA') for f in glob.glob(ROOT + 'engine/emo/n_*.png')}
EMO['check'] = Image.open(ROOT + 'engine/emo/check.png').convert('RGBA')
def ease(u): u = max(0., min(1., u)); return 1 - (1 - u) ** 3
def back(u, c=2.2):
    u = max(0., min(1., u)); return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
def smooth(u): u = max(0., min(1., u)); return u * u * (3 - 2 * u)
def interp(rm, t):
    if t <= rm[0][0]: return rm[0][1]
    for a, b in zip(rm, rm[1:]):
        if a[0] <= t <= b[0]: return a[1] + (b[1] - a[1]) * ((t - a[0]) / max(1e-6, b[0] - a[0]))
    return rm[-1][1]
def put(fr, im, cx, cy, k=1.0, alpha=1.0, rot=0):
    if k <= 0.02 or alpha <= 0.02: return
    if abs(k - 1) > 0.005: im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    if x >= W or y >= H or x + im.width <= 0 or y + im.height <= 0: return
    fr.alpha_composite(im.crop((max(0, -x), max(0, -y), min(im.width, W - x), min(im.height, H - y))), (max(0, x), max(0, y)))
_C = {}
def card(text, sz, fg, bg, name='Montserrat-900.ttf', padx=None, pady=None, r=None, sh=10, emo=None):
    k = (text, sz, fg, bg, name, emo)
    if k in _C: return _C[k]
    f = font(sz, name); padx = int(sz * 0.3) if padx is None else padx; pady = int(sz * 0.16) if pady is None else pady
    tw = f.getlength(text); asc, desc = f.getmetrics(); ew = int(sz * 1.15) if emo else 0
    w, h = int(tw + ew + 2 * padx), int(asc + desc * 0.6 + 2 * pady)
    im = Image.new('RGBA', (w + sh, h + sh), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = int(h * 0.22) if r is None else r
    d.rounded_rectangle((sh, sh, w + sh - 1, h + sh - 1), r, fill=(0, 0, 0, 150)); d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=bg + (255,))
    d.text((padx, pady - sz * 0.06), text, font=f, fill=fg + (255,))
    if emo: im.alpha_composite(EMO[emo].resize((sz, sz), Image.LANCZOS), (int(padx + tw + sz * 0.12), int(pady + asc * 0.08)))
    _C[k] = im; return im
# ---- fondo ----
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
g = np.clip(1 - np.hypot((xx - W * 0.5) / (W * 0.95), (yy - H * 0.36) / (H * 0.62)), 0, 1)[..., None] ** 1.3
BGA = (np.array(TH['bg0'], np.float32) * (1 - g) + np.array(TH['bg1'], np.float32) * g).astype(np.uint8)
BGI = Image.fromarray(BGA).convert('RGBA')
rng = np.random.RandomState(SP.get('seed', 7)); PART = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(20, 70), rng.uniform(4, 12), rng.choice(['%', '€', '+', '•'])) for _ in range(26)]
# ---- grabación ----
cap = cv2.VideoCapture(SP['rec']); RF = cap.get(cv2.CAP_PROP_FPS); FR = []
while True:
    ok, f_ = cap.read()
    if not ok: break
    FR.append(cv2.imencode('.jpg', f_, [cv2.IMWRITE_JPEG_QUALITY, 95])[1])
RW, RH = int(cap.get(3)), int(cap.get(4)); PW, PH = 680, 860; _l = [-1, None]
def recf(rt):
    i = max(0, min(len(FR) - 1, int(round(rt * RF))))
    if _l[0] != i: _l[0] = i; _l[1] = cv2.cvtColor(cv2.imdecode(FR[i], cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    return _l[1]
PMASK = Image.new('L', (PW, PH), 0); ImageDraw.Draw(PMASK).rounded_rectangle((0, 0, PW - 1, PH - 1), 54, fill=255)
BEZ = Image.new('RGBA', (PW + 60, PH + 60), (0, 0, 0, 0)); _d = ImageDraw.Draw(BEZ)
_d.rounded_rectangle((26, 30, PW + 58, PH + 58), 70, fill=(0, 0, 0, 120)); BEZ = BEZ.filter(ImageFilter.GaussianBlur(10)); _d = ImageDraw.Draw(BEZ)
_d.rounded_rectangle((8, 8, PW + 36, PH + 36), 68, fill=(12, 12, 20, 255)); _d.rounded_rectangle((PW // 2 - 62, 20, PW // 2 + 106, 44), 12, fill=(12, 12, 20, 255))
def crop_at(t):
    ks = SP['phone']['keys']
    if t <= ks[0][0]: return ks[0][1:4]
    for a, b in zip(ks, ks[1:]):
        if a[0] <= t <= b[0]:
            u = smooth((t - a[0]) / max(1e-6, b[0] - a[0])); return [a[q] + (b[q] - a[q]) * u for q in (1, 2, 3)]
    return ks[-1][1:4]
def phone(t):
    cy, hc, cx = crop_at(t); wc = hc * PW / PH; x0 = max(0, min(RW - wc, cx - wc / 2)); y0 = max(0, min(RH - hc, cy - hc / 2))
    a = recf(interp(SP['rmap'], t)); M = np.float32([[PW / wc, 0, -x0 * PW / wc], [0, PH / hc, -y0 * PH / hc]])
    im = Image.fromarray(cv2.warpAffine(a, M, (PW, PH), flags=cv2.INTER_AREA if wc > PW else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)).convert('RGBA')
    out = BEZ.copy(); out.paste(im, (22, 22), PMASK)
    return out, (x0, y0, PW / wc, PH / hc)
# ---- subtítulos en fichas ----
def captions(fr, t, big):
    for ch in SP['captions']:
        if ch['t0'] <= t < ch['t1']:
            sz = 112 if big else 78; gap = 16; ims = []
            for w in ch['words']:
                act = w[1] - 0.04 <= t < w[2] + 0.1
                ims.append((card(w[0], sz, TH['ink'], TH['acc'] if act else TH['card'], HEAD if big else 'Montserrat-900.ttf'), act, w))
            lines, cur, ws = [], [], 0
            for it in ims:
                if cur and ws + it[0].width + gap > 1000: lines.append(cur); cur, ws = [], 0
                cur.append(it); ws += it[0].width + gap
            lines.append(cur); y = (470 if big else 1330) - (len(lines) - 1) * (sz * 0.75)
            ain = ease((t - ch['t0']) / 0.12)
            for ln in lines:
                tot = sum(i[0].width for i in ln) + gap * (len(ln) - 1); x = (W - tot) / 2
                for im, act, w in ln:
                    k = 1.0
                    if t >= w[1] - 0.04: k = 1 + 0.16 * math.sin(math.pi * min(1, (t - w[1] + 0.04) / 0.22)) if act else 1.0
                    vis = t >= w[1] - 0.06 if big else True   # en el gancho cada palabra entra cuando se dice
                    if vis: put(fr, im, x + im.width / 2, y + im.height / 2 + 40 * (1 - ain), k * (back((t - w[1] + 0.06) / 0.18) if big else 1), rot=(-2 if act else 0))
                    x += im.width + gap
                y += sz * 1.5
            return
# ---- piezas ----
def fmt(v): return f"{v:.2f}".replace('.', ',') + SP.get('cur', ' €')
def price(t):
    h = SP['hook']; f = font(150, HEAD); slash = ease((t - h['t_slash']) / 0.25) if t >= h['t_slash'] else 0
    im = Image.new('RGBA', (760, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, 759, 419), 44, fill=(0, 0, 0, 150)); d.rounded_rectangle((0, 0, 747, 407), 44, fill=(255, 255, 255, 255))
    d.text((48, 26), h['label'], font=font(40), fill=(120, 126, 150, 255))
    s = fmt(h['frm']); tw = f.getlength(s); x = (748 - tw) / 2; y = 92 if slash < 1 else 70
    d.text((x, y), s, font=f, fill=TH['ink'] + (255,) if slash < 0.5 else (170, 174, 190, 255))
    if slash > 0: d.line((x - 16, y + 108, x - 16 + (tw + 32) * slash, y + 82), fill=(232, 30, 44, 255), width=16)
    return im
def tile(c):
    k = ('tile', c)
    if k not in _C:
        im = Image.new('RGBA', (134, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((10, 10, 133, 159), 22, fill=(0, 0, 0, 160)); d.rounded_rectangle((0, 0, 123, 149), 22, fill=TH['acc2'] + (255,), outline=TH['ink'] + (255,), width=6)
        f = font(118, HEAD); d.text(((124 - f.getlength(c)) / 2, 2), c, font=f, fill=TH['ink'] + (255,)); _C[k] = im
    return _C[k]
def stamp(lines):
    k = ('st',) + tuple(lines)
    if k not in _C:
        f1, f2 = font(150, HEAD), font(44); w = int(max(f1.getlength(lines[0]), f2.getlength(lines[1])) + 90)
        im = Image.new('RGBA', (w, 290), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((10, 10, w - 1, 289), 30, fill=(0, 0, 0, 150)); d.rounded_rectangle((0, 0, w - 11, 279), 30, fill=(232, 30, 44, 255), outline=(255, 255, 255, 255), width=8)
        d.text(((w - 10 - f1.getlength(lines[0])) / 2, 6), lines[0], font=f1, fill=(255, 255, 255, 255)); d.text(((w - 10 - f2.getlength(lines[1])) / 2, 196), lines[1], font=f2, fill=(255, 255, 255, 255)); _C[k] = im
    return _C[k]
def burst(fr, t, t0, x0, y0, emo, n=12, seed=3):
    x = t - t0
    if not (0 <= x < 1.1): return
    r = np.random.RandomState(seed)
    for _ in range(n):
        ang = r.uniform(-math.pi * 0.95, -math.pi * 0.05); v = r.uniform(600, 1300); sz = int(r.uniform(70, 120)); rot = r.uniform(-240, 240)
        put(fr, EMO[emo].resize((sz, sz), Image.LANCZOS), x0 + math.cos(ang) * v * x, y0 + math.sin(ang) * v * x + 1700 * x * x, 1, min(1, x / 0.05, (1.1 - x) / 0.3), rot * x)
# ---- render ----
tot = SP['tot']; n = int(round(tot * FPS)); CH = SP['chips']; PHN = SP['phone']; RES = SP['result']; ST = SP['stamp']; CL = SP['close']
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
ONLY = [float(x) for x in os.environ.get('ONLY', '').split(',') if x]
for i in range(n):
    t = i / FPS
    if ONLY and not any(abs(t - o) < 0.5 / FPS for o in ONLY): continue
    fr = BGI.copy(); d = ImageDraw.Draw(fr)
    for px, py, sp_, sz, chh in PART:   # partículas que suben
        y = (py - sp_ * t) % H; d.text((px + 14 * math.sin(t * 1.3 + px), y), chh, font=font(int(sz * 5)), fill=(255, 255, 255, 26))
    # barra de progreso en 4 tramos + chip del paso
    seg = [c[0] for c in CH] + [tot]; ci = max(k for k in range(len(CH)) if t >= CH[k][0])
    for k in range(len(CH)):
        x0 = 60 + k * 243; d.rounded_rectangle((x0, 196, x0 + 228, 212), 8, fill=(255, 255, 255, 60))
        u = max(0, min(1, (t - seg[k]) / (seg[k + 1] - seg[k])))
        if u > 0: d.rounded_rectangle((x0, 196, x0 + max(16, 228 * u), 212), 8, fill=TH['acc'] + (255,))
    put(fr, card(CH[ci][1], 46, TH['ink'], TH['acc'], padx=22, pady=10, sh=6), 60 + card(CH[ci][1], 46, TH['ink'], TH['acc'], padx=22, pady=10, sh=6).width / 2, 130, back((t - CH[ci][0]) / 0.25), rot=-2)
    T1 = PHN['t_in']; hook = t < T1 + 0.25
    if hook:   # gancho: precio que se tacha
        h = SP['hook']; uo = ease((t - T1) / 0.25) if t > T1 else 0; sw = 2.5 * math.sin(t * 5)
        put(fr, price(t), W / 2, 930 + 120 * (1 - back(t / 0.35)) + 500 * uo, 1 - 0.2 * uo, 1 - uo, -3 + sw)
        if t >= h['t_slash']:
            k = back((t - h['t_slash']) / 0.3); f = font(170, HEAD); s = fmt(h['to'])
            im = Image.new('RGBA', (int(f.getlength(s)) + 70, 230), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
            dd.rounded_rectangle((10, 10, im.width - 1, 229), 36, fill=(0, 0, 0, 150)); dd.rounded_rectangle((0, 0, im.width - 11, 219), 36, fill=TH['ok'] + (255,)); dd.text((30, 2), s, font=f, fill=(255, 255, 255, 255))
            put(fr, im, W / 2 + 40, 1190 + 500 * uo, k * (1 - 0.2 * uo), 1 - uo, 4)
            burst(fr, t, h['t_slash'], W / 2, 1150, SP.get('fly', 'check'), 10, 5)
    if T1 <= t < CL['t'] + 0.3:   # móvil con la grabación
        u = back((t - T1) / 0.45, 1.4); uo = ease((t - CL['t']) / 0.3) if t > CL['t'] else 0
        ph, (x0, y0, kx, ky) = phone(t); cy = 690 + 1300 * (1 - u) + 1500 * uo; rot = 1.6 * math.sin(t * 1.7)
        put(fr, ph, W / 2, cy, 1, 1, rot)
        tp = SP['tap']
        if tp['t'] <= t < tp['t'] + 0.5:   # toque
            p = (t - tp['t']) / 0.5; x = W / 2 - PW / 2 + (tp['x'] - x0) * kx; y = cy - PH / 2 + (tp['y'] - y0) * ky; r = 26 + 80 * p
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
            dd.ellipse((x - r, y - r, x + r, y + r), outline=TH['acc'] + (int(255 * (1 - p)),), width=12); dd.ellipse((x - 26, y - 26, x + 26, y + 26), fill=TH['acc'] + (int(230 * (1 - p)),)); fr.alpha_composite(lay)
        if t < SP['t_tiles_off'] + 0.2:   # letras del código
            ls = SP['tiles']; uo2 = ease((t - SP['t_tiles_off']) / 0.2) if t > SP['t_tiles_off'] else 0
            stp = min(140, 960 / max(1, len(ls))); ksc = stp / 140   # códigos largos: fichas más pequeñas para que quepan
            xs = W / 2 - (len(ls) * stp - 16 * ksc) / 2
            for j, (c, tt) in enumerate(ls):
                if t >= tt: put(fr, tile(c), xs + j * stp + 62 * ksc, 1185 - 60 * math.sin(math.pi * min(1, (t - tt) / 0.3)) + 200 * uo2, back((t - tt) / 0.22) * ksc, 1 - uo2, 6 * math.sin(j * 2.1))
        if t >= RES['t']:   # contador del total
            u2 = back((t - RES['t']) / 0.3); v = RES['frm'] + (RES['to'] - RES['frm']) * ease((t - RES['t']) / 0.7)
            put(fr, card(fmt(v), 150, (255, 255, 255), TH['ok'], HEAD, padx=44, pady=12, sh=12), W / 2, 1185 + 1500 * uo, u2 * (1 + 0.06 * math.sin(math.pi * min(1, (t - RES['t']) / 0.9))), 1 - uo, -3)
            burst(fr, t, RES['t'] + 0.15, W / 2, 1100, SP.get('fly', 'check'), 12, 9)
        if t >= ST['t']:
            k = 2.2 - 1.2 * ease((t - ST['t']) / 0.18); put(fr, stamp(ST['lines']), 800, 330 + 1500 * uo, k, min(1, (t - ST['t']) / 0.08) * (1 - uo), -10)
        sh_ = SP['ship']
        if t >= sh_['t']:
            sc_ = card(sh_['text'], 62, TH['ink'], TH['card'], emo='truck', padx=30, pady=16)
            if sc_.width > 620: sc_ = sc_.resize((620, int(sc_.height * 620 / sc_.width)), Image.LANCZOS)
            put(fr, sc_, 60 + sc_.width / 2, 400 + 1500 * uo, back((t - sh_['t']) / 0.3), 1 - uo, 6)
    if t >= CL['t']:   # cierre
        tc = t - CL['t']
        put(fr, EMO[CL.get('emo', 'pin')].resize((300, 300), Image.LANCZOS), W / 2, 560 - 40 * abs(math.sin(tc * 5)), back((tc - 0.05) / 0.35), 1, -10 + 6 * math.sin(tc * 4))
        put(fr, card(CL['word'], 190, TH['ink'], TH['acc'], HEAD, padx=50, pady=10, sh=14), W / 2, 860, back((tc - 0.15) / 0.3), 1, -3)
        put(fr, card(CL['handle'], 66, TH['ink'], TH['card'], padx=40, pady=18), W / 2, 1090, back((tc - 0.3) / 0.3), 1, 2)
        burst(fr, t, CL['t'] + 0.2, W / 2, 800, CL.get('burst', 'fire'), 10, 4)
    captions(fr, t, hook and t < T1)
    # golpe de zoom y sacudida de todo el cuadro
    z = 1.0; dx = dy = 0
    for p in SP.get('punches', []):
        x = t - p[0]
        if 0 <= x < 0.28: z += p[1] * (1 - x / 0.28) ** 2
    x = t - ST['t']
    if 0.12 <= x < 0.5: a = 16 * (1 - (x - 0.12) / 0.38) ** 2; dx = a * math.sin(x * 80); dy = a * math.cos(x * 61)
    if z > 1.002 or dx or dy:
        w2, h2 = W / z, H / z; fr = fr.transform((W, H), Image.AFFINE, (1 / z, 0, (W - w2) / 2 + dx, 0, 1 / z, (H - h2) / 2 + dy), resample=Image.BILINEAR)
    if ONLY: fr.convert('RGB').save(OUT.replace('.mp4', f'_{t:.2f}.jpg'), quality=88); continue
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait(); print('ok', OUT)
