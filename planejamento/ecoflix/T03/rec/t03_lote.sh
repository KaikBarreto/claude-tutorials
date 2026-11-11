#!/usr/bin/env bash
# T03 · ensaio (rápido ou completo) de vários capítulos, UMA trava por capítulo (docs/04: os jobs dos outros agentes entram entre os meus).
#   TUT_USER=... TUT_SENHA=... bash rec/t03/t03_lote.sh rapido 00 01 01b 02 ...     (ensaio.py + record.mjs --rapido + resumo.py --ens)
#   TUT_USER=... TUT_SENHA=... bash rec/t03/t03_lote.sh completo 00 01 ...          (record.mjs com os `at` + resumo.py)
# O prazo (timeout) vale por capítulo e roda DENTRO da trava (a espera na fila não conta). Apaga o MP4 logo depois do resumo; a folha de
# contato fica para olhar (apague depois de ver). Saída de cada capítulo: rec/t03[/_ens]/.capNN.out e o resumo em .capNN.resumo.
# Nunca edite este arquivo com um lote rodando (o bash lê o script aos poucos): copie para outro nome.
# T03_LOTE_MIN (padrão 110): o lote para sozinho antes desse tempo. A espera na fila usa `flock -w` com o que sobra (menos o prazo do
# capítulo), para nenhum corte de tempo da ferramenta cair no meio de uma gravação com a trava na mão.
set -u
limite=$(( $(date +%s) + ${T03_LOTE_MIN:-110} * 60 ))
cd "${TUT_HOME:-$(dirname "$0")/../..}" || exit 1   # $TUT_HOME (rodando uma cópia fora daqui: passe TUT_HOME)
: "${TUT_USER:?defina TUT_USER}" "${TUT_SENHA:?defina TUT_SENHA}"
export TUT_USER TUT_SENHA FAKE_URL=http://127.0.0.1:54303 FAKE_NOW=2026-11-10T08:30:00-03:00
modo="$1"; shift
for nn in "$@"; do
  if [ "$modo" = rapido ]; then
    python3 -I rec/t03/ensaio.py "$nn" >/dev/null
    dir=rec/t03/_ens; extra=--rapido; prazo=420; res="--ens"
  else
    dir=rec/t03; extra=""; prazo=600; res=""
  fi
  # a instância ainda é a minha? (RELIGAR.md)
  pid=$(cat rec/.runtime/fake54303.pid 2>/dev/null)
  if ! tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -q '^FAKE_PORT=54303$'; then echo "cap$nn: instância 54303 fora do ar"; exit 2; fi
  espera=$(( limite - $(date +%s) - prazo - 60 ))
  if [ "$espera" -lt 60 ]; then echo "== cap$nn e seguintes: sem tempo neste lote (rode de novo)"; break; fi
  echo "== cap$nn ($modo) fila $(date +%T)"
  flock -w "$espera" .heavy.lock bash -c "echo \"   trava \$(date +%T)\"; timeout $prazo node rec/record.mjs $dir/cap$nn.json $extra" > "$dir/.cap$nn.out" 2>&1
  rc=$?
  if ! grep -q "trava" "$dir/.cap$nn.out"; then echo "   sem vez na fila até $(date +%T): cap$nn e seguintes ficam para o próximo lote"; break; fi
  echo "   fim $(date +%T) rc=$rc"
  grep -h "FALHOU\|SEM ALVO" "$dir/.cap$nn.out" | head -3
  python3 -I rec/t03/resumo.py "$nn" $res > "$dir/.cap$nn.resumo" 2>&1
  head -2 "$dir/.cap$nn.resumo"
  case "$nn" in 02|03|04|05|06|07|08) python3 -I rec/t03/t03_estado.py "$nn" > "$dir/.cap$nn.estado" 2>&1; tail -1 "$dir/.cap$nn.estado";; esac
  [ "$nn" = 09 ] && python3 -I rec/t03/t03_pdfs.py | tail -1   # os PDFs do app (a próxima gravação reinicia o falso)
  rm -f "/home/claude/ecoflix/$dir/t03-cap$nn.mp4"
done
