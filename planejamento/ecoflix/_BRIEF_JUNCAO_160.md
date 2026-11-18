# Briefing da junção do mundo fictício para o app 1.60.10 · trilha EcoFlix (um agente)

As 26 aulas foram auditadas contra o EcoSistema 1.60.10 (`Tnn/cobertura_160.md`, seção 3 "Proposta" e o que cada uma
diz que "o mundo precisa ter"). O Kaik mandou cobrir tudo em detalhes (aulas mais longas, nenhuma se divide). Várias
propostas pedem dado novo no mundo da Recicla Vale Metais, e algumas mexem em número que outra aula fala.
**Tarefa**: decidir e aplicar, de uma vez, o que muda no mundo base, para as aulas poderem ser atualizadas em paralelo
sem uma quebrar o número da outra. Sem aprovação no meio: decida, aplique, relate.

## Ler
- `planejamento/ecoflix/MUNDO_FICTICIO.md` (inteiro) e `PRODUCAO.md` → "Retomada de 18/11" (decisões já tomadas).
- De cada `Tnn/cobertura_160.md`: só as partes sobre o mundo, sementes, handlers e "depende de decisão" (grep por
  "mundo", "semente", "handler", "RPC", "decis"). Não releia o resto.
- O gerador do mundo base: `/home/claude/ecoflix/rec/mundo/gerar/sementes.mjs` (determinístico; confere os números
  falados) e `/home/claude/ecoflix/RELIGAR.md`. Código do app 1.60.10 (só leitura): `/dev/shm/ecoflix-src`.

## Decisões já tomadas pelo coordenador (siga)
- Edição de pedido em caixa fechado só na T09; excluir lançamentos em lote na T14 e categoria em lote na T15; pedido de
  coleta pelo portal na T20; Rastreamento entra na T12; automação da folha na T19; SPED fora; CIOT sem marca.
- Entram no mundo: um cartão de crédito (T14), um segundo OFX (T14), a devolução e a complementar da T16 (com as notas
  que elas geram), um cliente em Lucro Real (T04, exemplos fiscais sempre em Lucro Real), a despesa/receita e a sangria da
  T06, os Pix da T13, a aba Preços do portal (T20), o código do grupo GRP-7C4E9A (T22).
- Regra: o que é ESTADO DE PARTIDA de várias aulas vai no mundo base; o que acontece DENTRO de uma aula (o aluno vê
  sendo feito) fica na semente extra daquela aula (`seeds-extra/tNN/`), e as aulas seguintes da história partem de um
  estado que já o contém só se a fala delas depender disso. Prefira não mexer em número que outra aula fala; se
  precisar mexer, mude e liste a aula e a linha de fala afetadas.

## Entregar
1. `planejamento/ecoflix/JUNCAO_160.md`: para cada pedido das coberturas, a decisão (entra no mundo base, fica na
   semente da aula, ou não entra, com o motivo), os nomes e números exatos escolhidos, e a tabela "número falado que
   mudou" (aula, capítulo/linha, de → para). No fim, uma seção por aula "o que a T-nn recebe pronto e o que ela mesma
   cria", curta, para os agentes das aulas lerem só a sua.
2. `MUNDO_FICTICIO.md` atualizado (só com Edit; nada de reescrever o arquivo).
3. `/home/claude/ecoflix/rec/mundo/gerar/sementes.mjs` atualizado com o que entra no mundo base, e
   `node rec/mundo/gerar/sementes.mjs` passando em todas as conferências (ajuste as conferências que mudaram de
   propósito e diga quais). Tabelas e colunas novas do 1.60.10: `rec/mundo/schema.json` e `defaults.json` já foram
   regenerados.
4. Handlers do Supabase falso que VÁRIAS aulas vão precisar e ainda não existem (um arquivo por RPC em
   `/home/claude/ecoflix/rec/mundo/handlers/rpc/`, espelhando a migration do app, com comentário citando a migration).
   Os de uma aula só ficam para o agente da aula: liste-os no JUNCAO_160.md. As chamadas desconhecidas que a varredura
   viu estão em `/home/claude/ecoflix/rec/varredura/tNN.unknowns.json`.

## Limites
- Não edite roteiros, falas, `gerar.py` das aulas nem `cobertura_160.md`. Não abra navegador nem rode robô. Sem commit.
- Nada de dado real; nomes, CNPJs e placas fictícios no padrão do MUNDO_FICTICIO. A fala nunca cita preço de plano.
- Nada de `pkill`/`killall`, `git stash/reset/clean/checkout`; `rm` só com caminho absoluto literal. Não derrube
  instância de ninguém (há uma varredura rodando em portas 543NN).

## Relatório final (até 200 palavras)
Quantos pedidos entraram no mundo base, quantos ficaram na aula, números falados que mudaram (aula e linha), handlers
criados, e o que ficou para decidir.
