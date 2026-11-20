# Roteiro T13 · Contas a Pagar e Receber

Roteiro pronto para o ensaio e, depois da revisão geral, para a voz (molde da Domiflix, sem etapa de aprovação). Coluna
Fala = texto da narração (voz Kaik Barreto), na grafia da legenda; o texto exato do TTS, com a grafia de pronúncia, está em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
(`T13/inventario.md`, EcoSistema 1.60.18).
Desktop (tela de 1600×900), logado como Rafael Nogueira (MASTER). Todo capítulo parte de um navegador novo na tela
"Contas a Pagar/Receber", com o mundo do fim do capítulo anterior (sementes `t13/inicio` e `t13/apos-capNN`); quando um
capítulo continua uma janela do anterior, o `setup` do robô a reabre fora do vídeo.

- **Título:** Contas a Pagar e Receber
- **Antes:** Estoque: saldo, histórico e posição (T10)
- **Próximo:** Bancos, cofre e conciliação bancária (T14)
- **Vinhetas (áreas):** CONTAS · LANÇAMENTO · RECORRÊNCIA · BAIXA · FIADO · COMPROVANTE · FILTROS · RESUMO (todos os
  capítulos menos o 0)
- **Duração estimada:** ~22 min de vídeo (3.074 palavras de fala, ~19,7 min de voz a 2,6 palavras/s, mais a vinheta de abertura, 19 vinhetas de capítulo, a cartela e as esperas dos formulários; as ilustrações correm junto da fala; alvo da fonte: 16 min, ampliado a pedido do Kaik: cobrir cada função em detalhes). 20 capítulos (0 a 19): novos 06, 10, 12, 13, 14 e 18; os da 1.59.154 ficaram em 01 a 05, 07, 08, 09, 11, 15, 16, 17 e 19.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos.
- **Estado inicial:** `plano.md` → "Mundo: o que esta aula precisa" (contas bancárias sem logo, centros de custo, categorias,
  a Hidráulica Moretti, a água vencida, o aluguel pago, a energia de hoje, as três parcelas da Fundição e o saldo da Aços
  Quiririm).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso precisa ter), `[ZOOM: ...]` (campo crítico; dura a frase
  inteira), `[ILUSTRAÇÃO: ...]` (cena desenhada no estilo da marca, nunca tela do app), `[TESTAR: ...]` (o robô confere
  antes de gravar).
- Nenhuma mensagem de erro encenada: os ⚠️ entram falados com "Uma dica:" e a tela mostra o caminho certo.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Contas a Pagar e Receber". | (sem fala) |
| [ILUSTRAÇÃO: as contas espalhadas: um balcão de ferro-velho com papéis soltos (o boleto da energia, o recibo da água, um caderninho do fiado aberto em "Aços Quiririm", um bilhete "aluguel dia 5"), desenhados no estilo da marca, sem logo de terceiros; os papéis balançam de leve] | Oi! Neste tutorial a gente vai organizar o que a Recicla Vale Metais tem pra pagar e pra receber. |
| (a ilustração: o boleto da energia ganha um selo vermelho "vence hoje"; o caderninho do fiado fica em destaque) | Sabe a conta de luz que só aparece no dia do vencimento? E o cliente que levou a prazo, e ninguém lembra quando paga? |
| (a ilustração: cada papel voa e vira uma linha de uma lista com três colunas, "data", "categoria" e "de quem", em verde) | Aqui, tudo entra com data, categoria e de quem é. O que a empresa paga e o que ela recebe, numa tela só. |
| Cartão discreto: "Antes: Estoque: saldo, histórico e posição". | Se você ainda não viu o tutorial do Estoque, dá uma olhada antes. |
| Dashboard da Recicla Vale Metais, logado como Rafael Nogueira (sem enquadrar os números do Dashboard); o cursor vai ao menu lateral, abre "Financeiro" e clica em "Contas a Pagar/Receber"; a tela abre na aba "Todas". [BACKEND: semente `t13/inicio`] | A tela fica no menu, em Financeiro, Contas a Pagar/Receber. [pause] Vamos conhecer a tela. |

### cap01 · A tela e as abas (vinheta: CONTAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/inicio`), aba "Todas"; a câmera passa pelo caminho "Financeiro › Contas a Pagar/Receber" e pelo título. | Esta é a tela das contas. Ela abre na aba Todas, com o que a empresa paga e o que recebe, juntos. |
| Clique em "A Pagar" (a aba fica vermelha): só contas a pagar; clique em "A Receber": as parcelas da Fundição Bandeira do Vale e, no fim, as linhas com o chip "Saldo"; volta para "Todas". | Na aba A Pagar fica só o que sai, em vermelho, pra não confundir com dinheiro entrando. Na A Receber, só o que entra. |
| A câmera percorre o cabeçalho da lista: "Descrição", "Categoria", "Emissão", "Vencimento", "Valor", "Status", "Quitada em", "Ações". | Cada linha é uma conta, com a descrição, a categoria, o vencimento, o valor e o status. |
| A câmera vai à linha "Água e esgoto de outubro": o vencimento 05/11/2026 num selo vermelho e o status "Vencida". | A água de outubro venceu dia cinco e não foi paga. Por isso ela está Vencida, com a data em vermelho. |
| A câmera desce à linha "Energia elétrica de outubro" ("Pendente", 10/11/2026) e depois à "Aluguel do galpão de novembro" ("Paga", "Quitada em" 05/11/2026). | A energia vence hoje e está Pendente. E o aluguel do galpão foi pago no dia cinco: está Paga. |
| O mouse para em cima do status "Vencida" da água: a dica mostra "Vencimento 05/11/2026" e "Vencida há 5 dia(s)". [TESTAR: texto da dica] | Parando o mouse em cima do status, o sistema conta mais: há quantos dias a conta venceu, ou quanto já foi pago. |
| Clique no meio da linha "Energia elétrica de outubro" (na categoria, longe dos botões): janela "Detalhes da conta" ("Informações completas do lançamento"), com "Tipo", "Valor", "Vencimento", "Categoria", "Cliente/fornecedor", "Parcela" e "Observação"; fecha (Esc). | E clicando na linha, abrem os Detalhes da conta: tipo, valor, vencimento, categoria, de quem é, a parcela e a observação. |
| A câmera sobe ao botão "Nova conta", no canto de cima. | Pra lançar uma conta nova, o botão é este: Nova conta. |

### cap02 · Os quatro cartões do topo (vinheta: CONTAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/inicio`), aba "Todas"; a câmera sobe para os quatro cartões. | Antes da lista, os quatro cartões lá de cima. Eles mostram quanto a empresa deve, quanto tem pra receber e o que está apertando. |
| [ZOOM: os cartões "Total a Pagar" e "Total a Receber", com os valores] | O Total a Pagar soma as contas que a empresa ainda deve, mais o que ela deve no saldo, o fiado. O Total a Receber é o contrário: as contas a receber, mais o que devem pra ela no saldo. |
| [ILUSTRAÇÃO: vencidas e os próximos sete dias: uma régua de novembro com "hoje, 10/11" no meio; à esquerda, a água (05/11) num bloco vermelho "Vencidas"; à direita, uma janela laranja de 10/11 a 17/11 com a energia (10/11) e a primeira parcela da Fundição (17/11), rotulada "Vence em 7 dias"; a janela acende quando a frase fala dela] | Vencidas é o que passou do vencimento e não foi pago, como a água. Vence em 7 dias é o que vence de hoje até daqui a sete dias, como a energia. |
| De volta à tela: [ZOOM: os cartões "Vencidas" e "Vence em 7 dias"] | Esses dois somam só contas, as a pagar e as a receber. O saldo não tem data de vencimento, então fica de fora deles. |
| A câmera abre para os cartões e as abas; clique em "A Pagar" (o segundo cartão vira "Total pago"), em "A Receber" ("Total recebido") e volta para "Todas". | Uma dica: os cartões acompanham o que está na lista. Na aba A Pagar, eles mostram o Total a Pagar e o Total pago. Na A Receber, o Total a Receber e o Total recebido. E com busca ou filtro ligado, somam só o que apareceu. |

### cap03 · Lista e calendário (vinheta: CONTAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/inicio`); a câmera vai aos botões "Lista" (marcado) e "Calendário", ao lado das abas. | E dá pra ver as mesmas contas num calendário. A tela abre na Lista, e do lado fica o Calendário. |
| Clique em "Calendário": novembro de 2026, os dias de "Dom" a "Sáb", etiquetas vermelhas e verdes nos dias com conta, o dia 10 marcado como hoje. | No calendário, cada dia mostra as contas que vencem nele. Vermelho é conta a pagar, e verde, a receber. |
| A câmera vai ao dia 5: o triângulo de alerta e a etiqueta "Água e esgoto de outubro". | O triângulo avisa que tem conta vencida naquele dia. É a água, do dia cinco. |
| Clique no dia 10: janela "Contas de 10/11/2026" com "Energia elétrica de outubro", "A Pagar", o valor e os botões "Marcar pago" e "Editar"; fecha a janela (Esc). | Clicando no dia, aparecem as contas dele, já com os botões de pagar e de editar. |
| A câmera vai ao aviso do topo: "Saldos de clientes/fornecedores não têm vencimento — veja na visão de Lista." | Uma dica: o calendário mostra só conta com vencimento. O saldo dos clientes e fornecedores não tem data, então ele fica na Lista, como a própria tela avisa. |
| Clique em "Lista": a lista volta. | Pra voltar, é só clicar em Lista. |

### cap04 · Lançar uma conta (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/inicio`), aba "Todas"; clique em "Nova conta": janela "Nova conta" ("Cadastre uma conta a pagar ou a receber com vencimento."), bloco "O que é"; o cursor já nasce na "Descrição". | Agora, lançar uma conta nova. A Hidráulica Moretti vai fazer a manutenção da prensa, com vencimento no dia dezenove. Clico em Nova conta. |
| A câmera mostra o "Tipo" em "A pagar (despesa)". | O Tipo já vem como A pagar. Se fosse dinheiro entrando, seria A receber. |
| Em "Descrição" ("Ex: Aluguel do galpão") digita "Manutenção da prensa enfardadeira"; em "Vencimento" abre o calendário e escolhe 19 (19/11/2026). | Na Descrição, o que é a conta: manutenção da prensa enfardadeira. E o Vencimento, dezenove de novembro. |
| Em "Valor" digita 3.480,00. [ZOOM: "Valor" com 3.480,00] | No Valor, três mil quatrocentos e oitenta reais. |
| Em "Categoria" abre a lista ("Pesquisar categoria..."), digita "Manut" e escolhe "Manutenção de máquinas". | A Categoria diz que tipo de gasto é esse. Aqui, Manutenção de máquinas. |
| Em "Cliente / Fornecedor" o tipo já está em "Fornecedor"; clica em "Selecione o fornecedor", digita "Moretti" e escolhe "Hidráulica Moretti Ltda". [BACKEND: busca de `suppliers` por nome] | Como é conta a pagar, o campo já vem em Fornecedor. É só escolher a Hidráulica Moretti. |
| Em "Centro de custo" ("— Nenhum —") escolhe "Pátio". | O Centro de custo diz qual parte da empresa gastou. A prensa fica no pátio, então, Pátio. |
| No bloco "Dinheiro", em "Pagamento previsto" ("Não definido") escolhe "Conta Principal" (grupo "Contas"); ao lado aparece "Forma de pagamento" com "Pix / Transferência" (padrão; as outras são "Boleto" e "Cheque"). [ZOOM: "Forma de pagamento"] | No Pagamento previsto, eu digo de onde esse dinheiro deve sair: da Conta Principal. É só uma previsão, mas na hora de pagar ela já vem sugerida. Do lado aparece a Forma de pagamento: Pix ou transferência, boleto ou cheque. Deixo no Pix. |
| Clique em "Criar conta": aviso "Conta criada"; a linha "Manutenção da prensa enfardadeira", com "Hidráulica Moretti Ltda" embaixo, a categoria com a etiqueta "Conta Principal", vencimento 19/11/2026, R$ 3.480,00 e "Pendente". [ZOOM: a linha nova, com 19/11/2026 e R$ 3.480,00] [BACKEND: insert em `financial_bills`; o select do aviso de conta igual (mesmo fornecedor, vencimento e valor) devolve vazio] | Criar conta. Pronto: a manutenção entrou na lista, pendente, com a data, a categoria e o fornecedor. |
| A câmera fica na linha. | Uma dica: se faltar uma categoria ou um fornecedor, o botão de mais, do lado do campo, cadastra na hora, sem sair daqui. E se você lançar a mesma conta duas vezes, o sistema avisa antes: Conta igual já cadastrada. |

### cap05 · A conta que já nasce paga (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap04`); clique em "Nova conta". | E quando a conta chega já paga? Ontem, o conserto do pneu da empilhadeira foi pago na hora, por Pix: cento e oitenta reais. |
| Preenche (o que passar da fala vai acelerado): "Descrição" "Conserto do pneu da empilhadeira"; "Vencimento" 09/11/2026; "Valor" 180,00; "Categoria" "Manutenção de máquinas"; "Centro de custo" "Pátio". | Preencho como qualquer conta: a descrição, a data de ontem, o valor, a categoria e o centro de custo. |
| Em "Pagamento previsto" escolhe "Conta Principal". | No Pagamento previsto, a conta de onde o Pix saiu: a Conta Principal. |
| Liga "Já paguei essa conta" ("Registra o pagamento agora — a conta já nasce quitada."); aparece "Data do pagamento" com 10/11/2026; no calendário escolhe 9 (09/11/2026). | Agora o que muda: ligo o Já paguei essa conta. Ele registra o pagamento junto, e a conta já nasce quitada. Na Data do pagamento, ontem. |
| Clique em "Criar conta": aviso "Conta criada e paga"; na busca ("Buscar por valor, descrição ou parceiro...") digita "pneu": a linha "Conserto do pneu da empilhadeira", "Paga", "Quitada em" 09/11/2026. [BACKEND: insert em `financial_bills` + rpc `pay_financial_bill` (transfer, Conta Principal, R$ 180,00, 09/11)] | Criar conta. Ela já entra como Paga, e o dinheiro já saiu da Conta Principal. Nada fica pendente pra lembrar depois. |
| A câmera fica na linha. | Numa conta a receber, a opção vira Já recebi essa conta. |

### cap06 · O sistema preenche pra você (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap05`, variante lateral), aba "Todas"; clique em "Nova conta": o cursor já está em "Descrição". | Tem conta que volta todo mês com os mesmos dados. A internet do escritório, por exemplo. Pra essas, o sistema ajuda a preencher. |
| Digita "Internet do escritório" (inteiro); embaixo do campo abre "Padrão encontrado: Internet do escritório". [BACKEND: rpc `get_financial_description_suggestions` (`p_context` bill, `p_direction` payable)] | Começo pela Descrição: Internet do escritório. Repara que, depois de três letras, aparece um Padrão encontrado. |
| [ZOOM: o bloco, com "Vale Fibra Telecom Ltda · Telefone e internet · Conta Principal · Boleto" e "Usado N vezes · última vez em <mês> de 2026"; o N e o mês saem da tela do ensaio] | Ele mostra o que a empresa usou das outras vezes: o fornecedor, a categoria, a conta do banco e a forma de pagamento. E quantas vezes esse padrão já foi usado. |
| Clique em "Preencher": "Categoria", o fornecedor, "Pagamento previsto" ("Conta Principal") e "Forma de pagamento" ("Boleto") preenchidos; o cursor vai para "Valor"; embaixo da descrição, "Campos preenchidos. Desfazer preenchimento". | Clico em Preencher. Pronto: categoria, fornecedor e pagamento previsto, tudo de uma vez. E o cursor já pula pro Valor. |
| Em "Valor" digita 289,90; em "Vencimento" escolhe 15 (15/11/2026). [ZOOM: "Valor" com 289,90] | Digito duzentos e oitenta e nove e noventa, e ajusto o Vencimento pro dia quinze. |
| A câmera vai a "Campos preenchidos. Desfazer preenchimento" (sem clicar). | Uma dica: o padrão só preenche campo vazio. O que você já escolheu, ele não troca. E se não era isso, tem o Desfazer preenchimento, logo embaixo. |
| A câmera fica na janela. | Dá pra fazer tudo pelo teclado: as setas escolhem o padrão, e o Enter ou o Tab preenchem. |
| Clique em "Criar conta": aviso "Conta criada"; a linha "Internet do escritório", 15/11/2026, R$ 289,90, "Pendente", etiqueta "Boleto · Conta Principal". [BACKEND: insert em `financial_bills` com `expected_payment_method` boleto] | Criar conta. E de onde vêm os padrões? Das contas e dos lançamentos do último ano com a mesma descrição. Vale também nas contas a receber e nas entradas e saídas do caixa e do banco. |

### cap07 · Parcelar uma conta (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap05`); clique em "Nova conta". | Agora uma compra dividida em vezes. Os pneus novos do caminhão truck saíram por sete mil e oitenta reais na Auto Peças Vale Forte, em três vezes. |
| Preenche (o que passar da fala vai acelerado): "Descrição" "Pneus do caminhão truck"; "Vencimento" 23/11/2026. | Primeiro a descrição e o Vencimento: a data da primeira parcela, vinte e três de novembro. |
| Em "Valor" digita 7.080,00; depois (acelerado) "Categoria" "Manutenção de veículos" e fornecedor "Auto Peças Vale Forte". [ZOOM: "Valor" com 7.080,00] | No Valor vai o total da compra, sete mil e oitenta, e não o valor da parcela. Categoria e fornecedor, como antes. |
| Clique em "Parcelar ou repetir" (a seção abre); liga "Parcelar": abre "Configurar faturamento" ("Parcelar R$ 7.080,00 do saldo"), com "Condição de pagamento" em "Manual (definir parcelas)". | Embaixo, em Parcelar ou repetir, ligo o Parcelar. |
| Em "Nº de parcelas" clica em "3": as linhas 1 · 23/11/2026 · R$ 2.360,00, 2 · 23/12/2026 · R$ 2.360,00 e 3 · 23/01/2027 · R$ 2.360,00; a faixa verde "Soma das parcelas" R$ 7.080,00. [ZOOM: as três linhas e a faixa "Soma das parcelas"] | Escolho três parcelas. O sistema divide o valor e põe uma por mês, no mesmo dia: dois mil trezentos e sessenta reais cada. A soma fecha com o total, por isso a faixa fica verde. |
| Clique em "Aplicar faturamento": na seção, o resumo "3x — 1º venc. 23/11/2026 — total R$ 7.080,00" e o botão "Editar". | Aplicar faturamento. O resumo mostra as três vezes, a primeira data e o total. |
| Clique em "Criar conta": aviso "3 parcelas criadas"; na busca digita "pneus": as três contas da Auto Peças Vale Forte, 23/11/2026, 23/12/2026 e 23/01/2027, R$ 2.360,00, "Pendente". [BACKEND: rpc `create_installment_bills` (três `financial_bills`, `installment_number` 1 a 3; descrição como a RPC real grava)] | Criar conta. Pronto, três parcelas criadas. |
| [ILUSTRAÇÃO: uma compra, três contas: o cartão "Pneus do caminhão truck · R$ 7.080,00" se divide em três cartões "R$ 2.360,00" (23/11, 23/12, 23/01), cada um com o selo "Pendente"; um deles ganha um "pago" e os outros seguem iguais] | Cada parcela vira uma conta separada. Dá pra pagar uma sem mexer nas outras. |
| (a ilustração: ao lado, dois quadros: "Parcelar: dívida com fim, como os pneus em 3x" e "Repetir: o gasto que volta todo mês, como um aluguel") | Parcelar é pra dívida com fim, como esses pneus. Pro gasto que volta todo mês, é o Repetir, que vem agora. |

### cap08 · A conta que se repete (vinheta: RECORRÊNCIA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap06`); clique em "Nova conta". | A empilhadeira da Recicla Vale é alugada: dois mil e trezentos reais todo dia doze, num contrato até abril. |
| Preenche (o que passar da fala vai acelerado): "Valor" 2.300,00; "Descrição" "Aluguel da empilhadeira"; "Vencimento" 12/11/2026; "Categoria" "Aluguel". [ZOOM: "Valor" com 2.300,00] | Valor, descrição e categoria, como sempre. O Vencimento é o da primeira: doze de novembro. |
| Clique em "Parcelar ou repetir"; liga "Repete?" ("Gera contas automaticamente na frequência escolhida."): aparecem "Frequência" ("Mensal"), "A cada" (1) e "Repetir até (opcional)". | Em Parcelar ou repetir, agora eu ligo o Repete. Ele gera as contas sozinho, na frequência que você escolher. |
| Abre "Frequência": "Semanal", "Mensal" e "Anual"; deixa "Mensal"; "A cada" fica 1. | Pode ser semanal, mensal ou anual. Aqui é mensal, a cada um mês. |
| Em "Repetir até (opcional)", no calendário, avança até abril de 2027 e escolhe 12 (12/04/2027); a câmera passa por "Deixe vazio para repetir sem data-fim.". | E no Repetir até, a data de parar: doze de abril, o fim do contrato. Sem data, ele repete sem fim. |
| Clique em "Criar conta": aviso "Conta recorrente criada"; na busca digita "aluguel da" (pega só o aluguel da empilhadeira, e não o conserto do pneu): seis contas "Aluguel da empilhadeira", de 12/11/2026 a 12/04/2027, R$ 2.300,00. [BACKEND: rpc `create_recurring_bill_template`: molde mensal (12/11/2026 a 12/04/2027) + todas as contas até a data de parar: 12/11, 12/12, 12/01, 12/02, 12/03 e 12/04 (com "Repetir até" a RPC cria todas)] | Criar conta. Repara: já entraram todas, de novembro até abril. |
| [ILUSTRAÇÃO: o molde e a janela de três meses: no alto, o cartão-molde "Aluguel da empilhadeira · R$ 2.300,00 · todo dia 12 · até 12/04/2027"; embaixo, uma régua de novembro a abril com as seis contas (12/11 a 12/04) já criadas até a bandeirinha "Repetir até"; no quadro "sem data", a moldura verde "próximos 3 meses" e a régua que anda um mês e cria a seguinte] | O sistema guarda um molde da conta. Com data de parar, ele já cria todas até ela. Sem data, ele mantém sempre os próximos três meses na lista e cria a seguinte sozinho, conforme o tempo passa. |

### cap09 · Só esta ou esta e as próximas (vinheta: RECORRÊNCIA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap07`); na busca digita "aluguel da": as três contas "Aluguel da empilhadeira" (12/11, 12/12 e 12/01). | E se uma delas mudar? A locadora pediu pra passar o vencimento pro dia quinze, a partir de dezembro. |
| Na linha de 12/12/2026, clique no lápis "Editar": janela "Editar conta recorrente", ""Aluguel da empilhadeira" faz parte de uma recorrência. O que deseja editar?", com "Só esta conta", "Esta e as próximas" e "Cancelar". | Clico em editar na de dezembro. Como ela faz parte de uma recorrência, o sistema pergunta antes: só esta conta, ou esta e as próximas? |
| [ILUSTRAÇÃO: só esta e esta e as futuras: a régua com as contas de novembro, dezembro e janeiro e o molde em cima; "Só esta conta" acende só dezembro; "Esta e as próximas" acende dezembro a abril e o molde; novembro, que ficou pra trás, não muda] | Só esta conta mexe só na de dezembro. Esta e as próximas muda esta, as seguintes que ainda não foram pagas e o molde, pras novas já nascerem certas. |
| Clique em "Esta e as próximas": janela "Editar conta"; em "Vencimento", no calendário, troca 12/12/2026 por 15 (15/12/2026); embaixo aparece "Esta data e as futuras serão deslocadas pelo mesmo período.". | Escolho Esta e as próximas e mudo o vencimento pra quinze de dezembro. Repara no aviso: as próximas andam o mesmo tanto. |
| Clique em "Salvar": aviso "Conta atualizada"; a lista: 12/11/2026, 15/12/2026, 15/01, 15/02, 15/03 e 15/04/2027. [BACKEND: update em `recurring_bill_templates` e nas `financial_bills` futuras não pagas; rpc `shift_recurring_bills_due_date` (de 12/12 para 15/12: +3 dias)] | Salvar. Novembro ficou no dia doze, e de dezembro em diante foi tudo pro dia quinze. |
| Na linha de 15/01/2027, clique na lixeira "Excluir": janela "Excluir conta recorrente", ""Aluguel da empilhadeira" faz parte de uma recorrência. O que deseja excluir?", "Só esta conta" e "Esta e as próximas" (vermelho); clique em "Cancelar". | Excluir faz a mesma pergunta. Esta e as próximas encerra a recorrência daqui pra frente, e as contas já pagas ficam no histórico. Aqui eu só cancelo. |

### cap10 · E as parcelas? (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap09`, variante lateral); na busca digita "pneus": as três parcelas da Auto Peças Vale Forte. | As parcelas dos pneus funcionam parecido. A Auto Peças pediu pra passar o vencimento pro dia vinte e oito, a partir da segunda. |
| Na parcela de 23/12/2026, clique no lápis "Editar": janela "Editar parcelas", ""Pneus do caminhão truck (parcela 2/3)" faz parte de um parcelamento. O que deseja editar?", com "Só esta conta", "Esta e as próximas", "Todas as parcelas pendentes" e "Cancelar". | Clico em editar na parcela dois. Aqui são três opções: Só esta conta, Esta e as próximas, ou Todas as parcelas pendentes. |
| Clique em "Esta e as próximas": "Editar conta" (descrição "Pneus do caminhão truck"); em "Vencimento" troca para 28 (28/12/2026); aparece "Esta data e as futuras serão deslocadas pelo mesmo período.". | Escolho Esta e as próximas e troco o vencimento pra vinte e oito de dezembro. |
| Clique em "Salvar": aviso "2 parcelas pendentes atualizadas"; a lista: 23/11/2026, 28/12/2026 e 28/01/2027. [BACKEND: rpc `update_installment_bill_group` (`p_scope` future)] | Salvar. A segunda e a terceira andaram juntas, e a primeira ficou como estava. |
| A câmera fica nas três linhas. | Uma dica: nessa edição em grupo, o valor e os outros campos da tela vão pra todas as parcelas escolhidas. Se as parcelas têm valores diferentes, mude uma de cada vez, com Só esta conta. |
| Na parcela de 28/01/2027, clique na lixeira: "Excluir parcelas", com as três opções ("Esta e as próximas" e "Todas as parcelas pendentes" em vermelho) e "Parcelas pagas ou com baixa permanecem no histórico e não serão excluídas."; clique em "Cancelar". | Excluir faz a mesma pergunta. E parcela que já foi paga não é apagada: fica no histórico. |

### cap11 · Dar baixa (vinheta: BAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap08`); clique na aba "A Pagar"; a câmera vai à linha "Energia elétrica de outubro" (etiqueta "Conta Principal", 10/11/2026, R$ 1.874,30, "Pendente"). | Chegou a hora de pagar. Dar baixa é registrar que a conta foi paga. A energia vence hoje: mil oitocentos e setenta e quatro reais e trinta. |
| Clique em "Marcar pago": janela "Pagar conta", "Energia elétrica de outubro · Restante R$ 1.874,30"; em "Forma de pagamento", o cartão "Pix/Transferência" já marcado (azul), com o valor 1.874,30 e a "Conta bancária" "Conta Principal". | Clico em Marcar pago. A janela já vem com o Pix e a Conta Principal, que estavam no previsto, e com o valor inteiro. |
| A câmera fica nos cartões "Dinheiro" e "Pix/Transferência". | Uma dica: quem não tem permissão pra mexer no banco não vê o Pix aqui. A baixa sai do caixa, e um aviso amarelo explica isso. |
| [ZOOM: o valor 1.874,30 e o resumo "Total informado: R$ 1.874,30" / "Quita a conta"] | Embaixo, a tela confirma que esse valor quita a conta. |
| "Data do pagamento" 10/11/2026; clique em "Confirmar pagamento": aviso "Pagamento registrado"; a linha passa a "Paga", com "Paga em" 10/11/2026. [BACKEND: rpc `pay_financial_bill` (transfer, Conta Principal, R$ 1.874,30, 10/11): `bill_payments`, saída em `bank_transactions` com a categoria "Energia elétrica", `status` paid, `paid_at`] | A data é hoje. Confirmar pagamento. Pronto, a energia está Paga. |
| [ILUSTRAÇÃO: o caminho do dinheiro: a conta "Energia elétrica de outubro", com a etiqueta da categoria, segue por duas trilhas: "Pix" termina na "Conta Principal" com uma seta de saída; "Dinheiro" termina no "caixa aberto"; a etiqueta da categoria viaja até um quadro "DRE" e se encaixa na linha "Energia elétrica"] | Uma dica: dar baixa mexe em dinheiro de verdade. No Pix, o valor sai da conta do banco; em dinheiro, sai do caixa aberto. E o lançamento leva a categoria da conta, por isso aparece certinho na DRE, o relatório do resultado da empresa. |
| (a ilustração: a baixa, a saída do dinheiro e o novo status se acendem juntos, num selo "tudo junto") | E é tudo junto: ou a baixa grava inteira, ou nada muda. |
| De volta à tela: na linha "Manutenção da prensa enfardadeira" (19/11/2026, R$ 3.480,00, "Pendente"), clique em "Marcar pago": "Pagar conta", "Manutenção da prensa enfardadeira · Restante R$ 3.480,00", com o Pix e a "Conta Principal" já marcados. | Agora um pagamento em parte. A Hidráulica Moretti pediu metade na entrega das peças, e o resto no fim do mês. |
| No campo do valor, apaga e digita 1.740,00. [ZOOM: o valor 1.740,00 e "Falta R$ 1.740,00 para quitar"] | No valor, mil setecentos e quarenta reais. A tela mostra quanto falta pra quitar. |
| Aparece "Novo vencimento do restante" com 19/11/2026; no calendário escolhe 30 (30/11/2026); embaixo, "O saldo de R$ 1.740,00 continuará em aberto com este vencimento.". | Como sobrou uma parte, aparece o Novo vencimento do restante. Coloco trinta de novembro. |
| Clique em "Confirmar pagamento": aviso "Pagamento registrado"; a linha fica "Parcial", com R$ 3.480,00 e, embaixo, "pago R$ 1.740,00 de R$ 3.480,00", e o vencimento 30/11/2026. [ZOOM: "Parcial", "pago R$ 1.740,00 de R$ 3.480,00" e 30/11/2026] [BACKEND: rpc `pay_financial_bill` parcial (`remainder_due_date` 30/11): `paid_amount` 1.740,00, `status` partial, `due_date` 30/11] | Confirmar. A conta ficou Parcial: mostra quanto já foi pago e quanto era, e agora vence dia trinta. |
| De volta à lista: busca "água" (aba "A Pagar"); na linha "Água e esgoto de outubro" ("Vencida", R$ 238,40), clique em "Marcar pago": "Pagar conta", "Água e esgoto de outubro · Restante R$ 238,40". | E a conta que atrasou? A água venceu dia cinco e veio com multa. Clico em Marcar pago. |
| Em "Juros / multa (opcional)" digita 4,77: aparece "A conta continua valendo R$ 238,40. Este valor entra como despesa separada." e "Categoria do juros" com "Juros e Multas". [ZOOM: o campo e o aviso] | O valor da conta continua o mesmo. A multa vai no campo Juros / multa: quatro reais e setenta e sete. Ela entra como uma despesa separada, na categoria Juros e Multas. |
| A câmera desce para "Tarifa (opcional)". | Tem também o campo Tarifa, pra quando o banco cobra pelo boleto ou pela transferência. |
| Liga "Múltiplas formas de pagamento": os cartões "Dinheiro" e "Pix/Transferência" passam a aceitar os dois, com "Valor em Dinheiro" e "Valor em Pix/Transferência"; desliga. | E se você paga uma parte em dinheiro e outra por Pix, liga o Múltiplas formas de pagamento e coloca o valor de cada uma. |
| A câmera fica no resumo "Total informado"; clique em "Cancelar". | Uma dica: se pagar a mais numa conta com fornecedor, a sobra vira crédito dele, e a tela avisa antes de confirmar. Aqui eu só cancelo. |

### cap12 · O valor real do mês (vinheta: BAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap11`); na busca digita "aluguel da": a conta de 12/11/2026, R$ 2.300,00, "Pendente". | Nem toda conta que se repete vem sempre igual. Este mês, o aluguel da empilhadeira veio com horas a mais: dois mil quatrocentos e quinze reais, em vez de dois mil e trezentos. |
| Clique em "Marcar pago": "Pagar conta"; no alto, "Valor desta ocorrência" com 2.300,00 e o texto "Altere o valor da conta antes de informar quanto será pago agora. Por padrão, as próximas contas mantêm o valor previsto.". | Clico em Marcar pago na de novembro. Como ela é de uma recorrência, aparece um campo lá em cima: Valor desta ocorrência. |
| Apaga e digita 2.415,00; o valor da forma de pagamento acompanha (2.415,00). [ZOOM: "Valor desta ocorrência" com 2.415,00] | Troco pra dois mil quatrocentos e quinze. O valor do pagamento acompanha sozinho. |
| [ZOOM: o resumo "Previsto: R$ 2.300,00 · Valor desta ocorrência: R$ 2.415,00. As próximas contas mantêm o valor previsto." e "Quita a conta"] | Embaixo, o resumo mostra o previsto e o valor deste mês. E avisa: as próximas contas mantêm o valor previsto. |
| A câmera vai ao interruptor "Atualizar o valor previsto das próximas contas" (desligado). | Se fosse um reajuste do contrato, era só ligar o Atualizar o valor previsto das próximas contas. Aí as próximas, que ainda estão abertas no valor antigo, passam pro valor novo. |
| Clica no cartão "Pix / Transferência (Banco)", escolhe "Conta Secundária" em "Conta bancária"; "Data do pagamento" 10/11/2026; "Confirmar pagamento": aviso "Pagamento registrado". [BACKEND: rpc `pay_recurring_financial_bill` (`p_occurrence_amount` 2415, `p_update_future_amounts` false)] | Aqui foi só este mês, então deixo desligado. Escolho o Pix, a Conta Secundária, e confirmo. |
| A lista: 12/11/2026 "Paga", R$ 2.415,00; 15/12/2026 "Pendente", R$ 2.300,00. [ZOOM: os dois valores] | Pronto. Novembro ficou paga por dois mil quatrocentos e quinze, e dezembro continua com dois mil e trezentos. |
| A câmera fica na lista. | Uma dica: isso é diferente de pagar em parte. Aqui você corrige quanto a conta vale. O pagamento parcial é quando você paga menos do que ela vale. |

Mundo: **cria um Pix de R$ 2.415,00 em 10/11 pela Conta Secundária** (junção 1.60: T14 e T15 contam com ele).

### cap13 · Pagar várias de uma vez (vinheta: BAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap12`), aba "A Pagar"; na busca digita "pneus": as três parcelas. | E quando um Pix só paga várias contas? A Recicla Vale vai adiantar duas parcelas dos pneus de uma vez. |
| Marca a caixinha das parcelas 1 e 2: no rodapé, a barra "2 linhas selecionadas", "Total: R$ 4.720,00", "Limpar" e "Quitar em lote". [ZOOM: a barra] | Marco a caixinha das duas. Embaixo aparece uma barra com duas linhas selecionadas e o total: quatro mil setecentos e vinte reais. |
| Clique em "Quitar em lote": janela "Pagar 2 linhas em 1 lançamento", "Total R$ 4.720,00 — vira um único lançamento, que casa 1-pra-1 na conciliação bancária.". | Clico em Quitar em lote. As duas viram um lançamento só, do jeito que vai aparecer no extrato do banco. |
| Em "Forma de pagamento" escolhe "Pix / Transferência (Banco)" e a "Conta Secundária"; a câmera passa por "Descrição do lançamento" ("Pagamento agrupado: Auto Peças Vale Forte (2 linhas)") e "Data do pagamento" 10/11/2026; "Confirmar pagamento": aviso "Pagamento de R$ 4.720,00 registrado em 1 lançamento (2 conta(s))". [BACKEND: rpc `pay_financial_bills_batch`: duas `bill_payments` com o mesmo `group_id` e uma saída em `bank_transactions`] | Escolho o Pix, a Conta Secundária, confiro a descrição do lançamento e a data, e confirmo. |
| A lista: parcelas 1 e 2 "Paga", a 3 "Pendente". | Pronto: as duas parcelas estão pagas, com um único lançamento no banco. |
| A câmera fica na lista. | Uma dica: junte contas da mesma categoria. Com categorias diferentes, o pagamento entra no relatório sem categoria, e a tela avisa antes. |
| (sem ação) | E dá pra marcar linha de saldo também: o fiado entra no lote, e você ainda escolhe quanto abater de cada um. |

Mundo: **cria um Pix de R$ 4.720,00 em 10/11 pela Conta Secundária** (T14 e T15).

### cap14 · Desfazer uma baixa (vinheta: BAIXA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap13`); na busca digita "pneu da": a linha "Conserto do pneu da empilhadeira", "Paga"; clique em "Mais ações" (três pontinhos) → "Estornar pagamento". | Deu baixa na conta errada? Dá pra desfazer. Na conta paga, clico em Mais ações e em Estornar pagamento. |
| Janela "Estornar pagamento": "Saiu de" Conta Principal e "Voltam R$ 180,00 para Conta Principal". [ZOOM: a frase "Voltam R$ 180,00 para ..."] [TESTAR: texto exato do nome da origem] | A tela mostra de onde o dinheiro saiu e avisa que ele volta pra lá: os cento e oitenta reais voltam pra Conta Principal, e a conta fica pendente de novo. |
| "Cancelar"; clique na lixeira da mesma linha: "Excluir conta?", "Excluir devolve R$ 180,00 para ..." e o botão "Excluir e estornar"; "Cancelar". | Excluir uma conta paga faz o mesmo caminho: o botão vira Excluir e estornar, e o dinheiro volta antes de a conta sumir. |
| A câmera fica na linha. | Uma dica: se o pagamento já foi conciliado com o extrato do banco, desfaça a conciliação primeiro. Aqui eu só cancelo. |

Mundo: nenhum dado muda (o robô cancela).

### cap15 · O fiado na mesma lista (vinheta: FIADO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap09`); clique na aba "A Receber"; na busca digita "Quiririm": a linha "Aços Quiririm Ltda", com "Cliente" embaixo, traços em "Categoria", "Emissão" e "Vencimento", R$ 4.870,00, o chip roxo "Saldo" e o botão "Receber". | Agora, o fiado. Ele aparece na mesma lista, com a etiqueta roxa Saldo. A Aços Quiririm levou ferro e chaparia a prazo: quatro mil oitocentos e setenta reais. |
| [ZOOM: o chip "Saldo" e o valor R$ 4.870,00] | A linha de saldo não tem vencimento nem categoria. É o total que o cliente deve, como o caderninho do balcão. |
| Clique em "Receber": janela "Receber de Aços Quiririm Ltda", "Saldo em aberto R$ 4.870,00"; em "Forma de recebimento" ("Dinheiro (Caixa)") escolhe "Pix / Transferência (Banco)"; em "Conta bancária" escolhe "Conta Principal". | A baixa dele é própria. Clico em Receber. A Aços Quiririm mandou um Pix, então troco pro Pix e escolho a Conta Principal. |
| "Valor" vem com 4.870,00; apaga e digita 2.000,00. [ZOOM: "Valor" com 2.000,00 e "Saldo após esta baixa: R$ 2.870,00"] | Ela pagou dois mil reais. Embaixo, a tela já mostra o saldo depois da baixa: dois mil oitocentos e setenta. |
| "Data do recebimento" 10/11/2026; clique em "Confirmar recebimento": aviso "Recebimento registrado"; a linha passa a R$ 2.870,00. [BACKEND: rpc `pay_partner_balance` (customer, Aços Quiririm Ltda, R$ 2.000,00, transfer, Conta Principal, 10/11): `balances` +2.870,00 e a entrada em `bank_transactions`] | Confirmar recebimento. O saldo da Aços Quiririm caiu pra dois mil oitocentos e setenta. |
| Na busca, troca por "Fundição": as três parcelas da Fundição Bandeira do Vale, R$ 4.790,00, 17/11/2026, 17/12/2026 e 18/01/2027, "Pendente"; nenhuma linha "Saldo". [TESTAR: o saldo da Fundição (+14.370,00) todo coberto pelas três parcelas abertas, sem linha de saldo] | Agora repara na Fundição Bandeira do Vale. Ela comprou trezentos quilos de cobre mel a prazo, em três vezes. E aqui só aparecem as parcelas. |
| [ILUSTRAÇÃO: o fiado parcelado: a venda "300 kg de cobre mel · R$ 14.370,00" gera duas coisas ao mesmo tempo: o saldo da Fundição (R$ 14.370,00) e três parcelas de R$ 4.790,00; uma balança de dois pratos mostra o mesmo dinheiro dos dois lados; a lista fica só com as parcelas e a linha de saldo se apaga, com o rótulo "já está nas parcelas"] | Uma dica: se o saldo de um cliente sumir da lista, olha se a venda foi parcelada. Na venda a prazo em parcelas, o mesmo dinheiro fica no saldo e nas parcelas. Pra não cobrar duas vezes, a lista desconta do saldo o que já virou parcela. |
| (a ilustração: segundo quadro, um saldo de R$ 5.000,00 com só R$ 3.000,00 em parcelas: a linha de saldo mostra os R$ 2.000,00 que sobram) | Se tudo virou parcela, a linha de saldo some. Se só uma parte virou, ela mostra só o que sobra. |
| De volta à tela, nas três parcelas da Fundição; o mouse para no lápis "Editar" de uma delas, sem clicar. | Uma dica: essas parcelas vieram do pedido de venda. Aqui dá pra mudar a descrição, o vencimento e a categoria; o valor e o cliente se mudam no próprio pedido. |

### cap16 · Anexar o comprovante (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap10`), aba "Todas"; na busca digita "energia": a linha "Energia elétrica de outubro", "Paga". | E o comprovante daquele Pix da energia? Ele fica guardado na própria conta. |
| Clique no lápis "Editar": janela "Editar conta"; clique em "Mais detalhes" (a seção abre): "Observações" e "Anexos (foto ou PDF)", com "Nenhum anexo." e o botão "Anexar". | Clico em editar e abro o Mais detalhes. Aqui ficam as observações e os anexos. |
| Clique em "Anexar": o robô entrega o arquivo `comprovante-pix-energia-outubro.pdf`; aparece o aviso "Anexo adicionado" e a miniatura com "PDF". [BACKEND: upload no bucket `financial-attachments` + insert em `transaction_attachments` (ref `financial_bill`) e `createSignedUrls`] | Anexar, e escolho o comprovante. O arquivo sobe na hora, com o aviso Anexo adicionado. Pode ser PDF ou foto, até do celular. |
| Clique em "Salvar": aviso "Conta atualizada". [BACKEND: update em `financial_bills` com os mesmos valores] | Salvar. O comprovante já está na conta. |
| Clique de novo no lápis "Editar" e em "Mais detalhes": a miniatura "PDF"; o mouse para em cima ("Baixar anexo"), sem clicar; depois "Cancelar". | E onde ele aparece depois? Aqui mesmo: é só abrir a conta e o Mais detalhes. Clicando na miniatura, o arquivo abre. |
| A câmera fica na janela. | Uma dica: se o comprovante já estiver com você na hora de dar baixa, anexa ali mesmo, no campo Comprovante. Aí ele fica na conta e também no lançamento do banco ou do caixa. |

### cap17 · Filtrar a lista (vinheta: FILTROS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap11`); clique na aba "A Receber": as parcelas da Fundição e, no fim, as linhas com o chip "Saldo" (Aços Quiririm Ltda, R$ 2.870,00). [TESTAR: as linhas "Saldo" na primeira página da aba "A Receber"] | Com a lista cheia, os filtros ajudam a achar o que você procura. Na aba A Receber, repara nas linhas de saldo, lá no fim. |
| Clique em "Filtros": o painel "Filtros"; a câmera desce por "Status", "Categoria", "Cliente/Fornecedor", "Centro de custo", "Banco previsto" e "Vencimento (período)". | Clico em Filtros. Dá pra filtrar por status, categoria, Cliente/Fornecedor, centro de custo, banco previsto e período de vencimento. |
| Em "Status" marca "Pendente"; clique em "Aplicar": a lista só com as pendentes; o botão "Filtros" fica verde, com o número 1. | No Status, marco Pendente e aplico. A lista mostra só as pendentes, e o botão Filtros avisa que tem um filtro ligado. |
| A câmera vai ao fim da lista: as linhas "Saldo" não estão mais lá. | Uma dica: repara que as linhas de saldo saíram. O saldo não tem status nem vencimento. Então, com filtro de status, período, categoria, centro de custo ou banco, ele fica de fora. |
| A câmera sobe aos cartões: agora somam só as linhas da lista (os valores mudaram). | E os cartões lá em cima mudaram junto: agora somam só as pendentes. |
| "Filtros" → em "Cliente/Fornecedor" busca "Fundição" ("Buscar parceiro...") e escolhe "Fundição Bandeira do Vale"; "Aplicar": as três parcelas da Fundição; "Filtros" com o número 2. | Junto com o status, escolho a Fundição Bandeira do Vale. Pronto: as três parcelas dela. |
| "Filtros" → "Limpar filtros" → "Aplicar": a lista volta inteira, com as linhas "Saldo" no fim. | Pra ver tudo de novo, Limpar filtros. E as linhas de saldo voltam. |
| "Filtros" → em "Vencimento (período)", clique em "Este mês": "De" 01/11/2026 e "Até" 30/11/2026; a câmera passa por "Próximos 7 dias" e "Até o fim do mês"; "Aplicar". | No período de vencimento, tem três atalhos: Este mês, Próximos 7 dias e Até o fim do mês. |
| A câmera sobe aos cartões: "A receber no período" e "Recebido no período". [ZOOM: os dois primeiros cartões] | Com um período ligado, os cartões mudam de nome: A receber no período e Recebido no período. |

### cap18 · Exportar a lista (vinheta: FILTROS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap16`); clique em "Exportar": menu "Exportar contas", com "PDF" e "Excel"; clique em "PDF". | Precisa mandar essa lista pro contador ou imprimir? O botão Exportar gera um PDF ou uma planilha do Excel. |
| Janela "Exportar contas (PDF)", "Escolha o que entra no arquivo. Os filtros já vêm com o que você está usando na tela."; a câmera desce pelo bloco "Filtros". | A janela já vem com os filtros que você está usando na tela, e dá pra mudar ali mesmo. |
| Bloco "Opções do arquivo": "Fiado / saldo de cliente e fornecedor" e "Agrupar por" ("Nenhum", "Status", "Categoria", "Mês"). [ZOOM: o bloco] | Em Opções do arquivo, você escolhe se o saldo dos clientes e fornecedores entra, e como agrupar: por status, por categoria ou por mês. |
| Fecha a janela (Esc). | Aqui eu só fecho. |

### cap19 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: as abas e os quatro cartões (cap01 e cap02) e o calendário de novembro (cap03). | Pronto! Recapitulando: a gente conheceu as abas, os quatro cartões e o calendário. |
| Montagem rápida: a "Nova conta" da manutenção da prensa (cap04), o "Já paguei essa conta" (cap05) e o "Configurar faturamento" dos pneus (cap06). | Lançou a manutenção da prensa, o conserto do pneu já pago e os pneus do caminhão em três vezes. E deixou o sistema preencher a internet do escritório pelo padrão. |
| Montagem rápida: o "Repete?" do aluguel da empilhadeira (cap08) e o "Esta e as próximas" (cap09). | Montou o aluguel da empilhadeira todo mês, até abril, e mudou o vencimento desta e das próximas. E fez o mesmo nas parcelas dos pneus. |
| Montagem rápida: a energia "Paga" e a prensa "Parcial" (cap09). | Deu baixa na energia inteira e em metade da prensa, com o resto pro fim do mês. Pagou o aluguel da empilhadeira pelo valor real do mês e duas parcelas dos pneus num lançamento só. |
| Montagem rápida: "Receber de Aços Quiririm Ltda" e a ilustração do fiado parcelado (cap10). | Recebeu parte do saldo da Aços Quiririm e viu por que o fiado parcelado aparece só nas parcelas. E viu como estornar uma baixa e exportar a lista. |
| Montagem rápida: a miniatura "PDF" (cap11) e o painel "Filtros" (cap12). | E anexou o comprovante e filtrou a lista. |
| Cartão "Próximo: Bancos, cofre e conciliação bancária"; cartela final. | No próximo tutorial, a gente faz o extrato do banco bater com o sistema. Até lá! |
