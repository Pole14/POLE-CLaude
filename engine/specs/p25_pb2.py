#!/usr/bin/env python3
"""pb2.py [ids] -> montaje corto de 4 escenas (gancho sobre el pedido / teclear / solicitar+total / tarjeta). Sin zoom, sin círculos ni emojis volando."""
import json, subprocess, sys
V='/home/claude/pole-claude/voices/'
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
J=json.load(open('cjobs.json')); ids=sys.argv[1:]
for j in J:
    if j['id'] not in ids: continue
    D=[dur(f"{V}p25_{j['id']}_{i}.wav") for i in range(4)]
    mins=[2.0,2.6,2.8,2.4]; pad=[0.12,0.05,0.05,0.7]
    Ls=[round(max(m,d+p),2) for m,d,p in zip(mins,D,pad)]
    S=[0.0]
    for x in Ls: S.append(round(S[-1]+x,3))
    E=S[1:]; tot=S[-1]
    voice=[[f"p25_{j['id']}_{i}",round(S[i]+(0.1 if i==0 else 0.0),3)] for i in range(4)]
    rm=[]
    def seg(*pts):
        for t,r in pts: rm.append([round(t,3),r])
    T2=S[2]+min(1.0,Ls[2]*0.4); TD=T2+0.35
    seg((0,0.25),(E[0]-0.02,1.15))
    seg((S[1],1.2),(S[1]+0.35,1.65),(S[1]+0.6,2.6),(S[1]+0.75,2.95),(E[1]-0.1,5.15))
    seg((S[2],5.16),(S[2]+0.35,5.9),(T2-0.1,7.2),(T2,7.3),(TD,7.47),(E[2]-0.02,8.44))
    seg((S[3],8.47),(S[3]+0.5,9.0),(tot,12.7))
    xs=[a for a,_ in rm]; assert all(xs[i+1]>xs[i] for i in range(len(xs)-1)),rm
    cam=[{'t':0,'z':1.0,'p':[540,960],'s':[540,960]},{'t':tot,'z':1.0,'p':[540,960],'s':[540,960]}]
    sc=j['scenes']; h=sc[0][1]
    lines=[{'t1':round(E[0]-0.02,3),'y':900,'font':'classic','gap':-0.12,'rows':[{'at':-1,'text':h[0],'size':90},{'at':-1,'text':h[1],'size':90},{'at':0.3,'text':h[2],'size':90,'fx':'blur'}]},
           {'t1':round(TD-0.02,3),'y':1040,'font':'classic','rows':[{'at':round(S[2]+0.1,3),'text':sc[2][1][0],'size':92}]},
           {'t1':round(E[2]-0.02,3),'y':1040,'font':'classic','rows':[{'at':round(TD+0.05,3),'text':sc[2][1][1],'size':92}]},
           {'t1':tot,'y':1120,'font':'classic','gap':-0.12,'rows':[{'at':round(S[3]+0.12,3),'text':sc[3][1][0],'size':100},{'at':round(S[3]+0.12+D[3]*0.5,3),'text':sc[3][1][1],'size':90}]}]
    code={'t0':round(S[1]+0.75,3),'t1':round(E[1]-0.03,3),'y':1040,'size':120,'font':'classic','text':'|emo:gift|POL25|emo:gift|','tw':round(Ls[1]-1.1,2)}
    sp={'tot':tot,'off':150,'maxw':960,'seo':'cupón descuento hacoo noviembre 2026','seo_y':150,'seo_alpha':0.4,'rmap':rm,'cam':cam,'punches':[],'shakes':[],'blurs':[],'spots':[],'lines':lines,'texts':[code],
        'taps':[{'t':round(T2,3),'x':856,'y':500}],'circles':[],'rects':[{'t0':round(S[3]+0.7,3),'t1':tot,'box':[40,750,1045,1080],'draw':0.45,'w':8}],'bursts':[]}
    json.dump(sp,open(f"{j['id']}.json",'w'),ensure_ascii=False)
    json.dump({'tot':tot,'voice':voice,'rec':'../p25/rec.mp4','song':j['song']},open(f"{j['id']}_base.json",'w'))
    print(j['id'],'tot',tot,Ls)
