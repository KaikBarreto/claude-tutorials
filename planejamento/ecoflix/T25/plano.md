# Plano · T25 · Dashboard, Agenda e rotina

- **Título:** Dashboard, Agenda e rotina (o da fonte). Arquivo: `EcoFlix T25 - Dashboard, Agenda e rotina.mp4`.
- **Antes:** T21 "Cato, o assistente". **Próximo:** as aulas dos módulos do plano (na ordem da trilha, a primeira é o T16,
  "Nota Fiscal de mercadoria (NF-e)"); cartão proposto "Próximo: os módulos do seu plano" (decisão 1).
- **Objetivo:** fechar a Formação básica lendo o Dashboard sem confundir margem com lucro, deixando o painel do jeito do dono,
  usando a Agenda (tarefas e avisos automáticos), os atalhos e o Ctrl+K, e montando as rotinas diária, semanal e mensal.
- **Duração:** alvo da fonte ~13 min; a fala fecha em ~10 min (ver `roteiro.md`). Só computador, um usuário (Rafael Nogueira).
- **Áreas das vinhetas:** DASHBOARD · AGENDA · ATALHOS · ROTINA · RESUMO.
- Base: `T25/inventario.md` (código 1.59.154). `FAKE_NOW` 2026-11-10T08:30:00-03:00 (terça).

## Capítulos (os 10 da fonte, na ordem, + abertura e recapitulação)

| # | Vinheta (área / título) | O que se mostra | Estado de partida |
|---|---|---|---|
| 0 | (sem vinheta) | Dashboard; ilustração do Rafael com as três perguntas do dia; destaque em "Dashboard" e "Agenda" no menu; cartão "Antes: Cato, o assistente". | `inicio` |
| 1 | DASHBOARD / Comprado, vendido e margem | Cartões em "Este mês" (margem de novembro alta e verde: o ferro de outubro vendido; junção); ilustração margem × lucro; filtro "Mês passado" (outubro, margem R$ 12.380,00); "Ver detalhes" → "Como é calculado". | `inicio` |
| 2 | DASHBOARD / Seis meses e o comparativo | "Compras vs Vendas (Últimos 6 Meses)" e "Evolução da Margem"; os comparativos "Mês Anterior" × "Mês Atual"; ilustração 31 dias × 10 dias. | `inicio` |
| 3 | DASHBOARD / Semanas e rankings | "Volume Semanal de Compras" (8 semanas, dica "Peso"); filtro "Mês passado"; "Materiais Mais Comprados" (R$ e Kg); "Principais Fornecedores"; "Principais Clientes" (R$ e Kg); "Ver todos os clientes". | `inicio` |
| 4 | DASHBOARD / O painel do seu jeito | "Configurações" → "Configurações do Dashboard": desliga "Métodos de Pagamento"; arrasta "Volume Semanal" para logo depois dos cartões; "Voltar ordem ao normal" em destaque. | `inicio` (layout padrão) |
| 5 | AGENDA / Tarefas no calendário | Menu "Agenda" (mês de novembro); "Nova Tarefa": "Revisão do caminhão FKD2E41", 12/11, 09:00, "Lembrar no dia"; "Salvar"; arrasta para o dia 13; feriados dos dias 15 e 20. | `inicio` → `apos-cap05` |
| 6 | AGENDA / Os avisos automáticos | "A Receber: R$ 4.790,00" (17/11) e "A Pagar: R$ 2.360,00" (23/11); clique → "Contas a Pagar/Receber"; dezembro: "Vencimento - Assinatura EcoSistema" (05/12); ilustração do fiado em parcelas; Dashboard com "1 lembrete para hoje". | `apos-cap05` |
| 7 | ATALHOS / Atalhos e o Ctrl+K | Ctrl+K, "cobre" → "Cobre mel" ("P. Compra" R$ 42,50, "P. Venda" R$ 47,90); "atalho" → "Ver Atalhos de Teclado" → "Atalhos de Teclado"; Shift+X (Caixa) e Shift+D (Dashboard). | `apos-cap05` |
| 8 | ROTINA / A rotina diária | Ilustração "10 min"; "Tarefas para hoje" ao abrir; Ctrl+K → "Histórico do Caixa" ("Caixas Fechados" de 09/11); "Contas a Pagar/Receber" ("Vence em 7 dias"); Agenda: amanhã, "Coleta na Auto Peças Vale Forte" 08:00. 🔒 Coletas citado. | `apos-cap05` sem a marca do lembrete diário |
| 9 | ROTINA / A rotina semanal | Ilustração "30 min"; Shift+E → "Estoque"; "Contas a Pagar/Receber" → aba "A Receber". | `apos-cap05` |
| 10 | ROTINA / A rotina mensal | Ilustração "2 h" com as quatro tarefas e as aulas; Agenda → dezembro → dia 1 → "Nova Tarefa" "Fechamento de novembro" com "Lembrar no dia". 🔒 notas fiscais citado. | `apos-cap05` → `apos-cap10` |
| 11 | RESUMO / Recapitulando | Montagem dos capítulos; cartão "Próximo: os módulos do seu plano"; cartela. | (montagem) |

Transições faladas: 0→1 "Vamos aos números"; 1→2 "Mais abaixo, os gráficos"; 2→3 "E quantos quilos entram por semana?"; 3→4 "E
dá pra deixar o painel do seu jeito"; 4→5 "Agora, a Agenda"; 5→6 "Além das tarefas"; 6→7 "Pra andar mais rápido"; 7→8 "Bom,
números lidos e agenda em uso: agora, a rotina"; 8→9 "Uma vez por semana"; 9→10 "E uma vez por mês, o fechamento"; 10→11
"Pronto! Recapitulando".

**Os ⚠️ da fonte e onde entram:**

| ⚠️ | Onde | Como |
|---|---|---|
| Margem (Vendas − Compras) não é lucro; o mês que vende o estoque comprado antes fica alto, e o de compra forte, baixo | cap01 | a margem de novembro, alta e verde na tela (o ferro de outubro), + "Uma dica:" + ilustração; outubro, o mês da compra, com margem pequena; o lucro "fica no Relatório Financeiro" |
| Gráfico sempre de 6 meses; o filtro manda nos cartões e rankings | cap02 | "Uma dica:" (vale para o código: 6 meses que terminam no fim do período) |
| Comparativo: mês passado inteiro × mês atual até hoje; queda grande no começo do mês | cap02 | "Uma dica:" + ilustração 31 × 10 dias |
| Agenda contando saldo e título duas vezes | cap06 | **não vale na 1.59.154** (o código abate o fiado dos títulos): a fala diz o positivo, "uma vez só, cada parcela no seu dia", e o clique que leva às Contas |
| 🔒 | cap08 (Coletas), cap10 (pacote contábil, MTR e CDF) | "depende do plano contratado", sem preço |
| "Propostas do marketplace" na rotina semanal | (fora) | o Marketplace está fora da trilha: sai da fala |

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)

**Começa com** o fim do T21 (o mundo depois do T13, T14 e T15). **Sementes:** `inicio`, `apos-cap05` (a revisão do caminhão
no dia 13), `apos-cap10` (o fechamento de novembro no dia 1º de dezembro = estado final; o T16 parte dele).

| Item | Valor |
|---|---|
| Dashboard, outubro ("Mês passado") | os números do T15: Total Compras **R$ 256.860,00**, Total Vendas **R$ 269.240,00**, Margem **R$ 12.380,00 (falado)**, verde |
| Rankings de outubro | os do T15: "Materiais Mais Comprados" 1º **Ferro pesado, 50.000 kg (falado)** (e 1º também em R$, R$ 47.500,00); "Principais Fornecedores" 1º **Depósito Irmãos Siqueira (falado)**; "Principais Clientes" 1º em R$ **Fundição Bandeira do Vale (falado)**, 1º em kg **Aços Quiririm Ltda (falado)** |
| Dashboard, novembro ("Este mês", 01 a 10/11) | junção (item 1, `MUNDO_LINHA_DO_TEMPO.md`): as 40 t de ferro pesado de outubro saem em novembro, então **vendas maiores que compras**: Total Compras R$ 18.781,45, Total Vendas R$ 118.620,20, Margem R$ 99.838,75, cartão verde (não falados); comparativos conforme a semente |
| Gráficos | 6 meses de junho a novembro (junho e julho zerados se o histórico começa em agosto); volume semanal das 8 semanas de 20/09 a 08/11 |
| Contas (do T13) | "A Receber: R$ 4.790,00" Fundição Bandeira do Vale em **17/11 (falado)**; "A Pagar: R$ 2.360,00" Auto Peças Vale Forte em **23/11 (falado)**; o resto do mundo pode aparecer |
| Assinatura | `subscription_expires_at` 2026-12-05 (o do T0): "Vencimento - Assinatura EcoSistema" no sábado, 05/12 **(falado)** |
| Agenda, semente | `schedule_tasks`: 10/11 14:00 "Cotação do cobre com a Fundição Bandeira do Vale" (Tarefa, "Lembrar no dia", pendente, criada pelo Rafael); 11/11 08:00 "Coleta na Auto Peças Vale Forte" (Coleta, fornecedor Auto Peças Vale Forte, "Lembrar no dia", pendente; junção: o lembrete da ordem 9 que a T12 agenda pra 11/11 de manhã) **(falado)** |
| Agenda, criada ao vivo | cap05: "Revisão do caminhão FKD2E41" (Tarefa, 12/11 09:00 → **13/11**, "Lembrar no dia"); cap10: "Fechamento de novembro" (Tarefa, 01/12 08:00, descrição "Conciliar o banco, conferir o DRE, mandar o pacote ao contador e ver MTR e CDF pendentes", "Lembrar no dia") |
| Feriados | `company_fiscal_config` com `cidade` "Taubaté", `uf` "SP": novembro mostra "Finados" (02), "Proclamação da República" (15) e "Consciência Negra" (20) |
| Histórico do Caixa | os caixas fechados de 09/11 do histórico base (sem números falados) |
| Material | "Cobre mel" com `purchase_price` 42,50 e `sale_price` 47,90 **(falado)** |
| Usuário | Rafael (MASTER, `full_access`); `user_shortcuts.shortcuts_enabled` true; `navigation_style` sidebar |
| `localStorage` por capítulo | `daily-tasks-reminder-last-shown-<id do Rafael>` = 2026-11-10 em todos os capítulos **menos o 8** (lá ele abre); `dashboard-layout-v2-<id>` vazio (layout padrão); `agenda-show-holidays` vazio (feriados ligados) |

## Gravação

- **Rotas:** `/dashboard`, `/agenda`, `/contas-pagar-receber`, `/historico-caixa`, `/materiais`, `/caixa` (só a abertura pelo
  Shift+X). Computador 1280×800 ou maior (a lateral da Agenda só aparece a partir de 1280 px). Sem celular, sem página
  pública, um usuário só, nada de Windows nem EcoTray.
- **RPCs a simular:** `get_financial_dre_summary` (regime caixa; "Este mês", "Mês passado" e as duas janelas do comparativo),
  `get_monthly_purchases_sales` (`p_months` 6), `get_dashboard_operacao` (`weeklyVolume`), `get_orders_payment_distribution`,
  `get_top_materials`, `get_top_partners`, `list_top_clients_paginated`, `get_dre_expenses_by_group`, e as da tela de Contas do
  T13 (`generate_due_recurring_bills` e as leituras).
- **Tabelas:** `schedule_tasks` (insert no cap05 e no cap10; update do `scheduled_date` no arrasto), `financial_bills`, `balances`,
  `suppliers` (`linked_customer_id`), `companies`, `company_fiscal_config`, `user_shortcuts`, e as da busca do Ctrl+K
  (`customers`, `suppliers`, `balances`, `materials`, `employees`).
- [TESTAR] o arrasto do Dashboard (dnd-kit, ponteiro, 8 px antes de pegar: apertar, mover devagar, soltar) e o da Agenda (arrasto
  nativo do navegador, `dragstart`/`drop`); o clique num aviso compacto do mês levando às Contas; o Ctrl+K não cair no atalho do
  navegador (a lista de atalhos abre pelo Ctrl+K, "Ver Atalhos de Teclado": o "?" não abre nada na 1.59.154).
- **Ilustrações** (`docs/09-aula-ilustrada.md`): cap00 (as três perguntas do dia); cap01 (margem × lucro: o ferro parado no
  estoque); cap02 (31 dias × 10 dias); cap06 (uma venda a prazo virando três parcelas, cada uma num dia); cap08, cap09, cap10 (as
  rotinas com o relógio e os itens, cada item com a etiqueta da sua aula); cap11 (as três rotinas juntas).

## Decisões tomadas (padrão; o Kaik muda se quiser)
1. **Cartão "Próximo:"** "os módulos do seu plano" (a fonte não nomeia aula; a próxima de verdade depende do plano de cada
   cliente). Alternativa: "Próximo: Nota Fiscal de mercadoria (NF-e)".
2. **Números falados só os que outra aula já fixou** (outubro e os rankings do T15, as contas do T13, os preços do mundo); os de
   novembro aparecem na tela e não são falados, porque dependem de tudo o que as aulas anteriores lançam no dia.
3. **⚠️ da contagem dupla na Agenda fora da fala** (o código corrigiu); a dica positiva fica.
4. **A rotina mensal vira uma tarefa na Agenda** ("Fechamento de novembro"), para a rotina ficar "definida" no sistema.
