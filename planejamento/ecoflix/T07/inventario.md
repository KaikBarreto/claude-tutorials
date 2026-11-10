# Inventário · T7 Comprar e vender sucata (EcoSistema 1.59.154)

Código lido: `/home/claude/ecoflix/app-src-1.59.154/` (`APP_VERSION = "1.59.154"`, `src/config/version.ts:16`). Só o que a
aula usa. Caminhos relativos a `src/`. Rótulos entre aspas = texto exato da tela (pt-BR).

## 1. Caminho até a compra e a venda
- Menu lateral **"Financeiro" → "Caixa"** (`config/routes.ts:411-418`). Rotas `/compra` e `/venda`
  (`App.tsx:473-482`; permissões `screen_caixa` + `action_register_purchase` / `action_register_sale`).
- Caixa aberto (`pages/Caixa.tsx:2982-3013`): botões **"Nova Compra"** (azul) e **"Nova Venda"** (verde), ao lado de
  "Nova Despesa" e "Nova Receita". Na aba "Início" do multi-caixa abre antes o seletor de caixa (`:2987-2991`).
- Atalhos (`hooks/useKeyboardShortcuts.tsx:24-25,34`, ligados por padrão): **Shift+C** → `/compra`, **Shift+V** →
  `/venda`, **Ctrl+K** → paleta. Paleta (`components/CommandPalette.tsx:126-129,618,684`): busca "Buscar páginas,
  clientes, fornecedores, materiais, funcionários...", grupo **"Ações Rápidas"**: "Nova Compra", "Nova Venda", "Abrir Caixa".

## 2. Tela Nova Compra (`pages/Purchase.tsx`; desktop `:4748-5320`)
- Topo: link **"Voltar para o caixa"** (`:4288-4291`); título **"Nova Compra"** (`i18n/locales/pt-BR/orders.json`
  `purchaseForm.title`); selo do caixa **"Caixa #N · Você"** (`components/CurrentCashRegisterBadge.tsx:96-110`; sem caixa,
  "Selecione um caixa"); "• Modo Offline" quando sem rede (`:4352`); "Importar XML" (fora da aula).
- **Fornecedor** (`:4754-4787`): botão "Selecionar fornecedor" (ou "Não informado") + "+" (aria "Cadastrar novo
  fornecedor"). **"Tabela de Preços"** (`:4788-4797`, `components/PriceTableSelector.tsx`): só com a preferência
  Múltiplas Tabelas ligada e tabela criada; estrela na tabela padrão; lista "Buscar tabela...".
- Cartão preto **"Pesagem"** (`components/OrderFormInputs.tsx:637-884`): visor LED da balança (`components/
  BalancaDisplays.tsx`, aparece com 1 balança ou mais; etiqueta = nome da balança no EcoTray, padrão "Balança",
  `ecotray/config.py:89,105`); **"Material"** ("Escreva o nome ou código do material", `:540`; "+" "Cadastrar novo
  material"); **"Valor/Kg"** (`:669`); **"Quantidade (Kg)"** + selo **"AO VIVO"** (`:710-716`, só com leitura contínua
  e peso fresco); botão preto **"Pesagem avançada"** (`:780-790`); **"Tara/Imp."** (`:800-821`, a balança não preenche
  sozinha: `continuousActive=false`); **"Estoque Disponível"** (`components/orders/AvailableStockField.tsx:61-102`:
  número = em estoque + pendente offline ± este pedido; linha "Em estoque: X Kg", "Nesta compra: +Y" / "Nesta venda: −Y");
  **"Valor Total do Item"** (`:858`); **"Incluir Item"** (`:865-868`). Enter no peso inclui (compra) ou vai ao preço (venda).
- Botão da balança dentro do campo (`components/InputPesoBalanca.tsx:280-414`): azul quando conectada (tooltip "Peso
  estável: … — Clique para capturar"), âmbar aguardando peso, vermelho desconectada ("Balança desconectada. Clique para ir
  às configurações."). Campo vazio + material escolhido: captura sozinho (`:112-144`); com valor: "Substituir **X** pelo
  peso da balança (**Y** kg)?" "Cancelar" / "Substituir" (`:456-465`). Ponto azul no campo = peso da balança.
  Conexão: EcoTray em `ws://127.0.0.1:8053` (`:65`). Gate: não-celular + módulo `balanca_integration` + "balança ativada"
  (`hooks/useBalancaHabilitada.ts:8-13`).
- Preço ao escolher o material (`OrderFormInputs.tsx:382-453`): preço especial do parceiro → tabela do pedido → preço do
  material. Avisos: **"Preço especial aplicado para {material}"**, **"Preço da tabela aplicado para {material}"**,
  "Carregando preços da tabela…". Tabela padrão não dá aviso (cai no preço do material).
- **"Itens do Pedido (n)"** (`:4895-5224`): colunas "Código", "Material", "Peso Líquido" (mostra o BRUTO quando a coluna
  "Tara/Imp." aparece; ver handoff H1), "Tara/Imp." (só com tara), "Valor/Kg", "Valor Total", "Ações"; "Nenhum item
  adicionado". Ponto azul: "Peso capturado automaticamente da balança via EcoTray" (`:5052-5063`). Linha com pesagem
  avançada abre com a seta: sub-linha "Pesagem avançada" com "1ª pesagem", "2ª pesagem", "Bruto", "Tara", "Impureza",
  "Desconto" e o campo "Desconto (R$):" + "R$/kg efetivo:" (`components/order/WeighingDetailRow.tsx:150-210`,
  `utils/receiptWeightDisplay.ts:107-125`). Células editáveis (preferência `allowEditOrderItems`, padrão ligada).
  Ações: **"Mesclar {n} pesagens deste material"** (`:5164-5175`), "Desmesclar e restaurar {n} pesagens originais"
  (`:5143-5162`), menu "Ações do item": "Editar", **"Adicionar tara / pesagem avançada"**, "Excluir" (`:5176-5194`).
- Rodapé: **"Total da Compra"** + lápis "Editar valor total" → "Calculado: R$ X" e "x" "Limpar valor editado"
  (`components/EditableOrderTotal.tsx:172-185`); "Projeção de Lucro" com olho (só quem vê lucro, `:5240-5254`);
  **"Opções avançadas"**, "Cancelar", **"Finalizar"** (`:5257-5313`). "Adicione pelo menos um item" (`:4135`).
- Toasts de inclusão: "Preencha todos os campos", "A quantidade deve ser maior que zero" (`:3404-3424`).

## 3. Selecionar e cadastrar fornecedor
- **"Selecionar Fornecedor"** (`components/EntitySearchModal.tsx`; chamada `Purchase.tsx:4418-4457`): busca "Buscar por
  nome, apelido, CPF/CNPJ ou telefone..."; "+" de cadastro (`:246-259`); 1ª opção **"Não informado"** (`:291-310`);
  linha com código, nome e apelido; selo roxo "Cliente+Fornecedor"; alfinete "Fixar como padrão"/"Desafixar"; menu ⋮
  "Editar"/"Excluir" (`:444-475`, só com permissão e internet). Indicador âmbar com número (`:72-122`): "Cadastro
  incompleto" + "CPF/CNPJ não informado", "Endereço não informado"/"Endereço incompleto", "Telefone não informado" (some com
  "Não possui telefone", `:65`) + "Use o menu ao lado para completar o cadastro.". Não bloqueia.
- "Não informado": pedido avulso (`Purchase.tsx:4440-4447`); sem saldo (item 6) e fora do histórico do parceiro.
- **"Novo Fornecedor"** (`components/EntityFormDialog.tsx:1191`; o "+" do campo ou do modal): abas "Dados de Contato",
  "Dados Fiscais", "Portal" (`:1213-1224`); "Nome *" ("Nome fantasia"), "Pessoa de Contato ou Apelido", "Telefone"
  ("(00) 00000-0000"), "Não possui telefone", "Mostrar o telefone no comprovante", "E-mail", "Chave PIX" ("Email, CPF,
  telefone ou chave aleatória"), "Tabela de Preços Padrão", "Etiqueta" (`:1231-1358`); "Também é cliente" (`:2264`);
  "Cancelar"/"Salvar" (`:1178-1181`). CPF/CNPJ fica em "Dados Fiscais" ("Tipo de Pessoa", `:1442-1500`).
  Salvar: `INSERT suppliers` → **"Fornecedor cadastrado com sucesso!"**, já selecionado, tabela do pedido = a padrão
  dele (`Purchase.tsx:5626-5667`, `applyDefaultPriceTable` `:977-995`).

## 4. Pesagem avançada (`components/AdvancedWeighingDialog.tsx`)
- **"Pesagem avançada"** · "Registre pesagem dupla, tara, impureza e dados do transporte" (`:382-384`); "Cancelar",
  **"Confirmar"** (já inclui o item, `Purchase.tsx:3342-3401`).
- **"1ª Pesagem"**, **"2ª Pesagem"** (cada uma com botão da balança, sem leitura contínua), **"Peso Bruto (Kg)"** =
  |1ª − 2ª| com "|412 − 96|" embaixo (`:252-257,444-480`); dica "Preencha 1ª e 2ª pesagem para o bruto, informe só a 1ª
  (conta como bruto) ou digite o bruto direto." (`:486`).
- **"Tara (Kg)"** (`:494`); **"Impureza"** com chave "kg" / "%"; em %: "= X Kg (sobre bruto − tara)" (`:508-548,261-269`).
- **"Líquido (Kg)"** = Bruto − Tara − Impureza (`:274,555`); **"Valor/Kg"**; **"Valor estimado"**; **"Desconto (R$)"** e
  **"Valor final"** (um recalcula o outro); "R$/Kg efetivo:" (`:562-617`; `lib/lineDiscount.ts`).
- **"Como exibir no comprovante"**: "Resumido" ("Só o peso líquido cobrado."), "Detalhado" ("Bruto, tara, impureza e
  líquido."), "Completo" ("1ª e 2ª pesagem, bruto, tara, impureza e líquido.") (`:622-657`); "Motorista", "Placa do
  veículo" (`:664-693`, tabelas `drivers`, `vehicles`).
- Erros: "Informe o peso bruto (1ª e 2ª pesagem ou o bruto direto)", "Peso líquido inválido. Tara e impureza não podem
  somar mais que o bruto" (`:321-327`).
- Valor: com a preferência "impureza desconta do valor" (padrão ligada, `hooks/usePaymentPreferences.tsx:47`), paga-se
  o líquido; o estoque sempre entra pelo líquido (`Sale.tsx:2194`, `lib/lineDiscount.ts:13`).
- Item editado: "Item carregado para edição", "Pesagem do item atualizada", "Edição cancelada" (`Purchase.tsx:3746,3793,4026`).

## 5. Mesclar (`Purchase.tsx:3494-3549,5796-5865`)
- **"Mesclar pesagens"**: "Deseja mesclar todas as {n} pesagens de "{material}" em uma única linha?", "Pesagens atuais:",
  "Pesagem 1: X kg (tara: Y)" + "R$ Z/kg", "Total mesclado: … kg (tara: …)" + "…/kg (média)", "Peso líquido: …",
  "Valor total: …"; "Cancelar" / **"Mesclar Todas"** → **"{n} pesagens mescladas com sucesso!"** (soma pesos e taras,
  mantém o valor, preço médio). "Desmesclar pesagens" (`components/order/UnmergeWeighingsDialog.tsx:31-44`).

## 6. Finalizar Pedido (`components/MultiPaymentDialog.tsx`)
- **"Finalizar Pedido"** · "Total: R$ X" (`:1225-1226`); painel **"Resumo do Pedido"** (`:1109-1219`): "Fornecedor:",
  "Saldo atual:", **"Saldo após o pedido:"** + "(Ele te deverá)" / "(Você deverá a ele)" / "(Quitado)" (`:740-769`),
  "Material / Qtd. / Unit. / Total", "Valor total", "Distribuição do pagamento", "Faturamento a prazo".
- Chave **"Múltiplas formas de pagamento"**; rótulo "Forma de pagamento" ou **"Formas de pagamento (máx. 3)"**
  (`:1338-1365`); quadrados **"Dinheiro"**, **"Pix/Transferência"**, **"Saldo do Fornecedor"** / "Saldo do Cliente"
  (`:1370-1392,309`). Sem parceiro, o saldo fica apagado: "Selecione um fornecedor no pedido para pagar com saldo."
  (`:310,915`). Na compra o valor fica editável mesmo com uma forma (`allowOverpay`, `Purchase.tsx:5332`).
- Restante automático: o campo não tocado recebe total − tocados (`:454-505`).
- Dinheiro: "Saldo atual do caixa: R$ X" (`:1549-1559`); acima do caixa: "Acima do dinheiro em caixa, o Caixa ficará
  negativo." (`:877-879`). Pix: lista "Conta Bancária" + "Chave PIX do fornecedor: …" (`:957-980`).
- Saldo: **"Vencimento (opcional)"** (+ "Vencimento atual do saldo: … Deixe em branco para manter; informe uma nova data
  para substituir.") e **"Configurar faturamento (parcelas)"** (`:993-1086`); configurado: "2 parcelas", "1ª em
  25/11/2026 · R$ 2.000,00", "Editar"; "Valor do saldo mudou — reconfigure o faturamento.".
- Bloco "Total": "Faltam: R$ X" / "Excesso: R$ X" (trava o botão), "Deixar no saldo …" (`:1572-1652`); "Arredondar para
  baixo" quando há centavos (`:1656-1688`). Botão **"CONFIRMAR PAGAMENTO"** / "PROCESSANDO..." (`:1088-1097`).
- **"Configurar faturamento"** (`components/InstallmentsConfigDialog.tsx:239-394`): "Parcelar R$ X do saldo", "Condição de
  pagamento" ("Manual (definir parcelas)" + condições cadastradas), "Nº de parcelas" 1·2·3·4·6·12 (1ª na data do pedido,
  as outras +1 mês, `:166-176`), linhas data + valor, "Adicionar parcela", "Soma das parcelas" (verde quando fecha),
  "Total do saldo: R$ X. A última parcela absorve os centavos para fechar a soma.", "Limpar faturamento",
  **"Aplicar faturamento"**.
- Ao confirmar: RPC **`create_purchase_atomic`** (`Purchase.tsx:2659`, com `p_installments`, `p_payment_condition_id`,
  `p_hide_financial_details`) → **"Compra registrada!"** (`:2948`). Sem caixa: "Abra o caixa antes de realizar compras"
  (`:2118`).

## 7. Comprovante
- Sem impressão automática (`autoPrintReceipts` desligada) abre **"Imprimir Comprovante"** · "Deseja imprimir o comprovante
  de compra?" (`components/PrintModal.tsx`; `orders.json printModal`); com impressão direta ligada, chave "Visualizar" /
  "Imprimir"; botões "Não, obrigado" e **"Imprimir direto"** (ou "Visualizar PDF").
- Direto pela térmica via EcoTray: **"Comprovante enviado para impressora"** (`Purchase.tsx:3091`); EcoTray fechado:
  "Impressora EcoTray não conectada — abrindo PDF na janela do navegador…" (`:3117`).
- **"Opções avançadas"** (`components/AdvancedOptionsPopover.tsx:109-189`): "Ajustes usados de vez em quando neste pedido.",
  "Data e hora do pedido" (com permissão), "Gerar nota fiscal" (módulo de notas), **"Comprovante sem valores"** · "Oculta
  preços, totais e formas de pagamento nos comprovantes." · tooltip "O pedido é salvo normalmente com os valores; eles só
  ficam ocultos nos comprovantes e no portal do cliente."; ponto no botão com opção ligada. **Vale só para o pedido atual**
  (o próximo nasce com valores: `Purchase.tsx:570-590,3166-3167`).

## 8. Tela Nova Venda (`pages/Sale.tsx`)
- Igual à compra, com "Cliente" / "Selecionar Cliente", preço de venda do material, título **"Nova Venda"**.
- Coluna **"Lucro"** por item (= total − quantidade × preço de compra do material, `:5355,5501`); embaixo de **"Total da
  Venda"**, **"Lucro estimado"** com olho (verde/vermelho; `:4450-4455,5608-5629`; só com permissão de ver lucro).
- Peso maior que o estoque → **"Estoque insuficiente"** (`components/SaleStockTransferDialog.tsx:458-553`): "Estoque
  insuficiente nesta unidade. Complete a quantidade combinando uma ou mais origens abaixo.", "Faltam **X Kg** de {material}.",
  **"Origem do estoque *"** (lista "Selecione a unidade ou material", grupos "Outras unidades" e **"Esta unidade"**: outros
  materiais com saldo), "Quantidade (Kg)", "Adicionar origem", "Alocado: X de Y Kg", "Quantidade coberta", "Cancelar",
  **"Transferir e Adicionar"** → "Transferência de X Kg de {origem} agendada para a finalização da venda"
  (`Sale.tsx:3786-3791`). Cancelando: **"Cancelar transferência?"** · "Cancelar inserção" / "Inserir mesmo assim" →
  "Item adicionado sem transferência. Estoque pode ficar negativo." (`:6019-6034,3829`). Ao finalizar com estoque negativo:
  "Atenção: estoque ficará negativo após esta venda:" (aviso, não bloqueia, `:2209`). Outras unidades sem rede: "A
  transferência entre unidades precisa de conexão para validar o saldo. Reconecte antes de finalizar esta venda." (`:5729`).
- RPC **`create_sale_with_stock_transfers_atomic`** (com transferência) ou `create_sale_atomic` (`:2512,2591`) →
  **"Venda registrada!"** (`:3238`); "Deseja imprimir o comprovante de venda?".

## 9. Sem internet
- Faixa no topo (`components/OfflineBanner.tsx:157-161`, montada em `components/layout/AppLayout.tsx:396`): **"Sem conexão —
  operações serão salvas localmente até reconectar na internet"**, "Sem conexão — N operação(ões) pendente(s) (…)",
  **"Sincronizando 1/1 operação..."**, **"Operações sincronizadas com sucesso!"**, "Algumas operações não puderam ser
  sincronizadas. Verifique as pendências."; sincroniza sozinha ao voltar a rede.
- Finalizar sem rede: fila local (`lib/offlineQueue.ts:635,697`, números `OFFLINE-C-…` / `OFFLINE-V-…`) → **"Compra salva
  localmente (OFFLINE-C-…). Será sincronizada quando a conexão voltar."** (`Purchase.tsx:5463`); sem comprovante nesse
  caminho (`:5376-5492`). Rotas liberadas offline: `/compra`, `/venda`, `/caixa`… (`config/offlineAllowedRoutes.ts`).
  Balança e impressora são locais (EcoTray).
- Caixa (`pages/Caixa.tsx:3056`, `components/OfflinePendingSyncTabs.tsx`): **"Pendências de Sincronização (OFFLINE)"** + número,
  "Sincronizar agora" (com rede), grupos "Compras"/"Vendas", cartão com o parceiro, "Compra"/"Venda", "Sincronizando" ou
  "Erro", número provisório, "1 item", kg, valor; "Tentar novamente (reenvia com segurança, não duplica)" (só em erro com chave
  de segurança, `:175-183,381-390`), "Remover da fila"; mensagem "Os itens com erro não sincronizam de novo pra não duplicar no
  banco. Remova cada um pela lixeira e refaça a operação normalmente." (`:113-114`).

## 10. Backend a simular
Tabelas: `suppliers` (select/insert), `customers`, `materials`, `price_tables`/itens, preços especiais do parceiro,
`cash_register`, contas bancárias, `log_pesagens` (insert a cada captura, `InputPesoBalanca.tsx:153-169`), `drivers`,
`vehicles`, `stock_movements`. RPCs: `create_purchase_atomic`, `create_sale_with_stock_transfers_atomic`,
`create_sale_atomic`, `get_next_order_number`/`preview_next_order_ref`/`preview_next_order_seq`; rascunhos do pedido
(`useOrderCache`). EcoTray falso: `ws://127.0.0.1:8053` (peso) e impressão direta (`printImageFast`).

## Handoffs (texto ou comportamento para o time; a fala não depende deles)
- H1: com tara na lista, a coluna se chama "Peso Líquido" mas mostra o bruto (`Purchase.tsx:4971,5068-5080`).
- H2: o tooltip do botão da balança mostra o peso com ponto ("Peso estável: 12.400 kg", `InputPesoBalanca.tsx:315`).
- H3: a Central de Ajuda (t7-c03) chama a janela de "Cadastro Rápido de Fornecedor"; na tela é "Novo Fornecedor". E (t7-problemas)
  diz que "Comprovante sem valores" fica gravado de um pedido pro outro; o código zera a cada pedido.
