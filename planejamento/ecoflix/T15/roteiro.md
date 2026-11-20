# Roteiro T15 · Relatório Financeiro e DRE

Pronto para gerar a voz e gravar (sem etapa de aprovação; o Kaik ajusta depois). Coluna Fala = narração (voz Kaik Barreto) na
grafia da legenda; a grafia do TTS fica em `narracao/tts_textos.py`, gerado desta coluna (uma linha da tabela = uma linha da
fala). Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código do 1.60.18
(`T15/inventario.md`). Mundo, valores e backend falso: `T15/plano.md`.

- **Título:** Relatório Financeiro e DRE
- **Antes:** Bancos, cofre e conciliação bancária (T14)
- **Próximo:** Cato, o assistente (T21)
- **Vinhetas (áreas):** CATEGORIAS · CENTROS DE CUSTO · RELATÓRIO · DASHBOARD · DASHBOARD · DRE · DRE · DRE · PATRIMÔNIO · EVOLUÇÃO · DFC · DFC · HISTÓRICO · HISTÓRICO · EXPORTAR · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~25 min de vídeo em 17 capítulos (~3.390 palavras de fala, ~21,7 min de voz a 2,6 palavras/s, mais 16 vinhetas e as
  ações sem fala; eram 2.259 palavras e ~16 min 45 s no 1.59.154; entram os capítulos Organizando o DRE, DFC prevista, DFC realizada e
  Vários lançamentos de uma vez, e trechos em outros oito).
- **Aula:** computador, janela de 1600×900 (16:9), logado como Rafael Nogueira (MASTER) do começo ao fim. `FAKE_NOW`
  2026-11-10T08:30:00-03:00; o mês lido é outubro ("Mês passado"). Cada capítulo abre um navegador novo, com o mundo do fim do
  anterior (`seeds-extra/t15/inicio`, `apos-cap01`, `apos-cap02`, `apos-cap10`; o nome do arquivo é o do capítulo de ORIGEM e não muda,
  porque a T21 e a T25 leem `t15/apos-cap10`); do capítulo 4 ao 15, o `setup` abre o relatório, escolhe "Mês passado" e a aba de partida
  fora do vídeo. O capítulo 14 parte de `apos-cap10` mais a variante `lote-categoria` (só ele; ela não segue adiante).
- **Marcas na coluna Tela:** `[BACKEND: ...]` (o que o backend falso ainda não tem), `[ZOOM: ...]` (dura a frase inteira, nunca
  em cima de outro zoom: entre dois, "a câmera abre"), `[ILUSTRAÇÃO: ...]` (cena HTML da marca, `docs/09-aula-ilustrada.md`:
  fundo branco, Montserrat, acento #50D088, objetos genéricos, nunca tela do app), `[TESTAR ...]` (o robô confere antes).


### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Relatório Financeiro e DRE". | (sem fala) |
| Dashboard do EcoSistema (tela inicial), logado como Rafael Nogueira; a câmera fica no geral, sem zoom. [BACKEND: semente `seeds-extra/t15/inicio.json`: o fim do T14 mais o "Mundo: o que esta aula precisa" do plano] | Oi! Neste tutorial a gente vai responder a pergunta que todo dono faz no fim do mês: eu ganhei ou perdi dinheiro? E por quê? |
| [ILUSTRAÇÃO: O mês do pátio: um galpão genérico; em "encheu o pátio de ferro", dois caminhões descarregam e a pilha de ferro cresce; em "saiu mais dinheiro", um cofrinho esvazia, com moedas saindo mais do que entrando; em "ganhou ou perdeu", um ponto de interrogação entre um selo verde "Lucro?" e um vermelho "Prejuízo?"] | Em outubro, a Recicla Vale Metais vendeu bem e ainda encheu o pátio de ferro. Mesmo assim, saiu mais dinheiro do que entrou. Afinal, ela ganhou ou perdeu? |
| A ilustração sai; volta o Dashboard. | Pra responder, a gente vai arrumar as categorias e os centros de custo, ler o Relatório Financeiro, o DRE e o fluxo de caixa, e exportar tudo pro contador. |
| Cartão discreto: "Antes: Bancos, cofre e conciliação bancária". | Se você ainda não viu o tutorial Bancos, cofre e conciliação bancária, dá uma olhada antes. |

### cap01 · O plano de contas (vinheta: CATEGORIAS)

| Tela | Fala |
| --- | --- |
| Do Dashboard, abre o menu "Financeiro" e clica em "Categorias Financeiras": "Categorias Financeiras", "Gerencie as categorias de receitas e despesas" e o menu da tela, com "Categorias", "Centros de custo" e "Grupos do DRE". [BACKEND: categorias, `dre_groups` e centros de custo da semente (plano, "Mundo")] | Tudo começa pelas categorias. No menu, Financeiro, Categorias Financeiras. |
| A câmera desce devagar por "Categorias de receita" ("Aluguel de caçamba" e as do sistema, com cadeado) e por "Categorias de despesa", com as divisórias "Impostos e deduções", "Custos adicionais" e "Despesas operacionais (OPEX)". | As categorias são o plano de contas da empresa: a lista que diz de onde vem e pra onde vai cada real. Em cima ficam as de receita, como o aluguel de caçamba. Embaixo, as de despesa, como a folha, a energia e o combustível. |
| [ILUSTRAÇÃO: Plano de contas: as contas do mês (folha, energia, diesel, aluguel de caçamba) caem cada uma na sua gaveta com etiqueta, e cada gaveta liga a uma linha de relatório, na primeira frase; na segunda, uma conta sem etiqueta cai num monte "Sem categoria"] | É pela categoria que o relatório separa o dinheiro. Despesa lançada sem categoria cai num monte só, e aí ninguém sabe o que ela é. |
| A ilustração sai; a câmera para nas divisórias das despesas. | Repara que as despesas ficam separadas pelo lugar onde entram no DRE, o relatório do resultado do mês, que a gente lê daqui a pouco. |
| No cartão "Frete" (em "Custos adicionais"), clica nos três pontos ("Ações de Frete") e em "Adicionar subcategoria": abre "Nova subcategoria", com "Categoria principal" em "Frete" e a dica "A subcategoria herda os dados do pai como ponto de partida, mas pode ter grupo DRE próprio.". | O Frete que já existe é o frete de compra, o de buscar a sucata no fornecedor. Ele entra como custo do material. Agora vou criar uma subcategoria nele: o frete de entrega. |
| Em "Nome", digita "Frete de entrega"; em "Onde aparece no DRE" (veio "Custos adicionais", do pai), abre a lista e escolhe "Despesas operacionais (OPEX)"; a "Prévia no DRE padrão" passa a "Despesas operacionais (OPEX)", "Frete de entrega" e "No padrão atual, reduz o resultado operacional.". | A subcategoria herda tudo da principal, mas pode mudar de lugar no DRE. Levar o material até o cliente é gasto do dia a dia da operação. Então eu escolho Despesas operacionais, o OPEX. A prévia embaixo já mostra onde ela vai entrar. |
| Clique em "Criar categoria": aviso "Categoria criada"; o cartão "Frete" abre sozinho, com "1 subcategoria", e mostra "Frete de entrega" com o selo "Despesas operacionais (OPEX)" e a nota "Subcategorias podem pertencer a outro grupo DRE; o lançamento segue sempre o grupo da própria subcategoria.". [ZOOM: o selo e a nota, a frase inteira] [BACKEND: insert em `financial_categories` (`parent_id` do Frete, `dre_group` opex, `cash_flow_group` operacional) com o `dre_group_id` do grupo de despesas operacionais] | Uma dica: cada subcategoria tem o seu lugar no DRE. Os lançamentos do frete de entrega vão pras despesas operacionais, mesmo com a principal em Custos adicionais. E a tela marca com um selo quando os dois são diferentes. |
| No cartão "Frete", já aberto, clica nos três pontos de "Frete de entrega" ("Ações de Frete de entrega"): o menu mostra "Editar", "Tornar principal" e "Excluir"; fecha sem escolher. | Nos três pontos de cada categoria dá pra editar. E numa subcategoria aparece o Tornar principal, que tira ela de dentro da outra e deixa ela sozinha na lista. |
| Nos três pontos de "Telefone e internet" ("Ações de Telefone e internet"), clica em "Excluir": a janela "Excluir categoria?", "Os lançamentos não serão apagados: eles ficarão sem categoria. Esta ação não pode ser desfeita."; clica em "Cancelar". [ZOOM: o texto da janela, a frase inteira] | Excluir uma categoria não apaga lançamento nenhum. Eles só ficam sem categoria. Se ela tiver subcategorias, elas viram principais. E as categorias do sistema, as do cadeado, não têm o Excluir. |
| A câmera passa pelo texto "N categorias · arraste para reordenar", no alto de "Categorias de despesa", sem arrastar. | E a ordem da lista é sua: é só arrastar uma categoria pra outra posição. |
| A câmera abre; em "Categorias de despesa", clique em "Nova": abre "Nova categoria", com "Tipo" em "Despesa"; em "Nome", digita "Máquinas e veículos". | Agora, uma categoria que pede cuidado: a compra de máquina ou de caminhão. |
| [ILUSTRAÇÃO: Nem toda saída é despesa, três cartões, um por linha. Cartão 1, nesta linha: um caminhão e uma prensa genéricos comprados; a seta vai para "bem da empresa", e um "despesa do mês" riscado] | Uma dica: comprar uma prensa ou um caminhão não é despesa do mês. O dinheiro vira um bem da empresa. |
| (ilustração, cartão 2: o dinheiro do empréstimo entra e a parcela devolve, os dois só trocam de lugar; a parcela se parte em dois lançamentos, "valor emprestado" e "juros", e só "juros" desce para "resultado") | Com empréstimo é parecido. Receber não é receita, e devolver o valor emprestado não é despesa. Só os juros entram no resultado. Se a parcela mistura os dois, são dois lançamentos. |
| (ilustração, cartão 3: o lucro saindo para os sócios, também fora de "despesa") | E a distribuição de lucro pros sócios também fica fora da despesa. |
| A ilustração sai. Em "Onde aparece no DRE", escolhe "Não compõe o DRE" ("Movimentação patrimonial: aparece no caixa, mas não no DRE."); a prévia mostra "informativo" e "No padrão atual, não altera o resultado.". Em "Grupo no Fluxo de Caixa (DFC)", escolhe "Atividades de investimento" ("Compra ou venda de máquinas, veículos e outros ativos."). | Por isso, essa categoria vai em Não compõe o DRE: o dinheiro sai do caixa, mas o resultado não muda. E no fluxo de caixa, que acompanha o caminho do dinheiro, ela fica em Atividades de investimento. |
| Clique em "Criar categoria": aviso "Categoria criada"; "Máquinas e veículos" aparece na divisória "Não compõe o DRE". [BACKEND: insert (`dre_group` outros, `cash_flow_group` investimento, sem `dre_group_id`); com o Frete de entrega, vira `apos-cap01`] | Pronto. O EcoSistema registra a compra. O controle dos bens, a depreciação da máquina e o ganho ou a perda quando ela for vendida ficam com o contador. Na dúvida sobre onde uma categoria entra, é ele quem orienta. |

### cap02 · Centros de custo (vinheta: CENTROS DE CUSTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap01`, na tela "Categorias Financeiras"); no menu da tela, clique em "Centros de custo": "Centros de custo", "Agrupe receitas e despesas por setor para saber quanto cada área gasta. É opcional em cada lançamento." e a lista com "Coleta", "Escritório", "Frota" e "Pátio". | Com as categorias certas, dá pra saber em que o dinheiro foi gasto. O centro de custo responde onde: em qual frente da empresa. |
| [ILUSTRAÇÃO: As frentes do pátio: um pátio genérico dividido em três áreas coloridas; "Pátio" (âmbar: balança e pilhas de sucata) recebe as contas de energia e de aluguel; "Coleta" (azul: caminhão e caçamba) recebe o diesel e a manutenção; "Produção" (roxo: uma prensa fazendo fardos de latinha) entra por último, ainda sem conta] | Na Recicla Vale Metais, o pátio fica com a energia e o aluguel, e a coleta fica com o combustível e a manutenção do caminhão. Assim, cada frente mostra quanto custa. |
| A ilustração sai. Clique em "Novo centro de custo": "Novo centro de custo", "Defina um nome e uma cor para identificar o setor nos lançamentos."; em "Nome", digita "Produção"; em "Cor", clica no roxo ("Cor #8B5CF6"); em "Descrição", digita "Prensa de latinha e papelão". | Agora, uma frente nova: a produção, a prensa que enfarda latinha e papelão. Coloco o nome, uma cor pra achar rápido nos gráficos e uma descrição. |
| [ZOOM: o interruptor "Ativo", ligado, com "Centros inativos deixam de aparecer nos formulários de lançamento, mas seguem nos lançamentos antigos.", a frase inteira] | Uma dica: quando uma frente parar, é só desligar o Ativo. Ela sai dos formulários e continua nos lançamentos antigos. Excluir não apaga lançamento nenhum, só tira a marcação, e eles ficam sem centro de custo. |
| A câmera abre; clique em "Salvar": aviso "Centro de custo criado"; "Produção" entra na lista; o mouse passa no lápis ("Editar centro de custo") e na lixeira ("Excluir centro de custo") da linha "Produção", sem clicar. [BACKEND: insert em `cost_centers` (`name` Produção, `color` #8B5CF6, `description`, `is_active` true); vira `apos-cap02`] | Salvei. Daqui pra frente, o Centro de custo aparece como opção nos lançamentos de despesa e de receita, no caixa, no banco e nas contas a pagar e receber. E, na lista, o lápis edita o centro, e a lixeira exclui. |

### cap03 · O Relatório Financeiro (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap02`, no Dashboard); abre o menu "Financeiro" e clica em "Relatório Financeiro": "Relatório Financeiro", "Visão completa das finanças do seu negócio", o filtro em "Este mês" e as abas, na aba "Dashboard". [BACKEND: `localStorage` sem "financial-report-tab"; as RPCs do relatório no backend falso (plano, "Gravação")] | Plano de contas pronto. Agora, o relatório. No menu, Financeiro, Relatório Financeiro. |
| Clique no filtro de período: a lista "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias", "Este ano" e "Personalizado"; o mouse passa por "Personalizado" e por "Todos os tempos"; escolhe "Mês passado", e a tela recarrega com outubro. | Em cima fica o período. A tela sempre abre em Este mês, e novembro mal começou. Tem também o Personalizado, que abre o calendário pra escolher as datas, e o Todos os tempos. Então eu escolho Mês passado, e a tela inteira passa a mostrar outubro. |
| A câmera fica no filtro, agora em "Mês passado". | Se um dia o relatório parecer vazio, confere o período primeiro. |
| A câmera passa pelas abas "Dashboard", "DRE", "DFC", "Centros de Custo" e "Histórico". | Embaixo ficam as cinco abas. Nesta aula, a gente passa pelo Dashboard, pelo DRE, pelo DFC, pelos Centros de Custo e pelo Histórico. E a tela volta sempre na última aba que você abriu. |
| Clique em "Centros de Custo": os cartões "Receitas financeiras", "Despesas financeiras", "Resultado das movimentações" e "Cobertura por centro de custo" e o gráfico "Receitas x despesas por centro". [BACKEND: `get_financial_dre_summary` de outubro e de setembro, com `costCenters` por categoria (plano, "Mundo")] | Nos Centros de Custo aparece o resultado de cada frente. |
| A câmera para nos cartões, em "vs. período anterior". | Cada cartão compara com o período anterior. Aqui, outubro contra setembro. |
| Clique na coluna "Pátio" do gráfico "Receitas x despesas por centro" ("Clique em uma coluna para detalhar o centro."): abre "Categorias de Pátio", "Selecione uma categoria para ver as movimentações que formam o valor."; fecha. | Clicando numa coluna, o centro abre nas categorias dele. No pátio, a folha, o aluguel e a energia. |
| A câmera desce até o "Ranking dos centros de custo" ("Pátio", "Coleta" e "Sem centro de custo", com "Não classificado"). | Em outubro, quem mais gastou foi o pátio, com a folha, o aluguel e a energia. A coleta gastou menos, e ainda trouxe a receita do aluguel de caçamba. |
| No "Ranking dos centros de custo", clique em "Movimentações" na linha "Pátio": a tela vai para a aba "Histórico", em "Despesas", com o filtro de centro de custo em "Pátio"; volta para "Centros de Custo". [BACKEND: `get_dre_expense_lines` devolve `cost_center_id`] | E o botão Movimentações leva pro Histórico já filtrado, com cada lançamento que formou esse valor. |
| A câmera aproxima do aviso azul "Esta visão considera receitas, despesas e impostos que já possuem dimensão financeira. Vendas e compras de pedidos ainda não possuem centro de custo e, por isso, não entram nestes totais.", a frase inteira. | Repara no aviso: aqui entram as receitas e as despesas lançadas no financeiro. A compra e a venda de material ficam fora desta conta. |
| A câmera abre e sobe até o cabeçalho da tela. | Uma dica: pra ver os valores do relatório, a pessoa precisa da permissão Ver Totais e Valores Financeiros. Sem ela, a tela abre só com o aviso Acesso Restrito. Quem libera é o administrador, em Usuários e Permissões. |

### cap04 · O Dashboard do mês (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: relatório em "Mês passado", aba "Dashboard"): o banner verde "Resultado do Período", "R$ 6.500,00", "Superávit". [ZOOM: o valor e "Superávit", a frase inteira] [BACKEND: `get_financial_dre_summary` e `get_dre_expenses_by_group` de outubro em competência (plano, "Mundo")] | Começando pelo Dashboard, a aba pra bater o olho. Em cima vem o Resultado do Período: outubro fechou no positivo, com seis mil e quinhentos reais. Um superávit. |
| A câmera abre no banner inteiro. | Quando o mês fecha negativo, o bloco fica vermelho e mostra déficit. E esse número é o mesmo do fim do DRE. |
| A câmera desce para "Despesas por Categoria": a rosca, "Total: R$ 40.705,90" e a lista, com "Folha salarial" (R$ 19.800,00) em primeiro. | Logo abaixo, as despesas por categoria, da maior pra menor. A folha salarial vem primeiro, com dezenove mil e oitocentos reais. |
| [ZOOM: a linha "Energia elétrica", R$ 7.700,00, a frase inteira] | E olha a energia elétrica: sete mil e setecentos reais, o dobro de um mês normal. Guarda essa, que a gente volta nela no Histórico. |
| A câmera abre e passa para "Receitas por Categoria": "Aluguel de caçamba", "Total: R$ 2.800,00". | Do lado ficam as receitas por categoria, o que entrou fora das vendas. Em outubro, o aluguel de caçamba: dois mil e oitocentos reais. |
| A câmera fica nos dois gráficos. | A compra e a venda de material não entram nesses gráficos. Elas têm linha própria no DRE. |

### cap05 · Fornecedores, clientes e ticket médio (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "Dashboard"); a câmera desce até os cartões "Ticket Médio Compra" e "Ticket Médio Venda". [BACKEND: `avgTicketPurchase`, `avgTicketSale`, `topSuppliers`, `topClients`, `topPurchaseMaterials` e `topSaleMaterials` de outubro (plano, "Mundo")] | Mais embaixo ficam os números do movimento do pátio. Primeiro, o ticket médio. |
| [ILUSTRAÇÃO: Ticket médio: as compras de outubro como pilhas de notas de alturas diferentes (de carroceiros e de depósitos); em "o total comprado", elas se juntam num montante só; em "dividido pelo número de compras", o montante se reparte em pilhas iguais, uma por compra; uma delas ganha o rótulo "Ticket Médio Compra"] | O Ticket Médio Compra é quanto vale, em média, cada compra do mês: o total comprado dividido pelo número de compras. O Ticket Médio Venda faz a mesma conta com as vendas. |
| A ilustração sai; a câmera fica nos dois cartões. | Com ele, dá pra ver se você está comprando em lotes maiores ou menores que nos outros meses. |
| A câmera vai para "Top Fornecedores", em "R$": em primeiro, "Depósito Irmãos Siqueira". | No Top Fornecedores, o primeiro de outubro é o Depósito Irmãos Siqueira, que vendeu o lote grande de ferro. |
| A câmera passa para "Top Clientes", em "R$": em primeiro, "Fundição Bandeira do Vale". | No Top Clientes, a Fundição Bandeira do Vale lidera em reais, com o cobre, o metal amarelo e o bronze. |
| Clique em "Kg" no "Top Clientes": em primeiro, "Aços Quiririm Ltda". [ZOOM: o primeiro da lista, com os quilos, a frase inteira] | Trocando pra quilos, quem vai pro topo é a Aços Quiririm, com o ferro e a chaparia. Um cliente traz valor, o outro traz volume. |
| A câmera abre e clica em "Ver todos" do "Top Clientes": abre a lista completa, paginada; fecha com Escape. | E o Ver todos abre a lista completa. |
| A câmera desce para "Materiais + Comprados": em primeiro, "Ferro pesado", "50.000 kg", "R$ 47.500,00". [ZOOM: a linha do ferro pesado, com os quilos e o valor, a frase inteira] | Nos materiais, o ferro pesado lidera as compras de outubro: cinquenta mil quilos, por quarenta e sete mil e quinhentos reais. |
| A câmera abre e passa para "Materiais + Vendidos": em primeiro, "Cobre mel"; o ferro pesado não está entre os cinco. | Já nos mais vendidos, ele nem aparece entre os cinco primeiros. Isso vai explicar o resultado do mês. |

### cap06 · Lendo o DRE (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "Dashboard"); clique na aba "DRE": o cabeçalho escuro "Demonstrativo Financeiro (DRE)", com "Regime de Caixa", "Regime de Competência" (marcado), "Organizar categorias" e "Exportar"; embaixo, "Estrutura do DRE" e a coluna "Outubro de 2026", "Valor · % receita". [BACKEND: `dre_groups` e `dre_group_id` da semente; `get_financial_dre_cost_center_breakdown` de outubro] | Agora, o DRE, o demonstrativo do resultado. É o relatório que o contador pede, e ele mostra, passo a passo, como as vendas viram resultado. |
| [ILUSTRAÇÃO: A escada do DRE: uma escada que desce; no alto, "Receita Bruta"; cada degrau tira um pedaço e acende junto com a fala: "Impostos e Deduções" até o patamar "Receita Líquida", "Custos Operacionais" até o patamar "Lucro Bruto"] | Ele se lê de cima pra baixo, como uma escada. Começa na Receita Bruta, que são as vendas. Tira os impostos e deduções, que o contador define, e chega na Receita Líquida. Tira os custos do material, e chega no Lucro Bruto. |
| (ilustração: os últimos degraus, "Despesas Operacionais" e "Outras Receitas e Despesas", até o chão, "Resultado do Período") | Depois saem as despesas operacionais, entram as outras receitas e despesas, e o que sobra é o Resultado do Período. |
| A ilustração sai; a câmera desce pela tabela: "01 (+) Receita Bruta", "02 (-) Impostos e Deduções", "03 = Receita Líquida", "04 (-) Custos Operacionais", "05 = Lucro Bruto" e "06 (-) Despesas Operacionais". | Na tela é igual: cada degrau numa faixa, com o valor de outubro. |
| Clique no grupo das despesas operacionais, dentro de "06 (-) Despesas Operacionais": abrem as categorias ("Folha salarial", "Aluguel", "Energia elétrica" e as outras), cada uma com o código, o valor e o percentual. | Clicando num grupo, ele abre as categorias, com o valor de cada uma. |
| [ZOOM: "Valor · % receita" no cabeçalho e o percentual da "Folha salarial", a frase inteira] | E do lado de cada valor vem quanto ele pesa na receita do mês. |
| A câmera para na linha da "Energia elétrica", dentro do grupo aberto, com o código, o valor e o percentual (a linha da categoria não abre: o DRE padrão do 1.60.18 não mostra centros de custo). [ZOOM: a linha, a frase inteira] | Cada categoria mostra o valor do mês. A divisão por centro de custo, quem gastou o quê, fica na aba Centros de Custo, que a gente já viu. |
| Clique na seta da faixa "06 (-) Despesas Operacionais" ("Recolher"): a faixa fecha no total; clique de novo ("Expandir"). | Pra ver só os totais, cada faixa recolhe na seta. |
| A câmera abre e desce até "08 = Resultado do Período", "R$ 6.500,00", na faixa verde. [ZOOM: a faixa e o valor, a frase inteira] | No fim, o resultado de outubro: seis mil e quinhentos reais, na faixa verde. |
| A câmera abre na tabela. | E lembra da categoria das máquinas? O que fica em Não compõe o DRE não aparece aqui. |

### cap07 · Organizando o DRE (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap02`; `setup`: "Mês passado", aba "DRE"). Clique em "Organizar categorias": a janela "Organizar categorias do DRE", "Organize os grupos do modelo padrão e mova categorias arrastando.", com a "Prévia da estrutura". [BACKEND: tabelas `dre_groups` e `financial_categories` (`dre_group_id`) da semente; `get_company_dre_configuration` com `mode` legacy e sem perfis] | O DRE que a gente acabou de ler tem uma estrutura, e ela é sua pra arrumar. No cabeçalho, Organizar categorias. |
| A câmera desce pela prévia: as faixas "01 Receita Bruta", "02 Impostos e Deduções", "04 Custos Operacionais", "06 Despesas Operacionais" e "07 Outras Receitas e Despesas", cada uma com os grupos e as categorias. | Aqui aparecem as mesmas faixas do DRE. Dentro de cada uma ficam os grupos, e dentro de cada grupo, as categorias. |
| Em "Natureza", escolhe "06 · Despesas Operacionais"; em "Novo subgrupo", digita "Despesas com pessoal" ("Ex.: Despesas com pessoal"); clique em "Adicionar": aviso "Grupo criado"; o grupo aparece na faixa 06. [BACKEND: insert em `dre_groups` (`nature` despesas_operacionais, `name` Despesas com pessoal)] | O contador pediu a folha separada das outras despesas. Então eu crio um subgrupo nas Despesas Operacionais: Despesas com pessoal. |
| Na linha da "Folha salarial", abre a lista "Mover Folha salarial para outro grupo DRE" e escolhe "06 · Despesas com pessoal": aviso "Categoria movida". [ZOOM: o grupo novo com a folha dentro, a frase inteira] [BACKEND: update de `dre_group_id` em `financial_categories`] | Agora é só levar a Folha salarial pra dentro dele, arrastando ou escolhendo o grupo na lista do lado. Nenhum lançamento muda, só o lugar onde a categoria aparece. |
| A câmera mostra o lápis ("Editar grupo Despesas com pessoal") e a lixeira ("Excluir grupo Despesas com pessoal") do grupo, sem clicar. | Dá pra renomear um grupo e trocar a ordem arrastando. Pra excluir, antes é preciso tirar as categorias de dentro dele. |
| Rola até o fim da janela e clica em "Outras visões": "Outras visões do mesmo DRE", com "DRE padrão do sistema", "Recomendado para a maioria das empresas." e o selo "Em uso"; embaixo, "Criar outra visão" e "Exemplos: DRE gerencial, DRE contábil ou EBITDA.". Não cria. [BACKEND: `get_company_dre_configuration`] | Embaixo ficam as Outras visões. Quem precisa de um DRE gerencial, contábil ou com EBITDA monta outra apresentação com os mesmos lançamentos. O DRE padrão é o recomendado pra maioria das empresas. |
| Clique em "Voltar à organização padrão" e em "Fechar": o DRE mostra "Despesas com pessoal" na faixa 06, com a "Folha salarial" dentro. | Fecho, e o DRE já mostra o grupo novo. Uma dica: esse mesmo painel abre em Categorias Financeiras, no item Grupos do DRE. |

### cap08 · Caixa ou competência (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE"); a câmera vai aos botões "Regime de Caixa" e "Regime de Competência" (marcado). | No cabeçalho do DRE fica um botão que gera muita dúvida: Regime de Caixa ou Regime de Competência. O DRE abre em competência. |
| Passa o mouse em "Regime de Caixa": a dica "Considera todo o dinheiro que entrou e saiu no período. Mostra sua situação de caixa, mas o material que você comprou e ainda está no estoque conta como custo agora, mesmo sem ter sido vendido.". [ZOOM: a dica, a frase inteira] | No caixa, conta todo o dinheiro que entrou e saiu no mês. O material comprado já vira custo, mesmo que ainda esteja no pátio. |
| A câmera abre; passa o mouse em "Regime de Competência": a dica "Considera só o custo do material que você realmente vendeu no período. O que está parado no estoque não abate o lucro até ser vendido. É o lucro contábil do negócio.". [ZOOM: a dica, a frase inteira] | Na competência, conta só o custo do material que foi vendido. O que está parado no estoque espera a venda. |
| [ILUSTRAÇÃO: O exemplo do pátio, com o ferro pesado de outubro, um passo por linha. Passo 1, nesta linha: um caminhão descarrega 50 t no pátio; o cartão "50 t × R$ 0,95/kg = R$ 47.500" sai de um cofrinho] | Pensa no ferro pesado de outubro. A Recicla Vale Metais comprou cinquenta toneladas, a noventa e cinco centavos o quilo. Saíram quarenta e sete mil e quinhentos reais. |
| (ilustração, passo 2: um caminhão leva 10 t para o cliente; o cartão "10 t × R$ 1,25/kg = R$ 12.500" entra no cofrinho; ficam 40 t no pátio) | E vendeu só dez toneladas, a um real e vinte e cinco o quilo. Entraram doze mil e quinhentos. |
| (ilustração, passo 3: acende a coluna "Caixa", com um bolso: "R$ 12.500 − R$ 47.500 = −R$ 35.000", em vermelho) | No caixa, a conta é o que entrou menos o que saiu: um prejuízo de trinta e cinco mil reais. É a verdade do bolso. |
| (ilustração, passo 4: acende a coluna "Competência": "R$ 12.500 − R$ 9.500 (o custo das 10 t) = +R$ 3.000", em verde; em "as outras quarenta toneladas", a pilha do pátio ganha a etiqueta "estoque: R$ 38.000") | Na competência, o custo é só o das dez toneladas vendidas: nove mil e quinhentos. Sobra um lucro de três mil. E as outras quarenta toneladas continuam no pátio, valendo trinta e oito mil reais como estoque. |
| (ilustração, passo 5: embaixo de cada coluna, a pergunta dela: "Quanto dinheiro sobrou?" no caixa e "Estou ganhando no que vendo?" na competência) | Nenhum dos dois está errado. O caixa responde quanto dinheiro sobrou. A competência responde se você está ganhando no que vende. |
| A ilustração sai; volta o DRE em competência. [ZOOM: "08 = Resultado do Período", "R$ 6.500,00", a frase inteira] | Agora no DRE de verdade, com o mês inteiro. Em competência, outubro deu seis mil e quinhentos reais de lucro. |
| A câmera abre; clique em "Regime de Caixa": a tabela recalcula e aparece a faixa cinza do detalhamento por centro de custo; a câmera desce até "08 = Resultado do Período", "-R$ 31.500,00", na faixa vermelha. [ZOOM: a faixa e o valor, a frase inteira] [BACKEND: `get_financial_dre_summary` e `get_dre_expenses_by_group` com `p_regime` caixa (`costBasis` caixa)] | Clico em Regime de Caixa, e o mesmo mês vira um prejuízo de trinta e um mil e quinhentos reais. |
| A câmera sobe até a faixa cinza "O detalhamento por centro de custo fica disponível no regime de competência, cuja data contábil é compatível com os lançamentos categorizados." e fica nela. | No regime de caixa, a tela avisa: o detalhamento por centro de custo só fica disponível na competência. |
| A câmera abre e sobe até "04 (-) Custos Operacionais"; clique no grupo dele (a primeira troca para caixa remontou a tabela e os grupos voltaram fechados, `FinancialReport.tsx:644-661`): aparece a linha "CMV / Compras de materiais", R$ 256.860,00. [ZOOM: a linha com o valor, a frase inteira] Na frase "Em competência", clique em "Regime de Competência" (R$ 218.860,00); na frase "Em caixa", clique em "Regime de Caixa" (R$ 256.860,00); os dois já estão carregados e o grupo continua aberto; a câmera fica na linha, e só o valor troca. | A diferença está na linha CMV, Compras de materiais. O CMV é o custo da mercadoria vendida. Em competência, a linha traz só o custo do que saiu. Em caixa, traz tudo o que foi comprado no mês. |
| A câmera fica na linha (o mesmo zoom). | E a diferença entre os dois resultados é de trinta e oito mil reais: o ferro que ficou no pátio, pelo preço de compra. |
| A câmera abre na tabela inteira. | Quem compra muito e segura o material esperando preço vê prejuízo no caixa e lucro na competência. É normal, e é pra isso que existem os dois. |
| A câmera fica na tabela inteira. | Uma dica: se a competência avisar que tem material em estoque sem custo de compra cadastrado, o custo do que foi vendido pode estar menor do que o real. Vale conferir o cadastro desses materiais. |

### cap09 · O patrimônio de hoje (vinheta: PATRIMÔNIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE", em competência); a câmera desce até a faixa escura "Patrimônio Operacional Atual" e clica nela: abrem "Saldo em Caixa (Dinheiro)", "Saldo Bancário", "Contas a Receber", "Estoque (Projeção de Venda)", "Contas a Pagar" e "= Patrimônio Operacional Atual", com "Positivo". [BACKEND: `get_company_patrimony` com a foto de 10/11 do mundo] | No pé do DRE fica o Patrimônio Operacional Atual. Clico pra abrir. Ele mostra do que a empresa é feita hoje. |
| A câmera desce linha por linha. | Ele soma o dinheiro em caixa, o saldo dos bancos, o que os clientes devem, como o fiado da Fundição Bandeira do Vale, e o estoque. E tira o que a empresa deve aos fornecedores. |
| [ZOOM: "Estoque (Projeção de Venda)" e o valor, a frase inteira] | O estoque entra pela projeção de venda: quanto o material do pátio renderia, vendido hoje pelo preço de venda cadastrado. |
| [ILUSTRAÇÃO: A foto de agora: uma câmera fotografa o pátio de hoje (caixa, banco, a receber, as pilhas do estoque e, à parte, o que se deve); em "trocar o mês", um calendário volta de novembro para outubro e a foto continua igual] | Uma dica: o patrimônio não segue o filtro de período. Ele é a foto de agora, e trocar o mês não muda nada aqui. |
| (ilustração: a pilha do estoque ganha a etiqueta "vira dinheiro quando vender, pelo preço do dia") | E ele é uma projeção. O estoque só vira dinheiro quando for vendido, e pelo preço do dia. |
| A ilustração sai; a câmera aproxima do ícone "Exportar Patrimônio", no canto da faixa, sem clicar. | No canto, o Exportar Patrimônio abre esse bloco numa aba nova, pra imprimir ou guardar. |

### cap10 · Mês a mês (vinheta: EVOLUÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE"); a câmera desce até "Evolução Mensal": o gráfico com "Vendas", "Compras", "Resultado" e "Margem Bruta %" e a tabela "Mês", "Vendas", "Compras", "Margem", "Resultado", de "jun/26" a "nov/26". [BACKEND: `get_monthly_financial_evolution` (`p_months` 6); junho e julho zerados se o histórico começa em agosto] | Descendo mais, a Evolução Mensal, com os últimos seis meses. Ela não segue o filtro de período, porque a ideia é comparar um mês com o outro. |
| [ZOOM: a linha "out/26" da tabela, a frase inteira] | Repara em outubro: as compras foram as maiores dos seis meses, e o resultado caiu. É o ferro do pátio de novo. |
| A câmera abre e sobe até o cabeçalho da tabela do DRE; clique em "Comparar períodos": a janela "Comparar períodos", com "Período principal" "Outubro de 2026"; em "Comparar com", clique em "Período anterior" ("Setembro de 2026"); a "Prévia das colunas" mostra setembro e outubro. [BACKEND: `get_financial_dre_summary` de setembro] | Pra comparar o DRE inteiro, tem o Comparar períodos. Escolho Período anterior, que aqui é setembro. |
| O mouse passa por "Mesmo período no ano passado" e por "Outro período" ("Escolha datas personalizadas no calendário"), na janela "Comparar períodos"; o "Período anterior" continua marcado. | Dá pra comparar também com o mesmo período do ano passado ou com outras datas, até três comparações lado a lado. |
| Clique em "Aplicar comparação": a tabela ganha as colunas "Setembro de 2026" e "Outubro de 2026"; a câmera desce pelas linhas. | Aplico, e os dois meses ficam lado a lado, linha por linha. |
| A câmera fica nas linhas das categorias. | Uma dica: o DRE monta cada linha pelo nome da categoria. Por isso, renomear uma categoria muda o que entra na linha dela, até na comparação com os outros meses. |
| Clique em "Comparar períodos" e em "Remover comparações": a tabela volta a uma coluna ("Outubro de 2026"). | Pra voltar ao DRE de um mês só, é o Remover comparações. E o Excel do DRE sai com as mesmas colunas, mais a variação entre elas. |

### cap11 · Vai ter dinheiro? A DFC prevista (vinheta: DFC)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap02`; `setup`: "Mês passado", aba "Dashboard"). Clique na aba "DFC": os botões "Previsto" (marcado) e "Realizado", "Próximos" "15 dias" e "30 dias" e os cartões "Saldo atual", "A receber · 15 dias", "A pagar · 15 dias", "Dívidas a receber" e "Dívidas a pagar". [BACKEND: a previsão lê as tabelas `financial_bills`, `bank_accounts`, `cash_register` e `companies`; sem RPC] | O DRE diz se a empresa ganhou. A DFC, o demonstrativo do fluxo de caixa, diz se vai ter dinheiro. Ela abre no Previsto, que olha pra frente. |
| [ILUSTRAÇÃO: Olhando pra frente: um calendário de 15 dias; em cada dia, moedas entrando (verde) e saindo (vermelho) de um cofrinho; a linha do saldo sobe e desce de um dia para o outro] | Ele parte do saldo de hoje, soma o que você tem a receber e tira o que tem a pagar, dia por dia, pelas datas de vencimento. |
| A ilustração sai; a câmera fica nos cartões. [ZOOM: "Dívidas a receber" e "Dívidas a pagar", a frase inteira] | Em cima, o saldo atual, o que entra e o que sai nos próximos quinze dias, e as dívidas: o que já venceu e ninguém deu baixa. |
| A câmera desce para a tabela: "Fluxo de caixa", "Dívida" e uma coluna por dia, com "Saldo inicial", "Recebimentos", "Total de saídas" e "Saldo final". | Na tabela, cada coluna é um dia. O saldo final de um dia é o saldo inicial do outro. |
| Clique na seta de "Total de saídas": abrem as categorias (as maiores primeiro). | A seta do Total de saídas abre as categorias. |
| Clique num valor de "Total de saídas": a janela "Saídas · <dia>", "N lançamentos", com "Para editar ou dar baixa, abra o lançamento em Contas a Pagar/Receber."; fecha. | E clicando num valor, aparecem as contas daquele dia. Pra pagar ou mudar a data, o lugar é Contas a Pagar e Receber. |
| A câmera desce para "Saldo por conta", para o gráfico "Evolução do saldo" e para "O que já venceu e não foi baixado" (a conta de água vencida, "N dias em atraso"). | Embaixo, o saldo de cada conta, o gráfico do saldo e a lista do que já venceu, como a conta de água. |
| Clique em "30 dias": a tabela e os cartões recalculam. | Trocando pra trinta dias, a previsão vai mais longe. |
| A câmera para em "Previsão otimista: considera que tudo será pago e recebido no vencimento. O que já venceu aparece como dívida e não é descontado novamente do saldo.". [ZOOM: a frase, a frase inteira] | Uma dica: essa previsão é otimista. Ela conta que todo mundo paga no dia. E se uma conta bancária for ficar negativa, a tela avisa em vermelho, com o nome da conta e o dia. |
| A câmera abre. | O Previsto não segue o filtro de período. Ele sempre começa hoje. |

### cap12 · Por onde o dinheiro passou: a DFC realizada (vinheta: DFC)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DFC"). Clique em "Realizado": "Realizado em Outubro de 2026. Transferências entre contas próprias ficam fora." e os cartões "Entradas", "Saídas" e "Variação líquida". [BACKEND: o realizado lê `bank_transactions` e `cash_transactions` do período, com a categoria e o `cash_flow_group`] | O Realizado olha pra trás: o dinheiro que entrou e saiu de verdade do caixa e do banco. E esse segue o período, aqui outubro. |
| [ZOOM: "Variação líquida", com o valor, a frase inteira] | Em outubro saiu mais do que entrou. É a mesma história do regime de caixa: o ferro que ficou no pátio. |
| A câmera abre e desce para "Estrutura do DFC": as atividades, com "Entradas", "Saídas" e "Líquido". | A tabela separa o dinheiro por atividade: as operacionais, do dia a dia, as de investimento, como comprar uma máquina, e as de financiamento, como um empréstimo. |
| Clique numa atividade e numa categoria: abrem as categorias e as subcategorias. | Lembra do grupo do fluxo de caixa que a gente escolheu na categoria das máquinas? É ele que decide em qual atividade cada lançamento entra. |
| A câmera desce até "Variação líquida de caixa" e "Realizado dia a dia" ("Data", "Entradas", "Saídas", "Variação", "Saldo realizado"). | No fim, a variação do caixa no período. E embaixo, o realizado dia a dia. |
| A câmera sobe; clique em "Filtros": "Centros de custo"; marca "Coleta": "Filtros (1)" e "Filtro aplicado ao realizado e às exportações."; limpa o filtro. | Dá pra filtrar por centro de custo, e o filtro vale também pro arquivo exportado. |
| Clique em "Exportar": "Excel", "PDF" e "CSV"; fecha sem escolher. | E o Exportar gera a DFC em Excel, PDF ou CSV. |
| A câmera abre. | Transferência entre contas da própria empresa não aparece aqui: o dinheiro só mudou de lugar. E se algum valor estiver sem categoria de fluxo de caixa, a tela mostra um aviso amarelo pra você corrigir a categoria. |

### cap13 · O Histórico (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE"); clique na aba "Histórico": as abas "Receitas", "Despesas" e "Compras", com os contadores; abre em "Receitas". [BACKEND: `purchases` e `sales` de outubro; `get_dre_revenue_lines` e `get_dre_expense_lines` de outubro, sem o dinheiro que espelha compra ou venda] | Agora o Histórico, com os lançamentos do mês, um por um, separados em receitas, despesas e compras. |
| Clique em "Despesas": a barra "N lançamentos", com o total, e a lista, com a data, o selo da fonte ("Caixa" ou "Banco") e o selo da categoria. | Uma dica: o relatório não inventa número nenhum. Se um resultado parece estranho, a causa está num lançamento: uma categoria faltando, uma despesa esquecida, um saque lançado como despesa. Por isso, comece sempre por aqui. |
| Clique na caixa "Buscar por descrição, categoria ou valor...", digita "3850": ficam as duas contas de energia; apaga a busca. | A busca acha pela descrição, pela categoria ou pelo valor. Digitando três mil oitocentos e cinquenta, já aparecem as duas contas. |
| Clique em "Filtros": o painel "Filtros", com "Categoria", "Cliente/Fornecedor", "Centro de custo" e "Conta bancária" ("Todas as contas"); em "Categoria", marca "Energia elétrica"; clique em "Aplicar". [BACKEND: `get_dre_expense_lines` e `get_dre_revenue_lines` devolvem `bank_account_id` e `bank_account_name`; sem isso o campo "Conta bancária" não aparece] | Lembra da energia de outubro? Em Filtros, escolho a categoria Energia elétrica. Dá pra filtrar também por cliente ou fornecedor, por centro de custo e por conta bancária. |
| A lista mostra duas linhas "Conta de energia", "13/10/2026", selo "Banco", "Energia elétrica" e "-R$ 3.850,00" cada; a barra "2 lançamentos", "-R$ 7.700,00". [ZOOM: as duas linhas, com a data e o valor, a frase inteira] [BACKEND: as duas linhas em `bank_transactions` (13/10/2026 09:12 e 16:40), nenhuma conciliada nem ligada a conta a pagar] | Duas contas de energia, no mesmo dia e com o mesmo valor: três mil, oitocentos e cinquenta reais. A conta foi lançada em dobro. |
| Na linha das 09:12, clique na seta ("Ver detalhes"): a linha abre o detalhe, com "Descrição", "Valor", "Tipo", "Data do lançamento", "Registrado em", "Categoria", "Centro de custo", "Conta bancária" e "Anexos"; fecha. [ZOOM: o detalhe, a frase inteira] | Antes de excluir, eu abro o lançamento na seta do lado. Aparece tudo o que foi preenchido: a conta, a data, a categoria, a hora em que foi registrado e os anexos. Os dois são iguais, mas um foi registrado depois do outro: é a cópia. |
| A câmera abre; na linha das 16:40, clique na lixeira ("Excluir lançamento"): a janela "Excluir lançamento?", com "Essa ação não pode ser desfeita."; clique em "Excluir": aviso "Lançamento excluído."; fica uma linha, com "1 lançamento" e "-R$ 3.850,00". [BACKEND: as leituras do grupo e `delete_bank_transaction_atomic` (apaga e devolve R$ 3.850,00 ao saldo da conta); vira `apos-cap10`] | Clico na lixeira da primeira, a que foi lançada depois, e em Excluir. Pronto: ficou uma conta só, e o DRE e o patrimônio já recalcularam sozinhos. |
| A câmera aproxima da lixeira e do lápis ("Editar categoria") da linha que ficou, sem clicar. | A lixeira aparece nas despesas lançadas no banco, pra quem tem a permissão Gerenciar Contas Bancárias. E o lápis do lado troca a categoria de um lançamento do caixa ou do banco. |
| [ILUSTRAÇÃO: O mesmo dinheiro não conta duas vezes: dois cartões genéricos, "Compra de cobre: R$ 4.250" e "Pagamento no caixa: R$ 4.250", ligados por um sinal de igual, "o mesmo dinheiro"; em "nada é contado duas vezes", o segundo cartão esmaece e o total fica R$ 4.250, com um R$ 8.500 riscado ao lado] | Uma dica: o Histórico não repete o dinheiro de uma compra ou de uma venda que já está na lista. Assim, nada é contado duas vezes. Pra ver o caixa linha por linha, o lugar é o Histórico do Caixa. |
| Limpa os filtros, clique na aba "Compras"; clique na seta ("Ver detalhes do pedido") da compra do ferro pesado do Depósito Irmãos Siqueira: "Itens" e "Formas de pagamento". | Na aba Compras, e nas vendas dentro das Receitas, a seta abre o pedido, com os itens e as formas de pagamento. |

### cap14 · Vários lançamentos de uma vez (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap10` mais a variante `lote-categoria`; `setup`: "Mês passado", aba "Histórico", em "Despesas"). Digita "Diesel" na busca: os lançamentos "Diesel do caminhão truck" (02/10 e 16/10), "Diesel do caminhão 3/4" (09/10) e "Diesel e gasolina da picape" (23/10); três com o selo "Outras Despesas". [BACKEND: `_patch` das três despesas de diesel para "Outras Despesas"; `get_dre_expense_lines`] | Olha o diesel do caminhão em outubro: três lançamentos, e todos caíram em Outras Despesas. O certo era Combustível. Acontece: o lançamento entra com a categoria errada, e o relatório trata o diesel como uma despesa qualquer. |
| Na linha de 16/10, clique no lápis ("Editar categoria"): a janela "Editar categoria", "Pesquisar categoria...", "Sem categoria"; escolhe "Combustível"; "Salvar": aviso "Categoria atualizada". [BACKEND: RPC `update_financial_transaction_category`] | Num lançamento só, é o lápis: escolho a categoria certa e pronto. |
| Clique em "Selecionar": aparecem as caixas de marcar e a barra "0 lançamentos selecionados" e "Selecione até 100 lançamentos manuais de caixa ou banco."; marca os dois "Diesel do caminhão" que sobraram: "2 lançamentos selecionados". | Mas sobraram dois diesel na categoria errada. Pra não fazer um por um, clico em Selecionar e marco os dois. Dá pra marcar até cem de uma vez, do caixa e do banco. |
| Clique em "Alterar categoria": a janela "Alterar categoria de 2 lançamentos", "Despesas selecionadas", "2 no banco · Valores e saldos não mudam."; em "Nova categoria (despesa)", escolhe "Combustível". [ZOOM: o resumo e o campo, a frase inteira] | Em Alterar categoria, escolho a categoria nova. A janela avisa: os valores e os saldos não mudam, só a classificação. |
| Clique em "Aplicar categoria": aviso "Categoria de 2 lançamentos atualizada."; a seleção fecha e as linhas aparecem com o selo "Combustível". [BACKEND: RPC `update_financial_transaction_categories_batch` (`p_cash_ids`, `p_bank_ids`, `p_category_id`)] | Aplico, e os dois mudam juntos. O DRE e o Dashboard já recalculam com a categoria certa. |
| Clique em "Selecionar" de novo e marca duas linhas de banco: o botão vermelho "Excluir selecionados" fica ativo; clique em "Cancelar seleção". | Do lado fica o Excluir selecionados, pra apagar vários lançamentos de banco da mesma conta. Se um deles não puder ser excluído, nenhum é. |
| A câmera abre. | Uma dica: compra e venda não entram na seleção. A categoria delas vem do pedido. |

### cap15 · Exportar em Excel e PDF (vinheta: EXPORTAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap10`; `setup`: "Mês passado", aba "Histórico", em "Despesas", sem filtro); clique em "Exportar": o menu "Exportar histórico" ("PDF", "Excel") e "Fechamento contábil" ("Fechamento completo (Excel)"). | Pra levar tudo pro contador, tem o Exportar. |
| Clique em "PDF": a janela "Exportar Histórico (PDF)", "O arquivo sai com os filtros abaixo, que já vêm iguais aos da tela. Ajuste aqui se quiser exportar algo diferente."; em "Incluir no arquivo", "Receitas", "Despesas" e "Compras" marcados; "Período" "01/10/2026 a 31/10/2026". O mouse passa no campo "Conta bancária" ("Todas as contas"), que só aparece quando a lista tem conta bancária. | O histórico sai em PDF ou em Excel, com o período e os filtros da tela. Aqui eu escolho o que entra: receitas, despesas e compras. |
| Aviso "PDF gerado em nova aba". [PDF NA TELA: o app abre o PDF em aba nova e a gravação filma uma aba só; o robô devolve o PDF (`POPS` + `PDF_JS`, padrão do t08) para a cena "pdf" da ilustração `ilu15_historico_pdf`: o PDF aparece na tela durante esta fala] | O Excel é pra você mexer nos números. O PDF é pra mandar pro contador ou guardar. |
| De volta à aba do relatório; clique em "Exportar", depois em "Fechamento completo (Excel)": aviso "Fechamento gerado: N lançamentos, N contas em aberto e N pendências para revisar." [BACKEND: as RPCs do fechamento, inventário seção 4] | E o Fechamento completo, em Excel, monta o pacote do mês pro contador: os lançamentos, as contas em aberto e o estoque no fim do período. |
| Clique na aba "DRE"; clique no "Exportar" do cabeçalho: "Planilha Excel" e "Documento PDF"; fecha sem escolher. | E o DRE tem o Exportar dele, em Planilha Excel ou Documento PDF, do jeito que está na tela, com o período e o regime. |

### cap16 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cartão "Frete" com "Frete de entrega" e o selo; "Máquinas e veículos" em "Não compõe o DRE"; "Produção" na lista dos centros de custo. | Pronto! Recapitulando: a gente montou o plano de contas, com o frete de entrega em outro lugar do DRE e as máquinas fora do resultado. E criou o centro de custo da produção. |
| Montagem rápida: o filtro em "Mês passado", o banner "Superávit" e o "Top Clientes" em "Kg". | Abriu o relatório em outubro, leu o resultado e as despesas no Dashboard, e viu quem liderou entre os fornecedores e os clientes. |
| Montagem rápida: a troca de regime ("R$ 6.500,00" na faixa verde, "-R$ 31.500,00" na vermelha) e um quadro da ilustração do pátio. | Leu o DRE nos dois regimes, organizou as categorias dele, e viu, com o ferro do pátio, por que outubro deu lucro na competência e prejuízo no caixa. |
| Montagem rápida: o patrimônio aberto, a "Evolução Mensal" e as colunas de setembro e outubro. | Viu o patrimônio de hoje, a evolução dos últimos seis meses e a comparação com setembro. |
| Montagem rápida: a aba "DFC" no "Previsto" e no "Realizado". | Olhou a DFC, a prevista e a realizada, pra saber se vai ter dinheiro e por onde ele passou. |
| Montagem rápida: as duas contas de energia, o "Lançamento excluído." e o "Exportar PDF". | E achou a energia lançada em dobro no Histórico, excluiu, trocou a categoria de vários lançamentos de uma vez e exportou o histórico pro contador. |
| Cartão "Próximo: Cato, o assistente"; cartela final. | No próximo tutorial, a gente pergunta pro Cato em português e recebe a resposta pronta. Até lá! |
