#!/usr/bin/env python3
"""Formato explicativo con diseño propio (8 nov 2026). Mismos pasos que el vídeo de referencia
(gancho de precio → grabación en tarjeta → pasos → código → descuento → guárdalo/sígueme, subtítulos karaoke),
pero estilo nuestro: fondo menta liso, tarjetas blancas redondeadas con sombra suave (sin bordes),
etiqueta de precio con pegatina verde, pasos en horizontal 1-2-3, código en píldora oscura con cursor,
insignia redonda de descuento y cierre con chincheta.
Uso: explainer2.py spec.json out_video.mp4  (sin audio; luego mux3.py)
"""
import json, math, os, subprocess, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SP = json.load(open(sys.argv[1])); OUT = sys.argv[2]
W, H, FPS = 1080, 1920, 30
BG = (226, 241, 232); INK = (15, 23, 42); GREEN = (22, 163, 74); MUTED = (120, 132, 150); LINE = (200, 214, 206); WHITE = (255, 255, 255)
_F = {}


def font(sz, w=800):
    k = (sz, w)
    if k not in _F:
        f = ImageFont.truetype(ROOT + 'fonts/tiktoksans_var.ttf', sz); f.set_variation_by_axes([36, 100, w, 0]); _F[k] = f
    return _F[k]


EMO = {os.path.basename(f)[2:-4]: Image.open(f).convert('RGBA') for f in glob.glob(ROOT + 'engine/emo/n_*.png')}


def ease(u): u = max(0., min(1., u)); return 1 - (1 - u) ** 3
def back(u):
    u = max(0., min(1., u)); c = 1.6; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def interp(rm, t):
    if t <= rm[0][0]: return rm[0][1]
    for a, b in zip(rm, rm[1:]):
        if a[0] <= t <= b[0]: return a[1] + (b[1] - a[1]) * ((t - a[0]) / max(1e-6, b[0] - a[0]))
    return rm[-1][1]


def put(fr, im, cx, cy, k=1.0, alpha=1.0, rot=0):
    if k <= 0.01 or alpha <= 0.01: return
    if k != 1: im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


_SH = {}


def soft_card(w, h, r=44, fill=WHITE):
    k = (w, h, r, fill)
    if k not in _SH:
        p = 40; im = Image.new('RGBA', (w + 2 * p, h + 2 * p), (0, 0, 0, 0))
        sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).rounded_rectangle((p, p + 14, p + w, p + h + 14), r, fill=70)
        sh = sh.filter(ImageFilter.GaussianBlur(20)); shadow = Image.new('RGBA', im.size, (20, 60, 40, 255)); shadow.putalpha(sh)
        im.alpha_composite(shadow); ImageDraw.Draw(im).rounded_rectangle((p, p, p + w, p + h), r, fill=fill)
        _SH[k] = im
    return _SH[k].copy()


def pill(text, sz, fg, bg, padx=34, pady=14, w=800, r=None):
    f = font(sz, w); tw = f.getlength(text); hh = int(sz * 1.25) + 2 * pady
    im = Image.new('RGBA', (int(tw + 2 * padx), hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, hh - 1), r if r is not None else hh // 2, fill=bg)
    d.text((padx, pady - sz * 0.04), text, font=f, fill=fg); return im


def fmt(v): return f"{v:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')


# ---------- gancho: etiqueta de precio ----------
def price_tag(t):
    w, h = 760, 400; im = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
    poly = [(40 + 120, 40), (40 + w, 40), (40 + w, 40 + h), (40 + 120, 40 + h), (40, 40 + h / 2)]
    sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).polygon([(x, y + 14) for x, y in poly], fill=70); sh = sh.filter(ImageFilter.GaussianBlur(18))
    s = Image.new('RGBA', im.size, (20, 60, 40, 255)); s.putalpha(sh); im.alpha_composite(s)
    d = ImageDraw.Draw(im); d.polygon(poly, fill=WHITE); d.ellipse((40 + 70, 40 + h / 2 - 22, 40 + 114, 40 + h / 2 + 22), fill=BG)
    d.text((220, 90), SP['price_label'], font=font(40, 700), fill=MUTED)
    disc = t >= SP['t_stamp'] + 0.25
    f = font(140, 900); txt = SP['price_from']
    d.text((220, 150), txt, font=f, fill=MUTED if disc else INK)
    if disc:
        p = ease((t - SP['t_stamp'] - 0.25) / 0.3); tw = f.getlength(txt)
        d.line((215, 235, 215 + (tw + 10) * p, 235), fill=(220, 50, 60), width=10)
    if t >= SP['t_stamp'] + 0.55:
        d.text((220, 320), SP['price_to'], font=font(84, 900), fill=GREEN)
    return im


def sticker(lines, sizes, d0=260):
    im = Image.new('RGBA', (d0 + 20, d0 + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((10, 10, d0 + 10, d0 + 10), fill=GREEN, outline=WHITE, width=10)
    tot = sum(int(s * 1.1) for s in sizes); y = (d0 + 20 - tot) / 2
    for l, s in zip(lines, sizes):
        f = font(s, 900); d.text(((d0 + 20 - f.getlength(l)) / 2, y - s * 0.1), l, font=f, fill=WHITE); y += int(s * 1.1)
    return im


# ---------- grabación en tarjeta ----------
REC = SP['rec']; CROP = SP['crop']; CW = 920; CH = int(CW * CROP[3] / CROP[2])
TMP = OUT + '_frames'; os.makedirs(TMP, exist_ok=True)
if not os.path.exists(TMP + '/f_0001.jpg'):
    subprocess.run(['ffmpeg', '-v', 'error', '-i', REC, '-vf', f'fps=30,crop={CROP[2]}:{CROP[3]}:{CROP[0]}:{CROP[1]},scale={CW}:{CH}',
                    '-q:v', '3', TMP + '/f_%04d.jpg'], check=True)
NREC = len(os.listdir(TMP))
MASK = Image.new('L', (CW, CH), 0); ImageDraw.Draw(MASK).rounded_rectangle((0, 0, CW - 1, CH - 1), 44, fill=255)


def rec_card(rt):
    i = max(1, min(NREC, int(round(rt * 30)) + 1)); im = soft_card(CW, CH)
    im.paste(Image.open(f'{TMP}/f_{i:04d}.jpg').convert('RGB'), (40, 40), MASK); return im


# ---------- pasos 1-2-3 ----------
def stepper(fr, t, cy, alpha):
    st = SP['steps']; n = len(st); xs = [W / 2 + (i - (n - 1) / 2) * 300 for i in range(n)]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(n - 1):
        done = t >= st[i][2]; d.line((xs[i] + 50, cy, xs[i + 1] - 50, cy), fill=GREEN if done else LINE, width=8)
    for i, (lab, t_on, t_done) in enumerate(st):
        x = xs[i]; done = t >= t_done; act = t_on <= t < t_done
        k = 1 + 0.12 * math.sin(min(1, (t - t_on) / 0.3) * math.pi) if act else 1; r = 46 * k
        if done or act: d.ellipse((x - r, cy - r, x + r, cy + r), fill=GREEN)
        else: d.ellipse((x - r, cy - r, x + r, cy + r), fill=WHITE, outline=LINE, width=6)
        if done: d.line((x - 18, cy + 2, x - 4, cy + 16, x + 20, cy - 14), fill=WHITE, width=9)
        else:
            f = font(46, 900); num = str(i + 1); d.text((x - f.getlength(num) / 2, cy - 30), num, font=f, fill=WHITE if act else MUTED)
        f = font(40, 800 if (act or done) else 650); d.text((x - f.getlength(lab) / 2, cy + 64), lab, font=f, fill=INK if (act or done) else MUTED)
    if alpha < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * alpha)))
    fr.alpha_composite(lay)


def code_pill(t):
    typed = ''.join(c for c, tt in SP['code_letters'] if t >= tt); full = ''.join(c for c, _ in SP['code_letters'])
    f = font(104, 900); w = int(f.getlength(full) + 150); h = 170
    im = Image.new('RGBA', (w, h + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((24, 0), SP['code_label'], font=font(32, 800), fill=GREEN)
    d.rounded_rectangle((0, 46, w - 1, 46 + h - 1), 40, fill=INK)
    d.text((60, 46 + 22), typed, font=f, fill=WHITE)
    if len(typed) < len(full) and int(t * 3) % 2 == 0:
        x = 60 + f.getlength(typed) + 8; d.rounded_rectangle((x, 46 + 38, x + 12, 46 + h - 38), 4, fill=GREEN)
    return im


def captions(fr, t):
    for ch in SP['captions']:
        if ch['t0'] <= t < ch['t1']:
            f = font(86, 900); d = ImageDraw.Draw(fr); words = ch['words']
            lines, cur, ws = [], [], 0
            for w in words:
                lw = f.getlength(w[0]) + 24
                if cur and ws + lw > 940: lines.append(cur); cur, ws = [], 0
                cur.append(w); ws += lw
            lines.append(cur); y = 190
            for ln in lines:
                tot = sum(f.getlength(w[0]) for w in ln) + 24 * (len(ln) - 1); x = (W - tot) / 2
                for w in ln:
                    d.text((x, y), w[0], font=f, fill=GREEN if w[1] <= t < w[2] + 0.12 else INK); x += f.getlength(w[0]) + 24
                y += 102
            return


tot = SP['tot']; n = int(round(tot * FPS))
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
BGI = Image.new('RGBA', (W, H), BG + (255,))
SEO = pill(SP['seo'], 24, (90, 120, 100, 160), (0, 0, 0, 0), padx=4, pady=2, w=650) if SP.get('seo') else None
T1, T2, T3 = SP['t_scene2'], SP['t_modal'], SP['t_follow']
for i in range(n):
    t = i / FPS; fr = BGI.copy()
    if SEO: fr.alpha_composite(SEO, ((W - SEO.width) // 2, 14))
    if t < T1 + 0.35:   # gancho
        uo = ease((t - T1) / 0.35) if t > T1 else 0
        sw = 3 * math.sin(t * 2.4)
        put(fr, price_tag(t), W / 2, 980 + 90 * (1 - back(t / 0.45)) - 250 * uo, 1 - 0.3 * uo, alpha=1 - uo, rot=-4 + sw)
        if t >= SP['t_stamp']:
            k = 1.7 - 0.7 * ease((t - SP['t_stamp']) / 0.22)
            put(fr, sticker(SP['sticker1'], [76, 34]), 820, 760 - 250 * uo, k * (1 - 0.3 * uo), alpha=1 - uo, rot=12)
    if T1 <= t < T3 + 0.35:   # grabación + pasos
        u = ease((t - T1) / 0.4); uo = ease((t - T3) / 0.35) if t > T3 else 0
        put(fr, rec_card(interp(SP['rmap'], t)), W / 2, 830 + 700 * (1 - u) - 150 * uo, 1 - 0.1 * uo, alpha=1 - uo)
        stepper(fr, t, 1390 + 500 * (1 - ease((t - T1 - 0.15) / 0.4)) - 150 * uo, (1 - uo))
        if SP['code_letters'][0][1] - 0.3 <= t < T2:
            uo2 = ease((t - T2 + 0.25) / 0.25) if t > T2 - 0.25 else 0
            put(fr, code_pill(t), W / 2, 1060, back((t - SP['code_letters'][0][1] + 0.3) / 0.35) * (1 - uo2))
        if SP['t_tap'] <= t < SP['t_tap'] + 0.55:
            p = (t - SP['t_tap']) / 0.55; x, y = SP['tap_xy']
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = 28 + 60 * p
            d.ellipse((x - r, y - r, x + r, y + r), outline=GREEN + (int(255 * (1 - p)),), width=9); d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=GREEN + (int(220 * (1 - p)),))
            fr.alpha_composite(lay)
        if t >= SP['t_disc']:
            k = 1.6 - 0.6 * ease((t - SP['t_disc']) / 0.22)
            put(fr, sticker(SP['sticker2'], [86, 34], 290), 860, 1150 - 150 * uo, k, alpha=1 - uo, rot=-10)
        if t >= SP['t_ship']:
            put(fr, pill(SP['ship'], 52, INK, WHITE, padx=40, pady=18), 360, 1150 - 150 * uo, back((t - SP['t_ship']) / 0.35), alpha=1 - uo, rot=-3)
    if t >= T3:   # cierre
        put(fr, EMO['pin'].resize((280, 280), Image.LANCZOS), W / 2, 760, back((t - T3 - 0.1) / 0.45), rot=-12)
        f = font(110, 900); g = SP['save']; im = Image.new('RGBA', (int(f.getlength(g)) + 20, 150), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 0), g, font=f, fill=INK); put(fr, im, W / 2, 1010, back((t - T3 - 0.25) / 0.45))
        put(fr, pill(SP['handle'], 58, WHITE, GREEN, padx=48, pady=18), W / 2, 1190, back((t - T3 - 0.45) / 0.45))
    captions(fr, t)
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait()
print('ok', OUT)
