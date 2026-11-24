<#
  Instalador de la agencia (skills de Claude + fabrica de reels).

  Uso (en PowerShell, dentro de la carpeta del repo):
    powershell -ExecutionPolicy Bypass -File .\instalar.ps1            # basico: enlaza skills y crea config
    powershell -ExecutionPolicy Bypass -File .\instalar.ps1 -Completo  # ademas instala todo para renderizar videos

  Basico   -> alcanza para guiones, estilos, planes de Meta Ads, fichas de propiedades y para MOSTRAR el sistema.
  Completo -> Python 3.11 + PyTorch + Whisper, ffmpeg, Node, dependencias y modelo de recorte (~3 GB, 15-30 min).
  Se puede correr varias veces: no borra nada.
#>
param([switch]$Completo)
$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$Skills = Join-Path $env:USERPROFILE ".claude\skills"
$Config = Join-Path $Repo "config.local.json"

function Paso($t) { Write-Host ""; Write-Host "== $t" -ForegroundColor Cyan }
function Ok($t)   { Write-Host "   OK  $t" -ForegroundColor Green }
function Ojo($t)  { Write-Host "   !!  $t" -ForegroundColor Yellow }
function Tiene($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

# ---------------------------------------------------------------- 1. Skills
Paso "1. Enlazando las skills en $Skills"
New-Item -ItemType Directory -Force $Skills | Out-Null
foreach ($d in Get-ChildItem (Join-Path $Repo "Skills") -Directory) {
    $dest = Join-Path $Skills $d.Name
    if (Test-Path $dest) {
        $it = Get-Item $dest -Force
        if ($it.LinkType) { cmd /c rmdir "$dest" | Out-Null }
        else {
            $bak = "$dest.respaldo-" + (Get-Date -Format "yyyyMMdd-HHmm")
            Rename-Item $dest $bak
            Ojo "habia una copia suelta de $($d.Name): la renombre a $bak"
        }
    }
    cmd /c mklink /J "$dest" "$($d.FullName)" | Out-Null
    Ok $d.Name
}

# ---------------------------------------------------------------- 2. Programas (solo -Completo)
$py = $null
if ($Completo) {
    Paso "2. Programas (winget)"
    if (-not (Tiene "winget")) { throw "No esta winget. Instala 'App Installer' desde Microsoft Store y volve a correr." }
    $apps = @(
        @{id="Python.Python.3.11"; cmd="py";     nombre="Python 3.11"},
        @{id="Gyan.FFmpeg";        cmd="ffmpeg"; nombre="ffmpeg"},
        @{id="OpenJS.NodeJS.LTS";  cmd="node";   nombre="Node.js"},
        @{id="Git.Git";            cmd="git";    nombre="Git"}
    )
    foreach ($a in $apps) {
        if (Tiene $a.cmd) { Ok "$($a.nombre) ya esta" }
        else {
            Write-Host "   instalando $($a.nombre)..."
            winget install --id $a.id -e --silent --accept-source-agreements --accept-package-agreements | Out-Null
            Ok "$($a.nombre) instalado (si algo no aparece, cerra y abri PowerShell y volve a correr)"
        }
    }
    $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
}

# ---------------------------------------------------------------- 3. Python
Paso "3. Python"
if (Test-Path $Config) {
    $c = Get-Content $Config -Raw | ConvertFrom-Json
    if ($c.python -and (Test-Path $c.python)) { $py = $c.python }
}
if (-not $py -and (Tiene "py")) {
    try { $py = (& py -3.11 -c "import sys;print(sys.executable)").Trim() } catch { $py = $null }
}
if (-not $py -and (Tiene "python")) { $py = (& python -c "import sys;print(sys.executable)").Trim() }
if ($py) { Ok "Python: $py" } else { Ojo "No encontre Python 3.11. Para renderizar videos corre: .\instalar.ps1 -Completo" }

if ($Completo -and $py) {
    Paso "4. Librerias de Python (PyTorch, Whisper...)"
    $nvidia = Tiene "nvidia-smi"
    & $py -m pip install --upgrade pip | Out-Null
    $tiene_torch = $false
    try { & $py -c "import torch" 2>$null; $tiene_torch = ($LASTEXITCODE -eq 0) } catch {}
    if (-not $tiene_torch) {
        if ($nvidia) { & $py -m pip install torch --index-url https://download.pytorch.org/whl/cu128 }
        else { & $py -m pip install torch }
    }
    & $py -m pip install -r (Join-Path $Repo "Skills\editar-reels-claude\requirements.txt")
    Ok "librerias listas (GPU NVIDIA: $nvidia)"

    Paso "5. Node (musica y efectos) y modelo de recorte"
    Push-Location (Join-Path $Repo "Skills\editar-reels-claude\scripts")
    npm install --no-fund --no-audit | Out-Null
    Pop-Location
    Ok "npm install"
    & $py (Join-Path $Repo "Skills\editar-reels-claude\scripts\check_env.py") --descargar-modelo
}

# ---------------------------------------------------------------- 6. Config de esta compu
Paso "6. config.local.json (rutas de ESTA compu, no se sube a GitHub)"
$ff = $null
if (Tiene "ffmpeg") { $ff = Split-Path -Parent (Get-Command ffmpeg).Source }
$cfg = [ordered]@{ python = $py; ffmpeg_bin = $ff; equipo = $env:COMPUTERNAME }
if (Test-Path $Config) {
    $old = Get-Content $Config -Raw | ConvertFrom-Json
    foreach ($p in $old.PSObject.Properties) { if (-not $cfg[$p.Name]) { $cfg[$p.Name] = $p.Value } }
}
($cfg | ConvertTo-Json) -replace '\\\\','/' | Set-Content -Encoding UTF8 $Config
Ok $Config

# ---------------------------------------------------------------- 7. Carpetas locales
Paso "7. Carpetas de trabajo"
foreach ($d in "Reels con Claude\Bandeja", "Meta Ads") { New-Item -ItemType Directory -Force (Join-Path $Repo $d) | Out-Null }
Ok "listas"

if ($Completo -and $py) {
    Paso "8. Chequeo del equipo"
    & $py (Join-Path $Repo "Skills\editar-reels-claude\scripts\check_env.py")
}

Write-Host ""
Write-Host "Listo. Abri Claude (app de escritorio, pestana Code) en la carpeta:" -ForegroundColor Green
Write-Host "   $Repo"
Write-Host "y pedile, por ejemplo: 'Mostrame que puedo hacer con la fabrica de reels'."
