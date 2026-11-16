#!/usr/bin/env python3
"""dpb.py [ids] -> spec para engine/dopa.py. Una sola locución (ElevenLabs con marcas de tiempo, rápida) y todos los tiempos salen de la voz.
jobs.json: [{id, voice, theme, chips[4], close, cemo, sents:[gancho, código (con 'escribe pol 25'), solicitar+beneficio, cierre]}]"""
import json,os,sys,base64,subprocess,urllib.request,re
SC=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V='/home/claude/pole-claude/voices/'
REC=SC+'/p25/rec.mp4'; CODE='POL25'; HANDLE='@hacoorabatt'
def api(path,data=None):
    r=urllib.request.Request('https://api.elevenlabs.io'+path,data=json.dumps(data).encode() if data else None,headers={'xi-api-key':open(SC+'/.el_key').read().strip(),'Content-Type':'application/json'})
    return urllib.request.urlopen(r,timeout=180)
vs=None; J=json.load(open('jobs.json')); ids=sys.argv[1:]
for j in J:
    if ids and j['id'] not in ids: continue
    text=' '.join(j['sents']); wav=f"{V}dp_{j['id']}.wav"; meta=f"{j['id']}_al.json"
    if not os.path.exists(meta):
        if vs is None: vs={v['name'].split(' ')[0]:v['voice_id'] for v in json.load(api('/v1/voices'))['voices']}
        body={'text':text,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.45,'similarity_boost':0.8,'style':0.3,'speed':1.12}}
        r=json.load(api(f"/v1/text-to-speech/{vs[j['voice']]}/with-timestamps?output_format=mp3_44100_128",body))
        open('/tmp/_d.mp3','wb').write(base64.b64decode(r['audio_base64']))
        # quita el aire muerto: cada silencio de más de 0,26 s se deja en 0,14 s y las marcas de tiempo se recolocan igual
        import numpy as np
        x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','/tmp/_d.mp3','-f','f32le','-ac','1','-ar','48000','-'],capture_output=True).stdout,np.float32)
        hop=480; e=np.abs(x[:len(x)//hop*hop]).reshape(-1,hop).mean(1); sil=e<0.006; cuts=[]; i=0
        while i<len(sil):
            if sil[i]:
                k=i
                while k<len(sil) and sil[k]: k+=1
                if (k-i)*0.01>0.26 and i>0 and k<len(sil): cuts.append(((i+7)*0.01,(k-7)*0.01))
                i=k
            else: i+=1
        keep=[]; p=0.0
        for a,b in cuts: keep.append((p,a)); p=b
        keep.append((p,len(x)/48000))
        y=np.concatenate([x[int(a*48000):int(b*48000)] for a,b in keep])
        def mp(t):
            rem=0.0
            for a,b in cuts:
                if t>=b: rem+=b-a
                elif t>a: return a-rem
            return t-rem
        al=r['alignment']; al['character_start_times_seconds']=[round(mp(t),3) for t in al['character_start_times_seconds']]; al['character_end_times_seconds']=[round(mp(t),3) for t in al['character_end_times_seconds']]
        subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','1','-i','-',wav],input=y.tobytes(),check=True)
        json.dump(al,open(meta,'w')); print(j['id'],'silencios recortados',len(cuts),'ahorro',round(sum(b-a for a,b in cuts),2),'s')
    al=json.load(open(meta)); cs=al['character_start_times_seconds']; ce=al['character_end_times_seconds']
    assert ''.join(al['characters'])==text
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wav],capture_output=True,text=True).stdout)
    sw=[]; p=0
    for s in j['sents']:
        a=text.index(s,p); p=a+len(s); sw.append([[m.group(0),round(cs[a+m.start()],3),round(ce[a+m.end()-1],3)] for m in re.finditer(r'\S+',s)])
    S=[w[0][1] for w in sw]; E=[w[-1][2] for w in sw]; r=lambda x:round(x,3)
    def wt(i,word,default):
        for w in sw[i]:
            if w[0].lower().strip('.,:;¿?¡!').startswith(word): return w[1]
        return default
    caps=[]
    for ws in sw:
        ws2=[]; k=0
        while k<len(ws):
            w=ws[k]
            if w[0].lower()=='pol' and k+1<len(ws) and ws[k+1][0].strip('.,')=='25': ws2.append([CODE,w[1],ws[k+1][2],True]); k+=2; continue
            ws2.append([w[0].strip('.,:;').upper(),w[1],w[2],w[0][-1] in '.,:;?!']); k+=1
        cur=[]
        for w in ws2:
            cur.append(w[:3])
            if w[3] or len(cur)==3 or sum(len(x[0]) for x in cur)>13: caps.append(cur); cur=[]
        if cur: caps.append(cur)
    captions=[{'t0':r(max(0,c[0][1]-0.06)) if i else 0,'t1':r(caps[i+1][0][1]-0.06) if i+1<len(caps) else dur+1,'words':c} for i,c in enumerate(caps)]
    T1=S[1]-0.12; tA=wt(1,'escribe',S[1]+(E[1]-S[1])*0.5); tB=E[1]-0.05
    tTap=S[2]+0.35; tRes=tTap+0.3; tSt=tRes+0.7; tM=min(tSt+0.9,E[2]-0.1); tC=S[3]-0.1; tot=round(min(dur,E[-1])+0.55,2)
    rm=[[r(T1),1.3],[r(tA-0.3),2.6],[r(tA),2.95],[r(tB),5.15],[r(S[2]),5.3],[r(tTap-0.25),7.0],[r(tTap),7.3],[r(tTap+0.2),7.5],[r(tM-0.02),8.44],[r(tM),8.5],[r(tM+0.5),9.0],[tot,11.5]]
    xs=[a for a,_ in rm]; assert all(xs[i+1]>xs[i] for i in range(len(xs)-1)),rm
    ts=r(S[0]+(E[0]-S[0])*0.55)
    for q,w in enumerate(sw[0][1:],1):
        if sw[0][q-1][0][-1] in ',?:': ts=r(w[1]); break
    step=(tB-tA)/len(CODE); tiles=[[c,r(tA+0.08+k*step)] for k,c in enumerate(CODE)]
    te=wt(2,'envío',tSt+0.6)
    sp={'tot':tot,'rec':REC,'theme':j.get('theme',{}),'seed':len(j['id'])+ord(j['id'][-1]),'captions':captions,'rmap':rm,
        'chips':[[0,'1 · '+j['chips'][0]],[r(T1),'2 · '+j['chips'][1]],[r(S[2]-0.05),'3 · '+j['chips'][2]],[r(tC),'4 · '+j['chips'][3]]],
        'hook':{'label':'Tu pedido en Hacoo','frm':70.94,'to':53.20,'t_slash':ts},
        'phone':{'t_in':r(T1),'keys':[[r(T1),1000,1490,590],[r(tA-0.25),760,900,400],[r(tB),760,900,400],[r(tTap-0.05),740,900,800],[r(tTap+0.3),1010,1400,590],[r(tM-0.1),1010,1400,590],[r(tM+0.4),1150,1450,590]]},
        'tiles':tiles,'t_tiles_off':r(tTap-0.1),'tap':{'t':r(tTap),'x':935,'y':710},'result':{'t':r(tRes),'frm':70.94,'to':53.20},
        'stamp':{'t':r(tSt),'lines':['-25%','SIN FECHA LÍMITE']},'ship':{'t':r(te),'text':'ENVÍO GRATIS'},
        'close':{'t':r(tC),'word':j['close'],'handle':HANDLE,'emo':j.get('cemo','pin'),'burst':'fire'},
        'punches':[[ts,0.06]]+[[t_,0.02] for _,t_ in tiles]+[[r(tTap),0.03],[r(tRes),0.07],[r(tSt+0.12),0.08],[r(tC+0.15),0.05]]}
    json.dump(sp,open(f"{j['id']}.json",'w'),ensure_ascii=False); json.dump({'tot':tot,'voice':[[f"dp_{j['id']}",0.0]],'song':j.get('song','trend3')},open(f"{j['id']}_base.json",'w')); print(j['id'],'tot',tot,'S',[r(x) for x in S])
