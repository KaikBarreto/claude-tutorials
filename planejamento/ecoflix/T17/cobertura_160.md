# Cobertura 1.60.10 · T17 Transporte, serviço e o contador

Auditoria só de leitura (18/11). Roteiro escrito no 1.59.154 (`f37573ea0`); app lido no 1.60.10 (`/dev/shm/ecoflix-src`,
caminhos relativos a `src/`). Sem varredura do robô para a T17 (`rec/varredura/` só tem t00 e t01). Rótulo entre aspas =
texto exato do código. Não mudaram desde o roteiro: Frota (`coletas/VehiclesTab.tsx`, `DriversTab.tsx`), aba de
movimentações (`FiscalInventoryHistoryTab.tsx`) e a comparação (`EstoqueFiscalTab.tsx`); nelas só há lacuna, não mudança.

## 1. Mudou no app (por capítulo)

### cap00 · Abertura
- **M1. Menu ganhou um item.** "Fiscal & Ambiental" agora termina em "Estoque Fiscal" e **"Relatórios Fiscais"**
  (`config/routes.ts:510-511`). "Estoque Fiscal" abre em `/fiscal-ambiental/estoque-fiscal/posicao` (antes `/relatorio`). A
  fala "em Transporte, em Notas de Serviço e no Estoque Fiscal" fica incompleta.

### cap03 · Numeração e percurso
- **M2. "Sincronizar Numeração"** não chama mais serviço externo: grava e mostra "Numeração do MDF-e atualizada: Série 1, Nº 1"
  (`mdfe/ConfigRodoviarioModal.tsx:109-111`). O texto "A numeração será sincronizada com o serviço fiscal..." continua
  (`:191`). O roteiro não clica; só muda se a aula passar a clicar.

### cap04 · Emitir o manifesto
- **M3. "Novo MDF-e" virou tela cheia** (`FiscalFullscreenWizard`), com o quadro "Documento" / "Modelo 58" no cabeçalho
  (`mdfe/NovoMdfeModal.tsx:1106-1117`). Etapas, "Resumo do MDF-e" e botões ("Cancelar", "Voltar", "Continuar", "Criar MDF-e")
  iguais (`:82-85`, `:1083-1101`).
- **M4. Etapa 1, rodapé da lista:** "2 NF-e(s) **vinculada(s)** • Valor total: R$ 55.380,00" (`:1302`; antes
  "selecionada(s)"). Embaixo da lista entrou o bloco novo "Importar nota pela chave de acesso" (`:1194-1298`, ver L1).
- **M5. Etapa 3, valor da carga:** rótulo "Valor Total da Carga (R$)", agora **editável**, com a ajuda "Sugerido pelas notas —
  pode ajustar." (`:1788-1804`; antes travado). A fala "E o valor da carga também" continua certa, mas perde a novidade.
- **M6. Toast da emissão:** "MDF-e #1 criado" (`:994`) e **"MDF-e #1 enviado ao motor fiscal próprio"** (`:1013`; antes
  "enviado para SEFAZ!"). A fala não muda; a coluna Tela e o robô, sim. Jargão interno na tela: anotar em
  `MELHORIAS_ECOSISTEMA.md`.
- **M7. Backend do manifesto:** emitir, consultar, encerrar, baixar e cancelar passam todos pela função `mdfe-contingency`
  com `action` `prepare` / `status` / `enclose` / `download` / `cancel` (`NovoMdfeModal.tsx:1001-1011`, `mdfe/MdfeTab.tsx:255-256`,
  `hooks/useMdfe.tsx:75,87,107,122,135`). As funções `plugnotas-mdfe-*` não são mais chamadas. A consulta automática de 5 s
  não exige mais `plugnotas_id` (`MdfeTab.tsx:249-253`). Toasts "MDF-e #1 autorizado!" e de encerramento iguais (`:258-263`).

### cap05 · Encerrar
- **M8.** Só o backend (M7): `mdfe-contingency` com `action: "enclose"`. Rótulos e selos iguais.

### cap07 · Emitir e acompanhar (NFS-e)
- **M9. "Nova NFS-e" virou tela cheia**, subtítulo "Informe o tomador, o serviço e os valores antes de transmitir ao
  município." e quadro "Ambiente" / "Produção" (ou "Homologação") (`NovaNfseModal.tsx:1151-1159`). Rodapé: "Cancelar" (1ª
  aba) ou "Voltar", "Salvar rascunho" (antes "Salvar Rascunho"), "Avançar", "Emitir NFS-e" (`:1015-1047`).
- **M10. Aba "Pessoas":** campo novo **"Série da DPS"** ("Série 1") com "Próxima DPS: nº 14" embaixo
  (`nfse/PessoasStep.tsx:131-148`).
- **M11. Aba "Serviço":** campo novo "Código de tributação municipal (opcional)" com "Preencha somente quando a prefeitura
  usar um complemento próprio ao código nacional." (`nfse/ServicoStep.tsx:232-246`).
- **M12. Aba "Valores":** "Retenções federais **(R$)**" e "Informe o valor efetivamente retido de cada tributo."
  (`nfse/ValoresStep.tsx:158-160`; antes "(%)").
- **M13. Pré-visualização** mostra a série e o número previsto de verdade (`nfse/EmitirStep.tsx`, props `serie` e
  `numeroPrevisto`; antes "a definir"). Com problema de certificado aparece o botão "Abrir certificado digital" (`:98`).
- **M14. Emissão e toasts:** o próprio modal transmite (`plugnotas-emit-nfse`, `NovaNfseModal.tsx:797`). Toast novo: **"NFS-e
  autorizada com sucesso"** (resposta já `emitida`) ou **"NFS-e enviada. A confirmação oficial aparecerá na lista."**
  (`:825-827`). "Nota de serviço enviada para emissão" saiu. Bloqueios novos antes de emitir: certificado lido da RPC
  `fiscal_onboarding_status` (`certificate_ready`, `:184`, `:525-539`) e, em produção, "cobertura do município" pela função
  `plugnotas-nfse-servicos-municipio` (`:290-321`, `:540-546`). Sem esses dois handlers o selo fica "1 pendência".
- **Não mudou (segue valendo o achado 1 de `propostas_fala.md`):** a alíquota do município ainda não chega a "Alíquota ISS %"
  (`NovaNfseModal.tsx:239`, `nfse/ServicoStep.tsx:124-127`); o robô continua digitando 3.

### cap08 · O serviço que você tomou
- **M15. Ativar não traz mais as notas na hora.** A ativação grava direto e marca a busca para o motor fiscal
  (`hooks/useInboundNfse.ts:160-190`); sai só o toast "Notas de serviço recebidas ativado"
  (`notas-recebidas/NotasRecebidasNfseTab.tsx:274`) e a faixa "Busca solicitada no Ambiente Nacional. A lista atualiza
  automaticamente em até 10 minutos." (`useInboundNfse.ts:210`; exibida em `NotasRecebidasNfseTab.tsx:834-837`). O toast "2
  nota(s) de serviço sincronizada(s)" não acontece nesse caminho. A fala "ele já buscou as notas, e chegaram duas" fica falsa.
  A função `plugnotas-enable-nfse-dfe` não é mais chamada.
- **M16. "Nova conta":** ordem dos campos agora "Tipo", "Descrição", "Vencimento", "Valor", "Categoria"
  (`contas/BillFormModal.tsx:891-968`), com as sugestões de preenchimento do 1.60.5 (assunto da T14). A fala não cita ordem;
  o robô precisa dos seletores novos.

### cap09 · Entrada, saída e saldo
- **M17. O relatório saiu do Estoque Fiscal.** Agora é menu **"Relatórios Fiscais"**, título "Relatórios Fiscais", sub-abas
  **"NF-e"** (o relatório do roteiro) e **"NFS-e"** (novo) (`pages/NotasFiscais.tsx:202-205,233`; rota
  `/fiscal-ambiental/relatorios/nfe`; os links antigos redirecionam, `App.tsx:507-520`). A fala "No Estoque Fiscal, a primeira
  aba é o Relatório fiscal" e a coluna Tela mudam. Cartões e gráficos iguais.
- **M18.** RPC trocada para `get_invoice_dashboard_secure` (`hooks/useInvoiceDashboard.tsx:183`); quem não pode ver valores vê
  "Valores protegidos" (`VisaoGeralTab.tsx:131`). Rafael é MASTER: não aparece.

### cap10 · O estoque pelas notas
- **M19. Sub-abas novas** (`pages/NotasFiscais.tsx:196-201`): **"Saldo atual"**, **"Posição em uma data"**,
  **"Movimentações"**, "Fiscal × operacional". Antes: "Relatório fiscal", "Posição do estoque", "Histórico fiscal", "Fiscal ×
  operacional".
- **M20. "Saldo atual"** (`FiscalInventoryPositionTab.tsx:137-143`): título "Saldo atual", subtítulo "Saldo fiscal atualizado,
  por material. Não altera o estoque operacional.". Não tem mais data nem "Ver posição". Busca nova "Buscar material ou
  código" (`:315`) e menu "⋯" por linha com "Informar saldo inicial" (`:349-360`). Atualiza sozinho: ao abrir, ao voltar à
  aba e a cada 10 s (`hooks/useFiscalInventoryLedger.ts:15,131-135`).
- **M21. "Posição em uma data"** é aba própria: título "Posição do estoque em uma data", "Saldo fiscal em 31/10/2026 às
  18:00. Não altera o estoque operacional.", "Data e hora da posição", "Ver posição" (`:137-143,186-200`). **"Voltar para
  agora" não existe mais** (o roteiro para a câmera nele e depois clica). Aqui não há "Informar saldo inicial".
- **M22. "Histórico fiscal" virou "Movimentações"** (só o nome da aba; dentro continua "KARDEX FISCAL — ...",
  `FiscalInventoryHistoryTab.tsx:366`). A fala "No Histórico fiscal fica o Kardex fiscal" muda.
- **M23. Regra do saldo (1.60.6, banco):** nota cancelada gera linha "Estorno" na data do cancelamento, com o motivo, tanto
  emitida quanto recebida; devolução entra pelo CFOP 1202/2202 e sai pelo 5202/6202
  (`supabase/migrations/20261117203000_fiscal_inventory_returns_and_live_balance.sql:41-70,187-209,264-286`). O roteiro não
  mostra nenhum dos dois casos (ver L20).

### cap11 · O pacote do mês
- **M24. Dois blocos novos no diálogo, antes de "Tipo de nota"** (`ExportContabilDialog.tsx:323-388`): "Emitente / CNPJ"
  ("Todos os CNPJs" ou um emitente; "Selecione um CNPJ para gerar o pacote somente daquele emitente.") e "Origem dos
  documentos" com a caixa **"Incluir notas destinadas ao CNPJ"** ("XMLs de NF-e emitidas por fornecedores contra a sua
  empresa. Entram na pasta “xmls/destinadas”."), desmarcada de saída. Aviso de tipo: "Marque Saída, Entrada ou notas
  destinadas." (`:410`). A câmera do roteiro passa por "Período" → "Tipo de nota": agora há dois blocos no meio.
- **M25. Toast final:** "Exportação pronta" / **"12 saída + 9 entrada + 0 destinada(s) baixados"**
  (`contexts/ExportProgressContext.tsx:156`). O menu "⋮" agora aparece também para quem só tem a permissão de exportar, sem
  "Nova Nota" (`pages/NotasFiscais.tsx:2132,2195-2209`).

### cap12 · O que o contador faz
- **M26.** Com a caixa das destinadas marcada, o ZIP ganha `AAAA-MM/xmls/destinadas/` e o "LEIA-ME.txt" lista as que ainda
  não têm XML (`utils/contabilExport/runExportPipeline.ts:333-349`, `buildReadmeClient.ts`). A ilustração só muda se a aula
  marcar a caixa.

## 2. Falta cobrir

### Manifesto (MDF-e)
| # | O que é (arquivo) | Quando o cliente usa | Vale? |
|---|---|---|---|
| L1 | "Importar nota pela chave de acesso": campo "Cole os 44 dígitos da chave", botão "Adicionar", selos "Nota recebida" / "Externa", "Valor (opcional)", aviso "Essa nota é do seu próprio CNPJ" (`NovoMdfeModal.tsx:1194-1298`; recusas em `:654-688`) | o caminhão da empresa leva carga com nota de outra empresa (buscar no fornecedor PJ o material comprado) | **sim, trecho** (novo) |
| L2 | "Frete de terceiros (CIOT)" + "Opcional": "RNTRC", "CIOT" ("Código numérico com 12 dígitos"), "CPF/CNPJ do gerador do CIOT" ("Obrigatório junto do CIOT"), "Contratante — CPF/CNPJ", "Contratante — Nome"; ajuda "?" "Como gerar o CIOT?" com dois links externos (`:1568-1678`); erros `:89-90,832-846` | frete pago a terceiro (caminhoneiro autônomo, agregado) | **sim, trecho** (pedido do Kaik) |
| L3 | Contingência escolhida: "Motivo da contingência *" (15 a 255), "Tipo de carga *" (12 opções, `:92-96`), "NCM do produto *", "Produto predominante *", CEPs quando há uma nota só (`:1841-1851`); selos "Preparando contingência", "Em contingência", "Falha na contingência", "Contingência recusada" (`MdfeStatusBadge.tsx:41-44`); menu "Enviar à SEFAZ", "Baixar XML assinado" e "Prazo de envio" (`MdfeTab.tsx:49-55,451-459`) | SEFAZ fora do ar na hora da saída | **sim, trecho** (hoje é só um zoom no botão) |
| L4 | "Reboques / Carretas (opcional)": "Adicionar reboque...", até 3 (`lib/mdfeComposicao.ts:23`), "Tara da composição" / "Capacidade da composição" (`NovoMdfeModal.tsx:1482-1552`) | cavalo com carreta | só citar (uma frase) |
| L5 | Dados que faltam na Frota perguntados no manifesto e guardados ("Vamos guardar na Frota, então estas perguntas não se repetem.", `:1388-1447`); "Ou digite a placa" / "Ou digite o nome" (`:1361,1467`) | veículo incompleto ou fora da frota | só citar |
| L6 | "OBSERVAÇÕES" ("Observações que aparecerão no DAMDFE...", `:1810-1816`) | recado no papel do manifesto | só citar |
| L7 | "Cancelar MDF-e #N": "O cancelamento será enviado à SEFAZ e é irreversível.", "...geralmente é de 24 horas...", "Motivo do cancelamento (mín. 15 caracteres)", "Voltar", "Confirmar Cancelamento" (`MdfeTab.tsx:765-805`) | manifesto emitido errado, carga não saiu | **sim, trecho** (abrir e "Voltar"; hoje só a ilustração) |
| L8 | Manifesto "Rejeitado": "Ver Erro" → "Erro no MDF-e #N", "Reemitir", "Excluir" → "Excluir MDF-e?"; "Pendente": "Emitir", "Excluir" (`:292-311,362-378,726-763`) | a SEFAZ recusou | **sim, capítulo curto** (depende de semente; decisão D2) |
| L9 | "Encerramento recusado" / "Cancelamento recusado" com "Ver Erro", "Verificar Status" e reenviar (`:379-432`); selo clicável "Consultar novamente na SEFAZ" (`:178-196`) | o pedido não passou | só citar (junto de L8) |
| L10 | Linha expandida "Detalhes do MDF-e #N" (com "Composição:", "Criado por:", "Erro SEFAZ:"), busca "Buscar por nº, placa ou motorista...", paginação (`:640-710`) | conferir um manifesto antigo | só citar |
| L11 | Novo veículo, novo motorista, excluir, tipos "Cavalo mecânico (tração)" e "Carreta / Reboque" | montar a frota | não: T12 (frota das coletas); aqui só o que o manifesto exige |

### Nota de serviço
| # | O que é | Quando usa | Vale? |
|---|---|---|---|
| L12 | "Série da DPS" e "Próxima DPS: nº N" (M10) | saber o número antes de emitir | **sim, uma frase** |
| L13 | "ISS retido na fonte" ("Tomador é responsável por reter e recolher."), "Retenções federais (R$)", "Ajustes (deduções e descontos)" (`nfse/ValoresStep.tsx:89-160`) | tomador PJ que retém imposto: caso comum de quem está no Lucro Real | **sim, trecho** (mostrar, sem preencher) |
| L14 | "Salvar rascunho" → "Rascunho salvo"; continuar e excluir rascunho (`NfseTab.tsx:230`) | nota começada sem o código do contador | só citar |
| L15 | Tomador por "Buscar pelo CNPJ" e "Preencher manualmente"; intermediário (`nfse/PessoasStep.tsx:157-316`) | tomador sem cadastro | só citar |
| L16 | Menu da linha: "Visualizar", "Consultar status", "Baixar XML", "Cancelar" (toast "Cancelamento enviado. A confirmação da prefeitura aparece em instantes.", `NfseTab.tsx:250`); filtro "Status" e ordenação (`:85-92,346-351`) | nota errada, conferir | só citar (o cancelamento depende da prefeitura) |
| L17 | "Código de tributação municipal (opcional)", "Situação do ISSQN", "Item NBS (opcional)", "Informações complementares" | só quando o contador pedir | não (a fala já diz que o código é do contador) |
| L18 | Relatório de NFS-e: cartões "Serviços autorizados", "ISS apurado", "Retenções federais" ("PIS, COFINS, CSLL, INSS e IRRF"), "Pendentes + rejeitadas"; "Valor autorizado no período", "Distribuição por status", "Top tomadores", "Top serviços" (`NfseReportTab.tsx:114-146,180-286`) | fechar o mês de serviço com o contador | **sim, trecho** (novo) |
| L19 | NFS-e recebidas: "Sincronizar agora", "Última sincronização", busca, "Baixar XML", aviso "Lançar esta despesa de novo?", faixa do certificado A1 (`NotasRecebidasNfseTab.tsx:755-812,1094`) | forçar a busca, não lançar duas vezes | "Sincronizar agora": **sim, uma frase**; resto só citar |

### Relatório e estoque fiscal
| # | O que é | Quando usa | Vale? |
|---|---|---|---|
| L20 | Cartão "Entrada" aberto: "Emitidas por você", "Recebidas de Fornecedor", "Recebidas ainda não classificadas" / "Não entram no total", "Ver notas recebidas" (`VisaoGeralTab.tsx:281-317`) | entender de onde vem a entrada (no Lucro Real, é a nota que dá crédito) | **sim, uma linha** |
| L21 | "Informar saldo inicial": "CNPJ", "Data-base", abas "Manual" ("Material", "Quantidade") e "Planilha" ("Baixar modelo", "Escolher planilha", tabela "Linha / Código / Quantidade / Validação"), "Confirmar saldo inicial" → "Saldo inicial registrado" (`FiscalInventoryPositionTab.tsx:621-784`); faixa amarela "Alguns saldos foram apurados pelas notas disponíveis, pois ainda não têm saldo inicial informado." (`:299-309`) | empresa que começa a usar o sistema já com estoque | **sim, capítulo** (o inventário marcou "não usado") |
| L22 | Saldo em vermelho quando negativo, selo "Arquivado", vazio "Nenhum material no estoque fiscal." (`:289,333,342`) | ler a tabela | uma frase dentro do capítulo |
| L23 | Atualização automática do saldo (M20) | acabou de emitir e quer ver o saldo | **sim, uma frase** (é a manchete do 1.60.6) |
| L24 | Movimentações: "Filtros" ("De", "Até", "CNPJ", "Tipo": "Entrada", "Saída", "Saldo inicial", "Ajuste", "Estorno"; "Nota, chave ou parceiro"; "Limpar filtros"), "Ordenar materiais" ("Código", "Nome"), "Geral (Todos)" (`FiscalInventoryHistoryTab.tsx:164-307`); coluna "Origem": "Nota fiscal", "Estorno", "Saldo inicial", "Ajuste manual", com o motivo embaixo (`:419-428,508-514`) | achar uma nota no Kardex, auditar um mês | **sim, trecho** |
| L25 | Cancelamento e devolução no Kardex (M23) | conferir que o saldo voltou depois de cancelar ou devolver | **sim, capítulo novo** (pedido do Kaik) |
| L26 | Fiscal × operacional: botão "Exportar" ("PDF", "Excel", `EstoqueFiscalTab.tsx:224-256`); cartões "Materiais com divergência" e "Alertas"; selos "Unid. mista", "Não classificado", "Material arquivado", "Saldo negativo" (`:719-775`); as outras linhas do quadro: "Delta negativo costuma indicar compra de pessoa física sem nota..." e "Notas de baixa por perda..." (`:636-647`) | mandar a comparação ao contador; entender a divergência mais comum do ferro-velho | **sim, trecho** (e resolve o achado 4: 13 materiais divergem, não um) |
| L27 | Seletor "Todos os CNPJs" e coluna "CNPJ" (só com mais de um emitente) | matriz e filial | não: T22 |

### Pacote do contador
| # | O que é | Quando usa | Vale? |
|---|---|---|---|
| L28 | "Incluir notas destinadas ao CNPJ" e a linha da prévia "Destinadas: N XML(s) · N ainda sem XML disponível" (`ExportContabilDialog.tsx:369-388,565-575`) | no Lucro Real o contador precisa do XML do fornecedor para o crédito | **sim, trecho** |
| L29 | "Emitente / CNPJ" | um pacote por CNPJ | só citar (um CNPJ no mundo) |
| L30 | "Tamanho estimado", "Tempo estimado" (`:579-590`); desmarcar status | pacote grande | só citar |
| L31 | Usuário só com "Exportação Contábil" (M25) | dar acesso ao escritório de contabilidade | só citar: permissões são da aula de usuários |
| L32 | "SPED Fiscal" (selo "BETA", `config/routes.ts:506`, atrás do recurso `sped_fiscal`) | arquivo fiscal para o contador | não: fora da trilha e não aparece no plano do mundo (achado 7). Decisão D4 |
| L33 | "Inutilizar numeração" no mesmo menu "⋮" | pulo de numeração | não: T16 |

## 3. Proposta

Falas no tom da aula. `[BACKEND]` = o que o mundo falso precisa.

### 3.0 Ajustes de fala nos capítulos que já existem
| Cap. | Tela | Fala nova |
|---|---|---|
| 00 L4 | o destaque passa também por "Relatórios Fiscais" | Tudo isso fica no menu Fiscal & Ambiental: em Transporte, em Notas de Serviço, no Estoque Fiscal e nos Relatórios Fiscais. |
| 04 (valor) | zoom em "Valor Total da Carga (R$)" e "Sugerido pelas notas — pode ajustar." | E o valor da carga vem sugerido pelas notas. Se o valor real for outro, dá pra ajustar. |
| 04 (criar) | toasts "MDF-e #1 criado" e "MDF-e #1 enviado ao motor fiscal próprio" | (fala igual) |
| 04 (etapa 2, depois do motorista) | a câmera passa por "Reboques / Carretas (opcional)" | Se o caminhão puxa carreta, ela entra aqui embaixo, em Reboques. São até três. |
| 07 L1 | "Série da DPS" "Série 1" e "Próxima DPS: nº 14" | (acrescentar) A série e o próximo número já aparecem aqui: esta vai ser a catorze. |
| 07 (emitir) | toast "NFS-e enviada. A confirmação oficial aparecerá na lista." | Emitir NFS-e. Ela foi enviada, e a confirmação aparece na lista. |
| 08 L4 | "Ativar mesmo assim": toast "Notas de serviço recebidas ativado"; a tela vira a lista, com a faixa "Busca solicitada no Ambiente Nacional. A lista atualiza automaticamente em até 10 minutos." | Ativar mesmo assim. Pronto, ativado. A busca roda sozinha, e as notas chegam em alguns minutos. |
| 08 L4b (novo) | corte curto (ou semente `apos-cap08a`): as duas notas na lista; zoom em "Sincronizar agora" e "Última sincronização" | Um pouco depois, chegaram duas notas. E se você quiser adiantar a busca, é só clicar em Sincronizar agora. |
| 10 | nomes das abas (M19 a M22) | ver 3.4 a 3.8 |
| 11 L1 | igual | (fala igual) |
| 13 L3 | montagem com "Saldo atual", o estorno e o toast | Conferiu os relatórios fiscais de outubro, viu o saldo fiscal de cada material, com cancelamento e devolução, comparou com o estoque do pátio e exportou o pacote do mês pro contador. |

`[BACKEND cap07]` RPC `fiscal_onboarding_status` com `certificate_ready: true`; `get_next_nfse_number` devolvendo 14;
`nfse_series` com a série 1; `plugnotas-emit-nfse` devolvendo `{ok, status: "processando"}`. `[BACKEND cap08]` update direto
em `company_fiscal_config` (`nfse_dfe_ativo`, `nfse_dfe_fonte: "sefin"`); `inbound_nfse` vazia até o corte.
`[BACKEND cap04/05]` função `mdfe-contingency` respondendo a `prepare`, `status`, `enclose`, `download`.

### 3.1 Trecho novo no cap04 · Nota de outra empresa, pela chave (depois de marcar as duas notas)
| Tela | Fala |
|---|---|
| A câmera desce até "Importar nota pela chave de acesso" e o texto "Use quando a NF-e foi emitida por outra empresa. Se ela já estiver em Notas Recebidas, preenchemos emitente e valor sozinhos." | E quando o seu caminhão leva carga com nota de outra empresa? Por exemplo, buscar no fornecedor o material que você comprou. Aí a nota entra pela chave de acesso. |
| Cola a chave da NF-e nº 884 do Depósito Irmãos Siqueira em "Cole os 44 dígitos da chave" e clica em "Adicionar": toast "NF-e #884 encontrada em Notas Recebidas"; a linha "NF-e #884 · Depósito Irmãos Siqueira", selo "Nota recebida" e o valor R$ 2.100,00. [ZOOM: a linha com o selo "Nota recebida"] | Colo os quarenta e quatro dígitos e clico em Adicionar. Como essa nota já estava nas Notas Recebidas, o sistema preencheu quem emitiu e o valor. |
| Zoom no rodapé "3 NF-e(s) vinculada(s) • Valor total: R$ 57.480,00". | Se a nota não estiver lá, ela entra do mesmo jeito, só com a chave, e o valor você digita se quiser. |
| Clica no "X" da linha ("Remover NF-e 884"): volta a "2 NF-e(s) vinculada(s) • Valor total: R$ 55.380,00". | Hoje a carga é só da Recicla Vale, então eu tiro essa nota e sigo com as duas. |

`[BACKEND]` `inbound_nfe` da nota 884 (T16) com `chave` de 44 dígitos **com dígito verificador válido e modelo 55**
(`lib/nfeAccessKey`), `emitente_nome`, `numero` 884, `valor` 2100.

### 3.2 Trecho novo no cap04 · Frete de terceiros (CIOT) (na etapa "Veículo e motorista", antes de "Continuar")
| Tela | Fala |
|---|---|
| Clica em "Frete de terceiros (CIOT)", com o selo "Opcional": a seção abre. [ZOOM: "O CIOT é exigido no transporte rodoviário remunerado de cargas de terceiros. Não se aplica ao transporte de carga própria sem cobrança de frete."] | Aqui embaixo fica o frete de terceiros. O CIOT é um código exigido quando o transporte é pago: você contrata um caminhoneiro, ou leva a carga de outra empresa cobrando frete. |
| A câmera passa por "RNTRC", "CIOT" ("Código numérico com 12 dígitos") e "CPF/CNPJ do gerador do CIOT" ("Obrigatório junto do CIOT"). | Nesse caso, vão aqui o registro do transportador, o RNTRC, o código do CIOT, com doze dígitos, e o CPF ou CNPJ de quem gerou o código. Os dois últimos andam juntos: um não entra sem o outro. |
| A câmera passa por "Contratante — CPF/CNPJ" e "Contratante — Nome". | E, se quiser, quem contratou o frete. |
| Passa o mouse no "?" ao lado de "CIOT" ("Como gerar o CIOT"), sem abrir os links; fecha a seção. (ver D1) | O código é gerado antes da viagem, numa instituição autorizada pela ANTT. Na dúvida se a sua viagem precisa, pergunte ao contador. |
| A seção fechada; a câmera volta ao veículo "Caminhão truck • FKD2E41 • SP". | Hoje a carga é da própria Recicla Vale, no caminhão dela, sem cobrar frete. Então fica em branco. |

`[BACKEND]` nada novo.

### 3.3 Trechos novos · Contingência, cancelamento e manifesto recusado
**No cap04 (substitui a linha do zoom no botão "Contingência"):**
| Tela | Fala |
|---|---|
| Clica em "Contingência" ("Use quando a SEFAZ estiver indisponível"): aparecem "Motivo da contingência *", "Tipo de carga *", "NCM do produto *" e "Produto predominante *". | Uma dica: a contingência é só pra quando a SEFAZ estiver fora do ar. Ela pede o motivo, o tipo de carga, o NCM e o produto principal da carga. |
| Zoom em "Imprima o DAMDFE em papel antes de liberar o caminhão. Prazo de regularização: até 168 horas." | O motorista só sai com o manifesto impresso em papel. E o sistema tem até cento e sessenta e oito horas, sete dias, pra enviar à SEFAZ. |
| Clica de volta em "Normal"; o quadro verde "Tudo pronto para criar e emitir o MDF-e" reaparece. | Hoje a SEFAZ está no ar, então eu volto pro Normal. |

**No cap05 (depois da ilustração encerrar × cancelar, antes de "Encerrar"):**
| Tela | Fala |
|---|---|
| "Ações" → "Cancelar": diálogo "Cancelar MDF-e #1". [ZOOM: "...é irreversível." e "O prazo para cancelamento geralmente é de 24 horas após a autorização, variando conforme a UF."] | Olha o cancelamento: ele não tem volta, pede um motivo com pelo menos quinze letras, e o prazo costuma ser de vinte e quatro horas. |
| Clica em "Voltar"; o manifesto continua "Autorizado". | Não é o caso aqui. Voltar. |

**Capítulo novo 05b · Quando o manifesto não passa (vinheta: MANIFESTO)** (depende de D2)
| Tela | Fala |
|---|---|
| Lista com o nº 1 "Encerrado" e um nº 2 "Rejeitado" (rascunho da viagem de amanhã). O cartão "MDF-e Rejeitados" em 1. [BACKEND: `mdfe_manifests` nº 2, `status: rejeitado`, `error_message` de placa sem UF] | E quando a SEFAZ não aceita? O manifesto fica como rejeitado, e conta aqui em cima. |
| "Ações" → "Ver Erro": "Erro no MDF-e #2" com a mensagem; "Fechar". | Em Ver Erro, o sistema mostra o motivo. Aqui, falta um dado do veículo. |
| "Ações" de novo: "Reemitir" e "Excluir" (sem clicar). | Você corrige o cadastro na Frota e clica em Reemitir. Ou, se o manifesto não serve mais, exclui. |
| Zoom nos selos possíveis numa faixa (ilustração com os selos do código: "Encerramento recusado", "Cancelamento recusado"). | E se a SEFAZ recusar um encerramento ou um cancelamento, o manifesto continua valendo. É só ver o erro e pedir de novo. |

### 3.4 cap09 reescrito · Entrada, saída e saldo (vinheta: RELATÓRIO FISCAL)
| Tela | Fala |
|---|---|
| Menu "Fiscal & Ambiental" › "Relatórios Fiscais": título "Relatórios Fiscais", sub-aba "NF-e"; no filtro do cabeçalho, "Mês passado". [BACKEND: `get_invoice_dashboard_secure` com `can_view_values: true`] | Antes de mandar o mês pro contador, vale conferir os números. Em Relatórios Fiscais, a primeira aba é a das notas de mercadoria. Escolho o mês passado, outubro. |
| (as três linhas dos cartões "Entrada", "Saída", "Saldo (Saída − Entrada)" e "Pendentes + Rejeitadas": como no roteiro) | (falas iguais) |
| Clica no cartão "Entrada": abre "Emitidas por você" e "Recebidas de Fornecedor". [ZOOM: as duas linhas] | Clicando na Entrada, ela se divide: as notas de entrada que a Recicla Vale emitiu, nas compras de pessoa física, e as que os fornecedores emitiram contra ela. No Lucro Real, é nessas notas que o contador busca os créditos de imposto. |
| Rola até os gráficos e os rankings (como no roteiro). | (fala igual) |
| Sub-aba "NFS-e": cartões "Serviços autorizados", "ISS apurado", "Retenções federais" e "Pendentes + rejeitadas". [ZOOM: "ISS apurado"] [BACKEND: RPC `get_nfse_dashboard` com as NFS-e 12 e 13 de outubro, se forem de outubro; senão período "Este mês"] | A segunda aba é o mesmo relatório pras notas de serviço: quanto foi autorizado, o ISS do período e as retenções. |
| Rola até "Top tomadores" e "Top serviços". | E embaixo, quem mais contratou e quais serviços mais saíram. |

### 3.5 cap10 reescrito · Saldo atual (vinheta: ESTOQUE FISCAL)
| Tela | Fala |
|---|---|
| Menu › "Estoque Fiscal": sub-aba "Saldo atual", "Saldo fiscal atualizado, por material. Não altera o estoque operacional."; tabela "Código", "Material", "Saldo fiscal". | Agora, o estoque fiscal: o estoque contado só pelas notas. Ele abre no Saldo atual, com o saldo fiscal de cada material. |
| Zoom na linha "Alumínio perfil" (o saldo já sem os 3.200 kg da nota de hoje). | Esse saldo se atualiza sozinho. As notas do alumínio que saíram hoje de manhã já estão descontadas aqui. |
| Digita "cobre" em "Buscar material ou código"; a tabela filtra; limpa a busca. | Pra achar um material, é só buscar pelo nome ou pelo código. |
| Zoom na faixa amarela "Alguns saldos foram apurados pelas notas disponíveis, pois ainda não têm saldo inicial informado." | Repara no aviso amarelo: tem material sem saldo inicial. Nesse caso, o sistema conta só pelas notas que ele conhece. |

`[BACKEND]` `get_fiscal_inventory_position` com `has_opening_balance: false` em um material (sugestão: a sucata de
bateria, que só entrou em 05/11 pela nota 2157) e `true` nos outros; a RPC é chamada de novo a cada 10 s.

### 3.6 Capítulo novo 10a · O saldo inicial (vinheta: ESTOQUE FISCAL)
| Tela | Fala |
|---|---|
| Na linha da sucata de bateria, menu "⋯" → "Informar saldo inicial": diálogo "Informar saldo inicial", "O saldo fica só no estoque fiscal e passa a ser a base dos movimentos posteriores." | Quando a empresa começa a usar o sistema, ela já tem material no pátio. Esse ponto de partida é o saldo inicial. Na linha do material, Informar saldo inicial. |
| "CNPJ" já escolhido; "Data-base" 01/08/2026; aba "Manual": "Material" já vem; digita a quantidade em "Quantidade". | Escolho a data-base, que é o dia em que esse número valia, e a quantidade. Uma dica: esse número é fiscal. No Lucro Real, o estoque entra no balanço, então combine o valor com o contador. |
| Clica na aba "Planilha": "Baixar modelo" e "Escolher planilha" (sem enviar); volta para "Manual". | Pra informar vários materiais de uma vez, tem a planilha: você baixa o modelo, preenche código e quantidade e envia. O sistema confere linha por linha antes de gravar. |
| Clica em "Confirmar saldo inicial": toast "Saldo inicial registrado"; a faixa amarela some. | Confirmar. O aviso amarelo some, e daqui pra frente as notas somam e descontam a partir desse saldo. |

`[BACKEND]` RPC `record_fiscal_inventory_entries` (`p_entry_type: "opening_balance"`); depois dela a posição devolve
`has_opening_balance: true`. Quantidade e data a definir na junção (não pode mudar número falado em outra aula).

### 3.7 cap10b · Posição em uma data e Movimentações (vinheta: ESTOQUE FISCAL)
| Tela | Fala |
|---|---|
| Sub-aba "Posição em uma data": "Posição do estoque em uma data"; em "Data e hora da posição", 31/10/2026 18:00; "Ver posição": "Saldo fiscal em 31/10/2026 às 18:00." | Pra ver um dia do passado, a aba é a Posição em uma data. Escolho o fim de outubro e clico em Ver posição. No Lucro Real, é o número que o contador pede no fechamento do mês e do ano. |
| A câmera fica na tabela. | Uma dica: essa posição é só consulta. Ela não muda saldo, nota nem o estoque de hoje. E a data é sempre do passado. |
| Sub-aba "Movimentações"; na lista "Materiais", "Metal amarelo (latão)": "KARDEX FISCAL — ...". | Em Movimentações fica o Kardex fiscal. Escolho o metal amarelo: cada linha é uma nota, com o CFOP, a quantidade e o saldo antes e depois. |
| Clica em "Filtros": "De", "Até", "Tipo" (abre: "Entrada", "Saída", "Saldo inicial", "Ajuste", "Estorno") e "Nota, chave ou parceiro". Escolhe "De" 01/10 e "Até" 31/10. | Nos filtros, dá pra fechar num período, num tipo de movimento, ou buscar por nota, chave ou parceiro. |
| "Limpar filtros"; clica em "Geral (Todos)". | E em Geral aparecem as movimentações de todos os materiais juntas. |

### 3.8 Capítulo novo 10c · Cancelamento e devolução (vinheta: ESTOQUE FISCAL)
| Tela | Fala |
|---|---|
| Em "Movimentações", material "Alumínio perfil"; filtro "Nota, chave ou parceiro" com "1249": duas linhas de 10/11, "Nota fiscal" 1249, CFOP 6102, −320 kg, e "Estorno" 1249, +320 kg, com o motivo "Pedido alterado pelo cliente antes de a mercadoria sair do pátio". [ZOOM: as duas linhas, colunas "Origem", "Movimento", "Antes", "Depois"] | E quando uma nota é cancelada? Lembra da nota mil duzentos e quarenta e nove, cancelada hoje cedo? A saída de trezentos e vinte quilos continua no Kardex, e logo abaixo entra o estorno, com o motivo do cancelamento. |
| [ILUSTRAÇÃO: uma régua do dia 10/11 com dois pontos: "Nota 1249 autorizada −320 kg" e "Cancelada +320 kg"; o saldo desce e volta.] | O sistema não apaga a nota. Ele devolve a quantidade na hora em que o cancelamento aconteceu. Assim, uma posição consultada entre os dois momentos mostra o saldo como era. |
| A ilustração sai; zoom na coluna "Depois" da linha do estorno. | O mesmo vale pra nota de fornecedor que foi cancelada depois de chegar: ela sai do saldo sozinha. |
| Limpa o filtro; material "Metal amarelo (latão)": a linha de hoje "Nota fiscal" nº 1254, CFOP 1202, +150 kg. [ZOOM: "CFOP 1202" e "+150"] (depende de D3) | E a devolução? A Fundição Bandeira do Vale devolveu cento e cinquenta quilos de metal amarelo. A nota de devolução entra no estoque fiscal como entrada. |
| [ILUSTRAÇÃO: duas setas com os rótulos "devolução de venda: volta pro estoque" e "devolução de compra: sai do estoque".] | Devolução de venda, o material volta. Devolução de compra, o material sai. E vale igual pra dentro e pra fora do estado. |
| A câmera volta ao Kardex. | Uma dica: no Lucro Real, a devolução também mexe nos impostos da nota original. Essa parte é com o contador. Aqui você confere a quantidade. |

`[BACKEND]` `get_fiscal_inventory_history_paged` com as linhas `movement_type: "reversal"` (motivo = `cancellation_reason`
da 1249, que a T16 cancela) e a nota de devolução (D3). A emissão da devolução é da T16: aqui só o efeito.

### 3.9 cap10d · Fiscal × operacional (acréscimos ao trecho atual)
| Tela | Fala |
|---|---|
| (depois da linha do metal amarelo e da ilustração) Zoom nos cartões "Materiais com divergência" e "Alertas". | Aqui em cima, o sistema conta quantos materiais deram diferença e quantos têm alerta, como saldo fiscal negativo. |
| Zoom no quadro "Como ler o Delta (fiscal − operacional)", linha "Delta negativo costuma indicar compra de pessoa física sem nota...". | A diferença mais comum no ferro-velho é esta: compra de pessoa física sem nota. O material entra no pátio, mas não entra no fiscal. |
| Zoom na linha "Pedidos ainda não finalizados...". | Uma dica: um não corrige o outro. Este quadro ajuda a achar o motivo de cada diferença. |
| Clica em "Exportar": "Exportar estoque fiscal" com "PDF" e "Excel" (sem baixar). | E dá pra exportar essa comparação em PDF ou em Excel e mandar junto pro contador. |

### 3.10 cap11 · acréscimos ao pacote
| Tela | Fala |
|---|---|
| (depois de "Período") A câmera passa por "Emitente / CNPJ" ("Todos os CNPJs"). | Se a empresa tem mais de um CNPJ, dá pra gerar um pacote pra cada um. |
| Marca "Incluir notas destinadas ao CNPJ"; zoom em "XMLs de NF-e emitidas por fornecedores contra a sua empresa. Entram na pasta “xmls/destinadas”."; na prévia, "Destinadas: 0 XML(s)". (ver D5) | Aqui tem uma opção importante pra quem está no Lucro Real: incluir as notas que os fornecedores emitiram contra o seu CNPJ. É com o XML delas que o contador aproveita os créditos. |
| Zoom na prévia. | Em outubro a Recicla Vale ainda não recebia essas notas pelo sistema, então vem zero. No pacote de novembro, elas já entram. |
| "Baixar Pacote": toast "Exportação pronta" / "12 saída + 9 entrada + 0 destinada(s) baixados". | (fala igual) |

cap12, primeira linha: acrescentar na ilustração a pasta "destinadas" e na fala "...e, se você marcou, as notas dos
fornecedores.".

## 4. Estimativa

| Bloco | Palavras de fala a mais | Segundos (2,6 palavras/s) |
|---|---|---|
| 3.0 ajustes | ~75 | ~29 |
| 3.1 nota pela chave | ~105 | ~40 |
| 3.2 CIOT | ~125 | ~48 |
| 3.3 contingência, cancelar, 05b | ~175 (troca ~35 da dica antiga) | ~54 líquidos |
| 3.4 relatórios | ~75 | ~29 |
| 3.5 saldo atual | ~65 (troca ~25) | ~15 líquidos |
| 3.6 saldo inicial | ~135 | ~52 |
| 3.7 posição e movimentações | ~85 (troca ~60) | ~10 líquidos |
| 3.8 cancelamento e devolução | ~185 | ~71 |
| 3.9 e 3.10 | ~125 | ~48 |
| **Total** | **~1.030 líquidas** | **~6 min 35 s de fala** |

Com vinhetas e esperas: de ~13 min para **~20 a 21 min**. **Capítulos novos: 3** (05b manifesto recusado, 10a saldo
inicial, 10c cancelamento e devolução); o cap10 atual se divide em três (saldo atual, posição e movimentações, fiscal ×
operacional). Ilustrações novas: 2 (régua do estorno, setas da devolução).

## 5. Depende de decisão
- **D1. Ajuda do CIOT.** O balão "Como gerar o CIOT?" traz o link "Gerar gratuitamente na eFrete" (marca de terceiro,
  `NovoMdfeModal.tsx:1608-1617`). Mostrar o balão, ou só falar da ANTT sem abrir?
- **D2. Manifesto recusado (05b).** Precisa de um MDF-e nº 2 "Rejeitado" na semente da tarde; muda o cartão "MDF-e
  Rejeitados" e a prévia de manifestos do pacote só se for de outubro (não é). Gravar com semente ou só citar numa frase?
- **D3. Devolução.** O mundo não tem devolução. Proposta: NF-e de entrada nº 1254, CFOP 1202, Fundição Bandeira do Vale,
  150 kg de metal amarelo, em 10/11 (número a conferir na junção: as duas notas do manifesto vêm depois da 1251). A emissão de devolução também não está na T16:
  conferir com a auditoria da T16 para os números baterem.
- **D4. SPED Fiscal.** É arquivo para o contador, mas está em BETA e fora do plano do mundo. Manter fora?
- **D5. Destinadas no pacote.** Mostrar com zero em outubro e explicar (proposto), ou semear XML de fornecedor em outubro
  (mexe na lista de Notas Recebidas da T16)?
- **D6. Junção do Fiscal × operacional (achado 4 de `propostas_fala.md`).** A proposta 3.9 assume a tela como ela é (vários
  materiais com divergência por compra de pessoa física sem nota) em vez de "só o metal amarelo". Confirmar.
- **D7. Quantidade e data-base do saldo inicial** da sucata de bateria (3.6): definir na junção.
- **Para `MELHORIAS_ECOSISTEMA.md`:** toast "enviado ao motor fiscal próprio" (M6); "Sincronizar Numeração" ainda fala em
  "serviço fiscal" (M2); alíquota do ISS do município que não chega à aba Valores (continua).
