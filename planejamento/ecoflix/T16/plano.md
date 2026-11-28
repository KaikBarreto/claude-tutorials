# Plano · T16 · Nota Fiscal de mercadoria (NF-e)

- **Título:** Nota Fiscal de mercadoria (NF-e) (o da fonte). 🔒 módulo **Notas Fiscais** (`notas_fiscais`).
- **Objetivo:** do certificado digital até a nota autorizada, na ordem da tela, e o que vem depois: cancelar, corrigir,
  inutilizar, baixar, receber e manifestar.
- **Antes:** Relatório Financeiro e DRE (T15). **Próximo:** Transporte, serviço e o contador (T17).
- **Regime do exemplo:** Lucro Real (Kaik, 10/11). A fala mostra os campos e diz que quem define é o contador; nenhum
  valor de imposto é explicado. **Emissão simulada:** não há SEFAZ, provedor, cota real nem numeração a queimar.
- **Duração:** ~35 min de vídeo (5.241 palavras de fala, ~33,6 min), numa aula só (Kaik, 18/11: "uma aula só do fiscal, mesmo que grande"). Passada do app 1.60.10 em 18/11: `cobertura_160.md` aplicada, 25 capítulos (6 novos: 11, 13, 14, 15, 17 e 18).
- **28/11: app 1.60.39** (`origin/main` de 26/11; detalhe e código em `andamento_160.md`, seção "28/11 · 1.60.39"). Mudou para a aula:
  aba "Impostos" (era "Impostos (padrão)") com as abas "NF-e e NFC-e" e "NFS-e" (cap04); o "Histórico" da NF-e é o diálogo único
  `FiscalDocumentHistoryDialog` (RPC `list_fiscal_document_history`, cap15); o "Filtros" da lista virou um painel com a seção "Status"
  (cap20); Notas Recebidas ganhou, em cima, a escolha "NF-e" / "NFS-e" e o botão **"Importar XML"** (edge `inbound-xml-import`: confere
  destinatário e protocolo; cap21 e cap23); a conferência do "Lançar compra…" mostra "Produtos", "Encargos/descontos" e "Total da nota"
  e a caixa "Registrar também no estoque fiscal (não altera o saldo físico)" (a compra em si é o cap11 da T17). Motor fiscal próprio
  (1.60.24) e ciência automática (1.60.33) não mudam a tela. 25 capítulos, 5.318 palavras (eram 5.264).
- Base: `inventario.md` (código 1.59.154) + `cobertura_160.md` e a seção 15 do inventário (o que mudou no 1.60.10, conferido na tela). Usuário logado: Rafael Nogueira (MASTER), desktop 1280×800, tema claro.
  `FAKE_NOW=2026-11-10T08:30:00-03:00`; todos os capítulos no mesmo dia, em ordem.

## Capítulos (os da fonte, na ordem)

| cap | Vinheta (área / título) | O que se mostra | Estado de partida |
|---|---|---|---|
| 00 | sem vinheta | Abertura: o problema (a carga de cobre só sai com nota), 🔒, "Antes: Relatório Financeiro e DRE". [ILUSTRAÇÃO] | `inicio` |
| 01 | FISCAL / Onde ficam as notas | Menu "Fiscal & Ambiental" (com "Relatórios Fiscais") → "Notas Fiscais (NF-e)"; sub-abas; "Configurações Fiscais", cota, cartões, "Nova Nota" (só com permissão de emitir). [ILUSTRAÇÃO] | `inicio` |
| 02 | CONFIGURAÇÃO / O certificado vem primeiro | "Configuração Fiscal": abas no alto, quatro apagadas; "1 · Certificado digital · primeira etapa da configuração fiscal". [ILUSTRAÇÃO ×2] | `inicio` |
| 03 | CERTIFICADO / Subindo o certificado A1 | Área de arrastar (.pfx), "Senha do Certificado", "Validar e salvar A1" → "Certificado validado!", "Válido até 14/09/2027"; a renovação anual. [ILUSTRAÇÃO] | `inicio` |
| 04 | CONFIGURAÇÃO / Empresa e impostos | "Empresa": "Importar dados", IE, endereço, logo e CSRT; "Impostos (padrão)": Lucro Real, ICMS e diferimento, PIS/COFINS, IPI, CFOPs, Informações Complementares Padrão, cBenef, IBS/CBS (par obrigatório); "Salvar configuração". [ILUSTRAÇÃO] | `apos-cap03` |
| 05 | CENÁRIOS / Cenários fiscais | Aviso fixo; cenário da Fundição (Venda, CNPJ; CST 51, diferimento 100); as outras condições (material, destino, regime, peso). [ILUSTRAÇÃO] | `apos-cap04` |
| 06 | NUMERAÇÃO / Série e numeração | O aviso âmbar da série não cadastrada; "Adicionar série" 1 / 1248; a série padrão (lista); séries separadas de entrada e saída. [ILUSTRAÇÃO] | `apos-cap05` |
| 07 | CONFIGURAÇÃO / Transportadora e serviços | Cargas Vale do Sol + placa; "Serviços" vazio. [ILUSTRAÇÃO] | `apos-cap06` |
| 08 | COTA / A cota de documentos | Selo "0/1.000 Documentos", o que conta, tolerância de 5. [ILUSTRAÇÃO] | `apos-cap07` |
| 09 | EMISSÃO / Nota avulsa, do zero | Nota em tela cheia: cabeçalho (número previsto, ambiente), "Quem emite", Serra Fina, natureza, numeração, cartão "Adicionar item" (Alumínio perfil 320 kg), detalhes do item, "Desconto geral", "Salvar Rascunho" → 1249 autorizada; "Visualizar". [ILUSTRAÇÃO] | `apos-cap07` |
| 10 | EMISSÃO / Nota a partir de um pedido | "Importar de" → "Pedido" (Fundição, Cobre mel 500 kg); "Transporte": frete, transportadora e "Volumes Transportados" (506 / 500 kg). Não emite. [ILUSTRAÇÃO] | `apos-cap09` |
| 11 | IMPOSTOS / Impostos e as outras abas | **Novo.** Na nota da Fundição: "Cenário fiscal aplicado", ICMS diferido, "PIS/COFINS Suspenso (CST 08)" (cliente indústria), "Ajustar impostos desta nota", IBS/CBS; "Faturamento" a prazo, boleto, 2 × R$ 11.975,00; "Opções" (xPed); "Informações complementares"; "Pré-visualização" → 1250 autorizada. [ILUSTRAÇÃO] | `apos-cap09` (o setup reabre a nota) |
| 12 | EMISSÃO / Nota de um caixa fechado | "Emissão em Massa (Caixa)", 09/11, caixa do Marcos → "Uma nota consolidada" → 1251 autorizada. [ILUSTRAÇÃO] | `apos-cap11` |
| 13 | EMISSÃO / Outras operações | **Novo.** A lista de naturezas; "Baixa de estoque por perda" (CFOP 5927, nota contra a própria empresa, "Dar baixa no estoque físico ao autorizar"); sai sem emitir. | `apos-cap12` |
| 14 | EMISSÃO / O que trava a emissão | **Novo.** Metalúrgica Pinhal: selo "3 pendências pra emitir", "Falta resolver:", aviso da IE (consulta por CNPJ) e "Usar IE ... e salvar no cadastro", "Completar cadastro" (CEP), item sem NCM → "Pronta pra emitir"; "Descartar". [ILUSTRAÇÃO] | `apos-cap12` |
| 15 | REJEIÇÃO / A SEFAZ recusou a nota | **Novo.** 1252 "Rejeitada pela SEFAZ" (Cód. 778): "Visualizar", "Histórico", os dois caminhos do menu, "Editar e reenviar (mesmo número)", NCM corrigido → autorizada. [ILUSTRAÇÃO ×2] | `apos-cap14` + `rejeitada-1252` |
| 16 | CORREÇÕES / Cancelar e corrigir | Cancelar a 1249; o prazo (24 h, até 20 dias, depois devolução); CC-e na 1250 e a lista "1 CC-e enviada". [ILUSTRAÇÃO ×2] | `apos-cap15` |
| 17 | DEVOLUÇÃO / Nota de devolução | **Novo.** NF-e de Entrada, "Devolução de venda" (CFOP 1202), "Selecionar nota do sistema" (1250), 40 kg = R$ 1.916,00, "Nota de origem de cada item" (item 1), sem Faturamento → 1253 autorizada. [ILUSTRAÇÃO ×2] | `apos-cap16` |
| 18 | COMPLEMENTAR / Nota complementar | **Novo.** Menu da 1250 → "Gerar nota complementar"; "Contar esta nota no Estoque Fiscal"; item Cobre mel 500 kg × R$ 0,50 = R$ 250,00; a prévia de impostos (sem ensinar valor) → 1254 autorizada. [ILUSTRAÇÃO] | `apos-cap17` |
| 19 | NUMERAÇÃO / Inutilizar numeração | "Inutilizar numeração": aviso (com o prazo do dia 10), "Por Faixa" 1246 a 1247, "Inutilizar Rejeitadas" (vazia); sub-aba "Inutilizadas". [ILUSTRAÇÃO] | `apos-cap18` |
| 20 | DOCUMENTOS / DANFE e XML | Menu da 1250 (DANFE, XML, Comprovante), o DANFE novo e a Reforma em 1º/12, "Visualizar" › XML, "XML de Cancelamento", detalhes da linha, busca/período/"Filtros"/"Homologação", "Exportação Contábil". [ILUSTRAÇÃO] | `apos-cap19` |
| 21 | NOTAS RECEBIDAS / As notas recebidas | "Ativar Notas Recebidas" → as duas notas. [ILUSTRAÇÃO] | `apos-cap19` |
| 22 | NOTAS RECEBIDAS / Manifestar a nota | "Ciência"; "Buscar documento"; grupos "Financeiro" e "Manifestar"; "Confirmar operação". [ILUSTRAÇÃO] | `apos-cap21` |
| 23 | NOTAS RECEBIDAS / Importar pelo XML | **1.60.39:** "Importar XML" (XML da Cooperativa, toast "NF-e importada com sucesso."); "Importar nota" pela chave (só citado) → "Lançar compra…": "alta" e "confira"; "Conferir na tela de compra" sem clicar (a compra é o cap11 da T17). [ILUSTRAÇÃO] | `apos-cap22` |
| 24 | RESUMO / Recapitulando | Montagem; o Cato fica no tutorial dele; "Próximo: Transporte, serviço e o contador". | `apos-cap23` |

Transições faladas: 01→02 "Antes de qualquer nota, a configuração"; 02→03 "Então, o certificado"; 03→04 "Com o
certificado validado, os dados da empresa"; 04→05 "E quando uma venda não segue o padrão?"; 05→06 "Agora, de qual
número a primeira nota sai"; 06→07 "Mais dois cadastros"; 07→08 "Antes de emitir, a cota"; 08→09 "Agora sim, a primeira
nota"; 09→10 "Quase sempre a nota nasce de uma venda que já está no sistema"; 10→11 "E as compras do dia, de quem não
emite nota?" (numeração de antes do 1.60.10). Novas: 10→11 "Antes de emitir, vale conferir o imposto"; 12→13 "Venda e compra são as
notas do dia a dia, mas..."; 13→14 "E quando a nota não deixa emitir?"; 14→15 "A nota passou pelas pendências... e mesmo assim
a SEFAZ recusou"; 15→16 "Nota autorizada, e se algo mudar?"; 16→17 "E quando a mercadoria volta?"; 17→18 "Último caso: a nota
saiu com valor a menor"; 18→19 "E o número que nunca virou nota?".

**Cuidados (⚠️) e o que não acontece (🚫), falados como na PERFIL:**

| Fonte | Onde | Fala (resumo) |
|---|---|---|
| ⚠️ ordem e contador | 02 | "Uma dica: faça essa configuração junto com o contador..." |
| ⚠️ validade estranha | 03 | "Uma dica: o A1 vale no máximo um ano..." (sem encenar o arquivo errado) |
| ⚠️ IBS/CBS | 04 | O cartão "Reforma Tributária (IBS/CBS)" e os códigos do contador. Sem datas (o aviso do topo não existe na 1.59.154) |
| ⚠️ impresso na nota / específico vence | 05 | o aviso fixo lido; "Uma dica: não precisa um cenário por combinação..." |
| ⚠️ cota | 08 | o que conta, a tolerância de 5, cancelada conta, recebida só depois de ativar |
| ⚠️ credenciamento | 09 | "Uma dica: antes da primeira nota, confirme com o contador o credenciamento..." |
| ⚠️ enviado ≠ autorizado | 09 | "Uma dica: enviada para processamento ainda não é autorizada..." |
| ⚠️ líquido, não bruto | 10 | "Uma dica: quando o cliente disser que o peso da nota não bate com o ticket..." |
| ⚠️ nome sem acento no XML | fora | não conferível no código (inventário 14.2); fica de fora |
| 🚫 ciência | 16 | "A ciência não é um botão: ela já vem sozinha. Pra baixar, é Buscar documento." |

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)

**Começa com (`inicio`, fim do T15):** módulo `notas_fiscais` ligado; **nenhum** certificado, `company_fiscal_config` sem
razão social nem regime (ou sem linha), `nfe_series`, `transportadoras`, `fiscal_scenarios` e `invoices` vazios; Notas
Recebidas desligado (`dfe_ativo` false); `companies.nfe_tier` 1. Endereço da empresa completo em Configurações › Empresa
(T1), com o código IBGE de Taubaté (3554102). `companies.name` "Recicla Vale Metais", telefone e e-mail `.example`.

| Item | Valores (fictícios) |
|---|---|
| Níveis (`nfe_module_tiers`) | o catálogo do app (junção, item 6): "Nível 1" 1.000 documentos/mês, "Nível 2" 3.000, "Nível 3" 5.000 (preço na tabela, nunca na tela); a empresa no Nível 1 (`useNfeTier.tsx`: tolerância de 5; âmbar a partir de 80 %; o selo `0/1.000 Documentos`). A fala não diz a cota |
| Certificado (cap 03) | arquivo `recicla-vale-metais-a1.pfx` (bytes falsos, < 200 KB), senha fictícia digitada mascarada; `plugnotas-certificate-info` devolve `certificateName` "RECICLA VALE METAIS LTDA", `vencimento` 2027-09-14, `daysRemaining` 308 |
| Empresa (cap 04) | Razão Social "Recicla Vale Metais Ltda", Nome Fantasia "Recicla Vale Metais", CNPJ da semente, **IE 688.047.314.106** (SP, dígitos válidos) |
| Impostos (cap 04) | "Lucro Real" (o quadro preenche PIS 1,65, COFINS 7,6, CST 01, não cumulativo); "Contribuinte de ICMS" ligado, ICMS interno 18 (padrão), CST e CFOPs no padrão da tela (1102, 2102, 5102, 6102, 5101, 5502); IBS/CBS ligado com CST-IBS/CBS 000 e cClassTrib 000001 em Saída e Entrada ("o que o contador passou") |
| Cenário (cap 05) | "Venda para a Fundição Bandeira do Vale": Operação "Venda"; "Cliente da nota" "Um cliente/fornecedor específico" = CNPJ da Fundição; o resto "Qualquer"; "CST do ICMS" 51 e "Diferimento (%)" 100 (do contador; a fala não lê os números) |
| Série (cap 06) | Série 1, "Última nota emitida nessa série" 1248 (a Recicla emite pelo EcoSistema desde agosto; a semente desta aula tira a configuração fiscal e as notas para mostrar a configuração do zero); a próxima é 1249. Em outubro, o "Última nota emitida" da série foi acertado errado (1247 em vez de 1245; o número da nota não se digita na emissão) e a 1248 saiu depois da 1245: 1246 e 1247 nunca viraram nota (cap 13) |
| Transportadora (cap 07) | **Cargas Vale do Sol Ltda**, CNPJ **41.826.537/0001-92**, IE **688.115.922.408**, SP, Rua dos Ferroviários, 380, Vila São José, Taubaté; placa **FJR3B27**, UF SP (conferir na semente que o nome não é de empresa real) |
| Clientes | Serra Fina Alumínio Reciclagem e Fundição Bandeira do Vale: PJ em SP, CNPJ e IE válidos, endereço completo, cadastro fiscal completo (sem selo "Incompleto") |
| Venda (cap 10) | pedido de venda de **ontem, 09/11 10:40** (junção: o T6 não tem caixa aberto em 10/11 antes das 08:31), no caixa #84 do Rafael, Pix na Conta Secundária, Fundição Bandeira do Vale, Cobre mel: bruto 506 kg, tara e impureza 6 kg, **líquido 500 kg × R$ 47,90 = R$ 23.950,00**, sem nota |
| Caixa fechado (cap 11) | caixa do **Marcos Antunes de 09/11** (segunda), aberto 07:02, **Fechado**, com 3 compras sem nota de pessoa física: Dona Cida (Alumínio latinha 38 kg, Papelão 120 kg), Valdir Pereira (Ferro misto 410 kg), Dona Cida (Alumínio latinha 26 kg, Papelão 60 kg). Consolidado: latinha 64 kg (R$ 396,80), papelão 180 kg (R$ 99,00), ferro misto 410 kg (R$ 307,50) = **R$ 803,30**, 3 itens. Se o histórico do Mundo já tiver esse caixa, usar o dele e ajustar a fala |
| Notas emitidas | 1249 Serra Fina, Alumínio perfil 320 kg × R$ 10,40 = **R$ 3.328,00**, CFOP 6102 (Serra Fina em Itamonte, MG); 1250 Fundição, Cobre mel 500 kg = R$ 23.950,00, frete "0 - Frete por conta do Remetente (CIF)", Cargas Vale do Sol (FJR3B27); 1251 entrada, Consumidor Final, "Entrada de sucata para revenda (pessoa física)", R$ 803,30. Chave de 44 dígitos: `35` + `2611` + CNPJ + `55` + `001` + número com 9 dígitos + `1` + código de 8 dígitos + DV (módulo 11); protocolo de 15 dígitos (`13526000…`); `authorized_at` no mesmo dia |
| Cancelamento (cap 12) | 1249, motivo "Pedido alterado pelo cliente antes de a mercadoria sair do pátio" |
| CC-e (cap 12) | 1250: "Onde se lê 'Placa FJR3B27', leia-se 'Placa GKM5D18'. A transportadora trocou o veículo da carga." |
| Inutilização (cap 13) | Série 1, ano 2026, 1246 a 1247, justificativa "Numeração pulada na emissão de outubro e não utilizada" |
| Notas recebidas (cap 15) | Auto Peças Vale Forte, NF-e nº 2157 de 05/11, "SUCATA DE BATERIA AUTOMOTIVA" 640 kg × R$ 3,10 = R$ 1.984,00 (a compra de 05/11, Pix da Conta Secundária); Depósito Irmãos Siqueira, nº 884 de 06/11, "FERRO PESADO" 1.200 kg × R$ 0,95, "FERRO MISTO" 320 kg × R$ 0,75 e "COBRE MISTO" 20 kg × R$ 36,00 = R$ 2.100,00 (a compra no saldo do T4). As duas "Autorizada", manifestação "Ciência", com XML |
| XML importado (cap 23; 1.60.39 pelo "Importar XML", entra em `inbound_nfe` com `origem` "manual" e sem número nem série, como a edge real) | `NFe-3871-Cooperativa-Recomeco.xml`: Cooperativa Recomeço (CNPJ da semente), nº 3871 de 09/11, "ALUMINIO LATINHA" 850 KG × 6,20 e "PLASTICO PET PRENSADO" 1.200 KG × 1,90 = R$ 7.550,00 (dá "alta" e "confira" pela regra do inventário 13) |

**Mundo novo do 1.60.10 (JUNCAO_160, seção 6):**

| Item | Valores (fictícios) |
|---|---|
| Certificado no 1.60 | o estado vem da RPC `fiscal_onboarding_status`, que lê `company_fiscal_config.fiscal_certificate_status`: `missing` na `inicio`, `valid` depois do envio (o handler `plugnotas-upload-certificate` grava) |
| Metalúrgica Pinhal Ltda (cap 14) | na `inicio`: CNPJ **91.647.382/0001-03**, Rua das Oficinas, 820, Parque Industrial, Taubaté/SP, **sem CEP e sem IE**; o cache da consulta de IE (`cnpj_registros_estaduais`) traz a inscrição **688204776112** ativa em SP (nada sai da máquina). Na aula: CEP 12086-410 e a IE gravados; nada é emitido |
| 1250 (cap 11) | a prazo, "Boleto (15)", 2 duplicatas de R$ 11.975,00 (10/12/2026 e 09/01/2027), xPed 4500123456, "Carga conferida na balança do pátio em 10/11/2026.", volumes 1 / Granel / 506 / 500 kg |
| 1252 (cap 15) | semente `rejeitada-1252`: Serra Fina, Alumínio perfil **150 kg × R$ 10,40 = R$ 1.560,00**, rejeitada com "Rejeição 778: Informado NCM inexistente [nItem:1]" (NCM 7602.00.99 no item) e os eventos do Histórico; corrigida para 7602.00.00 e autorizada com o mesmo número |
| 1253 (cap 17) | entrada, "Devolução de venda", CFOP 1202, referência à 1250, Cobre mel **40 kg × R$ 47,90 = R$ 1.916,00**, item na origem 1 (digitado: a 1250 do mundo não guarda o número do item). Só a nota |
| 1254 (cap 18) | "Complementar de venda", referência à 1250, Cobre mel **500 kg × R$ 0,50 = R$ 250,00**; CFOP e imposto os que a tela propõe |
| Fim da aula | notas 1249 (cancelada) a 1254; próxima livre **1255** (T17) |

**Fica para as próximas:** as três notas (1249 cancelada, 1250 com CC-e, 1251), a série em 1251, a transportadora, o
cenário, Notas Recebidas ligado com as três notas (a da Auto Peças confirmada). O T17 parte daqui (MDF-e da carga da 1250,
NFS-e, pacote do contador). Atualizar o `MUNDO_FICTICIO.md`.

## Gravação

- Rotas: `/dashboard` (entrada pelo menu), `/fiscal-ambiental/nfe/entrada`, `/saida`, `/recebidas`, `/inutilizadas`,
  `/fiscal-ambiental/configuracao/certificado`, `/empresa`, `/impostos`, `/cenarios`, `/numeracao`, `/transportadora`,
  `/servicos`.
- Edge functions a simular (todas fiéis ao formato do código): `plugnotas-upload-certificate` (sucesso, `vaultStored`
  true), `plugnotas-certificate-info`, `plugnotas-register-company` ("Empresa cadastrada no sistema de NF-e!"),
  `ibge-cities` (só se faltar IBGE), `plugnotas-emit` (sucesso com `plugnotasId`), `plugnotas-status` (troca para
  `emitida` em ~5 s, com chave, protocolo e `authorized_at`), `plugnotas-cancel` (`confirmed` true), `plugnotas-cce`
  (envio e status `CONCLUIDO`), `plugnotas-inutilize` (sucesso; grava `nfe_inutilized_numbers`), `plugnotas-download`
  (PDF de DANFE fictício com os dados da nota, XML da nota e XML de cancelamento; **a cena do papel usa a DANFE de exemplo do Kaik,
  pendente**), `plugnotas-enable-dfe`,
  `plugnotas-dfe-sync`, `plugnotas-manifestar` (sem fila: "Operação confirmada junto à SEFAZ"); **1.60.39:** `inbound-xml-import`
  (o "Importar XML", handler novo em 28/11).
- RPCs/tabelas: **1.60.39:** `list_fiscal_document_history` (o Histórico, handler novo em 28/11) e `get_invoices_paged` com
  `p_fiscal_config_ids` (filtro do emitente, só com mais de um CNPJ); `certificate_vault_status`, `count_fiscal_documents_in_month` (0 no cap 08), `get_invoices_paged` (inclui
  as inutilizadas de `nfe_inutilized_numbers` com `p_include_inutilizadas`), `dfe_inbound_import_enqueue` e a fila de jobs
  do import (fica "succeeded" em ~3 s), `company_fiscal_config`, `fiscal_scenarios`, `nfe_series`, `transportadoras`,
  `invoices`, `invoice_items`, `invoice_orders`, `nfe_module_tiers`, notas recebidas (`useInboundNfe`).
- Arquivos para o seletor de arquivo (o robô preenche o `input type=file`, sem janela do sistema): o `.pfx` falso e o XML
  da Cooperativa (XML de NF-e válido no esquema, dados fictícios).
- "Download DANFE" abre aba nova com o PDF: gravar a aba (como o comprovante em PDF do T7) ou cortar para ela.
  "Download XML" baixa arquivo: a câmera fica na tela do app.
- Sem celular, sem página pública, sem outro usuário. Sem cena de Windows.
- **Ilustrações** (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`; objetos genéricos, sem logo de terceiros, sem
  imitar tela do app): 00 carga e nota; 01 entrada × saída; 02 o certificado assina, passos 1-2-3; 03 régua de um ano; 04 o
  padrão em toda nota; 05 geral × estreita; 06 a sequência continua; 07 o caminhão na nota; 08 a barra da cota; 09 o caminho
  da nota (base: os 4 passos de `EmissionFlowTimeline.tsx`); 10 bruto, desconto, líquido; 11 várias compras, uma nota; 12
  cancelar × corrigir; 13 números com cadeado; 14 DANFE e XML; 15 a nota chega pela SEFAZ; 16 as respostas; 17 o
  casamento. Detalhe de cada uma na coluna Tela do roteiro.

## Pronúncias
- Da tabela do PERFIL (versão de 10/11 01:20): NF-e e ICMS em IPA (`/ˈẽniˈɛfiˈe/`, `/iˈseˈɛmiˈɛːsːi/`), NFS-e em IPA
  provisório (`/ˈẽːniˈɛːfiˈɛːsiˈeː/`, teste 8 do Kaik), SEFAZ "sefás", CFOP "cê-éfe-ó-pê", DANFE "dânfi", NCM, XML, PDF,
  MTR, CDF, DRE e EcoSistema como na tabela. Se o PERFIL mudar de novo, é só rodar o gerador outra vez: ele lê a config
  do perfil.
- Novas desta aula (testar num trecho curto antes da voz): **CC-e** "cê-cê-ê", **A1** "á-um", **pfx** "pê-éfe-xis"
  (dito "ponto pfx"), **IBS** "i-bê-ésse", **CBS** "cê-bê-ésse", **Fiscal & Ambiental** "Fiscal e Ambiental".
- Ditas por extenso, sem troca: PIS, COFINS, CNPJ, PET. Evitadas na fala: MDF-e (vira "manifesto de transporte"), DF-e,
  cClassTrib, RNTC, CST.
- Gerador: `T16_gera_tts.py` (na pasta T16 do scratchpad) lê o `roteiro.md` e a config do perfil (só leitura) e escreve
  `narracao/tts_textos.py` e `narracao/config_narracao.json` (37 trocas, 28 números para a legenda).

## Riscos e decisões para o Kaik
1. **Cancelar a 1249** (a Serra Fina mudou o pedido antes de a carga sair) e **CC-e da placa na 1250**: os dois são casos
   comuns e não encenam erro do sistema. Alternativa: cancelar uma nota extra criada só para isso.
2. **Inutilizar 1246 e 1247** (puladas em outubro, por um acerto errado do último número da série): é o único caso de inutilização que não
   exige encenar uma recusa na gravação. Alternativa: semear uma nota "Rejeitada" e usar "Inutilizar Rejeitadas".
3. **Cenário da Fundição com CST 51 e diferimento 100**: valores "do contador", sem explicação na fala. Alternativa:
   cenário só com texto nas informações complementares.
4. **IBS/CBS preenchido com 000 / 000001** (o exemplo da própria tela): sem falar de datas nem de obrigatoriedade.
5. **"Conferir na tela de compra" não é clicado** no cap 17 (a tela de Compra pede caixa aberto, assunto do T7): a fala diz
   o que o botão faz, com o texto da própria dica.
6. "Cancelado continua contando na cota" vem da fonte; a RPC não está na cópia (inventário 14.3).
7. **(28/11) DANFE de exemplo do Kaik** nas cenas do papel (cap20 e cap24, `cenas/ilustracoes.json`, pendente): é de homologação
   ("SEM VALOR FISCAL") e a nota da aula é de produção e autorizada. Conferir ao receber: modelo de antes de 01/12/2026 (sem IBS/CBS) e o
   destinatário escrito como "Fundição Bandeira do Vale Ltda". Alternativa: usar só num trecho com a marca coberta.
8. **(28/11) Importar XML × Importar nota**: o 1.60.39 deixa os dois botões na mesma tela. A aula ensina o "Importar XML" (o que o
   changelog anuncia) e só cita o "Importar nota" para a chave de acesso.
