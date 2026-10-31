# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T15 "Funcionários: Financeiro do Funcionário e Ponto Eletrônico".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 5: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Contas a Pagar/Receber -> "Contas a Pagar e Receber" | Funcionários / RH -> "Funcionários e érre-agá" | PJ/MEI -> "pê-jota ou mêi" | PDF -> "pê-dê-éfe" | CSV -> "cê-ésse-vê" | PIX -> "pix" | RH -> "érre-agá" | CLT -> "cê-éle-tê" | CBO -> "cê-bê-ó" | INSS -> "i-ene-ésse-ésse"
CAPS = {
0: """Oi! Neste tutorial a gente vai cuidar da equipe na Dominex: o cadastro de cada funcionário, o dinheiro do dia a dia, como vale, bônus e pagamento, e o ponto eletrônico pelo celular.
Com isso em dia, você sabe quanto cada pessoa tem a receber, e a folha do mês aparece sozinha nas contas a pagar.
A tela faz parte do módulo Funcionários e érre-agá. Com ele contratado, o item Funcionários aparece aqui no menu, em Gestão.
Se você ainda não viu o tutorial Notas Fiscais, dá uma olhada antes. [pause] Vamos conhecer a tela.""",
1: """As abas ficam aqui do lado. Em Funcionários fica a equipe, e em pê-jota ou mêi, os prestadores de serviço, cada um com o seu contrato.
As Equipes a gente montou no tutorial de ordens de serviço. E o Controle de Ponto é a segunda metade desta aula.
As três últimas são as ferramentas de érre-agá, que têm um tutorial só delas.
Na lista estão os seis técnicos da Glacial. Clicando num nome, a ficha abre aqui do lado, com as ações e os números da pessoa.
Agora, bora colocar alguém novo na equipe.""",
2: """A Tatiane, que cuida do escritório, já usa a Dominex desde o tutorial de usuários. Agora ela entra no cadastro de funcionários, pra receber o salário e bater o ponto.
A janela tem quatro abas: Dados, Pagamento, Ponto eletrônico e Perfil. A foto é opcional, e aparece na ficha e no ponto.
Em Dados vão o nome completo, o CPF, o telefone, o e-mail e o cargo, assistente administrativa.
Depois, o endereço e a data de admissão.
E a chave pix dela, aqui o e-mail. Ela fica guardada na ficha, à mão na hora de pagar.""",
3: """Agora a aba Pagamento. O salário da Tatiane é de dois mil e oitocentos reais.
Do lado fica o custo mensal total, que é quanto ela custa pra empresa. O Calcular monta esse número com o salário, os encargos e os benefícios, como o transporte.
Aplico, e o custo entra no cadastro. É esse custo que aparece na calculadora de mão de obra dos orçamentos.
No contrato de trabalho vai o regime. A Tatiane é registrada, então escolho cê-éle-tê.
O cê-bê-ó e a matrícula saem no holerite, e os dependentes entram no cálculo do imposto de renda.
Ela usa vale-transporte, de duzentos e vinte reais por mês, e o desconto dele também sai no holerite.""",
4: """Logo abaixo vem a configuração de pagamento: com que frequência e em que dia a pessoa recebe.
Dá pra pagar por mês, por quinzena ou por semana.
Na Glacial o pagamento é mensal, no quinto dia útil. Se preferir uma data fixa, é só trocar pra dia corrido e escolher o dia do mês.
Repara na dica: é essa configuração que faz a folha da Tatiane aparecer sozinha em Contas a Pagar.""",
5: """Falta ligar o cadastro ao login. Como a Tatiane já é usuária, é só vincular: escolho o nome dela aqui.
Pra quem ainda não tem login, o Criar acesso ao sistema cria um com o e-mail do cadastro. Depois, em Usuários e Permissões, é só aplicar o cargo da pessoa.
Clico em Criar Funcionário. Pronto, a Tatiane entrou na lista.""",
6: """Com a Tatiane cadastrada, eu completei os técnicos do mesmo jeito, cada um com o salário e o dia do pagamento. Agora, o dinheiro do dia a dia.
Clico no Rafael, e a ficha dele abre do lado. Em cima ficam as movimentações, e embaixo, os números, como o salário e o saldo atual, que é quanto ele tem a receber.
Imagina que o Rafael pediu um adiantamento de trezentos reais, em dinheiro. Clico em Vale, escolho de qual conta sai, aqui o caixa, e coloco o valor.
Registrar Vale. O vale sai do caixa na hora, porque o dinheiro já foi. E escolher a conta certa é o que faz a despesa cair no lugar certo do Financeiro.
O bônus é do mesmo jeito. Aqui, cento e cinquenta reais por produtividade.
E a falta. Em Descontar do salário, o valor de um dia já vem calculado pelo salário dele, cento e quarenta reais.
Repara no saldo atual: ele já desconta o vale e a falta e soma o bônus. O bônus e a falta ficam só no saldo e entram no dinheiro no dia do pagamento.""",
7: """Na hora de pagar, clico em Pagamento. A janela já abre no regime dele, o informal. O vale é descontado inteiro, e o dinheiro sai da Conta Principal.
Do lado, o resumo: o salário, mais o bônus, menos a falta e o vale. Ficam dois mil setecentos e noventa reais a pagar.
Confirmo, e ele pergunta se quero o recibo, que abre numa página pronta pra imprimir ou salvar em pê-dê-éfe. Agora eu deixo pra depois.
No Extrato fica cada movimento, com o saldo depois dele. E o Gerar Recibo, no pagamento, emite o recibo quando você quiser.
Na Tatiane, que é cê-éle-tê, a mesma janela abre no modo cê-éle-tê. Ela calcula o i-ene-ésse-ésse, o imposto de renda e o vale-transporte e mostra o líquido a pagar.
Ao confirmar, o holerite abre pronto pra imprimir. Uma dica: os descontos são uma estimativa, então confere com o seu contador antes de fechar a folha. O pagamento dela fica pro dia certo, então eu cancelo.""",
8: """Agora o ponto eletrônico, começando pelas regras. Em Controle de Ponto, na aba Config, fica a jornada padrão da empresa: das oito às cinco, com uma hora de intervalo.
Aqui você decide o que cada batida pede: a selfie e a localização. As duas já vêm ligadas, e na Glacial a gente fica só com a localização.
E pra quem faz plantão à noite, as batidas da madrugada contam no dia em que a pessoa começou a trabalhar.
Clico em Salvar configurações.
Se a equipe bate o ponto na empresa, tem o ponto em grupo: um link pra deixar aberto num tablet fixo, e cada um escolhe o próprio nome na lista.
E na Jornada Individual, cada pessoa pode ter o próprio horário, ou seguir o da empresa.""",
9: """Com as regras salvas, vamos ligar o ponto da Tatiane. Na ficha dela, clico em Editar e vou na aba Ponto eletrônico. É só ativar.
Com o ponto ligado, aparecem o PIN, que é opcional e protege a batida no tablet da empresa, e o acesso individual, com um link só dela.
Salvo, e o link de ativação já vem copiado. É só mandar pra ela. Uma dica: esse link vale por vinte e quatro horas.
No celular da Tatiane, o link abre o cadastro facial. A biometria é opcional, e aqui ela segue em Continuar sem biometria.
Abre o ponto dela, com o nome, o cargo e a marca da empresa. Ela bate o ponto sem login, só pelo link.
Ela toca em Registrar Entrada, o celular pega a localização e mostra o resumo: o tipo, o horário e o local.
Confirmar registro, e pronto, a entrada está registrada. O intervalo, a volta e a saída vêm depois, pelo mesmo botão.""",
10: """E do lado do escritório, você acompanha tudo na hora. Em Hoje, a Tatiane já aparece como presente, com o horário da entrada.
No olho ficam os registros do dia, com o endereço de cada batida.
Se alguém esquecer de bater, o lápis abre o registro manual. Você escolhe o tipo, a data e o horário e escreve a justificativa, que é obrigatória.
Em Histórico ficam as jornadas de todo mundo, com filtro por funcionário e por período, e o cê-ésse-vê leva tudo pra uma planilha.
E o Relatório mostra o mês inteiro num calendário, com as horas trabalhadas e o saldo de cada pessoa.""",
11: """E a folha do mês, quem lança? No dia seguinte, ela já está em Contas a Pagar e Receber. Procuro por folha na aba A Pagar.
Olha a folha de cada um, no valor do salário, vencendo no quinto dia útil do mês que vem. Ela entra sozinha pela configuração de pagamento, com antecedência pra você se programar.
Na hora de pagar, o Marcar como pago abre a mesma janela de pagamento, já quitando essa folha.
Como ela vence só no mês que vem, eu cancelo.""",
12: """Pronto! Recapitulando: a gente cadastrou a Tatiane com os dados, o salário, o custo mensal, o regime cê-éle-tê e o dia do pagamento, e vinculou o login que ela já tinha.
No Rafael, lançou um vale, um bônus e uma falta, pagou o salário com tudo descontado e viu o extrato.
Depois definiu as regras do ponto, ligou o ponto da Tatiane, que bateu a entrada pelo celular, e acompanhou tudo em Hoje, no Histórico e no Relatório.
E viu a folha de cada um aparecer sozinha em Contas a Pagar.
Com a equipe organizada, no próximo tutorial a gente conhece as ferramentas de érre-agá: o perfil comportamental, o organograma e o fluxograma. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A tela de Funcionários.",
           2: "Os dados da funcionária.",
           3: "Salário e contrato.",
           4: "O dia do pagamento.",
           5: "Acesso ao sistema.",
           6: "Vale, bônus e falta.",
           7: "O pagamento.",
           8: "As regras do ponto.",
           9: "O ponto no celular.",
           10: "Acompanhando o ponto.",
           11: "A folha em Contas a Pagar.",
           12: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Funcionários",
           2: "Cadastro",
           3: "Cadastro",
           4: "Cadastro",
           5: "Cadastro",
           6: "Financeiro do funcionário",
           7: "Financeiro do funcionário",
           8: "Ponto eletrônico",
           9: "Ponto eletrônico",
           10: "Ponto eletrônico",
           11: "Folha",
           12: "Resumo"}

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
