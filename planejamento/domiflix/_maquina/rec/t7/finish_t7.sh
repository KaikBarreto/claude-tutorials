#!/usr/bin/env bash
# T7 · montagem final na 1.38.24 (pedido "T7: render"): finish + legendas, parando ANTES do entregar.py.
# 1) disco >= 2,5 GB; 2) tira os nomes antigos (aula_final.mp4 tem hardlink em entrega_final/: o arquivo entregue continua lá e
# nunca é sobrescrito); 3) stems, music.wav e mix.wav em /dev/shm por symlink (o disco não cai no pico do mix); 4) finish.py sob a
# trava (vinheta e cartela de 03/11 reaproveitadas: mesmo título e frase); 5) limpa a memória; 6) legendas_aula.py sob a trava.
# Uso: bash rec/t7/finish_t7.sh   (log: t7/edit/finish.log e t7/edit/out/T7/legendas.log)
set -uo pipefail
cd /home/claude/domiflix/t7/edit
livre=$(df --output=avail -k /home/claude | tail -1)
[ "$livre" -ge 1572864 ] || { echo "PARADO: disco $((livre / 1024)) MB (< 1,5 GiB)"; exit 4; }   # coordenador 06/11: stems, music e mix em /dev/shm, o disco só precisa de ~0,6 GB
rm -f /home/claude/domiflix/t7/edit/out/T7/aula_final.mp4 /home/claude/domiflix/t7/edit/out/T7/video_sem_audio.mp4 \
      /home/claude/domiflix/t7/edit/out/T7/proj/build/mix.wav /home/claude/domiflix/t7/edit/out/T7/proj/build/music.wav
mkdir -p /dev/shm/t7_finish/stems
ln -sfn /dev/shm/t7_finish/stems /home/claude/domiflix/t7/edit/out/T7/proj/build/stems
ln -sf /dev/shm/t7_finish/music.wav /home/claude/domiflix/t7/edit/out/T7/proj/build/music.wav
ln -sf /dev/shm/t7_finish/mix.wav /home/claude/domiflix/t7/edit/out/T7/proj/build/mix.wav
echo "--- [$(date +%H:%M:%S)] finish (disco $((livre / 1024)) MB)"
flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 finish.py caps/T7.aula.json --skip-brand > finish.log 2>&1
rc=$?
echo "finish saida $rc"
tail -c 1500 finish.log | tr '\r' '\n' | grep -v "quadros" | tail -8
rm -rf /dev/shm/t7_finish/stems
rm -f /dev/shm/t7_finish/music.wav /home/claude/domiflix/t7/edit/out/T7/proj/build/music.wav /home/claude/domiflix/t7/edit/out/T7/proj/build/stems
[ "$rc" -eq 0 ] || exit "$rc"
mkdir -p /home/claude/domiflix/t7/edit/out/T7/legendas
cd /home/claude/domiflix/t7/narracao
flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I legendas_aula.py ../edit/out/T7/capitulos.json \
      ../edit/out/T7/proj/build/intro_v.mp4 ../edit/out/T7/legendas/aula_final > ../edit/out/T7/legendas.log 2>&1
echo "legendas saida $?"; tail -3 ../edit/out/T7/legendas.log
ls -la /home/claude/domiflix/t7/edit/out/T7/ /home/claude/domiflix/t7/edit/out/T7/legendas/ /home/claude/domiflix/t7/edit/out/T7/proj/build/
df -h /home/claude | tail -1
