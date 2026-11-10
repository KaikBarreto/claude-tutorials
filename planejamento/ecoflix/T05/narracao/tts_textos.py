# Texto enviado ao ElevenLabs (eleven_v4, Kaik Barreto) por capítulo do T5 "Balança e impressora: o EcoTray".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Driver -> "Dráiver" | EcoSistema -> "Ecossistema" | EcoTray -> "Ecotrêi" | PDF -> "pê-dê-éfe" | SmartScreen -> "smárti-scrím" | USB -> "u-ésse-bê" | driver -> "dráiver"
CAPS = {
0: """Oi! Neste tutorial a gente vai ligar o computador do escritório da Recicla Vale Metais na balança e na impressora do pátio.
Hoje, o Marcos lê o peso no visor da balança e digita no sistema. A balança marca trezentos e doze quilos, e no sistema entra trezentos e vinte e um.
E o comprovante abre num pê-dê-éfe, que ainda precisa mandar pra impressora.
Com o Ecotrêi, o peso entra sozinho e o cupom sai na hora.
A parte da balança depende do plano contratado. A da impressora funciona em qualquer plano.
Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. [pause] Vamos começar pelo que é o Ecotrêi.""",
1: """Tudo do Ecotrêi fica em Configurações, na aba Integrações.
Mas o que é o Ecotrêi? O Ecossistema roda no navegador. E o navegador, sozinho, não conversa com a balança nem com a impressora.
O Ecotrêi é um programa pequeno, instalado no computador onde elas estão ligadas. Ele faz a ponte.
A balança manda o peso pro Ecotrêi, e ele passa pro sistema. Na volta, o sistema manda o cupom, e o Ecotrêi entrega na impressora.
Ele funciona no Windows e no Mac, abre junto com o computador e fica num cantinho da tela, perto do relógio. Esse cantinho se chama bandeja.
Repara no selo: Ecotrêi não detectado nesta estação. Estação é o computador em que você está. Ainda não tem Ecotrêi aqui.
Embaixo ficam a impressora e a balança, cada uma com o botão Como funciona, que mostra o passo a passo. E tudo começa no Baixar Instalador.""",
2: """Vamos instalar. Clico em Baixar Instalador e escolho o sistema do computador. Aqui, Windows.
O download começa, e o navegador avisa que o arquivo pode ser perigoso.
Uma dica: esse aviso é normal com instaladores. O navegador fica desconfiado de programa pouco baixado.
Clico na setinha do aviso e escolho Manter.
Abrindo o arquivo, o Windows ainda mostra uma tela azul, a do smárti-scrím.
Clico em Mais informações e depois em Executar assim mesmo.
Abre o instalador do Ecotrêi. É só clicar em Instalar.
Ele baixa a versão mais nova, instala e cria um atalho na área de trabalho.
Pronto, instalado. E ele já fica configurado pra abrir sozinho toda vez que o Windows liga.
Clico em Fechar, e a janela do Ecotrêi abre. O ícone dele fica na bandeja, perto do relógio.
Nessa janela ficam as balanças, a impressora e o que o Ecotrêi fez por último. No tracinho, ela volta pra bandeja.
No Mac, o caminho é o mesmo: escolha a opção do Mac, abra o instalador e clique em Instalar. Lá, o Ecotrêi fica na barra de menus, no alto da tela.""",
3: """Com o Ecotrêi instalado, o sistema acha ele sozinho. Não tem código pra digitar nem endereço pra configurar.
Olha o selo: agora ele mostra a versão do Ecotrêi instalada neste computador.
Isso é o pareamento: o sistema e o Ecotrêi se reconhecem.
O sistema procura o Ecotrêi dentro do próprio computador. Por isso, ele vai instalado no computador em que a balança e a impressora estão ligadas.
E se um dia esse selo avisar que o Ecotrêi está desatualizado, é só fechar e abrir o Ecotrêi, que ele se atualiza.""",
4: """Agora a impressora. A impressora térmica, aquela de cupom, vai ligada no computador pelo cabo u-ésse-bê.
No sistema, eu ligo a Integração com Impressora. Pronto: Conectado ao Ecotrêi.
A lista traz as impressoras deste computador. Escolho a nossa, a de cupom.
Clico em Testar. O comprovante vai pra impressora, e o Ecotrêi avisa que imprimiu.
Na impressora sai um cupom de teste, com a data e a hora. Saiu o cupom? A ligação está funcionando. Mas repara: ele saiu cortado do lado.
Se a impressora não aparecer na lista, confira o cabo e clique em Atualizar.""",
5: """Aquele corte é a largura do papel. A bobina da impressora da Recicla Vale é a pequena, de cinquenta e oito milímetros, e o sistema vem com oitenta milímetros.
Com o papel mais estreito que o cupom, o lado sai cortado. Uma dica: cupom cortado quase sempre é a largura, e não a impressora.
Em Ajustar Escala, eu escolho cinquenta e oito milímetros. A prévia já mostra o cupom do tamanho da bobina.
O sistema manda essa largura pro Ecotrêi, e ele imprime exatamente nela. Então, se o cupom sair cortado, confira aqui primeiro.
A escala fina diminui o conteúdo dentro do papel, se precisar. Aqui fica em cem por cento.
Testar impressão manda um cupom de exemplo. Agora ele sai inteiro, então eu salvo.
E a impressão térmica turbo gera o comprovante mais rápido. Ela ainda está em teste: se algo sair diferente do normal, é só desligar.""",
6: """Agora a balança. Essa parte depende do plano contratado. Sem ela no plano, aqui aparece um cartão pra contratar, com o botão Pesar automático.
Uma dica: essa chave começa desligada, então ligue aqui pro peso começar a chegar. Na empresa em teste, a balança já vem liberada.
Ligada, o sistema avisa o Ecotrêi, e a balança fica liberada nele. Agora é cadastrar a balança lá.
Na janela do Ecotrêi, a área das balanças liberou. Clico em Configurar Balanças.
Ele procura sozinho a porta da balança, que é a entrada do cabo no computador, e marca com um tique.
Em Adicionar, dou um nome, Balança do pátio, e escolho a porta marcada.
O protocolo, que é o jeito de cada balança mandar o peso, fica no Automático. O Ecotrêi reconhece o modelo sozinho.
OK e Gravar. Pronto: a Balança do pátio aparece conectada.
De volta ao sistema, a Balança do pátio já está na lista, e o teste fica verde.
O Marcos põe na balança o saco de latinha da Dona Cida. Dezoito quilos e seiscentos, ao vivo, aqui no teste.
A unidade fica em quilo. As casas decimais dizem com quantos números depois da vírgula o peso entra no pedido. Aqui, três.
Com a leitura contínua ligada, depois de capturar, o peso segue mudando até você incluir. Desligada, ele fica fixo. Na Recicla Vale, fica desligada.
E repara: as chaves da impressora e da balança valem pro seu usuário. Se o Marcos usa esse computador com o login dele, ele liga também.""",
7: """Logo abaixo da chave da balança fica a opção Peso somente pela balança.
Imagina a carroça do Valdir na balança: trezentos e doze quilos. Com a opção ligada, ninguém digita outro número por cima. Só uma nova leitura da balança troca o peso.
E ela é uma regra da empresa: vale pra todos os usuários, em todos os computadores.
Vale a pena ligar quando todo peso da empresa passa pela balança integrada. Aí ninguém troca o peso na mão.
Com ela ligada, o peso entra só pela balança. Então, pra pesar, o Ecotrêi precisa estar aberto. Na Recicla Vale, por enquanto, ela fica desligada.""",
8: """Com a balança ligada no sistema, aparece um indicador no rodapé, em todas as telas.
Agora ele mostra Aguardando peso: o Ecotrêi está conectado, mas a balança não mandou peso nos últimos segundos. Normalmente, é a balança desligada.
O Marcos liga a balança, e a carroça do Valdir sobe: trezentos e doze quilos, ao vivo, com a bolinha verde.
E com o Ecotrêi fechado, ele mostra Balança desconectada. Isso a gente vê já já.
O indicador aparece pra quem tem a balança no plano e ligou a chave.
Uma dica: o peso ao vivo fica no computador do Ecotrêi. No celular, o sistema funciona normal, só sem esse indicador.""",
9: """E se o Ecotrêi fechar? Vamos ver. Clico com o botão direito no ícone dele e em Sair.
Na hora, o sistema avisa: Balança desconectada. E o rodapé mostra o mesmo.
Com o Ecotrêi fechado, o peso não chega e o cupom não vai pra impressora. Mas o sistema continua funcionando.
O comprovante abre em pê-dê-éfe, pra imprimir do jeito de sempre, e o peso você digita à mão. Com o Peso somente pela balança ligado, a pesagem espera o Ecotrêi voltar.
Aqui em Integrações, a impressora mostra Ecotrêi não encontrado.
Pra voltar, é só abrir o Ecotrêi. O atalho fica na área de trabalho.
E o sistema reconecta sozinho, em poucos segundos, sem atualizar a página. Se a impressora demorar, o Tentar conectar chama na hora.
Como o Ecotrêi abre junto com o Windows, no dia a dia é só ligar o computador.""",
10: """Por último, um aviso que evita cupom em branco. Imagina que instalaram outra impressora neste computador. Repara no triângulo amarelo do lado dela.
Dráiver é o programa que ensina o computador a falar com a impressora. Essa foi instalada com o dráiver genérico do Windows, que só imprime texto. E o cupom do sistema sai como imagem.
Escolhendo ela, o sistema avisa na hora: Dráiver incompatível. E o Ecotrêi segura a impressão, pra não sair folha em branco.
A saída é instalar o dráiver do fabricante da impressora. Até lá, use uma com o dráiver certo, como a nossa.
Volto pra nossa impressora de cupom, e o aviso some.
Uma dica: a impressora puxa o papel e ele sai em branco, sem nenhum aviso? Quase sempre é o dráiver também.
O sistema reconhece o dráiver genérico pelo nome. Com outro dráiver errado, a folha sai limpa, e a saída é a mesma: o dráiver do fabricante.""",
11: """Pronto! Recapitulando: a gente instalou o Ecotrêi, passando pelos avisos do navegador e do Windows, e viu o sistema se conectar com ele sozinho.
Ligou a impressora, fez o teste e acertou a largura do papel em cinquenta e oito milímetros.
Ligou a balança, cadastrou a balança do pátio no Ecotrêi e viu o peso chegando ao vivo.
Conheceu o Peso somente pela balança, o indicador do rodapé, o que acontece quando o Ecotrêi fecha e o aviso de dráiver incompatível.
No próximo tutorial, a gente abre o caixa e começa o dia. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que é o Ecotrêi.",
           2: "Baixar e instalar.",
           3: "O pareamento automático.",
           4: "Conectar a impressora.",
           5: "Largura do papel e impressão turbo.",
           6: "Conectar a balança.",
           7: "Peso somente pela balança.",
           8: "O indicador de peso.",
           9: "Quando o Ecotrêi cai.",
           10: "Dráiver incompatível.",
           11: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "EcoTray",
           2: "Instalação",
           3: "Conexão",
           4: "Impressora",
           5: "Impressora",
           6: "Balança",
           7: "Balança",
           8: "Balança",
           9: "Conexão",
           10: "Impressora",
           11: "Resumo"}

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
