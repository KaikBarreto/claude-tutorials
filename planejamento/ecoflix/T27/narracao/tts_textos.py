# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T27 "White Label".
# Cada linha do texto é uma linha da tabela Tela × Fala do roteiro.md (a vinheta de abertura não tem fala).
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   EcoSistema -> "Ecossistema" | White Label -> "uáit lêibou" | PDF -> "pê-dê-éfe"
#   A4 -> "á-quatro" | QR Code -> "quê-érre côde" (config: trocas "á-quatro" -> "A4", "quê-érre côde" -> "QR Code")
#   números: "cinco megas" -> legenda "5 MB"
#   1.60.22 (21/11): cap01 L3 (módulo), cap02 L6 (ícone padrão), cap03 L8-L9 (menu escuro, Seguir o tema), cap04 L4 (código com "#"),
#   cap05 L3, L5, L7, L8, cap06 NOVO "Desligar e voltar atrás" (antigos 6 e 7 viram 7 e 8), cap08 L5. Dica de desligar do cap05 saiu (vai no cap06).
CAPS = {
0: """Oi! Neste tutorial a gente vai deixar o Ecossistema com a cara da Recicla Vale Metais: o logo dela no menu, a cor dela, e os documentos sem o rodapé do Ecossistema.
Hoje, quem abre o sistema vê o logo do Ecossistema aqui no menu. E o comprovante sai com o rodapé do Ecossistema.
Com o uáit lêibou, a equipe e os parceiros passam a ver a marca da Recicla Vale.
O uáit lêibou é um módulo, então ele depende do plano contratado.
Se você ainda não viu o tutorial Sua conta e sua empresa, dá uma olhada antes. [pause] Vamos ver o que ele troca.""",
1: """O uáit lêibou fica nas Configurações, na aba Empresa, aqui na Identidade Visual.
Ele não tem tela própria: é esta gaveta aqui. Por enquanto, está desativado.
Se essa gaveta não aparece pra você, é porque o módulo uáit lêibou não está no seu plano. No período de teste, ele já vem liberado.
Ligado, ele troca o logo do menu, o ícone do menu recolhido e a cor principal. E tira o rodapé do Ecossistema dos documentos.
O endereço do sistema, a aba do navegador, os e-mails e a tela de login continuam os do Ecossistema. E é uma cor só: no tema escuro, o sistema usa a mesma cor, um pouco mais clara.""",
2: """Tudo começa pelas imagens. O logo horizontal a Recicla Vale já mandou, no tutorial da empresa. Com o uáit lêibou ligado, é ele que aparece no menu aberto.
Se a marca mudar um dia, é só clicar em Substituir e mandar a nova.
São duas imagens. O logo, comprido, vai no menu aberto. O ícone, quadrado, vai no menu recolhido, onde só cabe um quadradinho.
O ícone fica logo abaixo, no Ícone da Empresa. Ele também veio no tutorial da empresa.
Pra trocar, é o mesmo Substituir. A tela recomenda uma imagem quadrada, com fundo transparente.
E se você não mandar o ícone? O menu recolhido continua com o ícone do Ecossistema, mesmo com o uáit lêibou ligado.
Uma dica: as duas imagens podem ter até cinco megas. Arquivo maior, ou que não seja imagem, a tela recusa e avisa na hora.""",
3: """Com as imagens no lugar, é hora de ligar.
Uma dica: quem libera esse interruptor é o logo. Sem logo enviado, ele fica travado, e a tela pede o upload antes.
Ligo o interruptor. Pronto: uáit lêibou Ativo.
Olha o menu: o logo da Recicla Vale já entrou no lugar do logo do Ecossistema.
E o ícone? Ele aparece quando o menu está recolhido.
Uma dica: o ícone só aparece assim, com o menu recolhido e o uáit lêibou ligado. Com o menu aberto, quem aparece é o logo.
Abro o menu de novo, e volta o logo.
Mais uma dica: o menu do sistema é escuro. Logo de letra escura, com fundo transparente, quase some aqui. Mande uma versão que apareça bem no fundo escuro.
Ou, na aba Aparência, em Menu, escolha Seguir o tema. Aí o menu fica claro no tema claro.""",
4: """Agora a cor. Com o uáit lêibou ligado, aparecem as Personalizações.
O Nome Exibido no Sistema fica guardado aqui. Nas telas, quem mostra a marca é o logo e a cor.
Na Cor Primária, dá pra escolher no seletor ou digitar o código. Eu digito o do azul da Recicla Vale, e o quadradinho do lado já mostra como fica.
Uma dica: o código começa com o jogo da velha, como este. Sem ele, o sistema diz que salvou, mas a cor não muda, e não avisa.
Salvar Personalizações. Repara: os botões, os interruptores e a barrinha do menu já ficaram azuis.
Uma dica: com a Cor Primária vazia, o sistema volta às cores padrão. O Reset só limpa o campo. A volta vale depois do Salvar Personalizações.""",
5: """E onde a marca aparece? No menu, a gente já viu. No cabeçalho, o logo aparece pra quem usa o menu superior, e no celular.
Nos documentos, o que muda é o rodapé. O comprovante térmico, o á-quatro e os relatórios em pê-dê-éfe saem sem o rodapé do Ecossistema.
Vale também pra tabela de preços, pro ticket de pesagem, pro fechamento de caixa e pros outros relatórios.
Olha o comprovante de um pedido. Em cima, o logo da Recicla Vale, que já vinha desde o tutorial da empresa. E embaixo, acabou o rodapé do Ecossistema.
E, se você usa o quê-érre côde das fotos no comprovante, o logo da Recicla Vale vai no meio do quê-érre côde.
No Portal do parceiro, com a cor salva, o topo fica com a cor da Recicla Vale, e o rodapé do Ecossistema sai também.
E o comprovante que o parceiro baixa no Portal já sai sem o rodapé, mesmo sem cor salva.
No cadastro do rosto pro ponto, o funcionário também vê o logo e a cor da empresa. Já o logo da nota fiscal é outro: ele fica na Configuração Fiscal.""",
6: """E se um dia você quiser voltar atrás? Tem dois caminhos, e eles não fazem a mesma coisa.
O primeiro é o interruptor. Desligo, e o sistema avisa: uáit lêibou desativado.
O menu voltou pro logo do Ecossistema, e a cor voltou ao padrão.
Ligo de novo. A cor da Recicla Vale continuou guardada: voltou tudo, sem digitar nada.
O segundo caminho é remover o logo. A tela pergunta antes. Confirmo em Remover.
Repara: o menu voltou pro logo do Ecossistema, mas o uáit lêibou continua ativo. E a tela pede o logo de volta.
Ou seja, só remover o logo não desliga nada: os documentos continuam sem o rodapé do Ecossistema. Pra desligar de verdade, use o interruptor.
Agora eu mando o logo de novo, e está tudo no lugar.""",
7: """E a equipe? A troca vale pra empresa toda. Esse aqui é o sistema da Juliana, do escritório.
Mesmo logo, mesma cor, e ela não precisou mexer em nada.
Quando o uáit lêibou é ligado, ou a cor é salva, quem estiver com o sistema aberto vê a mudança na hora, sem sair e entrar de novo.
E quem muda o uáit lêibou é quem pode mexer na aba Empresa. A Juliana só vê o resultado.""",
8: """Pronto! Recapitulando: a gente achou o uáit lêibou na aba Empresa, viu o que ele troca e conferiu o logo e o ícone quadrado, que já tinham vindo do tutorial da empresa.
Ligou o interruptor, e o logo da Recicla Vale entrou no menu.
Salvou a cor da marca nas Personalizações.
Viu os documentos saindo sem o rodapé do Ecossistema.
Viu a diferença entre desligar no interruptor e só remover o logo.
E viu que a troca vale pra equipe toda, na hora.
No próximo tutorial, o parceiro acompanha tudo dele sozinho, sem precisar te ligar. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que muda.",
           2: "O logo e o ícone.",
           3: "Ligar o uáit lêibou.",
           4: "A cor da marca.",
           5: "Onde a marca aparece.",
           6: "Desligar e voltar atrás.",
           7: "A empresa toda, na hora.",
           8: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "White Label",
           2: "Marca",
           3: "White Label",
           4: "Cor",
           5: "Documentos",
           6: "White Label",
           7: "Equipe",
           8: "Resumo"}

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
