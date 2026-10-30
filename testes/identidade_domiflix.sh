#!/usr/bin/env bash
# Garante que o perfil Domiflix continua IDÊNTICO ao T3 (Kaik, 30/10: "nos próximos tutoriais não se perca nada").
# Renderiza com as ferramentas deste repositório + perfis/domiflix/marca e compara com referências tiradas dos
# arquivos reais do T3 (testes/referencias_domiflix/): palco escuro, cartão de capítulo, vinheta de abertura e cartela.
#   bash testes/identidade_domiflix.sh        (~2 min; Python, Node + Playwright, ffmpeg; sem rede)
# Passa se a diferença média de cada quadro for < 1 nível (0-255). Rode antes de publicar qualquer mudança visual.
set -euo pipefail
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; REF="$SKILL/testes/referencias_domiflix"
TMP="$(mktemp -d)"; trap 'rm -rf "${TMP:?}"' EXIT
H="$TMP/home"; mkdir -p "$H/t/edit" "$TMP/proj"
for d in kit audio web; do cp -r "$SKILL/ferramentas/$d" "$H/$d"; done
cp -r "$SKILL/ferramentas/edit/." "$H/t/edit/"; cp -r "$SKILL/perfis/domiflix/marca" "$H/marca"
# SoundFont da assinatura sonora: da pasta de modelos já instalada (MODELOS ou $TUT_HOME/models) ou baixa só ele
M="${MODELOS:-${TUT_HOME:-$HOME/tutoriais}/models}"
if [ -f "$M/GeneralUser-GS.sf2" ]; then ln -s "$M" "$H/models"; else
  mkdir -p "$H/models"; curl -sSL --retry 3 -o "$H/models/GeneralUser-GS.sf2" https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2
fi
OUT="$TMP/quadros"; mkdir -p "$OUT"

# palco e cartão de capítulo (mesmas entradas das referências: fundo gerado, quadros vizinhos cinza, t = 1,6 s)
python3 "$H/t/edit/fundo_escuro.py" "$TMP/fundo.png" >/dev/null
python3 - "$H" "$TMP/fundo.png" "$OUT" <<'EOF'
import sys, numpy as np, cv2
H, fundo, out = sys.argv[1:4]
sys.path.insert(0, f"{H}/t/edit"); sys.path.insert(0, f"{H}/kit")
import vinheta_cap as VC
bg = cv2.cvtColor(cv2.imread(fundo), cv2.COLOR_BGR2RGB); cinza = np.full((1080, 1920, 3), 128, np.uint8)
small = lambda im: cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
card = VC.Card("Clientes", "Cliente empresa pelo CNPJ", bg, dur=4.23)
cv2.imwrite(f"{out}/card_1.60.png", cv2.cvtColor(small(card.frame(1.6, cinza, cinza)), cv2.COLOR_RGB2BGR))
cv2.imwrite(f"{out}/fundo_escuro.png", cv2.cvtColor(small(bg), cv2.COLOR_RGB2BGR))
EOF

# vinheta de abertura e cartela (mesmo título e frase do T3)
bash "$H/kit/brand_clips.sh" "$TMP/proj" "Clientes, Fornecedores e Equipamentos" "Até a próxima aula!" >/dev/null
B="$TMP/proj/build"
for t in 1.0 2.2 3.4; do ffmpeg -v error -y -ss "$t" -i "$B/intro_v.mp4" -frames:v 1 -vf scale=960:540:flags=area "$OUT/abertura_$t.png"; done
ffmpeg -v error -y -ss 2.6 -i "$B/outro_v.mp4" -frames:v 1 -vf scale=960:540:flags=area "$OUT/cartela_2.6.png"

python3 - "$REF" "$OUT" "$B" <<'EOF'
import hashlib, os, sys, numpy as np, cv2, soundfile as sf
ref, out, build = sys.argv[1:4]; ruim = 0
for linha in open(os.path.join(ref, "audio.sha256")):  # som da vinheta e da cartela: amostras idênticas às do T3
    h, nome = linha.split()[:2]
    x, _ = sf.read(os.path.join(build, nome), dtype="float32", always_2d=True)
    ok = hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest() == h
    print(f"{nome:20s} amostras {'idênticas' if ok else 'DIFERENTES'}"); ruim += not ok
for f in sorted(x for x in os.listdir(ref) if x.endswith(".png")):
    a = cv2.imread(os.path.join(ref, f)).astype(np.int16); b = cv2.imread(os.path.join(out, f))
    if b is None: print(f"{f:20s} FALTOU"); ruim += 1; continue
    d = np.abs(a - b.astype(np.int16)); ok = d.mean() < 1.0
    print(f"{f:20s} dif. média {d.mean():5.2f} | máx {int(d.max()):3d}  {'ok' if ok else 'DIFERENTE'}"); ruim += not ok
print("IDÊNTICO ao T3" if not ruim else f"{ruim} quadro(s) diferente(s) do T3: o perfil Domiflix mudou")
sys.exit(1 if ruim else 0)
EOF
