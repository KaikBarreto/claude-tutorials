#!/usr/bin/env python3
"""T18 · montagem rápida do cap. 15 (Recapitulando): trechos das gravações dos capítulos 1 a 14, acelerados e emendados, no ritmo da fala.

O cap. 15 grava só a base (o Início da Área do Técnico, com o cursor passando pelos cartões). Esta montagem vira uma ilustração em
vídeo (a janela do app inteira, 16:10) que o editor cola SOBRE a janela em repouso (spec do cap. 15: box = a janela no palco,
radius 16, sem sombra, sem "pop"). Cada batida da fala ("abriu a Área do Técnico", "viu como o segmento define as ferramentas", ...)
mostra o trecho do capítulo que ensinou aquilo, acelerado para caber na batida; as emendas são uma dissolvência curta.

Os trechos são achados pelos RÓTULOS dos passos do robô (rec/t18/capNN.json -> rec/t18/t18-capNN.actions.json); por isso a montagem
só roda depois das gravações dos capítulos 1 a 14 e ANTES da limpeza das gravações brutas. Sem cursor desenhado (o cursor é da edição).

uso: python3 -I t18/edit/montagem_cap15.py [--rec <pasta das gravações>] [--out <arquivo.mp4>] [--seco]
  --seco  só mostra a tabela de trechos (velocidades, tempos), sem chamar o ffmpeg
saída: t18/edit/out/montagem_cap15.mp4 (30 fps, H.264) e a linha do spec (at, dur) que o specs.json usa
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
REC = os.path.join(DOMI, "rec", "t18")
OUT = os.path.join(HERE, "out", "montagem_cap15.mp4")
FADE = 0.14        # dissolvência entre trechos (s)
FPS = 30
LARG, ALT = 1600, 1000      # 16:10, como a janela do app (2560x1600); o editor ajusta ao retângulo da janela em repouso
V_ALERTA = 8.0     # acima disso o trecho passa rápido demais para ler: avisa
V_MAX = 14.0

# (capítulo, rótulo inicial, folga antes (s), rótulo final, folga depois (s), início da batida, fim da batida)
# tempos da batida = segundos da fala do cap. 15 (as palavras vêm de `python3 -I rec/t18/palavras.py 15`)
BATIDAS = [
    # "a gente abriu a Área do Técnico,"
    (1, 'clica em "Área do Técnico™" no menu', -0.7, "o selo do segmento: Refrigeração e Climatização", 0.8, 2.1, 4.0),
    # "viu como o segmento define as ferramentas"
    (1, "clica no selo do segmento", -0.5, "as ferramentas com cadeado", 0.6, 4.0, 6.5),
    # "e como chegar nelas de dentro da ordem de serviço."
    (3, "clica no botão redondo", -0.6, "as mesmas ferramentas do Início", 0.8, 6.5, 9.5),
    # "Consultou o Catálogo,"
    (4, "aba Ar Condicionado", -0.4, "aba Fluidos Refrigerantes", 0.5, 9.5, 11.1),
    # "com os códigos de erro,"
    (4, "clica em Códigos de erro", -0.3, "o código E1", 0.6, 11.1, 12.4),
    # "os compressores,"
    (5, "aba Compressores", -0.3, "Ficha técnica do compressor de 18.000 BTUs", 1.2, 12.4, 13.5),
    # "os controles"
    (5, "aba Controles Remotos", -0.3, "desce até o Código universal", 0.6, 13.5, 14.3),
    # "e os gases."  (segue até a "contas")
    (5, "abre o R-32", -0.3, "Substitui", 0.6, 14.3, 17.1),
    # "carga térmica,"
    (6, "1 janela", -0.5, "o resultado: 16.800 BTUs", 0.6, 17.1, 18.3),
    # "conversão,"
    (7, "digita 10 bar", -0.4, "Inverter unidades", 0.2, 18.3, 19.1),
    # "capacitor,"
    (8, "tensão 220V", -0.3, 'Use o capacitor de 40 µF', 1.5, 19.1, 20.0),
    # "cabo e disjuntor,"
    (9, "distância 20 m", -0.3, "cabo 4 mm² e disjuntor de 16 A", 0.8, 20.0, 21.5),
    # "superaquecimento"
    (10, "temperatura da linha de sucção 12", -0.4, "selo Ideal", 0.6, 21.5, 22.7),
    # "e subresfriamento,"
    (10, "pressão de alta 350 psi", -0.3, "selo Ideal do subresfriamento", 0.6, 22.7, 24.0),
    # "régua de gases"
    (11, "digita 150 psi", -0.3, "os dois campos se ajustam", 0.6, 24.0, 25.2),
    # "e retrofit."
    (12, "Gás atual: R-22", -0.3, "o selo Mais indicado no R-438A (MO99)", 0.8, 25.2, 26.3),
    # "Fechou com o ciclo de refrigeração"
    (13, "link Ver o ciclo de refrigeração", -0.3, "o evaporador na ilustração", 0.5, 26.3, 28.4),
    # "e a diluição de produto."
    (14, "proporção 1 para 10", -0.3, "454,55 mL de água", 0.8, 28.4, 30.1),
    # "Lembra que os resultados são de apoio: vale sempre conferir a placa do equipamento e o manual do fabricante."
    (6, "a nota abaixo do resultado", -0.2, 'o rodapé "Ferramenta de apoio..."', 2.5, 30.1, 36.3),
]
# o tempo "folga antes" é somado ao início do passo (negativo = começa antes do passo); "folga depois" é somada ao fim do passo


def carrega(rec, cap):
    base = os.path.join(rec, f"t18-cap{cap:02d}")
    A = json.load(open(base + ".actions.json"))
    return base + ".mp4", [a for a in A["actions"] if a.get("ok", True)], float(A["video"]["durationS"])


def instantes(acts, rotulo, fim):
    """início (mín. dos passos com o rótulo) ou fim (máx.) de um rótulo; 'rótulo#2' = só a 2ª ocorrência (em ordem de tempo)"""
    k = None
    if "#" in rotulo:
        rotulo, k = rotulo.rsplit("#", 1)
        k = int(k)
    m = sorted((a for a in acts if a.get("label") == rotulo), key=lambda a: a["tStart"])
    if not m or (k and len(m) < k):
        raise SystemExit(f"rótulo {rotulo!r}{'#' + str(k) if k else ''} não existe nas ações (confira rec/t18/capNN.json)")
    if k:
        m = [m[k - 1]]
    return max(a["tEnd"] for a in m) if fim else min(a["tStart"] for a in m)


def planeja(rec):
    """lista de trechos: arquivo, início/fim no bruto, duração na tela (com a sobra da dissolvência), velocidade"""
    cache, seg = {}, []
    t0 = BATIDAS[0][5]
    for i, (cap, ri, fi, rf, ff, b0, b1) in enumerate(BATIDAS):
        if cap not in cache:
            cache[cap] = carrega(rec, cap)
        arq, acts, dur_v = cache[cap]
        a = max(0.0, instantes(acts, ri, False) + fi)
        b = min(dur_v, instantes(acts, rf, True) + ff)
        sobra = FADE if i < len(BATIDAS) - 1 else 0.0
        L = (b1 - b0) + sobra
        if b - a < L:      # o trecho bruto é mais curto que a batida: nunca em câmera lenta, estende o fim (ou segura o último quadro)
            b = min(dur_v, a + L)
        v = max(1.0, (b - a) / L)
        seg.append(dict(i=i, cap=cap, arq=arq, a=a, b=b, L=L, v=v, b0=b0 - t0, b1=b1 - t0, rotulos=(ri, rf)))
    return seg, t0, BATIDAS[-1][6] - t0


def monta(seg, saida):
    entradas, filtros = [], []
    for s in seg:
        # -ss/-t antes do -i: a busca é por quadro (com recodificação), sem decodificar o começo do arquivo
        entradas += ["-ss", f"{s['a']:.3f}", "-t", f"{s['b'] - s['a']:.3f}", "-i", s["arq"]]
        filtros.append(f"[{s['i']}:v]setpts=(PTS-STARTPTS)/{s['v']:.4f},fps={FPS},scale={LARG}:{ALT}:flags=lanczos,"
                       f"tpad=stop_mode=clone:stop_duration={max(0.0, s['L'] - (s['b'] - s['a']) / s['v']) + 0.2:.3f},"
                       f"trim=duration={s['L']:.4f},setpts=PTS-STARTPTS,format=yuv420p,settb=1/{FPS}[v{s['i']}]")
    cur = "v0"
    for s in seg[1:]:
        filtros.append(f"[{cur}][v{s['i']}]xfade=transition=fade:duration={FADE}:offset={s['b0']:.4f}[x{s['i']}]")
        cur = f"x{s['i']}"
    cmd = ["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", f"[{cur}]", "-an",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", saida]
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    r = subprocess.run(["nice", "-n", "10", *cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg falhou:\n" + r.stderr[-1500:])


def main():
    av = sys.argv[1:]
    rec, saida, seco = REC, OUT, "--seco" in av
    if "--rec" in av:
        rec = os.path.abspath(av[av.index("--rec") + 1])
    if "--out" in av:
        saida = os.path.abspath(av[av.index("--out") + 1])
    seg, t0, dur = planeja(rec)
    print(f"{'#':>2} cap  bruto (s)        tela (s)       veloc.  trecho")
    for s in seg:
        aviso = "  <- rápido demais" if s["v"] > V_ALERTA else ""
        print(f"{s['i']:>2} {s['cap']:>3}  {s['a']:6.1f}-{s['b']:6.1f}   {s['b0']:5.1f}-{s['b1']:5.1f}   {s['v']:5.1f}x  "
              f"{s['rotulos'][0]} -> {s['rotulos'][1]}{aviso}")
        if s["v"] > V_MAX:
            print("   (acima de %.0fx: reduza o trecho bruto ou junte batidas)" % V_MAX)
    if not seco:
        monta(seg, saida)
        print(f"montagem: {saida}")
    print(f"spec do cap. 15 -> ilustração: at {t0:.2f}, dur {dur:.2f} (box = a janela em repouso [166, 44, 1587, 992], radius 16)")


if __name__ == "__main__":
    main()
