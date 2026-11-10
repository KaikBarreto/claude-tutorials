# Roteiro T6 · Caixa: abrir, fechar e o cofre

Pronto para a voz e a gravação (sem etapa de aprovação). Coluna Fala = texto da narração na grafia da legenda; a grafia
de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos
entre aspas como no código 1.59.154 (`T06/inventario.md`). Rótulos com a classe `uppercase` aparecem em maiúsculas na
tela ("DINHEIRO EM CAIXA"). Desktop, logado como Rafael Nogueira (administrador); o cap08 tem um trecho logado como
Marcos Antunes. Cada capítulo parte de um navegador novo com a semente indicada (`plano.md`, "Gravação").

- **Título:** Caixa: abrir, fechar e o cofre
- **Antes:** Balança e impressora: o EcoTray (T5)
- **Próximo:** Comprar e vender sucata (T7)
- **Vinhetas (áreas):** CAIXA · ABERTURA · COFRE · MULTI-CAIXA · MOVIMENTAÇÕES · FECHAMENTO · RESUMO
- **FAKE_NOW:** 10/11/2026 08:30 nos capítulos 0 a 9; 10/11/2026 17:40 nos capítulos 10 a 12.
- **Duração estimada:** ~13 min de vídeo (1.854 palavras, ~11,9 min de fala a 2,6 palavras/s, mais 12 vinhetas e as
  ações; alvo da fonte ~14 min).
- Marcas: `[BACKEND: ...]` o que o backend falso precisa ter; `[ZOOM: ...]` zoom suave que dura a frase inteira;
  `[ILUSTRAÇÃO: ...]` cena desenhada no estilo da marca (`docs/09-aula-ilustrada.md`); `[OUTRO USUÁRIO: ...]` trecho
  gravado em outra sessão.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Caixa: abrir, fechar e o cofre". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira, sem enquadrar valores. [ILUSTRAÇÃO: o dinheiro do dia no pátio: no centro, a gaveta de um caixa; da esquerda entra dinheiro (venda), para a direita sai dinheiro (compra de sucata de um carroceiro); aparecem nessa ordem, na primeira frase] | Oi! Neste tutorial a gente vai cuidar do dinheiro do dia na Recicla Vale Metais. |
| (ilustração: as notas saindo da gaveta para a carroça viram muitas setas; no fim, um ponto de interrogação sobre a gaveta, junto de "onde foi parar a diferença") | No ferro-velho, quase toda compra de sucata é paga em dinheiro vivo. Se o caixa não bate no fim do dia, ninguém sabe onde foi parar a diferença. |
| (ilustração: ao lado da gaveta aparece um cofre fechado, na palavra "cofre"; a cena some) | Então a gente vai ver com quanto o caixa abre, o que entra e sai, com quanto ele fecha, e onde fica o dinheiro da empresa quando não tem caixa aberto. |
| Dashboard; clique em "Financeiro" no menu lateral (abre o submenu); clique em "Caixa". | Tudo isso fica no menu lateral, em Financeiro, Caixa. |
| Cartão discreto "Antes: Balança e impressora: o EcoTray". | Se você ainda não viu o tutorial Balança e impressora, o EcoTray, dá uma olhada antes. [pause] Vamos começar pela tela com o caixa fechado. |

### cap01 · O caixa fechado (vinheta: CAIXA)

| Tela | Fala |
| --- | --- |
| `/caixa`, aba "Início" (o Rafael não tem caixa aberto; ainda não há abas no topo): título "MEU CAIXA" e o botão "Abrir Caixa". Câmera no bloco. [BACKEND: semente `inicio`, nenhum `cash_register` aberto; último fechado do Rafael = #84] | Essa é a tela do caixa logo cedo, antes de abrir. Em Meu Caixa fica o botão Abrir Caixa. |
| [ZOOM: o cartão amarelo com "#84 · R$ 1.250,00", "Rafael Nogueira", "09/11 07:58 → 09/11 17:44", o link "reabrir outro caixa" e o botão "Reabrir #84"] | E esse cartão amarelo é o último caixa que eu fechei, o de ontem, com o valor e o horário. Ele serve pra reabrir, se precisar corrigir alguma coisa. No fim do tutorial a gente usa. |
| O zoom solta; a câmera desce até "PAINEL GERENCIAL": "Hoje", "0 caixas encontrados", "Nenhum caixa foi aberto neste dia." | Mais embaixo, o Painel Gerencial mostra os caixas abertos no dia. Por enquanto, nenhum. |
| A câmera volta ao topo da página. | Quem não tem acesso aos caixas da equipe toda vê, no lugar disso, um cartão grande escrito Caixa Fechado, com o mesmo botão. |
| O robô aperta Shift+C (atalho padrão "Compra"): a tela de compra começa a abrir, aparece o aviso "Abra o caixa antes de realizar compras" e o app volta sozinho para `/caixa`. Câmera no aviso. | Repara o que acontece se alguém tenta lançar uma compra agora: o sistema avisa Abra o caixa antes de realizar compras e volta pra cá. |
| Câmera no botão "Abrir Caixa". | Venda, despesa e receita também passam por um caixa aberto. Então, vamos abrir. |

### cap02 · Abrir o caixa (vinheta: ABERTURA)

| Tela | Fala |
| --- | --- |
| Clique em "Abrir Caixa": janela "Abrir Caixa" ("Informe o saldo inicial em dinheiro. Deixe em branco ou 0 se abrir sem dinheiro em espécie."), "Abrir para o usuário" com "Rafael Nogueira (Você)", "SALDO DE ABERTURA (R$)" vazio, as dicas embaixo, o aviso amarelo do zero e "DATA E HORA DE ABERTURA". | Clico em Abrir Caixa. A janela pede o saldo inicial em dinheiro: quanto dinheiro vivo tem na gaveta agora. |
| [ZOOM: o campo "Saldo de Abertura (R$)" vazio e, embaixo, "R$ 1.250,00 foi o valor restante em dinheiro do último caixa (#84)"; o mesmo zoom segue nas três linhas] | O campo vem vazio de propósito. Embaixo tem uma dica: mil duzentos e cinquenta reais foi o que sobrou no último caixa. |
| (zoom continua) | Uma dica: esse número é só uma referência. Conte o dinheiro da gaveta e digite o que contou. Copiar a dica sem contar é o motivo mais comum de diferença no fechamento. |
| (zoom continua) O robô digita "1.500,00" no campo; o aviso amarelo some. | Hoje cedo eu pus mais troco na gaveta e contei mil e quinhentos reais. É isso que eu digito. |
| O zoom solta; clique em "Abrir Caixa": aviso "Caixa aberto com sucesso!"; aparecem as abas "Início" e "#85 \| Caixa - Rafael Nogueira (você)" e o cartão "DINHEIRO EM CAIXA" com R$ 1.500,00 e "Aberto em: 10/11/2026 08:31". [BACKEND: `get_dinheiro_balance` com `disponivel` 18.500; insert em `cash_register` com `register_number` 85; `cash_transactions` `opening` "Abertura do Caixa #85"] | Abrir Caixa. Pronto: o caixa abriu com mil e quinhentos reais, e a tela já mostra o caixa aberto. |

### cap03 · Abrir com zero (vinheta: ABERTURA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`), aba "#85 \| Caixa - Rafael Nogueira (você)"; a câmera desce até "HISTÓRICO DE TRANSAÇÕES", aba "Todas". [ZOOM: a linha com o selo "Abertura", "Abertura do Caixa #85" e R$ 1.500,00] | Lá embaixo, no Histórico de Transações, o sistema lançou sozinho a linha Abertura do Caixa, com os mil e quinhentos. Isso acontece sempre que o caixa abre com dinheiro. |
| O zoom solta. [ILUSTRAÇÃO: dia só de Pix: um caminhão sai do pátio com fardos de sucata para um cliente; o pagamento faz uma seta direto para um prédio de banco, com "Pix ou transferência"; a gaveta do caixa fica vazia; aparecem nessa ordem, nesta frase] | Agora imagina um dia em que a Recicla Vale só entrega carga pros clientes, e eles pagam por Pix ou transferência. Nenhum dinheiro vivo passa pela gaveta. |
| (ilustração: a gaveta vazia ganha "R$ 0,00" e o selo "abre com zero") | Aí faz sentido abrir o caixa com zero. É só deixar o campo vazio ou digitar zero. |
| Volta à tela; clique na aba "Início": "ABRIR CAIXA PARA OUTRO USUÁRIO" e o botão "Abrir Caixa"; clique em "Abrir Caixa": a janela vem com "Juliana Prado" em "Abrir para o usuário"; o robô abre a lista e escolhe "Marcos Antunes". | Agora é a vez do caixa do Marcos, o balanceiro. No Início, o administrador também abre caixa pra outra pessoa: em Abrir para o usuário, eu escolho o Marcos. |
| [ZOOM: o aviso amarelo "O caixa será aberto sem dinheiro em espécie (R$ 0,00). Use isso se a operação é só Pix/cartão."] | Repara no aviso amarelo com o campo vazio: o caixa abriria sem dinheiro em espécie, e sem aquela linha de abertura no histórico. |
| O zoom solta; câmera no campo "Saldo de Abertura (R$)" vazio. | Mas o Marcos paga os fornecedores em dinheiro na balança. Então o caixa dele precisa de dinheiro, e quem diz quanto dá é o cofre. |

### cap04 · O cofre da empresa (vinheta: COFRE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); o `setup` abre fora do vídeo "Início" › "Abrir Caixa" e escolhe "Marcos Antunes". [ZOOM: "Disponível no cofre agora: R$ 17.000,00" e "(de R$ 18.500,00 total", "R$ 1.500,00 está dentro de caixas abertos)."] | Embaixo do campo, o sistema mostra o disponível no cofre: dezessete mil reais, de dezoito mil e quinhentos no total. Mil e quinhentos estão dentro de caixas abertos. |
| O zoom solta. [ILUSTRAÇÃO: cofre × caixa: um cofre grande com "R$ 18.500,00" e a legenda "todo o dinheiro vivo da empresa"; embaixo, pequeno, "Conta Dinheiro"; aparece nesta frase] | O cofre é todo o dinheiro vivo da empresa: dezoito mil e quinhentos reais. No sistema, ele também aparece como Conta Dinheiro. |
| (ilustração: um maço "R$ 1.500,00" sai do cofre para a gaveta "Caixa do Rafael"; o total "R$ 18.500,00" continua em cima, agora com "dentro de caixas: R$ 1.500,00") | Quando eu abri o meu caixa com mil e quinhentos, esse dinheiro foi pra minha gaveta. Ele continua sendo da empresa, só mudou de lugar. |
| (ilustração: destaca o que ficou no cofre, "disponível: R$ 17.000,00") | O que não está em nenhum caixa aberto é o disponível no cofre: dezessete mil. É desse dinheiro que sai um caixa novo. |
| (ilustração: setas "abre o caixa" do cofre para a gaveta e "fecha o caixa" da gaveta de volta para o cofre; a cena some) | Por isso o caixa só abre com o dinheiro que já está registrado no cofre. E quando ele fecha, o dinheiro contado volta pro cofre. Assim, todo real tem um lugar. |
| Volta à janela; câmera no campo "Saldo de Abertura (R$)". | E se alguém tentar abrir com mais do que tem? É o que a gente vê agora. |

### cap05 · Saldo insuficiente (vinheta: COFRE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`; o `setup` abre o diálogo para "Marcos Antunes"). O robô digita "20.000,00" em "Saldo de Abertura (R$)". [ZOOM: o campo com R$ 20.000,00] | Hoje o Marcos tem compra grande na balança e quer começar com vinte mil reais. Digito vinte mil no saldo de abertura. |
| O zoom solta; clique em "Abrir Caixa": abre a janela "⚠️ Saldo insuficiente em dinheiro". [BACKEND: `get_dinheiro_balance` com `disponivel` 17.000 e `reservado_total` 1.500; a tela bloqueia antes de gravar] | Clico em Abrir Caixa, e aparece o aviso: Saldo insuficiente em dinheiro. |
| [ZOOM: "O caixa só pode abrir com o dinheiro que já está registrado no cofre da empresa. Você tentou abrir com R$ 20.000,00, mas há apenas R$ 17.000,00 disponíveis (R$ 1.500,00 já reservados em caixas abertos)."] | O texto explica: o caixa só abre com o dinheiro registrado no cofre. A gente tentou vinte mil, e o disponível é dezessete mil, porque mil e quinhentos já estão no meu caixa. |
| O zoom solta; câmera nos botões "Usar disponível (R$ 17.000,00)" e "Ajustar saldo do dinheiro", sem clicar. | Tem duas saídas. Usar disponível preenche o campo com os dezessete mil do cofre. |
| Cursor sobre "Ajustar saldo do dinheiro", sem clicar. | E Ajustar saldo do dinheiro corrige o cofre quando tem dinheiro na empresa que nunca foi lançado, como uma sobra guardada. Depois do ajuste, o caixa abre sozinho com o valor que você tentou. |
| (câmera nos dois botões) | Uma dica: se você está com o dinheiro na mão e o aviso aparece, é sinal de dinheiro sem registro. Conte tudo o que a empresa tem em espécie e ajuste o cofre uma vez só. |
| Clique em "Usar disponível (R$ 17.000,00)": o aviso fecha e o campo fica com "17.000,00"; clique em "Abrir Caixa": aviso "Caixa aberto com sucesso!"; aparece a aba "#86 \| Caixa - Marcos Antunes", selecionada, com "DINHEIRO EM CAIXA" R$ 17.000,00. [BACKEND: insert `cash_register` #86 com `opened_by` Marcos e 17.000; `opening` "Abertura do Caixa #86"] | Aqui não é o caso: o Marcos começa com os dezessete mil, e o resto vem do banco mais tarde. Usar disponível, Abrir Caixa, e pronto: o caixa do Marcos está aberto. |

### cap06 · Os dois cartões (vinheta: CAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), aba "#85 \| Caixa - Rafael Nogueira (você)"; câmera no cartão "DINHEIRO EM CAIXA" com R$ 1.500,00. | Com o caixa aberto, a tela tem dois cartões no topo. O primeiro é o Dinheiro em Caixa: o dinheiro vivo deste caixa, os meus mil e quinhentos. |
| [ZOOM: "Aberto em: 10/11/2026 08:31" e "Dinheiro total da empresa: R$ 18.500,00"] | Embaixo, a hora em que ele abriu e o Dinheiro total da empresa, que é o cofre: dezoito mil e quinhentos. |
| O zoom solta; clique em "Dinheiro total da empresa:": abre "Movimentações Financeiras" na conta "DINHEIRO (COFRE)", com o cartão "O cofre da empresa", R$ 18.500,00 e "Saldo Total em Dinheiro". | Clicando nele, o sistema abre o cofre. |
| [ZOOM: a barra e a legenda "Disponível no cofre: R$ 0,00 (0%)", "Caixa de Rafael Nogueira: R$ 1.500,00 (8%)" e "Caixa de Marcos Antunes: R$ 17.000,00 (92%)"] | A barra mostra onde está cada real: mil e quinhentos no meu caixa, dezessete mil no caixa do Marcos, e nada sobrando no cofre. |
| O zoom solta; menu lateral "Financeiro" › "Caixa"; volta na aba #85; câmera no cartão "SALDO BANCÁRIO" com o valor, as duas contas e os botões "Saque / Sangria", "Nova Movimentação Bancária" e "Saldo de Cliente/Fornecedor". | De volta ao caixa, o segundo cartão é o Saldo Bancário: o dinheiro das contas do banco, onde caem o Pix e a transferência. Os botões dele a gente usa daqui a pouco. |
| Clique no olho do "Dinheiro em Caixa" ("Ocultar saldo"). [ZOOM: o valor vira "R$ ••••••"; o zoom segue na linha de baixo] | No olhinho, você esconde o valor da tela, e ele vira pontinhos. |
| (zoom continua) Clique no olho de novo ("Mostrar saldo"); o zoom solta no fim da fala. | Uma dica: se alguém da equipe vê esses pontinhos sem ter clicado no olho, não é erro. É a permissão Ver Dinheiro Total em Caixa, desligada pra essa pessoa em Usuários e Permissões. |

### cap07 · Cada um com o seu caixa (vinheta: MULTI-CAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), aba #85. [ZOOM: as abas "Início", "#85 \| Caixa - Rafael Nogueira (você)" e "#86 \| Caixa - Marcos Antunes"; o zoom segue na linha de baixo] | Repara nas abas lá em cima: uma pro meu caixa e outra pro do Marcos. Cada operador tem o seu. |
| (zoom continua) | Isso é o multi-caixa. Cada um abre, opera e fecha o próprio caixa. Se faltar dinheiro numa gaveta, você sabe de quem é. |
| O zoom solta; clique no "?" à direita das abas: janela "Como funcionam os Multi-Caixas?"; câmera em "O que acontece ao operar em outro caixa?" e no primeiro item. | No ponto de interrogação, o sistema explica as regras. A principal: compra, venda, despesa e receita em dinheiro mexem só no caixa selecionado. |
| Câmera nos dois itens seguintes ("Saldo bancário (PIX/transferências) é compartilhado..." e "Saldo de clientes/fornecedores também é compartilhado..."). | Já o saldo do banco e o saldo de clientes e fornecedores são da empresa toda. |
| Fecha a janela; clique na aba "Início": "ABRIR CAIXA PARA OUTRO USUÁRIO", "PAINEL GERENCIAL", "Hoje", "2 caixas encontrados" e "RESUMO DO DIA". | Na aba Início fica o Painel Gerencial, com o resumo do dia somando os caixas. Daqui também sai o Abrir Caixa pra outro usuário, como eu fiz com o Marcos. |
| Câmera em "2 caixas encontrados". | E se a empresa preferir um caixa só pra todo mundo, dá pra desligar em Configurações, Usabilidade, na opção Multi-Caixas. |

### cap08 · O caixa dos outros (vinheta: MULTI-CAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); clique na aba "#86 \| Caixa - Marcos Antunes": "DINHEIRO EM CAIXA" R$ 17.000,00 e "Aberto em: 10/11/2026 08:4x". | Pra ver o caixa do Marcos, é só clicar na aba dele. Aqui estão os dezessete mil da gaveta dele e a hora em que abriu. |
| Câmera nos botões "NOVA COMPRA", "NOVA VENDA", "NOVA DESPESA" e "NOVA RECEITA". | O que eu lançar com essa aba aberta vai pro caixa do Marcos, não pro meu. Então, antes de lançar no caixa de outra pessoa, confira a aba. |
| A câmera sobe para as abas. | Quem pode ver e operar o caixa dos outros? O administrador e quem tem a permissão Ver e Operar Todos os Caixas. |
| [OUTRO USUÁRIO: navegador logado como Marcos Antunes ("o computador da balança"), `/caixa`: o caixa #86 dele, sem as abas, com o selo "#86" ao lado do título "Caixa"; câmera no topo da página] | Já o Marcos, no computador da balança, vê só o caixa dele, sem as abas. |
| (mesma tela) | E todo caixa fechado, de todo operador, fica guardado no Histórico do Caixa, com o nome de quem abriu. |

### cap09 · Saque e sangria (vinheta: MOVIMENTAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), Rafael, aba #85. [ILUSTRAÇÃO: suprimento × sangria: um banco à esquerda, a gaveta "Caixa do Marcos" no meio e o cofre à direita; a gaveta mostra "R$ 17.000,00" e uma meta "R$ 20.000,00"; aparece nesta frase] | Lembra que o Marcos queria vinte mil e abriu com dezessete? Os três mil que faltam vêm do banco. |
| (ilustração: seta verde do banco para a gaveta, com "suprimento" e, embaixo, o nome no sistema: "Saque") | Pôr dinheiro na gaveta durante o dia é o que muita gente chama de suprimento. Quando ele vem do banco, aqui no sistema é um Saque. |
| (ilustração: seta azul da gaveta e do cofre para o banco, com "Sangria") | A sangria é o caminho contrário: o dinheiro sai de um caixa, ou do cofre, e vai pro banco. |
| (ilustração: as duas setas ganham o selo "não é receita nem despesa"; uma moeda pequena "tarifa" sai do banco com o selo "despesa"; a cena some) | Nos dois casos não é receita nem despesa: é o mesmo dinheiro da empresa mudando de lugar. Só a tarifa do banco é despesa de verdade. |
| Clique em "Saque / Sangria": janela "Saque / Sangria" com "Saque" marcado e "Transferir dinheiro do banco para o cofre ou para um caixa aberto". | Clico no botão do saque. A janela tem as duas opções, Saque e Sangria, e o Saque já vem marcado. |
| Em "Conta de origem" fica a conta principal; em "Destino do saque" o robô abre a lista e troca o caixa do Rafael por "Caixa de Marcos Antunes". | A conta de origem é a principal do banco. No destino, eu escolho o caixa do Marcos. |
| O robô digita "3.000,00" em "Valor do Saque". [ZOOM: "Valor do Saque" com R$ 3.000,00] | Valor do saque: três mil reais. |
| O zoom solta; em "Tem tarifa no saque?" escolhe "Sim"; aparece "Valor da Tarifa" e o robô digita "6,50". [ZOOM: "Valor da Tarifa" com R$ 6,50] | O banco cobrou tarifa? Aqui, sim: seis reais e cinquenta. |
| O zoom solta; câmera em "Efeitos desta transação:": "Saldo da Conta Bancária", "Diminuirá em R$ 3006,50" e "(Saque: R$ 3.000,00 + Tarifa: R$ 6,50)"; "Fundo de Caixa", "Aumentará em R$ 3.000,00". | Embaixo, os efeitos: a conta do banco diminui três mil e seis reais e cinquenta, e o caixa do Marcos aumenta três mil. |
| (câmera nos efeitos) | Uma dica: nunca lance um saque como Nova Receita. Ele entraria no relatório como se a empresa tivesse faturado mais. A tarifa o sistema já lança separada, como despesa. |
| Clique em "Confirmar Saque": aviso "Saque realizado com sucesso!". [BACKEND: `create_manual_bank_transaction` com a saída do banco (−3.000, `transfer`), a tarifa (−6,50, `expense`, "Tarifa de Saque para o Caixa #86") e o espelho do cofre (+3.000); `cash_transactions` `transfer` +3.000 no #86 ("↓ SAQUE · <conta> → Caixa #86"); `adjust_cash_register_balance`] | Confirmar Saque. Pronto: o caixa do Marcos chegou nos vinte mil. |
| Clique de novo em "Saque / Sangria" e em "Sangria": "Transferir dinheiro do cofre ou de um caixa aberto para uma conta bancária", "Origem da sangria", "Conta de destino" e "Valor da Sangria"; câmera nos campos, sem preencher. | Na opção Sangria, você escolhe a origem, que pode ser o cofre ou um caixa aberto, e a conta do banco que recebe. É o que se faz quando sobra dinheiro na gaveta e ele vai pro banco. |
| Clique em "Cancelar"; clique em "Nova Movimentação Bancária": janela "Nova Movimentação Financeira" com "Tipo" ("Entrada", "Saída", "Transferência"). | Já a Nova Movimentação Bancária é pra entrada ou saída direto no banco, que não vem de pedido. Por exemplo, a tarifa mensal da conta. |
| Clique em "Saída"; "Conta bancária" fica na principal; "Descrição": o robô digita "Tarifa mensal do pacote de serviços"; "Valor": "39,90"; "Categoria": abre a lista e escolhe "Tarifas bancárias". Câmera acompanha cada campo. | Saída, a descrição, trinta e nove e noventa, e a categoria Tarifas bancárias. |
| Clique em "Salvar": aviso "Movimentação registrada com sucesso!". [BACKEND: `create_manual_bank_transaction` (saída −39,90, categoria "Tarifas bancárias", `p_cash_register_id` do #85); categoria de despesa "Tarifas bancárias" na semente] | Salvar. Essa sim entra no resultado como despesa. |

### cap10 · Fechar o caixa (vinheta: FECHAMENTO)

| Tela | Fala |
| --- | --- |
| Corte para as 17:40 (semente `apos-cap09` + `dia-10`); aba #85 com "DINHEIRO EM CAIXA" R$ 1.007,10; a câmera desce no "Histórico de Transações": a venda para Aços Quiririm Ltda (Pix/Transferência), as compras de Aparecida Ramos e de Valdir Pereira (Dinheiro) e a tarifa mensal. | Fim do dia. No meu caixa entrou a venda pra Aços Quiririm, por transferência, e saíram duas compras em dinheiro: a latinha da Aparecida e o ferro misto do Valdir. |
| A câmera sobe para o botão "FECHAR CAIXA", sem cadeado. [BACKEND: `order_drafts` vazio para o #85] | Antes de liberar o Fechar Caixa, o sistema confere se ficou algum pedido não finalizado neste caixa. |
| (câmera no botão) | Se ficou, o botão aparece com um cadeado, e passando o mouse ele mostra qual pedido falta finalizar ou cancelar. Aqui está tudo finalizado. |
| Clique em "Fechar Caixa": janela "Fechar Caixa #85", "Caixa de Rafael Nogueira · Aberto em 10/11/2026 08:31"; por um instante, "Calculando saldo de fechamento..."; câmera nos cartões. | Clico em Fechar Caixa. A janela faz a conta do dia. |
| [ZOOM: "SALDO DE ABERTURA" R$ 1.500,00, "RESTANTE EM CAIXA" R$ 1.007,10 e, em "SAÍDAS", "COMPRAS" R$ 492,90 com "Dinheiro: R$ 492,90"; o zoom segue na linha de baixo] | Abriu com mil e quinhentos, e saíram quatrocentos e noventa e dois e noventa em compras, em dinheiro. A venda e a tarifa foram pelo banco, então não mexem na gaveta. |
| (zoom continua, centrado em "RESTANTE EM CAIXA") | Restante em caixa: mil e sete reais e dez centavos. É o que o sistema espera achar na gaveta. |
| O zoom solta. [ILUSTRAÇÃO: esperado × contado: à esquerda uma pilha de notas "esperado: R$ 1.007,10"; à direita, uma mão contando notas da gaveta, "contado"; aparecem nessa ordem, nesta frase] | Agora vem a conferência. De um lado, o que o sistema espera. Do outro, o que você conta na gaveta. |
| (ilustração: as duas pilhas ficam iguais e ganham um visto; depois uma segunda versão rápida com a pilha da direita menor e o rótulo "diferença"; a cena some) | Se os dois batem, o caixa fecha sem diferença. Se não batem, a diferença fica registrada, pra mais ou pra menos. |
| Volta à janela; câmera em "VALOR DE FECHAMENTO" já preenchido com "1.007,10", "Digite o valor físico em dinheiro que está no caixa" e "Valor esperado pelo sistema: R$ 1.007,10". | O Valor de Fechamento já vem com o esperado. Mesmo assim, conte a gaveta e digite o que contou. |
| O robô seleciona o campo e digita "1.007,10". [ZOOM: o campo e "Valor esperado pelo sistema: R$ 1.007,10"] | Contei mil e sete e dez. Bateu, então não aparece diferença. |
| O zoom solta; câmera na área do campo. | Se não batesse, a diferença apareceria em amarelo, com a chave Registrar diferença no DRE. Ela decide se a falta ou a sobra entra no resultado da empresa. O cofre fica sempre com o valor que você contou. |
| (câmera no campo) | Uma dica: o campo aceita valor negativo. É pro dia em que saiu mais dinheiro do que tinha, e alguém completou com dinheiro de fora. O sistema não impede: ele registra. |
| Clique em "Confirmar Fechamento": aviso "Caixa fechado com sucesso!" e a janela "Imprimir Relatório" ("Deseja imprimir o relatório de fechamento de caixa?", "Não, obrigado", "Ver comprovante"). [BACKEND: update `cash_register` (`status` closed, `closing_balance` 1.007,10, `closed_at`); `cash_transactions` `closing` 1.007,10; sem `adjustment` (diferença zero)] | Confirmar Fechamento. O dinheiro contado volta pro cofre, e o sistema oferece imprimir o relatório do fechamento. |
| Clique em "Não, obrigado"; a tela volta para a aba "Início". | Desta vez, não, obrigado. O relatório fica guardado no Histórico do Caixa, pra imprimir quando quiser. |

### cap11 · Reabrir um caixa (vinheta: FECHAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`), aba "Início": "MEU CAIXA", "Abrir Caixa" e o cartão amarelo "#85 · R$ 1.007,10", "Rafael Nogueira", "10/11 08:31 → 10/11 17:4x", "reabrir outro caixa" e "Reabrir #85". | Fechei e lembrei de uma compra que ficou sem lançar. O caminho é reabrir o caixa. |
| [ZOOM: o cartão amarelo] | Olha o cartão amarelo de novo: agora ele mostra o caixa que eu acabei de fechar, com o valor e o horário. |
| O zoom solta; clique em "reabrir outro caixa": janela "Reabrir outro caixa" ("Escolha qual caixa fechado deseja reabrir. Ele volta exatamente como estava antes do fechamento."), lista com #85 (Rafael Nogueira, R$ 1.007,10), #84 (Rafael Nogueira, R$ 1.250,00), #83 (Marcos Antunes, R$ 640,00) e os anteriores. | No link reabrir outro caixa aparecem os últimos caixas fechados, de todos os operadores, com o nome de quem abriu. |
| Câmera na linha do #83, do Marcos, sem clicar. | Dá pra reabrir o caixa de outra pessoa, desde que ela não esteja com outro caixa aberto. Cada operador fica com um caixa aberto por vez. |
| O #85 já vem marcado (é o primeiro); clique em "Reabrir #85": janela "Reabrir caixa #85?" com "O caixa será reaberto exatamente como estava antes do fechamento. Todas as transações registradas continuarão associadas a este caixa." e o quadro "#85 · R$ 1.007,10". | O meu já vem marcado. Clico em reabrir, e o sistema confirma: o caixa volta exatamente como estava, com tudo que foi lançado nele. |
| Clique em "Reabrir Caixa": aviso "Caixa reaberto com sucesso!"; volta a aba "#85 \| Caixa - Rafael Nogueira (você)" com "DINHEIRO EM CAIXA" R$ 1.007,10. [BACKEND: update `cash_register` (`status` open, `closed_at` e `closing_balance` nulos, `reopened_at`); delete das linhas de diferença do fechamento (nenhuma aqui)] | Reabrir Caixa. Pronto: o caixa está aberto de novo. Agora é só lançar o que faltou e fechar outra vez. |

### cap12 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem: o cartão amarelo e o aviso "Abra o caixa antes de realizar compras". | Recapitulando: a gente viu a tela com o caixa fechado, o cartão amarelo de reabrir, e que sem caixa aberto a compra não sai. |
| Montagem: o campo com R$ 1.500,00 e o aviso amarelo do zero. | Abriu o caixa com o dinheiro contado, sem copiar a dica, e viu quando faz sentido abrir com zero. |
| Montagem: a ilustração do cofre e a janela "⚠️ Saldo insuficiente em dinheiro". | Entendeu o cofre, que é todo o dinheiro vivo da empresa, e o aviso de saldo insuficiente, com as duas saídas. |
| Montagem: os dois cartões e as abas dos dois caixas. | Conheceu os dois cartões, abriu o caixa do Marcos e viu cada operador com a sua aba. |
| Montagem: "Efeitos desta transação:" do saque. | Fez um saque do banco pro caixa do Marcos, com a tarifa, conheceu a sangria e lançou a tarifa mensal direto no banco. |
| Montagem: "Valor esperado pelo sistema: R$ 1.007,10" e "Reabrir caixa #85?". | E fechou o caixa sem diferença, e reabriu pelo cartão amarelo. |
| Cartão "Próximo: Comprar e vender sucata". | No próximo tutorial, a parte que a Recicla Vale faz o dia inteiro: comprar e vender sucata. Até lá! |
