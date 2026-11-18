# Cobertura 1.60.10 · T22 · Gerencial: matriz e filiais

Auditoria só de leitura (código em `/dev/shm/ecoflix-src`, diff `f37573ea0..5290be4cd`). Caminhos relativos a `src/`
(SQL e edge em `supabase/`). Nada foi editado fora deste arquivo. Varredura do robô da T22 ainda não existe
(`rec/varredura/` vai até t05).

**Resumo:** as telas do Gerencial **não mudaram** entre o 1.59.154 e o 1.60.10. O diff de `pages/Gerencial*.tsx`,
`components/gerencial/*`, `hooks/useCompanyGroup.ts`, `hooks/useGroup*.ts`, `components/settings/SettingsCompanyContent.tsx`,
`pages/Checkout.tsx`, `components/checkout/*` e `supabase/functions/create-group-payment` é vazio, e nenhuma nota de versão
de 1.59.155 a 1.60.10 (`config/version.ts:19-113`) fala do Gerencial. O roteiro atual continua batendo com a tela. O
trabalho desta aula é **cobertura**: o roteiro mostra o caminho feliz de cada tela e deixa de fora quase metade das
funções (preço por unidade, correção de saldo pela matriz, lote e fila de transferências, venda com estoque de outra
unidade, lado da filial na transferência, filtros e modos do estoque).

## 1. Mudou no app (por capítulo do roteiro atual)

Só três pontos, todos por componente compartilhado ou vizinhança. Nenhum pede fala nova.

**cap00 · menu lateral aberto**
- O grupo "Fiscal & Ambiental" ganhou o item **"Relatórios Fiscais"** e "Estoque Fiscal" passou a abrir em
  `/fiscal-ambiental/estoque-fiscal/posicao` (`config/routes.ts:510-511`). O grupo "Gerencial (Filiais)" segue igual
  (`config/routes.ts:552-556`). Só muda o que aparece no menu se ele estiver expandido na regravação.

**cap06 e cap07 · Financeiro Gerencial (a aba "Histórico", que o roteiro não abre)**
- A lista do Histórico é a mesma da T15 (`components/financial-report/RevenueExpenseList.tsx`, +322 linhas no diff) e
  ganhou o filtro **"Conta bancária"** (opção "Todas as contas", `:1082-1088`; no Gerencial o nome da conta vem com a
  empresa quando duas unidades têm conta de mesmo nome, `:232-237` do diff) e o botão **"Selecionar"** / "Cancelar
  seleção" (`:882-890`) para mexer em vários lançamentos manuais de uma vez. A DRE (consolidado, comparativo, regimes)
  não mudou. Entra na lacuna F1 abaixo.

**cap11 · Assinaturas e checkout**
- Telas iguais. `lib/billing/planPricing.ts` mudou só a régua de parcelas da proposta comercial (3 a 6 vezes), sem
  efeito no checkout do grupo. Os valores continuam só na tela.

**Pendências que já existiam e continuam valendo no 1.60.10 (código idêntico):** as quatro propostas de fala do
`propostas_fala.md` (cap07 L1 a L3 e cap09 L6) e os cinco achados (Histórico de Envios lê `materials_count` etc. em
`pages/GerencialConfiguracoes.tsx:361-365`; "Sobrescrever preços existentes"; a setinha do Dashboard; "Lucro Líquido" =
vendas menos compras em `pages/GerencialDashboard.tsx:216`; "(-) Compras (CMV)" do Comparativo em
`pages/GerencialFinanceiro.tsx:1103`).

**Precisão do roteiro contra o código (não é mudança do 1.60, mas a tela desmente a fala):**
- cap02: o título é **"Unidades Ativas (1/11)"**, não "(1)": o grupo nasce com limite de 10 filiais
  (`pages/GerencialConfiguracoes.tsx:258`; `supabase/migrations/20260405140000_group_limits_audit_expiry_select.sql:9`).
- cap11 L5 ("Escolho o Pix, e a cobrança única aparece"): no checkout do grupo a chave **"Cobrança recorrente"** ·
  "Cobra o total do grupo automaticamente todo mês." nasce **ligada** (`pages/Checkout.tsx:1234`;
  `components/checkout/CheckoutLayout.tsx:960-970`), então o Pix que aparece é o Pix recorrente mensal, não uma cobrança
  avulsa. Ver proposta P10.

## 2. Falta cobrir

Legenda da coluna Vale: **sim** = capítulo ou trecho proposto na seção 3; **citar** = uma frase; **não** = fica fora.

### A. Grupo e convite (caps. 02 e 03)

| # | O que é (rótulo exato · arquivo) | Quando o cliente usa | Vale |
|---|---|---|---|
| A1 | Botão **"Como funciona"** → "Como funciona o Gerencial de Filiais": 5 passos, "O que cada aba faz", "Relação Matriz × Filial" (`components/gerencial/GerencialHowItWorksModal.tsx:27-80,140-180`) | Dúvida no meio da configuração | citar (P1) |
| A2 | Código vencido: **"⚠ Código expirado — gere um novo"** em vermelho; botão de girar ("Gerar novo código (válido por 30 dias)") → "Código de convite regenerado! Válido por 30 dias." O código antigo é trocado no banco e deixa de valer (`pages/GerencialConfiguracoes.tsx:238-247`; `hooks/useCompanyGroup.ts:163`; migration `20260405225817…sql`, `regenerate_group_invite_code`) | Filial nova depois de 30 dias; código vazou | sim (P2) |
| A3 | Recusas ao vincular, na filial: "Código de convite inválido"; "Código de convite expirado. Solicite um novo código ao administrador do grupo."; "Sua empresa já está vinculada a um grupo. Saia do grupo atual antes de entrar em outro."; "Você não pode se juntar ao seu próprio grupo"; "Este grupo atingiu o limite máximo de 10 filiais." (migration `20260405225817…sql:113-138`; o aviso sai por `useCompanyGroup.ts:133`) | Código digitado errado, vencido, ou grupo cheio | sim (P2) |
| A4 | Limite de unidades no título "Unidades Ativas (n/11)" | Grupo grande | citar (P2) |
| A5 | "Remover unidade?" → "Remover" → "Empresa removida do grupo" (`useCompanyGroup.ts:147`) | Filial vendida ou fechada | não: o cap09 já mostra a lixeira e explica a volta |
| A6 | Passo a passo "Configure o grupo": cada etapa pendente é clicável e leva à aba (`GerencialSetupChecklist.tsx:167-199`); some com as 5 feitas | Primeira configuração | citar (P7) |
| A7 | Permissões de tela "Gerencial - Dashboard", "Gerencial - Financeiro", "Gerencial - Estoque" (`config/routes.ts:137-139`); Assinaturas e Configurações seguem a do Dashboard (`:555-556`) | Liberar o Gerencial só para o dono e o financeiro | citar no cap00; o passo a passo é da aula de Usuários e Permissões |

### B. Dashboard Gerencial (caps. 04 e 05)

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| B1 | Seletor de unidades com marcação múltipla: "Todas as Unidades", o nome da unidade quando é uma só, "n unidades" (`components/gerencial/BranchUnitSelector.tsx:19-27,87`); o mesmo seletor está no Financeiro e nas quatro abas do Estoque | Olhar só uma filial, ou comparar duas de cinco | sim (P3) |
| B2 | Períodos: "Hoje", "Este mês", "Mês passado", "Este ano", "Todos os tempos", "Personalizado" (`i18n/locales/pt-BR/common.json:3-10`) | Fechamento de trimestre, intervalo solto | citar (P3) |
| B3 | Cartão **"Lucro Líquido"** | Leitura rápida | não até a decisão do risco 1 (o número é vendas menos compras) |
| B4 | Sem movimento: "Nenhum dado financeiro no período selecionado." (`pages/GerencialDashboard.tsx:451`) | Período vazio | não |

### F. Financeiro Gerencial (caps. 06 e 07)

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| F1 | Aba **"Histórico"**: "Receitas", "Despesas", "Compras" com contadores, busca, filtros (o novo "Conta bancária"), "Exportar" (`pages/GerencialFinanceiro.tsx:159-161,1215-1240`) | Achar de qual unidade veio um lançamento | sim, curto (P4); o detalhe da lista é da **T15** |
| F2 | Aba **"Dashboard"**: faixa do resultado, "Despesas por Categoria", "Receitas por Categoria" e os maiores fornecedores, clientes e materiais; o "Ver todos" só funciona com **uma** unidade marcada (`:1247-1275`) | Ver onde o grupo gasta | sim, curto (P4) |
| F3 | **"Exportar"** da DRE (PDF com as unidades escolhidas, `:785-793,636-675`) | Mandar ao contador ou ao sócio | citar (P4) |
| F4 | Linhas que abrem: "Custos adicionais", "Total Impostos", "Total Despesas" por categoria (`:821-950`) | Ver o que compõe a despesa | citar (P4) |
| F5 | **"Patrimônio Operacional Atual"**: "Saldo em Caixa (Dinheiro)", "Saldo Bancário", "Contas a Receber", "Estoque (Projeção de Venda)", "Contas a Pagar", "= Patrimônio Operacional Atual" e o "Exportar Patrimônio" (`:987-1046`) | Quanto o grupo vale hoje | citar (P4); o bloco é explicado na **T15** |
| F6 | Aviso "Há material em estoque sem custo de compra cadastrado…" | já está no cap07 | coberto |

### E. Estoque Gerencial (cap. 08)

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| E1 | Visão Geral, menu ⋯ da linha: **"Corrigir saldo"** → janela "Corrigir saldo" · "Ajuste de entrada ou saída em {material}, numa unidade do grupo.": "Unidade *", "Material *" (quando a célula soma mais de um: "Este saldo soma n materiais desta unidade — qual você quer ajustar?"), "Entrada" / "Saída", "Quantidade *", "Saldo atual" → "Depois do ajuste", "O saldo desta unidade fica negativo depois do ajuste.", "Motivo da correção" ("Ex: inventário conferido no pátio, sobra de produção, quebra..."), "A correção fica no kardex da unidade identificada como ajuste feito pela matriz.", **"Registrar entrada"** / **"Registrar saída"** → "Entrada de … em … · {unidade}" (`GroupAdjustStockDialog.tsx:153-159,233-243,250-465`). Só a matriz vê a coluna "Ações" (`GerencialEstoqueVisaoGeral.tsx:641,685`) | Inventário da filial conferido pela matriz | **sim, capítulo (P6)** |
| E2 | ⋯ **"Transferir entre materiais"** · "Move saldo de {material} para outro material da MESMA unidade.": "Unidade *", origem, "Material de destino *", "Quantidade *", "Transferir"; recusas "Origem e destino não podem ser o mesmo material", "Saldo insuficiente. Disponível: …" (`GroupMaterialTransferDialog.tsx:214-254,289-449`) | Material lançado no cadastro errado na filial | sim (P6) |
| E3 | ⋯ **"Transferir entre unidades"** · "De qual unidade sai o {material}?" → "Continuar" → "Transferência em Lote"; avisos "… ainda não está vinculado ao catálogo do grupo nesta unidade. Ao continuar, o vínculo é criado…" e "Este material não pode ser transferido entre unidades: … Ajuste o catálogo em Gerencial › Configurações › Materiais." (`GroupUnitTransferPicker.tsx:138-146,205-291`) | Atalho da transferência sem sair do estoque | sim (P8) |
| E4 | Cartão de aviso **"n material(is) com saldo divergente entre cadastro e histórico"** · "Os números desta tela vêm do histórico de movimentações. O saldo gravado no cadastro do material não bate com esse histórico — o que existe só no cadastro não está somado acima.", colunas "Material", "Cadastro", "Histórico", "Histórico − Cadastro" (`GerencialEstoqueVisaoGeral.tsx:857-892`) | Número do grupo "faltando" material | sim (P6): é o porquê do "Corrigir saldo" |
| E5 | Tabela unificada: "Total Geral", paginação "Exibindo 1–n de n" · "por página", "Ver menos" nos cartões (`:739,782-796,172`) | Muitos materiais | não |
| E6 | Posição de Estoque: "Filial", "Data e hora (padrão: fim do dia)", **"Ver posição"**, **"Consolidado"** / **"Por unidade"**, cartões "Saldo total", "Valor em estoque", "Projeção de venda", linha que abre por unidade, "Total geral", legenda "Posição consolidada da rede" · "… Valores negativos indicam movimentações lançadas fora da ordem cronológica. Itens sem compra registrada até a data aparecem sem valorização." e "Foto do estoque em {data}. O padrão é o fim do dia (23:59)." (`GerencialEstoquePosicao.tsx:217-313,554-619`) | Estoque do grupo no fim do mês passado, para o balanço | sim (P5) |
| E7 | Histórico de Materiais: botão **"Filtros"** ("Período", "Material", "Limpar filtros"); tipos "Compra", "Venda", "Transferência", "Edição Manual", "Exclusão", "Produção", "Saldo inicial"; coluna "Saldo na Unidade" quando há mais de uma unidade (`GerencialEstoqueHistorico.tsx:57-73,331,358-413`) | Rastrear quem mexeu e em qual unidade | sim (P5) |
| E8 | Relatório de Estoque: filtros "Filial", "Período", "Material", **"Usuários"**; chip **"Ocultar itens zerados"**; **"Exportar Relatório"**; os quatro cartões abrem ("Total Comprado", "Total Vendido", "Lucro", "Margem") com "Preço médio de compra", "Material que mais comprou", "Material mais lucrativo", "Melhor margem", "Pior margem" e a **"Distribuição por forma de pagamento"** ("Dinheiro", "Pix/Transferência", "Saldo", "Em aberto" · "Considera os pedidos do período; não segue o filtro de material."); a linha do material abre por filial (`GerencialEstoqueRelatorio.tsx:466-522,536-760,800-880`; `i18n/locales/pt-BR/materials.json`, bloco `report`) | Saber qual unidade compra mais caro o mesmo material | sim (P5) |
| E9 | Aba **"Transferências"** do Estoque, com o contador de pendentes (`pages/GerencialEstoque.tsx:51-59,118`) | Fila do dia sem ir às Configurações | sim (P8) |

### P. Padronização (cap. 09)

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| P-1 | Catálogo: cadastrar à mão ("Nome do Material" · "Ex: Papelão", "Unidade": kg, un, m, m², m³, l, t, pç) → "Material adicionado ao catálogo"; lixeira → "Material removido do catálogo" (sem confirmação); "Nenhum material novo encontrado no estoque da matriz" ao importar de novo (`GerencialMaterialCatalog.tsx:51,61,101-182`; `hooks/useGroupMaterials.ts:81,98`) | Material que só a filial trabalha | sim, trecho (P7) |
| P-2 | **Tabelas de Preço do Grupo** · "Selecione uma tabela para ver/editar preços e configurar a vinculação com as filiais.": criar ("Nome da tabela..." + "Criar" → "Tabela de preços criada"), abrir a tabela, "Importar da matriz..." ("(Principal)") → "n preço(s) importado(s) da matriz", "Excluir" → "Tabela removida" (sem confirmação), grade "Material" · "Preço Compra (R$)" · "Preço Venda (R$)" com "Salvar" por linha → "Preço atualizado" (`GerencialPriceTables.tsx:227-378`; `hooks/useGroupPriceTables.ts:110-214`) | Ajustar o preço padrão do grupo | **sim, capítulo (P9)** |
| P-3 | **"Vinculação por Unidade"** · "Configure como cada unidade herda os preços desta tabela.": chave "Vinculada" / "Desvinculada" por unidade; "Tipo" ("%" ou "R$ fixo"), "Direção" ("+ (acima)" ou "- (abaixo)"), "Valor", "Salvar" → "Configuração atualizada"; **"Aplicar"** → "n preço(s) aplicado(s) à unidade". A variação vale para a compra **e** para a venda (`GerencialPriceTables.tsx:388-510`; migration `20260315220327…sql:61-88`, `apply_group_prices_to_company`) | Filial longe da usina paga menos no quilo; filial de cidade cara paga mais | **sim, capítulo (P9)** |
| P-4 | Clientes e Fornecedores: abas "Clientes (n)" e "Fornecedores (n)", "Buscar...", contador "n de n disponibilizado(s) para filiais", desmarcar → "Removido das filiais" (`GerencialClientsSuppliers.tsx:113,157-186`) | Fornecedor que é só da matriz | sim, trecho (P7) |
| P-5 | Categorias: "Marque as categorias que ficarão disponíveis para as filiais. Categorias usadas no DRE (Ganhos, Prejuízos, Impostos) são obrigatórias."; abas "Despesas (n)" e "Receitas (n)"; cadeado "Categoria obrigatória — usada no DRE"; desmarcar → "Categoria removida das filiais" (`GerencialCategories.tsx:19-25,116,146-228`) | Categoria que só existe na matriz | sim, trecho (P7) |
| P-6 | Enviar Ativos: "Desmarcar todos" / "Marcar todos"; se nada entrou: "Todos os ativos selecionados já estão configurados nesta filial" (`PushAssetsModal.tsx:110,167`) | Mandar só os fornecedores novos | sim, trecho (P7) |
| P-7 | "Histórico de Envios" · "Últimos 20 envios de ativos para filiais", selo "sobrescreveu preços" (`pages/GerencialConfiguracoes.tsx:335-392`) | Conferir quando o padrão foi enviado | não, até corrigirem o achado 1 (a linha mostra "Nenhum ativo") |

### T. Transferências (cap. 10)

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| T1 | Lote com vários materiais: "n de m selecionados", **"Selecionar todos com saldo"**, "Buscar material...", "sem vínculo" (linha apagada), quantidade por material com "Estoque: …", quadros **"Origem"** e **"Destino"** (quanto tem e quanto fica), "Saldo insuficiente na origem: disponível …" e o aviso "Ajuste as quantidades: há material com saldo insuficiente na origem" (`GerencialTransferForm.tsx:290,556-674`) | Caminhão com três materiais | **sim, capítulo (P8)** |
| T2 | Sem aprovação: botão "Transferir" e o estoque move na hora → "{qtd} de {material} transferidos para {destino}" (`:343-349,380`) | Grupo pequeno, dono único | sim (P8, uma frase) |
| T3 | Pendente → **"Cancelar"** → "Transferência cancelada"; selo "Cancelada" (`GerencialTransfers.tsx:150-152,273-280`; `hooks/useGroupTransfers.ts:183`) | Carga que não saiu | sim (P8) |
| T4 | **"Executar todas (n)"** → "Executar n transferência(s)?" · "… Todas as pendentes serão executadas agora; as que não tiverem saldo na origem serão listadas depois com o motivo." → "n transferências executadas" ou "n executada(s), n falhou(ram)" · "Veja o motivo de cada falha no resumo acima da lista" (`GerencialTransfers.tsx:127-133,171-232,312-318`) | Fila acumulada | sim (P8) |
| T5 | Lado da filial: no Estoque da filial, marca os materiais → barra **"Transferir Estoque"** → "Transferência em Lote" · "A transferência será enviada para a Matriz e movimentará o estoque quando ela confirmar." → "Solicitação criada — aguardando aprovação" · "Aguardando execução da Matriz — o estoque será movido quando ela confirmar" (`pages/Materiais.tsx:3655-3662`; `components/BulkTransferDialog.tsx:312-317,407-463`). A T10 mandou esse caso para cá (`T10/cobertura_160.md:93`) | A filial precisa de material ou quer mandar o excedente | **sim (P8)** |
| T6 | **"Usar estoque de outras unidades na venda"** · "Quando ativo, a venda pode puxar material de outra unidade do grupo se faltar estoque. Configure unidade por unidade.", uma chave por unidade (a matriz mexe em todas; a filial só na dela) (`pages/GerencialConfiguracoes.tsx:423-470`). Na venda: "Estoque insuficiente" → "Origem do estoque *" → grupo **"Outras unidades"** → "Transferir e Adicionar"; mensagens "Buscando saldo nas filiais...", "Nenhuma outra unidade possui saldo deste material.", "A consulta e a transferência entre unidades precisam de conexão…" e, com a aprovação ligada, **"O grupo exige aprovação de transferências. Para concluir a venda agora, use estoque desta unidade ou desative a aprovação no Gerencial."** (`components/SaleStockTransferDialog.tsx:181-184,462-576`; `pages/Sale.tsx:6446`). A T07 (cap14) só mostra "Esta unidade" | Cliente no balcão da matriz e o material está na filial | **sim, capítulo (P8b)** |
| T7 | "Nenhuma transferência registrada."; erro "Nenhuma transferência pôde ser criada. Verifique os vínculos dos materiais." | Casos de borda | não |

### S. Assinaturas (cap. 11)

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| S1 | **"Gerenciar"** em cada unidade: a matriz abre o montador de plano daquela unidade e confirma em "Confirmar mudança · {unidade}" · "Plano … · Mensal/Anual" · "Valor estimado — o valor exato é calculado no servidor ao confirmar." (`components/gerencial/GerencialAssinaturas.tsx:284-345,523-598`; `lib/billing/subscriptionChange.ts:108`). Recusa: "Você não tem permissão para gerenciar a assinatura desta unidade" | Subir o plano da filial sem pedir o login dela | sim, trecho sem valores (P10) |
| S2 | Chave **"Cobrança recorrente"** (ligada ao abrir); "CPF ou CNPJ da matriz *" · "Necessário para gerar a cobrança consolidada" quando a matriz não tem documento gravado (`CheckoutLayout.tsx:941-970`) | Pagar todo mês sem lembrar, ou só este mês | sim (P10) |
| S3 | Ciclos diferentes: "As unidades deste grupo têm ciclos de cobrança diferentes (…). Não existe um valor único a cobrar: alinhe todas as unidades no mesmo ciclo (mensal ou anual) e gere o pagamento do grupo de novo." (`supabase/functions/create-group-payment/index.ts:269-272`) | Matriz no anual e filial no mensal | sim, como dica (P10) |
| S4 | "Cartão de Crédito" e "Boleto" no pagamento do grupo; preço promocional "de … por" na linha da unidade (`GerencialAssinaturas.tsx:509-520`) | Outra forma de pagar | citar (P10); valores sem fala |

**Contagem:** 3 mudanças do app (nenhuma com fala) + 2 correções de precisão; **43 lacunas** (A 7, B 4, F 5, E 9, P 7,
T 7, S 4, sem contar a F6, já coberta), das quais 28 "sim", 9 "citar" e 6 "não".

## 3. Proposta

Tom do roteiro atual. Números do mundo fictício. Cada proposta diz onde entra. Capítulo novo = vinheta nova.

### P1 · trecho no cap02, depois da linha das abas (A1)

| Tela | Fala |
| --- | --- |
| Clique em "Como funciona": janela "Como funciona o Gerencial de Filiais"; a câmera desce pelos cinco passos até "Relação Matriz × Filial" ("Configura e distribui" / "Recebem e operam"); fecha. | Se bater dúvida no caminho, o botão Como funciona abre um resumo dos cinco passos, do convite até os resultados. |

### P2 · capítulo novo, depois do cap03 · "Quando o código não entra" (vinheta: FILIAL) (A2, A3, A4)

Semente própria `codigo-vencido`: igual à `apos-cap02`, com `invite_code_expires_at` em 09/11/2026 e a filial sem vínculo.
Não altera a história: o cap04 continua partindo de `apos-cap03`.

| Tela | Fala |
| --- | --- |
| Como Sandra Pires, em Configurações › "Empresa" › cartão "Filial", com "É Filial" ligado; cola "GRP-7C4E9A" e clica em "Vincular": aviso "Código de convite expirado. Solicite um novo código ao administrador do grupo.". [BACKEND: `join_group_by_invite_code` devolve o erro da migration] | E se o código não entrar? O caso mais comum é esse: o código passou dos trinta dias, e o sistema avisa que ele expirou. |
| Corte para a matriz, Configurações do grupo › "Unidades": no cartão "Código de Convite", a linha vermelha "⚠ Código expirado — gere um novo". [ZOOM: a linha vermelha] | Na matriz, o aviso também aparece em vermelho, embaixo do código. |
| Clique no botão de girar ("Gerar novo código (válido por 30 dias)"): aviso "Código de convite regenerado! Válido por 30 dias."; o código vira "GRP-2B91D5" e "Válido até 10/12/2026". [BACKEND: `regenerate_group_invite_code`] | Um clique nesse botão gera um código novo, com mais trinta dias. O antigo deixa de valer, então mande o novo pra filial. |
| [ILUSTRAÇÃO: três bilhetes de recusa lado a lado: "código errado", "já está em outro grupo", "grupo cheio"; na palavra "letra", uma lupa passa pelo código; na palavra "sair", uma seta tira a empresa de um contorno e leva ao outro] | As outras recusas são três. Código inválido: confira letra por letra. Empresa que já está em outro grupo: ela precisa sair de lá antes. E grupo cheio: cada grupo aceita até dez filiais. |
| Zoom no título "Unidades Ativas (1/11)". | Esse limite aparece aqui, do lado da contagem de unidades. |

### P3 · trecho no cap04, depois da linha do período (B1, B2)

| Tela | Fala |
| --- | --- |
| Abre o período: "Hoje", "Este mês", "Mês passado", "Este ano", "Todos os tempos", "Personalizado"; volta a "Mês passado". | No período, além dos atalhos, o Personalizado aceita qualquer intervalo de datas. |
| Abre o seletor "Todas as Unidades" e marca só "Filial Pindamonhangaba": o botão passa a mostrar o nome da filial; "Receita Total" R$ 72.000,00 e "Despesa Total" R$ 71.000,00; volta para "Todas as Unidades". | E o seletor de unidades aceita marcar uma, duas ou todas. Marcando só a filial, os cartões e os gráficos passam a mostrar só ela. Esse mesmo seletor aparece no Financeiro e no Estoque. |

### P4 · capítulo novo, depois do cap07 · "Além da DRE" (vinheta: FINANCEIRO) (F1 a F5)

| Tela | Fala |
| --- | --- |
| Financeiro, "Mês passado", "Regime de Competência"; clique na linha "Total Despesas": abrem as categorias; fecha. | Ainda no Financeiro, três coisas rápidas. Na DRE, as linhas de custos, impostos e despesas abrem, e mostram do que o total é feito. |
| Zoom no botão "Exportar"; depois a câmera desce e clica na faixa "Patrimônio Operacional Atual": "Saldo em Caixa (Dinheiro)", "Saldo Bancário", "Contas a Receber", "Estoque (Projeção de Venda)" e "Contas a Pagar". | O Exportar gera o PDF da DRE com as unidades escolhidas. E embaixo, o Patrimônio Operacional soma o caixa, o banco, o que tem a receber, o estoque e o que tem a pagar, do grupo inteiro. |
| Clique na aba "Dashboard": a faixa do resultado, "Despesas por Categoria" e "Receitas por Categoria". | A aba Dashboard mostra onde o grupo gasta e de onde vem a receita, por categoria. |
| Clique na aba "Histórico": "Receitas", "Despesas" e "Compras"; abre os filtros e, em "Conta bancária", escolhe a conta da filial. [BACKEND: `get_group_order_history_lines` e as linhas de despesa e receita das duas unidades, com `bankAccountName`] | E a aba Histórico lista os lançamentos das unidades, um por um. Dá pra filtrar por categoria e até pela conta bancária de onde o dinheiro saiu. Essas telas funcionam como no tutorial Relatório Financeiro e DRE. |

### P5 · trechos no cap08, trocando as três últimas linhas (E6, E7, E8)

| Tela | Fala |
| --- | --- |
| Aba "Posição de Estoque": em "Data e hora (padrão: fim do dia)", escolhe 31/10/2026 e clica em "Ver posição": "Foto do estoque em 31/10/2026 23:59"; cartões "Saldo total", "Valor em estoque" e "Projeção de venda". | A Posição de Estoque é uma foto do estoque numa data. Escolho trinta e um de outubro e clico em Ver posição: o saldo, o custo médio e o valor de cada material no fim daquele dia. |
| Clique na linha "Alumínio latinha": abrem as duas unidades; depois clique em "Por unidade". | Clicando no material, ele abre unidade por unidade. E o botão Por unidade muda a tabela inteira pra esse jeito. |
| Aba "Histórico de Materiais"; clique em "Filtros": "Período" e "Material"; escolhe "Alumínio latinha": ficam as linhas "Compra", "Venda" e "Transferência", com a coluna "Filial". | No Histórico de Materiais, o botão Filtros escolhe o período e o material. Cada linha mostra o tipo do movimento, a unidade e quem fez. |
| Aba "Relatório de Estoque"; clique no cartão "Total Comprado": abrem "Preço médio de compra", "Material que mais comprou" e a "Distribuição por forma de pagamento". | No Relatório de Estoque, os cartões de cima abrem. O Total Comprado mostra o preço médio e quanto saiu em dinheiro, em Pix, pelo saldo do parceiro e o que ficou em aberto. |
| Clique na linha "Alumínio latinha": abrem as duas unidades com "Preço Médio Compra" de cada; zoom nas duas. | E a linha do material abre por unidade. É aqui que você descobre se uma unidade está pagando mais caro que a outra no mesmo material. |
| A câmera passa pelos filtros "Usuários" e "Ocultar itens zerados" e para em "Exportar Relatório". | Dá pra filtrar por usuário, esconder o que não teve movimento e exportar o relatório. |

### P6 · capítulo novo, depois do cap08 · "Corrigir o estoque de uma unidade" (vinheta: ESTOQUE) (E1, E2, E4)

| Tela | Fala |
| --- | --- |
| Estoque › "Visão Geral" › "Tabela Unificada de Materiais": na linha "Papelão", clique no ⋯ da coluna "Ações": "Corrigir saldo", "Transferir entre unidades", "Transferir entre materiais". | Agora um caso do dia a dia. A filial contou o papelão no pátio e achou trinta quilos a menos que o sistema. A matriz resolve daqui, no menu de ações da linha. |
| Clique em "Corrigir saldo": janela "Corrigir saldo" · "Ajuste de entrada ou saída em Papelão, numa unidade do grupo."; em "Unidade *", "Filial Pindamonhangaba". | Corrigir saldo. Escolho a unidade, a filial. |
| Clique em "Saída"; em "Quantidade *", 30; o quadro mostra "Saldo atual" 420 kg e "Depois do ajuste" 390 kg. [ZOOM: o antes e o depois] | É uma saída de trinta quilos. A janela mostra o saldo de agora e como ele fica depois. |
| Em "Motivo da correção", digita "Inventário conferido no pátio"; zoom em "A correção fica no kardex da unidade identificada como ajuste feito pela matriz.". | Escrevo o motivo. E repara: a correção fica no histórico da filial, marcada como ajuste feito pela matriz. Ninguém fica sem saber. |
| Clique em "Registrar saída": aviso "Saída de 30 kg de Papelão · Filial Pindamonhangaba"; a célula da filial vira 390 kg. [BACKEND: RPC `adjust_material_stock_atomic` na empresa da filial] | Registrar saída. Pronto, o estoque da filial está certo. |
| De novo no ⋯, clique em "Transferir entre materiais": "Move saldo de Papelão para outro material da MESMA unidade."; a câmera passa por "Unidade *", "Material de destino *" e "Quantidade *"; "Cancelar". | No mesmo menu, o Transferir entre materiais passa saldo de um material pra outro dentro da mesma unidade. Serve quando a filial lançou a compra no material errado. |
| [ILUSTRAÇÃO: cadastro × histórico: duas colunas de um mesmo material, "o que o cadastro diz" e "o que o histórico soma", com alturas diferentes; na palavra "aviso", um cartão amarelo aparece embaixo da tabela com a diferença; na palavra "sua", uma prancheta de conferência] | Uma dica: essa tela soma as movimentações de cada unidade. Se um material tiver saldo no cadastro sem movimentação que explique, aparece um aviso embaixo, com a diferença material por material. O sistema não mexe sozinho: a conferência é sua. |

### P7 · trechos no cap09 (A6, P-1, P-4, P-5, P-6)

| Onde | Tela | Fala |
| --- | --- | --- |
| depois de "Importar do Estoque da Matriz" | Em "Nome do Material", digita "Sucata eletrônica"; "Unidade" kg; clique no "+": aviso "Material adicionado ao catálogo"; a linha aparece com "Sem vínculos". | Material que a matriz não trabalha também entra: é só dar o nome e a unidade. Ele aparece sem vínculos até alguma unidade usar. |
| depois de marcar a Fundição | Clique na aba "Fornecedores (n)"; busca "Coop"; marca "Cooperativa Recomeço"; a câmera mostra "n de n disponibilizado(s) para filiais". | Os fornecedores ficam na outra aba, com busca. Marcou, está disponível. Desmarcou, sai da lista das filiais. |
| na linha das categorias | Abas "Despesas (n)" e "Receitas (n)"; passa o cursor no cadeado de "Impostos": "Categoria obrigatória — usada no DRE". | As categorias vêm todas marcadas, e dá pra desmarcar as que são só da matriz. As de cadeado vão sempre, porque a DRE precisa delas. |
| na janela do Enviar Ativos | Clique em "Desmarcar todos" e marca só "Fornecedores". (volta a marcar todos para o envio da história) | E não precisa mandar tudo sempre. Depois, quando entrar um fornecedor novo, você desmarca o resto e envia só os fornecedores. |
| na volta à aba "Unidades" | O passo a passo "Configure o grupo" com "4 de 5 etapas concluídas"; cursor numa etapa pendente. | O passo a passo lá de cima vai marcando cada etapa, e some quando o grupo está todo configurado. |

A "Cooperativa Recomeço" é a fornecedora de latinha e PET do mundo; a semente precisa tê-la como fornecedora da matriz.

### P9 · capítulo novo, depois do cap09 · "Preço diferente por unidade" (vinheta: PADRONIZAÇÃO) (P-2, P-3)

| Tela | Fala |
| --- | --- |
| Configurações › "Tabelas de Preço": "Tabelas de Preço do Grupo" · "Selecione uma tabela para ver/editar preços e configurar a vinculação com as filiais."; clique na tabela principal: abre a grade "Material", "Preço Compra (R$)", "Preço Venda (R$)". | O padrão do grupo inclui o preço. Abrindo uma tabela, aparecem os materiais do catálogo com o preço de compra e o de venda. |
| Na linha "Alumínio latinha", troca a compra de 6,20 para 6,30 e clica em "Salvar": aviso "Preço atualizado". [ZOOM: a linha] | Dá pra ajustar aqui mesmo. Subo a compra da latinha pra seis e trinta e salvo. |
| A câmera desce até "Vinculação por Unidade" · "Configure como cada unidade herda os preços desta tabela."; na "Filial Pindamonhangaba", liga a chave: "Vinculada". | Embaixo fica a Vinculação por Unidade. É ela que diz como cada unidade recebe esses preços. Ligo a filial. |
| Em "Tipo", "%"; em "Direção", "- (abaixo)"; em "Valor", 5; clique em "Salvar": aviso "Configuração atualizada". [ZOOM: os três campos] | A filial fica mais longe do comprador e tem frete, então ela trabalha cinco por cento abaixo da tabela. Tipo, porcentagem. Direção, abaixo. Valor, cinco. Salvar. |
| Clique em "Aplicar": aviso "15 preço(s) aplicado(s) à unidade". [BACKEND: RPC `apply_group_prices_to_company` grava a tabela principal da filial com 5 % a menos] | E o Aplicar grava os preços na filial, já com o desconto. |
| [ILUSTRAÇÃO: a mesma tabela, duas réguas: a tabela do grupo no meio; à esquerda a matriz recebe o preço cheio; à direita a filial recebe o mesmo preço com uma etiqueta "5 % abaixo"; na palavra "dois", a etiqueta cai na compra e na venda] | Uma dica: essa variação vale para os dois preços, o de compra e o de venda. Se a diferença for em reais por quilo, troque o tipo pra valor fixo. |
| Zoom em "Importar da matriz..." e no botão vermelho "Excluir", sem clicar. | Nessa barra você também puxa os preços de uma tabela da matriz ou exclui a tabela. O Excluir não pede confirmação, então cuidado com o clique. |

Decisão embutida: o exemplo altera o preço da latinha (6,20 → 6,30) e os preços da filial. Para não mexer no mundo das
outras aulas, a semente de saída deste capítulo não segue adiante (o cap10 parte de `apos-cap09`).

### P8 · capítulo novo, depois do cap10 · "Lote, fila e o pedido da filial" (vinheta: TRANSFERÊNCIAS) (T1 a T5, E3, E9)

Parte de `apos-cap10` (aprovação ligada, a transferência da latinha concluída).

| Tela | Fala |
| --- | --- |
| Como Sandra Pires, no "Estoque" da filial: marca "Papelão" e "Plástico PET"; na barra de baixo, clique em "Transferir Estoque": janela "Transferência em Lote" com o aviso "A transferência será enviada para a Matriz e movimentará o estoque quando ela confirmar.". | A filial também pode pedir. No estoque dela, a Sandra marca os materiais e clica em Transferir Estoque. |
| Destino "Recicla Vale Metais"; quantidades 300 kg e 150 kg; os quadros "Origem" e "Destino" mostram quanto tem e quanto fica; clique em "Enviar 2 Transferência(s)" (`components/BulkTransferDialog.tsx:570-571`): aviso "2 solicitações criadas — aguardando aprovação" · "Aguardando execução da Matriz — o estoque será movido quando ela confirmar". [BACKEND: RPC `create_group_transfer_as_member` devolve `pending`] | Escolhe o destino e as quantidades. A tela mostra quanto tem em cada unidade e quanto vai ficar. O pedido segue pra matriz, e o estoque ainda não se move. |
| De volta à matriz: "Gerencial (Filiais)" → "Estoque": a aba "Transferências" com o contador 2; clique nela. [ZOOM: o contador] | Na matriz, o Estoque Gerencial tem uma aba Transferências, com o número de pedidos esperando. |
| Clique em "Nova": em "Origem", "Recicla Vale Metais"; em "Destino", "Filial Pindamonhangaba"; clique em "Selecionar todos com saldo" e depois desmarca até ficar só "Ferro misto"; em "Quantidade", digita mais do que o estoque: "Saldo insuficiente na origem: disponível …". | Em Nova, a matriz monta um lote com vários materiais de uma vez. O Selecionar todos com saldo marca tudo que a origem tem. Se a quantidade passar do estoque, a linha avisa e o sistema não deixa seguir. |
| Corrige para 500 kg; clique em "Solicitar 1 transferência"; a lista fica com três pendentes. | Corrijo e solicito. Agora são três na fila. |
| Na linha do "Plástico PET", clique em "Cancelar": aviso "Transferência cancelada"; selo "Cancelada". | Uma delas não vai mais sair: Cancelar. Ela fica na lista, marcada como cancelada. |
| Clique em "Executar todas (2)": "Executar 2 transferência(s)?" · "… as que não tiverem saldo na origem serão listadas depois com o motivo."; "Confirmar e Executar": aviso "2 transferências executadas". [BACKEND: RPC em lote de execução] | E as outras duas eu executo juntas, no Executar todas. Se alguma não tiver saldo na origem, as demais seguem, e a tela lista qual falhou e por quê. |
| Estoque › "Visão Geral": no ⋯ da linha "Inox", "Transferir entre unidades": janela "Transferir entre unidades" · "De qual unidade sai o Inox?"; "Cancelar". | Tem também um atalho na Visão Geral: no menu da linha, Transferir entre unidades já abre a transferência com o material escolhido. |
| [ILUSTRAÇÃO: com e sem aprovação: à esquerda, chave ligada, o fardo para numa cancela "pendente" até alguém liberar; à direita, chave desligada, o fardo passa direto] | Uma dica: com o Exigir aprovação desligado, não existe fila. A transferência feita pela matriz move o estoque na hora. |

### P8b · capítulo novo, logo depois · "Vender com o estoque da outra unidade" (vinheta: TRANSFERÊNCIAS) (T6)

Semente própria `venda-outra-unidade`: `apos-cap10` com `require_transfer_approval` desligado, para a venda puxar o
estoque da filial (com a aprovação ligada, a janela só mostra a mensagem de bloqueio).

| Tela | Fala |
| --- | --- |
| Configurações do grupo › "Transferências": cartão "Usar estoque de outras unidades na venda" · "Quando ativo, a venda pode puxar material de outra unidade do grupo se faltar estoque. Configure unidade por unidade."; liga a chave de "Recicla Vale Metais" ("Matriz"). | Último recurso das transferências. Nessa mesma aba fica o Usar estoque de outras unidades na venda, com uma chave por unidade. Ligo na matriz. |
| "Vendas" na matriz: cliente "Serra Fina Alumínio Reciclagem", material "Alumínio perfil" com mais quilos que o estoque; "Incluir Item": janela "Estoque insuficiente" · "Estoque insuficiente nesta unidade. Complete a quantidade combinando uma ou mais origens abaixo." · "Faltam 200 kg de Alumínio perfil.". | Agora, numa venda da matriz, faltam duzentos quilos de alumínio perfil. Em vez de travar, a janela pergunta de onde vem o resto. |
| Em "Origem do estoque *", abre a lista: o grupo "Outras unidades" com "Filial Pindamonhangaba — Alumínio perfil" e o saldo; escolhe; quantidade 200; "Quantidade coberta". [ZOOM: o grupo "Outras unidades"] [BACKEND: RPC `get_group_material_stock`] | Na lista aparece a filial, com o saldo que ela tem. Escolho, e a quantidade fica coberta. |
| Clique em "Transferir e Adicionar": o item entra na venda. | Transferir e Adicionar. O sistema transfere da filial pra matriz e põe o item na venda. |
| [ILUSTRAÇÃO: a venda e a cancela: a mesma cancela "pendente" da ilustração anterior fechada na frente do balcão de venda; na palavra "escolha", duas placas: "aprovação ligada" e "venda puxa da filial"] | Uma dica importante: isso só funciona com o Exigir aprovação desligado. Com a aprovação ligada, a venda avisa que o grupo exige aprovação e só deixa usar o estoque da própria unidade. É uma escolha do grupo: ou o controle da aprovação, ou a agilidade na venda. |

### P10 · trechos no cap11 (S1 a S4) e correção da linha do Pix

| Onde | Tela | Fala |
| --- | --- | --- |
| depois da primeira linha | Zoom no botão "Gerenciar" da linha da filial (sem abrir, para não mostrar valores). | O Gerenciar de cada linha deixa a matriz mudar o plano daquela unidade, sem precisar do login dela. |
| antes de escolher o Pix | Zoom na chave "Cobrança recorrente" · "Cobra o total do grupo automaticamente todo mês.", ligada. | Repara na Cobrança recorrente, que já vem ligada: o total do grupo é cobrado sozinho todo mês. Se quiser pagar só este mês, desligue antes de escolher a forma de pagamento. |
| **troca** a fala "Escolho o Pix, e a cobrança única aparece." | (mesma tela) | Escolho o Pix, e o QR Code do grupo aparece. Também dá pra pagar no cartão ou no boleto. |
| depois do "Pagamento Confirmado!" | [ILUSTRAÇÃO: dois calendários, "mensal" e "anual", que não se encaixam numa fatura só; na palavra "mesmo", os dois viram "mensal" e a fatura fecha] | Uma dica: pra pagar junto, todas as unidades precisam estar no mesmo ciclo, mensal ou anual. Se uma for anual e a outra mensal, o sistema avisa e não gera a fatura. Acerte o ciclo no Gerenciar e tente de novo. |

### cap00 e cap12 (resumo)

- cap00, depois da linha do módulo, uma frase (A7): "E quem enxerga o Gerencial na matriz é você quem decide, nas
  permissões de cada usuário." Tela: a mesma.
- cap12: duas linhas novas de montagem: "Corrigiu o estoque da filial e deu a ela um preço cinco por cento abaixo da
  tabela." e "Executou a fila de transferências e vendeu com o estoque da outra unidade."

### O que o mundo fictício precisa ter para gravar

- **Sementes novas:** `codigo-vencido` (P2), `venda-outra-unidade` (P8b); o P9 parte de `apos-cap09` e não deixa
  semente. O P6 e o P8 partem de `apos-cap03` e `apos-cap10`.
- **Dados:** papelão da filial com 420 kg (P6); papelão, plástico PET e alumínio perfil na filial e ferro misto e inox
  na matriz com saldo para o lote (P8, P8b); uma conta bancária na filial com lançamentos em outubro (P4); compras de
  latinha em outubro nas duas unidades com preço médio diferente (P5); posição de 31/10 das duas unidades (P5); um
  fornecedor comum às duas (P7); "Sucata eletrônica" só nesta aula (P7); segundo código do grupo "GRP-2B91D5" (só
  0-9 e A-F, como a função do app gera); um material da filial com saldo de cadastro sem movimentação se o aviso de
  divergência for mostrado na tela em vez de só na ilustração (P6).
- **Handlers RPC a ter no backend falso (além dos do plano):** `regenerate_group_invite_code`; os erros de
  `join_group_by_invite_code`; `adjust_material_stock_atomic` na empresa da filial; a RPC da transferência entre
  materiais usada por `GroupMaterialTransferDialog`; `get_group_stock_balance_at_date`; as movimentações do grupo do
  Histórico de Materiais com filtro de material; a distribuição por forma de pagamento do grupo
  (`hooks/useGroupOrdersPaymentDistribution.ts`); `apply_group_prices_to_company` e as tabelas `group_price_table_items`
  e de vínculo por unidade; `toggle_group_category_sharing`; `create_group_transfer_as_member`; a execução em lote e o
  cancelamento (`hooks/useGroupTransfers.ts:155-183`); `link_own_material_to_group_catalog` e `get_group_material_stock`
  (venda); `get_group_order_history_lines`, `get_group_financial_categories`, `get_group_patrimony_summary` com dados.
- **Outro usuário:** Sandra Pires no começo do P2 e do P8 (como no cap03).
- **Acerto no `MUNDO_FICTICIO.md`** (linhas 158-162): ali a latinha da matriz está com 4.300 kg e outubro com outros
  números; o `plano.md` e o roteiro usam 640 kg e os números da T15. Alinhar antes de gerar as sementes novas.

## 4. Estimativa

| Proposta | Tipo | Palavras | Fala (2,6 palavras/s) |
|---|---|---|---|
| P1 Como funciona | trecho cap02 | 20 | 8 s |
| P2 Quando o código não entra | **capítulo novo** | 102 | 39 s |
| P3 Período e unidades | trecho cap04 | 46 | 18 s |
| P4 Além da DRE | **capítulo novo** | 114 | 44 s |
| P5 Posição, histórico e relatório | troca 3 linhas do cap08 | 101 | 39 s (líquido, já descontadas as 3 linhas que saem) |
| P6 Corrigir o estoque de uma unidade | **capítulo novo** | 157 | 60 s |
| P7 Padronização | trechos cap09 | 106 | 41 s |
| P9 Preço diferente por unidade | **capítulo novo** | 153 | 59 s |
| P8 Lote, fila e o pedido da filial | **capítulo novo** | 195 | 75 s |
| P8b Vender com o estoque da outra unidade | **capítulo novo** | 127 | 49 s |
| P10 Assinaturas | trechos cap11 | 101 | 39 s |
| cap00 e cap12 | 3 frases | 46 | 18 s |
| **Total** | **6 capítulos novos** | **1268** | **488 s (cerca de 8,1 min de fala a mais)** |

A aula passa de 13 para 19 capítulos e de cerca de 9 para cerca de 17 min de voz. Ilustrações novas: 6 (P2, P6, P9,
P8, P8b, P10).

## 5. Depende de decisão

1. **Tamanho:** com tudo, a T22 quase dobra. Alternativa: partir em duas aulas, "Gerencial: grupo e números" (caps. 00 a
   08 com P1 a P6) e "Gerencial: padrão, transferências e assinaturas" (caps. 09 a 11 com P7 a P10).
2. **Venda com estoque de outra unidade (P8b) contra a aprovação (cap10):** os dois recursos não convivem. A aula ensina
   os dois e diz que é uma escolha, ou recomenda um?
3. **Preço por unidade (P9):** o exemplo muda preço de material. Fica isolado nesta aula (proposto) ou vira fato do mundo?
4. **"Cobrança recorrente" ligada por padrão (P10):** a história paga recorrente (como a tela abre) ou desliga a chave
   para a "fatura única" que a fala atual descreve?
5. **"Gerenciar" plano da unidade (S1):** só citar (proposto) ou abrir o montador, que mostra valores de plano?
6. **Pendências antigas ainda abertas:** risco 1 ("Lucro Líquido"), risco 2 (Comparativo em competência) e os achados 1
   e 2 do `propostas_fala.md`. Enquanto o app não mudar, o cartão "Lucro Líquido" (B3) e o "Histórico de Envios" (P-7)
   ficam sem fala.
7. **Acerto do `MUNDO_FICTICIO.md`** com o `plano.md` (latinha e outubro), antes das sementes novas.
