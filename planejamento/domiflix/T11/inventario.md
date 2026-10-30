# Inventário funcional · T11 — Contratos e PMOC (Dominex)

> Base para o roteiro do tutorial "T11 · Contratos e PMOC". Levantado em 30/10/2026 contra o código publicado
> `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`. **Análise estática,
> somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). Fontes: `lib/i18n/messages/app/contracts.ts:16-812` (assistente, abas de
  ambientes/equipamentos, documentos, cobrança) e `lib/i18n/messages/app/pmoc.ts:11-1054` (lista, detalhe, PMOC, RT, portal).
- "PMOC" = Plano de Manutenção, Operação e Controle (Lei Federal 13.589/2018). "RT" = Responsável Técnico. "TRT" = Termo
  de Responsabilidade Técnica. "OS de contrato" = ordem de serviço com `contract_id` e `origin = 'contract'`.
- O assistente de contrato tem 5.039 linhas (`components/contracts/ContractFormDialog.tsx`); aqui está o que aparece na
  tela e o que importa para o vídeo. Termos e pronúncias: seção 8.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | PMOC não tem menu: é um tipo de contrato | **Bate** | `/pmoc` redireciona para `/contratos?tipo=pmoc` (`pages/PMOC.tsx:13-15`; `App.tsx:858`). O filtro "Tipo" fica em "PMOC" (`pages/Contracts.tsx:123-136`). |
| 2 | Tela Contratos: indicadores, filtros de status, saúde e tipo | **Bate** | 4 indicadores, filtros "Status", "Saúde", "Tipo", tabela com "Saúde" e "Próxima OS" (seção 3.1). |
| 3 | Wizard comum (5 etapas) × PMOC (6 etapas) | **Mudou** | Na **criação** são **6** etapas no comum e **7** no PMOC: entrou **"Financeiro"** (`ContractFormDialog.tsx:495-521`). Na edição o Financeiro sai (5 e 6). A chave PMOC é **"É um contrato PMOC?"** na 1ª etapa. |
| 4 | Etapa Unidade (PMOC): ambientes e equipamentos por ambiente | **Mudou** | Agora são duas etapas: **"Unidade & RT"** (endereço da unidade + RT) e **"Ambientes e Equipamentos"** (ambientes com área, carga térmica, ocupantes e, por máquina, "Escopo da norma", "Começa na visita" e "Checklists da Máquina") (`contracts.ts:71-249`). |
| 5 | Frequência: mensal, bimestral, trimestral, semestral, anual ou por dias | **Bate** | Atalhos "Mensal", "Bimestral", "Trimestral", "Semestral", "Anual" e, por dias, "Semanal", "Quinzenal", "30/45/60/90 dias" (`ContractFormDialog.tsx:522-536`). No PMOC o aviso "Cadência das visitas" recomenda mensal. |
| 6 | Etapa Equipe, revisão e OS geradas de uma vez | **Bate** | "Equipe & Cobrança" exige **"Técnicos Executores \*"**. Ao criar ativo, todas as visitas do horizonte (padrão 12 meses) viram OS na hora (`hooks/useContracts.ts:2213-2330`). |
| 7 | Detalhe: abas do comum × abas extras do PMOC | **Mudou** | Comum: "Visão Geral", "Ocorrências", **"Chamados"**, "Ambientes e Equipamentos", "Financeiro", "Documentos". PMOC: as mesmas + **"Histórico PMOC"** e **"Cronograma"** (`pages/ContractDetail.tsx:1631-1652`). |
| 8 | Aba Cronograma: verde/laranja/vermelho e PDF anual | **Bate** | Verde concluída, laranja pendente futura, vermelho atrasada (`components/pmoc/PmocCronogramaCalendar.tsx:87,107`); botão **"Imprimir PDF Anual"** (`pmoc.ts:488-500`). |
| 9 | Aba Documentos: TRT, Certificado, Dossiê e Planilha | **Bate, maior** | Mais: lista de pendências com link, assinatura do RT, "Documentos no portal do cliente" (Liberado/Oculto), histórico de versões, edição dos textos e **11 artes de Certificado** (Changelog 1.28.15) (`pmoc.ts:699-777`). |
| 10 | Responsáveis Técnicos em Configurações de Contrato | **Bate** | Botão **"Configurações de Contrato"** → abas **"Documentos"** e **"Responsáveis Técnicos"** (`pages/ContractSettings.tsx:39-40`). RT também se cadastra **na hora** dentro do contrato ("Cadastrar e selecionar"). |
| 11 | Aba Financeiro: única/parcelada, marcar paga, aplicar em massa | **Bate, maior** | Mais: **cobrança contínua** ("Sem prazo para terminar"), **nota fiscal automática**, **"Cobrar online"** (Asaas, T19), seleção em massa (`contracts.ts:747-811`; `pmoc.ts:194-362`). |
| 12 | Renovar (+6/+12) e o que gera; pausar e excluir | **Bate** | "Renovar / Estender" com "Estender por" 6 ou 12 meses (`ContractDetail.tsx:3318-3343`). Pausar/Retomar **só no menu da linha da lista** (`Contracts.tsx:763-771`). |

Avisos da trilha conferidos: ⚠️ "não falar em tela de PMOC" → **bate**. ⚠️ "OS geradas de uma vez, sem robô diário" → **bate**:
o cron `generate-pmoc-orders` foi desligado (`useContracts.ts:2213-2217`). ⚠️ "documentos só saem certos com empresa,
RT e cliente completos; a tela lista as pendências com link" → **bate** (`components/pmoc/PmocContractDocsTab.tsx:456-485`).
⚠️ "Cronograma e Histórico só no PMOC" → **bate**. ⚠️ "Pausar/retomar só na lista" → **bate**. ⚠️ "Excluir preserva o
pago e remove cobrança em aberto" → **bate no detalhe**; o diálogo da **lista** diz outra coisa (seção 5, item 4).
🚫 "assinatura eletrônica de contrato" → **continua não existindo** (a "assinatura" é a imagem do RT nos PDFs).

### 0.2 O que mudou desde a 1.22.5 (Changelog, `pages/Changelog.tsx`)

| Versão | Mudança |
|---|---|
| 1.24.44 | Etapa **Financeiro** no assistente; "Cobrar online" por parcela (`Changelog.tsx:3471,3466`). |
| 1.24.59-1.24.60 | Cobrança **sem prazo para terminar**; configurar cobrança depois; cobrar várias parcelas de uma vez (`:3120-3130,3098`). |
| 1.28.15 | Certificado de Conformidade com **arte em 11 modelos** e prévia (`:2391-2401`). |
| 1.35.8 | **Chamados** do portal aparecem dentro do contrato (`:1649`). |
| 1.37.22 / 1.37.31 / 1.37.35 | Documentos publicados no portal; **portal do contrato com senha por seção**; card do Portal do Contrato reorganizado (`:768,610,517`). |
| 1.37.55 | **Checklist personalizado por equipamento** no PMOC, separado dos da norma (`:157`). |

### 0.3 O que mais pode surpreender (seção 5)

1. Toda OS de contrato nasce com **assinatura do técnico obrigatória**, comum ou PMOC (`useContracts.ts:1199`).
2. Criar contrato PMOC dispara **sozinho** a geração de TRT, Certificado, Cronograma e Dossiê em segundo plano.
3. "Editar" no menu da linha da lista **só abre o detalhe**; a edição é pelo botão "Editar contrato" do detalhe.
4. "Pausar" não mexe nas OS já geradas (só muda o status) (a confirmar rodando).
5. A permissão "Gerenciar Contratos" não esconde nenhum botão; o banco é que recusa algumas gravações.
6. Os PDFs abrem em **outra aba** (o gravador não mostra).

---

## 1. Rotas e navegação

| Tela | Menu | Rota |
|---|---|---|
| Contratos | Grupo **"Gestão"** → **"Contratos"** (`components/layout/SidebarMenuContent.tsx:116`) | `/contratos` (`?tipo=pmoc` ou `?tipo=comum` pré-filtra) |
| Detalhe do contrato | Clique na linha | `/contratos/:id` (aceita `nome-<código>`, `hooks/usePmocPortal.ts:52-92`) |
| Configurações de Contrato | Botão **"Configurações de Contrato"** na lista | `/configuracoes-contrato?tab=documentos|rt` (`App.tsx:862`) |
| Endereços antigos | — | `/pmoc` → `/contratos?tipo=pmoc`; `/responsaveis-tecnicos` → `/configuracoes-contrato?tab=rt` (`App.tsx:858,864`) |
| Portal público do contrato | Card "Portal do Contrato" da Visão Geral | `/contrato/unidade/<token ou nome-código>` (alias `/pmoc/unidade/...`) (`App.tsx:771-773`) → T12 |

Guardas: `screen:contracts` + módulo `contracts` (`App.tsx:859-862`).

---

## 2. Permissões e módulos

| Item | Regra | Fonte |
|---|---|---|
| Tela | `screen:contracts` ("Contratos" — "Contratos recorrentes, PMOC e as visitas programadas de cada um.") | `hooks/usePermissions.ts:61` |
| Ação | `fn:manage_contracts` ("Gerenciar Contratos") **não é consultada pela tela**; o banco a usa em `can_manage_contracts` (gravações do PMOC) | `supabase/migrations/20260613120000_can_manage_contracts_pmoc.sql:12-28,81-82` |
| Excluir parcela do contrato | admin/gestor ou `fn:delete_finance` gravado | `ContractDetail.tsx:361` |
| Técnicos executores | Usuários com papel `tecnico` + equipes | `hooks/useProfiles.ts:22-39` |
| Módulo 🔒 `contracts` | **"Gestão de Contratos e PMOC"** — "Gestão de contratos, Portal do Contrato e Portal do PMOC públicos, documentos (TRT, Certificado, Cronograma, Dossiê)" | `components/ModuleGateModal.tsx:113-115`; `hooks/useCompanyModules.ts:57-59` |
| Planos | Módulo pago desde 2026-06; incluído no Pro e no Business (no seed do fakebase: `avancado` e `master`) | `useCompanyModules.ts:57-59`; `rec/fakebase/seeds/gen-01-tenant.json` |
| Módulos que mudam abas | `cobrancas` + conta Asaas ("Cobrar online", "Faturamento Recorrente"), `nfe` (nota automática) | `pmoc.ts:250-301,451-468`; `contracts.ts:787-811` |

---

## 3. Por tela, janela e aba

### 3.1 Lista de Contratos (`pages/Contracts.tsx`)

- Título **"Contratos"**, subtítulo **"Gerencie contratos recorrentes e manutenções programadas"**; botões **"Configurações
  de Contrato"** e **"Novo Contrato"** (`Contracts.tsx:359-392`; `pmoc.ts:14-19`).
- Indicadores: **"Contratos Ativos"**, **"OSs Geradas (mês)"**, **"Próximas 7 dias"**, **"Vencendo em 30d"** (`Contracts.tsx:240-270`).
- Busca **"Buscar por nome, cliente ou telefone..."**; botão **"Filtros"** com **"Status"** (Ativo, Pausado, Cancelado,
  Expirado), **"Saúde"** (Em dia, Manutenção Pendente, ATENÇÃO) e **"Tipo"** (PMOC, Comum (não-PMOC))
  (`components/contracts/ContractsFilterButton.tsx`; `pmoc.ts:24-49`).
- Tabela: "Status", "Contrato", "Cliente", "Frequência", "Saúde", "Próxima OS", "Itens", "Ações" (`Contracts.tsx:661-681`).
  Selos "Acabando" e, no PMOC, o chip "Lei 13.589" (`components/pmoc/PmocComplianceBadge.tsx`; `pmoc.ts:479-486`).
- **Saúde** (visão `contract_health_status`): 0 OS vencidas sem concluir → "Em dia"; 1 → "Manutenção Pendente"; 2 ou mais →
  "ATENÇÃO" (`supabase/migrations/20260523164907_pmoc_v1_9_0_fundacao.sql:280-307`).
- Menu da linha: **"Visualizar"**, **"Pausar"**/**"Retomar"** (aviso "Status do contrato atualizado!"), **"Editar"** (abre o
  detalhe), **"Excluir"** (`Contracts.tsx:755-790`; `useContracts.ts:2528-2536`).
- Excluir pela lista: **"Excluir contrato"** / "Tem certeza? Todas as OSs, ocorrências e transações vinculadas serão
  excluídas." + "{n} OSs vinculadas serão apagadas junto." + caixa **"Tenho certeza que desejo excluir"** → "Excluir"
  (`pmoc.ts:88-97`).
- Vazio: "Nenhum contrato cadastrado" / "Crie seu primeiro contrato para gerar OSs automaticamente." + "Novo Contrato".

### 3.2 Assistente "Novo Contrato" / "Editar Contrato" (`components/contracts/ContractFormDialog.tsx`)

Etapas (barra no topo): **Comum** = "Identificação" → "Ambientes e Equipamentos" → "Frequência" → "Equipe & Cobrança" →
"Financeiro" → "Revisão". **PMOC** = "Identificação" → **"Unidade & RT"** → "Ambientes e Equipamentos" → "Frequência" →
"Equipe & Cobrança" → "Financeiro" → "Revisão" (`:495-521`; `contracts.ts:23-31`). Botões "Cancelar", "Voltar", "Próximo",
**"Criar Contrato"** ("Salvando…") ou "Salvar Alterações" (`contracts.ts:399-407`). Guarda **rascunho** (mesmo padrão
"Rascunho encontrado" do T3) (`ContractFormDialog.tsx:700-735`).

#### 3.2.1 Identificação (`contracts.ts:58-69`; `ContractFormDialog.tsx:2540-2580`)

- **"Nome do Contrato \*"** ("Ex: Manutenção Preventiva Mensal — Empresa X"; "Dê um nome claro que identifique este contrato").
- **"Cliente \*"** ("Selecione o cliente", busca "Buscar cliente...", "+" "Cadastrar novo cliente").
- Interruptor **"É um contrato PMOC?"** — "Plano de Manutenção, Operação e Controle. Ative para vincular um Responsável
  Técnico e gerar OSs com selo de conformidade legal." Ligar limpa o Tipo de Serviço. Na edição, ligar ou desligar pede
  confirmação ("Transformar em contrato PMOC?" / "Desligar PMOC deste contrato?", `contracts.ts:422-439`).

#### 3.2.2 Unidade & RT — só PMOC (`contracts.ts:71-107`)

- **"Responsável Técnico (RT)"** com dica: "Engenheiro ou Técnico em Refrigeração com CFT/CREA que assina o Termo de
  Responsabilidade Técnica conforme Lei Federal 13.589/2018. Diferente do Técnico Executor (quem executa as OSs no campo)."
  Lista "Selecione o RT..." ou "— Sem RT atribuído —", botão "+" (**"Novo Responsável Técnico"**: cadastro rápido com o nome e
  dados essenciais, "Cadastrar e selecionar", `pmoc.ts:779-785`). Rodapé: "...Pode ser definido depois."
- **"Identificação da Unidade"**: "Endereço do ambiente climatizado deste contrato (a loja/site). Pode ser diferente do
  endereço do cliente. Pré-preenchido a partir do cliente..." Campos "Nome da unidade / local" ("Ex: Loja Centro, Galpão
  2…"), "Endereço (logradouro)", "Número", "Complemento", "Bairro", "CEP", "Cidade", "UF".
- Selo **"Conforme Lei Federal 13.589/2018"** / "OSs sairão com selo de conformidade." e o quadro **"O que o PMOC
  desbloqueia"** (TRT, Dossiê, Cronograma anual em PDF, portal com QR Code, selo nas OSs).

#### 3.2.3 Ambientes e Equipamentos (`contracts.ts:156-249`)

- Título "Ambientes climatizados" (PMOC) ou "Ambientes" (comum); **"Adicionar ambiente"**; vazio "Nenhum ambiente cadastrado"
  / "Cadastre os ambientes climatizados deste contrato."
- Ambiente: **"Identificação do ambiente"** ("Ex: 2º andar — Sala 201"), **"Tipo de atividade"** ("Ex: Escritório
  administrativo"), **"Área climatizada (m²)"** (+ **"Calcular"**: largura × comprimento, "Usar"), **"Carga térmica (TR)"**
  (dica "TR (Tonelada de Refrigeração)... 1 TR = 12.000 BTU/h."), **"Nº de ocupantes fixos"**, **"Nº de ocupantes
  flutuantes"** (com dicas), "Equipamentos deste ambiente" + **"Adicionar equipamento"** (busca "Buscar equipamento do
  cliente...", "Criar novo equipamento", confirmar "Adicionar").
- Por máquina no PMOC: **"Escopo da norma"** — "Expansão Direta" (Split, Cassete, Piso Teto, Hi-wall, Janela, ACJ) ou
  "Sistemas Centrais" (VRF, Chiller, Fan Coil, UTA, Self Contained); **"Começa na visita"** — "Visita 1 (Mensal)", "Visita 3
  (Mensal + Trimestral)", "Visita 6 (+ Semestral)", "Visita 12 (Anual — revisão completa)" (`components/contracts/pmocMachineRoutine.ts:132-140`);
  **"Checklists da Máquina"** ("Preparando os checklists da norma…"; "Essencial" ou "Norma completa"; checklists
  personalizados do T4 também entram). Tabela de perguntas com "Frequência" (Mensal, Trimestral, Semestral, Anual, Eventual)
  e **"Na 1ª OS?"** (`contracts.ts:560-588,607-642`).
- Remover: "Remover ambiente?" / "Remover equipamento do ambiente?" (no PMOC o equipamento sai do contrato) (`contracts.ts:410-421`).

#### 3.2.4 Frequência (`contracts.ts:109-154`)

- **"Tipo de Frequência"**: "A cada X meses" / "A cada X dias"; **"Atalhos rápidos"**; **"Intervalo (meses) \*"**;
  **"Data de Início \*"**; **"Horizonte (meses)"** (padrão **12**, intervalo padrão **1 mês**, início = hoje,
  `ContractFormDialog.tsx:326-330`).
- **"Prévia das visitas"** (lista ou calendário) com "Fim de semana" quando cair em sábado/domingo.
- PMOC: alertas **"Cadência das visitas"** ("A Lei 13.589/2018 recomenda visita mensal no PMOC — é o padrão e a escolha mais
  segura...") e **"Rotina por equipamento"**; cadência diferente de mensal mostra "Cadência personalizada selecionada — fora
  do mensal recomendado pela norma."
- **"Opções avançadas — serviços com frequência própria"** com "Adicionar do catálogo PMOC" (no PMOC fica travado pelo
  padrão da norma).

#### 3.2.5 Equipe & Cobrança (`contracts.ts:250-268`)

**"Técnicos Executores \*"** (técnicos e equipes; "Selecione ao menos 1 técnico ou equipe para executar."), **"Responsáveis
Financeiros (Cobrança)"** (usuários), **"Tipo de Serviço"** (comum; "Opcional. Escolher um tipo define a cor e o rótulo das
OSs na agenda."), **"Checklist Padrão"** ("Pode ser sobrescrito por item"), **"Observações (opcional)"**, interruptor
**"Contrato Ativo"** ("OSs só serão geradas para contratos ativos"). Sem executor: toast "Sem responsável pela execução".

#### 3.2.6 Financeiro — só na criação (`contracts.ts:274-310,747-772`)

"Como e quando receber" / "Tudo aqui é opcional...". Interruptor **"Já gerar as parcelas a receber"**; "Descrição da parcela"
("Mensalidade do contrato"), **"Valor de cada parcela"** ("Cada parcela nasce com este valor. Não é um total dividido."),
"Primeiro vencimento", "Frequência da cobrança", "Quantas parcelas" (já igual ao horizonte), "Conta de recebimento",
"Categoria", "Forma de pagamento prevista"; "Duração da cobrança": "Por um período" / **"Sem prazo para terminar"**. Resumo
"Como vai ficar": "{n} parcelas de {valor}, somando {total}".

#### 3.2.7 Revisão e criação

- "Revisão do Contrato" em frases ("Este é um contrato PMOC chamado ... para o cliente ...", "O plano começa em ... e cobre
  12 meses, gerando 12 visita(s)", "O responsável técnico é ...") (`contracts.ts:312-397`).
- **"Criar Contrato"**: grava contrato, ambientes e itens; se **ativo**, gera **todas** as OS do horizonte na hora
  (status "agendada", 08:00, descrição "{nome} — Visita {n}", `require_tech_signature: true`) (`useContracts.ts:1188-1205,2213-2330`);
  gera as parcelas se pedido. Avisos: **"✅ Contrato PMOC criado com {n} OSs geradas na agenda"** (ou "⚠️ ... {n} de {total}"),
  "Contrato criado com sucesso!", "{n} parcelas lançadas no Financeiro"; PMOC sem RT: "⚠️ Sem Responsável Técnico (RT)
  definido"; PMOC: "Gerando documentos do contrato…" / "TRT, Certificado, Cronograma e Dossiê estão sendo criados em segundo
  plano." (`contracts.ts:448-471`; `ContractFormDialog.tsx:2283,2451-2465`). Depois abre o detalhe (`Contracts.tsx:826`).
- Editar datas/frequência/serviços: **"Recalcular visitas futuras?"** (refaz só as futuras não realizadas) (`contracts.ts:440-446`).

### 3.3 Detalhe do contrato (`pages/ContractDetail.tsx`)

Cabeçalho: nome, cliente, status, selo PMOC; **"Editar contrato"** e **"Excluir contrato"** (`:1590-1606`). Abas na seção 0.1.

- **Visão Geral** (`pmoc.ts:120-176`): faixa "Contrato acabando" (≤ 30 dias do fim → atalho para renovar,
  `ContractDetail.tsx:1452,1655-1670`); "Informações" (Cliente, Frequência, Início, Horizonte, Observações); **"Portal do
  Contrato"** ("Portal Público", "Copiar link", "Imprimir QR Code", "Regenerar token", "Quem vê o quê no portal" com
  Oculto/Sem senha/Com senha — detalhes no T12); "Resumo" (Frequência, Início, Horizonte, "Total de ocorrências", "Próxima OS")
  com **"Renovar / Estender"**, **"Plano de Manutenção"** e **"Relatório de Visitas"**; "Progresso" ("{x} de {y} concluídas ({p}%)").
- **Ocorrências**: "Ocorrências ({n})": "#", "Data", "Dia", "OS", "Serviços", "Status", "Ações" (pular = "Cancelar esta
  visita?" → "Cancelar visita") (`pmoc.ts:178-193,392-397`).
- **Chamados**: chamados abertos pelo portal para este contrato (`ContractDetail.tsx:1636`; T12).
- **Ambientes e Equipamentos**: edição com barra "Alterações não salvas. Salvar recalcula as visitas futuras..." e
  "Descartar"/"Salvar alterações" (`contracts.ts:513-558`).
- **Histórico PMOC**: "Prova de cumprimento da Planilha, tarefa por tarefa, em cada visita."; vazio "Sem execução registrada
  ainda" (`pmoc.ts:503-548`).
- **Financeiro** (3.5). **Documentos** (3.4; no comum: anexos "Documentos anexados" + "Liberar documentos no portal").
- **Cronograma**: "Cronograma do contrato" / calendário Dia/Semana/Mês, cores verde/laranja/vermelho, **"Imprimir PDF
  Anual"**; sem OS: "Gerar OSs deste contrato agora" (`pmoc.ts:488-501,968-976`).

### 3.4 Documentos do PMOC (`components/pmoc/PmocContractDocsTab.tsx`; `pmoc.ts:699-777`)

- **"Documentos no portal do cliente"** com selo "Liberado"/"Oculto" e botão "Liberar documentos no portal do cliente".
- **"Dados faltando pra gerar documentos PMOC"**: lista com link de cada pendência — "Razão social da empresa", "CNPJ da
  empresa" (→ Configurações, Empresa), "Nome do Responsável Técnico", "Modalidade do RT", "CFT/CREA do RT" (→ Responsáveis
  Técnicos), "Cliente vinculado...", "CNPJ/CPF do cliente", "Endereço do cliente" (`:456-485`).
- **"Assinatura do RT pendente"** + **"Adicionar assinatura agora"** (enviar foto ou desenhar; "Assinatura cadastrada!").
- Cartões: **"Dossiê PMOC"** ("capa + Termo de Responsabilidade Técnica + Certificado de Conformidade + Cronograma Anual";
  "Gerar Dossiê completo"/"Baixar última versão"), **"Termo de Responsabilidade Técnica"** ("Válido até", "Gerar TRT", "Baixar
  TRT", "Editar texto"), **"Certificado de Conformidade"** (idem, com arte), **"Planilha PMOC"** (ambientes, RT, equipamentos e
  o plano com periodicidade e mapa de 12 meses), "Histórico de versões ({n})". Selos "Assinado", "Sem assinatura", "Não gerado".
- Avisos: "Dossiê PMOC gerado!", "TRT gerado!", "Certificado gerado!", "Cronograma anual gerado!", "Planilha PMOC gerada!"
  (ou "... já estava atualizado") (`hooks/useGeneratePmocDocument.tsx:175-372`); erros traduzidos com botão de atalho (ex.:
  "CNPJ da empresa não cadastrado" → "Ir pra Configurações") (`utils/pmocErrorMessages.ts:27-93`). Validade padrão 12 meses
  (`hooks/useCompanyPmocDocTemplates.ts:32-34`). O PDF abre em nova aba (`PmocContractDocsTab.tsx:965`).

### 3.5 Financeiro do contrato (`pmoc.ts:194-362`; `contracts.ts:747-811`)

- Indicadores "Previsto", "Recebido", "Pendente", "Atrasado"; "Contas a Receber"; botões **"Nova Receita"**, **"Aplicar a
  todas"**, interruptor "Agenda" ("Cobranças visíveis na agenda").
- Sem parcelas: "Este contrato ainda não tem cobrança" + **"Configurar cobrança"**.
- "Nova Conta a Receber": "Descrição", "Valor (R$)", "Conta bancária / caixa", "Categoria", "Data de Vencimento (1ª
  parcela)", "Recorrência" (Única, Mensal, Bimestral, Trimestral, Semestral, Anual), "Quantidade de parcelas" → "Criar {n}
  Parcelas" ("{n} parcelas criadas").
- Linha: "Pago"/"Pendente"/"Atrasado", "Vence ...", ações "Marcar como pago", "Editar" ("Somente esta" / "Todas pendentes"),
  "Excluir"; seleção em massa (editar/excluir {n}). Cobrança contínua: "Cobrança contínua", "Alterar", "Desligar". 🔒 "Cobrar
  online" (T19) e "Nota fiscal automática" (T14).

### 3.6 Renovar, pausar e excluir

- **"Renovar / Estender contrato"**: "Estende este contrato e gera o próximo ciclo de visitas, continuando de onde a última
  visita parou. As visitas existentes não são alteradas." "Estender por" **6** ou **12** meses, "Horizonte atual" → novo,
  botão **"Renovar +{n} meses"**. Avisos "Contrato renovado!" / "{n} nova(s) visita(s) geradas até {data}."; inativo:
  "Contrato inativo" / "Reative o contrato antes de renovar." (`pmoc.ts:364-374`; `useContracts.ts:3442-3634`).
- **Pausar/Retomar**: só no menu da linha da lista; grava só `status` (`useContracts.ts:2528-2536`).
- **Excluir pelo detalhe**: "Tem certeza que deseja excluir o contrato {nome}?" + "Serão excluídos junto com o contrato:"
  ({n} ordens de serviço vinculadas, {n} cobrança(s) em aberto, {n} itens, alertas na agenda) + "{n} recebimento(s) já
  realizado(s) será(ão) preservado(s) no caixa" + caixa "Tenho certeza que desejo excluir" → **"Excluir tudo"**
  (`pmoc.ts:376-390`). Na prática: OS **futuras** apagadas, **passadas** mantidas no histórico sem vínculo, recebido
  preservado, em aberto removido; aviso "Contrato excluído com sucesso!" com o resumo (`useContracts.ts:3752-3781`).

### 3.7 Configurações de Contrato (`pages/ContractSettings.tsx`; `pmoc.ts:470-476`)

- "Configurações de Contrato" / "Documentos e responsáveis técnicos"; abas **"Documentos"** e **"Responsáveis Técnicos"**.
- **Documentos**: "Modelos padrão de documentos PMOC" (TRT = página 2 do Dossiê; Certificado = página 3), "Restaurar texto
  padrão", "Editar texto", **"Validade dos documentos"** (meses; padrão 12) (`pmoc.ts:845-871`).
- **Responsáveis Técnicos** (`pages/ResponsibleTechnicians.tsx`; `pmoc.ts:1013-1047`): "Cadastro regulatório PMOC (Lei
  13.589/2018)", indicadores Total/Ativos/Inativos, **"Novo Responsável"**; tabela Nome, CFT/CREA, Modalidade, Registro,
  Contato, Status, Ações (Editar/Inativar). Formulário (`pmoc.ts:786-834`): **"Nome completo"** ("Ex: João da Silva"),
  **"CFT/CREA"** ("Ex: CREA-SP 1234567"), **"Modalidade"** ("Ex: Engenheiro Mecânico"), **"Número de registro (ART/TRT)"**
  ("Ex: ART 1234567/2026"), "Email", "Telefone", **"Assinatura digitalizada"** e **"Carimbo do responsável"** (abas "Enviar
  imagem" / "Desenhar"; PNG ou JPG até 2 MB), "Observações", "Cadastro ativo". Botões "Cadastrar responsável" / "Salvar
  alterações". Imagens no bucket `responsible-technicians-media` (`hooks/useResponsibleTechnicians.ts:211-238`).

---

## 4. Backend por tela

### 4.1 Lista e detalhe

| Chamada | Detalhe | Fonte |
|---|---|---|
| `GET contracts` | `select=*,customers(id,name,document,phone,celular,email,address,city,state),customer:customers(id,name),responsible_technician...,contract_items(...),contract_environments(...),service_orders(...)` | `hooks/useContracts.ts`; `rec/fakebase/desconhecidos.log` |
| `GET contract_health_status` | Visão: saúde por contrato | `hooks/useContractHealth.ts:41` |
| `GET responsible_technicians?select=*&order=full_name.asc` | RT | `useResponsibleTechnicians.ts:69` |
| `GET contracts?select=public_pmoc_token,public_short_code,name&id=eq.` | Portal | `usePmocPortal.ts:24-48` |
| `GET pmoc_documents` | Versões dos PDFs | `hooks/usePmocDocuments.ts:76` |
| `GET financial_transactions` (do contrato), `financial_accounts`, `financial_categories` | Aba Financeiro e etapa Financeiro | `ContractDetail.tsx`; `ContractFormDialog.tsx` |
| `GET contract_activity_execution` | Visão do Histórico PMOC | `hooks/useContractPmocExecution.ts` |

### 4.2 Criar contrato (cliente → banco, na ordem)

1. `POST contracts` (com `is_pmoc`, `responsible_technician_id`, `unidade_*`, frequência, horizonte, status...) →
   `contract_environments` → `contract_items` (um por equipamento, com `pmoc_scope`/`pmoc_start_visit`).
2. PMOC/plano: `POST /rest/v1/rpc/replace_contract_plan_activities` `{ p_contract_id, p_activities }` + releitura de
   `contract_plan_activities` (`useContracts.ts:2193-2200`).
3. Se ativo: `regenerate_contract_visits` **só** com a flag `regenerate_contract_visits_rpc` ligada em `app_feature_flags`
   (`useContracts.ts:1896,1660-1685`; `hooks/useFeatureFlag.ts:10-32`); senão (padrão) o navegador grava **cada OS**:
   `POST service_orders`, `POST service_order_equipment`, `POST service_order_assignees`, atividades em lote (`useContracts.ts:1340-1372`).
4. Parcelas: `POST financial_transactions` em lote (etapa Financeiro).
5. PMOC: `autoGeneratePmocDocsV1` chama em sequência `GET /functions/v1/generate-pmoc-trt-pdf|certificado-pdf|cronograma-pdf|dossie-pdf?contract_id=`
   com o token do usuário (`useGeneratePmocDocument.tsx:84-110,124-150`).
- Abrir o PMOC no assistente chama `POST /rest/v1/rpc/ensure_pmoc_norm_templates` (cria os 4 checklists da norma da
  empresa) e lê `form_templates` com perguntas e `pmoc_activity_catalog` (`hooks/usePmocNormTemplates.ts:78-111`;
  `hooks/usePmocActivityCatalog.ts:153`).

### 4.3 Outras ações

| Ação | Chamada |
|---|---|
| Documentos | `GET /functions/v1/generate-pmoc-<doc>-pdf?contract_id=` → `{ pdf_url, version, cached, signature_status? }`; 400 com `{ error: "cnpj_missing" | "rt_missing" | ... }`; 404 = "Geração de PDF em breve" |
| Imprimir QR Code | função `generate-pmoc-qr-pdf` (`supabase/functions/generate-pmoc-qr-pdf/`) |
| Regenerar token | `POST /rest/v1/rpc/regenerate_pmoc_token` `{ p_contract_id }` (`usePmocPortal.ts:101`) |
| Renovar | `GET profiles`, `GET contracts?select=start_date,...`, `PATCH contracts` (horizonte), novas OS (`useContracts.ts:3442-3610`) |
| Pausar/Retomar | `PATCH contracts?id=eq.` `{ status }` |
| Excluir | apaga OS futuras e dependentes (`service_order_assignees`, `service_order_equipment`, `form_responses`, `os_photos`, `service_ratings`, `service_order_activities`), desvincula passadas, apaga parcelas em aberto, apaga o contrato (`useContracts.ts:1688-1700,3752`) |
| RT | `responsible_technicians` insert/update + upload em `responsible-technicians-media` |

### 4.4 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Item | Hoje | Falta |
|---|---|---|
| Clientes e equipamentos do T3 (Hotel Mirante do Mar com 4 equipamentos, documento e endereço) | **Coberto** (`seeds/gen-02-cadastros.json`) | — |
| Empresa com razão social e CNPJ em `company_settings` | **Coberto** (Glacial Cold Brasil, 91.520.340/0001-07) | — |
| Técnicos (papel `tecnico`) | **Coberto** (6 do seed) | Permissões do T2 |
| `service_types`, `form_templates`/`form_questions` (T4) | **Sem seed** (`desconhecidos.log`) | Seeds do mundo do T4 (tipo "Manutenção Preventiva", checklist de split) |
| `pmoc_activity_catalog` | **Sem seed** (`desconhecidos.log`) | Copiar o catálogo da norma das migrações `20260617200000_pmoc_activity_catalog_fase2.sql` (~150 linhas) e `20260628150000_pmoc_catalog_essencial_e_grupos.sql` (dado de referência, não do cliente) |
| RPC `ensure_pmoc_norm_templates` | **Sem handler** (resposta vazia: a máquina fica "sem checklist da norma") | Handler que cria os 4 `form_templates` de norma (expansão direta/sistemas centrais × essencial/complementar) com `form_questions` a partir do catálogo |
| RPC `replace_contract_plan_activities` | **Sem handler** | Insere em `contract_plan_activities` e devolve a contagem |
| `app_feature_flags` | Vazia (`seeds/00-vazias.json`) → geração de OS pelo navegador | Nada (bom para o vídeo) |
| `service_orders.order_number` | Sem gatilho: toda OS nasceria com **0** | Hook de numeração sequencial por empresa (vale também para T5/T7) |
| `contracts.public_pmoc_token` | Sem gatilho (link "Link público em geração. Aguarde alguns instantes.") | Hook: 32 hex no insert (`20260611110747_contract_portal_token_generalize.sql:37-81`); `public_short_code` já sai pela regra genérica (`core/defaults.mjs:58-62`) |
| Visão `contract_health_status` | Sem provedor (não há `handlers/views/`) | Provedor com a regra 0/1/2+ OS vencidas |
| Funções `generate-pmoc-*-pdf` e `generate-pmoc-qr-pdf` | **Sem handler** ("Resposta inválida da geração de PDF.") | Handlers que gravam `pmoc_documents` e devolvem `pdf_url` de um PDF fictício servido pelo storage falso |
| `financial_accounts` / `financial_categories` | Sem seed | Padrões do cadastro da empresa: contas "Caixa" e "Conta Principal"; categorias incluindo **"Contratos PMOC"** (entrada) (`supabase/functions/self-register/index.ts:985-1037`) |
| Storage `responsible-technicians-media` | Upload genérico aceito (`http/storage.mjs`) | Imagem fictícia de assinatura e carimbo |
| Nova aba (PDF) | O gravador segue na aba original (`rec/README.md`, "Limites") | Mostrar só a geração e o histórico de versões, ou ilustração |

---

## 5. Pegadinhas para roteiro e gravação

**[handoff]** = vale pedir correção ao time do app.

1. **[handoff]** A trilha falava em "5 × 6 etapas"; hoje são 6 × 7 na criação (Financeiro) e 5 × 6 na edição.
2. Toda OS de contrato nasce com assinatura do técnico obrigatória (`useContracts.ts:1199`), não só a do PMOC (trilha T5 dizia o contrário).
3. **[handoff]** "Editar" no menu da linha da lista só navega para o detalhe (`Contracts.tsx:772-776`).
4. **[handoff]** O diálogo de excluir da **lista** diz "Todas as OSs, ocorrências e transações vinculadas serão excluídas."
   (`pmoc.ts:89`), mas a exclusão preserva OS passadas e recebimentos (`useContracts.ts:3756-3776`); o do detalhe está certo.
5. Pausar só grava `status` (`useContracts.ts:2528-2536`): as OS futuras já geradas continuam na agenda (a confirmar).
   "Contrato Ativo" desligado na criação = nenhuma OS gerada.
6. **[handoff]** `fn:manage_contracts` não é usada pela tela (nenhum uso em `src/` fora do catálogo); botões aparecem a quem
   tem a tela e o banco recusa algumas gravações PMOC (`20260613120000_can_manage_contracts_pmoc.sql:81-82`).
7. Os PDFs abrem em outra aba (`PmocContractDocsTab.tsx:965`); no vídeo, mostrar o aviso de geração e a versão.
8. Criar PMOC dispara a geração automática dos documentos; se faltar dado, a falha é silenciosa (`ContractFormDialog.tsx:2451`).
9. Assinatura do RT: a "assinatura" do PMOC é a **imagem** do RT nos PDFs; sem ela o PDF sai com "linha em branco pra
   assinar à mão" (`pmoc.ts:713-714`).
10. Etapa Financeiro só existe na criação; depois, só pela aba Financeiro ("Configurar cobrança").
11. "Valor de cada parcela" é por parcela, não total ("Não é um total dividido."). Erro comum de narração.
12. Datas: "Contrato acabando" aparece a 30 dias do fim (`ContractDetail.tsx:1452`); "Renovar" só em contrato ativo.
13. Cadência fora do mensal no PMOC mostra aviso "fora do mensal recomendado pela norma" (comportamento esperado).
14. As visitas do PMOC agrupam por mês o que vence de cada máquina conforme "Começa na visita"; na cadência personalizada
    vale a frequência por pergunta (`contracts.ts:229`).
15. **[handoff]** Mensagem "⚠️ Sem Responsável Técnico (RT) definido" usa emoji no título do aviso; idem "✅ Contrato PMOC criado
    com..." (`contracts.ts:451`; `ContractFormDialog.tsx:2463`).

---

## 6. 🚫 Não prometer / telas mortas

- 🚫 Menu ou tela "PMOC" (`/pmoc` só redireciona). 🚫 Robô que gera OS todo dia (geração única, na criação/renovação).
- 🚫 Assinatura eletrônica do contrato pelo cliente. 🚫 Orçamento ou oportunidade virar contrato automaticamente (T9/T10).
- 🚫 Cronograma e Histórico PMOC em contrato comum. 🚫 Pausar pelo detalhe.
- 🚫 Envio automático do Dossiê ao cliente: o caminho é liberar no portal (T12) ou baixar e mandar.
- Telas mortas: `pages/PMOC.tsx` (redirect), `pages/ResponsibleTechnicians.tsx` como rota própria (redirect; o conteúdo vive
  em Configurações de Contrato).

---

## 7. Dúvidas em aberto

1. Pausar esconde ou cancela as OS futuras na agenda? (item 5).
2. Com o catálogo e os templates da norma semeados, quantas perguntas a "Visita 12" mostra no Hi-Wall (para a fala)?
3. Comportamento do "Imprimir QR Code" (abre PDF em nova aba?).
4. Ordem visual dos dois avisos ao criar ("✅ ..." e "Contrato criado com sucesso!").
5. "Carga térmica (TR)" tem calculadora no assistente? (`components/contracts/CargaTermicaCalculatorModal.tsx` existe; ver se
   o botão aparece ao lado do campo).

---

## 8. PMOC: regras e termos (com pronúncia sugerida para a Fernanda)

| Termo na tela | O que é (fonte) | TTS sugerido |
|---|---|---|
| PMOC | Plano de Manutenção, Operação e Controle (`contracts.ts:67`) | pê-móqui (testar; alternativa "pê, ême, ó, cê") |
| Lei Federal 13.589/2018 | Lei que exige o PMOC (`contracts.ts:100`) | lei federal treze mil quinhentos e oitenta e nove, de dois mil e dezoito |
| RT (Responsável Técnico) | Engenheiro/técnico com CFT/CREA que assina o TRT (`contracts.ts:73`) | érre tê |
| TRT | Termo de Responsabilidade Técnica (`pmoc.ts:727`) | tê érre tê |
| CFT / CREA | Conselhos profissionais do RT | cê éfe tê / créa |
| ART | Anotação de Responsabilidade Técnica (campo "Número de registro (ART/TRT)") | a érre tê |
| TR | Tonelada de Refrigeração; 1 TR = 12.000 BTU/h (`contracts.ts:186-187`) | tê érre; "doze mil bê-tê-ús por hora" |
| m² | Área climatizada | metros quadrados |
| Expansão Direta / Sistemas Centrais | Escopo da norma por máquina (`contracts.ts:214-219`) | normal |
| VRF, UTA, ACJ, fan coil, chiller, self contained | Tipos de sistema (`contracts.ts:216-219`) | vê érre éfe; u tê á; a cê jota; fên cóil; tchíler; sélfi contêined |
| Mensal / Trimestral / Semestral / Anual / Eventual | Frequências da norma (`contracts.ts:49-55`) | normal |
| Dossiê PMOC | Capa + TRT + Certificado + Cronograma (`pmoc.ts:719`) | dossiê pê-móqui |
| Ocupantes fixos / flutuantes | Pessoas permanentes / de passagem (`contracts.ts:190-197`) | normal |

Regras que a fala pode usar (todas do código): visita mensal recomendada; o técnico executor não é o RT; os documentos
dependem de empresa (razão social e CNPJ), RT (nome, modalidade, CFT/CREA) e cliente (documento e endereço); TRT e
Certificado valem 12 meses por padrão; "Começa na visita 12" faz a revisão anual completa na primeira visita.
