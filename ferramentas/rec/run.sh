#!/usr/bin/env bash
# Sobe e derruba o ambiente de gravacao: Supabase falso (porta 54321) + app da Dominex (porta 8080).
#   rec/run.sh build      gera o build de producao do app (app/dist) apontado para o Supabase falso (3 a 8 min, 1x)
#   rec/run.sh up         sobe os dois; usa app/dist se existir (rapido, como o sistema real), senao o vite dev
#   rec/run.sh up --dev   forca o vite dev (lento: centenas de modulos soltos por rota)
#   rec/run.sh fake       reinicia SO o Supabase falso (recarrega seeds/handlers; o app continua)
#   rec/run.sh down       derruba os dois
#   rec/run.sh status     mostra PIDs e se respondem
#   rec/run.sh logs       ultimas linhas dos logs
# So mexe nos PIDs que ele mesmo criou (rec/.runtime/*.pid). Nunca usa pkill.
set -euo pipefail

REC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="$(dirname "$REC")/app"
RUN="$REC/.runtime"
mkdir -p "$RUN"

cfg() { node -e 'console.log(require(process.argv[1])[process.argv[2]])' "$REC/env.json" "$1"; }
FAKE_PORT_PADRAO="$(cfg fakePort)"
FAKE_PORT="${FAKE_PORT:-$FAKE_PORT_PADRAO}"
# instância extra do Supabase falso (outro agente em paralelo): FAKE_PORT=54322 rec/run.sh fake|down|status
# (o app continua um só; o robô desvia as chamadas com FAKE_URL=http://127.0.0.1:54322)
if [ "$FAKE_PORT" = "$FAKE_PORT_PADRAO" ]; then FK=fake; else FK="fake$FAKE_PORT"; fi
APP_PORT="$(cfg appPort)"
ANON_KEY="$(cfg anonKey)"
PROJECT_ID="$(cfg projectId)"
TILES_PATH="$(cfg tilesPath)"

# variaveis que o app le (e que o build "assa" no codigo)
app_env() {
  export VITE_SUPABASE_URL="http://127.0.0.1:$FAKE_PORT"
  export VITE_SUPABASE_PUBLISHABLE_KEY="$ANON_KEY"
  export VITE_SUPABASE_PROJECT_ID="$PROJECT_ID"
  export VITE_MAP_TILES_URL="http://127.0.0.1:$FAKE_PORT$TILES_PATH"
}

pid_of() { cat "$RUN/$1.pid" 2>/dev/null || true; }

# o PID guardado ainda e o NOSSO processo? (evita matar outro que reaproveitou o numero)
is_ours() {
  local name="$1" pid args
  pid="$(pid_of "$name")"
  [ -n "$pid" ] || return 1
  kill -0 "$pid" 2>/dev/null || return 1
  args="$(ps -o args= -p "$pid" 2>/dev/null || true)"
  case "$name" in
    fake*) [[ "$args" == *"server.mjs"* ]] ;;
    app) [[ "$args" == *"vite"* || "$args" == *"serve-dist"* ]] ;;
  esac
}

stop_one() {
  local name="$1" pid
  if is_ours "$name"; then
    pid="$(pid_of "$name")"
    kill "$pid" 2>/dev/null || true
    for _ in $(seq 1 30); do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.2
    done
    kill -0 "$pid" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
    echo "parado: $name (pid $pid)"
  fi
  rm -f "${RUN:?}/$name.pid"
}

wait_http() { # url, tentativas (0,5s cada)
  local url="$1" n="${2:-60}"
  for _ in $(seq 1 "$n"); do
    if curl -s -o /dev/null --max-time 2 "$url"; then return 0; fi
    sleep 0.5
  done
  return 1
}

start_fake() {
  stop_one "$FK"
  (
    cd "$REC/fakebase"
    FAKE_PORT="$FAKE_PORT" nohup node server.mjs >"$RUN/${FK/fake/fakebase}.log" 2>&1 &
    echo $! >"$RUN/$FK.pid"
  )
  if wait_http "http://127.0.0.1:$FAKE_PORT/health" 40; then
    echo "fakebase de pe: http://127.0.0.1:$FAKE_PORT (pid $(pid_of "$FK"))"
  else
    echo "fakebase nao respondeu; veja $RUN/fakebase.log" >&2
    tail -n 20 "$RUN/fakebase.log" >&2 || true
    return 1
  fi
}

start_app() {
  local mode="${1:-auto}"
  [ -d "$APP/node_modules" ] || { echo "app nao instalado em $APP — rode rec/setup-app.sh" >&2; return 1; }
  if is_ours app; then
    echo "app ja de pe (pid $(pid_of app))"
    return 0
  fi
  rm -f "${RUN:?}/app.pid"
  if [ "$mode" != "dev" ] && [ -f "$APP/dist/index.html" ]; then
    (
      nohup node "$REC/recorder/serve-dist.mjs" "$APP/dist" "$APP_PORT" >"$RUN/app.log" 2>&1 &
      echo $! >"$RUN/app.pid"
    )
    echo "app: build de producao (app/dist)"
  else
    [ "$mode" = "dev" ] || echo "AVISO: app/dist nao existe; subindo o vite dev (lento). Rode rec/run.sh build para gerar o build." >&2
    (
      cd "$APP"
      app_env
      nohup node node_modules/.bin/vite --host 127.0.0.1 --port "$APP_PORT" --strictPort >"$RUN/app.log" 2>&1 &
      echo $! >"$RUN/app.pid"
    )
    echo "app: vite dev"
  fi
  if wait_http "http://127.0.0.1:$APP_PORT/" 120; then
    echo "app de pe: http://127.0.0.1:$APP_PORT (pid $(pid_of app))"
  else
    echo "app nao respondeu; veja $RUN/app.log" >&2
    tail -n 20 "$RUN/app.log" >&2 || true
    return 1
  fi
}

build_app() {
  [ -d "$APP/node_modules" ] || { echo "app nao instalado em $APP — rode rec/setup-app.sh" >&2; return 1; }
  stop_one app # libera CPU e memoria para o build
  rm -rf "${APP:?}/dist"
  echo "gerando o build de producao (use so 1 CPU livre; leva alguns minutos)... log: $RUN/build.log"
  (
    cd "$APP"
    app_env
    export NODE_OPTIONS="--max-old-space-size=5120"
    node node_modules/.bin/vite build >"$RUN/build.log" 2>&1
  ) || { echo "build falhou; ultimas linhas:" >&2; tail -n 25 "$RUN/build.log" >&2; return 1; }
  tail -n 3 "$RUN/build.log"
  [ -f "$APP/dist/index.html" ] && echo "build pronto: $APP/dist"
}

status_one() {
  local name="$1" url="$2"
  if is_ours "$name"; then
    local code
    code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "$url" || true)"
    echo "$name: pid $(pid_of "$name") responde http $code ($url)"
  else
    echo "$name: parado"
  fi
}

case "${1:-}" in
  build) build_app ;;
  up)
    is_ours "$FK" && echo "fakebase ja de pe (pid $(pid_of "$FK"))" || start_fake
    if [ "${2:-}" = "--dev" ]; then start_app dev; else start_app auto; fi
    ;;
  fake) start_fake ;;
  down)
    [ "$FK" = fake ] && stop_one app   # instância extra: só o fakebase dela (o app é compartilhado)
    stop_one "$FK"
    ;;
  status)
    status_one "$FK" "http://127.0.0.1:$FAKE_PORT/health"
    status_one app "http://127.0.0.1:$APP_PORT/"
    ;;
  logs)
    for f in fakebase app build; do
      echo "== $f.log =="
      tail -n 15 "$RUN/$f.log" 2>/dev/null || true
    done
    ;;
  *)
    sed -n 2,13p "$0"
    exit 1
    ;;
esac
