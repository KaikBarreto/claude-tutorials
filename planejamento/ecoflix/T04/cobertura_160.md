# Cobertura 1.60.10 · T4 Clientes, fornecedores e a ficha do parceiro

Auditoria de 18/11/2026, só leitura de código. Base: `/dev/shm/ecoflix-src` (`APP_VERSION = "1.60.10"`) contra o roteiro
(1.59.154), com `git diff f37573ea0 5290be4cd`. Caminhos relativos a `src/`; linhas do 1.60.10. A varredura do robô
(`rec/varredura/t04.txt`) ainda não existe: tudo aqui vem do código e leva `[TESTAR]` onde depende de tela.

Arquivos da aula **sem mudança** entre as duas versões: `BalancesReportModal.tsx`, `CustomerSupplierHistory.tsx`,
`SupplierProfitEstimate.tsx`, `components/partner/*` (Financeiro e Notas fiscais da ficha), `EntitiesSummaryTab.tsx`,
`PartnerFiscalBadge.tsx`, `PartnerDuplicateBadge.tsx`, `lib/nfe/partnerFiscalReadiness.ts`, `utils/balanceFormatting.ts`,
`hooks/useBalance.tsx`, `utils/dualEntityLink.ts`, `CepLookup.tsx`, `CitySelector.tsx`, `i18n/locales/pt-BR/clients.json`.
Ou seja: **caps. 0, 1, 2, 7, 8, 10, 11, 12 e 13 batem com o 1.60.10 como estão.** Mudam os caps. 3, 4, 5, 6 e 9.

## 1. Mudou no app (por capítulo)

**cap03 · Buscar dados pelo CNPJ**

1. **Bloco novo no topo da janela, acima das abas**, depois de qualquer busca de CNPJ ou CEP que deixe campo da nota vazio:
   título **"Falta isto para emitir NF-e"** com a contagem **"(1)"**, a linha **"Dá para salvar o cadastro assim, mas a nota
   não sai até preencher."** e cada campo como link sublinhado (**"Número"**; os possíveis são "CEP", "Estado", "Cidade",
   "Logradouro", "Número", "Bairro"). Em outra aba o link mostra a aba de destino: **"Número (Dados Fiscais)"**. Clicar leva
   à aba e põe o cursor no campo (`components/entity-form/PendenciasNfePanel.tsx:40-58`, `entity-form/pendenciasNfe.ts:41-59`,
   `EntityFormDialog.tsx:1557-1561`, foco em `:383-407`). Caixa âmbar, fixa em todas as abas enquanto faltar algo.
   Efeito no roteiro: da linha 4 do cap03 em diante a caixa está na tela (inclusive na linha 6, em "Dados de Contato", como
   "Número (Dados Fiscais)"). A fala "repara que um campo ficou vermelho" continua verdadeira (a linha vermelha embaixo do
   campo não mudou, `:2393`), mas o caminho natural agora é a lista.
2. **A lupa passou a consultar também a inscrição estadual**, ao mesmo tempo que a Receita (`CnpjLookupInput.tsx:118-149`).
   Num cadastro **novo** o "Indicador IE" nasce em "Não Contribuinte" (`EntityFormDialog.tsx:754`), então o que aparece
   embaixo de "Inscrição Estadual" é: **"A Sintegra informa IE 688412573032 para este CNPJ em SP. A ficha está marcada como
   Não Contribuinte."** e o link **"Usar a da Sintegra"** (`:2056-2078`). Um clique preenche a inscrição e troca o indicador
   para "Contribuinte ICMS" de uma vez (`:951-964`, `:1069-1076`); a frase vira **"Preenchido pela consulta do CNPJ: a
   Sintegra informa a inscrição estadual 688412573032 para este CNPJ em SP."** (`:2008-2014`).
   Efeito: a linha 5 do cap04 (escolher "Contribuinte ICMS" e digitar os 12 dígitos; fala "Eu preencho o que ele passou")
   deixa de ser o jeito da tela. Vira um clique.
3. **Backend falso** (não é rótulo, mas quebra a gravação): a consulta de inscrição sai **direto do navegador** para
   `https://publica.cnpj.ws/cnpj/<14 dígitos>` (`utils/consultaIe.ts:93-130`), fora do Supabase. Sem interceptar, o robô faz
   chamada real para a internet com CNPJ fictício. Ver "Mundo" na seção 3. A edge `cnpj-lookup` ganhou dois campos na
   resposta: `regime_ecf` e `regime_ecf_ano` (`supabase/functions/cnpj-lookup/index.ts`, `utils/cnpjLookup.ts`); ausentes
   valem como "não se sabe", então a simulação atual não quebra, mas convém mandar `null` nos dois.

**cap04 · Dados fiscais e o campo vermelho**

4. Tudo do item 1 e do item 2 (a caixa "Falta isto para emitir NF-e (1)" some quando o "Número" é preenchido; a inscrição
   vem pelo "Usar a da Sintegra"). A frase do regime **não mudou** para o Simples: "Preenchido pela consulta do CNPJ: a
   Receita informa que esta empresa é optante pelo Simples Nacional." (`:2208-2213`). Sinal verde, triângulo e botão
   "<n> incompletos" iguais.

**cap05 · Cliente e fornecedor ao mesmo tempo**

5. **O saldo do parceiro duplo não troca mais de sinal entre as abas** (nota 1.59.161). Antes, na aba Fornecedores o valor
   aparecia invertido; agora as duas abas, a ficha, a conta-corrente e a janela de edição leem o saldo único na convenção do
   cliente (`utils/dualBalancePerspective.ts:7-10`, `ClientsListView.tsx:205`, `:510`, `:686`, `ClientsSuppliers.tsx:322`).
   Depósito Irmãos Siqueira: **"-R$ 840,00"** em vermelho, "a pagar", **nas duas abas e na ficha**.
   Efeito: (a) Tela da linha 4 do cap05: a ficha na aba Fornecedores mostra "-R$ 840,00" (o roteiro diz "R$ 840,00");
   (b) **fala da linha 7 fica errada**: "O sinal muda de uma aba pra outra, mas a cor continua vermelha"; (c) `plano.md`,
   tabela de saldos ("-R$ 840,00" em Clientes, "R$ 840,00" em Fornecedores) e a conferência de cores do robô.

**cap06 · Tabela de preço do parceiro**

6. A aba **"Preços"** da ficha ganhou um filtro de três botões com contagem, à esquerda de "Buscar material...":
   **"Todos"**, **"Já comprados"** (na aba "Venda": **"Já vendidos"**) e **"Personalizados"** (`EntityPricePanel.tsx:1115-1150`).
   Vazios novos: "Nenhum material comprado deste fornecedor", "Nenhum material vendido para este cliente", "Nenhum preço
   personalizado". A linha 6 do cap06 mostra essa aba: a tela tem os três botões. Consulta nova para o backend falso:
   `purchases` com `purchase_items(material_id)` por `supplier_id` (e `sales`/`sale_items` por `customer_id`), com
   `reverted_at` nulo.
7. No seletor "Tabela de Preços Padrão", a tabela que o usuário fixou ganha um alfinete ("Minha tabela fixada",
   `PriceTableSelector.tsx:70-72`, `:101-103`). Só aparece se alguém fixar; no mundo ninguém fixa. Assunto da T3.

**cap09 · Conta-corrente: saldo e extrato**

8. **Menu "Exportar"** (nota 1.60.3). Antes: "Abrir Relatório (PDF)" e "Baixar Excel (.xlsx)". Agora, na ordem:
   **"PDF resumido"**, **"PDF detalhado (com produtos)"**, **"Baixar Excel (.xlsx)"** (`pages/BalanceDetail.tsx:1596-1620`).
   Enquanto gera o detalhado o botão vira "Gerando…"; avisos: "Extrato detalhado gerado", "Pop-up bloqueado. Libere pop-ups
   para gerar o relatório detalhado." (`:477`, `:537`). No detalhado, cada pedido ganha embaixo a tabela "Material", "Preço
   unit.", "Quantidade", "Total" (`utils/entityReportExport.ts`). A Tela da linha 11 cita o rótulo antigo; a fala ("sai em
   PDF ou em planilha") continua certa, mas não conta a novidade.
9. **Backend falso do pagamento**: a janela "Nova Movimentação de Saldo" deixou de chamar `create_manual_bank_transaction`
   + `update_balance` + `INSERT balance_movements`. Agora é **uma RPC só**, `record_partner_balance_movement`
   (`p_company_id`, `p_entity_type`, `p_entity_id`, `p_amount`, `p_operation_type` 'debit'/'credit', `p_payment_method`,
   `p_description`, `p_cash_register_id`, `p_bank_account_id`, `p_transaction_at`, `p_client_request_id`;
   `BalancePaymentModal.tsx:309-321`). Rótulos da janela iguais. Excluir pagamento com grupo passou a usar
   `delete_payment_group_atomic` (`BalanceDetail.tsx:853-866`).

## 2. Falta cobrir

Vale = **sim** (capítulo ou trecho na seção 3), **citar** (uma frase, na linha indicada) ou **não**.

**Cadastro, parte fiscal (o que o 1.59.157 trouxe e o que já existia sem aparecer)**

| # | O que é (rótulo exato, arquivo) | Quando o cliente usa | Vale |
|---|---|---|---|
| F1 | Inscrição estadual pela lupa: os 7 resultados. "A Sintegra informa IE X para este CNPJ em UF. A ficha está marcada como Não Contribuinte." + "Usar a da Sintegra"; "Preenchido pela consulta do CNPJ: a Sintegra informa a inscrição estadual X..."; **"Confere com a consulta do CNPJ: a Sintegra informa esta mesma inscrição estadual para este CNPJ em UF."**; **"A Sintegra informa IE X para este CNPJ em UF. A ficha tem Y."** + "Usar a da Sintegra"; **"A Sintegra não tem inscrição estadual ativa para este CNPJ. Se ele for isento, marque Isento de Inscrição."**; "A consulta de inscrição estadual atingiu o limite de 3 por minuto. Tente de novo em 1 minuto."; "Informe o estado (UF) na aba Endereço para a consulta saber qual inscrição estadual deste CNPJ usar." (`EntityFormDialog.tsx:2004-2108`) | Toda empresa cadastrada pelo CNPJ; conferir cadastro antigo antes de emitir | **sim** (cap04 refeito, N1 e N2). Limite de 3 por minuto e falta de UF: **citar** |
| F2 | Regime pela escrituração: "Preenchido pela consulta do CNPJ: na escrituração de 2024 esta empresa declarou **Lucro Real**. Confirme com o contador se mudou desde então." (`:2219-2227`); quando não sabe: "A consulta do CNPJ diz que esta empresa **não** é optante pelo Simples, e a Receita não tem escrituração recente deste CNPJ pra dizer qual regime ele declarou. Se souber, escolha entre Lucro Presumido e Lucro Real." (`:2234-2239`); "A Receita não informou o regime deste CNPJ. Deixe em "Não informado" se você não souber." (`:2241-2245`) | Cliente indústria e fornecedor grande (Lucro Real ou Presumido) | **sim** (N1, exemplo em Lucro Real) |
| F3 | Alerta vermelho no topo de Dados Fiscais: "Atenção: a Receita informa que este CNPJ está **Baixada**." (o texto em negrito é a situação que a Receita devolve; `:1937-1945`, `utils/consultaIe.ts:223-228`) | Fornecedor que fechou a empresa e continua vendendo sucata | **sim** (N2) |
| F4 | Trocar o CNPJ depois da busca limpa o que a consulta tinha preenchido (inscrição, indicador, regime, MEI, alertas); o que a pessoa digitou fica (`:862-876`, `entity-form/procedenciaConsulta.ts`) | Digitou o CNPJ errado e corrigiu | **sim**, um trecho no N2 |
| F5 | "Indicador IE *": "Contribuinte ICMS", "Isento de Inscrição", "Não Contribuinte"; ajuda "Contribuinte ICMS exige Inscrição Estadual; Isento/Não Contribuinte não."; campo travado com "Contribuinte isento de Inscrição Estadual — campo não se aplica" / "Não contribuinte de ICMS — campo não se aplica"; erro ao salvar "Inscrição Estadual obrigatória para contribuinte de ICMS" (`:2112-2146`, `utils/indicadorIe.ts:18-60`) | Toda pessoa jurídica | **sim** (N1); o roteiro só diz "o indicador" |
| F6 | "Regime tributário do fornecedor/cliente": "Não informado", "Simples Nacional", "MEI", "Lucro Presumido", "Lucro Real"; ajudas "É o regime de quem compra de você, não o da sua empresa — esse fica em Configuração Fiscal → Impostos. Usado pelos cenários fiscais: em "Não informado", este parceiro só casa com cenários de regime "Qualquer" — nada é deduzido." e "**MEI é Simples Nacional.** Para a nota e para os cenários fiscais, os dois valem exatamente o mesmo..." (`:2160-2261`) | Quem emite nota com regra por regime do parceiro (T16) | **sim** (N1); os cenários são da **T16**, não repetir |
| F7 | Só no cliente: "É Indústria" ("Ativa diferimento de ICMS automático nas vendas") e "É uma Reciclagem" (sem texto de ajuda) (`:2265-2295`); "É Indústria" entra no cálculo da nota (`utils/invoiceTaxes.ts:731`, `:923`, `:1043`) | Venda para siderúrgica, fundição, outra reciclagem | **sim** (N1). O efeito na nota é da **T16** |
| F8 | "Novo Cliente": a aula só cadastra fornecedor | Todo cliente novo | **citar** no N1 (mesma janela, com os dois interruptores a mais) |
| F9 | Completar um cadastro incompleto pelo CEP: "CEP" busca sozinho com 8 dígitos e preenche "Estado", "Cidade", "Logradouro" e "Bairro"; se o CEP vier sem bairro, a caixa "Falta isto para emitir NF-e" lista "Bairro" (`pendenciasNfe.ts:23-26`, `CepLookup.tsx:49`) | Pessoa física que passa a receber nota (o Rogério do cap02) | **sim**, trecho N3 no cap04 |
| F10 | Nota barrada por falta de inscrição (rejeição 232) e o botão que grava a inscrição no cadastro pela tela da nota | Na emissão | **não**: é da **T16** (F10 e N2 do `T16/cobertura_160.md`) |

**Cadastro, o resto da janela**

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| F11 | "Saldo inicial" aberto: "+ Adicionar saldo inicial", "Tipo de saldo" ("Eu devo a ele (a pagar)" / "Ele me deve (a receber)" no fornecedor; o inverso no cliente), "Valor", prévia "Saldo inicial: ..." (`:2800-2895`, `:1470-1472`) | Migração do caderno | **sim**, trecho N4 no cap02 (o roteiro só passa por cima) |
| F12 | Em edição: "Saldo", "Saldo atual: R$ ... (a pagar) · Última atualização ...", "Alterar saldo", "Cancelar alteração" | Corrigir saldo errado | **citar** no N5 (é o mesmo acerto do "Editar saldo") |
| F13 | Caixas "Mostrar o telefone no comprovante", "Mostrar a chave PIX no comprovante", "Mostrar CPF/CNPJ no comprovante", "Mostrar endereço no comprovante", "Mostrar os dados bancários no comprovante" (`:1649`, `:1683`, `:1787`, `:1929`, `:2441`) | Quem quer o dado do parceiro no papel | **citar** no cap02 (uma frase; o comprovante é da T7) |
| F14 | "Etiqueta" e "Dados bancários" em Dados de Contato; botão "Configurações" da tela ("Etiquetas": "Nova etiqueta", "Classifique clientes e fornecedores com uma cor fácil de reconhecer."; "Campos personalizados": "Novo campo", tipos "Texto curto", "Texto longo", "Número", "Data", "Sim/Não", "Lista de opções", "Obrigatório no cadastro", "Mostrar no portal") (`clients-suppliers/ClientsSuppliersSettingsDialog.tsx`) | Separar carroceiro, oficina, indústria; guardar dado próprio | **sim**, capítulo N6 curto |
| F15 | Filtros da lista: "Situação do saldo" ("Todos", "Com saldo", "Saldo zerado"), "Etiquetas"; "Ordenar" ("Código", "Nome", "Saldo", "CPF/CNPJ", "Telefone") | Achar quem está devendo | **sim**, no N6 (o roteiro só passa o mouse) |
| F16 | Aviso ao sair do campo: "Já existe um fornecedor cadastrado como “Nome” com este telefone." / "...com este CPF/CNPJ." (`:1620-1624`, `:1902-1906`); selo vermelho "Duplicado" na lista | Cadastro repetido | **citar** na dica do cap01 |
| F17 | "Também é cliente" quando o outro lado já existe com o mesmo CPF/CNPJ: "Vinculado ao cliente existente." | Juntar dois cadastros antigos | **citar** no cap05 |
| F18 | "Desvincular" (rodapé do Editar no parceiro duplo): "Desvincular cliente e fornecedor", "Escolha qual lado deve permanecer — o outro será removido.", "Manter como Cliente" / "Manter como Fornecedor" (`pages/ClientsSuppliers.tsx:1697-1727`) | Marcou por engano | **citar** no cap05 |
| F19 | Menu "..." da linha e da ficha: "Editar", "Excluir" ("Confirmar Exclusão", "Esta ação não pode ser desfeita."; no duplo: "Entidade dual não pode ser excluída ... Desfaça o vínculo antes de excluir."), "Portal do Fornecedor", "Nova Movimentação" | Limpar cadastro de teste | **citar** no N6 (mostrar o menu, sem excluir) |
| F20 | Aba "Portal" da janela ("Link do portal", "Pedir login no portal", o que o parceiro vê) | Portal | **não**: **T20** |

**Ficha e conta-corrente**

| # | O que é | Quando usa | Vale |
|---|---|---|---|
| F21 | Movimentação: "Receber" ("Você recebeu do fornecedor - Aumenta o saldo dele com você"), "Dinheiro" (apagado sem caixa aberto), "Data e hora do lançamento", aviso "Valor maior que o saldo atual. Isso criará um saldo negativo." (`BalancePaymentModal.tsx:166-190`, `:523-527`) | Adiantamento, vale, acerto em dinheiro | **sim**, N5 |
| F22 | "Crédito/débito": janela "Lançar crédito/débito", "Direção" ("Aumenta o que eu devo a ele · ou abate o que ele me deve" / "Aumenta o que ele me deve · ou abate o que eu devo a ele"), "Valor", prévia "Saldo hoje ... → depois ...", "Motivo do lançamento *" (não mexe em caixa nem banco; `components/balance/BalanceEntryDialog.tsx`) | Desconto combinado depois, bônus, abatimento | **sim**, N5 |
| F23 | Lápis "Editar saldo" ("Editar saldo (definir o valor final)", "Tipo de saldo", "Valor", "Observação (opcional)"; `balance/EditEntityBalanceDialog.tsx`) | Saldo que nasceu errado | **sim**, N5 (mostrar, sem salvar) |
| F24 | Lápis e lixeira de cada linha do extrato ("Editar movimentação", "Excluir movimentação"; "Excluir Movimentação", "Efeitos da exclusão", "Confirmar Exclusão"; "Lançamento excluído e todos os efeitos revertidos"; conciliado: "Este lançamento está conciliado com o extrato bancário. Desfaça a conciliação...") | Lançou valor errado | **sim**, N5 |
| F25 | Filtro "Data" do extrato; clicar num pedido abre os itens dele na própria linha | Conferir um mês com o parceiro | **citar** no N5 |
| F26 | "PDF detalhado (com produtos)" (item 8 da seção 1) | Parceiro que pede o extrato com os materiais | **sim**, linha do cap09 refeita |
| F27 | Aba "Preços": pôr um preço especial. Colunas "Estado" ("Herda", "Vinculado", "Fixo"), "Base", "Variação", "Preço final"; "Vincular todos", "Limpar preços personalizados", "Salvar preços"; filtro "Personalizados" (`EntityPricePanel.tsx:761-763`, `:839-843`, `:1190-1212`) | Preço combinado com um parceiro | **sim**, trecho N7 no cap06. A `T03/cobertura_160.md` (F16) deixou isso para a T4 |
| F28 | "Vencimento do saldo: dd/mm" e "Limpar vencimento" na conta-corrente | Venda ou compra no saldo com data | **não** aqui: nasce no pedido (**T7**) e na conta a receber (**T13**) |
| F29 | Pedidos: "Exportar" e ações da linha; Lucro estimado: "Exportar PDF" e "* preço de venda do cadastro (sem venda no período)" | Relatório do parceiro | **citar** (uma frase em cada capítulo) |
| F30 | "Tabela de preços" (botão da conta-corrente): abre os mesmos "Preços Personalizados" | atalho | **não** (repete a aba Preços) |

**De outra aula, não repetir**: restrição "só os próprios cadastros" e saldo oculto ("***", "Sem permissão para ver saldos",
`ClientsSuppliers.tsx:264-303`) e contas bancárias por usuário (1.59.165): **T2**. Cadastro rápido dentro da compra e do
ticket (1.59.155): **T7/T8**. "Saldo do Cliente" na pesagem avulsa (1.59.163): **T8**. Sugestão de cliente ou fornecedor ao
lançar conta (1.60.5): **T13**. Movimentar saldo pela conversa com o Cato (1.60.0): **T21**. "Importar da Matriz": **T22**.
Alfinete da tabela fixada: **T3**. "Ver tutorial" e "Como funciona?": fora (ajuda da própria tela). Lista vazia da busca
("Nenhum fornecedor encontrado", "Tente outro termo ou limpe a busca.", `ClientsListView.tsx:679-682`): fora.

## 3. Proposta

Ordem nova: 0 · 1 · 2 (+N4) · 3 · 4 (refeito, +N3) · **N1** · **N2** · 5 · 6 (+N7) · **N6** · 7 · 8 · 9 · **N5** · 10 · 11 · 12 · 13.

### 3.1 Linhas a trocar nos capítulos que existem

| Cap. | Linha | Tela nova | Fala nova |
|---|---|---|---|
| 02 | depois da L5 (Pix) | O mouse passa por "Mostrar o telefone no comprovante" e "Mostrar a chave PIX no comprovante", sem marcar. | Essas caixinhas de mostrar no comprovante decidem se o dado do parceiro sai impresso no papel dele. |
| 03 | L4 | A caixa âmbar "Falta isto para emitir NF-e (1)" aparece no topo junto com o toast; a câmera mostra "Nome Fantasia" e "Razão Social". | Pronto. A tela pede pra conferir antes de salvar. Vieram a razão social e o nome fantasia. |
| 03 | L7 | Em "Dados de Contato", [ZOOM: a caixa "Falta isto para emitir NF-e (1)", "Dá para salvar o cadastro assim, mas a nota não sai até preencher." e o link "Número (Dados Fiscais)"]. | E repara nesse aviso amarelo, em cima: falta um campo pra emitir nota fiscal. |
| 05 | L4 (Tela) | ficha com "Fornecedor", "Cliente+Fornecedor", **"-R$ 840,00"** em vermelho e "a pagar". | (igual) |
| 05 | L7 | Clique em "Clientes". [ZOOM: a linha "Depósito Irmãos Siqueira", "Cliente+Fornecedor", "-R$ 840,00" em vermelho] | Na aba Clientes, ele aparece do mesmo jeito: o mesmo valor, o mesmo vermelho. É um saldo só, e a Recicla deve. |
| 05 | depois da L3 | Reabre "Editar"; o mouse para no botão "Desvincular", no rodapé, sem clicar. | Se marcou por engano, o botão Desvincular, aqui no Editar, separa os dois de novo. E se o cliente já existia com o mesmo CNPJ, o sistema só liga um cadastro no outro. |
| 09 | L11 | Clique em "Exportar": "PDF resumido", "PDF detalhado (com produtos)" e "Baixar Excel (.xlsx)"; o mouse para no segundo; não clica (Esc). | E no Exportar, o extrato sai em PDF ou em planilha, pra mandar pro parceiro. O PDF detalhado mostra, em cada pedido, os materiais, o peso e o preço. |
| 13 | L2 | Montagem: a lupa, o aviso amarelo e o "Usar a da Sintegra". | Cadastrou a serralheria com a busca pelo CNPJ, que trouxe o endereço, a inscrição estadual e o regime, e completou o que faltava pra nota fiscal. |

### 3.2 cap04 refeito · O que falta pra emitir nota (vinheta: FISCAL)

Semente `apos-cap02`; o `setup` refaz o cap03 fora do vídeo e para em "Dados de Contato" com a caixa âmbar no topo.

| Tela | Fala |
|---|---|
| [ZOOM: a caixa "Falta isto para emitir NF-e (1)" com o link "Número (Dados Fiscais)"] | O aviso amarelo lista o que a nota fiscal exige e a consulta não trouxe. Aqui, só o Número. |
| Clique em "Número (Dados Fiscais)": a janela troca para "Dados Fiscais" e o cursor cai em "Número", com a linha vermelha "Não veio da Receita — obrigatório para emitir NF-e". | Clicando no nome do campo, a tela me leva direto pra ele. |
| [ILUSTRAÇÃO: a nota leva o endereço (a mesma de hoje).] | A nota leva o endereço completo do parceiro. Sem o número, a SEFAZ pode recusar a nota. Por isso a tela já cobra o que falta. |
| Digita "418": a linha vermelha e a caixa âmbar somem. | Eu completo com o número, quatrocentos e dezoito, e o aviso some. |
| Rola até "Inscrição Estadual". [ZOOM: "A Sintegra informa IE 688412573032 para este CNPJ em SP. A ficha está marcada como Não Contribuinte." e o link "Usar a da Sintegra"] | Agora, a inscrição estadual. A consulta também foi buscar esse número no cadastro do estado, e achou. |
| Clique em "Usar a da Sintegra": "Inscrição Estadual *" recebe 688412573032, "Indicador IE *" vira "Contribuinte ICMS" e a frase muda para "Preenchido pela consulta do CNPJ: a Sintegra informa a inscrição estadual 688412573032 para este CNPJ em SP.". [ZOOM: os dois campos] | Um clique em Usar a da Sintegra preenche a inscrição e já marca a serralheria como contribuinte de ICMS. Os dois campos andam juntos, do jeito que a nota pede. |
| [ZOOM: "Regime tributário do fornecedor" em "Simples Nacional" e a frase "Preenchido pela consulta do CNPJ: a Receita informa que esta empresa é optante pelo Simples Nacional."] | O regime também veio: Simples Nacional. E é o regime da serralheria, não o da Recicla Vale. |
| A câmera abre na aba inteira. | Uma dica: a consulta adianta o trabalho, mas quem confirma inscrição e regime é o contador. Na dúvida, manda a ficha pra ele antes da primeira nota. |
| "Salvar"; toast "Fornecedor cadastrado com sucesso!"; ícone verde, tooltip "Pronto para emitir NF-e". | Salvar. Na lista, a serralheria ganha o sinal verde: pronta pra emitir nota fiscal. |
| Triângulo do "Rogério Alves Costa": tooltip "Faltam dados para emitir NF-e para este cadastro:" e a lista. | Já o Rogério, que a gente cadastrou sem endereço, aparece com o triângulo de incompleto. O aviso mostra o que falta pra nota. |
| **(N3)** Clique no Rogério, "Editar", "Dados Fiscais"; em "CEP" digita "12062150": "Estado" SP, "Cidade" Taubaté, "Logradouro" e "Bairro" entram sozinhos; em "Número" digita "77"; "Salvar"; toast "Fornecedor atualizado!"; o triângulo vira o sinal verde. | Pra completar, é só editar. Eu digito o CEP, e a cidade, a rua e o bairro vêm sozinhos. Ponho o número, salvo, e o Rogério também fica pronto pra nota. |
| Botão "<n> incompletos": ficam "Valdir Pereira", "Aparecida Ramos" e "Cida Ramos"; "Mostrar todos". | E o botão de incompletos, lá em cima, mostra só quem ainda está com o cadastro pela metade. |
| A câmera abre na lista. | Uma dica: quem não emite nota pode deixar a aba Dados Fiscais de lado. Só com o nome, o parceiro já tem histórico e saldo, e o aviso não trava compra nem venda. |

### 3.3 N1 · Empresa do Lucro Real: inscrição, regime e indústria (vinheta: FISCAL) · capítulo novo, depois do cap04

Semente `apos-cap04`, aba "Clientes". Exemplo: a Aços Quiririm Ltda, siderúrgica de Taubaté, cliente da Recicla Vale.

| Tela | Fala |
|---|---|
| Aba "Clientes"; clique em "Aços Quiririm Ltda" e em "Editar": janela "Editar Cliente"; aba "Dados Fiscais". | Agora, um cliente grande. A Aços Quiririm é uma siderúrgica, e a Recicla Vale emite nota fiscal pra ela. Em empresa assim, três campos decidem se a nota sai certa. Vou abrir o cadastro dela, no Editar, em Dados Fiscais. |
| O mouse para na lupa do CNPJ; clique: a lupa gira; toast "Dados preenchidos — confira antes de salvar". | A lupa também serve pra conferir um cadastro antigo. Um clique, e o sistema consulta de novo. |
| [ZOOM: embaixo de "Inscrição Estadual": "A Sintegra informa IE <certa> para este CNPJ em SP. A ficha tem <errada>." e o link "Usar a da Sintegra"] | Primeiro, a inscrição estadual. Olha o aviso: o número que estava na ficha é diferente do que o estado informa. Alguém digitou errado lá atrás. |
| (o zoom continua) | Repara que o sistema não trocou nada sozinho. Ele mostra os dois números e deixa a escolha com você. |
| Clique em "Usar a da Sintegra": o campo troca e a frase vira "Preenchido pela consulta do CNPJ: a Sintegra informa a inscrição estadual <certa> para este CNPJ em SP.". | Eu clico em Usar a da Sintegra, e a ficha fica com o número certo. Inscrição errada é um dos motivos mais comuns de nota recusada. |
| Clique em "Indicador IE *": lista "Contribuinte ICMS", "Isento de Inscrição", "Não Contribuinte"; o mouse passa pelas três; fecha em "Contribuinte ICMS". [ZOOM: a lista e a ajuda "Contribuinte ICMS exige Inscrição Estadual; Isento/Não Contribuinte não."] | Segundo, o Indicador. Contribuinte de ICMS é a empresa que tem inscrição estadual, como a siderúrgica. Isento de Inscrição é a empresa que o estado dispensou. E Não Contribuinte é quem não tem inscrição, como a pessoa física. |
| (o zoom continua) | Só o contribuinte leva o número da inscrição. Nos outros dois, o campo fica travado, e tem que ficar vazio mesmo. |
| [ZOOM: "Regime tributário do cliente" em "Lucro Real" e a frase "Preenchido pela consulta do CNPJ: na escrituração de 2024 esta empresa declarou Lucro Real. Confirme com o contador se mudou desde então."] | Terceiro, o regime tributário do cliente. A consulta preencheu Lucro Real, e disse de onde tirou: da escrituração de dois mil e vinte e quatro. |
| (o zoom continua) | Esse dado vem com atraso. Por isso a tela pede: confirma com o contador se mudou desde então. |
| Clique no seletor: "Não informado", "Simples Nacional", "MEI", "Lucro Presumido", "Lucro Real"; fecha sem trocar. | As opções são Simples Nacional, MEI, Lucro Presumido e Lucro Real. E tem o Não informado: se você não sabe, deixa assim. O sistema não chuta regime. |
| [ZOOM: a ajuda "É o regime de quem compra de você, não o da sua empresa — esse fica em Configuração Fiscal → Impostos."] | Uma dica: aqui vai o regime da Aços Quiririm, não o da Recicla Vale. O da sua empresa fica na Configuração Fiscal, e a gente vê no tutorial de nota fiscal. |
| Rola até "É Indústria" ("Ativa diferimento de ICMS automático nas vendas") e "É uma Reciclagem". Clique em "É Indústria": liga. [ZOOM: os dois interruptores] | No cadastro de cliente tem mais dois botões. É Indústria: ligado, ele ativa o diferimento de ICMS automático nas vendas pra esse cliente. A siderúrgica é indústria, então eu ligo. |
| (o zoom continua; o mouse para em "É uma Reciclagem", sem ligar) | E É uma Reciclagem, pra quando o cliente é outro pátio. Quem diz qual dos dois vale pra cada cliente é o contador. |
| "Salvar"; toast "Cliente atualizado!"; a linha da Aços continua com o sinal verde. | Salvar. A Aços Quiririm está com a inscrição, o regime e o tipo certos. Quando chegar a hora da nota, o sistema já sabe com quem está falando. |
| O mouse para em "Novo Cliente", sem clicar. | E cliente novo é a mesma janela do fornecedor, em Novo Cliente, com esses dois botões a mais. |

### 3.4 N2 · Os avisos da consulta (vinheta: FISCAL) · capítulo novo, depois do N1

Semente `apos-cap04`, aba "Fornecedores". Nada é salvo.

| Tela | Fala |
|---|---|
| "Novo Fornecedor"; "Nome *": "Oficina do Tonho"; "Dados Fiscais", "Pessoa Jurídica"; CNPJ "52.917.384/0001-05"; clique na lupa. | A consulta também avisa quando tem problema. Chegou a Oficina do Tonho, querendo vender sucata com nota. Eu ponho o CNPJ e clico na lupa. |
| [ZOOM: o alerta vermelho "Atenção: a Receita informa que este CNPJ está **Baixada**."] | Olha o aviso vermelho: a Receita informa que esse CNPJ está baixado. A empresa foi encerrada. |
| (o zoom continua) | Nota fiscal pra CNPJ baixado, a SEFAZ recusa na certa. Melhor descobrir aqui do que depois de emitir. |
| Rola até "Inscrição Estadual": "A Sintegra não tem inscrição estadual ativa para este CNPJ. Se ele for isento, marque Isento de Inscrição." [ZOOM] | Embaixo, outro aviso: o estado não tem inscrição ativa pra esse CNPJ. Se a empresa for isenta, você marca Isento de Inscrição, em vez de deixar o campo vazio. |
| Volta ao "CNPJ", apaga e digita "46.280.719/0001-24" (o da serralheria): o alerta vermelho e o aviso da inscrição somem na hora; o campo mostra o aviso de CNPJ já cadastrado. | E se você digitou o CNPJ errado? É só corrigir. Quando o CNPJ muda, o sistema apaga o que tinha trazido da empresa anterior, pra não misturar dado de duas empresas. O que você digitou à mão, ele mantém. |
| "Cancelar". | Uma dica: se a consulta da inscrição disser que atingiu o limite, é só esperar um minuto e clicar de novo. Ela aceita três consultas por minuto. |

### 3.5 N4 (trecho no cap02, no lugar da linha do "Saldo inicial")

| Tela | Fala |
|---|---|
| Rola até "Saldo inicial"; clique em "+ Adicionar saldo inicial": "Tipo de saldo" com "Eu devo a ele (a pagar)" e "Ele me deve (a receber)", e "Valor". O mouse passa pelas duas opções. | Lá embaixo fica o Saldo inicial. Se o parceiro já chega com um valor do caderno antigo, você escolhe o lado, eu devo a ele ou ele me deve, e põe o valor. |
| Clique em "Cancelar alteração" (o bloco fecha). [TESTAR: o rótulo do botão de fechar na criação] | O Rogério começa do zero, então eu deixo sem. |

### 3.6 N7 (trecho no fim do cap06, no lugar da última linha)

| Tela | Fala |
|---|---|
| Na ficha do depósito, clique em "Preços": "Preços Personalizados", abas "Compra" e "Venda", filtro "Todos", "Já comprados", "Personalizados". | O preço especial de cada parceiro fica na ficha dele, na aba Preços. Tem um lado pra compra e outro pra venda. |
| Clique em "Já comprados": ficam ferro pesado, ferro misto e cobre misto. | O filtro Já comprados mostra só o que esse fornecedor já trouxe. Fica fácil achar o material. |
| Na linha "Ferro pesado", em "Estado" troca "Herda" por "Fixo" e digita o preço "1,00"; "Preço final" R$ 1,00. [ZOOM: a linha] | Cada material tem um estado. Herda segue a tabela do parceiro. Fixo é um preço combinado, que não muda quando a tabela muda. Eu combino o ferro pesado do depósito a um real o quilo. |
| O mouse para em "Vinculado", na lista do "Estado", sem escolher. | E Vinculado acompanha uma tabela com uma diferença, pra cima ou pra baixo. |
| "Salvar preços"; clique em "Personalizados": ficam o bronze (do tutorial de materiais) e o ferro pesado. | Salvar preços. Em Personalizados ficam só os combinados desse parceiro. |

### 3.7 N6 · Organizar a lista: etiquetas, filtros e ordem (vinheta: PARCEIROS) · capítulo novo, depois do cap06

Semente `apos-cap06`, aba "Fornecedores".

| Tela | Fala |
|---|---|
| Clique em "Configurações": janela com "Etiquetas" e "Campos personalizados". | Com a lista crescendo, vale organizar. Em Configurações ficam as etiquetas e os campos personalizados. |
| "Nova etiqueta": nome "CARROCEIRO", escolhe uma cor, "Aplicar em" "Somente fornecedores"; "Salvar". | Etiqueta é uma marca colorida pra separar os parceiros. Eu crio a etiqueta Carroceiro, só pra fornecedores. |
| O mouse passa por "Campos personalizados" e "Novo campo" ("Texto curto", "Número", "Data", "Sim/Não", "Lista de opções"), sem criar. Fecha. | Nos campos personalizados, você cria uma informação sua, como a placa do veículo, e ela aparece no cadastro e na ficha. |
| "Valdir Pereira" → "Editar" → em "Etiqueta" marca "CARROCEIRO" → "Salvar"; a linha ganha a etiqueta. | No cadastro do Valdir, em Etiqueta, eu marco Carroceiro. |
| Clique em "Filtros": "Situação do saldo" ("Todos", "Com saldo", "Saldo zerado") e "Etiquetas"; escolhe "Com saldo": ficam Cooperativa, Valdir e Depósito. | Nos Filtros, dá pra ver só quem está com saldo, ou só uma etiqueta. Com saldo, sobram os três fornecedores com conta aberta. |
| Limpa o filtro; clique em "Ordenar" → "Saldo". | E no Ordenar, a lista vai por código, nome, saldo, documento ou telefone. |
| Clique no "..." da linha "Cida Ramos": "Editar", "Excluir", "Portal do Fornecedor", "Nova Movimentação"; o mouse para em "Excluir", sem clicar; Esc. | Nos três pontinhos de cada linha ficam os atalhos: editar, lançar movimentação e excluir. A exclusão não tem volta, então confere antes. |

### 3.8 N5 · Ajustes na conta-corrente (vinheta: SALDO) · capítulo novo, depois do cap09

Semente `apos-cap09`, ficha da Cooperativa Recomeço, aba "Conta-corrente" (saldo R$ 1.350,00).

| Tela | Fala |
|---|---|
| Clique em "Movimentação"; o mouse passa por "Receber" ("Você recebeu do fornecedor - Aumenta o saldo dele com você") e por "Dinheiro"; "Cancelar". | Na Movimentação tem mais duas coisas. O tipo Receber, pra quando o fornecedor te devolve dinheiro. E a forma Dinheiro, que sai do caixa e só funciona com um caixa aberto. |
| Clique em "Crédito/débito": janela "Lançar crédito/débito", "Saldo atual: R$ 1.350,00". | E quando o acerto não envolve dinheiro? A cooperativa aceitou um desconto de cinquenta reais, porque o papelão de sexta veio molhado. Pra isso existe o Crédito/débito. |
| Em "Direção" clica em "Aumenta o que ele me deve · ou abate o que eu devo a ele"; "Valor" 50; [ZOOM: a prévia "Saldo hoje R$ 1.350,00 ... → depois R$ 1.300,00"] | Eu escolho a direção: abate o que eu devo a ele. Ponho cinquenta reais, e a tela já mostra a conta: o saldo de hoje e como fica depois. |
| "Motivo do lançamento *": "Desconto do papelão molhado de 06/11"; confirma; o extrato ganha a linha "Ajuste" e o "Saldo Atual" vira R$ 1.300,00. | O motivo é obrigatório. Confirmo, e o saldo cai pra mil e trezentos. Esse lançamento mexe só no saldo: não passa pelo caixa nem pelo banco. |
| O mouse para no lápis e na lixeira da linha nova ("Editar movimentação", "Excluir movimentação"). | Lancei errado? Cada linha do extrato tem um lápis, pra corrigir, e uma lixeira, pra excluir. |
| Clique na lixeira: "Excluir Movimentação", com "Efeitos da exclusão"; "Confirmar Exclusão"; toast; o saldo volta a R$ 1.350,00. [TESTAR: a lixeira aparece na linha de ajuste e o saldo volta] | A cooperativa mudou de ideia, então eu excluo. A tela mostra o que vai ser desfeito, eu confirmo, e o saldo volta pra mil trezentos e cinquenta. |
| O mouse para na linha do Pix de R$ 1.200,00. | Uma dica: excluir um pagamento desfaz tudo junto, o saldo do parceiro e a saída do banco. Se ele já estiver conciliado com o extrato do banco, o sistema pede pra desfazer a conciliação antes. |
| Clique no lápis "Editar saldo" ao lado de "Saldo Atual": janela "Editar saldo" ("Tipo de saldo", "Valor", "Observação (opcional)"); "Cancelar". | E o lápis do lado do Saldo Atual é só pra correção: ele define o valor final do saldo, direto. No dia a dia, use a Movimentação e o Crédito/débito, que deixam o histórico explicado. |
| Clique em "Data" (filtro do extrato) e fecha; clique numa linha "Pedido": os itens abrem embaixo. | No filtro Data, você olha um período só. E clicando num pedido, os materiais dele abrem ali mesmo. |

### 3.9 O que o mundo fictício precisa ter

- **Consulta de inscrição estadual (novo, vale para a aula inteira)**: interceptar no navegador `GET https://publica.cnpj.ws/cnpj/<14 dígitos>`
  e responder `{ "estabelecimento": { "situacao_cadastral": "Ativa", "inscricoes_estaduais": [ { "inscricao_estadual":
  "688412573032", "ativo": true, "atualizado_em": "2026-10-02T00:00:00Z", "estado": { "sigla": "SP" } } ] } }`
  (formato lido em `utils/consultaIe.ts:136-184`). Qualquer CNPJ sem resposta simulada devolve 404 (o app fica mudo).
  RPC `registrar_consulta_cnpj_ie` (grava o cache; devolve vazio) e select em `cnpj_registros_estaduais`
  (`utils/consultaIeCache.ts:88`, `:162`).
- **Edge `cnpj-lookup`**: acrescentar `regime_ecf` e `regime_ecf_ano` em todas as respostas (`null` na serralheria).
- **cap04**: a inscrição 688412573032 já é a do plano; ela agora vem da consulta, não da digitação. **N3**: edge
  `cep-lookup` para 12062150 (Rua das Palmeiras, Jardim Santa Luzia, Taubaté, SP) e o `UPDATE suppliers` do Rogério
  (número 77, `codigo_ibge` 3554102). As sementes `apos-cap04` em diante passam a ter o Rogério completo; "<n> incompletos"
  fica com três nomes.
- **N1**: na semente `t04/inicio`, a Aços Quiririm com `indicador_ie` 1, uma `inscricao_estadual` com um dígito trocado em
  relação à "certa" (duas inscrições de SP com dígito válido, a gerar pelo agente Mundo), `regime_tributario` nulo e
  `is_industry` falso. `cnpj-lookup` do CNPJ dela: os dados que a semente já tem (endereço completo, para a caixa âmbar
  não abrir), `opcao_pelo_simples: false`, `opcao_pelo_mei: false`, `regime_ecf: "lucro_real"`, `regime_ecf_ano: 2024`.
  `publica.cnpj.ws`: "Ativa" e a inscrição certa em SP. `UPDATE customers` (inscrição, `regime_tributario` 'lucro_real',
  `is_industry` true). Vira semente nova `apos-n1`, base do cap05 em diante.
- **N2**: CNPJ fictício 52.917.384/0001-05 (dígitos válidos; conferir que não é de empresa real). `cnpj-lookup`: razão social
  "ANTONIO CARLOS MEIRELES OFICINA MECANICA", Rua dos Ipês, 90, Vila São Geraldo, Taubaté/SP, CEP 12062-150, Simples
  `null`, ECF `null`. `publica.cnpj.ws`: `situacao_cadastral: "Baixada"`, `inscricoes_estaduais: []`. O select de
  duplicado por CPF/CNPJ devolve a serralheria quando o CNPJ dela é digitado. Nada é gravado.
- **cap06 + N7**: `purchases` com `purchase_items(material_id)` do depósito (a compra de 06/11); gravação em
  `entity_custom_prices` do ferro pesado fixo a 1,00 (compra). **Decisão**: esse preço muda a compra do depósito nas aulas
  seguintes; se não puder, o robô mostra e sai sem salvar ("Sair sem salvar?").
- **N6**: tabelas de etiqueta e de campo personalizado (`entity_labels`, `entity_custom_field_definitions`, RPC
  `set_partner_labels` com a etiqueta do Valdir). Semente própria, sem levar a etiqueta para as outras aulas, ou levar
  (decisão da junção).
- **cap09 e N5**: RPC `record_partner_balance_movement` no lugar das três chamadas antigas (debita o banco, baixa o saldo e
  cria o movimento, como o banco faz); RPC `apply_balance_delta` (N5) e a exclusão do ajuste (`update_balance` com o
  valor invertido + `DELETE balance_movements`, caminho sem grupo de `BalanceDetail.tsx:868-925`). O N5 termina com o
  saldo igual ao do começo: nenhuma semente nova.
- **Saldos**: nenhum número muda. Só o sinal do depósito na aba Fornecedores e na ficha ("-R$ 840,00").

## 4. Estimativa

| Bloco | Fala a mais (líquido, a 2,6 palavras/s) |
|---|---|
| Linhas trocadas (3.1) e cap04 refeito com o N3 | ~60 s |
| N1 · Empresa do Lucro Real | ~150 s |
| N2 · Os avisos da consulta | ~60 s |
| N4 (saldo inicial) e N7 (preço especial) | ~35 s |
| N6 · Organizar a lista | ~45 s |
| N5 · Ajustes na conta-corrente | ~95 s |
| **Total** | **~445 s (7 min 25 s) de fala; 4 capítulos novos e 3 trechos** |

A aula passa de ~15 para ~23 a 24 min de vídeo (com 4 vinhetas a mais). A parte fiscal (cap04 refeito, N1 e N2) responde por ~4 min desse aumento.

## 5. Depende de decisão

1. **Ligar "É Indústria" na Aços Quiririm** (N1) muda o imposto das notas dela na T16/T17 (diferimento automático). Se a
   junção não quiser mexer, o robô só mostra o interruptor, sem ligar, e a fala troca "então eu ligo" por "quem decide é
   o contador".
2. **Qual cliente é o exemplo de Lucro Real**: Aços Quiririm (proposto) ou Fundição Bandeira do Vale, que a T16 já usa com
   cenário próprio. Vale combinar com a T16 para não corrigir a inscrição do mesmo cliente duas vezes.
3. **Tamanho**: ~24 min numa aula só, ou partir em duas (cadastro e fiscal; ficha e saldo).
4. **N7 e N6 gravam no mundo** (preço fixo do depósito, etiqueta do Valdir): levar para as próximas aulas ou não.
5. **"É uma Reciclagem"** não tem texto de ajuda no app e não achei uso dele no cálculo da nota: a fala proposta só lê o
   rótulo. Conferir com o time do app o que ele faz antes de gravar.

## 6. Achados do app (para o time, fora do roteiro)

- O aviso "Informe o estado (UF) na **aba Endereço**..." (`EntityFormDialog.tsx:2105`) cita uma aba que não existe: o
  estado fica em "Dados Fiscais", no bloco "Endereço Fiscal".
- A nota 1.60.3 fala em "aba *Saldo*"; na ficha a aba se chama "Conta-corrente" (`ClientsListView.tsx`).
- A janela "Nova Movimentação de Saldo" continua pintando o "Saldo Atual" de verde quando positivo, também no fornecedor
  (`BalancePaymentModal.tsx`, linha do `currentBalance > 0`): o achado do inventário segue valendo.
