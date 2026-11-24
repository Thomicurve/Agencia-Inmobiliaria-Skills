import json, subprocess, numpy as np, sys, os, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
S='src/'; FILES={unicodedata.normalize('NFC',f[:-4]):S+f for f in os.listdir(S) if f.endswith('.mp4')}
def fps(p):
    r=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate','-of','default=nw=1:nk=1',p],capture_output=True,text=True).stdout.strip().split()[0].strip(',')
    a,b=r.split('/'); return float(a)/float(b)
W,H=1080,1920; FS=W*H*3
m=json.load(open('montaje.json',encoding='utf-8')); FPS=m['fps']; N=int(round(m['total']*FPS))
def pchip(xs,ys):
    xs=np.array(xs,float); ys=np.array(ys,float); h=np.diff(xs); d=np.diff(ys)/h; n=len(xs)
    if n==2: return lambda x: ys[0]+(x-xs[0])*d[0]
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
out=sys.argv[1] if len(sys.argv)>1 else 'montaje.mp4'
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
   '-c:v','h264_nvenc','-preset','p6','-cq','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',out],stdin=subprocess.PIPE)
frame=0
for si,sc in enumerate(m['scenes']):
    src=FILES[unicodedata.normalize('NFC',sc['src'])]; SFPS=fps(src)
    k=sc['k']; f=pchip([a for a,b in k],[b for a,b in k])
    o0=frame; o1=int(round(k[-1][0]*FPS)) if si<len(m['scenes'])-1 else N
    ts=[f(o/FPS) for o in range(o0,o1)]
    wins=[]
    for j,t in enumerate(ts):
        adv=abs(f((o0+j+1)/FPS)-t)*SFPS
        half=max(0.0,0.5*adv*0.5)
        c=t*SFPS; wins.append((int(round(c-half)),int(round(c+half))))
    lo=max(0,min(a for a,b in wins)); hi=max(b for a,b in wins)
    ss=max(0,lo/SFPS-0.05)
    dec=subprocess.Popen(['ffmpeg','-v','error','-ss',f'{ss:.3f}','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    cur=int(round(ss*SFPS)); buf={}; last=None
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
    print(f"{k[0][0]:6.2f}-{k[-1][0]:6.2f}s  {sc['name']:<32} {sc['src']:<24} {k[0][1]:.2f}-{k[-1][1]:.2f}  x{sp:.2f}",flush=True)
enc.stdin.close(); enc.wait(); print('frames',frame,'of',N)
