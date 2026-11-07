#!/usr/bin/env python3
"""Fábrica de vídeos checkout Hacoo (POLE14).

Uso:
  python3 factory.py --lang fr --fmt B --n 4 [--date 2026-11-12]
Genera N vídeos nuevos en out/ (mp4 + json con la descripción) sin repetir
combinaciones ya usadas (used.json). Formato A = gancho pequeño de 2 líneas
(copia del vídeo de 2,5k); B = gancho grande de 3 líneas en el centro.
"""
import argparse, datetime, json, os, re, subprocess, sys
from PIL import ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, ROOT)
from bank import BASES, PREF, HOOKS, CODE, OFF_EN, ENDS, END_TXT, SONGS, CAPTION, EMOJI

DUR = {k: v[0] for k, v in json.load(open(ROOT + 'voices/clip_texts.json')).items()}
USED_F = ROOT + 'used.json'


def load_used():
    return json.load(open(USED_F)) if os.path.exists(USED_F) else {'keys': [], 'log': []}


def tk(t0, t1, y, size, lines):
    return {"t0": round(t0, 2), "t1": round(t1, 2), "y": y, "style": "tk", "size": size, "lines": lines}


def width(line, sz):
    f = ImageFont.truetype(ROOT + 'fonts/tmp_w500_latin.ttf', sz)
    n = len(re.findall(r'\|emo:\w+\|', line)); txt = re.sub(r'\|emo:\w+\|', '', line).strip()
    return f.getlength(txt) + n * sz * 1.15 + sz * 0.7


def fit(lines, hi, maxw=840):
    s = hi
    while s > 50 and max(width(l, s) for l in lines) > maxw:
        s -= 2
    return s


def interp(rm, t):
    for i in range(len(rm) - 1):
        a, b = rm[i], rm[i + 1]
        if a[0] <= t <= b[0]:
            u = 0 if b[0] == a[0] else (t - a[0]) / (b[0] - a[0])
            return a[1] + (b[1] - a[1]) * u
    return rm[-1][1]


def build(bid, fmt, lang, hook, code, end, end_txt):
    bfile, rec, ui, shift, tot0, hook_end, flash, end_t0 = BASES[bid]
    base = json.load(open(ROOT + 'bases/' + bfile))
    rm = [list(p) for p in base['rmap']]
    if shift:
        rm = [[0, rm[0][1]]] + [[t + shift, r] for t, r in rm]
    # voces
    hA, hB, _ = HOOKS[lang][hook]
    voice = [[hook, 0.1]]
    t_code = max(hook_end + 0.1, 0.1 + DUR[hook] + 0.25)
    voice.append([code, round(t_code, 2)])
    t = t_code + DUR[code]
    if lang == 'en':
        t_off = max(end_t0 + 0.2, t + 0.3)
        voice.append([OFF_EN, round(t_off, 2)]); t = t_off + DUR[OFF_EN]
    t_end = max(t + 0.5, 7.0)
    voice.append([end, round(t_end, 2)])
    tot = round(max(tot0, t_end + DUR[end] + 0.6), 2)
    # rmap recortado / alargado (congela el último fotograma)
    if rm[-1][0] < tot:
        rm.append([tot, rm[-1][1]])
    cut = [p for p in rm if p[0] <= tot]
    if cut[-1][0] < tot:
        cut.append([tot, interp(rm, tot)])
    marks = []
    for m in base['marks']:
        if m['kind'] == 'emoji':
            continue
        m = dict(m, t0=m['t0'] + shift, t1=min(m['t1'] + shift, tot))
        if m['t1'] >= tot0 - 0.05:
            m['t1'] = tot
        if m['t0'] < tot and m['t1'] > hook_end + 0.05:
            marks.append(m)
    if fmt == 'A':
        sz = fit(hA, 64, 900); hook_txt = tk(0, hook_end, 800, sz, hA); tile_y = 550
    else:
        sz = fit(hB, 108); hook_txt = tk(0, hook_end, 930, sz, hB); tile_y = 930 - int(1.62 * sz) - 95
    marks.append({"kind": "emoji", "t0": 0.0, "t1": hook_end, "name": "hacoo", "x": 540, "y": tile_y, "size": 190 if fmt == 'A' else 180})
    texts = [hook_txt, tk(flash[0], flash[1], 1000, 100, ["POLE14"]), tk(end_t0, tot, 520, 64, end_txt)]
    return rec, {"tot": tot, "handle": "", "linear": True, "rmap": cut, "texts": texts, "marks": marks, "voice": voice}


def caption(lang, hook):
    a = HOOKS[lang][hook][0]
    s = ' '.join(a)
    emo = re.findall(r'\|emo:(\w+)\|', s)
    s = re.sub(r'\s*\|emo:\w+\|', '', s).strip().lower()
    return f"{s} {''.join(EMOJI.get(e, '') for e in emo)} {CAPTION[lang]}".replace('  ', ' ')


def hook_ok(flags, day):
    md = day.strftime('%m-%d')
    if 'month' in flags and day.month != flags['month']:
        return False
    if 'from' in flags and md < flags['from']:
        return False
    if 'to' in flags and md > flags['to']:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', required=True, choices=['fr', 'es', 'en'])
    ap.add_argument('--fmt', default='A', choices=['A', 'B'])
    ap.add_argument('--n', type=int, default=1)
    ap.add_argument('--date', default=None, help='fecha de publicación prevista (para ganchos de temporada)')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    day = datetime.date.fromisoformat(a.date) if a.date else datetime.date.today()
    used = load_used(); keys = set(used['keys'])
    hook_count = {}
    for k in used['keys']:
        h = k.split('|')[1]; hook_count[h] = hook_count.get(h, 0) + 1
    base_count = {}
    for k in used['keys']:
        b = k.split('|')[0]; base_count[b] = base_count.get(b, 0) + 1
    hooks = [h for h, v in HOOKS[a.lang].items() if hook_ok(v[2], day) and DUR.get(h, 9) <= 3.0]
    made = []
    n_log = len(used['log'])
    for i in range(a.n):
        best = None
        for bid in PREF[a.lang]:
            for h in hooks:
                k = f"{bid}|{h}|{a.fmt}"
                if k in keys:
                    continue
                score = hook_count.get(h, 0) * 3 + base_count.get(bid, 0) + PREF[a.lang].index(bid) * 0.3
                if best is None or score < best[0]:
                    best = (score, bid, h, k)
        if not best:
            print('sin combinaciones nuevas', file=sys.stderr); break
        _, bid, h, k = best
        j = n_log + i
        code = CODE[a.lang][j % len(CODE[a.lang])]
        end = ENDS[a.lang][j % len(ENDS[a.lang])]
        etxt = END_TXT[a.lang][j % len(END_TXT[a.lang])]
        song = SONGS[j % len(SONGS)]
        rec, spec = build(bid, a.fmt, a.lang, h, code, end, etxt)
        name = f"{day.isoformat()}_{a.lang}_{a.fmt}_{bid}_{h}{a.tag}"
        os.makedirs(ROOT + 'out', exist_ok=True)
        sp = ROOT + f'out/{name}.json'; json.dump(spec, open(sp, 'w'))
        v = ROOT + f'out/{name}_v.mp4'; o = ROOT + f'out/{name}.mp4'
        subprocess.run([sys.executable, ROOT + 'engine/native7.py', ROOT + 'recs/' + rec, sp, v], check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, ROOT + 'engine/mux3.py', v, sp, o, ROOT + f'music/{song}.mp3', '0'], check=True, stdout=subprocess.DEVNULL)
        os.remove(v)
        meta = {'file': f'out/{name}.mp4', 'lang': a.lang, 'fmt': a.fmt, 'base': bid, 'hook': h, 'song': song,
                'caption': caption(a.lang, h), 'tot': spec['tot'], 'made': datetime.datetime.now().isoformat(timespec='seconds')}
        json.dump(meta, open(ROOT + f'out/{name}.meta.json', 'w'), ensure_ascii=False, indent=1)
        keys.add(k); used['keys'].append(k); used['log'].append(meta)
        hook_count[h] = hook_count.get(h, 0) + 1; base_count[bid] = base_count.get(bid, 0) + 1
        made.append(meta)
        json.dump(used, open(USED_F, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(made, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
