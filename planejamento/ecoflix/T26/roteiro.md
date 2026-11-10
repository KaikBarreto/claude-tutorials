# Roteiro T26 · CRM/Kanban

Roteiro pronto para o ensaio gravado e, depois da revisão geral, para a voz (sem etapa de aprovação, como na Domiflix). Coluna
Fala = texto da narração (voz Kaik Barreto), na grafia da legenda, uma linha da tabela = uma linha da fala; a grafia de pronúncia
vai em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da
1.59.154 (`T26/inventario.md`; as regras do banco, do commit de release). Dados da Recicla Vale Metais (`plano.md` → "Mundo"); tudo
fictício.

- **Título:** CRM/Kanban
- **Antes:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Próximo:** fim da trilha (cartão "Fim da trilha")
- **Vinhetas (áreas):** CRM · CRM · FUNIS · ESTÁGIOS · REGRAS · AUTOMAÇÕES · MODELOS · OPORTUNIDADES · KANBAN · OPORTUNIDADES ·
  TAREFAS · FILTROS · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~15 min de vídeo (1.817 palavras de fala, ~11,6 min de voz a 2,6 palavras/s, mais 13 vinhetas, 10
  ilustrações e o tempo das ações; a fonte pede ~16 min)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` nos capítulos 0 a 11; `2026-11-10T17:30:00-03:00` no 12 (o fim do dia, com o funil em
  uso). Desktop, janela 1280×800, tema claro, logado como Rafael Nogueira (MASTER). Cada capítulo abre um navegador novo com a
  semente indicada.
- Marcas: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[ZOOM: ...]` (a frase inteira, nunca em cima de outro zoom),
  `[ILUSTRAÇÃO: ...]` (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`; nunca tela do app), `[TESTAR: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "CRM/Kanban". | (sem fala) |
| [ILUSTRAÇÃO: o problema do pátio: um celular genérico com balões de conversa ("Tenho retalho de chapa toda semana", "Me liga semana que vem", "Qual o preço do cobre?"), sem logo de aplicativo; na palavra "perder", os balões sobem e um deles some no alto] | Oi! Neste tutorial a gente vai organizar os negócios da Recicla Vale Metais num funil, pra nenhuma oportunidade se perder no caminho. |
| (a ilustração continua: o balão "Tenho retalho de chapa toda semana" fica parado, cinza, com um relógio ao lado, na palavra "esfria") | Sabe aquela indústria que avisou que tem sucata toda semana? A conversa fica no WhatsApp, ninguém retorna, e o negócio esfria. |
| (a ilustração continua: cada balão vira um cartão, com três etiquetas que acendem nas palavras "dono", "valor" e "passo") | No CRM, cada contato vira um cartão, com dono, valor e o próximo passo. |
| Dashboard da Recicla Vale Metais, logado como Rafael Nogueira (semente `inicio`). [ZOOM: o item "CRM/Kanban" no menu lateral], sem clicar. | Ele fica no menu lateral, em CRM/Kanban. |
| Cartão discreto: "Módulo CRM/Kanban". | O CRM/Kanban depende do plano contratado. |
| Cartão discreto: "Antes: Clientes, fornecedores e a ficha do parceiro". | Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. [pause] Vamos abrir o CRM. |

### cap01 · O funil de vendas (vinheta: CRM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`, empresa sem nenhum funil): clique em "CRM/Kanban"; o carregamento gira e abre "CRM/Kanban" · "Gerencie oportunidades e acompanhe seu processo comercial.", com o "Funil de vendas" na barra. [BACKEND: RPC `ensure_company_crm_default_pipeline` cria "Funil de vendas" (padrão, #22c55e) com "Novo", "Em contato", "Proposta", "Ganho" (`is_won`) e "Perdido" (`is_lost`); vira `apos-cap01`] | Na primeira vez que alguém abre o CRM, ele monta sozinho um funil, o Funil de vendas. |
| A câmera percorre os cabeçalhos das colunas, da esquerda para a direita: "Novo", "Em contato", "Proposta", "Ganho", "Perdido", cada um com "0" e "R$ 0,00". | São cinco colunas: Novo, Em contato, Proposta, Ganho e Perdido. |
| [ILUSTRAÇÃO: o funil de vendas: um funil largo em cima e estreito embaixo; na palavra "contatos", muitos cartões entram em cima ("Novo"); descem menos para "Em contato" e "Proposta"; na palavra "fecha", alguns saem embaixo em "Ganho"; na palavra "Perdido", um cartão escorrega pelo lado] | Funil é isso: entram muitos contatos em cima, alguns viram proposta, e uma parte fecha. O resto fica pelo caminho, no Perdido. |
| (a ilustração continua: o funil deita e vira cinco colunas, da esquerda para a direita, com os mesmos nomes; na palavra "anda", um cartão passa de uma coluna para a seguinte) | No sistema, o funil fica deitado. Cada etapa é uma coluna, e o cartão anda pra direita conforme o negócio avança. |
| De volta à tela: [ZOOM: o botão tracejado "Nova oportunidade" da coluna "Novo"] | Cada contato entra no funil por aqui, em Nova oportunidade. A gente cria uma daqui a pouco. |

### cap02 · Funil, Tarefas e os cartões (vinheta: CRM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap01`): `/crm`. [ZOOM: as abas "Funil" e "Tarefas"] | Lá em cima ficam as duas abas: Funil, que é esse quadro, e Tarefas, com as tarefas de cada oportunidade. |
| [ZOOM: os quatro cartões "Total de oportunidades" "0", "Valor total" "R$ 0,00", "Ganhos" "R$ 0,00" e "Em negociação" "R$ 0,00"] | E os quatro cartões: Total de oportunidades, Valor total, Ganhos e Em negociação. Por enquanto, tudo zerado. |
| [ILUSTRAÇÃO: o que cada cartão soma: um quadro com cartões coloridos nas colunas; na palavra "todos", acendem todos os cartões (Total e Valor total); na palavra "Ganho", só os da coluna "Ganho"; na palavra "negociação", só os das colunas do meio, sem "Ganho" e "Perdido"] | O Total e o Valor total contam todos os cartões do funil. Ganhos soma só o que está na coluna Ganho. E Em negociação, o que ainda não ganhou nem perdeu. |
| A câmera desce pela busca ("Buscar por título, contato, empresa, material, telefone ou e-mail..."), "Filtros", "Nova oportunidade" e a barra dos funis ("Funil de vendas", a engrenagem e o "+"). | Embaixo ficam a busca, os filtros e o botão Nova oportunidade. E nessa barra, os funis da empresa. |
| Plano geral da tela. | Uma dica: quem tem acesso à tela do CRM pode criar, editar, excluir e configurar tudo. Então libera a tela só pra quem vai cuidar do funil. |

### cap03 · Funis e estágios (vinheta: FUNIS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap01`): clique em "Configurações do CRM/Kanban": janela "Configurações do CRM/Kanban", menu "Funis", "Checklists" e "Etiquetas"; em "Funis", a linha "Funil de vendas" com o selo "Padrão" e "5 etapas · 0 oportunidades". | Agora, as configurações. Em Configurações do CRM/Kanban, na parte Funis, está o Funil de vendas, marcado como Padrão. |
| Clique em "Novo funil": janela "Novo funil" ("Defina o nome e a cor usada na navegação do CRM."); em "Nome *" digita "Sucata industrial"; em "Cor *" escolhe o azul `#0ea5e9`; clique em "Salvar": toast "Funil criado". [BACKEND: insert em `crm_pipelines` e as cinco etapas em `crm_stages`, "Ganho" e "Perdido" com status] [TESTAR: o campo de cor aceita o valor digitado pelo robô] | A Recicla Vale quer um funil só pras indústrias que geram sucata. Novo funil, o nome é Sucata industrial, e uma cor. Salvar. |
| A linha "Sucata industrial", "5 etapas · 0 oportunidades"; clique em "Tornar padrão": toast "Funil padrão atualizado"; o selo "Padrão" passa para ela. | Ele já nasce com as mesmas cinco etapas. Clico em Tornar padrão, e ele passa a abrir primeiro no CRM. |
| Arrasta a linha "Sucata industrial" para cima de "Funil de vendas"; a ordem troca. [TESTAR: arrastar e soltar nativo do navegador nas linhas] | Arrastando a linha, eu mudo a ordem dos funis na barra. O Sucata industrial vai pra frente. |
| Clique na linha "Sucata industrial": abre "Estágios deste funil" com "Novo", "Em contato", "Proposta", "Ganho" (selo "Ganho") e "Perdido" (selo "Perdido"); clique em "Novo estágio": janela "Novo estágio" ("Crie a coluna primeiro; regras e automações ficam disponíveis na edição."); em "Nome *" digita "Visita técnica"; clique em "Salvar etapa": toast "Estágio criado. Edite novamente para configurar regras e automações.". | Abrindo o funil, aparecem os estágios. Entre o contato e a proposta, a Recicla Vale sempre visita a indústria. Então, Novo estágio: Visita técnica. Salvar etapa. |
| "Visita técnica" aparece no fim da lista, depois de "Perdido"; arrasta a linha para entre "Em contato" e "Proposta". | O estágio novo entra no fim. Eu arrasto ele pra depois de Em contato. |
| [ILUSTRAÇÃO: quem é negociação: as seis colunas do funil; na palavra "negociação", "Novo", "Em contato", "Visita técnica" e "Proposta" ganham juntas a faixa "negociação"; na palavra "Ganho", só a coluna "Ganho" ganha um troféu e a "Perdido" um X] | Uma dica: estágio criado em Novo estágio é sempre de negociação. Só o Ganho e o Perdido que nascem com o funil contam como ganho e como perda nos cartões lá de cima. |

### cap04 · Nome, cor e orientação (vinheta: ESTÁGIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`): "Configurações do CRM/Kanban" › "Funis" › "Sucata industrial" aberto; clique no lápis "Editar estágio Visita técnica": janela "Configurar Visita técnica" ("Defina a coluna, os critérios de saída e o que acontece automaticamente."), abas "Coluna", "Regras" e "Automações". | Pra editar um estágio, é o lápis. Abre a configuração da Visita técnica, com três abas: Coluna, Regras e Automações. |
| Na aba "Coluna": "Nome *" "Visita técnica"; em "Cor *" troca o cinza do estágio novo pelo verde-azulado `#0d9488`. | Em Coluna ficam o nome e a cor. A cor veio cinza, e eu escolho uma diferente das outras, pra coluna destacar no quadro. |
| Em "Orientação para o time" ("O que precisa acontecer enquanto o cartão estiver aqui?") digita "Visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada.". | E em Orientação para o time, o combinado da etapa: visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada. |
| Clique em "Salvar etapa": toast "Configuração da etapa salva". [BACKEND: update em `crm_stages` (`color`, `description`); vira `apos-cap04`] | Salvar etapa. Esse texto fica aqui, na configuração da etapa, como referência pro time. |
| [ZOOM: a lixeira "Excluir estágio Visita técnica" na lista], sem clicar. | Uma dica: pra excluir um estágio, ele precisa estar vazio. Se tiver cartão nele, move os cartões pra outra coluna antes. |

### cap05 · Regras do estágio (vinheta: REGRAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`): na lista de "Sucata industrial", lápis "Editar estágio Em contato": "Configurar Em contato"; clique na aba "Regras": "Antes de sair desta etapa" · "O banco bloqueia avanço por arraste, edição ou integração enquanto houver pendências.". | Agora, as regras. Elas dizem o que precisa estar pronto antes de o cartão sair da etapa. Vou abrir o Em contato, na aba Regras. |
| [ILUSTRAÇÃO: a regra é a porta de saída: a coluna "Em contato" com uma porta à direita; na porta, a lista "tarefas encerradas" e "responsável"; na palavra "passa", um cartão chega e a porta só abre quando os dois itens ganham um visto] | Pensa numa porta na saída da coluna. O cartão só passa quando o que está na lista estiver feito. |
| A câmera percorre as seis chaves: "Tarefas", "Checklists", "Responsável", "Prazo", "Empresa" e "Observações", com as frases de cada uma. | Dá pra exigir as tarefas encerradas, os checklists marcados, um responsável, a previsão de fechamento, a empresa e as observações do cartão. |
| Liga "Tarefas" ("Todas as tarefas do cartão precisam estar encerradas.") e "Responsável" ("O cartão precisa ter uma pessoa responsável."). | No Em contato, eu ligo duas: Tarefas e Responsável. Assim, o cartão só vai pra visita com dono e com as tarefas feitas. |
| [ZOOM: "Tarefas obrigatórias por nome" e "Checklists obrigatórios por nome", com os exemplos "Ex.: Enviar proposta" e "Ex.: Documentação"] | Também dá pra exigir uma tarefa ou um checklist pelo nome. Uma dica: o nome tem que ser igualzinho, letra por letra. Um acento ou um espaço a mais, e a regra não reconhece. |
| Clique em "Salvar etapa": toast "Configuração da etapa salva". [BACKEND: `crm_stages.requirements` = `{tasks: true, assignee: true, taskNames: [], checklistNames: []}`; vira `apos-cap05`] | Salvar etapa. |

### cap06 · Automações (vinheta: AUTOMAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`): "Configurar Em contato" aberto (o `setup` abre fora do vídeo); clique na aba "Automações": "Fluxos desta etapa" · "Novas automações nascem pausadas para revisão." e "Nenhuma automação nesta etapa". | E as automações. Elas fazem sozinhas o trabalho repetido, quando alguma coisa acontece no cartão. |
| [ILUSTRAÇÃO: automação é gatilho e ações: à esquerda, o gatilho (um cartão entrando numa coluna); na palavra "ações", uma fileira de peças de dominó cai, uma por vez: "criar tarefa", "atribuir responsável", "definir prazo"] | É sempre assim: um gatilho e as ações. Quando o gatilho acontece, o sistema faz as ações, na ordem. |
| Clique em "Nova automação": "Nova automação" · "Use {NOME} e {CLIENTE} nos textos dinâmicos."; em "Nome *" digita "Agendar a visita"; abre "Gatilho": "Ao entrar nesta etapa", "Ao concluir uma tarefa", "Ao concluir um checklist", "Quando tudo estiver concluído"; fica em "Ao entrar nesta etapa". | Nova automação. O nome é Agendar a visita. No gatilho, dá pra escolher quando o cartão entra na etapa, quando uma tarefa ou um checklist é concluído, ou quando tudo estiver concluído. Fico com Ao entrar nesta etapa. |
| Abre o seletor da ação 1: "Criar tarefa", "Aplicar checklist", "Definir prazo do cartão", "Atribuir responsável", "Adicionar etiqueta", "Mover cartão", "Copiar cartão"; fica em "Criar tarefa". | As ações são estas: Criar tarefa, Aplicar checklist, Definir prazo do cartão, Atribuir responsável, Adicionar etiqueta, Mover cartão e Copiar cartão. Aqui vai uma só: Criar tarefa. |
| Em "Título da tarefa *" troca "Acompanhar {NOME}" por "Agendar visita na {CLIENTE}". [ZOOM: o título e a frase "Use {NOME} e {CLIENTE} nos textos dinâmicos."] | No título da tarefa, eu escrevo Agendar visita na, e o marcador CLIENTE, entre chaves. Ele vira o nome da empresa do cartão. |
| "Prazo em dias" em "1"; em "Contagem" escolhe "Dias úteis". | O prazo é de um dia útil. |
| A câmera abre para a ação inteira: "Título da tarefa *", "Prazo em dias" e "Contagem". | A tarefa da automação fica com o responsável do cartão. Pra escolher quem é, existe a ação Atribuir responsável. |
| [ZOOM: a chave em "Pausada"] | Uma dica: toda automação nova nasce pausada. Se ficar assim, ela não roda. Então eu ligo pra Ativa. |
| Liga a chave ("Ativa"); clique em "Salvar automação": toast "Automação salva e ativa"; na lista, "Agendar a visita", selo "Ativa", "Ao entrar nesta etapa · 1 ação". [BACKEND: insert em `crm_automation_rules` com `enabled` true; vira `apos-cap06`] | Salvar automação, e ela aparece ativa na lista. |
| [ILUSTRAÇÃO: ao entrar, só avançando: as colunas "Novo", "Em contato" e "Visita técnica"; na palavra "avança", um cartão vai de "Novo" para "Em contato" e um raio acende; na palavra "voltando", outro cartão volta de "Visita técnica" para "Em contato" e nada acende] | Uma dica: Ao entrar nesta etapa só roda quando o cartão avança pra ela, muda de funil ou já nasce nela. Voltando de uma coluna da frente, ela não roda. |

### cap07 · Checklists e etiquetas (vinheta: MODELOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`): "Configurações do CRM/Kanban" › "Checklists": "Modelos reutilizáveis de checklist pra aplicar em oportunidades." e o aviso "O modelo é só o ponto de partida…". | Agora, os modelos. Em Checklists ficam as listas prontas que a gente aplica nos cartões. |
| Clique em "Nova checklist"; "Nome *" "Documentos do fornecedor"; "Adicionar item" três vezes: "CNPJ conferido", "Local de retirada combinado", "Frequência da coleta combinada"; clique em "Salvar": toast "Checklist criada". | Nova checklist: Documentos do fornecedor, com três itens: CNPJ conferido, local de retirada combinado e frequência da coleta combinada. Salvar. |
| [ILUSTRAÇÃO: modelo e cópia: um carimbo "Documentos do fornecedor" carimba a lista em dois cartões; na palavra "depois", o carimbo ganha um item novo e as cópias já carimbadas continuam como estavam] | O modelo é o ponto de partida. Aplicado num cartão, ele vira uma cópia. Mudar o modelo depois não mexe no que já foi aplicado. |
| Clique em "Etiquetas" ("Etiquetas ajudam a classificar oportunidades no Kanban."); "Nova etiqueta"; "Nome *" "Indústria"; "Cor *" `#6366f1`; "Salvar": toast "Etiqueta criada". [BACKEND: inserts em `crm_checklist_templates` e `crm_labels`; vira `apos-cap07`] | Em Etiquetas, a mesma ideia. Nova etiqueta, Indústria, com uma cor. Salvar. |
| A câmera fica na lista das etiquetas. | São esses modelos que as regras e as automações usam: as ações Aplicar checklist e Adicionar etiqueta, e o checklist exigido pelo nome. |
| Plano geral da janela. | Uma dica: o modelo, a etiqueta e a pessoa que uma automação usa precisam continuar existindo. Se a ação não acha o que precisa, a automação falha e desfaz tudo: o cartão não muda de coluna, nem é criado. |

### cap08 · Nova oportunidade (vinheta: OPORTUNIDADES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`): `/crm` abre no funil padrão, "Sucata industrial", com "Novo", "Em contato", "Visita técnica" (verde-azulado), "Proposta", "Ganho" e "Perdido". | Com o funil pronto, o quadro já abre no Sucata industrial, com a Visita técnica no lugar certo. |
| Clique em "Nova oportunidade": "Nova oportunidade" · "Os dados ficam disponíveis apenas para a sua empresa."; em "Título *" digita "Retalho de chapa da Metalúrgica Jequitibá"; "Etapa *" já em "Novo". | A Metalúrgica Jequitibá ligou: gera retalho de chapa toda semana. Nova oportunidade. No título, Retalho de chapa da Metalúrgica Jequitibá. A etapa já vem em Novo. Esses dois são os obrigatórios. |
| Em "Valor" digita "8400". [ZOOM: "Valor" com o número] | O valor estimado: oito mil e quatrocentos reais por mês. |
| "Responsável" fica em "Sem responsável". | O responsável fica em branco por enquanto. |
| Em "Empresa" clica, digita "Metalúrgica Jequitibá" e escolhe 'Usar "Metalúrgica Jequitibá" como empresa avulsa'; em "Contato" digita "Paulo Lacerda"; em "Área/Setor", "Suprimentos"; em "E-mail", "paulo.lacerda@metalurgicajequitiba.example" (o "Telefone" fica vazio). | Em Empresa, dá pra escolher um cliente ou fornecedor do cadastro. Ela ainda não é cadastrada, então eu uso o nome como empresa avulsa. O contato é o Paulo Lacerda, de suprimentos. |
| Em "Tipo de material" escolhe "Chaparia"; em "Quantidade estimada" digita "12000" (unidade "Kg"); em "Meio de transporte" escolhe "Frota própria". [ZOOM: "Quantidade estimada" com o número e "Kg"] | Na operação, o material é chaparia, uns doze mil quilos por mês, e a retirada é com a frota própria. |
| Em "Previsão de fechamento" escolhe 30/11/2026; em "Observações" digita "Quer retirada a cada quinze dias, com caçamba.". | A previsão de fechamento é trinta de novembro. E nas observações, o que ela pediu: retirada a cada quinze dias, com caçamba. |
| Clique em "Salvar": toast "Oportunidade criada"; o cartão aparece em "Novo" com o título, "Paulo Lacerda", "Metalúrgica Jequitibá", o material com a quantidade, "R$ 8.400,00" e "30/11/2026". [BACKEND: insert em `crm_opportunities`; com o gatilho de criação, nenhuma automação no "Novo"; vira `apos-cap08`] | Salvar, e o cartão aparece no Novo, com o material, o valor e a previsão. |
| A câmera fica no cartão. | Quando o negócio fechar, a compra você lança no caixa, como sempre. O cartão guarda a história da negociação. |

### cap09 · Arrastar o cartão (vinheta: KANBAN)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`): o robô pega o cartão pela alça "Mover oportunidade" e solta em "Em contato"; o cartão fica lá, e o número da coluna muda. [BACKEND: update de `stage_id` (a trava olha o "Novo", sem regra) e RPC `reorder_company_crm_opportunities`; a automação "Agendar a visita" cria em `schedule_tasks` a tarefa "Agendar visita na Metalúrgica Jequitibá" (sem responsável, 11/11); a linha 'Etapa alterada de "Novo" para "Em contato".' no histórico] [TESTAR: arrasto pela alça, com o sensor que pede 6 px de movimento] | Agora, andar com o cartão. O Paulo atendeu, então eu arrasto o cartão pela alça até Em contato. |
| [ZOOM: o selo de tarefas abertas "1" no cartão] [TESTAR: o selo aparece sem recarregar] | Repara: a automação já criou a tarefa de agendar a visita. O cartão mostra uma tarefa aberta. |
| Arrasta o cartão de "Em contato" para "Visita técnica": toast de erro "Conclua as tarefas pendentes. Defina um responsável.". [ZOOM: o aviso] [BACKEND: a trava do "Em contato" devolve o erro P0001 com as duas pendências numa frase] | E se eu tentar levar pra Visita técnica agora? O sistema trava e mostra o que falta: Conclua as tarefas pendentes. Defina um responsável. |
| Corte: a tela recarregada mostra o cartão em "Em contato". [TESTAR: no erro, o quadro deixa o cartão desenhado no destino até buscar de novo (inventário, seção 1): o robô recarrega fora do vídeo e a tomada volta já no quadro certo] | O cartão continua em Em contato, esperando. |
| [ILUSTRAÇÃO: a regra é da porta de saída: o cartão em "Em contato", com três setas: para a frente ("Visita técnica"), para trás ("Novo") e para "Perdido"; na palavra "qualquer", as três setas batem na mesma porta com a lista] | Uma dica: quem manda é a regra da etapa de onde o cartão sai. E ela vale pra qualquer troca: avançar, voltar uma coluna ou mandar pro Perdido. |
| A câmera no cartão. | Pra destravar, é só resolver o que falta, na ficha do cartão. |

### cap10 · A ficha da oportunidade (vinheta: OPORTUNIDADES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`): clique no título do cartão: abre a ficha "Retalho de chapa da Metalúrgica Jequitibá", com "Editar", as abas "Detalhes", "Tarefas (1)" e "Histórico" (com a contagem), e os comentários à direita. | Clicando no cartão, abre a ficha da oportunidade, com três abas: Detalhes, Tarefas e Histórico. |
| Em "Detalhes": "Funil" "Sucata industrial", "Estágio" "Em contato"; em "Responsável" troca "Sem responsável" por "Rafael Nogueira". [BACKEND: update de `assigned_to`] | Em Detalhes ficam o funil, o estágio e o responsável. Eu escolho o Rafael, o dono do ferro-velho, que vai cuidar dessa negociação. |
| A câmera desce por "Valor Estimado", "Previsão Fechamento", "Negociação" ("Material", "Quantidade estimada", "Transporte", "Empresa") e "Observações". | Embaixo, o valor, a previsão, o material e a empresa. E as observações, que salvam sozinhas. É ali também que vai o motivo, se um negócio for pro Perdido. |
| Em "Etiquetas", clique em "Gerenciar" e marca "Indústria": a etiqueta aparece; o mouse passa por "Aplicar modelo", em "Checklists", sem clicar. | Em Etiquetas, eu aplico a Indústria, que a gente criou nos modelos. E em Checklists, o Aplicar modelo coloca a lista no cartão. |
| Clique em "Tarefas (1)": "Agendar visita na Metalúrgica Jequitibá", com a data 11/11; clique em "Concluir tarefa": a tarefa fica concluída. [BACKEND: update de `schedule_tasks.status` para `concluida`] | Na aba Tarefas está a tarefa que a automação criou: Agendar visita na Metalúrgica Jequitibá. A visita já foi marcada, então eu concluo. |
| Clique em "Histórico": 'Etapa alterada de "Novo" para "Em contato".', com o autor e o tempo. [TESTAR: a linha sem texto que a automação grava (inventário, seção 5); a câmera fica na linha da troca de etapa] | E o Histórico guarda cada mudança de etapa, com quem fez e quando. |
| Fecha a ficha; arrasta o cartão de "Em contato" para "Visita técnica": ele fica lá. [BACKEND: a trava do "Em contato" passa (responsável e tarefa encerrada); vira `apos-cap10`] | Fechando a ficha, agora sim: o cartão passa pra Visita técnica. |

### cap11 · Tarefas e Agenda (vinheta: TAREFAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`): clique na aba "Tarefas": "Tarefas" · "Tarefas vinculadas às oportunidades do funil", na visão "Kanban": colunas "Pendente", "Em andamento", "Concluída" e "Cancelada", com "Agendar visita na Metalúrgica Jequitibá" em "Concluída". | Agora, a aba Tarefas. Ela junta as tarefas de todas as oportunidades. No Kanban, cada coluna é uma situação: pendente, em andamento, concluída e cancelada. |
| Clique em "Nova tarefa": "Título *" "Enviar proposta"; "Oportunidade *" "Retalho de chapa da Metalúrgica Jequitibá"; "Responsável" "Rafael Nogueira"; "Data *" 12/11/2026; "Prioridade" "Alta"; clique em "Salvar": toast "Tarefa criada". [BACKEND: insert em `schedule_tasks` com `crm_opportunity_id` e categoria "crm"; vira `apos-cap11`] | Depois da visita, vem a proposta. Nova tarefa: Enviar proposta, ligada à oportunidade da Jequitibá, com o Rafael, pra quinta, dia doze, prioridade alta. Salvar. |
| A tarefa nova em "Pendente"; clique em "Lista": "Título", "Oportunidade", "Responsável", "Data", "Prioridade" e "Status". | Ela entra em Pendente. Na Lista, as mesmas tarefas viram uma tabela, com a oportunidade, o responsável, a data e a prioridade. |
| Clique em "Calendário": "Mês", "novembro de 2026", com as tarefas nos dias 11 e 12. | E no Calendário, cada tarefa no seu dia. |
| Menu lateral "Agenda": no dia 12/11, "Enviar proposta" com o selo "CRM". [TESTAR: a visão da Agenda que mostra o dia 12 sem rolar] | E a mesma tarefa aparece na Agenda, com o selo CRM. Assim, ela entra na rotina do dia. |
| [ILUSTRAÇÃO: uma tarefa, dois lugares: um cartão de tarefa "Enviar proposta" no meio; na palavra "CRM", ele aparece na aba Tarefas; na palavra "Agenda", a mesma tarefa aparece no dia 12 de um calendário genérico, ligada por uma linha] | É uma tarefa só, nos dois lugares. Concluiu num, aparece concluída no outro. |
| Clique em "Enviar proposta" na Agenda: abre `/crm` com "Editar oportunidade" da Jequitibá; clique em "Cancelar". | Clicando nela, a Agenda leva direto pra oportunidade no CRM. Uma dica: na Agenda dá pra concluir a tarefa; pra editar ou excluir, é na aba Tarefas do CRM. |

### cap12 · Filtros e busca (vinheta: FILTROS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap11-dia`, FAKE_NOW 17:30, com as cinco oportunidades do dia): o quadro do "Sucata industrial" com seis cartões; [ZOOM: "Total de oportunidades" "6" e "Valor total" "R$ 62.300,00"] | Com o funil em uso, entram mais cartões. No fim do dia, a Recicla Vale já tem seis oportunidades no funil: sessenta e dois mil e trezentos reais no total. |
| [ZOOM: "Ganhos" "R$ 19.000,00" e "Em negociação" "R$ 41.650,00"] | Já são dezenove mil reais ganhos, com a Construtora Pilar, e quarenta e um mil seiscentos e cinquenta reais em negociação. |
| Na busca, digita "alumínio": fica só "Perfis de alumínio da Esquadrias Horizonte"; os cartões do topo passam a "(filtrado)". | Na busca, dá pra achar pelo título, pelo contato, pela empresa ou pelo material. Digitando alumínio, sobra o cartão da Esquadrias Horizonte. E os cartões de cima passam a dizer filtrado. |
| Apaga a busca; clique em "Filtros": "Filtrar oportunidades" · "Refine os cards exibidos neste funil.", com "Status", "Valor mínimo", "Valor máximo", "Responsável", "Material" e "Meio de transporte". | Nos Filtros, dá pra separar por situação, por faixa de valor, por responsável, por material e por meio de transporte. |
| Em "Status" escolhe "Em negociação"; em "Responsável", "Rafael Nogueira"; clique em "Aplicar": ficam a Jequitibá e a Esquadrias Horizonte; o botão "Filtros" mostra "2"; [ZOOM: "Valor total (filtrado)" "R$ 26.200,00"] | Quero ver o que está com o Rafael e ainda em negociação. Aplicar, e ficam dois cartões: vinte e seis mil e duzentos reais. |
| Clique em "Filtros" › "Limpar filtros" › "Aplicar": voltam os seis. | Pra ver tudo de novo, é Limpar filtros. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem: a primeira abertura com o "Funil de vendas", as abas e os quatro cartões. | Pronto! Recapitulando: o CRM montou sozinho o Funil de vendas, e a gente conheceu as abas e os quatro cartões. |
| (a montagem continua: "Funil criado", "Tornar padrão", a "Visita técnica" arrastada, "Orientação para o time") | Criou o funil Sucata industrial, tornou padrão, pôs a Visita técnica no lugar e deu cor e orientação pra ela. |
| (a montagem continua: as chaves "Tarefas" e "Responsável", "Automação salva e ativa", "Checklist criada", "Etiqueta criada") | Ligou as regras de saída do Em contato e criou e ativou a automação que agenda a visita, além do checklist e da etiqueta. |
| (a montagem continua: o cartão da Jequitibá, o aviso da trava, a ficha, a tarefa concluída, a Agenda e os filtros) | Cadastrou a oportunidade da Metalúrgica Jequitibá, viu a trava, resolveu na ficha e moveu o cartão. A tarefa apareceu na aba Tarefas e na Agenda, e os filtros separaram o funil. |
| Cartão discreto: "Fim da trilha". | Essa foi a última aula da trilha. Sempre que precisar, volta em qualquer aula pelo capítulo que quiser rever. Até lá! |
