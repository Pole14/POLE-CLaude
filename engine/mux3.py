import sys,json,subprocess
# mux2.py vid spec.json out music.mp3 offset [lufs]
vid,spec,out,M,off=sys.argv[1:6]; lufs=sys.argv[6] if len(sys.argv)>6 else '-22'  # Pol 11 nov: más alta (antes -28); música estable bajo la voz; Pol 9 nov: 'que se escuche un poquito más' (antes -31)
sp=json.load(open(spec)); V=__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__)))+'/voices/'
T=sp['tot']; ins=['-stream_loop','-1','-ss',str(off),'-t',str(T+0.5),'-i',M]
fc=[f'[1:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I={lufs}:TP=-3:LRA=11,aresample=48000,afade=t=in:d=0.12,afade=t=out:st={T-0.6}:d=0.6[m]']
for i,(f,t) in enumerate(sp['voice']):
    ins+=['-i',V+f+'.wav']; fc.append(f'[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(t*1000)}|{int(t*1000)}[a{i}]')
n=len(sp['voice'])
fc.append(''.join(f'[a{i}]' for i in range(n))+f'amix=inputs={n}:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000[vo]')
fc.append(f'[vo][m]amix=inputs=2:normalize=0:duration=longest,apad,atrim=0:{T},alimiter=limit=0.9[ao]')
subprocess.run(['ffmpeg','-v','error','-y','-i',vid]+ins+['-filter_complex',';'.join(fc),'-map','0:v','-map','[ao]','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',out],check=True)
print('ok',out)
