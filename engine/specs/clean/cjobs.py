#!/usr/bin/env python3
"""Tanda LIMPIA 13-15 nov (estilo del vídeo 120es S2 que Pol dio por el mejor, 11 nov):
letra clásica de TikTok en minúsculas, gancho visible desde el fotograma 0 (solo la 3ª línea entra desenfocada),
6 frases cortas de voz (una por escena), cámara tranquila (zoom máx 1.08, movimientos lentos), sin golpes de zoom.
Cada escena: (texto voz, filas en pantalla). Escribe cjobs.json."""
import json
G = json.load(open('../g13/jobs.json'))
BASE = {j['id']: j for j in G}

ES_B = ['pon este código en la casilla del cupón', 'escribe este código donde pone cupón', 'copia este código en el cupón']
ES_B_T = ['pon este código', 'escribe este código', 'copia este código']
ES_C = ['y dale a solicitar', 'dale a solicitar', 'y dale a solicitar']
ES_D1 = 'de 39 euros... a 3,70'
ES_D2 = '100% de descuento, hasta 120 euros'
FR_B = ['écris ce code dans la case coupon', 'tape le code que tu vois à l\'écran', 'colle ce code dans la case coupon']
FR_B_T = ['écris ce code', 'tape ce code', 'colle ce code']
FR_C = ['et appuie sur appliquer', 'clique sur appliquer', 'appuie sur appliquer']
FR_D1 = 'ma commande passe de 36... à zéro'
FR_D2 = 'moins 100%, jusqu\'à 120'

# id: (hook filas [l1, l2, l3], hook voz, hook de fondo, cta voz, cta filas, ancla de cámara)
H = {
 'S01': (['cupón de hacoo', 'para noviembre', '(120€ |emo:moneyfly|)'], 'cupón de hacoo para noviembre, de 120 euros', 'cart', 'guárdalo para tu próximo pedido', ['guárdalo para tu', 'próximo pedido |emo:pin|']),
 'S02': (['si compras en hacoo', 'estás pagando de más', '(cupón 120€ |emo:eyes|)'], 'si compras en hacoo, estás pagando de más', 'card', 'envíaselo a quien compra en hacoo', ['envíaselo a quien', 'compra en hacoo |emo:bag|']),
 'S03': (['tutorial cupón hacoo', 'paso a paso', '(120€ |emo:check|)'], 'tutorial, cupón de hacoo de 120 euros, paso a paso', 'cart', 'comenta si te ha funcionado', ['comenta si te', 'ha funcionado |emo:pointdown|']),
 'S04': (['no pagues tu pedido', 'de hacoo todavía', '(cupón 120€ |emo:eyes|)'], 'para, no pagues tu pedido de hacoo todavía', 'card', 'sígueme para más cupones', ['sígueme para', 'más cupones |emo:gift|']),
 'S05': (['mira lo que pasa', 'si pongo esto en hacoo', '(120€ |emo:fire|)'], 'mira lo que pasa si pongo esto en hacoo', 'cart', 'pregunta lo que quieras en comentarios', ['preguntas en', 'comentarios |emo:pointdown|']),
 'S06': (['cómo pagar menos', 'en hacoo', '(cupón 120€ |emo:moneyfly|)'], 'cómo pagar menos en hacoo, con el cupón de 120 euros', 'card', 'guárdalo para tu próximo pedido', ['guárdalo para tu', 'próximo pedido |emo:pin|']),
 'S07': (['de 39€ a 3,70€', 'en hacoo', '(cupón 120€ |emo:fire|)'], 'de 39 euros a 3,70 en hacoo, así', 'cart', 'envíaselo a quien compra en hacoo', ['envíaselo a quien', 'compra en hacoo |emo:bag|']),
 'S08': (['código descuento hacoo', 'noviembre 2026', '(120€ |emo:moneyfly|)'], 'código descuento de hacoo para noviembre, 120 euros', 'card', 'comenta si te ha funcionado', ['comenta si te', 'ha funcionado |emo:pointdown|']),
 'S09': (['antes de pagar en hacoo', 'prueba este cupón', '(120€ |emo:check|)'], 'antes de pagar en hacoo, prueba este cupón', 'cart', 'sígueme para más cupones', ['sígueme para', 'más cupones |emo:gift|']),
 'S10': (['¿hacoo tiene un cupón', 'de 120€?', '(sí, mira |emo:eyes|)'], '¿hacoo tiene un cupón de 120 euros? sí, mira', 'card', 'pregunta lo que quieras en comentarios', ['preguntas en', 'comentarios |emo:pointdown|']),
 'S11': (['así se pone un código', 'en hacoo', '(120€ |emo:check|)'], 'así se pone un código en hacoo', 'cart', 'guárdalo para tu próximo pedido', ['guárdalo para tu', 'próximo pedido |emo:pin|']),
 'S12': (['120€ de descuento', 'en hacoo', '(con un solo código |emo:fire|)'], '120 euros de descuento en hacoo, con un solo código', 'card', 'envíaselo a quien compra en hacoo', ['envíaselo a quien', 'compra en hacoo |emo:bag|']),
 'S13': (['cupón hacco', 'paso a paso', '(120€ |emo:check|)'], 'cupón de hacoo de 120 euros, paso a paso', 'cart', 'comenta si te ha funcionado', ['comenta si te', 'ha funcionado |emo:pointdown|']),
 'S14': (['¿vas a pedir en hacoo?', 'usa antes este cupón', '(120€ |emo:moneyfly|)'], '¿vas a pedir en hacoo? usa antes este cupón', 'card', 'sígueme para más cupones', ['sígueme para', 'más cupones |emo:gift|']),
 'F01': (['comment mettre un', 'code promo sur hacoo', '(jusqu\'à 120 |emo:moneyfly|)'], 'comment mettre un code promo sur hacoo', 'card', 'enregistre la vidéo pour ta prochaine commande', ['enregistre la vidéo', 'pour plus tard |emo:pin|']),
 'F02': (['comment payer', 'moins cher sur hacoo', '(-100% |emo:eyes|)'], 'comment payer moins cher sur hacoo', 'card', 'envoie-la à quelqu\'un qui commande sur hacoo', ['envoie-la à quelqu\'un', 'qui commande sur hacoo |emo:bag|']),
 'F03': (['regarde ce qui se passe', 'quand j\'écris ça sur hacoo', '(-100% |emo:fire|)'], 'regarde ce qui se passe quand j\'écris ça sur hacoo', 'card', 'abonne-toi pour d\'autres codes', ['abonne-toi pour', 'd\'autres codes |emo:gift|']),
 'F04': (['code promo hacoo', '-100% jusqu\'à 120', '(novembre 2026 |emo:check|)'], 'code promo hacoo, moins 100%, jusqu\'à 120', 'card', 'pose ta question en commentaire', ['pose ta question', 'en commentaire |emo:pointdown|']),
 'F05': (['stop, ne paie pas', 'ta commande hacoo', '(pas encore |emo:eyes|)'], 'stop, ne paie pas ta commande hacoo tout de suite', 'card', 'envoie-la à quelqu\'un qui commande sur hacoo', ['envoie-la à quelqu\'un', 'qui commande sur hacoo |emo:bag|']),
 'F06': (['avant de payer sur hacoo', 'essaie ce code', '(jusqu\'à 120 |emo:moneyfly|)'], 'avant de payer sur hacoo, essaie ce code', 'card', 'enregistre la vidéo pour ta prochaine commande', ['enregistre la vidéo', 'pour plus tard |emo:pin|']),
 'F07': (['si tu commandes sur hacoo', 'tu paies trop cher', '(code -100% |emo:eyes|)'], 'si tu commandes sur hacoo, tu paies trop cher', 'card', 'abonne-toi pour d\'autres codes', ['abonne-toi pour', 'd\'autres codes |emo:gift|']),
 'F08': (['code réduction hacoo', '-100% sur ma commande', '(jusqu\'à 120 |emo:check|)'], 'code réduction hacoo, moins 100% sur ma commande', 'card', 'pose ta question en commentaire', ['pose ta question', 'en commentaire |emo:pointdown|']),
 'E01': (['hacoo discount code', 'for november', '(up to 120€ |emo:moneyfly|)'], 'hacoo discount code for november, up to 120 euros off', 'card', 'save this for your next order', ['save this for your', 'next order |emo:pin|']),
}
FRSONG = {'F01': 'fr4', 'F02': 'fr1', 'F03': 'fr2', 'F04': 'fr5', 'F05': 'fr6', 'F06': 'fr5', 'F07': 'fr6', 'F08': 'fr4'}
OUT = []
for n, (id_, (hr, hv, bg, cv, cr)) in enumerate(H.items()):
    b = BASE[id_]; lang = b['lang']; k = n % 3
    if lang == 'es':
        sc = [(hv, hr), (ES_B[k], [ES_B_T[k]]), (ES_C[k], ['dale a solicitar']), (ES_D1, ['de 39,17€ a 3,70€']), (ES_D2, ['100% de descuento', 'hasta 120€ |emo:moneyfly|']), (cv, cr)]
    elif lang == 'fr':
        sc = [(hv, hr), (FR_B[k], [FR_B_T[k]]), (FR_C[k], ['appuie sur appliquer']), (FR_D1, ['de 36,15 à 0,00 |emo:truck|']), (FR_D2, ['-100% de réduction', 'jusqu\'à 120 |emo:moneyfly|']), (cv, cr)]
    else:
        sc = [(hv, hr), ('type this code in the coupon box', ['type this code']), ('and tap apply', ['tap apply']), ('my order goes from 70 euros... to zero', ['70,34€ to 0,00€ |emo:truck|']), ('100% off, up to 120 euros', ['100% off', 'up to 120€ |emo:moneyfly|']), (cv, cr)]
    OUT.append(dict(id=id_, lang=lang, blog=b['blog'], date=b['date'], time=b['time'], voice=b['voice'], bg=bg if lang == 'es' else 'card',
                    song=FRSONG.get(id_, b['song']), caption=b['caption'], comment=b['comment'], scenes=sc))
json.dump(OUT, open('cjobs.json', 'w'), ensure_ascii=False, indent=1)
print(len(OUT), sum(len(s[0]) for j in OUT for s in j['scenes']), 'caracteres')
