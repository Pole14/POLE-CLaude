from sb import *
B=True
# ---------- ES ----------
build('E_K2','es','v120_K2',dict(h=5.88,ap=7.48,rev=9.12,s100=10.14,q1=14.2,drop=17.18,cta=18.7),'cart',
 dict(hook=[(0.0,'si vas a comprar',0),(0.72,'en hacoo, espera |emo:eyes|',0),None,(3.1,'mira este código',0),(3.96,'de 120€ |emo:moneyfly|',B)],
      tap=[(7.48,'dale a solicitar',0)],rev='y listo |emo:check|',
      c100=[(10.14,'100% de descuento',0),(11.5,'hasta 120€ |emo:moneyfly|',B)],
      q=[(14.2,'tu pedido pasa de 39€...',0),(16.98,'a 3,70€ |emo:fire|',B)],
      cta=[(18.7,'pásaselo a quien',0),(19.6,'compre en hacoo |emo:bag|',0)]),
 font='classic',mark='circle',end='total',emo=('moneyfly','moneyfly','fire'),song='gone')
build('E_V2','es','v120_V2',dict(h=5.08,ap=7.1,rev=8.74,s100=10.12,q1=14.24,drop=16.9,cta=18.44),'drop',
 dict(hook=[(0.0,'¿sabías que hacoo',0),(1.0,'tiene un cupón',0),(1.86,'de *120€*? |emo:moneyfly|',B),None,(4.1,'mira |emo:eyes|',B)],
      tap=[(7.1,'dale a *solicitar*',0)],rev='¡sorpresa! |emo:gift|',
      c100=[(10.12,'*100%* de descuento',0),(11.6,'hasta *120€*',B)],
      q=[(14.24,'39 euros...',0),(16.32,'se quedan en *3,70€* |emo:fire|',0)],
      cta=[(18.44,'comenta si te',0),(19.12,'ha funcionado |emo:pointdown|',0)]),
 font=None,mark='rect',end='card',emo=('gift','moneyfly','moneyfly'),zf=1.2,sizes=(84,108),song='trend2')
build('E_V1','es','v120_V1',dict(h=3.5,ap=5.06,rev=6.74,s100=7.8,q1=11.26,drop=13.46,cta=14.84),'card',
 dict(hook=[(0.0,'hacoo te descuenta',0),(1.1,'120€ |emo:moneyfly|',B),(2.06,'con este código',0)],
      tap=[(5.06,'dale a solicitar',0)],rev='ahí está |emo:check|',
      c100=[(7.8,'100% de descuento',0),(9.46,'hasta 120€ |emo:gift|',B)],
      q=[(11.26,'de 39€...',0),(13.04,'a 3,70€ |emo:fire|',B)],
      cta=[(14.84,'pásaselo a quien',0),(15.5,'compre en hacoo |emo:bag|',0)]),
 font='classic',mark='rect',end='total',emo=('fire','moneyfly','gift'),zf=1.25,sizes=(92,116),song='trend4')
build('E_Z','es','v120_Z',dict(h=3.18,ap=5.6,rev=7.14,s100=8.18,q1=11.84,drop=14.26,cta=15.88),'check',
 dict(hook=[(0.0,'así se usa el cupón',0),(1.14,'de *120€* de hacoo |emo:moneyfly|',0)],
      tap=[(5.6,'dale a *solicitar*',0)],rev='y ya está |emo:check|',
      c100=[(8.18,'*100%* de descuento',0),(9.54,'hasta *120€* |emo:fire|',B)],
      q=[(11.84,'de 39€...',0),(13.86,'a solo *3,70€* |emo:moneyfly|',B)],
      cta=[(15.88,'comenta si te',0),(16.54,'ha funcionado |emo:pointdown|',0)]),
 font='Montserrat-800.ttf',mark='circle',end='card',emo=('moneyfly','fire','moneyfly'),zf=1.2,sizes=(80,104),song='trend1')
# ---------- FR (grabación francesa) ----------
build('F_R2','fr','v120fr_R2e',dict(h=3.86,ap=5.26,rev=6.98,s100=8.38,cta=12.34),'card',
 dict(hook=[(0.0,"jusqu'à 120",B),(1.12,'de réduction sur hacoo |emo:moneyfly|',0),None,(2.78,'je te montre |emo:eyes|',0)],
      tap=[(5.26,'clique sur',0),(5.7,'le bouton rouge',0)],rev='regarde |emo:fire|',
      c100=[(8.38,'-100% de réduction',0),(10.08,"jusqu'à 120 |emo:gift|",B)],
      cta=[(12.34,'abonne-toi pour',0),(13.22,'plus de codes |emo:pin|',0)]),
 font='classic',mark='circle',end='total',emo=('moneyfly','moneyfly','moneyfly'),song='trend3')
build('F_C2','fr','v120fr_C2e',dict(h=2.28,ap=3.4,rev=5.26,s100=6.5,q1=10.16,drop=11.22,cta=13.12),'drop',
 dict(hook=[(0.0,'je paye *0,00* |emo:moneyfly|',B),(1.12,"je t'explique |emo:pointdown|",0)],
      tap=[(3.4,'clique sur',0),(3.84,'le *bouton rouge*',0)],rev='regarde ça |emo:eyes|',
      c100=[(6.5,'*-100%* de réduction',0),(7.72,"jusqu'à *120*",B)],
      q=[(10.16,'ma commande passe',0),(11.04,'à *0,00* |emo:check|',B)],
      cta=[(13.12,'partage-la',0),(13.76,'à un pote |emo:bheart|',0)]),
 font=None,mark='rect',end='card',emo=('moneyfly','gift','moneyfly'),zf=1.2,sizes=(84,110),song='trend5')
build('F_F2','fr','v120fr_F2e',dict(h=3.64,ap=4.84,rev=6.44,s100=7.38,q1=10.42,drop=11.2,cta=12.72),'check',
 dict(hook=[(0.0,"tu savais qu'hacoo",0),(1.3,'a un code de *120* ? |emo:eyes|',0)],
      tap=[(4.84,'clique sur',0),(5.22,'le *bouton rouge*',0)],rev='regarde |emo:gift|',
      c100=[(7.38,'*-100%* de réduction',0),(8.68,"jusqu'à *120* |emo:fire|",B)],
      q=[(10.42,'et je paie',0),(11.2,'*0,00* |emo:moneyfly|',B)],
      cta=[(12.72,'dis-moi en commentaire',0),(13.92,'si ça marche |emo:pointdown|',0)]),
 font='Montserrat-800.ttf',mark='circle',end='total',emo=('fire','moneyfly','moneyfly'),zf=1.24,sizes=(80,104),song='gone')
