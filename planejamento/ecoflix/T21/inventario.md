# Inventário · T21 · Cato, o assistente (EcoSistema 1.59.154)

Código lido (só leitura): `/home/claude/ecoflix/app-src-1.59.154/`. Caminhos relativos a `src/` (edge functions em
`supabase/functions/`). Desktop, logado como Rafael Nogueira (MASTER); um corte com Marcos Antunes (não administrador).

## Onde fica
- Botão redondo do Cato (`components/cato/CatoFab.tsx:94-164`), montado no `components/layout/AppLayout.tsx:525-537`
  em todas as telas logadas, **só quando** `companies.cato_enabled` = true **e** o usuário tem a permissão
  `action_use_cato` ("Usar o Cato (assistente de IA)", `config/routes.ts:296`); senão aparece o widget de suporte
  (`:278`). Computador: canto inferior direito; celular: inferior esquerdo, acima da barra de baixo (`CatoFab.tsx:119-123`).
- Rótulos do botão: "Abrir o Cato", "Fechar o Cato", "Cato está analisando", "Abrir nova resposta do Cato" (`:113`).
  Com o painel fechado: aviso "A resposta do Cato chegou" ("Abrir") ou "O Cato não conseguiu concluir a análise"
  ("Ver") (`:71-86`).
- Convite do beta (`components/cato/CatoInviteModal.tsx`, "Você foi convidado pra testar o Cato"): aparece uma vez por
  usuário (`profiles.cato_invite_seen_at`, `hooks/useCatoInvite.ts`). A aula não mostra: a semente marca como visto.

## Autorização de uso de IA · `components/cato/CatoAiConsentDialog.tsx`
- Sem aceite da versão vigente, clicar no botão abre este diálogo em vez do chat (`CatoFab.tsx:54-69,107-110`).
- "Antes da primeira conversa com o Cato" / "Leia rapidinho como ele trata os dados da sua empresa." (`:124-129`).
- Sete pontos (`:28-64`): "O Cato lê os dados da sua conta pra te responder: compras, vendas, estoque, saldos e contas.
  Isso inclui o nome dos seus clientes e fornecedores."; "... provedores de inteligência artificial contratados pela
  EcoSistema. Eles não usam os seus dados pra treinar os modelos deles."; microfone só quando você toca; "Ouvir a
  resposta também é só quando você pede ..."; a EcoSistema pode usar as conversas pra melhorar o assistente,
  anonimizando; "O Cato pode errar. Use como apoio e confira os números antes de decidir."; "Mudou de ideia? É só pedir
  pro suporte desligar o Cato quando quiser."
- "Ler os Termos de Uso completos" (`/termos`); "Seção 12" + "Inteligência Artificial (Cato) · versão 2.0" (o texto
  tem travessão: não ler).
- Administrador (`useCatoAiConsent.tsx:43-44`: role admin/company_admin ou preset full_access): "Agora não" e
  **"Entendi e autorizo"** → aviso "Cato autorizado" e o chat abre (`:84-96,160-188`).
- Outro usuário: **"Só o administrador da empresa pode autorizar o Cato. Peça pra ele abrir o Cato e concluir a
  autorização."** e "Entendi" (`:189-204`).
- Backend: `companies.ai_consent_at`, `ai_consent_version` (= `TERMS_VERSION` '2.0', `data/termsOfUse.ts:52`);
  RPC `accept_ai_terms(p_version)`.

## Painel do Cato · `components/cato/CatoChatPanel.tsx`
- Desktop: gaveta à direita, 400 px, por cima do app (abaixo de 1536 px de largura) (`:695-701`).
- Cabeçalho: logo "Cato.ai", "Agente de IA da EcoSistema"; sino ("Desligar o som do Cato"), "Expandir para tela
  cheia", "Fechar" (`:800-854`). Barra: "Conversas", "Nova", "Memória" (`:856-860`; a aula não usa).
- Começo: **"Oi, Rafael 👋"**, "Pergunte o que quiser sobre seu negócio" e 4 perguntas prontas (`:869-900`). As duas
  primeiras são fixas: "Como tá indo meu negócio esse mês?" e "Como tá meu caixa hoje?"; as outras dependem da tela
  (`lib/cato/starterPrompts.ts:73-107`): aberto em `/materiais`, vêm "Quanto tenho em estoque agora?" e "Qual material
  me deu mais faturamento?" (sem sorteio); em outra tela, duas sorteadas.
- Pergunta: balão à direita. Esperando: "Pensando…", "Buscando seus dados…", "Consultando…", "Analisando…",
  "Quase lá…" e "Pode fechar o Cato e continuar trabalhando. Eu aviso quando terminar." (`:135-141,1130-1145`).
- Resposta (`:903-1127`): em cima, "Consultei <fonte>" (`lib/cato/messages.ts:98-130`: "seu resumo financeiro",
  "suas compras e vendas", "seu estoque", "seu resumo bancário", "os saldos dos parceiros", "seu caixa", "a central de
  ajuda"...; ranking de parceiros não tem rótulo) e a linha de contexto "Período <início> – <fim> · Regime de
  competência · Atualizado às HH:MM" (`lib/cato/responsePresentation.ts:42-56`); o texto aparece digitando
  (negrito, listas); depois o gráfico (`CatoChart.tsx`: "pizza", "barra", "linha", com título) ou a tabela
  (`CatoTable.tsx`: título; coluna com "valor"/"saldo" vira R$, "Quantidade (kg)" vira "n kg").
- Linha de ações: botão do destino (`responsePresentation.ts:5-20`: "Abrir relatório financeiro", "Abrir caixa",
  "Abrir posição de estoque", "Abrir movimentações bancárias", "Abrir clientes e fornecedores"...; no computador navega
  e deixa o painel aberto, `:615-618`), "Copiar resposta", "Ouvir resposta", "Essa resposta ajudou?" (uma vez),
  👍 "Resposta útil", 👎 "Resposta não útil" (`:1001-1105`). Depois do 👎: "Número errado", "Não entendeu", "Faltou
  detalhe", "Resposta lenta", "Outro" (`:145-151,1111-1124`).
- Sugestões de próxima pergunta: até 3 pílulas acima do campo (`:1189-1211`).
- Campo "Pergunte ao Cato…", "Falar" (microfone), "Enviar"; rodapé "O Cato.ai pode cometer erros. Confira informações
  importantes.", **"Falar com atendente"** e "Cato.ai v1.0" (`:1223-1327`).
- A conversa fica guardada na sessão do navegador (`hooks/useCato.tsx:137-203`, chave `cato-conversation-v3`).

## Falar com atendente · `components/support/SupportTriageDialog.tsx`
- "Falar com o suporte", "Nos conte o que está acontecendo pra resolvermos mais rápido."; quadro "Ver os tutoriais
  resolve a maioria das dúvidas e ajuda a entender 100% o sistema." com "Ver vídeos" e "Ver artigos"; "Em qual
  tela/módulo? *" ("Buscar tela..."); "O que aconteceu? Descreva com detalhes *"; "Você já assistiu aos nossos tutoriais
  sobre isso? *" ("Sim"/"Não"); **"Falar no WhatsApp"** (abre o WhatsApp do suporte com empresa, usuário, e-mail, tela e
  descrição já escritos, `:228-251`). A aula não clica nele.

## Backend que a tela chama
- Pergunta: edge **`cato-background`** (corpo com `message`, `history`, `capabilities: ["acoes"]`, `context` com o
  `path`, `sessionId`, `companyScope`) → `{ jobId }`; a tela consulta **`cato_jobs`** (`status`, `response_payload`,
  `error_code`, `created_at`) a cada 1 s até `completed`/`failed` (4 min no máximo) (`hooks/useCato.tsx:308-394`).
- `response_payload`: `answer`, `toolsUsed`, `chart`, `table`, `images`, `action`, `context` (`period`, `regime`,
  `updatedAt`), `interactionId`, `budgetNotice`, `cacheHit` (`hooks/useCato.tsx:32-46`; tipos em `lib/cato/messages.ts`).
- Sugestões: edge **`cato-assist`** com `mode: "followups"` → `{ suggestions: [...] }` (`useCato.tsx:207-225`).
- 👍/👎: RPC `set_cato_feedback`; memória: RPC `cato_memory_manage('status')` (`hooks/useCatoMemory.ts`).
- Gate: `companies.cato_enabled`, `companies.ai_consent_*`, `profiles.cato_invite_seen_at`.

## Regras do Cato no servidor (o que a fala afirma)
- Limites (`supabase/functions/cato-assist/index.ts:81-118,397-454`; `_shared/cato/sessionEconomy.ts:8-9`): 20
  perguntas por minuto por usuário, 40 por minuto por empresa, 300 por dia por empresa e **40 por dia por usuário**
  (padrões; dá para mudar por variável de ambiente). Mensagens: "Você fez muitas perguntas em pouco tempo. Espera um
  minutinho e tenta de novo. 🙂", "Sua empresa fez muitas perguntas em pouco tempo...", "O Cato atingiu o limite de uso
  de hoje pra sua empresa...", "Você chegou ao limite de perguntas de hoje. Amanhã eu te atendo de novo! 🙂".
- "VOCÊ QUASE SÓ LÊ: não emite nota, não mexe em caixa/estoque" e "Recuse pedidos de criar, emitir, pagar ou apagar
  qualquer coisa" (`_shared/cato/systemPrompt.ts:67` e fim). Pedido de emitir nota, pagar, cadastrar, mexer no estoque
  ou no caixa vira resposta de orientação, com os passos para a pessoa fazer (`_shared/cato/capabilities.ts:11-34`,
  `cato-assist/index.ts:470-472,1359`). **Exceção:** com `capabilities: ["acoes"]` (a 1.59.154 manda) ele pode
  **propor** reajuste de preço da tabela padrão num cartão que a pessoa confirma ("Essa proposta é válida por 10
  minutos.", `components/cato/CatoActionCard.tsx`, RPC `cato_confirm_price_action`). A aula não mostra (a fonte não cita).
- "caixa" = as sessões de caixa do dia; mês ou período vai por `compras_vendas_mensais`, `resumo_financeiro` ou
  `materiais` (`systemPrompt.ts:36,42-43`; ferramenta `caixa`, `_shared/cato/tools.ts:276-289`).
- Saldo × movimento: "quanto o fulano me deve" = saldo em aberto (`saldos_parceiros`); "de quem mais comprei / pra
  quem mais vendi" = valor movimentado no período (`top_parceiros`) (`systemPrompt.ts`, regra "INTENÇÃO saldo ×
  movimento").
- Gráfico: distribuição → pizza, ranking → barra, evolução → linha, mesmo sem pedir; tabela quando pedem lista; sempre
  texto antes (`systemPrompt.ts:30,72-73`). "Sempre diga de onde veio o número" (`systemPrompt.ts`).

## Fonte × código (para o relatório)
- O Cato só aparece com a liberação da empresa (`cato_enabled`) e a permissão de uso; a fala diz "quando o Cato está
  liberado na sua conta".
- Limites: além dos três da fonte, há 40 perguntas por dia por usuário; os números podem ser trocados no servidor. A
  fala não diz os números.
- "Caixa só de dinheiro em espécie": a ferramenta de caixa soma também banco e saldo de parceiro das sessões do dia; o
  que vale é "caixa = o caixa de hoje". A fala usa isso.
- "Mexer em cadastro segue com você": vale para criar/editar/excluir cadastro; o reajuste de preço pode ser proposto
  pelo Cato e confirmado pela pessoa. A fala diz "emitir nota, pagar conta e cadastrar seguem com você".
