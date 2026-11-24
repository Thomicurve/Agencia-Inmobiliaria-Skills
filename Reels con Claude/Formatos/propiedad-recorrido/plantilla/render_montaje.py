import json, subprocess, numpy as np, sys
S='src/'   # clips SDR que deja preparar_tomas.py
# EDITAR: letra de cada toma de recorrido → archivo en src/
SRC={'A':S+'recorrida-parte-abajo.mp4','B':S+'recorrida-parte-arriba.mp4','Q':S+'recorrida-quincho.mp4'}
SFPS=60000/1001; W,H=1080,1920; FS=W*H*3
m=json.load(open('montaje.json',encoding='utf-8')); FPS=m['fps']; N=int(round(m['total']*FPS))
def pchip(xs,ys):
    xs=np.array(xs,float); ys=np.array(ys,float); h=np.diff(xs); d=np.diff(ys)/h; n=len(xs)
    if n==2: return lambda x: np.interp(x,xs,ys)
    mm=np.zeros(n); mm[0]=d[0]; mm[-1]=d[-1]
    for i in range(1,n-1):
        if d[i-1]*d[i]<=0: mm[i]=0
        else:
            w1=2*h[i]+h[i-1]; w2=h[i]+2*h[i-1]; mm[i]=(w1+w2)/(w1/d[i-1]+w2/d[i])
    def f(x):
        i=min(max(np.searchsorted(xs,x)-1,0),n-2); t=(x-xs[i])/h[i]
        h00=2*t**3-3*t**2+1; h10=t**3-2*t**2+t; h01=-2*t**3+3*t**2; h11=t**3-t**2
        return h00*ys[i]+h10*h[i]*mm[i]+h01*ys[i+1]+h11*h[i]*mm[i+1]
    return f
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
   '-c:v','h264_nvenc','-preset','p6','-cq','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','montaje.mp4'],stdin=subprocess.PIPE)
frame=0; log=[]
for sc in m['scenes']:
    k=sc['k']; f=pchip([a for a,b in k],[b for a,b in k])
    o0=int(round(k[0][0]*FPS)); o1=int(round(k[-1][0]*FPS)) if sc is not m['scenes'][-1] else N
    ts=[f(o/FPS) for o in range(o0,o1)]
    # source frame windows (motion blur: shutter = half of advance)
    wins=[]
    for j,t in enumerate(ts):
        adv=abs((f((o0+j+1)/FPS)-t))*SFPS  # src frames per out frame
        half=max(0.0,0.5*adv*0.5)
        c=t*SFPS; wins.append((int(round(c-half)),int(round(c+half))))
    lo=max(0,min(a for a,b in wins)); hi=max(b for a,b in wins)
    dec=subprocess.Popen(['ffmpeg','-v','error','-ss',f'{max(0,lo/SFPS-0.05):.3f}','-i',SRC[sc['src']],'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    # figure exact start frame index after seek: use pts by counting from lo (accurate seek in ffmpeg>=2.1 with -ss before -i decodes from that time)
    cur=int(round(max(0,lo/SFPS-0.05)*SFPS)); buf={}
    last=None
    for a,b in wins:
        while cur<=b:
            raw=dec.stdout.read(FS)
            if len(raw)<FS: break
            buf[cur]=np.frombuffer(raw,np.uint8); cur+=1
        for kk in [x for x in buf if x<a]: del buf[kk]
        sel=[buf[x] for x in range(a,b+1) if x in buf]
        if not sel: sel=[last] if last is not None else [buf[max(buf)]]
        img=sel[0] if len(sel)==1 else (np.sum([s.astype(np.uint16) for s in sel],axis=0)//len(sel)).astype(np.uint8)
        last=img; enc.stdin.write(img.tobytes()); frame+=1
    dec.stdout.close(); dec.kill()
    sp=(k[-1][1]-k[0][1])/(k[-1][0]-k[0][0])
    log.append(f"{k[0][0]:6.2f}-{k[-1][0]:6.2f}s  {sc['name']:<28} {sc['src']} {k[0][1]:.1f}-{k[-1][1]:.1f}  x{sp:.2f}")
    print(log[-1],flush=True)
enc.stdin.close(); enc.wait(); print('frames',frame,'of',N)
