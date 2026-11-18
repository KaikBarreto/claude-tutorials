# T16 · Cobertura no EcoSistema 1.60.10 (auditoria de 18/11/2026, só leitura de código)

Base: roteiro gravado na 1.59.154 (`f37573ea0`) contra o 1.60.10 (`5290be4cd`, `/dev/shm/ecoflix-src`). Caminhos relativos a
`src/`; as linhas são do 1.60.10. A varredura do robô (`rec/varredura/t16.txt`) ainda não existe: tudo aqui saiu do código e
precisa ser confirmado na tela quando o robô rodar. Não mudaram desde a 1.59.154 (o inventário continua valendo):
`CancelarNotaDialog`, `CartaCorrecaoDialog`, `InutilizarNumeracaoDialog`, `InvoiceTypeSelector`, `ImportarPedidoModal`,
`ImportarPedidosCaixaModal`, `ImportInboundNfeDialog`, `ImportNfeXmlDialog`, `TransportadoraTab`, `EmpresaSection`,
`QuotaLimitBanner`, `useNfeTier`.

## 1. Mudou no app (por capítulo)

| # | Cap. | O que o roteiro mostra | Como está no 1.60.10 (texto exato) | Arquivo:linha |
|---|---|---|---|---|
| M1 | 01 | Submenu com 5 telas fiscais (mais o SPED) | Entrou a 6ª tela, **"Relatórios Fiscais"**, depois de "Estoque Fiscal". A fala "as notas de mercadoria, as de serviço, o transporte, o ambiental e o estoque fiscal" fica sem um item que aparece no zoom | `config/routes.ts:511` |
| M2 | 02 | Trilho à esquerda com grupos e "precisa do certificado digital" | Continua como as `propostas_fala.md` já dizem: abas no alto (`desktopVariant="underline"`), sem grupos; o motivo da trava só existe como dica do navegador. As duas falas propostas para o cap02 seguem valendo | `pages/ConfiguracaoFiscal.tsx:1225`, `:933` |
| M3 | 02, 03 | Aviso "Passo 1 de 3: Configure primeiro o certificado digital." | Saiu. Agora é uma linha com o número **1** num círculo e **"Certificado digital · primeira etapa da configuração fiscal"**. Empresa e Impostos **continuam** com "Passo 2 de 3:" e "Passo 3 de 3:" (`EmpresaSection.tsx:264`, `ImpostosTab.tsx:316`), então o zoom do cap02 em "Passo 1 de 3" não existe mais | `components/notas-fiscais/CertificadoSection.tsx:336-338` |
| M4 | 03 | Subtítulo "Necessário para assinar e transmitir notas fiscais" | **"Use o certificado A1 do CNPJ para assinar e transmitir notas fiscais."** | `CertificadoSection.tsx:351` |
| M5 | 03 | Caixa "Certificado não configurado" | Linha **"Certificado não configurado. Envie o A1 para continuar."** | `CertificadoSection.tsx:419` |
| M6 | 03 | Rótulo "Arquivo do Certificado (.pfx ou .p12)" e botão "Selecionar arquivo" | Sumiram. Agora é uma **área de arrastar**: **"Arraste o certificado ou clique para selecionar"** / "Arquivo .pfx ou .p12 · até 200 KB" (arrastando: "Solte o certificado aqui"). Com o arquivo: nome do arquivo, **"Arquivo selecionado · clique ou arraste outro para trocar"** e o botão **"Remover"** | `CertificadoSection.tsx:425-487` |
| M7 | 03 | Senha e botão sempre visíveis; botão "Validar Certificado" | O campo "Senha do Certificado" e o botão **só aparecem depois de escolher o arquivo**. O botão virou **"Validar e salvar A1"** ("Validando..."). A senha ganhou o olho "Mostrar senha" / "Ocultar senha". A fala "Clico em Validar Certificado" precisa trocar | `CertificadoSection.tsx:490-542` |
| M8 | 03 | Depois de validar: "Configure os dados da empresa" | **"Complete os dados fiscais da empresa"** (e, com a empresa pronta, **"Empresa pronta para emitir"** no lugar de "Empresa habilitada para NF-e"). "Certificado validado!", "Próximo: Configurar Empresa" e "Substituir Certificado" não mudaram | `CertificadoSection.tsx:372-387` |
| M9 | 06 | "Série padrão" como campo de número já com 1, antes de cadastrar a série; ajuda "Pode digitar uma série que ainda não está cadastrada..." | Virou **lista** que só oferece séries cadastradas. Sem série nenhuma, a lista fica travada com **"Adicione uma série primeiro"** e a chave "Entrada e saída usam a mesma série" também fica travada. Ajuda nova: **"A série padrão precisa estar cadastrada em “Suas séries”."** Se o padrão salvo não está cadastrado, aparece o aviso âmbar **"Série 1 está definida como padrão, mas não foi cadastrada. Escolha uma série cadastrada ou adicione a série correta em “Suas séries”."** O capítulo precisa **inverter a ordem**: primeiro "Adicionar série", depois o zoom na série padrão | `SeriesNumeracaoTab.tsx:76-98`, `:128-151`, `:182` |
| M10 | 09, 10, 11 | A nota abre como janela (modal) com o título do tipo | Abre em **tela cheia**: botão **"Sair"** no alto à esquerda (não há X), título **"Nova NF-e de Saída"** / "Nova NF-e de Entrada", subtítulo **"Preencha os dados, adicione os itens e confira a nota antes de emitir."** e, à direita, **"Número previsto" "Nº 1249" "Série 1"** e o seletor **"Ambiente"** ("Produção" / "Homologação"). Os blocos "Quem emite", "Para quem", "O que é" e "Numeração" ficaram em duas colunas, com título grande | `NovaNotaModal.tsx:8759-8816`, `:5943-6614` |
| M11 | 09 | Linha "Adicionar item" com Material, NCM, CFOP, Qtd, Vl. Unit., Desconto, Vl. Total e "Incluir" | Virou um **cartão** (o mesmo do celular): **"Material"** (campo "Escreva o nome ou código do material"), **"CFOP"**, **"NCM"**, unidade ("KG"), **"Qtd"**, **"Valor"** (não mais "Vl. Unit."), botão **"Desconto"**, **"Total líquido:"** e **"Incluir"**. O zoom do roteiro em `"Vl. Unit." 10,40` muda para `"Valor" 10,40` | `MobileInvoiceInputCard.tsx:197-343`, `NovaNotaModal.tsx:6929-6962` |
| M12 | 09, 10, 11 | Tabela de itens com CFOP e Desconto em colunas; "Vl. Total" | Lista **"Itens adicionados"** com contador e as colunas **"Material", "NCM", "Qtd", "Vl. Unit.", "Total"**. CFOP e desconto saíram da linha: cada item abre os **detalhes** (seta "Mostrar detalhes do item" ou clique na linha) com **"CFOP do item"** (e a origem: "Natureza da operação", "Cenário: <nome>" ou "Manual"; link **"Usar CFOP automático"**) e **"Desconto do item"** ("Adicionar desconto" / "Alterar desconto"). CFOP com problema abre os detalhes sozinho, com "Revise o CFOP nos detalhes". O zoom do cap10 em `"Qtd" 500` continua possível; a coluna do total chama "Total" | `NovaNotaModal.tsx:7026-7399` |
| M13 | 09 | Passo Itens só com a tabela | Acima da lista há o botão **"Desconto geral"** ("Desconto geral da nota": "Esse desconto abate o total da nota inteira. ...") | `NovaNotaModal.tsx:6756-6810` |
| M14 | 09, 10, 11 | Lista piscava para "carregando" a cada consulta de status | A lista não troca mais pela tela de carregamento durante a atualização automática (nota 1.60.4). Só afeta a gravação: a espera do "Aguardando SEFAZ" fica mais limpa | `config/version.ts:41` |
| M15 | 11 | (não mostrado) aviso grande "Quem compra de empresa não emite a nota" na entrada com fornecedor CNPJ | Virou uma linha âmbar curta: **"Em compras entre empresas, o mais comum é o fornecedor emitir a NF-e de saída. Se necessário, você pode continuar e emitir esta NF-e de entrada."** com um "?" de ajuda. Não aparece no cap11 (consumidor final), mas aparece em qualquer entrada contra CNPJ | `NovaNotaModal.tsx:6217-6238` |
| M16 | 09 | Aba "Pré-visualização" (não mostrada) | Agora é um DANFE em preto e branco com a marca-d'água **"SEM VALOR FISCAL"**, canhoto, "Código de barras gerado após a emissão", "Chave de acesso / Gerada após a emissão" e "Protocolo de autorização de uso / Gerado após a emissão" | `DanfePreview.tsx:222-300` |
| M17 | 12, 13, 14 | Menu dos três pontinhos e ações de emissor sempre visíveis | Sem a permissão de emitir (`action_emit_nfe`), somem "Nova Nota", "Continuar preenchendo", "Emitir NF-e", reenviar, "Inutilizar numeração", "Carta de Correção", "Gerar nota complementar" e "Cancelar"; quem só tem Exportação Contábil vê só os três pontinhos com esse item. Rafael é MASTER: nada muda na gravação | `NotaFiscalTable.tsx:255-282`, `pages/NotasFiscais.tsx:2132-2209` |
| M18 | 15 | Faixa verde "Certificado A1 pronto para a consulta direta na SEFAZ." (não estava no roteiro, mas podia aparecer) | Saiu. Só aparece a faixa vermelha quando falta o certificado (botão "Enviar certificado") | `notas-recebidas/NotasRecebidasTab.tsx:1739-1759` |

Achado que continua: `IbsCbsReformaBanner.tsx` segue sem uso em tela nenhuma (o aviso de datas da Reforma não aparece). E a aba
Opções ainda diz "Adicione itens na aba Dados & Itens" (`NovaNotaModal.tsx:8186`), nome de aba que não existe: não ler em voz.

## 2. Falta cobrir (o 1.60.10 tem e o roteiro não mostra)

### 2.1 Emissão (tela da nota)
| # | O que é | Quando o cliente usa | Vale? |
|---|---|---|---|
| F1 | **Aba "Impostos"**: "Cenário fiscal aplicado:", o valor aproximado de tributos ("Lei 12.741/2012"), "Base de Cálculo", lista "Tributos desta nota" (ICMS, FCP, PIS, COFINS, IPI), botão **"Ajustar impostos desta nota"** ("CST e alíquota valem só nesta nota"), totais "Produtos", "Frete", "Outras Despesas", "Total da Nota" (`TaxCalculationPreview.tsx:936-1864`) | Conferir o imposto antes de emitir; trocar CST ou alíquota de uma nota só, a pedido do contador | **Sim, capítulo** (N1). É o coração do Lucro Real |
| F2 | **IBS/CBS na nota**: chave "Calcular IBS e CBS automaticamente" na aba Impostos da nota ("O sistema fiscal calculará automaticamente os novos tributos IBS e CBS nesta nota."), bloco "IBS e CBS (Reforma Tributária)" com a base "(valor dos itens, não a base do ICMS)" e "Será calculado na emissão, pela calculadora da SEFAZ.", que "não é imposto zero" e fica fora do valor aproximado de tributos; ajuste "IBS / CBS (Reforma)" (CST e cClassTrib) (`NovaNotaModal.tsx:7871-7885`, `TaxCalculationPreview.tsx:1575-1846`) | Toda nota desde a Reforma | **Sim, dentro do N1** |
| F3 | **DANFE novo**: letra sem serifa, títulos de seção, e o modelo com IBS, CBS e Imposto Seletivo "a partir de 1º de dezembro", trocado pela data de emissão (`config/version.ts:99-100`) | Quem estranhar o papel diferente | **Sim, trecho** no cap14 |
| F4 | **Aba "Faturamento"** ("Cobrança / Faturamento"): "À vista" / "A prazo"; "Forma de pagamento (fiscal)" (Dinheiro (01), PIX (17), Transferência (18), Outros (99); a prazo: Duplicata Mercantil (14), Boleto (15), Outros (99)); "Condição de pagamento" ("Manual (definir parcelas)" ou uma condição cadastrada); "Duplicatas / Parcelas" com "Adicionar parcela"; trava "A soma das parcelas precisa bater com o total da nota para emitir." Some em devolução e baixa por perda (`NovaNotaModal.tsx:7903-8100`, `:5447`) | Venda a prazo com boleto ou duplicata no DANFE | **Sim, dentro do N1** |
| F5 | **Aba "Transporte"** completa: "Modalidade do Frete", transportadora "Preencher manualmente" e o "+" ("Criar transportadora"), "Valor do Frete", "Outras Despesas", "Volumes Transportados" (Quantidade, Espécie, Marca, Peso Bruto (kg), Peso Líquido (kg)); aviso "Frete sem ocorrência de transporte não permite informar transportador/veículo." (`:7681-7823`) | Carga com frete cobrado na nota; peso no DANFE | **Sim, trecho** no cap10 (hoje só escolhe a transportadora) |
| F6 | **Aba "Opções"**: "Pedido de compra do cliente", "Nº do pedido (xPed)" (ex.: 4500123456), item do pedido por produto (`:8113-8190`) | Indústria que exige o número do pedido dela na nota | **Sim, dentro do N1** (uma frase) |
| F7 | **"Informações Adicionais"** no passo Itens: "Informações complementares" e "Reservado ao Fisco", cada um com "Somar aos textos herdados" ou "Substituir nesta nota" (`:7533-7660`) | Texto que o contador pede numa nota específica | **Sim, dentro do N1** |
| F8 | **Aba "Pré-visualização"** (M16) com "Pendências para emissão" clicáveis (`:8196-8520`) | Conferir a nota inteira antes de enviar | **Sim, dentro do N1** |
| F9 | **Pendências**: selo vermelho "N pendência(s) pra emitir" com a lista, e os textos: "Selecione um cliente", "Cliente com dados fiscais incompletos", "CEP do cliente incompleto: precisa ter 8 dígitos. ...", "Inscrição Estadual (IE) do emitente não configurada. Preencha nas Configurações Fiscais.", "Adicione pelo menos um item", "N item(ns) sem NCM", "N item(ns) com NCM inválido (informe 8 dígitos)", "N item(ns) sem quantidade", "N item(ns) com CFOP incompatível com o tipo ou destino da operação", "CNPJ/CPF da transportadora ... é inválido" (`:4366-4518`); atalhos "Completar cadastro" / "Completar os dados do destinatário" (`:6176-6189`) | Toda vez que o "Emitir Nota" está travado | **Sim, capítulo** (N2) |
| F10 | **Trava da inscrição estadual (rejeição 232)**: venda dentro do estado para CNPJ sem IE. Sem prova, só o aviso "Este cliente é empresa (CNPJ) e está sem inscrição estadual. ... Se for isento mesmo, pode seguir e emitir."; quando a consulta acha a IE ativa, **trava** e oferece o botão **"Usar IE <número> e salvar no cadastro"** (toast "IE <número> salva no cadastro") (`avisoIeDestinatario.ts:72-76`, `:207-215`; `NovaNotaModal.tsx:3050-3092`) | Cliente novo cadastrado sem IE | **Sim, dentro do N2** |
| F11 | **Nota rejeitada**: selo "Rejeitada"; em Visualizar, faixa vermelha **"Nota rejeitada pela SEFAZ"** com "Cód. NNN", o texto "A SEFAZ recusou a nota:" / "O que fazer:", o plano de ação e "Após corrigir, você pode tentar novamente."; menu **"Editar e reenviar (mesmo número)"**, **"Editar e reemitir com novo número (#N)"**, "Inutilizar numeração"; título "Reemitir NF-e de Saída" e "Esta nota será reemitida como Série 1 / Nº N". Dicas por código em `utils/sefazError.ts:61-100`: 203 e 781 (CNPJ não habilitado), 232 e 234 (IE do cliente), 778 (NCM inexistente), 280 a 286 e 290 a 296 (certificado), 321 (devolução sem item de origem), 501 (prazo de cancelamento), 217, 720 (`NotaFiscalPreview.tsx:832-898`, `NotaFiscalTable.tsx:360-390`, `NovaNotaModal.tsx:6726`, `:8780`) | Sempre que a SEFAZ recusa | **Sim, capítulo** (N3). É o pedido direto do Kaik |
| F12 | Nota recusada não trava mais as seguintes; avisos sem nome interno; espera do bloqueio temporário da SEFAZ também em cancelamento e carta de correção (`version.ts:87`, `:102-104`) | Segurança de quem emite várias seguidas | **Só citar** no N3 |
| F13 | **Devolução**: naturezas "Devolução de venda" (entrada, CFOP 1202 / 2202) e "Devolução de compra" (saída, 5202 / 6202); campo **"Chave da NF-e original (devolução)"**, botão **"Selecionar nota do sistema"** (abre "Importar NF-e de Saída para Devolução", busca "Buscar por número, cliente ou chave..."), "Vincula esta nota à original na SEFAZ. Obrigatória para emitir."; no passo Itens, bloco **"Nota de origem de cada item"** com "Origem: <chave>" e o campo "item na origem", e o aviso "Informe o número do item na nota de origem"; sem aba Faturamento; sem "Consumidor Final" (`NovaNotaModal.tsx:849-861`, `:6524-6576`, `:7421-7526`; `ImportarNfeSaidaModal.tsx:215-225`) | Cliente devolve carga, ou a empresa devolve compra | **Sim, capítulo** (N4) |
| F14 | **Nota complementar**: menu da nota autorizada **"Gerar nota complementar"** (também em Visualizar); abre a nota com a natureza "Complementar de venda" / "Complementar de compra", **"Chave da NF-e original (complementar)"** preenchida e a opção **"Contar esta nota no Estoque Fiscal"** ("Marque só se este complemento for de PESO/QUANTIDADE. ..."); erro "Só é possível gerar nota complementar a partir de uma nota autorizada pela SEFAZ" (`NotaFiscalTable.tsx:478`, `pages/NotasFiscais.tsx:1323-1353`, `NovaNotaModal.tsx:6584-6604`) | Preço ou imposto saiu a menor na nota original | **Sim, capítulo** (N5) |
| F15 | **Rascunho**: "Salvar Rascunho", selo "Rascunho", menu "Continuar preenchendo" e "Excluir"; ao sair com dados, "Descartar nota fiscal?" (`:8595`, `:8831-8840`; `NotaFiscalTable.tsx:354`) | Nota começada e interrompida | **Sim, trecho** no cap09 |
| F16 | **"Ambiente"** no cabeçalho da nota ("Produção" / "Homologação") e as abas "Produção" / "Homologação" da lista (`:8798-8813`) | Nota de teste, sem valor fiscal | **Sim, trecho** curto no cap09 (avisar para não emitir venda de verdade em Homologação) |
| F17 | **Data e hora da emissão** retroativa, com "Limpar" ("Voltar para a data e hora atuais") (`:6686-6743`) | Nota de carga que saiu horas antes | **Só citar** no cap09 (a fala "a data em branco é agora" já existe) |
| F18 | **Outras naturezas**: saída "Venda de produção própria", "Remessa para conserto", "Remessa para demonstração", "Remessa para fins de exportação", "Transferência de mercadorias", **"Baixa de estoque por perda"** (CFOP 5927, nota contra a própria empresa, opção "Dar baixa no estoque físico ao autorizar"); entrada "Compra de matéria-prima", "Entrada de bonificação, doação ou brinde", "Retorno de remessa"; e **"Outra operação"** (texto livre, "Ex.: Remessa para industrialização", até 60 caracteres) (`lib/nfe/natureOperations.ts:1-22`; `NovaNotaModal.tsx:817-838`, `:6356-6365`, `:6483-6503`) | Operação que não é venda nem compra | **Sim, trecho** (N6, curto): mostrar a lista e a baixa por perda |
| F19 | **Destinatário avulso**: "Preencher manualmente" na busca do cliente, com "Editar" e "Remover" (`:6124-6156`) | Cliente de uma venda só | **Só citar** no N2 |
| F20 | Regime do parceiro e cenários: aviso "Você tem cenários fiscais que só valem para um regime específico. Enquanto ... em branco, esses cenários não se aplicam a esta nota ..." (`:6280-6283`) | Quem criou cenário por regime | **Não**: o cenário da aula é por CNPJ; fica para dúvida de suporte |
| F21 | **"Quem emite"** vira seletor ("Escolha o CNPJ que vai emitir") e o cabeçalho mostra "Emitindo por" quando a empresa tem mais de um CNPJ (`:5957-6009`, `:8659-8674`) | Empresa com filial | **Só citar** (uma frase no cap09); o mundo fictício tem um CNPJ só |
| F22 | **NF-e pelo Cato** ("Prepare a NF-e de um pedido pelo Cato", `version.ts:56`) | Emitir pela conversa | **Outra aula**: a do Cato. Aqui, uma frase no resumo |

### 2.2 Lista, visualização e eventos
| # | O que é | Quando usa | Vale? |
|---|---|---|---|
| F23 | Filtro "Status" (Autorizada, Pendente, Aguardando SEFAZ, Rejeitada, Cancelada, Cancelamento Pendente, Rascunho), ordenação (Data, Número), busca e período (`pages/NotasFiscais.tsx:1733-1799`) | Achar uma nota antiga | **Sim, trecho** no cap14 |
| F24 | Menu "Consultar status" na nota que ficou em "Aguardando SEFAZ" (`NotaFiscalTable.tsx:422`) | Autorização que demora | **Sim, uma frase** no cap09 |
| F25 | **"Histórico"** ("Histórico da NF-e": eventos com "Sucesso", "Erro", "Enviado", "Aviso" e o protocolo) (`NotaFiscalHistorico.tsx:72-179`) | Saber o que aconteceu com a nota e quando | **Sim, trecho** no N3 |
| F26 | "Comprovante (Notinha)" da nota autorizada (`NotaFiscalTable.tsx:450`) | Entregar um resumo em papel térmico | **Só citar** no cap14 (o zoom já passa por ele) |
| F27 | Detalhe da linha (Participante, Identificação com "Chave NF-e:", Valores, "Situação e emissão", "Observações e ocorrências") | Conferir sem abrir a nota | **Só citar** no cap14 |
| F28 | **Cancelamento fora do prazo**: "Fora do prazo normal de 24h" (a SEFAZ ainda aceita até 480 horas, 20 dias), e depois disso o aviso de que o caminho é devolução; selo "Cancelando…"; dica do código 501 (`i18n/locales/pt-BR/invoices.json:10-13`) | Erro percebido dias depois | **Sim, trecho** no cap12 (hoje é uma frase) |
| F29 | Cancelamento e devolução acertam o Estoque Fiscal sozinhos (`version.ts:34`) | Quem acompanha o saldo fiscal | **Outra aula**: T17 (Estoque Fiscal). Não repetir |
| F30 | **Carta de correção depois de enviada**: "1 CC-e enviada", "PDF", "XML", "✅ Registrada na SEFAZ · protocolo ...", limite de 20 por nota, mínimo de 15 caracteres (inventário, seção 9) | Entregar a carta ao cliente ou à transportadora | **Sim, trecho** no cap12 |
| F31 | **Inutilizar a partir da nota** (menu "Inutilizar numeração" na rejeitada e no rascunho com número) e a aba "Inutilizar Rejeitadas" de verdade: "Marcar todos", "Confirmar inutilização em lote?", "Sim, inutilizar", "Nenhuma nota rejeitada nessa empresa." (`NotaFiscalTable.tsx:413`, `InutilizarNumeracaoDialog.tsx:590-760`) | Nota rejeitada que não vai ser reenviada | **Sim, trecho** no N3 (fecha o assunto da rejeitada) e uma frase no cap13 |
| F32 | Prazo de inutilização "até dia 10 do mês seguinte ao pulo" (está no aviso, o roteiro não lê) | Todo mês | **Sim, uma frase** no cap13 |

### 2.3 Configuração fiscal
| # | O que é | Quando usa | Vale? |
|---|---|---|---|
| F33 | **Certificado vencido ou com problema**: "Seu certificado A1 venceu" / "Envie o certificado renovado (.pfx ou .p12) para voltar a emitir e consultar documentos fiscais."; "O certificado precisa ser corrigido"; senha errada ("Senha do certificado incorreta. Confira a senha exata do arquivo .pfx/.p12 e tente novamente."); arquivo acima de 200 KB (`CertificadoSection.tsx:146-196`) | Renovação anual | **Sim, trecho** no cap03 (renovar é o caso de uso mais comum depois do primeiro envio) |
| F34 | Empresa: "Responsável técnico (CSRT)" e "Logo para Nota Fiscal" (o logo agora fica guardado no sistema, `version.ts:101`) | Logo no DANFE; CSRT quando o estado exige | **Sim, uma frase** no cap04 para o logo; CSRT só citar ("o contador avisa se o seu estado pede") |
| F35 | Impostos: blocos "PIS / COFINS" (CST de saída e entrada), "IPI", diferimento automático para indústria do mesmo estado ("100% = totalmente diferido (zero no DANFE)"), "Informações Complementares Padrão", "Reservado ao Fisco (padrão)", "Código de Benefício Fiscal (cBenef)" (`ImpostosTab.tsx:598-1060`) | Configuração do Lucro Real com o contador | **Sim, trecho** no cap04: hoje a câmera pula do ICMS para o CFOP |
| F36 | Aviso novo **"Este tipo de ICMS ainda não pode ser emitido por aqui"** ao escolher CST de substituição tributária (só para algumas empresas) (`CstSemEmissaoAviso.tsx:44-50`, `version.ts:88`) | Raro | **Só citar** no cap04 ("se a tela avisar que um código ainda não sai em nota, fale com o suporte antes de emitir") |
| F37 | IBS/CBS na configuração: "é obrigatório informar pelo menos um par completo (CST-IBS/CBS + cClassTrib) de Saída e/ou Entrada" (`ImpostosTab.tsx:1241`) | Ao ligar a Reforma | **Sim, uma frase** no cap04 |
| F38 | Cenários: demais condições (material por NCM, posição ou grupo; regime do parceiro; destino; inscrição estadual; tipo de parceiro), CFOP por cenário, e a aba "Cenários" com "sem revisão" | Exceções por material ou destino | **Só citar** no cap05: um segundo exemplo falado, sem cadastrar |
| F39 | Numeração: séries diferentes para entrada e saída ("Série padrão pra ENTRADA" / "Série padrão pra SAÍDA"), editar e excluir série (`SeriesNumeracaoTab.tsx:161-170`) | Quem separa entrada e saída | **Sim, uma frase** no cap06 |
| F40 | Permissões de emitir, manifestar e exportar (M17) | Equipe com papéis | **Outra aula**: usuários e permissões. Uma frase no cap01 |
| F41 | **Relatórios Fiscais › NF-e** (M1; antes era "Relatório fiscal" dentro do Estoque Fiscal) | Resumo do mês | **Outra aula**: T17. Precisa confirmar que a T17 cobre (ver Decisões) |

## 3. Proposta

Tom da aula mantido. Onde a fala cita imposto, ela não inventa valor: lê o que a tela mostrar na gravação (marcado
`[CONFERIR NA TELA]`), porque o cálculo do Lucro Real depende do cenário e da base, e o robô ainda não rodou.

### 3.1 Ajustes nos capítulos que já existem

| Cap. | Tela | Fala (nova ou trocada) |
|---|---|---|
| 01 | Zoom no submenu, agora com "Relatórios Fiscais" no fim. | Aqui ficam as telas fiscais: as notas de mercadoria, as de serviço, o transporte, o ambiental, o estoque fiscal e os relatórios fiscais. Hoje a gente fica nas notas de mercadoria. |
| 01 | (fim do capítulo, câmera em "Nova Nota") | Um detalhe: o botão Nova Nota só aparece pra quem tem permissão de emitir. Quem só exporta pro contador não vê. |
| 02 | Zoom na linha "1 Certificado digital · primeira etapa da configuração fiscal" (troca o zoom em "Passo 1 de 3"). | Por isso o certificado é a primeira etapa. Depois vêm os dados da empresa, e por último os impostos. |
| 03 | "Certificado não configurado. Envie o A1 para continuar." e a área "Arraste o certificado ou clique para selecionar" ("Arquivo .pfx ou .p12 · até 200 KB"); o robô entrega o arquivo: aparecem o nome, "Arquivo selecionado · clique ou arraste outro para trocar" e o campo "Senha do Certificado". | É só arrastar o arquivo ponto pfx pra esta área, ou clicar nela e escolher. Escolhido o arquivo, aparece o campo da senha. |
| 03 | Clique em "Validar e salvar A1". | Clico em Validar e salvar A1. Pronto: certificado validado. |
| 03 | [ILUSTRAÇÃO curta: o cartão "A1" com a data riscada e um cartão novo entrando no lugar] e a câmera em "Substituir Certificado". | O A1 vence todo ano. Quando vencer, a tela avisa que o certificado venceu, e é só enviar o arquivo renovado aqui mesmo. Sem isso, nenhuma nota sai. |
| 04 | Em "Empresa", a câmera desce até "Logo para Nota Fiscal". | Mais embaixo dá pra enviar o logo que sai impresso na nota. |
| 04 | Em "Impostos (padrão)", a câmera passa por "PIS / COFINS" (CST de saída e de entrada), "IPI" e pelo diferimento, antes do CFOP. | No Lucro Real, o PIS e a COFINS são não cumulativos, e cada um tem o código da venda e o código da compra. Tem também o IPI, pra quem industrializa, e o diferimento do ICMS. Nada disso se escolhe no chute: é a planilha do contador, campo por campo. |
| 04 | Zoom em "Informações Complementares Padrão" e "Código de Benefício Fiscal (cBenef)". | E o texto que precisa sair em toda nota, como a base legal de um benefício, fica em Informações Complementares Padrão. |
| 04 | No bloco "Reforma Tributária (IBS/CBS)", zoom nos pares de Saída e Entrada. | Ligando a Reforma, a tela exige pelo menos um par completo: o código do IBS e da CBS e a classificação tributária. |
| 05 | (depois de criar o cenário) zoom nas condições "NCM específico", "Destino" e "Regime do parceiro", sem preencher. | O cenário também pode valer por material, pelo NCM, por destino, dentro ou fora do estado, ou pelo regime do cliente. Por exemplo: toda venda de cobre pra fora do estado. |
| 06 | **Ordem invertida**: 1) "Suas séries" → "Adicionar série" (1 e 1248) → "Adicionar"; 2) só então o zoom em "Série padrão" (lista com "Série 1") e na ajuda "A série padrão precisa estar cadastrada em “Suas séries”.". | Primeiro eu cadastro a série, e depois escolho ela como padrão. A série padrão precisa estar na lista de Suas séries. |
| 06 | Desliga e religa "Entrada e saída usam a mesma série" para mostrar "Série padrão pra ENTRADA" e "Série padrão pra SAÍDA". | Quem separa as notas de entrada numa série e as de saída em outra desliga esta chave e escolhe uma série pra cada. |
| 09 | A nota abre em tela cheia: zoom no cabeçalho "Nova NF-e de Saída", "Número previsto Nº 1249 Série 1" e "Ambiente" "Produção". | A nota abre em tela cheia. Em cima já aparecem o número previsto e o ambiente. Produção é a nota de verdade. Homologação é só pra teste, e não vale como nota. |
| 09 | Cartão "Adicionar item": "Material" (digita "alumínio perfil"), "NCM", "Qtd" 320, "Valor" 10,40, "Total líquido:" R$ 3.328,00, "Incluir". | (troca "Vl. Unit." por "Valor" no zoom; a fala do item continua) |
| 09 | Em "Itens adicionados", clique na seta da linha: "CFOP do item" 6102 com "Natureza da operação" e "Desconto do item" "Adicionar desconto". | Cada item tem os seus detalhes. Aqui ficam o CFOP do item, com a origem dele, e o desconto do item. |
| 09 | Câmera em "Salvar Rascunho" (sem clicar). | Se precisar parar no meio, Salvar Rascunho guarda a nota, e depois é Continuar preenchendo, no menu dela. |
| 09 | (na linha "Aguardando SEFAZ") menu → zoom em "Consultar status", sem clicar. | Se a resposta demorar, o Consultar status pergunta de novo pra SEFAZ. |
| 10 | Aba "Transporte": além da transportadora, "Volumes Transportados" com "Quantidade" 1, "Espécie" "Granel", "Peso Bruto (kg)" 506,000 e "Peso Líquido (kg)" 500,000. | Em Volumes vão o peso bruto e o peso líquido da carga, que saem impressos na nota. |
| 12 | Diálogo de cancelamento; [ILUSTRAÇÃO: régua do tempo com "24 horas" em verde, "até 20 dias" em âmbar e, depois, um cadeado com "devolução"]. | O prazo normal de cancelamento é de vinte e quatro horas. Depois disso a SEFAZ ainda costuma aceitar até vinte dias, e a tela mostra a data limite. Passou dos vinte dias, não cancela mais: o caminho é a nota de devolução. |
| 12 | Depois do "Enviar CC-e": a lista "1 CC-e enviada" com "PDF", "XML" e "✅ Registrada na SEFAZ · protocolo ...". | A carta fica na lista, com o PDF pra mandar pro cliente e o protocolo da SEFAZ. Cada nota aceita até vinte cartas, e vale sempre a última. |
| 13 | Zoom no item "Prazo SEFAZ: até dia 10 do mês seguinte ao pulo". | E tem prazo: até o dia dez do mês seguinte. |
| 14 | Zoom no filtro "Status" aberto e na busca. | Pra achar uma nota antiga, tem a busca, o período e o filtro de status: autorizada, rejeitada, cancelada, rascunho. |
| 14 | PDF do DANFE aberto (ilustração do papel). | O DANFE ganhou um visual mais limpo. E a partir de primeiro de dezembro ele passa a sair com os campos do IBS, da CBS e do Imposto Seletivo. A troca é automática, pela data da nota. |

### 3.2 Capítulos novos

**N1 · Conferindo os impostos e as outras abas (vinheta: IMPOSTOS)** · entra depois do cap10, na nota da Fundição (nº 1250),
antes do "Emitir Nota" (o cap10 passa a terminar no passo Itens; o N1 emite).

| Tela | Fala |
|---|---|
| Capítulo novo (semente `apos-cap09`, com o `setup` reabrindo a nota da Fundição já importada do pedido); clique na aba "Impostos": "Cenário fiscal aplicado: Venda para a Fundição Bandeira do Vale". [ZOOM: essa linha] | Antes de emitir, vale conferir o imposto. Na aba Impostos, a primeira linha diz qual cenário fiscal entrou. Aqui, o da Fundição, que a gente criou lá na configuração. |
| A câmera desce por "Base de Cálculo" e pela lista "Tributos desta nota": ICMS (CST 51, diferimento 100 %), PIS e COFINS. [CONFERIR NA TELA os valores] | Embaixo, tributo por tributo. O ICMS veio com o código e o diferimento do cenário. O PIS e a COFINS vieram do padrão do Lucro Real: um vírgula sessenta e cinco e sete vírgula seis por cento. |
| [ILUSTRAÇÃO: Padrão e exceção na mesma nota: a folha da nota com três linhas, "ICMS", "PIS" e "COFINS"; o carimbo "cenário" marca só o ICMS e o carimbo "padrão" marca as outras duas] | É assim que a nota se monta: o cenário muda só o que ele diz, e o resto continua vindo do padrão. |
| Clique em "Ajustar impostos desta nota": abre o painel com os grupos ICMS, PIS, COFINS, IPI e "IBS / CBS (Reforma)"; zoom em "CST e alíquota valem só nesta nota"; fecha sem mudar. | Se o contador pedir um código diferente só nesta nota, tem o botão Ajustar impostos desta nota. O que muda aqui vale só pra ela, e não mexe na configuração. |
| Desce até "Reforma Tributária": "Calcular IBS e CBS automaticamente" ligado e o bloco "IBS e CBS (Reforma Tributária)" com "Será calculado na emissão, pela calculadora da SEFAZ.". [ZOOM: o bloco] | E a Reforma. Com o cálculo ligado, o IBS e a CBS vão na nota. A tela avisa que o valor é calculado na emissão, pela calculadora da SEFAZ. Então, se aparecer sem valor aqui, não quer dizer imposto zero. |
| Clique na aba "Faturamento" ("Cobrança / Faturamento"): marca "A prazo"; "Forma de pagamento (fiscal)" = "Boleto (15)"; "Condição de pagamento" = "Manual (definir parcelas)"; duas parcelas de R$ 11.975,00, com vencimento em 10/12/2026 e 09/01/2027 (trecho acelerado). [ZOOM: as duas parcelas] | Em Faturamento vai como a venda foi combinada. A Fundição paga em duas vezes no boleto: duas parcelas de onze mil novecentos e setenta e cinco reais. A soma tem que bater com o total da nota, senão ela não emite. |
| Clique na aba "Opções": em "Nº do pedido (xPed)" digita 4500123456. | Em Opções vai o número do pedido de compra do cliente, quando a indústria exige isso na nota. |
| Volta ao passo "Itens" e desce a "Informações Adicionais": "Informações complementares" com "Somar aos textos herdados" marcado; digita "Carga conferida na balança do pátio em 10/11/2026.". | E em Informações complementares vai o texto livre desta nota. Dá pra somar ao texto padrão da configuração ou trocar ele só aqui. |
| Clique na aba "Pré-visualização": o DANFE em preto e branco com a marca "SEM VALOR FISCAL"; a câmera passa pelo emitente, pelo destinatário, pelos itens e pelas duplicatas. | Por último, a Pré-visualização. É a nota como ela vai sair, ainda sem valor fiscal. Confiro o cliente, os itens, o imposto e as parcelas. |
| Clique em "Emitir Nota": "Aguardando SEFAZ" e, em ~5 s, toast "Nota #1250 autorizada pela SEFAZ!". | Tudo certo. Emitir Nota. Ela entra como Aguardando SEFAZ e, em instantes, a mil duzentos e cinquenta está autorizada. |

Mundo: a nota 1250 passa a ter `payment` a prazo com duas duplicatas (ajustar `apos-cap10` e o que a T17 lê dela) e o
`purchase_order_number`. Handlers: os mesmos do cap10. Conferir no ensaio se o cenário da Fundição (CST 51, 100 %) aparece
na linha "Cenário fiscal aplicado" com a Fundição cadastrada como contribuinte com IE (senão o motor volta para CST 00).

**N2 · O que trava a emissão (vinheta: EMISSÃO)** · entra depois do N1.

| Tela | Fala |
|---|---|
| Capítulo novo (semente `apos-cap10`); "Nova Nota" → "NF-e de Saída"; em "Para quem" escolhe "Metalúrgica Pinhal Ltda" (cliente novo de Taubaté, CNPJ, sem inscrição estadual e sem CEP); o selo de cima fica vermelho: "2 pendência(s) pra emitir". [ZOOM: o selo] | E quando a nota não deixa emitir? O selo de cima conta as pendências. Enquanto ele estiver vermelho, o Emitir Nota fica travado. |
| Passa o mouse no selo: "Falta resolver:" com "Cliente com dados fiscais incompletos" e "Adicione pelo menos um item". | Passando o mouse, ele diz o que falta. Aqui, o cadastro do cliente está incompleto, e a nota ainda não tem item. |
| Clique em "Completar cadastro": abre o cadastro do cliente; preenche o CEP 12030-180 (o endereço vem sozinho) e salva (trecho acelerado). | O atalho Completar cadastro abre a ficha do cliente aqui mesmo. Preencho o CEP, salvo, e a pendência some. |
| Aparece o aviso vermelho da inscrição estadual: "... a consulta por CNPJ encontrou a inscrição 688.204.771.110 ativa em SP. ..." e o botão "Usar IE 688.204.771.110 e salvar no cadastro". [ZOOM: o aviso e o botão] | Agora olha este aviso. A Pinhal é empresa do mesmo estado e está sem inscrição estadual no cadastro. O sistema consultou o CNPJ e achou a inscrição ativa. Sem ela, a SEFAZ recusa a nota. |
| Clique em "Usar IE 688.204.771.110 e salvar no cadastro": toast "IE 688.204.771.110 salva no cadastro"; o aviso some. | Um clique grava a inscrição no cadastro e libera a nota. |
| [ILUSTRAÇÃO: Dois casos: à esquerda, um prédio "empresa com inscrição" e a nota barrada até a inscrição entrar; à direita, um prédio "empresa isenta" e a nota passando com um aviso amarelo] | Se o cliente for isento de verdade, a tela só avisa e deixa seguir. Ela só trava quando acha a inscrição. |
| "Avançar" → "Itens": inclui "Ferro misto", 1.000 kg a 1,20; apaga o NCM do item; o selo mostra "1 item(ns) sem NCM"; digita 7204.49.00 de volta; o selo vira "Pronta pra emitir". | Nos itens é a mesma ideia: item sem NCM, sem quantidade ou com o CFOP errado pro destino vira pendência, com o campo marcado. Corrigiu, o selo fica verde. |
| Clique em "Sair": "Descartar nota fiscal?"; confirma. | Esta era só um exemplo, então saio sem emitir. Um detalhe: dá pra digitar um cliente de uma venda só, sem cadastrar, em Preencher manualmente. |

Mundo: cliente "Metalúrgica Pinhal Ltda" (CNPJ fictício, Taubaté/SP, `indicador_ie` vazio, sem CEP). Handlers: consulta de IE
por CNPJ (`utils/consultaIe.ts`, com leitura do cache em `utils/consultaIeCache.ts`) devolvendo uma inscrição ativa em SP;
busca de CEP; `update` em `customers`. A nota não é emitida: não consome número.

**N3 · A SEFAZ recusou: ler o motivo e corrigir (vinheta: REJEIÇÃO)** · entra depois do N2.

| Tela | Fala |
|---|---|
| Capítulo novo (semente `apos-cap11`, mais a nota "#1252" da Serra Fina, 300 kg de alumínio perfil, R$ 3.120,00, com o selo "Rejeitada"). [ZOOM: o selo "Rejeitada"] | A nota passou pelas pendências, foi enviada, e a SEFAZ recusou. Acontece. A Serra Fina refez o pedido, e a nota nova voltou como Rejeitada. |
| [ILUSTRAÇÃO: Rejeitada não é cancelada: a folha da nota volta do prédio "SEFAZ" com um bilhete vermelho "motivo"; um selo "sem valor" aparece nela; ao lado, o número 1252 continua com um ponto "livre"] | Nota rejeitada não vale e não foi autorizada. O número dela continua livre. Então não é caso de cancelar: é corrigir e mandar de novo. |
| Menu da "#1252" → "Visualizar": faixa vermelha "Nota rejeitada pela SEFAZ" com "Cód. 778" e o texto "A SEFAZ recusou a nota: ... O que fazer: NCM inexistente em um dos itens. Corrija o NCM do material no cadastro de materiais e emita novamente.". [ZOOM: a faixa] | Em Visualizar, a faixa vermelha traz o código da rejeição, o que a SEFAZ disse e o que fazer. Aqui é o setecentos e setenta e oito: o NCM de um item não existe. |
| Fecha; menu da "#1252": zoom em "Editar e reenviar (mesmo número)" e "Editar e reemitir com novo número (#1253)". | No menu aparecem dois caminhos. Editar e reenviar usa o mesmo número. Editar e reemitir pega o próximo número livre, pra quando já saíram outras notas depois dela. |
| Clique em "Editar e reenviar (mesmo número)": abre "Reemitir NF-e de Saída" com tudo preenchido; passo "Itens": o NCM 7602.00.99 marcado; corrige para 7602.00.00. [ZOOM: o NCM] | Reenvio com o mesmo número. A nota abre preenchida. Vou nos itens e corrijo o NCM do alumínio. |
| Em "Dados", zoom em "Esta nota será reemitida como Série 1 / Nº 1252"; clique em "Emitir Nota": "Aguardando SEFAZ" e, em ~5 s, "Nota #1252 autorizada pela SEFAZ!". | A tela confirma: vai ser reemitida com o mesmo número. Emitir Nota. Pronto, autorizada. |
| [ILUSTRAÇÃO: As recusas mais comuns: quatro cartões entram um a um, cada um com o conserto: "CNPJ não habilitado → contador credencia na SEFAZ", "Inscrição estadual do cliente → corrigir o cadastro", "NCM inexistente → corrigir o material", "Certificado → enviar o A1 vigente"] | As recusas mais comuns são quatro. CNPJ não habilitado: o contador precisa credenciar a empresa na SEFAZ. Inscrição estadual do cliente errada ou faltando: corrige no cadastro. NCM que não existe: corrige no material. E certificado vencido ou do CNPJ errado: envia o A1 certo na configuração. |
| (a ilustração continua: um quinto cartão, "Instabilidade da SEFAZ → esperar e reenviar") | Às vezes o problema nem é seu: é instabilidade da SEFAZ. Aí a própria mensagem manda esperar uns minutos e enviar de novo. E uma nota recusada não trava as próximas. |
| Menu da "#1252" → "Histórico": "Histórico da NF-e" com o envio com "Erro", o reenvio e a autorização com "Sucesso" e o protocolo. | Tudo o que aconteceu com a nota fica em Histórico: a recusa, o reenvio e a autorização, com data e hora. |
| Menu de uma rejeitada (ilustração do menu, sem clicar): zoom em "Inutilizar numeração". | E se a nota recusada não for mais sair? Aí o número dela precisa ser fechado, em Inutilizar numeração, que a gente vê daqui a pouco. |

Mundo: nota 1252 já rejeitada na semente (`status` rejeitada, `error_message` "Rejeicao: Informado NCM inexistente [nItem:1]",
item com NCM 7602.00.99), mais os eventos em `nfe_events` para o Histórico. Handlers: `plugnotas-emit` em reenvio (mesmo
número) e `plugnotas-status` autorizando a 1252. Daqui em diante a numeração do mundo anda: a consolidada do caixa continua
1251 e a próxima livre passa a ser 1253 (rever as sementes `apos-cap11` em diante e a ilustração do cap13, que lista de 1246
a 1251).

**N4 · Devolução (vinheta: DEVOLUÇÃO)** · entra depois do cap12 (cancelar e corrigir), porque é o que sobra quando o prazo de
cancelar passou.

| Tela | Fala |
|---|---|
| Capítulo novo (semente `apos-cap12`). [ILUSTRAÇÃO: A carga volta: o caminhão sai da fundição de volta para o pátio com uma parte do cobre; uma folha nova, "devolução", nasce ligada por uma linha à folha "1250"] | E quando a mercadoria volta? A Fundição recebeu o cobre e devolveu quarenta quilos, que vieram com mistura. A nota mil duzentos e cinquenta já está valendo e a carga já rodou, então não é cancelamento. É uma nota de devolução. |
| Sub-aba "Entrada" → "Nova Nota" → "NF-e de Entrada"; em "Natureza da Operação" escolhe "Devolução de venda": o "CFOP" vira 1202 e aparece o campo "Chave da NF-e original (devolução)". | A mercadoria está entrando de volta, então é NF-e de Entrada, com a natureza Devolução de venda. O CFOP muda sozinho, e aparece um campo novo: a chave da nota original. |
| Clique em "Selecionar nota do sistema": "Importar NF-e de Saída para Devolução"; busca "1250"; escolhe a nota da Fundição: o cliente, a chave e os itens vêm preenchidos. [ZOOM: a chave de 44 dígitos e "Vincula esta nota à original na SEFAZ. Obrigatória para emitir."] | Toda devolução aponta pra nota que ela devolve. Em vez de colar os quarenta e quatro números, clico em Selecionar nota do sistema e escolho a mil duzentos e cinquenta. Vêm o cliente, a chave e os itens. |
| "Avançar" → "Itens": na linha "Cobre mel" troca a "Qtd" de 500 para 40; o total fica R$ 1.916,00. [ZOOM: "Qtd" 40] | Nos itens, deixo só o que voltou: quarenta quilos, pelo mesmo preço da venda. Mil novecentos e dezesseis reais. |
| Desce ao bloco "Nota de origem de cada item": "1 · Cobre mel", "Origem: <chave>" e o campo "item na origem" com 1. [ZOOM: o bloco] | Embaixo tem um bloco que só a devolução tem. A SEFAZ exige, em cada produto devolvido, a nota de origem e o número daquele item dentro dela. Como eu importei a nota, veio tudo pronto. |
| (zoom continua no campo "item na origem") | Se a nota original for antiga e o número não vier, é abrir o DANFE dela e copiar o número da coluna Item. Sem isso, a SEFAZ recusa a devolução. |
| Zoom nas abas: "Dados", "Itens", "Impostos", "Transporte", "Opções", "Pré-visualização" (sem "Faturamento"). | Repara que a aba Faturamento sumiu: devolução não tem cobrança. |
| Clique em "Emitir Nota": "Aguardando SEFAZ" e, em ~5 s, "Nota #1253 autorizada pela SEFAZ!". | Emitir Nota. Pronto: a devolução mil duzentos e cinquenta e três está autorizada, ligada à nota original. |
| [ILUSTRAÇÃO: Os dois sentidos: à esquerda, "cliente devolve a venda → Entrada, Devolução de venda"; à direita, "você devolve a compra → Saída, Devolução de compra"] | E o contrário também existe. Quando é a Recicla Vale que devolve uma compra pro fornecedor, é NF-e de Saída, com a natureza Devolução de compra. E uma dica: confirme com o contador quem emite a devolução no seu caso, você ou o cliente. |

Mundo: nada novo além da 1250 autorizada com `nfe_key` e os itens com o número de item gravado. Handlers: RPC/consulta da
lista do "Importar NF-e de Saída para Devolução" (`ImportarNfeSaidaModal.tsx`), `plugnotas-emit` e `plugnotas-status` para a
1253. Conferir no ensaio se a linha âmbar "Em compras entre empresas..." (M15) aparece nessa entrada contra CNPJ; se
aparecer, a fala ganha uma frase ("esse aviso é pra compra; aqui é devolução, pode seguir").

**N5 · Nota complementar (vinheta: COMPLEMENTAR)** · entra depois do N4.

| Tela | Fala |
|---|---|
| Capítulo novo (semente `apos-N4`), sub-aba "Saída". [ILUSTRAÇÃO: A diferença: a folha "1250" com "R$ 47,90 o quilo"; ao lado, um bilhete "combinado: R$ 48,40"; uma folha pequena, "complementar", nasce com só a diferença] | Último caso: a nota saiu com valor a menor. O preço combinado com a Fundição era quarenta e oito e quarenta, e a nota saiu a quarenta e sete e noventa. Não se corrige valor com carta de correção. Pra isso existe a nota complementar, que leva só a diferença. |
| Menu da "#1250" → "Gerar nota complementar": abre "Nova NF-e de Saída" com a natureza "Complementar de venda", o cliente e a "Chave da NF-e original (complementar)" preenchidos. [ZOOM: a natureza e a chave] | No menu da nota original, Gerar nota complementar. Ela já abre com o cliente, a natureza e a chave da nota original. |
| Zoom em "Contar esta nota no Estoque Fiscal" (desmarcado) e no texto "Marque só se este complemento for de PESO/QUANTIDADE. ...". | Repara nesta opção, desmarcada. Complemento de preço não mexe no estoque fiscal, porque o peso já saiu na nota original. Só se marca quando o complemento é de peso. |
| "Avançar" → "Itens": "Cobre mel", "Qtd" 460, "Valor" 0,50; total R$ 230,00. [CONFERIR NA TELA como a complementar de valor se preenche] | Nos itens vai só a diferença: cinquenta centavos por quilo, nos quatrocentos e sessenta quilos que ficaram com o cliente. Duzentos e trinta reais. |
| Clique em "Emitir Nota": "Aguardando SEFAZ" e "Nota #1254 autorizada pela SEFAZ!". | Emitir Nota. Pronto: a complementar mil duzentos e cinquenta e quatro está autorizada. O mesmo caminho serve pra imposto que saiu a menor, sempre com a orientação do contador. |

Mundo: nada novo. Handlers: `plugnotas-emit` e `plugnotas-status` para a 1254. **Risco**: não li como o item de uma
complementar de valor é montado no XML (quantidade × diferença); o exemplo precisa do ensaio e do aval do contador do Kaik
antes de virar fala.

**N6 · Outras operações (trecho curto, dentro do cap09 ou logo depois do cap11)**

| Tela | Fala |
|---|---|
| "Nova Nota" → "NF-e de Saída"; abre a lista "Natureza da Operação": "Venda de mercadorias", "Venda de produção própria", "Remessa para conserto", "Remessa para demonstração", "Remessa para fins de exportação", "Devolução de compra", "Complementar de venda", "Transferência de mercadorias", "Baixa de estoque por perda" e "Outra operação". [ZOOM: a lista] | A natureza da operação tem bem mais que venda e compra: remessa pra conserto, transferência entre unidades, baixa por perda. E, se a sua não estiver na lista, Outra operação deixa escrever o nome. O CFOP de cada uma vem da configuração. |
| Escolhe "Baixa de estoque por perda": o cliente some (nota contra a própria empresa), o CFOP vira 5927 e aparece "Dar baixa no estoque físico ao autorizar". [ZOOM: a opção] | Um exemplo: material que estragou ou foi furtado. A baixa por perda é uma nota contra a própria empresa. E dá pra marcar pra ela já dar baixa no estoque físico quando for autorizada. |
| "Sair" sem emitir. | Qual natureza usar em cada caso, é o contador quem diz. |

Mundo: nada novo; sem emissão.

### 3.3 Resumo (cap18)
Acrescentar uma linha à montagem: "Conferiu os impostos e as parcelas antes de emitir, resolveu uma pendência, corrigiu uma
nota recusada, e emitiu uma devolução e uma complementar." E uma frase final: "Quem usa o Cato também pode pedir a nota de um
pedido pela conversa. Isso fica no tutorial do Cato."

## 4. Estimativa

| Item | Palavras de fala | Segundos (2,6 palavras/s) |
|---|---|---|
| Ajustes nos capítulos 01 a 14 (3.1) | 547 | 210 |
| N1 Impostos e outras abas | 284 | 109 |
| N2 Pendências | 185 | 71 |
| N3 Rejeição | 269 | 103 |
| N4 Devolução | 265 | 102 |
| N5 Complementar | 154 | 59 |
| N6 Outras operações | 87 | 33 |
| Resumo | ~45 | 17 |
| **Total** | **~1.840** | **~705 s (≈ 12 min de fala)** |

Capítulos novos: **5** (N1 a N5) mais **1 trecho** (N6); com vinhetas e esperas de SEFAZ, a aula vai de ~22 min para ~35 min.
Regravar por mudança de tela: caps 03, 06, 09, 10 e 11 (inteiros) e os zooms dos caps 01 e 02.

## 5. Decisões que dependem do Kaik
1. **Tamanho**: ~35 min numa aula só, ou partir em duas (T16a configuração, caps 00 a 08; T16b emissão e correções).
2. **Complementar (N5)**: o exemplo de diferença de preço precisa do aval do contador e do ensaio; sem isso, vira só citação.
3. **Quem emite a devolução (N4)**: a aula mostra a Recicla Vale emitindo a entrada de devolução de um cliente contribuinte;
   na prática muitos contadores pedem que o cliente emita. A fala já manda confirmar, mas o exemplo pode trocar para
   "Devolução de compra" (saída) se o Kaik preferir.
4. **Numeração do mundo**: N3, N4 e N5 consomem 1252, 1253 e 1254; mexe nas sementes da T17 e T18 (que partem do fim da T16).
5. **Relatórios Fiscais › NF-e**: saiu do Estoque Fiscal e virou tela própria; confirmar que a T17 cobre, senão entra aqui.
6. **Valores de imposto na fala (N1)**: ler os números da tela (depois do robô) ou manter a fala só nos percentuais.
