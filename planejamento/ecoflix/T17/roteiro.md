# Roteiro T17 · Transporte, serviço e o contador

- **Título:** Transporte, serviço e o contador
- **Antes:** Nota Fiscal de mercadoria (NF-e) (T16)
- **Próximo:** Ambiental: MTR e CDF (T18)
- **Vinhetas (áreas):** TRANSPORTE · FROTA · MANIFESTO · SERVIÇO · RELATÓRIO FISCAL · ESTOQUE FISCAL · CONTADOR · RESUMO (todo
  capítulo menos o 0)
- **Duração estimada:** ~23 min de vídeo (3.191 palavras de fala, ~20,5 min a 2,6 palavras/s, mais a vinheta de abertura, 19
  vinhetas de capítulo, as esperas da SEFAZ simulada e a cartela). Aula única, mesmo longa (Kaik, 18/11): nenhum capítulo sai
  para outra aula.
- **App 1.60.10** (aplicação de 18/11 sobre o roteiro do 1.59.154; o que mudou e o que entrou: `T17/cobertura_160.md`).
  **20 capítulos (0 a 19).** Novos: 6 (manifesto recusado), 13 (saldo inicial), 15 (cancelamento e devolução). O antigo 8 virou
  9 e 10 (ativar; depois, as notas que chegaram) e o antigo 10 virou 12, 14 e 16. Renumerados: 6→7, 7→8, 8→9, 9→11, 10→12,
  11→17, 12→18, 13→19.
- Coluna Fala = texto da narração na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela =
  o que o robô faz e onde a câmera foca, rótulos entre aspas como no código 1.60.10 (`T17/inventario.md` e `T17/cobertura_160.md`). Logado como Rafael
  Nogueira (MASTER), desktop. Mundo e sementes: `T17/plano.md`. FAKE_NOW 10/11/2026 09:30 nos capítulos 0 a 4, 14:20 do 5 ao 9 e 14:40 do 10 em
  diante (junção 1.60: depois das notas 1249 a 1254 do T16; as duas notas do alumínio são a 1255 e a 1256).
- Exemplos em **Lucro Real**; **SPED Fiscal (BETA) fica fora**; no CIOT a tela não abre o balão "Como gerar o CIOT?" (ele cita a
  marca de um parceiro); CFOP e imposto, só os que a tela mostra (a fala não dita número de CFOP nem valor de imposto).
- Marcas: `[BACKEND: ...]` o que o backend falso ainda não tem; `[ZOOM: ...]` zoom suave que dura a frase inteira (sem zoom em cima de
  zoom); `[ILUSTRAÇÃO: ...]` desenho por código no estilo da marca, nunca tela inventada.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Transporte, serviço e o contador". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira. [ILUSTRAÇÃO: o dia da Recicla Vale: entra "Recicla Vale Metais · terça, 10 de novembro" e três cartões, um por trecho da frase: um caminhão com fardos de alumínio e a seta "Taubaté → Itamonte (MG)"; uma caçamba no pátio da "Aços Quiririm"; uma pasta "Outubro" indo para o "Contador".] | Oi! Neste tutorial a gente vai cuidar dos outros documentos da Recicla Vale Metais: o que acompanha a carga na estrada, o que cobra um serviço e o pacote que o contador pede todo mês. |
| (ilustração: os três cartões acendem um a um, na ordem da frase) | Hoje sai um caminhão de alumínio pra Minas Gerais, a coleta com caçamba na Aços Quiririm vira cobrança, e outubro fecha com o contador. |
| A ilustração sai; a câmera vai ao menu lateral e clica em "Fiscal & Ambiental"; o submenu abre e o destaque passa por "Transporte (MDF-e)", "Notas de Serviço (NFS-e)", "Estoque Fiscal" e "Relatórios Fiscais" (sem parar em "SPED Fiscal", se aparecer). | Tudo isso fica no menu Fiscal & Ambiental: em Transporte, em Notas de Serviço, no Estoque Fiscal e nos Relatórios Fiscais. |
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
| Clica na sub-aba "Frota": "Frota (veículos e motoristas do MDF-e)", aba "Veículos"; a lista "Veículos da frota" com FKD2E41 (Caminhão truck), GHT7B19 (Caminhão 3/4) e EZR4C63 (Picape), selo "Sem tipo"; clica no FKD2E41 na lista e o painel dele abre. [BACKEND: frota da base: placa, descrição, tara e capacidade (T12), sem dados de transporte] | Antes do primeiro manifesto, o caminhão e o motorista precisam estar na Frota. Os caminhões da Recicla Vale já estão aqui: é a mesma frota da pesagem. |
| Clica em "Editar" no painel do FKD2E41: "Editar veículo"; a câmera desce até "Dados de transporte (MDF-e / NF-e)". | Pro manifesto, faltam os dados de transporte do caminhão truck. Clico em Editar. |
| "UF de licenciamento" → "SP"; "Tipo" → "Veículo único (truck, toco, utilitário)"; "Tipo de rodado" → "Truck"; "Tipo de carroceria" → "Aberta". | Ele é emplacado em São Paulo. No Tipo, é um veículo único, sem carreta. O rodado é truck, e a carroceria é aberta. |
| A câmera para em "Tara (kg)" 6380 e "Capacidade (kg)" 14000, já preenchidos (vieram da frota das coletas). [ZOOM: "Tara (kg)" e "Capacidade (kg)"] | A tara, o peso do caminhão vazio, já veio da frota: seis mil trezentos e oitenta quilos. E ele leva até catorze mil quilos de carga. |
| Digita "30" em "Capacidade (m³)"; a câmera mostra a ajuda "máx. 999 m³" embaixo do campo. | Uma dica: peso aqui é sempre em quilos. Se o número parecer tonelada, a própria tela avisa. |
| Clica em "Salvar": toast "Veículo atualizado"; o painel mostra "Dados de transporte" preenchido e o selo "Veículo único". | Salvar, e o caminhão está pronto pro manifesto. |
| Aba "Motoristas": "Edson Moura" na lista; clica em "Editar": "Editar motorista". | Agora o motorista. O Edson Moura já está na lista. Clico em Editar. |
| Digita "318.472.650-90" em "CPF", "04728193604" em "CNH", escolhe "C" em "Categoria" e 18/03/2029 em "Validade da CNH". [ZOOM: "CPF"] | O manifesto leva o CPF do motorista, então eu completo o CPF, a CNH, a categoria e a validade. |
| Clica em "Salvar": toast "Motorista atualizado"; o painel mostra "Dados pessoais" e "Carteira de habilitação". | Salvar. Caminhão e motorista prontos. |

### cap03 · Numeração e percurso (vinheta: TRANSPORTE)

| Tela | Fala |
| --- | --- |
| Clica na sub-aba "Manifestos" e em "Configurações do MDF-e": diálogo "Configurações do MDF-e", "Série" 1, "Próximo Número" 1 e o quadro "Série" / "Próximo MDF-e". [ZOOM: quadro "Série" / "Próximo MDF-e"] | Com a frota pronta, uma olhada nas Configurações do MDF-e. Aqui ficam a série e o próximo número do manifesto. |
| A câmera sobe até "Série e próximo número do manifesto. Útil quando a empresa já emitiu MDF-e em outro sistema." (sem clicar em "Sincronizar Numeração", que no 1.60.10 só grava a série e o número). | A Recicla Vale nunca emitiu manifesto, então começa no número um. Se a sua empresa já emitia em outro sistema, é aqui que você continua a sequência. |
| A câmera desce até "Motoristas e veículos agora ficam em Transporte (MDF-e) → Frota" e o botão "Ir para Frota"; fecha o diálogo no "X". | E o caminhão e o motorista ficam na Frota, que a gente acabou de ver. |
| [ILUSTRAÇÃO: o percurso: mapa simplificado de SP, RJ e MG, sem marca de mapa; os pontos "Taubaté (SP)" e "Itamonte (MG)"; o caminhão parado em Taubaté com o rótulo "Carregamento".] | Agora, o percurso. Hoje o caminhão leva alumínio pra Serra Fina, em Itamonte, Minas Gerais. |
| (ilustração: uma linha sai de Taubaté, entra no RJ e sobe até Itamonte, onde aparece "Descarregamento"; o RJ acende em verde com "estado do meio do caminho") | Ele sai de Taubaté, passa pelo Rio de Janeiro e sobe pra Minas. São Paulo é a origem, Minas Gerais é o destino, e o Rio de Janeiro é o estado do meio do caminho. |
| (ilustração: o RJ vai para um cartão "Percurso (UFs Atravessadas)" com "1ª UF: RJ") | O estado do meio do caminho vai no Percurso. E isso a gente preenche em cada manifesto, na hora de emitir. |

### cap04 · Emitir o manifesto (vinheta: MANIFESTO)

| Tela | Fala |
| --- | --- |
| Clica em "Novo MDF-e": a tela cheia "Novo MDF-e (Manifesto Eletrônico)", com o quadro "Documento" / "Modelo 58" no cabeçalho; etapa "Notas fiscais", lista "NF-ES VINCULADAS"; o "Resumo do MDF-e" à direita. [BACKEND: semente `apos-cap02`; `inicio` com as NF-e 1255 e 1256 da Serra Fina de hoje] | Hora de emitir. Clico em Novo MDF-e, e o primeiro passo são as notas da carga. |
| Digita "Serra Fina" em "Buscar NF-e..." e marca a "NF-e #1255" e a "NF-e #1256" (as de hoje); embaixo, "2 NF-e(s) vinculada(s) • Valor total: R$ 55.380,00". [ZOOM: "Valor total: R$ 55.380,00"] | Busco a Serra Fina e marco as duas notas de hoje: o alumínio perfil e o alumínio bloco. Juntas, dão cinquenta e cinco mil, trezentos e oitenta reais. |
| A câmera desce até o quadro tracejado "Importar nota pela chave de acesso" e o texto "Use quando a NF-e foi emitida por outra empresa. Se ela já estiver em Notas Recebidas, preenchemos emitente e valor sozinhos.". | E quando o seu caminhão leva carga com nota de outra empresa? Por exemplo, buscar no fornecedor o material que você comprou. Aí a nota entra pela chave de acesso. |
| Cola a chave da NF-e nº 884 do Depósito Irmãos Siqueira em "Cole os 44 dígitos da chave" e clica em "Adicionar": toast "NF-e #884 encontrada em Notas Recebidas"; aparece a linha "NF-e #884 · Depósito Irmãos Siqueira", com o selo "Nota recebida" e o valor 2.100,00. [ZOOM: a linha com o selo "Nota recebida"] [BACKEND: `inbound_nfe` da 884 com chave válida, modelo 55] | Colo os quarenta e quatro dígitos e clico em Adicionar. Como essa nota já estava nas Notas Recebidas, o sistema preencheu quem emitiu e o valor. |
| Zoom no rodapé "3 NF-e(s) vinculada(s) • Valor total: R$ 57.480,00". | Se a nota não estiver lá, ela entra do mesmo jeito, só com a chave, e o valor você digita se quiser. |
| Clica no "X" da linha ("Remover NF-e 884"): volta a "2 NF-e(s) vinculada(s) • Valor total: R$ 55.380,00". | Hoje a carga é só da Recicla Vale, então eu tiro essa nota e sigo com as duas. |
| Clica em "Continuar": etapa "Veículo e motorista"; em "Veículo (tração)", escolhe "Caminhão truck • FKD2E41 • SP" (selo "Veículo único"); em "Motorista", "Edson Moura (318.472.650-90)". | Continuar. No veículo, o caminhão truck, e no motorista, o Edson. Como a Frota está completa, não falta nenhum dado. |
| A câmera passa por "Reboques / Carretas (opcional)" e o texto "Nenhuma carreta cadastrada. Marque suas carretas como Carreta / Reboque em Transporte → Frota para montá-las aqui.". | Se o caminhão puxa carreta, ela entra aqui, em Reboques, até três. Pra isso, a carreta precisa estar na Frota como Carreta / Reboque. |
| Clica em "Frete de terceiros (CIOT)", com o selo "Opcional": a seção abre. [ZOOM: "O CIOT é exigido no transporte rodoviário remunerado de cargas de terceiros. Não se aplica ao transporte de carga própria sem cobrança de frete."] | Aqui embaixo fica o frete de terceiros. O CIOT é um código exigido quando o transporte é pago: você contrata um caminhoneiro, ou leva a carga de outra empresa cobrando frete. |
| A câmera passa por "RNTRC", "CIOT" ("Código numérico com 12 dígitos") e "CPF/CNPJ do gerador do CIOT" ("Obrigatório junto do CIOT"). Não abre o balão "?" ("Como gerar o CIOT"), que cita a marca de um parceiro. | Nesse caso, vão aqui o registro do transportador na ANTT, o código do CIOT, com doze dígitos, e o CPF ou CNPJ de quem gerou o código. Os dois últimos andam juntos: um não entra sem o outro. |
| A câmera passa por "Contratante — CPF/CNPJ" e "Contratante — Nome". | E, se quiser, quem contratou o frete. |
| O cursor fica no campo "CIOT" (vazio). | O código é gerado antes da viagem, numa instituição autorizada pela ANTT. Na dúvida se a sua viagem precisa, pergunte ao contador. |
| Clica de novo em "Frete de terceiros (CIOT)": a seção fecha; a câmera volta ao veículo "Caminhão truck • FKD2E41 • SP". | Hoje a carga é da própria Recicla Vale, no caminhão dela, sem cobrar frete. Então fica em branco. |
| Clica em "Continuar": etapa "Trajeto e carga"; o cartão "Carregamento (Origem)" já está com "SP" e "Taubaté". [BACKEND: cidades da API do IBGE respondidas localmente para SP e MG] | Continuar. A origem já vem com a cidade da empresa: Taubaté. |
| Clica em "Adicionar UF ao percurso"; na linha "1ª UF", escolhe "RJ". | No Percurso, eu adiciono o Rio de Janeiro, o estado do meio do caminho. |
| No cartão "Descarregamento (Destino)", troca a UF para "MG" e escolhe a cidade "Itamonte"; o "Resumo do MDF-e" mostra "Itamonte/MG" em "Destino". | E no destino, Minas Gerais, cidade de Itamonte. |
| A câmera desce até "Peso Bruto Total (kg)" 5800, com "Somado das notas selecionadas — edite se o peso bruto real diferir.", e "Valor Total da Carga (R$)" 55.380,00, com "Sugerido pelas notas — pode ajustar.". [ZOOM: "Peso Bruto Total (kg)" e "Valor Total da Carga (R$)"] | O peso já vem somado das notas: cinco mil e oitocentos quilos. E o valor da carga vem sugerido pelas notas. Se o valor real for outro, dá pra ajustar. |
| A câmera passa por "OBSERVAÇÕES" ("Observações que aparecerão no DAMDFE..."), sem digitar. | Embaixo ficam as observações, que saem impressas no papel do manifesto. |
| Clica em "Continuar": "Revise antes de emitir"; em "Como emitir", "Normal" já escolhido ("Envia para a SEFAZ agora"). [BACKEND: `mdfe_contingency_availability` devolve disponível] | Na revisão, o jeito de emitir fica no Normal, que envia pra SEFAZ na hora. |
| Clica em "Contingência" ("Use quando a SEFAZ estiver indisponível"): aparecem "Motivo da contingência *", "Tipo de carga *", "NCM do produto *" e "Produto predominante *" (e o quadro "Ainda faltam informações", porque nada foi preenchido). | Uma dica: a contingência é só pra quando a SEFAZ estiver fora do ar. Ela pede o motivo, o tipo de carga, o NCM e o produto principal da carga. |
| Zoom em "Imprima o DAMDFE em papel antes de liberar o caminhão. Prazo de regularização: até 168 horas.". [ZOOM: a frase] | Nesse caso, o motorista só sai com o manifesto impresso em papel. E o prazo pra regularizar com a SEFAZ é de até cento e sessenta e oito horas, sete dias. |
| Clica de volta em "Normal"; o quadro verde "Tudo pronto para criar e emitir o MDF-e" reaparece. | Hoje a SEFAZ está no ar, então eu volto pro Normal. |
| Clica em "Criar MDF-e": toasts "MDF-e #1 criado" e "MDF-e #1 enviado ao motor fiscal próprio"; a lista mostra o nº 1 com "Aguardando SEFAZ". [BACKEND: function `mdfe-contingency`, `action: "prepare"` → aguardando_sefaz] | Tudo pronto. Criar MDF-e. O manifesto número um foi criado e já foi enviado pra autorização. |
| Espera a consulta automática (5 s): toast "MDF-e #1 autorizado!"; o selo vira "Autorizado"; a câmera fica na linha (Nº 1, Edson Moura, FKD2E41, o trajeto, R$ 55.380,00, 5.800). [ZOOM: linha do nº 1 com "Autorizado"] [BACKEND: `mdfe-contingency`, `action: "status"` → autorizado na 1ª consulta] | Pronto, autorizado. Na linha aparecem o motorista, a placa, o trajeto, o valor e o peso. |
| Passa o mouse em "Ações" da linha: o menu mostra "Encerrar", "Cancelar", "Baixar DAMDFE (PDF)" e "Baixar XML" (sem clicar). | E pelo menu de ações você baixa o PDF do manifesto, que vai com o motorista na viagem. |

### cap05 · Encerrar no fim da viagem (vinheta: MANIFESTO)

| Tela | Fala |
| --- | --- |
| Corte para a tarde: Transporte › "Manifestos", o nº 1 "Autorizado"; o cartão "MDF-e Autorizados" em 1. [BACKEND: semente `apos-cap04`, FAKE_NOW 14:20] | À tarde, a carga foi entregue em Itamonte. Agora falta encerrar o manifesto. |
| [ILUSTRAÇÃO: encerrar × cancelar: em cima, a linha do tempo "Autorizado" (o caminhão sai de Taubaté) → estrada → "Encerrado" (carga entregue em Itamonte), com um visto; embaixo, um ramo à parte, "Cancelar": um manifesto riscado, que não deveria existir, com um relógio e "prazo curto".] | Uma dica: encerrar não é cancelar. Encerrar é o fim normal da viagem. Cancelar é anular um manifesto que não deveria existir, e tem prazo curto. |
| A ilustração sai; "Ações" da linha → "Cancelar": diálogo "Cancelar MDF-e #1". [ZOOM: "O cancelamento será enviado à SEFAZ e é irreversível.", "O prazo para cancelamento geralmente é de 24 horas após a autorização, variando conforme a UF." e "Motivo do cancelamento (mín. 15 caracteres)"] | Olha o cancelamento: ele não tem volta, pede um motivo com pelo menos quinze letras, e o prazo costuma ser de vinte e quatro horas depois da autorização. |
| Clica em "Voltar"; o manifesto continua "Autorizado". | Não é o caso aqui. Voltar. |
| Passa o mouse em "Ações" da linha e clica em "Encerrar": toast "Encerramento enviado. Aguardando confirmação da SEFAZ — o status é atualizado automaticamente."; o selo vira "Encerramento enviado". [BACKEND: `mdfe-contingency`, `action: "enclose"` → encerramento_pendente] | No menu de ações, Encerrar. O pedido vai pra SEFAZ, e o selo mostra que o encerramento foi enviado. |
| Espera a consulta (5 s): toast "MDF-e #1: encerramento confirmado pela SEFAZ"; selo "Encerrado"; o cartão "MDF-e Encerrados" vai a 1. [ZOOM: selo "Encerrado" e cartão "MDF-e Encerrados"] [BACKEND: `mdfe-contingency`, `action: "status"` → encerrado] | Pronto, encerrado. A viagem está fechada, e o manifesto passa a contar nos encerrados. |

### cap06 · Quando o manifesto não passa (vinheta: MANIFESTO) · NOVO

| Tela | Fala |
| --- | --- |
| Transporte › "Manifestos": o nº 2 "Rejeitado" (GHT7B19, Jair Lopes, Taubaté/SP → Itamonte/MG, R$ 1.560,00, 150) em cima do nº 1 "Encerrado"; o cartão "MDF-e Rejeitados" em 1. [ZOOM: selo "Rejeitado" e cartão "MDF-e Rejeitados"] [BACKEND: semente lateral `mdfe2-rejeitado` por cima da `apos-cap05`] | E quando a SEFAZ não aceita? Olha o manifesto número dois, da viagem de amanhã: ele ficou como rejeitado, e conta aqui em cima, nos rejeitados. |
| "Ações" da linha do nº 2 → "Ver Erro": diálogo "Erro no MDF-e #2", com "A SEFAZ recusou o MDF-e" e o detalhe "CPF do condutor: número inválido". [ZOOM: o detalhe] | No menu de ações, Ver Erro. O sistema mostra o motivo. Aqui, o CPF do motorista está errado. |
| Clica em "Fechar"; passa o mouse em "Ações" de novo: "Ver Erro", "Reemitir" e "Excluir" (sem clicar). | Fechar. No mesmo menu ficam Reemitir e Excluir. |
| O cursor passa por "Reemitir" e depois por "Excluir"; sai do menu. | Se a recusa foi uma falha de momento, é só Reemitir. Se o erro está num dado do manifesto, o caminho é excluir, corrigir o cadastro na Frota e criar outro. |
| [ILUSTRAÇÃO: os selos de recusa, com os rótulos do código: à esquerda "Rejeitado" (o manifesto não vale: corrigir e criar outro); à direita "Encerramento recusado" e "Cancelamento recusado" (o manifesto continua "Autorizado": ver o erro e pedir de novo).] | E se a SEFAZ recusar um encerramento ou um cancelamento, o manifesto continua valendo. É só ver o erro e pedir de novo. |
| A ilustração sai; o cursor vai a "Buscar por nº, placa ou motorista..." e depois clica na linha do nº 1: abre "Detalhes do MDF-e #1". | Pra achar um manifesto antigo, tem a busca por número, placa ou motorista. E clicando na linha, abrem os detalhes dele. |

### cap07 · A nota de serviço (vinheta: SERVIÇO)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Notas de Serviço (NFS-e)": título "Nota Fiscal de Serviço (NFS-e)", lista com o nº 13 (Aços Quiririm Ltda, R$ 1.850,00) e o nº 12 (Fundição Bandeira do Vale, R$ 950,00), os dois "Autorizada"; a câmera não para nos cartões de cima. [BACKEND: NFS-e 12 e 13 na semente] | Agora, a nota de serviço. Ela fica em Notas de Serviço. |
| [ILUSTRAÇÃO: mercadoria × serviço, lado esquerdo "Mercadoria": fardos de sucata saindo do pátio no caminhão, com a folha "NF-e" e o rótulo "SEFAZ".] | Pensa assim: quando a Recicla Vale vende sucata, a mercadoria sai do pátio. A nota dessa venda é a nota fiscal de mercadoria, a NF-e. |
| (ilustração, lado direito "Serviço": uma caçamba recolhida no pátio da "Aços Quiririm", com a folha "NFS-e", o rótulo "Prefeitura" e um pátio sem nenhuma mercadoria saindo) | Quando ela cobra um trabalho, como a coleta com caçamba, não sai mercadoria nenhuma. Essa é a nota de serviço, a NFS-e, que é da prefeitura. |
| A ilustração sai; zoom nas colunas "Número", "Tomador", "Valor" e "Status" da lista. | Na lista ficam as notas de serviço emitidas: o número, quem contratou, que aqui se chama tomador, o valor e o status. |
| Zoom no botão "Configurações Fiscais" do cabeçalho, sem clicar. | E os dados da empresa que a nota de serviço usa, como a inscrição municipal, ficam nas Configurações Fiscais. Quem confere esses dados é o contador. |

### cap08 · Emitir e acompanhar (vinheta: SERVIÇO)

| Tela | Fala |
| --- | --- |
| Clica em "Nova NFS-e": a tela cheia "Nova NFS-e" ("Informe o tomador, o serviço e os valores antes de transmitir ao município."), quadro "Ambiente" / "Produção"; aba "Pessoas", "Data de competência" com 10/11/2026 e o selo de pendências na barra de cima. [BACKEND: RPC `fiscal_onboarding_status` com o certificado pronto] | Vou cobrar a coleta com caçamba que a Recicla Vale fez na Aços Quiririm. Nova NFS-e. |
| Troca a "Data de competência" para 06/11/2026. A câmera passa por "Série da DPS" ("Série 1") e "Próxima DPS: nº 14". [ZOOM: "Próxima DPS: nº 14"] [BACKEND: `nfse_series` com a série 1; RPC `get_next_nfse_number` → 14] | Na data de competência vai o dia do serviço: seis de novembro. A série e o próximo número já aparecem aqui: esta vai ser a catorze. |
| Em "Tomador do serviço", clica em "Cliente ou fornecedor": "Selecionar tomador"; digita "Aços" em "Buscar por nome, CNPJ/CPF ou código..." e escolhe "Aços Quiririm Ltda". O cursor passa por "Buscar pelo CNPJ". | No tomador, quem contratou, eu escolho a Aços Quiririm no cadastro. Se ele não tiver cadastro, dá pra buscar pelo CNPJ. |
| Clica em "Avançar": aba "Serviço"; "Município" já com "Taubaté"; clica em "Selecionar código de tributação", digita "coleta" em "Buscar por código ou descrição..." e escolhe o código de coleta e remoção de resíduos; "Código do serviço (LC116)" se preenche sozinho. [BACKEND: `plugnotas-nfse-servicos-municipio` com a lista de Taubaté] | Avançar. O município já vem como Taubaté. O código do serviço é o seu contador que passa. Aqui, coleta e remoção de resíduos. |
| Zoom em "Puxar serviço salvo", sem clicar. | Se a empresa emite sempre o mesmo serviço, ele pode ficar salvo, e aí é só puxar por aqui. |
| Digita em "Descrição do serviço": "Coleta e remoção de resíduos metálicos com caçamba no pátio da Aços Quiririm em 06/11/2026." | Na descrição, o que foi feito, do jeito que vai aparecer na nota. |
| Clica em "Avançar": aba "Valores"; digita "1850" em "Valor do serviço"; a barra de cima mostra "Total da nota" R$ 1.850,00. [ZOOM: "Valor do serviço"] | Avançar. O valor do serviço: mil oitocentos e cinquenta reais. |
| Em "Alíquota ISS %", digita 3 (no 1.60.10 a alíquota da lista do município ainda não chega a este campo: MELHORIAS). [ZOOM: "Alíquota ISS %"] | Na alíquota do ISS, eu coloco três por cento, o número da lista do município. Quem confirma esse número é o contador. |
| A câmera passa por "ISS retido na fonte" ("Tomador é responsável por reter e recolher.", desligado) e por "Retenções federais (R$)" ("Informe o valor efetivamente retido de cada tributo."), sem preencher. [ZOOM: "ISS retido na fonte" e "Retenções federais (R$)"] | Repara nestas opções. Se quem contratou é quem recolhe o ISS, você liga o ISS retido na fonte. E embaixo ficam as retenções federais, em reais: o valor que o cliente descontou de cada imposto. |
| A câmera sobe até "Ajustes (deduções e descontos)" e volta; "Valor líquido" R$ 1.850,00. | Isso acontece bastante quando o cliente é empresa, como a Aços Quiririm, que está no Lucro Real. Se tem retenção e de quanto, quem diz é o contador. Nesta nota não tem, então fica tudo zerado. |
| Clica em "Avançar": aba "Pré-visualização", o espelho da nota com a Aços Quiririm, o serviço, R$ 1.850,00, "Série" 1 e "Nº RPS (previsto)" 14; selo "Pronta pra emitir". | Na pré-visualização, a nota aparece como vai sair, já com a série e o número. E o selo mostra que ela está pronta pra emitir. |
| O cursor passa pelo botão "Salvar rascunho", sem clicar. | Se ainda faltar alguma informação do contador, dá pra salvar o rascunho e continuar depois. |
| Clica em "Emitir NFS-e": toast "NFS-e enviada. A confirmação oficial aparecerá na lista."; a lista mostra a nova linha "Processando". [BACKEND: `plugnotas-emit-nfse` → processando] | Emitir NFS-e. Ela foi enviada, e entra na lista como processando. |
| Espera a consulta automática (8 s): selo "Autorizada" e "14" na coluna "Número". [ZOOM: "14" na coluna "Número" com "Autorizada"] [BACKEND: `plugnotas-nfse-status` → emitida, nº 14] | E em instantes fica autorizada: nota de serviço número catorze. |
| Abre o menu "Ações" da linha e passa por "Baixar PDF", "Histórico" e "Cancelar" (sem clicar); fecha o menu. | Pelo menu, você baixa o PDF pra mandar pra Aços Quiririm, acompanha tudo no Histórico e, se a nota saiu errada, pede o cancelamento. |

### cap09 · O serviço que você tomou (vinheta: SERVIÇO)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Notas Fiscais (NF-e)"; sub-aba "Notas Recebidas"; aba "NFS-e": "Ative as Notas de Serviço Recebidas". [BACKEND: `nfse_dfe_ativo` desligado; `nfse_dfe_fonte` "sefin"] | E quando é a Recicla Vale que contrata um serviço? A nota chega em Notas Fiscais, nas Notas Recebidas, na aba NFS-e. |
| Zoom no texto "...as notas de serviço (NFS-e) que prestadores emitem contra o CNPJ da sua empresa... passam a entrar aqui automaticamente, prontas pra virar despesa." | São as notas que outras empresas emitem contra o seu CNPJ: o contador, a manutenção, um frete. Elas entram aqui sozinhas, prontas pra virar despesa. |
| Clica em "Ativar NFS-e Recebidas": diálogo "Ativar o recebimento de notas de serviço?". [ZOOM: "Ao ativar, cada nota de serviço recebida passa a contar na sua cota mensal de documentos fiscais..."] | Clico em Ativar NFS-e Recebidas. Repara no aviso: cada nota recebida conta na cota mensal de documentos fiscais, a mesma das notas que você emite. |
| Clica em "Ativar mesmo assim": toast "Notas de serviço recebidas ativado"; a tela vira "Notas de serviço emitidas contra o seu CNPJ", com "Recurso ativo", a lista ainda vazia e a faixa "Busca solicitada no Ambiente Nacional. A lista atualiza automaticamente em até 10 minutos.". [ZOOM: a faixa] [BACKEND: update direto em `company_fiscal_config`] | Ativar mesmo assim. Pronto, ativado. A busca roda sozinha, e as notas chegam em alguns minutos. |
| Zoom no aviso fixo "A NFS-e é da prefeitura, e só chega aqui a nota de cidade que entrou no sistema nacional...". | Uma dica: só chega aqui a nota de cidade que já entrou no sistema nacional. Se uma nota não aparecer, peça o PDF ao prestador e lance a despesa na mão. |

### cap10 · Da nota recebida à despesa (vinheta: SERVIÇO) · era a 2ª metade do cap08

| Tela | Fala |
| --- | --- |
| Corte (FAKE_NOW 14:40): a mesma aba, agora com duas linhas na lista. [BACKEND: semente lateral `nfse-recebidas` por cima da `apos-cap09`: o que o motor fiscal trouxe do Ambiente Nacional] | Um pouco depois, chegaram duas notas. |
| Zoom nas duas linhas: "Contabilidade Manacá Ltda" R$ 1.650,00 e "Balanças Tremembé Manutenção Ltda" R$ 980,00. [ZOOM: colunas "Prestador" e "Valor"] | Os honorários do escritório de contabilidade, de mil seiscentos e cinquenta reais, e a aferição da balança rodoviária, de novecentos e oitenta. |
| O cursor vai a "Última sincronização há 16 minutos" e ao botão "Sincronizar agora" (sem clicar). | Aqui em cima aparece quando foi a última busca. E se você quiser adiantar, é só clicar em Sincronizar agora. |
| Abre "Ações" na linha da Balanças Tremembé; no grupo "Financeiro", clica em "Lançar despesa / conta": "Nova conta" com "A pagar (despesa)", "Descrição" "Balanças Tremembé Manutenção Ltda" e "Valor" R$ 980,00 já preenchidos. | Serviço não entra no estoque, então aqui o caminho é a despesa. Na linha da balança, Lançar despesa ou conta. |
| Escolhe 20/11/2026 em "Vencimento" e "Manutenção de máquinas" em "Categoria"; clica em "Criar conta": toast "Conta criada"; a linha ganha o selo "Lançada". | A conta já vem com o valor e os dados da nota. Falta o vencimento, dia vinte, e a categoria. Criar conta. E a nota fica marcada como lançada. |
| Zoom no selo "Lançada" (o aviso "Lançar esta despesa de novo?" só é citado). | Se você tentar lançar a mesma nota de novo, o sistema avisa antes, pra despesa não entrar duas vezes. |

### cap11 · Entrada, saída e saldo (vinheta: RELATÓRIO FISCAL)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Relatórios Fiscais": título "Relatórios Fiscais", sub-aba "NF-e"; no filtro de período do cabeçalho, escolhe "Mês passado". [BACKEND: RPC `get_invoice_dashboard_secure` com `can_view_values`] | Antes de mandar o mês pro contador, vale conferir os números. Em Relatórios Fiscais, a primeira aba é a das notas de mercadoria. Escolho o mês passado, outubro. |
| Zoom suave nos cartões "Entrada" e "Saída". | Aqui em cima, o que entrou e o que saiu em notas no mês. |
| A câmera passa para o cartão "Saldo (Saída − Entrada)", com R$ 71.625,00 e "Positivo". [ZOOM: cartão "Saldo (Saída − Entrada)"] | O saldo é a saída menos a entrada. Em outubro, ficou positivo: setenta e um mil, seiscentos e vinte e cinco reais. |
| A câmera passa para o cartão "Pendentes + Rejeitadas", com 0 e "Tudo em dia". [ZOOM: cartão "Pendentes + Rejeitadas"] | E o último cartão junta as notas pendentes e as rejeitadas. Aqui está tudo em dia. Se aparecer um número, resolve antes de fechar o mês. |
| Clica no cartão "Entrada": abre a linha "Emitidas por você" com "9 · R$ 97.315,00". [ZOOM: a linha] | Clicando na Entrada, ela se abre. Em outubro, as nove notas foram emitidas pela própria Recicla Vale, nas compras de pessoa física. As notas que os fornecedores emitem contra ela aparecem aqui, numa linha separada. |
| A câmera fica no cartão aberto. | No Lucro Real, é nessas notas de fornecedor que o contador costuma buscar os créditos de imposto. |
| Rola até "Entrada × Saída no período", "Distribuição por status", "Top Fornecedores" e "Top Clientes". | Embaixo, o gráfico do mês, a divisão por status e o ranking dos fornecedores e dos clientes. |
| Volta ao topo; sub-aba "NFS-e": cartões "Serviços autorizados" (R$ 2.800,00, "2 notas válidas"), "ISS apurado", "Retenções federais" ("PIS, COFINS, CSLL, INSS e IRRF") e "Pendentes + rejeitadas". [ZOOM: os quatro cartões] [BACKEND: RPC `get_nfse_dashboard`] | A segunda aba é o mesmo relatório pras notas de serviço: quanto foi autorizado, o ISS do período e as retenções. |
| Rola até "Top tomadores" e "Top serviços". | E embaixo, quem mais contratou e quais serviços mais saíram. |

### cap12 · O estoque pelas notas (vinheta: ESTOQUE FISCAL)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Estoque Fiscal": sub-aba "Saldo atual", "Saldo fiscal atualizado, por material. Não altera o estoque operacional."; tabela "Código", "Material", "Saldo fiscal". [BACKEND: saldo inicial fiscal de 01/08 (menos a bateria) e notas de agosto a novembro] | Agora, o estoque fiscal: o estoque contado só pelas notas. Ele abre no Saldo atual, com o saldo fiscal de cada material. |
| Zoom nas linhas "Alumínio bloco" e "Alumínio perfil" (já sem os 5.800 kg das notas de hoje). | Esse saldo se atualiza sozinho. As notas do alumínio que saíram hoje de manhã já estão descontadas aqui. |
| Digita "cobre" em "Buscar material ou código": a tabela filtra (Cobre mel, Cobre misto, Fio de cobre encapado); limpa a busca. | Pra achar um material, é só buscar pelo nome ou pelo código. |
| A câmera fica na coluna "Saldo fiscal". | Se algum saldo aparecer em vermelho, é porque ficou negativo: saiu mais nota do que entrou. |
| Zoom na faixa amarela "Alguns saldos foram apurados pelas notas disponíveis, pois ainda não têm saldo inicial informado.". [ZOOM: a faixa] | Repara no aviso amarelo: tem material sem saldo inicial. Nesse caso, o sistema conta só pelas notas que ele conhece. |

### cap13 · O saldo inicial (vinheta: ESTOQUE FISCAL) · NOVO

| Tela | Fala |
| --- | --- |
| Na linha "Bateria automotiva" (640 kg), menu "⋯" → "Informar saldo inicial": diálogo "Informar saldo inicial", "O saldo fica só no estoque fiscal e passa a ser a base dos movimentos posteriores."; "Material" já vem com "13 · Bateria automotiva". | Quando a empresa começa a usar o sistema, ela já tem material no pátio. Esse ponto de partida é o saldo inicial. Aqui, falta o da bateria. Na linha dela, Informar saldo inicial. |
| "CNPJ" já escolhido; em "Data-base", 31/10/2026; em "Quantidade", digita 3320. [ZOOM: "Data-base" e "Quantidade"] | Escolho a data-base, que é o dia em que esse número valia: trinta e um de outubro. E a quantidade: três mil trezentos e vinte quilos. |
| A câmera fica no diálogo. | Uma dica: esse número é fiscal. No Lucro Real, o estoque entra no balanço, então combine o valor com o contador. |
| Clica na aba "Planilha": "Baixar modelo" e "Escolher planilha" (sem enviar); volta para "Manual" (os dados continuam). | Pra informar vários materiais de uma vez, tem a planilha: você baixa o modelo, preenche código e quantidade e envia. O sistema confere linha por linha antes de gravar. |
| Clica em "Confirmar saldo inicial": toast "Saldo inicial registrado"; a faixa amarela some. [BACKEND: RPC `record_fiscal_inventory_entries`, `opening_balance`] | Confirmar saldo inicial. O aviso amarelo some, e daqui pra frente as notas somam e descontam a partir desse saldo. |
| Zoom na linha "Bateria automotiva", agora com 3.960 kg. [ZOOM: a linha] | A bateria passa a três mil novecentos e sessenta quilos: o saldo inicial mais a nota que entrou em novembro. |

### cap14 · Um dia do passado e as movimentações (vinheta: ESTOQUE FISCAL) · era o meio do cap10

| Tela | Fala |
| --- | --- |
| Sub-aba "Posição em uma data": "Posição do estoque em uma data"; em "Data e hora da posição", 31/10/2026 18:00; clica em "Ver posição": "Saldo fiscal em 31/10/2026 às 18:00. Não altera o estoque operacional.". | Pra ver um dia do passado, a aba é a Posição em uma data. Escolho a data e a hora, aqui o fim de outubro, e clico em Ver posição. |
| A câmera fica na tabela. | É o número que o contador costuma pedir no fechamento do mês e do ano. |
| A câmera fica no subtítulo "Saldo fiscal em 31/10/2026 às 18:00.". | Uma dica: essa posição é só consulta. Ela não muda saldo, nota nem o estoque de hoje. E a data é sempre do passado. |
| Sub-aba "Movimentações"; na lista "Materiais", clica em "Metal amarelo (latão)": "KARDEX FISCAL — 10 - Metal amarelo (latão)", colunas "Data", "Origem", "Material", "Nota / CFOP", "Movimento", "Antes", "Depois". | Em Movimentações fica o Kardex fiscal. Escolho o metal amarelo: cada linha é uma nota, com o CFOP, a quantidade e o saldo antes e depois. |
| Clica em "Filtros": "De", "Até", "Tipo" (abre: "Todos os tipos", "Entrada", "Saída", "Saldo inicial", "Ajuste", "Estorno"; fecha sem escolher) e "Nota, chave ou parceiro". | Nos filtros, dá pra fechar num período, num tipo de movimento, ou buscar por nota, chave ou parceiro. |
| Clica em "Geral (Todos)": "KARDEX FISCAL — Geral". | E em Geral aparecem as movimentações de todos os materiais juntas. |

### cap15 · Cancelamento e devolução (vinheta: ESTOQUE FISCAL) · NOVO

| Tela | Fala |
| --- | --- |
| Em "Movimentações", com "Geral (Todos)" escolhido, abre "Filtros" e digita "1249" em "Nota, chave ou parceiro". | E quando uma nota é cancelada? Lembra da nota mil duzentos e quarenta e nove, cancelada hoje cedo? Eu busco por ela aqui, nos filtros. |
| Ficam duas linhas de 10/11: "Nota fiscal" nº 1249, −320 kg, e, acima dela, "Estorno" nº 1249, +320 kg, com o motivo "Pedido alterado pelo cliente antes de a mercadoria sair do pátio". [ZOOM: as duas linhas, colunas "Origem", "Movimento", "Antes", "Depois"] | A saída de trezentos e vinte quilos continua no Kardex, e logo acima entra o estorno, com o motivo do cancelamento. |
| [ILUSTRAÇÃO: uma régua do dia 10/11 com dois pontos: "Nota 1249 autorizada · −320 kg" e "Cancelada · estorno +320 kg"; a linha do saldo desce e volta.] | O sistema não apaga a nota. Ele devolve a quantidade na hora em que o cancelamento aconteceu. Assim, uma posição consultada entre os dois momentos mostra o saldo como era. |
| A ilustração sai; zoom na coluna "Depois" da linha do estorno. | O mesmo vale pra nota de fornecedor que foi cancelada depois de chegar: ela sai do saldo sozinha. |
| Clica em "Limpar filtros"; material "Cobre mel": a linha de hoje "Nota fiscal" nº 1253, Fundição Bandeira do Vale, com o CFOP de devolução e +40 kg. [ZOOM: a linha da 1253] [BACKEND: NF-e 1253 da T16 (devolução da Fundição, entrada)] | E a devolução? A Fundição Bandeira do Vale devolveu quarenta quilos de cobre mel. A nota de devolução, a mil duzentos e cinquenta e três, entra no estoque fiscal como entrada. |
| [ILUSTRAÇÃO: duas setas com os rótulos "devolução de venda: volta pro estoque" e "devolução de compra: sai do estoque".] | Devolução de venda, o material volta. Devolução de compra, o material sai. E vale igual pra dentro e pra fora do estado. |
| A ilustração sai; a câmera volta ao Kardex do cobre mel. | Uma dica: no Lucro Real, a devolução também mexe nos impostos da nota original. Essa parte é com o contador. Aqui você confere a quantidade. |

### cap16 · Fiscal e operacional (vinheta: ESTOQUE FISCAL) · era o fim do cap10

| Tela | Fala |
| --- | --- |
| Sub-aba "Fiscal × operacional"; no filtro de período do cabeçalho, escolhe "Mês passado"; "Comparação por material". | Na última aba, o fiscal e o operacional ficam lado a lado, material por material. Escolho o mês passado, outubro. |
| Zoom nos cartões "Materiais com divergência" e "Alertas". | Aqui em cima, o sistema conta quantos materiais deram diferença e quantos têm alerta, como saldo fiscal negativo. |
| A câmera desce até a linha "Metal amarelo (latão)": "Mov. Fiscal" −1.100, "Mov. Operacional" 0, "Delta" −1.100. [ZOOM: linha do metal amarelo, colunas "Mov. Fiscal", "Mov. Operacional" e "Delta"] | Repara no metal amarelo: mil e cem quilos de diferença. |
| [ILUSTRAÇÃO: fiscal × operacional: duas réguas do calendário, de outubro a novembro; em cima, "Notas (fiscal)": a nota de 600 kg de metal amarelo para a "Fundição Bandeira do Vale" cai em 30/10; embaixo, "Pedidos e pátio (operacional)": o pedido da mesma venda só fecha em 03/11, depois da linha "fim de outubro"; os 600 kg acendem na diferença.] | Seiscentos são de uma venda pra Fundição Bandeira do Vale. A nota saiu no dia trinta de outubro, mas o pedido só foi finalizado no dia três de novembro. |
| (ilustração: as réguas ganham os rótulos "segue as notas" e "segue compras, pedidos e pátio") | O fiscal segue as notas. O operacional segue as compras, os pedidos e o pátio. Por isso, os dois podem dar diferente. |
| A ilustração sai; zoom no quadro "Como ler o Delta (fiscal − operacional)", na linha "Delta negativo costuma indicar compra de pessoa física sem nota: entrou material no pedido, mas não houve nota de entrada.". [ZOOM: a linha] | Os outros quinhentos vêm do caso mais comum no ferro-velho: compra de pessoa física sem nota. O material entra no pátio, mas não entra no fiscal. |
| Zoom na linha "Pedidos ainda não finalizados não entram no movimento operacional, o que também gera diferença.". | Uma dica: um não corrige o outro. Este quadro, Como ler o Delta, ajuda a achar o motivo de cada diferença. |
| Volta ao topo e clica em "Exportar": o menu "Exportar estoque fiscal" com "PDF" e "Excel" (sem baixar); fecha o menu. | E dá pra exportar essa comparação em PDF ou em Excel e mandar junto pro contador. |

### cap17 · O pacote do mês (vinheta: CONTADOR)

| Tela | Fala |
| --- | --- |
| Menu "Fiscal & Ambiental" › "Notas Fiscais (NF-e)"; sub-aba "Saída"; clica no botão de três pontinhos ("Mais opções de NF-e"), ao lado de "Nova Nota", e em "Exportação Contábil". | Agora, o pacote que o contador pede todo mês. Ele fica em Notas Fiscais, no botão de três pontinhos: Exportação Contábil. |
| Diálogo "Exportação Contábil"; zoom em "Gera um pacote ZIP com XMLs, planilha e PDF resumo pra mandar pra contabilidade.". | Ele junta num arquivo só os XML das notas, uma planilha e um PDF de resumo. |
| A câmera passa por "Emitente / CNPJ" ("Selecione um CNPJ para gerar o pacote somente daquele emitente."). | Se a empresa tem mais de um CNPJ, dá pra gerar um pacote pra cada um. |
| Em "Período", escolhe "Mês passado". | No período, o mês passado. |
| Em "Origem dos documentos", marca "Incluir notas destinadas ao CNPJ". [ZOOM: "XMLs de NF-e emitidas por fornecedores contra a sua empresa. Entram na pasta “xmls/destinadas”."] | Aqui tem uma opção importante pra quem está no Lucro Real: incluir as notas que os fornecedores emitiram contra o seu CNPJ. É com o XML delas que o contador aproveita os créditos. |
| A câmera passa por "Tipo de nota" ("Saída", "Entrada") e "Status" ("Emitidas", "Canceladas", "Inutilizadas", "Rejeitadas"), todos marcados. | Saída e entrada, e todos os status, já vêm marcados. Assim o contador recebe o mês inteiro. |
| A câmera passa por "Extras": "Incluir DANFEs (PDFs)" e "Incluir MDF-e's? (XML + DAMDFE)", marcados. | Nos extras, entram também o PDF de cada nota e os manifestos do período. |
| A câmera vai à prévia "21 notas no período (12 saída · 9 entrada)" e à linha "Destinadas: 0 XML(s)". [ZOOM: a prévia] [BACKEND: `count_invoices_for_export`; nenhuma `inbound_nfe` em outubro] | A prévia conta vinte e uma notas em outubro: doze de saída e nove de entrada. E as destinadas vêm zeradas, porque em outubro a Recicla Vale ainda não recebia essas notas pelo sistema. No pacote de novembro, elas já entram. |
| Clica em "Baixar Pacote": a barra de progresso da exportação e o toast "Exportação pronta" / "12 saída + 9 entrada + 0 destinada(s) baixados"; o navegador baixa "Exportação Contábil - Recicla Vale Metais - <período>.zip". [BACKEND: XML e DANFEs de outubro; `plugnotas-download`] | Baixar Pacote. Ele monta tudo aqui no navegador e baixa o arquivo zip no computador. |

### cap18 · O que o contador faz (vinheta: CONTADOR)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: o pacote aberto: o arquivo "Exportação Contábil - Recicla Vale Metais - ....zip" se abre em pastas, uma por trecho da frase: "2026-10 › xmls › saida", "entrada" e "destinadas", "danfes", e os arquivos "Relacao-Notas-Fiscais.xlsx", "Relacao-Notas-Fiscais.pdf" e "LEIA-ME.txt" (nomes exatos do código; ícones genéricos, sem marca de programa).] | E o que vai dentro dele? Pastas com os XML de saída e de entrada, o PDF de cada nota, a planilha com a relação das notas, o resumo em PDF e, se você marcou, as notas dos fornecedores. |
| (ilustração: o pacote vai, por uma seta, até um cartão "Contador", com ícones genéricos de e-mail e de pasta compartilhada) | Você manda o pacote pro contador do jeito que vocês já combinam, por e-mail ou numa pasta compartilhada. |
| (ilustração: no cartão "Contador", três marcas acendem uma por vez: "confere as notas", "lança na contabilidade", "chama se algo não bater") | Com ele, o contador confere as notas do mês, lança na contabilidade e te chama se alguma coisa não bater. |
| (ilustração: uma pasta "Recicla Vale · notas de outubro" fica guardada do lado da empresa, ao lado da cópia que foi para o contador) | Uma dica: guardar os XML é responsabilidade da empresa, e não do sistema. Baixe o pacote todo mês e guarde uma cópia com você, além da que fica com o contador. |

### cap19 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: "Veículo atualizado", a etapa "Trajeto e carga" com o RJ no percurso, o MDF-e nº 1 "Encerrado" e o "Erro no MDF-e #2". | Pronto! Recapitulando: a gente completou a frota com o caminhão e o motorista, emitiu o manifesto da carga de alumínio pra Minas, com o Rio de Janeiro no percurso, encerrou no fim da viagem e viu o que fazer quando a SEFAZ recusa. |
| (montagem: a NFS-e nº 14 "Autorizada", "Notas de serviço recebidas ativado" e a nota da balança "Lançada") | Emitiu a nota de serviço da coleta com caçamba, ativou as notas de serviço recebidas e lançou uma delas como despesa. |
| (montagem: o cartão "Saldo (Saída − Entrada)", "Saldo inicial registrado", o estorno da 1249, a linha do metal amarelo e o toast "Exportação pronta") | Conferiu os relatórios fiscais de outubro, informou um saldo inicial, viu o cancelamento e a devolução no Kardex, comparou o estoque fiscal com o do pátio e exportou o pacote do mês pro contador. |
| Cartão "Próximo: Ambiental: MTR e CDF". | No próximo tutorial, a gente cuida da parte que mantém a licença da sua empresa de pé. Até lá! |
