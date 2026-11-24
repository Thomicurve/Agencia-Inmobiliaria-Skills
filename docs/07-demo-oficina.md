# 07 · Demo para la oficina (15 minutos)

**Objetivo:** mostrar que con el celular y Claude cualquiera de la oficina puede producir reels con la marca de la agencia, sin saber editar.

## Antes de ir (en casa)
- [ ] `git push` de todo (o pedile a Claude *«Subí los cambios al repo»*).
- [ ] Copiá a un pendrive/Drive la carpeta de la propiedad que vas a mostrar (`Propiedades/<Localidad> - <Dirección>/`) **sin** `tomas/` ni las carpetas `trabajo/` (quedan ~500 MB con los FINAL). Las propiedades no están en GitHub. y, si querés editar en vivo, una toma corta de cabeza parlante (30 s).
- [ ] Si la compu de la oficina no tiene nada: probá el clon + `instalar.ps1` (básico) desde ahí antes de la reunión.

## En la oficina
```powershell
git clone https://github.com/Thomicurve/Agencia-Inmobiliaria-Skills.git C:\Agencia-Inmobiliaria
cd C:\Agencia-Inmobiliaria
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```
Copiá la carpeta de la propiedad del pendrive a `C:\Agencia-Inmobiliaria\Reels con Claude\Propiedades\`.
Abrí la app de Claude → **Code** → carpeta del repo.

## Guión
| Min | Qué mostrar | Qué decir / pedir |
|---|---|---|
| 0–2 | **El resultado**: el `FINAL` de la propiedad en el celular o la tele | «Esto lo hizo Claude con planos del celular y audios de WhatsApp.» |
| 2–4 | **La fábrica**: `README.md` y el mapa de carpetas | Tres tipos de reel, cada uno con su estilo. Todo vive en GitHub y se instala en 5 minutos. |
| 4–6 | **La marca y los estilos** | Pedir: *«Mostrame en una tabla en qué se diferencian los estilos de propiedades, captación y marca personal.»* |
| 6–8 | **La ficha de propiedad** | Abrir `propiedad.json`. Pedir: *«Cambiá el precio de <propiedad> a USD 185.000»* → explicar que los próximos reels ya salen con ese precio. |
| 8–11 | **Alta de una propiedad real de la oficina** | Pegar el texto de una publicación: *«Dá de alta esta propiedad y escribí el guion del reel de planos»* → mostrar la lista de planos y audios a grabar. |
| 11–13 | **Captación** | *«Dame 5 ideas de reels de captación para nuestra zona y el guion del mejor.»* |
| 13–15 | **Cómo trabajar en equipo** | Bandeja → Claude ordena → reel. `git pull` al empezar, «subí los cambios» al terminar. Repartir roles: quién graba, quién revisa. |

**Si la compu tiene placa NVIDIA y corriste `-Completo`:** en el minuto 11 podés editar en vivo la toma de 30 s (*«Reel de marca personal con la toma de la Bandeja, revisión rápida, 1080p»*). Tarda ~5–10 min: arrancalo y seguí con el guión mientras renderiza.

## Preguntas que te pueden hacer
- **¿Hay que saber editar?** No. Se graba con el celular y se dan notas en castellano.
- **¿Cuánto tarda un reel?** 20–40 min de máquina por reel de propiedad; tu tiempo, ~10 min de revisión.
- **¿Se puede cambiar el estilo?** Sí: se le muestran referencias y se guarda en el `estilo.md` del tipo.
- **¿Dónde quedan los videos?** En la compu donde se hicieron (son pesados). En GitHub están las recetas, no los videos.
