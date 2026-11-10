# Roteiro T0 · Bem-vindo ao EcoSistema

Roteiro pronto para o ensaio gravado e, depois da revisão geral, para a voz (voz Kaik Barreto, ElevenLabs eleven_v4). Coluna
Fala = texto da narração na grafia da legenda (uma linha da tabela = uma linha da fala); a grafia de pronúncia do TTS está em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
(`T00/inventario.md`, versão 1.59.154). Estados S1, S2, S3 e S13, dados novos e o que muda no vertical: `T00/plano.md`.
Marcas: `[BACKEND: ...]` (o backend falso ainda não tem), `[ZOOM: ...]` (dura a frase inteira), `[ILUSTRAÇÃO: ...]` (cena
desenhada, nunca tela inventada), `[CELULAR]` (gravação 390×844), `[TESTAR]` (o robô confere antes de gravar).
Sem preço na fala: o valor da mensalidade e o da economia anual ficam na tela, sem destaque.

- **Título:** Bem-vindo ao EcoSistema
- **Antes:** nenhum (primeira aula; vídeo obrigatório do primeiro acesso, sem cartão "Antes:")
- **Próximo:** Sua conta e sua empresa (T1)
- **Vinhetas (áreas):** COMEÇANDO · TRILHA · TRILHA · AJUDA · O SISTEMA · MENU · MENU · VOCABULÁRIO · ASSINATURA ·
  ASSINATURA · ASSINATURA · ASSINATURA · RESUMO (todos os capítulos menos o 0)
- **Formatos:** 16:9 e 9:16 (vertical), mesmo áudio e mesma legenda
- **Duração estimada:** ~11 min de vídeo (1.533 palavras de fala, ~9,8 min de voz a 2,6 palavras/s, mais a vinheta de abertura,
  13 vinhetas de capítulo e a cartela); alvo da fonte ~12 min

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta da aula EcoFlix com o título "Bem-vindo ao EcoSistema". | (sem fala) |
| [ILUSTRAÇÃO: o caminho do pátio: título "Bem-vindo ao EcoSistema" no alto; acendem em sequência, presos às palavras "sucata", "portão" e "conta", as estações "Portão", "Balança", "Caixa", "Estoque", "Venda" e "Dinheiro na conta", ligadas por uma linha verde; ícones genéricos, sem marca] | Oi! Boas-vindas ao EcoSistema. A partir de agora, a sua empresa tem um lugar só pra organizar tudo, da sucata que entra no portão até o dinheiro na conta. |
| [ILUSTRAÇÃO: o caminho sobe e diminui; entram três cartões, cada um na sua expressão: "Os combinados", "O sistema por cima", "O seu plano"] | Neste tutorial, a gente firma os combinados da nossa parceria, dá uma volta pelo sistema e vê o seu plano. |
| [ILUSTRAÇÃO: cartão "Recicla Vale Metais", "Ferro-velho em Taubaté, SP", com a etiqueta "Empresa de exemplo das aulas"] | Em todas as aulas, a empresa de exemplo é a Recicla Vale Metais, um ferro-velho de Taubaté, com dados inventados. |
| O cartão fica na tela. | Esta é a primeira aula, então é só seguir daqui. [pause] Vamos aos combinados. |

### cap01 · Os combinados (vinheta: COMEÇANDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S1). O portão abre sozinho sobre o Dashboard: no cabeçalho, o logo do EcoSistema e o selo "Primeiro passo"; no painel, "Antes de usar o sistema" e "Bem-vindo, Rafael". [BACKEND: S1: `get_ecoflix_learning_status` com `introGate.required` true, `accountStage` "trial", T0 sem progresso; player com vídeo fictício local, mudo] | Este vídeo é o primeiro passo. Ele aparece no primeiro acesso, antes de qualquer tela do sistema. |
| Destaque em "Este vídeo explica os combinados importantes da nossa parceria e mostra como aproveitar os tutoriais.". | Os combinados são três: aprender pela trilha, na ordem; tirar dúvida pela própria aula; e acompanhar o seu plano na tela Assinatura. |
| [ZOOM: a caixa "Assisti ao vídeo até o final e entendi os combinados." (ainda apagada) e o botão "Assista até o final para confirmar"] | No fim do vídeo, você marca que assistiu e entendeu, e o sistema libera a primeira aula. |
| Destaque no quadro "Você pode pular durante o teste" e no botão "Pular por agora" (sem clicar). | Começou pelo período de teste? Aí dá pra pular por agora, e o ponto em que você parou fica salvo. |
| [ILUSTRAÇÃO: linha do tempo "Período de teste" → "Assinatura ativa". Em cima, na frase "quem confirma", o caminho "Assistiu e confirmou": o selo verde "Combinados confirmados" segue até a assinatura. Embaixo, na frase "quem pula", o caminho "Pulou": na "Assinatura ativa" o vídeo volta com a etiqueta "Etapa obrigatória"] | Uma dica: vale assistir até o fim ainda no teste. Quem confirma no teste não vê este vídeo de novo ao contratar. Quem pula, vê ele voltar como etapa obrigatória. |

### cap02 · Como funciona a trilha (vinheta: TRILHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), no Dashboard. Clique no cartão "Rafael Nogueira" (selo "MASTER", "Recicla Vale Metais Ltda"), no rodapé do menu; o menu da conta abre; destaque em "Tutoriais \| EcoFlix" e clique. [BACKEND: S2 (plano, "Mundo"): trilha `tutoriais-do-sistema` com as 26 aulas; T0 concluído] | E a trilha, como funciona? Ela fica no menu da sua conta, em Tutoriais EcoFlix. |
| A trilha abre: "Olá, Rafael · continue sua trilha", "Aprenda a usar o EcoSistema", o botão "Começar trilha", "Trilha do seu plano" e a barra. | Aqui estão todas as aulas, já na ordem certa. |
| A câmera desce pelos primeiros módulos, com o selo "Formação básica": "Bem-vindo ao EcoSistema" ("Concluída") e "Sua conta e sua empresa" ("Próxima aula recomendada"). | Primeiro vem a Formação básica: o que todo ferro-velho usa no dia a dia, como compra, venda, caixa e estoque. |
| A câmera desce até o primeiro módulo com o selo "Tem no seu plano" (T16) e para no selo. | Depois vêm os módulos do seu plano, com o selo Tem no seu plano. |
| A câmera volta ao T1; destaque em "Próxima aula recomendada". | A próxima aula recomendada fica marcada, e o progresso fica salvo: dá pra parar e continuar de onde parou. |
| Clique em "Materiais e tabelas de preço" ("Na sequência da formação básica"): o diálogo "Consultar fora da ordem?" ("Sua próxima aula recomendada continuará marcada na trilha."); depois da frase, clique em "Voltar à trilha". | Precisa consultar uma aula fora da ordem? Pode abrir. O sistema só confirma, e a próxima recomendada continua marcada. |

### cap03 · Aulas de outros módulos (vinheta: TRILHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S3), na trilha; a câmera desce até o último módulo, "CRM/Kanban", com o selo "Não tem no seu plano" e a aula marcada "Conheça este módulo". [BACKEND: S3 = S2 sem `crm_kanban` em `company_modules`; no T26, `includedInPlan` false e `requiredForUser` false] | E os módulos que não estão no seu plano? Eles também aparecem na trilha, com o selo Não tem no seu plano. |
| Clique na aula; "Consultar fora da ordem?" → "Consultar esta aula". A aula abre; destaque no painel da trilha em "Conheça outros módulos" e "Você pode assistir e contratar direto pela aula.". | Pode assistir à vontade. É um jeito de conhecer a função antes de contratar. |
| A câmera desce aos detalhes da aula: o selo "Não tem no seu plano" e o cartão "Conheça agora. Ative quando fizer sentido.", com o botão "Adicionar ao meu plano" (sem clicar; sem zoom no texto do valor). | Se fizer sentido, a contratação sai da própria aula, pelo administrador da empresa. |
| [ILUSTRAÇÃO: a barra "Trilha do seu plano": os blocos "Formação básica" e "Módulos do seu plano" entram na barra e enchem o progresso, na frase "contam só"; os blocos "Outros módulos" ficam ao lado, fora da barra] | E essas aulas não mexem no seu progresso. Na barra da trilha, contam só a Formação básica e os módulos do seu plano. |

### cap04 · Dúvida depois da aula (vinheta: AJUDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), na trilha: clique em "Começar trilha"; abre a aula "Sua conta e sua empresa". A câmera desce do player aos detalhes e para no botão verde "Tirar dúvidas com o suporte" (sem clicar). | Ficou alguma dúvida depois da aula? Embaixo do vídeo tem o botão Tirar dúvidas com o suporte. |
| [ILUSTRAÇÃO: "Mensagem pronta para o suporte": um balão de conversa genérico, sem marca de aplicativo, onde entram, um por vez, os itens da mensagem do app (`EcoFlixLessonDetails.tsx:45-55`): "E-mail do usuário: rafael.nogueira@reciclavalemetais.example", "Empresa: Recicla Vale Metais Ltda", "Trilha: Tutoriais do sistema", "Módulo: Sua conta e sua empresa" e, por último, "Minha dúvida:" com o cursor piscando] | Ele abre o WhatsApp do suporte com a mensagem pronta: o seu e-mail, a sua empresa, a trilha e a aula. É só escrever a dúvida e enviar. |
| A ilustração sai; a aula volta, com o botão em destaque. | Assim, quem te atende já sabe de qual aula você está falando. |

### cap05 · Do portão até a conta (vinheta: O SISTEMA)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: "Do portão até a conta", estação "Portão": a Dona Cida (figura genérica) chega com sacos de latinha] | Bom, o que o EcoSistema resolve? Pensa num dia comum na Recicla Vale. A Dona Cida chega com latinha. |
| [ILUSTRAÇÃO: estação "Balança": o visor desenhado marca "38 kg"; o visor cresce na tela durante a frase] | A balança marca trinta e oito quilos. |
| [ILUSTRAÇÃO: estação "Caixa": um recibo "Pedido de compra · Alumínio latinha · 38 kg × R$ 6,20 = R$ 235,60"; o dinheiro sai do caixa para a Dona Cida] | No caixa, isso vira um pedido de compra: a seis reais e vinte o quilo, dá duzentos e trinta e cinco reais e sessenta, pagos na hora. |
| [ILUSTRAÇÃO: estação "Estoque": "Alumínio latinha + 38 kg"] | O material entra no estoque. |
| [ILUSTRAÇÃO: estação "Venda": a latinha juntada vai para "Serra Fina Alumínio Reciclagem", com o ícone de nota fiscal] | Depois, a latinha juntada é vendida pra Serra Fina Alumínio Reciclagem, com a nota fiscal. |
| [ILUSTRAÇÃO: estação "Dinheiro na conta": um banco genérico; a linha verde fecha o caminho; aparece um painel "Números do dia e do mês"] | E o dinheiro cai na conta. Tudo isso vira os números do dia e do mês. |
| [ILUSTRAÇÃO: cada estação ganha a etiqueta da sua aula: "Balança e impressora: o EcoTray", "Caixa: abrir, fechar e o cofre", "Comprar e vender sucata", "Estoque: saldo, histórico e posição", "Nota Fiscal de mercadoria (NF-e)", "Bancos, cofre e conciliação bancária"] | Cada parte desse caminho tem a sua aula na trilha. |

### cap06 · Um passeio pelo menu (vinheta: MENU)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), no Dashboard ("Olá, Rafael!"); a câmera enquadra o menu lateral inteiro, sem abrir nada. [TESTAR: lembretes e checklist do Dashboard fechados pelo `setup`] | Agora, onde fica cada coisa. O menu tem as áreas do sistema. Primeiro, o Dashboard, com o resumo dos números. |
| Clique em "Financeiro": abrem "Caixa", "Histórico do Caixa", "Movimentações Financeiras" (o nome com a Conta Dinheiro ligada), "Relatório Financeiro", "Contas a Pagar/Receber" e "Categorias Financeiras". | No Financeiro ficam o caixa, as contas a pagar e a receber, os bancos e os relatórios. |
| Destaque em "Pedidos". | Em Pedidos, cada compra e cada venda. |
| Destaque em "Fiscal & Ambiental" (sem abrir). | Em Fiscal & Ambiental, as notas fiscais e os documentos ambientais. |
| Clique em "Materiais": abrem "Estoque", "Histórico (Kardex)", "Relatório", "Ticket de Pesagem" e "Produção" (o "Financeiro" fecha sozinho). | Em Materiais, o estoque, o ticket de pesagem e a produção. |
| Destaque em "Coletas & Logística" (sem abrir). | Em Coletas & Logística, as ordens de coleta e a frota. |
| Destaque em "Clientes e Fornecedores", "Funcionários (RH)" e "CRM/Kanban", um por vez, cada um na sua palavra. | Depois, os cadastros em Clientes e Fornecedores, a equipe em Funcionários e as negociações no CRM. |
| Destaque em "Agenda" e, depois do traço, em "Gerencial (Filiais)". | Na Agenda, as tarefas e os avisos. E o Gerencial é pra quem tem matriz e filiais. |
| Destaque no botão "Configurações", no rodapé do menu. | No rodapé ficam as Configurações da empresa. |
| A câmera volta ao menu inteiro. | Algumas dessas áreas são módulos, como as notas fiscais, as coletas e o Gerencial. Elas dependem do plano contratado, e cada uma tem a sua aula. |

### cap07 · Os menus e a sua conta (vinheta: MENU)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), no Dashboard. Clique no cartão "Rafael Nogueira", no rodapé do menu: o menu da conta abre. | Agora, o menu da sua conta. No computador, ele abre clicando no seu nome. |
| Destaque em "Meu Perfil", "Assinatura" e "Tema", um por vez (sem clicar). | No seu perfil, você troca a foto, o nome e a senha. Em Assinatura, acompanha o seu plano. Em Tema, escolhe a tela clara ou escura. |
| Destaque em "Tutoriais \| EcoFlix", "Central de Ajuda" e "Falar com o Suporte", um por vez. | Em Tutoriais EcoFlix, você volta pra trilha. Na Central de Ajuda, procura a resposta por escrito. E em Falar com o Suporte, chama o suporte. |
| Esc fecha o menu; clique em "Configurações" (rodapé) e na aba "Aparência": "Estilo de Navegação (Desktop)". Clique em "Menu Superior": o toast "Estilo de navegação alterado para Menu Superior" e o menu passa para a barra no topo. [BACKEND: `UPDATE profiles SET navigation_style = 'topbar'`; o capítulo seguinte parte de novo com `sidebar`] [TESTAR: janela de 1280 px mostra a barra do topo] | Prefere o menu em cima da tela? Em Configurações, Aparência, é só escolher Menu Superior. Vale pro computador, e dá pra voltar quando quiser. |
| [CELULAR] (no 16:9, a gravação do celular entra no centro do palco): a barra de baixo "Início", "Caixa", "Novo", "Estoque" e "Menu"; toque em "Menu": a gaveta com as mesmas áreas e, no fim, a seção "Conta". | No celular, o menu fica embaixo: Início, Caixa, o botão Novo, pra começar uma compra ou uma venda, Estoque e o Menu, com todas as áreas e a sua conta. |

### cap08 · As palavras do pátio (vinheta: VOCABULÁRIO)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: cliente × fornecedor: o pátio no meio; na frase "vende", uma seta de saída para "Cliente: pra quem você vende", com o caminhão da Aços Quiririm Ltda; na frase "compra", uma seta de entrada de "Fornecedor: de quem você compra", com o catador, o carroceiro e outro depósito (figuras genéricas)] | Antes das telas, umas palavras que aparecem o tempo todo. A mais importante: cliente é pra quem você vende o material. Fornecedor é de quem você compra: o catador, o carroceiro, outro depósito. |
| Capítulo novo (S2): "Configurações" → aba "Usabilidade"; destaque em "Inverter os termos Cliente e Fornecedor" e na frase "Compras, vendas, vínculos, saldos e documentos fiscais continuam com a mesma lógica." (sem ligar). | Uma dica: se no seu pátio se fala ao contrário, dá pra inverter só os nomes, em Configurações, Usabilidade. Por dentro, nada muda: a compra segue com o fornecedor, a venda com o cliente, e as notas fiscais também. |
| [ILUSTRAÇÃO: glossário, um cartão por frase, cada um com o desenho e o exemplo da Recicla Vale. Cartão "Pedido": o recibo "Compra · Dona Cida · Alumínio latinha · 38 kg"] | Pedido é cada compra ou venda, com o material, o peso e o valor. |
| [cartão "Caixa": uma gaveta de dinheiro com "Abre de manhã · fecha no fim do dia"] | Caixa é onde entra e sai o dinheiro do dia. Abre de manhã e fecha no fim do expediente. |
| [cartão "Saldo (fiado)": "Fundição Bandeira do Vale · a receber em parcelas"] | Saldo é o fiado: o que ficou pra depois, a receber de um cliente ou a pagar a um fornecedor. |
| [cartão "Tabela de preço": "Ferro pesado · R$ 0,95 o quilo" e, ao lado, "Tabela Depósitos · outro preço"] | Tabela de preço é o preço do quilo de cada material. Dá pra ter uma tabela só pros depósitos, por exemplo. |
| [cartão "Ficha técnica": latinha solta → fardo de latinha] | Ficha técnica é a receita da produção, como a latinha que vira fardo. |
| [cartão "Ordem de coleta": o caminhão FKD2E41 indo a um parceiro] | Ordem de coleta é quando o caminhão vai buscar material num parceiro. |
| [cartão "MTR": um documento que viaja junto com a carga no caminhão] | E o MTR é o documento ambiental que acompanha o transporte do resíduo. |
| [os sete cartões juntos, em grade] | Cada uma dessas palavras tem a sua aula. Por enquanto, basta saber o que ela quer dizer. |

### cap09 · A sua assinatura (vinheta: ASSINATURA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), no Dashboard. Clique no cartão "Rafael Nogueira" → "Assinatura": a tela "Assinatura" ("Gerencie seu plano, módulos e pagamentos"). [BACKEND: S2: assinatura, módulos e pagamentos do plano ("Mundo")] | Agora, o seu plano. Tudo sobre ele fica em Assinatura, no menu da sua conta. |
| Destaque no alto do cartão: "Recicla Vale Metais Ltda", o selo "Ativa" e "Plano Personalizado • 10 módulos". | No alto, o status da assinatura, aqui Ativa, e o nome do plano, com os módulos que ele tem. |
| [ZOOM: "25 dias restantes" e "Vencimento" 05/12/2026] | Logo abaixo, quantos dias faltam e o vencimento: cinco de dezembro. |
| Destaque em "Valor mensal" e em "Formas de pagamento" ("PIX", "Boleto", "Cartão"), sem zoom no valor. | Embaixo, o valor da mensalidade e as formas de pagamento. |
| [ZOOM: "Uso da conta": "Usuários" 1 / 3 e "Notas fiscais este mês"] | Em Uso da conta, você vê quantos usuários estão cadastrados e quantas notas fiscais saíram no mês. |
| Destaque em "Pagar Agora" e, mais abaixo, em "Gerenciar plano" (sem clicar). | Uma dica: ver esta tela é uma coisa, mexer é outra. Pagar e mudar o plano ficam com o administrador, ou com quem tem a permissão de gerenciar a assinatura. |

### cap10 · Módulos e permissões (vinheta: ASSINATURA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), em "Assinatura"; a câmera desce até "Plano & módulos" ("Plano Personalizado • 10 módulos • Mensal") e para em "Módulos ativos". | Mais abaixo ficam os Módulos ativos. Cada módulo libera uma parte do sistema, como as notas fiscais, as coletas ou o Gerencial. |
| [ILUSTRAÇÃO: dois cartões lado a lado; acende o primeiro, "Módulo fora do plano": uma tela com um cadeado e a frase "o que o módulo faz e como ativar"] | Se uma tela não aparece pra você, são dois motivos. Ou ela é de um módulo que não está no plano: aí, no lugar da função, a tela mostra o que o módulo faz e como ativar. |
| [ILUSTRAÇÃO: acende o segundo cartão, "Usuário sem permissão": o item sai do menu; embaixo, "Quem libera: o administrador, em Usuários e Permissões"] | Ou o seu usuário não tem permissão pra ela. Quem libera é o administrador, em Usuários e Permissões. |
| [ILUSTRAÇÃO: linha do tempo "Período de teste", com todos os módulos acesos, → "Assinatura ativa", com só os contratados acesos; na frase "é só ligar", um módulo apagado acende de novo com a etiqueta "Módulo ligado"] | Uma dica: no teste, todos os módulos ficam liberados. Com a assinatura ativa, ficam os que você contratou. Pra ter de volta uma tela do teste, é só ligar o módulo. |

### cap11 · Quando a empresa cresce (vinheta: ASSINATURA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), em "Assinatura", no cartão "Plano & módulos"; destaque em "Gerenciar plano" (sem abrir). | E quando a empresa cresce, o plano cresce junto. Em Gerenciar plano, você liga um módulo novo ou mais usuários. |
| [ILUSTRAÇÃO: a régua do mês: "Último pagamento 05/11", "Hoje", "Vencimento 05/12"; na frase "só a diferença", o trecho de hoje até o vencimento acende em verde com a etiqueta "Só a diferença, pelos dias que faltam"; sem valores em R$] | Mudou no meio do mês? Antes de confirmar, o sistema mostra o valor. Quando tem cobrança na hora, é só a diferença, pelos dias que faltam até o vencimento. |
| [ILUSTRAÇÃO: na mesma régua, "Pagamento confirmado" e o módulo novo acende] | E o plano novo libera assim que o pagamento confirma. |
| [ILUSTRAÇÃO: uma pessoa com um computador e um celular, os dois ligados ao mesmo usuário; ao lado, o contador "Usuários 3 / 3"] | Uma dica: o limite de usuários é de cadastros, não de gente conectada ao mesmo tempo. O mesmo usuário entra do computador e do celular. |
| [ILUSTRAÇÃO: um cartão com o título do app "Sua equipe cresceu! 🎉", a linha "Nova mensalidade (estimada)" sem valor e o selo "Plano Personalizado"] | Bateu o limite? Ao criar mais um usuário, o sistema abre o aviso Sua equipe cresceu!, mostra a nova mensalidade, e o plano passa a se chamar Personalizado. |

### cap12 · Formas de pagamento (vinheta: ASSINATURA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (S2), em "Assinatura"; destaque em "Formas de pagamento" ("PIX", "Boleto", "Cartão") e no botão "Pagar Agora" (sem clicar). | Pra pagar, é só clicar em Pagar Agora: dá pra pagar com Pix, boleto ou cartão. |
| A câmera desce até a faixa "Débito recorrente ativo no cartão de crédito" ("Sua assinatura será cobrada automaticamente todo mês…"). [BACKEND: `asaas_subscription_id` preenchido e o pagamento de cartão de 05/11 recebido (S2)] | No cartão, a cobrança se repete sozinha todo mês. É assim na Recicla Vale. |
| [ILUSTRAÇÃO: três colunas: "Cartão", um calendário que se marca sozinho mês a mês; "Pix", um mês por vez, até o interruptor "Pix Automático" ligar e os meses passarem a se marcar sozinhos, com a nota "se o banco aceitar"; "Boleto", um mês por vez] | No boleto, você paga cada mês. No Pix também, a não ser com o Pix Automático, que aparece na hora de pagar: ligado, ele repete a cobrança, se o seu banco aceitar. |
| [ILUSTRAÇÃO: a coluna "Boleto" acende] | Uma dica: se o QR Code do Pix demorar a aparecer, o boleto é o caminho mais rápido. |
| De volta à tela: a câmera desce até o cartão "Economize … por ano" ("Mude para o plano anual e pague 12 meses com 20% de desconto (Pix ou Boleto).") e para nele, sem zoom no valor. | Também dá pra passar pro plano anual: os doze meses de uma vez, no Pix ou no boleto, com desconto. A tela mostra quanto você economiza. |
| A câmera desce até "Histórico de Pagamentos" ("4 pagamentos realizados"): os cartões "Renovação • Recicla Vale Metais Ltda", com o selo "Pago", a forma ("Cartão", "PIX", "Boleto") e "Baixar PDF"; o carrossel rola devagar. | No Histórico de Pagamentos fica cada mensalidade paga, com a nota fiscal pra baixar. |
| Destaque em "Baixar PDF" do primeiro cartão (sem clicar). | Uma dica: pra nota da assinatura sair, o cadastro da empresa precisa estar completo, com CNPJ e endereço. |
| A câmera sobe até "Cancelar assinatura", ao lado de "Gerenciar plano" (sem clicar). | E, se um dia cancelar, a cobrança automática para, e o acesso continua até o vencimento. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o portão (cap01) e a trilha com os selos (cap02 e cap03). | Pronto! Recapitulando: a gente firmou os combinados e viu como a trilha funciona, na ordem, com as aulas dos outros módulos liberadas pra conhecer. |
| Montagem rápida: o botão "Tirar dúvidas com o suporte", o menu com o "Financeiro" aberto e o menu da conta. | Viu onde tirar dúvida, passeou pelo menu e pelo menu da sua conta, e aprendeu as palavras do pátio. |
| Montagem rápida: a tela "Assinatura" (o alto, os "Módulos ativos" e o "Histórico de Pagamentos"). | E conheceu a sua assinatura: o plano, os módulos, como crescer e como pagar. |
| Capítulo novo (S13): o portão abre sobre o Dashboard, com o vídeo já visto; clique na caixa "Assisti ao vídeo até o final e entendi os combinados." (liga); [ZOOM: a caixa marcada e o botão "Confirmar e começar a primeira aula"]; no fim da frase, clique no botão. [BACKEND: S13; `acknowledge_ecoflix_intro` grava e a tela segue para a aula do T1] | Agora é só marcar que assistiu e entendeu os combinados, e clicar em Confirmar e começar a primeira aula. |
| Cartão "Próximo: Sua conta e sua empresa"; cartela final. | No próximo tutorial, você deixa o sistema com a cara da sua empresa. Até lá! |
