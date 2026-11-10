import sys, os, time, json
sys.path.insert(0, '/home/claude/domiflix/rec/t7/_ex')
os.chdir('/home/claude/domiflix')
import base
from base import rolar
SW = {"role": "switch"}
INP = lambda n=0: {"selector": "main input[placeholder='Digite o valor...']", "nth": n}
ACC = {"text": "Hi-Wall 18.000 BTUs", "within": "main"}
def passos_checklist():
    return [
      {"do":"click","target":ACC}, {"do":"wait","ms":1200},
      rolar("document.querySelector('[role=switch]')", 520), {"do":"wait","ms":400},
      {"do":"click","target":SW}, {"do":"click","target":SW}, {"do":"click","target":SW}, {"do":"click","target":SW}, {"do":"click","target":SW},
      {"do":"wait","ms":500},
      rolar("document.querySelector('input[placeholder=\"Digite o valor...\"]')", 480), {"do":"wait","ms":300},
      {"do":"click","target":INP(0)}, {"do":"type","target":INP(0),"text":"7,6"},
      {"do":"click","target":INP(1)}, {"do":"type","target":INP(0),"text":"118"},
      {"do":"click","target":INP(1)}, {"do":"type","target":INP(0),"text":"345"},
      {"do":"click","target":INP(1)}, {"do":"type","target":INP(0),"text":"12"},
      {"do":"click","target":{"text":"Temperatura de insuflamento","within":"main"}},
      {"do":"wait","ms":600},
    ]
if __name__ == '__main__':
    t0 = time.time()
    base.run('r2', passos_checklist() + [
      {"do":"shot","name":"r2-a-num-ok"},
      {"do":"state","table":"form_responses","max":12,"pick":["response_value"]},
      rolar("[...document.querySelectorAll('main *')].find(e=>e.children.length===0&&e.textContent.trim()==='Normal')", 520),
      {"do":"shot","name":"r2-b-ruido"},
      {"do":"list","selector":"main [role=checkbox]","attr":"aria-label"},
      {"do":"html","selector":"main [role=checkbox]","max":700},
    ])
    print('tempo', round(time.time() - t0))

def passos_checklist_ate_assinatura():
    LAB = "[...document.querySelectorAll('main label')].find(e=>e.textContent.trim()==='Normal')"
    GAL = {"selector":"main label","hasText":"Galeria"}
    return passos_checklist() + [
      rolar(LAB, 520), {"do":"wait","ms":300},
      {"do":"click","target":{"selector":"main label","hasText":"Normal","nth":0}},
      {"do":"wait","ms":800},
      rolar("[...document.querySelectorAll('main label')].find(b=>b.textContent.trim()==='Galeria')", 500), {"do":"wait","ms":300},
      {"do":"upload","target":GAL,"file":"rec/t7/assets/foto-equipamento.jpg","after":2200},
      rolar("document.querySelector('main textarea')", 480), {"do":"wait","ms":300},
      {"do":"click","target":{"selector":"main textarea"}},
      {"do":"type","target":{"selector":"main textarea"},"text":"Limpar os filtros a cada 30 dias e manter o dreno livre."},
      {"do":"click","target":{"text":"Recomendações ao cliente","within":"main"}},
      {"do":"wait","ms":900},
    ]
