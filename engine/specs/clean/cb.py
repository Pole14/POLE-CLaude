#!/usr/bin/env python3
"""cb.py [ids] -> <ID>.json + <ID>_base.json (estilo limpio del 120es S2).
6 escenas: gancho / poner código / solicitar / total baja / tarjeta 100% / CTA. Una frase de voz por escena.
Cámara tranquila: zoom máx 1.05, transiciones ≥0.9 s, sin golpes ni sacudidas."""
import json, subprocess, sys
V = '/home/claude/pole-claude/voices/'
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
L = {
 'es': dict(rec='../k120/rec.mp4', fy=476, seo='cupón descuento hacoo noviembre 2026', CIRC=[30, 412, 330, 545], BTN=(860, 474), BTNC=[690, 418, 1034, 532], CARD=[40, 712, 1040, 1058],
            y=dict(cart=820, card=830, ins=830, code=900, tap=900, res=900, cardt=1110, cta=1110)),
 'fr': dict(rec='../r4/rec.mp4', fy=527, seo='code promo hacoo novembre 2026', CIRC=[18, 468, 470, 590], BTN=(850, 523), BTNC=[680, 468, 1034, 580], CARD=[24, 705, 1056, 1045],
            y=dict(card=830, ins=990, code=900, tap=900, res=900, cardt=1100, cta=1100)),
 'en': dict(rec='../en/rec.mp4', fy=575, seo='hacoo discount code november 2026', CIRC=[20, 520, 480, 628], BTN=(888, 572), BTNC=[770, 525, 1010, 620], CARD=[28, 715, 1052, 1010],
            y=dict(card=830, ins=1020, code=930, tap=930, res=930, cardt=1080, cta=1080)),
}
J = json.load(open('cjobs.json')); ids = sys.argv[1:]
for n, j in enumerate(J):
    if ids and j['id'] not in ids: continue
    R = L[j['lang']]; Y = R['y']; lang = j['lang']
    D = [dur(f"{V}c13_{j['id']}_{i}.wav") for i in range(6)]
    mins = [2.3, 2.9, 1.6, 1.9, 1.9, 1.8]; pad = [0.12, 0.05, 0.05, 0.05, 0.05, 0.5]
    Ls = [round(max(m, d + p), 2) for m, d, p in zip(mins, D, pad)]
    S = [0.0]
    for x in Ls: S.append(round(S[-1] + x, 3))
    E = S[1:]; tot = S[-1]
    voice = [[f"c13_{j['id']}_{i}", round(S[i] + (0.1 if i == 0 else 0.0), 3)] for i in range(6)]
    # ---- recording map
    rm = []
    def seg(*pts):
        for t, r in pts: rm.append([round(t, 3), r])
    T2 = S[2] + Ls[2] * 0.62   # momento del toque en "solicitar"
    if lang == 'es':
        seg(*((0, 0.6), (E[0] - 0.02, 2.2)) if j['bg'] == 'cart' else ((0, 12.8), (E[0] - 0.02, 15.5)))
        seg((S[1], 5.0), (S[1] + 0.5, 5.6), (S[1] + 0.8, 6.1), (S[1] + 0.95, 6.75), (E[1] - 0.15, 9.05))
        seg((S[2], 9.06), (S[2] + 0.35, 9.45), (T2 - 0.2, 9.9), (T2, 9.97), (E[2] - 0.02, 10.16))
        seg((S[3], 10.2), (E[3] - 0.02, 11.7))
        seg((S[4], 11.95), (S[4] + 0.6, 12.6), (tot, 16.3))
    elif lang == 'fr':
        seg((0, 10.62), (E[0] - 0.02, 11.9))
        seg((S[1], 3.0), (S[1] + 0.6, 3.88), (E[1] - 0.15, 6.05))
        seg((S[2], 6.06), (S[2] + 0.4, 6.6), (S[2] + 0.42, 8.25), (T2, 8.42), (E[2] - 0.02, 8.62))
        seg((S[3], 9.62), (E[3] - 0.02, 10.09))
        seg((S[4], 10.26), (S[4] + 0.3, 10.55), (tot, 11.6))
    else:
        seg((0, 1.6), (E[0] - 0.02, 3.2))
        seg((S[1], 4.1), (S[1] + 0.45, 4.6), (S[1] + 0.7, 4.85), (S[1] + 0.95, 5.35), (E[1] - 0.15, 7.55))
        seg((S[2], 7.56), (S[2] + 0.45, 8.3), (T2 - 0.15, 8.55), (T2, 8.66), (E[2] - 0.02, 8.92))
        seg((S[3], 8.96), (E[3] - 0.02, 10.7))
        seg((S[4], 10.75), (S[4] + 0.45, 11.2), (tot, 11.9))
    xs = [a for a, _ in rm]; assert all(xs[i + 1] > xs[i] for i in range(len(xs) - 1)), (j['id'], rm)
    # ---- cámara tranquila
    cam = []
    def K(t, z, p=(540, 960), s=None): cam.append({'t': round(t, 3), 'z': z, 'p': list(p), 's': list(s or p)})
    fy = R['fy']; ZF = 1.05
    K(0, 1.0); K(E[0] - 0.03, 1.03)
    K(S[1], 1.0, (0, fy)); K(S[1] + 0.95, ZF, (0, fy)); K(E[2] - 0.03, ZF, (0, fy))
    K(S[3], 1.0); K(E[3] - 0.03, 1.025)
    K(S[4], 1.0); K(tot, 1.04, (540, 880))
    # ---- textos (letra clásica de TikTok, minúsculas)
    sc = j['scenes']; hook = sc[0][1]
    hy = Y['cart'] if (lang == 'es' and j['bg'] == 'cart') else Y['card']
    rows0 = [{'at': -1, 'text': hook[0], 'size': 90}, {'at': -1, 'text': hook[1], 'size': 90}, {'at': 0.3, 'text': hook[2], 'size': 90, 'fx': 'blur'}]
    lines = [{'t1': round(E[0] - 0.02, 3), 'y': hy, 'font': 'classic', 'gap': -0.12, 'rows': rows0},
             {'t1': round(E[2] - 0.02, 3), 'y': Y['tap'], 'font': 'classic', 'rows': [{'at': round(S[2] + 0.1, 3), 'text': sc[2][1][0], 'size': 92}]},
             {'t1': round(E[3] - 0.02, 3), 'y': Y['res'], 'font': 'classic', 'rows': [{'at': round(S[3] + 0.08, 3), 'text': sc[3][1][0], 'size': 92}]},
             {'t1': round(E[4] - 0.02, 3), 'y': Y['cardt'], 'font': 'classic', 'gap': -0.12, 'rows': [{'at': round(S[4] + 0.12, 3), 'text': sc[4][1][0], 'size': 90}, {'at': round(S[4] + 0.12 + D[4] * 0.45, 3), 'text': sc[4][1][1], 'size': 108}]},
             {'t1': tot, 'y': Y['cta'], 'font': 'classic', 'gap': -0.12, 'rows': [{'at': round(S[5] + 0.12, 3), 'text': sc[5][1][0], 'size': 90}, {'at': round(S[5] + 0.12 + D[5] * 0.45, 3), 'text': sc[5][1][1], 'size': 90}]}]
    code = {'t0': round(S[1] + 0.95, 3), 't1': round(E[1] - 0.03, 3), 'y': Y['code'], 'size': 108, 'font': 'classic', 'text': '|emo:gift|120HACOO|emo:gift|', 'tw': round(Ls[1] - 1.35, 2)}
    sp = {'tot': tot, 'off': 150, 'maxw': 960, 'seo': R['seo'], 'seo_y': 150, 'seo_alpha': 0.4, 'rmap': rm, 'cam': cam,
          'punches': [], 'shakes': [], 'blurs': [], 'spots': [] if hy == Y.get('cart') else [{'t0': -0.5, 't1': round(E[0] - 0.02, 3), 'box': [-90, -90, -80, -80], 'dim': 0.38, 'fade': 0.15}], 'lines': lines, 'texts': [code],
          'taps': [{'t': round(T2, 3), 'x': R['BTN'][0], 'y': R['BTN'][1]}],
          'circles': [{'t0': round(S[1] + 1.0, 3), 't1': round(E[1] - 0.05, 3), 'box': R['CIRC'], 'draw': 0.4, 'w': 8},
                      {'t0': round(S[2] + 0.3, 3), 't1': round(E[2] - 0.03, 3), 'box': R['BTNC'], 'draw': 0.3, 'w': 8}],
          'rects': [{'t0': round(S[4] + 0.75, 3), 't1': tot, 'box': R['CARD'], 'draw': 0.45, 'w': 8}],
          'bursts': [{'t': 0.2, 'x': 540, 'y': 1650, 'emo': 'moneyfly', 'n': 6, 'seed': n + 2},
                     {'t': round(S[3] + 0.05, 3), 'x': 860, 'y': 780, 'emo': ['moneyfly', 'gift', 'fire'][n % 3], 'n': 9, 'seed': n + 7}]}
    json.dump(sp, open(f"{j['id']}.json", 'w'), ensure_ascii=False)
    json.dump({'tot': tot, 'voice': voice, 'rec': R['rec'], 'song': j['song']}, open(f"{j['id']}_base.json", 'w'))
    print(j['id'], 'tot', tot, 'escenas', Ls)
