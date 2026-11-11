#!/usr/bin/env python3
"""ctts.py [ids] [--redo]: una frase de voz por escena -> voices/c13_<ID>_<i>.wav (ElevenLabs)."""
import json,os,subprocess,sys,urllib.request
SC=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V='/home/claude/pole-claude/voices/'
def api(path,data=None):
    r=urllib.request.Request('https://api.elevenlabs.io'+path,data=json.dumps(data).encode() if data else None,headers={'xi-api-key':open(SC+'/.el_key').read().strip(),'Content-Type':'application/json'})
    return urllib.request.urlopen(r,timeout=120)
J=json.load(open('cjobs.json')); ids=[a for a in sys.argv[1:] if not a.startswith('--')]
vs={v['name'].split(' ')[0]:v['voice_id'] for v in json.load(api('/v1/voices'))['voices']}
for j in J:
    if ids and j['id'] not in ids: continue
    for i,(txt,_) in enumerate(j['scenes']):
        out=f"{V}c13_{j['id']}_{i}.wav"
        if os.path.exists(out) and '--redo' not in sys.argv: continue
        prev=j['scenes'][i-1][0] if i else None; nxt=j['scenes'][i+1][0] if i+1<len(j['scenes']) else None
        body={'text':txt,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.45,'similarity_boost':0.8,'style':0.3,'speed':1.05 if j['lang']=='fr' else 1.1}}
        if prev: body['previous_text']=prev
        if nxt: body['next_text']=nxt
        a=api(f"/v1/text-to-speech/{vs[j['voice']]}?output_format=mp3_44100_128",body).read()
        open('tmp.mp3','wb').write(a)
        # recorta silencios de inicio y final
        subprocess.run(['ffmpeg','-v','error','-y','-i','tmp.mp3','-af','silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse','-ar','48000','-ac','1',out],check=True)
    print('ok',j['id'],flush=True)
