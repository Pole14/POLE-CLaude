import json, subprocess, os
V='/home/claude/pole-claude/voices/'
WORDS=json.load(open('words.json'))
O=0.1
REC={
 'es':dict(rec='../k120/rec.mp4',fy=476,sf=430,ty0=901,ty1=901,cy=885,
   FIELD=[22,436,664,516],CIRC=[30,412,330,545],BTN=(860,474),BTNC=[690,418,1034,532],TOT0=[44,866,1036,936],TOT1=[44,862,1036,932],CARD=[40,712,1040,1058],
   tapd=0.33,seo='cupón descuento hacoo noviembre 2026',
   hook={'cart':lambda c1:[[0,0.6],[min(1.7,c1*0.4),2.2],[min(1.7,c1*0.4)+0.75,3.4],[c1-0.3,5.6],[c1,6.1]],
         'check':lambda c1:[[0,3.5],[c1-0.3,5.6],[c1,6.1]],
         'zoomout':lambda c1:[[0,3.5],[c1-0.3,5.6],[c1,6.1]],
         'card':lambda c1:[[0,12.9],[c1-0.4,14.5],[c1-0.39,5.3],[c1-0.3,5.6],[c1,6.1]],
         'drop':lambda c1:[[0,9.9],[0.34,10.14],[0.37,10.16],[0.42,10.2],[c1-0.4,11.7],[c1-0.39,5.3],[c1-0.3,5.6],[c1,6.1]]},
   mid=lambda h,ap,rev,s100,end:[[h,6.75],[ap-0.3,9.05],[ap,9.45],[ap+0.25,9.9],[ap+0.65,10.14],[rev-0.03,10.16],[rev+0.02,10.2],[s100-0.75,11.75],[s100-0.6,11.95],[s100-0.2,12.6],[end,14.6]],
   replay=lambda q1,drop,cta:[[q1+0.01,9.6],[drop-0.05,10.14],[drop-0.02,10.16],[drop+0.03,10.2],[cta,11.0]],
   endt=lambda cta,tot:[[tot,11.9]], endc=lambda cta,tot:[[cta+0.01,13.2],[tot,16.3]], endt2=lambda cta,tot:[[cta+0.01,10.2],[tot,11.75]]),
 'fr':dict(rec='../r4/rec.mp4',fy=527,sf=430,ty0=956,ty1=991,cy=875,
   FIELD=[20,478,660,578],CIRC=[18,468,470,590],BTN=(850,523),BTNC=[680,468,1034,580],TOT0=[24,905,1056,1005],TOT1=[24,940,1056,1040],CARD=[24,705,1056,1045],
   tapd=0.3,seo='code promo hacoo novembre 2026',
   hook={'check':lambda c1:[[0,2.95],[c1-0.3,3.55],[c1,3.85]],
         'card':lambda c1:[[0,10.62],[c1-0.4,11.85],[c1-0.39,2.95],[c1,3.85]],
         'drop':lambda c1:[[0,8.3],[0.34,8.62],[0.35,9.62],[c1-0.4,10.1],[c1-0.39,2.95],[c1,3.85]]},
   mid=lambda h,ap,rev,s100,end:[[h,3.9],[ap-0.3,6.05],[ap,6.6],[ap+0.01,8.25],[ap+0.5,8.6],[rev-0.02,8.62],[rev,9.62],[s100-0.65,10.10],[s100-0.64,10.26],[s100-0.2,10.55],[end,11.85]],
   replay=lambda q1,drop,cta:[[q1+0.01,8.05],[drop-0.02,8.62],[drop-0.01,9.62],[cta,10.0]],
   endt=lambda cta,tot:[[tot,10.1]], endc=lambda cta,tot:[[cta+0.01,10.7],[tot,11.85]], endt2=lambda cta,tot:[[cta+0.01,9.62],[tot,10.1]]),
}
def build(name,lang,voice,M,hookv,rows,font=None,mark='circle',end='total',emo=('moneyfly','moneyfly','moneyfly'),zf=1.22,sizes=(90,112),typ=2.3,res=1.6,song='gone'):
    R=REC[lang]; W=WORDS[voice]['w']; dur=WORDS[voice]['dur']
    # --- pausas extra: antes de "ap" (para teclear con calma) y antes de s100 (para ver el resultado)
    def gap_before(tv):
        prev=max([w for w in W if w[2]<=tv+0.02],key=lambda w:w[2],default=None)
        return (prev[2]+tv)/2 if prev else tv-0.05
    splits=[]
    d1=max(0,typ-(M['ap']-M['h']));  d2=max(0,res-(M['s100']-M['rev']))
    if d1>0.05: splits.append((gap_before(M['ap']),d1))
    if d2>0.05: splits.append((gap_before(M['s100']),d2))
    splits.sort()
    def tm(tv): return round(tv+O+sum(d for s,d in splits if tv>=s-1e-6),3)
    # clips de voz
    cuts=[0]+[s for s,_ in splits]+[dur]; voice_list=[]
    for i in range(len(cuts)-1):
        if len(cuts)==2: voice_list.append([voice,O]); break
        cn=f'{voice}_{name}{i}'
        subprocess.run(['ffmpeg','-v','error','-y','-i',V+voice+'.wav','-ss',str(cuts[i]),'-to',str(cuts[i+1]),'-af','afade=t=in:d=0.02',V+cn+'.wav'],check=True)
        voice_list.append([cn,tm(cuts[i]+1e-4)-1e-4 if i else O])
    h,ap,rev,s100=[tm(M[k]) for k in ('h','ap','rev','s100')]; cta=tm(M['cta']); tot=round(tm(dur)+0.45,2)
    q1=tm(M['q1']) if M.get('q1') else None; drop=tm(M['drop']) if M.get('drop') else None
    c1=round(h-0.28,3)
    rm=R['hook'][hookv](c1)+R['mid'](h,ap,rev,s100,q1 if q1 else cta)
    if q1: rm+=R['replay'](q1,drop,cta)+(R['endt'] if end=='total' else R['endc'])(cta,tot)
    else:  rm+=(R['endt2'] if end=='total' else (lambda c,t:[[t,R['mid'](h,ap,rev,s100,cta)[-1][1]+0.01]]))(cta,tot)
    xs=[a for a,_ in rm]; assert all(xs[i+1]>xs[i] for i in range(len(xs)-1)),(name,rm)
    fy,sf,ty0,ty1,cy=R['fy'],R['sf'],R['ty0'],R['ty1'],R['cy']
    ctr={'p':[540,960],'s':[540,960]}
    cam=[]
    K=lambda t,z,p,s: cam.append({'t':round(t,3),'z':z,'p':list(p),'s':list(s)})
    if hookv=='cart':
        tc=min(1.7,c1*0.4); K(0,1.0,(540,700),(540,700)); K(tc,1.07,(540,700),(540,700)); K(tc+0.75,1.0,(540,960),(540,960)); K(c1-0.3,1.07,(540,ty0),(540,760))
    elif hookv=='check':
        K(0,1.0,(540,960),(540,960)); K(c1-0.3,1.09,(540,ty0),(540,760))
    elif hookv=='zoomout':
        K(0,1.42,(1080,ty0),(1080,700)); K(1.0,1.38,(1080,ty0),(1080,700)); K(c1-0.3,1.0,(540,960),(540,960))
    elif hookv=='card':
        K(0,1.03,(540,cy),(540,740)); K(c1-0.4,1.1,(540,cy),(540,740)); K(c1-0.39,1.0,(540,960),(540,960))
    else:
        K(0,1.05,(540,ty0),(540,760)); K(0.34,1.07,(540,ty0),(540,760)); K(0.35,1.07,(540,ty1),(540,760)); K(c1-0.4,1.13,(540,ty1),(540,760)); K(c1-0.39,1.0,(540,960),(540,960))
    K(c1,1.0,(540,960),(540,960)); K(h+0.5,zf,(0,fy),(0,sf)); K(ap-0.3,zf+0.03,(0,fy),(0,sf)); K(ap+0.15,zf,(1080,fy),(1080,sf)); K(ap+0.6,zf,(1080,fy),(1080,sf))
    K(min(rev-0.15,ap+0.95),1.05,(540,ty0),(540,760)); K(rev-0.02,1.05,(540,ty0),(540,760)); K(rev,1.05,(540,ty1),(540,760)); K(s100-0.75,1.09,(540,ty1),(540,760))
    K(s100-0.2,1.0,(540,cy),(540,cy)); K(s100+0.35,1.05,(540,cy),(540,740))
    if q1:
        K(q1,1.08,(540,cy),(540,740)); K(q1+0.01,1.06,(540,ty0),(540,760)); K(drop-0.02,1.1,(540,ty0),(540,760)); K(drop,1.1,(540,ty1),(540,760)); K(cta,1.13,(540,ty1),(540,760))
        if end=='total': K(cta+0.7,1.03,(540,ty1),(540,800)); K(tot,1.05,(540,ty1),(540,800))
        else: K(cta+0.01,1.03,(540,cy),(540,740)); K(tot,1.08,(540,cy),(540,740))
    else:
        K(cta,1.08,(540,cy),(540,740))
        if end=='total': K(cta+0.01,1.05,(540,ty1),(540,760)); K(tot,1.1,(540,ty1),(540,760))
        else: K(tot,1.1,(540,cy),(540,740))
    ts=[k['t'] for k in cam]; assert all(ts[i+1]>ts[i] for i in range(len(ts)-1)),(name,ts)
    strip=(lambda s:s.replace('*','')) if font=='classic' else (lambda s:s)
    S1,S2=sizes
    G=[]
    def grp(key,y,t1,gap=-0.1):
        rr=[{'at':tm(tv) if isinstance(tv,(int,float)) else tv[0],'text':strip(tx),'size':(S2 if big else S1)} for tv,tx,big in rows.get(key,[])]
        if rr: G.append({'t1':round(t1,3),'y':y,'font':font,'gap':gap if font=='classic' else 0.0,'rows':rr})
    hy={'cart':820,'check':1130,'card':1010,'drop':1100,'zoomout':1060}[hookv]
    hk=rows['hook']; 
    # el gancho puede tener 2 frases: se parte donde haya un hueco marcado con None
    parts=[[]]
    for r in hk:
        if r is None: parts.append([])
        else: parts[-1].append(r)
    for i,pr in enumerate(parts):
        t1=tm(parts[i+1][0][0])-0.12 if i+1<len(parts) else c1
        G.append({'t1':round(t1,3),'y':hy,'font':font,'gap':-0.1 if font=='classic' else 0.0,'rows':[{'at':max(0.12,tm(tv)),'text':strip(tx),'size':(S2 if big else S1)} for tv,tx,big in pr]})
    grp('tap',980,rev-0.05); 
    G.append({'t1':round(s100-0.7,3),'y':1150,'font':font,'rows':[{'at':rev,'text':strip(rows['rev']),'size':S2}]})
    grp('c100',1000,(q1 if q1 else cta)-0.05)
    if q1: grp('q',1150,cta-0.05)
    grp('cta',1150 if end=='total' else 1000,tot)
    code={'t0':round(h+0.05,3),'t1':round(ap-0.08,3),'y':980,'size':S2,'font':font,'text':strip(rows.get('code','|emo:gift|120HACOO|emo:gift|')),'tw':round(ap-0.3-h-0.1,2)}
    sp={'tot':tot,'off':150,'maxw':960,'seo':R['seo'],'seo_y':150,'seo_alpha':0.4,'rmap':[[round(a,3),round(b,3)] for a,b in rm],'cam':cam,
        'punches':[0.15,rev]+([drop] if q1 else []),'shakes':[{'t':rev,'amp':7}]+([{'t':drop,'amp':8}] if q1 else []),
        'taps':[{'t':round(ap+R['tapd'],3),'x':R['BTN'][0],'y':R['BTN'][1]}],
        'rects':[{'t0':round(s100+0.25,3),'t1':round((q1 if q1 else cta)-0.02,3),'box':R['CARD'],'draw':0.45,'w':8}],
        'lines':G,'texts':[code],'blurs':[],
        'bursts':[{'t':0.42 if hookv=='drop' else 0.18,'x':860 if hookv=='drop' else 540,'y':780 if hookv=='drop' else hy+120,'emo':emo[0],'n':10,'seed':len(name)},
                  {'t':round(rev+0.03,3),'x':860,'y':770,'emo':emo[1],'n':12,'seed':7+len(voice)}]}
    if q1: sp['bursts'].append({'t':round(drop+0.03,3),'x':860,'y':770,'emo':emo[2],'n':10,'seed':21}); sp['blurs'].append({'t':round(q1,3),'half':0.1,'px':50})
    if hookv in('card','drop'): sp['blurs'].append({'t':round(c1-0.395,3),'half':0.1,'px':50})
    if hookv=='card': sp['rects'].append({'t0':0.5,'t1':round(c1-0.42,3),'box':R['CARD'],'draw':0.45,'w':8})
    if (q1 and end=='card') or (not q1 and end=='total'): sp['blurs'].append({'t':round(cta,3),'half':0.1,'px':50})
    if end=='card' and q1: sp['rects'].append({'t0':round(cta+0.3,3),'t1':tot,'box':R['CARD'],'draw':0.45,'w':8})
    if mark=='circle':
        sp['circles']=[{'t0':round(h+0.1,3),'t1':round(ap-0.1,3),'box':R['CIRC'],'draw':0.4,'w':8},{'t0':round(ap+0.1,3),'t1':round(min(rev-0.2,ap+0.9),3),'box':R['BTNC'],'draw':0.3,'w':8}]
    else:
        sp['rects']+=[{'t0':round(h+0.1,3),'t1':round(ap-0.1,3),'box':R['FIELD'],'draw':0.4,'w':7},{'t0':round(ap+0.1,3),'t1':round(min(rev-0.2,ap+0.9),3),'box':R['BTNC'],'draw':0.3,'w':7}]
    json.dump(sp,open(f'{name}.json','w')); json.dump({'tot':tot,'voice':voice_list,'rec':R['rec'],'song':song},open(f'{name}_base.json','w'))
    print(name,'tot',tot,'splits',[(round(s,2),round(d,2)) for s,d in splits],'c1',c1,'h',h,'ap',ap,'rev',rev,'s100',s100,'q1',q1,'drop',drop,'cta',cta)
