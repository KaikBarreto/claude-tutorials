# Inventário funcional · T22 — Ferramentas de RH: Perfil Comportamental (DISC), Organograma e Fluxograma (Dominex)

> Base para o roteiro do tutorial "T22 · Ferramentas de RH". Levantado em 31/10/2026 contra o código publicado
> `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T14.
> As três ferramentas são abas da tela Funcionários (T15). O Guia Técnico só as resume (`docs/guia-tecnico/secoes/T15.html`, cap. 12).

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). **emp** = `lib/i18n/messages/app/employees.ts` (bloco pt-br `:9-1210`; DISC do
  gestor `:704-850`, organograma `:1100-1208`); **disc** = `lib/i18n/messages/app/discProfile.ts` (bloco pt-br `:22-1400`:
  tela pública, gráficos, perfis, dossiê); **proc** = `lib/i18n/messages/app/processes.ts` (bloco pt-br `:16-223`).
- As três gravam no banco a cada mudança (organograma e fluxograma com salvamento automático); nada depende de serviço externo.
  O que sai em arquivo (PDF/PNG) é gerado no navegador.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Onde ficam as três ferramentas em **Funcionários** | **Bate** | Abas "Perfil Comportamental", "Organograma", **"Fluxograma"** (antes "Processos", renomeada na 1.28.17) (`pages/Employees.tsx:382-386`; emp `:317-318`; proc `:19`; `pages/Changelog.tsx:2361`). Endereços próprios `/funcionarios/perfil/…`, `/funcionarios/organograma`, `/funcionarios/fluxogramas` (`App.tsx:872-880`). |
| 2 | **DISC**: gerar o link e definir se o funcionário vê o resultado | **Bate** | Na aba, cartão de cada funcionário "Sem teste" + **"Gerar link"** → janela **"Gerar link de avaliação"** com "Funcionário vê o resultado ao final" ("Você pode mudar isso a cada avaliação. O padrão vem das configurações da empresa.") → **"Gerar link"** → link copiado ("Link gerado e copiado!") (`components/employees/EmployeeDiscOverview.tsx:382-415`; `components/employees/disc/DiscGenerateLinkModal.tsx`; emp `:748-754`). Padrão da empresa em Configurações › Regional, cartão "Perfil Comportamental" (`components/settings/SettingsRegionalContent.tsx:109-117`). |
| 3 | O funcionário responde **sem login** | **Bate, mais curto** | `/avaliacao/<nome>-<código>` (`App.tsx:759`; `hooks/useEmployeeDisc.ts:48-51`): "Teste de Perfil Comportamental (DISC)", "Olá, {nome}!", "Como funciona", **"Começar"**; **28 perguntas** sorteadas do banco de 56 (escala de arrastar + escolha) "Pergunta {n} de 28", "Voltar"/"Avançar", **"Enviar respostas"** (`pages/DiscAssessmentPublic.tsx:124-128,439-660`; disc `:24-66`). Ficou mais rápido na 1.32.2 (`Changelog.tsx:1962`). |
| 4 | Ler o perfil: fatores, competências, emocional, qualidades, pontos de atenção | **Bate** | Ficha do funcionário, sub-aba **"Visão geral"**: "Perfil {código}", "Gráfico DISC", "Competências Comportamentais", "Perfil emocional", "Qualidades", "Pontos de atenção", "Motivadores de carreira" (`components/employees/disc/DiscReport.tsx:439-555`; disc `:113-180,1075-1121`). |
| 5 | Histórico, evolução e comparação entre dois | **Bate** | Sub-abas **"Interações"** (um colega: "Atritos", "Sinergias", "Melhor comunicação") e **"Histórico"** ("Histórico de avaliações", "Evolução do perfil", "Linha do tempo") (`components/employees/EmployeeProfileDetail.tsx:977-979,251,612,748`); botão **"Comparar"** na aba, só com 2+ perfis respondidos (`EmployeeDiscOverview.tsx:490-510`). |
| 6 | Baixar dossiê e comparativo em **PDF** | **Bate, com outro nome** | Botões **"Ver PDF"** (dossiê) e **"Ver comparação"** (em "Interações") abrem o PDF **em nova aba** (`EmployeeProfileDetail.tsx:202-238,905-950,1082-1110`; disc `:1116-1118`). |
| 7 | **Organograma**: quadro, funcionário, cargo manual e setor | **Bate** | "Novo Organograma" → "Nome do organograma" ("Ex: Estrutura 2026") → "Criar"; o quadro **nasce com a caixa "Direção"** (1.28.17) (`components/employees/orgchart/OrgChartTab.tsx:96,173-190`; `OrgChartCanvas.tsx:861`; `Changelog.tsx:2356`). "Adicionar nó" com abas "Funcionário"/"Manual" (emp `:1139-1154`). |
| 8 | Conectar, organizar, buscar, destacar setor, tela cheia | **Bate** | "+" nas bordas da caixa liga a nova pessoa já na hierarquia (`OrgChartCanvas.tsx:603-650`; `OrgChartNode.tsx:115-137`); **"Organizar"** ("Reposiciona automaticamente em árvore"); "Tela cheia" com "Ferramentas": "Adicionar caixa", "Árvore", "Destacar por setor", "Buscar pessoa" (`OrgChartFullscreen.tsx:339-344`). |
| 9 | Exportar em PNG ou PDF | **Bate** | **"Exportar"** → "Baixar imagem (PNG)" / "Baixar PDF" ("Sai no tema atual"): **download** (`OrgChartCanvas.tsx:348-385,979-1000`; `lib/canvas/graphExport.ts:371-386,403-511`). |
| 10 | **Fluxograma**: início, ação, decisão, subprocesso e fim | **Bate, com outro nome** | "Novo fluxograma" → "Nome do fluxograma" ("Ex.: Abertura de ordem de serviço") → "Criar fluxograma"; nasce com a forma **"Início"** (`components/employees/processes/ProcessCanvas.tsx:625-646`). "Adicionar forma": "Início", **"Tarefa"** (a "ação" da trilha), "Decisão", "Subprocesso", "Documento", "Espera", "Fim", "Observação" (proc `:52-72`). |
| 11 | Raias, conexões e organização automática | **Bate** | "Adicionar raia" ("Nome da raia (setor ou responsável)"), conexões com "Tipo de conexão" "Sequência"/"Informação" e "Rótulo (ex.: Sim, Não)", **"Formatar"** e **"Organizar"** (`ProcessCanvas.tsx:1338-1347,649-680`; proc `:74-111`). |
| 12 | Conferir problemas e gerar o **POP** | **Bate** | Botão **"Conferência do fluxograma"** com contagem de erros/avisos e "Ir até a etapa" (`ProcessCanvas.tsx:1359-1369,1494-1540`; proc `:156-180`); **"Baixar POP em PDF"** no menu "Exportar" (nova aba) (`:1386-1410,857`; `components/employees/processes/ProcessPopDocument.tsx`). |
| 13 | Exportar, **compartilhar** e manter atualizado | **Parcial** | Exportar imagem/PDF e o POP; **não há compartilhar** nem publicar (P8, P9). |

Avisos da trilha:

- ⚠️ "Link do DISC é individual e público" → **bate**: qualquer um com o link abre o teste e, depois de respondido e com o
  resultado liberado, vê o perfil (P3). Só dados fictícios.
- ⚠️ "Visibilidade do resultado depende da configuração ao gerar" → **bate** (`COALESCE(avaliação, empresa, false)`,
  `supabase/migrations/20260727090000_disc_public_white_label_flag.sql:68`).
- ⚠️ "Organograma e Fluxograma salvam automaticamente" → **bate**: selo "Salvando…" → "Salvo" (organograma, debounce ~800 ms,
  `OrgChartCanvas.tsx:239-330,1017-1025`) e "Salvando..." / "Salvo" / "Erro ao salvar" (fluxograma, `ProcessCanvas.tsx:1236-1245`; proc `:100-102`).
- ⚠️ "Fluxograma nasce com etapa inicial; a conferência aponta caminhos sem início, sem fim ou isolados" → **bate** (13 problemas,
  proc `:166-180`).
- ⚠️ "POP sai do fluxograma; desenho desatualizado gera documento desatualizado" → **bate**, com o próprio aviso do POP: "Documento
  gerado pelo sistema a partir do fluxograma cadastrado. Mantenha o desenho atualizado: ele é a fonte deste procedimento." (proc `:221`).

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.28.14 | Desfazer e refazer pelo teclado no Organograma | `:2422` |
| 1.28.17 | "Processos" vira **Fluxograma**; organograma e fluxograma já abrem com a primeira caixa; botões do fluxograma voltam a responder | `:2361,2356,2351` |
| 1.32.2 | Teste de perfil comportamental mais rápido de responder | `:1962` |
| 1.37.35 | No computador, perfis com a lista ao lado da ficha | `:507` |

(DISC 1.17.28 a 1.17.42 e Organograma 1.17.31 a 1.17.46 são anteriores à 1.22.5: `Changelog.tsx:5515-5801`.)

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. "Ver PDF", "Ver comparação" e "Baixar POP em PDF" abrem nova aba; os exports do organograma e do fluxograma baixam arquivo.
2. O link do DISC continua mostrando o resultado depois de respondido, para quem tiver o link (P3).
3. "O fluxograma está pronto para ser publicado." aparece, mas não existe publicar; o POP sai sempre "Versão 1" (P8).
4. As respostas do DISC de todos são legíveis por qualquer usuário da empresa pela API (P1, LGPD).
5. "Comparar" só aparece com dois ou mais perfis respondidos: a semente precisa de um perfil antigo.
6. O tooltip do gráfico DISC cita pessoas reais como exemplo de cada fator (P6).

### 0.4 O que a empresa ganha ao nascer (cadastro) e toca o RH

Conferido nas duas portas de cadastro (`supabase/functions/self-register/index.ts:728-1052`,
`supabase/functions/create-company/index.ts:330-557`), no RPC `seed_company_catalog`
(`supabase/migrations/20260718120000_seed_company_catalog_i18n.sql:10-247`: só tipos de serviço, status de OS e tipos de tarefa) e
nos gatilhos `AFTER INSERT ON companies`:

- **DISC:** nenhuma avaliação. O padrão de "Funcionário vê o resultado ao final" é a coluna
  `company_settings.disc_show_result_to_employee` (padrão `true`, `supabase/migrations/20260724120000_disc_perfil_comportamental.sql:35`),
  que já vem na linha de configurações criada pelo gatilho (`20260612150000_company_settings_backfill_e_trigger.sql:100-102`).
- **Organograma e fluxograma:** nenhum quadro (`org_charts` e `processes` vazios). A caixa "Direção" e a etapa "Início" são criadas
  pelo app ao abrir um quadro novo (seções 3.6 e 3.8), não no cadastro.
- **Cargos e setores:** não existe tabela de cargos nem de setores. "Cargo" é texto livre no cadastro do funcionário
  (`T15/inventario.md` 3.3) e "Setor" é texto da caixa do organograma ("Ex: Comercial", seção 3.6).
- **Funcionários:** nenhum no cadastro; os do mundo fictício vêm do T9 e do T15.

---

## 1. Rotas e navegação

| Tela | Caminho | URL | Componente |
|---|---|---|---|
| Perfil Comportamental (lista) | Gestão › Funcionários › aba "Perfil Comportamental" | `/funcionarios` (aba é estado) | `components/employees/EmployeeDiscOverview.tsx` |
| Perfil de um funcionário | clique no cartão | `/funcionarios/perfil/<nome>-<código>` (`pages/Employees.tsx:211-236,345-356`) | `components/employees/EmployeeProfileDetail.tsx` |
| Teste (sem login) | link copiado | `/avaliacao/<nome>-<código>` (`App.tsx:759`) | `pages/DiscAssessmentPublic.tsx` |
| Organogramas | aba "Organograma" | `/funcionarios/organograma` e `/funcionarios/organograma/<nome>-<código>` (`pages/Employees.tsx:238-282`) | `orgchart/OrgChartTab.tsx`, `OrgChartCanvas.tsx`, `OrgChartFullscreen.tsx` |
| Fluxogramas | aba "Fluxograma" | `/funcionarios/fluxogramas` e `/funcionarios/fluxogramas/<nome>-<código>`; `/funcionarios/processos` redireciona (`App.tsx:879-883`) | `processes/ProcessesTab.tsx`, `ProcessCanvas.tsx`, `ProcessFullscreen.tsx` |
| Padrão "funcionário vê o resultado" | Configurações › "Regional" › cartão "Perfil Comportamental" | `/configuracoes?tab=regional` | `components/settings/SettingsRegionalContent.tsx:109-117`; textos `lib/i18n/messages/app/settings.ts:334-342` |

Abrir um organograma ou fluxograma muda a URL (dá para voltar com o navegador e mandar o endereço a um colega logado).

## 2. Permissões e módulos

| O quê | Regra | Onde |
|---|---|---|
| As três abas | tela "Funcionários" + módulo `rh` ("Funcionários / RH") | `App.tsx:869-880`; `components/ModuleGateModal.tsx:117-120` |
| Gerar link DISC (gravar `disc_assessments`) | membro da empresa com `can_manage_system` | `supabase/migrations/20260724120000_disc_perfil_comportamental.sql:106-118` |
| Ler perfis DISC | **qualquer** usuário da empresa | `:101-104` (P1) |
| Organograma e fluxograma | ler: qualquer usuário da empresa; gravar: policy de gestores **e** policy "Users manage own company …" para qualquer usuário | `supabase/migrations/20261001130000_processes.sql:86-130` (espelho de `org_charts`, P2) |
| Teste público | anônimo, só pelas RPCs `get_disc_public` / `submit_disc_assessment` (SECURITY DEFINER) | `20260727090000_...sql:13-102`; `20260725100000_disc_show_result_per_assessment.sql:128-211` |
| Cartão de padrão em Configurações | aba Regional (admin/gestor ou `fn:manage_settings`, a confirmar) | `SettingsRegionalContent.tsx` |

---

## 3. Por tela

### 3.1 Aba "Perfil Comportamental" (`components/employees/EmployeeDiscOverview.tsx`)

- Lista **todos os funcionários ativos** (inclusive PJ) (`:378-379`), em grade ou lista (padrão guardado no navegador
  `disc-overview-view-mode`, `:355`). Barra: **"Comparar"** só com 2+ perfis respondidos (`:490-510`).
- Cartão sem teste: "Sem teste" + **"Gerar link"**; pendente: "Aguardando resposta" + **"Copiar link"** ("Link copiado!");
  respondido: código do perfil, barras dos fatores ("{fator}: {pontos}") e "Respondido em {data}"; rodapé "Ver detalhes"
  (`:116-259`; emp `:733-747`). Vazio: "Nenhum funcionário ativo" (`:480-487`).
- **"Gerar link de avaliação"** (`components/employees/disc/DiscGenerateLinkModal.tsx`): interruptor "Funcionário vê o resultado ao
  final" ("Não" / "Sim"; abre no padrão da empresa, `:44,52`), dica, **"Gerar link"** → `INSERT disc_assessments` (pending,
  `show_result_to_employee`) → copia `/avaliacao/<nome>-<código>` → toast **"Link gerado e copiado!"** com o endereço por 10 s
  (`EmployeeDiscOverview.tsx:388-415`; `hooks/useEmployeeDisc.ts:110-148`). Se a cópia falhar, o título vira "Link do ponto
  gerado" (P5).
- A aba "Perfil" da janela do funcionário (T15) tem o mesmo teste: "Perfil Comportamental (DISC)", "Gerar link do teste",
  "Copiar link", "Compartilhar", "Aguardando resposta"/"Respondido", "Ver relatório completo" (`components/employees/EmployeeDiscPanel.tsx`; emp `:704-732`).

### 3.2 Teste público (`pages/DiscAssessmentPublic.tsx`; disc `:24-66`)

- Carrega `get_disc_public(p_code)`: marca da empresa, primeiro nome e nome completo, status e se mostra o resultado
  (`:140-160`; `20260727090000_...sql:70-94`). Foto pela edge pública `disc-photo?code=` (`:181-195`).
- Intro: "Teste de Perfil Comportamental (DISC)", "Leva cerca de 5 minutos. Responda pensando no seu dia a dia.", "Olá, {nome}!",
  "Como funciona" (escala de arrastar, escolha, "Não existe resposta certa ou errada…"), aviso de sinceridade, **"Começar"**
  (`:439-506`).
- Perguntas: **28 por link**, sorteio fixo pelo código (mesmo link = mesmas perguntas, `:124-128`); escala de 5 níveis "Nada a ver
  comigo" … "Tudo a ver comigo" (começa no "Neutro", aceita ←/→ e 1 a 5) e perguntas de alternativa (exigem escolha); "Pergunta
  {n} de 28", "Voltar", "Avançar" (Enter avança), na última **"Enviar respostas"** ("Enviando...") (`:280-345,550-660`;
  `components/employees/disc/DiscScaleSlider.tsx`, `DiscChoiceSelect.tsx`).
- Envio: `submit_disc_assessment(p_code, p_answers, p_scores, …, p_locale)` — a pontuação é calculada no navegador
  (`:203-224`; `lib/disc/scoring`). Resultado liberado: **"Seu perfil comportamental"** com o relatório e "Ver PDF"
  (`:390-438`); oculto: **"Obrigado!"** — "Suas respostas foram registradas. A equipe de RH receberá o seu perfil." (`:382-389`).
  Reabrir um link já respondido e oculto: "Respostas já enviadas" (`:374-381`).

### 3.3 Perfil do funcionário (`components/employees/EmployeeProfileDetail.tsx`)

- No computador, lista da equipe à esquerda ("Buscar funcionário...") e ficha à direita (`EmployeeDiscOverview.tsx:429-467`).
- Cabeçalho com **"Ver PDF"** (dossiê, só com perfil respondido; "Gerando PDF...") e **"Nova avaliação"** ("Ao responder a nova
  avaliação, ela vira o perfil atual e a atual vai para o histórico.") (`:1082-1140`; emp `:838-840`).
- Sub-abas **"Visão geral"**, **"Interações"**, **"Histórico"** (`:977-979`):
  - Visão geral = relatório (`DiscReport.tsx`): "Perfil {código}" e nome do perfil (ex.: "O Executor"), "Sobre o seu perfil",
    "Gráfico DISC" (Dominância, Influência, Estabilidade, Conformidade), "Competências Comportamentais" (radar), "Perfil
    emocional", "Qualidades", "Pontos de atenção", "Motivadores de carreira" ("Fator predominante", "Fator de apoio", "Para
    refletir") e o aviso "Esta é uma ferramenta de autoconhecimento e comunicação de equipe. Não é um teste clínico nem um
    diagnóstico. Nenhum perfil é melhor ou pior que outro." (disc `:69-180`). Sem perfil: "Sem perfil ainda" + "Gerar link do teste" (`:1166-1171`).
  - Interações: "Como se comporta com" — escolha um colega ("Selecione um funcionário"; quem não respondeu aparece "ainda não fez a
    avaliação") → "Atritos", "Sinergias", "Melhor comunicação" e **"Ver comparação"** (PDF) (`:251-370`; emp `:791-805`).
  - Histórico: "Histórico de avaliações", **"Evolução do perfil"** (gráfico e radar por avaliação, texto "Comparando com a avaliação
    anterior: …"), "Linha do tempo" com "Ver desta data" (`:612-796`; emp `:807-841`). Uma só avaliação: "Faça uma nova avaliação
    para ver a evolução do perfil ao longo do tempo.".

### 3.4 "Comparar perfis" (`components/employees/EmployeeDiscCompare.tsx`)

"Comparar perfis" — "Selecione dois funcionários para ver a dinâmica entre eles." — "Primeiro funcionário", "Segundo funcionário"
→ "Gráfico DISC cruzado", "Radar de competências cruzado", "Atritos", "Sinergias", "Melhor comunicação"; "Voltar"
(`:303-425`; emp `:755-774`). Mesma pessoa: "Escolha dois funcionários diferentes.".

### 3.5 Organogramas — lista (`components/employees/orgchart/OrgChartTab.tsx`)

- "Monte a estrutura da sua empresa em um quadro visual", **"Novo Organograma"** (`:96`); vazio: "Nenhum organograma ainda" —
  "Crie um organograma para desenhar a estrutura da sua empresa, com funcionários e setores." (`:109-111`).
- Janela "Novo Organograma": "Nome do organograma" ("Ex: Estrutura 2026"), "Cancelar"/**"Criar"** (`:173-205`). Cartões com
  "{n} nós" e botões "Abrir", "Renomear" ("Renomear organograma"), "Excluir" ("Excluir organograma?" — "Esta ação não pode ser
  desfeita. O quadro e suas conexões serão perdidos.") (`:139-157,210-252`; emp `:1100-1122`).

### 3.6 Editor do organograma (`OrgChartCanvas.tsx`, `OrgChartFullscreen.tsx`, `OrgChartNode.tsx`)

- Quadro novo ganha a caixa **"Direção"** (manual), sem entrar no desfazer (`OrgChartCanvas.tsx:850-870`).
- Barra: **"Adicionar nó"**, **"Adicionar caixa"** ("Nova caixa"), **"Organizar"** ("Reposiciona automaticamente em árvore"),
  "Desfazer", "Refazer", **"Exportar"** ("Baixar imagem (PNG)", "Baixar PDF", "Sai no tema atual"; vazio: "Nada para exportar"),
  "Preferências" ("Linhas curvas", "Fundo" Pontos/Linhas/Xadrez/Nenhum, "Minimapa", "Encaixar na grade", "Guias de alinhamento"),
  "Tela cheia", selo "Salvando…"/"Salvo"; nome do organograma editável no topo (`:940-1110`; emp `:1123-1137,1193-1207`).
- "Adicionar nó" (`:1456+`; emp `:1139-1154`): aba **"Funcionário"** ("Buscar funcionário...", lista dos cadastrados,
  "Adicionar"; "Nenhum funcionário encontrado") ou **"Manual"** ("Nome \*" "Nome da pessoa ou cargo", "Cargo" "Ex: Diretor",
  "Setor" "Ex: Comercial", "Cor do setor", "Cor personalizada"). Pelo "+" das bordas de uma caixa, a nova já entra ligada
  (acima = chefe; abaixo/lados = subordinado) e a ramificação se reorganiza (`:603-650`); pela barra entra solta.
- Clique numa caixa → painel **"Editar nó"**: "Nome", "Cargo", "Setor", "Cor do setor" ("Sem cor"), "Aplicar aos de baixo",
  "Excluir nó", "Fechar"; caixa de funcionário: "Nome, cargo e foto vêm do cadastro do funcionário."; caixa de texto: "Texto da
  caixa", "Cor da caixa" (emp `:1155-1170`).
- Ligar à mão: arrastar da borda de uma caixa a outra (React Flow; a confirmar no robô).
- **Tela cheia** — "Ferramentas": "Adicionar caixa", **"Árvore"** (painel "Hierarquia": "Buscar pessoa...", "Expandir tudo",
  "Recolher tudo", "{n} pessoas"), **"Destacar por setor"** ("Limpar destaque"), **"Buscar pessoa"** ("Nome ou cargo...",
  "Ninguém encontrado."), "Fechar" (`OrgChartFullscreen.tsx:339-344`; `OrgChartTreeView.tsx`; emp `:1172-1192`).
- Celular: "Arraste e use os dedos para dar zoom. Edite pelo computador para a melhor experiência." (emp `:1138`).

### 3.7 Fluxogramas — lista (`components/employees/processes/ProcessesTab.tsx`; proc `:21-50`)

"Desenhe os processos da empresa em um fluxograma e documente como cada etapa deve ser feita.", **"Novo fluxograma"**; vazio
"Nenhum fluxograma ainda"; janela "Novo fluxograma": "Nome do fluxograma" ("Ex.: Abertura de ordem de serviço"), "Cancelar" /
**"Criar fluxograma"**; cartões "{n} etapas"; "Renomear fluxograma"/"Salvar"; "Excluir fluxograma?" — "Essa ação é permanente e
remove o fluxograma e tudo que foi desenhado nele.".

### 3.8 Editor do fluxograma (`ProcessCanvas.tsx`, `ProcessNode.tsx`, `ProcessLaneNode.tsx`, `ProcessEdge.tsx`)

- Nasce com **"Início"** no centro, pronto para renomear (`:625-646`).
- Barra (rótulos visíveis a partir de 1280 px, `:1312-1420`): **"Adicionar forma"** (lista com a dica de cada forma, ex.: Decisão
  "Use quando o caminho muda conforme uma condição, como Sim ou Não."), **"Adicionar raia"**, **"Formatar"** ("Alinha as caixas…
  sem mexer no seu arranjo."), **"Organizar"** ("Reposiciona todas as caixas do zero, da esquerda para a direita. Desfaz o arranjo
  manual."), "Desfazer"/"Refazer", **"Conferência do fluxograma"** (com número de problemas), **"Sobre o processo"**,
  **"Exportar"** ("Exportar como imagem", "Exportar como PDF", **"Baixar POP em PDF"**), "Configurações" ("Minimapa", "Alinhar à
  grade", "Guias inteligentes", "Estilo da linha" Curva/Reta, "Fundo"), "Tela cheia"/"Sair da tela cheia", selo de salvamento
  (proc `:74-111`).
- **"Editar etapa"** (clique numa forma, `:1789+`): "Nome da etapa" ("Ex.: Conferir peças no estoque"), "Como fazer", "Responsável"
  ("Selecionar funcionário" ou "Cargo ou setor (texto livre)"), "Duração" ("Ex.: 48h, 2 dias úteis"), "Cor", "Ícone" ("Padrão da
  forma"), "Fluxograma vinculado" (Subprocesso), "Aplicar esta cor a toda a raia", "Excluir etapa" (proc `:113-130`).
- Raia: "Nome da raia (setor ou responsável)", "Excluir raia"; conexão: "Tipo de conexão" "Sequência"/"Informação", "Rótulo (ex.:
  Sim, Não)" (proc `:103-110`).
- **"Conferência do fluxograma"** (`:1494-1540`): "Nenhum problema encontrado. O fluxograma está pronto para ser publicado." ou a
  lista com "Erro"/"Aviso" e "Ir até a etapa" (proc `:156-180`; regras em `lib/flowchart/validate.ts`).
- **"Sobre o processo"** (`:1615+`): "Objetivo", "Abrangência", "Disparo", "Dono do processo" ("Selecionar funcionário"),
  "Entradas", "Saídas" (listas com "Adicionar"/"Remover"), "Frequência" ("Ex.: por demanda, mensal"), "Área", "Indicadores"
  (proc `:132-154`).
- **POP** (`ProcessPopDocument.tsx`; proc `:183-222`): "Procedimento Operacional Padrão", "Processo", "Versão", "Emitido em", "Área",
  "Dono do processo", "Código", seções "Objetivo", "Escopo", "O que dispara o processo", "Entradas", "Saídas", "Responsabilidades"
  ("Cada faixa do fluxograma corresponde a um responsável:"), "Fluxograma" (o desenho), "Descrição das etapas" ("Siga para o passo
  {n} ({nome}).", "Se {condição}, vá para o passo…", "Fim do processo."), "Indicadores", "Histórico de revisões" ("Versão 1, de
  {data}"), aviso final. Abre em nova aba (`ProcessCanvas.tsx:850-860`; `utils/openPdfInTab.ts:44-90`).

---

## 4. Backend por tela

### 4.1 Chamadas

| Tela / ação | Tabelas | RPC / edge / storage | Linhas |
|---|---|---|---|
| Aba DISC | `employees`, `disc_assessments` (select de todas da empresa; insert pending) | — | `hooks/useEmployeeDisc.ts:71-148` |
| Perfil, histórico | `disc_assessments` por funcionário (todas / só respondidas) | — | `useEmployeeDisc.ts:166-274` |
| PDFs do DISC | `company_settings` (idioma, marca) | gerado no navegador (`utils/discDossierPdf`) | `EmployeeProfileDetail.tsx:905-950` |
| Teste público | — | RPCs `get_disc_public`, `submit_disc_assessment` (anon); edge `disc-photo` | `pages/DiscAssessmentPublic.tsx:140,181-224` |
| Organogramas | `org_charts` (select, insert, update `name`, update `data` com o grafo, delete) | — | `hooks/useOrgCharts.ts:80-170` |
| Fluxogramas | `processes` (select `id, name, data, meta, status, version, public_short_code, …`, insert, update, delete) | — | `hooks/useProcesses.ts:65-170` |
| Gatilhos | `ensure_public_short_code` (12 letras/números) em `disc_assessments`, `org_charts`, `processes`, `employees` | — | `supabase/migrations/20260620200000_public_short_codes_links_amigaveis.sql` (`generate_public_short_code`); `20261001130000_processes.sql:80-85` |

### 4.2 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Precisa | Situação | O que fazer |
|---|---|---|
| `employees` do fim do T15 (Tatiane + seis técnicos) | do T15 | herdar |
| `disc_assessments` | sem semente | perfis já respondidos (seção "Mundo" do plano) |
| `org_charts`, `processes` | sem semente | vazias no começo |
| RPCs `get_disc_public`, `submit_disc_assessment` | **sem handler** (`handlers/rpc/`) | criar: devolver marca, nomes, status e (se liberado) o resultado; gravar respostas e pontuação recebidas |
| Edge `disc-photo` | **sem handler** | foto da semente ou 404 (a tela cai nas iniciais) |
| `public_short_code` gerado por gatilho | o fakebase não tem gatilho | o handler/hook de insert precisa preencher (12 caracteres) |

---

## 5. Pegadinhas para roteiro e gravação

- **P1. [handoff, segurança/LGPD] (média, dentro da empresa) Respostas do DISC abertas a todos.** A policy "DISC visible to own
  company" libera SELECT de `disc_assessments` (respostas, pontuação, perfil) a qualquer usuário logado da empresa
  (`supabase/migrations/20260724120000_disc_perfil_comportamental.sql:101-104`); a tela só aparece para quem tem Funcionários, mas
  pela API um técnico lê o perfil comportamental dos colegas. O próprio comentário diz que espelha `employees` (ver T15 P19).
- **P2. [handoff, segurança] (baixa, dentro da empresa) Organograma e fluxograma editáveis por qualquer usuário.** Além da policy de
  gestores, "Users manage own company processes" (FOR ALL, só empresa) deixa qualquer usuário da empresa criar, alterar e apagar
  (`20261001130000_processes.sql:116-130`), "espelho EXATO" de `org_charts` (`:86-91`).
- **P3. [handoff, segurança/LGPD] (baixa) O link do DISC não expira.** Depois de respondido, `get_disc_public` continua devolvendo
  pontuação e perfil a quem tiver o link, se o resultado estiver liberado (`20260727090000_...sql:83-94`), e a foto sai pela edge
  pública `disc-photo` com o mesmo código (`pages/DiscAssessmentPublic.tsx:181-182`). O código tem 12 caracteres (~60 bits), então
  não é adivinhável; o risco é o link repassado.
- **P4. Tudo que é PDF abre nova aba; PNG/PDF do quadro baixam arquivo** (P13 do T15; `utils/openPdfInTab.ts:44-90`;
  `lib/canvas/graphExport.ts:384-386,511`). O gravador ainda não grava nova aba nem download.
- **P5. [handoff, texto] Aviso de link do DISC fala em ponto.** Se a cópia automática falhar, o toast do DISC usa "Link do ponto
  gerado" (`EmployeeDiscOverview.tsx:405-407`; emp `:668`).
- **P6. Tooltip do gráfico com pessoas reais.** Passar o mouse num fator mostra "Costuma ser associado a Steve Jobs…", "…Oprah
  Winfrey…", "…Warren Buffett…", "…Bill Gates…" (`components/employees/disc/DiscLineChart.tsx:303`; disc `:77-108`). Na gravação,
  não pairar o cursor sobre o gráfico.
- **P7. Comparação e histórico pedem semente.** "Comparar" exige 2+ funcionários com perfil (`EmployeeDiscOverview.tsx:490-500`);
  "Evolução do perfil" pede 2+ avaliações do mesmo funcionário (emp `:809,813`).
- **P8. [handoff] "Pronto para ser publicado" sem publicar.** A conferência diz "O fluxograma está pronto para ser publicado." (proc
  `:158`), mas não há ação de publicar: `status` fica "draft" e `version` em 1 (só a migration fala em incrementar, `20261001130000_processes.sql:57-58`;
  nenhum uso em `hooks/useProcesses.ts`). O POP sai sempre "Versão 1" e o "Histórico de revisões" tem uma linha só.
- **P9. Não existe compartilhar** organograma nem fluxograma (só o endereço da página, que exige login). A trilha cita "compartilhar"
  no cap. 13.
- **P10. Botões do fluxograma só com ícone abaixo de 1280 px** (`hidden xl:inline`, `ProcessCanvas.tsx:1313,1339,1343,1347`). A
  gravação em 1280×800 fica no limite: conferir que os rótulos aparecem (a confirmar).
- **P11. 28 perguntas é longo no vídeo.** Responder pelo teclado (1 a 5 e Enter) e acelerar a edição (selo 4x); as de alternativa
  pedem clique.
- **P12. Interação com o canvas.** Ligar caixas e mover formas é arrastar com o mouse (React Flow): testar o passo `drag` do robô
  (o T5 deixou o arrasto HTML5 como "testar antes"). O "+" das bordas e o "Organizar" evitam arrastar.

## 6. 🚫 Não prometer

- Compartilhar ou publicar organograma/fluxograma; controle de versões do POP (P8, P9).
- DISC como teste clínico, de aptidão ou de seleção (o próprio aviso da tela diz que não é).
- Envio automático do link do DISC por e-mail ou WhatsApp (só copiar/compartilhar pelo aparelho).
- Organograma montado sozinho a partir dos cargos (é desenhado à mão).

## 7. Dúvidas em aberto (só rodando)

1. O texto do resultado público para o perfil escolhido na semente (nome do perfil, ex.: "O Executor", vem de disc `:243+`).
2. Os rótulos da barra do fluxograma em 1280 px (P10) e o comportamento do "+" das bordas no organograma com o robô.
3. Onde o cartão "Perfil Comportamental" aparece em Configurações (aba Regional) e quem pode alterar.
4. Se o PDF do dossiê renderiza no Chromium da gravação (gerado no navegador, em nova aba).

## 8. Termos e pronúncias

DISC ("disque"), POP ("pópi" ou "procedimento operacional padrão"), PDF ("pê-dê-éfe"), PNG ("pê-ene-gê"); fatores
Dominância, Influência, Estabilidade, Conformidade; perfis por letras ("D I" = "dê i").
