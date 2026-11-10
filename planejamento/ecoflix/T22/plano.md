# Plano · T22 Gerencial: matriz e filiais

- **Título:** Gerencial: matriz e filiais (o da fonte). 🔒 **Módulo Gerencial** (`modulo_gerencial`), contratado na matriz.
- **Objetivo:** a matriz da Recicla Vale Metais (Taubaté) passa a enxergar a filial de Pindamonhangaba: cria o grupo, vincula a
  filial pelo código, lê o Dashboard, a DRE do grupo nos dois regimes e o estoque, padroniza o catálogo, transfere material com
  aprovação e paga as duas assinaturas numa fatura só.
- **Antes:** Relatório Financeiro e DRE (T15). **Próximo:** Coletas e Logística (T12, "o caminhão saindo do pátio pra buscar
  material").
- **Vinhetas (áreas):** GERENCIAL · GRUPO · FILIAL · DASHBOARD · DASHBOARD · FINANCEIRO · FINANCEIRO · ESTOQUE · PADRONIZAÇÃO ·
  TRANSFERÊNCIAS · ASSINATURAS · RESUMO.
- **Alvo da fonte:** 16 min. **Fala:** 1.410 palavras, ~9 min de voz + 12 vinhetas, as ilustrações e as esperas (≈ 12 min de
  vídeo; a fala fecha abaixo da fonte, como na Domiflix).
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` em todos os capítulos. Desktop 1280×800, menu lateral aberto. Logado: Rafael Nogueira
  (matriz) em todos, menos o **cap. 3**, gravado como **Sandra Pires** (gerente da filial, outro usuário).
- Base: `T22/inventario.md` (código 1.59.154).

## Capítulos (os da fonte, na ordem)

| # | Vinheta (área / título) | O que a tela mostra | Cuidados falados | Fala |
|---|---|---|---|---|
| 0 | (sem vinheta) | Menu "Gerencial (Filiais)" aberto; [ILUSTRAÇÃO: somar na mão] | 🔒 contratado na matriz · "Antes: Relatório Financeiro e DRE" | 0:35 |
| 1 | GERENCIAL / Como o Gerencial funciona | "Módulo Gerencial" (sem grupo); [ILUSTRAÇÃO: matriz × filial, em 3 tempos] | ⚠️ cada unidade é empresa própria; ⚠️ junta e padroniza, quem opera a filial é a filial | 0:50 |
| 2 | GRUPO / Criar o grupo e o código | "Configurar Grupo" → "Grupo Recicla Vale" → "Criar Grupo"; abas; "Código de Convite" GRP-7KQ4TX, "Válido até 10/12/2026", copiar; "Unidades Ativas" só com a matriz | código vale 30 dias | 1:00 |
| 3 | FILIAL / Do lado da filial | Sandra Pires: "Configurações" › "Empresa" › "Filial" → "É Filial" → código → "Vincular" → "Vinculada ao grupo"; [ILUSTRAÇÃO: o código liga as unidades] | | 0:45 |
| 4 | DASHBOARD / O Dashboard Gerencial | "Dashboard Gerencial", "Mês passado", "Todas as Unidades", cartões "Receita Total" e "Despesa Total", "Estoque Total", gráfico por unidade | (sem citar o "Lucro Líquido": risco 1) | 0:55 |
| 5 | DASHBOARD / Ranking e resumo por unidade | "Ranking por Lucro"; "Resumo por Unidade" (matriz -R$ 27.650,00 -10.2%; filial R$ 1.000,00 1.4%); [ILUSTRAÇÃO: a compra que ainda está no pátio] | | 0:55 |
| 6 | FINANCEIRO / A DRE do grupo | "Financeiro" › "DRE" › "Consolidado" em "Regime de Caixa" (vendas 341.240, compras 318.860, resultado -26.650); "Comparativo" (-27.650 + 1.000) | | 1:00 |
| 7 | FINANCEIRO / Caixa e competência | "Regime de Competência" (CMV 273.860, Lucro Bruto 64.980, resultado 18.350); [ILUSTRAÇÃO: caixa × competência]; [ILUSTRAÇÃO: o aviso do material sem custo] | ⚠️ "o CMV pode estar subestimado" | 1:10 |
| 8 | ESTOQUE / O estoque do grupo | "Visão Geral" (latinha 640 + 1.850 = 2.490 kg), "Posição de Estoque", "Histórico de Materiais", "Relatório de Estoque" | | 0:55 |
| 9 | PADRONIZAÇÃO / Enviar Ativos | "Importar do Estoque da Matriz"; tabelas e categorias entram sozinhas; marca a Fundição Bandeira do Vale; "Enviar Ativos" → "Confirmar Envio"; lixeira | ⚠️ remover por engano não apaga nada | 1:15 |
| 10 | TRANSFERÊNCIAS / Transferência com aprovação | Liga "Exigir aprovação em transferências"; "Nova": filial → matriz, alumínio latinha 1.200 kg → "Solicitar" → "Pendente" → "Executar" → "Confirmar e Executar" → "Concluída"; [ILUSTRAÇÃO: um material do grupo, dois da unidade] | ⚠️ o total do grupo soma N materiais, a transferência tira de um | 1:20 |
| 11 | ASSINATURAS / Assinaturas numa fatura só | "Assinaturas do grupo"; "Pagar tudo de uma vez"; aviso das cobranças canceladas; "PIX"; "Pagamento Confirmado!" | ⚠️ a filial não paga mais o boleto ou Pix antigo (dito com todas as letras) | 1:00 |
| 12 | RESUMO / Recapitulando | Montagem; cartão "Próximo: Coletas e Logística" | | 0:40 |

Transições faladas: 0→1 "Vamos entender como ele funciona"; 1→2 "Começando pela matriz"; 2→3 "Agora do lado da filial"; 3→4 "De volta
à matriz"; 4→5 "E o ranking"; 5→6 "Agora o Financeiro"; 6→7 "Agora o mesmo outubro em regime de competência"; 7→8 "Agora o
estoque"; 8→9 "Agora a padronização"; 9→10 "Agora as transferências"; 10→11 "Por último, as assinaturas".

## Estado de partida (semente `inicio`)
Mundo base + o bloco abaixo; **sem grupo** (`company_groups` vazio). A filial já opera há meses no sistema dela, com assinatura e
dados próprios.

## Mundo: o que esta aula precisa
**Empresas**
- Matriz: "Recicla Vale Metais" (Taubaté/SP), CNPJ **47.318.506/0001-07** (o do T1; junção); plano "Personalizado" · "Mensal" · "Ativa", com o módulo Gerencial; CNPJ gravado (o checkout não pede documento).
- Filial: nome no sistema **"Filial Pindamonhangaba"** (razão "Recicla Vale Metais Ltda", CNPJ **47.318.506/0002-98** (mesma raiz da matriz; junção),
  Pindamonhangaba/SP), plano próprio sem o Gerencial (ex.: "Avançado") · "Mensal" · "Ativa" · vence em 15/11/2026. O nome curto evita
  que os gráficos e o comparativo cortem as duas como "Recicla Vale…" (risco 3).
- Usuária da filial: **Sandra Pires**, gerente, MASTER da filial, `sandra.pires@reciclavalemetais.example` (domínio do T2, junção).

**Grupo (criado na aula):** "Grupo Recicla Vale"; RPC `generate_group_invite_code` devolve **GRP-7KQ4TX**, válido até 10/12/2026;
`require_transfer_approval` desligado ao criar (liga no cap. 10). Vínculo da filial em 10/11/2026 (cap. 3).

**Números de outubro (período "Mês passado"; setembro só para as setinhas):**

| | Vendas | Compras | CMV (competência) | Despesas da operação | Receita / Despesa no Dashboard | Lucro | Margem |
|---|---|---|---|---|---|---|---|
| Recicla Vale Metais | 269.240,00 | 256.860,00 | 218.860,00 | 36.855,90 | 272.040,00 / 299.690,00 | -27.650,00 | -10.2% |
| Filial Pindamonhangaba | 72.000,00 | 62.000,00 | 55.000,00 | 9.000,00 | 72.000,00 / 71.000,00 | 1.000,00 | 1.4% |
| Grupo | 341.240,00 | 318.860,00 | 273.860,00 | 45.855,90 | 344.040,00 / 370.690,00 | -26.650,00 | |

Junção (`MUNDO_LINHA_DO_TEMPO.md`): a matriz é a Recicla Vale do T15, com o outubro da semente (sem a energia em dobro, que só
existe no estado do T15): vendas 269.240,00, compras 256.860,00, CMV 218.860,00, frete 2.400,00 ("Custos adicionais"), impostos
3.574,10 ("(-) Impostos e Deduções"), despesas da operação 36.855,90 e aluguel de caçamba 2.800,00 ("(+) Outras Receitas"). No
Dashboard, receita = vendas + outras receitas e despesa = compras + frete + impostos + despesas da operação. A filial não tem frete,
impostos nem outras receitas. DRE do grupo: caixa = Resultado de Caixa 19.980,00 ("Margem Bruta: 5.9%") e Resultado do Período
-26.650,00 ("Déficit"); competência = Lucro Bruto 64.980,00 ("Margem Bruta: 19.0%") e Resultado do Período 18.350,00 (diferença
45.000,00 = compras − CMV: 38.000,00 do ferro pesado parado na matriz e 7.000,00 na filial). Estoque com custo em todas as
entradas (`stockCostReliable` verdadeiro: o aviso do CMV não aparece). Setembro (só para as setinhas): a matriz com o setembro da
semente (vendas 273.047,73, compras 201.784,25); filial 66.000,00, 57.000,00, 9.000,00.

**Estoque (10/11):** a filial tem os 15 materiais do mundo com os mesmos nomes (cadastro dela), sem o "Radiador de cobre" do T3.
**Alumínio latinha: matriz 640 kg (o estoque de 10/11 do mundo base, junção), filial 1.850 kg** (depois da transferência do cap. 10: 1.840 e 650). Histórico de novembro
(03 a 09/11) com algumas compras e vendas nas duas unidades.

**Padronização (cap. 9):** a matriz tem as tabelas de preço do mundo (a "Tabela Depósitos" do T3 e a principal) e as categorias
financeiras; "Fundição Bandeira do Vale" é cliente das duas unidades. O envio liga os materiais de mesmo nome da filial ao catálogo
do grupo e cria só o que faltava (junção: no mundo base as duas têm os mesmos 15 materiais; o "Radiador de cobre" só existe na T3).

**Transferência (cap. 10):** "Alumínio latinha", 1.200 kg, origem "Filial Pindamonhangaba", destino "Recicla Vale Metais", observação
"Lote para a Serra Fina Alumínio Reciclagem".

Anotar no `MUNDO_FICTICIO.md`: a filial (nome, CNPJ, plano, Sandra Pires), o grupo e o código, os números de outubro.

## Gravação
- Rotas: `/gerencial`, `/gerencial/configuracoes`, `/gerencial/financeiro`, `/gerencial/estoque`, `/gerencial/assinaturas`,
  `/checkout?mode=group&group=<id>`; cap. 3: `/configuracoes` (aba "Empresa") no login da filial.
- Sementes: `inicio` (caps. 0 a 2), `apos-cap02` (grupo criado; entrada do 3), `apos-cap03` (filial vinculada; entrada dos caps. 4 a
  9), `apos-cap09` (catálogo, tabelas, categorias, parceiro marcado e envio feito), `apos-cap10` (aprovação ligada e transferência
  concluída), `apos-cap11` (pagamento do grupo confirmado).
- RPCs a ter no backend falso: `generate_group_invite_code`, `get_group_members_with_names`, `regenerate_group_invite_code`,
  `join_group_by_invite_code`, `get_group_branch_stock_settings`, `get_group_financial_summary`, `get_group_stock_summary`,
  `get_group_expense_categories`, `get_group_financial_dre_summary` (com `_regime` e `cmv`), `get_group_patrimony_summary`,
  `get_dre_expenses_by_group`, `get_group_inventory_report_data` (e as das abas Posição, Histórico e Relatório),
  `import_owner_materials_to_group`, `import_owner_price_table_to_group`, `toggle_group_shared_entity`,
  `import_company_categories_to_group`, `push_group_assets_to_company`, `create_group_transfer_and_execute`,
  `execute_group_stock_transfer`, `get_group_subscription_summary`, `group_expected_payment`. Tabelas: `company_groups`,
  `company_group_members`, `group_materials` (e vínculos), `group_price_tables`, `group_shared_entities`,
  `group_financial_categories`, `group_push_audit`, transferências do grupo.
- Integrações a simular: edge `create-group-payment` (devolve um Pix fictício, nada vai para o Asaas) e um passo de bastidor que
  confirma o pagamento (o checkout passa a "Pagamento Confirmado!"). Área de transferência liberada no navegador (copiar o código).
- Outro usuário: cap. 3 com `user` = Sandra Pires (filial).
- Ilustrações (`docs/09-aula-ilustrada.md`, estilo da marca): somar na mão (0); **matriz × filial** em três tempos (1: o grupo; 2:
  números sobem, catálogo desce, transferência; 3: o cadeado na operação da filial); o código liga as unidades (3); a compra que ainda
  está no pátio (5); **caixa × competência** (7); o aviso do material sem custo (7); um material do grupo, dois da unidade (10).
- Zoom: o código de convite, os cartões de receita e despesa, as linhas do resumo, as linhas da DRE, a linha do alumínio, a
  quantidade da transferência, o aviso das cobranças. Sem zoom no cartão "Lucro Líquido" nem nos valores das assinaturas.

## Riscos, decisões e handoffs
1. **"Lucro Líquido" do Dashboard = vendas − compras** (`GerencialDashboard.tsx:216,251-258`): não fecha com "Receita Total" − "Despesa
   Total" nem com a soma do "Lucro" da tabela (receita − despesa). A fala não cita o cartão. Handoff.
2. **"Compras (CMV)" do Comparativo mostra as compras nos dois regimes** (`GerencialFinanceiro.tsx:1102`): em competência, o
   "Resultado" por unidade não soma o do consolidado. Decisão: o cap. 6 liga "Regime de Caixa" antes de abrir o Comparativo. Handoff.
3. Nomes cortados em 15 letras nos gráficos e em 12 no Comparativo: com "Recicla Vale Metais Pindamonhangaba", as duas unidades
   apareceriam como "Recicla Vale…". Decisão: a filial se chama "Filial Pindamonhangaba" no sistema. Handoff (tooltip ou nome curto).
4. **Fonte × código:** a matriz consegue "Corrigir saldo" do estoque de uma unidade pela Visão Geral (`GroupAdjustStockDialog.tsx`);
   o ⚠️ "não é operação" vale para caixa, compras e notas, e a fala diz exatamente isso.
5. "Remover unidade?" diz "você perderá acesso aos dados dela"; remover só muda o `status` (nenhum dado apagado,
   `useCompanyGroup.ts:137-150`). A volta pelo código (RPC `join_group_by_invite_code`) não está nesta cópia do código: a fala segue
   a fonte; conferir no SQL do app real.
6. Assinaturas e checkout mostram valores de plano: na tela como estão, sem fala nem zoom.
