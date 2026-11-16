#!/usr/bin/env python3
"""exb.py [ids] -> vídeo "explicativo animado" (ticket + sello, grabación en tarjeta, checklist, fichas del código, sello del descuento, cierre seguir).
Una sola locución (ElevenLabs con marcas de tiempo) -> subtítulos karaoke palabra a palabra y todos los tiempos del spec salen de la voz.
jobs.json: [{id, voice, song, theme, stamp1, sents:[gancho, código (con 'escribe pol 25'), solicitar+beneficio, ..., cierre]}]"""
import json,os,sys,base64,subprocess,urllib.request,re
SC=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V='/home/claude/pole-claude/voices/'
REC=SC+'/p25/rec.mp4'; CODE='POL25'
def api(path,data=None):
    r=urllib.request.Request('https://api.elevenlabs.io'+path,data=json.dumps(data).encode() if data else None,headers={'xi-api-key':open(SC+'/.el_key').read().strip(),'Content-Type':'application/json'})
    return urllib.request.urlopen(r,timeout=180)
vs=None
J=json.load(open('jobs.json')); ids=sys.argv[1:]
for j in J:
    if ids and j['id'] not in ids: continue
    text=' '.join(j['sents']); wav=f"{V}ex_{j['id']}.wav"; meta=f"{j['id']}_al.json"
    if not os.path.exists(meta):
        if vs is None: vs={v['name'].split(' ')[0]:v['voice_id'] for v in json.load(api('/v1/voices'))['voices']}
        body={'text':text,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.45,'similarity_boost':0.8,'style':0.3,'speed':1.1}}
        r=json.load(api(f"/v1/text-to-speech/{vs[j['voice']]}/with-timestamps?output_format=mp3_44100_128",body))
        open('/tmp/_e.mp3','wb').write(base64.b64decode(r['audio_base64']))
        subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/_e.mp3','-ar','48000','-ac','1',wav],check=True)
        json.dump(r['alignment'],open(meta,'w'))
    al=json.load(open(meta)); ch=al['characters']; cs=al['character_start_times_seconds']; ce=al['character_end_times_seconds']
    assert ''.join(ch)==text, 'alineación distinta del texto'
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wav],capture_output=True,text=True).stdout)
    # palabras con tiempos, por frase
    sw=[]; p=0
    for s in j['sents']:
        a=text.index(s,p); p=a+len(s); ws=[]
        for m in re.finditer(r'\S+',s):
            ws.append([m.group(0),round(cs[a+m.start()],3),round(ce[a+m.end()-1],3)])
        sw.append(ws)
    S=[w[0][1] for w in sw]; E=[w[-1][2] for w in sw]; n=len(sw)
    def wt(i,word,default):
        for w in sw[i]:
            if w[0].lower().strip('.,:;¿?¡!').startswith(word): return w[1]
        return default
    # subtítulos: trozos de hasta 3 palabras, corte en puntuación; "pol 25" -> POL25
    caps=[]
    for ws in sw:
        ws2=[]; k=0
        while k<len(ws):
            w=ws[k]
            if w[0].lower()=='pol' and k+1<len(ws) and ws[k+1][0].strip('.,')=='25': ws2.append([CODE,w[1],ws[k+1][2],ws[k+1][0][-1] in '.,:']); k+=2; continue
            ws2.append([w[0].strip('.,:;').upper(),w[1],w[2],w[0][-1] in '.,:;?!']); k+=1
        cur=[]
        for w in ws2:
            cur.append(w[:3])
            if w[3] or len(cur)==3 or sum(len(x[0]) for x in cur)>15: caps.append(cur); cur=[]
        if cur: caps.append(cur)
    captions=[]
    for i,c in enumerate(caps):
        t1=caps[i+1][0][1]-0.03 if i+1<len(caps) else dur+1
        c=[[w[0] if w[0].startswith('POL') else ('Hacoo'+w[0][5:].lower() if w[0].startswith('HACOO') else (w[0].capitalize() if q==0 else w[0].lower())),w[1],w[2]] for q,w in enumerate(c)]
        captions.append({'t0':round(max(0,c[0][1]-0.05),3) if i else 0,'t1':round(t1,3),'words':c})
    r=lambda x:round(x,3)
    T1=S[1]-0.05; tA=wt(1,'escribe',S[1]+(E[1]-S[1])*0.5); tB=E[1]-0.1
    tTap=S[2]+0.45; tDisc=tTap+0.7; tModal=min(tDisc+1.1,E[2]-0.2); tF=S[n-1]-0.05; tot=round(min(dur,E[-1])+0.7,2)
    rm=[[r(T1),1.3],[r(tA-0.3),2.6],[r(tA),2.95],[r(tB),5.15],[r(S[2]),5.3],[r(tTap-0.3),7.0],[r(tTap),7.3],[r(tTap+0.2),7.5],[r(tModal-0.02),8.44],[r(tModal),8.5],[r(tModal+0.5),9.0],[tot,11.5]]
    xs=[a for a,_ in rm]; assert all(xs[i+1]>xs[i] for i in range(len(xs)-1)),rm
    step=(tB-tA)/len(CODE)
    stamp_t=r(S[0]+(E[0]-S[0])*0.55)
    for w in sw[0][1:]:
        if sw[0][sw[0].index(w)-1][0][-1] in ',?': stamp_t=r(w[1]); break
    te=wt(2,'envío',None)
    sp={'rec':REC,'crop':[0,520,1180,880],'tot':tot,'total':'70,94 €','t_stamp':stamp_t,'stamp1':j.get('stamp1',['NO PAGUES','ESTO']),'t_scene2':r(T1),'t_modal':r(tModal),'t_follow':r(tF),'t_followed':r(tF+1.05),
        'rmap':rm,'code_letters':[[c,r(tA+0.12+k*step)] for k,c in enumerate(CODE)],'tiles_y':1080,'list_title':'TU PEDIDO EN HACOO',
        'items':[['Casilla del cupón',r(T1+0.1),r(tA-0.1)],['Código',r(tA-0.1),r(tB)],['Tocar Solicitar',r(tB),r(tTap+0.15)],['Descuento real',r(tTap+0.15),r(tDisc)]],
        't_tap':r(tTap),'t_tiles_off':r(tTap-0.15),'tap_xy':[810,715],'t_disc':r(tDisc),'stamp2':['-25%','SIN FECHA LÍMITE'],'t_ship':r(te) if te else tot+5,'stamp3':['ENVÍO GRATIS'],
        'handle':'@hacoorabatt','follow':'SEGUIR','followed':'SIGUIENDO','seo':'cupón descuento hacoo · código hacoo noviembre 2026','captions':captions,'theme':j.get('theme',{}),
        'price_label':'Tu pedido en Hacoo','price_from':'70,94 €','price_to':'53,20 €','sticker1':j.get('sticker1',['-25%','CÓDIGO']),
        'steps':[['Código',r(T1+0.1),r(tB)],['Solicitar',r(tB),r(tTap+0.15)],['Ahorra',r(tTap+0.15),r(tDisc)]],'code_label':'TU CÓDIGO','sticker2':['-25%','SIN LÍMITE'],'ship':'Envío gratis','save':j.get('save','Guárdalo')}
    json.dump(sp,open(f"{j['id']}.json",'w'),ensure_ascii=False)
    json.dump({'tot':tot,'voice':[[f"ex_{j['id']}",0.0]],'song':j.get('song','')},open(f"{j['id']}_base.json",'w'))
    print(j['id'],'tot',tot,'S',[r(x) for x in S])
