# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T16 "Nota Fiscal de mercadoria (NF-e)".
# Gerado do roteiro.md (coluna Fala): cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   Fiscal & Ambiental -> "Fiscal e Ambiental" | NFS-e -> "ene-éfe-ésse-ê" | NF-e -> "ene-éfe-ê" | CC-e -> "cê-cê-ê" | EcoSistema -> "Ecossistema" | SEFAZ -> "sefás" | CFOP -> "cê-éfe-ó-pê" | ICMS -> "i-cê-eme-ésse" | DANFE -> "dânfi" | NCM -> "ene-cê-ême" | XML -> "xis-ême-éle" | PDF -> "pê-dê-éfe" | MTR -> "ême-tê-érre" | CDF -> "cê-dê-éfe" | DRE -> "dê-érri-ê" | IBS -> "i-bê-ésse" | CBS -> "cê-bê-ésse" | A1 -> "á-um" | pfx -> "pê-éfe-xis"
# Novas desta aula (testar num trecho curto antes): CC-e, A1, pfx, IBS, CBS, Fiscal & Ambiental.
CAPS = {
0: """Oi! Neste tutorial a gente vai do certificado digital até a nota fiscal autorizada, na Recicla Vale Metais.
A Fundição Bandeira do Vale compra cobre dela toda semana. E a carga só sai do pátio com a nota fiscal de mercadoria, a ene-éfe-ê.
As notas fazem parte do módulo Notas Fiscais. Se ele estiver no seu plano, tudo fica em Fiscal e Ambiental.
Se você ainda não viu o tutorial Relatório Financeiro e dê-érri-ê, dá uma olhada antes. [pause] É a parte mais delicada do sistema, então a gente vai devagar e na ordem.""",
1: """Tudo começa no menu, em Fiscal e Ambiental.
Aqui ficam as telas fiscais: as notas de mercadoria, as de serviço, o transporte, o ambiental e o estoque fiscal. Hoje a gente fica nas notas de mercadoria.
Clico em Notas Fiscais, ene-éfe-ê.
Em cima ficam as sub-abas: Entrada, Saída, Notas Recebidas e Inutilizadas.
Saída é a nota da venda, quando a mercadoria sai do pátio pro cliente. Entrada é a da compra, quando ela chega do fornecedor.
Do lado direito ficam as Configurações Fiscais e a cota do mês. Embaixo, os cartões das notas emitidas, pendentes e rejeitadas ou canceladas. E o botão Nova Nota.""",
2: """Antes de qualquer nota, a configuração. Ela fica no botão Configurações Fiscais e é tudo o que a sefás, a Secretaria da Fazenda do estado, precisa saber antes da primeira nota.
Na esquerda ficam as seções, em três grupos: emissão, regras fiscais e documentos.
Repara que Empresa, Impostos, Numeração e Transportadora estão apagados, com o aviso precisa do certificado digital.
É o certificado digital que assina a nota, como a assinatura da empresa. Sem ele, nada do que for preenchido aqui chega na sefás.
Por isso a ordem está na própria tela. Passo um, o certificado. Passo dois, os dados da empresa. Passo três, os impostos.
Uma dica: faça essa configuração junto com o contador. Um campo errado aqui faz a sefás recusar a nota na hora de emitir.""",
3: """Então, o certificado. A ene-éfe-ê usa o certificado á-um, que é um arquivo de computador com uma senha.
Em Arquivo do Certificado, clico em Selecionar arquivo e escolho o arquivo ponto pê-éfe-xis da Recicla Vale.
Em Senha do Certificado vai a senha do próprio arquivo, e não a senha da empresa.
Clico em Validar Certificado. Pronto: certificado validado.
Embaixo aparece até quando ele vale: catorze de setembro de dois mil e vinte e sete.
Uma dica: o á-um vale no máximo um ano. Se a tela disser que a validade não confere, quase sempre foi enviado o arquivo errado, o da certificadora, e não o do CNPJ.
Aí é pedir o arquivo certo ao contador e usar o Substituir Certificado. E o botão Próximo leva pra empresa.""",
4: """Com o certificado validado, os dados da empresa. É o passo dois.
O Importar dados traz o que já está no cadastro da empresa: o nome, o CNPJ, o telefone e o e-mail.
Confiro a razão social completa e digito a inscrição estadual. O CNPJ daqui é o que vai como emitente em toda nota.
O endereço fiscal vem do cadastro da empresa, o mesmo do comprovante. Pra mudar, é em Configurações, Empresa.
Passo três, os impostos. Primeiro, o regime tributário. A Recicla Vale é Lucro Real, e quem define isso é o contador.
Olha: escolhido o regime, a tela já ajusta os campos de PIS e COFINS.
Mais embaixo vem o i-cê-eme-ésse, o imposto do estado sobre a mercadoria, com a alíquota e os códigos que o contador passar.
Depois, o cê-éfe-ó-pê padrão de cada operação. O cê-éfe-ó-pê é o código que diz que tipo de nota é aquela: uma venda, uma compra, uma devolução.
No fim, a Reforma Tributária. Ligado o cálculo do i-bê-ésse e da cê-bê-ésse, o sistema calcula esses tributos sozinho, com os códigos que o contador passar.
Tudo isso é o padrão. Ele vale pra toda nota em que nenhum cenário se aplica.
Clico em Salvar configuração. Pronto: a empresa está cadastrada pra emitir ene-éfe-ê.""",
5: """E quando uma venda não segue o padrão? Pra isso existem os cenários. Um cenário é uma exceção ao padrão, que só vale numa situação certa.
O aviso de cima vale pra todos os cenários: o que você preenche aqui vai impresso na nota. O Ecossistema não faz recomendação fiscal, então confirme tudo com a contabilidade.
Por exemplo: o contador passou um tratamento próprio para as vendas à Fundição Bandeira do Vale. Clico em Criar o primeiro cenário e dou um nome que diga a situação.
Em Quando aplicar ficam as condições. Aqui, a operação é venda, e o cliente é um só: a Fundição, pelo CNPJ. O resto fica em Qualquer.
Em O que aplicar entra só o que muda, do jeito que o contador passou. Campo em branco não é zero: ele continua vindo do padrão.
Clico em Criar cenário. Ele nasce como não revisado, e depois de conferir com a contabilidade é só marcar como revisado.
Uma dica: não precisa um cenário pra cada combinação. Cadastre a regra geral e, depois, só a exceção mais estreita. Quando duas servem pra mesma nota, vale a mais específica.""",
6: """Agora, de qual número a primeira nota sai. Toda nota tem uma série e um número. A série é a sequência, e o número sobe de um em um.
Aqui, entrada e saída usam a mesma série, a série um. Pra quem usa uma série só, é deixar assim.
A Recicla Vale já emitia nota em outro sistema, na série um. A última foi a mil duzentos e quarenta e oito, então a numeração precisa continuar dali.
Em Adicionar série, informo a série um e a última nota emitida nela, a mil duzentos e quarenta e oito.
Se a empresa nunca emitiu nota, é deixar em zero, e a primeira sai com o número um.
Clico em Adicionar. Pronto: a próxima nota sai com o número mil duzentos e quarenta e nove.""",
7: """Mais dois cadastros. Quando a carga vai com uma transportadora contratada, os dados dela vão na nota. Então a gente cadastra uma vez, e na nota é só escolher.
Aqui vai a Cargas Vale do Sol: razão social, CNPJ, inscrição estadual e endereço.
No bloco Veículo vai a placa do caminhão que costuma fazer a entrega.
Clico em Adicionar, e ela entra na lista.
E Serviços é o cadastro da nota de serviço, a ene-éfe-ésse-ê, pra quando a empresa presta um serviço, como uma coleta. Isso fica pro próximo tutorial.""",
8: """Antes de emitir, a cota. Cada nível do módulo tem um limite de documentos por mês, e o selo mostra quantos já foram usados: zero de cem.
Passando o mouse, aparecem o nível contratado e quanto você emitiu no mês. O tamanho da cota depende do plano.
Toda nota que você emite conta: a de mercadoria, a de serviço, o manifesto de transporte, o ême-tê-érre e o cê-dê-éfe. E as notas recebidas, depois que você ativa esse recurso.
Uma dica: nota cancelada continua contando. Cancelar não devolve o documento pra cota.
O selo fica âmbar perto do limite e vermelho quando chega nele. Mesmo assim, ainda dá pra emitir mais cinco documentos: é a tolerância.
Só depois dos cinco a emissão trava, com o aviso Suas notas do mês acabaram. Aí é subir de nível, e vale na hora.""",
9: """Agora sim, a primeira nota. A Serra Fina Alumínio Reciclagem comprou alumínio perfil e pediu a nota. Clico em Nova Nota.
É uma venda, então ene-éfe-ê de Saída. A nota tem dois passos: Dados e Itens.
Em Para quem, escolho o cliente: a Serra Fina.
Em O que é vai a natureza da operação: venda de mercadorias. O cê-éfe-ó-pê vem sozinho, pela natureza e pelo estado do cliente.
E a numeração: série um, número mil duzentos e quarenta e nove, como a gente configurou. A data em branco é agora.
Clico em Avançar, e vêm os itens.
Escolho o alumínio perfil. O ene-cê-ême, que é o código do tipo de mercadoria, e o preço de venda vêm do cadastro. Trezentos e vinte quilos, a dez e quarenta o quilo.
Clico em Incluir. A nota fica em três mil trezentos e vinte e oito reais, e o selo de cima diz Pronta pra emitir.
Uma dica: antes da primeira nota, confirme com o contador que o CNPJ já está credenciado na sefás pra emitir ene-éfe-ê. Assim a primeira nota já sai autorizada.
Quando você emite, o certificado assina a nota e ela vai pra sefás. A sefás confere e, estando tudo certo, autoriza. Aí a nota ganha um protocolo e uma chave de acesso.
Clico em Emitir Nota, e ela entra na lista como Aguardando sefás.
Uma dica: enviada pra processamento ainda não é autorizada. A nota só está autorizada quando aparecem o número, o protocolo e a chave de acesso.
Em Visualizar está tudo: a nota mil duzentos e quarenta e nove, autorizada, com a chave de acesso, os quarenta e quatro números que identificam a nota, e o protocolo da sefás.""",
10: """Quase sempre a nota nasce de uma venda que já está no sistema. Hoje cedo, a Fundição Bandeira do Vale comprou cobre mel. Em vez de digitar tudo de novo, a gente puxa o pedido.
Em Importar de, clico em Pedido, e aparecem as vendas. Esta é a da Fundição.
Clico em Importar. O cliente e os itens vêm do pedido.
Repara na quantidade: quinhentos quilos. A balança marcou quinhentos e seis, mas seis quilos foram de tara e impureza.
A nota leva sempre o peso líquido, já sem a tara e a impureza. Quinhentos quilos de cobre mel, a quarenta e sete e noventa: vinte e três mil novecentos e cinquenta reais.
Uma dica: quando o cliente disser que o peso da nota não bate com o ticket, quase sempre ele está comparando o bruto com o líquido.
A carga vai com a transportadora. Na aba Transporte, escolho a modalidade do frete e a Cargas Vale do Sol, que já vem com a placa.
Emitir Nota. Pronto: a mil duzentos e cinquenta está autorizada.""",
11: """E as compras do dia, de quem não emite nota? A Dona Cida e o Valdir vendem sucata como pessoa física, e a nota de entrada dessas compras sai pela Recicla Vale.
Em vez de uma nota por compra, dá pra juntar o dia todo. Na barra Importar de, clico em Emissão em Massa, Caixa.
Escolho ontem, nove de novembro. Aparece o caixa do Marcos, já fechado, com as compras do dia.
Seleciono todas as que ainda não têm nota.
Em Como as notas serão geradas, escolho Uma nota consolidada. A tela mostra a faixa: ene-éfe-ê mil duzentos e cinquenta e um, de oitocentos e três reais e trinta.
Ela junta os itens iguais: sessenta e quatro quilos de latinha, cento e oitenta de papelão e quatrocentos e dez de ferro misto. Quem prefere uma nota por compra usa a outra opção, Uma nota por pedido.
Clico em Montar nota consolidada. A nota fica em nome da própria Recicla Vale, como consumidor final, e a natureza é entrada de sucata para revenda, de pessoa física.
Confiro os itens e clico em Emitir Nota. Pronto: a mil duzentos e cinquenta e um está autorizada, com as compras do dia inteiro.""",
12: """Nota emitida, e se algo mudar? A Serra Fina ligou: desistiu do alumínio, e a carga nem saiu do pátio. Então a nota mil duzentos e quarenta e nove vai ser cancelada.
No menu da nota, Cancelar. O motivo é obrigatório, com pelo menos quinze caracteres.
Confirmar Cancelamento. Pronto, cancelada. Passadas vinte e quatro horas da autorização, a própria tela avisa que o prazo normal acabou.
Já a mil duzentos e cinquenta continua valendo. Só mudou um detalhe: a transportadora trocou o caminhão da carga. Pra isso existe a carta de correção, um aviso que fica junto da nota.
Ela corrige erros em campos específicos. E a própria tela diz o que não dá pra corrigir: valores, quantidade, quem vende e quem compra, a data e o que mudar o imposto.
No texto, uso o formato que a tela sugere: onde se lê a placa antiga, leia-se a placa nova.
Clico em Enviar cê-cê-ê. Pronto: a correção fica registrada junto da nota.""",
13: """E o número que nunca virou nota? No sistema antigo, as notas mil duzentos e quarenta e seis e mil duzentos e quarenta e sete foram recusadas e ficaram pra trás. Esses números estão em aberto na sefás.
Inutilizar é avisar a sefás que esses números não vão virar nota.
Fica nos três pontinhos, em Inutilizar numeração. Repara no aviso: é pra sempre, e só vale pra número que nunca foi autorizado. Nota autorizada se resolve com o cancelamento.
Em Por Faixa vai a série um, do mil duzentos e quarenta e seis ao mil duzentos e quarenta e sete. Dá pra fechar um número só ou uma faixa inteira de uma vez.
E na aba Inutilizar Rejeitadas, as notas recusadas aqui no sistema se fecham em lote.
Escrevo a justificativa e clico em Inutilizar na sefás.
Pronto. Os números fechados ficam aqui, em Inutilizadas.""",
14: """Agora, os arquivos da nota. Toda nota autorizada tem dois: o dânfi e o xis-ême-éle.
O dânfi é a folha impressa que acompanha a carga no caminhão. O xis-ême-éle é o arquivo oficial da nota, que o contador guarda.
Os dois ficam no menu da nota.
Download dânfi abre o pê-dê-éfe, pronto pra imprimir.
E Download xis-ême-éle baixa o arquivo, com o número da nota no nome.
O menu muda com a situação da nota. Na cancelada, aparece o xis-ême-éle de Cancelamento.""",
15: """Até aqui, as notas que a Recicla Vale emite. Agora, as que ela recebe.
Quando um fornecedor emite uma nota com o CNPJ da Recicla Vale como destinatário, a nota passa pela sefás. Com o recurso ativo, ela aparece sozinha aqui.
Clico em Ativar Notas Recebidas. A tela avisa: daqui pra frente, cada nota recebida conta na mesma cota das notas que você emite.
Ativar mesmo assim. Em instantes chegam as notas emitidas contra o CNPJ da Recicla Vale: a da Auto Peças Vale Forte, de mil novecentos e oitenta e quatro reais, e a do Depósito Irmãos Siqueira.
Cada linha mostra quem emitiu, o valor, a data, a situação na sefás e a manifestação.""",
16: """Chegou a nota, e agora? Repara na coluna Manifestação: as duas já estão com Ciência.
Manifestar é responder à sefás sobre a nota que chegou. A ciência não é um botão: ela já vem sozinha, quando a nota entra.
A do Depósito chegou só com o resumo. Pra baixar o xis-ême-éle e o dânfi de uma nota recebida, é Buscar documento, que não confirma nem recusa nada.
As respostas ficam no grupo Manifestar. Confirmar operação diz que a compra é sua. Desconhecer operação, que você não reconhece a nota. E Operação não realizada, que a compra não aconteceu.
As duas últimas pedem uma justificativa e não podem ser desfeitas.
A bateria da Auto Peças chegou certinho, então confirmo a operação. Pronto: confirmada.""",
17: """E a nota que ainda não apareceu na lista? A Cooperativa Recomeço vendeu latinha e PET ontem e mandou o xis-ême-éle por e-mail. Dá pra trazer a nota pelo arquivo.
Clico em Importar nota, vou na aba Arquivo xis-ême-éle e escolho o arquivo da cooperativa.
Importar nota. Pronto: nota importada, e ela entra na lista com as outras.
Agora, Lançar compra. O sistema lê o xis-ême-éle e acha o fornecedor pelo CNPJ.
E casa cada item com um material do cadastro. A latinha do xis-ême-éle tem o mesmo nome do material, então a confiança é alta.
O PET prensado tem palavras em comum com o Plástico PET, e o selo pede pra conferir. Quando a confiança é baixa, o material fica pra você escolher.
A nota traz só o peso líquido. E Conferir na tela de compra leva os itens pra tela de Compra. Nada é lançado agora: lá você confere os valores e escolhe como pagou.""",
18: """Pronto! Recapitulando: a gente subiu o certificado á-um, preencheu a empresa e os impostos no Lucro Real e criou um cenário, sempre com o que o contador passou.
Continuou a numeração do sistema antigo, cadastrou a transportadora e viu a cota do mês, com a tolerância de cinco documentos.
Emitiu a nota pelos três caminhos: do zero, a partir de um pedido e a partir de um caixa fechado.
Cancelou uma nota, mandou uma carta de correção, inutilizou os números que sobraram e baixou o dânfi e o xis-ême-éle.
E ativou as notas recebidas, confirmou uma operação e importou uma nota pelo xis-ême-éle.
No próximo tutorial, o documento que acompanha a carga na estrada e o pacote que o contador pede. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "Onde ficam as notas.",
           2: "O certificado vem primeiro.",
           3: "Subindo o certificado á-um.",
           4: "Empresa e impostos.",
           5: "Cenários fiscais.",
           6: "Série e numeração.",
           7: "Transportadora e serviços.",
           8: "A cota de documentos.",
           9: "Nota avulsa, do zero.",
           10: "Nota a partir de um pedido.",
           11: "Nota de um caixa fechado.",
           12: "Cancelar e corrigir.",
           13: "Inutilizar numeração.",
           14: "dânfi e xis-ême-éle.",
           15: "As notas recebidas.",
           16: "Manifestar a nota.",
           17: "Importar pelo xis-ême-éle.",
           18: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Fiscal",
           2: "Configuração",
           3: "Certificado",
           4: "Configuração",
           5: "Cenários",
           6: "Numeração",
           7: "Configuração",
           8: "Cota",
           9: "Emissão",
           10: "Emissão",
           11: "Emissão",
           12: "Correções",
           13: "Numeração",
           14: "Documentos",
           15: "Notas recebidas",
           16: "Notas recebidas",
           17: "Notas recebidas",
           18: "Resumo"}

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
