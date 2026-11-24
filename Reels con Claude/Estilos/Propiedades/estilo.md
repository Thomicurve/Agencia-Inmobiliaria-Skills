# Estilo · Reels de PROPIEDADES
Se suma a `Marca/Marca.md`. Aprobado con los reels de la primera propiedad (nov 2026). Referencias en `referencias/`.

**Objetivo:** que alguien que busca casa se frene, vea lo mejor de la propiedad en ~1 minuto y comente la palabra del CTA.
**Formatos que usa:** `propiedad-recorrido` (tomas largas caminando) · `propiedad-planos` (planos cortos, con o sin tomas habladas).
**Datos:** salen de `Propiedades/<propiedad>/propiedad.json` (precio, dirección, localidad, palabra del CTA). Nunca escribirlos a mano en el reel.

## Montaje
- Voz en off grabada aparte por ambiente (audios .m4a), sin audio de cámara. Las tomas habladas a cámara sí llevan su audio (mejorado, en sincronía).
- Velocidad variable siguiendo la voz: rápido en pasillos/escaleras (x2,5–x4 con desenfoque de movimiento), lento en lo lindo (isla, pileta, cierre x0,5–x1,3). Cambios de velocidad con curvas suaves (PCHIP), sin saltos. Para cámara lenta se usan los clips `*60.mp4`.
- Cada clip arranca cuando ya estoy entrando al ambiente: nunca el momento en que miro a cámara esperando el OK.
- Lo que se ve coincide con lo que digo (cada ambiente sobre su frase).
- Duración objetivo ~1 minuto (60–75 s).

## Cartel fijo arriba (todo el video) — exclusivo de este tipo
- Precio: «USD 250.000». Gilroy ExtraBold 72 px blanco; «USD» Gilroy Light 44 px en #C9D1DE.
- Dirección + localidad debajo: Cormorant italic 46 px blanco, separador «·» en #C9D1DE.
- Filete blanco translúcido de 120 × 2 px entre líneas. Degradado azul arriba rgba(23,40,68,.66)→0 en 470 px.
- Arranque: el precio aparece grande al centro, cuenta hasta el valor y sube a su lugar (por eso la voz arranca en 1,6 s si no hay toma hablada al inicio).

## Subtítulos
- Poppins Regular 44 px blanco, sombra 0 2px 18px rgba(0,0,0,.5). Centro de pantalla (y ≈ 1000–1300).
- Una palabra clave por frase en Cormorant italic 600, 124 px, blanca. Entradas suaves 0,35–0,45 s con desenfoque. Sin rebote.
- Cada subtítulo al menos ~1 s en pantalla.

## Gráficos
- Pocos y elegantes (2–4 por reel además del cartel).
- Etiquetas de zona: PLANTA BAJA / PLANTA ALTA / EXTERIOR (Poppins 27 px, tracking .30em, pastilla #172844 entre filetes blancos).
- Tarjetas de datos: cristal azul (rgba(23,40,68,.82)→rgba(14,25,44,.88)), borde 2 px #6E6E6E, números Gilroy ExtraBold con conteo animado (años, m² cubiertos, m² de lote), ✓ en círculo blanco con tilde #172844 (apto crédito, permuta).
- CTA final: fondo oscurecido en azul, palabra del CTA gigante (Gilroy ExtraBold hasta 190 px, se achica si es larga) en placa blanca con letras #172844 y borde #6E6E6E, letras que suben una por una y pulso hasta el final; caja de comentario de Instagram que la escribe y flecha blanca al ícono de comentarios.

## Recursos
**Permitidos:** cartel de precio · etiquetas de zona · tarjetas de datos con conteo · ✓ · íconos de ambientes de `recursos/iconos/` (dormitorio, baño, m², pileta, ubicación) · caja de comentario de Instagram · logo AB claro chico al final.
**Prohibidos:** texto detrás de la cabeza · palabras gigantes a mitad del video · emojis · stickers · escenas a pantalla completa con fondo de color (tapan la casa) · música Synthwave.

## Sonido
- Música: Lo-Fi suave. Efectos: whoosh en cada cambio de escena, uiclick en cada ✓, riser + impact + braaam en la palabra del CTA.

## CTA
«Si te interesó, comentame la palabra **<palabra_cta>** y te paso toda la info.» (la palabra suele ser la localidad o el barrio).
