# Plano · T6 "Caixa: abrir, fechar e o cofre"

- **Título:** Caixa: abrir, fechar e o cofre (o da fonte).
- **Áreas das vinhetas:** CAIXA · ABERTURA · COFRE · MULTI-CAIXA · MOVIMENTAÇÕES · FECHAMENTO · RESUMO.
- **Objetivo:** abrir o caixa com o dinheiro contado, entender o cofre (todo o dinheiro vivo da empresa) e o limite que
  ele põe na abertura, operar dois caixas (Rafael e Marcos), mover dinheiro entre banco e caixa sem virar receita, fechar
  conferindo o esperado e reabrir.
- **Antes:** T5 "Balança e impressora: o EcoTray". **Próximo:** T7 "Comprar e vender sucata".
- **Duração:** ~23 min de vídeo (3.253 palavras, ~20,9 min de fala; era 2.044 palavras em 14,5 min). Aplicada ao app **1.60.18**
  em 20/11/2026: cobertura 1.60.10 (`cobertura_160.md`) + handoff do cofre zerado/negativo (19/11).
- **Base:** `T06/inventario.md` (código 1.60.18). Desktop 1600x900, logado como **Rafael Nogueira** (administrador MASTER); um
  trecho do cap09 (cap09b) logado como **Marcos Antunes**.
- **FAKE_NOW (10/11/2026):** 08:30:00 caps 0-1; 08:30:55 cap2; 08:41:50 caps 3-5; 08:43:30 cap6; 08:45:00 caps 7-10; 08:55:00 cap11;
  17:30:00 cap12; 17:40:00 cap13; 17:42:40 cap14; 17:44:00 cap15.

## Capítulos (numeração nova: 6, 11 e 12 são novos; os antigos 6 a 12 viraram 7 a 10, 13, 14 e 15)
| # | Vinheta / título | O que a tela mostra | Estado de partida |
|---|---|---|---|
| 0 | (abertura) | Dashboard → "Financeiro" › "Caixa". Cartão "Antes: Balança e impressora: o EcoTray". | `inicio` |
| 1 | CAIXA / O caixa fechado | "Meu Caixa", cartão amarelo "Reabrir #84", "Painel Gerencial" vazio, Shift+C → "Abra o caixa antes de realizar compras". | `inicio` |
| 2 | ABERTURA / Abrir o caixa | Campo vazio e a dica do #84; digita R$ 1.500,00; **novo:** "Data e Hora de Abertura" (retroativa) e a primeira abertura da empresa; #85 aberto. | `inicio` |
| 3 | ABERTURA / Abrir com zero | Linha "Abertura do Caixa #85"; **novo:** três pontinhos › "Editar saldo de abertura" (abre e cancela) e busca/filtros/abas do histórico; dia só de Pix; aviso do zero no diálogo do Marcos. | `apos-cap02` |
| 4 | COFRE / O cofre da empresa | "Disponível no cofre agora: R$ 17.000,00 (de R$ 18.500,00 total...)"; ilustração cofre × caixa. | `apos-cap02` + diálogo do Marcos |
| 5 | COFRE / Saldo insuficiente | R$ 20.000,00 → aviso do cofre; **novo:** link "Ver tutorial: como funciona o dinheiro do caixa"; "Usar disponível (R$ 17.000,00)"; #86 aberto. | idem |
| 6 | COFRE / Cofre zerado ou negativo (**novo**, handoff 19/11) | Com #85 e #86 abertos o disponível é R$ 0,00: tenta R$ 500,00 para a Juliana → aviso "há apenas R$ 0,00 disponíveis"; botão "Abrir zerado (R$ 0,00)"; (fora do vídeo, `cofre-negativo`) → "o cofre está negativo em R$ 1.200,00 e não há dinheiro disponível"; "Abrir zerado" preenche 0,00; "Abrir Caixa" abre o #87 zerado, sem barrar. | `apos-cap05` + `cofre-negativo` no meio |
| 7 | CAIXA / Os dois cartões | (antigo 6) "Dinheiro em Caixa", cofre e barra, "Saldo Bancário", olho. | `apos-cap05` |
| 8 | MULTI-CAIXA / Cada um com o seu caixa | (antigo 7) abas, "?", painel; **novo:** calendário do painel (09/11), "Transações do Dia" e gráficos, "Resumo do Caixa Atual", botão "Saldo de Cliente/Fornecedor". | `apos-cap05` |
| 9 | MULTI-CAIXA / O caixa dos outros | (antigo 8) aba do Marcos; **novo:** permissões abrir/fechar (cadeado); cap09b = Marcos logado (voz linhas 5-6). | `apos-cap05` |
| 10 | MOVIMENTAÇÕES / Saque e sangria | (antigo 9) saque de R$ 3.000,00 + tarifa; **novo:** destino "Cofre (Conta DINHEIRO)" e "Data/hora do lançamento" no lugar da sangria sem preencher; tarifa mensal R$ 39,90. | `apos-cap05` |
| 11 | MOVIMENTAÇÕES / Despesa e receita do dia (**novo**) | "Nova Despesa" com o preenchimento inteligente (Gás da empilhadeira, R$ 50,00, dinheiro) e "Nova Receita" (Aluguel de caçamba, R$ 120,00, Pix na Conta Principal). | `apos-cap10` |
| 12 | MOVIMENTAÇÕES / Sangria no fim do dia (**novo**) | 17:30: "Saque / Sangria" › "Sangria" do caixa do Marcos, R$ 5.000,00 para a Conta Principal. | `apos-cap11` + `dia-10` |
| 13 | FECHAMENTO / Fechar o caixa | (antigo 10) esperado **R$ 957,10**; **novo:** trava (cap13a, rascunho do Valdir), cartões Saídas/Entradas, Projeção de Lucro, diferença de exemplo (950,00 → −R$ 7,10) e contagem certa, data/hora retroativa do fechamento. | `apos-cap12` |
| 14 | FECHAMENTO / Reabrir um caixa | (antigo 11) cartão amarelo "Reabrir #85" (R$ 957,10), "reabrir outro caixa", "Reabrir caixa #85?"; **novo:** corrigir pedido de caixa fechado não pede reabrir. | `apos-cap13` |
| 15 | RESUMO / Recapitulando | Montagem; cartão "Próximo: Comprar e vender sucata". | `apos-cap14` |

## Cuidados (⚠️ da fonte) e onde entram
| Cuidado | Onde | Como |
|---|---|---|
| Sem caixa aberto, compra/venda/despesa/receita não saem | cap01 | aviso "Abra o caixa antes de realizar compras" na tela e a saída logo depois ("vamos abrir") |
| A dica de valor não é o valor preenchido | cap02 | "Uma dica:" contar a gaveta e digitar |
| Caixa e cofre: o caixa só abre com o que está no cofre | cap04 e cap05 | conceito com ilustração; o aviso do cofre na tela e as duas saídas |
| Saque e sangria não são receita nem despesa; a tarifa é | cap09 | "Uma dica:" não lançar saque como "Nova Receita" |
| "Abertura do Caixa #85" só com saldo > 0 | cap03 | a linha no histórico e a explicação do zero |
| Fechamento aceita valor negativo | cap10 | "Uma dica:" (informação) |
| Sem "Ver Dinheiro Total em Caixa" vê "R$ ••••••" | cap06 | "Uma dica:" mostrando a máscara pelo olho (é a mesma) |

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (Recicla Vale Metais; Rafael, Juliana e Marcos; cofre com R$ 18.500,00):
- **Empresa:** `multi_cash_enabled` true; `cash_account_enabled` true; `cash_account_opt_out` false; atalhos de teclado
  ligados (padrão).
- **Usuários ativos:** Rafael Nogueira (admin MASTER, com "Realizar lançamentos ... data retroativa" por ser admin);
  Juliana Prado; Marcos Antunes com o acesso que o T2 der, **sem** "Ver e Operar Todos os Caixas" e sem "Gerenciar
  Contas Bancárias" (o "Operador Padrão" já é assim). Senha do Marcos no backend falso para o trecho do cap08.
- **Contas:** cofre `bank_accounts` kind `cash` "DINHEIRO (COFRE)" com saldo total **R$ 18.500,00** às 08:30 de 10/11 e
  nenhum caixa aberto; duas contas bancárias sem logo de banco (`institution_code` nulo): "Conta Principal" (padrão) e
  "Conta Secundária" (os nomes da T13 e da T14; saldos do mundo base, sugestão R$ 46.870,35 e R$ 12.400,00; a fala não
  diz nome de conta nem o saldo do banco; saldos da junção: `MUNDO_LINHA_DO_TEMPO.md`, "Bancos"). Categoria de sistema "Tarifas"
  (a junção tirou a "Tarifas bancárias"; convive com "Combustível", da T14).
- **Últimos caixas fechados:** #84 Rafael Nogueira, 09/11 07:58 → 17:44, fechou com **R$ 1.250,00**; #83 Marcos Antunes,
  09/11 07:02 → 17:36, fechou com R$ 640,00 (as três compras da T16); os anteriores do histórico. A fala não diz número de caixa: se a sequência
  do mundo der outros números, só a coluna Tela muda (#84 → último do Rafael, #85 e #86 → os dois de hoje).
- **Categoria:** "Tarifas" (a de sistema), a das tarifas do histórico.
- **Criado ao vivo (manhã, 1.60.18):** (cap06, descartável) o caixa #87 da Juliana aberto zerado; (cap11, segue na cadeia) despesa "Gás da empilhadeira"
  R$ 50,00 em dinheiro (Combustível · Pátio) e receita "Aluguel de caçamba" R$ 120,00 por Pix na Conta Principal; o #85 passa a R$ 1.450,00.
  Padrões do preenchimento: "Gás da empilhadeira" (4 usos, última em setembro de 2026, do mundo base) e "Aluguel de caçamba" (2 usos, setembro,
  das 2 contas a receber pagas que a semente `apos-cap11` acrescenta). Antes disso: caixa #85 do Rafael aberto com R$ 1.500,00 (08:31, linha "Abertura do Caixa #85"); caixa
  #86 do Marcos aberto pelo Rafael com R$ 17.000,00 (08:4x, "Usar disponível"); saque de R$ 3.000,00 da conta principal
  para o #86 com tarifa de R$ 6,50 ("Tarifa de Saque para o Caixa #86"), o #86 fica com R$ 20.000,00 e o cofre com
  R$ 21.500,00 no total; saída bancária "Tarifa mensal do pacote de serviços" R$ 39,90 da Conta Secundária, categoria
  "Tarifas", com o caixa #85.
- **Semente `dia-10` (entre o cap09 e o cap10), no caixa #85:** venda para Aços Quiririm Ltda, 1.600 kg de ferro pesado
  a R$ 1,25 = **R$ 2.000,00** por Pix/transferência na conta principal (10:15; junção: o pátio tem 2.180 kg às 08:30); compra de Aparecida Ramos, 42 kg de
  alumínio latinha a R$ 6,20 = **R$ 260,40** em dinheiro (11:20); compra de Valdir Pereira, 310 kg de ferro misto a
  R$ 0,75 = **R$ 232,50** em dinheiro (15:05). Esperado no fechamento: 1.500,00 − 50,00 − 492,90 = **R$ 957,10**. Nenhum
  pedido não finalizado no #85. O #86 do Marcos segue aberto com o movimento que o T7 quiser (não aparece aqui).
- **Criado ao vivo (fim do dia):** (cap12) sangria de R$ 5.000,00 do #86 (20.000,00 → 15.000,00) para a Conta Principal, "Depósito do fim do dia" (17:31);
  fechamento do #85 às 17:4x com R$ 957,10 (sem diferença) e a reabertura logo depois. Efeito na T9: #85 fecha com 957,10, #86 com 15.000,00.
- **Estado final:** #85 (Rafael) reaberto e #86 (Marcos) aberto, ambos em 10/11. Se o T7 começar na manhã do dia 10, ele
  parte de `apos-cap09` (os dois caixas abertos), não do fim desta aula.

## Gravação
- **Rotas:** `/dashboard`, `/caixa` (abas "Início", #85, #86), `/compra` (só o redirecionamento do cap01),
  `/movimentacoes-bancarias` (conta DINHEIRO, cap06). Janela de desktop; sem celular; sem página pública.
- **Outro usuário:** cap08, Marcos Antunes logado num navegador próprio ("o computador da balança"), só `/caixa`.
- **Cortes de relógio:** ver FAKE_NOW acima (a manhã anda; fim do dia às 17:30 e 17:40).
- **Sementes (`rec/mundo/seeds-extra/t06/`, `rec/t06/t06_sementes.py`):** `inicio` (caps 0 a 2), `apos-cap02` (caps 3 a 5; o `setup`
  dos caps 4 e 5 abre fora do vídeo "Início" › "Abrir Caixa" e escolhe "Marcos Antunes"), `apos-cap05` (caps 6 a 10; no cap06 a
  `cofre-negativo` entra no meio, por POST ao `/__dev/seed` feito pelo robô), `apos-cap10` (saque e tarifa; cap11), `apos-cap11`
  (despesa, receita e as 2 contas a receber; cap12 em diante), `dia-10` (venda e compras; cap12 em diante), `apos-cap12` (sangria;
  cap13), `dia-10-rascunho` (só o cap13a), `apos-cap13` (fechado; cap14), `apos-cap14` (reaberto; cap15).
- **Backend falso, o que precisa existir:**
  1. RPC `get_dinheiro_balance(p_company_id)` com `enabled`, `account_id`, `saldo_total`, `reservado_total` (soma dos
     saldos correntes dos caixas abertos), `disponivel` e `caixas_abertos[]` (`register_id`, `operator_id`,
     `operator_name`, `opening_balance`, `opened_at`).
  2. `cash_register`: insert com `register_number` sequencial por empresa; `opening_balance` como saldo corrente
     (o razão do caixa), `initial_opening_balance`; update de fechamento e de reabertura.
  3. `cash_transactions`: `opening`, `transfer`, `closing`, `adjustment`; delete com filtros `like`/`ilike` na reabertura.
  4. RPCs `create_manual_bank_transaction` (saque, tarifa, espelho do cofre, saída bancária) e
     `adjust_cash_register_balance`.
  5. `order_drafts` vazio para o #85 (botão "Fechar Caixa" livre); canal de tempo real `company-updates:<empresa>:<uuid>` tolerado (1.60).
  7. RPCs `get_cash_register_other_order_ids` e `get_financial_description_suggestions` (handlers do mundo base).
  6. A tela `/compra` precisa carregar o bastante para disparar o aviso e voltar (sem caixa aberto do Rafael).
- **Ilustrações** (`docs/09-aula-ilustrada.md`, estilo da marca, sem tela inventada): o dinheiro do dia no pátio
  (cap00); dia só de Pix (cap03); cofre × caixa (cap04); o limite do cofre e as duas saídas (cap05); suprimento ×
  sangria e a tarifa (cap10); esperado × contado e a volta ao cofre (cap13).

## Pronúncias
Da tabela do PERFIL: EcoSistema, EcoTray, DRE ("Registrar diferença no DRE"). Nenhuma nova. Números por extenso;
"R$ ••••••" é falado como "R$ com pontinhos".

## Decisões tomadas (o Kaik pode mudar)
1. A tela do cap01 é a do gestor (aba "Início"), porque a aula é gravada como Rafael; o cartão "Caixa Fechado" do
   operador entra só na fala.
2. O zero do cap03 é mostrado no diálogo do caixa do Marcos (campo vazio) sem confirmar; o caixa que abre com zero não
   é gravado.
3. No aviso do cofre a aula usa "Usar disponível" (o cofre segue com o total do mundo) e completa com um saque no cap09;
   "Ajustar saldo do dinheiro" só é explicado.
4. O fechamento é sem diferença (o recap da fonte); a diferença e a chave do DRE entram faladas.
