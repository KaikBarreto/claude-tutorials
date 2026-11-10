#!/usr/bin/env bash
# junta as partes do gerar.py (cabeçalho + alvos + capítulos + final); uso: rec/t19/montar_gerar.sh  (as partes _head.py, _alvos.py, _caps*.py e _final.txt são editadas à mão)
cd /home/claude/domiflix/rec/t19
python3 - <<'PY'
import glob, re
head = open('_head.py', encoding='utf8').read()
alvos = open('_alvos.py', encoding='utf8').read()
caps = ''.join(open(f, encoding='utf8').read() for f in sorted(glob.glob('_caps*.py')))
nums = sorted(int(m) for m in re.findall(r'^def cap(\d\d)\(', caps, re.M))
tail = "\n\nCAPS = {" + ", ".join(f"{n}: cap{n:02d}" for n in nums) + "}\n\n" + open('_final.txt', encoding='utf8').read()
open('gerar.py', 'w', encoding='utf8').write(head + alvos + caps + tail)
print('gerar.py com os capítulos', nums)
PY
