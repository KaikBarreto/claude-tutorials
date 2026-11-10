#!/usr/bin/env python3
"""T7 · montagem rápida do cap. 13 (Recapitulando): trechos das gravações do celular, acelerados e emendados, no ritmo da fala.

O cap. 13 grava só a base (a OS #16 na tela, com o botão da Área do Técnico). Esta montagem vira uma ilustração em vídeo
(780x1688, a tela do celular) que o editor cola SOBRE a tela do aparelho em repouso (spec do cap. 13: box = a tela do celular
no palco, radius 46, sem sombra, sem "pop"). Cada batida da fala ("abriu a ordem pela agenda", "tocou em A Caminho", ...) mostra
o trecho do capítulo que ensinou aquilo, acelerado para caber na batida; as emendas são uma dissolvência curta.

Os trechos são achados pelos RÓTULOS dos passos do robô (rec/t7/capNN.json -> rec/t7/t7-capNN.actions.json); por isso a montagem
só roda depois das gravações dos capítulos 1 a 12 e ANTES da limpeza das gravações brutas.

uso: python3 -I t7/edit/montagem_cap13.py [--rec <pasta das gravações>] [--out <arquivo.mp4>] [--seco]
  --seco  só mostra a tabela de trechos (velocidades, tempos), sem chamar o ffmpeg
saída: t7/edit/out/montagem_cap13.mp4 (30 fps, H.264) e a linha do spec (at, dur) que o specs.py usa
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
REC = os.path.join(DOMI, "rec", "t7")
OUT = os.path.join(HERE, "out", "montagem_cap13.mp4")
FADE = 0.14        # dissolvência entre trechos (s)
FPS = 30
V_ALERTA = 8.0     # acima disso o trecho passa rápido demais para ler: avisa
V_MAX = 14.0

# (capítulo, rótulo inicial, folga antes (s), rótulo final, folga depois (s), início da batida, fim da batida)
# tempos da batida = segundos da fala do cap. 13 (as palavras vêm de `rec/t7/_ex/palavras.py 13`)
BATIDAS = [
    # "o técnico abriu a ordem pela agenda,"
    (1, "a OS número 16 na Agenda", 0.6, "Preencher OS", 1.6, 2.1, 4.5),
    # "tocou em A Caminho,"
    (2, "A Caminho", -0.8, "a posição do técnico", 0.8, 4.5, 6.2),
    # "acompanhou a rota"
    (2, "o cartão Rota até o cliente", -0.3, "o rótulo com minutos e quilômetros", 0.5, 6.2, 7.6),
    # "e fez o check-in quando chegou."
    (3, "Fazer Check-in", -0.5, "cabeçalho: o selo Em Andamento", 0.6, 7.6, 9.6),
    # "Depois preencheu o checklist do equipamento,"
    (4, "abre o acordeão do equipamento", -0.5, "o checklist do equipamento", 1.0, 9.6, 12.3),
    # "com respostas,"
    (4, "interruptor 3 -> Sim", -0.3, "interruptor 5 -> Sim", 0.3, 12.3, 13.1),
    # "medições,"
    (4, "corrente do compressor: 7,6", -1.0, "pressão de baixa: 118", 0.3, 13.1, 14.1),
    # "foto"
    (5, "escolhe a foto pela galeria", -0.3, "a miniatura na pergunta", 0.5, 14.0, 15.0),
    # "e a assinatura do cliente,"
    (9, "o campo da assinatura", -0.5, "o botão Confirmar", 0.3, 15.0, 16.3),
    # "anotou os materiais que usou"
    (6, "escolhe o Limpa-evaporador", -0.5, "Adicionar#1", 1.0, 16.3, 18.2),
    # "e viu como pausar"
    (7, "Pausar OS", -0.8, "cabeçalho: o selo Pausada", 0.8, 18.2, 19.6),
    # "e como finalizar parcialmente quando a visita não termina no dia."
    (8, "Finalizar Parcial", -0.5, "Finalizar Parcialmente", 2.5, 19.6, 23.5),
    # "Na finalização, conferiu o resumo do consumo, e o estoque baixou."
    (10, "Finalizar OS", -0.5, "Confirmar e finalizar", 2.5, 23.5, 28.0),
    # "A ordem virou um relatório,"
    (11, "o número da OS", -0.5, "a duração do atendimento", 0.5, 28.0, 30.2),
    # "que dá pra baixar em PDF"
    (11, "o rodapé: Baixar PDF", -0.3, "Baixar PDF", 1.5, 30.2, 31.4),
    # "ou mandar por link,"
    (12, "o menu de mais ações", -0.4, "Copiar Link", 0.8, 31.4, 32.6),
    # "e o cliente avaliou o atendimento."
    (12, "arrasta a nota até 10", -0.8, "Enviar avaliação", 3.0, 32.6, 35.0),
    # 1.38.21 (L4 nova, inserida na voz em 05/11): "E, quando a ordem muda no meio do atendimento,"
    (14, "o menu de mais ações", -0.8, "a gaveta Editar OS: Estrutura da OS", -0.3, 35.0, 38.0),
    # "ele ajusta os equipamentos e os checklists na gaveta Editar OS,"
    (14, "arrasta o checklist até o Hi-Wall", -0.3, "arrasta o checklist até o Hi-Wall", 0.5, 38.0, 42.4),
    # "e as respostas vão junto."
    (14, "Salvar equipamentos e checklists", -0.5, "o aviso: OS atualizada, respostas acompanharam", -1.5, 42.4, 44.3),
]
# o tempo "folga antes" é somado ao início do passo (negativo = começa antes do passo); "folga depois" é somada ao fim do passo


def carrega(rec, cap):
    base = os.path.join(rec, f"t7-cap{cap:02d}")
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
        raise SystemExit(f"rótulo {rotulo!r}{'#' + str(k) if k else ''} não existe nas ações (confira rec/t7/capNN.json)")
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
        filtros.append(f"[{s['i']}:v]setpts=(PTS-STARTPTS)/{s['v']:.4f},fps={FPS},scale=780:1688:flags=lanczos,"
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
    print(f"spec do cap. 13 -> ilustração: at {t0:.2f}, dur {dur:.2f} (box = a tela do celular em repouso, radius 46)")


if __name__ == "__main__":
    main()
