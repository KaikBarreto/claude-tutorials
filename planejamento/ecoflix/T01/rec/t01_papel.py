#!/usr/bin/env python3
"""T01 · papel REAL do comprovante para as ilustrações (cap00, cap05, cap08, cap10). Gera rec/t01/papel.json (robô sem voz, só para
capturar PDFs: o app abre o comprovante em janela nova e o gancho guarda o PDF que ele gerou) e, depois da captura, grava os PDFs e os
PNGs em rec/t01/papel/. Uso:
  python3 -I rec/t01/t01_papel.py gerar      -> rec/t01/papel.json
  (gravar: node rec/record.mjs rec/t01/papel.json --rapido --out /dev/shm/t01_papel, pela fila, instância 54311 com a semente t01/papel)
  python3 -I rec/t01/t01_papel.py extrair    -> rec/t01/papel/NOME.pdf e NOME.png (300 dpi) + texto
Capturas: A (pedido #1758, estado depois do cap08), T_off/T_on (pedido #1757 com 5 kg de tara; peso líquido desligado e ligado),
S_ambas/S_cli (assinaturas: operador e cliente; só o cliente), E_nome (Nome em destaque)."""
import base64, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(H, 'cap10.json'), encoding='utf8'))
GANCHO = next(s['js'] for s in json.load(open(os.path.join(H, '..', 't27', 'cap05.json'), encoding='utf8'))['setup'] if s.get('js', '').startswith('(()=>{if(window.__pdfs)'))
CAPTURA = ("(async()=>{const n0=window.__n0||0;let n=-1,parado=0;for(let i=0;i<60;i++){const k=(window.__pdfs||[]).length;if(k>n0&&k===n){if(++parado>=3)break}else parado=0;n=k;"
           "await new Promise(r=>setTimeout(r,250))}const b=window.__pdfs&&window.__pdfs.length>n0&&window.__pdfs[window.__pdfs.length-1];if(!b)return 'SEM PDF';"
           "const u=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));"
           "return {nome:'%s',pdfs:window.__pdfs.length,bytes:u.length,b64:btoa(s)}})()")
FECHA = "(()=>{const j=window.__janelas||[];for(const w of j){try{if(!w.closed)w.close()}catch(e){}}return 'ok'})()"
SW = ("(()=>{const el=[...document.querySelectorAll('main label')].find(e=>e.textContent.trim()==='%s');if(!el)return 'SEM ALVO';let c=el;"
      "while(c&&c!==document.body){const b=c.querySelector('button[role=switch]');if(b){b.scrollIntoView({block:'center'});b.click();return 'clicou: '+b.getAttribute('aria-checked')}c=c.parentElement}return 'SEM SWITCH'})()")
def st(**k): return k
def ir(url, esp, alvo=None):
    return [st(do='goto', url=url), st(do='waitFor', text=esp, timeout=30), st(do='waitFor', idle=True)]
def pedido(nome, linha):
    sel = f'main tbody tr:nth-child({linha}) button[aria-haspopup=menu]'
    return (ir('/pedidos', 'Pedidos') + [st(do='waitFor', target={'selector': sel}, timeout=20), st(do='eval', js=GANCHO),
            st(do='eval', js='window.__n0=window.__pdfs.length'),
            st(do='hover', target={'selector': sel}), st(do='pause', seconds=0.6),
            st(do='click', target={'role': 'menuitem', 'name': 'Ver comprovante'}),
            st(do='eval', js=CAPTURA % nome, label='captura ' + nome), st(do='eval', js=FECHA)])
def config():
    return ir('/configuracoes', 'Configurações do Sistema') + [st(do='click', target={'selector': '#tab-btn-usability'}), st(do='waitFor', idle=True), st(do='pause', seconds=0.8)]
def chave(rot, label): return [st(do='eval', js=SW % rot, label=label), st(do='pause', seconds=1.5)]
steps = []
steps += pedido('A', 1)
steps += pedido('T_off', 2)
steps += config() + chave('Mostrar só peso líquido', 'liga peso líquido') + pedido('T_on', 2)
steps += config() + chave('Mostrar só peso líquido', 'desliga peso líquido')
steps += config() + chave('Assinaturas no comprovante', 'liga assinaturas') + pedido('S_ambas', 1)
steps += config() + [st(do='click', target={'selector': '#receipt-signature-mode'}), st(do='click', target={'role': 'option', 'name': 'Só o cliente/fornecedor'}), st(do='pause', seconds=1.5)] + pedido('S_cli', 1)
steps += config() + chave('Assinaturas no comprovante', 'desliga assinaturas') + [st(do='click', target={'text': 'Nome em destaque', 'exact': True}), st(do='pause', seconds=1.5)] + pedido('E_nome', 1)
steps.append(st(do='eval', js='JSON.stringify(window.__avisos||"sem observador")'))
setup = base['setup'][:7] + [st(do='eval', js=GANCHO)]
rob = {k: v for k, v in base.items() if k not in ('steps', 'setup')}
rob.update(name='t01-papel', title='T01 · captura do papel real do comprovante (sem voz)', seed='t01-papel', seedExtra=base['seedExtra'] + ['t01/papel'],
           setup=setup, steps=steps)
O = os.path.join(H, 'papel')
if sys.argv[1:2] == ['gerar']:
    json.dump(rob, open(os.path.join(H, 'papel.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(len(steps), 'passos -> rec/t01/papel.json')
elif sys.argv[1:2] == ['extrair']:
    os.makedirs(O, exist_ok=True)
    a = json.load(open(sys.argv[2] if len(sys.argv) > 2 else '/dev/shm/t01_papel/t01-papel.actions.json', encoding='utf8'))['actions']
    for x in a:
        v = x.get('value')
        if (x.get('label') or '').startswith('captura ') and isinstance(v, dict):
            pdf = os.path.join(O, v['nome'] + '.pdf'); open(pdf, 'wb').write(base64.b64decode(v['b64']))
            subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', pdf, os.path.join(O, v['nome'])], check=True)
            t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
            open(os.path.join(O, v['nome'] + '.txt'), 'w', encoding='utf8').write(t)
            print('OK', v['nome'], v['bytes'], 'bytes')
        elif (x.get('label') or '').startswith('captura '):
            print('FALHA', x.get('label'), str(v)[:100])
