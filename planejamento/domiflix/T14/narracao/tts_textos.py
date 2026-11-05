# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T14 "Notas Fiscais".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 4: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   NBS -> "ene-bê-ésse" | ISS -> "i-ésse-ésse" | XML -> "xis-eme-éle" | A1 -> "á um" | NFS-e -> "ene-éfe-ésse-é" | NF-e -> "ene-éfe-é" | PMOC -> "pê-móqui" | PDF -> "pê-dê-éfe" | DRE -> "dê érri ê"
# Revisão 1.38.24 (05/11, fase 1): capítulos 2, 3, 8 e 13 reescritos inteiros (voz nova, um nó por capítulo);
#   cap 0 L4 e cap 10 L3 trocados por emenda (narracao/emendas_1_38_24.json). Os demais capítulos mantêm a voz de 04/11.
CAPS = {
0: """Oi! Neste tutorial a gente vai emitir a nota fiscal do serviço direto da Dominex e acompanhar as notas que os fornecedores emitem pra sua empresa.
A configuração fiscal é feita uma vez só. Depois, cada nota sai em poucos cliques, com os códigos e os impostos já preenchidos.
As notas fazem parte do módulo Emissão de Notas Fiscais. Com ele contratado, o item Notas Fiscais aparece aqui no menu.
Se você ainda não viu o tutorial Integração com WhatsApp, dá uma olhada antes. [pause] Vamos entender as duas notas.""",
1: """Esta tela cuida de duas notas. A ene-éfe-ésse-é é a nota fiscal de serviço, que a sua empresa emite pro cliente depois do atendimento.
A ene-éfe-é é a nota de produto, que o fornecedor emite quando você compra dele. Ela chega aqui sozinha, pelo CNPJ da empresa.
Nas abas ficam as notas emitidas, o relatório das últimas, as emissões automáticas dos contratos e as notas recebidas. E o selo mostra quantas notas já saíram no mês.""",
2: """Antes da primeira nota, a configuração. Em Configurações fiscais são quatro abas, e o painel no alto mostra o que ainda falta pra emitir.
O nome e o CNPJ já vêm do cadastro da empresa. A Inscrição Municipal é o número da empresa na prefeitura, e sem ela não dá pra emitir.
No endereço fiscal, o CEP preenche a rua, o bairro, a cidade e o código do município.
No ambiente de emissão, a gente fica em Homologação, que emite notas de teste, sem valor fiscal. Com tudo conferido, é só trocar pra Produção, e aí as notas valem de verdade.
Repara que o Verificar cobertura do município ainda está travado. A consulta é feita com o certificado, então fica pra depois do envio.
Clico em Salvar dados fiscais. Esses dados valem também pro cadastro da empresa, no sistema todo, e a tela já passa pro certificado.""",
3: """Com os dados salvos, vem o certificado digital á um. É ele que assina as notas: é só enviar aqui pra liberar a emissão. Escolho o arquivo do certificado.
Dou um nome pra ele e digito a senha, que é a do próprio certificado, e não a do sistema.
Antes de enviar, a autorização. O certificado fica guardado com criptografia e só serve pra assinar as notas que a sua empresa mandar emitir.
Clico em Enviar certificado. A tela volta pra aba Empresa e confere sozinha o município, que está liberado. O painel mostra até quando o certificado vale, e a empresa já está apta a emitir.
E na aba do certificado, cada uso dele fica registrado: o envio e a consulta do município.""",
4: """Com o certificado no lugar, falta dizer como a empresa paga imposto. A Glaciál é do Simples Nacional. Na apuração, a primeira opção já vem marcada, e é a da maioria das empresas do Simples.
No percentual de tributos do Simples vai o número que o seu contador passa. Aqui, seis por cento. Ele entra sozinho em toda nota nova.
Clico em Salvar tributação.""",
5: """O último passo são os serviços. É a mesma lista de tipos de serviço das ordens de serviço, e com os códigos preenchidos uma vez, toda nota já sai pronta.
A higienização ainda não tem código. Abro ela na aba Fiscal e escolho o código do serviço, o código municipal, de três dígitos, e o código ene-bê-ésse, da Nomenclatura Brasileira de Serviços.
A alíquota do i-ésse-ésse fica em branco, porque a Glaciál é do Simples e o i-ésse-ésse não é retido. Se a sua empresa não for do Simples, a alíquota da prefeitura vai aqui. Salvo.""",
6: """Tudo pronto, bora emitir a primeira nota. É a da limpeza dos splits do Restaurante Sabor da Serra, que pagou pelo link. Clico em Nova Nota.
Em Pessoas, a data de competência já vem com hoje, o dia do serviço, e o regime de apuração em Competência. O tomador é o cliente, o restaurante.
Pra emitir, o cliente precisa ter CPF ou CNPJ e endereço no cadastro. Esses dados ficam na aba Fiscal da ficha do cliente.
Em Serviço, escolho a Higienização de Split, que agora está entre os prontos pra emitir. Os códigos fiscais vêm todos do cadastro.
Na discriminação, eu conto o que foi feito. É o texto que aparece na nota.""",
7: """Em Valores, o valor do serviço: quatrocentos e cinquenta reais. Sem retenção, a alíquota fica em branco, do jeito que a prefeitura pede pro Simples, e o aviso amarelo lembra disso.
O percentual do Simples veio da tributação que a gente salvou, e a prévia mostra o cálculo antes de emitir.
Na última aba, a pré-visualização, com a empresa, o cliente, o serviço e os valores. O número só sai depois da emissão.
Tá tudo certo, então clico em Emitir ene-éfe-ésse-é, e a nota vai pra prefeitura.""",
8: """A resposta da prefeitura chega na hora. No Ver detalhe, a nota está autorizada, com número e chave de acesso.
Mais embaixo, o histórico guarda cada passo da nota, a começar pela emissão.
Na lista, o menu da nota tem o Baixar pê-dê-éfe, pra mandar pro cliente ou pro contador.
Como a nota foi emitida em homologação, o pê-dê-éfe sai marcado sem valor fiscal. Em produção, sai a nota que vale.""",
9: """E se a nota ainda não estiver pronta, ou precisar ser desfeita? A da academia fica pra depois do serviço do mês. Começo a nota e clico em Salvar rascunho.
O rascunho não vai pra prefeitura. Depois é só continuar preenchendo e emitir, ou excluir.
A nota autorizada se cancela no Cancelar nota, com um motivo, que é obrigatório e vai junto pra prefeitura.
A nota cancelada continua na lista com o número dela, e uma nota nova sai com outro número. Esta aqui está certa, então eu volto.""",
10: """Pra contrato que se repete todo mês, dá pra deixar a nota sair sozinha. No contrato pê-móqui do hotel, a aba Financeiro tem a Nota fiscal automática.
Ligo e escolho quando a nota sai: num dia fixo, no vencimento da parcela ou quando o cliente pagar. Aqui, no vencimento. Na descrição, o texto que vai na nota.
Os dados fiscais vêm do tipo de serviço do contrato, a Manutenção Preventiva. Só falta o código ene-bê-ésse, que eu escolho aqui, e a tela salva sozinha.
No vencimento de cada parcela, a nota sai sozinha, e dá pra acompanhar tudo na aba Emissões automáticas.""",
11: """Agora o caminho inverso, as notas que chegam pra você. Em Notas recebidas, a ene-éfe-é dos fornecedores é consultada direto na Receita Federal, pelo CNPJ da empresa.
Clico em Ligar recebimento automático. Ele só precisa do certificado que a gente enviou.
No Sincronizar, chegou uma nota nova, de uma compra de material na Cobre Sul Suprimentos. Por enquanto, só tem o resumo dela.""",
12: """Pra liberar a nota completa, eu manifesto. São quatro respostas, e a mais comum é dar ciência da operação, que avisa a Receita que você sabe da nota.
A manifestação vai pra Receita e é definitiva. Com a resposta dela, chega a nota completa.
Agora a compra vira conta a pagar. A nota já traz o vencimento combinado com o fornecedor.
O formulário já vem com a descrição, o valor de mil cento e oitenta reais, o fornecedor e o vencimento. Escolho a categoria, a conta e a forma de pagamento, e salvo. A nota ficou marcada como Lançada.
E o Ver lançamento abre essa despesa direto nas Movimentações do Financeiro.""",
13: """Pronto! Recapitulando: em Configurações fiscais, você salvou os dados da empresa, enviou o certificado, definiu a tributação e deixou os serviços com código.
Emitiu a nota de serviço em quatro abas, com a autorização na hora e o pê-dê-éfe pra mandar. O rascunho espera a hora certa, e o cancelamento pede um motivo.
No contrato, a nota sai sozinha a cada parcela. E as notas dos fornecedores chegam pelo CNPJ, recebem a ciência e viram conta a pagar.
Com as notas em dia, falta acompanhar tudo de cima. No próximo tutorial, o último da trilha, a gente lê o Dashboard, os relatórios e as exportações. Até lá!""",
}

# Capítulos que mudaram na revisão 1.38.24 (voz nova): inteiros = um nó por capítulo; emendas = narracao/emendas_1_38_24.json.
REGERAR_INTEIROS = [2, 3, 8, 13]
EMENDAS_1_38_24 = {0: [4], 10: [3]}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "A nota do serviço.",
           2: "Os dados da empresa.",
           3: "O certificado digital.",
           4: "A tributação.",
           5: "Os serviços com código.",
           6: "Pessoas e serviço.",
           7: "Valores e emissão.",
           8: "Nota autorizada.",
           9: "Rascunho e cancelamento.",
           10: "Nota automática do contrato.",
           11: "As notas dos fornecedores.",
           12: "Ciência e conta a pagar.",
           13: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Notas fiscais",
           2: "Configuração",
           3: "Configuração",
           4: "Configuração",
           5: "Configuração",
           6: "Emissão",
           7: "Emissão",
           8: "Emissão",
           9: "Emissão",
           10: "Notas fiscais",
           11: "Notas recebidas",
           12: "Notas recebidas",
           13: "Resumo"}

if __name__ == "__main__":
    tot = 0
    pal = 0
    for k, v in CAPS.items():
        w = len(v.replace("[pause]", "").split())
        tot += len(v)
        pal += w
        marca = " (inteiro, voz nova)" if k in REGERAR_INTEIROS else (f" (emenda L{EMENDAS_1_38_24[k]})" if k in EMENDAS_1_38_24 else "")
        print(f"cap {k:2d}: {len(v):5d} chars, {w:4d} palavras, ~{w/2.6:5.1f} s{marca}")
    tit = sum(len(v) for v in TITULOS.values())
    print("total chars CAPS", tot, "| TITULOS", tit, "| soma", tot + tit, "| palavras", pal, f"| ~{pal/2.6/60:.1f} min de fala")
    nova = sum(len(CAPS[k]) for k in REGERAR_INTEIROS)
    print("caracteres de voz nova: inteiros", nova, "(caps", ", ".join(map(str, REGERAR_INTEIROS)) + ")")
