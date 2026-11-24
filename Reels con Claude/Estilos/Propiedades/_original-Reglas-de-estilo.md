# Reglas de estilo · reels inmobiliarios (sacadas de mis referencias)

## Paleta de la inmobiliaria (manda sobre todo lo demás)
- Principales: azul **#172844** y gris **#6E6E6E**. Nada de dorado ni neón.
- Sobre video: textos en blanco; acentos claros en #C9D1DE (tono claro del azul) para que se lean sobre fondos oscuros.
- Sombras y oscurecidos con tinte azul: rgba(23,40,68,α) en lugar de negro puro.

## Formato
- Vertical 1080×1920, 30 fps. Recorridos con voz en off (audio aparte), sin audio de cámara.
- Videos de iPhone en HDR (HLG): convertir siempre a SDR bt709 (tonemap hable, npl 100, gamma 1.05, saturación 1.12).
- Velocidad variable siguiendo la voz: rápido en pasillos/escaleras (x2,5–x4 con desenfoque de movimiento), lento en lo lindo (isla, pileta, cierre x0,5–x1,3). Cambios de velocidad siempre con curvas suaves, sin saltos.
- Cada clip arranca cuando ya estoy entrando al ambiente: nunca el momento en que miro a cámara esperando el OK.
- Lo que se ve tiene que coincidir con lo que digo en la voz (cada ambiente sobre su frase).
- Duración objetivo: ~1 minuto.

## Cartel fijo arriba (todo el video)
- Precio: «USD 250.000» (escribir **USD**, nunca U$D). Gilroy ExtraBold 72 px blanco; «USD» Gilroy Light 44 px en #C9D1DE.
- Dirección + localidad debajo: Cormorant italic 46 px blanco, separador «·» en #C9D1DE.
- Filete blanco translúcido de 120 × 2 px entre líneas. Degradado azul arriba rgba(23,40,68,.66)→0 en 470 px.
- Arranque: el precio aparece grande al centro, cuenta hasta el valor y sube a su lugar.

## Subtítulos
- Poppins Regular 44 px blanco, sombra suave 0 2px 18px rgba(0,0,0,.5). Centro de pantalla (y ≈ 1000–1300), fuera de la zona de botones de Instagram.
- Una palabra clave por frase en Cormorant italic 600, 124 px, blanca. Entradas suaves 0,35–0,45 s con desenfoque. Sin rebote.
- Frases agrupadas: cada subtítulo al menos ~1 s en pantalla (nada de trozos que parpadean).
- No repetir texto: si un subtítulo dice algo, la tarjeta no lo repite (y al revés, ocultar el subtítulo cuando un gráfico ya lo dice).

## Gráficos
- Pocos y elegantes: etiquetas de zona (Poppins 27 px, tracking .30em, sobre pastilla azul #172844, entre filetes blancos).
- Tarjetas de datos: cristal azul (degradado rgba(23,40,68,.82)→rgba(14,25,44,.88)), borde 2 px #6E6E6E, números Gilroy ExtraBold blancos con conteo animado, ✓ en círculo blanco con tilde #172844.
- CTA final muy visible: fondo oscurecido en azul, palabra clave gigante (Gilroy ExtraBold 190 px) en **placa blanca con letras #172844 y borde #6E6E6E**, letras que suben una por una y pulso hasta el final; caja de comentario de Instagram que la escribe (avatar y botón de enviar en #172844) y flecha blanca al ícono de comentarios.

## Sonido
- Voz: quitar eco (WPE suave), highpass 85 Hz, afftdn, -2,5 dB a 250 Hz, +2 dB a 3,5 kHz, de-esser, compresor 3:1. Pausas máx. ~0,4 s.
- Música Lo-Fi 12 dB bajo la voz con ducking. Efectos 20–25 dB bajo la voz. Máster −14 LUFS, pico < −1 dBTP.
