import json
J=json.load(open('cjobs.json'))
FB=['écris ce code dans la case coupon','tape le code que tu vois à l\'écran','colle ce code dans la case coupon']
FC=['et appuie sur appliquer','clique sur appliquer','appuie sur appliquer']
CT=[('enregistre la vidéo pour ta prochaine commande',['enregistre la vidéo','pour plus tard |emo:pin|'],'Enregistre la vidéo'),('envoie-la à quelqu\'un qui commande sur hacoo',['envoie-la à quelqu\'un','qui commande sur hacoo |emo:bag|'],'Envoie-la à quelqu\'un qui commande sur hacoo'),
    ('abonne-toi pour d\'autres codes',['abonne-toi pour','d\'autres codes |emo:gift|'],'Abonne-toi pour d\'autres codes'),('pose ta question en commentaire',['pose ta question','en commentaire |emo:pointdown|'],'Pose ta question en commentaire')]
FV=['Liam','Charlie','Jessica']; FS=['fr4','fr1','fr2','fr5','fr6','fr4','fr5','fr6']
N=[('F09',['code promo hacoo','novembre 2026','(-100% |emo:check|)'],'code promo hacoo de novembre, moins 100%','code promo hacoo novembre 2026 ✅ 120HACOO : -100% jusqu\'à 120 + livraison gratuite.','#codepromohacoo #hacoo #codepromo'),
 ('F10',['ma commande hacoo','à 0,00','(code promo |emo:fire|)'],'ma commande hacoo à zéro, regarde','ma commande hacoo à 0,00 😳 code 120HACOO : -100% jusqu\'à 120 + livraison gratuite.','#hacoo #codepromohacoo #hacco'),
 ('F11',['tuto code promo','hacoo','(jusqu\'à 120 |emo:check|)'],'tuto, code promo hacoo, jusqu\'à 120','tuto code promo hacoo ✅ 120HACOO : -100% sur ma commande, jusqu\'à 120.','#hacoo #codepromo #tuto'),
 ('F12',['tu commandes sur hacoo ?','regarde ça','(-100% |emo:eyes|)'],'tu commandes sur hacoo ? regarde ça','tu commandes sur hacoo ? regarde ça 👀 code 120HACOO : -100% jusqu\'à 120.','#hacoo #codepromohacoo #bonplan'),
 ('F13',['comment utiliser','un code sur hacoo','(tuto |emo:check|)'],'comment utiliser un code sur hacoo','comment utiliser un code promo sur hacoo ✅ 120HACOO : -100% jusqu\'à 120 + livraison gratuite.','#codepromohacoo #hacoo #astuce'),
 ('F14',['code réduction hacoo','novembre','(jusqu\'à 120 |emo:moneyfly|)'],'code réduction hacoo pour novembre, jusqu\'à 120','code réduction hacoo novembre ✅ 120HACOO : -100% sur ma commande, jusqu\'à 120.','#codereduction #hacoo #codepromo'),
 ('F15',['-100% sur hacoo','avec un seul code','(jusqu\'à 120 |emo:fire|)'],'moins 100% sur hacoo, avec un seul code','-100% sur hacoo avec un seul code 😳 120HACOO : jusqu\'à 120 + livraison gratuite.','#hacoo #codepromo #hacco'),
 ('F16',['avant de commander','sur hacoo','(regarde ça |emo:eyes|)'],'avant de commander sur hacoo, regarde ça','avant de commander sur hacoo regarde ça 👀 code 120HACOO : -100% jusqu\'à 120.','#hacoo #codepromohacoo #bonplan')]
for k,(i,hr,hv,cap,tags) in enumerate(N):
    if any(j['id']==i for j in J): continue
    cv,cr,ctxt=CT[k%4]
    sc=[(hv,hr),(FB[k%3],[FB[k%3]]),(FC[k%3],['appuie sur appliquer']),('ma commande passe de 36... à zéro',['de 36,15 à 0,00 |emo:truck|']),('moins 100%, jusqu\'à 120',['-100% de réduction','jusqu\'à 120 |emo:moneyfly|']),(cv,cr)]
    J.append(dict(id=i,lang='fr',voice=FV[k%3],song=FS[k],bg='card',caption=f'{cap} {ctxt} {tags}',comment='code : 120HACOO ✅ (-100% jusqu\'à 120)',scenes=sc))
if not any(j['id']=='S15' for j in J):
    J.append(dict(id='S15',lang='es',voice='Jessica',song='trend3',bg='cart',caption='el cupón de 120 € de hacoo paso a paso ✅ código 120HACOO: 100% de descuento hasta 120 €, de 39,17 € a 3,70 €. Guárdalo para tu próximo pedido #cuponhacoo #hacoo #codigohacoo',
      comment='código: 120HACOO ✅ (hasta 120 € de descuento)',scenes=[('el cupón de 120 euros de hacoo, paso a paso',['el cupón de 120€','de hacoo','(paso a paso |emo:check|)']),('copia este código en el cupón',['copia este código']),('y dale a solicitar',['dale a solicitar']),('de 39 euros... a 3,70',['de 39,17€ a 3,70€']),('100% de descuento, hasta 120 euros',['100% de descuento','hasta 120€ |emo:moneyfly|']),('guárdalo para tu próximo pedido',['guárdalo para tu','próximo pedido |emo:pin|'])]))
json.dump(J,open('cjobs.json','w'),ensure_ascii=False,indent=1); print(len(J))
