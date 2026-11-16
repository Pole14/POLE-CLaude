#!/usr/bin/env python3
"""rb.py [ids] -> estilo "referencia 16 nov", versión directa: pantalla completa del móvil, un bloque de texto corto que cambia por frase,
rectángulo rojo en la casilla. Se empieza a teclear el código en el segundo 1 (sin escena de relleno). 4 frases: gancho / código / solicitar / cierre."""
import json, subprocess, sys
V='/home/claude/pole-claude/voices/'
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
k=1920/2340; X=lambda x:round(97+x*k); Y=lambda y:round((y+150)*k)
J=json.load(open('cjobs.json')); ids=sys.argv[1:]
for j in J:
    if ids and j['id'] not in ids: continue
    use=[0,2,3,4]; D=[dur(f"{V}rf_{j['id']}_{i}.wav") for i in use]
    mins=[1.9,2.0,2.6,1.8]; pad=[0.05,0.05,0.05,0.4]
    Ls=[round(max(m,d+p),2) for m,d,p in zip(mins,D,pad)]
    S=[0.0]
    for x in Ls: S.append(round(S[-1]+x,3))
    E=S[1:]; tot=S[-1]; r=lambda x:round(x,3)
    voice=[[f"rf_{j['id']}_{i}",r(S[q]+(0.06 if q==0 else 0.0))] for q,i in enumerate(use)]
    T=S[2]+0.75
    rm=[[0,1.2],[0.4,1.65],[0.9,2.9],[r(E[1]-0.15),5.15],[S[2],5.16],[r(S[2]+0.3),5.9],[r(T-0.1),7.2],[r(T),7.3],[r(T+0.2),7.47],
        [r(E[2]-0.52),8.44],[r(E[2]-0.5),8.47],[r(E[2]-0.05),9.0],[S[3],9.02],[tot,12.7]]
    xs=[a for a,_ in rm]; assert all(xs[i+1]>xs[i] for i in range(len(xs)-1)),rm
    lines=[]; ys=[(800,850),(800,850),(1010,1050),(1090,1130)]
    for q,i in enumerate(use):
        rows=j['scenes'][i][1]; y=ys[q][0] if len(rows)==2 else ys[q][1]
        lines.append({'t1':r(E[q]-0.02) if q<3 else tot,'y':y,'font':'classic','rows':[{'at':-1 if q==0 else r(S[q]+0.02),'text':t,'size':76} for t in rows]})
    sp={'tot':tot,'off':0,'maxw':900,'seo':'cupón descuento hacoo noviembre 2026','seo_y':int(Y(60)),'seo_alpha':0.35,'rmap':rm,
        'cam':[{'t':0,'z':1.0,'p':[540,960],'s':[540,960]},{'t':tot,'z':1.0,'p':[540,960],'s':[540,960]}],'punches':[],'shakes':[],'blurs':[],'spots':[],'lines':lines,'texts':[],'taps':[],'circles':[],'bursts':[],
        'rects':[{'t0':0.25,'t1':r(T+0.1),'box':[X(22),Y(452),X(590),Y(548)],'draw':0.35,'w':6}]}
    json.dump(sp,open(f"{j['id']}.json",'w'),ensure_ascii=False)
    json.dump({'tot':tot,'voice':voice,'rec':j['rec'],'song':j['song']},open(f"{j['id']}_base.json",'w'))
    print(j['id'],'tot',tot,Ls)
