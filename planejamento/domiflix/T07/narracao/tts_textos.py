# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T7 "O técnico em campo".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   BTUs -> "bê-tê-ús" | Check-in -> "Tchéquin" | Google Maps -> "Gúgol Méps" | Hi-Wall -> "rai-uól" | NPS -> "ene-pê-ésse" | PDF -> "pê-dê-éfe" | Waze -> "Uêiz" | check-in -> "tchéquin" | check-out -> "tchécaut" | psi -> "pê-ésse-i" | spray -> "isprei"
CAPS = {
0: """Oi! Neste tutorial a gente vai acompanhar uma ordem de serviço pelo celular do técnico, do trajeto até o cliente à entrega do relatório.
É assim que o trabalho de campo acontece: o técnico abre a ordem, preenche o atendimento, anota o material que usou e entrega o relatório ao cliente. Tudo no celular, com a ordem que a gente criou no tutorial anterior, e cada passo fica registrado na própria OS.
Se você ainda não viu o tutorial de Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo, dá uma olhada antes. [pause] Vamos começar pela agenda do técnico.""",
1: """Vamos abrir a ordem. O técnico começa pela agenda, onde ele vê as ordens dele e as da equipe dele. Aqui está a OS número dezesseis, do Colégio Monte Verde, às nove da manhã. Tocando nela, abre o resumo, com o cliente, o horário, o responsável e a descrição do serviço.
O botão que leva ao atendimento é o Preencher OS. Toco nele, e a ordem abre em tela cheia. No alto, a faixa da empresa mostra o número da OS, o serviço, a data e a hora, e o status, que por enquanto é Pendente.
Logo abaixo está o cartão Ir para o Atendimento, com os botões que a gente usa já já. Depois vêm os dados do cliente, com o telefone, o atalho de WhatsApp e o endereço, e a descrição do serviço.
Esse botão redondo, no canto da tela, é a Área do Técnico, a caixa de ferramentas de refrigeração. Ela fica disponível durante o atendimento, e é o assunto do próximo tutorial.
Uma dica: essa página é a mesma pro técnico, pro gestor e pro cliente. Quem abre o link sem fazer login vê a visão do cliente, e a gente chega nela no fim do tutorial.""",
2: """Com a ordem aberta, o primeiro passo é ir até o cliente. Toco em A Caminho. Na primeira vez, é só permitir a localização quando o celular perguntar: é ela que registra o local do tchéquin e coloca o técnico no mapa.
Pronto: o status mudou pra A Caminho, e o cartão agora é o Iniciar Atendimento. Enquanto a ordem está aberta no celular, a posição do técnico chega ao Mapa ao Vivo do gestor.
Logo abaixo aparece a Rota até o cliente. O mapa mostra o caminho, e o rótulo diz quantos minutos e quantos quilômetros faltam até o endereço.
Pra ver melhor, toco em Ampliar, e o mapa ocupa a tela toda. Fecho aqui no canto.
Os botões Uêiz e Gúgol Méps levam o trajeto direto pro aplicativo de navegação, com o endereço do cliente.
Uma dica: o A Caminho é opcional. Se o técnico já estiver no local, ele faz o tchéquin direto, a partir da ordem Pendente.""",
3: """Chegou ao local? Então é hora do tchéquin. Toco em Fazer Tchéquin. O celular registra a hora e o lugar do atendimento, e o status passa pra Em Andamento.
Logo abaixo do cabeçalho fica o carimbo do tchéquin: o dia, a hora e o endereço onde o técnico estava. Esses dados vão pro relatório do cliente.
Assim que o tchéquin é feito, a tela ganha o cartão de Checklists, com um checklist pra cada equipamento da ordem, e o rodapé preto, com Finalizar OS, Finalizar Parcial e o menu de mais ações.""",
4: """Com o atendimento iniciado, é hora do checklist. Cada equipamento da ordem tem o seu. Aqui é o rai-uól dezoito mil bê-tê-ús da sala dos professores, e o checklist é o de Manutenção preventiva de split, que a gente importou no tutorial de Tipos de Serviço, Tipos de Tarefa e Checklists. O contador mostra as perguntas respondidas: por enquanto, zero de treze.
As primeiras cinco perguntas são de Sim ou Não: filtros, serpentinas, dreno, fixações e conexões elétricas. O asterisco vermelho marca as obrigatórias. É só tocar no interruptor, e a resposta vira Sim.
Trabalhe com o celular conectado: cada resposta é gravada na hora, e se a internet cair o aplicativo avisa em vermelho que ainda não dá pra salvar.
Depois vêm as medições, em campos de número. Digito a corrente do compressor, sete vírgula seis ampères, a pressão de baixa, cento e dezoito pê-ésse-i, e a de alta, trezentos e quarenta e cinco pê-ésse-i. Por último, a temperatura de insuflamento, doze graus Celsius. Cada valor grava quando eu toco fora do campo.
No ruído e na vibração, marco Normal. Se precisar, dá pra marcar mais de uma opção.
Uma dica: pra mudar uma resposta, é só tocar no lápis. O contador vai subindo conforme o técnico responde: já são dez de treze.""",
5: """Algumas perguntas pedem foto. Aqui são dois botões: o Tirar Foto abre a câmera do celular, e a Galeria escolhe uma imagem que já está no aparelho.
Vou pela galeria. A foto sobe com uma barra de progresso, o aplicativo avisa quando ela foi enviada, e a miniatura aparece na pergunta, com a lixeira, se for preciso apagar.
Quando o checklist tem uma pergunta de vídeo, aparece o botão Gravar, pra registrar um clipe de até trinta segundos. O aplicativo deixa o vídeo mais leve antes de enviar.
A última pergunta antes da assinatura é de texto: as Recomendações ao cliente. O técnico escreve com as próprias palavras, toca fora do campo, e a resposta fica salva.""",
6: """Durante o serviço, o técnico anota os materiais que usou. Toco no menu de mais ações, aquele do rodapé, e escolho Consumir do estoque.
A própria janela já explica: o estoque só baixa quando a OS for finalizada. Até lá, o que o técnico anota é um rascunho que dá pra corrigir.
Em Material, dá pra procurar pelo nome ou pelo código, e cada um mostra quanto tem disponível. Escolho o Limpa-evaporador em isprei, coloco a quantidade, dois, e uma observação, se quiser. Toco em Adicionar, e o aplicativo avisa: Material anotado.
Faço o mesmo com a Fita isolante, um rolo. Os dois ficam na lista Já registrado nesta OS, e dali o técnico pode editar ou remover.
Toco em Fechar. E lembra do Consumo de estoque na OS, que a gente ligou em Configurações, na aba Usabilidade? É ele que libera essa opção no menu.""",
7: """Se o técnico precisar interromper o atendimento, ele pausa a ordem. No menu de mais ações, toco em Pausar OS. Pronto: a ordem fica Pausada, e o aplicativo avisa que é só retomar pra continuar o preenchimento.
O rodapé agora só tem o Retomar OS. Tudo que já foi preenchido continua salvo, e a ordem aparece em OS pausadas na agenda do gestor.
Quando voltar ao serviço, toco em Retomar OS, e o atendimento segue de onde parou.""",
8: """E quando a visita não pode terminar no mesmo dia, existe o Finalizar Parcial, o botão laranja do rodapé. Ele abre uma confirmação: a ordem fica marcada como Parcialmente Concluída e aparece em OS pausadas até ser concluída de verdade. O que já foi preenchido fica salvo.
Confirmo em Finalizar Parcialmente. O aplicativo avisa, fecha a ordem e volta pra agenda.
Na agenda, a ordem aparece em OS pausadas, com o tempo que faz que ela parou. Pra continuar, toco em Ver detalhes e depois em Preencher OS. O status agora é Parcialmente Concluída.
Toco em Retomar OS, e o técnico continua de onde parou.""",
9: """De volta ao atendimento, falta a assinatura do cliente, a última pergunta do checklist. Pra pedir a assinatura, a gente usa uma pergunta de assinatura no checklist, marcada como obrigatória: assim a OS só é concluída com ela.
O cliente assina com o dedo, direto na tela do celular. Quando ele começa a desenhar, aparecem o Limpar, pra recomeçar, e o Confirmar. E tem o Tela cheia, que abre o campo na horizontal, com mais espaço.
Toco em Confirmar, e o checklist do equipamento passa a Concluído. Pra rever a assinatura, é só tocar no lápis.""",
10: """Com tudo respondido, dá pra finalizar. Toco em Finalizar OS. Como o técnico anotou materiais, o aplicativo mostra antes o Resumo do consumo: o que vai sair do estoque e quanto fica de cada material.
Dá pra ajustar a quantidade aqui mesmo. Se a fita isolante foi de dois rolos, é só mudar o número, e o saldo que fica já se atualiza.
Confirmo em Confirmar e finalizar. O estoque baixa, a ordem é concluída, o aplicativo registra o tchécaut, com a hora e o local, e o técnico já cai no Relatório de Serviço.""",
11: """A ordem concluída vira o Relatório de Serviço. No alto estão o número da OS, o cliente e o equipamento atendido.
Em Execução ficam o tchéquin e o tchécaut, cada um com o nome de quem fez, a hora e o endereço. E logo abaixo, a duração do atendimento: uma hora e vinte e cinco minutos.
Mais abaixo vêm as respostas do checklist, equipamento por equipamento, com a foto que o técnico anexou e a assinatura do cliente, com data, hora e local.
No rodapé, o Baixar pê-dê-éfe gera o relatório em arquivo. No menu ao lado ficam o Copiar Link e o Imprimir.
Com o pê-dê-éfe baixado, é só enviar ao cliente pelo meio que você preferir, como e-mail ou WhatsApp.""",
12: """Falta o cliente receber o resultado. No menu do rodapé, toco em Copiar Link, e o aplicativo avisa: Link copiado. É só enviar esse link ao cliente: ele acompanha a ordem e baixa o relatório sem precisar de login.
Ele abre o link e vê a ordem como o cliente vê: o nome da empresa, o número da OS, o status Concluída e o mesmo relatório que o técnico tem, com o botão pra baixar o pê-dê-éfe.
Como a ordem está concluída, abre sozinha a pesquisa Como foi seu atendimento? O cliente escolhe uma nota de zero a dez, arrastando o controle. Depois dá estrelas pra cada critério da sua empresa e, se quiser, deixa o nome e um comentário.
Preencho com nota dez, cinco estrelas em cada critério, o nome e um comentário, e toco em Enviar avaliação. A avaliação é enviada, e o cliente recebe o agradecimento.
Essa avaliação chega pra você em ene-pê-ésse e Satisfação, na tela de Ordens de Serviço, que a gente viu no tutorial anterior. E enquanto o atendimento acontece, o mesmo link mostra o status em tempo real, com o técnico responsável e, quando ele está a caminho, a posição no mapa.""",
13: """Pronto! Recapitulando: o técnico abriu a ordem pela agenda, tocou em A Caminho, acompanhou a rota e fez o tchéquin quando chegou.
Depois preencheu o checklist do equipamento, com respostas, medições, foto e a assinatura do cliente, anotou os materiais que usou e viu como pausar e como finalizar parcialmente quando a visita não termina no dia.
Na finalização, conferiu o resumo do consumo, e o estoque baixou. A ordem virou um relatório, que dá pra baixar em pê-dê-éfe ou mandar por link, e o cliente avaliou o atendimento.
No próximo tutorial, a gente conhece a Área do Técnico de Refrigeração e Climatização, a caixa de ferramentas de apoio que fica a um toque do atendimento. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Abrindo a OS no celular.",
           2: "A Caminho e a rota.",
           3: "Tchéquin.",
           4: "O checklist do equipamento.",
           5: "Fotos e vídeo.",
           6: "Consumir do estoque.",
           7: "Pausar e retomar.",
           8: "Finalizar parcialmente.",
           9: "A assinatura do cliente.",
           10: "Finalizar a OS.",
           11: "O relatório e o pê-dê-éfe.",
           12: "O link do cliente.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Técnico em campo",
           2: "Técnico em campo",
           3: "Técnico em campo",
           4: "Técnico em campo",
           5: "Técnico em campo",
           6: "Técnico em campo",
           7: "Técnico em campo",
           8: "Técnico em campo",
           9: "Técnico em campo",
           10: "Técnico em campo",
           11: "Relatório",
           12: "Visão do cliente",
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
