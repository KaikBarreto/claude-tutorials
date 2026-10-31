# Roteiro T8 · Estoque, compras e inventário

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T08/inventario.md`).
Aula no computador (janela de 1024 px ou mais), logada como Camila Duarte (admin) do começo ao fim. Todos os nomes, valores e datas
são fictícios; os dias do Kardex, da Posição e do Relatório são relativos ao dia da gravação (relógio travado no `FAKE_NOW`).

- **Título final:** Estoque, compras e inventário
- **Vinhetas (áreas):** ESTOQUE · LOCAIS · HISTÓRICO · COMPRAS · NOTA FISCAL · INVENTÁRIO · POSIÇÃO · RELATÓRIO · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Área do Técnico: Refrigeração e Climatização (T18)
- **Próximo:** Orçamentos, Precificação e Proposta (T9)
- **Duração estimada:** ~19 min de vídeo (2.443 palavras de fala, ~15,7 min de voz a 2,6 palavras/s, mais vinhetas e pausas do robô; o plano previa ~24 min com a compra direta em capítulo próprio, a fala segue o tempo natural)
- **Estado inicial (fim do T2; o T18 não altera dados):** Glacial Cold Brasil, Camila Duarte (admin) logada, oito usuários ativos (T2, com Rafael Lima), OS #1 a #16 (a #16 concluída no T7, com a baixa de Limpa-evaporador e Fita isolante no Kardex),
  cinco fornecedores no cadastro (Polar Distribuidora de Peças Ltda, Gelo Norte Componentes Ltda com o CNPJ 91.345.602/0001-36, Cobre Sul Suprimentos Ltda, Distribuidora Aurora de Peças Ltda e Ventura Gás e Tubos).
  **Entra por seed de bastidor, antes do cap01:** só o local "Estoque Principal" (padrão); grupos Gases, Cobre e tubos, Elétrica e Consumíveis; nove materiais, EST-001 a EST-009 (saldo, mínimo, custo e venda em R$):
  Gás refrigerante R-410A (kg) 8,5, mín. 10, 90,00 e 150,00 · Gás refrigerante R-32 (kg) 6, mín. 4, 98,00 e 160,00 · Tubo de cobre 1/4" (m) 45, mín. 30, 16,00 e 28,00 · Tubo de cobre 3/8" (m) 12, mín. 20, 26,00 e 42,00 ·
  Mangueira de dreno (m) 60, mín. 25, 3,50 e 8,00 · Capacitor 35 µF (un) 9, mín. 4, 34,00 e 62,00 · Limpa-evaporador em spray (un) 10, mín. 6, 20,00 e 38,00 · Fita isolante 28, mín. 12, 6,50 e 11,00 ·
  Suporte para condensadora 8, mín. 4, 48,00 e 85,00 (o T9 usa os quatro valores fixados no plano dele). Histórico: "Cadastro inicial" de cerca de 90 dias antes, duas compras recebidas de R-410A (20 kg a 86,00, 60 dias antes, e 15 kg a 90,00, 25 dias antes)
  e os movimentos do mês (as duas linhas de Consumo da OS #16).
- **Criado ao vivo:** material **Capacitor 40 µF** (EST-010, grupo Elétrica, fornecedor Polar, 6 un, custo 38,90, venda 70,00, mínimo 4); entrada de 10 de Fita isolante e saída de 3 capacitores; local **Van 01** (gases e Fita isolante; acesso só do Rafael Lima);
  transferência de 2 kg de R-410A; requisição **Reposição de gás, cobre e capacitor** (R-410A 10 kg, Tubo de cobre 3/8" 20 m, Capacitor 40 µF 6 un) com três cotações completas (Ventura Gás e Tubos 94,00, 29,50 e 39,00, total 1.764,00; Cobre Sul 98,00, 27,00 e 38,00, total 1.748,00, a "Mais barata";
  Polar 99,00, 31,00 e 36,00, total 1.826,00) e fornecedor escolhido por material (R-410A na Ventura, Tubo na Cobre Sul, Capacitor na Polar); três ordens de compra (Ventura Recebida, +10 kg de R-410A; Cobre Sul Recebida parcial, +10 m de 20; Polar em Rascunho);
  nota fiscal da Gelo Norte (Capacitor 40 µF 440V 10 un a 37,00, Contator 25 A 4 un a 58,00 e Filtro secador 6 un a 21,50, total 731,00; os dois últimos são criados); inventário de Gases e Elétrica no Estoque Principal, finalizado (R-410A contado 16 contra 16,5; Capacitor 35 µF contado 8 contra 9).
- **Estado final:** Estoque Principal com R-410A 16, R-32 6, Tubo 1/4" 45, Tubo 3/8" 22, Mangueira 60, Capacitor 35 µF 8, Capacitor 40 µF 13, Limpa-evaporador 10, Fita isolante 38, Suporte 8, Contator 25 A 4 e Filtro secador 6; Van 01 com R-410A 2 kg (Fita e R-32 zerados);
  uma requisição, três cotações, três ordens, uma nota importada e um inventário finalizado. Vira `seeds-extra/t8/apos-cap15.json`; o T9 parte dele (custo e venda do R-410A, Limpa-evaporador, Fita isolante e Mangueira de dreno).
- Decisões padrão: a compra direta só é citada (cap08), sem clicar: o tutorial Financeiro (T13) a demonstra, por isso não há semente financeira no T8; fora do vídeo o que a trilha promete e o código não faz ("Categoria" no cadastro, "cotação vencedora", compra montada pela NF-e);
  as três cotações cobrem os três materiais, para o selo "Mais barata" (menor total) não confundir, e o texto fala da escolha por material; nenhum clique em "Aceitar" cotação, "Excluir" material, "Cancelar inventário", "Excluir ordem", "Exportar PDF", "Exportar Excel" nem "Baixar PDF" (a câmera só passa);
  sem foto de material; subtítulo "Operacional" das abas de local ignorado; "Nota já importada" só falado; sem preço de plano; Fita isolante parte de 28 (fim do T7), não de 29 como no plano; o "Itens abaixo do mínimo" adiciona todos os listados (não há caixa por item).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[ILUSTRAÇÃO: ...]` (nenhuma nesta aula).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Estoque, compras e inventário". | (sem fala) |
| Dashboard da Dominex, logado como Camila Duarte (Glacial Cold Brasil); a câmera desliza pelo menu lateral até o grupo "Gestão" e para em "Estoque"; clique: abre a tela "Estoque" ("Controle de peças e materiais"). | Oi! Neste tutorial a gente vai cuidar do que a Glacial Cold Brasil tem guardado: os materiais, os locais onde eles ficam, as compras para repor e a contagem. |
| A câmera percorre as seis abas da tela. | Quando o técnico usa um gás, quando chega uma entrega, quando uma peça está acabando, tudo passa por aqui. Você sabe o que tem, onde está e quanto custou. |
| Cartão discreto: "Antes: Área do Técnico: Refrigeração e Climatização". | Se você ainda não viu o tutorial Área do Técnico: Refrigeração e Climatização, dá uma olhada antes. [pause] Vamos conhecer a tela. |

### cap01 · A tela e as seis abas (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Zoom no cabeçalho: título "Estoque", subtítulo "Controle de peças e materiais" e, à direita, os botões "Importar XML (NF-e)" e "Configurações" (só a câmera passa). Depois a barra de abas: "Estoque Atual", "Histórico de Materiais (Kardex)", "Compras de Material", "Inventários", "Posição de Estoque" e "Relatório". [BACKEND: semente de estoque do T8 (`stocks`, `material_groups`, `inventory`, `inventory_stock_levels` com mínimo e presença, `inventory_movements` coerentes em duas épocas); handler de `get_accessible_inventory_ids` (sem ele a tabela "Estoque Atual" aparece vazia); unidades só as da lista do app (un, kg, l, m, cx, pc)] | A tela tem seis abas: Estoque Atual, Histórico de Materiais, que é o Kardex, Compras de Material, Inventários, Posição de Estoque e Relatório. Lá em cima ficam também os botões Importar XML da NF-e e Configurações, que a gente usa mais à frente. |
| Na aba "Estoque Atual" (um só local, sem abas de local): zoom nos cartões "Total de itens", "Valor investido (R$)" e "Estoque baixo" (2). | Começo pelo Estoque Atual. Os três cartões resumem o estoque: o total de itens, o valor investido, que é a quantidade vezes o custo de cada material, e quantos itens estão com estoque baixo. |
| Clique em "Buscar por nome, código ou categoria...", digita "fita": a lista filtra; limpa o campo. Clique em "Filtros": a caixa "Estoque abaixo do mínimo" e a lista "Grupo"; fecha. | Pra achar um material, é só buscar pelo nome ou pelo código. Em Filtros, dá pra ver só o que está abaixo do mínimo, ou só um grupo. |
| A câmera percorre o cartão "Itens do Estoque": colunas "Nome", "SKU", "Categoria" (mostra o grupo, em selo com bolinha de cor), "Quantidade", "Qtd. mínima" e "Custo Unit."; para nas linhas do "Gás refrigerante R-410A" e do "Tubo de cobre 3/8"", com o triângulo vermelho e o fundo avermelhado; hover no triângulo do gás: dica "Estoque abaixo do mínimo: 8,5 de 10". | Cada linha traz o nome, o código, o grupo, a quantidade, a quantidade mínima e o custo unitário. Repara nestas duas, com o triângulo vermelho: estão abaixo do mínimo. O gás tem oito vírgula cinco, e o mínimo é dez. |
| Clique em "Exportar": o menu com "PDF" e "Excel"; clique em "PDF": abre a janela "Selecionar materiais" (a câmera passa; fecha em "Cancelar" sem gerar arquivo). [NÃO baixar: o gravador não captura download] | Pra levar o estoque pra fora, o Exportar gera um PDF ou uma planilha do Excel, com os materiais que você escolher. |

### cap02 · Cadastrar um material (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Clique em "Cadastrar Material": abre a janela "Novo Item de Estoque". Em "Nome do Item *" digita "Capacitor 40 µF". [BACKEND: `register_inventory_movement` ("Cadastro inicial") e `set_inventory_presence`; o código sugerido olha os `EST-` já existentes] | Vamos cadastrar um material do zero. Clico em Cadastrar Material e dou o nome: Capacitor 40 µF. |
| A câmera para em "Código/SKU", já preenchido com "EST-010", no botão "Auto" e na dica "Código sequencial sugerido automaticamente (você pode personalizar)." (sem alterar). | O código já vem preenchido, no próximo número da sequência. Uma dica: se você tem um código seu, é só digitar por cima. |
| Em "Grupo" escolhe "Elétrica"; em "Fornecedor" abre a lista (ligada ao cadastro de fornecedores) e escolhe "Polar Distribuidora de Peças Ltda". | Em Grupo, escolho Elétrica. O Fornecedor vem da lista dos fornecedores cadastrados: a Polar Distribuidora de Peças. |
| Em "Quantidade" digita 6; "Unidade" fica em "Unidade (un)"; em "Preço de Custo (R$)" digita "38,90" e em "Preço de Venda (R$)" digita "70,00". | A quantidade inicial é seis, em unidade. O preço de custo é o que a empresa paga: trinta e oito reais e noventa centavos. O preço de venda, setenta reais, é o que aparece quando o material entra num orçamento. |
| Desce até "Locais deste material": marca a caixa do "Estoque Principal" e digita 4 no campo "Mín.". | Em Locais deste material, marco o Estoque Principal e coloco o mínimo em quatro. É esse mínimo que dispara o alerta de estoque baixo, e ele vale para cada local. Sem mínimo, o material não avisa quando está acabando. |
| A câmera passa por "Foto do item", "Código de barras" e "Vendável na loja" (sem preencher; sem foto, o bucket `inventory-photos` não existe no falso). | Tem ainda a foto, o código de barras e a chave Vendável na loja, que coloca o material no caixa do PDV. São opcionais, e hoje ficam como estão. |
| Clique em "Salvar": toast "Item cadastrado com sucesso!"; a linha "Capacitor 40 µF" entra na lista com 6 un e mínimo 4. | Salvo, e o capacitor entra na lista com seis unidades. A quantidade inicial já fica registrada no histórico, como cadastro inicial. |

### cap03 · Entrada, saída e estoque baixo (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Menu da linha "Fita isolante" → "Registrar entrada": a janela mostra o material, o código, o local ("Estoque Principal", "Principal") e "Saldo atual: 28". Digita 10 em "Quantidade" e "Compra no balcão" em "Observação"; a câmera para em "Saldo após: 38"; clique em "Confirmar": toast "Entrada registrada". [BACKEND: `register_inventory_movement` calcula saldo antes e depois e espelha em `inventory.quantity`; unidade da Fita no seed dentro da lista do app] | Quando chega material, registro a entrada. No menu da linha da Fita isolante, clico em Registrar entrada, digito dez e escrevo, em Observação, Compra no balcão. Repara no Saldo após, que mostra quanto vai ficar: trinta e oito. Confirmo. |
| Menu da linha "Capacitor 40 µF" → "Registrar saída": digita 3 em "Quantidade"; a câmera para em "Saldo após: 3"; clique em "Confirmar": toast "Saída registrada". | A saída é igual. No capacitor, clico em Registrar saída e tiro três. Olho o Saldo após antes de confirmar, porque a Dominex não aceita uma saída maior do que o saldo. |
| A linha do "Capacitor 40 µF" fica avermelhada, com o triângulo (dica "Estoque abaixo do mínimo: 3 de 4"); zoom no cartão "Estoque baixo", que sobe de 2 para 3. [BACKEND: view `inventory_low_stock`] | O capacitor ficou com três, abaixo do mínimo de quatro. A linha fica vermelha, e o cartão Estoque baixo passa de dois para três. |
| Clique em "Filtros" e liga "Estoque abaixo do mínimo": a lista mostra "Gás refrigerante R-410A", "Tubo de cobre 3/8"" e "Capacitor 40 µF"; desliga a caixa e fecha. | Em Filtros, marco Estoque abaixo do mínimo e vejo só os três que precisam de reposição. Esse alerta olha o mínimo de cada local, e daqui a pouco isso vai fazer sentido. |
| A câmera abre o menu da linha de um material e passa por "Editar", "Registrar entrada", "Registrar saída" e "Excluir" (sem clicar; fecha o menu com Esc). | Uma dica: no mesmo menu existe o Excluir. Para encerrar um material, zere o saldo e tire dos locais, porque ao excluir o histórico dele também é apagado. |

### cap04 · Locais e grupos de material (vinheta: LOCAIS)

| Tela | Fala |
| --- | --- |
| Clique em "Configurações" (cabeçalho): abre a janela "Configurações do Estoque", na aba "Grupos de material": a lista com Gases, Cobre e tubos, Elétrica e Consumíveis, cada um com a bolinha de cor (sem editar nada). | Quando a empresa tem uma van, ou mais de um depósito, entram os locais. Tudo começa em Configurações, que tem duas abas. Em Grupos de material ficam as famílias do estoque, cada uma com a sua cor: Gases, Cobre e tubos, Elétrica e Consumíveis. |
| Clique na aba "Locais de estoque": a linha "Estoque Principal" com o selo "Principal". No campo "Novo local de estoque" digita "Van 01" e clica no botão "+": toast "Depósito criado com sucesso!"; "Van 01" entra na lista. | Em Locais de estoque, já existe o Estoque Principal, o local padrão da empresa. Vou criar o da van do técnico: digito Van 01 e clico no botão de mais. |
| Fecha a janela: a tela ganha as abas de local ("Estoque Principal", com a estrela, e "Van 01"), sob o subtítulo "Operacional" (a câmera ignora o subtítulo). | Fechando a janela, cada local ganha a sua aba, e o principal leva uma estrela. |
| Clique na engrenagem da aba "Van 01": abre "Configurar Van 01", na aba "Itens". Em "Adicionar por grupo" escolhe "Gases" e clica em "Adicionar grupo" (os gases são marcados na hora); na lista marca "Fita isolante"; clique em "Salvar": toast "Itens do local atualizados". [BACKEND: `add_group_to_stock` (grava na hora) e `set_stock_materials`] | Agora digo o que existe na van. Na engrenagem da aba, em Adicionar por grupo, escolho Gases, e os gases já entram. Marco também a Fita isolante e salvo. |
| (sem ação; a câmera fica na lista de itens marcados) | Uma dica: para tirar um material de um local, transfira o saldo antes, porque com saldo a Dominex não deixa remover e oferece o botão Transferir saldo. |

### cap05 · Transferir para a van (vinheta: LOCAIS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Estoque Principal"; menu da linha "Gás refrigerante R-410A" → "Transferir": abre "Transferir entre locais de estoque". [BACKEND: `transfer_stock_between` com as duas pernas (saída e entrada) no Kardex] | Com a van criada, vamos carregá-la. No Estoque Principal, no menu do Gás refrigerante R-410A, clico em Transferir. |
| "Local de origem" já vem "Estoque Principal" ("Disponível: 8,5"); em "Local de destino" escolhe "Van 01"; "Quantidade" 2; "Observações" "Carga da van do Rafael". | A origem já vem preenchida, com oito vírgula cinco disponíveis. Escolho a Van 01 como destino, digito dois quilos e anoto: Carga da van do Rafael. |
| Clique em "Transferir": toast "Transferência realizada com sucesso!". Clique na aba "Van 01": o R-410A aparece com 2 kg; volta à aba "Estoque Principal": 6,5. | Clico em Transferir. Na aba da Van 01, o R-410A aparece com dois quilos, e no Estoque Principal sobram seis vírgula cinco. A transferência tira de um local e põe no outro, e o histórico guarda os dois lados. |

### cap06 · Quem enxerga cada local (vinheta: LOCAIS)

| Tela | Fala |
| --- | --- |
| Clique na engrenagem da aba "Van 01" e na aba "Acesso" de "Configurar Van 01": a chave "Restringir acesso a este local" desligada, com o texto "Todos os usuários da empresa veem este local.". [BACKEND: `get_stock_access` e `set_stock_access`; o Rafael Lima vem do T2] | Dá para escolher quem enxerga cada local. Na engrenagem da van, abro a aba Acesso. Por padrão, todos os usuários da empresa veem o local. |
| Liga a chave: o texto muda para "Apenas os usuários marcados veem e movimentam este local." e aparece a lista de usuários; zoom em "Camila Duarte" com "Sempre tem acesso". | Ligo Restringir acesso a este local, e aparece a lista de pessoas. A Camila, que é administradora, mostra Sempre tem acesso: quem administra enxerga todos os locais. |
| Liga a chave de "Rafael Lima"; clique em "Salvar acesso": toast "Acesso do local atualizado". | Marco o Rafael Lima, que é quem usa a van, e clico em Salvar acesso. Agora só ele e a gestão veem e movimentam a Van 01. |
| (sem ação; a câmera fica na lista de usuários) | Uma dica: marque sempre alguém, porque sem ninguém marcado o local continua aberto a todos. |

### cap07 · Todo movimento no Kardex (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Clique na aba "Histórico de Materiais (Kardex)": duas colunas; à esquerda "Materiais", com o item "Geral (Todos)", a busca "Buscar material..." e "Filtros"; à direita o título "Kardex geral". [BACKEND: movimentos semeados dentro do mês da data congelada (o Kardex abre em "este mês"), coerentes (saldo antes + alteração = saldo depois)] | E tudo isso fica registrado no Kardex, o histórico dos movimentos do estoque. A coluna da esquerda lista os materiais, e a da direita traz o Kardex geral, com os movimentos de todos eles. |
| Zoom nas colunas "Data e Hora", "Tipo", "Material e origem", "Local", "Estoque inicial", "Alteração" e "Estoque final"; a câmera percorre as linhas de hoje: Entrada da "Fita isolante" ("Compra no balcão"), Saída do "Capacitor 40 µF", Entrada "Cadastro inicial" do capacitor e a Transferência, com o local "Estoque Principal → Van 01". | Cada linha diz quando foi, o tipo do movimento, o material e quem lançou, o local, o estoque antes, a alteração e o estoque depois. Aqui estão a entrada da fita, o capacitor que cadastramos e a saída dele. E a transferência mostra os dois locais na mesma linha. |
| A câmera para nas duas linhas do tipo "Consumo", com a origem "OS #16". | Estas duas linhas de Consumo vêm da OS número dezesseis, que o técnico finalizou no tutorial dele. A baixa aconteceu porque a empresa ligou a opção Consumo de estoque na OS e o técnico anotou o que usou. Sem essa opção e sem os materiais anotados, concluir a ordem não mexe no estoque. |
| Clique em "Filtros": "Período" (este mês), "Tipo de movimento" e "Local"; escolhe "Consumo" em "Tipo de movimento": a lista fica só com as duas linhas; limpa o filtro. | Nos Filtros, escolho o período, que começa no mês atual, o tipo de movimento e o local. Filtrando por Consumo, ficam só essas duas linhas. |
| Clique em "Gás refrigerante R-410A" na coluna "Materiais": o título vira "Histórico deste material" e a lista mostra só os movimentos do R-410A. | E se eu clico num material, como o Gás refrigerante R-410A, vejo só o histórico dele. Todo movimento deixa rastro: quem fez, quando e de onde. |

### cap08 · Requisição de compra (vinheta: COMPRAS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Compras de Material": título "Requisições de Compra" e a faixa vermelha "3 materiais abaixo do mínimo", com a ação "Criar requisição". [BACKEND: view `inventory_low_stock` (a faixa e a janela "Itens abaixo do mínimo"); numeração de `compras` por gatilho emulado] | Agora, o que fazer quando o material está acabando: as compras. Na aba Compras de Material, uma faixa vermelha já avisa que três materiais estão abaixo do mínimo. |
| A câmera passa pelos botões da barra: "Fornecedores", "Nova requisição de compra" e "Registrar compra direta" (sem clicar). | Aqui em cima, o Fornecedores abre o cadastro dos fornecedores. O Registrar compra direta lança a entrada no estoque e a despesa de uma vez. Ele só aparece para quem administra estoque e financeiro, e fica para o tutorial Financeiro. |
| Clique em "Criar requisição": abre "Nova Requisição de Compra". Em "Título *" digita "Reposição de gás, cobre e capacitor"; a câmera mostra "Local de destino" (Estoque Principal) com o texto "Os materiais recebidos entram neste local de estoque.". | Vou fazer uma requisição, que é a lista do que precisa ser comprado. Clico em Criar requisição e dou o título: Reposição de gás, cobre e capacitor. O destino é o Estoque Principal, porque é pra lá que o material vai quando chegar. |
| Clique em "Adicionar itens abaixo do mínimo": abre "Itens abaixo do mínimo"; em "Selecionar local de estoque" escolhe "Estoque Principal"; as três linhas mostram "Deficit: N un"; clique em "Adicionar à requisição" (adiciona todos os listados). | Em vez de procurar um por um, uso o Adicionar itens abaixo do mínimo. Escolho o local, e a lista mostra o déficit de cada material, ou seja, quanto falta para chegar ao mínimo. Adiciono todos à requisição. |
| As três linhas entram com a quantidade em branco; o robô digita "10" no R-410A, "20" no "Tubo de cobre 3/8"" e "6" no "Capacitor 40 µF" (trecho acelerado). | As quantidades entram em branco, porque quem decide quanto comprar é você. Peço dez quilos de R-410A, vinte metros de tubo de cobre de três oitavos e seis capacitores. |
| Clique em "Salvar": toast "Requisição criada!"; a requisição aparece como cartão (#N, "Reposição de gás, cobre e capacitor"). | Salvo, e a requisição está criada. |

### cap09 · Cotações e fornecedor por material (vinheta: COMPRAS)

| Tela | Fala |
| --- | --- |
| Clique no cartão da requisição: abre a tela da requisição (botão "Voltar para requisições") com os blocos "Materiais", "Cotações" e "Ordens de compra". | Com a requisição criada, o próximo passo é pedir preço aos fornecedores. Clico nela e abre a tela da requisição, com três blocos: Materiais, Cotações e Ordens de compra. |
| Em "Cotações" clica em "Nova cotação": em "Fornecedor *" escolhe "Ventura Gás e Tubos"; na tabela (Material, Qtd., Valor unitário (R$), Valor total (R$)) digita os unitários: R-410A "94,00", Tubo de cobre 3/8" "29,50" e Capacitor 40 µF "39,00"; a câmera para em "Total geral" (R$ 1.764,00). [BACKEND: `compra_cotacoes` e `compra_cotacao_precos` pela gravação genérica; o total vem da soma das linhas] | Em Cotações, clico em Nova cotação e escolho o fornecedor, a Ventura Gás e Tubos. Digito o valor de cada material: noventa e quatro reais o quilo do gás, vinte e nove reais e cinquenta centavos o metro do tubo e trinta e nove reais o capacitor. A Dominex soma o total. |
| Clique em "Salvar cotação": toast "Cotação criada!". Repete para "Cobre Sul Suprimentos Ltda" (98,00, 27,00 e 38,00) e "Polar Distribuidora de Peças Ltda" (99,00, 31,00 e 36,00) em trecho acelerado. | Salvo, e faço o mesmo com a Cobre Sul e com a Polar, cada uma com os seus preços. |
| Os três cartões de cotação: fornecedor, selo "Pendente", "3/3 materiais com preço", o valor total e o selo "Mais barata" no da Cobre Sul. (Não clicar em "Aceitar".) | Cada cartão mostra quantos materiais têm preço e o total. O selo Mais barata marca o menor total, mas o melhor preço de cada material pode estar em outro fornecedor. |
| Em "Materiais", abre o campo "Fornecedor escolhido" de cada linha (as opções vêm no formato "Fornecedor (R$ preço)", em ordem de preço) e escolhe: R-410A com a Ventura, Tubo de cobre 3/8" com a Cobre Sul e Capacitor 40 µF com a Polar. | Por isso a escolha é por material. Em Materiais, o campo Fornecedor escolhido lista as opções em ordem de preço. O gás fica com a Ventura, o tubo com a Cobre Sul e o capacitor com a Polar. |
| (sem ação; a câmera fica nos três materiais com o fornecedor escolhido) | Uma dica: até aqui o estoque não mudou. Ele só sobe quando o material chega e você registra o recebimento. |

### cap10 · Ordem de compra e recebimento (vinheta: COMPRAS)

| Tela | Fala |
| --- | --- |
| Em "Ordens de compra" clica em "Gerar ordens de compra": toast "3 ordens de compra geradas."; surgem três cartões, um por fornecedor (Ventura, Cobre Sul e Polar), todos com o selo "Rascunho". [BACKEND: numeração de `compra_ordens` por gatilho (com autor e data de envio)] | Com o fornecedor escolhido em cada material, é hora de gerar as ordens de compra. Clico em Gerar ordens de compra, e a Dominex cria uma por fornecedor, todas em Rascunho. |
| Na ordem da Ventura: menu → "Marcar como enviada": toast "Ordem marcada como enviada." e selo "Enviada". Abre o menu de novo: aparecem "Baixar PDF" (a câmera passa, sem clicar) e "Registrar recebimento". | Na ordem da Ventura, clico em Marcar como enviada, e o selo muda para Enviada. No menu também aparece o Baixar PDF, que gera o documento da ordem para você mandar ao fornecedor. |
| Clique em "Registrar recebimento": a janela mostra "Informe só o que chegou agora. Você pode receber em partes, o saldo continua pendente." e, por item, "Qtd. pedida", "Qtd. recebida" e "Qtd. pendente"; clique em "Receber tudo" e em "Confirmar recebimento": toast "Recebimento registrado. 1 item atualizado."; selo "Recebida". [BACKEND: `receber_ordem_compra`: entrada no local da requisição, soma o recebido e define o status, sem criar despesa] | Chegou o gás. Em Registrar recebimento, vejo o que foi pedido, o que já chegou e o que está pendente. Como veio tudo, clico em Receber tudo e confirmo. |
| Na ordem da Cobre Sul: "Marcar como enviada" e "Registrar recebimento"; digita 10 em "Quantidade" do tubo (pedidos 20); "Confirmar recebimento": selo "Recebida parcial" e "Qtd. pendente" 10. | O tubo da Cobre Sul chegou pela metade: dez metros dos vinte. Informo só o que chegou agora. O resto continua pendente, e a ordem fica como Recebida parcial. |
| A câmera mostra os três cartões: Ventura "Recebida", Cobre Sul "Recebida parcial" e Polar "Rascunho". | A ordem da Polar continua em rascunho, esperando o envio. |
| Volta à aba "Estoque Atual" (aba "Estoque Principal"): "Gás refrigerante R-410A" com 16,5 e "Tubo de cobre 3/8"" com 22; o cartão "Estoque baixo" cai de 3 para 1 (só o capacitor). | De volta ao Estoque Atual, o gás subiu para dezesseis vírgula cinco, e o tubo para vinte e dois. O cartão de estoque baixo caiu para um: só o capacitor, que ainda não chegou. |

### cap11 · A nota fiscal em XML (vinheta: NOTA FISCAL)

| Tela | Fala |
| --- | --- |
| Clique em "Importar XML (NF-e)" (cabeçalho): a janela com o texto "Selecione o arquivo .xml da nota fiscal eletrônica para dar entrada no estoque."; passo `upload` no botão "Escolher arquivo XML" com o XML fictício da Gelo Norte. [BACKEND: XML fictício com o CNPJ da Gelo Norte igual ao do cadastro, três produtos (o nome do primeiro contém "Capacitor 40 µF") e chave de 44 dígitos fora de `nfe_imports`; passo `upload` do robô (`rec/recorder/runner.mjs`); TESTAR o leitor e o casamento do nome antes de gravar] | E quando o fornecedor manda a nota fiscal em XML? Clico em Importar XML da NF-e e escolho o arquivo da nota. A Dominex lê tudo na hora. |
| Revisão: o cartão "Fornecedor" com "Gelo Norte Componentes Ltda", o CNPJ e o selo "Vinculado". | Primeiro aparece o fornecedor, a Gelo Norte Componentes, com o selo Vinculado, porque o CNPJ da nota já está no cadastro. Se fosse um fornecedor novo, a Dominex cadastraria junto. |
| "Produtos da nota" ("2 novos • 3 no total"): a câmera percorre os três cartões, com nome, "Qtd", "Unidade", "Custo un." e "Destino no estoque": "Capacitor 40 µF 440V" já vem em "Capacitor 40 µF (EST-010)"; "Contator 25 A" e "Filtro secador" vêm em "Criar novo item". | Em Produtos da nota, cada item traz o nome, a quantidade, a unidade e o custo. O Destino no estoque diz onde cada um entra. O capacitor a Dominex reconheceu pelo nome e ligou ao que a gente cadastrou. O contator de 25 A e o filtro secador são novos e vão ser criados. |
| Zoom no rodapé ("3 itens • R$ 731,00"); clique em "Confirmar entrada": aviso "NF-e importada" ("3 itens importados • 2 novos. Entrada registrada no estoque."). | Confirmo a entrada. Três itens importados, dois deles novos. |
| (sem ação; a câmera fica na lista de estoque com os itens novos) | A nota dá entrada no estoque principal e cadastra o fornecedor se ele for novo. Para levar algum item pra van, é só transferir depois. E se a mesma nota for importada de novo, a Dominex avisa antes de repetir a entrada. |

### cap12 · Contar e ajustar (vinheta: INVENTÁRIO)

| Tela | Fala |
| --- | --- |
| Clique na aba "Inventários" e em "Novo inventário": o assistente na etapa "Locais" ("Selecione os locais de estoque que serão contados."); marca "Estoque Principal" ("Principal") e clica em "Avançar". [BACKEND: numeração de `inventory_counts`, coluna `diff` de `inventory_count_items`, view `inventory_count_divergences` e `finalize_inventory_count`] | Agora, a conferência: o inventário, que é a contagem física do estoque. Na aba Inventários, clico em Novo inventário. A primeira etapa é Locais, e eu marco o Estoque Principal. |
| Etapa "Escopo" ("Escolha quais materiais entram na contagem."): escolhe "Por grupo de material", marca "Gases" e "Elétrica" e clica em "Avançar". | Em Escopo, posso contar tudo, só alguns grupos ou itens específicos. Hoje vou por grupo: Gases e Elétrica. |
| Etapa "Confirmar": o quadro "Resumo do inventário"; digita "Contagem do mês" em "Observações"; clique em "Criar inventário": toast "Inventário criado"; abre a janela "Inventário #N". | Na última etapa, vejo o resumo e escrevo uma observação: Contagem do mês. Clico em Criar inventário. |
| Na janela "Inventário #N": colunas "Material", "Local", "Esperado", "Contado" e "Diferença"; zoom em "Esperado" e nos campos "Contado" vazios ("Não contado"). [BACKEND: semear saldo, mesmo zerado, para todo par material × local que deve entrar na contagem; TESTAR a rolagem da lista] | A lista mostra o que era esperado de cada material, o saldo na hora em que criei o inventário, e o campo Contado fica por minha conta. |
| O robô digita o "Contado" dos quatro itens: R-410A "16", R-32 "6", Capacitor 35 µF "8" e Capacitor 40 µF "13", saindo de cada campo com Tab (trecho acelerado); as diferenças aparecem ("-0,5" e "-1", em vermelho); surge a faixa amarela "Divergências encontradas: 2 itens" com "Valor total das divergências". | Agora é só contar o que está na prateleira e digitar. A contagem salva sozinha quando eu saio do campo, e a diferença aparece na hora. Contei dezesseis quilos de R-410A, seis de R-32, oito capacitores de 35 µF e treze de 40 µF. Dois itens deram diferença. |
| Clique na aba "Divergências (2)": colunas "Material", "Local", "Esperado", "Contado", "Diferença" e "Valor divergência", com o total no rodapé. | Na aba Divergências ficam só os dois itens que não bateram, com o valor de cada diferença. |
| Clique em "Finalizar inventário": a caixa "Finalizar inventário?" ("2 itens com divergência. O estoque será ajustado em R$ …. Esta ação não pode ser desfeita.") com o campo "Observações finais"; clique em "Finalizar": toast "Inventário finalizado" ("2 itens ajustados no estoque."). | Antes de finalizar, confira essa aba: ao finalizar, o estoque é ajustado para o valor contado e não volta atrás. Clico em Finalizar, e os dois itens são ajustados. |
| Fecha a janela; a lista de inventários mostra "Inventário #N" com o selo "Finalizado". | O inventário fica Finalizado, e os ajustes entram no Kardex. Uma dica: evite movimentar o estoque enquanto conta. |

### cap13 · O saldo numa data (vinheta: POSIÇÃO)

| Tela | Fala |
| --- | --- |
| Clique na aba "Posição de Estoque": as abas de local ("Todos os locais", "Estoque Principal" e "Van 01"), a busca "Buscar material ou SKU...", o seletor de data e hora (agora), "Exportar" e "Atualizar"; os cartões "Valor em estoque (custo)" e "Projeção de venda"; a tabela com Local, SKU, Material, Un., Saldo, Valor (custo) e Projeção venda e a linha "Total". [BACKEND: `get_stock_balance_at_date` soma o Kardex até a data; movimentos em duas épocas, com a data escolhida entre elas] | Terminada a contagem, dá para voltar no tempo com a Posição de Estoque. Ela mostra o saldo de cada material em cada local, com o valor pelo custo, a projeção de venda e o total no fim. Por padrão, é a posição de agora. |
| Clique no seletor de data: abre o calendário; escolhe um dia de 30 dias atrás; a tabela e os cartões se recalculam sozinhos. [TESTAR: hora que o seletor grava ao escolher o dia (00:00 ou a atual)] | Mas posso escolher qualquer dia no calendário. Escolho o de um mês atrás, e os saldos e os valores se recalculam sozinhos: é como o estoque estava naquele dia. |
| Clique em "Buscar material ou SKU..." e digita "R-410A": a tabela fica com o gás; limpa a busca. Clique em "Exportar": o menu com "PDF" e "Excel" (a câmera passa, sem escolher). | A busca ajuda a seguir um material só, e o Exportar leva a posição para PDF ou Excel. Uma dica: o valor usa o custo cadastrado hoje, e não o custo daquele dia. |

### cap14 · Compras, média paga e preço (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Clique na aba "Relatório": o título "Relatório de estoque por material" e o período "Todo o histórico"; os cartões "Total comprado" (já aberto, com "Ticket médio por compra" e "Materiais comprados"), "Total vendido" e "Lucro bruto" (selo "PDV" e um traço no lugar do valor) e "Projeção de lucro" (selo "estimativa"). [BACKEND: `get_material_purchase_report`; compras recebidas em duas datas; TESTAR a largura (a tabela tem 1320 px de mínimo: rolar na horizontal ou recolher o menu lateral) e abrir com o navegador limpo] | E para saber quanto a empresa paga pelos materiais, o Relatório. O Total comprado soma as compras do período, e abrindo o cartão dá para ver o ticket médio de cada compra. |
| A câmera passa por "Total vendido" e "Lucro bruto" (selo "PDV", "Será calculado a partir das vendas do PDV.") e abre "Projeção de lucro" (faixa amarela "Projeção, não lucro realizado"). | Total vendido e Lucro bruto dependem das vendas do PDV. A Projeção de lucro é uma estimativa, feita com o preço de venda cadastrado. |
| Desce ao painel "Evolução do preço de compra": a lista "Materiais" (subtítulo "Selecione para analisar") com o item "Visão geral" (subtítulo "Maiores altas e quedas") e, à direita, "Variações recentes de preço". | Aqui embaixo, a Evolução do preço de compra compara cada material com a compra anterior dele, e mostra as maiores altas e quedas. |
| Escolhe "Gás refrigerante R-410A": os cartões "Último preço", "Média do período", "Menor preço", "Maior preço" e "Variação" e as abas "Preço médio" e "Volume comprado". | No R-410A, o último preço foi noventa e quatro reais o quilo, o menor foi oitenta e seis reais, e o maior, noventa e quatro. A média é ponderada pela quantidade comprada, e a variação compara o último preço com o da compra anterior. |
| Desce à lista "Por material": colunas "Última compra", "Compras", "Qtd. comprada", "Valor comprado", "Média paga" e "Saldo atual"; clique na linha do R-410A: abre o "Histórico de compras" (data, fornecedor, local e ordem de compra, quantidade e preço). | Na lista por material, a coluna Média paga mostra o que a empresa pagou em média. Clicando na linha do R-410A, vejo cada compra: data, fornecedor, ordem de compra, quantidade e preço. |
| (sem ação; a câmera fica no histórico de compras) | Uma dica: a média paga considera as compras recebidas por ordem de compra e as compras diretas. As entradas rápidas e as notas importadas não entram. |

### cap15 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cadastro do "Capacitor 40 µF", a entrada de "Fita isolante" e o cartão "Estoque baixo". | Pronto! Recapitulando: você cadastrou um material, com grupo, custo, preço de venda e mínimo por local, e registrou entradas e saídas, com o alerta de estoque baixo. |
| Montagem rápida: as abas de local, a transferência para a "Van 01", a aba "Acesso" e o "Kardex geral". | Criou a Van 01, transferiu material para ela, escolheu quem enxerga o local e acompanhou tudo no Kardex. |
| Montagem rápida: a requisição, as três cotações, as ordens de compra e a janela "Importar XML (NF-e)". | Para repor, fez a requisição, pediu cotações, escolheu o fornecedor de cada material e recebeu pelas ordens de compra. A nota fiscal em XML também deu entrada. A compra direta fica para o tutorial Financeiro. |
| Montagem rápida: o "Inventário #N" finalizado, a "Posição de Estoque" e o "Relatório". | Fechou com o inventário, a posição numa data e o relatório de compras e de preço. |
| Cartão "Próximo: Orçamentos, Precificação e Proposta"; cartela final. | Com o estoque em ordem, o próximo passo é montar orçamentos e propostas para os seus clientes. Até lá! |
