# Inventário · T17 Transporte, serviço e o contador (EcoSistema 1.59.154)

Código lido em `/home/claude/ecoflix/app-src-1.59.154/` (só leitura). Caminhos relativos a `src/`. Rótulo entre aspas =
texto exato da tela. 🔒 Módulo **Notas Fiscais** (`screen_notas_fiscais`, todas as telas abaixo).

## 0. Fonte × código (o que muda no roteiro)
| Capítulo da fonte | No código | Roteiro |
|---|---|---|
| 2 Frota (pendência 3) | **Existe**: sub-aba "Frota" de Transporte (`/fiscal-ambiental/transporte/frota`), o mesmo cadastro de Coletas → Frota e da pesagem (`components/coletas/FrotaSection.tsx:12-24`) | capítulo feito na tela |
| 3 Configuração rodoviária: percurso e estados intermediários | **Mudou**: "Configurações do MDF-e" hoje só tem série e próximo número + ponte "Ir para Frota" (`mdfe/ConfigRodoviarioModal.tsx:24-33,134-218`). O percurso é preenchido **em cada manifesto**, na etapa "Trajeto e carga" (`mdfe/MdfePercursoCard.tsx:76-162`) | cap03 = série/número + o conceito do percurso (ilustração); o percurso é preenchido no cap04 |
| 8 NFS-e recebida (pendência 3) | **Existe**: Notas Fiscais (NF-e) → "Notas Recebidas" → aba "NFS-e" (`/fiscal-ambiental/nfe/recebidas-nfse`), com ativação própria e "Lançar despesa / conta" (`notas-recebidas/NotasRecebidasNfseTab.tsx`) | capítulo feito na tela |
| 9 Relatório Fiscal | Virou a 1ª aba de Estoque Fiscal: "Relatório fiscal" (`/fiscal-ambiental/estoque-fiscal/relatorio`; `App.tsx:509-517` redireciona os links antigos) | menu "Estoque Fiscal" |
| 11 Exportação Contábil | No menu "⋮" ("Mais opções de NF-e") das listas Entrada/Saída de NF-e (`pages/NotasFiscais.tsx:2098-2134`) | aberta por ali |
| 12 Mandar pro contador | Não há envio pelo sistema: o pacote é baixado como ZIP (`contexts/ExportProgressContext.tsx:142-156`) | fala + ilustração do pacote |

## 1. Menu e cabeçalho (todas as telas)
- Menu lateral "Fiscal & Ambiental" (`config/routes.ts:428-444`): "Notas Fiscais (NF-e)", "SPED Fiscal" (selo "BETA", fora da
  trilha, a câmera não para), "Notas de Serviço (NFS-e)", "Transporte (MDF-e)", "Ambiental (MTR/CDF)", "Estoque Fiscal".
- Cabeçalho (`pages/NotasFiscais.tsx:1795-1890`): trilha "Financeiro › <tela>"; título por tela (`:210-217`): "Transporte (MDF-e)",
  "Notas de Serviço (NFS-e)", "Notas Fiscais (NF-e)", "Estoque Fiscal"; subtítulo "Gerenciamento de documentos fiscais
  eletrônicos"; botão "Configurações Fiscais" só em NF-e e NFS-e (`:1830-1843`); selo da cota "<usados>/<limite> Documentos"
  (`:1846-1890`, tooltip "Até N documentos fiscais por mês.", "Você emitiu N neste mês.").
- Sub-abas (`pages/NotasFiscais.tsx:175-198`): NF-e "Entrada", "Saída", "Notas Recebidas", "Inutilizadas"; Transporte
  "Manifestos", "Frota"; Estoque Fiscal "Relatório fiscal", "Posição do estoque", "Histórico fiscal", "Fiscal × operacional".

## 2. Transporte → Frota · `/fiscal-ambiental/transporte/frota`
- Título "Frota (veículos e motoristas do MDF-e)" (`pages/NotasFiscais.tsx:1966-1973`); abas "Veículos" e "Motoristas"
  (`coletas/FrotaSection.tsx:7-10`).
- **Veículos** (`coletas/VehiclesTab.tsx`): "Veículos" + "Mesma frota usada na pesagem de compra/venda." (`:446-448`), botão
  "Novo veículo" (`:451-454`), busca "Buscar placa, descrição ou RNTRC" (`:490`); painel do veículo com "Editar" (`:209-212`),
  "Capacidade operacional" ("Tara", "Capacidade", "Volume"), "Identificação", "Dados de transporte" ("Utilizados na emissão de
  MDF-e e no transporte da NF-e.") (`:223-295`).
- Formulário "Editar veículo"/"Novo veículo" (`:642-888`): "Cadastro dos veículos da frota (compartilhado com a pesagem).";
  "Dados básicos": "Placa *" (placa Mercosul desenhada embaixo), "Descrição / Apelido"; "Dados de transporte (MDF-e / NF-e)":
  "UF de licenciamento", "RNTRC", "Tipo" ("Não classificar", "Cavalo mecânico (tração)", "Carreta / Reboque", "Veículo único
  (truck, toco, utilitário)"; ajuda "Usado pra montar a composição do MDF-e (cavalo + carretas).") (`lib/coletas/fleetOptions.ts:79-98`),
  "Tipo de rodado" ("Truck", "Toco", "Cavalo Mecânico", "VAN", "Utilitário", "Outros", `fleetOptions.ts:13-20`), "Tipo de carroceria"
  ("Não Aplicável", "Aberta", "Fechada/Baú", "Granelera", "Porta Container", "Sider", `:23-30`), "Tara (kg)", "Capacidade (kg)",
  "Capacidade (m³)" ("máx. 999 m³ — limite da SEFAZ"); botões "Cancelar" e "Salvar"/"Cadastrar".
  Aviso (só aviso) com peso abaixo de 1.000 kg: "Valor parece estar em toneladas — informe em quilos (ex.: 32.000)."
  (`lib/coletas/vehicleLimits.ts:39-45`). Toasts: "Veículo atualizado" / "Veículo cadastrado" (`hooks/useFleet.ts:121-124`).
- **Motoristas** (`coletas/DriversTab.tsx`): "Motoristas" (`:340`), "Novo motorista", painel com "Editar", "Dados pessoais",
  "Carteira de habilitação"; formulário "Editar motorista" ("Cadastro dos motoristas da frota (compartilhado com a pesagem).",
  `:502-507`): "Nome *", "CPF", "Telefone", "CNH" ("Nº de registro (11 dígitos)"), "Categoria", "Validade da CNH"; "Salvar".
  Toasts "Motorista atualizado" / "Motorista cadastrado" (`hooks/useFleet.ts:197-200`).
- Backend: tabelas `vehicles` e `drivers` (select/insert/update por `company_id`, `hooks/useFleet.ts:66-210`).

## 3. Transporte → Manifestos · `/fiscal-ambiental/transporte`
- Título "Manifesto Eletrônico de Documentos Fiscais (MDF-e)" (`pages/NotasFiscais.tsx:1960-1966`); cartões "MDF-e Autorizados",
  "MDF-e Pendentes", "MDF-e Rejeitados", "MDF-e Encerrados" (`InvoiceStatsCards.tsx:90-118`).
- `mdfe/MdfeTab.tsx`: busca "Buscar por nº, placa ou motorista..."; botões "Configurações do MDF-e" e "Novo MDF-e" (`:480-500`);
  vazio "Nenhum MDF-e encontrado" / "Crie um novo MDF-e para agrupar suas NF-es de transporte" (`:520-525`); colunas "Nº", "Data",
  "Motorista", "Placa", "Trajeto", "Valor", "Peso (kg)", "Status", "Ações" (`:568-580`); linha expandida "Motorista:", "Placa:",
  "Origem:", "Destino:", "Valor da carga:", "Peso bruto:", "Data de criação:", "Status:" (`:640-690`).
- Selos (`mdfe/MdfeStatusBadge.tsx:11-44`): "Pendente", "Aguardando SEFAZ", "Autorizado", "Rejeitado", "Cancelado",
  "Encerramento enviado", "Encerramento recusado", "Encerrado", "Cancelamento enviado", "Em contingência"...
- Menu "Ações" do autorizado (`MdfeTab.tsx:318-335`): "Encerrar", "Cancelar", "Baixar DAMDFE (PDF)", "Baixar XML".
  "Encerrar" não pede confirmação (`:198-206`). Diálogo "Cancelar MDF-e #N" (`:765-805`): "O cancelamento será enviado à SEFAZ e
  é irreversível.", "Atenção: O prazo para cancelamento geralmente é de 24 horas após a autorização, variando conforme a UF.",
  "Motivo do cancelamento (mín. 15 caracteres)", "Voltar", "Confirmar Cancelamento" (não usado na aula).
- Toasts (`hooks/useMdfe.tsx:73-170`, `MdfeTab.tsx:255-275`): "MDF-e #N autorizado!", "Encerramento enviado. A confirmação da
  SEFAZ aparece em instantes.", "MDF-e #N: encerramento confirmado pela SEFAZ".
- Backend: tabelas `mdfe_manifests`, `mdfe_invoices`; edges `plugnotas-mdfe-emit`, `plugnotas-mdfe-status` (consulta a cada
  5 s enquanto "Aguardando SEFAZ", "Encerramento enviado" ou "Cancelamento enviado", `MdfeTab.tsx:242-275`),
  `plugnotas-mdfe-enclose`, `plugnotas-mdfe-download`, `plugnotas-mdfe-cancel`, `mdfe-contingency`; RPC `mdfe_contingency_availability`.

## 4. "Configurações do MDF-e" (diálogo) · `mdfe/ConfigRodoviarioModal.tsx`
- Título "Configurações do MDF-e"; "Série e próximo número do manifesto. Útil quando a empresa já emitiu MDF-e em outro sistema."
  (`:135-141`); "Série", "Próximo Número", quadro "Série" / "Próximo MDF-e", botão "Sincronizar Numeração", "A numeração será
  sincronizada com o serviço fiscal. Use apenas se precisar ajustar a sequência." (`:149-201`); "Motoristas e veículos agora ficam
  em Transporte (MDF-e) → Frota, com categoria (cavalo ou carreta) e conferência dos limites da SEFAZ." + "Ir para Frota" (`:205-217`).
- Backend: lê `company_fiscal_config.last_mdfe_number/last_mdfe_serie` e o maior `mdfe_manifests.mdfe_number` (`:55-77`); o botão
  chama a edge `plugnotas-mdfe-sync-numbering` (não clicado na aula).

## 5. "Novo MDF-e (Manifesto Eletrônico)" · `mdfe/NovoMdfeModal.tsx`
- Título e "Selecione as NF-es autorizadas e preencha os dados do transporte." (`:912-917`); etapas "Notas fiscais", "Veículo e
  motorista", "Trajeto e carga", "Revisão e emissão" (`:62-67`); lateral "Resumo do MDF-e" / "Atualiza enquanto você preenche" com
  "NF-es", "Valor da carga", "Peso bruto", "Veículo", "Motorista", "Reboques", "Origem", "Destino" (`:117-131,1535-1575`); rodapé
  "Cancelar", "Voltar", "Continuar", "Criar MDF-e" (`:877-906`).
- Etapa 1 (`:957-1003`): "NF-ES VINCULADAS", busca "Buscar NF-e...", linhas "NF-e #<n>" + nome do cliente + valor; rodapé
  "<n> NF-e(s) selecionada(s) • Valor total: R$ ...". Só NF-e autorizada, com chave, fora de homologação (`:260-268`).
- Etapa 2 (`:1006-1260`): "COMPOSIÇÃO", "Veículo (tração)" (item "<descrição> • <placa> • <UF>" + selo do tipo), "Motorista"
  (item "<nome> (<CPF>)"); os campos "Tara do veículo (kg) *", "Tipo de rodado *", "Tipo de carroceria *" só aparecem quando faltam na
  Frota (`:1079-1140`); "Reboques / Carretas (opcional)"; seção recolhida "Frete de terceiros (CIOT)" (não usada).
- Etapa 3 (`:1333-1452`): "TRAJETO", "Carregamento (Origem)" (UF, Cidade; vem preenchido com a cidade da empresa, `:236-255`),
  cartão "Percurso (UFs Atravessadas)" / "Estados pelos quais o veículo vai passar (opcional)", "Adicionar UF ao percurso", linha
  "1ª UF" ("Selecione a UF", só os estados que não são origem nem destino) (`MdfePercursoCard.tsx:76-162`), "Descarregamento
  (Destino)" (também vem com a cidade da empresa); "Peso Bruto Total (kg)" (somado das notas: "Somado das notas selecionadas — edite se
  o peso bruto real diferir."), "Valor Total da Carga" (travado), "OBSERVAÇÕES".
  As cidades vêm da API do IBGE no navegador (`fetch servicodados.ibge.gov.br/.../municipios`, `:274-298`).
- Etapa 4 (`:1457-1533`): "Revise antes de emitir"; "Como emitir": "Normal" ("Envia para a SEFAZ agora") e "Contingência" ("Use
  quando a SEFAZ estiver indisponível"; ao escolher, "Motivo da contingência *" e "...Imprima o DAMDFE em papel antes de liberar o
  caminhão. Prazo de regularização: até 168 horas."); quadro verde "Tudo pronto para criar e emitir o MDF-e".
- Ao criar (`:680-823`): insert em `mdfe_manifests` (o número vem do gatilho) e `mdfe_invoices`; toasts "MDF-e #N criado" e
  "MDF-e #N enviado para SEFAZ!"; chama a edge `plugnotas-mdfe-emit` sozinho.

## 6. Notas de Serviço (NFS-e) · `/fiscal-ambiental/nfse`
- Título "Nota Fiscal de Serviço (NFS-e)" (`pages/NotasFiscais.tsx:2026-2032`); `NfseTab.tsx`: "Nova NFS-e" (`:479-483`); colunas
  "Número", "Data", "Tomador", "Valor", "Status", "Ações" (`:560-565`); selos "Rascunho", "Pendente", "Processando", "Autorizada",
  "Rejeitada", "Cancelada" (`:54-68`); menu "Visualizar", "Consultar status", "Baixar PDF", "Baixar XML", "Histórico", "Cancelar"
  (`:390-455`).
- "Nova NFS-e" (`NovaNfseModal.tsx`): barra "Total da nota" / "Base ISS" e selo "<n> pendência(s) pra emitir" ou "Pronta pra
  emitir" (`:693-735`); abas "Pessoas", "Serviço", "Valores", "Pré-visualização" (`:61-66`); rodapé "Voltar", "Cancelar", "Salvar
  Rascunho", "Avançar", "Emitir NFS-e" (`:843-905`).
  - Pessoas (`nfse/PessoasStep.tsx:84-215`): "Data de competência *", "Tomador do serviço *" com "Selecionar do cadastro" ou
    "Buscar pelo CNPJ".
  - Serviço (`nfse/ServicoStep.tsx:131-290`): "Local da prestação" ("País" Brasil, "Município"), "Serviço prestado" (+ "Puxar serviço
    salvo"), "Código de Tributação Nacional *" (busca "Buscar por código ou descrição..."), "Código do serviço (LC116)" (automático),
    "Situação do ISSQN", "Descrição do serviço *".
  - Valores (`nfse/ValoresStep.tsx:63-210`): "Valor do serviço", "Alíquota ISS %" (vem da lista do município quando ela traz,
    `ServicoStep.tsx:122-127`), "ISS retido na fonte", "Retenções federais (%)", prévia com "Base de cálculo do ISS" e "Valor líquido".
  - Pré-visualização (`nfse/EmitirStep.tsx`): o espelho da nota ("a definir" no número); bloqueio "Configure o certificado digital
    nas Configurações Fiscais." e aviso "Inscrição Municipal não configurada..." se faltarem (`NovaNfseModal.tsx:444-460`).
- Toasts: "Nota de serviço enviada para emissão" (`NovaNfseModal.tsx:679`). Status por consulta a cada 8 s, até 8 vezes
  (`NfseTab.tsx:259-280`).
- Backend: `nfse_invoices`, `nfse_invoice_services`, `customers`; edges `plugnotas-nfse-servicos-municipio` (códigos e alíquota do
  município, `nfse/CtribnacSelect.tsx:74-77`), `plugnotas-emit-nfse`, `plugnotas-nfse-status`.

## 7. NF-e → Notas Recebidas → NFS-e · `/fiscal-ambiental/nfe/recebidas-nfse`
- Título "Notas Recebidas (Distribuição DF-e)" e abas "NF-e" / "NFS-e" (`pages/NotasFiscais.tsx:1987-2024`).
- Desligado (`NotasRecebidasNfseTab.tsx:612-684`): "Ative as Notas de Serviço Recebidas", "...as notas de serviço (NFS-e) que
  prestadores emitem contra o CNPJ da sua empresa — contador, manutenção, segurança, frete de terceiro — passam a entrar aqui
  automaticamente, prontas pra virar despesa...", botão "Ativar NFS-e Recebidas"; diálogo "Ativar o recebimento de notas de
  serviço?" com "Ao ativar, cada nota de serviço recebida passa a contar na sua cota mensal de documentos fiscais — o mesmo limite
  das notas que você emite...", "Você já usou N de M documentos fiscais neste mês." e "Ativar mesmo assim" (`:425-498`).
- Ligado (`:686-880`): "Notas de serviço emitidas contra o seu CNPJ" (ajuda: "...Diferente da NF-e, a nota de serviço não tem
  manifestação... Serviço também não entra em estoque — por isso o caminho aqui é lançar a despesa."), "Recurso ativo",
  "Sincronizar agora", "Última sincronização ...", busca "Buscar por prestador, CNPJ/CPF, número, chave ou serviço", aviso fixo
  (`inboundNfseShared.ts:251-254`): "A NFS-e é da prefeitura, e só chega aqui a nota de cidade que entrou no sistema nacional. Se o
  prestador emite pelo site de uma prefeitura que ainda não entrou, a nota dele não vai aparecer — não é defeito do sistema. Nesse
  caso peça o PDF ao prestador e lance a despesa na mão."; colunas "Prestador", "Competência", "Emissão", "Valor", "Situação",
  "Ações"; selo "Lançada".
- Menu da linha (`:500-580`): "Baixar XML", grupo "Financeiro": "Lançar despesa / conta" → abre "Nova conta"
  (`contas/BillFormModal.tsx:852`) já com "A pagar (despesa)", "Valor", "Descrição" (= prestador) e as observações da nota
  (`lib/inboundBill.ts:222-271`); faltam "Vencimento *" e "Categoria *"; botão "Criar conta" → "Conta criada".
- Toasts: "Notas de serviço recebidas ativado", "<n> nota(s) de serviço sincronizada(s)" (`:262-318`).
- Backend: `company_fiscal_config` (flag `nfse_dfe_ativo`), `inbound_nfse`; edges `plugnotas-enable-nfse-dfe` e
  `plugnotas-nfse-dfe-sync` (`hooks/useInboundNfse.ts:195-240`); `financial_bills` pelo formulário de conta.

## 8. Estoque Fiscal · `/fiscal-ambiental/estoque-fiscal/<sub>`
- **Relatório fiscal** (`VisaoGeralTab.tsx`): cartões "Entrada" (abre "Emitidas por você", "Recebidas de Fornecedor"), "Saída",
  "Saldo (Saída − Entrada)" ("Positivo"/"Negativo"), "Pendentes + Rejeitadas" ("Aguardando envio ou rejeitadas" ou "Tudo em dia")
  (`:94-140`); "Entrada × Saída no período", "Distribuição por status", "Top Fornecedores", "Top Clientes". Período no filtro do
  cabeçalho ("Este mês", "Mês passado", ...). RPC `get_invoice_dashboard`.
- **Posição do estoque** (`FiscalInventoryPositionTab.tsx:118-230`): "Saldo fiscal agora, por material. Não altera o estoque
  operacional." / "Saldo fiscal em <data>."; "Informar saldo inicial" (não usado); "Data e hora da posição" (dias futuros
  desligados, `ui/RetroactiveDateTimePicker.tsx:135,222`), "Ver posição", "Voltar para agora"; colunas "Código", "Material", "Saldo
  fiscal". RPCs `get_fiscal_inventory_position` / `get_fiscal_inventory_position_at` (`hooks/useFiscalInventoryLedger.ts:90-110`).
- **Histórico fiscal** (`FiscalInventoryHistoryTab.tsx:160-450`): lista "Materiais" com "Geral (Todos)"; "KARDEX FISCAL — <material>"
  e "Entradas, saídas, cancelamentos e ajustes que formam o saldo fiscal."; colunas "Data", "Origem", "Material", "Nota / CFOP",
  "Movimento", "Antes", "Depois". RPC `get_fiscal_inventory_history_paged`.
- **Fiscal × operacional** (`EstoqueFiscalTab.tsx:440-670`): "Compare o movimento das notas fiscais com o movimento de compras e
  vendas no período selecionado."; cartões "Entradas Fiscais", "Saídas Fiscais", "Materiais com divergência", "Alertas";
  "Comparação por material", "Ocultar itens zerados"; colunas "Material", "Entrada Fiscal", "Saída Fiscal", "Mov. Fiscal", "Mov.
  Operacional", "Delta"; quadro "Como ler o Delta (fiscal − operacional)" ("Pedidos ainda não finalizados não entram no movimento
  operacional, o que também gera diferença." etc.). RPCs `get_fiscal_inventory_report_data` e `get_inventory_report_data`
  (`hooks/useFiscalInventory.tsx:120-136`).

## 9. Exportação Contábil (diálogo) · `ExportContabilDialog.tsx`
- Aberta pelo "⋮" "Mais opções de NF-e" → "Exportação Contábil" (`pages/NotasFiscais.tsx:2098-2134`, admin ou
  `action_export_contabil`).
- Título "Exportação Contábil", "Gera um pacote ZIP com XMLs, planilha e PDF resumo pra mandar pra contabilidade." (`:293-298`);
  "Período" (começa em "Este mês", `:62`); "Tipo de nota": "Saída", "Entrada"; "Status": "Emitidas", "Canceladas", "Inutilizadas",
  "Rejeitadas"; "Extras": "Incluir DANFEs (PDFs)" ("Adiciona uma pasta com o PDF de cada nota emitida no pacote.") e "Incluir
  MDF-e's? (XML + DAMDFE)" ("Adiciona os manifestos de transporte autorizados do período."); prévia "<n> notas no período (...)",
  "Tamanho estimado", "Tempo estimado"; botões "Cancelar" e "Baixar Pacote" (`:262-520`). Tudo marcado de saída (`:64-71`).
- Gera no navegador (`utils/contabilExport/runExportPipeline.ts`): "Iniciando exportação...", "Gerando PDF resumo...", "Compactando
  pacote..."; arquivo "Exportação Contábil - <Empresa> - <período>.zip" (`filenameUtils.ts:48-52`) com `AAAA-MM/xmls/saida`,
  `.../xmls/entrada`, `.../danfes/...`, `mdfe-xml/`, `mdfe-damdfe/`, "Relacao-Notas-Fiscais.xlsx", "Relacao-Notas-Fiscais.pdf" e
  "LEIA-ME.txt" (`:296-375`); toast "Exportação pronta" / "<n> saída + <n> entrada baixados" (`ExportProgressContext.tsx:150-156`).
- Backend: RPC `count_invoices_for_export`; tabelas `invoices` (XML), `nfe_events`, `nfe_inutilized_numbers`, `companies`,
  `profiles`, `mdfe_manifests`; storage `nfe-danfes`; edges `plugnotas-download` e `plugnotas-mdfe-download`.

## 10. Handoffs (o app; a fala não depende)
- H1. CDF e NFS-e mostram os cartões "Notas Emitidas / Notas Pendentes / Rejeitadas/Canceladas" da NF-e (`pages/NotasFiscais.tsx:1916`
  só esconde em outras abas): na NFS-e a câmera não para neles.
- H2. A ajuda do cartão de Exportação diz "estrutura plana" para um mês só, mas o código sempre cria a pasta `AAAA-MM/`
  (`runExportPipeline.ts:280-300`).
- H3. "Configurações do MDF-e" não fala de percurso, e a fonte (cap. 3) ainda chama de "Configuração rodoviária".
