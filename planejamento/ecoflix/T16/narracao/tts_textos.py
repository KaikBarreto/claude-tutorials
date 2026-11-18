# Texto enviado ao ElevenLabs (eleven_v4, voz Kaik Barreto) por capítulo do T16 "Nota Fiscal de mercadoria (NF-e)".
# Gerado do roteiro.md (coluna Fala) por T16_gera_tts.py: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia usadas (legenda -> fala; tabela do PERFIL de 10/11 01:20, com o IPA de NF-e, NFS-e e ICMS):
#   Fiscal & Ambiental -> "Fiscal e Ambiental" | EcoSistema -> "Ecossistema" | NFS-e -> "/ˈẽːniˈɛːfiˈɛːsiˈeː/" | SEFAZ -> "sefás" | DANFE -> "dânfi" | NF-e -> "/ˈẽniˈɛfiˈe/" | CFOP -> "cê-éfe-ó-pê" | ICMS -> "/iˈseˈɛmiˈɛːsːi/" | CC-e -> "cê-cê-ê" | NCM -> "ene-cê-ême" | MTR -> "ême-tê-érre" | CDF -> "cê-dê-éfe" | XML -> "xis-ême-éle" | PDF -> "pê-dê-éfe" | DRE -> "dê-érri-ê" | pfx -> "pê-éfe-xis" | IBS -> "i-bê-ésse" | CBS -> "cê-bê-ésse" | A1 -> "á-um"
# Novas desta aula (testar num trecho curto antes da voz): CC-e, A1, pfx, IBS, CBS, Fiscal & Ambiental.
CAPS = {
0: """Oi! Neste tutorial a gente vai do certificado digital até a nota fiscal autorizada, na Recicla Vale Metais.
A Fundição Bandeira do Vale compra cobre dela toda semana. E a carga só sai do pátio com a nota fiscal de mercadoria, a /ˈẽniˈɛfiˈe/.
As notas fazem parte do módulo Notas Fiscais. Se ele estiver no seu plano, tudo fica em Fiscal e Ambiental.
Se você ainda não viu o tutorial Relatório Financeiro e dê-érri-ê, dá uma olhada antes. [pause] É a parte mais delicada do sistema, então a gente vai devagar e na ordem.""",
1: """Tudo começa no menu, em Fiscal e Ambiental.
Aqui ficam as telas fiscais: as notas de mercadoria, as de serviço, o transporte, o ambiental, o estoque fiscal e os relatórios fiscais. Hoje a gente fica nas notas de mercadoria.
Clico em Notas Fiscais, /ˈẽniˈɛfiˈe/.
Em cima ficam as sub-abas: Entrada, Saída, Notas Recebidas e Inutilizadas.
Saída é a nota da venda, quando a mercadoria sai do pátio pro cliente. Entrada é a da compra, quando ela chega do fornecedor.
Notas Recebidas são as que os fornecedores emitem contra o seu CNPJ, e Inutilizadas guarda os números fechados. Cada uma tem a sua parte neste tutorial.
Do lado direito ficam as Configurações Fiscais e a cota do mês. Embaixo, os cartões das notas emitidas, pendentes e rejeitadas ou canceladas. E o botão Nova Nota.
Um detalhe: o botão Nova Nota só aparece pra quem tem permissão de emitir. Quem só exporta as notas pro contador não vê esse botão.""",
2: """Antes de qualquer nota, a configuração. Ela fica no botão Configurações Fiscais e é tudo o que a sefás, a Secretaria da Fazenda do estado, precisa saber antes da primeira nota.
Em cima ficam as seções, na ordem em que se preenche: do certificado até os serviços.
Repara que Empresa, Impostos, Numeração e Transportadora estão apagadas: elas só abrem depois do certificado digital.
É o certificado digital que assina a nota, como a assinatura da empresa. Sem ele, nada do que for preenchido aqui chega na sefás.
Por isso o certificado é a primeira etapa. Depois vêm os dados da empresa, e por último os impostos.
Uma dica: faça essa configuração junto com o contador. Um campo errado aqui faz a sefás recusar a nota na hora de emitir.""",
3: """Então, o certificado. A /ˈẽniˈɛfiˈe/ usa o certificado á-um, que é um arquivo de computador com uma senha.
É só arrastar o arquivo ponto pê-éfe-xis da Recicla Vale pra esta área, ou clicar nela e escolher. Escolhido o arquivo, aparece o campo da senha.
Em Senha do Certificado vai a senha do próprio arquivo, e não a senha da empresa.
Clico em Validar e salvar á-um. Pronto: certificado validado.
Embaixo aparece até quando ele vale: catorze de setembro de dois mil e vinte e sete.
Uma dica: o á-um vale no máximo um ano. Se a tela disser que a validade não confere, quase sempre foi enviado o arquivo errado, o da certificadora, e não o do CNPJ.
Aí é pedir o arquivo certo ao contador e usar o Substituir Certificado.
Na renovação é o mesmo caminho. O á-um vence todo ano. Quando ele vence, a tela avisa que o certificado venceu, e é só enviar o arquivo renovado aqui mesmo. Sem isso, nenhuma nota sai.
E o botão Próximo leva pra empresa.""",
4: """Com o certificado validado, os dados da empresa. É o passo dois.
O Importar dados traz o que já está no cadastro da empresa: o nome, o CNPJ, o telefone e o e-mail.
Confiro a razão social completa e digito a inscrição estadual. O CNPJ daqui é o que vai como emitente em toda nota.
O endereço fiscal vem do cadastro da empresa, o mesmo do comprovante. Pra mudar, é em Configurações, Empresa.
Mais embaixo dá pra enviar o logo que sai impresso na nota. E o responsável técnico só se preenche se o contador pedir, porque alguns estados exigem.
Passo três, os impostos. Primeiro, o regime tributário. A Recicla Vale é Lucro Real, e quem define isso é o contador.
Olha: escolhido o regime, a tela já ajusta os campos de PIS e COFINS.
Mais embaixo vem o /iˈseˈɛmiˈɛːsːi/, o imposto do estado sobre a mercadoria, com a alíquota e os códigos que o contador passar. Aqui também fica o diferimento automático nas vendas pra indústria.
Depois, o PIS e a COFINS. No Lucro Real o regime é o não cumulativo, e cada um tem o código da venda e o código da compra. Embaixo, o i-pê-í, só pra quem industrializa. Nada disso se escolhe no chute: é a planilha do contador, campo por campo.
Depois, o cê-éfe-ó-pê padrão de cada operação. O cê-éfe-ó-pê é o código que diz que tipo de nota é aquela: uma venda, uma compra, uma devolução.
O texto que precisa sair em toda nota, como a base legal de um benefício, fica em Informações Complementares Padrão. E, logo abaixo, o campo reservado ao Fisco e o código de benefício fiscal, só quando o contador pedir.
No fim, a Reforma Tributária. Ligado o cálculo do i-bê-ésse e da cê-bê-ésse, o sistema calcula esses tributos sozinho. Pra salvar, a tela pede pelo menos um par completo: o código e a classificação tributária, que o contador passa.
Tudo isso é o padrão. Ele vale pra toda nota em que nenhum cenário se aplica.
Clico em Salvar configuração. Pronto: a empresa está cadastrada pra emitir /ˈẽniˈɛfiˈe/.""",
5: """E quando uma venda não segue o padrão? Pra isso existem os cenários. Um cenário é uma exceção ao padrão, que só vale numa situação certa.
O aviso de cima vale pra todos os cenários: o que você preenche aqui vai impresso na nota. O Ecossistema não faz recomendação fiscal, então confirme tudo com a contabilidade.
Por exemplo: o contador passou um tratamento próprio para as vendas à Fundição Bandeira do Vale. Clico em Criar o primeiro cenário e dou um nome que diga a situação.
Em Quando aplicar ficam as condições. Aqui, a operação é venda, e o cliente é um só: a Fundição, pelo CNPJ. O resto fica em Qualquer.
O cenário também pode valer por material, pelo ene-cê-ême, por destino, dentro ou fora do estado, pelo regime do cliente e até pelo peso da nota. Por exemplo: toda venda de cobre pra fora do estado.
Em O que aplicar entra só o que muda, do jeito que o contador passou. Campo em branco não é zero: ele continua vindo do padrão.
Clico em Criar cenário. Ele nasce como não revisado, e depois de conferir com a contabilidade é só marcar como revisado.
Uma dica: não precisa criar um cenário pra cada combinação. Cadastre a regra geral e, depois, só a exceção mais estreita. Quando duas servem pra mesma nota, vale a mais específica.""",
6: """Agora, de qual número a primeira nota sai. Toda nota tem uma série e um número. A série é a sequência, e o número sobe de um em um.
Quem já emite nota continua a sequência. A Recicla Vale usa a série um, e a última foi a mil duzentos e quarenta e oito, então a numeração precisa continuar dali.
Repara que a tela já avisa: a série um está como padrão, mas ainda não foi cadastrada. Então, primeiro o cadastro.
Em Adicionar série, informo a série um e a última nota emitida nela, a mil duzentos e quarenta e oito.
Se a empresa nunca emitiu nota, é deixar em zero, e a primeira sai com o número um.
Clico em Adicionar. Pronto: a próxima nota sai com o número mil duzentos e quarenta e nove.
Agora a série padrão mostra a série um, e o aviso sumiu. Aqui, entrada e saída usam a mesma série. Pra quem usa uma série só, é deixar assim.
Quem separa as notas de entrada numa série e as de saída em outra desliga esta chave e escolhe uma série pra cada.""",
7: """Mais dois cadastros. Quando a carga vai com uma transportadora contratada, os dados dela vão na nota. Então a gente cadastra uma vez, e na nota é só escolher.
Aqui vai a Cargas Vale do Sol: razão social, CNPJ, inscrição estadual e endereço.
No bloco Veículo vai a placa do caminhão que costuma fazer a entrega.
Clico em Adicionar, e ela entra na lista.
E Serviços é o cadastro da nota de serviço, a /ˈẽːniˈɛːfiˈɛːsiˈeː/, pra quando a empresa presta um serviço, como uma coleta. Isso fica pro próximo tutorial.""",
8: """Antes de emitir, a cota. Cada nível do módulo tem um limite de documentos por mês, e o selo mostra quantos já foram usados: por enquanto, nenhum.
Passando o mouse, aparecem o nível contratado e quanto você emitiu no mês. O tamanho da cota depende do plano.
Toda nota que você emite conta: a de mercadoria, a de serviço, o manifesto de transporte, o ême-tê-érre e o cê-dê-éfe. E as notas recebidas, depois que você ativa esse recurso.
Uma dica: nota cancelada continua contando. Cancelar não devolve o documento pra cota.
O selo fica âmbar perto do limite e vermelho quando chega nele. Mesmo assim, ainda dá pra emitir mais cinco documentos: é a tolerância.
Só depois dos cinco a emissão trava, com o aviso Suas notas do mês acabaram. Aí é subir de nível, e vale na hora.""",
9: """Agora sim, a primeira nota. A Serra Fina Alumínio Reciclagem comprou alumínio perfil e pediu a nota. Clico em Nova Nota.
É uma venda, então /ˈẽniˈɛfiˈe/ de Saída. A nota abre em tela cheia, com as abas em cima. As duas primeiras são as obrigatórias: Dados e Itens.
No alto ficam o número previsto e o ambiente. Produção é a nota de verdade. Homologação é só pra teste, e não vale como nota fiscal.
Em Quem emite aparece a empresa, e quem tem mais de um CNPJ escolhe aqui qual deles emite. Em Para quem, escolho o cliente: a Serra Fina.
Em O que é vai a natureza da operação: venda de mercadorias. O cê-éfe-ó-pê vem sozinho, pela natureza e pelo estado do cliente.
E a numeração: série um, número mil duzentos e quarenta e nove, como a gente configurou. A data em branco é agora, e dá pra informar outra quando a carga saiu mais cedo.
Clico em Avançar, e vêm os itens.
Escolho o alumínio perfil. O ene-cê-ême, que é o código do tipo de mercadoria, e o preço de venda vêm do cadastro. Trezentos e vinte quilos, a dez e quarenta o quilo.
Clico em Incluir. A nota fica em três mil trezentos e vinte e oito reais, e o selo de cima diz Pronta pra emitir.
Cada item tem os seus detalhes. Aqui ficam o cê-éfe-ó-pê do item, com a origem dele, e o desconto do item. O desconto da nota inteira fica no botão Desconto geral.
Uma dica: antes da primeira nota, confirme com o contador que o CNPJ já está credenciado na sefás pra emitir /ˈẽniˈɛfiˈe/. Assim a primeira nota já sai autorizada.
Se precisar parar no meio, o Salvar Rascunho guarda a nota. Depois é só abrir o menu dela, na lista, e clicar em Continuar preenchendo.
Quando você emite, o certificado assina a nota e ela vai pra sefás. A sefás confere e, estando tudo certo, autoriza e devolve o protocolo. Aí sim, a nota vale.
Clico em Emitir Nota, e ela entra na lista como Aguardando sefás.
Uma dica: enviada pra processamento ainda não é autorizada. A nota só está autorizada quando aparecem o número, o protocolo e a chave de acesso. Se a resposta demorar, o Consultar status, no menu da nota, pergunta de novo pra sefás.
Em Visualizar está tudo: a nota mil duzentos e quarenta e nove, autorizada, com a chave de acesso, os quarenta e quatro números que identificam a nota, e o protocolo da sefás.""",
10: """Muitas vezes a nota nasce de uma venda que já está no sistema. Ontem, a Fundição Bandeira do Vale comprou cobre mel, e a carga sai hoje. Em vez de digitar tudo de novo, a gente puxa o pedido.
Em Importar de, clico em Pedido, e aparecem as vendas. Esta é a da Fundição.
Clico em Importar. O cliente e os itens vêm do pedido.
Repara na quantidade: quinhentos quilos. A balança marcou quinhentos e seis, mas seis quilos foram de tara e impureza.
A nota leva sempre o peso líquido, já sem a tara e a impureza. Quinhentos quilos de cobre mel, a quarenta e sete e noventa: vinte e três mil novecentos e cinquenta reais.
Uma dica: quando o cliente disser que o peso da nota não bate com o ticket, quase sempre ele está comparando o bruto com o líquido.
A carga vai com a transportadora. Na aba Transporte, escolho a modalidade do frete e a Cargas Vale do Sol, que já vem com a placa.
Em Volumes Transportados vão a quantidade, a espécie e os pesos da carga: quinhentos e seis quilos de bruto e quinhentos de líquido. Eles saem impressos na nota. Se o frete for cobrado na nota, o valor também entra nesta aba.
A nota já está pronta pra emitir. Mas antes vale passar pelas outras abas, e é o que a gente faz agora.""",
11: """Antes de emitir, vale conferir o imposto. Na aba Impostos, a primeira linha diz qual cenário fiscal entrou. Aqui, o da Fundição, que a gente criou lá na configuração.
Embaixo, tributo por tributo. O /iˈseˈɛmiˈɛːsːi/ veio com o código e o diferimento do cenário. A tela mostra o imposto cheio, a parte diferida e o que fica a recolher, que aqui é zero.
Já o PIS e a COFINS aparecem como suspensos, e a tela avisa com este selo. Isso não veio do cenário. Veio do cadastro da Fundição, que está marcada como indústria.
É assim que a nota se monta: o cenário muda só o que ele diz, o cadastro do cliente entra com a parte dele, e o resto vem do padrão. Se algum código parecer estranho, quem confirma é o contador.
Se o contador pedir um código diferente só nesta nota, tem o botão Ajustar impostos desta nota. O que muda aqui vale só pra ela, e não mexe na configuração.
E a Reforma Tributária. Com o cálculo ligado, o i-bê-ésse e a cê-bê-ésse aparecem num grupo à parte, com a base e o valor de cada um. A própria tela avisa que eles ficam fora do valor aproximado de tributos lá de cima.
Em Faturamento vai como a venda foi combinada. A Fundição paga a prazo, em duas vezes no boleto. Marco A prazo, escolho Boleto e adiciono a segunda parcela. A tela já divide o total: duas de onze mil novecentos e setenta e cinco reais.
Informo o vencimento de cada parcela. A soma tem que bater com o total da nota, senão ela não emite. E quem usa sempre o mesmo prazo escolhe uma condição de pagamento, e as parcelas já vêm preenchidas.
Em Opções vai o número do pedido de compra do cliente, quando a indústria exige esse número na nota.
Voltando em Itens, lá embaixo ficam as Informações complementares: o texto livre desta nota. Dá pra somar ao texto padrão da configuração ou trocar ele só aqui.
Por último, a Pré-visualização. É a nota como ela vai sair, ainda sem valor fiscal. Confiro o cliente, as parcelas, o imposto, o transporte e os itens.
Tudo certo. Emitir Nota. Ela entra como Aguardando sefás e, em instantes, a mil duzentos e cinquenta está autorizada.""",
12: """E as compras do dia, de quem não emite nota? A Dona Cida e o Valdir vendem sucata como pessoa física, e a nota de entrada dessas compras sai pela Recicla Vale.
Em vez de uma nota por compra, dá pra juntar o dia todo. Na barra Importar de, clico em Emissão em Massa, Caixa.
Hoje ainda não tem caixa fechado, e a tela avisa. Escolho ontem, nove de novembro. Aparece o caixa do Marcos, já fechado, com as compras do dia.
Seleciono todas as que ainda não têm nota.
Em Como as notas serão geradas, escolho Uma nota consolidada. A tela mostra a faixa: /ˈẽniˈɛfiˈe/ mil duzentos e cinquenta e um, de oitocentos e três reais e trinta.
Ela junta os itens iguais: sessenta e quatro quilos de latinha, cento e oitenta de papelão e quatrocentos e dez de ferro misto. Quem prefere uma nota por compra usa a outra opção, Uma nota por pedido.
Clico em Montar nota consolidada. A nota fica em nome da própria Recicla Vale, como consumidor final, e a natureza é entrada de sucata para revenda, de pessoa física.
Confiro os itens e clico em Emitir Nota. Pronto: a mil duzentos e cinquenta e um está autorizada, com as compras do dia inteiro.""",
13: """Venda e compra são as notas do dia a dia, mas a natureza da operação tem bem mais: remessa pra conserto, remessa pra demonstração, transferência entre unidades, baixa por perda. E, se a sua não estiver na lista, Outra operação deixa escrever o nome.
Um exemplo: material que estragou ou foi furtado. Na baixa de estoque por perda, a nota sai contra a própria empresa, sem cliente, e o cê-éfe-ó-pê muda sozinho. A tela lembra que o valor é o custo do material.
Por padrão, essa nota só informa a sefás e não mexe no seu estoque. Marcando esta opção, o sistema dá baixa no estoque quando a nota é autorizada. E, se a nota for cancelada, o estoque volta.
Qual natureza usar em cada caso, e com qual cê-éfe-ó-pê, é o contador quem diz. Saio sem emitir.""",
14: """E quando a nota não deixa emitir? Olha esta venda pra Metalúrgica Pinhal, um cliente novo. O selo de cima conta as pendências. Enquanto ele estiver vermelho, o Emitir Nota fica travado.
Passando o mouse, ele diz o que falta. Aqui são três coisas: o cadastro do cliente está incompleto, falta a inscrição estadual dele, e a nota ainda não tem item.
Primeiro, olha este aviso vermelho. A Pinhal é empresa do mesmo estado e está sem inscrição estadual no cadastro. O sistema consultou o CNPJ e achou a inscrição ativa. Sem ela, a sefás recusa a nota.
Um clique grava a inscrição no cadastro e libera essa parte da nota.
Se o cliente for isento de verdade, a tela só avisa e deixa seguir. Ela só trava quando a consulta acha uma inscrição ativa.
Sobrou o cadastro incompleto. O atalho Completar cadastro abre a ficha do cliente aqui mesmo, já nos dados fiscais. Faltava o CEP. Preencho, salvo, e essa pendência some.
Nos itens é a mesma ideia. Incluo mil quilos de ferro misto. Se eu apagar o ene-cê-ême, o selo acusa na hora: item sem ene-cê-ême. O mesmo vale pra item sem quantidade ou com o cê-éfe-ó-pê errado pro destino. Corrigiu, o selo fica verde: Pronta pra emitir.
Esta era só um exemplo, então saio e descarto a nota. Um detalhe: pra um cliente de uma venda só, dá pra digitar os dados direto na nota, sem cadastrar, em Preencher manualmente.""",
15: """A nota passou pelas pendências, foi enviada, e mesmo assim a sefás recusou. Acontece. Esta é outra venda pra Serra Fina, de cento e cinquenta quilos de alumínio perfil, que voltou como Rejeitada pela sefás.
Nota rejeitada não foi autorizada, então não vale como nota. E o número dela não foi usado na sefás. Por isso não é caso de cancelar: é corrigir e mandar de novo.
Em Visualizar, a faixa vermelha traz o código da rejeição, o que a sefás disse e o que fazer. Aqui é o setecentos e setenta e oito: o ene-cê-ême de um item não existe.
E tudo o que acontece com a nota fica em Histórico, com data e hora: o envio, a recusa e, depois, a autorização.
No menu aparecem dois caminhos pra corrigir. Editar e reenviar usa o mesmo número. Editar e reemitir pega o próximo número livre, pra quando já saíram outras notas depois dela.
E se essa venda não for mais acontecer? Aí o número precisa ser fechado, em Inutilizar numeração, que a gente vê mais adiante.
Vou de mesmo número. A nota abre preenchida, e a tela confirma: vai ser reemitida como série um, número mil duzentos e cinquenta e dois, com o número travado.
Nos itens, o ene-cê-ême do alumínio estava com o final errado. Corrijo aqui. E, pra não repetir o erro, vale conferir também o ene-cê-ême no cadastro do material.
Emitir Nota. Ela volta pra fila da sefás e, em instantes, está autorizada.
As recusas mais comuns são quatro. CNPJ não habilitado: o contador precisa credenciar a empresa na sefás. Inscrição estadual do cliente errada ou faltando: corrige no cadastro. ene-cê-ême que não existe: corrige no item e no material. E certificado vencido ou de outro CNPJ: envia o á-um certo na configuração.
Às vezes o problema nem é seu: é instabilidade da sefás. Aí a própria mensagem manda esperar uns minutos e enviar de novo. E uma nota recusada não trava a emissão das próximas.""",
16: """Nota autorizada, e se algo mudar? A Serra Fina ligou: desistiu daquele primeiro pedido, e a carga nem saiu do pátio. Então a nota mil duzentos e quarenta e nove vai ser cancelada.
No menu da nota, Cancelar. O motivo é obrigatório, com pelo menos quinze caracteres.
Confirmar Cancelamento. Pronto, cancelada.
O prazo normal de cancelamento é de vinte e quatro horas. Depois disso a sefás ainda costuma aceitar o pedido até vinte dias, e a tela avisa que a nota está fora do prazo normal. Passou dos vinte dias, não cancela mais: o caminho é a nota de devolução, que a gente vê daqui a pouco.
Já a mil duzentos e cinquenta continua valendo. Só mudou um detalhe: a transportadora trocou o caminhão da carga. Pra isso existe a carta de correção, um aviso que fica junto da nota.
Ela corrige erros em campos específicos. E a própria tela diz o que não dá pra corrigir: valores, quantidade, quem vende e quem compra, a data e qualquer coisa que mude o imposto.
No texto, uso o formato que a tela sugere: onde se lê a placa antiga, leia-se a placa nova.
Clico em Enviar cê-cê-ê. Pronto: a correção fica registrada junto da nota.
Abrindo a Carta de Correção de novo, ela está na lista, com o pê-dê-éfe pra mandar pro cliente ou pra transportadora, o xis-ême-éle e o protocolo da sefás. Cada nota aceita até vinte cartas, e vale sempre a última.""",
17: """E quando a mercadoria volta? A Fundição recebeu o cobre e devolveu quarenta quilos, que vieram com mistura. A nota mil duzentos e cinquenta já está valendo e a carga já rodou, então não é cancelamento. É uma nota de devolução.
A mercadoria está entrando de volta, então é /ˈẽniˈɛfiˈe/ de Entrada, com a natureza Devolução de venda. O cê-éfe-ó-pê muda sozinho, e aparece um campo novo: a chave da nota original.
Toda devolução aponta pra nota que ela devolve. Em vez de colar os quarenta e quatro números, clico em Selecionar nota do sistema e escolho a mil duzentos e cinquenta. Vêm o cliente, a chave e os itens.
Nos itens, deixo só o que voltou: quarenta quilos, pelo mesmo preço da venda. Mil novecentos e dezesseis reais.
Embaixo tem um bloco que só a devolução tem. A sefás exige, em cada produto devolvido, a nota de origem e o número daquele item dentro dela. A chave já veio. O número do item, a tela está pedindo.
Esse número está no dânfi da nota original, na coluna Item. O cobre era o item um, então digito um. Quando a nota original já guarda esse número, ele vem preenchido sozinho. Uma dica: confira sempre, porque número errado joga o crédito do cliente no produto errado.
Repara que a aba Faturamento sumiu: devolução não tem cobrança. E em Impostos a tela propõe os códigos da entrada. Em devolução, vale mostrar essa prévia pro contador antes de emitir.
Emitir Nota. Pronto: a devolução mil duzentos e cinquenta e três está autorizada, ligada à nota original.
E o contrário também existe. Quando é a Recicla Vale que devolve uma compra pro fornecedor, é /ˈẽniˈɛfiˈe/ de Saída, com a natureza Devolução de compra. Uma dica: confirme com o contador quem emite a devolução no seu caso, você ou o cliente.""",
18: """Último caso: a nota saiu com valor a menor. O preço combinado com a Fundição era quarenta e oito e quarenta o quilo, e a nota saiu a quarenta e sete e noventa. Valor não se corrige com carta de correção. Pra isso existe a nota complementar, que leva só a diferença.
No menu da nota original, Gerar nota complementar. Ela já abre com o cliente, a natureza Complementar de venda e a chave da nota original.
Repara nesta opção, desmarcada: contar esta nota no estoque fiscal. Só se marca quando o complemento é de peso. Em complemento de valor, o peso já saiu na nota original.
Os itens vêm vazios, porque quem diz o que complementar é você. Incluo o cobre mel, com os quinhentos quilos da nota e só a diferença no valor: cinquenta centavos por quilo. Duzentos e cinquenta reais.
Em Impostos, a tela propõe o imposto da complementar pelas mesmas regras da venda. Uma dica: complementar é a nota que mais muda de um caso pro outro. Mostre esta prévia pro contador antes de emitir.
Emitir Nota. Pronto: a complementar mil duzentos e cinquenta e quatro está autorizada. O mesmo caminho serve pra imposto que saiu a menor, sempre com a orientação do contador.""",
19: """E o número que nunca virou nota? Em outubro, a sequência pulou dois números: a mil duzentos e quarenta e seis e a mil duzentos e quarenta e sete nunca viraram nota. Esses números estão em aberto na sefás.
Inutilizar é avisar a sefás que esses números não vão virar nota.
Fica nos três pontinhos, em Inutilizar numeração. Repara no aviso: é pra sempre, e só vale pra número que nunca foi autorizado. Tem prazo: até o dia dez do mês seguinte. E nota autorizada se resolve com o cancelamento.
Em Por Faixa vai a série um, do mil duzentos e quarenta e seis ao mil duzentos e quarenta e sete. Dá pra fechar um número só ou uma faixa inteira de uma vez.
A outra aba, Inutilizar Rejeitadas, lista as notas recusadas que não vão ser corrigidas, pra fechar todas de uma vez. Aqui está vazia, porque a nossa rejeitada foi corrigida e autorizada.
Escrevo a justificativa e clico em Inutilizar na sefás.
Pronto. Os números fechados ficam aqui, em Inutilizadas.""",
20: """Agora, os arquivos da nota. Toda nota autorizada tem dois: o dânfi e o xis-ême-éle.
O dânfi é a folha impressa que acompanha a carga no caminhão. O xis-ême-éle é o arquivo oficial da nota, que o contador guarda.
Os dois ficam no menu da nota. Ali também tem o Comprovante, um resumo da nota pra imprimir na impressora térmica.
Download dânfi abre o pê-dê-éfe, pronto pra imprimir. O dânfi ganhou um visual mais limpo. E, a partir de primeiro de dezembro, ele passa a sair com os campos do i-bê-ésse, da cê-bê-ésse e do Imposto Seletivo. A troca é automática, pela data de emissão da nota.
E Download xis-ême-éle baixa o arquivo, com o número da nota no nome.
E em Visualizar, a aba xis-ême-éle mostra o mesmo arquivo enviado à sefás, pra conferir ou copiar um trecho.
O menu muda com a situação da nota. Na cancelada, aparece o xis-ême-éle de Cancelamento.
Clicando na linha, abrem os detalhes sem sair da lista: a chave, os valores, o protocolo e quem emitiu.
Pra achar uma nota antiga, tem a busca, o período e os Filtros, com a situação: autorizada, rejeitada, cancelada, rascunho. E as notas de teste ficam separadas, na aba Homologação.
E pra mandar as notas do mês pro contador, tem a Exportação Contábil, que é assunto do próximo tutorial.""",
21: """Até aqui, as notas que a Recicla Vale emite. Agora, as que ela recebe.
Quando um fornecedor emite uma nota com o CNPJ da Recicla Vale como destinatário, a nota passa pela sefás. Com o recurso ativo, ela aparece sozinha aqui.
Clico em Ativar Notas Recebidas. A tela avisa: a partir da ativação, cada nota recebida conta na mesma cota das notas que você emite.
Ativar mesmo assim. Em instantes chegam as notas emitidas contra o CNPJ da Recicla Vale: a da Auto Peças Vale Forte, de mil novecentos e oitenta e quatro reais, e a do Depósito Irmãos Siqueira.
Cada linha mostra quem emitiu, o valor, a data, a situação na sefás e a manifestação.
Depois disso, as notas entram sozinhas. E o Sincronizar agora faz a busca na hora.""",
22: """Chegou a nota, e agora? Repara na coluna Manifestação: as duas já estão com Ciência.
Manifestar é responder à sefás sobre a nota que chegou. A ciência não é um botão: ela já vem sozinha, quando a nota entra.
A do Depósito chegou só com o resumo. Pra baixar o xis-ême-éle e o dânfi de uma nota recebida, é Buscar documento, que não confirma nem recusa nada.
As respostas ficam no grupo Manifestar. Confirmar operação diz que a compra é sua. Desconhecer operação, que você não reconhece a nota. E Operação não realizada, que a compra não aconteceu.
As duas últimas pedem uma justificativa e não podem ser desfeitas.
A bateria da Auto Peças chegou certinho, então confirmo a operação. Pronto: confirmada.""",
23: """E a nota que ainda não apareceu na lista? A Cooperativa Recomeço vendeu latinha e PET ontem e mandou o xis-ême-éle por e-mail. Dá pra trazer a nota pelo arquivo.
Clico em Importar nota, vou na aba Arquivo xis-ême-éle e escolho o arquivo da cooperativa.
Importar nota. Pronto: nota importada, e ela entra na lista com as outras.
Agora, Lançar compra. O sistema lê o xis-ême-éle e acha o fornecedor pelo CNPJ.
E casa cada item com um material do cadastro. A latinha do xis-ême-éle tem o mesmo nome do material, então a confiança é alta.
O PET prensado tem palavras em comum com o Plástico PET, e o selo pede pra conferir. Quando a confiança é baixa, o material fica pra você escolher.
A nota traz só o peso líquido. E Conferir na tela de compra leva os itens pra tela de Compra. Nada é lançado agora: lá você confere os valores e escolhe como pagou. No mesmo menu, a nota recebida também pode virar despesa ou ir pro saldo do fornecedor.""",
24: """Pronto! Recapitulando: a gente subiu o certificado á-um, preencheu a empresa e os impostos no Lucro Real e criou um cenário, sempre com o que o contador passou.
Continuou a numeração da série um, cadastrou a transportadora e viu a cota do mês, com a tolerância de cinco documentos.
Emitiu a nota pelos três caminhos: do zero, a partir de um pedido e a partir de um caixa fechado. E conferiu os impostos, as parcelas e a pré-visualização antes de emitir.
Resolveu as pendências que travam a emissão, corrigiu uma nota recusada pela sefás e emitiu uma devolução e uma complementar.
Cancelou uma nota, mandou uma carta de correção, inutilizou os números que tinham ficado em aberto e baixou o dânfi e o xis-ême-éle.
E ativou as notas recebidas, confirmou uma operação e importou uma nota pelo xis-ême-éle.
Quem usa o Cáto também pode pedir a nota de um pedido pela conversa, e isso fica no tutorial do Cáto. No próximo, o documento que acompanha a carga na estrada e o pacote que o contador pede. Até lá!""",
}
# Títulos dos capítulos (vinheta), na grafia de pronúncia.
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
           11: "Impostos e as outras abas.",
           12: "Nota de um caixa fechado.",
           13: "Outras operações.",
           14: "O que trava a emissão.",
           15: "A sefás recusou a nota.",
           16: "Cancelar e corrigir.",
           17: "Nota de devolução.",
           18: "Nota complementar.",
           19: "Inutilizar numeração.",
           20: "dânfi e xis-ême-éle.",
           21: "As notas recebidas.",
           22: "Manifestar a nota.",
           23: "Importar pelo xis-ême-éle.",
           24: "Recapitulando."}
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
           11: "Impostos",
           12: "Emissão",
           13: "Emissão",
           14: "Emissão",
           15: "Rejeição",
           16: "Correções",
           17: "Devolução",
           18: "Complementar",
           19: "Numeração",
           20: "Documentos",
           21: "Notas recebidas",
           22: "Notas recebidas",
           23: "Notas recebidas",
           24: "Resumo"}

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
