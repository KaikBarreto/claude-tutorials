# T7 · O técnico em campo · inventário do app 1.38.6

Levantamento feito em 30/10/2026 sobre `/home/claude/domiflix/src-1.38.6` (somente leitura; só análise estática, o app e o backend falso não foram executados). Convenções:

- Caminhos `arquivo:linha` são relativos a `src/` da 1.38.6 (ex.: `pages/TechnicianOS.tsx:3911`). `rec/...` = `/home/claude/domiflix/rec/`. `supabase/...` = raiz do repositório extraído (migrations).
- `TechnicianOS.tsx` = `pages/TechnicianOS.tsx` (5.011 linhas; a tela inteira vive nele e em `components/technician/*`). `os.ts` = `lib/i18n/messages/app/os.ts`; blocos usados aqui (pt-br): `technicianFlow` (`os.ts:797-1007`), `stockConsumption` (`:1012-1092`), `publicView` (`:1262-1289`), `osPhotoField` (`:1399`), `osVideo` (`:1541-1564`), `dynamicForm` (`:1567-1597`), `osDocumentReport` (`:1705-1760`).
- Rótulos entre aspas estão EXATOS como aparecem na tela. Onde o texto é fixo no componente (fora do i18n), a linha do componente é a fonte; os textos do `SignaturePad` ("Tela cheia", "Limpar", "Confirmar") e da pesquisa de avaliação não estão no i18n.
- O app que o robô usa é a 1.38.5; as telas de T7 não foram comparadas byte a byte com a 1.38.5 (Dúvida 7.1).
- O guia técnico do app e a trilha embutida em `docs/domiflix/trilha-de-tutoriais.md` são idênticos à 1.22.5: não servem de verificação do que mudou. O código manda.
- **T7 é a aula do celular.** Tudo que é `lg:` (1024 px para cima) muda de forma: o computador ganha uma coluna "Equipamentos" e um rodapé de ações próprios (`components/technician/OsDesktopShell.tsx:69-160`). Este inventário descreve o CELULAR (menos de 1024 px) e anota onde o computador difere.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (1.22.5) × código de hoje

| # | Capítulo da trilha 1.22.5 | Situação na 1.38.6 | Evidência |
|---|---|---|---|
| 1 | Abrindo a OS no celular: o link, o endereço amigável e o que o técnico vê primeiro | **Bate, com ajustes.** É uma página só (`/os-tecnico/:id`) para técnico, gestor e cliente; o técnico chega pelo botão "Preencher OS" (painel da Agenda ou detalhe da OS). O "endereço amigável" (`/os-tecnico/<cliente>-<serviço>-<código>`) só nasce se a OS tem `public_short_code`. A primeira tela é o cabeçalho (empresa, "OS #16", tipo, "Serviços desta OS", data e hora, selo de status) e o cartão "Ir para o Atendimento". | `App.tsx:742`; `TechnicianOS.tsx:460-463, 1022-1042, 1233-1242, 3670-3768, 3911-3941`; `ScheduleDetailPanel.tsx:365-371`; `utils/shareLinks.ts:27-45` |
| 2 | **A Caminho** → mapa em tela cheia com botão pra Waze e Google Maps | **Bate.** "A Caminho" é opcional (o check-in também sai de "Pendente"/"Agendada"). Cartão "Rota até o cliente" com mapa, "Ampliar", "Waze" e "Google Maps"; Waze e Maps abrem janela nova. | `TechnicianOS.tsx:3494-3562, 3794-3907`; `components/schedule/RouteToCustomerMap.tsx:241`; `utils/geolocation.ts:89-170`; `os.ts:813-820` |
| 3 | **Check-in**: a OS vira "Em Andamento" e a localização é registrada | **Bate.** Pede a posição do aparelho; grava hora, local e autor; mostra "Check-in: dd/MM/yyyy às HH:mm" + endereço; aparece o rodapé preto com "Finalizar OS" e "Finalizar Parcial". | `TechnicianOS.tsx:1631-1683, 1744-1797, 3963-3982, 4694-4761` |
| 4 | Preenchendo checklist por equipamento: conformidade, medição, seleção e observação | **Mudou.** Um acordeão por equipamento (foto, nome, categoria, serviços, contador "X de Y"), com o checklist dentro. "Medição" existe só como "Medida PMOC" (T11); o modelo da aula usa Sim/Não, Número (sem unidade na tela), Seleção, Foto, Texto e Assinatura; "Conformidade" é um tipo que este modelo não usa. | `TechnicianOS.tsx:173-440, 4063-4140`; `components/technician/DynamicFormQuestions.tsx:537-775, 944-1055`; `data/checklistCatalog.ts:94-113` |
| 5 | **Fotos e vídeo**: câmera, galeria e evidências do atendimento | **Bate, com ajustes.** Foto: "Tirar Foto" (câmera) e "Galeria", envio 3 por vez com barra, janela "Salvar foto no aparelho?" só no caminho da câmera. Vídeo: clipe de até 30 s e 50 MB, com compressão; **o checklist da aula não tem pergunta de vídeo**. | `OsPhotoField.tsx:96-310`; `OsVideoField.tsx:16-33`; `os.ts:1399-1424, 1541-1564` |
| 6 | **Consumo de estoque**: lançar o material usado dentro da OS | **Bate.** Menu ⋮ › "Consumir do estoque"; só anota; a baixa acontece ao finalizar. Depende do interruptor da empresa. | `TechnicianOS.tsx:817, 4581-4692`; `components/service-orders/OsConsumeStockDialog.tsx`; `hooks/useOsMaterials.ts:454-464`; `os.ts:1012-1092` |
| 7 | **Pausar** e retomar a OS — e como isso aparece na agenda do gestor | **Bate.** Pausar não pede confirmação; cartão "OS Pausada"; checklist travado com aviso; "Retomar OS" no rodapé. | `TechnicianOS.tsx:3322-3347, 3945-3960, 4073-4077, 4704-4712` |
| 8 | **Assinatura** do técnico e do cliente | **Não bate como está escrito.** O cartão "Assinaturas" (técnico + cliente) só existe quando a OS exige, e nenhuma tela liga essa exigência numa OS comum. A assinatura da aula é a **pergunta do checklist** "Assinatura do cliente" (obrigatória no modelo). | `TechnicianOS.tsx:4242-4308`; `ServiceOrderFormDialog.tsx:199-200, 456`; `hooks/useContracts.ts:1200`; `components/SignaturePad.tsx:188-337` |
| 9 | **Finalizar parcialmente** uma visita de contrato e preservar o que ficou pendente | **Mudou.** O botão "Finalizar Parcial" aparece em **qualquer** OS em atendimento (não só contrato); não valida nada, não faz check-out, marca "Parcialmente Concluída" e **sai da tela**. Existe desde a 1.14.19. | `TechnicianOS.tsx:3353-3370, 4730-4738, 4845-4877`; `types/database.ts:419-438`; `pages/Changelog.tsx:7149-7155` |
| 10 | Revisar o consumo de estoque e concluir a OS | **Bate, com ajustes.** Com material lançado, o "Resumo do consumo" **substitui** a pergunta "Finalizar OS?"; sem material, sai a pergunta de sempre. Depois, a pergunta de receita só aparece para quem tem permissão. | `TechnicianOS.tsx:1806-1927, 1938-2054, 4801-4910`; `components/service-orders/OsConsumptionSummaryDialog.tsx`; `hooks/useCanLaunchOsRevenue.ts` |
| 11 | Copiar o **link público** e conferir a visão do cliente sem login | **Bate, com nuances.** Com `?modo=cliente` a página vira a visão do cliente **mesmo com sessão**. Mostra status, técnico, execução, respostas do checklist, fotos e, ao concluir, o relatório + a pesquisa "Como foi seu atendimento?". O endereço copiado é sempre `https://dominex.app/...`. | `TechnicianOS.tsx:460-463, 966-983, 2680-3312`; `components/technician/OSRatingSurvey.tsx`; `utils/shareLinks.ts:27-45` |
| 12 | Baixar e compartilhar o **PDF** do relatório da OS | **Bate em parte.** Há "Baixar PDF", "Imprimir" e "Copiar Link"; **não há botão de compartilhar** o PDF (quem manda é a pessoa, com o arquivo baixado). O PDF é montado no navegador. | `OSReport.tsx:829-865, 1579-1628`; `utils/pdfPageRenderer.ts:488`; `os.ts:1705-1760` |

### 0.2 O que mudou desde a 1.22.5 (datado pelo changelog embutido em `pages/Changelog.tsx`)
- **1.23.0** (`:4572`) consumo de estoque direto na OS; "Estoque nunca impede fechar a ordem de serviço"; custo dos materiais na visão da OS.
- **1.24.21** (`:3991`) PDF gerado pelo celular sai com todas as fotos. **1.24.23** (`:3937`) pergunta "Houve alguma receita…" ao concluir. **1.24.35** (`:3638`) fuso da empresa em todo o sistema, inclusive o carimbo da assinatura. **1.24.50** (`:3313`) o link público passa a mandar só o que o relatório usa (sem valores de mão de obra e peças).
- **1.25.11** (`:2778`) o relatório mostra quem realmente fez o check-in e o check-out.
- **1.29.0** (`:2207`) Perguntas em Vídeo em todos os planos. **1.32.6-1.32.8** (`:1875-1905`) nome do checklist fixo no topo; vídeo pesado é comprimido ("Deixando o vídeo mais leve..."). **1.33.0** (`:1848`) fotos sobem 3 por vez; a que já subiu não se perde.
- **1.33.5** (`:1788`) atalho de WhatsApp com o cliente também no app do técnico. **1.35.0** (`:1742`) avisos automáticos de WhatsApp (a caminho, início, fim): T21.
- **1.36.3-1.36.5** "Resetar OS", também durante o atendimento (T5). **1.36.4** (`:1573`) logo da empresa na prévia do link. **1.36.23** (`:1195`) serviço e checklist **por equipamento** na tela do técnico.
- **1.37.0** (`:1111`) o cliente volta a ver o técnico no mapa do link (RPC leve). **1.37.29** (`:633`) campo de texto do checklist não fecha mais ao digitar. **1.37.36** (`:489`) check-in não trava por responsável arquivado. **1.37.47** (`:277`) link de OS respeita a separação de tarefas internas. **1.37.49** (`:248`) lembrete de WhatsApp pode levar o link de acompanhamento (T21).
- **Sem mudança de tela na 1.38.5/1.38.6** para T7 (as duas versões só mexem em cadastros, buscas e DRE, `Changelog.tsx:45-57`).

### 0.3 O que o roteiro precisa saber antes de escrever
1. **Gravar no celular é decisão de projeto, não só de viewport.** Abaixo de 1024 px a página usa pilha de cartões, cabeçalho fixo na cor da marca e rodapé preto; a partir de 1024 px vira três colunas com a barra "Equipamentos" à esquerda e rodapé de ações branco (`OsDesktopShell.tsx:69-160`). O robô de hoje grava 1280×800 (`rec/recorder/browser.mjs:11-13`) e mostraria o desenho do computador. A trilha manda gravar no celular (seção 4.9).
2. **Sem posição do aparelho nada anda.** "A Caminho", "Fazer Check-in" e "Finalizar" pedem a localização (15 s em alta precisão, depois 30 s em baixa) e, se faltar, mostram um aviso explicando (`TechnicianOS.tsx:1631-1683`; `os.ts:945-952`).
3. **Não existe rascunho nem offline na tela do técnico.** Cada resposta grava na hora (texto e número ao sair do campo). Sem internet aparece uma faixa vermelha e nada salva. A única coisa que o aparelho guarda é a lista de materiais lançados sem rede (P1).
4. **A assinatura do cliente na aula é uma pergunta do checklist**, não o cartão "Assinaturas". O cartão só aparece em OS de contrato/PMOC ou criada pela API (P2).
5. **"Finalizar Parcial" existe em toda OS em atendimento**, não faz check-out e fecha a tela. A trilha dizia que era "própria de contrato" (P3).
6. **O interruptor Sim/Não grava "Sim" no primeiro toque.** Para responder "Não" é preciso tocar no lápis e desligar (P7). A faixa "Checklist incompleto" marca o que faltar como "Sim/Conforme" (P8).
7. **Consumo de estoque só anota; o estoque só baixa ao finalizar**, e o resumo do consumo toma o lugar do "Finalizar OS?" (P12). O estoque nunca impede o fechamento.
8. **A linha de avaliação (`service_ratings`) nasce SEMPRE ao finalizar**, mesmo se a OS foi criada com "Gerar Pesquisa de Satisfação" = Não (P14; liga com T5 P7). O cliente só avalia pelo link público.
9. **PDF, Waze, Google Maps e "Imprimir" saem da página** (download, janela nova, caixa de impressão): o robô não captura (P16).
10. **O link copiado aponta para `https://dominex.app/...`**, não para onde o app está rodando (P15). Na gravação, a visão do cliente é aberta pela URL local.
11. **Rafael Lima (técnico) sem permissões gravadas vê tudo, inclusive "Editar OS"** no menu (P17). Já a pergunta de receita não aparece para ele (P13).
12. **O botão flutuante "Área do Técnico™" fica sempre no canto da tela** para empresas de refrigeração e abre as ferramentas da T18 (P18).

---

## 1. Rotas e navegação

| Tela / modo | Como se chega | URL (pt-br) | Componente | Guarda |
|---|---|---|---|---|
| Execução (técnico logado) | Agenda › clicar na OS › "Preencher OS"; Ordens de Serviço › detalhe › "Preencher OS"; linha da tabela › "Abrir checklist" (nova aba) | `/os-tecnico/:id` | `pages/TechnicianOS.tsx` | rota **pública**, fora do `AppLayout` (`App.tsx:742`); sem sessão cai no modo cliente |
| Relatório (técnico, OS concluída) | mesma URL; o botão do painel vira "Relatório de Serviço" | `/os-tecnico/:id` | `TechnicianOS.tsx:2506-2677` + `components/technician/OSReport.tsx` | status `concluida` |
| Visão do cliente | link copiado ("Copiar link da OS", "Copiar link do cliente" ou "Copiar Link" do relatório) | `/os-tecnico/<id ou slug-código>?modo=cliente` | `TechnicianOS.tsx:2680-3312` | `?modo=cliente` (força), ou ausência de sessão (redireciona) |
| Visão do cliente, OS pausada | mesma URL quando `status = pausada` | idem | relatório parcial `:2140-2207` | mostra só equipamentos 100% completos |
| Link antigo | `/<uuid>` | redireciona para `/os-tecnico/<uuid>?modo=cliente` | `App.tsx:955-970` | |

- **Pontos de entrada do técnico:** "Preencher OS" (`schedule.ts:126`) ou "Relatório de Serviço" se concluída, no painel da Agenda (`components/schedule/ScheduleDetailPanel.tsx:365-371`); o mesmo botão no detalhe da OS (`ServiceOrderViewDialog.tsx:786-793`); cronograma do contrato (`PmocContractCronogramaTab.tsx:88,113`) e Portal do Cliente (`CustomerPortal.tsx:967-1007`), estes dois fora de T7.
- **O técnico só vê, na Agenda, as OS em que é responsável ou da sua equipe** (`pages/Schedule.tsx:223, 274-279`). Para Rafael achar a OS #16, ela precisa ter `service_order_assignees` (ou `technician_id`) com o id dele.
- **Depois do login o técnico cai em `/dashboard`** (`pages/Auth.tsx:195`); não existe tela inicial própria do técnico. No celular a Agenda abre em "Dia" (T5).
- **"Voltar" e "Sair do preenchimento" fazem `navigate(-1)`** (`TechnicianOS.tsx:3709`; `os.ts:886`); "Finalizar Parcial" também (`:3364`). Se a página foi aberta direto pela URL, não há histórico para voltar: o robô precisa chegar à OS pela Agenda (Dúvida 7.9). O `AppLayout` esconde o próprio botão de voltar nessa rota (`components/layout/AppLayout.tsx:356`).
- **Endereço amigável:** quando a OS tem `public_short_code`, a barra de endereço é reescrita sem recarregar para `/os-tecnico/<cliente>-<serviço>-<código>` preservando `?modo=cliente` (`TechnicianOS.tsx:1229-1242`); o UUID antigo continua valendo. A visão do cliente resolve por UUID (`get_public_os`) ou por código (`get_public_os_by_code`) (`:1253-1257`).
- **`?modo=cliente` com sessão aberta:** a página usa o cliente anônimo (`db = supabaseAnon`) "mesmo que haja sessão de outro usuário/empresa persistida" (`:460-463`). Isto permite gravar a visão do cliente na mesma sessão do Rafael, sem abrir contexto anônimo.
- **Deep-link útil para a gravação:** `/os-tecnico/<uuid>` direto (mas sem histórico para o "Voltar").

---

## 2. Permissões, módulos e configurações

| O que | Regra | Efeito para Rafael Lima (seed) | Evidência |
|---|---|---|---|
| Abrir a tela | rota pública; precisa de sessão para o modo técnico | entra no modo técnico | `App.tsx:742`; `TechnicianOS.tsx:1022-1042` |
| Ver a OS na Agenda | `screen:schedule`; técnico só vê as suas/da equipe | vê a #16 se for responsável | `App.tsx:797`; `Schedule.tsx:274-279` |
| "Editar OS" no menu ⋮ | `isAdminOrGestor()` ou `hasPermission('fn:editar_os_campo')`; escondido em OS de PMOC/contrato | **aparece** (sem registro de permissões, `hasPermission` devolve `roles.length > 0`) | `TechnicianOS.tsx:805-806`; `hooks/usePermissions.ts:132`; `contexts/AuthContext.tsx:383-394` |
| "Consumir do estoque" | só o interruptor da empresa "Consumo de estoque na OS" (não há permissão por usuário) | aparece (seed liga) | `TechnicianOS.tsx:817`; `hooks/useOsMaterials.ts:173-177`; `pages/Settings.tsx:1676-1695` |
| Baixar o estoque (servidor) | só o técnico responsável, quem criou a OS ou gestor; senão "Acesso negado…" (a OS fecha mesmo assim) | precisa ser responsável da #16 | `supabase/migrations/20261013150000_customer_paid_expenses_and_customer_stock.sql:1042-1120`; `TechnicianOS.tsx:1819-1838` |
| Pergunta de receita ao concluir | `useCanLaunchOsRevenue`: admin sim; **sem registro de permissões, não**; senão `*` ou `fn:os_finish_revenue`; mais o interruptor `os_finish_revenue_prompt_enabled`, acesso financeiro do plano e OS ainda sem receita | **não aparece** para Rafael | `hooks/useCanLaunchOsRevenue.ts`; `hooks/useOsFinishRevenuePrompt.ts`; `TechnicianOS.tsx:2035-2044` |
| Bloqueio por assinatura SaaS vencida | só no modo técnico autenticado | não se aplica | `TechnicianOS.tsx:2462-2464` |
| Botão flutuante "Área do Técnico™" | `company_settings.segment = 'refrigeracao'` | aparece | `TechnicianOS.tsx:991-994, 4942-4966` |
| Perguntas em Vídeo | todos os planos (1.29.0); sem trava de módulo na tela | vale | `Changelog.tsx:2207`; T4 inventário |

- **Configurações › Usabilidade › Ordens de Serviço** (`lib/i18n/messages/app/settings.ts:203-232`; `pages/Settings.tsx:213-217, 724-728`): cinco interruptores. **Só dois têm efeito na tela do técnico:** "Salvar fotos no dispositivo" (lido em `OsPhotoField.tsx:138-139`, padrão ligado) e "Consumo de estoque na OS" (interruptor da empresa, `Settings.tsx:1680`). "Salvamento Automático", "Exibir Valores" e **"Exigir Assinatura"** ("Tornar obrigatória a assinatura do cliente ao finalizar OS") não têm leitor em lugar nenhum fora da própria tela de Configurações: são interruptores mortos (P2 e seção 6).
- **Módulos:** T7 não exige módulo pago. O seed da Glacial já liga `video_questions`, `whatsapp` etc.; nada disso muda a tela do técnico (o botão de WhatsApp com o cliente aparece quando há telefone, `components/CustomerWhatsAppLink.tsx`, 1.33.5).
- **Sem permissões gravadas = acesso total** (`AuthContext.tsx:383-394`; achado de segurança 2 do `TRILHA.md`). Para T7 isto significa que Rafael também enxerga "Editar OS" e o menu completo; ver Riscos e P17.

---

## 3. Por tela / janela / aba

Tudo abaixo é **uma página só** (`pages/TechnicianOS.tsx`), vista no CELULAR. Onde o computador difere, está dito.

### 3.1 Chegando na OS (Agenda › painel › "Preencher OS")
- No celular a Agenda abre em **"Dia"** (T5) e o técnico só vê as OS dele ou da equipe dele (`Schedule.tsx:223, 274-279`). Clicar na OS abre o painel "Resumo da OS" e o botão grande **"Preencher OS"** leva, na mesma aba, para `/os-tecnico/<id>` (`ScheduleDetailPanel.tsx:365-371`; `schedule.ts:126`). Com a OS concluída o botão se chama **"Relatório de Serviço"** (`schedule.ts:127`).
- A tela mostra carregamento até a OS chegar. Com `public_short_code` o endereço é reescrito sem recarregar (`TechnicianOS.tsx:1229-1242`); sem ele fica o UUID.
- Não existe tela inicial do técnico: depois do login o app abre o Dashboard (`pages/Auth.tsx:195`).

### 3.2 Cabeçalho fixo (`TechnicianOS.tsx:3670-3768`)
- Faixa na **cor da marca** (`bg-primary`; a Glacial não tem White Label ligado, então vale a cor padrão), cantos de baixo arredondados, **fixa no topo** ao rolar.
- Linha de cima: botão **"Voltar"** (seta + texto, `navigate(-1)`) à esquerda e o **selo de status** à direita (`getOsStatusLabel`, `types/database.ts:419-438`): "Agendada", "Pendente", "A Caminho", "Em Andamento", "Pausada", "Concluída", "Cancelada", e **"Parcialmente Concluída"** quando está pausada com `partial_finish`.
- Centro: nome da empresa, **"OS #16"** (`formatOSNumber`, `lib/osNumber.ts:42`), tipo da OS com ícone de chave (`osTypeLabel`), **"Serviços desta OS"** com um chip colorido por serviço (tabela `service_order_service_types`) e a data `dd/MM/yyyy` + hora `HH:mm` agendadas.
- No computador o mesmo cabeçalho vale, mas Cliente/Técnico/Check-in vão para a coluna da esquerda (`sidebarContextBlocks`, `:3568-3668`) com os títulos "CHECK-IN" e "CHECK-OUT".

### 3.3 Cartão "Ir para o Atendimento" (`:3911-3941`)
- Aparece com status **pendente/agendada** (`isPending`, `:3316`) ou **a caminho**. Título **"Ir para o Atendimento"** (pendente/agendada) ou **"Iniciar Atendimento"** (a caminho).
- Texto: "Informe ao cliente que você está a caminho ou faça o check-in ao chegar." (só pendente/agendada); "Chegou no local? Faça o check-in para iniciar." (a caminho).
- Botões (**só celular**, `lg:hidden`): **"A Caminho"** (índigo, só pendente/agendada) e **"Fazer Check-in"** (contorno em pendente, cheio em a caminho). No computador os mesmos botões ficam no rodapé branco (`:4419-4433`).

### 3.4 A Caminho e "Rota até o cliente" (`:3494-3563, 3794-3907`)
- "A Caminho" pede a posição, grava um ponto `en_route` em `technician_locations` e **depois** muda o status para `a_caminho`; toast **"Status atualizado: A Caminho!"** (`:3494-3519`).
- Cartão **"Rota até o cliente"** (faixa índigo com ícone de mapa; só em "a caminho" e só se há destino: coordenadas da OS/cliente ou endereço) (`:3794-3843`):
  - mapa `RouteToCustomerMap` (Leaflet; fundo vetorial MapLibre via `lib/mapTiles.ts`; rota do OSRM por `fetchOSRMRoute`, `utils/geolocation.ts:150-170`); sem coordenadas do cliente, geocodifica o endereço (Nominatim);
  - rótulo **"🕐 ~N min até o cliente (X km)"** (`components/schedule/RouteToCustomerMap.tsx:241`);
  - botão **"Ampliar"** (canto inferior direito do mapa, aria "Ampliar mapa");
  - dois botões lado a lado: **"Waze"** e **"Google Maps"**, que abrem **janela nova** (`window.open`, `:3535-3562`); sem endereço, toast "Sem endereço para abrir a navegação.".
- **Tela cheia** (`:3846-3907`): diálogo "Mapa da rota em tela cheia" com a faixa "Rota até o cliente", botão redondo de fechar (aria "Fechar mapa"; **Esc** também fecha, `:985-990`), o mapa e os mesmos "Waze"/"Google Maps".
- Destino por `resolveOsDestination` (`utils/geolocation.ts:89-119`): endereço de serviço da OS antes do endereço do cliente. Origem = posição do aparelho, semeada ao entrar em "a caminho" (`:1716-1742`) e atualizada quando o técnico anda 50 m ou a cada 15 s (`:1693-1711`).
- **Rastreamento:** com a OS a caminho, em andamento ou **pausada** o aparelho manda a posição a cada 30 s (`technician_locations`, evento "tracking"); é isso que alimenta o Mapa ao Vivo do gestor e o mapa do cliente (`:1686`; `hooks/useTechnicianLocations.ts:45-130`).

### 3.5 Check-in (`:1744-1797, 3963-3982`)
- "Fazer Check-in" pede a posição e grava em `service_orders`: `check_in_time` (**relógio do navegador**, `:1747`), `check_in_location`, `check_in_by` e `status = 'em_andamento'`; grava também o evento `check_in` em `technician_locations`; toast **"Check-in realizado com sucesso!"**.
- Em segundo plano troca latitude/longitude pelo **endereço** (geocodificação reversa, `utils/reverseGeocode.ts:205`).
- Passa a aparecer a faixa **"Check-in: dd/MM/yyyy às HH:mm"** com o endereço (ou "lat, lng") à direita (`:3963-3982`; só celular), o selo "Em Andamento", o cartão "Checklists" (3.7) e o **rodapé preto** (3.12). O banco carimba o autor se vier nulo (`:1749-1752`; 1.37.36 tirou o bloqueio por responsável arquivado).

### 3.6 Cartões de contexto (`:3985-4061`)
- **Cliente** (só celular): nome, documento, telefone com link `tel:` + atalho de WhatsApp (`CustomerWhatsAppLink`, 1.33.5), endereço "rua, cidade - UF"; se a OS tem endereço de serviço, um bloco **"Endereço deste serviço"** com a nota "O atendimento é neste local, diferente do endereço cadastrado do cliente.". Em OS de contrato aparece o bloco do contrato.
- **"Descrição do Serviço"** (só celular, só se a OS tem descrição) e **"Observações"** (só se tem observação).

### 3.7 Cartão "Checklists" e acordeão por equipamento (`:4063-4140`, `:173-455`)
- Só existe **depois do check-in** e se a OS tem checklist (`isCheckedIn && questionnaireItems.length > 0`, `:4064`; os itens vêm de `service_order_equipment` com `form_template_id`, `:3378`). Antes do check-in nada de checklist (P5).
- Título **"Checklists"** (ícone de prancheta, letra grande). Com a OS pausada: faixa **"OS pausada — retome o atendimento para preencher os checklists."** e o bloco fica a 60% de opacidade, travado (`:4073-4083`).
- **Um item de acordeão por equipamento**, um aberto por vez; o primeiro abre sozinho (`:960-964`). Cabeçalho: foto (toque amplia), nome ("Hi-Wall 18.000 BTUs - Sala dos professores"), categoria, marca/modelo, ambiente (local cadastrado), selos dos **serviços do equipamento** (1.36.23) e **"N checklists"** se houver mais de um. O selo de progresso é **"Concluído"** (todas as obrigatórias respondidas) ou **"X de Y"** (respondidas/total das perguntas visíveis, **de qualquer tipo**) ou "N pendente(s)" (`:296-340`). O cabeçalho do equipamento aberto fica grudado abaixo da faixa da OS ao rolar (`:230-246`; 1.32.6).
- Dentro do equipamento há **um botão por checklist** (nome "Manutenção preventiva de split", selos dos serviços ligados, selo "Concluído"/"X de Y"/"Pendente" e seta); abre e fecha as perguntas (`:346-434`). Com equipamento o botão aparece mesmo com um checklist só; sem equipamento e com um checklist só as perguntas vêm direto (`:436-447`). Checklist avulso (sem equipamento) vira um item com ícone de prancheta e o nome do checklist (`:296-300`).
- `VisitChecklistPanel` (`:4168-4182`) é o checklist de **visita de contrato/PMOC**: fora de T7 (T11).
- "Concluído" e o bloqueio de finalizar olham **só as obrigatórias**; "X de Y" conta tudo.

### 3.8 Perguntas (`components/technician/DynamicFormQuestions.tsx`)
- Cada pergunta: número ("1."), texto, asterisco vermelho se obrigatória, e em cinza a orientação (`guidance`) e a descrição (`:944-1026`). Rótulos: `os.ts:1567-1597`.
- **Respondeu → modo resposta:** mostra o valor (selo "Sim"/"Não", "Conforme"…, texto ou lista) com o **lápis** (title "Editar resposta"); tocar no lápis ou no nome reabre, e reaberta aparece o visto (title "Fechar edição") (`:950-1008, 1028-1052`). **Foto não entra nesse modo** (`:950`).
- Tipos (`renderSingleTypeInput`, `:530-840`):
  - **Sim/Não** (`:537-561`): interruptor + selo **"Sim"** (verde), **"Não"** (vermelho) ou "Não respondido". Cada mudança grava na hora. O primeiro toque sempre liga (P7).
  - **Conformidade** (`:563-631`): botões "Conforme", "Não Conforme", "N/A". O modelo da aula **não usa** este tipo.
  - **Texto** (`:633-652`): caixa de 2 linhas, placeholder "Digite sua resposta..."; grava **ao sair do campo** (`closeFieldEdit`, `:465-471`).
  - **Número** (`:654-669`): campo numérico decimal, placeholder "Digite o valor..."; grava ao sair do campo; **a unidade cadastrada não aparece** (P9).
  - **Medida PMOC** (`:675-735`): com unidade, "Faixa esperada: min a max" e aviso "Valor fora da faixa esperada — confira o equipamento ou registre observação." (T11; fora da aula).
  - **Seleção** (`:738-775`): **caixas de marcar** (dá para marcar mais de uma) e "N selecionada(s)"; grava a cada toque.
  - **Foto** (`:777-797`), **Vídeo** (`:799-817`), **Assinatura** (`:819-835`): ver 3.9 a 3.11.
  - Pergunta com mais de um tipo: "Exclusivo" (ao responder um, os outros somem e surgem o selo "Respondido" e o botão "Limpar resposta e mostrar todas as opções") ou "Cumulativo" (mostra todos) (`:842-940`). O rótulo do tipo Vídeo não está na lista de nomes (`:853-862`): aparece o texto cru do tipo.
- **Modelo da aula** ("Manutenção Preventiva de Split", 13 perguntas, `data/checklistCatalog.ts:94-113`): 5 Sim/Não **obrigatórias** ("Filtros limpos / em bom estado?", "Serpentinas (evap/cond) sem sujeira excessiva?", "Dreno desobstruído e escoando?", "Fixações e suportes firmes?", "Conexões elétricas reapertadas e sem aquecimento?" com a descrição "Verificar bornes e contatos."); 4 Número ("Corrente do compressor medida" A, com a descrição "Comparar com a corrente nominal de placa."; "Pressão de baixa" psi; "Pressão de alta" psi; "Temperatura de insuflamento" °C); 1 Seleção ("Ruído / vibração anormal?": Normal, Leve, "Anormal — requer atenção"); 1 Foto ("Foto do equipamento", opcional); 1 Texto ("Recomendações ao cliente"); 1 Assinatura **obrigatória** ("Assinatura do cliente"). **Não há pergunta de vídeo.**
- Validação (`:240-304`): lista as obrigatórias sem resposta; `autoFillValueFor` (`:89-97`) define o que o atalho preenche (conformidade → "Conforme", Sim/Não → "true").
- Gravação (`saveResponse`, `:369-445`): lê `form_responses` por (OS, pergunta, equipamento), faz `update` ou `insert` com `responded_at` e `responded_by`; erro → toast "Erro ao salvar resposta".

### 3.9 Foto (`OsPhotoField.tsx:96-310`; `os.ts:1399-1424`)
- Dois botões lado a lado: **"Tirar Foto"** (entrada de arquivo escondida `accept="image/*" capture="environment"`, `:296-301`) e **"Galeria"** (some se a pergunta exige câmera, `:312-316`). Contagem "1 foto"/"N fotos" (`:390-391`); miniaturas com lixeira (title "Remover foto"; janela **"Remover foto?"**, "Tem certeza que deseja remover esta foto? Essa ação não pode ser desfeita.", "Cancelar"/"Remover"; apaga o arquivo de verdade, 1.33.0).
- Envio: comprime (`processImageFile`; HEIC vira JPEG), sobe **3 por vez** (`utils/osUpload.ts:35`, 1.33.0) para o bucket **`os-photos`** (`:31`) com barra "Enviando... N%"; se parte falha, salva as que subiram e avisa "{ok} de {total} fotos foram enviadas…" (`:225-246`).
- **Pela câmera, com "Salvar fotos no dispositivo" ligado** (padrão): abre a janela **"Salvar foto no aparelho?"** ("Deseja guardar esta foto no seu aparelho?", **"Agora não"** / **"Salvar imagem"**) e **não** mostra o toast de sucesso. **Pela galeria** (ou com o interruptor desligado): toast **"Foto enviada!"** (ou "{n} fotos enviadas!") (`:249-257`).
- Pergunta de foto única recusa a segunda: "Apenas uma foto permitida" / "Remova a atual para enviar outra." (`:189-197`).
- Dado: a lista de endereços das fotos (separados por vírgula) vai em `form_responses.response_photo_url` (`DynamicFormQuestions.tsx:785-795`). **A seção "Registro Fotográfico (N fotos)" do relatório lê outra tabela (`os_photos`), que a tela do técnico não preenche** (P11).

### 3.10 Vídeo (`OsVideoField.tsx`; `os.ts:1541-1564`)
- Só aparece se o checklist tiver pergunta do tipo Vídeo (o modelo da aula não tem).
- Botões **"Gravar"** / **"Parar gravação"** / **"Regravar"** e **"Galeria"** (a galeria some se a pergunta exige gravação na hora, `DynamicFormQuestions.tsx:804`). Dica: "Clipe curto de até 30 segundos. Precisa de conexão para enviar." Limite de **30 s** e **50 MB** (`OsVideoField.tsx:16-33`); vídeo pesado é comprimido no aparelho ("Deixando o vídeo mais leve...", "faltam ~Ns", 1.32.7-1.32.8). Toasts: "Vídeo enviado!", "Vídeo muito longo", "Vídeo muito grande", "Não foi possível acessar a câmera".
- "Gravar" usa a câmera do aparelho (`getUserMedia` + `MediaRecorder`); sem câmera, só a galeria.

### 3.11 Assinatura
- **Pergunta "Assinatura do cliente" do checklist** (`DynamicFormQuestions.tsx:819-835`): título centralizado e um campo branco para assinar com o dedo (inline); botões **"Tela cheia"** (abre em paisagem), **"Limpar"** e **"Confirmar"** (os dois últimos só depois de desenhar), mais Desfazer/Refazer (aria "Desfazer"/"Refazer") no canto (`components/SignaturePad.tsx:124-169, 188-337`). Confirmado, o campo mostra a imagem (alt "Assinatura") com "Tela cheia" e "Limpar". A assinatura é gravada como **texto (data URL) em `form_responses.response_value`** (`:827-830`).
- **Cartão "Assinaturas"** (`TechnicianOS.tsx:4242-4308`) com "Assinatura do Técnico" e "Assinatura do Cliente": só aparece se a OS tem `require_tech_signature` ou `require_client_signature`. Essas marcas **só nascem em OS de contrato** (`hooks/useContracts.ts:1200`), de PMOC (`generate-pmoc-orders`) ou pela API pública (`20261017122000_public_api_v1_booking_engine.sql`); o formulário da OS nunca as liga (`ServiceOrderFormDialog.tsx:199-200, 456`). **Na OS #16 o cartão não aparece** (P2). Quando a marca existe, "Finalizar OS" recusa sem a assinatura ("Assinatura do técnico obrigatória"/"Assinatura do cliente obrigatória", `:1860-1867`).
- Carimbo legal (data, hora no fuso da empresa e local) fica no relatório (`lib/signatureStamp.ts`; 1.24.35); o nome de quem assina não é gravado (`TechnicianOS.tsx:1966`).

### 3.12 Rodapé preto e menu "Mais ações" (`:4567-4761`)
- **Rodapé preto fixo** (só celular; aparece **depois do check-in ou com a OS pausada**), cantos de cima arredondados: com a OS em andamento, **"Finalizar OS"** (verde, mais largo) + **"Finalizar Parcial"** (laranja, ícone de pausa) + botão hambúrguer (aria **"Mais ações"**); com a OS pausada, só **"Retomar OS"** + hambúrguer (`:4694-4761`). Um degradê preto no "chão" da tela fica atrás (`:4567-4572`).
- **Menu "Mais ações"** (`:4574-4692`): pílulas empilhadas sobre fundo desfocado (aria do fundo "Fechar menu"), nesta ordem: **"Editar OS"** (só se permitido; sem internet fica desativado com o texto "Disponível apenas online"), **"Consumir do estoque"** (só se a empresa liga), **"Pausar OS"** (em andamento) ou **"Finalizar OS"** (pausada), **"Copiar link da OS"** (só OS compartilhável, não tarefa) e **"Sair do preenchimento"** (`navigate(-1)`).
- **Antes do check-in não existe rodapé nem menu** (o link só pode ser copiado depois).
- Fim da página: rodapé do sistema com versão, direitos e "Atualizar" (`<SystemFooter />`, `:4408-4412`).
- **Computador:** rodapé branco fixo com os mesmos botões e "Copiar link do cliente" (`components/technician/OsDesktopShell.tsx:148-160`; `TechnicianOS.tsx:4419-4560`).

### 3.13 "Consumir do estoque" (`components/service-orders/OsConsumeStockDialog.tsx`; `os.ts:1012-1092`)
- Janela de baixo (`ResponsiveModal`). Título **"Consumir do estoque"**, subtítulo **"Anote o que você usou. O estoque só baixa quando a OS for finalizada."**.
- Campos: **"De onde saiu"** (**só aparece se há mais de um estoque ou estoque do cliente**; o do cliente ganha o sufixo "· Estoque do cliente", `:311-327`); **"Material"** (placeholder "Escolha o material", busca "Buscar por nome ou código...", grupos "Neste estoque"/"Outros materiais", "{qty} {unit} disponíveis" ou "sem saldo aqui"); **"Quantidade"** (placeholder "Ex.: 2,5", aceita vírgula); **"Observação (opcional)"** (placeholder "Ex.: troca do capacitor da unidade externa"). Saldo: "Tem {qty} {unit} neste estoque" / "Sem saldo neste estoque"; acima do saldo: "Você está tirando mais do que tem neste estoque. Dá para continuar, o saldo vai ficar negativo."
- Botões **"Adicionar"** (vira "Salvar alteração" + "Cancelar edição" ao editar) e **"Fechar"**. Lista **"Já registrado nesta OS"** com editar/remover e selos "Aguardando envio" (só no aparelho) e "Já baixado" (já descontado). Toasts: "Material anotado", "Material atualizado", "Material removido"; sem rede: "Sem conexão. O consumo foi guardado no aparelho e será enviado quando a internet voltar."
- Cada linha é um **rascunho** em `service_order_materials` (`committed_quantity = 0`, `hooks/useOsMaterials.ts:261`); o saldo **não mexe** até finalizar. O último estoque usado fica em `localStorage` (`LAST_STOCK_KEY`). Linhas sem rede ficam em `localStorage` (`PENDING_PREFIX`) e sobem depois ("Consumo pendente enviado ({n}).").
- Estoques vêm de `stocks` (`is_default` ou o primeiro; consulta com `customer_id.is.null`, `hooks/useStocks.ts:16-47`); materiais e saldo de `inventory` + `inventory_stock_levels` (`components/inventory/InventoryMaterialSelect.tsx`).

### 3.14 Pausar e retomar (`:3322-3347, 3945-3960`)
- **"Pausar OS"** (menu ⋮) **não pede confirmação**: `status = 'pausada'` e toast **"OS pausada com sucesso!"**. A tela mostra o selo "Pausada", o cartão âmbar **"OS Pausada"** ("Esta OS foi pausada. Retome o atendimento para continuar o preenchimento."), checklists travados e o rodapé só com **"Retomar OS"**. O menu da OS pausada oferece "Finalizar OS" e "Consumir do estoque". O aparelho continua mandando a posição (`:1686`).
- **"Retomar OS"** → `status = 'em_andamento'` e toast **"OS retomada com sucesso!"**.
- Na Agenda do gestor a OS entra em "OS Pausadas" ("Pausada há …", "Retomar agora"; T5). O carimbo `paused_at` é preenchido por gatilho do banco, com `updated_at` como reserva (`components/schedule/PausedOrdersDialog.tsx:122-125`; `hooks/usePausedOrders.ts:12-14`).

### 3.15 "Finalizar Parcial" (`:3353-3370, 4730-4738, 4845-4877`)
- Botão laranja do rodapé (só com a OS em andamento). Abre **"Finalizar parcialmente?"**: "A OS ficará marcada como Parcialmente Concluída e aparecerá nas OS pausadas até ser concluída de verdade." + nota "O que você já preencheu fica salvo. Você pode retomar e concluir quando terminar o serviço."; botões **"Cancelar"** e **"Finalizar Parcialmente"**; toast **"OS finalizada parcialmente"**.
- Efeito: `status = 'pausada'` + `partial_finish = true`; **não valida** obrigatórias, assinatura ou PMOC; **não faz check-out**; e executa `navigate(-1)`: **a tela fecha** e volta para onde o técnico estava (`:3364`). O selo passa a "Parcialmente Concluída" (`types/database.ts:430-438`).
- Reabrir: a OS aparece em "OS Pausadas" da Agenda; "Preencher OS" abre de novo com a OS pausada e "Retomar OS" no rodapé. A conclusão de verdade limpa a marca (`partial_finish: false`, `:1961`).
- Visto pelo link público, uma OS pausada mostra um **relatório parcial** (`isPausedPublicReport`, `:2145`; `:2140-2207`) com só os equipamentos 100% completos.

### 3.16 Finalizar a OS (`:1806-1927, 1938-2101, 4801-4910`)
Ordem real de "Finalizar OS" (`handleFinishOS`):
1. Se faltam obrigatórias: se **todas** as faltantes são Sim/Não ou Conformidade, abre **"Checklist incompleto"** ("Faltam {n} item(ns) do checklist sem resposta. Você pode voltar e preencher, ou marcar o restante como Conforme para concluir agora." + aviso "Isto é apenas uma facilidade de preenchimento: o conteúdo é de responsabilidade do técnico e do responsável técnico…"; botões **"Voltar e preencher"** / **"Marcar {n} como Conforme e concluir"**); o atalho grava "Sim" nos Sim/Não (`:2059-2101`; `autoFillValueFor`). Se falta qualquer outra coisa (texto, número, seleção, **assinatura**), só aparece o toast vermelho **"Campos obrigatórios pendentes"** / "Preencha os campos: …" (três primeiros nomes).
2. Assinaturas exigidas pela OS (cartão "Assinaturas"); 3. conformidade e checklist PMOC (só contrato/PMOC, T11).
4. **Com consumo lançado e o interruptor ligado:** abre o **"Resumo do consumo"** ("Confira o que saiu do estoque nesta OS. Dá para corrigir a quantidade antes de confirmar."; por linha "Fica com {qty} {unit}" ou "Fica negativo em {qty} {unit}"; botões **"Voltar"** / **"Confirmar e finalizar"**), que **substitui** a pergunta do passo 5 (`finishWithConsumptionGate`, `:1806-1812`; `components/service-orders/OsConsumptionSummaryDialog.tsx`). Ao confirmar, chama a RPC `commit_os_material_consumption` (`useOsMaterials.ts:454-464`) e **sempre** finaliza a seguir: toasts "Materiais baixados do estoque", "Materiais baixados. Alguns ficaram com saldo negativo, vale conferir no Estoque." ou, se falhar, "Não deu para baixar os materiais do estoque" + "A OS foi finalizada mesmo assim…" (`:1819-1838`).
5. Sem consumo: **"Finalizar OS?"** — "Tem certeza que deseja finalizar e concluir esta OS?" — "Cancelar"/"Finalizar" (`:4885-4910`).
Depois da confirmação (`proceedFinishOS`, `:1938-2054`): pede a posição, geocodifica o endereço, grava `check_out_time/location/by`, `status = 'concluida'`, `partial_finish = false` e as assinaturas do cartão (se houver); **cria a linha em `service_ratings` sempre** (`:2003-2013`, ignora o erro 23505); grava o evento `check_out`; toast **"OS finalizada com sucesso!"**; por fim `maybeOpenRevenuePrompt` (**só quem tem permissão**; pergunta "Houve alguma receita nesta Ordem de Serviço?", T5/T13). A tela vira o **relatório** (3.17).

### 3.17 Relatório da OS concluída e PDF (`TechnicianOS.tsx:2506-2677`; `components/technician/OSReport.tsx`)
- Cabeçalho com "OS #N" e **"Relatório de Serviço"**. Seções (`os.ts:1705-1760`): Cliente; "Equipamento(s)" / "Ver N equipamentos"; "Descrição do Chamado" (só enquanto a OS não está concluída/cancelada); **Execução** (CHECK-IN e CHECK-OUT com nome de quem fez, 1.25.11, hora e endereço; **"Duração:"** em "{h}h {m}min"); "Registro Fotográfico (N fotos)" com Antes/Durante/Depois (dados legados, P11); respostas dos checklists por equipamento; "Assinaturas" (cartão e perguntas de assinatura, com carimbo); **"Avaliação do Cliente"** (NPS e estrelas) só se houver nota.
- **Rodapé do celular** (`OSReport.tsx:1579-1628`): faixa preta com **"Baixar PDF"** (verde; vira **"Gerando PDF..."**) e hambúrguer (aria "Mais ações") com **"Copiar Link"** e **"Imprimir"**. **Não existe botão de compartilhar o PDF.**
- **PDF**: montado no navegador (html2canvas + jsPDF; `utils/pdfPageRenderer.ts:488`), nome `OS-<números> | <empresa>.pdf` (`OSReport.tsx:853-856`); abre todos os acordeões antes (`:840-850`); vídeo no PDF vira o texto "Vídeo disponível no relatório online" (`os.ts:1707`). Erro: "Erro ao gerar PDF". "Imprimir" chama `window.print()` (`:829-838`).
- Sem White Label o relatório termina com o logo "Dominex" e "www.dominex.app". A pesquisa **não** aparece para o técnico logado (`:2598` exige `forceReadOnly`).

### 3.18 Link público: visão do cliente e pesquisa (`TechnicianOS.tsx:2680-3312`; `components/technician/OSRatingSurvey.tsx`)
- **Copiar o link** (3.12/3.17): `https://dominex.app/os-tecnico/<cliente>-<serviço>-<código>?modo=cliente&preview=<chave>` (`utils/shareLinks.ts:27-45`; `handleCopyTrackingLink`, `TechnicianOS.tsx:966-983`); toast **"Link copiado!"**; sem `public_short_code` o link usa o UUID. Tarefas não geram link (`lib/serviceOrderAccess.ts:16-20`).
- Cabeçalho do cliente: logo (ou ícone) + empresa, selo de status, "OS #N", tipo, data. Faixa **"Acompanhamento em tempo real"** com bolinha pulsando (`:2747-2754`). **"Técnico responsável"** (nome e foto) só em "a caminho"/"em andamento". Cartão **"Execução"** (CHECK-IN/CHECK-OUT, endereço, "Duração:"). Cartão "Cliente". Cartão do status: "Aguardando início do atendimento" (pendente), "Técnico a caminho..." , "Técnico em atendimento...", "Esta OS foi cancelada" — **para "Agendada" não há texto** (`:3019-3031`). Mapa **"Localização do técnico em tempo real"** com "🕐 Previsão de chegada: ~N min (X km)" só em "a caminho" (`:3034-3036`; `components/schedule/PublicTrackingMap.tsx`; sonda a posição a cada 20 s pela RPC `get_public_os_technician_location`). "Respostas do Checklist" por equipamento (com "Aguardando resposta..." nas vazias), "Fotos" e, no fim, "Copiar link" / "Link copiado!" (`:3282-3289`). Atualiza sozinha a cada 20 s.
- **Concluída:** o cliente vê o mesmo relatório da 3.17, **com o mesmo rodapé "Baixar PDF" + hambúrguer** (a tela chama `OSReport` igual nos dois modos, `TechnicianOS.tsx:2627-2632`; `OSReport.tsx:1579-1583`), e a gaveta **"Como foi seu atendimento?"** (`OSRatingSurvey.tsx`): escala NPS 0-10, estrelas por critério (os da empresa), **"Seu nome (opcional)"**, **"Comentário (opcional)"** (placeholder "Conte como foi sua experiência..."), botões **"Fechar"** / **"Enviar avaliação"**; toast e faixa **"Avaliação enviada"** / "Obrigado pelo seu feedback!". Abre sozinha se ainda não avaliou (`:2598-2617`) e, fechada, deixa o atalho "Avaliar atendimento" (`RateServiceAffordance.tsx`). Se a empresa guardou o link do Google e a nota enviada atinge o mínimo (ou não há mínimo), abre o convite ("Que bom que você gostou!", "Avaliar no Google"/"Agora não", `os.ts:738-741`; regra em `OSRatingSurvey.tsx:369-376`). Envio pela RPC `submit_public_os_rating` (`hooks/useServiceRatings.ts:91`). Os textos da pesquisa são fixos no componente (fora do i18n).
- A pesquisa só aparece se `survey_enabled` (existe a linha de avaliação) e a OS está concluída (`:2598`).

### 3.19 "Editar OS" (opcional; `EditOsScopeDrawer.tsx`, `hooks/useEditOsScope.ts:41`)
- Gaveta aberta pelo menu ⋮ (3.12): abas **"Equipamentos"** e **"Checklists avulsos"**, "Adicionar equipamento", "Selecionar checklists", "Salvar"; ao remover algo com resposta, "Respostas serão apagadas" / "Apagar e salvar"; toast "OS atualizada" (`os.ts:960-1006`). RPC `edit_service_order_scope` (migration `20260815120000_editar_os_campo_scope_e_rls.sql`). Fora dos 12 capítulos; só dizer que existe, se couber.

### 3.20 Botão flutuante "Área do Técnico™" (`:4942-5004`)
- Para `segment = 'refrigeracao'` (`:991-994`): botão redondo no canto inferior esquerdo (efeito DarkVeil em WebGL), sempre visível no celular; abre a caixa de ferramentas em tela cheia com **"Voltar para OS"** (`os.ts:879`; T18). Aparece em **todas** as telas de execução, também nos vídeos (decidir se aparece no enquadramento, P18).

<!--CONTINUA-->
