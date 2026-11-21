# T26 · andamento da aplicação no 1.60.22 (21/11)

**Feito:** `tts_textos.py` (17 caps, 0 a 16; 2.943 palavras na legenda, 16.459 caracteres de fala + 348 de títulos; antes 1.817 palavras, 10.254 + 245), `config_narracao.json` (números novos), `roteiro.md` (gerado do tts + rótulos do robô),
`plano.md`, `inventario.md` (faixas "Aplicação 21/11"), `preparar_aula.sh T26`, `rec/t26/gerar.py` (17 caps, âncoras ok, sem aviso de ordem), `cenas/ilustracoes.json` (12 entradas; novas `ilu08_reentrada`, `ilu13_barra`;
alteradas/renumeradas `ilu03`, `ilu06_avanca`, `ilu10_regra`, `ilu14_tarefa`, todas com `clima: dados` e `v3: pendente`), sementes novas `t26/apos-cap08..apos-cap14` e `apos-cap14-dia` (REST, sem navegador),
`rec/t26/t26_corpo.sh` e `t26_lote.sh` (molde T18, quadros em /dev/shm, para se o disco < 450 MB).

**Novos capítulos:** 8 Automação com várias ações, 12 Checklist na oportunidade, 13 Probabilidade, origem e tarefas. Renumerados: 8→9, 9→10, 10→11, 11→14, 12→15 (agora com Perdidos, ordem na coluna e arrastar para Ganho), 13→16.
Sem corte, recarga nem espera de 31 s no cap10: o 1.60.22 devolve o cartão travado sozinho e atualiza selo/atividades na hora.

**Ensaios (2 lotes, fila `--prio 26`, voz ESTIMADA: atraso é só referência):** lote 1 = rápido tolerante nos 17 caps; lote 2 = rápido estrito 6, 13 a 16 + completo 3 a 16 (+ religada do 14 com a correção do arrasto da tarefa).
Completo, falhos 0 e maxLate (s): 3 (0,89), 4 (0,78), 5 (0,28), 6 (1,45), 7 (1,71), 8 (3,35), 9 (1,32), 10 (0,06), 11 (0,31), 12 (1,22), 13 (16,49: L9 e L10 apertadas, Editar > Cancelar fecha a ficha e ela é reaberta), 15 (7,46), 16 (0,58); 14 (0,0 falho, 1,52 após a correção do arrasto). Caps 0 a 2: rápido, 0 falho (só cursor/zoom).
Conferências tela x fala: 0 DIFERENTE (inclui R$ 23.650,00 / R$ 37.000,00, 25/11/2026, 80% e Telefone).

**Falta:** voz real e novo `gerar.py` com ela (refazer âncoras, sobretudo cap13 L9 a L11, cap15, cap08); completo dos caps 0 a 2;

**Comandos:** instância 54326 (derrubada no fim: `FAKE_PORT=54326 bash rec/run.sh down`; subir: `FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54326 bash rec/run.sh fake`; `rec/t26/fake_now.json` guarda o FAKE_NOW por capítulo, 17:30 nos 15 e 16).
Lote (fundo, `TUT_SENHA` aleatória no ambiente): `bash rec/t26/t26_lote.sh 14:c 15:s ...` (r tolerante, s estrito, c completo; MP4 e folha em /dev/shm/t26rec). Refazer as sementes: `FAKE_URL=http://127.0.0.1:54326 TUT_SENHA=<8+ caracteres> node rec/t26/aux/t26_cadeia.mjs` e `python3 -I rec/t26/aux/t26_dia.py`.

**Achados para o MELHORIAS:** as achados 1, 2, 6 e o histórico vazio estão corrigidos no 1.60.22 (cartão travado volta sozinho, selo/atividades atualizam). Agenda: o chip da tarefa deixou de ser `button` (usar texto). Calendário da aba Tarefas: Mês/Semana/Dia são botões de texto.
Droppable do kanban de tarefas é só a faixa de 80 px abaixo do cabeçalho (coluna vazia: soltar fora dela não muda a situação).
