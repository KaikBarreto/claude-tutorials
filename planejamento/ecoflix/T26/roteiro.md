# Roteiro T26 · CRM/Kanban

Roteiro para a voz e a gravação no app 1.60.22 (aplicação de 21/11), tela 1600x900. A coluna Fala é a de `narracao/tts_textos.py`, na grafia da legenda
(CRM, CRM/Kanban; a pronúncia fica no tts); uma linha da tabela = uma linha da fala. A coluna Tela é o que o robô faz naquela linha (os rótulos entre aspas
são os do código do 1.60.22, conferidos no ensaio; `rec/t26/gerar.py` é a fonte). Dados da Recicla Vale Metais (`plano.md` → "Mundo"); tudo fictício.

- **Título:** CRM/Kanban
- **Antes:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Próximo:** fim da trilha (cartão "Fim da trilha")
- **Capítulos:** 17 (0 a 16). Novos em 21/11: 8 (automação com várias ações), 12 (checklist na oportunidade), 13 (probabilidade, origem e tarefas). Renumerados: Nova oportunidade 8→9, Arrastar o cartão 9→10, A ficha 10→11, Tarefas e Agenda 11→14, Filtros 12→15 (agora também com Perdidos, a ordem na coluna e arrastar para Ganho), Recapitulando 13→16.
- **Vinhetas (áreas):** CRM · CRM · FUNIS · ESTÁGIOS · REGRAS · AUTOMAÇÕES · MODELOS · AUTOMAÇÕES · OPORTUNIDADES · KANBAN · OPORTUNIDADES · OPORTUNIDADES · OPORTUNIDADES · TAREFAS · FILTROS · RESUMO (todos os capítulos menos o 0)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` nos capítulos 0 a 14; `2026-11-10T17:30:00-03:00` nos 15 e 16 (o fim do dia, com seis oportunidades). Desktop, tema claro, logado como Rafael Nogueira (MASTER). Cada capítulo abre um navegador novo com a semente indicada (`rec/t26/gerar.py` → SEMENTE).
- **Fala:** 2.943 palavras (antes 1.817). Sem travessão; número por extenso; valores calculados só depois de vistos na tela no ensaio (R$ 23.650,00, R$ 37.000,00 e 25/11 foram vistos na tela no ensaio).
- Marcas: `[ILUSTRAÇÃO: ...]` desenho por código no estilo da marca, nunca tela inventada (ver `cenas/ilustracoes.json`).


### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| (segue a tela da linha anterior) [ILUSTRAÇÃO: a conversa do celular se perde e esfria; no CRM cada contato vira um cartão, com dono, valor e próximo passo] | Oi! Neste tutorial a gente vai organizar os negócios da Recicla Vale Metais num funil, pra nenhuma oportunidade se perder no caminho. |
| (segue a tela da linha anterior) | Sabe aquela indústria que avisou que tem sucata toda semana? A conversa fica no WhatsApp, ninguém retorna, e o negócio esfria. |
| (segue a tela da linha anterior) | No CRM, cada contato vira um cartão, com dono, valor e o próximo passo. |
| item CRM/Kanban do menu lateral (zoom, sem clicar) | Ele fica no menu lateral, em CRM/Kanban. |
| CRM/Kanban (módulo do plano) | O CRM/Kanban depende do plano contratado. |
| (segue a tela da linha anterior) | Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. Vamos abrir o CRM. |

### cap01 · O funil de vendas (vinheta: CRM)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "O funil de vendas". | (sem fala) |
| CRM/Kanban (menu lateral) › Funil de vendas (barra dos funis) | Na primeira vez que alguém abre o CRM, ele monta sozinho um funil, o Funil de vendas. |
| coluna Novo › coluna Em contato › coluna Proposta › o quadro rola para a direita (Ganho e Perdido) › coluna Perdido | São cinco colunas: Novo, Em contato, Proposta, Ganho e Perdido. |
| o quadro volta ao começo (sob a ilustração) [ILUSTRAÇÃO: o funil: muitos entram, alguns viram proposta, uma parte fecha e o resto vai pro Perdido; deitado, vira as colunas] | Funil é isso: entram muitos contatos em cima, alguns viram proposta, e uma parte fecha. O resto fica pelo caminho, no Perdido. |
| (segue a tela da linha anterior) | No sistema, o funil fica deitado. Cada etapa é uma coluna, e o cartão anda pra direita conforme o negócio avança. |
| botão tracejado Nova oportunidade da coluna Novo (zoom) | Cada contato entra no funil por aqui, em Nova oportunidade. A gente cria uma daqui a pouco. |

### cap02 · Funil, Tarefas e os cartões (vinheta: CRM)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Funil, Tarefas e os cartões". | (sem fala) |
| aba Funil (zoom nas abas) › aba Tarefas | Lá em cima ficam as duas abas: Funil, que é esse quadro, e Tarefas, com as tarefas de cada oportunidade. |
| os quatro cartões (zoom) › Total de oportunidades 0 › Valor total R$ 0,00 › Ganhos R$ 0,00 › Em negociação R$ 0,00 | E os quatro cartões: Total de oportunidades, Valor total, Ganhos e Em negociação. Por enquanto, tudo zerado. |
| (segue a tela da linha anterior) [ILUSTRAÇÃO: Total e Valor total somam tudo; Ganhos, só a coluna Ganho; Em negociação, o que não ganhou nem perdeu] | O Total e o Valor total contam todos os cartões do funil. Ganhos soma só o que está na coluna Ganho. E Em negociação, o que ainda não ganhou nem perdeu. |
| busca › Filtros › Nova oportunidade › barra dos funis: Funil de vendas › engrenagem Configurar estágios › + Criar funil | Embaixo ficam a busca, os filtros e o botão Nova oportunidade. E nessa barra, os funis da empresa. A engrenagem abre as configurações, e o mais cria um funil novo. |
| (segue a tela da linha anterior) | Uma dica: quem tem acesso à tela do CRM pode criar, editar, excluir e configurar tudo. Então libera a tela só pra quem vai cuidar do funil. |

### cap03 · Funis e estágios (vinheta: FUNIS)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Funis e estágios". | (sem fala) |
| Configurações do CRM/Kanban › menu Funis › linha Funil de vendas › selo Padrão | Agora, as configurações. Em Configurações do CRM/Kanban, na parte Funis, está o Funil de vendas, marcado como Padrão. |
| Novo funil › Nome: Sucata industrial › Cor (o seletor de cor) › Cor: azul #0ea5e9 › Salvar (Novo funil) | A Recicla Vale quer um funil só pras indústrias que geram sucata. Novo funil, o nome é Sucata industrial, e uma cor. Salvar. |
| Sucata industrial: 5 etapas › Tornar padrão › selo Padrão no Sucata industrial | Ele já nasce com as mesmas cinco etapas. Clico em Tornar padrão, e ele passa a abrir primeiro no CRM. |
| arrasta a linha Sucata industrial para cima do Funil de vendas › Sucata industrial vai pra frente | Arrastando a linha, eu mudo a ordem dos funis na barra. O Sucata industrial vai pra frente. |
| lápis Editar funil (zoom) › lixeira Excluir funil (abre a confirmação) › confirmação: Excluir este funil? (zoom) › Cancelar (o funil fica) | No lápis, dá pra trocar o nome e a cor de um funil. E na lixeira, excluir. Uma dica: excluir o funil apaga todas as oportunidades dele, e não tem volta. |
| abre o funil Sucata industrial › Estágios deste funil › estágio Em contato › estágio Proposta › Novo estágio › foco no Nome (a janela abre com o foco nas abas) › Nome: Visita técnica › ... | Abrindo o funil, aparecem os estágios. Entre o contato e a proposta, a Recicla Vale sempre visita a indústria. Então, Novo estágio: Visita técnica. Salvar etapa. |
| Visita técnica entra no fim da lista › arrasta Visita técnica para depois de Em contato | O estágio novo entra no fim. Eu arrasto ele pra depois de Em contato. |
| selo Ganho › selo Perdido [ILUSTRAÇÃO: estágio criado em Novo estágio é de negociação; só o Ganho e o Perdido do funil contam como ganho e perda] | Uma dica: estágio criado em Novo estágio é sempre de negociação. Só o Ganho e o Perdido que nascem com o funil contam como ganho e como perda nos cartões lá de cima. |
| fecha as Configurações › troca para o Funil de vendas (barra) › o quadro do Funil de vendas (sem a Visita técnica) › volta ao Sucata industrial | No quadro, eu troco de funil clicando no nome, aqui na barra. Cada funil tem o seu quadro, com as suas colunas. |

### cap04 · Nome, cor e orientação (vinheta: ESTÁGIOS)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Nome, cor e orientação". | (sem fala) |
| lápis Editar estágio Visita técnica › aba Coluna › aba Regras › aba Automações | Pra editar um estágio, é o lápis. Abre a configuração da Visita técnica, com três abas: Coluna, Regras e Automações. |
| Nome * Visita técnica › Cor * (veio cinza) › Cor: verde-azulado #0d9488 | Em Coluna ficam o nome e a cor. A cor veio cinza, e eu escolho uma diferente das outras, pra coluna destacar no quadro. |
| Orientação para o time › Orientação: Visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada. | E em Orientação para o time, o combinado da etapa: visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada. |
| Salvar etapa › lápis de novo: o texto fica na configuração da etapa › Orientação para o time salva (zoom) | Salvar etapa. Esse texto fica guardado aqui, na configuração da etapa. |
| fecha a configuração (Esc) › lixeira Excluir estágio Visita técnica › confirmação: Excluir este estágio? (zoom) › Cancelar (o estágio fica) | Uma dica: pra excluir um estágio, ele precisa estar vazio. Se tiver cartão nele, move os cartões pra outra coluna antes. |
| fecha as Configurações › ícone de informação na coluna Visita técnica (zoom) › clica no ícone: a orientação aparece ali mesmo › orientação da Visita técnica (zoom) › fecha a orientação | Agora, repara no quadro: a coluna ganhou um ícone de informação. Clicando nele, o time lê a orientação ali mesmo, sem abrir a configuração. |

### cap05 · Regras do estágio (vinheta: REGRAS)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Regras do estágio". | (sem fala) |
| lápis Editar estágio Em contato › aba Regras | Agora, as regras. Elas dizem o que precisa estar pronto antes de o cartão sair da etapa. Vou abrir o Em contato, na aba Regras. |
| (segue a tela da linha anterior) [ILUSTRAÇÃO: a regra é a porta de saída da coluna: o cartão só passa com a lista feita] | Pensa numa porta na saída da coluna. O cartão só passa quando o que está na lista estiver feito. |
| chave Tarefas › chave Checklists › chave Responsável › chave Prazo › chave Empresa › chave Observações | Dá pra exigir as tarefas encerradas, os checklists marcados, um responsável, a previsão de fechamento, a empresa e as observações do cartão. |
| liga Tarefas › liga Responsável | No Em contato, eu ligo duas: Tarefas e Responsável. Assim, o cartão só vai pra visita com dono e com as tarefas feitas. |
| Tarefas obrigatórias por nome (zoom) › Checklists obrigatórios por nome (zoom) › uma por linha / o nome tem que ser igualzinho (zoom) | Também dá pra exigir uma tarefa ou um checklist pelo nome. Pra exigir mais de uma, é uma por linha. Uma dica: o nome tem que ser igualzinho, letra por letra. Um acento ou um espaço a mais, e a regra não reconhece. |
| Salvar etapa | Salvar etapa. |

### cap06 · Automações (vinheta: AUTOMAÇÕES)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Automações". | (sem fala) |
| aba Automações › Novas automações nascem pausadas para revisão. › Nenhuma automação nesta etapa | E as automações. Elas fazem sozinhas o trabalho repetido, quando alguma coisa acontece no cartão. |
| (segue a tela da linha anterior) [ILUSTRAÇÃO: automação é um gatilho e as ações, que caem na ordem como dominós] | É sempre assim: um gatilho e as ações. Quando o gatilho acontece, o sistema faz as ações, na ordem. |
| Nova automação › Nome: Agendar a visita › Gatilho (abre a lista) › Ao entrar nesta etapa › Ao concluir uma tarefa › Ao concluir um checklist › Quando tudo estiver concluído › ... | Nova automação. O nome é Agendar a visita. No gatilho, dá pra escolher quando o cartão entra na etapa, quando uma tarefa ou um checklist é concluído, ou quando tudo estiver concluído. Fico com Ao entrar nesta etapa. |
| ação 1 (abre a lista das ações) › Criar tarefa › Aplicar checklist › Definir prazo do cartão › Atribuir responsável › Adicionar etiqueta › Mover cartão › ... | As ações são estas: Criar tarefa, Aplicar checklist, Definir prazo do cartão, Atribuir responsável, Adicionar etiqueta, Mover cartão e Copiar cartão. Aqui vai uma só: Criar tarefa. |
| Título da tarefa * › título: Agendar visita na › título: {CLIENTE} › Use {NOME} e {CLIENTE} nos textos dinâmicos. (zoom) | No título da tarefa, eu escrevo Agendar visita na, e o marcador CLIENTE, entre chaves. Ele vira o nome da empresa do cartão. |
| Prazo em dias: 1 › Contagem: Dias úteis | O prazo é de um dia útil. |
| a ação inteira (título, prazo e contagem) | A tarefa da automação fica com o responsável do cartão. Pra escolher quem é, existe a ação Atribuir responsável. |
| chave em Pausada (zoom) › liga a chave (Ativa) | Uma dica: toda automação nova nasce pausada. Se ficar assim, ela não roda. Então eu ligo pra Ativa. |
| Salvar automação › Agendar a visita, Ativa (zoom) | Salvar automação, e ela aparece ativa na lista. |
| Salvar etapa (zoom) › Fechar (zoom, sem clicar) | A automação já ficou salva. Agora, o nome, a cor e as regras só valem depois de Salvar etapa. Saindo pelo Fechar, o que não foi salvo se perde. |
| Ao entrar nesta etapa · 1 ação (zoom) [ILUSTRAÇÃO: Ao entrar nesta etapa roda quando o cartão avança; voltando de uma coluna da frente, não roda] | Uma dica: Ao entrar nesta etapa só roda quando o cartão avança pra ela, muda de funil ou já nasce nela. Voltando de uma coluna da frente, ela não roda. |

### cap07 · Checklists e etiquetas (vinheta: MODELOS)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Checklists e etiquetas". | (sem fala) |
| menu Checklists › aviso: o modelo é só o ponto de partida | Agora, os modelos. Em Checklists ficam as listas prontas que a gente aplica nos cartões. |
| Nova checklist › Nome: Documentos do fornecedor › Adicionar item (1) › item 1 › item 1: CNPJ conferido › Adicionar item (2) › item 2 › ... | Nova checklist: Documentos do fornecedor, com três itens: CNPJ conferido, local de retirada combinado e frequência da coleta combinada. Salvar. |
| o modelo Documentos do fornecedor na lista [ILUSTRAÇÃO: o modelo carimba uma cópia em cada cartão; mudar o modelo depois não mexe nas cópias] | O modelo é o ponto de partida. Aplicado num cartão, ele vira uma cópia. Mudar o modelo depois não mexe no que já foi aplicado. |
| lápis Editar checklist › setas: trocar a ordem dos itens › lixeira do item: tirar item › Cancelar (o modelo fica como está) › lixeira Excluir checklist › confirmação: Excluir este modelo de checklist? (zoom) › Cancelar (o modelo fica) | No lápis, eu edito o modelo: dá pra trocar a ordem dos itens e tirar item. E na lixeira, excluir. Das duas formas, os cartões que já receberam a lista não mudam. |
| menu Etiquetas › Nova etiqueta › Nome: Indústria › Cor (o seletor de cor) › Cor: #6366f1 › Salvar (Nova etiqueta) › a etiqueta Indústria na lista | Em Etiquetas, o caminho é parecido. Nova etiqueta, Indústria, com uma cor. Salvar. |
| lápis Editar etiqueta › nome e cor da etiqueta (zoom) › Cancelar (a etiqueta fica como está) › lixeira Excluir etiqueta › confirmação: Excluir esta etiqueta? (zoom) › Cancelar (a etiqueta fica) | Pra mudar o nome ou a cor, é o lápis. Agora, cuidado com a lixeira: excluir uma etiqueta tira ela de todos os cartões que usam. |
| (segue a tela da linha anterior) | São esses modelos que as regras e as automações usam: as ações Aplicar checklist e Adicionar etiqueta, e o checklist exigido pelo nome. |
| (segue a tela da linha anterior) | Uma dica: o modelo, a etiqueta e a pessoa que uma automação usa precisam continuar existindo. Se a ação não acha o que precisa, a automação falha e desfaz tudo: o cartão não muda de coluna, nem é criado. |

### cap08 · Automação com várias ações (vinheta: AUTOMAÇÕES)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Automação com várias ações". | (sem fala) |
| aba Automações da Visita técnica | Com os modelos prontos, dá pra montar uma automação mais completa. Vou criar uma na Visita técnica. |
| Nova automação › Nome: Preparar a proposta › Gatilho: Ao entrar nesta etapa › ação 1 (abre a lista das ações) › Aplicar checklist | O nome é Preparar a proposta, e o gatilho, Ao entrar nesta etapa. A primeira ação agora é Aplicar checklist. |
| Modelo de checklist (abre a lista) › Documentos do fornecedor › Nome no cartão › Nome no cartão: Documentos da › Nome no cartão: {CLIENTE} | Eu escolho o modelo Documentos do fornecedor. E no nome que vai pro cartão, uso de novo o marcador CLIENTE. |
| liga Criar tarefa vinculada › Concluir a tarefa marca o checklist e vice-versa (zoom) | Ligando Criar tarefa vinculada, o checklist ganha uma tarefa com o mesmo nome. Concluiu a tarefa, o checklist fica marcado. Marcou o checklist inteiro, a tarefa fica concluída. |
| Adicionar ação › ação 2 (abre a lista das ações) › Definir prazo do cartão › Prazo em dias › Prazo: 15 › Contagem: Dias corridos | Adicionar ação. A segunda é Definir prazo do cartão: quinze dias corridos. Esse prazo é a previsão de fechamento, e ela é trocada quando a automação roda. |
| Adicionar ação (3) › ação 3 (abre a lista das ações) › Mover cartão › ação 3 (abre a lista) › Copiar cartão › Copiar cartão: funil e etapa de destino (zoom) | As ações Mover cartão e Copiar cartão pedem o funil e a etapa de destino. Uma dica: Mover cartão tem que ser sempre a última ação, e o destino nunca é a coluna de perdido. |
| Remover ação (a terceira) › seta para baixo: troca a ordem das ações › seta para cima: volta a ordem | Aqui eu não vou mover nada, então removo essa ação. E com as setas, eu troco a ordem das ações. |
| liga a chave (Ativa) › apaga o nome (para mostrar o aviso) › Salvar automação sem nome › aviso: Dê um nome para a automação. (zoom) › Nome: Preparar a proposta › Salvar automação | Ligo pra Ativa. Se faltar alguma coisa, o sistema avisa o quê, como o nome aqui. Preenchido, Salvar automação. |
| Preparar a proposta na lista › Editar › botão de pausar › lixeira Excluir automação (sem clicar) | Na lista, cada automação tem o Editar, o botão de pausar, que desliga sem apagar, e a lixeira. Uma dica: a lixeira apaga na hora, sem perguntar. |
| Nova automação (só para mostrar os gatilhos) › Gatilho (abre a lista) › Ao concluir uma tarefa › Nome exato da tarefa * (zoom) › Ao concluir um checklist › Nome exato do checklist * (zoom) › Quando tudo estiver concluído › ... | E os outros gatilhos. Ao concluir uma tarefa e Ao concluir um checklist pedem o nome exato, letra por letra. E Quando tudo estiver concluído roda quando todas as tarefas do cartão estão encerradas e todos os itens de checklist, marcados. |
| Preparar a proposta, Ativa (zoom) [ILUSTRAÇÃO: o cartão volta e entra de novo na etapa: a automação não cria tudo em dobro, ela reaproveita a tarefa e o checklist que já tinha criado] | Uma dica: se o cartão voltar e entrar de novo na etapa, a automação não cria tudo em dobro. Ela aproveita a tarefa e o checklist que já tinha criado. |

### cap09 · Nova oportunidade (vinheta: OPORTUNIDADES)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Nova oportunidade". | (sem fala) |
| o quadro abre no Sucata industrial › coluna Visita técnica no lugar certo | Com o funil pronto, o quadro já abre no Sucata industrial, com a Visita técnica no lugar certo. |
| Nova oportunidade › Título: Retalho de chapa da Metalúrgica Jequitibá › Etapa *: Novo | A Metalúrgica Jequitibá ligou: gera retalho de chapa toda semana. Nova oportunidade. No título, Retalho de chapa da Metalúrgica Jequitibá. A etapa já vem em Novo. Esses dois são os obrigatórios. |
| Valor › seleciona o 0 › Valor 8400 (zoom) | O valor estimado: oito mil e quatrocentos reais por mês. |
| Responsável: Rafael Nogueira (vem preenchido) › Responsável: Sem responsável | O responsável já vem preenchido com quem está criando. Por enquanto, eu deixo sem responsável. |
| Empresa (abre a busca) › busca: Metalúrgica Jequitibá › Usar "Metalúrgica Jequitibá" como empresa avulsa › Contato: Paulo Lacerda › Área/Setor: Suprimentos › Telefone (sem mexer o cursor) › foco no Telefone › ... | Em Empresa, dá pra escolher um cliente ou fornecedor do cadastro. Escolhendo alguém dali, o contato, o telefone e o e-mail já vêm preenchidos. Mas a Metalúrgica Jequitibá ainda não é cadastrada, então eu uso o nome como empresa avulsa e preencho o contato eu mesmo: o Paulo Lacerda, de suprimentos, com telefone e e-mail. |
| a janela desce até Operação › Tipo de material (abre a busca) › busca: Chap › Chaparia › o mais ao lado do material (cadastrar) › Quantidade estimada 12000 Kg (zoom) › Meio de transporte: Frota própria | Na operação, o material é chaparia. Se o material ainda não existe, dá pra usar o nome avulso, ou cadastrar ali no mais. A unidade vem do material. São uns doze mil quilos por mês, e a retirada é com a frota própria. |
| Data inicial (zoom) › Previsão de fechamento › Previsão de fechamento 30/11/2026 › Observações › Observações: Quer retirada a cada quinze dias, com caçamba. | A data inicial marca quando a conversa começou. A previsão de fechamento é trinta de novembro. E nas observações, o que ela pediu: retirada a cada quinze dias, com caçamba. |
| Salvar (Nova oportunidade) › o cartão no Novo: material, valor e previsão › o mais da coluna Em contato (cria direto nela) | Salvar, e o cartão aparece no Novo, com o material, o valor e a previsão. E o mais de cada coluna cria a oportunidade direto naquela etapa. |
| o cartão (a compra se lança no caixa) | Quando o negócio fechar, a compra você lança no caixa, como sempre. O cartão guarda a história da negociação. |

### cap10 · Arrastar o cartão (vinheta: KANBAN)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Arrastar o cartão". | (sem fala) |
| arrasta o cartão pela alça até Em contato | Agora, andar com o cartão. O Paulo atendeu, então eu arrasto o cartão pela alça até Em contato. |
| o cartão em Em contato › selo de tarefas abertas 1 (zoom) | Repara: a automação já criou a tarefa de agendar a visita. O cartão mostra uma tarefa aberta. |
| arrasta para Visita técnica (a trava) › aviso: Conclua as tarefas pendentes. Defina um responsável. (zoom) › fecha o aviso | E se eu tentar levar pra Visita técnica agora? O sistema trava e mostra o que falta: Conclua as tarefas pendentes. Defina um responsável. |
| o cartão continua em Em contato | O cartão continua em Em contato, esperando. |
| a coluna Em contato (a regra da etapa de onde o cartão sai) [ILUSTRAÇÃO: a trava é a regra da etapa de onde o cartão sai, para avançar, voltar ou ir pro Perdido] | Uma dica: quem manda é a regra da etapa de onde o cartão sai. E ela vale pra qualquer troca: avançar, voltar uma coluna ou mandar pro Perdido. |
| o cartão (pra destravar, a ficha) | Pra destravar, é só resolver o que falta, na ficha do cartão. |

### cap11 · A ficha da oportunidade (vinheta: OPORTUNIDADES)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "A ficha da oportunidade". | (sem fala) |
| clique no cartão (abre a ficha) › aba Detalhes › aba Tarefas (1) › aba Histórico | Clicando no cartão, abre a ficha da oportunidade, com três abas: Detalhes, Tarefas e Histórico. |
| Funil: Sucata industrial › Estágio: Em contato › Responsável: Sem responsável › Responsável: Rafael Nogueira | Em Detalhes ficam o funil, o estágio e o responsável. Eu escolho o Rafael, o dono do ferro-velho, que vai cuidar dessa negociação. |
| a ficha desce até os valores › Valor Estimado R$ 8.400,00 › Previsão Fechamento 30/11/2026 › Material: Chaparia › Empresa: Metalúrgica Jequitibá › a ficha desce até as Observações › Observações (salvam sozinhas; o motivo da perda vai aqui) | Embaixo, o valor, a previsão, o material e a empresa. E as observações, que salvam sozinhas. É ali também que vai o motivo, se um negócio for pro Perdido. |
| a ficha desce até Etiquetas e Checklists › Etiquetas: Gerenciar › marca Indústria › fecha a lista das etiquetas › Checklists: Aplicar modelo (sem clicar) | Em Etiquetas, eu aplico a Indústria, que a gente criou nos modelos. Mais abaixo ficam os Checklists, que a gente vê daqui a pouco. |
| a ficha sobe até as abas › aba Tarefas › tarefa da automação: Agendar visita na Metalúrgica Jequitibá (11/11) › Concluir tarefa | Na aba Tarefas está a tarefa que a automação criou: Agendar visita na Metalúrgica Jequitibá. A visita já foi marcada, então eu concluo. |
| aba Histórico › Histórico: Etapa alterada de "Novo" para "Em contato". (quem e quando) › Histórico: Automação Agendar a visita executada | E o Histórico guarda cada mudança de etapa, com quem fez e quando. A automação também fica registrada ali, com o nome dela. |
| fecha a ficha › arrasta o cartão para Visita técnica (agora passa) | Fechando a ficha, agora sim: o cartão passa pra Visita técnica. |

### cap12 · Checklist na oportunidade (vinheta: OPORTUNIDADES)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Checklist na oportunidade". | (sem fala) |
| o cartão em Visita técnica (zoom) › previsão 25/11/2026 (zoom) | Repara no cartão. Quando ele entrou na Visita técnica, a automação Preparar a proposta aplicou o checklist e mudou a previsão pra vinte e cinco de novembro. |
| clique no cartão (abre a ficha) › a ficha desce até os Checklists › checklist Documentos da Metalúrgica Jequitibá | Na ficha, o checklist veio com o nome da empresa: Documentos da Metalúrgica Jequitibá. |
| marca: CNPJ conferido › marca: Local de retirada combinado › marca: Frequência da coleta combinada › 3/3 (zoom) | Na visita, o Rafael vai marcando. CNPJ conferido, local de retirada, frequência da coleta. Cada clique já salva. |
| a ficha sobe até as abas › aba Tarefas › tarefa vinculada: Concluída | E a tarefa vinculada ficou concluída sozinha, porque o checklist foi todo marcado. |
| aba Detalhes › a ficha desce até os Checklists › Aplicar modelo › escolhe o modelo Documentos do fornecedor | Sem automação, o caminho é o Aplicar modelo: escolhe o modelo, e a lista entra no cartão. |
| lixeira: Remover checklist › remove o checklist a mais (sem pergunta) | Aplicou a mais? A lixeira remove o checklist do cartão. Ela remove na hora, sem perguntar. |
| fecha a ficha › o cartão mostra o contador de itens (zoom) | E o cartão mostra quantos itens já foram feitos. |

### cap13 · Probabilidade, origem e tarefas (vinheta: OPORTUNIDADES)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Probabilidade, origem e tarefas". | (sem fala) |
| clique no cartão (abre a ficha) › a ficha desce até Probabilidade e Origem › Probabilidade 50% (zoom) | Ainda na ficha, dois campos que valem ouro. A Probabilidade é a chance de fechar. Todo cartão nasce com cinquenta por cento. |
| Probabilidade › Probabilidade: 80 › confirma (Enter) | A visita foi boa, então eu subo pra oitenta. |
| Origem: texto livre, exemplo WhatsApp (zoom) › Origem › Origem: Telefone › confirma (Enter) | E a Origem diz de onde veio o contato. É um texto livre, com o exemplo WhatsApp. Esse veio por telefone. |
| fecha a ficha › o cartão: barra de probabilidade verde, 80% (zoom) [ILUSTRAÇÃO: a probabilidade vira uma barra no cartão: verde de 70 pra cima, amarela de 40 a 69, vermelha abaixo de 40] | No cartão, a probabilidade vira uma barra: verde de setenta pra cima, amarela de quarenta a sessenta e nove, vermelha abaixo disso. Dá pra bater o olho e ver onde insistir. |
| clique no cartão (abre a ficha) › comentários (lado direito) › caixa de comentário › comentário: Paulo pediu a proposta até sexta. › Comentar › comentário com nome e hora (zoom) | Do lado direito ficam os comentários. Eu anoto o que foi combinado: Paulo pediu a proposta até sexta. Comentar. Fica com o meu nome e a hora, junto com as mudanças do cartão. |
| Criar Tarefa (pela ficha) › Título: Ligar pro Paulo › Data * (abre o calendário) › dia 13 › Salvar (Nova tarefa) | Pra não esquecer, Criar Tarefa, aqui mesmo. A oportunidade já vem ligada. Ligar pro Paulo, dia treze. Salvar. |
| aba Tarefas › os três pontinhos da tarefa › Editar › Marcar em andamento › Concluir › Cancelar tarefa › Excluir › ... | Na aba Tarefas, os três pontinhos trazem as ações: editar, marcar em andamento, concluir, cancelar ou excluir. Uma dica: pra regra da etapa, tarefa cancelada conta como encerrada. |
| aba Detalhes › a ficha sobe até as abas › Estágio (muda sem arrastar) › Funil (trocar manda pra primeira etapa do outro) | Pela ficha também dá pra mudar o estágio, sem arrastar, e a regra da etapa vale do mesmo jeito. E trocar o funil manda a oportunidade pra primeira etapa do outro funil. |
| a ficha desce até o contato › botão WhatsApp do contato (zoom, sem clicar) › Editar (abre o cadastro completo) › o cadastro desce até as Tarefas (no fim) › Tarefas no fim do cadastro › Cancelar | Como o cadastro tem telefone, a ficha ganha o botão WhatsApp, que abre a conversa fora do sistema. E o Editar abre o cadastro completo, pra corrigir valor, contato ou material, com as tarefas no fim. |
| lixeira Excluir oportunidade › lixeira (abre a confirmação) › confirmação: Excluir esta oportunidade? (zoom) › Cancelar (a oportunidade fica) | E a lixeira exclui a oportunidade. Uma dica: vão junto as tarefas e o histórico, e não tem volta. Negócio que não deu certo vai pro Perdido, não pra lixeira. |
| fecha a ficha › o cartão: 80% e Telefone (zoom) | Fechando, o cartão já mostra os oitenta por cento e a origem. |

### cap14 · Tarefas e Agenda (vinheta: TAREFAS)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Tarefas e Agenda". | (sem fala) |
| aba Tarefas › coluna Pendente › coluna Em andamento › coluna Concluída (a tarefa da visita) › coluna Cancelada | Agora, a aba Tarefas. Ela junta as tarefas de todas as oportunidades. No Kanban, cada coluna é uma situação: pendente, em andamento, concluída e cancelada. |
| Nova tarefa › Título: Enviar proposta › Oportunidade * (abre a busca) › Retalho de chapa da Metalúrgica Jequitibá › Responsável (abre a busca) › Rafael Nogueira › Data * (abre o calendário) › ... | Depois da visita, vem a proposta. Nova tarefa: Enviar proposta, ligada à oportunidade da Jequitibá, com o Rafael, pra quinta, dia doze, prioridade alta. Salvar. |
| Enviar proposta em Pendente › arrasta Enviar proposta para Em andamento | Ela entra em Pendente. No Kanban, eu mudo a situação arrastando. Comecei a proposta, levo pra Em andamento. |
| clique na tarefa (abre a edição) › Hora › Descrição › Lembrar no dia › Excluir (zoom, sem clicar) › Cancelar | Clicando na tarefa, abre a edição: dá pra pôr hora, descrição e lembrete. É aqui também que ela é excluída, e sai da Agenda junto. |
| Filtrar › Filtrar: responsável, situação, prioridade e oportunidade › fecha o Filtrar › busca por título | Em Filtrar, dá pra separar por responsável, situação, prioridade e oportunidade. E a busca acha pelo título. |
| visão Lista › coluna Oportunidade › coluna Responsável › coluna Data › coluna Prioridade › clica no cabeçalho Data (ordena) | Na Lista, as mesmas tarefas viram uma tabela, com a oportunidade, o responsável, a data e a prioridade. Clicando no cabeçalho, eu ordeno. |
| visão Calendário › Mês › Semana › Dia › Enviar proposta no dia 12 (calendário) | E o Calendário mostra por mês, semana ou dia, cada tarefa no seu dia. |
| Agenda (menu lateral) › Enviar proposta no dia 12, selo CRM (zoom) | E a mesma tarefa aparece na Agenda, com o selo CRM. Assim, ela entra na rotina do dia. |
| uma tarefa só (zoom) [ILUSTRAÇÃO: uma tarefa só, na aba Tarefas e na Agenda: concluiu num, aparece concluída no outro] | É uma tarefa só, nos dois lugares. Concluiu num, aparece concluída no outro. |
| clique na tarefa (leva ao CRM) › Editar oportunidade da Jequitibá › Cancelar | Clicando nela, a Agenda leva direto pra oportunidade no CRM. Uma dica: na Agenda dá pra concluir a tarefa; pra editar ou excluir, é na aba Tarefas do CRM. |

### cap15 · Filtros, busca e fechar o negócio (vinheta: FILTROS)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Filtros, busca e fechar o negócio". | (sem fala) |
| Total de oportunidades 6 (zoom) › Valor total R$ 62.300,00 (zoom) | Com o funil em uso, entram mais cartões. No fim do dia, a Recicla Vale já tem seis oportunidades no funil: sessenta e dois mil e trezentos reais no total. |
| Ganhos R$ 19.000,00 (zoom) › Em negociação R$ 41.650,00 (zoom) | Já são dezenove mil reais ganhos, com a Construtora Pilar, e quarenta e um mil seiscentos e cinquenta reais em negociação. |
| Busca › busca: alumínio › o cartão da Esquadrias Horizonte › cartões de cima dizem filtrado | Na busca, dá pra achar pelo título, pelo contato, pela empresa ou pelo material. Digitando alumínio, sobra o cartão da Esquadrias Horizonte. E os cartões de cima passam a dizer filtrado. |
| apaga a busca › Filtros › Status › Valor mínimo / Valor máximo › Responsável › Material › Meio de transporte | Nos Filtros, dá pra separar por situação, por faixa de valor, por responsável, por material e por meio de transporte. |
| Responsável: Rafael Nogueira › Status: Em negociação › Aplicar › Valor total (filtrado) R$ 26.200,00 (zoom) | Quero ver o que está com o Rafael e ainda em negociação. O quadro se ajusta a cada escolha, e o Aplicar só fecha a janela. Ficam dois cartões: vinte e seis mil e duzentos reais. |
| Filtros (2) › Limpar filtros › Aplicar (voltam os seis) | Pra ver tudo de novo, é Limpar filtros. |
| Filtros (3) › Status: Perdidos › Aplicar › abre o cartão do Papelão (Perdido) › a ficha desce até as Observações › Observações: o motivo da perda (zoom) › fecha a ficha › ... | Outro uso: em Status, Perdidos, pra rever o que não fechou. O motivo está nas observações do cartão. |
| arrasta o cartão da Elétrica Ponto Certo para cima do outro, em Em contato › a ordem se mantém: o mais urgente no topo | O cartão fica onde eu soltar. Levo o da Elétrica Ponto Certo pra Em contato, em cima do outro, e a ordem se mantém. Assim, o mais urgente fica no topo. |
| arrasta Caminho Firme para Ganho › Ganhos R$ 23.650,00 (zoom) › Em negociação R$ 37.000,00 (zoom) | E quando fecha? A Transportadora Caminho Firme aceitou a proposta. Arrasto pra Ganho, e os cartões de cima acompanham: vinte e três mil seiscentos e cinquenta reais ganhos, trinta e sete mil reais em negociação. |

### cap16 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Recapitulando". | (sem fala) |
| Funil de vendas (montado sozinho) › abas Funil e Tarefas › os quatro cartões | Pronto! Recapitulando: o CRM montou sozinho o Funil de vendas, e a gente conheceu as abas e os quatro cartões. |
| Configurações do CRM/Kanban › Sucata industrial, Padrão › abre o Sucata industrial › Configurar Visita técnica (cor e orientação) | Criou o funil Sucata industrial, tornou padrão, pôs a Visita técnica no lugar e deu cor e orientação pra ela. |
| fecha a Visita técnica › Configurar Em contato › aba Regras (Tarefas e Responsável ligadas) › aba Automações (Agendar a visita, Ativa) › fecha o Em contato › Checklists › Etiquetas | Ligou as regras de saída do Em contato e criou e ativou duas automações, uma que agenda a visita e outra que prepara a proposta, além do checklist e da etiqueta. |
| fecha as Configurações › o cartão da Jequitibá em Visita técnica | Cadastrou a oportunidade da Metalúrgica Jequitibá, viu a trava, resolveu na ficha e moveu o cartão. Marcou o checklist, ajustou a probabilidade e a origem, e comentou. |
| aba Tarefas › Agenda | A tarefa apareceu na aba Tarefas e na Agenda, os filtros separaram o funil, e um negócio fechou arrastando pra Ganho. |
| (segue a tela da linha anterior) | Essa foi a última aula da trilha. Sempre que precisar, volta em qualquer aula pelo capítulo que quiser rever. Até lá! |
