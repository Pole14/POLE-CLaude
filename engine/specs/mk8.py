from sb import *
B=True
build('E_K5','es','v120_K5',dict(h=4.14,ap=6.12,rev=7.68,s100=8.82,q1=12.58,drop=16.02,cta=17.52),'zoomout',
 dict(hook=[(0.0,'*120€* menos |emo:moneyfly|',B),(1.12,'en tu pedido de hacoo',0),(2.18,'con un solo código',0)],
      tap=[(6.12,'dale a *solicitar*',0)],rev='y listo |emo:check|',
      c100=[(8.82,'*100%* de descuento',0),(10.1,'hasta *120€* |emo:gift|',B)],
      q=[(12.58,'tu pedido pasa de 39€...',0),(15.4,'a *3,70€* |emo:fire|',B)],
      cta=[(17.52,'guárdalo antes',0),(18.14,'de comprar |emo:pin|',0)]),
 font='ArchivoBlack-Regular.ttf',mark='rect',end='total',emo=('gift','moneyfly','fire'),zf=1.2,sizes=(72,96),song='trend3')
