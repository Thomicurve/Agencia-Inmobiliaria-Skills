#!/usr/bin/env bash
# Instalador para Mac / Linux (básico: enlaza las skills y crea config.local.json).
#   bash instalar.sh            → básico
#   bash instalar.sh --completo → además Python, ffmpeg, Node y librerías (Mac: necesita Homebrew)
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
SK="$HOME/.claude/skills"; mkdir -p "$SK"
echo "== Enlazando skills en $SK"
for d in "$REPO"/Skills/*/; do
  n="$(basename "$d")"
  if [ -e "$SK/$n" ] && [ ! -L "$SK/$n" ]; then mv "$SK/$n" "$SK/$n.respaldo-$(date +%Y%m%d-%H%M)"; fi
  ln -sfn "${d%/}" "$SK/$n"; echo "   OK $n"
done
if [ "$1" = "--completo" ]; then
  if command -v brew >/dev/null; then brew install python@3.11 ffmpeg node; fi
  PY="$(command -v python3.11 || command -v python3)"
  "$PY" -m pip install torch
  "$PY" -m pip install -r "$REPO/Skills/editar-reels-claude/requirements.txt"
  (cd "$REPO/Skills/editar-reels-claude/scripts" && npm install --no-fund --no-audit)
  "$PY" "$REPO/Skills/editar-reels-claude/scripts/check_env.py" --descargar-modelo
fi
PY="$(command -v python3.11 || command -v python3 || true)"
FF="$(dirname "$(command -v ffmpeg 2>/dev/null || echo /x/x)")"
[ -f "$REPO/config.local.json" ] || printf '{"python": "%s", "ffmpeg_bin": "%s", "equipo": "%s"}\n' "$PY" "$FF" "$(hostname)" > "$REPO/config.local.json"
mkdir -p "$REPO/Reels con Claude/Bandeja" "$REPO/Meta Ads"
echo "Listo. Abrí Claude en $REPO"
