#!/usr/bin/env bash
# T0 · um capítulo pela fila (um por chamada). uso: bash rec/t00/t00_um.sh NN[b] [--completo]   (b = celular 9:16)
# Rápido (padrão): rec/t00/_ens/capNN.json com --rapido; completo: rec/t00/capNN.json. MP4 leve (ultrafast, crf 30) só para a folha de contato.
# Precisa de TUT_SENHA (8+ caracteres) no ambiente; a instância é a 54300.
set -u
cd "$(dirname "$0")/../.."
a="$1"; modo="${2:-}"
n="${a%b}"; suf=""; [ "$a" != "$n" ] && suf=".9x16"
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54300 TUT_USER=rafael@reciclavalemetais.example
: "${TUT_SENHA:?defina TUT_SENHA (8+ caracteres) no ambiente}"
curl -sf http://127.0.0.1:54300/health >/dev/null || { echo "instância 54300 fora do ar: FAKE_NOW=$FAKE_NOW FAKE_PORT=54300 bash rec/run.sh fake"; exit 3; }
if [ "$modo" = "--completo" ]; then
  arq="rec/t00/cap$n$suf.json"; out="rec/t00/.cap$a.out"; extra=""; ens=""
else
  arq="rec/t00/_ens/cap$n$suf.json"; out="rec/t00/_ens/cap$a.out"; extra="--rapido"; ens="--ens"
fi
bash rec/fila.sh --prio 00 -- node rec/record.mjs "$arq" $extra --preset ultrafast --crf 30 >"$out" 2>&1
echo "rc=$? ($arq)"; tail -n 3 "$out" | cut -c1-300
grep -n "SEM ALVO\|DIFERENTE" "$out" | cut -c1-260 | head
python3 -I rec/t00/resumo.py "$a" $ens > "$out.resumo" 2>&1; grep -m2 -A1 "passos, vídeo" "$out.resumo" | cut -c1-220
grep -in "FALHOU\|not found\|timeout\|SEM ALVO\|DIFERENTE\|sem botao\|ja fechada\|=> \"\[\"" "$out.resumo" | cut -c1-240 | head -n 12
[ "$modo" = "--completo" ] && awk '$5+0>=0.4 || /late +[0-9]/' "$out.resumo" | grep -v " late   -" | cut -c1-200 | head -n 12
true
