import json
B=['pon este código en la casilla del cupón','escribe este código donde pone cupón','copia este código en el cupón','pon este código en la casilla del cupón','escribe este código donde pone cupón']
C=['y dale a solicitar','dale a solicitar','y dale a solicitar','dale a solicitar','y dale a solicitar']
D1='de 70 euros... a cero, y con envío gratis'
D2='100% de descuento, hasta 180 euros'
J=[
 ('H1','Liam','gone',['cupón de hacoo','de 180€','(noviembre 2026 |emo:check|)'],'cupón de hacoo de 180 euros, para noviembre','guárdalo para tu próximo pedido',['guárdalo para tu','próximo pedido |emo:pin|'],
  'cupón de hacoo de 180 € ✅ código HACOO180: 100% de descuento hasta 180 €, de 70,94 € a 0,00 € con envío gratis. Guárdalo para tu próximo pedido #cuponhacoo #hacoo #codigohacoo'),
 ('H2','Jessica','trend2',['de 70,94€ a 0,00€','en hacoo','(cupón 180€ |emo:fire|)'],'de 70 euros a cero en hacoo, mira','envíaselo a quien compra en hacoo',['envíaselo a quien','compra en hacoo |emo:bag|'],
  'de 70,94 € a 0,00 € en hacoo 😳 cupón HACOO180: 100% de descuento hasta 180 € + envío gratis. Envíaselo a quien compra en hacoo #hacoo #cuponhacoo #hacco'),
 ('H3','Charlie','trend4',['código hacoo de 180€','paso a paso','(tutorial |emo:check|)'],'código de hacoo de 180 euros, paso a paso','comenta si te ha funcionado',['comenta si te','ha funcionado |emo:pointdown|'],
  'código hacoo de 180 € paso a paso ✅ HACOO180: 100% de descuento hasta 180 €. Comenta si te ha funcionado #codigohacoo #hacoo #tutorial'),
 ('H4','Will','trend1',['si compras en hacoo','mira este cupón','(180€ |emo:eyes|)'],'si compras en hacoo, mira este cupón de 180 euros','sígueme para más cupones',['sígueme para','más cupones |emo:gift|'],
  'si compras en hacoo mira este cupón 👀 HACOO180: 100% de descuento hasta 180 €, mi pedido de 70,94 € se quedó en 0,00 €. Sígueme para más cupones #hacoo #cuponhacoo #codigodescuento'),
 ('H5','Chris','trend3',['180€ de descuento','en hacoo','(con un solo código |emo:moneyfly|)'],'180 euros de descuento en hacoo, con un solo código','pregunta lo que quieras en comentarios',['preguntas en','comentarios |emo:pointdown|'],
  '180 € de descuento en hacoo con un solo código 😳 HACOO180: 100% hasta 180 € + envío gratis. Pregunta lo que quieras en comentarios #hacoo #cuponhacoo #descuento'),
]
out=[]
for k,(i,v,s,hr,hv,cv,cr,cap) in enumerate(J):
    sc=[(hv,hr),(B[k],[B[k]]),(C[k],['dale a solicitar']),(D1,['de 70,94€ a 0,00€ |emo:truck|']),(D2,['100% de descuento','hasta 180€ |emo:moneyfly|']),(cv,cr)]
    out.append(dict(id=i,lang='es',voice=v,song=s,bg='card',caption=cap,comment='código: HACOO180 ✅ (hasta 180 € de descuento)',scenes=sc))
json.dump(out,open('cjobs.json','w'),ensure_ascii=False,indent=1); print(len(out))
