# Roteiro T21 · Cato, o assistente

Roteiro pronto para a voz e a gravação (molde do T3 da Domiflix; sem etapa de aprovação). Coluna Fala = texto da narração
(voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela = o
que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código (`T21/inventario.md`, versão 1.59.154).
Aula no computador (janela 1280×800), logado como Rafael Nogueira (MASTER), com um corte como Marcos Antunes no
capítulo 2. O painel do Cato abre sempre na tela "Estoque" (`/materiais`), onde as quatro perguntas prontas não são
sorteadas. As respostas do Cato são **simuladas** no backend falso: texto, gráficos, tabela e sugestões estão em
`plano.md` → "Respostas simuladas" (R1 a R9).

- **Título:** Cato, o assistente
- **Antes:** Relatório Financeiro e DRE (T15)
- **Próximo:** Dashboard, Agenda e rotina (T25)
- **Vinhetas (áreas):** CATO · AUTORIZAÇÃO · PERGUNTAS · RESPOSTAS · LIMITES · AJUDA · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~8 min de vídeo (1.028 palavras e 5.439 caracteres de fala, ~6,6 min de voz a 2,6 palavras/s,
  mais 9 vinhetas e as esperas das nove respostas; alvo da fonte: 8 min)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça).
- **Sementes:** `inicio` (Cato liberado, sem autorização; caps. 0 a 2) e `apos-cap02` (autorização gravada; caps. 3 a 9).
  Caps. 3 a 8 são uma conversa só, gravada em sequência; para regravar um deles, o `setup` restaura a conversa pelo
  `sessionStorage`.
- Marcas na coluna Tela: `[BACKEND: ...]`, `[ZOOM: ...]` (a frase inteira), `[ILUSTRAÇÃO: ...]` (desenho no estilo da
  marca, nunca tela do app).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Cato, o assistente". | (sem fala) |
| [ILUSTRAÇÃO: o problema: uma silhueta genérica diante de três cartões de relatório (genéricos, sem tela do app), procurando um número; os cartões saem e ficam dois balões de conversa: a pergunta "Quem tá me devendo?" e a resposta com um valor] | Oi! Neste tutorial a gente vai parar de abrir relatório pra tirar dúvida simples. |
| (a ilustração segue: o balão da resposta acende) | Na Recicla Vale Metais, quando o Rafael quer saber quem está devendo ou quanto tem no pátio, ele pergunta em português, e a resposta vem com o número. |
| Tela "Estoque" do EcoSistema, logado como Rafael Nogueira (semente `inicio`); a câmera vai até o botão redondo do Cato, no canto inferior direito. | Quem responde é o Cato, o assistente de inteligência artificial do EcoSistema. |
| Cartão discreto: "Antes: Relatório Financeiro e DRE". | Se você ainda não viu o tutorial Relatório Financeiro e DRE, dá uma olhada antes. Assim fica fácil conferir os números que o Cato traz. |

### cap01 · Onde o Cato fica (vinheta: CATO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), na tela "Estoque"; zoom suave no botão redondo do Cato; o mouse passa por cima (rótulo "Abrir o Cato"). [BACKEND: `companies.cato_enabled` true e `profiles.cato_invite_seen_at` preenchido, sem o convite do beta] | Com o Cato liberado na conta da empresa, ele fica neste botão redondo, no canto de baixo, em qualquer tela do sistema. |
| [ILUSTRAÇÃO: onde fica: um computador genérico com o botão redondo no canto inferior direito e um celular genérico com o botão no canto inferior esquerdo, acima da barra de baixo; cada um acende com a sua parte da frase] | No computador, ele fica à direita. No celular, à esquerda, logo acima da barra de baixo. |
| Clique no botão: em vez do chat, abre a janela "Antes da primeira conversa com o Cato". [BACKEND: `companies.ai_consent_at` vazio] | Pra abrir, é só clicar. Na primeira vez, antes da conversa, aparece a autorização. |

### cap02 · Autorizar o Cato (vinheta: AUTORIZAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`; o `setup` clica no botão do Cato fora do vídeo): janela "Antes da primeira conversa com o Cato", "Leia rapidinho como ele trata os dados da sua empresa."; a câmera desce pelos pontos. | Essa janela explica, em poucas linhas, como o Cato trata os dados da empresa. |
| [ILUSTRAÇÃO: o caminho da pergunta: o balão "Quem tá me devendo?" vai até o Cato; o Cato lê os dados da empresa (compras, vendas, estoque, saldos e contas); um trecho passa por um "serviço de inteligência artificial" com um cadeado e o aviso "não treina com os seus dados"; a resposta volta ao balão] | Pra responder, ele lê os dados da sua conta: compras, vendas, estoque, saldos e contas. Esses trechos passam por serviços de inteligência artificial contratados pela EcoSistema, que não usam os seus dados pra treinar os modelos deles. |
| De volta à janela; zoom nos pontos do microfone e de "Ouvir a resposta". | O microfone e a leitura em voz alta só ligam quando você toca no botão. |
| Zoom em "O Cato pode errar. Use como apoio e confira os números antes de decidir.". | E o Cato pode errar. Use como apoio e confira os números antes de decidir. |
| Corte: logado como Marcos Antunes (semente `inicio`), o mesmo clique no botão do Cato: a janela com o mesmo resumo, sem o botão de autorizar, com "Só o administrador da empresa pode autorizar o Cato. Peça pra ele abrir o Cato e concluir a autorização." e "Entendi"; zoom no aviso. [BACKEND: Marcos com a permissão `action_use_cato`, não administrador] | Uma dica: só o administrador da empresa autoriza. Pra quem não é, a janela mostra este aviso, e a saída é pedir pro administrador abrir o Cato e concluir. |
| De volta ao Rafael (semente `inicio`, janela aberta): clique em "Entendi e autorizo": aviso "Cato autorizado" e o painel do Cato abre à direita. [BACKEND: RPC `accept_ai_terms` grava `ai_consent_at` e `ai_consent_version` '2.0'; vira `apos-cap02`] | O Rafael é o administrador, então ele clica em Entendi e autorizo. Pronto: o Cato está autorizado pra empresa toda. |

### cap03 · As perguntas prontas (vinheta: PERGUNTAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`), na tela "Estoque"; clique no botão do Cato: o painel abre à direita com "Oi, Rafael 👋", "Pergunte o que quiser sobre seu negócio" e as perguntas prontas "Como tá indo meu negócio esse mês?", "Como tá meu caixa hoje?", "Quanto tenho em estoque agora?" e "Qual material me deu mais faturamento?". [BACKEND: RPC `cato_memory_manage('status')`] | Com o Cato autorizado, o painel abre aqui do lado, com quatro perguntas prontas pra quebrar o gelo. |
| A câmera passa pelo campo "Pergunte ao Cato…" e pelo botão "Enviar". | Dá pra clicar numa delas ou escrever a sua pergunta aqui embaixo, do jeito que você fala. |
| Clique em "Como tá indo meu negócio esse mês?": o balão da pergunta à direita; o brilho com "Pensando…" e "Buscando seus dados…". [BACKEND: edge `cato-background` devolve o `jobId`; `cato_jobs` vira `completed` ~3 s depois com R1] | Vou clicar na primeira: como tá indo meu negócio esse mês. |
| A resposta aparece digitando: "Consultei seu resumo financeiro", a linha do período ("Regime de caixa", "Atualizado às ..."), "Vendas", "Compras", "Despesas" e o resultado em negrito. [ZOOM: "Vendas" R$ 118.620,20 e o resultado R$ 67.604,65] | Em poucos segundos ele responde: até hoje, dia dez, a empresa vendeu uns cento e dezoito mil e seiscentos reais, e o resultado do mês está em uns sessenta e sete mil e seiscentos. |
| A câmera desce para as três pílulas acima do campo: "Compara com outubro", "Quais despesas tive esse mês?" e "Qual material mais vendi?". [BACKEND: edge `cato-assist` com `mode: "followups"` devolve as sugestões de R1] | Embaixo, ele já sugere as próximas perguntas. É só clicar, se quiser seguir por ali. |

### cap04 · O que ele responde bem (vinheta: PERGUNTAS)

| Tela | Fala |
| --- | --- |
| A mesma conversa; no campo "Pergunte ao Cato…" digita "Quem tá me devendo?" e clica em "Enviar". [BACKEND: R2] | Agora, as perguntas do dia a dia. Primeiro: quem tá me devendo. |
| A resposta: "Consultei os saldos dos parceiros", a lista dos três parceiros e o gráfico de barras "Saldo a receber por parceiro". [ZOOM: o total R$ 17.540,00 e a linha "Fundição Bandeira do Vale: R$ 14.370,00"] | São três parceiros, que somam dezessete mil, quinhentos e quarenta reais. A Fundição Bandeira do Vale é a maior: catorze mil, trezentos e setenta. |
| Digita "Quanto tenho em estoque agora?" e envia: "Consultei seu estoque", o peso total, o valor a custo médio, a projeção e os três materiais de maior valor. [BACKEND: R3] | No estoque, ele traz o peso, o valor pelo custo médio, uns noventa e seis mil reais, e os materiais que mais pesam no valor, com o alumínio perfil na frente. |
| Digita "Qual o saldo das minhas contas no banco?" e envia: "Consultei seu resumo bancário", as três contas e o total. [BACKEND: R4] | No banco, ele separa o saldo de agora, uns cento e trinta e dois mil reais nas três contas, do que entrou e saiu no mês. |
| Digita "Como tá meu caixa hoje?" e envia: "Consultei seu caixa" e a resposta: nenhum caixa aberto hoje, e os dois caixas de ontem. [BACKEND: R5] | E o caixa: hoje ainda não tem nenhum aberto, e ele conta como fecharam os de ontem. |
| [ILUSTRAÇÃO: caixa é o de hoje: à esquerda, uma gaveta de caixa com a etiqueta "hoje"; à direita, um calendário com "o mês"; a pergunta "como tá meu caixa?" liga na gaveta e "compras e vendas dos últimos três meses" liga no calendário] | Uma dica: pro Cato, caixa é o caixa de hoje. Pra saber do mês, pergunte pelo mês. |

### cap05 · Gráfico ou tabela (vinheta: RESPOSTAS)

| Tela | Fala |
| --- | --- |
| A mesma conversa; digita "Compras e vendas dos últimos três meses" e envia: "Consultei suas compras e vendas", os três meses e o gráfico de linha "Compras e vendas por mês". [BACKEND: R6] | Pro mês, a pergunta é do mês: compras e vendas dos últimos três meses. Aqui a resposta vem com uma linha, mês a mês. |
| A câmera no gráfico de linha (as linhas "Compras" e "Vendas"). | Em outubro, as compras quase alcançaram as vendas, com o pátio cheio de ferro. Em novembro, o ferro saiu, e as vendas passaram longe das compras. |
| Digita "Pra quem eu mais vendi em outubro?" e envia: a lista dos três clientes e o gráfico de barras "Vendas por cliente em outubro". [BACKEND: R7] [ZOOM: "Fundição Bandeira do Vale: R$ 112.800,00"] | Agora, pra quem eu mais vendi em outubro. A Fundição vem na frente, com cento e doze mil e oitocentos reais. |
| [ILUSTRAÇÃO: saldo × valor movimentado: a ficha da Fundição Bandeira do Vale com duas caixas: "vendido em outubro: R$ 112.800" (várias setas de venda ao longo do mês) e "deve hoje: R$ 14.370" (o que ficou em aberto)] | Uma dica: isso é o valor vendido no mês, não é o que ela deve. O saldo em aberto da Fundição, que apareceu lá em cima, é de catorze mil, trezentos e setenta. |
| (a ilustração segue: embaixo de cada caixa entra a pergunta: "quanto ela me deve?" e "pra quem eu mais vendi?") | Quanto alguém te deve é o saldo. De quem você mais comprou, ou pra quem mais vendeu, é o valor movimentado no período. São duas perguntas diferentes. |
| Digita "Lista meu estoque em tabela" e envia: "Consultei seu estoque", o texto curto e a tabela "Estoque em 10/11/2026" ("Material", "Quantidade (kg)", "Valor em estoque"). [BACKEND: R8] | E quando você pede uma lista, ele monta uma tabela, com o material, a quantidade e o valor. |
| [ILUSTRAÇÃO: a regra: quatro cartões pequenos que acendem com a frase: pizza ("distribuição"), barras ("ranking"), linha ("ao longo do tempo") e tabela ("lista"); embaixo, "o texto vem sempre antes"] | A regra é simples: distribuição vira pizza, ranking vira barra, o que muda no tempo vira linha, e lista vira tabela. E o texto vem sempre antes. |

### cap06 · De onde vêm os números (vinheta: RESPOSTAS)

| Tela | Fala |
| --- | --- |
| A mesma conversa, na resposta da tabela. [ZOOM: "Consultei seu estoque" e a linha do período com "Atualizado às ..."] | Repara no que vem em cima de cada resposta: de onde ele tirou os dados, o período e a hora da consulta. |
| A câmera desce pela tabela até o botão "Abrir posição de estoque". | Os números são lidos direto dos seus dados, os mesmos das telas do sistema. E o botão embaixo leva pra tela de onde o número veio. |
| Clique em "Abrir posição de estoque": atrás do painel abre a "Posição de Estoque"; clique em "Fechar" no painel; a câmera desce até a linha "Total geral". [BACKEND: RPC `get_stock_balance_at_date` com o estoque de `plano.md` → "Mundo"] [ZOOM: "Total geral" com "Valor" R$ 96.076,00] | Na Posição de Estoque, o total geral dá os mesmos noventa e seis mil e setenta e seis reais. |
| [ILUSTRAÇÃO: o mesmo dado: no centro, "os dados da empresa"; uma seta vai para um cartão "tela do sistema" e outra para um balão "resposta do Cato", e os dois mostram "R$ 96.076,00"] | É o mesmo número, porque os dois leem os mesmos dados. |
| Clique no botão do Cato: o painel volta com a conversa; a câmera desce até o rodapé "O Cato.ai pode cometer erros. Confira informações importantes.". | Mesmo assim, ele avisa aqui embaixo que pode cometer erros. Quando o número for pra uma decisão, confira na tela, por aquele botão. |

### cap07 · Os limites do Cato (vinheta: LIMITES)

| Tela | Fala |
| --- | --- |
| A mesma conversa; digita "Emite a nota da venda pra Fundição Bandeira do Vale" e envia. [BACKEND: R9] | E o que ele não faz? Vou pedir pra ele emitir uma nota. |
| A resposta: "Consultei a central de ajuda", "Emitir nota fica com você: eu consulto e explico, mas não emito." e os três passos. | Ele explica que emitir nota fica com você e mostra o caminho no sistema, passo a passo. |
| [ILUSTRAÇÃO: consulta × executa: duas colunas: "o Cato" (lupa: consultar, explicar, montar gráfico e tabela) e "você, nas telas do sistema" (nota fiscal, pagamento de conta, cadastro); cada item acende com a frase] | O Cato consulta e responde. Emitir nota, pagar conta e cadastrar seguem com você, nas telas do sistema. |
| [ILUSTRAÇÃO: limites de uso: um relógio com "por minuto" e um calendário com "por dia"; um balão "espera um minutinho" e uma seta de volta ao chat] | Uma dica: o Cato tem um limite de perguntas por minuto e por dia. É um limite que protege o custo do serviço, não é castigo. Se ele pedir pra você esperar um minutinho, a espera resolve. |

### cap08 · Avaliar e falar com o suporte (vinheta: AJUDA)

| Tela | Fala |
| --- | --- |
| A mesma conversa; na resposta da tabela (R8), clique em "Resposta útil" (👍): o botão fica marcado. [BACKEND: RPC `set_cato_feedback`] | Em cada resposta, tem o joinha e o dedo pra baixo. Ajudou, é só clicar no joinha. |
| Na resposta da nota (R9), clique em "Resposta não útil" (👎): aparecem "Número errado", "Não entendeu", "Faltou detalhe", "Resposta lenta" e "Outro"; clique em "Faltou detalhe". | Se não ajudou, o dedo pra baixo abre os motivos, num clique. Esse retorno ajuda o time da EcoSistema a melhorar o Cato. |
| No rodapé do painel, clique em "Falar com atendente": janela "Falar com o suporte" ("Nos conte o que está acontecendo pra resolvermos mais rápido."). | E quando você precisar de uma pessoa de verdade, o caminho fica aqui embaixo: Falar com atendente. |
| A câmera passa por "Ver vídeos", "Ver artigos", "Em qual tela/módulo? *", "O que aconteceu? Descreva com detalhes *" e "Você já assistiu aos nossos tutoriais sobre isso? *", e para em "Falar no WhatsApp", sem clicar; fecha a janela. | Você conta em qual tela estava e o que aconteceu, e o botão Falar no WhatsApp abre a conversa com o suporte, com tudo já escrito. |

### cap09 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a janela de autorização e o aviso "Cato autorizado". | Pronto! Recapitulando: a gente achou o Cato no canto da tela e autorizou o uso, que só o administrador faz. |
| Montagem rápida: as respostas do mês, dos saldos, do estoque, do banco e do caixa. | Fez as perguntas do dia a dia: o resultado do mês, quem está devendo, o estoque, o banco e o caixa, que é sempre o de hoje. |
| Montagem rápida: o gráfico de linha, o de barras, a tabela e o "Total geral" da Posição de Estoque. | Viu quando vem gráfico e quando vem tabela, e conferiu um número na tela de onde ele veio. |
| Montagem rápida: a resposta da nota, o joinha e a janela "Falar com o suporte". | Entendeu que o Cato consulta e você executa, e achou o caminho pro atendente. |
| Cartão "Próximo: Dashboard, Agenda e rotina"; cartela final. | No próximo tutorial, a gente olha a tela inicial e a rotina que mantém o sistema vivo. Até lá! |
