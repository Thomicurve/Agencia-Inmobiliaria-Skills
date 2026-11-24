"""Fábrica · preparar las tomas de una propiedad para un reel de recorrido o de planos.

  python preparar_tomas.py --tomas "<propiedad>/tomas/planos" --work "<reel>/trabajo" \
      [--lento Exterior,Suite] [--hablados Hook,HabladoLuminosidad] [--vocab "<localidad>, <calle>, quincho, toilette"]

Hace, sin tocar nunca los originales:
  1. Videos (.MOV/.mp4) → trabajo/src/<nombre>.mp4  (1080x1920, SDR bt709; si es HDR/HLG del iPhone aplica el
     tonemap aprobado: hable, npl 100, gamma 1.05, saturación 1.12). Respeta los fps y la rotación del iPhone.
  2. --lento: además crea <nombre>60.mp4 interpolado a 60 fps (minterpolate) para cámara lenta suave.
  3. Audios (.m4a/.wav/.mp3) y videos de --hablados → transcripción palabra a palabra en trabajo/voz/<nombre>.json
     (si un audio y un video se llaman igual, el del audio queda como <nombre>Voz.json).
Los nombres se normalizan a NFC (el iPhone los guarda con tildes descompuestas).
Si un archivo de salida ya existe, se salta (borralo para rehacerlo).
"""
import argparse, json, os, subprocess, unicodedata
import comun  # consola UTF-8 en Windows

VID = (".mov", ".mp4", ".m4v")
AUD = (".m4a", ".wav", ".mp3", ".aac")
HDR_VF = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
          "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=1.05:saturation=1.12,")
FIT = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
SLOW = "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                        "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    return r.stdout.strip()


def venc():
    enc = comun.pick_encoder()
    if enc == "nvenc":
        return ["-c:v", "h264_nvenc", "-preset", "p6", "-rc", "vbr", "-cq", "16", "-b:v", "0"]
    if enc == "videotoolbox":
        return ["-c:v", "h264_videotoolbox", "-q:v", "70"]
    return ["-c:v", "libx264", "-preset", "medium", "-crf", "16"]


def to_sdr(src, dst, extra=""):
    hdr = probe(src) in ("arib-std-b67", "smpte2084")
    vf = (HDR_VF if hdr else "") + FIT + ("," + extra if extra else "")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-an", *venc(), "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", dst], check=True)
    return hdr


ap = argparse.ArgumentParser()
ap.add_argument("--tomas", required=True)
ap.add_argument("--work", required=True)
ap.add_argument("--lento", default="", help="videos (sin extensión, separados por coma) que necesitan versión 60 fps")
ap.add_argument("--hablados", default="", help="videos donde hablás a cámara: se transcribe su audio")
ap.add_argument("--vocab", default="")
ap.add_argument("--sin-video", action="store_true")
ap.add_argument("--sin-voz", action="store_true")
a = ap.parse_args()

src_dir, voz_dir = os.path.join(a.work, "src"), os.path.join(a.work, "voz")
os.makedirs(src_dir, exist_ok=True); os.makedirs(voz_dir, exist_ok=True)
files = sorted(os.listdir(a.tomas))
lento = {nfc(x.strip()) for x in a.lento.split(",") if x.strip()}
hablados = {nfc(x.strip()) for x in a.hablados.split(",") if x.strip()}
vids = [f for f in files if f.lower().endswith(VID)]
auds = [f for f in files if f.lower().endswith(AUD)]
vid_stems = {nfc(os.path.splitext(f)[0]) for f in vids}

if not a.sin_video:
    for f in vids:
        stem = nfc(os.path.splitext(f)[0]); src = os.path.join(a.tomas, f)
        out = os.path.join(src_dir, stem + ".mp4")
        if not os.path.exists(out):
            hdr = to_sdr(src, out)
            print(f"video  {stem:<32} → src/{stem}.mp4 {'(HDR→SDR)' if hdr else ''}", flush=True)
        if stem in lento and not os.path.exists(os.path.join(src_dir, stem + "60.mp4")):
            to_sdr(src, os.path.join(src_dir, stem + "60.mp4"), SLOW)
            print(f"lento  {stem:<32} → src/{stem}60.mp4", flush=True)

if not a.sin_voz:
    jobs = []
    for f in auds:
        stem = nfc(os.path.splitext(f)[0])
        jobs.append((f, stem + "Voz" if stem in vid_stems else stem))
    for f in vids:
        stem = nfc(os.path.splitext(f)[0])
        if stem in hablados:
            jobs.append((f, stem))
    todo = [(f, n) for f, n in jobs if not os.path.exists(os.path.join(voz_dir, n + ".json"))]
    if todo:
        import torch, whisper
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("turbo", device=dev)
        for f, name in todo:
            wav = os.path.join(voz_dir, f"_{name}16k.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(a.tomas, f), "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
            res = model.transcribe(wav, language="es", word_timestamps=True, condition_on_previous_text=False,
                                   initial_prompt=a.vocab or None, fp16=(dev == "cuda"))
            words = [{"w": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)}
                     for seg in res["segments"] for w in seg.get("words", [])]
            json.dump({"text": res["text"].strip(), "words": words}, open(os.path.join(voz_dir, name + ".json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            os.remove(wav)
            print(f"voz    {name:<32} «{res['text'].strip()[:90]}»", flush=True)
print("listo →", a.work)
