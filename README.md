# Agencia Inmobiliaria · Skills de Claude

Todo lo que la agencia usa con Claude, en un solo lugar y portable a cualquier compu:

- **Fábrica de reels** (`Reels con Claude/` + skill `editar-reels-claude`): reels de **propiedades**, **captación** y **marca personal**, cada uno con su estilo.
- **Meta Ads** (`Meta Ads/` + skill `meta-ads-inmobiliaria`): planear, cargar y analizar campañas de captación y de ventas.

## Empezar en una compu nueva (5 minutos)
```powershell
git clone https://github.com/Thomicurve/Agencia-Inmobiliaria-Skills.git E:\Agencia-Inmobiliaria
cd E:\Agencia-Inmobiliaria
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```
Después abrí la app de Claude → pestaña **Code** → carpeta `E:\Agencia-Inmobiliaria`.
Para **renderizar videos** en esa compu: `.\instalar.ps1 -Completo` (ver [docs/01-instalar.md](docs/01-instalar.md)).

## Guías
| | |
|---|---|
| [01 · Instalar y sincronizar](docs/01-instalar.md) | compu nueva, qué se sube y qué no, cómo pasar las tomas |
| [02 · Reel de una propiedad](docs/02-reel-propiedad.md) | de la grabación al video final, paso a paso |
| [03 · Reels de captación y marca personal](docs/03-reel-captacion-marca-personal.md) | cabeza parlante |
| [04 · Estilos y marca](docs/04-estilos-y-marca.md) | crear o cambiar un estilo, íconos, recursos permitidos, formatos nuevos |
| [05 · Meta Ads](docs/05-meta-ads.md) | campañas con los reels |
| [06 · Pedidos rápidos](docs/06-pedidos-rapidos.md) | frases para copiar y pegar en Claude |
| [07 · Demo para la oficina](docs/07-demo-oficina.md) | guión de 15 minutos para mostrar el sistema |

## Mapa
```
Agencia-Inmobiliaria/                 ← este repo
├─ README.md · CLAUDE.md · instalar.ps1 · instalar.sh
├─ docs/                              guías
├─ Skills/
│   ├─ editar-reels-claude/           skill de reels (scripts, plantillas HyperFrames, música SynthFlow)
│   └─ meta-ads-inmobiliaria/         skill de Meta Ads
├─ Reels con Claude/                  la fábrica
│   ├─ Bandeja/                       lo recién grabado
│   ├─ Marca/                         base común: Marca.md, logos, tipografías, música
│   ├─ Estilos/<Tipo>/estilo.md       Propiedades · Captacion · Marca personal (+ recursos y referencias)
│   ├─ Formatos/<formato>/            propiedad-planos · propiedad-recorrido · cabeza-parlante
│   ├─ Propiedades/<Localidad> - <Dirección>/   ⛔ solo local: ficha, guiones, tomas y videos terminados
│   ├─ Captacion/AAAA-MM-DD · <tema>/
│   └─ Marca personal/AAAA-MM-DD · <tema>/
└─ Meta Ads/                          campañas (los leads no se suben)
```

**Repo privado**: tiene datos de la agencia y fuentes con licencia (Gilroy). No lo hagas público.
