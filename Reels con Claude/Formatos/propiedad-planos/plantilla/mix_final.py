# Mezcla: voz en off + efectos + música Lo-Fi con ducking + máster -14 LUFS
import json, re, subprocess, numpy as np
SR=48000
VT=json.load(open('voice_timeline.json',encoding='utf-8')); DUR=VT['total']
W={w['w'].strip(',.').lower():w['start'] for w in VT['words'] if w['start']>53}
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True,check=True).stdout,np.float32).reshape(-1,2).copy()
def lufs(x):
    x.astype(np.float32).tofile('_t.f32')
    r=subprocess.run(['ffmpeg','-hide_banner','-f','f32le','-ar',str(SR),'-ac','2','-i','_t.f32','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1])
n=int(DUR*SR); voz=load('voice.wav')[:n]; voz=np.pad(voz,((0,n-len(voz)),(0,0)))
mix=voz.copy()
tR=56.01
# EDITAR: efectos (archivo, segundo, dB). Un whoosh por cambio de escena, uiclick en cada ✓, riser+impact+braaam en el CTA (tR)
EV=[('impact',0.12,-27),('whoosh',1.15,-29),('uiclick',4.40,-29),('uiclick',8.59,-28),
    ('whoosh',9.95,-27),('whoosh',18.55,-28),('whoosh',23.69,-25),('whoosh',32.10,-29),('whoosh',36.39,-25),('whoosh',43.15,-29),
    ('whoosh',46.71,-27),('uiclick',47.69,-26),('uiclick',50.39,-26),('whoosh',53.65,-27),
    ('riser',tR-2.75,-27),('impact',tR-0.03,-18),('braaam',tR+0.05,-30),('uiclick',tR+0.35+1.4,-24)]
for f,t,db in EV:
    s=load(f'sfx/{f}.wav'); i=int(t*SR); j=min(n,i+len(s)); mix[i:j]+=s[:j-i]*10**(db/20)
mus=load('musica.wav')[:n]; mus=np.pad(mus,((0,n-len(mus)),(0,0)))
win=int(0.02*SR); env=np.sqrt(np.convolve(voz[:,0]**2,np.ones(win)/win,'same')); act=(env>10**(-38/20)).astype(np.float32)
at,rl=np.exp(-1/(0.04*SR)),np.exp(-1/(0.45*SR)); duck=np.empty(n,np.float32); g=0.0
for k in range(n):
    c=at if act[k]>g else rl; g=c*g+(1-c)*act[k]; duck[k]=g
base=lufs(voz)-12-lufs(mus); t=np.arange(n)/SR
gain=10**(base/20)*10**(-7*duck/20)*np.clip(t/0.6,0,1)*np.clip((DUR-t)/2.0,0,1)
# después de la voz final, la música sube un poco para cerrar
gain*=1+0.4*np.clip((t-58.6)/0.8,0,1)*np.clip((DUR-t)/2.0,0,1)
mix+=mus*gain[:,None]
mix.astype(np.float32).tofile('_m.f32')
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','_m.f32','-c:a','pcm_f32le','mezcla.wav'],check=True)
m=subprocess.run(['ffmpeg','-hide_banner','-i','mezcla.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
j=json.loads(m[m.rindex('{'):m.rindex('}')+1])
af=(f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
    f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000")
subprocess.run(['ffmpeg','-v','error','-y','-i','mezcla.wav','-af',af,'-c:a','pcm_s24le','master.wav'],check=True)
print('musica base',round(base,1),'dB')
