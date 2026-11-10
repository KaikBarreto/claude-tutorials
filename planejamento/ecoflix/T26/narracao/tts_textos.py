# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T26 "CRM/Kanban".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala, na mesma ordem.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   CRM/Kanban -> "cê-érre-ême-canban" | CRM -> "cê-érre-ême" | Kanban -> "canban"
# A testar no ensaio: "checklist"/"checklists", "WhatsApp" e "Jequitibá" na escrita normal.
CAPS = {
0: """Oi! Neste tutorial a gente vai organizar os negócios da Recicla Vale Metais num funil, pra nenhuma oportunidade se perder no caminho.
Sabe aquela indústria que avisou que tem sucata toda semana? A conversa fica no WhatsApp, ninguém retorna, e o negócio esfria.
No cê-érre-ême, cada contato vira um cartão, com dono, valor e o próximo passo.
Ele fica no menu lateral, em cê-érre-ême-canban.
O cê-érre-ême-canban depende do plano contratado.
Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. [pause] Vamos abrir o cê-érre-ême.""",
1: """Na primeira vez que alguém abre o cê-érre-ême, ele monta sozinho um funil, o Funil de vendas.
São cinco colunas: Novo, Em contato, Proposta, Ganho e Perdido.
Funil é isso: entram muitos contatos em cima, alguns viram proposta, e uma parte fecha. O resto fica pelo caminho, no Perdido.
No sistema, o funil fica deitado. Cada etapa é uma coluna, e o cartão anda pra direita conforme o negócio avança.
Cada contato entra no funil por aqui, em Nova oportunidade. A gente cria uma daqui a pouco.""",
2: """Lá em cima ficam as duas abas: Funil, que é esse quadro, e Tarefas, com as tarefas de cada oportunidade.
E os quatro cartões: Total de oportunidades, Valor total, Ganhos e Em negociação. Por enquanto, tudo zerado.
O Total e o Valor total contam todos os cartões do funil. Ganhos soma só o que está na coluna Ganho. E Em negociação, o que ainda não ganhou nem perdeu.
Embaixo ficam a busca, os filtros e o botão Nova oportunidade. E nessa barra, os funis da empresa.
Uma dica: quem tem acesso à tela do cê-érre-ême pode criar, editar, excluir e configurar tudo. Então libera a tela só pra quem vai cuidar do funil.""",
3: """Agora, as configurações. Em Configurações do cê-érre-ême-canban, na parte Funis, está o Funil de vendas, marcado como Padrão.
A Recicla Vale quer um funil só pras indústrias que geram sucata. Novo funil, o nome é Sucata industrial, e uma cor. Salvar.
Ele já nasce com as mesmas cinco etapas. Clico em Tornar padrão, e ele passa a abrir primeiro no cê-érre-ême.
Arrastando a linha, eu mudo a ordem dos funis na barra. O Sucata industrial vai pra frente.
Abrindo o funil, aparecem os estágios. Entre o contato e a proposta, a Recicla Vale sempre visita a indústria. Então, Novo estágio: Visita técnica. Salvar etapa.
O estágio novo entra no fim. Eu arrasto ele pra depois de Em contato.
Uma dica: estágio criado em Novo estágio é sempre de negociação. Só o Ganho e o Perdido que nascem com o funil contam como ganho e como perda nos cartões lá de cima.""",
4: """Pra editar um estágio, é o lápis. Abre a configuração da Visita técnica, com três abas: Coluna, Regras e Automações.
Em Coluna ficam o nome e a cor. A cor veio cinza, e eu escolho uma diferente das outras, pra coluna destacar no quadro.
E em Orientação para o time, o combinado da etapa: visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada.
Salvar etapa. Esse texto fica aqui, na configuração da etapa, como referência pro time.
Uma dica: pra excluir um estágio, ele precisa estar vazio. Se tiver cartão nele, move os cartões pra outra coluna antes.""",
5: """Agora, as regras. Elas dizem o que precisa estar pronto antes de o cartão sair da etapa. Vou abrir o Em contato, na aba Regras.
Pensa numa porta na saída da coluna. O cartão só passa quando o que está na lista estiver feito.
Dá pra exigir as tarefas encerradas, os checklists marcados, um responsável, a previsão de fechamento, a empresa e as observações do cartão.
No Em contato, eu ligo duas: Tarefas e Responsável. Assim, o cartão só vai pra visita com dono e com as tarefas feitas.
Também dá pra exigir uma tarefa ou um checklist pelo nome. Uma dica: o nome tem que ser igualzinho, letra por letra. Um acento ou um espaço a mais, e a regra não reconhece.
Salvar etapa.""",
6: """E as automações. Elas fazem sozinhas o trabalho repetido, quando alguma coisa acontece no cartão.
É sempre assim: um gatilho e as ações. Quando o gatilho acontece, o sistema faz as ações, na ordem.
Nova automação. O nome é Agendar a visita. No gatilho, dá pra escolher quando o cartão entra na etapa, quando uma tarefa ou um checklist é concluído, ou quando tudo estiver concluído. Fico com Ao entrar nesta etapa.
As ações são estas: Criar tarefa, Aplicar checklist, Definir prazo do cartão, Atribuir responsável, Adicionar etiqueta, Mover cartão e Copiar cartão. Aqui vai uma só: Criar tarefa.
No título da tarefa, eu escrevo Agendar visita na, e o marcador CLIENTE, entre chaves. Ele vira o nome da empresa do cartão.
O prazo é de um dia útil.
A tarefa da automação fica com o responsável do cartão. Pra escolher quem é, existe a ação Atribuir responsável.
Uma dica: toda automação nova nasce pausada. Se ficar assim, ela não roda. Então eu ligo pra Ativa.
Salvar automação, e ela aparece ativa na lista.
Uma dica: Ao entrar nesta etapa só roda quando o cartão avança pra ela, muda de funil ou já nasce nela. Voltando de uma coluna da frente, ela não roda.""",
7: """Agora, os modelos. Em Checklists ficam as listas prontas que a gente aplica nos cartões.
Nova checklist: Documentos do fornecedor, com três itens: CNPJ conferido, local de retirada combinado e frequência da coleta combinada. Salvar.
O modelo é o ponto de partida. Aplicado num cartão, ele vira uma cópia. Mudar o modelo depois não mexe no que já foi aplicado.
Em Etiquetas, a mesma ideia. Nova etiqueta, Indústria, com uma cor. Salvar.
São esses modelos que as regras e as automações usam: as ações Aplicar checklist e Adicionar etiqueta, e o checklist exigido pelo nome.
Uma dica: o modelo, a etiqueta e a pessoa que uma automação usa precisam continuar existindo. Se a ação não acha o que precisa, a automação falha e desfaz tudo: o cartão não muda de coluna, nem é criado.""",
8: """Com o funil pronto, o quadro já abre no Sucata industrial, com a Visita técnica no lugar certo.
A Metalúrgica Jequitibá ligou: gera retalho de chapa toda semana. Nova oportunidade. No título, Retalho de chapa da Metalúrgica Jequitibá. A etapa já vem em Novo. Esses dois são os obrigatórios.
O valor estimado: oito mil e quatrocentos reais por mês.
O responsável fica em branco por enquanto.
Em Empresa, dá pra escolher um cliente ou fornecedor do cadastro. Ela ainda não é cadastrada, então eu uso o nome como empresa avulsa. O contato é o Paulo Lacerda, de suprimentos.
Na operação, o material é chaparia, uns doze mil quilos por mês, e a retirada é com a frota própria.
A previsão de fechamento é trinta de novembro. E nas observações, o que ela pediu: retirada a cada quinze dias, com caçamba.
Salvar, e o cartão aparece no Novo, com o material, o valor e a previsão.
Quando o negócio fechar, a compra você lança no caixa, como sempre. O cartão guarda a história da negociação.""",
9: """Agora, andar com o cartão. O Paulo atendeu, então eu arrasto o cartão pela alça até Em contato.
Repara: a automação já criou a tarefa de agendar a visita. O cartão mostra uma tarefa aberta.
E se eu tentar levar pra Visita técnica agora? O sistema trava e mostra o que falta: Conclua as tarefas pendentes. Defina um responsável.
O cartão continua em Em contato, esperando.
Uma dica: quem manda é a regra da etapa de onde o cartão sai. E ela vale pra qualquer troca: avançar, voltar uma coluna ou mandar pro Perdido.
Pra destravar, é só resolver o que falta, na ficha do cartão.""",
10: """Clicando no cartão, abre a ficha da oportunidade, com três abas: Detalhes, Tarefas e Histórico.
Em Detalhes ficam o funil, o estágio e o responsável. Eu escolho o Rafael, o dono do ferro-velho, que vai cuidar dessa negociação.
Embaixo, o valor, a previsão, o material e a empresa. E as observações, que salvam sozinhas. É ali também que vai o motivo, se um negócio for pro Perdido.
Em Etiquetas, eu aplico a Indústria, que a gente criou nos modelos. E em Checklists, o Aplicar modelo coloca a lista no cartão.
Na aba Tarefas está a tarefa que a automação criou: Agendar visita na Metalúrgica Jequitibá. A visita já foi marcada, então eu concluo.
E o Histórico guarda cada mudança de etapa, com quem fez e quando.
Fechando a ficha, agora sim: o cartão passa pra Visita técnica.""",
11: """Agora, a aba Tarefas. Ela junta as tarefas de todas as oportunidades. No canban, cada coluna é uma situação: pendente, em andamento, concluída e cancelada.
Depois da visita, vem a proposta. Nova tarefa: Enviar proposta, ligada à oportunidade da Jequitibá, com o Rafael, pra quinta, dia doze, prioridade alta. Salvar.
Ela entra em Pendente. Na Lista, as mesmas tarefas viram uma tabela, com a oportunidade, o responsável, a data e a prioridade.
E no Calendário, cada tarefa no seu dia.
E a mesma tarefa aparece na Agenda, com o selo cê-érre-ême. Assim, ela entra na rotina do dia.
É uma tarefa só, nos dois lugares. Concluiu num, aparece concluída no outro.
Clicando nela, a Agenda leva direto pra oportunidade no cê-érre-ême. Uma dica: na Agenda dá pra concluir a tarefa; pra editar ou excluir, é na aba Tarefas do cê-érre-ême.""",
12: """Com o funil em uso, entram mais cartões. No fim do dia, a Recicla Vale já tem seis oportunidades no funil: sessenta e dois mil e trezentos reais no total.
Já são dezenove mil reais ganhos, com a Construtora Pilar, e quarenta e um mil seiscentos e cinquenta reais em negociação.
Na busca, dá pra achar pelo título, pelo contato, pela empresa ou pelo material. Digitando alumínio, sobra o cartão da Esquadrias Horizonte. E os cartões de cima passam a dizer filtrado.
Nos Filtros, dá pra separar por situação, por faixa de valor, por responsável, por material e por meio de transporte.
Quero ver o que está com o Rafael e ainda em negociação. Aplicar, e ficam dois cartões: vinte e seis mil e duzentos reais.
Pra ver tudo de novo, é Limpar filtros.""",
13: """Pronto! Recapitulando: o cê-érre-ême montou sozinho o Funil de vendas, e a gente conheceu as abas e os quatro cartões.
Criou o funil Sucata industrial, tornou padrão, pôs a Visita técnica no lugar e deu cor e orientação pra ela.
Ligou as regras de saída do Em contato e criou e ativou a automação que agenda a visita, além do checklist e da etiqueta.
Cadastrou a oportunidade da Metalúrgica Jequitibá, viu a trava, resolveu na ficha e moveu o cartão. A tarefa apareceu na aba Tarefas e na Agenda, e os filtros separaram o funil.
Essa foi a última aula da trilha. Sempre que precisar, volta em qualquer aula pelo capítulo que quiser rever. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O funil de vendas.",
           2: "Funil, Tarefas e os cartões.",
           3: "Funis e estágios.",
           4: "Nome, cor e orientação.",
           5: "Regras do estágio.",
           6: "Automações.",
           7: "Checklists e etiquetas.",
           8: "Nova oportunidade.",
           9: "Arrastar o cartão.",
           10: "A ficha da oportunidade.",
           11: "Tarefas e Agenda.",
           12: "Filtros e busca.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "CRM",
           2: "CRM",
           3: "Funis",
           4: "Estágios",
           5: "Regras",
           6: "Automações",
           7: "Modelos",
           8: "Oportunidades",
           9: "Kanban",
           10: "Oportunidades",
           11: "Tarefas",
           12: "Filtros",
           13: "Resumo"}

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
