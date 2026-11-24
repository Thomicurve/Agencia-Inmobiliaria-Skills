# Campañas de ventas (una por propiedad)

**Meta del negocio:** conseguir compradores reales de corto plazo para **una propiedad concreta**. En Argentina se usa mucho el **formulario** en los anuncios de venta porque **filtra mejor** que el mensaje directo: quien completa preguntas de presupuesto y plazo está más cerca de comprar. El resultado real que medimos es **visitas** y **ofertas/reservas**.

## Presupuesto según el valor de la propiedad

| Precio de la propiedad | Presupuesto diario | Origen |
|---|---|---|
| Ticket bajo (< 100K USD, lotes, deptos chicos, alquileres) | **3–7 USD** | Notas de la agencia |
| 100K – 600K USD | **5–10 USD** | Notas de la agencia |
| > 600K USD | 10–15 USD | **Sugerencia, a validar** |

Duración: 14 días mínimo; 21–30 días si el ticket es alto (el comprador tarda más). Elegí el extremo bajo del rango si la zona es chica o la propiedad muy específica, y el alto si el público es amplio o hay urgencia.

## Configuración (Administrador de anuncios)

| Nivel | Campo | Valor |
|---|---|---|
| Campaña | Objetivo | **Clientes potenciales** |
| Campaña | Nombre | `VTA | <Localidad> - <Dirección> | FORM | AAAA-MM` — **una campaña por propiedad** |
| Conjunto | Ubicación de la conversión | **Formularios instantáneos** |
| Conjunto | Objetivo de rendimiento | **Maximizar el número de clientes potenciales** |
| Conjunto | Presupuesto diario | según la tabla de arriba |
| Conjunto | Ubicación geográfica | Localidad de la propiedad + localidades desde donde viene el comprador típico (ej. una casa en Funes o Roldán: Funes + Roldán + Rosario). Acá sí se puede abrir más que en captación |
| Conjunto | Edad | 28–65 (ajustar al producto: monoambiente inversor 25+, casa familiar 30–55) |
| Conjunto | Intereses | inmuebles, ZonaProp, Argenprop, inversión inmobiliaria; **crédito hipotecario** si `apto_credito: true` |
| Anuncio | **Anuncios de varios anunciantes** | **DESACTIVADO, siempre** |
| Anuncio | Formulario | ver abajo |

## Formulario instantáneo
- **Tipo**: **Mayor intención** (agrega una pantalla para que la persona revise sus datos antes de enviar: menos leads pero más reales). Usar «Más volumen» solo si no llegan leads en 7 días.
- **Introducción**: título con la propiedad (ej. «Casa en Roldán · 3 amb. · pileta») + 1 línea de lo más fuerte.
- **Preguntas** (opción múltiple, para filtrar — elegí 2–3, no más):
  1. ¿Cuándo pensás comprar? → Ya · En 1–3 meses · En 3–6 meses · Solo estoy mirando
  2. ¿Cómo pensás pagar? → Contado · Crédito hipotecario · Necesito vender otra propiedad · Permuta (incluir solo si `permuta` no es null)
  3. ¿Tu presupuesto está en el rango de <precio ± 10%>? → Sí · Un poco por debajo · No
- **Datos de contacto**: nombre completo + teléfono (prellenados por Meta). Email opcional (agrega fricción).
- **Política de privacidad**: URL de `agencia.json` (Meta la exige).
- **Pantalla final**: «¡Gracias! Te escribimos por WhatsApp en menos de 1 hora hábil» + botón a WhatsApp o al perfil de IG.

**Velocidad de respuesta**: el lead se llama/escribe **en la primera hora** (idealmente minutos). Pasado un día, la tasa de contacto cae mucho. Definí en `plan.md` quién descarga los leads (Meta Business Suite → Centro de clientes potenciales, o integración) y cada cuánto.

## Estructura recomendada
```
VTA | <Localidad> - <Dirección> | FORM | 2026-11    (7 USD/día · 21 días)
└─ Roldán+Funes+Rosario | 30-60 | intereses-inmo+credito
   ├─ A1 recorrido-reel     (reel FINAL de la fábrica)
   ├─ A2 fotos-carrusel     (6–10 fotos, la mejor primero)
   └─ A3 planos-reel        (si existe)
```

## Datos del anuncio
Los datos (precio, m², dormitorios, apto crédito, permuta, extras) se leen de `propiedad.json`. Si el precio cambia, se cambia allá y se actualiza el copy — nunca al revés.
