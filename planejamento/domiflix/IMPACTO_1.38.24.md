# Impacto da Dominex 1.38.24 nas aulas da Domiflix

> Levantamento de 05/11/2026, só leitura. Compara `src-1.38.21` (main `a68adc13`, base das gravações atuais) com `src-1.38.24`
> (`origin/main` `2bc90726`). Cobre `e78d82c7` (fiscal: ambiente e convênio, #9), `c4db8f2d` (fiscal: upsert seguro, #10),
> `1c30c722` (1.38.23, planejar visitas individualmente) e `2bc90726` (1.38.24, vincular OS existente ao cronograma).
> Análise estática do código e das migrações: **nada foi rodado**. O que só se confirma na tela está marcado "(a confirmar)".
> Caminhos de código são relativos a `src-1.38.24/src/` (exceto `supabase/...`). Linhas de roteiro: `Tnn/roteiro.md:linha`.
> Nenhum `roteiro.md` nem `tts_textos.py` foi alterado: as falas novas ficam só neste arquivo.
>
> Legenda: **(a)** nada visível muda · **(b)** só o robô muda (rótulo, posição, passo novo; fala intacta) · **(c)** a fala muda ·
> **(d)** aula entregue mostra o que não existe mais ou confunde.

## 1. Resumo

| Aula | Estado | Classe | Falas que mudam | Observação curta |
|---|---|---|---|---|
| T0 / T0 v2, T1, T2, T3 v2, T4 | entregues | (a) | 0 | Nada de Configurações, permissões, cadastros ou serviços mudou |
| T5 | entregue | **(b)** leve (L84) | 0 (1 opcional) | Planner "Jornadas por dia" ganha "Adicionar outra data", "Adicionar dia" e a lixeira por dia; texto de apoio novo |
| **T7** (regravar com cap14) | a regravar | **(b)** no cap14 | 0 (1 leve opcional) | `EditOsScopeDrawer`: só a aba "Data e horários" ganha os mesmos controles; aba "Equipamentos" intacta |
| T8, T9, T10, T13, T15, T17, T18, T19, T20, T21, T22 | vários | (a) | 0 | Nenhum arquivo que essas aulas mostram mudou (conferido contra as linhas de contrato/OS de cada roteiro) |
| **T11** | **gravando, pausado** | **(c) só no cap10**; resto (a) | **1 trocada + 2 novas (opcionais)** | Aba "Ocorrências" refeita; assistente, PMOC, Documentos, Renovar e Excluir iguais |
| T12 | voz pronta | (a) | 0 | Portal público não mudou; a faixa "Dados faltando" do cap08 **continua** (seção 3) |
| **T14** | não gravado | por capítulo (seção 6) | não reescrito | Verificar município agora depende do certificado; notas ganham ambiente fixo |

## 2. T11 · Contratos e PMOC (urgente)

### 2.1 O que mudou no app que importa

| Commit | Efeito |
|---|---|
| `1c30c722` (1.38.23) | `pages/ContractDetail.tsx`, aba Ocorrências: colunas "Data" e "Dia" viram **"Prevista"** e **"Agenda"** (a Agenda mostra uma etiqueta por data, ex.: "01/12 · ter"); botão **"Planejar visita"** em cada linha "Agendada" ou "Pendente" (abre o `ServiceOrderFormDialog` em edição, com o cliente travado e sem a pergunta "só esta ou esta e as próximas"); selo **"Planejada"** na visita personalizada; estado vazio "Nenhuma visita gerada". Colunas novas no banco: `service_orders.contract_reference_date` e `contract_visit_customized_at` |
| `2bc90726` (1.38.24) | Botão **"Vincular OS existente"** ao lado do título da aba Ocorrências (contrato ativo e permissão); novo `components/service-orders/LinkExistingServiceOrderDialog.tsx`; selo **"Vinculada"**; RPC `link_service_order_to_contract`. `VERSION_NOTES` novo |
| Os dois | Assistente "Novo Contrato" (`ContractFormDialog`), `visitScheduleEngine`, `contracts.ts` (i18n) e `pmoc.ts` fora das chaves de Ocorrências **não mudaram**. Só a criação passa a gravar `contract_reference_date` em cada OS (igual à data da visita), sem efeito na tela |

Rótulos novos exatos (`lib/i18n/messages/app/pmoc.ts`, bloco `contractDetail.occurrences`):
`colReference` "Prevista" · `colSchedule` "Agenda" · `planAction` "Planejar visita" · `loadingAction` "Carregando..." · `plannedBadge` "Planejada" · `linkedBadge` "Vinculada" ·
`planDialogTitle` "Planejar visita do contrato" · `planDialogDescription` "Ajuste esta visita sem alterar as demais datas do contrato." ·
`linkAction` "Vincular OS existente" · `linkDialogTitle` "Vincular OS existente ao contrato" · `linkDialogDescription` "Escolha uma OS deste cliente e a competência do cronograma que ela representa." ·
`linkKeepsHistoryTitle` "O histórico original será preservado" · `linkOrderLabel` "Ordem de Serviço" · `linkSearchPlaceholder` "Buscar por número, serviço, equipamento ou status..." ·
`linkPeriodLabel` "Competência do contrato" · `linkPeriodPlaceholder` "Selecione a visita do cronograma" · `linkPeriodHelp` "A visita automática vazia será substituída pela OS escolhida." ·
`linkReplaceOs` "substitui OS #{número}" · `linkSubmit` "Vincular OS" · `linkCancel` "Cancelar" · `linkSuccessTitle` "OS vinculada ao contrato" · `referenceLabel` "Prevista no contrato" e `scheduledLabel` "Agenda da visita" (só no celular).
Em `os.ts` (`app.os.form`): `scheduleAddDate` "Adicionar outra data" · `scheduleAddDay` "Adicionar dia" · `scheduleRemoveDay` "Remover este dia" · `dailyScheduleHelp` "Monte o período, remova dias inadequados ou adicione datas avulsas. Máximo de 31 dias." · `contractCustomerLocked` "O cliente é definido pelo contrato e não pode ser trocado nesta visita."

### 2.2 Capítulo por capítulo

| Cap | Classe | Linhas | O que a tela mostra agora | Fala |
|---|---|---|---|---|
| 00 Abertura | (a) | 41 a 46 | Igual | Mantém |
| 01 Onde fica o PMOC | (a) | 51 a 55 | Lista, "Filtros", "Tipo" iguais | Mantém |
| 02 O Responsável Técnico | (a) | 60 a 65 | Configurações de Contrato iguais | Mantém |
| 03 Um contrato comum | (a) | 71 a 77 | Cinco etapas, "Prévia das datas (5)" (L74) e "Revisão" (L77) **idênticas**; "Criar Contrato (5 OSs)" e os avisos iguais | Mantém |
| 04 a 09 (PMOC) | (a) | 83 a 138 | Etapa "Agenda" com "Cadência das visitas" e "Prévia das datas (13)" (L114 a L118), "Revisão" (L135) e criação (L137) idênticas | Mantém |
| **10 O contrato por dentro** | **(c)** | **147** (e 145, ver abaixo) | Ver abaixo | **Troca 1 fala** + 2 novas opcionais |
| 10, demais linhas | (a) | 144, 145, 146, 148 a 150 | Visão Geral, "Ambientes e Equipamentos", "Histórico PMOC" e "Financeiro" iguais | Mantém |
| 11 Cronograma | (a) | 156 a 159 | Calendário e "Imprimir PDF Anual" iguais | Mantém |
| 12 Documentos | (a) | 165 a 170 | Iguais, **mas a faixa "Dados faltando pra gerar documentos PMOC" aparece** (seção 3) | Mantém |
| 13 Renovar, pausar e excluir | (a) | 176 a 178 | "Renovar / Estender" e "Excluir contrato" iguais (as contas internas da renovação mudam para usar a data prevista, sem efeito visível) | Mantém |
| 14 Recapitulando | (b) | 187 | A montagem rápida de "Ocorrências" usa a tela nova | Mantém (ver 2.4) |

**Cap10, L147 (Ocorrências), tela nova.** Clique em "Ocorrências": título "Ocorrências (13)" com o botão **"Vincular OS existente"** à direita; tabela **"#", "Prevista", "Agenda", "OS", "Serviços", "Status" e "Ações"**. "Prevista" traz dd/MM/aaaa; "Agenda" traz uma etiqueta por data de execução (ex.: "01/12 · ter"); em "Ações" cada linha tem **"Planejar visita"** (borda, ícone de lápis) e o botão de pular (lixeira, dica "Pular (cancelar esta visita)"). Os dois botões novos ficam desativados com "Carregando..." enquanto a lista de OS carrega.

**Fala atual (L147):** "Em Ocorrências, todas as visitas do contrato, cada uma com data, dia da semana e ordem de serviço. Cada visita é uma ordem de serviço normal na agenda. Se uma não vai acontecer, o Pular cancela só ela."
Hoje a primeira frase cita "Data" e "Dia", colunas que não existem mais. **Proposta (substitui a frase inicial, resto igual):**

> Em Ocorrências, todas as visitas do contrato. A coluna Prevista traz a data do cronograma, e a Agenda mostra quando cada visita está marcada, com o dia da semana. Cada visita é uma ordem de serviço normal na agenda. Se uma não vai acontecer, o Pular cancela só ela.

### 2.3 A aula fica desatualizada sem "planejar visitas" e "vincular OS existente"?

**Errada não fica; desatualizada fica.** Com a troca da fala acima, nada do que é dito deixa de ser verdade. Mas a tela passa a mostrar, na mesma linha onde a câmera passa pelo "Pular", dois botões novos ("Planejar visita" em toda linha e "Vincular OS existente" ao lado do título) que a voz ignora, e são justamente as duas novidades das versões 1.38.23 e 1.38.24. Recomendo **mostrar, com ~50 s de voz a mais, dentro do cap10, sem criar capítulo nem renumerar**, no estilo "mostra e cancela" do cap13 (o mundo fica intacto para o T12, que espera OS #1 a #33).

Duas linhas novas, depois de L147 e antes de L148 ("Ambientes e Equipamentos"):

| Tela | Fala proposta |
|---|---|
| Na linha da primeira visita, clique em **"Planejar visita"**: abre **"Planejar visita do contrato"** ("Ajuste esta visita sem alterar as demais datas do contrato."), etapa "Atendimento e orçamento" com o cliente travado ("O cliente é definido pelo contrato e não pode ser trocado nesta visita."); clique em "Próximo" até "Equipe e agenda" e zoom em "Período do atendimento", "Jornadas por dia", "Adicionar outra data" e "Adicionar dia" (a lixeira "Remover este dia" só fica ativa com mais de um dia); clique em "Cancelar". | Se uma visita precisa mudar, é só clicar em Planejar visita. Abre só aquela visita, e dá pra ajustar a equipe, os horários, as observações e as datas, até em dias que não são seguidos, com o Adicionar dia. As outras visitas do contrato não mudam. Aqui eu só mostro e cancelo. |
| Clique em **"Vincular OS existente"**: abre **"Vincular OS existente ao contrato"**, com o aviso "O histórico original será preservado", a lista em "Ordem de Serviço" (busca "Buscar por número, serviço, equipamento ou status...") e, depois de marcar uma OS, o seletor **"Competência do contrato"** ("Selecione a visita do cronograma", itens como "01/12/2026 · substitui OS #22"); zoom no botão "Vincular OS" (sem clicar); clique em "Cancelar". | E se a ordem de serviço já existia antes do contrato? Em Vincular OS existente, escolho a ordem desse cliente e a visita do cronograma que ela vai representar. O número, o status e as datas reais continuam iguais, e só a visita automática ainda vazia daquela data é substituída. Aqui também eu só mostro e fecho em Cancelar. |

Notas para o robô (a confirmar):
- A lista só traz OS do mesmo cliente, que não sejam do próprio contrato, nem canceladas, nem "tarefa" (`lib/contractServiceOrderLinking.ts`). O Hotel Mirante do Mar tem uma OS avulsa na semente do T5 (a "A Caminho" do Bruno Alves, entre as #1 a #15); conferir que ela segue ali e sem contrato, senão a janela mostra "Nenhuma OS disponível". A "Competência" só lista visitas "Agendada" ou "Pendente" sem planejamento.
- Todo o carregamento depende de `GET service_orders` responder na página do contrato; se falhar, aparece o alerta "Planejamento temporariamente indisponível" e os dois botões ficam desativados. Esperar o fim de "Carregando..." antes de clicar.
- Fakebase: regerar o schema (`service_orders.contract_reference_date` e `contract_visit_customized_at`) e aceitar essas colunas no `select` do detalhe do contrato e no `INSERT` das OS do contrato. As sementes `apos-cap09` sem as colunas funcionam (o app cai na data agendada). Nenhum clique grava, então a RPC `link_service_order_to_contract` não precisa de handler se o plano acima for mantido.
- Opção mínima, se o Kaik preferir não aumentar a aula: só a troca da fala da L147 (zoom das colunas sem passar pelos botões novos). Fica correta, mas deixa as duas novidades sem explicação.

### 2.4 Quais capítulos já gravados na 1.38.21 ainda servem

Servem sem regravar: **cap00 a cap09, cap11, cap12 e cap13**. A diferença de versão não aparece em tela nenhuma desses capítulos. **Regravar: cap10** (só o trecho da aba "Ocorrências", mas a gravação é por capítulo). **Cap14** (montagem rápida): refazer só o corte da aba "Ocorrências" com a tela nova, fala igual (já cobre "acompanha as ocorrências"). Se o cap10 for gravado na 1.38.24 e os outros na 1.38.21, o resto da página (abas, cartões) é idêntico, então não há emenda visível entre capítulos.

## 3. A faixa "Dados faltando pra gerar documentos PMOC" (Endereço do cliente)

**Não foi corrigida na 1.38.24.** `hooks/useContractDetail.ts:42` continua com `customers (id, name, document, phone)`, sem `address`, `city` e `state`. `pages/ContractDetail.tsx:1576` monta `customer_address` a partir desses três campos (`customerExtra.address, .city, .state`), que chegam vazios, e `components/pmoc/PmocContractDocsTab.tsx:480` (arquivo idêntico nas duas versões) lista "Endereço do cliente — complete no cadastro do cliente" sob o título "Dados faltando pra gerar documentos PMOC". Nenhuma migração nem commit novo toca nisso (o `useContractDetail.ts` só ganhou colunas de `service_orders`). Portanto **T12 cap08 e T11 cap12 não podem ser regravados sem a faixa só por atualizar a versão**.

Saídas (decisão do Kaik): (1) deixar a faixa e ajustar a fala, já que a L165 do T11 e o cap08 do T12 dizem "se faltar algo, a aba mostra o atalho"; a L165 do T11 afirma "nenhum aviso... o mundo já está completo", o que o app contradiz; (2) no fakebase, devolver `address`, `city` e `state` dentro de `customers` no embed de `GET contracts` mesmo fora do `select` (a confirmar se o fakebase respeita o `select`); (3) corrigir o app (acrescentar os três campos na linha 42), o que é código do app e fica fora desta tarefa.

## 4. T5 · Ordens de Serviço (entregue)

O assistente "Nova Ordem de Serviço" mantém **todos os textos em português** (`ServiceOrderFormDialog.tsx` só moveu strings fixas para o i18n: "Atendimento", "Serviços e orçamento", "Escopo técnico", "Equipe e agenda", "Revisão", "Resumo da OS", "Precificação da OS", sem mudança de redação). Única mudança visível: o planner da etapa "Equipe e agenda".

| Linha | Classe | Tela agora | Fala |
|---|---|---|---|
| 82, 88, 94 | (a) | Etapas, "Revisão", Recorrência iguais | Mantém |
| **84** | **(b)** | Em "Período do atendimento": o texto de apoio passa a "Monte o período, remova dias inadequados ou adicione datas avulsas. Máximo de 31 dias."; entre "Data final" e a lista aparece o seletor **"Adicionar outra data"** com o botão **"Adicionar dia"**; cada dia de "Jornadas por dia" ganha a lixeira "Remover este dia" (desativada com um dia só, como na aula) | Mantém: "Se o serviço dura mais de um dia, dá pra marcar o período inteiro, com o horário de cada dia" continua certa. **Opcional:** "...com o horário de cada dia. Também dá pra acrescentar uma data avulsa, no Adicionar dia." (não recomendo regravar só por isso) |

Efeito no robô: o enquadramento do zoom em "Jornadas por dia" muda de altura (uma linha a mais); conferir o recorte. No modo edição da OS, os campos da etapa "Escopo técnico" ficam desativados até o escopo carregar ("Carregando equipamentos e checklists desta OS..."); a aula T5 não edita OS, então não afeta.

## 5. T7 · Editar OS em campo (regravar inteiro, com cap14)

`EditOsScopeDrawer.tsx` mudou em **3 linhas**: ele passa a repassar ao `ServiceOrderSchedulePlanner` os rótulos `addDate`, `addDay` e `removeDay` (de `app.os.form`). Nada na aba de equipamentos e checklists: o arrasto, "Adicionar equipamento", "Selecionar checklists", "Remover equipamento", "Salvar equipamentos e checklists", a confirmação de remoção e o aviso "OS atualizada" são os mesmos (`useEditOsScope`, `editOsScopeState` e a RPC `edit_service_order_scope` não mudaram).

| Linha (`T07/roteiro.md`) | Classe | Tela agora | Fala |
|---|---|---|---|
| 159 a 166 (aba "Equipamentos") | (a) | Igual | Mantém |
| **167** (aba "Data e horários") | **(b)** + (c) leve opcional | "Período da OS", "Data inicial", "Data final", **"Adicionar outra data"** com **"Adicionar dia"**, "Horário de cada dia" ("1 dia agendado"), com a lixeira **"Remover este dia"** desativada (um dia só) | Atual: "Na outra aba, Data e horários, o técnico remarca a ordem sem sair do preenchimento: a data, e o início e o fim de cada dia." **Proposta opcional:** "Na outra aba, Data e horários, o técnico remarca a ordem sem sair do preenchimento: a data, e o início e o fim de cada dia, e ainda pode acrescentar uma data avulsa ou tirar um dia. Lembrando que a edição precisa de internet: sem conexão, o Editar OS aparece desativado, com o aviso Disponível apenas online." (+~90 caracteres de voz; como a fala do cap14 ainda vai ser gerada, vale já entrar) |

**Afeta o cap14?** Só a imagem da L167 (sem tocar, só zoom). A voz do cap14 ainda não foi gerada (aula a regravar), então a proposta custa quase nada agora.

## 6. T12 e T13

| Aula | Classe | Observação |
|---|---|---|
| **T12** Portal do Cliente e Portal do Contrato | **(a)** | Portal público (`pmoc-portal-share`) e páginas do portal não mudaram. Cap07 (L108) e cap09 a cap11 (L125 a L130) iguais. **Cap08 (L117 a L119)**: faixa de endereço continua (seção 3) |
| **T13** Financeiro | **(a)** | Nada de Financeiro mudou. Só cita o contrato como categoria "Contratos PMOC" |

## 7. T14 · Notas Fiscais (só classificação; não reescrito)

O que `e78d82c7` (#9) e `c4db8f2d` (#10) tocam, em termos de tela e de robô:

- **Tela, `pages/FiscalSettings.tsx` e `components/fiscal/EmpresaSection.tsx` (#9):** "Verificar cobertura do município" fica **desativado sem certificado válido**, com o texto novo "Envie um certificado A1 válido antes de consultar a habilitação oficial do município." (`nfse.ts`, `coverageNeedsCertificate`). Clicar na linha de status do município sem certificado leva à aba do certificado. "Salvar" dos dados da empresa sem certificado leva à aba do certificado. Depois de "Enviar certificado" com o município preenchido, o app volta à aba "Empresa" e roda a verificação em silêncio (sem aviso "Município liberado para emissão de NFS-e.").
- **Servidor (#9), sem efeito visível se o backend falso imitar:** `fiscal_ambiente` obrigatório para emitir ("fiscal_environment_invalid"); nova coluna `nfse_emissions.fiscal_ambiente`, fixa por nota, usada por consultar, cancelar e baixar PDF (nota sem ambiente devolve 409 "fiscal_environment_unknown"); a cota de emissão só vale em Produção; `upload-certificate` exige que o CNPJ do certificado seja o da empresa; erro 503 deixa de significar "não configurado" em `utils/nfseEdge.ts`.
- **#10:** só migração de permissão (`GRANT UPDATE (company_id)`), sem tela.

| Cap (`T14/roteiro.md`) | Classe | Motivo |
|---|---|---|
| 02 Dados da empresa (L60 a L65) | **(c)** | O botão "Verificar cobertura do município" (L64) não pode mais ser clicado antes do certificado; a ordem da aula (verificar, depois salvar) muda. (L61 a L63 seguem dependendo da reescrita da 1.38.21: sem "registro") |
| 03 Certificado (L71 a L75) | **(c)** | Após "Enviar certificado" a tela volta para "Empresa" e confirma o município sozinha |
| 04 a 06 | (a) | Tributação, serviços e pessoas não mudaram |
| 07 Emissão (L110) | **(b)** | O `nfse-emit` do fakebase deve gravar `fiscal_ambiente` "homologacao" na nota |
| 08 a 10 | **(b)** | `nfse-status`, `nfse-cancel`, `nfse-danfse` e a nota automática dependem de `fiscal_ambiente` na semente das notas; sem ele, o servidor real devolveria 409 |
| 11 a 13 | (a) | Notas recebidas e recap sem mudança |

Fakebase: regerar o schema (`nfse_emissions.fiscal_ambiente`; mais as colunas de `service_orders` da seção 2.3). O certificado fictício continua sendo decisão do fakebase (o servidor real agora rejeitaria CNPJ divergente; o backend falso não precisa imitar).

## 8. Riscos transversais (somam aos G1 a G9 dos levantamentos anteriores)

**G10. Gaveta "novidades da versão".** Se alguma gravação passar a rodar a **1.38.24**, o `VERSION_NOTES` novo ("Ordens de Serviço já cadastradas agora podem ser vinculadas às visitas do contrato sem perder datas, status ou histórico.") abre a gaveta quando a versão vista é diferente da atual. O `setup` deve ler `APP_VERSION` em vez de número fixo (mesmo cuidado do G7).

**G11. Schema do fakebase.** Regerar `rec/fakebase/tools/gen-schema.mjs` apontando para `src-1.38.24`: `service_orders` ganha `contract_reference_date` (date) e `contract_visit_customized_at` (timestamptz); `nfse_emissions` ganha `fiscal_ambiente`; RPC nova `link_service_order_to_contract(p_service_order_id, p_contract_id, p_reference_date)`. Tarefas pesadas sob `flock $TUT_HOME/.heavy.lock`.

**G12. Permissões.** "Planejar visita" aparece para admin, gestor ou `fn:edit_os`; "Vincular OS existente" para admin, gestor, super admin ou `fn:manage_contracts` (e contrato "Ativo"). Camila (admin) vê os dois. Nenhuma aula esconde botão por permissão nesse ponto.

## 9. Demais aulas (confirmação)

T0, T0 v2, T1, T2, T3 v2, T4, T8, T9, T10, T13, T15, T17, T18, T19, T20, T21, T22: **(a)**, sem falas novas. T19 mostra a aba "Financeiro" do contrato (L162) e T10 o CRM; nenhuma dessas telas mudou. Os únicos arquivos do app alterados fora de contratos, OS e fiscal foram `config/version.ts` e `pages/Changelog.tsx` (novas entradas 1.38.23 e 1.38.24), que nenhuma aula mostra.

## 10. Decisões pendentes para o Kaik

1. T11 cap10: incluir os dois trechos novos (+~50 s de voz) ou só trocar a fala da L147.
2. Faixa "Endereço do cliente": mostrar e ajustar a fala, esconder pelo fakebase, ou pedir o conserto no app.
3. T7 cap14 L167 e T5 L84: aceitar as frases opcionais (T7 sim, T5 não).
