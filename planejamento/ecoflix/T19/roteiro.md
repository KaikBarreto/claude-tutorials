# Roteiro T19 · Funcionários e ponto eletrônico

Roteiro pronto para a voz e a gravação (molde da Domiflix, sem etapa de aprovação). Coluna Fala = texto da narração (voz Kaik
Barreto), na grafia da legenda; a grafia de pronúncia do TTS fica em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde
a câmera foca, com os rótulos entre aspas como no código 1.59.154 (`T19/inventario.md`). Mundo e sementes: `T19/plano.md`.
Desktop 1280×800, logado como Rafael Nogueira (MASTER), menu lateral aberto; o capítulo 9 é no celular (`device: phone`, sem login).
Cada capítulo parte de um navegador novo com a semente do fim do anterior.

- **Título:** Funcionários e ponto eletrônico
- **Antes:** Relatório Financeiro e DRE (T15)
- **Próximo:** White Label (T27)
- **Vinhetas (áreas):** FUNCIONÁRIOS · CADASTRO · CADASTRO · DEPARTAMENTOS · MOVIMENTAÇÕES · PAGAMENTO · EXTRATO · PONTO
  ELETRÔNICO · PONTO ELETRÔNICO · PONTO ELETRÔNICO · PONTO ELETRÔNICO · FUNCIONÁRIOS · RESUMO
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos, no backend falso e no robô.
- **Duração estimada:** ~16 min de vídeo (≈ 2.050 palavras, ~13,2 min de voz a 2,6 palavras/s, mais 13 vinhetas, 11 ilustrações e
  as esperas). Alvo da fonte: 16 min.
- 🔒 módulo Funcionários (RH): dito no cap. 0. Sem preço de plano.
- Marcas na Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[ZOOM: ...]` (dura a frase inteira), `[ILUSTRAÇÃO: ...]`,
  `[TESTAR: ...]` (o robô confere antes de gravar).
- Pronúncias (TTS): Funcionários (RH) "Funcionários érre-agá", DRE "dê-érri-ê", PDF "pê-dê-éfe" (do perfil); novas: CLT
  "cê-éle-tê", INSS "i-ene-ésse-ésse", EPI "é-pê-í", PIN "pin" (testar no nó de pronúncia).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Funcionários e ponto eletrônico". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira; o cursor vai ao menu lateral e clica em "Funcionários (RH)"; abre "Funcionários (RH)" · "Gerencie sua equipe e controle de pagamentos", na aba "Funcionários", com a lista "Equipe". [BACKEND: semente `seeds-extra/t19/inicio.json` (plano.md, "Mundo")] | Oi! Neste tutorial a gente vai colocar a equipe do pátio da Recicla Vale Metais dentro do sistema: quanto cada um ganha, o que já adiantou e a que horas bateu o ponto. |
| [ILUSTRAÇÃO: o caderninho do pátio: um caderno aberto com "Vale Diego 200", "Falta sexta" e "Bônus Cláudio" escritos à mão e um relógio de cartão de ponto ao lado; na palavra "lembrar", as anotações se embaralham; na última frase, viram três cartões limpos na cor da marca: "Saldo", "Extrato" e "Ponto"] | Num ferro-velho, vale sai do caixa quase toda semana. Se fica só no caderno, no dia do pagamento alguém precisa lembrar de tudo. Aqui, cada coisa fica no lugar dela. |
| De volta à tela; cartão discreto "Módulo Funcionários (RH)". | Tudo isso fica em Funcionários RH, que depende do plano contratado. |
| Cartão discreto "Antes: Relatório Financeiro e DRE". | Os vales e os pagamentos saem do caixa e entram no relatório financeiro. Então, se você ainda não viu o tutorial Relatório Financeiro e DRE, dá uma olhada antes. [pause] Vamos conhecer a tela. |

### cap01 · A tela Funcionários e suas abas (vinheta: FUNCIONÁRIOS)

| Tela | Fala |
| --- | --- |
| Zoom suave nas abas do topo, da esquerda para a direita, sem clicar: "Funcionários", "Registro de Ponto", "Folha de Ponto", "Ausências" e "Configurações de Ponto". | Lá em cima ficam as abas. Em Funcionários ficam o cadastro e o dinheiro de cada um. Registro de Ponto, Folha de Ponto, Ausências e Configurações de Ponto são do ponto eletrônico. |
| A câmera segue para "Configurações de RH" e "Dashboard"; desce para "Ativos" / "Inativos" e para os botões "Gerenciar departamentos", "Exportar Relatório" e "Novo Funcionário". | No fim, as Configurações de RH e o Dashboard. Na aba Funcionários, a lista abre nos Ativos, e do lado ficam os departamentos, o relatório e o botão Novo Funcionário. |
| A lista "Equipe" (7) com os selos verdes de saldo; zoom na busca "Buscar por nome ou cargo...". | Cada pessoa aparece com o cargo e, do lado, o saldo: o que a empresa ainda vai pagar pra ela. Em cima, dá pra buscar pelo nome ou pelo cargo. |
| Clique em "Diego Santana": a ficha abre à direita ("Ativo"; "Movimentações" com "Vale", "Bônus", "Falta", "Recebimento" e "Pagamento"; "Resumo financeiro"; "Dados profissionais"). | Clicando no Diego, o ajudante do pátio, abre a ficha dele: os botões de vale, bônus, falta, recebimento e pagamento, o resumo do salário e do saldo e os dados do cadastro. |
| Clique na aba "Dashboard": "Funcionários Ativos", "Folha de Pagamento", "Média Salarial" e "Saldo Total a Pagar"; volta para "Funcionários". | E o Dashboard resume a equipe inteira: quantos estão ativos, a soma dos salários e o saldo total a pagar. |

### cap02 · Cadastrar o funcionário (vinheta: CADASTRO)

| Tela | Fala |
| --- | --- |
| Clique em "Novo Funcionário": janela "Novo Funcionário" com as abas "Dados", "Remuneração" e "Ponto eletrônico", aberta em "Dados". | Começando pelo cadastro. O Gabriel Rocha começou hoje como ajudante de pátio. Em Novo Funcionário, a janela abre na aba Dados. |
| Digita "Gabriel Rocha" em "Nome *"; em "CPF", 41827395664 (a máscara mostra 418.273.956-64); em "Telefone", 12900004107 (fica (12) 90000-4107). [ZOOM: "CPF" com 418.273.956-64, a frase toda] | Coloco o nome, o CPF e o telefone. O CPF é conferido assim que você sai do campo. |
| Em "Cargo", "Ajudante de pátio"; em "Departamento", escolhe "Pátio" (bolinha verde); em "Data de Admissão", 10/11/2026. | O cargo é ajudante de pátio, no departamento Pátio, e a admissão é hoje, dez de novembro. |
| Aba "Remuneração"; em "Salário *", 1980,00 (fica R$ 1.980,00). [ZOOM: "Salário *" com R$ 1.980,00] | Na aba Remuneração vai o salário: mil novecentos e oitenta reais. |
| [ILUSTRAÇÃO: o iceberg do custo: um iceberg no mar com "Salário R$ 1.980" na ponta, fora da água; na palavra "ponta", a água baixa e aparecem embaixo, um por vez, "fundo de garantia", "décimo terceiro", "férias", "INSS da empresa" e "EPI"] | E quanto ele custa de verdade pra empresa? O salário é só a ponta. |
| Clique em "Calcular", ao lado de "Custo mensal total": janela "Calcular custo mensal" · "Composição do custo mensal"; "Regime tributário" já em "Lucro Real / Presumido"; "Salário base" R$ 1.980,00. [BACKEND: `company_fiscal_config.is_simples_nacional = false` (Lucro Real)] | O botão Calcular abre a conta, e o regime tributário já vem do cadastro fiscal: Lucro Real. Quem define isso é o contador. |
| Em "Custos anuais (rateado ÷ 12)", campo "EPI e uniformes": 600,00 (aparece "Mensal: R$ 50,00"); a câmera desce para o resumo: "+ FGTS (8%)", "+ 13º (provisão)", "+ Férias + 1/3 (provisão)", "+ INSS patronal (28.8%)", "+ Custos anuais (÷12)" e "Custo total mensal" R$ 3.361,00. [ZOOM: "Custo total mensal" R$ 3.361,00, na frase do total] | Coloco seiscentos reais por ano de EPI e uniforme, a luva e a botina. A calculadora soma o fundo de garantia, o décimo terceiro, as férias e o INSS da empresa. Custo total mensal: três mil trezentos e sessenta e um reais. |
| Zoom no rodapé "Valores estimados com base na legislação trabalhista. ..."; clique em "Aplicar R$ 3.361,00": o campo "Custo mensal total" fica com R$ 3.361,00. | São valores estimados, e o contador confirma. Clico em Aplicar, e o custo fica no cadastro, pra você enxergar quanto a equipe pesa. |
| Em "Chave PIX", "(12) 90000-4107"; clique em "Cadastrar": aviso "Funcionário cadastrado"; o Gabriel entra na lista "Equipe". [BACKEND: `INSERT employees` + RPC `generate_ponto_slug` (o ponto nasce ligado porque a empresa já usa o ponto) devolvendo `gabriel-rocha-4f7k`; vira `apos-cap02`] | Por último, a chave Pix, que aqui é o celular dele. Cadastrar. Pronto, o Gabriel já está na lista. |
| Zoom no selo de saldo do Gabriel, R$ 1.980,00. | Uma dica: funcionário novo já nasce com o saldo igual ao salário, mil novecentos e oitenta. Daqui pra frente, cada vale, bônus e falta mexe nesse número. |

### cap03 · Campos de folha (vinheta: CADASTRO)

| Tela | Fala |
| --- | --- |
| Menu "…" do Gabriel → "Editar": "Editar Funcionário"; aba "Remuneração"; em "Regime de contratação", clique em "CLT". [BACKEND: semente `apos-cap02`] | Agora os campos de folha. O Gabriel vai ser registrado em carteira. Então, editando o cadastro, em Regime de contratação, eu marco CLT. |
| Aparecem "Nº de dependentes (IRRF)" e "Desconta vale-transporte (até 6%)"; em "Nº de dependentes (IRRF)", digita 1. | Aparecem os campos de folha. Em Número de dependentes, coloco um, o filho dele. É o número que entra no cálculo do imposto de renda. |
| Liga "Desconta vale-transporte (até 6%)"; aparece "Valor mensal do VT": 220,00 (fica R$ 220,00). [ZOOM: "Valor mensal do VT" com R$ 220,00] | Ele vem de ônibus, então ligo o desconto do vale-transporte. O vale dele custa duzentos e vinte reais por mês, e o desconto vai até seis por cento do salário, como diz a tela. |
| Clique em "Atualizar": aviso "Funcionário atualizado". [BACKEND: RPC `update_employee_with_salary_adjustment` sem troca de salário (nenhum ajuste no extrato); vira `apos-cap03`] | Atualizar, e pronto. |
| [ILUSTRAÇÃO: Informal × CLT: dois cartões lado a lado; "Informal" com a conta "salário mais bônus, menos faltas e vales"; na palavra "CLT", o segundo cartão entra com a mesma conta e mais três linhas, "INSS", "imposto de renda" e "vale-transporte", com o selo "estimado"] | Esses campos entram no pagamento feito no modo CLT, que estima os descontos da folha. Pra quem é informal, o pagamento é a conta simples do saldo. |

### cap04 · Departamentos (vinheta: DEPARTAMENTOS)

| Tela | Fala |
| --- | --- |
| Clique em "Gerenciar departamentos": janela "Departamentos" · "Organize seus funcionários em departamentos por cor e ícone.", com "Escritório" (azul, maleta) e "Pátio" (verde, chave). [BACKEND: semente `apos-cap03`] | Pra organizar a equipe, tem os departamentos. A Recicla Vale Metais já tem o Escritório e o Pátio. |
| Em "Novo departamento": "Nome *" = "Transporte"; em "Cor", o robô preenche #EA580C (laranja) sem abrir o seletor do sistema; em "Ícone", abre a grade e escolhe o caminhão (`truck`). | Vou criar o Transporte, pros motoristas. Escolho uma cor, o laranja, e o ícone do caminhão. |
| Clique em "Adicionar": aviso "Departamento criado"; "Transporte" entra na lista; fecha a janela. [BACKEND: `INSERT employee_departments`] | Adicionar, e ele já entra na lista. |
| "Edson Moura" → "Editar" → "Departamento": "Transporte" → "Atualizar": aviso "Funcionário atualizado"; na lista, o Edson aparece com o caminhão laranja e "Transporte". | Agora é só colocar o Edson, o motorista, nele. No cadastro, em Departamento, escolho Transporte e atualizo. Pronto: na lista ele já aparece com a cor e o ícone. |
| Clique em "Filtros": "Departamento" com "Todos os departamentos", "Sem departamento", "Escritório", "Pátio" e "Transporte"; fecha sem filtrar. [vira `apos-cap04`] | E nos Filtros da lista dá pra ver um departamento de cada vez. |

### cap05 · Lançar vale, bônus e falta (vinheta: MOVIMENTAÇÕES)

| Tela | Fala |
| --- | --- |
| Clique em "Diego Santana"; zoom no "Resumo financeiro": "Salário" R$ 1.980,00 e "Saldo atual" R$ 1.980,00. [BACKEND: semente `apos-cap04`] | Agora o dia a dia. O Diego recebeu o salário ontem, então o saldo dele voltou pra mil novecentos e oitenta reais. |
| Botão "Vale": "Registrar Vale" · "Adiantamento que será descontado do saldo do funcionário"; "Origem do Pagamento" já em "Dinheiro (Caixa)"; em "Valor *", 200,00 (R$ 200,00); em "Descrição (opcional)", "Adiantamento". [ZOOM: "Valor *" com R$ 200,00] (sem zoom no "Saldo: R$ 1500.00") | Hoje ele pediu um vale de duzentos reais. No botão Vale, a origem já vem em Dinheiro, do caixa. Coloco o valor e uma descrição. |
| Clique em "Confirmar": a janela fecha (sem zoom no aviso); "Saldo atual" vai para R$ 1.780,00. [BACKEND: `employee_movements` "vale" + `cash_transactions` "Vale - Diego Santana" (Folha Salarial) + RPC `adjust_cash_register_balance` no caixa do Rafael] | Confirmar. O dinheiro sai do caixa aberto, e o saldo dele cai pra mil setecentos e oitenta. |
| A câmera fica em "Vales" R$ 200,00, no "Resumo financeiro". | Uma dica: o vale lançado aqui já mexe no caixa ou no banco. Então não lance de novo em Movimentações Bancárias. Na conciliação do extrato, é só usar o Buscar lançamento pra casar com ele. |
| Botão "Falta": "Registrar Falta" · "Desconto por falta que será subtraído do saldo"; em "Valor *", 90,00; em "Descrição (opcional)", "Faltou sexta, 06/11, sem avisar"; clique em "Confirmar". [ZOOM: "Valor *" com R$ 90,00] | Na sexta, o Diego faltou sem avisar. Na Falta, lanço o desconto de um dia: noventa reais. |
| Zoom no "Resumo financeiro": "Saldo atual" R$ 1.690,00, "Vales" R$ 200,00 e "Faltas" R$ 90,00. [ZOOM: "Saldo atual" R$ 1.690,00] | Repara na conta: mil novecentos e oitenta de salário, menos duzentos de vale, menos noventa da falta. Saldo: mil seiscentos e noventa. |
| [ILUSTRAÇÃO: a conta do saldo: uma fita de máquina de somar; entram, um por vez, "Salário 1.980", "mais Bônus 0", "menos Faltas 90", "menos Vales 200" e o total "Saldo 1.690"; na palavra "Pagou", um carimbo "Pago" cobre a fita e ela recomeça só com "Salário 1.980"] | Uma dica: o saldo é sempre o salário, mais os bônus, menos as faltas e os vales, contando só o que aconteceu depois do último pagamento. Pagou, ele recomeça do salário. |
| Clique em "Cláudio Ribeiro" ("Saldo atual" R$ 2.600,00); botão "Bônus": "Registrar Bônus"; em "Valor *", 150,00; em "Descrição (opcional)", "Meta de prensagem de outubro"; clique em "Confirmar"; "Saldo atual" vai para R$ 2.750,00. [ZOOM: "Valor *" com R$ 150,00] [vira `apos-cap05`] | E o bônus soma. O Cláudio, da empilhadeira, bateu a meta de prensagem de outubro: cento e cinquenta reais. O saldo dele sobe pra dois mil setecentos e cinquenta. |

### cap06 · Pagar e receber do funcionário (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| Clique em "Edson Moura": "Resumo financeiro" com "Salário" R$ 2.900,00, "Saldo atual" R$ 2.650,00, "Vales" R$ 500,00 e "Bônus" R$ 250,00. [BACKEND: semente `apos-cap05`] | Hora de pagar. O Edson estava na estrada ontem, dia do pagamento, e recebe hoje. Em outubro ele pegou quinhentos reais de vale e ganhou duzentos e cinquenta de bônus. |
| Botão "Recebimento": "Receber do Funcionário" · "Registrar devolução de valor pelo funcionário", com "Vales pendentes:" R$ 500,00; em "Valor a receber", 100,00; "Forma de Recebimento" em "Dinheiro (entra no caixa)"; em "Observações (opcional)", "Sobra do vale da viagem". [ZOOM: "Valor a receber" com 100,00 e "Máximo: R$ 500,00 (total de vales pendentes)"] | Antes, ele devolveu cem reais de um vale que não usou. Isso é o Recebimento: o dinheiro entra no caixa e abate dos vales. |
| Clique em "Confirmar Recebimento": "Recebimento confirmado!", com "Vales antes" R$ 500,00, "Abatido" -R$ 100,00 e "Vales restantes" R$ 400,00; clique em "Fechar". [ZOOM: "Vales restantes" R$ 400,00] [BACKEND: `cash_transactions` deposit "Recebimento - Edson Moura" + `employee_movements` "recebimento"] | Confirmado: dos quinhentos de vale, sobram quatrocentos. |
| Botão "Pagamento": "Realizar Pagamento" · "Pagamento ao funcionário"; ao lado, o "Resumo do funcionário": "Salário:" R$ 2.900,00, "Total de Bônus:" R$ 250,00 e "Descontos:" R$ 400,00 ("Vales:" R$ 400,00, "Faltas:" R$ 0,00). [TESTAR: em 1280 px o resumo flutua à direita; se não couber, vem empilhado no topo] | Agora o Pagamento. O resumo mostra o salário, o bônus e os descontos. |
| Zoom em "Quanto você quer descontar dos vales" (400,00) e "Valor padrão: 100% dos vales (R$ 400,00)". | Aqui você escolhe quanto dos vales desconta agora. O padrão é tudo, os quatrocentos. O que ficar de fora passa pro próximo pagamento. |
| Em "Modo de pagamento", clique em "CLT (com folha)": no resumo entram "Folha CLT", "- INSS", "- IRRF", "Líquido" e "Valores estimados; confirme com seu contador."; clique em "Normal". [ZOOM: "Valores estimados; confirme com seu contador."] (sem zoom nos valores do modo CLT) | No modo CLT, o sistema estima o INSS e o imposto de renda e mostra o líquido. Uma dica: são valores estimados, então confirme com o seu contador. O Edson é informal, então volto pro Normal. |
| Zoom em "Valor efetivamente pago" 2.750,00 e "Calculado: R$ 2.750,00". [ZOOM: "Valor efetivamente pago"] | O valor fica em dois mil setecentos e cinquenta: o salário, mais o bônus, menos os quatrocentos de vale. Se você pagar outro valor, a tela pede o motivo, e a diferença vale só pra esse pagamento. |
| Em "Forma de Pagamento", "PIX/Transferência"; "Conta bancária" já na conta principal; clique em "Confirmar Pagamento"; a janela fecha. [BACKEND: `employee_movements` "pagamento" (`balance_after` 0) + "ajuste" "Reset para salário base" + `bank_transactions` "Pagamento - Edson Moura" (Folha Salarial) na conta principal; vira `apos-cap06`] [TESTAR: "Pagamento registrado!" não deve abrir (plano.md, risco 5); se abrir, "Não, obrigado"] | Ele recebe por Pix, da conta principal. Confirmar Pagamento. |
| Zoom no "Saldo atual" R$ 2.900,00 (e "Último pagamento" com a data de hoje, em "Dados profissionais"). | Repara no saldo: voltou pra dois mil e novecentos, o salário dele. |
| [ILUSTRAÇÃO: o ciclo do pagamento: uma linha do tempo de outubro em que o vale, o bônus e o recebimento caem num balde "Saldo"; na palavra "fecha", o balde esvazia no "Pagamento"; na palavra "próximo", um balde novo de novembro começa cheio só com "Salário 2.900"] | O pagamento fecha o mês. Tudo o que vier depois, vale, bônus ou falta, conta pro próximo. |

### cap07 · O extrato do funcionário (vinheta: EXTRATO)

| Tela | Fala |
| --- | --- |
| Botão "Extrato": janela "Extrato - Edson Moura"; cartões "Bônus" R$ 0,00, "Vales" R$ 0,00, "Faltas" R$ 0,00 e "Saldo" R$ 2.900,00. [BACKEND: semente `apos-cap06`] | Tudo isso fica guardado no Extrato. Em cima, o mês que começou agora: sem vale, sem bônus, e o saldo igual ao salário. |
| A linha "Pagamento" de hoje, R$ 2.750,00 ("Saldo após: R$ 0,00"), com "Salário base", "+ Bônus", "Subtotal", "Total de vales acumulados", "Vales descontados neste pgto", "Valor pago" e "Forma" PIX, e o botão "Gerar Recibo"; junto, a linha "Ajuste" "Reset para salário base". [ZOOM: "Valor pago" R$ 2.750,00] [TESTAR: a ordem das linhas "Ajuste" e "Pagamento"] | Embaixo, cada movimento. O pagamento de hoje mostra a conta inteira e tem o Gerar Recibo, pro recibo do Edson. Junto dele fica o ajuste que volta o saldo pro salário. |
| Rola a lista: "Recebimento" +R$ 100,00 ("Recebimento do funcionário - Sobra do vale da viagem", "via Dinheiro"), os dois "Vale" (com "Gerar Recibo"), o "Bônus" e a linha "Ajuste" "Ajuste de salário: R$ 2.800,00 → R$ 2.900,00". [ZOOM: "Ajuste de salário: R$ 2.800,00 → R$ 2.900,00", nesta frase e na seguinte] | Mais pra baixo, o recebimento de hoje e os vales e o bônus de outubro. E repara nessa linha: Ajuste de salário, de dois mil e oitocentos pra dois mil e novecentos. |
| (o zoom continua na linha do ajuste) | Quando você troca o salário no cadastro, o sistema lança esse ajuste sozinho e corrige o saldo pela diferença. Nada some do histórico. |
| Zoom na lixeira de uma linha "Vale", sem clicar. | Uma dica: excluir um vale ou um pagamento aqui também desfaz o dinheiro no caixa ou no banco. |
| [ILUSTRAÇÃO: a linha do extrato presa ao dinheiro: a linha "Vale 300" ligada por um fio a uma gaveta de caixa; na palavra "junto", a lixeira leva a linha e o fio puxa os trezentos de volta para a gaveta] Depois, clique em "Fechar". | A lixeira leva o dinheiro junto. Então use ela só pra lançamento errado. |

### cap08 · Ligar o ponto e gerar o link (vinheta: PONTO ELETRÔNICO)

| Tela | Fala |
| --- | --- |
| Menu "…" do Gabriel → "Editar" → aba "Ponto eletrônico": "Ativar ponto eletrônico" ligado · "Gera um link público pro funcionário bater ponto sem login.". [BACKEND: semente `apos-cap06`; Gabriel com `ponto_enabled` e `ponto_slug` `gabriel-rocha-4f7k`] | Agora o ponto eletrônico. Ele fica no cadastro, na aba Ponto eletrônico. Como a Recicla Vale Metais já usa o ponto, o Gabriel já nasceu com ele ligado. |
| Zoom em "PIN do ponto (opcional)" · "Sem PIN. Qualquer um com o link consegue bater o ponto dele." e no botão "Definir PIN", sem clicar; clique em "Cancelar". | Ligado, ele ganha um link só dele, pra bater o ponto pelo celular, sem senha. E se quiser, defina um PIN de quatro ou seis números: aí só ele bate o ponto dele. |
| Na lista, menu "…" do Gabriel → "Copiar link do ponto": aviso "Link copiado". | Pra mandar o link, é no menu dele: Copiar link do ponto. |
| [ILUSTRAÇÃO: o link vai pro celular: o link sai do computador como um envelope e pousa num celular genérico, sem marca de aplicativo, com o nome "Gabriel" na tela] | Aí é só enviar pro celular do Gabriel, por mensagem. |
| Aba "Configurações de Ponto"; desce até o cartão "Ativar ponto eletrônico" ("Marque quem vai bater ponto. ..."), com "Rafael Nogueira", "Juliana Prado" e "Rogério Batista"; marca "Juliana Prado"; clique em "Ativar ponto (1)": aviso "1 funcionário com ponto ativado". [BACKEND: RPC `bulk_enable_ponto` (Juliana → `juliana-prado-8w3n`); vira `apos-cap08`] | Pra ligar o ponto de quem já estava cadastrado, tem um atalho aqui, em Configurações de Ponto. A Juliana, do escritório, vai começar a bater ponto: marco ela e clico em Ativar ponto. |
| Sobe até o cartão "Tablet da empresa": o QR Code, o link `/ponto/empresa/recicla-vale-metais-2h6p`, "Copiar link" e "Baixar QR code", sem clicar. [BACKEND: RPC `get_or_create_ponto_kiosk_slug`] | E aqui em cima fica o outro link, o do tablet da empresa. Ele é um só, com a lista de todo mundo, pra ficar num tablet na entrada do pátio. |
| [ILUSTRAÇÃO: dois links: à esquerda, três celulares, cada um com um link e um nome (Gabriel, Diego, Juliana); na palavra "tablet", à direita, entra um tablet único com a lista da equipe; na palavra "ninguém", um cadeado aparece entre o tablet e os links pessoais] | Uma dica: são dois links diferentes. O pessoal é um por funcionário, pro celular dele. O do tablet é um por empresa. E o tablet não mostra o link pessoal de ninguém. |

### cap09 · O ponto pelo celular (vinheta: PONTO ELETRÔNICO)

| Tela | Fala |
| --- | --- |
| Celular, sem login, em `/ponto/gabriel-rocha-4f7k`: cabeçalho verde com "GR", "Gabriel Rocha" e "Ajudante de pátio"; "Recicla Vale Metais" e a data; "PONTO ELETRÔNICO"; no rodapé, "Você ainda não bateu o ponto hoje" e o relógio correndo. [BACKEND: semente `apos-cap08`; edge `time-clock-portal` (`get_state`)] | No celular do Gabriel, o link abre direto a tela do ponto, com o nome dele, a empresa e o relógio. |
| Toque em "Registrar Entrada": janela "Registrar Entrada" · "Confirme localização e selfie para registrar o ponto"; "Obtendo sua localização...". [BACKEND: passo `geo` em -23.0105, -45.5412; Nominatim interceptado (plano.md)] | Ele toca em Registrar Entrada. Primeiro, o celular pega a localização. |
| Tela "Selfie do ponto" · "Centralize o rosto para a selfie", com a câmera no círculo; toque em "Tirar foto agora". [BACKEND: câmera falsa do Chromium com o avatar ilustrado, nenhum rosto real] [TESTAR: com o avatar, o guia pode ficar em "Posicione seu rosto dentro da moldura"] | Depois vem a selfie. Ela sai sozinha quando o rosto fica no centro, ou é só tocar em Tirar foto agora. |
| Confirmação: "Tipo" "Entrada", "Horário", "Local" "Rua Projetada Doze, 1450 - Parque Industrial Vale Verde - Taubaté" e a miniatura da selfie. [ZOOM: "Horário" e "Local", a frase toda] | Na confirmação aparecem o tipo, o horário, o local e a foto. Assim a empresa sabe quando e de onde ele bateu. |
| Toque em "Confirmar registro": aviso "Ponto registrado"; "Registros de hoje" com "Entrada" e a hora; no rodapé, "Trabalhando" e os botões "Iniciar Intervalo" e "Registrar Saída". [BACKEND: `register_punch` grava `time_records` com a hora do servidor, `source` link_publico, foto no `time-photos`; vira `apos-cap09`] | Confirmar registro. Pronto, a entrada está gravada, e os próximos botões já aparecem: o intervalo e a saída. |
| [ILUSTRAÇÃO: a hora do sistema: um celular com o relógio marcando 7:25, riscado; ao lado, a batida carimbada "Entrada 7:02, horário da empresa", saindo de um relógio do sistema; na palavra "bagunça", o carimbo fica e o relógio do celular some] | Uma dica: quem marca a hora é o sistema, no horário da empresa, e não o relógio do celular. Celular com a hora errada não bagunça o registro. |

### cap10 · Registro e folha de ponto (vinheta: PONTO ELETRÔNICO)

| Tela | Fala |
| --- | --- |
| (o `setup` abre a aba "Folha de Ponto" e escolhe "Cláudio Ribeiro" fora do vídeo; plano.md, risco 1) A folha de novembro de 2026 do Cláudio: "Data", "Entrada → Saída", "Trabalhado", "Saldo", "Status" e "Ações"; 02/11 "Feriado" (Finados), dias "Completo", 05/11 "Falta" e hoje "Em andamento". [BACKEND: semente `apos-cap09`] | Do lado do gestor, a Folha de Ponto mostra o mês de cada um, dia a dia. Aqui, o do Cláudio: entrada e saída, as horas trabalhadas e o saldo de cada dia. |
| Zoom na linha de 05/11/2026, com o status "Falta" e o botão "Lançar". [ZOOM: a linha de 05/11, a fala toda] | Repara no dia cinco: Falta, e ninguém lançou nada. Uma dica: dia útil que já passou, sem batida e sem ausência lançada, aparece como falta sozinho. |
| [ILUSTRAÇÃO: a falta que aparece sozinha: o calendário da semana; os dias com batida ganham um visto verde; o dia cinco, vazio, ganha o selo "Falta"; na palavra "justificar", um papel de atestado pousa nele e o selo troca para "Atestado"] | É assim que a falta vira uma linha pra você justificar. |
| Clique em "Lançar": "Lançar ausência" · "Registre quem não veio: férias, atestado, falta, folga ou feriado"; "Funcionário" travado no Cláudio; em "Tipo *", "Atestado"; datas 05/11/2026 ("1 dia de ausência"); em "Observação", "Consulta médica"; clique em "Lançar ausência": aviso "Ausência lançada"; a linha vira "Atestado". [BACKEND: `INSERT employee_absences` (atestado, 05/11) e o recálculo da `time_sheets` do dia; vira `apos-cap10`] | O Cláudio trouxe atestado. Em Lançar, escolho Atestado e coloco a observação. Lançar ausência, e o dia vira Atestado. |
| Zoom no rodapé "Total do mês" ("0 falta(s) · 0 de férias · 1 com atestado") e no aviso "1 dia(s) sem saída registrada não entram no saldo". | No rodapé fica o total do mês. E repara no aviso: hoje ainda não tem saída, então o dia de hoje fica fora do saldo até ele bater a saída. |
| Clique em "Exportar": "Exportar Folha de Ponto", com "Espelho de Ponto (PDF)" e "Planilha para contabilidade (Excel)"; zoom em "Não substitui arquivos fiscais AEJ ou AFD."; clique em "Cancelar". | Pra levar o mês pro contador, tem o Exportar: o espelho de ponto em PDF ou a planilha. A planilha é pra conferência e não substitui os arquivos fiscais do ponto. |
| Aba "Registro de Ponto", em "Hoje": as batidas de hoje por pessoa (a Juliana com "Ainda não bateu ponto hoje"); zoom no cartão do Gabriel: a miniatura da selfie, "Entrada", a hora, o endereço e "Mobile - Chrome". [BACKEND: edge `time-photo-url` para as miniaturas] | E no Registro de Ponto ficam as batidas, uma por uma. A do Gabriel está aqui, com a selfie, a hora e o endereço. |
| Zoom no botão "Lançar manual". | Se alguém esquecer de bater, o Lançar manual registra por ele, e a batida fica marcada como Manual. |

### cap11 · Configurações do ponto (vinheta: PONTO ELETRÔNICO)

| Tela | Fala |
| --- | --- |
| Aba "Configurações de Ponto", cartão "Jornada Padrão da Empresa"; zoom em "Exigir selfie" ("Foto obrigatória a cada batida de ponto.") e "Exigir localização" ("Geolocalização obrigatória a cada batida."), os dois ligados. [BACKEND: semente `apos-cap10`] | Nas Configurações de Ponto ficam as regras. Com Exigir selfie e Exigir localização ligados, toda batida precisa da foto e do local. É assim que a Recicla Vale Metais usa. |
| Zoom em "Entrada padrão" 07:00, "Saída padrão" 16:00, "Intervalo padrão (min)" 60 e "Tolerância de atraso (min)" 10. | Embaixo, a jornada da empresa: entrada às sete, saída às quatro da tarde, uma hora de intervalo e dez minutos de tolerância de atraso. |
| Zoom em "Dias em que a empresa trabalha", com "Seg" a "Sex" ligados. | E os dias em que a empresa trabalha, de segunda a sexta. Dia desmarcado não gera falta. |
| Desce até "Jornada Individual": a tabela com cada um e os horários herdados em cinza; clique no lápis da "Juliana Prado": "Jornada — Juliana Prado" · "Sobrescreve o padrão da empresa para este funcionário.". | Quem tem outro horário ganha uma jornada individual. A Juliana, do escritório, entra às oito e sai às cinco. |
| De "Seg" a "Sex": entrada 08:00 e saída 17:00, intervalo 60 (trecho acelerado, selo 4x); clique em "Salvar jornada": aviso "Jornada salva"; na tabela, a linha dela mostra "08:00-17:00 (1h int.)". [BACKEND: RPC `save_employee_time_schedules`; vira `apos-cap11`] | No lápis dela, troco os horários de segunda a sexta e deixo uma hora de intervalo. Salvar jornada, e a folha dela passa a esperar esse horário. |
| [ILUSTRAÇÃO: jornada da empresa × individual: uma régua de horas de segunda a sexta com a faixa da empresa, das sete às quatro; na palavra "vence", a faixa da Juliana, das oito às cinco, desce por cima só na linha dela] | A jornada individual vence a da empresa só pra aquela pessoa. O resto da equipe segue no horário padrão. |

### cap12 · Arquivar ou excluir (vinheta: FUNCIONÁRIOS)

| Tela | Fala |
| --- | --- |
| Aba "Funcionários"; clique em "Rogério Batista": "Ajudante de pátio" e "Último pagamento" 30/10/2026. [BACKEND: semente `apos-cap11`] | Por último, quem sai da empresa. O Rogério, ajudante, saiu no fim de outubro e já recebeu tudo. |
| Abre o menu "…" do Rogério, com "Arquivar" em destaque, sem clicar ainda. | Uma dica: se a pessoa batia ponto, desligue o ponto eletrônico no cadastro dela antes de arquivar. Assim o link pessoal para de funcionar. O do Rogério já está desligado. |
| Clique em "Arquivar": aviso "Funcionário arquivado" · "O funcionário foi movido para inativos. O histórico foi mantido."; ele sai da lista. | Então é só Arquivar. Ele sai dos ativos, e o histórico fica guardado: os vales, os pagamentos e o extrato. |
| Clique em "Inativos": o Rogério aparece; abre o menu "…": "Reativar", "Excluir definitivamente" e "Extrato". | Ele fica em Inativos. Se voltar a trabalhar, é só Reativar. |
| Clique em "Excluir definitivamente": diálogo "Excluir definitivamente" · "Atenção: esta ação é irreversível. Todo o histórico de movimentações de Rogério Batista (vales, bônus, faltas e pagamentos) será apagado permanentemente. Não há como desfazer." [ZOOM: o texto do diálogo] | Já o Excluir definitivamente apaga a pessoa e todo o histórico dela, sem volta. Ele é pra cadastro feito por engano. |
| [ILUSTRAÇÃO: arquivo × lixeira: à direita, uma lixeira em que uma ficha e um extrato somem (o Excluir); na palavra "Arquivar", entra à esquerda uma caixa-arquivo com a ficha e o extrato do Rogério dentro; na palavra "voltar", uma seta de volta, "Reativar"] | Pra quem saiu, o caminho é Arquivar: a ficha fica guardada e pode voltar. |
| Clique em "Cancelar"; o Rogério segue em "Inativos". [vira `apos-cap12`] | Então, aqui, Cancelar. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cadastro do Gabriel e o "Custo total mensal" R$ 3.361,00. | Pronto! Recapitulando: a gente cadastrou o Gabriel com o salário, o custo mensal e a chave Pix, e preencheu os campos de folha do regime CLT. |
| Montagem rápida: o departamento "Transporte"; o vale e a falta do Diego; o bônus do Cláudio. | Criou o departamento Transporte, lançou o vale e a falta do Diego e o bônus do Cláudio. |
| Montagem rápida: "Recebimento confirmado!", "Realizar Pagamento" e o "Extrato - Edson Moura". | Recebeu a sobra do vale do Edson, fez o pagamento dele e conferiu tudo no extrato. |
| Montagem rápida: "Copiar link do ponto", o celular com "Ponto registrado" e a "Folha de Ponto" com "Atestado". | Ligou o ponto eletrônico, viu o Gabriel bater a entrada pelo celular, justificou a falta do Cláudio e ajustou a jornada da Juliana. |
| Montagem rápida: "Inativos" com o Rogério. | E arquivou o Rogério, sem perder nada do histórico. |
| Cartão "Próximo: White Label"; cartela final. | No próximo tutorial, a gente deixa o sistema com a marca da sua empresa. Até lá! |
