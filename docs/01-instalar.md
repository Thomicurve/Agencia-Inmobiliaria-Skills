# 01 · Instalar en una compu y mantener todo sincronizado

## Qué necesitás
- La **app de Claude** (escritorio) con la sesión de la cuenta iniciada.
- **Git** (`winget install Git.Git`) y acceso al repo privado en GitHub.
- Para **renderizar** videos: idealmente una placa NVIDIA. Sin placa funciona, pero más lento (conviene 1080p).

## Instalación
```powershell
git clone https://github.com/Thomicurve/Agencia-Inmobiliaria-Skills.git E:\Agencia-Inmobiliaria
cd E:\Agencia-Inmobiliaria
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```
| Modo | Qué hace | Sirve para |
|---|---|---|
| `instalar.ps1` (básico) | Enlaza las skills en `~/.claude/skills` y crea `config.local.json` | Mostrar el sistema, escribir guiones, dar de alta propiedades, ajustar estilos, Meta Ads |
| `instalar.ps1 -Completo` | Además instala Python 3.11, PyTorch, Whisper, ffmpeg, Node, dependencias y el modelo de recorte (~3 GB) | Hacer los videos en esa compu |

En Mac: `bash instalar.sh` (o `bash instalar.sh --completo`, necesita Homebrew).
No hace falta que sea el disco `E:`: el repo puede estar en cualquier carpeta.

Después: app de Claude → **Code** → abrir la carpeta del repo → pedir *«Chequeá que el equipo esté listo para hacer reels»*.

## Qué se sube a GitHub y qué no
| Se sube ✅ | No se sube ❌ (queda en cada compu) |
|---|---|
| Skills, scripts y plantillas | Videos y audios (.MOV, .mp4, .m4a, .wav) |
| Marca, estilos, logos, tipografías | Tomas crudas y Bandeja |
| Plantillas de ficha y guion (`Formatos/`) | **Toda la carpeta `Propiedades/`**: fichas, guiones, tomas, reels y fotos |
| Reels de captación y marca personal (guion, scripts) | Carpetas `trabajo/` pesadas · modelo de recorte (lo baja el instalador) |
| Guías | `config.local.json`, leads de Meta Ads |

**Las propiedades se pasan aparte**: copiá la carpeta entera `Propiedades/<Localidad> - <Dirección>/` (pendrive, disco externo o Google Drive) a la misma ruta en la otra compu. Si solo necesitás datos y guion, alcanza con `propiedad.json` y `guiones/`. Tomas sueltas → `Bandeja/`.

## Rutina diaria
- **Al empezar**: `git pull` (o pedile a Claude *«Traé lo último del repo»*).
- **Al terminar** algo útil para otras compus (una propiedad nueva, un estilo, una plantilla): *«Subí los cambios al repo»*. Claude revisa que no entre nada pesado ni privado, hace el commit y el push.

## Si algo falla
- *«Corré el chequeo del equipo»* → Claude ejecuta `check_env.py` y te dice qué falta y cómo instalarlo.
- Las skills no aparecen → volvé a correr `instalar.ps1` y reiniciá la app de Claude.
