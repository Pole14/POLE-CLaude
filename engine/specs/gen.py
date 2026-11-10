#!/usr/bin/env python3
"""Tanda de vídeos a partir de jobs.json.  Uso: gen.py tier | tts [ids] | align [ids] | build [ids]
tts solo genera si la cuenta de ElevenLabs es de pago (licencia comercial), salvo --force."""
import json, os, re, subprocess, sys, unicodedata, urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SC=os.path.dirname(HERE); V='/home/claude/pole-claude/voices/'
J=json.load(open('jobs.json')); JD={j['id']:j for j in J}
def key(): return open(SC+'/.el_key').read().strip()
def api(path,data=None):
    r=urllib.request.Request('https://api.elevenlabs.io'+path,data=json.dumps(data).encode() if data else None,headers={'xi-api-key':key(),'Content-Type':'application/json'})
    return urllib.request.urlopen(r,timeout=120)
def tier():
    d=json.load(api('/v1/user/subscription')); return d.get('tier'),d.get('character_count'),d.get('character_limit')
def norm(w):
    w=w.lower().strip(" .,;:!?¿¡\"«»()…")
    return w
def sel(args): return [JD[a] for a in args if a in JD] or J
cmd=sys.argv[1]; ids=[a for a in sys.argv[2:] if not a.startswith('--')]
if cmd=='tier': print(tier())
elif cmd=='tts':
    t=tier(); print('tier',t)
    if t[0]=='free' and '--force' not in sys.argv: sys.exit('cuenta gratis: sin licencia comercial, no genero')
    vs={v['name'].split(' ')[0]:v['voice_id'] for v in json.load(api('/v1/voices'))['voices']}
    for j in sel(ids):
        out=f"{V}v13_{j['id']}.wav"
        if os.path.exists(out) and '--redo' not in sys.argv: continue
        a=api(f"/v1/text-to-speech/{vs[j['voice']]}?output_format=mp3_44100_128",{'text':j['script'],'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.4,'similarity_boost':0.8,'style':0.35}}).read()
        open(f"v13_{j['id']}.mp3",'wb').write(a)
        subprocess.run(['ffmpeg','-v','error','-y','-i',f"v13_{j['id']}.mp3",'-ar','48000','-ac','1',out],check=True); print('tts',j['id'],len(a))
elif cmd=='align':
    import numpy as np; from faster_whisper import WhisperModel
    m=WhisperModel('small',compute_type='int8'); W=json.load(open('words.json')) if os.path.exists('words.json') else {}
    for j in sel(ids):
        vn=j.get('wav') or f"v13_{j['id']}"
        if not os.path.exists(V+vn+'.wav'): print('sin voz',j['id']); continue
        a=subprocess.run(['ffmpeg','-v','error','-i',V+vn+'.wav','-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout
        x=np.frombuffer(a,np.float32); segs,_=m.transcribe(x,language=j['lang'],word_timestamps=True)
        W[vn]={'dur':round(len(x)/16000,2),'w':[[w.word.strip(),round(float(w.start),2),round(float(w.end),2)] for s in segs for w in s.words]}
        print(j['id'],W[vn]['dur'],' '.join(w[0] for w in W[vn]['w']))
    json.dump(W,open('words.json','w'),ensure_ascii=False)
elif cmd=='build':
    sys.path.insert(0,SC+'/t11'); import sb
    EM=[('moneyfly','moneyfly','fire'),('gift','moneyfly','moneyfly'),('fire','moneyfly','gift'),('moneyfly','fire','moneyfly'),('moneyfly','gift','fire')]
    bad=[]
    for n,j in enumerate(sel(ids)):
        vn=j.get('wav') or f"v13_{j['id']}"
        if vn not in sb.WORDS: print('sin alinear',j['id']); continue
        W=sb.WORDS[vn]['w']; dur=sb.WORDS[vn]['dur']; A=j['anchors']
        def find(alts,after,before=1e9):
            for w,s,e in W:
                if s>after+0.01 and s<before:
                    nw=norm(w)
                    if any(nw==a or (a.isalpha() and len(a)>=4 and nw.startswith(a)) for a in alts): return s
            return None
        try:
            M={}; t=-1
            for k in ('h','ap','rev','s100','hasta','q1','drop','cta'):
                v=find(A[k],t)
                if v is None: raise Exception(f"ancla {k} {A[k]} no encontrada")
                M[k]=v; t=v
            amt=find(A['amt'],-1,M['h']) if A.get('amt') else None
            R=j['rows']; B=True
            hook=[(0.0,R['hook'][0],0),(0.0,R['hook'][1],0),(amt if amt is not None else 0.35,R['hook'][2],B)]
            tap=[(M['ap'],R['tap'][0],0)]+([(M['ap']+0.45,R['tap'][1],0)] if len(R['tap'])>1 else [])
            rows=dict(hook=hook,tap=tap,rev=R['rev'],c100=[(M['s100'],R['c100'][0],0),(M['hasta'],R['c100'][1],B)],
                      q=[(M['q1'],R['q'][0],0),(M['drop']-0.25,R['q'][1],B)],cta=[(M['cta'],R['cta'][0],0),(M['cta']+min(0.8,max(0.3,(dur-M['cta'])/2)),R['cta'][1],0)])
            sb.build(j['id'],j['lang'],vn,M,j['hookv'],rows,font=None,mark=j['mark'],end=j['end'],emo=EM[n%len(EM)],zf=[1.2,1.22,1.24][n%3],sizes=(84,112),song=j['song'])
        except Exception as e: bad.append((j['id'],str(e))); print('FALLO',j['id'],e)
    print('fallos',bad)
