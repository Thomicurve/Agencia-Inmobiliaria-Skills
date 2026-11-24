# Segmentación: zonas, edad e intereses

## Ubicación geográfica — la decisión más importante en captación
Regla de la agencia: **definir específicamente dónde queremos captar. Barrios, no localidades enteras; no «todo Rosario».**

Cómo cargarlo en Meta:
1. **Barrio por nombre**: escribí el barrio en el buscador de ubicaciones. Algunos barrios de Rosario aparecen; muchos no.
2. **Pin + radio** (lo más común): «Soltar pin» en el centro del barrio y radio mínimo de **1 km** (el mínimo que permite Meta sin categoría especial). Para barrios grandes, 2–3 km; para barrios cerrados o country, 1 km sobre el acceso.
3. **Varios pins** para cubrir un barrio irregular, en lugar de un radio grande que se coma barrios que no queremos.
4. **Excluir** zonas que caen dentro del radio y no interesan (opción «Excluir» en el buscador).

Meta hoy muestra a «personas que viven o estuvieron recientemente» en la zona; no se puede elegir solo residentes. Por eso los radios chicos y bien ubicados importan.

**Tamaño del público**: con 3–10 USD/día, un público de 10.000–150.000 personas está bien. Si Meta marca el público como «muy específico» o la campaña no gasta, ampliá el radio de a 1 km antes de agregar intereses.

## `zonas.md`
Cada zona que se trabaje queda registrada en `{ADS}/zonas.md` (plantilla en `{SKILL}/templates/zonas.md`): nombre, localidad, cómo se carga (barrio o pin), coordenadas, radio, prioridad, ticket típico y notas. Así la próxima campaña en la misma zona se carga igual y los resultados son comparables.

Para sacar coordenadas: Google Maps → clic derecho en el centro del barrio → copiar las coordenadas.

## Edad
- Captación: **30–65+** (los propietarios que venden son mayormente de esa franja).
- Ventas: ajustá al producto (ver `ventas.md`).
- No segmentes por género.

## Intereses
Intereses a probar (notas de la agencia): **inmuebles, ZonaProp, Argenprop, inversión inmobiliaria**, etc. Otros candidatos (sugerencia, a validar): bienes raíces, compra de vivienda, crédito hipotecario, mudanza, arquitectura/decoración del hogar.

Ojo con el **Público Advantage+** (por defecto en Meta): con él activado, edad e intereses son **sugerencias** y Meta puede mostrar el anuncio fuera de ellos (la **ubicación sí se respeta siempre**).
- Captación con zona chica: la zona ya filtra mucho. Recomendación inicial: **opciones de público originales** con intereses, para probar la regla de la agencia. Si no gasta, probar sin intereses (solo zona + edad).
- Ventas: probá primero con opciones originales + intereses; si el costo por lead calificado sale alto, una segunda tanda con Advantage+ para comparar.
- Anotá en `campana.json → conjuntos[].publico_advantage` cuál se usó: es una variable para el análisis.

## Públicos personalizados (cuando haya datos)
- **Interactuaron** con la cuenta de IG/página en 90–365 días → buen público de remarketing para ventas.
- **Abrieron el formulario y no lo enviaron** → remarketing de ventas.
- **Excluir** a quienes ya enviaron formulario de esa propiedad.
Usalos solo cuando la cuenta tenga volumen; con cuentas chicas el público queda demasiado pequeño.
