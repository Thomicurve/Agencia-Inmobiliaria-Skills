# PLANTILLA · gráficos del reel (HyperFrames 1080x1920) · fábrica de reels
# Datos fijos (precio, dirección, localidad, palabra del CTA) salen de ../../../propiedad.json.
# EDITAR POR REEL (buscar «EDITAR»): FRASES, etiquetas de zona, tarjetas de datos y los ids de pieza (VT["pieces"][...]).
import json, re, unicodedata, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "graficos", "index.html")
VT = json.load(open(os.path.join(HERE, "voice_timeline.json"), encoding="utf-8"))
TOTAL = VT["total"]
words = VT["words"]

# ---- datos de la propiedad (no editar acá: editar propiedad.json) ----
PROP = json.load(open(os.path.join(HERE, "..", "..", "..", "propiedad.json"), encoding="utf-8"))
PRECIO = int(PROP["precio"]); MONEDA = PROP.get("moneda", "USD")
DIRECCION = PROP["direccion"]; LOCALIDAD = PROP["localidad"]; CTA_WORD = PROP["palabra_cta"]
PRECIO_TXT = f"{PRECIO:,}".replace(",", ".")  # 250000 → 250.000
BIG_PX = min(190, int(900 / (0.72 * len(CTA_WORD))))  # palabra gigante del CTA: se achica si es larga
PRECIO_K = str(PRECIO // 1000)  # cómo se dice en la voz: «<precio> mil»
D = PROP.get("datos", {})
ANIOS = D.get("antiguedad_anios", 0); M2_LOTE = D.get("m2_lote", 0); M2_CUB = D.get("m2_cubiertos", 0)
PERMUTA = PROP.get("permuta", "")  # texto debajo de «Acepta permuta»

T_CTA_MIN = 0  # se fija abajo cuando se conoce la pieza del CTA
# Whisper pone mal el inicio de la primera palabra de cada audio: se corrige con la pista real
seen = set()
for w in words:
    if w["clip"] not in seen:
        seen.add(w["clip"]); w["start"] = VT["pieces"][str(w["clip"])][0]
    w["w"] = {"pisero": "pizzero", "fuera,": "afuera,", "llevas": "llevás"}.get(w["w"], w["w"])

def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)))

# Frases: '|' separa trozos, *clave*. Las frases entre [] no se muestran (las dice un gráfico).
# EDITAR: guion en pantalla (EJEMPLO genérico: reemplazar por lo que se dice en la voz). "|" separa trozos, *clave*, [frase] = no se muestra (la dice un gráfico)
FRASES = """[Por <precio> mil dólares]
te llevás | esta casa
con *pileta* en <Localidad>.
Abajo, cocina, living y comedor
en un solo *ambiente*,
con *ventanales* en toda la planta,
*luz* todo el día.
*Arriba* dos dormitorios,
el principal en *suite*,
con *vestidor* y baño propio.
Pero el gran *atractivo* | está afuera,
*quincho* con parrilla
[Pileta y un lote de <m² lote> metros]
con *verde* de sobra.
Ubicada sobre | <calle> *<nombre>*,
[tiene solo <años> años y <m² cubiertos> metros cubiertos en dos plantas]
[Esta propiedad es apto crédito y se acepta permuta]
[Si te interesó, comentame la palabra <PALABRA> y te paso toda la información]"""

chunks = []  # (start, end, [(text, is_key)], hidden)
wi = 0
for line in FRASES.splitlines():
    hidden = line.startswith("[")
    line = line.strip("[]")
    for part in line.split("|"):
        toks = part.split()
        items = []
        st = None; en = None
        for t in toks:
            key = t.startswith("*") or t.strip("¡,.:").startswith("*")
            clean = t.replace("*", "")
            # avanzar hasta la palabra que coincide
            while norm(words[wi]["w"]) != norm(clean) and not (norm(clean) == PRECIO_K and PRECIO_K in words[wi]["w"]):
                wi += 1
            w = words[wi]; wi += 1
            st = w["start"] if st is None else st; en = w["end"]
            items.append((clean, key))
        chunks.append([st, en, items, hidden])
# tiempos de salida: hasta el siguiente trozo (máx. 0,55 s tras la última palabra)
for i, c in enumerate(chunks):
    nxt = chunks[i + 1][0] if i + 1 < len(chunks) else TOTAL
    c[1] = min(nxt - 0.02, c[1] + 0.55)
    c[0] = max(0, c[0] - 0.06)

H = []  # html
J = []  # js
def add(s): J.append(s)

cap_html = []
for i, (st, en, items, hidden) in enumerate(chunks):
    if hidden:
        continue
    small_before = [t for t, k in items if not k]
    has_key = any(k for t, k in items)
    parts = []
    if has_key:
        kidx = [j for j, (t, k) in enumerate(items) if k][0]
        pre = " ".join(t for t, k in items[:kidx])
        key = items[kidx][0]
        post = " ".join(t for t, k in items[kidx + 1:])
        # puntuación pegada a la clave pasa a texto chico
        m = re.match(r"^([¡]?)(.+?)([,.:!]?)$", key)
        key_core = m.group(2).replace("¡", "")
        if m.group(1): pre = (pre + " ¡").strip()
        if pre: parts.append(f'<div class="sm" id="c{i}a">{pre}</div>')
        parts.append(f'<div class="key" id="c{i}k">{key_core}</div>')
        if post: parts.append(f'<div class="sm" id="c{i}b">{post}</div>')
        add(f'tl.fromTo("#cap{i}",{{opacity:0}},{{opacity:1,duration:.01}},{st:.3f});')
        if pre:
            add(f'tl.fromTo("#c{i}a",{{opacity:0,y:18,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.35,ease:"power3.out"}},{st:.3f});')
        add(f'tl.fromTo("#c{i}k",{{opacity:0,y:26,scale:.94,filter:"blur(14px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.55,ease:"power3.out"}},{st + (0.12 if pre else 0):.3f});')
        if post:
            add(f'tl.fromTo("#c{i}b",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{st + 0.3:.3f});')
    else:
        text = " ".join(t for t, k in items)
        parts.append(f'<div class="sm solo" id="c{i}a">{text}</div>')
        add(f'tl.fromTo("#cap{i}",{{opacity:0}},{{opacity:1,duration:.01}},{st:.3f});')
        add(f'tl.fromTo("#c{i}a",{{opacity:0,y:18,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.35,ease:"power3.out"}},{st:.3f});')
    add(f'tl.to("#cap{i}",{{opacity:0,y:-10,duration:.16,ease:"power2.in"}},{en - 0.16:.3f});')
    cap_html.append(f'<div class="cap" id="cap{i}">{"".join(parts)}</div>')

# ---------- Cartel fijo (precio + dirección) ----------
add('tl.fromTo("#price",{opacity:0,y:640,scale:1.75,filter:"blur(18px)"},{opacity:1,y:640,scale:1.6,filter:"blur(0px)",duration:.5,ease:"power3.out"},0.42);')
add('const pv={v:0}; tl.to(pv,{v:'+str(PRECIO)+',duration:1.15,ease:"power2.out",onUpdate:()=>{document.querySelector("#pnum").textContent=Math.round(pv.v).toLocaleString("es-AR");}},0.45);')
add('tl.to("#price",{y:0,scale:1,duration:.9,ease:"power3.inOut"},2.15);')
add('tl.fromTo("#topshade",{opacity:0},{opacity:1,duration:.8,ease:"sine.out"},2.2);')
add('tl.fromTo("#rule",{scaleX:0},{scaleX:1,duration:.6,ease:"power3.out"},2.85);')
add('tl.fromTo("#addr",{opacity:0,y:12,filter:"blur(8px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.6,ease:"power3.out"},3.0);')

add('tl.fromTo("#capbg",{opacity:0},{opacity:1,duration:.6,ease:"sine.out"},1.7);')
add('tl.to("#capbg",{opacity:0,duration:.5,ease:"sine.in"},54.2);')
# ---------- Etiquetas de zona (EDITAR: ids de pieza y textos) ----------
zones = [("z1", "PLANTA BAJA", 5.75, 9.4), ("z2", "PLANTA ALTA", 20.95, 24.0), ("z3", "EXTERIOR", 29.35, 32.6)]
zone_html = []
for zid, txt, a, b in zones:
    zone_html.append(f'<div class="zone" id="{zid}"><span class="zl" id="{zid}l"></span><span class="zt">{txt}</span><span class="zl" id="{zid}r"></span></div>')
    add(f'tl.fromTo("#{zid}",{{opacity:0,y:-8}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{a});')
    add(f'tl.fromTo("#{zid}l",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power3.out"}},{a + .1});')
    add(f'tl.fromTo("#{zid}r",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power3.out"}},{a + .1});')
    add(f'tl.to("#{zid}",{{opacity:0,duration:.4,ease:"power2.in"}},{b});')

# ---------- Tarjetas de datos (EDITAR: palabras que disparan cada dato) ----------
def wt(txt, after=0):  # momento en que se dice una palabra
    return [w["start"] for w in words if norm(w["w"]) == norm(txt) and w["start"] >= after][0]
def card_in(cid, t):
    add(f'tl.fromTo("#{cid}",{{opacity:0,y:80,scale:.92,filter:"blur(18px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:1.0,ease:VB(0.07)}},{t:.3f});')
def card_out(cid, t):
    add(f'tl.to("#{cid}",{{opacity:0,y:-36,filter:"blur(14px)",duration:.35,ease:"power2.in"}},{t:.3f});')
def count(el, to, t, dur=1.0, dec=False):
    add(f'(()=>{{const o={{v:0}};tl.to(o,{{v:{to},duration:{dur},ease:"power2.out",onUpdate:()=>{{document.querySelector("#{el}").textContent=Math.round(o.v).toLocaleString("es-AR");}}}},{t:.3f});}})();')
# m² de lote — propiedad.json
tP = wt("Pileta", 34); t432 = wt(str(M2_LOTE), 34)
card_in("sLote", tP - 0.05)
add(f'tl.fromTo("#sLoteA",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{tP + 0.15:.3f});')
count("nLote", M2_LOTE, t432 - 0.05, 1.1)
add(f'tl.fromTo("#sw1",{{x:-900}},{{x:900,duration:.9,ease:"power2.inOut"}},{t432 + 0.9:.3f});')
card_out("sLote", wt("con", t432) - 0.25)
# años · m² cubiertos — propiedad.json
t4 = wt(str(ANIOS), 48); t149 = wt(str(M2_CUB), 48)
card_in("sDatos", wt("tiene", 48) - 0.1)
count("nAnios", ANIOS, t4 - 0.05, 0.6)
add(f'tl.fromTo("#dA",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{t4:.3f});')
add(f'tl.fromTo("#dSep",{{scaleY:0}},{{scaleY:1,duration:.5,ease:"power3.out"}},{t149 - 0.3:.3f});')
add(f'tl.fromTo("#dB",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{t149 - 0.1:.3f});')
count("nM2", M2_CUB, t149 - 0.05, 1.0)
add(f'tl.fromTo("#dC",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{wt("dos", 52) - 0.05:.3f});')
add(f'tl.fromTo("#sw2",{{x:-900}},{{x:900,duration:.9,ease:"power2.inOut"}},{wt("plantas", 52):.3f});')
card_out("sDatos", 54.15)
# ---------- Tarjeta apto crédito / permuta ----------
tA = wt("apto", 54); tPm = wt("permuta", 54); tDp = wt("departamento", 54)
card_in("card", 54.35)
add(f'tl.fromTo("#r1",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{tA - 0.1:.3f});')
add(f'tl.fromTo("#k1",{{scale:0,rotation:-40}},{{scale:1,rotation:0,duration:.9,ease:VB(0.06)}},{tA:.3f});')
add(f'tl.fromTo("#r2",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{tPm - 0.15:.3f});')
add(f'tl.fromTo("#k2",{{scale:0,rotation:-40}},{{scale:1,rotation:0,duration:.9,ease:VB(0.06)}},{tPm - 0.05:.3f});')
add(f'tl.fromTo("#r3",{{opacity:0}},{{opacity:1,duration:.4,ease:"power2.out"}},{tDp:.3f});')
add(f'tl.fromTo("#sweep",{{x:-900}},{{x:900,duration:.9,ease:"power2.inOut"}},{tA + 0.6:.3f});')
add(f'tl.fromTo("#sweep",{{x:-900}},{{x:900,duration:.9,ease:"power2.inOut",immediateRender:false}},{tDp + 0.6:.3f});')
card_out("card", 61.15)

# ---------- CTA ----------
CTA = 61.35
T_CTA_MIN = VT["pieces"]["10"][0] - 0.5
tSi = VT["pieces"]["10"][0]; tCom = wt("comentame", T_CTA_MIN); tRol = wt(CTA_WORD, T_CTA_MIN); tInf = wt("toda", T_CTA_MIN)
add(f'tl.fromTo("#dim",{{opacity:0}},{{opacity:1,duration:.7,ease:"sine.out"}},{CTA});')
add(f'tl.to("#topshade",{{opacity:0,duration:.6}},{CTA});')
add(f'tl.fromTo("#cta1",{{opacity:0,y:20,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"power3.out"}},{tSi - 0.05:.3f});')
add(f'tl.fromTo("#cta2",{{opacity:0,y:20,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"power3.out"}},{tCom - 0.1:.3f});')
word = CTA_WORD.upper()
letters = "".join(f'<span class="L" id="L{j}">{ch}</span>' for j, ch in enumerate(word))
T0 = tRol - 0.15
add(f'tl.fromTo("#bigword",{{opacity:0,scale:.82,filter:"blur(12px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.75,ease:VB(0.08)}},{T0 - 0.2:.3f});')
for j in range(len(word)):
    add(f'tl.fromTo("#L{j}",{{opacity:0,y:120,scale:.4,filter:"blur(16px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:1.0,ease:VB(0.09)}},{T0 + j * 0.065:.3f});')
add(f'tl.fromTo("#glow",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.9,ease:"power2.out"}},{T0 + 0.1:.3f});')
add(f'tl.fromTo("#ring",{{opacity:.9,scale:.5}},{{opacity:0,scale:1.6,duration:1.1,ease:"power2.out",immediateRender:false}},{T0 + 0.45:.3f});')
add(f'tl.fromTo("#shine",{{x:-700}},{{x:700,duration:.8,ease:"power2.inOut"}},{T0 + 1.0:.3f});')
add(f'tl.fromTo("#bigword",{{scale:1}},{{scale:1.05,duration:.55,ease:"sine.inOut",yoyo:true,repeat:{int((TOTAL - T0 - 1.6) / 0.55) // 2 * 2 - 1}}},{T0 + 1.6:.3f});')
add(f'tl.fromTo("#shine",{{x:-700}},{{x:700,duration:.8,ease:"power2.inOut",immediateRender:false}},{T0 + 3.0:.3f});')
add(f'tl.fromTo("#shine",{{x:-700}},{{x:700,duration:.8,ease:"power2.inOut",immediateRender:false}},{T0 + 4.6:.3f});')
# caja de comentario
TB = tRol + 0.35
add(f'tl.fromTo("#cbox",{{opacity:0,y:60,scale:.94}},{{opacity:1,y:0,scale:1,duration:1.0,ease:VB(0.07)}},{TB:.3f});')
typed = CTA_WORD
add(f'tl.call(()=>{{document.querySelector("#ctext").textContent="Agregá un comentario...";document.querySelector("#ctext").className="ph";}},null,{TB - 0.01:.3f});')
for j in range(1, len(typed) + 1):
    t = TB + 0.7 + j * 0.09
    add(f'tl.call(()=>{{const e=document.querySelector("#ctext");e.textContent="{typed[:j]}";e.className="tx";}},null,{t:.3f});')
add(f'tl.fromTo("#send",{{scale:.6,opacity:.35}},{{scale:1,opacity:1,duration:.7,ease:VB(0.08)}},{TB + 1.4:.3f});')
add(f'tl.fromTo("#cursor",{{opacity:1}},{{opacity:0,duration:.01,repeat:11,yoyo:true,repeatDelay:.3}},{TB + 0.1:.3f});')
add(f'tl.fromTo("#arrowp",{{strokeDashoffset:420}},{{strokeDashoffset:0,duration:.7,ease:"power2.out"}},{TB + 1.6:.3f});')
add(f'tl.fromTo("#arrowh",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.6,ease:VB(0.08)}},{TB + 2.2:.3f});')
add(f'tl.fromTo("#cta3",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.45,ease:"power3.out"}},{tInf - 0.1:.3f});')
# zoom suave de cámara
add('tl.fromTo("#zoom",{scale:1.06},{scale:1,duration:2.2,ease:"power3.out"},0);')
# transiciones en movimiento al cambiar de planta y al salir afuera
add('tl.to("#zoom",{scale:1.07,duration:.01},20.89);')
add('tl.to("#zoom",{scale:1,duration:.7,ease:"power3.out"},20.9);')
add('tl.to("#zoom",{scale:1.08,duration:.01},29.29);')
add('tl.to("#zoom",{scale:1,duration:.8,ease:"power3.out"},29.3);')
add(f'tl.to("#zoom",{{scale:1.06,duration:{TOTAL - CTA:.2f},ease:"sine.inOut"}},{CTA});')

html = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family:"Gilroy"; src:url("assets/fonts/Gilroy-ExtraBold.otf") format("opentype"); font-weight:800; }}
@font-face {{ font-family:"Gilroy"; src:url("assets/fonts/Gilroy-Light.otf") format("opentype"); font-weight:300; }}
@font-face {{ font-family:"Poppins"; src:url("assets/fonts/Poppins-Regular.ttf") format("truetype"); font-weight:400; }}
@font-face {{ font-family:"Cormorant"; src:url("assets/fonts/Cormorant-VariableFont_wght.ttf") format("truetype"); font-weight:300 700; font-style:normal; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1920px; overflow:hidden; background:#0b0907; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
#zoom {{ position:absolute; inset:0; transform-origin:50% 45%; }}
#base {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.layer {{ position:absolute; inset:0; pointer-events:none; }}
#topshade {{ position:absolute; left:0; right:0; top:0; height:470px; background:linear-gradient(180deg, rgba(23,40,68,.66) 0%, rgba(23,40,68,.34) 55%, rgba(23,40,68,0) 100%); opacity:0; }}
#hdr {{ position:absolute; left:0; right:0; top:185px; display:flex; flex-direction:column; align-items:center; }}
#price {{ font-family:"Gilroy"; font-weight:800; font-size:72px; letter-spacing:.015em; color:#fff; line-height:1; text-shadow:0 3px 22px rgba(0,0,0,.45); opacity:0; white-space:nowrap; }}
#price .cur {{ font-weight:300; font-size:44px; letter-spacing:.08em; margin-right:12px; vertical-align:14px; color:#C9D1DE; }}
#rule {{ width:120px; height:2px; margin:20px 0 14px; background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.85), rgba(255,255,255,0)); transform:scaleX(0); }}
#addr {{ font-family:"Cormorant"; font-style:italic; font-weight:500; font-size:46px; color:#fff; letter-spacing:.01em; text-shadow:0 2px 16px rgba(0,0,0,.55); opacity:0; }}
#addr b {{ font-weight:600; }}
#addr .dot {{ color:#C9D1DE; margin:0 14px; font-style:normal; }}
.zone {{ position:absolute; left:0; right:0; top:430px; display:flex; align-items:center; justify-content:center; gap:22px; opacity:0; }}
.zone {{ }}
.zone .zt {{ background:rgba(23,40,68,.78); border-radius:30px; padding:8px 10px 8px 20px;  font-family:"Poppins"; font-size:27px; letter-spacing:.30em; color:rgba(255,255,255,.95); text-shadow:0 2px 12px rgba(0,0,0,.6); padding-left:.34em; }}
.zone .zl {{ width:70px; height:1.5px; background:rgba(255,255,255,.85); transform-origin:center; }}
.cap {{ position:absolute; left:70px; right:70px; top:950px; height:400px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; opacity:0; }}
.cap .sm {{ font-family:"Poppins"; font-size:44px; line-height:1.25; color:#fff; text-shadow:0 2px 18px rgba(0,0,0,.6), 0 1px 3px rgba(0,0,0,.5); }}
.cap .key {{ font-family:"Cormorant"; font-style:italic; font-weight:600; font-size:124px; line-height:1.0; color:#fff; margin:2px 0 4px; text-shadow:0 4px 30px rgba(0,0,0,.7), 0 2px 6px rgba(0,0,0,.55); }}
#card {{ position:absolute; left:120px; right:120px; top:930px; padding:46px 54px 40px; border-radius:44px; overflow:hidden;
  background:linear-gradient(160deg, rgba(23,40,68,.82), rgba(14,25,44,.88)); border:2px solid rgba(110,110,110,.85);
  backdrop-filter:blur(30px) saturate(1.3); box-shadow:0 40px 90px -30px rgba(0,0,0,.8), inset 0 2px 0 rgba(255,255,255,.14); opacity:0; }}
#card .row {{ display:flex; align-items:center; gap:26px; margin:10px 0; }}
#card .chk {{ width:62px; height:62px; flex:none; border-radius:50%; background:#FFFFFF; display:flex; align-items:center; justify-content:center; box-shadow:0 0 26px rgba(255,255,255,.25); }}
#card .chk svg {{ width:34px; height:34px; }}
#card .rt {{ font-family:"Gilroy"; font-weight:800; font-size:52px; color:#fff; line-height:1.05; }}
#card #r3 {{ font-family:"Cormorant"; font-style:italic; font-size:40px; color:#C9D1DE; margin:4px 0 0 88px; }}
#sweep {{ position:absolute; top:-20%; bottom:-20%; width:220px; left:50%; margin-left:-110px; transform:skewX(-18deg); background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.16), rgba(255,255,255,0)); }}
.stat {{ position:absolute; left:150px; right:150px; top:900px; padding:40px 40px 38px; border-radius:44px; overflow:hidden; text-align:center;
  background:linear-gradient(160deg, rgba(23,40,68,.82), rgba(14,25,44,.88)); border:2px solid rgba(110,110,110,.85);
  backdrop-filter:blur(30px) saturate(1.3); box-shadow:0 40px 90px -30px rgba(0,0,0,.8), inset 0 2px 0 rgba(255,255,255,.14); opacity:0; }}
.stat .slab {{ font-family:"Poppins"; font-size:26px; letter-spacing:.32em; color:rgba(255,255,255,.92); padding-left:.32em; }}
.stat .snum {{ font-family:"Gilroy"; font-weight:800; font-size:170px; line-height:1.0; margin:8px 0 4px;
  background:linear-gradient(180deg,#FFFFFF 0%,#E6EAF0 55%,#C3CAD6 100%); -webkit-background-clip:text; background-clip:text; color:transparent; }}
.stat .snum.sm2 {{ font-size:130px; }}
.stat .snum .u {{ font-size:.42em; margin-left:10px; vertical-align:.9em; }}
.stat .ssub {{ font-family:"Cormorant"; font-style:italic; font-weight:500; font-size:46px; color:#C9D1DE; margin-top:6px; }}
.stat .cols {{ display:flex; align-items:center; justify-content:center; gap:44px; }}
.stat .sep {{ width:2px; height:170px; background:linear-gradient(180deg, rgba(255,255,255,0), rgba(255,255,255,.7), rgba(255,255,255,0)); }}
.stat .sw {{ position:absolute; top:-20%; bottom:-20%; width:220px; left:50%; margin-left:-110px; transform:skewX(-18deg); background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.14), rgba(255,255,255,0)); }}
#ring {{ position:absolute; width:880px; height:300px; border-radius:50%; border:3px solid rgba(255,255,255,.9); opacity:0; }}
#capbg {{ position:absolute; left:0; right:0; top:880px; height:540px; background:radial-gradient(ellipse 50% 50% at 50% 50%, rgba(23,40,68,.55) 0%, rgba(23,40,68,.30) 50%, rgba(23,40,68,0) 100%); opacity:0; }}
#dim {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 52%, rgba(15,27,47,.62) 0%, rgba(15,27,47,.86) 70%); opacity:0; }}
#cta1 {{ position:absolute; left:60px; right:60px; top:500px; text-align:center; font-family:"Cormorant"; font-style:italic; font-weight:500; font-size:64px; color:#fff; opacity:0; }}
#cta2 {{ position:absolute; left:60px; right:60px; top:625px; text-align:center; font-family:"Poppins"; font-size:44px; letter-spacing:.06em; color:#fff; opacity:0; }}
#cta2 b {{ color:#C9D1DE; font-weight:400; }}
#bigwrap {{ position:absolute; left:0; right:0; top:700px; height:300px; display:flex; justify-content:center; align-items:center; }}
#glow {{ position:absolute; width:900px; height:300px; border-radius:50%; background:radial-gradient(ellipse, rgba(255,255,255,.22), rgba(255,255,255,0) 70%); opacity:0; }}
#bigword {{ position:relative; display:flex; overflow:hidden; isolation:isolate; padding:14px 56px 6px; background:#FFFFFF; border-radius:42px; border:4px solid #6E6E6E; box-shadow:0 34px 90px -20px rgba(0,0,0,.65), 0 0 0 10px rgba(255,255,255,.12); opacity:0; }}
#bigword .L {{ display:inline-block; font-family:"Gilroy"; font-weight:800; font-size:{BIG_PX}px; line-height:1.1; letter-spacing:.01em;
  color:#172844; opacity:0; }}
#shine {{ position:absolute; top:0; bottom:0; width:140px; left:50%; margin-left:-70px; transform:skewX(-20deg); background:linear-gradient(90deg, rgba(110,110,110,0), rgba(110,110,110,.28), rgba(110,110,110,0)); }}
#cbox {{ position:absolute; left:110px; width:740px; top:1060px; height:112px; border-radius:56px; background:rgba(255,255,255,.97); display:flex; align-items:center; padding:0 18px 0 22px; gap:22px; box-shadow:0 30px 70px -20px rgba(0,0,0,.7); opacity:0; }}
#cbox .av {{ width:72px; height:72px; border-radius:50%; flex:none; background:#172844; display:flex; align-items:center; justify-content:center; font-family:"Gilroy"; font-weight:800; font-size:34px; color:#FFFFFF; }}
#cbox .field {{ flex:1; font-family:"Poppins"; font-size:40px; color:#111; display:flex; align-items:center; }}
#ctext.ph {{ color:#9a9a9a; font-size:34px; }}
#ctext.tx {{ color:#111; font-weight:400; }}
#cursor {{ width:3px; height:44px; background:#111; margin-left:4px; }}
#send {{ width:76px; height:76px; border-radius:50%; flex:none; background:#172844; display:flex; align-items:center; justify-content:center; }}
#send svg {{ width:36px; height:36px; }}
#arrow {{ position:absolute; left:760px; top:1150px; width:260px; height:300px; overflow:visible; }}
#cta3 {{ position:absolute; left:80px; width:760px; top:1225px; text-align:center; font-family:"Poppins"; font-size:40px; line-height:1.3; color:#fff; opacity:0; }}
#cta3 i {{ font-family:"Cormorant"; font-weight:600; font-size:54px; color:#C9D1DE; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="zoom"><video id="base" class="clip" src="assets/montaje.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0"></video></div>
  <div class="layer" id="ov">
    <div id="dim"></div>
    <div id="topshade"></div>
    <div id="capbg"></div>
    {"".join(zone_html)}
    {"".join(cap_html)}
    <div id="card"><div id="sweep"></div>
      <div class="row" id="r1"><div class="chk" id="k1"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#172844" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="rt">Apto crédito</div></div>
      <div class="row" id="r2"><div class="chk" id="k2"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#172844" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="rt">Acepta permuta</div></div>
      <div id="r3">{PERMUTA}</div>
    </div>
    <div class="stat" id="sLote"><div class="sw" id="sw1"></div>
      <div class="slab" id="sLoteA">PILETA &nbsp;·&nbsp; LOTE DE</div>
      <div class="snum"><span id="nLote">0</span><span class="u">m²</span></div>
    </div>
    <div class="stat" id="sDatos"><div class="sw" id="sw2"></div>
      <div class="cols">
        <div class="col" id="dA"><div class="snum sm2"><span id="nAnios">0</span></div><div class="slab">AÑOS</div></div>
        <div class="sep" id="dSep"></div>
        <div class="col" id="dB"><div class="snum sm2"><span id="nM2">0</span><span class="u">m²</span></div><div class="slab">CUBIERTOS</div></div>
      </div>
      <div class="ssub" id="dC">en dos plantas</div>
    </div>
    <div id="cta1">¿Te interesó?</div>
    <div id="cta2">comentame la palabra</div>
    <div id="bigwrap"><div id="glow"></div><div id="ring"></div><div id="bigword">{letters}<div id="shine"></div></div></div>
    <div id="cbox"><div class="av">R</div><div class="field"><span id="ctext" class="ph">Agregá un comentario...</span><span id="cursor"></span></div>
      <div id="send"><svg viewBox="0 0 24 24"><path d="M3 11.5L21 3l-6.5 18-3.2-7.3L3 11.5z" fill="#FFFFFF"/></svg></div></div>
    <svg id="arrow" viewBox="0 0 260 300"><path id="arrowp" d="M20 20 C 150 30, 210 110, 205 250" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-dasharray="420" stroke-dashoffset="420"/>
      <path id="arrowh" d="M178 222 L205 262 L230 220" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" style="transform-origin:205px 250px; opacity:0"/></svg>
    <div id="cta3">y te paso <i>toda la información</i></div>
    <div id="hdr"><div id="price"><span class="cur">{MONEDA}</span><span id="pnum">{PRECIO_TXT}</span></div><div id="rule"></div><div id="addr"><b>{DIRECCION}</b><span class="dot">·</span>{LOCALIDAD}</div></div>
  </div>
</div>
<script>
const rb=(vel,fuerza,rebotes,frenado,t)=>vel*fuerza*Math.sin(rebotes*t*2*Math.PI)/Math.exp(frenado*t);
const VB=(fuerza=0.12,llegada=0.3)=>(p)=>{{const tot=llegada+0.8,t=p*tot;if(t<llegada){{const u=t/llegada;return u*u;}}return 1+rb(2/llegada,fuerza,2.5,5,t-llegada);}};
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(J)}
tl.to({{}},{{duration:0.01}},{TOTAL - 0.01});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(cap_html), "subtitulos ->", OUT)
for c in chunks:
    print(f"{c[0]:6.2f}-{c[1]:6.2f} {'(oculto) ' if c[3] else ''}{' '.join(('*'+t+'*') if k else t for t,k in c[2])}")
