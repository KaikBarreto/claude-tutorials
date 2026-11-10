# Inventário · T12 Coletas e Logística (EcoSistema 1.59.154)

Levantado em 10/11/2026 contra `/home/claude/ecoflix/app-src-1.59.154/` (análise estática, só leitura). Caminhos relativos
a `src/` (edge functions em `supabase/functions/`). Rótulo entre aspas = texto exato da tela. Só o que a aula usa.
🔒 módulo `coletas`; o pedido pelo portal depende também do módulo `portal_cliente`.

## 0. Rotas, menu e permissão
- `/coletas/:section` → `pages/Coletas.tsx` (`App.tsx:404-410`), permissão `screen_coletas` em todas as seções. Seções
  (`pages/Coletas.tsx:45-84`): título e descrição de cada uma:
  - "Ordens de Coleta", "Solicite, agende e acompanhe as ordens de coleta" (`ordens`)
  - "Frota", "Veículos e motoristas disponíveis para as coletas" (`frota`)
  - "Equipamentos", "Caçambas, bags, caixas e paletes em campo" (`equipamentos`; `/coletas/cacambas` redireciona para cá, `:38-43`)
  - "Rastreamento" e "Rotas": **fora da aula**. Na 1.59.154 "Rotas" abre "Roteirização" + "Em breve — esta função chega
    numa próxima atualização" (`:122-128`, `components/coletas/ComingSoonTab.tsx:19-21`), mas "Rastreamento" já abre
    um mapa com as posições dos motoristas (`components/coletas/CollectionTrackingTab.tsx`): a fonte está desatualizada.
  - "Relatório", "Indicadores e histórico das coletas" (`relatorio`)
  - "Configurações", "Ajuste a numeração, as janelas e as regras do portal de coletas" (`configuracoes`)
- Caminho no topo: "Coletas & Logística" › <seção> (`:104-106`).
- Menu lateral "Coletas & Logística" → "Ordens de Coleta", "Frota", "Equipamentos", "Rastreamento", "Rotas", "Relatório",
  "Configurações" (`config/routes.ts:458-474`). Ponto vermelho no menu quando há solicitação de coleta não vista
  (`components/layout/SidebarMenuContent.tsx:186,423`); abrir o quadro marca como vista (`components/coletas/CollectionOrdersBoard.tsx:332-339`).
- Tela da ordem fora do layout: `/coletas/ordem/:id` → `pages/CollectionOrderPage.tsx` (`App.tsx:370`).
- Página pública do parceiro: `/portal/:token` → `pages/EntityPortal.tsx`, aba "Coletas" (`:1077`).

## 1. Etapas e regras (`lib/coletas/collectionTypes.ts`)
- Status: "Solicitada" → "Agendada" → "A caminho" → "Concluída", e "Cancelada" (`COLLECTION_STATUS_LABELS`). Só anda para a
  frente, uma etapa por vez; concluída e cancelada não saem do lugar (`COLLECTION_STATUS_FLOW`).
- Janelas: "Manhã", "Tarde", "Dia todo" (`WINDOW_LABELS`).
- Erro de arrastar fora da regra: "Transição inválida: Concluída → A caminho" (`CollectionOrdersBoard.tsx:533-537`;
  `hooks/useCollectionOrders.ts:243-247`). Não encenado na aula.

## 2. Quadro "Ordens de Coleta" (`components/coletas/CollectionOrdersBoard.tsx`)
- Colunas (`:120-157`): "Solicitada" (contorno tracejado âmbar, pedidos esperando aprovação), "Agendada", "A caminho",
  "Concluídas" (selo "Coluna de conclusão"), "Cancelada"; contador em cada cabeçalho; "Nenhuma ordem" na coluna vazia.
- Barra (`:1016-1066`): "Filtros" (painel: "Data agendada" "De"/"Até" com "As solicitadas aparecem sempre, independente da
  data.", "Status", "Parceiro", "Limpar Filtros", `:948-1004`), botões "Quadro"/"Lista", "Nova ordem".
- Cartão "Solicitada" (`:654-744`): "#N", "via portal", parceiro, material, "dd/mm/aaaa · Janela", cidade, "Solicitada em: ...",
  botões "Aprovar" (abre "Agendar coleta") e "Recusar" (abre "Recusar solicitação?", campo "Motivo", "Voltar",
  "Recusar solicitação", `:1248-1288`).
- Cartão das outras colunas (`:746-829`): "#N", janela, parceiro, cidade, motorista, placa, "Criada em: ...", botão
  "Preencher" (concluída: "Relatório") e os botões das próximas etapas, sem "Concluída" (na "Agendada": "A caminho" e
  "Cancelada"; na "A caminho": "Cancelada") (`:632-652,812-825`). Menu "Ações da ordem": "Visualizar", "Editar",
  "Copiar link" (concluída), "Excluir" (`:568-626`).
- "Cancelar coleta?": "A ordem #N será marcada como cancelada. Essa ação não pode ser desfeita.", "Voltar", "Cancelar coleta" (`:1220-1246`).
- Toasts: "Ordem de coleta criada", "Status alterado para Agendada/A caminho/Concluída" (`hooks/useCollectionOrders.ts:197,321`).

## 3. Nova ordem (`components/coletas/CollectionOrderDialog.tsx`)
- "Nova ordem de coleta", texto "Agende uma coleta em um fornecedor ou cliente cadastrado — ou, pra quem pede coleta
  esporádica e não quer se cadastrar, em "Sem cadastro" (nome + telefone + endereço)." (`:419-430`).
- Etapas "Parceiro", "Coleta", "Frota" (`:145,432-463`); rodapé "Cancelar"/"Voltar", "Avançar", "Criar ordem" (`:732-777`).
- "Parceiro": "Parceiro da coleta" ("Cadastrado" / "Sem cadastro"), "Tipo" ("Fornecedor"/"Cliente"), "Parceiro *"
  ("Selecionar…" → janela "Selecionar Fornecedor", busca "Buscar por nome, apelido, CPF/CNPJ ou telefone...",
  `:781-791`); endereço preenchido do cadastro do parceiro e editável (`:336-351,555-572`).
- "Coleta": "Data agendada" (campo de data), "Período" ("Não definido", "Manhã", "Tarde", "Dia todo", conforme
  Configurações), "Material estimado" ("Ex: ~500kg de ferro"), "Observações" ("Detalhes da coleta, ponto de
  referência…") (`:661-729`).
- "Frota": "Motorista" e "Veículo" (autocompletar + "+"), quadro "Revisão" (`:574-659`).
- A ordem interna já nasce "Agendada" (`:384-388`).

## 4. Agendar coleta (`components/coletas/ScheduleCollectionDialog.tsx`)
- Portão de "Agendada" a partir de "Solicitada" ("Aprovar" ou arrastar): "Agendar coleta", "Ordem #N — informe a data e a
  janela da coleta.", "Data da coleta *" (vem a data pedida), "Janela *" (vem a pedida), "Motorista *"/"Veículo *" só com
  "Exigir motorista e veículo para agendar"; "Cancelar", "Agendar" (`:102-196`).

## 5. Tela da ordem (`pages/CollectionOrderPage.tsx`)
- Cabeçalho "Ordem #N", parceiro e selo do status; quadro com "Fornecedor" (ou "Cliente"), "Endereço", "Agendamento",
  "Frota" ("Motorista · placa"), "Material estimado", "Observações" (`:1129-1229`).
- Bloco "Equipamentos" com "Entreguei" e "Recolhi": "Tipo de equipamento", "Unidade" (Entreguei: só as que estão na base;
  Recolhi: só as que estão com o parceiro), "Adicionar"; linha "Caçamba 5 m³ — Caçamba 03" (`:1231-1347`). As
  movimentações valem quando a coleta é concluída (`hooks/useCollectionOrders.ts:228-232,284-292`).
- "Checklist" e "Assinatura" ("Motorista", "Responsável no local") só se configurados (`:1349-1408`); o mundo não usa.
- Aviso com a ordem "A caminho": "Localização em registro — ..." ou "Sem sinal de GPS — ..." (`:1162-1185`); a aula não
  comenta (rastreamento fora da trilha).
- Rodapé: "Iniciar coleta" (agendada), "Concluir coleta" (a caminho), "Falta para concluir: ..." (`:1411-1470`).
- Concluída: relatório "Relatório de Coleta N", "Voltar às ordens" (`:302-361`).

## 6. Detalhe da ordem (`components/coletas/CollectionOrderDetailDialog.tsx`)
- "Ordem #N", selo do status, "Via portal"/"Interna", "Detalhes da ordem de coleta."; "Parceiro" ("(Fornecedor)"),
  "Endereço", "Material estimado", "Agendamento", "Motorista", "Veículo", "Observações", "Criada em", "Concluída em"
  (`:195-307`).
- "Equipamentos movimentados": "Recolhido · Caçamba 5 m³ (Caçamba 03)", "Entregue · ..." (`:309-356`).
- "Histórico": linhas "Agendada → A caminho" com data e hora, motivo embaixo quando houver; "Nenhum evento registrado ainda."
  (`:420-474`). Rodapé "Editar", "Preencher"/"Relatório", próximas etapas; na solicitada "Recusar"/"Aprovar" (`:477-546`).

## 7. Portal do parceiro (`components/portal/PortalCollectionsTab.tsx`, `PortalRequestCollectionDialog.tsx`)
- Aba "Coletas": título "Coletas", botão "Solicitar coleta", lista "Minhas coletas" (`PortalCollectionsTab.tsx:77-103`).
- "Solicitar coleta", "Peça a coleta do seu material. A empresa confirma o dia e o horário.": "Tipo" ("Coletar material"),
  "Material *" ("ex: Sucata de ferro"), "Quantidade estimada" ("ex: 500 kg"), "Data preferida" (sem dia passado),
  "Período" ("Selecione o período"), "Endereço da coleta" (do cadastro), "Observações", "Cancelar", "Solicitar coleta";
  toast "Solicitação enviada (#N)" (`PortalRequestCollectionDialog.tsx:177-279`). O material vira "Material — quantidade" (`:117-121`).
- Edge `collection-request` (`supabase/functions/collection-request/index.ts`): token, opção do parceiro, senha da aba
  Coletas, módulos `portal_cliente` e `coletas`, regras de antecedência e dias aceitos (`lib/coletas/collectionSettings.ts:81-116`),
  status "solicitada" com "Exigir aprovação da solicitação" ligado (senão "agendada") (`:215-217`), aviso aos usuários.

## 8. Frota (`components/coletas/FrotaSection.tsx`, `VehiclesTab.tsx`, `DriversTab.tsx`)
- Abas "Veículos" e "Motoristas" (`FrotaSection.tsx:7-10`).
- Veículos: "Veículos", "Mesma frota usada na pesagem de compra/venda.", "Novo veículo"; lista "Veículos da frota" com
  busca "Buscar placa, descrição ou RNTRC"; detalhe com a placa no modelo Mercosul, "Cadastro compartilhado com pesagem e
  documentos de transporte.", "Capacidade operacional" ("Tara", "Capacidade", "Volume"), "Identificação", "Dados de
  transporte" (`VehiclesTab.tsx:187-301,442-455`).
- "Novo veículo" ("Cadastro dos veículos da frota (compartilhado com a pesagem)."): "Dados básicos": "Placa *" ("Ex:
  ABC1D23", desenho da placa), "Descrição / Apelido" ("Ex: Caminhão Munck"); "Dados de transporte (MDF-e / NF-e)": "UF de
  licenciamento", "RNTRC", "Tipo" ("Veículo único (truck, toco, utilitário)"...), "Tipo de rodado" ("Truck", "Toco"...),
  "Tipo de carroceria", "Tara (kg)", "Capacidade (kg)", "Capacidade (m³)"; "Cancelar", "Cadastrar" (`:642-888`;
  `lib/coletas/fleetOptions.ts`). Toast "Veículo cadastrado" (`hooks/useFleet.ts:122`).
- Motoristas: "Motoristas", "Novo motorista"; busca "Buscar nome, CPF, telefone ou CNH"; detalhe "Dados pessoais" e
  "Carteira de habilitação" ("Número da CNH", "Categoria", "Validade") (`DriversTab.tsx:164-205,336-349`).
- "Novo motorista" ("Cadastro dos motoristas da frota (compartilhado com a pesagem)."): "Nome *" ("Ex: João da Silva"),
  "CPF", "Telefone", "CNH" ("Nº de registro (11 dígitos)"), "Categoria" ("Não informado", "A"... "E"...), "Validade da CNH";
  "Cancelar", "Cadastrar" (`:500-612`). Toast "Motorista cadastrado" (`hooks/useFleet.ts:198`). Sem validação de CPF/CNH.

## 9. Equipamentos (as caçambas) (`components/coletas/EquipamentosSection.tsx` e vizinhos)
- Abas "Equipamentos" e "Movimentações"; botão "Configurações" (`EquipamentosSection.tsx:12-15,48-63`).
- "Tipos de equipamento" ("Caçamba, bag, caixa, palete. O regime do tipo decide o resto: “uma a uma” ...; “por quantidade”
  ..."): tabela "Nome", "Regime" ("Uma a uma"/"Por quantidade"), "Quantidade", "Situação", "Ações"; "Mostrar inativos",
  "Novo tipo" (`:76-83`; `EquipmentTypesCrud.tsx:146-308`). Janela "Novo tipo de equipamento": "Nome *" ("Ex: Bag 1m³,
  Caçamba 5m³"), "Cada unidade tem identificação própria" (`:310-402`).
- "Unidades identificáveis": lista "Equipamentos" com identificação, tipo, lugar ("Minha base", parceiro, "Externo", "Sem
  movimentação") e condição ("OK", "Em manutenção", "Baixada"); "Nova unidade"; detalhe com "Editar", "Movimentar",
  "Posição atual" ("Nesta posição há ..." ou "Ainda sem movimentação registrada"), "A posição é calculada automaticamente
  pelo histórico de movimentações.", "Cadastro" (`ContainersTab.tsx:200-447`). Janela "Nova unidade" ("A posição atual vem
  das movimentações e não é editada neste formulário."): "Identificação *" ("Ex: Caçamba 01"), "Tipo de equipamento *",
  "Condição"; "Cadastrar" (`:449-480`). Toast "Unidade cadastrada" (`hooks/useCollectionContainers.ts:61`).
- "Onde tudo está agora" ("Soma do que está na base, em campo e com parceiros. ..."): "Equipamentos", "Na base", "Em
  campo", "Com parceiros"; tabela "Identificação", "Tipo", "Lugar atual", "Desde", "Condição"; "Movimentar"
  (`EquipamentosSection.tsx:95-99`; `EquipmentPositionTab.tsx:97-100,412-416`).
- "Nova movimentação" ("Lançamento avulso de equipamento — de onde saiu pra onde foi."): "De *" e "Para *" com "Minha
  base", "Parceiro", "Externo" ("Compra nova, perda ou baixa — entra ou sai do sistema rastreável."), "Data",
  "Equipamentos *", "Observação"; "Cancelar", "Registrar" (`NewEquipmentMovementModal.tsx:46-54,587-690`). Toast
  "Movimentação registrada" (`hooks/useCollectionEquipmentMovements.ts:106-108`).
- "Movimentações": "Data", "Usuário", "Equipamento", "De → Para"; as que vieram de ordem levam "Ordem N" e o aviso "Esta
  movimentação veio de Ordem N — para corrigir ou excluir, edite a própria ordem (bloco Entreguei/Recolhi)."
  (`EquipmentHistoryTab.tsx:160-169,323,450-480`).

## 10. Relatório (`components/coletas/CollectionReportTab.tsx`)
- "Período" (padrão "Este mês"; "Mês passado"...), "Total de coletas", "Concluídas", "Canceladas", "Taxa de conclusão"
  (concluídas ÷ (total − canceladas)), "Por status", "Por motorista", "Por veículo", "Por parceiro" (`:108-207`).
- Cada ordem entra no período pela data de conclusão; sem ela, pela data agendada; sem data, pelo dia em que foi criada
  (`:57-74`). A fonte diz que ordem sem data não aparece: na 1.59.154 ela aparece.

## 11. Configurações (`components/coletas/CollectionSettingsTab.tsx`)
- "Operação": "Prefixo da numeração" ('Ex.: "COL-"', 'Aparece antes do número da ordem (ex.: "COL-8"). Vazio = só o
  número.', salva ao sair do campo: "Prefixo da numeração salvo"), "Janelas de coleta oferecidas" ("Manhã", "Tarde", "Dia
  todo"; "Períodos que aparecem ao agendar uma coleta."), "Exigir motorista e veículo para agendar" (`:111-180`).
- "Portal e solicitações": "Exigir aprovação da solicitação", "Antecedência mínima (horas)" ("Antecedência mínima salva"),
  "Dias aceitos para coleta" ("Dom" a "Sáb"; "Dias aceitos salvos"), "Avisar quando chegar solicitação" (`:182-271`).
- "Checklist da coleta" e "Relatório público" (fora da aula) (`:273-395`). Padrões: sem prefixo, as três janelas, sem exigir
  frota, com aprovação, antecedência 0, segunda a sábado, com aviso (`lib/coletas/collectionSettings.ts:20-32`).

## 12. Backend que as telas chamam
| Ação | Chamada |
|---|---|
| Listar ordens | `collection_orders` (paginado), `collection_settings`, `collection_order_events` (`hooks/useCollectionOrders.ts:131-146`; `hooks/useCollectionOrderEvents.ts:26`) |
| Criar ordem | `rpc get_next_collection_order_number` + insert em `collection_orders` (`:172-184`) |
| Mudar etapa, aprovar, concluir | `rpc change_collection_order_status` (`p_to`, `p_nota`, data, janela, `p_fleet`, `p_equipment_lines`) (`:284-292`) |
| Parceiros, frota | `suppliers`/`customers` (`CollectionOrderDialog.tsx:194-243`), `drivers`, `vehicles` (`hooks/useFleet.ts`) |
| Equipamentos | `collection_equipment_types`, `collection_containers`, `collection_equipment_positions`, `collection_equipment_movements`; `rpc register_collection_equipment_movement` |
| Tela da ordem | `collection_orders` (detalhe), `collection_order_equipment_movements`, `collection_driver_locations` (insert com posição); relatório pela edge `collection-report` |
| Portal | edges `entity-portal` e `collection-request` |
| Solicitações não vistas | `collection_orders` (`hooks/useUnviewedCollectionRequests.ts:42`) |
| Configurações | `collection_settings` upsert (`hooks/useCollectionSettings.ts:65`) |
