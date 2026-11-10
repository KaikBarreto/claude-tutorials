#!/usr/bin/env bash
# gerar.py = _head.py + _caps.py + _fim.py (edite os três; este comando junta). Troca atômica (mv): um rodar.sh em curso nunca lê o arquivo pela metade.
cd "$(dirname "$0")" && cat _head.py _caps.py _fim.py > gerar.py.novo && mv gerar.py.novo gerar.py
