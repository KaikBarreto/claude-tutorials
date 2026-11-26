"""T15 · papel real do PDF do Histórico (cap15, "O PDF é pra mandar pro contador ou guardar."): lê do actions.json da GRAVAÇÃO FINAL o passo `eval`
"PDF do histórico" ('PDF:<base64>' do blob que o app abre na aba nova), grava o PDF, rasteriza a primeira página a 350 dpi (pdftoppm) e gera o
bbox do pdftotext. Saída: t15/edit/out/comprovantes/cap15-historico.{pdf,png,bbox.html}.
Uso: python3 -I rec/t15/t15_papel.py [--ens]   (--ens lê o ensaio rápido em rec/t15/_ens, só para desenhar a cena antes da gravação final)"""
import base64, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
O = os.path.join(TUT, 't15', 'edit', 'out', 'comprovantes'); os.makedirs(O, exist_ok=True)
pasta = os.path.join(H, '_ens') if '--ens' in sys.argv else H
a = json.load(open(os.path.join(pasta, 't15-cap15.actions.json'), encoding='utf8'))
v = next((x.get('value') for x in a['actions'] if (x.get('label') or '').startswith('PDF do histórico')), None)
if not isinstance(v, str) or not v.startswith('PDF:'):
    sys.exit(f'SEM PDF no actions.json: {str(v)[:120]}')
nome = 'cap15-historico'
pdf = os.path.join(O, nome + '.pdf'); open(pdf, 'wb').write(base64.b64decode(v[4:]))
subprocess.run(['pdftoppm', '-r', '350', '-png', '-singlefile', '-f', '1', '-l', '1', pdf, os.path.join(O, nome)], check=True)
subprocess.run(['pdftotext', '-bbox', '-f', '1', '-l', '1', pdf, os.path.join(O, nome + '.bbox.html')], check=True)
print(subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout)
print(subprocess.run(['pdftotext', '-layout', '-f', '1', '-l', '1', pdf, '-'], capture_output=True, text=True).stdout[:3500])
