# Campañas de captación (propietarios)

**Meta del negocio:** que propietarios de una zona concreta escriban para tasar o vender su propiedad. El resultado real que medimos es **tasaciones agendadas** y **propiedades captadas**, no mensajes.

## Configuración (Administrador de anuncios)

| Nivel | Campo | Valor |
|---|---|---|
| Campaña | Objetivo | **Interacción** |
| Campaña | Categoría especial de anuncios | Ninguna, salvo que Meta la exija (ver `ejecucion.md`) |
| Campaña | Presupuesto | **Presupuesto de campaña Advantage** activado si hay 2 conjuntos; si hay 1, da igual |
| Conjunto | Ubicación de la conversión | **Apps de mensajes** → **WhatsApp** (recomendado) y/o **Instagram** |
| Conjunto | Objetivo de rendimiento | **Maximizar el número de conversaciones** |
| Conjunto | Presupuesto diario | **5–10 USD** (incluso **3–7 USD**) |
| Conjunto | Ubicación geográfica | **Barrios**: pin + radio chico o barrio por nombre. **Nunca la localidad entera ni «todo Rosario»** (ver `segmentacion.md`) |
| Conjunto | Edad | 30–65+ (propietarios); bajar a 28 solo si la zona es de primeros compradores que ya venden |
| Conjunto | Intereses | inmuebles, ZonaProp, Argenprop, inversión inmobiliaria, etc. |
| Conjunto | Ubicaciones (placements) | Advantage+ (automáticas), revisando que los creativos se vean bien en 9:16 y 4:5 |
| Anuncio | **Anuncios de varios anunciantes** | **DESACTIVADO, siempre** |
| Anuncio | Plantilla de mensaje | Saludo + 2–3 preguntas frecuentes (abajo) |

> Alternativa a probar más adelante (sugerencia, a validar): objetivo **Clientes potenciales** con ubicación de la conversión **Mensajes**. Optimiza hacia personas con más intención, pero suele costar más por conversación. Probarla solo cuando haya histórico de la configuración base para comparar.

## Plantilla de mensaje (WhatsApp / Instagram)
La primera impresión del chat filtra y orienta. Escribila en `anuncios/copys.md`.

- **Saludo**: «¡Hola! 👋 Somos <Agencia>. Contanos qué propiedad tenés y en qué barrio, y te decimos cómo podemos ayudarte a venderla.»
- **Preguntas frecuentes** (botones que el usuario toca; cada una abre el chat con ese texto):
  - «Quiero tasar mi propiedad en <Zona>»
  - «Estoy pensando en vender, ¿cómo trabajan?»
  - «¿Cuánto vale hoy una casa en <Zona>?»
- Opcional: respuesta automática en WhatsApp Business para fuera de horario («Te respondemos hoy antes de las 19 h»).

## Guion de calificación (para quien responde los chats)
Dejalo en `plan.md`. Objetivo: en 3–4 mensajes saber si es un propietario real con intención.
1. ¿Qué tipo de propiedad es y dónde está? (¿está en nuestra zona?)
2. ¿Sos el/la propietario/a? (¿decide sola/o o con alguien más?)
3. ¿En qué plazo pensás vender? (ya · 3 meses · 6+ meses · solo curiosidad)
4. ¿Está publicada con otra inmobiliaria?
→ Si responde ya/3 meses y es propietario/a: **calificado** → proponer tasación con día y hora.

Cada contacto va a `leads.csv` con su estado (ver `analisis.md`).

## Estructura recomendada
```
CAP | Funes Centro | WSP | 2026-11       (5 USD/día · 14 días)
└─ Funes Centro 2km | 30-65 | intereses-inmo
   ├─ A1 tasacion-reel        (video de captación de la fábrica de reels)
   ├─ A2 vendimos-carrusel    (casos reales vendidos en la zona, si los hay)
   └─ A3 consejo-reel         (consejo de valor: «3 errores al vender en Funes»)
```
Si se quiere comparar dos zonas: dos conjuntos con presupuesto de campaña Advantage, mismos anuncios.

## Ganchos que suelen funcionar para captar
- Tasación profesional sin cargo / sin compromiso.
- Prueba social local: «Vendimos en <barrio>» (solo si es real, con foto de la propiedad vendida).
- Valor: consejo concreto del agente a cámara (cabeza parlante) — genera confianza antes del chat.
- Escasez de oferta: «Tenemos compradores buscando en <barrio>» — **solo si es verdad y verificable**.
