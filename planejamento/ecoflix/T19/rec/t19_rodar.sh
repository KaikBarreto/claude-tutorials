#!/usr/bin/env bash
# T19 · um capítulo por trava: gera o roteiro, grava (ensaio rápido ou completo), resume e, com --seed, grava a semente apos-capNN
# (só com 0 passo falho e nenhum "SEM ALVO"), tudo na MESMA trava da gravação. O MP4 vai para /dev/shm e a folha de contato fica
# para conferir (apagar depois de olhar).
#   bash rec/t19/t19_rodar.sh NN [--ens] [--seed] [--quadros "t1 t2 ..."]
# Instância: FAKE_PORT 54319 (só desta aula), FAKE_NOW 2026-11-10T08:30:00-03:00. Precisa de TUT_USER e TUT_SENHA no ambiente.
set -uo pipefail
TUT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$TUT_HOME"
NN=$(printf %02d "$((10#$1))"); shift
ENS=0; SEED=0; QUADROS=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --ens) ENS=1 ;;
    --seed) SEED=1 ;;
    --quadros) QUADROS="$2"; shift ;;
  esac
  shift
done
export FAKE_URL=http://127.0.0.1:54319 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:?falta TUT_USER}" "${TUT_SENHA:?falta TUT_SENHA}"
PID=$(cat rec/.runtime/fake54319.pid 2>/dev/null || true)
AMB=$( [[ -n "$PID" ]] && tr '\0' '\n' < "/proc/$PID/environ" 2>/dev/null || true)
if [[ "$AMB" != *$'\nFAKE_PORT=54319\n'* && "$AMB" != FAKE_PORT=54319$'\n'* ]] || [[ "$AMB" != *"FAKE_NOW=$FAKE_NOW"* ]]; then
  echo "instância 54319 não é a desta aula (ou caiu): FAKE_NOW=$FAKE_NOW FAKE_PORT=54319 bash rec/run.sh fake"; exit 4
fi
python3 -I rec/t19/gerar.py "$NN" | tail -2
if [[ $ENS == 1 ]]; then
  python3 -I rec/t19/ensaio.py "$NN"
  ROT=rec/t19/_ens/cap$NN.json; OUTD=rec/t19/_ens; ARGS=(--rapido); TAG=ens
else
  ROT=rec/t19/cap$NN.json; OUTD=rec/t19; ARGS=(); TAG=final
fi
LOG=rec/t19/.cap$NN.$TAG.out
flock .heavy.lock bash -c '
  set -uo pipefail
  timeout 900 node rec/record.mjs "$0" "${@:4}" > "$1" 2>&1; echo "record exit $?" >> "$1"
  A="$2/t19-cap$3.actions.json"
  if [[ "'"$SEED"'" == 1 ]]; then
    F=$(python3 -c "import json,sys;a=json.load(open(sys.argv[1]));print(sum(1 for x in a[\"actions\"] if x.get(\"error\") or x.get(\"ok\") is False))" "$A" 2>/dev/null || echo X)
    S=$(grep -v SEMENTE "$1" | grep -c "SEM ALVO" || true)
    if [[ "$F" == 0 && "$S" == 0 ]]; then node rec/t19/t19_semente.mjs "apos-cap$3" >> "$1" 2>&1; else echo "SEMENTE NAO GRAVADA: falhos $F, SEM ALVO $S" >> "$1"; fi
  fi
  if [[ -n "'"$QUADROS"'" && -f "$2/t19-cap$3.mp4" ]]; then
    mkdir -p /dev/shm/t19/q$3
    for t in '"$QUADROS"'; do ffmpeg -loglevel error -y -ss "$t" -i "$2/t19-cap$3.mp4" -frames:v 1 -vf scale=1280:-1 "/dev/shm/t19/q$3/t$t.jpg"; done
  fi
' "$ROT" "$LOG" "$OUTD" "$NN" "${ARGS[@]}"
tail -3 "$LOG"
[[ -f "$OUTD/t19-cap$NN.mp4" ]] && mv -f "$OUTD/t19-cap$NN.mp4" "/dev/shm/t19/t19-cap$NN.$TAG.mp4"
[[ -f "$OUTD/t19-cap$NN.contact.jpg" ]] && mv -f "$OUTD/t19-cap$NN.contact.jpg" "/dev/shm/t19/t19-cap$NN.$TAG.contact.jpg"
python3 -I rec/t19/resumo.py "$NN" $([[ $ENS == 1 ]] && echo --ens) | grep -vE "^ +[0-9]+ (mark|wait|pause) " | head -80
echo "SEM ALVO no log: $(grep -v 'SEMENTE' "$LOG" | grep -c 'SEM ALVO')"
