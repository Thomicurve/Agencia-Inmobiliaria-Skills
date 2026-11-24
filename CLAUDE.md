# Agencia inmobiliaria · instrucciones para Claude

Este repo es la raíz de la agencia (`{AG}`). Hablá en español rioplatense, claro y sin jerga: quien te usa puede no ser técnico. Ejecutá vos los comandos.

- **Reels** (cualquier video, reel, short, TikTok, portada, propiedad nueva, Bandeja, estilos): usá la skill `editar-reels-claude`. Fábrica en `Reels con Claude/` (mapa en su `LEEME.md`).
- **Publicidad en Meta / Facebook / Instagram**: skill `meta-ads-inmobiliaria`. Datos en `Meta Ads/`.
- **Datos de una propiedad**: siempre de `Reels con Claude/Propiedades/<Localidad> - <Dirección>/propiedad.json`. Nunca los copies a mano en scripts, copys o gráficos. **`Reels con Claude/Propiedades/` es solo local** (fichas, guiones, tomas y videos terminados): nunca lo agregues al repo; las plantillas genéricas están en `Reels con Claude/Formatos/`.
- **Rutas**: nunca escribas rutas absolutas (E:\…, C:\…) en archivos del repo; usá rutas relativas a `{AG}`. Lo propio de cada compu (Python, ffmpeg) está en `config.local.json` (no se sube). Si falta, sugerí correr `instalar.ps1`.
- **Qué se sube a GitHub**: ver `.gitignore`. Videos, audios, tomas, carpetas `trabajo/` pesadas, el modelo de recorte y los leads **no** se suben. Antes de un commit, revisá `git status` y que no entre nada pesado ni con datos personales.
- **Guías para personas**: `docs/`. Si cambia el flujo de trabajo, actualizá la guía correspondiente.
- **Sincronizar**: al empezar, `git pull`; al terminar algo que sirve en otras compus (estilo, plantilla, guía; nunca propiedades), proponé commit + push con un mensaje claro en español.
