#!/usr/bin/env bash
# Prepara a área de trabalho de um tutorial a partir desta skill.
#
#   TUT_HOME=~/tutoriais TUTORIAL=t1 MARCA=/caminho/da/marca bash instalar.sh
#
#   TUT_HOME  raiz da área de trabalho (padrão ~/tutoriais). Recebe kit/ audio/ web/ models/ rec/ marca/ e a trava
#             .heavy.lock que serializa as tarefas pesadas.
#   TUTORIAL  id do tutorial (padrão t1): cria $TUT_HOME/$TUTORIAL/{edit,narracao} e $TUT_HOME/rec/$TUTORIAL.
#             As gravações do robô se chamam <id>-capNN (ex.: t1-cap03).
#   PERFIL    perfil pronto de uma série (pasta perfis/<nome>): marca, voz, pronúncias e padrão de montagem.
#             PERFIL=domiflix = o padrão do T3 da Dominex, idêntico. Sem perfil: modelos neutros.
#             Perfil com mundo fictício próprio (perfis/<nome>/mundo: schema, sementes, handlers do Supabase falso) instala
#             em $TUT_HOME/rec/mundo, e o rec/run.sh e o robô passam a usar esse mundo (PERFIL=ecoflix).
#   MARCA     pasta com marca.json + arquivos da marca (logo, fontes). Padrão: a do PERFIL, senão modelos/.
#   APP_SRC   código do app (git archive da versão publicada). Se a marca tem som próprio da vinheta fora do git
#             ("vinheta.som" + "som_origem", ex.: EcoFlix), ele é copiado daí para $TUT_HOME/marca.
#
# Rode de novo para outro tutorial (só TUTORIAL muda); arquivos que já existem não são sobrescritos.
# Rede: github.com e raw.githubusercontent.com (modelos), pypi.org, registry.npmjs.org.
set -euo pipefail
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; F="$SKILL/ferramentas"
TUT_HOME="${TUT_HOME:-$HOME/tutoriais}"; TUTORIAL="${TUTORIAL:-t1}"; PERFIL="${PERFIL:-}"; P=""
if [ -n "$PERFIL" ]; then
  P="$SKILL/perfis/$PERFIL"; [ -d "$P" ] || { echo "perfil '$PERFIL' não existe em perfis/"; exit 1; }
  MARCA="${MARCA:-$P/marca}"
fi
MARCA="${MARCA:-$SKILL/modelos}"
mkdir -p "$TUT_HOME"; TUT_HOME="$(cd "$TUT_HOME" && pwd)"

# kit (vinheta, cartela, trilha, SFX, fontes, ASR) + modelos + dependências Python
DOMI="$TUT_HOME" bash "$F/kit/setup.sh"

# marca: marca.json + logo/fontes (não sobrescreve uma marca já instalada)
mkdir -p "$TUT_HOME/marca"
if [ ! -f "$TUT_HOME/marca/marca.json" ]; then
  [ -f "$MARCA/marca.json" ] || { echo "MARCA=$MARCA não tem marca.json"; exit 1; }
  cp -r "$MARCA/." "$TUT_HOME/marca/"
fi
# som próprio da vinheta (mídia: não vai para o git): copia do código do app; sem ele, a vinheta usa o sintetizado
SOM="$(python3 -c 'import json,sys; v=json.load(open(sys.argv[1])).get("vinheta") or {}; print(v.get("som","") if isinstance(v,dict) else "", v.get("som_origem","") if isinstance(v,dict) else "", sep="\t")' "$TUT_HOME/marca/marca.json")"
SOM_DST="$(printf '%s' "$SOM" | cut -f1)"; SOM_ORIG="$(printf '%s' "$SOM" | cut -f2)"
if [ -n "$SOM_DST" ] && [ ! -f "$TUT_HOME/marca/$SOM_DST" ]; then
  if [ -n "${APP_SRC:-}" ] && [ -n "$SOM_ORIG" ] && [ -f "$APP_SRC/$SOM_ORIG" ]; then
    mkdir -p "$(dirname "$TUT_HOME/marca/$SOM_DST")"; cp "$APP_SRC/$SOM_ORIG" "$TUT_HOME/marca/$SOM_DST"
    echo "som da vinheta: $APP_SRC/$SOM_ORIG -> marca/$SOM_DST"
  else
    echo "AVISO: falta o som da vinheta (marca/$SOM_DST). Rode de novo com APP_SRC=<código do app> (copia $SOM_ORIG);"
    echo "       sem ele, a vinheta sai com o som sintetizado."
  fi
fi

# gravador, editor e narração do tutorial
mkdir -p "$TUT_HOME/rec/$TUTORIAL" "$TUT_HOME/$TUTORIAL/edit/caps" "$TUT_HOME/$TUTORIAL/edit/out" "$TUT_HOME/$TUTORIAL/narracao"
cp -r --update=none "$F/rec/." "$TUT_HOME/rec/"
# mundo fictício do perfil (sem ele, o Supabase falso usa o mundo que mora em rec/fakebase, o da Dominex)
if [ -n "$P" ] && [ -d "$P/mundo" ]; then
  mkdir -p "$TUT_HOME/rec/mundo"
  cp -r --update=none "$P/mundo/." "$TUT_HOME/rec/mundo/"
fi
# kit do robô por aula (ensaio rápido, resumo com a palavra falada, prévia do ritmo, explorador): o id da aula é o nome da pasta
cp --update=none "$F/rec/molde/"*.py "$F/rec/molde/"*.mjs "$TUT_HOME/rec/$TUTORIAL/"
cp -r --update=none "$F/edit/." "$TUT_HOME/$TUTORIAL/edit/"
cp -r --update=none "$F/narracao/." "$TUT_HOME/$TUTORIAL/narracao/"
pega() { [ -n "$P" ] && [ -f "$P/$1" ] && echo "$P/$1" || echo "$SKILL/modelos/$(basename "$1")"; }  # perfil > modelo
for f in config_narracao.json tts_textos.py; do
  [ -f "$TUT_HOME/$TUTORIAL/narracao/$f" ] || cp "$(pega "narracao/$f")" "$TUT_HOME/$TUTORIAL/narracao/$f"
done
[ -f "$TUT_HOME/$TUTORIAL/edit/caps/specs.json" ] || cp "$(pega specs.json)" "$TUT_HOME/$TUTORIAL/edit/caps/specs.json"
[ -f "$TUT_HOME/$TUTORIAL/edit/caps/aula.modelo.json" ] || cp "$(pega aula.json)" "$TUT_HOME/$TUTORIAL/edit/caps/aula.modelo.json"
if [ -n "$P" ]; then
  # kit de ilustração da série (ex.: perfis/ecoflix/cenas: cenas_ecoflix.html + exemplo/) ao lado do cenas_modelo.html
  [ -d "$P/cenas" ] && cp -r --update=none "$P/cenas/." "$TUT_HOME/$TUTORIAL/edit/cenas/"
  [ -f "$P/voz.json" ] && cp --update=none "$P/voz.json" "$TUT_HOME/$TUTORIAL/narracao/voz.json"
  [ -f "$P/PERFIL.md" ] && cp --update=none "$P/PERFIL.md" "$TUT_HOME/$TUTORIAL/PERFIL.md"
fi
# palco escuro na cor de acento da marca (com a marca Dominex sai idêntico ao do T3)
[ -f "$TUT_HOME/$TUTORIAL/edit/assets/fundo_escuro.png" ] || python3 "$TUT_HOME/$TUTORIAL/edit/fundo_escuro.py" >/dev/null
touch "$TUT_HOME/.heavy.lock"

pip install --break-system-packages -q num2words 2>&1 | grep -v -i warning || pip install -q num2words 2>&1 | grep -v -i warning || true
# robô: Playwright + Chromium (em muitas máquinas já vem instalado; senão instala)
if ! node -e "require('playwright')" >/dev/null 2>&1; then
  (cd "$TUT_HOME/rec" && npm install --no-audit --no-fund playwright >/dev/null 2>&1 && npx playwright install chromium >/dev/null 2>&1) \
    || echo "AVISO: instale o Playwright e o Chromium (npm i playwright && npx playwright install chromium)"
fi
command -v ffmpeg >/dev/null || echo "AVISO: ffmpeg não encontrado (necessário para gravar e montar)"

echo "pronto: $TUT_HOME (tutorial $TUTORIAL${PERFIL:+, perfil $PERFIL}, marca em $TUT_HOME/marca)"
[ -n "$P" ] && echo "leia $TUT_HOME/$TUTORIAL/PERFIL.md: o padrão da série vale inteiro"
echo "próximo: roteiro (modelos/roteiro.md) e narração; depois rec/<id>/capNN.json e a gravação (docs/04-gravacao.md)"
