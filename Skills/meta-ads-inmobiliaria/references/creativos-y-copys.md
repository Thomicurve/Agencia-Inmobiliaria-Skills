# Creativos y copys

## Formatos
| Formato | Medida | Dónde se ve | Uso |
|---|---|---|---|
| Video vertical (reel) | 9:16, 1080×1920, 15–45 s | Reels, Historias | El principal. Sale de la fábrica de reels |
| Video/imagen feed | 4:5, 1080×1350 | Feed FB/IG | Recorte del mismo reel o foto |
| Carrusel | 1:1 o 4:5, 6–10 tarjetas | Feed | Ventas: fotos de la propiedad, la mejor primero |

- Dejá **zona segura** en 9:16: sin texto importante en el 14 % superior ni el 35 % inferior (lo tapan la interfaz y el copy).
- Primeros 3 segundos = gancho (precio + zona en ventas; pregunta o dato en captación).
- Subtítulos siempre (la mayoría mira sin sonido).
- **Mejoras de contenido Advantage+** (Meta modifica el creativo con IA: música, brillo, expansión de imagen, variaciones de texto): **desactivá** las que alteren cómo se ve la propiedad (expansión/generación de imagen, retoques visuales). Una propiedad tiene que verse como es.

## Copys — estructura
Español rioplatense (vos), frases cortas, 1–2 emojis como mucho, tono de `Marca.md`.

- **Texto principal** (arriba del creativo): 1.ª línea = gancho (se corta a ~125 caracteres). Luego 2–4 líneas de datos/beneficio. Cierre con llamado a la acción.
- **Título** (debajo, ~40 caracteres).
- **Botón**: captación → «Enviar mensaje» / «Enviar mensaje de WhatsApp»; ventas → «Más información» o «Obtener cotización»/«Registrarte».
- Escribí **2 variantes de texto principal** por anuncio (Meta permite cargar varias y rota).
- Incluí **nombre y matrícula del corredor** (en el texto o en el creativo): la ley de corretaje de Santa Fe lo exige en la publicidad. Tomalo de `agencia.json`.

## Plantillas

### Captación
```
¿Estás pensando en vender tu casa en <Barrio>? 🏡
Te hacemos una tasación profesional, sin cargo y sin compromiso, con datos reales de lo que se vendió en tu zona.
Escribinos y coordinamos una visita esta semana 👇
<Corredor> · Mat. <N.º>
Título: Tasación sin cargo en <Barrio>
```
```
Vendimos en <Barrio> en <N> días.
Si tenés una propiedad en la zona y querés saber cuánto vale hoy, hablemos por WhatsApp.
<Corredor> · Mat. <N.º>
Título: ¿Cuánto vale tu casa hoy?
```

### Ventas (datos desde `propiedad.json`)
```
<Tipo> en <Localidad> · USD <precio> 🔑
<dormitorios> dormitorios · <baños> baños · <m2_cubiertos> m² cub. · lote <m2_lote> m²
<extras más fuertes: pileta, quincho…>
<✅ Apto crédito>  <🔁 Acepta permuta <permuta>>
Dejanos tus datos y te mandamos fotos, planos y coordinamos una visita.
<Corredor> · Mat. <N.º>
Título: <Tipo> en <Localidad> · USD <precio>
```

## Qué no poner
- Promesas que la agencia no confirmó (plazos de venta, «compradores esperando», rentabilidades).
- Precio distinto al de `propiedad.json`.
- Frases que Meta rechaza por «atributos personales» («¿Sos propietario y estás endeudado?»). Hablá de la propiedad, no de la situación de la persona.
- Mayúsculas sostenidas, signos repetidos, clickbait.

## Dónde se guarda
`anuncios/copys.md` con un bloque por anuncio: nombre (`A1 tasacion-reel`), archivo del creativo (ruta), texto principal ×2, título, botón, y — en captación — saludo y preguntas frecuentes del chat; en ventas — preguntas del formulario.
