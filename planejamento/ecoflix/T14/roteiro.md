# Roteiro T14 · Bancos, cofre e conciliação bancária

Roteiro pronto para o ensaio sem voz e, depois da revisão geral, para gerar a voz (voz Kaik Barreto, ElevenLabs). Coluna
Fala = texto da narração na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py` (uma linha
por linha da tabela). Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da
1.60.18 (`T14/inventario.md`). Tudo fictício no backend falso: nenhum banco, conta ou extrato real; contas sem
instituição (ícone genérico, sem logo de banco).

- **Título:** Bancos, cofre e conciliação bancária
- **Antes:** Contas a Pagar e Receber (T13)
- **Próximo:** Relatório Financeiro e DRE (T15)
- **Vinhetas (áreas):** BANCOS · COFRE · MOVIMENTAÇÕES · CONCILIAÇÃO · FECHAMENTO · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~24 min de vídeo (3.209 palavras de fala, ~20,6 min de voz a 2,6 palavras/s; 18 vinhetas de capítulo, as ilustrações e as esperas aceleradas; antes do 1.60.18: 2.211 palavras)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` em todos os capítulos. Logado: Rafael Nogueira (admin MASTER). Desktop
  1600×900. Cada capítulo abre um navegador novo na semente indicada (`plano.md`, "Gravação"); o `setup` reabre fora do
  vídeo a tela onde o capítulo começa.
- **Estado inicial:** `plano.md`, "Mundo": cofre R$ 18.500,00 e nenhum caixa aberto; "Conta Principal" (principal,
  R$ 39.593,47), "Conta Secundária" (R$ 83.380,00), "Poupança antiga" (zerada); os Pix de novembro e os do T13 na Conta
  Principal; a conta "Água e esgoto de outubro" (R$ 238,40) em aberto; nenhum extrato importado.
- **Criado ao vivo:** a "Conta Cooperativa" (R$ 5.000,00); a "Poupança antiga" arquivada; o ajuste do cofre (+R$ 60,00);
  o combustível (R$ 350,00), a transferência (R$ 8.000,00) e o saque (R$ 2.000,00 + tarifa R$ 6,50); o "Cartão Empresa" e a despesa de R$ 180,00 (variante `cartao`, que não segue); as três despesas de teste excluídas em lote (variante `lote`, que não segue); a importação do
  `Extrato_20261101_20261110.ofx` e a conciliação finalizada (17 linhas: 13 casadas, 1 baixada, 1 criada, 2 ignoradas).
- **Marcas na Tela:** `[BACKEND: ...]` (falta no backend falso), `[ZOOM: ...]` (dura a frase inteira, nunca um zoom dentro
  de outro), `[ILUSTRAÇÃO: ...]` (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`), `[TESTAR ...]`. "(nº)" = o
  número do pedido na semente (a fala nunca diz número de pedido).
- Nenhum erro encenado: os ⚠️ da fonte entram como "Uma dica:"; os que o código mudou estão no `plano.md` ("Riscos").

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Bancos, cofre e conciliação bancária". | (sem fala) |
| [ILUSTRAÇÃO: banco × sistema que não batem: à esquerda um extrato de banco genérico (sem marca) com "Saldo R$ 44.933,47"; à direita o painel do sistema com "R$ 46.382,57"; entre os dois um ponto de interrogação âmbar que pulsa em "diferença"; a cena abre em "extrato" e "sistema"] | Oi! Neste tutorial a gente vai fazer o extrato do banco bater com o sistema da Recicla Vale Metais, linha por linha, até a diferença zerar. |
| (a ilustração: o ponto de interrogação cresce em "ninguém sabe"; depois os dois números se ligam por um traço verde e viram "R$ 0,00" em "resolve") | Sabe quando o banco mostra um saldo, o sistema mostra outro, e ninguém sabe de onde vem a diferença? É isso que a gente resolve aqui. |
| Dashboard do EcoSistema, logado como Rafael Nogueira; a câmera fica no menu lateral. [BACKEND: semente `t14/inicio`] | No caminho, a gente cadastra uma conta nova e o cartão de crédito da empresa, acerta o cofre, corrige lançamentos errados e registra o dinheiro que só muda de lugar. |
| Cartão discreto: "Antes: Contas a Pagar e Receber". | Se você ainda não viu o tutorial Contas a Pagar e Receber, dá uma olhada antes. [pause] Vamos começar pela tela. |

### cap01 · A tela e as contas (vinheta: BANCOS)

| Tela | Fala |
| --- | --- |
| No menu lateral, clique em "Financeiro" e em "Movimentações Financeiras": a tela abre com o título "Movimentações Financeiras" e a "Conta Principal" selecionada. | Tudo começa em Financeiro, Movimentações Financeiras. Com o cofre ligado, a tela tem esse nome. Sem o cofre, ela aparece como Movimentações Bancárias. |
| A câmera desce pela lista lateral: "Resumo", "DINHEIRO (COFRE)", "Conta Principal", "Conta Secundária", "Poupança antiga", cada uma com o saldo embaixo do nome, e os botões pontilhados "Nova Conta" e "Novo Cartão". | Aqui do lado ficam as contas da empresa, com o saldo embaixo de cada nome. Primeiro vem o cofre, depois a conta principal e as outras. |
| A câmera vai ao cartão azul da "Conta Principal" (nome, saldo, o olho) e aos botões "Saque", "Sangria", "Nova Movimentação" e "Extrato", sem clicar. | Clicando numa conta, abre o cartão dela, com o saldo e os botões do dia a dia: Saque, Sangria, Nova Movimentação e Extrato. |
| Desce até "Histórico de Movimentações"; a câmera passa pelo botão "Selecionar lançamentos" (ícone de lista marcada, à esquerda do período), pelo período "Este mês" e pela busca "Buscar por descrição ou valor...". | Embaixo, o histórico do mês. Dá pra trocar o período, buscar por descrição ou valor e, no Selecionar lançamentos, mexer em vários de uma vez. A gente usa ele daqui a pouco. |
| Clique numa linha de Pix de compra: ela abre para baixo com os itens do pedido e a forma de pagamento; clique de novo e fecha. A câmera passa pelo olho do cartão azul. | Linha que veio de pedido abre e mostra os itens. E o olho, aqui em cima, esconde os valores quando tem gente por perto. |
| Clique em "Extrato": janela "Exportar Extrato Bancário", com "Formato" ("PDF" e "Excel") e "Período" em "Este mês"; abre a lista do período ("Mês passado", "Personalizado"); fecha a janela (Esc) sem gerar. [ZOOM: "Formato" e "Período"] | O Extrato gera o movimento da conta em pê-dê-éfe ou em Excel, no período que você escolher. É o arquivo pra mandar pro contador ou guardar no fechamento. |
| A câmera volta à lista lateral das contas. | Um detalhe: em Usuários e Permissões, o administrador pode liberar só algumas contas pra uma pessoa. Quem tem essa restrição só enxerga aqui as contas liberadas. O cofre e os cartões não mudam. |
| Clique em "Resumo": "Resumo financeiro", "Dinheiro e contas bancárias", o total, "Dinheiro", "Contas bancárias" e "Distribuição do saldo". | No Resumo, você vê o total da empresa: o dinheiro do cofre somado com o das contas do banco. |
| A câmera sobe às abas "Movimentações Financeiras" e "Conciliação", sem clicar. | E lá em cima ficam duas abas. Nesta, você cuida das contas. Na Conciliação, confere o extrato do banco. Vamos começar pelas contas. |

### cap02 · Cadastrar e arquivar contas (vinheta: BANCOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em "Movimentações Financeiras" › "Conta Principal". Clique em "Nova Conta": janela "Nova Conta Bancária" ("Adicione uma nova conta para controlar suas movimentações"). | A Recicla Vale abriu uma conta numa cooperativa de crédito. Pra ela entrar aqui, é Nova Conta. |
| Em "Nome da conta *" digita "Conta Cooperativa"; a câmera passa pelo campo "Instituição" ("Selecione a instituição..."), sem abrir. | O nome é do jeito que a empresa chama a conta: Conta Cooperativa. A instituição é opcional. |
| Em "Valor em conta (R$)" digita 5.000,00 (fica "R$ 5.000,00"); aparece "Data desse saldo" com 10/11/2026. [ZOOM: "Valor em conta (R$)" com R$ 5.000,00 e "Data desse saldo"] | Em Valor em conta, o saldo que ela tem hoje no banco: cinco mil reais. A data desse saldo fica em hoje. |
| Em "Cor identificadora" clica na cor verde-azulada (#14B8A6); a "Pré-visualização" muda de cor. | Escolho uma cor pra reconhecer a conta de longe. |
| Clique em "Criar Conta": aviso "Conta criada com sucesso"; a "Conta Cooperativa" entra na lista, logo abaixo da "Conta Principal". Clique nela: o cartão com R$ 5.000,00 e, no histórico, a linha "Ajuste de saldo - Saldo inicial" com a etiqueta preta "Ajuste". [ZOOM: a linha do ajuste, com a etiqueta e o valor] [BACKEND: insert em `bank_accounts` e em `bank_transactions` ("Ajuste de saldo - Saldo inicial", `excluded_from_dre` true, `transaction_at` 10/11) e `update_bank_balance`; `get_financial_movements` devolve a linha] | Criar Conta. Repara no histórico: o saldo entrou como Ajuste de saldo, Saldo inicial. Ele acerta o saldo da conta, mas não conta como receita nem como despesa. |
| Nos três pontinhos da "Conta Cooperativa", clique em "Editar": janela "Editar Conta Bancária"; a câmera vai à frase embaixo de "Valor em conta (R$)"; depois clique em "Cancelar". [ZOOM: "Alterar este valor gerará um ajuste automático no saldo (sem impacto no DRE)."] | Uma dica: se o saldo ficar torto, edite a conta e corrija o Valor em conta. A diferença entra como Correção manual, também fora da DRE. Assim o resultado do mês fica limpo, sem receita inventada. |
| Nos três pontinhos da "Conta Cooperativa": o menu "Tornar principal", "Editar" e "Excluir"; o cursor para em "Tornar principal", sem clicar; fecha o menu (Esc). | Nesse menu também fica o Tornar principal. A principal é a conta que já vem escolhida nos pedidos e nos pagamentos. Aqui, ela continua sendo a Conta Principal. |
| Nos três pontinhos da "Poupança antiga", clique em "Excluir": janela "Remover conta bancária", "Como deseja proceder com a conta Poupança antiga?", com as opções "Arquivar" ("Oculta a conta mantendo todo o histórico") e "Migrar e Excluir" ("Transfere transações para outra conta e exclui permanentemente"). [ZOOM: as duas opções] | Agora a poupança antiga, que ninguém usa mais. No Excluir, o sistema pergunta como fazer: Arquivar ou Migrar e Excluir. |
| Clique na opção "Arquivar": a janela vira "Arquivar conta". [ZOOM: "A conta será ocultada das listagens mas todo o histórico de transações será preservado."] | Uma dica: arquivar não tem volta. A conta sai das listas e o histórico fica guardado. Já o Migrar e Excluir passa os lançamentos pra outra conta e apaga esta de vez. Na dúvida, arquive. |
| Clique no botão "Arquivar": aviso "Conta arquivada com sucesso"; a "Poupança antiga" sai da lista. [BACKEND: update `bank_accounts.is_archived` true; vira `apos-cap02`] | Arquivar. Pronto, a lista ficou só com as contas que a empresa usa. |

### cap03 · O cartão de crédito da empresa (vinheta: BANCOS)

Variante `cartao` (semente `apos-cap02`; o cartão criado NÃO segue adiante: o cap04 abre em `apos-cap02` sem ele, e a T15 não vê o cartão).

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `cartao`), "Movimentações Financeiras". Clique em "Novo Cartão" (botão pontilhado da lista lateral): janela "Novo Cartão de Crédito" ("Cadastre o cartão para lançar despesas e acompanhar as faturas"). | Além das contas, dá pra cadastrar o cartão de crédito da empresa. É no Novo Cartão. |
| "Nome do cartão *" digita "Cartão Empresa"; "Dia do fechamento *" 25; "Dia do vencimento *" 5; aparece "A fatura que fecha no dia 25 vence no dia 5 do mês seguinte. Compras feitas no dia do fechamento já entram na próxima fatura." [ZOOM: os dois dias e a frase] | O nome, o dia em que a fatura fecha e o dia em que ela vence: fecha no dia vinte e cinco e vence no dia cinco. O sistema já explica em qual fatura cada compra cai. |
| "Limite do cartão" 10.000,00; clique em "Criar Cartão": o cartão entra na lista lateral. [BACKEND: insert em `bank_accounts` com `kind` card, `closing_day` 25, `due_day` 5, `credit_limit` 10.000,00] | O limite é opcional: com ele, o sistema mostra quanto ainda dá pra gastar. Criar Cartão. |
| Clique em "Cartão Empresa": o cartão com "Fatura em aberto" R$ 0,00, "Limite total:" e "Disponível:" R$ 10.000,00, "fecha dia 25 · vence dia 5" e os botões "Nova despesa" e "Extrato". | Ele fica separado das contas, com a fatura em aberto e o limite disponível. |
| Clique em "Nova despesa": janela "Nova Despesa"; em "Descrição" digita "Con": aparece "Padrão encontrado: Conserto do pneu da empilhadeira", a linha com categoria, centro de custo, conta e forma, "Usado 1 vez" e o botão "Preencher". [ZOOM: o padrão e o "Preencher"] [BACKEND: `get_financial_description_suggestions` (`p_context` movement, `p_direction` payable) devolve o conserto do pneu da T13] | Compra no cartão é Nova despesa. E repara: comecei a digitar e o sistema lembrou de um lançamento parecido, com a categoria e o centro de custo. |
| Clique em "Preencher": a categoria e o centro de custo entram; "Pagou com" continua em "Cartão Empresa"; embaixo, "Campos preenchidos. Desfazer preenchimento". [ZOOM: "Pagou com" e a frase] | Preencher. Ele completa o que estava vazio e respeita o que eu já escolhi: o pagamento continua no cartão. Quando o campo está livre, ele sugere também a conta e a forma de pagamento mais usadas. |
| "Valor" 180,00; clique em "Confirmar Despesa": o painel "Faturas" mostra a fatura do mês com o selo "Aberta" e R$ 180,00; "Disponível:" R$ 9.820,00. [BACKEND: `compute_card_bill_month`, `upsert_credit_card_bill` e a compra em `bank_transactions` do cartão] | Cento e oitenta reais, Confirmar Despesa. A compra não sai de conta nenhuma agora: ela entra na fatura. |
| Na fatura, clique em "Pagar Fatura": janela "Pagar Fatura", com "Data do pagamento *", "Origem do pagamento" e "Este pagamento quita a fatura."; clique em "Cancelar". [ZOOM: "Origem do pagamento" e a frase] | Na hora de pagar, é Pagar Fatura: você escolhe de qual conta sai o dinheiro. Pode pagar tudo ou uma parte, e se errar, o pagamento tem o Estornar. Aqui eu só mostrei. |
| A câmera fica na fatura "Aberta". | Uma dica: pagar a fatura não cria despesa nova. As compras já são as despesas; o pagamento só tira o dinheiro da conta e quita a fatura. |

### cap04 · O cofre e o ajuste de saldo (vinheta: COFRE)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: cofre × banco: à esquerda um cofre com notas, rotulado "DINHEIRO (COFRE)", e dentro dele duas partes, "Disponível no cofre" e "Caixa de Marcos Antunes" (o caixa aberto, tracejado); à direita duas contas de banco genéricas, "Conta Principal" e "Conta Secundária"; embaixo, uma barra "Total da empresa" que soma os dois lados; cada lado acende na sua frase: "dinheiro vivo", "banco", "total"] | Agora o cofre. Ele é todo o dinheiro vivo da empresa: o que está guardado e o que está nos caixas abertos. O banco é o dinheiro nas contas. Os dois juntos dão o total da empresa. |
| Capítulo novo (semente `apos-cap02`). Clique em "DINHEIRO (COFRE)": o cartão "O cofre da empresa", R$ 18.500,00, "Saldo Total em Dinheiro", a barra toda verde ("Disponível no cofre") e os botões "Nova movimentação", "Novo depósito" e "Extrato". [ZOOM: R$ 18.500,00 e "Saldo Total em Dinheiro"] [BACKEND: `get_dinheiro_balance` com `saldo_total` 18.500,00 e `caixas_abertos` vazio] | Este é o cofre da Recicla Vale: dezoito mil e quinhentos reais. Ainda não tem caixa aberto hoje, então está tudo no cofre. |
| A câmera fica no cartão do cofre. | Hoje cedo, o Rafael contou o cofre e deu dezoito mil quinhentos e sessenta. Sessenta reais a mais do que o sistema mostra. |
| Nos três pontinhos de "DINHEIRO (COFRE)", o único item "Ajustar saldo"; clique: janela "Ajustar saldo da Conta DINHEIRO", com "Saldo atual" R$ 18.500,00. | Pra acertar, é nos três pontinhos do cofre: Ajustar saldo. É a única opção dele, porque o cofre não se edita nem se arquiva. |
| Em "Novo saldo" digita 18.560,00: "Diferença" mostra +R$ 60,00 em verde. [ZOOM: "Novo saldo" e "Diferença" +R$ 60,00] | Em Novo saldo, o valor contado. A Diferença aparece na hora: mais sessenta reais, em verde. |
| Em "Motivo *" digita "Contagem do cofre"; clique em "Confirmar ajuste": aviso "Saldo ajustado" ("+R$ 60,00 registrado no histórico"); o cartão passa a R$ 18.560,00. [BACKEND: insert em `cash_transactions` (`type` adjustment, `amount` 60,00, `excluded_from_dre` true); `get_dinheiro_balance` passa a 18.560,00] | O motivo é obrigatório: contagem do cofre. Confirmar ajuste. |
| Desce ao histórico do cofre: a linha do ajuste, +R$ 60,00, com a etiqueta preta "Ajuste" na coluna do tipo. [BACKEND: `get_financial_movements` do cofre devolve o ajuste de `cash_transactions`; vira `apos-cap03`] | O ajuste fica no histórico com a etiqueta Ajuste. É acerto de contagem: não entra como receita nem como despesa. |

### cap05 · Movimentação, transferência e saque (vinheta: MOVIMENTAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`). Clique em "Conta Principal": o cartão azul com os botões. | Hoje cedo, o Rafael também fez três coisas no banco: pagou o combustível da picape por Pix, trouxe dinheiro da Conta Secundária e sacou no caixa eletrônico. Cada uma tem o seu jeito de registrar. |
| Clique em "Nova Movimentação": janela "Nova Movimentação Financeira"; em "Tipo" clica "Saída" (vermelho); "Conta bancária" já em "Conta Principal". | O combustível é gasto de verdade. Nova Movimentação, tipo Saída, na Conta Principal. |
| Preenche (trecho acelerado nas digitações): "Descrição" "Combustível da picape"; "Valor *" 350,00; "Categoria *" "Combustível"; "Centro de custo" "Frota". [ZOOM: "Valor *" com R$ 350,00] | Descrição, combustível da picape. Valor, trezentos e cinquenta reais. Categoria Combustível e centro de custo Frota. |
| A câmera passa pela caixa "Não contar na DRE (saldo herdado / histórico)", desmarcada; clique em "Salvar": aviso "Movimentação registrada com sucesso!". [BACKEND: `create_manual_bank_transaction` (withdrawal, −350,00, categoria Combustível, centro Frota)] | Essa opção de não contar na DRE é pra saldo herdado de outro sistema. Combustível é despesa, então ela fica desmarcada. Salvar. |
| Clique em "Nova Movimentação"; a câmera passa por "Entrada" (verde), "Data/hora do lançamento" e "Vincular a fornecedor/cliente (opcional)"; segue para "Transferência" (a janela só é fechada na transferência da linha seguinte). | A Entrada funciona do mesmo jeito, pra dinheiro que chegou sem pedido, como um rendimento. Dá pra acertar a data e a hora do lançamento e, se quiser, vincular a um cliente ou fornecedor. |
| [ILUSTRAÇÃO: dinheiro mudando de lugar: três potes lado a lado, "Conta Secundária", "Conta Principal" e "DINHEIRO (COFRE)", e em cima o placar "Total da empresa"; oito mil passam da Conta Secundária para a Conta Principal em "transferência"; dois mil passam da Conta Principal para o cofre em "saque"; o placar não muda em "nem mais pobre"; só uma moeda de R$ 6,50 sai do desenho com a etiqueta "despesa"] | Uma dica: transferência entre contas suas, saque e depósito só mudam o dinheiro de lugar. A empresa não fica mais rica nem mais pobre, então nada disso entra na DRE. |
| Clique em "Nova Movimentação" e em "Transferência" (laranja): "Conta de origem" vem com "Conta Principal"; troca para "Conta Secundária"; em "Conta de destino" escolhe "Conta Principal"; "Valor *" 8.000,00; aparece "Prévia da transferência:" com a saída em vermelho e a entrada em verde. [ZOOM: "Prévia da transferência:" com R$ 8.000,00] | Por isso a transferência tem tipo próprio. De onde saiu, a Conta Secundária. Pra onde foi, a Conta Principal. Oito mil reais, e a prévia mostra a saída e a entrada. |
| Clique em "Transferir": aviso "Transferência realizada com sucesso!". [BACKEND: `create_manual_bank_transaction` ×2 com o mesmo `group_id` (−8.000,00 na Secundária, +8.000,00 na Principal, `excluded_from_dre` true, descrição "Transferência: Conta Secundária → Conta Principal")] | Transferir. Repara que nem pediu categoria: é dinheiro da empresa trocando de conta. |
| Clique em "Saque": janela "Saque / Sangria" com "Saque" marcado ("Transferir dinheiro do banco para o cofre ou para um caixa aberto"); "Conta de origem" "Conta Principal"; "Destino do saque" já em "Cofre (Conta DINHEIRO)". | Agora o saque, que vai da Conta Principal pro cofre. |
| "Valor do Saque" 2.000,00; em "Tem tarifa no saque?" escolhe "Sim"; "Valor da Tarifa" 6,50. [ZOOM: "Valor do Saque" e "Valor da Tarifa" R$ 6,50] | Dois mil reais. O banco cobrou tarifa? Sim, seis reais e cinquenta. |
| A câmera vai a "Efeitos desta transação:": "Saldo da Conta Bancária", "Diminuirá em R$ 2006,50" ("(Saque: R$ 2.000,00 + Tarifa: R$ 6,50)"), e "Cofre (Conta DINHEIRO)", "Aumentará em R$ 2.000,00". [ZOOM: os dois cartões dos efeitos] | Antes de confirmar, os efeitos: o banco perde o saque mais a tarifa, e o cofre ganha só o saque. A tarifa, essa sim, vira uma despesa separada. |
| Clique em "Confirmar Saque": aviso "Saque realizado com sucesso!"; de volta ao cartão, a câmera passa pelo botão "Sangria". [BACKEND: insert duplo em `bank_transactions` ("↑ SAQUE · Conta Principal → Cofre (DINHEIRO)" −2.000,00 e "↓ SAQUE · Conta Principal → Cofre" +2.000,00 no cofre, `excluded_from_dre` true), `update_bank_account_balance` ×2 e a tarifa "Tarifa de Saque para o Cofre" −6,50 (`create_manual_bank_transaction`, type expense); cofre R$ 20.560,00] | Confirmar Saque. O caminho contrário, levar dinheiro do cofre pro banco, é a Sangria, aqui do lado. Também só muda o dinheiro de lugar. |
| A câmera para no botão "Saque". [vira `apos-cap04`] | Uma dica: sem o cofre ligado, o saque só vai pra um caixa aberto, então o caixa precisa estar aberto antes. Com o cofre ligado e algum caixa aberto, o sistema ainda pergunta se o dinheiro vai mesmo pro cofre. |

### cap06 · Corrigir e excluir lançamentos (vinheta: MOVIMENTAÇÕES)

Variante `lote` = `apos-cap04` + três despesas avulsas de teste na Conta Principal, de 09/11 ("Internet do pátio (teste)" R$ 149,90, "Seguro da picape (teste)" R$ 312,40, "Rastreador (teste)" R$ 89,90, categoria "Outras Despesas", soma R$ 552,20). A Conta Principal abre em R$ 44.684,77 e termina em R$ 45.236,97. O estado não segue adiante (o cap07 abre em `apos-cap04`).

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `lote`), "Conta Principal". A câmera desce ao histórico: três linhas com "(teste)" na descrição. | Ontem, treinando a equipe, o Rafael lançou três despesas de teste na Conta Principal. Elas não existem de verdade, e o saldo ficou menor do que devia. |
| Na linha "Rastreador (teste)", clique nos três pontinhos ("Ações do lançamento"): o menu com "Editar" e "Excluir". | Todo lançamento feito à mão tem esses três pontinhos, com Editar e Excluir. |
| Clique em "Editar": janela "Editar lançamento", com "Valor (R$)" e "Conta"; a câmera passa pelos dois campos; clique em "Cancelar". [ZOOM: "Valor (R$)" e "Conta"] | O Editar corrige o valor ou a conta. Digitou cento e cinquenta no lugar de quinze, ou lançou na conta errada? É aqui. |
| A câmera passa pelo ícone de setas no fim da linha ("Transferir para outra conta"), sem clicar. | Esse ícone do lado faz só a troca de conta, num clique. |
| Nos três pontinhos, clique em "Excluir": janela "Excluir lançamento?" com o valor que volta pro saldo e "Essa ação não pode ser desfeita."; clique em "Cancelar". [ZOOM: o texto da janela] | O Excluir apaga o lançamento e devolve o valor pro saldo. Dá pra fazer um por um. Mas são três, então vamos de uma vez. |
| Na busca "Buscar por descrição ou valor..." digita "teste": ficam as três linhas. | Primeiro eu filtro: busco por teste, e ficam só as três. |
| Clique em "Selecionar lançamentos": o botão vira "Cancelar seleção"; aparece a barra "0 lançamentos selecionados" / "Selecione até 100 itens. Lançamentos protegidos não exibem caixa de seleção."; cada linha ganha uma caixa de marcar. [ZOOM: a barra] | Agora, Selecionar lançamentos. Cada linha ganha uma caixinha, e aparece essa barra. Dá pra marcar até cem de uma vez, sempre da mesma conta. |
| Marca a caixa do cabeçalho ("Selecionar lançamentos elegíveis desta página"): "3 lançamentos selecionados" e os botões "Limpar", "Alterar categoria" e "Excluir selecionados". | Marco todas pela caixinha de cima. Três lançamentos selecionados. |
| Clique em "Alterar categoria": janela "Alterar categoria de 3 lançamentos", "Despesas selecionadas", "Nova categoria (despesa)"; clique em "Cancelar" (só mostra). [ZOOM: "Despesas selecionadas" e "Nova categoria (despesa)"] | Antes de excluir, repara nesse outro botão. O Alterar categoria troca a categoria de todos os marcados de uma vez. É o jeito rápido de arrumar despesa que caiu na categoria errada. Só não mistura entrada com saída no mesmo lote. |
| Clique em "Excluir selecionados": janela "Excluir 3 lançamentos?", "A seleção da conta Conta Principal será excluída em uma única operação. Se qualquer item não puder ser excluído, nenhum lançamento será alterado.", "Entradas selecionadas" e "Saídas selecionadas" R$ 552,20. [ZOOM: "Saídas selecionadas"] | Agora sim, Excluir selecionados. O sistema mostra o total do que vai sair: quinhentos e cinquenta e dois reais e vinte. Confiro antes de confirmar. |
| A câmera desce ao aviso âmbar e a "Essa ação não pode ser desfeita."; clique em "Excluir selecionados": aviso "3 lançamentos excluídos."; a barra some; o cartão azul volta para R$ 45.236,97. [ZOOM: o saldo do cartão] [BACKEND: `delete_bank_transactions_batch_atomic`] | Excluir. Os três saem juntos, e o saldo da conta volta pro lugar. |
| Limpa a busca; clique em "Selecionar lançamentos" de novo: os Pix de compra e de venda ficam sem caixa; clique em "Cancelar seleção". [ZOOM: uma linha de pedido sem caixa ao lado de uma com caixa] | Uma dica: Pix de compra e de venda não tem caixinha, porque pedido se corrige no próprio pedido. E o lote é tudo ou nada: se um dos marcados estiver conciliado ou protegido, o sistema avisa e não apaga nenhum. |

### cap07 · O que é conciliar (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: conciliação: à esquerda o cartão "Extrato do banco" com cinco linhas (data, descrição, valor), à direita o cartão "Lançamentos do sistema" com quatro; as linhas entram em "extrato" e em "lançamento"] | Com as contas em dia, a conciliação. Conciliar é conferir cada linha do extrato do banco com um lançamento do sistema. |
| (a ilustração: uma a uma as linhas se ligam por traços verdes e um placar embaixo, "Diferença", desce até R$ 0,00 em "zero") | Quando toda linha tem par, a diferença entre o saldo do banco e o do sistema chega a zero. |
| (a ilustração: a quinta linha do banco, "TARIFA PACOTE SERVICOS", fica sem par e pisca em âmbar em "tarifa"; um lançamento novo surge do lado do sistema e se liga a ela) | E a linha que sobra mostra o que ficou sem lançar, como uma tarifa que ninguém viu. É isso que deixa o fechamento do mês certo. |
| Capítulo novo (semente `apos-cap04`). Clique na aba "Conciliação": "Conta para conciliar" já com "Conta Principal"; no meio, "Nenhum extrato em conciliação" e o botão "Importar novo extrato". [BACKEND: `get_statement_imports` vazio] | Na tela, é a aba Conciliação. A conta já vem escolhida: a Conta Principal. |
| Clique em "Como funciona?": janela "Como funciona a conciliação bancária"; a câmera passa por "O que é conciliar?" e pelos passos; fecha a janela. [ZOOM: "O que é conciliar?" e o parágrafo embaixo] | E se bater dúvida, o Como funciona explica cada passo e cada botão. Primeiro, o extrato do banco. |

### cap08 · Importar o extrato (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: baixar o OFX: uma janela de banco genérica, sem marca, com quatro cartões em sequência: "Extrato" → "Período: 01/11 a 10/11" → "Exportar" → "OFX" (o cartão "PDF" ao lado fica cinza em "ler"); um arquivo "Extrato_20261101_20261110.ofx" desce para uma pasta "Downloads" em "OFX"] | O extrato sai do site ou do app do banco. Você abre o extrato, escolhe o período e exporta no formato OFX. O PDF serve pra ler; pra conciliar, é o OFX. |
| Capítulo novo (semente `apos-cap04`), aba "Conciliação". Clique em "Importar novo extrato": janela "Importar extrato OFX"; clique em "Como pegar o arquivo do seu banco?": o passo a passo abre. [ZOOM: o passo a passo, com "OFC", "Money", "Gerenciador Financeiro" ou "Conciliação bancária"] | Em Importar novo extrato, o próprio sistema ensina a achar o arquivo. Em alguns bancos ele tem outro nome, como Gerenciador Financeiro ou Conciliação bancária. |
| O robô entrega o arquivo `Extrato_20261101_20261110.ofx` na área "Arraste o arquivo .ofx aqui ou clique para selecionar" (a janela de arquivos do sistema não aparece); o nome do arquivo aparece com o botão "Trocar". | Escolho o arquivo que baixei, de um a dez de novembro. |
| "Prévia do extrato": "Banco", "Conta do arquivo" 40218-7, "Período" 01/11/2026 a 10/11/2026, "Transações" 17, "Saldo final do extrato" R$ 44.933,47 em 10/11/2026. [ZOOM: "Período", "Transações" e "Saldo final do extrato"] | Antes de importar, a prévia: o período, dezessete transações e o saldo final que o banco informou. |
| Clique em "Importar": a janela vira "Extrato importado", "17 de 17 linhas importadas" e a confirmação de que nenhuma linha estava repetida; aviso "Extrato importado" com as 17 transações; clique em "Concluir". [BACKEND: `create_bank_statement_import` grava o import e as 17 linhas, `opening_balance` 46.382,57, `inserted_count` 17; vira `apos-cap06`] | Importar. Se um dia você subir o mesmo período de novo, o sistema reconhece o que já entrou e não duplica. |
| A tabela: cabeçalho "Linha do extrato" e "Conciliação"; a câmera desce pelas primeiras linhas (data, a etiqueta "Pagamento" na da água, a descrição do banco, o valor) e pelos botões da direita. [BACKEND: `get_bank_reconciliation_state` com as 17 linhas e as sugestões do `plano.md`] | Pronto. À esquerda, cada linha do banco, com a data e o valor. À direita, o que fazer com ela. |
| A câmera passa por um valor verde com "+" (Pix da Serra Fina) e um vermelho com "−" (Pix do Depósito Irmãos Siqueira). | Uma dica: repara no sinal. Entrada vem em verde, com mais. Saída, em vermelho, com menos. Se alguma linha vier com o sinal trocado, confira com o banco antes de casar. |
| A câmera desce ao rodapé: "Saldo do banco" R$ 44.933,47, "Saldo conciliado" R$ 46.382,57, "Diferença" R$ -1.449,10 em vermelho e, embaixo do "Finalizar conciliação" (desabilitado), "Ainda há 17 linhas pendentes". | No rodapé ficam os três números do fechamento. A gente volta neles no fim. |

### cap09 · Casar com o sistema (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), o extrato aberto. Na linha "PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA" (03/11, −R$ 2.250,00), o bloco "Casa com um lançamento no sistema": "Compra #(nº) • Depósito Irmãos Siqueira", a data 03/11 e −R$ 2.250,00. [ZOOM: o bloco da sugestão] | Começa pelo mais fácil. Nesta linha, o Pix de dois mil duzentos e cinquenta reais pro Depósito Irmãos Siqueira, o sistema já achou o par: a compra do dia três. |
| Clique em "Casar com Compra #(nº) • Depósito Irmãos Siqueira": aviso "Linha casada"; a linha fica com o selo verde "Casada" e o botão "Desfazer". [BACKEND: `reconcile_match_existing`] | Confiro a data e o parceiro, e caso. A linha fica como Casada. |
| Trecho acelerado: o robô desce e, em cada sugestão verde, para meio segundo no lançamento e clica em "Confirmar": aluguel (−R$ 6.800,00), conserto do pneu (−R$ 180,00), energia (−R$ 1.874,30), Hidráulica Moretti (−R$ 1.740,00), Aços Quiririm (+R$ 2.000,00), combustível (−R$ 350,00), saque (−R$ 2.000,00) e tarifa do saque (−R$ 6,50). Não toca nas linhas sem sugestão nem nas do aviso âmbar. | As outras sugestões vão do mesmo jeito: o aluguel, a energia, o Pix da Aços Quiririm, o combustível, o saque e a tarifa dele. Cada uma eu confiro antes de casar. |
| A câmera para na linha "PIX RECEBIDO RECICLA VALE METAIS LTDA" (10/11, +R$ 8.000,00, etiqueta "Transferência"), com "Criar receita", "Mais ações" e a nota "Sem casamento automático." [BACKEND: linha 15 sem sugestão (`plano.md`); TESTAR o comportamento real] | Agora, os oito mil que vieram da Conta Secundária. Esse dinheiro já está no sistema: é a transferência que a gente registrou. |
| Clique em "Mais ações" e em "Casar com transferência" ("Dinheiro que veio de outra conta sua"): janela "Casar com transferência" ("Escolha a transferência entre suas contas que corresponde às linhas do extrato."), "Valor da linha" R$ 8.000,00 e a candidata "Conta Secundária → Conta Principal", 10/11, R$ 8.000,00. [ZOOM: a candidata] [BACKEND: `reconcile_search_transfer_candidates` devolve a perna +8.000,00] | Então é em Mais ações, Casar com transferência. Aparece a transferência certa, da Conta Secundária pra Conta Principal. |
| Marca a candidata; a câmera passa por "Isso só cria o vínculo da conciliação. Nenhum lançamento é criado e o saldo não muda."; clique em "Casar transferência": aviso "Linha casada com a transferência"; selo "Casada". [BACKEND: `reconcile_match_existing` com `p_allow_any_date`; vira `apos-cap07`] | Casar transferência. Isso só liga a linha à transferência: não cria nada novo e o saldo não muda. |
| A câmera fica no selo "Casada" da linha. | Uma dica: pra dinheiro que veio de outra conta sua, o caminho é sempre esse. Criar receita lançaria o valor de novo, e o saldo ficaria em dobro. |

### cap10 · Baixar uma conta (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`). A linha "PAGTO BOLETO AGUA E ESGOTO" (09/11, etiqueta "Pagamento", −R$ 238,40), com o botão "Baixar conta" e "Mais ações". | Esta linha é o boleto da água, duzentos e trinta e oito reais e quarenta. Lembra da conta de água que estava vencida? Ela foi paga no banco, mas a baixa ficou pra trás. |
| Clique em "Baixar conta": painel "Baixar conta a pagar"; clique em "Selecione a conta": a lista com "Água e esgoto de outubro", R$ 238,40. | Baixar conta. A lista traz só as contas em aberto do mesmo valor: a água e esgoto de outubro. |
| Escolhe "Água e esgoto de outubro"; clique em "Dar baixa de R$ 238,40": aviso "Conta baixada"; selo roxo "Baixada". [ZOOM: "Dar baixa de R$ 238,40"] [BACKEND: `reconcile_settle_bill` (conta paga, `paid_amount` 238,40, a saída na Conta Principal com a categoria "Água e esgoto"); vira `apos-cap08`] | Dar baixa. A linha fica como Baixada, e em Contas a Pagar e Receber a água já aparece como Paga. |
| A câmera fica no selo "Baixada". | Por aqui, a baixa é sempre do valor inteiro. Pagamento em parte, você faz na tela de Contas a Pagar e Receber. |

### cap11 · Criar um lançamento (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`). A linha "TARIFA PACOTE SERVICOS" (09/11, etiqueta "Tarifa", −R$ 64,90), com "Criar despesa", "Mais ações" e a nota "Sem casamento automático." | Esta outra linha não existe em lugar nenhum do sistema: a tarifa do pacote do banco, sessenta e quatro reais e noventa. |
| Clique em "Mais ações": o menu com "Baixar conta" (cinza, "Nenhuma conta em aberto bate com esta linha"), "Ajuste", "Funcionário", "Saldo do cliente/fornecedor", "Casar com transferência", "Buscar lançamento", "Casar com vários lançamentos" e "Ignorar". | Em Mais ações ficam todos os destinos de uma linha. O Funcionário, por exemplo, é pro vale pago por Pix. O Ajuste abre o mesmo lançamento com a opção de não contar na DRE, pra linha que só acerta saldo. E o Saldo do cliente ou fornecedor é pro acerto de fiado. |
| O cursor passa por "Funcionário", por "Ajuste" ("Abre o lançamento com a opção de não contar na DRE") e por "Saldo do cliente/fornecedor", sem clicar; fecha o menu (Esc). | Uma dica: vale que já foi lançado na tela de Funcionários se casa com o Buscar lançamento, sem criar de novo. O próprio painel do Funcionário lembra disso. |
| Clique em "Criar despesa": painel "Criar lançamento de saída", com o aviso azul "Veio de outra conta sua? Volte e use Casar com transferência.", a chave "Não é receita nem despesa (só ajusta o saldo)" desligada e a "Descrição" já com "TARIFA PACOTE SERVICOS". | Pra tarifa, é Criar despesa. A descrição já vem do extrato. E a chave Não é receita nem despesa fica desligada, porque tarifa é gasto de verdade. |
| Em "Categoria *" ("Selecione a categoria") escolhe "Tarifas"; o botão vira "Criar R$ 64,90". [ZOOM: "Categoria *" com "Tarifas" e o botão "Criar R$ 64,90"] | A categoria é obrigatória: Tarifas. E o botão já mostra o valor. |
| Clique em "Criar R$ 64,90": aviso "Lançamento criado"; selo azul "Criada". [BACKEND: `reconcile_create_transaction` (categoria Tarifas, −64,90, Conta Principal); vira `apos-cap09`] | Criar. A linha fica como Criada, e a tarifa entra no histórico da conta como despesa. |

### cap12 · Buscar e aceitar centavos (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`). A linha "PIX RECEBIDO SERRA FINA ALUMINIO" (09/11, +R$ 4.815,00), com "Criar receita", "Mais ações" e a nota "Sem casamento automático." [BACKEND: linha 6 sem sugestão, sem `near_matches`, sem candidato distante] | Este Pix da Serra Fina Alumínio caiu no dia nove: quatro mil oitocentos e quinze reais. E o sistema não sugeriu nada. |
| [ILUSTRAÇÃO: data e centavos: à esquerda o cartão do banco "09/11 · Pix · R$ 4.815,00"; à direita o cartão da venda "03/11 · 463 kg de alumínio perfil × R$ 10,40 = R$ 4.815,20"; em "dia três" as duas datas piscam em âmbar; em "centavos" os R$ 0,20 se destacam; um traço liga os dois cartões] | É que a venda foi registrada no dia três, por quatro mil oitocentos e quinze reais e vinte. A Serra Fina pagou depois e deixou os centavos de fora. |
| A câmera passa por "Criar receita", sem clicar; clique em "Mais ações" e em "Buscar lançamento": painel "Buscar lançamento para casar". | Em vez de criar outra receita, a gente procura a venda que já existe. Mais ações, Buscar lançamento. |
| Em "Nome do cliente/fornecedor, nº do pedido..." digita "Serra": a frase "Mostra lançamentos de R$ 4.815,00 (ou com até R$ 2,00 de diferença)" e o resultado "Venda #(nº) • Serra Fina Alumínio Reciclagem", 03/11, +R$ 4.815,20, com o selo âmbar "dif. −R$ 0,20". [ZOOM: o resultado com o selo "dif. −R$ 0,20"] [BACKEND: `reconcile_search_candidates` com "Serra" devolve a venda] | Digito Serra. A busca aceita até dois reais de diferença e casa mesmo com a data diferente. Olha a venda, com vinte centavos a menos. |
| Marca a venda; clique em "Casar com selecionado": janela "Casar com valor diferente?", "O lançamento é R$ 4.815,20 e a linha é R$ 4.815,00. Casar assim? A diferença de R$ -0,20 vai pro resumo de ajustes." | Casar com selecionado. O sistema confirma: casar com valor diferente? |
| Clique em "Casar assim": aviso "Linha casada"; selo "Casada"; no rodapé aparece o bloco âmbar "Diferenças casadas" com R$ -0,20. [ZOOM: "Diferenças casadas"] [BACKEND: casamento manual com `value_difference` −0,20; `matched_value_difference_total` −0,20 e `count` 1; vira `apos-cap10`] | Casar assim. A diferença não vira lançamento. Ela fica guardada no rodapé, em Diferenças casadas, pra quem quiser conferir. |
| A câmera fica no selo "Casada". | Uma dica: quando muda só a data, ou só uns centavos no mesmo dia, o sistema já mostra o lançamento num aviso, com o botão de casar. A busca fica pra quando mudam a data e o valor juntos, como aqui. |

### cap13 · Ignorar uma linha (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`). As linhas "TARIFA AVULSA" (09/11, etiqueta "Tarifa", −R$ 12,00) e "ESTORNO TARIFA AVULSA" (09/11, +R$ 12,00), uma embaixo da outra. | Estas duas linhas se anulam: o banco cobrou doze reais de tarifa por engano e devolveu no mesmo dia. |
| [ILUSTRAÇÃO: ignorar: as duas linhas, "−R$ 12,00" e "+R$ 12,00", se juntam e viram "R$ 0,00" em "nenhuma"; um selo cinza "Ignorada" pousa nas duas em "Ignorar"] | Nenhuma das duas precisa virar lançamento. Pra isso existe o Ignorar: a linha sai da fila sem criar nada. |
| Marca as caixas "Selecionar linha" das duas: a barra no topo com "2 selecionadas", "Soma: +R$ 0,00", "Ignorar (2)" e "Limpar seleção". [ZOOM: "2 selecionadas" e "Soma: +R$ 0,00"] | Marco as duas. A soma dá zero. |
| Clique em "Ignorar (2)": janela "Ignorar 2 linhas?" ("Elas saem do cálculo do saldo e podem ser desfeitas depois."); clique em "Ignorar": aviso de linhas ignoradas; as duas com o selo cinza "Ignorada". [BACKEND: `reconcile_ignore_entries_batch`; vira `apos-cap11`] | Ignorar. O sistema confirma, e as duas ficam como Ignorada. Dá pra desfazer depois, se precisar. |
| [ILUSTRAÇÃO: a cena volta com uma tarifa de verdade, "−R$ 64,90", ignorada sozinha: o placar "Diferença" fica vermelho em "aberta" e o botão "Finalizar conciliação" desenhado fica cinza em "não libera"] | Uma dica: ignorar conta como resolvido. Ignore só o que não mexeu no dinheiro da empresa, como esse par. Uma tarifa de verdade ignorada deixa a diferença aberta, e o fechamento não libera. |

### cap14 · Valores repetidos (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap11`). As linhas "PIX ENVIADO APARECIDA RAMOS" e "PIX ENVIADO AUTO PECAS VALE FORTE" (06/11, −R$ 380,00 cada), com o aviso âmbar "Atenção: há 2 lançamentos de R$ 380,00 que podem casar com esta linha. Escolha qual deles é o certo para evitar duplicidade." e o botão "Escolher lançamento". [ZOOM: o aviso da primeira linha] | Agora, duas linhas parecidas: dois Pix de trezentos e oitenta reais no mesmo dia. Um foi pra Aparecida Ramos; o outro, pra Auto Peças Vale Forte. |
| [ILUSTRAÇÃO: valores repetidos: à esquerda os dois Pix do banco, "R$ 380,00 · APARECIDA RAMOS" e "R$ 380,00 · AUTO PECAS VALE FORTE"; à direita as duas compras, "200 kg de plástico PET · Aparecida Ramos" e "400 kg de ferro pesado · Auto Peças Vale Forte"; em "errada" um traço cruzado fica vermelho e uma compra fica solta, piscando "pendente"; em seguida os traços certos, pelo nome, ficam verdes] | Aqui o sistema pede que você escolha. Casar com a compra errada deixaria a outra pendente pra sempre. |
| Na linha da Aparecida Ramos, clique em "Escolher lançamento": "Escolha o lançamento que casa com esta linha", com "Compra #(nº) • Aparecida Ramos" (06/11) e "Compra #(nº) • Auto Peças Vale Forte" (06/11), as duas −R$ 380,00. | Escolher lançamento. A lista mostra as duas compras, e o nome no extrato diz qual é: a da Aparecida Ramos. |
| Marca "Compra #(nº) • Aparecida Ramos"; clique em "Casar com o selecionado": aviso "Linha casada"; selo "Casada". [BACKEND: `reconcile_match_existing`; o estado recalcula a linha da Auto Peças] | Marco a compra da Aparecida, e Casar com o selecionado. |
| A linha da Auto Peças Vale Forte agora mostra a sugestão verde "Casa com um lançamento no sistema", "Compra #(nº) • Auto Peças Vale Forte"; clique em "Casar com Compra #(nº) • Auto Peças Vale Forte": selo "Casada". [BACKEND: a linha 4 deixa de ser ambígua (um candidato só); vira `apos-cap12`] | Repara: a outra linha ficou com um par só, e a sugestão já vem certa. É só casar. |
| A câmera fica nos dois selos "Casada". | Uma dica: quando aparecer esse aviso, escolha pelo nome e pela data do extrato. Assim nenhuma compra fica pendente nem vira lançamento em dobro. |

### cap15 · Desfazer e cancelar (vinheta: CONCILIAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap12`). Na linha do Depósito Irmãos Siqueira ("Casada"), clique em "Desfazer": aviso "Conciliação desfeita"; a linha volta a pendente, com a sugestão verde. [BACKEND: `reconcile_unmatch_entry` (sem confirmação: casamento com lançamento que já existia)] | Errou alguma? Toda linha resolvida tem o Desfazer, que devolve a linha pra pendente. Casada e Ignorada desfazem na hora. |
| Clique em "Casar com Compra #(nº) • Depósito Irmãos Siqueira": selo "Casada" de novo. | Aqui eu só desfiz pra mostrar, então caso de novo. |
| A câmera vai à linha da tarifa ("Criada") e para no "Desfazer", sem clicar. | Já a Criada e a Baixada mexem em dinheiro. O Desfazer delas pede confirmação, porque apaga o lançamento criado ou estorna a baixa. |
| Clique em "Cancelar conciliação" (no alto, à direita): janela "Cancelar esta conciliação?", com "17 linha(s) do extrato serão canceladas", "13 vínculo(s) com lançamento existente serão removidos; os lançamentos serão preservados", "1 conta(s) a pagar/receber serão reabertas", "1 lançamento(s) criado(s) pela conciliação serão excluídos", "2 linha(s) ignorada(s) voltarão ao estado anterior" (a ordem segue a primeira linha de cada tipo) e "Digite CANCELAR para confirmar"; clique em "Manter conciliação". [ZOOM: a lista e o campo do CANCELAR] | E o Cancelar conciliação desfaz o arquivo inteiro de uma vez: os vínculos, os lançamentos criados e as baixas. Por segurança, pede pra digitar a palavra cancelar. Aqui eu mantenho a conciliação. |
| Clique em "Voltar" (no alto): a entrada da aba com o cartão "Continuar conciliação", "Todas as linhas resolvidas" (falta finalizar), o nome do arquivo e o período; clique em "Continuar": a tabela volta. [BACKEND: `get_statement_imports` com o import aberto e `pending_count` 0] | Já o Voltar só sai da tela. O progresso fica salvo, e o Continuar retoma de onde parou, até no dia seguinte. |
| A câmera fica na tabela, com os selos das linhas. | Uma dica: lançamento conciliado não sai pelo Excluir das movimentações. Primeiro você desfaz a linha aqui, e depois exclui lá. |

### cap16 · Fechar a conciliação (vinheta: FECHAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap12`), o extrato aberto. A câmera desce ao rodapé: "Saldo do banco" R$ 44.933,47, "Saldo conciliado" R$ 44.933,47, "Diferença" R$ 0,00 em verde e "Diferenças casadas" R$ -0,20. [ZOOM: "Saldo do banco" e "Saldo conciliado"] | Hora de fechar. No rodapé, o Saldo do banco é o saldo final que veio no arquivo. O Saldo conciliado é o que o sistema soma com as linhas resolvidas. |
| [ILUSTRAÇÃO: os três números: uma balança de dois pratos, "Saldo do banco" num prato e "Saldo conciliado" no outro; a "Diferença" é o desnível entre eles; linhas resolvidas pousam no prato do sistema até a balança nivelar em "zero", e o placar "Diferença R$ 0,00" fica verde em "verde"] | A Diferença é a distância entre os dois. Ela está em zero, em verde, e não sobrou nenhuma linha pendente. |
| Clique em "Diferenças casadas": o quadro "Diferenças de valor casadas" com o pedido da Serra Fina, "R$ 4.815,00 → R$ 4.815,20" e R$ -0,20; fecha o quadro. | Os vinte centavos da Serra Fina ficam aqui, só pra conferência. Eles não travam o fechamento. |
| A câmera para no botão "Finalizar conciliação", habilitado. | Uma dica: o fechamento só libera com todas as linhas resolvidas e a diferença em zero. Se ela não zerar, alguma linha foi ignorada sem motivo. Cada linha se resolve de verdade, sem lançamento pra forçar o zero, e é isso que deixa o fechamento confiável. |
| Clique em "Finalizar conciliação": aviso "Conciliação finalizada"; no topo, a faixa "Conciliação finalizada" (somente leitura); no rodapé, o selo "Conciliação finalizada"; os botões "Desfazer" somem. [BACKEND: `finalize_bank_reconciliation`; vira `apos-cap14`] | Finalizar conciliação. Pronto: esse extrato fica selado, só pra leitura. |
| Clique em "Fechar" (no alto): a entrada da aba com "Importar novo extrato" e "Conciliações anteriores (1)"; clique para abrir: "Extrato_20261101_20261110.ofx", "01/11/2026 a 10/11/2026 · 17 linhas" e o selo "Conciliado". | Ele vai pra Conciliações anteriores, com o selo Conciliado. No próximo extrato, é só importar e seguir do mesmo jeito. |

### cap17 · Outros casos do extrato (vinheta: CONCILIAÇÃO)

Segundo extrato, da Conta Secundária (`Extrato_Secundaria_20261106_20261109.ofx`, 8 linhas, conta 51730-2). Não é finalizado e não segue para a T15. Variante `outros` (partida: `apos-cap14`, com a Secundária em R$ 75.380,00 depois da transferência do cap05).

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `outros`). Aba "Conciliação"; em "Conta para conciliar" escolhe "Conta Secundária"; "Importar novo extrato", entrega o arquivo, "Importar", "Concluir" (trecho acelerado): oito linhas; as quatro com par certo são confirmadas no acelerado e sobram quatro. | Na Conta Secundária, o extrato é pequeno, mas tem casos que aparecem bastante. Eu importo o arquivo e já casei as linhas que têm par certo. Sobram os casos diferentes. |
| Linha do Pix enviado ao Depósito Irmãos Siqueira (R$ 340,00): "Mais ações" › "Saldo do cliente/fornecedor": painel "Baixar na conta-corrente"; em "Cliente ou fornecedor *" escolhe o Depósito; aparece o saldo dele. [ZOOM: o saldo do parceiro e o botão "Dar baixa de R$ ..."] [BACKEND: `reconcile_create_balance_payment`] | O primeiro é o acerto de fiado: a empresa devia ao Depósito Irmãos Siqueira e pagou uma parte por Pix. É em Mais ações, Saldo do cliente ou fornecedor. Escolho o Depósito, e o sistema mostra o saldo dele. |
| Clique em "Dar baixa de R$ 340,00": selo da linha resolvida. | Dar baixa. Não precisa bater com o valor do pedido: cada Pix abate o que ele vale, até zerar a dívida. |
| Linha do Pix recebido da Aços Quiririm (+R$ 50.215,00): "Mais ações" › "Casar com vários lançamentos"; marca as duas vendas; o botão vira "Casar com 2 lançamentos"; clique. [ZOOM: as duas vendas marcadas e a soma] [BACKEND: `reconcile_search_split_candidates`, `reconcile_match_entry_split`] | O segundo: um Pix só pagou duas vendas do mesmo cliente. Em Mais ações, Casar com vários lançamentos, marco as duas vendas. Quando a soma fecha com o valor da linha, o botão libera. |
| Linhas "FOLHA LOTE 1" e "FOLHA LOTE 2": marca as duas caixas; na barra, "Soma:" e "Casar 2 linhas com um lançamento"; clique: janela; escolhe o lançamento da folha; "Casar 2 linhas". [ZOOM: "Soma:" e o botão] [BACKEND: `reconcile_match_group`] | O terceiro é o contrário: o banco mostra duas linhas, e no sistema é um lançamento só, a folha de pagamento. Marco as duas, confiro a soma, e Casar duas linhas com um lançamento. |
| [ILUSTRAÇÃO: o Pix lançado na conta errada: o bloco "Achamos este lançamento em outra conta" e o botão "Mover para ... e casar"] | E quando o Pix foi lançado na conta errada, o sistema avisa na própria linha: achamos este lançamento em outra conta. Um botão move o lançamento pra conta certa e já casa. |
| A câmera passa por "Criar receita" numa linha de entrada, sem clicar. | Entrada que não existe no sistema, como um rendimento, é Criar receita, igual à tarifa que a gente criou. O resto segue como no extrato anterior. |

### cap18 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a "Conta Cooperativa" entrando na lista (cap02) e o "Cartão Empresa" (cap03). | Pronto! Recapitulando: a gente cadastrou a Conta Cooperativa com o saldo inicial, arquivou a poupança que ninguém usava e cadastrou o cartão de crédito da empresa. |
| Montagem rápida: "Ajustar saldo da Conta DINHEIRO" com +R$ 60,00 (cap04) e os "Efeitos desta transação" do saque (cap05). | Ajustou o cofre pelo caminho certo e registrou o combustível, a transferência e o saque, cada um do seu jeito. |
| Montagem rápida: a barra "3 lançamentos selecionados" e a janela "Excluir 3 lançamentos?" (cap06). | Corrigiu e excluiu lançamentos, um por um e vários de uma vez. |
| Montagem rápida: a "Prévia do extrato" (cap08) e a janela "Casar com transferência" (cap09). | Importou o extrato do banco e casou as linhas com os lançamentos, inclusive a transferência entre as contas. |
| Montagem rápida: os selos "Baixada" (cap10) e "Criada" (cap11), "Diferenças casadas" (cap12) e "Ignorada" (cap13). | Deu baixa na conta de água pelo extrato, criou a tarifa, aceitou a diferença de centavos e ignorou o par de tarifa e estorno. |
| Montagem rápida: o aviso âmbar dos R$ 380,00 (cap14) e o rodapé com "Diferença" R$ 0,00 e "Conciliação finalizada" (cap16). | Escolheu o lançamento certo entre os valores repetidos e finalizou a conciliação com diferença zero. |
| Montagem rápida: "Casar com vários lançamentos" e "Casar 2 linhas com um lançamento" (cap17). | E, no extrato de outra conta, resolveu o acerto de fiado, o Pix que pagou duas vendas e as duas linhas do banco que são um lançamento só. |
| Cartão "Próximo: Relatório Financeiro e DRE"; cartela final. | No próximo tutorial, a gente responde a pergunta que todo dono faz: eu ganhei ou perdi dinheiro esse mês? Até lá! |
