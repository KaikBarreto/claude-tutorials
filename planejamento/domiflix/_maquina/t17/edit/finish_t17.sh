#!/usr/bin/env bash
# T17 · montagem final (pedido "T17: render", 06/11): finish + legendas, parando ANTES do entregar.py (o entregar é do coordenador).
# Molde: t21/edit/finish_t21.sh. Re-executável.
# 1) disco >= 1,2 GiB para COMEÇAR (piso do coordenador; abaixo disso espera, conferindo de 10 em 10 min, e não para de vez);
# 2) stems, music.wav e mix.wav em /dev/shm/t17_finish por symlink (o disco não cai no pico do mix);
# 3) finish.py sob a trava (vinheta e cartela novas: título "Dashboard, relatórios e exportações");
# 4) apaga stems e music da memória (o mix.wav fica para a medição do pico depois do AAC; apagar à mão depois, com o /dev/shm do T17);
# 5) legendas_aula.py sob a trava. O video_sem_audio.mp4 e os renders de capítulo ficam (revisão do coordenador).
# Uso: bash t17/edit/finish_t17.sh   (log: t17/edit/finish.log e t17/edit/out/T17/legendas.log)
set -uo pipefail
cd /home/claude/domiflix/t17/edit
export TUT_HOME=/home/claude/domiflix
while :; do
  livre=$(df --output=avail -k /home/claude | tail -1)
  [ "$livre" -ge 1258292 ] && break
  echo "--- [$(date +%H:%M:%S)] disco $((livre / 1024)) MB (< 1,2 GiB): espero 10 min para o finish"
  sleep 600
done
for n in 00 01 02 03 04 05 06 07 08 09 10 11; do
  [ -s "out/cap$n/cap$n.mp4" ] || { echo "PARADO: falta out/cap$n/cap$n.mp4 (renderize antes)"; exit 6; }
done
OUT=/home/claude/domiflix/t17/edit/out/T17
mkdir -p "$OUT/proj/build" /dev/shm/t17_finish/stems
ln -sfn /dev/shm/t17_finish/stems "$OUT/proj/build/stems"
ln -sf /dev/shm/t17_finish/music.wav "$OUT/proj/build/music.wav"
ln -sf /dev/shm/t17_finish/mix.wav "$OUT/proj/build/mix.wav"
echo "--- [$(date +%H:%M:%S)] finish (disco $((livre / 1024)) MB)"
flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 -I finish.py caps/T17.aula.json > finish.log 2>&1
rc=$?
echo "finish saida $rc ($(date +%H:%M:%S))"
tail -c 2500 finish.log | tr '\r' '\n' | grep -v "quadros  " | tail -14
rm -rf /dev/shm/t17_finish/stems
rm -f /dev/shm/t17_finish/music.wav "$OUT/proj/build/music.wav" "$OUT/proj/build/stems"
[ "$rc" -eq 0 ] || exit "$rc"
mkdir -p "$OUT/legendas"
cd /home/claude/domiflix/t17/narracao
flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I legendas_aula.py ../edit/out/T17/capitulos.json \
      ../edit/out/T17/proj/build/intro_v.mp4 ../edit/out/T17/legendas/aula_final > ../edit/out/T17/legendas.log 2>&1
echo "legendas saida $? ($(date +%H:%M:%S))"; tail -3 ../edit/out/T17/legendas.log
ls -la "$OUT" "$OUT/legendas" "$OUT/proj/build"
df -h /home/claude | tail -1
