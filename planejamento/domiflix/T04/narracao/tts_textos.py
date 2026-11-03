# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T4 "Tipos de Serviço, Tipos de Tarefa e Checklists".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   ISS -> "i-ésse-ésse" | LC -> "éle-cê" | MP -> "ême-pê" | psi -> "pê-ésse-i"
CAPS = {
0: """Oi! Neste tutorial a gente vai montar o cardápio de serviços da sua empresa e os roteiros que o técnico preenche em cada visita: os tipos de serviço, os tipos de tarefa e os checklists.
É daqui que saem as ordens de serviço: o tipo de cada uma, o prefixo do número e o roteiro do técnico. Quanto mais caprichado esse cadastro, mais rápido fica abrir uma ordem.
Se você ainda não viu o tutorial de Clientes, Fornecedores e Equipamentos, dá uma olhada antes. [pause] Vamos abrir a tela de Serviços.""",
1: """Os serviços ficam no menu da esquerda, em Gestão, Serviços.
A tela tem três abas: Tipos de Serviços, Tipos de Tarefas e Checklists. O tipo de serviço diz o que a equipe vai fazer, o checklist é o roteiro dessa visita, e o tipo de tarefa organiza os compromissos internos da agenda. A gente passa pelas três, nessa ordem.
Na primeira aba ainda não tem nada. Aqui em cima ficam os botões Categorias e Novo Serviço. Vamos começar pelas categorias.""",
2: """As categorias agrupam serviços parecidos e depois viram um filtro na lista. Vale criar antes dos serviços.
Escrevo o nome, escolho a cor e clico no mais. Instalação, Manutenção e Higienização.
Pela alça do lado, dá pra arrastar e deixar na ordem que você preferir.
Pronto, três categorias. Agora o primeiro serviço.""",
3: """Vou cadastrar a manutenção preventiva, que é o serviço que a Glaciál mais faz. Clico em Novo Serviço.
Dou o nome, Manutenção Preventiva, e escolho uma cor, que identifica o serviço nas listas. Uma dica: uma cor diferente pra cada serviço ajuda a bater o olho.
Escolho a categoria Manutenção e escrevo uma descrição curta.
No Prefixo de Numeração OS vão as letras que abrem o número da ordem de serviço. Pra preventiva, ême-pê. Assim, quando a ordem sair, o número já mostra de que serviço se trata.
Em Preço padrão, coloco cento e oitenta reais. É o valor que o orçamento sugere quando você adiciona esse serviço, e dá pra ajustar na hora.
Os dois interruptores ficam ligados: o Vinculado a equipamento, que a gente explica já já, e o Ativo, que deixa o serviço disponível pra escolher.
Criar. Pronto, o primeiro serviço está na lista.
Os outros serviços da Glaciál eu já deixei cadastrados do mesmo jeito: manutenção corretiva, instalação, higienização, carga de gás e visita técnica.""",
4: """Agora a lista tem os seis serviços, cada um com a sua cor, a categoria e o prefixo.
Pra achar um, é só buscar pelo nome ou pela descrição.
Em Filtros você vê só uma categoria, e em Ordenar escolhe a ordem de A a Z ou de Z a A.
Agora o Vinculado a equipamento. Na Manutenção Preventiva ele está ligado: a ordem de serviço pede o aparelho do cliente, o que é bom pra higienização e manutenção. Já a Visita Técnica está desligada, porque serve pra visita e orçamento, onde ainda não tem aparelho.
Na hora de abrir a ordem, ligado, a Dominex pede o aparelho do cliente. Desligado, pede só o serviço.""",
5: """Agora os dados fiscais do serviço. Se a sua empresa emite nota fiscal de serviço, esta aba é pra você. A Fiscal aparece pra quem tem o módulo de Nota Fiscal.
No Código de serviço, eu busco o código do serviço, catorze ponto zero um ponto zero um, e escolho. O Item da éle-cê cento e dezesseis vem preenchido sozinho.
O código de tributação municipal tem três dígitos, definidos pela prefeitura: zero zero um. É ele que a prefeitura usa pra aceitar a nota.
E a Alíquota de i-ésse-ésse, que é a do seu município. Aqui, cinco por cento. Salvo. Vale preencher agora: com o código salvo aqui, toda nota emitida com esse serviço já nasce classificada.""",
6: """Agora o dia a dia do cadastro. Pra mudar qualquer coisa, é só abrir o serviço, editar a ficha aqui do lado e salvar.
Uma dica: pra pausar um serviço sem perder o histórico, é só desligar o Ativo. Ele sai das listas de escolha e continua cadastrado.
O Excluir pede confirmação, e remove o cadastro de vez. Aqui eu cancelo.""",
7: """Agora a aba Tipos de Tarefas. Tarefa é um compromisso interno da equipe, diferente da ordem de serviço, que é pro cliente. Os tipos aparecem na Agenda, quando você cria uma nova tarefa, e só os ativos entram na escolha.
Clico em Novo Tipo, dou o nome, Reunião, escolho a cor e clico em Criar.
Faço o mesmo com Entrega de material e com Compra de peças.
Cada tipo tem a sua ficha, com cor, descrição e o Ativo, igual aos serviços.""",
8: """Agora os checklists, que são o roteiro que o técnico preenche em cada visita: o que conferir, medir e fotografar. Pra não começar do zero, a Dominex tem modelos prontos.
No Catálogo de Checklists ficam os modelos sugeridos pro seu ramo: instalação, higienização, manutenção preventiva e carga de gás. Cada empresa adapta do seu jeito, porque as perguntas ficam totalmente editáveis depois.
Olha o da manutenção preventiva: já vem com as perguntas prontas, cada uma com o seu jeito de responder, como um número em pê-ésse-i, e com as obrigatórias marcadas.
Clico em Selecionar, dou o nome do meu checklist, Manutenção preventiva de split, e Criar checklist. Pronto: treze perguntas importadas de uma vez.""",
9: """O checklist já abriu no editor. Em Serviços habilitados eu escolho onde ele vale: tiro o Todos os serviços e marco só a Manutenção Preventiva. Assim ele aparece só nas ordens desse serviço.
Agora um checklist do zero. Clico em Novo checklist, dou o nome, Higienização de split, desligo o Todos os serviços e marco a Higienização de Split. Criar.
Uma dica: se você não marcar nenhum serviço, o checklist vale pra todos.""",
10: """Hora das perguntas. Clico em Nova Pergunta. À esquerda a gente monta a pergunta, e à direita a prévia mostra como o técnico vai ver na ordem de serviço.
Escrevo a pergunta, Estado da serpentina, e uma orientação que só o técnico vê. Uma dica: a pergunta fica curta e direta, e a explicação vai na orientação. Em Escolha como responder, marco Conformidade, e a prévia já mostra as três respostas.
São oito jeitos de responder: Verdadeiro ou Falso, Conformidade, Texto, Número, Foto, Vídeo, Seleção e Assinatura.
Deixo o Campo obrigatório ligado, e a ordem só avança depois que o técnico responde. A Frequência é pros contratos, e a gente vê no tutorial de Contratos. Nova Pergunta, e ela entra no checklist.
Outra pergunta: Aspecto da água retirada, do tipo Seleção. Escrevo as opções: limpa, turva e suja.""",
11: """Agora uma coisa que deixa a pergunta mais completa: dá pra combinar jeitos de responder. Em Filtros lavados?, deixo Verdadeiro ou Falso e marco Foto também. Aparece o Modo de resposta múltipla: no Exclusivo, o técnico escolhe uma forma só; no Cumulativo, responde as duas. Escolho Cumulativo: ele marca e ainda anexa a foto.
Ligo o Exigir foto da câmera, e a foto passa a ser tirada na hora, sem usar a galeria.
No tipo Vídeo, o técnico grava um clipe curto como resposta. Com o Exigir gravação na hora, o clipe é gravado na hora, como a foto.""",
12: """Com as perguntas criadas, vale organizar e conferir. Na lista, cada pergunta mostra o jeito de responder e os selos Cumulativo e Câmera. Pela alça, dá pra arrastar e deixar na ordem em que o técnico vai executar.
E quando o checklist cresce, a busca e o filtro de tipo ajudam a achar uma pergunta.
Pra conferir, o botão Ver abre o checklist igualzinho ao que o técnico vê na ordem de serviço. Dá pra responder à vontade, que nada é salvo.""",
13: """Pra fechar os checklists, o vínculo e a desativação. Na lista, cada checklist mostra quantas perguntas tem e em quais serviços vale.
Pra aposentar um checklist, é só desativar: ele sai da lista e das ordens novas, e as ordens antigas continuam com o roteiro que usaram. É por isso que o sistema desativa em vez de apagar. Aqui eu cancelo.""",
14: """Pronto! Recapitulando: a gente criou as categorias e os tipos de serviço, com cor, prefixo, preço padrão e os dados fiscais. E cadastrou os tipos de tarefa que aparecem na Agenda.
Depois montou os checklists: um a partir do modelo pronto e outro do zero, com perguntas de vários tipos, cada um ligado aos serviços certos.
Com os serviços e os roteiros prontos, no próximo tutorial a gente abre ordens de serviço, organiza a agenda das equipes e acompanha tudo no mapa ao vivo. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela de Serviços.",
           2: "Categorias.",
           3: "Novo tipo de serviço.",
           4: "Organizando a lista.",
           5: "Dados fiscais.",
           6: "Editar, desativar e excluir.",
           7: "Tipos de tarefa.",
           8: "Catálogo de modelos.",
           9: "Checklist do zero.",
           10: "As perguntas.",
           11: "Combinando respostas.",
           12: "Organizar e conferir.",
           13: "Vincular e desativar.",
           14: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Serviços",
           2: "Serviços",
           3: "Serviços",
           4: "Serviços",
           5: "Serviços",
           6: "Serviços",
           7: "Tarefas",
           8: "Checklists",
           9: "Checklists",
           10: "Checklists",
           11: "Checklists",
           12: "Checklists",
           13: "Checklists",
           14: "Resumo"}

if __name__ == "__main__":
    tot = 0
    pal = 0
    for k, v in CAPS.items():
        w = len(v.replace("[pause]", "").split())
        tot += len(v)
        pal += w
        print(f"cap {k:2d}: {len(v):5d} chars, {w:4d} palavras, ~{w/2.6:5.1f} s")
    tit = sum(len(v) for v in TITULOS.values())
    print("total chars CAPS", tot, "| TITULOS", tit, "| soma", tot + tit, "| palavras", pal, f"| ~{pal/2.6/60:.1f} min de fala")
