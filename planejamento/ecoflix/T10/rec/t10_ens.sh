#!/bin/bash
# T10 · ensaio de um ou mais capítulos, UMA trava por capítulo (a fila dos outros entra entre eles).
#   bash rec/t10/t10_ens.sh 02 03 ...          ensaio RÁPIDO (ensaio.py + --rapido + resumo.py --ens)
#   COMPLETO=1 bash rec/t10/t10_ens.sh 02 ...   gravação com os tempos (rec/t10/capNN.json) + resumo.py
# O MP4 sai apagado logo depois (fica actions/telemetry; a folha de contato fica para olhar e apagar). A senha nasce aqui e não vai
# para arquivo nenhum. Nunca edite este arquivo com ele rodando (copie para outro nome).
cd /home/claude/ecoflix || exit 2
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54310 TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc A-Za-z0-9)}"; export TUT_SENHA
for n in "$@"; do
  nn=$(printf %02d $((10#$n)))
  P=$(cat rec/.runtime/fake54310.pid 2>/dev/null)
  if ! tr '\0' '\n' < /proc/$P/environ 2>/dev/null | grep -qx 'FAKE_PORT=54310'; then echo "cap$nn: a instância 54310 não é a minha (pid $P)"; exit 3; fi
  if [ -n "$COMPLETO" ]; then
    json=rec/t10/cap$nn.json; dir=rec/t10; extra=""; ens=""
  else
    python3 -I rec/t10/ensaio.py $nn >/dev/null; json=rec/t10/_ens/cap$nn.json; dir=rec/t10/_ens; extra="--rapido"; ens="--ens"
  fi
  out=rec/t10/.cap$nn${ens:+.ens}.out
  flock .heavy.lock timeout 900 node rec/record.mjs $json $extra > $out 2>&1
  echo "##### cap$nn ${COMPLETO:+COMPLETO}${ens:+RÁPIDO} exit $? ($(date +%H:%M:%S))"
  rm -f /home/claude/ecoflix/$dir/t10-cap$nn.mp4
  python3 -I rec/t10/resumo.py $nn $ens 2>&1 | tail -n 60
  echo "SEM ALVO: $(grep -c 'SEM ALVO' $out)"
done
