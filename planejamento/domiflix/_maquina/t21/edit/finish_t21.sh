#!/usr/bin/env bash
# T21 · montagem final (pedido "T21: render", 06/11): finish + legendas, parando ANTES do entregar.py (o entregar é do coordenador).
# Molde: rec/t7/finish_t7.sh. 1) disco >= 1,2 GiB (piso do coordenador); 2) stems, music.wav e mix.wav em /dev/shm/t21_finish por symlink
# (o disco não cai no pico do mix); 3) finish.py sob a trava (vinheta e cartela novas: título "Integração com WhatsApp"); 4) apaga stems e
# music da memória (o mix.wav fica para a medição do pico depois do AAC; apagar à mão depois); 5) legendas_aula.py sob a trava.
# Uso: bash t21/edit/finish_t21.sh   (log: t21/edit/finish.log e t21/edit/out/T21/legendas.log)
set -uo pipefail
cd /home/claude/domiflix/t21/edit
export TUT_HOME=/home/claude/domiflix
livre=$(df --output=avail -k /home/claude | tail -1)
[ "$livre" -ge 1258292 ] || { echo "PARADO: disco $((livre / 1024)) MB (< 1,2 GiB)"; exit 4; }
OUT=/home/claude/domiflix/t21/edit/out/T21
mkdir -p "$OUT/proj/build" /dev/shm/t21_finish/stems
ln -sfn /dev/shm/t21_finish/stems "$OUT/proj/build/stems"
ln -sf /dev/shm/t21_finish/music.wav "$OUT/proj/build/music.wav"
ln -sf /dev/shm/t21_finish/mix.wav "$OUT/proj/build/mix.wav"
echo "--- [$(date +%H:%M:%S)] finish (disco $((livre / 1024)) MB)"
flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 -I finish.py caps/T21.aula.json > finish.log 2>&1
rc=$?
echo "finish saida $rc"
tail -c 2500 finish.log | tr '\r' '\n' | grep -v "quadros  " | tail -14
rm -rf /dev/shm/t21_finish/stems
rm -f /dev/shm/t21_finish/music.wav "$OUT/proj/build/music.wav" "$OUT/proj/build/stems"
[ "$rc" -eq 0 ] || exit "$rc"
mkdir -p "$OUT/legendas"
cd /home/claude/domiflix/t21/narracao
flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I legendas_aula.py ../edit/out/T21/capitulos.json \
      ../edit/out/T21/proj/build/intro_v.mp4 ../edit/out/T21/legendas/aula_final > ../edit/out/T21/legendas.log 2>&1
echo "legendas saida $?"; tail -3 ../edit/out/T21/legendas.log
ls -la "$OUT" "$OUT/legendas" "$OUT/proj/build"
df -h /home/claude | tail -1
