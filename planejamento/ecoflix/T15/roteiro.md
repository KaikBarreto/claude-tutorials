# Roteiro T15 · Relatório Financeiro e DRE

Pronto para gerar a voz e gravar (sem etapa de aprovação; o Kaik ajusta depois). Coluna Fala = narração (voz Kaik Barreto) na
grafia da legenda; a grafia do TTS fica em `narracao/tts_textos.py`, gerado desta coluna (uma linha da tabela = uma linha da
fala). Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da 1.59.154
(`T15/inventario.md`). Mundo, valores e backend falso: `T15/plano.md`.

- **Título:** Relatório Financeiro e DRE
- **Antes:** Bancos, cofre e conciliação bancária (T14)
- **Próximo:** Cato, o assistente (T21)
- **Vinhetas (áreas):** CATEGORIAS · CENTROS DE CUSTO · RELATÓRIO · DASHBOARD · DASHBOARD · DRE · DRE · PATRIMÔNIO · EVOLUÇÃO ·
  HISTÓRICO · EXPORTAR · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~16 min de vídeo (2.236 palavras e 12.232 caracteres de fala, ~14,3 min de voz a 2,6 palavras/s,
  mais 12 vinhetas e as ações sem fala; alvo da fonte, ~17 min)
- **Aula:** computador, janela de 1280×800, logado como Rafael Nogueira (MASTER) do começo ao fim. `FAKE_NOW`
  2026-11-10T08:30:00-03:00; o mês lido é outubro ("Mês passado"). Cada capítulo abre um navegador novo, com o mundo do fim do
  anterior (`seeds-extra/t15/inicio`, `apos-cap01`, `apos-cap02`, `apos-cap10`); do capítulo 4 ao 11, o `setup` abre o
  relatório, escolhe "Mês passado" e a aba de partida fora do vídeo.
- **Marcas na coluna Tela:** `[BACKEND: ...]` (o que o backend falso ainda não tem), `[ZOOM: ...]` (dura a frase inteira, nunca
  em cima de outro zoom: entre dois, "a câmera abre"), `[ILUSTRAÇÃO: ...]` (cena HTML da marca, `docs/09-aula-ilustrada.md`:
  fundo branco, Montserrat, acento #50D088, objetos genéricos, nunca tela do app), `[TESTAR ...]` (o robô confere antes).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Relatório Financeiro e DRE". | (sem fala) |
| Dashboard do EcoSistema (tela inicial), logado como Rafael Nogueira; a câmera fica no geral, sem zoom. [BACKEND: semente `seeds-extra/t15/inicio.json`: o fim do T14 mais o "Mundo: o que esta aula precisa" do plano] | Oi! Neste tutorial a gente vai responder a pergunta que todo dono faz no fim do mês: eu ganhei ou perdi dinheiro? E por quê? |
| [ILUSTRAÇÃO: O mês do pátio: um galpão genérico; em "encheu o pátio de ferro", dois caminhões descarregam e a pilha de ferro cresce; em "saiu mais dinheiro", um cofrinho esvazia, com moedas saindo mais do que entrando; em "ganhou ou perdeu", um ponto de interrogação entre um selo verde "Lucro?" e um vermelho "Prejuízo?"] | Em outubro, a Recicla Vale Metais vendeu bem e ainda encheu o pátio de ferro. Mesmo assim, saiu mais dinheiro do que entrou. Afinal, ela ganhou ou perdeu? |
| A ilustração sai; volta o Dashboard. | Pra responder, a gente vai arrumar as categorias e os centros de custo, ler o Relatório Financeiro e o DRE, e exportar tudo pro contador. |
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
| A câmera abre; em "Categorias de despesa", clique em "Nova": abre "Nova categoria", com "Tipo" em "Despesa"; em "Nome", digita "Máquinas e veículos". | Agora, uma categoria que pede cuidado: a compra de máquina ou de caminhão. |
| [ILUSTRAÇÃO: Nem toda saída é despesa, três cartões, um por linha. Cartão 1, nesta linha: um caminhão e uma prensa genéricos comprados; a seta vai para "bem da empresa", e um "despesa do mês" riscado] | Uma dica: comprar uma prensa ou um caminhão não é despesa do mês. O dinheiro vira um bem da empresa. |
| (ilustração, cartão 2: o dinheiro do empréstimo entra e a parcela devolve, os dois só trocam de lugar; a parcela se parte em dois lançamentos, "valor emprestado" e "juros", e só "juros" desce para "resultado") | Com empréstimo é parecido. Receber não é receita, e devolver o valor emprestado não é despesa. Só os juros entram no resultado. Se a parcela mistura os dois, são dois lançamentos. |
| (ilustração, cartão 3: o lucro saindo para os sócios, também fora de "despesa") | E a distribuição de lucro pros sócios também fica fora da despesa. |
| A ilustração sai. Em "Onde aparece no DRE", escolhe "Não compõe o DRE" ("Movimentação patrimonial: aparece no caixa, mas não no DRE."); a prévia mostra "informativo" e "No padrão atual, não altera o resultado.". Em "Grupo no Fluxo de Caixa (DFC)", escolhe "Atividades de investimento" ("Compra ou venda de máquinas, veículos e outros ativos."). | Por isso, essa categoria vai em Não compõe o DRE: o dinheiro sai do caixa, mas o resultado não muda. E no fluxo de caixa, que acompanha o caminho do dinheiro, ela fica em Atividades de investimento. |
| Clique em "Criar categoria": aviso "Categoria criada"; "Máquinas e veículos" aparece na divisória "Não compõe o DRE". [BACKEND: insert (`dre_group` outros, `cash_flow_group` investimento, sem `dre_group_id`); com o Frete de entrega, vira `apos-cap01`] | Pronto. O EcoSistema registra a compra. O controle dos bens, a depreciação da máquina e o ganho ou a perda quando ela for vendida ficam com o contador. Na dúvida sobre onde uma categoria entra, é ele quem orienta. |

### cap02 · Centros de custo (vinheta: CENTROS DE CUSTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap01`, na tela "Categorias Financeiras"); no menu da tela, clique em "Centros de custo": "Centros de custo", "Agrupe receitas e despesas por setor para saber quanto cada área gasta. É opcional em cada lançamento." e a lista com "Coleta" e "Pátio". | Com as categorias certas, dá pra saber em que o dinheiro foi gasto. O centro de custo responde onde: em qual frente da empresa. |
| [ILUSTRAÇÃO: As frentes do pátio: um pátio genérico dividido em três áreas coloridas; "Pátio" (âmbar: balança e pilhas de sucata) recebe as contas de energia e de aluguel; "Coleta" (azul: caminhão e caçamba) recebe o diesel e a manutenção; "Produção" (roxo: uma prensa fazendo fardos de latinha) entra por último, ainda sem conta] | Na Recicla Vale Metais, o pátio fica com a energia e o aluguel, e a coleta fica com o combustível e a manutenção do caminhão. Assim, cada frente mostra quanto custa. |
| A ilustração sai. Clique em "Novo centro de custo": "Novo centro de custo", "Defina um nome e uma cor para identificar o setor nos lançamentos."; em "Nome", digita "Produção"; em "Cor", clica no roxo ("Cor #8B5CF6"); em "Descrição", digita "Prensa de latinha e papelão". | A terceira frente vai ser a produção, a prensa que enfarda latinha e papelão. Coloco o nome, uma cor pra achar rápido nos gráficos e uma descrição. |
| [ZOOM: o interruptor "Ativo", ligado, com "Centros inativos deixam de aparecer nos formulários de lançamento, mas seguem nos lançamentos antigos.", a frase inteira] | Uma dica: quando uma frente parar, é só desligar o Ativo. Ela sai dos formulários e continua nos lançamentos antigos. Excluir não apaga lançamento nenhum, só tira a marcação, e eles ficam sem centro de custo. |
| A câmera abre; clique em "Salvar": aviso "Centro de custo criado"; "Produção" entra na lista. [BACKEND: insert em `cost_centers` (`name` Produção, `color` #8B5CF6, `description`, `is_active` true); vira `apos-cap02`] | Salvei. Daqui pra frente, o Centro de custo aparece como opção nos lançamentos de despesa e de receita, no caixa, no banco e nas contas a pagar e receber. |

### cap03 · O Relatório Financeiro (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap02`, no Dashboard); abre o menu "Financeiro" e clica em "Relatório Financeiro": "Relatório Financeiro", "Visão completa das finanças do seu negócio", o filtro em "Este mês" e as abas, na aba "Dashboard". [BACKEND: `localStorage` sem "financial-report-tab"; as RPCs do relatório no backend falso (plano, "Gravação")] | Plano de contas pronto. Agora, o relatório. No menu, Financeiro, Relatório Financeiro. |
| Clique no filtro de período: a lista "Todos os tempos", "Hoje", "Últimos 7 dias", "Este mês", "Mês passado", "Últimos 30 dias", "Este ano" e "Personalizado"; escolhe "Mês passado", e a tela recarrega com outubro. | Em cima fica o período. A tela sempre abre em Este mês, e novembro mal começou. Então eu escolho Mês passado, e a tela inteira passa a mostrar outubro. |
| A câmera fica no filtro, agora em "Mês passado". | Se um dia o relatório parecer vazio, confere o período primeiro. |
| A câmera passa pelas abas "Dashboard", "DRE", "DFC", "Centros de Custo" e "Histórico". | Embaixo ficam as abas. Nesta aula, a gente passa pelo Dashboard, pelo DRE, pelos Centros de Custo e pelo Histórico. E a tela volta sempre na última aba que você abriu. |
| Clique em "Centros de Custo": os cartões "Receitas financeiras", "Despesas financeiras", "Resultado das movimentações" e "Cobertura por centro de custo" e o gráfico "Receitas x despesas por centro"; a câmera desce até o "Ranking dos centros de custo" ("Pátio", "Coleta" e "Sem centro de custo", com "Não classificado"). [BACKEND: `get_financial_dre_summary` de outubro e de setembro, com `costCenters` por categoria (plano, "Mundo")] | Nos Centros de Custo aparece o resultado de cada frente. Em outubro, quem mais gastou foi o pátio, com a folha, o aluguel e a energia. A coleta gastou menos, e ainda trouxe a receita do aluguel de caçamba. |
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
| A câmera abre e passa pelo "Ver todos", sem clicar. | E o Ver todos abre a lista completa. |
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
| A câmera abre e desce até "08 = Resultado do Período", "R$ 6.500,00", na faixa verde. [ZOOM: a faixa e o valor, a frase inteira] | No fim, o resultado de outubro: seis mil e quinhentos reais, na faixa verde. |
| A câmera abre na tabela. | E lembra da categoria das máquinas? O que fica em Não compõe o DRE não aparece aqui. |

### cap07 · Caixa ou competência (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE"); a câmera vai aos botões "Regime de Caixa" e "Regime de Competência" (marcado). | No cabeçalho do DRE fica o botão que mais gera dúvida: Regime de Caixa ou Regime de Competência. O DRE abre em competência. |
| Passa o mouse em "Regime de Caixa": a dica "Considera todo o dinheiro que entrou e saiu no período. Mostra sua situação de caixa, mas o material que você comprou e ainda está no estoque conta como custo agora, mesmo sem ter sido vendido.". [ZOOM: a dica, a frase inteira] | No caixa, conta todo o dinheiro que entrou e saiu no mês. O material comprado já vira custo, mesmo que ainda esteja no pátio. |
| A câmera abre; passa o mouse em "Regime de Competência": a dica "Considera só o custo do material que você realmente vendeu no período. O que está parado no estoque não abate o lucro até ser vendido. É o lucro contábil do negócio.". [ZOOM: a dica, a frase inteira] | Na competência, conta só o custo do material que foi vendido. O que está parado no estoque espera a venda. |
| [ILUSTRAÇÃO: O exemplo do pátio, com o ferro pesado de outubro, um passo por linha. Passo 1, nesta linha: um caminhão descarrega 50 t no pátio; o cartão "50 t × R$ 0,95/kg = R$ 47.500" sai de um cofrinho] | Pensa no ferro pesado de outubro. A Recicla Vale Metais comprou cinquenta toneladas, a noventa e cinco centavos o quilo. Saíram quarenta e sete mil e quinhentos reais. |
| (ilustração, passo 2: um caminhão leva 10 t para o cliente; o cartão "10 t × R$ 1,25/kg = R$ 12.500" entra no cofrinho; ficam 40 t no pátio) | E vendeu só dez toneladas, a um real e vinte e cinco o quilo. Entraram doze mil e quinhentos. |
| (ilustração, passo 3: acende a coluna "Caixa", com um bolso: "R$ 12.500 − R$ 47.500 = −R$ 35.000", em vermelho) | No caixa, a conta é o que entrou menos o que saiu: um prejuízo de trinta e cinco mil reais. É a verdade do bolso. |
| (ilustração, passo 4: acende a coluna "Competência": "R$ 12.500 − R$ 9.500 (o custo das 10 t) = +R$ 3.000", em verde; em "as outras quarenta toneladas", a pilha do pátio ganha a etiqueta "estoque: R$ 38.000") | Na competência, o custo é só o das dez toneladas vendidas: nove mil e quinhentos. Sobra um lucro de três mil. E as outras quarenta toneladas continuam no pátio, valendo trinta e oito mil reais como estoque. |
| (ilustração, passo 5: embaixo de cada coluna, a pergunta dela: "Quanto dinheiro sobrou?" no caixa e "Estou ganhando no que vendo?" na competência) | Nenhum dos dois está errado. O caixa responde quanto dinheiro sobrou. A competência responde se você está ganhando no que vende. |
| A ilustração sai; volta o DRE em competência. [ZOOM: "08 = Resultado do Período", "R$ 6.500,00", a frase inteira] | Agora no DRE de verdade, com o mês inteiro. Em competência, outubro deu seis mil e quinhentos reais de lucro. |
| A câmera abre; clique em "Regime de Caixa": a tabela recalcula e aparece a faixa cinza do detalhamento por centro de custo; a câmera desce até "08 = Resultado do Período", "-R$ 31.500,00", na faixa vermelha. [ZOOM: a faixa e o valor, a frase inteira] [BACKEND: `get_financial_dre_summary` e `get_dre_expenses_by_group` com `p_regime` caixa (`costBasis` caixa)] | Clico em Regime de Caixa, e o mesmo mês vira um prejuízo de trinta e um mil e quinhentos reais. |
| A câmera abre e sobe até a linha "CMV / Compras de materiais", em "04 (-) Custos Operacionais". [ZOOM: a linha com o valor, a frase inteira] Na frase "Em competência", clique em "Regime de Competência" (R$ 218.860,00); na frase "Em caixa", clique em "Regime de Caixa" (R$ 256.860,00). | A diferença está na linha CMV, Compras de materiais. O CMV é o custo da mercadoria vendida. Em competência, a linha traz só o custo do que saiu. Em caixa, traz tudo o que foi comprado no mês. |
| A câmera fica na linha (o mesmo zoom). | E a diferença entre os dois resultados é de trinta e oito mil reais: o ferro que ficou no pátio, pelo preço de compra. |
| A câmera abre na tabela inteira. | Quem compra muito e segura o material esperando preço vê prejuízo no caixa e lucro na competência. É normal, e é pra isso que existem os dois. |

### cap08 · O patrimônio de hoje (vinheta: PATRIMÔNIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE", em competência); a câmera desce até a faixa escura "Patrimônio Operacional Atual" e clica nela: abrem "Saldo em Caixa (Dinheiro)", "Saldo Bancário", "Contas a Receber", "Estoque (Projeção de Venda)", "Contas a Pagar" e "= Patrimônio Operacional Atual", com "Positivo". [BACKEND: `get_company_patrimony` com a foto de 10/11 do mundo] | No pé do DRE fica o Patrimônio Operacional Atual. Clico pra abrir. Ele mostra do que a empresa é feita hoje. |
| A câmera desce linha por linha. | Ele soma o dinheiro em caixa, o saldo dos bancos, o que os clientes devem, como o fiado da Fundição Bandeira do Vale, e o estoque. E tira o que a empresa deve aos fornecedores. |
| [ZOOM: "Estoque (Projeção de Venda)" e o valor, a frase inteira] | O estoque entra pela projeção de venda: quanto o material do pátio renderia, vendido hoje pelo preço de venda cadastrado. |
| [ILUSTRAÇÃO: A foto de agora: uma câmera fotografa o pátio de hoje (caixa, banco, a receber, as pilhas do estoque e, à parte, o que se deve); em "trocar o mês", um calendário volta de novembro para outubro e a foto continua igual] | Uma dica: o patrimônio não segue o filtro de período. Ele é a foto de agora, e trocar o mês não muda nada aqui. |
| (ilustração: a pilha do estoque ganha a etiqueta "vira dinheiro quando vender, pelo preço do dia") | E ele é uma projeção. O estoque só vira dinheiro quando for vendido, e pelo preço do dia. |
| A ilustração sai; a câmera aproxima do ícone "Exportar Patrimônio", no canto da faixa, sem clicar. | No canto, o Exportar Patrimônio abre esse bloco numa aba nova, pra imprimir ou guardar. |

### cap09 · Mês a mês (vinheta: EVOLUÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE"); a câmera desce até "Evolução Mensal": o gráfico com "Vendas", "Compras", "Resultado" e "Margem Bruta %" e a tabela "Mês", "Vendas", "Compras", "Margem", "Resultado", de "jun/26" a "nov/26". [BACKEND: `get_monthly_financial_evolution` (`p_months` 6); junho e julho zerados se o histórico começa em agosto] | Descendo mais, a Evolução Mensal, com os últimos seis meses. Ela não segue o filtro de período, porque a ideia é comparar um mês com o outro. |
| [ZOOM: a linha "out/26" da tabela, a frase inteira] | Repara em outubro: as compras foram as maiores dos seis meses, e o resultado caiu. É o ferro do pátio de novo. |
| A câmera abre e sobe até o cabeçalho da tabela do DRE; clique em "Comparar períodos": a janela "Comparar períodos", com "Período principal" "Outubro de 2026"; em "Comparar com", clique em "Período anterior" ("Setembro de 2026"); a "Prévia das colunas" mostra setembro e outubro. [BACKEND: `get_financial_dre_summary` de setembro] | Pra comparar o DRE inteiro, tem o Comparar períodos. Escolho Período anterior, que aqui é setembro. |
| Clique em "Aplicar comparação": a tabela ganha as colunas "Setembro de 2026" e "Outubro de 2026"; a câmera desce pelas linhas. | Aplico, e os dois meses ficam lado a lado, linha por linha. |
| A câmera fica nas linhas das categorias. | Uma dica: o DRE monta cada linha pelo nome da categoria. Por isso, renomear uma categoria muda o que entra na linha dela, até na comparação com os outros meses. |

### cap10 · O Histórico (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`setup`: "Mês passado", aba "DRE"); clique na aba "Histórico": as abas "Receitas", "Despesas" e "Compras", com os contadores; abre em "Receitas". [BACKEND: `purchases` e `sales` de outubro; `get_dre_revenue_lines` e `get_dre_expense_lines` de outubro, sem o dinheiro que espelha compra ou venda] | Agora o Histórico, com os lançamentos do mês, um por um, separados em receitas, despesas e compras. |
| Clique em "Despesas": a barra "N lançamentos", com o total, e a lista, com a data, o selo da fonte ("Caixa" ou "Banco") e o selo da categoria. | Uma dica: o relatório não inventa número nenhum. Se um resultado parece estranho, a causa está num lançamento: uma categoria faltando, uma despesa esquecida, um saque lançado como despesa. Por isso, comece sempre por aqui. |
| Clique em "Filtros": o painel "Filtros", com "Categoria", "Cliente/Fornecedor", "Centro de custo" e "Fonte"; em "Categoria", marca "Energia elétrica"; clique em "Aplicar". | Lembra da energia de outubro? Em Filtros, escolho a categoria Energia elétrica. Dá pra filtrar também por cliente ou fornecedor, por centro de custo e pela fonte. |
| A lista mostra duas linhas "Conta de energia", "13/10/2026", selo "Banco", "Energia elétrica" e "-R$ 3.850,00" cada; a barra "2 lançamentos", "-R$ 7.700,00". [ZOOM: as duas linhas, com a data e o valor, a frase inteira] [BACKEND: as duas linhas em `bank_transactions` (13/10/2026 09:12 e 16:40), nenhuma conciliada nem ligada a conta a pagar] | Duas contas de energia, no mesmo dia e com o mesmo valor: três mil, oitocentos e cinquenta reais. A conta foi lançada em dobro. |
| A câmera abre; na linha das 16:40, clique na lixeira ("Excluir lançamento"): a janela "Excluir lançamento?", com "Essa ação não pode ser desfeita."; clique em "Excluir": aviso "Lançamento excluído."; fica uma linha, com "1 lançamento" e "-R$ 3.850,00". [BACKEND: as leituras do grupo e `delete_bank_transaction_atomic` (apaga e devolve R$ 3.850,00 ao saldo da conta); vira `apos-cap10`] | Clico na lixeira da segunda e em Excluir. Pronto: ficou uma conta só, e o DRE e o patrimônio já recalcularam sozinhos. |
| A câmera aproxima da lixeira e do lápis ("Editar categoria") da linha que ficou, sem clicar. | A lixeira aparece nas despesas lançadas no banco. E o lápis do lado troca a categoria de um lançamento do caixa ou do banco. |
| [ILUSTRAÇÃO: O mesmo dinheiro não conta duas vezes: dois cartões genéricos, "Compra de cobre: R$ 4.250" e "Pagamento no caixa: R$ 4.250", ligados por um sinal de igual, "o mesmo dinheiro"; em "nada é contado duas vezes", o segundo cartão esmaece e o total fica R$ 4.250, com um R$ 8.500 riscado ao lado] | Uma dica: o Histórico não repete o dinheiro de uma compra ou de uma venda que já está na lista. Assim, nada é contado duas vezes. Pra ver o caixa linha por linha, o lugar é o Histórico do Caixa. |

### cap11 · Exportar em Excel e PDF (vinheta: EXPORTAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap10`; `setup`: "Mês passado", aba "Histórico", em "Despesas", sem filtro); clique em "Exportar": o menu "Exportar histórico" ("PDF", "Excel") e "Fechamento contábil" ("Fechamento completo (Excel)"). | Pra levar tudo pro contador, tem o Exportar. |
| Clique em "PDF": a janela "Exportar Histórico (PDF)", "O arquivo sai com os filtros abaixo, que já vêm iguais aos da tela. Ajuste aqui se quiser exportar algo diferente."; em "Incluir no arquivo", "Receitas", "Despesas" e "Compras" marcados; "Período" "01/10/2026 a 31/10/2026". | O histórico sai em PDF ou em Excel, com o período e os filtros da tela. Aqui eu escolho o que entra: receitas, despesas e compras. |
| Clique em "Exportar PDF": aviso "PDF gerado em nova aba". [TESTAR: a aba nova com o PDF do app; se o gravador não seguir a aba, a câmera fica no aviso] | O Excel é pra você mexer nos números. O PDF é pra mandar pro contador ou guardar. |
| De volta à aba do relatório; clique em "Exportar", e a câmera para em "Fechamento completo (Excel)", sem clicar; fecha o menu. | E o Fechamento completo, em Excel, monta o pacote do mês pro contador: os lançamentos, as contas em aberto e o estoque no fim do período. |
| Clique na aba "DRE"; clique no "Exportar" do cabeçalho: "Planilha Excel" e "Documento PDF"; fecha sem escolher. | E o DRE tem o Exportar dele, em Planilha Excel ou Documento PDF, do jeito que está na tela, com o período e o regime. |

### cap12 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cartão "Frete" com "Frete de entrega" e o selo; "Máquinas e veículos" em "Não compõe o DRE"; "Produção" na lista dos centros de custo. | Pronto! Recapitulando: a gente montou o plano de contas, com o frete de entrega em outro lugar do DRE e as máquinas fora do resultado. E criou o centro de custo da produção. |
| Montagem rápida: o filtro em "Mês passado", o banner "Superávit" e o "Top Clientes" em "Kg". | Abriu o relatório em outubro, leu o resultado e as despesas no Dashboard, e viu os maiores fornecedores e clientes do mês. |
| Montagem rápida: a troca de regime ("R$ 6.500,00" na faixa verde, "-R$ 31.500,00" na vermelha) e um quadro da ilustração do pátio. | Leu o DRE nos dois regimes e viu, com o ferro do pátio, por que outubro deu lucro na competência e prejuízo no caixa. |
| Montagem rápida: o patrimônio aberto, a "Evolução Mensal" e as colunas de setembro e outubro. | Viu o patrimônio de hoje, a evolução dos últimos seis meses e a comparação com setembro. |
| Montagem rápida: as duas contas de energia, o "Lançamento excluído." e o "Exportar PDF". | E achou a energia lançada em dobro no Histórico, excluiu, e exportou o histórico pro contador. |
| Cartão "Próximo: Cato, o assistente"; cartela final. | No próximo tutorial, a gente pergunta pro Cato em português e recebe a resposta pronta. Até lá! |
