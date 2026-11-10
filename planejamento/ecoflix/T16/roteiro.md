# Roteiro T16 · Nota Fiscal de mercadoria (NF-e)

Roteiro pronto para a voz e a gravação (sem etapa de aprovação, como na Domiflix; o Kaik ajusta depois). Coluna Fala =
texto da narração (voz Kaik Barreto) na grafia da legenda; a grafia de pronúncia vai em `narracao/tts_textos.py`, gerado
desta coluna (uma linha da tabela = uma linha da fala). Coluna Tela = o que o robô faz e onde a câmera foca, com os
rótulos entre aspas como no código da 1.59.154 (`inventario.md`).
Aula no computador (janela 1280×800, tema claro), logado como Rafael Nogueira (MASTER). Todo capítulo parte de um
navegador novo com o mundo do fim do capítulo anterior (sementes `seeds-extra/t16/apos-capNN.json`); quando um capítulo
continua uma tela, o `setup` do robô a reabre fora do vídeo. Emissão, certificado, SEFAZ, provedor e notas recebidas
são simulados no backend falso (`plano.md`, "Gravação"): nenhum certificado, CNPJ, chave ou protocolo real.

- **Título:** Nota Fiscal de mercadoria (NF-e)
- **Antes:** Relatório Financeiro e DRE (T15)
- **Próximo:** Transporte, serviço e o contador (T17)
- **Vinhetas (áreas):** FISCAL · CONFIGURAÇÃO · CERTIFICADO · CONFIGURAÇÃO · CENÁRIOS · NUMERAÇÃO · CONFIGURAÇÃO · COTA ·
  EMISSÃO · EMISSÃO · EMISSÃO · CORREÇÕES · NUMERAÇÃO · DOCUMENTOS · NOTAS RECEBIDAS · NOTAS RECEBIDAS · NOTAS RECEBIDAS ·
  RESUMO (todo capítulo menos o 00)
- **Duração estimada:** ~22 min de vídeo (2.853 palavras de fala, ~18,3 min a 2,6 palavras/s; mais a vinheta de abertura,
  18 vinhetas de ~3,5 s, a cartela, as esperas de tela como o "Aguardando SEFAZ" e o "Processando a nota", e os
  preenchimentos acelerados). Alvo da fonte: ~25 min; como na Domiflix, a fala natural fecha abaixo.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos. Regime do exemplo: Lucro Real.
- **Sementes:** `inicio` (sem certificado nem configuração fiscal; entrada dos capítulos 00 a 03), `apos-cap03`,
  `apos-cap04`, `apos-cap05`, `apos-cap06`, `apos-cap07` (entrada do 08 e do 09), `apos-cap09`, `apos-cap10`, `apos-cap11`,
  `apos-cap12`, `apos-cap13` (entrada do 14), `apos-cap14`, `apos-cap15`, `apos-cap16`; valores em `plano.md`, "Mundo".
- Marcas na Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[ZOOM: ...]` (dura a frase inteira, ≥ 2,5 s,
  sem zoom em cima de zoom), `[ILUSTRAÇÃO: ...]` (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`; nunca tela do
  app), "trecho acelerado" (preenchimento sem fala nova, selo 4x).
- O que a fonte pede e o código não confirma (fica fora da fala): o aviso IBS/CBS fixo no topo e o nome sem acento no XML
  (`inventario.md`, seção 14).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Nota Fiscal de mercadoria (NF-e)". | (sem fala) |
| [ILUSTRAÇÃO: Carga e nota: o pátio da Recicla Vale Metais (galpão genérico, montes de sucata); um caminhão genérico é carregado com cobre; na palavra "autorizada", uma folha de nota com um visto verde aparece ao lado do caminhão] | Oi! Neste tutorial a gente vai do certificado digital até a nota fiscal autorizada, na Recicla Vale Metais. |
| (a ilustração continua: o caminhão vai até um prédio genérico rotulado "Fundição"; na frase "só sai do pátio com a nota", a folha pousa sobre a carga e o caminhão parte) | A Fundição Bandeira do Vale compra cobre dela toda semana. E a carga só sai do pátio com a nota fiscal de mercadoria, a NF-e. |
| Dashboard da Recicla Vale Metais, logado como Rafael Nogueira; cartão discreto "Módulo Notas Fiscais". [BACKEND: semente `inicio`] | As notas fazem parte do módulo Notas Fiscais. Se ele estiver no seu plano, tudo fica em Fiscal & Ambiental. |
| Cartão discreto "Antes: Relatório Financeiro e DRE". | Se você ainda não viu o tutorial Relatório Financeiro e DRE, dá uma olhada antes. [pause] É a parte mais delicada do sistema, então a gente vai devagar e na ordem. |

### cap01 · Onde ficam as notas (vinheta: FISCAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), no Dashboard; a câmera desce ao menu lateral e clica em "Fiscal & Ambiental": o submenu abre. | Tudo começa no menu, em Fiscal & Ambiental. |
| Zoom no submenu: "Notas Fiscais (NF-e)", "Notas de Serviço (NFS-e)", "Transporte (MDF-e)", "Ambiental (MTR/CDF)" e "Estoque Fiscal" (sem passar o mouse no "SPED Fiscal", que está fora da trilha). | Aqui ficam as telas fiscais: as notas de mercadoria, as de serviço, o transporte, o ambiental e o estoque fiscal. Hoje a gente fica nas notas de mercadoria. |
| Clique em "Notas Fiscais (NF-e)": a tela "Notas Fiscais (NF-e)" ("Gerenciamento de documentos fiscais eletrônicos") abre na sub-aba "Entrada", com "Notas Fiscais de Entrada" e "Nenhuma nota fiscal de entrada encontrada". | Clico em Notas Fiscais, NF-e. |
| Zoom nas sub-abas "Entrada", "Saída", "Notas Recebidas" e "Inutilizadas". | Em cima ficam as sub-abas: Entrada, Saída, Notas Recebidas e Inutilizadas. |
| [ILUSTRAÇÃO: Entrada × saída: no centro, o pátio; à esquerda, uma catadora genérica com o carrinho de latinhas chega ao pátio, seta "Entrada"; à direita, o caminhão sai do pátio para a fundição, seta "Saída"; cada seta ganha uma folha de nota na sua palavra] | Saída é a nota da venda, quando a mercadoria sai do pátio pro cliente. Entrada é a da compra, quando ela chega do fornecedor. |
| A câmera volta à tela; zoom em "Notas Recebidas" e "Inutilizadas". | Notas Recebidas são as que os fornecedores emitem contra o seu CNPJ, e Inutilizadas guarda os números fechados. Cada uma tem a sua parte neste tutorial. |
| A câmera passa por "Configurações Fiscais" e pelo selo "0/100 Documentos" (no alto, à direita), depois pelos cartões "Notas Emitidas", "Notas Pendentes" e "Rejeitadas/Canceladas", e para em "Nova Nota" (sem clicar). | Do lado direito ficam as Configurações Fiscais e a cota do mês. Embaixo, os cartões das notas emitidas, pendentes e rejeitadas ou canceladas. E o botão Nova Nota. |

### cap02 · O certificado vem primeiro (vinheta: CONFIGURAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`) na tela "Notas Fiscais (NF-e)"; clique em "Configurações Fiscais": abre a página "Configuração Fiscal" ("Tudo que a SEFAZ precisa saber antes da primeira nota."), na seção "Certificado". | Antes de qualquer nota, a configuração. Ela fica no botão Configurações Fiscais e é tudo o que a SEFAZ, a Secretaria da Fazenda do estado, precisa saber antes da primeira nota. |
| Zoom no trilho da esquerda: "Emissão" ("Certificado", "Empresa"), "Regras fiscais" ("Impostos (padrão)", "Cenários") e "Documentos" ("Numeração", "Transportadora", "Serviços"). | Na esquerda ficam as seções, em três grupos: emissão, regras fiscais e documentos. |
| Zoom em "Empresa", "Impostos (padrão)", "Numeração" e "Transportadora", apagados, com "precisa do certificado digital" embaixo de cada um. | Repara que Empresa, Impostos, Numeração e Transportadora estão apagados, com o aviso precisa do certificado digital. |
| [ILUSTRAÇÃO: O certificado assina a nota: uma folha de nota com os itens do pátio; um cartão "Certificado digital" com "CNPJ" desliza e deixa uma assinatura na folha, na palavra "assina"; a folha segue para o prédio "SEFAZ"; na frase "nada chega", uma folha sem assinatura bate numa barreira e volta] | É o certificado digital que assina a nota, como a assinatura da empresa. Sem ele, nada do que for preenchido aqui chega na SEFAZ. |
| Zoom no aviso "Passo 1 de 3: Configure primeiro o certificado digital."; [ILUSTRAÇÃO curta, sobre o palco: três cartões numerados entram em ordem, cada um na sua palavra: "1 Certificado", "2 Empresa", "3 Impostos"] | Por isso a ordem está na própria tela. Passo um, o certificado. Passo dois, os dados da empresa. Passo três, os impostos. |
| A câmera volta ao cartão "Certificado Digital A1". | Uma dica: faça essa configuração junto com o contador. Um campo errado aqui faz a SEFAZ recusar a nota na hora de emitir. |

### cap03 · Subindo o certificado A1 (vinheta: CERTIFICADO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`) em "Configuração Fiscal" › "Certificado": "Certificado Digital A1" ("Necessário para assinar e transmitir notas fiscais") e "Certificado não configurado". | Então, o certificado. A NF-e usa o certificado A1, que é um arquivo de computador com uma senha. |
| Em "Arquivo do Certificado (.pfx ou .p12)", clique em "Selecionar arquivo"; o robô entrega `recicla-vale-metais-a1.pfx` ao campo (sem janela do sistema) e o botão passa a mostrar o nome do arquivo. [BACKEND: arquivo falso, < 200 KB] | Em Arquivo do Certificado, clico em Selecionar arquivo e escolho o arquivo ponto pfx da Recicla Vale. |
| Em "Senha do Certificado" ("Digite a senha do certificado") digita a senha fictícia (só pontos); zoom na ajuda "Use a senha do próprio certificado digital, não a senha da empresa.". | Em Senha do Certificado vai a senha do próprio arquivo, e não a senha da empresa. |
| Clique em "Validar Certificado" ("Validando..."): toast "Certificado validado com sucesso!"; o cartão vira "Certificado validado!" com "Configure os dados da empresa". [BACKEND: edge `plugnotas-upload-certificate` devolve `success` e `vaultStored` true; `plugnotas-certificate-info` devolve o certificado do "Mundo"; RPC `certificate_vault_status` com `presente` true] | Clico em Validar Certificado. Pronto: certificado validado. |
| [ZOOM: o nome "RECICLA VALE METAIS LTDA" e o chip "Válido até 14/09/2027", a frase inteira] | Embaixo aparece até quando ele vale: catorze de setembro de dois mil e vinte e sete. |
| [ILUSTRAÇÃO: Régua de um ano: uma régua do tempo com doze meses; o cartão "A1 do CNPJ" cabe dentro de um ano; outro cartão, "certificado da certificadora", estica por vários anos e ganha um ponto âmbar na frase "a validade não confere"; na palavra "errado", o segundo cartão sai e o primeiro fica] | Uma dica: o A1 vale no máximo um ano. Se a tela disser que a validade não confere, quase sempre foi enviado o arquivo errado, o da certificadora, e não o do CNPJ. |
| Zoom em "Substituir Certificado" e em "Próximo: Configurar Empresa" (sem clicar). | Aí é pedir o arquivo certo ao contador e usar o Substituir Certificado. E o botão Próximo leva pra empresa. |

### cap04 · Empresa e impostos (vinheta: CONFIGURAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`) em "Certificado" ("Certificado validado!"); clique em "Próximo: Configurar Empresa": seção "Empresa", com o aviso "Passo 2 de 3: Preencha os dados da empresa para NF-e.". | Com o certificado validado, os dados da empresa. É o passo dois. |
| Em "Dados da Empresa", clique em "Importar dados": toast "Dados importados! Revise e complete as informações antes de salvar."; "Razão Social *", "Nome Fantasia", "CNPJ *", "Telefone" e "E-mail" preenchidos com o cadastro. | O Importar dados traz o que já está no cadastro da empresa: o nome, o CNPJ, o telefone e o e-mail. |
| Em "Razão Social *" completa "Recicla Vale Metais Ltda"; em "Inscrição Estadual" digita 688.047.314.106. [ZOOM: "CNPJ *" e "Inscrição Estadual", a frase inteira] | Confiro a razão social completa e digito a inscrição estadual. O CNPJ daqui é o que vai como emitente em toda nota. |
| A câmera desce a "Endereço Fiscal" (o endereço do cadastro, em Taubaté) e para em "Editar em Configurações › Empresa". | O endereço fiscal vem do cadastro da empresa, o mesmo do comprovante. Pra mudar, é em Configurações, Empresa. |
| Clique em "Impostos (padrão)" ("usado quando nenhum cenário se aplica"): aviso "Passo 3 de 3: Selecione o regime tributário. Os campos serão ajustados automaticamente."; em "Regime Tributário *" abre a lista e escolhe "Lucro Real". | Passo três, os impostos. Primeiro, o regime tributário. A Recicla Vale é Lucro Real, e quem define isso é o contador. |
| Aparece o quadro "Lucro Real:" ("PIS: 1,65% \| COFINS: 7,60% (Regime Não Cumulativo)", "ICMS destacado conforme CST", "Gera direito a crédito de PIS/COFINS", "Possibilidade de apuração de IPI"). [ZOOM: o quadro "Lucro Real:", a frase inteira] | Olha: escolhido o regime, a tela já ajusta os campos de PIS e COFINS. |
| A câmera desce por "Contribuinte de ICMS" (ligado) e "Alíquota do ICMS interno, sem o FCP (%)" (18) até o bloco "ICMS" ("CST Entrada", "CST Saída"). [ZOOM: "Alíquota do ICMS interno, sem o FCP (%)", a frase inteira] | Mais embaixo vem o ICMS, o imposto do estado sobre a mercadoria, com a alíquota e os códigos que o contador passar. |
| A câmera desce até "CFOPs Padrão" ("CFOP Entrada Interna" 1102, "CFOP Entrada Interestadual" 2102, "CFOP Saída Interna" 5102, "CFOP Saída Interestadual" 6102, "CFOP Saída Indústria" 5101, "CFOP Saída Exportação" 5502). | Depois, o CFOP padrão de cada operação. O CFOP é o código que diz que tipo de nota é aquela: uma venda, uma compra, uma devolução. |
| Desce até "Reforma Tributária (IBS/CBS)"; liga "Calcular IBS e CBS automaticamente"; em Saída e em Entrada digita "CST-IBS/CBS" 000 e "cClassTrib" 000001 (trecho acelerado). | No fim, a Reforma Tributária. Ligado o cálculo do IBS e da CBS, o sistema calcula esses tributos sozinho, com os códigos que o contador passar. |
| [ILUSTRAÇÃO: O padrão vale para toda nota: o contador (figura genérica) entrega uma folha "Impostos (padrão)"; ela vira um carimbo que marca, uma a uma, três notas ("venda de cobre", "venda de alumínio", "compra de latinha"); na frase "toda nota", as três ficam carimbadas] | Tudo isso é o padrão. Ele vale pra toda nota em que nenhum cenário se aplica. |
| Rodapé "Alterações não salvas"; clique em "Salvar configuração" ("Cadastrando..."): toasts "Configurações fiscais salvas!" e "Empresa cadastrada no sistema de NF-e!"; o rodapé volta a "Sem alterações pendentes". [BACKEND: `company_fiscal_config` atualizado; edge `plugnotas-register-company` devolve `success` sem `message`] | Clico em Salvar configuração. Pronto: a empresa está cadastrada pra emitir NF-e. |

### cap05 · Cenários fiscais (vinheta: CENÁRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`); "Configuração Fiscal" › "Cenários": "Cenários fiscais" ("Defina as condições da operação e o tratamento que entra na nota. Sem cenário aplicável, a configuração de Impostos continua valendo.") e o vazio "Nenhum cenário cadastrado". | E quando uma venda não segue o padrão? Pra isso existem os cenários. Um cenário é uma exceção ao padrão, que só vale numa situação certa. |
| Zoom no aviso fixo "O que você preenche aqui vai impresso na nota fiscal. Confirme com a sua contabilidade..." (até "recomendação fiscal."). | O aviso de cima vale pra todos os cenários: o que você preenche aqui vai impresso na nota. O EcoSistema não faz recomendação fiscal, então confirme tudo com a contabilidade. |
| Clique em "Criar o primeiro cenário"; em "Nome do cenário *" digita "Venda para a Fundição Bandeira do Vale". | Por exemplo: o contador passou um tratamento próprio para as vendas à Fundição Bandeira do Vale. Clico em Criar o primeiro cenário e dou um nome que diga a situação. |
| Em "Etapa 1" › "Quando aplicar" ("O cenário só entra quando a nota bate com todas estas condições. ..."): "Operação *" = "Venda"; "Cliente da nota" = "Um cliente/fornecedor específico" e digita o CNPJ da Fundição. [ZOOM: o campo do CNPJ, a frase inteira] | Em Quando aplicar ficam as condições. Aqui, a operação é venda, e o cliente é um só: a Fundição, pelo CNPJ. O resto fica em Qualquer. |
| Em "Etapa 2" › "O que aplicar" ("Preencha só o que muda neste cenário. Campo em branco não é zero nem desligado: ..."): "CST do ICMS" = 51 e "Diferimento (%)" = 100; os outros campos ficam em "Usar a configuração de Impostos". | Em O que aplicar entra só o que muda, do jeito que o contador passou. Campo em branco não é zero: ele continua vindo do padrão. |
| Clique em "Criar cenário": toast "Cenário criado"; a lista "Regras cadastradas" mostra "Venda · 1" com o cenário; selo "Não revisado"; zoom em "Marcar como revisado" ("Marque depois de conferir este cenário com a sua contabilidade."). | Clico em Criar cenário. Ele nasce como não revisado, e depois de conferir com a contabilidade é só marcar como revisado. |
| [ILUSTRAÇÃO: Geral × estreita: um funil com três cartões, do mais aberto ao mais estreito: "Impostos (padrão)", "Toda venda", "Venda para a Fundição"; uma nota de cobre da Fundição desce e para no cartão mais estreito, que acende na frase "vale a mais específica"] | Uma dica: não precisa criar um cenário pra cada combinação. Cadastre a regra geral e, depois, só a exceção mais estreita. Quando duas servem pra mesma nota, vale a mais específica. |

### cap06 · Série e numeração (vinheta: NUMERAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); "Configuração Fiscal" › "Numeração", sub-aba "NF-e": "Série padrão das suas notas" ("Configure qual série é usada por padrão ao emitir uma NF-e nova."). | Agora, de qual número a primeira nota sai. Toda nota tem uma série e um número. A série é a sequência, e o número sobe de um em um. |
| Zoom em "Entrada e saída usam a mesma série" (ligado, "Deixe ligado se você só usa 1 série pra tudo.") e em "Série padrão" (1). | Aqui, entrada e saída usam a mesma série, a série um. Pra quem usa uma série só, é deixar assim. |
| [ILUSTRAÇÃO: A sequência continua: uma fila de folhas numeradas 1246, 1247 e 1248 sob o rótulo "sistema antigo"; na palavra "continuar", uma seta cruza para o rótulo "EcoSistema" e a próxima folha nasce como 1249] | A Recicla Vale já emitia nota em outro sistema, na série um. A última foi a mil duzentos e quarenta e oito, então a numeração precisa continuar dali. |
| Em "Suas séries" ("Nenhuma série cadastrada ainda."), clique em "Adicionar série": diálogo "Adicionar Série"; "Número da série" 1; "Última nota emitida nessa série" 1248. [ZOOM: "Última nota emitida nessa série" com 1248, a frase inteira] | Em Adicionar série, informo a série um e a última nota emitida nela, a mil duzentos e quarenta e oito. |
| Zoom na ajuda "Se você nunca emitiu nada nessa série, deixe em 0. O sistema vai começar a próxima do nº 1.". | Se a empresa nunca emitiu nota, é deixar em zero, e a primeira sai com o número um. |
| Clique em "Adicionar": toast "Série adicionada com sucesso"; a linha "Série 1" com "Última nota emitida: 1248". [BACKEND: insere `nfe_series`] | Clico em Adicionar. Pronto: a próxima nota sai com o número mil duzentos e quarenta e nove. |

### cap07 · Transportadora e serviços (vinheta: CONFIGURAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`); "Configuração Fiscal" › "Transportadora": formulário "Nova transportadora" e "Nenhuma transportadora cadastrada". | Mais dois cadastros. Quando a carga vai com uma transportadora contratada, os dados dela vão na nota. Então a gente cadastra uma vez, e na nota é só escolher. |
| Preenche "Razão Social *" "Cargas Vale do Sol Ltda", "CPF/CNPJ" 41.826.537/0001-92, "Inscrição Estadual" 688.115.922.408, "UF" SP, "Logradouro" "Rua dos Ferroviários", "Número" 380, "Bairro" "Vila São José" e "Cidade" "Taubaté" (trecho acelerado). [ZOOM: "CPF/CNPJ", a frase inteira] | Aqui vai a Cargas Vale do Sol: razão social, CNPJ, inscrição estadual e endereço. |
| Em "Veículo": "Placa" FJR3B27 e "UF Veículo" SP. [ILUSTRAÇÃO: O caminhão na nota: um caminhão genérico com a placa FJR3B27; a placa sai do para-choque e pousa no quadro "transporte" de uma folha de nota, na palavra "placa"] | No bloco Veículo vai a placa do caminhão que costuma fazer a entrega. |
| Clique em "Adicionar": toast "Transportadora cadastrada!"; a linha "Cargas Vale do Sol Ltda • SP" com "CPF/CNPJ: ... • Placa: FJR3B27". [BACKEND: insere `transportadoras`] | Clico em Adicionar, e ela entra na lista. |
| Clique em "Serviços": botão "Novo serviço" e o vazio "Nenhum serviço cadastrado" ("Cadastre os serviços que você presta para emitir NFS-e."). | E Serviços é o cadastro da nota de serviço, a NFS-e, pra quando a empresa presta um serviço, como uma coleta. Isso fica pro próximo tutorial. |

### cap08 · A cota de documentos (vinheta: COTA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`) na tela "Notas Fiscais (NF-e)", sub-aba "Saída". [ZOOM: o selo verde "0/100 Documentos", a frase inteira] [BACKEND: `nfe_module_tiers` e `companies.nfe_tier` do "Mundo"; RPC `count_fiscal_documents_in_month` devolve 0] | Antes de emitir, a cota. Cada nível do módulo tem um limite de documentos por mês, e o selo mostra quantos já foram usados: zero de cem. |
| Passa o mouse no selo: a dica "Nível 1", "Até 100 documentos fiscais por mês.", "Você emitiu 0 neste mês." e a linha do próximo nível. | Passando o mouse, aparecem o nível contratado e quanto você emitiu no mês. O tamanho da cota depende do plano. |
| [ILUSTRAÇÃO: O que conta: ícones genéricos entram numa caixa rotulada "Cota do mês", cada um na sua palavra: "nota de mercadoria", "nota de serviço", "manifesto de transporte", "MTR", "CDF"; por último, "notas recebidas", com a etiqueta "depois de ativar"] | Toda nota que você emite conta: a de mercadoria, a de serviço, o manifesto de transporte, o MTR e o CDF. E as notas recebidas, depois que você ativa esse recurso. |
| (a ilustração continua: uma folha com o carimbo "cancelada" também entra na caixa) | Uma dica: nota cancelada continua contando. Cancelar não devolve o documento pra cota. |
| [ILUSTRAÇÃO: A barra da cota: uma barra de 0 a 100 que enche; verde até 79, âmbar a partir de 80, vermelha no 100; cada cor acende na sua palavra; depois do 100, um trecho curto marcado "+5", na palavra "cinco"] | O selo fica âmbar perto do limite e vermelho quando chega nele. Mesmo assim, ainda dá pra emitir mais cinco documentos: é a tolerância. |
| (a ilustração continua: no fim do "+5", um cadeado fecha a barra) | Só depois dos cinco a emissão trava, com o aviso Suas notas do mês acabaram. Aí é subir de nível, e vale na hora. |

### cap09 · Nota avulsa, do zero (vinheta: EMISSÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`), sub-aba "Saída" ("Notas Fiscais de Saída"); clique em "Nova Nota": "Nova Nota Fiscal" ("Selecione o tipo de nota fiscal") com os cartões "NF-e de Entrada" e "NF-e de Saída". | Agora sim, a primeira nota. A Serra Fina Alumínio Reciclagem comprou alumínio perfil e pediu a nota. Clico em Nova Nota. |
| Clique em "NF-e de Saída" ("Emitir nota fiscal de venda para cliente"): a nota abre no passo "Dados"; em cima, "Total da nota" R$ 0,00, "Itens" 0 e o selo vermelho de pendências; as abas "Dados" e "Itens" em destaque. | É uma venda, então NF-e de Saída. A nota tem dois passos: Dados e Itens. |
| Em "Para quem", no campo "Cliente" ("Buscar por nome, apelido, CPF/CNPJ ou telefone..."), digita "Serra Fina" e escolhe "Serra Fina Alumínio Reciclagem" (cadastro completo). | Em Para quem, escolho o cliente: a Serra Fina. |
| Em "O que é", "Natureza da Operação" = "Venda de mercadorias"; o "CFOP" mostra 5102. | Em O que é vai a natureza da operação: venda de mercadorias. O CFOP vem sozinho, pela natureza e pelo estado do cliente. |
| Em "Numeração": "Série" 1, "Número previsto" 1249, "Data e hora da emissão" vazia ("Padrão: agora"); embaixo, "Esta nota será emitida como Série 1 / Nº 1249". [ZOOM: "Número previsto" e "Esta nota será emitida como Série 1 / Nº 1249", a frase inteira] [BACKEND: o próximo número sai de `nfe_series` (1248 + 1)] | E a numeração: série um, número mil duzentos e quarenta e nove, como a gente configurou. A data em branco é agora. |
| Clique em "Avançar": passo "Itens", com "Produtos/Itens" e o bloco "Adicionar item". | Clico em Avançar, e vêm os itens. |
| Em "Selecionar material..." escolhe "Alumínio perfil": "NCM" 7602.00.00 e "Vl. Unit." 10,40 preenchidos; em "Qtd" digita 320. [ZOOM: "Qtd" 320 e "Vl. Unit." 10,40, a frase inteira] | Escolho o alumínio perfil. O NCM, que é o código do tipo de mercadoria, e o preço de venda vêm do cadastro. Trezentos e vinte quilos, a dez e quarenta o quilo. |
| Clique em "Incluir": toast "Item adicionado!"; a linha entra na tabela ("Vl. Total" R$ 3.328,00); em cima, "Total da nota" R$ 3.328,00 e o selo verde "Pronta pra emitir". [ZOOM: "Total da nota" e "Pronta pra emitir", a frase inteira] | Clico em Incluir. A nota fica em três mil trezentos e vinte e oito reais, e o selo de cima diz Pronta pra emitir. |
| A câmera vai ao rodapé ("Voltar", "Salvar Rascunho", "Emitir Nota"), sem clicar. | Uma dica: antes da primeira nota, confirme com o contador que o CNPJ já está credenciado na SEFAZ pra emitir NF-e. Assim a primeira nota já sai autorizada. |
| [ILUSTRAÇÃO: O caminho da nota (os quatro passos de `EmissionFlowTimeline.tsx`): 1 "Crie a nota" (a folha preenchida); 2 "Envie para a SEFAZ" (o cartão do certificado assina e a folha viaja até o prédio "SEFAZ"); 3 "Aguarde a autorização" (um relógio; volta um visto verde com três etiquetas: "número", "protocolo", "chave de acesso"); 4 "Baixe os documentos" (uma folha DANFE e um arquivo XML); os passos 1 e 2 acendem na primeira frase, o 3 em "autoriza" e o 4 em "a nota vale"] | Quando você emite, o certificado assina a nota e ela vai pra SEFAZ. A SEFAZ confere e, estando tudo certo, autoriza e devolve o protocolo. Aí sim, a nota vale. |
| Clique em "Emitir Nota": toasts "Nota fiscal salva! Enviando para SEFAZ..." e "Nota fiscal enviada para processamento!"; a nota fecha e a lista "Saída" mostra "#1249" ("Série 1") com o selo "Aguardando SEFAZ". [BACKEND: insere `invoices` e `invoice_items`; edge `plugnotas-emit` devolve `success` e `plugnotasId`] | Clico em Emitir Nota, e ela entra na lista como Aguardando SEFAZ. |
| A câmera fica na linha; em ~5 s, toast "Nota #1249 autorizada pela SEFAZ!" e o selo vira "Autorizada". [BACKEND: `plugnotas-status` devolve `statusChanged` e `status` emitida, com `nfe_key`, `nfe_protocol` e `authorized_at` do "Mundo"] | Uma dica: enviada pra processamento ainda não é autorizada. A nota só está autorizada quando aparecem o número, o protocolo e a chave de acesso. |
| Menu da linha (três pontinhos) → "Visualizar": "NF-e #1249" com o selo "Autorizada"; na aba "DANFE", a faixa verde com "Chave de Acesso" e "Protocolo". [ZOOM: "Chave de Acesso" e "Protocolo", a frase inteira] | Em Visualizar está tudo: a nota mil duzentos e quarenta e nove, autorizada, com a chave de acesso, os quarenta e quatro números que identificam a nota, e o protocolo da SEFAZ. |

### cap10 · Nota a partir de um pedido (vinheta: EMISSÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), sub-aba "Saída"; "Nova Nota" → "NF-e de Saída"; no passo "Dados", a barra "Importar de" com o botão "Pedido". | Muitas vezes a nota nasce de uma venda que já está no sistema. Hoje cedo, a Fundição Bandeira do Vale comprou cobre mel. Em vez de digitar tudo de novo, a gente puxa o pedido. |
| Clique em "Pedido": "Importar de Pedido de Venda"; no topo da lista, o pedido de hoje da "Fundição Bandeira do Vale", com o peso e R$ 23.950,00. [BACKEND: o pedido de venda do "Mundo", sem nota] | Em Importar de, clico em Pedido, e aparecem as vendas. Esta é a da Fundição. |
| Clique em "Importar": toast "Pedido importado com sucesso!"; selo "Pedido importado"; o "Cliente" vira a Fundição Bandeira do Vale e a natureza fica "Venda de mercadorias". | Clico em Importar. O cliente e os itens vêm do pedido. |
| Clique em "Avançar": no passo "Itens", a linha "Cobre mel" com "Qtd" 500, "Vl. Unit." 47,90 e "Vl. Total" R$ 23.950,00. [ZOOM: "Qtd" 500, a frase inteira] | Repara na quantidade: quinhentos quilos. A balança marcou quinhentos e seis, mas seis quilos foram de tara e impureza. |
| [ILUSTRAÇÃO: Bruto, desconto e líquido: uma balança genérica com o cobre mostra "506 kg"; uma etiqueta "tara e impureza: 6 kg" sai da pilha; o visor muda para "500 kg", que vai para a folha da nota; cada número na sua palavra] | A nota leva sempre o peso líquido, já sem a tara e a impureza. Quinhentos quilos de cobre mel, a quarenta e sete e noventa: vinte e três mil novecentos e cinquenta reais. |
| (a ilustração termina na folha da nota com "500 kg") | Uma dica: quando o cliente disser que o peso da nota não bate com o ticket, quase sempre ele está comparando o bruto com o líquido. |
| Aba "Transporte": em "Modalidade do Frete" escolhe "0 - Frete por conta do Remetente (CIF)"; em "Transportadora" escolhe "Cargas Vale do Sol Ltda (FJR3B27)"; os "Dados da Transportadora" se preenchem. | A carga vai com a transportadora. Na aba Transporte, escolho a modalidade do frete e a Cargas Vale do Sol, que já vem com a placa. |
| Clique em "Emitir Nota": "Aguardando SEFAZ" e, em ~5 s, toast "Nota #1250 autorizada pela SEFAZ!" e "Autorizada". [BACKEND: como no cap 09, nº 1250, com `invoice_orders` ligando o pedido] | Emitir Nota. Pronto: a mil duzentos e cinquenta está autorizada. |

### cap11 · Nota de um caixa fechado (vinheta: EMISSÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`), sub-aba "Entrada"; "Nova Nota" → "NF-e de Entrada" ("Registrar nota fiscal de compra do fornecedor"). | E as compras do dia, de quem não emite nota? A Dona Cida e o Valdir vendem sucata como pessoa física, e a nota de entrada dessas compras sai pela Recicla Vale. |
| Na barra "Importar de", clique em "Emissão em Massa (Caixa)": "Emitir NF-e em massa" ("Selecione as compras e confira exatamente como o lote será numerado e emitido."), aba "Por Caixa". | Em vez de uma nota por compra, dá pra juntar o dia todo. Na barra Importar de, clico em Emissão em Massa, Caixa. |
| No botão da data escolhe 9 de novembro: "Caixas de origem" mostra "Marcos Antunes" com o selo "Fechado" e "09/11 07:02"; marca o caixa; a lista traz as três compras. [BACKEND: o caixa fechado do "Mundo", com as três compras sem nota] | Escolho ontem, nove de novembro. Aparece o caixa do Marcos, já fechado, com as compras do dia. |
| Clique em "Selecionar todos sem NF-e": "3/3 selecionados". | Seleciono todas as que ainda não têm nota. |
| Em "Como as notas serão geradas", clique em "Uma nota consolidada" ("Junta os itens e abre a nota para você revisar antes de emitir."); à direita, "Faixa prevista para este lote" "NF-e nº 1251", "Valor dos pedidos" R$ 803,30 e "3 itens após consolidar.". [ZOOM: "Faixa prevista para este lote" e "Valor dos pedidos", a frase inteira] | Em Como as notas serão geradas, escolho Uma nota consolidada. A tela mostra a faixa: NF-e mil duzentos e cinquenta e um, de oitocentos e três reais e trinta. |
| [ILUSTRAÇÃO: Várias compras, uma nota: três tickets pequenos ("Dona Cida: latinha e papelão", "Valdir: ferro misto", "Dona Cida: latinha e papelão") deslizam e se juntam numa folha só, que mostra "latinha 64 kg", "papelão 180 kg" e "ferro misto 410 kg", cada linha na sua palavra] | Ela junta os itens iguais: sessenta e quatro quilos de latinha, cento e oitenta de papelão e quatrocentos e dez de ferro misto. Quem prefere uma nota por compra usa a outra opção, Uma nota por pedido. |
| Clique em "Montar nota consolidada": toast "3 pedido(s) importado(s) com sucesso!"; a nota volta com "Consumidor Final / Não Identificado" marcado; em "Natureza da Operação" escolhe "Entrada de sucata para revenda (pessoa física)". | Clico em Montar nota consolidada. A nota fica em nome da própria Recicla Vale, como consumidor final, e a natureza é entrada de sucata para revenda, de pessoa física. |
| "Avançar" → "Itens" (as três linhas); clique em "Emitir Nota": "Aguardando SEFAZ" e, em ~5 s, toast "Nota #1251 autorizada pela SEFAZ!". [BACKEND: como no cap 09, nº 1251; `invoice_orders` com os três pedidos] | Confiro os itens e clico em Emitir Nota. Pronto: a mil duzentos e cinquenta e um está autorizada, com as compras do dia inteiro. |

### cap12 · Cancelar e corrigir (vinheta: CORREÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap11`), sub-aba "Saída": "#1250" e "#1249", as duas "Autorizada". | Nota emitida, e se algo mudar? A Serra Fina ligou: desistiu do alumínio, e a carga nem saiu do pátio. Então a nota mil duzentos e quarenta e nove vai ser cancelada. |
| Menu da "#1249" → "Cancelar": "Cancelar Nota Fiscal #1249" ("Esta ação irá marcar a nota fiscal como cancelada. ..."); em "Motivo do Cancelamento" digita "Venda desfeita pelo cliente antes de a mercadoria sair do pátio". | No menu da nota, Cancelar. O motivo é obrigatório, com pelo menos quinze caracteres. |
| Clique em "Confirmar Cancelamento": toast "Nota fiscal cancelada"; o selo vira "Cancelada". [BACKEND: edge `plugnotas-cancel` devolve `confirmed` true] | Confirmar Cancelamento. Pronto, cancelada. Passadas vinte e quatro horas da autorização, a própria tela avisa que o prazo normal acabou. |
| [ILUSTRAÇÃO: Cancelar × corrigir: à esquerda, uma folha de nota recebe o carimbo "cancelada" e fica cinza; à direita, outra folha continua branca e recebe um bilhete grampeado com "onde se lê... leia-se..."; cada lado acende na sua frase] | Já a mil duzentos e cinquenta continua valendo. Só mudou um detalhe: a transportadora trocou o caminhão da carga. Pra isso existe a carta de correção, um aviso que fica junto da nota. |
| Menu da "#1250" → "Carta de Correção": "Carta de Correção - NF-e #1250"; zoom no aviso "Importante: A Carta de Correção (CC-e) permite corrigir erros em campos específicos da NF-e. Não é permitido corrigir: ...". | Ela corrige erros em campos específicos. E a própria tela diz o que não dá pra corrigir: valores, quantidade, quem vende e quem compra, a data e qualquer coisa que mude o imposto. |
| Em "Texto da Correção *" digita "Onde se lê 'Placa FJR3B27', leia-se 'Placa GKM5D18'. A transportadora trocou o veículo da carga."; zoom na "Dica: Use o formato "Onde se lê '...', leia-se '...'" para deixar a correção clara.". | No texto, uso o formato que a tela sugere: onde se lê a placa antiga, leia-se a placa nova. |
| Clique em "Enviar CC-e": toast "Carta de Correção enviada com sucesso!". [BACKEND: edge `plugnotas-cce` (envio; o status responde `CONCLUIDO`, sequência 1)] | Clico em Enviar CC-e. Pronto: a correção fica registrada junto da nota. |

### cap13 · Inutilizar numeração (vinheta: NUMERAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap12`), sub-aba "Saída". | E o número que nunca virou nota? No sistema antigo, as notas mil duzentos e quarenta e seis e mil duzentos e quarenta e sete foram recusadas e ficaram pra trás. Esses números estão em aberto na SEFAZ. |
| [ILUSTRAÇÃO: Números com cadeado: a fila 1246, 1247, 1248, 1249, 1250 e 1251; de 1248 a 1251, folhas com visto (a 1249 com o carimbo "cancelada"); 1246 e 1247, espaços vazios; na palavra "inutilizar", um cadeado fecha os dois] | Inutilizar é avisar a SEFAZ que esses números não vão virar nota. |
| Clique nos três pontinhos ao lado de "Nova Nota" → "Inutilizar numeração": "Inutilizar Numeração de NF-e"; zoom no aviso "Operação irreversível!" e nos itens "Só funciona em números que NUNCA foram autorizados pela SEFAZ" e "Para anular nota emitida, use Cancelamento". | Fica nos três pontinhos, em Inutilizar numeração. Repara no aviso: é pra sempre, e só vale pra número que nunca foi autorizado. Nota autorizada se resolve com o cancelamento. |
| Aba "Por Faixa": "Série *" 1, "Ano *" 2026, "Número Inicial *" 1246, "Número Final" 1247; embaixo, "Inutilizará as Notas #1246 até #1247 da Série 1, ano 2026". [ZOOM: esse resumo, a frase inteira] | Em Por Faixa vai a série um, do mil duzentos e quarenta e seis ao mil duzentos e quarenta e sete. Dá pra fechar um número só ou uma faixa inteira de uma vez. |
| Zoom na aba "Inutilizar Rejeitadas" (sem clicar). | E na aba Inutilizar Rejeitadas, as notas recusadas aqui no sistema se fecham em lote. |
| Em "Justificativa * (mínimo 15 caracteres)" digita "Numeração recusada no sistema anterior e não utilizada"; clique em "Inutilizar na SEFAZ": toast "Numeração inutilizada com sucesso". [BACKEND: edge `plugnotas-inutilize` grava `nfe_inutilized_numbers`] | Escrevo a justificativa e clico em Inutilizar na SEFAZ. |
| Sub-aba "Inutilizadas": "Numerações Inutilizadas" ("Números fechados na SEFAZ que não viraram nota. ..."), botão "Saída" ativo, as linhas "#1246" e "#1247" com o selo "Inutilizada". [BACKEND: `get_invoices_paged` com `p_include_inutilizadas` devolve as duas] | Pronto. Os números fechados ficam aqui, em Inutilizadas. |

### cap14 · DANFE e XML (vinheta: DOCUMENTOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap13`), sub-aba "Saída". | Agora, os arquivos da nota. Toda nota autorizada tem dois: o DANFE e o XML. |
| [ILUSTRAÇÃO: DANFE e XML: à esquerda, uma folha impressa "DANFE" vai para a cabine do caminhão, junto da carga; à direita, um arquivo "XML" vai para uma pasta rotulada "contador"; cada um na sua frase] | O DANFE é a folha impressa que acompanha a carga no caminhão. O XML é o arquivo oficial da nota, que o contador guarda. |
| Menu da "#1250" (três pontinhos); zoom em "Download XML", "Download DANFE", "Comprovante (Notinha)" e "Carta de Correção". | Os dois ficam no menu da nota. |
| Clique em "Download DANFE": abre a aba nova com o PDF "DANFE 1250 - Recicla Vale Metais" (Fundição Bandeira do Vale, Cobre mel 500 kg). [BACKEND: `plugnotas-download` (ou o bucket `nfe-danfes`) devolve o PDF fictício com os dados da nota] | Download DANFE abre o PDF, pronto pra imprimir. |
| Volta à aba do sistema; menu da "#1250" → "Download XML": baixa "NFe 1250 - Recicla Vale Metais.xml" (a câmera fica na tela do sistema). [BACKEND: `plugnotas-download` com `type` xml] | E Download XML baixa o arquivo, com o número da nota no nome. |
| Menu da "#1250" → "Visualizar" → aba "XML": "XML da nota" ("Mesmo arquivo enviado à SEFAZ. Pode selecionar e copiar trechos direto daqui.") e "Copiar XML"; fecha. [BACKEND: o conteúdo do XML da 1250 para a aba] | E em Visualizar, a aba XML mostra o mesmo arquivo enviado à SEFAZ, pra conferir ou copiar um trecho. |
| Menu da "#1249" (selo "Cancelada"): zoom em "XML de Cancelamento". | O menu muda com a situação da nota. Na cancelada, aparece o XML de Cancelamento. |
| Clique nos três pontinhos ao lado de "Nova Nota": zoom em "Exportação Contábil" (sem clicar); fecha o menu. | E pra mandar as notas do mês pro contador, tem a Exportação Contábil, que é assunto do próximo tutorial. |

### cap15 · As notas recebidas (vinheta: NOTAS RECEBIDAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap14`); sub-aba "Notas Recebidas": "Notas Recebidas (Distribuição DF-e)", aba "NF-e", e o bloco "Ative as Notas Recebidas". | Até aqui, as notas que a Recicla Vale emite. Agora, as que ela recebe. |
| [ILUSTRAÇÃO: A nota chega pela SEFAZ: um prédio genérico "Auto Peças" emite uma folha com "destinatário: Recicla Vale"; a folha passa pelo prédio "SEFAZ" e desce para uma caixa "Notas Recebidas"; na frase "aparece sozinha", ela pousa na caixa] | Quando um fornecedor emite uma nota com o CNPJ da Recicla Vale como destinatário, a nota passa pela SEFAZ. Com o recurso ativo, ela aparece sozinha aqui. |
| Clique em "Ativar Notas Recebidas": diálogo "Ativar consulta de notas recebidas?". [ZOOM: o texto "Ao ativar, cada nota fiscal recebida dos seus fornecedores passa a contar na sua cota mensal de documentos fiscais...", a frase inteira] | Clico em Ativar Notas Recebidas. A tela avisa: a partir da ativação, cada nota recebida conta na mesma cota das notas que você emite. |
| Clique em "Ativar mesmo assim": toast "Notas Recebidas ativado"; a tela vira "Notas emitidas contra o seu CNPJ", com "Recurso ativo", "Importar nota" e "Sincronizar agora"; chegam "Auto Peças Vale Forte" (R$ 1.984,00, 09/11/2026) e "Depósito Irmãos Siqueira" (R$ 2.185,00, 06/11/2026), as duas "Autorizada" e "Ciência". [BACKEND: edges `plugnotas-enable-dfe` e `plugnotas-dfe-sync` (o sync inicial é silencioso); as duas notas do "Mundo"] | Ativar mesmo assim. Em instantes chegam as notas emitidas contra o CNPJ da Recicla Vale: a da Auto Peças Vale Forte, de mil novecentos e oitenta e quatro reais, e a do Depósito Irmãos Siqueira. |
| Zoom nas colunas "Emitente", "Valor", "Emissão", "SEFAZ" e "Manifestação". | Cada linha mostra quem emitiu, o valor, a data, a situação na SEFAZ e a manifestação. |
| Zoom em "Sincronizar agora" (sem clicar). | Depois disso, as notas entram sozinhas. E o Sincronizar agora faz a busca na hora. |

### cap16 · Manifestar a nota (vinheta: NOTAS RECEBIDAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap15`): "Notas emitidas contra o seu CNPJ" com as duas notas. [ZOOM: a coluna "Manifestação" com "Ciência" nas duas, a frase inteira] | Chegou a nota, e agora? Repara na coluna Manifestação: as duas já estão com Ciência. |
| [ILUSTRAÇÃO: As respostas: a nota da Auto Peças no centro, já com o selo "Ciência" (chega sozinho, na palavra "sozinha"); três caminhos saem dela, ainda apagados: "Confirmar operação", "Desconhecer operação", "Operação não realizada" (a escolha é feita na tela real, nas falas seguintes)] | Manifestar é responder à SEFAZ sobre a nota que chegou. A ciência não é um botão: ela já vem sozinha, quando a nota entra. |
| Menu da nota do "Depósito Irmãos Siqueira": "Ver XML" apagado ("XML ainda não disponível") e "Buscar documento" (dica "Baixa o XML e o DANFE (não confirma nem recusa nada)"); clique em "Buscar documento": a linha atualiza e o DANFE recebido abre em aba nova; volta à aba do sistema. [BACKEND: a nota do Depósito chega só com o resumo; edge `plugnotas-dfe-fetch-doc` devolve `xmlSaved` e `pdfSaved` sem fila] | A do Depósito chegou só com o resumo. Pra baixar o XML e o DANFE de uma nota recebida, é Buscar documento, que não confirma nem recusa nada. |
| Menu da nota da "Auto Peças Vale Forte", grupo "Manifestar": zoom em "Confirmar operação" (dica "Confirma que a compra/entrada é sua"), "Desconhecer operação" e "Operação não realizada". | As respostas ficam no grupo Manifestar. Confirmar operação diz que a compra é sua. Desconhecer operação, que você não reconhece a nota. E Operação não realizada, que a compra não aconteceu. |
| (o zoom continua nas duas últimas) | As duas últimas pedem uma justificativa e não podem ser desfeitas. |
| Clique em "Confirmar operação": toast "Operação confirmada junto à SEFAZ"; o selo vira "Confirmada". [BACKEND: edge `plugnotas-manifestar` sem fila] | A bateria da Auto Peças chegou certinho, então confirmo a operação. Pronto: confirmada. |

### cap17 · Importar pelo XML (vinheta: NOTAS RECEBIDAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap16`): "Notas emitidas contra o seu CNPJ". | E a nota que ainda não apareceu na lista? A Cooperativa Recomeço vendeu latinha e PET ontem e mandou o XML por e-mail. Dá pra trazer a nota pelo arquivo. |
| Clique em "Importar nota": "Importar nota recebida" ("Traga uma NF-e para esta lista pela chave de acesso ou pelo XML autorizado."); aba "Arquivo XML"; em "Selecione o XML autorizado da NF-e" o robô entrega `NFe-3871-Cooperativa-Recomeco.xml`. | Clico em Importar nota, vou na aba Arquivo XML e escolho o arquivo da cooperativa. |
| Clique em "Importar nota": "Processando a nota" e, em ~3 s, "Nota importada" ("A NF-e já foi adicionada à lista. ..."); clique em "Concluir": a linha "Cooperativa Recomeço" (R$ 7.550,00) entra na lista. [BACKEND: RPC `dfe_inbound_import_enqueue` e o job "succeeded"; a nota entra com `xml_content`] | Importar nota. Pronto: nota importada, e ela entra na lista com as outras. |
| Menu da "Cooperativa Recomeço" → "Lançar compra…": o título "Importar NF-e nº 3871" com o nome da cooperativa; "Fornecedor: Cooperativa Recomeço" com "por CNPJ/CPF". | Agora, Lançar compra. O sistema lê o XML e acha o fornecedor pelo CNPJ. |
| Zoom no primeiro cartão: "ALUMINIO LATINHA", selo verde "alta", "Material" = "Alumínio latinha". [ILUSTRAÇÃO: O casamento: à esquerda, os nomes do XML ("ALUMINIO LATINHA", "PLASTICO PET PRENSADO"); à direita, os materiais do cadastro ("Alumínio latinha", "Plástico PET"); uma linha liga cada par: cheia no primeiro (nome igual, selo "alta"), pontilhada no segundo (palavras em comum, selo "confira"), cada uma na sua frase] | E casa cada item com um material do cadastro. A latinha do XML tem o mesmo nome do material, então a confiança é alta. |
| Zoom no segundo cartão: "PLASTICO PET PRENSADO", selo amarelo "confira", "Material" = "Plástico PET", "Qtd" 1.200 KG e "Valor un." 1,90. | O PET prensado tem palavras em comum com o Plástico PET, e o selo pede pra conferir. Quando a confiança é baixa, o material fica pra você escolher. |
| Zoom na frase "A NF-e traz só o peso líquido..." e no botão "Conferir na tela de compra" (sem clicar). | A nota traz só o peso líquido. E Conferir na tela de compra leva os itens pra tela de Compra. Nada é lançado agora: lá você confere os valores e escolhe como pagou. |

### cap18 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: "Certificado validado!" e o quadro "Lucro Real:" (trechos dos capítulos 03 e 04). | Pronto! Recapitulando: a gente subiu o certificado A1, preencheu a empresa e os impostos no Lucro Real e criou um cenário, sempre com o que o contador passou. |
| Montagem rápida: "Série 1" com "Última nota emitida: 1248", a linha da Cargas Vale do Sol e o selo "0/100 Documentos". | Continuou a numeração do sistema antigo, cadastrou a transportadora e viu a cota do mês, com a tolerância de cinco documentos. |
| Montagem rápida: as linhas "#1249", "#1250" e "#1251" com "Autorizada" (trechos dos capítulos 09 a 11). | Emitiu a nota pelos três caminhos: do zero, a partir de um pedido e a partir de um caixa fechado. |
| Montagem rápida: "Cancelada", "Carta de Correção - NF-e #1250", "Numerações Inutilizadas" e o PDF do DANFE. | Cancelou uma nota, mandou uma carta de correção, inutilizou os números que tinham ficado em aberto e baixou o DANFE e o XML. |
| Montagem rápida: "Notas emitidas contra o seu CNPJ" com "Confirmada" e o casamento "alta" e "confira". | E ativou as notas recebidas, confirmou uma operação e importou uma nota pelo XML. |
| Cartão "Próximo: Transporte, serviço e o contador"; cartela final. | No próximo tutorial, o documento que acompanha a carga na estrada e o pacote que o contador pede. Até lá! |
