#!/usr/bin/env bash
# T17 · fase 2 (06/11): gerar.py = _head.py + _caps.py (edite os dois; este comando junta)
cd "$(dirname "$0")" && cat _head.py _caps.py > gerar.py
