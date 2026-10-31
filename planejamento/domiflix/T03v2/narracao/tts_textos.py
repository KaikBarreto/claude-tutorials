# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T3 v2 "Clientes, Fornecedores e Equipamentos" (Dominex 1.38.9).
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela x Fala.
# As linhas [mantém] são IDÊNTICAS, byte a byte, às do T3 gravado (exemplos/dominex-t3/narracao/tts_textos.py): reaproveitam o áudio.
# `python3 tts_textos.py diff` classifica cada frase em mantém/nova pelo texto do T3 e soma os caracteres de voz nova.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   QR Code -> "quê-érre côde" | QR -> "quê-érre" | Hi-Wall -> "rai-uól" | BTUs -> "bê-tê-ús" | Waze -> "Uêiz"
#   PMOC -> "pê-móqui" (testar na primeira geração; plano B: "pê ême ó cê")
#   "Sim ou Não" é a leitura de "Sim/Não" (rótulo do tipo de campo; a legenda volta para "Sim/Não" pelo config)
# Ajustes herdados do T3: cap. 2 "Com ela ligada"; cap. 3 "deixo o WhatsApp ligado"; cap. 12 "dá pra incluir a marca".
# Mapa v2 <- T3: 0<-0 | 1<-1 | 2<-2 | 3<-3 | 4<-4 | 5<-5 | 6 e 7 NOVOS | 8<-6 | 9<-7 | 10<-8 | 11<-9 | 12<-10 | 13<-11
CAPS = {
0: """Oi! Neste tutorial a gente vai deixar a base da sua empresa pronta no Dominex: os clientes, os fornecedores e os equipamentos que você atende.
Parece só cadastro, mas é daqui que saem as ordens de serviço, os contratos e até o quê-érre côde colado em cada aparelho. Então vale fazer com calma.
Se você ainda não fez as configurações iniciais da empresa, dá uma olhada antes no tutorial de introdução. [pause] Vamos começar pelos clientes.""",
1: """Os clientes ficam aqui no menu da esquerda, em Gestão, Clientes e Fornecedores.
A tela tem duas abas, Clientes e Fornecedores. Na aba Clientes, a lista fica na esquerda e a ficha abre do lado direito, sem sair da tela.
Olha: clico na Padaria Bom Grão e a ficha dela abre aqui do lado. Clico em outro cliente e ela troca na hora.
Cada linha mostra o documento, o telefone e a cidade. E esse selo diz se é pessoa jurídica ou pessoa física.
Pra achar alguém rápido, use a busca. Ela procura pelo nome, documento, telefone, cidade, e-mail e até pelo endereço.
Aqui em cima ficam os três botões que a gente vai usar hoje: Configurações, Formulários de captação e Novo Cliente. Vamos começar pelo Novo Cliente.""",
2: """Imagina que o Colégio Monte Verde te ligou pedindo um orçamento pros aparelhos da escola. Bora cadastrar.
A janela tem três abas: Contato, Fiscal e Portal. Quando o cliente é empresa, a dica é começar pela Fiscal, porque o CNPJ preenche quase tudo sozinho.
Eu digito o CNPJ aqui... e quando completa o último número, o sistema busca na Receita. Pronto: dados da empresa preenchidos.
Veio a razão social, o nome fantasia, o e-mail e o endereço completo. Repara que o endereço do cliente fica aqui na aba Fiscal, nesse bloco Endereço fiscal. É ele que aparece no mapa, na ordem de serviço e no orçamento.
Se faltar alguma coisa, como o complemento, é só completar.
Voltando pra aba Contato, o nome já veio preenchido e o tipo já tá como Pessoa Jurídica.
Agora o celular de quem cuida dos aparelhos lá. Com o número completo, libera essa opção: Receber mensagens pelo WhatsApp. Com ela ligada, o cliente passa a receber pelo WhatsApp os avisos de ordem de serviço, de cobrança e de vencimento.
Em Origem, eu marco de onde esse cliente veio. Esse aqui foi indicação. Já já a gente vê como organizar essa lista.
Em Observações vale anotar o que a equipe precisa saber antes de ir, tipo o horário em que dá pra entrar na escola.
A terceira aba é a do Portal, o link onde o cliente acompanha as ordens de serviço, os equipamentos e as cobranças. Ele já vem ligado, pronto pra usar. A gente vê isso no tutorial do Portal do Cliente.
Agora é só clicar em Criar. Pronto, cliente criado! Repara que a janela fecha e ele entra na lista, em ordem alfabética. Pra ver os detalhes, é só clicar nele.""",
3: """Agora um cliente pessoa física. O Marcos quer instalar um split no apartamento dele. Começo pelo nome... e troco o tipo pra Pessoa Física.
Coloco o celular, deixo o WhatsApp ligado, e depois o e-mail dele.
Ele chegou pelo Instagram. E se a origem não estivesse na lista, esse botão de mais do lado cria uma nova na hora, sem sair da janela.
Na aba Fiscal vai o CPF. É só digitar o número.
No endereço, eu começo pelo CEP. Completou os oito números, ele já traz a rua, o bairro e a cidade.
Aí eu completo o número e o complemento.
Criar. E pronto, mais um na lista. Uma dica: se você não sabe o CEP, dá pra digitar o nome da rua em Logradouro, que ele vai sugerindo os endereços.""",
4: """Lembra da Origem? Essa lista você monta do seu jeito, aqui em Configurações. Já tem Indicação, Instagram, Google e WhatsApp.
Vou criar mais uma: Site, pra quem chega pelo seu site. Adicionar, e pronto.
Pelo menu de cada uma dá pra editar ou excluir.
E por que isso importa? Porque marcando a origem de cada cliente, você descobre de onde estão vindo os seus clientes e onde vale a pena investir.""",
5: """Bom, agora que os clientes tão cadastrados, vamos ver a ficha. Clico no Colégio Monte Verde.
Em cima ficam o nome, a razão social e o menu Ações, com Editar e Excluir. E clicando no nome, dá pra pular pra outro cliente sem voltar pra lista.
No cartão Informações tá o que a gente preencheu. E esse ícone verde do lado do celular abre o WhatsApp do cliente direto.
Embaixo, o endereço com o mapa, e dois botões que o técnico adora: abrir no Google Maps ou no Uêiz.
Agora uma parte muito útil: o Responsável no Local. É a pessoa que o técnico procura quando chega lá, que nem sempre é quem contratou o serviço.
Na escola é o seu Antônio, o zelador. Coloco o nome, o cargo e o telefone... e Adicionar.
Pronto, ele aparece aqui, e nesse menu tem o WhatsApp dele, direto. Dá pra cadastrar quantos contatos quiser.
Do lado da Geral ficam as outras abas. Em Equipamentos, os aparelhos desse cliente, que a gente cadastra daqui a pouco. Em Histórico, todas as ordens de serviço. Em Tarefas, os lembretes da agenda. E tem ainda Estoque, Chamados, Contratos, Documentos, Financeiro e Cobranças. Cada uma tem o seu tutorial. O importante agora é saber que tudo desse cliente fica reunido aqui.""",
6: """Agora as etiquetas, que marcam clientes e fornecedores com uma cor.
Ficam aqui em Configurações, Etiquetas. Eu já deixei a Preferencial.
Imagina que o Colégio Monte Verde tem contrato de pê-móqui: Nova etiqueta, escrevo Contrato pê-móqui, escolho a cor e Salvar etiqueta.
Pra usar, na ficha do Colégio Monte Verde, Ações, Editar, e em Etiquetas marco a nova e a Preferencial: dá pra marcar mais de uma. Salvar.
Pronto: elas aparecem na ficha e na lista. E em Filtros dá pra ver só os clientes de uma etiqueta.""",
7: """Agora os campos personalizados, pra guardar uma informação extra do cadastro.
Lembra do horário em que dá pra entrar na escola? Clico em Novo campo, escrevo Horário de acesso e deixo o tipo Texto. Salvar campo.
Os outros tipos são Número, Data, Lista de opções e Sim ou Não. E dá pra deixar obrigatório ou mostrar no Portal do Cliente.
Os fornecedores têm os campos deles: é só trocar aqui em cima.
Pra preencher, Ações, Editar, escrevo o horário e Salvar. Ele aparece no cartão Informações.""",
8: """Agora uma coisa que economiza muito tempo. Em vez de você digitar o cadastro, o próprio cliente preenche. Você manda um link pelo WhatsApp, coloca na bio do Instagram, e ele mesmo se cadastra.
Clico em Novo formulário e dou um título.
Na aba Campos eu escolho o que o cliente vai preencher e o que é obrigatório. Nome e celular, obrigatórios. O endereço, opcional.
E na aba LGPD fica o texto de consentimento, que o cliente precisa aceitar antes de enviar. Já vem pronto, mas dá pra ajustar.
Salvo, e o formulário já tá ativo.
Agora é copiar o link e mandar pro cliente.
É isso que o cliente vê quando abre o link. Ele preenche, aceita o termo e envia.
E de volta no Dominex, a Luana já tá na lista de clientes. O cadastro entra direto, na hora. E o formulário vai contando quantas pessoas se cadastraram por ele.""",
9: """Agora os fornecedores, que ficam aqui na aba do lado. É quem vende pra você: a loja de peças, o distribuidor de gás, o fabricante.
O botão pra cadastrar fica aqui em cima, do lado direito: Novo Fornecedor.
O cadastro é bem simples: o nome, o CNPJ, a pessoa que te atende, telefone, e-mail e endereço. Nas observações eu anoto o que compro dele.
Lá em cima, em Etiquetas, escolho a Preferencial.
Salvar.
Na ficha ficam os dados e o Histórico de Gastos. Toda despesa que você lançar no Financeiro escolhendo esse fornecedor aparece aqui, com o total gasto. Assim você sabe quanto compra de cada um.""",
10: """Agora os equipamentos. Eles ficam em Gestão, Equipamentos. Cada equipamento é um aparelho instalado num cliente, e é nele que fica guardada cada manutenção.
Antes de cadastrar, vale decidir quais informações você quer guardar de cada aparelho. Em Configurar Campos estão os que já vêm prontos: marca, modelo, número de série, capacidade, local e data de instalação. Dá pra renomear, esconder ou mudar a ordem.
E dá pra criar os seus. Eu sempre quero saber a tensão do aparelho, então crio o campo Tensão, do tipo lista de opções: cento e vinte e sete, duzentos e vinte e trezentos e oitenta volts.
Marco como obrigatório. Repara que cada mudança já grava sozinha. Agora as categorias.
Em Categorias, a gente separa os tipos de aparelho. Já tem rai-uól, Cassete e Piso-Teto. Vou criar Multi Split, escolho uma cor e clico no mais.
Por último, as Etiquetas dos equipamentos: crio Em garantia, escolho uma cor e Salvar etiqueta.""",
11: """Agora sim, o equipamento. Novo Equipamento.
Primeiro o cliente: Colégio Monte Verde.
As etiquetas do cliente aparecem aqui, na hora de escolher.
No nome, a dica é juntar o tipo e o lugar, assim o técnico acha rapidinho: rai-uól dezoito mil bê-tê-ús, sala dos professores. Categoria, Split rai-uól.
Logo abaixo, em Etiquetas, escolho Em garantia.
Marca, modelo, número de série, capacidade, o local e a data em que ele foi instalado.
E olha o campo que a gente criou: Tensão, com asterisco porque é obrigatório. Duzentos e vinte.
Tem ainda a validade da garantia. E o identificador o sistema gera sozinho quando salva.
Criar. Pronto!
Agora um atalho. Às vezes você tá cadastrando o aparelho e o cliente ainda nem existe no sistema. Não precisa sair daqui: digita o nome, clica no mais e cria o cliente só com o nome. Depois você completa o cadastro dele com calma.
Termino o aparelho e crio.
E lembra da aba Equipamentos na ficha do cliente? O aparelho já tá lá. Se você cadastrar por aqui, o cliente já vem escolhido.""",
12: """Clicando no aparelho, abre a ficha dele.
Aqui ficam todas as informações e o quê-érre côde do equipamento. Esse quê-érre é o que vai colado no aparelho.
Em Gerar Etiqueta você escolhe o que sai impresso: o nome e o telefone da sua empresa, o quê-érre côde, o nome do aparelho e o identificador. Se quiser, dá pra incluir a marca, o modelo e o cliente. Escolhe o tamanho e já vê como fica.
Aí é só clicar em Imprimir. Uma dica: na janela de impressão, deixa o dimensionamento em tamanho real.
Se preferir mandar pra uma gráfica, o Baixar quê-érre salva a imagem.
E pra que serve esse quê-érre? Quando o cliente ou o técnico aponta a câmera do celular, abre o portal do cliente já nesse aparelho, com o histórico de manutenção. A gente mostra isso em detalhe no tutorial do Portal do Cliente.
Na aba Anexos você guarda o manual, a nota de compra, as fotos da instalação. Repara que o que você anexa aqui também aparece pro cliente no portal.
Em Histórico ficam as ordens de serviço feitas nesse aparelho. E aqui embaixo dá pra deixar uma listinha de pendências dele, tipo trocar as pilhas do controle.""",
13: """Pronto! Recapitulando: a gente cadastrou um cliente empresa pelo CNPJ e um cliente pessoa física pelo CEP, organizou as origens e colocou o responsável no local com WhatsApp. Marcou os clientes com etiquetas coloridas e criou o campo Horário de acesso. Criou um formulário pro cliente se cadastrar sozinho, cadastrou um fornecedor e deixou os equipamentos prontos, com categoria, campo personalizado e etiqueta com quê-érre côde.
Com essa base, abrir uma ordem de serviço fica muito mais rápido, porque o cliente e o aparelho já estão no sistema.
No próximo tutorial, a gente cadastra os tipos de serviço, os tipos de tarefa e os checklists, que é o que o técnico preenche em cada visita. Até lá!""",
}
TITULOS = {1: "A tela de Clientes.",
           2: "Cliente empresa pelo CNPJ.",
           3: "Cliente pessoa física pelo CEP.",
           4: "Origens.",
           5: "A ficha do cliente.",
           6: "Etiquetas.",
           7: "Campos personalizados.",
           8: "Formulário de captação.",
           9: "Fornecedores.",
           10: "Preparando os equipamentos.",
           11: "Cadastrando um equipamento.",
           12: "quê-érre côde e etiqueta.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Clientes",
           2: "Clientes",
           3: "Clientes",
           4: "Clientes",
           5: "Clientes",
           6: "Clientes",
           7: "Clientes",
           8: "Clientes",
           9: "Fornecedores",
           10: "Equipamentos",
           11: "Equipamentos",
           12: "Equipamentos",
           13: "Resumo"}

if __name__ == "__main__":
    import re
    import sys

    def frases(texto):
        """Quebra em frases como o capNN.json do T3 (ponto, exclamação, interrogação e dois-pontos)."""
        return [f for f in re.split(r"(?<=[.!?:])\s+", texto.replace("[pause]", " ").replace("\n", " ")) if f.strip()]

    if len(sys.argv) > 1 and sys.argv[1] == "diff":
        import importlib.util
        import os
        aqui = os.path.dirname(os.path.abspath(__file__))
        t3 = os.path.join(aqui, "..", "..", "..", "..", "exemplos", "dominex-t3", "narracao", "tts_textos.py")
        spec = importlib.util.spec_from_file_location("t3", t3)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        MAPA = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: None, 7: None, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 11}
        novos_total = 0
        for k, v in CAPS.items():
            antigas = set(frases(mod.CAPS[MAPA[k]])) if MAPA[k] is not None else set()
            novas = [f for f in frases(v) if f not in antigas]
            ch = sum(len(f) for f in novas)
            novos_total += ch
            print(f"cap {k:2d} (T3 {MAPA[k] if MAPA[k] is not None else '--':>2}): {len(novas):2d} frases novas, {ch:4d} caracteres")
            for f in novas:
                print(f"        + {f}")
        tit_novos = sum(len(TITULOS[k]) for k in (6, 7))
        print(f"voz nova nos capítulos: {novos_total} | títulos novos (6 e 7): {tit_novos} | soma: {novos_total + tit_novos}")
    else:
        tot = 0
        pal = 0
        for k, v in CAPS.items():
            w = len(v.replace("[pause]", "").split())
            tot += len(v)
            pal += w
            print(f"cap {k:2d}: {len(v):5d} chars, {w:4d} palavras, ~{w / 2.6:5.1f} s")
        tit = sum(len(v) for v in TITULOS.values())
        print("total chars CAPS", tot, "| TITULOS", tit, "| soma", tot + tit, "| palavras", pal, f"| ~{pal / 2.6 / 60:.1f} min de fala")
