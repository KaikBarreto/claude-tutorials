# Inventário funcional · T15 — Funcionários: Financeiro do Funcionário e Ponto Eletrônico (Dominex)

> Base para o roteiro do tutorial "T15 · Funcionários: Financeiro do Funcionário e Ponto Eletrônico". Levantado em 31/10/2026
> contra o código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T14.
> O Guia Técnico (`docs/guia-tecnico/secoes/T15.html`) ajudou a achar as telas; onde diverge, vale o código (lista na seção 0.4).
> Perfil Comportamental, Organograma e Fluxograma (abas da mesma tela) ficam no T22; Equipes ficou no T5.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...`, `docs/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). **emp** = `lib/i18n/messages/app/employees.ts` (bloco pt-br `:9-1210`);
  **tc** = `lib/i18n/messages/app/timeclock.ts` (ponto público, bloco pt-br `:9-179`); **fin** = `lib/i18n/messages/app/finance.ts`.
- Três "saldos" diferentes aparecem nesta aula e não se misturam: o **saldo do funcionário** (salário ± vale, bônus e falta,
  livro `employee_movements`), o **caixa da empresa** (`financial_transactions`) e o **saldo de horas** do ponto (`time_sheets`).
  O ponto **não** mexe no saldo financeiro nem na folha (seção 5, P10).

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Tela **Funcionários**: cadastro, financeiro individual e ponto | **Bate, reorganizada** | Título **"Funcionários (RH)"**, subtítulo "Gerencie funcionários, vales, pagamentos e extratos" (emp `:305-308`). Abas na lateral: "Funcionários", **"PJ/MEI"** (nova), "Equipes", **"Controle de Ponto"**, "Perfil Comportamental", "Organograma", "Fluxograma" (`pages/Employees.tsx:373-388`; emp `:311-319`). No computador a lista abre com a ficha ao lado ("Lista de Funcionários", "Selecione um funcionário") desde a 1.37.40 (`pages/Changelog.tsx:431-432`). |
| 2 | Cadastro: dados, foto, chave PIX, admissão | **Bate** | **"Novo Funcionário"** → janela com abas **"Dados"**, **"Pagamento"**, **"Ponto eletrônico"**, **"Perfil"** (`components/employees/EmployeeFormDialog.tsx:376-389`). Único obrigatório: "Nome Completo \*" (`:295`). Rascunho automático (`:117-133`). |
| 3 | Remuneração: salário, custo mensal, campos CLT | **Bate, com outro nome** | A aba chama **"Pagamento"** (emp `:700`). "Salário \*", "Custo mensal total" + **"Calcular"**, bloco "Contrato de trabalho" com **"Regime"** "Informal"/"CLT"/"PJ/MEI" e, fora de PJ, "CBO", "Matrícula", "Dependentes (IRRF)", "Vale-transporte" (`EmployeeFormDialog.tsx:461-611`). O asterisco do salário **não é validado** (P3). |
| 4 | Configuração de pagamento: frequência e dia | **Bate** | "Configuração de Pagamento": "Frequência" (Mensal/Quinzenal/Semanal), "Tipo de dia" (Dia útil/Dia corrido), "N° dia útil do mês"/"Dia do mês", padrão 5º dia útil (`:617-698`; emp `:950-974`). É ela que faz a folha nascer em Contas a Pagar (cap. 10). |
| 5 | **Vincular acesso ao sistema**: login do funcionário | **Bate, com risco** | Ainda na aba "Pagamento": "Vincular a um usuário do sistema" (usuário que já existe) e "Criar acesso ao sistema" (cria login com papel técnico) (`:701-765`). O login criado por aqui **nasce sem permissões gravadas = acesso a tudo** (P1, segurança, alta). |
| 6 | **Vale, falta e bônus** | **Bate** | Ações "Vale", "Bônus", "Falta" na ficha (`components/employees/EmployeeListDetail.tsx:125-146`). Só o **vale** vira saída na hora (RPC `create_employee_vale`, `supabase/migrations/20260922120000_employee_vale_atomico.sql:492-717`); bônus e falta ficam no saldo (`pages/Employees.tsx:771-795`). "Descontar do banco de horas" também desconta dinheiro (P4). |
| 7 | **Pagar funcionário**: informal × CLT (holerite) e desconto do vale | **Bate** | "Pagamento, {nome}": "Tipo de pagamento" "Normal / Informal" / "CLT" (`EmployeePaymentModal.tsx:377-395`); CLT mostra INSS, IRRF, vale-transporte e "Líquido a pagar" e **abre o holerite em nova aba** (`pages/Employees.tsx:974-990`). Tabela de 2026 = a de 2025, provisória (P6). |
| 8 | **Ponto**: link público e bater ponto pelo celular | **Mudou** | O ponto tem aba própria no cadastro, **"Ponto eletrônico"** ("Ative o acesso individual do funcionário ao ponto pelo celular.", emp `:975-982`). Ao salvar ligado, o sistema copia o **link de ativação** (`/ativar-ponto/<token>`, cadastro facial com "Continuar sem biometria") quando ainda não há biometria, senão o link do ponto (`pages/Employees.tsx:507-557`). |
| 9 | Aba **Ponto** do gestor: Hoje, Histórico, Relatório, Configurações | **Bate, com rótulos novos** | A aba chama **"Controle de Ponto"** e as sub-abas **"Hoje"**, **"Histórico"**, **"Relatório"**, **"Config"** (emp `:13-18`; `components/time-tracking/AdminTimePanel.tsx:20-55`). Em "Config" ficam o link do **quiosque** ("Ponto em grupo (quiosque)") e as chaves "Exigir selfie"/"Exigir geolocalização", que **já vêm ligadas** (P8). |
| 10 | A **folha** em Contas a Pagar e quitada de lá | **Bate, com ressalva** | Folha criada por cron diário com 35 dias de antecedência ("Folha {nome} — {AAAA-MM}", categoria "Folha de Pagamento") (`supabase/migrations/20261019030000_competencia_no_fuso_da_empresa_folha_e_recebivel.sql:65-152`; `supabase/functions/generate-payroll/index.ts:54`). Quitar por Contas a Pagar abre o mesmo modal com "Quitando folha pendente, período …" (`EmployeePaymentModal.tsx:367-371`), mas **ignora o modo CLT** (P5). |

Avisos da trilha:

- ⚠️ "Vale gera despesa na hora. Bônus e falta não" → **bate** (`pages/Employees.tsx:771-795`; RPC grava `financial_transactions` paga, categoria "Funcionários", descrição "Vale - {nome}", `20260922120000_...sql:657-689`).
- ⚠️ "Criar acesso exige e-mail e senha de 6+" → **bate** ("Email é obrigatório para criar acesso", "Senha deve ter pelo menos 6 caracteres", `EmployeeFormDialog.tsx:296-298`).
- ⚠️ "Holerite CLT abre em popup" → **bate** (`pages/Employees.tsx:974-990`): bloqueado, vira o aviso "Pagamento registrado." / "Libere os pop-ups para ver o holerite, ou reabra pelo extrato do funcionário." (emp `:683-684`). Regra de 30/10: não encenar o bloqueio.
- ⚠️ "Selfie e localização só se a empresa exigir" → **bate, mas o padrão é exigir**: sem configuração gravada, as duas valem `true` (`supabase/migrations/20260308163937_f394308f-3dcd-4b96-864a-ee67ec9de54c.sql:63-64`; `supabase/functions/time-clock-portal/index.ts:1020-1023`; `components/time-tracking/TimeSettings.tsx:41-42`).
- 🚫 "Não existe botão Gerar Folha" → **continua** (nenhum botão; só o cron `20260426020000_payroll_cron_schedule.sql:27-43`).
- 🚫 "Não existe tela separada de ponto para o gestor" → **continua** (é a aba "Controle de Ponto").

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.24.15 | Vale não conta mais duas vezes no resultado | `:4198` |
| 1.24.33 | Ponto em grupo (tablet), PIN por funcionário, ponto no fuso da empresa | `:3707,3712,3717` |
| 1.25.0 / 1.25.1 | Teste facial opcional; ponto em aba própria do cadastro; quiosque reconhece pelo rosto | `:2975,2953,2938` |
| 1.25.4 / 1.25.5 / 1.25.6 | Um único link para ativar o ponto; biometria numa leitura; link do quiosque nas configurações | `:2902,2890,2878` |
| 1.25.7 | Vale e saída financeira sempre sincronizados (RPC atômica) | `:2866` |
| 1.28.12 | Mais de uma jornada no mesmo dia; histórico e relatório por jornada | `:2451,2461` |
| 1.36.13 | Prestadores PJ e MEI em aba própria, com contrato | `:1440,1445` |
| 1.37.40 / 1.37.42 | Lista com a ficha ao lado; mais espaço | `:431,372` |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. O login criado em "Criar acesso ao sistema" tem acesso a todas as telas (P1, segurança). O Guia diz o contrário.
2. A senha aparece por extenso no aviso "Acesso ao sistema criado!" por 15 segundos (P2): problema para a gravação.
3. "Valor a Pagar" mostra a fórmula "{subtotal} - {desconto} (vales)", mas o subtotal **já tirou** os vales (P7).
4. Quitar a folha por Contas a Pagar com "CLT" escolhido paga o valor sem INSS/IRRF e não abre holerite (P5).
5. "Raio máximo (metros)", "Tolerância atraso (min)" e "Permitir fora do horário" são gravados e **não fazem nada** (P9).
6. A folha só aparece **no dia seguinte** ao cadastro (cron das 04:00) e já com o mês seguinte (janela de 35 dias).
7. Pagar pela tela de Funcionários **quita a folha pendente mais antiga** do funcionário, seja de que mês for (P12).

### 0.4 Guia Técnico × código (handoff de texto para o time do app)

| Guia (`docs/guia-tecnico/secoes/T15.html`, cap.) | Código 1.38.6 |
|---|---|
| Cap. 1: "Excluir funcionário? Todos os dados e movimentações serão perdidos." / "Excluir ambos" / "Só o funcionário" | É **arquivar**: "Arquivar funcionário?", "Arquivar e excluir usuário", "Só arquivar", "Arquivar" (emp `:386-396`; RPC `archive_employee`, `supabase/migrations/20260920002000_preserva_time_records_ao_excluir_funcionario.sql:39-93`) |
| Cap. 3: "Salário — Sim — Validação: Salário é obrigatório" | Sem validação: só o nome é exigido (`EmployeeFormDialog.tsx:293-299`); a mensagem existe e não é usada (emp `:1044`) |
| Cap. 5: "O acesso criado por aqui nasce com perfil Técnico… não dá acesso a nada além do perfil Técnico" | Nasce sem `user_permissions` = modo legado com acesso total (P1) |
| Cap. 7: "Falta descontada do banco de horas não mexe no saldo financeiro" | Mexe: `falta_banco` entra em "Faltas" e no subtotal (P4) |
| Cap. 9: aba "Ponto" com "Gera um link público pro funcionário bater o ponto pelo celular" e toast "Link gerado e copiado!" | Aba "Ponto eletrônico", texto "Ative o acesso individual…"; sem biometria o toast é "Link de ativação copiado!" (emp `:669,977`) |
| Cap. 10: "Situações possíveis: … Atrasado"; "Raio máximo… em relação ao ponto de referência"; Relatório com "Exportação em CSV"; "Herda empresa (08:00-18:00)" | "Atrasado" nunca é calculado (P9); raio sem efeito; o CSV está no **Histórico** (`components/time-tracking/TimeHistory.tsx:189-215`); padrão 08:00-17:00 (`TimeSettings.tsx:38-39`) |
| Cap. 11: "ponto → horas → folha → conta a pagar" | O ponto não alimenta saldo, falta nem folha (P10) |

### 0.5 O que a empresa ganha ao nascer (cadastro) e toca esta aula

Conferido nas duas portas de cadastro (`supabase/functions/self-register/index.ts:728-1052`,
`supabase/functions/create-company/index.ts:330-557`), no RPC `seed_company_catalog`
(`supabase/migrations/20260718120000_seed_company_catalog_i18n.sql:10-247`: só tipos de serviço, status de OS e tipos de tarefa) e
nos gatilhos `AFTER INSERT ON companies`:

- **Funcionários, cargos e escalas:** nada. Não existe tabela de cargos ("Cargo" é texto livre, seção 3.3). `time_settings` e
  `time_schedules` não têm semente nem no cadastro nem em migration (só o `CREATE TABLE`,
  `supabase/migrations/20260308163937_f394308f-3dcd-4b96-864a-ee67ec9de54c.sql:45-57`): nascem no primeiro "Salvar configurações"
  da aba "Config" (seção 3.10; `useTimeRecords.ts:686-725`); até lá a tela mostra os padrões do código (08:00-17:00,
  `TimeSettings.tsx:38-39`).
- **Três nomes para o dinheiro do salário:** o cadastro cria a categoria "Salários e Encargos" (`self-register/index.ts:1009`;
  `create-company/index.ts:514`), que nenhum fluxo desta aula usa; a folha usa "Folha de Pagamento", criada na primeira folha
  (`supabase/migrations/20261019030000_competencia_no_fuso_da_empresa_folha_e_recebivel.sql:86-96`); vale e pagamento gravam o
  texto "Funcionários", sem categoria cadastrada (P12). Handoff junto com a P12.
- **Contas:** "Caixa" e "Conta Principal" (`self-register/index.ts:1033-1038`; `create-company/index.ts:538-542`), as que
  aparecem em "De qual conta sai o vale?" ("Caixa (em dinheiro)") e em "Pagar com" (seções 3.4 e 3.5).
- **Ponto e biometria:** nada no cadastro; o link do quiosque nasce no primeiro pedido (RPC `get_or_create_ponto_kiosk_slug`,
  seção 4.1).

---

## 1. Rotas e navegação

| Tela | Caminho no menu | URL | Componente |
|---|---|---|---|
| Funcionários (RH) | Gestão › **Funcionários** (`components/layout/SidebarMenuContent.tsx:117`, módulo `rh`) | `/funcionarios` (`App.tsx:869`) | `pages/Employees.tsx` |
| Abas Perfil/Organograma/Fluxograma (T22) | dentro de Funcionários | `/funcionarios/perfil/:param`, `/funcionarios/organograma[/:param]`, `/funcionarios/fluxogramas[/:param]` (`App.tsx:872-880`) | mesma página |
| Endereço antigo de equipes | — | `/equipes` → `/funcionarios` (`App.tsx:868`) | — |
| Ponto pessoal (sem login) | link copiado | `/ponto/<slug>` (`App.tsx:747`) | `pages/PontoPublico.tsx` → `components/ponto/PontoScreen.tsx` |
| Ativação do ponto + cadastro facial (sem login, 24 h) | link copiado | `/ativar-ponto/<token>` (`App.tsx:753`; alias `/cadastro-facial/:token` `:755`) | `pages/FaceEnrollment.tsx` |
| Quiosque (tablet da empresa, sem login) | Config › "Ponto em grupo (quiosque)" | `/ponto/empresa/<kioskSlug>` (`App.tsx:750`) | `pages/PontoKiosk.tsx` |
| Folha em Contas a Pagar | Financeiro › "Contas a Pagar/Receber" (`SidebarMenuContent.tsx:179`) | `/financeiro/contas` | `components/financial/FinanceContas.tsx` |

- Não há `?tab=` para as abas de Funcionários: a aba é estado da página (`pages/Employees.tsx:154-162`). As sub-abas do ponto
  também são estado (`AdminTimePanel.tsx:14`). O robô clica nelas.
- Slug do ponto: `<nome-sem-acento>-<8 letras/números>` (`supabase/migrations/20260916140000_guarda_posse_ponto_reassign_e_fecha_rpcs_mortas.sql:135-235`, código em `:147,224`), gerado uma vez e permanente.

## 2. Permissões e módulos

| O quê | Regra | Onde |
|---|---|---|
| Tela Funcionários | Permissão "Funcionários" (`screen:employees`, "Cadastro de funcionários, folha de pagamento e controle de ponto.") **e** módulo `rh` | `hooks/usePermissions.ts:89`; `App.tsx:869`; `hooks/useCompanyModules.ts:62` |
| Módulo | **"Funcionários / RH"** — "Gestão de funcionários, ponto eletrônico, movimentações financeiras de colaboradores" (fallback do aviso de upgrade) | `components/ModuleGateModal.tsx:117-120` |
| Aba "Controle de Ponto" | admin/gestor **ou** "Gerenciar Ponto" (`fn:manage_timeclock`) **ou** "Gerenciar Funcionários" (`fn:manage_employees`) | `pages/Employees.tsx:371,379-381`; `usePermissions.ts:127-128` |
| Vale | Servidor exige admin/gestor, acesso total ou "Gerenciar Financeiro" (`fn:manage_finance`): "Sem permissão para gerenciar o Financeiro" | `20260922120000_...sql:541-560` |
| Excluir vale no extrato | admin/gestor ou "Excluir Lançamento Financeiro" com registro (`can_delete_finance`) | `components/employees/EmployeeExtract.tsx:105-108`; `20260922120000_...sql:471-486` |
| Arquivar | admin/gestor ou `fn:manage_employees` (RPC) | `20260920002000_...sql:55-66` |
| Criar acesso | `can_manage_users` na edge `create-user` | `supabase/functions/create-user/index.ts:143-151` |
| Registro manual de ponto | só admin/gestor ("Só administrador ou gestor pode lançar batida em outra data.") | `hooks/useTimeRecords.ts:609-631`; emp `:101` |
| Ponto pessoal sem o módulo `rh` | **continua funcionando** (gate desligado de propósito); o quiosque exige o módulo | `supabase/functions/time-clock-portal/index.ts:135-150,490-492` |

Na Glacial (todos os módulos ligados, Camila admin) aparece tudo.

---

## 3. Por tela

### 3.1 Funcionários (RH) — cabeçalho e lista (`pages/Employees.tsx:1073-1404`)

- Cabeçalho: "Funcionários (RH)", subtítulo, selo com a contagem (só Informal/CLT ativos, `:203-206,1084`), alternância
  lista/grade (`ViewModeToggle`) e **"Novo Funcionário"** (`:1085-1092`; emp `:328`).
- Computador, modo lista (padrão): coluna "Lista de Funcionários" com busca "Buscar por nome ou cargo..." e ordenação "A-Z" /
  "Mais recente" / "Mais antigo"; cada linha com foto, nome, "cargo · telefone" e o **saldo** em selo verde/vermelho
  (`:1102-1130`; emp `:322-338`). Sem seleção: "Selecione um funcionário" — "Escolha um funcionário na lista para abrir a
  ficha e as ações disponíveis." (`:1161-1165`). Sem ninguém: "Nenhum funcionário cadastrado" — "Clique em "Novo
  Funcionário" para começar" (`:1154-1159`; emp `:344-345`).
- Grade (cartões) e celular: as ações viram menu ("Visualizar", "Vale", "Bônus", "Falta", "Pagamento", "Link do ponto",
  "Editar", "Arquivar") (`:1307-1361`; emp `:361-371`).

### 3.2 Ficha do funcionário (`components/employees/EmployeeListDetail.tsx`)

- Topo: foto, nome, cargo, selo do regime ("Informal"/"CLT"/"PJ/MEI") e, com ponto ligado, selo "Controle de Ponto";
  botões **"Editar"**, **"Extrato"**, **"Arquivar"** (`:84-123`).
- Faixa **"Movimentações"**: **"Vale"**, **"Bônus"**, **"Falta"**, **"Pagamento"** e, com ponto, **"Link do ponto"** (copia
  `/ponto/<slug>`, toast "Link gerado e copiado!") (`:125-146`; `pages/Employees.tsx:1057-1066`).
- Números: "Salário", "Saldo atual", "Vales", "Bônus", "Faltas", "Pagamento" (`:148-177`).
- Blocos "Contrato de trabalho" ("Data de Admissão", "Regime", "Matrícula", "CBO", "CPF", "Chave PIX") e "Dados" ("Telefone",
  "Email", "Endereço") (`:179-199`).

### 3.3 Janela "Novo Funcionário" / "Editar Funcionário" (`components/employees/EmployeeFormDialog.tsx`)

Título "Novo Funcionário"/"Editar Funcionário" (com PJ/MEI vira "Novo Prestador"/"Editar Prestador") (`:359`). Rodapé
fixo: "Cancelar" e **"Criar Funcionário"** (edição: "Salvar"; PJ: "Criar Prestador") (`:343-353`). Rascunho: ao reabrir,
pergunta se retoma (só os campos da aba Dados e salário, `:117-133,362-373`).

**Aba "Dados"** (`:391-459`):

| Campo | Máscara / regra | Linhas |
|---|---|---|
| Foto ("Adicionar foto do funcionário" / "Trocar foto") | imagem até 5 MB ("Arquivo muito grande (máx 5MB)"), vai para o bucket privado `employee-photos` | `:392-422,198-219`; emp `:851-854,1047-1048` |
| "Nome Completo \*" | placeholder "Nome do funcionário"; único obrigatório ("Nome é obrigatório") | `:425-428,295` |
| "CPF" | máscara CPF/CNPJ, "000.000.000-00" | `:429-432` |
| "Telefone" | "(00) 00000-0000" | `:433-436` |
| "Email" | "email@exemplo.com"; vira obrigatório com "Criar acesso" | `:437-440,296` |
| "Cargo" | "Ex: Técnico" | `:441-444` |
| "Endereço" | "Endereço completo" (texto livre, sem CEP) | `:445-448` |
| "Data de Admissão" | seletor de data | `:449-452` |
| "Chave PIX" | máscara; "CPF, email, telefone ou chave aleatória" | `:453-456` |

**Aba "Pagamento"** (`:461-766`):

- "Salário \*" (moeda; colar "4.550" não vira centavos) e, fora de PJ, "Custo mensal total" + botão **"Calcular"** ("Salário +
  encargos + benefícios") (`:463-485`). "Calcular" abre **"Calcular Custo Mensal"** (o mesmo da precificação, T9:
  "Salário e Encargos", "Benefícios mensais", "Custos anuais (rateado ÷ 12)", "Jornada", "Regime tributário da empresa",
  "Custo Total Mensal", "Hora Homem (HH)", botões "Cancelar"/"Aplicar {valor}") (`components/service-orders/MonthlyCostCalculatorModal.tsx`; `lib/i18n/messages/app/crm.ts:1024-1074`).
  Aplicar preenche o custo e, se o salário estiver vazio, o salário (`EmployeeFormDialog.tsx:819-833`).
- "Contrato de trabalho" → **"Regime"**: "Informal" (padrão), "CLT", "PJ/MEI" (`:490-510`). Fora de PJ: "CBO" ("Ex: 7156-10"),
  "Matrícula" ("Ex: 00123"), "Dependentes (IRRF)", "Vale-transporte" Não/Sim → "Valor mensal do VT" (`:513-572`). Os campos
  CLT aparecem também no Informal (só somem no PJ). Trocar para PJ desliga o ponto: "Ponto eletrônico desativado: o regime
  PJ/MEI não usa ponto." (`:275-283`; emp `:686`).
- "Configuração de Pagamento" (fora de PJ): "Frequência" "Mensal"/"Quinzenal"/"Semanal"; "Tipo de dia" "Dia útil"/"Dia corrido";
  "N° dia útil do mês" ou "Dia do mês" (1 a 31, padrão 5); quinzenal "1° pagamento"/"2° pagamento" (5 e 20); semanal "Dia da
  semana" (padrão Sexta-feira). Dica: "Valor da folha aparece automaticamente em Contas a Pagar conforme essa configuração."
  (`:617-698`; padrões `:88-92`).
- "Vincular a um usuário do sistema": lista "Nenhum" + todos os usuários da empresa ("nome (telefone)"); dica "Vincula este
  funcionário a um usuário existente no sistema" (`:701-720`; emp `:1018-1023`).
- "Criar acesso ao sistema" (só na criação ou em edição sem usuário vinculado): interruptor com "Cria automaticamente um
  usuário com perfil Técnico"; sem e-mail: "Preencha o email acima para criar o acesso"; "Login de acesso" (o e-mail);
  "Senha temporária (gerada automaticamente)" (campo **em texto aberto** + "Gerar", "Anote a senha, ela será exibida apenas uma
  vez") ou "Senha \*" com indicador de força ("Crie uma senha segura", "Defina a senha que o funcionário usará para acessar o
  sistema") (`:723-765`; emp `:1024-1037`).

**Aba "Ponto eletrônico"** (fora de PJ, `:769-800`):

- Cartão "Ponto eletrônico" — "Ative o acesso individual do funcionário ao ponto pelo celular." — interruptor
  "Desativado"/"Ativado" (`:771-788`; emp `:975-982`).
- Com o ponto ligado: **"PIN do ponto"** (opcional, "Protege a batida dele no tablet compartilhado da empresa."; "Definir PIN",
  4 ou 6 dígitos; em funcionário novo, "Salve o funcionário primeiro para poder definir um PIN.") (`components/employees/PontoPinField.tsx`; emp `:983-1001`)
  e **"Acesso individual ao ponto"** ("Um único link ativa a biometria e depois abre o ponto do funcionário.", selo
  "Aguardando ativação"/"Acesso configurado", "Gerar link de ativação", "Link permanente do ponto" + "Copiar ponto", "As fotos
  não são enviadas nem armazenadas, apenas a assinatura matemática do rosto."; novo: "Salve o funcionário e ative o ponto para
  gerar o link de ativação.") (`components/employees/FaceBiometricsField.tsx:84-185`; emp `:1002-1016`).

**Aba "Perfil"**: teste DISC (T22) (`:806-815`).

**Ao salvar** (`pages/Employees.tsx:559-679`; `hooks/useEmployees.ts:71-98`): `INSERT/UPDATE employees` → "Funcionário
criado!" / "Funcionário atualizado!". Se o ponto foi **ligado agora**: RPC `generate_ponto_slug`; RPC
`get_employee_face_template_status`; sem biometria, RPC `create_employee_face_enrollment_link` e o link copiado é o de
**ativação** (`/ativar-ponto/<token>`), toast **"Link de ativação copiado!"** com o endereço por 10 s; com biometria, o link
do ponto ("Link gerado e copiado!") (`:507-557`; emp `:666-671`). Com "Criar acesso": edge `create-user` (papel `tecnico`,
`employee_id`), depois `employees.user_id`, toast **"Acesso ao sistema criado!"** — "Email: {email}, Senha: {password}" por
15 s (`:638-676`; emp `:673-674`). Falha: "Funcionário criado, mas erro ao criar acesso" (emp `:676`). Foto nova de funcionário
vinculado vira o avatar do usuário (`:580-587`).

### 3.4 "Registrar Vale / Bônus / Falta — {nome}" (`components/employees/EmployeeMovementModal.tsx`)

- Título "Registrar {Vale|Bônus|Falta} — {nome}" (`:204`), faixa "Saldo atual: R$ …" (`:221-225`).
- **Vale**: "De qual conta sai o vale? \*" (lista só caixa/banco ativos; Caixa aparece "Caixa (em dinheiro)"; a primeira já vem
  marcada), "Centro de custo" só se houver centros ativos (`:229-261`; `pages/Employees.tsx:360-363`). Sem conta: "Nenhuma conta
  ou caixa ativo encontrado. Cadastre uma conta em Financeiro, Contas e Cartões." (emp `:471-472`).
- **Falta**: "Tipo de desconto" "Descontar do salário" ("Valor será deduzido do saldo financeiro") / "Descontar do banco de
  horas" ("Registra {h}h negativas no banco de horas"); valor **sugerido** = salário ÷ dias úteis do mês (22 por padrão):
  "Sugestão: R$ …/dia (8.0h/dia · 176h/mês)"; caixa "Aplicar perda de DSR" (dobra o valor no modo salário) e resumos "Total
  desconto" (`:264-377,103-116`; `utils/employeeCalculations.ts:300-303`; `hooks/useEmployeeWorkHours.ts:61-71`).
- Comuns: "Valor \*", "Descrição" ("Observação opcional..."), "Cancelar" / **"Registrar {tipo}"** (`:193-201,286-297,379-382`).
- Ao registrar: vale → RPC `create_employee_vale` (idempotente) → "Vale registrado!"; bônus/falta → `INSERT employee_movements`
  → "Movimentação registrada!" (`pages/Employees.tsx:771-795`; `hooks/useEmployeeMovements.ts:53,65-84`).

### 3.5 "Pagamento, {nome}" (`components/employees/EmployeePaymentModal.tsx`)

- Esquerda: "Tipo de pagamento" ("Normal / Informal" e "CLT"; PJ trava em "PJ/MEI"; abre no regime do funcionário,
  `:168-170,356,377-395`); com vales: **"Descontar dos Vales"** (vazio = 100%; "Total de vales: R$ …, Padrão: 100%" e
  "Restante: R$ … (será relançado)") (`:434-450`); **"Pagar com"** (contas ativas com saldo, "Conta Principal" primeiro,
  `:137-150,453-485`); "Centro de custo" (se houver); "Observações (opcional)" (`:498-506`).
- Direita, informal: "Salário", "Total de Bônus", "Descontos" (Vales, Faltas), "Subtotal", **"Valor a Pagar"** com a linha
  "{subtotal} - {desconto} (vales)" (`:609-659`). CLT: "Proventos" (Salário, Total de Bônus, "Total de proventos"),
  "Descontos" (INSS, IRRF, "Vale-transporte", Faltas, Vales), **"Líquido a pagar"**, "Bases de cálculo" (Base INSS, Base IRRF,
  Base FGTS, "FGTS do mês (recolhido)") e o aviso "Valores calculados com base nas tabelas vigentes de INSS, IRRF e FGTS. São
  estimativas, confirme com o seu contador antes de fechar a folha." (`:528-608,663-667`; emp `:516`).
- Rodapé "Cancelar" / **"Confirmar Pagamento"** (desligado com valor ≤ 0 ou sem conta; líquido negativo: "Descontos maiores que
  os proventos, líquido negativo. Ajuste os vales ou faltas antes de pagar.") (`:306-350`).
- Ao confirmar (`pages/Employees.tsx:799-1011`): movimento "pagamento" ("Movimentação registrada!"), "ajuste" "Reset para
  salário base" (com o detalhamento), "vale_residual" se sobrou vale; quita a **folha pendente mais antiga** do funcionário
  (`:907-941`) ou cria a saída "Pagamento de salário - {nome}" (categoria "Funcionários", `:942-964`). CLT: abre o **holerite**
  em nova aba (`:974-990`). Informal: **"Deseja gerar Recibo?"** — "O recibo do pagamento será aberto em uma nova página para
  impressão ou download em PDF." — "Não" / "Sim, gerar recibo" (nova aba) (`:1633-1679`; emp `:565-570`).

### 3.6 "Extrato, {nome}" (`components/employees/EmployeeExtract.tsx`)

- **"Exportar"** (página do extrato em nova aba, `:151-153,384-389`); cartões "Bônus", "Vales", "Faltas", "Saldo" (`:392-421`).
- Cartões por movimento com selo ("Vale", "Saldo de vale", "Bônus", "Falta", "Falta (BH)", "Pagamento", "Ajuste"), data,
  valor, "Saldo após"; pagamento com o detalhamento ("Salário base", "+ Bônus", "- Faltas", "Subtotal", "Total de vales
  acumulados", "Vales descontados", "Forma de pagamento", "Valor líquido pago") (`:223-350`; `utils/employeeCalculations.ts:140-147`).
- **"Gerar Recibo"** em pagamento e vale: escolhe "A4 (imprimível)" ou "Térmico 80mm"; pagamento CLT reabre o holerite
  (`:353-375,448-479`). Lixeira: "Excluir movimentação?" (vale: "O vale e a saída financeira vinculada serão excluídos. O valor
  voltará automaticamente para a conta de origem.") (`:254-274`; emp `:442-448`).

### 3.7 Arquivar (`pages/Employees.tsx:1594-1631`; `hooks/useEmployees.ts:100-116`)

"Arquivar funcionário?" — sem usuário: "O funcionário será removido das operações ativas, mas seu histórico de ponto e
movimentações será preservado."; com usuário: "…Deseja excluir também o usuário do sistema? Isso liberará o email para
reutilização." com "Arquivar e excluir usuário" (edge `manage-user` `delete_user`) e "Só arquivar". Toast "Funcionário
arquivado!" — "O histórico foi preservado e o funcionário foi removido das equipes e ordens de serviço ativas.". O trigger
cancela as folhas pendentes ("Funcionário desativado", `20260426010000_payroll_integration.sql:429-452`). **Não gravar.**

### 3.8 Controle de Ponto — "Hoje" (`components/time-tracking/TimeToday.tsx`; `hooks/useTimeRecords.ts:496-661`)

- Indicadores "Presentes", "Ausentes", "Em intervalo", "Concluídos" (`:59-64`); tabela "Funcionário", "Entrada", "Intervalo",
  "Saída", "Trabalhado", "Status", "Ações" (olho = "Registros do dia," e lápis = "Registro manual,") (`:150-226`).
- Lista **todos os funcionários ativos**, com ou sem ponto, inclusive PJ (`useTimeRecords.ts:507-518`). Status: "Ausente" sem
  batida, "Presente", "Em intervalo", "Concluído" (`:578-585`). Atualiza a cada 60 s e por tempo real (`:532,548-570`).
- "Registro manual, {nome}": "Tipo de registro" (Entrada, Início intervalo, Fim intervalo, Saída), "Data", "Horário",
  "Justificativa \*" ("Motivo do registro manual..."), "Cancelar"/"Registrar" (`components/time-tracking/ManualPunchModal.tsx`; emp `:68-87`).
- "Registros do dia, {nome}": batidas com endereço e miniatura da selfie, totais "Trabalhado"/"Intervalo"/"Saldo", "Editar"
  e "Excluir" (batida some da lista mas fica guardada) (`components/time-tracking/TimeDayDetailModal.tsx:112-118`; emp `:106-139`).

### 3.9 "Histórico" e "Relatório"

- Histórico: filtros (botão de filtros: "Funcionário", "Período", "Status" Completo/Incompleto/Justificado), botão **"CSV"**
  (download), colunas "Data", "Funcionário", "Entrada", "Saída", "Trabalhado", "Saldo", "Status", "Ações"; selo "{n}
  jornadas"; rodapé "Esperado"/"Trabalhado"/"Saldo"; vazio "Nenhum registro de ponto" (`TimeHistory.tsx:34-41,150-215`; emp `:141-208`;
  colunas do CSV emp `:645-662`).
- Relatório: filtros "Mês", "Ano", "Funcionário" ("Visão geral de todos os funcionários" / "Relatório de {nome}"), "Calendário"
  (dias "Sem registro"), resumo "Dias trabalhados", "Total trabalhado", "Saldo do mês", "Faltas / Atrasos", gráfico "Horas por
  dia" (`components/time-tracking/TimeReport.tsx:164-288`; emp `:210-251`). Sem exportação.

### 3.10 "Config" (`components/time-tracking/TimeSettings.tsx`)

- "Jornada Padrão da Empresa": "Entrada padrão" 08:00, "Saída padrão" 17:00, "Intervalo (min)" 60; chaves **"Exigir selfie"**,
  **"Exigir geolocalização"**, "Biometria obrigatória no quiosque" ("Desativada por padrão…"); "Raio máximo (metros)" ("0 = sem
  restrição"), "Tolerância atraso (min)" 10, "Permitir fora do horário"; "Batidas da madrugada contam para o dia anterior até"
  05:00; botão **"Salvar configurações"** (`:37-50,111-177`; emp `:270-301`). Grava `time_settings` (`useTimeRecords.ts:686-725`).
- Cartão **"Ponto em grupo (quiosque)"** — "Deixe este link aberto num tablet fixo da empresa. O time inteiro bate o ponto por
  ali, escolhendo o próprio nome na lista." — "Link do quiosque", "Copiar link", "Abrir quiosque" (nova aba), "Baixar QR Code"
  (download) (`:180-181`; `components/employees/PontoKioskLinkDialog.tsx:67-182`; emp `:1080-1097`; RPC `get_or_create_ponto_kiosk_slug`, `hooks/usePontoAdmin.ts:28-30`).
- "Jornada Individual": tabela por funcionário e dia (padrão herdado em cinza, "Folga" no fim de semana), lápis → "Jornada,
  {nome}" com um interruptor por dia e horários, "Cancelar"/"Salvar jornada" (`:183-318`).

### 3.11 Ponto pelo celular

**Ativação** (`pages/FaceEnrollment.tsx`; tc `:154-178`): "Cadastro facial", "Olá, {nome}", "Vamos fazer uma leitura guiada…",
"Começar cadastro" (câmera, 3 poses) ou **"Continuar sem biometria"** → abre o ponto (`:68-76,144-171`). Link vale 24 h
(emp `:1009`).

**Ponto** (`components/ponto/PontoScreen.tsx`; tc `:11-71`): cabeçalho com foto, nome, cargo e marca da empresa; "PONTO
ELETRÔNICO"; "Você ainda não bateu o ponto hoje"; botão **"Registrar Entrada"** (depois "Iniciar Intervalo", "Voltar do
Intervalo", "Registrar Saída", "Registrar Nova Entrada"); "Registros de hoje". Fluxo (`:780-916`): sempre tenta a localização
("Obtendo sua localização...", endereço por OpenStreetMap, `utils/reverseGeocode.ts:91`), selfie se exigida ("Centralize o
rosto no círculo", "Tirar foto agora", "Esta selfie será protegida e usada como evidência do registro de ponto."), confirmação
"Tipo", "Horário", "Local" → **"Confirmar registro"** → toast "✅ Entrada registrada" (`:896`). Negar a localização com ela
exigida: "Não foi possível obter a localização. Verifique as permissões do navegador." + "Tentar novamente".

**Quiosque** (`pages/PontoKiosk.tsx`; tc `:112-148`): grade com quem tem ponto ligado ("Não bateu hoje", "Trabalhando"…),
busca "Buscar funcionário", ordem "A-Z"/"Quem falta"; PIN se cadastrado. Sem ninguém: "Ninguém com ponto ativo ainda".

### 3.12 A folha em Contas a Pagar (`components/financial/FinanceContas.tsx`)

- Linha "Folha {nome} — {AAAA-MM}" com ícone de pessoas (`:1419-1421,1585`), valor = salário (quinzenal ×0,5, semanal ÷4,33),
  vencimento pela configuração (`20260426010000_...sql:176-270`). Gerada pelo cron `generate-payroll` às 04:00, janela de 35
  dias, só para ativos com salário > 0; nunca duas no mesmo período (`:167-171`).
- "Marcar pago" numa folha abre o **mesmo** "Pagamento, {nome}" com a faixa "Quitando folha pendente, período 2026-12"
  (`:255-262,1793-1803`); confirmar chama a RPC `pay_payroll_transaction` → **"Folha quitada com sucesso"** (erro "Erro ao pagar
  folha") e grava no extrato "Folha quitada via Contas a Pagar" (`:278-309`; fin `:437-441`; `20261019030000_...sql:162-274`).

---

## 4. Backend por tela

### 4.1 Chamadas

| Tela / ação | Tabelas | RPC / edge / storage | Linhas |
|---|---|---|---|
| Lista e ficha | `employees` (select `*`, ordem nome), `employee_movements` (todas, para o saldo), `employee_contracts` (PJ), `financial_accounts` | — | `hooks/useEmployees.ts:60-69`; `pages/Employees.tsx:401-416` |
| Novo/editar | `employees` insert/update; `profiles.avatar_url` | bucket `employee-photos` (upload); RPC `generate_ponto_slug`, `get_employee_face_template_status`, `create_employee_face_enrollment_link`; edge `create-user`; `users` (lista para vincular) | `EmployeeFormDialog.tsx:198-219`; `pages/Employees.tsx:507-679` |
| PIN | — | RPCs do PIN (`hooks/usePontoAdmin.ts`, migration `20260917153000_ponto_kiosk_e_pin.sql`) | `PontoPinField.tsx` |
| Vale | — | RPC `create_employee_vale` (grava `financial_transactions` + `employee_movements`) | `hooks/useEmployeeMovements.ts:65-84` |
| Bônus / falta | `employee_movements` insert | — | `useEmployeeMovements.ts:40-55` |
| Pagamento | `employee_movements` (pagamento, ajuste, vale_residual); `financial_transactions` select (folha pendente) + update **ou** insert | — | `pages/Employees.tsx:862-964` |
| Excluir movimento | `employee_movements` delete/update (recalcula) | RPC `delete_employee_vale` (vale) | `useEmployeeMovements.ts:100-142` |
| Arquivar | — | RPC `archive_employee`; edge `manage-user` (`delete_user`) | `useEmployees.ts:100-116`; `pages/Employees.tsx:1017-1039` |
| Hoje / manual | `employees` (ativos), `time_records`, `time_sheets` do dia; canal realtime `time_records` | RPC `register_time_punch` (manual, `p_force_date`) | `useTimeRecords.ts:507-631` |
| Histórico / Relatório / dia | `time_sheets`, `time_records` | RPC `recompute_time_sheet` (editar/excluir batida) | `useTimeRecords.ts:664-879` |
| Config | `time_settings` (select/insert/update), `time_schedules` (delete + insert) | RPC `get_or_create_ponto_kiosk_slug` | `useTimeRecords.ts:686-758`; `usePontoAdmin.ts:28-30` |
| Ponto pessoal / quiosque | — | edge `time-clock-portal` (ações `get_state`, `register_punch`, `get_kiosk`, `match_face`, `calibrate_face`; bucket privado `time-photos`); host `nominatim.openstreetmap.org` | `supabase/functions/time-clock-portal/index.ts:466-1366`; `utils/reverseGeocode.ts:91` |
| Ativação | — | edge `face-enrollment` (ações `context`, `complete`) | `supabase/functions/face-enrollment/index.ts:153-200` |
| Folha | `financial_transactions` (`payroll_kind='salary'`) | RPC `pay_payroll_transaction`; cron/edge `generate-payroll` | `FinanceContas.tsx:278-309` |

### 4.2 Gatilhos e rotinas do banco que mudam a tela (o fakebase não tem)

- Cron diário **04:00** chama `generate-payroll` → cria as folhas dos próximos 35 dias (`20260426020000_...sql:27-43`; `generate-payroll/index.ts:54`).
  A categoria "Folha de Pagamento" é criada na primeira folha (`20261019030000_...sql:86-96`).
- `trg_employee_deactivated` cancela folhas pendentes ao arquivar (`20260426010000_...sql:429-452`).
- `ensure_public_short_code` dá `public_short_code` ao funcionário (`20260726100000_employees_public_short_code.sql:36-37`).
- `register_time_punch(_service)` recalcula o espelho `time_sheets` na mesma transação (comentário `useTimeRecords.ts:618-621`).

### 4.3 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Precisa | Situação | O que fazer |
|---|---|---|
| `employees` (6 técnicos do T9 + a nova), `employee_movements` | **Sem semente** (`seeds/gen-01-tenant.json` só tem empresa, perfis e papéis) | Semente do T9 (técnicos com `monthly_cost`) + `seeds-extra/t15/` |
| `time_settings`, `time_schedules`, `time_records`, `time_sheets` | sem semente | vazias no começo; batidas criadas pelo handler |
| `financial_accounts`, `financial_categories` | já combinadas a partir do T8/T9 (`PRODUCAO.md`, Alinhamentos) | herdar do T14 |
| RPCs `generate_ponto_slug`, `get_employee_face_template_status`, `create_employee_face_enrollment_link`, `create_employee_vale`, `register_time_punch`, `recompute_time_sheet`, `get_or_create_ponto_kiosk_slug`, `pay_payroll_transaction`, `archive_employee` | **sem handler** (`handlers/rpc/` só tem portal e captação) | criar (seção 7 do plano) |
| Edges `create-user`, `time-clock-portal`, `face-enrollment`, `generate-payroll` | **sem handler** (`handlers/functions/` tem `cep-lookup`, `lead-capture-submit`, `tenant-asaas-card-fees`) | criar; `create-user` também é do T2 (estender, não reescrever) |
| Storage `employee-photos`, `time-photos` | só `storage/company-logos` | aceitar upload e servir URL assinada |
| `nominatim.openstreetmap.org` | **já existe** (`handlers/ext/nominatim.openstreetmap.org.mjs`) | endereço fictício perto da empresa |

---

## 5. Pegadinhas para roteiro e gravação

- **P1. [handoff, segurança] (alta, dentro da empresa) Login criado pelo RH tem acesso a tudo.** "Criar acesso ao sistema" chama
  `create-user` com papel `tecnico` e **sem** `permissions`/`preset_id` (`pages/Employees.tsx:589-600,638-650`); a edge só grava
  `user_permissions` quando recebe a lista (`supabase/functions/create-user/index.ts:61-79`); sem registro, `hasPermission` e
  `hasScreenAccess` liberam tudo para quem tem qualquer papel (`contexts/AuthContext.tsx:382-394`). Todo funcionário que ganha
  login por aqui enxerga Financeiro, salários dos colegas, Configurações etc. É o achado 2 do `TRILHA.md` por um caminho que
  **sempre** cai nele. O Guia afirma o contrário (seção 0.4). Na fala: depois de criar o acesso, ajustar o cargo em Usuários e
  Permissões (T2).
- **P2. [handoff, segurança] (baixa) Senha por extenso na tela.** O aviso "Acesso ao sistema criado!" mostra "Email: …, Senha: …"
  por 15 s (`pages/Employees.tsx:612-616,662-666`; emp `:673-674`) e a "Senha temporária" é campo de texto aberto
  (`EmployeeFormDialog.tsx:747-751`). Na gravação a senha (fictícia) apareceria: ver decisão no plano.
- **P3. [handoff] "Salário \*" não é obrigatório.** O asterisco está no rótulo (emp `:868`), mas o envio só confere o nome
  (`EmployeeFormDialog.tsx:293-299`); "Salário é obrigatório" (emp `:1044`) nunca aparece. Sem salário, não nasce folha
  (`20261019030000_...sql:82-84`).
- **P4. [handoff] "Descontar do banco de horas" também desconta dinheiro.** O movimento `falta_banco` grava o valor em reais
  (`pages/Employees.tsx:758-795`), e o saldo soma `falta_banco` em "Faltas" (`utils/employeeCalculations.ts:64`), que sai do
  subtotal do pagamento (`pages/Employees.tsx:803`). Não existe "banco de horas" que receba essas horas. Na aula: só "Descontar do
  salário".
- **P5. [handoff] (média, financeiro) Quitar a folha por Contas a Pagar ignora o CLT.** O modal abre sem o regime (cai em
  "Normal / Informal") e, se o usuário trocar para "CLT", a tela mostra o líquido com INSS/IRRF, mas a RPC recebe
  `salário + bônus − faltas − vales` e não há holerite (`components/financial/FinanceContas.tsx:278-295,1793-1803`). Também não
  relança vale não descontado (a RPC só grava pagamento e reset, `20261019030000_...sql:248-262`): desconto parcial **some** com
  o resto dos vales. Na aula: quitar por lá só funcionário informal e com 100% dos vales, ou só abrir o modal.
- **P6. [handoff, regra] Tabela de 2026 provisória.** `payrollTables.ts:35-38`: "2026: TABELA_2025, // placeholder até publicação
  oficial de 2026 — CONFIRMAR e substituir". O holerite de novembro de 2026 usa INSS/IRRF de 2025. A fala não lê números; o aviso
  da tela já pede o contador.
- **P7. [handoff, texto] Fórmula do "Valor a Pagar" confunde.** O subtotal já desconta os vales (`EmployeePaymentModal.tsx:256-258`),
  e a linha embaixo diz "{subtotal} - {desconto} (vales)" (`:653-657`; emp `:551`): com vale de R$ 300,00, aparece "R$ 2.790,00 -
  R$ 300,00 (vales)" sobre o total R$ 2.790,00. Sem zoom nessa linha.
- **P8. Selfie e localização já vêm exigidas.** Padrões `true` no banco, na edge e no formulário (seção 0.1). A selfie pede câmera
  (no robô: câmera simulada ou "Exigir selfie" desligado antes; decisão no plano). A batida **sempre** pede a localização, mesmo
  quando não exigida (`PontoScreen.tsx:836-845,800-835`).
- **P9. [handoff] Configurações sem efeito.** "Raio máximo (metros)", "Tolerância atraso (min)" e "Permitir fora do horário" só
  existem na tabela e na tela (`20260308163937_...sql:65-67`; `TimeSettings.tsx:146-160`); nenhuma função as lê (busca em
  `supabase/` e `src/`). Não há ponto de referência para medir raio. O status "Atrasado" existe no texto (emp `:26`) e nunca é
  calculado (`useTimeRecords.ts:578-585`). Na aula, não citar os três campos nem "Atrasado" (🚫).
- **P10. O ponto não alimenta a folha.** As horas ficam em `time_sheets`; vale, falta e pagamento ficam em `employee_movements`;
  nada liga um ao outro (nenhum uso de `time_sheets` em `pages/Employees.tsx` ou nas RPCs de folha). Falta por ponto é lançada à
  mão na ficha.
- **P11. A folha aparece no dia seguinte, já do mês seguinte.** Cron 04:00 com janela [hoje, hoje+35] (`generate-payroll/index.ts:54`;
  `20261019030000_...sql:124-128`). O período é o mês do **vencimento** ("2026-12" para o 5º dia útil de dezembro,
  `20260426010000_...sql:213`). Feriado de 20/11 não está na tabela nacional (`:43-71`), só os oito fixos e os móveis.
- **P12. [handoff] Pagar pela tela de Funcionários quita a folha pendente mais antiga**, de qualquer período, e grava o valor pago
  nela (`pages/Employees.tsx:907-938`). Sem folha pendente, cria "Pagamento de salário - {nome}" na categoria **"Funcionários"**,
  que não existe no cadastro (vale também usa "Funcionários", `20260922120000_...sql:676`); a folha do cron usa "Folha de
  Pagamento". Dois nomes para o mesmo custo no DRE (T20; a confirmar como aparece).
- **P13. Holerite, recibo, extrato e "Abrir quiosque" abrem em nova aba; CSV, QR Code e PDF baixam arquivo** (`pages/Employees.tsx:974-990,1670-1673`;
  `EmployeeExtract.tsx:60-70`; `TimeHistory.tsx:193`). O gravador ainda não grava nova aba nem download (`PRODUCAO.md`).
- **P14. Endereço do app nos links.** O toast do link de ativação e o "Link do quiosque" mostram `window.location.origin`
  (`pages/Employees.tsx:513`; `hooks/useFaceBiometrics.ts:16-18`; `PontoKioskLinkDialog.tsx:67`): na gravação, `127.0.0.1:8080`
  (TRILHA, trabalho comum 7).
- **P15. "Hoje" lista quem não usa ponto.** Todos os ativos aparecem como "Ausente", inclusive PJ/MEI (`useTimeRecords.ts:507-518`).
  Com os seis técnicos sem ponto, o quadro mostra "Ausentes 6".
- **P16. [handoff, texto] Concordância nos avisos da batida.** O toast junta "{tipo}" + "registrada": "✅ Início do intervalo
  registrada", "✅ Fim do intervalo registrada" (`PontoScreen.tsx:896`; tc `:38-43,75`). Na aula, só "Entrada".
- **P17. [handoff, texto] Duas instruções para o mesmo lugar.** O vazio do quiosque diz "Ative o ponto eletrônico dos funcionários
  no sistema, em Funcionários, Ponto, e eles aparecem aqui." (tc `:131`): a aba é "Ponto eletrônico" do cadastro.
- **P18. [handoff, segurança] (média, entre empresas, a confirmar com chamada de teste) `create-user` liga funcionário de outra
  empresa.** Com `employee_id` no corpo, a edge faz `update employees set user_id` com a chave de serviço, sem filtrar pela empresa
  de quem chama (`supabase/functions/create-user/index.ts:100-109`). Quem souber o UUID de um funcionário de outra empresa troca
  o vínculo dele.
- **P19. [handoff, segurança/LGPD] (média, dentro da empresa) Dados pessoais e salário legíveis por qualquer usuário.** A policy
  "Users manage own company employees" (FOR ALL, só empresa) continua viva ao lado da de gestores
  (`supabase/migrations/20260418163700_9165358e-c67c-420d-b74f-be9aeac54c1e.sql:115-118`; reafirmada em
  `20260826161618_rls_wrap_auth_initplan.sql:1641-1648`): um técnico lê e altera CPF, salário, chave PIX, endereço e telefone de
  todos pela API. `employee_movements` também (`20260922120000_...sql:422-469`). Amplia o achado 5 do `TRILHA.md` (T09 P28).
- **P20. [handoff, segurança/LGPD] (média, dentro da empresa) Selfies do ponto abertas aos colegas.** No bucket privado
  `time-photos`, qualquer usuário ativo da empresa lista, baixa, troca e apaga as selfies dos colegas
  (`supabase/migrations/20261016080000_storage_isolamento_por_empresa_onda1.sql:98-110,154-170`). A selfie é "a evidência
  jurídica da batida" (`time-clock-portal/index.ts:1219-1222`).
- **P21. [handoff, segurança] (baixa) Link pessoal sobrevive ao arquivamento.** O link resolve só por slug + `ponto_enabled`
  (`time-clock-portal/index.ts:774-783`), e `archive_employee` não desliga o ponto (`20260920002000_...sql:39-93`). É deliberado
  ("o arquivado ainda precisa fechar o próprio mês", `:543-546`), mas sem prazo: o ex-funcionário segue batendo ponto e vendo nome
  e foto.
- **P22. [handoff, segurança] (baixa, dentro da empresa) Quitar folha não confere papel.** `pay_payroll_transaction` aceita
  qualquer usuário da empresa (`20261019030000_...sql:194-211`).
- **P23. Rascunho do formulário.** Abrir "Novo Funcionário" com rascunho guardado mostra a pergunta de retomar antes do formulário
  (`EmployeeFormDialog.tsx:362-373`): limpar o `localStorage` no `setup` do robô.

## 6. 🚫 Não prometer

- Botão "Gerar Folha" (não existe; a folha é do cron).
- Tela separada de ponto para o gestor.
- Cerca virtual / raio de distância, tolerância de atraso, bloqueio fora do horário, status "Atrasado" (P9).
- Banco de horas que receba a falta "Descontar do banco de horas" (P4); ponto descontando falta ou hora extra na folha (P10).
- Lançamentos separados de INSS, IRRF e FGTS no Financeiro (o comentário do código confirma: `pages/Employees.tsx:817-819`).
- Holerite e recibo enviados ao funcionário (são páginas para imprimir ou salvar em PDF).
- Pagamento por Pix feito pelo sistema (a chave PIX é só registro; Guia cap. 2).
- Quiosque, PIN e biometria aparecem como recurso, mas a aula não os demonstra (decisão no plano).
- Prestador PJ/MEI tem aba própria e contrato (fora do roteiro principal; citar se sobrar tempo).

## 7. Dúvidas em aberto (só rodando)

1. A miniatura e o link da foto do funcionário com o bucket privado `employee-photos`: a gravação usa URL assinada? (`EmployeeFormDialog.tsx:212`
   grava `getPublicUrl`; `SignedAvatarImage` no ponto.)
2. O texto exato do aviso de PIN e de biometria logo depois de ligar o ponto num funcionário novo (componentes recebem `employeeId` nulo).
3. Ordem das linhas em "A Pagar" com seis folhas no mesmo vencimento e a busca por "Folha".
4. Como "Funcionários" (categoria inexistente) aparece no DRE e na Visão Geral do Financeiro (P12).
5. A câmera simulada do Chromium passa pelo enquadramento "Centralize o rosto no círculo" ou só pelo "Tirar foto agora"?
6. O selo "Controle de Ponto" e "Link do ponto" na ficha logo após salvar (o `ponto_slug` chega pelo `invalidateQueries`).

## 8. Termos e pronúncias

PIX ("pix"), CPF ("cê-pê-éfe"), CLT ("cê-éle-tê"), PJ/MEI ("pê-jota ou mêi"), CBO ("cê-bê-ó"), IRRF ("i-érre-érre-éfe"), INSS
("i-ene-ésse-ésse"), FGTS ("éfe-gê-tê-ésse"), DSR ("dê-ésse-érre"), VT ("vale-transporte"), PIN ("pim"), QR Code (perfil).
