# Roteiro T18 · Área do Técnico: Refrigeração e Climatização

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T18/inventario.md`).
Aula toda no computador (janela de 1024 px ou mais), logada como Camila Duarte. Todos os nomes, valores e códigos são fictícios;
as contas dos exemplos foram rodadas com as próprias funções do app (código 1.38.6).

- **Título final:** Área do Técnico: Refrigeração e Climatização
- **Vinhetas (áreas):** ÁREA DO TÉCNICO · CATÁLOGO · CARGA TÉRMICA · CONVERSÃO · ELÉTRICA · SUPERAQUECIMENTO · GASES · CICLO · DILUIÇÃO · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** O técnico em campo (T7)
- **Próximo:** Estoque, compras e inventário (T8)
- **Duração estimada:** ~14 min de vídeo (1.930 palavras de fala, ~12,4 min de voz a 2,6 palavras/s, mais vinhetas e pausas do robô; o plano previa 19 a 20 min, a fala foi enxugada para caber nos 12.500 caracteres)
- **Tamanho:** pedido do Kaik para a voz deste tutorial: no máximo 12.500 caracteres (`CAPS` + `TITULOS`); o plano previa 19 a 20 min e a fala foi enxugada para caber, sem cortar nenhuma ferramenta.
- **Estado inicial (fim do T7):** Glacial Cold Brasil, segmento "Refrigeração e Climatização"; Camila Duarte (admin) logada; Rafael Lima e os outros técnicos; Colégio Monte Verde com o
  "Hi-Wall 18.000 BTUs - Sala dos professores" (marca Aerovento, modelo AV-HW18; T3); OS #16 Concluída (T7), saldos de estoque do T7.
- **Esta aula não cria nem altera dados da empresa:** tudo é cálculo e consulta na tela. O estado ao fim é o do início (`seeds-extra/t18/` = fim do T7 + catálogo).
- **Entra por seed "de bastidor", antes do cap01:** o **catálogo global fictício** (marcas Aerovento, Nortec, Brisamar e Cristalar, sem logos): Ar Condicionado com Hi-Wall 9.000, 12.000 e 18.000 BTUs, Cassete 36.000 BTUs
  e Piso-Teto 48.000 BTUs (o Hi-Wall 18.000 BTUs da Aerovento com código AV-HW18, gás R-410A, consumo e potência preenchidos), cerca de 14 códigos de erro (E1, E4, F1, P4...) com diagnóstico em passos e solução genéricos,
  2 compressores com ficha (capacitor de trabalho de 40 µF no de 18.000 BTUs), 2 geladeiras (consumo de 24 h/dia), 2 controles remotos e 8 fluidos (R-410A, R-32, R-22, R-134a, R-404A, R-290, R-407C, R-448A).
  Uma **OS Em Andamento** (check-in feito) só para o cap03, fora do estado final.
- Decisões padrão: catálogo fictício e sem logos; prévia de outro ramo só com "Energia Solar" (sem clicar em "Falar com representante"); "Baixar manual" só apontado; sem histórico, recentes nem favoritos de modelos (não existem);
  no Superaquecimento a lista de fabricantes só passa na tela e a escolha é "Padrão"; o aviso de pressão fora da faixa só é falado (não se encena); cada capítulo começa com os campos nos padrões da ferramenta (sem memória de sessão).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[ILUSTRAÇÃO: ...]` (nenhuma nesta aula: tudo aparece na tela).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Área do Técnico: Refrigeração e Climatização". | (sem fala) |
| Dashboard da Dominex, logado como Camila Duarte (Glacial Cold Brasil); a câmera desliza pelo menu lateral e para no item "Área do Técnico™", logo depois do grupo Operacional. | Oi! Neste tutorial a gente vai conhecer a Área do Técnico, a caixa de ferramentas de refrigeração e climatização que fica dentro da Dominex. |
| A câmera fica no item "Área do Técnico™". | São as contas e as consultas do dia a dia do técnico: quantos BTUs uma sala pede, qual capacitor usar, a pressão de um gás, o código de erro de um split. Tudo reunido num lugar só, pra apoiar o atendimento. |
| Cartão discreto: "Antes: O técnico em campo". | Se você ainda não viu o tutorial O técnico em campo, dá uma olhada antes. [pause] Vamos começar abrindo a Área do Técnico. |

### cap01 · O segmento define as ferramentas (vinheta: ÁREA DO TÉCNICO)

| Tela | Fala |
| --- | --- |
| Clique em "Área do Técnico™" no menu lateral: abre a tela com o título "Área do Técnico™", o selo ciano "Refrigeração e Climatização" ao lado e, na esquerda, o menu das ferramentas ("Início", "Catálogo", "Carga Térmica"...). | A Área do Técnico fica no menu da esquerda, logo depois do grupo Operacional. Quando abre, o selo aqui no alto mostra o segmento da empresa: Refrigeração e Climatização. |
| Clique no selo: abre a lista de nichos com a busca "Buscar nicho..."; o nicho da empresa vem primeiro, com a marca "Incluído". | É o segmento que define quais ferramentas a empresa usa. Clicando no selo, aparece a lista de ramos, e o da Glacial vem primeiro, com a marca Incluído. |
| Escolhe "Energia Solar": o menu mostra itens com cadeado e o conteúdo vira o cartão "Ferramentas de Energia Solar"; a câmera passa pelo botão "Falar com representante" (sem clicar). [Não clicar: abre o WhatsApp comercial da Dominex em outra aba. Não escolher "Assistência Técnica (TI)", que não tem prévia] | Escolhendo outro ramo, como Energia Solar, aparece uma prévia: as ferramentas daquele ramo com um cadeado, e o botão Falar com representante. |
| Escolhe de volta "Refrigeração e Climatização" (a marca "Incluído"); o menu das dez ferramentas volta. | Volto pro nosso segmento, e as ferramentas de refrigeração estão todas aqui. |

### cap02 · O Início (vinheta: ÁREA DO TÉCNICO)

| Tela | Fala |
| --- | --- |
| Clique em "Início": o hub com "Ferramentas" ("Escolha uma ferramenta para começar.") e os dez cartões coloridos; a câmera percorre "Catálogo", "Carga Térmica", "Conversão", "Cálculo de Capacitor", "Cabo Elétrico", "Superaquecimento", "Régua de Gases", "Retrofit de Gás", "Ciclo de Refrigeração" e "Diluição de Produto". | Já dentro, o Início é a porta de entrada. Em Ferramentas ficam os dez cartões, um pra cada ferramenta, e a gente passa por todos eles hoje. |
| Rola até "Termos Técnicos Explicados"; digita "capacitor" em "Buscar termo (ex: BTU, capacitor, pressão)"; abre o termo "Capacitor" e a câmera passa pela descrição e pelo "Exemplo" (compressor de 18.000 BTUs, capacitor de uns 40 µF). | Logo abaixo ficam os Termos Técnicos Explicados, um glossário pra quando aparece uma sigla ou uma unidade que você não conhece. Digito capacitor, abro o termo, e vem a explicação em linguagem simples. O exemplo diz que um compressor de dezoito mil BTUs costuma usar uns quarenta microfarads. Guarda esse número, que ele volta daqui a pouco. |
| Limpa a busca: aparecem os quatro grupos "Medidas e Unidades", "Ciclo Básico de Refrigeração", "Elétrica e Instalação" e "Gases e Nomenclatura"; abre um grupo. | Sem a busca, os termos ficam em quatro grupos: Medidas e Unidades, Ciclo Básico de Refrigeração, Elétrica e Instalação, e Gases e Nomenclatura. |

### cap03 · Dentro da ordem de serviço (vinheta: ÁREA DO TÉCNICO)

| Tela | Fala |
| --- | --- |
| Na Agenda, abre uma OS em andamento (resumo da OS e "Preencher OS"): a tela da ordem abre em tela cheia, com o botão redondo da ferramenta no canto inferior esquerdo. [BACKEND: uma OS Em Andamento com check-in feito, do Rafael Lima semeada só para este capítulo, ou a da Júlia Santos que o T5 já semeia (a fala não cita o técnico); a tela do técnico e a rota `/os-tecnico/:id` do T7; WebGL do fundo do botão] [TESTAR: abrir a tela do técnico como gestora; se travar por ser OS de outro técnico, gravar o capítulo como o técnico responsável (`"user"`)] | E durante o atendimento? Aqui está uma ordem de serviço em andamento. Lembra do botão redondo no canto da tela, que a gente viu no tutorial anterior? |
| Clique no botão redondo: a Área do Técnico abre em tela cheia, por cima da ordem, com o mesmo Início. | Um clique, e a Área do Técnico abre por cima da ordem, com as mesmas ferramentas. |
| Clique em "Conversão" (a ferramenta abre); clique no botão vermelho "Voltar para OS", no rodapé: a ordem reaparece como estava. | Abro a Conversão, por exemplo. Quando terminar a consulta, é só clicar em Voltar para OS, e a ordem continua exatamente de onde parou. |
| A câmera fica no cartão "Checklists" da ordem. | As ferramentas guardam o que você digitou enquanto o navegador ficar aberto, então dá pra ir e voltar sem perder a conta. A Área do Técnico é a caixa de ferramentas, e o preenchimento da ordem continua na própria OS. |

### cap04 · Marcas, modelos e códigos de erro (vinheta: CATÁLOGO)

| Tela | Fala |
| --- | --- |
| Volta à Área do Técnico (menu lateral) e clica em "Catálogo": título "Catálogo - Ar Condicionado" com o selo verde "N itens"; a câmera percorre as cinco abas ("Ar Condicionado", "Compressores", "Linha Branca", "Controles Remotos" e "Fluidos Refrigerantes") e para na grade de marcas. [BACKEND: semente do catálogo global fictício (`equipment_brands`, `equipment_model_categories`, `equipment_models` com a potência no nome, `equipment_error_codes`, `compressor_specs`, `remote_configs` e `refrigerant_gases`), sem logos; sem ela a tela diz "Catálogo em atualização"; o backend falso precisa entender o embed `model:equipment_models!inner(...)` com filtro `model.domain`, `in.(...)`, `limit=5000` e `order` com `nullsFirst`; vigiar o `desconhecidos.log`] | Passando pro Catálogo, que é a biblioteca de equipamentos. Ele tem cinco abas: Ar Condicionado, Compressores, Linha Branca, Controles Remotos e Fluidos Refrigerantes. A gente começa pelo Ar Condicionado. É uma consulta online, então é só estar conectado. |
| Clique em "Buscar por marca, equipamento ou código de erro" e digita "E1": a lista passa a ter as seções "Catálogo" e "Códigos de Erro", com o código agrupado e os aparelhos em que ele aparece; limpa a busca. | Imagina que o split de um cliente mostrou E1 no display. É só digitar o código na busca: ela procura por marca, por equipamento e por código de erro, e mostra em quais aparelhos ele existe. |
| Clique em "Filtros": janela com os grupos "Potência", "Tipo" e "Gás refrigerante"; marca "18.000 BTUs" em "Potência" e clica em "Ver resultados": aparecem os cartões dos modelos dessa potência, de todas as marcas. Limpa os filtros. | Também dá pra filtrar por potência, por tipo e por gás refrigerante. Marco dezoito mil BTUs e clico em Ver resultados: aparecem os modelos dessa potência, de todas as marcas. |
| Clique na marca "Aerovento": a tela da marca, com a faixa de marcas e os modelos por potência crescente; a câmera para no cartão "Hi-Wall 18.000 BTUs" e percorre os selos (potência, tipo, gás e "Cód.: AV-HW18"). | Pelo caminho das marcas é parecido. Entro na Aerovento, e os modelos aparecem em ordem de potência. Este é o Hi-Wall dezoito mil BTUs, o mesmo aparelho do Colégio Monte Verde. O cartão traz a potência, o tipo, o gás refrigerante e o código do modelo. |
| No cartão, zoom em "Consumo de energia" ("Por hora" e "Por mês"); clique em "Ajustar": abre "Tarifa e uso"; digita a tarifa em "Tarifa (R$/kWh)", muda "Horas de uso por dia" (controle deslizante) e clica em "Aplicar": os valores se atualizam. [TESTAR: mexer no controle deslizante pelo teclado] | O cartão ainda estima o consumo de energia. Em Ajustar, eu coloco a tarifa da minha região e as horas de uso por dia, clico em Aplicar, e o valor por hora e por mês se atualiza. |
| Clique em "Códigos de erro": a tela "Hi-Wall 18.000 BTUs - Aerovento" com o campo "Informe o código de erro no display"; digita "E1", abre o código e a câmera percorre "Diagnóstico" (passos), "Solução" e "Componente:". | Agora o Códigos de erro. Digito o E1 que apareceu no display, abro o código, e o Diagnóstico vem em passos, com a Solução e o componente envolvido. |
| Volta ao cartão; a câmera passa pelo botão "Baixar manual" (sem clicar). [Não clicar: baixa um arquivo; na semente, `manual_url` fictícia e `manual_type` vazio para o botão sair "Baixar manual"] | E, quando o modelo tem manual, o botão Baixar manual salva o arquivo. |

### cap05 · Compressores, linha branca, controles e fluidos (vinheta: CATÁLOGO)

| Tela | Fala |
| --- | --- |
| Clique na aba "Compressores": a grade de marcas; entra em "Nortec", clica em "Ficha técnica" do compressor de 18.000 BTUs; a câmera percorre "Capacitor de trabalho", "Capacitor de partida", "Óleo" e "Equivalências". | O Catálogo ainda tem mais quatro abas. Em Compressores, a Ficha técnica reúne o que o técnico procura na hora da troca: os capacitores de trabalho e de partida, o óleo e as equivalências com outros modelos. |
| Clique na aba "Linha Branca"; entra em "Brisamar"; no cartão da geladeira, zoom em "Consumo de energia" ("estimado · 24 h/dia") e no botão "Códigos de erro". | Na Linha Branca, geladeiras e freezers também trazem códigos de erro e consumo, que aqui é estimado em vinte e quatro horas por dia. |
| Clique na aba "Controles Remotos": a lista com a busca "Buscar por marca ou controle"; clica em "Ver detalhes técnicos" de um controle: "Detalhes Técnicos" com "Como configurar" e "Código universal". | Em Controles Remotos, os Detalhes Técnicos mostram como configurar o controle e o código universal dele. |
| Clique na aba "Fluidos Refrigerantes": as seções "Puros" e "Misturas (blends)"; clica em "R-32": a ficha "Fluido Refrigerante" com o potencial de aquecimento global (GWP), a "Classe de segurança" e o campo "Substitui". [Não clicar em "Ficha técnica" nem em "Guia do fabricante": abrem links externos] | E em Fluidos Refrigerantes ficam os gases, separados em Puros e Misturas. Abrindo o R-32, a ficha mostra o potencial de aquecimento global, a classe de segurança e o que ele substitui. |

### cap06 · Quantos BTUs o ambiente pede (vinheta: CARGA TÉRMICA)

| Tela | Fala |
| --- | --- |
| Clique em "Carga Térmica" no menu das ferramentas: título "Carga Térmica" ("Dimensione a capacidade em BTUs do ambiente."), os seis campos e o cartão de resultado. | Passando pras calculadoras. A Carga Térmica diz quantos BTUs o ambiente pede. Imagina que o Colégio Monte Verde quer conferir o aparelho da sala dos professores. |
| Digita "Altura (metros)" 2,8, "Largura (metros)" 4 e "Comprimento (metros)" 5; depois "Quantidade de pessoas" 4, "Eletroeletrônicos" 3 e "Janelas (2 x 1,5 metros)" 1: o resultado vai se atualizando e para em "16.800 BTUs". | Coloco a altura, dois vírgula oito metros, a largura, quatro, e o comprimento, cinco. Depois, quatro pessoas, três eletroeletrônicos e uma janela. Repara que o resultado vai se atualizando enquanto eu digito: dezesseis mil e oitocentos BTUs. O aparelho que está lá, de dezoito mil, fica bem perto disso. |
| Clique na chave "BTU" / "TR": o resultado mostra "1,4 TR"; volta para "BTU". | Dá pra ver também em TR, a tonelada de refrigeração, que vale doze mil BTUs: aqui, um vírgula quatro. |
| Liga "Ambiente ensolarado?": o resultado sobe para "21.200 BTUs"; a câmera passa pela nota abaixo do resultado e, depois, pelo rodapé "Ferramenta de apoio...". | Se a sala pega sol, é só ligar o Ambiente ensolarado, e o resultado sobe pra vinte e um mil e duzentos BTUs. A nota da ferramenta recomenda escolher um aparelho com a potência indicada ou maior. E no rodapé fica o lembrete: os valores são de apoio, então vale conferir a placa do equipamento e o manual do fabricante. |

### cap07 · Pressão, temperatura, potência e medidas (vinheta: CONVERSÃO)

| Tela | Fala |
| --- | --- |
| Clique em "Conversão": título "Conversão" ("Converta entre unidades de medida."), as abas "Pressão", "Temperatura", "Potência" e "Comprimento"; em "Pressão", digita 10 em "De" (bar): o campo "Para" (psi) mostra 145,037738; clique em "Inverter unidades". | Na Conversão, a gente troca de unidade sem calculadora. Em Pressão, digito dez bar e já vejo uns cento e quarenta e cinco psi. O Inverter unidades faz o caminho de volta. Temperatura, Potência e Comprimento funcionam do mesmo jeito. |
| Em "Mais usadas", clique em "HP → BTU/h": aparece "Modo de cálculo" com "Refrigeração" e "Energia"; digita 2 em "De": com "Refrigeração", "18.000"; clique em "Energia": "5.088". | Em Mais usadas ficam os atalhos do dia a dia, como HP pra BTUs por hora e milímetros pra polegadas. No HP vale escolher o Modo de cálculo: em Refrigeração, que é a conta comercial, dois HP são dezoito mil BTUs por hora. Em Energia, que é a conta física, são cinco mil e oitenta e oito. |
| Em "Mais usadas", clique em "mm → pol": digita 6,35 em "De" (mm): o campo "Para" (pol) mostra 0,25. | Na tubulação de cobre, por exemplo, seis vírgula trinta e cinco milímetros são um quarto de polegada. |
| Clique na estrela "Favoritar conversão"; a conversão aparece em "Favoritas", acima dos atalhos. | E a estrela guarda a conversão em Favoritas, pra voltar nela com um clique. |

### cap08 · Capacitor (vinheta: ELÉTRICA)

| Tela | Fala |
| --- | --- |
| Clique em "Cálculo de Capacitor": a chave "Fase" em "Monofásico" e a chave "Cálculo" em "Estimativa (BTU)"; em "Selecione o BTU" escolhe "18.000"; em "Selecione a tensão" deixa "220V": aparece "Capacitor recomendado": "Use o capacitor de 40 µF", com "Amper" 8,38 e "Potência" 1.844. | Daqui pra parte elétrica, começando pelo capacitor. Imagina o Hi-Wall dezoito mil BTUs do colégio, em duzentos e vinte volts. Escolho o BTU, escolho a tensão, e a Dominex recomenda o capacitor: quarenta microfarads, além da corrente e da potência esperadas. |
| Clique na foto do capacitor: amplia; fecha. | A foto ajuda a identificar a peça, e dá pra ampliar. |
| Clique em "Preciso (LRA)": o campo "LRA (Locked Rotor Amps)"; digita 30: "Use o capacitor de 31 µF". | Se você tem a etiqueta do compressor na mão, o modo Preciso usa o LRA, a corrente de rotor bloqueado. Com trinta ampères, o resultado é trinta e um microfarads. Sem a etiqueta, é só usar a Estimativa por BTU. |
| Clique em "Trifásico": a câmera passa por "Entrada", "Tensão trifásica" e "Contator recomendado" com "Relé térmico:" (sem digitar). | E em Trifásico a lógica muda: a máquina não usa capacitor, e a ferramenta recomenda o contator e o relé térmico a partir da corrente do motor. |

### cap09 · Cabo e disjuntor (vinheta: ELÉTRICA)

| Tela | Fala |
| --- | --- |
| Clique em "Cabo Elétrico": em "Selecione a capacidade (BTU)" escolhe "18.000"; a chave de tensão em "220v"; digita 20 em "Distância do quadro elétrico (m)": "É recomendado utilizar" mostra "Cabo elétrico: 4 mm²" e "Disjuntor: 16 A", com a queda de tensão (1,4%) e o cartão "Disjuntor recomendado" com a foto (bipolar). | Seguindo na parte elétrica, o cabo e o disjuntor. Escolho dezoito mil BTUs, duzentos e vinte volts, e a distância até o quadro elétrico: vinte metros. A Dominex indica o cabo de quatro milímetros quadrados e o disjuntor de dezesseis ampères, com a queda de tensão e a foto do disjuntor. |
| Muda a distância para 30: o cabo vai para "6 mm²" e o disjuntor continua "16 A". | Aumentou a distância? É só mudar o número, e o cabo é recalculado: com trinta metros, passa pra seis milímetros quadrados. |

### cap10 · Superaquecimento e subresfriamento (vinheta: SUPERAQUECIMENTO)

| Tela | Fala |
| --- | --- |
| Clique em "Superaquecimento": título "Superaquecimento e Subresfriamento", aba "Superaquecimento (SH)". Clique em "Modelo / fabricante": a lista abre (a câmera não demora nela: os nomes de fabricantes são rótulos do próprio app) e escolhe "Padrão". "Fluido Refrigerante" fica em "R-410A" e "Unidade de pressão" em "psi". | E agora o coração do trabalho com gás: pressão e temperatura. No Superaquecimento, primeiro escolho o Modelo ou fabricante. Se o modelo está na lista, a Dominex já sugere o gás e a faixa ideal daquele fabricante. Como aqui eu não sei o modelo, fico com Padrão. O gás é o R-410A, e a unidade de pressão, psi. |
| A câmera passa pela nota do modelo, abaixo da seleção ("Valor genérico de referência..."). | A nota embaixo lembra que a faixa do Padrão é uma referência genérica, então o manual do fabricante tem a palavra final. |
| Digita 118 em "Pressão de baixa (sucção)" e 12 em "Temperatura da linha de sucção": o resultado "7,7 °C" com o selo verde "Ideal" e "Temperatura de saturação". | Meço a pressão de baixa, cento e dezoito psi, e a temperatura da linha de sucção, doze graus. O superaquecimento dá sete vírgula sete graus, com o selo Ideal, porque está dentro da faixa. |
| Muda para 125 e 15: o resultado vai a "9,1 °C" e o selo vira "Alto". | Mudando a leitura pra cento e vinte e cinco e quinze graus, o resultado vai pra nove vírgula um, e o selo vira Alto. O selo pode mostrar Baixo, Ideal ou Alto. |
| Clique na aba "Subresfriamento (SC)": digita 350 em "Pressão de alta (líquido)" e 35 em "Temperatura da linha de líquido": "6,4 °C" com o selo "Ideal". | No Subresfriamento é a mesma ideia, com a pressão de alta, trezentos e cinquenta psi, e a temperatura da linha de líquido, trinta e cinco graus: seis vírgula quatro, Ideal. |
| Zoom na chave "psi" / "bar" de "Unidade de pressão" (sem trocar). [O aviso "Trocar para bar e recalcular" não é encenado: fica só falado] | Uma dica: confere a unidade de pressão antes de digitar. Se o valor não bater com a faixa do gás, a Dominex avisa e sugere trocar a unidade com um clique. |

### cap11 · Régua de Gases (vinheta: GASES)

| Tela | Fala |
| --- | --- |
| Clique em "Régua de Gases": a régua vertical (-40 a +60 °C), os campos de pressão e de temperatura, "Gás" em "R-410A", "Unidade" em "psi" e a temperatura em 5 °C: a pressão mostra "121" psi. | A Régua de Gases mostra a pressão de saturação de cada gás por temperatura. Começo com o R-410A a cinco graus: cento e vinte e um psi. |
| Digita 150 no campo da pressão: a temperatura e a régua acompanham; arrasta a régua para cima e para baixo (passo `drag`). | É uma mão dupla: se eu digito a pressão, a temperatura acompanha, e se arrasto a régua, os dois campos se ajustam. |
| Clique em "Unidade" e escolhe "bar": a pressão passa a bar. | Dá pra ver tudo em bar também, é só trocar a Unidade. |
| Em "Gás" escolhe "R-404A": aparece "Fórmula" com vapor e líquido; clica em líquido e volta para vapor. | Nas misturas, como o R-404A, eu escolho a Fórmula, vapor ou líquido, conforme o ponto que estou medindo. |
| Em "Gás" escolhe "R-32": aparece a chama âmbar; passa o mouse sobre ela e mostra o texto do cuidado. | E o R-32 vem com o ícone de chama: o gás é inflamável, e passando o mouse aparece o cuidado a seguir. |

### cap12 · Retrofit de Gás (vinheta: GASES)

| Tela | Fala |
| --- | --- |
| Clique em "Retrofit de Gás": em "Gás atual:" escolhe "R-22"; a lista "Gases que podem substituir o R-22" mostra o "R-438A (MO99)" com o selo "Mais indicado". | Pra fechar os gases, o Retrofit. Imagina um equipamento antigo que ainda usa R-22. Em Gás atual eu escolho ele, e a lista mostra os gases que podem substituir, com o selo Mais indicado no primeiro, o R-438A. |
| A câmera percorre "Óleo", "Cuidados" e "Pressão de trabalho" do R-438A; clique na chave "Unidade:" (psi / bar) e volta. | Cada opção traz o óleo, os cuidados e a pressão de trabalho, em psi ou em bar. |
| Zoom na nota "Drop-in é a troca de gás no mesmo equipamento..."; em "Gás atual:" escolhe "R-404A": a lista se atualiza. | Drop-in é a troca de gás no mesmo equipamento, em geral só trocando o óleo e o filtro secador, sempre seguindo a ficha técnica do gás e do compressor. Mudando o Gás atual pra R-404A, a lista se atualiza. |

### cap13 · Ciclo de Refrigeração e termos (vinheta: CICLO)

| Tela | Fala |
| --- | --- |
| Clique em "Superaquecimento" e no link "Ver o ciclo de refrigeração": abre "Ciclo de Refrigeração" ("Ciclo Básico de Refrigeração") com a "Ilustração" animada. | Pra fechar o raciocínio, o ciclo de refrigeração. Quem está no Superaquecimento chega aqui pelo link Ver o ciclo de refrigeração, e também pelo menu. A Ilustração mostra o caminho do gás pelo compressor, pelo condensador, pela válvula de expansão e pelo evaporador. |
| Clique em "Imagem 2D" e volta para "Ilustração"; rola até "Termos do ciclo", abre "Compressor" (descrição e exemplo) e "Evaporador". | Se preferir, a Imagem 2D mostra o mesmo ciclo parado. E, em Termos do ciclo, cada componente é explicado, com um exemplo de campo. |

### cap14 · Produto e água (vinheta: DILUIÇÃO)

| Tela | Fala |
| --- | --- |
| Clique em "Diluição de Produto": "Modo de Diluição" em "Preparar solução"; digita 10 em "Proporção" ("1 para") e 500 em "Volume final desejado" (unidade mL): o galão mostra "Produto" 45,45 mL e "Água" 454,55 mL. | Agora a Diluição de Produto. Imagina um produto de limpeza de serpentina que pede diluição de um pra dez, e você quer quinhentos mililitros de solução. Em Preparar solução, coloco a proporção e o volume final. A Dominex mostra quanto de produto e quanto de água: quarenta e cinco vírgula quarenta e cinco mililitros de produto e quatrocentos e cinquenta e quatro vírgula cinquenta e cinco de água. |
| Zoom na chave "Unidade" (mL e L, sem trocar) e no desenho do galão com a proporção. | O galão desenhado mostra a proporção, e a unidade pode ser mililitros ou litros. |
| Clique em "Tenho X de produto": digita 50 em "Quantidade de produto": o resultado mostra "Água a adicionar". | E se você já tem uma quantidade de produto na mão, o modo Tenho X de produto diz quanto de água adicionar. |

### cap15 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o selo do segmento, o Início com os cartões, a ordem com o botão redondo e o Catálogo com o código de erro. | E é isso! Recapitulando: a gente abriu a Área do Técnico, viu como o segmento define as ferramentas e como chegar nelas de dentro da ordem de serviço. Consultou o Catálogo, com os códigos de erro, os compressores, os controles e os gases. |
| Montagem rápida: Carga Térmica, Conversão, Capacitor, Cabo Elétrico, Superaquecimento, Régua de Gases e Retrofit de Gás. | Depois passou pelas contas: carga térmica, conversão, capacitor, cabo e disjuntor, superaquecimento e subresfriamento, régua de gases e retrofit. |
| Montagem rápida: o ciclo, a diluição e o rodapé "Ferramenta de apoio...". | Fechou com o ciclo de refrigeração e a diluição de produto. Lembra que os resultados são de apoio: vale sempre conferir a placa do equipamento e o manual do fabricante. |
| Cartão "Próximo: Estoque, compras e inventário"; cartela final. | Com as ferramentas na mão, o próximo passo é cuidar do que entra e sai do estoque. No próximo tutorial, a gente vê o estoque, as compras e o inventário. Até lá! |
