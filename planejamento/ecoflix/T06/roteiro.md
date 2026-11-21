# Roteiro T6 · Caixa: abrir, fechar e o cofre

Aplicado ao app 1.60.18 em 20/11/2026 (cobertura 1.60.10 + handoff do cofre zerado), pronto para a voz e a gravação. Coluna Fala = texto da narração na grafia da legenda; a grafia
de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos
entre aspas como no código do app 1.60.18 (`T06/inventario.md`). Rótulos com a classe `uppercase` aparecem em maiúsculas na
tela ("DINHEIRO EM CAIXA"). Tela de gravação 1600x900. Desktop, logado como Rafael Nogueira (administrador); o cap09 tem um trecho logado como
Marcos Antunes (cap09b). Cada capítulo parte de um navegador novo com a semente indicada (`plano.md`, "Gravação").

- **Título:** Caixa: abrir, fechar e o cofre
- **Antes:** Balança e impressora: o EcoTray (T5)
- **Próximo:** Comprar e vender sucata (T7)
- **Vinhetas (áreas):** CAIXA · ABERTURA · COFRE · MULTI-CAIXA · MOVIMENTAÇÕES · FECHAMENTO · RESUMO
- **FAKE_NOW:** 10/11/2026 08:30 nos capítulos 0 e 1; 08:30:55 no 2; 08:41:50 nos 3 a 5; 08:43:30 no 6; 08:45 nos 7 a 10; 08:55 no 11; 17:30 no 12; 17:40 no 13; 17:42:40 no 14; 17:44 no 15.
- **Duração estimada:** ~23 min de vídeo (3.253 palavras, ~20,9 min de fala a 2,6 palavras/s, mais as vinhetas e as ações; antes: 2.044 palavras, ~14,5 min).
- Marcas: `[BACKEND: ...]` o que o backend falso precisa ter; `[ZOOM: ...]` zoom suave que dura a frase inteira;
  `[ILUSTRAÇÃO: ...]` cena desenhada no estilo da marca (`docs/09-aula-ilustrada.md`); `[OUTRO USUÁRIO: ...]` trecho
  gravado em outra sessão; `[TESTAR: ...]` o robô confere no ensaio.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Caixa: abrir, fechar e o cofre". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira, sem enquadrar valores. [ILUSTRAÇÃO: o dinheiro do dia no pátio: no centro, a gaveta de um caixa; da esquerda entra dinheiro (venda), para a direita sai dinheiro (compra de sucata de um carroceiro); aparecem nessa ordem, na primeira frase] | Oi! Neste tutorial a gente vai cuidar do dinheiro do dia na Recicla Vale Metais. |
| (ilustração: as notas saindo da gaveta para a carroça viram muitas setas; no fim, um ponto de interrogação sobre a gaveta, junto de "onde foi parar a diferença") | No ferro-velho, quase toda compra de sucata é paga em dinheiro vivo. Se o caixa não bate no fim do dia, ninguém sabe onde foi parar a diferença. |
| (ilustração: ao lado da gaveta aparece um cofre fechado, na palavra "cofre"; a cena some) | Então a gente vai ver com quanto o caixa abre, com quanto ele fecha, e onde fica o dinheiro da empresa quando não tem caixa aberto. |
| Dashboard; clique em "Financeiro" no menu lateral (abre o submenu); clique em "Caixa". | Tudo isso fica no menu lateral, em Financeiro, Caixa. |
| Cartão discreto "Antes: Balança e impressora: o EcoTray". | Se você ainda não viu o tutorial Balança e impressora, o EcoTray, dá uma olhada antes. [pause] Vamos começar pela tela com o caixa fechado. |

### cap01 · O caixa fechado (vinheta: CAIXA)

| Tela | Fala |
| --- | --- |
| `/caixa`, aba "Início" (o Rafael não tem caixa aberto; ainda não há abas no topo): título "MEU CAIXA" e o botão "Abrir Caixa". Câmera no bloco. [BACKEND: semente `inicio`, nenhum `cash_register` aberto; último fechado do Rafael = #84] | Essa é a tela do caixa logo cedo, antes de abrir. Em Meu Caixa fica o botão Abrir Caixa. |
| [ZOOM: o cartão amarelo com "#84 · R$ 1.250,00", "Rafael Nogueira", "09/11 07:58 → 09/11 17:44", o link "reabrir outro caixa" e o botão "Reabrir #84"] | E esse cartão amarelo é o último caixa que eu fechei, o de ontem, com o valor e o horário. Ele serve pra reabrir, se precisar corrigir alguma coisa. |
| O zoom solta; a câmera desce até "PAINEL GERENCIAL": "Hoje", "0 caixas encontrados", "Nenhum caixa foi aberto neste dia." | Mais embaixo, o Painel Gerencial mostra os caixas abertos no dia. Por enquanto, nenhum. |
| A câmera volta ao topo da página. | Quem não tem acesso aos caixas da equipe toda vê, no lugar disso, um cartão grande escrito Caixa Fechado, com o mesmo botão. |
| O robô aperta Shift+C (atalho padrão "Compra"): a tela de compra começa a abrir, aparece o aviso "Abra o caixa antes de realizar compras" e o app volta sozinho para `/caixa`. Câmera no aviso. [TESTAR: se o atalho não responder nessa tela, o robô abre `/compra` direto pelo endereço; o aviso e a volta são os mesmos, `Purchase.tsx:2102-2121`] | Repara o que acontece se alguém tenta lançar uma compra agora: o sistema avisa Abra o caixa antes de realizar compras e volta pra cá. |
| Câmera no botão "Abrir Caixa". | Uma dica: venda, despesa e receita também precisam de caixa aberto. Então o dia começa por aqui: vamos abrir. |

### cap02 · Abrir o caixa (vinheta: ABERTURA)

| Tela | Fala |
| --- | --- |
| Clique em "Abrir Caixa": janela "Abrir Caixa" ("Informe o saldo inicial em dinheiro. Deixe em branco ou 0 se abrir sem dinheiro em espécie."), "Abrir para o usuário" com "Rafael Nogueira (Você)", "SALDO DE ABERTURA (R$)" vazio, as dicas embaixo, o aviso amarelo do zero e "DATA E HORA DE ABERTURA". | Clico em Abrir Caixa. A janela pede o saldo inicial em dinheiro: quanto dinheiro vivo tem na gaveta agora. |
| [ZOOM: o campo "Saldo de Abertura (R$)" vazio e, embaixo, "R$ 1.250,00 foi o valor restante em dinheiro do último caixa (#84)"; o mesmo zoom segue nas três linhas] | O campo vem vazio de propósito. Embaixo tem uma dica: mil duzentos e cinquenta reais foi o que sobrou no último caixa. |
| (zoom continua) | Uma dica: esse número é só uma referência. Conte o dinheiro da gaveta e digite o que contou. Copiar a dica sem contar é o motivo mais comum de diferença no fechamento. |
| (zoom continua) O robô digita "1.500,00" no campo; o aviso amarelo some. | Hoje cedo eu pus mais troco na gaveta e contei mil e quinhentos reais. É isso que eu digito. |
| O zoom solta; câmera em "DATA E HORA DE ABERTURA" (já com 10/11/2026 08:31) e em "Altere para abrir o caixa com data/hora retroativa". [TESTAR: a janela rola até o campo; sem o aviso amarelo do zero a janela fica mais baixa] | Embaixo fica a Data e Hora de Abertura, que já vem com a hora de agora. Ela só aparece pra quem tem a permissão de data retroativa, e serve pro dia em que o caixa ficou sem abrir no sistema. |
| (mesma câmera) | Uma dica: no primeiro caixa da vida da empresa não tem limite. O valor que você digitar é o que inaugura o cofre. |
| O zoom solta; clique em "Abrir Caixa": aviso "Caixa aberto com sucesso!"; aparecem as abas "Início" e "#85 \| Caixa - Rafael Nogueira (você)" e o cartão "DINHEIRO EM CAIXA" com R$ 1.500,00 e "Aberto em: 10/11/2026 08:31". [BACKEND: `get_dinheiro_balance` com `disponivel` 18.500; insert em `cash_register` com `register_number` 85; `cash_transactions` `opening` "Abertura do Caixa #85"] | Abrir Caixa. Pronto: o caixa abriu com mil e quinhentos reais. |

### cap03 · Abrir com zero (vinheta: ABERTURA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`), aba "#85 \| Caixa - Rafael Nogueira (você)"; a câmera desce até "HISTÓRICO DE TRANSAÇÕES", aba "Todas". [ZOOM: a linha com o selo "Abertura", "Abertura do Caixa #85" e R$ 1.500,00] | Lá embaixo, no Histórico de Transações, o sistema lançou sozinho a linha Abertura do Caixa, com os mil e quinhentos. Isso acontece sempre que o caixa abre com dinheiro. |
| O zoom solta. No fim da linha "Abertura", clique nos três pontinhos ("Abrir ações da movimentação"): item "Editar saldo de abertura"; clique: janela "Editar Saldo de Abertura", com "Saldo de Abertura Atual" R$ 1.500,00 e "Novo Saldo de Abertura". | E se você digitou o valor errado na abertura? Não precisa fechar e abrir de novo. Nos três pontinhos dessa linha tem o Editar saldo de abertura. |
| [ZOOM: "Atenção: alterar o saldo de abertura ajusta o Dinheiro em Caixa atual no mesmo valor da diferença. Esta alteração fica registrada na auditoria do caixa."] Clique em "Cancelar". | Você informa o valor certo, o Dinheiro em Caixa se ajusta pela diferença, e a mudança fica registrada. Aqui está certo, então eu cancelo. |
| A câmera passa pela busca "Buscar transação...", por "Filtros" e pelas abas "Todas", "Dinheiro" e "Pix/Transferência". [BACKEND: nada é gravado] | Nesse histórico dá pra buscar, filtrar e corrigir cada lançamento do dia. Isso a gente vê no tutorial Pedidos e histórico do caixa. |
| O zoom solta. [ILUSTRAÇÃO: dia só de Pix: um caminhão sai do pátio com fardos de sucata para um cliente; o pagamento faz uma seta direto para um prédio de banco, com "Pix ou transferência"; a gaveta do caixa fica vazia; aparecem nessa ordem, nesta frase] | Agora imagina um dia em que a Recicla Vale só entrega carga pros clientes, e eles pagam por Pix ou transferência. Nenhum dinheiro vivo passa pela gaveta. |
| (ilustração: a gaveta vazia ganha "R$ 0,00" e o selo "abre com zero") | Aí faz sentido abrir o caixa com zero. É só deixar o campo vazio ou digitar zero. |
| Volta à tela; clique na aba "Início": "ABRIR CAIXA PARA OUTRO USUÁRIO" e o botão "Abrir Caixa"; clique em "Abrir Caixa": a janela vem com "Juliana Prado" em "Abrir para o usuário"; o robô abre a lista e escolhe "Marcos Antunes". | Agora, o caixa do Marcos, o balanceiro. No Início, o administrador abre caixa pra outra pessoa: em Abrir para o usuário, escolho o Marcos. |
| [ZOOM: o aviso amarelo "O caixa será aberto sem dinheiro em espécie (R$ 0,00). Use isso se a operação é só Pix/cartão."] | Repara no aviso amarelo: com o campo vazio, o caixa abre sem dinheiro em espécie. Uma dica: aberto com zero, o caixa não ganha a linha de abertura no histórico. Não está faltando nada. |
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
| [ZOOM: "O caixa só pode abrir com o dinheiro que já está registrado no cofre da empresa. Você tentou abrir com R$ 20.000,00, mas há apenas R$ 17.000,00 disponíveis (R$ 1.500,00 já reservados em caixas abertos)."] | O caixa só abre com o dinheiro registrado no cofre. A gente tentou vinte mil, e o disponível é dezessete mil, porque mil e quinhentos já estão no meu caixa. |
| O zoom solta; a câmera passa pelo link "Ver tutorial: como funciona o dinheiro do caixa" (ícone de play), sem clicar (ele abre em outra aba). | Embaixo desse texto tem um link pro tutorial do dinheiro do caixa, que abre em outra aba. |
| O zoom solta; câmera nos botões "Usar disponível (R$ 17.000,00)" e "Ajustar saldo do dinheiro", sem clicar. | Tem duas saídas. Como o cofre tem saldo, a primeira se chama Usar disponível, e preenche o campo com os dezessete mil do cofre. |
| Cursor sobre "Ajustar saldo do dinheiro", sem clicar. | E Ajustar saldo do dinheiro é pra quando tem dinheiro na empresa que nunca foi lançado. Você corrige o cofre, e o caixa abre sozinho com o valor que tentou. |
| (câmera nos dois botões) | Uma dica: se o aviso aparece e o dinheiro está na sua mão, conte tudo o que a empresa tem em espécie e ajuste o cofre uma vez só. |
| Clique em "Usar disponível (R$ 17.000,00)": o aviso fecha e o campo fica com "17.000,00"; clique em "Abrir Caixa": aviso "Caixa aberto com sucesso!"; aparece a aba "#86 \| Caixa - Marcos Antunes", selecionada, com "DINHEIRO EM CAIXA" R$ 17.000,00. [BACKEND: insert `cash_register` #86 com `opened_by` Marcos e 17.000; `opening` "Abertura do Caixa #86"] | Aqui não é o caso: o Marcos começa com os dezessete mil, e o resto vem do banco mais tarde. Usar disponível, Abrir Caixa, e pronto: o caixa do Marcos está aberto. |

### cap06 · Cofre zerado ou negativo (vinheta: COFRE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`: #85 do Rafael e #86 do Marcos abertos); o `setup` abre fora do vídeo "Início" › "Abrir Caixa" (a janela vem com "Juliana Prado"). [ZOOM: "Disponível no cofre agora: R$ 0,00" e "(de R$ 18.500,00 total", "R$ 18.500,00 está dentro de caixas abertos)."] | Agora o contrário. Com o meu caixa e o do Marcos abertos, todo o dinheiro do cofre está dentro de caixas. O disponível é zero, de dezoito mil e quinhentos no total. |
| O zoom solta. O robô digita "500,00" em "Saldo de Abertura (R$)"; clique em "Abrir Caixa": abre a janela "⚠️ Saldo insuficiente em dinheiro". [BACKEND: `get_dinheiro_balance` com `disponivel` 0 e `reservado_total` 18.500] | Vou abrir um terceiro caixa, o da Juliana, com quinhentos reais de troco. Digito quinhentos e clico em Abrir Caixa. |
| [ZOOM: "Você tentou abrir com R$ 500,00, mas há apenas R$ 0,00 disponíveis (R$ 18.500,00 já reservados em caixas abertos)."] | O aviso é o de antes: tentei quinhentos, e o disponível é zero, porque os dezoito mil e quinhentos já estão nos dois caixas abertos. |
| O zoom solta; câmera nos botões "Abrir zerado (R$ 0,00)" e "Ajustar saldo do dinheiro", sem clicar. | Repara no botão. Sem saldo no cofre, ele não é mais o Usar disponível: vira Abrir zerado. E o Ajustar saldo do dinheiro continua pro dinheiro da empresa que nunca foi lançado. |
| A janela fecha com Esc; fora do vídeo o robô lança uma saída de R$ 1.200,00 direto no cofre; clique em "Abrir Caixa" de novo. [BACKEND: `get_dinheiro_balance` com `disponivel` −1.200,00: o cofre fica em R$ 17.300,00 para R$ 18.500,00 reservados] | Agora imagina que o cofre ficou negativo, com mil e duzentos reais a menos do que estava registrado. Clico em Abrir Caixa de novo. |
| [ZOOM: "Você tentou abrir com R$ 500,00, mas o cofre está negativo em R$ 1.200,00 e não há dinheiro disponível (R$ 18.500,00 já reservados em caixas abertos)."] | Agora o aviso diz que o cofre está negativo em mil e duzentos reais e que não há dinheiro disponível. O botão é o mesmo: Abrir zerado. |
| O zoom solta; câmera no texto abaixo ("Se há dinheiro físico que ainda não foi registrado, ajuste o saldo do dinheiro abaixo — o caixa abre em seguida com o mesmo valor.") e no botão "Ajustar saldo do dinheiro". [TESTAR: o texto de quem não tem a permissão de ajustar contas, "Peça ao responsável para ajustar o saldo do dinheiro nas Movimentações Financeiras, ou abra o caixa zerado (R$ 0,00).", só sai na tela se der para entrar com um usuário sem essa permissão; senão fica só na fala] | Quem pode ajustar contas vê esse texto e o botão Ajustar saldo do dinheiro. Quem não pode vê, no lugar, um recado pedindo ao responsável que ajuste o saldo, ou que abra o caixa zerado. |
| Clique em "Abrir zerado (R$ 0,00)": o aviso fecha e o campo fica com "0,00"; clique em "Abrir Caixa": aviso "Caixa aberto com sucesso!"; aparece a aba "#87 \| Caixa - Juliana Prado" com "DINHEIRO EM CAIXA" R$ 0,00. [BACKEND: insert `cash_register` #87 com `opened_by` a Juliana e 0; sem linha de abertura] | Clico em Abrir zerado. Ele só preenche o campo com zero e fecha o aviso, e eu ainda clico em Abrir Caixa. E o caixa abre: abrir zerado nunca é barrado pelo cofre, nem com ele negativo. |
| (câmera na aba #87 e no cartão "DINHEIRO EM CAIXA") | Uma dica: zerado não tira nada do cofre. Quando entrar dinheiro de verdade nesse caixa, o caminho é o saque do banco, que a gente vê daqui a pouco. |

### cap07 · Os dois cartões (vinheta: CAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), aba "#85 \| Caixa - Rafael Nogueira (você)"; câmera no cartão "DINHEIRO EM CAIXA" com R$ 1.500,00. | Com o caixa aberto, a tela tem dois cartões no topo. O primeiro é o Dinheiro em Caixa: o dinheiro vivo deste caixa, os meus mil e quinhentos. |
| [ZOOM: "Aberto em: 10/11/2026 08:31" e "Dinheiro total da empresa: R$ 18.500,00"] | Embaixo, a hora em que ele abriu e o Dinheiro total da empresa, que é o cofre: dezoito mil e quinhentos. |
| O zoom solta; clique em "Dinheiro total da empresa:": abre "Movimentações Financeiras" na conta "DINHEIRO (COFRE)", com o cartão "O cofre da empresa", R$ 18.500,00 e "Saldo Total em Dinheiro". | Clicando nele, o sistema abre o cofre. |
| [ZOOM: a barra e a legenda "Disponível no cofre: R$ 0,00 (0%)", "Caixa de Rafael Nogueira: R$ 1.500,00 (8%)" e "Caixa de Marcos Antunes: R$ 17.000,00 (92%)"] | A barra mostra onde está cada real: mil e quinhentos no meu caixa, dezessete mil no caixa do Marcos, e nada sobrando no cofre. |
| O zoom solta; menu lateral "Financeiro" › "Caixa"; volta na aba #85; câmera no cartão "SALDO BANCÁRIO" com o valor, as duas contas e os botões "Saque / Sangria", "Nova Movimentação Bancária" e "Saldo de Cliente/Fornecedor". | De volta ao caixa, o segundo cartão é o Saldo Bancário: o dinheiro das contas do banco, onde caem o Pix e a transferência. Os botões dele a gente usa daqui a pouco. |
| Clique no olho do "Dinheiro em Caixa" ("Ocultar saldo"). [ZOOM: o valor vira "R$ ••••••"; o zoom segue na linha de baixo] | No olhinho, você esconde o valor da tela, e ele vira pontinhos. |
| (zoom continua) Clique no olho de novo ("Mostrar saldo"); o zoom solta no fim da fala. | Uma dica: se alguém da equipe vê esses pontinhos sem ter clicado no olho, não é erro. É a permissão Ver Dinheiro Total em Caixa, desligada pra essa pessoa em Usuários e Permissões. |

### cap08 · Cada um com o seu caixa (vinheta: MULTI-CAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), aba #85. [ZOOM: as abas "Início", "#85 \| Caixa - Rafael Nogueira (você)" e "#86 \| Caixa - Marcos Antunes"; o zoom segue na linha de baixo] | Repara nas abas lá em cima: uma pro meu caixa e outra pro do Marcos. Cada operador tem o seu. |
| (zoom continua) | Isso é o multi-caixa. Cada um abre, opera e fecha o próprio caixa. Se faltar dinheiro numa gaveta, você sabe de quem é. |
| O zoom solta; clique no "?" à direita das abas: janela "Como funcionam os Multi-Caixas?"; câmera em "O que acontece ao operar em outro caixa?" e no primeiro item. | No ponto de interrogação, o sistema explica as regras. A principal: compra, venda, despesa e receita em dinheiro mexem só no caixa selecionado. |
| Câmera nos dois itens seguintes ("Saldo bancário (PIX/transferências) é compartilhado..." e "Saldo de clientes/fornecedores também é compartilhado..."). | Já o saldo do banco e o saldo de clientes e fornecedores são da empresa toda. |
| Fecha a janela; clique na aba "Início": "ABRIR CAIXA PARA OUTRO USUÁRIO", "PAINEL GERENCIAL", "Hoje", "2 caixas encontrados" e "RESUMO DO DIA". | Na aba Início fica o Painel Gerencial, com o resumo do dia somando os caixas. Daqui também sai o Abrir Caixa pra outro usuário, como eu fiz com o Marcos. |
| Câmera em "2 caixas encontrados". | E se a empresa preferir um caixa só pra todo mundo, dá pra desligar em Configurações, Usabilidade, na opção Multi-Caixas. |
| Ainda na aba "Início", clique no seletor "Hoje": abre o calendário; o robô escolhe 09/11: aparecem "2 caixas encontrados" (#83 e #84) e o "RESUMO DO DIA" de ontem; o painel fica em 09/11. | O painel não mostra só hoje. No calendário, eu escolho ontem e vejo os caixas e o resumo daquele dia. |
| A câmera desce por "TRANSAÇÕES DO DIA", com o selo e o nome do operador em cada linha, e pelos gráficos "Visão Geral", "Compras por Forma", "Vendas por Forma" e "Distribuição entre Caixas" (só aparecem quando o dia tem movimento: por isso é o painel de 09/11); no fim, clique no botão "Hoje" para voltar. | Mais embaixo, as transações do dia com o nome de quem lançou, e os gráficos: quanto foi em dinheiro e quanto foi por Pix, e quanto cada caixa movimentou. E no botão Hoje, eu volto pro dia de hoje. |
| Clique na aba #85; a câmera desce até "RESUMO DO CAIXA ATUAL": "Total Comprado", "Total Vendido", "Projeção de Lucro", "Receitas" e "Despesas"; clique no olho ("Ocultar valores") e de novo. | Dentro de cada caixa tem o Resumo do Caixa Atual: o que comprou, o que vendeu, a projeção de lucro, as receitas e as despesas só deste caixa. O olhinho esconde os valores, se tiver gente por perto. |
| Câmera no botão "Saldo de Cliente/Fornecedor" do cartão "SALDO BANCÁRIO". | E esse botão lança um recebimento ou um pagamento no saldo de um cliente ou fornecedor, sem sair do caixa. A janela é a mesma do tutorial Clientes, fornecedores e a ficha do parceiro. |

### cap09 · O caixa dos outros (vinheta: MULTI-CAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); clique na aba "#86 \| Caixa - Marcos Antunes": "DINHEIRO EM CAIXA" R$ 17.000,00 e "Aberto em: 10/11/2026 08:4x". | Pra ver o caixa do Marcos, é só clicar na aba dele. Aqui estão os dezessete mil da gaveta dele e a hora em que abriu. |
| Câmera nos botões "NOVA COMPRA", "NOVA VENDA", "NOVA DESPESA" e "NOVA RECEITA". | O que eu lançar com essa aba aberta vai pro caixa do Marcos, não pro meu. Então, antes de lançar no caixa de outra pessoa, confira a aba. |
| A câmera sobe para as abas. | Quem pode ver e operar o caixa dos outros? O administrador e quem tem a permissão Ver e Operar Todos os Caixas. |
| A câmera fica nas abas. | Abrir e fechar caixa também são permissões. Quem não tem vê o botão com um cadeado. |
| [OUTRO USUÁRIO: navegador logado como Marcos Antunes ("o computador da balança"), `/caixa`: o caixa #86 dele, sem as abas, com o selo "#86" ao lado do título "Caixa"; câmera no topo da página] | Já o Marcos, no computador da balança, vê só o caixa dele, sem as abas. |
| (mesma tela) | E todo caixa fechado, de todo operador, fica guardado no Histórico do Caixa, com o nome de quem abriu. |

### cap10 · Saque e sangria (vinheta: MOVIMENTAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), Rafael, aba #85. [ILUSTRAÇÃO: suprimento × sangria: um banco à esquerda, a gaveta "Caixa do Marcos" no meio e o cofre à direita; a gaveta mostra "R$ 17.000,00" e uma meta "R$ 20.000,00"; aparece nesta frase] | Lembra que o Marcos queria vinte mil e abriu com dezessete? Os três mil que faltam vêm do banco. |
| (ilustração: seta verde do banco para a gaveta, com "suprimento" e, embaixo, o nome no sistema: "Saque") | Pôr dinheiro na gaveta durante o dia é o que muita gente chama de suprimento. Quando ele vem do banco, aqui no sistema é um Saque. |
| (ilustração: seta azul da gaveta e do cofre para o banco, com "Sangria") | A sangria é o caminho contrário: o dinheiro sai de um caixa, ou do cofre, e vai pro banco. |
| (ilustração: as duas setas ganham o selo "não é receita nem despesa"; uma moeda pequena "tarifa" sai do banco com o selo "despesa"; a cena some) | Nos dois casos não é receita nem despesa: é o mesmo dinheiro da empresa mudando de lugar. Só a tarifa do banco é despesa de verdade. |
| Clique em "Saque / Sangria": janela "Saque / Sangria" com "Saque" marcado e "Transferir dinheiro do banco para o cofre ou para um caixa aberto". | No botão do saque, a janela abre com a opção Saque marcada. |
| Em "Conta de origem" fica a conta principal; em "Destino do saque" o robô abre a lista e troca o caixa do Rafael por "Caixa de Marcos Antunes". | A conta de origem é a principal do banco. No destino, eu escolho o caixa do Marcos. |
| O robô digita "3.000,00" em "Valor do Saque". [ZOOM: "Valor do Saque" com R$ 3.000,00] | Valor do saque: três mil reais, o que falta pro Marcos. |
| O zoom solta; em "Tem tarifa no saque?" escolhe "Sim"; aparece "Valor da Tarifa" e o robô digita "6,50". [ZOOM: "Valor da Tarifa" com R$ 6,50] | O banco cobrou tarifa? Aqui, sim: seis reais e cinquenta. |
| O zoom solta; câmera em "Efeitos desta transação:": "Saldo da Conta Bancária", "Diminuirá em R$ 3006,50" e "(Saque: R$ 3.000,00 + Tarifa: R$ 6,50)"; "Fundo de Caixa", "Aumentará em R$ 3.000,00". | Embaixo, os efeitos: a conta do banco diminui três mil e seis reais e cinquenta, e o caixa do Marcos aumenta três mil. |
| (câmera nos efeitos) | Uma dica: nunca lance um saque como Nova Receita. Ele entraria no relatório como se a empresa tivesse faturado mais. A tarifa o sistema já lança separada, como despesa. |
| Clique em "Confirmar Saque": aviso "Saque realizado com sucesso!". [BACKEND: `create_manual_bank_transaction` com a saída do banco (−3.000, `transfer`), a tarifa (−6,50, `expense`, "Tarifa de Saque para o Caixa #86") e o espelho do cofre (+3.000); `cash_transactions` `transfer` +3.000 no #86 ("↓ SAQUE · <conta> → Caixa #86"); `adjust_cash_register_balance`] | Confirmar Saque. Pronto: o caixa do Marcos chegou nos vinte mil. |
| Clique de novo em "Saque / Sangria"; em "Destino do saque" o robô abre a lista e pousa em "Cofre (Conta DINHEIRO)", sem escolher; fecha a lista. | Uma dica: se o destino for o cofre e tiver caixa aberto, o sistema pergunta antes de gravar, porque esse dinheiro não aparece na gaveta de ninguém. |
| Câmera em "Data/hora do lançamento"; clique em "Cancelar". | E esqueceu de lançar o saque de ontem? Quem tem a permissão de data retroativa escolhe o dia aqui. A sangria de verdade, a gente faz no fim do dia. |
| Clique em "Cancelar"; clique em "Nova Movimentação Bancária": janela "Nova Movimentação Financeira" com "Tipo" ("Entrada", "Saída", "Transferência"). | Já a Nova Movimentação Bancária é pra entrada ou saída direto no banco, que não vem de pedido. Por exemplo, a tarifa mensal da conta. |
| Clique em "Saída"; em "Conta bancária" o robô escolhe a "Conta Secundária" (a tarifa do pacote da principal é a de R$ 64,90 do extrato da T14); "Descrição": o robô digita "Tarifa mensal do pacote de serviços"; "Valor": "39,90"; "Categoria": abre a lista e escolhe "Tarifas" (a categoria de sistema). Câmera acompanha cada campo. | Saída, a descrição, trinta e nove e noventa, e a categoria Tarifas. |
| Clique em "Salvar": aviso "Movimentação registrada com sucesso!". [BACKEND: `create_manual_bank_transaction` (saída −39,90 da Conta Secundária, categoria "Tarifas", `p_cash_register_id` do #85); a categoria de sistema "Tarifas" na semente (junção: não existe "Tarifas bancárias")] | Salvar. Essa sim entra no resultado como despesa. |

### cap11 · Despesa e receita do dia (vinheta: MOVIMENTAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`), aba "#85 \| Caixa - Rafael Nogueira (você)", 08:5x. Câmera nos botões "NOVA DESPESA" e "NOVA RECEITA". | Nem tudo que sai do caixa é compra de sucata. O gás da empilhadeira, o almoço da equipe, um conserto: isso é despesa, e aqui no caixa ela tem botão próprio. |
| Clique em "Nova Despesa": janela "Nova Despesa" ("Informe o valor e motivo da despesa"), com os blocos "O QUE É", "DINHEIRO", "MAIS DETALHES" e "PARCELAR OU REPETIR". | Nova Despesa. A janela pergunta o que é, de onde sai o dinheiro, e guarda os detalhes mais embaixo. |
| Em "Descrição" o robô digita "Gás da": a partir da terceira letra abre a lista com "Padrão encontrado: Gás da empilhadeira", "Combustível · Pátio · Dinheiro (Caixa)" e "Usado 4 vezes · última vez em setembro de 2026". [ZOOM: a lista e o botão "Preencher"] [BACKEND: `get_financial_description_suggestions` com o padrão do gás; 4 despesas em dinheiro de R$ 50,00 no mundo base] | Começo pela descrição, e o sistema reconhece: essa despesa já foi lançada outras vezes. Ele mostra o padrão encontrado, com a categoria, o centro de custo e a forma de pagamento. |
| Clique em "Preencher": "Descrição" completa para "Gás da empilhadeira"; "Categoria" fica "Combustível", "Centro de custo" "Pátio", "Pagou com" "Dinheiro (Caixa)"; embaixo, "Campos preenchidos. Desfazer preenchimento". O robô digita "50,00" em "Valor". | Clico em Preencher e os campos vêm prontos, inclusive o nome completo. Se não era isso, tem o Desfazer preenchimento logo embaixo. Agora o valor: cinquenta reais. |
| O robô abre a lista "Pagou com": grupo "Dinheiro" com "Dinheiro (Caixa)" e grupo "Contas" com "Conta Principal" e "Conta Secundária"; fecha sem trocar. | Em Pagou com, você diz de onde saiu o dinheiro. Dinheiro, Caixa, sai da gaveta deste caixa. Se você escolher uma conta do banco, a gaveta não muda. |
| Clique em "Mais detalhes": "Observação (opcional)", os anexos e "Não contar na DRE (saldo herdado / histórico)". Câmera desce até "Parcelar ou repetir", sem abrir. | Em Mais detalhes dá pra escrever uma observação e anexar o comprovante. Parcelar e repetir a gente vê no tutorial Contas a Pagar e Receber. |
| Clique em "Confirmar Despesa": aviso "Retirada realizada com sucesso!"; "DINHEIRO EM CAIXA" cai de R$ 1.500,00 para R$ 1.450,00; no "Histórico de Transações", a linha "Despesa", "Gás da empilhadeira", R$ 50,00, "Dinheiro". [ZOOM: o valor do cartão] | Confirmar Despesa. Repara no Dinheiro em Caixa: caiu de mil e quinhentos pra mil quatrocentos e cinquenta. E a despesa já está no histórico. |
| Clique em "Nova Receita": janela "Nova Receita" ("Informe o valor e motivo da receita"); em "Descrição" o robô digita "Aluguel de": o padrão aparece; "Preencher": "Descrição" "Aluguel de caçamba", "Categoria" "Aluguel de caçamba", "Recebeu em" "Conta Principal", forma Pix ou transferência; "Valor": "120,00". [BACKEND: semente com 2 contas a receber pagas "Aluguel de caçamba" de 26/08 e 10/09/2026 (a régua do app só sugere receita a partir de conta a receber ou de dinheiro); "Usado 2 vezes · última vez em setembro de 2026"] | A Nova Receita é o mesmo caminho, pro dinheiro que entra e não é venda de sucata. Aqui, o aluguel de uma caçamba: cento e vinte reais, recebidos por Pix na conta do banco. |
| Clique em "Confirmar Receita": aviso "Depósito realizado com sucesso!"; "DINHEIRO EM CAIXA" segue R$ 1.450,00 e o "SALDO BANCÁRIO" sobe R$ 120,00. | Confirmar Receita. Como caiu no banco, a gaveta não mudou. |
| Câmera nos dois cartões. | Uma dica: receita é dinheiro novo que a empresa ganhou. Troco que vem do banco pra gaveta não é receita, é saque, como a gente acabou de ver. |

### cap12 · Sangria no fim do dia (vinheta: MOVIMENTAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap11` + `dia-10`), 17:30; aba "#86 \| Caixa - Marcos Antunes": "DINHEIRO EM CAIXA" com o valor do fim do dia. | Fim da tarde, e o caixa do Marcos ainda está com muito dinheiro vivo. Dinheiro parado na gaveta é risco. A saída é uma sangria. |
| Clique em "Saque / Sangria" e em "Sangria" ("Transferir dinheiro do cofre ou de um caixa aberto para uma conta bancária"). Em "Origem da sangria" o robô abre a lista ("Cofre (Conta DINHEIRO)", "Caixa de Rafael Nogueira", "Caixa de Marcos Antunes", cada um com o saldo) e escolhe "Caixa de Marcos Antunes". | Em Saque, Sangria, opção Sangria. A origem pode ser o cofre ou um caixa aberto, cada um com o saldo do lado. Escolho o caixa do Marcos. |
| "Conta de destino": "Conta Principal"; "Valor da Sangria": "5.000,00"; "Descrição (Opcional)": "Depósito do fim do dia". [ZOOM: "Valor da Sangria"] | O destino é a conta principal, e o valor, cinco mil reais, que o Marcos vai depositar no banco. |
| Câmera em "Efeitos desta transação:": "Caixa selecionado", "Diminuirá em R$ 5.000,00"; "Conta Bancária de destino", "Aumentará em R$ 5.000,00". | Embaixo, os efeitos: o caixa do Marcos diminui cinco mil, e a conta do banco aumenta cinco mil. |
| Clique em "Confirmar Sangria": aviso "Sangria realizada com sucesso!"; o "DINHEIRO EM CAIXA" do #86 cai R$ 5.000,00. [BACKEND: `create_manual_bank_transaction` com a entrada no banco e o espelho do cofre; `cash_transactions` `transfer` −5.000 no #86; `adjust_cash_register_balance`] | Confirmar Sangria. Não é despesa: o dinheiro só trocou a gaveta pelo banco. |

### cap13 · Fechar o caixa (vinheta: FECHAMENTO)

| Tela | Fala |
| --- | --- |
| Corte para as 17:40 (semente `apos-cap11` + `dia-10` + `apos-cap12`); aba #85 com "DINHEIRO EM CAIXA" R$ 957,10; a câmera desce no "Histórico de Transações": a venda para Aços Quiririm Ltda (Pix/Transferência), as compras de Aparecida Ramos e de Valdir Pereira (Dinheiro), o gás da empilhadeira (Despesa, Dinheiro) e a tarifa mensal. | Fim do dia. No meu caixa entrou a venda pra Aços Quiririm, por transferência, e saíram duas compras em dinheiro, a latinha da Aparecida e o ferro misto do Valdir, mais o gás da empilhadeira que lancei de manhã. |
| A câmera sobe para o botão "FECHAR CAIXA", sem cadeado. [BACKEND: `order_drafts` vazio para o #85] | Antes de liberar o Fechar Caixa, o sistema confere se ficou algum pedido não finalizado neste caixa. |
| [trecho `cap13a`, semente com o rascunho de compra do Valdir Pereira] Aba #85; a câmera desce até "PEDIDOS NÃO FINALIZADOS" com o contador "1" e abre o painel: a compra do Valdir Pereira, "1 item", o peso, R$ 86,00 e "Rafael Nogueira". No `cap13` a câmera segue no botão livre. [BACKEND: `order_drafts` do #85 com 1 item de cobre] | Se ficou, olha o painel Pedidos Não Finalizados. Aqui, uma compra do Valdir pela metade. |
| (`cap13a`) A câmera sobe ao botão "FECHAR CAIXA" com o cadeado; o mouse para em cima: dica "Finalize ou cancele antes de fechar o caixa:" e o pedido. [ZOOM: o botão e a dica] | Enquanto ela estiver aí, o Fechar Caixa fica com cadeado, e passando o mouse ele diz qual pedido está travando. |
| (`cap13a`) Clique no pedido do painel: abre a compra; volta. Corte para o `cap13`: botão sem cadeado. | Clicando no pedido, o sistema abre ele pra você finalizar ou descartar. Resolvido isso, o cadeado some. No nosso dia está tudo finalizado, e o botão está livre. |
| Clique em "Fechar Caixa": janela "Fechar Caixa #85", "Caixa de Rafael Nogueira · Aberto em 10/11/2026 08:31"; por um instante, "Calculando saldo de fechamento..."; câmera nos cartões. | Clico em Fechar Caixa. A janela faz a conta do dia. |
| [ZOOM: "SALDO DE ABERTURA" R$ 1.500,00, "RESTANTE EM CAIXA" R$ 957,10 e, em "SAÍDAS", "COMPRAS" R$ 492,90 com "Dinheiro: R$ 492,90" e "DESPESAS" com "Dinheiro: R$ 50,00"; o zoom segue na linha de baixo] | Abriu com mil e quinhentos, e saíram quatrocentos e noventa e dois e noventa em compras e cinquenta reais de despesa, em dinheiro. A venda, a tarifa e a receita foram pelo banco, então não mexem na gaveta. |
| (zoom continua, centrado em "RESTANTE EM CAIXA") | Restante em caixa: novecentos e cinquenta e sete reais e dez centavos. É o que o sistema espera achar na gaveta. |
| O zoom solta. Câmera em "SAÍDAS" › "DESPESAS" ("Dinheiro: R$ 50,00" e a linha "PIX/Transf.") e em "ENTRADAS" › "VENDAS" ("PIX/Transf.: R$ 2.000,00") e "RECEITAS" (a linha "PIX/Transf." com os R$ 120,00). [TESTAR: se a tarifa de R$ 39,90 entra em "Despesas" › "PIX/Transf." deste caixa] | Cada cartão separa o que foi em dinheiro do que foi por Pix ou transferência. Só a coluna do dinheiro mexe na gaveta: as compras e o gás da empilhadeira. |
| Clique em "Projeção de Lucro" (abre a tabela por material: "Material", "Comprado (kg)", "Valor Compra", "Vendido (kg)", "Valor Venda"). | A Projeção de Lucro mostra o dia material por material. E no Relatório de Pedidos do Caixa você confere quanto comprou e quanto vendeu de cada um. |
| O zoom solta. [ILUSTRAÇÃO: esperado × contado: à esquerda uma pilha de notas "esperado: R$ 957,10"; à direita, uma mão contando notas da gaveta, "contado"; aparecem nessa ordem, nesta frase] | Agora vem a conferência. De um lado, o que o sistema espera. Do outro, o que você conta na gaveta. |
| (ilustração: as duas pilhas ficam iguais e ganham um visto; depois uma segunda versão rápida com a pilha da direita menor e o rótulo "diferença"; a cena some) | Se os dois batem, o caixa fecha sem diferença. Se não batem, a diferença fica registrada, pra mais ou pra menos. |
| Volta à janela; câmera em "VALOR DE FECHAMENTO" já preenchido com "957,10", "Digite o valor físico em dinheiro que está no caixa" e "Valor esperado pelo sistema: R$ 957,10". | O Valor de Fechamento já vem com o esperado. Mesmo assim, conte a gaveta e digite o que contou. |
| O robô digita "950,00" no "Valor de Fechamento": borda amarela, "Diferença detectada: -R$ 7,10" e a chave "Registrar diferença no DRE". [ZOOM: o aviso e a chave] | Olha o que acontece se eu contar novecentos e cinquenta: o sistema mostra a diferença, sete reais e dez centavos a menos. |
| (zoom continua em "...essa falta também conta como Prejuízo (despesa) no resultado da empresa.") | A chave Registrar diferença no DRE decide se essa falta entra no resultado como prejuízo. Se fosse sobra, entraria como ganho. O cofre fica sempre com o valor que você contou. |
| O zoom solta; o robô corrige para "957,10": o aviso some. [ZOOM: o campo e "Valor esperado pelo sistema: R$ 957,10"] | Contei de novo, e tinha uma nota dobrada: novecentos e cinquenta e sete e dez. Bateu, então não aparece diferença. |
| (câmera no campo) | Uma dica: o campo aceita valor negativo. É pro dia em que saiu mais dinheiro do que tinha, e alguém completou com dinheiro de fora. O sistema não impede: ele registra. |
| Câmera em "Data/hora do fechamento" e em "Altere para fechar o caixa com data/hora retroativa". | Com a mesma permissão de data retroativa, dá pra fechar com a data e a hora em que o caixa parou de verdade. |
| Clique em "Confirmar Fechamento": aviso "Caixa fechado com sucesso!" e a janela "Imprimir Relatório" ("Deseja imprimir o relatório de fechamento de caixa?", "Não, obrigado", "Ver comprovante"). [BACKEND: update `cash_register` (`status` closed, `closing_balance` 957,10, `closed_at`); `cash_transactions` `closing` 957,10; sem `adjustment` (diferença zero)] | Confirmar Fechamento. O dinheiro contado volta pro cofre, e o sistema oferece imprimir o relatório do fechamento. |
| Clique em "Não, obrigado"; a tela volta para a aba "Início". | Desta vez, não, obrigado. O relatório fica guardado no Histórico do Caixa, pra imprimir quando quiser. |

### cap14 · Reabrir um caixa (vinheta: FECHAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`), aba "Início": "MEU CAIXA", "Abrir Caixa" e o cartão amarelo "#85 · R$ 957,10", "Rafael Nogueira", "10/11 08:31 → 10/11 17:4x", "reabrir outro caixa" e "Reabrir #85". | Fechei e lembrei de uma compra que ficou sem lançar. O caminho é reabrir o caixa. |
| (cartão amarelo na tela) | Reabrir é pra lançar o que ficou de fora. Pra corrigir uma compra ou venda de um caixa já fechado, não precisa: a edição do pedido deixa manter o caixa original ou escolher um caixa aberto. Isso está no tutorial Pedidos e histórico do caixa. |
| [ZOOM: o cartão amarelo] | Olha o cartão amarelo de novo: agora ele mostra o caixa que eu acabei de fechar, com o valor e o horário. |
| O zoom solta; clique em "reabrir outro caixa": janela "Reabrir outro caixa" ("Escolha qual caixa fechado deseja reabrir. Ele volta exatamente como estava antes do fechamento."), lista com #85 (Rafael Nogueira, R$ 957,10), #84 (Rafael Nogueira, R$ 1.250,00), #83 (Marcos Antunes, R$ 640,00) e os anteriores. | No link reabrir outro caixa aparecem os últimos caixas fechados, de todos os operadores, com o nome de quem abriu. |
| Câmera na linha do #83, do Marcos, sem clicar. | Dá pra reabrir o caixa de outra pessoa, desde que ela não esteja com outro caixa aberto. Cada operador fica com um caixa aberto por vez. |
| O #85 já vem marcado (é o primeiro); clique em "Reabrir #85": janela "Reabrir caixa #85?" com "O caixa será reaberto exatamente como estava antes do fechamento. Todas as transações registradas continuarão associadas a este caixa." e o quadro "#85 · R$ 957,10". | O meu já vem marcado. Clico em reabrir, e o sistema confirma: o caixa volta exatamente como estava, com tudo que foi lançado nele. |
| Clique em "Reabrir Caixa": aviso "Caixa reaberto com sucesso!"; volta a aba "#85 \| Caixa - Rafael Nogueira (você)" com "DINHEIRO EM CAIXA" R$ 957,10. [BACKEND: update `cash_register` (`status` open, `closed_at` e `closing_balance` nulos, `reopened_at`); delete das linhas de diferença do fechamento (nenhuma aqui)] | Reabrir Caixa. Pronto: o caixa está aberto de novo. Agora é só lançar o que faltou e fechar outra vez. |

### cap15 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem: o cartão amarelo e o aviso "Abra o caixa antes de realizar compras". | Recapitulando: a gente viu a tela com o caixa fechado, o cartão amarelo de reabrir, e que sem caixa aberto a compra não sai. |
| Montagem: o campo com R$ 1.500,00 e o aviso amarelo do zero. | Abriu o caixa com o dinheiro contado, sem copiar a dica, e viu quando faz sentido abrir com zero. |
| Montagem: a ilustração do cofre e a janela "⚠️ Saldo insuficiente em dinheiro". | Entendeu o cofre, que é todo o dinheiro vivo da empresa, o aviso de saldo insuficiente com as duas saídas, e que abrir zerado nunca é barrado, nem com o cofre negativo. |
| Montagem: os dois cartões e as abas dos dois caixas. | Conheceu os dois cartões, abriu o caixa do Marcos, viu cada operador com a sua aba e o painel do dia. |
| Montagem: "Padrão encontrado" da despesa e o aviso "Retirada realizada com sucesso!". | Lançou uma despesa em dinheiro e uma receita no banco, com o preenchimento que o sistema sugere. |
| Montagem: "Efeitos desta transação:" do saque. | Fez um saque do banco pro caixa do Marcos, com a tarifa, lançou a tarifa mensal direto no banco, e no fim do dia fez a sangria do caixa dele pro banco. |
| Montagem: "Diferença detectada" e "Efeitos desta transação:" da sangria. | Viu a diferença aparecer no fechamento, antes de acertar a contagem. |
| Montagem: "Valor esperado pelo sistema: R$ 957,10" e "Reabrir caixa #85?". | E fechou o caixa batendo com a contagem, e reabriu pelo cartão amarelo. |
| Cartão "Próximo: Comprar e vender sucata". | No próximo tutorial, a parte que a Recicla Vale faz o dia inteiro: comprar e vender sucata. Até lá! |
