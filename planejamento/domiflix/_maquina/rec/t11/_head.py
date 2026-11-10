#!/usr/bin/env python3
"""T11 · gera rec/t11/cap00..cap14.json (roteiros do robô) a partir da voz pronta (t11/narracao/capNN.json).

Contratos e PMOC, no COMPUTADOR (janela 1280x800, 2x), logada como Camila Duarte (admin, Glacial Cold Brasil), Dominex 1.38.19,
FAKE_NOW 2026-11-10T10:00:00-03:00 (backend 54329 E robô). Gravar com APP_ORIGIN=https://www.dominex.app (o cartão "Portal do Contrato" mostra o link).
Os `at` saem da palavra que anuncia cada passo (A(linha, palavra, folga)); o gesto "pousa" ~0,7 a 1 s depois do início do passo.
Rodar de qualquer pasta: `python3 -I rec/t11/gerar.py [NN ...]`. Depois: `node rec/record.mjs rec/t11/capNN.json --check`.

Cadeia de sementes (rec/t11/cadeia.json, de rec/t11/semear.py): fim do T5 + `t11/inicio` (fim do T10 para esta aula); depois, o último
`t11/apos-capNN` (gerado por `rec/t11/rodar.sh NN --seed`, na mesma trava da gravação). Estado de cada capítulo em SEMENTE.

O assistente "Novo Contrato" (1.38.19: 5 etapas, a mesma para comum e PMOC) atravessa os capítulos 4 a 9 e cada capítulo recomeça num navegador novo:
o `setup` (sem filmar) devolve o rascunho que o capítulo anterior deixou. O rascunho do assistente vive em `sessionStorage['form-draft:contract-form']`
(useFormDraft); o último passo de cada capítulo de 4 a 8 o devolve em `eval` rotulado "rascunho" e `rec/t11/colher.py NN` o guarda em
`rec/t11/_rascunhos/capNN.json`. O `setup` do capítulo seguinte o grava de volta no sessionStorage, abre "Novo Contrato" e aceita "Retomar rascunho".

Particularidades (lições deste tutorial, ver docs/08-licoes.md):
 - Observador `OBS`: guarda em `window.__avisos` todo aviso de erro do app, tela escura e faixa da trilha Domiflix; o eval final do capítulo devolve.
 - O cliente do seletor é um item `cmdk`: clicar por `[cmdk-item]`+texto (o nome do contrato digitado também contém o nome do cliente).
 - Nada de clique que abre outra aba ou baixa arquivo ("Imprimir PDF Anual", "Baixar TRT", "Imprimir QR Code" só recebem o cursor).
"""
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
NARR = os.path.join(TUT, 't11', 'narracao')
CAD = json.load(open(os.path.join(HERE, 'cadeia.json'), encoding='utf8'))
BASE = CAD['inicio']
IDS = CAD['ids']
RASC = os.path.join(HERE, '_rascunhos')
STORAGE = {'dominex:portal-tickets-seen:d40f5787-1779-501f-900c-ddb2b90a36e5': '2031-01-01T00:00:00.000Z'}
CARIMBO = 'assets/carimbo-rt.png'  # relativo a esta pasta (o `upload` resolve pela pasta do roteiro)

# Observador de avisos de erro na tela (aceite da fase 1): guarda em window.__avisos todo texto que apareça com "Não foi possível", "erro",
# "Tente novamente" ou "indisponível"; o passo final de cada capítulo devolve a lista (o resumo imprime) e ela tem de sair vazia.
OBS = ("(()=>{window.__avisos=[];const re=/N[ãa]o foi poss[ií]vel|erro|Tente novamente|indispon[ií]vel/i;const chk=(t)=>{t=(t||'').trim();"
       "const m=t&&t.match(new RegExp('[^]{0,40}('+re.source+')[^]{0,40}','i'));"
       "if(m&&window.__avisos.length<10)window.__avisos.push(m[0].replace(/[\\n\\r\\t ]+/g,' '))};new MutationObserver(ms=>{for(const m of ms){"
       "m.addedNodes.forEach(n=>chk(n.textContent));if(m.type==='characterData')chk(m.target.textContent)}}).observe(document.body,"
       "{childList:true,subtree:true,characterData:true});chk(document.body.innerText);"
       # tela escura de introdução e faixa de lembrete da trilha Domiflix (G1)
       "setInterval(()=>{const f=document.querySelector('section[aria-label^=\"Lembrete da trilha\"]');"
       "const e=[...document.querySelectorAll('div.fixed')].some(x=>getComputedStyle(x).backgroundColor==='rgb(17, 17, 17)');"
       "if((f||e)&&window.__avisos.length<10&&!window.__avisos.includes('TRILHA DOMIFLIX'))window.__avisos.push('TRILHA DOMIFLIX')},300);return 1})()")

NOMES = ['Abertura', 'Onde fica o PMOC', 'O Responsável Técnico', 'Um contrato comum', 'Ligando o PMOC', 'Unidade e responsável técnico',
         'Ambientes climatizados', 'A frequência da norma', 'Equipe e cobrança', 'Revisão e criação', 'O contrato por dentro', 'O cronograma do ano',
         'Os documentos da norma', 'Renovar, pausar e excluir', 'Recapitulando']
# estado de partida de cada capítulo: o último apos-capNN (de capítulo anterior) que mexeu no banco
SEMENTE = {0: None, 1: None, 2: None, 3: 'apos-cap02', 4: 'apos-cap03', 5: 'apos-cap03', 6: 'apos-cap03', 7: 'apos-cap03', 8: 'apos-cap03',
           9: 'apos-cap03', 10: 'apos-cap09', 11: 'apos-cap09', 12: 'apos-cap09', 13: 'apos-cap12', 14: 'apos-cap12'}
