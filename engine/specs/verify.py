#!/usr/bin/env python3
"""verify.py ID... -> duración, formato, loudness, transcripción whisper del audio final y hoja de fotogramas chk_ID.jpg"""
import json,subprocess,sys,cv2,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel('small',compute_type='int8'); JD={j['id']:j for j in json.load(open('jobs.json'))}
for n in sys.argv[1:]:
    f=f'out_{n}.mp4'; s=json.load(open(n+'.json'))
    p=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',f],capture_output=True,text=True).stdout)
    v=[x for x in p['streams'] if x['codec_type']=='video'][0]; a=[x for x in p['streams'] if x['codec_type']=='audio']
    lo=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    I=[l for l in lo.splitlines() if l.strip().startswith('I:')][-1].strip()
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout,np.float32)
    segs,_=m.transcribe(x,language=JD[n]['lang']); tx=' '.join(s_.text.strip() for s_ in segs)
    print(n,v['width'],v['height'],v['r_frame_rate'],'dur',round(float(p['format']['duration']),2),'spec',s['tot'],'audio',len(a),I,'MB',round(int(p['format']['size'])/1e6,1)); print('   ',tx)
    ts=[0,0.5,s['lines'][0]['t1']-0.3,s['texts'][0]['t0']+1.6,s['taps'][0]['t']+0.06,s['punches'][1]+0.02,s['punches'][1]+0.5,s['rects'][0]['t0']+1.3]
    if len(s['punches'])>2: ts+=[s['punches'][2]-0.4,s['punches'][2]+0.05,s['punches'][2]+0.6]
    ts+=[s['tot']-0.8,s['tot']-0.05]
    c=cv2.VideoCapture(f); ims=[]
    for t in ts:
        c.set(cv2.CAP_PROP_POS_FRAMES,int(round(t*60))); ok,im=c.read()
        if not ok: im=np.zeros((1920,1080,3),np.uint8)
        im=cv2.resize(im,(216,384)); cv2.putText(im,'%.2f'%t,(4,376),0,0.6,(0,160,0),2); ims.append(im)
    cv2.imwrite(f'chk_{n}.jpg',np.hstack(ims))
