# Roteiro T17 · Dashboard, relatórios e exportações

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`,
gerado por script a partir desta coluna. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela
(`T17/inventario.md`, conferido de novo contra o código da 1.38.6).
Aula no computador (janela de 1280×800), logada como Camila Duarte (admin), com o navegador no fuso America/Sao_Paulo e o relógio em FAKE_NOW (o padrão do robô, `rec/recorder/browser.mjs:22,178,189`). Todo capítulo parte de um navegador novo, com o mesmo mundo: a aula só lê e filtra, nada é gravado no banco.
Tudo fictício: os números do Dashboard saem das sementes de todas as aulas (OS #1 a #34 e as do T21, o Financeiro do T13 ao T15, as avaliações do T7). A fala explica o que cada número quer dizer e não lê valores (P23) nem datas.

- **Título final:** Dashboard, relatórios e exportações (o nome da TRILHA e do plano, que o cartão final do T21 já promete)
- **Vinhetas (áreas):** DASHBOARD · RELATÓRIOS · EXPORTAÇÕES · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Integração com WhatsApp (T21)
- **Próximo:** fim da trilha (cartão "Fim da trilha"; a fala convida a voltar a qualquer tutorial)
- **FAKE_NOW:** `2026-11-13T16:30:00-03:00` (sexta-feira), no backend falso e no robô. Motivo: depois do corte do T21 (15:00); a saudação sai "Boa tarde. Veja como está o dia." (P14); a OS da academia do dia 13 já está concluída (16:10), então **nenhuma OS do dia fica aberta** e o bug de fuso do Dashboard não aparece (P2; decisão do Kaik para este lote e alinhamento do `PRODUCAO.md`).
- **Duração estimada:** ~7 min de vídeo (975 palavras de fala, ~6,2 min de voz a 2,6 palavras/s, mais 11 vinhetas e a navegação entre as telas; o plano previa ~14 min, a fala segue o tempo natural)
- **Estado inicial (fim do T21):** `seeds-extra/t21/apos-cap10.json`: Glacial Cold Brasil; Camila Duarte (admin) logada; os seis técnicos e a Tatiane Ribeiro (T15, com a jornada do dia 11 no ponto); OS #1 a #34, com a #34 do Hotel Mirante do Mar concluída no dia 13 pelo Rafael Lima (09:42 às 11:05) e a OS da Academia Ponto Forte do dia 13 a caminho com o Lucas Ferreira (corte do T21); o chamado da Mariana Lopes (T5, sem data) em aberto; o Financeiro do T13 ao T15 (Conta Principal R$ 17.735,00 e Caixa R$ 800,00 no fim do T15; as folhas de dezembro a pagar); as avaliações do T7; o estoque do T8; o WhatsApp conectado (T21).
  Conferido nas duas portas de cadastro e no `seed_company_catalog` (inventário 0.5): o Dashboard não tem configuração própria (os blocos são fixos), os tipos de serviço de "OS por Tipo de Serviço" vêm do catálogo e do T4, e as contas Caixa e Conta Principal nascem com a empresa.
- **Por semente (bastidor, `seeds-extra/t17/inicio.json` = o fim do T21 mais):** a OS da academia do dia 13 **concluída** (check-in 15:05, check-out 16:10; entra em "Desempenho da Equipe", e os avisos de WhatsApp dela seguem "Ignorado"); **nenhuma OS do dia 13 aberta às 16:30** (P2: senão "Requer Atenção" mostra "Atrasada 0 dias"); nenhum lançamento em 01/10 nem em 01/11 (P2: o "Fluxo de Caixa" descarta o primeiro dia do período; conferir as sementes do T13 ao T15); nenhuma posição em `technician_locations` nas últimas 2 h (a equipe já voltou, decisão 2); o `storage` com a marca `dominex:portal-tickets-seen:<id da Camila>` (sem o aviso de chamados por cima, P15).
- **Criado ao vivo:** nada no banco (só leitura e filtros); a exportação do capítulo 10 gera um arquivo fora do vídeo.
- **Estado final:** igual ao inicial. É a última aula da trilha; atualizar `MUNDO_FICTICIO.md` com o fim do mundo fictício.
- **Sementes entre capítulos:** `inicio` em todos os capítulos (nenhum grava nada).
- Decisões padrão (`plano.md` → "Riscos e decisões", proposta recomendada; com duas opções, a mais simples sem rosto, senha nem dado real):
  **gravar sem OS do dia aberta** (decisão 1 e decisão do Kaik para este lote: o bug de fuso do Dashboard, P2), com "Evolução de OS" em "Este mês" e "Diário" e sem zoom nos rótulos do eixo (P3); mapa vazio, com a equipe recolhida às 16:30 (decisão 2): a fala explica quem entra no mapa, e "Abrir Mapa ao Vivo" fica em zoom; "Requer Atenção" com o que a semente herdada tiver (decisão 3): a fala vale para a lista e para "Tudo em dia!", e "Atribuir técnico" não é clicado (P9); "Exportar meus dados" de verdade, com três grupos e sem "Funcionários" (decisão 4, P19), e plano B "Cancelar", como no T1, se o gravador não seguir com o download (a fala vale nos dois casos); exportações de lista só com o menu aberto (decisão 5, P18); a atividade comercial fica de fora (decisão 6, P21); o achado de segurança P20 vai para o time do app, e a fala do capítulo 10 recomenda liberar a exportação só para quem precisa (decisão 7); nenhum valor lido (decisão 8, P23); sem zoom em "Todos os tempos", na linha "concluídas este mês" nem na seta de "OS Abertas" (decisão 9: P1, P5 e P7); sem Assinatura (decisão 10); os 12 blocos ficam (decisão 11).
  A conferência do código da 1.38.6 mudou três coisas do plano:
  (1) "Configurações" fica no rodapé do menu, ao lado de "Sair" (como no T1);
  (2) Contas a Pagar/Receber abre na aba "Todas" (`components/financial/FinanceContas.tsx:159`), e o filtro de status fica dentro do botão "Filtros", na seção "Status" (`:894-900`; `components/ui/FilterButton.tsx`);
  (3) clicar na linha de "Chamados abertos" abre as Ordens de Serviço na aba "Chamados", já no chamado (`lib/portalCalls.ts:23-27`).
  Handoffs (a fala não depende deles): "Todos os tempos" mostra o mês atual (P1); fuso e ordem dos gráficos (P2 e P3); "concluídas este mês" fixo (P5); seta de "OS Abertas" (P7); atalhos genéricos (P9); consultas sem uso (P24); lista de OS sem o período (P25); Guia T17 (inventário 0.4); segurança P20 (`TRILHA.md`, achado 9).
  Pronúncias: NPS "ene-pê-ésse" (T5), DRE "dê érri ê" (T13), DFC "dê-éfe-cê" (T20), PDF "pê-dê-éfe", CSV "cê-ésse-vê" e Excel "ékisel" (T13), Shift "chift" (T1), check-in e check-out "tchéquin" e "tchécaut" (T7); Dashboard na escrita normal, como no T1, no T2, no T5 e no T12; "Contas a Pagar/Receber" lido "Contas a Pagar e Receber" e "Funcionários / RH", "Funcionários e RH" (a legenda volta a escrever a barra); nenhuma pronúncia nova.
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[handoff: ...]` (texto ou comportamento do app para o time corrigir; a fala não depende dele).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Dashboard, relatórios e exportações". | (sem fala) |
| Dashboard, logada como Camila Duarte: "Olá, Camila! 👋" e "Boa tarde. Veja como está o dia.", com o filtro "Este mês" à direita; a câmera desce devagar pelos três cartões e pelos blocos. [BACKEND: semente `seeds-extra/t17/inicio.json`; tiles de Niterói, Nominatim e unpkg do fakebase; avisos da Dominex sem semente, nenhum aviso no topo] | Oi! Neste último tutorial da trilha, a gente vai ler o Dashboard, encontrar o relatório de cada área e levar os dados pra PDF, Excel ou CSV. |
| A câmera continua pelos blocos. | O Dashboard é a primeira tela do dia. Ele junta o que aconteceu nas ordens de serviço, no caixa e na equipe, e cada número leva pra tela de onde veio. |
| Cartão discreto: "Atalho: Shift + D". | Uma dica: com os atalhos ligados, o Shift mais D volta pro Dashboard de qualquer tela. |
| Cartão discreto: "Antes: Integração com WhatsApp". | Se você ainda não viu o tutorial Integração com WhatsApp, dá uma olhada antes. [pause] Vamos começar pelos números do topo. |

### cap01 · Os números do topo (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo, logada (semente `inicio`), no Dashboard em "Este mês"; zoom em "OS Abertas" ("{n} pendentes"), sem zoom na seta (P7). | Lá em cima ficam três números. OS Abertas conta as ordens do período que estão em aberto, e embaixo, quantas estão pendentes. |
| Zoom em "Taxa de Conclusão", sem zoom na linha "concluídas este mês" (P5). | A Taxa de Conclusão mostra quanto do trabalho do período já foi concluído. |
| Zoom em "Faturamento" ("no período selecionado", com a seta de variação, se houver; inventário, dúvida 1). | E o Faturamento soma o que já entrou e foi pago no período. Quando aparece uma setinha, ela compara com o período anterior. |
| A câmera fica no cartão "Faturamento". | O que ainda vai entrar fica em Contas a Pagar/Receber. |
| Clique em "OS Abertas": abre "Ordens de Serviço"; volta ao Dashboard pelo menu "Dashboard". | E cada cartão leva pra tela de origem. Clico em OS Abertas e caio nas ordens de serviço. |

### cap02 · Equipe, caixa e evolução (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); zoom em "Equipe em Campo" ("Ao vivo"): o mapa de Niterói com o cartão "Nenhum técnico em campo agora" e o botão "Abrir Mapa ao Vivo", sem clicar (decisão 2). [TESTAR: o mapa vetorial no Chromium do robô (inventário, dúvida 3, a mesma do T5)] | Logo abaixo, o dia em movimento. Em Equipe em Campo, o mapa mostra ao vivo quem está a caminho ou em atendimento. No fim da tarde a equipe já voltou, e o Abrir Mapa ao Vivo leva pro mapa completo. |
| A câmera fica no mapa. | Entra no mapa o técnico que abriu a ordem com a localização do celular liberada. |
| Zoom em "Fluxo de Caixa": as linhas "Entradas" e "Saídas" e o resumo "Entradas:", "Saídas:" e "Saldo:". | No Fluxo de Caixa ficam as entradas, as saídas e o saldo do período. |
| A câmera fica no resumo do bloco. | Ele e o faturamento contam o dinheiro que entrou de fora. Transferência entre as suas contas e pagamento da fatura do cartão ficam de fora, porque o dinheiro só trocou de bolso. |
| Em "Evolução de OS" (abre em "Mensal"), clique em "Diário": as áreas "Total" e "Concluídas", dia a dia, sem zoom nos rótulos do eixo (P2 e P3). | E a Evolução de OS mostra o total e as concluídas. No Diário, dá pra ver o ritmo de cada dia. |

### cap03 · Status, tipos e equipe (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); zoom em "OS por Status": "Pendente", "Agendada", "A Caminho", "Em Andamento" e "Concluída" (e "Cancelada", se houver), com a quantidade e a porcentagem. | Agora a coluna da direita. O OS por Status mostra quantas ordens estão em cada status, e a porcentagem de cada um. |
| Zoom em "OS por Tipo de Serviço": a rosca com o "total" no meio e a lista dos tipos. | Em OS por Tipo de Serviço, a rosca mostra que serviço a equipe mais fez no período. |
| Zoom em "Desempenho da Equipe": os técnicos com as medalhas, "{n} concluídas", a nota média e o "{tempo} médio"; o rodapé com "técnicos em campo" e "Ver relatório", sem clicar (P9). | E no Desempenho da Equipe estão os técnicos que mais concluíram, com a nota média das avaliações e o tempo médio de cada atendimento, do check-in ao check-out. |

### cap04 · O que pede atenção (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); zoom em "Requer Atenção": a lista das OS com data passada e ainda abertas ("Atrasada {n} dias") ou "Tudo em dia!" ("Nenhuma OS requer atenção imediata"), o que a semente herdada tiver (decisão 3); sem clicar em "Atribuir técnico" (P9). | E agora, o que precisa de você. O Requer Atenção junta as ordens com a data vencida que ainda estão abertas, da mais atrasada pra menos atrasada. |
| A câmera fica no bloco. | Ele e os chamados aparecem sempre, seja qual for o período, assim o que é antigo continua à vista. |
| Zoom em "Chamados abertos": o chamado da Mariana Lopes (cliente, descrição, status e "há {tempo}"). | Em Chamados abertos ficam os pedidos que os clientes abriram pelo portal. |
| Clique na linha do chamado: abre "Ordens de Serviço" na aba "Chamados", já no chamado (`lib/portalCalls.ts:23-27`); volta ao Dashboard. | Clicando, você vai direto pro chamado, na aba Chamados das ordens de serviço. |

### cap05 · O período e a origem (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); clique no filtro "Este mês": a lista "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias", "Este ano" e "Personalizado"; escolhe "Mês passado": os cartões e os blocos mudam (sem "Todos os tempos", P1). | Tudo isso obedece a um filtro só, aqui em cima, que começa em Este mês. Escolho Mês passado, e a tela inteira muda junto. |
| Abre o filtro e escolhe "Personalizado": "Selecionar datas", com o calendário de "Início" e "Fim"; fecha sem aplicar (Esc); escolhe "Este mês" de novo. | No Personalizado, você escolhe as datas de início e de fim. Eu volto pro Este mês. |
| Em "OS por Status", clique em "Concluída": abre "Ordens de Serviço" já no status "Concluída" (a lista vem em "Todo o período", P25); volta ao Dashboard. | Os blocos também levam pra origem. Clico em Concluída, e a lista de ordens de serviço já abre nesse status. |
| Clique no cartão "Faturamento": abre a "Visão Geral" do Financeiro (`/financeiro` → `/financeiro/relatorio`, P22). | E o Faturamento leva pra Visão Geral do Financeiro, o painel do dinheiro da empresa. |

### cap06 · Ordens de serviço e satisfação (vinheta: RELATÓRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); menu "Operacional" → "Ordens de Serviço" → aba "Relatório": "Total de OS", "Taxa de conclusão", "Tempo médio" e "Faturamento"; os gráficos "Volume de OS ao Longo do Tempo", "Faturamento ao Longo do Tempo" e "OS por Dia da Semana". [BACKEND: as leituras do T5 herdadas (`T05/inventario.md` 4)] | Pra ir além do resumo, cada área tem o seu relatório. O das ordens de serviço fica na aba Relatório, com o total, a taxa de conclusão, o tempo médio, o faturamento e a evolução no tempo. |
| A câmera desce por "Top 10 Clientes", "Top Técnicos (Concluídas)" e "Saúde do agendamento". | Mais embaixo, os clientes que mais pedem, os técnicos que mais concluem e a saúde do agendamento, que mostra o que foi feito no prazo. |
| Clique na aba "NPS e Satisfação": "NPS Score", "Média Geral", "Respostas" e "Taxa de Resposta"; "Distribuição NPS", "Ranking de Técnicos" e "Feed de Feedbacks". [BACKEND: RPCs do NPS do T5 herdadas (`get_nps_technician_ranking`, `get_nps_open_detractors`, `get_nps_criteria_averages`)] | Do lado fica a aba NPS e Satisfação. O NPS nasce da avaliação que o cliente faz depois da visita, e aqui ficam a nota, a distribuição, o ranking dos técnicos e os comentários. |

### cap07 · Financeiro e estoque (vinheta: RELATÓRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); menu "Financeiro" → "Relatórios": abas "Visão Geral", "DRE - Resultado", "DFC - Fluxo de Caixa", "Contabilidade" e "Análise", com um clique rápido em cada uma. [BACKEND: herdado do T13 e do T20, como o `cash_flow_opening_balances` do DFC] | E no Financeiro, os relatórios ficam no item Relatórios, em cinco abas: a visão geral, o DRE, o DFC, o pacote pra contabilidade e a análise dos períodos. |
| Zoom na aba "DRE - Resultado". | A leitura de cada um está no tutorial Relatório Financeiro e DRE. |
| Menu "Gestão" → "Estoque": abas "Posição de Estoque", "Inventários" e "Relatório", com um clique rápido em cada uma. [BACKEND: `get_accessible_inventory_ids` e os dados do T8 herdados (`T08/plano.md:94`)] **[1.38.19, robô]** a aba "Relatório" abre com as subabas "Compras" (a do T8, aberta por padrão) e "Curva ABC"; só o clique rápido na aba, sem abrir a "Curva ABC" (se abrir, o handler `get_inventory_abc_report` devolve `[]`). Fala intacta. Nas telas do Dashboard conferir que não há faixa de aviso nem o gate da trilha Domiflix (G1 do `IMPACTO_1.38.19.md`). | No Estoque, a Posição de Estoque mostra o saldo numa data, os Inventários guardam as contagens, e o Relatório mostra as compras de material. |

### cap08 · Pessoas: o ponto (vinheta: RELATÓRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); menu "Gestão" → "Funcionários" → aba "Controle de Ponto" → "Histórico": as jornadas (a da Tatiane, do T15), com o botão "CSV" em zoom, sem baixar. | E das pessoas, o ponto. Em Funcionários, Controle de Ponto, o Histórico tem as jornadas de cada um, e o CSV leva tudo pra uma planilha, com a entrada, a saída, as horas e o saldo de cada dia. |
| Clique em "Relatório": o "Calendário" do mês e o resumo. | E o Relatório mostra o mês num calendário, com as horas e o saldo. O ponto faz parte do módulo Funcionários / RH. |

### cap09 · PDF, Excel e CSV (vinheta: EXPORTAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); menu "Financeiro" → "Contas a Pagar/Receber" (abre em "Todas"); clique na aba "A Receber"; clique em "Filtros" e, em "Status", escolhe "Pendentes". | E quando precisar levar os dados pra fora? Em Contas a Pagar/Receber, eu fico na aba A Receber e filtro só as pendentes. |
| Clique em "Exportar": abre "Excel", "PDF" e "CSV", sem clicar (o PDF abre nova aba e os outros baixam arquivo, P18). | O Exportar leva a lista pra Excel, PDF ou CSV. |
| A câmera fica no menu aberto; fecha. | Uma dica: ajusta o período e os filtros antes, porque o arquivo sai exatamente com o que está na tela. |
| Cortes rápidos: o "Exportar" de "Movimentações Financeiras" ("PDF", "Excel" e "CSV"), o de "DRE - Resultado" ("Excel" e "PDF") e o do "Estoque" ("PDF" e "Excel"), cada um aberto e fechado sem escolher. | O mesmo Exportar aparece nas movimentações, no DRE e no estoque. |

### cap10 · Exportar meus dados (vinheta: EXPORTAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); clique em "Configurações" no rodapé do menu (engrenagem, ao lado de "Sair"); na aba "Empresa", rola até o fim: o cartão "Exportar meus dados" ("Baixe uma planilha do Excel com os dados da sua empresa: clientes, equipamentos, ordens de serviço, orçamentos, contratos, financeiro e mais. ..."). | E pra levar tudo de uma vez, tem o Exportar meus dados, no fim da aba Empresa, nas Configurações. Ele gera uma planilha do Excel com os dados da empresa, e serve de cópia de segurança. |
| Clique em "Exportar dados": janela "Exportar meus dados" ("Escolha o que deseja incluir na planilha. O arquivo é gerado na hora e baixado automaticamente.") com os grupos; clique em "Limpar seleção"; marca "Clientes", "Ordens de Serviço" e "Financeiro". | Você escolhe os grupos. Aqui, os clientes, as ordens de serviço e o financeiro. |
| Zoom no grupo "Funcionários", desmarcado (P19: a aba leva CPF, salário e chave PIX). | Uma dica: esse arquivo pode levar os dados da empresa inteira. Guarda num lugar seguro e libera essa opção só pra quem precisa. |
| Clique em "Exportar": "Exportando...", "Exportando {sheet}... {rows} registros" e o aviso "Exportação concluída! O arquivo foi baixado.". [TESTAR: o aviso com o download bloqueado no gravador (`acceptDownloads: false`, como o "Exportar pacote" do T20); plano B: "Cancelar", como no T1, com a mesma fala] [BACKEND: as leituras paginadas de `customers`, `customer_contacts`, `service_orders`, `service_materials`, `financial_transactions` e `financial_accounts` (`hooks/useCompanyDataExport.ts:218-1336`)] | No Exportar, ele junta cada parte e baixa a planilha, com uma aba pra cada assunto. |

### cap11 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: os três cartões e os blocos do Dashboard. | Pronto! Recapitulando: no Dashboard, você viu o que cada número quer dizer, como o período comanda a tela e como cada cartão leva pra origem. |
| Montagem rápida: o Relatório de OS, o NPS e os Relatórios do Financeiro. | Depois encontrou o relatório de cada área: ordens de serviço, satisfação, financeiro, estoque e ponto. |
| Montagem rápida: o menu "Exportar" e o aviso de conclusão. | E levou os dados pra fora, com o Exportar de cada lista e o Exportar meus dados. |
| Cartão "Fim da trilha"; cartela final. | Esse foi o último tutorial da trilha. Volte em qualquer um pelo capítulo que precisar. Até a próxima! |
