# Fase 2 · Ejecutar (cargar la campaña)

Requisito: `campana.json` con `estado: "aprobada"`. Si no, volvé a `planificacion.md`.

## Paso 1 · Requisitos de la cuenta (la primera vez; después, solo si algo falla)
Repasalos con el usuario y marcá en `agencia.json → requisitos_ok` cuando estén:
- [ ] **Cuenta publicitaria** en Meta Business Suite, en USD, con medio de pago cargado (lo carga el usuario). Recordale que la tarjeta suma **IVA y las percepciones vigentes** sobre lo gastado.
- [ ] **Página de Facebook** y **cuenta de Instagram profesional** conectadas a la cuenta publicitaria.
- [ ] **WhatsApp Business** conectado a la página (Configuración de la página → WhatsApp) — necesario para captación por WhatsApp.
- [ ] **URL de política de privacidad** publicada (necesaria para formularios instantáneos). Si no existe, ofrecé redactar una simple (Ley 25.326 de datos personales) para que la publiquen en su web o en un Google Sites.
- [ ] Quién **recibe y responde** chats y leads, y con qué horario.

## Paso 2 · Ficha de carga
Generá `ficha-de-carga.md` copiando `{SKILL}/templates/ficha-de-carga.md` y completando **cada campo con el valor exacto** de `campana.json` y `anuncios/copys.md`, en el orden en que aparece en el Administrador de anuncios (Campaña → Conjunto → Anuncio). Que el usuario pueda cargarla sin pensar: nombres para copiar y pegar, coordenadas, radios, textos completos, ruta de cada archivo.

Los nombres de los botones de Meta cambian seguido: si el usuario no encuentra un campo, pedile una captura y ubicalo en ella.

### Categoría especial de anuncios
Al crear la campaña Meta pregunta por «Categorías especiales de anuncios» (vivienda, empleo, crédito…). La de **vivienda** es obligatoria para anuncios dirigidos a EE. UU. y otros países; **para Argentina hoy en general no se exige**, y declararla limita mucho la segmentación (radio mínimo de ~25 km, sin edad ni intereses), lo que rompería la regla de barrios. Dejala en «ninguna». Si Meta la exige o rechaza anuncios por ese motivo, **pará y avisá al usuario** antes de seguir: cambia toda la estrategia de segmentación.

## Paso 3 · Acompañar la carga
Dos modos (preguntá cuál prefiere):
- **El usuario carga** con la ficha abierta, y vos respondés dudas. (Recomendado las primeras veces: aprende.)
- **Te pide que lo hagas en el navegador** (Claude en Chrome o el navegador integrado, con su sesión de Meta abierta): completás los campos según la ficha y **te detenés antes de «Publicar»**. Publicar lo aprieta el usuario después de revisar. Nunca cambies medios de pago, límites de gasto ni configuración de la cuenta.

## Paso 4 · Checklist antes de publicar (revisalo campo por campo)
- [ ] Objetivo correcto: captación = **Interacción + Mensajes**; ventas = **Clientes potenciales + Formulario instantáneo**.
- [ ] Una campaña por propiedad (ventas).
- [ ] Presupuesto diario y fecha de finalización (o recordatorio de pausa) cargados. Total = diario × días coincide con el plan.
- [ ] Ubicación: barrios/pins del plan, **no** la localidad entera ni el país. Revisá que Meta no haya agregado «Argentina» por defecto.
- [ ] Edad e intereses del plan; Público Advantage+ según el plan.
- [ ] **«Anuncios de varios anunciantes» DESACTIVADO en cada anuncio** (se revisa uno por uno; duplicar anuncios a veces lo vuelve a activar).
- [ ] Mejoras de contenido Advantage+ que alteran la imagen: desactivadas.
- [ ] Captación: número de WhatsApp correcto, saludo y preguntas frecuentes cargados.
- [ ] Ventas: formulario «Mayor intención», preguntas de filtro, política de privacidad, pantalla final.
- [ ] Copy con datos de `propiedad.json` y nombre + matrícula del corredor.
- [ ] Vista previa en Reels/Historias: nada importante tapado.
- [ ] Nombres de campaña, conjunto y anuncio según la convención (el análisis depende de ellos).

## Paso 5 · Después de publicar
- Anotá en `campana.json`: `estado: "activa"`, `fechas.inicio`, y los ID de campaña si el usuario los pasa.
- Meta revisa los anuncios (minutos a 24 h). Si rechaza alguno: leé el motivo con el usuario, corregí el copy/creativo según `creativos-y-copys.md` («Qué no poner») y pedí revisión.
- Recordá el calendario: **día 3** solo verificar que entrega y que llegan chats/leads; **no tocar nada** hasta el día 7 (cada cambio fuerte reinicia el aprendizaje de Meta).
- Creá `leads.csv` (de la plantilla) y explicá cómo completarlo: una fila por contacto, se actualiza el estado a medida que avanza.
