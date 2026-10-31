# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T2 "Usuários, cargos e permissões".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   RH -> "érre-agá"
CAPS = {
0: """Oi! Neste tutorial a gente vai colocar a equipe dentro da Dominex, dando a cada pessoa exatamente o acesso de que ela precisa.
O técnico em campo precisa da agenda dele. Quem fica no escritório precisa da ordem de serviço, do orçamento e do financeiro. Cada um vê só o que faz parte do seu trabalho, e quem decide isso é você.
Se você ainda não viu o tutorial Configurações e identidade da empresa, dá uma olhada antes. [pause] Vamos abrir a tela de usuários.""",
1: """Os usuários ficam em Configurações, no rodapé do menu, do lado do Sair.
É a aba Usuários e Permissões. Aqui no alto, o contador mostra quantos usuários ativos a empresa tem e quantas vagas o plano oferece.
Por enquanto só a Camila, a administradora. A lista fica à esquerda. Ao clicar numa pessoa, o painel da direita mostra os dados e o que ela pode fazer.
Aqui em cima ficam dois botões. O Criar Usuário cadastra uma pessoa. O Configurações, de dentro desta aba, abre os cargos, que são os modelos de acesso. Antes de cadastrar as pessoas, vale montar os cargos.""",
2: """Clico em Configurações, e abre a janela de cargos, ainda vazia. Uma dica: o cargo é um modelo de acesso, que você monta uma vez e aplica em quantas pessoas quiser.
O primeiro é o cargo do técnico de campo. Dou o nome, Técnico de Campo, e uma descrição curta.
Embaixo fica o editor de permissões. As telas do sistema aparecem agrupadas por categoria, e cada tela tem o seu interruptor.
Imagina o que esse técnico precisa. A agenda dele, pra ver as visitas do dia. Então ligo a Agenda.
Esse zero de quatro mostra as ações que existem dentro da tela, e nenhuma está ligada. Clicando na seta, elas aparecem. O Ver Toda a Agenda, por exemplo, mostra as tarefas de todo mundo. O técnico só precisa das dele, então deixo desligado.
Ligo também a Área do Técnico, com as ferramentas de cálculo e de consulta que ele usa em campo.""",
3: """O técnico também trabalha na ordem de serviço, mas ele abre a ordem dele pela agenda ou pelo link. Não precisa da lista com todas as ordens da empresa. Por isso, na linha Ordens de Serviço eu não ligo a tela. Só abro a seta.
Ligo apenas a ação Editar OS em campo. Repara no aviso em itálico: a tela está desligada, mas a ação continua valendo por conta própria. É assim que o técnico preenche o checklist da ordem, sem ver as ordens do escritório.
Pronto, é só clicar em Criar Cargo. O Técnico de Campo aparece na lista, com três permissões.""",
4: """Agora o cargo de quem fica no escritório. Chamo de Escritório, com uma descrição do que a pessoa faz.
Pra achar uma permissão rápido, uso a busca. Ela ignora acento: se eu digito orcamento sem acento, ela acha Orçamentos do mesmo jeito. Ligo a tela.
Agora digito financeiro. A busca mostra a tela Financeiro e as ações dela. Ligo a tela e o Gerenciar Financeiro, que permite criar e editar lançamentos. O Excluir Lançamento Financeiro eu deixo desligado, porque ele fica à parte: só liga pra quem pode apagar lançamento.
Limpo a busca e ligo o resto do dia a dia do escritório: o Dashboard, a Agenda com a opção de ver toda a agenda, as Ordens de Serviço com criar e editar, os Clientes e Fornecedores com criar e editar, e os Equipamentos.
Criar Cargo, e os dois cargos estão na lista, cada um com o total de permissões. O lápis edita um cargo. Só um detalhe: quem já recebeu o cargo guarda uma cópia dele. Então, se você mudar o cargo depois, é só aplicar de novo nas pessoas.""",
5: """Com os cargos prontos, vamos cadastrar a equipe. O primeiro é o Rafael, técnico de campo. Clico em Criar Usuário. À esquerda ficam os dados da pessoa, e à direita, as permissões.
Escrevo o nome e crio uma senha. O indicador vai ficando verde conforme ela cumpre os requisitos: oito caracteres, um número, uma letra minúscula, uma maiúscula e um caractere especial. Com tudo verde, é uma senha forte.
Agora o e-mail: é com ele e a senha que o Rafael vai entrar. O telefone é opcional. Mais abaixo, o Vincular a Funcionário liga a pessoa ao cadastro do érre-agá, e eu deixo em Nenhum.
Em Tipo de Usuário, escolho Técnico. É isso que faz o Rafael aparecer na lista de técnicos da ordem de serviço, pra ser escolhido como responsável. Quem trabalha só no escritório fica como Interno.
Agora a parte prática. Em Perfis rápidos, clico no cargo Técnico de Campo, e as permissões ligam de uma vez: a Agenda, a Área do Técnico e a ação de editar a OS em campo. É só escolher o cargo aqui, porque é ele que define o que o técnico enxerga.
Criar Usuário, e o Rafael já está na lista, com o cargo Técnico de Campo embaixo do nome.""",
6: """A segunda pessoa é a Tatiane, que cuida do escritório. Preencho os dados do mesmo jeito e deixo o tipo como Interno, porque ela não sai pra campo.
Em Perfis rápidos, clico em Escritório, e as permissões do cargo ligam todas.
Agora imagina que só a Tatiane vá cuidar dos contratos. Procuro Contratos na busca e ligo a tela. Olha os chips: o Escritório apagou, e o Personalizado acendeu. Mexeu em qualquer permissão, o perfil vira Personalizado, e o cargo em si continua do jeito que estava.
Já o Acesso Total liga tudo de uma vez, inclusive as telas que a Dominex criar no futuro. É o perfil de quem administra.
Pra Tatiane, vale o cargo do jeito que ele é. Clico em Escritório de novo, e a seleção volta ao cargo.
Criar Usuário, e a Tatiane entra na lista com o cargo Escritório.""",
7: """Pra conferir o que cada pessoa pode fazer, é só clicar nela na lista. No painel do Rafael, o Perfil de acesso é o Técnico de Campo, e nos Dados do usuário aparece que ele é Técnico, com o telefone.
Mais abaixo, as Permissões concedidas: duas telas, a Agenda e a Área do Técnico, e uma ação, a Editar OS em campo. É exatamente o que a gente liberou no cargo.
O Editar abre a mesma janela do cadastro, já preenchida. Dá pra ajustar o telefone, o tipo ou as permissões a qualquer hora. Aqui eu só olho e cancelo.""",
8: """Agora, a prova de verdade: entrar como o Rafael, com o e-mail e a senha que a gente definiu. Ele já abre na Agenda.
Repara no menu: só a Agenda e a Área do Técnico. O menu dele tem apenas o que o trabalho pede. Cada pessoa vê só o que foi liberado.
A Área do Técnico, com as ferramentas de refrigeração, também está liberada pra ele. E, quando houver ordens pra ele, é pela Agenda que ele abre cada uma e preenche o checklist.""",
9: """E quando alguém sai de férias ou deixa a empresa? De volta como Camila, a lista já tem o resto da equipe: eu cadastrei os outros técnicos do mesmo jeito.
Vou usar o Paulo de exemplo. Olha o contador lá em cima: oito usuários ativos.
Clico em Desativar. O acesso dele é cortado, mas o cadastro fica guardado e a vaga do plano é liberada. O contador cai pra sete, e a etiqueta Inativo aparece na lista.
Quando ele voltar, é só clicar em Reativar. O Paulo volta com o mesmo cargo e as mesmas permissões, e o contador sobe de novo. Pra reativar, é só ter uma vaga livre no plano.
O Excluir é diferente: apaga a pessoa do sistema de vez, com acesso, permissões e vínculos. Pra só tirar o acesso, o caminho é o Desativar. Aqui eu cancelo.
Já na conta da própria Camila, aparece só o Editar. O Desativar e o Excluir ficam pros outros usuários. Uma dica: a empresa sempre fica com pelo menos um administrador ativo, que é quem cuida dos acessos.""",
10: """Pra fechar, as vagas do plano. No contador, o primeiro número é quantos usuários ativos você tem, e o segundo é quantas vagas o plano oferece.
Só quem está ativo ocupa vaga, e por isso o Desativar libera uma. Quando a equipe crescer além do plano, é na Assinatura, no menu da sua conta, que você aumenta o número de usuários. Isso a gente viu nas boas-vindas à Dominex.""",
11: """Pronto! Recapitulando: a gente montou dois cargos, o Técnico de Campo e o Escritório, ligando tela por tela e as ações de cada uma. E viu que uma ação pode valer mesmo com a tela desligada.
Depois cadastrou o Rafael e a Tatiane, aplicando o cargo com um clique, e viu que o perfil vira Personalizado quando se mexe numa permissão, e que o Acesso Total libera tudo.
Conferiu o que cada um pode fazer, entrou como o Rafael pra ver só o que foi liberado, aprendeu a desativar e reativar sem perder o cadastro, e entendeu as vagas do plano.
Com a equipe dentro, no próximo tutorial a gente cadastra os clientes, os fornecedores e os equipamentos. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Onde ficam os usuários.",
           2: "Montando um cargo.",
           3: "A ação sem a tela.",
           4: "O cargo do escritório.",
           5: "Cadastrando um técnico.",
           6: "Acesso Total ou personalizado.",
           7: "Conferindo o acesso.",
           8: "O que o técnico vê.",
           9: "Desativar e reativar.",
           10: "Vagas do plano.",
           11: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Usuários",
           2: "Cargos",
           3: "Permissões",
           4: "Cargos",
           5: "Usuários",
           6: "Permissões",
           7: "Usuários",
           8: "Permissões",
           9: "Usuários",
           10: "Usuários",
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
