import json,subprocess,sys,cv2,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel('small',compute_type='int8'); rows=[]
out=sys.argv[1]
for a in sys.argv[2:]:
    d,n=a.split('/'); f=f'{d}/out_{n}.mp4'; s=json.load(open(f'{d}/{n}.json'))
    lo=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    I=[l for l in lo.splitlines() if l.strip().startswith('I:')][-1].strip()
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout,np.float32)
    lang='fr' if n.startswith('F') else ('en' if n.startswith('E') else 'es')
    seg,_=m.transcribe(x,language=lang); print(n,round(len(x)/16000,2),'spec',s['tot'],I,'|',' '.join(q.text.strip() for q in seg),flush=True)
    c=cv2.VideoCapture(f); N=int(c.get(7)); ims=[]
    for t in np.linspace(0,(N-3)/60,10):
        c.set(1,int(t*60)); ok,im=c.read()
        if not ok: im=np.zeros((1920,1080,3),np.uint8)
        im=cv2.resize(im,(200,356)); cv2.putText(im,'%.1f'%t,(4,348),0,0.6,(0,160,0),2); ims.append(im)
    rows.append(np.hstack(ims))
cv2.imwrite(out,np.vstack(rows))
