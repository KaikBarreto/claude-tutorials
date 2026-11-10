# Roteiro T10 · Estoque: saldo, histórico e posição

Roteiro pronto para a voz e a gravação (molde do T3 da Domiflix; sem etapa de aprovação). Coluna Fala = texto da narração
(voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela = o
que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código (`T10/inventario.md`, versão 1.59.154).
Aula no computador (janela 1280×800), logado como Rafael Nogueira (MASTER). Cada capítulo parte de um navegador novo,
com a semente indicada; quando um capítulo continua uma tela do anterior, o `setup` do robô a reabre fora do vídeo.

- **Título:** Estoque: saldo, histórico e posição
- **Antes:** Pedidos e histórico do caixa (T9)
- **Próximo:** Contas a Pagar e Receber (T13)
- **Vinhetas (áreas):** ESTOQUE · HISTÓRICO · RELATÓRIO · POSIÇÃO · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~15 min de vídeo (2.130 palavras de fala, ~13,7 min de voz a 2,6 palavras/s, mais 12 vinhetas,
  as ilustrações e as ações; alvo da fonte: 16 min)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça). O "dia 31" é 31/10, um sábado.
- **Sementes:** `inicio` (mundo base com a "Tabela Depósitos" do T3 e os valores de `plano.md` → "Mundo"; caps. 0 a 3) e
  `apos-cap03` (mais a transferência de 320 kg; caps. 4 a 12). Números falados que dependem da semente: caps. 2, 3, 4, 5,
  6, 8 e 10 (tabela em `plano.md`).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda precisa), `[ZOOM: ...]` (campo crítico, a frase
  inteira), `[ILUSTRAÇÃO: ...]` (desenho no estilo da marca, nunca tela do app).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Estoque: saldo, histórico e posição". | (sem fala) |
| [ILUSTRAÇÃO: as três perguntas do contador: uma silhueta genérica de contador com um balão; entram, um por vez com a fala, três cartões: "Quanto tem hoje?" (pilha de sucata com uma balança), "De onde veio?" (caminhão chegando com uma seta para a pilha) e "Quanto tinha no dia 31?" (calendário de outubro com o 31 marcado)] | Oi! Neste tutorial a gente vai responder as três perguntas que o contador da Recicla Vale Metais faz todo fim de mês. |
| (a ilustração segue: os três cartões acendem um a um, com "hoje", "veio" e "trinta e um") | Quanto material tem hoje no pátio, de onde ele veio e quanto tinha no dia trinta e um. |
| Dashboard do EcoSistema, logado como Rafael Nogueira (semente `inicio`); a câmera vai até "Materiais" no menu, sem abrir. | As respostas ficam no menu Materiais, em quatro telas que conversam entre si. |
| Cartão discreto: "Antes: Pedidos e histórico do caixa". | Se você ainda não viu o tutorial Pedidos e histórico do caixa, dá uma olhada antes. É de lá que vêm os pedidos que mexem no estoque. |

### cap01 · As quatro portas do estoque (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), no Dashboard; clique em "Materiais": abre "Estoque", "Histórico", "Relatório", "Ticket de Pesagem" e "Produção"; a câmera enquadra os três primeiros. | Vamos às quatro portas. Clicando em Materiais, aparecem as três primeiras: Estoque, Histórico e Relatório. |
| Clique em "Estoque": a tela "Estoque" abre com a coluna "Tabelas de Preço" à esquerda; a câmera desce pela coluna até "Posição de Estoque", embaixo de "Nova Tabela", sem clicar. [Com uma tabela de preço só, o botão "Posição de Estoque" fica no cabeçalho da tela: ver `plano.md`] | A quarta fica dentro do Estoque, aqui na coluna das tabelas de preço: a Posição de Estoque. |
| [ILUSTRAÇÃO: as quatro portas: quatro portas lado a lado com os rótulos reais "Estoque", "Histórico", "Relatório" e "Posição de Estoque"; embaixo de cada uma entra, com a frase, o que ela responde: "quanto tem agora", "cada entrada e saída", "o que comprou e vendeu no período", "quanto tinha numa data"] | O Estoque mostra quanto tem agora. O Histórico conta cada entrada e cada saída. O Relatório soma o que você comprou e vendeu num período. E a Posição mostra quanto tinha numa data. |
| De volta à tela "Estoque", quadro geral. | A gente começa pelo saldo de agora. |

### cap02 · O saldo de cada material (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em "Estoque"; a câmera nos três cartões de cima: "Peso Total em Estoque", "Total Pago" e "Projeção de Vendas". | Esta é a tela do saldo. Os três cartões de cima somam o pátio inteiro. |
| Zoom em "Peso Total em Estoque". | O Peso Total em Estoque é a soma do saldo de todos os materiais. |
| A câmera passa para "Total Pago" e "Projeção de Vendas". | O Total Pago é quanto esse estoque custou, pelo preço médio que você pagou. E a Projeção de Vendas é quanto ele vale pela tabela de venda. |
| A câmera desce para a "Lista de Materiais"; o mouse para na linha "Cobre mel". [ZOOM: "Estoque Atual" (212,500) e "Preço médio pago" (R$ 42,50) da linha "Cobre mel"] [BACKEND: `purchase_items` do Cobre mel todos a R$ 42,50, para o custo médio dar R$ 42,50] | Olha o cobre mel: duzentos e doze quilos e meio no Estoque Atual, pagos em média a quarenta e dois e cinquenta o quilo. |
| Mouse sobre o cabeçalho "Preço médio pago" (abre a explicação; a câmera fica no selo "estimativa", sem ler o texto). | Esse é o preço médio do material que você tem hoje. Por isso ele vem com o selo de estimativa. |
| [ILUSTRAÇÃO: o que mexe no saldo: no centro, uma pilha de sucata com "Estoque Atual"; entram setas com "Compra", "Transferência", "Entrada manual" e "Produção"; saem setas com "Venda", "Transferência", "Saída manual" e "Exclusão"; cada seta acende com a palavra] | O Estoque Atual é o saldo de verdade. Ele muda com tudo o que entra e sai: compra, venda, transferência, ajuste manual, exclusão e produção. |
| De volta à lista; a câmera na linha "Ferro misto" ("Estoque Atual" 6.420,000). | Então, quando alguém pergunta quanto tem, a resposta é aqui. O ferro misto, por exemplo, está com seis mil quatrocentos e vinte quilos. |

### cap03 · Transferir entre materiais (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em "Estoque"; entra a [ILUSTRAÇÃO: a separação no pátio: uma pilha "Ferro misto · 6.420 kg"; um ajudante tira as peças grossas; uma seta leva "320 kg" para a pilha "Ferro pesado · 2.180 kg"] | Agora, a transferência. Ontem, na separação, o Marcos tirou trezentos e vinte quilos de ferro pesado do meio do ferro misto. |
| (a ilustração segue: os números viram "6.100 kg" e "2.500 kg"; embaixo entra "o peso é o mesmo") | O peso é o mesmo, só mudou de material. A transferência registra isso: sai de um, entra no outro. |
| De volta à tela "Estoque"; mouse no "..." da linha "Ferro misto" (o menu abre ao passar): "Movimentar estoque", "Transferir estoque", "Editar" e "Excluir"; clique em "Transferir estoque". | Na linha do ferro misto, eu abro o menu e clico em Transferir estoque. |
| Janela "Transferir Estoque". [ZOOM: "Estoque Atual de Ferro misto" com 6.420,000 Kg] | A janela mostra o estoque atual do ferro misto: seis mil quatrocentos e vinte quilos. |
| Em "Material de Destino *" digita "ferro pes" e escolhe "Ferro pesado"; em "Quantidade a Transferir (Kg) *" digita 320. [ZOOM: "Quantidade a Transferir (Kg) *" com 320] | No material de destino, escolho o ferro pesado. E na quantidade, trezentos e vinte quilos. |
| Clique em "Transferir": aviso "Transferido 320,000 Kg de Ferro misto para Ferro pesado"; a lista atualiza e a câmera passa pelas linhas "Ferro misto" (6.100,000) e "Ferro pesado" (2.500,000). [BACKEND: RPC `transfer_material_stock`: tira 320 do Ferro misto, põe no Ferro pesado e grava duas linhas "TRANSFERENCIA" em `stock_movements` (6.420 → 6.100 e 2.180 → 2.500), `created_by` Rafael; vira `apos-cap03`] | Transferir. Pronto: o ferro misto ficou com seis mil e cem quilos, e o ferro pesado, com dois mil e quinhentos. |
| Marca as caixas de "Cobre mel" e "Cobre misto": aparece a barra embaixo com "2 selecionados" e "Transferir Estoque"; zoom na barra, sem clicar; depois desmarca as duas. | E quando você marca vários materiais, a barra de baixo traz o Transferir Estoque. Esse botão é outra coisa: ele leva material entre a matriz e a filial, e faz parte do Gerencial, que depende do plano contratado. |

### cap04 · O Kardex, linha a linha (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`), em "Estoque"; menu "Materiais" → "Histórico": "Histórico de Materiais", com "Geral (Todos)" marcado na coluna "Materiais" e a tabela de movimentações. [BACKEND: `stock_movements` com `stock_before`/`stock_after` encadeados e `created_at` = `transaction_at`; `profiles` para a coluna "Usuário"] | Agora o Histórico, de onde veio cada quilo. É o Kardex do estoque. |
| [ILUSTRAÇÃO: Kardex é um extrato: à esquerda, um extrato de banco genérico ("saldo anterior", "+ depósito", "saldo"); à direita, a mesma forma com sucata ("Estoque Inicial", "+ Movimentação", "Estoque Final"); as duas colunas entram lado a lado com a frase] | O Kardex é a ficha de cada material, como um extrato de banco. Cada linha é uma entrada ou uma saída, com o saldo antes e depois. |
| Na coluna "Materiais", clique em "Ferro pesado": o título do Kardex passa a mostrar o código e "Ferro pesado"; a linha de cima é a "Transferência" de hoje. | Escolho o ferro pesado aqui na coluna dos materiais. Repara que a transferência que a gente fez já está em cima. |
| [ZOOM: a linha "Transferência": "Estoque Inicial" 2.180,000 Kg, "Movimentação" +320,000 Kg e "Estoque Final" 2.500,000 Kg] | É só ler da esquerda pra direita: tinha dois mil cento e oitenta quilos, entraram trezentos e vinte, ficou com dois mil e quinhentos. |
| A câmera desce para a linha de baixo: a "Compra" de 09/11 (1.320,000 Kg, +860,000 Kg, 2.180,000 Kg). | A linha de baixo veio antes: uma compra de ontem, de oitocentos e sessenta quilos. O estoque final dela, dois mil cento e oitenta, é o inicial da transferência. |
| [ILUSTRAÇÃO: a corrente: as duas linhas empilhadas; uma seta liga o "Estoque Final" da compra ao "Estoque Inicial" da transferência e acende com "começo da seguinte"] | É uma corrente: o final de uma linha é o começo da seguinte. Assim dá pra seguir o material quilo a quilo. |
| A câmera sobe até o botão "Filtros" (sem contador) e mostra que a tabela só tem linhas de novembro. | Uma dica: o Histórico abre em Este mês. Hoje é dia dez, então ele mostra dez dias. |
| Clique em "Filtros": painel "Filtros do Kardex"; em "Período" abre a lista e escolhe "Este ano"; clique em "Aplicar filtros": entram agosto, setembro e outubro (a paginação cresce) e o botão "Filtros" mostra 1. | Pra ver mais, é só trocar o período pra Este ano ou Todos os tempos. Assim, quem abre a tela no dia dois não acha que o histórico sumiu: só estava vendo dois dias. |

### cap05 · Os tipos de movimentação (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`; o `setup` deixa "Ferro pesado" e o período "Este ano" aplicados); a câmera na coluna "Tipo": os selos "Transferência", "Compra" e "Venda" das primeiras linhas. | Cada linha tem um tipo, com uma cor. |
| Clique em "Filtros"; em "Tipo de movimentação" abre a lista: "Compra", "Venda", "Transferência", "Edição Manual", "Exclusão", "Produção" e "Saldo inicial". | No filtro de tipo aparecem todos os sete. |
| [ILUSTRAÇÃO: os tipos no pátio: cartões pequenos com o nome real e um desenho: "Compra" (carroça chegando), "Venda" (caminhão saindo), "Transferência" (seta de uma pilha para outra), "Edição Manual" (prancheta de contagem), "Exclusão" (pedido riscado com uma seta de volta), "Produção" (latinhas virando fardo, com um cadeado) e "Saldo inicial" (bandeira de largada); acendem "Compra", "Venda" e "Transferência"] | Compra é material que entrou porque você comprou. Venda é o que saiu porque você vendeu. Transferência tira de um material e põe em outro. |
| (a ilustração segue: acendem "Edição Manual" e "Exclusão") | Edição Manual é um ajuste feito direto no estoque, sem compra nem venda. Exclusão é quando um pedido é excluído, ou um material com estoque sai do cadastro: o saldo volta. |
| (a ilustração segue: acendem "Produção", com o cadeado, e "Saldo inicial") | Produção aparece pra quem usa a Produção, que depende do plano contratado: é a latinha que vira fardo, por exemplo. E o Saldo inicial é a quantidade com que o material entrou no sistema. |
| De volta ao painel: marca "Edição Manual" e "Exclusão"; clique em "Aplicar filtros": ficam a "Edição Manual" de 31/10 (−14,000 Kg) e a "Exclusão" de 22/10 (−180,000 Kg). [BACKEND: as duas linhas de `plano.md` → "Mundo"] | Vou deixar só esses dois tipos. No sábado, dia trinta e um, o Rafael contou o pátio e ajustou o ferro pesado: menos catorze quilos. |
| Clique na linha "Edição Manual": abre "Saída", "Observação" ("Contagem do pátio no fechamento do mês"), "Estoque" 1.874,000 Kg → 1.860,000 Kg, "Rafael Nogueira" e a hora. [ZOOM: "Observação" e "Estoque"] | Abrindo a linha, aparece a observação que ele escreveu, o estoque antes e depois, quem fez e a hora. |
| A câmera vai à linha "Exclusão" de 22/10 (−180,000 Kg). | E aqui, uma compra de cento e oitenta quilos que tinha entrado duas vezes. A repetida foi excluída, e o estoque voltou. |
| Clique em "Filtros": em "Tipo de movimentação" desmarca os dois; em "Fornecedores" marca "Depósito Irmãos Siqueira"; "Aplicar filtros": ficam as compras do Siqueira e as vendas. [BACKEND: filtro de parte pelos `order_id` de `purchases` (fornecedor) e `sales` (cliente)] | Uma dica sobre os filtros de Fornecedores e de Clientes: o de fornecedor mexe nas compras, e o de cliente, nas vendas. |
| A câmera passa pela lista, agora sem "Transferência", "Edição Manual" e "Exclusão". | Com um deles marcado, a transferência, o ajuste manual e a exclusão saem da lista, porque não têm fornecedor nem cliente. Não é erro. |
| Clique em "Filtros" → "Limpar filtros": a lista volta com tudo, em "Este mês". | Pra ver tudo de novo, é só limpar os filtros. |

### cap06 · O pedido por trás da linha (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`); "Materiais" → "Histórico" → "Ferro pesado" (período "Este mês"); clique na linha "Compra" de 09/11 (+860,000 Kg): abre a tabela "Material", "Peso", "Valor Unit." e "Total". [BACKEND: `purchase_items` da compra; view `orders_with_payments` com o Pix em `bank_payments`] | Toda linha de compra ou de venda abre o pedido que gerou ela. Clicando na compra de ontem, aparece o que veio. |
| [ZOOM: a linha do item: "Ferro pesado", "Peso" 860,000, "Valor Unit." R$ 0,95 e "Total" R$ 817,00] | Oitocentos e sessenta quilos de ferro pesado, a noventa e cinco centavos, deu oitocentos e dezessete reais. |
| A câmera desce para "Fornecedor:" (Depósito Irmãos Siqueira) e "Formas de Pagamento" ("Pix/Transferência: R$ 817,00") e para em "Total do Pedido:" (R$ 817,00). | Embaixo, o fornecedor, o Depósito Irmãos Siqueira, como foi pago, no Pix, e o total do pedido. |
| A câmera desce para "Fotos anexadas" (duas miniaturas); clique na primeira: a foto amplia; fecha. [BACKEND: `order_attachments` com 2 fotos fictícias (sucata de ferro numa caçamba, sem placa nem rosto) e URLs assinadas do bucket `order-attachments`] | E as fotos tiradas na hora da compra. Clicando, a foto amplia. |
| Quadro geral da linha aberta. | Quando o contador pergunta de onde veio o ferro, a resposta está aqui: o pedido, o pagamento e as fotos, na mesma linha. |

### cap07 · Comprado, vendido e lucro (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`); menu "Materiais" → "Relatório": "Relatório de Estoque", com o período em "Este mês". [BACKEND: RPCs `get_financial_dre_summary`, `get_inventory_report_data` e `get_orders_payment_distribution`] | Agora o Relatório de Estoque: tudo o que você comprou e vendeu num período. |
| Clique no período e escolhe "Mês passado": os cartões e a tabela passam para outubro. | Ele também abre em Este mês. Pra fechar outubro, escolho Mês passado. |
| Zoom no período "Mês passado". | Uma dica: o Relatório conta só os pedidos finalizados, pela data de cada pedido. Pedido excluído ou estornado fica de fora. |
| A câmera nos quatro cartões: "Total Comprado", "Total Vendido", "Lucro" e "Projeção de Lucro". | Em cima, quatro cartões: Total Comprado, Total Vendido, Lucro e Projeção de Lucro. |
| Clique em "Total Comprado": abre "Preço médio de compra", "Qtd. Comprada", "Materiais comprados" e "Material que mais comprou". | Clicando num cartão, ele abre os detalhes, como o preço médio de compra e o material que mais comprou. |
| Clique em "Projeção de Lucro" (selo "estimativa"): abre a explicação. | A Projeção de Lucro é uma estimativa. |
| [ILUSTRAÇÃO: a projeção: a pilha "comprado em outubro" passa toda para "vendido", com uma etiqueta "preço médio de venda"; aparece o cartão "lucro projetado" e, embaixo, "não desconta despesas"] | Ela imagina que você vendeu tudo o que comprou no mês, pelo preço médio de venda, ou pelo da tabela se o material não teve venda. É lucro bruto, sem as despesas. |
| [ILUSTRAÇÃO: Estoque × Relatório: dois cartões lado a lado: "Estoque" (o ferro pesado, 2.500 kg, com as setas de compra, venda, transferência, ajuste manual, exclusão e produção) e "Relatório de outubro" (só "comprado" e "vendido"); entre eles, um sinal de diferente] | Uma dica: o saldo da tela de Estoque não é o comprado menos o vendido daqui. |
| (a ilustração segue: as setas a mais do lado do Estoque acendem; do lado do Relatório, o calendário de outubro) | O Relatório só soma compras e vendas do período. O saldo vem acumulado desde o começo e muda também com transferência, ajuste manual, exclusão e produção. Quando os números não batem, é quase sempre isso. |

### cap08 · Material por material (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`; o `setup` deixa o período em "Mês passado"); a câmera desce até "Detalhamento por Material". | Embaixo dos cartões fica o detalhamento, material por material. |
| [ZOOM: a linha "Cobre mel": "Qtd. Comprada" 980,000, "Valor Comprado" R$ 41.650,00 e "Preço Médio Compra" R$ 42,50] | Olha o cobre mel em outubro: comprou novecentos e oitenta quilos, por quarenta e um mil seiscentos e cinquenta reais. Dividindo o valor pelos quilos, dá o preço médio de compra: quarenta e dois e cinquenta. |
| [ILUSTRAÇÃO: peso líquido: um saco de latinha na balança, "86 kg"; saem o saco (a tara) e a sujeira (a impureza), "6 kg" ao todo; sobra "80 kg", com os rótulos "Tara/Imp." e "Peso Líquido do Item", e o "80 kg" vai para o estoque e para o relatório] | Uma dica: a quantidade comprada daqui é a líquida, já sem a tara e a impureza. A Dona Cida pôs oitenta e seis quilos de latinha na balança. Tirando o saco e a sujeira, seis quilos, entraram oitenta quilos. Por isso esse número pode ser menor que o peso que você lembra de ter pesado. |
| De volta à tabela. [ZOOM: "Qtd. Vendida" 1.000,000, "Valor Vendido" R$ 47.900,00 e "Preço Médio Venda" R$ 47,90 da linha "Cobre mel"] | E o cobre mel vendeu mil quilos, por quarenta e sete mil e novecentos reais, a quarenta e sete e noventa em média. |
| [ILUSTRAÇÃO: resultado e margem: duas barras, "vendido R$ 47.900" e "comprado R$ 41.650"; a sobra "R$ 6.250" ganha o rótulo "Resultado"; depois a sobra vira uma fatia da barra do vendido: "13% = Margem"] | O Resultado é o vendido menos o comprado no mês: seis mil duzentos e cinquenta reais. E a Margem é esse resultado em porcentagem do que foi vendido: uns treze por cento. |
| De volta à tabela; mouse no cabeçalho "Lucro s/ Vendas" (abre a explicação, sem ler). [ZOOM: a célula "Lucro s/ Vendas" do Cobre mel, R$ 5.400,00] | Já o Lucro s/ Vendas olha só o que foi vendido: a diferença entre os dois preços médios, vezes os mil quilos. Dá cinco mil e quatrocentos. Também é estimativa. |
| A câmera desce até a linha "Bateria automotiva" ("Qtd. Comprada" 1.320,000; "Qtd. Vendida" 0,000). | Uma dica: material com muita compra e nenhuma venda, como a bateria automotiva, mil trezentos e vinte quilos comprados, não é erro. É material que entrou e ainda não saiu do pátio. |

### cap09 · O filtro de fornecedor (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`; o `setup` deixa o período em "Mês passado"); clique no filtro "Fornecedores" e marca "Depósito Irmãos Siqueira": os cartões ficam só com "Total Comprado" e a tabela, só com as colunas de compra. [BACKEND: `get_inventory_report_data` com `p_supplier_ids`, só os materiais com compra do Siqueira] | Agora repara o que acontece quando eu filtro por um fornecedor, o Depósito Irmãos Siqueira. Ficam só as compras. O Total Vendido, o Lucro e as colunas de venda saem. |
| [ILUSTRAÇÃO: a pilha não tem dono: o cobre misto do Siqueira (caminhão) e o do Valdir (carroça) caem na mesma pilha; depois o caminhão da Fundição Bandeira do Vale leva parte da pilha; sobre ela, "de quem era cada quilo?"] | É de propósito. O cobre misto do Siqueira foi pra mesma pilha do cobre do Valdir. Quando a Fundição compra, não tem como saber de quem era cada quilo. |
| Zoom na tabela, só com "Código", "Material", "Qtd. Comprada", "Valor Comprado" e "Preço Médio Compra". | Então, com esse filtro, o relatório responde uma pergunta: quanto você comprou do Siqueira, de cada material, e a que preço. |
| Abre "Fornecedores" e desmarca "Depósito Irmãos Siqueira": voltam os quatro cartões e todas as colunas. | Pra ver venda, lucro e margem, é só tirar o filtro. |

### cap10 · A foto do estoque numa data (vinheta: POSIÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`), em "Estoque"; na coluna "Tabelas de Preço", clique em "Posição de Estoque": a tela abre com "Escolha a data" em 10/11/2026 e 23:59 e a tabela "Posição de estoque em 10/11/2026 23:59". [BACKEND: RPC `get_stock_balance_at_date` (saldo em `p_at`, com `avg_cost` e `sale_price`, só saldo diferente de zero)] | E a terceira pergunta do contador: quanto tinha no dia trinta e um. A Posição de Estoque abre no dia de hoje, no fim do dia. |
| [ZOOM: a linha "Ferro pesado", "Saldo" 2.500,000] | Hoje, o ferro pesado está com dois mil e quinhentos quilos. |
| [ILUSTRAÇÃO: a foto numa data: uma linha do tempo de outubro a novembro com as movimentações do ferro pesado como pontos; uma câmera fotografa em "31/10 23:59"; os pontos de novembro (as compras, a venda e a transferência) ficam de fora, apagados] | A Posição é uma foto do estoque. Você escolhe a data e a hora, e ela mostra o saldo de cada material naquele instante. O que entrou ou saiu depois fica fora da foto. |
| Clique na data (10/11/2026): abre o calendário de novembro; clique na seta do mês anterior e no dia 31: a data vira 31/10/2026 e a hora fica 23:59. [ZOOM: "Data e hora (padrão: fim do dia)" com 31/10/2026 e 23:59] | Eu volto o calendário pra outubro e clico no dia trinta e um. A hora fica em vinte e três e cinquenta e nove, então entra tudo o que aconteceu no sábado. |
| Clique em "Ver posição": o título vira "Posição de estoque em 31/10/2026 23:59" e a tabela recarrega. | Ver posição. |
| [ZOOM: a linha "Ferro pesado", "Saldo" 1.860,000] | No dia trinta e um, o ferro pesado tinha mil oitocentos e sessenta quilos. A diferença pra hoje são as compras, a venda e a transferência de novembro. |
| A câmera passa pelas colunas "Valor" e "Projeção venda", pela linha "Total geral" e pela nota do rodapé ("Valor = saldo × custo médio das compras até a data. Projeção = saldo × preço de venda atual."). | Do lado, o valor desse estoque, pelo custo médio das compras até aquela data, e a projeção, pelo preço de venda de hoje. Embaixo, o total geral. |

### cap11 · Exportar para o contador (vinheta: POSIÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`; o `setup` deixa 31/10/2026 23:59 aplicado na Posição de Estoque); clique em "Exportar" → "PDF": janela "Exportar estoque (PDF)" com "Colunas do arquivo", "Grupos" e "Materiais". | Com a foto do dia trinta e um na tela, é só exportar. No Exportar, escolho PDF. |
| A câmera em "Colunas do arquivo" (as seis marcadas) e no rodapé ("<n> de <n> materiais"). [BACKEND: upsert em `stock_export_preferences`] | Aqui você escolhe as colunas e os materiais do arquivo. A tela guarda essa escolha pra próxima vez. |
| Clique em "Exportar": aviso "Posição de estoque exportada em PDF"; abre a aba nova com o PDF (o robô mostra a aba ~3 s, com "Baixar PDF" no canto, e volta). [BACKEND: nada; o PDF é feito no navegador e abre em aba nova (popup liberado no robô)] | Exportar, e o PDF abre numa aba nova, pronto pra baixar e mandar pro contador. |
| "Exportar" → "Excel": "Exportar estoque (Excel)" → "Exportar": aviso "Posição de estoque exportada em Excel" (o arquivo baixa). | Se o contador preferir planilha, o mesmo caminho em Excel baixa o arquivo. |
| Corte rápido: o botão "Exportar" do "Histórico de Materiais" aberto ("PDF", "Excel") e o botão "Exportar Relatório" do "Relatório de Estoque" (o robô grava cada um ~2 s, sem exportar). | O Histórico e o Relatório também exportam, cada um pelo seu botão. |

### cap12 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a lista do "Estoque" com o ferro misto e o ferro pesado depois da transferência. | Pronto! Recapitulando: a gente conferiu o saldo de cada material na tela de Estoque e transferiu trezentos e vinte quilos do ferro misto pro ferro pesado. |
| Montagem rápida: o Kardex do ferro pesado e a compra de 09/11 aberta, com as fotos. | Leu o Kardex linha a linha, conheceu os tipos de movimentação e abriu uma compra pra ver o pedido, o pagamento e as fotos. |
| Montagem rápida: o "Relatório de Estoque" de outubro, na linha do cobre mel. | No Relatório, viu o comprado, o vendido, o resultado e a margem do mês, e por que o filtro de fornecedor mostra só as compras. |
| Montagem rápida: "Posição de estoque em 31/10/2026 23:59" e a aba do PDF. | E tirou a foto do estoque do dia trinta e um, exportada em PDF e Excel pro contador. |
| Cartão "Próximo: Contas a Pagar e Receber"; cartela final. | No próximo tutorial, a gente cuida das contas que vencem: as que você paga e as que você recebe. Até lá! |
