---
name: meta-ads-inmobiliaria
description: Planifica, carga y analiza campañas de Meta Ads (Facebook e Instagram) para la inmobiliaria, en Argentina. Dos tipos — CAPTACIÓN (conseguir propietarios que quieran vender o tasar, por barrio, con mensajes a WhatsApp o Instagram) y VENTAS (una campaña por propiedad, con formulario instantáneo para filtrar compradores). Arma el plan con presupuesto, zonas, públicos, copys y KPIs; genera la ficha de carga paso a paso para el Administrador de anuncios; y analiza los resultados exportados (CSV) junto con el seguimiento de leads para decidir pausar, iterar o escalar. Úsala cuando el usuario pida armar, planear, cargar, revisar, optimizar o cerrar una campaña o anuncio pago de Meta / Facebook / Instagram, publicitar una propiedad, conseguir captaciones con anuncios, o analizar cómo le fue a una campaña.
---

# Meta Ads · Inmobiliaria (leer primero)

Esta skill acompaña una campaña completa en tres fases: **1. Planear → 2. Ejecutar (cargar) → 3. Analizar**. Cada fase tiene su guía en `{SKILL}/references/`. `{SKILL}` es la carpeta de esta skill (la que contiene este `SKILL.md`).

La persona que te habla probablemente no es experta en Meta Ads. **Hablale claro, en español rioplatense y sin jerga**; cuando uses un término de Meta (objetivo, conjunto, ubicación de la conversión), explicalo en media frase la primera vez. Las preguntas se hacen **con AskUserQuestion**, en tandas de hasta 4, con tu recomendación como primera opción. **No preguntes lo que ya está en los archivos.**

## Espacio de trabajo `{ADS}`

`{AG}` es la raíz de la agencia (el repo): la carpeta real de esta skill es `{AG}/Skills/meta-ads-inmobiliaria`; si no la sabés, `python -c "import os;print(os.path.dirname(os.path.dirname(os.path.realpath(r'{SKILL}'))))"`. Nunca escribas rutas absolutas en archivos del repo.

`{ADS}` = **`{AG}/Meta Ads`**. Si no existe, ofrecé crearlo (o preguntá otra ruta) copiando `{SKILL}/templates/agencia.json`, `zonas.md`, `aprendizajes.md` e `historico.csv`.

```
Meta Ads/
├─ agencia.json        datos fijos: página, IG, WhatsApp, cuenta publicitaria, política de privacidad, corredor y matrícula, tono
├─ zonas.md            barrios/zonas donde captamos, con pin, radio y prioridad
├─ aprendizajes.md     qué funcionó y qué no (se actualiza al cerrar cada campaña)
├─ historico.csv       una fila por campaña cerrada → nuestros propios valores de referencia
├─ Captacion/AAAA-MM-DD · <zona>/          ← una carpeta por campaña
└─ Ventas/<Localidad> - <Dirección>/AAAA-MM-DD/   ← una campaña por propiedad
    ├─ campana.json     plan estructurado (lo leen los scripts) + estado
    ├─ plan.md          plan legible para aprobar
    ├─ ficha-de-carga.md  campo por campo, en el orden del Administrador de anuncios
    ├─ anuncios/        copys.md + creativos (o rutas a los reels)
    ├─ resultados/      exportes CSV del Administrador de anuncios (AAAA-MM-DD.csv)
    ├─ leads.csv        seguimiento de cada contacto hasta captación/venta
    └─ informes/        AAAA-MM-DD.md
```

**Conexión con la fábrica de reels** (`{AG}/Reels con Claude`, skill `editar-reels-claude`):
- Los datos de una propiedad (precio, dirección, dormitorios, apto crédito, permuta) se leen de `Reels con Claude/Propiedades/<Localidad> - <Dirección>/propiedad.json`. **No los copies a mano en los copys: leelos de ahí.** Si la propiedad no existe allá, pedí los datos y ofrecé darla de alta con esa skill.
- Los creativos de video salen de `.../reels/*/` (FINAL) de la propiedad, o de `Reels con Claude/Captacion/*/` para captación. Si no hay video, proponé hacerlo con esa skill o usar fotos (carrusel).
- El tono y la marca: `Reels con Claude/Marca/Marca.md`.

## Reglas de oro (de la experiencia de la agencia en Argentina — no las cambies sin que el usuario lo pida)

| | Captación (propietarios) | Ventas (compradores) |
|---|---|---|
| Objetivo de Meta | **Interacción** → ubicación de la conversión **Mensajes** (WhatsApp y/o Instagram Direct) | **Clientes potenciales** → **Formularios instantáneos** |
| Por qué | En Argentina el formulario genera fricción para el propietario: mejor que hable directo por WhatsApp o IG | El formulario filtra mejor a compradores reales de corto plazo |
| Estructura | 1 campaña por zona/tanda, 1–2 conjuntos, 2–3 anuncios | **Una campaña por propiedad** |
| Presupuesto diario | **5–10 USD**, incluso **3–7 USD** | Según el valor: **3–7 USD** tickets bajos · **5–10 USD** propiedades de 100K–600K USD |
| Ubicación | **Barrios concretos**, nunca la localidad entera ni «todo Rosario» | Zona de la propiedad + de dónde vienen los compradores |
| Intereses a probar | inmuebles, ZonaProp, Argenprop, inversión inmobiliaria, etc. | ídem + crédito hipotecario si es apto crédito |

**Siempre**: desactivar **«Anuncios de varios anunciantes»** (multianunciante) en cada anuncio. Es una casilla a nivel anuncio que Meta deja activada por defecto: si queda activa, el anuncio aparece junto a los de la competencia.

Todo lo que agregues que **no** venga de estas reglas (p. ej. presupuesto para propiedades de más de 600K) marcalo en el plan como **«sugerencia, a validar»**.

## Flujo

Identificá en qué fase está el pedido y abrí la guía correspondiente **antes** de actuar:

1. **Planear** → `references/planificacion.md` (+ `captacion.md` o `ventas.md`, + `segmentacion.md`, + `creativos-y-copys.md`). Termina con `campana.json` + `plan.md` + `anuncios/copys.md` aprobados por el usuario (`estado: "aprobada"`).
2. **Ejecutar** → `references/ejecucion.md`. Genera `ficha-de-carga.md`, repasa el checklist previo a publicar y acompaña la carga. **Publicar o activar la campaña lo hace siempre el usuario** (gasta dinero): vos preparás todo y verificás. Al terminar: `estado: "activa"` y fecha de inicio.
3. **Analizar** → `references/analisis.md`. El usuario exporta el CSV del Administrador de anuncios a `resultados/`, completa `leads.csv`, y corrés:
   ```bash
   python "{SKILL}/scripts/analizar.py" "<carpeta de la campaña>"
   ```
   El script deja `informes/AAAA-MM-DD.md` con los números y alertas; vos agregás el diagnóstico y **una** recomendación concreta (mantener / cambiar creativo / ajustar público / escalar / pausar). Al cerrar: `--cerrar` suma la fila a `historico.csv` y anotás lo aprendido en `aprendizajes.md`.

Si el usuario pide «cómo van las campañas», listá las carpetas con `estado: "activa"` en `campana.json` y ofrecé analizar cada una.

## Lo que nunca hacés
- Publicar, activar, subir presupuesto o cargar medios de pago: eso lo hace el usuario.
- Pedir o escribir tokens, contraseñas o datos de tarjeta.
- Prometer en un anuncio algo que la agencia no confirmó (precios, «vendemos en 30 días», «tenemos compradores en tu barrio»).
- Sacar conclusiones con menos de 7 días o muy pocos resultados: decilo y esperá (ver `analisis.md`).
- Subir `leads.csv` a ningún lado: tiene datos personales de terceros.
