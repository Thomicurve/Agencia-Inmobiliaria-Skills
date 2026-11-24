# Formato · propiedad-planos
Planos cortos fijos o con movimiento suave por ambiente + voz en off por ambiente (.m4a). Opcional: tomas habladas a cámara (gancho, un comentario en un ambiente).
Aprobado con la primera propiedad de la agencia (nov 2026). Los reels terminados están en `Propiedades/` de la compu principal (no se suben).

## Qué grabar
- Un plano por ambiente (5–15 s), estabilizado, entrando al ambiente.
- Un audio por bloque de voz (Ubicación, Todo integrado, Suite, Quincho y pileta, Apto crédito, Cta…).
- Opcional: `Hook.MOV` hablado a cámara para el gancho.
- Si un audio y un video se llaman igual (Suite.m4a / Suite.MOV), no pasa nada: el audio se transcribe como `SuiteVoz.json`.

## Plantilla (`plantilla/`)
| Archivo | Qué hace | Qué se edita por reel |
|---|---|---|
| `build_voice.py` | Limpia la voz (WPE + cadena), acorta pausas, ordena audios y tomas habladas → `voice.wav` + `voice_timeline.json` | `SEQ` (orden), `WJ` (id → json), `START` |
| `montaje.json` | Escenas: `src` (clip de `src/`) y keyframes `[tiempo reel, tiempo clip]` | Todo: se arma con los tiempos de `voice_timeline.json` |
| `render_montaje.py` | Renderiza el montaje con velocidad suave (PCHIP) y desenfoque de movimiento → `montaje.mp4` | Nada |
| `build_graficos.py` | Cartel precio/dirección, subtítulos, zonas, tarjetas, CTA → `graficos/index.html` | `FRASES`, `zones`, tarjetas de datos. Precio/dirección/CTA salen de `propiedad.json` |
| `mix_final.py` | Efectos + música con ducking + máster −14 LUFS → FINAL | `EV` (efectos), `tR` (momento de la palabra del CTA), filtro `start>…` |

## Pasos
1. `python "{SKILL}/scripts/preparar_tomas.py" --tomas "<propiedad>/tomas/<carpeta>" --work trabajo --lento <planos lindos> [--hablados Hook] --vocab "<localidad, calle>"`
2. Copiar `plantilla/*` a `trabajo/`. Editar `SEQ`/`WJ` → `python build_voice.py`.
3. Escribir `montaje.json` (cada escena sobre su frase) → **mostrar el plan de escenas** → `python render_montaje.py`.
4. Copiar `montaje.mp4` a `graficos/assets/` y las fuentes de `Marca/tipografias/` a `graficos/assets/fonts/`. Editar `FRASES` → `python build_graficos.py` → **mostrar palabras clave** → `npx hyperframes check` / `snapshot` / `render . -o ../trabajo/reel-video.mp4`.
5. `node synthflow_render.cjs sfx trabajo/sfx` + música lofi → editar `EV` → `python mix_final.py`.
