#!/usr/bin/env bash
# gerar.py = _head.py + _caps.py + _fim.py (edite os três; este comando junta)
cd "$(dirname "$0")" && cat _head.py _caps.py _fim.py > gerar.py
