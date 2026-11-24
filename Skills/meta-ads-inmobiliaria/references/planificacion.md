# Fase 1 · Planear una campaña

Objetivo de la fase: dejar en la carpeta de la campaña un **`campana.json`**, un **`plan.md`** y **`anuncios/copys.md`**, revisados y aprobados por el usuario.

## Paso 0 · Contexto (sin preguntar)
Leé antes de la entrevista:
- `{ADS}/agencia.json` → si faltan campos clave (página, IG, WhatsApp, URL de política de privacidad, corredor y matrícula), pedilos una sola vez y guardalos.
- `{ADS}/zonas.md` → zonas ya definidas y su prioridad.
- `{ADS}/aprendizajes.md` e `{ADS}/historico.csv` → qué funcionó; usá los costos reales como KPIs objetivo si hay al menos 2 campañas comparables.
- Ventas: el `propiedad.json` de la fábrica de reels y qué reels/fotos hay.
- Campañas activas: no superpongas zonas de captación activas (compiten entre sí por el mismo público).

## Paso 1 · Entrevista (AskUserQuestion, máx. 2 tandas de 4)

**Si no está claro:** ¿captación o ventas? Si es ventas, ¿qué propiedad?

**Captación — tanda 1**
1. **Zona**: ofrecé las zonas de `zonas.md` por prioridad (o una nueva: barrio + localidad). Una campaña = una zona o un grupo de barrios vecinos.
2. **Gancho / propuesta**: tasación sin cargo · vendimos en tu barrio · guía o consejo para vender · otro. Solo lo que la agencia realmente ofrece.
3. **Canal**: WhatsApp (recomendado) · Instagram Direct · ambos.
4. **Presupuesto y duración**: 5 USD/día × 14 días (recomendado) · 3 USD/día · 10 USD/día · otro.

**Ventas — tanda 1**
1. **Confirmá los datos** leídos de `propiedad.json` (precio, apto crédito, permuta) y si el precio es publicable.
2. **Creativo**: reel existente (listá los FINAL) · carrusel de fotos · hacer un reel nuevo.
3. **Presupuesto**: el que corresponde por precio (ver `ventas.md`) como primera opción.
4. **¿Quién recibe los leads y en cuánto tiempo los llama?** (crítico: un lead de formulario se enfría en horas).

**Tanda 2 (si hace falta):** edad mínima, intereses a probar, fechas, si quiere probar 2 ganchos distintos.

## Paso 2 · Armar la campaña
1. Creá la carpeta: `Captacion/AAAA-MM-DD · <zona>/` o `Ventas/<Localidad> - <Dirección>/AAAA-MM-DD/`.
2. Copiá `{SKILL}/templates/campana.json`, `plan.md` y `leads.csv` y completalos siguiendo:
   - `captacion.md` o `ventas.md` (configuración de cada tipo),
   - `segmentacion.md` (zonas, pins, edad, intereses),
   - `creativos-y-copys.md` (anuncios y textos → `anuncios/copys.md`).
3. **Nombres** (se usan en el Administrador de anuncios y el script los usa para cruzar datos):
   - Campaña: `CAP | <Zona> | WSP | AAAA-MM` · `VTA | <Localidad> - <Dirección> | FORM | AAAA-MM`
   - Conjunto: `<Zona o radio> | <edad> | <público>` (ej. `Funes Centro 2km | 30-65 | intereses-inmo`)
   - Anuncio: `A1 <gancho>-<formato>` (ej. `A1 tasacion-reel`, `A2 vendimos-carrusel`)
4. **KPIs objetivo** en `campana.json → kpis_objetivo`: si hay histórico, usá la mediana de las campañas cerradas del mismo tipo; si no, los valores de partida de `analisis.md` marcados como «referencia inicial». Los números que trae la plantilla son de captación: en ventas reemplazalos (costo por lead, no por conversación). En ventas, completá también `meta` con Clientes potenciales / Formularios instantáneos / Maximizar el número de clientes potenciales.
5. **Calendario de revisión**: día 3 (solo que esté entregando), día 7 (primera evaluación), luego semanal y cierre.

## Paso 3 · Presentar y aprobar
Mostrá un resumen corto (no el JSON): objetivo, zona/público, presupuesto diario y total (+ aviso de que la tarjeta suma IVA y percepciones), anuncios con su copy, KPIs objetivo y fechas de revisión. Preguntá si se aprueba o qué cambiar. Al aprobar: `estado: "aprobada"` y pasá a `ejecucion.md`.

## Principios de planificación con presupuestos chicos
- **No fragmentar**: con 3–10 USD/día, más de 2 conjuntos o más de 3 anuncios por conjunto reparte tan poco que nada aprende.
- **Probar una sola cosa por vez**: con poco presupuesto se prueban **creativos/ganchos** (2–3 anuncios en un mismo conjunto), no 4 públicos distintos.
- **Mínimo 7 días** antes de juzgar; idealmente 14 para captación y 14–30 para ventas.
- **El resultado que importa no es el mensaje, es la captación o la visita**: por eso existe `leads.csv` desde el día 1.
