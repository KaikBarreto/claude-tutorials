"""Emenda as frases novas (um MP3 com as frases de trocas.json separadas por [pause]) no áudio de cada capítulo,
no lugar da frase antiga, SEM mudar a duração do capítulo (a gravação de tela segue sincronizada):
frase nova começa onde a antiga começava; o resto da janela antiga vira silêncio. Troca sem frase nova = só silêncio.
Saída: emendas/capNN_v2.wav (48 kHz mono) para cada capítulo afetado; depois rode
  python3 -I proc.py NN=emendas/capNN_v2.wav ...   (refaz palavras/legendas desses capítulos)
uso: python3 -I emendar.py <frases_novas.mp3> [--insercoes <insercoes.mp3>]
     (sem trocas na lista: só `--insercoes <mp3>`; sem inserções: só o MP3 das frases novas)

Regras (31/10/2026, depois do T1/T4/T7):
  * o início da janela nunca fica abaixo de 0 (troca em 0 s) nem invade a palavra anterior;
  * frase nova mais longa que a janela: o tempo é comprimido com ffmpeg `atempo` (mantém o tom), no máximo ~8%, para a
    fala terminar >= 0,2 s antes da próxima palavra do capítulo (pelas `words` do capNN.json) ou do fim do capítulo;
    se ainda assim não couber, o script AVISA e nunca deixa a frase passar por cima da fala seguinte (corta o fim com
    fade e diz quanto cortou: gere a frase de novo, mais curta). Aula ainda não gravada: EMENDA_COMPRIME_MAX=0 (sem
    compressão) com `empurra` em todas as trocas;
  * `"empurra": true` numa troca (opção, 1/11/2026, T3 v2): se a frase não couber nem comprimida, em vez de cortar o fim o script abre
    silêncio logo depois da janela e o resto do capítulo anda para a frente (a duração CRESCE, como numa inserção; as trocas seguintes do
    capítulo e as inserções com `em` numérico acompanham o deslocamento). Use quando a frase nova é boa e só a janela é curta;
  * imprime a folga final de cada troca (próxima palavra - fim da fala nova) e um resumo no fim;
  * lê o take ORIGINAL do capítulo: se o capNN.json atual já é uma emenda (take dentro de emendas/), usa o
    capNN.v1.json (cópia guardada) em vez de emendar duas vezes; sem o v1, para com a explicação;
  * apaga o `words.json` do take antigo de emendas/capNN_v2 para o proc.py não reaproveitar o ASR da emenda anterior.

Inserções (1/11/2026, T3 v2): a chave `insercoes` do trocas.json acrescenta frases que NÃO existiam, o que MUDA a duração do
capítulo (as trocas não mudam). Cada item: {"cap": 10, "em": 6.52 | "fim", "folga": 0.12, "novo": "frase"}; `em` = instante do corte
no take ORIGINAL (num silêncio; o script avisa se cair em cima de fala) e `folga` = silêncio extra de cada lado da frase
(o resto do áudio é empurrado para a frente). As frases vêm de outro MP3 (`--insercoes`), recortadas do mesmo jeito das trocas
(alinhamento por palavra, bordas pelo VAD, volume casado por LUFS). Capítulo que também tem trocas parte da saída delas e grava
emendas/capNN_v3.wav (o _v2 fica só com as trocas); capítulo só com inserções grava emendas/capNN_v2.wav. Depois do
proc.py desses arquivos, as `words` já estão no relógio novo: a gravação de tela usa a duração nova."""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import proc  # noqa: E402

SR = 48000
MARGEM = 0.20      # folga desejada entre o fim da fala nova e a próxima palavra (s)
MARGEM_MIN = 0.03  # abaixo disso a frase encostaria na fala seguinte: corta o fim em vez de invadir
# compressão máxima de tempo (8%). Aula AINDA NÃO GRAVADA (T11, 05/11/2026): a tela vai ser gravada em cima do áudio novo, então não
# há sincronismo a manter; com EMENDA_COMPRIME_MAX=0 e "empurra": true nas trocas, a frase nova fica na velocidade natural e o
# capítulo cresce o necessário.
COMPRIME_MAX = float(os.environ.get("EMENDA_COMPRIME_MAX", "0.08"))
RECUO_INI = 0.03   # a janela antiga começa 30 ms antes da primeira palavra
AVANCO_FIM = 0.05  # e termina 50 ms depois da última


def carregar_cap(cap):
    """capNN.json do take ORIGINAL (se o atual já é uma emenda, usa o capNN.v1.json guardado)."""
    p = os.path.join(HERE, f"cap{cap:02d}.json")
    c = json.load(open(p))
    if os.path.basename(os.path.dirname(c.get("arquivo", ""))) == "emendas":
        v1 = os.path.join(HERE, f"cap{cap:02d}.v1.json")
        if not os.path.exists(v1):
            sys.exit(f"cap{cap:02d}.json já é uma emenda (take {c['take']}) e não há cap{cap:02d}.v1.json: restaure o take original")
        print(f"cap{cap:02d}: cap{cap:02d}.json já é uma emenda; usando cap{cap:02d}.v1.json (take original)")
        c = json.load(open(v1))
    return c


def lufs(y):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(y.astype(np.float64)) if len(y) > SR * 0.4 else -70


def fade(y, ms=8):
    n = min(int(SR * ms / 1000), len(y) // 2)
    if n > 0:
        y[:n] *= np.linspace(0, 1, n)
        y[-n:] *= np.linspace(1, 0, n)
    return y


def atempo(clip, r):
    """acelera o trecho em `r` (> 1) sem mexer no tom (ffmpeg atempo). Devolve (trecho, razão real de duração)."""
    d = tempfile.mkdtemp(prefix="emendar_")
    a, b = os.path.join(d, "in.wav"), os.path.join(d, "out.wav")
    try:
        sf.write(a, clip, SR, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-filter:a", f"atempo={r:.6f}", "-ar", str(SR), "-ac", "1",
                        "-c:a", "pcm_f32le", b], check=True)
        out, sr = sf.read(b, dtype="float32")
        assert sr == SR
    finally:
        for f in (a, b):
            if os.path.exists(f):
                os.remove(f)
        os.rmdir(d)
    return out, len(clip) / len(out)


def proxima_palavra(c, cap, i, T):
    """início (s) da próxima fala depois da troca i: a próxima palavra do capítulo que não é de outra janela trocada, o
    início da frase nova de outra troca logo adiante, ou o fim do capítulo."""
    mine = T[i]
    outras = [t for j, t in enumerate(T) if t["cap"] == cap and j != i]
    cand = [c["dur"]]
    for w in c["words"]:
        if w["s"] is None or w["s"] < mine["ate"] - 0.02:
            continue
        if any(o["de"] - 0.02 <= w["s"] <= o["ate"] + 0.02 for o in outras):
            continue
        cand.append(w["s"])
        break
    cand += [max(0.0, o["de"] - RECUO_INI) for o in outras if o["novo"] and o["de"] >= mine["ate"] - 0.02]
    return min(cand)


def palavra_anterior_fim(c, de):
    """fim (s) da última palavra que termina antes da janela (0 se não há)."""
    fins = [w["e"] for w in c["words"] if w["e"] is not None and w["s"] is not None and w["s"] < de - 0.01 and w["e"] <= de + 0.02]
    return max(fins) if fins else 0.0


def recortar(src, frases, rotulo="frase"):
    """Transcreve o MP3 `src` (as `frases`, uma por linha, nesta ordem) e devolve {frase: (trecho, instante da última palavra
    dentro do trecho, em s)}: alinhamento palavra a palavra com o texto pedido e bordas encostadas no silêncio (VAD)."""
    tid, d, words = proc.transcrever(src)
    toks = proc.tokens("\n".join(frases))
    vad = json.load(open(os.path.join(d, "vad.json")))
    ws = proc.alinhar(toks, words, vad)
    x, sr = sf.read(os.path.join(d, "audio48k.wav"), dtype="float32")
    assert sr == SR

    def borda(t, lado):
        """encosta o corte no silêncio mais próximo (VAD) para não cortar sílaba"""
        for v0, v1 in vad:
            if v0 - 0.02 <= t <= v1 + 0.02:
                return v0 - 0.04 if lado == "ini" else v1 + 0.06
        return t

    clips = {}
    for li, frase in enumerate(frases):
        fw = [w for w in ws if w["linha"] == li]
        a, b = max(0.0, borda(fw[0]["s"], "ini")), borda(fw[-1]["e"], "fim")
        fim_vad = next((v1 for v0, v1 in vad if v0 - 0.02 <= fw[-1]["e"] <= v1 + 0.02), 0.0)  # o mais tardio dos dois: conservador
        clips[frase] = (x[int(a * SR):int(b * SR)].copy(), max(fw[-1]["e"], fim_vad) - a)
        ok = min(w["ok"] for w in fw)
        print(f"{rotulo} {li + 1}: {a:6.2f}-{b:6.2f} ({b - a:.2f}s) menor semelhança {ok:.2f}: {frase}")
    return clips


def inserir(y, pontos):
    """Cola frases novas num áudio, empurrando o resto para a frente (a duração aumenta).
    pontos: [(segundo do corte no take de partida, trecho, folga)] em ordem crescente; cada trecho entra com `folga` s de
    silêncio de cada lado."""
    partes, ult = [], 0
    for t, clip, folga in pontos:
        i = min(len(y), max(ult, int(round(t * SR))))
        gap = np.zeros(int(round(folga * SR)), dtype=y.dtype)
        partes += [y[ult:i], gap, clip, gap]
        ult = i
    partes.append(y[ult:])
    return np.concatenate(partes)


def main():
    cfg = json.load(open(os.path.join(HERE, "trocas.json")))
    T, INS = cfg.get("trocas", []), cfg.get("insercoes", [])
    args = sys.argv[1:]
    ins_mp3 = None
    if "--insercoes" in args:
        k = args.index("--insercoes")
        ins_mp3 = args[k + 1]
        del args[k:k + 2]
    src = args[0] if args else None
    novas = [t["novo"] for t in T if t["novo"]]
    if (novas and not src) or (INS and not ins_mp3):
        sys.exit("uso: python3 -I emendar.py <frases_novas.mp3> [--insercoes <insercoes.mp3>]")

    # 1) transcreve o MP3 das frases novas e acha cada frase (alinhamento palavra a palavra com o texto pedido)
    clips = recortar(src, novas, "frase") if novas else {}  # frase -> (trecho, instante da última palavra no trecho, em s)
    clips_ins = recortar(ins_mp3, [i["novo"] for i in INS], "inserção") if INS else {}

    os.makedirs(os.path.join(HERE, "emendas"), exist_ok=True)
    resumo = []
    emendado = {}  # cap -> áudio depois das trocas
    empurrado = {}  # cap -> [(instante original, segundos de silêncio aberto ali)] das trocas com `empurra`
    for cap in sorted({t["cap"] for t in T}):
        c = carregar_cap(cap)
        y, sr2 = sf.read(os.path.join(c["pasta"], "audio48k.wav"), dtype="float32")
        assert sr2 == SR
        if y.ndim == 2:
            y = y.mean(1)
        y = y.copy()
        alvo = lufs(y)
        fim_cap0 = len(y) / SR  # duração do take original (relógio original; `y` cresce se uma troca usar `empurra`)
        empurroes = []          # (instante no relógio ORIGINAL, segundos de silêncio aberto ali): o que vem depois andou
        for i, t in enumerate(T):
            if t["cap"] != cap:
                continue
            off = sum(e for p, e in empurroes if p <= t["de"] + 1e-6)  # quanto o capítulo já andou até esta troca
            prox = min(proxima_palavra(c, cap, i, T), fim_cap0) + off
            ant = palavra_anterior_fim(c, t["de"])
            ant = ant + off if ant else 0.0
            ini = max(0.0, t["de"] - RECUO_INI) + off                # (a) nunca abaixo de 0
            if ant and ini < ant + 0.005 and ant < t["de"] + off:   # nem em cima da palavra anterior
                ini = ant + 0.005
            fim = min(len(y) / SR, t["ate"] + AVANCO_FIM + off, max(ini, prox - 0.005))
            a, b = int(round(ini * SR)), int(round(fim * SR))
            y[a:b] = 0.0
            nome = f"cap{cap:02d} {t['de']:.2f}-{t['ate']:.2f}"
            if not t["novo"]:
                print(f"{nome} -> (silêncio)")
                resumo.append((nome, "silêncio", None, None, "ok"))
                continue
            cl, fim_fala = clips[t["novo"]]
            cl = cl.copy()
            # (b) a fala nova precisa terminar >= MARGEM antes da próxima fala: comprime o tempo, no máximo 8%
            r = 1.0
            disponivel = prox - MARGEM - ini
            if fim_fala > disponivel and COMPRIME_MAX > 0:
                alvo_r = fim_fala / max(disponivel, 1e-3) * 1.002   # razão de duração que dá a folga pedida (com 0,2% de sobra)
                r_nom = min(1.0 + COMPRIME_MAX, alvo_r)
                for _ in range(3):  # a razão real do atempo difere um pouco da pedida: confere e corrige
                    cl2, real = atempo(cl, r_nom)
                    if ini + fim_fala / real <= prox - MARGEM or r_nom >= 1.0 + COMPRIME_MAX - 1e-6:
                        break
                    r_nom = min(1.0 + COMPRIME_MAX, r_nom * alvo_r / real)
                cl, r = cl2, real
                fim_fala /= real
            g = 10 ** ((alvo - lufs(cl)) / 20) if lufs(cl) > -60 else 1.0
            cl = fade(cl * min(g, 2.0))
            aviso = ""
            fim_nova = ini + fim_fala
            if t.get("empurra") and fim_nova > prox - MARGEM + 0.005:
                # `empurra`: a frase não cabe nem comprimida. Em vez de cortar o fim, abre silêncio logo depois da janela e o resto do
                # capítulo anda para a frente (a duração do capítulo CRESCE; a gravação de tela usa a duração nova)
                extra = round(fim_nova - (prox - MARGEM) + 0.005, 3)
                pos = int(round(fim * SR))
                y = np.concatenate([y[:pos], np.zeros(int(round(extra * SR)), dtype=y.dtype), y[pos:]])
                empurroes.append((fim - off, extra))
                prox += extra
                aviso = f"EMPURRADA: +{extra:.2f} s de silêncio depois da frase; o resto do capítulo andou {extra:.2f} s (o capítulo ficou mais longo)"
            folga = prox - fim_nova
            lim = int(round((prox - MARGEM_MIN) * SR)) - a           # nunca invade a fala seguinte
            if len(cl) > lim:
                cl = fade(cl[:max(lim, 0)].copy(), 15)
                perda = fim_nova - (prox - MARGEM_MIN)
                if perda > 0.005:  # só o silêncio do rabo do trecho não é perda
                    aviso = (f"CORTADA: perdeu {perda:.2f} s do fim da fala (não coube nem comprimida {COMPRIME_MAX * 100:.0f}%); "
                             f"gere a frase de novo, mais curta")
            if not aviso and folga < MARGEM - 0.005:
                aviso = f"ATENÇÃO: folga {folga:.2f} s < {MARGEM:.1f} s mesmo com compressão de {(r - 1) * 100:.1f}%"
            empurrada = aviso.startswith("EMPURRADA")
            n = min(len(cl), len(y) - a)
            y[a:a + n] += cl[:n]
            comp = f", tempo x{r:.3f} (+{(r - 1) * 100:.1f}%)" if r > 1.0 else ""
            print(f"{nome} -> {t['novo']}")
            print(f"    fala nova termina em {fim_nova:.2f} s; próxima fala em {prox:.2f} s -> folga final {folga:.2f} s{comp}")
            if aviso:
                print(f"    {aviso}")
            resumo.append((nome, "frase nova", r, folga, "ok" if not aviso else "empurrada" if empurrada else aviso.split(":")[0]))
        empurrado[cap] = empurroes
        out = os.path.join(HERE, "emendas", f"cap{cap:02d}_v2.wav")
        sf.write(out, y, SR, subtype="PCM_24")
        emendado[cap] = y
        velho = os.path.join(HERE, "takes", f"cap{cap:02d}_v2", "words.json")
        if os.path.exists(velho):  # o proc.py só roda o ASR se não há words.json: não deixa valer o da emenda anterior
            os.remove(velho)
        print("  ->", out, f"{len(y) / SR:.2f}s, LUFS {lufs(y):.2f} (antes {alvo:.2f})")

    # 2) inserções: frases que não existiam; a duração do capítulo AUMENTA (o resto do áudio é empurrado para a frente)
    for cap in sorted({i["cap"] for i in INS}):
        c = carregar_cap(cap)  # take original: dá o VAD para conferir que o corte cai num silêncio
        if cap in emendado:
            y, sufixo = emendado[cap], "v3"  # parte da saída das trocas; o _v2 continua só com elas
        else:
            y, _ = sf.read(os.path.join(c["pasta"], "audio48k.wav"), dtype="float32")
            y = (y.mean(1) if y.ndim == 2 else y).copy()
            sufixo = "v2"
        alvo = lufs(y)
        fim_cap = len(y) / SR
        pontos = []
        for it in sorted((i for i in INS if i["cap"] == cap), key=lambda i: fim_cap if i["em"] == "fim" else float(i["em"])):
            t_vad = c["dur"] if it["em"] == "fim" else float(it["em"])  # relógio do take original (o VAD é dele)
            t = fim_cap if it["em"] == "fim" else t_vad + sum(e for p, e in empurrado.get(cap, []) if p <= t_vad + 1e-6)
            folga = float(it.get("folga", 0.12))
            cl, fim_fala = clips_ins[it["novo"]]
            g = 10 ** ((alvo - lufs(cl)) / 20) if lufs(cl) > -60 else 1.0
            cl = fade(cl * min(g, 2.0))
            fala = [v for v in c["vad"] if v[0] < t_vad < v[1]]
            antes = max([v[1] for v in c["vad"] if v[1] <= t_vad] or [0.0])
            depois = min([v[0] for v in c["vad"] if v[0] >= t_vad] or [c["dur"]])
            aviso = "  ATENÇÃO: o corte cai em cima de fala; escolha um instante num silêncio" if fala and it["em"] != "fim" else ""
            print(f"cap{cap:02d} inserção em {t:.2f} s (silêncio de {antes:.2f} a {depois:.2f} s) + {len(cl) / SR:.2f} s de frase, "
                  f"folga {folga:.2f} s de cada lado -> {it['novo']}{aviso}")
            pontos.append((t, cl, folga))
            resumo.append((f"cap{cap:02d} inserção {t:.2f}", "inserida", None, None, "ok" if not aviso else "ATENÇÃO"))
        y2 = inserir(y, pontos)
        out = os.path.join(HERE, "emendas", f"cap{cap:02d}_{sufixo}.wav")
        sf.write(out, y2, SR, subtype="PCM_24")
        velho = os.path.join(HERE, "takes", f"cap{cap:02d}_{sufixo}", "words.json")
        if os.path.exists(velho):
            os.remove(velho)
        print("  ->", out, f"{len(y2) / SR:.2f}s (era {len(y) / SR:.2f}s, +{(len(y2) - len(y)) / SR:.2f}s), LUFS {lufs(y2):.2f} (antes {alvo:.2f})")

    print("\nresumo das folgas (fala nova -> próxima fala):")
    for nome, tipo, r, folga, st in resumo:
        if folga is None:
            print(f"  {nome:<22} {tipo}" + (f"  {st}" if tipo == "inserida" else ""))
        else:
            print(f"  {nome:<22} folga {folga:5.2f} s  tempo x{r:.3f}  {st}")


if __name__ == "__main__":
    main()
