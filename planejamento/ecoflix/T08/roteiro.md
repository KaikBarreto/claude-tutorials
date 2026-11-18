# Roteiro T8 · Ticket de Pesagem

Pronto para o ensaio e a voz (sem etapa de aprovação). Coluna Fala = narração (voz Kaik Barreto), na grafia da legenda;
a grafia de pronúncia vai em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera fica, com os rótulos
como no código (`T08/inventario.md`; app **1.60.10**, conferidos na tela nas explorações de 18/11).

**18/11 · aplicação do 1.60.10** (`cobertura_160.md` + `JUNCAO_160.md`): capítulos novos **07** (ticket com valores), **11** (pesagem
avulsa com cobrança) e **12** (sem internet); os antigos 07, 08, 09 e 10 viraram **08, 09, 10 e 13**. Trechos novos nos caps 01, 02,
06, 08, 09 e 10. As propostas antigas (`propostas_fala.md`) entraram.

**18/11 · ajuste de foco (pedido do Kaik):** a pesagem avulsa perde ênfase (cap11: 13 → 6 linhas, ~138 → ~55 s; saem o passo a passo
do cadastro rápido, a placa, o tipo de caminhão, a divisão entre formas, a trava e o estorno); o cap01 ganha os três casos de uso do
ticket padrão; o cap08 diz de onde vem o preço no ticket sem valores e no ticket com valores; cap01 e cap13 citam a avulsa numa frase.

- **Título:** Ticket de Pesagem
- **Antes:** Comprar e vender sucata (T7)
- **Próximo:** Pedidos e histórico do caixa (T9)
- **Vinhetas (áreas):** TICKET · TICKET · PESAGEM · PESAGEM · PESAGEM · ABAS · VALORES · VALORIZAR · COMPROVANTE · VALORIZAR ·
  AVULSA · OFFLINE · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~16 min (2.017 palavras de fala, ~12,9 min a 2,6 palavras/s, mais 13 vinhetas, a digitação nas
  janelas e as ilustrações).
- **Gravação:** computador 1280×800, logado como Rafael Nogueira; `FAKE_NOW` por capítulo (`rec/fake_now.json`: 08:40 nos caps 0 a
  3, 08:49 nos 4 e 5, 08:51 no 6, 08:55 no 7, 08:58 nos 8 a 10, 09:12 no 11, 09:20 nos 12 e 13, de 10/11/2026); EcoTray falso
  ligado como no fim do T5 ("Balança do pátio" com 0 kg), sem cena de Windows. Cada capítulo parte de um navegador novo com a
  semente do fim do anterior (`inicio`, `apos-cap02` a `apos-cap08`, `apos-cap10`, `apos-cap11`); quando o capítulo continua a
  criação, o `setup` reabre a aba por "Rascunhos abertos" fora do vídeo. Pesos digitados (decisão 1 do plano). Números na tela:
  ticket da cooperativa **#58**, do Jair **#59**, pesagem avulsa **#60** (a fala não lê números de ticket nem de pedido). O balão
  de dica do Cato é calado pelo robô (`localStorage`). Nada do que a aula cria segue para a T9 (JUNCAO_160).
- **Marcas:** `[BACKEND: ...]`, `[ILUSTRAÇÃO: ...]`, `[ZOOM: ...]` (dura a frase inteira), `[GRAVAÇÃO: ...]`,
  `[TESTAR: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Ticket de Pesagem". | (sem fala) |
| Dashboard, logado como Rafael Nogueira (semente `inicio`). A câmera fica no centro da tela. | Oi! Neste tutorial a gente resolve a situação clássica do pátio: o caminhão chegou, precisa pesar agora, mas o preço ainda não está fechado. |
| [ILUSTRAÇÃO: o caminhão de latinha da Cooperativa Recomeço sobe na balança; o visor marca "9.460 kg"; ao lado, uma etiqueta de preço com "R$ ?"; na palavra "depois", a etiqueta ganha um relógio.] | Na Recicla Vale Metais, a Cooperativa Recomeço mandou um caminhão de latinha, e o preço só vai ser combinado depois. |
| [ILUSTRAÇÃO, continua: o "9.460 kg" desce para um ticket; o "R$ ?" fica esperando ao lado.] | Com o Ticket de Pesagem, você registra o peso agora e resolve o valor depois. |
| Cartão discreto: "Antes: Comprar e vender sucata". | Se você ainda não viu o tutorial Comprar e vender sucata, dá uma olhada antes. [pause] Vamos ver quando usar o ticket. |

### cap01 · Quando usar o ticket (vinheta: TICKET)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), no Dashboard; no menu lateral, clique em "Materiais" e em "Ticket de Pesagem": cabeçalho "Ticket de Pesagem" ("Gerencie tickets de pesagem rodoviária"). | O ticket fica no menu Materiais, em Ticket de Pesagem. |
| [ILUSTRAÇÃO: Dois caminhos: em cima, "Compra direta": pesa, põe o preço, paga, e o estoque e o caixa mexem na hora; embaixo, "Ticket": pesa agora, o ticket fica salvo, depois "Valorizar" vira compra ou venda e só no "Finalizar" o estoque e o caixa mexem. Na palavra "fechado" acende o de cima; na palavra "depois", o de baixo.] | Com o preço fechado, você faz a compra direto, como no tutorial anterior. Com o preço em aberto, você pesa no ticket e transforma em compra ou venda depois. |
| [ILUSTRAÇÃO, continua: o ticket com o peso; o estoque e o caixa ficam cinza até o "Finalizar".] | Ticket salvo é peso registrado, e só. Nenhum quilo entra no estoque e nenhum centavo entra ou sai do caixa por causa dele. Isso só acontece quando o pedido que nasce dele é finalizado. |
| De volta à tela (a lista do Ticket de Pesagem, parada); o cursor vai ao cartão "Ticket #57", que espera o preço em "Aguardando valorização". | Na prática, o ticket resolve três situações. O preço que só fecha depois: no fim do dia, ou depois de classificar o material. |
| O cursor vai ao botão "Novo Ticket de Pesagem", sem clicar. | Vários caminhões no pátio ao mesmo tempo: cada um fica com o seu ticket aberto, e ninguém espera o outro terminar. |
| O cursor descansa; a lista continua parada. | E a venda: o caminhão que vem buscar material é pesado do mesmo jeito, num ticket de venda. |
| Zoom nas colunas "Aguardando valorização" (cabeçalho âmbar, com os cartões do #57 e do #56) e "Valorizados" (verde). | Os tickets ficam aqui. Em Aguardando valorização, o que ainda espera o preço. Em Valorizados, o que já virou pedido. |
| Clique na aba "Pesagens avulsas": título "Pesagens Avulsas", "Nenhuma pesagem avulsa registrada"; o cursor passa em "Nova Pesagem Avulsa", sem clicar; depois clique em "Tickets padrão". | Já a aba Pesagens avulsas é pra quem só quer usar a balança, sem comprar nem vender. A gente faz uma mais adiante. |

### cap02 · Criar o ticket (vinheta: TICKET)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em "Ticket de Pesagem". Clique em "Novo Ticket de Pesagem": cabeçalho "Novo Ticket de Pesagem" ("Preencha o ticket. Use as abas para atender vários veículos."). | O caminhão da cooperativa chegou. Clico em Novo Ticket de Pesagem. |
| Zoom na barra de cima: "Modalidade" em "Ticket padrão", "Tipo" em "Compra" e "Valores" em "Sem valores". | Em cima ficam três chaves: ticket padrão; compra, porque a gente vai comprar a latinha; e sem valores, porque o preço ainda não fechou. |
| Zoom em "Com valores", sem clicar. | Quando o preço já está combinado, dá pra fazer o ticket com valores, e ele já guarda o preço de cada material. A gente faz um assim mais adiante. |
| Clique em "Selecionar fornecedor": janela "Selecionar Fornecedor" ("Buscar por nome, apelido, CPF/CNPJ ou telefone...", com o "+" de "Cadastrar novo" ao lado). O cursor passa em "Não informado" (primeira opção) e no pino ao lado de "Cooperativa Recomeço" (dica "Fixar como padrão"), sem clicar. | Agora o fornecedor. Se ele não quiser se identificar, existe a opção Não informado. E o pino, ao lado do nome, deixa um fornecedor fixo para os próximos tickets. |
| Clique em "Cooperativa Recomeço" (a janela já lista os cinco fornecedores, sem busca). [BACKEND: `suppliers` com a Cooperativa Recomeço] | Aqui, o fornecedor é a Cooperativa Recomeço. |
| No card "Pesagem", em "Material" ("Escreva o nome ou código do material"), digita "latinha" e escolhe "Alumínio latinha". [BACKEND: com a balança ligada, "Quantidade (Kg)" pode receber "0,000" da Balança do pátio ao escolher o material; não atrapalha] | No card Pesagem, o material: alumínio latinha. |
| Em "Motorista" ("Digite ou busque o motorista") digita "Edson" e escolhe "Edson Moura"; em "Placa do Veículo" ("Digite ou busque a placa") escolhe "FKD2E41". [BACKEND: `drivers` e `vehicles` do mundo] | E, aqui dentro, o motorista e a placa. O Edson Moura e o caminhão dele já estão cadastrados, então é só escolher na lista. |
| O cursor passa no "+" ao lado de "Motorista" ("Gerenciar motoristas": abre a janela "Motoristas", com "Novo motorista") e no "+" de "Placa do Veículo" ("Gerenciar placas"), sem clicar. | Motorista novo? O botão de mais, ao lado do campo, abre o cadastro de motoristas sem sair do ticket. O mesmo vale para a placa. |
| Zoom na barra escura de abas, à direita: "Número" "#58", "Peso" "0 kg", "CLIENTE/FORNECEDOR" "Cooperativa Recomeço" e, embaixo, "Seu rascunho". | Do lado direito fica a aba deste ticket, com o número, o peso e o fornecedor. |

### cap03 · A primeira pesagem e o rascunho (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`: rascunho com a cooperativa, o Edson e a placa; o `setup` reabre a aba e escolhe "Alumínio latinha" fora do vídeo). Clique em "Pesagem avançada", embaixo de "Quantidade (Kg)": janela "Pesagem avançada" ("Registre pesagem dupla, tara, impureza e dados do transporte"). | O Edson sobe na balança com o caminhão cheio. A primeira pesagem vai na Pesagem avançada. |
| Em "1ª Pesagem" digita 9460: o "Peso Bruto (Kg)" mostra "9.460" e "= 1ª pesagem"; "Líquido (Kg)" "9.460". [ZOOM: "1ª Pesagem" e o "Peso Bruto (Kg)", com "= 1ª pesagem"] | Na primeira pesagem, nove mil quatrocentos e sessenta quilos. Por enquanto, ela conta como bruto. |
| Zoom no botão da balança dentro do campo "1ª Pesagem", sem clicar. | Com a balança ligada no EcoTray, o botão dentro do campo puxa esse peso sozinho. |
| Zoom na dica "Preencha 1ª e 2ª pesagem para o bruto, informe só a 1ª (conta como bruto) ou digite o bruto direto." | E a dica embaixo mostra os três jeitos: as duas pesagens, só a primeira, ou o bruto digitado direto. |
| Em "Como exibir no comprovante", marca "Completo" ("1ª e 2ª pesagem, bruto, tara, impureza e líquido."). | Em Como exibir no comprovante, eu marco Completo, pra sair a conta inteira no papel. |
| Clique em "Confirmar": em "Itens do Ticket (1)", "Alumínio latinha" com o peso 9.460; na aba, "9.460 kg". [BACKEND: o rascunho grava em `weighing_tickets` (`status` draft) 600 ms depois] | Confirmar. Agora o caminhão vai descarregar. |
| [ILUSTRAÇÃO: O rascunho: a aba do ticket com "Seu rascunho" e um tique de "salvo" que pisca a cada mudança; ao lado, um relógio anda enquanto o caminhão descarrega.] | E não precisa fazer mais nada: o ticket fica salvo sozinho, como rascunho, a cada mudança. |
| Zoom na aba: "#58" e "Seu rascunho". | Não existe um status de esperando a segunda pesagem. O ticket fica aqui, aberto, até o caminhão voltar. E esse número é só a previsão: o ticket ganha número quando é salvo. |
| Clique em "Voltar": a lista; zoom em "Rascunhos abertos" com "1"; clique: a criação volta com a aba da cooperativa e o item. | Mesmo saindo da tela, o rascunho continua lá, em Rascunhos abertos. |
| A câmera fica no item reaberto. | Uma dica: quando o rascunho é reaberto, confira o que já estava preenchido antes de salvar. |

### cap04 · Descarregar e a segunda pesagem (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`: o rascunho com o item de 9.460 kg; o `setup` reabre a aba). [ILUSTRAÇÃO: Entrada e saída: o caminhão cheio na balança, "1ª pesagem 9.460 kg"; ele descarrega a latinha no pátio; volta vazio, "2ª pesagem 6.380 kg"; na palavra "diferença", os "3.080 kg" da latinha se destacam entre as duas.] | O caminhão descarregou e voltou vazio pra balança. A diferença entre as duas pesagens é a latinha que ficou no pátio. |
| No item "Alumínio latinha", "Ações do item" (⋮) → "Adicionar tara / pesagem avançada": a janela abre com "Peso Bruto (Kg)" 9.460 e "1ª Pesagem" e "2ª Pesagem" vazias. | No item, em Adicionar tara, pesagem avançada. O peso da entrada está no bruto. |
| Em "1ª Pesagem" digita 9460; em "2ª Pesagem" digita 6380: o "Peso Bruto (Kg)" vira "3.080", com "|9.460 − 6.380|" embaixo; "Líquido (Kg)" "3.080". | A gente passa ele pra primeira pesagem e põe a segunda, com o caminhão vazio: seis mil trezentos e oitenta quilos. |
| [ZOOM: "Peso Bruto (Kg)" "3.080" e "|9.460 − 6.380|"] | Pronto: o bruto sai sozinho, a diferença das duas. Três mil e oitenta quilos de latinha. |
| Zoom em "Tara (Kg)", em branco. | A tara é o peso do que vem junto e não é material, como uma caçamba. Aqui o caminhão já saiu na segunda pesagem, então a tara fica em branco. |
| Clique em "Confirmar": aviso "Pesagem do item atualizada"; a linha mostra o peso 3.080. | Confirmar, e a pesagem do item está atualizada. |
| Clique na seta da linha "Alumínio latinha" ("Ver detalhes da pesagem"): abre o detalhe, com "1ª pesagem", "2ª pesagem" e "Bruto" (`components/order/WeighingDetailRow.tsx`). | Na linha, a setinha abre o detalhe, com as duas pesagens e o bruto. |

### cap05 · Impureza em porcentagem ou em quilos (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`; o `setup` reabre a aba). Em "Ações do item" → "Adicionar tara / pesagem avançada": agora a janela abre com "1ª Pesagem" 9.460, "2ª Pesagem" 6.380 e o bruto "3.080". | Falta a impureza. Na latinha sempre vem um pouco de sujeira e de água, e isso sai do peso. |
| Em "Impureza", clique em "%" e digita 2: embaixo aparece "= 61,6 Kg (sobre bruto − tara)". [ZOOM: "Impureza" com "2" e "= 61,6 Kg (sobre bruto − tara)"] | Aqui ela vai em porcentagem: dois por cento. O sistema mostra quanto isso dá: sessenta e um quilos e seiscentos. |
| Zoom no seletor "kg" e "%". | Se preferir, troca pra quilos e digita direto o peso da impureza. |
| [ILUSTRAÇÃO: A conta do líquido: "Bruto 3.080" menos "Tara 0" menos "Impureza 61,6" igual a "Líquido 3.018,4"; cada parcela entra na sua palavra.] | E o líquido fecha a conta: o bruto, menos a tara, menos a impureza. |
| [ZOOM: "Líquido (Kg)" "3.018,4"] | Três mil e dezoito quilos e quatrocentos. É esse peso que vale na compra. |
| Clique em "Confirmar": "Pesagem do item atualizada"; a linha mostra "Tara/Imp." 61,6. [BACKEND: o rascunho guarda `impurity_pct` 2 e `impurity_kg` 61,6] | Confirmar, e o ticket da cooperativa está pesado. |

### cap06 · Vários veículos ao mesmo tempo (vinheta: ABAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`; o `setup` reabre a aba). [ILUSTRAÇÃO: dois caminhões da Recicla Vale na fila da balança, o truck com a latinha da cooperativa e o 3/4 com a bateria da Auto Peças; cada um puxa uma aba própria na tela, "#58" e "#59".] | Enquanto isso, chega o Jair Lopes, com o caminhão três quartos, trazendo bateria da Auto Peças Vale Forte. |
| Na barra de abas, clique em "+ Novo ticket": abre uma aba em branco ("#59", "Sem cliente/fornecedor"; a barra mostra "(2)"). | Cada caminhão ganha a sua aba. Em Novo ticket, abre uma aba em branco. |
| Na aba nova (o preenchimento pode ser acelerado na edição): "Selecionar fornecedor" → "Auto Peças Vale Forte"; "Material" → "Bateria automotiva"; "Motorista" → "Jair Lopes"; "Placa do Veículo" → "GHT7B19"; "Pesagem avançada": "1ª Pesagem" 5640 → "Confirmar". | Fornecedor, material, motorista, placa e a primeira pesagem: cinco mil seiscentos e quarenta quilos. |
| Clique na barra escura: a lista mostra "#58" "3.080 kg" "Cooperativa Recomeço" e "#59" "5.640 kg" "Auto Peças Vale Forte". [ZOOM: a lista das duas abas] | Na barra de cima, a gente troca de um caminhão pro outro. Cada aba guarda o seu rascunho, e nada se mistura. |
| Clique em "#58": volta o ticket da cooperativa. Clique em "Salvar Ticket de Pesagem": aviso "Ticket de pesagem salvo" e a janela "Ticket #58 salvo" ("O que deseja fazer com este ticket de pesagem?"), com "Imprimir comprovante", "Valorizar" e "Fechar". [BACKEND: RPC `finalize_weighing_ticket_v4` → `ticket_number` 58, `status` pending] | O ticket da cooperativa está pronto, então eu salvo. Agora sim, ele ganha o número de verdade. |
| Clique em "Fechar": fica a aba do Jair ("#59", "Auto Peças Vale Forte", "Seu rascunho"). | O valor a gente resolve depois. E a aba do Jair continua aberta, esperando ele descarregar. |
| Clique na barra escura: na lista de abas, zoom no "x" da aba do Jair, sem clicar (ele pede "Descartar este ticket?", com "Manter ticket" e "Descartar ticket"); fecha a lista. | Se alguém fechar uma aba no x, o sistema pergunta antes de descartar o ticket. |
| Clique em "Voltar": a tela dos tickets; clique em "Rascunhos apagados" (com "1"): janela "Rascunhos apagados" ("Recupere um rascunho que foi apagado por engano. Ele volta como uma aba ativa."), com um rascunho do Valdir Pereira ("Ferro misto", "380 kg", "Apagado há cerca de 19 horas por Rafael Nogueira"), "Recuperar" e o botão de excluir definitivamente; fecha sem recuperar. [BACKEND: rascunho apagado na semente `inicio`] | E se descartar sem querer, o rascunho vai para Rascunhos apagados, na tela dos tickets. Dali dá pra recuperar. |

### cap07 · Ticket com valores (vinheta: VALORES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`; `FAKE_NOW` 08:55; o `setup` reabre a aba do Jair por "Rascunhos abertos"): "Auto Peças Vale Forte", "Bateria automotiva", "#59", "5.640 kg". O cursor passa na chave "Valores". | O Jair descarregou. E com a Auto Peças o preço da bateria já está combinado. Então este ticket pode ser feito com valores. |
| Clique em "Com valores": aparece "Tabela de Preços" ("Principal") embaixo de "Fornecedor"; os itens ganham "Valor/Kg", "Desc. (R$)" e "Total", e "Total geral: R$ 0,00"; a aba passa a mostrar "Valor". [ZOOM: "Tabela de Preços" e as colunas novas] | Mudo a chave para Com valores. Aparecem a Tabela de Preços, embaixo do fornecedor, e as colunas de valor nos itens. |
| No item, "Ações do item" → "Adicionar tara / pesagem avançada": "1ª Pesagem" 5640 (digitada de novo, como no cap04), "2ª Pesagem" 4180 ("Peso Bruto (Kg)" "1.460", "|5.640 − 4.180|"); "Valor/Kg" 3,40: "Valor estimado R$ 4.964,00", "R$/Kg efetivo: R$ 3,40". | No item, eu completo a pesagem: a segunda deu quatro mil cento e oitenta quilos. E ponho o preço combinado: três e quarenta o quilo. |
| Clique em "Confirmar": "Pesagem do item atualizada". [ZOOM: "Total geral: R$ 4.964,00"] | Confirmar. São mil quatrocentos e sessenta quilos de bateria, e o total do ticket aparece embaixo: quatro mil novecentos e sessenta e quatro reais. |
| A câmera fica no total. | Atenção: mesmo com valores, o ticket não paga ninguém. Ele só guarda o preço. O dinheiro continua saindo só quando a compra é finalizada. |
| Clique em "Salvar Ticket de Pesagem": "Ticket de pesagem salvo" e a janela "Ticket #59 salvo"; "Fechar". [BACKEND: `finalize_weighing_ticket_v4`, `pricing_mode` priced, `price_table_id` da "Principal"] | Salvo o ticket do Jair. Ele vai para Aguardando valorização, já com o valor. |
| Configurações › "Usabilidade"; a tela desce até "Permitir forma de pagamento no ticket de pesagem" ("O balanceiro escolhe a forma de pagamento já no ticket com valores; a compra/venda abre pré-preenchida."), desligada. [ZOOM: a opção] | E, se quiser, o balanceiro já deixa a forma de pagamento escolhida no ticket com valores. É só ligar esta opção em Configurações, Usabilidade. |

### cap08 · Valorizar o ticket (vinheta: VALORIZAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`; `FAKE_NOW` 08:58), em "Ticket de Pesagem": "Aguardando valorização" ("R$ 4.964,00", 4) com os cartões #59, #58, #57 e #56; o cursor vai ao cartão "Ticket #58" ("COMPRA", "Fornecedor: Cooperativa Recomeço", "Sem valores", "Alumínio latinha", "3.018,4 kg", "10/11/26 08:52"). | Pouco depois, o preço com a cooperativa fechou. É hora de valorizar: transformar o peso em pedido. |
| Marca "Selecionar" no #58; a coluna desce e marca "Selecionar" no #56 (o ticket de ontem da cooperativa, "Alumínio perfil", "412 kg"): aparece a barra "2 selecionados" com **"Valorizar 2 tickets"**; o "Selecionar" do #57 (Auto Peças) fica apagado, com a dica "Selecione tickets do mesmo cliente ou fornecedor". Não clica em valorizar. [ZOOM: a barra] [BACKEND: ticket #56 na semente `inicio`] | Uma dica: se o mesmo fornecedor tem mais de um ticket esperando, marque Selecionar em cada um e use Valorizar dois tickets. Vira uma compra só. Precisa ser o mesmo fornecedor e o mesmo tipo. |
| Fecha a barra no "x" (limpa a seleção) e a coluna volta ao alto. No cartão do #58, "Ações" → "Valorizar". [BACKEND: `order_drafts` insert com o item e o preço da tabela principal, R$ 6,20] A tela vai para a Compra (`/compra`) com o rascunho: fornecedor "Cooperativa Recomeço", "Alumínio latinha", o peso, "Tara/Imp." 61,6, "Valor/Kg" 6,20 e o total. | Hoje eu valorizo só o ticket de hoje. Em Ações, Valorizar. O sistema abre uma compra já preenchida: a cooperativa, a latinha, o peso e a impureza. |
| [ZOOM: o "Valor/Kg" 6,20 e o total da linha, R$ 18.714,08] | Como este ticket foi feito sem valores, o preço vem da tabela: seis e vinte o quilo. Dá dezoito mil setecentos e catorze reais e oito centavos. |
| A câmera fica no "Valor/Kg". | O sistema procura o preço nesta ordem: o preço especial do fornecedor, se existir; depois a tabela dele; e por último a tabela padrão. Já no ticket com valores, como o do Jair, vale o preço que está no ticket. |
| Zoom na célula "Valor/Kg". | Se o preço combinado for outro, é só mudar o valor do quilo aqui, antes de finalizar. Num ticket de venda, abre uma venda do mesmo jeito. |
| [ILUSTRAÇÃO: o caminho: ticket, "Valorizar", compra em rascunho, "Finalizar", estoque e caixa; o estoque e o caixa só acendem no "Finalizar".] | Repara: até aqui, nada entrou no estoque e nada saiu do caixa. A compra está em rascunho, e o efeito só acontece quando ela for finalizada. |

### cap09 · Imprimir o comprovante (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), em "Ticket de Pesagem"; no cartão "Ticket #58", "Ações" → "Ver comprovante": janela "Gerar comprovante do ticket" ("Escolha o formato do comprovante deste ticket de pesagem."), com "A4" ("Folha") e "Térmico" ("80mm"). | O motorista leva o comprovante do ticket. Em Ações, Ver comprovante, e o formato: Térmico, o cupom, ou A4, a folha. |
| Clique em "Térmico": abre a aba nova com o PDF do comprovante. [GRAVAÇÃO: gravar a aba nova] [ZOOM: a faixa "TICKET DE PESAGEM" / "NÃO VALORIZADO", "Documento sem valor financeiro definitivo" e o título "Ticket de pesagem N° #58"] | Repara no papel: ticket de pesagem, não valorizado. É o comprovante do peso, ainda sem valor de compra. |
| [ZOOM: "Motorista: Edson Moura" e "Placa: FKD2E41", e as linhas "1ª pesagem", "2ª pesagem", "Bruto", "Impureza" (com "(2%)") e o peso líquido] | Com o modo Completo, sai a conta inteira: o motorista, a placa, as duas pesagens, o bruto, a impureza e o líquido. |
| De volta à aba do sistema: Configurações › "Integrações"; zoom em "Imprimir comprovante do Ticket de Pesagem" ("Envia o comprovante térmico direto pra impressora ao salvar um ticket"), desligada. | E se quiser que o cupom saia sozinho na impressora ao salvar cada ticket, ligue Imprimir comprovante do Ticket de Pesagem, em Configurações, Integrações. |
| Configurações › "Usabilidade"; a tela desce até "Assinaturas no comprovante" ("Linhas para assinar no rodapé. Escolha quem assina: o operador, o cliente/fornecedor ou os dois. No ticket de pesagem, o operador aparece como Empresa."); liga a chave (aviso "Assinaturas ativadas no comprovante"): aparece "Quem assina"; abre a lista: "Operador e cliente/fornecedor", "Só o cliente/fornecedor", "Só o operador". [ZOOM: a lista] | Quer que o motorista assine o peso? Em Usabilidade, ligue Assinaturas no comprovante e escolha quem assina: os dois, só o fornecedor, ou só o operador. |
| Escolhe "Só o cliente/fornecedor"; o cursor vai à frase "No ticket de pesagem, o operador aparece como Empresa." | No ticket de pesagem, o lado do operador sai escrito Empresa. |
| O cursor passa em "Marca de ticket não valorizado" (ligada: "Mantém o aviso igual na tela, no PDF e na impressão. Tickets provisórios offline continuam identificados.") e a tela desce até "Exigir cliente/fornecedor no Ticket de Pesagem" (desligada). | Aqui também ficam duas regras do ticket: tirar do papel a marca de não valorizado, e exigir o fornecedor para salvar. |
| [GRAVAÇÃO: por baixo da ilustração, o robô devolve "Quem assina" a "Operador e cliente/fornecedor" e desliga "Assinaturas no comprovante" (regra do mundo: assinatura desligada).] [ILUSTRAÇÃO: Pesagens mescladas: duas linhas de ferro misto, "1.200 kg" e "800 kg", viram uma linha só, "2.000 kg", no comprovante; na palavra "Desmesclar", o botão "Desmesclar pesagens" separa as duas de novo.] | Uma dica: se o ticket tiver pesagens do mesmo material mescladas numa linha, o comprovante mostra só a soma. Pra conferir cada pesagem no papel, use o Desmesclar pesagens antes de imprimir. |

### cap10 · Quando o ticket sai da lista de pendentes (vinheta: VALORIZAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), em "Ticket de Pesagem": o "Ticket #58" segue em "Aguardando valorização". [ZOOM: o cartão] | E quando o ticket sai de Aguardando valorização? Mesmo com a compra em rascunho, ele continua aqui. |
| No cartão do #58, "Ações": o cursor passa em "Editar" e "Excluir", sem clicar (o menu fica aberto). | Enquanto ele espera, dá pra corrigir em Editar ou apagar em Excluir. Depois de valorizado, ele trava, e a correção passa a ser no pedido. |
| No mesmo menu, "Valorizar": aviso "Estes tickets já tinham um pedido em aberto — retomando." ("Atualizado com os itens atuais do ticket (1 item, R$ 18.714,08)."); abre a mesma compra. [BACKEND: `order_drafts` reaproveitado (update)] | Valorizando de novo, o sistema retoma a mesma compra, sem duplicar. |
| Clique em "Finalizar": "Finalizar Pedido"; escolhe "Pix/Transferência" e a conta bancária principal; clique em "CONFIRMAR PAGAMENTO": "Compra registrada!" e "Pedido finalizado — voltando ao Ticket de Pesagem" (o meio pode ser acelerado na edição). [BACKEND: caixa do Rafael aberto; finalizar da compra do T7; o ticket vira `valorized` com `valorized_order_id`] [TESTAR: se abrir "Imprimir Comprovante", fechar antes da volta] | Finalizo como no tutorial anterior: Pix, e confirmar pagamento. Agora sim, a latinha entrou no estoque e o pagamento saiu da conta. |
| A tela volta sozinha para "Ticket de Pesagem": o "Ticket #58" está em "Valorizados", com "Valorizado pelo pedido #…". [ZOOM: "Valorizado pelo pedido #…"] Depois, "Ações" do #58: o cursor passa em "Ver pedido", sem clicar; fecha o menu. | E o sistema volta sozinho pro Ticket de Pesagem. O ticket passou pra Valorizados, com o número da compra. E, em Ações, o Ver pedido abre essa compra. |
| Clique no botão "Lista" (ao lado da busca): a tabela com o selo "Valorizado" (verde) no #58 e "Aguardando valorização" (âmbar) nos outros; depois "Filtros" › "Status": "Aguardando valorização", "Valorizado" e "Cancelado". | Na lista, cada ticket mostra a situação. São três: Aguardando valorização, em amarelo; Valorizado, em verde; e Cancelado. |
| Fecha o filtro. O cursor vai ao período no alto ("Este mês", que só existe no modo Lista) e abre "Filtros": "Tipo", "Status", "Usuário". | O período, lá no alto, vale para a lista inteira. E os filtros separam por tipo, situação e usuário. |
| "Exportar" › "PDF" (a outra opção é "Excel"): janela "Exportar PDF" ("Escolha quais tickets serão incluídos no relatório") com "Período", "Tipo de Ticket" ("Compras", "Vendas"), "Status" ("Pendente", "Valorizado", "Cancelado") e "Usuário que criou". [ZOOM: a janela] | Em Exportar sai o relatório dos tickets, em PDF ou Excel, com o período, o tipo, a situação e o usuário que você escolher. |
| Fecha a janela sem gerar; a câmera fica na lista. | Um detalhe: o dono pode limitar um balanceiro a ver só os tickets que ele mesmo criou. Isso fica em Usuários e Permissões. |
| Volta ao "Kanban"; o cursor vai ao cartão "Ticket #59" ("Auto Peças Vale Forte", "R$ 4.964,00", "1.460 kg") em "Aguardando valorização". | E o ticket do Jair segue em Aguardando valorização, já com o valor, esperando a vez dele. |

### cap11 · Pesagem avulsa com cobrança (vinheta: AVULSA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`; `FAKE_NOW` 09:12), em "Ticket de Pesagem". [ILUSTRAÇÃO: um caminhão caçamba de areia, de fora, sobe na balança da Recicla Vale Metais; uma placa "Serviço de pesagem".] | Agora o outro caso: um caminhão de areia, que não é fornecedor nem cliente da Recicla Vale, só quer usar a balança. E a empresa cobra por esse serviço. |
| Aba "Pesagens avulsas" → "Nova Pesagem Avulsa" ("Preencha a pesagem avulsa. Use as abas para atender vários veículos."; "Modalidade" em "Pesagem avulsa", "Tipo" fixo em "Serviço ao cliente"). "Selecionar cliente": janela "Selecionar Cliente"; digita "Areal Boa Vista" ("Nenhum resultado encontrado."), clique em "Cadastrar «Areal Boa Vista»" e, no "Cadastro Rápido de Cliente" com o "Nome" já preenchido, "Criar Cliente": o cliente volta escolhido. Gestos calmos, sem passar pelos outros campos. [BACKEND: `customers` insert] | Em Pesagens avulsas, Nova Pesagem Avulsa. O dono do caminhão ainda não tem cadastro: eu cadastro na hora, só com o nome. |
| Em "Descrição do material" ("Ex.: Areia, terra, entulho") digita "Areia média". "Pesagem avançada": "1ª Pesagem" 23840, "2ª Pesagem" 9120 ("Peso Bruto (Kg)" "14.720", "|23.840 − 9.120|"); "Confirmar": "Areia média", "14.720". [ZOOM: o "Peso Bruto (Kg)"] | Escrevo o que é, areia média, e peso na entrada e na saída, como no ticket: catorze mil setecentos e vinte quilos. |
| A tela desce. **"Valor cobrado pela pesagem"**: "60,00". [ZOOM: o campo] (A placa e o "Tipo de caminhão" ficam em branco.) | Depois, o valor cobrado pela pesagem: sessenta reais. |
| "Salvar Pesagem Avulsa": abre "Finalizar Pedido" ("Total: R$ 60,00", "Cliente: Areal Boa Vista"); clique em "Pix/Transferência" (a "Conta Principal" já vem escolhida); o cursor passa em "Dinheiro" e em "Saldo do Cliente", sem clicar. | Ao salvar, escolho como ele pagou. Foi no Pix, mas também dá em dinheiro ou no saldo do cliente. |
| "CONFIRMAR PAGAMENTO": a janela "Ticket #60 salvo" com o selo "PESAGEM AVULSA" ("Somente comprovante de peso. Esta pesagem não possui valor comercial e não pode ser valorizada."), só "Imprimir comprovante" e "Fechar". [ZOOM: a janela] [BACKEND: `finalize_weighing_ticket_v4` + `apply_standalone_weighing_charge_v1`: receita de R$ 60,00 na Conta Principal, categoria "Serviço de pesagem", descrição "Serviço de pesagem avulsa #60"] Na frase do comprovante: "Imprimir comprovante" → "Térmico". [ILUSTRAÇÃO com o PDF do app (`rec/t08/arquivos/cap11-comprovante-avulsa.pdf`, refeito no ensaio: agora sem placa, sem tipo de caminhão e sem as duas pesagens abertas): faixa "PESAGEM AVULSA" / "SEM VALOR COMERCIAL", o peso e o "Valor da pesagem: R$ 60,00".] No fim, "Voltar": a lista "Pesagens Avulsas" com "#60", "Areal Boa Vista", "14.720 kg", "Sem valor comercial". | Pronto. O valor já entrou na conta, sem pedido e sem mexer no estoque. O comprovante sai marcado como pesagem avulsa. |

### cap12 · Sem internet (vinheta: OFFLINE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap11`; `FAKE_NOW` 09:20; variante lateral: nada do que acontece aqui segue). O `setup` abre "Novo Ticket de Pesagem", escolhe Cooperativa Recomeço, Alumínio latinha, Edson Moura e FKD2E41 e derruba a internet de verdade (passo `rede` do robô: o backend fica inalcançável; o relógio da tela começa em 09:22). [ILUSTRAÇÃO: o caminhão na balança, o sinal de internet cortado; na tela, a faixa "Sem internet."] | E se a internet cair com o caminhão em cima da balança? O ticket continua funcionando. |
| A criação do ticket com a faixa vermelha no alto ("Sem conexão — operações serão salvas localmente até reconectar na internet") e o aviso âmbar "Sem internet. Você pode pesar e finalizar normalmente: o ticket fica guardado neste aparelho e sobe sozinho quando a conexão voltar. O comprovante do motorista sai como provisório — o número oficial é atribuído na sincronização." [ZOOM: o aviso] No fim da linha, "Pesagem avançada" e 7210 na "1ª Pesagem". | O sistema avisa que está sem internet, e que dá pra pesar e finalizar normalmente. |
| "Confirmar" (o item entra com 7.210 kg) e "Salvar Ticket de Pesagem": a janela "Ticket OFF-01 guardado neste aparelho" com o aviso "Comprovante provisório (sem número oficial). O ticket sobe sozinho quando a internet voltar e a 2ª via já sai numerada.", o botão "Valorizar (precisa de internet)" apagado e, no canto, "Ticket guardado neste aparelho · Comprovante PROVISÓRIO (OFF-01)". A faixa vermelha passa a "Sem conexão — 1 operação pendente (será sincronizado ao reconectar)". [ZOOM: o título e o aviso da janela] | Você pesa do mesmo jeito, confirma e salva. O ticket fica guardado neste computador, e o comprovante do motorista sai como provisório, sem o número oficial. |
| "Fechar". "Opções avançadas" (com o sinal cortado no botão): "Fotos do pedido", "Anexar" apagado e "Disponível com internet." [ZOOM: o balão] No fim, Esc e "Voltar". | Só três coisas esperam a internet. Anexar foto é uma delas: o botão mostra que só fica disponível com internet. |
| A tela dos tickets com o aviso "Sem internet. Você continua pesando e imprimindo: cada ticket fica guardado neste aparelho e sobe sozinho quando a conexão voltar. 1 ticket aguardando." e "A lista abaixo mostra só o que já está no servidor. Valorizar, editar ticket já salvo e anexar foto precisam de internet." No Ticket #59, "Ações" → "Valorizar": aviso vermelho "Sem internet: não é possível valorizar agora. O ticket fica registrado com os pesos. Valorize quando a conexão voltar." "Ações" → "Editar": "Sem internet: não é possível editar um ticket já salvo. Você pode criar tickets novos normalmente." [ZOOM: cada aviso; no fim, o aviso âmbar da lista] | Valorizar é outra: o sistema avisa pra valorizar quando a conexão voltar. E editar um ticket já salvo, a mesma coisa: fica pra depois. |
| A conexão volta (passo `rede`): em uns 4 s a faixa vermelha e o aviso âmbar somem e o ticket aparece no alto de "Aguardando valorização" com o número de verdade: "Ticket #61", Cooperativa Recomeço, Alumínio latinha, 7.210 kg (no ensaio, com a semente `apos-cap08`, saiu #60). [ZOOM: o cartão novo] | Quando a conexão volta, o ticket sobe sozinho e ganha o número de verdade. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: "Novo Ticket de Pesagem" com a cooperativa, o Edson e a placa. | Pronto! Recapitulando: a gente criou o ticket da cooperativa com o fornecedor, o material, o motorista e a placa. |
| Montagem rápida: a "1ª Pesagem", "Rascunhos abertos" e o "Peso Bruto (Kg)" 3.080. | Fez a primeira pesagem na entrada, viu o rascunho salvo sozinho e fez a segunda na saída, com o bruto saindo sozinho. |
| Montagem rápida: a impureza "2" com "%", as duas abas e "Ticket #58 salvo". | Aplicou a impureza em porcentagem, atendeu um segundo caminhão em outra aba e salvou o ticket dele com valores. |
| Montagem rápida: a compra preenchida, o comprovante "NÃO VALORIZADO" e a coluna "Valorizados". | Valorizou o ticket da cooperativa, que virou uma compra já preenchida, imprimiu o comprovante e viu o ticket ir pra Valorizados quando a compra foi finalizada. |
| Montagem rápida: "Ticket #60 salvo" ("PESAGEM AVULSA") e o aviso "Sem internet." | Por fim, viu a pesagem avulsa e o ticket funcionando sem internet. |
| Cartão "Próximo: Pedidos e histórico do caixa"; cartela final. | No próximo tutorial, a gente acha e corrige um pedido antigo. Até lá! |
