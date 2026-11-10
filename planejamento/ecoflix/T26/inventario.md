# Inventário · T26 · CRM/Kanban

Código 1.59.154 (`/home/claude/ecoflix/app-src-1.59.154/`), leitura estática. Caminhos relativos a `src/`. As regras do banco
(trava de etapa, automações, histórico) vêm das migrations do commit de release `f37573ea0` no repositório do EcoSistema
(`git show f37573ea0:supabase/migrations/...`, só leitura), que a cópia `app-src` não traz.

**Automações na 1.59.154: sim.** Nota de versão 1.59.151 "CRM com regras e automações por etapa" (`config/version.ts:33`);
migration `20261106170000_crm_regras_automacoes.sql` no commit de release, coberta por `lib/crmAutomationMigration.test.ts`;
telas em `components/crm/settings/CrmStageConfigurationDialog.tsx`. (Se está aplicada no Supabase de produção, o código não diz:
pendência 9 da fonte. Na gravação com o backend falso, não importa.)

## 1. Tela `/crm` (`pages/Crm.tsx`; rota `App.tsx:467-471`, permissão `screen_crm_kanban`, módulo `crm_kanban`)
- Menu lateral **"CRM/Kanban"** (`config/routes.ts:478`). Título **"CRM/Kanban"** · "Gerencie oportunidades e acompanhe seu
  processo comercial."; botão **"Configurações do CRM/Kanban"** (`:535-546`). Sem permissões de ação: quem entra na tela cria,
  edita, exclui e configura (`:185-187`).
- Primeira abertura sem funil: RPC **`ensure_company_crm_default_pipeline`** (`hooks/useTenantCrm.ts:48-61`) cria **"Funil de
  vendas"** (padrão) com **"Novo"**, **"Em contato"**, **"Proposta"**, **"Ganho"** (status ganho) e **"Perdido"** (status perdido)
  (migration `20260929180000`, `:155-200`).
- Abas **"Funil"** e **"Tarefas"** (`:548-567`). Cartões do topo, sobre a lista **já filtrada** (`:314-323`, `:573-598`):
  **"Total de oportunidades"**, **"Valor total"**, **"Ganhos"** (soma das etapas com status ganho), **"Em negociação"** (nem ganho
  nem perdido); com filtro, "(filtrado)" no rótulo.
- Busca "Buscar por título, contato, empresa, material, telefone ou e-mail...", **"Filtros"** (com o número de filtros ativos),
  **"Nova oportunidade"** (`:600-612`). Barra dos funis (um botão por funil, na ordem), engrenagem "Configurar estágios", "+"
  "Criar funil" (`:614-632`).
- Coluna (`:119-179`): cabeçalho na cor da etapa com nome, quantidade e soma dos valores, "+" "Adicionar em <etapa>"; vazia:
  botão tracejado "Nova oportunidade".
- Arrastar: `@dnd-kit`, só pela alça **"Mover oportunidade"** do cartão (`components/crm/OpportunityCard.tsx:96`); ao soltar,
  update de `stage_id` + RPC `reorder_company_crm_opportunities` (`useTenantCrm.ts:352-398`); erro vira toast com a mensagem do
  banco (`Crm.tsx:481-483`). **Achado:** no erro, o quadro não volta o cartão (o estado local do arraste fica; só a próxima busca
  ressincroniza).
- **"Filtrar oportunidades"** · "Refine os cards exibidos neste funil." (`:676-759`): "Status" ("Todos", "Em negociação", "Ganhos",
  "Perdidos"), "Valor mínimo", "Valor máximo", "Responsável" ("Todos" + usuários ativos), "Material" (só os usados no funil), "Meio
  de transporte"; "Limpar filtros", **"Aplicar"**.
- Deep link `/crm?opportunity=<id>` (vindo da Agenda) abre o formulário "Editar oportunidade" (`:238-263`).

## 2. Cartão (`components/crm/OpportunityCard.tsx`)
Etiquetas no topo, alça "Mover oportunidade", título, contato, empresa, material · quantidade, lixeira "Excluir oportunidade",
valor, "Probabilidade" com barra, progresso de checklist, origem, tarefas abertas ("<n> tarefa(s) aberta(s)"), inicial do
responsável, previsão de fechamento. Clique no título abre a ficha. **Achado:** o selo de tarefas abertas só se atualiza com
mudança de tarefa ou 30 s depois (`hooks/useCrmTasks.ts:183-202`): a tarefa criada pela automação no arraste não aparece na hora.

## 3. Configurações (`components/crm/settings/`)
- **"Configurações do CRM/Kanban"** · "Gerencie funis, checklists e etiquetas usados no seu processo comercial."; menu **"Funis"**,
  **"Checklists"**, **"Etiquetas"**; rodapé "Fechar" (`CrmSettingsDialog.tsx`).
- **Funis** (`CrmPipelinesSection.tsx`): "Organize os funis comerciais e as etapas de cada Kanban.", **"Novo funil"** (`:186-192`);
  linha do funil: nome, selo **"Padrão"**, "<n> etapas · <n> oportunidades", **"Tornar padrão"** (toast "Funil padrão
  atualizado"), lápis "Editar funil", lixeira "Excluir funil"; arrastar a linha reordena (HTML5; setas no celular) (`:200-330`).
  Aberto: **"Estágios deste funil"**, **"Novo estágio"**, linha da etapa com bolinha de cor, nome, selos **"Ganho"**/**"Perdido"**,
  lápis "Editar estágio <nome>", lixeira "Excluir estágio <nome>"; arrastar reordena (`:331-440`). Excluir estágio com cartão:
  toast **"Mova ou exclua as oportunidades deste estágio antes de removê-lo"** (`:170-183`).
- Janela **"Novo funil"** · "Defina o nome e a cor usada na navegação do CRM.": "Nome *", "Cor *", "Cancelar", "Salvar"; toast
  **"Funil criado"** (`:500-573`). O funil novo nasce com as mesmas cinco etapas, **"Ganho" e "Perdido" com status**
  (`useTenantCrm.ts:100-138`). **Estágio criado em "Novo estágio" nunca tem status** de ganho ou perdido, e não há tela para marcar.
- Janela da etapa (`CrmStageConfigurationDialog.tsx`): **"Novo estágio"** · "Crie a coluna primeiro; regras e automações ficam
  disponíveis na edição." / **"Configurar <etapa>"** · "Defina a coluna, os critérios de saída e o que acontece automaticamente.";
  abas **"Coluna"**, **"Regras"**, **"Automações"** (as duas últimas só na edição); rodapé "Fechar", **"Salvar etapa"**; toasts
  **"Estágio criado. Edite novamente para configurar regras e automações."**, **"Configuração da etapa salva"** (`:190-243`).
  - Coluna: "Nome *", "Cor *", **"Orientação para o time"** ("O que precisa acontecer enquanto o cartão estiver aqui?") (`:244-250`).
    O texto só aparece nesta janela (nem no quadro nem no cartão).
  - Regras: **"Antes de sair desta etapa"** · "O banco bloqueia avanço por arraste, edição ou integração enquanto houver
    pendências."; chaves **"Tarefas"** ("Todas as tarefas do cartão precisam estar encerradas."), **"Checklists"** ("Todos os itens
    aplicados precisam estar marcados."), **"Responsável"** ("O cartão precisa ter uma pessoa responsável."), **"Prazo"** ("Exige
    previsão de fechamento no cartão."), **"Empresa"** ("Exige uma contraparte vinculada ao cartão."), **"Observações"** ("Exige
    observações preenchidas no cartão."); **"Tarefas obrigatórias por nome"** e **"Checklists obrigatórios por nome"** (uma por
    linha) (`:42-49`, `:252-266`).
  - Automações: **"Fluxos desta etapa"** · **"Novas automações nascem pausadas para revisão."**, **"Nova automação"**; vazio "Nenhuma
    automação nesta etapa"; editor "Nova automação" · "Use {NOME} e {CLIENTE} nos textos dinâmicos.", "Voltar para lista", **"Nome
    *"**, **"Gatilho"** ("Ao entrar nesta etapa", "Ao concluir uma tarefa", "Ao concluir um checklist", "Quando tudo estiver
    concluído"; nas duas do meio, "Nome exato da tarefa *"/"Nome exato do checklist *"); ações ("Criar tarefa", "Aplicar checklist",
    "Definir prazo do cartão", "Atribuir responsável", "Adicionar etiqueta", "Mover cartão", "Copiar cartão"); "Criar tarefa":
    **"Título da tarefa *"** (padrão "Acompanhar {NOME}"), **"Prazo em dias"**, **"Contagem"** ("Dias corridos"/"Dias úteis"), **sem
    responsável**; "Adicionar ação"; chave **"Pausada"/"Ativa"** (nasce Pausada); **"Salvar automação"** → **"Automação salva e
    ativa"** / "Automação salva como pausada"; na lista: nome, selo "Ativa"/"Pausada", "<gatilho> · <n> ação" (`lib/crmAutomation.ts`;
    dialog `:268-292`). Tabela `crm_automation_rules` (`hooks/useCrmStageAutomations.ts`).
- **Checklists** (`CrmChecklistsSection.tsx`): "Modelos reutilizáveis de checklist pra aplicar em oportunidades.", **"Nova
  checklist"**, aviso "O modelo é só o ponto de partida: aplicar numa oportunidade cria uma cópia dos itens, e editar o modelo depois
  não altera quem já aplicou."; janela "Nova checklist": "Nome *", "Itens", **"Adicionar item"**, "Salvar"; toast **"Checklist
  criada"**. Tabela `crm_checklist_templates`.
- **Etiquetas** (`CrmLabelsSection.tsx`): "Etiquetas ajudam a classificar oportunidades no Kanban.", **"Nova etiqueta"**; janela:
  "Nome *", "Cor *", "Salvar"; toast **"Etiqueta criada"**. Tabela `crm_labels`.

## 4. Nova oportunidade (`components/crm/opportunity/OpportunityFormDialog.tsx`)
**"Nova oportunidade"** · "Os dados ficam disponíveis apenas para a sua empresa."; blocos "Oportunidade" (**"Título *"**, **"Etapa
*"**, "Valor", "Responsável" com "Sem responsável"), "Empresa e contato" ("Empresa": "Selecionar empresa", busca "Buscar cliente ou
fornecedor..." e 'Usar "<texto>" como empresa avulsa'; "Contato", "Área/Setor", "Telefone", "E-mail"), "Operação" ("Tipo de
material": "Selecionar material"/"Buscar material..."; "Quantidade estimada" + unidade "Kg"; "Meio de transporte": "Frota própria",
"Transportadora", "Por conta do cliente", "Por conta do fornecedor", "A definir"), "Prazos e observações" ("Data inicial",
"Previsão de fechamento", "Observações"); "Cancelar", **"Salvar"** (só com título e etapa); toast **"Oportunidade criada"**
(`Crm.tsx:394-406`). Insert em `crm_opportunities`.

## 5. Ficha (`components/crm/detail/`)
- `OpportunityDetailModal.tsx`: título, "Editar", lixeira, "Fechar"; abas **"Detalhes"**, **"Tarefas (<n>)"**, **"Histórico
  (<n>)"**; coluna da direita com comentários ("Escreva um comentário…", "Comentar") e o que mudou (`:96-180`).
- **Detalhes** (`OpportunityDetailsTab.tsx`): "Funil", "Estágio", **"Responsável"** (troca na hora; trocar o estágio aqui também
  passa pela trava), cartões "Valor Estimado", "Probabilidade", "Previsão Fechamento", "Origem"; "Contato do Cliente"/"Contato do
  Fornecedor" (com telefone, um botão de conversa externa: a aula não preenche telefone); "Negociação" ("Material", "Quantidade
  estimada", "Transporte", "Empresa", "Cargo do contato", "Data de início"); "Observações" (salva sozinha: "Salvo"); **"Checklists"**
  ("Aplicar modelo"); **"Etiquetas"** ("Gerenciar") (`:237-431`).
- **Tarefas** (`components/crm/tasks/OpportunityTasksSection.tsx`): lista das tarefas do cartão, caixa "Concluir tarefa"/"Reabrir
  tarefa", "Nova tarefa".
- **Histórico** (`OpportunityHistoryTab.tsx`): atividades do sistema; troca de etapa grava **'Etapa alterada de "<de>" para
  "<para>".'** (migration `20261005234137`, `:370-404`). **Achado:** a execução de automação grava uma linha do sistema sem texto
  (aparece só o autor e a hora).

## 6. Aba Tarefas (`components/crm/CrmTasksTab.tsx` e `tasks/`)
"Tarefas" · "Tarefas vinculadas às oportunidades do funil", **"Nova tarefa"**, "Filtrar", "Buscar por título...", visões
**"Kanban"**, **"Lista"**, **"Calendário"** (a escolha fica no navegador). Kanban: "Pendente", "Em andamento", "Concluída",
"Cancelada". Lista: "Título", "Oportunidade", "Responsável", "Data", "Prioridade", "Status". Calendário: "Mês", "Semana", "Dia".
Janela "Nova tarefa": "Título *", **"Oportunidade *"**, "Descrição", "Responsável", "Data *", "Hora", "Prioridade" ("Baixa",
"Média", "Alta", "Urgente"), "Lembrar no dia", "Salvar"; toast **"Tarefa criada"** (`hooks/useCrmTasks.ts:116-132`). Tabela
`schedule_tasks` (a mesma da Agenda) com `crm_opportunity_id` e categoria "crm".
- **Agenda** (`/agenda`, `components/agenda/TaskCard.tsx:32-41`, `:95-110`): a tarefa do CRM aparece com o selo **"CRM"**; clique
  leva a `/crm?opportunity=<id>`; na Agenda ela pode ser concluída, e editar ou excluir fica na aba Tarefas do CRM.

## 7. Regras do banco (migration `20261106170000`, commit `f37573ea0`)
- **Trava**: toda troca de `stage_id` (avançar, voltar, ir para "Perdido") checa as regras da **etapa de origem**
  (`crm_guard_stage_advance`, `:783-794`); as pendências saem juntas numa frase: "Conclua as tarefas pendentes.", "Conclua todos
  os itens dos checklists.", **"Defina um responsável."**, "Defina uma previsão de fechamento.", "Vincule ou informe a empresa do
  cartão.", "Preencha as observações do cartão.", "Conclua a tarefa: <nome>." (título idêntico), "Conclua o checklist: <nome>."
  (`:240-397`). Tarefa "encerrada" = concluída ou cancelada.
- **"Ao entrar nesta etapa"** dispara quando o cartão nasce na etapa, muda de funil ou vai para uma etapa **de posição maior**;
  voltar não dispara (`crm_trigger_stage_automations`, `:797-823`). Ações em ordem; "Criar tarefa" usa o **responsável do cartão**
  (e "Atribuir responsável" antes dela já vale); o prazo conta a partir de hoje, em dias corridos ou úteis (`:177-204`, `:405-470`).
- **Erro numa ação** (responsável, etiqueta ou modelo inexistente) marca a execução como falha e **desfaz a operação inteira**
  (mover ou criar o cartão) (`:770-777`). Execução única por evento (sem repetir).

## 8. Código × fonte (para o relatório)
1. Fonte: "só os dois do funil padrão têm esse status". Código: **todo funil criado em "Novo funil" também nasce com "Ganho" e
   "Perdido" com status**; o que nunca tem status é a etapa criada em "Novo estágio". A fala diz o que vale nos dois casos.
2. "Orientação para o time" não aparece no quadro nem no cartão: só na janela da etapa.
3. Trava no arraste: o cartão fica desenhado no destino até a próxima busca (sem ressincronizar no erro).
4. Histórico: execução de automação vira linha sem texto.
5. O selo de tarefas abertas não se atualiza depois do arraste que dispara a automação (só com mudança de tarefa ou 30 s).
6. Aba Tarefas do admin (`/admin/crm-tarefas`): fora da aula, como a fonte manda.
