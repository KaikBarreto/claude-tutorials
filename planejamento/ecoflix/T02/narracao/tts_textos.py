# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T2 "Usuários e permissões".
# Cada linha do texto é uma linha da tabela Tela × Fala do roteiro.md (a vinheta de abertura não tem fala).
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   EcoSistema -> "Ecossistema" | NF-e -> "/ˈẽniˈɛfiˈe/" | NFS-e -> "/ˈẽːniˈɛːfiˈɛːsiˈeː/" (PERFIL 00:50: com espaço;
#   troca de N palavras para 1 no proc.py) | Fiscal & Ambiental -> "Fiscal e Ambiental" (nova)
CAPS = {
0: """Oi! Neste tutorial a gente vai colocar a equipe da Recicla Vale Metais dentro do Ecossistema, cada um com o acesso certo.
O Marcos pesa o material e opera o caixa, mas não precisa ver o lucro.
A Juliana cuida das contas e das notas, e não mexe no caixa.
O dono decide quem vê valor, quem abre caixa e quem não vê nada.
Se você ainda não viu o tutorial Sua conta e sua empresa, dá uma olhada antes. [pause] Vamos ver onde fica.""",
1: """Tudo começa nas Configurações, no rodapé do menu, do lado do Sair.
A equipe fica nesta aba aqui, Usuários e Permissões.
Em cima ficam o contador de usuários e o botão Criar Usuário. Por enquanto só tem um, o Rafael, o dono.
Clicando no nome, aparece o acesso de cada um. A coroa mostra que o Rafael é o master: o responsável pela conta da empresa.
E se alguém da equipe não acha esta aba? É que cada aba das Configurações tem a sua permissão.
A desta aqui se chama Gerenciar Usuários. Com ela ligada, e a tela Configurações também, a pessoa vê a aba e cuida da equipe.""",
2: """A equipe começa pelo Marcos, o balanceiro. Clico em Criar Usuário, e abre a janela do novo usuário.
Primeiro o nome completo: Marcos Antunes.
Depois o e-mail. É com ele que o Marcos vai entrar no sistema.
E a senha é você que define, aqui na hora. Repara que a tela mostra se ela está forte: oito caracteres, número, letra minúscula, maiúscula e um caractere especial.
Uma dica: a foto, coloca depois de criar, no Editar. É lá que ela fica gravada.
Depois de criar, é só passar o e-mail e a senha pro Marcos, e ele já entra. Agora, o que ele vai poder fazer.""",
3: """Do lado direito ficam as permissões. E pra não ligar uma por uma, tem os perfis rápidos.
São três. Pensa num chaveiro: cada perfil já vem com um conjunto de chaves.
O Acesso Total liga tudo, igual ao do dono.
O Somente Visualização libera as telas pra consultar, sem editar nem excluir.
E o Operador Padrão é o dia a dia do pátio: caixa, compra e venda, estoque e ticket de pesagem, sem as funções de administração.
É o que serve pro Marcos. E o perfil é só um ponto de partida: dá pra ajustar depois, chave por chave.
Criar Usuário. Pronto, o Marcos está na lista, ativo.""",
4: """Agora a Juliana, do escritório. Ela não se encaixa em nenhum perfil, então a gente monta o acesso dela na mão.
A lista é separada em grupos. Cada linha é uma tela do sistema, com o interruptor do lado.
Pensa assim: a tela é a porta, e as ações são o que a pessoa pode fazer lá dentro.
Pra Juliana, eu ligo a tela Contas a Pagar e Receber. Abro as ações dela e ligo duas: Criar Conta e Dar Baixa em Conta. O contador mostra duas de quatro.
Uma dica: primeiro a tela, depois as ações. Ligar só a ação não abre a tela. Com a tela Caixa desligada, o Registrar Venda sozinho não leva ninguém até o caixa.
Pra achar mais rápido, tem a busca. Digito nota, e aparece o Fiscal e Ambiental. Ligo a tela e as ações de emitir /ˈẽniˈɛfiˈe/ e /ˈẽːniˈɛːfiˈɛːsiˈeː/.
Do mesmo jeito, ligo o resto do escritório: o banco, o relatório financeiro, os pedidos e os clientes e fornecedores. O Caixa fica desligado.
Uma dica: duas travas mandam mais que qualquer chave daqui. A primeira é o plano. Tela de módulo que a empresa não contratou nem aparece nesta lista, nem pro dono. Sem o módulo de Funcionários, por exemplo, ninguém vê a tela de Funcionários.
A segunda é o próprio sistema, que confere a permissão de novo a cada operação, lá no servidor. Então não tem como contornar por fora.
Criar Usuário, e a Juliana entra na equipe.""",
5: """Agora os dois casos do pátio. Primeiro o balanceiro: o Marcos opera o caixa, mas o dono não quer que ele veja o lucro.
Aproveito e coloco a foto dele. No Editar, ela sobe na hora.
Na Tela inicial, escolho o Caixa. Assim, quando o Marcos entrar, ele já cai direto no caixa.
E se um dia ele esquecer a senha, é aqui também: no Nova Senha, você coloca outra.
Busco lucro, e aparece o Ver Projeção de Lucro, dentro do Caixa. Desligo.
Repara que o perfil virou Personalizado. Agora é o Operador Padrão com um ajuste.
Atualizar. O aviso lembra que o Marcos precisa entrar de novo pra ver a mudança. Ele continua comprando e vendendo. Só o lucro sai da tela dele.
E o escritório. A Juliana tem as contas, o banco, o relatório e as notas. A tela Caixa ficou desligada, então ela não abre nem fecha caixa.""",
6: """E quando alguém sai de férias, ou sai da empresa? No menu de cada usuário tem dois caminhos: desativar e excluir.
Desativar é como guardar o crachá: a pessoa fica sem acesso, e você devolve quando quiser. Excluir é rasgar o crachá.
Desativo o Marcos. Ele fica sem acesso, e tudo o que ele fez continua no sistema. E olha o contador: quem está desativado não conta no limite do plano.
Pra voltar, é o mesmo menu: Ativar. Pronto, o Marcos está de volta.
Já o Excluir apaga o acesso de vez, e não tem volta. Por isso a tela pede o e-mail da pessoa pra confirmar.
Aqui eu cancelo. No dia a dia, quem sai de férias ou deixa a empresa, você desativa.
E quem pode o quê? Desativar e ativar ficam com quem cuida desta aba. Excluir aparece só pro master. E o master não pode ser desativado nem excluído.
Nome, e-mail e senha de alguém, só o master ou a própria pessoa mudam.""",
7: """E o master? Ele é o responsável pela conta da empresa. Só ele exclui usuário e passa o controle pra outra pessoa.
Pensa num dono que vende o ferro-velho, ou num sócio que assume a empresa. É pra isso que serve o Tornar master.
No menu da pessoa, Tornar master. A janela explica o que muda: ela passa a ter o controle total, e a troca é na hora.
Uma dica: passe o controle só pra quem você confiaria a empresa inteira. Você continua com as suas permissões, mas perde a proteção: o novo master pode até desativar ou excluir a sua conta.
Aqui eu cancelo, e o Rafael continua como master.""",
8: """Agora o tamanho da equipe. O número de usuários depende do plano contratado. A Recicla Vale está com três de três: o Rafael, a Juliana e o Marcos.
Pensa em cadeiras: cada usuário ativo ocupa uma. Quem está desativado libera a dele.
Com todas ocupadas, o Criar Usuário abre esta janela.
Aqui você escolhe quantos usuários a mais quer. Cada usuário extra entra na mensalidade, e a tela já mostra a estimativa.
O Continuar calcula o valor certinho antes de você confirmar. Aqui eu só olho, e cancelo.""",
9: """Pra fechar, os valores. No topo da lista, no Geral, fica o Ver Totais e Valores Financeiros: o saldo do banco, os totais e o lucro.
Sem essa permissão, esses números aparecem escondidos, com pontinhos no lugar.
Agora imagina uma compra de mil quilos de ferro pesado, a noventa e cinco centavos o quilo. Quem compra precisa ver esse preço, senão não fecha o pedido.
Uma dica: esconder valor não trava a operação. O preço do material continua na compra e na venda. O que some é o consolidado: o lucro, os totais do período, o saldo do caixa e o do banco.
No Marcos, os valores do caixa ficam ligados, porque ele opera o caixa. Só a projeção de lucro está desligada.
E pra quem não pode ver nem o preço, como um ajudante que só pesa, o caminho é o Ticket de Pesagem.
Sem o Criar Ticket de Pesagem com Valores e sem o Ver Totais e Valores Financeiros, o ticket fica só com o peso. O valor, quem tem a permissão coloca depois.
Aqui não muda nada no Marcos, então eu cancelo.""",
10: """Pronto! Recapitulando: a gente achou a aba Usuários e Permissões, nas Configurações, e viu que ela depende da permissão Gerenciar Usuários.
Criou o Marcos com nome, e-mail e a senha definida na hora, e deu a ele o Operador Padrão.
Montou na mão o acesso da Juliana, tela por tela e ação por ação, sem o caixa.
Tirou a projeção de lucro do Marcos e colocou a foto e a tela inicial dele.
Desativou e ativou um usuário, viu que excluir não tem volta e que passar o controle pede confiança.
E entendeu o limite do plano e as permissões de valor.
No próximo tutorial, a gente monta o cardápio de materiais da Recicla Vale, com o preço de cada um. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Onde fica.",
           2: "Criar o usuário.",
           3: "Os três perfis rápidos.",
           4: "Telas e ações.",
           5: "O balanceiro e o escritório.",
           6: "Desativar ou excluir.",
           7: "Passar o controle.",
           8: "O limite de usuários.",
           9: "Esconder o valor.",
           10: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Usuários",
           2: "Usuários",
           3: "Permissões",
           4: "Permissões",
           5: "Permissões",
           6: "Usuários",
           7: "Master",
           8: "Plano",
           9: "Valores",
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
