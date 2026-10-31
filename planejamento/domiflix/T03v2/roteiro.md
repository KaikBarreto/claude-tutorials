# Roteiro T3 v2 · Clientes, Fornecedores e Equipamentos (Dominex 1.38.9)

Atualização do T3 (aprovado em 30/10, gravado na 1.37.56) para a **1.38.9**, a pedido do Kaik em 31/10: "Editar" e "Excluir" da ficha
foram para dentro de "Ações"; "Configurar origens" virou o modal único "Configurações", com Origens, Etiquetas e Campos personalizados de
clientes e fornecedores (recursos novos); a 1.38.9 trouxe várias etiquetas também em equipamentos, filtros, etiquetas nos seletores e
configurações reunidas. Voz nova só no que muda.

Coluna **Fala** = texto da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS está em
`narracao/tts_textos.py`. Coluna **Tela** = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela
(`inventario_delta.md`). Coluna **Voz** diz o que acontece com o áudio da linha:

- `[mantém]` texto idêntico, letra por letra, ao do T3 gravado: reaproveita o áudio (`python3 narracao/tts_textos.py diff` confere);
- `[muda]` a linha existe no T3 e só uma frase muda: a frase nova entra no lugar da antiga (`voz_nova.md`, "Trocas no lugar");
- `[nova]` linha ou capítulo que não existia: voz nova (nó novo, frase inserida ou anexada).

Todos os nomes, documentos e telefones são fictícios.

- **Título final:** Clientes, Fornecedores e Equipamentos (o mesmo do T3: o "Próximo" do T1 e o "Antes" do T4 continuam valendo).
- **Vinhetas (áreas):** CLIENTES · FORNECEDORES · EQUIPAMENTOS · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3).
- **Antes:** Introdução e configurações iniciais (a fala do cap00 não muda).
- **Próximo:** Tipos de Serviço, Tipos de Tarefa e Checklists (T4).
- **Duração estimada:** ~14 min de vídeo. O T3 tem 12:13; o v2 soma ~1:46: dois capítulos novos (~71 s de fala), quatro frases inseridas
  ou anexadas (~20 s), duas vinhetas (~7 s) e folga de robô (~8 s). 1.993 palavras de fala (T3: 1.769), ~12,8 min de voz a 2,6 palavras/s.
  Conta completa em `voz_nova.md`, "Duração".
- **Estado inicial (igual ao do T3):** Glacial Cold Brasil com 12 clientes, 4 fornecedores e 25 equipamentos; Camila Duarte (admin) logada;
  todos os módulos ligados (PDV, CRM, contratos, portal do cliente). **Entra por seed (sem câmera):** etiqueta **Preferencial**
  (clientes e fornecedores, laranja `#F97316`, sem atribuição a ninguém).
- **Criado ao vivo (igual ao do T3):** Colégio Monte Verde, Marcos Antônio Braga, Luana Martins (pelo formulário público), Pousada Sol Nascente,
  origem Site, contato Antônio Ferreira, formulário "Cadastro de novos clientes", fornecedor Ventura Gás e Tubos, campo Tensão (lista
  127 V, 220 V e 380 V, obrigatório), categoria Multi Split, Hi-Wall 18.000 BTUs - Sala dos professores e Cassete 36.000 BTUs - Recepção,
  anexo do manual e a tarefa "Trocar as pilhas do controle".
- **Criado ao vivo (novo no v2):** etiqueta **Contrato PMOC** (clientes e fornecedores, azul `#3B82F6`) e etiqueta **Em garantia**
  (equipamentos, verde `#22C55E`); campo de cliente **Horário de acesso** (Texto, visível, não obrigatório, portal desligado).
  Atribuições: Colégio Monte Verde recebe Contrato PMOC e Preferencial; Ventura Gás e Tubos recebe Preferencial; o Hi-Wall do colégio recebe
  Em garantia; o valor "Depois das 17h ou aos sábados" vai no campo Horário de acesso do colégio.
- **Estado final:** o do T3 mais os itens acima (`seeds-extra/t3v2/apos-cap12.json`, o último capítulo que mexe em dados; a capturar na gravação). O T4 continua
  partindo dele (o T4 trabalha em Serviços, que nada disso toca).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar),
  `[ILUSTRAÇÃO: ...]`. Nesta atualização não entra ilustração nova.

## Mapa dos capítulos (v2 ← T3)

| v2 | Título da vinheta | Área | T3 | Voz |
| --- | --- | --- | --- | --- |
| cap00 | Abertura | (sem vinheta) | cap00 | mantém |
| cap01 | A tela de Clientes | CLIENTES | cap01 | 2 frases mudam (selo PJ; nome do botão) |
| cap02 | Cliente empresa pelo CNPJ | CLIENTES | cap02 | mantém |
| cap03 | Cliente pessoa física pelo CEP | CLIENTES | cap03 | mantém |
| cap04 | Origens | CLIENTES | cap04 | 1 frase muda ("Configurações") |
| cap05 | A ficha do cliente | CLIENTES | cap05 | 1 frase muda (menu "Ações") |
| cap06 | Etiquetas | CLIENTES | novo | nova |
| cap07 | Campos personalizados | CLIENTES | novo | nova |
| cap08 | Formulário de captação | CLIENTES | cap06 | mantém |
| cap09 | Fornecedores | FORNECEDORES | cap07 | 1 frase nova no buraco da emenda do T3 |
| cap10 | Preparando os equipamentos | EQUIPAMENTOS | cap08 | 3 frases mudam + 1 frase anexada no fim |
| cap11 | Cadastrando um equipamento | EQUIPAMENTOS | cap09 | 2 frases inseridas |
| cap12 | QR Code e etiqueta | EQUIPAMENTOS | cap10 | mantém |
| cap13 | Recapitulando | RESUMO | cap11 | 1 frase inserida |

### cap00 · Abertura

| Tela | Fala | Voz |
| --- | --- | --- |
| Vinheta Domiflix com o título "Clientes, Fornecedores e Equipamentos". | (sem fala) | |
| Tela inicial do Dominex, logada. | Oi! Neste tutorial a gente vai deixar a base da sua empresa pronta no Dominex: os clientes, os fornecedores e os equipamentos que você atende. | [mantém] |
| Câmera desliza devagar pelo menu Gestão. | Parece só cadastro, mas é daqui que saem as ordens de serviço, os contratos e até o QR Code colado em cada aparelho. Então vale fazer com calma. | [mantém] |
| Cartão discreto: "Antes: Introdução e configurações iniciais". | Se você ainda não fez as configurações iniciais da empresa, dá uma olhada antes no tutorial de introdução. [pause] Vamos começar pelos clientes. | [mantém] |

### cap01 · A tela de Clientes (vinheta: CLIENTES)

| Tela | Fala | Voz |
| --- | --- | --- |
| Menu lateral, grupo Gestão, clique em "Clientes e Fornecedores". [BACKEND: o `schema.json` precisa conhecer `party_labels` e as tabelas de atribuição; a lista de clientes as consulta desde o primeiro quadro] | Os clientes ficam aqui no menu da esquerda, em Gestão, Clientes e Fornecedores. | [mantém] |
| Tela "Clientes e Fornecedores": abas Clientes e Fornecedores, "Lista de Clientes" à esquerda (com "Filtros" ao lado da busca), "Selecione um cliente" à direita. | A tela tem duas abas, Clientes e Fornecedores. Na aba Clientes, a lista fica na esquerda e a ficha abre do lado direito, sem sair da tela. | [mantém] |
| Clique em "Padaria Bom Grão": a ficha abre. Clique em "Hotel Mirante do Mar": a ficha troca. | Olha: clico na Padaria Bom Grão e a ficha dela abre aqui do lado. Clico em outro cliente e ela troca na hora. | [mantém] |
| Zoom numa linha: documento, telefone, cidade e o selo "PJ" (ainda não há etiqueta colorida em nenhum cliente). | Cada linha mostra o documento, o telefone e a cidade. E esse selo diz se é pessoa jurídica ou pessoa física. | [muda] frase 2 |
| Digita "mirante" em "Buscar clientes..."; sobra só o hotel. Limpa a busca. | Pra achar alguém rápido, use a busca. Ela procura pelo nome, documento, telefone, cidade, e-mail e até pelo endereço. | [mantém] |
| Destaque nos botões do topo: "Configurações" (ícone de ajustes), "Formulários de captação", "Novo Cliente". [TESTAR: `within: 'main'`, porque "Configurações" também existe no menu lateral] | Aqui em cima ficam os três botões que a gente vai usar hoje: Configurações, Formulários de captação e Novo Cliente. Vamos começar pelo Novo Cliente. | [muda] frase 2 |

### cap02 · Cliente empresa pelo CNPJ (vinheta: CLIENTES)

| Tela | Fala | Voz |
| --- | --- | --- |
| Clique em "Novo Cliente"; a janela abre na aba "Contato". [TESTAR: na 1.38.9 a aba traz "Etiquetas" ("Sem etiquetas") em "Outros dados", entre "Origem" e "Observações"; sem fala e sem clique] | Imagina que o Colégio Monte Verde te ligou pedindo um orçamento pros aparelhos da escola. Bora cadastrar. | [mantém] |
| Zoom nas abas "Contato", "Fiscal" e "Portal"; clique em "Fiscal". | A janela tem três abas: Contato, Fiscal e Portal. Quando o cliente é empresa, a dica é começar pela Fiscal, porque o CNPJ preenche quase tudo sozinho. | [mantém] |
| Digita o CNPJ em "CPF/CNPJ"; no último número a lupa gira e aparece "Dados da empresa preenchidos!". | Eu digito o CNPJ aqui... e quando completa o último número, o sistema busca na Receita. Pronto: dados da empresa preenchidos. | [mantém] |
| Zoom em Razão Social, Nome Fantasia, E-mail fiscal e no bloco "Endereço fiscal" (CEP, Logradouro, Número, Bairro, UF / Cidade). | Veio a razão social, o nome fantasia, o e-mail e o endereço completo. Repara que o endereço do cliente fica aqui na aba Fiscal, nesse bloco Endereço fiscal. É ele que aparece no mapa, na ordem de serviço e no orçamento. | [mantém] |
| Digita "Bloco B" em "Complemento". | Se faltar alguma coisa, como o complemento, é só completar. | [mantém] |
| Volta para a aba "Contato": "Nome" já preenchido, "Tipo" em Pessoa Jurídica. | Voltando pra aba Contato, o nome já veio preenchido e o tipo já tá como Pessoa Jurídica. | [mantém] |
| Digita o "Celular"; o interruptor "Receber mensagens pelo WhatsApp" libera e fica ligado. [TESTAR: desde a 1.38.5 o interruptor já nasce ligado; o clique do robô só roda se estiver desligado] | Agora o celular de quem cuida dos aparelhos lá. Com o número completo, libera essa opção: Receber mensagens pelo WhatsApp. Com ela ligada, o cliente passa a receber pelo WhatsApp os avisos de ordem de serviço, de cobrança e de vencimento. | [mantém] |
| Abre "Origem" e escolhe "Indicação". | Em Origem, eu marco de onde esse cliente veio. Esse aqui foi indicação. Já já a gente vê como organizar essa lista. | [mantém] |
| Digita em "Observações": "Visitas só depois das 17h ou aos sábados." | Em Observações vale anotar o que a equipe precisa saber antes de ir, tipo o horário em que dá pra entrar na escola. | [mantém] |
| Clique na aba "Portal": cartão "Portal do cliente" com "Portal ativo" ligado. | A terceira aba é a do Portal, o link onde o cliente acompanha as ordens de serviço, os equipamentos e as cobranças. Ele já vem ligado, pronto pra usar. A gente vê isso no tutorial do Portal do Cliente. | [mantém] |
| Clique em "Criar"; aviso "Cliente criado com sucesso!"; o colégio aparece na lista. [TESTAR: o botão "Criar" fica desabilitado enquanto as etiquetas carregam; esperar a rede ociosa antes do clique] | Agora é só clicar em Criar. Pronto, cliente criado! Repara que a janela fecha e ele entra na lista, em ordem alfabética. Pra ver os detalhes, é só clicar nele. | [mantém] |

### cap03 · Cliente pessoa física pelo CEP (vinheta: CLIENTES)

| Tela | Fala | Voz |
| --- | --- | --- |
| "Novo Cliente"; digita "Marcos Antônio Braga" em "Nome". | Agora um cliente pessoa física. O Marcos quer instalar um split no apartamento dele. Começo pelo nome... | [mantém] |
| "Tipo": escolhe "Pessoa Física". | ...e troco o tipo pra Pessoa Física. | [mantém] |
| Digita o "Celular", WhatsApp ligado, digita o "Email". | Coloco o celular, deixo o WhatsApp ligado, e depois o e-mail dele. | [mantém] |
| "Origem": "Instagram". Zoom rápido no botão "+" ao lado do campo. | Ele chegou pelo Instagram. E se a origem não estivesse na lista, esse botão de mais do lado cria uma nova na hora, sem sair da janela. | [mantém] |
| Aba "Fiscal": digita o CPF em "CPF/CNPJ". | Na aba Fiscal vai o CPF. É só digitar o número. | [mantém] |
| Digita o "CEP"; aviso "Endereço encontrado!"; Logradouro, Bairro e UF / Cidade se preenchem. | No endereço, eu começo pelo CEP. Completou os oito números, ele já traz a rua, o bairro e a cidade. | [mantém] |
| Digita "Número" e "Complemento" ("Apto 702"). | Aí eu completo o número e o complemento. | [mantém] |
| "Criar"; aviso "Cliente criado com sucesso!". | Criar. E pronto, mais um na lista. Uma dica: se você não sabe o CEP, dá pra digitar o nome da rua em Logradouro, que ele vai sugerindo os endereços. | [mantém] |

### cap04 · Origens (vinheta: CLIENTES)

| Tela | Fala | Voz |
| --- | --- | --- |
| Clique em "Configurações" (topo); abre "Configurações de clientes e fornecedores" já em "Origens" ("Canais de aquisição"), com Indicação, Instagram, Google e WhatsApp. A câmera passa pelo menu da esquerda ("Origens", "Etiquetas", "Campos personalizados") e termina na lista de origens. [TESTAR: `within: 'main'` no botão; o dialog abre sempre em "Origens"] | Lembra da Origem? Essa lista você monta do seu jeito, aqui em Configurações. Já tem Indicação, Instagram, Google e WhatsApp. | [muda] frase 2 |
| Digita "Site" em "Nova origem..." e clica em "Adicionar"; aviso "Origem criada!". | Vou criar mais uma: Site, pra quem chega pelo seu site. Adicionar, e pronto. | [mantém] |
| Abre o menu de uma origem: "Editar" e "Excluir". | Pelo menu de cada uma dá pra editar ou excluir. | [mantém] |
| Fecha a janela; zoom na lista de clientes. | E por que isso importa? Porque marcando a origem de cada cliente, você descobre de onde estão vindo os seus clientes e onde vale a pena investir. | [mantém] |

### cap05 · A ficha do cliente (vinheta: CLIENTES)

| Tela | Fala | Voz |
| --- | --- | --- |
| Clique em "Colégio Monte Verde"; a ficha abre na aba "Geral". | Bom, agora que os clientes tão cadastrados, vamos ver a ficha. Clico no Colégio Monte Verde. | [mantém] |
| Zoom no cabeçalho: nome com setinha, selo PJ, razão social e o botão "Ações". Passa o mouse em "Ações": abre o menu com "Copiar link do portal", "Abrir portal", "Criar oportunidade no CRM", "Editar" e "Excluir" (sem clicar em nenhum). Clique no nome: abre "Buscar cliente..."; fecha. [TESTAR: o menu abre ao passar o mouse e fecha 200 ms depois de sair; mover o mouse e gravar sem clicar, com guarda `unless`] | Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir. E clicando no nome, dá pra pular pra outro cliente sem voltar pra lista. | [muda] frase 1 |
| Cartão "Informações": Origem, CPF/CNPJ, Email, Celular com o ícone verde do WhatsApp. | No cartão Informações tá o que a gente preencheu. E esse ícone verde do lado do celular abre o WhatsApp do cliente direto. | [mantém] |
| Cartão "Endereço" com o mapa e os botões "Abrir no Google Maps" e "Abrir no Waze". | Embaixo, o endereço com o mapa, e dois botões que o técnico adora: abrir no Google Maps ou no Waze. | [mantém] |
| Cartão "Responsável no Local (falar com)": "Nenhum contato cadastrado"; clique em "Adicionar". | Agora uma parte muito útil: o Responsável no Local. É a pessoa que o técnico procura quando chega lá, que nem sempre é quem contratou o serviço. | [mantém] |
| Janela "Novo Contato": "Antônio Ferreira", Cargo "Zelador", Telefone; clique em "Adicionar". | Na escola é o seu Antônio, o zelador. Coloco o nome, o cargo e o telefone... e Adicionar. | [mantém] |
| O contato aparece no cartão; abre o menu da linha: "WhatsApp", "Editar contato", "Excluir contato". | Pronto, ele aparece aqui, e nesse menu tem o WhatsApp dele, direto. Dá pra cadastrar quantos contatos quiser. | [mantém] |
| Percorre as abas: Equipamentos, Histórico, Tarefas, Estoque, Chamados, Contratos, Documentos, Financeiro, Cobranças. | Do lado da Geral ficam as outras abas. Em Equipamentos, os aparelhos desse cliente, que a gente cadastra daqui a pouco. Em Histórico, todas as ordens de serviço. Em Tarefas, os lembretes da agenda. E tem ainda Estoque, Chamados, Contratos, Documentos, Financeiro e Cobranças. Cada uma tem o seu tutorial. O importante agora é saber que tudo desse cliente fica reunido aqui. | [mantém] |

### cap06 · Etiquetas (vinheta: CLIENTES)

Capítulo novo. Parte do fim do cap05 (a ficha do Colégio Monte Verde aberta). Etiqueta é a cor de classificação (recurso 1.38.8): o selo
"PJ" do cap01 não é etiqueta e por isso a fala do cap01 passou a dizer "selo".

| Tela | Fala | Voz |
| --- | --- | --- |
| Clique em "Configurações" (topo, `within: 'main'`): abre "Configurações de clientes e fornecedores" em "Origens"; clique em "Etiquetas" ("Cores e classificações") no menu da esquerda. [BACKEND: `party_labels` (escopo `party`) e o seed "Preferencial", laranja; defaults de `party_labels` (`scope` party, `show_in_portal` falso, `is_active` verdadeiro, `color` `#64748B`)] | Agora as etiquetas, que marcam clientes e fornecedores com uma cor. | [nova] |
| Seção "Etiquetas": título "Etiquetas", texto "Classifique clientes e fornecedores com cores fáceis de reconhecer.", botão "Nova etiqueta" e a lista com "Preferencial" (laranja). Zoom no botão e na lista. | Ficam aqui em Configurações, Etiquetas. Eu já deixei a Preferencial. | [nova] |
| Clique em "Nova etiqueta": digita "Contrato PMOC" em "Nome da etiqueta"; em "Cor saturada" abre o seletor (botão com `#DC2626`) e escolhe o azul `#3B82F6` na grade; a prévia mostra o selo azul "Contrato PMOC"; clique em "Salvar etiqueta" (aviso "Etiqueta criada!"); depois "Cancelar" e fecha a janela (X). "Mostrar nos portais" fica desligado. [TESTAR: o seletor de cor é um popover próprio (botão de cor com `title="#3B82F6"`), não `input[type=color]`; depois de salvar o formulário continua aberto em modo de edição, por isso o "Cancelar"] | Imagina que o Colégio Monte Verde tem contrato de PMOC: Nova etiqueta, escrevo Contrato PMOC, escolho a cor e Salvar etiqueta. | [nova] |
| Na ficha do Colégio Monte Verde: passa o mouse em "Ações" e clica em "Editar" (janela "Editar Cliente", aba "Contato"); rola até "Outros dados"; em "Etiquetas" ("Sem etiquetas") abre a lista "Selecione uma ou mais etiquetas", marca "Contrato PMOC" e "Preferencial" (o botão passa a mostrar "Contrato PMOC" e "+1"), fecha a lista; clique em "Salvar". [BACKEND: RPC `set_customer_labels(p_customer_id, p_label_ids)`] [TESTAR: marcar na ordem Contrato PMOC, depois Preferencial; o primeiro vira a etiqueta principal] | Pra usar, na ficha do Colégio Monte Verde, Ações, Editar, e em Etiquetas marco a nova e a Preferencial: dá pra marcar mais de uma. Salvar. | [nova] |
| A ficha mostra os dois selos ao lado do nome e, no cartão "Informações", a linha "Etiquetas". Na lista, o Colégio mostra o selo "Contrato PMOC" com a bolha "+1"; passa o mouse na bolha (dica com os dois selos). Depois clique em "Filtros" (ao lado da busca): grupo "Etiquetas", marca "Contrato PMOC", botão "Aplicar (1)"; a lista fica só com o Colégio Monte Verde; "Limpar tudo" e "Fechar". [TESTAR: "Aplicar (1)" fica no rodapé da folha, usar `clicar_fixo`] | Pronto: elas aparecem na ficha e na lista. E em Filtros dá pra ver só os clientes de uma etiqueta. | [nova] |

### cap07 · Campos personalizados (vinheta: CLIENTES)

Capítulo novo, na sequência do cap06 (a ficha do Colégio Monte Verde aberta).

| Tela | Fala | Voz |
| --- | --- | --- |
| Clique em "Configurações"; clique em "Campos personalizados" ("Informações adicionais") no menu da esquerda: título "Campos de clientes", texto "Crie informações adicionais para cadastro, ficha e portal.", botão "Novo campo" e a lista vazia ("Nenhum campo personalizado."). [BACKEND: `party_field_config` com defaults (`field_type` text, `is_visible` verdadeiro, `is_required` falso, `is_visible_in_portal` falso, `position` 0) e `customers.custom_fields` `{}`] | Agora os campos personalizados, pra guardar uma informação extra do cadastro. | [nova] |
| Clique em "Novo campo": digita "Horário de acesso" em "Nome do campo"; "Tipo" continua em "Texto"; clique em "Salvar campo" (aviso "Campo criado!"; o formulário continua aberto em modo de edição). | Lembra do horário em que dá pra entrar na escola? Clico em Novo campo, escrevo Horário de acesso e deixo o tipo Texto. Salvar campo. | [nova] |
| Abre a lista "Tipo" e mostra Texto, Número, Data, Lista de opções e Sim/Não (fecha sem trocar). Zoom nos interruptores "Visível", "Obrigatório" e "Mostrar no Portal do Cliente", sem mexer. Clique em "Cancelar". | Os outros tipos são Número, Data, Lista de opções e Sim/Não. E dá pra deixar obrigatório ou mostrar no Portal do Cliente. | [nova] |
| No topo da seção, clique em "Fornecedores": o título vira "Campos de fornecedores" e o interruptor do portal some; volta para "Clientes". Fecha a janela. | Os fornecedores têm os campos deles: é só trocar aqui em cima. | [nova] |
| Na ficha do Colégio Monte Verde: "Ações", "Editar"; em "Outros dados", a seção "Campos personalizados" mostra "Horário de acesso"; digita "Depois das 17h ou aos sábados"; "Salvar". A ficha passa a mostrar a linha "Horário de acesso" no cartão "Informações". | Pra preencher, Ações, Editar, escrevo o horário e Salvar. Ele aparece no cartão Informações. | [nova] |

### cap08 · Formulário de captação (vinheta: CLIENTES)

| Tela | Fala | Voz |
| --- | --- | --- |
| Volta para a lista; clique em "Formulários de captação"; janela vazia: "Nenhum formulário ainda". | Agora uma coisa que economiza muito tempo. Em vez de você digitar o cadastro, o próprio cliente preenche. Você manda um link pelo WhatsApp, coloca na bio do Instagram, e ele mesmo se cadastra. | [mantém] |
| "Novo formulário"; aba "Geral": Título "Cadastro de novos clientes". | Clico em Novo formulário e dou um título. | [mantém] |
| Aba "Campos": "Exibir" e "Obrigatório" em Nome e Celular; "Exibir" em CEP, Endereço, Número, Cidade e Estado (UF). | Na aba Campos eu escolho o que o cliente vai preencher e o que é obrigatório. Nome e celular, obrigatórios. O endereço, opcional. | [mantém] |
| Aba "LGPD": "Exigir consentimento" ligado e o texto padrão. | E na aba LGPD fica o texto de consentimento, que o cliente precisa aceitar antes de enviar. Já vem pronto, mas dá pra ajustar. | [mantém] |
| "Salvar"; aviso "Formulário criado com sucesso!"; na lista: "Ativo", "0 cadastro(s)". | Salvo, e o formulário já tá ativo. | [mantém] |
| "Copiar link"; aviso "Link gerado e copiado!". | Agora é copiar o link e mandar pro cliente. | [mantém] |
| Página pública do formulário (sem login): preenche "Luana Martins", celular e CEP, marca o consentimento e clica em "Enviar cadastro"; tela "Cadastro enviado com sucesso". | É isso que o cliente vê quando abre o link. Ele preenche, aceita o termo e envia. | [mantém] |
| De volta a Clientes: "Luana Martins" na lista; no gerenciador, "1 cadastro(s)". | E de volta no Dominex, a Luana já tá na lista de clientes. O cadastro entra direto, na hora. E o formulário vai contando quantas pessoas se cadastraram por ele. | [mantém] |

### cap09 · Fornecedores (vinheta: FORNECEDORES)

| Tela | Fala | Voz |
| --- | --- | --- |
| Clique na aba "Fornecedores" (ícone de caminhão); "Lista de Fornecedores" com os quatro fornecedores (com "Filtros" ao lado da busca). | Agora os fornecedores, que ficam aqui na aba do lado. É quem vende pra você: a loja de peças, o distribuidor de gás, o fabricante. | [mantém] |
| Zoom em "Novo Fornecedor" no topo do painel da direita; clique. | O botão pra cadastrar fica aqui em cima, do lado direito: Novo Fornecedor. | [mantém] |
| Janela "Novo Fornecedor": "Ventura Gás e Tubos", CPF/CNPJ, Contato "Rodrigo", Telefone, E-mail, Endereço, Observações "Gás R-410A e tubo de cobre". | O cadastro é bem simples: o nome, o CNPJ, a pessoa que te atende, telefone, e-mail e endereço. Nas observações eu anoto o que compro dele. | [mantém] |
| Volta ao topo da janela (o campo "Etiquetas" fica logo abaixo de "Nome"): abre a lista, marca "Preferencial" e fecha. [BACKEND: RPC `set_supplier_labels(p_supplier_id, p_label_ids)`] [TESTAR: cabe em ~3,3 s de fala; o robô rola até o topo e marca a etiqueta dentro da janela de 4 s que a emenda do T3 deixou em silêncio] | Lá em cima, em Etiquetas, escolho a Preferencial. | [nova] |
| "Salvar"; aviso "Fornecedor cadastrado!"; clique nele na lista (aparece o selo "Preferencial" na linha). | Salvar. | [mantém] |
| Ficha: "Dados do fornecedor" e "Histórico de Gastos" ("Nenhum gasto registrado"). A ficha ainda mostra "Editar" e "Excluir" como botões visíveis, sem fala. | Na ficha ficam os dados e o Histórico de Gastos. Toda despesa que você lançar no Financeiro escolhendo esse fornecedor aparece aqui, com o total gasto. Assim você sabe quanto compra de cada um. | [mantém] |

### cap10 · Preparando os equipamentos (vinheta: EQUIPAMENTOS)

| Tela | Fala | Voz |
| --- | --- | --- |
| Menu Gestão, "Equipamentos": "Lista de Equipamentos" com os aparelhos dos clientes (sem abas; no topo, "Configurar Campos" e "Novo Equipamento"). | Agora os equipamentos. Eles ficam em Gestão, Equipamentos. Cada equipamento é um aparelho instalado num cliente, e é nele que fica guardada cada manutenção. | [mantém] |
| Passa o mouse em "Configurar Campos" e clica: abre "Configurações de equipamentos" na seção "Categorias" (padrão); clique em "Campos personalizados" ("Informações adicionais") no menu da esquerda: Marca, Modelo, Nº de Série, Capacidade/Especificação, Local e Data de Instalação, com as colunas Nome, Tipo, Visível, Portal e Obrig. [TESTAR: o botão segue chamado "Configurar Campos" e a janela se chama "Configurações de equipamentos"; o clique na seção "Campos personalizados" tem de acontecer antes de a fala chegar em "marca, modelo..."] | Antes de cadastrar, vale decidir quais informações você quer guardar de cada aparelho. Em Configurar Campos estão os que já vêm prontos: marca, modelo, número de série, capacidade, local e data de instalação. Dá pra renomear, esconder ou mudar a ordem. | [mantém] |
| "Adicionar novo campo": "Tensão", tipo "Lista de opções", opções "127 V", "220 V" e "380 V"; "Adicionar campo"; aviso "Campo criado!". [BACKEND: `equipment_field_config.is_visible_in_portal` com default falso; o campo nasce com "Portal" desligado] | E dá pra criar os seus. Eu sempre quero saber a tensão do aparelho, então crio o campo Tensão, do tipo lista de opções: cento e vinte e sete, duzentos e vinte e trezentos e oitenta volts. | [mantém] |
| Liga "Obrig." em Tensão (último interruptor da linha); aparece "Salvo"; clique em "Categorias" no menu da esquerda da janela, sem fechar. | Marco como obrigatório. Repara que cada mudança já grava sozinha. Agora as categorias. | [muda] frase 3 |
| Seção "Categorias" ("Tipos de equipamento"): Split Hi-Wall, Split Cassete e Split Piso-Teto. Digita "Multi Split" em "Nome da categoria", escolhe a cor e clica no botão "+"; aviso "Categoria criada com sucesso!"; a categoria entra na lista. [TESTAR: não há mais o botão "Nova Categoria" nem "Criar"; o bloco de adicionar é o campo de nome, o seletor de cor nativo e o "+"] | Em Categorias, a gente separa os tipos de aparelho. Já tem Hi-Wall, Cassete e Piso-Teto. Vou criar Multi Split, escolho uma cor e clico no mais. | [muda] frases 1 e 3 |
| Clique em "Etiquetas" ("Cores e classificações"; texto "Classifique equipamentos com cores fáceis de reconhecer."): "Nova etiqueta", "Nome da etiqueta" "Em garantia", cor verde `#22C55E`, "Salvar etiqueta" (aviso "Etiqueta criada!"), "Cancelar"; fecha a janela. [BACKEND: `party_labels` com `scope` equipment; as etiquetas de equipamento são outro conjunto, não aparecem para clientes] | Por último, as Etiquetas dos equipamentos: crio Em garantia, escolho uma cor e Salvar etiqueta. | [nova] |

### cap11 · Cadastrando um equipamento (vinheta: EQUIPAMENTOS)

| Tela | Fala | Voz |
| --- | --- | --- |
| Na página Equipamentos, clique em "Novo Equipamento" (topo). | Agora sim, o equipamento. Novo Equipamento. | [mantém] |
| "Cliente": busca "Colégio" e a lista mostra "Colégio Monte Verde" com o selo "Contrato PMOC" e a bolha "+1"; escolhe-o. | Primeiro o cliente: Colégio Monte Verde. | [mantém] |
| Zoom nas etiquetas ao lado do nome do colégio na lista e, depois de escolhido, as bandeirinhas no campo "Cliente". | As etiquetas do cliente aparecem aqui, na hora de escolher. | [nova] |
| "Nome": "Hi-Wall 18.000 BTUs - Sala dos professores"; "Categoria": "Split Hi-Wall". | No nome, a dica é juntar o tipo e o lugar, assim o técnico acha rapidinho: Hi-Wall dezoito mil BTUs, sala dos professores. Categoria, Split Hi-Wall. | [mantém] |
| Campo "Etiquetas" (largura total, logo abaixo da Categoria; "Selecione uma ou mais etiquetas"): abre a lista e marca "Em garantia". [BACKEND: RPC `set_equipment_labels(p_equipment_id, p_label_ids)`] | Logo abaixo, em Etiquetas, escolho Em garantia. | [nova] |
| Marca "Aerovento", Modelo "AV-HW18", Nº de Série, Capacidade "18.000 BTUs", Local "Sala dos professores", Data de Instalação. | Marca, modelo, número de série, capacidade, o local e a data em que ele foi instalado. | [mantém] |
| Zoom em "Tensão *"; escolhe "220 V". | E olha o campo que a gente criou: Tensão, com asterisco porque é obrigatório. Duzentos e vinte. | [mantém] |
| "Validade da Garantia"; zoom em "Identificador": "Gerado automaticamente ao salvar". | Tem ainda a validade da garantia. E o identificador o sistema gera sozinho quando salva. | [mantém] |
| "Criar"; aviso "Equipamento criado com sucesso!". | Criar. Pronto! | [mantém] |
| "Novo Equipamento" de novo; em "Cliente" digita "Pousada Sol Nascente" (não existe); clique no "+"; janela "Novo cliente" com o nome; "Criar cliente"; o cliente fica escolhido. | Agora um atalho. Às vezes você tá cadastrando o aparelho e o cliente ainda nem existe no sistema. Não precisa sair daqui: digita o nome, clica no mais e cria o cliente só com o nome. Depois você completa o cadastro dele com calma. | [mantém] |
| "Cassete 36.000 BTUs - Recepção", Categoria "Split Cassete", Tensão "380 V"; "Criar" (sem etiqueta). | Termino o aparelho e crio. | [mantém] |
| Clientes, "Colégio Monte Verde", aba "Equipamentos": o Hi-Wall aparece na tabela; zoom em "Novo Equipamento". | E lembra da aba Equipamentos na ficha do cliente? O aparelho já tá lá. Se você cadastrar por aqui, o cliente já vem escolhido. | [mantém] |

### cap12 · QR Code e etiqueta (vinheta: EQUIPAMENTOS)

| Tela | Fala | Voz |
| --- | --- | --- |
| Clique no Hi-Wall; abre a ficha do equipamento, aba "Geral" (o selo "Em garantia" fica embaixo do nome e o menu "Ações" ocupa o lugar de "Editar" e "Excluir"; sem fala). | Clicando no aparelho, abre a ficha dele. | [mantém] |
| Zoom no QR Code, no identificador e no cartão "Informações" (com Tensão 220 V). | Aqui ficam todas as informações e o QR Code do equipamento. Esse QR é o que vai colado no aparelho. | [mantém] |
| "Gerar Etiqueta"; janela "Gerar Etiqueta de Identificação": "Itens da etiqueta", "Tamanho" 5×8 cm, "Pré-visualização". Marca "Nome do cliente". | Em Gerar Etiqueta você escolhe o que sai impresso: o nome e o telefone da sua empresa, o QR Code, o nome do aparelho e o identificador. Se quiser, dá pra incluir a marca, o modelo e o cliente. Escolhe o tamanho e já vê como fica. | [mantém] |
| Zoom no aviso sobre tamanho real e no botão "Imprimir" (sem clicar). | Aí é só clicar em Imprimir. Uma dica: na janela de impressão, deixa o dimensionamento em tamanho real. | [mantém] |
| Fecha; "Baixar QR (PNG)"; aviso "QR Code salvo!". | Se preferir mandar pra uma gráfica, o Baixar QR salva a imagem. | [mantém] |
| Zoom em "Abrir link" e "Copiar link". | E pra que serve esse QR? Quando o cliente ou o técnico aponta a câmera do celular, abre o portal do cliente já nesse aparelho, com o histórico de manutenção. A gente mostra isso em detalhe no tutorial do Portal do Cliente. | [mantém] |
| Aba "Anexos": "Enviar" o PDF do manual; aviso "1 anexo enviado!". | Na aba Anexos você guarda o manual, a nota de compra, as fotos da instalação. Repara que o que você anexa aqui também aparece pro cliente no portal. | [mantém] |
| Aba "Histórico / Tarefas": "Ordens de Serviço Relacionadas" vazia; em "Nova tarefa..." digita "Trocar as pilhas do controle" e adiciona. | Em Histórico ficam as ordens de serviço feitas nesse aparelho. E aqui embaixo dá pra deixar uma listinha de pendências dele, tipo trocar as pilhas do controle. | [mantém] |

### cap13 · Recap e próximo (vinheta: RESUMO)

| Tela | Fala | Voz |
| --- | --- | --- |
| Tour rápido do robô, na ordem da fala: lista de clientes; "Configurações" (Origens, depois Etiquetas e Campos personalizados, 1 s em cada); ficha do Colégio Monte Verde com os selos e a linha "Horário de acesso"; "Formulários de captação"; aba "Fornecedores"; Equipamentos com "Configurar Campos" (Categorias, Etiquetas e Campos personalizados, 1 s em cada); ficha do Hi-Wall com o QR. [TESTAR: o recap do T3 clicava "Configurar origens", na aba "Categorias" e no diálogo "Configurar Campos do Equipamento"; nada disso existe mais, o robô é reescrito] | Pronto! Recapitulando: a gente cadastrou um cliente empresa pelo CNPJ e um cliente pessoa física pelo CEP, organizou as origens e colocou o responsável no local com WhatsApp. Marcou os clientes com etiquetas coloridas e criou o campo Horário de acesso. Criou um formulário pro cliente se cadastrar sozinho, cadastrou um fornecedor e deixou os equipamentos prontos, com categoria, campo personalizado e etiqueta com QR Code. | [muda] frase nova entre as frases 3 e 4 |
| Ficha do equipamento com o QR. | Com essa base, abrir uma ordem de serviço fica muito mais rápido, porque o cliente e o aparelho já estão no sistema. | [mantém] |
| Cartão "Próximo: Tipos de Serviço, Tipos de Tarefa e Checklists"; cartela final. | No próximo tutorial, a gente cadastra os tipos de serviço, os tipos de tarefa e os checklists, que é o que o técnico preenche em cada visita. Até lá! | [mantém] |
