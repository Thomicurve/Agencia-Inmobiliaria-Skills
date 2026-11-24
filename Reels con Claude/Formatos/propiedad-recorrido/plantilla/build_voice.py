# Voz en off: sin eco (WPE) + limpieza + pausas acortadas + audios en secuencia
import numpy as np, wave, json, subprocess, os, soundfile as sf
from nara_wpe.wpe import wpe
from nara_wpe.utils import stft, istft
SR=48000; PAD_IN=0.10; PAD_OUT=0.16; MAXGAP=0.38
ORDER=[1,2,3,4,6,7,5,8,9,10]          # Intro, Planta baja, Lavadero, Arriba, Quincho, Pileta, Habitación, Ubicación, Apto crédito, Cierre
GAP={2:0.45,3:0.40,4:0.55,6:1.10,7:0.40,5:0.40,8:0.60,9:0.45,10:0.55}
START=0.45; TAIL=3.0
os.makedirs('voz/clean',exist_ok=True)
for i in range(1,11):
    x,sr=sf.read(f'voz/v{i}s.wav'); x=x[None,:]
    X=stft(x,size=1024,shift=256).transpose(2,0,1)
    Y=wpe(X,taps=12,delay=3,iterations=3,statistics_mode='full')
    y=istft(Y.transpose(1,2,0),size=1024,shift=256)[0][:x.shape[1]]
    y=0.6*y+0.4*x[0]   # suave: sin sonido "robótico"
    sf.write(f'voz/d{i}.wav',(y/np.abs(y).max()*0.7).astype(np.float32),sr,subtype='PCM_16')
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'voz/d{i}.wav','-af',
      'highpass=f=85,afftdn=nr=10:nf=-50:tn=1,agate=threshold=0.010:ratio=1.6:range=0.35:attack=3:release=180:knee=4,'
      'equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=2,equalizer=f=9000:t=h:w=1:g=1,'
      'deesser=i=0.35,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=3,loudnorm=I=-16:TP=-2:LRA=7',
      '-ar','48000','-ac','1',f'voz/clean/c{i}.wav'],check=True)
def load(p):
    w=wave.open(p); return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
def segs(x):
    hop=480; r=np.sqrt(np.convolve(x**2,np.ones(960)/960,'same'))[::hop]; db=20*np.log10(r+1e-9)
    act=db>db.max()-40; out=[]; s=None
    for k,a in enumerate(list(act)+[False]):
        t=k*hop/SR
        if a and s is None: s=t
        if not a and s is not None: out.append([s,t]); s=None
    m=[]
    for a,b in out:
        if m and a-m[-1][1]<0.12: m[-1][1]=b
        elif b-a>0.08: m.append([a,b])
    return m
words={i:json.load(open(f'voz/w{i}.json',encoding='utf-8'))['words'] for i in range(1,11)}
pieces=[]; t=START; tl={}; wordsout=[]
for c in ORDER:
    t+=GAP.get(c,0) if c!=ORDER[0] else 0
    x=load(f'voz/clean/c{c}.wav'); s=segs(x)
    cuts=[]; a=max(0,s[0][0]-PAD_IN)
    for k in range(len(s)-1):
        if s[k+1][0]-s[k][1]>MAXGAP: cuts.append([a,s[k][1]+0.11]); a=s[k+1][0]-(MAXGAP-0.11)
    cuts.append([a,min(len(x)/SR,s[-1][1]+PAD_OUT)])
    t0=t; mp=[]
    for a,b in cuts:
        mp.append([a,b,t]); pieces.append((c,a,b,t)); t+=b-a
    def remap(u):
        for a,b,tt in mp:
            if u<=b: return tt+max(0,u-a)
        return mp[-1][2]+(mp[-1][1]-mp[-1][0])
    for w in words[c]: wordsout.append({'w':w['w'],'start':round(remap(w['start']),3),'end':round(remap(w['end']),3),'clip':c})
    tl[c]=[round(t0+PAD_IN,3),round(t-PAD_OUT,3)]
    print(c,f"{t0+PAD_IN:6.2f}-{t-PAD_OUT:6.2f}",[(round(a,2),round(b,2)) for a,b,_ in mp])
TOTAL=round(t+TAIL,2)
out=np.zeros(int(TOTAL*SR)+SR,np.float32)
for c,a,b,tt in pieces:
    x=load(f'voz/clean/c{c}.wav'); y=x[int(a*SR):int(b*SR)].copy(); f=int(0.012*SR)
    y[:f]*=np.linspace(0,1,f); y[-f:]*=np.linspace(1,0,f); i0=int(tt*SR); out[i0:i0+len(y)]+=y
out=out[:int(TOTAL*SR)]
w=wave.open('voice.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(out,-1,1)*32767).astype(np.int16).tobytes()); w.close()
json.dump({'pieces':tl,'total':TOTAL,'words':wordsout},open('voice_timeline.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
print('TOTAL',TOTAL)
