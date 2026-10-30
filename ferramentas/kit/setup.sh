#!/usr/bin/env bash
# Prepara o kit Domiflix numa máquina nova: copia o kit da skill para DOMI (padrão /home/user/domiflix),
# instala as dependências Python e baixa os modelos (ASR Parakeet v3, VAD Silero, SoundFont GeneralUser GS).
# Rede: github.com + raw.githubusercontent.com (modelos) e pypi. Vídeo pelo Drive: drive.google.com + drive.usercontent.google.com.
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOMI="${DOMI:-/home/user/domiflix}"
mkdir -p "$DOMI/models"
for d in kit audio web; do mkdir -p "$DOMI/$d"; cp -r --update=none "$SRC/$d/." "$DOMI/$d/"; done
# marca (cores, fonte, logo, vinheta): $DOMI/marca/marca.json, lida pelo kit/ui.py. MARCA=<pasta com marca.json>
# instala uma se ainda não houver (o instalar.sh da skill faz o mesmo); sem marca.json vale o padrão neutro.
if [ -n "${MARCA:-}" ] && [ ! -f "$DOMI/marca/marca.json" ]; then
  [ -f "$MARCA/marca.json" ] || { echo "MARCA=$MARCA não tem marca.json"; exit 1; }
  mkdir -p "$DOMI/marca"; cp -r "$MARCA/." "$DOMI/marca/"
fi
chmod +x "$DOMI"/kit/*.sh
pip install --break-system-packages -q sherpa-onnx scipy soundfile pyloudnorm opencv-python-headless fonttools brotli pillow numpy gdown 2>&1 | grep -v -i warning || true
pip install --break-system-packages -q --no-deps tinysoundfont 2>&1 | grep -v -i warning || true
cd "$DOMI/models"
[ -f silero_vad.onnx ] || curl -sSL --retry 3 -o silero_vad.onnx https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx &
[ -f GeneralUser-GS.sf2 ] || curl -sSL --retry 3 -o GeneralUser-GS.sf2 https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2 &
if [ ! -f sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/encoder.int8.onnx ]; then
  (curl -sSL --retry 3 -o parakeet.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2 \
    && tar -xjf parakeet.tar.bz2 && rm parakeet.tar.bz2) &
fi
wait
ls "$DOMI/models"
echo "kit pronto em $DOMI"
