# Plano · T26 · CRM/Kanban

- **Título:** CRM/Kanban (o da fonte). 🔒 módulo `crm_kanban`. **Aula nova.**
- **Objetivo (uma frase):** montar o funil de captação de sucata industrial da Recicla Vale Metais, com etapa própria, regras de
  saída e uma automação ativa, e levar uma oportunidade pelo funil até a tarefa aparecer na Agenda.
- **Antes:** T4 · Clientes, fornecedores e a ficha do parceiro. **Próximo:** fim da trilha (cartão "Fim da trilha").
- **Áreas das vinhetas:** CRM · CRM · FUNIS · ESTÁGIOS · REGRAS · AUTOMAÇÕES · MODELOS · OPORTUNIDADES · KANBAN · OPORTUNIDADES ·
  TAREFAS · FILTROS · RESUMO.
- **Duração:** alvo da fonte ~16 min; fala de 1.817 palavras (~11,6 min de voz) → ~15 min de vídeo com as vinhetas e as ações.
- **Base:** `T26/inventario.md` (código 1.59.154 e as migrations do commit de release). Desktop 1280×800, tema claro, Rafael
  Nogueira (MASTER).
- **Automações na versão gravada:** sim (1.59.151 em diante; migration `20261106170000` no commit `f37573ea0`).
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (caps 0 a 11); `2026-11-10T17:30:00-03:00` no cap12.

## Capítulos (os 12 da fonte, na ordem; cap00 abertura e cap13 recapitulando)

| # | Vinheta (área / título) | O que a tela mostra | Estado de partida | Duração |
|---|---|---|---|---|
| 0 | (sem vinheta) | [ILUSTRAÇÃO: conversas que esfriam → cartões]; zoom no menu "CRM/Kanban"; cartões "Módulo CRM/Kanban" e "Antes: …" | `inicio` | 0:45 |
| 1 | CRM / O funil de vendas | Primeira abertura: nasce o "Funil de vendas" (Novo, Em contato, Proposta, Ganho, Perdido); [ILUSTRAÇÃO: o funil de vendas deitando em colunas]; "Nova oportunidade" | `inicio` (sem funil) | 0:50 |
| 2 | CRM / Funil, Tarefas e os cartões | Abas "Funil" e "Tarefas"; os quatro cartões zerados; [ILUSTRAÇÃO: o que cada cartão soma]; busca, "Filtros", barra dos funis; dica da permissão | `apos-cap01` | 1:00 |
| 3 | FUNIS / Funis e estágios | "Configurações do CRM/Kanban" › "Funis": "Novo funil" "Sucata industrial", "Tornar padrão", arrastar a linha; "Novo estágio" "Visita técnica" e arrastar para depois de "Em contato"; [ILUSTRAÇÃO: quem é negociação] | `apos-cap01` | 1:25 |
| 4 | ESTÁGIOS / Nome, cor e orientação | "Configurar Visita técnica" › "Coluna": cor, "Orientação para o time", "Salvar etapa"; lixeira (dica de excluir) | `apos-cap03` | 0:55 |
| 5 | REGRAS / Regras do estágio | "Configurar Em contato" › "Regras": [ILUSTRAÇÃO: a porta de saída]; liga "Tarefas" e "Responsável"; "por nome" (dica); "Salvar etapa" | `apos-cap04` | 1:05 |
| 6 | AUTOMAÇÕES / Automações | "Automações" › "Nova automação" "Agendar a visita": gatilho, as sete ações, "Criar tarefa" "Agendar visita na {CLIENTE}", 1 dia útil, "Pausada" → "Ativa", "Salvar automação"; [ILUSTRAÇÃO: gatilho e ações; só avançando] | `apos-cap05` | 1:40 |
| 7 | MODELOS / Checklists e etiquetas | "Nova checklist" "Documentos do fornecedor" (3 itens); [ILUSTRAÇÃO: modelo e cópia]; "Nova etiqueta" "Indústria"; dica dos modelos vivos | `apos-cap06` | 1:05 |
| 8 | OPORTUNIDADES / Nova oportunidade | Quadro do "Sucata industrial"; "Nova oportunidade" da Metalúrgica Jequitibá (todos os campos da fonte); cartão em "Novo" | `apos-cap07` | 1:25 |
| 9 | KANBAN / Arrastar o cartão | Novo → Em contato (a automação cria a tarefa); Em contato → Visita técnica: "Conclua as tarefas pendentes. Defina um responsável."; [ILUSTRAÇÃO: a regra é da porta de saída] | `apos-cap08` | 0:55 |
| 10 | OPORTUNIDADES / A ficha da oportunidade | Ficha: "Detalhes" (responsável Rafael, etiqueta "Indústria"), "Tarefas" (concluir), "Histórico"; o cartão passa para "Visita técnica" | `apos-cap09` | 1:10 |
| 11 | TAREFAS / Tarefas e Agenda | Aba "Tarefas": Kanban, "Nova tarefa" "Enviar proposta" (12/11), "Lista", "Calendário"; "Agenda" com o selo "CRM"; [ILUSTRAÇÃO: uma tarefa, dois lugares]; clique volta ao CRM | `apos-cap10` | 1:15 |
| 12 | FILTROS / Filtros e busca | Seis cartões e os totais; busca "alumínio"; "Filtros": "Em negociação" + Rafael → R$ 26.200,00; "Limpar filtros" | `apos-cap11-dia` | 1:05 |
| 13 | RESUMO / Recapitulando | Montagem; cartão "Fim da trilha" | (reaproveita) | 0:50 |

Transições faladas: 0→1 "Vamos abrir o CRM"; 1→2 "Lá em cima ficam as duas abas"; 2→3 "Agora, as configurações"; 3→4 "Pra editar
um estágio, é o lápis"; 4→5 "Agora, as regras"; 5→6 "E as automações"; 6→7 "Agora, os modelos"; 7→8 "Com o funil pronto"; 8→9
"Agora, andar com o cartão"; 9→10 "Pra destravar… na ficha do cartão" / "Clicando no cartão"; 10→11 "Agora, a aba Tarefas"; 11→12
"Com o funil em uso".

**Cuidados da fonte na fala**

| Marca | Onde | Fala (resumo) | Na tela |
|---|---|---|---|
| ⚠️ Trava pela etapa de origem, em qualquer troca; a lista de pendências | cap09 | o bloqueio de verdade + "Uma dica: quem manda é a regra da etapa de onde o cartão sai… avançar, voltar uma coluna ou mandar pro Perdido." | toast "Conclua as tarefas pendentes. Defina um responsável."; ilustração |
| ⚠️ Automação nova nasce pausada | cap06 | "Uma dica: toda automação nova nasce pausada. Se ficar assim, ela não roda. Então eu ligo pra Ativa." | chave "Pausada" → "Ativa" |
| ⚠️ "Ao entrar nesta etapa" só avançando | cap06 | "Uma dica: … só roda quando o cartão avança pra ela, muda de funil ou já nasce nela. Voltando…, ela não roda." | ilustração |
| ⚠️ Ação que falha desfaz tudo | cap07 | "Uma dica: o modelo, a etiqueta e a pessoa que uma automação usa precisam continuar existindo…" | (fala) |
| ⚠️ Estágio criado na tela não é Ganho nem Perdido | cap03 (e cap02) | "Uma dica: estágio criado em Novo estágio é sempre de negociação. Só o Ganho e o Perdido que nascem com o funil contam…" | selos "Ganho"/"Perdido"; ilustração |
| ⚠️ "Por nome" cobra texto idêntico | cap05 | "Uma dica: o nome tem que ser igualzinho, letra por letra…" | zoom nos dois campos |
| ⚠️ Excluir estágio com cartões | cap04 | "Uma dica: pra excluir um estágio, ele precisa estar vazio…" | zoom na lixeira (sem clicar) |
| ⚠️ Sem permissão de ação separada | cap02 | "Uma dica: quem tem acesso à tela do CRM pode criar, editar, excluir e configurar tudo…" | (fala) |
| 🚫 Sem importação, integração, automação por tempo, motivo de perda, conversão em pedido | cap01, cap06, cap08, cap10 | no positivo: entra por "Nova oportunidade"; os gatilhos são os quatro da tela; a compra se lança no caixa; o motivo vai nas observações | (fala) |
| 🚫 "Criar tarefa" sem responsável | cap06 | "A tarefa da automação fica com o responsável do cartão. Pra escolher quem é, existe a ação Atribuir responsável." | a ação aberta |
| 🚫 `/crm-tarefas` é do admin | (não aparece) | a aula usa só a aba Tarefas de `/crm` | |
| 🔒 CRM/Kanban | cap00 | "O CRM/Kanban depende do plano contratado." | cartão "Módulo CRM/Kanban" |

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)

**No `inicio`:** módulo `crm_kanban` ativo; **nenhuma linha** de CRM da empresa (`crm_pipelines`, `crm_stages`,
`crm_opportunities`, `crm_automation_rules`, `crm_checklist_templates`, `crm_labels`, `crm_opportunity_activities`); usuários
ativos Rafael Nogueira, Juliana Prado e Marcos Antunes (T2); materiais da T3 (Chaparia, Bateria automotiva, Alumínio perfil, Cobre
misto, Ferro pesado, Papelão).

**Criado na tela:**

| Item | Valores (fictícios) |
|---|---|
| Funil padrão (cap01, pela RPC) | "Funil de vendas", #22c55e: "Novo" #3b82f6, "Em contato" #f59e0b, "Proposta" #8b5cf6, "Ganho" #22c55e (`is_won`), "Perdido" #ef4444 (`is_lost`) |
| Funil novo (cap03) | "Sucata industrial", #0ea5e9, **padrão** e **primeiro** na ordem; etapas "Novo", "Em contato", **"Visita técnica"** (posição 2, criada em "Novo estágio"), "Proposta", "Ganho", "Perdido" |
| Visita técnica (cap04) | cor #0d9488; "Orientação para o time": "Visitar a indústria, ver o volume e o tipo de sucata e combinar a retirada." |
| Regras do "Em contato" (cap05) | `requirements` = `{tasks: true, assignee: true, taskNames: [], checklistNames: []}` |
| Automação (cap06) | "Agendar a visita", "Em contato", "Ao entrar nesta etapa", ação "Criar tarefa" "Agendar visita na {CLIENTE}", `dueDays` 1, "Dias úteis", **ativa** |
| Modelos (cap07) | checklist "Documentos do fornecedor": "CNPJ conferido", "Local de retirada combinado", "Frequência da coleta combinada"; etiqueta "Indústria" #6366f1 |
| Oportunidade (cap08) | "Retalho de chapa da Metalúrgica Jequitibá"; "Novo"; valor **R$ 8.400,00**; sem responsável; empresa avulsa "Metalúrgica Jequitibá"; contato "Paulo Lacerda", "Suprimentos", paulo.lacerda@metalurgicajequitiba.example (sem telefone); "Chaparia" **12.000 Kg**; "Frota própria"; previsão 30/11/2026; observações "Quer retirada a cada quinze dias, com caçamba." |
| Tarefa da automação (cap09) | "Agendar visita na Metalúrgica Jequitibá", 11/11/2026 (1 dia útil), pendente, sem responsável; **concluída** no cap10 |
| Ficha (cap10) | responsável **Rafael Nogueira**; etiqueta "Indústria"; o cartão vai para "Visita técnica" |
| Tarefa nova (cap11) | "Enviar proposta", oportunidade da Jequitibá, Rafael, **12/11/2026**, prioridade "Alta", categoria "crm" |

**Semente do cap12** (`apos-cap11-dia`, FAKE_NOW 17:30): o `apos-cap11` mais cinco oportunidades no "Sucata industrial", criadas
durante o dia (10:00 a 17:00) por Rafael e Juliana:

| Título | Etapa | Valor | Responsável | Material · quantidade | Transporte |
|---|---|---|---|---|---|
| Baterias da frota da Transportadora Caminho Firme | Proposta | R$ 4.650,00 | Juliana Prado | Bateria automotiva · 1.500 Kg | Por conta do fornecedor |
| Perfis de alumínio da Esquadrias Horizonte | Em contato | R$ 17.800,00 | Rafael Nogueira | Alumínio perfil · 2.000 Kg | Transportadora |
| Cobre de manutenção da Elétrica Ponto Certo | Novo | R$ 10.800,00 | (sem) | Cobre misto · 300 Kg | A definir |
| Ferro de demolição da Construtora Pilar | Ganho | R$ 19.000,00 | Rafael Nogueira | Ferro pesado · 20.000 Kg | Frota própria |
| Papelão do Mercado Bom Preço | Perdido | R$ 1.650,00 | Juliana Prado | Papelão · 3.000 Kg | Por conta do fornecedor |

Totais (com a Jequitibá): 6 oportunidades, **R$ 62.300,00**; "Ganhos" **R$ 19.000,00**; "Em negociação" **R$ 41.650,00**; filtro
"Em negociação" + Rafael → Jequitibá e Esquadrias, **R$ 26.200,00**; busca "alumínio" → só a Esquadrias. Empresas avulsas (sem
cadastro), sem telefone.

**Sementes** (`seeds-extra/t26/`): `inicio` (caps 0 e 1), `apos-cap01` (caps 2 e 3), `apos-cap03` (cap04), `apos-cap04` (cap05),
`apos-cap05` (cap06), `apos-cap06` (cap07), `apos-cap07` (cap08), `apos-cap08` (cap09), `apos-cap09` (cartão em "Em contato" com a
tarefa aberta; cap10), `apos-cap10` (cap11), `apos-cap11-dia` (cap12). Nenhuma outra aula depende do CRM.

## Gravação

- **Rotas:** `/dashboard`, `/crm` (abas "Funil" e "Tarefas"; janela "Configurações do CRM/Kanban"), `/agenda` (cap11), deep link
  `/crm?opportunity=<id>`.
- **Backend falso, com a lógica que no app real é do banco** (marcas `[BACKEND]` do roteiro): RPC `ensure_company_crm_default_pipeline`
  (só quando não há funil), `reorder_company_crm_opportunities`; inserts e updates diretos em `crm_pipelines`, `crm_stages`,
  `crm_opportunities`, `crm_automation_rules`, `crm_checklist_templates`, `crm_labels`, `schedule_tasks`; e o que os gatilhos fazem:
  1. **Trava** em toda troca de `stage_id`: regras da etapa de origem; erro com código P0001 e as pendências juntas numa frase
     ("Conclua as tarefas pendentes. Defina um responsável.").
  2. **Automação "Ao entrar nesta etapa"** só ao nascer na etapa, mudar de funil ou ir para posição maior; "Criar tarefa" com o
     responsável do cartão, `{CLIENTE}` = empresa do cartão, prazo em dias úteis a partir de hoje.
  3. **Histórico:** 'Etapa alterada de "<de>" para "<para>".' a cada troca (e a linha do sistema da automação).
  4. Contagem de tarefas abertas por cartão (o selo) e a lista da Agenda (`schedule_tasks` com `crm_opportunity_id`).
- **[TESTAR]:** arrasto do quadro pela alça "Mover oportunidade" (`@dnd-kit`, 6 px); arrasto nativo das linhas na janela de
  configurações; os campos de cor; o selo de tarefa aberta logo depois do arrasto; **depois da trava**, o cartão fica desenhado no
  destino até a tela buscar de novo: o robô recarrega fora do vídeo e a tomada seguinte já mostra o cartão em "Em contato"; a visão
  da Agenda com o dia 12 sem rolar.
- **Não clicar:** "Excluir funil", "Excluir estágio", lixeira do cartão, "Aplicar modelo" (só mostrado), o botão de conversa do
  contato (a oportunidade fica sem telefone para ele não aparecer).
- **Ilustrações** (cenas HTML no estilo da marca; balões e celulares genéricos, sem logo de aplicativo; nenhuma imita tela do app):
  cap00 conversas que esfriam viram cartões; **cap01 o funil de vendas** (largo em cima, estreito embaixo, e deitado em colunas);
  cap02 o que cada cartão soma; cap03 quem é negociação (Ganho e Perdido); cap05 a regra é a porta de saída; cap06 gatilho e ações
  (dominó) e "ao entrar, só avançando"; cap07 modelo e cópia (carimbo); cap09 a regra vale para qualquer troca; cap11 uma tarefa,
  dois lugares.
- Celular, cena de Windows, outro usuário: não há. `/admin/crm-tarefas` nunca aparece.

## Riscos e decisões para o Kaik

1. **O funil da aula é "Sucata industrial"** (captar indústrias que geram sucata): é o uso de CRM que mais faz sentido num
   ferro-velho; o "Funil de vendas" padrão fica como segundo funil. O valor do cartão é a compra estimada por mês.
2. **Regras e automação pensadas para a trava mostrar as duas pendências** da fonte: a automação só cria a tarefa (sem "Atribuir
   responsável"), e a ficha resolve as duas no cap10.
3. **Achados do código** (handoff para o time): o cartão bloqueado fica desenhado no destino até a próxima busca; a execução de
   automação vira uma linha sem texto no Histórico; o selo de tarefa aberta não se atualiza depois do arraste que cria a tarefa
   (a tomada recarrega fora do vídeo); "Orientação para o time" só aparece na janela da etapa.
4. **Código × fonte:** funil criado em "Novo funil" também nasce com "Ganho" e "Perdido" com status (a fonte diz que só o padrão);
   a fala vale para os dois casos.
5. **Pendência 9 da fonte** (migration das automações aplicada em produção): não afeta a gravação no backend falso; se um dia gravar
   na conta de teste, conferir antes.
6. **Nomes novos** (Metalúrgica Jequitibá, Paulo Lacerda, Transportadora Caminho Firme, Esquadrias Horizonte, Elétrica Ponto Certo,
   Construtora Pilar, Mercado Bom Preço): conferir na semente que nenhum é de empresa real da região.
7. **Fim da trilha:** sem cartão "Próximo"; fecha com "Fim da trilha" e "Até lá!".
