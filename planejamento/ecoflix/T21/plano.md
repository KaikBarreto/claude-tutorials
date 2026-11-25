# Plano · T21 · Cato, o assistente (app 1.60.22)

- **Título:** Cato, o assistente (o catálogo não muda). **Antes:** T15 "Relatório Financeiro e DRE". **Próximo:** T25 "Dashboard,
  Agenda e rotina".
- **Objetivo:** do "só consulta" ao "prepara e você confirma": autorizar e ligar a memória; perguntar (resultado, saldos,
  estoque, banco, caixa); gráfico × tabela e conferir na tela de origem; pedir compra, venda, ticket e reajuste de preço;
  baixa de conta, caixa, transferência, saldo de parceiro; cadastros; anexos; NF-e de um pedido; acompanhar pedidos;
  limites e permissões; avaliar e chegar ao atendente.
- **Áreas das vinhetas:** CATO · AUTORIZAÇÃO · MEMÓRIA · PERGUNTAS ×2 · RESPOSTAS · AÇÕES ×3 · FINANCEIRO ×2 · ARQUIVOS · FISCAL · PEDIDOS · LIMITES · AJUDA · RESUMO.
- **Alvo:** ~24 min de vídeo (2.654 palavras, 14.181 caracteres de fala). Desktop **1600×900**, Rafael Nogueira (MASTER), cortes
  como **Marcos Antunes** (cap. 2 e cap. 15). `FAKE_NOW=2026-11-10T08:30:00-03:00`. Todas as respostas e cartões do Cato são
  **simulados** no backend falso, no formato real, com os números do mundo.
- Base: `T21/inventario.md` (1.59.154) + a seção "Revisão 1.60.22" dele + `cobertura_160.md`. Código 1.60.22 em
  `/dev/shm/ecoflix-src22/src` (edge e migrations em `supabase/`). O painel abre na tela "Estoque" (`/materiais`): ali as quatro
  perguntas prontas saem sem sorteio (as duas últimas são sorteadas nas outras telas).

## Capítulos

| # | Vinheta (área / título) | O que se mostra | Ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (sem vinheta) | Abertura: pergunta e ação; cartão "Antes" | dois balões (pergunta e cartão) | `inicio` |
| 1 | CATO / Onde o Cato fica | botão redondo, balão de dica, permissão em "Usuários e Permissões", clique abre a autorização | computador × celular | `inicio` |
| 2 | AUTORIZAÇÃO / Autorizar o Cato | os pontos; corte do Marcos; "Entendi e autorizo" | o caminho da pergunta | `inicio` → `apos-cap02` |
| 3 | MEMÓRIA / A memória do Cato | "Quer que o Cato lembre de você?"; "Usar memória"; botão "Memória" (nota, lápis, lixeira, expiração); aba "Da empresa" | (só tela) | `apos-cap02` |
| 4 | PERGUNTAS / Conhecendo o painel | sugestões, clipe e microfone, "Conversas", "Mais opções do Cato", R1 e as pílulas | (só tela) | `apos-cap02` |
| 5 | PERGUNTAS / O que ele responde bem | R2 a R5; ⚠️ caixa = o de hoje | caixa do dia × mês | conversa do cap. 4 |
| 6 | RESPOSTAS / Gráfico, tabela e de onde vêm os números | R6, R7, R8; ⚠️ saldo × valor movimentado; "Abrir posição de estoque" → "Total geral" | saldo × movimentado; a regra dos gráficos | conversa do cap. 5 |
| 7 | AÇÕES / Lançar uma compra pela conversa | pergunta de pagamento, cartão de compra, "Corrigir dados", "Lançar compra", "Próximos passos"; ⚠️ "sim" não confirma, cartão vale 10 min | regra do cartão; relógio de 10 min | "Nova" (semente `apos-cap06`) |
| 8 | AÇÕES / Venda, ticket e preços | venda, ticket, reajuste de preço | estoque insuficiente | conversa do cap. 7 |
| 9 | FINANCEIRO / Contas, caixa e banco | baixa, abrir caixa, saída no caixa, transferência, fechar caixa; ⚠️ registra, não movimenta o banco | sistema × banco | conversa do cap. 8 |
| 10 | FINANCEIRO / Saldo de cliente e fornecedor | acerto (só saldo) × recebimento (saldo e dinheiro) | acerto × pagamento | conversa do cap. 9 |
| 11 | AÇÕES / Cadastros | parceiro e material novos; produção só citada | cria × altera | conversa do cap. 10 |
| 12 | ARQUIVOS / Fotos, planilhas e PDFs | foto de pesagem → ticket; print de tabela → pergunta | arquivo não manda; formatos | conversa do cap. 11 |
| 13 | FISCAL / Nota fiscal pelo Cato | "Preparar NF-e", forma de pagamento, prévia do DANFE, "Criar rascunho", "Emitir NF-e", autorizada, "Abrir DANFE" | os três tempos; Cato × tela de Notas | conversa do cap. 12 |
| 14 | PEDIDOS / Pedidos e revisões | "Acompanhar pedidos", "Respostas revisadas" | (só tela) | conversa do cap. 13 |
| 15 | LIMITES / Limites e permissões | "O que você consegue fazer?", corte do Marcos, restrições, o que não faz, limites de uso | permissão nas duas portas; o que fica nas telas; limites de uso | conversa do cap. 14 |
| 16 | AJUDA / Avaliar e falar com o suporte | 👍 e 👎, pesquisa de fim de conversa, "Falar com atendente" | (só tela) | conversa do cap. 15 |
| 17 | RESUMO / Recapitulando | montagem; cartão "Próximo: Dashboard, Agenda e rotina" | | |

**Cuidados (⚠️) com "Uma dica:"**: só o administrador autoriza (cap. 2); a memória é pessoal e não guarda número (cap. 3);
"caixa" é o caixa de hoje (cap. 5); saldo × valor movimentado (cap. 6); "sim" no chat não confirma e o cartão vale 10 minutos
(cap. 7); o Cato registra, não movimenta o banco (cap. 9); acerto × pagamento de saldo (cap. 10); arquivo sozinho não lança
nada (cap. 12); rascunho, envio e autorização são três momentos (cap. 13); permissão conferida duas vezes e limites de uso
(cap. 15). O limite de uso não é encenado.

## O que o Cato responde (e a fonte no código 1.60.22)

Regras comuns, em todos os cartões: o Cato pergunta uma informação por vez (`_shared/cato/operations.ts:230` descrições e
`systemPrompt.ts:27`); chamar a ação só propõe, "sim" escrito não executa (`capabilityAnswer.ts:33`, `systemPrompt.ts:78`);
a prévia vale 10 minutos (`CatoActionCard.tsx:329`); a permissão é conferida de novo no clique (`systemPrompt.ts:75`).

| Id | Pedido (cap.) | O que o Cato responde | Fonte (código 1.60.22) |
|---|---|---|---|
| A1a | compra sem forma de pagamento (7) | "Como esta compra será paga: dinheiro, Pix/transferência ou saldo com o fornecedor?" + "Nenhuma compra foi lançada." | `_shared/cato/purchaseIntent.ts:119-121,129` |
| A1b | "Pix, pela Conta Principal" (7) | cartão "Entrada de material": Fornecedor, item, "Preços informados nesta conversa", "Total da compra", "Forma de pagamento", "Conta", "Estoque entra e o financeiro registra R$ …", "Corrigir dados", "Agora não", "Lançar compra" | `components/cato/CatoActionCard.tsx:470-545` |
| A1c | clique (7) | "Compra lançada." + "Abrir comprovante" | `CatoActionCard.tsx:456-460,547-556` |
| (7) | "Próximos passos" | "Pedido registrado", pagamento, "Preparar NF-e" | `CatoOrderJourney.tsx:29-36`; permissão `cato_order_journeys` em `migrations/20261115143000_cato_order_journeys.sql:12,22` |
| A2 | venda completa no saldo (8) | cartão "Saída de material", "Total da venda", "Vencimento", "Estoque sai e o financeiro registra R$ …", "Lançar venda"; depois "Venda lançada." e "A receber: R$ …" | `CatoActionCard.tsx:476-545`; `CatoOrderJourney.tsx:30` |
| (8) | venda sem estoque (só ilustração) | "Não há estoque suficiente de … Use a tela de Venda para escolher uma transferência ou ajuste a quantidade." | `purchaseIntent.ts:166` |
| A3 | ticket de compra sem valores (8) | cartão "Ticket de compra", "Somente pesagem, sem valores", peso líquido, "Ao confirmar, o ticket recebe número. Estoque e financeiro não mudam até a valorização.", "Finalizar ticket" | `CatoActionCard.tsx:634-719` (649, 696, 705) |
| A4 | reajuste dos dois cobres (8) | cartão "Tabela de preços", "Reajuste em N materiais", de → para, "Confirme em até 10 minutos.", "Sim, atualizar"; depois "Reajuste aplicado." | `CatoActionCard.tsx:270-352,138-141` |
| A5 | baixa da parcela 1/3 (9) | faixa "Pagamento e recebimento", "Baixar conta", descrição, valor, "Forma", "Data", "Confirmar baixa"; depois "Conta baixada." | `CatoOperationActionCard.tsx:76`; `migrations/20261114161000_cato_money_operations.sql:21,47` |
| A6 | abrir caixa com 1.500 (9) | "Abertura de caixa", "Confirmar abertura"; depois "Caixa aberto." (saldo inicial dito explicitamente, "inclusive zero") | `CatoOperationActionCard.tsx:86`; `operations.ts:169-171`; `migrations/20261114161500_cato_money_complete.sql:82,131` |
| A7 | saída de 85 no caixa (9) | "Movimento de caixa", "Confirmar lançamento"; depois "Lançamento no caixa registrado." | `CatoOperationActionCard.tsx:78`; `20261114161000_...sql:27,50`; `20261114161500_...sql:115` |
| A8 | transferência 2.000 (9) | "Transferência entre contas", saldos antes → depois, "Confirmar transferência"; depois "Transferência registrada." | `CatoOperationActionCard.tsx:80,371-384`; `20261114161500_...sql:99,158` |
| A9 | fechar caixa contei 1.415 (9) | "Fechamento de caixa", diferença para o esperado, "Confirmar fechamento" (não confirmar) | `CatoOperationActionCard.tsx:87`; `operations.ts:178-181`; `20261114161500_...sql:89` |
| A10a | abate 100 do Valdir (10) | pergunta se o saldo é de cliente ou fornecedor (simulada: a regra manda perguntar) | `systemPrompt.ts:30` |
| A10b | "fornecedor" (10) | cartão "Movimentação no saldo", "Hoje: …", "Ele ficará te devendo R$ …", "Não movimenta caixa nem banco.", "Confirmar", "Cancelar", "Corrigir" | `components/cato/CatoBalanceActionCard.tsx:56-68` |
| A11 | recebimento de 1.000 da Aços Quiririm (10) | faixa "Saldo do parceiro", fatos "Origem", "Destino", "Forma", "Data", "Vínculo" | `CatoOperationActionCard.tsx:77,300` |
| A12 | cadastrar fornecedor (11) | "Novo parceiro", "Salvar cadastro"; depois "Cadastro de fornecedor salvo: …" (não altera parceiro existente) | `CatoOperationActionCard.tsx:81`; `operations.ts:102-112`; `migrations/20261114171000_cato_nonfiscal_qa_fixes.sql:59` |
| A13 | cadastrar material (11) | "Novo material", "Salvar cadastro" (nasce sem estoque) | `CatoOperationActionCard.tsx:82`; `operations.ts:114-124` |
| A15a | foto de pesagem (12) | "Li os dados da pesagem. O que você quer fazer com eles? Você pode pedir um ticket de compra ou de venda." | `_shared/cato/attachments.ts:68-69` |
| A15b | "Ticket de compra" (12) | cartão do ticket (A3) com "Arquivo usado" embaixo | `CatoChatPanel.tsx:1334` |
| A16a/b | print de tabela (12) | "Li a tabela do anexo. Você quer consultar os preços ou preparar uma atualização?"; "Esses valores são preços de compra ou de venda?" | `attachments.ts:65-66,144` |
| (12) | arquivo ilegível (só ilustração) | "Não consegui ler o arquivo com segurança. Pode enviar uma foto mais nítida ou um recorte menor?" | `functions/cato-assist/index.ts:655` |
| (12) | ordem escrita no arquivo (só fala) | o conteúdo é dado não confiável; o Cato não segue instruções do documento | `attachments.ts:361` |
| A17a | "Preparar NF-e" da venda no saldo (13) | "Qual forma de pagamento deve constar na NF-e: dinheiro, PIX, transferência, boleto ou duplicata a prazo?" (a forma "saldo" não é aceita) | `_shared/cato/invoiceFiscalAdapter.ts:56-58`; botão: `CatoOrderJourney.tsx:36` |
| A17b | "Duplicata a prazo" (13) | faixa "Nota fiscal eletrônica", "Rascunho de NF-e", "N item(ns) para <destinatário>", valor, fatos, "Visualizar prévia do DANFE" + "PDF para revisão. Não transmite a nota.", "Criar rascunho" | `CatoOperationActionCard.tsx:85,371-394`; `invoiceFiscalAdapter.ts:143`; `CatoDanfePreviewButton.tsx:26-30` |
| A17c | "Criar rascunho" (13) | "Rascunho preparado", "Emitir NF-e", "Consultar situação" | `CatoInvoiceResult.tsx:166-198` |
| A17d | "Emitir NF-e" (13) | "NF-e enviada para processamento na SEFAZ.", "Aguardando confirmação da SEFAZ" | `CatoOperationActionCard.tsx:261`; `CatoInvoiceResult.tsx:92,167` |
| A17e | "Consultar situação" (13) | "NF-e autorizada", "A nota nº N foi aprovada pela SEFAZ.", "O DANFE já está pronto para abrir.", "Abrir DANFE" | `CatoInvoiceResult.tsx:131-140,143` |
| (13) | recusa (só fala) | o `error_message` aparece no cartão; "Emitir novamente" | `CatoInvoiceResult.tsx:174-175,187` |
| (14) | "Acompanhar pedidos" | "Pedidos lançados por você no Cato. Até 20 registros dos últimos 30 dias.", "Para acompanhar", "Outros pedidos" | `CatoOrderJourney.tsx:72-76` |
| (14) | "Respostas revisadas" | "Nenhuma resposta revisada" | `CatoCorrectionsPanel.tsx:56` |
| A18 | "O que você consegue fazer?" (15) | "O que consigo fazer no seu acesso agora", "1. Ações com sua confirmação" (lista dos 18 rótulos), "2. Consultas", "3. Limites" | `_shared/cato/capabilityAnswer.ts:1-37` |
| A19 | Marcos pede preço (15) | "Seu usuário não tem permissão para alterar preços. Peça ao administrador da empresa para conferir seu acesso. Nenhum preço foi alterado." | `_shared/cato/priceIntent.ts:67` |
| (15) | restrições | "…o Cato fica indisponível para evitar exposição indireta." | `config/routes.ts:343,350,357,364` |
| (15) | o que não faz | cadastro existente, estoque, cancelar nota, reabrir caixa: "Ainda não consigo … pelo chat." | `_shared/cato/capabilities.ts:14-37,54` |
| (16) | pesquisa de fim de conversa | "Sim / Consegui concluir", "Em parte / Ajudou, mas faltou algo", "Não / Ainda preciso resolver", "Enviar avaliação"; só depois de 2 perguntas e 3 min parado | `CatoResolutionSurvey.tsx:20-39,298`; `CatoChatPanel.tsx:120,811-822` |

Menu e painel (cap. 4): "Mais opções do Cato" `CatoChatPanel.tsx:1099-1139`; "Sugestões para começar" `:1196`; clipe `:1608-1617`;
"Conversas", "Nova", "Memória" `:1710-1712`; "Suas conversas" `CatoHistoryDialog.tsx:119-121`. Memória (cap. 3): janela
`CatoMemoryConsentDialog.tsx:33-72` (aparece uma vez por sessão com a decisão `pending`, `CatoFab.tsx:185-190`); botão "Memória"
`CatoMemoryDialog.tsx:48-85`. Balão de dica (cap. 1): `CatoFab.tsx:295-305`. Permissão (cap. 1 e 15): `config/routes.ts:309`.

**O que saiu da fala por não dar para confirmar:** a ordem de produção e a conversão não são mostradas (sem ficha técnica
"Fardo de alumínio" confirmada na cadeia; uma frase fala delas, sustentada pelos rótulos "Preparar produção" e "Preparar
conversão de materiais" da lista de A18, `capabilityAnswer.ts:15-16`); "Ver itens e tributos" (componente `CatoFiscalDetails`
não é renderizado em lugar nenhum); "valorizar ticket" como limite (não há regra que o negue, só a tela do ticket); o ambiente
(Homologação/Produção) do cartão da nota (não anunciar); o formulário por pedido; "Respostas revisadas" só como tela vazia;
o cartão "Quer guardar esse combinado…" da memória (depende de a conversa gerar a sugestão); números de limite de uso.

## Mundo: o que esta aula precisa (do T21 antigo; o que muda está na seção seguinte)
Além do `MUNDO_FICTICIO.md`, com os números da junção (`MUNDO_LINHA_DO_TEMPO.md`): ferro misto 6.420 kg e ferro pesado 2.180 kg
(T10), cobre mel 42 kg e latão 214 kg (T7), o lote de alumínio que sai pra Minas na T17 e a chaparia da carga da T18 ainda no
pátio às 08:30; preço médio = preço de compra da tabela. A T21 herda a T13, a T14 e a T15 (as ações delas ficam antes das 08:30).

| Item | Valores (fictícios) | Onde aparece |
|---|---|---|
| Liberação do Cato | `companies.cato_enabled` = true; `ai_consent_at` vazio em `inicio`; `profiles.cato_invite_seen_at` preenchido (Rafael e Marcos) | caps. 1 e 2 |
| Marcos Antunes | com a permissão `action_use_cato` ("Usar o Cato (assistente de IA)"); não administrador | cap. 2 (corte) |
| Estoque em 10/11 08:30 (15 materiais, saldo × preço de compra = valor; × preço de venda = projeção) | Ferro pesado 2.180 kg · Ferro misto 6.420 · Chaparia 3.750 · Cobre mel 42 · Cobre misto 148 · Fio de cobre encapado 96 · Alumínio latinha 640 · Alumínio perfil 3.385 · Alumínio bloco 2.830 · Metal amarelo (latão) 214 · Bronze 38 · Inox 260 · Bateria automotiva 3.960 · Papelão 1.850 · Plástico PET 920. **Total 26.733 kg, valor R$ 96.076,00, projeção R$ 116.689,40** (sem o "Radiador de cobre", que só existe na T3) | R3, R8 e a tela "Posição de Estoque" (cap. 6: o "Total geral" tem de bater) |
| Novembro, 1 a 10 (regime de caixa, o padrão do `resumo_financeiro`) | vendas R$ 118.620,20 (Fundição Bandeira do Vale 57.460,00; Aços Quiririm 55.085,00; Serra Fina 4.815,20; Depósito Irmãos Siqueira 1.260,00); compras R$ 18.781,45; despesas R$ 32.234,10 (aluguel 6.800,00, folha 19.800,00, diesel 1.180,00 e as da T13 e da T14: pneu 180,00, energia 1.874,30, prensa 1.740,00, combustível 350,00, tarifas 64,90 e 6,50, água 238,40); resultado R$ 67.604,65 | R1, R6 |
| Saldos a receber | Fundição Bandeira do Vale R$ 14.370,00 (as 3 parcelas de R$ 4.790,00 do T13); Aços Quiririm Ltda R$ 2.870,00 (o saldo do T4 depois da baixa de R$ 2.000,00 da T13); Valdir Pereira R$ 300,00 (o vale do T4); total R$ 17.540,00 | R2 |
| Bancos | "Conta Principal" R$ 44.933,67 (o fim da T14); "Conta Secundária" R$ 82.515,00 (R$ 90.515,00 em 10/11 08:30, menos a transferência de R$ 8.000,00 da T14); "Conta Cooperativa" R$ 5.000,00 (T14); total R$ 132.448,67; novembro: entradas R$ 101.620,20 e saídas R$ 43.554,10, sem as transferências entre as contas e sem o saque para o cofre | R4 |
| Caixa de hoje | nenhum caixa aberto em 10/11 até 08:30 (a T6 abre o #85 às 08:31); ontem, 09/11: o #83 do Marcos fechou com R$ 640,00 e o #84 do Rafael com R$ 1.250,00 | R5 |
| Meses | setembro: compras R$ 201.784,25, vendas R$ 273.047,73 (regra do gerador: 93 % de outubro e a descarga de setembro; conferir na semente); outubro (T15): compras R$ 256.860,00, vendas R$ 269.240,00, por cliente Fundição 112.800,00, Aços Quiririm 77.460,60, Serra Fina 60.349,20 e Depósito Irmãos Siqueira 18.630,20; novembro até o dia 10: compras R$ 18.781,45, vendas R$ 118.620,20 | R6, R7 |

Só o estoque é conferido na tela nesta aula (cap. 6); os demais números aparecem nas respostas simuladas e saem da linha
do tempo da junção (`MUNDO_LINHA_DO_TEMPO.md`), que o gerador do mundo confere. Se a semente der outros valores, trocar nas
respostas e nas falas dos caps. 3 a 6.


### O que muda no mundo para o 1.60.22 (somar ao quadro acima)
- **Sementes:** a cadeia é a do `andamento_160.md` (t14 e t15 até `apos-cap10`, mais `t21/inicio` e `t21/apos-cap02`). Em `t21/inicio`:
  `cato_memory_manage('status')` com `personalDecision: "pending"` (cap. 3); chave `cato_adoption_nudge_<empresa>_<usuário>` **ausente** no
  armazenamento local do Rafael (cap. 1, balão); Marcos sem `cato_memory` pendente e sem editar material (cap. 2, 15). Em `t21/apos-cap06`
  (novo, criado na etapa 2): tudo igual a `apos-cap02`, com a conversa do cap. 6 já feita (o cap. 7 começa em "Nova").
- **Dados do mundo que os cartões citam** (conferidos nas sementes base): fornecedores Aparecida Ramos, Cooperativa Recomeço e Valdir Pereira;
  clientes Serra Fina Alumínio Reciclagem, Fundição Bandeira do Vale e Aços Quiririm Ltda; motoristas Jair Lopes e veículo GHT7B19;
  tabela "Principal": alumínio latinha compra 6,20, alumínio perfil venda 10,40, cobre mel compra 42,50 e cobre misto compra 36,00;
  parcelas "Fatura venda #1731 (parcela 1/3 a 3/3)" de R$ 4.790,00 (1/3 vence em 17/11); contas "Conta Principal" e "Conta Secundária";
  próximo ticket 58; última nota 1248 (a da aula sai nº 1249). **Sem caixa aberto às 08:30:** o cap. 9 abre um e fecha com a diferença.
- **A conferir no ensaio (o código não fechou só pela leitura):** o saldo inicial do "Abrir caixa" (cofre ou não); se a venda no saldo
  pergunta a forma de pagamento da NF-e (A17a); o "Total" da venda e o líquido do ticket (aritmética do pedido: 120 × 6,20 = 744,00;
  500 × 10,40 = 5.200,00; 1.480 − 60 = 1.420); o saldo do Valdir (R$ 300,00 → R$ 200,00); a diferença do fechamento; o selo de variação do
  cartão de preço; o número do pedido seguinte; o título e o rótulo do cartão "Saldo do parceiro".

### Gravação
- **Rotas:** `/materiais` (o painel abre aqui), `/materiais/posicao-estoque` (cap. 6), `/usuarios` (permissão, cap. 1 e 15; conferir a rota no ensaio). Tela 1600×900.
- **Não clicar:** "Falar no WhatsApp", "Ouvir resposta", "Apagar toda a minha memória", "Agora não" do cartão, "Confirmar fechamento".
- **Conversas:** caps. 4 a 6 numa conversa; "Nova" no cap. 7 e os caps. 7 a 16 em outra; o `setup` restaura pelo `sessionStorage` (`cato-conversation-v3:<empresa>:<usuário>`).
- **PDF na tela:** a prévia do DANFE (cap. 13) abre em aba nova; o robô devolve o PDF (padrão `POPS` + `PDF_JS` do `rec/t08/gerar.py`) e `cenas/ilustracoes.json` ganha a entrada `"tipo": "comprovante"`, `"cena": "pdf"` (etapa 3).

### Handlers novos para a etapa 2 (overlay `rec/t21/overlay`, ver `andamento_160.md`)
Edge: `cato-background`, `cato-assist` (`followups`), `plugnotas-emit` (+ `preview_danfe`). RPCs: `cato_confirm_{purchase,sale,weighing_ticket,
price,partner_balance,operation}_action` (gravam de verdade; a compra e a venda por `criarPedido` de `rec/mundo/lib/eco.mjs`),
`cato_order_journeys`, `cato_memory_manage`, `cato_routines_manage`, `cato_corrections_manage`, `get_my_cato_conversations(_messages)`,
`submit_cato_resolution_feedback`. Tabelas: `cato_jobs`, `cato_attachments`, `cato_pending_actions`, bucket `cato-attachments`.
Cada resposta A-série tem `expira_em` = agora + 10 min e o `action` no formato de `lib/cato/messages.ts` (`CatoPurchaseAction`,
`CatoSaleAction`, `CatoWeighingTicketAction`, `CatoPriceAction`, `CatoBalanceAction`, `CatoOperationAction`).

### Respostas simuladas R1 a R8 (as do T21 anterior, sem mudança; R9 saiu; formato do `response_payload`, `hooks/useCato.tsx:32-46`)
Todas com `interactionId` (uuid novo), `cacheHit: false`, sem `images`, `action` nem `budgetNotice`. `context.period`
em AAAA-MM-DD. O texto usa só o markdown que o painel desenha (negrito, listas). O campo `followups` abaixo **não** vai
no `response_payload`: é o que a edge `cato-assist` (`mode: "followups"`) devolve em `suggestions` depois da resposta.

R1 · "Como tá indo meu negócio esse mês?" (pergunta pronta)
```json
{"toolsUsed":["resumo_financeiro"],"context":{"period":{"start":"2026-11-01","end":"2026-11-10","timezone":"America/Sao_Paulo"},"regime":"caixa","updatedAt":"<agora>"},
 "answer":"Novembro começou no azul. Olhando seus lançamentos de 1 a 10 de novembro:\n\n- **Vendas:** R$ 118.620,20\n- **Compras:** R$ 18.781,45\n- **Despesas:** R$ 30.249,20\n\nO resultado até aqui é de **R$ 69.589,55**, no regime de caixa. A Fundição Bandeira do Vale foi o maior cliente do período, com R$ 57.460,00 em vendas. Ainda faltam 20 dias pro mês fechar.",
 "followups":["Compara com outubro","Quais despesas tive esse mês?","Qual material mais vendi?"]}
```
R2 · "Quem tá me devendo?"
```json
{"toolsUsed":["saldos_parceiros"],"context":{"updatedAt":"<agora>"},
 "answer":"Hoje, **3 parceiros** têm saldo a seu favor, somando **R$ 17.540,00**:\n\n1. **Fundição Bandeira do Vale:** R$ 14.370,00\n2. **Aços Quiririm Ltda:** R$ 2.870,00\n3. **Valdir Pereira:** R$ 300,00\n\nA Fundição concentra 82% do que você tem a receber.",
 "chart":{"type":"barra","title":"Saldo a receber por parceiro","valueFormat":"currency","points":[{"label":"Fundição Bandeira do Vale","value":14370},{"label":"Aços Quiririm Ltda","value":2870},{"label":"Valdir Pereira","value":300}]},
 "followups":["Pra quem eu tô devendo?","Quais contas vencem essa semana?","Quanto a Fundição me pagou em outubro?"]}
```
R3 · "Quanto tenho em estoque agora?"
```json
{"toolsUsed":["estoque_atual"],"context":{"period":{"start":"2026-11-10","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Agora você tem **26.733 kg** de material no pátio. A custo médio, esse estoque vale **R$ 96.076,00**; pela tabela de venda, a projeção é de **R$ 116.689,40**.\n\nOs materiais que mais pesam no valor:\n\n1. **Alumínio perfil:** 3.385 kg, R$ 30.126,50\n2. **Alumínio bloco:** 2.830 kg, R$ 20.093,00\n3. **Bateria automotiva:** 3.960 kg, R$ 12.276,00\n\nSó o alumínio perfil e o bloco já passam da metade do valor do estoque.",
 "followups":["Lista meu estoque em tabela","Quanto vale meu alumínio?","O que está parado há mais tempo?"]}
```
R4 · "Qual o saldo das minhas contas no banco?"
```json
{"toolsUsed":["resumo_bancario"],"context":{"period":{"start":"2026-11-01","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Agora, suas contas no banco somam **R$ 132.448,67**:\n\n- **Conta Principal:** R$ 44.933,67\n- **Conta Secundária:** R$ 82.515,00\n- **Conta Cooperativa:** R$ 5.000,00\n\nEsse é o saldo de agora. Em novembro, até hoje, entraram **R$ 114.620,20** e saíram **R$ 53.554,10** nas contas.",
 "followups":["Quais pagamentos saíram do banco esse mês?","Quanto tenho no cofre?","Compara as entradas com outubro"]}
```
R5 · "Como tá meu caixa hoje?"
```json
{"toolsUsed":["caixa"],"context":{"period":{"start":"2026-11-10","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Hoje ainda **não tem caixa aberto**: ninguém abriu o caixa até agora. Ontem, dia 9, foram dois: o do Marcos Antunes fechou com **R$ 640,00** e o do Rafael Nogueira com **R$ 1.250,00**.",
 "followups":["Quanto tenho no cofre?","Quanto comprei ontem?","Mostra os caixas da semana"]}
```
R6 · "Compras e vendas dos últimos três meses"
```json
{"toolsUsed":["compras_vendas_mensais"],"context":{"period":{"start":"2026-09-01","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Olhando suas compras e vendas dos últimos três meses:\n\n- **Setembro:** comprou R$ 201.784,25 e vendeu R$ 273.047,73\n- **Outubro:** comprou R$ 256.860,00 e vendeu R$ 269.240,00\n- **Novembro (até o dia 10):** comprou R$ 18.781,45 e vendeu R$ 118.620,20\n\nEm outubro, as compras quase alcançaram as vendas: o pátio encheu de ferro pesado. Em novembro, esse ferro saiu, e as vendas passaram longe das compras.",
 "chart":{"type":"linha","title":"Compras e vendas por mês","valueFormat":"currency","series":[{"name":"Compras","points":[{"label":"set/26","value":201784.25},{"label":"out/26","value":256860},{"label":"nov/26","value":18781.45}]},{"name":"Vendas","points":[{"label":"set/26","value":273047.73},{"label":"out/26","value":269240},{"label":"nov/26","value":118620.2}]}]},
 "followups":["Qual foi meu resultado em outubro?","Por que outubro teve tanta compra?","Compara com agosto"]}
```
R7 · "Pra quem eu mais vendi em outubro?" (`top_parceiros` não tem rótulo "Consultei...")
```json
{"toolsUsed":["top_parceiros"],"context":{"period":{"start":"2026-10-01","end":"2026-10-31"},"updatedAt":"<agora>"},
 "answer":"Em outubro, olhando suas vendas, quem mais comprou de você foi:\n\n1. **Fundição Bandeira do Vale:** R$ 112.800,00\n2. **Aços Quiririm Ltda:** R$ 77.460,60\n3. **Serra Fina Alumínio Reciclagem:** R$ 60.349,20\n\nA Fundição ficou com 42% das vendas do mês.",
 "chart":{"type":"barra","title":"Vendas por cliente em outubro","valueFormat":"currency","points":[{"label":"Fundição Bandeira do Vale","value":112800},{"label":"Aços Quiririm Ltda","value":77460.6},{"label":"Serra Fina Alumínio Reciclagem","value":60349.2}]},
 "followups":["Quanto a Fundição me deve?","Qual material mais vendi em outubro?","Compara com setembro"]}
```
R8 · "Lista meu estoque em tabela"
```json
{"toolsUsed":["estoque_atual"],"context":{"period":{"start":"2026-11-10","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Aqui está o seu estoque de agora, do maior valor para o menor. São **15 materiais**, somando **26.733 kg** e **R$ 96.076,00** a custo médio.",
 "table":{"title":"Estoque em 10/11/2026","columns":["Material","Quantidade (kg)","Valor em estoque"],"rows":[["Alumínio perfil",3385,30126.5],["Alumínio bloco",2830,20093],["Bateria automotiva",3960,12276],["Metal amarelo (latão)",214,5885],["Cobre misto",148,5328],["Ferro misto",6420,4815],["Alumínio latinha",640,3968],["Chaparia",3750,2625],["Ferro pesado",2180,2071],["Cobre mel",42,1785],["Plástico PET",920,1748],["Fio de cobre encapado",96,1728],["Inox",260,1508],["Bronze",38,1102],["Papelão",1850,1017.5]]},
 "followups":["Quanto vale meu estoque pela tabela de venda?","Me mostra num gráfico","O que está parado há mais tempo?"]}
```

## Riscos e decisões para o Kaik
1. **Duração:** ~24 min numa aula só (o Kaik pediu "nenhuma aula se divide"). A cobertura sugeria duas; ficou uma.
2. **Rotinas (cap. 14):** decidido em 25/11: os resumos agendados ainda não estão liberados para os clientes e saíram da aula (fala, gerar.py e ilustrações); só os pedidos e as respostas revisadas ficam no cap. 14.
3. **Balão de dica (cap. 1):** sorteia a frase e depende da chave local; se não der para encenar, a linha sai sem prejuízo.
4. **Títulos:** o painel diz "Agente de IA da EcoSistema"; o catálogo segue "Cato, o assistente".
5. **Ambiente da nota** não é anunciado; o modelo novo do DANFE só vale em produção a partir de 01/12/2026 (não citar).
6. **Limites de uso:** a fala não diz números (no código: 20 por minuto por usuário, 40 por minuto por empresa, 300 por dia por empresa
   e 40 por dia por usuário, ajustáveis no servidor, `cato-assist/index.ts:101-118`); há também o aviso por conversa "Esta conversa já
   fez análises mais pesadas…" (`:649,807`), não encenado.
