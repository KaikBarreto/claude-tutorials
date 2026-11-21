# Roteiro T21 · Cato, o assistente

Roteiro para o ensaio gravado e, depois da revisão geral, para a voz (voz Kaik Barreto, ElevenLabs eleven_v4). Coluna Fala =
texto da narração (uma linha da tabela = uma linha da fala); números por extenso como se fala, e a legenda volta à grafia da
tela pelo `numeros` do `narracao/config_narracao.json`; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna
Tela = o que o robô faz, **o que o Cato responde** (texto entre aspas; "(código)" = texto copiado do código 1.60.22, "(simulada)"
= redigida por nós no formato real) e onde a câmera foca, com os rótulos como no código (`T21/inventario.md`, `T21/plano.md` →
"O que o Cato responde": a fonte de cada resposta, arquivo:linha). Computador, 1600×900, logado como Rafael Nogueira (MASTER),
com um corte como Marcos Antunes no cap. 2 e no cap. 15.
Marcas: `[BACKEND: ...]` (o backend falso ainda não tem), `[ZOOM: ...]` (dura a frase inteira), `[ILUSTRAÇÃO: ...]` (cena desenhada,
nunca tela inventada), `[TESTAR]` (o robô confere antes de gravar).

- **Título:** Cato, o assistente (o catálogo não muda; o painel diz "Agente de IA da EcoSistema", e a fala diz "agente de inteligência artificial")
- **Antes:** Relatório Financeiro e DRE (T15). **Próximo:** Dashboard, Agenda e rotina (T25)
- **Vinhetas (áreas):** CATO · AUTORIZAÇÃO · MEMÓRIA · PERGUNTAS ×2 · RESPOSTAS · AÇÕES ×3 · FINANCEIRO ×2 · ARQUIVOS · FISCAL · ROTINA · LIMITES · AJUDA · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~24 min de vídeo (2.630 palavras e 14.065 caracteres de fala, ~16,9 min de voz a 2,6 palavras/s, mais 17 vinhetas, as esperas das respostas e os cliques dos cartões); era ~8 min
- **Revisão 21/11 (app 1.60.22):** de 10 para 18 capítulos (00 a 17). O Cato deixou de só consultar: prepara 18 tipos de ação com cartão de confirmação. Novos: cap03 (memória), cap07 a cap15 (ações, arquivos, NF-e, pedidos e rotinas, limites); caps. 5 e 6 antigos viram o cap06; o cap07 antigo ("só consulta") foi descartado e substituído pelo cap15. **Não entrou:** "Ver itens e tributos" (componente que o 1.60.22 não renderiza em lugar nenhum), ambiente da nota (Homologação/Produção), formulário por pedido ("modo manual"), abas internas (Analytics, Operações, Aprendizado, Efetividade), conversão e ordem de produção demonstradas (só uma frase), valores de plano.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça).
- **Sementes:** `inicio` (Cato liberado, sem autorização, memória `pending`; caps. 0 a 2), `apos-cap02` (autorização gravada; cap. 3 em diante). Caps. 4 a 6 são uma conversa; caps. 7 a 14 são outra ("Nova"), para o "Total geral" do cap. 6 bater antes de qualquer lançamento; cap. 15 em diante, mesma conversa mais o corte do Marcos. Detalhe em `plano.md`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Cato, o assistente". | (sem fala) |
| [ILUSTRAÇÃO: dois balões: "Quem tá me devendo?" recebe um valor; "Lança uma compra de 120 kg de latinha" recebe um cartão com um botão de confirmar] | Oi! Neste tutorial a gente conhece o Cato, o agente de inteligência artificial do EcoSistema. |
| (a ilustração segue: o balão da pergunta acende, depois o do cartão) | Ele faz duas coisas. Responde perguntas sobre o seu negócio, com o número na hora. E prepara tarefas pra você: uma compra, uma baixa de conta, até uma nota fiscal. |
| Tela "Estoque" (semente `inicio`), Rafael Nogueira; a câmera vai ao botão redondo do Cato, no canto inferior direito. | Na Recicla Vale Metais, o Rafael pede em português, confere o resumo e confirma. Nada é lançado só por conversar. |
| Cartão discreto: "Antes: Relatório Financeiro e DRE". | Se você ainda não viu os tutoriais de compra e venda, de contas e de notas fiscais, vale ver antes. Aqui a gente faz as mesmas tarefas, só que pela conversa. |

### cap01 · Onde o Cato fica (vinheta: CATO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`), tela "Estoque"; zoom suave no botão redondo (rótulo "Abrir o Cato"). [BACKEND: `companies.cato_enabled` true, `profiles.cato_invite_seen_at` preenchido] | Com o Cato liberado na conta da empresa, ele fica neste botão redondo, no canto de baixo, em qualquer tela do sistema. |
| [ILUSTRAÇÃO: computador × celular: o botão no canto inferior direito do computador e no inferior esquerdo do celular, acima da barra de baixo] | No computador, ele fica à direita. No celular, à esquerda, logo acima da barra de baixo. |
| O balão de dica ao lado do botão, com "Abrir Cato" e o xis "Fechar dica do Cato"; a câmera fecha no xis (sem clicar). [BACKEND: sem a chave `cato_adoption_nudge_<empresa>_<usuário>` no armazenamento local; a bolinha de notificação no botão] [TESTAR: se o balão não aparecer a tempo, esta linha sai] | De vez em quando ele mostra uma dica do que pode fazer. É só clicar pra abrir, ou fechar a dica no xis. |
| "Usuários e Permissões", edição do Marcos, linha "Usar o Cato (assistente de IA)" com a descrição. [ZOOM na descrição: "o Cato responde sobre dados gerais da empresa … mesmo de telas que este usuário não pode abrir"] | Quem usa o Cato é quem tem esta permissão, em Usuários e Permissões. Uma dica: o Cato responde sobre os dados gerais da empresa, até de telas que a pessoa não abre. Libere pra quem pode ver esses números. |
| Volta ao Rafael; clique no botão: em vez do chat, abre "Antes da primeira conversa com o Cato". [BACKEND: `companies.ai_consent_at` vazio] | Pra abrir, é só clicar. Na primeira vez, antes da conversa, aparece a autorização. |

### cap02 · Autorizar o Cato (vinheta: AUTORIZAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`inicio`; o `setup` clica no botão fora do vídeo): janela "Antes da primeira conversa com o Cato", "Leia rapidinho como ele trata os dados da sua empresa."; a câmera desce pelos pontos. | Essa janela explica, em poucas linhas, como o Cato trata os dados da empresa. |
| [ILUSTRAÇÃO: o caminho da pergunta: o balão "Quem tá me devendo?" vai ao Cato; o Cato lê os dados da empresa (compras, vendas, estoque, saldos e contas); um trecho passa por um "serviço de inteligência artificial" com um cadeado e "não treina com os seus dados"; a resposta volta ao balão] | Pra responder, ele lê os dados da sua conta: compras, vendas, estoque, saldos e contas. Esses trechos passam por serviços de inteligência artificial contratados pela EcoSistema, que não usam os seus dados pra treinar os modelos deles. |
| De volta à janela; zoom nos pontos do microfone e de "Ouvir a resposta". | O microfone e a leitura em voz alta só ligam quando você toca no botão. |
| Zoom em "O Cato pode errar. Use como apoio e confira os números antes de decidir.". | E o Cato pode errar. Use como apoio e confira os números antes de decidir. |
| Corte: Marcos Antunes (`inicio`), o mesmo clique: a janela sem o botão de autorizar, com "Só o administrador da empresa pode autorizar o Cato. Peça pra ele abrir o Cato e concluir a autorização." e "Entendi"; zoom no aviso. [BACKEND: Marcos com `action_use_cato`, não administrador] | Uma dica: só o administrador da empresa autoriza. Pra quem não é, a janela mostra este aviso, e a saída é pedir pro administrador abrir o Cato e concluir. |
| Volta ao Rafael (`inicio`, janela aberta): clique em "Entendi e autorizo": aviso "Cato autorizado". [BACKEND: RPC `accept_ai_terms`; vira `apos-cap02`] | O Rafael é o administrador, então ele clica em Entendi e autorizo. Pronto: o Cato está autorizado pra empresa toda. |

### cap03 · A memória do Cato (vinheta: MEMÓRIA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (`apos-cap02`), tela "Estoque"; clique no botão: o painel abre e, por cima, "Quer que o Cato lembre de você?" com "Agora não" e "Usar memória". [BACKEND: `cato_memory_manage('status')` com `personalDecision: "pending"`] | Logo que o Cato é autorizado, ele pergunta se pode lembrar de você. |
| [ZOOM: "Ele guarda apenas preferências declaradas e assuntos recentes. Saldos, preços e quantidades são sempre consultados novamente no sistema."] | Com a memória ligada, ele guarda as preferências que você disser e os assuntos recentes, pra continuar de onde parou. Número ele não decora: saldo, preço e quantidade ele consulta de novo, toda vez. |
| [ZOOM: "A memória é pessoal dentro desta empresa. Ela não é compartilhada com outros usuários e não guarda senhas, documentos ou autorizações."] | A memória é só sua, dentro da empresa. Outro usuário não vê, e ela não guarda senha nem documento. |
| Clique em "Usar memória" (o aviso "Memória do Cato ativada" se a tela mostrar). [BACKEND: `cato_memory_manage` ação `accept_personal_consent`] | O Rafael clica em Usar memória. Se preferir, é só clicar em Agora não e ligar depois. |
| Painel aberto; rodapé, botão "Memória": "Memória do Cato", aba "Minha memória", chave "Lembrar entre conversas"; "Adicionar nota": digita "Prefiro os valores em tabela, do maior para o menor." e "Salvar nota"; a nota na lista com lápis e lixeira; o botão "Apagar toda a minha memória" aparece (sem clicar). [BACKEND: `cato_memory_manage` `list`, `save`] | Tudo que ele guardou fica no botão Memória, embaixo do painel. Dá pra escrever uma nota, corrigir, apagar uma por uma ou apagar tudo. |
| [ZOOM: "Notas e preferências expiram em 90 dias; assuntos recentes, em 30 dias. Valores, saldos e preços são consultados novamente. Pausar não apaga o que foi salvo."] | As notas valem por noventa dias, e os assuntos recentes, por trinta. Desligar a chave só pausa: o que já estava salvo continua lá. |
| Aba "Da empresa": "Usar notas da empresa" e "Apenas usuários com acesso total podem publicar ou alterar notas da empresa."; fecha a janela. | E tem a aba Da empresa, com as notas que valem pra todo mundo que usa o Cato. Só quem tem acesso total escreve ali. |

### cap04 · Conhecendo o painel (vinheta: PERGUNTAS)

| Tela | Fala |
| --- | --- |
| Painel com "Oi, Rafael 👋", "Pergunte o que quiser sobre seu negócio" e "Sugestões para começar": "Como tá indo meu negócio esse mês?", "Como tá meu caixa hoje?", "Quanto tenho em estoque agora?", "Qual material me deu mais faturamento?". | Com a memória resolvida, o painel do Cato abre aqui do lado, com quatro perguntas prontas pra quebrar o gelo. |
| Campo "Pergunte ao Cato…": a câmera passa pelo clipe "Anexar foto, arquivo ou planilha", pelo microfone "Falar" e por "Enviar". | Aqui embaixo você escreve do jeito que fala. O clipe anexa foto ou arquivo, e o microfone escreve o que você disser, pra você conferir antes de enviar. |
| Barra embaixo do campo: "Conversas", "Nova", "Memória"; clique em "Conversas": "Suas conversas", "Retome uma análise de onde parou."; fecha. [BACKEND: `get_my_cato_conversations` com 1 conversa] | Debaixo do campo ficam as suas conversas antigas, o botão pra começar uma nova e a memória. |
| "Mais opções do Cato" (três pontinhos): o menu com "Notificações", "Ler respostas automaticamente", "Acompanhar pedidos", "Suas rotinas", "Respostas revisadas", "Falar com atendente", "Sobre o Cato"; a câmera passa pelos itens; fecha. | E nos três pontinhos ficam o som, a leitura das respostas em voz alta, os pedidos, as rotinas e o atendente. A gente volta neles já já. |
| Clique em "Como tá indo meu negócio esse mês?": o balão da pergunta; "Pensando…" e "Buscando seus dados…". [BACKEND: edge `cato-background` devolve o `jobId`; `cato_jobs` vira `completed` ~3 s depois com R1] | Vou clicar na primeira pergunta: como tá indo meu negócio esse mês. |
| Resposta R1 (simulada): "Consultei seu resumo financeiro", linha do período, "Vendas", "Compras", "Despesas" e o resultado. [ZOOM: "Vendas" R$ 118.620,20 e o resultado] | Em poucos segundos ele responde: até hoje, dia dez, a empresa vendeu uns cento e dezoito mil e seiscentos reais, e o resultado do mês está em uns sessenta e dois mil e quinhentos. |
| A câmera desce às três pílulas acima do campo ("Sugestões de perguntas"): "Compara com outubro", "Quais despesas tive esse mês?", "Qual material mais vendi?". [BACKEND: `cato-assist` `mode: "followups"`] | Embaixo, ele já sugere as próximas perguntas. É só clicar, se quiser seguir por ali. |

### cap05 · O que ele responde bem (vinheta: PERGUNTAS)

| Tela | Fala |
| --- | --- |
| A mesma conversa; digita "Quem tá me devendo?" e envia. Resposta R2 (simulada): "Consultei os saldos dos parceiros" e a lista dos três parceiros. [BACKEND: R2] | Agora, as perguntas do dia a dia. Primeiro: quem tá me devendo. |
| O gráfico de barras "Saldo a receber por parceiro". [ZOOM: total R$ 17.540,00 e "Fundição Bandeira do Vale: R$ 14.370,00"] | São três parceiros, que somam dezessete mil, quinhentos e quarenta reais. A Fundição Bandeira do Vale é a maior: catorze mil, trezentos e setenta. |
| Digita "Quanto tenho em estoque agora?": R3 (simulada), "Consultei seu estoque", peso, valor a custo médio, projeção e os três materiais de maior valor. | No estoque, ele traz o peso, o valor pelo custo médio, uns noventa e seis mil reais, e os materiais que mais pesam no valor, com o alumínio perfil na frente. |
| Digita "Qual o saldo das minhas contas no banco?": R4 (simulada), "Consultei seu resumo bancário", as três contas e o total. | No banco, ele separa o saldo de agora, uns cento e vinte e cinco mil reais nas três contas, do que entrou e saiu no mês. |
| Digita "Como tá meu caixa hoje?": R5 (simulada), "Consultei seu caixa": nenhum caixa aberto hoje e os dois de ontem. | E o caixa: hoje ainda não tem nenhum aberto, e ele conta como fecharam os de ontem. |
| [ILUSTRAÇÃO: caixa é o de hoje: à esquerda, uma gaveta de caixa com a etiqueta "hoje"; à direita, um calendário com "o mês"; "como tá meu caixa?" liga na gaveta e "compras e vendas dos últimos três meses" no calendário] | Uma dica: pro Cato, caixa é o caixa de hoje. Pra saber do mês, pergunte pelo mês. |

### cap06 · Gráfico, tabela e de onde vêm os números (vinheta: RESPOSTAS)

| Tela | Fala |
| --- | --- |
| A mesma conversa; digita "Compras e vendas dos últimos três meses": R6 (simulada), "Consultei suas compras e vendas" e o gráfico de linha "Compras e vendas por mês". | Pro mês, a pergunta é do mês: compras e vendas dos últimos três meses. Aqui a resposta vem com uma linha, mês a mês. |
| A câmera no gráfico (as linhas "Compras" e "Vendas"). | Em outubro, as compras quase alcançaram as vendas, com o pátio cheio de ferro. Em novembro, o ferro saiu, e as vendas passaram longe das compras. |
| Digita "Pra quem eu mais vendi em outubro?": R7 (simulada), a lista e o gráfico "Vendas por cliente em outubro". [ZOOM: "Fundição Bandeira do Vale: R$ 112.800,00"] | Agora, pra quem eu mais vendi em outubro. A Fundição vem na frente, com cento e doze mil e oitocentos reais. |
| [ILUSTRAÇÃO: saldo × valor movimentado: a ficha da Fundição com "vendido em outubro: R$ 112.800" e "deve hoje: R$ 14.370"] | Uma dica: isso é o valor vendido no mês, não é o que ela deve. O saldo em aberto da Fundição, que apareceu lá em cima, é de catorze mil, trezentos e setenta. |
| (a ilustração segue: embaixo de cada caixa entra a pergunta "quanto ela me deve?" e "pra quem eu mais vendi?") | Quanto alguém te deve é o saldo. De quem você mais comprou, ou pra quem mais vendeu, é o valor movimentado no período. São duas perguntas diferentes. |
| Digita "Lista meu estoque em tabela": R8 (simulada), "Consultei seu estoque", o texto curto e a tabela "Estoque em 10/11/2026" (Material, Quantidade (kg), Valor em estoque). | E quando você pede uma lista, ele monta uma tabela, com o material, a quantidade e o valor. |
| [ILUSTRAÇÃO: a regra: quatro cartões que acendem com a frase: pizza ("distribuição"), barras ("ranking"), linha ("ao longo do tempo"), tabela ("lista"); embaixo, "o texto vem sempre antes"] | A regra é simples: distribuição vira pizza, ranking vira barra, o que muda no tempo vira linha, e lista vira tabela. E o texto vem sempre antes. |
| Na resposta da tabela. [ZOOM: "Consultei seu estoque" e a linha do período com "Atualizado às ..."] | Repara no que vem em cima de cada resposta: de onde ele tirou os dados, o período e a hora da consulta. Os números são lidos direto dos seus dados, os mesmos das telas do sistema, e o botão embaixo leva pra tela de onde o número veio. |
| Clique em "Abrir posição de estoque": atrás do painel abre a "Posição de Estoque"; volta ao painel e fecha; a câmera desce à linha "Total geral". [BACKEND: RPC `get_stock_balance_at_date`] [ZOOM: "Valor" R$ 96.076,00] | Na Posição de Estoque, o total geral dá os mesmos noventa e seis mil e setenta e seis reais. É o mesmo número, porque os dois leem os mesmos dados. |
| Clique no botão do Cato: o painel volta com a conversa; a câmera desce ao rodapé "O Cato.ai pode cometer erros. Confira informações importantes.". | Mesmo assim, ele avisa aqui embaixo que pode cometer erros. Quando o número for pra uma decisão, confira na tela, por aquele botão. |

### cap07 · Lançar uma compra pela conversa (vinheta: AÇÕES)

| Tela | Fala |
| --- | --- |
| Clique em "Nova" (conversa limpa); digita "Lança uma compra de 120 kg de alumínio latinha da Aparecida Ramos, a 6,20" e envia. | Agora, a parte nova: pedir pro Cato fazer. Vou pedir uma compra de cento e vinte quilos de alumínio latinha da Aparecida Ramos, a seis reais e vinte centavos o quilo. |
| Resposta A1a (código): "Como esta compra será paga: dinheiro, Pix/transferência ou saldo com o fornecedor?" e "Nenhuma compra foi lançada."; digita "Pix, pela Conta Principal". [BACKEND: A1a] | Faltou dizer como foi pago, então ele pergunta. Uma coisa de cada vez, e eu respondo curtinho: Pix, pela Conta Principal. |
| O cartão A1b: "Entrada de material", "Fornecedor: Aparecida Ramos", "Alumínio latinha", "120 kg", "R$ 744,00", "R$ 6,20/kg", "Preços informados nesta conversa", "Total da compra R$ 744,00", "Forma de pagamento Pix", "Conta Conta Principal". [ZOOM no cartão inteiro] [BACKEND: A1b] | Com tudo na mão, ele monta este cartão. Fornecedor, material, quantidade, preço, total e a forma de pagamento. É o resumo pra você conferir. |
| [ZOOM: "Estoque entra e o financeiro registra R$ 744,00."] | Repara nesta linha: até aqui, nada mudou. O estoque só entra e o financeiro só registra quando você confirma. |
| [ILUSTRAÇÃO: a regra do cartão: "você pede", "o Cato pergunta e monta o resumo", "você confirma no botão"; um balão "sim" riscado ao lado] | Uma dica: escrever sim na conversa não confirma nada. Quem lança é o botão do cartão, e é você quem clica. |
| Cursor em "Corrigir dados" (clica: o pedido volta escrito no campo; apaga o campo) e em "Agora não" (sem clicar). [TESTAR: o campo recebe o pedido de volta] | Errou alguma coisa? Corrigir dados devolve o pedido pro campo, pra você mudar só o que precisa. E Agora não desiste, sem lançar. |
| Clique em "Lançar compra": o cartão vira "Compra lançada." (verde) com "Abrir comprovante". [BACKEND: RPC `cato_confirm_purchase_action` grava a compra de verdade, por `criarPedido`] | Conferi, está certo: Lançar compra. Pronto, a compra entrou, e o comprovante abre aqui. |
| Embaixo, "Próximos passos" abre: "Pedido registrado", o pagamento e "Preparar NF-e". [BACKEND: RPC `cato_order_journeys`] | Embaixo, ele ainda mostra os próximos passos desse pedido. |
| [ILUSTRAÇÃO: um relógio de dez minutos ao lado de um cartão; o cartão apaga e aparece "A proposta expirou ou algum cadastro mudou. Peça ao Cato para montar novamente."] | Uma dica: o cartão vale por dez minutos. Passou disso, ou mudou algum cadastro no meio, ele expira, e é só pedir de novo. |

### cap08 · Venda, ticket e preços (vinheta: AÇÕES)

| Tela | Fala |
| --- | --- |
| Digita "Lança uma venda de 500 kg de alumínio perfil pra Serra Fina, a 10,40, no saldo, vencimento 10/12" e envia: o cartão A2 "Saída de material", "Total da venda R$ 5.200,00", "Forma de pagamento Saldo", "Vencimento 10/12/2026", "Estoque sai e o financeiro registra R$ 5.200,00.". [BACKEND: A2] | A venda é igual. Desta vez eu já digo tudo de uma vez: cliente, material, quantidade, preço e pagamento. Quinhentos quilos de alumínio perfil pra Serra Fina, a dez reais e quarenta centavos, no saldo, com vencimento dia dez de dezembro. |
| (o cartão fica na tela; a câmera passa pelos campos) | Ele não pergunta nada e já traz o cartão da venda. |
| Clique em "Lançar venda": "Venda lançada." e "Abrir comprovante"; "Próximos passos" mostra "A receber: R$ 5.200,00" e "Preparar NF-e". [BACKEND: RPC `cato_confirm_sale_action`; `cato_order_journeys`] | Lançar venda. O material sai do estoque e os cinco mil e duzentos reais ficam a receber. |
| [ILUSTRAÇÃO: uma pilha de material menor que o pedido; o cartão apaga e entra a mensagem "Não há estoque suficiente… Use a tela de Venda"] | Uma dica: se não tiver estoque pra vender, a proposta não passa. Aí o caminho é a tela de venda, que você já conhece. |
| Digita "Faz um ticket de compra da Cooperativa Recomeço: plástico PET, bruto 1.480, tara 60, motorista Jair Lopes, placa GHT7B19" e envia: o cartão A3 "Ticket de compra", "Somente pesagem, sem valores", "Plástico PET", "Peso líquido 1.420 kg", "Bruto", "Tara", "Motorista", "Veículo". [BACKEND: A3] | O ticket de pesagem também. Eu dou o bruto e a tara, e ele calcula o líquido: mil quatrocentos e vinte quilos. |
| [ZOOM: "Ao confirmar, o ticket recebe número. Estoque e financeiro não mudam até a valorização."]; clique em "Finalizar ticket": aviso verde e "Abrir comprovante". [BACKEND: RPC `cato_confirm_weighing_ticket_action`] | Ticket só registra a pesagem. Estoque e financeiro só mudam quando ele for valorizado, lá na tela do ticket. Dá pra pedir o ticket com valores também, dizendo o preço de cada material. |
| Digita "Sobe 50 centavos o preço de compra do cobre mel e do cobre misto" e envia: o cartão A4 "Tabela de preços", "Reajuste em 2 materiais", Cobre mel R$ 42,50 → R$ 43,00, Cobre misto R$ 36,00 → R$ 36,50, "Confirme em até 10 minutos.". [BACKEND: A4] | E os preços. Peço pra subir cinquenta centavos na compra dos dois cobres, e o cartão mostra o preço de hoje e o novo, lado a lado. |
| Clique em "Sim, atualizar": "Reajuste aplicado.". [BACKEND: RPC `cato_confirm_price_action` grava `price_table_items` da tabela "Principal"] | Sim, atualizar. Vale pra um material, pra vários ou pra tabela inteira, em porcentagem ou em reais. |

### cap09 · Contas, caixa e banco (vinheta: FINANCEIRO)

| Tela | Fala |
| --- | --- |
| Digita "Dá baixa na primeira parcela da Fundição Bandeira do Vale, recebi por Pix na Conta Principal" e envia: o cartão A5 com a faixa "Pagamento e recebimento", "Baixar conta", "Fatura venda #1731 (parcela 1/3)", R$ 4.790,00, "Forma" e "Data", "Confirmar baixa". [BACKEND: A5] | No financeiro, a mesma lógica. A Fundição pagou a primeira parcela, e eu peço a baixa: recebi por Pix, na Conta Principal. |
| Clique em "Confirmar baixa": "Conta baixada.". [BACKEND: RPC `cato_confirm_operation_action`, baixa a parcela e lança no banco] | Confirmar baixa, e a conta está baixada. |
| [ILUSTRAÇÃO: o sistema registra × o banco movimenta: um caderno com "baixa registrada" e o aplicativo do banco; uma seta riscada entre os dois] | Uma dica: o Cato registra no sistema. Ele não manda Pix nem movimenta a sua conta no banco. O dinheiro você movimenta no banco, e aqui fica o registro. |
| Digita "Abre o caixa com 1.500 reais": o cartão A6 "Abertura de caixa", "Abrir caixa", "Confirmar abertura"; confirma: "Caixa aberto.". [BACKEND: A6] [TESTAR: de onde sai o saldo inicial (cofre ou não)] | Dá pra abrir o caixa por aqui. Ele exige que você diga o valor contado, mesmo que seja zero. |
| Digita "Lança uma saída de 85 reais no caixa, gás da empilhadeira, categoria Combustível": o cartão A7 "Movimento de caixa", "Lançamento no caixa", "Confirmar lançamento"; confirma: "Lançamento no caixa registrado.". [BACKEND: A7] | Lançar uma saída, ou uma entrada, com o motivo e a categoria. Aqui, oitenta e cinco reais de gás da empilhadeira. Vale pro caixa, e vale pra conta do banco. |
| Digita "Transfere 2.000 da Conta Secundária pra Conta Principal": o cartão A8 "Transferência entre contas", "Transferir valores", o saldo de cada conta antes → depois, "Confirmar transferência"; confirma: "Transferência registrada.". [BACKEND: A8] | Transferir entre contas, ou do banco pro caixa. O cartão mostra o saldo de cada conta antes e depois. |
| Digita "Fecha o caixa, contei 1.415": o cartão A9 "Fechamento de caixa", "Fechar caixa", a diferença pro esperado, "Confirmar fechamento"; não confirma (rola o cursor). [BACKEND: A9] [TESTAR: a diferença] | E fechar o caixa: você diz quanto contou, e ele mostra a diferença pro que o sistema esperava, antes de você confirmar. |

### cap10 · Saldo de cliente e fornecedor (vinheta: FINANCEIRO)

| Tela | Fala |
| --- | --- |
| Digita "Abate 100 reais do saldo do Valdir Pereira, ele entregou uma bateria em troca"; resposta A10a (simulada, da regra do prompt: pergunta cliente ou fornecedor): "O saldo é de um cliente ou de um fornecedor?"; digita "fornecedor"; o cartão A10b "Valdir Pereira", "Movimentação no saldo", "Hoje: Ele te deve R$ 300,00.", "Ele ficará te devendo R$ 200,00.", "Não movimenta caixa nem banco.", "Confirmar", "Cancelar", "Corrigir". [BACKEND: A10] | Com saldo de parceiro, tem dois pedidos diferentes. O primeiro é o acerto: o Valdir abateu cem reais do vale dele, em troca de uma bateria. |
| [ZOOM: as duas linhas do saldo e "Não movimenta caixa nem banco."]; clique em "Confirmar". [BACKEND: RPC `cato_confirm_partner_balance_action`] | O cartão diz quanto ele te devia e quanto vai dever. E avisa: esse acerto não mexe em caixa nem em banco. |
| Digita "Registra o recebimento de 1.000 reais do saldo da Aços Quiririm, por Pix na Conta Principal": o cartão A11 com a faixa "Saldo do parceiro", R$ 1.000,00, "Origem", "Destino", "Forma", "Data"; confirma. [BACKEND: A11; `cato_confirm_operation_action`] | O segundo é quando entrou dinheiro de verdade. A Aços Quiririm pagou mil reais do que devia. Aí o saldo dela cai e o dinheiro entra na conta. |
| [ILUSTRAÇÃO: acerto × pagamento: duas fichas de parceiro; na primeira só o saldo muda; na segunda o saldo muda e uma moeda cai na conta do banco] | Uma dica: acerto muda só o saldo. Pagamento ou recebimento muda o saldo e o dinheiro. Diga qual dos dois você quer. |

### cap11 · Cadastros (vinheta: AÇÕES)

| Tela | Fala |
| --- | --- |
| Digita "Cadastra o fornecedor Sebastião Lima, telefone (12) 9 0000-0147": o cartão A12 "Novo parceiro", "Salvar cadastro"; confirma: "Cadastro de fornecedor salvo: Sebastião Lima.". [BACKEND: A12] | Fornecedor novo no balcão? Dá pra cadastrar pela conversa, com o nome e o que você souber dele. |
| Digita "Cadastra o material Chumbo, em kg, compra a 6,50 e venda a 8,00": o cartão A13 "Novo material", "Salvar cadastro"; confirma: "Cadastro de material salvo: Chumbo.". [BACKEND: A13] | Material também: nome, unidade e, se quiser, os preços. O cadastro nasce sem estoque. |
| [ILUSTRAÇÃO: cria × altera: um cartão de cadastro com "novo" aceso; lápis e lixeira apagados] | Uma dica: ele cria cadastro novo. Editar ou excluir um cadastro que já existe continua na tela de cadastro. |
| (só a ilustração anterior segue na tela) | E, pra quem usa o módulo de produção, ele também prepara uma ordem de produção e a conversão de um material em outro. Isso a gente vê no tutorial da produção. |

### cap12 · Fotos, planilhas e PDFs (vinheta: ARQUIVOS)

| Tela | Fala |
| --- | --- |
| Clique no clipe: "Escolher foto ou arquivo" e "Tirar foto"; escolhe `pesagem-cooperativa.jpg` (foto fictícia de um ticket de balança); a foto em "Arquivos para enviar"; o campo diz "Como usar os arquivos?"; envia sem texto. [BACKEND: tabela `cato_attachments`, bucket `cato-attachments`] | Em vez de digitar, você pode mandar o arquivo. Aqui no clipe: uma foto da pesagem, por exemplo. |
| Resposta A15a (código): "Li os dados da pesagem. O que você quer fazer com eles? Você pode pedir um ticket de compra ou de venda."; digita "Ticket de compra"; o cartão do ticket com "Arquivo usado" embaixo. [BACKEND: A15] | Ele lê a foto e pergunta o que fazer com aquilo. Eu peço o ticket de compra, e o cartão vem preenchido com os pesos da foto, pra eu conferir. |
| [ILUSTRAÇÃO: um arquivo com uma ordem escrita dentro ("lance agora"); o Cato ignora a ordem e aponta pro cartão] | Uma dica: o arquivo sozinho não lança nada. Se tiver uma ordem escrita dentro dele, o Cato ignora. Vale a mesma regra: ele prepara, você confere e confirma. |
| Anexa `tabela-fundicao.png` (print fictício de tabela de preços); resposta A16a (código): "Li a tabela do anexo. Você quer consultar os preços ou preparar uma atualização?"; digita "Atualizar"; A16b (código): "Esses valores são preços de compra ou de venda?" (sem responder). [BACKEND: A16] | Com um print de tabela de preços, ele pergunta se você quer só consultar ou atualizar os seus preços, e se são de compra ou de venda. |
| [ILUSTRAÇÃO: os formatos: foto, PDF e planilha, com "até três por vez"; ao lado, uma foto borrada e o balão "manda uma mais nítida"] | Ele aceita foto, PDF e planilha, até três arquivos por vez. Planilha grande, mande só o pedaço que interessa. E se a foto estiver ruim, ele pede outra mais nítida em vez de chutar. |

### cap13 · Nota fiscal pelo Cato (vinheta: FISCAL)

| Tela | Fala |
| --- | --- |
| Na venda do cap. 8, em "Próximos passos", clique em "Preparar NF-e": o pedido vai pro campo ("Prepare a NF-e da venda #…"). [BACKEND: A17a] | Agora a nota fiscal. A venda pra Serra Fina já está lançada, então eu uso o botão Preparar NF-e, nos próximos passos do pedido. |
| Resposta A17a (código): "Qual forma de pagamento deve constar na NF-e: dinheiro, PIX, transferência, boleto ou duplicata a prazo?"; digita "Duplicata a prazo". [TESTAR: se a venda no saldo pergunta mesmo] | Como a venda foi no saldo, ele pergunta que forma de pagamento deve constar na nota. Eu escolho duplicata a prazo. |
| O cartão A17b: a faixa "Nota fiscal eletrônica", "Rascunho de NF-e", "1 item(ns) para Serra Fina Alumínio Reciclagem", R$ 5.200,00, "Operação", "Forma de pagamento", "Vencimento"; a câmera passa pelos campos. [BACKEND: A17b] | Ele não pede pra digitar nada de novo. Busca no pedido o destinatário, os itens e o valor, e usa a configuração fiscal da empresa. |
| Clique em "Visualizar prévia do DANFE": "Preparando PDF…", abre o PDF numa aba; [ZOOM: "PDF para revisão. Não transmite a nota."]; volta. [BACKEND: prévia do DANFE (PDF fictício)] | Antes de qualquer coisa, a prévia do DANFE. É um PDF só pra revisar: não transmite a nota, ainda não foi nada pra SEFAZ. |
| Clique em "Criar rascunho": o cartão vira "Rascunho preparado" com "Emitir NF-e" e "Consultar situação". [BACKEND: RPC `cato_confirm_operation_action` cria `invoices` em rascunho] | Conferi a prévia: Criar rascunho. Repara que são duas confirmações. A primeira cria o rascunho. A nota só é enviada no segundo botão. |
| [ILUSTRAÇÃO: os três tempos: "rascunho", "enviada pra SEFAZ", "autorizada", cada um com o seu botão ou estado] | Uma dica: rascunho, envio e autorização são três momentos. Nota autorizada é só depois da resposta da SEFAZ. |
| Clique em "Emitir NF-e": "NF-e enviada para processamento na SEFAZ." e "Aguardando confirmação da SEFAZ". [BACKEND: edge `plugnotas-emit` simulada] | Emitir NF-e. Ele envia e fica acompanhando a resposta. |
| Clique em "Consultar situação": "NF-e autorizada", "A nota nº 1249 foi aprovada pela SEFAZ.", "O DANFE já está pronto para abrir."; [ZOOM no botão "Abrir DANFE"], sem clicar. [BACKEND: a nota vira `emitida` com a consulta] | Autorizada. Aparece o número da nota e o botão Abrir DANFE. |
| [ILUSTRAÇÃO: o Cato com a nota de um lado; do outro, a tela de Notas Fiscais com "cancelar", "carta de correção", "nota avulsa"] | Uma dica: pelo Cato sai a nota de um pedido que já existe. Nota avulsa, cancelamento e carta de correção continuam na tela de Notas Fiscais. E a tributação quem define é o seu contador. |
| Fala sobre a recusa, sem encenar: o cursor passa por "Consultar situação" (a faixa de erro e "Emitir novamente" não aparecem na gravação). | Se a SEFAZ recusar, o motivo aparece no cartão. Você corrige o cadastro ou a configuração e usa Emitir novamente. |

### cap14 · Pedidos, rotinas e revisões (vinheta: ROTINA)

| Tela | Fala |
| --- | --- |
| "Mais opções do Cato" → "Acompanhar pedidos": "Pedidos lançados por você no Cato. Até 20 registros dos últimos 30 dias."; "Para acompanhar" (a venda da Serra Fina com "A receber: R$ 5.200,00" e "Acompanhar NF-e") e "Outros pedidos" (a compra da Aparecida). [BACKEND: RPC `cato_order_journeys`] | Lembra dos três pontinhos? Em Acompanhar pedidos ficam os pedidos que você lançou pelo Cato, com o que falta em cada um: receber, pagar ou emitir a nota. |
| "Voltar à conversa"; menu → "Suas rotinas": "Ver sinais agora": "Estoque sem saída há pelo menos 30 dias", contas vencidas e a vencer. [BACKEND: RPC `cato_routines_manage` `preview`] | Em Suas rotinas, o botão Ver sinais agora mostra o que merece atenção: material parado no pátio, conta vencida e conta pra vencer. |
| "Agendamentos" → "Programar": "O que acompanhar" = "Contas a vencer e vencidas", "Frequência" = "Todo dia", horário 08:00, liga "Receber este resumo" ("Apenas uma notificação dentro do app"), "Salvar agendamento": "Agendamento salvo". [BACKEND: `cato_routines_manage` `save`] | E dá pra programar: todo dia, às oito, ele deixa um resumo das contas. O aviso chega aqui dentro do sistema, só pra você. |
| Menu → "Respostas revisadas": "Nenhuma resposta revisada". [BACKEND: `cato_corrections_manage` lista vazia] | Se uma resposta antiga do Cato for corrigida depois, a correção aparece em Respostas revisadas. |

### cap15 · Limites e permissões (vinheta: LIMITES)

| Tela | Fala |
| --- | --- |
| Conversa; digita "O que você consegue fazer?" e envia: A18 (código, montada por `buildCatoCapabilitiesAnswer`): "O que consigo fazer no seu acesso agora", "1. Ações com sua confirmação" (a lista), "Pagamentos registram a operação no EcoSistema; não transferem dinheiro pela sua conta bancária.", "2. Consultas", "3. Limites". [BACKEND: A18] | Na dúvida do que dá pra pedir, pergunte pra ele: o que você consegue fazer? A lista que ele mostra é a do seu usuário, e ele avisa que pagamento registra a operação no sistema, não transfere dinheiro pelo banco. |
| Corte: Marcos Antunes; digita "Atualiza o preço de compra do cobre mel pra 43 reais"; resposta A19 (código): "Seu usuário não tem permissão para alterar preços. Peça ao administrador da empresa para conferir seu acesso. Nenhum preço foi alterado." [BACKEND: A19; Marcos sem a permissão de editar material] | Agora, um corte: é o Marcos. Ele pede pra atualizar o preço do cobre mel, e o Cato responde que o usuário dele não tem permissão pra alterar preços. Nenhum preço foi alterado. |
| [ILUSTRAÇÃO: a mesma chave abre a tela e o Cato: uma permissão ligada às duas portas; conferida no pedido e no clique] | O Cato não dá poder a mais pra ninguém. Cada ação pede a mesma permissão da tela: registrar compra, dar baixa em conta, emitir nota. E ela é conferida de novo no clique do cartão. |
| "Usuários e Permissões", a restrição de ver só os próprios pedidos, com o trecho "o Cato fica indisponível para evitar exposição indireta". [ZOOM no trecho] | Uma dica: quem tem restrição de ver só os próprios cadastros, pedidos ou tíquetes, ou só algumas contas do banco, fica sem o Cato. É pra ele não mostrar o que a pessoa não pode ver. |
| [ILUSTRAÇÃO: o que fica nas telas: editar e excluir cadastro, ajustar estoque, cancelar nota, reabrir caixa; cada item acende com a fala] | E o que ele ainda não faz: editar ou excluir cadastro, ajustar estoque, cancelar nota e reabrir caixa. Nesses casos, ele explica o caminho na tela. |
| [ILUSTRAÇÃO: limites de uso: um relógio "por minuto" e um calendário "por dia"; um balão "espera um minutinho" e uma seta de volta ao chat] | Uma dica: o Cato tem um limite de perguntas por minuto e por dia. É um limite que protege o custo do serviço, não é castigo. Se ele pedir pra você esperar um minutinho, a espera resolve. |
| Volta ao Rafael; o rodapé "O Cato.ai pode cometer erros. Confira informações importantes.". | E continua valendo: ele pode errar. Por isso existe o cartão. Leia antes de confirmar. |

### cap16 · Avaliar e falar com o suporte (vinheta: AJUDA)

| Tela | Fala |
| --- | --- |
| Na resposta da tabela (R8), clique em "Resposta útil" (👍); em outra resposta, clique em "Resposta não útil" (👎): "Número errado", "Não entendeu", "Faltou detalhe", "Resposta lenta", "Outro"; clique em "Faltou detalhe". [BACKEND: RPC `set_cato_feedback`] | Em cada resposta, tem o joinha e o dedo pra baixo. Ajudou, é só clicar no joinha. Se não ajudou, o dedo pra baixo abre os motivos, num clique. |
| A pesquisa de fim de conversa: "Sim / Consegui concluir", "Em parte / Ajudou, mas faltou algo", "Não / Ainda preciso resolver", a nota de zero a dez, "Enviar avaliação". [BACKEND: o robô avança o relógio 3 minutos; RPC `submit_cato_resolution_feedback`] | Depois de um tempo parado, ele também pergunta se a conversa resolveu o que você precisava. Leva dois cliques. |
| "Mais opções do Cato" → "Falar com atendente": janela "Falar com o suporte". | E quando você precisar de uma pessoa de verdade, o caminho está nos três pontinhos: Falar com atendente. |
| A câmera passa por "Ver vídeos", "Ver artigos", "Em qual tela/módulo? *", "O que aconteceu? Descreva com detalhes *" e "Você já assistiu aos nossos tutoriais sobre isso? *", e para em "Falar no WhatsApp", sem clicar; fecha. | Você conta em qual tela estava e o que aconteceu, e o botão Falar no WhatsApp abre a conversa com o suporte, com tudo já escrito. |

### cap17 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a janela de autorização e a janela da memória. | Pronto! Recapitulando: a gente achou o Cato, autorizou o uso e ligou a memória, que é só sua. |
| Montagem rápida: as respostas, o gráfico, a tabela e o "Total geral" da Posição de Estoque. | Fez as perguntas do dia a dia, viu quando vem gráfico e quando vem tabela, e conferiu um número na tela de origem. |
| Montagem rápida: os cartões de compra, venda, ticket e preço. | Pediu uma compra, uma venda, um ticket e um reajuste de preço, sempre conferindo o cartão antes de confirmar. |
| Montagem rápida: baixa, caixa, saldo, foto e o DANFE. | Baixou conta, mexeu no caixa, acertou saldo, mandou foto e emitiu a nota de um pedido, com a prévia do DANFE. |
| Montagem rápida: a resposta de capacidades e o corte do Marcos. | E viu os limites: o Cato prepara, você confirma, e cada um só faz o que a sua permissão deixa. |
| Cartão "Próximo: Dashboard, Agenda e rotina"; cartela final. | No próximo tutorial, a gente olha a tela inicial e a rotina que mantém o sistema vivo. Até lá! |
