#!/usr/bin/env bash
# T22 · ensaio de um capítulo. Uso: bash rec/t22/t22_ens.sh NN [--completo] [--estado]
#   (sem opção)  ensaio RÁPIDO: rec/t22/_ens/capNN.json sem os `at` (ensaio.py), sem MP4; saídas em rec/t22/_ens/ e resumo.py --ens
#   --completo   ensaio COMPLETO com os tempos estimados (o roteiro rec/t22/capNN.json), com MP4 e folha de contato em /dev/shm/t22rec
#                (o MP4 e a folha ficam lá para olhar e apagar); actions/telemetry em rec/t22/; resumo.py
#   --estado     depois da gravação e DENTRO da mesma trava, grava a semente apos-capNN a partir do banco (t22_estado.py)
# Vários capítulos podem esperar a trava ao mesmo tempo (cada um com a sua): cada gravação zera e semeia a minha instância (porta 54322,
# FAKE_NOW 2026-11-10 08:30). Por isso este script NÃO religa a instância: se ela não for a minha, para (religar é à mão, sem gravação
# minha em curso). O roteiro é gerado de novo DENTRO da trava (gerar.py, ~0,1 s), para a fila nunca gravar um roteiro velho.
set -uo pipefail
cd /home/claude/ecoflix
export TUT_HOME=/home/claude/ecoflix FAKE_URL=http://127.0.0.1:54322 FAKE_NOW=2026-11-10T08:30:00-03:00
export TUT_USER=rafael@reciclavalemetais.example
if [ -z "${TUT_SENHA:-}" ]; then TUT_SENHA="$(python3 -I -c 'import secrets; print(secrets.token_urlsafe(9))')"; fi
export TUT_SENHA
NN=$(printf '%02d' "$((10#$1))"); shift
N=$((10#$NN))
MODO=rapido; ESTADO=""
for a in "$@"; do case "$a" in --completo) MODO=completo ;; --estado) ESTADO=1 ;; *) echo "opção desconhecida: $a"; exit 2 ;; esac; done
PIDF=rec/.runtime/fake54322.pid
minha() { local p; p=$(cat $PIDF 2>/dev/null || echo 0); grep -qz "^FAKE_PORT=54322\$" /proc/$p/environ 2>/dev/null && grep -qz "^FAKE_NOW=$FAKE_NOW\$" /proc/$p/environ 2>/dev/null && curl -s -o /dev/null --max-time 3 http://127.0.0.1:54322/health; }
if ! minha; then echo "INSTÂNCIA 54322 NÃO É A MINHA OU NÃO RESPONDE: religue com FAKE_NOW=$FAKE_NOW FAKE_PORT=54322 bash rec/run.sh fake"; exit 4; fi
TMP=/dev/shm/t22rec
mkdir -p rec/t22/_ens rec/t22/_estado
if [ "$MODO" = rapido ]; then
  PREP="python3 -I rec/t22/gerar.py $N > /dev/null && python3 -I rec/t22/ensaio.py $N > /dev/null"
  REC="node rec/record.mjs rec/t22/_ens/cap$NN.json --out $TMP --name t22-cap$NN --no-encode"
  DEST=rec/t22/_ens; LOG=rec/t22/_ens/.cap$NN.out
else
  PREP="python3 -I rec/t22/gerar.py $N > /dev/null"
  REC="node rec/record.mjs rec/t22/cap$NN.json --out $TMP --name t22-cap$NN"
  DEST=rec/t22; LOG=rec/t22/.cap$NN.out
fi
CMD="$PREP && mkdir -p $TMP && timeout 900 $REC; rc=\$?; mv -f $TMP/t22-cap$NN.actions.json $TMP/t22-cap$NN.telemetry.json $DEST/ 2>/dev/null; rm -rf $TMP/_frames;"
if [ -n "$ESTADO" ]; then
  CMD="$CMD if [ \$rc = 0 ]; then python3 -I rec/t22/t22_estado.py $N > rec/t22/_estado/cap$NN.log 2>&1 || echo ESTADO-FALHOU; fi;"
fi
CMD="$CMD exit \$rc"
flock .heavy.lock nice -n 5 bash -c "$CMD" > "$LOG" 2>&1
RC=$?
echo "=== cap$NN ($MODO) rc=$RC $(date +%H:%M)"
tail -3 "$LOG" | cut -c1-240
[ -n "$ESTADO" ] && { echo "--- estado do cap$NN:"; tail -20 rec/t22/_estado/cap$NN.log 2>/dev/null; }
if [ "$MODO" = rapido ]; then python3 -I rec/t22/resumo.py "$N" --ens 2>&1 | head -80; else python3 -I rec/t22/resumo.py "$N" 2>&1 | head -90; fi
grep -h "SEM ALVO" "$LOG" 2>/dev/null | head -3
