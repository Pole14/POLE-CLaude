#!/usr/bin/env python3
"""stts.py DIR PREFIX [ids]: UNA sola locución por vídeo (prosodia continua) con marcas de tiempo por carácter;
se corta en 6 trozos justo en el silencio entre frases (fundido de 15 ms), sin recortar colas -> voz fluida."""
import json,os,sys,base64,subprocess,urllib.request
SC=os.path.dirname(os.path.abspath(__file__)); V='/home/claude/pole-claude/voices/'
D,P=sys.argv[1],sys.argv[2]; ids=sys.argv[3:]
def api(path,data=None):
    r=urllib.request.Request('https://api.elevenlabs.io'+path,data=json.dumps(data).encode() if data else None,headers={'xi-api-key':open(SC+'/.el_key').read().strip(),'Content-Type':'application/json'})
    return urllib.request.urlopen(r,timeout=180)
vs={v['name'].split(' ')[0]:v['voice_id'] for v in json.load(api('/v1/voices'))['voices']}
J=json.load(open(f'{SC}/{D}/cjobs.json'))
for j in J:
    if ids and j['id'] not in ids: continue
    sents=[s.strip() for s,_ in j['scenes']]
    sents=[s if s[-1] in '.?!' else s+'.' for s in sents]
    text=' '.join(sents); starts=[]; p=0
    for s in sents: starts.append(text.index(s,p)); p=starts[-1]+len(s)
    body={'text':text,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.45,'similarity_boost':0.8,'style':0.3,'speed':1.05 if j['lang']=='fr' else 1.1}}
    r=json.load(api(f"/v1/text-to-speech/{vs[j['voice']]}/with-timestamps?output_format=mp3_44100_128",body))
    open('/tmp/_v.mp3','wb').write(base64.b64decode(r['audio_base64']))
    al=r.get('normalized_alignment') or r['alignment']; cs=al['character_start_times_seconds']; ce=al['character_end_times_seconds']
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','/tmp/_v.mp3'],capture_output=True,text=True).stdout)
    def last_end(a,b):  # fin real de la última letra (no espacio) en [a,b)
        for k in range(b-1,a-1,-1):
            if text[k].strip() and text[k] not in '.?!,': return ce[k]
        return ce[b-1]
    def first_start(a):
        k=a
        while not text[k].strip(): k+=1
        return cs[k]
    cuts=[0.0]
    for i in range(1,len(sents)):
        e=last_end(starts[i-1],starts[i-1]+len(sents[i-1])); s=first_start(starts[i])
        cuts.append(round(e+(s-e)*0.5,3))
    cuts.append(dur)
    # recorta solo el silencio inicial del primer trozo
    cuts[0]=max(0,first_start(0)-0.05)
    for i in range(len(sents)):
        a,b=cuts[i],cuts[i+1]
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','/tmp/_v.mp3','-af',f'afade=t=in:d=0.015,afade=t=out:st={max(0,b-a-0.03)}:d=0.03','-ar','48000','-ac','1',f'{V}{P}{j["id"]}_{i}.wav'],check=True)
    print('ok',j['id'],[round(cuts[i+1]-cuts[i],2) for i in range(len(sents))],flush=True)
