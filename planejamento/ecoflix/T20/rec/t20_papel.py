"""T20 · papel real do relatório do portal (cap09, Baixar PDF: HTML escrito na aba nova): lê do actions.json da GRAVAÇÃO FINAL o passo
`eval` "PDF DO ..." ('HTML:<base64>' da aba nova que o app abre), imprime no Chromium (mídia de impressão, @page do app), rasteriza com
pdftoppm (300 dpi, uma PNG por página) e gera o bbox do pdftotext. Saída: t20/edit/out/comprovantes/cap09-relatorio.*
Uso: python3 -I rec/t20/t20_papel.py [09] [--ens]"""
import base64, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); TUT = os.path.dirname(os.path.dirname(H))
O = os.path.join(TUT, 't20', 'edit', 'out', 'comprovantes'); os.makedirs(O, exist_ok=True)
ALVO = {'09': ('PDF DO RELATÓRIO', 'cap09-relatorio')}
JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[1]);await p.emulateMedia({media:'print'});
await p.pdf({path:process.argv[2],preferCSSPageSize:true,printBackground:true});await b.close()})()"""
PASTA = os.path.join(H, '_ens') if '--ens' in sys.argv else H
for cap in ([a for a in sys.argv[1:] if a != '--ens'] or ALVO):
    rot, nome = ALVO[cap]
    a = json.load(open(os.path.join(PASTA, f't20-cap{cap}.actions.json'), encoding='utf8'))
    v = next((x.get('value') for x in a['actions'] if (x.get('label') or '').startswith(rot)), None)
    if not isinstance(v, str) or not v.startswith('HTML:'):
        print(f'cap{cap}: SEM HTML no actions.json: {str(v)[:120]}'); continue
    html = os.path.join(O, nome + '.html'); open(html, 'wb').write(base64.b64decode(v[5:]))
    pdf = os.path.join(O, nome + '.pdf')
    subprocess.run(['node', '-e', JS, '--', html, pdf], check=True, cwd=os.path.join(TUT, 'rec'))
    for f in os.listdir(O):
        if f.startswith(nome) and f.endswith('.png'): os.remove(os.path.join(O, f))
    subprocess.run(['pdftoppm', '-r', '300', '-png', pdf, os.path.join(O, nome)], check=True)
    subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', '-f', '1', '-l', '1', pdf, os.path.join(O, nome)], check=True)   # nome.png = página 1
    subprocess.run(['pdftotext', '-bbox', pdf, os.path.join(O, nome + '.bbox.html')], check=True)
    print(cap, sorted(f for f in os.listdir(O) if f.startswith(nome)))
    print(subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout[:1800])
