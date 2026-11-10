#!/usr/bin/env python3
"""T15 · montagem rápida do cap. 12 (Recapitulando): trechos das gravações dos capítulos, emendados no ritmo da fala (molde: T7, cap. 13).

A gravação ao vivo do cap. 12 só serve de base (ela mostra o Rafael com vale, bônus e falta em R$ 0,00, porque o pagamento já fechou o
ciclo, e ~1 s de tela branca ao abrir Contas): esta montagem vira uma ilustração em vídeo do tamanho da janela do app em repouso
(1586x992; spec do cap. 12: box [166, 44, 1587, 992], radius 16, sem sombra, sem "pop", `repouso` no capítulo inteiro) e cobre a base
do começo ao fim. Cada batida da fala mostra o trecho do capítulo que ensinou aquilo; a gravação não tem cursor (o editor o desenha
depois), então os trechos escolhidos são de tela que muda sozinha ou parada no resultado. Recorte leve por batida (zoom 1,2 a 1,4x)
para o texto ficar legível; o trecho do celular (9b) entra num aparelho genérico no meio da janela. Nunca em câmera lenta: trecho
bruto mais curto que a batida estende o fim (ou, com `segura`, repete o último quadro, para não entrar no passo seguinte).

Os trechos são achados pelos RÓTULOS dos passos do robô (rec/t15/capNN.json -> rec/t15/t15-capNN.actions.json); por isso a montagem
só roda depois das gravações finais e ANTES da limpeza das gravações brutas.

uso: python3 -I t15/edit/montagem_cap12.py [--seco] [--out <arquivo.mp4>]
  --seco  só mostra a tabela de trechos (velocidades, tempos), sem chamar o ffmpeg
saída: t15/edit/out/montagem_cap12.mp4 (1586x992, 30 fps, H.264)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
REC = os.path.join(DOMI, "rec", "t15")
OUT = os.path.join(HERE, "out", "montagem_cap12.mp4")
ASSETS = os.path.join(HERE, "out", "montagem_cap12_assets")
FADE = 0.14        # dissolvência entre trechos (s)
FPS = 30
OW, OH = 1586, 992  # a janela do app em repouso no palco (o overlay não reescala)
SW, SH = 2560, 1600
V_ALERTA = 4.0
FIM = 44.0          # fim do cap. 12 (narração 43,20 s + cauda 0,8 s)

# a 1ª batida começa 0,35 s antes do capítulo (spec: at -0,35): a ilustração já entra opaca no 1º quadro e a vinheta funde direto nela
# (cap, rótulo inicial, folga antes, rótulo final, folga depois, início da batida, fim da batida, zoom, centro do recorte, segura)
# o início = tStart do rótulo inicial + folga; o fim = tEnd do rótulo final + folga (s do vídeo bruto); batidas em s da fala do cap. 12
BATIDAS = [
    # L1 "Pronto! Recapitulando:" -> a ficha da Tatiane com os selos CLT e Controle de Ponto (fim do cap. 9; o aviso do link fica fora do recorte)
    ("09", "Salvar", 2.2, "Salvar", 3.4, -0.35, 2.00, 1.30, (1576, 750), False),
    # "a gente cadastrou a Tatiane com os dados,"
    ("02", "Nome Completo", -0.2, "Cargo", 0.0, 2.00, 4.60, 1.25, (1280, 780), False),
    # "o salário,"
    ("03", "Salário R$ 2.800,00", 0.5, "Salário R$ 2.800,00", 0.6, 4.60, 5.50, 1.35, (1280, 560), False),
    # "o custo mensal,"
    ("03", "Custo Total Mensal e Hora Homem", -0.5, "Custo Total Mensal e Hora Homem", 0.0, 5.50, 6.60, 1.25, (1280, 900), False),
    # "o regime CLT"
    ("03", "CLT", -0.1, "CLT", 1.0, 6.60, 7.80, 1.40, (1280, 680), False),
    # "e o dia do pagamento,"
    ("04", "Configuração de Pagamento", 0.9, "Configuração de Pagamento", 0.6, 7.80, 9.20, 1.30, (1280, 1000), False),
    # "e vinculou o login que ela já tinha."
    ("05", "abre a lista de usuários", -0.3, "escolhe Tatiane Ribeiro", 1.0, 9.20, 11.50, 1.25, (1280, 900), False),
    # L2 "No Rafael, lançou um vale, um bônus e uma falta," -> a ficha do Rafael com os três (fim do cap. 6)
    ("06", "Saldo atual", 0.05, "Vales, Bônus e Faltas", 0.8, 11.50, 15.60, 1.35, (1900, 850), False),
    # "pagou o salário com tudo descontado" -> a janela Pagamento com o resumo (cap. 7)
    ("07", "Valor a Pagar", -0.9, "Valor a Pagar", 0.0, 15.60, 17.90, 1.30, (1380, 720), False),
    # "e viu o extrato." (recorte na lista de movimentos: os cartões do topo já mostram o ciclo novo, zerado, depois do pagamento)
    ("07", "Extrato", 1.0, "Extrato", 1.9, 17.90, 19.30, 1.40, (1280, 1040), False),
    # L3 "Depois definiu as regras do ponto," -> Controle de Ponto > Config (cap. 8)
    ("08", "Jornada Padrão da Empresa", -0.2, "Jornada Padrão da Empresa", 1.0, 19.30, 21.30, 1.30, (1280, 760), False),
    # "ligou o ponto da Tatiane,"
    ("09", "Ativado", 0.3, "Ativado", 1.5, 21.30, 23.00, 1.25, (1280, 820), False),
    # "que bateu a entrada pelo celular," -> o celular do 9b
    ("09b", "Confirmar registro", -0.6, "Confirmar registro", 1.2, 23.00, 24.90, 1.00, None, False),
    # "e acompanhou tudo em Hoje,"
    ("10", "linha da Tatiane: entrada e Presente", 0.5, "linha da Tatiane: entrada e Presente", -1.3, 24.90, 26.60, 1.20, (1500, 1000), False),
    # "no Histórico"
    ("10", "Histórico", 2.25, "Histórico", 1.1, 26.60, 27.60, 1.20, (1280, 700), False),
    # "e no Relatório."
    ("10", "Relatório", 1.16, "Relatório", 1.6, 27.60, 28.80, 1.20, (1280, 800), False),
    # L4 "E viu a folha de cada um aparecer sozinha em Contas a Pagar." + L5 (próximo tutorial): as folhas em A Pagar (cap. 11), paradas
    # no resultado até o fim (o ⋮ da folha do Rafael abre em 20,2 s do bruto: o trecho para antes e o último quadro se repete)
    ("11", "folha de cada um", -0.3, "menu ⋮ da folha do Rafael", -1.0, 28.80, FIM, 1.25, (1450, 1100), True),
]


def carrega(cap):
    base = os.path.join(REC, f"t15-cap{cap}")
    A = json.load(open(base + ".actions.json"))
    v = A["video"]
    return base + ".mp4", [a for a in A["actions"] if a.get("ok", True)], float(v["durationS"]), (int(v["width"]), int(v["height"]))


def instante(acts, rotulo, fim):
    m = [a for a in acts if a.get("label") == rotulo]
    if not m:
        raise SystemExit(f"rótulo {rotulo!r} não existe nas ações (confira rec/t15/capNN.json)")
    return m[0]["tEnd"] if fim else m[0]["tStart"]


def recorte(z, centro):
    """retângulo (x, y, w, h) do bruto 2560x1600 com zoom z em volta do centro, dentro da tela, na proporção da janela"""
    w, h = round(SW / z / 2) * 2, round(SH / z / 2) * 2
    cx, cy = centro
    x = int(min(max(cx - w / 2, 0), SW - w)) // 2 * 2
    y = int(min(max(cy - h / 2, 0), SH - h)) // 2 * 2
    return x, y, w, h


def planeja():
    cache, seg = {}, []
    t0 = BATIDAS[0][5]
    for i, (cap, ri, fi, rf, ff, b0, b1, z, centro, segura) in enumerate(BATIDAS):
        if cap not in cache:
            cache[cap] = carrega(cap)
        arq, acts, dur_v, tam = cache[cap]
        a = max(0.0, instante(acts, ri, False) + fi)
        b = min(dur_v, instante(acts, rf, True) + ff)
        if b <= a:
            raise SystemExit(f"batida {i}: trecho vazio ({a:.2f} a {b:.2f} s no cap. {cap})")
        sobra = FADE if i < len(BATIDAS) - 1 else 0.0
        L = (b1 - b0) + sobra
        if b - a < L and not segura:   # nunca em câmera lenta: estende o fim
            b = min(dur_v, a + L)
        v = max(1.0, (b - a) / L)
        seg.append(dict(i=i, cap=cap, arq=arq, a=a, b=b, L=L, v=v, b0=b0 - t0, b1=b1 - t0, z=z, centro=centro, tam=tam,
                        segura=segura, rotulos=(ri, rf)))
    return seg, t0, BATIDAS[-1][6] - t0


def assets_celular():
    """fundo da janela com o aparelho genérico (corpo escuro + sombra) e a máscara arredondada da tela (PIL); devolve a posição da tela"""
    from PIL import Image, ImageDraw, ImageFilter
    os.makedirs(ASSETS, exist_ok=True)
    sh_, sw_ = 880, 406                     # tela do celular (780x1688 reduzido, mesma proporção)
    bez, r_t, r_c = 12, 40, 52               # moldura, raio da tela, raio do corpo
    cw, chh = sw_ + 2 * bez, sh_ + 2 * bez
    x0, y0 = (OW - cw) // 2, (OH - chh) // 2
    bg = Image.new("RGB", (OW, OH), (243, 244, 246))          # gelo da marca (#F3F4F6)
    sombra = Image.new("L", (OW, OH), 0)
    ImageDraw.Draw(sombra).rounded_rectangle([x0, y0 + 14, x0 + cw, y0 + chh + 14], r_c, fill=90)
    sombra = sombra.filter(ImageFilter.GaussianBlur(18))
    bg.paste((60, 64, 72), mask=sombra)
    ImageDraw.Draw(bg).rounded_rectangle([x0, y0, x0 + cw, y0 + chh], r_c, fill=(30, 30, 30))   # escuro da marca (#1E1E1E)
    bg.save(os.path.join(ASSETS, "fundo_celular.png"))
    m = Image.new("L", (sw_ * 2, sh_ * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, sw_ * 2 - 1, sh_ * 2 - 1], r_t * 2, fill=255)
    m.resize((sw_, sh_), Image.LANCZOS).save(os.path.join(ASSETS, "mascara_tela.png"))
    return x0 + bez, y0 + bez, sw_, sh_


def monta(seg, saida):
    entradas, filtros, nin = [], [], 0
    cel = None
    for s in seg:
        L_raw = s["b"] - s["a"]
        hold = max(0.0, s["L"] - L_raw / s["v"]) + 0.2
        entradas += ["-ss", f"{s['a']:.3f}", "-t", f"{L_raw:.3f}", "-i", s["arq"]]
        k_vid = nin; nin += 1
        base = f"[{k_vid}:v]setpts=(PTS-STARTPTS)/{s['v']:.4f},fps={FPS}"
        fim = f"tpad=stop_mode=clone:stop_duration={hold:.3f},trim=duration={s['L']:.4f},setpts=PTS-STARTPTS,format=yuv420p,settb=1/{FPS}[v{s['i']}]"
        if s["tam"][1] > s["tam"][0]:   # celular: tela arredondada dentro do aparelho genérico, no meio da janela
            if cel is None:
                cel = assets_celular()
            sx, sy, sw_, sh_ = cel
            entradas += ["-loop", "1", "-framerate", str(FPS), "-t", f"{s['L'] + 0.5:.3f}", "-i", os.path.join(ASSETS, "fundo_celular.png"),
                         "-loop", "1", "-framerate", str(FPS), "-t", f"{s['L'] + 0.5:.3f}", "-i", os.path.join(ASSETS, "mascara_tela.png")]
            k_bg, k_m = nin, nin + 1; nin += 2
            filtros.append(f"{base},scale={sw_}:{sh_}:flags=lanczos,format=rgba[ph{s['i']}]")
            filtros.append(f"[{k_m}:v]format=gray,fps={FPS}[mk{s['i']}]")
            filtros.append(f"[ph{s['i']}][mk{s['i']}]alphamerge[pa{s['i']}]")
            filtros.append(f"[{k_bg}:v]fps={FPS},format=rgba[bg{s['i']}]")
            filtros.append(f"[bg{s['i']}][pa{s['i']}]overlay={sx}:{sy}:shortest=1,{fim}")
        else:
            x, y, w, h = recorte(s["z"], s["centro"] or (SW / 2, SH / 2))
            filtros.append(f"{base},crop={w}:{h}:{x}:{y},scale={OW}:{OH}:flags=lanczos,{fim}")
    cur = "v0"
    for s in seg[1:]:
        filtros.append(f"[{cur}][v{s['i']}]xfade=transition=fade:duration={FADE}:offset={s['b0']:.4f}[x{s['i']}]")
        cur = f"x{s['i']}"
    cmd = ["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", f"[{cur}]", "-an",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart", saida]
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    r = subprocess.run(["nice", "-n", "10", *cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg falhou:\n" + r.stderr[-2500:])


def main():
    av = sys.argv[1:]
    saida, seco = OUT, "--seco" in av
    if "--out" in av:
        saida = os.path.abspath(av[av.index("--out") + 1])
    seg, t0, dur = planeja()
    print(f"{'#':>2} cap   bruto (s)        fala (s)       veloc. zoom  trecho")
    for s in seg:
        aviso = "  <- rápido demais" if s["v"] > V_ALERTA else ""
        hold = max(0.0, s["L"] - (s["b"] - s["a"]) / s["v"])
        print(f"{s['i']:>2} {s['cap']:>3}  {s['a']:6.2f}-{s['b']:6.2f}   {s['b0']:5.2f}-{s['b1']:5.2f}   {s['v']:4.2f}x {s['z']:.2f}  "
              f"{s['rotulos'][0]} -> {s['rotulos'][1]}{f'  (segura {hold:.1f} s)' if hold > 0.05 else ''}{aviso}")
    if not seco:
        monta(seg, saida)
        print(f"montagem: {saida}")
    print(f"spec do cap. 12 -> ilustração: at {t0:.2f}, dur {dur:.2f} (box = a janela em repouso [166, 44, 1587, 992], radius 16)")


if __name__ == "__main__":
    main()
