# T21 · estado da gravação (porta 54340) · fase 2 (G) em 06/11, app 1.38.24 · GRAVAÇÃO FINAL PRONTA (01:33)

**Feito (06/11, 00:48 a 01:33):** emenda da L2 do recap (cap10) na velocidade natural; respiro no cap07; robô ajustado (prévia `prever.py`);
ensaio `--rapido` de 00, 04, 06, 07, 08 e 10 (0 falho); **gravação final de 00 a 10** (`lote.sh --gravar`, uma trava por capítulo, sem `--seed`).
**Não montar nem renderizar** antes do "T21: render" do coordenador.

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54340` em todo comando. FAKE_NOW 12/11 14:00 nos caps 0 a 7 e 9; 13/11 15:00
nos caps 8 e 10 (`FAKE_NOW=... FAKE_PORT=54340 rec/run.sh fake`, fora da trava; o `rodar.sh` troca sozinho). Navegador só sob `flock $TUT_HOME/.heavy.lock
nice -n 10`, uma trava por capítulo. Sem pkill; sem commit. **Sem `--seed`**: as `seeds-extra/t21/apos-capNN.json` de 05/11 valem (já alimentaram o T14 e o T17).
- `rec/t21/lote.sh [--gravar] NN ...` (sem `--gravar`: ensaio `--rapido`); resumo em `rec/t21/_debug/{ens,rec}-NN.log`. Versões da fase 1: `rodar.sh.fase1`, `lote.sh.fase1`.
- `rodar.sh` (fase 2): grava em `/dev/shm/t21_rec` e faz `mv` para `rec/t21/` (ou `_ens/`) ao fim de cada capítulo; para se o disco tiver < 1,5 GiB, se o
  8080 não responder 200 ou se a 54340 não estiver com o FAKE_NOW do capítulo (confere antes e de novo dentro da trava); recusa `--seed`.
- `prever.py NN [--tudo] [--ens]` (novo, molde do T22): simula o ritmo com as durações da última gravação (ou do ensaio rápido) e o `at` atual.
- `gerar.py` = `_head.py` + `_caps.py` + `_fim.py` (`bash rec/t21/montar.sh`). As mudanças da fase 2 estão nos comentários "fase 2" do `_caps.py`.

## Gravação final (06/11, `rec/t21/t21-capNN.{mp4,actions.json,telemetry.json,contact.jpg}`)
Todas com 0 passo falho, `unknowns` vazio, `__avisos` = "[]", 0 DIFERENTE nas conferências tela x fala, pageErrors 0, rodapé "Dominex v1.38.24", folhas
de contato sem erro do app e sem dado real (cap00: 2 avisos "Mixed Content" do logo da empresa no console, os mesmos da fase 1; o logo aparece).
| cap | vídeo | maior atraso | cap | vídeo | maior atraso |
|---|---|---|---|---|---|
| 00 | 36,31 s | 0,30 (selo Desconectado) | 06 | 30,94 s | 0,21 |
| 01 | 28,46 s | 0,42 (cadeado de Histórico) | 07 | 33,10 s | 0,29 (campo Celular) |
| 02 | 35,90 s | 0,36 (marca a caixa) | 08 | 33,27 s | 0,09 |
| 03 | 27,91 s | 0,27 | 09 | 24,06 s | 0,47 (marca L3) |
| 04 | 44,79 s | 0,03 | 10 | 31,76 s | 0,36 (Técnico a caminho) |
| 05 | 55,74 s | 0,47 (Serviço iniciado) | | | |

## Voz (fase 2)
- **cap10 L2** (`t21/narracao/trocas.json`, 1 troca com `empurra`, `EMENDA_COMPRIME_MAX=0`): frase do nó "T21 emendas 1.38.24"
  (`recebido/2055_lote6/zip/T21_emendas.mp3`, 9,12 s) no lugar de 8,52 a 16,76 s. Saída `emendas/cap10_v2.wav` + `proc.py` (take `cap10_v2`):
  29,44 -> 30,26 s (+0,81 s), -21,33 LUFS. O resto do cap10 é o take ORIGINAL (o nó "T21 cap10 Recapitulando 1.38.24" NÃO foi usado). Original em
  `cap10.v1.json`; logs `emendar_1_38_24.log` e `proc_emendas_1_38_24.log`. ASR: 0 palavra fraca nova (a única é o "QR" em 4,36 s, a mesma do take
  original). Junção limpa: silêncio a -87 dB dos dois lados, maior salto entre amostras 0,0003, vãos de 0,26 s antes e 0,39 s depois (no take original 0,32 e 0,29).
- **cap07, respiro** (`pausas.py 07 6.42:9.2`; original em `t21/narracao/emendas/cap07.orig.json`, áudio em `takes/T21_cap07_A_autoriza_o_do_cliente_pausas/`):
  9,2 s de silêncio entre a L1 e a L2 para a navegação até a janela Editar Cliente (~8,7 a 9,8 s). Narração 22,40 -> 31,60 s.
- `emendar.py` e `pausas.py` = os da skill (o `emendar.py` antigo em `emendar.py.antes_skill`); `proc.py` já era igual; `tts_textos.py` = o do planejamento.

## Mudanças no robô na fase 2 (`_caps.py`)
- A prévia pelo ensaio rápido da fase 1 dava atraso >= 0,8 s em 00 (1,55), 04 (0,81), 06 (1,77), 07 (10,6), 08 (1,48) e 10 (5,81):
  - cap00: sem o hover em "Agenda"; Configurações e Integrações com `at` fixo (0,6 e 2,9 s); marca L4 antes do último hover.
  - cap04: as duas escolhas de horário mais espaçadas ("Começa" 2,3 s antes do "sete", "Termina" 1,5 s antes do "dez").
  - cap06: aba no "Na aba Cobranças"; rolagem suave por eval (`js_main_ate`, título "Escolha quando enviar" em y 76) para lista e editor caberem
    na tela (na fase 1 o robô rolava sozinho 3 vezes); hovers da lista de 0,8 para 0,5/0,6 s.
  - cap07: respiro na voz (acima); rótulo novo "a opção Receber mensagens pelo WhatsApp, no cadastro" no "Ela", Celular no "lado", interruptor no "Hotel".
  - cap08: selos com `at` mais cedo e `seconds` menores; marca L4 antes do hover do "concluído" (o `hover()` só parte em dois na marca pendente).
  - cap10: fala nova da L2. Rolagem por eval ("Escolha quando enviar" em y 330: abas, lista e prévia juntas); o cursor segue a fala: Proteção do número,
    aba Ordens de serviço ("ligou os avisos da ordem de serviço"), aba Cobranças só apontada ("conheceu os das cobranças"), Técnico a caminho
    (Editando, Cordial) no "escolheu o estilo" e a prévia no "técnico a caminho"; Histórico no começo da L3 e contadores no "acompanhou".
- Margem sem mudar o fluxo: cap01 (cadeado de Automações 0,9 s), cap03 (Número 1,1 s), cap05 (Lembrete e Técnico a caminho 0,6 s).

## Para a montagem (só com "T21: render"; tempos em s do vídeo do capítulo, conferidos no actions.json da gravação final)
- **cap07, cortes no respiro** (fala parada de 6,28 a 15,72 s; `cortes` no spec, o `finish.py` tira vídeo e áudio juntos):
  [6,45, 7,60] (lista de clientes carregando), [10,50, 11,55] (1º clique em Ações, que não abriu o menu; o 2º clique é em 11,62 s) e
  [12,80, 15,30] (janela Editar Cliente já aberta, parada, antes da L2; a janela rola sozinha até o interruptor em 15,2 a 16,7 s). Sobram ~4,7 s do
  caminho em silêncio (Gestão 5,29, Clientes e Fornecedores 6,18, Hotel 9,12, Ações, Editar 12,44). Nenhuma aceleração pedida (o `finish.py` só corta).
- **cap10, L3** ("Viu que recebe quem está autorizado no cadastro", 17,80 a ~20,5 s): trecho reaproveitado do cap07, o hover
  "interruptor Receber mensagens pelo WhatsApp (ligado)" (cap07, gesto em 22,26 s, até 24,21 s). Nesse vão o robô do cap10 vai ao Histórico (clique em 19,51 s);
  "e acompanhou cada envio no Histórico" com os contadores (gesto em 20,20 s). L4 (22,9 a 30,3 s): Histórico parado, sob o cartão "Próximo" e a cartela.
- **cap03, ilustração** do celular lendo o QR na L2 (13,16 a 19,24 s): cobre a leitura por bastidor (15,16 s) e o pulo da tela para Automações (~17,0 s);
  a Conexão (Conectado, número, Canal ativo) volta em 20,82 s.
- Sem zoom no nome técnico do histórico ("OS · a_caminho", P1, cap08) nem no texto da prévia das cobranças (empresa de exemplo "Clima Forte Serviços", P6, cap06).

## Fase 1 (05/11)
Mundo: `semear.py` -> `seeds-extra/t21/inicio.json` (WhatsApp sem conexão, Academia sem autorização) + `corte-dia13.json` + `cadeia.json` (cadeia do T22 + `t22/apos-cap11`). `snap.mjs base` antes de gravar semente.
Sementes: `apos-cap03` (conectado), `apos-cap04` (horários 07:00 às 22:00), `apos-cap05` (automações ligadas, Cordial, lembrete), `apos-cap07` e `apos-cap10` por `compor.py` (apos-cap05 + corte do dia 13); caps 6 a 10 só leem.
Handlers novos (rec/fakebase/handlers/functions/): `whatsapp-connect`, `whatsapp-connection-select`, `whatsapp-connection-disconnect`, `whatsapp-bastidor-leitura-qr` (a "leitura do QR", chamada pelo robô no cap 3).
Lições: o 1º clique em "Integrações" logo após abrir Configurações pode não pegar (cap0 clica de novo `unless` a subaba); "Configurações" do rodapé exige `noScroll`; a subaba WhatsApp casa por `SEL('[role=tab]', hasText)`, não por papel+nome; a tela pula para Automações assim que conecta (o robô abre Conexão depois, para mostrar número e Canal ativo); o cap 10 não visita a ficha do cliente (montagem reaproveita o cap 7). Fase 2: rascunho em `rec/t21/LICOES.md`.
