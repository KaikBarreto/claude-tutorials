# Impacto da Dominex 1.38.19 nas aulas da Domiflix

> Levantamento de 03/11/2026, só leitura. Compara `src-1.38.19` (main `24f499ba`) com `src-1.38.6` (roteiros, inventários e aulas T1, T4 e T5)
> e com `src-1.38.9` (gravações em andamento). Análise estática do código e das migrações: **nada foi rodado**. O que só se confirma na tela está
> marcado "(a confirmar)". Caminhos de código são relativos a `src-1.38.19/src/` (exceto `supabase/...`). Linhas de roteiro: `Tnn/roteiro.md:linha`.
>
> Legenda: **(a)** nada visível muda · **(b)** só o robô muda (rótulo, posição, passo novo; fala intacta) · **(c)** a fala muda ·
> **(d)** aula entregue mostra o que não existe mais ou confunde.

## 1. Resumo

| Aula | Estado | Classe | Falas que mudam | Observação curta |
|---|---|---|---|---|
| T1 | entregue 1.38.6 | **(d) leve** | 2 (se regravar) | Integrações ganhou a 4ª subaba "Impressora fiscal"; o vídeo diz "três subabas" |
| T2 | voz pronta | (a) | 0 | Telas de usuário intactas; só o casco global (seção 3) |
| T3 v2 | gravando 1.38.9 | (a) | 0 | Nada entre 1.38.9 e 1.38.19 toca as telas da aula |
| T4 | entregue 1.38.6 | **(d) leve** | 2 (se regravar) | "Novo Tipo" virou "Novo Serviço" (botão e janela) |
| T5 | entregue 1.38.6 | **(d) forte** | 5 | Assistente da Nova OS refeito: some a etapa "Orçamento", nomes novos, etapa "Revisão" |
| T7 | voz pronta | (a) | 0 | Só o casco global (aviso/lembrete no topo do celular) |
| T8 | voz pronta | **(c)** + (b) | 2 + 3 leves | Estoque abre em "Estoque geral" (somente leitura); compras em lista e detalhe |
| T9 | voz pronta | **(c)** | 8 (10 se o total mudar) + 1 leve | Assistente de 5 para 3 etapas; deslocamento passa a ter BDI e o total do exemplo muda |
| T10 | só roteiro | (a) | 0 | |
| T11 | só roteiro | **(c)** | 11 + 1 leve | Assistente do contrato de 6/7 etapas para 5 |
| T12 | voz pronta | (a) | 0 | |
| T13 | só roteiro | **(c)** + (b) | 2 | Conciliação sai da lista de contas; "Nova conta"/"Novo cartão" saem do rodapé |
| T14 | só roteiro | (b) | 0 | Status "Autorizada" agora exige prova fiscal na linha (semente/handler) |
| T15 | só roteiro | **(c)** | 2 + 1 leve | Cadastro de funcionário ganhou a aba "Acesso" |
| T17 | só roteiro | (b) | 0 | Aba "Relatório" do Estoque ganhou subabas |
| T18 | voz pronta | (a) | 0 | |
| T19 | só roteiro | (a) | 0 | |
| T20 | só roteiro | (a) | 0 | |
| T21 | só roteiro | (a) | 0 | |
| T22 | só roteiro | (a) | 0 | |

Falas novas que valem voz paga **agora** (aulas ainda sem gravação): T9 8, T11 11, T8 2, T13 2, T15 2 = **25 falas** (mais 6 leves).
Se o Kaik quiser regravar as entregues: T5 5, T4 2, T1 2 = 9 falas.

Onde "só o robô muda" (sem voz nova): T14, T17, T8 (parte), T9 (cap01 a cap04), T13 (parte).

## 2. O que mudou na 1.38.19 que importa para as aulas

Mapa dos commits da lista do Kaik aos efeitos em tela (o resto do diff é PDV, portal admin e fiscal de servidor, sem aula):

| Commit / versão | Efeito nas aulas |
|---|---|
| 432bf94e (1.38.17) orçamentos, estoque, fluxos | Assistente de orçamento 3 etapas (T9); Estoque geral + Curva ABC + compras lista/detalhe (T8); assistente da OS (T5); assistente do contrato (T11); acesso do funcionário (T15) |
| 15509e79 (1.38.19) OS com BDI e PWA | Precificação dentro da Nova OS (T5); `PwaRootEntry` só age em app instalado (nenhuma aula) |
| a6e9136e (1.38.18) quantidade na OS | Selecionar o serviço já cria a linha com Qtd 1 e preço cadastrado (T5) |
| af86eecd proposta sem onboarding | Só `ProposalSimulator`/PDF do simulador de assinatura da Dominex; nenhuma aula |
| 61e5d400 (1.38.16) NFC-e e impressora | Subaba "Impressora fiscal" em Integrações (T1, e vista de passagem em T19/T21); NFC-e e PDV não têm aula |
| e776dc45 (1.38.15) recorrência no financeiro | Só servidor (webhook Asaas): `supabase/functions/tenant-asaas-webhook`, `_shared/tenant-subscription-state.ts`. Nenhuma tela de aula muda |
| f3634f1a, 592a2e2f (1.38.14, 1.38.12) modais | `components/ui/ResponsiveModal.tsx`, `responsive-dialog.tsx`, `contexts/OverlayCoordinatorContext.tsx`: modais deixam de piscar; sem mudança de texto. Efeito de bastidor na seção 3 |
| 388f928b, 3114875b (1.38.13) avisos e NPS | Seção 6 |
| commits fiscais | `lib/fiscal/nfseStatusTruth.ts` muda o rótulo de status da NFS-e (T14) |
| 1.38.10 e 1.38.11 (já entre 1.38.9 e 1.38.19) | Trilha guiada da Domiflix: `DomiflixIntroGate` e `DomiflixLearningReminder` entram no casco do app (seção 3, **risco real de bloqueio**) |

## 3. Riscos transversais (valem para toda gravação na 1.38.19)

**G1. Tela cheia escura bloqueia o app se o backend falso não semear a trilha.** (prioridade máxima)
- `components/layout/AppLayout.tsx:49,127` monta `DomiflixIntroGate` para todo usuário que não é admin do painel master (inclui Camila, Rafael, Tatiane).
- `components/domiflix/DomiflixIntroGate.tsx:75`: `gateOpen = isLoading || isError || (introGate.required && !pulou)`. Isto é, **enquanto a chamada carrega ou se ela falha, o gate fica aberto** (fundo `#111`, tela inteira, prende o foco).
- A chamada é a RPC `get_domiflix_learning_status` (`hooks/useDomiflix.ts:449`). O handler existente em `rec/fakebase/handlers/rpc/get_domiflix_learning_status.mjs` **lança "Trilha não encontrada"** se não houver linha em `domiflix_learning_paths` com `slug = 'tutoriais-do-sistema'`. Só `seeds-extra/t0v2/catalogo.json` cria essa linha. Os mundos das outras aulas não têm: no 1.38.19 o app abriria já bloqueado. (No 1.38.9 não existia o gate.)
- Mesmo com a trilha semeada como no T0 v2 (`is_onboarding: true`, `intro_gate_enabled_at: @now-30d`), o gate pede o vídeo de introdução a quem não tem linha em `domiflix_intro_acknowledgements`, **por usuário**: Rafael (T7), Tatiane (T15) e quem mais for logado precisam do reconhecimento.
- `components/domiflix/DomiflixLearningReminder.tsx:26` mostra uma faixa azul/vermelha no topo (`AppLayout.tsx:39,194,277`) quando `reminder.severity` é `invite|soft|critical`, o que acontece com `is_onboarding: true`, empresa com menos de 30 dias e trilha incompleta.
- **Correção recomendada (uma só semente comum a todos os mundos):** `domiflix_learning_paths` com `slug: tutoriais-do-sistema`, `is_active: true`, **`is_onboarding: false`**. Assim `introGate.required` e a severidade do lembrete saem falsos para qualquer usuário (handler, linhas 63-66 e `introGate.required`), sem depender de reconhecimento por usuário. Se preferir manter `is_onboarding: true`, é preciso `learning_onboarding_started_at` com mais de 31 dias, reconhecimento e `domiflix_user_onboarding.dismissed_until` para cada usuário gravado.
- Verificar com a fumaça: abrir `/dashboard` e checar que não existe `[data-domiflix-intro]`/fundo escuro e que `desconhecidos.log` não traz `get_domiflix_learning_status`.

**G2. Casco do app reorganizado.** `AppLayout.tsx` agora é `h-[100dvh] overflow-hidden`, com faixa do lembrete e `SystemNoticeBanners` **acima** do `<main>` (fora da rolagem) e o `main` com `min-h-0`. Sem aviso nem lembrete semeados, nada aparece; a rolagem passa a ser só do `main`. Gravações que mediam rolagem de página inteira (`window.scrollTo`) devem usar o contêiner do `main` (a confirmar no robô).

**G3. Coordenador de sobreposições** (`contexts/OverlayCoordinatorContext.tsx`): `DailyTasksPopup`, `VersionUpdateNotification` (celular), termos de uso, NPS e o gate agora disputam uma fila por prioridade (`marketing 10 < reminder 20 < tutorial 30 < userAction 50 < destructive 70 < critical 100`). Um modal de prioridade maior **suspende** os menores sem fechá-los. Só atrapalha se algo de prioridade alta (G1) estiver aberto.

**G4. Menu e título.** Item admin "Avisos" virou "Avisos e NPS" (`components/layout/SidebarMenuContent.tsx`, `TopNavbar.tsx`, `MoreMenuDrawer.tsx`), só para o painel master. Nenhuma aula mostra.

**G5. Etiquetas.** `usePartyLabels` aparece agora em seletores de cliente/fornecedor/equipamento (`CustomerSelectField`, `SearchableSelect`, agenda, compras, distribuição de serviços do orçamento). Sem etiquetas semeadas, as telas ficam iguais (o T3 v2 já cobre).

## 4. Detalhe por aula

### T9 · Orçamentos, Precificação e Proposta (a fundo) · **(c)**

Estrutura nova do assistente "Novo Orçamento": **3 etapas** em vez de 5 (`components/quotes/QuoteFormDialog.tsx:552-555`; `lib/i18n/messages/app/crm.ts`, `stepAssembly`, `stepCommercial`, `stepReviewSend`):

| Antes (1.38.6, roteiro) | Agora |
|---|---|
| 1 Destinatário · 2 Serviços e mão de obra · 3 Materiais e deslocamento | **1 "Montagem"** (rola numa tela só: destinatário, bloco "Configurações BDI", "Serviços e Mão de Obra", "Materiais", "Deslocamento"; `QuoteFormDialog.tsx:1640-2043`) |
| 4 Desconto e condições | **2 "Condições comerciais"** (desconto, brindes, parcelas, observações, termos; `:2044`) |
| 5 Validade e revisão | **3 "Revisão e envio"** (válido até, template, capa da proposta, resumo; `:2142`) |

Tabela do roteiro:

| Cap | Linhas | Classe | O que a tela mostra agora |
|---|---|---|---|
| cap00 | 21-31 | (a) | |
| cap01 | 36-50 | (b) | "Configurar Proposta" e "+ Novo Orçamento" sobem para a linha das abas, à direita, e só existem na aba Orçamentos (`pages/Quotes.tsx:174` `QuotesHeaderActions`, `:1110` `actions=`). A fala L47 ("À direita ficam...") continua certa |
| cap02 | 51-60 | (b) | A barra de composição sai do formulário de taxas e vai para o Simulador, que agora é a prévia "Composição" com barra empilhada, "Coeficiente" e "Custo dividido pelo coeficiente" (`components/pricing/BDIPreviewCard.tsx:123`, `BDICompositionPreview.tsx`). Os cartões "Deslocamento/Custo Total/BDI/Lucro Esperado" deixam de existir como cartões. "Salvar" só habilita depois de alterar algo e aparece o texto "Há alterações de precificação ainda não salvas." (`PricingConfigForm.tsx:83,177-179`). Os campos viram `NumericInput` (aceitam vírgula). L58/L60 seguem verdadeiras (o preço final 1.666,67 permanece) |
| cap03 | 61-70 | (b) | Ficha da Van 01 ganha o bloco "Seu custo por hora / Cliente paga com BDI por hora" (`components/service-orders/GlobalCostsTab.tsx:400`) e selos de categoria com ícone |
| cap04 | 71-82 | (b) | Muda o desenho: em vez do seletor "Tipo de serviço", a aba é lista à esquerda ("Tipos de serviço", busca "Buscar tipo de serviço...") e ficha à direita (`ServiceCostsTab.tsx:371`). Sub-abas iguais. O Resumo troca "Custo total / Preço sugerido (BDI)" por "Seu custo total para executar / Cliente paga com BDI" (`:672-676`); as quatro caixas e as taxas do simulador continuam. A fala L81 ainda serve ("preço sugerido" vira "o cliente paga") |
| cap05 | 83-90 | **(c)** | **L88:** "o assistente tem cinco etapas, e a primeira é o destinatário" (agora 3 etapas e a primeira é a Montagem, com o destinatário no alto). **L90** "Avanço." não vale: não há troca de etapa (o robô rola) |
| cap06 | 91-101 | **(c)** | **L96:** "A segunda etapa são os serviços" (tudo é a mesma etapa). O bloco BDI vem **recolhido**: as taxas ficam atrás do botão "Ajustar taxas e entender o BDI" (`QuoteFormDialog.tsx:1474`), com a caixa "Usar BDI" e o selo "Coeficiente 0.6000". Sem o clique, a câmera não vê "Imposto %, Adm...". Linha de serviço: coluna "Cliente paga / un." e seletor de modalidade ("Custo + BDI", "Preço cadastrado", "Valor manual", `QuoteItemsTable.tsx:412-428`). Os resultados do exemplo não mudam: Higienização 3 × 180,00 em "Custo + BDI" (`QuoteFormDialog.tsx:945-955`), Carga de Gás 1 × 350,00 em "Preço cadastrado" com o selo "Sem custos configurados". Subtotal 890,00 igual. **L101** (soft): a dica de que digitar o preço tira a linha do BDI continua válida, mas agora é uma modalidade escolhível |
| cap07 | 102-109 | **(c)** | **L107:** "A terceira etapa traz os materiais" (mesma etapa). Material do estoque entra como "Preço cadastrado" (150,00/kg, sem BDI), então L108 vale. **L109:** o deslocamento tem modalidade (`:2016`): padrão **"Custo por km + BDI"** (`useState('cost_bdi')`, `:606`). 18 km × 1,50 = **custo 27,00, preço 45,00** (27 ÷ 0,6). A tela mostra "Custo 27,00 · Preço resultante 45,00" (`:2038`). A fala "mostra vinte e sete reais" fica errada |
| cap08 | 110-118 | **(c)** | **L115:** "Na quarta etapa... Dou sessenta e sete reais, e o total vai fechar em mil reais". Passa a ser a etapa 2, "Condições comerciais". Com deslocamento 45,00 e desconto 67,00 o total seria **R$ 1.018,00** |
| cap09 | 119-128 | **(c)** | **L124** ("última etapa é a validade e a revisão"; é "Revisão e envio", com "Capa da proposta" e o botão "Abrir proposta completa"). **L125:** não existe "Sugestão pelo BDI R$ 735,00" nem o cartão escuro "Resumo do Orçamento". O resumo é o painel "Resumo do orçamento" (`QuotePricingSummary.tsx:56`): "Mão de obra, Recursos e extras, Materiais, Deslocamento, Custo total, Preço sugerido, Preço praticado, Desconto, Lucro estimado, Margem, Pagamentos, À vista", mais "O que entra no BDI?" ("Dentro do BDI automático"/"Fora do BDI automático", `QuoteBdiScopeGuide.tsx`) e "Composição do preço sugerido". **L126-127** mudam de valor se o total mudar (item abaixo) |
| cap10-cap13 | 129-168 | (a) | Configurar proposta, link, visão do cliente e visualizações: arquivos sem mudança |
| cap14 | 169-179 | (a) | Aprovação do #2 (semente): sem mudança |
| cap15 | 180-189 | (b) | "Gerar OS" intacto. L187 ("no valor de mil reais") só muda se o total do #9 mudar |
| cap16 | 190-198 | **(c)** | **L195:** "Montou o orçamento em cinco etapas... a diferença entre a Sugestão pelo BDI e o Total do orçamento" |

**Decisão necessária (números do #9).** Pelo código (`QuoteFormDialog.tsx:1135-1169`, `calculateMixedQuotePricing :197`) o `displacement_cost` salvo é o **preço** do deslocamento, não o custo:

| Cenário | Deslocamento | Desconto | Total | Parcelas à vista / 10x |
|---|---|---|---|---|
| Roteiro atual | 27,00 | 67,00 | 1.000,00 | 950,00 / 100,00 |
| 1.38.19 sem mexer no robô | 45,00 | 67,00 | **1.018,00** | 967,10 / 101,80 |
| **Opção A (recomendada):** robô digita desconto **85,00** | 45,00 | 85,00 | **1.000,00** | 950,00 / 100,00 |
| Opção B: modalidade "Valor manual" = 27,00 | 27,00 | 67,00 | 1.000,00 | igual | 

Com a opção A, L126, L127 e L187 (e o "R$ 1.000,00" da OS #17, do cap15 e dos mundos seguintes) ficam como estão, e só mudam 8 falas: **L88, L96, L107, L109, L115, L124, L125, L195** (mais L101 leve). Sem A nem B, entram também L126, L127 e L187 (11 falas). Valores calculados à mão (a confirmar na tela): "Preço sugerido" R$ 1.085,00 = (3 × 108,00 + 27,00) ÷ 0,6 = 585,00 do BDI automático + 500,00 fora do BDI (Carga de Gás 350,00 e R-410A 150,00); "Preço praticado" R$ 1.000,00 após o desconto.

Robô (cap05-cap09): abrir "Ajustar taxas e entender o BDI" antes de enquadrar as taxas; sem cliques de "Próximo" entre destinatário, serviços e materiais (um só "Próximo" para ir às condições e outro para a revisão); o `FormWizardStepper` (`components/ui/FormWizardStepper.tsx`) substitui barra e bolinhas; o seletor de material em lote segue (`MaterialBatchPicker.tsx`, agora com custo separado do preço para item avulso); "Criar Orçamento" fica no rodapé da etapa 3.

Backend: seção 5.

### T8 · Estoque, compras e inventário (a fundo) · **(c)** leve + (b)

| Cap | Linhas | Classe | O que a tela mostra agora |
|---|---|---|---|
| cap01 | 41-49 | (b) | Seis abas iguais. A tela abre em **"Estoque geral"** (visão consolidada, somente leitura) e há um painel lateral "Locais de estoque" (`pages/Inventory.tsx:107,209,731`; `components/inventory/StockLocationNavigator.tsx`), **mesmo com um local só** (antes as abas de local só existiam com 2 ou mais: `Inventory.tsx` 1.38.6, `stocks.length > 1`). O roteiro (L45-46) assume "um só local, sem abas de local" |
| cap02-cap03 | 51-71 | (b) | "Cadastrar Material", editar e "Registrar entrada/saída" ficam **bloqueados no Estoque geral**: aparece o aviso "Selecione um local de estoque" (`Inventory.tsx:299,306,338,362`). O robô precisa clicar no local "Estoque Principal" antes. Falas intactas |
| cap04 | 73-81 | **(c)** | **L79** ("cada local ganha a sua aba, e o principal leva uma estrela"): agora o local aparece na lista lateral. **L80** (leve): "Na engrenagem da aba" passa a "Configurar local" no item da lista |
| cap05 | 83-89 | (c) leve | **L89** "Na aba da Van 01": passa a clicar no local "Van 01" da lista. Transferir segue no menu da linha |
| cap06 | 91-98 | (c) leve | **L95** "Na engrenagem da van": igual a L80 |
| cap07 | 100-108 | (b) | Kardex com o filtro "Período" reposicionado (`InventoryKardexTab.tsx`) |
| cap08 | 110-119 | **(c)** | Compras viram **lista e detalhe** (`MaterialPurchasesTab.tsx:56,67`): título "Compras e requisições", "Selecione uma compra", busca "Buscar por código, título ou fornecedor...". Os botões "Nova requisição de compra" e "Registrar compra direta" viram o menu **"Nova compra"** com "Criar requisição" e "Registrar compra direta" (`:53,64`). **L115** ("Aqui em cima, o Fornecedores... O Registrar compra direta...") fala de botões que agora são itens de menu. A faixa vermelha e "Criar requisição" seguem (a confirmar a posição). **L119** fala de requisição "como cartão": agora é linha da lista |
| cap09-cap10 | 121-141 | (b) | A requisição abre no painel de detalhe, ao lado da lista, sem sair da tela; "Voltar para requisições" só aparece no celular (`CompraDetailView.tsx`, prop `embedded`). Cotações, ordens e recebimento iguais |
| cap11 | 143-151 | (a) | |
| cap12 | 153-164 | (b) | Inventários ganhou filtro de período (`InventoryCountsTab.tsx:35`, padrão "todo o período") |
| cap13 | 166-172 | (a) | |
| cap14 | 174-183 | (b) | A aba "Relatório" agora tem as subabas **"Compras"** (o relatório do roteiro, aberto por padrão) e **"Curva ABC"** (`InventoryReportsTab.tsx:21`). Fala intacta; Curva ABC é assunto novo e não precisa entrar |

Fala nova a decidir (opcional, não obrigatória): uma frase sobre "Estoque geral" e outra sobre a Curva ABC.

### T5 · Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo (a fundo) · entregue 1.38.6 · **(d) forte**

Kanban, Lista, Filtros, Configurações de OS, detalhe, "Resetar OS" e Agenda: **sem mudança** (arquivos intactos). O que mudou é o assistente "Nova Ordem de Serviço" (`components/service-orders/ServiceOrderFormDialog.tsx:1231`):

| Antes (vídeo) | Agora |
|---|---|
| 1 "Cliente e Serviço" · 2 "Orçamento" · 3 "Equipamentos e Checklists" · 4 "Agendamento e Detalhes" | 1 **"Atendimento e orçamento"** · 2 **"Escopo técnico"** · 3 **"Equipe e agenda"** · 4 **"Revisão"** (`lib/i18n/messages/app/os.ts:157-160`) |
| Orçamento em etapa própria, com "Selecionar serviço...", "Qtd", "Valor Unit." e botão "+" ("Incluir") | Cliente, "Tipos de Serviço" e o orçamento ficam **na mesma etapa**; escolher o serviço **já cria a linha** com Qtd 1 e preço cadastrado ("O serviço entra abaixo com quantidade 1 e o preço cadastrado.", `:2301`), sem botão "+". Aparece a chave **"Precificar com BDI"** (desligada: "Preço livre"; `ServiceOrderBudgetSection.tsx:120`), o guia "O que entra no BDI?" e os totais "Serviços e mão de obra", "Materiais" e "Total para faturamento" (`:256`) |
| "Revisão do escopo da OS" no início da etapa 4 | Etapa final "Revisão" com resumo "Confira antes de salvar"; a conclusão da OS ("Conclusão da OS", exigir assinatura técnica/do cliente) fica em "Equipe e agenda" |

O vídeo entregue mostra um caminho que não existe mais (etapa "Orçamento", botão "+", nomes das etapas). Falas que cairiam numa regravação:

| Linha | Fala | Problema |
|---|---|---|
| T05:52 | "A janela tem quatro etapas, e a primeira é Cliente e Serviço." | continuam quatro, mas a primeira é "Atendimento e orçamento" |
| T05:62 | "Agora a etapa Orçamento..." | não há etapa Orçamento |
| T05:63 | "...Clico no mais, e o Total para faturamento mostra..." | não há "+" |
| T05:79 | "Última etapa: Agendamento e Detalhes. Primeiro, uma revisão do escopo..." | agora "Equipe e agenda" e depois a "Revisão" |
| T05:91 | "...na última etapa, ligo a Recorrência." | a Recorrência fica em "Equipe e agenda" (penúltima) |

(Leve: T05:65 "Vamos pra próxima etapa" segue válida; T05:71 não cita o nome da etapa.) Para o cliente que assistir ao T5 entregue, o dano é: procurar etapa e botão que não existem. Valores permanecem (Manutenção Preventiva 1 × 180,00, total 180,00; "Total para faturamento" mantém o rótulo).

### T7 · O técnico em campo (a fundo) · **(a)**

Tela do técnico (Agenda do dia, OS, checklist, "A Caminho", assinatura, PDF) sem mudança nos arquivos do inventário: só `Schedule.tsx`/`ScheduleHeader.tsx` ganham etiquetas no filtro de cliente (invisível sem etiquetas) e `hooks/useContracts.ts` ganha campos de portal. O que muda para a gravação no celular é só o casco (seção 3): `AppLayout.tsx` mobile com altura de tela e faixa do lembrete acima do conteúdo, e o `VersionUpdateNotification` (gaveta "novidades da versão") passa pela fila de sobreposições. Rafael Lima é usuário não-admin: precisa passar pelo G1.

### T11 · Contratos e PMOC (a fundo) · **(c)**

Assistente "Novo Contrato" refeito (`components/contracts/ContractFormDialog.tsx:526`): **5 etapas para contrato comum e PMOC** (em vez de 6 e 7) e a etapa "Portal" só na edição.

| Antes | Agora |
|---|---|
| Identificação · (Unidade & RT, só PMOC) · Ambientes e Equipamentos · Frequência · Equipe & Cobrança · Financeiro · Revisão | **Dados do contrato** (nome, cliente, "É um contrato PMOC?"; no PMOC traz aqui Responsável Técnico e Identificação da Unidade, `:2972-2995`) · **Escopo técnico** (ambientes e equipamentos; título "Equipamentos e escopo" ou "Ambientes e equipamentos") · **Agenda** (frequência e prévia) · **Operação e cobrança** (equipe, tipo de serviço, checklist, "Contrato Ativo" e, na criação, "Configuração financeira" com "Já gerar as parcelas", `:4145`) · **Revisão** (+ "Portal" antes da revisão na edição, `:4387`) |

Falas que mudam (T11):

| Linha | Motivo |
|---|---|
| 72 | "Um contrato comum tem seis etapas" (agora cinco) |
| 73 | "Segunda etapa: Ambientes e Equipamentos" (agora "Escopo técnico") |
| 74 | "Na Frequência..." (agora "Agenda") |
| 75 | "Em Equipe e Cobrança..." (agora "Operação e cobrança") |
| 76 | "No Financeiro, deixo desligado..." (não é mais etapa; é bloco dentro de "Operação e cobrança") |
| 86 | "ganhou a Unidade e RT, e agora são sete" (não ganha etapa; os campos entram em "Dados do contrato") |
| 92 | "Vamos pela primeira etapa nova, a Unidade e RT" |
| 114 | "Na Frequência, a lei recomenda visita mensal..." (agora "Agenda") |
| 118 | "...na etapa de Ambientes" (leve) |
| 124 | "Em Equipe e Cobrança, os Técnicos Executores..." |
| 125 | "Agora o Financeiro, a etapa Como e quando receber" (é o bloco "Configuração financeira") |
| 135 | "Última etapa: a Revisão" (leve; continua última na criação, mas nomes das seções mudam) |

Total: 11 falas (72, 73, 74, 75, 76, 86, 92, 114, 118, 124, 125; a 118 é a mais leve) e 1 leve (135). Telas L67-139 mudam de nomes (robô). Detalhe do contrato, cronograma, documentos e renovar/pausar (cap10 a cap13): arquivos sem mudança (a confirmar a edição, que ganha a etapa "Portal").

### T2 · Usuários, cargos e permissões (a fundo) · **(a)**

Nenhuma tela de Configurações > Usuários mudou. "Criar Usuário" e "Vincular a Funcionário" iguais. Mudança só no servidor: `supabase/functions/create-user/index.ts` agora valida que `employee_id` é da empresa do chamador e falha de forma explícita; o handler falso `rec/fakebase/handlers/functions/create-user.mjs` já vincula `employee_id`. Pegadinha de bastidor: G1 (Camila precisa passar pelo gate). A tela de funcionários (aba "Acesso") é do T15, não do T2.

### T13 · Financeiro (a fundo) · **(c)** leve

Só a coluna "Contas e cartões" de Movimentações mudou (`components/financial/FinanceMovimentacoes.tsx`):

- O item **"Conciliação" sai da lista** (antes entre "Geral (Todos)" e o grupo "Contas"). Agora é o botão **"Conciliação bancária (OFX)"** no cabeçalho, ao lado do título (`:820`, `lib/i18n/messages/app/finance.ts:1585`); dentro da conciliação há "Voltar para Visão geral" (`ReconciliationTab.tsx:94`) e o botão "Como funciona?" virou **"Ajuda"** (`finance.ts:1591`).
- Os botões "Nova conta" e "Novo cartão" **saem do rodapé** e viram um "+" expansível no título de cada grupo ("Contas" e "Cartões"), com rótulos "Nova conta" e "Novo cartão" ao passar o mouse (`:55`, `:769`). O grupo "Cartões" aparece mesmo vazio (para quem gerencia contas). As janelas continuam "Nova Conta" e "Novo Cartão" (`finance.ts:985-986`).
- Carga da coluna com esqueleto "Carregando contas e cartões...".

| Linha | Classe | Problema |
|---|---|---|
| T13:66-67 | **(c)** | Tela: lista com "Conciliação". Fala L67: "Logo acima fica a Conciliação..." (agora é o botão do cabeçalho) |
| T13:69 | **(c)** | "...uma poupança... você cria em Nova conta, aqui embaixo" (agora no "+" do grupo Contas) |
| T13:120 | (b) | "Clico em Novo cartão (rodapé da coluna)": a fala não cita o rodapé; só o robô muda |

Contas a pagar/receber, recorrência da conta, cartão e demais capítulos: arquivos sem mudança. A recorrência corrigida em 1.38.15 é do contrato Asaas (servidor), não da conta recorrente do T13.

### T14 · Notas Fiscais (a fundo) · **(b)**

Mudou a regra de exibição do status da NFS-e (`lib/fiscal/nfseStatusTruth.ts:19`): "Autorizada", "Rejeitada" e "Cancelada" só aparecem se a linha tem `status_fiscal_confirmado = true` e, para autorizada, `status_fiscal_confirmado_em` de no máximo **15 minutos** atrás; senão o selo vira **"Aguardando confirmação fiscal"** (laranja, ícone girando; `components/fiscal/nfseStatus.tsx:74`, `lib/i18n/messages/app/nfse.ts:336`). O status legado `falhou` passa a contar como pendente e não oferece "reemitir". Erros de emitir/cancelar ganham um texto de orientação no aviso (`utils/nfseEdge.ts`, `nfseOrientationDescription`).

Efeito nas falas: nenhum (as falas dizem "Autorizada" etc.). Efeito no robô/backend: as sementes de NFS-e e os handlers `nfse-emit`, `nfse-status` e `nfse-cancel` precisam gravar as colunas novas, e o relógio da gravação não pode passar de 15 min depois da confirmação (o `FAKE_NOW` congelado resolve; se o relógio andar, a nota "autorizada" volta a "Aguardando confirmação fiscal" e o app tenta atualizar sozinho pelo `nfse-status`). `CustomerFormDialog.tsx` (cadastro rápido de tomador) ganha etiquetas e campos personalizados, sem mudar os rótulos fiscais.

### T1 · Configurações e identidade · entregue 1.38.6 · **(d) leve**

Tudo igual, menos Integrações: ganhou a subaba **"Impressora fiscal"** entre "Cobranças (Asaas)" e "API Pública" (`components/settings/SettingsWhatsappContent.tsx:158`, sem condição de módulo). O vídeo entregue diz "São três subabas" e "a terceira, API Pública" (T01:148, T01:150; a tela de T01:151 destaca "as três subabas"). Quem abrir verá quatro, a de impressora no meio. Confunde pouco; resolver exige regravar só o trecho de Integrações (2 falas).

### T4 · Serviços, tarefas e checklists · entregue 1.38.6 · **(d) leve**

`lib/i18n/messages/app/os.ts:546,568`: o botão "Novo Tipo" da aba "Tipos de Serviços" virou **"Novo Serviço"**, e a janela "Novo Tipo de Serviço" virou **"Novo Serviço"** (o título de edição continua "Editar Tipo de Serviço"; "Tipo de Tarefa" e "Checklists" não mudam). Falas: T04:41 ("Categorias e Novo Tipo") e T04:56 ("Clico em Novo Tipo"). O vídeo entregue mostra um botão com nome antigo na mesma posição; o cliente entende. Além disso, `ServiceTypesPanel.tsx` corrige a seleção ao criar (sem impacto visual).

### T3 v2 (gravando em 1.38.9) · **(a)**

Entre 1.38.9 e 1.38.19, o único arquivo das telas da aula que mudou é `components/customers/CustomerSelectField.tsx` (opção `showCreateLabel`, só usada pelo PDV). Não precisa regravar por causa da 1.38.19. A gravação só precisa do ajuste G1 se o app de gravação for atualizado.

### T12 · Portais do Cliente e do Contrato · **(a)** (base 1.38.9)

Em relação à 1.38.9: só `hooks/useContracts.ts` e `lib/contractPortalSections.ts` (helper) e a etapa "Portal" na **edição** do contrato (`ContractFormDialog.tsx:4387`). A configuração "Quem vê o quê" que o T12 grava continua no cartão do detalhe do contrato (`pages/ContractDetail.tsx`, sem mudança). Casco G1.

### T18 · Área do Técnico (Refrigeração e Climatização) · **(a)**

Arquivos do inventário sem mudança, além do casco. (`pages/modulos/AreaDoTecnico.tsx` mudou: é a página de venda do módulo, não a aula.)

### T10 · CRM · **(a)**. `CustomerDetail.tsx` só ganha etiquetas (1.38.8/9).

### T15 · Funcionários · **(c)**

`components/employees/EmployeeFormDialog.tsx:429,747`: a janela de funcionário ganhou a aba **"Acesso"** (entre "Pagamento" e "Ponto eletrônico"; PJ/MEI troca "Ponto" por "Contrato"): "Acesso ao sistema" ("Vincule um usuário existente ou crie login, papel e permissões para este funcionário."), e-mail de login, "Vincular a um usuário do sistema", "Criar acesso ao sistema", "Papel no sistema" e "Permissões" (antes o vínculo/criação ficava na aba Dados e o login criado nascia sem permissões, ver T15:93). Cadastro de acesso passa por `useEmployeeAccess` e `create-user` com `employee_id`.

| Linha | Classe | Problema |
|---|---|---|
| T15:63 | **(c)** | "A janela tem quatro abas: Dados, Pagamento, Ponto eletrônico e Perfil" (agora cinco com "Acesso") |
| T15:93 | **(c)** | "...Criar acesso ao sistema cria um com o e-mail... Depois, em Usuários e Permissões, é só aplicar o cargo": agora o papel e as permissões são escolhidos na própria aba "Acesso" (o handoff P1 do roteiro muda) |
| T15:92 | leve | Vincular agora é na aba "Acesso" (a fala só diz "escolho o nome dela aqui") |

Robô: o cap05 muda de aba (passo extra "Acesso") e os pontos de zoom.

### T17 · Dashboard e relatórios · **(b)**

Menu "Gestão" → "Estoque": as abas "Posição de Estoque", "Inventários" e "Relatório" seguem, mas "Relatório" abre com subabas "Compras" e "Curva ABC" (T17:102). Faixas de aviso do Dashboard (`SystemNoticeBanners scope="dashboard"`) só aparecem com aviso semeado (G1/seção 6). Fala intacta.

### T19, T20, T21, T22 · **(a)**

- T19: Integrações ganha a subaba "Impressora fiscal" entre "Cobranças (Asaas)" e "API Pública"; o roteiro entra por nome em "Cobranças (Asaas)". `Quotes.tsx` (menu "Gerar cobrança" do orçamento) só reorganizou botões. A correção do status do contrato após baixa externa (1.38.15) é do servidor.
- T20: só `finance.ts` (rótulos da conciliação e contas), fora da DRE.
- T21: Integrações > WhatsApp: ganha irmã "Impressora fiscal"; o resto igual.
- T22: `Employees.tsx` só mudou o fluxo de salvar acesso; abas "Perfil Comportamental", "Organograma" e "Fluxograma" e o gerador de link DISC iguais.

## 5. O que o backend falso precisa ganhar (1.38.19)

Base: `$TUT_HOME/rec/fakebase` (`schema.json` hoje gerado do `types.ts` da 1.38.9; backup `schema.json.1.38.6`). RPC sem handler devolve vazio pelo tipo do schema; RPC fora do schema devolve `null` (`http/rest.mjs`, `emptyRpcResult`); coluna fora do schema é aceita e salva, só não ganha padrão.

**5.1 Regerar o schema (`rec/fakebase/tools/gen-schema.mjs` apontando para `src-1.38.19`)**, que traz:

| Tipo | Itens (todos entre 1.38.9 e 1.38.19) |
|---|---|
| Tabelas novas | `admin_notices`, `admin_notice_dismissals`, `admin_nps_surveys`, `admin_nps_responses` (avisos e NPS); `company_nfce_settings`, `nfce_documents`, `nfce_events`, `nfce_outbox` (NFC-e, nenhuma aula) |
| Colunas | `quotes.use_bdi`; `service_orders`: `use_bdi, tax_rate, admin_indirect_rate, profit_rate, bdi, total_cost, km_cost, distance_km, displacement_cost, commercial_adjustment`; `service_order_budget_items`: `pricing_mode, price_override, unit_hours, unit_hourly_rate, unit_labor_cost, unit_materials_cost, unit_extras_cost, unit_total_cost, profit_rate, bdi`; `inventory.fiscal_*` (12 colunas, sem tela nas aulas) |
| RPCs novas | `get_inventory_abc_report(p_start_date, p_end_date, p_stock_ids)`, `get_pending_admin_nps()`, `submit_admin_nps(...)` |
| Armadilha | O `types.ts` commitado coloca `status_fiscal_confirmado`, `status_fiscal_confirmado_em`, `status_fiscal_fonte`, `status_fiscal_evidencia` em `affiliate_commissions` (linha 782) por engano; no banco (`supabase/migrations/20261101193000_nfse_status_exige_prova_oficial.sql`) elas são de **`nfse_emissions`**. Acrescentar à mão no schema/sementes de `nfse_emissions` |
| Fora do `types.ts` | As tabelas `domiflix_learning_paths`, `domiflix_intro_acknowledgements`, `domiflix_user_onboarding` e a coluna `companies.learning_onboarding_started_at` não estão no `types.ts` (o app usa `as any`); só existem nas sementes `seeds-extra/t0v2`. Ver G1 |

**5.2 Padrões e gatilhos**
- `TABLE_DEFAULTS.quotes.use_bdi = true`. O app já trata `null` como ligado (`quote.use_bdi !== false`), mas as sementes de orçamento históricas podem trazer `use_bdi: false` quando `bdi` for 0 (migração `20261102160000_quotes_use_bdi.sql` faz isso).
- `TABLE_DEFAULTS.service_orders`: `use_bdi=false, tax_rate=10, admin_indirect_rate=12, profit_rate=10, bdi=0.68, total_cost=0, km_cost=0, distance_km=0, displacement_cost=0, commercial_adjustment=0`. `service_order_budget_items`: `pricing_mode='manual'`, `bdi=0.68`, demais custos 0.

**5.3 RPCs/handlers a atualizar (já existem; só falta a parte nova)**
- `sync_service_order_budget` (T5, T9): passar a aceitar `p_pricing` (jsonb) e gravar na OS `use_bdi, tax_rate, admin_indirect_rate, profit_rate, bdi, total_cost, km_cost, distance_km, displacement_cost, commercial_adjustment` e, em cada item, `pricing_mode, unit_*, price_override, profit_rate, bdi` (`supabase/migrations/20261103133000_os_budget_bdi_methodology.sql`). Sem isso o vídeo de T5 funciona (o handler ignora o resto), mas ao reabrir a OS os itens voltam em "Preço livre". Total da OS continua `services + materials` (+ ajuste comercial se houver).
- `generate_service_order_from_quote` (T9 cap15): copiar da cotação para a OS `use_bdi, tax_rate, admin_indirect_rate, profit_rate, bdi, total_cost, km_cost, distance_km, displacement_cost` e `commercial_adjustment = total_price − soma dos itens`, e os itens com `pricing_mode` conforme a regra da migração. Obrigatório só se alguma aula abrir o orçamento da OS gerada; o valor R$ 1.000,00 já sai de `q.total_value`.
- `get_inventory_abc_report`: só se alguma gravação abrir "Relatório > Curva ABC" (nenhum roteiro abre; devolver `[]` basta).

**5.4 O que cada aula chama de novo ou de diferente**

| Aula | Tabelas/RPCs que as telas novas chamam |
|---|---|
| T9 | `quotes` (insert/update com `use_bdi`, `displacement_cost` = preço), `quote_items` (sem `pricing_mode`; usa `price_override`), `pricing_settings`, `service_costs`, `service_materials`, `service_cost_resources`, `service_gifts`, view `cost_resources_with_rate` (já existe), `inventory`, `proposal_templates`. Novo: `hooks/useServiceCostBreakdown.ts` lê `service_costs`, `service_materials`, `service_cost_resources`, `service_gifts` e a view juntos (consulta em lote: testar `select=*` nelas) |
| T5 | `service_orders`, `service_order_budget_items`, RPC `sync_service_order_budget` (novo `p_pricing`), `sync_service_order_scope_with_services`, `service_types`, mesmas leituras de custo do T9 (para o preço do serviço), `pricing_settings` (para o BDI do botão "Precificar com BDI") |
| T7 | nada novo |
| T8 | `inventory_stock_levels` (alimenta o "Estoque geral"; hook já existe), `get_accessible_inventory_ids`, `compras` com `material_count` (coluna calculada no hook), `inventory_counts` (filtro de data em `created_at`), RPC `get_inventory_abc_report` (só ABC) |
| T11 | `contracts` (insert já usa `portal_is_public` e `portal_sections` na edição), resto igual |
| T2 | `create-user` com `employee_id` (handler pronto) |
| T13 | `financial_accounts` (esqueleto de carregamento aguarda `isLoading`); nada novo |
| T14 | `nfse_emissions` com `status_fiscal_confirmado`, `_em`, `_fonte`, `_evidencia`; `nfse_events`; handlers `nfse-emit`, `nfse-status`, `nfse-cancel` gravando esses campos e, nas respostas de erro, `orientacao` |
| T15 | `create-user` com `employee_id` (aba "Acesso") |
| Todas | `get_domiflix_learning_status`, `get_pending_admin_nps`, `admin_notices`, `admin_notice_dismissals` (ver seção 6 e G1) |

## 6. NPS e avisos da plataforma numa gravação

**Podem aparecer? Só se o backend falso devolver dados. Como está hoje, o NPS e os avisos de texto não aparecem. O que pode aparecer sem querer é a trilha Domiflix (G1).**

| Elemento | Onde monta | Condição para aparecer | Estado no backend falso | Como impedir |
|---|---|---|---|---|
| **Avisos da plataforma** (faixa no topo) | `components/notices/SystemNoticeBanners.tsx`, em `AppLayout.tsx:34,195,278,319` (escopo global, acima do conteúdo) e no Dashboard; lê `admin_notices` (`hooks/useSystemNotices.ts:41`) e `admin_notice_dismissals` | Existir linha ativa em `admin_notices` dentro de `starts_at/ends_at` e do público (`all` ou empresa) e não dispensada | `admin_notices` e `admin_notice_dismissals` estão em `seeds/00-vazias.json` (vazias de propósito) | Manter as duas em `_vazias`; **não semear** linha nelas; depois de regerar o schema, conferir que seguem na lista. Nenhum `seeds-extra` pode conter `admin_notices` |
| **NPS da plataforma** (diálogo no computador, gaveta no celular, pesquisa de uma pergunta por vez) | `components/nps/PlatformNpsSurvey.tsx` em `AppLayout.tsx:35,128`; RPC `get_pending_admin_nps` (`hooks/usePlatformNpsSurvey.ts:25`) | A RPC devolver uma pesquisa pendente (`admin_nps_surveys` ativa, `trigger = 'login'`, sem resposta do usuário). Não monta para o painel master | Sem handler: hoje a RPC está fora do schema e devolve `null` → nada aparece. Depois de regerar o schema ela vira `RETURNS TABLE` e o vazio padrão é `[]` → também nada | Criar o handler `get_pending_admin_nps.mjs` que **sempre devolve `[]`** (cinto e suspensório) e um `submit_admin_nps.mjs` que nunca é chamado; não semear `admin_nps_surveys`. É diferente do NPS por OS (`nps_settings`, relatório "NPS e Satisfação" do T17), que continua como está |
| **Trilha / lembrete Domiflix** | `DomiflixIntroGate` (tela cheia), `DomiflixLearningReminder` (faixa) em `AppLayout.tsx` | Ver G1: o gate abre durante o carregamento, em erro da RPC ou com vídeo de introdução pendente | Hoje lança "Trilha não encontrada" fora do T0 v2 → **gate preso** | Semente `domiflix_learning_paths` com `is_onboarding: false` em todo mundo (G1) |
| Gaveta "novidades da versão" (celular) | `components/pwa/VersionUpdateNotification.tsx` | Celular, versão vista diferente da atual | `localStorage` limpo por gravação | Manter o `setup` do robô gravando a versão atual como vista (T7, T15 cap9) |
| Lista diária de tarefas | `components/tasks/DailyTasksPopup.tsx` | Tarefas do dia do usuário | Já tratado nas aulas | Sem mudança |

Todos passam pelo coordenador de sobreposições: se o gate (prioridade `critical`) estiver aberto, os outros ficam suspensos. A verificação mínima antes de cada gravação: abrir o Dashboard, ver que `desconhecidos.log` não registra `get_domiflix_learning_status` nem `get_pending_admin_nps`, e que não há faixa no topo.

## 7. Ordem sugerida

1. Backend falso: semente comum de `domiflix_learning_paths` (G1), regerar schema, handler de NPS vazio, colunas de `nfse_emissions` (5.1). Reconstruir o app de gravação na 1.38.19 sob `flock $TUT_HOME/.heavy.lock` e rodar a fumaça.
2. T9 (voz de 8 falas se a opção A for aceita), depois T11 (11 falas) e T8 (2 falas); T13 e T15 (2 falas cada) quando chegarem na fila.
3. Sem voz nova: T2, T7, T12, T18 (voz pronta) e T10, T14, T17, T19, T20, T21, T22 só pedem o ajuste de robô e do mundo.
4. Decisão do Kaik: regravar T5 (5 falas, vídeo mostra etapa inexistente), T4 (2) e T1 (2) ou aceitar a diferença. T5 é o único com risco de confundir.
