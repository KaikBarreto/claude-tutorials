"""T02 · tira do actions.json do cap12 a página do Relatório por Usuário (o passo `eval` "relatório HTML..." devolve 'HTML:<base64>',
a aba nova que o app abre no Visualizar / PDF) e gera o papel real da ilustração: out/comprovantes/cap12.html, cap12.pdf (impressão do
Chromium, A4 paisagem como o @page do app pede), cap12-N.png (pdftoppm -r 200) e cap12.bbox.html (pdftotext -bbox).
Uso: python3 -I relatorio_pdf.py [--ens]"""
import base64, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
rec = os.path.join(TUT, 'rec', 't02', '_ens' if '--ens' in sys.argv else '')
O = os.path.join(H, 'out', 'comprovantes'); os.makedirs(O, exist_ok=True)
a = json.load(open(os.path.join(rec, 't02-cap12.actions.json'), encoding='utf8'))
v = next((x.get('value') for x in a['actions'] if (x.get('label') or '').startswith('relatório HTML')), None)
if not isinstance(v, str) or not v.startswith('HTML:'):
    raise SystemExit(f'sem HTML no actions.json: {str(v)[:80]}')
html = os.path.join(O, 'cap12.html'); open(html, 'wb').write(base64.b64decode(v[5:]))
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[1]);await p.emulateMedia({media:'print'});
await p.pdf({path:process.argv[2],preferCSSPageSize:true,printBackground:true});await b.close()})()"""
subprocess.run(['node', '-e', js, '--', html, os.path.join(O, 'cap12.pdf')], check=True, cwd=os.path.join(TUT, 'rec'))
for f in os.listdir(O):
    if f.startswith('cap12-') and f.endswith('.png'): os.remove(os.path.join(O, f))
subprocess.run(['pdftoppm', '-r', '200', '-png', os.path.join(O, 'cap12.pdf'), os.path.join(O, 'cap12')], check=True)
subprocess.run(['pdftotext', '-bbox', os.path.join(O, 'cap12.pdf'), os.path.join(O, 'cap12.bbox.html')], check=True)
print(sorted(f for f in os.listdir(O) if f.startswith('cap12')))
print(subprocess.run(['pdftotext', '-layout', os.path.join(O, 'cap12.pdf'), '-'], capture_output=True, text=True).stdout[:2500])
