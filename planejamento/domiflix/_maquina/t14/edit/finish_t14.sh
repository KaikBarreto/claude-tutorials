#!/usr/bin/env bash
# T14 · montagem final (pedido "T14: render", 06/11): finish + legendas, parando ANTES do entregar.py (o entregar é do coordenador).
# Molde: t21/edit/finish_t21.sh (re-executável). 1) disco >= 1,2 GiB (piso do coordenador); 2) stems, music.wav e mix.wav em
# /dev/shm/t14_finish por symlink (o disco não cai no pico do mix); 3) finish.py do T14 sob a trava (cortes e aceleração do cap09);
# 4) apaga stems e music da memória (o mix.wav fica para a medição do pico depois do AAC; apagar à mão depois); 5) legendas_aula.py sob a trava.
# O video_sem_audio.mp4 fica (pedido do coordenador). Uso: bash t14/edit/finish_t14.sh   (log: t14/edit/finish.log e t14/edit/out/T14/legendas.log)
set -uo pipefail
cd /home/claude/domiflix/t14/edit
export TUT_HOME=/home/claude/domiflix
livre=$(df --output=avail -k /home/claude | tail -1)
[ "$livre" -ge 1258292 ] || { echo "PARADO: disco $((livre / 1024)) MB (< 1,2 GiB)"; exit 4; }
OUT=/home/claude/domiflix/t14/edit/out/T14
mkdir -p "$OUT/proj/build" /dev/shm/t14_finish/stems
ln -sfn /dev/shm/t14_finish/stems "$OUT/proj/build/stems"
ln -sf /dev/shm/t14_finish/music.wav "$OUT/proj/build/music.wav"
ln -sf /dev/shm/t14_finish/mix.wav "$OUT/proj/build/mix.wav"
echo "--- [$(date +%H:%M:%S)] finish (disco $((livre / 1024)) MB)"
flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 -I finish.py caps/T14.aula.json > finish.log 2>&1
rc=$?
echo "finish saida $rc"
tail -c 2500 finish.log | tr '\r' '\n' | grep -v "quadros  " | tail -16
rm -rf /dev/shm/t14_finish/stems
rm -f /dev/shm/t14_finish/music.wav "$OUT/proj/build/music.wav" "$OUT/proj/build/stems"
[ "$rc" -eq 0 ] || exit "$rc"
mkdir -p "$OUT/legendas"
cd /home/claude/domiflix/t14/narracao
flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I legendas_aula.py ../edit/out/T14/capitulos.json \
      ../edit/out/T14/proj/build/intro_v.mp4 ../edit/out/T14/legendas/aula_final > ../edit/out/T14/legendas.log 2>&1
echo "legendas saida $?"; tail -3 ../edit/out/T14/legendas.log
ls -la "$OUT" "$OUT/legendas" "$OUT/proj/build"
df -h /home/claude | tail -1
