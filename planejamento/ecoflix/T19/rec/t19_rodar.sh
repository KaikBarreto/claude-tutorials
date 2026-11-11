#!/usr/bin/env bash
# T19 · UM capítulo por trava: gera o roteiro e, na MESMA trava, grava o ensaio rápido (--ens) e/ou o completo (--final; só se o
# rápido chegou ao fim), roda o
# prever.py depois do rápido e, com --seed, grava a semente apos-capNN (só de uma gravação que chegou ao fim: record exit 0).
# MP4 e folha de contato vão para /dev/shm/t19 (apagar depois de olhar); actions/telemetry ficam em rec/t19 (o prever.py usa).
#   bash rec/t19/t19_rodar.sh NN [--ens] [--final] [--seed] [--quadros "t1 t2 ..."]     (sem --ens/--final: só --ens)
#   Pela fila justa da trava (rec/fila.sh --prio 19, um capítulo por vez). PRAZO_FIM=<epoch>: se a vez chegar a menos de 12 min do
#   prazo do lote, não grava (saída 5), para o lote em segundo plano não morrer no meio de uma gravação.
#   MP4 de ensaio (rápido e completo) com --preset ultrafast --crf 30: só para a folha de contato.
# Instância: FAKE_PORT 54319 (só desta aula), FAKE_NOW 2026-11-10T08:30:00-03:00. Precisa de TUT_USER e TUT_SENHA no ambiente.
set -uo pipefail
TUT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$TUT_HOME"
NN=$(printf %02d "$((10#$1))"); shift
ENS=0; FIN=0; SEED=0; QUADROS=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --ens) ENS=1 ;;
    --final) FIN=1 ;;
    --seed) SEED=1 ;;
    --quadros) QUADROS="$2"; shift ;;
  esac
  shift
done
[[ $ENS == 0 && $FIN == 0 ]] && ENS=1
export FAKE_URL=http://127.0.0.1:54319 FAKE_NOW=2026-11-10T08:30:00-03:00
: "${TUT_USER:?falta TUT_USER}" "${TUT_SENHA:?falta TUT_SENHA}"
PID=$(cat rec/.runtime/fake54319.pid 2>/dev/null || true)
AMB=$( [[ -n "$PID" ]] && tr '\0' '\n' < "/proc/$PID/environ" 2>/dev/null || true)
if [[ "$AMB" != *$'\nFAKE_PORT=54319\n'* && "$AMB" != FAKE_PORT=54319$'\n'* ]] || [[ "$AMB" != *"FAKE_NOW=$FAKE_NOW"* ]]; then
  echo "instância 54319 não é a desta aula (ou caiu): FAKE_NOW=$FAKE_NOW FAKE_PORT=54319 bash rec/run.sh fake"; exit 4
fi
python3 -I rec/t19/gerar.py "$NN" | tail -2
[[ $ENS == 1 ]] && python3 -I rec/t19/ensaio.py "$NN"
mkdir -p /dev/shm/t19
export NN ENS FIN SEED QUADROS PRAZO_FIM="${PRAZO_FIM:-0}"
bash /home/claude/ecoflix/rec/fila.sh --prio 19 -- bash -c '
  set -uo pipefail
  if (( PRAZO_FIM > 0 && $(date +%s) > PRAZO_FIM - 720 )); then echo "PRAZO: a vez chegou tarde, não gravei" > rec/t19/.cap$NN.prazo; exit 5; fi
  rm -f rec/t19/.cap$NN.prazo
  falhos() { python3 -c "import json,sys;a=json.load(open(sys.argv[1]));print(sum(1 for x in a[\"actions\"] if x.get(\"error\") or x.get(\"ok\") is False))" "$1" 2>/dev/null || echo X; }
  semalvo() { grep -v SEMENTE "$1" | grep -c "SEM ALVO" || true; }
  boa=""
  if [[ $ENS == 1 ]]; then
    L=rec/t19/.cap$NN.ens.out
    timeout 900 node rec/record.mjs rec/t19/_ens/cap$NN.json --rapido --preset ultrafast --crf 30 > "$L" 2>&1; echo "record exit $?" >> "$L"
    grep -q "^record exit 0$" "$L" && boa=ens   # a semente só precisa do capítulo inteiro (passo opcional falho não muda o banco)
    python3 -I rec/t19/prever.py "$NN" --ens > rec/t19/.cap$NN.prever.out 2>&1
  fi
  if [[ $FIN == 1 && $ENS == 1 && -z "$boa" ]]; then
    echo "completo NÃO gravado: o rápido não chegou ao fim" > rec/t19/.cap$NN.final.out
  elif [[ $FIN == 1 ]]; then
    boa=""   # a semente sai do estado da ÚLTIMA gravação
    L=rec/t19/.cap$NN.final.out
    timeout 900 node rec/record.mjs rec/t19/cap$NN.json --preset ultrafast --crf 30 > "$L" 2>&1; echo "record exit $?" >> "$L"
    grep -q "^record exit 0$" "$L" && boa=final
    if [[ -n "$QUADROS" && -f rec/t19/t19-cap$NN.mp4 ]]; then
      mkdir -p /dev/shm/t19/q$NN
      for t in $QUADROS; do ffmpeg -loglevel error -y -ss "$t" -i rec/t19/t19-cap$NN.mp4 -frames:v 1 -vf scale=1280:-1 "/dev/shm/t19/q$NN/t$t.jpg"; done
    fi
  fi
  if [[ $SEED == 1 ]]; then
    if [[ -n "$boa" ]]; then node rec/t19/t19_semente.mjs "apos-cap$NN" > rec/t19/.cap$NN.semente.out 2>&1; echo "semente ($boa): $(cat rec/t19/.cap$NN.semente.out)";
    else echo "SEMENTE NAO GRAVADA (nenhuma gravação limpa)" | tee rec/t19/.cap$NN.semente.out; fi
  fi
  exit 0
'
RC=$?
[[ -f rec/t19/.cap$NN.prazo ]] && { cat rec/t19/.cap$NN.prazo; exit 5; }
for T in ens final; do
  D=rec/t19; [[ $T == ens ]] && D=rec/t19/_ens
  [[ -f "$D/t19-cap$NN.mp4" ]] && mv -f "$D/t19-cap$NN.mp4" "/dev/shm/t19/t19-cap$NN.$T.mp4"
  [[ -f "$D/t19-cap$NN.contact.jpg" ]] && mv -f "$D/t19-cap$NN.contact.jpg" "/dev/shm/t19/t19-cap$NN.$T.contact.jpg"
done
if [[ $ENS == 1 ]]; then
  echo "== ENSAIO RÁPIDO cap$NN"; tail -1 rec/t19/.cap$NN.ens.out
  python3 -I rec/t19/resumo.py "$NN" --ens | grep -vE "^ +[0-9]+ (mark|wait|pause) " | grep -E 'falhos|ERRO|DIFERENTE|SEM ALVO|avisos de erro|conferências' | head -30
  echo "SEM ALVO no log: $(grep -v SEMENTE rec/t19/.cap$NN.ens.out | grep -c 'SEM ALVO')"
  echo "== PREVER cap$NN"; grep -E 'previsto|>= ?0[.,]8|L[0-9]+ ' rec/t19/.cap$NN.prever.out | head -12
fi
if [[ $FIN == 1 ]]; then
  echo "== COMPLETO cap$NN"; tail -1 rec/t19/.cap$NN.final.out
  python3 -I rec/t19/resumo.py "$NN" | grep -vE "^ +[0-9]+ (wait|pause) " | head -90
  echo "SEM ALVO no log: $(grep -v SEMENTE rec/t19/.cap$NN.final.out | grep -c 'SEM ALVO')"
fi
[[ $SEED == 1 ]] && cat rec/t19/.cap$NN.semente.out
exit 0
