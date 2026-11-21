# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T26 "CRM/Kanban" (app 1.60.22, aplicação de 21/11).
# Cada linha do texto é uma linha da tabela Tela x Fala do roteiro.md (o robô prende cada gesto a uma palavra da linha).
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   CRM/Kanban -> "cê-érre-ême-canban" | CRM -> "cê-érre-ême" | Kanban -> "canban"
# A testar na voz: "checklist"/"checklists", "WhatsApp" e "Jequitibá" na escrita normal.
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
Embaixo ficam a busca, os filtros e o botão Nova oportunidade. E nessa barra, os funis da empresa. A engrenagem abre as configurações, e o mais cria um funil novo.
Uma dica: quem tem acesso à tela do cê-érre-ême pode criar, editar, excluir e configurar tudo. Então libera a tela só pra quem vai cuidar do funil.""",
3: """Agora, as configurações. Em Configurações do cê-érre-ême-canban, na parte Funis, está o Funil de vendas, marcado como Padrão.
A Recicla Vale quer um funil só pras indústrias que geram sucata. Novo funil, o nome é Sucata industrial, e uma cor. Salvar.
Ele já nasce com as mesmas cinco etapas. Clico em Tornar padrão, e ele passa a abrir primeiro no cê-érre-ême.
Arrastando a linha, eu mudo a ordem dos funis na barra. O Sucata industrial vai pra frente.
No lápis, dá pra trocar o nome e a cor de um funil. E na lixeira, excluir. Uma dica: excluir o funil apaga todas as oportunidades dele, e não tem volta.
Abrindo o funil, aparecem os estágios. Entre o contato e a proposta, a Recicla Vale sempre visita a indústria. Então, Novo estágio: Visita técnica. Salvar etapa.
O estágio novo entra no fim. Eu arrasto ele pra depois de Em contato.
Uma dica: estágio criado em Novo estágio é sempre de negociação. Só o Ganho e o Perdido que nascem com o funil contam como ganho e como perda nos cartões lá de cima.
No quadro, eu troco de funil clicando no nome, aqui na barra. Cada funil tem o seu quadro, com as suas colunas.""",
4: """Pra editar um estágio, é o lápis. Abre a configuração da Visita técnica, com três abas: Coluna, Regras e Automações.
Em Coluna ficam o nome e a cor. A cor veio cinza, e eu escolho uma diferente das outras, pra coluna destacar no quadro.
E em Orientação para o time, o combinado da etapa: visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada.
Salvar etapa. Esse texto fica guardado aqui, na configuração da etapa.
Uma dica: pra excluir um estágio, ele precisa estar vazio. Se tiver cartão nele, move os cartões pra outra coluna antes.
Agora, repara no quadro: a coluna ganhou um ícone de informação. Clicando nele, o time lê a orientação ali mesmo, sem abrir a configuração.""",
5: """Agora, as regras. Elas dizem o que precisa estar pronto antes de o cartão sair da etapa. Vou abrir o Em contato, na aba Regras.
Pensa numa porta na saída da coluna. O cartão só passa quando o que está na lista estiver feito.
Dá pra exigir as tarefas encerradas, os checklists marcados, um responsável, a previsão de fechamento, a empresa e as observações do cartão.
No Em contato, eu ligo duas: Tarefas e Responsável. Assim, o cartão só vai pra visita com dono e com as tarefas feitas.
Também dá pra exigir uma tarefa ou um checklist pelo nome. Pra exigir mais de uma, é uma por linha. Uma dica: o nome tem que ser igualzinho, letra por letra. Um acento ou um espaço a mais, e a regra não reconhece.
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
A automação já ficou salva. Agora, o nome, a cor e as regras só valem depois de Salvar etapa. Saindo pelo Fechar, o que não foi salvo se perde.
Uma dica: Ao entrar nesta etapa só roda quando o cartão avança pra ela, muda de funil ou já nasce nela. Voltando de uma coluna da frente, ela não roda.""",
7: """Agora, os modelos. Em Checklists ficam as listas prontas que a gente aplica nos cartões.
Nova checklist: Documentos do fornecedor, com três itens: CNPJ conferido, local de retirada combinado e frequência da coleta combinada. Salvar.
O modelo é o ponto de partida. Aplicado num cartão, ele vira uma cópia. Mudar o modelo depois não mexe no que já foi aplicado.
No lápis, eu edito o modelo: dá pra trocar a ordem dos itens e tirar item. E na lixeira, excluir. Das duas formas, os cartões que já receberam a lista não mudam.
Em Etiquetas, o caminho é parecido. Nova etiqueta, Indústria, com uma cor. Salvar.
Pra mudar o nome ou a cor, é o lápis. Agora, cuidado com a lixeira: excluir uma etiqueta tira ela de todos os cartões que usam.
São esses modelos que as regras e as automações usam: as ações Aplicar checklist e Adicionar etiqueta, e o checklist exigido pelo nome.
Uma dica: o modelo, a etiqueta e a pessoa que uma automação usa precisam continuar existindo. Se a ação não acha o que precisa, a automação falha e desfaz tudo: o cartão não muda de coluna, nem é criado.""",
8: """Com os modelos prontos, dá pra montar uma automação mais completa. Vou criar uma na Visita técnica.
O nome é Preparar a proposta, e o gatilho, Ao entrar nesta etapa. A primeira ação agora é Aplicar checklist.
Eu escolho o modelo Documentos do fornecedor. E no nome que vai pro cartão, uso de novo o marcador CLIENTE.
Ligando Criar tarefa vinculada, o checklist ganha uma tarefa com o mesmo nome. Concluiu a tarefa, o checklist fica marcado. Marcou o checklist inteiro, a tarefa fica concluída.
Adicionar ação. A segunda é Definir prazo do cartão: quinze dias corridos. Esse prazo é a previsão de fechamento, e ela é trocada quando a automação roda.
As ações Mover cartão e Copiar cartão pedem o funil e a etapa de destino. Uma dica: Mover cartão tem que ser sempre a última ação, e o destino nunca é a coluna de perdido.
Aqui eu não vou mover nada, então removo essa ação. E com as setas, eu troco a ordem das ações.
Ligo pra Ativa. Se faltar alguma coisa, o sistema avisa o quê, como o nome aqui. Preenchido, Salvar automação.
Na lista, cada automação tem o Editar, o botão de pausar, que desliga sem apagar, e a lixeira. Uma dica: a lixeira apaga na hora, sem perguntar.
E os outros gatilhos. Ao concluir uma tarefa e Ao concluir um checklist pedem o nome exato, letra por letra. E Quando tudo estiver concluído roda quando todas as tarefas do cartão estão encerradas e todos os itens de checklist, marcados.
Uma dica: se o cartão voltar e entrar de novo na etapa, a automação não cria tudo em dobro. Ela aproveita a tarefa e o checklist que já tinha criado.""",
9: """Com o funil pronto, o quadro já abre no Sucata industrial, com a Visita técnica no lugar certo.
A Metalúrgica Jequitibá ligou: gera retalho de chapa toda semana. Nova oportunidade. No título, Retalho de chapa da Metalúrgica Jequitibá. A etapa já vem em Novo. Esses dois são os obrigatórios.
O valor estimado: oito mil e quatrocentos reais por mês.
O responsável já vem preenchido com quem está criando. Por enquanto, eu deixo sem responsável.
Em Empresa, dá pra escolher um cliente ou fornecedor do cadastro. Escolhendo alguém dali, o contato, o telefone e o e-mail já vêm preenchidos. Mas a Metalúrgica Jequitibá ainda não é cadastrada, então eu uso o nome como empresa avulsa e preencho o contato eu mesmo: o Paulo Lacerda, de suprimentos, com telefone e e-mail.
Na operação, o material é chaparia. Se o material ainda não existe, dá pra usar o nome avulso, ou cadastrar ali no mais. A unidade vem do material. São uns doze mil quilos por mês, e a retirada é com a frota própria.
A data inicial marca quando a conversa começou. A previsão de fechamento é trinta de novembro. E nas observações, o que ela pediu: retirada a cada quinze dias, com caçamba.
Salvar, e o cartão aparece no Novo, com o material, o valor e a previsão. E o mais de cada coluna cria a oportunidade direto naquela etapa.
Quando o negócio fechar, a compra você lança no caixa, como sempre. O cartão guarda a história da negociação.""",
10: """Agora, andar com o cartão. O Paulo atendeu, então eu arrasto o cartão pela alça até Em contato.
Repara: a automação já criou a tarefa de agendar a visita. O cartão mostra uma tarefa aberta.
E se eu tentar levar pra Visita técnica agora? O sistema trava e mostra o que falta: Conclua as tarefas pendentes. Defina um responsável.
O cartão continua em Em contato, esperando.
Uma dica: quem manda é a regra da etapa de onde o cartão sai. E ela vale pra qualquer troca: avançar, voltar uma coluna ou mandar pro Perdido.
Pra destravar, é só resolver o que falta, na ficha do cartão.""",
11: """Clicando no cartão, abre a ficha da oportunidade, com três abas: Detalhes, Tarefas e Histórico.
Em Detalhes ficam o funil, o estágio e o responsável. Eu escolho o Rafael, o dono do ferro-velho, que vai cuidar dessa negociação.
Embaixo, o valor, a previsão, o material e a empresa. E as observações, que salvam sozinhas. É ali também que vai o motivo, se um negócio for pro Perdido.
Em Etiquetas, eu aplico a Indústria, que a gente criou nos modelos. Mais abaixo ficam os Checklists, que a gente vê daqui a pouco.
Na aba Tarefas está a tarefa que a automação criou: Agendar visita na Metalúrgica Jequitibá. A visita já foi marcada, então eu concluo.
E o Histórico guarda cada mudança de etapa, com quem fez e quando. A automação também fica registrada ali, com o nome dela.
Fechando a ficha, agora sim: o cartão passa pra Visita técnica.""",
12: """Repara no cartão. Quando ele entrou na Visita técnica, a automação Preparar a proposta aplicou o checklist e mudou a previsão pra vinte e cinco de novembro.
Na ficha, o checklist veio com o nome da empresa: Documentos da Metalúrgica Jequitibá.
Na visita, o Rafael vai marcando. CNPJ conferido, local de retirada, frequência da coleta. Cada clique já salva.
E a tarefa vinculada ficou concluída sozinha, porque o checklist foi todo marcado.
Sem automação, o caminho é o Aplicar modelo: escolhe o modelo, e a lista entra no cartão.
Aplicou a mais? A lixeira remove o checklist do cartão. Ela remove na hora, sem perguntar.
E o cartão mostra quantos itens já foram feitos.""",
13: """Ainda na ficha, dois campos que valem ouro. A Probabilidade é a chance de fechar. Todo cartão nasce com cinquenta por cento.
A visita foi boa, então eu subo pra oitenta.
E a Origem diz de onde veio o contato. É um texto livre, com o exemplo WhatsApp. Esse veio por telefone.
No cartão, a probabilidade vira uma barra: verde de setenta pra cima, amarela de quarenta a sessenta e nove, vermelha abaixo disso. Dá pra bater o olho e ver onde insistir.
Do lado direito ficam os comentários. Eu anoto o que foi combinado: Paulo pediu a proposta até sexta. Comentar. Fica com o meu nome e a hora, junto com as mudanças do cartão.
Pra não esquecer, Criar Tarefa, aqui mesmo. A oportunidade já vem ligada. Ligar pro Paulo, dia treze. Salvar.
Na aba Tarefas, os três pontinhos trazem as ações: editar, marcar em andamento, concluir, cancelar ou excluir. Uma dica: pra regra da etapa, tarefa cancelada conta como encerrada.
Pela ficha também dá pra mudar o estágio, sem arrastar, e a regra da etapa vale do mesmo jeito. E trocar o funil manda a oportunidade pra primeira etapa do outro funil.
Como o cadastro tem telefone, a ficha ganha o botão WhatsApp, que abre a conversa fora do sistema. E o Editar abre o cadastro completo, pra corrigir valor, contato ou material, com as tarefas no fim.
E a lixeira exclui a oportunidade. Uma dica: vão junto as tarefas e o histórico, e não tem volta. Negócio que não deu certo vai pro Perdido, não pra lixeira.
Fechando, o cartão já mostra os oitenta por cento e a origem.""",
14: """Agora, a aba Tarefas. Ela junta as tarefas de todas as oportunidades. No canban, cada coluna é uma situação: pendente, em andamento, concluída e cancelada.
Depois da visita, vem a proposta. Nova tarefa: Enviar proposta, ligada à oportunidade da Jequitibá, com o Rafael, pra quinta, dia doze, prioridade alta. Salvar.
Ela entra em Pendente. No canban, eu mudo a situação arrastando. Comecei a proposta, levo pra Em andamento.
Clicando na tarefa, abre a edição: dá pra pôr hora, descrição e lembrete. É aqui também que ela é excluída, e sai da Agenda junto.
Em Filtrar, dá pra separar por responsável, situação, prioridade e oportunidade. E a busca acha pelo título.
Na Lista, as mesmas tarefas viram uma tabela, com a oportunidade, o responsável, a data e a prioridade. Clicando no cabeçalho, eu ordeno.
E o Calendário mostra por mês, semana ou dia, cada tarefa no seu dia.
E a mesma tarefa aparece na Agenda, com o selo cê-érre-ême. Assim, ela entra na rotina do dia.
É uma tarefa só, nos dois lugares. Concluiu num, aparece concluída no outro.
Clicando nela, a Agenda leva direto pra oportunidade no cê-érre-ême. Uma dica: na Agenda dá pra concluir a tarefa; pra editar ou excluir, é na aba Tarefas do cê-érre-ême.""",
15: """Com o funil em uso, entram mais cartões. No fim do dia, a Recicla Vale já tem seis oportunidades no funil: sessenta e dois mil e trezentos reais no total.
Já são dezenove mil reais ganhos, com a Construtora Pilar, e quarenta e um mil seiscentos e cinquenta reais em negociação.
Na busca, dá pra achar pelo título, pelo contato, pela empresa ou pelo material. Digitando alumínio, sobra o cartão da Esquadrias Horizonte. E os cartões de cima passam a dizer filtrado.
Nos Filtros, dá pra separar por situação, por faixa de valor, por responsável, por material e por meio de transporte.
Quero ver o que está com o Rafael e ainda em negociação. O quadro se ajusta a cada escolha, e o Aplicar só fecha a janela. Ficam dois cartões: vinte e seis mil e duzentos reais.
Pra ver tudo de novo, é Limpar filtros.
Outro uso: em Status, Perdidos, pra rever o que não fechou. O motivo está nas observações do cartão.
O cartão fica onde eu soltar. Levo o da Elétrica Ponto Certo pra Em contato, em cima do outro, e a ordem se mantém. Assim, o mais urgente fica no topo.
E quando fecha? A Transportadora Caminho Firme aceitou a proposta. Arrasto pra Ganho, e os cartões de cima acompanham: vinte e três mil seiscentos e cinquenta reais ganhos, trinta e sete mil reais em negociação.""",
16: """Pronto! Recapitulando: o cê-érre-ême montou sozinho o Funil de vendas, e a gente conheceu as abas e os quatro cartões.
Criou o funil Sucata industrial, tornou padrão, pôs a Visita técnica no lugar e deu cor e orientação pra ela.
Ligou as regras de saída do Em contato e criou e ativou duas automações, uma que agenda a visita e outra que prepara a proposta, além do checklist e da etiqueta.
Cadastrou a oportunidade da Metalúrgica Jequitibá, viu a trava, resolveu na ficha e moveu o cartão. Marcou o checklist, ajustou a probabilidade e a origem, e comentou.
A tarefa apareceu na aba Tarefas e na Agenda, os filtros separaram o funil, e um negócio fechou arrastando pra Ganho.
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
           8: "Automação com várias ações.",
           9: "Nova oportunidade.",
           10: "Arrastar o cartão.",
           11: "A ficha da oportunidade.",
           12: "Checklist na oportunidade.",
           13: "Probabilidade, origem e tarefas.",
           14: "Tarefas e Agenda.",
           15: "Filtros, busca e fechar o negócio.",
           16: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "CRM",
           2: "CRM",
           3: "Funis",
           4: "Estágios",
           5: "Regras",
           6: "Automações",
           7: "Modelos",
           8: "Automações",
           9: "Oportunidades",
           10: "Kanban",
           11: "Oportunidades",
           12: "Oportunidades",
           13: "Oportunidades",
           14: "Tarefas",
           15: "Filtros",
           16: "Resumo"}

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
