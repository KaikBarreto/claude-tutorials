# Inventário · T16 · Nota Fiscal de mercadoria (NF-e)

> Levantado em 10/11/2026 (segunda tentativa, depois do reinício das 00:40).
> Código da versão gravada `APP_VERSION = "1.59.154"` (`src/config/version.ts:16`), cópia somente leitura em
> `/home/claude/ecoflix/app-src-1.59.154/`. Caminhos relativos a `src/`, exceto `supabase/...`.

## 1. Onde fica
- Menu lateral "Fiscal & Ambiental" → "Notas Fiscais (NF-e)" → `/fiscal-ambiental/nfe/entrada` (`config/routes.ts:428-445`).
  Outros itens do submenu (fora desta aula): "SPED Fiscal" (selo "BETA"), "Notas de Serviço (NFS-e)", "Transporte (MDF-e)",
  "Ambiental (MTR/CDF)", "Estoque Fiscal".
- Sub-abas da tela NF-e (`config/fiscalAmbientalTabs.ts:75-81`; rótulos `pages/NotasFiscais.tsx:176-179`): "Entrada",
  "Saída", "Notas Recebidas", "Inutilizadas".
- Permissão `screen_notas_fiscais`; ações `action_emit_nfe`, `action_manifest_inbound`, `action_export_contabil`
  (`config/routes.ts:248-253`). Módulo `notas_fiscais` (🔒).

## 2. Configuração Fiscal (`/fiscal-ambiental/configuracao/:secao`, `pages/ConfiguracaoFiscal.tsx`)
- Botão "Configurações Fiscais" no cabeçalho da tela NF-e (`pages/NotasFiscais.tsx:1832-1843`) → página "Configuração
  Fiscal", descrição "Tudo que a SEFAZ precisa saber antes da primeira nota." (`ConfiguracaoFiscal.tsx:1192-1201`).
- Trilho (`:924-980`): grupo "Emissão": "Certificado", "Empresa"; "Regras fiscais": "Impostos (padrão)" (sublabel "usado
  quando nenhum cenário se aplica"), "Cenários"; "Documentos": "Numeração", "Transportadora", "Serviços".
  Sem certificado, Empresa/Impostos/Numeração/Transportadora ficam apagados com "precisa do certificado digital"; quem
  entra por link vê "Esta seção só abre depois do certificado digital" / "É o certificado que assina a nota. Sem ele,
  nada do que for preenchido aqui chega na SEFAZ." e "Ir para o certificado" (`:985-1000`).
- Rodapé (`:1087-1096`, `:1239-1282`): "Esta seção salva sozinha, item a item" (Certificado, Cenários, Numeração,
  Transportadora, Serviços) ou "Alterações não salvas" / "Sem alterações pendentes" + "Descartar alterações" e
  **"Salvar configuração"** ("Salvando..." / "Cadastrando...") em Empresa e Impostos.
- Salvar (`handleSave`, `:696-909`): grava `company_fiscal_config` e chama a edge `plugnotas-register-company`
  (toast "Empresa cadastrada no sistema de NF-e!"); edge `ibge-cities` se faltar o código IBGE.

### 2.1 Certificado (`components/notas-fiscais/CertificadoSection.tsx`)
- "Passo 1 de 3: Configure primeiro o certificado digital." (`:309`); "Certificado Digital A1" / "Necessário para assinar
  e transmitir notas fiscais" (`:321-323`).
- Sem certificado: "Certificado não configurado" (`:391`); "Arquivo do Certificado (.pfx ou .p12)", botão "Selecionar
  arquivo"; "Senha do Certificado" (placeholder "Digite a senha do certificado"; ajuda "Use a senha do próprio
  certificado digital, não a senha da empresa."); **"Validar Certificado"** ("Validando...") (`:394-457`).
- Sucesso: toast "Certificado validado com sucesso!" (`:279-285`); "Certificado validado!" + "Configure os dados da
  empresa" (ou "Empresa habilitada para NF-e" depois do cadastro) (`:342-348`); chip de validade "Válido até dd/mm/aaaa"
  (`CertificateValidityChip.tsx:38-40`); "Próximo: Configurar Empresa"; "Substituir Certificado" (`:353-360`).
- Validade implausível (> 400 dias): "Certificado enviado, mas a validade não confere" / "Pode ser recusado pela SEFAZ.
  Confirme com sua contabilidade se este é o certificado A1 vigente." (`:332-340`); chip "Validade não confere · confira
  com a contabilidade" (`CertificateValidityChip.tsx:46-50`).
- Backend: edge `plugnotas-upload-certificate`; edge `plugnotas-certificate-info` (`hooks/useCertificateInfo.tsx:48`);
  RPC `certificate_vault_status` e (só rollback) `certificate_upload_store_self`.

### 2.2 Empresa (`components/notas-fiscais/EmpresaSection.tsx`)
- "Passo 2 de 3: Preencha os dados da empresa para NF-e." (`:264`); "Dados da Empresa" (+ "Importar dados" quando vazio);
  "Razão Social *", "Nome Fantasia", "CNPJ *", "Telefone", "E-mail", "Inscrição Estadual", "Inscrição Municipal"
  ("Necessária para emitir NFS-e") (`:270-324`); "Endereço Fiscal" (endereço do cadastro + "Editar em Configurações ›
  Empresa") (`:331-381`); "Responsável técnico (CSRT)"; "Logo para Nota Fiscal".

### 2.3 Impostos (padrão) (`components/notas-fiscais/ImpostosTab.tsx`)
- "Passo 3 de 3: Selecione o regime tributário. Os campos serão ajustados automaticamente." (`:310`); "Regime Tributário *"
  / "Este campo controla todos os cálculos de impostos e campos visíveis"; opções "Simples Nacional", "Simples Nacional —
  excesso de sublimite", "Lucro Presumido", **"Lucro Real"** (`:317-338`). Lucro Real mostra o quadro "Lucro Real:" com
  "PIS: 1,65% | COFINS: 7,60% (Regime Não Cumulativo)", "ICMS destacado conforme CST", "Gera direito a crédito de
  PIS/COFINS", "Possibilidade de apuração de IPI" (`:375-385`) e preenche PIS 1,65, COFINS 7,6, CST 01, não cumulativo
  (`:252-257`).
- Blocos com CST (regime normal): "Contribuinte de ICMS", "Alíquota do ICMS interno, sem o FCP (%)", "Alíquota do FCP,
  que soma por cima do ICMS (%)"; "ICMS" ("CST Entrada", "CST Saída"); "PIS / COFINS"; "IPI ..."; **"CFOPs Padrão"**
  ("CFOP Entrada Interna", "CFOP Entrada Interestadual", "CFOP Saída Interna", "CFOP Saída Interestadual", "CFOP Saída
  Indústria", "CFOP Saída Exportação") (`:984-1060`); "Informações Complementares Padrão"; "Reservado ao Fisco
  (padrão)"; "Código de Benefício Fiscal (cBenef)"; **"Reforma Tributária (IBS/CBS)"** ("Calcular IBS e CBS
  automaticamente", "CST-IBS/CBS", "cClassTrib") (`:1197-1300`).
- **Achado**: `IbsCbsReformaBanner.tsx` (o aviso "Reforma Tributária: IBS/CBS na NF-e" com as datas 03/08/2026 e
  04/01/2027) **não é renderizado em nenhuma tela** da 1.59.154 (nenhum import). A fonte diz "O aviso fica fixo no topo
  da tela": vale o código, a aula não mostra esse aviso.

### 2.4 Cenários (`components/notas-fiscais/CenariosFiscaisTab.tsx`, `CenarioFiscalCard.tsx`)
- Cabeçalho "Cenários fiscais" / "Defina as condições da operação e o tratamento que entra na nota. Sem cenário aplicável,
  a configuração de Impostos continua valendo." (`CenariosFiscaisTab.tsx:170-177`); aviso fixo "O que você preenche aqui
  vai impresso na nota fiscal. Confirme com a sua contabilidade — o EcoSistema não faz recomendação fiscal." (`:206-211`,
  tem travessão na tela; na fala, sem).
- Vazio: "Nenhum cenário cadastrado" / "Suas notas continuam saindo pela configuração de Impostos, exatamente como saem
  hoje. ..." e **"Criar o primeiro cenário"** (`:243-256`); com itens: "Novo cenário", lista "Regras cadastradas" agrupada
  em "Venda · n" / "Compra · n".
- Editor (`CenarioFiscalCard.tsx`): "Nome do cenário *" (placeholder "Ex.: Venda para indústria de outro estado")
  (`:786-795`); selo "Não revisado" e "Marcar como revisado" (`:810-835`); "Etapa 1" **"Quando aplicar"** / "O cenário só
  entra quando a nota bate com todas estas condições. "Qualquer" deixa a condição aberta. Se duas regras servirem para a
  mesma nota, vale a mais específica." (`:847-852`); "Operação *" ("Venda", "Compra"); "Cliente da nota"; "Natureza da
  operação"; material ("NCM específico", "Posição (4 primeiros dígitos)", "Grupo de materiais", "Qualquer material");
  "Regime do parceiro"; "Destino" ("Dentro do estado", "Fora do estado", "Qualquer"); "Inscrição estadual"; "Tipo de
  parceiro" (`hooks/useFiscalScenarios.tsx:37-71`); "Etapa 2" **"O que aplicar"** / "Preencha só o que muda neste
  cenário. Campo em branco não é zero nem desligado: ..." (`:1338-1345`); "CFOP", "CST do ICMS", "Alíquota de ICMS (%)",
  "Diferimento (%)", "CST do PIS", "CST do COFINS" (placeholder "Usar a configuração de Impostos", `:138`).
- Botões "Descartar alterações", **"Criar cenário"** / "Salvar cenário"; toasts "Cenário criado", "Cenário salvo",
  "Cenário marcado como revisado" (`:1657-1662`, `:700-760`). Backend: tabela `fiscal_scenarios` (select/insert/update/
  delete, `hooks/useFiscalScenarios.tsx:89-121`).

### 2.5 Numeração (`components/notas-fiscais/SeriesNumeracaoTab.tsx`, `AdicionarSerieDialog.tsx`)
- Sub-abas "NF-e" / "NFS-e" (`ConfiguracaoFiscal.tsx:1040-1059`). "Série padrão das suas notas" / "Configure qual série é
  usada por padrão ao emitir uma NF-e nova."; "Entrada e saída usam a mesma série" (ligado) / "Deixe ligado se você só
  usa 1 série pra tudo."; "Série padrão"; "Pode digitar uma série que ainda não está cadastrada — ela é criada
  automaticamente na 1ª nota emitida." (`:80-158`).
- "Suas séries" / "Cadastre séries que você já usava em outros sistemas para continuar a numeração de onde parou.";
  linha "Série 1" + "Última nota emitida: N"; vazio "Nenhuma série cadastrada ainda."; **"Adicionar série"** (`:163-208`).
- Diálogo "Adicionar Série" ("Use isso pra cadastrar séries que você já usou antes do sistema, pra continuar a numeração
  de onde parou."): "Número da série", "Última nota emitida nessa série" ("Se você nunca emitiu nada nessa série, deixe em
  0. O sistema vai começar a próxima do nº 1."), "Cancelar", **"Adicionar"**; toast "Série adicionada com sucesso"
  (`AdicionarSerieDialog.tsx:43-81`; `hooks/useNfeSeries.ts:92`). Backend: `nfe_series`, `company_fiscal_config`.

### 2.6 Transportadora e Serviços
- `TransportadoraTab.tsx`: "Nova transportadora"; "Razão Social *" (placeholder "Nome da transportadora"), "CPF/CNPJ",
  "Inscrição Estadual", "UF", "Logradouro", "Número", "Bairro", "Cidade"; bloco "Veículo": "Placa" (placeholder
  "ABC1D23"), "UF Veículo", "RNTC (ANTT)"; **"Adicionar"**; toast "Transportadora cadastrada!"; vazio "Nenhuma
  transportadora cadastrada"; linha com "CPF/CNPJ: ..." e "• Placa: ..." (`:142-262`). Tabela `transportadoras`
  (`hooks/useTransportadoras.ts:37-69`).
- `components/servicos/ServicosManagerPanel.tsx`: "Novo serviço"; vazio "Nenhum serviço cadastrado" / "Cadastre os
  serviços que você presta para emitir NFS-e." / "Cadastrar primeiro serviço" (`:193-218`). É da nota de serviço (T17).

## 3. Cota mensal (`pages/NotasFiscais.tsx:1845-1903`, `hooks/useNfeTier.tsx`, `QuotaLimitBanner.tsx`)
- Selo no cabeçalho "N/limite Documentos" (verde; âmbar a partir de 80%; vermelho na cota) ou "N Documentos · Ilimitado";
  dica ao passar o mouse: nome do nível, "Até X documentos fiscais por mês.", "Você emitiu N neste mês.", "Próximo nível:
  ... — até Y docs/mês." (sem preço).
- Tolerância `TOLERANCE = 5` depois da cota nominal (`useNfeTier.tsx:63-76`; `supabase/functions/_shared/fiscal-quota.ts:7`).
  Cartão âmbar "Você já emitiu quase todas as notas do seu nível este mês" / "Ainda dá pra emitir mais N notas antes de
  travar. ..."; vermelho "Suas notas do mês acabaram" + "Aumentar nível" (abre `LimiteNivelModal`, que mostra preço: **não
  abrir**) (`QuotaLimitBanner.tsx:56-83`).
- Backend: `nfe_module_tiers` (level, name, doc_limit, price), `companies.nfe_tier`, RPC `count_fiscal_documents_in_month`.

## 4. Lista de NF-e (`pages/NotasFiscais.tsx`, `NotaFiscalTable.tsx`)
- Título da tela "Notas Fiscais (NF-e)" / "Gerenciamento de documentos fiscais eletrônicos"; "Notas Fiscais de Saída"
  (ou de Entrada) + abas "Produção" / "Homologação" (`NotasFiscais.tsx:1804-1807`, `:2073-2097`); filtro de período; busca;
  "Status"; **"Nova Nota"** e o menu de três pontinhos ("Mais opções de NF-e": "Exportação Contábil", **"Inutilizar
  numeração"**) (`:2101-2167`). Cartões do topo `InvoiceStatsCards`.
- Colunas "Número" ("#1249" + "Série 1"), "Data", "Cliente"/"Fornecedor", "Operação", "Valor", "Status", "Ações"
  (`NotaFiscalTable.tsx:750-765`). Selos: "Rascunho", "Pendente", "Aguardando SEFAZ", "Autorizada", "Rejeitada",
  "Cancelada", "Cancelando…", "Inutilizada" (`:122-131`).
- Clique na linha abre o detalhe: "Participante", "Identificação" (**"Chave NF-e:"**, 44 dígitos), "Valores", "Situação e
  emissão" ("Ambiente:" "Produção", "Autorizada em:", **"Protocolo de autorização:"**), "Observações e ocorrências"
  ("Motivo do cancelamento:") (`:500-700`).
- Menu da linha (`:329-489`): "Visualizar"; "Continuar preenchendo" (rascunho); "Emitir NF-e" (pendente); "Editar e
  reenviar (mesmo número)" / "Editar e reemitir com novo número" e "Inutilizar numeração" (rejeitada); "Consultar status"
  (aguardando); **"Download XML"**, **"Download DANFE"**, "Comprovante (Notinha)", **"Carta de Correção"**, "Gerar nota
  complementar" (autorizada); "XML de Cancelamento" (cancelada); "Histórico"; **"Cancelar"** / "Excluir" (rascunho).
- Polling `plugnotas-status` (5 s, depois 30 s) com toasts "Nota #N autorizada pela SEFAZ!", "Nota #N rejeitada: ...",
  "Nota #N cancelada" (`NotasFiscais.tsx:565-624`).

## 5. Nova Nota (`InvoiceTypeSelector.tsx`, `NovaNotaModal.tsx`)
- Seletor "Nova Nota Fiscal" / "Selecione o tipo de nota fiscal": cartões **"NF-e de Entrada"** ("Registrar nota fiscal
  de compra do fornecedor") e **"NF-e de Saída"** ("Emitir nota fiscal de venda para cliente"); "Cancelar".
- Barra de resumo: "Total da nota", "Itens", "N pendência(s) pra emitir" (dica "Falta resolver:") ou **"Pronta pra
  emitir"** (`NovaNotaModal.tsx:5546-5594`).
- Abas (`:5502-5511`): **"Dados"**, **"Itens"**, "Impostos", "Faturamento" (só a prazo), "Transporte", "Opções",
  "Pré-visualização". (O Guia Técnico diz "Dados & Itens": no código são dois passos.)
- Passo Dados: barra "Importar de" com **"Pedido"** e, só na entrada, **"Emissão em Massa (Caixa)"**; selo "Pedido
  importado" (`:5710-5745`); "Quem emite"; "Para quem" ("Cliente"/"Fornecedor"; busca "Buscar por nome, apelido, CPF/CNPJ
  ou telefone..."; na entrada, "Consumidor Final / Não Identificado"); "O que é" ("Natureza da Operação", "Outra
  operação", "CFOP"); "Numeração" ("Série", **"Número previsto"** só leitura, "Data e hora da emissão" "Padrão: agora",
  "Esta nota será emitida como Série 1 / Nº N", "Deixe em branco para emitir com a data e hora atuais.") (`:5755-6554`).
- Naturezas (`lib/nfe/natureOperations.ts:1-22`): saída "Venda de mercadorias" (5102 / 6102) e outras; entrada "Compra de
  mercadorias" (1102 / 2102), "Entrada de sucata para revenda (pessoa física)" (1102 / 2102) e outras
  (`NovaNotaModal.tsx:792-815`).
- Passo Itens: "Produtos/Itens"; bloco "Adicionar item" com "Selecionar material..." (preenche NCM do cadastro e o preço de
  venda na saída), "NCM" ("Buscar NCM"), "CFOP", "Qtd", "Vl. Unit.", "Desconto", "Vl. Total" e **"Incluir"**; toast "Item
  adicionado!" (`:486-750`, `:6691-6761`).
- Rodapé (`:8105-8199`): "Cancelar" / "Voltar", "Salvar Rascunho", **"Avançar"** (Dados) e **"Emitir Nota"** (dica
  "Corrija as pendências antes de emitir").
- Emitir: grava `invoices` + `invoice_items` (+ `invoice_orders`), toast **"Nota fiscal salva! Enviando para SEFAZ..."**
  (`:5182-5185`); edge `plugnotas-emit`, toast **"Nota fiscal enviada para processamento!"** (`hooks/usePlugNotas.tsx:88`);
  depois "Aguardando SEFAZ" e o polling acima até "Autorizada".

## 6. Visualizar (`NotaFiscalPreview.tsx`)
- Título "NF-e #N" + selo de status (`:1664-1672`); botões "DANFE", "Comprovante (Notinha)", "XML", "Gerar nota complementar",
  "Histórico" (`:744-796`); abas **"DANFE"** e **"XML"** (`:912-919`). Na nota autorizada, faixa verde no topo do DANFE com
  **"Chave de Acesso"** (botão copiar) e **"Protocolo"** (`:990-1008`); nota não autorizada leva a marca d'água
  "SIMULAÇÃO". Aba XML: "XML da nota" / "Mesmo arquivo enviado à SEFAZ. Pode selecionar e copiar trechos direto daqui." /
  "Copiar XML" (`:924-967`).

## 7. A partir de um pedido (`ImportarPedidoModal.tsx`)
- Botão "Pedido" da barra "Importar de" → **"Importar de Pedido de Venda"** (ou "de Compra") (`:637-640`); busca "Buscar por
  nº do pedido ou cliente..." + filtro de período; linha "Pedido <ref>" com data, parceiro, peso total, valor e **"Importar"**
  (`:360-436`, `:526`). Sem abas "Recentes"/"Buscar" (o Guia Técnico ainda cita).
- Ao importar: toast **"Pedido importado com sucesso!"** e selo "Pedido importado"; o parceiro vira o destinatário e os itens
  vêm com o **peso líquido** (bruto menos tara e impureza; `NovaNotaModal.tsx:3019-3051`, `:3147-3149`). Tabelas `sale_items`
  / `purchase_items`; RPC da lista de pedidos.

## 8. Emissão em Massa (Caixa) (`ImportarPedidosCaixaModal.tsx`; só na NF-e de Entrada)
- **"Emitir NF-e em massa"** / "Selecione as compras e confira exatamente como o lote será numerado e emitido." (`:1160-1161`);
  "1. Pedidos do lote" / "Escolha as compras que serão faturadas"; abas **"Por Caixa"** / "Por Fornecedor" (`:1168-1190`);
  data ("Hoje" ou "09 de novembro, 2026"); "Caixas de origem" (nome do operador, selo **"Fechado"**, hora de abertura);
  "Selecionar todos sem NF-e"; "N/M selecionados" (`:1196-1369`).
- "2. Configuração e resultado" / "Como as notas serão geradas": "Uma nota por pedido" ("Emite diretamente uma NF-e para cada
  pedido selecionado.") e **"Uma nota consolidada"** ("Junta os itens e abre a nota para você revisar antes de emitir.");
  "Série e numeração": "Série fiscal", "Último número usado", "Próximo número", "Faixa prevista para este lote" ("NF-e nº N");
  "Valor dos pedidos"; "N itens após consolidar."; rodapé "Cancelar" + **"Montar nota consolidada"** (ou "Emitir N notas
  agora") (`:927-1131`). Toast "N pedido(s) importado(s) com sucesso!" (`:924`).
- Consolidada por caixa entra como **"Consumidor Final / Não Identificado"** (nota contra a própria empresa)
  (`NovaNotaModal.tsx:2967-2983`).

## 9. Cancelar e Carta de Correção
- `CancelarNotaDialog.tsx` + `i18n/locales/pt-BR/invoices.json` (`cancelDialog.*`): **"Cancelar Nota Fiscal #N"** / "Esta ação
  irá marcar a nota fiscal como cancelada. Por favor, informe o motivo do cancelamento."; **"Motivo do Cancelamento"**
  (placeholder "Informe o motivo do cancelamento (mínimo 15 caracteres)..."; "Faltam N caractere(s) (mínimo 15 exigido pela
  SEFAZ)"; máximo 255); "Voltar", **"Confirmar Cancelamento"**. Até 24 h da autorização, sem alerta (depois, "Fora do prazo
  normal de 24h", até 480 h). Edge `plugnotas-cancel`; toasts "Nota fiscal cancelada" ou "Cancelamento em processamento, pode
  levar alguns instantes" (selo "Cancelando…") (`hooks/usePlugNotas.tsx:104-147`).
- `CartaCorrecaoDialog.tsx`: **"Carta de Correção - NF-e #N"**; alerta "Importante: A Carta de Correção (CC-e) permite
  corrigir erros em campos específicos da NF-e. Não é permitido corrigir: valores, quantidade, dados de identificação do
  remetente/destinatário, data de emissão, ou qualquer informação que altere o cálculo do imposto." (`:193-200`); "Nova Carta
  de Correção" / "Descreva de forma clara e objetiva a correção a ser feita"; **"Texto da Correção *"** (15 a 1000
  caracteres, contador "N/1000"); "Dica: Use o formato "Onde se lê '...', leia-se '...'" para deixar a correção clara.";
  "Fechar", **"Enviar CC-e"** (`:152-319`). Toast "Carta de Correção enviada com sucesso!" (`hooks/useCartaCorrecao.tsx:33`).
  Depois: "1 CC-e enviada", "PDF", "XML", "✅ Registrada na SEFAZ · protocolo ...". Limite 20 por nota. Edge `plugnotas-cce`.

## 10. Inutilizar (`InutilizarNumeracaoDialog.tsx`)
- Três pontinhos ao lado de "Nova Nota" → "Inutilizar numeração" → **"Inutilizar Numeração de NF-e"**; aviso **"Operação
  irreversível!"** com "Os números ficam permanentemente bloqueados", "Só funciona em números que NUNCA foram autorizados pela
  SEFAZ", "Prazo SEFAZ: até dia 10 do mês seguinte ao pulo", "Para anular nota emitida, use Cancelamento" (`:445-459`).
- Abas **"Por Faixa"** / "Inutilizar Rejeitadas" (`:491-503`); "Série *", "Ano *", **"Número Inicial *"**, "Número Final"
  ("Igual ao inicial"); resumo "Inutilizará as Notas #A até #B da Série 1, ano 2026" (`:509-578`); **"Justificativa *
  (mínimo 15 caracteres)"** (placeholder "Ex: Numeração não utilizada por falha de sistema durante emissão"); botão
  **"Inutilizar na SEFAZ"**; toast "Numeração inutilizada com sucesso". Edge `plugnotas-inutilize` (grava
  `nfe_inutilized_numbers`; marca `invoices` da faixa como `inutilizada`).
- Sub-aba "Inutilizadas": **"Numerações Inutilizadas"** / "Números fechados na SEFAZ que não viraram nota. Escolha o tipo para
  ver as inutilizações de Saída ou de Entrada." + "Saída" / "Entrada" (`NotasFiscais.tsx:2035-2070`); lista via RPC
  `get_invoices_paged` (`p_include_inutilizadas`).

## 11. DANFE e XML (`hooks/usePlugNotas.tsx:220-310`)
- Menu da linha "Download DANFE": PDF em aba nova, nome "DANFE N - Recicla Vale Metais" (atalho do bucket `nfe-danfes` ou
  edge `plugnotas-download`). "Download XML": arquivo "NFe N - Recicla Vale Metais.xml". "XML de Cancelamento" na cancelada:
  "Cancelamento N - ....xml".

## 12. Notas Recebidas (`notas-recebidas/NotasRecebidasTab.tsx`)
- Desligado: **"Ative as Notas Recebidas"** / "Com este recurso ativo, as NF-e emitidas contra o CNPJ da sua empresa (por
  fornecedores e indústrias que autofaturam) passam a entrar aqui automaticamente. Ative para começar a receber."; **"Ativar
  Notas Recebidas"**; nota "Este recurso consulta a base da SEFAZ pelo seu provedor fiscal. Dependendo do seu plano, pode haver
  consumo de cota — ..." (`:1797-1860`).
- Confirmação **"Ativar consulta de notas recebidas?"** ("Ao ativar, cada nota fiscal recebida dos seus fornecedores passa a
  contar na sua cota mensal de documentos fiscais — o mesmo limite das notas que você emite. ... A contagem vale a partir da
  ativação."; "Você já usou N de L documentos fiscais neste mês."); "Cancelar", **"Ativar mesmo assim"**; toast "Notas
  Recebidas ativado" (`:1308-1378`, `:430-436`).
- Ativo: **"Notas emitidas contra o seu CNPJ"** (dica: "São as NF-e que fornecedores emitiram tendo o seu CNPJ como
  destinatário, buscadas diretamente na SEFAZ. ..."), chave "Recurso ativo", **"Importar nota"**, **"Sincronizar agora"**,
  busca "Buscar por emitente, CNPJ, chave ou natureza"; colunas "Emitente", "Valor", "Emissão", "SEFAZ", "Manifestação",
  "Ações" (`:1898-2100`). Selos SEFAZ "Autorizada"/"Cancelada"/"Denegada"; manifestação "Ciência", "Confirmada",
  "Desconhecida", "Não realizada", "Sem manifestação" (`inboundShared.ts:93-143`).
- Menu da linha (`:1420-1620`): "Ver XML", "Ver/baixar PDF", **"Buscar documento"** (dica "Baixa o XML e o DANFE (não
  confirma nem recusa nada)"); "Financeiro": "Lançar despesa / conta", "Pendurar no saldo do fornecedor", **"Lançar
  compra…"**, "Contar no estoque fiscal"; "Manifestar": **"Confirmar operação"** (dica "Confirma que a compra/entrada é sua"),
  **"Desconhecer operação"**, **"Operação não realizada"**.
- Confirmar: sem justificativa; toast "Operação confirmada junto à SEFAZ" (`:559-583`). Negativas (`ManifestarDialog.tsx`):
  "Você está declarando à SEFAZ que NÃO reconhece esta operação." / "... NÃO foi realizada." + "Esta manifestação é
  registrada na SEFAZ e não pode ser desfeita."; justificativa mínima de 15; "Confirmar manifestação".
- 🚫 Ciência: não existe botão; é automática pelo provedor e não é pré-requisito do download (`inboundShared.ts:346-362`).
- Backend: edges `plugnotas-enable-dfe`, `plugnotas-dfe-sync`, `plugnotas-manifestar`, `plugnotas-dfe-fetch-doc`; hook
  `useInboundNfe`.

## 13. Importar por XML e casamento de material
- "Importar nota" (`ImportInboundNfeDialog.tsx`): **"Importar nota recebida"** / "Traga uma NF-e para esta lista pela chave
  de acesso ou pelo XML autorizado."; abas "Chave de acesso" / **"Arquivo XML"** ("Selecione o XML autorizado da NF-e");
  "Cancelar", **"Importar nota"**; "Aguardando a janela segura" / "Processando a nota" ("O XML está na fila da VPS e deve
  aparecer na lista em instantes."); **"Nota importada"** / "A NF-e já foi adicionada à lista. ..."; **"Concluir"**.
  RPC `dfe_inbound_import_enqueue` + fila de jobs (`hooks/useInboundNfeImport.ts:77-100`).
- "Lançar compra…" abre `components/ImportNfeXmlDialog.tsx` com o XML da nota: título "Importar NF-e nº N — <emitente>"
  (`:350`); "Fornecedor: <nome>" + "por CNPJ/CPF"; cartão por item: nome do XML, "cProd · NCM ...", selo de confiança
  **"alta"**, **"confira"**, "baixa" ou "sem correspondência" (`:73-77`), "Qtd", "Valor un.", "Material" (busca "Buscar
  material..."); "A NF-e traz só o peso líquido — bruto, tara e impureza continuam manuais."; rodapé "Contar também no estoque
  fiscal", "Cancelar", "Conferir na tela de compra" (dica "Ao continuar, abrimos um pedido novo na tela de Compra com estes
  itens preenchidos. Nada é lançado agora — ...") (`NotasRecebidasTab.tsx:2562-2595`).
- Regra do casamento (`lib/nfe/matchMaterial.ts`): código igual ou nome igual (sem acento e sem caixa) = "alta"; senão,
  palavras em comum (≥ 3 letras) / maior lista, NCM igual soma 0,15: ≥ 0,85 "alta", ≥ 0,6 "confira", ≥ 0,34 "baixa".
  "alta" e "confira" vêm marcados; "baixa" fica para o operador (`lib/nfe/buildImportModel.ts:61-66`).

## 14. Código × fonte (vale o código; vai no relatório)
1. **Aviso IBS/CBS "fixo no topo"**: o componente existe (`IbsCbsReformaBanner.tsx`) mas não é usado em tela nenhuma. A
   aula mostra o cartão "Reforma Tributária (IBS/CBS)" de Impostos e não fala das datas.
2. **"No XML autorizado, o nome do produto sai sem acento"**: no código, `sanitizeNfeText`
   (`supabase/functions/_shared/nfe-text-sanitize.ts:18-45`) mantém as letras acentuadas e o `xProd` vai com acento ao
   provedor (`plugnotas-emit/index.ts:2475`). Não dá para conferir: fica fora da fala.
3. **"Cancelado continua contando na cota"**: depende da RPC `count_fiscal_documents_in_month` (não está na cópia). Fica na
   fala como está na fonte; conferir no banco.
4. Guia Técnico desatualizado (a aula segue o código): abas "Dados" e "Itens" (não "Dados & Itens"); "Número previsto" (não
   "Número (automático)"); modal de pedido sem "Recentes"/"Buscar"; cancelamento até 24 h + 480 h; o bloco "Como funciona?"
   não existe mais na tela de NF-e.
5. Sobram na tela e não entram na fala: "SPED Fiscal" (selo "BETA", fora da trilha), "Exportação Contábil" (T17),
   `EmissionFlowTimeline.tsx` (não usado; serve de base para a ilustração do caminho da nota).
