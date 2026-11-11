#!/usr/bin/env bash
# T21 · roda DENTRO da trava pesada (chamado pelo t21_fila.sh através do rec/fila.sh): nunca pega a trava de novo.
# Uso: bash rec/t21/t21_dentro.sh NN|2b ens|ambos|completo
#   ens      = ensaio rápido (sem os `at`), MP4 ultrafast só para a folha de contato, e o resumo
#   ambos    = o rápido e, se ele saiu limpo (0 passo falho, nenhum "SEM ALVO", pageIssues vazio, avisos []), o prever.py e o
#              ensaio completo do MESMO capítulo (uma trava, um capítulo: poupa uma volta inteira na fila)
#   completo = só o ensaio completo (com os `at` da fala estimada)
# Saídas: MP4 e folha em /dev/shm/t21ens e /dev/shm/t21rec; actions/telemetry copiados para rec/t21/_ens e rec/t21.
set -uo pipefail
cd /home/claude/ecoflix
N="$1"; MODO="${2:-ens}"
case "$N" in *b) NOME="cap$(printf %02d "${N%b}")b" ;; *) NOME="cap$(printf %02d "$N")" ;; esac
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54321
: "${TUT_USER:?defina TUT_USER}"; : "${TUT_SENHA:?defina TUT_SENHA}"
PID="$(cat rec/.runtime/fake54321.pid)"
AMB="$(tr '\0' '\n' < "/proc/$PID/environ")"
grep -qx 'FAKE_PORT=54321' <<< "$AMB" || { echo "a instância 54321 não é a da T21"; exit 3; }
grep -qx "FAKE_NOW=$FAKE_NOW" <<< "$AMB" || { echo "FAKE_NOW da instância diferente"; exit 3; }

limpo() {   # o actions.json do argumento saiu limpo?
  python3 -I - "$1" <<'EOF'
import json, sys
a = json.load(open(sys.argv[1]))
acts = a['actions']
falhos = [x for x in acts if x.get('error') or x.get('ok') is False]
pi = a.get('pageIssues') or {}
n_pi = sum(len(v) for v in pi.values() if isinstance(v, list))
sem = [x for x in acts if 'SEM ALVO' in json.dumps(x.get('value', ''), ensure_ascii=False)]
avisos = [x.get('value') for x in acts if x.get('label') == 'avisos de erro na tela']
ruim = falhos or n_pi or sem or any(v not in ('[]', '"[]"', []) for v in avisos)
print(f'limpo? falhos {len(falhos)}, pageIssues {n_pi}, SEM ALVO {len(sem)}, avisos {avisos}')
sys.exit(1 if ruim else 0)
EOF
}

rapido() {
  python3 -I rec/t21/ensaio.py "$N"
  mkdir -p /dev/shm/t21ens
  echo "## rápido $NOME $(date +%H:%M:%S)"
  timeout 900 node rec/record.mjs "rec/t21/_ens/$NOME.json" --rapido --preset ultrafast --crf 30 --out /dev/shm/t21ens > "rec/t21/_ens/.$NOME.out" 2>&1
  echo "record saiu $?"
  cp /dev/shm/t21ens/t21-$NOME.actions.json /dev/shm/t21ens/t21-$NOME.telemetry.json rec/t21/_ens/ 2>/dev/null
  python3 -I rec/t21/resumo.py "$N" --ens
  limpo "rec/t21/_ens/t21-$NOME.actions.json"
}

completo() {
  mkdir -p /dev/shm/t21rec
  echo "## completo $NOME $(date +%H:%M:%S)"
  timeout 900 node rec/record.mjs "rec/t21/$NOME.json" --preset ultrafast --crf 30 --out /dev/shm/t21rec > "rec/t21/.$NOME.out" 2>&1
  echo "record saiu $?"
  cp /dev/shm/t21rec/t21-$NOME.actions.json /dev/shm/t21rec/t21-$NOME.telemetry.json rec/t21/ 2>/dev/null
  python3 -I rec/t21/resumo.py "$N"
  limpo "rec/t21/t21-$NOME.actions.json"
}

case "$MODO" in
  ens) rapido ;;
  completo) completo ;;
  ambos)
    if rapido; then
      python3 -I rec/t21/prever.py "$N" --ens | grep -E "===|ATRASO|~|fim previsto"
      completo
    else
      echo "rápido com problema: o completo fica para depois"
    fi ;;
  *) echo "modo? $MODO"; exit 2 ;;
esac
