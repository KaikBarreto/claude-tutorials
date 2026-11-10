#!/usr/bin/env bash
# gerar.py = _head.py + _caps.py + _tail.py (edite os três e rode este script)
cd "$(dirname "$0")" && cat _head.py _caps.py _tail.py > gerar.py && python3 -I -c "import ast,sys;ast.parse(open('gerar.py').read())" && echo "gerar.py montado"
