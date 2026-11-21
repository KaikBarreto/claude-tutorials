# Roteiro T25 · Dashboard, Agenda e rotina

Roteiro pronto para o ensaio gravado e, depois da revisão geral, para a voz (voz Kaik Barreto, ElevenLabs eleven_v4). Coluna
Fala = texto da narração (uma linha da tabela = uma linha da fala); números e "Contas a Pagar e Receber" vão como se fala, e a
legenda volta à grafia da tela pelo `numeros` do `narracao/config_narracao.json`; a grafia de pronúncia do TTS está em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
(`T25/inventario.md`, versão 1.59.154, revisada no 1.60.22). Sementes, dados e o que simular: `T25/plano.md`.
Marcas: `[BACKEND: ...]` (o backend falso ainda não tem), `[ZOOM: ...]` (dura a frase inteira), `[ILUSTRAÇÃO: ...]` (cena
desenhada, nunca tela inventada), `[TESTAR]` (o robô confere antes de gravar). Computador, logado como Rafael Nogueira.

- **Título:** Dashboard, Agenda e rotina
- **Antes:** Cato, o assistente (T21)
- **Próximo:** as aulas dos módulos do plano (cartão "Próximo: os módulos do seu plano"; na trilha, a primeira é o T16)
- **Vinhetas (áreas):** DASHBOARD ×5 · AGENDA ×3 · ATALHOS · ROTINA ×3 · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~14 min de vídeo (1.787 palavras de fala, ~11,5 min de voz a 2,6 palavras/s, mais a vinheta de abertura, 13 vinhetas de capítulo, a cartela e as ações na tela); alvo da fonte ~13 min
- **Revisão 21/11 (app 1.60.22):** 14 capítulos (eram 12): novos cap04 "Quem deve e como você paga" e cap07 "Concluir, editar e excluir"; os antigos 4 a 11 viram 5, 6, 8, 9, 10, 11, 12, 13. Trechos novos: filtro de período aberto e Total Compras com "Por forma de pagamento" (cap01), ordenar "Todos os clientes" e clique no nome do pódio (cap03), busca de parceiro e Ações Rápidas e Atalhos nas Configurações (cap09), filtros de Contas (cap10). Não entrou: "Sem permissão" (sem tela), "Notificação push" (sem função confirmada), o DRE por dentro (T15). A tela é 1600x900.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta da aula EcoFlix com o título "Dashboard, Agenda e rotina". | (sem fala) |
| Capítulo novo (`inicio`), no Dashboard: "Olá, Rafael!" e "Bem-vindo de volta ao seu painel de controle", a faixa "1 lembrete para hoje" no alto; a câmera passa devagar pelos cartões. [BACKEND: `inicio` (plano, "Mundo")] [TESTAR: "Tarefas para hoje" não abre (marca do dia no `localStorage`)] | Oi! Esta é a última aula da Formação básica. Neste tutorial, a gente lê os números do Dashboard e monta a rotina que mantém o sistema vivo. |
| [ILUSTRAÇÃO: o Rafael (figura genérica), de manhã, no escritório do pátio; três balões acendem, cada um na sua pergunta: "Como vai o mês?", "Que conta vence?", "O que tem pra amanhã?"] | Na Recicla Vale Metais, o Rafael começa o dia com três perguntas: como vai o mês, que conta vence e o que tem pra amanhã. |
| A ilustração sai; destaque em "Dashboard", no alto do menu, e depois em "Agenda", no fim. | As respostas ficam em duas telas do menu: o Dashboard, no alto, e a Agenda, no fim. |
| Cartão "Antes: Cato, o assistente". | Se você ainda não viu o tutorial do Cato, o assistente, dá uma olhada antes. [pause] Vamos aos números. |


### cap01 · Comprado, vendido e margem (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`), no Dashboard, filtro "Este mês". Destaque nos três cartões, um por vez: "Total Compras", "Total Vendas" e "Margem (Vendas − Compras)". | Lá em cima ficam três cartões: Total Compras, Total Vendas e a Margem. Eles seguem o filtro de período, que abre em Este mês. |
| [NOVO 1.60.22] Clique no filtro de período: a lista aberta, de "Todos os tempos" a "Personalizado"; destaque em "Hoje", "Últimos 7 dias", "Este ano" e "Personalizado"; fecha sem escolher (Esc). Não se escolhe nada, para não pedir número novo. | No filtro, dá pra ver só o dia de hoje, os últimos sete dias, este ano ou, em Personalizado, as datas que você quiser. |
| [ZOOM: o cartão "Margem (Vendas − Compras)", verde, com o valor de novembro (R$ 99.838,75)] | Repara na margem: ela é só vendas menos compras, no período. Em novembro, até hoje, a Recicla Vale vendeu bem mais do que comprou, e ela aparece alta, em verde. |
| [ILUSTRAÇÃO: margem × lucro. À esquerda, um caminhão leva do pátio a pilha de ferro com a etiqueta "Comprado em outubro, vendido agora", e a conta "Vendas − Compras" em verde, bem alta. Na frase "o lucro de verdade", à direita, a conta "Vendas − custo do que foi vendido − impostos − despesas", com a etiqueta "Relatório Financeiro"] | Uma dica: margem não é lucro. Boa parte dessa venda é o ferro que foi comprado em outubro e ficou no pátio. O lucro de verdade, com custo, imposto e despesa, fica no Relatório Financeiro. |
| No filtro, escolhe "Mês passado": os cartões mudam para outubro. [ZOOM: "Total Compras" R$ 256.860,00, "Total Vendas" R$ 269.240,00 e "Margem (Vendas − Compras)" R$ 12.380,00, verde] [BACKEND: `get_financial_dre_summary` de outubro com os números do T15] | Agora, outubro inteiro. As vendas passaram as compras por pouco, e a margem ficou em doze mil trezentos e oitenta reais. Foi o mês em que esse ferro entrou. |
| Clique em "Ver detalhes" no cartão da margem: a janela "Margem (Vendas − Compras)", com o bloco "Como é calculado": "Total de Vendas", "− Total de Compras", "= Margem". Depois da frase, fecha. | Em Ver detalhes, a conta aparece aberta: o total de vendas, menos o total de compras, dá a margem. |
| [NOVO 1.60.22] Clique no cartão "Total Compras" (ainda em "Mês passado"): a janela "Total de Compras" com "Total no período", "Comparativo mensal" e, só nas compras, "Por forma de pagamento" [ZOOM]. Fecha ao fim. [TESTAR: a lista de formas de outubro (lida no ensaio)] | Os outros dois cartões também abrem. Em Total Compras, o Ver detalhes mostra quanto saiu por cada forma de pagamento. |

### cap02 · Seis meses e o comparativo (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`, "Este mês"); a câmera desce até "Compras vs Vendas (Últimos 6 Meses)": as barras "compras" e "vendas" de junho a novembro. | Mais abaixo, os gráficos. Em Compras versus Vendas, cada mês tem duas barras: o que a empresa comprou e o que vendeu. |
| Destaque em "Evolução da Margem": a linha mês a mês. | Do lado, a Evolução da Margem mostra como a margem andou, mês a mês. |
| Destaque em "(Últimos 6 Meses)" e, lá em cima, no filtro "Este mês". | Uma dica: esses gráficos mostram sempre seis meses, mesmo com o filtro num mês só. O filtro manda nos cartões e nos rankings. |
| A câmera desce aos três "Comparativo Mensal" ("Total Compras", "Total Vendas" e "Margem"). [ZOOM: o "Comparativo Mensal - Total Vendas", com "Mês Anterior", "Mês Atual" e a queda em %] | Embaixo, o Comparativo Mensal põe o mês passado inteiro contra o mês atual, até hoje. |
| [ILUSTRAÇÃO: dois calendários lado a lado: "Outubro" com os 31 dias marcados e "Novembro, até hoje" com 10 dias marcados; a seta de queda fica grande; na frase "vai ficando justa", os dias de novembro se completam e a seta encolhe] | Uma dica: como hoje é dia dez, a queda aparece grande. É normal no começo do mês: são dez dias contra trinta e um. Até o fim do mês, a comparação vai ficando justa. |


### cap03 · Semanas e rankings (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`); a câmera desce até "Volume Semanal de Compras": a área "Peso (kg)", com as oito semanas. | E quantos quilos entram por semana? O Volume Semanal de Compras mostra as últimas oito semanas, em quilos. |
| Passa o mouse num ponto: a dica "Peso", com os quilos da semana. | Passando o mouse, aparece o peso de cada semana. São sempre as mesmas oito semanas, seja qual for o filtro. |
| No filtro, escolhe "Mês passado"; a câmera vai a "Materiais Mais Comprados", em "R$", com o "Ferro pesado" em primeiro; clique em "Kg". [ZOOM: o "Ferro pesado" em primeiro, com o peso] [BACKEND: `get_top_materials` de outubro (T15)] | Nos rankings, o filtro volta a valer. Em outubro, o material mais comprado foi o ferro pesado, em reais e em quilos: cinquenta mil quilos. |
| Destaque em "Principais Fornecedores": o "Depósito Irmãos Siqueira" em primeiro. | Em Principais Fornecedores, o primeiro é o Depósito Irmãos Siqueira, que trouxe a maior parte desse ferro. |
| Em "Principais Clientes", em "R$": a "Fundição Bandeira do Vale" em primeiro; clique em "Kg": a "Aços Quiririm Ltda" passa para o primeiro lugar. | Em Principais Clientes, a Fundição Bandeira do Vale lidera em reais, com o cobre. Em quilos, quem lidera é a Aços Quiririm, com o ferro. |
| Clique em "Ver todos os clientes": a janela "Todos os clientes" ("Período: …", "{n} no período", "Página 1 de …"); no seletor "Por Valor (R$)" escolhe "Por Quantidade (kg)" e a lista muda para quilos; depois da frase, fecha. [NOVO 1.60.22: o seletor] | E em Ver todos os clientes aparece a lista completa do período, por valor ou por quantidade em quilos. |
| [NOVO 1.60.22] Clique no nome "Aços Quiririm Ltda" no pódio de "Principais Clientes": o histórico do parceiro abre (a ficha é da aula de Clientes e Fornecedores). Fim do capítulo. [TESTAR: a página abre sem erro] | Clicando no nome de quem está no pódio, você vai direto pro histórico dele. |

### cap04 · Quem deve e como você paga (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| [NOVO] Capítulo novo (`inicio`, "Este mês"); a câmera desce até o cartão "Saldos em Aberto": as colunas "A receber" (verde) e "A pagar" (vermelho), com os maiores parceiros de cada lado. [BACKEND: `balances`, as mesmas leituras do "Relatório de Saldos" da aula de Clientes e Fornecedores] | Mais um cartão que responde pergunta do dia: Saldos em Aberto. De um lado, quem deve pra empresa. Do outro, pra quem a empresa deve. |
| Destaque na coluna "A receber", na "A pagar" e na linha "Fundição Bandeira do Vale" (primeira de "A receber"): nome do parceiro e valor de cada um (lido no ensaio: três de cada lado, sem "Ver mais"; o 1º a receber é a Fundição). | Aparecem os maiores de cada lado, com o valor de cada um. Quem mais deve pra empresa é a Fundição Bandeira do Vale. |
| Destaque em "Posição líquida", no rodapé do cartão (verde com +, vermelho com −). | Embaixo, a Posição líquida faz a conta: o que tem a receber menos o que tem a pagar. Verde, sobra. Vermelho, falta. |
| A câmera sobe até o filtro "Este mês" e volta ao cartão: o saldo não muda com o período. [TESTAR: o cartão não segue o filtro (`useOpenBalancesSummary` não recebe datas)] | Uma dica: esse cartão não olha o filtro. Ele mostra o saldo de hoje, seja qual for o período. |
| Clique em "Ver relatório": a janela "Relatório de Saldos" ("Visualize todos os saldos a receber e a pagar"), com "A Receber" e "A Pagar"; clique em "Exportar Relatório": o menu abre com "Exportar em PDF" e "Exportar em Excel" (sem escolher: nada é baixado, e a fala não cita o PDF); Esc fecha o menu e a janela. | Em Ver relatório, abre a lista completa de quem deve e de quem se deve, com o total de cada lado, e dá pra exportar. |
| A câmera desce a "Métodos de Pagamento das Compras": a pizza com a % de cada forma e a lista "Dinheiro", "Pix/Transferência" e "Saldo" (formas lidas no ensaio), no período do filtro. [BACKEND: `get_orders_payment_distribution` de novembro] | Ao lado, os Métodos de Pagamento das Compras: quanto saiu em dinheiro, em Pix ou transferência e em saldo, no período do filtro. |
| [ZOOM: a linha "Dinheiro" da lista] | É um bom termômetro de quanto dinheiro vivo o caixa precisa ter pra comprar. |
| A câmera desce ao fim do painel: "Demonstrativo Financeiro (DRE)", com o seletor "Regime de Caixa" (sem clicar: o conteúdo é da aula do Relatório Financeiro). | E, no fim do painel, fica o DRE resumido, o mesmo do Relatório Financeiro. Ele tem um tutorial só dele. |

### cap05 · O painel do seu jeito (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`, layout padrão); destaque no botão "Configurações", ao lado do filtro de período; clique: a janela "Configurações do Dashboard" ("Escolha quais seções exibir. Arraste os cards para reordená-los."). | E dá pra deixar o painel do seu jeito. No botão Configurações, ao lado do filtro, ficam todas as partes do Dashboard. |
| Desliga a chave de "Métodos de Pagamento"; fecha a janela: o cartão sai do painel. | Cada parte tem a sua chave. Desligo Métodos de Pagamento, e ele sai do painel. |
| Passa o mouse no "Volume Semanal": a alça aparece no canto de cima; aperta, move devagar e solta o cartão logo depois dos três cartões do topo. [TESTAR: arrasto dnd-kit, 8 px antes de pegar] | Pra mudar a ordem, é só segurar o cantinho do cartão e arrastar. Trago o Volume Semanal pra perto do topo. |
| Abre "Configurações" de novo; destaque em "Voltar ordem ao normal" (sem clicar); fecha. | Se quiser desfazer, o Voltar ordem ao normal põe o painel como era. E a arrumação fica salva no seu usuário, neste navegador. |


### cap06 · Tarefas no calendário (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`, agora com as tarefas do contador no dia 9 e da lona no dia 18), no Dashboard; clique em "Agenda", no fim do menu: o calendário de "nov 2026" em "Mês", com o dia 10 marcado; à direita, "10 de novembro", "terça-feira" e a tarefa "Cotação do cobre com a Fundição Bandeira do Vale", 14:00. [TESTAR: janela ≥ 1280 px mostra a lateral] | Agora, a Agenda, no fim do menu. Ela abre no mês, com o dia de hoje marcado, e do lado ficam as tarefas do dia. |
| Clique em "Nova Tarefa": a janela "Nova Tarefa"; em "Título" digita "Revisão do caminhão truck"; "Categoria" fica em "Tarefa"; "Data" 12/11/2026; "Horário" 09:00. | Pra marcar uma tarefa, é em Nova Tarefa. A revisão do caminhão truck, na quinta, dia doze, às nove da manhã. |
| Destaque em "Lembrar no dia", já ligado; clique em "Salvar": o toast "Tarefa criada com sucesso" e a tarefa aparece no dia 12. [BACKEND: `INSERT schedule_tasks`] | Com Lembrar no dia ligado, ela avisa no dia. Salvo, e ela já está no calendário. |
| Arrasta a tarefa do dia 12 para o dia 13: o toast "Tarefa atualizada". [TESTAR: arrasto nativo do navegador] [BACKEND: `UPDATE schedule_tasks.scheduled_date`; vira `apos-cap06`] | A oficina só pode na sexta? É só arrastar a tarefa pro dia treze. |
| Destaque nas etiquetas com estrela do dia 15, "Proclamação da República", e do dia 20, "Consciência Negra". | E os feriados aparecem sozinhos, com uma estrela: a Proclamação da República, no dia quinze, e a Consciência Negra, no dia vinte. |
| A câmera fica nos feriados. | Pra esconder os feriados, é em Configurações, Usabilidade, Exibir Feriados. |


### cap07 · Concluir, editar e excluir (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| [NOVO] Capítulo novo (`apos-cap06`), na Agenda de novembro; clique no dia 9: à direita, "09 de novembro" e a tarefa "Ligar pro contador sobre as notas de outubro", 16:00, com o círculo à esquerda. [BACKEND: tarefa do contador na semente `inicio`] | Tarefa feita, tarefa concluída. Ontem o Rafael ligou pro contador, e a tarefa ainda está aberta. |
| Clique no círculo à esquerda da tarefa: ela fica riscada; o toast "Tarefa atualizada". [TESTAR: `confere` da tarefa riscada] | É só clicar no círculo do lado dela, e ela fica riscada. |
| Clique de novo no círculo: volta a pendente (sem risco); clique outra vez: concluída. [BACKEND: `UPDATE schedule_tasks.status`] | Clicou sem querer? Um clique de novo, e ela volta a ficar pendente. Concluo outra vez. |
| Clique no dia 13; passa o mouse na "Revisão do caminhão truck": aparecem o lápis e a lixeira; clique no lápis: a janela "Editar Tarefa"; troca o "Horário" para 10:30 (roleta de horas e minutos), "Concluir", "Salvar": "Tarefa atualizada". [BACKEND: `UPDATE schedule_tasks.scheduled_time`] | Pra mudar uma tarefa, passe o mouse nela e clique no lápis. Abre a janela Editar Tarefa, igual à de criar. Troco o horário da revisão pra dez e meia, e salvo. |
| Clique no dia 18; passa o mouse na "Buscar a lona nova do caminhão"; clique na lixeira: "Excluir Tarefa" ("Tem certeza que deseja excluir esta tarefa?"); clique em "Excluir Tarefa": o toast "Tarefa excluída". [BACKEND: `DELETE schedule_tasks`] | E a lixeira exclui. O sistema pede a confirmação antes de apagar, e a tarefa sai do calendário. |
| Passa o mouse na "Coleta na Auto Peças Vale Forte" (dia 11): o cartão com a categoria "Coleta", a data, a hora e o parceiro; clique na tarefa: "Editar Tarefa", com destaque em "Categoria" ("Coleta") e em "Cliente / Fornecedor" ("Auto Peças Vale Forte"); "Cancelar". | Cada tarefa tem uma categoria, com a sua cor. Na categoria Coleta, aparece um campo a mais, pra dizer em qual cliente ou fornecedor é a retirada. |
| A câmera desce até a "Legenda:" do rodapé do calendário, com as cores das categorias. | As cores estão na legenda, embaixo do calendário. |
| Clique em "Semana" (a semana atual), em "Dia", em "Mês" e no botão "Hoje" (volta ao dia 10). | Em cima, você troca a vista: a semana, um dia só ou o mês. E o botão Hoje traz de volta pro dia de hoje. |
| Duplo clique no dia 19: abre "Nova Tarefa" com a "Data" já em 19/11/2026; "Cancelar". Fim do capítulo: `apos-cap07` (contador concluída, revisão às 10:30, lona excluída). | Um atalho: dois cliques num dia já abrem a tarefa nova naquela data. |

### cap08 · Os avisos automáticos (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap07`), na Agenda de novembro; destaque nos avisos com o selo vermelho "A Pagar" e o verde "A Receber". | Além das tarefas, a Agenda mostra sozinha os avisos do dinheiro: as contas a pagar em vermelho e as a receber em verde, no dia do vencimento. |
| [ZOOM: "A Receber: R$ 4.790,00", no dia 17] | No dia dezessete, por exemplo, tem quatro mil setecentos e noventa reais a receber: a primeira parcela da Fundição Bandeira do Vale. |
| [ZOOM: "A Pagar: R$ 2.360,00", no dia 23] | E no dia vinte e três, dois mil trezentos e sessenta reais a pagar: a parcela dos pneus, na Auto Peças Vale Forte. |
| [ILUSTRAÇÃO: o fiado com vencimento: a venda a prazo da Fundição (300 kg de cobre mel, R$ 14.370,00) se divide em três parcelas de R$ 4.790,00, que caem uma em cada dia do calendário (17/11, 17/12, 18/01) com o selo "A Receber"; o saldo não aparece de novo ao lado] | O fiado com vencimento entra do mesmo jeito, uma vez só: cada parcela no seu dia. |
| Clique no aviso do dia 17: abre "Contas a Pagar/Receber". [TESTAR: clique no aviso compacto do mês] | Clicando no aviso, você vai direto pra Contas a Pagar e Receber, pra conferir ou dar baixa. |
| Volta à Agenda (Shift+A); clique na seta do próximo mês: "dez 2026"; destaque em "Vencimento - Assinatura EcoSistema", no dia 5. | E o vencimento da assinatura do EcoSistema também entra, em laranja: aqui, no sábado, cinco de dezembro. |
| Tecla Shift+D: o Dashboard, com a faixa "1 lembrete para hoje" e a "Cotação do cobre com a Fundição Bandeira do Vale" no alto. | E as tarefas com Lembrar no dia aparecem no alto do Dashboard, no dia certo. |


### cap09 · Atalhos e o contról-cá (vinheta: ATALHOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap05`), no Dashboard; tecla Ctrl+K: a busca abre ("Buscar páginas, clientes, fornecedores, materiais, funcionários..."), com "Ações Rápidas" e "Navegação". [TESTAR: o Ctrl+K chega à página, sem o atalho do navegador] | Pra andar mais rápido, o Ctrl+K abre a busca de tudo: telas, clientes, fornecedores, materiais e funcionários. |
| Digita "cobre": em "Resultados da Busca", "Cobre mel", "Cobre misto" e os outros; passa o mouse em "Cobre mel": o painel ao lado mostra "Material", "Estoque", "P. Compra" e "P. Venda". [ZOOM: "P. Compra" R$ 42,50 e "P. Venda" R$ 47,90] | Digito cobre, e os materiais aparecem na hora. No Cobre mel, o painel mostra o estoque e os preços: quarenta e dois e cinquenta na compra e quarenta e sete e noventa na venda. |
| O destaque vai ao rodapé do painel ("Pressione Enter para abrir"). | Com Enter, você vai direto pra ele. |
| [NOVO 1.60.22] Apaga a busca e digita "fundi": em "Resultados da Busca", "Fundição Bandeira do Vale"; o painel mostra "Cliente", o telefone e o "Saldo" (valor não falado); destaque no "Saldo" e no rodapé "Pressione Enter para abrir" (não se aperta Enter). | Vale pra gente também. Digito Fundição, e o painel já mostra o telefone e o saldo do cliente. Com Enter, abre o histórico dele. |
| [NOVO 1.60.22] Apaga a busca (Ctrl+A, Backspace): o grupo "Ações Rápidas" com "Nova Compra", "Nova Venda" e "Abrir Caixa"; destaque em cada um (sem clicar). | Sem digitar nada, as Ações Rápidas começam uma compra, uma venda ou abrem o caixa, de qualquer tela. |
| Apaga a busca e digita "atalho": em "Sistema", "Ver Atalhos de Teclado"; Enter: a janela "Atalhos de Teclado", com "Atalhos Globais", "Geral" e "Navegação". (O "?" do teclado não abre a lista na 1.59.154: `useKeyboardShortcutsModal` não está montado; o caminho é este.) | E digitando atalho, aparece Ver Atalhos de Teclado, com a lista inteira. |
| Destaque em "Navegação", um por vez: "Compra" Shift+C, "Venda" Shift+V, "Caixa" Shift+X, "Pedidos" Shift+P, "Ver Estoque" Shift+E, "Configurações" Shift+S e "Agenda" Shift+A. | É sempre Shift mais uma letra: Shift+C abre a compra, Shift+V a venda, Shift+X o caixa, Shift+P os pedidos, Shift+E o estoque, Shift+S as configurações e Shift+A a agenda. |
| Esc fecha; tecla Shift+X: abre o "Caixa"; depois, tecla Shift+D: volta ao Dashboard. | Olha: Shift+X, e o caixa abre. Shift+D, e volto pro Dashboard. |
| A câmera fica no Dashboard. | Os atalhos valem fora dos campos de texto. Com o cursor num campo, a letra vai pro campo. |
| [NOVO 1.60.22] Tecla Shift+S: abre Configurações; clique na aba "Atalhos": "Atalhos de Teclado" com a chave "Atalhos estão ativados" (destaque; nada é desligado). | Quer desligar os atalhos, ou trocar a letra de cada um? É em Configurações, Atalhos. |

### cap10 · A rotina diária (vinheta: ROTINA)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: "Rotina diária · 10 min": um relógio de dez minutos; três itens acendem, cada um na frase dele, com a etiqueta da aula: "Conferir o caixa" (Caixa: abrir, fechar e o cofre), "Contas do dia" (Contas a Pagar e Receber), "Coletas de amanhã" (Agenda)] | Bom, números lidos e agenda em uso. Agora, a rotina que mantém o sistema vivo, começando pela diária: uns dez minutos, logo cedo. |
| Clique em "Dashboard" no menu: no alto do painel, a faixa "1 lembrete para hoje" com a "Cotação do cobre com a Fundição Bandeira do Vale", 14:00 (destaque na faixa). [Achado 1.60.18 e 1.60.22: a janela "Tarefas para hoje" não abre na gravação, mesmo sem a marca do dia; a fala usa a faixa, que está na tela] | Ao abrir o Dashboard de manhã, as tarefas de hoje já aparecem no alto, como a cotação do cobre com a Fundição, às duas da tarde. |
| Clique em "Fechar"; Ctrl+K, digita "histórico", escolhe "Histórico do Caixa" e Enter: "Histórico do Caixa" ("Todos os registros de fechamento do caixa"), "Caixas Fechados", com os caixas de 09/11 e o "Saldo Final" de cada um. | Primeiro, o caixa. No Histórico do Caixa, você confere se os caixas de ontem fecharam, com o saldo final de cada um. Depois, é só abrir o caixa do dia. |
| Menu "Financeiro" → "Contas a Pagar/Receber"; destaque nos cartões "Vencidas" e "Vence em 7 dias". | Depois, as contas. Em Contas a Pagar e Receber, os cartões Vencidas e Vence em 7 dias mostram o que pede atenção agora. |
| [NOVO 1.60.22] Clique em "Filtros" na tela de Contas: o painel abre em "Vencimento (período)", com os botões "Este mês", "Próximos 7 dias" e "Até o fim do mês" (destaque em "Próximos 7 dias" e em "Até o fim do mês", sem clicar; a função é da aula de Contas a Pagar e Receber); Esc fecha. | Nos filtros da tela, dá pra ver só o que vence nos próximos sete dias ou até o fim do mês. |
| Tecla Shift+A: a Agenda; clique no dia 11: à direita, "11 de novembro", "quarta-feira", e "Coleta na Auto Peças Vale Forte", 08:00, na cor de "Coleta". | E, na Agenda, o que tem pra amanhã: a coleta na Auto Peças Vale Forte, às oito da manhã. |
| A câmera fica na tarefa. | Quem tem o módulo de Coletas confere também as ordens de coleta do dia seguinte. Ele depende do plano contratado. |

### cap11 · A rotina semanal (vinheta: ROTINA)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: "Rotina semanal · 30 min": o relógio de meia hora; dois itens acendem, com a etiqueta da aula: "Estoque" (Estoque: saldo, histórico e posição) e "Fiado vencido" (Contas a Pagar e Receber)] | Uma vez por semana, meia hora pra duas conferências: o estoque e o fiado. |
| Capítulo novo (`apos-cap07`); tecla Shift+E: a tela "Estoque", com os materiais e os saldos. | Shift+E abre o Estoque. Aqui você confere se o saldo bate com o que tem no pátio, pelo menos nos materiais que mais giram, como o cobre e a latinha. |
| A câmera passa pelos saldos do "Cobre mel" e do "Alumínio latinha". | Pra acertar uma diferença, o caminho está na aula do estoque. |
| Menu "Financeiro" → "Contas a Pagar/Receber" → aba "A Receber" (1.60.22: os cartões do alto viram "Total a Receber" e "Total recebido"; a fala não os cita): as parcelas da Fundição e o fiado da Aços Quiririm. | Depois, o fiado. Em Contas a Pagar e Receber, na aba A Receber, ficam as parcelas e o fiado de cada cliente. |
| Destaque na coluna "Status". | O que passar da data aparece como Vencida, e é hora de cobrar. Assim, nenhum fiado fica esquecido. |


### cap12 · A rotina mensal (vinheta: ROTINA)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: "Rotina mensal · 2 h": um calendário com o dia 1º marcado e quatro itens, com a etiqueta da aula: "Conciliar o banco" (Bancos, cofre e conciliação bancária), "Conferir o DRE" (Relatório Financeiro e DRE), "Pacote do contador" (Transporte, serviço e o contador) e "MTR e CDF pendentes" (Ambiental: MTR e CDF)] | E uma vez por mês, o fechamento: umas duas horas, em quatro passos. |
| [ILUSTRAÇÃO: acendem os dois primeiros itens] | Conciliar o extrato do banco com o sistema e conferir o DRE do mês, no Relatório Financeiro. |
| [ILUSTRAÇÃO: acendem os dois últimos, com um cadeado pequeno e a etiqueta "Módulo do plano"] | Mandar o pacote das notas pro contador e ver se ficou algum MTR ou CDF pendente. Esses dois dependem do módulo de notas fiscais, do plano contratado. |
| Capítulo novo (`apos-cap07`); tecla Shift+A: a Agenda; seta do próximo mês: "dez 2026", com "Vencimento - Assinatura EcoSistema" no dia 5; clique no dia 1. | Pra não esquecer, a gente marca o fechamento na Agenda, no primeiro dia útil: terça, primeiro de dezembro. |
| Clique em "Nova Tarefa": "Título" "Fechamento de novembro"; "Descrição" "Conciliar o banco, conferir o DRE, mandar o pacote ao contador e ver MTR e CDF pendentes"; "Data" 01/12/2026; "Horário" 08:00; "Lembrar no dia" ligado; "Salvar": "Tarefa criada com sucesso". [BACKEND: `INSERT schedule_tasks`; vira `apos-cap12`] | Nova Tarefa: Fechamento de novembro, com os quatro passos na descrição, às oito da manhã, e Lembrar no dia ligado. No dia, ela aparece logo cedo. |


### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: os três cartões e o "Como é calculado" (cap01), os gráficos e o comparativo (cap02), os rankings (cap03) e os saldos em aberto (cap04). | Pronto! Recapitulando: a gente leu o Dashboard sem confundir margem com lucro, com os gráficos de seis meses, o comparativo e os rankings. |
| Montagem rápida: "Configurações do Dashboard" e o arrasto do "Volume Semanal" (cap05). | Deixou o painel do seu jeito, escondendo e trocando os cartões de lugar. |
| Montagem rápida: a tarefa nova arrastada para o dia 13 (cap06), a tarefa do contador riscada (cap07) e os avisos "A Receber" e "A Pagar" (cap08). | Marcou e mudou uma tarefa de dia na Agenda e viu os avisos que aparecem sozinhos. |
| Montagem rápida: a lista "Atalhos de Teclado" e a busca do Ctrl+K com o "Cobre mel" (cap09). | Usou os atalhos e a busca do Ctrl+K. |
| [ILUSTRAÇÃO: as três rotinas lado a lado: "Diária · 10 min", "Semanal · 30 min" e "Mensal · 2 h", cada uma com os seus itens] | E montou as três rotinas: a diária, a semanal e a mensal. |
| Cartão "Próximo: os módulos do seu plano"; cartela final. | A Formação básica acabou. No próximo tutorial, começam as aulas dos módulos que fazem parte do seu plano. Até lá! |
