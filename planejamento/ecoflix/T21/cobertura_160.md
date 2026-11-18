# Cobertura 1.60.10 · T21 · Cato, o assistente

Auditoria só de leitura (código em `/dev/shm/ecoflix-src`, diff `f37573ea0..5290be4cd`). Caminhos relativos a `src/`
(edge em `supabase/functions/`). Nada foi editado fora deste arquivo. Varredura do robô da T21 ainda não existe
(`rec/varredura/` só tem t00 a t04).

**Resumo:** o Cato deixou de ser só leitura. No 1.60.10 a tela manda 11 capacidades em toda pergunta
(`lib/cato/messages.ts:295`) e o servidor oferece **18 tipos de ação** com cartão de confirmação, anexos, NF-e,
acompanhamento de pedidos, rotinas e memória pessoal. A tese da aula ("o Cato consulta e você executa", cap. 7 e resumo)
ficou **falsa**. Metade do roteiro se aproveita (autorização e perguntas); a outra metade é nova.

## 0. O que se aproveita do roteiro atual

| Cap. atual | Fala | Tela (gravação) | Ilustração |
|---|---|---|---|
| 00 Abertura | reescrever (promete só "tirar dúvida") | regravar | trocar (falta o "fazer") |
| 01 Onde fica | **aproveita inteira** | regravar (rótulo do botão pode mudar, ver 1) | aproveita |
| 02 Autorizar | **aproveita inteira** (a janela não mudou, sem diff) | aproveita o corte do Marcos e o aceite; o final muda (abre a janela da memória) | aproveita |
| 03 Perguntas prontas | aproveita, com o número já proposto (69.600) e uma frase nova do clipe | regravar (painel mudou) | |
| 04 O que responde bem | **aproveita inteira** | regravar (painel mudou) | aproveita |
| 05 Gráfico ou tabela | **aproveita inteira** | regravar | aproveita as duas |
| 06 De onde vêm os números | **aproveita inteira** | regravar | aproveita |
| 07 Limites | **descartar** as 3 primeiras linhas e a ilustração "consulta × executa"; só a dica do limite de uso fica | descartar R9 | fica só "limites de uso" |
| 08 Avaliar e suporte | reescrever 2 linhas ("Falar com atendente" mudou de lugar) | regravar | |
| 09 Recapitulando | reescrever | montagem nova | |

Toda cena com o painel aberto precisa ser regravada: cabeçalho, barra de ações e campo mudaram (seção 1). O áudio dos
caps. 01, 02, 04, 05 e 06 serve como está.

## 1. Mudou no app (por capítulo do roteiro atual)

**cap00 / cap01 · botão**
- Rótulo com aviso pendente: era "Abrir nova resposta do Cato", agora **"Abrir 1 notificação do Cato"** (resposta,
  dica, rotina ou resposta revisada) (`components/cato/CatoFab.tsx:332`).
- Novo: balão de dica ao lado do botão, com frase sorteada e **"Abrir Cato"** / "Fechar dica do Cato"
  (`CatoFab.tsx:29-71,295-305`), às vezes com o nome da pessoa ou da empresa (`lib/cato/nudgePersonalization.ts`). Na
  gravação o balão pode aparecer sobre a tela "Estoque": a semente precisa calar (chave
  `cato_adoption_nudge_<empresa>_<usuário>` no armazenamento local) ou a aula mostra de propósito (proposta: mostrar 1 vez).
- Convite do beta: o texto "por enquanto ele só consulta e não altera nada" virou "Além de consultar, ele prepara ações
  como reajustar preços, lançar compras e vendas e criar tickets de pesagem. Antes de qualquer mudança, você confere um
  resumo e confirma no cartão" (`CatoInviteModal.tsx`). A aula continua sem mostrar.

**cap02 · autorização**
- A janela "Antes da primeira conversa com o Cato" **não mudou**. Muda o que vem depois: com a autorização dada, na
  primeira abertura do painel aparece **"Quer que o Cato lembre de você?"** com "Agora não" e **"Usar memória"**
  (`CatoMemoryConsentDialog.tsx:35-73`; gatilho em `CatoFab.tsx:185-190`, uma vez por sessão enquanto a decisão for
  `pending`). A fala "Pronto: o Cato está autorizado" hoje é seguida por essa janela na tela.

**cap03 · painel**
- Cabeçalho: o sino ("Desligar o som do Cato") saiu. No lugar, **"Mais opções do Cato"** (três pontinhos) com
  "Notificações" (Ligadas/Desligadas), "Ler respostas automaticamente", "Acompanhar pedidos", "Suas rotinas",
  "Respostas revisadas", "Falar com atendente" e "Sobre o Cato" (`CatoChatPanel.tsx:1095-1139`).
- A barra "Conversas", "Nova", "Memória" desceu para **baixo do campo** (`:1709-1713`).
- As perguntas prontas ganharam o rótulo **"Sugestões para começar"** (`:1196`) e as pílulas, **"Sugestões de
  perguntas"** (`:1564`).
- Campo: novo botão de clipe **"Anexar foto, arquivo ou planilha"** com "Escolher foto ou arquivo" e "Tirar foto"
  (`:1603-1620`); o campo agora cresce até 5 linhas; com anexo o texto de apoio vira "Como usar os arquivos?" e,
  ocupado, "Prepare sua próxima pergunta…" (`:1645`).
- Achado antigo continua: em `/materiais` as duas últimas sugestões saem sorteadas (`lib/cato/starterPrompts.ts` sem diff).

**cap04 a cap06 · respostas**
- "Consultei …", linha do período, gráfico, tabela e botão de destino: **sem mudança** (`lib/cato/messages.ts` e
  `responsePresentation.ts` só ganharam tipos). Novo: botão flutuante **"Nova resposta"** quando a pessoa rolou para
  cima (`CatoChatPanel.tsx:1521-1528`).

**cap07 · limites (o capítulo que caiu)**
- "Emite a nota da venda pra Fundição Bandeira do Vale" **não vira mais orientação**: chama a ação de NF-e
  (`_shared/cato/operations.ts:156-175`, `systemPrompt.ts` "NF-e DO PEDIDO"). A resposta R9 e a ilustração
  "consulta × executa" estão erradas.
- A regra do servidor deixou de ser "VOCÊ QUASE SÓ LÊ" e virou "CAPACIDADES ATUAIS: as ferramentas de AÇÃO deste turno
  podem preparar operações reais, incluindo compras, vendas, tickets, cadastros, financeiro, produção e NF-e …
  A proposta só é executada após confirmação no cartão e revalidação de permissões" (`_shared/cato/systemPrompt.ts`).
- Limites de uso: os mesmos quatro (20/min usuário, 40/min empresa, 300/dia empresa, 40/dia usuário,
  `cato-assist/index.ts:101-118,479-532`). Novo: limite **por conversa** para análises pesadas e anexos, com o aviso
  "Esta conversa já fez análises mais pesadas. Prefira um arquivo ou recorte específico por vez." (`:636-649`).

**cap08 · avaliar e suporte**
- **"Falar com atendente" saiu do rodapé** e foi para o menu "Mais opções do Cato" (`:1129-1132`). "Cato.ai v1.0" saiu
  do rodapé; virou "Sobre o Cato" no mesmo menu, que abre "Novidades do Cato" (`:1133-1137,1720-1761`).
- Novo: pesquisa de fim de conversa (3 minutos parado, depois de duas perguntas): "Sim / Consegui concluir", "Em parte /
  Ajudou, mas faltou algo", "Não / Ainda preciso resolver", nota de zero a dez e "Enviar avaliação"
  (`CatoResolutionSurvey.tsx:22-39,227-298`; gatilho `CatoChatPanel.tsx:811-840`).
- A janela "Falar com o suporte" não mudou.

## 2. Falta cobrir

### 2.1 Ações com cartão (o que o código oferece)
Regras comuns: o Cato pergunta **uma informação por vez**; chamar a ação só **propõe**; "sim" escrito no chat não
executa; a prévia vale **10 minutos**; o servidor confere a permissão de novo no clique. Rótulos dos cartões:

| # | Ação | Cartão (rótulos exatos) | Permissão conferida | Vale capítulo? |
|---|---|---|---|---|
| 1 | Lançar compra | "Entrada de material" / "Finalizar compra" / "Fornecedor: …" / "Preços informados nesta conversa" / "Total da compra" / "Forma de pagamento", "Conta", "Vencimento" / "Estoque entra e o financeiro registra R$ …" / **"Corrigir dados"**, **"Agora não"**, **"Lançar compra"**; depois "Abrir comprovante" (`CatoActionCard.tsx:470-559`) | "Registrar Compra" | **sim** (é o exemplo da nota de versão) |
| 2 | Lançar venda | igual, "Saída de material" / "Finalizar venda" / **"Lançar venda"**; a prévia cai se faltar estoque (`:68`, `tools.ts:1033`) | "Registrar Venda" | **sim** |
| 3 | Ticket de pesagem (compra ou venda, sem ou com valores) | "Ticket de compra" / "Somente pesagem, sem valores" / "Peso líquido", "Bruto", "Tara", "Impureza" / "Motorista", "Veículo" / "Ao confirmar, o ticket recebe número. Estoque e financeiro não mudam até a valorização." / **"Finalizar ticket"** ou "Finalizar por R$ …" / "Abrir comprovante" (`:643-719`) | "Ticket de Pesagem — Compra/Venda", "Criar Ticket de Pesagem com Valores" | **sim** |
| 4 | Reajustar preços (1 material, vários, tabela inteira; % ou reais) | "Tabela de preços" / "Reajuste preparado" ou "Reajuste em N materiais" / de → para / "+ N outros materiais — ver todos" / "N materiais sem preço cadastrado ficaram de fora." / "Confirme em até 10 minutos." / **"Sim, atualizar"** (`:270-365`) | editar material | **sim** (era o risco 2 do plano) |
| 5 | Ajuste de saldo de parceiro (sem dinheiro) | "Movimentação no saldo" ou "Definir saldo final" / "Hoje: Ele te deve R$ …" / "Ele ficará te devendo R$ …" / **"Não movimenta caixa nem banco."** / "Confirmar", "Cancelar", "Corrigir" (`CatoBalanceActionCard.tsx:56-68`) | "Lançar crédito/débito no saldo" | **sim** |
| 6 | Pagar ou receber saldo de parceiro (com dinheiro) | faixa "Saldo do parceiro"; fatos "Origem", "Destino", "Forma", "Data", "Vínculo" (`CatoOperationActionCard.tsx:77,300`) | "Dar Baixa em Conta", "Ver saldos de cliente/fornecedor" | **sim**, junto do 5 (a diferença é o ponto) |
| 7 | Baixar conta (pagar ou receber um título) | faixa "Pagamento e recebimento" / "Baixar conta" / **"Confirmar baixa"** / depois "Conta baixada." | "Dar Baixa em Conta" | **sim** |
| 8 | Entrada ou saída no caixa | "Movimento de caixa" / "Lançamento no caixa" / "Confirmar lançamento" | "Registrar Receita/Despesa" | **sim** |
| 9 | Entrada ou saída no banco | "Movimento bancário" / "Movimentação bancária" / "Confirmar lançamento" | "Registrar Movimentação Bancária", "Usar Contas Bancárias" | trecho |
| 10 | Transferência (banco, caixa, contas) | "Transferência entre contas" / "Transferir valores" / saldos antes → depois / **"Confirmar transferência"** | "Registrar Transferências Financeiras" | trecho |
| 11 | Abrir caixa | "Abertura de caixa" / "Abrir caixa" / "Confirmar abertura" (o saldo inicial tem de ser dito, até se for zero) | "Abrir Caixa" | trecho |
| 12 | Fechar caixa | "Fechamento de caixa" / "Fechar caixa" / mostra a diferença / "Confirmar fechamento" | "Fechar Caixa" | trecho |
| 13 | Cadastrar parceiro | "Novo parceiro" / "Salvar cadastro" (não altera cadastro existente) | "Cadastrar Parceiros" | trecho |
| 14 | Cadastrar material | "Novo material" / "Salvar cadastro" (sem mexer em estoque) | "Cadastrar Materiais" | trecho |
| 15 | Ordem de produção | "Planejamento da produção" / "Planejar ordem de produção" / "Criar ordem" | "Registrar Produção" | só citar (módulo de produção, T11) |
| 16 | Conversão de materiais | "Conversão de materiais" / "Converter materiais" / "Confirmar conversão" | "Registrar Produção" | só citar |
| 17 | Preparar NF-e de um pedido | "Nota fiscal eletrônica" / "Preparar NF-e" / **"Visualizar prévia do DANFE"** + "PDF para revisão. Não transmite a nota." / "Ambiente: Produção" / **"Criar rascunho"**; depois "Rascunho preparado", **"Emitir NF-e"**, "Consultar situação", "Ver itens e tributos"; depois "NF-e enviada para processamento na SEFAZ."; por fim **"NF-e autorizada"**, "A nota nº N foi aprovada pela SEFAZ.", "O DANFE já está pronto para abrir.", **"Abrir DANFE"** (`CatoOperationActionCard.tsx:85,380`, `CatoDanfePreviewButton.tsx:26-30`, `CatoInvoiceResult.tsx:125-209`, `CatoFiscalDetails.tsx:38-44`) | "Emitir NF-e (Produto)" | **sim, capítulo próprio** (parte fiscal) |
| 18 | "O que você consegue fazer?" | resposta montada com as ações liberadas **para aquele usuário**: "O que consigo fazer no seu acesso agora", "1. Ações com sua confirmação", "2. Consultas", "3. Limites" (`_shared/cato/capabilityAnswer.ts`) | | **sim** (fecha os limites) |

Fontes da lista: `_shared/cato/operations.ts:5-18` (12 operações), `tools.ts:817,882,1033,1056` (preço, compra, venda,
ticket), `systemPrompt.ts` (ajuste de saldo), `capabilityAnswer.ts:1-20`. Títulos e rótulos de confirmação das operações
vêm do banco (`supabase/migrations/20261114160000_cato_operation_framework.sql` e seguintes).

### 2.2 O resto que o roteiro não mostra

| Função | O que é / quando usa | Vale? |
|---|---|---|
| Perguntas de esclarecimento | faltou dado ou há dois cadastros parecidos: ele pergunta, com as opções reais ("Foi em dinheiro, Pix ou transferência?", "Qual conta bancária foi usada?", "Não encontrei um único parceiro com esse nome…") | sim, dentro da compra |
| "Corrigir dados" / "Corrigir" | devolve o pedido para o campo, já escrito, para a pessoa mudar o que quiser (`CatoChatPanel.tsx:188-223,695-699`) | sim |
| Estados do cartão | "Você optou por não lançar esta compra.", "A proposta expirou ou algum cadastro mudou. Peça ao Cato para montar novamente.", "Os preços mudaram nesse meio tempo — peça o reajuste de novo.", "Você não tem permissão para registrar compras." | sim (dica) |
| "Próximos passos" depois de compra ou venda | "Pedido registrado → A receber: R$ …", botões "Registrar pagamento/recebimento", "Pagar/Receber saldo do parceiro", "Preparar NF-e", "Acompanhar NF-e" (`CatoOrderJourney.tsx`) | sim |
| "Acompanhar pedidos" (menu) | lista dos pedidos lançados pelo Cato, "Para acompanhar" e "Outros pedidos"; até 20 dos últimos 30 dias | sim, trecho |
| Anexos | até 3 arquivos, foto JPG/PNG/WebP (até 20 MB, o app reduz), PDF, XLSX ou CSV (até 5 MB); planilha até 3 abas, 200 linhas e 20 colunas; colar e arrastar também valem; "Arquivos para enviar", "Arquivo usado"; perguntas "Li os dados da pesagem. O que você quer fazer com eles?…", "Li a tabela do anexo. Você quer consultar os preços ou preparar uma atualização?", "Esses valores são preços de compra ou de venda?", "Não consegui ler o arquivo com segurança. Pode enviar uma foto mais nítida ou um recorte menor?" (`lib/cato/attachments.ts:4-6,93-97`, `_shared/cato/attachments.ts:66-74,141-236`, `cato-assist/index.ts:655-657`) | **sim, capítulo** |
| Memória pessoal (1.60.9) | janela de convite; "Memória" → "Memória do Cato", abas "Minha memória" / "Da empresa", chave "Lembrar entre conversas", "Adicionar nota", lápis, lixeira, "Apagar toda a minha memória"; "Notas e preferências expiram em 90 dias; assuntos recentes, em 30 dias. Valores, saldos e preços são consultados novamente. Pausar não apaga o que foi salvo."; cartão no chat "Quer guardar esse combinado para as próximas conversas?" com "Guardar para próximas conversas" / "Só nesta conversa" (`CatoMemoryDialog.tsx`, `CatoMemorySuggestion.tsx`) | **sim, capítulo** |
| Notas da empresa | aba "Da empresa": só quem tem acesso total publica; valem para todos que usam o Cato | sim, trecho |
| "Conversas" e "Nova" | "Suas conversas", "Retome uma análise de onde parou." (`CatoHistoryDialog.tsx:117-140`) | sim, trecho |
| "Suas rotinas" | "Ver sinais agora" (estoque sem saída há 30 dias, contas vencidas e a vencer) e "Programar": "Resumo da rotina", "Contas a vencer e vencidas", "Estoque sem saída há 30 dias"; "Todo dia" / "Toda semana", horário; aviso só dentro do app; também abre escrevendo "me avise todo dia às 8 das contas a vencer" (`CatoRoutinesPanel.tsx`, `lib/cato/routines.ts`) | sim, trecho |
| "Respostas revisadas" | quando uma resposta antiga é corrigida, a correção aparece ali, com "Ver conversa completa" | só citar |
| Voz | microfone "Falar" (o texto aparece e a pessoa revisa antes de enviar), "Ouvir resposta", "Ler respostas automaticamente" | só citar (já citado no cap. 2) |
| "Notificações" | liga e desliga o som do Cato | só citar |
| Tela cheia | "Expandir para tela cheia" / "Recolher janela" | só citar |
| Formulário por pedido | se a pessoa pedir "formulário" ou "modo manual", o Cato mostra um cartão que abre a tela do sistema dentro da conversa (`lib/cato/operationalWorkflows.ts`, `CatoWorkflowCard.tsx`) | **não**: caminho de exceção, confunde com o cartão de confirmação |
| Quem pode usar | permissão "Usar o Cato (assistente de IA)" com o aviso "o Cato responde sobre dados gerais da empresa … mesmo de telas que este usuário não pode abrir" (`config/routes.ts:309`); quem tem restrição de ver só os próprios cadastros, pedidos, tíquetes ou contas escolhidas fica **sem o Cato** (`routes.ts:331-364`, `_shared/cato/access.ts:35-40,196-201`) | **sim** (permissões foi pedido) |
| O que ele ainda não faz | editar ou excluir cadastro, zerar ou ajustar estoque, cancelar nota, emitir NFS-e, MDF-e, MTR ou CDF, valorizar ou cancelar ticket, reabrir caixa, mandar Pix de verdade, câmbio entre contas (`capabilities.ts:14-37`, `capabilityAnswer.ts` "3. Limites") | **sim** |
| Abas internas (Analytics, Operações, Aprendizado, Efetividade) | painel da equipe EcoSistema | não: não é do cliente |
| Cadastro de usuário e permissão | onde se liga a permissão do Cato | T2 (só citar o caminho) |

## 3. Proposta: estrutura nova completa

- **Título proposto:** "Cato, o agente de IA" (o cabeçalho do painel diz "Agente de IA da EcoSistema"). Manter "Cato, o
  assistente" se o catálogo não puder mudar.
- 18 capítulos (00 a 17). Vinhetas: CATO · AUTORIZAÇÃO · MEMÓRIA · PERGUNTAS · RESPOSTAS · AÇÕES · FINANCEIRO · ARQUIVOS ·
  FISCAL · ROTINA · LIMITES · AJUDA · RESUMO.
- `FAKE_NOW` 2026-11-10T08:30. As respostas e os cartões continuam **simulados** no backend falso, no formato real.
- Caps. 04 a 06 são uma conversa; caps. 07 a 12 são outra ("Nova"), para o "Total geral" do estoque do cap. 06 bater
  antes de qualquer lançamento.

### cap00 · Abertura
| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título. | (sem fala) |
| [ILUSTRAÇÃO: dois balões: "Quem tá me devendo?" recebe um valor; "Lança uma compra de 120 kg de latinha" recebe um cartão com um botão de confirmar] | Oi! Neste tutorial a gente conhece o Cato, o agente de inteligência artificial do EcoSistema. |
| (a ilustração segue: o balão da pergunta acende, depois o do cartão) | Ele faz duas coisas. Responde perguntas sobre o seu negócio, com o número na hora. E prepara tarefas pra você: uma compra, uma baixa de conta, até uma nota fiscal. |
| Tela "Estoque", Rafael Nogueira; a câmera vai ao botão redondo. | Na Recicla Vale Metais, o Rafael pede em português, confere o resumo e confirma. Nada é lançado só por conversar. |
| Cartão "Antes: Relatório Financeiro e DRE". | Se você ainda não viu os tutoriais de compra e venda, de contas e de notas fiscais, vale ver antes. Aqui a gente faz as mesmas tarefas, só que pela conversa. |

### cap01 · Onde o Cato fica (CATO)
| Tela | Fala |
| --- | --- |
| Zoom no botão redondo ("Abrir o Cato"). | (fala atual, linha 1) Com o Cato liberado na conta da empresa, ele fica neste botão redondo, no canto de baixo, em qualquer tela do sistema. |
| [ILUSTRAÇÃO atual: computador × celular] | (fala atual, linha 2) No computador, ele fica à direita. No celular, à esquerda, logo acima da barra de baixo. |
| Balão de dica ao lado do botão, com "Abrir Cato"; a bolinha de notificação no botão. [BACKEND: sem a chave `cato_adoption_nudge_…`] | De vez em quando ele mostra uma dica do que pode fazer. É só clicar pra abrir, ou fechar a dica no xis. |
| "Usuários e Permissões", edição do Marcos, a linha "Usar o Cato (assistente de IA)" com a descrição. [ZOOM na descrição] | Quem usa o Cato é quem tem esta permissão. Uma dica: o Cato responde sobre os dados gerais da empresa, até de telas que a pessoa não abre. Libere pra quem pode ver esses números. |
| Clique no botão: abre "Antes da primeira conversa com o Cato". | (fala atual, linha 3) Pra abrir, é só clicar. Na primeira vez, antes da conversa, aparece a autorização. |

### cap02 · Autorizar o Cato (AUTORIZAÇÃO)
Fala e Tela atuais, sem mudança, até o clique em "Entendi e autorizo" (aviso "Cato autorizado"). O capítulo termina no
aviso; a janela da memória é o cap. 03.

### cap03 · A memória do Cato (MEMÓRIA) · novo
| Tela | Fala |
| --- | --- |
| Painel abrindo e, por cima, "Quer que o Cato lembre de você?". [BACKEND: `cato_memory_manage('status')` com `personalDecision: "pending"`] | Logo na primeira conversa, o Cato pergunta se pode lembrar de você. |
| [ZOOM: "Ele guarda apenas preferências declaradas e assuntos recentes. Saldos, preços e quantidades são sempre consultados novamente no sistema."] | Com a memória ligada, ele guarda as preferências que você disser e os assuntos recentes, pra continuar de onde parou. Número ele não decora: saldo, preço e quantidade ele consulta de novo, toda vez. |
| [ZOOM: "A memória é pessoal dentro desta empresa…"] | A memória é só sua. Outro usuário não vê, e ela não guarda senha nem documento. |
| Clique em "Usar memória": aviso "Memória do Cato ativada". [BACKEND: ação `accept_personal_consent`] | O Rafael clica em Usar memória. Se preferir, é só clicar em Agora não e ligar depois. |
| Rodapé do painel, botão "Memória": janela "Memória do Cato", aba "Minha memória", chave "Lembrar entre conversas"; "Adicionar nota": digita "Prefiro os valores em tabela, do maior para o menor." e "Salvar nota"; a nota na lista com lápis e lixeira. | Tudo que ele guardou fica aqui, no botão Memória. Dá pra escrever uma nota, corrigir, apagar uma por uma ou apagar tudo. |
| [ZOOM: "Notas e preferências expiram em 90 dias; assuntos recentes, em 30 dias. … Pausar não apaga o que foi salvo."] | As notas valem por noventa dias, e os assuntos recentes, por trinta. Desligar a chave só pausa: o que já estava salvo continua lá. |
| Aba "Da empresa": "Usar notas da empresa" e o aviso de quem publica. | E tem as notas da empresa, que valem pra todo mundo que usa o Cato. Só quem tem acesso total escreve ali. |

### cap04 · Conhecendo o painel (PERGUNTAS)
| Tela | Fala |
| --- | --- |
| Painel com "Oi, Rafael 👋", "Sugestões para começar". | (fala atual cap03, linha 1) Com o Cato autorizado, o painel abre aqui do lado, com quatro perguntas prontas pra quebrar o gelo. |
| Campo "Pergunte ao Cato…": o clipe, o microfone e "Enviar". | Aqui embaixo você escreve do jeito que fala. O clipe anexa foto ou arquivo, e o microfone escreve o que você disser, pra você conferir antes de enviar. |
| Barra "Conversas", "Nova", "Memória"; clique em "Conversas": "Suas conversas", "Retome uma análise de onde parou."; fecha. | Embaixo do campo ficam as suas conversas antigas, o botão de começar uma nova e a memória. |
| "Mais opções do Cato": o menu aberto; a câmera passa pelos itens; fecha. | E nos três pontinhos ficam o som, a leitura em voz alta, os pedidos, as rotinas e o atendente. A gente volta neles já já. |
| Clique em "Como tá indo meu negócio esse mês?" [R1]. | (fala atual cap03, linhas 3 a 5, com "sessenta e nove mil e seiscentos") |

### cap05 · O que ele responde bem (PERGUNTAS)
Fala e Tela atuais do cap04 (R2 a R5 e a dica do caixa de hoje).

### cap06 · Gráfico, tabela e de onde vêm os números (RESPOSTAS)
Fala e Tela atuais do cap05 e do cap06, em sequência (R6, R7, R8, a regra dos gráficos, "Abrir posição de estoque", o
"Total geral" e o rodapé). Uma vinheta só.

### cap07 · Lançar uma compra pela conversa (AÇÕES) · novo
| Tela | Fala |
| --- | --- |
| "Nova" (conversa limpa); digita "Lança uma compra de 120 kg de alumínio latinha da Aparecida Ramos" e envia. | Agora, a parte nova: pedir pro Cato fazer. Vou pedir uma compra de cento e vinte quilos de latinha da Aparecida Ramos. |
| Resposta: "Qual o preço por kg?"; digita "6,20". Resposta: "Como foi o pagamento: dinheiro, Pix ou saldo?"; digita "Pix, pela Conta Principal". [BACKEND: A1a, A1b] | Faltou o preço e a forma de pagamento, então ele pergunta. Uma coisa de cada vez, e eu respondo curtinho. |
| O cartão: "Entrada de material", "Finalizar compra", "Fornecedor: Aparecida Ramos", "Alumínio latinha 120 kg", "R$ 6,20/kg", "Total da compra R$ 744,00", "Forma de pagamento Pix", "Conta Conta Principal". [ZOOM no cartão inteiro] [BACKEND: A1c] | Com tudo na mão, ele monta este cartão. Fornecedor, material, quantidade, preço, total e como foi pago. É o resumo pra você conferir. |
| [ZOOM: "Estoque entra e o financeiro registra R$ 744,00."] | Repara nesta linha: até aqui, nada mudou. O estoque só entra e o financeiro só registra quando você confirma. |
| [ILUSTRAÇÃO: a regra do cartão: três passos, "você pede", "o Cato pergunta e monta o resumo", "você confirma no botão"; um balão "sim" riscado ao lado] | Uma dica: escrever sim na conversa não confirma nada. Quem lança é o botão do cartão, e é você quem clica. |
| Cursor em "Corrigir dados" (o pedido volta escrito no campo; apaga) e em "Agora não" (sem clicar). | Errou alguma coisa? Corrigir dados devolve o pedido pro campo, pra você mudar só o que precisa. E Agora não desiste, sem lançar. |
| Clique em "Lançar compra": o cartão vira o aviso verde com o número do pedido e "Abrir comprovante". [BACKEND: RPC `cato_confirm_purchase_action`] | Conferi, está certo: Lançar compra. Pronto, a compra entrou, com o número do pedido e o comprovante pra abrir. |
| Embaixo, "Próximos passos": abre; "Pedido registrado", "Pagamento registrado", "Preparar NF-e". [BACKEND: RPC `cato_order_journeys`] | E ele já mostra os próximos passos desse pedido: o pagamento e a nota fiscal. |
| [ILUSTRAÇÃO: um relógio de dez minutos ao lado de um cartão; o cartão apaga e aparece "peça de novo"] | Uma dica: o cartão vale por dez minutos. Se passar disso, ou se um cadastro mudar no meio, ele expira, e é só pedir de novo. |

### cap08 · Venda, ticket de pesagem e preços (AÇÕES) · novo
| Tela | Fala |
| --- | --- |
| Digita "Lança uma venda de 500 kg de alumínio perfil pra Serra Fina, a 10,40, no saldo, vencimento 10/12" e envia: cartão "Saída de material", "Finalizar venda", "Total da venda R$ 5.200,00", "Forma de pagamento Saldo", "Vencimento 10/12/2026". [BACKEND: A2] | A venda é igual. Desta vez eu já disse tudo de uma vez: cliente, material, quantidade, preço e pagamento. Ele não pergunta nada e já traz o cartão. |
| Clique em "Lançar venda": aviso verde, "Abrir comprovante"; "Próximos passos" mostra "A receber: R$ 5.200,00". [BACKEND: RPC `cato_confirm_sale_action`] | Lançar venda. O material sai do estoque e os cinco mil e duzentos reais ficam a receber. |
| [ILUSTRAÇÃO: uma pilha de material menor que o pedido; o cartão apaga com "estoque insuficiente"] | Uma dica: se não tiver estoque pra vender, a proposta não passa. Aí o caminho é a tela de venda, que você já conhece. |
| Digita "Faz um ticket de compra da Cooperativa Recomeço: plástico PET, bruto 1.480, tara 60, motorista Jair Lopes, placa GHT7B19" e envia: cartão "Ticket de compra", "Somente pesagem, sem valores", "Peso líquido 1.420 kg", "Bruto", "Tara", "Impureza", "Motorista", "Veículo". [BACKEND: A3] | O ticket de pesagem também. Eu dou o bruto e a tara, e ele calcula o líquido: mil quatrocentos e vinte quilos. |
| [ZOOM: "Ao confirmar, o ticket recebe número. Estoque e financeiro não mudam até a valorização."]; clique em "Finalizar ticket": aviso verde e "Abrir comprovante". [BACKEND: RPC `cato_confirm_weighing_ticket_action`] | Ticket só registra a pesagem. Estoque e financeiro só mudam quando ele for valorizado, lá na tela do ticket. Dá pra pedir o ticket com valores também, dizendo o preço de cada material. |
| Digita "Sobe 50 centavos o preço de compra do cobre mel e do cobre misto" e envia: cartão "Tabela de preços", "Reajuste em 2 materiais", "Cobre mel R$ 42,50 → R$ 43,00", "Cobre misto R$ 36,00 → R$ 36,50", "Confirme em até 10 minutos.". [BACKEND: A4] | E os preços. Peço pra subir cinquenta centavos na compra dos dois cobres, e o cartão mostra o preço de hoje e o novo, lado a lado. |
| Clique em "Sim, atualizar": aviso verde. [BACKEND: RPC `cato_confirm_price_action`] | Sim, atualizar. Vale pra um material, pra vários ou pra tabela inteira, em porcentagem ou em reais. Ele mexe só na tabela padrão. |

### cap09 · Contas, caixa e banco (FINANCEIRO) · novo
| Tela | Fala |
| --- | --- |
| Digita "Dá baixa na primeira parcela da Fundição Bandeira do Vale, recebi por Pix na Conta Principal" e envia: cartão com a faixa "Pagamento e recebimento", "Baixar conta", R$ 4.790,00, os fatos e "Confirmar baixa". [BACKEND: A5] | No financeiro, a mesma lógica. A Fundição pagou a primeira parcela, e eu peço a baixa: recebi por Pix, na Conta Principal. |
| Clique em "Confirmar baixa": "Conta baixada." e "Abrir comprovante" (abre os fatos). [BACKEND: RPC `cato_confirm_operation_action`] | Confirmar baixa, e a conta está baixada. |
| [ILUSTRAÇÃO: o sistema registra × o banco movimenta: de um lado um caderno com "baixa registrada", do outro o aplicativo do banco; uma seta riscada entre os dois] | Uma dica: o Cato registra no sistema. Ele não manda Pix nem movimenta a sua conta no banco. O dinheiro você movimenta no banco, e aqui fica o registro. |
| Digita "Abre o caixa com 1.500 reais": cartão "Abertura de caixa", "Abrir caixa", "Confirmar abertura"; confirma. [BACKEND: A6] | Dá pra abrir o caixa por aqui. Ele exige que você diga o valor contado, mesmo que seja zero. |
| Digita "Lança uma saída de 85 reais no caixa, gás da empilhadeira, categoria Combustível": cartão "Movimento de caixa", "Lançamento no caixa", "Confirmar lançamento"; confirma: "Lançamento no caixa registrado.". [BACKEND: A7] | Lançar uma saída, ou uma entrada, com o motivo e a categoria. Vale pro caixa e vale pra conta do banco. |
| Digita "Transfere 2.000 da Conta Secundária pra Conta Principal": cartão "Transferência entre contas", "Transferir valores", os saldos de cada conta antes e depois, "Confirmar transferência"; confirma. [BACKEND: A8] | Transferir entre contas, ou do banco pro caixa. O cartão mostra o saldo de cada conta antes e depois. |
| Digita "Fecha o caixa, contei 1.415": cartão "Fechamento de caixa", "Fechar caixa", a diferença zerada, "Confirmar fechamento" (não confirma: "Cancelar"). [BACKEND: A9] | E fechar o caixa: você diz quanto contou, e ele mostra a diferença pro que o sistema esperava, antes de você confirmar. |

### cap10 · Saldo de cliente e fornecedor (FINANCEIRO) · novo
| Tela | Fala |
| --- | --- |
| Digita "Abate 100 reais do saldo do Valdir Pereira, ele entregou uma bateria em troca": resposta "O saldo é de um cliente ou de um fornecedor?"; digita "fornecedor"; cartão "Valdir Pereira", "Movimentação no saldo", "Hoje: Ele te deve R$ 300,00.", "Ele ficará te devendo R$ 200,00.", "Não movimenta caixa nem banco.". [BACKEND: A10] | Com saldo de parceiro, tem dois pedidos diferentes. O primeiro é o acerto: o Valdir abateu cem reais do vale dele. |
| [ZOOM: as duas linhas do saldo e "Não movimenta caixa nem banco."]; clique em "Confirmar": "Saldo atualizado.". [BACKEND: RPC `cato_confirm_partner_balance_action`] | O cartão diz quem deve pra quem, hoje e depois. E avisa: esse acerto não mexe em caixa nem em banco. |
| Digita "Registra o recebimento de 1.000 reais do saldo da Aços Quiririm, por Pix na Conta Principal": cartão com a faixa "Saldo do parceiro", R$ 1.000,00, "Origem", "Destino", "Forma", "Data"; confirma. [BACKEND: A11] | O segundo é quando entrou dinheiro de verdade. A Aços Quiririm pagou mil reais do que devia. Aí o saldo dela cai e o dinheiro entra na conta. |
| [ILUSTRAÇÃO: acerto × pagamento: duas fichas de parceiro; na primeira só o saldo muda; na segunda o saldo muda e uma moeda cai na conta do banco] | Uma dica: acerto muda só o saldo. Pagamento ou recebimento muda o saldo e o dinheiro. Diga qual dos dois você quer. |

### cap11 · Cadastros e produção (AÇÕES) · novo
| Tela | Fala |
| --- | --- |
| Digita "Cadastra o fornecedor Sebastião Lima, telefone (12) 9 0000-0147": cartão "Novo parceiro", "Salvar cadastro"; confirma. [BACKEND: A12] | Fornecedor novo no balcão? Dá pra cadastrar pela conversa, com o nome e o que você souber dele. |
| Digita "Cadastra o material Chumbo, em kg, compra a 6,50 e venda a 8,00": cartão "Novo material", "Salvar cadastro"; confirma. [BACKEND: A13] | Material também: nome, unidade e, se quiser, os preços. O cadastro nasce sem estoque. |
| [ILUSTRAÇÃO: cria × altera: um cartão de cadastro com "novo" aceso; lápis e lixeira apagados] | Uma dica: ele cria cadastro novo. Editar ou excluir um cadastro que já existe continua na tela de cadastro. |
| Digita "Planeja uma ordem de produção de 500 kg de Fardo de alumínio pra amanhã": cartão "Planejamento da produção", "Planejar ordem de produção", "Criar ordem" (mostra, "Cancelar"). [BACKEND: A14] | E, pra quem usa a produção, ele planeja uma ordem a partir da ficha técnica e prepara a conversão de um material em outro. |

### cap12 · Fotos, planilhas e PDFs (ARQUIVOS) · novo
| Tela | Fala |
| --- | --- |
| Clique no clipe: "Escolher foto ou arquivo" e "Tirar foto"; escolhe `pesagem-cooperativa.jpg` (foto fictícia de um ticket de balança); a foto em "Arquivos para enviar"; envia sem texto. [BACKEND: tabela `cato_attachments`, bucket `cato-attachments`] | Em vez de digitar, você pode mandar o arquivo. Aqui no clipe: uma foto da pesagem, por exemplo. |
| Resposta: "Li os dados da pesagem. O que você quer fazer com eles? Você pode pedir um ticket de compra ou de venda."; digita "Ticket de compra da Cooperativa Recomeço"; cartão do ticket com "Arquivo usado" embaixo. [BACKEND: A15] | Ele lê a foto e pergunta o que fazer com aquilo. Eu peço o ticket, e o cartão vem preenchido com os pesos da foto, pra eu conferir. |
| [ILUSTRAÇÃO: um arquivo com uma ordem escrita dentro ("lance agora"); o Cato ignora a ordem e aponta pro cartão] | Uma dica: o arquivo sozinho não lança nada. Vale a mesma regra: ele prepara, você confere e confirma. |
| Anexa `tabela-fundicao.png` (print fictício de tabela de preços): "Li a tabela do anexo. Você quer consultar os preços ou preparar uma atualização?"; depois "Esses valores são preços de compra ou de venda?". [BACKEND: A16] | Com um print de tabela de preços, ele pergunta se você quer só consultar ou atualizar os seus preços, e se são de compra ou de venda. |
| [ILUSTRAÇÃO: os formatos: foto, PDF e planilha, com "até três por vez"; ao lado, uma foto borrada e o balão "manda uma mais nítida"] | Ele aceita foto, PDF e planilha, até três arquivos por vez. Planilha grande, mande só o pedaço que interessa. E se a foto estiver ruim, ele pede outra mais nítida em vez de chutar. |

### cap13 · Nota fiscal pelo Cato (FISCAL) · novo
| Tela | Fala |
| --- | --- |
| Em "Próximos passos" da venda do cap. 08, clique em "Preparar NF-e" (ou digita "Emite a nota da venda pra Serra Fina"): cartão com a faixa "Nota fiscal eletrônica", "Preparar NF-e", os fatos do pedido, "Ambiente: Produção". [BACKEND: A17] | Agora a nota fiscal. A venda pra Serra Fina já está lançada, então eu peço a nota desse pedido. |
| A câmera passa pelos fatos do cartão (destinatário, itens, valores). | Ele não pede pra digitar nada de novo. Busca no pedido o destinatário, os itens, os pesos e os valores, e usa a configuração fiscal da empresa. |
| Clique em "Visualizar prévia do DANFE": abre o PDF numa aba; [ZOOM: "PDF para revisão. Não transmite a nota."]; volta. | Antes de qualquer coisa, a prévia do DANFE. É um PDF só pra revisar: ainda não foi nada pra SEFAZ. |
| Clique em "Criar rascunho": o cartão vira "NF-e do pedido" com "Rascunho preparado", "Emitir NF-e", "Consultar situação" e "Visualizar prévia do DANFE". [BACKEND: RPC `cato_confirm_operation_action`] | Conferi a prévia: Criar rascunho. Repara que são duas confirmações. A primeira cria o rascunho. A nota só é enviada no segundo botão. |
| [ILUSTRAÇÃO: os três tempos da nota: "rascunho", "enviada pra SEFAZ", "autorizada", cada um com o seu botão ou estado] | Uma dica: rascunho, envio e autorização são três momentos. Nota autorizada é só depois da resposta da SEFAZ. |
| Clique em "Emitir NF-e": "Processando a solicitação de emissão…", depois "NF-e enviada para processamento na SEFAZ." e "Aguardando confirmação da SEFAZ". [BACKEND: edge `plugnotas-emit` simulada] | Emitir NF-e. Ele envia e fica acompanhando a resposta. |
| O estado muda: "NF-e autorizada", "A nota nº 1249 foi aprovada pela SEFAZ.", "O DANFE já está pronto para abrir."; clique em "Abrir DANFE" (PDF em aba nova); abre "Ver itens e tributos". | Autorizada. Aí aparece o botão Abrir DANFE, e dá pra ver os itens e os tributos da nota aqui mesmo. |
| [ILUSTRAÇÃO: o Cato com a nota de um lado; do outro, a tela de Notas Fiscais com "cancelar", "carta de correção", "nota avulsa"] | Uma dica: pelo Cato sai a nota de um pedido que já existe. Nota avulsa, cancelamento e carta de correção continuam na tela de Notas Fiscais. E a tributação quem define é o seu contador. |
| De volta ao cartão; cursor em "Consultar situação" e, na faixa de erro (não encenada), "Emitir novamente". | Se a SEFAZ recusar, o motivo aparece no cartão. Você corrige o cadastro ou a configuração e usa Emitir novamente. |

### cap14 · Acompanhar pedidos e rotinas (ROTINA) · novo
| Tela | Fala |
| --- | --- |
| "Mais opções do Cato" → "Acompanhar pedidos": "Continue de onde parou.", a compra da Aparecida e a venda da Serra Fina; abre a venda: "Pedido registrado → A receber: R$ 5.200,00", "NF-e autorizada", "Registrar recebimento", "Acompanhar NF-e". | Lembra dos três pontinhos? Em Acompanhar pedidos ficam os pedidos que você lançou pelo Cato, com o que falta em cada um: receber, pagar ou emitir a nota. |
| "Voltar à conversa"; menu → "Suas rotinas": "Ver sinais agora": "Estoque sem saída há pelo menos 30 dias", "Vencidas", "Vencem nos próximos 7 dias". [BACKEND: RPC `cato_routines_manage` `preview`] | Em Suas rotinas, o botão Ver sinais agora mostra o que merece atenção: material parado no pátio, conta vencida e conta pra vencer. |
| "Programar": "O que acompanhar" = "Contas a vencer e vencidas", "Frequência" = "Todo dia", "Horário" 08:00, liga "Receber este resumo", "Salvar agendamento": "Agendamento salvo". | E dá pra programar: todo dia, às oito, ele deixa um resumo das contas. O aviso chega aqui dentro do sistema, só pra você. |
| Menu → "Respostas revisadas": "Nenhuma resposta revisada", "Quando uma resposta precisar de complemento, ela aparece aqui.". | E se uma resposta antiga do Cato for corrigida depois, a correção aparece em Respostas revisadas. |

### cap15 · Limites e permissões (LIMITES) · novo (substitui o cap07 atual)
| Tela | Fala |
| --- | --- |
| Conversa; digita "O que você consegue fazer?" e envia: "O que consigo fazer no seu acesso agora", "1. Ações com sua confirmação", "2. Consultas", "3. Limites". [BACKEND: A18] | Na dúvida do que dá pra pedir, pergunte pra ele. A lista que ele mostra é a do seu usuário. |
| Corte: logado como Marcos Antunes; digita "Atualiza o preço de compra do cobre mel pra 43 reais": resposta de que ele não tem permissão pra mexer em preço e que um administrador pode fazer ou liberar. [BACKEND: A19; Marcos sem a permissão de editar material] | O Cato não dá poder a mais pra ninguém. O Marcos não pode mexer em preço na tela, então também não pode pelo Cato. |
| [ILUSTRAÇÃO: a mesma chave abre a tela e o Cato: uma permissão ligada às duas portas; a permissão é conferida duas vezes, no pedido e no clique] | Cada ação pede a mesma permissão da tela: registrar compra, dar baixa em conta, emitir nota. E ela é conferida de novo no clique do cartão. |
| "Usuários e Permissões", a restrição de ver só os próprios pedidos, com o trecho "o Cato fica indisponível para evitar exposição indireta". [ZOOM no trecho] | Uma dica: quem tem restrição de ver só os próprios cadastros, pedidos ou tíquetes, ou só algumas contas do banco, fica sem o Cato. É pra ele não mostrar o que a pessoa não pode ver. |
| [ILUSTRAÇÃO: o que fica nas telas: editar e excluir cadastro, ajustar estoque, cancelar nota, valorizar ticket, reabrir caixa; cada item acende com a fala] | E o que ele ainda não faz: editar ou excluir cadastro, ajustar estoque, cancelar nota, valorizar ticket e reabrir caixa. Nesses casos, ele explica o caminho na tela. |
| [ILUSTRAÇÃO atual: limites de uso] | (fala atual cap07, linha 4) Uma dica: o Cato tem um limite de perguntas por minuto e por dia. É um limite que protege o custo do serviço, não é castigo. Se ele pedir pra você esperar um minutinho, a espera resolve. |
| Rodapé "O Cato.ai pode cometer erros. Confira informações importantes.". | E continua valendo: ele pode errar. Por isso existe o cartão. Leia antes de confirmar. |

### cap16 · Avaliar e falar com o suporte (AJUDA)
| Tela | Fala |
| --- | --- |
| 👍 numa resposta; 👎 em outra → "Faltou detalhe". | (fala atual cap08, linhas 1 e 2) |
| A pesquisa de fim de conversa: "Sim", "Em parte", "Não", a nota de zero a dez, "Enviar avaliação". [BACKEND: o robô avança o relógio 3 minutos; RPC `submit_cato_resolution_feedback`] | Depois de um tempo parado, ele também pergunta se a conversa resolveu o que você precisava. Leva dois cliques. |
| "Mais opções do Cato" → "Falar com atendente": janela "Falar com o suporte". | E quando você precisar de uma pessoa de verdade, o caminho está nos três pontinhos: Falar com atendente. |
| A câmera passa pelos campos e para em "Falar no WhatsApp", sem clicar. | (fala atual cap08, linha 4) |

### cap17 · Recapitulando (RESUMO)
| Tela | Fala |
| --- | --- |
| Montagem: autorização, janela da memória. | Pronto! Recapitulando: a gente achou o Cato, autorizou o uso e ligou a memória, que é só sua. |
| Montagem: respostas, gráfico, tabela, "Total geral". | Fez as perguntas do dia a dia, viu quando vem gráfico e quando vem tabela, e conferiu um número na tela de origem. |
| Montagem: cartões de compra, venda, ticket e preço. | Pediu uma compra, uma venda, um ticket e um reajuste de preço, sempre conferindo o cartão antes de confirmar. |
| Montagem: baixa, caixa, saldo, foto, DANFE. | Baixou conta, mexeu no caixa, acertou saldo, mandou foto e emitiu a nota de um pedido, com a prévia do DANFE. |
| Montagem: resposta de capacidades, corte do Marcos. | E viu os limites: o Cato prepara, você confirma, e cada um só faz o que a sua permissão deixa. |
| Cartão "Próximo: Dashboard, Agenda e rotina". | No próximo tutorial, a gente olha a tela inicial e a rotina que mantém o sistema vivo. Até lá! |

### O que o mundo fictício precisa ter
- **Estado:** o do T21 atual (fim da T15), mais: configuração fiscal ativa com emitente e série 1 (última nota 1248, como
  no mundo base; a T21 não herda a T16), cadastro fiscal completo da Serra Fina (Itamonte, MG), 3 parcelas de R$ 4.790,00
  da Fundição em aberto, saldo a receber da Aços Quiririm R$ 2.870,00, vale do Valdir R$ 300,00, ficha técnica "Fardo de
  alumínio" (T11), ticket seguinte 58, Marcos sem editar material, memória com `personalDecision: "pending"` em `inicio`.
- **Arquivos fictícios (desenhados, sem dado real):** `pesagem-cooperativa.jpg` (ticket de balança: Cooperativa Recomeço,
  Plástico PET, bruto 1.480, tara 60) e `tabela-fundicao.png` (print de tabela de preços com 4 materiais do mundo).
- **Handlers novos no backend falso:** `cato_confirm_purchase_action`, `cato_confirm_sale_action`,
  `cato_confirm_weighing_ticket_action`, `cato_confirm_price_action`, `cato_confirm_partner_balance_action`,
  `cato_confirm_operation_action` (cada um devolve `executada` com o resumo e os ids, e grava de verdade no mundo:
  compra, venda, ticket, preço, baixa, lançamento, transferência, cadastro); `cato_order_journeys`;
  `cato_routines_manage` (`status`, `preview`, `save`); `cato_corrections_manage` (lista vazia);
  `cato_memory_manage` (`status`, `accept_personal_consent`, `list`, `save`, `set_enabled`);
  `get_my_cato_conversations`; `submit_cato_resolution_feedback`; tabela `cato_attachments` e bucket `cato-attachments`
  (enviar e assinar URL); edge `plugnotas-emit` e a consulta da nota (rascunho → processando → autorizada, com o PDF do
  DANFE fictício da T16); a prévia do DANFE (PDF fictício).
- **Respostas simuladas novas (A1 a A19):** `response_payload` com `action` no formato de `lib/cato/messages.ts`
  (`CatoPurchaseAction`, `CatoSaleAction`, `CatoWeighingTicketAction`, `CatoPriceAction`, `CatoBalanceAction`,
  `CatoOperationAction` com `subtype`, `title`, `facts`, `balances`, `confirm_label`, `environment`) e `expira_em` = agora
  + 10 min. Os textos de pergunta saem do código quando existem ("Foi em dinheiro, Pix ou transferência?", "O saldo é de
  um cliente ou de um fornecedor?", "Li os dados da pesagem…"); os demais são escritos no plano e marcados como simulados.
- **Conferir no ensaio (o código não deixou claro só pela leitura):** se a compra no Pix exige caixa aberto; de onde sai o
  saldo inicial do "Abrir caixa" pelo Cato (cofre ou não); o texto do selo de variação do cartão de preço quando o
  reajuste é em reais; título e rótulo de confirmar do cartão "Saldo do parceiro" (vêm do banco, montados na hora); o
  número do pedido seguinte no estado da aula.

## 4. Estimativa
- **Fala:** hoje 1.028 palavras (~6,6 min). Proposta: ~2.490 palavras (767 aproveitadas + ~1.720 novas; ~16 min a
  2,6 palavras/s). **Cerca de 565 s de fala a mais.** Vídeo final perto de 21 a 23 min, com as esperas das respostas, os
  cliques dos cartões e 17 vinhetas.
- **Capítulos:** de 10 para 18 (00 a 17). **10 novos** (03, 07 a 15), 2 fundidos (05 e 06 atuais viram um), 1 descartado
  (07 atual), 5 aproveitados quase inteiros.
- **Ilustrações:** 7 aproveitadas, 1 descartada ("consulta × executa"), 13 novas (a da abertura é refeita).

## 5. Depende de decisão
1. **Uma aula longa (~22 min) ou duas** ("Cato: perguntar", caps. 00 a 06, ~9 min; "Cato: pedir pra fazer", caps. 07 a
   17, ~13 min). Recomendo duas: a segunda depende de T7, T8, T13 e T16, a primeira não.
2. **Posição na trilha e o cartão "Antes":** hoje vem depois da T15; a parte de ações pede T7 (compra e venda), T8
   (ticket), T13 (contas) e T16 (NF-e) antes.
3. **Título:** "Cato, o assistente" ou "Cato, o agente de IA".
4. **Emissão de NF-e na tela:** encenar em "Produção" (como o cliente vê) ou "Homologação" (o cartão mostra
   "Homologação — sem valor fiscal"). Proposta: Produção, simulada.
5. **Mostrar o balão de dica** do botão (cap. 01) ou calar na semente.
6. **Produção e conversão** (cap. 11): manter o trecho de uma linha ou tirar, já que é módulo à parte.
7. **Rotinas** (cap. 14): os resumos agendados são recentes; confirmar se já estão liberados pra todos os clientes antes
   de prometer na fala.
