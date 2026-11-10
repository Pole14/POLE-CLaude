# Tanda 13-15 nov: 14 ES + 8 FR + 1 EN. Un gancho distinto por vídeo (test de ganchos).
import json
ACC={'R':'7905293','N':'7802274','H':'7801775','C':'7690746','X':'7992090','FR':'7841739','FC':'7801996','FD':'7968754'}
ES_I={1:("Escribe el código de la pantalla en la casilla del cupón... dale a solicitar... y mira el total.",'escribe','mira','MIRA EL TOTAL |emo:eyes|'),
      2:("Copia el código que ves en pantalla y pégalo en el cupón... dale a solicitar... y listo.",'copia','listo','Y LISTO |emo:check|'),
      3:("Pon el código de la pantalla donde dice cupón... dale a solicitar... y fíjate en el precio.",'pon','fíjate','FÍJATE EN EL PRECIO |emo:eyes|'),
      4:("Teclea el código de la pantalla en el cupón... dale a solicitar... y ahí lo tienes.",'teclea','ahí','AHÍ LO TIENES |emo:check|'),
      5:("Mete el código de la pantalla en la casilla... dale a solicitar... y mira lo que pasa.",'mete','mira','MIRA LO QUE PASA |emo:eyes|')}
ES_C={1:("Cien por cien de descuento, hasta ciento veinte euros.",['hasta']),2:("Te descuenta el cien por cien, hasta ciento veinte euros.",['hasta']),3:("Es un cupón del cien por cien, con tope de ciento veinte euros.",['tope','con'])}
ES_P={1:("Mi pedido pasa de treinta y nueve euros... a tres con setenta.",['mi'],['MI PEDIDO PASA DE 39€...','A 3,70€']),
      2:("De treinta y nueve euros... me quedo en tres con setenta, que es el envío.",['de'],['DE 39€...','A 3,70€ (EL ENVÍO)']),
      3:("Treinta y nueve euros... que se quedan en tres con setenta.",['treinta','39'],['39 EUROS...','SE QUEDAN EN 3,70€']),
      4:("Solo pago el envío: de treinta y nueve euros... a tres con setenta.",['solo','sólo'],['SOLO PAGO EL ENVÍO','DE 39€ A 3,70€'])}
ES_T={1:("Guárdalo para tu próximo pedido.",['guárdalo','guardalo','guárdelo'],['GUÁRDALO PARA','TU PRÓXIMO PEDIDO |emo:pin|']),
      2:("Envíaselo a quien compra en Hacoo.",['envíaselo','enviáselo','envíasela'],['ENVÍASELO A QUIEN','COMPRA EN HACOO |emo:bag|']),
      3:("Sígueme para más cupones de Hacoo.",['sígueme','sigueme'],['SÍGUEME PARA','MÁS CUPONES |emo:gift|']),
      4:("Comenta si te ha funcionado.",['comenta'],['COMENTA SI TE','HA FUNCIONADO |emo:pointdown|']),
      5:("Pregunta lo que quieras en comentarios.",['pregunta'],['PREGUNTA LO QUE QUIERAS','EN COMENTARIOS |emo:pointdown|'])}
# id, cuenta, fecha, hora, voz, gancho (voz), líneas del gancho, ancla de la cifra, variante, marca, final, canción, I,C,P,T, descripción
ES=[
('S01','R','2026-11-13','17:38','Liam',"Cupón de Hacoo para noviembre: ciento veinte euros.",['CUPÓN DE HACOO','PARA NOVIEMBRE','(120€ |emo:moneyfly|)'],['ciento','120'],'cart','circle','total','gone',1,1,1,1,
 "cupón de hacoo para noviembre ✅ código 120HACOO: 100% de descuento hasta 120 €, de 39,17 € a 3,70 €. Guárdalo para tu próximo pedido #cuponhacoo #hacoo #codigohacoo"),
('S02','N','2026-11-13','18:04','Jessica',"Si compras en Hacoo, estás pagando de más.",['SI COMPRAS EN HACOO','ESTÁS PAGANDO DE MÁS','(CUPÓN 120€ |emo:moneyfly|)'],None,'drop','rect','card','trend2',3,2,2,2,
 "si compras en hacoo estás pagando de más 👀 cupón 120HACOO: 100% de descuento hasta 120 €. Envíaselo a quien compra en hacoo #hacoo #cuponhacoo #codigodescuento"),
('S03','H','2026-11-13','18:29','Charlie',"Tutorial: cómo usar el cupón de ciento veinte euros de Hacoo.",['TUTORIAL CUPÓN HACOO','PASO A PASO','(120€ |emo:check|)'],['ciento','120'],'check','circle','total','trend4',2,1,3,4,
 "tutorial cupón hacoo paso a paso ✅ código 120HACOO: hasta 120 € de descuento, de 39,17 € a 3,70 €. Comenta si te ha funcionado #hacooespaña #cuponhacoo #tutorial"),
('S04','C','2026-11-13','18:53','Will',"Para. No pagues tu pedido de Hacoo todavía.",['NO PAGUES EN HACOO','TODAVÍA |emo:eyes|','(CUPÓN 120€ |emo:check|)'],None,'zoomout','rect','total','trend1',5,3,4,3,
 "no pagues tu pedido de hacoo todavía 👀 código descuento 120HACOO: 100% hasta 120 €, solo pagas el envío. Sígueme para más cupones #hacoo #codigohacoo #cuponhacoo"),
('S05','X','2026-11-13','19:16','Chris',"Mira lo que pasa cuando escribo esto en Hacoo.",['MIRA LO QUE PASA','SI ESCRIBO ESTO EN HACOO','(120€ |emo:eyes|)'],None,'card','circle','total','trend3',4,1,1,5,
 "mira lo que pasa con este cupón de hacoo 👀 120HACOO: 100% de descuento hasta 120 €, de 39,17 € a 3,70 €. Pregunta lo que quieras en comentarios #cuponhacoo #hacoo #codigodescuento"),
('S06','N','2026-11-14','17:49','Charlie',"Cómo pagar menos en Hacoo: cupón de ciento veinte euros.",['CÓMO PAGAR MENOS','EN HACOO','(CUPÓN 120€ |emo:moneyfly|)'],['ciento','120'],'cart','rect','card','trend5',1,2,3,1,
 "cómo pagar menos en hacoo ✅ cupón 120HACOO: 100% de descuento hasta 120 €. Guárdalo para tu próximo pedido #hacoo #cuponhacoo #ahorrar"),
('S07','H','2026-11-14','18:12','Liam',"De treinta y nueve euros a tres con setenta en Hacoo. Así.",['MI PEDIDO DE HACOO','DE 39,17€ A 3,70€','(CUPÓN 120€ |emo:check|)'],None,'drop','circle','total','gone',3,1,4,2,
 "de 39,17 € a 3,70 € en hacoo 😳 cupón 120HACOO: 100% de descuento hasta 120 €. Envíaselo a quien compra en hacoo #cuponhacoo #hacoo #hacco"),
('S08','C','2026-11-14','18:37','Jessica',"Código descuento de Hacoo para noviembre: ciento veinte euros.",['CÓDIGO DESCUENTO HACOO','NOVIEMBRE 2026','(120€ |emo:gift|)'],['ciento','120'],'check','rect','total','trend2',4,3,1,4,
 "código descuento hacoo noviembre 2026 ✅ 120HACOO: 100% hasta 120 €, de 39,17 € a 3,70 €. Comenta si te ha funcionado #codigodescuento #hacoo #codigohacoo"),
('S09','X','2026-11-14','19:03','Will',"Antes de pagar en Hacoo, prueba este cupón.",['ANTES DE PAGAR','EN HACOO, PRUEBA ESTO','(CUPÓN 120€ |emo:moneyfly|)'],None,'zoomout','circle','card','trend4',2,1,2,3,
 "antes de pagar en hacoo prueba este cupón ✅ 120HACOO: 100% de descuento hasta 120 €, solo pagas el envío. Sígueme para más cupones #hacoo #cuponhacoo #codigohacoo"),
('S10','R','2026-11-15','17:44','Chris',"¿Hacoo tiene un cupón de ciento veinte euros? Sí, mira.",['¿CUPÓN DE HACOO','DE 120 EUROS?','(SÍ, MIRA |emo:eyes|)'],None,'card','rect','total','trend1',5,2,1,5,
 "¿hacoo tiene un cupón de 120 €? sí ✅ código 120HACOO: 100% de descuento hasta 120 €. Pregunta lo que quieras en comentarios #hacoo #cuponhacoo #codigodescuento"),
('S11','N','2026-11-15','18:08','Will',"Así se pone un código en Hacoo, en diez segundos.",['CÓMO PONER UN CÓDIGO','EN HACOO','(CUPÓN 120€ |emo:check|)'],None,'check','circle','card','trend3',1,3,3,1,
 "cómo poner un código en hacoo ✅ cupón 120HACOO: 100% de descuento hasta 120 €, de 39,17 € a 3,70 €. Guárdalo para tu próximo pedido #codigohacoo #hacoo #tutorial"),
('S12','H','2026-11-15','18:33','Jessica',"Ciento veinte euros de descuento en Hacoo con un solo código.",['DESCUENTO EN HACOO','CON UN SOLO CÓDIGO','(120€ |emo:moneyfly|)'],['ciento','120'],'drop','rect','total','trend5',3,1,2,2,
 "120 € de descuento en hacoo con un solo código 😳 120HACOO: 100% hasta 120 €, solo pagas el envío. Envíaselo a quien compra en hacoo #hacoo #cuponhacoo #descuento"),
('S13','C','2026-11-15','18:57','Liam',"Cupón de Hacoo de ciento veinte euros, paso a paso.",['CUPÓN HACCO','PASO A PASO','(120€ |emo:gift|)'],['ciento','120'],'cart','circle','total','gone',4,2,4,4,
 "cupón hacco paso a paso ✅ código 120HACOO en hacoo: 100% de descuento hasta 120 €. Comenta si te ha funcionado #hacco #hacoo #cuponhacoo"),
('S14','X','2026-11-15','19:21','Charlie',"¿Vas a hacer un pedido en Hacoo? Usa antes este cupón.",['¿VAS A PEDIR EN HACOO?','USA ANTES ESTE CUPÓN','(120€ |emo:moneyfly|)'],None,'zoomout','rect','total','trend2',2,3,1,3,
 "¿vas a pedir en hacoo? usa antes este cupón ✅ 120HACOO: 100% de descuento hasta 120 €, de 39,17 € a 3,70 €. Sígueme para más cupones #hacoo #cuponhacoo #codigohacoo"),
]
FR_I={1:("Écris le code affiché à l'écran dans la case coupon... appuie sur appliquer... et regarde le total.",['écris','ecris'],['appuie'],['regarde'],'REGARDE LE TOTAL |emo:eyes|',['APPUIE SUR','APPLIQUER']),
      2:("Copie le code de l'écran et colle-le dans coupon... clique sur appliquer... et voilà.",['copie','copy'],['clique'],['voilà','voila'],'ET VOILÀ |emo:check|',['CLIQUE SUR','APPLIQUER']),
      3:("Tape le code que tu vois à l'écran... appuie sur le bouton rouge... et regarde le prix.",['tape','tap'],['appuie'],['regarde'],'REGARDE LE PRIX |emo:eyes|',['APPUIE SUR','LE BOUTON ROUGE']),
      4:("Mets le code de l'écran dans la case du coupon... clique sur appliquer... et c'est fait.",['mets','met','mais'],['clique'],["c'est",'cest','fait'],"C'EST FAIT |emo:check|",['CLIQUE SUR','APPLIQUER'])}
FR_C={1:"Cent pour cent de réduction, jusqu'à cent vingt.",2:"Moins cent pour cent sur la commande, jusqu'à cent vingt."}
FR_P={1:("Ma commande passe de trente-six... à zéro.",['ma'],['MA COMMANDE PASSE DE 36,15...','À 0,00']),
      2:("Trente-six au départ... et zéro à payer, livraison incluse.",['trente','36','trente-six'],['36,15 AU DÉPART...','0,00 À PAYER']),
      3:("Avec la livraison gratuite : de trente-six... à zéro.",['avec'],['LIVRAISON GRATUITE','DE 36,15 À 0,00'])}
FR_T={1:("Enregistre la vidéo pour ta prochaine commande.",['enregistre'],['ENREGISTRE LA VIDÉO','POUR TA COMMANDE |emo:pin|']),
      2:("Envoie-la à quelqu'un qui commande sur Hacoo.",['envoie','envoie-la','envoi'],['ENVOIE-LA À QUELQU\'UN','QUI COMMANDE SUR HACOO |emo:bag|']),
      3:("Abonne-toi pour d'autres codes Hacoo.",['abonne','abonne-toi'],['ABONNE-TOI POUR','D\'AUTRES CODES |emo:gift|']),
      4:("Pose ta question en commentaire.",['pose'],['POSE TA QUESTION','EN COMMENTAIRE |emo:pointdown|'])}
FR=[
('F01','FC','2026-11-13','09:23','Charlie',"Tuto : comment mettre un code promo sur Hacoo.",['COMMENT METTRE','UN CODE PROMO SUR HACOO','(TUTO |emo:check|)'],None,'check','circle','total','trend1',1,1,1,1,
 "comment mettre un code promo sur hacoo ✅ code 120HACOO : -100% sur ma commande, jusqu'à 120 + livraison gratuite. Enregistre la vidéo #codepromohacoo #hacoo #tuto"),
('F02','FD','2026-11-13','09:49','Liam',"Comment payer moins cher sur Hacoo.",['COMMENT PAYER','MOINS CHER SUR HACOO','(JUSQU\'À 120 |emo:moneyfly|)'],None,'card','rect','total','trend4',3,2,2,2,
 "comment payer moins cher sur hacoo 👀 code promo 120HACOO : -100% jusqu'à 120 + livraison gratuite. Envoie-la à quelqu'un qui commande sur hacoo #hacoo #codepromo #bonplan"),
('F03','FD','2026-11-14','08:26','Jessica',"Regarde ce qui se passe quand j'écris ça sur Hacoo.",['REGARDE CE QUI SE PASSE','QUAND J\'ÉCRIS ÇA SUR HACOO','(JUSQU\'À 120 |emo:eyes|)'],None,'drop','circle','card','trend2',2,1,3,3,
 "regarde ce code promo hacoo 👀 120HACOO : -100% sur ma commande, jusqu'à 120 + livraison gratuite. Abonne-toi pour d'autres codes #hacoo #codepromohacoo #hacco"),
('F04','FR','2026-11-14','08:52','Charlie',"Code promo Hacoo de novembre : jusqu'à cent vingt.",['CODE PROMO HACOO','NOVEMBRE 2026','(JUSQU\'À 120 |emo:moneyfly|)'],['cent','120'],'zoomout','rect','total','gone',4,2,1,4,
 "code promo hacoo novembre 2026 ✅ 120HACOO : -100% sur ma commande, jusqu'à 120 + livraison gratuite. Pose ta question en commentaire #codepromohacoo #hacoo #codereduction"),
('F05','FC','2026-11-14','09:34','Liam',"Stop. Ne paie pas ta commande Hacoo tout de suite.",['NE PAIE PAS','TA COMMANDE HACOO','(PAS ENCORE |emo:eyes|)'],None,'card','circle','total','trend5',1,1,2,2,
 "ne paie pas ta commande hacoo tout de suite 👀 code réduction 120HACOO : -100% jusqu'à 120 + livraison gratuite. Envoie-la à quelqu'un qui commande sur hacoo #hacoo #codereduction #codepromo"),
('F06','FC','2026-11-15','08:41','Jessica',"Avant de payer sur Hacoo, essaie ce code.",['AVANT DE PAYER','SUR HACOO, ESSAIE ÇA','(JUSQU\'À 120 |emo:gift|)'],None,'check','rect','card','trend3',3,2,1,1,
 "avant de payer sur hacoo essaie ce code promo ✅ 120HACOO : -100% jusqu'à 120 + livraison gratuite. Enregistre la vidéo #hacoo #codepromohacoo #astuce"),
('F07','FD','2026-11-15','09:07','Charlie',"Si tu commandes sur Hacoo, tu paies trop cher.",['SI TU COMMANDES SUR HACOO','TU PAIES TROP CHER','(JUSQU\'À 120 |emo:moneyfly|)'],None,'drop','circle','total','trend1',2,1,3,3,
 "si tu commandes sur hacoo tu paies trop cher 👀 code promo 120HACOO : -100% sur ma commande, jusqu'à 120. Abonne-toi pour d'autres codes #hacoo #codepromo #bonplan"),
('F08','FR','2026-11-15','09:53','Liam',"Code réduction Hacoo : moins cent pour cent sur ma commande.",['CODE RÉDUCTION HACOO','SUR MA COMMANDE','(-100% |emo:check|)'],['cent','100','100%','moins'],'zoomout','rect','total','trend2',4,2,1,4,
 "code réduction hacoo ✅ 120HACOO : -100% sur ma commande, jusqu'à 120 + livraison gratuite. Pose ta question en commentaire #codereduction #hacoo #codepromohacoo"),
]
jobs=[]
for (i,a,d,tm_,v,hk,hl,amt,hv,mk,en,sg,I,C,P,T,cap) in ES:
    it,hw,rw,rtx=ES_I[I]; ct,ha=ES_C[C]; pt,qa,ql=ES_P[P]; tt,ta,tl=ES_T[T]
    jobs.append(dict(id=i,lang='es',blog=ACC[a],date=d,time=tm_,voice=v,script=' '.join([hk,it,ct,pt,tt]),
      anchors=dict(amt=amt,h=[hw],ap=['dale'],rev=[rw],s100=['cien','100','100%'],hasta=ha,q1=qa,drop=['tres','3','3,70','370','3.70'],cta=ta),
      rows=dict(hook=hl,tap=['DALE A SOLICITAR'],rev=rtx,c100=['100% DE DESCUENTO','HASTA 120€ |emo:moneyfly|'],q=ql,cta=tl),
      hookv=hv,mark=mk,end=en,song=sg,caption=cap,comment="código: 120HACOO ✅ (hasta 120 € de descuento)"))
for (i,a,d,tm_,v,hk,hl,amt,hv,mk,en,sg,I,C,P,T,cap) in FR:
    it,hw,aw,rw,rtx,tapl=FR_I[I]; ct=FR_C[C]; pt,qa,ql=FR_P[P]; tt,ta,tl=FR_T[T]
    jobs.append(dict(id=i,lang='fr',blog=ACC[a],date=d,time=tm_,voice=v,script=' '.join([hk,it,ct,pt,tt]),
      anchors=dict(amt=amt,h=hw,ap=aw,rev=rw,s100=['cent','100','100%','moins','-100%'],hasta=["jusqu'à",'jusqua','jusqu'],q1=qa,drop=['zéro','zero','0'],cta=ta),
      rows=dict(hook=hl,tap=tapl,rev=rtx,c100=['-100% DE RÉDUCTION',"JUSQU'À 120 |emo:gift|"],q=ql,cta=tl),
      hookv=hv,mark=mk,end=en,song=sg,caption=cap,comment="code : 120HACOO ✅ (-100% jusqu'à 120)"))
jobs.append(dict(id='E01',lang='en',blog=ACC['R'],date='2026-11-14',time='17:27',voice='Liam',
  script="Hacoo discount code for November: up to one hundred twenty euros off. Type the code on screen into the coupon box... tap apply... and watch the total. One hundred percent off, up to one hundred twenty euros. My order goes from seventy euros... to zero, with free shipping. Save this for your next order.",
  anchors=dict(amt=['up'],h=['type'],ap=['tap'],rev=['watch'],s100=['one','100','100%','hundred'],hasta=['up'],q1=['my'],drop=['zero','0'],cta=['save']),
  rows=dict(hook=['HACOO DISCOUNT CODE','FOR NOVEMBER','(UP TO 120€ |emo:moneyfly|)'],tap=['TAP APPLY'],rev='WATCH THE TOTAL |emo:eyes|',c100=['100% OFF','UP TO 120€ |emo:gift|'],q=['MY ORDER: 70,34€...','0,00€ + FREE SHIPPING'],cta=['SAVE THIS FOR','YOUR NEXT ORDER |emo:pin|']),
  hookv='check',mark='circle',end='total',song='trend3',
  caption="hacoo discount code for november ✅ code 120HACOO: 100% off up to 120 € + free shipping. Save it for your next order #hacoo #hacoocode #discountcode",comment="code: 120HACOO ✅ (100% off up to 120 €)"))
json.dump(jobs,open('jobs.json','w'),ensure_ascii=False,indent=1)
print(len(jobs),'jobs; chars:',sum(len(j['script']) for j in jobs),'max',max(len(j['script']) for j in jobs))
