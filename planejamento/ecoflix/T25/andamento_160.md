# T25 · andamento da aplicação no 1.60.22 (21/11)

**Feito:** `tts_textos.py` (14 caps, 1.818 palavras, 10.024 caracteres com títulos), `config_narracao.json` (+ "xífti-pê", "xífti-ésse"), `roteiro.md` (gerado por script do tts + telas), `plano.md`, `inventario.md` (nota),
`preparar_aula.sh T25`, `rec/t25/gerar.py` (14 caps; 1600x900; VERSAO lê `app/dist/.versao-app`), `t25_sementes.py`, `t25_corpo.sh` e `t25_lote.sh` (novos, gravam em `/dev/shm/t25_ens`),
sementes `t25/inicio` (+ tarefas do contador 09/11 e da lona 18/11), `apos-cap06` (era apos-cap05), `apos-cap07` (escrito por `t25_sementes.py apos07`), `apos-cap12` (era apos-cap10), `cenas/ilustracoes.json` (renumeradas, `v3: pendente`, nenhuma nova).
Capítulos novos: 4 "Quem deve e como você paga" e 7 "Concluir, editar e excluir". Antigos 4 a 11 viram 5, 6, 8 a 13. Nenhum handler novo; nada pedido ao mundo base.

**Ensaios (3 lotes; o brief pedia no máximo 2):** rápido 0 falho em todos (0 a 13). Completo (voz estimada, só referência): cap01 0,99; cap03 0,17; cap04 0,32 (depois de alongar a fala, ainda sem novo completo); cap07 3,24 (antes do alongamento da fala);
cap09 1,45; cap10 4,53 (a lateral da Coleta usava seletor velho: trocado por `CARD_TAREFA`, SEM reensaio). Rápido do cap07 só passou no completo (0 falho). Refazer âncoras com a voz real.
**Sem reensaio depois da última edição:** cap07 (fala alongada em 2 linhas), cap10 (seletor da Coleta), cap04 (linha 5 alongada).

**Comandos:** subir fake: `cd /home/claude/ecoflix && FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54325 bash rec/run.sh fake` (porta 54325; instância derrubada no fim).
Lote em segundo plano: `cd /home/claude/ecoflix && bash rec/t25/t25_lote.sh 07:c 10:c 04:c > /dev/shm/t25_lote4.log 2>&1` (item `NN:r` rápido, `NN:c` completo, `NN:r:sem` captura a semente). `FAKE_NOW` fixo 2026-11-10T08:30:00-03:00.
Semente `apos-cap07` é escrita à mão (`python3 -I rec/t25/t25_sementes.py apos07`); `apos-cap06` e `apos-cap12` saem do ensaio rápido com `:sem`.

**Lido na tela (valores do ensaio):** Saldos em Aberto: A receber R$ 17.540,00 (Fundição 14.370; Aços Quiririm 2.870; Valdir Pereira 300), A pagar R$ 4.890,00 (Cooperativa Recomeço 2.550; Serra Fina 1.500; Depósito Irmãos Siqueira 840), Posição líquida +R$ 12.650,00 (só a Fundição é falada).
Métodos de Pagamento (novembro): Dinheiro 34,9%, Pix/Transferência 34,2%, Saldo 30,9%. Total Compras de outubro: Dinheiro 47,5%, Pix/Transferência 45,2%, Saldo 7,3%. Painel da Fundição na busca: telefone (12) 90000-1706, Saldo R$ 14.370,00.

**Frases sem tela:** cap09 L9 "Os atalhos valem fora dos campos de texto..." e cap10 L7 "Quem tem o módulo de Coletas..." (antigas); cap04 L7 "bom termômetro" (opinião, só o zoom em Dinheiro); cap07 L1 "Ontem o Rafael ligou pro contador" (contexto); cap06 "Pra esconder os feriados..." (antiga).
Nada de PDF na fala (o menu Exportar Relatório só abre).
**Achados para o MELHORIAS:** (1) a janela "Tarefas para hoje" não abre na gravação do 1.60.18 e 1.60.22 (marca do dia removida, página recarregada, tarefa de hoje pendente): a fala do cap10 passou a usar a faixa do Dashboard; ver se é o app (overlay) ou o mundo falso.
(2) "Pressione Enter para abrir" é quebrado por um kbd (seletor por texto exato não acha). (3) O "?" ainda não abre a lista de atalhos; "Card Lucro"/"Evolução do Lucro" na janela de configurações do Dashboard. (4) O cartão do comparativo do Total Compras mostra "Mês atual" de novembro mesmo com o filtro em "Mês passado".
(5) A Agenda do mês: o centro da célula do dia cai na tarefa e abre "Editar Tarefa": clicar no número do dia.
