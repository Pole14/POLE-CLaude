import json
B=['pon este código en la casilla del cupón','escribe este código donde pone cupón','copia este código en el cupón']
C=['y dale a solicitar','dale a solicitar']
CT=[('guárdalo para tu próximo pedido',['guárdalo para tu','próximo pedido |emo:pin|'],'Guárdalo para tu próximo pedido'),('envíaselo a quien compra en hacoo',['envíaselo a quien','compra en hacoo |emo:bag|'],'Envíaselo a quien compra en hacoo'),
    ('comenta si te ha funcionado',['comenta si te','ha funcionado |emo:pointdown|'],'Comenta si te ha funcionado'),('sígueme para más cupones',['sígueme para','más cupones |emo:gift|'],'Sígueme para más cupones'),('pregunta lo que quieras en comentarios',['preguntas en','comentarios |emo:pointdown|'],'Pregunta lo que quieras en comentarios')]
V=['Liam','Jessica','Charlie','Will','Chris']; S=['trend3','trend1','trend4','trend2','trend5']
N=[('B1',['cupón de hacoo','de 200€','(black friday 2026 |emo:check|)'],'cupón de hacoo de 200 euros, para el black friday','cupón de hacoo de 200 € black friday 2026 ✅ código BLACKF: hasta 200 € de descuento + envío gratis, hasta el 30 nov.','#cuponhacoo #hacoo #blackfriday'),
 ('B2',['black friday en hacoo','cupón de 200€','(código BLACKF |emo:fire|)'],'black friday en hacoo, cupón de 200 euros','black friday en hacoo 🔥 cupón de hasta 200 € con el código BLACKF + envío gratis.','#blackfriday #hacoo #cuponhacoo'),
 ('B3',['antes de pagar en hacoo','pon este código','(hasta 200€ |emo:eyes|)'],'antes de pagar en hacoo, pon este código','antes de pagar en hacoo pon este código 👀 BLACKF: cupón de hasta 200 € + envío gratis.','#hacoo #codigohacoo #cuponhacoo'),
 ('B4',['código hacoo','black friday','(200€ de descuento |emo:moneyfly|)'],'código de hacoo para el black friday, 200 euros de descuento','código hacoo black friday ✅ BLACKF: cupón de hasta 200 € + envío gratis, del 13 al 30 nov.','#codigohacoo #blackfriday #hacoo'),
 ('B5',['¿cupón de 200€','en hacoo?','(sí, mira |emo:eyes|)'],'¿cupón de 200 euros en hacoo? sí, mira','¿cupón de 200 € en hacoo? sí 👀 código BLACKF: hasta 200 € de descuento + envío gratis.','#hacoo #cuponhacoo #codigodescuento'),
 ('B6',['si compras en hacoo','mira este cupón','(200€ |emo:fire|)'],'si compras en hacoo, mira este cupón de 200 euros','si compras en hacoo mira este cupón 🔥 BLACKF: hasta 200 € de descuento + envío gratis.','#hacoo #cuponhacoo #hacco'),
 ('B7',['200€ de descuento','en hacoo','(con un solo código |emo:check|)'],'200 euros de descuento en hacoo, con un solo código','200 € de descuento en hacoo con un solo código ✅ BLACKF: cupón de hasta 200 € + envío gratis.','#hacoo #descuento #cuponhacoo'),
 ('B8',['el cupón de hacoo','del black friday','(hasta 200€ |emo:moneyfly|)'],'el cupón de hacoo del black friday, hasta 200 euros','el cupón de hacoo del black friday ✅ código BLACKF: hasta 200 € + envío gratis.','#cuponhacoo #blackfriday #hacoo'),
 ('B9',['no pagues tu pedido','de hacoo todavía','(cupón 200€ |emo:eyes|)'],'para, no pagues tu pedido de hacoo todavía','no pagues tu pedido de hacoo todavía 👀 cupón BLACKF: hasta 200 € de descuento + envío gratis.','#hacoo #codigohacoo #cuponhacoo'),
 ('B10',['cómo usar el cupón','de 200€ de hacoo','(paso a paso |emo:check|)'],'cómo usar el cupón de 200 euros de hacoo, paso a paso','cómo usar el cupón de 200 € de hacoo ✅ código BLACKF + envío gratis, paso a paso.','#cuponhacoo #hacoo #tutorial'),
 ('B11',['código descuento hacoo','noviembre 2026','(hasta 200€ |emo:fire|)'],'código descuento de hacoo para noviembre, hasta 200 euros','código descuento hacoo noviembre 2026 🔥 BLACKF: cupón de hasta 200 € + envío gratis.','#codigodescuento #hacoo #codigohacoo')]
J=[]
for k,(i,hr,hv,cap,tags) in enumerate(N):
    cv,cr,ctxt=CT[k%5]
    sc=[(hv,hr),(B[k%3],[B[k%3]]),(C[k%2],['dale a solicitar']),('cupón aplicado, y el envío gratis',['envío gratis |emo:truck|']),('200 euros de descuento, hasta el 30 de noviembre',['200€ de descuento','hasta el 30 nov |emo:moneyfly|']),(cv,cr)]
    J.append(dict(id=i,lang='es',voice=V[k%5],song=S[(k+k//5)%5],bg='card',caption=f'{cap} {ctxt} {tags}',comment='código: BLACKF ✅ (cupón de hasta 200 €, hasta el 30 nov)',scenes=sc))
json.dump(J,open('cjobs.json','w'),ensure_ascii=False,indent=1); print(len(J))
