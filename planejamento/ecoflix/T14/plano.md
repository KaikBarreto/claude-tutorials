# Plano · T14 "Bancos, cofre e conciliação bancária"

- **Título:** Bancos, cofre e conciliação bancária (o da fonte).
- **Áreas das vinhetas:** BANCOS · COFRE · MOVIMENTAÇÕES · CONCILIAÇÃO · FECHAMENTO · RESUMO.
- **Objetivo:** deixar as contas da Recicla Vale Metais certas (conta nova, cofre ajustado, dinheiro que muda de lugar
  registrado como transferência) e fazer o extrato de novembro da Conta Principal bater com o sistema, linha por linha,
  até a diferença zerar e a conciliação ser finalizada.
- **Antes:** T13 "Contas a Pagar e Receber". **Próximo:** T15 "Relatório Financeiro e DRE" (fonte: "eu ganhei ou perdi
  dinheiro esse mês?").
- **Duração:** alvo da fonte ~18 min; fala estimada ~13 min (2.000 a 2.100 palavras a 2,6 palavras/s) + 15 vinhetas,
  9 ilustrações e as esperas aceleradas → **~16 min** de vídeo.
- **Módulo:** nenhum (Fase 1). O "Funcionário" do painel só é citado, não aberto.
- Base: `T14/inventario.md` (código 1.59.154). Banco, OFX e o site do banco **simulados**: nenhum banco, conta ou arquivo
  real; contas sem instituição (sem logo de terceiros).

## Capítulos

| # | Vinheta (área / título) | O que a tela mostra | Avisos e ilustração | Parte de |
|---|---|---|---|---|
| 0 | (abertura) | Vinheta; o problema do fim do mês; cartão "Antes". | [ILUSTRAÇÃO: banco × sistema que não batem] | `inicio` |
| 1 | BANCOS / A tela e as contas | Menu "Financeiro" › "Movimentações Financeiras"; lista lateral (cofre, contas, "Nova Conta"); cartão da Conta Principal e os botões; histórico; "Resumo"; abas do topo. | nome da tela muda com o cofre (informação) | `inicio` |
| 2 | BANCOS / Cadastrar e arquivar contas | "Nova Conta": "Conta Cooperativa", R$ 5.000,00, "Data desse saldo", cor; o "Ajuste de saldo - Saldo inicial" no histórico; "Editar" (dica do ajuste, sem salvar); "Tornar principal" mostrado; "Excluir" › "Arquivar" a "Poupança antiga". | ⚠️ saldo torto (dica); ⚠️ arquivar não tem volta (dica) | `inicio` |
| 3 | COFRE / O cofre e o ajuste de saldo | "DINHEIRO (COFRE)": "O cofre da empresa" R$ 18.500,00; "Ajustar saldo" para R$ 18.560,00, motivo "Contagem do cofre"; a linha "Ajuste" no histórico. | [ILUSTRAÇÃO: cofre × banco]; ajuste fora da DRE (informação) | `apos-cap02` |
| 4 | MOVIMENTAÇÕES / Movimentação, transferência e saque | "Nova Movimentação" Saída "Combustível da picape" R$ 350,00; "Transferência" Conta Secundária → Conta Principal R$ 8.000,00; "Saque" de R$ 2.000,00 para o cofre com tarifa de R$ 6,50 ("Efeitos desta transação"); "Sangria" citada. | ⚠️ mover dinheiro não é receita nem despesa (dica + [ILUSTRAÇÃO]); ⚠️ sem cofre, saque precisa de caixa aberto (dica) | `apos-cap03` |
| 5 | CONCILIAÇÃO / O que é conciliar | [ILUSTRAÇÃO: conciliação]; aba "Conciliação" com a Conta Principal já escolhida; "Como funciona?". | | `apos-cap04` |
| 6 | CONCILIAÇÃO / Importar o extrato | [ILUSTRAÇÃO: baixar o OFX no banco]; "Importar novo extrato", "Como pegar o arquivo do seu banco?", o arquivo, "Prévia do extrato", "Importar", a tabela e o rodapé. | ⚠️ conferir o sinal (dica) | `apos-cap04` |
| 7 | CONCILIAÇÃO / Casar com o sistema | A sugestão da compra do Depósito Irmãos Siqueira; as demais sugestões (acelerado); a entrada de R$ 8.000,00 por "Mais ações" › "Casar com transferência". | ⚠️ não criar receita para transferência (dica) | `apos-cap06` |
| 8 | CONCILIAÇÃO / Baixar uma conta | Boleto da água R$ 238,40 → "Baixar conta" → "Dar baixa de R$ 238,40" → "Baixada". | baixa só total por aqui (informação) | `apos-cap07` |
| 9 | CONCILIAÇÃO / Criar um lançamento | Tarifa do pacote R$ 64,90: "Mais ações" (os destinos, "Funcionário"); "Criar despesa", categoria "Tarifas", "Criar R$ 64,90". | ⚠️ vale já lançado em Funcionários (dica) | `apos-cap08` |
| 10 | CONCILIAÇÃO / Buscar e aceitar centavos | Pix da Serra Fina R$ 4.815,00 × venda de 03/11 R$ 4.815,20: "Buscar lançamento", "dif. −R$ 0,20", "Casar com valor diferente?", "Casar assim", "Diferenças casadas". | [ILUSTRAÇÃO: data e centavos]; não criar outra receita (dica) | `apos-cap09` |
| 11 | CONCILIAÇÃO / Ignorar uma linha | Tarifa avulsa −R$ 12,00 e o estorno +R$ 12,00: marcar as duas, "Soma", "Ignorar (2)", "Ignorar 2 linhas?". | [ILUSTRAÇÃO: ignorar]; ⚠️ ignorar conta como resolvido (dica) | `apos-cap10` |
| 12 | CONCILIAÇÃO / Valores repetidos | Dois Pix de R$ 380,00 no mesmo dia: o aviso âmbar, "Escolher lançamento", "Casar com o selecionado"; a outra linha já vem com a sugestão certa. | [ILUSTRAÇÃO: valores repetidos]; escolher pelo nome (dica) | `apos-cap11` |
| 13 | CONCILIAÇÃO / Desfazer e cancelar | "Desfazer" numa "Casada" e casar de novo; "Desfazer" da "Criada" mostrado; "Cancelar conciliação" (lista e "CANCELAR", depois "Manter conciliação"); "Voltar" e "Continuar conciliação". | ⚠️ três botões (informação); ⚠️ lançamento conciliado não se exclui (dica) | `apos-cap12` |
| 14 | FECHAMENTO / Fechar a conciliação | Rodapé com diferença zero; "Diferenças casadas"; "Finalizar conciliação"; "Conciliações anteriores (1)" com "Conciliado". | [ILUSTRAÇÃO: os três números]; ⚠️ sem lançamento tampão (dica) | `apos-cap12` |
| 15 | RESUMO / Recapitulando | Montagem rápida dos capítulos; cartão "Próximo: Relatório Financeiro e DRE". | | (montagem) |

Transições faladas: 0→1 "Vamos começar pela tela"; 1→2 "Vamos começar pelas contas"; 2→3 o cofre; 3→4 "hoje cedo, três
coisas no banco"; 4→5 a aba Conciliação; 5→6 "Primeiro, o extrato do banco"; 6→7 "Começa pelo mais fácil"; 7→8 o boleto
da água; 8→9 "Esta outra linha não existe em lugar nenhum"; 9→10 o Pix da Serra Fina; 10→11 "Estas duas linhas se
anulam"; 11→12 "duas linhas iguais"; 12→13 "Errou alguma?"; 13→14 "Hora de fechar".

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` e coerente com o fim do T13 (`T13/plano.md`, "Mundo"; o T13 pede que o T14 concilie os Pix
dele). `FAKE_NOW=2026-11-10T08:30:00-03:00` em todos os capítulos. Logado: Rafael Nogueira (admin MASTER, gerencia contas
bancárias e concilia). Empresa com `cash_account_enabled` true e **nenhum caixa aberto** durante a aula.

**Contas** (`bank_accounts`, todas sem instituição: `institution_code`, `institution_name` e `institution_ispb` nulos):

| Conta | kind | Principal | Cor | Saldo no fim de 31/10 | Saldo no início da aula |
|---|---|---|---|---|---|
| DINHEIRO (COFRE) | cash | | (verde fixo) | | R$ 18.500,00 (RPC `get_dinheiro_balance`), tudo "Disponível no cofre" |
| Conta Principal | bank | sim | #3B82F6 | R$ 46.382,57 | R$ 39.593,47 |
| Conta Secundária | bank | | #8B5CF6 | R$ 25.000,00 | R$ 25.000,00 |
| Poupança antiga | bank | | #F59E0B | R$ 0,00 | R$ 0,00 (último lançamento em 14/08/2026, o resgate que zerou a conta) |

Nomes: os do T13 ("Conta Principal", "Conta Secundária"). O T6 sugeriu "Conta Reserva" para a segunda: na consolidação
vale um nome só; se ficar "Conta Reserva", trocar "Conta Secundária" na Tela e nas falas dos capítulos 4, 7 e 15.
**Categorias:** despesa "Combustível" (das despesas fixas do mundo) e a de sistema "Tarifas" (a central de ajuda confirma
esse nome; o T6 escreveu "Tarifas bancárias"); centro de custo "Frota" (T13). **Conta a pagar em aberto** (T13): "Água e
esgoto de outubro", R$ 238,40, vencida em 05/11/2026, sem parceiro. Nenhuma outra conta em aberto de R$ 238,40,
R$ 64,90, R$ 12,00, R$ 380,00, R$ 4.815,00 ou R$ 8.000,00 (as do T13: prensa R$ 1.740,00 em 30/11, pneus 3x R$ 2.360,00,
aluguel da empilhadeira R$ 2.300,00, parcelas da Fundição R$ 4.790,00: nenhuma bate).

**Lançamentos da Conta Principal de 01/11 a 10/11 08:30** (`bank_transactions`; **só estes** no período, senão o OFX
precisa da linha correspondente):

| Data e hora | Origem | Valor |
|---|---|---|
| 03/11 09:40 | Compra (nº da semente; sugestão #1452) · Depósito Irmãos Siqueira · 3.000 kg de ferro misto × R$ 0,75 · Pix | −2.250,00 |
| 03/11 16:10 | Venda (sugestão #618) · Serra Fina Alumínio Reciclagem · 463 kg de alumínio perfil × R$ 10,40 · Pix | +4.815,20 |
| 05/11 10:05 | baixa da conta "Aluguel do galpão de novembro" (T13, descrição que `pay_financial_bill` grava) | −6.800,00 |
| 06/11 09:40 | Compra (sugestão #1471) · Cooperativa Recomeço · 200 kg de plástico PET × R$ 1,90 · Pix | −380,00 |
| 06/11 14:05 | Compra (sugestão #1473) · Auto Peças Vale Forte · 400 kg de ferro pesado × R$ 0,95 · Pix | −380,00 |
| 09/11 11:00 | "Conserto do pneu da empilhadeira" pago (T13, cap05) | −180,00 |
| 10/11 08:05 | baixa da "Energia elétrica de outubro" (T13, cap09) | −1.874,30 |
| 10/11 08:10 | baixa parcial da "Manutenção da prensa enfardadeira" (T13, cap09) | −1.740,00 |
| 10/11 08:15 | recebimento do saldo da Aços Quiririm Ltda (T13, cap10; o histórico entende "Valor Recebido de ...") | +2.000,00 |

Conferência: 46.382,57 − 6.789,10 = 39.593,47. A aula cria ao vivo, no dia 10/11 depois das 08:30: "Combustível da
picape" −350,00 (cap04); a transferência "Transferência: Conta Secundária → Conta Principal" +8.000,00 (cap04, duas pernas
com o mesmo `group_id`); o saque "↑ SAQUE · Conta Principal → Cofre (DINHEIRO)" −2.000,00 e "Tarifa de Saque para o Cofre"
−6,50 (cap04).

**O extrato OFX** (`Extrato_20261101_20261110.ofx`, fictício, gerado pelo agente do mundo): OFX 1.x SGML no molde de
`src/utils/ofx/fixtures/itau_sgml.ofx` (cabeçalho `OFXHEADER:100`, `CHARSET:1252`), um `<STMTRS>` só, `CURDEF` BRL,
`BANKID` fictício (sugestão 0999, conferir que não é código de banco real), `ACCTID` 40218-7, `ACCTTYPE` CHECKING,
`DTSTART` 20261101, `DTEND` 20261110, `LEDGERBAL` `BALAMT` 44933.47 `DTASOF` 20261110. Memos sem acento, nenhum
começando por "SALDO" (o parser descarta). `DTPOSTED` com hora e `[-3:BRT]`; `FITID` único por linha. As 17 linhas:

| # | DTPOSTED | TRNTYPE | TRNAMT | MEMO | No sistema | Resolve no |
|---|---|---|---|---|---|---|
| 1 | 03/11 09:41 | DEBIT | -2250.00 | PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA | compra de 03/11 | cap07 (sugestão, zoom) |
| 2 | 05/11 10:06 | DEBIT | -6800.00 | PIX ENVIADO ALUGUEL GALPAO NOV | baixa do aluguel | cap07 (sugestão) |
| 3 | 06/11 09:41 | DEBIT | -380.00 | PIX ENVIADO COOPERATIVA RECOMECO | compra da cooperativa | cap12 (ambígua) |
| 4 | 06/11 14:06 | DEBIT | -380.00 | PIX ENVIADO AUTO PECAS VALE FORTE | compra da Auto Peças | cap12 (ambígua, depois sugestão) |
| 5 | 09/11 08:00 | PAYMENT | -238.40 | PAGTO BOLETO AGUA E ESGOTO | conta a pagar da água (em aberto) | cap08 (Baixar conta) |
| 6 | 09/11 09:12 | CREDIT | 4815.00 | PIX RECEBIDO SERRA FINA ALUMINIO | venda de 03/11, R$ 4.815,20 | cap10 (Buscar, dif. −0,20) |
| 7 | 09/11 11:01 | DEBIT | -180.00 | PIX ENVIADO BORRACHARIA DOIS IRMAOS | conserto do pneu | cap07 (sugestão) |
| 8 | 09/11 23:00 | FEE | -64.90 | TARIFA PACOTE SERVICOS | nada | cap09 (Criar despesa) |
| 9 | 09/11 23:00 | FEE | -12.00 | TARIFA AVULSA | nada | cap11 (Ignorar) |
| 10 | 09/11 23:30 | CREDIT | 12.00 | ESTORNO TARIFA AVULSA | nada | cap11 (Ignorar) |
| 11 | 10/11 08:05 | DEBIT | -1874.30 | PIX ENVIADO CONCESSIONARIA ENERGIA | baixa da energia | cap07 (sugestão) |
| 12 | 10/11 08:10 | DEBIT | -1740.00 | PIX ENVIADO HIDRAULICA MORETTI LTDA | baixa parcial da prensa | cap07 (sugestão) |
| 13 | 10/11 08:15 | CREDIT | 2000.00 | PIX RECEBIDO ACOS QUIRIRIM LTDA | recebimento da Aços | cap07 (sugestão) |
| 14 | 10/11 08:10 | DEBIT | -350.00 | PIX ENVIADO AUTO POSTO BOA VIAGEM | combustível (cap04) | cap07 (sugestão) |
| 15 | 10/11 08:20 | XFER | 8000.00 | PIX RECEBIDO RECICLA VALE METAIS LTDA | transferência (cap04) | cap07 (Casar com transferência) |
| 16 | 10/11 08:25 | ATM | -2000.00 | SAQUE CAIXA ELETRONICO | saque (cap04) | cap07 (sugestão) |
| 17 | 10/11 08:25 | FEE | -6.50 | TARIFA SAQUE | tarifa do saque (cap04) | cap07 (sugestão) |

Contas: Σ das linhas = −1.449,10; saldo inicial do import = 44.933,47 + 1.449,10 = 46.382,57 = o saldo do sistema em
31/10 (outubro estava certo). Se o mundo base tiver outro saldo em 31/10, `BALAMT` = saldo de 31/10 − 1.449,10. Etiquetas
na tela: 5 "Pagamento", 8, 9 e 17 "Tarifa", 15 "Transferência", 16 "Caixa eletrônico"; as outras sem etiqueta. Nomes
novos só de memo (Borracharia Dois Irmãos, Auto Posto Boa Viagem, concessionária de energia genérica): conferir que não
são empresas reais da região. Números dos pedidos: os da semente (a fala não diz número).

**Rodapé esperado** (Saldo do banco = `BALAMT`; Saldo conciliado = saldo inicial + linhas resolvidas, sem as ignoradas;
Diferença = banco − conciliado): depois do import R$ 44.933,47 · R$ 46.382,57 · R$ -1.449,10 e "Ainda há 17 linhas
pendentes"; no fim R$ 44.933,47 · R$ 44.933,47 · R$ 0,00, "Diferenças casadas" R$ -0,20 (1). O saldo da Conta Principal
no sistema termina em R$ 44.933,67 (os R$ 0,20 da Serra Fina ficam só no resumo de ajustes).

**Esta aula cria:** a "Conta Cooperativa" (#14B8A6, R$ 5.000,00 de saldo inicial em 10/11, linha "Ajuste de saldo -
Saldo inicial"); a "Poupança antiga" arquivada; o ajuste do cofre +R$ 60,00 (motivo "Contagem do cofre"; cofre
R$ 18.560,00, depois R$ 20.560,00 com o saque); os quatro lançamentos do cap04 (Conta Secundária termina com
R$ 17.000,00); a conciliação finalizada do extrato (17 linhas: 13 casadas, 1 baixada, 1 criada, 2 ignoradas); a água
"Paga" em 09/11; a tarifa "TARIFA PACOTE SERVICOS" R$ 64,90 na categoria "Tarifas". Atualizar o `MUNDO_FICTICIO.md`
(contas, cofre e a conciliação de novembro valem para o T15 em diante).

## Gravação
- **Rotas:** `/dashboard` (só a entrada do cap01) e `/movimentacoes-bancarias` (abas "Movimentações Financeiras" e
  "Conciliação"). Desktop 1280×800, um usuário, sem celular, sem página pública. Cada capítulo abre um navegador novo na
  semente da tabela; o `setup` reabre fora do vídeo a conta ou o extrato onde o capítulo começa.
- **Sementes:** `inicio`; `apos-cap02` (conta nova, poupança arquivada); `apos-cap03` (ajuste do cofre); `apos-cap04` (os
  quatro lançamentos); `apos-cap06` (extrato importado, 17 pendentes); `apos-cap07` (10 resolvidas; pendentes as linhas
  3, 4, 5, 6, 8, 9 e 10); `apos-cap08`; `apos-cap09`; `apos-cap10`; `apos-cap11`; `apos-cap12` (0 pendentes, entrada do
  13 e do 14; o 13 desfaz e refaz a linha 1 e termina igual); `apos-cap14` (finalizada).
- **Backend falso, contas e cofre:** `bank_accounts` (select com `is_archived` false, insert, update de nome, cor, saldo e
  `is_archived`); `bank_transactions` (insert direto do ajuste inicial e do saque para o cofre, select); RPCs
  `update_bank_balance`, `update_bank_account_balance`, `create_manual_bank_transaction` (Saída e as duas pernas da
  transferência, tarifa do saque), `get_dinheiro_balance` (saldo do cofre, `caixas_abertos` vazio),
  `get_financial_movements` (histórico de cada conta, com o ajuste como "Ajuste de saldo ..." e o do cofre vindo de
  `cash_transactions`), `set_default_bank_account` (não usado); `cash_transactions` (insert do ajuste do cofre, `type`
  adjustment); `financial_categories`, `cost_centers`; `get_usable_bank_accounts`.
- **Backend falso, conciliação** (contrato em `src/hooks/useBankReconciliation.ts`, tipos `:31-385`):
  1. `get_statement_imports` (vazio no início; depois o import aberto com `pending_count`; no fim `finalized`).
  2. `create_bank_statement_import`: grava o import e as 17 linhas, calcula `opening_balance` = `p_ledger_balance` − Σ,
     devolve `inserted_count` 17, `skipped_dup_count` 0.
  3. `get_bank_reconciliation_state`: `statement_balance`, `reconciled_balance`, `difference`, `pending_count`,
     `matched_value_difference_*` e, por linha, `suggested`: linhas 1, 2, 7, 11, 12, 13, 14, 16 e 17 com
     `suggested_transaction_id` e `candidates` [o lançamento]; 3 e 4 `ambiguous` true, `candidate_count` 2, `candidates`
     [as duas compras] (depois de casar a 3, a 4 passa a ter só a compra da Auto Peças como sugestão); 5, 6, 8, 9, 10 e 15
     sem candidato, `near_matches` vazio (a 6 é de outro dia; o quase-casamento automático é do mesmo dia), `distant` 0.
     A 15 sem sugestão: a perna de transferência fica para "Casar com transferência" (é o caminho que a central de ajuda
     ensina; [TESTAR] o comportamento real da RPC; a fala vale nos dois casos).
  4. `reconcile_find_distant_exact_candidates` → vazio; `reconcile_find_in_other_accounts` → vazio.
  5. `reconcile_match_existing` (sugestão, escolhido, transferência com `p_allow_any_date`), `reconcile_search_transfer_candidates`
     (linha 15 → a perna +8.000,00 da Conta Principal, origem Conta Secundária, destino Conta Principal),
     `reconcile_search_candidates` (linha 6, busca "Serra" ou vazia → a venda de R$ 4.815,20), `reconcile_settle_bill`
     (linha 5 → a água: `status` paid, `paid_amount`, `bill_payments`, a saída em `bank_transactions` com a categoria da
     conta), `reconcile_create_transaction` (linha 8, categoria "Tarifas"), `reconcile_ignore_entries_batch` (9 e 10),
     `reconcile_unmatch_entry` (linha 1 no cap13), `cancel_bank_reconciliation` (não confirmado), `finalize_bank_reconciliation`.
  6. Casamento manual com diferença: `value_difference` −0,20 na linha 6, sem lançamento novo.
- **Arquivo:** o robô entrega `Extrato_20261101_20261110.ofx` ao `input[type=file]` da área de importação (a janela de
  arquivos do sistema não aparece). O parse é no navegador: o arquivo tem de passar no `parseOfx` real.
- **Ilustrações** (cenas HTML no estilo da marca, `docs/09-aula-ilustrada.md`; sem logo de banco; valores do mundo):
  cap00 banco × sistema que não batem; cap03 cofre × banco; cap04 dinheiro mudando de lugar; cap05 conciliação; cap06
  baixar o OFX no banco (cartões "Extrato" → "Período" → "Exportar" → "OFX"); cap10 data e centavos; cap11 ignorar;
  cap12 valores repetidos; cap14 os três números. O detalhe de cada uma está no roteiro.
- Trechos acelerados (formulário sem fala, as sugestões em sequência do cap07): selo "4x" da edição.

## Riscos e decisões
1. **"Tornar principal" só mostrado** (sem clicar): a Conta Principal segue principal para o resto da trilha. Clicar
   mudaria o padrão dos pedidos das aulas seguintes. (pergunta ao Kaik no relatório)
2. **Fonte desatualizada** (vale o código, relatório): "Abra o caixa antes de realizar saques" não existe; com o cofre o
   saque não pede caixa; a dica falada é a do código (sem cofre, saque precisa de caixa aberto). O selo de casada é
   "Casada". O menu diz "Movimentações Financeiras" com o cofre.
3. **Nenhum erro encenado:** os ⚠️ entram como "Uma dica:" na hora certa; nenhum toast de erro na tela.
4. **Fórmula do rodapé:** a do código (`ReconciliationBalanceFooter.tsx:14-22`) e da central de ajuda; a fala só afirma
   o que vale em qualquer caso (zero no fim, verde).
5. Conflitos de nome entre o T6 e o T13 (conta secundária e categoria de tarifa): resolver na consolidação.
