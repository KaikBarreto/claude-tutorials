
# ---------------------------------------------------------------- trechos comuns (não filmados, no `setup`)
AGUARDA = {'do': 'waitFor', 'idle': True}
SETUP_DASH = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA]
SETUP_LISTA = [{'do': 'goto', 'url': '/dashboard'}, {'do': 'waitFor', 'text': 'Olá, Camila!', 'timeout': 25}, AGUARDA,
               {'do': 'goto', 'url': '/contratos'}, {'do': 'waitFor', 'text': 'Gerencie contratos recorrentes e manutenções programadas', 'timeout': 25}, AGUARDA]
PREWARM = ['/dashboard', '/contratos']
RASCUNHO = "sessionStorage.getItem('form-draft:contract-form')"
BTN = lambda n, **kw: {'role': 'button', 'name': n, 'exact': True, **kw}
BTNX = lambda n, **kw: {'role': 'button', 'name': n, **kw}
LINK = lambda n, **kw: {'role': 'link', 'name': n, 'exact': True, **kw}
TAB = lambda n, **kw: {'role': 'tab', 'name': n, 'exact': True, **kw}
ITEM = lambda n, **kw: {'role': 'menuitem', 'name': n, **kw}
OPT = lambda n, **kw: {'role': 'option', 'name': n, **kw}
SW = lambda n, **kw: {'role': 'switch', 'name': n, 'exact': True, **kw}
TXT = lambda t, **kw: {'text': t, 'exact': True, **kw}
P = lambda t, **kw: {'text': t, 'within': 'main', **kw}
PD = lambda t, **kw: {'text': t, 'within': DLG, **kw}
SEL = lambda s, **kw: {'selector': s, **kw}
DLG = '[role=dialog]'
POP = '[data-radix-popper-content-wrapper]'
CLIENTE = lambda nome: {'selector': '[cmdk-item]', 'hasText': nome}
ACOES = lambda nome: {'selector': f"main tbody tr:has-text('{nome}') button[aria-label='Ações']"}
LINHA = lambda nome: {'selector': 'main tbody tr', 'hasText': nome}
ROLA_DLG = "(()=>{const d=document.querySelector('[role=dialog] .overflow-y-auto');if(!d)return 'sem rolagem';d.scrollTo({top:%s,behavior:'%s'});return d.scrollHeight})()"
TOPO = ROLA_DLG % (0, 'auto')
