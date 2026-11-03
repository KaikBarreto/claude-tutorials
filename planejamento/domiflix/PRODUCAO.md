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
| T0 | Boas-vindas à Dominex (ilustrada) | ok | ok | ok | ok | — | — | ok | ok (30/10 22:51, 3:25) |
| T1 | Configurações e identidade da empresa | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 05:20, 11:58) · **v2 18:33** (pronúncia + logo com texto branco; 12:05; 1.38.6) |
| T2 | Usuários, cargos e permissões | ok | ok | ok (V3 18:3x) | ok (zip 5, 19:31) | agente D (54324), 1.38.9, desde 20:3x | | | |
| T3 | Clientes, Fornecedores e Equipamentos | ok | ok | ok | ok | ok | ok | ok | ok (30/10) |
| T4 | Serviços, tarefas e checklists | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 10:46, 10:27) · **v2 18:37** (pronúncia; só o áudio) |
| T5 | Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 18:2x, 13:49; 1.38.6) |
| T7 | O técnico em campo (celular) | ok | ok | ok | ok (31/10 00:29; emenda do cap05 com folga 0,17 s) | agente A, 1.38.9 (porta 54321) | gravando | | |
| T18 | Área do Técnico: Refrigeração e Climatização | ok | ok | ok | ok (31/10 11:30) | agente B, 1.38.9 (porta 54322), desde 19:0x | | | |
| T8 | Estoque, compras e inventário | ok | ok | ok (V3) | ok (zip 5, 19:50) | agente E (54325), 1.38.9, desde 20:3x | | | |
| T9 | Orçamentos, Precificação e Proposta | ok | ok | ok (V3) | ok (zip 5, 20:11) | agente F (54326), 1.38.9, desde 20:3x | | | |
| T10 | CRM: funil, leads e captação | ok | ok | | | | | | |
| T11 | Contratos e PMOC | ok | ok | | | | | | |
| T12 | Portal do Cliente e Portal do Contrato | ok | ok | ok (V3) | ok (zip 5; títulos 20:4x) | agente G (54327), 1.38.9, desde 20:3x | | | |
| T13 | Financeiro | ok | ok | | | | | | |
| T19 | Integração com Asaas, Assinaturas e Cobranças | ok | ok | | | | | | |
| T20 | Relatório Financeiro e DRE | ok | ok | | | | | | |
| T14 | Notas Fiscais (NFS-e e NF-e) | ok | ok | | | | | | |
| T15 | Funcionários: Financeiro do Funcionário e Ponto | ok | ok | | | | | | |
| T22 | Ferramentas de RH: DISC, Organograma, Fluxograma | ok | ok | | | | | | |
| T21 | Integração com WhatsApp | ok | ok | | | | | | |
| T17 | Dashboard, relatórios e exportações | ok | ok | | | | | | |

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
- Sem preço de plano da Dominex em nenhum vídeo.
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
| V3b | T10 (10,4 mil), T11 (14,2 mil) = ~24,6 mil | mesmo fluxo | roteiros ok; aguardando créditos |
| V4 | T13 (12,8 mil), T19 (9,1 mil), T20 (7,9 mil), T14 (7,7 mil) = ~37,5 mil | mesmo fluxo | roteiros ok; aguardando créditos |
| V5 | T15 (8,2 mil), T22 (6,9 mil), T21 (5,4 mil), T17 (5,6 mil) = ~26,1 mil | mesmo fluxo | roteiros ok; aguardando créditos |

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
