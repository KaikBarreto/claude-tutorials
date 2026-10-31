"""Palco escuro do formato vertical 9:16 (1080x1920), a mesma arte do palco do 16:9.
O palco do 16:9 (fundo_escuro.py: folhas curvas quase pretas com a borda acesa no acento da marca, fio ciano, bloom,
vinheta e granulado) é gerado de novo e GIRADO 90° no sentido horário: 1920x1080 vira 1080x1920 sem reamostrar um
pixel. É o mesmo desenho (mesmas cores, mesma luz, mesmo granulado): as bordas acesas que no 16:9 cruzam as margens
da esquerda e da direita passam a cruzar as de cima e as de baixo, que são as que aparecem em volta do painel
vertical de 1008x1700 (margens de 110 px em cima e embaixo, 36 px nos lados). O 16:9 não é tocado: este módulo só LÊ
a saída do fundo_escuro.py, então qualquer ajuste futuro do palco vale também aqui.
uso: python3 fundo_escuro_vertical.py [saida.png]   (1080x1920; padrão assets/fundo_escuro_9x16.png)
Rode de novo depois de trocar a marca (marca/marca.json), como o fundo_escuro.py."""
import os
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "assets", "fundo_escuro_9x16.png")
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
horizontal = os.path.abspath(OUT) + ".16x9.tmp.png"
try:
    subprocess.run([sys.executable, os.path.join(HERE, "fundo_escuro.py"), horizontal], check=True, stdout=subprocess.DEVNULL)
    im = cv2.imread(horizontal, cv2.IMREAD_COLOR)
finally:
    if os.path.exists(horizontal):
        os.remove(horizontal)
assert im is not None and im.shape[:2] == (1080, 1920), "o palco do 16:9 deveria ter 1920x1080"
img = np.ascontiguousarray(np.rot90(im, k=-1))  # 90° horário
cv2.imwrite(OUT, img)
print(OUT, "média", img.mean().round(1), f"{img.shape[1]}x{img.shape[0]}")
