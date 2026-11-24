"""Crea la carpeta de la fábrica de reels (una sola vez). No borra ni sobrescribe nada.

  python crear_carpeta.py --dest "<raíz del repo>/Reels con Claude"

Reels con Claude/
  Bandeja/          lo que grabaste, sin ordenar (Claude lo archiva)
  Marca/            base común: Marca.md, logos/, tipografias/, musica/
  Estilos/<Tipo>/   estilo.md, recursos/iconos/, referencias/   (Propiedades, Captacion, Marca personal)
  Formatos/         plantillas probadas por formato (propiedad-planos, propiedad-recorrido, cabeza-parlante)
  Propiedades/      una carpeta por propiedad: propiedad.json, guiones/, tomas/, reels/
  Captacion/        un reel por carpeta: toma/, guion.md, trabajo/, FINAL
  Marca personal/   igual que Captacion
"""
import argparse, os
import comun  # consola UTF-8 en Windows

TIPOS = ["Propiedades", "Captacion", "Marca personal"]
LEEME = {
    "Bandeja": "Tirá acá lo que grabaste (videos y audios). Claude te propone a qué propiedad o reel va cada cosa y lo mueve.\n",
    "Marca": "Base común a todos los reels: Marca.md (paleta, tipografías, logo, tono, sonido).\n",
    "Marca/logos": "Logos de la marca (.svg o .png con fondo transparente).\n",
    "Marca/tipografias": "Fuentes de la marca (.ttf u .otf).\n",
    "Marca/musica": "Opcional: música propia. Si no hay, Claude la genera con SynthFlow.\n",
    "Formatos": "Una carpeta por formato de video, con LEEME.md (cómo se graba y se arma) y plantilla/ (scripts probados).\n",
    "Propiedades": "Una carpeta por propiedad: «<Localidad> - <Dirección>/» con propiedad.json, guiones/, tomas/ y reels/.\n",
    "Captacion": "Un reel por carpeta: «AAAA-MM-DD · <tema>/» con toma/, guion.md, proyecto.json, trabajo/ y el FINAL.\n",
    "Marca personal": "Un reel por carpeta: «AAAA-MM-DD · <tema>/» con toma/, guion.md, proyecto.json, trabajo/ y el FINAL.\n",
}
for t in TIPOS:
    LEEME[f"Estilos/{t}"] = f"Estilo propio de los reels de {t}: estilo.md (se suma a Marca/Marca.md) con la lista de recursos permitidos y prohibidos.\n"
    LEEME[f"Estilos/{t}/recursos/iconos"] = f"Íconos que solo se usan en reels de {t} (.svg).\n"
    LEEME[f"Estilos/{t}/referencias"] = f"Reels de otros que te gustan para {t}. Claude los mira para ajustar el estilo.\n"

ap = argparse.ArgumentParser()
ap.add_argument("--dest", required=True)
a = ap.parse_args()
for sub, txt in LEEME.items():
    d = os.path.join(a.dest, *sub.split("/"))
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "LEEME.txt")
    if not os.path.exists(f) and not os.listdir(d):
        open(f, "w", encoding="utf-8").write(txt)
print(f"fábrica lista → {a.dest}")
print("Falta: Marca/Marca.md y Estilos/<Tipo>/estilo.md (los armamos juntos con tus referencias).")
