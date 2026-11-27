#!/usr/bin/env python3
"""Copia as aulas EcoFlix fechadas (1080p + legendas) para a pasta de entrega da sessão.

Uso: python3 -I publicar_entrega.py [T05 T15 ...]   (sem argumento: todas as que têm final)
Destino: $ECOFLIX_ENTREGA (padrão /mnt/attach/outputs/EcoFlix). Uma pasta por aula:
  "EcoFlix Tnn - <título>/EcoFlix Tnn - <título>.mp4" + .srt + .vtt
O título vem do nome da prévia em $TUT_HOME/entrega_previa. Pula o que já está lá com o mesmo tamanho.
"""
import os, re, shutil, sys, subprocess, time
from pathlib import Path

TUT = Path(os.environ.get("TUT_HOME", "/home/claude/ecoflix"))
DEST = Path(os.environ.get("ECOFLIX_ENTREGA", "/mnt/attach/outputs/EcoFlix"))


def titulos():
    t = {}
    for p in sorted((TUT / "entrega_previa").glob("EcoFlix T* - *(previa 720p).mp4")):
        m = re.match(r"EcoFlix (T\d\d) - (.+?)( 1\.\d+\.\d+)? \(previa 720p\)\.mp4$", p.name)
        if m:
            t[m.group(1)] = m.group(2).strip()
    return t


def legenda(out, ext):
    for c in (out / f"aula_final.{ext}", out / "legendas" / f"aula_final.{ext}"):
        if c.exists():
            return c
    return None


def duracao(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    try:
        s = float(r.stdout.strip())
        return f"{int(s // 60)}:{int(s % 60):02d}"
    except ValueError:
        return "?"


def mesma(src, dst):
    # a pasta de arquivos da sessão insere um bloco 'uuid' (~6 KB) no MP4: vídeo igual, tamanho um pouco maior
    if not dst.exists():
        return False
    d = dst.stat().st_size - src.stat().st_size
    return d == 0 or (src.suffix == ".mp4" and 0 < d <= 65536)


def copiar(src, dst):
    if mesma(src, dst):
        return False
    tmp = dst.with_name(dst.name + ".parcial")
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)
    return True


def main():
    pedidas = {a.upper() for a in sys.argv[1:]}
    tit = titulos()
    DEST.mkdir(parents=True, exist_ok=True)
    linhas = []
    for d in sorted(TUT.glob("t[0-9][0-9]")):
        aula = "T" + d.name[1:]
        out = d / "edit" / "out" / aula
        mp4 = out / "aula_final.mp4"
        if aula not in tit:
            continue
        nome = f"EcoFlix {aula} - {tit[aula]}"
        pasta = DEST / nome
        alvo = pasta / f"{nome}.mp4"
        vert = pasta / f"{nome} (vertical).mp4"
        if (not pedidas or aula in pedidas) and pasta.exists():
            # versão 9:16 opcional: out/TNN/entrega/*(vertical).mp4 (+ .srt/.vtt com o mesmo nome)
            for v in sorted((out / "entrega").glob("*(vertical).mp4")):
                feito = copiar(v, vert)
                for ext in ("srt", "vtt"):
                    lg = v.with_suffix("." + ext)
                    if lg.exists():
                        copiar(lg, pasta / f"{nome} (vertical).{ext}")
                print(("copiada " if feito else "já estava ") + nome + " (vertical)", flush=True)
        extra = "  + vertical 9:16" if vert.exists() else ""
        if not mp4.exists():
            # final local já liberado do disco: vale a cópia da entrega
            if alvo.exists():
                linhas.append(f"{nome}  ({duracao(alvo)}){extra}")
            continue
        if not pedidas or aula in pedidas:
            pasta.mkdir(exist_ok=True)
            feito = copiar(mp4, pasta / f"{nome}.mp4")
            for ext in ("srt", "vtt"):
                lg = legenda(out, ext)
                if lg:
                    copiar(lg, pasta / f"{nome}.{ext}")
            print(("copiada " if feito else "já estava ") + nome, flush=True)
            time.sleep(1)
        if mesma(mp4, alvo):
            linhas.append(f"{nome}  ({duracao(mp4)}){extra}")
    (DEST / "LEIA-ME.txt").write_text(
        "Aulas EcoFlix prontas para subir (1080p, com legendas .srt e .vtt).\n"
        "Cada pasta tem o vídeo e as legendas da aula.\n\n" + "\n".join(linhas) + "\n", encoding="utf-8")
    print(f"{len(linhas)} aula(s) no LEIA-ME", flush=True)


if __name__ == "__main__":
    main()
