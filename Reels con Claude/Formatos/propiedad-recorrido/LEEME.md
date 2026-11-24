# Formato · propiedad-recorrido
Recorrido caminando con el celular en pocas tomas largas (planta baja, arriba, exterior) + voz en off por ambiente (.m4a).
Aprobado con la primera propiedad de la agencia (nov 2026). Los reels terminados están en `Propiedades/` de la compu principal (no se suben).

## Qué grabar
- 2–4 tomas largas continuas (`recorrida-parte-abajo.MOV`, `recorrida-parte-arriba.MOV`, `recorrida-quincho.MOV`), caminando lento y estable.
- Un audio por bloque de voz (Intro, Planta baja, Arriba, Quincho, Pileta, Ubicación, Apto crédito, Cierre…).

## Plantilla (`plantilla/`)
Igual que `propiedad-planos`, con dos diferencias:
- `render_montaje.py` usa un diccionario `SRC` (letra → toma larga en `src/`): **editar `SRC`** con las tomas del reel. Los keyframes de `montaje.json` recorren cada toma a distinta velocidad (x2,5–x4 en pasillos, x0,5–x1,3 en lo lindo).
- `build_voice.py` usa audios numerados `voz/v<N>s.wav` y `ORDER`/`GAP`. Para un reel nuevo conviene usar el `build_voice.py` de `propiedad-planos` (más nuevo: lee los audios directo de la carpeta de tomas por nombre) con todos los audios como `'vo'`.

## Pasos
1. `python "{SKILL}/scripts/preparar_tomas.py" --tomas "<propiedad>/tomas/<carpeta>" --work trabajo --vocab "<localidad, calle>"` (para la cámara lenta del cierre, `--lento <toma>`).
2. Voz → montaje → gráficos → mezcla, igual que `propiedad-planos`.
