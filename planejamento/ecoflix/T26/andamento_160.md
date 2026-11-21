# T26 · andamento da aplicação no 1.60.22 (21/11)

**Feito:** `tts_textos.py` (17 caps, 0 a 16; 2.943 palavras na legenda, 16.459 caracteres de fala + 348 de títulos; antes 1.817 palavras, 10.254 + 245), `config_narracao.json` (números novos), `roteiro.md` (gerado do tts + rótulos do robô),
`plano.md`, `inventario.md` (faixas "Aplicação 21/11"), `preparar_aula.sh T26`, `rec/t26/gerar.py` (17 caps, âncoras ok, sem aviso de ordem), `cenas/ilustracoes.json` (12 entradas; novas `ilu08_reentrada`, `ilu13_barra`;
alteradas/renumeradas `ilu03`, `ilu06_avanca`, `ilu10_regra`, `ilu14_tarefa`, todas com `clima: dados` e `v3: pendente`), sementes novas `t26/apos-cap08..apos-cap14` e `apos-cap14-dia` (REST, sem navegador),
`rec/t26/t26_corpo.sh` e `t26_lote.sh` (molde T18, quadros em /dev/shm, para se o disco < 450 MB).

**Novos capítulos:** 8 Automação com várias ações, 12 Checklist na oportunidade, 13 Probabilidade, origem e tarefas. Renumerados: 8→9, 9→10, 10→11, 11→14, 12→15 (agora com Perdidos, ordem na coluna e arrastar para Ganho), 13→16.
Sem corte, recarga nem espera de 31 s no cap10: o 1.60.22 devolve o cartão travado sozinho e atualiza selo/atividades na hora.

**Ensaios (2 lotes, fila `--prio 26`, voz ESTIMADA: atraso é só referência):** lote 1 = rápido tolerante nos 17 caps; lote 2 = rápido estrito 6, 13 a 16 + completo 3 a 16 (+ religada do 14 com a correção do arrasto da tarefa).
Ajuste de tempo (21/11, voz ainda ESTIMADA): completo, falhos 0 e maxLate (s): 0 (0,10), 1 (0,07), 2 (0,11), 13 (1,40), 15 (1,41); os demais caps seguem como no lote 2 (3 a 12, 14 e 16; o 8 com 3,35 e o 7 com 1,71 e o 14 com 1,52 ainda acima da meta e não mexidos nesta rodada). Conferências tela x fala: 0 DIFERENTE.
Causa do cap13 (16,49): `Editar` e a lixeira ficam no cabeçalho da ficha (fora da faixa 96..altura-70) e o robô rolava ~7 s à toa em cada gesto: `noScroll` neles. Mais: Origem digitada antes (`Esse`), Telefone/comentário/Título da tarefa adiantados, sem o hover em Tarefas, Cancelar com folga de 2 s (o cursor leva ~2 s até o rodapé).
Cap15 (7,46): o Perdidos passou a ser o ÚLTIMO trecho (some a religada dos Filtros), e a ordem das linhas mudou: Limpar, ordem na coluna, Ganho, Perdidos.
Falas trocadas: cap13 L10 "E a lixeira exclui a oportunidade." > "Reabrindo a ficha, a lixeira exclui a oportunidade." (a ficha reabre depois do Cancelar); cap15: a linha "Outro uso: em Status, Perdidos, pra rever o que não fechou. O motivo está nas observações do cartão." foi da posição 7 para a 9 (última), sem mudar o texto. Fala: 16.476 caracteres (antes 16.459). `config_narracao.json` sem mudança (nenhum número novo).
**Falta:** voz real e novo `gerar.py` com ela (refazer âncoras, sobretudo cap13 L9 a L11, cap15, cap08, cap07, cap14);

**Comandos:** instância 54326 (derrubada no fim: `FAKE_PORT=54326 bash rec/run.sh down`; subir: `FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54326 bash rec/run.sh fake`; `rec/t26/fake_now.json` guarda o FAKE_NOW por capítulo, 17:30 nos 15 e 16).
Lote (fundo, `TUT_SENHA` aleatória no ambiente): `bash rec/t26/t26_lote.sh 14:c 15:s ...` (r tolerante, s estrito, c completo; MP4 e folha em /dev/shm/t26rec). Refazer as sementes: `FAKE_URL=http://127.0.0.1:54326 TUT_SENHA=<8+ caracteres> node rec/t26/aux/t26_cadeia.mjs` e `python3 -I rec/t26/aux/t26_dia.py`.

**Achados para o MELHORIAS:** as achados 1, 2, 6 e o histórico vazio estão corrigidos no 1.60.22 (cartão travado volta sozinho, selo/atividades atualizam). Agenda: o chip da tarefa deixou de ser `button` (usar texto). Calendário da aba Tarefas: Mês/Semana/Dia são botões de texto.
Droppable do kanban de tarefas é só a faixa de 80 px abaixo do cabeçalho (coluna vazia: soltar fora dela não muda a situação).
