# Plano · T9 "Pedidos e histórico do caixa"

- **Título:** Pedidos e histórico do caixa (o da fonte).
- **Áreas das vinhetas:** PEDIDOS · CORREÇÕES · COMPROVANTES · HISTÓRICO · RESUMO.
- **Objetivo:** achar um pedido antigo pelos filtros, corrigir pedido sem duplicar estoque nem caixa (edição e exclusão no
  caixa aberto; reabertura para o caixa já fechado), reimprimir comprovante, e usar o Histórico do Caixa (relatórios e
  reabrir).
- **Antes:** T8 "Ticket de Pesagem". **Próximo:** T10 "Estoque: saldo, histórico e posição".
- **Duração:** alvo da fonte ~12 min; a fala dá ~10,9 min (1.702 palavras), ~12,5 min com vinhetas, PDFs e ações.
- **Base:** `T09/inventario.md` (código 1.59.154). Desktop, logado como **Rafael Nogueira** (administrador).
- **FAKE_NOW:** `2026-11-11T08:30:00-03:00` (quarta), a manhã seguinte ao dia do T6. Motivo: o caixa antigo a reabrir é
  do Marcos, que não está com caixa aberto nesse dia, e o Rafael já tem o caixa dele aberto (a edição de pedido sem caixa
  aberto do usuário pode cair no aviso "Abra o caixa antes de realizar compras" ao sair da edição, `Purchase.tsx:2102-2121`).
  "Três semanas atrás" = 21/10.

## A história
A Auto Peças Vale Forte liga: vendeu bateria velha para a Recicla Vale em 21/10 e quer o comprovante. O pedido não aparece
no nome dela: o Marcos lançou no fornecedor errado (Depósito Irmãos Siqueira). Enquanto isso, no caixa de hoje do Rafael,
a latinha da Aparecida foi lançada com 24 kg em vez de 42 kg e uma compra do Valdir saiu duplicada.

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área / título) | O que a tela mostra | Estado de partida |
|---|---|---|---|
| 0 | (abertura) | Ilustração do telefonema; menu "Pedidos"; cartão "Antes: Ticket de Pesagem". | `inicio` |
| 1 | PEDIDOS / Duas telas, dois trabalhos | Ilustração pedido × caixa; "Pedidos" e "Financeiro" › "Histórico do Caixa" no menu. | `inicio` |
| 2 | PEDIDOS / A tela Pedidos | "Este mês", "Todas as Ordens", colunas, "Resumo do período filtrado", linha expandida. | `inicio` |
| 3 | PEDIDOS / Filtrar até achar | "Mês passado"; busca "Vale Forte" sem a bateria; "Tipo: Compras" + "Material: Bateria automotiva" + "Com Pix/Transferência" → 21/10, "Depósito Irmãos Siqueira", R$ 744,00. | `inicio` |
| 4 | CORREÇÕES / Editar um pedido | "Editar" no pedido de 21/10: o aviso do caixa fechado e a dica de reabrir (sem editar); "Hoje": a latinha da Aparecida, 24 kg → 42 kg, "CONFIRMAR PAGAMENTO" em dinheiro. Ilustração: desfaz e grava de novo. | `inicio` |
| 5 | CORREÇÕES / Excluir e o selo de estornado | Valdir duplicado → prévia "Vou desfazer tudo que este pedido criou:" → "Pedido excluído"; a compra de 03/11 da Aparecida com "Estornado em 05/11"; Histórico de Exclusões. | `apos-cap04` |
| 6 | COMPROVANTES / Reimprimir e cupom sem valor | "Ver comprovante" da latinha: "Popup bloqueado..." e a liberação (ilustração do navegador); PDF em nova aba; "Cupom sem valor" no Valdir → "Comprovante sem valores" → PDF sem valores. | `apos-cap05` |
| 7 | HISTÓRICO / O Histórico do Caixa | "Histórico do Caixa": colunas, corrente do mesmo dia, resumo da linha, busca "21/10". | `apos-cap06` |
| 8 | HISTÓRICO / Relatórios do caixa | No #70 de 21/10: "Ver comprovante" (fechamento) e "Relatório de estoque" (nova aba). | `apos-cap06` |
| 9 | HISTÓRICO / Reabrir um caixa antigo | "Reabrir caixa" no #70 → `/caixa`, aba do Marcos → "Editar" a bateria → "Fornecedor" "Auto Peças Vale Forte" → Pix → "Visualizar PDF" (comprovante certo) → "Fechar Caixa #70" com "Data/hora do fechamento" 21/10 17:31. | `apos-cap06` |
| 10 | RESUMO / Recapitulando | Montagem; cartão "Próximo: Estoque: saldo, histórico e posição". | (montagem) |

Transições: 0→1 "antes de procurar, onde procurar"; 2→3 "a Auto Peças não aparece"; 3→4 "achou, agora corrigir"; 4→5
"e quando o pedido nem devia existir?"; 5→6 "a Aparecida quer o comprovante novo"; 6→7 "e o caixa de 21/10?"; 8→9 "agora
corrigir lá dentro".

## Cuidados (⚠️ da fonte) e onde entram
| Cuidado | Onde | Como |
|---|---|---|
| O sistema não soma por cima: desfaz o pedido antigo e grava o novo | cap04 | ilustração + "Uma dica:" não lançar outra compra só com a diferença |
| Reabrir é o caminho menos traumático (ensinar antes de editar por cima) | cap04 (dito antes de qualquer edição) e cap09 (feito) | "Uma dica:" no aviso do "Editar Pedido"; nenhuma edição ou exclusão "por cima" de caixa fechado na aula |
| Lançamento retroativo vai pro caixa daquele dia | cap09 | a compra corrigida fica no #70 de 21/10, com a data dele; dito que vale para lançamento com data de outro dia ("Em qual caixa lançar?") |
| "Popup bloqueado..." e liberar pelo cadeado; todo PDF abre em nova aba | cap06 | o aviso na tela, a saída logo depois (ilustração do navegador) |
| A aba "Todas" pode demorar a refletir; recarregar | cap09 | "Uma dica:" depois da correção |

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` e do fim do T6 (caixas #85 e #86 de 10/11 fechados no fim daquele dia):
- **Rafael:** caixa **#87** aberto em 11/11 às 07:10 com R$ 1.200,00 (ele mesmo). Compras dele no #87, todas em dinheiro:
  07:22 Aparecida Ramos, **24 kg** de alumínio latinha a R$ 6,20 = **R$ 148,80** (o certo seriam 42 kg); 07:41 Valdir
  Pereira, 280 kg de ferro misto a R$ 0,75 = **R$ 210,00**; 07:42 a mesma compra do Valdir de novo (duplicada).
- **Marcos:** nenhum caixa aberto em 11/11. Caixa **#70** de 21/10/2026, 07:02 → 17:31, saldo inicial R$ 800,00, saldo
  final **R$ 612,50**; dentro dele: 09:15 Aparecida Ramos, 18 kg de alumínio latinha (R$ 111,60) e 138 kg de papelão
  (R$ 75,90), em dinheiro; 10:12 **"Depósito Irmãos Siqueira"** (errado: era a Auto Peças Vale Forte), **240 kg de
  bateria automotiva** a R$ 3,10 = **R$ 744,00**, Pix/Transferência na "Conta Principal". Nenhuma diferença no fechamento.
- **Auto Peças Vale Forte:** compra de 08/10 (caixa do dia), 850 kg de chaparia a R$ 0,70 = R$ 595,00, Pix (aparece na
  busca do cap03). Nenhuma compra de bateria no nome dela em outubro.
- **Tabela de preço:** Depósito Irmãos Siqueira e Auto Peças Vale Forte compram bateria pela mesma tabela (a padrão, R$ 3,10).
  A Vale Forte tem o preço especial de R$ 3,40 na bateria (T7) desde 09/11 18:00; trocar o fornecedor de um pedido salvo
  não refaz o preço dos itens já lançados (`Purchase.tsx:2180-2205` só mexe no item que está sendo digitado), então os
  240 kg seguem a R$ 3,10 `[TESTAR no ensaio]`.
- **Estornado:** 03/11, Aparecida Ramos, 38 kg de alumínio latinha e 280 kg de papelão = R$ 389,60, dinheiro, no caixa do
  Marcos de 03/11, lançada duas vezes (junção: a cooperativa tem 14 compras no T4 e o extrato da T14 não tem esse Pix); a
  cópia foi excluída em 05/11 com o caixa de 03/11 já fechado: `reverted_at` 05/11, compensação no caixa do Marcos de 05/11
  (`reverted_compensation_register_id`), a linha fica na lista com "Estornado em 05/11". Linha correspondente em
  `destructive_actions_audit` (05/11).
- **Criado ao vivo:** a latinha da Aparecida corrigida para 42 kg = R$ 260,40 (o #87 paga a diferença de R$ 111,60); a
  compra duplicada do Valdir excluída (auditoria "Excluiu compra ..."); "Cupom sem valor" ligado na compra do Valdir;
  #70 reaberto, a bateria passada para "Auto Peças Vale Forte" (mesma data, mesmo caixa, mesmo Pix) e o #70 fechado de
  novo com 21/10/2026 17:31 e R$ 612,50.
- **Estado final:** #87 do Rafael aberto; #70 fechado em 21/10. O T10 parte de `apos-cap09`.

## Gravação
- **Rotas:** `/pedidos`, `/compra` (modo edição, duas vezes), `/historico-caixa`, `/configuracoes` (aba "Empresa"),
  `/historico-exclusoes`, `/caixa` (abas "Início", #70 e #87). PDFs em nova aba (comprovante de compra, relatório de
  fechamento, relatório de estoque): o robô grava a aba nova e volta.
- **Popup bloqueado (cap06):** no primeiro "Ver comprovante" o robô faz o `window.open` da página devolver `null` (o
  navegador "bloqueou"), para o aviso real do app aparecer; a liberação no navegador é ilustração; o segundo clique abre
  normal.
- **RPCs e tabelas a simular:** `set_order_hide_financials`; `preview_order_deletion` (estoque e pagamentos do pedido, modo
  `hard_delete` com o #87 aberto); `delete_purchase_atomic` (com a linha em `destructive_actions_audit`, `entity_label` =
  nome do fornecedor, como a central de ajuda descreve); `revert_consolidated_order_atomic` (devolve `origin_register_closed`
  false com a origem aberta) e `create_purchase_atomic` (respeita `p_transaction_at` e o caixa de origem); reabrir e fechar
  com `closed_at` retroativo; filtros por material (vínculo dos itens) e por forma de pagamento.
- **Sementes entre capítulos:** `inicio` (caps 0 a 4), `apos-cap04` (latinha corrigida; cap05), `apos-cap05` (Valdir
  excluído; cap06), `apos-cap06` (cupom sem valor; caps 7 a 9). No cap09 o `setup` não precisa reabrir nada fora do vídeo.
- **Ilustrações** (`docs/09-aula-ilustrada.md`): o telefonema da Auto Peças (cap00); pedido × caixa (cap01); desfaz e
  grava de novo (cap04); excluir com caixa aberto × caixa fechado (cap05); liberar pop-ups no navegador genérico, sem logo
  (cap06); reabrir, corrigir e fechar × corrigir por cima (cap09).

## Pronúncias
Da tabela do PERFIL: PDF ("pê-dê-éfe"). Nenhuma nova. "NF-e" aparece só na tela (menu "Emitir NF-e"), não na fala.

## Decisões tomadas (o Kaik pode mudar)
1. A aula não edita nem exclui pedido de caixa fechado "por cima": o estornado aparece pronto (semente de 05/11) e a
   correção do pedido antigo é feita reabrindo o caixa (o ⚠️ da fonte manda ensinar esse caminho antes).
2. O caixa antigo é do Marcos: mostra o gestor reabrindo e fechando o caixa de outro operador (o T6 só falou disso).
3. O fechamento de novo usa "Data/hora do fechamento" do dia 21/10, para o caixa continuar com o fechamento daquele dia.
