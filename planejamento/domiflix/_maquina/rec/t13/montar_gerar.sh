#!/usr/bin/env bash
# junta as partes do gerar.py (base + capítulos); uso: rec/t13/montar_gerar.sh  (as partes são editadas à mão e este script as junta)
cd /home/claude/domiflix/rec/t13
python3 - <<'PY'
import glob, re
base = open('gerar_base2.txt', encoding='utf8').read()
partes = ''.join(open(f, encoding='utf8').read() for f in sorted(glob.glob('cap_parte*.txt')))
caps = sorted(int(m) for m in re.findall(r'^def cap(\d\d)\(', partes, re.M))
tail = "\n\nCAPS = {" + ", ".join(f"{n}: cap{n:02d}" for n in caps) + "}\n" + open('gerar_final.txt', encoding='utf8').read()
open('gerar.py', 'w', encoding='utf8').write(base + partes + tail)
print('gerar.py com os capítulos', caps)
PY
