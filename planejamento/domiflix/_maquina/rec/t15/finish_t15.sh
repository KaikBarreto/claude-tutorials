#!/usr/bin/env bash
# T15 · montagem final na 1.38.24 (pedido "T15: render"): finish + legendas, parando ANTES do entregar.py (o entregar é do coordenador).
# 1) disco >= 1,5 GiB; 2) stems, music.wav e mix.wav em /dev/shm por symlink (o disco não cai no pico do mix); 3) finish.py sob a trava
# (vinheta e cartela geradas com o título da aula); 4) apaga os stems e a trilha da memória (o rmtree do finish ignora o symlink);
# 5) legendas_aula.py sob a trava. O mix.wav fica em /dev/shm (o entregar mede o pico com ele): apagar /dev/shm/t15_finish depois da entrega.
# O video_sem_audio.mp4 NÃO é apagado (o remendo exige o total exato de quadros).
# Uso: bash rec/t15/finish_t15.sh   (log: t15/edit/out/T15/finish.log e t15/edit/out/T15/legendas.log)
set -uo pipefail
cd /home/claude/domiflix/t15/edit
livre=$(df --output=avail -k /home/claude | tail -1)
[ "$livre" -ge 1572864 ] || { echo "PARADO: disco $((livre / 1024)) MB (< 1,5 GiB)"; exit 4; }
mkdir -p /home/claude/domiflix/t15/edit/out/T15/proj/build /dev/shm/t15_finish/stems
rm -f /home/claude/domiflix/t15/edit/out/T15/proj/build/music.wav /home/claude/domiflix/t15/edit/out/T15/proj/build/mix.wav
[ -L /home/claude/domiflix/t15/edit/out/T15/proj/build/stems ] || rm -rf /home/claude/domiflix/t15/edit/out/T15/proj/build/stems
ln -sfn /dev/shm/t15_finish/stems /home/claude/domiflix/t15/edit/out/T15/proj/build/stems
ln -sf /dev/shm/t15_finish/music.wav /home/claude/domiflix/t15/edit/out/T15/proj/build/music.wav
ln -sf /dev/shm/t15_finish/mix.wav /home/claude/domiflix/t15/edit/out/T15/proj/build/mix.wav
echo "--- [$(date +%H:%M:%S)] finish (disco $((livre / 1024)) MB)"
flock /home/claude/domiflix/.heavy.lock nice -n 10 env TUT_LOCKED=1 python3 finish.py caps/T15.aula.json > out/T15/finish.log 2>&1
rc=$?
echo "finish saída $rc [$(date +%H:%M:%S)]"
tail -c 1500 out/T15/finish.log | tr '\r' '\n' | grep -v "quadros" | tail -8
rm -rf /dev/shm/t15_finish/stems
rm -f /dev/shm/t15_finish/music.wav /home/claude/domiflix/t15/edit/out/T15/proj/build/music.wav /home/claude/domiflix/t15/edit/out/T15/proj/build/stems
[ "$rc" -eq 0 ] || exit "$rc"
mkdir -p /home/claude/domiflix/t15/edit/out/T15/legendas
cd /home/claude/domiflix/t15/narracao
flock /home/claude/domiflix/.heavy.lock nice -n 10 python3 -I legendas_aula.py ../edit/out/T15/capitulos.json \
      ../edit/out/T15/proj/build/intro_v.mp4 ../edit/out/T15/legendas/aula_final > ../edit/out/T15/legendas.log 2>&1
echo "legendas saída $?"; tail -3 ../edit/out/T15/legendas.log
ls -la /home/claude/domiflix/t15/edit/out/T15/ /home/claude/domiflix/t15/edit/out/T15/legendas/ /home/claude/domiflix/t15/edit/out/T15/proj/build/
df -h /home/claude | tail -1
