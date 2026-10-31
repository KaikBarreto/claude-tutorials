# Roteiro T4 · Tipos de Serviço, Tipos de Tarefa e Checklists

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T04/inventario.md`).
Todos os nomes, valores e códigos são fictícios.

- **Título final:** Tipos de Serviço, Tipos de Tarefa e Checklists (é o nome que o cartão final do T3 já promete; na trilha, "Serviços, tarefas e checklists")
- **Vinhetas (áreas):** SERVIÇOS · TAREFAS · CHECKLISTS · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Clientes, Fornecedores e Equipamentos (T3)
- **Próximo:** Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo (T5)
- **Duração estimada:** ~10 min de vídeo (1.419 palavras de fala, ~9,1 min de voz a 2,6 palavras/s, mais vinhetas e pausas do robô)
- **Estado inicial (fim do T3):** Glacial Cold Brasil com 16 clientes, fornecedores e 27 equipamentos; nenhum tipo de serviço, de tarefa nem checklist;
  módulos `nfe`, `contracts` e `video_questions` ligados (por isso aparecem a aba "Fiscal" e o campo "Frequência"); Camila Duarte (admin) logada.
- **Criado ao vivo:** categorias Instalação `#3B82F6`, Manutenção `#22C55E`, Higienização `#06B6D4`; tipo de serviço **Manutenção Preventiva**
  (MP, `#22C55E`, categoria Manutenção, preço padrão 180, vinculado a equipamento, fiscal 14.01.01 + 001 + ISS 5); tipos de tarefa Reunião
  `#8B5CF6`, Entrega de material `#F97316`, Compra de peças `#EAB308`; checklist **Manutenção preventiva de split** (modelo do catálogo, 13 perguntas,
  ligado a Manutenção Preventiva); checklist **Higienização de split** (do zero, ligado a Higienização de Split) com 4 perguntas ao vivo.
- **Entra por seed, "do mesmo jeito" (sem câmera):** Manutenção Corretiva (MC, `#F97316`, Manutenção, 220), Instalação de Split (INS, `#3B82F6`,
  Instalação, 650, fiscal 14.06.01 + 001 + ISS 5), Higienização de Split (HIG, `#06B6D4`, Higienização, 180), Carga de Gás (GAS, `#A855F7`, Manutenção, 350)
  e **Visita Técnica** (VT, `#6B7280`, sem categoria, 120, "Vinculado a equipamento" desligado); tipo de tarefa Treinamento da equipe `#3B82F6`;
  no checklist de higienização, as perguntas "Observações" (Texto) e "Assinatura do cliente" (Assinatura), além das 4 ao vivo.
- **Estado final:** `seeds-extra/t4/apos-cap14.json`; o T5 parte dele (abre OS com Manutenção Preventiva, Visita Técnica e Instalação de Split e usa os tipos de tarefa na Agenda).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[ILUSTRAÇÃO: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Tipos de Serviço, Tipos de Tarefa e Checklists". | (sem fala) |
| Dashboard da Dominex, logado como Camila Duarte (Glacial Cold Brasil); a câmera desliza pelo menu lateral até o grupo Gestão. | Oi! Neste tutorial a gente vai montar o cardápio de serviços da sua empresa e os roteiros que o técnico preenche em cada visita: os tipos de serviço, os tipos de tarefa e os checklists. |
| A câmera para no item "Serviços" do grupo Gestão. | É daqui que saem as ordens de serviço: o tipo de cada uma, o prefixo do número e o roteiro do técnico. Quanto mais caprichado esse cadastro, mais rápido fica abrir uma ordem. |
| Cartão discreto: "Antes: Clientes, Fornecedores e Equipamentos". | Se você ainda não viu o tutorial de Clientes, Fornecedores e Equipamentos, dá uma olhada antes. [pause] Vamos abrir a tela de Serviços. |

### cap01 · A tela de Serviços (vinheta: SERVIÇOS)

| Tela | Fala |
| --- | --- |
| Clique em "Serviços" no grupo Gestão do menu lateral; abre a tela com o título "Serviços" e o subtítulo "Configure os tipos de serviços, tarefas e checklists". [TESTAR: gravar sempre por Gestão e Serviços (`/checklists` e `/questionarios` redirecionam para a aba padrão)] | Os serviços ficam no menu da esquerda, em Gestão, Serviços. |
| Zoom nas abas "Tipos de Serviços", "Tipos de Tarefas" e "Checklists". | A tela tem três abas: Tipos de Serviços, Tipos de Tarefas e Checklists. O tipo de serviço diz o que a equipe vai fazer, o checklist é o roteiro dessa visita, e o tipo de tarefa organiza os compromissos internos da agenda. A gente passa pelas três, nessa ordem. |
| Aba "Tipos de Serviços" vazia ("Nenhum tipo de serviço"); zoom nos botões "Categorias" e "Novo Tipo", na linha das abas. | Na primeira aba ainda não tem nada. Aqui em cima ficam os botões Categorias e Novo Tipo. Vamos começar pelas categorias. |

### cap02 · Categorias (vinheta: SERVIÇOS)

| Tela | Fala |
| --- | --- |
| Clique em "Categorias": abre a janela "Categorias de Serviço" ("Nenhuma categoria cadastrada."). | As categorias agrupam serviços parecidos e depois viram um filtro na lista. Vale criar antes dos serviços. |
| No rodapé, "Nova categoria": digita "Instalação" em "Nome da categoria...", escolhe o azul no seletor de cor (ou digita `#3B82F6`) e clica no "+"; toast "Categoria criada!". Repete com "Manutenção" (verde, `#22C55E`) e "Higienização" (ciano, `#06B6D4`). [BACKEND: `POST service_type_categories` já coberto, `sort_order` = máximo + 1] | Escrevo o nome, escolho a cor e clico no mais. Instalação, Manutenção e Higienização. |
| Arrasta "Higienização" pela alça uma posição para cima e devolve ao fim. [TESTAR: `drag` HTML5 reordena as categorias; se falhar, só mostrar a alça] | Pela alça do lado, dá pra arrastar e deixar na ordem que você preferir. |
| Fecha a janela. | Pronto, três categorias. Agora o primeiro serviço. |

### cap03 · Novo tipo de serviço (vinheta: SERVIÇOS)

| Tela | Fala |
| --- | --- |
| Clique em "Novo Tipo": abre o modal "Novo Tipo de Serviço", aba "Dados" (pílulas "Dados" e "Fiscal"). [Lista vazia: o primeiro tipo nasce limpo; os demais não são criados ao vivo por causa da pegadinha P1] | Vou cadastrar a manutenção preventiva, que é o serviço que a Glacial mais faz. Clico em Novo Tipo. |
| Digita "Manutenção Preventiva" em "Nome *"; em "Cor", digita `#22C55E` no campo de texto ao lado do quadrado (`{"selector":"input[type=color] + input"}`). | Dou o nome, Manutenção Preventiva, e escolho uma cor, que identifica o serviço nas listas. Uma dica: uma cor diferente pra cada serviço ajuda a bater o olho. |
| Em "Categoria", escolhe "Manutenção"; digita em "Descrição": "Limpeza e conferência completa do aparelho". | Escolho a categoria Manutenção e escrevo uma descrição curta. |
| Digita "MP" em "Prefixo de Numeração OS"; zoom na prévia embaixo do campo. | No Prefixo de Numeração OS vão as letras que abrem o número da ordem de serviço. Pra preventiva, MP. Assim, quando a ordem sair, o número já mostra de que serviço se trata. |
| Digita `180` em "Preço padrão (opcional)" (campo numérico). | Em Preço padrão, coloco cento e oitenta reais. É o valor que o orçamento sugere quando você adiciona esse serviço, e dá pra ajustar na hora. |
| Zoom nos interruptores "Vinculado a equipamento" e "Ativo" (ambos ligados). | Os dois interruptores ficam ligados: o Vinculado a equipamento, que a gente explica já já, e o Ativo, que deixa o serviço disponível pra escolher. |
| Clique em "Criar"; toast "Tipo de serviço criado!"; o modal fecha e o tipo aparece na lista, com a ficha aberta à direita. | Criar. Pronto, o primeiro serviço está na lista. |
| Recarrega a lista: aparecem os outros cinco tipos (Manutenção Corretiva, Instalação de Split, Higienização de Split, Carga de Gás e Visita Técnica), "6 tipos cadastrados". [BACKEND: seed `seeds-extra/t4/apos-cap03.json` com os cinco tipos "de bastidor", carregado entre o cap03 e o cap04] | Os outros serviços da Glacial eu já deixei cadastrados do mesmo jeito: manutenção corretiva, instalação, higienização, carga de gás e visita técnica. |

### cap04 · Organizando a lista (vinheta: SERVIÇOS)

| Tela | Fala |
| --- | --- |
| Zoom na lista: título "Tipos de Serviço", "6 tipos cadastrados" e as linhas com cor, nome e "Categoria • Prefixo". | Agora a lista tem os seis serviços, cada um com a sua cor, a categoria e o prefixo. |
| Digita "higien" em "Buscar por nome ou descrição..."; sobra "Higienização de Split"; limpa a busca. | Pra achar um, é só buscar pelo nome ou pela descrição. |
| Clique em "Filtros": popover com o grupo "Categoria"; marca "Manutenção"; a lista filtra; clique em "Limpar filtros". Abre "Ordenar" ("Nome (A-Z)" e "Nome (Z-A)") e fecha sem trocar. | Em Filtros você vê só uma categoria, e em Ordenar escolhe a ordem de A a Z ou de Z a A. |
| Clique em "Visita Técnica": a ficha mostra "Vinculado a equipamento" desligado. Depois clique em "Manutenção Preventiva": o mesmo interruptor, ligado. | Agora o Vinculado a equipamento. Na Manutenção Preventiva ele está ligado: a ordem de serviço pede o aparelho do cliente, o que é bom pra higienização e manutenção. Já a Visita Técnica está desligada, porque serve pra visita e orçamento, onde ainda não tem aparelho. |
| [ILUSTRAÇÃO: duas colunas sobre o efeito na ordem de serviço, "Ligado: escolhe o aparelho do cliente" e "Desligado: só o serviço"; fundo branco, Montserrat, verde, objetos genéricos. A tela de Nova OS só entra no T5.] | Na hora de abrir a ordem, ligado, a Dominex pede o aparelho do cliente. Desligado, pede só o serviço. |

### cap05 · Dados fiscais (vinheta: SERVIÇOS)

| Tela | Fala |
| --- | --- |
| Clique em "Manutenção Preventiva" na lista; na ficha, clique na pílula "Fiscal" (módulo Nota Fiscal): bloco "Fiscal (NFS-e)" ("Classificação tributária usada ao emitir nota fiscal de serviço. Todos os campos são opcionais."). | Agora os dados fiscais do serviço. Se a sua empresa emite nota fiscal de serviço, esta aba é pra você. A Fiscal aparece pra quem tem o módulo de Nota Fiscal. |
| Clique em "Código de serviço (cTribNac)": abre a busca "Buscar por código ou descrição..."; digita "14.01"; escolhe "14.01.01"; o campo "Item da LC 116" se preenche com 14.01. [BACKEND: `functions/nfse-tax-codes.mjs`, com `{type:'servico'}` devolvendo `{items:[{codigo,descricao,itemLc116}], total}` com ao menos `140101` e `140601` e vizinhos reais da migration `20260903182000`; sem ele a busca mostra "Nenhum código encontrado."] | No Código de serviço, eu busco o código do serviço, catorze ponto zero um ponto zero um, e escolho. O Item da LC cento e dezesseis vem preenchido sozinho. |
| Digita `001` em "Código de tributação municipal (cTribMun)" (só três dígitos). | O código de tributação municipal tem três dígitos, definidos pela prefeitura: zero zero um. É ele que a prefeitura usa pra aceitar a nota. |
| Digita `5` em "Alíquota de ISS (%)"; clique em "Salvar"; toast "Tipo de serviço atualizado!". | E a Alíquota de ISS, que é a do seu município. Aqui, cinco por cento. Salvo. Vale preencher agora: com o código salvo aqui, toda nota emitida com esse serviço já nasce classificada. |

### cap06 · Editar, desativar e excluir (vinheta: SERVIÇOS)

| Tela | Fala |
| --- | --- |
| Pílula "Dados" da ficha de "Manutenção Preventiva": edita "Descrição" para "Limpeza, conferência e teste completos do aparelho" e clica em "Salvar"; toast "Tipo de serviço atualizado!". | Agora o dia a dia do cadastro. Pra mudar qualquer coisa, é só abrir o serviço, editar a ficha aqui do lado e salvar. |
| Zoom no interruptor "Ativo". | Uma dica: pra pausar um serviço sem perder o histórico, é só desligar o Ativo. Ele sai das listas de escolha e continua cadastrado. |
| Clique em "Excluir": janela "Excluir Tipo de Serviço" ("Tem certeza que deseja excluir este tipo de serviço? Esta ação não pode ser desfeita."); clique em "Cancelar". [Não excluir tipo nem categoria: o falso não emula FK] | O Excluir pede confirmação, e remove o cadastro de vez. Aqui eu cancelo. |

### cap07 · Tipos de tarefa (vinheta: TAREFAS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Tipos de Tarefas": lista com "Treinamento da equipe" (já cadastrado) e a "Ficha do tipo de tarefa" à direita. [BACKEND: seed do tipo de tarefa "Treinamento da equipe", `#3B82F6`] | Agora a aba Tipos de Tarefas. Tarefa é um compromisso interno da equipe, diferente da ordem de serviço, que é pro cliente. Os tipos aparecem na Agenda, quando você cria uma nova tarefa, e só os ativos entram na escolha. |
| Clique em "Novo Tipo": modal "Novo Tipo de Tarefa" com "Nome *" ("Ex: Reunião, Entrega, Compra"), "Cor", "Descrição" e "Ativo"; digita "Reunião", cor `#8B5CF6`, descrição "Reunião de equipe"; clique em "Criar"; toast "Tipo de tarefa criado!". | Clico em Novo Tipo, dou o nome, Reunião, escolho a cor e clico em Criar. |
| Repete com "Entrega de material" (`#F97316`) e "Compra de peças" (`#EAB308`); a lista mostra os quatro tipos. | Faço o mesmo com Entrega de material e com Compra de peças. |
| Zoom na "Ficha do tipo de tarefa" de "Compra de peças": cor, descrição, interruptor "Ativo", "Salvar" e "Excluir". | Cada tipo tem a sua ficha, com cor, descrição e o Ativo, igual aos serviços. |

### cap08 · Catálogo de modelos (vinheta: CHECKLISTS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Checklists": cabeçalho "Checklists" ("Modelos de checklist reutilizáveis em OS e PMOC") e estado vazio "Nenhum checklist criado". | Agora os checklists, que são o roteiro que o técnico preenche em cada visita: o que conferir, medir e fotografar. Pra não começar do zero, a Dominex tem modelos prontos. |
| Clique em "Catálogo de Checklists": janela larga; zoom no aviso "Estes são apenas modelos sugeridos." e na lista "Instalação de Split", "Higienização de Split", "Manutenção Preventiva de Split" e "Carga de Gás". | No Catálogo de Checklists ficam os modelos sugeridos pro seu ramo: instalação, higienização, manutenção preventiva e carga de gás. Cada empresa adapta do seu jeito, porque as perguntas ficam totalmente editáveis depois. |
| Clique em "Manutenção Preventiva de Split": a coluna da direita mostra as perguntas, cada uma com o selo do tipo (por exemplo "Número (psi)") e o selo vermelho de obrigatória. | Olha o da manutenção preventiva: já vem com as perguntas prontas, cada uma com o seu jeito de responder, como um número em psi, e com as obrigatórias marcadas. |
| Clique em "Selecionar": passo "Nome do novo checklist"; digita "Manutenção preventiva de split"; clique em "Criar checklist"; toast "13 perguntas importadas!"; o editor abre. [BACKEND: `POST form_templates` e `POST form_questions` em lote, já cobertos] | Clico em Selecionar, dou o nome do meu checklist, Manutenção preventiva de split, e Criar checklist. Pronto: treze perguntas importadas de uma vez. |

### cap09 · Checklist do zero (vinheta: CHECKLISTS)

| Tela | Fala |
| --- | --- |
| Editor aberto (seta "Voltar à prévia", "13 perguntas"); na linha "Serviços habilitados", clique no botão "Todos os serviços"; desmarca "Todos os serviços" e marca só "Manutenção Preventiva"; toast "Serviços vinculados ao checklist!". [TESTAR: ao desmarcar "Todos os serviços" o app seleciona o primeiro serviço da lista; desmarcar esse e marcar "Manutenção Preventiva"] | O checklist já abriu no editor. Em Serviços habilitados eu escolho onde ele vale: tiro o Todos os serviços e marco só a Manutenção Preventiva. Assim ele aparece só nas ordens desse serviço. |
| Clique em "Voltar à prévia"; clique em "Novo checklist": modal "Novo Checklist"; digita "Higienização de split" em "Nome do checklist"; desliga "Todos os serviços"; marca "Higienização de Split"; clique em "Criar"; o editor abre vazio ("Nenhuma pergunta criada"). | Agora um checklist do zero. Clico em Novo checklist, dou o nome, Higienização de split, desligo o Todos os serviços e marco a Higienização de Split. Criar. |
| Zoom na linha "Serviços habilitados" do novo checklist. | Uma dica: se você não marcar nenhum serviço, o checklist vale pra todos. |

### cap10 · As perguntas (vinheta: CHECKLISTS)

| Tela | Fala |
| --- | --- |
| Clique em "Nova Pergunta": modal com os blocos "Escreva a pergunta", "Escolha como responder" e "Defina as regras", e a "Prévia na OS" ("Atualiza enquanto você configura") à direita. | Hora das perguntas. Clico em Nova Pergunta. À esquerda a gente monta a pergunta, e à direita a prévia mostra como o técnico vai ver na ordem de serviço. |
| Digita "Estado da serpentina" em "Pergunta"; em "Orientação para o técnico (opcional)" digita "Observe se há sujeira ou amassados nas aletas."; clique em "Conformidade": a prévia mostra "Conforme", "Não conforme" e "N/A". | Escrevo a pergunta, Estado da serpentina, e uma orientação que só o técnico vê. Uma dica: a pergunta fica curta e direta, e a explicação vai na orientação. Em Escolha como responder, marco Conformidade, e a prévia já mostra as três respostas. |
| A câmera passa pelos oito blocos: "Verdadeiro/Falso", "Conformidade", "Texto", "Número", "Foto", "Vídeo", "Seleção" e "Assinatura". | São oito jeitos de responder: Verdadeiro ou Falso, Conformidade, Texto, Número, Foto, Vídeo, Seleção e Assinatura. |
| Zoom em "Campo obrigatório" (ligado) e em "Frequência" (sem abrir o seletor); clique em "Nova Pergunta" no rodapé; toast "Pergunta adicionada!". | Deixo o Campo obrigatório ligado, e a ordem só avança depois que o técnico responde. A Frequência é pros contratos, e a gente vê no tutorial de Contratos. Nova Pergunta, e ela entra no checklist. |
| Nova Pergunta: digita "Aspecto da água retirada"; marca "Seleção"; em "Opções de resposta" digita "Limpa", "Turva" e "Suja", cada uma com "+"; clique em "Nova Pergunta". | Outra pergunta: Aspecto da água retirada, do tipo Seleção. Escrevo as opções: limpa, turva e suja. |

### cap11 · Combinando respostas (vinheta: CHECKLISTS)

| Tela | Fala |
| --- | --- |
| Nova Pergunta: digita "Filtros lavados?"; mantém "Verdadeiro/Falso" e marca também "Foto": aparece o painel "Modo de resposta múltipla" com "Exclusivo" e "Cumulativo"; clique em "Cumulativo". | Agora uma coisa que deixa a pergunta mais completa: dá pra combinar jeitos de responder. Em Filtros lavados?, deixo Verdadeiro ou Falso e marco Foto também. Aparece o Modo de resposta múltipla: no Exclusivo, o técnico escolhe uma forma só; no Cumulativo, responde as duas. Escolho Cumulativo: ele marca e ainda anexa a foto. |
| Liga "Exigir foto da câmera" ("Bloqueia upload da galeria, exige foto tirada na hora"); a prévia mostra "Tirar foto agora"; clique em "Nova Pergunta". | Ligo o Exigir foto da câmera, e a foto passa a ser tirada na hora, sem usar a galeria. |
| Nova Pergunta: digita "Dreno escoando"; marca "Vídeo" e desmarca "Verdadeiro/Falso"; liga "Exigir gravação na hora"; a prévia mostra "Gravar vídeo agora"; clique em "Nova Pergunta". | No tipo Vídeo, o técnico grava um clipe curto como resposta. Com o Exigir gravação na hora, o clipe é gravado na hora, como a foto. |

### cap12 · Organizar e conferir (vinheta: CHECKLISTS)

| Tela | Fala |
| --- | --- |
| Zoom na lista de perguntas: selos de tipo, "Cumulativo" e "Câmera", e a alça de arrastar; arrasta "Estado da serpentina" para o topo. [TESTAR: `drag` HTML5 reordena as perguntas (só vale com a busca vazia, "Todos os tipos" e "Ordem do checklist"); se falhar, só mostrar a alça] | Com as perguntas criadas, vale organizar e conferir. Na lista, cada pergunta mostra o jeito de responder e os selos Cumulativo e Câmera. Pela alça, dá pra arrastar e deixar na ordem em que o técnico vai executar. |
| Digita "serpentina" em "Pesquisar pergunta, descrição ou tipo..."; abre o filtro "Todos os tipos" e fecha; limpa a busca. | E quando o checklist cresce, a busca e o filtro de tipo ajudam a achar uma pergunta. |
| Clique em "Voltar à prévia" e em "Ver": abre a prévia ("Como este checklist aparece para o técnico na Ordem de Serviço"); responde duas perguntas (marca "Conforme" e escolhe "Limpa"); clique em "Fechar". [TESTAR: alvo do botão "Ver", que não é o ícone de olho da ficha; não anexar arquivo na prévia] | Pra conferir, o botão Ver abre o checklist igualzinho ao que o técnico vê na ordem de serviço. Dá pra responder à vontade, que nada é salvo. |

### cap13 · Vincular e desativar (vinheta: CHECKLISTS)

| Tela | Fala |
| --- | --- |
| Na lista de checklists, zoom nas linhas "Higienização de split" ("6 perguntas · 1 serviço") e "Manutenção preventiva de split" ("13 perguntas · 1 serviço"). [BACKEND: seed `apos-cap12` acrescenta ao checklist de higienização as perguntas "Observações" (Texto) e "Assinatura do cliente" (Assinatura), além das 4 ao vivo] | Pra fechar os checklists, o vínculo e a desativação. Na lista, cada checklist mostra quantas perguntas tem e em quais serviços vale. |
| No editor, zoom no interruptor "Ativo" e na lixeira; clique na lixeira: janela "Desativar checklist?" ("...continuará preservado nas OSs já existentes."); lê o texto; clique em "Cancelar". [TESTAR: a lixeira não tem nome acessível, alvo por ícone ou posição] | Pra aposentar um checklist, é só desativar: ele sai da lista e das ordens novas, e as ordens antigas continuam com o roteiro que usaram. É por isso que o sistema desativa em vez de apagar. Aqui eu cancelo. |

### cap14 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: lista de serviços com as categorias; ficha com os dados fiscais; aba Tipos de Tarefas. | Pronto! Recapitulando: a gente criou as categorias e os tipos de serviço, com cor, prefixo, preço padrão e os dados fiscais. E cadastrou os tipos de tarefa que aparecem na Agenda. |
| Montagem rápida: catálogo de modelos, editor com as perguntas e a prévia do "Ver". | Depois montou os checklists: um a partir do modelo pronto e outro do zero, com perguntas de vários tipos, cada um ligado aos serviços certos. |
| Cartão "Próximo: Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo"; cartela final. | Com os serviços e os roteiros prontos, no próximo tutorial a gente abre ordens de serviço, organiza a agenda das equipes e acompanha tudo no mapa ao vivo. Até lá! |
