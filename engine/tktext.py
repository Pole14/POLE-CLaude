from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
_F={}
def font(w,size):
    k=(w,size)
    if k not in _F: _F[k]=ImageFont.truetype(D+f'fonts/tmp_w{w}_latin.ttf',size)
    return _F[k]
def parse(line):
    out=[]
    for p in line.split('|'):
        if not p: continue
        if p.startswith('emo:'): out.append(('e',p[4:]))
        elif p.startswith('hl:'): out.append(('t',p[3:]))
        else: out.append(('t',p))
    return out
def render_block(lines,size,mode,EMO,weight=600):
    """mode 'box': white rounded boxes, black text. 'shadow': white text, soft shadow."""
    f=font(weight,size); asc,desc=f.getmetrics(); lh=int(size*1.18)
    padx=int(size*.34); pady=int(size*.10)
    rows=[]
    for ln in lines:
        segs=parse(ln); wsum=0; items=[]
        for kind,v in segs:
            if kind=='t':
                w=f.getlength(v); items.append(('t',v,wsum)); wsum+=w
            else:
                es=int(size*1.0); items.append(('e',v,wsum+size*.06)); wsum+=es+size*.12
        rows.append((items,wsum))
    W=int(max(w for _,w in rows)+2*padx+20); H=lh*len(rows)+2*pady+20
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if mode=='box':
        r=int(size*.28)
        for i,(items,w) in enumerate(rows):
            x0=(W-w)/2-padx; y0=10+i*lh; x1=(W+w)/2+padx; y1=y0+lh+2*pady
            d.rounded_rectangle((x0,y0,x1,y1),r,fill=(255,255,255,255))
    txt=Image.new('RGBA',(W,H),(0,0,0,0)); td=ImageDraw.Draw(txt)
    col=(22,22,22,255) if mode=='box' else (255,255,255,255)
    for i,(items,w) in enumerate(rows):
        bx=(W-w)/2; by=10+pady+i*lh+(lh-(asc+desc))/2
        for kind,v,ox in items:
            if kind=='t': td.text((bx+ox,by),v,font=f,fill=col)
            else:
                e=EMO[v].resize((int(size),int(size)),Image.LANCZOS)
                txt.alpha_composite(e,(int(bx+ox),int(by+(asc+desc-size)/2+size*.04)))
    if mode=='shadow':
        a=txt.split()[3]; sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(a.point(lambda x:int(x*.55)))
        sh=sh.filter(ImageFilter.GaussianBlur(size*.06)); im.alpha_composite(sh,(0,int(size*.04)))
    im.alpha_composite(txt)
    return im

def outline_block(lines,size,EMO,w=700,st_div=9):
    f=ImageFont.truetype(D+f'fonts/tmp_w{w}_latin.ttf',size); st=max(3,round(size/st_div))
    asc,desc=f.getmetrics(); lh=int(size*1.08)
    rows=[]
    for ln in lines:
        items=[]; x=0
        for kind,v in parse(ln):
            if kind=='e': items.append(('e',v,x+size*.05)); x+=size*1.1
            else: items.append(('t',v,x)); x+=f.getlength(v)
        rows.append((items,x))
    W=int(max(r[1] for r in rows)+4*st+20); H=lh*len(rows)+4*st+20
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for i,(items,w_) in enumerate(rows):
        bx=(W-w_)/2; by=10+2*st+i*lh
        for k,v,ox in items:
            if k=='t': d.text((bx+ox,by),v,font=f,fill='white',stroke_width=st,stroke_fill='black')
            else:
                e=EMO[v].resize((size,size),Image.LANCZOS); im.alpha_composite(e,(int(bx+ox),int(by+(asc+desc-size)/2+size*.08)))
    if W>1000:
        s=1000/W; im=im.resize((1000,int(H*s)),Image.LANCZOS)
    return im
