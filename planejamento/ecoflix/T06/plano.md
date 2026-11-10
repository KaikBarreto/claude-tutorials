# Plano · T6 "Caixa: abrir, fechar e o cofre"

- **Título:** Caixa: abrir, fechar e o cofre (o da fonte).
- **Áreas das vinhetas:** CAIXA · ABERTURA · COFRE · MULTI-CAIXA · MOVIMENTAÇÕES · FECHAMENTO · RESUMO.
- **Objetivo:** abrir o caixa com o dinheiro contado, entender o cofre (todo o dinheiro vivo da empresa) e o limite que
  ele põe na abertura, operar dois caixas (Rafael e Marcos), mover dinheiro entre banco e caixa sem virar receita, fechar
  conferindo o esperado e reabrir.
- **Antes:** T5 "Balança e impressora: o EcoTray". **Próximo:** T7 "Comprar e vender sucata".
- **Duração:** alvo da fonte ~14 min; a fala dá ~13 min (2.044 palavras, ver `roteiro.md`), ~14,5 min com vinhetas e
  ações.
- **Base:** `T06/inventario.md` (código 1.59.154). Desktop, logado como **Rafael Nogueira** (administrador MASTER); um
  trecho do cap08 logado como **Marcos Antunes** (outro usuário).
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` nos capítulos 0 a 9 (a manhã); `2026-11-10T17:40:00-03:00` nos capítulos 10
  a 12 (fim do dia, com o movimento do dia por semente).

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área / título) | O que a tela mostra | Estado de partida |
|---|---|---|---|
| 0 | (abertura) | Dashboard → "Financeiro" › "Caixa". Problema: no ferro-velho quase tudo se paga em dinheiro vivo. Cartão "Antes: Balança e impressora: o EcoTray". | `inicio` |
| 1 | CAIXA / O caixa fechado | Aba "Início" do gestor: "Meu Caixa", "Abrir Caixa", cartão amarelo "Reabrir #84"; "Painel Gerencial" sem caixas. Atalho de compra → "Abra o caixa antes de realizar compras" e volta. | `inicio` |
| 2 | ABERTURA / Abrir o caixa | "Abrir Caixa": campo vazio, dica "R$ 1.250,00 foi o valor restante...", conta a gaveta e digita R$ 1.500,00; caixa #85 aberto. | `inicio` |
| 3 | ABERTURA / Abrir com zero | Linha "Abertura do Caixa #85" no histórico; ilustração do dia só de Pix; "Início" › "Abrir Caixa" para o Marcos: aviso amarelo do zero. | `apos-cap02` |
| 4 | COFRE / O cofre da empresa | No mesmo diálogo, "Disponível no cofre agora: R$ 17.000,00 (de R$ 18.500,00 total...)"; ilustração cofre × caixa. | `apos-cap02` + diálogo do Marcos aberto pelo `setup` |
| 5 | COFRE / Saldo insuficiente | Tenta R$ 20.000,00 para o Marcos → "⚠️ Saldo insuficiente em dinheiro"; as duas saídas; "Usar disponível (R$ 17.000,00)"; caixa #86 do Marcos aberto. | idem |
| 6 | CAIXA / Os dois cartões | "Dinheiro em Caixa" (aberto em, "Dinheiro total da empresa:" → "O cofre da empresa" com a barra), "Saldo Bancário" e os botões; olho → "R$ ••••••". | `apos-cap05` |
| 7 | MULTI-CAIXA / Cada um com o seu caixa | Abas "Início", "#85 \| Caixa - Rafael Nogueira (você)", "#86 \| Caixa - Marcos Antunes"; "?" → "Como funcionam os Multi-Caixas?"; "Início" › "Painel Gerencial". | `apos-cap05` |
| 8 | MULTI-CAIXA / O caixa dos outros | Aba do Marcos; quem pode; o Marcos logado no computador da balança vê só o caixa dele. | `apos-cap05` |
| 9 | MOVIMENTAÇÕES / Saque e sangria | Ilustração suprimento × sangria; "Saque / Sangria": saque de R$ 3.000,00 da conta principal para o caixa do Marcos com tarifa de R$ 6,50; a opção "Sangria" (sem confirmar); "Nova Movimentação Bancária": saída "Tarifa mensal do pacote de serviços" R$ 39,90. | `apos-cap05` |
| 10 | FECHAMENTO / Fechar o caixa | Fim do dia: o caixa #85 com o movimento; trava de pedido não finalizado (falada); "Fechar Caixa #85": esperado R$ 1.007,10, contado R$ 1.007,10; "Confirmar Fechamento"; "Imprimir Relatório" → "Não, obrigado". | `apos-cap09` + `dia-10` |
| 11 | FECHAMENTO / Reabrir um caixa | Cartão amarelo "Reabrir #85"; "reabrir outro caixa" (lista de todos); "Reabrir #85" → "Reabrir caixa #85?" → "Reabrir Caixa". | `apos-cap10` |
| 12 | RESUMO / Recapitulando | Montagem do que foi feito; cartão "Próximo: Comprar e vender sucata". | (montagem) |

Transições faladas: 1→2 "Então, vamos abrir"; 2→3 o histórico mostra a linha de abertura; 3→4 "quem diz quanto dá é o
cofre"; 4→5 "e se tentar mais do que tem?"; 5→6 os dois cartões com os dois caixas abertos; 6→7 as abas; 7→8 clicar na
aba do Marcos; 8→9 "os três mil que faltam vêm do banco"; 9→10 "fim do dia"; 10→11 "fechei e lembrei".

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
  nenhum caixa aberto; duas contas bancárias sem logo de banco (`institution_code` nulo), sugestão "Conta Principal"
  (padrão, R$ 46.870,35) e "Conta Reserva" (R$ 12.400,00); se o mundo base já tiver nomes e saldos, valem os dele (a
  fala não diz nome de conta nem o saldo do banco).
- **Últimos caixas fechados:** #84 Rafael Nogueira, 09/11 07:58 → 17:44, fechou com **R$ 1.250,00**; #83 Marcos Antunes,
  09/11 07:04 → 17:36, fechou com R$ 640,00; os anteriores do histórico. A fala não diz número de caixa: se a sequência
  do mundo der outros números, só a coluna Tela muda (#84 → último do Rafael, #85 e #86 → os dois de hoje).
- **Categoria:** "Tarifas bancárias" (despesa), da rotina de despesas fixas do histórico.
- **Criado ao vivo (manhã):** caixa #85 do Rafael aberto com R$ 1.500,00 (08:31, linha "Abertura do Caixa #85"); caixa
  #86 do Marcos aberto pelo Rafael com R$ 17.000,00 (08:4x, "Usar disponível"); saque de R$ 3.000,00 da conta principal
  para o #86 com tarifa de R$ 6,50 ("Tarifa de Saque para o Caixa #86"), o #86 fica com R$ 20.000,00 e o cofre com
  R$ 21.500,00 no total; saída bancária "Tarifa mensal do pacote de serviços" R$ 39,90, categoria "Tarifas bancárias",
  com o caixa #85.
- **Semente `dia-10` (entre o cap09 e o cap10), no caixa #85:** venda para Aços Quiririm Ltda, 8.000 kg de ferro pesado
  a R$ 1,25 = **R$ 10.000,00** por Pix/transferência na conta principal (10:15); compra de Aparecida Ramos, 42 kg de
  alumínio latinha a R$ 6,20 = **R$ 260,40** em dinheiro (11:20); compra de Valdir Pereira, 310 kg de ferro misto a
  R$ 0,75 = **R$ 232,50** em dinheiro (15:05). Esperado no fechamento: 1.500,00 − 492,90 = **R$ 1.007,10**. Nenhum
  pedido não finalizado no #85. O #86 do Marcos segue aberto com o movimento que o T7 quiser (não aparece aqui).
- **Criado ao vivo (fim do dia):** fechamento do #85 às 17:4x com R$ 1.007,10 (sem diferença) e a reabertura logo depois.
- **Estado final:** #85 (Rafael) reaberto e #86 (Marcos) aberto, ambos em 10/11. Se o T7 começar na manhã do dia 10, ele
  parte de `apos-cap09` (os dois caixas abertos), não do fim desta aula.

## Gravação
- **Rotas:** `/dashboard`, `/caixa` (abas "Início", #85, #86), `/compra` (só o redirecionamento do cap01),
  `/movimentacoes-bancarias` (conta DINHEIRO, cap06). Janela de desktop; sem celular; sem página pública.
- **Outro usuário:** cap08, Marcos Antunes logado num navegador próprio ("o computador da balança"), só `/caixa`.
- **Cortes de relógio:** capítulos 0 a 9 às 08:30; 10 a 12 às 17:40 (semente `dia-10`).
- **Sementes entre capítulos:** `inicio` (caps 0 a 2), `apos-cap02` (caps 3 a 5; o `setup` dos caps 4 e 5 abre fora do
  vídeo "Início" › "Abrir Caixa" e escolhe "Marcos Antunes"), `apos-cap05` (caps 6 a 9), `apos-cap09` + `dia-10`
  (cap10), `apos-cap10` (cap11).
- **Backend falso, o que precisa existir:**
  1. RPC `get_dinheiro_balance(p_company_id)` com `enabled`, `account_id`, `saldo_total`, `reservado_total` (soma dos
     saldos correntes dos caixas abertos), `disponivel` e `caixas_abertos[]` (`register_id`, `operator_id`,
     `operator_name`, `opening_balance`, `opened_at`).
  2. `cash_register`: insert com `register_number` sequencial por empresa; `opening_balance` como saldo corrente
     (o razão do caixa), `initial_opening_balance`; update de fechamento e de reabertura.
  3. `cash_transactions`: `opening`, `transfer`, `closing`, `adjustment`; delete com filtros `like`/`ilike` na reabertura.
  4. RPCs `create_manual_bank_transaction` (saque, tarifa, espelho do cofre, saída bancária) e
     `adjust_cash_register_balance`.
  5. `order_drafts` vazio para o #85 (botão "Fechar Caixa" livre); canal de tempo real `multi-cash-<empresa>` tolerado.
  6. A tela `/compra` precisa carregar o bastante para disparar o aviso e voltar (sem caixa aberto do Rafael).
- **Ilustrações** (`docs/09-aula-ilustrada.md`, estilo da marca, sem tela inventada): o dinheiro do dia no pátio
  (cap00); dia só de Pix (cap03); cofre × caixa (cap04); o limite do cofre e as duas saídas (cap05); suprimento ×
  sangria e a tarifa (cap09); esperado × contado e a volta ao cofre (cap10).

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
