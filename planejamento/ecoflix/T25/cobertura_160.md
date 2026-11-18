# Cobertura 1.60.10 · T25 · Dashboard, Agenda e rotina

Base: roteiro e inventário (1.59.154, `f37573ea0`) contra `/dev/shm/ecoflix-src` (1.60.10, `5290be4cd`). Caminhos relativos
a `src/`. Só leitura de código; sem navegador, sem robô. Não existe `rec/varredura/t25.txt` ainda.

**Resumo:** as telas próprias da aula **não mudaram** entre as duas versões (diff vazio em `pages/Dashboard.tsx`,
`pages/Agenda.tsx`, `components/dashboard/*`, `components/agenda/*`, `hooks/useDashboardLayout.ts`,
`hooks/useScheduleTasks.tsx`, `hooks/useKeyboardShortcuts.tsx`, `components/CommandPalette.tsx`,
`components/KeyboardShortcutsModal.tsx`, `components/DateRangeFilter.tsx`, `components/settings/SettingsShortcutsContent.tsx`,
`utils/holidays.ts`, `pages/CashHistory.tsx`, `i18n/locales/pt-BR/*`, `components/financial-report/FinancialDRE.tsx`,
`components/BalancesReportModal.tsx`). As linhas do `inventario.md` continuam valendo. O que mudou está nas telas
emprestadas (Contas a Pagar/Receber e o menu). O trabalho grande é a seção 2: o que o roteiro nunca mostrou.

## 1. Mudou no app

| # | Cap. | O que o roteiro mostra | Como está no 1.60.10 | Arquivo:linha |
|---|---|---|---|---|
| M1 | cap09 (aba "A Receber") | Os quatro cartões de sempre no alto da tela de Contas | Na aba "A Receber" o 1º cartão vira **"Total a Receber"** e o 2º vira **"Total recebido"**; na aba "A Pagar", **"Total a Pagar"** e **"Total pago"**. Em "Todas" segue "Total a Pagar" e "Total a Receber". "Vencidas" e "Vence em 7 dias" não mudam. Com período de vencimento ligado os rótulos viram "A receber no período", "Recebido no período", "A pagar no período", "Pago no período". A fala do cap09 não cita esses cartões: muda só a imagem (regravar o trecho; [TESTAR] o destaque do robô, se ele mira o cartão pela posição). | `components/contas/BillsSummaryCards.tsx:110-135,156,166` |
| M2 | cap08 e cap09 (Contas) | Filtros da tela sem atalho de período | No painel de filtros, em "Vencimento (período)", três botões novos: **"Este mês"**, **"Próximos 7 dias"**, **"Até o fim do mês"**. O roteiro não abre os filtros; ver L17. | `pages/ContasPagarReceber.tsx:1376-1378` |
| M3 | cap00, cap05, cap08 (menu lateral em quadro) | "Fiscal & Ambiental" com 5 filhos | Ganhou o 6º filho **"Relatórios Fiscais"**, e "Estoque Fiscal" agora abre em `/fiscal-ambiental/estoque-fiscal/posicao`. Só aparece se o menu estiver expandido no quadro; a fala não é afetada (T16 a T18 tratam). | `config/routes.ts:510-511` |
| M4 | cap09 (tela "Estoque") | Lista de materiais | `pages/Materiais.tsx` mudou só na parte de tabelas de preço ("Duplicar tabela", "Fixar para meus pedidos e tickets", "Definir como principal"), que é da T3. A lista de saldos que o cap09 mostra não mudou. Nada a fazer aqui. | `pages/Materiais.tsx` (diff) |

Sem mudança visível: `pages/Caixa.tsx` (Shift+X do cap07; só consulta interna), `components/layout/AppLayout.tsx` (idioma do
perfil e barra do celular), `SettingsUsabilityContent.tsx` na seção "Agenda" → "Exibir Feriados" (o diff é de "Assinaturas
no comprovante", da T7/T8).

Continuam valendo os achados do inventário: o "?" não abre a lista de atalhos (o hook segue sem montar); "Agenda" e "Contas
a Pagar/Receber" seguem fora da "Navegação" do Ctrl+K (`CommandPalette.tsx:93-123`); a janela "Configurações do Dashboard"
ainda diz "Card Lucro", "Evolução do Lucro" e "Comparativo Mensal - Lucro" (`hooks/useDashboardLayout.ts:26,28,32`).

## 2. Falta cobrir

### Dashboard

| # | O que é (rótulo exato) | Quando o cliente usa | Vale? |
|---|---|---|---|
| L1 | Filtro de período completo: "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias", "Este ano", **"Personalizado"** (abre o seletor de datas) (`components/DateRangeFilter.tsx:426-450`). O roteiro só usa "Este mês" e "Mês passado". | Ver o dia, a semana ou um intervalo qualquer (ex.: a quinzena). | **Sim, trecho** no cap01 (abrir a lista e ler; sem escolher, para não pedir número novo). |
| L2 | "Ver detalhes" de **"Total de Compras"** e **"Total de Vendas"** (`components/dashboard/StatDetailModal.tsx:67-68`): "Total no período", "Comparativo mensal" ("Mês anterior", "Mês atual", "vs. mês anterior") e, só nas compras, **"Por forma de pagamento"** (`:257`). O roteiro abre só o da margem. | Saber quanto das compras saiu em dinheiro, Pix ou saldo. | **Sim, trecho** no cap01 (uma frase, abrindo o de compras). |
| L3 | **"Saldos em Aberto"** (`pages/Dashboard.tsx:1643`): colunas "A receber" (verde) e "A pagar" (vermelho) com os 5 maiores parceiros de cada lado, "Ver mais (n)" quando passa de 5, "Sem saldos" quando vazio, **"Posição líquida"** no rodapé (+ verde, − vermelho) (`:303-383`) e o link **"Ver relatório"** (`:1652`), que abre "Relatório de Saldos" · "Visualize todos os saldos a receber e a pagar", com "Exportar Relatório" → "Exportar em PDF" / "Exportar em Excel" (`components/BalancesReportModal.tsx:240-274`). Não segue o filtro de período (é o saldo de hoje). | Todo dia: quem me deve e a quem eu devo, sem sair do painel. | **Sim, capítulo novo** (P2). O "Relatório de Saldos" por dentro é da T4: aqui só abrir e apontar. |
| L4 | **"Métodos de Pagamento das Compras"** (`:1693`): pizza com a % e o valor de cada forma ("Dinheiro", "Pix/Transferência", "Saldo", "Cartão", "Cheque", "Outro"); segue o filtro; "Sem dados" quando vazio. O cap04 só desliga a chave, sem explicar o cartão. | Saber quanto dinheiro vivo o pátio precisa ter para comprar. | **Sim**, no capítulo novo P2. |
| L5 | **"Demonstrativo Financeiro (DRE)"** no fim do painel, com o seletor **"Regime de Caixa"** / **"Regime de Competência"** (`components/financial-report/FinancialDRE.tsx:1378,1401`; começa em caixa, `pages/Dashboard.tsx:421`) e as dicas de cada regime ao passar o mouse (`FinancialDRE.tsx:1381-1385,1404-1408`). Sem "Exportar" no painel (`showExport={false}`, `Dashboard.tsx:1511`). | Ver o resultado do período sem abrir o Relatório Financeiro. | **Só citar** (uma frase em P2: "é o mesmo da aula do Relatório Financeiro"). O conteúdo é da T15. [TESTAR] se trocar o regime mexe nos três cartões do topo (a consulta dos cartões leva o regime, `Dashboard.tsx:501-518`). |
| L6 | Clicar num nome do pódio de "Principais Fornecedores" ou "Principais Clientes" abre o **histórico do parceiro** (`Dashboard.tsx:1988,2071`). | Do ranking direto para a ficha de quem mais vende ou compra. | **Sim, trecho** no cap03 (uma frase). A ficha é da T4. |
| L7 | Janela "Todos os clientes" / "Todos os fornecedores": seletor **"Por Valor (R$)"** / **"Por Quantidade (kg)"**, "Período: …", "{n} no período", "Anterior", "Próximo", "Página {x} de {y}" (`components/dashboard/TopEntitiesDialog.tsx:191-202,314`). O roteiro abre e fecha. | Lista completa do mês, por valor ou por peso. | **Sim, trecho** no cap03 (uma frase com o seletor). |
| L8 | Usuário sem permissão de ver valores: os cartões e gráficos mostram **"Sem permissão"** / "Sem permissão para visualizar" (`Dashboard.tsx:186,195`), e "Ver detalhes" some. | Operador de balança abre o painel e não vê os números. | **Só citar** no cap04 (uma frase); a permissão é da T2. |
| L9 | "Compra de balcão" aparece nos rankings como **"Sem cadastro"** (achado do robô em `propostas_fala.md`). | Entender a linha estranha no ranking. | **Só citar** no cap03, se a semente tiver compra sem cadastro em outubro; senão não. |
| L10 | Cartões de topo que não são do painel: aviso de vencimento da assinatura (`SubscriptionExpirationCard`), convite de avaliação (`GoogleReviewCard`, dispensa permanente) e "Retomar tour" (`features/onboarding/OnboardingProgressCard.tsx:62`). | Aparecem sozinhos. | **Não.** Assinatura e tour são da T0; a avaliação não é função. Garantir que não apareçam na gravação. |
| L11 | No celular os cartões e os comparativos viram carrossel (`Dashboard.tsx:2166-2225`); "Configurações" vira só ícone. | Dono olhando o painel no celular. | **Não** (o plano definiu aula só de computador). |

### Agenda

| # | O que é | Quando o cliente usa | Vale? |
|---|---|---|---|
| L12 | **Concluir tarefa**: o círculo à esquerda da tarefa, na lateral do dia (`components/agenda/TaskCard.tsx:147-165`); a tarefa fica riscada e, no mês, com "✓ Concluída" (`:103`); clicar de novo volta a pendente (`pages/Agenda.tsx:165-170`); toast "Tarefa atualizada". Só as pendentes entram em "Tarefas para hoje" e na faixa do Dashboard (`AgendaReminders.tsx:22`). | Todo dia: dar baixa no que foi feito; a tarefa de hoje concluída sai da faixa do Dashboard e de "Tarefas para hoje" (as de dias passados não voltam: os dois só olham a data de hoje). | **Sim, capítulo novo** (P3). É a maior lacuna: a aula ensina a criar e nunca a concluir. |
| L13 | **Editar**: clique na tarefa (no mês) ou no lápis (na lateral) abre **"Editar Tarefa"** (`TaskCard.tsx:41,212`; `TaskFormDialog.tsx:251`). **Excluir**: a lixeira → "Excluir Tarefa" · "Tem certeza que deseja excluir esta tarefa?" · "Cancelar" / "Excluir Tarefa" (`Agenda.tsx:268-274`); toast "Tarefa excluída" (`hooks/useScheduleTasks.tsx:508`). Lápis e lixeira só aparecem ao passar o mouse. | Mudou o horário, ou a tarefa foi marcada errado. | **Sim**, em P3. |
| L14 | Vistas **"Dia"** e **"Semana"**, botão **"Hoje"**, setas e o seletor de mês no título (`components/agenda/AgendaCalendar.tsx:223-290`). O roteiro só usa "Mês" e a seta. | Semana cheia de coletas: ver por horário. | **Sim**, em P3 (uma passada por "Semana" e volta com "Hoje"). |
| L15 | **Duplo clique num dia** abre "Nova Tarefa" já naquela data (`AgendaCalendar.tsx:320,383`; `Agenda.tsx:135-139`). | Atalho para marcar rápido. | **Sim**, em P3 (uma frase). |
| L16 | Categoria **"Coleta"** com o campo **"Cliente / Fornecedor"** ("Selecionar...", busca "Buscar por nome, apelido, CPF/CNPJ ou telefone...", "Remover seleção") (`TaskFormDialog.tsx:318-400`), e a "Legenda:" das cores no rodapé. A semente tem uma coleta, mas a aula nunca mostra como se cria. | Marcar retirada num fornecedor sem ter o módulo de Coletas. | **Sim**, em P3 (abrir a tarefa da coleta em "Editar Tarefa" e apontar os dois campos; sem salvar). |
| L17 | Cartão que abre ao passar o mouse na tarefa do mês: categoria, título, descrição, data, hora, parceiro e "🔔 Lembrete ativo" (`TaskCard.tsx:64-118`). | Ler a tarefa sem abrir. | **Só citar** em P3 (aparece sozinho quando o robô passa o mouse). |
| L18 | **"Notificação push"** (chave no formulário). No front a chave só é gravada (`notify_push`); não há leitura dela em nenhuma tela desta cópia. | (não dá para afirmar pelo código) | **Não falar** até confirmar o que ela faz no servidor (decisão 2). |
| L19 | Tarefas do CRM na Agenda ("Tarefa de CRM", "Abrir oportunidade →"; concluem aqui, editam só no CRM) (`TaskCard.tsx:33-40,133-142`). | Quem tem o módulo de CRM. | **Não**: é da T26. |

### Atalhos e Ctrl+K

| # | O que é | Quando o cliente usa | Vale? |
|---|---|---|---|
| L20 | Ctrl+K achando **parceiro**: o painel mostra o tipo, telefone e **"Saldo"** (`CommandPalette.tsx:199`), e Enter abre o **histórico do parceiro**; material abre "Estoque" já no item; funcionário mostra "Cargo" (`:455-500`). O roteiro só busca material. | Cliente no telefone perguntando quanto deve. | **Sim, trecho** no cap07. |
| L21 | Grupo **"Ações Rápidas"**: "Nova Compra", "Nova Venda", "Abrir Caixa" (`:684`); compra e venda pedem o caixa se nenhum estiver escolhido (`:468-478`). | Começar uma compra de qualquer tela. | **Sim, trecho** no cap07 (uma frase, só apontando). |
| L22 | Grupo **"Aparência"**: digitar "tema" mostra "Mudar para Tema Escuro" / "Mudar para Tema Claro" (`:521-551,640`). | Trocar o tema sem ir às Configurações. | **Só citar** (uma frase); o tema é da T1. |
| L23 | Atalhos que a fala não diz: Shift+P "Pedidos", Shift+E "Ver Estoque", Shift+S "Configurações", Shift+N "Fiscal & Ambiental", Shift+F "Funcionários (RH)" (`hooks/useKeyboardShortcuts.tsx:25-36`). No Mac, o Ctrl vira Cmd (`:19`). | Navegar sem o mouse. | **Sim, trecho**: a lista já está na tela no cap07; acrescentar Pedidos, Estoque e Configurações na fala. |
| L24 | **Configurações → "Atalhos"**: chave "Atalhos de Teclado" ("Atalhos estão ativados" / "Atalhos estão desativados"; toasts "Atalhos ativados!" / "Atalhos desativados!") e **trocar a letra**: "Clique na tecla para personalizar", toast `Tecla alterada para "X"` (`components/settings/SettingsShortcutsContent.tsx:40,82,107,122`). | Quem digita muito com Shift e esbarra nos atalhos; ou quer outra letra. | **Só citar** no cap07 (uma frase com o caminho). A tela é da T1, que já a mostra. |

### Rotina (telas de outras aulas)

| # | O que é | Vale? |
|---|---|---|
| L25 | Em Contas, os botões novos "Este mês", "Próximos 7 dias" e "Até o fim do mês" do filtro "Vencimento (período)" (M2). Serve à rotina diária e semanal. | **Só citar** no cap08 (uma frase). A função é da **T13**: quem mostra é ela. |
| L26 | Tudo o mais de Histórico do Caixa, Contas, Estoque, conciliação, DRE, notas, MTR/CDF e coletas. | **Não**: T9, T13, T10, T14, T15, T16 a T18 e T12. |

## 3. Proposta

Tom do roteiro atual. Números novos não são falados (decisão 2 do plano). Ordem final sugerida: cap00, cap01 (+P1), cap02,
cap03 (+P4), **cap03b (P2, novo)**, cap04 (+P5), cap05, **cap05b (P3, novo)**, cap06, cap07 (+P6), cap08 (+P7), cap09 (M1),
cap10, cap11 (+P8).

### P1 · cap01, dois trechos a mais (DASHBOARD)

| Tela | Fala |
| --- | --- |
| (depois da 1ª linha) Clique no filtro de período: a lista aberta, de "Todos os tempos" a "Personalizado"; destaque em "Hoje", "Últimos 7 dias" e "Personalizado"; fecha sem escolher. | No filtro, dá pra ver só o dia de hoje, os últimos sete dias, o ano inteiro ou, em Personalizado, as datas que você quiser. |
| (depois do "Ver detalhes" da margem, ainda em "Mês passado") Clique em "Ver detalhes" no cartão "Total Compras": a janela "Total de Compras", com "Total no período", "Comparativo mensal" e "Por forma de pagamento"; fecha. | Os outros dois cartões também abrem. Em Total Compras, o Ver detalhes mostra quanto saiu por cada forma de pagamento. |

Mundo: nada novo (o detalhe usa o mesmo `get_orders_payment_distribution` de outubro que o plano já simula).

### P2 · capítulo novo cap03b · "Quem deve e como você paga" (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`, "Este mês"); a câmera desce até "Saldos em Aberto": as colunas "A receber" e "A pagar". | Mais um cartão que responde pergunta do dia: Saldos em Aberto. De um lado, quem deve pra empresa. Do outro, pra quem a empresa deve. |
| [ZOOM: a coluna "A receber", com a "Fundição Bandeira do Vale" e a "Aços Quiririm Ltda"] | Aparecem os maiores de cada lado, com o valor. Aqui, a Fundição Bandeira do Vale e a Aços Quiririm. |
| Destaque em "Posição líquida", no rodapé do cartão. | Embaixo, a Posição líquida faz a conta: o que tem a receber menos o que tem a pagar. Verde, sobra. Vermelho, falta. |
| A câmera fica no cartão; destaque no filtro "Este mês", lá em cima. | Uma dica: esse cartão não olha o filtro. Ele mostra o saldo de hoje, seja qual for o período. |
| Clique em "Ver relatório": a janela "Relatório de Saldos" ("Visualize todos os saldos a receber e a pagar"), com "A Receber" e "A Pagar"; destaque em "Exportar Relatório"; fecha. | Em Ver relatório, abre a lista completa, que dá pra exportar em PDF ou em Excel. |
| A câmera vai a "Métodos de Pagamento das Compras": a pizza e a lista com a porcentagem de cada forma. | Do lado, os Métodos de Pagamento das Compras: quanto saiu em dinheiro, em Pix e em saldo, no período do filtro. |
| [ZOOM: a linha "Dinheiro" da lista] | É um bom termômetro de quanto dinheiro vivo o caixa precisa ter pra comprar. |
| A câmera desce ao fim do painel: "Demonstrativo Financeiro (DRE)", com "Regime de Caixa" e "Regime de Competência". | E, no fim do painel, fica o DRE resumido, o mesmo do Relatório Financeiro. Ele tem um tutorial só dele. |

Mundo: `balances` do mundo já tem a Fundição (+R$ 14.370,00), a Aços Quiririm (+R$ 2.870,00 depois da T13) e a Serra Fina
Alumínio (−R$ 1.500,00); conferir o sinal no cartão (a receber × a pagar) e a "Posição líquida" antes de gravar, sem falar
valor. [BACKEND] leituras do "Relatório de Saldos" (`balances` com `balance_movements` e os nomes dos parceiros), as mesmas da
T4. `get_orders_payment_distribution` de novembro com pelo menos Dinheiro, Pix/Transferência e Saldo. O bloco do DRE já é
alimentado pelo `get_financial_dre_summary` e `get_dre_expenses_by_group` do plano; não clicar no regime (L5, [TESTAR]).

### P3 · capítulo novo cap05b · "Concluir, editar e excluir" (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap05`), na Agenda de novembro; clique no dia 9: à direita, "09 de novembro", "segunda-feira", e a tarefa "Ligar pro contador sobre as notas de outubro", 16:00. | Tarefa feita, tarefa concluída. Ontem o Rafael ligou pro contador, e a tarefa ainda está aberta. |
| Clique no círculo à esquerda da tarefa: ela fica riscada; o toast "Tarefa atualizada". | É só clicar no círculo do lado dela. Ela fica riscada, e para de aparecer nos lembretes. |
| A câmera fica na tarefa riscada. | Clicou sem querer? Um clique de novo, e ela volta a ficar pendente. |
| Clique no dia 13; passa o mouse na "Revisão do caminhão truck": aparecem o lápis e a lixeira; clique no lápis: a janela "Editar Tarefa"; troca "Horário" para 10:30; "Salvar": "Tarefa atualizada". | Pra mudar uma tarefa, passe o mouse nela e clique no lápis. Troco o horário da revisão pra dez e meia, e salvo. |
| Clique no dia 18; passa o mouse em "Buscar a lona nova do caminhão"; clique na lixeira: "Excluir Tarefa" ("Tem certeza que deseja excluir esta tarefa?"); clique em "Excluir Tarefa": o toast "Tarefa excluída". | E a lixeira exclui. O sistema pede a confirmação, e a tarefa sai do calendário. |
| Clique no dia 11 e, no calendário, clique na "Coleta na Auto Peças Vale Forte": abre "Editar Tarefa"; destaque em "Categoria" ("Coleta") e em "Cliente / Fornecedor" ("Auto Peças Vale Forte"); "Cancelar". | Cada tarefa tem uma categoria, com a sua cor. Na categoria Coleta, aparece um campo a mais, pra dizer em qual cliente ou fornecedor é a retirada. |
| Destaque na "Legenda:" do rodapé ("Tarefa", "Coleta", "CRM", "Outro"). | As cores estão na legenda, embaixo do calendário. |
| Clique em "Semana": a semana de 8 a 14 de novembro; depois em "Dia"; depois em "Hoje" e de volta a "Mês". | Em cima, você troca a vista: a semana, um dia só ou o mês. E o botão Hoje traz de volta pro dia de hoje. |
| Duplo clique no dia 19: abre "Nova Tarefa" com "Data" 19/11/2026; "Cancelar". | Um atalho: dois cliques num dia já abrem a tarefa nova naquela data. |

Mundo: duas tarefas a mais na semente `inicio` (e em `apos-cap05`), criadas pelo Rafael, categoria "Tarefa", pendentes:
09/11 16:00 "Ligar pro contador sobre as notas de outubro" ("Lembrar no dia" ligado; como é de ontem, não entra em "1 lembrete
para hoje" nem em "Tarefas para hoje") e 18/11 sem horário "Buscar a lona nova do caminhão". Semente nova `apos-cap05b`
(a do contador concluída, a revisão às 10:30, a da lona excluída), de onde partem o cap06 em diante. [BACKEND] `UPDATE
schedule_tasks` (`status`, `scheduled_time`) e `DELETE schedule_tasks`. [TESTAR] o lápis e a lixeira só aparecem com o mouse
em cima (`opacity-0 group-hover`); o duplo clique no dia; o cap05 mostra as duas tarefas novas no mês (conferir o quadro).
Se a "Notificação push" entrar (decisão 2), é uma linha a mais neste capítulo.

### P4 · cap03, dois trechos a mais (DASHBOARD)

| Tela | Fala |
| --- | --- |
| (depois de "Principais Fornecedores") Destaque no nome "Depósito Irmãos Siqueira" (cursor em cima, sem clicar). | Clicando no nome, você vai direto pro histórico desse fornecedor. |
| (trocar a última linha) Clique em "Ver todos os clientes": a janela "Todos os clientes"; clique em "Por Quantidade (kg)" e volta a "Por Valor (R$)"; destaque em "Página 1 de …"; fecha. | E em Ver todos os clientes aparece a lista completa do período, por valor ou por quantidade. |

Mundo: `list_top_clients_paginated` respondendo também com `p_sort_by` de quantidade. Se outubro tiver compra de balcão,
acrescentar a frase de L9 ("A linha Sem cadastro junta as compras de balcão, sem fornecedor.").

### P5 · cap04, um trecho a mais (DASHBOARD)

| Tela | Fala |
| --- | --- |
| (antes do "Voltar ordem ao normal") A câmera fica na janela "Configurações do Dashboard". | Um aviso: os valores do painel só aparecem pra quem tem permissão de ver o financeiro. Quem não tem vê o aviso Sem permissão. |

### P6 · cap07, quatro trechos a mais (ATALHOS)

| Tela | Fala |
| --- | --- |
| (depois de "Com Enter, você vai direto pra ele") Apaga e digita "fundi": em "Resultados da Busca", "Fundição Bandeira do Vale"; o painel mostra "Cliente", o telefone e "Saldo". | Vale pra gente também. Digito Fundição, e o painel já mostra o telefone e o saldo do cliente. Com Enter, abre o histórico dele. |
| Apaga a busca: destaque no grupo "Ações Rápidas" ("Nova Compra", "Nova Venda", "Abrir Caixa"). | Sem digitar nada, as Ações Rápidas começam uma compra, uma venda ou abrem o caixa, de qualquer tela. |
| (trocar a linha do "É sempre Shift mais uma letra") Destaque em "Navegação", um por vez: "Compra", "Venda", "Caixa", "Pedidos", "Ver Estoque", "Configurações" e "Agenda". | É sempre Shift mais uma letra: Shift+C abre a compra, Shift+V a venda, Shift+X o caixa, Shift+P os pedidos, Shift+E o estoque, Shift+S as configurações e Shift+A a agenda. |
| (última linha, depois de "a letra vai pro campo") A câmera fica no Dashboard. | E em Configurações, Atalhos, dá pra desligar os atalhos ou trocar a letra de cada um. |

Mundo: `customers` com o telefone fictício da Fundição e o saldo dela em `balances` (já existem). Pronúncia nova no
`tts_textos.py`: "xífti-pê" e "xífti-ésse".

### P7 · cap08, um trecho a mais (ROTINA)

| Tela | Fala |
| --- | --- |
| (depois dos cartões "Vencidas" e "Vence em 7 dias") A câmera fica nos cartões. | Nos filtros da tela, dá pra ver só o que vence nos próximos sete dias ou até o fim do mês. |

Sem clique (a função é da T13). No cap09, só regravar a aba "A Receber" (M1); a fala fica.

### P8 · cap11, recapitulação

Acrescentar na 1ª linha "os saldos em aberto" e trocar a 3ª por: "Marcou, mudou de dia e concluiu tarefas na Agenda, e viu os
avisos que aparecem sozinhos." Montagem com um quadro de P2 e um de P3.

## 4. Estimativa

| Bloco | Palavras | Segundos de fala (2,6 palavras/s) |
|---|---|---|
| P1 (cap01) | ~55 | ~21 |
| P2 (cap03b, novo) | ~165 | ~63 |
| P3 (cap05b, novo) | ~165 | ~63 |
| P4 (cap03) | ~25 a mais | ~10 |
| P5 (cap04) | ~27 | ~10 |
| P6 (cap07) | ~85 a mais | ~33 |
| P7 + P8 | ~35 a mais | ~13 |
| **Total** | **~560** | **~215 s de fala (≈ 3,6 min)** |

**2 capítulos novos** (2 vinhetas a mais, ~10 s). A aula vai de ~10 min para ~14 min, perto do alvo de 13 min da fonte.
Regravação obrigatória pelo app novo: só o cap09 (M1); os outros capítulos mudam por cobertura, não por mudança do app.

## Depende de decisão

1. **Dois capítulos novos** (cap03b e cap05b) ou diluir nos capítulos vizinhos. Os novos pedem a semente `apos-cap05b` e duas
   tarefas a mais no mundo.
2. **"Notificação push"**: o front só grava a chave; falta confirmar com o time o que ela dispara antes de falar.
3. **DRE no painel**: só citado (T15 cobre). Mostrar a troca de regime aqui exige testar se os cartões do topo mudam junto.
4. **"Card Lucro" / "Evolução do Lucro"** na janela de configurações continua diferente da tela ("Margem"): segue como
   handoff para o time; a fala não lê esses nomes.
5. **Permissão (P5)** e **filtros de Contas (P7)**: frases de citação; cortar se a T2 e a T13 já bastarem.
