# Catálogo de grabaciones (bases) y frases de voz (Martin Osborne) para la fábrica.
BASES = {
 # id: (archivo base, grabación, idioma de la app, shift, tot, fin del gancho, flash POLE14 (t0,t1), inicio texto final)
 'A':   ('A.json',      's06b.mp4', 'fr', 0.0, 10.8, 2.6, (4.85, 5.6), 5.7),
 'FW':  ('FW.json',     'r09b.mp4', 'fr', 0.0, 10.6, 2.6, (4.05, 4.6), 5.0),
 'B':   ('B.json',      's03b.mp4', 'es', 0.8, 10.8, 2.4, (5.02, 5.8), 5.9),
 'C':   ('C.json',      's15b.mp4', 'es', 0.0, 10.6, 2.2, (4.03, 5.4), 6.0),
 'D':   ('D.json',      'r08b.mp4', 'es', 0.0, 10.6, 2.3, (4.11, 4.9), 5.0),
 'Y1':  ('Y1.json',     'r20b.mp4', 'es', 0.0, 10.6, 2.0, (3.82, 5.0), 5.3),
 'X4':  ('X4.json',     'r13b.mp4', 'es', 0.4, 10.8, 2.4, (3.79, 5.0), 5.8),
 'X2':  ('X2.json',     's16b.mp4', 'en', 0.0, 10.8, 2.4, (4.54, 5.6), 5.7),
 'C02': ('c10_02.json', 'r12b.mp4', 'en', 0.0, 10.6, 2.1, (4.0, 4.65), 5.65),
 'C04': ('c10_04.json', 'r19b.mp4', 'en', 0.0, 10.6, 2.3, (4.5, 5.2), 5.3),
 'Z1':  ('Z1.json',     'r14b.mp4', 'de', 0.0, 10.6, 2.0, (3.9, 4.8), 4.9),
 # Código AMG63 (solo @reductionsxhacoo). Grabación de Pol del 7 nov, dirección tapada.
 'AMG1': ('AMG1.json',  'amg1b.mp4', 'fr', 0.0, 11.5, 2.4, (4.6, 5.4), 7.0, 'amg63'),
}
# Bases por código: las que no indican código son de POLE14
CODE_OF = lambda bid: BASES[bid][8] if len(BASES[bid]) > 8 else 'pole14'
# Preferencia de grabación por idioma del vídeo (primero las que tienen la app en ese idioma)
PREF = {'fr': ['A', 'Z1', 'C02', 'B', 'X4', 'C', 'D', 'Y1', 'X2', 'C04', 'FW'],
        'es': ['B', 'C', 'D', 'Y1', 'X4', 'X2', 'C02', 'C04'],
        'en': ['X2', 'C02', 'C04', 'Z1', 'A', 'B']}
# Ganchos: clip de voz -> (líneas formato A [2], líneas formato B [3], flags)
HOOKS = {
 'fr': {
  'n_fr_h0': (["Meilleur code promo Hacoo", "ça marche |emo:check|"], ["Meilleur code", "promo Hacoo", "ça marche |emo:check|"], {}),
  'n_fr_h1': (["Code Hacoo", "réduction en plus |emo:fire|"], ["Code Hacoo", "réduction", "en plus |emo:fire|"], {}),
  'n_fr_h3': (["Code promo Hacoo", "de novembre |emo:check|"], ["Code promo", "Hacoo de", "novembre |emo:check|"], {'month': 11}),
  'n_fr_h4': (["Le code promo Hacoo", "qui marche vraiment |emo:fire|"], ["Le code promo", "Hacoo qui", "marche vraiment |emo:fire|"], {}),
  'n_fr_h5': (["Code promo Hacoo", "avec livraison gratuite |emo:truck|"], ["Code Hacoo", "avec livraison", "gratuite |emo:truck|"], {}),
  'n_fr_h6': (["Code Hacoo", "Black Friday |emo:fire|"], ["Code Hacoo", "pour le", "Black Friday |emo:fire|"], {'from': '11-20', 'to': '12-01'}),
  'n_fr_h7': (["Comment mettre un code", "sur Hacoo |emo:check|"], ["Comment mettre", "un code", "sur Hacoo |emo:check|"], {}),
  'cp_fr_h1': (["L'astuce pour payer", "moins sur Hacoo |emo:shush|"], ["L'astuce pour", "payer moins", "sur Hacoo |emo:shush|"], {}),
  'cp_fr_h3': (["Le code Hacoo", "qui marche cet hiver |emo:snow|"], ["Le code Hacoo", "qui marche", "cet hiver |emo:snow|"], {}),
  'cp_fr_h4': (["Comment payer moins", "sur Hacoo |emo:moneyfly|"], ["Comment payer", "moins sur", "Hacoo |emo:moneyfly|"], {}),
  'cp_fr_h5': (["Code promo Hacoo 2026", "qui marche |emo:check|"], ["Code promo", "Hacoo 2026", "qui marche |emo:check|"], {}),
  'cp_fr_h6': (["Le code Hacoo", "que personne ne donne |emo:shush|"], ["Le code Hacoo", "que personne", "ne te donne |emo:shush|"], {}),
  'cp_fr_h7': (["Ne commande pas sur Hacoo", "sans ce code |emo:eyes|"], ["Ne commande", "pas sur Hacoo", "sans ce code |emo:eyes|"], {}),
  'cp_fr_h8': (["Code Hacoo pour ta", "première commande |emo:gift|"], ["Code Hacoo", "pour ta 1re", "commande |emo:gift|"], {}),
  'cp_fr_t2': (["Tu paies trop sur Hacoo ?", "Regarde ça |emo:eyes|"], ["Tu paies trop", "sur Hacoo ?", "Regarde ça |emo:eyes|"], {}),
  'cp_fr_t5': (["Code Hacoo", "mis à jour 2026 |emo:check|"], ["Code Hacoo", "mis à jour", "2026 |emo:check|"], {}),
  'cp_fr_t8': (["-14% sur Hacoo", "en 10 secondes |emo:fire|"], ["-14% sur", "Hacoo en", "10 secondes |emo:fire|"], {}),
  'cp_fr_t9': (["Le code secret", "de Hacoo |emo:shush|"], ["Le code", "secret", "de Hacoo |emo:shush|"], {}),
  'cp_fr_t11': (["Tu commandes sur Hacoo ?", "Il te faut ça |emo:eyes|"], ["Tu commandes", "sur Hacoo ?", "Il te faut ça |emo:eyes|"], {}),
  'cp_fr_t13': (["Ton haul Hacoo moins cher", "avec ce code |emo:moneyfly|"], ["Ton haul Hacoo", "moins cher", "avec ce code |emo:moneyfly|"], {}),
 },
 'es': {
  'cp_es_h1': (["Truco para no pagar", "tanto en Hacoo |emo:moneyfly|"], ["Truco para no", "pagar tanto", "en Hacoo |emo:moneyfly|"], {}),
  'cp_es_h3': (["El código de Hacoo", "que funciona este invierno |emo:snow|"], ["El código Hacoo", "que funciona", "este invierno |emo:snow|"], {}),
  'cp_es_h4': (["¿Cómo pagar menos", "en Hacoo? |emo:eyes|"], ["¿Cómo pagar", "menos en", "Hacoo? |emo:eyes|"], {}),
  'cp_es_h5': (["Cupón Hacoo 2026", "que sí funciona |emo:check|"], ["Cupón Hacoo", "2026 que", "sí funciona |emo:check|"], {}),
  'cp_es_h6': (["El código de Hacoo", "que nadie te cuenta |emo:shush|"], ["El código de", "Hacoo que nadie", "te cuenta |emo:shush|"], {}),
  'cp_es_h7': (["Así compro en Hacoo", "más barato |emo:moneyfly|"], ["Así compro", "en Hacoo", "más barato |emo:moneyfly|"], {}),
  'cp_es_h8': (["Código Hacoo para", "tu primer pedido |emo:gift|"], ["Código Hacoo", "para tu primer", "pedido |emo:gift|"], {}),
  'cp_es_h9': (["No compres en Hacoo", "sin este código |emo:eyes|"], ["No compres", "en Hacoo sin", "este código |emo:eyes|"], {}),
  'cp_es_h2': (["Código Hacoo", "Black Friday 2026 |emo:fire|"], ["Código Hacoo", "para el", "Black Friday |emo:fire|"], {'from': '11-20', 'to': '12-01'}),
  'cp_es_t2': (["¿Pagas de más en Hacoo?", "Mira esto |emo:eyes|"], ["¿Pagas de más", "en Hacoo?", "Mira esto |emo:eyes|"], {}),
  'cp_es_t9': (["El código secreto", "de Hacoo |emo:shush|"], ["El código", "secreto", "de Hacoo |emo:shush|"], {}),
  'cp_es_t11': (["¿Compras en Hacoo?", "Necesitas esto |emo:eyes|"], ["¿Compras", "en Hacoo?", "Necesitas esto |emo:eyes|"], {}),
  'cp_es_t12': (["Cupones de Hacoo", "que funcionan |emo:check|"], ["Cupones de", "Hacoo que", "funcionan |emo:check|"], {}),
  'n_es_h0': (["Mejor cupón de Hacoo", "funciona |emo:fire|"], ["Mejor cupón", "de Hacoo", "funciona |emo:fire|"], {}),
  'n_es_h1': (["Cupón Hacoo", "descuento extra |emo:moneyfly|"], ["Cupón Hacoo", "con descuento", "extra |emo:moneyfly|"], {}),
  'n_es_h3': (["Hacoo", "cupón de noviembre |emo:check|"], ["Cupón de", "Hacoo de", "noviembre |emo:check|"], {'month': 11}),
  'n_es_h4': (["El cupón de Hacoo", "que sí funciona |emo:check|"], ["El cupón", "de Hacoo que", "sí funciona |emo:check|"], {}),
  'n_es_h7': (["Así se pone un cupón", "en Hacoo |emo:check|"], ["Así se pone", "un cupón", "en Hacoo |emo:check|"], {}),
 },
 'en': {
  'cp_en_h1': (["How to stop overpaying", "on Hacoo |emo:moneyfly|"], ["How to stop", "overpaying", "on Hacoo |emo:moneyfly|"], {}),
  'cp_en_h3': (["The Hacoo code that", "works this winter |emo:snow|"], ["The Hacoo code", "that works", "this winter |emo:snow|"], {}),
  'cp_en_h4': (["How to pay less", "on Hacoo |emo:moneyfly|"], ["How to", "pay less", "on Hacoo |emo:moneyfly|"], {}),
  'cp_en_h6': (["The Hacoo code", "nobody tells you about |emo:shush|"], ["The Hacoo code", "nobody tells", "you about |emo:shush|"], {}),
  'cp_en_h7': (["Don't order on Hacoo", "without this code |emo:eyes|"], ["Don't order", "on Hacoo without", "this code |emo:eyes|"], {}),
  'cp_en_h8': (["Hacoo code for", "your first order |emo:gift|"], ["Hacoo code", "for your", "first order |emo:gift|"], {}),
  'cp_en_h2': (["Hacoo code", "Black Friday 2026 |emo:fire|"], ["Hacoo code", "for", "Black Friday |emo:fire|"], {'from': '11-20', 'to': '12-01'}),
 },
}
CODE = {'fr': ['n_fr_c1'], 'es': ['n_es_c0', 'n_es_c1'], 'en': ['cp_en_code']}
CODE_AMG = {'fr': ['amg_fr_c1', 'amg_fr_c2']}
CODE_TXT = {'pole14': 'POLE14', 'amg63': 'AMG63'}
OFF_EN = 'cp_en_off'
ENDS = {'fr': ['n_fr_e0', 'n_fr_e1', 'n_fr_e2', 'n_fr_e3', 'cp_fr_e2', 'cp_fr_e3', 'cp_fr_e4', 'cp_fr_xe0', 'cp_fr_xe3'],
        'es': ['n_es_e0', 'n_es_e1', 'n_es_e2', 'n_es_e3', 'cp_es_e1', 'cp_es_e2', 'cp_es_e3', 'cp_es_e5', 'cp_es_xe0'],
        'en': ['cp_en_e0', 'cp_en_e1', 'cp_en_e2', 'cp_en_e3', 'cp_en_e4']}
END_TXT = {'fr': [["14% de réduction", "+ livraison gratuite |emo:truck|"], ["-14% sur tout", "+ livraison offerte |emo:fire|"], ["-14% de réduction", "+ livraison gratuite |emo:check|"]],
           'es': [["14% de descuento", "+ envío gratis |emo:truck|"], ["-14% en todo", "+ envío gratis |emo:check|"]],
           'en': [["14% off", "+ free delivery |emo:truck|"], ["14% off everything", "+ free delivery |emo:check|"]]}
SONGS = ['ninao', 'coqueta', 'lolita', 'parisienne', 'free', 'arrochadeira', 'es666', 'gone']
CAPTION = {'fr': "POLE14 = -14% (jusqu'à 14 €) + livraison gratuite #hacoo #codepromohacoo #hacco #codereduction",
           'es': "POLE14 = 14% de descuento (hasta 14 €) + envío gratis #hacoo #cuponhacoo #codigohacoo #hacco",
           'en': "POLE14 = 14% off (up to €14) + free delivery #hacoo #hacoocode #discountcode #hacco"}
EMOJI = {'fire': '🔥', 'check': '✅', 'truck': '🚚', 'moneyfly': '💸', 'shush': '🤫', 'eyes': '👀', 'gift': '🎁', 'snow': '❄️'}
