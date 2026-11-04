# Roteiro T9 · Orçamentos, Precificação e Proposta

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T09/inventario.md`).
Aula no computador (janela de 1024 px ou mais), logada como Camila Duarte (admin) do começo ao fim; só o cap12 sai da área logada (página pública da proposta, por `goto` na mesma aba).
Todos os nomes, valores e datas são fictícios; "Válido até", "visto há X", "Documento gerado em" e o 1º vencimento são relativos ao dia da gravação (relógio travado no `FAKE_NOW`).

- **Título final:** Orçamentos, Precificação e Proposta
- **Vinhetas (áreas):** ORÇAMENTOS · PRECIFICAÇÃO · CUSTOS GLOBAIS · CUSTOS DOS SERVIÇOS · PROPOSTA · APROVAÇÃO · ORDEM DE SERVIÇO · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Estoque, compras e inventário (T8)
- **Próximo:** CRM: funil, leads e captação (T10)
- **Duração estimada:** ~19 min de vídeo (2.369 palavras de fala, ~15,2 min de voz a 2,6 palavras/s, mais vinhetas e pausas do robô; o plano previa ~24 min contando o tempo do robô, a fala segue o tempo natural)
- **Estado inicial (fim do T8):** Glacial Cold Brasil, Camila Duarte (admin) logada, OS #1 a #16, tipos de serviço do T4 (Higienização de Split R$ 180,00, Carga de Gás R$ 350,00, Manutenção Preventiva R$ 180,00, Instalação de Split R$ 650,00...),
  estoque do T8 (doze materiais, EST-001 a EST-012, no Estoque Principal e na Van 01) com os custos e preços de venda fixados lá (R-410A 90,00 e 150,00; Limpa-evaporador em spray 20,00 e 38,00; Fita isolante 6,50 e 11,00; Mangueira de dreno 3,50 e 8,00), conta "Conta Principal" no Financeiro.
  **Pousada Brisa do Mar** (base) com três equipamentos: Hi-Wall 9.000 BTUs - Suíte 1 e Suíte 2 (Brisatec) e Hi-Wall 12.000 BTUs - Recepção (Aerovento). Todos os módulos ligados; nenhum cadeado nesta aula.
  **Entra por seed de bastidor (`seeds-extra/t9/`), antes do cap01:** `pricing_settings` da empresa **com zeros** (a aula preenche); `proposal_templates` com as quatro linhas (Clean, Vanguarda, Aurora, Prisma); `employees` com custo mensal fictício;
  categoria de receita "Vendas de Serviços"; **oito orçamentos históricos** (datas relativas ao dia): #1 Padaria Bom Grão Aprovado 640,00 · #2 Hotel Mirante do Mar **Enviado 3.200,00, 3 visualizações, 3 parcelas** (é o do cap14) ·
  #3 Clínica Sorriso Leve Rascunho 540,00 · #4 Academia Ponto Forte Rejeitado 1.850,00 · #5 Restaurante Sabor da Serra Aprovado 780,00 · #6 Mercado Vila Nova Enviado 1.450,00 (1 visualização) ·
  #7 prospecto Casa de Repouso Vida Mansa Enviado 980,00 (sem visualização) · #8 Escritório Lemos & Prado Rascunho 2.100,00. Os aprovados do histórico vieram do link, por isso sem "No financeiro" e sem OS (nenhum "Convertido").
- **Criado ao vivo:** taxas da Precificação (6 / 12 / 22, R$ 1,50 por km, 5% à vista, 10 parcelas); recurso **Van 01** (R$ 20,00/h); custos do tipo **Higienização de Split** (R$ 108,00; preço sugerido R$ 180,00); configuração da proposta (Clean, logo 120%, seção "Garantia" ligada);
  orçamento **#9 da Pousada Brisa do Mar**: Higienização de Split × 3 + Carga de Gás × 1 (R$ 890,00), R-410A 1 kg (R$ 150,00), deslocamento 18 km (custo R$ 27,00, preço R$ 45,00 na 1.38.19), desconto R$ 85,00, **Total R$ 1.000,00** (Rascunho, Enviado, Aprovado pelo cliente, Convertido);
  aprovação do #2 em três parcelas; **OS #17**, "Agendada", sem data nem técnico.
- **Estado final:** Precificação salva, Van 01, custos da Higienização, proposta configurada, #9 Convertido (OS #17), #2 Aprovado com o selo "No financeiro" (três parcelas pendentes em Contas a Receber) e o resto do histórico como semeado.
  Vira `seeds-extra/t9/apos-cap16.json`; o T10 parte dele; atualizar `MUNDO_FICTICIO.md`.
- Decisões padrão: ordem "motor primeiro" (Precificação, Custos Globais, Custos dos Serviços, orçamento, proposta, aprovação, OS), como recomenda o plano; visão do cliente por `goto` na mesma aba, com plano B (cap12 e cap13 só com "Visualizar" e a lista);
  dois orçamentos de propósito (o #9 mostra o link do cliente e a OS; o #2 mostra a aprovação por dentro, porque aprovado pelo link o item "Aprovar orçamento" some); aprovar e "Gerar OS" não lançam custo nem baixam estoque (falado);
  as duas somas do orçamento ficam diferentes de propósito (1.38.19: "Preço sugerido" R$ 1.085,00 = (3 × 108,00 + 27,00 do deslocamento) ÷ 0,6 = 585,00 dentro do BDI automático, mais 500,00 fora do BDI, que são a Carga de Gás 350,00 e o R-410A 150,00 a "Preço cadastrado"; o "Preço praticado" é R$ 1.000,00 depois do desconto de R$ 85,00; valores a confirmar na tela);
  vinhetas do assistente em ORÇAMENTOS (o plano usava o singular); da caixa "Incluir brindes neste orçamento" só se fala que ela existe (o Clean não imprime brindes); "Observações" é texto para o cliente (sai impresso);
  nada de clique em "PDF", "WhatsApp", "Abrir proposta em nova guia", "Baixar PDF", "Pagar" e "Gerar cobrança" (a câmera só passa), nem em "Rejeitar", "Editar", "Excluir" e "Desfazer lançamento"; sem foto de recurso nem logo novo; sem preço de plano;
  Precificação e Custos Globais valem para todo plano (sem cadeado).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[ILUSTRAÇÃO: ...]` (nenhuma nesta aula).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Orçamentos, Precificação e Proposta". | (sem fala) |
| Dashboard da Dominex, logado como Camila Duarte (Glacial Cold Brasil); a câmera desliza pelo menu lateral e para em "Orçamentos" (item solto, entre "Área do Técnico" e o grupo "Gestão"); clique: abre a tela "Orçamentos". | Oi! Neste tutorial a gente vai montar um orçamento com o preço certo e mandar uma proposta que fecha negócio. |
| A câmera percorre as quatro abas da tela. | Primeiro, a gente ensina a Dominex a calcular o preço com os custos da empresa. Depois, monta o orçamento, entrega a proposta, aprova e transforma tudo em ordem de serviço. |
| Cartão discreto: "Antes: Estoque, compras e inventário". | Se você ainda não viu o tutorial Estoque, compras e inventário, dá uma olhada antes. [pause] Vamos olhar a tela. |

### cap01 · A tela e as quatro abas (vinheta: ORÇAMENTOS)

| Tela | Fala |
| --- | --- |
| Zoom no título "Orçamentos" ("Gerencie orçamentos, custos e precificação"), na barra de abas ("Orçamentos", "Custos dos Serviços", "Custos Globais" e "Precificação") e nos botões "Configurar Proposta" e "+ Novo Orçamento". [BACKEND: `TABLE_DEFAULTS.quotes` (status "rascunho", número pela sequência a partir do #9, `token` de 64 caracteres previsível); sementes de `quotes` e `quote_items` com o cabeçalho completo (`total_cost`, `total_value`, `bdi`, `view_count`, `last_viewed_at`, `receivable_installments`); testar os embutidos `quotes?select=*,customers(...),quote_items(*),proposal_templates(...)` e vigiar o `desconhecidos.log`] **[1.38.19, robô]** "Configurar Proposta" e "+ Novo Orçamento" sobem para a linha das abas, à direita, e só existem na aba "Orçamentos". | A tela tem quatro abas no topo: Orçamentos, Custos dos Serviços, Custos Globais e Precificação. A primeira é a lista dos orçamentos, e as outras três cuidam de calcular o preço. À direita ficam o Configurar Proposta e o Novo Orçamento. |
| Zoom nos cartões "Em Aberto", "Conversão" e "Ticket Médio". | Em cima, três cartões. O Em Aberto soma o valor das propostas enviadas que ainda esperam resposta. O Ticket Médio mostra o valor médio dos aprovados. E a Conversão compara os aprovados com os enviados, aprovados e rejeitados: o orçamento que já virou ordem de serviço sai dessa conta. |
| Clique no cartão "Em Aberto": a lista filtra por "Enviado". Abre o filtro "Status" dentro da busca, desmarca "Enviado" e a lista volta a mostrar todos. | Clicando no Em Aberto, a lista mostra só os enviados, e a Conversão faz o mesmo com os aprovados. Para voltar, tiro a marca do filtro de Status. |
| A câmera percorre a lista: colunas "Nº", "Cliente" (com o indicador de visualização), "Data", "Custo", "Valor", "Margem" e o selo de "Status"; clique em "Buscar por cliente, número ou telefone...", digita "hotel" e limpa o campo. | Cada linha traz o número, o cliente, a data, o custo, o valor, a margem e o status. Dá para buscar por cliente, número ou telefone. |

### cap02 · O BDI da empresa (vinheta: PRECIFICAÇÃO)

| Tela | Fala |
| --- | --- |
| Clique na aba "Precificação": o cabeçalho "Precificação" ("Taxas padrão aplicadas em todos os orçamentos via método BDI") e o cartão azul "Método BDI" com a caixa "Preço = Custo Total ÷ BDI". [BACKEND: `pricing_settings` da empresa com zeros no começo (empresa nova); `upsert` da gravação genérica] | Tudo começa pelo preço. Na aba Precificação, a Dominex usa o método do BDI: o preço é o custo total dividido pelo BDI, e assim imposto e despesas da empresa nunca ficam de fora. |
| Zoom no número grande "BDI atual" (1.0000) e nos campos "Imposto (%)", "Adm. Indireta (%)" e "Lucro Padrão (%)", todos em 0; digita 6, 12 e 22 (a vírgula e o ponto seguem o app). | Uma empresa nova começa com tudo zerado, e por isso o BDI vale um. Preencha e salve as taxas antes do primeiro orçamento, porque é delas que o preço sai. Imposto, seis por cento. Administração Indireta, doze por cento. Lucro Padrão, vinte e dois por cento. |
| O "BDI atual" passa a 0.6000; a barra de composição ganha a legenda "Imposto 6%", "Adm. 12%", "Lucro 22%" e "BDI 60.0%". **[1.38.19, robô]** os campos aceitam vírgula (`NumericInput`); "Salvar" só habilita depois de alterar algo e aparece "Há alterações de precificação ainda não salvas.". | O BDI atual vira zero vírgula seis: um menos quarenta por cento, que é a soma das três taxas. A barra mostra como o preço se compõe. |
| Bloco "Deslocamento e Pagamento": digita "Custo por KM (R$)" 1,5, "Desconto à vista (%)" 5 e "Parcelas (cartão)" 10; clique em "Salvar": toast "Configurações de precificação salvas!". | Embaixo, o deslocamento e o pagamento: um real e cinquenta centavos por quilômetro, cinco por cento de desconto à vista e até dez parcelas no cartão. Clico em Salvar. A partir daí, todo orçamento novo já nasce com essas taxas. |
| Cartão "Simulador de Preço" (selo "Tempo real"): "Custo do serviço" abre em 1.000; a câmera passa pelos cartões "Deslocamento", "Custo Total", "BDI" e "Lucro Esperado" e para no destaque "Preço Final (BDI)" (R$ 1.666,67) e na linha "Preço = R$ 1.000,00 ÷ 0.6000 = R$ 1.666,67". **[1.38.19, robô]** o Simulador agora é a prévia "Composição" (barra empilhada, "Coeficiente" e "Custo dividido pelo coeficiente"); os cartões "Deslocamento", "Custo Total", "BDI" e "Lucro Esperado" não existem mais como cartões; o preço final R$ 1.666,67 continua. Reenquadrar a câmera. | À direita, o Simulador de Preço. Se um serviço custa mil reais, o preço final é mil seiscentos e sessenta e seis reais e sessenta e sete centavos, que é mil dividido por zero vírgula seis. Ele usa as taxas que já estão salvas. |

### cap03 · O custo da Van 01 (vinheta: CUSTOS GLOBAIS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Custos Globais": o título da página é "Centro de Custos" ("Cadastre veículos, ferramentas e recursos. O custo/hora é rateado automaticamente."); a faixa "Custo/hora Veículos", "Custo/hora Ferramentas", "Custo/hora EPIs" e "Custo/Brinde". [BACKEND: provedor da view `cost_resources_with_rate` em `handlers/views/` (soma de `cost_resource_items` ÷ `monthly_hours`, com os itens anuais ÷ 12); sem ele a aba e o custo por hora ficam vazios] | Agora, quanto custa o que você usa para trabalhar. Na aba Custos Globais, que na tela se chama Centro de Custos, a gente cadastra veículos, ferramentas e outros recursos, e a Dominex rateia o custo por hora, sozinha. |
| Clique em "Novo Recurso": a janela "Qual recurso deseja cadastrar?" com Veículos, Ferramentas, Brindes, EPIs e Outros (a câmera passa); clique em "Veículos". | Em Novo Recurso, a janela pergunta qual recurso eu quero cadastrar: veículos, ferramentas, brindes, EPIs ou outros. Vou de veículo. |
| Abre "Novo Veículo": em "Nome do veículo" digita "Van 01"; em "Horas de uso mensal (para rateio)" digita 176 (dica "Padrão: 176h (22 dias × 8h)"); em "Depreciação mensal" digita 1.400 e em "Manutenção + Combustível" digita 1.620. | Dou o nome, Van 01. As horas de uso por mês: cento e setenta e seis, que são vinte e dois dias de oito horas. A depreciação é de mil e quatrocentos reais por mês, e a manutenção com combustível, mil seiscentos e vinte reais. |
| Em "Seguro" digita 3.600 e em "Documentação / IPVA" digita 2.400, com a chave "Valor anual (÷12)" ligada nas duas linhas; zoom no cartão "Resumo": "Total mensal:" R$ 3.520,00 e "Custo/hora:" R$ 20,00. [TESTAR: as chaves "Valor anual (÷12)" vêm ligadas nessas duas linhas; senão o robô liga] | O seguro, de três mil e seiscentos reais, e o IPVA, de dois mil e quatrocentos reais, são valores anuais: a Dominex divide cada um por doze. No resumo, o total mensal fica em três mil quinhentos e vinte reais, e o custo por hora da van, em vinte reais. |
| Clique em "Salvar": a "Van 01" entra na lista "Recursos de custo" (selo "Ativo"); a faixa "Custo/hora Veículos" mostra R$ 20,00/h. Clique em "Van 01": o detalhe com "Custo mensal", "Horas mensais", "Custo por hora" e "Composição do custo". **[1.38.19, robô]** a ficha da Van 01 ganha o bloco "Seu custo por hora" / "Cliente paga com BDI por hora" e selos de categoria com ícone; os valores seguem. | Salvo. No alto, o custo por hora dos veículos já mostra vinte reais. E, clicando na van, vejo a composição do custo, item por item. |

### cap04 · Quanto custa executar um serviço (vinheta: CUSTOS DOS SERVIÇOS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Custos dos Serviços": o cabeçalho "Custos por Tipo de Serviço" ("Defina mão de obra e materiais para precificação automática."); no seletor "Tipo de serviço" escolhe "Higienização de Split" (bolinha de cor); a câmera passa pelas sub-abas "Mão de obra", "Recursos", "Materiais" e "Resumo". **[1.38.19, robô]** o desenho mudou: lista à esquerda ("Tipos de serviço", busca "Buscar tipo de serviço...") e ficha à direita, no lugar do seletor "Tipo de serviço"; as sub-abas são as mesmas. | Agora, o custo de cada serviço. Na aba Custos dos Serviços, escolho o tipo de serviço, a Higienização de Split. A tela tem quatro partes: mão de obra, recursos, materiais e resumo. |
| Sub-aba "Mão de obra": digita "Custo / hora (R$)" 32 e "Horas" 1,5; a caixa "Custo HH" mostra R$ 48,00 e o aviso verde "Salvo automaticamente" aparece. | Na mão de obra, o técnico custa trinta e dois reais por hora, e o serviço leva uma hora e meia. O Custo HH, ou hora-homem, fica em quarenta e oito reais. A tela salva sozinha. |
| Clique em "Calcular": abre "Calcular Custo de Mão de Obra" (selo "Calculadora de equipe"); a câmera passa por "Horas mensais base" e pela lista de funcionários; fecha em "Cancelar" (sem aplicar). [BACKEND: `employees` com custo mensal fictício; a lista mostra esses valores] | Se você prefere calcular a hora a partir da equipe, o botão Calcular abre uma calculadora com o custo mensal de cada funcionário. Como eu já sei o valor, fecho. |
| Sub-aba "Recursos": "Recursos Vinculados" (o grupo "Veículos" já vem aberto); marca "Van 01"; a linha ganha a conta "1.5h × R$ 20,00 = R$ 30,00"; a câmera para nela e no "Total recursos vinculados". | Em Recursos, vinculo a Van 01. Ela custa vinte reais por hora, e o serviço dura uma hora e meia: trinta reais. |
| Sub-aba "Materiais": em "Item do estoque (opcional)" ("Selecione do estoque") escolhe "Limpa-evaporador em spray", quantidade 1, "Adicionar"; repete com "Fita isolante" e "Mangueira de dreno"; a câmera para no "Total" (R$ 30,00). [BACKEND: `inventory` com o custo do T8 em cada item (20,00 + 6,50 + 3,50); esta tela usa o preço de custo] | Em Materiais, escolho do estoque um limpa-evaporador em spray, uma fita isolante e uma mangueira de dreno, um de cada. Aqui o material entra pelo preço de custo, e o total é trinta reais. |
| Sub-aba "Resumo": as caixas "Mão de obra", "Materiais", "Recursos" e "Extras manuais"; o cartão com "Custo total" (R$ 108,00), "Preço sugerido (BDI)" (R$ 180,00) e a linha "BDI: 0.6000" com "Lucro padrão: 22.00%". **[1.38.19, robô]** o resumo troca "Custo total" / "Preço sugerido (BDI)" por "Seu custo total para executar" / "Cliente paga com BDI"; as quatro caixas e os valores continuam. | No Resumo, a soma: quarenta e oito reais de mão de obra, trinta reais de recurso e trinta reais de material, ou seja, cento e oito reais de custo. Dividido pelo BDI, o preço sugerido é cento e oitenta reais. |
| (sem ação; a câmera fica no cartão de resumo) | Isso se faz uma vez só. Daí em diante, o preço sai calculado em todo orçamento. |

### cap05 · O destinatário (vinheta: ORÇAMENTOS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Orçamentos" e em "+ Novo Orçamento": abre "Novo Orçamento", com o `FormWizardStepper` de três etapas, "Montagem", "Condições comerciais" e "Revisão e envio" (a câmera passa pelos nomes). [TESTAR: limpar o armazenamento da sessão entre tomadas, senão aparece "Rascunho encontrado"] | Com o motor de preço pronto, vamos montar o orçamento. Em Novo Orçamento, o assistente tem três etapas, e a primeira é a Montagem, que começa pelo destinatário. |
| Etapa "Montagem", bloco "Destinatário": clique em "Novo prospecto": aparecem "Nome *", "Telefone" e "E-mail"; volta para "Cliente cadastrado". | Posso orçar para um cliente cadastrado ou para um prospecto, alguém que ainda não é cliente e só precisa de um nome. Ainda não é cliente? Orce como prospecto. |
| Em "Cliente *" ("Selecione o cliente") busca "Pousada" e escolhe "Pousada Brisa do Mar"; **sem "Próximo"** (1.38.19): a câmera desce para os serviços na mesma etapa "Montagem". | Hoje é cliente cadastrado: a Pousada Brisa do Mar. |

### cap06 · Serviços e preço (vinheta: ORÇAMENTOS)

| Tela | Fala |
| --- | --- |
| Ainda na etapa "Montagem": desce até o bloco "Configurações BDI" (caixa "Usar BDI" e selo "Coeficiente 0.6000"); **clique em "Ajustar taxas e entender o BDI"** para abrir os campos (o bloco vem recolhido; sem o clique a câmera não os vê): "Imposto %" 6, "Adm. Indireta %" 12, "Lucro %" 22, "Custo / km" 1,5, "Desconto à vista %" 5 e "Parcelas (cartão)" 10 (a câmera passa, sem mexer). | Descendo na mesma tela, chegam os serviços. No bloco Configurações BDI, o Ajustar taxas e entender o BDI mostra as taxas que salvei na Precificação. Elas valem só para este orçamento, e posso ajustar se precisar. |
| Em "Selecionar tipo de serviço..." escolhe "Higienização de Split"; em "Qtd:" digita 3; clique em "Adicionar": a linha entra com "Preço unit." R$ 180,00, modalidade "Custo + BDI" e coluna "Cliente paga / un.". [BACKEND: `service_costs`, `service_materials` e `service_cost_resources` do tipo, lidos pelo assistente; o preço é custo ÷ BDI] | Escolho a Higienização de Split e a quantidade, três, que são os três splits da pousada. O preço unitário já sai calculado: cento e oitenta reais, que é o custo de cento e oito reais dividido pelo BDI. |
| Clique no nome da linha: ela se expande com "Mão de obra", "Materiais", "Recursos e extras" e "Custo total unit."; fecha. | Clicando no nome do serviço, vejo de onde vem o preço: a mão de obra, os materiais, os recursos e extras, e o custo total de cada unidade. |
| Em "Selecionar tipo de serviço..." escolhe "Carga de Gás" (Qtd 1) e clica em "Adicionar": a linha entra com o selo âmbar "Sem custos configurados", modalidade "Preço cadastrado" e "Preço unit." R$ 350,00. | Agora a Carga de Gás. Esse serviço ainda não tem custo cadastrado, e a Dominex avisa com o selo Sem custos configurados. Nesse caso, o preço vem do preço padrão do tipo de serviço: trezentos e cinquenta reais. |
| Zoom no rodapé "Subtotal Serviços" (R$ 890,00). | O subtotal dos serviços fecha em oitocentos e noventa reais. |
| A câmera passa pelo campo "Preço unit." de uma linha (editável), sem digitar. | Uma dica: se você digita o preço na mão, ou muda a quantidade depois, aquela linha deixa de acompanhar as taxas do BDI. |

### cap07 · Materiais e deslocamento (vinheta: ORÇAMENTOS)

| Tela | Fala |
| --- | --- |
| **Sem "Próximo"** (1.38.19): desce até o bloco "Materiais" da mesma etapa "Montagem". Clique em "Adicionar materiais": abre o seletor em lote (busca "Buscar por nome, código ou categoria...", grupos "Mais usados" e "Todos"); digita "gás": a linha "Gás refrigerante R-410A" mostra "R$ 150,00 / kg" (entra como "Preço cadastrado", sem BDI). | Logo abaixo ficam os materiais. Em Adicionar materiais, busco gás e escolho o Gás refrigerante R-410A. O preço que aparece, cento e cinquenta reais por quilo, é o preço de venda cadastrado no estoque. |
| Aumenta a quantidade para 1 (botão "+"); o rodapé mostra "1 material" e "Total: R$ 150,00"; clique em "Adicionar ao orçamento": a tabela (Material, Qtd, Preço unit., Total) com o "Subtotal Materiais". | Coloco um quilo e adiciono ao orçamento. O material do estoque entra pelo preço de venda, sem BDI, e a lista não mostra saldo, porque orçar não consome estoque. |
| No bloco "Deslocamento" (fora do "Ajustar taxas") digita 18 em "Distância (km)"; "Modalidade" fica em "Custo por km + BDI"; embaixo aparece "Custo R$ 27,00 · Preço resultante R$ 45,00" e a câmera para nessa linha (1.38.19: o deslocamento no orçamento passa a valer R$ 45,00). | Embaixo, o deslocamento: dezoito quilômetros. A Dominex multiplica pelo custo por quilômetro, que dá vinte e sete reais de custo, e, na modalidade Custo por km mais BDI, o preço resultante é de quarenta e cinco reais. |

### cap08 · Desconto e condições (vinheta: ORÇAMENTOS)

| Tela | Fala |
| --- | --- |
| Clique em "Próximo": etapa "Condições comerciais". Em "Desconto" mantém "R$" e digita **85,00** (decisão do Tech Lead na 1.38.19: deslocamento R$ 45,00 + desconto R$ 85,00 mantêm o total em R$ 1.000,00 e a OS #17 em R$ 1.000,00): aparece "− R$ 85,00" em vermelho e, no resumo lateral, o "Preço praticado" fecha em R$ 1.000,00 (o "Preço sugerido" mostra R$ 1.085,00); alterna para "%" (a câmera mostra) e volta para "R$". | No Próximo, entram as Condições comerciais, com o desconto em reais ou em porcentagem. Dou oitenta e cinco reais, e o Preço praticado, aqui do lado, vai fechar em mil reais. |
| A câmera passa pela caixa "Incluir brindes neste orçamento" e pelo bloco "Cobrança após aprovação" com "Nº de parcelas" em "À vista" (sem alterar nada). | A caixa de brindes e o número de parcelas, em À vista, eu deixo como estão. |
| Em "Observações" digita "Atendimento de segunda a sexta, das 8h às 17h."; em "Condições / Termos" digita "Serviço executado após a aprovação, com data combinada com o cliente.". | Em Observações, escrevo o horário de atendimento. Em Condições e Termos, a regra do serviço: executado depois da aprovação, em data combinada com o cliente. |
| (sem ação; a câmera fica nos dois campos) | Repara que os dois textos saem na proposta do cliente: Condições e Termos aparece como Informações adicionais, e Observações aparece com o mesmo nome. Então escrevo pensando nele. |

### cap09 · Validade e revisão (vinheta: ORÇAMENTOS)

| Tela | Fala |
| --- | --- |
| Clique em "Próximo": etapa "Revisão e envio". Em "Válido até" escolhe, no calendário, a data de 15 dias à frente; "Template da Proposta" fica em "Clean" (bolinha de cor) e a "Capa da proposta" aparece ao lado, com o botão "Abrir proposta completa" (sem clicar). | Agora a última etapa, Revisão e envio. Em Válido até, marco quinze dias à frente: é a data que o cliente vê na proposta. O modelo é o Clean, com a Capa da proposta ao lado. |
| Zoom no painel lateral "Resumo do orçamento" (selo "BDI automático"): "Preço praticado" R$ 1.000,00, "Preço sugerido" R$ 1.085,00 e "Desconto − R$ 85,00"; depois o guia "O que entra no BDI?" com "Dentro do BDI automático" e "Fora do BDI automático" (Carga de Gás e R-410A, a R$ 500,00 juntos). Valores a confirmar na tela. | No resumo, aqui do lado, o Preço sugerido, mil e oitenta e cinco reais, é só uma referência para você. Logo abaixo, o guia O que entra no BDI mostra o que o BDI calcula sozinho e o que fica de fora, como a Carga de Gás e o gás, que entram pelo preço cadastrado. |
| Zoom em "Preço praticado" (R$ 1.000,00, em destaque no resumo lateral). | O que vale é o Preço praticado, mil reais: os preços das linhas, mais o deslocamento, menos o desconto. É o valor da proposta e da ordem de serviço. |
| Zoom em "Pagamentos" do resumo lateral: "À vista" (R$ 950,00) e "10x" (R$ 100,00), com "Lucro estimado" e "Margem" logo acima. | Embaixo, as opções de pagamento: novecentos e cinquenta reais à vista, com cinco por cento de desconto, ou dez parcelas de cem reais no cartão. |
| Clique em "Criar Orçamento": toast "Orçamento criado com sucesso!"; a janela fecha e a linha nova entra no topo da lista com o selo "Rascunho". | Clico em Criar Orçamento. Ele entra na lista como Rascunho, e ainda não foi para o cliente. |

### cap10 · Configurar a proposta (vinheta: PROPOSTA)

| Tela | Fala |
| --- | --- |
| Clique em "Configurar Proposta" (topo da tela): abre a janela de três etapas (barra e bolinhas "Modelo", "Personalização" e "Revisão"); na etapa "Modelo" ("Escolha o estilo visual da proposta enviada ao cliente.") a câmera percorre Clean, Vanguarda, Aurora e Prisma, com a capa A4 de cada um. | Agora, o documento que o cliente recebe. Em Configurar Proposta, o primeiro passo é o modelo: Clean, Vanguarda, Aurora ou Prisma, cada um com uma capa diferente. |
| A câmera volta para o "Clean" e fica na capa dele. | Aqui é só a prévia. O modelo de cada proposta, a gente escolhe dentro do orçamento, como acabei de fazer. Eu fico com o Clean. |
| Clique em "Próximo": etapa "Personalização". Em "Tamanho do logo" arrasta o controle para 120%; a câmera desce por "Cor Primária", "Cor de Destaque" e "Fundo do Cabeçalho" (sem mudar as cores) e pelas chaves "Mostrar paginação?" e "Mostrar deslocamento" (as duas em Sim). [BACKEND: o bucket `company-logos` existe no falso; não enviar logo novo] | Em Personalização, ajusto o tamanho do logo, que vem da empresa. Mais abaixo ficam as cores, a de destaque e a do cabeçalho, e as chaves para mostrar a paginação e o deslocamento. |
| Em "Seções da proposta" ("Ligue, desligue e reordene as seções."): a lista de sete seções, cada uma com ▲▼ e uma chave; liga "Garantia" e digita "Garantia de 90 dias sobre o serviço."; clica em ▲ na "Garantia" para subir uma posição. | Nas Seções da proposta, ligo, desligo e mudo a ordem de cada parte pelas setas, no modelo Clean. Ligo a Garantia e escrevo: Garantia de noventa dias sobre o serviço. Esse texto vira o padrão de todos os orçamentos. |
| Clique em "Próximo": etapa "Revisão" ("Veja como a proposta vai chegar ao cliente. Confirme em "Salvar"."); folheia as páginas A4 pelas setas "Página X/Y" do rodapé. | Na Revisão, folheio as páginas e vejo como a proposta chega ao cliente. É um exemplo, e não o orçamento da pousada. |
| Clique em "Salvar": toast "Configuração da proposta salva" (a janela continua aberta); fecha no X. | Salvo. O que eu salvo aqui vale para todas as propostas da empresa. A janela continua aberta, e eu fecho. |

### cap11 · Visualizar e gerar o link (vinheta: PROPOSTA)

| Tela | Fala |
| --- | --- |
| Menu "⋮" da linha do orçamento da "Pousada Brisa do Mar" → "Visualizar": abre a janela "Proposta #N" no modelo Clean (empresa, cliente, serviços e total); a primeira linha mostra "Não visualizada pelo cliente ainda". [TESTAR: "Documento gerado em" depende do relógio travado] | Antes de mandar, eu confiro. No menu da linha, Visualizar abre a proposta como o cliente vai ver, no modelo Clean. A primeira linha avisa que ele ainda não abriu. |
| A câmera passa pelos botões "Gerar cobrança", "WhatsApp" e "PDF" do canto (sem clicar); fecha a janela. [NÃO clicar: o PDF baixa arquivo e o WhatsApp abre outra aba] | No canto ficam o WhatsApp, que abre a conversa com a mensagem pronta, o PDF, que gera o arquivo, e o Gerar cobrança, assunto de outro tutorial. O envio é manual, e esses botões não mudam o status do orçamento. |
| Menu "⋮" da linha → "Gerar link da proposta": toast "Link gerado e copiado!" ("Já pode colar e enviar pro cliente."); o selo da linha passa de "Rascunho" para "Enviado". [TESTAR: se a cópia falhar, o toast mostra o endereço local; mapear o nome do produto (TRILHA 7) ou cortar o toast] | Para mandar de verdade, uso Gerar link da proposta. Ele copia o link, pronto para colar numa mensagem, e muda o orçamento para Enviado. É a partir daí que o cliente vê os botões Aprovar e Rejeitar. |
| Zoom no cartão "Em Aberto", que sobe. | Repara no cartão Em Aberto, que subiu: ele soma justamente as propostas enviadas. |

### cap12 · O que o cliente vê (vinheta: PROPOSTA)

| Tela | Fala |
| --- | --- |
| Navegação (`goto`, mesma aba) para a página pública da proposta, `/proposta/<token>?preview=1`: a página "Proposta Comercial" abre sem login, no Clean, com a empresa, "Orçamento #N" e o selo "Proposta válida até dd/mm/aaaa". [BACKEND: handlers de `get_quote_public_payload`, `respond_quote_public` e `record_quote_view`; token previsível; PLANO B: se não rodar, pular os cap12 e cap13 e ficar só com "Visualizar" e a lista] | Vamos ver do lado do cliente. Ele recebe o link e abre a proposta no navegador, sem precisar entrar no sistema. No alto, a empresa, o número do orçamento e a validade. |
| Rola devagar: o bloco "Cliente", as tabelas "Serviços" e "Produtos e materiais" e os totais ("Total dos serviços", "Total de materiais", "Subtotal", "Deslocamento", "Descontos" e "Total"). | Mais abaixo, os dados do cliente, os serviços e os materiais, com valor unitário, quantidade e subtotal, e os totais, com o deslocamento e o desconto. O total é o que a gente viu: mil reais. |
| Continua rolando: "Formas de pagamento" ("À vista no PIX" e "Parcelado no cartão"), "Informações adicionais", "Observações" e "Garantia"; o rodapé "Proposta preparada por Glacial Cold Brasil". | Depois, as formas de pagamento, à vista no Pix ou parcelado no cartão, as informações adicionais, as observações e a garantia que configurei. Tudo o que escrevi no orçamento está aqui. |
| Zoom no botão escuro "Baixar PDF" (canto inferior direito, sem clicar); a câmera chega aos botões "Aprovar" e "Rejeitar". | O cliente pode baixar a proposta em PDF. E, no fim, ficam dois botões, Aprovar e Rejeitar, que só aparecem porque o orçamento está como Enviado. |
| Clique em "Aprovar": a página mostra "✅ Proposta aprovada! Obrigado.". (Não clicar em "Rejeitar".) | Se ele aprova, basta um clique, sem precisar entrar nem se cadastrar. |
| Navegação (`goto`) de volta para `/orcamentos`: a linha da "Pousada Brisa do Mar" agora é "Aprovado" (verde), sem o selo "No financeiro". [TESTAR: o `goto` espera a lista carregada] | De volta à Dominex, o orçamento da Pousada já está Aprovado. Uma dica: quando o cliente aprova pelo link, a conta a receber só nasce sozinha se a opção Aprovação pelo link da proposta já gera conta a receber estiver ligada, em Configurações. |

### cap13 · Quem abriu a proposta (vinheta: PROPOSTA)

| Tela | Fala |
| --- | --- |
| Na lista, zoom na coluna "Cliente" da linha "Hotel Mirante do Mar": abaixo do nome, o olho com "3" e "visto há X"; passa o mouse: dica "Visualizada 3× · última vez dd/MM HH:mm (há X)". [BACKEND: `view_count` e `last_viewed_at` semeados no #2] | Outra informação útil fica na lista. Embaixo do nome do cliente, o olho mostra quantas vezes ele abriu a proposta e há quanto tempo. No Hotel Mirante do Mar, foram três vezes, e, passando o mouse, aparece o dia e a hora da última. |
| Zoom na linha "Casa de Repouso Vida Mansa (prospecto)" (Enviado): o olho apagado com "Não visualizada". | Já a proposta da Casa de Repouso Vida Mansa, que é um prospecto, ainda não foi aberta: o olho está apagado, com Não visualizada. |
| Abre o menu "⋮" de uma linha e a câmera passa pelo item "Abrir proposta em nova guia" (sem clicar); fecha o menu. | Quando você mesmo abre pelo item Abrir proposta em nova guia, a olhada do dono não conta. E a mesma pessoa, no mesmo navegador, só conta de novo depois de trinta minutos. |

### cap14 · Aprovar por dentro (vinheta: APROVAÇÃO)

| Tela | Fala |
| --- | --- |
| Na linha do "Hotel Mirante do Mar" (Enviado, R$ 3.200,00), menu "⋮" → "Aprovar orçamento": abre "Aprovar Orçamento #N", com "Valor: R$ 3.200,00" e os dois botões em pílula, "Já recebi" e "Vou receber depois" (este marcado, com a dica "Gera conta a receber pendente. O saldo da conta só muda quando você der a baixa."). [BACKEND: `financial_accounts` ("Conta Principal"), `financial_categories` ("Vendas de Serviços") e `financial_transactions` na gravação genérica] | E se o cliente fechar por telefone ou pelo WhatsApp, você aprova por dentro. Neste outro orçamento, o do Hotel Mirante do Mar, que está como Enviado, abro o menu e clico em Aprovar orçamento. |
| Zoom no subtítulo "Valor: R$ 3.200,00" e nos dois botões em pílula. | A janela mostra o valor, três mil e duzentos reais, e pergunta como o cliente vai pagar: Já recebi ou Vou receber depois. |
| Em "Vou receber depois": "Parcelas" 3x (vem do orçamento), "Primeiro vencimento", "Conta prevista do recebimento" e a lista "Parcelas que serão criadas" ("Parcela 1/3" e as seguintes, com "Total"). | No Vou receber depois, as três parcelas já vêm do orçamento. Escolho o primeiro vencimento, e a lista mostra cada parcela que será criada, nos mesmos dias dos meses seguintes. |
| Clique em "Já recebi": aparecem "Forma de pagamento *" (PIX), "Data do recebimento *", "Caixa / Conta bancária *" ("Conta Principal") e "Tarifa de máquina/gateway"; volta para "Vou receber depois". | Se o cliente já tivesse pago, o Já recebi pede a forma de pagamento, a data, a conta onde o dinheiro entrou e a tarifa, se houve. Aqui é a receber, então volto. |
| Clique em "Aprovar e gerar conta a receber": toast "Orçamento aprovado!" ("3 parcelas criadas em Contas a Receber. Dê a baixa conforme o dinheiro entrar."); a linha ganha o selo "No financeiro"; abre o menu da linha e a câmera passa por "Ver lançamento no financeiro". | Clico em Aprovar e gerar conta a receber. Pronto: três parcelas criadas em Contas a Receber, e a linha ganha o selo No financeiro. No menu, passa a existir o Ver lançamento no financeiro. |
| (sem ação; a câmera fica na linha aprovada) | Repara que a aprovação lança só a receita. O custo do orçamento serve para você enxergar a margem, e não vira despesa. |

### cap15 · Gerar a ordem de serviço (vinheta: ORDEM DE SERVIÇO)

| Tela | Fala |
| --- | --- |
| Na linha da "Pousada Brisa do Mar" (Aprovado), menu "⋮" → "Gerar OS": abre "Distribuir serviços · Orçamento #N" ("Defina em qual equipamento cada serviço será executado. Os checklists vinculados serão aplicados automaticamente."). [BACKEND: handler de `generate_service_order_from_quote` (cria a OS #17 "agendada", as linhas do orçamento da OS, os serviços por equipamento e marca o orçamento "convertido"); sem ele o toast aparece e nada é criado] | Voltando à Pousada, que aprovou pelo link: hora de gerar a ordem de serviço. No menu da linha, clico em Gerar OS. Antes, a Dominex pergunta em qual equipamento cada serviço será feito, e já aplica os checklists ligados a cada um. |
| Para "Higienização de Split": clique em "Todos" (marca "Hi-Wall 9.000 BTUs - Suíte 1", "Hi-Wall 9.000 BTUs - Suíte 2" e "Hi-Wall 12.000 BTUs - Recepção"); para "Carga de Gás": marca só o "Hi-Wall 12.000 BTUs - Recepção". | A higienização é nos três splits da pousada, e o botão Todos marca os três de uma vez. A Carga de Gás é só no split da recepção. |
| Clique em "Gerar OS": toast "OS gerada com sucesso!" ("Serviços, equipamentos, checklists, materiais e valores foram copiados."); a linha passa a "Convertido" (índigo). | Clico em Gerar OS. A ordem nasce com os serviços, os equipamentos, os checklists e o valor do orçamento, e o orçamento passa para Convertido. |
| Clique em "Ordens de Serviço" no menu lateral: a OS #17 no topo, com "Gerada do Orçamento #N", valor R$ 1.000,00 e status "Agendada". [TESTAR: o rótulo do status na lista de OS (inventário 7.6)] | Na tela de Ordens de Serviço, a OS número dezessete já está lá, agendada, no valor de mil reais. Falta só escolher o técnico e a data, como no tutorial de Ordens de Serviço. |
| (sem ação; a câmera fica na OS gerada) | Uma dica: o Gerar OS não mexe no estoque. O consumo de material é lançado na própria ordem, quando o técnico a executa. |

### cap16 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a "Precificação" com o "BDI atual", a "Van 01" nos Custos Globais e o "Resumo" dos Custos dos Serviços. | Pronto! Recapitulando: você ensinou a Dominex a calcular o preço. Salvou as taxas na Precificação, cadastrou a Van 01 nos Custos Globais e montou o custo da higienização, que virou preço pelo BDI. |
| Montagem rápida: as etapas do "Novo Orçamento" e o painel "Resumo do orçamento" com o "Preço sugerido" e o "Preço praticado". | Montou o orçamento em três etapas, com serviços, materiais, deslocamento e desconto, e viu a diferença entre o Preço sugerido e o Preço praticado. |
| Montagem rápida: o "Configurar Proposta", o "Visualizar", a página do cliente com "Aprovar" e o indicador de visualização. | Configurou a proposta, gerou o link, viu o que o cliente vê, aprovou com um clique e acompanhou as visualizações. |
| Montagem rápida: a janela "Aprovar Orçamento" com as parcelas e a janela "Distribuir serviços". | Aprovou outro orçamento por dentro, com as parcelas, e transformou o aprovado em ordem de serviço, distribuída pelos equipamentos. |
| Cartão "Próximo: CRM: funil, leads e captação"; cartela final. | Com o orçamento fechado, o próximo passo é encher o funil de novos clientes. No próximo tutorial, a gente vê o CRM. Até lá! |
