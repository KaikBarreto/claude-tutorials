# Roteiro T9 · Pedidos e histórico do caixa

Pronto para a voz e a gravação (sem etapa de aprovação). Coluna Fala = texto da narração na grafia da legenda; a grafia
de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos
entre aspas como no código 1.59.154 (`T09/inventario.md`). Desktop, logado como Rafael Nogueira (administrador). Cada
capítulo parte de um navegador novo com a semente indicada (`plano.md`, "Gravação"). PDFs abrem em aba nova: o robô grava
a aba e volta.

- **Título:** Pedidos e histórico do caixa
- **Antes:** Ticket de Pesagem (T8)
- **Próximo:** Estoque: saldo, histórico e posição (T10)
- **Vinhetas (áreas):** PEDIDOS · CORREÇÕES · COMPROVANTES · HISTÓRICO · RESUMO
- **FAKE_NOW:** 11/11/2026 08:30 (quarta) em todos os capítulos.
- **Duração estimada:** ~12,5 min de vídeo (1.702 palavras, ~10,9 min de fala a 2,6 palavras/s, mais 10 vinhetas, os
  PDFs em aba nova e as ações; alvo da fonte ~12 min).
- Marcas: `[BACKEND: ...]`, `[ZOOM: ...]`, `[ILUSTRAÇÃO: ...]` (`docs/09-aula-ilustrada.md`), `[TESTAR: ...]` (o robô
  confere no ensaio).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Pedidos e histórico do caixa". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira. [ILUSTRAÇÃO: o telefonema: um telefone genérico tocando, com o cartão "Auto Peças Vale Forte"; um calendário volta três semanas até "21/10"; nesta frase] | Oi! Neste tutorial a gente vai achar aquele pedido de três semanas atrás, corrigir o que saiu errado e imprimir o comprovante de novo. |
| (ilustração: um balão "cadê o comprovante da bateria?" e, ao lado, uma pilha de comprovantes com um ponto de interrogação; a cena some) | Na Recicla Vale Metais, a Auto Peças Vale Forte ligou pedindo o comprovante da bateria que vendeu em vinte e um de outubro. E o pedido não aparece no nome dela. |
| Volta ao Dashboard; a câmera passa pelo menu lateral em "Pedidos" e em "Financeiro" › "Histórico do Caixa", sem clicar. | Pra resolver, a gente usa duas telas: Pedidos, no menu lateral, e Histórico do Caixa, dentro de Financeiro. |
| Cartão discreto "Antes: Ticket de Pesagem". | Se você ainda não viu o tutorial Ticket de Pesagem, dá uma olhada antes. [pause] Primeiro, o trabalho de cada tela. |

### cap01 · Duas telas, dois trabalhos (vinheta: PEDIDOS)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: pedido × caixa: à esquerda, uma pilha de comprovantes com "cada compra e cada venda"; à direita, gavetas de caixa lado a lado, cada uma com um nome e um dia ("Rafael · 10/11", "Marcos · 10/11", "Marcos · 21/10"); a pilha entra nesta frase] | Pedidos mostra cada compra e cada venda, uma por linha, de todos os caixas. É a tela pra achar um pedido, corrigir e imprimir de novo. |
| (ilustração: entram as gavetas; a "Marcos · 21/10" se destaca) | O Histórico do Caixa mostra os caixas já fechados: o dia de cada operador, com quanto abriu e quanto fechou. É a tela pra rever um dia inteiro e, se precisar, reabrir aquele caixa. |
| (ilustração: uma seta liga um comprovante da pilha à gaveta "Marcos · 21/10"; a cena some) | Todo pedido nasce dentro de um caixa. Por isso as duas telas andam juntas. |
| Volta à tela; clique em "Pedidos" no menu lateral: a tela "Pedidos" ("Histórico completo de compras e vendas"). | Vamos começar pelos pedidos. |

### cap02 · A tela Pedidos (vinheta: PEDIDOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), `/pedidos`; câmera no período "Este mês" e em "Todas as Ordens" ("N ordem(ns) • Exibindo 1-25 de N"). | A tela abre no mês atual, com todas as compras e vendas, de todos os caixas e de todos os operadores. |
| [ZOOM: o cartão "Resumo do período filtrado", com "Compras" e "Vendas" por forma de pagamento] | Em cima, o resumo do período: quanto saiu em compras e quanto entrou em vendas, separado em dinheiro, Pix e saldo. |
| O zoom solta; câmera nas colunas "Usuário", "Data", "Tipo", "N° Pedidos", "Cliente/Fornecedor", "Pagamento", "Valor" e "Ações". | Cada linha tem quem lançou, a data, se é compra ou venda, o número, o cliente ou fornecedor, como foi pago e o valor. |
| Clique na linha da compra de hoje de Aparecida Ramos (R$ 148,80): ela abre com "Material", "Peso", "V.Unit.", "Total" e "Formas de Pagamento" (Alumínio latinha, 24). | Clicando na linha, ela abre com os materiais, o peso, o preço e como foi pago. Aqui, a latinha da Aparecida, de hoje cedo: vinte e quatro quilos. Guarda esse número. |
| Câmera no "⋮" no fim da linha, sem abrir. | No fim de cada linha fica o menu do pedido. Daqui a pouco a gente usa ele. |

### cap03 · Filtrar até achar (vinheta: PEDIDOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); clique no período "Este mês" e escolha "Mês passado". | A bateria da Auto Peças é de vinte e um de outubro. Então, primeiro o período: Mês passado. |
| Clique em "Filtros": "Filtrar pedidos" ("Combine os campos para chegar ao pedido certo."); na busca ("Pedido, cliente, operador, placa..."), o robô digita "Vale Forte". | Em Filtros, a busca acha pelo nome do cliente ou fornecedor, pelo número do pedido, pelo operador ou pela placa. Digito Vale Forte. |
| [ZOOM: a única linha que sobra, 08/10, "Auto Peças Vale Forte", R$ 595,00] | No nome da Auto Peças só tem uma compra de chaparia. A bateria não está aqui. |
| O zoom solta; apaga a busca; em "Tipo" marca só "Compras"; em "Material" marca "Bateria automotiva"; em "Forma de Pagamento" marca "Com Pix/Transferência". Aparecem as etiquetas "Filtrando por", "Tipo: Compras", "Material: Bateria automotiva" e "Pagamento: Com Pix/Transferência". | Então eu procuro pelo que eu sei da compra. Tipo, Compras. Material, Bateria automotiva. E a forma de pagamento, Pix. |
| Clique na linha que sobra (21/10/2026, "Depósito Irmãos Siqueira", "Pix/Transferência", R$ 744,00): ela abre com "Bateria automotiva", 240, R$ 3,10. [ZOOM: a linha e o item] | Achou: vinte e um de outubro, duzentos e quarenta quilos de bateria, setecentos e quarenta e quatro reais. Só que no nome do Depósito Irmãos Siqueira. |
| O zoom solta; câmera nas etiquetas "Filtrando por" e em "Limpar todos". | O pedido saiu no fornecedor errado. Repara que cada filtro vira uma etiqueta aqui em cima, e o Limpar todos tira tudo de uma vez. |

### cap04 · Editar um pedido (vinheta: CORREÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`; o `setup` refaz o período e os filtros do cap03 fora do vídeo). No "⋮" da compra de 21/10, clique em "Editar": janela "Editar Pedido" ("O pedido será carregado para edição. Após salvar, o pedido original será substituído."). [ZOOM: "Se o pedido for de um caixa já fechado, o acerto do dinheiro é lançado no caixa de hoje e o pedido antigo fica marcado como estornado."; o zoom segue na linha de baixo] | Achado o pedido, vem a correção. Em Editar, a janela avisa: se o pedido é de um caixa já fechado, o acerto vai pro caixa de hoje, e o pedido antigo fica marcado como estornado. |
| (zoom continua) | Uma dica: pra pedido de caixa fechado, o caminho mais tranquilo é reabrir o caixa daquele dia, corrigir lá dentro e fechar de novo. Assim não nasce estorno nem lançamento no caixa de hoje. É o que a gente faz no fim do tutorial. |
| O zoom solta; clique em "Cancelar"; no período, "Hoje"; clique em "Limpar todos". | Então eu cancelo e começo pelo que é de hoje. Lembra da latinha da Aparecida? Ela trouxe quarenta e dois quilos, não vinte e quatro. |
| No "⋮" da compra de Aparecida Ramos (R$ 148,80), "Editar"; na janela, "Editar Pedido": abre a tela "Compra" com o selo "Editando Compra #N" e o botão "Cancelar Edição"; câmera no selo. | O caixa de hoje está aberto, então é só editar. A compra abre do jeito que foi lançada, com o selo de edição em cima. Dá pra mudar o fornecedor, os itens, o peso, o preço e a forma de pagamento. |
| Na lista de itens, "Ações do item" do "Alumínio latinha" → "Editar": aviso "Item carregado para edição"; o item volta para o formulário; em "Quantidade (Kg)" o robô troca 24 por 42. [ZOOM: "Quantidade (Kg)" com 42 e "Valor Total do Item" com R$ 260,40] | No item, Editar. Ele volta pro formulário, eu troco o peso pra quarenta e dois quilos, e o total vai pra duzentos e sessenta reais e quarenta. |
| O zoom solta; clique em "Incluir Item": o item volta para a lista com 42 kg. | Incluir Item, e o item volta pra lista com o peso certo. |
| [ILUSTRAÇÃO: não soma por cima: à esquerda, o pedido antigo "24 kg · R$ 148,80" é desfeito por inteiro: o estoque perde 24 kg e os R$ 148,80 voltam para a gaveta; nesta frase] | Agora, o que o sistema faz ao salvar. Ele não soma por cima. Primeiro desfaz o pedido antigo inteiro: tira os vinte e quatro quilos do estoque e devolve o dinheiro pro caixa. |
| (ilustração: à direita, o pedido novo "42 kg · R$ 260,40" é gravado: o estoque ganha 42 kg e R$ 260,40 saem da gaveta) | Depois grava o pedido certo como se fosse a primeira vez: quarenta e dois quilos no estoque, e duzentos e sessenta e quarenta saindo do caixa. |
| (ilustração: embaixo, o resultado "+18 kg" e "R$ 111,60 para a Aparecida"; a cena some) | No fim, o estoque ganha só os dezoito quilos que faltavam, e do caixa sai só a diferença que a Aparecida recebe. Nada duplica. |
| Volta à tela; clique em "Finalizar Compra": janela "Finalizar Pedido"; escolhe "Dinheiro" (R$ 260,40); clique em "CONFIRMAR PAGAMENTO": avisos "Revertendo pedido original...", "Pedido original revertido! Criando pedido editado..." e "Compra registrada!"; janela "Imprimir Comprovante" → "Não, obrigado". [BACKEND: `revert_consolidated_order_atomic` com a origem aberta (#87) e `create_purchase_atomic` no #87 com a data original; 42 kg, R$ 260,40, dinheiro] | Finalizar Compra, em dinheiro, Confirmar pagamento. Os avisos mostram as duas etapas: reverte o original e cria o editado. |
| Câmera no aviso "Compra registrada!". | Uma dica: não lance uma compra nova só com a diferença. Edite o pedido: o sistema desfaz o antigo e grava o certo, e o estoque fica correto. |

### cap05 · Excluir e o selo de estornado (vinheta: CORREÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`), `/pedidos` com "Hoje": as duas compras de Valdir Pereira, 07:41 e 07:42, de R$ 210,00. | E quando o pedido nem devia existir? A compra do Valdir saiu duas vezes, com um minuto de diferença. |
| No "⋮" da compra das 07:42, clique em "Excluir": janela "Excluir compra #N", "Valdir Pereira · R$ 210,00", "Vou desfazer tudo que este pedido criou:"; por um instante "Calculando o que será desfeito…"; depois "Estoque" ("− Ferro misto 280 kg") e "Financeiro" ("− Pagamento em dinheiro R$ 210,00 (apaga)"). [ZOOM: os blocos "Estoque" e "Financeiro"] | Em Excluir, antes de apagar, o sistema mostra tudo que vai desfazer: os duzentos e oitenta quilos de ferro misto saem do estoque, e os duzentos e dez reais voltam pro caixa. |
| O zoom solta; clique em "Excluir pedido": aviso "Pedido excluído" ("Pedido excluído e saldos revertidos."). [BACKEND: `preview_order_deletion` e `delete_purchase_atomic` em modo `hard_delete` (#87 aberto); linha em `destructive_actions_audit`] | Excluir pedido. Como o caixa de hoje está aberto, o pedido sai de vez. |
| No período, "Este mês"; a câmera desce até as duas compras de 03/11 da Aparecida Ramos (R$ 389,60), uma com o selo "Estornado em 05/11"; o cursor para no selo e aparece a dica "Estornado ... correção lançada no caixa de hoje". [ZOOM: o selo e a dica; o zoom segue na linha de baixo] | Agora repara nesta compra de três de novembro, da Aparecida. Ela também saiu duas vezes, e a cópia foi excluída no dia cinco, com o caixa do dia três já fechado. |
| (zoom continua) | Aí o sistema não mexe no caixa antigo. Ele lança a correção no caixa do dia em que excluiu, e deixa o pedido na lista, com o selo Estornado e a data. |
| O zoom solta. [ILUSTRAÇÃO: excluir × estornar: à esquerda, uma gaveta aberta ("hoje"): o pedido some dela; à direita, uma gaveta fechada com cadeado ("03/11"): o pedido fica nela com o selo "Estornado em 05/11", e uma seta leva a correção para a gaveta "05/11"; nesta frase; a cena some] | O pedido estornado não entra nos totais, e não dá mais pra editar nem excluir. Ele fica como o rastro de que existiu. |
| Clique em "Configurações" no rodapé do menu; na aba "Empresa", desce até "Histórico de Exclusões" e clica em "Ver histórico": a tela "Histórico de Exclusões" com a linha de hoje "Excluiu compra "Valdir Pereira"", com a hora e o e-mail do Rafael. [BACKEND: `entity_label` = nome do fornecedor] | E quem excluiu o quê, e quando, fica no Histórico de Exclusões. Só o administrador abre: em Configurações, Empresa, Ver histórico. |

### cap06 · Reimprimir e cupom sem valor (vinheta: COMPROVANTES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), `/pedidos` com "Hoje". No "⋮" da compra de Aparecida Ramos (R$ 260,40), clique em "Ver comprovante". [o robô faz o `window.open` da página devolver `null` neste clique, como se o navegador bloqueasse] Aparece o aviso "Popup bloqueado. Permita popups para gerar comprovantes."; câmera no aviso. | A Aparecida quer o comprovante novo, com os quarenta e dois quilos. No menu do pedido, Ver comprovante. Repara no aviso: Popup bloqueado. |
| [ILUSTRAÇÃO: liberar pop-ups: uma barra de endereço genérica (sem logo de navegador) com o endereço do sistema; o cursor clica no cadeado à esquerda do endereço; abre um painel com "Pop-ups" e a opção "Permitir", que é marcada; nesta frase e na próxima] | Todo PDF do sistema abre numa aba nova, e alguns navegadores bloqueiam isso na primeira vez. |
| (ilustração continua; a cena some no fim da fala) | Uma dica: pra liberar, clique no cadeado ao lado do endereço do site, procure Pop-ups e marque Permitir. É uma vez só. |
| Volta à tela; "Ver comprovante" de novo: abre a aba nova com o comprovante em PDF (Aparecida Ramos, Alumínio latinha, 42 kg, R$ 260,40). [ZOOM: a linha do item com 42 kg e R$ 260,40] | Pronto: o comprovante abre na aba nova, com o peso certo. Daqui você imprime ou manda pra ela. |
| O zoom solta; volta à aba do sistema; no "⋮" da compra de Valdir Pereira, clique em "Cupom sem valor": aviso "Cupom sem valor ativado" e o selo "Comprovante sem valores" na linha. [BACKEND: `set_order_hide_financials` com `p_value` true] | Agora o Valdir. Ele quer o comprovante pra mostrar o peso na obra de onde veio a sucata, sem mostrar quanto recebeu. No menu, Cupom sem valor. |
| [ZOOM: o selo "Comprovante sem valores"] | A linha ganha o selo Comprovante sem valores. |
| O zoom solta; "Ver comprovante" do Valdir: a aba nova mostra o comprovante só com o material e o peso (Ferro misto, 280 kg), sem valores. | E o comprovante sai só com o material e o peso. O pedido continua com o valor no sistema; só o papel sai sem. |
| Volta à aba do sistema; abre o "⋮" da compra do Valdir: a opção agora é "Mostrar valores no comprovante"; fecha o menu sem clicar. | Pra voltar ao normal, a mesma opção vira Mostrar valores no comprovante. |

### cap07 · O Histórico do Caixa (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`); menu "Financeiro" › "Histórico do Caixa": "Histórico do Caixa" ("Todos os registros de fechamento do caixa"), "Caixas Fechados", "N registro(s) • Exibindo 1-N de N". | E o caixa de vinte e um de outubro? Ele está no Histórico do Caixa, em Financeiro. Aqui fica cada caixa fechado, um por linha. |
| Câmera nas colunas "Código", "Abertura", "Fechamento", "Aberto por", "Saldo Inicial", "Saldo Final" e "Ações". | Cada linha tem o número do caixa, quando abriu e quando fechou, quem abriu, o saldo inicial e o final. |
| [ZOOM: o ícone de corrente entre os caixas #85 e #86 de 10/11 e a dica "Caixas fechados no mesmo dia"] | Essa correntinha junta os caixas fechados no mesmo dia, como o meu e o do Marcos, de ontem. |
| O zoom solta; clique na linha do #86: abre o resumo com "Total Compras", "Total Vendas", "Receitas", "Despesas" e "Lucro Projetado". | Clicando na linha, abre o resumo daquele caixa: compras, vendas, receitas, despesas e o lucro projetado. |
| Na busca ("Buscar por responsável, data ou código..."), o robô digita "21/10": ficam os caixas abertos em 21/10 (o #70, "Marcos Antunes", 21/10/2026 07:02 e 21/10/2026 17:31, R$ 800,00 e R$ 612,50, e o do Rafael daquele dia, se o histórico tiver). [ZOOM: a linha do #70] | A busca acha por nome, data ou número. Digito vinte e um barra dez, e aparecem os caixas daquele dia. O do Marcos é este aqui. |
| O zoom solta; câmera no botão "Filtros". | Em Filtros, dá pra escolher o operador e o período, quando a lista fica grande. |

### cap08 · Relatórios do caixa (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`; o `setup` deixa a busca "21/10" fora do vídeo). No "Ações" do #70, clique em "Ver comprovante": abre a aba nova com o relatório de fechamento do caixa #70 em PDF. | Nas ações do caixa, Ver comprovante abre o relatório de fechamento daquele dia, o mesmo que sai quando o caixa fecha. |
| [ZOOM: o resumo do relatório: a abertura, as entradas e saídas por forma de pagamento e o fechamento] | Ele traz com quanto abriu, o que entrou e saiu em cada forma de pagamento, e com quanto fechou. |
| O zoom solta; volta à aba do sistema; no "Ações" do #70, clique em "Relatório de estoque": abre a aba nova "Relatório de Estoque do Caixa #70"; câmera nas colunas "Material", "Qtd. Comprada", "Valor Comprado" e "Preço Médio Compra". | Já o Relatório de estoque mostra, material por material, o que esse caixa comprou e vendeu, com o preço médio. |
| [ZOOM: a linha "Bateria automotiva", 240, R$ 744,00, R$ 3,10] | Olha a bateria aqui: duzentos e quarenta quilos, setecentos e quarenta e quatro reais. É um bom jeito de conferir o dia de um operador. |
| O zoom solta; volta à aba do sistema. | Os dois relatórios abrem em aba nova, igual ao comprovante do pedido. |

### cap09 · Reabrir um caixa antigo (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), `/historico-caixa` com a busca "21/10"; abre o "Ações" do #70; câmera em "Reabrir caixa". | Agora a correção do jeito tranquilo. Nas ações do caixa de vinte e um de outubro, Reabrir caixa. |
| (câmera no item) | Pra reabrir, o dono do caixa não pode estar com outro caixa aberto. O Marcos não abriu caixa hoje, então a opção está liberada. Se estivesse, ela aparece apagada e explica que é preciso fechar o caixa atual dele primeiro. |
| Clique em "Reabrir caixa": janela "Reabrir Último Caixa?" ("O caixa será reaberto exatamente como estava antes do fechamento. Todas as transações registradas continuarão associadas a este caixa.", "Fechado em: 21/10/2026 17:31"); clique em "Reabrir Caixa": aviso "Caixa reaberto com sucesso!"; o app vai para o Caixa. [BACKEND: update `cash_register` #70 (`status` open, `closed_at` e `closing_balance` nulos, `reopened_at`)] | O sistema confirma que o caixa volta exatamente como estava. Reabrir Caixa, e ele já leva pra tela do Caixa. |
| Na tela Caixa, as abas "Início", "#70 \| Caixa - Marcos Antunes" e "#87 \| Caixa - Rafael Nogueira (você)"; clique na aba do #70; a câmera desce no "Histórico de Transações" até a compra de "Depósito Irmãos Siqueira", R$ 744,00. | Em cima aparece a aba do caixa do Marcos, de vinte e um de outubro, do lado do meu de hoje. Dentro dele está a compra da bateria. |
| No "⋮" da compra, "Editar"; na janela, "Editar Pedido": abre "Compra" com "Editando Compra #N"; em "Fornecedor", clique em "Depósito Irmãos Siqueira": janela "Selecionar Fornecedor"; o robô digita "Vale Forte" e escolhe "Auto Peças Vale Forte". [ZOOM: o campo "Fornecedor" com "Auto Peças Vale Forte" e o item "Bateria automotiva", 240 kg, R$ 744,00] [TESTAR: o preço do item continua R$ 3,10 depois da troca] | Editar. Como o caixa está aberto de novo, a edição é normal. No fornecedor, eu troco pra Auto Peças Vale Forte. O resto fica igual: duzentos e quarenta quilos, setecentos e quarenta e quatro reais. |
| O zoom solta; "Finalizar Compra" → "Finalizar Pedido": "Pix/Transferência" na "Conta Principal", R$ 744,00 → "CONFIRMAR PAGAMENTO": avisos "Revertendo pedido original...", "Pedido original revertido! Criando pedido editado..." e "Compra registrada!"; janela "Imprimir Comprovante" → "Visualizar PDF": a aba nova mostra o comprovante no nome da Auto Peças Vale Forte. [BACKEND: `revert_consolidated_order_atomic` com a origem aberta (#70) e `create_purchase_atomic` com `p_transaction_at` de 21/10 no #70] [TESTAR: o comprovante e a linha do histórico mostram 21/10/2026; se mostrarem outra data, a câmera não enquadra a data] | Finalizar, Pix na conta principal, Confirmar pagamento. E o comprovante já sai certo, no nome da Auto Peças. |
| Volta à aba do sistema; menu "Financeiro" › "Caixa"; aba "#70 \| Caixa - Marcos Antunes": no "Histórico de Transações", a compra agora com "Auto Peças Vale Forte". | Repara: a compra corrigida ficou no caixa daquele dia, o do Marcos. O meu caixa de hoje não mudou. |
| (câmera na aba "Todas" do histórico) | Uma dica: se a correção ainda não aparece na aba Todas do histórico, recarregue a página antes de achar que sumiu. |
| A câmera sobe; clique em "Fechar Caixa": janela "Fechar Caixa #70", "Caixa de Marcos Antunes · Aberto em 21/10/2026 07:02", "Valor de Fechamento" com "612,50" e "Valor esperado pelo sistema: R$ 612,50". | Agora é fechar de novo. O valor de fechamento já vem com os seiscentos e doze e cinquenta daquele dia, porque a correção não mexeu no dinheiro da gaveta. |
| Em "Data/hora do fechamento", clique na data, escolha 21 de outubro de 2026 no calendário e digite "17:31" em "Hora". [ZOOM: "Data/hora do fechamento" com 21/10/2026 e 17:31] | E como o caixa é de outro dia, eu ajusto a data e a hora do fechamento pro fim daquele dia: vinte e um de outubro, dezessete e trinta e um. |
| O zoom solta; clique em "Confirmar Fechamento": aviso "Caixa fechado com sucesso!"; "Imprimir Relatório" → "Não, obrigado". [BACKEND: update `cash_register` #70 com `closed_at` 21/10/2026 17:31 e `closing_balance` 612,50; `cash_transactions` `closing` com a mesma data] | Confirmar Fechamento. Pronto: reabriu, corrigiu lá dentro e fechou de novo, sem estorno e sem mexer no caixa de hoje. |
| A tela volta para a aba "Início"; câmera na aba "#87 \| Caixa - Rafael Nogueira (você)". | Uma dica: o mesmo vale pra qualquer lançamento com data de outro dia. Ele vai pro caixa daquele dia, não pro de hoje, e quando o caixa do dia é outro, o sistema pergunta em qual caixa lançar. |

### cap10 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem: as etiquetas "Filtrando por" e a linha de 21/10. | Recapitulando: na tela Pedidos, a gente achou a bateria de três semanas atrás pelos filtros de período, tipo, material e pagamento, mesmo no nome errado. |
| Montagem: a ilustração do "não soma por cima" e o selo "Editando Compra #N". | Corrigiu o peso da latinha da Aparecida editando o pedido, sem duplicar estoque nem caixa. |
| Montagem: a prévia "Vou desfazer tudo que este pedido criou:" e o selo "Estornado em 05/11". | Excluiu a compra duplicada do Valdir e entendeu o selo de estornado. |
| Montagem: o comprovante da Aparecida e o selo "Comprovante sem valores". | Reimprimiu o comprovante, liberou a aba nova no navegador e usou o cupom sem valor. |
| Montagem: o Histórico do Caixa e o "Relatório de Estoque do Caixa #70". | No Histórico do Caixa, abriu o resumo, o relatório de fechamento e o de estoque. |
| Montagem: "Reabrir Último Caixa?" e "Fechar Caixa #70". | E reabriu o caixa de vinte e um de outubro com segurança, corrigiu o fornecedor lá dentro e fechou de novo. |
| Cartão "Próximo: Estoque: saldo, histórico e posição". | No próximo tutorial, o estoque: quanto tem, de onde veio e quanto valia. Até lá! |
