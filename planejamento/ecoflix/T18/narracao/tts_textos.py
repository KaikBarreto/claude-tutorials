# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T18 "Ambiental: MTR e CDF" (app 1.60.22, aplicação de 21/11).
# Cada linha do texto é uma linha da tabela Tela x Fala do roteiro.md (o robô prende cada gesto a uma palavra da linha).
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Fiscal & Ambiental -> "Fiscal e Ambiental" | NF-e -> "/ˈẽniˈɛfiˈe/" | SEFAZ -> "sefás" | MTR -> "ême-tê-érre" | CDF -> "cê-dê-éfe" | PDF -> "pê-dê-éfe" | SIGOR -> "Sigôr" | IBAMA -> "Ibama"
# Palavra nova para testar na voz: "ONU" (cap06, linha 4).
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar da parte que mantém a licença da Recicla Vale Metais de pé: o manifesto de cada carga de resíduo e o certificado do destino.
Hoje sai uma carga de chaparia pra Aços Quiririm. E a Auto Peças Vale Forte espera o certificado das sucatas que mandou em outubro.
Tudo isso fica no menu Fiscal e Ambiental, em Ambiental.
O Ambiental faz parte do módulo de Notas Fiscais, então depende do plano contratado.
Se você ainda não viu o tutorial de transporte, serviço e o contador, dá uma olhada antes. [pause] Primeiro, o que é cada um.""",
1: """Aqui em Ambiental ficam as duas abas: ême-tê-érre e cê-dê-éfe. Em português claro, é assim.
Gerador é quem produz o resíduo. Transportador é quem leva. E destinador é quem recebe e dá o destino, como reciclar.
O ême-tê-érre, o manifesto de transporte de resíduos, acompanha a carga do gerador até o destino.
E o cê-dê-éfe, o certificado de destinação final, é o destinador confirmando que recebeu e deu o destino.
A Recicla Vale faz os dois papéis. Quando manda chaparia pra Aços Quiririm, ela é a geradora e emite o ême-tê-érre. Quando a Auto Peças Vale Forte manda sucata pra cá, ela é a destinadora e emite o cê-dê-éfe.
Uma dica: a ordem no tempo é sempre essa. Primeiro sai o ême-tê-érre, junto com a carga. Depois que o destinador recebe e dá baixa, sai o cê-dê-éfe, que cobre um período e junta os ême-tê-érre desse período. Um não substitui o outro.""",
2: """Por que isso importa? Quem trabalha com resíduo trabalha com licença ambiental.
E é pelo ême-tê-érre e pelo cê-dê-éfe que a empresa mostra pra onde foi cada carga. Numa fiscalização, os dois costumam ser pedidos juntos.
Uma dica: e se perguntarem se a sua empresa é obrigada a emitir? A resposta honesta é que quem define é o órgão ambiental do estado e a licença da empresa. O sistema entrega a ferramenta, e a interpretação da norma fica com eles.""",
3: """Antes do primeiro ême-tê-érre, um passo de configuração. Repara que o Novo ême-tê-érre ainda está desligado.
Uma dica: antes de qualquer emissão, precisam estar prontos o estado da empresa, nas Configurações Fiscais, e o acesso ao sistema ambiental do estado, que a gente configura agora.
Em Configurações, o sistema já vem pelo estado da empresa. A Recicla Vale é de São Paulo, então é o Sigôr.
Uma dica: em outro estado, a tela é a mesma, e o sistema também vem pelo estado da empresa. Nos estados que usam o sistema federal, no lugar do CPF e da senha entra o token de integração, que a gente gera no portal.
No Sigôr, o acesso é o do próprio usuário: o CPF da pessoa cadastrada no portal e a mesma senha que ela usa pra entrar. Aqui, o do Rafael.
O código da unidade geradora é o número que aparece no portal, ao lado do nome da empresa.
O ambiente fica em Produção. A opção Homologação é só pra teste.
Salvar acesso. Repara que o quadro avisa: acesso salvo, teste pendente. Então eu clico em Testar acesso salvo. Pronto: acesso validado, com a resposta do órgão e a data do último teste.
Se a senha do portal mudar, é só digitar a nova aqui, salvar e testar de novo. E se você esquecer a senha, a dica logo abaixo manda usar o Esqueci minha senha, na tela de login do portal.
Agora, Sincronizar dados do Sigôr. Ele traz as listas oficiais de resíduo, classe, unidade e tratamento, e com elas o Novo ême-tê-érre libera. Se o órgão mudar uma lista, é só sincronizar de novo.
Também aparecem os Resíduos salvos. A Recicla Vale manda muita sucata de ferro, então eu salvo esse resíduo uma vez só.
Código do Ibama, classe, estado físico, acondicionamento e tratamento vêm das listas do órgão. Quem confirma cada um é quem cuida da licença da empresa. [pause]
Repara que a unidade aparece do jeito que o órgão escreve, com a sigla na frente. Aqui, tonelada. Se um dia o resíduo for líquido, em litro ou metro cúbico, o campo Densidade passa a ser obrigatório.
Salvar resíduo. Na hora do ême-tê-érre, é só escolher.
Cada resíduo salvo pode ser editado ou excluído por aqui. Excluir não mexe nos manifestos que já saíram.
Uma dica: emitir e cancelar ême-tê-érre e cê-dê-éfe é uma permissão própria, a de documentos ambientais. Quem não tem continua vendo as listas e baixando o pê-dê-éfe, mas o botão de novo fica desligado.
Por último, em Materiais, eu marco os três ferros e ligo todos a esse resíduo. Na lista também tem a opção Nenhum, que tira a ligação, mas aqui eu escolho a sucata de ferro. Assim o ême-tê-érre consegue puxar a carga direto da nota fiscal. [pause]""",
4: """Hora de emitir. Hoje sai pra Aços Quiririm uma carga de chaparia de três mil e seiscentos quilos. Novo ême-tê-érre.
Ele abre em tela cheia, em três etapas: transporte e destino, resíduos e responsável. Aqui do lado, o resumo vai se preenchendo e avisa quantas etapas ainda faltam.
O transportador é a própria Recicla Vale, com o caminhão dela. Como é o primeiro ême-tê-érre, eu cadastro com a razão social, o CNPJ e o código da unidade no Sigôr. [pause]
O destinador é a Aços Quiririm, que vai reciclar o ferro. Aqui eu só digito o CNPJ e clico na lupa: a razão social vem sozinha. O código da unidade dela vem do cadastro dela no Sigôr. [pause]
Motorista e placa vêm da mesma frota do manifesto de transporte: o Jair, no caminhão três quartos. Se o motorista ou a placa forem novos, o botão de mais, ao lado do campo, cadastra na hora.
A expedição é hoje. Dá pra marcar um dia à frente, mas não pra trás.
Avançar. Nos resíduos, em vez de digitar, eu puxo da nota fiscal da carga. Busco a Aços Quiririm, marco a nota de hoje e clico em Conferir.
A prévia mostra o resíduo salvo e a quantidade já em tonelada: três vírgula seis. E a chave da nota vai pras observações.
Uma dica: dá pra marcar mais de uma nota, e o sistema soma tudo por resíduo. Se um material da nota não estiver ligado a um resíduo salvo, como o cobre desta outra nota, ele fica de fora, e a prévia avisa. [pause]
Usar no ême-tê-érre. A linha já vem com tudo que estava no resíduo salvo, e com a quantidade da nota. Se marcar a nota errada, o botão Desfazer tira tudo o que veio dela.
Avançar. No responsável, o Rafael, sócio-administrador. E a observação já leva a chave da nota.
Tudo pronto. Emitir ême-tê-érre. Pronto: o ême-tê-érre foi emitido no Sigôr, com o número oficial dele.
Uma dica: o ême-tê-érre e o cê-dê-éfe contam na mesma cota mensal das notas fiscais. Passando o mouse aqui no selo, aparece o seu nível, quantos documentos o mês permite e quantos você já emitiu. Perto do fim do mês, confira antes de emitir.""",
5: """Com o ême-tê-érre emitido, ele aparece na lista com o destinador, o resíduo, a data e o status: emitido.
Em Ver tentativas fica cada envio ao órgão, com a resposta dele. Aqui, um só, autorizado.
Baixar pê-dê-éfe. O pê-dê-éfe do ême-tê-érre abre pronto, e vai com o motorista, junto com a carga.
A lista guarda o histórico de todos os manifestos, cada um com o pê-dê-éfe dele. E pra próxima carga parecida, repara no ícone de Usar como modelo.""",
6: """À tarde sai outra carga pra Aços Quiririm, agora de ferro misto. Em vez de começar do zero, eu clico em Usar como modelo. Transportador, destinador, motorista e placa já vêm preenchidos, e a data é a de hoje.
Avançar. Nos resíduos, vem a mesma sucata de ferro. Eu só troco a quantidade: três vírgula dois toneladas.
Se a carga levar mais de um tipo de resíduo, o Adicionar resíduo cria outra linha, e cada linha pode partir de um resíduo salvo, mesmo sem nota fiscal. Pra esta carga uma linha basta, então eu tiro a segunda. [pause]
Pra resíduo perigoso no transporte, como bateria, os dados da ONU entram aqui, em Resíduo perigoso. Sucata de ferro não é o caso, então fica fechado. Cada resíduo ainda tem um campo de observação, que também é opcional.
Avançar. No responsável, já vem o Rafael. Uma dica: o modelo copia também a observação, com a chave da nota da carga anterior. Eu apago, porque esta carga tem outra nota.
Tudo pronto. Emitir ême-tê-érre. Pronto, o segundo manifesto do dia, em poucos cliques.""",
7: """Mais tarde, a Aços Quiririm pediu pra deixar essa carga de ferro misto pra semana que vem.
Essa carga não vai sair hoje, então o ême-tê-érre é cancelado. O botão de cancelar aparece no ême-tê-érre emitido.
O cancelamento vai pro sistema ambiental e não tem volta. Por isso, confira se é o ême-tê-érre certo.
Cancelar ême-tê-érre. Pronto, cancelado. Quando a carga sair, sai um ême-tê-érre novo.
Uma dica: o ême-tê-érre cancelado continua contando na cota do mês. Por isso, cancele só o que não vai mesmo sair.""",
8: """Nem todo envio passa de primeira. Olha a lista inteira: além do emitido e do cancelado, tem um com Erro, um com Confirmar no órgão e um Rascunho, que é o manifesto salvo, mas ainda não enviado.
No erro, o Ver tentativas mostra o que o órgão respondeu.
Daí são dois caminhos. Corrigir e tentar novamente abre o mesmo manifesto, pra arrumar o campo que o órgão recusou. E Tentar novamente reenvia do jeito que está. Como a data de expedição já passou, o sistema troca pra hoje.
Já o Confirmar no órgão quer dizer que o envio pode ter chegado lá, mas a resposta não voltou. Por isso a linha só tem o Ver tentativas: o sistema não deixa reenviar nem copiar esse manifesto.
Antes de qualquer coisa, confira no portal do órgão se o manifesto foi criado. Assim a mesma carga não sai com dois manifestos.""",
9: """Agora, o outro lado. Aqui no cê-dê-éfe, a Recicla Vale é a destinadora.
Em outubro, a Auto Peças Vale Forte mandou três cargas de sucata pra cá, cada uma com o ême-tê-érre dela. A Recicla Vale recebeu e deu baixa no Sigôr.
Agora sai um cê-dê-éfe só, que cobre outubro e junta os três.
Novo cê-dê-éfe. Ele também abre em tela cheia, com as cinco etapas em cima: dá pra clicar em qualquer uma pra voltar e conferir. No período, outubro inteiro. [pause]
O destinador é a sua empresa, quem recebeu o resíduo. O CNPJ já vem preenchido, a unidade dela no Sigôr aparece logo abaixo, e o responsável é o Rafael.
No gerador, a Auto Peças Vale Forte, com o CNPJ e a unidade dela no Sigôr.
Como o gerador já está informado, a lista de ême-tê-érre aqui é opcional: sem ela, o certificado sai pelo gerador e pelo período. Mas eu informo os números dos três ême-tê-érre que vieram com as cargas.
Repara no aviso: o cê-dê-éfe só junta ême-tê-érre que já foi recebido. Se faltar dar baixa em algum, isso é feito no portal do órgão, antes do cê-dê-éfe. Aqui também tem a observação, que consta no certificado.
E a emissão do cê-dê-éfe é definitiva. O resumo aqui embaixo ajuda a conferir tudo antes.
Emitir cê-dê-éfe. Pronto, o certificado foi emitido, com o número dele.
Na lista, cada cê-dê-éfe mostra o período, o CNPJ do gerador e o status. O menu de ações tem o que dá pra fazer com cada certificado.""",
10: """Com o certificado emitido, o pê-dê-éfe sai pelo menu de ações: Baixar pê-dê-éfe. O certificado abre pronto, pra salvar.
Uma dica: o cê-dê-éfe é documento de fiscalização. Guarde o pê-dê-éfe fora do sistema, na pasta da licença, e deixe os ême-tê-érre do mesmo período por perto.
Na fiscalização, os dois costumam ser pedidos juntos.""",
11: """O cê-dê-éfe também pode parar no caminho. Aqui tem um com erro, um rascunho e um emitido que ficou sem o pê-dê-éfe.
Em Ver erro aparece o motivo. Este é o mais comum: um dos manifestos ainda não teve a baixa do recebimento no portal.
Depois de dar a baixa lá no portal, é só clicar em Tentar novamente. Pronto, emitido, já com número.
O rascunho é um certificado que não chegou a ser enviado. Ele pode ser excluído, porque ainda não existe no órgão.
E quando um certificado fica emitido sem o pê-dê-éfe, o menu de ações mostra Gerar pê-dê-éfe, que busca o arquivo de novo.""",
12: """E como tudo isso conversa com a nota fiscal? A carga de chaparia de hoje tem a nota de venda dela, aqui em Notas Fiscais.
São três documentos da mesma carga, cada um com o seu papel. A nota fiscal é a venda, e vai pra sefás. O ême-tê-érre é o transporte do resíduo, e vai pro órgão ambiental.
E o cê-dê-éfe vem depois, do destinador, confirmando o destino.
Eles são independentes: cada um é emitido na sua tela. O que o ême-tê-érre aproveita da nota é o que a gente viu: os itens, pelo Puxar da nota fiscal, e a chave, na observação.
Assim você digita menos, e a nota e o ême-tê-érre da mesma carga ficam ligados pela chave.""",
13: """Pronto! Recapitulando: a gente configurou o acesso ao Sigôr, sincronizou as listas do órgão, salvou a sucata de ferro como resíduo e ligou os materiais a ele.
Emitiu o ême-tê-érre da carga de chaparia puxando da nota fiscal, acompanhou, baixou o pê-dê-éfe, usou esse manifesto como modelo pra carga seguinte e cancelou o que ficou pra depois.
Viu também o que fazer quando um envio dá erro ou fica pra confirmar no órgão.
E emitiu o cê-dê-éfe de outubro da Auto Peças Vale Forte, guardou o pê-dê-éfe junto da licença e viu como resolver um certificado com erro, rascunho ou sem pê-dê-éfe.
No próximo tutorial, a gente coloca a equipe do pátio dentro do sistema. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que é ême-tê-érre e cê-dê-éfe.",
           2: "Licença e fiscalização.",
           3: "Acesso e resíduos.",
           4: "Emitir o ême-tê-érre da carga.",
           5: "Acompanhar e baixar o pê-dê-éfe.",
           6: "O próximo manifesto mais rápido.",
           7: "Cancelar um ême-tê-érre.",
           8: "Quando o envio não passa.",
           9: "O certificado do destino.",
           10: "Baixar e guardar.",
           11: "Quando o certificado não sai.",
           12: "A nota da mesma carga.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Ambiental",
           2: "Ambiental",
           3: "Configuração",
           4: "MTR",
           5: "MTR",
           6: "MTR",
           7: "MTR",
           8: "MTR",
           9: "CDF",
           10: "CDF",
           11: "CDF",
           12: "Nota fiscal",
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
