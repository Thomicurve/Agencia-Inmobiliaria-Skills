# Voz: audios en off (sin eco, limpios, pausas acortadas) + audio de las tomas habladas (mejorado, en sincronía)
import numpy as np, json, subprocess, os, sys, soundfile as sf, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
from nara_wpe.wpe import wpe
from nara_wpe.utils import stft, istft
SR=48000; PAD_IN=0.10; PAD_OUT=0.16; MAXGAP=0.26
# carpeta de tomas: proyecto.json → "tomas" (relativa a la carpeta de la propiedad)
PROY=json.load(open('../proyecto.json',encoding='utf-8'))
T=os.path.abspath(os.path.join('..','..','..',PROY['tomas']))+'/'
def nf(s): return unicodedata.normalize('NFC',s)
SRCF={nf(f):f for f in os.listdir(T)}
# EDITAR: orden de la voz. (id, archivo, tipo 'vo'|'talk', pausa antes en s, [[in,out],...] solo para 'talk')
SEQ=[('ubic','Ubicación.m4a','vo',0,None),
     ('integ','Todo integrado.m4a','vo',0.30,None),
     ('toil','Toilette.m4a','vo',0.34,None),
     ('suite','Suite.m4a','vo',0.30,None),
     ('seg','Segundo dormitorio y baño.m4a','vo',0.20,None),
     ('quin','El quincho y pileta.m4a','vo',0.38,None),
     ('hab','Baño y hab independiente.m4a','vo',0.22,None),
     ('apto','Apto crédito.m4a','vo',0.34,None),
     ('cta','Cta.m4a','vo',0.42,None)]
# EDITAR: id → nombre del .json de palabras en voz/ (sale de preparar_tomas.py)
WJ={'hook':'Hook','ubic':'Ubicación','integ':'Todo integrado','luz':'HabladoLuminosidad','toil':'Toilette','suite':'SuiteVoz',
    'seg':'Segundo dormitorio y baño','quin':'El quincho y pileta','hab':'Baño y hab independiente','apto':'Apto crédito','cta':'Cta'}
# START: 1.6 si arranca con voz en off (deja que el precio aparezca); 0 si arranca con toma hablada
START=1.6; TAIL=2.8
os.makedirs('voz/clean',exist_ok=True)
CHAIN=('highpass=f=85,afftdn=nr=12:nf=-50:tn=1,agate=threshold=0.010:ratio=1.6:range=0.35:attack=3:release=180:knee=4,'
       'equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=2,equalizer=f=9000:t=h:w=1:g=1,'
       'deesser=i=0.35,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=3,loudnorm=I=-16:TP=-2:LRA=7')
def clean(i,f,kind):
    raw=f'voz/raw_{i}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',T+SRCF[nf(f)],'-vn','-ac','1','-ar',str(SR),raw],check=True)
    x,sr=sf.read(raw); xx=x[None,:]
    X=stft(xx,size=1024,shift=256).transpose(2,0,1)
    Y=wpe(X,taps=12,delay=3,iterations=3,statistics_mode='full')
    y=istft(Y.transpose(1,2,0),size=1024,shift=256)[0][:len(x)]
    mix=0.55 if kind=='talk' else 0.6     # tomas habladas: más reverberación de la casa
    y=mix*y+(1-mix)*x
    sf.write(f'voz/d_{i}.wav',(y/np.abs(y).max()*0.7).astype(np.float32),sr,subtype='PCM_16')
    ch=CHAIN.replace('nr=12','nr=16') if kind=='talk' else CHAIN
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'voz/d_{i}.wav','-af',ch,'-ar',str(SR),'-ac','1',f'voz/clean/{i}.wav'],check=True)
    return sf.read(f'voz/clean/{i}.wav')[0].astype(np.float32)
def segs(x):
    hop=480; r=np.sqrt(np.convolve(x**2,np.ones(960)/960,'same'))[::hop]; db=20*np.log10(r+1e-9)
    act=db>db.max()-38; out=[]; s=None
    for k,a in enumerate(list(act)+[False]):
        t=k*hop/SR
        if a and s is None: s=t
        if not a and s is not None: out.append([s,t]); s=None
    m=[]
    for a,b in out:
        if m and a-m[-1][1]<0.12: m[-1][1]=b
        elif b-a>0.08: m.append([a,b])
    return m
pieces=[]; t=START; tl={}; wordsout=[]
for i,f,kind,gap,io in SEQ:
    t+=gap
    x=clean(i,f,kind)
    JF={nf(g):g for g in os.listdir('voz')}; W=json.load(open('voz/'+JF[nf(WJ[i]+'.json')],encoding='utf-8'))['words']
    if kind=='talk':
        t0=t; mp=[]
        for a,b in io: mp.append([a,b,t]); pieces.append((i,a,b,t,kind)); t+=b-a
        tl[i]=[round(t0,3),round(t,3)]
    else:
        s=segs(x); cuts=[]; a=max(0,s[0][0]-PAD_IN)
        for k in range(len(s)-1):
            if s[k+1][0]-s[k][1]>MAXGAP: cuts.append([a,s[k][1]+0.10]); a=s[k+1][0]-(MAXGAP-0.10)
        cuts.append([a,min(len(x)/SR,s[-1][1]+PAD_OUT)])
        t0=t; mp=[]
        for a,b in cuts: mp.append([a,b,t]); pieces.append((i,a,b,t,kind)); t+=b-a
        tl[i]=[round(t0+PAD_IN,3),round(t-PAD_OUT,3)]
    def remap(u):
        for a,b,tt in mp:
            if u<a: return tt
            if u<=b: return tt+(u-a)
        return mp[-1][2]+(mp[-1][1]-mp[-1][0])
    for w in W:
        if i=='luz' and w['w'].strip(',.').lower() in ('como','podemos','ver'): continue
        if kind=='talk' and not any(a-0.05<=w['start']<=b-0.05 for a,b in io): continue
        wordsout.append({'w':w['w'],'start':round(remap(w['start']),3),'end':round(remap(w['end']),3),'clip':i})
    print(f"{i:6} {tl[i][0]:6.2f}-{tl[i][1]:6.2f}", [(round(a,2),round(b,2)) for a,b,_ in mp])
TOTAL=round(t+TAIL,2)
out=np.zeros(int(TOTAL*SR)+SR,np.float32)
for i,a,b,tt,kind in pieces:
    x=sf.read(f'voz/clean/{i}.wav')[0].astype(np.float32); y=x[int(a*SR):int(b*SR)].copy(); f=int((0.05 if kind=='talk' else 0.012)*SR)
    f2=int(0.02*SR) if kind=='talk' else f; y[:f2]*=np.linspace(0,1,f2); y[-f2:]*=np.linspace(1,0,f2); i0=int(tt*SR); out[i0:i0+len(y)]+=y
out=out[:int(TOTAL*SR)]
sf.write('voice.wav',np.clip(out,-1,1),SR,subtype='PCM_16')
json.dump({'pieces':tl,'total':TOTAL,'words':wordsout},open('voice_timeline.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
print('TOTAL',TOTAL)
for w in wordsout: print(f"{w['clip']}:{w['w']}@{w['start']:.2f}",end='  ')
