#!/usr/bin/env python3
"""Formato "explicativo animado" (inspirado en un vídeo de 2k likes, 8 nov 2026).
Fondo claro con puntos, tarjetas con sombra desplazada, subtítulos karaoke en mayúsculas con la palabra activa
resaltada en amarillo, ticket con sello "NO PAGUES ESTO", trozo real de la grabación dentro de una tarjeta,
checklist que se va marcando, letras del código que salen al teclear, sello del descuento y cierre "sígueme".
Uso: explainer.py spec.json out_video.mp4   (sin audio; el audio lo pone mux3.py)
"""
import json, math, os, subprocess, sys, glob
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SP = json.load(open(sys.argv[1])); OUT = sys.argv[2]
W, H, FPS = 1080, 1920, 30
BG = (243, 240, 233); INK = (22, 24, 44); YEL = (255, 214, 64); RED = (226, 44, 62); BLUE = (64, 72, 210); GREY = (200, 200, 208)
_F = {}


def font(sz, w=800):
    k = (sz, w)
    if k not in _F:
        f = ImageFont.truetype(ROOT + 'fonts/tiktoksans_var.ttf', sz); f.set_variation_by_axes([36, 100, w, 0]); _F[k] = f
    return _F[k]


EMO = {os.path.basename(f)[2:-4]: Image.open(f).convert('RGBA') for f in glob.glob(ROOT + 'engine/emo/n_*.png')}
EMO['check'] = Image.open(ROOT + 'engine/emo/check.png').convert('RGBA')


def ease(u): u = max(0., min(1., u)); return 1 - (1 - u) ** 3
def back(u):
    u = max(0., min(1., u)); c = 1.7; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


# ---------- fondo con puntos ----------
BGIMG = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(BGIMG)
for y in range(20, H, 44):
    for x in range(20, W, 44): d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(214, 210, 200, 255))


def card(w, h, r=30, fill=(255, 255, 255, 255), sh=14, bw=6):
    im = Image.new('RGBA', (w + sh + 2, h + sh + 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((sh, sh, w + sh - 1, h + sh - 1), r, fill=INK + (255,))
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=INK + (255,), width=bw)
    return im


def paste_scaled(fr, im, cx, cy, k=1.0, rot=0.0, alpha=1.0):
    if k <= 0.01 or alpha <= 0.01: return
    if k != 1.0: im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ---------- ticket ----------
def receipt(total, strike):
    w, h = 520, 760; im = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    zig = [(0, 0), (w, 0), (w, h - 20)] + [(w - i * 26 - (13 if j else 0), h - (0 if j else 20)) for i in range(w // 26 + 1) for j in (0, 1)][:-1] + [(0, h - 20)]
    d.polygon([(x + 12, y + 12) for x, y in zig], fill=INK + (255,)); d.polygon(zig, fill=(255, 255, 255, 255), outline=INK + (255,))
    e = EMO['hacoo'].resize((110, 110), Image.LANCZOS); im.alpha_composite(e, ((w - 110) // 2, 40))
    d.text((40, 190), 'Pedido', font=font(40, 750), fill=INK)
    for i in range(6):
        y = 270 + i * 50; d.rounded_rectangle((40, y, 330 - (i % 3) * 60, y + 18), 9, fill=GREY); d.rounded_rectangle((380, y, 480, y + 18), 9, fill=GREY)
    for x in range(40, 480, 22): d.line((x, 590, x + 11, 590), fill=INK, width=4)
    d.text((40, 620), 'TOTAL', font=font(52, 850), fill=INK)
    tw = font(52, 850).getlength(total); d.text((480 - tw, 620), total, font=font(52, 850), fill=INK)
    if strike > 0: d.line((30, 652, 30 + 470 * strike, 652), fill=RED, width=8)
    return im


def stamp(lines, sizes, rot):
    f = [font(s, 900) for s in sizes]; tw = max(ff.getlength(l) for ff, l in zip(f, lines)); th = sum(int(s * 1.05) for s in sizes)
    w, h = int(tw + 70), th + 50; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, w - 4, h - 4), 14, fill=(255, 255, 255, 235), outline=RED, width=9)
    y = 22
    for ff, l, s in zip(f, lines, sizes):
        d.text(((w - ff.getlength(l)) / 2, y - s * 0.12), l, font=ff, fill=RED); y += int(s * 1.05)
    return im.rotate(rot, resample=Image.BICUBIC, expand=True)


# ---------- grabación dentro de la tarjeta ----------
REC = SP['rec']; CROP = SP['crop']; CW, CH = 900, int(900 * CROP[3] / CROP[2])
TMP = OUT + '_frames'; os.makedirs(TMP, exist_ok=True)
if not os.path.exists(TMP + '/f_0001.jpg'):
    subprocess.run(['ffmpeg', '-v', 'error', '-i', REC, '-vf', f'fps=30,crop={CROP[2]}:{CROP[3]}:{CROP[0]}:{CROP[1]},scale={CW - 12}:{CH - 12}',
                    '-q:v', '3', TMP + '/f_%04d.jpg'], check=True)
NREC = len(os.listdir(TMP))


def rec_at(rt):
    i = max(1, min(NREC, int(round(rt * 30)) + 1)); return Image.open(f'{TMP}/f_{i:04d}.jpg').convert('RGBA')


def interp(rm, t):
    if t <= rm[0][0]: return rm[0][1]
    for a, b in zip(rm, rm[1:]):
        if a[0] <= t <= b[0]: return a[1] + (b[1] - a[1]) * ((t - a[0]) / max(1e-6, b[0] - a[0]))
    return rm[-1][1]


SHOT = card(CW, CH, 30)
MASK = Image.new('L', (CW - 12, CH - 12), 0); ImageDraw.Draw(MASK).rounded_rectangle((0, 0, CW - 13, CH - 13), 24, fill=255)


# ---------- checklist ----------
def checklist(t):
    w, h = 820, 360; im = card(w, h, 26); d = ImageDraw.Draw(im)
    d.text((40, 26), SP['list_title'], font=font(30, 800), fill=BLUE)
    for i, (lab, t_on, t_done) in enumerate(SP['items']):
        y = 86 + i * 66
        if i: [d.line((40 + x, y - 10, 40 + x + 8, y - 10), fill=GREY, width=2) for x in range(0, w - 80, 14)]
        done = t >= t_done; act = t >= t_on and not done
        if done:
            d.ellipse((40, y + 6, 80, y + 46), fill=BLUE); d.line((50, y + 26, 58, y + 35, 71, y + 17), fill='white', width=6)
        else:
            d.ellipse((40, y + 6, 80, y + 46), fill=YEL if act else (255, 255, 255), outline=INK if act else GREY, width=4)
        col = BLUE if act else (INK if done else (150, 150, 160))
        d.text((100, y + 4), lab, font=font(40, 800 if act or done else 650), fill=col)
        if i == 1:
            typed = ''.join(ch for ch, tt in SP['code_letters'] if t >= tt)
            x0 = 100 + font(40, 800).getlength(lab) + 20
            if typed:
                fw = font(38, 900); bw = fw.getlength(typed) + 30
                d.rounded_rectangle((x0, y + 4, x0 + bw, y + 50), 8, fill=INK); d.text((x0 + 15, y + 4), typed, font=fw, fill=YEL)
            else:
                d.rounded_rectangle((x0, y + 8, x0 + 170, y + 46), 8, fill=GREY)
    return im


# ---------- subtítulos karaoke ----------
def caption(fr, t):
    for ch in SP['captions']:
        if ch['t0'] <= t < ch['t1']:
            f = font(66, 850); words = ch['words']; lines = []; cur = []; wsum = 0
            for wd in words:
                lw = f.getlength(wd[0]) + 28
                if cur and wsum + lw > 900: lines.append(cur); cur = []; wsum = 0
                cur.append(wd); wsum += lw
            lines.append(cur)
            d = ImageDraw.Draw(fr); y = 190
            for ln in lines:
                tot = sum(f.getlength(w[0]) for w in ln) + 28 * (len(ln) - 1); x = (W - tot) / 2
                for w in ln:
                    lw = f.getlength(w[0])
                    if w[1] <= t < w[2] + 0.12:
                        d.rounded_rectangle((x - 12, y + 4, x + lw + 12, y + 84), 10, fill=YEL)
                    d.text((x, y), w[0], font=f, fill=INK); x += lw + 28
                y += 92
            return


# ---------- render ----------
tot = SP['tot']; n = int(round(tot * FPS))
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
SEO = None
if SP.get('seo'):
    f = font(26, 650); SEO = Image.new('RGBA', (int(f.getlength(SP['seo'])) + 10, 40), (0, 0, 0, 0))
    ImageDraw.Draw(SEO).text((5, 4), SP['seo'], font=f, fill=INK + (110,))
T1, T2, T3 = SP['t_scene2'], SP['t_modal'], SP['t_follow']
for i in range(n):
    t = i / FPS; fr = BGIMG.copy()
    if SEO: fr.alpha_composite(SEO, ((W - SEO.width) // 2, 14))
    # escena 1: ticket
    if t < T1 + 0.3:
        u_in = back(t / 0.45); u_out = ease((t - T1) / 0.3) if t > T1 else 0
        strike = ease((t - SP['t_stamp'] - 0.2) / 0.35) if t > SP['t_stamp'] else 0
        paste_scaled(fr, receipt(SP['total'], strike), W / 2, 1060 + 80 * (1 - u_in) - 300 * u_out, 0.95 * (1 - 0.4 * u_out), alpha=1 - u_out)
        if t >= SP['t_stamp']:
            k = 1.6 - 0.6 * ease((t - SP['t_stamp']) / 0.22)
            paste_scaled(fr, stamp(SP['stamp1'], [70, 70], 10), W / 2 - 40, 900 - 300 * u_out, k * (1 - 0.4 * u_out), alpha=1 - u_out)
    # escenas 2-4: grabación + checklist
    if T1 <= t < T3 + 0.3:
        u = ease((t - T1) / 0.35); uo = ease((t - T3) / 0.3) if t > T3 else 0
        sh = SHOT.copy(); rec = rec_at(interp(SP['rmap'], t)); sh.paste(rec, (6, 6), MASK)
        cy = 860 + 500 * (1 - u) - 200 * uo
        paste_scaled(fr, sh, W / 2 + 7, cy, alpha=1 - uo)
        cl = checklist(t); u2 = ease((t - T1 - 0.15) / 0.35)
        paste_scaled(fr, cl, W / 2 + 7, 1440 + 500 * (1 - u2) - 200 * uo, alpha=1 - uo)
        # letras del código en fichas
        if t < T2:
            ls = [(c, tt) for c, tt in SP['code_letters'] if t >= tt]; tile = 118; gap = 14
            x0 = W / 2 - (len(SP['code_letters']) * (tile + gap) - gap) / 2
            for j, (c, tt) in enumerate(ls):
                im = card(tile, 140, 16, sh=8, bw=5); d = ImageDraw.Draw(im); ff = font(96, 900)
                d.text(((tile - ff.getlength(c)) / 2, 8), c, font=ff, fill=INK)
                paste_scaled(fr, im, x0 + j * (tile + gap) + tile / 2, SP['tiles_y'], back((t - tt) / 0.25))
        # sello del descuento
        if t >= SP['t_disc']:
            k = 1.5 - 0.5 * ease((t - SP['t_disc']) / 0.22)
            paste_scaled(fr, stamp(SP['stamp2'], [74, 34], -8), 800, 1540 - 200 * uo, k, alpha=1 - uo)
        if t >= SP['t_ship']:
            paste_scaled(fr, stamp(SP['stamp3'], [44], 5), 330, 1720 - 200 * uo, back((t - SP['t_ship']) / 0.3), alpha=1 - uo)
        # toque en el botón
        if SP['t_tap'] <= t < SP['t_tap'] + 0.6:
            p = (t - SP['t_tap']) / 0.6; x, y = SP['tap_xy']
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = 30 + 60 * p
            d.ellipse((x - r, y - r, x + r, y + r), outline=BLUE + (int(255 * (1 - p)),), width=8); d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=BLUE + (int(200 * (1 - p)),))
            fr.alpha_composite(lay)
    # escena final: sígueme
    if t >= T3:
        u = back((t - T3 - 0.1) / 0.4)
        av = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(av)
        d.ellipse((10, 10, 299, 299), fill=INK); d.ellipse((0, 0, 289, 289), fill='white', outline=INK, width=8)
        av.alpha_composite(EMO['hacoo'].resize((170, 170), Image.LANCZOS), (60, 60)); paste_scaled(fr, av, W / 2, 760, u)
        f = font(56, 800); hw = int(f.getlength(SP['handle'])) + 80
        pill = card(hw, 100, 50, sh=10); ImageDraw.Draw(pill).text((40, 16), SP['handle'], font=f, fill=INK); paste_scaled(fr, pill, W / 2, 1010, u)
        fol = t >= SP['t_followed']; lab = SP['followed'] if fol else SP['follow']
        bw = int(font(54, 900).getlength(lab)) + 110
        btn = card(bw, 110, 24, fill=(255, 255, 255, 255) if fol else BLUE + (255,), sh=10)
        ImageDraw.Draw(btn).text((55, 18), lab, font=font(54, 900), fill=INK if fol else (255, 255, 255)); paste_scaled(fr, btn, W / 2, 1180, back((t - T3 - 0.3) / 0.4))
        if SP['t_followed'] - 0.35 <= t < SP['t_followed'] + 0.3:
            p = (t - SP['t_followed'] + 0.35) / 0.65; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = 25 + 55 * p
            d.ellipse((W / 2 + 60 - r, 1190 - r, W / 2 + 60 + r, 1190 + r), outline=INK + (int(255 * (1 - p)),), width=7); fr.alpha_composite(lay)
    caption(fr, t)
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait()
print('ok', OUT)
