#!/usr/bin/env bash
# Prepara, sem instalar nada no sistema, um Python com Tk 8.6 (Xft, fontes de verdade) para rodar as janelas do EcoTray
# (dashboard.py e installer_gui.py) num display virtual. Tudo fica em $CENA_WIN_CACHE (padrão /dev/shm/cena-windows):
#   tkroot/   pacotes do Ubuntu baixados com apt-get download e só extraídos (python3-tk, libtk8.6, libtcl8.6, libxft2, BLT)
#   venv/     Python do sistema que casa com o _tkinter extraído + Pillow + websockets (o painel usa os dois)
#   fonts/    Montserrat (a fonte do painel) e Inconsolata (no lugar da Consolas do Windows, que não é livre)
#   fonts.conf  fontconfig próprio: as fontes acima, "Consolas"/"Menlo" -> Inconsolata, sem emoji colorido (derruba o Xft)
#   env.sh    variáveis para rodar o Python com Tk (fonte: source env.sh)
# Rede: archive.ubuntu.com (pacotes), raw.githubusercontent.com (fontes), pypi (Pillow, websockets).
# Rode de novo à vontade: o que já existe é reaproveitado. Depois de reiniciar a máquina o /dev/shm some e o
# capturar_ecotray.py chama este script sozinho.
set -euo pipefail
C="${CENA_WIN_CACHE:-/dev/shm/cena-windows}"
mkdir -p "$C"/{debs,tkroot,fonts,fccache,apt/lists/partial,apt/cache/archives/partial}
C="$(cd "$C" && pwd)"
A=(-o Dir::State::Lists="$C/apt/lists" -o Dir::Cache="$C/apt/cache" -o Debug::NoLocking=1)

# 1) Tk 8.6 com Xft (o Python do python-build-standalone traz Tk sem Xft: fontes de bitmap, sem Montserrat)
if ! ls "$C"/tkroot/usr/lib/python3*/lib-dynload/_tkinter*.so >/dev/null 2>&1 || ! ls "$C"/tkroot/usr/lib/libBLT*.so* >/dev/null 2>&1; then
  command -v apt-get >/dev/null || { echo "sem apt-get: instale um Python com tkinter (Tk 8.6 com Xft) e aponte CENA_WIN_PY"; exit 1; }
  echo "baixando Tk 8.6 (pacotes do Ubuntu, só extraídos)..."
  apt-get "${A[@]}" update >/dev/null 2>&1 || true
  (cd "$C/debs" && apt-get "${A[@]}" download python3-tk libtk8.6 libtcl8.6 libxft2 tk8.6-blt2.5 >/dev/null 2>&1)
  for d in "$C"/debs/*.deb; do dpkg-deb -x "$d" "$C/tkroot"; done
fi
SO="$(ls "$C"/tkroot/usr/lib/python3*/lib-dynload/_tkinter*.so | head -1)"
PYV="$(basename "$(dirname "$(dirname "$SO")")")"            # ex.: python3.12
# o Python do próprio Ubuntu (o _tkinter extraído é compilado para ele); um python3.X de outro lugar no PATH não serve
PYSYS="${CENA_WIN_PY:-}"; [ -n "$PYSYS" ] || { [ -x "/usr/bin/$PYV" ] && PYSYS="/usr/bin/$PYV"; } || PYSYS="$(command -v "$PYV" || true)"
[ -n "$PYSYS" ] || { echo "o _tkinter extraído é do $PYV, que não existe nesta máquina"; exit 1; }

# 2) venv com Pillow e websockets (+ o tkinter extraído via .pth)
if [ ! -x "$C/venv/bin/python" ]; then
  echo "criando venv ($PYV) com Pillow e websockets..."
  if command -v uv >/dev/null; then
    UV_CACHE_DIR="$C/uvcache" uv venv -q --no-python-downloads --python "$PYSYS" "$C/venv"
    VIRTUAL_ENV="$C/venv" UV_CACHE_DIR="$C/uvcache" uv pip install -q pillow websockets
  else
    "$PYSYS" -m venv "$C/venv" && "$C/venv/bin/pip" install -q pillow websockets
  fi
fi
SP="$("$C/venv/bin/python" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
printf '%s\n%s\n' "$C/tkroot/usr/lib/$PYV" "$C/tkroot/usr/lib/$PYV/lib-dynload" > "$SP/cena_windows_tk.pth"

# 3) fontes: Montserrat 400/700 (o painel usa normal e bold) e Inconsolata (monoespaçada no lugar da Consolas)
baixa() { [ -s "$C/fonts/$1" ] || curl -sSfL --retry 3 -o "$C/fonts/$1" "$2"; }
baixa Montserrat-Regular.ttf "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Regular.ttf"
baixa Montserrat-Bold.ttf "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Bold.ttf"
# Inconsolata estática (a variável sai com o espaçamento errado no Xft)
baixa Inconsolata-Regular.ttf "https://raw.githubusercontent.com/googlefonts/Inconsolata/main/fonts/ttf/Inconsolata-Regular.ttf"
baixa Inconsolata-Bold.ttf "https://raw.githubusercontent.com/googlefonts/Inconsolata/main/fonts/ttf/Inconsolata-Bold.ttf"

cat > "$C/fonts.conf" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <cachedir>$C/fccache</cachedir>
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
  <dir>$C/fonts</dir>
  <alias binding="same"><family>Consolas</family><prefer><family>Inconsolata</family></prefer></alias>
  <alias binding="same"><family>Menlo</family><prefer><family>Inconsolata</family></prefer></alias>
  <selectfont><rejectfont><glob>*NotoColorEmoji*</glob></rejectfont></selectfont>
  <!-- o Xft dá a toda letra de fonte "mono" a largura do maior glifo (na Inconsolata, 20 px): medir letra a letra -->
  <match target="font"><test name="family"><string>Inconsolata</string></test><edit name="spacing" mode="assign"><const>proportional</const></edit></match>
</fontconfig>
EOF

cat > "$C/env.sh" <<EOF
export CENA_WIN_CACHE="$C"
export CENA_WIN_TKPY="$C/venv/bin/python"
export FONTCONFIG_FILE="$C/fonts.conf"
export LD_LIBRARY_PATH="$C/tkroot/usr/lib/x86_64-linux-gnu:$C/tkroot/usr/lib\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
export TCL_LIBRARY="$C/tkroot/usr/share/tcltk/tcl8.6"
export TK_LIBRARY="$C/tkroot/usr/share/tcltk/tk8.6"
EOF
# conferência: Tk 8.6 com a Montserrat visível
( source "$C/env.sh"; "$CENA_WIN_TKPY" -c 'import tkinter; print("Tk", tkinter.TkVersion)' ) >/dev/null
echo "pronto: $C (source $C/env.sh)"
