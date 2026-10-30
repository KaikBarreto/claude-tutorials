# T0 · Boas-vindas à Dominex (aula ilustrada)

Pedido do Kaik (30/10/2026 21:16 e 21:19): vídeo rápido de **2 a 4 minutos**, **sem tela de sistema**, só ilustrando
e explicando conceitos e combinados com o cliente. Prepara a pessoa para ser cliente e assistir aos demais tutoriais:
suporte pelo WhatsApp, mas os tutoriais são de suma importância para aproveitar o sistema; o **Guia Técnico**
(`dominex.app/guia-tecnico`), onde a pessoa vê e pesquisa por escrito como funciona cada coisa; onde fica a tela de
Assinatura; gestão do plano e upgrade; como funciona o proporcional (pró-rata) ao adicionar algo; como serão os
tutoriais e o que a pessoa vai aprender.

## Formato
- Identidade Domiflix completa (vinheta de abertura com o título, cartela, trilha seed 3, voz Fernanda, legendas).
- No lugar da gravação: **cenas ilustradas** desenhadas por código (como a ilustração do QR do T3), sobre o palco
  escuro, no tamanho da janela do app (painel claro 1587×992, cantos 16 px). Objetos genéricos, sem logo de terceiros
  (WhatsApp, Pix, bandeiras de cartão e navegador só como texto ou ícone genérico).
- 4 blocos com vinheta de capítulo falada + boas-vindas e fecho curtos. Duração estimada: **~3 min 40 s**
  (≈ 500 palavras; a Fernanda leu o T3 a 2,6 palavras/s → ~3 min 15 s de fala + 4 vinhetas + abertura e cartela).
  Se precisar encurtar, sai a linha do período de teste (~8 s).
- "Não invente telas": as cenas não imitam a tela do sistema; mostram o caminho por **texto e ícones**
  (ex.: cartão "Menu da sua conta" com os itens Assinatura, Tutoriais | Domiflix, Falar com o Suporte). Tudo que
  aparece escrito nas cenas é rótulo real (app ou Guia Técnico) ou conceito; nenhum valor em R$.

## Fatos confirmados (código 1.38.6 e página publicada)
| Fato | Fonte |
|---|---|
| Menu da conta (cartão com a foto no rodapé da barra lateral; no topo; no celular, gaveta Menu → Conta): **Perfil, Assinatura, Tema, Tutoriais \| Domiflix, Central de Ajuda, Falar com o Suporte** | `src/lib/i18n/messages/app/shell.ts:79-86`; `src/components/layout/SidebarMenuContent.tsx:521-526,633-657`; `TopNavbar.tsx:432-438,480-500`; `MoreMenuDrawer.tsx:374-395` |
| "Falar com o Suporte" abre o WhatsApp do suporte (`wa.me/<número da Dominex>`) | `SidebarMenuContent.tsx:209,651`; `TopNavbar.tsx:156,496` |
| **Central de Ajuda** = gaveta lateral de perguntas frequentes ("Dúvidas frequentes sobre o sistema. Caso não encontre sua resposta, entre em contato pelo Suporte via WhatsApp."). Não é o Guia Técnico | `src/components/layout/HelpCenterDrawer.tsx`; `settings.ts:1743-1746` |
| **Guia Técnico** (`dominex.app/guia-tecnico`, página pública): "Manual completo do produto" · "Guia Técnico" · "Como funciona cada função do sistema, tela por tela, na ordem da Trilha Domiflix."; sumário por fases (Deixar o sistema de pé · Os cadastros que sustentam tudo · A operação rodando · Vender · Contratos, PMOC e o cliente · O dinheiro e o fiscal · Gente e crescimento); busca **"Buscar no guia…"** (procura em títulos e parágrafos, lista os trechos com a palavra marcada e um clique leva ao trecho, que pisca em amarelo); botão **"Baixar o guia"** (PDF). Publicado: v1.37.36, atualizado em 22/10/2026 (conferido em 30/10) | `public/guia-tecnico/index.html` (cabeçalho, `#busca`, script da busca, `a.baixar`); `vite.config.ts:17`; `docs/guia-tecnico/CONTRATO.md:5-12` |
| O Guia Técnico **não tem link dentro do app logado** na 1.38.6 (só imagens dele são usadas na landing/login): o vídeo mostra e fala o endereço | busca por `guia-tecnico` em `src/` (só `LoginShowcase.tsx`, `HomeFeatures.tsx`, `HeroGalaxy.tsx`, imagens) |
| Tela **Assinatura** (`/assinatura`): status, Plano, Vencimento, Valor mensal, formas de pagamento (PIX, Boleto, Cartão), **Pagar Agora**, **Uso da conta**, cartão Sua Assinatura com **Gerenciar Meu Plano** e Cancelar assinatura, **Histórico de pagamentos** | `settings.ts:1195-1240,1381-1383`; `pages/Billing.tsx:50,367,398`; Guia Técnico T16 §1-3 (`docs/guia-tecnico/secoes/T16.html`) |
| Pagamento: Pix, Boleto ou Cartão; **anual com 20% de desconto só no Pix/Boleto**; no cartão a cobrança é mensal e renova sozinha ("Sua assinatura é renovada automaticamente no cartão cadastrado.") | `settings.ts:1212,1216-1217,1252-1253`; `components/checkout/CheckoutLayout.tsx:377-379`; Guia T16 §1 |
| **Gerenciar Meu Plano**: abas **Planos Prontos** e **Personalizado** (módulos + usuários adicionais), painel Seu Plano recalcula ao vivo | `settings.ts:1238,1242-1247`; Guia T16 §3-4 |
| **Período de teste**: todos os módulos liberados; ao ativar a assinatura, valem os do plano escolhido | `src/hooks/useCompanyModules.ts:135,204-229`; Guia T16 §5 "Como saber o que você já tem" |
| **Upgrade = proporcional** (plano mais caro, módulo pago, usuário extra, nível de NFS-e): paga hoje `(valor novo − valor atual) × fração do ciclo que falta`; o recurso novo só entra depois do pagamento confirmado; na renovação seguinte, valor cheio do plano novo. Faixa verde: "Upgrade: você paga apenas o ajuste proporcional e os recursos são liberados após a confirmação." Mensal → anual recomeça o ciclo e é só Pix/Boleto (fica fora do vídeo; o guia explica) | `supabase/functions/_shared/subscription-proration.ts:56-82`; `supabase/functions/change-subscription-plan/index.ts:18-24`; migração `20261014110000_subscription_upgrade_proration.sql:1-5,93-98`; `CheckoutLayout.tsx:370-374,417-424`; Guia T16 §3 |
| **Redução**: mantém o plano atual até o fim do período pago; o valor novo vale na próxima cobrança ("Downgrade agendado"; "Mudança de valor agendada") | `change-subscription-plan/index.ts:26-32,384-410`; `settings.ts:1213-1214`; Guia T16 §1,§3 |
| Base sempre inclusa: módulo básico, Portal do Cliente, Precificação Avançada (Orçamentos e Precificação), Perguntas em Vídeo | `change-subscription-plan/index.ts:15-16`; Guia T16 §4 |
| Trilha: uma aula por área, com capítulos; cada aula só usa o que já foi ensinado; ordem T0 → T2 → T3 → T4 → T5 → T7 → T18 → T8 → T9 → T10 → T11 → T12 → T13 → T19 → T20 → T14 → T15 → T22 → T21 → T17 | `docs/domiflix/trilha-de-tutoriais.md:5-10,24-50` |

## Roteiro (rascunho para aprovação) · Ilustração × Fala
Versão viva para o Kaik comentar: https://claude.ai/artifact/UQjsgSUXMRz34vCAh2qW3w (o doc vale sobre este resumo).

**Abertura (vinheta da aula)**: "Boas-vindas à Dominex".

**0 · Boas-vindas** (sem vinheta de capítulo)
- Ilustração: um círculo com 4 estações genéricas ligadas por setas: chamado do cliente → ordem de serviço → técnico
  em campo → dinheiro na conta.
- Fala: "Oi! Boas-vindas à Dominex. A partir de agora, a sua empresa tem um lugar só pra organizar o trabalho, do
  chamado do cliente até o dinheiro na conta. Neste vídeo rápido, eu te mostro como a gente vai caminhar junto."

**1 · Como funcionam os tutoriais** (vinheta: COMEÇANDO)
- Ilustração: uma trilha com as 7 fases (os mesmos nomes do sumário do Guia Técnico) acendendo junto com a fala;
  um cartão de aula com a lista de capítulos (títulos reais do T3); o cartão "Menu da sua conta" com
  "Tutoriais | Domiflix" em destaque.
- Fala: "Os tutoriais da Domiflix são o seu caminho pra dominar o sistema. Cada aula mostra uma área inteira, na
  prática, dividida em capítulos, pra você voltar direto no ponto que precisar. Eles seguem uma ordem, e cada aula
  aproveita o que você viu antes: primeiro a sua equipe e os cadastros, depois as ordens de serviço e o técnico em
  campo, e aí orçamentos, contratos, financeiro e por aí vai. Pra encontrar, é só abrir o menu da sua conta e clicar
  em Tutoriais Domiflix. E aqui vai o combinado mais importante: assiste aos tutoriais, na ordem. É neles que você
  descobre os recursos que fazem o sistema render de verdade no seu dia a dia."

**2 · Quando bater uma dúvida** (vinheta: AJUDA)
- Ilustração, em três momentos:
  1. o cartão de aula com um capítulo em destaque (voltar no ponto certo);
  2. um navegador genérico com o endereço **dominex.app/guia-tecnico**, o título "Guia Técnico" e o campo
     "Buscar no guia…"; a busca é digitada, aparecem os trechos com a palavra marcada e o trecho escolhido pisca em
     amarelo (busca e resultado **reais**: rodar a busca da página e copiar o primeiro resultado);
  3. o cartão "Menu da sua conta" com "Falar com o Suporte" em destaque e um celular genérico com balões de
     conversa (verde genérico, sem logo).
- Fala: "Bateu uma dúvida? Volta direto no capítulo daquele assunto. E se você preferir ler, tem o Guia Técnico,
  no endereço dominex ponto app barra guia técnico. Ali está cada função do sistema explicada por escrito, tela por
  tela, na mesma ordem dos tutoriais. É só digitar na busca o que você procura, e um clique te leva direto no trecho
  que explica. E sempre que precisar, o nosso suporte atende pelo WhatsApp: no menu da sua conta, é só clicar em
  Falar com o Suporte. Uma dica: quando você já assistiu à aula daquele assunto, a conversa fica bem mais rápida,
  porque a gente já parte do mesmo ponto."

**3 · A sua assinatura** (vinheta: ASSINATURA)
- Ilustração: o menu da conta com "Assinatura" em destaque; um cartão-resumo com Status, Plano, Vencimento e Valor
  mensal (tarjas no lugar dos valores), "Uso da conta", "Histórico de pagamentos"; três fichas de pagamento por
  texto: Pix, Boleto, Cartão; selo "Anual: 20% no Pix e no boleto".
- Fala: "Tudo sobre o seu plano fica na tela Assinatura, também no menu da sua conta. Ali você vê o status, o plano,
  o vencimento e o valor, acompanha o uso da conta e o histórico de pagamentos. Pra pagar, é só clicar em Pagar
  Agora: dá pra usar Pix, boleto ou cartão. No plano anual, o Pix e o boleto têm vinte por cento de desconto; no
  cartão, a cobrança é mensal e renova sozinha."

**4 · Quando a empresa cresce** (vinheta: ASSINATURA) · pró-rata
- Ilustração: peças de módulo todas acesas ("período de teste") e depois só as do plano; cartão "Gerenciar Meu
  Plano" com as abas "Planos Prontos" e "Personalizado" (módulos + usuários); uma linha do tempo do ciclo
  (início · hoje · vencimento): a parte que já passou em cinza, a que falta em verde; uma peça "+ módulo" entra e só a
  parte verde é cobrada ("diferença proporcional"); selo "liberado após a confirmação"; no vencimento seguinte, o
  valor do plano novo. Por fim, "reduzir": tudo continua até o vencimento e o valor menor entra no próximo ciclo.
- Fala: "No período de teste, todos os módulos ficam liberados pra você conhecer; ao ativar a assinatura, ficam
  os do plano que você escolheu. E quando a sua empresa crescer, o plano cresce junto. Em Gerenciar Meu Plano, você
  escolhe um dos Planos Prontos ou monta o seu no Personalizado, com os módulos e os usuários que precisar. E funciona
  assim: se você aumenta o plano no meio do caminho, paga hoje só a diferença, proporcional aos dias que faltam até o
  vencimento. Os recursos novos entram assim que o pagamento é confirmado, e a renovação seguinte já vem com o valor
  do plano novo. E se você reduzir, continua com tudo até o vencimento, e o valor menor começa no próximo ciclo."

**5 · Fecho** (sem vinheta)
- Ilustração: a trilha de novo, com a primeira fase acesa.
- Fala: "Pronto, agora você já sabe como a gente vai trabalhar junto. O próximo passo é colocar a sua equipe no
  sistema: no próximo tutorial, a gente cadastra os usuários e define o que cada um pode ver. Te vejo lá!"

**Cartela**: "Até a próxima aula!"

## Produção
- Cenas por código (PIL, 2× para anti-serrilhado, Montserrat, verde #00C597), sincronizadas às palavras da fala
  (`narracao/capNN.json`), no formato das ilustrações do editor (`illustrations` cobrindo a janela inteira).
- Sem gravação de robô: cada bloco vira um capítulo com vídeo "em branco" + ilustração na janela o tempo todo
  (aproveita palco, vinhetas, trilha, SFX e legendas do pipeline). Ferramenta pequena a criar: capítulo ilustrado
  sem gravação (vídeo e telemetria vazios).
- Narração: 6 nós no ElevenLabs (um por bloco) + nó de títulos (Como funcionam os tutoriais · Quando bater uma
  dúvida · A sua assinatura · Quando a empresa cresce).
- Pronúncias: testar num trecho curto "dominex ponto app barra guia técnico" (se a voz ler "app" errado, usar
  "ép" no texto do TTS); legenda com a grafia `dominex.app/guia-tecnico` (registrar em `trocas`). Pix, boleto,
  Domiflix e Dominex a voz já lê bem; o roteiro usa "proporcional" em vez de "pró-rata".

## Decisões para o Kaik
1. **Configurações da empresa** (identidade, White Label, Regional, Usabilidade, Origens, Atalhos, Aparência,
   Integrações) estavam no T0 antigo e ficam sem aula com o T0 novo. Proposta: um **T1 "Configurações da empresa"**
   (com tela, ~10 min) antes do T2. Se aprovado, o fecho do T0 aponta para ele.
2. **Central de Ajuda** (gaveta de perguntas frequentes no menu da conta): proposta deixar fora do vídeo; os
   caminhos citados são tutoriais, Guia Técnico e suporte.
3. Valores dos planos: o roteiro **não mostra preços** (mudam e podem ter promoção); só o desconto de 20% do anual.
4. Linha do período de teste (bloco 4): manter? Ajuda quem assiste ainda no teste a não estranhar módulos que
   "somem" ao ativar.

## Sugestões para o time da Dominex (não bloqueiam o vídeo)
- Colocar um link **"Guia Técnico"** dentro do app (menu da conta ou na Central de Ajuda). Se entrar antes da
  gravação, a fala muda para "no menu da sua conta" em vez do endereço.
- No sumário e no "Ir para…" do Guia Técnico publicado, três seções aparecem só com o código: **"T1 · T1"**,
  **"T6 · T6"** e **"T16 · T16"** (título faltando no menu; o texto das seções existe).
