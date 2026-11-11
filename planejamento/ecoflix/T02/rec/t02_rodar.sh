#!/usr/bin/env bash
# T2 · grava UM capítulo sob a trava pesada: o ensaio rápido (--ens: sem os `at`, com o MP4 e a folha de contato) ou a gravação completa.
# Saídas em /dev/shm/t02rec (o disco de /home está quase cheio); o actions.json e o telemetry.json voltam para rec/t02/ (ou
# rec/t02/_ens/), que o resumo.py e o prever.py leem. O MP4 e a folha de contato ficam só em /dev/shm: apague depois de olhar.
#   TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<qualquer> bash rec/t02/t02_rodar.sh 03 [--ens]
# A senha vem só do ambiente (o setup do capítulo entra pela tela de login com "$TUT_USER"/"$TUT_SENHA"); nunca vai para arquivo.
# A linha final diz os quadros por segundo da captura e o maior atraso: com a máquina carregada (render de cenas ao lado, até
# 17:35 de 11/11) a captura cai para ~9 qps e os gestos atrasam até 2,5 s; aí o atraso é da carga, não do roteiro: grave de novo.
set -euo pipefail
EU=$(readlink -f "$0")
cd "$(dirname "$EU")/../.."   # $TUT_HOME
N=$(printf %02d "$((10#$1))")
ENS=${2:-}
PORTA=54302
export FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:$PORTA
: "${TUT_USER:?defina TUT_USER no ambiente}" "${TUT_SENHA:?defina TUT_SENHA no ambiente}"
# a instância ainda é a minha (porta e FAKE_NOW)?
pid=$(cat "rec/.runtime/fake$PORTA.pid")
amb=$(tr '\0' '\n' < "/proc/$pid/environ")
grep -qx "FAKE_PORT=$PORTA" <<<"$amb" || { echo "a instância $PORTA não é a minha (pid $pid)"; exit 1; }
grep -qx "FAKE_NOW=$FAKE_NOW" <<<"$amb" || { echo "FAKE_NOW da instância $PORTA não é $FAKE_NOW"; exit 1; }
OUT=/dev/shm/t02rec
mkdir -p "$OUT"
if [ "$ENS" = "--ens" ]; then
  python3 -I rec/t02/ensaio.py "$N"
  ln -sfn ../assets rec/t02/_ens/assets   # o upload do cap05 usa assets/ relativo à pasta do roteiro
  ROT=rec/t02/_ens/cap$N.json
  DEST=rec/t02/_ens
  EXTRA=   # o rápido também monta o MP4: a folha de contato dele é a conferência da tela (regra de 11/11, 18:46)
else
  ROT=rec/t02/cap$N.json
  DEST=rec/t02
  EXTRA=
fi
rm -f "$OUT/t02-cap$N".*
st=0
flock .heavy.lock node rec/record.mjs "$ROT" --out "$OUT" $EXTRA > "$OUT/t02-cap$N.log" 2>&1 || st=$?
cp "$OUT/t02-cap$N.actions.json" "$OUT/t02-cap$N.telemetry.json" "$DEST/" 2>/dev/null || true
grep -E "FALHOU|seeds extras|^saidas" "$OUT/t02-cap$N.log" || true
qps=$(python3 -I -c "import json,sys; a=json.load(open(sys.argv[1])); print(a['stats'].get('captureFps'), a['late']['maxS'])" "$OUT/t02-cap$N.actions.json" 2>/dev/null || echo "? ?")
echo "cap$N ${ENS:-completo}: saída $st ($(date +%H:%M:%S)) · qps/atraso máx $qps"
