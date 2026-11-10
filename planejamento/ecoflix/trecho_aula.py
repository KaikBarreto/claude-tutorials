#!/usr/bin/env python3
"""Mostra só um pedaço da fonte da Trilha EcoFlix, para o roteiro não precisar ler o arquivo inteiro (~60 mil tokens).

uso: python3 -I trecho_aula.py T7      a seção da aula T7
     python3 -I trecho_aula.py molde   as convenções e o molde de cada aula
     python3 -I trecho_aula.py fora    o que fica de fora, as pendências e o padrão de gravação
A fonte é a cópia de docs/ecoflix/trilha-de-tutoriais.md do repositório do EcoSistema; ECOFLIX_FONTE muda o caminho.
"""
import os
import re
import sys

FONTE = os.environ.get("ECOFLIX_FONTE", "/home/claude/ecoflix/fonte/trilha-de-tutoriais.md")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    alvo = sys.argv[1].strip()
    linhas = open(FONTE, encoding="utf8").read().split("\n")

    def bloco(i, para):
        j = i + 1
        while j < len(linhas) and not para(linhas[j]):
            j += 1
        return "\n".join(linhas[i:j]).rstrip()

    if re.fullmatch(r"[Tt]\d+", alvo):
        aula = alvo.upper()
        for i, linha in enumerate(linhas):
            m = re.match(r"^# 🎬 (T\d+)\b", linha)
            if m and m.group(1) == aula:
                print(bloco(i, lambda x: x.startswith("# ")))
                return
        sys.exit(f"aula {aula} não achada em {FONTE}")
    if alvo == "molde":
        i = next(i for i, linha in enumerate(linhas) if linha.startswith("## Convenções"))
        print(bloco(i, lambda x: x.startswith("## 🗺️") or x.startswith("# ")))
        return
    if alvo == "fora":
        i = next(i for i, linha in enumerate(linhas) if linha.startswith("# ❌"))
        print("\n".join(linhas[i:]).rstrip())
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
