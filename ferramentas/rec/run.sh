#!/usr/bin/env bash
# Sobe e derruba o ambiente de gravacao: Supabase falso (porta 54321) + app da Dominex (porta 8080).
# Mundo de outra serie (rec/mundo, instalado pelo PERFIL, ou FAKE_MUNDO=<pasta>): schema, sementes, handlers e enderecos
# (mundo.json "env": porta padrao do fakebase, chave, app) vem de la; sem ele, o mundo da Dominex de sempre.
#   rec/run.sh build      gera o build de producao do app (app/dist) apontado para o Supabase falso (3 a 8 min, 1x)
#                         APP_WORK=<pasta> (a do rec/setup-app.sh): builda la (ex.: /dev/shm) e traz so o dist para app/
#   rec/run.sh up         sobe os dois; usa app/dist se existir (rapido, como o sistema real), senao o vite dev
#   rec/run.sh up --dev   forca o vite dev (lento: centenas de modulos soltos por rota)
#   rec/run.sh fake       reinicia SO o Supabase falso (recarrega seeds/handlers; o app continua)
#   rec/run.sh app        sobe SO o app (8080); cada agente sobe o proprio fakebase (FAKE_PORT=... rec/run.sh fake)
#   rec/run.sh down       derruba os dois
#   rec/run.sh status     mostra PIDs e se respondem
#   rec/run.sh logs       ultimas linhas dos logs
# So mexe nos PIDs que ele mesmo criou (rec/.runtime/*.pid). Nunca usa pkill.
set -euo pipefail

REC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="$(dirname "$REC")/app"
RUN="$REC/.runtime"
mkdir -p "$RUN"

MUNDO="${FAKE_MUNDO:-$REC/mundo}"
if [ -f "$MUNDO/schema.json" ]; then export FAKE_MUNDO="$MUNDO"; else MUNDO=""; fi
# valor de rec/env.json, com o "env" do mundo.json por cima
cfg() {
  node -e 'const fs=require("fs");const a=JSON.parse(fs.readFileSync(process.argv[1],"utf8"));let m={};
    try{m=JSON.parse(fs.readFileSync(process.argv[3],"utf8")).env||{}}catch(e){}
    console.log(process.argv[2] in m ? m[process.argv[2]] : a[process.argv[2]])' "$REC/env.json" "$1" "${MUNDO:-/nada}/mundo.json"
}
FAKE_PORT_PADRAO="$(cfg fakePort)"
FAKE_PORT="${FAKE_PORT:-$FAKE_PORT_PADRAO}"
# instância extra do Supabase falso (outro agente em paralelo): FAKE_PORT=54322 rec/run.sh fake|down|status
# (o app continua um só; o robô desvia as chamadas com FAKE_URL=http://127.0.0.1:54322)
if [ "$FAKE_PORT" = "$FAKE_PORT_PADRAO" ]; then FK=fake; else FK="fake$FAKE_PORT"; fi
# com um mundo, cada instancia anota as lacunas no proprio arquivo (duas instancias nao se apagam)
[ -n "$MUNDO" ] && export FAKE_UNKNOWN_LOG="${FAKE_UNKNOWN_LOG:-$RUN/desconhecidos$FAKE_PORT.log}"
APP_WORK="${APP_WORK:-$APP}"
# data do mundo: a do mundo.json ("env.fakeNow") quando a pessoa nao passou FAKE_NOW (o robo usa a mesma)
if [ -z "${FAKE_NOW:-}" ] && [ -n "$MUNDO" ]; then
  FN="$(cfg fakeNow)"; [ "$FN" != "undefined" ] && export FAKE_NOW="$FN"
fi
APP_PORT="$(cfg appPort)"
ANON_KEY="$(cfg anonKey)"
PROJECT_ID="$(cfg projectId)"
TILES_PATH="$(cfg tilesPath)"

# variaveis que o app le (e que o build "assa" no codigo): sempre o endereco gravado (fakeUrl), que o robo desvia
# para a instancia de cada um (FAKE_URL)
BAKED_URL="$(cfg fakeUrl)"
BAKED_URL="${BAKED_URL%/}"
app_env() {
  export VITE_SUPABASE_URL="$BAKED_URL"
  export VITE_SUPABASE_PUBLISHABLE_KEY="$ANON_KEY"
  export VITE_SUPABASE_PROJECT_ID="$PROJECT_ID"
  export VITE_MAP_TILES_URL="$BAKED_URL$TILES_PATH"
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

# Serviço que fica de pé (fake, app) não pode herdar a trava pesada: chamado de dentro de um flock, o processo segura a
# trava enquanto viver (05/11/2026: o 8080 subiu sob o flock da troca de versão e parou a fila de 5 agentes por 50 min).
# Chame dentro do subshell, logo antes do nohup: fecha todo descritor que aponte para um arquivo *.heavy.lock.
fecha_trava() {
  local fd alvo
  for fd in /proc/"$BASHPID"/fd/*; do
    alvo="$(readlink "$fd" 2>/dev/null || true)"
    case "$alvo" in
      *.heavy.lock) eval "exec ${fd##*/}>&-" ;;
    esac
  done
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
    fecha_trava
    FAKE_PORT="$FAKE_PORT" nohup node server.mjs >"$RUN/${FK/fake/fakebase}.log" 2>&1 &
    echo $! >"$RUN/$FK.pid"
  )
  if wait_http "http://127.0.0.1:$FAKE_PORT/health" 40; then
    echo "fakebase de pe: http://127.0.0.1:$FAKE_PORT (pid $(pid_of "$FK"))${MUNDO:+ mundo $MUNDO}${FAKE_NOW:+ FAKE_NOW=$FAKE_NOW}"
  else
    echo "fakebase nao respondeu; veja $RUN/${FK/fake/fakebase}.log" >&2
    tail -n 20 "$RUN/${FK/fake/fakebase}.log" >&2 || true
    return 1
  fi
}

start_app() {
  local mode="${1:-auto}"
  [ -d "$APP/node_modules" ] || [ -f "$APP/dist/index.html" ] || { echo "app nao instalado em $APP — rode rec/setup-app.sh" >&2; return 1; }
  if is_ours app; then
    echo "app ja de pe (pid $(pid_of app))"
    return 0
  fi
  rm -f "${RUN:?}/app.pid"
  if [ "$mode" != "dev" ] && [ -f "$APP/dist/index.html" ]; then
    (
      fecha_trava
      nohup node "$REC/recorder/serve-dist.mjs" "$APP/dist" "$APP_PORT" >"$RUN/app.log" 2>&1 &
      echo $! >"$RUN/app.pid"
    )
    echo "app: build de producao (app/dist)"
  else
    [ "$mode" = "dev" ] || echo "AVISO: app/dist nao existe; subindo o vite dev (lento). Rode rec/run.sh build para gerar o build." >&2
    [ -d "$APP_WORK/node_modules" ] || { echo "vite dev precisa do codigo com node_modules (APP_WORK=$APP_WORK)" >&2; return 1; }
    (
      cd "$APP_WORK"
      app_env
      fecha_trava
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

# lista de um campo do <mundo>/app/ajustes.json (uma linha por item)
ajustes() {
  [ -n "$MUNDO" ] && [ -f "$MUNDO/app/ajustes.json" ] || return 0
  node -e 'for (const x of (require(process.argv[1])[process.argv[2]] || [])) console.log(x)' "$MUNDO/app/ajustes.json" "$1"
}

build_app() {
  [ -d "$APP_WORK/node_modules" ] || { echo "app nao instalado em $APP_WORK — rode rec/setup-app.sh (com o mesmo APP_WORK)" >&2; return 1; }
  stop_one app # libera CPU e memoria para o build
  rm -rf "${APP_WORK:?}/dist"
  echo "gerando o build de producao em $APP_WORK (use so 1 CPU livre; leva alguns minutos)... log: $RUN/build.log"
  (
    cd "$APP_WORK"
    app_env
    while IFS= read -r c; do [ -n "$c" ] && { echo "antes do build: $c"; bash -c "$c"; }; done < <(ajustes antesDoBuild)
    export NODE_OPTIONS="--max-old-space-size=${BUILD_MEM_MB:-5120}"
    node node_modules/.bin/vite build >"$RUN/build.log" 2>&1
  ) || { echo "build falhou; ultimas linhas:" >&2; tail -n 25 "$RUN/build.log" >&2; return 1; }
  tail -n 3 "$RUN/build.log"
  [ -f "$APP_WORK/dist/index.html" ] || { echo "build sem dist/index.html" >&2; return 1; }
  # versao do app gravada (o robo marca no localStorage que "ja viu" as novidades desta versao)
  sed -n 's/.*APP_VERSION *= *["'"'"']\([^"'"'"']*\)["'"'"'].*/\1/p' "$APP_WORK/src/config/version.ts" 2>/dev/null | head -n 1 >"$APP_WORK/dist/.versao-app" || true
  if [ "$APP_WORK" != "$APP" ]; then
    # so o resultado vai para o disco (sem as pastas do site que o app gravado nao usa)
    local ex=() p
    while IFS= read -r p; do [ -n "$p" ] && ex+=(--exclude="./$p"); done < <(ajustes foraDoBuild)
    rm -rf "${APP:?}/dist.novo"
    mkdir -p "$APP/dist.novo"
    tar -C "$APP_WORK/dist" "${ex[@]}" -cf - . | tar -C "$APP/dist.novo" -xf -
    rm -rf "${APP:?}/dist"
    mv "$APP/dist.novo" "$APP/dist"
    echo "dist copiado para $APP/dist ($(du -sh "$APP/dist" | cut -f1)${ex[*]:+; fora: ${ex[*]}})"
  fi
  echo "build pronto: $APP/dist (versao $(cat "$APP/dist/.versao-app" 2>/dev/null || echo '?'))"
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
  app) start_app auto ;;
  down)
    [ "$FK" = fake ] && stop_one app   # instância extra: só o fakebase dela (o app é compartilhado)
    stop_one "$FK"
    ;;
  status)
    status_one "$FK" "http://127.0.0.1:$FAKE_PORT/health"
    status_one app "http://127.0.0.1:$APP_PORT/"
    ;;
  logs)
    for f in "${FK/fake/fakebase}" app build; do
      echo "== $f.log =="
      tail -n 15 "$RUN/$f.log" 2>/dev/null || true
    done
    ;;
  *)
    sed -n 2,16p "$0"
    exit 1
    ;;
esac
