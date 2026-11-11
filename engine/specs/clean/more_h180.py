import json
J=json.load(open('cjobs.json'))
B=['pon este código en la casilla del cupón','escribe este código donde pone cupón','copia este código en el cupón']
C=['y dale a solicitar','dale a solicitar']
CT=[('guárdalo para tu próximo pedido',['guárdalo para tu','próximo pedido |emo:pin|'],'Guárdalo para tu próximo pedido'),('envíaselo a quien compra en hacoo',['envíaselo a quien','compra en hacoo |emo:bag|'],'Envíaselo a quien compra en hacoo'),
    ('comenta si te ha funcionado',['comenta si te','ha funcionado |emo:pointdown|'],'Comenta si te ha funcionado'),('sígueme para más cupones',['sígueme para','más cupones |emo:gift|'],'Sígueme para más cupones'),('pregunta lo que quieras en comentarios',['preguntas en','comentarios |emo:pointdown|'],'Pregunta lo que quieras en comentarios')]
V=['Liam','Jessica','Charlie','Will','Chris']; S=['gone','trend1','trend2','trend3','trend4','trend5']
N=[('H6',['¿cupón de 180€','en hacoo?','(sí, mira |emo:eyes|)'],'¿cupón de 180 euros en hacoo? sí, mira','¿cupón de 180 € en hacoo? sí 👀 código HACOO180: 100% de descuento hasta 180 €.','#hacoo #cuponhacoo #codigohacoo'),
 ('H7',['no pagues tu pedido','de hacoo todavía','(cupón 180€ |emo:eyes|)'],'para, no pagues tu pedido de hacoo todavía','no pagues tu pedido de hacoo todavía 👀 cupón HACOO180: 100% hasta 180 € + envío gratis.','#hacoo #codigohacoo #cuponhacoo'),
 ('H8',['antes de pagar en hacoo','prueba este cupón','(180€ |emo:check|)'],'antes de pagar en hacoo, prueba este cupón','antes de pagar en hacoo prueba este cupón ✅ HACOO180: 100% de descuento hasta 180 €.','#cuponhacoo #hacoo #codigodescuento'),
 ('H9',['mira lo que pasa','si pongo esto en hacoo','(180€ |emo:fire|)'],'mira lo que pasa si pongo esto en hacoo','mira lo que pasa con este código de hacoo 😳 HACOO180: de 70,94 € a 0,00 € con envío gratis.','#hacoo #cuponhacoo #hacco'),
 ('H10',['así se pone un código','en hacoo','(180€ |emo:check|)'],'así se pone un código en hacoo','cómo poner un código en hacoo ✅ HACOO180: 100% de descuento hasta 180 €.','#codigohacoo #hacoo #tutorial'),
 ('H11',['código descuento hacoo','noviembre 2026','(180€ |emo:moneyfly|)'],'código descuento de hacoo para noviembre, 180 euros','código descuento hacoo noviembre 2026 ✅ HACOO180: 100% hasta 180 €, de 70,94 € a 0,00 €.','#codigodescuento #hacoo #codigohacoo'),
 ('H12',['cómo usar el cupón','de 180€ en hacoo','(tutorial |emo:check|)'],'cómo usar el cupón de 180 euros en hacoo','cómo usar el cupón de 180 € de hacoo ✅ HACOO180: 100% de descuento + envío gratis.','#cuponhacoo #hacoo #tutorial'),
 ('H13',['mi pedido de hacoo','se quedó en 0,00€','(cupón 180€ |emo:fire|)'],'mi pedido de hacoo se quedó en cero euros','mi pedido de hacoo se quedó en 0,00 € 😳 cupón HACOO180: 100% hasta 180 € + envío gratis.','#hacoo #cuponhacoo #descuento'),
 ('H14',['¿vas a pedir en hacoo?','usa antes este cupón','(180€ |emo:moneyfly|)'],'¿vas a pedir en hacoo? usa antes este cupón','¿vas a pedir en hacoo? usa antes este cupón ✅ HACOO180: 100% de descuento hasta 180 €.','#hacoo #cuponhacoo #codigohacoo'),
 ('H15',['cupón hacco','de 180€','(noviembre |emo:check|)'],'cupón de hacoo de 180 euros, para noviembre','cupón hacco de 180 € ✅ código HACOO180 en hacoo: 100% de descuento hasta 180 €.','#hacco #hacoo #cuponhacoo')]
for k,(i,hr,hv,cap,tags) in enumerate(N):
    if any(j['id']==i for j in J): continue
    cv,cr,ctxt=CT[k%5]
    sc=[(hv,hr),(B[k%3],[B[k%3]]),(C[k%2],['dale a solicitar']),('de 70 euros... a cero, y con envío gratis',['de 70,94€ a 0,00€ |emo:truck|']),('100% de descuento, hasta 180 euros',['100% de descuento','hasta 180€ |emo:moneyfly|']),(cv,cr)]
    J.append(dict(id=i,lang='es',voice=V[k%5],song=S[k%6],bg='card',caption=f'{cap} {ctxt} {tags}',comment='código: HACOO180 ✅ (hasta 180 € de descuento)',scenes=sc))
json.dump(J,open('cjobs.json','w'),ensure_ascii=False,indent=1); print(len(J))
