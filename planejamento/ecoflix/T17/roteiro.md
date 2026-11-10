# Roteiro T17 · Transporte, serviço e o contador

- **Título:** Transporte, serviço e o contador
- **Antes:** Nota Fiscal de mercadoria (NF-e) (T16)
- **Próximo:** Ambiental: MTR e CDF (T18)
- **Vinhetas (áreas):** TRANSPORTE · FROTA · MANIFESTO · SERVIÇO · RELATÓRIO FISCAL · ESTOQUE FISCAL · CONTADOR · RESUMO (todo
  capítulo menos o 0)
- **Duração estimada:** ~13 min de vídeo (1.841 palavras de fala, ~11,8 min a 2,6 palavras/s, mais a vinheta de abertura, 13
  vinhetas de capítulo, as esperas da SEFAZ simulada e a cartela; alvo da fonte ~16 min)
- Coluna Fala = texto da narração na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela =
  o que o robô faz e onde a câmera foca, rótulos entre aspas como no código 1.59.154 (`T17/inventario.md`). Logado como Rafael
  Nogueira (MASTER), desktop. Mundo e sementes: `T17/plano.md`. FAKE_NOW 10/11/2026 08:30 nos capítulos 0 a 4 e 14:20 do 5 em diante.
- Marcas: `[BACKEND: ...]` o que o backend falso ainda não tem; `[ZOOM: ...]` zoom suave que dura a frase inteira (sem zoom em cima de
  zoom); `[ILUSTRAÇÃO: ...]` desenho por código no estilo da marca, nunca tela inventada.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Transporte, serviço e o contador". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira. [ILUSTRAÇÃO: o dia da Recicla Vale: entra "Recicla Vale Metais · terça, 10 de novembro" e três cartões, um por trecho da frase: um caminhão com fardos de alumínio e a seta "Taubaté → Itamonte (MG)"; uma caçamba no pátio da "Aços Quiririm"; uma pasta "Outubro" indo para o "Contador".] | Oi! Neste tutorial a gente vai cuidar dos outros documentos da Recicla Vale Metais: o que acompanha a carga na estrada, o que cobra um serviço e o pacote que o contador pede todo mês. |
| (ilustração: os três cartões acendem um a um, na ordem da frase) | Hoje sai um caminhão de alumínio pra Minas Gerais, a coleta com caçamba na Aços Quiririm vira cobrança, e outubro fecha com o contador. |
| A ilustração sai; a câmera vai ao menu lateral e clica em "Fiscal & Ambiental"; o submenu abre e o destaque passa por "Transporte (MDF-e)", "Notas de Serviço (NFS-e)" e "Estoque Fiscal" (sem parar em "SPED Fiscal"). | Tudo isso fica no menu Fiscal & Ambiental: em Transporte, em Notas de Serviço e no Estoque Fiscal. |
| Cartão discreto: "Módulo Notas Fiscais". | Essas telas fazem parte do módulo de Notas Fiscais, então dependem do plano contratado. |
| Cartão discreto: "Antes: Nota Fiscal de mercadoria (NF-e)". | Se você ainda não viu o tutorial da nota fiscal de mercadoria, dá uma olhada antes. [pause] Vamos começar pelo manifesto. |

### cap01 · O que é o MDF-e (vinheta: TRANSPORTE)

| Tela | Fala |
| --- | --- |
| Clica em "Transporte (MDF-e)" no submenu: tela "Transporte (MDF-e)", sub-aba "Manifestos", título "Manifesto Eletrônico de Documentos Fiscais (MDF-e)"; a câmera desce até a lista vazia, "Nenhum MDF-e encontrado". [BACKEND: semente `inicio`, sem `mdfe_manifests`] | O manifesto fica aqui, em Transporte, na aba Manifestos. A Recicla Vale ainda não emitiu nenhum. |
| [ILUSTRAÇÃO: o manifesto: um caminhão genérico; entram nele duas folhas "NF-e" ("alumínio perfil", "alumínio bloco"); por cima desce uma capa "MDF-e" que abraça as duas notas, o caminhão (placa FKD2E41) e o motorista; a capa entra com a palavra "manifesto".] | Imagina o caminhão saindo com alumínio de duas vendas. Cada venda tem a sua nota fiscal. O manifesto, o MDF-e, é o documento da viagem: ele junta as notas da carga, o caminhão e o motorista. |
| (ilustração: o caminhão anda numa estrada; na saída, o selo "Autorizado"; na chegada, "Encerrado") | Ele é emitido antes de o caminhão sair e encerrado quando a viagem termina. |
| A ilustração sai; zoom suave nos cartões "MDF-e Autorizados", "MDF-e Pendentes", "MDF-e Rejeitados" e "MDF-e Encerrados", todos em 0. | Aqui em cima, os cartões contam os manifestos autorizados, pendentes, rejeitados e encerrados. |
| A câmera volta à tela inteira; cartão "Dica: confirme com o contador quando o MDF-e é obrigatório". | Uma dica: quem precisa emitir o manifesto depende da operação e do estado. Confirme com a sua contabilidade, principalmente quando a carga atravessa estado. O sistema entrega a ferramenta, e quem interpreta a regra é o contador. |

### cap02 · Veículo e motorista (vinheta: FROTA)

| Tela | Fala |
| --- | --- |
| Clica na sub-aba "Frota": "Frota (veículos e motoristas do MDF-e)", aba "Veículos"; a lista "Veículos da frota" com FKD2E41 (Caminhão truck), GHT7B19 (Caminhão 3/4) e EZR4C63 (Picape), selo "Sem tipo"; o painel do FKD2E41 aberto. [BACKEND: frota da base, só placa e descrição] | Antes do primeiro manifesto, o caminhão e o motorista precisam estar na Frota. Os caminhões da Recicla Vale já estão aqui: é a mesma frota da pesagem. |
| Clica em "Editar" no painel do FKD2E41: "Editar veículo"; a câmera desce até "Dados de transporte (MDF-e / NF-e)". | Pro manifesto, faltam os dados de transporte do caminhão truck. Clico em Editar. |
| "UF de licenciamento" → "SP"; "Tipo" → "Veículo único (truck, toco, utilitário)"; "Tipo de rodado" → "Truck"; "Tipo de carroceria" → "Aberta". | Ele é emplacado em São Paulo. No Tipo, é um veículo único, sem carreta. O rodado é truck, e a carroceria é aberta. |
| Digita "7800" em "Tara (kg)" e "14000" em "Capacidade (kg)". [ZOOM: "Tara (kg)" e "Capacidade (kg)"] | A tara é o peso do caminhão vazio: sete mil e oitocentos quilos. E ele leva até catorze mil quilos de carga. |
| Digita "30" em "Capacidade (m³)"; a câmera mostra a ajuda "máx. 999 m³" embaixo do campo. | Uma dica: peso aqui é sempre em quilos. Se o número parecer tonelada, a própria tela avisa. |
| Clica em "Salvar": toast "Veículo atualizado"; o painel mostra "Dados de transporte" preenchido e o selo "Veículo único". | Salvar, e o caminhão está pronto pro manifesto. |
| Aba "Motoristas": "Edson Moura" na lista; clica em "Editar": "Editar motorista". | Agora o motorista. O Edson Moura já está na lista. Clico em Editar. |
| Digita "318.472.650-90" em "CPF", "04728193604" em "CNH", escolhe "C" em "Categoria" e 18/03/2029 em "Validade da CNH". [ZOOM: "CPF"] | O manifesto leva o CPF do motorista, então eu completo o CPF, a CNH e a categoria. |
| Clica em "Salvar": toast "Motorista atualizado"; o painel mostra "Dados pessoais" e "Carteira de habilitação". | Salvar. Caminhão e motorista prontos. |

### cap03 · Numeração e percurso (vinheta: TRANSPORTE)

| Tela | Fala |
| --- | --- |
| Clica na sub-aba "Manifestos" e em "Configurações do MDF-e": diálogo "Configurações do MDF-e", "Série" 1, "Próximo Número" 1 e o quadro "Série" / "Próximo MDF-e". [ZOOM: quadro "Série" / "Próximo MDF-e"] | Com a frota pronta, uma olhada nas Configurações do MDF-e. Aqui ficam a série e o próximo número do manifesto. |
| A câmera sobe até "Série e próximo número do manifesto. Útil quando a empresa já emitiu MDF-e em outro sistema." (sem clicar em "Sincronizar Numeração"). | A Recicla Vale nunca emitiu manifesto, então começa no número um. Se a sua empresa já emitia em outro sistema, é aqui que você continua a sequência. |
| A câmera desce até "Motoristas e veículos agora ficam em Transporte (MDF-e) → Frota" e o botão "Ir para Frota"; fecha o diálogo no "X". | E o caminhão e o motorista ficam na Frota, que a gente acabou de ver. |
| [ILUSTRAÇÃO: o percurso: mapa simplificado de SP, RJ e MG, sem marca de mapa; os pontos "Taubaté (SP)" e "Itamonte (MG)"; o caminhão parado em Taubaté com o rótulo "Carregamento".] | Agora, o percurso. Hoje o caminhão leva alumínio pra Serra Fina, em Itamonte, Minas Gerais. |
| (ilustração: uma linha sai de Taubaté, entra no RJ e sobe até Itamonte, onde aparece "Descarregamento"; o RJ acende em verde com "estado do meio do caminho") | Ele sai de Taubaté, passa pelo Rio de Janeiro e sobe pra Minas. São Paulo é a origem, Minas Gerais é o destino, e o Rio de Janeiro é o estado do meio do caminho. |
| (ilustração: o RJ vai para um cartão "Percurso (UFs Atravessadas)" com "1ª UF: RJ") | O estado do meio do caminho vai no Percurso. E isso a gente preenche em cada manifesto, na hora de emitir. |

### cap04 · Emitir o manifesto (vinheta: MANIFESTO)

| Tela | Fala |
| --- | --- |
| Clica em "Novo MDF-e": "Novo MDF-e (Manifesto Eletrônico)", etapa "Notas fiscais", lista "NF-ES VINCULADAS"; o "Resumo do MDF-e" à direita. [BACKEND: semente `apos-cap02` com as duas NF-e da Serra Fina de hoje] | Hora de emitir. Clico em Novo MDF-e, e o primeiro passo são as notas da carga. |
| Digita "Serra Fina" em "Buscar NF-e..." e marca as duas primeiras (as de hoje); embaixo, "2 NF-e(s) selecionada(s) • Valor total: R$ 55.380,00". [ZOOM: "Valor total: R$ 55.380,00"] | Busco a Serra Fina e marco as duas notas de hoje: o alumínio perfil e o alumínio bloco. Juntas, dão cinquenta e cinco mil, trezentos e oitenta reais. |
| Clica em "Continuar": etapa "Veículo e motorista"; em "Veículo (tração)", escolhe "Caminhão truck • FKD2E41 • SP" (selo "Veículo único"); em "Motorista", "Edson Moura (318.472.650-90)". | Continuar. No veículo, o caminhão truck, e no motorista, o Edson. Como a Frota está completa, não falta nenhum dado. |
| Clica em "Continuar": etapa "Trajeto e carga"; o cartão "Carregamento (Origem)" já está com "SP" e "Taubaté". [BACKEND: cidades da API do IBGE respondidas localmente para SP e MG] | Continuar. A origem já vem com a cidade da empresa: Taubaté. |
| Clica em "Adicionar UF ao percurso"; na linha "1ª UF", escolhe "RJ". | No Percurso, eu adiciono o Rio de Janeiro, o estado do meio do caminho. |
| No cartão "Descarregamento (Destino)", troca a UF para "MG" e escolhe a cidade "Itamonte"; o "Resumo do MDF-e" mostra "Itamonte/MG" em "Destino". | E no destino, Minas Gerais, cidade de Itamonte. |
| A câmera desce até "Peso Bruto Total (kg)" 5800, com "Somado das notas selecionadas", e "Valor Total da Carga" R$ 55.380,00. [ZOOM: "Peso Bruto Total (kg)" e "Valor Total da Carga"] | O peso já vem somado das notas: cinco mil e oitocentos quilos. E o valor da carga também. |
| Clica em "Continuar": "Revise antes de emitir"; em "Como emitir", "Normal" já escolhido ("Envia para a SEFAZ agora"). [BACKEND: `mdfe_contingency_availability` devolve disponível] | Na revisão, o jeito de emitir fica no Normal, que envia pra SEFAZ na hora. |
| Zoom no botão "Contingência" ("Use quando a SEFAZ estiver indisponível"), sem clicar. [ZOOM: botão "Contingência"] | Uma dica: a contingência é só pra quando a SEFAZ estiver fora do ar. Nesse caso, o motorista só sai com o PDF do manifesto impresso em papel. |
| A câmera mostra o quadro verde "Tudo pronto para criar e emitir o MDF-e" e o resumo; clica em "Criar MDF-e": toasts "MDF-e #1 criado" e "MDF-e #1 enviado para SEFAZ!"; a lista mostra o nº 1 com "Aguardando SEFAZ". [BACKEND: `plugnotas-mdfe-emit` → aguardando_sefaz] | Tudo pronto. Criar MDF-e. O manifesto número um foi criado e já foi enviado pra SEFAZ. |
| Espera a consulta automática (5 s): toast "MDF-e #1 autorizado!"; o selo vira "Autorizado"; a câmera fica na linha (Nº 1, Edson Moura, FKD2E41, o trajeto, R$ 55.380,00, 5.800). [ZOOM: linha do nº 1 com "Autorizado"] [BACKEND: `plugnotas-mdfe-status` → autorizado na 1ª consulta] | Pronto, autorizado. Na linha aparecem o motorista, a placa, o trajeto, o valor e o peso. |
| Passa o mouse em "Ações" da linha: o menu mostra "Encerrar", "Cancelar", "Baixar DAMDFE (PDF)" e "Baixar XML" (sem clicar). | E pelo menu de ações você baixa o PDF do manifesto, que vai com o motorista na viagem. |

### cap05 · Encerrar no fim da viagem (vinheta: MANIFESTO)

| Tela | Fala |
| --- | --- |
| Corte para a tarde: Transporte › "Manifestos", o nº 1 "Autorizado"; o cartão "MDF-e Autorizados" em 1. [BACKEND: semente `apos-cap04`, FAKE_NOW 14:20] | À tarde, a carga foi entregue em Itamonte. Agora falta encerrar o manifesto. |
| [ILUSTRAÇÃO: encerrar × cancelar: em cima, a linha do tempo "Autorizado" (o caminhão sai de Taubaté) → estrada → "Encerrado" (carga entregue em Itamonte), com um visto; embaixo, um ramo à parte, "Cancelar": um manifesto riscado, que não deveria existir, com um relógio e "prazo curto".] | Uma dica: encerrar não é cancelar. Encerrar é o fim normal da viagem. Cancelar é anular um manifesto que não deveria existir, e tem prazo curto. |
| A ilustração sai; passa o mouse em "Ações" da linha e clica em "Encerrar": toast "Encerramento enviado. A confirmação da SEFAZ aparece em instantes."; o selo vira "Encerramento enviado". [BACKEND: `plugnotas-mdfe-enclose` → encerramento_pendente] | No menu de ações, Encerrar. O pedido vai pra SEFAZ, e o selo mostra que o encerramento foi enviado. |
| Espera a consulta (5 s): toast "MDF-e #1: encerramento confirmado pela SEFAZ"; selo "Encerrado"; o cartão "MDF-e Encerrados" vai a 1. [ZOOM: selo "Encerrado" e cartão "MDF-e Encerrados"] [BACKEND: `plugnotas-mdfe-status` → encerrado] | Pronto, encerrado. A viagem está fechada, e o manifesto passa a contar nos encerrados. |

### cap06 · A nota de serviço (vinheta: SERVIÇO)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Notas de Serviço (NFS-e)": título "Nota Fiscal de Serviço (NFS-e)", lista com o nº 13 (Aços Quiririm Ltda, R$ 1.850,00) e o nº 12 (Fundição Bandeira do Vale, R$ 1.200,00), os dois "Autorizada"; a câmera não para nos cartões de cima. [BACKEND: NFS-e 12 e 13 na semente] | Agora, a nota de serviço. Ela fica em Notas de Serviço. |
| [ILUSTRAÇÃO: mercadoria × serviço, lado esquerdo "Mercadoria": fardos de sucata saindo do pátio no caminhão, com a folha "NF-e" e o rótulo "SEFAZ".] | Pensa assim: quando a Recicla Vale vende sucata, a mercadoria sai do pátio. A nota dessa venda é a nota fiscal de mercadoria, a NF-e. |
| (ilustração, lado direito "Serviço": uma caçamba recolhida no pátio da "Aços Quiririm", com a folha "NFS-e", o rótulo "Prefeitura" e um pátio sem nenhuma mercadoria saindo) | Quando ela cobra um trabalho, como a coleta com caçamba, não sai mercadoria nenhuma. Essa é a nota de serviço, a NFS-e, que é da prefeitura. |
| A ilustração sai; zoom nas colunas "Número", "Tomador", "Valor" e "Status" da lista. | Na lista ficam as notas de serviço emitidas: o número, quem contratou, que aqui se chama tomador, o valor e o status. |
| Zoom no botão "Configurações Fiscais" do cabeçalho, sem clicar. | E os dados da empresa que a nota de serviço usa, como a inscrição municipal, ficam nas Configurações Fiscais. Quem confere esses dados é o contador. |

### cap07 · Emitir e acompanhar (vinheta: SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clica em "Nova NFS-e": "Nova NFS-e", aba "Pessoas", "Data de competência" com 10/11/2026 e o selo vermelho de pendências na barra de cima. | Vou cobrar a coleta com caçamba que a Recicla Vale fez na Aços Quiririm. Nova NFS-e. |
| Troca a "Data de competência" para 07/11/2026. Em "Tomador do serviço", clica em "Cliente ou fornecedor": "Selecionar tomador"; digita "Aços" em "Buscar por nome, CNPJ/CPF ou código..." e escolhe "Aços Quiririm Ltda". | Na data de competência vai o dia do serviço: sete de novembro. No tomador, quem contratou, eu escolho a Aços Quiririm no cadastro. |
| Clica em "Avançar": aba "Serviço"; "Município" já com "Taubaté"; clica em "Selecionar código de tributação", digita "coleta" em "Buscar por código ou descrição..." e escolhe o código de coleta e remoção de resíduos; "Código do serviço (LC116)" se preenche sozinho. [BACKEND: `plugnotas-nfse-servicos-municipio` com a lista de Taubaté] | Avançar. O município já vem como Taubaté. O código do serviço é o seu contador que passa. Aqui, coleta e remoção de resíduos. |
| Zoom em "Puxar serviço salvo", sem clicar. | Se a empresa emite sempre o mesmo serviço, ele pode ficar salvo, e aí é só puxar por aqui. |
| Digita em "Descrição do serviço": "Coleta e remoção de resíduos metálicos com caçamba no pátio da Aços Quiririm em 07/11/2026." | Na descrição, o que foi feito, do jeito que vai aparecer na nota. |
| Clica em "Avançar": aba "Valores"; digita "1850" em "Valor do serviço"; a barra de cima mostra "Total da nota" R$ 1.850,00. [ZOOM: "Valor do serviço"] | Avançar. O valor do serviço: mil oitocentos e cinquenta reais. |
| A câmera vai a "Alíquota ISS %", com 3 vindo da lista do município, e "ISS retido na fonte" desligado. [ZOOM: "Alíquota ISS %"] | A alíquota do ISS veio da lista do município. Quem confirma esse número é o contador. |
| Clica em "Avançar": aba "Pré-visualização", o espelho da nota com a Aços Quiririm, o serviço e R$ 1.850,00; selo "Pronta pra emitir". | Na pré-visualização, a nota aparece como vai sair. E o selo mostra que ela está pronta pra emitir. |
| Clica em "Emitir NFS-e": toast "Nota de serviço enviada para emissão"; a lista mostra a nova linha "Processando". [BACKEND: `plugnotas-emit-nfse` → processando] | Emitir NFS-e. Ela entra na lista como processando. |
| Espera a consulta automática (8 s): selo "Autorizada" e "14" na coluna "Número". [ZOOM: "14" na coluna "Número" com "Autorizada"] [BACKEND: `plugnotas-nfse-status` → emitida, nº 14] | E em instantes fica autorizada: nota de serviço número catorze. |
| Abre o menu "Ações" da linha e para em "Baixar PDF" e "Histórico" (sem clicar); fecha o menu. | Pelo menu, você baixa o PDF pra mandar pra Aços Quiririm e acompanha tudo no Histórico. |

### cap08 · O serviço que você tomou (vinheta: SERVIÇO)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Notas Fiscais (NF-e)"; sub-aba "Notas Recebidas"; aba "NFS-e": "Ative as Notas de Serviço Recebidas". [BACKEND: `nfse_dfe_ativo` desligado] | E quando é a Recicla Vale que contrata um serviço? A nota chega em Notas Fiscais, nas Notas Recebidas, na aba NFS-e. |
| Zoom no texto "...as notas de serviço (NFS-e) que prestadores emitem contra o CNPJ da sua empresa... passam a entrar aqui automaticamente, prontas pra virar despesa." | São as notas que outras empresas emitem contra o seu CNPJ: o contador, a manutenção, um frete. Elas entram aqui sozinhas, prontas pra virar despesa. |
| Clica em "Ativar NFS-e Recebidas": diálogo "Ativar o recebimento de notas de serviço?". [ZOOM: "Ao ativar, cada nota de serviço recebida passa a contar na sua cota mensal de documentos fiscais..."] | Clico em Ativar NFS-e Recebidas. Repara no aviso: cada nota recebida conta na cota mensal de documentos fiscais, a mesma das notas que você emite. |
| Clica em "Ativar mesmo assim": toasts "Notas de serviço recebidas ativado" e "2 nota(s) de serviço sincronizada(s)"; a tela vira "Notas de serviço emitidas contra o seu CNPJ", com "Recurso ativo". [BACKEND: `plugnotas-enable-nfse-dfe` e `plugnotas-nfse-dfe-sync` → 2 notas] | Ativar mesmo assim. Pronto, ele já buscou as notas, e chegaram duas. |
| Zoom nas duas linhas: "Contabilidade Jequitibá Ltda" R$ 1.650,00 e "Balanças Tremembé Manutenção Ltda" R$ 980,00. [ZOOM: colunas "Prestador" e "Valor"] | Os honorários do escritório de contabilidade, de mil seiscentos e cinquenta reais, e a aferição da balança rodoviária, de novecentos e oitenta. |
| Zoom no aviso fixo "A NFS-e é da prefeitura, e só chega aqui a nota de cidade que entrou no sistema nacional...". | Uma dica: só chega aqui a nota de cidade que já entrou no sistema nacional. Se uma nota não aparecer, peça o PDF ao prestador e lance a despesa na mão. |
| Abre "Ações" na linha da Balanças Tremembé; no grupo "Financeiro", clica em "Lançar despesa / conta": "Nova conta" com "A pagar (despesa)", "Valor" R$ 980,00 e "Descrição" "Balanças Tremembé Manutenção Ltda" já preenchidos. | Serviço não entra no estoque, então aqui o caminho é a despesa. Na linha da balança, Lançar despesa ou conta. |
| Escolhe 20/11/2026 em "Vencimento" e "Manutenção" em "Categoria"; clica em "Criar conta": toast "Conta criada"; a linha ganha o selo "Lançada". [BACKEND: categoria de despesa de manutenção na base] | A conta já vem com o valor e os dados da nota. Falta o vencimento, dia vinte, e a categoria. Criar conta. E a nota fica marcada como lançada. |

### cap09 · Entrada, saída e saldo (vinheta: RELATÓRIO FISCAL)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Estoque Fiscal": sub-aba "Relatório fiscal"; no filtro de período do cabeçalho, escolhe "Mês passado". [BACKEND: notas de outubro na semente; `get_invoice_dashboard`] | Antes de mandar o mês pro contador, vale conferir os números. No Estoque Fiscal, a primeira aba é o Relatório fiscal. Escolho o mês passado, outubro. |
| Zoom suave nos cartões "Entrada" e "Saída". | Aqui em cima, o que entrou e o que saiu em notas no mês. |
| A câmera passa para o cartão "Saldo (Saída − Entrada)", com R$ 71.625,00 e "Positivo". [ZOOM: cartão "Saldo (Saída − Entrada)"] | O saldo é a saída menos a entrada. Em outubro, ficou positivo: setenta e um mil, seiscentos e vinte e cinco reais. |
| A câmera passa para o cartão "Pendentes + Rejeitadas", com 0 e "Tudo em dia". [ZOOM: cartão "Pendentes + Rejeitadas"] | E o último cartão junta as notas pendentes e as rejeitadas. Aqui está tudo em dia. Se aparecer um número, resolve antes de fechar o mês. |
| Rola até "Entrada × Saída no período", "Distribuição por status", "Top Fornecedores" e "Top Clientes". | Embaixo, o gráfico do mês, a divisão por status e o ranking dos fornecedores e dos clientes. |

### cap10 · O estoque pelas notas (vinheta: ESTOQUE FISCAL)

| Tela | Fala |
| --- | --- |
| Sub-aba "Posição do estoque": "Saldo fiscal agora, por material. Não altera o estoque operacional."; a tabela "Código", "Material", "Saldo fiscal". [BACKEND: saldo inicial fiscal de 01/08 e notas de agosto a novembro] | Agora, o estoque fiscal: o estoque contado só pelas notas. Na Posição do estoque, aparece o saldo fiscal de cada material, agora. |
| Em "Data e hora da posição", escolhe 31/10/2026 e 18:00; clica em "Ver posição": o subtítulo passa a "Saldo fiscal em ..." com a data escolhida. | Pra ver um dia do passado, escolho a data e a hora, aqui o fim de outubro, e clico em Ver posição. |
| A câmera fica na tabela e no botão "Voltar para agora". | Uma dica: essa posição é só consulta. Ela não muda saldo, nota, movimentação nem o estoque de hoje. E a data é sempre do passado, nunca do futuro. |
| Clica em "Voltar para agora"; sub-aba "Histórico fiscal"; na lista "Materiais", escolhe "Metal amarelo (latão)": o "KARDEX FISCAL" dele, com as linhas de outubro (a de 30/10, saída de 600 kg). | No Histórico fiscal fica o Kardex fiscal de cada material. Escolho o metal amarelo: cada linha é uma entrada ou uma saída, com o saldo antes e depois. |
| Sub-aba "Fiscal × operacional" (período "Mês passado"): os cartões e "Comparação por material"; a linha "Metal amarelo (latão)" com "Delta" −600. [ZOOM: linha do metal amarelo, colunas "Mov. Fiscal", "Mov. Operacional" e "Delta"] | Na última aba, o fiscal e o operacional ficam lado a lado. Repara no metal amarelo: seiscentos quilos de diferença. |
| [ILUSTRAÇÃO: fiscal × operacional: duas réguas do calendário, de outubro a novembro; em cima, "Notas (fiscal)": a nota de 600 kg de metal amarelo para a "Fundição Bandeira do Vale" cai em 30/10; embaixo, "Pedidos e pátio (operacional)": o pedido da mesma venda só fecha em 03/11, depois da linha "fim de outubro"; os 600 kg acendem na diferença.] | Foi uma venda pra Fundição Bandeira do Vale. A nota saiu no dia trinta de outubro, mas o pedido só foi finalizado no dia três de novembro. |
| (ilustração: as réguas ganham os rótulos "segue as notas" e "segue compras, pedidos e pátio") | O fiscal segue as notas. O operacional segue as compras, os pedidos e o pátio. Por isso, os dois podem dar diferente. |
| A ilustração sai; zoom no quadro "Como ler o Delta (fiscal − operacional)", na linha "Pedidos ainda não finalizados não entram no movimento operacional, o que também gera diferença.". | Uma dica: um não corrige o outro. Quando aparece diferença, este quadro, Como ler o Delta, ajuda a achar o motivo. |

### cap11 · O pacote do mês (vinheta: CONTADOR)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Notas Fiscais (NF-e)"; sub-aba "Saída"; clica no botão de três pontinhos ("Mais opções de NF-e"), ao lado de "Nova Nota", e em "Exportação Contábil". | Agora, o pacote que o contador pede todo mês. Ele fica em Notas Fiscais, no botão de três pontinhos: Exportação Contábil. |
| Diálogo "Exportação Contábil"; zoom em "Gera um pacote ZIP com XMLs, planilha e PDF resumo pra mandar pra contabilidade.". | Ele junta num arquivo só os XML das notas, uma planilha e um PDF de resumo. |
| Em "Período", escolhe "Mês passado". | No período, o mês passado. |
| A câmera passa por "Tipo de nota" ("Saída", "Entrada") e "Status" ("Emitidas", "Canceladas", "Inutilizadas", "Rejeitadas"), todos marcados. | Saída e entrada, e todos os status, já vêm marcados. Assim o contador recebe o mês inteiro. |
| A câmera passa por "Extras": "Incluir DANFEs (PDFs)" e "Incluir MDF-e's? (XML + DAMDFE)", marcados. | Nos extras, entram também o PDF de cada nota e os manifestos do período. |
| A câmera vai à prévia "21 notas no período (12 saída · 9 entrada)". [ZOOM: prévia "21 notas no período"] [BACKEND: `count_invoices_for_export`] | A prévia conta vinte e uma notas em outubro: doze de saída e nove de entrada. |
| Clica em "Baixar Pacote": a barra de progresso da exportação ("Gerando PDF resumo...", "Compactando pacote...") e o toast "Exportação pronta" / "12 saída + 9 entrada baixados"; o navegador baixa "Exportação Contábil - Recicla Vale Metais - <período>.zip". [BACKEND: XML e DANFEs de outubro; `plugnotas-download`] | Baixar Pacote. Ele monta tudo aqui no navegador e baixa o arquivo zip no computador. |

### cap12 · O que o contador faz (vinheta: CONTADOR)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: o pacote aberto: o arquivo "Exportação Contábil - Recicla Vale Metais - ....zip" se abre em pastas, uma por trecho da frase: "2026-10 › xmls › saida" e "entrada", "danfes", e os arquivos "Relacao-Notas-Fiscais.xlsx", "Relacao-Notas-Fiscais.pdf" e "LEIA-ME.txt" (nomes exatos do código; ícones genéricos, sem marca de programa).] | E o que vai dentro dele? Pastas com os XML de saída e de entrada, o PDF de cada nota, a planilha com a relação das notas e o resumo em PDF. |
| (ilustração: o pacote vai, por uma seta, até um cartão "Contador", com ícones genéricos de e-mail e de pasta compartilhada) | Você manda o pacote pro contador do jeito que vocês já combinam, por e-mail ou numa pasta compartilhada. |
| (ilustração: no cartão "Contador", três marcas acendem uma por vez: "confere as notas", "lança na contabilidade", "chama se algo não bater") | Com ele, o contador confere as notas do mês, lança na contabilidade e te chama se alguma coisa não bater. |
| (ilustração: uma pasta "Recicla Vale · notas de outubro" fica guardada do lado da empresa, ao lado da cópia que foi para o contador) | Uma dica: guardar os XML é responsabilidade da empresa, e não do sistema. Baixe o pacote todo mês e guarde uma cópia com você, além da que fica com o contador. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: "Veículo atualizado", o MDF-e nº 1 "Encerrado" e o percurso com o RJ. | Pronto! Recapitulando: a gente completou a frota com o caminhão e o motorista, emitiu o manifesto da carga de alumínio pra Minas, com o Rio de Janeiro no percurso, e encerrou no fim da viagem. |
| (montagem: a NFS-e nº 14 "Autorizada" e a nota da balança "Lançada") | Emitiu a nota de serviço da coleta com caçamba e lançou como despesa uma nota de serviço recebida. |
| (montagem: o cartão "Saldo (Saída − Entrada)", a linha do metal amarelo e o toast "Exportação pronta") | Conferiu o relatório fiscal de outubro, comparou o estoque fiscal com o operacional e exportou o pacote do mês pro contador. |
| Cartão "Próximo: Ambiental: MTR e CDF". | No próximo tutorial, a gente cuida da parte que mantém a licença da sua empresa de pé. Até lá! |
