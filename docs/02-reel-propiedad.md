# 02 · Reel de una propiedad, paso a paso

Resultado: un reel vertical de ~1 minuto con cartel de precio, voz en off limpia, subtítulos, datos animados y CTA «comentame la palabra …».
Los reels terminados quedan en `Reels con Claude/Propiedades/<Localidad> - <Dirección>/reels/` de la compu donde se hicieron.
⛔ La carpeta `Propiedades/` **no se sube a GitHub**: todo lo de cada propiedad queda en la compu donde se trabaja.

## 1 · Dar de alta la propiedad (una vez por propiedad)
Pedile a Claude:
> *Tengo una propiedad nueva: casa en Funes, San Martín 450, USD 165.000, 3 dormitorios, 2 baños, 180 m² en lote de 600 m², pileta, apta crédito. Palabra del CTA: FUNES. Dala de alta.*

Crea `Propiedades/Funes - San Martín 450/` con `propiedad.json`, `guiones/`, `tomas/` y `reels/`.
Si ya tenés el texto de la publicación, pegalo: saca los datos de ahí.
**Si cambia el precio, se cambia solo en `propiedad.json`** y todos los reels nuevos lo toman.

## 2 · Guion
> *Escribí el guion de voz en off para el reel de planos de Funes - San Martín 450.*

Queda en `guiones/`. Indica qué decir en cada ambiente y qué plano grabar. Un audio por bloque (Ubicación, Planta baja, Suite, Exterior, Apto crédito, CTA).

## 3 · Grabar
| Formato | Qué grabar |
|---|---|
| **propiedad-planos** (recomendado) | Un plano de 5–15 s por ambiente, estable, entrando al ambiente. Opcional: un gancho hablado a cámara (`Hook.MOV`). |
| **propiedad-recorrido** | 2–4 tomas largas caminando (planta baja, arriba, exterior). |

- Voz en off: grabá **un audio por bloque** con el celular cerca de la boca, en un ambiente con poco eco. Nombralos como el bloque (`Ubicación.m4a`, `Suite.m4a`, `Cta.m4a`).
- iPhone en HDR está bien: se convierte solo.

## 4 · Pasar el material
Copiá todo a `Reels con Claude/Bandeja/` y decí:
> *Ordená la Bandeja: son los planos y audios de Funes - San Martín 450.*

Claude los mueve a `Propiedades/Funes - San Martín 450/tomas/planos/`.

## 5 · Hacer el reel
> *Hacé el reel de planos de Funes - San Martín 450.*

Claude va a:
1. Preparar las tomas (HDR→SDR, cámara lenta, transcribir audios).
2. Armar la voz (sin eco, sin pausas largas).
3. **Mostrarte el plan de escenas** (qué plano va sobre cada frase) → aprobás o corregís.
4. Renderizar el montaje con velocidad suave.
5. **Mostrarte las palabras clave** de los subtítulos → aprobás.
6. Gráficos (cartel de precio, zonas, datos, CTA) → vista previa.
7. Música Lo-Fi, efectos y máster.

Entrega en `reels/AAAA-MM-DD · planos/`: `FINAL - ….mp4` y `portada.png`.

## 6 · Notas y correcciones
Hablale como a un editor: *«el living va antes que la cocina»*, *«la pileta más lenta»*, *«el precio tapa la ventana»*.
Cada nota vale para todo el video. Si sirve para siempre, Claude ofrece guardarla en el estilo de propiedades.

## 7 · Publicar
- Miralo en el celular **con y sin sonido**. Nada importante debajo de los botones de Instagram.
- *«Escribí el texto de la publicación de Instagram»* → usa los datos de `propiedad.json`.
- Para la publicidad paga: ver [05 · Meta Ads](05-meta-ads.md).
- Después de publicar podés pedir *«Liberá espacio del reel de Funes»* (borra `trabajo/`, varios GB).
