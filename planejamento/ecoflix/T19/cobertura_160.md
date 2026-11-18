# Cobertura 1.60.10 · T19 Funcionários e ponto eletrônico

Auditoria só de leitura (18/11/2026). Código: `/dev/shm/ecoflix-src` (1.60.10), diff `f37573ea0..5290be4cd`. Caminhos relativos a
`src/`. Rótulos entre aspas = texto exato do código. Não há varredura do robô para a T19 (`rec/varredura/` só tem t00 a t05).

Resumo do diff nas telas da aula: mudaram `EmployeePaymentModal.tsx` (+416 linhas, redesenho), o novo
`funcionarios/PayrollAdjustmentsEditor.tsx`, `utils/payrollTables.ts` e `payrollDeductions.ts` (tabelas oficiais de 2026), a troca
de "Vale" por "Vale/Adiantamento" em seis arquivos, e a calculadora de custo (salário mínimo de referência). **Não mudaram**:
`pages/Employees.tsx`, `EmployeeFormDialog.tsx`, departamentos, todas as abas do ponto (`funcionarios/ponto/*`),
`PontoScreen.tsx`, `PontoKiosk.tsx`, a edge `time-clock-portal` e o `employees.json`. Os caps. 0, 2, 3, 4, 8, 10, 11 e 12 batem
com o 1.60.10 como estão. As notas de versão 1.59.155 a 1.60.10 (`config/version.ts:19-113`) não citam nada desta aula.

## 1. Mudou no app (por capítulo)

### cap01 · A tela Funcionários
1. Ficha, "Resumo financeiro": o item "Vales" virou **"Vales/Adiantamentos"** (`components/EmployeesListView.tsx:387`). Os botões
   de "Movimentações" continuam "Vale", "Bônus", "Falta", "Recebimento", "Pagamento" (`:372-376`) e o menu "…" continua "Vale".
   A fala não cita o rótulo; só a coluna Tela muda.

### cap05 · Vale, bônus e falta
2. Título da janela: "Registrar Vale" virou **"Registrar Vale/Adiantamento"** (`components/EmployeeMovementModal.tsx:53`). O
   subtítulo é o mesmo.
3. Aviso de sucesso: "Movimentação registrada" · **"Registrar Vale/Adiantamento registrado com sucesso"** (`:265-266`; segue
   duplicado, continua sem zoom).
4. A janela do vale ficou mais larga (`sm:max-w-2xl`, `:365`), a origem escolhida ganha borda escura e fundo (`:406,420`) e o
   botão "Confirmar" ficou preto (`:347`). O "Saldo: R$ 1500.00" com ponto continua (`:413`).
5. Erros: "Abra o caixa antes de registrar Vales/Adiantamentos em dinheiro" (`:325`) e "Para registrar um Vale/Adiantamento,
   informe se a saída é em dinheiro ou PIX" (`:315`).
6. Zoom do "Resumo financeiro" (linhas 4 e 6 do capítulo): "Vales" R$ 200,00 agora é "Vales/Adiantamentos" R$ 200,00 (item 1).

### cap06 · Pagar e receber
7. "Receber do Funcionário": "Vales pendentes:" virou **"Vales/Adiantamentos pendentes:"** (`components/EmployeeReceivementModal.tsx:304`);
   no sucesso, "Vales antes" e "Vales restantes" viraram **"Vales/Adiantamentos antes"** e **"Vales/Adiantamentos restantes"**
   (`:253,261`). "Máximo: R$ 500,00 (total de vales pendentes)" não mudou (`:324`).
8. "Realizar Pagamento" foi redesenhado (`components/EmployeePaymentModal.tsx`): janela larga (`sm:max-w-6xl`, `:964`) em duas
   colunas fixas. O painel flutuante "Resumo do funcionário" sumiu; no lugar, um cartão à direita com o título **"Resumo do
   pagamento"** (`:1313-1317`; em tela estreita ele vem primeiro, no topo). O `[TESTAR]` do painel flutuante deixa de valer.
9. Ordem dos blocos da coluna esquerda: "Modo de pagamento" (`:984`) → bloco dos vales → (só no CLT) "Proventos e descontos
   desta folha" e "INSS desta folha" → valor → "Data e hora do pagamento" → "Forma de Pagamento" → conta → "Observações (opcional)".
10. Bloco dos vales: "Quanto você quer descontar dos vales" e "Valor padrão: 100% dos vales (R$ 400,00)" não existem mais. Agora:
    título **"Vales/Adiantamentos desta folha"** · "Defina quanto do saldo em aberto será descontado neste pagamento." · selo
    **"Em aberto: R$ 400,00"** · campo **"Desconto neste pagamento"** · "Começa com 100% do saldo, mas você pode descontar menos e
    deixar o restante para a próxima folha." (`:999-1031`). O campo não aceita mais do que o saldo em aberto: ao sair dele, volta
    para o máximo (`utils/payrollPayment.ts:2-6`, `:1019-1023`).
11. Campo do valor: "Valor efetivamente pago" virou **"Valor líquido do pagamento"**, com o número grande (`:1091-1104`).
    "Calculado: R$ 2.750,00" e o link "voltar ao calculado" continuam (`:1107-1124`). A mensagem do rodapé ainda diz "valor
    efetivamente pago" (`:915-921`).
12. Resumo no modo "Normal": "Salário:", "Total de Bônus:", "Descontos:", **"Vales/Adiantamentos:"**, "Faltas:" (`:868-872`).
13. Resumo no modo "CLT (com folha)": "Proventos (bruto)" saiu. Agora: "Folha CLT", "Salário base", "+ Adicional", "+ Bônus",
    "+ {provento extra}", **"Total de proventos"**, "- INSS", "- IRRF", "- Vale-transporte", "- Faltas", "- Vales/Adiantamentos",
    "- {desconto extra}", **"Total de descontos"**, "Líquido" e "Valores estimados; confirme com seu contador." (`:840-864`).
14. A folha CLT usa as tabelas oficiais de 2026 (INSS da Portaria 13/2026, IRRF com a redução da Lei 15.270/2025, salário mínimo
    R$ 1.621,00; `utils/payrollTables.ts:5-9,73-93`). O risco 7 do plano (tabela de 2026 = 2025) acabou: os valores do modo CLT já
    podem aparecer com zoom. No relance do Edson (bruto R$ 3.150,00): "- INSS" R$ 266,60, "- IRRF" R$ 0,00, "Líquido" R$ 2.483,40.
    `[TESTAR]`. Competência sem tabela bloqueia: "Não há tabela oficial cadastrada para a competência MM/AAAA. O pagamento CLT foi
    bloqueado para não calcular impostos com valores antigos." (`:901-904`).
15. "Forma de Pagamento" em grade de duas colunas, opção escolhida com borda escura, "Pagamento Misto" na linha de baixo
    (`:1207-1244`); "Confirmar Pagamento" preto (`:948`).
16. Sobra de vale depois do pagamento: a linha criada se chama **"Vales/Adiantamentos restantes do período anterior"** (`:737`).

### cap07 · Extrato
17. Cartão "Vales" virou **"Vales/Adiantamentos"** (`components/EmployeeExtract.tsx:1198`).
18. O selo das linhas de vale virou **"Vale/Adiantamento"** (`utils/employeeCalculations.ts:397`, usado em
    `EmployeeExtract.tsx:1046,1307`).
19. Detalhe do pagamento: **"Total de Vales/Adiantamentos acumulados"** e **"Vales/Adiantamentos descontados neste pgto"**
    (`:933,940`). O recibo impresso segue igual: "Valor do Vale/Adiantamento", "Vales/Adiantamentos restantes (não descontados)"
    (`utils/employeeReceiptHtmlGenerator.ts`).

### cap09 · Ponto pelo celular
20. Sem mudança de texto. Só correção interna na selfie (`components/ponto/CenteredSelfieCapture.tsx:48-74`). No tablet, o
    reconhecimento pede só o rosto de frente (`components/ponto/FaceCaptureExperience.tsx:62-65`); não aparece na aula atual.

### Fala que precisa trocar por causa do item 1 a 19
- cap05 linha 2: "No botão Vale, a origem já vem em Dinheiro" → "O botão Vale abre o Registrar Vale/Adiantamento, e a origem já
  vem em Dinheiro, do caixa." (dá nome ao que a tela mostra).
- cap06 linha 4: "Aqui você escolhe quanto dos vales desconta agora. O padrão é tudo, os quatrocentos." segue válida; só a Tela
  muda (item 10). cap06 linha 6: trocar o início por "O valor líquido do pagamento fica em dois mil setecentos e cinquenta".
- cap06 linha 5 (modo CLT): pode ganhar os números (item 14), ver proposta B.

## 2. Falta cobrir

| # | O que é (código) | Quando o cliente usa | Vale? |
|---|---|---|---|
| L1 | **Folha CLT completa**: "Proventos e descontos desta folha" com "Adicionar rápido" ("Horas extras 50%", "Horas extras 60%", "DSR sobre horas extras", "Comissão"), "Proventos extras", "Descontos extras", chave "Compõe as bases de INSS, IRRF e FGTS" (`funcionarios/PayrollAdjustmentsEditor.tsx:22-27,109,132-172`); "INSS desta folha" com "Novo valor" e "Motivo do ajuste" (`EmployeePaymentModal.tsx:1043-1085`); "Gerar Holerite" no extrato (`EmployeeExtract.tsx:1096,1365`) | Todo mês, em quem é registrado: hora extra, comissão, empréstimo, INSS já recolhido em outro vínculo | **Sim, capítulo novo** (novidade do 1.60, e o cap03 hoje prepara campos que a aula nunca usa) |
| L2 | **Férias, 13º e rescisão**: menu "…" → "Pagar férias", "Pagar 13º salário", "Pagar rescisão" (`EmployeesListView.tsx:283-291`); janela "Pagar Férias" etc. com o aviso "é uma verba de competência própria ... não altera o saldo de salário em aberto" (`EmployeeCompetenceMovementModal.tsx:64-75,381-387`) | Fim de ano, férias, desligamento. Quem lança como bônus bagunça o saldo | **Sim, capítulo novo** |
| L3 | **Pagar valor diferente do calculado**: "Motivo da diferença" com "Produção", "Gratificação", "Benefício pago em dinheiro", "Acerto", "Outro" (`EmployeePaymentModal.tsx:69-75,1141-1168`); selo "+ R$ X a mais" / "- R$ X a menos"; diálogo "Confirme o valor do pagamento" quando a diferença passa de 30% ou de R$ 2.000 (`:420-423,1326-1378`) | Mês com produção por fora, acerto, arredondamento | **Sim, trecho no cap06** (hoje só uma frase) |
| L4 | **Pagamento sem saída de dinheiro**: vales comeram o salário → diálogo "Pagamento sem saída de dinheiro" / "Confirmar mesmo assim" (`:1380-1404`); sem vale e valor zero → botão travado com "O valor a pagar está zerado e não há vales a descontar. Confira o valor antes de confirmar." (`:906-912`) | Funcionário que pegou vale demais | Só citar (uma frase no trecho L3) |
| L5 | **"Pagamento Misto"** (parte em dinheiro, parte em Pix, um campo completa o outro, `:1263-1298,428-449`) e **"Data e hora do pagamento"** retroativa · "Por padrão é agora. Pode mudar pra registrar pagamento retroativo." (`:1186-1202`) | Paga metade em dinheiro; lança hoje o pagamento de ontem | **Sim, trecho no cap06** |
| L6 | Vale por "PIX/Transferência (Banco)" e o seletor "Qual caixa?" com mais de um caixa aberto (`EmployeeMovementModal.tsx:419-430`) | Vale por Pix | Só citar no cap05 (uma frase) |
| L7 | **"Exportar Relatório"** → "Relatório de Funcionários": modelos "Relatório de movimentações" · "Detalha vale, bônus, falta e pagamento no período escolhido." e "Relação de pagamento" · "Salário, saldo em aberto e quanto pagar a cada funcionário hoje."; "Período", "O que incluir", "Funcionários incluídos", "Marcar todos", "Excel", "Visualizar / PDF" (`EmployeesRhReportDialog.tsx:709-836,685-693`) | Fechar a folha num PDF só, mandar pro contador | **Sim, capítulo curto** (o cap01 só aponta o botão) |
| L8 | **Aba "Ausências"**: lista com "Funcionário", "Tipo", "Período", "Dias", "Observação", "Ações"; "Lançar ausência"; filtro "Todos os funcionários"; editar, excluir ("Excluir ausência"), clipe de anexo (`funcionarios/ponto/AusenciasTab.tsx:126-330`) | Lançar férias de 30 dias de uma vez; conferir quem está afastado | **Sim, trecho no cap10** (a aba é citada no cap01 e nunca aberta) |
| L9 | **"Lançar manual" de verdade**: "Lançar registro manual" · "Crie um registro de ponto manualmente. Não exige foto nem localização."; "Funcionário *", "Tipo *", data e hora, "Observação", "Lançar" → "Registro manual lançado" (`PunchManualDialog.tsx:183-292`); no cartão da batida, menu "Editar" ("Editar registro de ponto", selo "Editado" com o horário original) e "Excluir" ("Excluir batida?" · "A foto e a localização continuam guardadas, mas a batida some da lista e da folha de ponto.", `RegistroPontoTab.tsx:356-376,465-476`); filtros "Hoje", "Semana", "Mês" (`:84-86`) | Esqueceu de bater; bateu errado | **Sim, trecho no cap10** (hoje é só um zoom no botão) |
| L10 | **Folha, visão "Todos os funcionários"**: tabela "Funcionário", "Dias com registro", "Trabalhado", "Esperado", "Saldo", "Faltas", "Férias", "Atestado", linha "Total" (`EspelhoPontoTab.tsx:742-780`); **"Composição do saldo"**: "Horas positivas (extras)", "Horas negativas (atrasos/faltas)", "Saldo líquido" (`:162-173`) | Ver o mês da equipe inteira; saber se o saldo é hora extra ou atraso | **Sim, trecho no cap10** (resolve com dado: ver "mundo") |
| L11 | **O dia inteiro no celular**: "Iniciar Intervalo", "Voltar do Intervalo", "Registrar Saída", estados "Em intervalo" e "Jornada concluída", e **"Registrar Nova Entrada"** para uma segunda jornada no mesmo dia (`components/ponto/PontoScreen.tsx:116-125,146-149`); localização negada: "Tentar novamente" (`:984`) | Todo dia | **Sim, trecho no cap09** (a aula só bate a entrada) |
| L12 | **PIN de verdade**: "Definir PIN" → "Novo PIN", "Repita o PIN", "4 ou 6 dígitos numéricos."; depois "PIN definido. O funcionário digita antes de bater o ponto."; "Trocar PIN", "Remover PIN" (`funcionarios/ponto/PontoPinField.tsx:51-125`); no celular, teclado do PIN antes da tela do ponto (`components/ponto/PinGate.tsx`) | Link que pode cair na mão de outro | **Sim, trecho no cap08** (hoje só zoom, sem clicar) |
| L13 | **Tablet da empresa em uso** (`pages/PontoKiosk.tsx`): abre na câmera; "Buscar manualmente" → lista com "Buscar funcionário" e ordem "A–Z" / "Quem falta" (`:63-66,419,481`); cadeado "Protegido por PIN" no cartão; depois da batida, tela "Entrada registrada" com a hora e "Voltar agora" (`:57-60,286`) | Pátio com um tablet na entrada | **Sim, capítulo novo** (o cap08 mostra o link e nunca a tela) |
| L14 | **Reconhecimento facial**: no cadastro, "Reconhecimento facial" · "O funcionário faz uma única ativação guiada pelo celular." · "A foto não é salva. O aparelho envia apenas uma referência matemática protegida." · "Gerar link de ativação" · "Excluir biometria" (`funcionarios/ponto/FaceBiometricsField.tsx:77-112`); na configuração, "Exigir reconhecimento facial no quiosque" · "Desligado por padrão. Ao ligar, a busca manual só aparece se a câmera ou o reconhecimento ficarem indisponíveis." (`ConfigPontoTab.tsx:385-389`) | Tablet sem ninguém digitar o nome | **Só citar** (dentro de L13): gravar exige um rosto, e a aula não usa rosto real. Depende de decisão |
| L15 | Configurações de Ponto: **"Batidas da madrugada contam para o dia anterior até"** · "Quem entra à noite e sai depois da meia-noite tem as horas somadas no dia em que começou a trabalhar." (`ConfigPontoTab.tsx:456-466`); "Folga" num dia da jornada individual e a dica "Pra tirar o sábado de uma pessoa só, edite a jornada dela." (`:521,919`) | Turno da noite; quem não trabalha sábado | **Sim, duas frases no cap11** |
| L16 | **Configurações de RH** (`funcionarios/ConfigRhTab.tsx`): "Automação da folha" · "Gera uma previsão agregada em Contas a Pagar. Valores individuais continuam restritos ao RH." (`:214-217`); "Regra padrão para novos funcionários"; "Faltas na projeção"; "Regras de pagamento" + "Nova regra" (ciclo, "Vencimento do saldo", "Adiantamento separado" · "Ex.: 40% no dia 20 e o restante no vencimento."); "Competências" ("Projetada", "Fechada", "Paga"; "Atualizar projeções"; "Fechar esta folha?"); no cadastro, "Regra da folha" (`EmployeeFormDialog.tsx:826`); no pagamento, o aviso "Pagamento ligado à folha projetada" · "A conta agregada em Contas a Pagar será baixada automaticamente." (`EmployeePaymentModal.tsx:968-977`) | Quem quer a folha prevista no Contas a Pagar | **Sim, capítulo novo**, mas **depende de decisão**: no mundo a automação está desligada e ligar muda o Contas a Pagar da T13 |
| L17 | Calculadora de custo: "Adicional" ("Nenhum", "Periculosidade", "Insalubridade" com "Grau mínimo (10%)", "Grau médio (20%)", "Grau máximo (40%)" e, novo, "Base federal de 2026: R$ 1.621,00." + "Usar valor federal", `MonthlyCostCalculatorModal.tsx:314-389`); benefícios ("Plano de saúde", "Plano odontológico", "Seguro de vida", "Transporte", "Refeição / alimentação"); "Treinamentos e NRs", "ASO / Saúde ocupacional", "Celular e internet"; "Horas trabalhadas por mês"; "Fator sobre o salário"; "Hora Homem (HH)" (`:401-513`); no extrato, "Provisões trabalhistas (mensal)" (`EmployeeExtract.tsx:1223`) | Função com adicional; saber o custo da hora | **Sim, trecho no cap02** (passar a câmera e ler; sem preencher, para o R$ 4.264,00 não mudar) |
| L18 | Lista: "Ordenar" ("Mais Antigos Primeiro", "Mais Recentes Primeiro", "Ordem Alfabética"), alternador de visão (lista ou cartões), "Selecionar Foto" | Equipe grande | Só citar no cap01 (uma frase) |
| L19 | Departamentos: lápis (editar) e lixeira ("Os funcionários deste departamento ficarão SEM departamento (não serão apagados).") | Reorganizar a equipe | Só citar no cap04 (uma frase) |
| L20 | "Gerar Recibo" aberto (recibo do pagamento e do vale) | Entregar comprovante | Só citar: já dito no cap07; o holerite da proposta A mostra o documento |
| L21 | Permissões "Criar, Editar e Excluir Funcionários" e "Excluir Funcionários" | Dar acesso ao RH | Não: é da T2 (Usuários e permissões). O cap01 já cita a do ponto |
| L22 | Casar o vale ou o pagamento com o extrato do banco (destino "Funcionário") | Conciliação | Não: é da T14 (Bancos, cofre e conciliação). O cap05 já remete |
| L23 | Baixa da conta de folha no Contas a Pagar | Com a automação ligada | Não: é da T13; aqui só o aviso (L16) |

## 3. Proposta

Tom igual ao da aula. Números por extenso só na fala. Capítulos novos entram com letra para não renumerar agora.

### A. Capítulo novo, depois do cap06 · "A folha de quem é CLT" (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| Clique em "Marcos Antunes" ("Regime" CLT, "Saldo atual" R$ 2.400,00); botão "Pagamento": "Realizar Pagamento" já abre com "Modo de pagamento" em "CLT (com folha)"; à direita, "Resumo do pagamento" com "Folha CLT". | Agora o pagamento de quem é registrado. O Marcos, o balanceiro, é CLT. Então o Pagamento dele já abre no modo CLT, com a folha do lado. |
| Em "Proventos e descontos desta folha", "Adicionar rápido": clique em "Horas extras 50%"; em "Proventos extras" aparece a linha "Horas extras 50%" com a chave "Compõe as bases de INSS, IRRF e FGTS" ligada; em "Valor em reais", 180,00. [ZOOM: a linha com R$ 180,00] | Em outubro ele fez hora extra. No Adicionar rápido, escolho Horas extras cinquenta por cento e coloco o valor já calculado: cento e oitenta reais. |
| Zoom na chave "Compõe as bases de INSS, IRRF e FGTS". | Uma dica: essa chave diz se o valor entra na conta do INSS, do imposto de renda e do fundo de garantia. Hora extra entra. Uma ajuda de custo, por exemplo, você deixa desligada. |
| Em "Descontos extras", "Adicionar desconto": "Descrição" = "Convênio farmácia", "Valor em reais" = 60,00. | Nos Descontos extras vai o que sai só nessa folha, como o convênio da farmácia: sessenta reais. |
| Zoom lento no "Resumo do pagamento": "Salário base" R$ 2.400,00, "+ Horas extras 50%" R$ 180,00, "Total de proventos" R$ 2.580,00, "- INSS" R$ 207,89, "- IRRF" R$ 0,00, "- Vale-transporte" R$ 144,00, "- Convênio farmácia" R$ 60,00, "Total de descontos" R$ 411,89, "Líquido" R$ 2.168,11. [ZOOM: "Líquido"] [TESTAR: os centavos do INSS] | Repara no resumo: dois mil quinhentos e oitenta de proventos. O sistema calcula o INSS pela tabela do ano, o imposto de renda, que aqui deu zero, e o vale-transporte, seis por cento do salário. Líquido: dois mil cento e sessenta e oito reais e onze centavos. |
| Zoom em "INSS desta folha" · "Calculado pela tabela oficial: R$ 207,89"; liga a chave: aparecem "Novo valor" e "Motivo do ajuste" ("Ex.: desconto já recolhido em outro vínculo"); desliga de novo. | Se o contador passar outro valor de INSS, é só ligar essa chave, digitar o novo valor e o motivo. Sem motivo, o sistema não deixa confirmar. Aqui eu deixo o calculado. |
| "Valor líquido do pagamento" 2.168,11; "Forma de Pagamento" em "PIX/Transferência"; "Confirmar Pagamento". | O valor líquido já vem preenchido. Pix, e Confirmar Pagamento. |
| Botão "Extrato" do Marcos: na linha "Pagamento", botão "Gerar Holerite"; clique: abre o holerite em nova aba, com "HORAS EXTRAS 50%" e "INSS (PROGRESSIVO)". [TESTAR: o robô captura a aba nova] | E no extrato, o pagamento de quem é CLT tem o Gerar Holerite: o documento com cada provento e cada desconto, pra entregar pro Marcos. |
| Zoom em "Valores estimados; confirme com seu contador." (cena do resumo, reaproveitada). | Uma dica: a folha daqui é uma estimativa pra você pagar certo e guardar o histórico. A folha oficial continua com o seu contador. |

Mundo: Marcos **sem** o pagamento de 09/11 na semente (motivo falado não precisa; hoje todos menos o Edson foram pagos); Marcos
com `dependents_count` 1, `vt_enabled` true, `vt_monthly_value` 220,00, sem `monthly_cost_breakdown`. Handlers: os do cap06
(`employee_movements`, `bank_transactions`, RPC de saldo) e a leitura de `companies` para o holerite. Conta: `payrollDeductions.ts:37-92`.

### B. Trechos no cap06 (Edson)

| Tela | Fala |
| --- | --- |
| (troca a linha 5) "CLT (com folha)": no "Resumo do pagamento", "- INSS" R$ 266,60, "- IRRF" R$ 0,00, "Líquido" R$ 2.483,40; volta para "Normal". | No modo CLT, o sistema calcula o INSS e o imposto de renda e mostra o líquido. O Edson é informal, então volto pro Normal. A folha CLT a gente vê já já, com o Marcos. |
| (depois da linha 6) Em "Valor líquido do pagamento", digita 2.900,00: selo "+ R$ 150,00 a mais", "Motivo da diferença" → lista "Produção", "Gratificação", "Benefício pago em dinheiro", "Acerto", "Outro"; escolhe "Gratificação"; depois clica em "voltar ao calculado". [ZOOM: o selo e o motivo] | Se nesse mês você pagar diferente, é só digitar. O sistema mostra quanto foi a mais ou a menos e pede o motivo: produção, gratificação, acerto. E essa diferença não vira saldo nem dívida. Aqui, volto ao calculado. |
| Zoom em "Data e hora do pagamento" · "Por padrão é agora. Pode mudar pra registrar pagamento retroativo."; depois em "Pagamento Misto" (clique: aparecem os campos "Dinheiro" e "PIX", `:1266-1284`; volta para "PIX/Transferência"). | Dá pra mudar a data, se o pagamento foi ontem. E no Pagamento Misto, uma parte sai do caixa e a outra do banco: você digita uma, e o sistema completa a outra. |
| Cartão discreto com o texto do diálogo "Pagamento sem saída de dinheiro" (cena curta com o Diego numa semente lateral, ou só a fala). | Uma dica: se os vales comerem o salário inteiro, o sistema avisa que nenhum dinheiro vai sair e pede pra você confirmar. |

### C. Capítulo novo, depois do A · "Férias, décimo terceiro e rescisão" (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| Menu "…" da "Juliana Prado": zoom em "Pagar férias", "Pagar 13º salário" e "Pagar rescisão". | Férias, décimo terceiro e rescisão têm lugar próprio, no menu de cada funcionário. |
| Clique em "Pagar férias": "Pagar Férias" · "Pagamento de férias (já com o terço constitucional, se for o caso). Não altera o saldo de salário em aberto."; zoom no aviso "Férias é uma verba de competência própria ... não altera o saldo de salário em aberto do funcionário." | A Juliana sai de férias em dezembro. Em Pagar férias, repara no aviso: esse valor sai do caixa ou do banco, mas não mexe no saldo de salário dela. |
| "Valor *" 3.733,33; "Forma de pagamento" em "PIX/Transferência (Banco)"; "Observação (opcional)" = "Período aquisitivo 2025/2026"; "Confirmar": aviso "Férias registrado" · "R$ 3.733,33 para Juliana Prado. O saldo de salário em aberto não foi alterado." [ZOOM: "Valor *"] | Coloco o valor que o contador passou, já com o terço: três mil setecentos e trinta e três reais e trinta e três centavos. Pix, uma observação, e Confirmar. |
| "Saldo atual" da Juliana segue R$ 2.800,00; "Extrato": linha com o selo azul "Férias". | O saldo dela continua igual, e no extrato as férias aparecem numa linha própria. |
| Menu "…" do "Cláudio Ferraz" → "Pagar 13º salário": "Pagar 13º Salário" · "... lance uma parcela por vez, com a data de cada uma."; "Valor *" 1.050,00; "Observação (opcional)" = "1ª parcela 2026"; "Confirmar". | O décimo terceiro é igual, uma parcela por vez. A primeira do Cláudio: mil e cinquenta reais. |
| [ILUSTRAÇÃO: três gavetas ao lado do balde "Saldo" do cap06: "Férias", "13º" e "Rescisão"; na palavra "bônus", uma nota que ia cair no balde desvia para a gaveta certa] | Uma dica: não lance férias nem décimo terceiro como bônus. O bônus entra no saldo do mês e bagunça a conta. E a rescisão, de quem sai da empresa, fica nesse mesmo menu. |

Mundo: nada novo na semente além do estado do capítulo A. Handlers: `INSERT employee_movements` com `type` "ferias" e
"decimo_terceiro"; `financial_categories` get-or-create "Férias" e "13º Salário" (`utils/payrollCategory.ts:39-43`);
`bank_transactions` e saldo da conta (`EmployeeCompetenceMovementModal.tsx:150-320`).

### D. Capítulo curto, depois do cap07 · "O relatório da equipe" (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Aba "Funcionários" → "Exportar Relatório": "Relatório de Funcionários"; "Modelo de relatório" com "Relatório de movimentações" e "Relação de pagamento". | Pra ver a equipe inteira num papel só, tem o Exportar Relatório, com dois modelos. |
| Em "Relatório de movimentações": "Período", "O que incluir" (os tipos), "Funcionários incluídos" com "Marcar todos". | O Relatório de movimentações lista os vales, os bônus, as faltas e os pagamentos do período que você escolher, de quem você marcar. |
| Clique em "Relação de pagamento" · "Salário, saldo em aberto e quanto pagar a cada funcionário hoje."; "Visualizar / PDF": abre o PDF com a equipe e o total. [ZOOM: o total] [TESTAR: aba nova] | E a Relação de pagamento mostra, hoje, quanto pagar a cada um e o total da folha. Sai em PDF ou em Excel. É o papel pra conferir antes do dia do pagamento. |

Mundo: nada novo (usa os movimentos já semeados). Handler: as leituras de `employees` e `employee_movements` do relatório
(`EmployeesRhReportDialog.tsx:380-430`) e `companies`.

### E. Trechos no cap08 e no cap09 (PIN e o dia inteiro)

| Tela | Fala |
| --- | --- |
| (cap08, troca a linha 2) Clique em "Definir PIN": "Novo PIN" 4107, "Repita o PIN" 4107; "Atualizar"; reabre: "PIN definido. O funcionário digita antes de bater o ponto." e os botões "Trocar PIN" e "Remover PIN". | Ligado, ele ganha um link só dele. E pra ninguém bater por ele, defino um PIN de quatro números. Se ele esquecer, é aqui que você troca ou remove. |
| (cap09, antes da linha 1) Celular: teclado do PIN; digita 4107. | No celular, primeiro ele digita o PIN. |
| (cap09, depois da linha 5, com o relógio do mundo em 11:00) Toque em "Iniciar Intervalo" (mesmo fluxo, acelerado, selo 4x): rodapé "Em intervalo" e o botão "Voltar do Intervalo". | Na hora do almoço, ele toca em Iniciar Intervalo, e na volta, em Voltar do Intervalo. |
| (relógio em 16:00) "Registrar Saída": rodapé "Jornada concluída", "Registros de hoje" com as quatro batidas e o botão "Registrar Nova Entrada". | No fim do dia, Registrar Saída, e a jornada fica concluída. Se ele voltar à noite pra um serviço extra, é só tocar em Registrar Nova Entrada: o sistema aceita mais de uma jornada no mesmo dia. |

Mundo: RPC `set_ponto_pin` e `has_ponto_pin` verdadeiro para o Gabriel; edge `time-clock-portal` validando o PIN e devolvendo
`allowed_actions` conforme a última batida (`PontoScreen.tsx:150-176`); o capítulo passa a precisar de três horas falsas
(08:30, 11:00, 16:00): ou três navegadores, ou a hora do servidor falso avançando por passo. O cap10 e o cap13 passam a mostrar
o Gabriel com o dia completo (ajustar a semente `apos-cap09` e o aviso "1 dia(s) sem saída", que continua valendo pelo Cláudio).

### F. Capítulo novo, depois do cap09 · "O tablet da empresa" (vinheta: PONTO ELETRÔNICO)

| Tela | Fala |
| --- | --- |
| Tablet (1024×768, sem login) em `/ponto/empresa/<slug>`: abre a câmera com o relógio e o nome da empresa; toque em "Buscar manualmente". | E quem não tem celular bate no tablet da empresa, aquele outro link. Ele abre a câmera pra reconhecer o rosto. Sem o rosto cadastrado, é só tocar em Buscar manualmente. |
| A lista da equipe em cartões, com "Buscar funcionário" e a ordem "A–Z" / "Quem falta"; toque em "Quem falta". | Aparece a equipe inteira, com quem já bateu e quem ainda falta. |
| Toque no cartão "Diego Morais" (já "Trabalhando"): tela do ponto dele, com "Voltar para a lista"; "Iniciar Intervalo" → selfie → "Confirmar registro": tela "Intervalo iniciado" com a hora e "Voltar agora". | O Diego toca no nome dele, bate o intervalo, e o tablet confirma com a hora e volta sozinho pra lista, pronto pro próximo. |
| Zoom no cadeado do cartão do Gabriel ("Protegido por PIN"). | Quem tem PIN aparece com o cadeado, e o tablet pede o PIN antes. |
| Desktop: "Configurações de Ponto", zoom em "Exigir reconhecimento facial no quiosque"; depois o cadastro, aba "Ponto eletrônico", bloco "Reconhecimento facial" · "Gerar link de ativação" e "A foto não é salva. ...". | Se quiser que o tablet reconheça todo mundo pelo rosto, cada um faz uma ativação pelo celular, com o link gerado no cadastro. A foto não é guardada. E essa chave aqui tira a busca por nome do tablet. |

Mundo: edge `time-clock-portal` com as ações do quiosque (`get_state` por `kioskSlug`, lista da equipe, `register_punch` com
`employeeId`); câmera falsa; `kiosk_require_face` falso; ninguém com biometria. Confirmar o tamanho de tela do tablet.

### G. Trechos no cap10 e no cap11 (gestor)

| Tela | Fala |
| --- | --- |
| (cap10, antes da linha 1) "Folha de Ponto" em "Todos os funcionários": "Funcionário", "Dias com registro", "Trabalhado", "Esperado", "Saldo", "Faltas", "Férias", "Atestado" e a linha "Total"; passa o cursor num saldo: "Composição do saldo" com "Horas positivas (extras)" e "Horas negativas (atrasos/faltas)". | A Folha de Ponto abre com o resumo do mês de toda a equipe. E passando o mouse no saldo, dá pra ver quanto é hora a mais e quanto é atraso ou falta. |
| (cap10, troca a linha 8) "Registro de Ponto" → "Lançar manual": "Lançar registro manual" · "... Não exige foto nem localização."; "Funcionário *" = Juliana Prado, "Tipo *" = "Entrada", hora 08:00, "Observação" = "Esqueceu de bater"; "Lançar": aviso "Registro manual lançado"; o cartão dela com o selo "Manual". | A Juliana esqueceu de bater hoje. No Lançar manual, escolho ela, o tipo, a hora e o motivo. A batida entra marcada como Manual. |
| No cartão da batida, menu "…": "Editar" e "Excluir"; zoom nos filtros "Hoje", "Semana", "Mês". | Batida errada dá pra editar, e ela fica com o selo Editado e o horário original guardado. E em cima, você vê o dia, a semana ou o mês. |
| Aba "Ausências" → "Lançar ausência": "Funcionário *" = Juliana Prado, "Tipo *" = "Férias", "Data de início" 07/12/2026, "Data de fim" 05/01/2027 ("30 dias de ausência", `AbsenceFormDialog.tsx:257`); "Lançar ausência"; a linha entra na tabela ("Tipo", "Período", "Dias"). | E na aba Ausências você lança um período inteiro de uma vez. As férias da Juliana, de sete de dezembro a cinco de janeiro. Nesses dias a folha dela mostra Férias, e não falta. |
| (cap11, depois da linha 2) Zoom em "Batidas da madrugada contam para o dia anterior até" (05:00). | Pra quem trabalha à noite: batida de madrugada, até esse horário, conta no dia em que o turno começou. |
| (cap11, na janela "Jornada — Juliana Prado") zoom numa chave de dia desligada, com "Folga". | E desligando um dia aqui, ele vira folga só pra essa pessoa. |

Mundo: para a visão "Todos os funcionários" não mostrar falta falsa (risco 1 do plano, que continua: `lib/ponto/folha.ts` não
mudou), o resumo é gravado **antes** de o Gabriel e a Juliana terem ponto, ou seja, com a semente `apos-cap06`; ou então aceita-se
abrir no Cláudio como hoje e mostrar o resumo só de relance. Handlers: `INSERT time_records` com `source` manual
(`PunchManualDialog.tsx:95-160`), `employee_absences` de período, leitura dos anexos vazia.

### H. Trechos pequenos (uma frase cada)

| Onde | Tela | Fala |
| --- | --- | --- |
| cap01, depois da linha 4 | Zoom em "Ordenar" e no alternador de visão. | Dá pra ordenar a lista e trocar pra visão em cartões. |
| cap02, depois da linha 7 | Na calculadora, a câmera passa por "Adicional" ("Periculosidade", "Insalubridade"), pelos benefícios e por "Horas trabalhadas por mês", sem preencher; no resumo, "Hora Homem (HH)". | Tem também o adicional de periculosidade ou insalubridade, os benefícios e as horas do mês. Com isso, a calculadora mostra até quanto custa a hora de trabalho dele. |
| cap04, depois da linha 3 | Zoom no lápis e na lixeira de um departamento. | No lápis você troca o nome, a cor e o ícone. Excluindo, ninguém é apagado: as pessoas só ficam sem departamento. |
| cap05, depois da linha 2 | Zoom em "PIX/Transferência (Banco)". | Se o vale for por Pix, escolha Banco, e ele sai da conta. |

### I. Capítulo novo, opcional · "Folha no Contas a Pagar" (vinheta: CONFIGURAÇÕES), antes do cap12

Só o esqueleto, porque depende de decisão (L16). Tela: aba "Configurações de RH" → "Regras de pagamento" → "Nova regra" ("Nome"
"Folha mensal", "Ciclo", "Vencimento do saldo" "Dia útil no mês seguinte", "Número do dia útil" 5, "Adiantamento separado") →
liga "Automação da folha" (diálogo "Ativar projeção automática?" · "Só funcionários atribuídos manualmente a uma regra entrarão
na folha. ...", "Ativar") → cadastro do Cláudio, "Regra da folha" → "Competências" com a folha "Projetada" → no pagamento, o
aviso "Pagamento ligado à folha projetada". Fala (resumo): "Se você quer ver a folha no Contas a Pagar antes de pagar, crie uma
regra de pagamento, ligue a automação e escolha a regra no cadastro de cada um. O sistema lança uma conta só, com o total, sem
abrir o salário de ninguém. Pagou o funcionário, a conta é baixada sozinha." Mundo: tabelas e RPCs da projeção
(`hooks/usePayrollProjection.ts`), que o backend falso ainda não tem.

## 4. Estimativa

| Proposta | Capítulos novos | Fala a mais |
|---|---|---|
| A. A folha de quem é CLT | 1 | ~93 s |
| B. Trechos do cap06 | 0 | ~50 s (troca uma linha de ~20 s) |
| C. Férias, 13º e rescisão | 1 | ~52 s |
| D. O relatório da equipe | 1 | ~27 s |
| E. PIN e o dia inteiro no celular | 0 | ~34 s |
| F. O tablet da empresa | 1 | ~46 s |
| G. Trechos do cap10 e do cap11 | 0 | ~58 s |
| H. Frases soltas | 0 | ~28 s |
| **Total sem o I** | **4** | **~390 s (6 min 30 s), 1.010 palavras a 2,6 palavras/s** |
| I. Folha no Contas a Pagar (opcional) | 1 | ~45 s |

Com 4 vinhetas, 1 ilustração nova, as esperas de tela (holerite, PDF, tablet) e os trechos acelerados, o vídeo vai de ~16 para
~24 min, em 18 capítulos. O cap13 (recapitulando) precisa de duas frases a mais (~10 s, fora da tabela).

## Depende de decisão
1. **Marcos sem o pagamento de 09/11** e com dependente e VT (proposta A): muda a semente `inicio` e o `MUNDO_FICTICIO.md`.
2. **Reconhecimento facial** (L14): só citar, como proposto, ou gravar com um rosto ilustrado (o motor pode não reconhecer um avatar).
3. **Automação da folha** (proposta I): entra nesta aula, vai para a T13 ou fica fora.
4. **Três horas falsas no cap09** (proposta E) e o tablet como terceiro formato de tela (proposta F).
5. Duração: a aula passa de 16 para cerca de 24 min; a alternativa é partir em duas (Funcionários e folha · Ponto eletrônico).
