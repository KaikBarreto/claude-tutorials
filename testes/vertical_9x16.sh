#!/usr/bin/env bash
# Confere o formato VERTICAL 9:16 (1080x1920) do perfil Domiflix (T0 v2, pedido do Kaik 31/10): as peças verticais têm a mesma
# identidade, o mesmo som e a mesma duração das do 16:9 e respeitam a área segura. O 16:9 NÃO é testado aqui: para isso rode
# `bash testes/identidade_domiflix.sh` (tem de dar "IDÊNTICO ao T3") antes e depois de mexer em qualquer arquivo compartilhado.
#   flock $TUT_HOME/.heavy.lock nice -n 10 bash testes/vertical_9x16.sh        (~3 min; Python, Node + Playwright, ffmpeg; sem rede)
#   MANTER=<pasta> bash testes/vertical_9x16.sh    copia os quadros conferidos (e uma amostra da animação) para a pasta, para olhar
# Confere: 1) palco vertical = o palco do 16:9 girado 90° (bit a bit); 2) vinheta de capítulo: mesma duração e voz do 16:9, texto
# na área segura, título >= 44 px em até 3 linhas; 3) vinheta de abertura e cartela: 1080x1920, mesmo número de quadros e SOM
# IDÊNTICO ao do 16:9 (testes/referencias_domiflix/audio.sha256), conteúdo claro só dentro da área segura; 3b) as mesmas
# checagens na vinheta e na cartela verticais da EcoFlix (estilo ecosistema-reciclagem; som igual ao do 16:9 dela); 4) legendas de 32
# caracteres por linha; 5) o adaptador render_chapter_vertical.py; 6) o molde das cenas verticais: render, guias e a auditoria
# (aprova o exemplo e reprova texto pequeno).
set -euo pipefail
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; REF="$SKILL/testes/referencias_domiflix"
TMP="$(mktemp -d)"; trap 'rm -rf "${TMP:?}"' EXIT
H="$TMP/home"; mkdir -p "$H/t/edit" "$TMP/proj"
for d in kit audio web; do cp -r "$SKILL/ferramentas/$d" "$H/$d"; done
tar -C "$SKILL/ferramentas/edit" --exclude=node_modules --exclude=__pycache__ -cf - . | tar -C "$H/t/edit" -xf -; cp -r "$SKILL/perfis/domiflix/marca" "$H/marca"
M="${MODELOS:-${TUT_HOME:-$HOME/tutoriais}/models}"
if [ -f "$M/GeneralUser-GS.sf2" ]; then ln -s "$M" "$H/models"; else
  mkdir -p "$H/models"; curl -sSL --retry 3 -o "$H/models/GeneralUser-GS.sf2" https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2
fi
OUT="$TMP/quadros"; mkdir -p "$OUT"; ruim=0; E="$H/t/edit"
ok() { echo "  ok   $1"; }; falha() { echo "  FALHA $1"; ruim=$((ruim + 1)); }

echo "1) palco escuro vertical"
python3 "$E/fundo_escuro.py" "$TMP/fundo16.png" >/dev/null; python3 "$E/fundo_escuro_vertical.py" "$TMP/fundo9.png" >/dev/null
python3 - "$TMP" <<'EOF' && ok "palco 1080x1920 = palco do 16:9 girado 90°, idêntico" || falha "palco vertical"
import sys, numpy as np, cv2
t = sys.argv[1]; a = cv2.imread(f"{t}/fundo16.png"); b = cv2.imread(f"{t}/fundo9.png")
assert b.shape == (1920, 1080, 3), b.shape
assert np.array_equal(np.rot90(a, -1), b), "o palco vertical não é o do 16:9 girado"
EOF

echo "2) vinheta de capítulo vertical"
python3 -I - "$H" "$TMP/fundo9.png" "$OUT" <<'EOF' && ok "vinheta de capítulo: duração/voz do 16:9, texto na área segura, título >= 44 px" || falha "vinheta de capítulo"
import sys, numpy as np, cv2
H, fundo, out = sys.argv[1:4]
sys.path.insert(0, f"{H}/t/edit"); sys.path.insert(0, f"{H}/kit")
import vinheta_cap as V16, vinheta_cap_vertical as V9, vertical as V
assert (V9.DUR, V9.VOZ_AT) == (V16.DUR, V16.VOZ_AT) and V9.dur_for(1.64) == V16.dur_for(1.64) and V9.dur_for(3.4) == V16.dur_for(3.4), "duração diferente do 16:9"
bg = cv2.cvtColor(cv2.imread(fundo), cv2.COLOR_BGR2RGB); cinza = np.full((1920, 1080, 3), 128, np.uint8)
for kicker, title in (("Assinatura", "Quando a empresa cresce"), ("Clientes", "Cliente empresa pelo CNPJ"), ("Resumo", "Os combinados do onboarding da Dominex com o suporte e o plano"), ("", "Curto")):
    c = V9.Card(kicker, title, bg, dur=V9.dur_for(1.64))
    assert c.size >= V.TEXTO_MIN and len(c.tit) <= V9.MAX_LINHAS, (title, c.size, len(c.tit))
    for cx in c.caixas():
        assert not V.caixa_fora_da_segura(cx), (title, cx)
    img = c.frame(1.6, cinza, cinza); assert img.shape == (1920, 1080, 3)
c = V9.Card("Assinatura", "Quando a empresa cresce", bg, dur=V9.dur_for(1.64))
cv2.imwrite(f"{out}/card_v_1.60.png", cv2.cvtColor(c.frame(1.6, cinza, cinza), cv2.COLOR_RGB2BGR))
EOF

echo "3) vinheta de abertura e cartela verticais (navegador)"
PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')" \
  bash "$H/kit/brand_clips_vertical.sh" "$TMP/proj" "Boas-vindas à Dominex" "Até a próxima aula!" >/dev/null
B="$TMP/proj/build"
for t in 1.0 2.2 3.4; do ffmpeg -v error -y -ss "$t" -i "$B/intro_v.mp4" -frames:v 1 "$OUT/abertura_v_$t.png"; done
ffmpeg -v error -y -ss 2.6 -i "$B/outro_v.mp4" -frames:v 1 "$OUT/cartela_v_2.6.png"
for t in 0.3 0.7 1.2 1.6 1.9 2.6 3.0 3.8 4.2; do ffmpeg -v error -y -ss "$t" -i "$B/intro_v.mp4" -frames:v 1 "$OUT/anim_abertura_$t.png"; done  # só para olhar (MANTER)
for t in 0.8 1.1 1.4 1.8 3.4; do ffmpeg -v error -y -ss "$t" -i "$B/outro_v.mp4" -frames:v 1 "$OUT/anim_cartela_$t.png"; done
python3 -I - "$REF" "$OUT" "$B" "$H/t/edit" <<'EOF' && ok "vinhetas: 1080x1920, mesma duração, som idêntico ao do 16:9, conteúdo na área segura" || falha "vinhetas verticais"
import hashlib, os, subprocess, sys, json, numpy as np, cv2, soundfile as sf
ref, out, build, edit = sys.argv[1:5]; sys.path.insert(0, edit); import vertical as V
ruim = 0
for linha in open(os.path.join(ref, "audio.sha256")):  # o som do 16:9 (T3): o vertical usa a mesma linha do tempo e os mesmos CUES
    h, nome = linha.split()[:2]; n16 = int(linha.split()[-2])
    x, _ = sf.read(os.path.join(build, nome), dtype="float32", always_2d=True)
    igual = hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest() == h and len(x) == n16
    print(f"    {nome:18s} amostras {'idênticas às do 16:9' if igual else 'DIFERENTES'}"); ruim += not igual
for nome, quadros in (("intro_v.mp4", 133), ("outro_v.mp4", 116)):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=width,height,nb_read_frames,r_frame_rate", "-of", "json", os.path.join(build, nome)], capture_output=True, text=True, check=True).stdout)["streams"][0]
    igual = (j["width"], j["height"], int(j["nb_read_frames"]), j["r_frame_rate"]) == (1080, 1920, quadros, "30/1")
    print(f"    {nome:18s} {j['width']}x{j['height']} {j['nb_read_frames']} quadros {j['r_frame_rate']}  {'ok' if igual else 'DIFERENTE (esperado 1080x1920, %d quadros, 30/1)' % quadros}"); ruim += not igual
for f in sorted(x for x in os.listdir(out) if x.startswith(("abertura_v", "cartela_v"))):
    r = V.fora_da_area_segura(cv2.cvtColor(cv2.imread(os.path.join(out, f)), cv2.COLOR_BGR2RGB))
    print(f"    {f:22s} {'conteúdo dentro da área segura' if not r else 'FORA DA ÁREA SEGURA ' + str(r)}"); ruim += bool(r)
sys.exit(1 if ruim else 0)
EOF

echo "3b) vinheta de abertura e cartela verticais da EcoFlix (estilo ecosistema-reciclagem, navegador)"
for f in 9x16 16x9; do  # a do 16:9 só serve de referência do som (mesma linha do tempo = mesmas amostras)
  S="brand_clips.sh"; [ "$f" = 9x16 ] && S="brand_clips_vertical.sh"; mkdir -p "$TMP/eco$f"
  PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')" \
    MARCA_JSON="$SKILL/perfis/ecoflix/marca" bash "$H/kit/$S" "$TMP/eco$f" "Bem-vindo ao EcoSistema" "Até a próxima aula!" >/dev/null
done
B9="$TMP/eco9x16/build"
for t in 1.0 2.2 3.4; do ffmpeg -v error -y -ss "$t" -i "$B9/intro_v.mp4" -frames:v 1 "$OUT/eco_abertura_v_$t.png"; done
ffmpeg -v error -y -ss 2.6 -i "$B9/outro_v.mp4" -frames:v 1 "$OUT/eco_cartela_v_2.6.png"
python3 -I - "$TMP/eco16x9/build" "$B9" "$OUT" "$H/t/edit" <<'EOF' && ok "EcoFlix: 1080x1920, mesma duração, som idêntico ao do 16:9 dela, conteúdo na área segura" || falha "vinhetas verticais da EcoFlix"
import hashlib, os, subprocess, sys, json, numpy as np, cv2, soundfile as sf
b16, b9, out, edit = sys.argv[1:5]; sys.path.insert(0, edit); import vertical as V
som = lambda p: hashlib.sha256(np.ascontiguousarray(sf.read(p, dtype="float32", always_2d=True)[0]).tobytes()).hexdigest()  # noqa: E731
ruim = 0
for nome in ("intro_audio.wav", "outro_audio.wav"):
    igual = som(os.path.join(b16, nome)) == som(os.path.join(b9, nome))
    print(f"    {nome:18s} amostras {'idênticas às do 16:9' if igual else 'DIFERENTES das do 16:9'}"); ruim += not igual
for nome, quadros in (("intro_v.mp4", 133), ("outro_v.mp4", 116)):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=width,height,nb_read_frames,r_frame_rate", "-of", "json", os.path.join(b9, nome)], capture_output=True, text=True, check=True).stdout)["streams"][0]
    igual = (j["width"], j["height"], int(j["nb_read_frames"]), j["r_frame_rate"]) == (1080, 1920, quadros, "30/1")
    print(f"    {nome:18s} {j['width']}x{j['height']} {j['nb_read_frames']} quadros {j['r_frame_rate']}  {'ok' if igual else 'DIFERENTE (esperado 1080x1920, %d quadros, 30/1)' % quadros}"); ruim += not igual
for f in sorted(x for x in os.listdir(out) if x.startswith("eco_")):
    r = V.fora_da_area_segura(cv2.cvtColor(cv2.imread(os.path.join(out, f)), cv2.COLOR_BGR2RGB))
    print(f"    {f:26s} {'conteúdo dentro da área segura' if not r else 'FORA DA ÁREA SEGURA ' + str(r)}"); ruim += bool(r)
sys.exit(1 if ruim else 0)
EOF

echo "4) legendas de 32 caracteres por linha"
python3 -I - "$SKILL/ferramentas/narracao" <<'EOF' && ok "legendas: linhas <= 32 caracteres, até 2 linhas" || falha "legendas verticais"
import sys; sys.path.insert(0, sys.argv[1])
import legendas as L
txt = "E funciona assim: se você aumenta o plano no meio do caminho, paga hoje só a diferença, proporcional aos dias que faltam até o vencimento. Os recursos novos entram assim que o pagamento é confirmado, e a renovação seguinte já vem com o valor do plano novo."
ws = [{"w": w, "s": i * 0.35, "e": i * 0.35 + 0.3} for i, w in enumerate(txt.split())]
L.MAXL = 32
bl = L.blocos(ws)
for b in bl:
    ls = L.linhas(" ".join(w["w"] for w in b)); assert len(ls) <= 2 and max(map(len, ls)) <= 32, ls
print(f"    {len(bl)} legendas; a maior linha tem {max(len(l) for b in bl for l in L.linhas(' '.join(w['w'] for w in b)))} caracteres")
EOF

echo "5) adaptador do capítulo vertical (render_chapter_vertical.py)"
mkdir -p "$TMP/cap" && cd "$TMP/cap"
ffmpeg -v error -y -f lavfi -i "color=c=0x202020:s=1080x1920:r=30:d=2" -f lavfi -i "aevalsrc=t/3:s=48000:d=3" -map 0:v -c:v libx264 -pix_fmt yuv420p -t 2 v.mp4 -map 1:a -c:a pcm_f32le -t 3 n.wav
echo '{"name":"cap01","video":"v.mp4","narration":"n.wav","audio_offset":-0.5,"trim":{"start":0,"end":2.0},"output":{"dir":"out"}}' > cap01.chapter.json
python3 -I "$E/render_chapter_vertical.py" cap01.chapter.json >/dev/null
python3 - <<'EOF' && ok "sidecar: 60 quadros, WAV de 2 s, vídeo sem recodificar" || falha "adaptador do capítulo"
import json, soundfile as sf
s = json.load(open("out/cap01.edit.json")); x, sr = sf.read(s["wav"])
assert s["frames"] == 60 and abs(s["dur"] - 2.0) < 1e-6 and s["video"].endswith("v.mp4") and sr == 48000 and len(x) == 96000, s
# narração = rampa t/3; com audio_offset -0,5 o instante 1,0 s do vídeo é o 1,5 s da narração (0,5)
assert abs(x[48000] - 0.5) < 0.01, f"audio_offset mal aplicado: {x[48000]:.3f} (esperado 0.5)"
EOF
echo '{"name":"cap01","video":"v.mp4","trim":{"start":0.5,"end":2.0},"output":{"dir":"out2"}}' > ruim.chapter.json
python3 -I "$E/render_chapter_vertical.py" ruim.chapter.json >/dev/null 2>&1 && falha "trim parcial deveria ser recusado" || ok "trim parcial recusado (gere o trecho com --de/--ate)"

echo "6) molde das cenas verticais (navegador)"
CE="$E/cenas"; mkdir -p "$H/t/edit/assets"; cp "$TMP/fundo9.png" "$H/t/edit/assets/fundo_escuro_9x16.png"
if [ -d "$SKILL/ferramentas/edit/cenas/node_modules/lucide-static" ]; then ln -sfn "$SKILL/ferramentas/edit/cenas/node_modules" "$CE/node_modules"; else (cd "$CE" && npm install --no-audit --no-fund >/dev/null 2>&1); fi  # ícones lucide
cp "$CE/cenas_modelo_vertical.html" "$CE/cenas_vertical.html"; sed 's/font-size:68px/font-size:30px/' "$CE/cenas_modelo_vertical.html" > "$CE/cenas_ruim.html"
echo '{"dur":6.0,"words":[{"w":"Agenda,","linha":1,"s":1.0,"e":1.4},{"w":"clientes","linha":1,"s":2.0,"e":2.5},{"w":"e","linha":1,"s":2.6,"e":2.7},{"w":"financeiro.","linha":1,"s":3.0,"e":3.6}],"linhas":[{"i":0,"s":0.2,"e":0.9},{"i":1,"s":1.0,"e":5.0}]}' > "$TMP/narr.json"
node "$CE/render_cenas_vertical.cjs" 0 "$TMP/narr.json" "$OUT/cena" --stills 0.5,4.5 --guias --html "$CE/cenas_vertical.html" >/dev/null
node "$CE/render_cenas_vertical.cjs" 0 "$TMP/narr.json" "$OUT/cena" --stills 4.5 --html "$CE/cenas_vertical.html" >/dev/null
[ -s "$OUT/cena/cap00_4.50.png" ] && ok "quadros do molde (com e sem guias)" || falha "quadros do molde"
node "$CE/render_cenas_vertical.cjs" 0 "$TMP/narr.json" - --auditar --passo 0.5 --html "$CE/cenas_vertical.html" | tail -2 && ok "auditoria aprova o exemplo do molde" || falha "auditoria deveria aprovar o exemplo"
if node "$CE/render_cenas_vertical.cjs" 0 "$TMP/narr.json" - --auditar --passo 0.5 --html "$CE/cenas_ruim.html" > "$TMP/audit_ruim.txt"; then falha "auditoria deveria reprovar texto de 30 px"
else grep -q "texto pequeno" "$TMP/audit_ruim.txt" && ok "auditoria reprova texto abaixo de 44 px" || falha "auditoria reprovou por outro motivo"; fi

[ -z "${MANTER:-}" ] || { mkdir -p "$MANTER"; cp -r "$OUT/." "$MANTER/"; }
echo; [ "$ruim" -eq 0 ] && echo "VERTICAL 9:16 OK" || echo "$ruim verificação(ões) falharam no vertical 9:16"
exit $((ruim > 0))
