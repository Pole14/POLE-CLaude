import json
B=['pon este código en la casilla del cupón','escribe este código donde pone cupón','copia este código en el cupón','pon este código en la casilla del cupón','escribe este código donde pone cupón']
C=['y dale a solicitar','dale a solicitar','y dale a solicitar','dale a solicitar','y dale a solicitar']
D1='de 70 euros... a 53'
D2='envío gratis, y 25% de descuento'
CM='código: POL25 ✅ (25% de descuento + envío gratis)'
J=[
 ('P1','Liam','gone',['código hacoo','25% de descuento','(+ envío gratis |emo:truck|)'],'código de hacoo, 25% de descuento y envío gratis','guárdalo para tu próximo pedido',['guárdalo para tu','próximo pedido |emo:pin|'],
  'código hacoo 25% de descuento ✅ POL25: 25% menos + envío gratis, de 70,94 € a 53,20 €. Guárdalo para tu próximo pedido #codigohacoo #hacoo #cuponhacoo'),
 ('P2','Jessica','trend5',['cupón hacoo','sin fecha límite','(25% |emo:check|)'],'cupón de hacoo sin fecha límite, 25% de descuento','envíaselo a quien compra en hacoo',['envíaselo a quien','compra en hacoo |emo:bag|'],
  'cupón hacoo sin fecha límite ✅ código POL25: 25% de descuento + envío gratis. Envíaselo a quien compra en hacoo #cuponhacoo #hacoo #codigodescuento'),
 ('P3','Charlie','trend2',['de 70,94€ a 53,20€','en hacoo','(código POL25 |emo:fire|)'],'de 70 euros a 53 en hacoo, así','comenta si te ha funcionado',['comenta si te','ha funcionado |emo:pointdown|'],
  'de 70,94 € a 53,20 € en hacoo 👀 código POL25: 25% de descuento + envío gratis. Comenta si te ha funcionado #hacoo #cuponhacoo #hacco'),
 ('P4','Will','trend4',['cómo pagar menos','en hacoo','(25% + envío gratis |emo:truck|)'],'cómo pagar menos en hacoo','sígueme para más cupones',['sígueme para','más cupones |emo:gift|'],
  'cómo pagar menos en hacoo ✅ código POL25: 25% de descuento + envío gratis. Sígueme para más cupones #hacoo #codigohacoo #ahorrar'),
 ('P5','Chris','trend1',['si compras en hacoo','usa este código','(25% |emo:eyes|)'],'si compras en hacoo, usa este código','pregunta lo que quieras en comentarios',['preguntas en','comentarios |emo:pointdown|'],
  'si compras en hacoo usa este código 👀 POL25: 25% de descuento + envío gratis. Pregunta lo que quieras en comentarios #hacoo #cuponhacoo #descuento'),
]
out=[]
for k,(i,v,s,hr,hv,cv,cr,cap) in enumerate(J):
    sc=[(hv,hr),(B[k],[B[k]]),(C[k],['dale a solicitar']),(D1,['de 70,94€ a 53,20€ |emo:moneyfly|']),(D2,['envío gratis','+ 25% de descuento |emo:truck|']),(cv,cr)]
    out.append(dict(id=i,lang='es',voice=v,song=s,bg='card',caption=cap,comment=CM,scenes=sc))
json.dump(out,open('cjobs.json','w'),ensure_ascii=False,indent=1); print(len(out))
