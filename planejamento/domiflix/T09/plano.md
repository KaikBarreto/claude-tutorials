# Plano · T9 — Orçamentos, Precificação e Proposta

- **Título final da aula:** Orçamentos, Precificação e Proposta (do preço certo à proposta aprovada)
- **Áreas das vinhetas:** ORÇAMENTOS · PRECIFICAÇÃO · CUSTOS GLOBAIS · CUSTOS DOS SERVIÇOS · PROPOSTA · APROVAÇÃO · ORDEM DE SERVIÇO
- **Objetivo (uma frase):** montar um orçamento com preço calculado pelo BDI, entregar a proposta ao cliente, aprovar (pelo link ou por
  dentro, com o financeiro) e gerar a ordem de serviço distribuída pelos equipamentos.
- **Pré-requisito:** T8 (Estoque, compras e inventário). Aviso: "Antes: Estoque, compras e inventário".
- **Próximo:** T10 (CRM: funil, leads e captação). Aviso: "Próximo: CRM: funil, leads e captação".
- **Duração estimada:** ~24 min de fala natural (17 blocos; a trilha previa ~45 min). Sem módulo pago (Precificação e Custos Globais valem para
  todo plano desde a 1.29.0). Sem preço de plano da Dominex; valores em R$ de serviços e materiais do mundo fictício aparecem.
- Base: `T09/inventario.md` (código 1.38.6). Rótulos entre aspas = exatamente como na tela. **Ordem proposta = "motor primeiro"**
  (tela → Precificação → Custos → orçamento → proposta → aprovação → OS), diferente da trilha (decisão 1). As contas dos capítulos 2 a 9 seguem as regras
  da seção 3.2.1 do inventário (conferidas à mão, **não rodadas no app**).

## Capítulos propostos

| # | Vinheta (área / título) | O que a tela mostra | Avisos na tela (positivos) | Duração |
|---|---|---|---|---|
| 0 | — | Menu lateral com "Orçamentos" em destaque. Fala: "Neste tutorial você vai montar um orçamento com preço certo e mandar uma proposta que fecha." | "Antes: Estoque, compras e inventário" | 0:30 |
| 1 | ORÇAMENTOS / A tela e as quatro abas | Título "Orçamentos" ("Gerencie orçamentos, custos e precificação"); abas no topo: "Orçamentos", "Custos dos Serviços", "Custos Globais", "Precificação". Cartões "Em Aberto", "Conversão", "Ticket Médio": clica em "Em Aberto" (a lista filtra por Enviado) e desmarca "Enviado" no filtro "Status" (volta a Todos). Lista: Nº, Cliente (com o indicador de visualização), Data, Custo, Valor, Margem e o selo de Status; busca e filtro "Status". | "Os cartões Em Aberto e Conversão filtram a lista" | 1:15 |
| 2 | PRECIFICAÇÃO / O BDI da empresa | Aba "Precificação": cartão "Método BDI" ("Preço = Custo Total ÷ BDI"). Digita "Imposto (%)" 6, "Adm. Indireta (%)" 12, "Lucro Padrão (%)" 22 → "BDI atual" **0.6000** e a barra de composição; "Deslocamento e Pagamento": "Custo por KM (R$)" 1,5, "Desconto à vista (%)" 5, "Parcelas (cartão)" 10; "Salvar" → "Configurações de precificação salvas!". Simulador: "Custo do serviço" 1.000 → "Preço Final (BDI)" **R$ 1.666,67** e a linha "Preço = R$ 1.000,00 ÷ 0.6000 = R$ 1.666,67". | "Salvou as taxas? Todo orçamento novo já nasce com elas" | 1:50 |
| 3 | CUSTOS GLOBAIS / O custo da Van 01 | Aba "Custos Globais" (título "Centro de Custos"): faixa "Custo/hora Veículos". "Novo Recurso" → "Qual recurso deseja cadastrar?" (Veículos, Ferramentas, Brindes, EPIs, Outros; câmera passa) → Veículos: "Nome do veículo" Van 01, "Horas de uso mensal (para rateio)" 176, "Depreciação mensal" 1.400, "Manutenção + Combustível" 1.620, "Seguro" 3.600 e "Documentação / IPVA" 2.400 (ambos com "Valor anual (÷12)") → "Total mensal:" R$ 3.520,00, **"Custo/hora:" R$ 20,00** → "Salvar". Clica em "Van 01": "Composição do custo". | "O custo por hora do recurso é rateado sozinho" | 1:30 |
| 4 | CUSTOS DOS SERVIÇOS / Quanto custa executar um serviço | Aba "Custos dos Serviços", "Tipo de serviço" Higienização de Split. "Mão de obra": "Custo / hora (R$)" 32 e "Horas" 1,5 → "Custo HH" R$ 48,00 ("Salvo automaticamente"); abre "Calcular" (calculadora de equipe, só mostra) e fecha em "Cancelar". "Recursos": marca "Van 01" (R$ 20,00/h × 1,5 h = R$ 30,00). "Materiais": "Selecione do estoque" Limpa-evaporador em spray 1, Fita isolante 1, Mangueira de dreno 1 → R$ 30,00. "Resumo": "Custo total" **R$ 108,00**, "Preço sugerido (BDI)" **R$ 180,00**, "BDI: 0.6000 \| Lucro padrão: 22.00%". | "Cadastrou os custos uma vez? O preço sai calculado em todo orçamento" | 2:15 |
| 5 | ORÇAMENTO / Etapa 1: Destinatário | Aba "Orçamentos" → "+ Novo Orçamento": cinco bolinhas. Alterna "Cliente cadastrado" × "Novo prospecto" (aparecem "Nome *", "Telefone", "E-mail"; volta). "Cliente *": Pousada Brisa do Mar → "Próximo". | "Ainda não é cliente? Orce como prospecto" | 0:50 |
| 6 | ORÇAMENTO / Etapa 2: Serviços e preço | Bloco "Configurações BDI" já com 6 / 12 / 22 e "Custo / km" 1,5 (selo "BDI 60.0%"). "Selecionar tipo de serviço...": Higienização de Split, "Qtd:" 3, "Adicionar" → preço **R$ 180,00** (custo 108 ÷ 0,60). Clica no nome: "Mão de obra", "Materiais", "Custos extras", "Custo total unit.". Adiciona Carga de Gás: selo âmbar **"Sem custos configurados"** e preço **R$ 350,00** (preço padrão do tipo). "Subtotal Serviços" R$ 890,00. | "Com custo cadastrado, o preço sai do BDI; sem custo, entra o preço padrão" | 2:00 |
| 7 | ORÇAMENTO / Etapa 3: Materiais e deslocamento | "Adicionar materiais": busca "gás", Gás refrigerante R-410A 1 → rodapé "Total: R$ 150,00" → "Adicionar ao orçamento"; tabela Material, Qtd, Preço unit., Total e "Subtotal Materiais". "Deslocamento": 18 km → "= R$ 27,00". | "Material do estoque entra pelo preço de venda" | 1:30 |
| 8 | ORÇAMENTO / Etapa 4: Desconto e condições | "Desconto": "R$" 67,00 ("− R$ 67,00"); alterna "%" e volta. Caixa "Incluir brindes neste orçamento" (só passa). "Observações" ("Atendimento de segunda a sexta, das 8h às 17h.") e "Condições / Termos" ("Serviço executado após a aprovação, com data combinada com o cliente."). | "Desconto em R$ ou em %: você escolhe" | 1:10 |
| 9 | ORÇAMENTO / Etapa 5: Validade e revisão | "Válido até" (+15 dias), "Template da Proposta" **Clean**, "Nº de parcelas" "À vista". Cartão "Resumo do Orçamento": "BDI Calculado", "Custo Total", "+ Deslocamento", "Sugestão pelo BDI" **R$ 735,00**, **"Total do orçamento" R$ 1.000,00**, "À vista (5% desc.)" R$ 950,00, "10x cartão" R$ 100,00 e a nota "Custos e margem são referências internas". "Criar Orçamento" → "Orçamento criado com sucesso!"; a linha nova entra como "Rascunho". | "O Total do orçamento é o valor da proposta" | 1:30 |
| 10 | PROPOSTA / Configurar Proposta | Botão "Configurar Proposta": etapa "Modelo" (Clean, Vanguarda, Aurora, Prisma; câmera percorre as capas A4 e fica no Clean); "Personalização": "Tamanho do logo" 120%, "Cor Primária", "Cor de Destaque", "Fundo do Cabeçalho", chaves "Mostrar paginação?" e "Mostrar deslocamento"; "Seções da proposta": liga "Garantia" e escreve "Garantia de 90 dias sobre o serviço.", move uma seção com ▲▼; "Revisão": folheia as páginas A4; "Salvar" → "Configuração da proposta salva" (a janela continua aberta; fecha no X). | "Uma configuração para todas as propostas" | 1:50 |
| 11 | PROPOSTA / Visualizar e gerar o link | Menu "⋮" da linha do orçamento da Pousada: "Visualizar" → janela "Proposta #N" no Clean ("Não visualizada pelo cliente ainda"; botões "Gerar cobrança", "WhatsApp" e "PDF" só passam na tela). Fecha. "Gerar link da proposta" → "Link gerado e copiado!" ("Já pode colar e enviar pro cliente.") e o selo da linha passa de "Rascunho" para **"Enviado"**; "Em Aberto" sobe. | "Gerou o link? O orçamento vira Enviado" | 1:30 |
| 12 | PROPOSTA / O que o cliente vê | Página pública (sem login) no Clean: cabeçalho com a empresa, "Orçamento #N" e o selo "Proposta válida até …"; rola por "Cliente", "Serviços", "Produtos e materiais", os totais, "Formas de pagamento" ("À vista no PIX", "Parcelado no cartão"), "Informações adicionais", "Observações", "Garantia"; botão "Baixar PDF" (só aparece). Botões **"Aprovar"** e "Rejeitar" (câmera passa); clica **"Aprovar"** → "✅ Proposta aprovada! Obrigado." Volta ao app: a linha agora é "Aprovado". | "O cliente abre sem login e responde com um clique" | 1:20 |
| 13 | PROPOSTA / Quem abriu a proposta | Na lista, o indicador do orçamento do Hotel Mirante do Mar: olho + "3" + "visto há X"; passa o mouse: "Visualizada 3× · última vez dd/MM HH:mm (há X)". Compara com "Não visualizada". Fala: abrir pelo item "Abrir proposta em nova guia" (a olhada do dono) não conta. | "Quantas vezes o cliente abriu, e quando" | 0:50 |
| 14 | APROVAÇÃO / Aprovar por dentro | Orçamento do Hotel Mirante do Mar (Enviado), R$ 3.200,00: menu → "Aprovar orçamento" → "Aprovar Orçamento #N" ("Valor: R$ 3.200,00"). "Vou receber depois" (já marcado): "Parcelas" 3x, "Primeiro vencimento", lista "Parcelas que serão criadas". Alterna "Já recebi": "Forma de pagamento" PIX, "Data do recebimento", "Caixa / Conta bancária" Conta Principal, "Tarifa de máquina/gateway"; volta a "Vou receber depois" → "Aprovar e gerar conta a receber" → "Orçamento aprovado!" ("3 parcelas criadas em Contas a Receber…"). A linha ganha **"No financeiro"** e o menu, "Ver lançamento no financeiro". | "Já recebi ou Vou receber depois: você escolhe" | 2:00 |
| 15 | ORDEM DE SERVIÇO / Gerar OS | Orçamento da Pousada (Aprovado): menu → "Gerar OS" → "Distribuir serviços · Orçamento #N": Higienização de Split nos três equipamentos (botão "Todos": Hi-Wall 9.000 BTUs - Suíte 1, Suíte 2 e Hi-Wall 12.000 BTUs - Recepção), Carga de Gás na Recepção; "Gerar OS" → "OS gerada com sucesso!". A linha vira **"Convertido"**. Abre "Ordens de Serviço": OS #17 "Gerada do Orçamento #N", valor R$ 1.000,00, status "Agendada" (rótulo a conferir na lista de OS, inventário 7.6). | "Cada serviço no equipamento certo" | 1:40 |
| 16 | ORÇAMENTOS / Recapitulando | Montagem: Precificação, Custos, wizard, proposta, link, aprovação, OS. | "Próximo: CRM: funil, leads e captação" | 0:45 |

Transições faladas: 0→1 "Vamos olhar a tela"; 1→2 "Tudo começa pelo preço: primeiro as taxas da empresa"; 2→3 "Agora, quanto custa o que você usa: veículos, ferramentas";
4→5 "Com o motor pronto, vamos montar o orçamento"; 8→9 "Falta só a validade e a revisão"; 9→10 "Agora o documento que o cliente recebe"; 11→12 "Vamos ver do lado do cliente";
13→14 "E se o cliente fechar por telefone ou WhatsApp, você aprova por dentro"; 14→15 "Voltando à Pousada, que aprovou pelo link: hora de gerar a ordem de serviço". Recap → próximo:
"Com o orçamento fechado, o próximo passo é encher o funil de novos clientes."

**Falas dos cuidados ⚠️** (regra de 30/10 20:56: caminho certo primeiro, consequência numa frase, sem encenar falha):

| Cuidado | Fala sugerida | Na tela |
|---|---|---|
| Taxas da empresa | "Preencha e salve as taxas da empresa antes do primeiro orçamento: é delas que o preço sai." | "Salvar" e "BDI atual" |
| Simulador | "O simulador usa as taxas que já estão salvas; salvou, ele atualiza." | Cartão "Simulador de Preço" |
| Preço sem custo | "Se o serviço não tem custo cadastrado, o preço vem do preço padrão do tipo, e o selo Sem custos configurados avisa." | Selo âmbar na linha |
| Preço digitado | "Digitou o preço na mão? Aquela linha deixa de acompanhar o BDI." | Campo "Preço unit." |
| Material e estoque | "O material do estoque entra pelo preço de venda, sem BDI; orçar não consome estoque." | Seletor "Adicionar materiais" |
| Dois valores | "A sugestão pelo BDI é só uma referência para você; o Total do orçamento é o valor da proposta e da ordem de serviço." | "Sugestão pelo BDI" e "Total do orçamento" |
| Observações | "O que você escreve em Observações aparece na proposta do cliente; condições de pagamento e garantia vão em Condições e Termos." | Campos da etapa 4 |
| Configurar Proposta | "O que você salva aqui vale para todas as propostas; o modelo de cada proposta você escolhe dentro do orçamento." | "Salvar" e "Template da Proposta" |
| Link e status | "Gerar o link deixa o orçamento como Enviado, e é a partir daí que o cliente vê Aprovar e Rejeitar." | Selo "Enviado" |
| WhatsApp | "O botão WhatsApp abre a conversa com a mensagem pronta; o envio é seu, e o status continua como estava." | Botão "WhatsApp" |
| Aprovação no link | "Quando o cliente aprova pelo link, o orçamento fica Aprovado; a conta a receber só nasce sozinha se você ligar essa opção em Configurações." | Selo "Aprovado" |
| Aprovar por dentro | "Ao aprovar por dentro, Já recebi lança a entrada paga e Vou receber depois gera as parcelas; o custo do orçamento é só para a sua margem e não vira despesa." | Janela "Aprovar Orçamento" |
| Gerar OS | "Gerar OS cria a ordem com os serviços e o valor do orçamento, distribui por equipamento e não mexe no estoque; o consumo de material se lança na própria OS." | Janela "Distribuir serviços" |
| Validade | "A validade é a data que o cliente vê na proposta." | "Válido até" |
| Conversão | "O cartão Conversão compara os aprovados com os enviados, aprovados e rejeitados; o orçamento que já virou ordem de serviço sai dessa conta." | Cartão "Conversão" |

## Mundo fictício (continuidade)

- **Começa em:** fim do T8 (T0→T1→T4→T5→T7→T18→T2→T8→T9): Glacial Cold Brasil, Camila Duarte (admin), técnicos, 16 clientes; tipos de serviço do T4
  (Higienização de Split R$ 180, Carga de Gás R$ 350, Manutenção Preventiva R$ 180, Instalação de Split R$ 650…); estoque do T8 (EST-001 a EST-010, local
  Van 01); OS #1 a #16; "Conta Principal" no Financeiro. **Pousada Brisa do Mar** (base) tem 3 equipamentos: Hi-Wall 9.000 BTUs - Suíte 1 e Suíte 2 (Brisatec) e
  Hi-Wall 12.000 BTUs - Recepção (Aerovento). Todos os módulos ligados; nenhum 🔒 nesta aula.
- **Entra por seed de bastidor (`seeds-extra/t9/`):** `pricing_settings` da empresa **com zeros** (a aula preenche); `proposal_templates` com as 4 linhas (Clean, Vanguarda, Aurora, Prisma);
  **custo e preço de venda** de 4 materiais do T8 (proposta a alinhar com o T8, que ainda não os fixa): Limpa-evaporador em spray R$ 20,00 / 38,00, Fita isolante R$ 6,50 / 11,00,
  Mangueira de dreno R$ 3,50 / 8,00 (o custo bate com a compra direta do T8), Gás refrigerante R-410A R$ 90,00 / 150,00 (o custo fica na faixa das compras do T8, R$ 86 a 94 o kg); `employees` com custo mensal fictício;
  categoria de receita "Vendas de Serviços"; **8 orçamentos históricos** (datas relativas ao dia): #1 Padaria Bom Grão Aprovado R$ 640,00 · #2 Hotel Mirante do Mar **Enviado R$ 3.200,00, 3 visualizações, 3 parcelas** (é o do capítulo 14) ·
  #3 Clínica Sorriso Leve Rascunho R$ 540,00 · #4 Academia Ponto Forte Rejeitado R$ 1.850,00 · #5 Restaurante Sabor da Serra Aprovado R$ 780,00 · #6 Mercado Vila Nova Enviado R$ 1.450,00 (1 visualização) ·
  #7 prospecto Casa de Repouso Vida Mansa Enviado R$ 980,00 · #8 Escritório Lemos & Prado Rascunho R$ 2.100,00. Os aprovados do histórico vieram do link da proposta, por isso sem "No financeiro" e sem OS (nenhum "Convertido" semeado).
- **Esta aula cria (ao vivo):** taxas da Precificação (6 / 12 / 22, R$ 1,50 por km, 5% à vista, 10 parcelas); recurso **Van 01** (R$ 20,00/h); custos do tipo **Higienização de Split**
  (R$ 108,00; preço sugerido R$ 180,00); configuração da proposta (Clean, cores, seção "Garantia"); orçamento **#9 da Pousada Brisa do Mar**: Higienização de Split × 3 + Carga de Gás × 1 (R$ 890,00),
  R-410A 1 kg (R$ 150,00), deslocamento 18 km (R$ 27,00), desconto R$ 67,00 → **Total R$ 1.000,00** (Rascunho → Enviado → Aprovado pelo cliente → Convertido); aprovação do #2 em 3 parcelas;
  **OS #17**, "Agendada". Estado final em `seeds-extra/t9/apos-capNN.json`; atualizar `MUNDO_FICTICIO.md`.
- **Dois orçamentos de propósito:** quando o cliente aprova pelo link, o item "Aprovar orçamento" some (o orçamento já está Aprovado e, por padrão, sem financeiro); por isso o #9 mostra
  o caminho do link e a OS, e o #2 mostra a aprovação por dentro. **Dados:** nomes, valores e datas fictícios; salários e custos mensais dos funcionários só inventados; sem preço de plano.

## Gravação

- **Já coberto (T3/T7/T8):** login e menu; `click`/`type`/`select`/`hover`/`drag`/`scroll`; janelas e listas (Radix); gravação genérica (REST) em todas as tabelas; relógio travado no `FAKE_NOW`.
- **Falta (ordem de importância; detalhe no inventário 4.3):**
  1. **`TABLE_DEFAULTS.quotes`:** hoje `status` e `token` nascem `null` e `quote_number` 0 (`rec/fakebase/core/defaults.mjs:12-22`). Precisa de `status 'rascunho'`, número pela sequência (#9 em diante) e `token` de 64 caracteres
     **previsível no falso** (ex.: derivado do número), senão o roteiro não sabe o endereço do `goto` do capítulo 12.
  2. **Sementes:** `quotes` + `quote_items` (cabeçalho completo: `total_cost`, `total_value`, `bdi`, `view_count`, `last_viewed_at`, `receivable_installments`), `pricing_settings` (zeros), `proposal_templates`,
     `service_types` (T4), `inventory` + `inventory_stock_levels` com custo e venda (T8), `employees`, `financial_accounts`, `financial_categories`. Nenhuma dessas tem linha hoje.
     `company_settings` sem as colunas de aprovação cai em "Vou receber depois" e "link sem financeiro" (o esperado).
  3. **Provedor da view `cost_resources_with_rate`** (`handlers/views/` está vazio): soma de `cost_resource_items.value` ÷ `monthly_hours`. Sem ele "Custos Globais" e o preço do serviço ficam vazios.
  4. **Handler `generate_service_order_from_quote`:** sem ele o toast "OS gerada com sucesso!" aparece e nada é criado. Cria a OS #17 ("agendada"), as linhas do orçamento da OS, os serviços por equipamento, e marca o orçamento "convertido".
  5. **Página pública (TRILHA 6):** handlers de `get_quote_public_payload`, `respond_quote_public` e `record_quote_view`, e `goto` para `/proposta/<token>?preview=1` **na mesma aba**. Sem eles a página mostra "Proposta não encontrada."
     Plano B (decisão 3): capítulos 12 e 13 só com o "Visualizar" e a lista.
  6. **Testar antes:** os embutidos da lista (`quotes?select=*,customers(...),quote_items(*),proposal_templates(...)`) e vigiar o `desconhecidos.log` (hoje nada do T9 foi exercitado).
  7. **Nada de download, nova aba nem envio de arquivo (TRILHA 6):** "PDF", "WhatsApp", "Abrir proposta em nova guia" e "Pagar" só aparecem (câmera, sem clicar); sem foto do recurso nem logo novo.
  8. **Limpar o armazenamento da sessão entre tomadas** (o aviso "Rascunho encontrado" reaparece depois de um ensaio interrompido).
  9. **Relógio (TRILHA 5):** "Válido até", "Documento gerado em", "visto há X" e a data do 1º vencimento dependem do relógio travado.
  10. **Endereço do app (TRILHA 7):** a mensagem do WhatsApp e o toast "Link da proposta gerado" (se a cópia falhar) mostram o endereço da página, hoje `127.0.0.1:8080`; usar o nome mapeado do T10/T12 ou não deixar esse texto na câmera.
- **Passos de teclado:** valores com vírgula (1,5; 67,00); no wizard, a quantidade do serviço é inteira (mínimo 1) e a do material aceita decimal.

## Pronúncias (testar num trecho curto e registrar em `config_narracao.json` e `PERFIL.md`)

BDI ("bê-dê-i"), HH ("agá-agá", "hora-homem"), Hi-Wall ("rai-uól"), Pix ("piks"), PDF ("pê-dê-éfe"), WhatsApp ("uótsapp"), Clean ("clin"), Vanguarda, Aurora, Prisma, A4 ("a quatro"),
R-410A ("érre quatrocentos e dez a"), Van 01 ("van zero um"), Brisa do Mar, Mirante, Brisatec, Aerovento, OS ("ó-ésse"), "R$ 1.666,67" (falar "mil seiscentos e sessenta e seis reais e sessenta e sete centavos").

## Riscos e decisões para o Kaik

1. **Ordem dos capítulos:** "motor primeiro" (recomendo: o BDI já aparece funcionando no orçamento) × a ordem da trilha (orçamento primeiro, custos depois). Na ordem da trilha o orçamento sai com o selo "Sem custos configurados" e o preço vira o padrão do tipo.
2. **Duração:** ~24 min contra ~45 da trilha. Se ficar longa, dividir em duas partes: preço (capítulos 0 a 9, ~14 min) e proposta e fechamento (10 a 16, ~10 min).
3. **Visão do cliente (12 e 13):** tentar a página pública por `goto` (depende dos handlers e do token previsível) ou ficar só no "Visualizar"? Recomendo tentar, com o plano B pronto.
4. **Gerar OS e estoque:** a aula diz que "Gerar OS" **não baixa estoque** e que aprovar **não lança custo** (o código e o banco dizem isso; a trilha e o Guia Técnico dizem o contrário). Confirmar a fala e abrir pedido de correção do Guia.
5. **Dois orçamentos (#9 e #2):** por causa da aprovação pelo link (cuidado "Aprovação no link"). Alternativa de um orçamento só: aprovar por dentro o #9 e pular o clique do cliente (perde o capítulo 12).
6. **Preços de materiais do T8:** custo e venda propostos aqui precisam entrar na semente do T8 (hoje o plano do T8 só diz "com custo e preço de venda"); sem preço de venda o orçamento usa o de custo.
7. **Brindes:** a trilha cita o custo de brindes; o modelo Clean **não imprime brindes**. Só mostrar a caixa "Incluir brindes neste orçamento", sem prometer brinde na proposta.
8. **Números do Resumo:** a "Sugestão pelo BDI" (R$ 735,00) fica abaixo do Total (R$ 1.000,00) porque a Carga de Gás não tem custo cadastrado e o material entra sem BDI. Aceito como momento didático; alternativa: cadastrar custo da Carga de Gás (+30 s no capítulo 4).
9. **"Gerar cobrança"** aparece no menu da linha e na janela "Proposta #N" (a semente tem Cobranças e conta Asaas ativa). Recomendo só passar a câmera e dizer que cobrança é outro tutorial (T19), sem clicar.
10. **Achados para o time do app (não corrigidos aqui):** [handoff] Precificação nova zerada (P6); "Salvar rascunho" rebaixa o status (P12); "Rejeitar" sem confirmação (P14); "Desfazer lançamento" apaga parcelas pagas (P15);
    Observações impressas (P9); Clean sem brindes (P18); "Expirado" só visual (P10); "Conversão" cai depois do Gerar OS (P11); aviso do sino sem destino (P31). **Segurança:** [handoff, segurança] quem tem o link da proposta pode ler custo e margem pela API aberta (P27, média, a confirmar);
    a calculadora de mão de obra mostra e grava o custo mensal dos funcionários sem checar papel (P28, baixa); a função pública devolve a alíquota de imposto (P29, baixa). **Nenhum vazamento entre empresas.**
