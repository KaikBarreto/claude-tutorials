# T11 · Produção · cobertura no 1.60.10

Auditoria só de leitura (18/11/2026). Roteiro escrito no 1.59.154 (`f37573ea0`); app lido no 1.60.10 (`5290be4cd`, em
`/dev/shm/ecoflix-src/src`). Caminhos abaixo relativos a `components/producao/`, salvo indicação. Não existe
`rec/varredura/t11.txt`: nada aqui foi visto na tela, tudo vem do código. Onde o texto final depende de formatação que
só a tela mostra, está marcado `[conferir na varredura]`.

**O que mudou de verdade.** Entre as duas versões, só quatro arquivos das telas da aula mudaram:
`pages/Producao.tsx` (as abas saíram da coluna da esquerda e viraram abas horizontais), `RecipeFormDialog.tsx` + `.css`
(a ficha técnica foi redesenhada: rótulos, ordem dos campos, botão de criar produto, lugar do "Excluir ficha"),
`ProductionByEmployeeReport.tsx` (a matriz avançada ganhou a chave "Peças | Jogos") e
`components/ui/responsive-dialog.tsx` (a ficha em linha não mostra mais título nem descrição). **Não mudaram**:
`ProductionOrderList`, `ProductionKanbanBoard`, `ProductionOrderDialog`, `ProductionOrderDetail`, `DailyEntryDialog`,
`FinalizeProductionDialog`, `ProductionReport`, `ProductionDetailReport`, `ProductionSettings`, `QuickConversionTab`,
`QuickConversionHistory`, `ProductionMachinesTab`, `lib/producao.ts`, `pages/MaterialHistory.tsx`, `ModuleUpsellScreen`,
os itens de menu e as três permissões da Produção. As notas de versão de 1.59.155 a 1.60.10 (`config/version.ts:19-116`)
não trazem nenhuma linha sobre Produção.

**Consequência.** Os capítulos 02, 03 e 04 (ficha) precisam de regravação e de seis falas trocadas; o cap01 troca uma
fala. Do cap05 ao cap13 a tela é a mesma do roteiro. O grosso deste documento é a seção 2: o roteiro deixou de fora
duas abas inteiras ("Conversão" e "Máquinas"), a perda padrão da ficha, a edição da ordem em andamento, a visão em
Lista, metade do relatório e seis das onze configurações.

## 1. Mudou no app (por capítulo)

| # | Cap. | No roteiro | No 1.60.10 (texto exato) | Onde |
| --- | --- | --- | --- | --- |
| M1 | 01 (L1, Tela e fala) e todos os "clique na aba" | "Do lado esquerdo ficam as abas"; zoom na coluna de abas | As seis abas são **horizontais, em cima do conteúdo**, com sublinhado na ativa (rótulo da ativa em negrito). Mesmos nomes e mesma ordem: "Ordens de Produção", "Conversão", "Fichas Técnicas", "Máquinas", "Relatório", "Configurações" | `pages/Producao.tsx:16-23,66-71` (`desktopVariant="underline"`) |
| M2 | 02 (L3) | Painel com o título "Nova ficha técnica" e a frase "Monte a receita: matérias-primas entram, o produto final sai." | Título e frase **não aparecem mais** na ficha em linha. No alto fica o campo do nome, grande e sem rótulo, com o texto de fundo **"Nova ficha técnica"** (vira o nome do produto depois de escolhido). Logo abaixo, a seção **"Receita de produção"** · **"Para produzir 1 unidade, estes materiais serão consumidos."** (o "unidade" vira a unidade escolhida: "Para produzir 1 Kg, ...") | `RecipeFormDialog.tsx:922,925-935,996-1001`; `components/ui/responsive-dialog.tsx:113-124` |
| M3 | 02 (L3, L4) | "Matérias-primas (entram) \*" à esquerda, a seta, o cartão "Produto final" | Bolinha verde **"1"** + **"O que entra"** · "Matérias-primas consumidas"; no meio a palavra **"vira"** com a seta; à direita o cartão **"2 · Resultado"** · **"Produto final"**. O cartão tracejado continua "Adicionar matéria-prima"; o seletor continua "Escolher material" | `RecipeFormDialog.tsx:1008-1013,1021,1030,1042-1043` |
| M4 | 02 (L5) | Cartão mostra "Fardo de alumínio" e "unidade de produção: pç"; seletor "Selecione o produto" sem rótulo | Nome do produto e **"Cada produção gera 1 {unidade}"**; o seletor ganhou o rótulo **"Produto que será produzido"** (texto de fundo igual, "Selecione o produto"; o campo escolhido mostra só o nome, sem o código). Sem produto: "Selecione o produto acabado abaixo" (igual) | `RecipeFormDialog.tsx:1052-1054,1058,1064-1073` |
| M5 | 02 (L6, zoom e fala) | Botão "+" (só ícone, título "Criar novo produto"); fala "esse botão de mais" | Botão de texto **"Cadastrar novo produto"** (com o "+" na frente), embaixo do seletor. O achado 1 e a nota do `propostas_fala.md` ("o + só aparece com o foco do teclado") deixam de valer: a ficha agora se ajusta à largura do painel (`RecipeFormDialog.css`, `@container`). Conferir a 1280 px na varredura | `RecipeFormDialog.tsx:1075-1086`; `RecipeFormDialog.css:1-52` |
| M6 | 02 (L7) | "A câmera sobe até 'Nome da ficha', vazio, com 'Fardo de alumínio' de placeholder" | É o campo grande do alto (M2), sem o rótulo "Nome da ficha" na tela. O texto de fundo vira "Fardo de alumínio" depois de escolher o produto | `RecipeFormDialog.tsx:928-935` |
| M7 | 03 (L1) | "Unidade de produção", embaixo da receita | **"Unidade produzida"**, agora **em cima**, antes da receita, ao lado de "Peças por jogo". Opções iguais ("Kg — Quilograma") | `RecipeFormDialog.tsx:955-977` |
| M8 | 03 (L1, L2, L6) | Total ao vivo "Consumo por Kg" · "1 Kg" (e "1,60 Kg" no Cobre mel) | Dois quadros no pé do cartão do produto: **"Rendimento"** · "1 Kg" e **"Consumo previsto"** · "1 Kg" (Cobre mel: "1,6 Kg"). Com insumos de unidades diferentes, o segundo mostra "N insumo(s)" | `RecipeFormDialog.tsx:1098-1110` |
| M9 | 03 (L4, Tela e fala) | "Peças por unidade de venda (ex.: jogo = 4)" | **"Peças por jogo"** (a palavra "jogo" é a do agrupamento configurado), texto de fundo "Opcional", agora em cima ao lado da unidade. As Configurações e a janela da ordem ainda dizem "Peças por unidade de venda" (`ProductionSettings.tsx:578`, `ProductionOrderDialog.tsx:796`): para o time do app | `RecipeFormDialog.tsx:978-989` |
| M10 | 04 (L1, L3) | "Coprodutos (saem junto) · opcional" | **"Outros resultados da produção · opcional"** · **"Sobras e coprodutos que também entram no estoque"**. O parágrafo ("Coproduto que vem da perda...") , o vazio ("Use quando a produção gera mais de um material (ex.: sobra reaproveitável).") e o cartão "Adicionar coproduto" são os mesmos | `RecipeFormDialog.tsx:1118-1157` |
| M11 | 03 (L6), 04 (edição da ficha) | "Excluir ficha" no rodapé, à esquerda | Na ficha em linha, **"Excluir ficha"** fica no alto à direita, na linha do nome (botão discreto, vermelho). O rodapé tem só "Salvar ficha", alinhado à direita | `RecipeFormDialog.tsx:936-952,502-540` |

Continua valendo o `propostas_fala.md` (cap06: mostrar o check da "Concluída" antes de editar a coluna; achados 3 a 10).
Os achados 1 e 2 (corte a 1280 px) precisam ser medidos de novo: a ficha mudou (M5) e as abas saíram da lateral (M1), o
que devolve largura ao quadro.

## 2. Falta cobrir

| # | O que é (rótulos do código) | Quando o cliente usa | Vale? |
| --- | --- | --- | --- |
| L1 | **Perda padrão por matéria-prima.** No cartão do insumo, "Perda padrão" abre "Quanto se perde deste insumo" (%, "Vazio = esta ficha não tem perda padrão.") e "Essa perda vira": "Nada, é perda pura (some, não volta pro estoque)" ou "Vira outro material (entra no estoque como sobra)" + "Escolher material da sobra" (botão "Criar novo material"). Prévia ao vivo: "De 100 Kg de X, 37,5 Kg viram Y." e "Na sua ficha: cada 1 Kg usa 1,6 Kg e devolve 0,6 Kg de Y.". Recolhido, o cartão mostra "Perde 37,5% → Y". Embaixo nasce o cartão do coproduto com o selo "Vem da perda" (`RecipeFormDialog.tsx:566-830,843-873`; `recipeLoss.ts:194-229`). No lançamento do dia a sobra vem preenchida em "Subprodutos" com o selo "Da ficha" e "· sugerido N Kg. Pode corrigir se a balança disser outro valor.", e a matéria-prima avisa "A ficha já conta 37,5% de perda deste insumo no valor sugerido: ..." (`DailyEntryDialog.tsx:1059-1075,1185-1196`) | Toda produção com sobra previsível: capa do fio, borra, rebarba | **Sim, capítulo novo** (P5). O roteiro mandou "não abrir". É o recurso que tira a digitação da sobra de todo dia |
| L2 | **Aba "Conversão".** "Produto \*", "Quantidade \*", painel "Resultado" (consumo, "Preço usado: R$ .../Kg · média de todas as compras já feitas", "Custo estimado total", "Custo estimado por peça"), botão "Confirmar" → "Produção registrada — custo/peça R$ ..."; "Histórico do período" com o botão "Estornar — devolve o insumo e retira o produto" → "Estornar esta produção?" → "Produção estornada — insumo e produto voltaram ao estoque" (`QuickConversionTab.tsx:380-548`; `QuickConversionHistory.tsx:185-318`) | Transformar material sem ordem, equipe nem lançamento, várias vezes ao dia | **Sim, capítulo novo** (P6). Aba inteira fora do roteiro; nenhuma outra aula mostra |
| L3 | **Aba "Máquinas".** "Cadastre as máquinas da sua produção pra identificar qual rodou cada ordem.", "Nova máquina", "Nome ou número da máquina" ("Ex.: Prensa 02"), avisos "Máquina adicionada", "Máquina renomeada", "Máquina desativada", "Já existe uma máquina com esse nome"; "Desativar "{nome}"?" (`ProductionMachinesTab.tsx:96-369`). Com máquina cadastrada: campo "Máquina" na ordem ("Nenhuma"), filtro "MÁQUINA" e "Ranking de máquinas" no relatório | Pátio com mais de uma prensa, moinho ou descascador | **Sim, capítulo novo curto** (P7) |
| L4 | **Editar ordem em andamento.** Lápis "Editar ordem" do cartão → "Editar ordem em andamento" · "Você pode mudar a equipe, a meta, a data, o responsável e a coluna. A produção já lançada nos dias anteriores é preservada."; ficha travada ("A ficha técnica e o produto que sai não mudam depois que a produção começou: ..."); equipe: "Pode incluir ou tirar gente com a produção já rolando. ..."; botão "Salvar ordem" → "Ordem atualizada" (`ProductionOrderDialog.tsx:731-741,757-762,915-920,721,659`; `ProductionKanbanBoard.tsx:188`) | Funcionário faltou, a meta mudou, trocou o responsável | **Sim, capítulo novo** (P4) |
| L5 | **Menu de cada dia lançado**: "Editar este dia" (abre "Editar lançamento do dia", botão "Salvar alterações", aviso "Lançamento atualizado — estoque ajustado") e "Excluir este dia" → "Excluir este lançamento?" · "O dia 10/11 sai da ordem e o total é recalculado. Se este dia já baixou estoque, a matéria-prima volta e o produto sai. Os outros dias ficam intactos." · "Excluir dia" → "Lançamento excluído" (`ProductionOrderDetail.tsx:524,532,711-735,365`; `DailyEntryDialog.tsx:772,838,856`) | Digitou o peso errado ontem; lançou o dia duas vezes | **Sim**, no P4. O roteiro só ensina a excluir a ordem inteira |
| L6 | **Produção em mais de um dia**: cada "Lançar produção do dia" vira uma linha em "Lançamentos" e soma em "Produzido até agora"; botão "Finalizar ordem" dentro da ordem (`ProductionOrderDetail.tsx:436,546,558`) | Lote que leva a semana | **Sim, uma fala** no P4 (sem lançar o segundo dia, para não mudar as contas) |
| L7 | **Visão "Lista"** das ordens: filtros "Período", "Produto" ("Todos os produtos", busca por código ou nome, "Limpar filtro"), "Status" ("Todos os status", "Rascunho", "Em andamento", "Concluída", "Cancelada"); menu da linha "Ver detalhes", "Editar", "Finalizar ordem", "Excluir"; vazio "Nenhuma produção com esses filtros" (`ProductionOrderList.tsx:293-299,318-372,390-396,507-530`) | Achar ordem antiga; o Kanban não filtra por data | **Sim**, no P4 |
| L8 | **Excluir ordem que tem lançamento e não foi finalizada**: "Atenção: esta ordem tem lançamentos. Ao excluir, todos os dias são estornados de uma vez — o estoque que já baixou volta ao normal. Esta ação não pode ser desfeita." (só na Lista, `ProductionOrderList.tsx:589`; no quadro o texto é o genérico, `ProductionKanbanBoard.tsx:1178`) | Ordem aberta por engano, já com dia lançado | **Só citar** (dica no fim do P4) |
| L9 | **Menu da coluna**: "Excluir coluna" → "Excluir coluna?" · "As ordens desta coluna serão movidas para a primeira coluna. Nenhuma produção é apagada." → "Coluna excluída" (`ProductionKanbanBoard.tsx:483,1120-1134,1024`) | Etapa que não se usa mais | **Sim, uma fala** no cap06 (P8), sem excluir |
| L10 | **Permissão "Ver Custos na Produção"**: "... Sem esta permissão o operador continua vendo as quantidades — só o dinheiro some" (tela, PDF e Excel) (`config/routes.ts:229`) | Encarregado lança sem ver custo | **Sim, uma fala** na dica do cap05 (P8). O passeio pelas permissões é da T2 |
| L11 | **Relatório, o que o roteiro não abre**: filtro "MÁQUINA"; gráfico com "Diário", "Semanal", "Mensal"; no "Ranking de produtos" a chave "Quantidade" / "Custo (R$)"; "Detalhamento por produto" com "Buscar produto..." e a linha que abre o rateio por funcionário; aba **"Lançamentos"** ("Ranking de máquinas", "Detalhamento por lançamento": "Data da produção", "Produto", "Quantidade", "Máquina", "Responsável", linha "Total", botão "Exportar PDF"); em "Por funcionário": "Exportar" ("PDF", "Excel (.xlsx)"), "Detalhamento por funcionário" ("clique numa linha para ver os produtos daquele funcionário", "Buscar funcionário...", "Ver todos (N funcionários)"), "Ver matriz completa (avançado)" (`ProductionReport.tsx:1145-1218,1306-1308,840-923,1396-1398`; `ProductionDetailReport.tsx:427-478`; `ProductionByEmployeeReport.tsx:695-705,921-953,1054-1100`) | Fechamento do mês, conferir quem produziu o quê | **Sim, trechos** no cap11 (P9) |
| L12 | **Matriz "Peças \| Jogos"** (novo no 1.60): na matriz avançada, a chave "Peças" / "Jogos" e o aviso "Atenção: N produto fica fora desta matriz porque não tem jogo configurado em todas as fichas do período. Use Peças para ver todos." (`ProductionByEmployeeReport.tsx:1117-1150`) | Só quem usa "Peças por jogo" | **Só citar** (a chave só aparece com ficha em jogos; o mundo não tem) |
| L13 | **Seis configurações que o roteiro só deixa passar na tela**: "Descontar o valor das sobras do custo de produção"; "Qual preço de compra vira o custo do produto" ("Como calcular": "Média de todas as compras", "Média de um período" + "Quantos dias considerar", "Preço da última compra"); "Exigir funcionário na ordem"; "Como você chama o agrupamento de peças" ("Nome (singular)", "Plural (opcional)"); "Lançar produção em jogos"; "Padrões de ficha e ordem" ("Unidade padrão de novas fichas", "Prefixo da numeração da OP", 'Ex.: "MP-"') (`ProductionSettings.tsx:405-416,436-486,496-498,519-565,574-580,719-752`) | Acertar o custo, a numeração e a unidade uma vez | **Sim, trecho falado** no cap12 (P10) |
| L14 | **Produção em jogos** (caso de uso inteiro): "Peças por jogo" na ficha, chave "Peças" / "jogos" na ordem e no lançamento, "= 40 peças", coluna "Jogos" e "Custo/jogo" no relatório | Quem fabrica peça e vende em conjunto | **Só citar** (P10 e a fala do cap03). O ferro-velho da aula não produz por peça; mostrar exigiria um produto novo no mundo. **Depende de decisão** |
| L15 | **De onde vem o custo estimado**: aviso âmbar na linha ("Sem preço pela régua configurada — usando ...") e a frase "N de M insumos não tinham preço pela régua configurada — o custo deles usa a fonte mais confiável disponível." (`ProductionOrderDialog.tsx:976-1012`) | Material sem compra no período | **Só citar** (uma frase no P10; no mundo a latinha tem compra) |
| L16 | **Excluir ficha**: "Excluir esta ficha técnica?" · "A ficha sai da lista e você pode criar outra para o mesmo produto. As ordens de produção já feitas continuam com o histórico." → "Ficha técnica excluída" (`RecipeFormDialog.tsx:1166-1186,369`) | Receita que não se usa mais | **Sim, uma dica** no cap04 (P3), sem excluir |
| L17 | **Travas da ficha e da finalização**: as cinco mensagens da ficha (inventário), mais as três da perda (`RecipeFormDialog.tsx:418-420`, `recipeLoss.ts:122-134`); "Lance ao menos um dia de produção antes de finalizar" e "Esta ordem ainda não tem lançamentos. ..." (`FinalizeProductionDialog.tsx:303,489`); "Ordem cancelada não pode ir para concluída" | Erro de preenchimento | **Só citar**: uma fala no cap10 (P8) sobre finalizar sem lançamento. As outras se explicam na tela |
| L18 | "Descartar este lançamento?" ao fechar com dados; "Observação (opcional)" do lançamento | | **Não**: a primeira se explica; a segunda não é gravada (achado do inventário) |
| L19 | Aba "Produção" dentro do cadastro do material (atalho para ficha e pacote) e as colunas de Produção na importação por planilha | | **Outra aula**: cadastro de materiais (T10). Aqui só a frase do P10 |
| L20 | Busca de fichas "Buscar ficha ou produto...", busca por código do produto na ordem, botão "Coluna", celular (botão flutuante "Produção") | | **Não**: a busca se explica; "Coluna" já é citado; a aula é desktop |

## 3. Proposta

Ordem sugerida dos capítulos: 00 a 09 (com P1 a P3), **P4** (novo, depois do 09), 10 a 13 (com P8 a P10), **P6**, **P5**,
**P7** (novos, depois do 13), recapitulação (P11). Os três novos do fim ficam depois do cap13 de propósito: não mudam
as sementes nem os números dos capítulos 05 a 13 (a ordem do fardo continua #3, o Kardex do fio continua com as mesmas
linhas, a janela da ordem continua sem o campo "Máquina").

### P1 · cap01, linha 1 (troca)

| Tela | Fala |
| --- | --- |
| Zoom suave na faixa de abas, em cima: "Ordens de Produção", "Conversão", "Fichas Técnicas", "Máquinas", "Relatório", "Configurações" (sem clicar). | As abas ficam aqui em cima. São seis, e a gente passa por todas: Ordens de Produção, Conversão, Fichas Técnicas, Máquinas, Relatório e Configurações. |

### P2 · cap02 e cap03 (Tela nova; falas trocadas só onde indicado)

| Cap. · linha | Tela (1.60.10) | Fala |
| --- | --- | --- |
| 02 · L3 | Clique em "Nova": no painel da direita, o campo do nome com "Nova ficha técnica" de fundo, "Unidade produzida", "Peças por jogo" e a seção "Receita de produção" · "Para produzir 1 pç, estes materiais serão consumidos.", com "1 · O que entra", a palavra "vira" e o cartão "2 · Resultado" · "Produto final". | (igual) |
| 02 · L4 | Em "O que entra", "Adicionar matéria-prima" → "Escolher material" → "Alumínio latinha". | (igual) |
| 02 · L5 | No cartão "Produto final", em "Produto que será produzido" ("Selecione o produto"), "Fardo de alumínio"; o cartão mostra o nome e "Cada produção gera 1 pç". | (igual) |
| 02 · L6 | [ZOOM: o botão "Cadastrar novo produto", embaixo do seletor, sem clicar] | Se ainda não estiver, o botão Cadastrar novo produto cria o material sem sair da ficha. |
| 02 · L7 | A câmera sobe até o campo do alto, agora com "Fardo de alumínio" de fundo. | E o nome da ficha, aqui no alto, é opcional. Em branco, ela usa o nome do produto. |
| 03 · L1 | Em cima, em "Unidade produzida", troca "pç — Peça" por "Kg — Quilograma"; a receita passa a "Para produzir 1 Kg, ..." e o cartão a "Cada produção gera 1 Kg". | Agora as quantidades. Primeiro, a unidade produzida: o fardo é pesado na balança, então ele sai em quilo. |
| 03 · L2 | [ZOOM: o campo "Qtd"] digita 1; no pé do cartão do produto, "Rendimento" "1 Kg" e "Consumo previsto" "1 Kg". | (igual) |
| 03 · L4 | A câmera vai a "Peças por jogo", vazio ("Opcional"), ao lado da unidade. | Peças por jogo serve pra quem produz por peça e vende em conjunto, como um jogo de quatro. O fardo sai em quilo, então fica vazio. |
| 03 · L6 | "Cobre mel": o campo do alto mostra "Cobre mel"; "Fio de cobre encapado" com 1,6 "Kg"; "Consumo previsto" "1,6 Kg". | (igual) |

### P3 · cap04 (uma fala trocada e uma dica nova)

| Tela | Fala |
| --- | --- |
| (L1, troca) A câmera desce até "Outros resultados da produção · opcional" · "Sobras e coprodutos que também entram no estoque". | E quando sai mais de uma coisa do mesmo processo? Isso é o coproduto, e ele fica aqui embaixo, em Outros resultados da produção. |
| (nova, no fim) [ZOOM: o botão "Excluir ficha", no alto à direita, sem clicar] | Uma dica: o botão Excluir ficha, aqui no alto, tira a ficha da lista. As ordens que já foram feitas com ela continuam com o histórico. |

### P4 · capítulo novo, depois do cap09 · "Mexer na ordem em andamento" (vinheta: ORDENS)

Semente `apos-cap09`, FAKE_NOW 17:30. Nada é salvo: o capítulo termina no mesmo estado (o cap10 segue de `apos-cap09`).

| Tela | Fala |
| --- | --- |
| O quadro, "#3" "Em andamento" em "Na prensa". Passa o mouse no cartão e clica no lápis "Editar ordem" (ação antes da frase): "Editar ordem em andamento" · "Você pode mudar a equipe, a meta, a data, o responsável e a coluna. A produção já lançada nos dias anteriores é preservada." | A ordem já tem um dia lançado, e mesmo assim dá pra mexer nela. O lápis do cartão abre Editar ordem em andamento: a equipe, a meta, a data, o responsável e a coluna continuam livres. |
| [ZOOM: "Ficha técnica", travada, com "A ficha técnica e o produto que sai não mudam depois que a produção começou: o que já foi consumido e o que já entrou no estoque foram calculados por esta ficha."] | Só a ficha técnica fica travada, porque o que já foi consumido foi calculado por ela. |
| [ZOOM: "Equipe (quem vai produzir)" e o texto "Pode incluir ou tirar gente com a produção já rolando. Quem sair do time continua no relatório dos dias em que já produziu — só não aparece mais nos próximos lançamentos."]; fecha a janela sem salvar. | Faltou alguém, ou entrou outro no lugar? É só trocar na equipe. Quem sai continua no relatório dos dias em que produziu, e só deixa de aparecer nos próximos lançamentos. |
| Clique no cartão "#3": "Produção #3"; em "Lançamentos", abre o menu de três pontos da linha "10/11": "Editar este dia", "Excluir este dia". | Dentro da ordem, cada dia lançado tem o seu menu. Editar este dia reabre o lançamento pra corrigir um número. |
| Clique em "Excluir este dia": "Excluir este lançamento?" · "O dia 10/11 sai da ordem e o total é recalculado. Se este dia já baixou estoque, a matéria-prima volta e o produto sai. Os outros dias ficam intactos."; clica em "Cancelar". | E Excluir este dia tira só aquele lançamento: o total é recalculado, e o estoque daquele dia volta. Os outros dias ficam como estão. Aqui eu cancelo. |
| [ZOOM: "Produzido até agora" 480 Kg e o botão "Lançar produção do dia"] | Se a produção leva mais de um dia, é só lançar de novo amanhã. Cada dia vira uma linha, e o produzido até agora vai somando. |
| Fecha a ordem; no alto do quadro, clica em "Lista": aparecem "Período", "Produto" ("Todos os produtos") e "Status"; abre "Status": "Todos os status", "Rascunho", "Em andamento", "Concluída", "Cancelada" e fecha. | O quadro também vira lista. Na Lista aparecem os filtros de período, produto e status, bons pra achar uma ordem antiga. |
| Abre o menu da linha "#3": "Ver detalhes", "Editar", "Finalizar ordem", "Excluir"; clica em "Excluir": "Excluir ordem de produção?" · "Atenção: esta ordem tem lançamentos. Ao excluir, todos os dias são estornados de uma vez — o estoque que já baixou volta ao normal. Esta ação não pode ser desfeita."; "Cancelar". | O menu de cada linha tem as mesmas ações do cartão. E uma dica: excluir uma ordem que já tem lançamento estorna todos os dias de uma vez. O sistema avisa antes. |
| Volta para "Kanban" (o app guarda a última visão: o robô precisa voltar, senão o cap10 abre em Lista). | (sem fala) |

Mundo: nada novo. O backend falso só precisa responder às leituras da janela de edição (as mesmas do cap05).

### P5 · capítulo novo, depois do P6 · "Perda padrão: a sobra já sai calculada" (vinheta: FICHA TÉCNICA)

Semente `apos-cap13` (com o que o P6 deixar). Usa a ficha do Cobre mel: 1,6 Kg de fio para 1 Kg de cobre, logo 0,6 Kg de
capa, que é 37,5% do fio.

| Tela | Fala |
| --- | --- |
| "Fichas Técnicas" › "Cobre mel"; no cartão "Fio de cobre encapado", clica em "Perda padrão" (ação antes da frase): abre "Quanto se perde deste insumo" e "Essa perda vira". | Tem sobra que se repete em toda produção. No fio de cobre, a capa sai sempre na mesma proporção. Dá pra deixar isso na ficha, em Perda padrão, dentro do cartão da matéria-prima. |
| [ZOOM: "Quanto se perde deste insumo"] digita 37,5; embaixo, "Vazio = esta ficha não tem perda padrão.". | Em Quanto se perde deste insumo, trinta e sete e meio por cento: de um quilo e seiscentos de fio, seiscentos gramas são capa. |
| Em "Essa perda vira", marca "Vira outro material (entra no estoque como sobra)" (a outra opção é "Nada, é perda pura (some, não volta pro estoque)"); em "Escolher material da sobra", "Capa de fio". Aparece a prévia "De 100 Kg de Fio de cobre encapado, 37,5 Kg viram Capa de fio." e "Na sua ficha: cada 1 Kg usa 1,6 Kg e devolve 0,6 Kg de Capa de fio." [ZOOM: a prévia] | Depois, pra onde ela vai. Perda pura some, e não volta pro estoque. Aqui ela vira outro material, a Capa de fio. E a tela já confere a conta: de cem quilos de fio, trinta e sete e meio viram capa. |
| A câmera desce até "Outros resultados da produção": o cartão "Capa de fio" com o selo "Vem da perda" e "Sai da perda de Fio de cobre encapado. A quantidade é calculada no lançamento do dia, a partir do que foi consumido de verdade — e dá pra ajustar na mão."; clica em "Salvar ficha": "Ficha técnica salva". [BACKEND: `upsert_production_recipe_atomic` com `loss_pct` 37.5 e `scrap_material_id` da Capa de fio no insumo] | Repara embaixo: a Capa de fio apareceu sozinha, com o selo Vem da perda. Salvar ficha. |
| "Ordens de Produção" › "Nova produção": "Cobre mel", 40, equipe "Diego Morais", "Criar ordem": cartão "#4" em "A fazer". [BACKEND: `get_next_production_order_number` → 4] | Pra ver funcionando, crio uma ordem de quarenta quilos de Cobre mel, com o Diego. |
| Clique no "#4" › "Lançar produção do dia"; em "Diego Morais", 40. Em "Subprodutos", a linha "Capa de fio" já vem com 24 e, embaixo, o selo "Da ficha" + "37,5% de Fio de cobre encapado · sugerido 24 Kg. Pode corrigir se a balança disser outro valor." [ZOOM: essa linha] `[conferir na varredura: casas decimais do "sugerido"]` | No lançamento do dia, o Diego descascou quarenta quilos. E a capa já veio preenchida em Subprodutos: vinte e quatro quilos, calculados sobre o fio usado de verdade. Se a balança disser outro valor, é só corrigir. |
| Desce a "Matéria-prima usada": "Sugerido pela ficha: 64 Kg", "Real (Kg)" 64 e "A ficha já conta 37,5% de perda deste insumo no valor sugerido: 24 Kg do que foi usado hoje — vira Capa de fio em Subprodutos.". | Na matéria-prima, o sistema lembra que a ficha já conta essa perda. Como o fio usado bateu com a ficha, ele não pede motivo. |
| "Salvar lançamento": "Lançamento salvo — estoque ajustado". [BACKEND: `add_production_entry_atomic` (fio teórico 64, real 64; saídas Cobre mel 40 principal e Capa de fio 24; Diego 40); `stock_movements`: fio −64, cobre +40, capa +24] | Salvar lançamento. O fio saiu, e o cobre e a capa entraram no estoque, sem ninguém digitar a sobra. |

Mundo: material novo **"Capa de fio"** (grupo Outros, "Kg", estoque 0, preço de compra fictício a definir, entra no
`MUNDO_FICTICIO.md`); "Fio de cobre encapado" com pelo menos 64 Kg em `apos-cap13`; handlers das duas RPCs com os
campos de perda. Estado final muda: ordem #4 "Em andamento", ficha do cobre com perda.

### P6 · capítulo novo, depois do cap13 · "Conversão: produzir em um passo" (vinheta: CONVERSÃO)

Semente `apos-cap13`. Vem antes do P5 para a ficha do cobre ainda estar sem perda (pelo código, a Conversão só manda o
produto principal para o banco; o que o banco faz com a perda padrão não dá para ler daqui).

| Tela | Fala |
| --- | --- |
| Clique na aba "Conversão": à esquerda "Produto \*" e "Quantidade \*", à direita "Resultado" com "Selecione o produto e digite a quantidade para ver o consumo e o custo.". | Nem toda produção precisa de ordem, equipe e lançamento. Pra transformar um material em outro num passo só, existe a aba Conversão. |
| Em "Produto \*" ("Escreva o nome ou código do produto"), "Cobre mel"; em "Quantidade \*", 10. Em "Resultado": "Fio de cobre encapado" 16 Kg, "Preço usado: R$ 18,00/Kg · média de todas as compras já feitas", "Custo estimado total" R$ 288,00, "Custo estimado por peça" R$ 28,80. [ZOOM: o painel "Resultado"] [BACKEND: `get_material_cost_with_basis` do fio → `{cost 18.00, basis_used media_historica, is_fallback false}`] | Escolho o produto, que vem da ficha técnica, e digito a quantidade: dez quilos de Cobre mel. Do lado, o resultado aparece antes de gravar: vão sair dezesseis quilos de fio, e o custo fica em vinte e oito e oitenta por quilo. |
| Clique em "Confirmar": aviso "Produção registrada — custo/peça R$ 28,80"; o produto continua escolhido e a quantidade volta a vazio. [BACKEND: RPC `register_production_atomic` (planejado e produzido 10; consumo do fio 16) → `{total_material_cost 288, cost_per_unit 28.8}`; `stock_movements`: fio −16, cobre +10] | Confirmar. O estoque mexe na hora: o fio baixa, e o cobre entra. E a tela continua pronta, com o produto escolhido, pra lançar o próximo. |
| A câmera desce até "Histórico do período": a linha de hoje, "16 Kg de Fio de cobre encapado", "10 Kg de Cobre mel", R$ 288,00 e "R$ 28,80/un.". `[conferir na varredura: desenho da linha]` | Embaixo fica o histórico do período, com o que saiu, o que entrou e o custo. |
| Clique no botão de estornar da linha (título "Estornar — devolve o insumo e retira o produto"): "Estornar esta produção?" · "Atenção: o insumo baixado volta ao estoque e o produto creditado sai. Esta ação não pode ser desfeita."; confirma: aviso "Produção estornada — insumo e produto voltaram ao estoque". [BACKEND: a mesma RPC `delete_production_order_atomic` do cap13 (`QuickConversionHistory.tsx:180`)] | Lançou errado? O botão de estornar devolve tudo: o fio volta, e o cobre sai. |
| A câmera abre para a aba inteira. | Uma dica: a Conversão não tem equipe, nem real contra teórico, nem motivo de perda. Ela baixa exatamente o que a ficha manda. Precisa desse controle? Use a ordem de produção. |

Mundo: nada novo além dos dois handlers. Com o estorno, o estoque volta ao de `apos-cap13`.

### P7 · capítulo novo, depois do P5 · "Máquinas" (vinheta: MÁQUINAS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Máquinas": "Cadastre as máquinas da sua produção pra identificar qual rodou cada ordem." e "Nenhuma máquina cadastrada ainda."; clica em "Nova máquina"; em "Nome ou número da máquina" ("Ex.: Prensa 02"), digita "Prensa 01" e confirma: aviso "Máquina adicionada". [BACKEND: `INSERT production_machines`] | Se o pátio tem mais de uma máquina, vale cadastrar em Máquinas. Nova máquina, o nome, e pronto: Prensa zero um. |
| "Ordens de Produção" › "Nova produção": [ZOOM: o campo novo "Máquina", com "Nenhuma" e "Prensa 01"]; fecha sem criar. | A partir daí, a ordem ganha o campo Máquina. |
| "Relatório": [ZOOM: o filtro "MÁQUINA" ("Todas as máquinas")]; clica na aba "Lançamentos": "Ranking de máquinas". | E o relatório passa a filtrar por máquina e a mostrar o ranking de máquinas, na aba Lançamentos. |
| De volta a "Máquinas", passa o mouse na linha "Prensa 01" (lápis de renomear e o botão de desativar, sem clicar). | Uma dica: máquina que saiu de uso é desativada, e não apagada. Ela some das ordens novas e continua nas antigas. |

Mundo: nenhuma máquina na semente (o campo "Máquina" não pode aparecer nos capítulos 05 a 13); "Prensa 01" nasce ao vivo.

### P8 · falas soltas (cap05, cap06, cap10)

| Onde | Tela | Fala |
| --- | --- | --- |
| cap05, depois da dica das permissões | (a mesma câmera, no cartão) | E tem uma terceira, Ver Custos na Produção. Sem ela, a pessoa lança tudo e vê as quantidades, mas nenhum valor em reais. |
| cap06, depois de "O botão Coluna cria outra" | Abre o menu de três pontos da coluna "A fazer": "Editar", "Excluir coluna" (sem clicar); fecha. | E o menu de três pontos tem o Excluir coluna. As ordens dela vão pra primeira coluna, e nenhuma produção é apagada. |
| cap10, depois de "a ordem fecha assim mesmo" | (o mesmo zoom) | Só não fecha ordem sem nenhum dia lançado: o sistema pede pelo menos um lançamento. |

### P9 · cap11, trechos novos (Relatório)

| Tela | Fala |
| --- | --- |
| (L1, troca) ... "PRODUTO" em "Fardo de alumínio". | Agora o relatório. Em cima ficam os filtros: período, produto, funcionário e máquina. Escolho o Fardo de alumínio, neste mês. |
| (depois dos cartões) O gráfico "Peças produzidas · Fardo de alumínio"; clica em "Semanal" e volta a "Diário". | O gráfico mostra a produção no tempo, e os botões trocam entre diário, semanal e mensal. |
| (na aba "Por produto", antes da tabela) "Ranking de produtos": clica em "Custo (R$)" e volta a "Quantidade"; na tabela, clica na linha "Fardo de alumínio": abre o rateio com Cláudio Ferraz e Diego Morais. | No ranking dá pra comparar por quantidade ou por custo. E clicando numa linha da tabela, ela abre quem produziu aquele produto. |
| (em "Por funcionário", depois da meta) Desce a "Detalhamento por funcionário" ("clique numa linha para ver os produtos daquele funcionário"); clica em "Cláudio Ferraz"; desce a "Ver matriz completa (avançado)" e abre. | Mais abaixo, o detalhamento: clicando no nome, aparecem os produtos daquela pessoa. E em Ver matriz completa, o cruzamento de cada funcionário com cada produto. |
| Clique na aba "Lançamentos": "Detalhamento por lançamento" com "Data da produção", "Produto", "Quantidade", "Máquina", "Responsável" e o botão "Exportar PDF". | A terceira aba, Lançamentos, lista a produção por data, com produto, quantidade, máquina e responsável, e tem o seu próprio Exportar PDF. |

Mundo: nada novo (o rateio por funcionário e os lançamentos saem das mesmas leituras do cap11).

### P10 · cap12, trecho novo (as seis configurações que faltam)

Na ordem em que aparecem na tela; entram entre as falas atuais (a do multinível continua primeiro).

| Tela | Fala |
| --- | --- |
| [ZOOM: "Descontar o valor das sobras do custo de produção", desligado] | Descontar o valor das sobras do custo de produção. Desligado, toda a matéria-prima entra no custo do produto principal, e a sobra entra no estoque sem valor. Ligado, a sobra deixa de pesar no custo, e isso vale só da próxima produção em diante. |
| [ZOOM: "Qual preço de compra vira o custo do produto"]; abre "Como calcular": "Média de todas as compras", "Média de um período", "Preço da última compra"; fecha sem trocar. | Qual preço de compra vira o custo do produto: a média de todas as compras, que é o padrão, a média de um período, como os últimos trinta dias, ou o preço da última compra. Se faltar compra pra regra escolhida, o sistema usa a próxima fonte e avisa na tela. |
| [ZOOM: "Exigir funcionário na ordem", desligado] | Exigir funcionário na ordem obriga a informar a equipe antes de criar a ordem. |
| [ZOOM: "Como você chama o agrupamento de peças" ("Nome (singular)" com "jogo") e, embaixo, "Lançar produção em jogos"] | Quem produz por peça e vende em conjunto escolhe aqui o nome do agrupamento: jogo, caixa, fardo. E com Lançar produção em jogos ligado, a quantidade é digitada em jogos, e o sistema converte pra peças. |
| (no fim, depois da meta) [ZOOM: "Padrões de ficha e ordem": "Unidade padrão de novas fichas" e "Prefixo da numeração da OP"] | Por fim, os padrões: a unidade que já vem nas fichas novas, e um prefixo pra numeração das ordens. |

### P11 · cap14 (recapitulação), uma linha a mais

| Tela | Fala |
| --- | --- |
| (montagem: a edição da ordem, a aba Conversão, a perda padrão, a aba Máquinas) | E ainda viu como mexer numa ordem em andamento, a Conversão em um passo, a perda padrão que já calcula a sobra e o cadastro de máquinas. |

A linha 2 da recapitulação continua valendo; a linha 4 continua valendo.

## 4. Estimativa

| Bloco | Palavras de fala a mais | Segundos (2,6 palavras/s) |
| --- | --- | --- |
| P1 a P3 (trocas e a dica do Excluir ficha; líquido) | ~45 | ~17 |
| P4 Mexer na ordem em andamento (novo) | ~208 | ~80 |
| P5 Perda padrão (novo) | ~209 | ~80 |
| P6 Conversão (novo) | ~153 | ~59 |
| P7 Máquinas (novo) | ~69 | ~27 |
| P8 falas soltas | ~60 | ~23 |
| P9 Relatório (líquido) | ~90 | ~35 |
| P10 Configurações | ~164 | ~63 |
| P11 recapitulação | ~27 | ~10 |
| **Total** | **~1.025** | **~395 s de fala (cerca de 6,5 min)** |

**Capítulos novos: 4** (P4, P5, P6, P7), com 2 vinhetas novas de área (CONVERSÃO, MÁQUINAS). Com as esperas de tela, a
aula vai de ~16 para ~24 min. Regravar: cap01 a cap04 (mudança do app), cap05, 06, 10, 11, 12 e 14 (falas novas).

## Depende de decisão

1. **Onde fica a Perda padrão.** Proposto no fim (P5), para não mexer nas sementes. A alternativa didática é colar no
   cap04, junto do coproduto, o que obriga a refazer as sementes de `apos-cap04` em diante.
2. **Fardo com perda padrão em vez de coproduto avulso.** O caso da aula (lata de aço no meio da latinha virando
   chaparia) é exatamente o que a perda padrão resolve: com 3% na latinha, a chaparia viria sugerida (14,94 Kg sobre os
   498 Kg reais). Trocar deixa a história mais redonda, mas reescreve os capítulos 04 e 07. Mantido como está.
3. **Material novo "Capa de fio"** no mundo fictício (nome, grupo e preço).
4. **Produção em jogos (L14)**: só citada. Demonstrar pede um produto por peça, que o ferro-velho da aula não tem.
5. **Duração**: ~24 min. Se for demais, a divisão natural é uma segunda aula com P6, P5 e P7 ("Produção: conversão,
   perda padrão e máquinas").

## Para o time do app (achados da leitura)

- "Peças por jogo" na ficha, mas "Peças por unidade de venda" nas Configurações e no aviso da ordem
  (`ProductionSettings.tsx:578`, `ProductionOrderDialog.tsx:796`, `QuickConversionTab.tsx:417`).
- O aviso de exclusão de ordem com lançamentos só existe na Lista; pelo quadro, a mesma ordem mostra o texto genérico
  "A ordem será excluída permanentemente." (`ProductionKanbanBoard.tsx:1178` × `ProductionOrderList.tsx:589`).
- O texto da equipe continua dizendo "Na finalização você informa quanto cada um produziu"
  (`ProductionOrderDialog.tsx:912`); quem informa é o lançamento do dia.
