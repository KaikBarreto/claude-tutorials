#!/bin/bash
# T10 · ensaio RÁPIDO e, se ele passar, o COMPLETO do mesmo capítulo, numa trava só por capítulo (a fila anda entre um capítulo e outro).
#   bash rec/t10/t10_cap.sh 03 04          (SO_COMPLETO=1: pula o rápido; SO_RAPIDO=1: não grava o completo)
# Passa para o completo só com: 0 passo falho e nenhum "SEM ALVO" no rápido, e atraso previsto (prever.py --ens) < 0,8 s.
# O MP4 sai apagado logo depois; a folha de contato do completo fica para olhar (e apagar). A senha nasce aqui e não vai para arquivo.
# Nunca edite este arquivo com ele rodando (copie para outro nome).
cd /home/claude/ecoflix || exit 2
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54310 TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc A-Za-z0-9)}"; export TUT_SENHA
for n in "$@"; do
  nn=$(printf %02d $((10#$n)))
  P=$(cat rec/.runtime/fake54310.pid 2>/dev/null)
  if ! tr '\0' '\n' < /proc/$P/environ 2>/dev/null | grep -qx 'FAKE_PORT=54310'; then echo "cap$nn: a instância 54310 não é a minha (pid $P)"; exit 3; fi
  python3 -I rec/t10/ensaio.py $nn >/dev/null
  export nn SO_COMPLETO SO_RAPIDO
  flock .heavy.lock bash -c '
    if [ -z "$SO_COMPLETO" ]; then
      timeout 900 node rec/record.mjs rec/t10/_ens/cap$nn.json --rapido > rec/t10/.cap$nn.ens.out 2>&1
      echo "##### cap$nn RÁPIDO exit $? ($(date +%H:%M:%S))"
      rm -f /home/claude/ecoflix/rec/t10/_ens/t10-cap$nn.mp4 /home/claude/ecoflix/rec/t10/_ens/t10-cap$nn.contact.jpg
      python3 -I rec/t10/resumo.py $nn --ens > rec/t10/.cap$nn.ens.resumo 2>&1; cat rec/t10/.cap$nn.ens.resumo
      sa=$(grep -c "SEM ALVO" rec/t10/.cap$nn.ens.out); echo "SEM ALVO: $sa"
      python3 -I rec/t10/prever.py $nn --ens > rec/t10/.cap$nn.prever 2>&1; grep -E "ATRASO|maior atraso" rec/t10/.cap$nn.prever
      falhos=$(grep -o "falhos [0-9]*" rec/t10/.cap$nn.ens.resumo | head -1 | grep -o "[0-9]*")
      atraso=$(grep -o "maior atraso [0-9.]*" rec/t10/.cap$nn.prever | grep -o "[0-9.]*$")
      if [ -n "$SO_RAPIDO" ] || [ "$falhos" != "0" ] || [ "$sa" != "0" ] || awk "BEGIN{exit !(${atraso:-9} >= 0.8)}"; then
        echo "##### cap$nn: completo NÃO gravado (falhos=$falhos, SEM ALVO=$sa, atraso previsto=$atraso${SO_RAPIDO:+, só rápido})"; exit 0
      fi
    fi
    timeout 900 node rec/record.mjs rec/t10/cap$nn.json > rec/t10/.cap$nn.out 2>&1
    echo "##### cap$nn COMPLETO exit $? ($(date +%H:%M:%S))"
    rm -f /home/claude/ecoflix/rec/t10/t10-cap$nn.mp4
    python3 -I rec/t10/resumo.py $nn 2>&1 | tail -n 70
    echo "SEM ALVO (completo): $(grep -c "SEM ALVO" rec/t10/.cap$nn.out)"
  '
done
