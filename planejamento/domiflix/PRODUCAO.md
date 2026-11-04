# Produção de todos os tutoriais Domiflix (pedido do Kaik, 30/10/2026 22:44)

> "agora com todas as instruções que te passei faça todos os tutoriais seguindo o molde do t3, só a introdução que é
> diferente. E se precisar depois eu ajusto detalhes, mas só pare com todos prontos agora, se possível tudo num mesmo
> ZIP todos na melhor qualidade pra eu baixar"

Molde: **T3** (`exemplos/dominex-t3/`, `perfis/domiflix/PERFIL.md`): robô no app real com Supabase falso e mundo
fictício Glacial Cold Brasil, voz Fernanda (eleven_v4), câmera v2 auditada, vinhetas faladas, trilha seed 3, legendas.
T0 é a aula ilustrada (`docs/09-aula-ilustrada.md`). Não parar para perguntar: decisões abertas seguem o padrão abaixo
e ficam listadas para o Kaik ajustar depois.

## Ordem de produção e situação
Etapas: L = levantamento · R = roteiro + `tts_textos.py` · V = voz gerada · Z = zip recebido e `proc.py` ·
B = backend falso (sementes + handlers) · G = gravação (robô) · E = edição (specs, câmera auditada, render) ·
F = montagem final + legendas + conferência · ok = no ZIP

| Aula | Título | L | R | V | Z | B | G | E | F |
|---|---|---|---|---|---|---|---|---|---|
| T0 | Boas-vindas à Dominex (ilustrada) | ok | ok | ok | ok | — | — | ok | ok (30/10 22:51, 3:25) · **v2 entregue 04/11 02:4x** (4:20,6, 16:9 + 9:16, -15,8 LUFS, SRT/VTT por versão; v1 em `t0/entrega_antiga`) |
| T1 | Configurações e identidade da empresa (+ cap. PWA pedido 04/11) | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 05:20, 11:58) · **v2 18:33** (pronúncia + logo com texto branco; 12:05; 1.38.6) · **remendo 1.38.19 entregue 04/11 12:2x** (12:09) |
| T2 | Usuários, cargos e permissões | ok | ok | ok (V3 18:3x) | ok (zip 5, 19:31) | agente novo 03/11 22:4x, 1.38.19 (54324): **ensaio ok 04/11 00:4x** (cap00–10, 0 falho; cap11 só montagem); **entregue 04/11 09:xx** (10:15, -15,8 LUFS, 181 legendas; recarregamento do "Criar Usuário" cortado com pausa na voz nos caps 05 e 06) | | | |
| T3 | Clientes, Fornecedores e Equipamentos | ok | ok | ok | ok | ok | ok | ok | **v2 entregue 03/11 22:4x** (14:13, 1.38.19, -15,8 LUFS; v1 de 30/10 em `t3/edit/out`) |
| T4 | Serviços, tarefas e checklists | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 10:46, 10:27) · **v2 18:37** (pronúncia; só o áudio) · **remendo 1.38.19 entregue 04/11 14:2x** (10:28; caps 01 a 08 e 14 novos) |
| T5 | Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 18:2x, 13:49; 1.38.6) · **remendo 1.38.19 entregue 04/11 12:2x** (13:56) |
| T7 | O técnico em campo (celular) | ok | ok | ok | ok (31/10 00:29; emenda do cap05 com folga 0,17 s) | ok (54321) | ok (1.38.19) | ok | ok (03/11 20:3x, 12:26; 1.38.19) |
| T18 | Área do Técnico: Refrigeração e Climatização | ok | ok | ok | ok (31/10 11:30) | ok (1.38.19, 54322) | ok | ok | **entregue 04/11 02:2x** (13:19, -15,8 LUFS, 208 legendas; zoom no cap00 depois da revisão) |
| T8 | Estoque, compras e inventário | ok | ok | ok (V3) | ok (zip 5, 19:50) | fase 1 ok 04/11 11:xx (16 caps, 0 falho) | ok (fase 2; atraso máximo 0,79 s) | ok (câmera 0) | **entregue 04/11 16:5x** (16:53, -15,8 LUFS) · pico corrigido 18:42 (-3,6 dBTP; vídeo idêntico) |
| T9 | Orçamentos, Precificação e Proposta | ok | ok | ok (V3) | ok (zip 5, 20:11) | fase 1 ok 04/11 11:xx (17 caps, 0 falho, falas × tela 0 diferença) | ok (atraso máx. 0,77 s) | ok (câmera 0) | aprovado 04/11 20:0x (16:38); falta trocar vinhetas 05 a 09 e entregar |
| T10 | CRM: funil, leads e captação | ok | ok | ok (04/11 17:xx) | | agente 04/11 15:4x (54328): backend, telas, robô provisório e ensaio | | | |
| T11 | Contratos e PMOC | ok | ok | ok (04/11 17:xx) | ok (zip 7, 15 caps, 15,5 min; 0 fala a refazer) | fase 1, agente 04/11 19:0x (54329) | | | |
| T12 | Portal do Cliente e Portal do Contrato | ok | ok | ok (V3) | ok (zip 5; títulos 20:4x) | agente novo 04/11 00:5x, 1.38.19 (54327): ensaio ok 03:2x; **aprovado 04/11 07:xx** (12:00; cap08 com faixa de endereço = defeito do app) | | | |
| T13 | Financeiro | ok | ok | ok (04/11 17:xx) | ok (zip 7, 15 caps, 14,0 min; 0 fala a refazer) | | | | |
| T19 | Integração com Asaas, Assinaturas e Cobranças | ok | ok | ok (04/11 17:xx) | ok (zip 7, 14 caps, 9,7 min; 0 fala a refazer) | | | | |
| T20 | Relatório Financeiro e DRE | ok | ok | ok (04/11 17:xx) | ok (zip 7, 13 caps, 8,7 min; 0 fala a refazer) | | | | |
| T14 | Notas Fiscais (NFS-e e NF-e) | ok | ok | ok (04/11 17:xx) | ok (zip 7, 14 caps, 8,3 min; 0 fala a refazer) | | | | |
| T15 | Funcionários: Financeiro do Funcionário e Ponto | ok | ok | ok (04/11 17:xx) | ok (zip 7, 13 caps, 8,9 min; 0 fala a refazer) | | | | |
| T22 | Ferramentas de RH: DISC, Organograma, Fluxograma | ok | ok | ok (04/11 17:xx) | ok (zip 7, 12 caps, 7,5 min; 0 fala a refazer) | | | | |
| T21 | Integração com WhatsApp | ok | ok | ok (04/11 17:xx) | ok (zip 7, 11 caps, 5,9 min; 0 fala a refazer) | | | | |
| T17 | Dashboard, relatórios e exportações | ok | ok | ok (04/11 17:xx) | ok (zip 7, 12 caps, 6,0 min; 0 fala a refazer) | | | | |

Ordem (TRILHA.md): T0 → T1 → T4 → T5 → T7 → T18 → T2 → T8 → T9 → T12 → T13 → T20 → T10 → T11 → T15 → T22 → T19 →
T21 → T14 → T17. O mundo fictício segue a ordem de **exibição** (cada aula parte do estado final da anterior).

## Como cada aula é feita (molde T3)
1. **R**: `planejamento/domiflix/Tnn/roteiro.md` (Tela × Fala por capítulo, estilo `exemplos/dominex-t3/roteiro.md` e
   `estilo_narracao.md`) + `$TUT_HOME/tnn/narracao/tts_textos.py` (`CAPS`, `TITULOS`, `KICKERS`) + `config_narracao.json`.
2. **V**: o fluxo ElevenLabs único (todas as aulas), nós rotulados `Tnn capMM <título>` e `Tnn títulos` (1 versão por fala, pedido do Kaik).
   O Kaik exporta o zip do fluxo; `proc.py` por aula (`recebido_<hhmm>/Tnn*`), `titulos.py`.
3. **B**: `rec/fakebase/seeds-extra/tnn/` + handlers que faltam (lista no `plano.md` → "Gravação").
4. **G**: `rec/tnn/capMM.json` (passos com `label`, `at` pelos tempos do `capMM.json`), gravação um capítulo por vez sob
   `.heavy.lock`; aceite: 0 passo falho, `lateBy` < 0,8 s, sem dado real.
5. **E**: `edit/caps/specs.json` → `montar_cap.py` → `auditar_camera.py` (0 problema) → `render_chapter.py`.
6. **F**: `finish.py` → `legendas_aula.py` → `entregar.py`; vídeo completo 1080p + .srt + .vtt.
7. Limpeza de disco: depois do F, apagar gravações, renders de capítulo e `proj/` da aula (fica o final + legendas).

## Ambiente de gravação (antes da primeira gravação nova)
- App de gravação em `$TUT_HOME/app` **atualizado para a 1.38.6** em 30/10 22:55 (`DOMINEX_SRC=src-1.38.6
  rec/setup-app.sh` + `rec/run.sh build`; dependências iguais). Fumaça ok (0 problema). Antes de cada gravação, conferir
  se saiu versão nova (`git fetch` no clone, só leitura) e repetir.
  **31/10 18:07: app de gravação na 1.38.9** (feito pelo agente do T3 v2, sob a trava; schema do backend falso com
  as tabelas e RPCs de etiquetas e campos). O dist da 1.38.6 ficou em `rec/.runtime/dist-1.38.6.bak`. T1 (cap05, 06
  e 13 regravados) e T5 ficaram na 1.38.6; T3 v2, T7 e as seguintes gravam na 1.38.9.
  31/10 05:3x: saiu a **1.38.7** (só painel admin: `update-company`, permissão de um vendedor, changelog); nenhuma tela
  das aulas muda, então a gravação segue na 1.38.6. Atualizar quando sair versão que mexa em tela de aula.
- Data do mundo: exportar o **mesmo `FAKE_NOW`** para o backend falso (`rec/run.sh fake`/`up`) e para o robô (o
  navegador instala o relógio nessa data: `recorder/browser.mjs`, testado 30/10). Datas diferentes = a assinatura da
  empresa fictícia (`@now+23d`) aparece vencida e o app mostra a tela de bloqueio com preço.
- Robô da área de trabalho **unificado com o da skill** (30/10 23:0x; o antigo em `rec/_antes_skill/`): máscara de senha,
  modo URL, `$VAR`. Validado regravando o T3 cap04: 23 passos, 0 falho, `lateBy` máx 0,29 s.
- Robô ainda sem: nova aba (PDF, link público), download, página sem login por capítulo, endereço com nome de produto
  nos links, celular (T7). Fazer antes das aulas que precisam (ver cada `plano.md`).

## Decisões abertas: padrão adotado (o Kaik ajusta depois)
- Recomendação de cada `plano.md` → "Riscos e decisões" vale como decidida, salvo o que está abaixo.
- Integrações externas (Asaas, NFS-e/NF-e, WhatsApp, mapa): só simuladas no backend falso, telas fiéis ao código.
- Notas fiscais (T14): ambiente de **homologação**, PDF com "SEM VALOR FISCAL"; empresa Glacial Cold Brasil (escolha
  do Kaik) com CNPJ fictício válido.
- Aulas longas (T11 ~17 min): uma aula só, como manda a trilha (1 tutorial por área).
- T7 e telas de técnico: celular genérico no palco (sem marca), toque marcado, mesma câmera.
- T2: lista começa só com a Camila; Rafael e Tatiane criados na aula, os outros técnicos entram num corte.
- Portal (T12): mostrar a configuração da senha, sem demonstrar o login protegido; página pública gravada sem login.
- Endereço do app nos links: nome de produto mapeado para a máquina local (sem rede).
- Datas: navegador e backend falso congelados na mesma data (`FAKE_NOW`), mês seguinte ao da gravação quando o PMOC
  precisar de visitas futuras.
- **Sem tarja** (Kaik 03/11 20:16: "não precisa botar tarja preta cobrindo nada inclusive faturamento, são dados mock"; e,
  perguntado, "Mostrar tudo"): faturamento, valores e os preços de plano do catálogo (R$ 197, R$ 547...) aparecem na tela
  como estão. A fala e as ilustrações seguem sem citar preço de plano. Substitui o antigo "sem preço de plano em nenhum vídeo".
- **T19 × T1 (Asaas):** o T19 parte sem a conta Asaas para mostrar a ativação, embora o cap11 do T1 mostre o cartão
  "Ativo"; a fala do T19 avisa "se na sua empresa a integração já está ativa, pode pular". Alternativa, se o Kaik
  preferir continuidade exata: regravar o cap11 do T1 com a integração desligada.

## Alinhamentos entre aulas (valem por cima dos roteiros)
- **Links do app na tela** (31/10 20:5x): o app monta link público com `window.location.origin`, e na gravação aparecia
  `http://127.0.0.1:8080/...` (T12: Link do portal e link da unidade). Origem real do app: `https://www.dominex.app`
  (`src/lib/indexNow.ts:3`). O agente do T12 está pondo no gravador a opção `APP_ORIGIN` (desligada por padrão; o navegador
  abre o app na origem real e o `page.route` serve o app local; chamadas externas abortadas). Toda aula que mostra link
  público (T9 proposta, T12 portal, T15 ponto, T19 cobrança...) grava com ela.
- **Financeiro padrão do cadastro** (contas Caixa e Conta Principal, 14 categorias padrão + 14 do sistema; detalhe em
  `MUNDO_FICTICIO.md` → Base): nas sementes de toda aula a partir da primeira que abre o Financeiro (T8/T9). O T11 já
  conta com eles; o T13, o T19 e o T20 foram revistos para isso (31/10 05:3x).
- **T9:** "Primeiro vencimento" das 3 parcelas do Orçamento #2 = **20/11/2026** (o T13 parte delas: 20/11, 20/12, 20/01).
- **FAKE_NOW `2026-11-10T10:00:00-03:00`** em T11, T12, T13, T19, T20 e T14 (fatura do cartão fechada no dia 5,
  mensalidades do PMOC a partir de 10/12 ainda futuras).
- **T9 → T15:** os funcionários que o T9 semeia para a calculadora de mão de obra entram só com o custo mensal
  (`monthly_cost`) e salário 0; o T15 completa os salários num corte (com salário, o cron criaria folhas que o T13 não
  mostra em Contas a Pagar).
- **Dashboard (toda aula que o mostra):** OS de hoje ainda aberta aparece "Atrasada 0 dias" e os gráficos deslocam um dia
  (bug de fuso, `src/pages/Dashboard.tsx:169,193,221`; T17 P2). Nas sementes, nenhuma OS do dia aberta no momento da
  gravação, ou a câmera não enquadra "Requer Atenção".
- **T7 → T8:** Fita isolante com 28 no estoque (o roteiro do T8 e o T7 batem; o `plano.md` do T8 dizia 29).
- **T22:** o robô nunca pousa o cursor no gráfico DISC (o tooltip cita pessoas reais; T22 P6).
- **T19:** o handler `tenant-asaas-card-fees` (criado no T1) responde sem a franquia do Pix (`freeCount 0`): estender por
  semente ou parâmetro, sem reescrever o do T1.
- **Catálogo do plano (Gerenciar Meu Plano → Personalizado, 1.38.19):** a aba só calcula preço com `subscription_modules`
  completo: `basic` > 0; `customer_portal`, `finance_advanced`, `pricing_advanced` e `video_questions` com preço 0;
  `extra_user` > 0; `whatsapp_tiers` respondendo (`src/components/billing/ModulesManagementCard.tsx:186-199`). Faltando um,
  aparece "Não foi possível validar o catálogo de preços", "preço indisponível" e R$ 0,00 (T0 v2 cap05, 04/11). Aula que
  mostra essa tela (T13, T17, T20) parte do `seeds-extra/t0v2/catalogo.json` corrigido, com preços das migrations.
- **Trilha Domiflix (G1 do `IMPACTO_1.38.19.md`):** toda aula depois do T0 semeia `domiflix_learning_paths`
  `tutoriais-do-sistema` com `is_onboarding: false`, como `seeds-extra/t2/inicio.json`; sem isso a tela escura de introdução
  ou a faixa de lembrete aparecem (a base `gen-03-domiflix.json` está com `true`, que só o T0 v2 usa).

## Retomada (03/11 16:3x)
- 31/10 21:0x: o limite semanal do Kaik acabou e os US$ 90 de créditos foram gastos em < 20 min (9 agentes em paralelo +
  a conversa principal). Tudo parou; a máquina reiniciou e os arquivos ficaram. **Regra nova: no máximo 3 agentes**, briefs
  curtos, nada de consulta em laço (a máquina só grava/renderiza um capítulo por vez; agente a mais só gasta).
- Kaik 03/11 16:33: continuar; revisitar aulas cujas telas mudaram ("principalmente a partir de orçamento, precificação,
  custos dos serviços"); fazer o T0 obrigatório (vertical também). **App de gravação na 1.38.19** (main `24f499ba`,
  `src-1.38.19`; dist da 1.38.9 em `rec/.runtime/dist-1.38.9.bak`). Toda gravação nova é na 1.38.19.
- Decisões do T0 v2 (Kaik 16:4x): D8 frases dele letra por letra (imagem destaca o rótulo real); D7 sem aviso para
  técnicos; D3 conta **em teste** ("Escolher meu plano", sem preço); D4 sem treinamento ao vivo; D1, D2, D5, D6 como
  propostos. Conferência na 1.38.19 (agente do T0): em teste os módulos fora do plano mostram o selo azul "LIBERADO NO
  TESTE"; para mostrar o vermelho pedido pelo Kaik, R04/R05 são gravadas com a conta contratada (o resto em teste). Cena 04
  reescrita para ser exata ("Se você confirmar ainda no teste, essa confirmação continua valendo quando contratar..."): em
  teste a introdução tem "Pular por agora", e quem contrata sem confirmar volta a ter o vídeo obrigatório. O botão de
  contratar ainda abre `/billing` (erro C5): a cena para no clique.
- **Voz do T0 v2 gerada 16:47** (fluxo único, nós `T00v2 cap00/01/02/03/06` + `T00v2 títulos`, 1 versão cada, 2.471
  créditos; ids em `scratchpad/t0v2_nos.json`): 28,3 + 44,1 + 29,7 + 36,8 + 19,6 s; cap04/cap05 e 4 títulos reaproveitam o
  T0 atual. Aguardando o Kaik exportar o fluxo (zip 6).
- Prévia do visual vertical (20 s) enviada ao Kaik 16:4x.
- **Impacto da 1.38.19** (`IMPACTO_1.38.19.md`, 17:1x): entregues T1 (Integrações ganhou a 4ª subaba "Impressora fiscal";
  2 falas), T4 ("Novo Tipo" virou "Novo Serviço"; 2 falas) e **T5 (assistente da Nova OS refeito, sem a etapa
  "Orçamento"; 5 falas)**; com voz: **T9 (assistente de 5 → 3 etapas; 8 falas; desconto do exemplo passa a R$ 85,00 para o
  total seguir R$ 1.000,00)** e T8 ("Estoque geral" e compras em lista; 2 + 3 leves); sem voz: T11 (contrato 6/7 → 5
  etapas; 11 + 1), T13 (2), T15 (aba "Acesso"; 2 + 1); T14 e T17 só robô; **T2, T3 v2, T7, T10, T12, T18–T22 sem mudança
  visível**. Backend falso: schema da 1.38.19, BDI, NPS vazio e **semente base com a introdução da DomiFlix concluída**
  (sem ela a 1.38.19 abre com a tela escura da introdução em toda aula).
- Plano: (1) T0 v2 (telas + ilustrações, montagem depois do zip 6); (2) backend 1.38.19 (agente); (3) falas novas de T9,
  T8, T5, T4, T1 e roteiros de T11/T13/T15 (agente), voz delas num lote; (4) gravações na 1.38.19, uma aula por vez na
  ordem T7 → T3 v2 (toda na 1.38.19) → T18 → T2 → T12 → T8 → T9; (5) remendos das entregues (T5 capítulos da OS; T4 e T1
  trechos), com `remendar_aula.py`.
- 17:3x **Backend falso na 1.38.19** (agente): schema regerado (258 tabelas, 381 RPCs; o anterior em `schema.json.1.38.9`),
  BDI (`quotes.use_bdi`, padrões de OS e itens), `sync_service_order_budget` com `p_pricing`, `generate_service_order_from_quote`
  copiando o BDI, NPS e avisos vazios; semente base `seeds/gen-03-domiflix.json` (agente do T0) com a introdução concluída
  para os 7 usuários base. Fumaça ok (Dashboard, Clientes, Nova OS, Novo Orçamento, Estoque, Compras, Financeiro).
  Pendente: sincronizar com a cópia da skill (`ferramentas/rec/fakebase`) no fim.
- 17:3x T7 retomado (mesmo agente): regravar tudo na 1.38.19 e entregar.
- 17:1x **Falas da 1.38.19 reescritas** (agente de roteiro): T9 12 trocas (1.324 caracteres; total segue R$ 1.000,00 com
  desconto R$ 85,00), T8 5, T5 6 (regravar cap02, 03, 04 só tela, 05, 06), T4 2 (+ as 2 do "Glaciál"; regravar cap01 e
  cap03), T1 2 (regravar cap11); roteiros de T11, T13, T15 (e anotações de T14/T17) atualizados. Pronúncia ajustada por
  mim: "á-pê-í Pública" (T1) e "Custo por quilômetro mais bê-dê-i" (T9). `trocas_1.38.19.json` em `tN/narracao/`.
- 17:17 **Voz das falas da 1.38.19 gerada** (nós `T01/T04/T05/T08/T09 emendas 1.38.19`, 3.180 créditos; ids em
  `scratchpad/emendas_1_38_19_nos.json`). Saldo ElevenLabs estimado ~3,2 mil. Entra no mesmo zip 6 do Kaik.
- 17:23 Kaik: "nessas vinhetas de início e fim não precisa ter o logo da domiflix E o logo da dominex, só o da dominex tá
  bom". Feito no T0 v2: vertical sem o logo DomiFlix; no 16:9, opção `brand_clips.sh --sem-domiflix` (ou `"sem_domiflix":
  true` no JSON da aula), padrão desligado (as outras aulas seguem com o "▶ DOMIFLIX" em texto; identidade IDÊNTICA).
  Prévia refeita enviada.
- 17:33 Kaik mandou só os 11 MP3 novos (a exportação inteira do fluxo vinha de cópia antiga, idêntica à de 31/10).
  Emendas de T1, T4, T5, T8, T9 rodando (`scratchpad/emendas_1_38_19.sh`); T0 v2: agente processando em `t0v2/narracao`.
- 18:2x Emendas aplicadas; 5 falas apertadas (T1 cap11, T4 cap01, T5 cap02, T8 cap04 cortada, T9 cap09 cortada) refeitas
  com `"empurra": true` (2ª passada, `scratchpad/emendas_1_38_19_b.sh`). T0 v2: voz processada (~4:10), 31 de 36 telas
  gravadas (computador e celular; R04/R05/R16–R18 em conta contratada), 15 ilustrações nas duas proporções; faltam R16–R18
  com tarja, "20% de desconto" no R17 e histórico de pagamentos no R16, render e montagem (prévia do cap01 antes).
- Agentes: levantamento do impacto da 1.38.19 (`IMPACTO_1.38.19.md`), telas e ilustrações do T0 v2 (porta 54328),
  pipeline vertical (retomado). As gravações (T2, T3 v2, T7, T8, T9, T12, T18) esperam o levantamento.
- 18:5x 2ª passada das emendas: T1 cap11 com folga 0,20/0,21 s (empurrada); T4, T5, T8, T9 na fila da trava. T0 v2: 20%
  de desconto só com ciclo anual (`Billing.tsx:333`, semente `conta-anual` no R17); R16 com 3 pagamentos; C5 confirmado
  (404). **cap01 16:9 gravado com 64,8 s para 44,1 s de voz** (aula carregando devagar): regravando sem a espera. O
  `render_chapter_vertical.py` só aceitava quadro pronto: o agente do vertical está fazendo a câmera da tela do celular
  (recorte ~2,4×, sem moldura, conteúdo até y 1420). T3 v2: falta o cap05 final. T7: renders dos capítulos na fila.
  4 agentes ativos (T0, T7, T3 v2, vertical); nada novo até um deles fechar.
- 19:0x Kaik: "não tem como gravar ou renderizar em paralelo?". Gravação continua sozinha (2 núcleos; com render junto o
  robô atrasa até 13 s). **Render em partes** (`render_chapter.py`, padrão 2 processos, 4 trechos com corte fora de aviso,
  destaque, ilustração e título): ~1,4× mais rápido, 598 de 600 quadros idênticos sem perda; instalado em 22 aulas às 19:5x
  (o T3 antigo ficou como estava). Falta o mesmo no `render_chapter_vertical.py`.
- 19:3x Vertical: `render_chapter_vertical.py` aceita a gravação do celular (agente do vertical concluído); falta o specs
  do celular do T0 v2 (agente do T0). Emendas da 1.38.19: T1, T4, T5, T8 com folgas ≥ 0,20 s; T9 (uma folga de 0,18 s, sem
  corte) terminando o `proc.py`.
- 20:0x **Prévia do cap01 do T0 v2 (16:9) enviada ao Kaik** (`t0v2/edit/out/cap01/cap01_previa.mp4`, 44,9 s; gravação 45,7 s
  para 44,08 s de voz, maior atraso 1,2 s num passo sem rótulo, câmera com 0 problema). Pergunta: as bolinhas da ilustração
  (uma por aula) ficam? Celular: regravando o cap01-p sem os ~6 s de hover (manter o anel nos toques "Ver trilha" e "Menu").
  Emendas: o `tts_textos.py` da área de trabalho de T1/T4/T5/T8/T9 era o anterior à 1.38.19 (legenda e linhas do
  `capNN.json` sairiam com o texto antigo); trocado pelo do planejamento e `proc.py` refeito (`scratchpad/emendas_texto.sh`).
- 20:16 Kaik sobre a prévia: "ficou ótimo mas não precisa botar tarja preta cobrindo nada inclusive faturamento, são dados
  mock"; perguntado sobre os preços de plano (são os do catálogo real), "Mostrar tudo". Regra nova em "Alinhamentos".
- 20:3x **T7 entregue** (`Domiflix T7 - O técnico em campo`, 12:26, -15,8 LUFS, 14 capítulos, câmera 0 problema; handoffs em
  `rec/t7/HANDOFFS.md`; para o T8: Fita isolante 28 e consumo de 2 rolos; P23 não conferido na 1.38.19). `overlay.py` (avisos
  ao lado do celular) e `montar_cap.py` (celular, `repouso`, `TUT_REC`) do T7 levados para a skill. Emendas da 1.38.19 com o
  texto novo: semelhança 0,80 a 1,00 (o resto é número lido pelo ASR). Agentes agora: T3 v2, T0 v2 (novo, contexto do
  anterior acabou; segue cap01 sem tarja, cap02–06, montagem e entrega) e T18 (novo).
- 20:27–21:15 **trava presa por um teste meu** (flock dentro de flock; lição em `docs/08`): máquina parada 47 min. O agente do
  T3 v2 achou; encerrado pelo PID. `identidade_domiflix.sh` IDÊNTICO com o `overlay.py`/`montar_cap.py` do T7 na skill.
  T3 v2: 14 capítulos gravados na 1.38.19 e auditados; renders, finish e entrega em andamento. T7 conferido na folha de quadros.
- 22:2x `recorte_celular.sh` OK com as ferramentas do T7 (celular: pior erro de cobertura 0,004; 16:9: 50 de 50 quadros
  idênticos ao código antigo). T3 v2: 14 capítulos renderizados, `aula_final.mp4` pronto (22:22), revisão minha antes da
  entrega. T18: ensaio rápido dos 16 capítulos ok (cap07 e cap14 corrigidos no `gerar.py`: botão por substring e galão por
  `role=img`); segue para a gravação. T0 v2: regravando cap02-p, cap03 e cap06-p sem tarja.
- 22:38 Kaik: "avance". T3 v2 revisado e aprovado (folha de quadros: vinheta, cartões de capítulo, telas sem tarja, cartela);
  o agente estava parado 16 min num laço `pgrep -f` que achava a si mesmo (lição em `docs/08`), encerrado pelo PID; segue
  legendas e entrega. **T2 despachado** (porta 54324, 1.38.19): fase 1 = preparo e ensaio rápido; gravação real só depois
  do T0 v2, que tem prioridade na trava.
- 22:4x **T3 v2 entregue** em `entrega_final/` (MP4, SRT e VTT; 242 legendas; 0 falho, maior atraso 0,44 s). Ponto
  conhecido: no cap10 (10:24 do vídeo) o clique na aba Categorias cai com a aba 67% visível na borda enquanto a câmera se
  afasta (meio segundo); a gravação bruta já foi limpa, refazer = regravar o cap10. Fica como está salvo pedido do Kaik.
- 04/11 00:0x **T0 v2 montado** nas duas proporções (4:20,6; mesma linha do tempo; -15,8 LUFS; câmera 0 problema) e posto
  em `entrega_final/` pelo agente antes da minha revisão; o T0 antigo foi para `t0/entrega_antiga`. A revisão do vídeo
  inteiro (folha de 2 s, dois formatos) achou: (1) cap05, aba Personalizado com erro do app ("Não foi possível validar o
  catálogo de preços", "preço indisponível", R$ 0,00) por ~3 s, causado pelo catálogo da semente sem `finance_advanced` e
  `extra_user`; (2) cap03, volta do Guia Técnico recarrega o app (spinner ~3,5 s + quadro escuro), com o aviso do endereço
  por cima; (3) cap05, cartão vazio de 2 a 3,6 s entre duas cenas; (4) abertura com 6,6 s de cartão vazio só com o título.
  Devolvido ao mesmo agente: catálogo com preços das migrations, pausa + `cortes` no cap03, regravação de cap03 e cap05
  nos dois formatos. Ainda não foi ao Kaik.
- 04/11 00:1x o T2 semeou por engano a 54321 (do T7, entregue; ninguém gravava nela): desligadas a 54321 e a 54323 (T3 v2,
  entregue). 00:28 Kaik: "avance". Fila sem mudança e sem 4º agente (regra de 3): T0 v2 corrigindo com prioridade, T18
  renderizando, T2 grava depois do T0 v2; a vaga do T0 v2 vai para o T12 (preparo de 31/10 em `rec/t12/ESTADO.md`).
- 04/11 01:4x T0 v2 com os 4 ajustes entregue por cima. Aprovados: cap03 (pausa de 3,6 s + `cortes` 30,4–33,95 nos dois
  formatos), cartão vazio do cap05, abertura do cap00. **Recusado o cap05**: para a faixa de redução sumir o agente baixou a
  conta para R$ 357 só no cap05 (semente `conta-cap05`), e a tela mostrava "Plano Avançado" a R$ 357/mês com renovação de
  R$ 547 embaixo e R$ 547 no cap04. Refazendo: conta em R$ 547 e, na aba Personalizado, módulos e usuários marcados com a
  fala até o total passar de R$ 547 (aumento, como diz a fala). Disco a 2,9 GB: apagados renders e `video_sem_audio` do
  T3 v1 e `src-1.38.11` (3,4 GB livres). T2 com ensaio ok, parado até a vez; T12 despachado (fase 1).
- 04/11 01:56 **container reiniciou**: pararam o T12 (fase 1), o finish do T18 e a cadeia do cap05 do T0 v2; todos os
  backends caíram. App religado (novo `rec/run.sh app`, só o 8080); a 54321 fica desligada de propósito. Os três agentes
  retomados com a ordem de religar a própria porta e refazer o que ficou pela metade. T2 segue parado (religa a 54324 na vez).
- 04/11 02:2x **T18 entregue** (13:19). Revisão do vídeo inteiro: sem erro do app; só a abertura parada 32 s, resolvida
  com 2 zooms no cap00. Stems e `music.wav` do T18 apagados (1,1 GB; o `remendar_aula.py` só usa o `mix.wav`): 5,2 GB
  livres. T2 liberado para gravar (divide a trava com o T0 v2, que tem prioridade, e com o ensaio do T12).
- 04/11 02:4x **T0 v2 aprovado**: cap05 refeito com a conta em R$ 547 e, no Personalizado, Cobranças online + CRM /
  Kanban + 2 usuários (R$ 357 → 617, faixa verde de Upgrade; a linha "R$ -190,00 vs plano atual" aparece ~2 s, é do app).
  Varredura de cor nos dois finais: só elementos normais do app. Legendas da vertical recriadas como hardlink (o pedido quer
  SRT/VTT por versão). Limpeza do T0 v2: stems, `music.wav`, prévia antiga e renders de capítulo (gravações ficam até o
  retorno do Kaik). Prévias 720p para o Kaik em codificação; roteiro final com tempos e lista de telas com o dev-documentos.
- 04/11 03:xx Prévias 720p do T0 v2 enviadas ao Kaik. Roteiro final (`T00v2/roteiro_final.md`) achou o destaque "Tem no seu
  plano" sobre a legenda do player no cap01 vertical (gaveta "Ver trilha" não abria): cap01-p refazendo. Para o Kaik decidir:
  Personalizado a R$ 617 acima do Master (R$ 597; sugestão: Cobranças + 8 usuários = R$ 567); faixa R11 do lembrete fora;
  quadro "Você pode pular durante o teste" na confirmação; botão "Escolher meu plano" leva a /billing (404, C5).
  T12: fase 1 ok; o agente corrigiu `fakebase/core/query.mjs` (embed `alias:coluna_fk(...)`), aceito e levado à skill;
  liberado para gravar.
- 04/11 03:5x T0 v2, cap01 do 9:16: a gaveta "Ver trilha" abre ATRÁS da aula no celular (defeito do app: `DomiflixWatch.tsx:575`
  `z-[100]` × `drawer.tsx` `z-50`; anotado em `T00v2/sinalizacoes.md`, seção 4). Feito: destaque errado removido; os outros 18
  destaques do 9:16 conferem (folha com OCR). Em curso: cap01-p sem toque em "Ver trilha" (opção b: lista de módulos da
  página inicial no celular, sem selos; os selos ficam na ilustração e no cabeçalho da aula). Corrigido o app, regravar o
  cap01-p com a gaveta (opção a). Sem CSS injetado.
- 04/11 04:xx 9:16 do cap01 refeito (opção b: lista de módulos da página inicial no celular, sem toque em "Ver trilha";
  18 destaques conferidos com OCR) e entregue por cima. Roteiro final publicado como documento para o Kaik
  (https://claude.ai/artifact/D5S8enARu7gU81gadHCEe1; cópia em `T00v2/roteiro_final.md`). T0 v2 fechado, salvo o que o
  Kaik decidir (Personalizado R$ 617, faixa R11, gaveta no celular depois da correção do app).
- 04/11 06:2x **segundo reinício do container**: pararam os renders do T2 (feitos até o cap07) e o finish do T12 (ainda na
  fila da trava). App religado com `rec/run.sh app`; T2 e T12 retomados (religam a própria porta e refazem o que parou).
- 04/11 06:4x disco a 2,6 GB: o T2 parou antes do finish (12 capítulos gravados e renderizados, câmera 0). Apaguei 1,5 GB
  de intermediários de revisão e testes no scratchpad (folhas brutas, splice, rec_fake, ex/, testes de 30/10): 4,1 GB.
  Regra nova no brief: stems e `music.wav` saem logo depois do finish.
- 04/11 07:xx **T12 aprovado** (12:00, -15,8 LUFS, câmera 0, 0 falho, maior trecho sem zoom 15,7 s). Revisão: 5 folhas de 3 s +
  busca de cor. Única ressalva: a faixa "Dados faltando: Endereço do cliente" na aba Documentos (cap08, 8:30–8:57) é DEFEITO DO
  APP (`useContractDetail.ts:42` não busca o endereço; anotado em `T00v2/sinalizacoes.md`, seção 4); regravar o cap08 depois
  da correção. Entregando.
- 04/11 07:xx **T12 entregue** (11:59, -15,8 LUFS, 194 legendas). T8 e T9 despachados (fase 1 na 1.38.19, portas 54325 e
  54326); gravação só com o meu "pode gravar" (disco a 4,3 GB, o T2 ainda monta).
- 04/11 08:xx T2 montado (10:14, 12 caps, 0 falho, câmera 0). Revisão: busca de cor, quadros parados e 4 folhas de zoom
  limpas; só o recarregamento do app depois de "Criar Usuário" (`window.location.reload()` em `Users.tsx`, 3,7 a 9,6 s) nos
  caps 05 e 06. Pedido: `pausas.py` (mesma voz) + regravação + `cortes`, como no T0 v2 cap03.
- 04/11 09:xx **T2 entregue** (10:15). Entregues até aqui na 1.38.19: T0 v2 (16:9 + 9:16), T3 v2, T18, T12, T2.
- 04/11 09:xx Desligadas as portas 54324 (T2) e 54327 (T12), entregues. Remendos de T5 (caps 02 a 06), T4 (01 e 03) e
  T1 (11) despachados (fase 1 na 1.38.19, porta 54324; `remendar_aula.py` na fase 2). Em curso: T8, T9 (fase 1) e remendos.
- 04/11 10:xx Remendos, fase 1 ok (8 capítulos, 0 falho). Aceito e a sinalizar ao Kaik: rodapé v1.38.19 nos capítulos novos
  contra v1.38.6 nos vizinhos; T5 cap05 com a fala "Confira antes de salvar" e o título real "Pronto para criar" em destaque.
  Durações: T5 +6,2 s, T4 +0,3 s, T1 +4,0 s. Liberada a gravação, com revisão antes de trocar os arquivos entregues.
- 04/11 11:xx Remendos, fase 2 revistos (folhas de emenda, de 3 s e de destaques, mais a conferência do `05-edicao.md`):
  quadros idênticos ao entregue fora dos capítulos novos (T5 desloca 185 quadros), sem buraco nem estalo nas emendas,
  legendas iguais e deslocadas. **T5 e T1 aprovados** (entrega + limpeza pelo agente). **T4 retido**: os capítulos antigos
  02, 04, 05 e 06 (aba Tipos de Serviços, 1.38.6) mostram "+ Novo Tipo", grande no zoom da aba Fiscal do cap05, logo depois
  do cap03 ensinar "Novo Serviço". Regravar só a tela desses 4 na 1.38.19 (mesma voz; `serviceTypes.btnNew` mudou, tarefas
  seguem "Novo Tipo"). A análise de impacto olhou só as falas; o rótulo na tela dos capítulos vizinhos escapou.
- 04/11 11:xx T8 fase 1 ok: 16 capítulos no ensaio, 0 falho, observador de avisos vazio, falas sem mudança. Robô ajustado à
  1.38.19 (Estoque geral + locais, menu lateral recolhido a 1280 px, Nova compra, inventário, Kardex, Relatório). Defeito do
  app: material novo fora da lista por até 30 s (`accessible-inventory-ids` sem invalidação; `sinalizacoes.md` seção 4); o
  robô usa o foco da janela. **T8: pode gravar**, com aviso no recolhimento do menu (cap00) e revisão antes da entrega.
- 04/11 11:xx T9 fase 1 ok (assistente de 3 etapas, Garantia já ligada, OS #17 pelo Visualizar OS; handler
  `notify-quote-response`). Decidido: cap13 "passando o mouse" = hover no olho + zoom + aviso com o `title` exato (a dica
  nativa não grava; abrir o Visualizar contrariava a fala); menu lateral recolhido como no T8 ("Configurar Proposta" cobre
  a aba "Precificação" a 1280 px). Fica: cap09 com dois "sugerido" (a fala explica). **T9: pode gravar.**
  Próxima leva de voz (remendo só de áudio, mesma duração): T9 cap06 "os custos extras" → "os recursos e extras" (rótulo).
- 04/11 12:2x **T5 e T1 entregues** com os remendos da 1.38.19 (T5 835,8 s, -15,9 LUFS; T1 729,2 s, -15,8 LUFS; gravações e
  renders de capítulo apagados). T4: 02, 04, 05 e 06 regravados na 1.38.19 (0 falho, atraso máximo 0,67 s, câmera 0, estados
  iguais aos de 31/10); `conferir_remendo` OK (+8 quadros, legendas 172 → 172). **Liberada a entrega.** A mesma revisão achou
  mais 3 capítulos antigos na aba Tipos de Serviços com "+ Novo Tipo": cap14 (recapitulação, 10 s, legível no zoom das
  Categorias), cap07 e cap08 (começam nela por 1 s, pelo `setup` do robô). Regravar só a tela dos 3 (mesma voz, partindo dos
  `apos` existentes) e remendar de novo. `conferir_remendo.py` passou a aceitar vários trechos (`--novos A:B,C:D`).
- 04/11 13:1x T4 entregue (12:28). T2 original (168 MB) enviado ao Kaik pelo chat: passou inteiro, o limite de 30 MB não vale
  mais. 13:1x o limite de 5 h da conta parou os 3 agentes; 14:13 **terceiro reinício do container** (app e fakebases caíram).
  Religuei o app 8080; agentes retomados às 14:1x, cada um sobe o próprio fakebase (54324 T4, 54325 T8, 54326 T9).
- 04/11 14:2x **T4 entregue de novo, final** (10:28, -15,8 LUFS, -3,6 dBTP): caps 07, 08 e 14 regravados na 1.38.19 (0 falho,
  atraso máximo 0,45 s, câmera 0, mesmas durações). `conferir_remendo --novos 297.53:387.07,587.73:624.37` OK (dois trechos,
  deslocamento 0); o silêncio antes da cartela já existia no entregue (falso alarme corrigido na ferramenta). "+ Novo Serviço"
  conferido por recorte no começo de 07 e 08 e no 14. Fica só o rodapé v1.38.6 nos caps 00 e 09 a 13 (já sinalizado).
- 04/11 15:4x Kaik: "continue fazendo os vídeos". T8 e T9 na fase 2 (gravando e renderizando, uma trava por capítulo).
  As 10 aulas restantes têm roteiro pronto na 1.38.19 (T11, T13 e T15 já reescritos), mas a voz espera ~88 mil créditos
  do ElevenLabs (saldo ~3 mil); perguntado de novo ao Kaik. Enquanto isso, **T10 sem voz** (agente, 54328): backend falso
  dos 16 `[BACKEND]`, telas conferidas na 1.38.19, `gerar.py` com tempos provisórios do texto e ensaio; com a voz, falta só
  regerar os tempos, ensaiar e gravar. Disco 4,7 GB livres.
- 04/11 16:5x **T8 entregue** (16:53, -15,8 LUFS; 16 caps, 0 falho, atraso máximo 0,79 s, câmera 0). Revisão: folha de 3 s
  inteira, 25 destaques e avisos, recapitulação sem selo. Único ajuste: o aviso final passou a usar o título exato do T9
  ("Próximo: Orçamentos, Precificação e Proposta"), com remendo do cap15 e `conferir_remendo` OK. Pico real -0,6 dBTP
  (as outras aulas ficam entre -3,3 e -3,6): é o AAC estourando num "s" forte do fim do cap12 (13:54; no mix.wav é
  -4,7 dBFS). Correção só no áudio: -3 dB em 834,93-835,06 s, com rampas de 20 ms, e vídeo copiado.
- 04/11 17:13 **Kaik comprou US$ 20 de créditos no ElevenLabs** (print: 172.768 de 286.000 usados, saldo 113.232;
  Creator, renova em 28/11). Agente de voz despachado: emenda do T9 cap06 ("os recursos e extras", rótulo de
  `QuoteFormDialog.tsx:1753`), T11, V4, V5 e o T10 por último, depois da conferência de rótulos do agente do T10.
  Reserva mínima de 8 mil. **17:5x: voz gerada** para T10, T11, T13, T14, T15, T17, T19, T20, T21, T22 e a emenda
  do T9 (141 nós, ~100 min, ~88,4 mil créditos; saldo ~24,8 mil). Daqui não se baixa o áudio (o proxy recusa
  `elevenlabsusercontent.com`): o Kaik exporta o fluxo (zip 7).
- 04/11 17:49 **zip 7 recebido** (305 MP3, exportação atual; os 141 novos extraídos em `$TUT_HOME/recebido/1749/`, 95 MB).
  Disco 3,1 → 4,4 GB: apagados os `video_sem_audio.mp4` de T0, T1, T3 v2, T5, T7 e T18 (MD5 dos pacotes igual ao vídeo
  do `aula_final.mp4`; recria-se com `-map 0:v -c copy`, ver `docs/05-edicao.md`), caches do pip/uv e testes sintéticos.
  T2, T4 e T12 ficam: o final tem um quadro a menos (`-shortest`). Processamento: T9 cap06 com o agente do T9 (emenda),
  T10 com o agente do T10 (tempos reais, ensaio, fase 1) e as outras 9 com um agente de voz (`proc.py`, títulos,
  palavras fracas).
- 04/11 18:42 **T8 final na entrega**: pico real -0,6 → -3,6 dBTP (-3 dB em 0,13 s do `mix.wav`, vídeo copiado,
  MD5 dos pacotes de vídeo igual, áudio alinhado ao mix com correlação ≥ 0,999), -15,8 LUFS. Lição em `08-licoes.md`.
- 04/11 18:59 Kaik: "consegue acelerar despachando mais agentes em paralelo?" Resposta: o gargalo é a máquina (2 CPUs,
  carga 2,3; gravação, render e ASR em fila única); mais agentes só alongam a fila e gastam o limite de uso. O que ajuda é
  a próxima aula pronta quando a fila vaga: **T11 fase 1** despachado como 4º agente (54329, `FAKE_NOW` 2026-11-10 10:00),
  sem escrever em `t11/narracao` enquanto o agente de voz processa.
- 04/11 19:27 Kaik ouviu o T10: a voz dizia "wébruqui"; o certo é **"wébirrúqui"**. A grafia do TTS virou "Uébirrúqui(s)"
  (fonte e trocas da legenda). Como o T10 ainda não foi gravado, os capítulos 02, 08 e 10 foram gerados de novo,
  inteiros (nós `T10 capNN … (v2)`, 3.176 créditos, saldo ~21,6 mil). Aguardando o Kaik mandar os 3 MP3.
- 04/11 19:27 **Pedido novo do Kaik: capítulo de instalar o app (PWA) no T1**, no computador e depois no celular, explicando
  que o app é web mas não precisa ficar no navegador, com as diferenças entre Android e iOS. Decidido (perguntas 19:3x):
  entra **logo depois da abertura do T1**, com uma frase nova na abertura e no resumo; o **celular o Kaik grava** (Android e
  iPhone, sem narração); o **computador é gravado aqui**, no navegador inteiro (Xvfb + x11grab, cadeado em dominex.app
  com CA local; agente em `t1pwa/`, 54330). O app é instalável (manifest, service worker, `PwaRootEntry`), mas não tem
  botão de instalar dentro dele (`InstallBanner.tsx` não é usado). Roteiro e voz do capítulo depois das gravações.
  Roteiro e voz já feitos às 19:4x (cap14, 81,1 s; título; frases trocadas na abertura e no resumo); celular ilustrado
  (o Kaik preferiu: "grave você ou ilustre tudo").
- 04/11 19:4x **Handoff do app: preenchimento e edição de OS** (`HANDOFF_OS_preenchimento_2026-11-04.md`). AINDA NÃO
  publicado (sem commit/deploy; migration pendente): não gravar antes de confirmar a publicação e atualizar app 8080,
  `src-*` e o schema do backend falso. Impacto nas falas: **T7** (cap03: "o cartão de Checklists" e o rodapé "Finalizar OS,
  Finalizar Parcial"; a tela do preenchimento aparece em quase todos os capítulos → regravar a imagem do T7 inteiro na
  versão nova, com a mesma voz onde a fala não muda) e, se o formulário de criação também mudou, **T5** (cap04: "checklists
  avulsos"). T2 (permissão "Editar OS em campo") não muda. O caso de uso sugerido (checklist sem equipamento arrastado
  para dentro do equipamento em "Editar OS", respostas mantidas) pede um trecho novo no T7. Falas novas só com os
  rótulos finais do código publicado.
- 04/11 19:5x **Voz do zip 7 processada** em T11, T13, T14, T15, T17, T19, T20, T21 e T22 (`proc.py` e títulos; 164 palavras
  fracas, todas do ASR, conferidas isoladas e desaceleradas; nenhuma fala a refazer). Disco 4,1 → 3,0 GB com a montagem do
  T9: apagados rascunhos de 29 a 31/10 e os MP3 dos zips 1, 3 e 4 (voz já processada e ainda no fluxo) → 3,4 GB.
- 04/11 20:0x Liberar `elevenlabsusercontent.com` no ambiente do claude.ai/code não valeu para esta sessão do chat (4 min de
  teste, 403); download segue manual. **T9 revisado e aprovado** (998,4 s; 0 falho; atraso máx. 0,77 s; 32 destaques e
  avisos conferidos; emenda "recursos e extras" no cap06), menos as vinhetas 05 a 09 que diziam "Primeira" a "Quinta etapa"
  (assistente de 3 etapas): títulos sem número, nó `T09 títulos 05 a 09 (v2)` (133 créditos). **T1 cap14, computador gravado
  de verdade** (`t1pwa/desktop.mp4`, 21,8 s; técnica em `docs/04-gravacao.md`); celular ilustrado em andamento (`t1pwa_cel/`).
- 04/11 20:06 **zip 8 recebido** (7 MP3: T10 caps 02/08/10 v2, T01 cap14 + título + emendas, T09 títulos v2; durações iguais às
  geradas) em `recebido/2006/`; repassados aos agentes do T9, do T10 e do capítulo do app.

## Fila (31/10 12:1x; nada sai da fila sem estar entregue)
1. **Rodando (Kaik 14:48 liberou até 4 agentes ao mesmo tempo):** dev-video no 06 e no 12 do site (com a trava
   pesada só para ele, pedido de urgência) · G3 com o T5 pausado antes do cap17 e do finish · dev-gravacao corrigindo
   T1 e T4 (prepara o leve; o pesado espera a trava) · dev-levantamento na 1.38.9 + roteiro do T3 v2 (`T03v2/`).
   Disco: 5,6 GB livres; T1/T4 guardam `video_sem_audio.mp4` para corrigir só o áudio.
2. **Próximas vagas, nesta ordem.** A **1.38.8** saiu às 12:40 (`0b35ea72`, etiquetas e campos personalizados; fonte em
   `$TUT_HOME/src-1.38.8`). O T1 não muda: as Configurações e o `CustomerOriginManagerDialog` seguem iguais.
   (a) `emendar.py` corrigido, T4 (emenda do cap03) e T1 (cap05 com o logo branco e emendas de pronúncia), ainda na
   1.38.6, como o resto do T1; reentregar os dois. (b) Em paralelo: levantamento da 1.38.8 em Clientes e Fornecedores,
   roteiro dos trechos do T3 e voz só do que muda. (c) Trocar o app de gravação para a 1.38.8, depois que o T5 e o cap05
   do T1 estiverem gravados. (d) T7 retomado (G4, `rec/t7/ESTADO.md`) e T18, na 1.38.8. (e) T3 v2. (f) Com créditos:
   vozes V3–V5 e as aulas T2, T8, T9, T12, T13, T20, T10, T11, T15, T22, T19, T21, T14, T17, na ordem da trilha
   (conferir telas de cliente, fornecedor e portal na versão nova).
   **Kaik 12:45: "vou soltar a 1.38.9 com as funções definitivas disso"**: o levantamento do T3 v2 e a troca do app
   esperam a 1.38.9 (vigia no `main` rodando), não a 1.38.8.
   **1.38.9 publicada 13:27** (`7690807a`; fonte em `$TUT_HOME/src-1.38.9`): várias etiquetas em clientes, fornecedores e
   **equipamentos**, filtros, etiquetas nos seletores (OS, agenda, orçamento, compras, PDV), configurações reunidas
   (`Equipment.tsx` perdeu ~190 linhas: a configuração de campos do equipamento deve ter ido para o modal único) e
   etiquetas no portal do PMOC. Afeta o T3 (capítulos de equipamento também) e muda telas de T5, T8, T9, T11, T12
   (sem etiquetas semeadas, só aparecem os controles novos). O T5 segue na 1.38.6 (já gravado; seletores sem etiqueta
   ficam iguais); conferir na entrega se a agenda ganhou filtro visível.
   **16:4x:** levantamento e roteiro do T3 v2 prontos (`T03v2/`), voz gerada (lote V2c). Para gravar na 1.38.9, o backend
   falso precisa de 5 tabelas, 5 colunas, 3 RPCs chamadas em todo salvar, padrões e o gancho de exclusão
   (`T03v2/inventario_delta.md`); a troca do app para a 1.38.9 vem junto com isso, depois do T1 cap05/cap06 (1.38.6).
   T7 retomado (G4): prepara agora e grava na 1.38.9.
4. **T0 v2 (Kaik 31/10 17:13, `T00v2/pedido_kaik_31-10.txt`):** refazer o T0 para o onboarding novo (o vídeo é o 1º
   passo obrigatório; trilha "Tutoriais do sistema" → Formação Básica → módulos do plano → outros módulos com "Não tem no
   seu plano"; progresso; lembretes de 30 dias; "Tirar dúvidas com o suporte"), 4 a 4:30, 16:9 **e 9:16 nativo**, com
   telas reais da DomiFlix nova. **Antes de gerar:** roteiro revisado + storyboard das duas proporções + lista de telas
   para aprovação. A DomiFlix nova **não está no `main`** (17:13: só a atual, com temporadas). Voz: ~4 mil caracteres,
   com ~5 mil reservados no saldo (recarga do Kaik às 18:28).
   **19:3x roteiro + storyboards prontos** (`T00v2/`: 39 cenas, 4:28 estimado, 2.445 caracteres de voz nova; capítulos de
   assinatura e plano reaproveitam o áudio do T0) e **publicados para aprovação**: https://claude.ai/artifact/Gjtpv2dE1HEY5GCx4hcnUx
   (cena a cena com os quadros 16:9 e 9:16, decisões D1–D6, confirmações C1–C17, telas R01–R18). Aguardando o ok do Kaik.
   Bloqueio: a DomiFlix nova não está no `main` (a branch `trilha-tutoriais-domiflix` é de 06/09, página do site; nenhuma
   outra branch tem nome que indique a DomiFlix nova): R01–R12 esperam a publicação. Falta também o 9:16 no pipeline (D6).
   **20:02 Kaik: DomiFlix nova publicada** (no `main` desde 17:34: 1.38.11 + ajustes até `487a0ca3` 19:29; o agente tinha
   conferido um `main` antigo). Fonte em `$TUT_HOME/src-1.38.11`. Agente de roteiro conferindo C1–C17 e R01–R12 no código
   novo e ajustando o pacote; a página de aprovação será regenerada. O app de gravação segue na 1.38.9.
   **21:0x conferido na 1.38.11** (agente de roteiro): o código confirmou introdução obrigatória, trilha, selos, percentual
   "Trilha do seu plano", lembrete de 30 dias, próxima aula e suporte com contexto (C8 e C17 saíram). Cena 22: o botão abre o
   WhatsApp com a mensagem pronta (não envia sozinho). 4:27 estimado; 2.433 caracteres de voz. Página de aprovação v2 publicada.
   Para o Kaik: D7 (técnicos também passam pela introdução), D8 (frases dele × rótulos: "Aprenda a usar a Dominex",
   "Materiais e extras", "Formação básica"), D3 (conta contratada ou em teste) e **erro no app: "Adicionar ao meu plano" e
   "Escolher meu plano" abrem `/billing`, que não existe** (cai em "não encontrada"). O player desenha a legenda a 15%/18% do
   pé e usa UMA legenda por aula nas duas versões (mesma linha do tempo). Captura: app 1.38.11 em outra porta (8081) e
   backend próprio; **não usar a 54322** (é do T18): usar a 54328.
5. **Kaik 31/10 20:23: "botei mais créditos, avance, pode botar quantos agentes em paralelo você quiser, até 10".** Os 4
   agentes tinham parado no limite semanal da API (20:1x) e foram retomados. Rodando (9): T7 (A, 54321; corrige o celular
   que vaza no zoom, pedido do Kaik), T18 (B, 54322), T3 v2 (C, 54323), T2 (D, 54324), T8 (E, 54325), T9 (F, 54326),
   T12 (G, 54327), roteiro do T0 v2 (1.38.11) e pipeline vertical 9:16 do T0 v2. Gargalo real: a máquina tem 2 CPUs e
   gravação/render são um por vez (trava por capítulo); os agentes mantêm a fila cheia. Disco: 6,5 → 9,0 GB livres
   (apagados 75 caches `.pkl` de vídeos do site que não mudaram hoje; regeráveis com `tools/run.py <spec> track`).
   Pergunta ao Kaik: os créditos são do Claude ou do ElevenLabs (as vozes de T10, T11, T13–T15, T17, T19–T22 pedem ~88 mil).
3. **T3 v2 (Kaik 31/10 12:11):** "Editar" e "Excluir" da ficha foram para "Ações" (já na 1.38.6, `5f0b64ea`: fichas de
   cliente e de equipamento) e "Configurar origens" virou um modal único "Configurações" com Origens, Etiquetas, Campos
   de clientes e Campos de fornecedores (`CustomerSettingsDialog.tsx`, recurso novo; publicado na 1.38.8). Afeta no T3: cap01 (botões do topo), cap04 (vira origens + etiquetas + campos), cap05 (cabeçalho da
   ficha), cap07 (fornecedor, campos), cap10 (ficha do equipamento) e o recap; no T1, o cap09 (Origens) se o cartão de
   Configurações mudar. Plano: levantamento da versão nova → roteiro dos trechos → voz só do que muda → regravar esses
   capítulos → reentregar (T1 junto, se o cap09 mudar). As aulas seguintes passam a gravar na versão nova.

## Correções pedidas pelo Kaik (31/10 11:04)
- **Pronúncia** em todas as aulas: Glacial Cold Brasil → "Glaciál Côude Brasil" (sozinho, "Glaciál"); White Label →
  "uáit lêibou". Textos e `config_narracao.json` corrigidos no planejamento e na área de trabalho (perfil também).
  Já gravadas: T1 (cap03, cap06, cap07, cap13 por emenda; cap05 refeito inteiro), T4 (cap03 por emenda), T18 (cap01,
  emenda depois do V2). `trocas.json` de t1 e t4 prontos.
- **T1, logo do White Label:** usar a versão com o texto branco (`/home/claude/brand-fix/assets/glacial_horizontal_texto_branco.png`)
  no "Logo completo" (o menu é escuro). Roteiro do cap05 reescrito (linhas 3 e 4) e voz nova (`T01 cap05 ... (v2)`):
  regravar o cap05 com o passo "Substituir" + upload, refazer a edição dele, as emendas e o `finish`/`entregar`.
- **T4:** emenda no cap03, render só do cap03 e `finish`/`entregar` de novo.
- **Processado 31/10 11:30** (`recebido/1118/processar.log`): T18 inteiro ok (16 capítulos, títulos, emenda do cap01 com
  0,57 s de folga; palavras fracas conferidas isoladas: todas do ASR). T7 cap05 e T1 cap03/06/07/13 emendados, mas a frase
  nova é um pouco mais longa: encosta na fala seguinte no T7 cap05 (−0,05 s) e no T1 cap03 (−0,16 s), sem respiro no T1
  cap07 (+0,03 s). T4: `emendar.py` quebrou (troca começando em 0 s dá índice negativo). **Antes de usar:** corrigir o
  `emendar.py` (início ≥ 0; frase mais longa que a janela comprimida até ~8% para deixar ≥ 0,2 s antes da próxima fala)
  e refazer as emendas de t1, t4 e t7. A fala do T7 diz "deixa" (decodificado isolado: "Deixa o vídeo"); o ASR é que cola
  "aplicativo deixa". Cópias `capNN.v1.json` guardadas.
- **Vídeos do site (sugestões do Matheus):** cabeçalho do portal em preto, "como se a marca tivesse definido assim",
  e, no círculo, só o ícone do logo com o nome embaixo (05 PMOC e 06 Portal do Cliente).

## Voz: lotes e exportação
Kaik (30/10 23:13): **um fluxo só com todas as aulas**, **uma versão por fala** (`generations_count: 1`), v3 liberado
se for melhor (custa o mesmo que o v4 por caractere: fica o v4, voz do T3); fala ruim regera só ela. Estimativa:
~12 mil caracteres por aula, ~230 mil créditos no total.

| Lote | Aulas | Fluxo ElevenLabs | Situação |
|---|---|---|---|
| — | T0 | 1fUfJ2KZAxkHKnc8wwce (fluxo próprio) | exportado 30/10 22:12 |
| V1 | T1, T4, T5, T7 (39,6 mil caracteres, 65 nós) | Tuop7qPrgwc8qdaVebww (fluxo único) | exportado 31/10 00:29; proc.py e títulos ok (semelhança 0,87 a 1,00) |
| V2 | T18 (11,3 mil caracteres, 17 nós) + `T07 cap05 emenda` | mesmo fluxo | exportado 31/10 11:18 (zip 3); processando |
| V2b | Correções de pronúncia (Kaik 31/10 11:04): `T01 cap05 A cor e o logo da marca (v2)` (logo com texto branco), `T01 emendas`, `T04 emendas`, `T18 emenda` = 1.745 créditos | mesmo fluxo | gerado 11:11, exportado 11:18 (zip 3); processando |
| V2c | T3 v2 (1.38.9): `T03v2 cap06 Etiquetas`, `T03v2 cap07 Campos personalizados`, `T03v2 emendas`, `T03v2 inserções`, `T03v2 títulos` = 1.824 créditos | mesmo fluxo | gerado 31/10 16:37; **saldo ~0**; exportado 16:50 (zip 4): MP3 em `$TUT_HOME/recebido/1650/` |
| V3 | T2 (8.464), T8 (13.934), T9 (13.544), T12 (10.270) = 46.212 créditos, 61 nós (1 versão cada), ~52,8 min de voz | mesmo fluxo | **gerado 31/10 18:3x–18:41** (Kaik comprou créditos 18:28 e aprovou "gere T2, T8, T9 e T12"); 61/61 concluídas, 0 falha; ids em `scratchpad/v3_nos.json`; zip 5 (18:53) processado: 96 palavras fracas, todas do ASR (conferidas isoladas e desaceleradas), nenhuma fala a refazer |
| V3b | T10 (10,4 mil), T11 (14,2 mil) = ~24,6 mil | mesmo fluxo | **gerado 04/11 17:2x–17:5x** (1 versão cada, 0 falha; durações medidas nos `nos_elevenlabs.json`); zip 7 recebido 17:49; processando |
| V4 | T13 (12,8 mil), T19 (9,1 mil), T20 (7,9 mil), T14 (7,7 mil) = ~37,5 mil | mesmo fluxo | **gerado 04/11 17:2x–17:5x** (1 versão cada, 0 falha; durações medidas nos `nos_elevenlabs.json`); zip 7 recebido 17:49; processando |
| V5 | T15 (8,2 mil), T22 (6,9 mil), T21 (5,4 mil), T17 (5,6 mil) = ~26,1 mil | mesmo fluxo | **gerado 04/11 17:2x–17:5x** (1 versão cada, 0 falha; durações medidas nos `nos_elevenlabs.json`); zip 7 recebido 17:49; processando |

**Falas a refazer (próximo lote de voz, junto com o T18; o Kaik exporta uma vez):** T07 cap05, frase "O aplicativo
deixa o vídeo mais leve antes de enviar." (em ~0:29; o ASR não ouve o "deixa" nem isolado; há tempo de fala para ele,
então pode estar só fraco). Nó curto `T07 cap05 emenda` (~55 caracteres) + `emendar.py` antes de gravar o T7 (`t7/narracao/trocas.json` pronto). As demais
palavras fracas do V1 foram conferidas decodificando o trecho isolado: eram do ASR (números, nomes colados).

**Para terminar (31/10 07:20): V3 + V4 + V5 = ~134,4 mil caracteres** (~70,8 + 37,5 + 26,1), mais ~3 mil de reserva
para regerar falas; saldo de ~3,6 mil.
**31/10 18:28:** o Kaik comprou créditos (saldo ~55,1 mil, "Para o t0"). Gerado o V3 (T2, T8, T9, T12: 46,2 mil); sobram
~8,9 mil, com **~5 mil reservados para a voz do T0 v2** depois da aprovação do roteiro. Faltam V3b + V4 + V5 = ~88,2 mil.

**Créditos (Kaik, 30/10 23:16): 54.670 restantes** (de 121.000) → ~54 mil caracteres ≈ 55 a 60 min de fala ≈ 4 aulas.
Gerar agora, na ordem da produção, só o que couber (T1, T4, T5, T7 se couber), com ~2 mil de reserva para regerar falas.
As demais: roteiro pronto e voz quando houver créditos (o Kaik avisa). Antes de cada lote: somar os caracteres de
`CAPS` + `TITULOS` e conferir com o saldo.

## Entrega
Nome do arquivo **sem dois-pontos** (o ZIP abre no Windows e no Mac): título com ":" vira " - " só no nome do
arquivo (ex.: `Domiflix T18 - Área do Técnico - Refrigeração e Climatização.mp4`); na vinheta fica como no roteiro.
ZIP único (ou em partes, se passar do limite de envio) com `Domiflix Tnn - <Título>.mp4/.srt/.vtt` de todas as aulas
(T0 a T22, incluindo o T3 já entregue), 1080p, CRF 20 (padrão T3).
