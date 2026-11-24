# Marca · base común de todos los reels

Esto lo comparten **todos** los tipos de video (propiedades, captación, marca personal).
Cada tipo suma sus reglas en `Estilos/<Tipo>/estilo.md`. **Si un estilo de tipo contradice esta base, manda el estilo de tipo** (solo en lo que dice explícitamente).

## Paleta (manda sobre todo lo demás)
- Principales: azul **#172844** y gris **#6E6E6E**. Nada de dorado ni neón.
- Sobre video: textos en blanco **#FFFFFF**; acento claro **#C9D1DE** (tono claro del azul) para que se lea sobre fondos oscuros.
- Sombras y oscurecidos con tinte azul: `rgba(23,40,68,α)` en lugar de negro puro.

## Tipografías (`Marca/tipografias/`)
| Uso | Fuente |
|---|---|
| Números, impacto, palabra gigante del CTA | Gilroy ExtraBold (800) · Gilroy Light (300) para monedas/unidades |
| Subtítulos y etiquetas | Poppins Regular |
| Palabra clave elegante, direcciones | Cormorant (italic 600) |

En HyperFrames se copian a `graficos/assets/fonts/` y se cargan con `@font-face` locales.

## Logo (`Marca/logos/`)
- `logo-AB.svg` (color, para fondos claros) y `logo-AB-claro.svg` (para fondos oscuros / sobre video).
- Nunca deformarlo ni cambiarle colores. Margen mínimo alrededor: la altura de la «A».

## Texto y tono
- Español rioplatense con voseo («te llevás», «comentame», «escribime»).
- Moneda siempre **USD** (nunca U$D ni U$S). Miles con punto: 250.000. Superficies en **m²**.
- Una idea por pantalla. Nunca repetir el mismo texto en subtítulo y tarjeta a la vez.

## Formato técnico (todos)
- Vertical 1080×1920, 30 fps, H.264, bt709 SDR. Videos de iPhone HDR → SDR siempre (lo hace `preparar_tomas.py`).
- Zona segura Instagram: nada importante en los 250 px de arriba ni en los 420 px de abajo, ni en los 140 px de la derecha (botones).
- Movimientos suaves: textos con entradas de 0,3–0,45 s con desenfoque; tarjetas con rebote suave; zooms máximo 5–10 %, con curva, nunca cortes.

## Sonido (todos)
- Voz: highpass 85 Hz, afftdn, −2,5 dB a 250 Hz, +2 dB a 3,5 kHz, de-esser, compresor 3:1. Si hay eco de la casa: WPE suave. Pausas máx. ~0,4 s.
- Música 12 dB bajo la voz con ducking de 7 dB. Efectos 20–25 dB bajo la voz.
- Máster **−14 LUFS**, pico real **< −1 dBTP**, verificado sobre el MP4 final.
- Música propia en `Marca/musica/` (si no hay, se genera con SynthFlow: Lo-Fi por defecto).

## Entrega (todos)
- `FINAL - <nombre>.mp4` + `portada.png` (fotograma con palabra grande) en la carpeta del reel.
- Revisar en el celular con y sin sonido antes de publicar.
