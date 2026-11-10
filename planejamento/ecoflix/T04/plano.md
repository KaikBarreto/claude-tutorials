# Plano · T4 Clientes, fornecedores e a ficha do parceiro

- **Título:** Clientes, fornecedores e a ficha do parceiro (o da fonte).
- **Objetivo (uma frase):** cadastrar quem traz e quem leva sucata (pessoa física, empresa pela busca do CNPJ, parceiro
  que é cliente e fornecedor) e aprender a ler o saldo na ficha e no relatório de saldos.
- **Antes:** T3 · Materiais e tabelas de preço. **Próximo:** T5 · Balança e impressora: o EcoTray.
- **Áreas das vinhetas:** PARCEIROS · CADASTRO · CADASTRO · FISCAL · SALDO · PREÇOS · FICHA · FICHA · SALDO · FICHA · FICHA ·
  SALDO · RESUMO.
- **Duração estimada:** ~15 min de vídeo (1.966 palavras, ~12,6 min de fala a 2,6 palavras/s, mais 13 vinhetas, as
  ilustrações e as esperas de tela). Alvo da fonte: 17 min. Voz: 11.052 caracteres (falas + títulos).
- **Pronúncia:** as do PERFIL que a aula usa (SEFAZ, PDF, EcoTray) e duas novas a testar: "Cliente-mais-Fornecedor" →
  Cliente+Fornecedor e "pét" → PET. O `config_narracao.json` do T04 segue o `PERFIL.md` (o do perfil estava, às 01:20,
  com NF-e, NFS-e e ICMS em outra grafia; a aula não fala nenhum dos três).
- **Base:** `T04/inventario.md` (código 1.59.154). **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos.
- **Usuário:** Rafael Nogueira (dono, administrador MASTER). Computador, janela 1280×800.

## Estado de partida (fim do T3 + mundo base)
Recicla Vale Metais com todos os módulos; a "Tabela Depósitos" e o material novo do T3 já existem; a tabela padrão é a
"Principal"; a preferência de várias tabelas de preço ligada (padrão do app). Parceiros do `MUNDO_FICTICIO.md` com o
histórico de agosto a 10/11 e os saldos da seção "Mundo" abaixo. Nenhuma nota fiscal emitida ainda (a primeira é do T16).

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área / título) | O que se mostra | Fala (s) |
|---|---|---|---|
| 0 | (sem vinheta) | Vinheta da EcoFlix; Dashboard; [ILUSTRAÇÃO: o pátio]; cartão "Antes: Materiais e tabelas de preço"; menu "Clientes e Fornecedores"; recolher o menu | 41 |
| 1 | PARCEIROS / Como a tela está organizada | Abas "Clientes", "Fornecedores", "Visão geral"; [ILUSTRAÇÃO: cliente × fornecedor]; linha com o saldo; busca, "Filtros", "Ordenar"; ficha ao lado; "Relatório", "Novo Cliente"; aviso de mesmo telefone e busca pelo número (dica ⚠️) | 72 |
| 2 | CADASTRO / Pessoa física e pessoa jurídica | "Novo Fornecedor": Rogério Alves Costa (nome, apelido, telefone, Pix, "Saldo inicial", CPF em "Pessoa Física"), "Salvar"; "Pessoa Jurídica" mostra CNPJ, razão social, inscrição estadual | 62 |
| 3 | CADASTRO / Buscar dados pelo CNPJ | Serralheria Bem-Te-Vi: CNPJ + lupa "Buscar dados da empresa pelo CNPJ" (simulada); razão social, nome fantasia, endereço, telefone e e-mail preenchidos; um campo vermelho | 42 |
| 4 | FISCAL / Dados fiscais e o campo vermelho | "Número" com "Não veio da Receita — obrigatório para emitir NF-e"; [ILUSTRAÇÃO: a nota leva o endereço]; número 418; inscrição estadual, indicador e regime (o contador define); "Salvar"; sinal verde × triângulo "Incompleto"; botão "<n> incompletos"; dica ⚠️ de quem não emite nota | 77 |
| 5 | SALDO / Cliente e fornecedor ao mesmo tempo | Editar a serralheria e marcar "Também é cliente"; selo "Cliente+Fornecedor"; Depósito Irmãos Siqueira; [ILUSTRAÇÃO: saldo unificado]; o mesmo saldo nas duas abas | 59 |
| 6 | PREÇOS / Tabela de preço do parceiro | Editar o depósito: "Tabela de Preços Padrão" → "Tabela Depósitos"; aviso azul do duplo; "Salvar"; [ILUSTRAÇÃO: qual preço vale na compra]; aba "Preços" | 44 |
| 7 | FICHA / A ficha do parceiro | Cooperativa Recomeço: cabeçalho, as 7 abas, "Visão geral", "Acesso ao portal" (🔒) | 36 |
| 8 | FICHA / Os materiais que ele mais movimenta | Aba "Pedidos": cartões, gráfico dos 5 materiais por peso; [ILUSTRAÇÃO: peso × valor]; "Período"; lista de pedidos | 37 |
| 9 | SALDO / Conta-corrente: saldo e extrato | "Saldo Atual" R$ 2.550,00 vermelho; [ILUSTRAÇÃO: os quatro casos do saldo] (dica ⚠️); extrato; "Movimentação": pagar R$ 1.200,00 por Pix; saldo R$ 1.350,00; "Exportar" | 76 |
| 10 | FICHA / Lucro estimado | "Mês passado"; latinha, papelão e o total; aviso "Estimativa — sucata é fungível..." (dica ⚠️); [ILUSTRAÇÃO: sucata é fungível] | 68 |
| 11 | FICHA / Financeiro e notas fiscais | Aba "Financeiro" (frete e sacos de ráfia); aba "Notas fiscais" vazia (🔒) | 34 |
| 12 | SALDO / Relatório de saldos | "Relatório de Saldos": "A Receber" e "A Pagar", os quatro casos devagar, o duplo uma vez só; "Exportar Relatório"; olho → conta-corrente da Aços Quiririm na ficha cheia | 67 |
| 13 | RESUMO / Recapitulando | Montagem do que foi feito; cartão "Próximo: Balança e impressora: o EcoTray"; cartela | 42 |

Transições faladas: 0→1 "Vamos ver como a tela está organizada"; 1→2 "Agora, cadastrar"; 2→3 "E o CNPJ tem um atalho" / "O
atalho é a busca pelo CNPJ"; 3→4 "repara que um campo ficou vermelho" / "O campo vermelho é o Número"; 4→5 "Agora, um caso
comum no pátio"; 5→6 "Agora, a tabela de preço"; 6→7 "Agora, a ficha"; 7→8 "Em Pedidos fica o resumo"; 8→9 "Agora, a
conta-corrente"; 9→10 "Agora, o Lucro estimado"; 10→11 "Agora, o Financeiro"; 11→12 "Pra fechar, a pergunta do dia a dia".

**Os cuidados da fonte na fala**
| Cuidado | Onde | Fala |
|---|---|---|
| ⚠️ Como ler o saldo (os 4 casos) | cap. 9 (regra + ilustração) e cap. 12 (os 4 casos na tela, um por frase) | "Uma dica: pra ler qualquer saldo, pensa sempre do lado da Recicla Vale. Verde é dinheiro pra receber. Vermelho é dinheiro pra pagar." |
| ⚠️ Lucro Estimado é estimativa | cap. 10, em cima do aviso fixo | "Uma dica: esse número é uma estimativa, não é dinheiro no bolso. O aviso da tela diz: sucata é fungível." |
| ⚠️ Selo de duplicidade (no código: "Mesmo telefone") | cap. 1, na lista de fornecedores | "Uma dica: muitas vezes é a mesma pessoa cadastrada duas vezes... Buscando pelo telefone, os dois aparecem juntos" |
| ⚠️ Quem não emite nota ignora Dados Fiscais | cap. 4, depois do incompleto | "Uma dica: quem não emite nota pode deixar a aba Dados Fiscais de lado. Só com o nome, o parceiro já tem histórico e saldo" |
| 🚫 Cliente = pra quem vende; fornecedor = de quem compra | cap. 1 (ilustração) | dito no positivo, sem dizer que o nome nunca muda (o app tem a opção de inverter, fora da aula) |
| 🔒 Portal e nota fiscal | cap. 7 e cap. 11 | "O portal depende do plano contratado." / "A emissão de nota depende do plano contratado" |

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (a conferir/consolidar pelo agente Mundo; os números abaixo estão na fala).

**Saldos em 10/11 08:30 (início do T4).** Só estes cinco diferentes de zero (os outros parceiros zerados):
| Parceiro | Saldo na linha | De onde vem | Na tela |
|---|---|---|---|
| Aços Quiririm Ltda (cliente) | +4.870,00 | venda no saldo em 05/11: ferro pesado 2.608 kg (3.260,00), chaparia 1.000 kg (980,00), ferro misto 600 kg (630,00) | verde, "a receber" |
| Serra Fina Alumínio Reciclagem (cliente) | −1.500,00 | adiantamento recebido por Pix em 06/11 pela próxima carga de alumínio | vermelho, "a pagar" |
| Cooperativa Recomeço (fornecedor) | +2.550,00 | compra de 06/11 (3.700,00) no saldo, menos Pix parcial de 1.150,00 em 09/11 | vermelho, "a pagar" |
| Valdir Pereira (fornecedor) | −300,00 | vale em dinheiro em 03/11 ("adiantamento a favor dele" lido como dinheiro adiantado a ele) | verde, "a receber" |
| Depósito Irmãos Siqueira (duplo, linha `party`) | −840,00 | compra no saldo em 06/11: ferro pesado 1.200 kg (1.140,00), ferro misto 320 kg (240,00), cobre misto 20 kg (720,00) = 2.100,00; venda no saldo em 05/11: papelão 1.250 kg (1.000,00) e plástico PET 100 kg (260,00) = 1.260,00 | vermelho nas duas abas ("-R$ 840,00" em Clientes, "R$ 840,00" em Fornecedores) |
Se o fiado parcelado da Fundição Bandeira do Vale (T13) virar saldo de parceiro, o total de "A Receber" do cap. 12 muda.

**Cooperativa Recomeço** (fornecedora PJ, completa para NF-e, com `portal_token`): 14 compras, uma por sexta de 07/08 a
06/11, a preço de tabela, forma "Saldo", cada uma paga por Pix na segunda seguinte (a de 06/11 só em parte, acima).
| Material | R$/kg | Ago (4) | Set (4) | Out (5) | 06/11 | Total |
|---|---|---|---|---|---|---|
| Papelão | 0,55 | 6.700 | 6.900 | 8.400 | 1.700 | 23.700 kg |
| Plástico PET | 1,90 | 2.050 | 2.150 | 2.600 | 520 | 7.320 kg |
| Alumínio latinha | 6,20 | 1.000 | 1.050 | 1.250 | 240 | 3.540 kg |
| Chaparia | 0,70 | 850 | 900 | 1.100 | 220 | 3.070 kg |
| Ferro misto | 0,75 | 700 | 750 | 900 | 180 | 2.530 kg |
| Valor | | 14.900,00 | 15.582,50 | 18.755,00 | 3.700,00 | 52.937,50 |
Na tela: "Total Comprado" R$ 52.937,50, "Total de Pedidos" 14, "Ticket Médio" R$ 3.781,25; gráfico "Papelão: 59%",
"Plástico PET: 18%", "Alumínio latinha: 9%", "Chaparia: 8%", "Ferro misto: 6%".
- Outubro precisa de **vendas** desses cinco materiais a preço de tabela (papelão 0,80 e PET 2,60 para o Depósito Irmãos
  Siqueira; latinha 7,40 para a Serra Fina; chaparia 0,98 e ferro misto 1,05 para a Aços Quiririm), todas pagas, para o
  preço médio de venda sair igual ao da tabela e sem o "*" de preço de cadastro. Lucro estimado de outubro: "Custo total
  comprado" R$ 18.755,00, "Margem estimada total" R$ 5.998,00, "Margem média %" 24,2%; linhas: papelão 0,25/kg e
  R$ 2.100,00 (31,3%), PET 0,70 e R$ 1.820,00 (26,9%), latinha 1,20 e R$ 1.500,00 (16,2%), chaparia 0,28 e R$ 308,00
  (28,6%), ferro misto 0,30 e R$ 270,00 (28,6%).
- Ligados à cooperativa: conta a pagar paga "Frete das entregas de outubro", R$ 450,00, vencimento 31/10 (categoria de
  frete do mundo); receita no caixa "Venda de sacos de ráfia usados", R$ 120,00, em 15/10 (outras receitas). Nenhuma nota.

**Duplicidade (novo no mundo base):** "Cida Ramos", fornecedora PF, cadastro repetido da Aparecida Ramos: mesmo telefone
(proposta (12) 90000-1102 nos dois, ou o que a Aparecida já tiver), sem CPF, sem endereço, uma compra paga em dinheiro em
18/09 (alumínio latinha 9 kg). Assim as duas ganham o selo "Mesmo telefone" (e não "Duplicado", que é por CPF/CNPJ).

**Aptidão fiscal no início:** Valdir Pereira, Aparecida Ramos e Cida Ramos incompletos (PF sem endereço); os PJ completos,
com código IBGE. Todos os parceiros com `portal_token`.

**Esta aula cria (vira o mundo das próximas):**
| Item | Valores |
|---|---|
| Rogério Alves Costa (cap. 2) | fornecedor PF, apelido "Rogério Eletricista", telefone (12) 90000-2611, Pix rogerio.costa@pix.example, CPF 418.273.560-90, sem endereço (fica "Incompleto"), saldo zero |
| Serralheria Bem-Te-Vi (cap. 3-4) | fornecedor PJ, nome digitado "Serralheria Bem-Te-Vi"; CNPJ 46.280.719/0001-24; da busca: razão social "BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA", nome fantasia "SERRALHERIA BEM-TE-VI", Rua das Palmeiras, (número em branco), Jardim Santa Luzia, Taubaté/SP (IBGE 3554102), CEP 12062-150, telefone (12) 90000-2742, e-mail contato@serralheriabemtevi.example, Simples Nacional; na tela: número 418, "Contribuinte ICMS", inscrição estadual 688412573032 (SP, dígitos conferidos) |
| Serralheria dupla (cap. 5) | cliente criado com os mesmos dados e vínculo `link_customer_supplier`; saldo único zero |
| Depósito Irmãos Siqueira (cap. 6) | "Tabela de Preços Padrão" = "Tabela Depósitos" (nos dois lados do duplo) |
| Pagamento (cap. 9) | Pix de R$ 1.200,00 à Cooperativa Recomeço, conta bancária principal, observação "Acerto parcial da entrega de 06/11", 10/11 ~08:35; saldo R$ 1.350,00 |
Saldos no fim: A Receber R$ 5.170,00 (Aços Quiririm 4.870,00; Valdir −300,00); A Pagar R$ 3.690,00 (Cooperativa 1.350,00;
Depósito −840,00; Serra Fina −1.500,00). A "Cida Ramos" continua no mundo (a aula só aponta).

## Gravação
- **Janela** 1280×800: a tela fica no modo compacto (altura ≤ 820 px): subtítulo escondido e selos da lista só com ícone
  (o robô passa o mouse para o tooltip). Menu lateral recolhido do cap. 1 em diante, no `setup` (botão de ícone do topo);
  no cap. 0 o recolher aparece com a fala. Sem celular, sem página pública, sem outro usuário, sem cena de Windows.
- **Rotas:** `/dashboard` (início do cap. 0), `/clientes-fornecedores`, e no fim do cap. 12 `/balance/customer/<id>` →
  `/saldo/...` → `/cliente/acos-quiririm-ltda-<código>?tab=conta-corrente`.
- **Sementes** (`seeds-extra/t04/`): `inicio` (caps. 0, 1, 2), `apos-cap02` (Rogério; caps. 3 e 4), `apos-cap04`
  (serralheria; cap. 5), `apos-cap05` (serralheria dupla; cap. 6), `apos-cap06` (tabela do depósito; caps. 7, 8, 9),
  `apos-cap09` (pagamento; caps. 10, 11, 12). Cada capítulo abre um navegador novo; o `setup` loga, recolhe o menu, abre
  `/clientes-fornecedores` e a aba do capítulo. O do cap. 4 refaz fora do vídeo o formulário do cap. 3 (Novo Fornecedor,
  nome, Dados Fiscais, Pessoa Jurídica, CNPJ, lupa) e para na aba Dados Fiscais com o "Número" vermelho.
- **Simular no backend falso** (`[BACKEND: ...]` no roteiro):
  1. Edge `cnpj-lookup`: para 46280719000124 devolve `{success: true, data: {...}}` com os dados acima (`numero: ""`,
     `cidade: "TAUBATE"`, `opcao_pelo_simples: true`, `opcao_pelo_mei: false`), com ~1 s de espera (a lupa gira).
  2. Edge `ibge-cities` (SP, com Taubaté 3554102) para a cidade casar e o código IBGE entrar.
  3. Selects com `ilike` "%d%i%g%i%t%o%s%" do telefone e do CPF/CNPJ (aviso de duplicado ao sair do campo; os números
     novos não batem com ninguém) e select do outro lado pelo `cpf_cnpj` (cap. 5).
  4. RPCs `set_partner_labels` (depois de cada salvar, lista vazia), `link_customer_supplier` (liga os dois e cria a linha
     `party`), espelho no cliente vinculado de nome, CPF/CNPJ, contato, endereço e tabela de preços padrão (cap. 6).
  5. Cap. 9: `cash_register` aberto (qualquer estado serve; a aula usa Pix), RPCs `create_manual_bank_transaction` e
     `update_balance`, `INSERT balance_movements` ("Valor Pago a Cooperativa Recomeço · Acerto parcial da entrega de 06/11").
  6. RPC `get_supplier_profit_estimate` (cap. 10) com as cinco linhas de outubro (`qty_bought`, `buy_value`,
     `avg_buy_price`, `qty_sold`, `avg_sale_price`, `sale_price_is_fallback: false`, `est_margin_unit`, `est_margin_total`).
  7. Embeds: `purchases` com itens e `materials(name)` (cap. 8); `cash_transactions` e `financial_bills` com
     `category:financial_categories(name, color)` e filtro `partner_type`/`partner_id` (cap. 11); `balances` com
     `balance_movements(created_at)` em ordem do mais novo, `.neq('balance', 0)` (cap. 12).
  8. "Visão geral" da tela (cap. 1): RPCs `get_financial_dre_summary`, `list_top_clients_paginated`,
     `list_top_suppliers_paginated`, `get_clients_suppliers_inactive_count` (período "Este mês").
- **[TESTAR antes de gravar]:** as 7 abas da ficha cabem na largura com o menu recolhido; o botão "<n> incompletos" aparece
  em 1280 px; a cidade "TAUBATE" vira "Taubaté" com o código IBGE depois da busca; a serralheria sai com o sinal verde;
  o olho do relatório chega na ficha cheia na aba da conta-corrente.
- **Ilustrações** (desenho por código no estilo da marca, `docs/09-aula-ilustrada.md`; nada de tela inventada): o pátio
  (cap. 0), cliente × fornecedor (1), a nota leva o endereço (4), saldo unificado (5), qual preço vale na compra (6), peso
  × valor (8), os quatro casos do saldo (9), sucata é fungível (10). Descrição e frase de cada uma no roteiro.
- **Não clicar:** "Abrir Relatório (PDF)", "Exportar em PDF/Excel" (abrem aba nova ou baixam arquivo): só o menu aberto.

## Riscos e decisões (padrão adotado; o Kaik muda se quiser)
1. **Ficha:** a fonte fala das 5 abas da página `/cliente/...`; no código 1.59.154 o clique na lista abre a ficha ao lado,
   com 7 abas e outros rótulos ("Pedidos", "Financeiro"...). A aula segue o clique da lista; a página cheia só aparece no
   olho do relatório (cap. 12).
2. **"Duplicado" × "Mesmo telefone":** no código, telefone igual dá o selo leve "Mesmo telefone"; "Duplicado" é por
   CPF/CNPJ. A aula usa o do código, com o cadastro repetido "Cida Ramos" no mundo.
3. **Valdir:** "adiantamento a favor dele" lido como vale dado a ele (ele deve R$ 300,00). Se for o contrário (crédito
   dele), troca o exemplo do fornecedor negativo.
4. **Nomenclatura:** sem dizer "nunca muda" (existe "Inverter os termos Cliente e Fornecedor" em Configurações).
5. **Nomes novos** (Serralheria Bem-Te-Vi, Rogério Alves Costa, Cida Ramos, Rua das Palmeiras, Jardim Santa Luzia, CEP
   12062-150): conferir na semente que não são de empresa ou pessoa real da região.
