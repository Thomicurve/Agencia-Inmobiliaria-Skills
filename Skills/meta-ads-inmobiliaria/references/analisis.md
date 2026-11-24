# Fase 3 · Analizar resultados

## Qué necesita el análisis
1. **Exporte de Meta** en `resultados/AAAA-MM-DD.csv`. Cómo lo saca el usuario: Administrador de anuncios → filtrar por la campaña → pestaña **Anuncios** (para ver cada anuncio) → rango «Desde el inicio» → **Exportar → Exportar datos de la tabla → .csv**. Columnas mínimas: nombre de campaña/conjunto/anuncio, importe gastado, impresiones, alcance, frecuencia, clics en el enlace, resultados, y según el tipo «conversaciones con mensajes iniciadas» o «clientes potenciales».
2. **`leads.csv`** actualizado: lo que Meta no ve (quién respondió, quién calificó, tasaciones, visitas, captaciones). Una fila por contacto; columnas `fecha, nombre, telefono, canal (wsp/ig/form), anuncio (A1, A2…), estado, calificado (si/vacío), motivo_descarte, notas`. Valores de `estado` (el script los entiende así):
   - Captación: `nuevo` · `no_responde` · `contactado` · `descartado` · `calificado` · `tasacion` · `captado` · `perdido` (fue calificado y no se concretó)
   - Ventas: `nuevo` · `no_responde` · `contactado` · `descartado` · `calificado` · `visita` · `oferta` · `reserva` · `vendido` · `perdido`
   - `calificado = si` se marca una vez y no se borra aunque después el estado cambie. Si el usuario pega el CSV de leads de Meta, ayudalo a pasarlo a este formato.
3. `campana.json` con `kpis_objetivo`.

## Correr el script
```bash
python "{SKILL}/scripts/analizar.py" "<carpeta de la campaña>"            # informe con el CSV más nuevo
python "{SKILL}/scripts/analizar.py" "<carpeta>" --export "<ruta.csv>"     # otro CSV
python "{SKILL}/scripts/analizar.py" "<carpeta>" --cerrar                  # informe final + fila en historico.csv
```
Deja `informes/AAAA-MM-DD.md` con: totales, tabla por anuncio, embudo de leads, comparación contra objetivos y alertas automáticas. Si el script no reconoce alguna columna, lo dice: pedile al usuario que agregue esa columna en el Administrador de anuncios (Columnas → Personalizar) y vuelva a exportar.

Después **vos** completás la sección «Diagnóstico y recomendación» del informe y se la explicás al usuario en 4–6 líneas.

## Cuándo se puede concluir
| Momento | Qué mirar | Qué hacer |
|---|---|---|
| Día 1–3 | ¿Gasta? ¿Aprobado? ¿Llegan chats/leads? | Solo arreglar errores (rechazo, no entrega, número equivocado). **No optimizar** |
| Día 7 | Primera lectura | Decidir con la tabla de abajo si hay ≥ 10 resultados; si hay menos, esperar o ampliar público |
| Semanal | Tendencia | Rotar creativos con fatiga, escalar lo que funciona |
| Cierre | Costo por calificado / captado / visita | `--cerrar` + `aprendizajes.md` |

Cambios fuertes (presupuesto > +30 %, público, objetivo, creativo nuevo en el conjunto) reinician el aprendizaje: agrupalos y hacelos de una vez, no de a uno por día.

## Embudo y métricas que importan
Las métricas de Meta explican **por qué**; las de `leads.csv` dicen **si sirvió**.

**Captación:** gasto → conversaciones iniciadas → respondieron → calificados (propietario + plazo ≤ 3 meses + en zona) → tasaciones → **captaciones**.
**Ventas:** gasto → leads del formulario → contactados → calificados (plazo ≤ 3 meses + presupuesto acorde) → visitas → **ofertas/reservas**.

KPI principal: **costo por calificado** (y al cierre, costo por captación / por visita).

## Valores de partida
**Referencia inicial, a reemplazar por el histórico propio** (`historico.csv`) en cuanto haya 2–3 campañas cerradas del mismo tipo. Son órdenes de magnitud para Argentina con presupuestos chicos, no metas.

| Métrica | Captación (mensajes) | Ventas (formulario) |
|---|---|---|
| CPM | 1–4 USD | 1–4 USD |
| CTR de enlace | ≥ 1 % | ≥ 1 % |
| Costo por resultado | 0,5–2 USD por conversación | 1–5 USD por lead |
| % que responde / es contactable | ≥ 50 % | ≥ 60 % |
| % calificado sobre resultados | 10–25 % | 15–30 % |
| Frecuencia (7 días) | ≤ 3 | ≤ 3 |

## Árbol de diagnóstico (de arriba hacia abajo; quedate con el primero que aplique)
1. **No gasta / gasta muy poco** → público demasiado chico (ampliar radio 1 km o sacar intereses), anuncio rechazado, o tope de gasto de la cuenta.
2. **CPM muy alto** (> 2× la referencia) → público chico y saturado o mucha competencia: ampliar zona/edad o probar Público Advantage+.
3. **CTR bajo** (< 0,8 %) con CPM normal → el **creativo/gancho** no engancha: cambiar los primeros 3 segundos o el gancho; probar otro formato.
4. **CTR bien pero pocos resultados** → fricción en el paso siguiente: captación = saludo/preguntas del chat poco claros o número mal; ventas = formulario largo o confuso.
5. **Muchos resultados pero pocos calificados** → el público o el gancho atrae curiosos: captación = zona mal elegida o gancho demasiado «gratis»; ventas = pasar a «Mayor intención», agregar pregunta de presupuesto, mostrar el precio en el creativo.
6. **Calificados que no avanzan** (no agendan tasación/visita) → problema comercial, no de anuncios: velocidad de respuesta, guion, seguimiento. Decilo así.
7. **Frecuencia > 3 y costo subiendo** → fatiga: rotar creativos o pausar unos días.

## Decisiones
- **Escalar**: costo por calificado ≤ objetivo durante 7 días con ≥ 3 calificados → subir presupuesto **20–30 %** cada 3–4 días, o duplicar la campaña en una zona vecina.
- **Iterar**: un anuncio claramente peor (costo por resultado > 2× el mejor con gasto comparable) → pausarlo y reemplazarlo por una variante del mejor.
- **Pausar**: 2× el objetivo de costo por calificado después de 14 días, o 0 calificados con > 30 conversaciones/leads.
- **Ventas**: cuando hay reserva, pausar la campaña de esa propiedad el mismo día.

Siempre **una** recomendación principal y concreta («Pausar A2 y duplicar A1 con otro gancho en los primeros 3 s»), no una lista de 8 ideas.

## Al cerrar
1. `analizar.py --cerrar` (suma la fila a `historico.csv`, marca `estado: "cerrada"`).
2. En `aprendizajes.md`: 2–4 líneas con fecha y campaña — qué gancho/zona/público funcionó o no, y el número que lo respalda.
3. Si una zona rindió, actualizá su prioridad en `zonas.md`.
