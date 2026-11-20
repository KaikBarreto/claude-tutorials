# Roteiro T9 · Pedidos e histórico do caixa

Pronto para a voz e a gravação (sem etapa de aprovação). Coluna Fala = texto da narração na grafia da legenda; a grafia
de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos
entre aspas como no código 1.60.18 (`T09/inventario.md`, `cobertura_160.md`). Desktop, logado como Rafael Nogueira (administrador). Cada
capítulo parte de um navegador novo com a semente indicada (`plano.md`, "Gravação"). PDFs abrem em aba nova: o robô grava
a aba e volta.

- **Título:** Pedidos e histórico do caixa
- **Antes:** Ticket de Pesagem (T8)
- **Próximo:** Estoque: saldo, histórico e posição (T10)
- **Vinhetas (áreas):** PEDIDOS · CORREÇÕES · COMPROVANTES · HISTÓRICO · RESUMO (o cap07 novo é COMPROVANTES)
- **FAKE_NOW:** 11/11/2026 08:30 (quarta) em todos os capítulos.
- **Duração estimada:** ~17 min de vídeo (2.252 palavras, ~14,4 min de fala a 2,6 palavras/s, mais 11 vinhetas, os
  PDFs em aba nova e as ações). Cresceu de 1.702 palavras por pedido do Kaik (cobrir cada função e caso de uso).
- **Renumeração (20/11):** capítulo novo 7 "Exportar a lista"; os antigos 7 a 10 viraram 8 a 11 (Histórico do Caixa, Relatórios,
  Reabrir, Recapitulando). Os nomes das sementes seguem os de antes (`apos-cap09` é o estado depois da reabertura).
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
| Capítulo novo (semente `inicio`), `/pedidos`; câmera no período "Este mês" e em "Todas as Ordens" ("N ordem(ns) • Exibindo 1-25 de N"). | A tela abre no mês atual, com todas as compras e vendas, de todos os caixas e de todos os operadores. Se um usuário só enxerga os próprios pedidos, é uma restrição ligada no cadastro dele, que a gente viu em Usuários e permissões. |
| [ZOOM: o cartão "Resumo do período filtrado" (vem fechado: o robô clica), com "Compras" e "Vendas" por forma de pagamento: "Dinheiro", "Pix/Transferência" e "Saldo"] | Em cima, o resumo do período: quanto saiu em compras e quanto entrou em vendas, separado em dinheiro, Pix e saldo. |
| O zoom solta; câmera nas colunas "Usuário", "Data", "Tipo", "N° Pedidos", "Cliente/Fornecedor", "Pagamento", "Valor" e "Ações". | Cada linha tem quem lançou, a data, se é compra ou venda, o número, o cliente ou fornecedor, como foi pago e o valor. |
| **(novo 1.60)** Passa o mouse em "Data" e "N° Pedidos"; clique em "Valor": a lista ordena do menor para o maior (o 1º clique numa coluna é crescente); a ordem por "Data" volta (dois cliques, crescente e decrescente). Câmera no rodapé: "Itens por página" e "Exibindo 1-N de N". | Clicando em Data, no número do pedido ou em Valor, a lista muda de ordem. E no rodapé você escolhe quantos pedidos aparecem por página. |
| **(novo 1.60)** A lista sobe até uma linha paga no Pix; o cursor para em "Pix/Transferência": a dica mostra a conta ("Conta Principal") com a bolinha de cor. [ZOOM: a dica; é do próprio app (Radix), aparece na gravação] | Na coluna Pagamento, passando o mouse num Pix, aparece em qual conta ele caiu. Num pagamento misto, aparece quanto foi em cada forma. |
| Clique na linha da compra de hoje de Aparecida Ramos (R$ 148,80): ela abre com "Material", "Peso", "V.Unit.", "Total" e "Formas de Pagamento" (Alumínio latinha, 24). | Clicando na linha, ela abre com os materiais, o peso, o preço e como foi pago. Aqui, a latinha da Aparecida, de hoje cedo: vinte e quatro quilos. Guarda esse número. |
| Câmera no "⋮" no fim da linha, sem abrir. | No fim de cada linha fica o menu do pedido. Daqui a pouco a gente usa ele. |

### cap03 · Filtrar até achar (vinheta: PEDIDOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); clique no período "Este mês" e escolha "Mês passado". | A bateria da Auto Peças é de vinte e um de outubro. Então, primeiro o período: Mês passado. |
| Clique em "Filtros": "Filtrar pedidos" ("Combine os campos para chegar ao pedido certo."); na busca ("Pedido, cliente, operador, placa..."), o robô digita "Vale Forte". | Em Filtros, a busca acha pelo nome do cliente ou fornecedor, pelo número do pedido, pelo operador ou pela placa. Digito Vale Forte. |
| [ZOOM: as três linhas que sobram, as compras de outubro da "Auto Peças Vale Forte" (08/10, R$ 595,00; 15/10; 29/10), nenhuma com bateria] | No nome da Auto Peças, nenhuma compra de bateria em outubro. A bateria não está aqui. |
| O zoom solta; apaga a busca; em "Tipo" marca só "Compras"; em "Material" marca "Bateria automotiva"; em "Forma de Pagamento" marca "Com Pix/Transferência". Aparecem as etiquetas "Filtrando por", "Tipo: Compras", "Material: Bateria automotiva" e "Pagamento: Com Pix/Transferência". | Então eu procuro pelo que eu sei da compra. Tipo, Compras. Material, Bateria automotiva. E a forma de pagamento, Pix. |
| Clique na linha que sobra (21/10/2026, "Depósito Irmãos Siqueira", "Pix/Transferência", R$ 744,00): ela abre com "Bateria automotiva", 240, R$ 3,10. [ZOOM: a linha e o item] | Achou: vinte e um de outubro, duzentos e quarenta quilos de bateria, setecentos e quarenta e quatro reais. Só que no nome do Depósito Irmãos Siqueira. |
| O zoom solta; câmera nas etiquetas "Filtrando por" e em "Limpar todos". | O pedido saiu no fornecedor errado. Repara que cada filtro vira uma etiqueta aqui em cima, e o Limpar todos tira tudo de uma vez. |
| **(novo 1.60)** Abre "Filtros" de novo; câmera em "Forma de Pagamento" (a lista aberta: "Com Saldo", "Pagamento Misto", "Não informado") e em "Conta"; fecha. Os filtros de tipo, material, pagamento e conta procuram no período inteiro (1.60.x). | Os outros filtros seguem a mesma ideia: pagos com saldo, pagamento misto, ou por uma conta bancária específica. |
| **(novo 1.60)** Câmera no período. (Aviso do app que o mundo não mostra, só dito: "Mostrando os N pedidos mais recentes do período..." e, no resumo, "O período escolhido tem mais de 1000 pedidos...".) | Uma dica: num período muito longo, com mais de mil pedidos, a tela mostra os mais recentes e avisa. Aí é só buscar pelo nome ou reduzir o período. |

### cap04 · Editar um pedido (vinheta: CORREÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`; o `setup` refaz o período e os filtros do cap03 fora do vídeo). No "⋮" da compra de 21/10, clique em "Editar": janela "Editar Pedido" ("O pedido será carregado para edição. Após salvar, o pedido original será substituído."). [ZOOM: "Se o caixa original estiver fechado, você poderá mantê-lo quando o pedido não movimentar dinheiro ou escolher um caixa aberto para receber o acerto."] | Achado o pedido, vem a correção. Em Editar, a janela avisa o que acontece quando o caixa do pedido já fechou: se não teve dinheiro no meio, dá pra manter o caixa original. Com dinheiro, você escolhe um caixa aberto pra receber o acerto. |
| Clique em "Editar Pedido": tela "Compra" com a faixa "Editando pedido … · Depósito Irmãos Siqueira · …" e o selo "Editando Compra #N". [ZOOM: "Caixa de destino da edição:" com o selo "Caixa #70 · Original" e a legenda "Sem movimento em dinheiro: você pode manter o caixa original sem alterar o fechamento."] | A bateria foi paga no Pix, e o caixa dela, o setenta, do Marcos, fechou em vinte e um de outubro. Como não teve dinheiro, o sistema já propõe manter o caixa original, sem mexer no fechamento daquele dia. |
| Clique no selo: janela "Em qual caixa registrar?" ("Escolha o caixa onde a operação será registrada.") com "Manter no caixa original #70" ("Sem movimento em dinheiro; o fechamento não será alterado.", etiqueta "Atual") e "Caixa #88 · Você"; o robô escolhe "Manter no caixa original #70". | Clicando no selo, aparecem as opções: manter no caixa original, ou lançar num caixa aberto, aqui o meu de hoje. Eu deixo no original. |
| Em "Fornecedor", clique em "Depósito Irmãos Siqueira": "Selecionar Fornecedor", digita "Vale Forte", escolhe "Auto Peças Vale Forte": janela **"Atualizar os preços?"** ("Com Auto Peças Vale Forte, o preço de 1 item é diferente."; "Bateria automotiva" R$ 3,10 → R$ 3,40/kg; "Total dos itens" R$ 744,00 → R$ 816,00). [ZOOM: o item, o total e os botões "Manter preços" e "Atualizar 1 preço"] Clique em "Manter preços". (No 1.60.10 a janela era "Trocar fornecedor?" com "Só nos próximos"; no 1.60.18 mudou.) [TESTAR: os valores 3,10, 3,40 e 744,00; 816,00 não é falado] | No fornecedor, eu troco pra Auto Peças Vale Forte. O sistema pergunta se atualiza os preços, porque ela tem um preço combinado na bateria. A compra já foi paga, então eu mantenho os preços, e o valor continua setecentos e quarenta e quatro reais. |
| "Finalizar" → "Finalizar Pedido": "Pix/Transferência" na "Conta Principal" → "CONFIRMAR PAGAMENTO" → "Imprimir Comprovante" → "Visualizar PDF": a aba nova mostra o comprovante no nome da Auto Peças Vale Forte, com 21/10/2026 (o robô devolve o PDF para a edição). [BACKEND: `revert_consolidated_order_atomic` com `p_compensation_register_id` = #70 (fechado, sem dinheiro) → `reverted_mode` `hard_delete`; `create_purchase_atomic` com `p_force_cash_register` no #70 e a data original] | Finalizar, Pix na conta principal, Confirmar pagamento. O comprovante já sai certo, no nome da Auto Peças, com a data de vinte e um de outubro. É esse que a gente manda pra ela. |
| Volta a "Pedidos" sem recarregar ("Mês passado"; busca "1665"): a linha de 21/10 com "Auto Peças Vale Forte", sem selo de estornado. Depois a busca "1663": no "⋮" da compra em dinheiro de 21/10 09:15 (R$ 187,50), "Editar" → "Editar Pedido": [ZOOM: "Caixa de destino da edição:" com "Caixa #88 · Você" e "O caixa original está fechado. Como houve movimento em dinheiro, escolha um caixa aberto."] | O pedido continua no caixa de vinte e um de outubro, e nada de estorno. Agora olha outra compra do mesmo dia, paga em dinheiro. Aqui o caixa original não é opção: o acerto precisa ir pra um caixa aberto, e o pedido antigo fica marcado como estornado. |
| Clique em "Cancelar Edição" (nada é gravado). | Uma dica: se a correção de um pedido em dinheiro precisa ficar no caixa daquele dia, reabra o caixa, corrija lá dentro e feche de novo. A gente faz isso no fim do tutorial. E tudo isso vale igual pra venda. |
| Volta a "Pedidos" sem recarregar; período "Hoje". | Então eu cancelo e começo pelo que é de hoje. Lembra da latinha da Aparecida? Ela trouxe quarenta e dois quilos, não vinte e quatro. |
| No "⋮" da compra de Aparecida Ramos (R$ 148,80), "Editar"; na janela, "Editar Pedido": abre a tela "Compra" com o selo "Editando Compra #N" e o botão "Cancelar Edição"; câmera no selo. | O caixa de hoje está aberto, então é só editar. A compra abre do jeito que foi lançada, com o selo de edição em cima. Dá pra mudar o fornecedor, os itens, o peso, o preço e a forma de pagamento. |
| Na lista de itens, "Ações do item" do "Alumínio latinha" → "Editar": aviso "Item carregado para edição"; o item volta para o formulário; em "Quantidade (Kg)" o robô troca 24 por 42. [ZOOM: "Quantidade (Kg)" com 42 e "Valor Total do Item" com R$ 260,40] | No item, Editar. Ele volta pro formulário, eu troco o peso pra quarenta e dois quilos, e o total vai pra duzentos e sessenta reais e quarenta. |
| O zoom solta; clique em "Incluir Item": o item volta para a lista com 42 kg. | Incluir Item, e o item volta pra lista com o peso certo. |
| [ILUSTRAÇÃO: não soma por cima: à esquerda, o pedido antigo "24 kg · R$ 148,80" é desfeito por inteiro: o estoque perde 24 kg e os R$ 148,80 voltam para a gaveta; nesta frase] | Agora, o que o sistema faz ao salvar. Ele não soma por cima. Primeiro desfaz o pedido antigo inteiro: tira os vinte e quatro quilos do estoque e devolve o dinheiro pro caixa. |
| (ilustração: à direita, o pedido novo "42 kg · R$ 260,40" é gravado: o estoque ganha 42 kg e R$ 260,40 saem da gaveta) | Depois grava o pedido certo como se fosse a primeira vez: quarenta e dois quilos no estoque, e duzentos e sessenta e quarenta saindo do caixa. |
| (ilustração: embaixo, o resultado "+18 kg" e "R$ 111,60 para a Aparecida"; a cena some) | No fim, o estoque ganha só os dezoito quilos que faltavam, e do caixa sai só a diferença que a Aparecida recebe. Nada duplica. |
| Volta à tela; clique em "Finalizar": janela "Finalizar Pedido"; escolhe "Dinheiro" (R$ 260,40); clique em "CONFIRMAR PAGAMENTO": avisos "Revertendo pedido original...", "Pedido original revertido! Criando pedido editado..." e "Compra registrada!"; janela "Imprimir Comprovante" → "Não, obrigado". [BACKEND: `revert_consolidated_order_atomic` com a origem aberta (#88) e `create_purchase_atomic` no #88 com a data original; 42 kg, R$ 260,40, dinheiro] | Finalizar, em dinheiro, Confirmar pagamento. Os avisos mostram as duas etapas: reverte o original e cria o editado. |
| Câmera no aviso "Compra registrada!". | Uma dica: não lance uma compra nova só com a diferença. Edite o pedido: o sistema desfaz o antigo e grava o certo, e o estoque fica correto. |

### cap05 · Excluir e o selo de estornado (vinheta: CORREÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`), `/pedidos` com "Hoje": as duas compras de Valdir Pereira, 07:41 e 07:42, de R$ 210,00. | E quando o pedido nem devia existir? A compra do Valdir saiu duas vezes, com um minuto de diferença. |
| No "⋮" da compra das 07:42, clique em "Excluir": janela "Excluir compra #N", "Valdir Pereira · R$ 210,00", "Vou desfazer tudo que este pedido criou:"; por um instante "Calculando o que será desfeito…"; depois "Estoque" ("− Ferro misto 280 kg") e "Financeiro" ("− Pagamento em dinheiro R$ 210,00 (apaga)"). [ZOOM: os blocos "Estoque" e "Financeiro"] | Em Excluir, antes de apagar, o sistema mostra tudo que vai desfazer: os duzentos e oitenta quilos de ferro misto saem do estoque, e os duzentos e dez reais voltam pro caixa. |
| O zoom solta; clique em "Excluir pedido": aviso "Pedido excluído" ("Pedido excluído e saldos revertidos."). [BACKEND: `preview_order_deletion` e `delete_purchase_atomic` em modo `hard_delete` (#88 aberto); linha em `destructive_actions_audit`, agora com IP e navegador] | Excluir pedido. Como o caixa de hoje está aberto, o pedido sai de vez. |
| No período, "Este mês"; a câmera desce até as duas compras de 03/11 da Aparecida Ramos (R$ 389,60), uma com o selo "Estornado em 05/11"; o cursor para no selo e aparece a dica "Estornado — correção lançada no caixa de hoje". [ZOOM: o selo e a dica; o zoom segue na linha de baixo] | Agora repara nesta compra de três de novembro, da Aparecida. Ela também saiu duas vezes, e a cópia foi excluída no dia cinco, com o caixa do dia três já fechado. |
| (zoom continua) | Aí o sistema não mexe no caixa antigo. Ele lança a correção no caixa do dia em que excluiu, e deixa o pedido na lista, com o selo Estornado e a data. |
| O zoom solta. [ILUSTRAÇÃO: excluir × estornar: à esquerda, uma gaveta aberta ("hoje"): o pedido some dela; à direita, uma gaveta fechada com cadeado ("03/11"): o pedido fica nela com o selo "Estornado em 05/11", e uma seta leva a correção para a gaveta "05/11"; nesta frase; a cena some] | O pedido estornado não entra nos totais, e não dá mais pra editar nem excluir. Ele fica como o rastro de que existiu. |
| **(novo 1.60)** No "⋮" da outra compra de 03/11 (08:47, R$ 389,60, dinheiro, no caixa já fechado), "Excluir": na prévia, "Financeiro" com "R$ 389,60 ↩ estorno hoje" no lugar de "(apaga)" e o aviso amarelo (texto do banco: "Parte do pedido saiu de um caixa já fechado → ..."). [ZOOM: "↩ estorno hoje"] Clique em "Cancelar": nada é excluído. | Dá pra ver isso antes de confirmar. Na outra compra desse dia, paga em dinheiro, a prévia mostra estorno hoje no lugar de apaga. Eu só quis mostrar, então cancelo. |
| **(novo 1.60)** Câmera na lista. (As travas do app, só ditas: "Abra o caixa de hoje" e "Este lançamento está conciliado. Desfaça a conciliação antes de excluir.") | Uma dica: pra excluir pedido de caixa fechado, você precisa estar com um caixa aberto. E pedido já conciliado no banco só sai depois de desfazer a conciliação. |
| Clique em "Configurações" no rodapé do menu; na aba "Empresa", desce até "Histórico de Exclusões" e clica em "Ver histórico": a tela "Histórico de Exclusões" com a linha de hoje "Excluiu compra "Valdir Pereira"", com a hora e o e-mail do Rafael. [BACKEND: `entity_label` = nome do fornecedor] | E quem excluiu o quê, e quando, fica no Histórico de Exclusões. Só o administrador abre: em Configurações, Empresa, Ver histórico. |
| **(novo 1.60)** Câmera nos filtros "Período", "Todos os tipos", "Todos os usuários" e na busca "Buscar pelo nome do registro..."; clique na linha "Excluiu compra "Valdir Pereira"": abre "Quem" (e-mail e função), "Onde" ("Chrome (Desktop)", "IP: 203.0.113.24") e os dados do pedido ("Número", "Total"). [ZOOM: o painel] | Aqui dá pra filtrar por período, tipo e usuário. E clicando na linha, aparece quem excluiu, de onde, e os dados do pedido que saiu. |

### cap06 · Reimprimir e cupom sem valor (vinheta: COMPROVANTES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), `/pedidos` com "Hoje". No "⋮" da compra de Aparecida Ramos (R$ 260,40), clique em "Ver comprovante". [o robô faz o `window.open` da página devolver `null` neste clique, como se o navegador bloqueasse] Aparece o aviso "Popup bloqueado. Permita popups para gerar comprovantes."; câmera no aviso. | A Aparecida quer o comprovante novo, com os quarenta e dois quilos. No menu do pedido, Ver comprovante. Repara no aviso: popup bloqueado. |
| [ILUSTRAÇÃO: liberar pop-ups: uma barra de endereço genérica (sem logo de navegador) com o endereço do sistema; o cursor clica no cadeado à esquerda do endereço; abre um painel com "Pop-ups" e a opção "Permitir", que é marcada; nesta frase e na próxima] | Todo PDF do sistema abre numa aba nova, e alguns navegadores bloqueiam isso na primeira vez. |
| (ilustração continua; a cena some no fim da fala) | Uma dica: pra liberar, clique no cadeado ao lado do endereço do site, procure pop-ups e marque Permitir. É uma vez só. |
| Volta à tela; "Ver comprovante" de novo: abre a aba nova com o comprovante em PDF (Aparecida Ramos, Alumínio latinha, 42 kg, R$ 260,40). [ZOOM: a linha do item com 42 kg e R$ 260,40] [o robô devolve o PDF; a edição mostra a aba] | Pronto: o comprovante abre na aba nova, com o peso certo. Daqui você imprime ou manda pra ela. |
| O zoom solta; volta à aba do sistema; no "⋮" da compra de Valdir Pereira, clique em "Cupom sem valor": aviso "Cupom sem valor ativado" e o selo "Comprovante sem valores" na linha. [BACKEND: `set_order_hide_financials` com `p_value` true] | Agora o Valdir. Ele quer o comprovante pra mostrar o peso na obra de onde veio a sucata, sem mostrar quanto recebeu. No menu, Cupom sem valor. |
| [ZOOM: o selo "Comprovante sem valores"] | A linha ganha o selo Comprovante sem valores. |
| O zoom solta; "Ver comprovante" do Valdir: a aba nova mostra o comprovante só com o material e o peso (Ferro misto, 280 kg), sem valores. [o robô devolve o PDF] | E o comprovante sai só com o material e o peso. O pedido continua com o valor no sistema; só o papel sai sem. |
| Volta à aba do sistema; abre o "⋮" da compra do Valdir: a opção agora é "Mostrar valores no comprovante"; fecha o menu sem clicar. | Pra voltar ao normal, a mesma opção vira Mostrar valores no comprovante. |
| **(novo 1.60)** Abre o "⋮" da compra da Aparecida; câmera em "Ver fotos anexadas" e "Enviar pelo WhatsApp" (sem clicar; sem o módulo de portal, o app abre uma janela de aviso); fecha. ("Imprimir direto" só existe com o EcoTray: fora desta aula.) | O menu ainda tem as fotos anexadas e o envio pelo WhatsApp, que manda o pedido com o link do portal. |

### cap07 · Exportar a lista (vinheta: COMPROVANTES)

| Tela | Fala |
| --- | --- |
| **Capítulo novo (1.60.18; semente `apos-cap06`)**, `/pedidos` com "Mês passado"; clique em "Exportar": menu "Exportar pedidos" com "PDF" e "Excel"; passa o mouse nos dois e clica em "PDF". | Além do comprovante de um pedido, dá pra tirar a lista inteira. Em Exportar, você escolhe PDF ou Excel. |
| Janela "Exportar PDF" ("Escolha quais pedidos serão incluídos no relatório"): "Período" já em "Mês passado"; desmarca "Vendas" em "Tipo de Pedido"; "Forma de Pagamento" com "Dinheiro", "PIX / Transferência" e "Saldo" marcados. | A janela já vem com o período da tela. Eu deixo só as compras de outubro, em todas as formas de pagamento. |
| [ZOOM: "Detalhamento" · "Detalhar materiais de cada pedido"] marca a caixa. | No PDF, dá pra detalhar: embaixo de cada pedido saem os materiais, com peso, preço e total. |
| Clique em "Exportar PDF" ("Gerando..."): abre a aba nova "Relatório de Pedidos" (HTML); aviso "Relatório de pedidos gerado". [o robô devolve o HTML; a edição mostra o cabeçalho com o período e as linhas com os materiais] (Limite de 1.000 pedidos por relatório; Excel gera "Excel gerado": só ditos.) | Exportar, e o relatório abre numa aba nova, pronto pra imprimir ou mandar pro contador. No Excel, sai a planilha da lista. |

### cap08 · O Histórico do Caixa (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`); menu "Financeiro" › "Histórico do Caixa": "Histórico do Caixa" ("Todos os registros de fechamento do caixa"), "Caixas Fechados", "N registro(s) • Exibindo 1-N de N". | E o caixa de vinte e um de outubro? Ele está no Histórico do Caixa, em Financeiro. Aqui fica cada caixa fechado, um por linha. |
| Câmera nas colunas "Código", "Abertura", "Fechamento", "Aberto por", "Saldo Inicial", "Saldo Final" e "Ações". | Cada linha tem o número do caixa, quando abriu e quando fechou, quem abriu, o saldo inicial e o final. |
| [ZOOM: o ícone de corrente entre os caixas #85 e #86 de 10/11 e a dica "Caixas fechados no mesmo dia"] | Essa correntinha junta os caixas fechados no mesmo dia, como o meu e o do Marcos, de ontem. |
| O zoom solta; clique na linha do #85: abre o resumo com "Total Compras", "Total Vendas", "Receitas", "Despesas" e "Lucro Projetado". | Clicando na linha, abre o resumo daquele caixa: compras, vendas, receitas, despesas e o lucro projetado. |
| Na busca ("Buscar por responsável, data ou código..."), o robô digita "21/10": ficam os caixas abertos em 21/10 (o #70, "Marcos Antunes", 21/10/2026 07:02 e 21/10/2026 17:31, R$ 800,00 e R$ 612,50). [ZOOM: a linha do #70] | A busca acha por nome, data ou número. Digito vinte e um barra dez, e aparecem os caixas daquele dia. O do Marcos é este aqui. |
| **(mudou)** Apaga a busca; clique em "Filtros": painel "Filtros do Histórico"; em "Aberto por" escolhe "Marcos Antunes"; em "Período" "Mês passado"; "Aplicar": só os caixas do Marcos de outubro; depois "Filtros" → "Limpar filtros". | Em Filtros, eu escolho quem abriu o caixa e o período. Aplicar, e ficam só os caixas do Marcos em outubro. Limpar filtros volta tudo. |

### cap09 · Relatórios do caixa (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`; o `setup` deixa a busca "21/10" fora do vídeo). No "Ações" do #70, clique em "Ver comprovante": abre a aba nova com o relatório de fechamento do caixa #70 em PDF. | Nas ações do caixa, Ver comprovante abre o relatório de fechamento daquele dia, o mesmo que sai quando o caixa fecha. |
| [ZOOM: o resumo do relatório: a abertura, as entradas e saídas por forma de pagamento e o fechamento] | Ele traz com quanto abriu, o que entrou e saiu em cada forma de pagamento, e com quanto fechou. |
| O zoom solta; volta à aba do sistema; no "Ações" do #70, clique em "Relatório de estoque": abre a aba nova "Relatório de Estoque do Caixa #70"; câmera nas colunas "Material", "Qtd. Comprada", "Valor Comprado" e "Preço Médio Compra". | Já o Relatório de estoque mostra, material por material, o que esse caixa comprou e vendeu, com o preço médio. |
| [ZOOM: a linha "Bateria automotiva", 240, R$ 744,00, R$ 3,10] | Olha a bateria aqui: duzentos e quarenta quilos, setecentos e quarenta e quatro reais. É um bom jeito de conferir o dia de um operador. |
| O zoom solta; volta à aba do sistema. ("Imprimir direto" nas ações do caixa fechado só existe com o EcoTray: fora desta aula.) | Os dois relatórios abrem em aba nova, igual ao comprovante do pedido. |

### cap10 · Reabrir um caixa antigo (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), `/historico-caixa` com a busca "21/10"; abre o "Ações" do #70; câmera em "Reabrir caixa". | Agora aquela compra em dinheiro de vinte e um de outubro. Ela saiu sem fornecedor, e eu quero corrigir sem tirar ela do caixa daquele dia. Então, nas ações do caixa, Reabrir caixa. |
| (câmera no item) | Pra reabrir, o dono do caixa não pode estar com outro caixa aberto. O Marcos não abriu caixa hoje, então a opção está liberada. Se estivesse, ela aparece apagada e explica que é preciso fechar o caixa atual dele primeiro. |
| Clique em "Reabrir caixa": janela **"Reabrir caixa #70?"** ("O caixa será reaberto exatamente como estava antes do fechamento. Todas as transações registradas continuarão associadas a este caixa.", "#70", "Marcos Antunes", "21/10 07:02 → 21/10 17:31"); clique em "Reabrir Caixa": aviso "Caixa reaberto com sucesso!"; o app vai para o Caixa. [BACKEND: update `cash_register` #70 (`status` open, `closed_at` e `closing_balance` nulos, `reopened_at`)] | O sistema confirma que o caixa volta exatamente como estava. Reabrir Caixa, e ele já leva pra tela do Caixa. |
| Na tela Caixa, as abas "Início", "#70 \| Caixa - Marcos Antunes" e "#88 \| Caixa - Rafael Nogueira (você)"; clique na aba do #70; a câmera desce no "Histórico de Transações" até a compra de R$ 187,50 (dinheiro, sem fornecedor). | Em cima aparece a aba do caixa do Marcos, de vinte e um de outubro, do lado do meu de hoje. Dentro dele está a compra em dinheiro, sem fornecedor. |
| No "⋮" da compra, "Editar"; na janela, "Editar Pedido": abre "Compra" com "Editando Compra #N" **sem** "Caixa de destino da edição:" (o caixa está aberto); em "Fornecedor", clique em "Não informado": "Selecionar Fornecedor"; o robô digita "Aparecida" e escolhe "Aparecida Ramos". [ZOOM: "Fornecedor" e os dois itens (Alumínio latinha 18 kg, Papelão 138 kg), R$ 187,50] [TESTAR: se aparecer "Atualizar os preços?", o robô clica "Manter preços"; se aparecer, a fala ganha uma frase] | Editar. Com o caixa aberto de novo, a edição é normal, sem escolher caixa de destino. No fornecedor, eu escolho a Aparecida, e o valor fica igual: cento e oitenta e sete reais e cinquenta. |
| O zoom solta; "Finalizar" → "Finalizar Pedido": "Dinheiro" (R$ 187,50) → "CONFIRMAR PAGAMENTO" → "Imprimir Comprovante" → "Não, obrigado". [BACKEND: `revert_consolidated_order_atomic` com a origem aberta (#70) e `create_purchase_atomic` no #70 com `p_transaction_at` de 21/10] | Finalizar, em dinheiro, Confirmar pagamento. |
| Volta à aba do sistema ("Voltar para o caixa"); aba "#70 \| Caixa - Marcos Antunes": no "Histórico de Transações", a compra de R$ 187,50 agora com "Aparecida Ramos". | Repara: a compra corrigida ficou no caixa daquele dia, o do Marcos. O meu caixa de hoje não mudou. |
| (câmera na aba "Todas" do histórico) | Uma dica: se a correção ainda não aparece na aba Todas do histórico, recarregue a página antes de achar que sumiu. |
| A câmera sobe; clique em "Fechar Caixa": janela "Fechar Caixa #70", "Caixa de Marcos Antunes · Aberto em 21/10/2026 07:02", "Valor de Fechamento" com "612,50" e "Valor esperado pelo sistema: R$ 612,50". | Agora é fechar de novo. O valor de fechamento já vem com os seiscentos e doze e cinquenta daquele dia, porque a correção não mexeu no dinheiro da gaveta. |
| Em "Data/hora do fechamento", clique na data, escolha 21 de outubro de 2026 no calendário e digite "17:31" em "Hora". [ZOOM: "Data/hora do fechamento" com 21/10/2026 e 17:31] | E como o caixa é de outro dia, eu ajusto a data e a hora do fechamento pro fim daquele dia: vinte e um de outubro, dezessete e trinta e um. |
| O zoom solta; clique em "Confirmar Fechamento": aviso "Caixa fechado com sucesso!"; "Imprimir Relatório" → "Não, obrigado". [BACKEND: update `cash_register` #70 com `closed_at` 21/10/2026 17:31 e `closing_balance` 612,50; `cash_transactions` `closing` com a mesma data] | Confirmar Fechamento. Pronto: reabriu, corrigiu lá dentro e fechou de novo, sem estorno e sem mexer no caixa de hoje. |
| A tela volta para a aba "Início"; câmera na aba "#88 \| Caixa - Rafael Nogueira (você)". | Uma dica: o mesmo vale pra qualquer lançamento com data de outro dia. Ele vai pro caixa daquele dia, não pro de hoje, e quando o caixa do dia é outro, o sistema pergunta em qual caixa lançar. |

### cap11 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem: as etiquetas "Filtrando por" e a linha de 21/10 (e a ordenação da lista). | Recapitulando: na tela Pedidos, a gente achou a bateria de três semanas atrás pelos filtros de período, tipo, material e pagamento, mesmo no nome errado, e viu como ordenar a lista. |
| Montagem: "Caixa de destino da edição: Caixa #70 · Original", a ilustração do "não soma por cima" e o selo "Editando Compra #N". | Corrigiu o fornecedor da bateria direto na edição, mantendo o caixa original, e o peso da latinha da Aparecida, sem duplicar estoque nem caixa. |
| Montagem: a prévia "↩ estorno hoje" e o selo "Estornado em 05/11". | Excluiu a compra duplicada do Valdir, viu na prévia o que muda num caixa fechado e entendeu o selo de estornado. |
| Montagem: o comprovante da Aparecida e o selo "Comprovante sem valores". | Reimprimiu o comprovante, liberou a aba nova no navegador e usou o cupom sem valor. |
| Montagem: "Exportar PDF" e o "Relatório de Pedidos". | Tirou a lista de pedidos em PDF, com os materiais de cada pedido. |
| Montagem: "Filtros do Histórico", o Histórico do Caixa e o "Relatório de Estoque do Caixa #70". | No Histórico do Caixa, filtrou por operador e período, abriu o resumo, o relatório de fechamento e o de estoque. |
| Montagem: "Reabrir caixa #70?" e "Fechar Caixa #70". | E reabriu o caixa de vinte e um de outubro pra corrigir uma compra em dinheiro lá dentro, e fechou de novo. |
| Cartão "Próximo: Estoque: saldo, histórico e posição". | No próximo tutorial, o estoque: quanto tem, de onde veio e quanto valia. Até lá! |
