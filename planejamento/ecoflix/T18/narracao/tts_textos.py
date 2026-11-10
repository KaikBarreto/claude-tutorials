# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T18 "Ambiental: MTR e CDF".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Fiscal & Ambiental -> "Fiscal e Ambiental" | NF-e -> "/ˈẽniˈɛfiˈe/" | SEFAZ -> "sefás" | MTR -> "ême-tê-érre" | CDF -> "cê-dê-éfe" | PDF -> "pê-dê-éfe" | SIGOR -> "Sigôr" | IBAMA -> "Ibama"
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar da parte que mantém a licença da Recicla Vale Metais de pé: o manifesto de cada carga de resíduo e o certificado do destino.
Hoje sai uma carga de chaparia pra Aços Quiririm. E a Auto Peças Vale Forte espera o certificado das sucatas que mandou em outubro.
Tudo isso fica no menu Fiscal e Ambiental, em Ambiental.
O Ambiental faz parte do módulo de Notas Fiscais, então depende do plano contratado.
Se você ainda não viu o tutorial de transporte, serviço e o contador, dá uma olhada antes. [pause] Primeiro, o que é cada um.""",
1: """Gerador é quem produz o resíduo. Transportador é quem leva. E destinador é quem recebe e dá o destino, como reciclar.
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
No Sigôr, o acesso é o do próprio usuário: o CPF da pessoa cadastrada no portal e a mesma senha que ela usa pra entrar. Aqui, o do Rafael.
O código da unidade geradora é o número que aparece no portal, ao lado do nome da empresa.
Salvar acesso. E Testar acesso salvo: pronto, validado.
Agora, Sincronizar dados do Sigôr. Ele traz as listas oficiais de resíduo, classe, unidade e tratamento, e com elas o Novo ême-tê-érre libera.
Também aparecem os Resíduos salvos. A Recicla Vale manda muita sucata de ferro, então eu salvo esse resíduo uma vez só.
Código do Ibama, classe, estado físico, acondicionamento e tratamento vêm das listas do órgão. Quem confirma cada um é quem cuida da licença da empresa.
Repara que a unidade aparece do jeito que o órgão escreve, com a sigla na frente. Aqui, tonelada.
Salvar resíduo. Na hora do ême-tê-érre, é só escolher.
Por último, em Materiais, eu ligo os três ferros a esse resíduo. Assim o ême-tê-érre consegue puxar a carga direto da nota fiscal.""",
4: """Hora de emitir. Hoje sai pra Aços Quiririm uma carga de chaparia de três mil e seiscentos quilos. Novo ême-tê-érre.
O transportador é a própria Recicla Vale, com o caminhão dela. Como é o primeiro ême-tê-érre, eu cadastro com a razão social, o CNPJ e o código da unidade no Sigôr.
O destinador é a Aços Quiririm, que vai reciclar o ferro. O código da unidade dela vem do cadastro dela no Sigôr.
Motorista e placa vêm da mesma frota do manifesto de transporte: o Jair, no caminhão três quartos. E a expedição é hoje.
Avançar. Nos resíduos, em vez de digitar, eu puxo da nota fiscal da carga. Busco a Aços Quiririm, marco a nota de hoje e clico em Conferir.
A prévia mostra o resíduo salvo e a quantidade já em tonelada: três vírgula seis. E a chave da nota vai pras observações.
Usar no ême-tê-érre. A linha já vem com tudo que estava no resíduo salvo, e com a quantidade da nota.
Avançar. No responsável, o Rafael, sócio-administrador. E a observação já leva a chave da nota.
Tudo pronto. Emitir ême-tê-érre. Pronto: o ême-tê-érre foi emitido no Sigôr, com o número oficial dele.
Uma dica: o ême-tê-érre e o cê-dê-éfe contam na mesma cota mensal das notas fiscais. Perto do fim do mês, confira esse número antes de emitir.""",
5: """Com o ême-tê-érre emitido, ele aparece na lista com o destinador, o resíduo, a data e o status: emitido.
Em Ver tentativas fica cada envio ao órgão. Aqui, um só, autorizado. Se um envio der erro, a linha mostra o botão de tentar de novo.
Baixar pê-dê-éfe. O pê-dê-éfe do ême-tê-érre vai com o motorista, junto com a carga.
E pra próxima carga parecida, o Usar como modelo abre um ême-tê-érre novo com os mesmos resíduos.""",
6: """Mais tarde, a Recicla Vale emitiu pelo modelo o ême-tê-érre da carga de ferro misto da tarde. Só que a Aços Quiririm pediu pra deixar essa carga pra semana que vem.
Essa carga não vai sair hoje, então o ême-tê-érre é cancelado. O botão de cancelar aparece no ême-tê-érre emitido.
O cancelamento vai pro sistema ambiental e não tem volta. Por isso, confira se é o ême-tê-érre certo.
Cancelar ême-tê-érre. Pronto, cancelado. Quando a carga sair, sai um ême-tê-érre novo.
Uma dica: o ême-tê-érre cancelado continua contando na cota do mês. Por isso, cancele só o que não vai mesmo sair.""",
7: """Agora, o outro lado. Aqui no cê-dê-éfe, a Recicla Vale é a destinadora.
Em outubro, a Auto Peças Vale Forte mandou três cargas de sucata pra cá, cada uma com o ême-tê-érre dela. A Recicla Vale recebeu e deu baixa no Sigôr.
Agora sai um cê-dê-éfe só, que cobre outubro e junta os três.
Novo cê-dê-éfe. No período, outubro inteiro.
O destinador é a sua empresa, quem recebeu o resíduo. O CNPJ já vem preenchido, e o responsável é o Rafael.
No gerador, a Auto Peças Vale Forte, com o CNPJ e a unidade dela no Sigôr.
E os números dos três ême-tê-érre que vieram com as cargas.
Repara no aviso: o cê-dê-éfe só junta ême-tê-érre que já foi recebido. Se faltar dar baixa em algum, isso é feito no portal do órgão, antes do cê-dê-éfe.
E a emissão do cê-dê-éfe é definitiva. O resumo aqui embaixo ajuda a conferir tudo antes.
Emitir cê-dê-éfe. Pronto, o certificado foi emitido, com o número dele.
Na lista, cada cê-dê-éfe mostra o período, o gerador e o status. Se um der erro, o menu de ações mostra o erro e deixa tentar de novo.""",
8: """Com o certificado emitido, o pê-dê-éfe sai pelo menu de ações: Baixar pê-dê-éfe.
Uma dica: o cê-dê-éfe é documento de fiscalização. Guarde o pê-dê-éfe fora do sistema, na pasta da licença, e deixe os ême-tê-érre do mesmo período por perto.
Na fiscalização, os dois costumam ser pedidos juntos.""",
9: """E como tudo isso conversa com a nota fiscal? A carga de chaparia de hoje tem a nota de venda dela, aqui em Notas Fiscais.
São três documentos da mesma carga, cada um com o seu papel. A nota fiscal é a venda, e vai pra sefás. O ême-tê-érre é o transporte do resíduo, e vai pro órgão ambiental.
E o cê-dê-éfe vem depois, do destinador, confirmando o destino.
Eles são independentes: cada um é emitido na sua tela. O que o ême-tê-érre aproveita da nota é o que a gente viu: os itens, pelo Puxar da nota fiscal, e a chave, na observação.
Assim você digita menos, e a nota e o ême-tê-érre da mesma carga ficam ligados pela chave.""",
10: """Pronto! Recapitulando: a gente configurou o acesso ao Sigôr, sincronizou as listas do órgão, salvou a sucata de ferro como resíduo e ligou os materiais a ele.
Emitiu o ême-tê-érre da carga de chaparia puxando da nota fiscal, acompanhou, baixou o pê-dê-éfe e cancelou o ême-tê-érre da carga que ficou pra depois.
E emitiu o cê-dê-éfe de outubro da Auto Peças Vale Forte, com o pê-dê-éfe guardado junto da licença.
No próximo tutorial, a gente coloca a equipe do pátio dentro do sistema. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que é ême-tê-érre e cê-dê-éfe.",
           2: "Licença e fiscalização.",
           3: "Acesso e resíduos.",
           4: "Emitir o ême-tê-érre da carga.",
           5: "Acompanhar e baixar o pê-dê-éfe.",
           6: "Cancelar um ême-tê-érre.",
           7: "O certificado do destino.",
           8: "Baixar e guardar.",
           9: "A nota da mesma carga.",
           10: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Ambiental",
           2: "Ambiental",
           3: "Configuração",
           4: "MTR",
           5: "MTR",
           6: "MTR",
           7: "CDF",
           8: "CDF",
           9: "Nota fiscal",
           10: "Resumo"}

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
