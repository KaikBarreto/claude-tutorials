# Roteiro T13 · Contas a Pagar e Receber

Roteiro pronto para o ensaio e, depois da revisão geral, para a voz (molde da Domiflix, sem etapa de aprovação). Coluna
Fala = texto da narração (voz Kaik Barreto), na grafia da legenda; o texto exato do TTS, com a grafia de pronúncia, está em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
(`T13/inventario.md`, versão 1.59.154).
Desktop (janela de 1280×800), logado como Rafael Nogueira (MASTER). Todo capítulo parte de um navegador novo na tela
"Contas a Pagar/Receber", com o mundo do fim do capítulo anterior (sementes `t13/inicio` e `t13/apos-capNN`); quando um
capítulo continua uma janela do anterior, o `setup` do robô a reabre fora do vídeo.

- **Título:** Contas a Pagar e Receber
- **Antes:** Estoque: saldo, histórico e posição (T10)
- **Próximo:** Bancos, cofre e conciliação bancária (T14)
- **Vinhetas (áreas):** CONTAS · LANÇAMENTO · RECORRÊNCIA · BAIXA · FIADO · COMPROVANTE · FILTROS · RESUMO (todos os
  capítulos menos o 0)
- **Duração estimada:** ~14,5 min de vídeo (1.951 palavras de fala, ~12,5 min de voz a 2,6 palavras/s, mais a vinheta
  de abertura, 13 vinhetas de capítulo, a cartela e as esperas dos formulários; as 7 ilustrações correm junto da fala;
  alvo da fonte: 16 min)
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
| A câmera sobe ao botão "Nova conta", no canto de cima. | Pra lançar uma conta nova, o botão é este: Nova conta. |

### cap02 · Os quatro cartões do topo (vinheta: CONTAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/inicio`), aba "Todas"; a câmera sobe para os quatro cartões. | Antes da lista, os quatro cartões lá de cima. Eles mostram quanto a empresa deve, quanto tem pra receber e o que está apertando. |
| [ZOOM: os cartões "Total a Pagar" e "Total a Receber", com os valores] | O Total a Pagar soma as contas que a empresa ainda deve, mais o que ela deve no saldo, o fiado. O Total a Receber é o contrário: as contas a receber, mais o que devem pra ela no saldo. |
| [ILUSTRAÇÃO: vencidas e os próximos sete dias: uma régua de novembro com "hoje, 10/11" no meio; à esquerda, a água (05/11) num bloco vermelho "Vencidas"; à direita, uma janela laranja de 10/11 a 17/11 com a energia (10/11) e a primeira parcela da Fundição (17/11), rotulada "Vence em 7 dias"; a janela acende quando a frase fala dela] | Vencidas é o que passou do vencimento e não foi pago, como a água. Vence em 7 dias é o que vence de hoje até daqui a sete dias, como a energia. |
| De volta à tela: [ZOOM: os cartões "Vencidas" e "Vence em 7 dias"] | Esses dois somam só contas, as a pagar e as a receber. O saldo não tem data de vencimento, então fica de fora deles. |
| A câmera abre para os cartões e as abas; clique em "A Pagar": os quatro valores continuam iguais; clique em "Todas". | Uma dica: repara que eu troquei de aba e os números não mudaram. Os cartões mostram sempre a empresa inteira, com ou sem filtro. |

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
| Capítulo novo (semente `t13/inicio`), aba "Todas"; clique em "Nova conta": janela "Nova conta" ("Cadastre uma conta a pagar ou a receber com vencimento."), bloco "O que é". | Agora, lançar uma conta nova. A Hidráulica Moretti vai fazer a manutenção da prensa, com vencimento no dia dezenove. Clico em Nova conta. |
| A câmera mostra o "Tipo" em "A pagar (despesa)". | O Tipo já vem como A pagar. Se fosse dinheiro entrando, seria A receber. |
| Em "Valor" digita 3.480,00. [ZOOM: "Valor" com 3.480,00] | No Valor, três mil quatrocentos e oitenta reais. |
| Em "Descrição" ("Ex: Aluguel do galpão") digita "Manutenção da prensa enfardadeira"; em "Vencimento" abre o calendário e escolhe 19 (19/11/2026). | Na Descrição, o que é a conta: manutenção da prensa enfardadeira. E o Vencimento, dezenove de novembro. |
| Em "Categoria" abre a lista ("Pesquisar categoria..."), digita "Manut" e escolhe "Manutenção de máquinas". | A Categoria diz que tipo de gasto é esse. Aqui, Manutenção de máquinas. |
| Em "Cliente / Fornecedor" o tipo já está em "Fornecedor"; clica em "Selecione o fornecedor", digita "Moretti" e escolhe "Hidráulica Moretti Ltda". [BACKEND: busca de `suppliers` por nome] | Como é conta a pagar, o campo já vem em Fornecedor. É só escolher a Hidráulica Moretti. |
| Em "Centro de custo" ("— Nenhum —") escolhe "Pátio". | O Centro de custo diz qual parte da empresa gastou. A prensa fica no pátio, então, Pátio. |
| No bloco "Dinheiro", em "Pagamento previsto" ("Não definido") escolhe "Conta Principal" (grupo "Contas"). | No Pagamento previsto, eu digo de onde esse dinheiro deve sair: da Conta Principal. É só uma previsão, mas na hora de pagar ela já vem sugerida. |
| Clique em "Criar conta": aviso "Conta criada"; a linha "Manutenção da prensa enfardadeira", com "Hidráulica Moretti Ltda" embaixo, a categoria com a etiqueta "Conta Principal", vencimento 19/11/2026, R$ 3.480,00 e "Pendente". [ZOOM: a linha nova, com 19/11/2026 e R$ 3.480,00] [BACKEND: insert em `financial_bills`; o select do aviso de conta igual (mesmo fornecedor, vencimento e valor) devolve vazio] | Criar conta. Pronto: a manutenção entrou na lista, pendente, com a data, a categoria e o fornecedor. |

### cap05 · A conta que já nasce paga (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap04`); clique em "Nova conta". | E quando a conta chega já paga? Ontem, o conserto do pneu da empilhadeira foi pago na hora, por Pix: cento e oitenta reais. |
| Preenche (o que passar da fala vai acelerado): "Valor" 180,00; "Descrição" "Conserto do pneu da empilhadeira"; "Vencimento" 09/11/2026; "Categoria" "Manutenção de máquinas"; "Centro de custo" "Pátio". | Preencho como qualquer conta: o valor, a descrição, a data de ontem, a categoria e o centro de custo. |
| Em "Pagamento previsto" escolhe "Conta Principal". | No Pagamento previsto, a conta de onde o Pix saiu: a Conta Principal. |
| Liga "Já paguei essa conta" ("Registra o pagamento agora — a conta já nasce quitada."); aparece "Data do pagamento" com 10/11/2026; no calendário escolhe 9 (09/11/2026). | Agora o que muda: ligo o Já paguei essa conta. Ele registra o pagamento junto, e a conta já nasce quitada. Na Data do pagamento, ontem. |
| Clique em "Criar conta": aviso "Conta criada e paga"; na busca ("Buscar por valor, descrição ou parceiro...") digita "pneu": a linha "Conserto do pneu da empilhadeira", "Paga", "Quitada em" 09/11/2026. [BACKEND: insert em `financial_bills` + rpc `pay_financial_bill` (transfer, Conta Principal, R$ 180,00, 09/11)] | Criar conta. Ela já entra como Paga, e o dinheiro já saiu da Conta Principal. Nada fica pendente pra lembrar depois. |
| A câmera fica na linha. | Numa conta a receber, a opção vira Já recebi essa conta. |

### cap06 · Parcelar uma conta (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap05`); clique em "Nova conta". | Agora uma compra dividida em vezes. Os pneus novos do caminhão truck saíram por sete mil e oitenta reais na Auto Peças Vale Forte, em três vezes. |
| Em "Valor" digita 7.080,00. [ZOOM: "Valor" com 7.080,00] | No Valor vai o total da compra, sete mil e oitenta, e não o valor da parcela. |
| Preenche (o que passar da fala vai acelerado): "Descrição" "Pneus do caminhão truck"; "Vencimento" 23/11/2026; "Categoria" "Manutenção de veículos"; fornecedor "Auto Peças Vale Forte". | No Vencimento, a data da primeira parcela: vinte e três de novembro. Categoria e fornecedor, como antes. |
| Clique em "Parcelar ou repetir" (a seção abre); liga "Parcelar": abre "Configurar faturamento" ("Parcelar R$ 7.080,00 do saldo"), com "Condição de pagamento" em "Manual (definir parcelas)". | Embaixo, em Parcelar ou repetir, ligo o Parcelar. |
| Em "Nº de parcelas" clica em "3": as linhas 1 · 23/11/2026 · R$ 2.360,00, 2 · 23/12/2026 · R$ 2.360,00 e 3 · 23/01/2027 · R$ 2.360,00; a faixa verde "Soma das parcelas" R$ 7.080,00. [ZOOM: as três linhas e a faixa "Soma das parcelas"] | Escolho três parcelas. O sistema divide o valor e põe uma por mês, no mesmo dia: dois mil trezentos e sessenta reais cada. A soma fecha com o total, por isso a faixa fica verde. |
| Clique em "Aplicar faturamento": na seção, o resumo "3x — 1º venc. 23/11/2026 — total R$ 7.080,00" e o botão "Editar". | Aplicar faturamento. O resumo mostra as três vezes, a primeira data e o total. |
| Clique em "Criar conta": aviso "3 parcelas criadas"; na busca digita "pneus": as três contas da Auto Peças Vale Forte, 23/11/2026, 23/12/2026 e 23/01/2027, R$ 2.360,00, "Pendente". [BACKEND: rpc `create_installment_bills` (três `financial_bills`, `installment_number` 1 a 3; descrição como a RPC real grava)] | Criar conta. Pronto, três parcelas criadas. |
| [ILUSTRAÇÃO: uma compra, três contas: o cartão "Pneus do caminhão truck · R$ 7.080,00" se divide em três cartões "R$ 2.360,00" (23/11, 23/12, 23/01), cada um com o selo "Pendente"; um deles ganha um "pago" e os outros seguem iguais] | Cada parcela vira uma conta separada. Dá pra pagar uma sem mexer nas outras. |
| (a ilustração: ao lado, dois quadros: "Parcelar: dívida com fim, como os pneus em 3x" e "Repetir: o gasto que volta todo mês, como um aluguel") | Parcelar é pra dívida com fim, como esses pneus. Pro gasto que volta todo mês, é o Repetir, que vem agora. |

### cap07 · A conta que se repete (vinheta: RECORRÊNCIA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap06`); clique em "Nova conta". | A empilhadeira da Recicla Vale é alugada: dois mil e trezentos reais todo dia doze, num contrato até abril. |
| Preenche (o que passar da fala vai acelerado): "Valor" 2.300,00; "Descrição" "Aluguel da empilhadeira"; "Vencimento" 12/11/2026; "Categoria" "Aluguel". [ZOOM: "Valor" com 2.300,00] | Valor, descrição e categoria, como sempre. O Vencimento é o da primeira: doze de novembro. |
| Clique em "Parcelar ou repetir"; liga "Repete?" ("Gera contas automaticamente na frequência escolhida."): aparecem "Frequência" ("Mensal"), "A cada" (1) e "Repetir até (opcional)". | Em Parcelar ou repetir, agora eu ligo o Repete. Ele gera as contas sozinho, na frequência que você escolher. |
| Abre "Frequência": "Semanal", "Mensal" e "Anual"; deixa "Mensal"; "A cada" fica 1. | Pode ser semanal, mensal ou anual. Aqui é mensal, a cada um mês. |
| Em "Repetir até (opcional)", no calendário, avança até abril de 2027 e escolhe 12 (12/04/2027); a câmera passa por "Deixe vazio para repetir sem data-fim.". | E no Repetir até, a data de parar: doze de abril, o fim do contrato. Sem data, ele repete sem fim. |
| Clique em "Criar conta": aviso "Conta recorrente criada"; na busca digita "aluguel da" (pega só o aluguel da empilhadeira, e não o conserto do pneu): três contas "Aluguel da empilhadeira", 12/11/2026, 12/12/2026 e 12/01/2027, R$ 2.300,00. [BACKEND: rpc `create_recurring_bill_template`: molde mensal (12/11/2026 a 12/04/2027) + as contas da janela de três meses a partir de 10/11: 12/11, 12/12 e 12/01] | Criar conta. Repara: já entraram as contas de novembro, dezembro e janeiro. |
| [ILUSTRAÇÃO: o molde e a janela de três meses: no alto, o cartão-molde "Aluguel da empilhadeira · R$ 2.300,00 · todo dia 12 · até 12/04/2027"; embaixo, uma régua de novembro a abril com uma moldura verde "próximos 3 meses" sobre 12/11, 12/12 e 12/01, já como contas; a régua anda um mês e a conta de 12/02 aparece; em abril, uma bandeirinha "Repetir até", e nada depois] | O sistema guarda um molde da conta e mantém sempre os próximos três meses na lista. Conforme o tempo passa, ele cria a seguinte sozinho, até a data de parar. |

### cap08 · Só esta ou esta e as futuras (vinheta: RECORRÊNCIA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap07`); na busca digita "aluguel da": as três contas "Aluguel da empilhadeira" (12/11, 12/12 e 12/01). | E se uma delas mudar? A locadora pediu pra passar o vencimento pro dia quinze, a partir de dezembro. |
| Na linha de 12/12/2026, clique no lápis "Editar": janela "Editar conta recorrente", ""Aluguel da empilhadeira" faz parte de uma recorrência. O que deseja editar?", com "Só esta conta", "Esta e as futuras" e "Cancelar". | Clico em editar na de dezembro. Como ela faz parte de uma recorrência, o sistema pergunta antes: só esta conta, ou esta e as futuras? |
| [ILUSTRAÇÃO: só esta e esta e as futuras: a régua com as contas de novembro, dezembro e janeiro e o molde em cima; "Só esta conta" acende só dezembro; "Esta e as futuras" acende dezembro, janeiro e o molde; novembro, que ficou pra trás, não muda] | Só esta conta mexe só na de dezembro. Esta e as futuras muda esta, as próximas que ainda não foram pagas e o molde, pras novas já nascerem certas. |
| Clique em "Esta e as futuras": janela "Editar conta"; em "Vencimento", no calendário, troca 12/12/2026 por 15 (15/12/2026); embaixo aparece "Esta data e as futuras serão deslocadas pelo mesmo período.". | Escolho Esta e as futuras e mudo o vencimento pra quinze de dezembro. Repara no aviso: as próximas andam o mesmo tanto. |
| Clique em "Salvar": aviso "Conta atualizada"; a lista: 12/11/2026, 15/12/2026 e 15/01/2027. [BACKEND: update em `recurring_bill_templates` e nas `financial_bills` futuras não pagas; rpc `shift_recurring_bills_due_date` (de 12/12 para 15/12: +3 dias)] | Salvar. Novembro ficou no dia doze, e dezembro e janeiro foram pro dia quinze. |
| Na linha de 15/01/2027, clique na lixeira "Excluir": janela "Excluir conta recorrente", ""Aluguel da empilhadeira" faz parte de uma recorrência. O que deseja excluir?", "Só esta conta" e "Esta e as futuras" (vermelho); clique em "Cancelar". | Excluir faz a mesma pergunta. Esta e as futuras encerra a recorrência daqui pra frente, e as contas já pagas ficam no histórico. Aqui eu só cancelo. |

### cap09 · Dar baixa (vinheta: BAIXA)

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

### cap10 · O fiado na mesma lista (vinheta: FIADO)

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

### cap11 · Anexar o comprovante (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap10`), aba "Todas"; na busca digita "energia": a linha "Energia elétrica de outubro", "Paga". | E o comprovante daquele Pix da energia? Ele fica guardado na própria conta. |
| Clique no lápis "Editar": janela "Editar conta"; clique em "Mais detalhes" (a seção abre): "Observações" e "Anexos (foto ou PDF)", com "Nenhum anexo." e o botão "Anexar". | Clico em editar e abro o Mais detalhes. Aqui ficam as observações e os anexos. |
| Clique em "Anexar": o robô entrega o arquivo `comprovante-pix-energia-outubro.pdf`; aparece a miniatura com "PDF". [BACKEND: upload no bucket `financial-attachments` + insert em `transaction_attachments` (ref `financial_bill`) e `createSignedUrls`] | Anexar, e escolho o comprovante. Pode ser PDF ou foto, até do celular. |
| Clique em "Salvar": aviso "Conta atualizada". [BACKEND: update em `financial_bills` com os mesmos valores] | Salvar. O comprovante já está na conta. |
| Clique de novo no lápis "Editar" e em "Mais detalhes": a miniatura "PDF"; o mouse para em cima ("Baixar anexo"), sem clicar; depois "Cancelar". | E onde ele aparece depois? Aqui mesmo: é só abrir a conta e o Mais detalhes. Clicando na miniatura, o arquivo abre. |
| A câmera fica na janela. | Uma dica: se o comprovante já estiver com você na hora de dar baixa, anexa ali mesmo, no campo Comprovante. Aí ele fica na conta e também no lançamento do banco ou do caixa. |

### cap12 · Filtrar a lista (vinheta: FILTROS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t13/apos-cap11`); clique na aba "A Receber": as parcelas da Fundição e, no fim, as linhas com o chip "Saldo" (Aços Quiririm Ltda, R$ 2.870,00). [TESTAR: as linhas "Saldo" na primeira página da aba "A Receber"] | Com a lista cheia, os filtros ajudam a achar o que você procura. Na aba A Receber, repara nas linhas de saldo, lá no fim. |
| Clique em "Filtros": o painel "Filtros"; a câmera desce por "Status", "Categoria", "Cliente/Fornecedor", "Centro de custo", "Banco previsto" e "Vencimento (período)". | Clico em Filtros. Dá pra filtrar por status, categoria, Cliente/Fornecedor, centro de custo, banco previsto e período de vencimento. |
| Em "Status" marca "Pendente"; clique em "Aplicar": a lista só com as pendentes; o botão "Filtros" fica verde, com o número 1. | No Status, marco Pendente e aplico. A lista mostra só as pendentes, e o botão Filtros avisa que tem um filtro ligado. |
| A câmera vai ao fim da lista: as linhas "Saldo" não estão mais lá. | Uma dica: repara que as linhas de saldo saíram. O saldo não tem status nem vencimento. Então, com filtro de status, período, categoria, centro de custo ou banco, ele fica de fora. |
| A câmera sobe aos quatro cartões: os mesmos valores de antes. | E os cartões lá em cima continuam iguais, como a gente viu. |
| "Filtros" → em "Cliente/Fornecedor" busca "Fundição" ("Buscar parceiro...") e escolhe "Fundição Bandeira do Vale"; "Aplicar": as três parcelas da Fundição; "Filtros" com o número 2. | Junto com o status, escolho a Fundição Bandeira do Vale. Pronto: as três parcelas dela. |
| "Filtros" → "Limpar filtros" → "Aplicar": a lista volta inteira, com as linhas "Saldo" no fim. | Pra ver tudo de novo, Limpar filtros. E as linhas de saldo voltam. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: as abas e os quatro cartões (cap01 e cap02) e o calendário de novembro (cap03). | Pronto! Recapitulando: a gente conheceu as abas, os quatro cartões e o calendário. |
| Montagem rápida: a "Nova conta" da manutenção da prensa (cap04), o "Já paguei essa conta" (cap05) e o "Configurar faturamento" dos pneus (cap06). | Lançou a manutenção da prensa, o conserto do pneu já pago e os pneus do caminhão em três vezes. |
| Montagem rápida: o "Repete?" do aluguel da empilhadeira (cap07) e o "Esta e as futuras" (cap08). | Montou o aluguel da empilhadeira todo mês, até abril, e mudou o vencimento desta e das futuras. |
| Montagem rápida: a energia "Paga" e a prensa "Parcial" (cap09). | Deu baixa na energia inteira e em metade da prensa, com o resto pro fim do mês. |
| Montagem rápida: "Receber de Aços Quiririm Ltda" e a ilustração do fiado parcelado (cap10). | Recebeu parte do saldo da Aços Quiririm e viu por que o fiado parcelado aparece só nas parcelas. |
| Montagem rápida: a miniatura "PDF" (cap11) e o painel "Filtros" (cap12). | E anexou o comprovante e filtrou a lista. |
| Cartão "Próximo: Bancos, cofre e conciliação bancária"; cartela final. | No próximo tutorial, a gente faz o extrato do banco bater com o sistema. Até lá! |
