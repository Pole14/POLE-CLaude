#!/usr/bin/env python3
"""nvb.py [ids] -> formatos nuevos (15 nov): X marcador (serif + rotulador + contador), Y 3 pasos (pastilla negra, lista con checks), Z nota (máquina de escribir en caja blanca).
Los textos van abajo (y>=1150) para no tapar ni la casilla ni el total."""
import json, subprocess, sys
V='/home/claude/pole-claude/voices/'
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
STY={'A':{'file':'DMSerifDisplay-Regular.ttf','fill':[20,20,20,255],'stroke':0.085,'sfill':[255,255,255,255],'hl':{'bg':[255,221,51,255],'fg':[20,20,20,255]},'lh':1.12,'shadow':0.35},
     'B':{'file':'BricolageGrotesque.ttf','var':'ExtraBold','fill':[255,255,255,255],'pill':{'bg':[16,16,16,255],'r':0.34,'padx':0.42,'pady':0.12},'hl':{'fg':[255,221,51,255]},'lh':1.3,'shadow':0.4},
     'C':{'file':'SpaceMono-Bold.ttf','fill':[20,20,20,255],'pill':{'bg':[255,255,255,255],'line':[20,20,20,255],'lw':5,'r':0.16,'padx':0.34,'pady':0.1},'hl':{'fg':[226,28,38,255]},'lh':1.34,'shadow':0.5}}
TOTBOX=[20,862,1060,940]
J=json.load(open('cjobs.json')); ids=sys.argv[1:]
for j in J:
    if ids and j['id'] not in ids: continue
    D=[dur(f"{V}nova_{j['id']}_{i}.wav") for i in range(4)]
    mins=[2.2,2.6,2.8,2.4]; pad=[0.12,0.05,0.05,0.7]
    Ls=[round(max(m,d+p),2) for m,d,p in zip(mins,D,pad)]
    S=[0.0]
    for x in Ls: S.append(round(S[-1]+x,3))
    E=S[1:]; tot=S[-1]
    voice=[[f"nova_{j['id']}_{i}",round(S[i]+(0.1 if i==0 else 0.0),3)] for i in range(4)]
    rm=[]
    def seg(*pts):
        for t,r in pts: rm.append([round(t,3),r])
    T2=S[2]+min(1.0,Ls[2]*0.4); TD=T2+0.35
    if j['map']=='h':
        seg((0,0.25),(E[0]-0.02,1.15)); seg((S[1],1.2),(S[1]+0.35,1.65),(S[1]+0.6,2.6),(S[1]+0.75,2.95),(E[1]-0.1,5.15))
        seg((S[2],5.16),(S[2]+0.35,5.9),(T2-0.1,7.2),(T2,7.3),(TD,7.47),(E[2]-0.02,8.44)); seg((S[3],8.47),(S[3]+0.5,9.0),(tot,12.7))
    else:
        seg((0,0.1),(E[0]-0.02,0.9)); seg((S[1],0.95),(S[1]+0.35,1.5),(S[1]+0.6,2.0),(S[1]+0.75,2.3),(E[1]-0.1,4.2))
        seg((S[2],4.21),(S[2]+0.35,5.0),(T2-0.1,6.35),(T2,6.5),(TD,7.0),(E[2]-0.02,7.7)); seg((S[3],7.75),(S[3]+0.5,8.25),(tot,12.05))
    xs=[a for a,_ in rm]; assert all(xs[i+1]>xs[i] for i in range(len(xs)-1)),rm
    cam=[{'t':0,'z':1.0,'p':[540,960],'s':[540,960]},{'t':tot,'z':1.0,'p':[540,960],'s':[540,960]}]
    lines=[]; texts=[]; counters=[]; spots=[]; c=j['code']; f=j['fmt']; r=lambda x:round(x,3)
    if f=='X':
        lines+=[{'t1':r(E[0]-0.02),'y':1170,'font':'A','gap':0.05,'rows':[{'at':-1,'text':'así baja el *total*','size':124},{'at':-1,'text':'en hacoo','size':124},{'at':0.35,'text':'(con un solo código)','size':72,'fx':'blur'}]},
                {'t1':r(E[1]-0.03),'y':985,'font':'A','rows':[{'at':r(S[1]+0.1),'text':'pon este código','size':100}]},
                {'t1':r(TD-0.02),'y':1200,'font':'A','rows':[{'at':r(S[2]+0.1),'text':'dale a *solicitar*','size':112}]},
                {'t1':r(E[2]-0.02),'y':1150,'font':'A','rows':[{'at':r(TD),'text':'total del pedido','size':76}]},
                {'t1':tot,'y':1180,'font':'A','rows':[{'at':r(S[3]+0.12),'text':'*25%* de descuento','size':116},{'at':r(S[3]+0.12+D[3]*0.5),'text':'+ envío gratis |emo:truck|','size':100}]}]
        texts+=[{'t0':r(S[1]+0.5),'t1':r(E[1]-0.03),'y':1095,'size':150,'font':'A','text':'*'+c+'*','tw':1.0}]
        counters+=[{'t0':r(TD),'t1':r(E[2]-0.02),'y':1400,'size':200,'font':'A','frm':j['frm'],'to':j['to'],'dur':0.8,'suffix':' €','in':1}]
        spots+=[{'t0':0.15,'t1':r(E[0]-0.05),'box':TOTBOX,'dim':0.38,'fade':0.35},{'t0':r(TD-0.1),'t1':r(E[2]-0.05),'box':TOTBOX,'dim':0.38,'fade':0.3}]
    elif f=='Y':
        h2=r(S[1]+0.1+D[1]*0.52)
        lines+=[{'t1':r(E[0]-0.02),'y':1160,'font':'B','rows':[{'at':-1,'text':'*3 pasos* para','size':108},{'at':-1,'text':'pagar menos en hacoo','size':84}]},
                {'t1':r(E[2]-0.02),'y':985,'x':90,'font':'B','rows':[{'at':r(S[1]+0.1),'text':'*1*  casilla del cupón','size':72,'done':h2},{'at':h2,'text':'*2*  escribe '+c,'size':72,'done':r(S[2]+0.1)},{'at':r(S[2]+0.1),'text':'*3*  dale a solicitar','size':72,'done':r(TD+0.1)}]},
                {'t1':tot,'y':1170,'font':'B','rows':[{'at':r(S[3]+0.12),'text':'*100%* de descuento','size':100},{'at':r(S[3]+0.12+D[3]*0.5),'text':'hasta 180€ |emo:fire|','size':92}]}]
        spots+=[{'t0':r(TD-0.1),'t1':r(E[2]-0.05),'box':TOTBOX,'dim':0.38,'fade':0.3}]
    else:
        a=0.15; t1=a+1.0; t2=t1+0.15
        texts+=[{'t0':-1,'t1':r(E[0]-0.02),'y':1150,'size':84,'font':'C','text':'nota mental:'},
                {'t0':r(a+0.75),'t1':r(E[0]-0.02),'y':1270,'size':84,'font':'C','text':'no pagar en *hacoo*','tw':0.9},
                {'t0':r(a+1.8),'t1':r(E[0]-0.02),'y':1390,'size':84,'font':'C','text':'sin este cupón |emo:eyes|','tw':0.7},
                {'t0':r(S[1]+0.1),'t1':r(E[1]-0.03),'y':985,'size':76,'font':'C','text':'código:','tw':0.3},
                {'t0':r(S[1]+0.5),'t1':r(E[1]-0.03),'y':1090,'size':124,'font':'C','text':'*'+c+'*','tw':1.0},
                {'t0':r(S[2]+0.1),'t1':r(TD-0.02),'y':1200,'size':84,'font':'C','text':'pulsa *solicitar*','tw':0.5},
                {'t0':r(TD),'t1':r(E[2]-0.02),'y':1200,'size':84,'font':'C','text':'mira cómo baja |emo:eyes|','tw':0.6},
                {'t0':r(S[3]+0.12),'t1':tot,'y':1170,'size':84,'font':'C','text':'cupón de hasta *200€*','tw':0.8},
                {'t0':r(S[3]+0.12+D[3]*0.5),'t1':tot,'y':1295,'size':84,'font':'C','text':'+ envío gratis |emo:truck|','tw':0.6}]
        spots+=[{'t0':r(TD-0.1),'t1':r(E[2]-0.05),'box':TOTBOX,'dim':0.38,'fade':0.3}]
    sp={'tot':tot,'off':150,'maxw':940,'styles':STY,'seo':'cupón descuento hacoo noviembre 2026','seo_y':150,'seo_alpha':0.4,'rmap':rm,'cam':cam,'punches':[],'shakes':[],'blurs':[],'spots':spots,'lines':lines,'texts':texts,'counters':counters,
        'taps':[{'t':r(T2),'x':856,'y':500}],'circles':[],'rects':[{'t0':r(S[3]+0.7),'t1':tot,'box':[40,750,1045,1080],'draw':0.45,'w':8}],'bursts':[]}
    json.dump(sp,open(f"{j['id']}.json",'w'),ensure_ascii=False)
    json.dump({'tot':tot,'voice':voice,'rec':j['rec'],'song':j['song']},open(f"{j['id']}_base.json",'w'))
    print(j['id'],'tot',tot,Ls)
