#!/usr/bin/env bash
# T22 · montagem final (pedido "T22: render", 06/11): finish + legendas, parando ANTES do entregar.py (o entregar é do coordenador).
# Molde: rec/t7/finish_t7.sh. 1) disco >= 1,5 GiB; 2) stems, music.wav e mix.wav em /dev/shm por symlink (o disco não cai no pico do
# mix); 3) finish.py sob a trava (vinheta e cartela novas: o T22 ainda não tinha); 4) tira stems e trilha da memória (o mix.wav fica em
# /dev/shm/t22_finish até a medição do pico real depois do AAC; apagar à mão depois); 5) legendas_aula.py sob a trava.
# NÃO apaga video_sem_audio.mp4. O áudio dos capítulos está em /dev/shm/t22_caps (render_todos.sh).
# Uso: bash rec/t22/finish_t22.sh   (logs: t22/edit/finish.log e t22/edit/out/T22/legendas.log)
set -uo pipefail
cd /home/claude/domiflix/t22/edit
livre=$(df --output=avail -k /home/claude | tail -1)
[ "$livre" -ge 1572864 ] || { echo "PARADO: disco $((livre / 1024)) MB (< 1,5 GiB)"; exit 4; }
for NN in 00 01 02 03 04 05 06 07 08 09 10 11; do
  [ -s "/dev/shm/t22_caps/cap$NN.wav" ] && [ -s "out/cap$NN/cap$NN.mp4" ] || { echo "PARADO: falta o render do cap$NN"; exit 5; }
done
mkdir -p /home/claude/domiflix/t22/edit/out/T22/proj/build /dev/shm/t22_finish/stems
ln -sfn /dev/shm/t22_finish/stems /home/claude/domiflix/t22/edit/out/T22/proj/build/stems
ln -sf /dev/shm/t22_finish/music.wav /home/claude/domiflix/t22/edit/out/T22/proj/build/music.wav
ln -sf /dev/shm/t22_finish/mix.wav /home/claude/domiflix/t22/edit/out/T22/proj/build/mix.wav
echo "--- [$(date +%H:%M:%S)] finish (disco $((livre / 1024)) MB)"
flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 finish.py caps/T22.aula.json > finish.log 2>&1
rc=$?
echo "finish saida $rc"
tail -c 1500 finish.log | tr '\r' '\n' | grep -v "quadros" | tail -8
rm -rf /dev/shm/t22_finish/stems
rm -f /dev/shm/t22_finish/music.wav /home/claude/domiflix/t22/edit/out/T22/proj/build/music.wav /home/claude/domiflix/t22/edit/out/T22/proj/build/stems
[ "$rc" -eq 0 ] || exit "$rc"
mkdir -p /home/claude/domiflix/t22/edit/out/T22/legendas
cd /home/claude/domiflix/t22/narracao
flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I legendas_aula.py ../edit/out/T22/capitulos.json \
      ../edit/out/T22/proj/build/intro_v.mp4 ../edit/out/T22/legendas/aula_final > ../edit/out/T22/legendas.log 2>&1
echo "legendas saida $?"; tail -3 ../edit/out/T22/legendas.log
ls -la /home/claude/domiflix/t22/edit/out/T22/ /home/claude/domiflix/t22/edit/out/T22/legendas/ /home/claude/domiflix/t22/edit/out/T22/proj/build/
df -h /home/claude | tail -1
