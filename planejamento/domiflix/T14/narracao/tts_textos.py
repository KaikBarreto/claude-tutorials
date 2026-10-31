# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T14 "Notas Fiscais".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 4: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   NBS -> "ene-bê-ésse" | ISS -> "i-ésse-ésse" | XML -> "xis-eme-éle" | A1 -> "á um" | NFS-e -> "ene-éfe-ésse-é" | NF-e -> "ene-éfe-é" | PMOC -> "pê-móqui" | PDF -> "pê-dê-éfe" | DRE -> "dê érri ê"
CAPS = {
0: """Oi! Neste tutorial a gente vai emitir a nota fiscal do serviço direto da Dominex e acompanhar as notas que os fornecedores emitem pra sua empresa.
A configuração fiscal é feita uma vez só. Depois, cada nota sai em poucos cliques, com os códigos e os impostos já preenchidos.
As notas fazem parte do módulo Emissão de Notas Fiscais. Com ele contratado, o item Notas Fiscais aparece aqui no menu.
Se você ainda não viu o tutorial Relatório Financeiro e dê érri ê, dá uma olhada antes. [pause] Vamos entender as duas notas.""",
1: """Esta tela cuida de duas notas. A ene-éfe-ésse-é é a nota fiscal de serviço, que a sua empresa emite pro cliente depois do atendimento.
A ene-éfe-é é a nota de produto, que o fornecedor emite quando você compra dele. Ela chega aqui sozinha, pelo CNPJ da empresa.
Nas abas ficam as notas emitidas, o relatório das últimas, as emissões automáticas dos contratos e as notas recebidas. E o selo mostra quantas notas já saíram no mês.""",
2: """Antes da primeira nota, a configuração. Em Configurações fiscais são quatro passos, e o primeiro é a empresa.
O nome e o CNPJ já vêm do cadastro da empresa. A Inscrição Municipal é o número da empresa na prefeitura, e é ela que permite o registro pra emitir.
No endereço fiscal, o CEP preenche a rua, o bairro, a cidade e o código do município.
No ambiente de emissão, a gente fica em Homologação, que emite notas de teste, sem valor fiscal. Com tudo conferido, é só trocar pra Produção, e aí as notas valem de verdade.
Uma dica: confere se o município está liberado antes de tudo, assim a nota passa direto. Clico em Verificar cobertura do município, e Niterói está liberado.
Clico em Salvar dados da empresa, e ela fica registrada pra emissão. Repara que esses dados valem também pro cadastro da empresa, no sistema todo.""",
3: """Com a empresa registrada, vem o certificado digital á um. É ele que assina as notas: é só enviar aqui pra liberar a emissão. Escolho o arquivo do certificado.
Dou um nome pra ele e digito a senha, que é a do próprio certificado, e não a do sistema.
Antes de enviar, a autorização. O certificado fica guardado com criptografia e só serve pra assinar as notas que a sua empresa mandar emitir.
Clico em Enviar certificado. A tela mostra até quando ele vale, e a empresa já está apta a emitir.
E cada uso do certificado fica registrado aqui embaixo, a começar por este envio.""",
4: """Com o certificado no lugar, falta dizer como a empresa paga imposto. A Glacial é do Simples Nacional. Na apuração, a primeira opção já vem marcada, e é a da maioria das empresas do Simples.
No percentual de tributos do Simples vai o número que o seu contador passa. Aqui, seis por cento. Ele entra sozinho em toda nota nova.
Clico em Salvar tributação.""",
5: """O último passo são os serviços. É a mesma lista de tipos de serviço das ordens de serviço, e com os códigos preenchidos uma vez, toda nota já sai pronta.
A higienização ainda não tem código. Abro ela na aba Fiscal e escolho o código do serviço, o código municipal, de três dígitos, e o código ene-bê-ésse, da Nomenclatura Brasileira de Serviços.
A alíquota do i-ésse-ésse fica em branco, porque a Glacial é do Simples e o i-ésse-ésse não é retido. Se a sua empresa não for do Simples, a alíquota da prefeitura vai aqui. Salvo.""",
6: """Tudo pronto, bora emitir a primeira nota. É a da limpeza dos splits do Restaurante Sabor da Serra, que pagou pelo link. Clico em Nova Nota.
Em Pessoas, a data de competência já vem com hoje, o dia do serviço, e o regime de apuração em Competência. O tomador é o cliente, o restaurante.
Pra emitir, o cliente precisa ter CPF ou CNPJ e endereço no cadastro. Esses dados ficam na aba Fiscal da ficha do cliente.
Em Serviço, escolho a Higienização de Split, que agora está entre os prontos pra emitir. Os códigos fiscais vêm todos do cadastro.
Na discriminação, eu conto o que foi feito. É o texto que aparece na nota.""",
7: """Em Valores, o valor do serviço: quatrocentos e cinquenta reais. Sem retenção, a alíquota fica em branco, do jeito que a prefeitura pede pro Simples, e o aviso amarelo lembra disso.
O percentual do Simples veio da tributação que a gente salvou, e a prévia mostra o cálculo antes de emitir.
Na última aba, a pré-visualização, com a empresa, o cliente, o serviço e os valores. O número só sai depois da emissão.
Tá tudo certo, então clico em Emitir ene-éfe-ésse-é, e a nota vai pra prefeitura.""",
8: """A tela acompanha a resposta da prefeitura. Pronto, a nota foi autorizada, com número, protocolo e chave de acesso.
No Ver pê-dê-éfe, a nota abre aqui mesmo. Como foi emitida em homologação, ela sai marcada sem valor fiscal. Em produção, sai a nota que vale.
O xis-eme-éle também fica aqui, e o histórico guarda cada passo da nota.
Na lista, a nota está Autorizada. O menu dela tem o Baixar pê-dê-éfe e o Baixar xis-eme-éle, pra mandar pro cliente ou pro contador.""",
9: """E se a nota ainda não estiver pronta, ou precisar ser desfeita? A da academia fica pra depois do serviço do mês. Começo a nota e clico em Salvar rascunho.
O rascunho não vai pra prefeitura. Depois é só continuar preenchendo e emitir, ou excluir.
A nota autorizada se cancela no Cancelar nota, com um motivo, que é obrigatório e vai junto pra prefeitura.
A nota cancelada continua na lista com o número dela, e uma nota nova sai com outro número. Esta aqui está certa, então eu volto.""",
10: """Pra contrato que se repete todo mês, dá pra deixar a nota sair sozinha. No contrato pê-móqui do hotel, a aba Financeiro tem a Nota fiscal automática.
Ligo e escolho quando a nota sai: num dia fixo, no vencimento da parcela ou quando o cliente pagar. Aqui, no vencimento. Na descrição, o texto que vai na nota.
Como esse contrato não tem tipo de serviço, os dados fiscais vão aqui mesmo. E a tela salva sozinha.
No vencimento de cada parcela, a nota sai sozinha, e dá pra acompanhar tudo na aba Emissões automáticas.""",
11: """Agora o caminho inverso, as notas que chegam pra você. Em Notas recebidas, a ene-éfe-é dos fornecedores é consultada direto na Receita Federal, pelo CNPJ da empresa.
Clico em Ligar recebimento automático. Ele só precisa do certificado que a gente enviou.
No Sincronizar, chegou uma nota nova, de uma compra de material na Cobre Sul Suprimentos. Por enquanto, só tem o resumo dela.""",
12: """Pra liberar a nota completa, eu manifesto. São quatro respostas, e a mais comum é dar ciência da operação, que avisa a Receita que você sabe da nota.
A manifestação vai pra Receita e é definitiva. Com a resposta dela, chega a nota completa.
Agora a compra vira conta a pagar. A nota já traz o vencimento combinado com o fornecedor.
O formulário já vem com a descrição, o valor de mil cento e oitenta reais, o fornecedor e o vencimento. Escolho a categoria, a conta e a forma de pagamento, e salvo. A nota ficou marcada como Lançada.
E o Ver lançamento abre essa despesa direto nas Movimentações do Financeiro.""",
13: """Pronto! Recapitulando: em Configurações fiscais, você registrou a empresa, enviou o certificado, definiu a tributação e deixou os serviços com código.
Emitiu a nota de serviço em quatro abas, viu a autorização e abriu o pê-dê-éfe. O rascunho espera a hora certa, e o cancelamento pede um motivo.
No contrato, a nota sai sozinha a cada parcela. E as notas dos fornecedores chegam pelo CNPJ, recebem a ciência e viram conta a pagar.
Com o dinheiro e as notas em dia, o próximo passo é a equipe. No próximo tutorial, a gente vê o financeiro de cada funcionário e o ponto eletrônico. Até lá!""",
}

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
        print(f"cap {k:2d}: {len(v):5d} chars, {w:4d} palavras, ~{w/2.6:5.1f} s")
    tit = sum(len(v) for v in TITULOS.values())
    print("total chars CAPS", tot, "| TITULOS", tit, "| soma", tot + tit, "| palavras", pal, f"| ~{pal/2.6/60:.1f} min de fala")
