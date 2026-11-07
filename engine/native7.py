import sys, json, subprocess, math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
# usage: native.py rec.mp4 spec.json out.mp4
REC, SPEC, OUT = sys.argv[1:4]
import os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
FONT = D + 'fonts/Oswald-Bold.ttf'
W, H, FPS = 1080, 1920, 60
sp = json.load(open(SPEC))
EMO = {'star': Image.open(D + 'engine/emo_star.png').convert('RGBA'),
       'flushed': Image.open(D + 'engine/emo_flushed.png').convert('RGBA')}
for _n, _f in {'money':'b42','scream':'b41','shush':'b40','party':'b51','devil':'b30','halo':'b03','wink':'b35','cowboy':'b20','crazy':'b55','peek':'b62','grin':'b04','laugh':'b02'}.items():
    EMO[_n] = Image.open(D + 'engine/emo/' + _f + '.png').convert('RGBA')
EMO['check'] = Image.open(D + 'engine/emo/check.png').convert('RGBA')
import glob, os
sys.path.insert(0, D + 'engine'); from tktext import render_block, outline_block
for _f in glob.glob(D + 'engine/emo/n_*.png'): EMO[os.path.basename(_f)[2:-4]] = Image.open(_f).convert('RGBA')
FONTS = {'condensed': D + 'fonts/tmp_w500_latin.ttf', 'classic': D + 'fonts/tmp_w500_latin.ttf', 'tkbox': D + 'fonts/tmp_w500_latin.ttf', 'tkplain': D + 'fonts/tmp_w500_latin.ttf'}

cap = cv2.VideoCapture(REC); rfps = cap.get(cv2.CAP_PROP_FPS); RN = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fw, fh = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
S = H / fh; dw = int(fw * S); X0 = (W - dw) // 2
REC_END = RN / rfps
class _Seq:
    i = -1; f = None
    def get(self, k):
        k = min(k, RN - 1)
        if k < self.i:
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, k - 1)); self.i = max(0, k - 1) - 1
        while self.i < k:
            ok, fr = cap.read()
            if not ok: break
            self.f = cv2.resize(fr, (dw, H), interpolation=cv2.INTER_AREA); self.i += 1
        return self.f
SEQ = _Seq()

def check_icon(sz):
    im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, sz - 1, sz - 1), int(sz * 0.18), fill=(52, 199, 89, 255))
    d.line((sz * .22, sz * .52, sz * .42, sz * .72, sz * .78, sz * .3), fill='white', width=max(3, sz // 8), joint='curve')
    return im

_tc = {}
SQ = {'condensed': 1.0, 'classic': 1.0, 'tkbox': 1.0, 'tkplain': 1.0}
def _txt_piece(v, font, st, sq, fill='white', glow=False):
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), v, font=font, stroke_width=st)
    asc, desc = font.getmetrics()
    pad = 14 if glow else 0
    im = Image.new('RGBA', (r - l + 4 + 2 * pad, asc + desc + 2 * st + 4 + 2 * pad), (0, 0, 0, 0))
    if glow:
        from PIL import ImageFilter
        g = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).text((2 - l + pad, st + 2 + pad), v, font=font, fill=(255, 214, 0, 255), stroke_width=st + 4, stroke_fill=(255, 214, 0, 255))
        g = g.filter(ImageFilter.GaussianBlur(9)); a = g.split()[3].point(lambda x: int(x * 0.75)); g.putalpha(a)
        im.alpha_composite(g)
    ImageDraw.Draw(im).text((2 - l + pad, st + 2 + pad), v, font=font, fill=fill, stroke_width=st, stroke_fill='black')
    if glow: im = im.crop((pad - 0, pad, im.width - pad, im.height - pad)) if False else im
    return im.resize((max(1, int(im.width * sq)), im.height), Image.LANCZOS)

def text_img(line, size, style='condensed'):
    k = (line, size, style)
    if k in _tc: return _tc[k]
    font = ImageFont.truetype(FONTS[style], size)
    st = max(3, round(size / 17))
    if style == 'tkbox': st = 0
    fillc = (18, 18, 18) if style == 'tkbox' else 'white'
    pieces = []
    for p in line.split('|'):
        if p.startswith('emo:'):
            name = p[4:]
            e = EMO[name].resize((int(size * 0.9), int(size * 0.9)), Image.LANCZOS)
            pieces.append(('img', e))
        elif p.startswith('hl:'):
            pieces.append(('hl', _txt_piece(p[3:], font, st, SQ[style], fill=(255, 225, 60), glow=True)))
        elif p:
            pieces.append(('txt', _txt_piece(p, font, st, SQ[style], fill=fillc)))
    if not pieces: pieces = [("txt", Image.new("RGBA", (2, int(size * 1.2)), (0, 0, 0, 0)))]
    hgt = max((im.height - 28) if k == 'hl' else im.height for k, im in pieces)
    out = Image.new('RGBA', (sum((im.width - 28) if k == 'hl' else im.width for k, im in pieces) + 10, hgt), (0, 0, 0, 0))
    x = 0; asc = font.getmetrics()[0]
    for kind, im in pieces:
        if kind == 'hl':
            out.alpha_composite(im, (x - 14, -14)) if False else None
            out.alpha_composite(im.crop((14, 14, im.width - 14, im.height - 14)), (x, 0))
            x += im.width - 28; continue
        if kind == 'txt':
            out.alpha_composite(im, (x, 0))
        else:
            out.alpha_composite(im, (x + 3, int(st + 2 + asc * 0.55 - im.height / 2)))
        x += im.width + (6 if kind == 'img' else 0)
    _tc[k] = out
    return out

def draw_texts(base, t):
    for it in sp['texts']:
        if not (it['t0'] <= t < it['t1']): continue
        st = it.get('style', 'condensed')
        if st == 'nat':
            key = ('nat', tuple(it['lines']), it.get('size', 62), it.get('sd', 15))
            if key not in _tc: _tc[key] = outline_block(it['lines'], it.get('size', 62), EMO, 700, it.get('sd', 15))
            im = _tc[key]; base.alpha_composite(im, (int(W / 2 - im.width / 2), int(it['y'] - im.height / 2))); continue
        if st in ('tk','ol'):
            u = 1.0 if it.get('nopop') else min(1.0, (t - it['t0']) / 0.2)
            k = 0.86 + 0.14 * u + 0.06 * math.sin(u * math.pi)
            key = (st, tuple(it['lines']), it.get('size', 64))
            if key not in _tc: _tc[key] = (outline_block(it['lines'], it.get('size', 90), EMO) if st == 'ol' else render_block(it['lines'], it.get('size', 64), 'box', EMO, 500))
            im = _tc[key]
            if k != 1.0: im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
            base.alpha_composite(im, (int(W / 2 - im.width / 2), int(it['y'] - im.height / 2)))
            continue
        ims = []
        for line in it['lines']:
            sz = line if isinstance(line, str) else line[1]
            ln = line if isinstance(line, str) else line[0]
            ims.append((text_img(ln, sz, st), sz))
        gap = 0.0 if st == 'condensed' else 0.0
        tight = [int(sz * (1.13 if st == 'condensed' else 1.42 if st == 'tkbox' else 1.22)) for _, sz in ims]
        total = sum(tight)
        y = it['y'] - total / 2
        u = 1.0 if it.get('nopop') else min(1.0, (t - it['t0']) / 0.2)
        k = 0.86 + 0.14 * u + 0.06 * math.sin(u * math.pi)
        for (im, sz), h in zip(ims, tight):
            cy = y + h / 2
            if st == 'tkbox':
                px, py = int(sz * .32), int(sz * .14); bw, bh = int(im.width * k) + 2 * px, int(im.height * k) + 2 * py
                lay = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((0, 0, bw - 1, bh - 1), int(sz * .28), fill=(255, 255, 255, 255))
                base.alpha_composite(lay, (int(W / 2 - bw / 2), int(cy - bh / 2)))
            if im.width > 860:
                f = 860 / im.width; im = im.resize((860, max(1, int(im.height * f))), Image.LANCZOS)
            if k != 1.0:
                im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
            base.alpha_composite(im, (int(W / 2 - im.width / 2), int(cy - im.height / 2)))
            y += h

def hand_ellipse(base, box, prog, seed, col=(222, 18, 34, 255)):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rx, ry = (x1 - x0) / 2 + 22, (y1 - y0) / 2 + 26
    n = 90; end = 1.08 * prog; tilt = -0.025
    pts = []
    for i in range(int(n * end) + 1):
        a = -2.4 + 2 * math.pi * i / n
        j = 1 + 0.05 * math.sin(i * 0.21 + seed) - 0.04 * (i / n)
        x = rx * j * math.cos(a); y = ry * j * math.sin(a)
        pts.append((cx + x * math.cos(tilt) - y * math.sin(tilt), cy + x * math.sin(tilt) + y * math.cos(tilt)))
    if len(pts) > 1:
        lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
        dd.line(pts, fill=col, width=9, joint='curve')
        for p in (pts[0], pts[-1]):
            dd.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=col)
        base.alpha_composite(lay)

def draw_marks(base, t):
    d = ImageDraw.Draw(base)
    for m in sp.get('marks', []):
        if not (m['t0'] <= t < m['t1']): continue
        prog = min(1.0, (t - m['t0']) / 0.35)
        if m['kind'] == 'circle':
            hand_ellipse(base, m['box'], prog, 3, tuple(m.get('color', (222, 18, 34, 255))))
            if m.get('label') and prog > 0.6:
                f = ImageFont.truetype(D + 'fonts/Caveat-Bold.ttf', 78)
                tl = Image.new('RGBA', (260, 120), (0, 0, 0, 0))
                ImageDraw.Draw(tl).text((10, 0), m['label'], font=f, fill=(222, 18, 34, 255))
                tl = tl.rotate(14, resample=Image.BICUBIC, expand=True)
                base.alpha_composite(tl, (int(m['box'][0] - 40), int(m['box'][1] - 120)))
        if m['kind'] == 'arrow':
            (ax, ay), (bx, by) = m['from'], m['to']
            px, py = ax + (bx - ax) * prog, ay + (by - ay) * prog
            ac = tuple(m.get('color', (230, 20, 30, 255))); aw = m.get('w', 24)
            if 'color' not in m: d.line((ax, ay, px, py), fill=(120, 0, 0, 255), width=34)
            d.line((ax, ay, px, py), fill=ac, width=aw)
            if prog >= 1:
                ang = math.atan2(by - ay, bx - ax); L = m.get('head', 70)
                p1 = (bx - L * math.cos(ang - 0.5), by - L * math.sin(ang - 0.5))
                p2 = (bx - L * math.cos(ang + 0.5), by - L * math.sin(ang + 0.5))
                d.polygon([(bx + 10 * math.cos(ang), by + 10 * math.sin(ang)), p1, p2], fill=ac, outline=ac if 'color' in m else (120, 0, 0, 255))

def draw_marks2(base, t):
    for m in sp.get('marks', []):
        if not (m['t0'] <= t < m['t1']): continue
        dt = t - m['t0']
        if m['kind'] == 'rect':
            x0, y0, x1, y1 = m['box']; prog = min(1.0, dt / 0.25)
            lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
            pts = [(x0, y0), (x1, y0 - 3), (x1 + 2, y1), (x0 - 2, y1 + 2), (x0, y0)]
            segs = int(4 * prog * 100); 
            path = []
            for k in range(4):
                if segs <= k * 100: break
                f = min(1.0, (segs - k * 100) / 100)
                a, b = pts[k], pts[k + 1]
                path += [a, (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)]
            if len(path) > 1: dd.line(path, fill=(232, 20, 32, 255), width=11, joint='curve')
            base.alpha_composite(lay)
        if m['kind'] == 'garrow':
            x, y = m['x'], m['y'] + 12 * math.sin(dt * 8); L = m.get('len', 150); u = min(1.0, dt / 0.15); s_ = 0.6 + 0.4 * u
            lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
            P = [(0, 0), (-58, 64), (-23, 64), (-23, L), (23, L), (23, 64), (58, 64)]
            dd.polygon([(x + a * s_, y + b * s_) for a, b in P], fill=(46, 204, 64, 255), outline=(0, 0, 0, 255), width=6)
            base.alpha_composite(lay)
        if m['kind'] == 'emoji':
            sz = m.get('size', 120); an = m.get('anim', 'pop'); x, y = m['x'], m['y']
            u = min(1.0, dt / 0.18); k = 0.5 + 0.5 * u + 0.18 * math.sin(u * math.pi)
            if an == 'tap':
                ph = (dt % 0.55) / 0.55; y += -26 * math.sin(ph * math.pi); k *= 1 - 0.08 * math.sin(ph * math.pi)
            if an == 'tapd':
                ph = (dt % 0.55) / 0.55; y += 22 * math.sin(ph * math.pi)
            if an == 'bob':
                y += 14 * math.sin(dt * 9 + m.get('ph', 0))
            im = EMO[m['name']].resize((max(1, int(sz * k)), max(1, int(sz * k))), Image.LANCZOS)
            if m.get('rot'): im = im.rotate(m['rot'], resample=Image.BICUBIC, expand=True)
            base.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

def outro(t0):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(img)
    return img, d

_RM = sp.get('rmap')
if _RM:
    _X = np.array([a for a, b in _RM], float); _Y = np.array([b for a, b in _RM], float)
    _h = np.diff(_X); _d = np.diff(_Y) / _h; _m = np.zeros_like(_Y)
    for k in range(1, len(_Y) - 1):
        if _d[k - 1] * _d[k] > 0: w1 = 2 * _h[k] + _h[k - 1]; w2 = _h[k] + 2 * _h[k - 1]; _m[k] = (w1 + w2) / (w1 / _d[k - 1] + w2 / _d[k])
    _m[0] = _d[0]; _m[-1] = _d[-1]
def rec_time(t):
    if not _RM: return t
    if sp.get('linear'): return float(np.interp(t, _X, _Y))
    if t <= _X[0]: return _Y[0]
    if t >= _X[-1]: return _Y[-1]
    j = int(np.searchsorted(_X, t)) - 1; h = _h[j]; u = (t - _X[j]) / h
    h00 = 2*u**3 - 3*u**2 + 1; h10 = u**3 - 2*u**2 + u; h01 = -2*u**3 + 3*u**2; h11 = u**3 - u**2
    return h00 * _Y[j] + h10 * h * _m[j] + h01 * _Y[j + 1] + h11 * h * _m[j + 1]
TOT = sp['tot']; OUT_T = sp.get('outro', None)
ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-profile:v', 'high', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
for i in range(int(TOT * FPS)):
    t = i / FPS
    if OUT_T is not None and t >= OUT_T:
        base = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(base)
        u = min(1.0, (t - OUT_T) / 0.6)
        bw = int(760 * (0.3 + 0.7 * u)); bx = W // 2 - bw // 2; by = 1020
        d.rounded_rectangle((bx, by, bx + bw, by + 96), 20, fill=(255, 255, 255, 255), outline=(37, 244, 238, 255), width=6)
        d.rounded_rectangle((bx + 6, by + 6, bx + bw + 6, by + 102), 20, outline=(254, 44, 85, 255), width=4)
        if u >= 1:
            f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 44)
            d.ellipse((bx + 34, by + 26, bx + 72, by + 64), outline=(30, 30, 30), width=5); d.line((bx + 66, by + 60, bx + 80, by + 74), fill=(30, 30, 30), width=6)
            n = int(min(len(sp['handle']), (t - OUT_T - 0.6) / 0.06 + 1))
            d.text((bx + 100, by + 22), sp['handle'][:max(0, n)], font=f, fill=(20, 20, 20))
        ff.stdin.write(np.array(base.convert('RGB')).tobytes()); continue
    r0 = rec_time(t); spd = abs(rec_time(t + 1 / FPS) - r0) * FPS
    if spd > 2.2 and not sp.get('linear'):
        acc = None; n = 3
        for q in range(n):
            rq = rec_time(t + (q - 1) * 0.5 / FPS); f_ = SEQ.get(max(0, int(rq * rfps))).astype(np.float32); acc = f_ if acc is None else acc + f_
        fr = cv2.cvtColor((acc / n).astype(np.uint8), cv2.COLOR_BGR2RGB)
    else:
        fr = cv2.cvtColor(SEQ.get(int(r0 * rfps)), cv2.COLOR_BGR2RGB)
    canvas = np.zeros((H, W, 3), np.uint8); canvas[:, X0:X0 + dw] = fr
    _b = Image.fromarray(canvas).convert('RGBA'); draw_marks(_b, t); draw_marks2(_b, t); canvas = np.array(_b.convert('RGB'))
    z = 1.0 if sp.get('linear') else 1.0 + 0.05 * min(1.0, t / max(1e-3, TOT))
    _zc = None
    for zs in sp.get('zsegs', []):
        if zs[0] <= t < zs[1]:
            e = min(1.0, (t - zs[0]) / 0.22, (zs[1] - t) / 0.22); e = max(0.0, e); e = e * e * (3 - 2 * e)
            z = (z if zs[5] else 1.0) * (1 + (zs[2] - 1) * e) + (0.04 * (t - zs[0]) / max(0.1, zs[1] - zs[0])); _zc = (zs[3], zs[4])
    for hp in sp.get('punches', []):
        x = t - hp
        if -0.05 <= x < 0.35: z += 0.045 * (1 - max(x, 0) / 0.35) ** 2
    if z > 1.0005:
        cx, cy = _zc if _zc else sp.get('cam', [330, 760])
        for _a, _c in sp.get('cams', []):
            if t >= _a: cx, cy = _c
        M = np.float32([[z, 0, cx - z * cx], [0, z, cy - z * cy]])
        canvas = cv2.warpAffine(canvas, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    base = Image.fromarray(canvas).convert('RGBA')
    draw_texts(base, t)
    ff.stdin.write(np.array(base.convert('RGB')).tobytes())
ff.stdin.close(); ff.wait(); print('ok', S, X0, dw, REC_END)
