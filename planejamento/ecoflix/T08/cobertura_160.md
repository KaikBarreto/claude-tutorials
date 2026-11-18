# Cobertura 1.60.10 · T8 Ticket de Pesagem

Auditoria de 18/11/2026, só leitura de código (`/dev/shm/ecoflix-src`, 1.60.10) e `git diff f37573ea0 5290be4cd`.
Nada foi aberto no navegador nem rodado no robô: tudo abaixo é o que o código diz, não o que foi visto na tela. Não há
varredura do robô para a T08 (`rec/varredura/t08.txt` não existe). Caminhos relativos a `src/`.

Arquivos da aula com mudança desde o 1.59.154: `pages/WeighingTicket.tsx` (+302), `components/weighing/WeighingTicketForm.tsx`
(+467), `utils/thermalReceiptGenerator.ts`, `utils/buildWeighingReceiptParams.ts`, `components/EntitySearchModal.tsx`,
`components/Quick{Supplier,Customer}Dialog.tsx`, `components/MultiPaymentDialog.tsx`,
`components/settings/SettingsUsabilityContent.tsx`, `components/settings/SettingsIntegrationsContent.tsx`,
`config/routes.ts`. Sem mudança: cartão, kanban, tabela, criador de abas, `OrderSwitcher`, `AdvancedWeighingDialog`,
`ExportTicketsDialog`, `ReceiptFormatDialog` (os capítulos 03 a 06 batem como estão).

## 1. Mudou no app

### cap01 · Quando usar o ticket
- **A fala da pesagem avulsa ficou errada.** O roteiro diz "é só um comprovante de peso" e a ilustração/plano marcam 🚫.
  Desde o 1.59.163 a avulsa pode cobrar: com "Valor cobrado pela pesagem" maior que zero, salvar abre o pagamento e lança
  receita no caixa ou no banco, ou dívida e conta a receber no saldo do cliente
  (`WeighingTicketForm.tsx:1837-1851,3113-3184`; RPC `finalize_weighing_ticket_v4` e `apply_standalone_weighing_charge_v1`,
  `WeighingTicket.tsx:2028,2113`). Continua verdade: não vira pedido e não mexe no estoque. Fala nova na seção 3 (A).
- O resto do capítulo (menu, colunas, aba "Pesagens avulsas", "Nenhuma pesagem avulsa registrada", "Nova Pesagem
  Avulsa") não mudou (`WeighingTicket.tsx:3790-3791,3979,3970`).

### cap02 · Criar o ticket
- **Janela "Selecionar Fornecedor"**: ganhou o botão "+" ao lado da busca (`aria-label="Cadastrar novo"`,
  `EntitySearchModal.tsx:266-273`) e, quando a busca não acha ninguém, embaixo de "Nenhum resultado encontrado." aparece
  o botão **"Cadastrar «o que foi digitado»"** (`:332-343`). O roteiro não clica neles, mas o "+" aparece no quadro.
- **"Cadastro Rápido de Fornecedor"** (aberto pela busca ou pelo "+" do campo): novo campo **"Chave PIX"** ("Email, CPF,
  telefone ou chave aleatória", `QuickSupplierDialog.tsx:540-544`; no de cliente, `QuickCustomerDialog.tsx:522`). Vindo
  da busca, o que foi digitado já entra em "Nome" ou, se forem só números com 3 dígitos ou mais, em "CPF/CNPJ"
  (`WeighingTicketForm.tsx:2772-2776`).
- **"Com valores"** (o roteiro só dá zoom): a "Tabela de Preços" do ticket novo agora nasce na ordem tabela do parceiro >
  tabela preferida do usuário > tabela padrão da empresa (`WeighingTicketForm.tsx:813-846`). Antes nascia vazia.

### cap06 · Salvar
- RPC do salvar mudou de `finalize_weighing_ticket_v3` para **`finalize_weighing_ticket_v4`** (`WeighingTicket.tsx:2113`).
  Rótulos e janela "Ticket #58 salvo" iguais. **O handler do mundo fictício precisa responder à v4** (devolve também
  `standalone_charge_status`).

### cap07 · Valorizar
- **Ordem do preço na valorização mudou**: tabela gravada no ticket > tabela padrão do fornecedor
  (`suppliers.default_price_table_id`) > tabela preferida do usuário (`profiles.preferred_price_table_id`) > tabela
  padrão da empresa (`WeighingTicket.tsx:2413-2459`, `resolveInitialPriceTableId`). Antes era ticket > padrão da empresa.
  O preço personalizado do fornecedor continua na frente de tudo. Para a Cooperativa dar R$ 6,20, o Rafael não pode ter
  tabela preferida diferente da "Principal" na semente. A fala "O preço vem da tabela" continua certa.
- O valorizar agora faz duas leituras a mais (`suppliers` e, às vezes, `profiles`): conferir os handlers.

### cap08 · Comprovante
- **Título do cupom térmico**: era "Ticket N° …", agora **"Ticket de pesagem N° #58"**
  (`utils/thermalReceiptGenerator.ts:1565-1569`). A marca d'água atravessada saiu do cupom (nota do 1.59.155). As faixas
  "TICKET DE PESAGEM" / "NÃO VALORIZADO" e "Documento sem valor financeiro definitivo" continuam (`:1098-1163`) enquanto
  "Marca de ticket não valorizado" estiver ligada, que é o padrão (`:1191-1196`). O PDF guardado
  `rec/t08/arquivos/cap08-comprovante-termico.pdf` é do 1.59.154: **gerar de novo** para a ilustração.
- **Dados do fornecedor no comprovante**: a reimpressão agora carrega o cadastro inteiro do parceiro (CPF/CNPJ, endereço,
  telefone, conforme as chaves "mostrar nos documentos" do cadastro), não só o nome (`WeighingTicket.tsx:536-596,3482`).
  O cupom da Cooperativa pode sair com mais linhas que o de antes.
- **Assinaturas**: com "Assinaturas no comprovante" ligado, o respiro acima das linhas subiu de 8 para 14 mm e agora
  existe a escolha "Quem assina" (seção 2). Só afeta o quadro se a semente ligar a chave.
- Configurações › Integrações: "Imprimir comprovante do Ticket de Pesagem" igual (`SettingsIntegrationsContent.tsx:559`).
  Na mesma tela, a trava do peso da balança mudou de texto: "Padrão da empresa; exceções ficam em Usuários e Permissões"
  (`:665`). É da T5/T2; só cuidar para não aparecer no zoom com texto antigo em mente.

### cap09 · Finalizar a compra
- **Cupom da compra que nasceu de ticket**: a linha do operador vira duas, **"Ticket: Rafael"** (quem pesou) e
  **"Caixa: Rafael"** (quem finalizou) (`thermalReceiptGenerator.ts:1626-1639`). Só aparece se o robô abrir "Imprimir
  Comprovante" (o roteiro manda fechar).
- `pages/Purchase.tsx` mudou muito (+740), mas "Compra registrada!" (`:3305`) e "Pedido finalizado — voltando ao Ticket
  de Pesagem" (`:3586`) seguem iguais. Os rótulos do finalizar são da T7: valer o que a auditoria da T07 disser.

## 2. Falta cobrir

| # | O que é (rótulo exato, arquivo) | Quando o cliente usa | Vale? |
|---|---|---|---|
| 1 | **Pesagem avulsa de ponta a ponta**: "Modalidade" › "Pesagem avulsa"; "Tipo" fixo em **"Serviço ao cliente"**; campo "Cliente"; **"Descrição do material"** ("Ex.: Areia, terra, entulho"); "Tipo de caminhão" ("Ex.: Carreta, caçamba, bitrem"); **"Valor cobrado pela pesagem"**; "Itens da Pesagem"; **"Salvar Pesagem Avulsa"** (`WeighingTicketForm.tsx:1903-1936,1954,2110,2172,2574-2587`) | Balança que presta serviço para terceiro (areia, entulho, caminhão do vizinho) | **Sim, capítulo novo** (B) |
| 2 | **Cobrança da avulsa**: com valor, salvar abre "Finalizar Pedido" ("Total: R$ …") com "Dinheiro", "Pix/Transferência" e "Saldo do Cliente", até 3 formas juntas, sem parcelamento; com dinheiro, **"Caixa que recebe o dinheiro"**; "CONFIRMAR PAGAMENTO". Depois: campo travado com "Cobrança já lançada no financeiro. O valor não pode mais ser alterado." Erros: "Selecione o caixa que receberá o dinheiro"; do banco, "Selecione um cliente para lançar a pesagem no saldo." (`WeighingTicketForm.tsx:3113-3184,1931-1935`; migration `20261111193000`) | Cobrar a pesagem na hora ou pôr na conta do cliente | **Sim**, mesmo capítulo (B) |
| 3 | Avulsa cobrada **não pode ser excluída** ("Pesagem avulsa com cobrança não pode ser excluída. Estorne o financeiro antes.") e gera categoria "Serviço de pesagem" e lançamento "Serviço de pesagem avulsa #…" | Quem errou o valor | Só citar em B (uma frase); o estorno é da T13/T14 |
| 4 | **Cadastrar pela busca** (seção 1, cap02) | Fornecedor ou cliente novo no portão, sem sair do ticket | **Sim, trecho** (C), dentro do capítulo da avulsa |
| 5 | **Ticket "Com valores"**: "Tabela de Preços" ao lado do fornecedor, coluna de valor, "Total geral"; aba mostra "Valor" (`WeighingTicketForm.tsx:2703-2720`) | Preço já combinado, mas quem paga é o caixa depois | **Sim, trecho** (D): hoje é só um zoom |
| 6 | **Forma de pagamento no ticket**: Configurações › Usabilidade › "Permitir forma de pagamento no ticket de pesagem" ("O balanceiro escolhe a forma de pagamento já no ticket com valores; a compra/venda abre pré-preenchida.") (`SettingsUsabilityContent.tsx:1147-1167`) | Balanceiro combina a forma, caixa só confirma | Só citar em D (uma frase, com zoom na chave) |
| 7 | **"Exigir cliente/fornecedor no Ticket de Pesagem"** (`SettingsUsabilityContent.tsx:1117-1135`; erro "Selecione o fornecedor para salvar o ticket") | Dono que não quer ticket sem dono | Só citar (E) |
| 8 | **Assinaturas**: Configurações › Usabilidade › "Assinaturas no comprovante" + **"Quem assina"**: "Operador e cliente/fornecedor", "Só o cliente/fornecedor", "Só o operador"; "No ticket de pesagem, o operador aparece como Empresa." (`SettingsUsabilityContent.tsx:878-929`; `thermalReceiptGenerator.ts:2352-2380`) | Motorista assina o peso na saída | **Sim, trecho** no cap08 (E) |
| 9 | **"Marca de ticket não valorizado"** ("Mantém o aviso igual na tela, no PDF e na impressão. Tickets provisórios offline continuam identificados.") (`SettingsUsabilityContent.tsx:935-955`) | Quem não quer a faixa no papel | Só citar em E |
| 10 | **Valorizar vários tickets juntos**: "Selecionar" no cartão ou na lista, barra **"Valorizar 2 tickets"**; regras: "Selecione somente tickets do mesmo tipo", "Selecione tickets do mesmo cliente ou fornecedor" (`WeighingTicket.tsx:4117-4131,2693-2702`) | Fornecedor com várias cargas no dia, um pagamento só | **Sim, trecho** no cap07 (F) |
| 11 | **Ticket de venda** ("Tipo" › "Venda", campo "Cliente", valorizar abre `/venda`) | Carga saindo com peso a confirmar | Só citar (já há meia frase no cap07; manter) |
| 12 | **Editar e Excluir** no menu "Ações": título "Editar Ticket #58"; "Confirmar exclusão" ("Tem certeza que deseja excluir este ticket de pesagem? Esta ação não pode ser desfeita."); valorizado: "Este ticket já virou pedido e não pode ser editado." (`WeighingTicket.tsx:3227,4137-4140`) | Corrigir peso ou apagar ticket errado antes de valorizar | **Sim, trecho** no cap09 (G) |
| 13 | **"Ver pedido"** no ticket valorizado (abre a compra) | Conferir o que foi pago | Só citar em G |
| 14 | **Lista como relatório**: filtro de período só no modo Lista; aviso "1 ticket aguardando valorização fora deste período" + "ver todos"; "Filtros" (Tipo, Status, Usuário); **"Exportar"** › PDF ou Excel com "Período", "Tipo de Ticket", "Status", "Usuário que criou" (`WeighingTicket.tsx:3704-3719,4023-4040`; `ExportTicketsDialog.tsx:267-347`) | Fechamento do mês, conferência | **Sim, trecho** no cap09 (G) |
| 15 | **Lixeira de rascunhos** de ticket ("Recuperar", "Excluir definitivamente"; só aparece havendo rascunho apagado) (`WeighingTicket.tsx:3949-3958`) | Aba fechada no x por engano | Só citar no cap06, junto do x (H) |
| 16 | **Sem internet**: aviso "Sem internet. Você pode pesar e finalizar normalmente…"; salvar dá "Ticket guardado neste aparelho" e comprovante **PROVISÓRIO**; "Valorizar (precisa de internet)"; editar ticket salvo e anexar foto ficam bloqueados (`WeighingTicketForm.tsx:2733-2768`; `WeighingTicket.tsx:2186-2187,3726-3750,4212-4222`) | Internet caiu com caminhão na balança | **Sim, capítulo curto** (I), com ilustração: gravar offline depende do robô (decisão) |
| 17 | **Item do ticket**: "Editar", "Mesclar pesagens" / "Desmesclar pesagens", "Excluir", ordenar por cabeçalho (Código, Material, Peso) | Mesmo material pesado duas vezes | Só citar: o cap08 já dá a dica do mesclar. Se sobrar tempo, mostrar o menu no cap05 (5 s, sem fala nova) |
| 18 | **Cadastro rápido de material** ("+" no campo Material) e **"Gerenciar motoristas" / "Gerenciar placas"** | Motorista ou material novo no portão | Só citar no cap02 (J, uma frase). O cadastro de material é da T3 |
| 19 | **"Não informado"** como fornecedor e **fixar parceiro** (pino) na janela de busca | Catador avulso; fornecedor de todo dia | Só citar no cap02 (J) |
| 20 | **"Opções avançadas"** › anexar foto (depende do módulo Portal do Cliente) | Foto da carga | Não: módulo 🔒, é da T20 |
| 21 | **Dois operadores no mesmo ticket** ("Assumir este ticket?", "Outro operador está atendendo este ticket.") | Portão e escritório juntos | Não: é opt-in por empresa (`weighing_ticket_draft_collaboration_enabled`, ligado em `CompanySettings.tsx`); fora do mundo da aula |
| 22 | **Restrição "Ver somente os tíquetes de pesagem que criar"** e "Ver somente clientes e fornecedores que cadastrar" (`config/routes.ts`, `USER_RESTRICTIONS`); com ela o campo do parceiro fica "Não informado" e travado | Balanceiro terceirizado | Outra aula: **T2** (Usuários e Permissões). Aqui só uma frase em G |
| 23 | **Trava do peso da balança por usuário** (`useScaleWeightLock`): com ela, o peso não pode ser digitado | Evitar peso digitado à mão | Outra aula: **T5** (balança) e **T2**. A T8 grava com peso digitado: a semente tem de manter a trava desligada para o Rafael |
| 24 | **Cato registra, valoriza, edita e cancela ticket** (`WeighingTicket.tsx:3618-3635`) | Lançar pela conversa | Outra aula: **T21** |
| 25 | Kanban: "Este ticket já virou pedido e não pode voltar." ao arrastar; "Carregar mais" | Raro | Não |

## 3. Proposta

Ordem sugerida dos capítulos: 00, 01, 02, 03, 04, 05, 06, **06b (novo, D)**, 07, 08, 09, **09b (novo, B+C)**,
**09c (novo, I)**, 10. Falas no tom da aula; números por extenso só onde a fala lê.

### A · cap01, trocar a última fala (avulsa)
| Tela | Fala |
| --- | --- |
| Zoom em "Nova Pesagem Avulsa", sem clicar; depois clique em "Tickets padrão". | A pesagem avulsa não vira pedido e não mexe no estoque. Se você cobra pelo serviço, ela já lança o recebimento. A gente faz uma no fim deste tutorial. |

### J · cap02, duas frases a mais
| Tela | Fala |
| --- | --- |
| Na janela "Selecionar Fornecedor", zoom na primeira opção "Não informado" e no pino ao lado de "Cooperativa Recomeço", sem clicar. | Se o fornecedor não quiser se identificar, existe a opção Não informado. E o pino deixa um fornecedor fixo para os próximos tickets. |
| Depois de escolher o motorista, zoom em "Gerenciar motoristas", no fim da lista de sugestões. | Motorista novo? Em Gerenciar motoristas você cadastra ali mesmo, sem sair do ticket. O mesmo vale para a placa. |

### D · cap06b novo · Ticket com valores (vinheta: VALORES)
| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`). "Rascunhos abertos" › aba do Jair ("Auto Peças Vale Forte", "Bateria automotiva"). Zoom em "Valores". | O Jair descarregou. E com a Auto Peças o preço da bateria já está combinado. Então este ticket pode ser feito com valores. |
| Clique em "Com valores": aparece "Tabela de Preços" ao lado de "Fornecedor" e a coluna de valor nos itens. [ZOOM: "Tabela de Preços"] | Mudo a chave para Com valores. Aparece a Tabela de Preços, que já vem com a tabela do fornecedor, e o valor de cada item. |
| No item, "Ações do item" › "Adicionar tara / pesagem avançada": "1ª Pesagem" 5640, "2ª Pesagem" 4180 (bruto "1.460"); "Valor/Kg" 3,40 › "Confirmar". [ZOOM: "Total geral"] | Ponho a segunda pesagem e o preço combinado: três e quarenta o quilo. O total do ticket aparece embaixo. |
| A câmera fica no total. | Atenção: mesmo com valores, o ticket não paga ninguém. Ele só guarda o preço. O dinheiro continua saindo só quando a compra é finalizada. |
| Configurações › "Usabilidade"; zoom em "Permitir forma de pagamento no ticket de pesagem", desligada; volta. | E, se quiser, o balanceiro já deixa a forma de pagamento escolhida no ticket. É só ligar esta opção em Configurações, Usabilidade. |
| De volta ao ticket: "Salvar Ticket de Pesagem" › "Ticket #59 salvo" › "Fechar". | Salvo o ticket do Jair. Ele vai para Aguardando valorização, já com o valor. |

Mundo: bateria a R$ 3,40 para a Auto Peças é o preço personalizado que a T7 já usa (`MUNDO_FICTICIO.md`, linha 99);
2ª pesagem 4.180 kg é número novo (1.460 kg × 3,40 = R$ 4.964,00): **o coordenador confirma**. Muda o fim do cap09 (o
rascunho do Jair deixa de existir: a última fala "o ticket do Jair continua no rascunho" sai) e o que a T9/T10 herdam.
Handlers: `price_tables`, `price_table_items`, `entity_custom_prices`, `finalize_weighing_ticket_v4` com `ticket_number` 59.

### F · cap07, trecho a mais (valorizar em conjunto)
| Tela | Fala |
| --- | --- |
| Antes de "Ações" › "Valorizar": na coluna "Aguardando valorização", marcar "Selecionar" em dois cartões do mesmo fornecedor; aparece a barra com **"Valorizar 2 tickets"**; desmarcar sem clicar. | Uma dica: se o mesmo fornecedor tem mais de um ticket esperando, marque Selecionar em cada um e use Valorizar dois tickets. Vira uma compra só. Precisa ser o mesmo fornecedor e o mesmo tipo. |
| Zoom no "Valor/Kg" 6,20 (fala atual do preço, com um complemento). | O preço vem nesta ordem: o preço especial do fornecedor, se existir; depois a tabela dele; e por último a tabela padrão. |

Mundo: um segundo ticket pendente da Cooperativa Recomeço (ou trocar o fornecedor do #57 para a Cooperativa, com item
e peso, o que também resolve o "#57 com 0 kg" das `propostas_fala.md`).

### E · cap08, trecho a mais (assinaturas e avisos do papel)
| Tela | Fala |
| --- | --- |
| Configurações › "Usabilidade"; liga "Assinaturas no comprovante": aparece "Quem assina". Abre a lista: "Operador e cliente/fornecedor", "Só o cliente/fornecedor", "Só o operador". [ZOOM: a lista] | Quer que o motorista assine o peso? Em Configurações, Usabilidade, ligue Assinaturas no comprovante e escolha quem assina: os dois, só o fornecedor, ou só a empresa. |
| Escolhe "Só o cliente/fornecedor": aviso "Assinaturas do comprovante atualizadas". [ILUSTRAÇÃO: o rodapé do cupom com uma linha só, da largura do papel, e "Cooperativa Recomeço" embaixo.] | Com uma assinatura só, a linha ocupa a largura inteira do papel. No ticket, o lado do operador sai com o nome da empresa. |
| Zoom em "Marca de ticket não valorizado" (ligada) e, mais abaixo, em "Exigir cliente/fornecedor no Ticket de Pesagem" (desligada). | Aqui também ficam duas regras do ticket: tirar do papel o aviso de não valorizado, e exigir o fornecedor para salvar. |

A fala atual "Repara no papel: ticket de pesagem, não valorizado." continua; o zoom passa a pegar também o título novo
"Ticket de pesagem N° #58". Mundo: `companies.show_signatures_on_receipt` e `receipt_signature_mode` (update); o
capítulo seguinte parte com a chave como a aula quiser deixar (sugestão: ligada, "Só o cliente/fornecedor", e avisar a T9).

### G · cap09, trecho a mais (corrigir, apagar, relatório)
| Tela | Fala |
| --- | --- |
| No cartão do #57 (pendente), "Ações": zoom em "Editar" e "Excluir", sem clicar. | Enquanto o ticket espera o preço, dá pra corrigir em Editar ou apagar em Excluir. Depois de valorizado, ele trava: a correção passa a ser no pedido, em Ver pedido. |
| Modo "Lista": zoom no filtro de período no alto e em "Filtros" (fala atual dos três status continua). | Na lista, o período do alto vale para tudo, e os filtros separam por tipo, situação e usuário. |
| "Exportar" › "PDF": janela com "Período", "Tipo de Ticket", "Status", "Usuário que criou"; fecha sem gerar. | E em Exportar sai o relatório dos tickets, em PDF ou Excel, com os filtros que você escolher. |
| A câmera volta ao kanban. | Um detalhe: o dono pode limitar um balanceiro a ver só os tickets que ele mesmo criou. Isso fica em Usuários e Permissões. |

### H · cap06, uma frase a mais
| Tela | Fala |
| --- | --- |
| Depois do zoom no "x" da aba. | E se descartar sem querer, o rascunho vai para a lixeira da tela de tickets, de onde dá pra recuperar. |

Só gravar o zoom se a semente tiver um rascunho apagado (o botão só existe com contagem maior que zero); senão a fala
vai sobre a lista de abas.

### B + C · cap09b novo · Pesagem avulsa com cobrança (vinheta: AVULSA)
| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`). [ILUSTRAÇÃO: um caminhão caçamba de areia, de fora, sobe na balança da Recicla Vale; uma placa "Serviço de pesagem".] | Agora o outro caso: um caminhão de areia, que não é fornecedor nem cliente de sucata, só quer usar a balança. E a Recicla Vale cobra por isso. |
| Aba "Pesagens avulsas" › "Nova Pesagem Avulsa": título "Nova Pesagem Avulsa"; "Modalidade" em "Pesagem avulsa"; "Tipo" mostra "Serviço ao cliente". [ZOOM: a barra de cima] | Em Pesagens avulsas, Nova Pesagem Avulsa. O tipo já vem como serviço ao cliente: aqui a empresa não compra nem vende, ela presta um serviço. |
| "Selecionar cliente": na busca, digita "Areal Boa Vista"; "Nenhum resultado encontrado." e o botão "Cadastrar «Areal Boa Vista»". [ZOOM: o botão] | O dono do caminhão ainda não tem cadastro. Eu busco, o sistema não acha, e oferece cadastrar com o que eu digitei. |
| Clique: "Cadastro Rápido de Cliente" com "Nome" preenchido; preenche "Telefone"; zoom em "Chave PIX"; salva; o cliente já volta escolhido no ticket. | O nome já vem preenchido. Completo o telefone e salvo. Se eu tivesse buscado pelo CPF ou CNPJ, era ele que vinha preenchido. E repara: o cadastro rápido agora tem a chave Pix. Esse atalho vale também no ticket padrão. |
| "Descrição do material": digita "Areia média". "Pesagem avançada": "1ª Pesagem" 23840, "2ª Pesagem" 9120 › "Confirmar" (bruto "14.720"). | Na pesagem avulsa não tem material cadastrado. Eu escrevo o que é: areia média. E peso do mesmo jeito, entrada e saída. |
| "Placa do Veículo": "HBN3F27"; "Tipo de caminhão": "Caçamba"; **"Valor cobrado pela pesagem"**: 60,00. [ZOOM: os dois campos] | A placa, o tipo de caminhão e o valor cobrado pela pesagem: sessenta reais. |
| "Salvar Pesagem Avulsa": abre "Finalizar Pedido" ("Total: R$ 60,00") com "Dinheiro", "Pix/Transferência" e "Saldo do Cliente". [ZOOM: as três formas] | Como tem valor, ao salvar o sistema pergunta como o cliente pagou: dinheiro, Pix, ou saldo do cliente, que é pôr na conta dele. |
| Escolhe "Dinheiro": aparece "Caixa que recebe o dinheiro" com o caixa do Rafael › "CONFIRMAR PAGAMENTO". | Foi em dinheiro. Escolho o caixa que recebe, e confirmo. |
| Aviso "Ticket de pesagem salvo" e a janela "Ticket #60 salvo" com o selo "PESAGEM AVULSA", só "Imprimir comprovante" e "Fechar". | Pronto. Os sessenta reais já entraram no caixa como receita de serviço de pesagem. Sem pedido e sem mexer no estoque. |
| "Imprimir comprovante" › "Térmico". [ILUSTRAÇÃO com o PDF do app: faixa "PESAGEM AVULSA" / "SEM VALOR COMERCIAL", "Tipo de caminhão: Caçamba", "Valor da pesagem: R$ 60,00".] | O comprovante sai marcado como pesagem avulsa, sem valor comercial, com o peso e o valor da pesagem. Repara que não tem botão Valorizar: avulsa nunca vira compra ou venda. |
| De volta à aba "Pesagens avulsas"; "Ações" › "Editar": zoom em "Cobrança já lançada no financeiro. O valor não pode mais ser alterado."; "Voltar". | Atenção: depois de cobrada, o valor fica travado, e a pesagem não pode ser excluída sem antes estornar o recebimento. |
| [ILUSTRAÇÃO: três caminhos saindo do "Valor cobrado": "Dinheiro" › caixa; "Pix" › conta bancária; "Saldo do Cliente" › conta a receber.] | Se fosse no saldo, o cliente ficava devendo e nascia uma conta a receber. E dá pra dividir entre as três formas. Sem valor nenhum, a avulsa é só o comprovante de peso. |

Mundo novo (**nomes e números a confirmar pelo coordenador**, nenhum existe hoje no `MUNDO_FICTICIO.md`): cliente
"Areal Boa Vista" (criado na tela; telefone (12) 9 0000-xxxx), placa "HBN3F27", 23.840 e 9.120 kg, R$ 60,00, ticket #60
(ou #59 se o D não entrar), categoria "Serviço de pesagem". Caixa do Rafael aberto (já é exigência do cap09). Handlers:
`customers` insert (cadastro rápido), `balances` (leitura do saldo do cliente), `cash_registers` (seletor do caixa),
`finalize_weighing_ticket_v4` devolvendo `standalone_charge_status: "charged"`, lista da aba avulsa com
`ticket_kind = standalone`, `weighing_fee` e `vehicle_type`. Efeito nas aulas seguintes: +R$ 60,00 no caixa do Rafael
em 10/11 (T9 e T6 conferem o fechamento) e um cliente a mais (T4).

### I · cap09c novo · Sem internet (vinheta: OFFLINE)
| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: o caminhão na balança, o sinal de internet cortado; na tela, a faixa "Sem internet."] | E se a internet cair com o caminhão em cima da balança? O ticket continua funcionando. |
| Criação de ticket com o aviso "Sem internet. Você pode pesar e finalizar normalmente…". [ZOOM: o aviso] | O sistema avisa, e você pesa e salva normalmente. O ticket fica guardado neste computador. |
| "Salvar Ticket de Pesagem": "Ticket guardado neste aparelho"; janela com "Comprovante provisório (sem número oficial)" e "Valorizar (precisa de internet)". | O comprovante sai como provisório, sem número oficial. Quando a internet volta, o ticket sobe sozinho e ganha o número de verdade. |
| A câmera fica na janela. | Só duas coisas esperam a conexão: valorizar e editar um ticket já salvo. |

Gravação: exige o robô simular queda (o app decide por ping, não por `navigator.onLine`). Se não der para gravar agora,
vira só ilustração com as três falas. Para não sujar o mundo, o ticket offline é descartado na semente seguinte.

## 4. Estimativa

| Bloco | Segundos de fala | Capítulo novo |
|---|---|---|
| A (cap01, troca) | +4 | |
| J (cap02) | +16 | |
| H (cap06) | +6 | |
| D (cap06b) | +50 | sim |
| F (cap07) | +22 | |
| E (cap08) | +30 | |
| G (cap09) | +30 | |
| B + C (cap09b) | +110 | sim |
| I (cap09c) | +25 | sim |
| Recapitulação (cap10, duas frases) | +10 | |
| **Total** | **~300 s (5 min)** | **3** |

Com vinhetas, digitação e ilustrações, a aula vai de ~10 para ~16 a 17 min.

## 5. Depende de decisão
1. **Nomes e números novos** do mundo (Areal Boa Vista, HBN3F27, 23.840/9.120 kg, R$ 60,00, 2ª pesagem do Jair 4.180 kg).
2. **Salvar o ticket do Jair** (D) muda o que a T9/T10 herdam (um ticket pendente a mais em vez de um rascunho).
3. **Os R$ 60,00 no caixa do Rafael** mexem no fechamento do dia 10/11 das outras aulas; alternativa sem efeito no
   caixa: cobrar em "Saldo do Cliente" (aí nasce conta a receber, que a T13 enxerga).
4. **Capítulo offline**: gravar com o robô ou só ilustrar.
5. **Assinaturas**: deixar a chave ligada no mundo depois do cap08 ou devolver ao padrão.
6. Nada aqui foi visto na tela: os textos vêm do código. O primeiro ensaio no 1.60.10 confirma layout e ordem dos campos.
