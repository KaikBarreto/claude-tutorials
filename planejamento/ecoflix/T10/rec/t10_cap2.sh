#!/bin/bash
# T10 · regra de 11/11 18:46 (coordenador): por capítulo, numa trava só, o ensaio RÁPIDO (com o MP4 montado, para a folha de contato) e o
# prever.py; o COMPLETO só quando o capítulo tem gesto sensível a espera (lista do FORCAR) ou o prever.py acusa atraso >= 0,4 s.
#   FORCAR="03 04" bash rec/t10/t10_cap2.sh 01 03 04        (SO_COMPLETO=1: pula o rápido, que já passou)
# Sem completo quando o rápido tem passo falho, "SEM ALVO" ou pageIssues (precisa conserto) ou o atraso previsto passa de 0,8 s (precisa
# âncora nova). O MP4 sai apagado logo depois; as folhas de contato ficam para olhar (e apagar). A senha nasce aqui e não vai para arquivo.
# Nunca edite este arquivo com ele rodando (copie para outro nome).
cd /home/claude/ecoflix || exit 2
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54310 TUT_USER=rafael@reciclavalemetais.example
TUT_SENHA="${TUT_SENHA:-$(head -c 12 /dev/urandom | base64 | tr -dc A-Za-z0-9)}"; export TUT_SENHA
for n in "$@"; do
  nn=$(printf %02d $((10#$n)))
  P=$(cat rec/.runtime/fake54310.pid 2>/dev/null)
  if ! tr '\0' '\n' < /proc/$P/environ 2>/dev/null | grep -qx 'FAKE_PORT=54310'; then echo "cap$nn: a instância 54310 não é a minha (pid $P)"; exit 3; fi
  python3 -I rec/t10/ensaio.py $nn >/dev/null
  forca=""; case " $FORCAR " in *" $nn "*) forca=1;; esac
  export nn forca SO_COMPLETO
  flock .heavy.lock bash -c '
    issues() { python3 -c "import json,sys;a=json.load(open(sys.argv[1]));print(sum(len(v) for v in (a.get(\"pageIssues\") or {}).values()))" "$1" 2>/dev/null || echo 9; }
    if [ -z "$SO_COMPLETO" ]; then
      timeout 900 node rec/record.mjs rec/t10/_ens/cap$nn.json --rapido > rec/t10/.cap$nn.ens.out 2>&1
      echo "##### cap$nn RÁPIDO exit $? ($(date +%H:%M:%S))"
      rm -f /home/claude/ecoflix/rec/t10/_ens/t10-cap$nn.mp4
      python3 -I rec/t10/resumo.py $nn --ens > rec/t10/.cap$nn.ens.resumo 2>&1; cat rec/t10/.cap$nn.ens.resumo
      sa=$(grep -c "SEM ALVO" rec/t10/.cap$nn.ens.out); pi=$(issues rec/t10/_ens/t10-cap$nn.actions.json)
      python3 -I rec/t10/prever.py $nn --ens > rec/t10/.cap$nn.prever 2>&1; grep -E "ATRASO|~|maior atraso" rec/t10/.cap$nn.prever
      falhos=$(grep -o "falhos [0-9]*" rec/t10/.cap$nn.ens.resumo | head -1 | grep -o "[0-9]*")
      atraso=$(grep -o "maior atraso [0-9.]*" rec/t10/.cap$nn.prever | grep -o "[0-9.]*$")
      echo "SEM ALVO: $sa; pageIssues: $pi; atraso previsto: $atraso; gesto sensível: ${forca:-não}"
      if [ "$falhos" != "0" ] || [ "$sa" != "0" ] || [ "$pi" != "0" ]; then echo "##### cap$nn: RÁPIDO COM PROBLEMA (completo não gravado)"; exit 0; fi
      if awk "BEGIN{exit !(${atraso:-9} >= 0.8)}"; then echo "##### cap$nn: rápido ok; atraso previsto $atraso >= 0,8 (completo não gravado: âncora nova)"; exit 0; fi
      if [ -z "$forca" ] && awk "BEGIN{exit !(${atraso:-9} < 0.4)}"; then echo "##### cap$nn: SÓ RÁPIDO (ok; atraso previsto $atraso < 0,4 e sem gesto sensível)"; exit 0; fi
    fi
    timeout 900 node rec/record.mjs rec/t10/cap$nn.json > rec/t10/.cap$nn.out 2>&1
    echo "##### cap$nn COMPLETO exit $? ($(date +%H:%M:%S))"
    rm -f /home/claude/ecoflix/rec/t10/t10-cap$nn.mp4
    python3 -I rec/t10/resumo.py $nn 2>&1 | tail -n 70
    echo "SEM ALVO (completo): $(grep -c "SEM ALVO" rec/t10/.cap$nn.out); pageIssues: $(issues rec/t10/t10-cap$nn.actions.json)"
  '
done
