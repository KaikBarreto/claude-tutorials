#!/usr/bin/env bash
# T2 · enfileira UMA exploração na trava pesada. Uso: bash rec/t2/_explorar_na_fila.sh <cenario sem .mjs> <sementes separadas por vírgula> [e-mail]
# (a senha de demonstração é gerada dentro da trava e não aparece na linha de comando)
cd /home/claude/domiflix || exit 1
c="$1"; sem="$2"; mail="${3:-}"
nohup flock .heavy.lock nice -n 10 bash -c '
  export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54324 FAKE_NOW="2026-11-03T09:00:00-03:00"
  export TUT_SENHA="$(bash rec/t2/senha_demo.sh)"
  node rec/t2/explorar.mjs rec/t2/_ex/$0.mjs '"${mail:+$mail}"' --seed $1 > rec/t2/_debug/$0.log 2>&1
  echo "fim rc=$?" >> rec/t2/_debug/$0.log' "$c" "$sem" > /dev/null 2>&1 &
echo "na fila: $c ($sem) pid $!"
