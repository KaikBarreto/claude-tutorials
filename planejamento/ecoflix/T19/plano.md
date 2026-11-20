# Plano · T19 Funcionários e ponto eletrônico

- **Título:** Funcionários e ponto eletrônico (o da fonte). 🔒 módulo **Funcionários (RH)** (`funcionarios`).
- **Objetivo:** a equipe do pátio da Recicla Vale Metais dentro do sistema: cadastro e custo, vale, bônus, falta, pagamento,
  recebimento, extrato e o ponto eletrônico batido no celular e conferido pelo gestor.
- **Antes:** Relatório Financeiro e DRE (T15). **Próximo:** White Label (T27, "deixar o sistema com a sua marca").
- **Vinhetas (áreas):** FUNCIONÁRIOS · CADASTRO · CADASTRO · DEPARTAMENTOS · MOVIMENTAÇÕES · PAGAMENTO · PAGAMENTO · PAGAMENTO ·
  EXTRATO · RELATÓRIO · PONTO ELETRÔNICO (5 capítulos) · FUNCIONÁRIOS · RESUMO.
- **Versão 1.60.18 (20/11):** 18 capítulos (eram 14; "nenhuma aula se divide", mais profundidade). **Fala:** ~3.150 palavras,
  ~20 min de voz + vinhetas e ilustrações (≈ 24 a 25 min de vídeo). Tela 1600×900 (o cap. 13, tablet, 1024×768).
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) nos caps 0 a 12 e `2026-11-10T16:30:00-03:00` nos caps 13 a 17 (`rec/t19/fake_now.json`;
  a instância 54319 religa entre o 12 e o 13). Logado: Rafael Nogueira (MASTER), menu lateral recolhido. Cap. 12 no celular
  (`device: phone`, sem login, hora do ponto avançada por `__avanco_min` no falso), cap. 13 no tablet da empresa.
- Base: `T19/inventario.md` (código 1.59.154 + bloco "Atualização 1.60.18").

## Capítulos (numeração 1.60.18; os da fonte entre parênteses)

| # | Vinheta (área / título) | O que a tela mostra | Cuidados falados | Fala (estimada) |
|---|---|---|---|---|
| 0 | (sem vinheta) | Dashboard → menu "Funcionários (RH)"; [ILUSTRAÇÃO: o caderninho do pátio] | 🔒 · "Antes: Relatório Financeiro e DRE" | 0:49 |
| 1 | FUNCIONÁRIOS / A tela Funcionários e suas abas | As 7 abas; Ativos/Inativos; botões; lista "Equipe" com o saldo; ficha do Diego; "Dashboard" | ⚠️ abas do ponto só com "Gerenciar Ponto Eletrônico" | 1:17 |
| 2 | CADASTRO / Cadastrar o funcionário | Gabriel Rocha; calculadora do custo (Lucro Real, EPI, adicional, benefícios, horas, Hora Homem → R$ 4.264,00); Pix | ⚠️ estimativa → contador; saldo novo = salário | 1:54 |
| 3 | CADASTRO / Campos de folha | CLT, dependentes 1, VT R$ 220,00; [ILUSTRAÇÃO: Informal × CLT] | | 0:52 |
| 4 | DEPARTAMENTOS / Departamentos | "Transporte" (laranja, caminhão), lápis e lixeira, Edson nele, Filtros | | 0:48 |
| 5 | MOVIMENTAÇÕES / Lançar vale, bônus e falta | "Registrar Vale/Adiantamento" (Dinheiro ou Banco), falta, bônus; [ILUSTRAÇÃO: a conta do saldo] | ⚠️ não lançar o vale de novo no banco | 1:37 |
| 6 | PAGAMENTO / Pagar e receber do funcionário | Recebimento R$ 100,00; Pagamento largo: "Resumo do pagamento", "Vales/Adiantamentos desta folha", CLT de relance, "Valor líquido do pagamento", diferença + motivo, data, Pagamento Misto, Pix, recibo na aba nova; [ILUSTRAÇÕES: sem saída de dinheiro, recibo, ciclo] | ⚠️ pagou, zera | 2:32 |
| 7 | PAGAMENTO / A folha de quem é CLT (novo) | Marcos: folha CLT com horas extras 50%, convênio farmácia, INSS/IRRF/VT, líquido, ajuste do INSS, holerite na aba nova | ⚠️ folha estimada; a oficial é do contador | 1:51 |
| 8 | PAGAMENTO / Férias e décimo terceiro (novo) | Juliana: "Pagar férias" R$ 3.733,33; Cláudio: "Pagar 13º salário" R$ 1.050,00; rescisão citada | ⚠️ não lançar como bônus | 1:01 |
| 9 | EXTRATO / O extrato do funcionário (7) | Cartões, pagamento detalhado, Gerar Recibo (A4/Térmico, aba nova), ajuste de salário, lixeira | ⚠️ excluir desfaz o dinheiro | 1:07 |
| 10 | RELATÓRIO / O relatório da equipe (novo) | "Exportar Relatório": movimentações × Relação de pagamento (aba nova), PDF/Excel | | 0:32 |
| 11 | PONTO ELETRÔNICO / Ligar o ponto e gerar o link (8) | Ponto eletrônico do Gabriel + PIN 4107; Copiar link; Ativar ponto Juliana; Tablet da empresa | ⚠️ dois links | 1:21 |
| 12 | PONTO ELETRÔNICO / O ponto pelo celular (9) | PIN → Entrada, Iniciar/Voltar do Intervalo, Saída, Registrar Nova Entrada | ⚠️ a hora é a do sistema | 1:18 |
| 13 | PONTO ELETRÔNICO / O ponto no tablet da empresa (novo) | Tablet 1024×768: Buscar manualmente, lista, saída do Diego, cadeado do PIN; chave do reconhecimento facial | | 0:55 |
| 14 | PONTO ELETRÔNICO / Folha, registro e ausências (10) | Folha da equipe; Cláudio Falta → Atestado; Exportar; Registro; Lançar manual da Juliana; Ausências (férias) | ⚠️ falta sozinha; ⚠️ planilha não substitui fiscais | 1:59 |
| 15 | PONTO ELETRÔNICO / Configurações do ponto (11) | Selfie, localização, jornada, madrugada, dias; jornada da Juliana (intervalo por dia, folga) | | 1:18 |
| 16 | FUNCIONÁRIOS / Arquivar ou excluir (12) | Arquivar, Inativos, Reativar, Excluir; link pessoal arquivado = acesso desativado | dica: desligar o ponto antes | 1:00 |
| 17 | RESUMO / Recapitulando (13) | Montagem do que foi feito; cartão "Próximo: White Label" | | 1:13 |

Transições faladas: 0→1 "Vamos conhecer a tela"; 1→2 "Começando pelo cadastro"; 2→3 "Agora os campos de folha"; 3→4 "Pra
organizar a equipe"; 4→5 "Agora o dia a dia"; 5→6 "Hora de pagar"; 6→7 "Agora o pagamento de quem é registrado"; 7→8 "Férias,
décimo terceiro e rescisão têm lugar próprio"; 8→9 "Tudo isso fica guardado no Extrato"; 9→10 "Pra ver a equipe inteira num papel
só"; 10→11 "Agora o ponto eletrônico"; 11→12 "No celular, primeiro ele digita o pin"; 12→13 "E quem não tem celular bate no tablet";
13→14 "A Folha de Ponto abre com o resumo"; 14→15 "Nas Configurações de Ponto ficam as regras"; 15→16 "Por último, quem sai da empresa".

## Estado de partida (semente `inicio`)
Mundo base (`MUNDO_FICTICIO.md`) + o bloco abaixo. Ninguém pago hoje; todos pagos em 09/11 (5º dia útil), menos o Edson (na estrada
nesse dia). Caixa do Rafael aberto às 08:30 pela semente da aula (junção: no mundo base nenhum caixa abre em 10/11 antes das
08:31, como mostra a T6). Ponto em uso desde 01/09 pelo pátio (Marcos, Edson, Cláudio, Diego).

## Mundo: o que esta aula precisa
**Departamentos** (`employee_departments`): "Escritório" (#2563EB, `briefcase`), "Pátio" (#16A34A, `wrench`). Criado na aula:
"Transporte" (#EA580C, `truck`).

**Funcionários** (`employees`; e-mails `@reciclavalemetais.example`, o domínio do T2 (junção); telefones (12) 90000-41xx):

| Nome | Cargo | Depto | Admissão | Salário | Regime | CPF | Chave Pix | Ponto (slug) |
|---|---|---|---|---|---|---|---|---|
| Rafael Nogueira | Sócio-administrador | Escritório | 02/03/2015 | 6.000,00 | Informal | 274.913.508-79 (o do T18, junção) | rafael.nogueira@reciclavalemetais.example | não |
| Juliana Prado | Assistente administrativa | Escritório | 05/06/2023 | 2.800,00 | CLT | 362.918.470-78 | juliana.prado@reciclavalemetais.example | não (liga no cap. 11: `juliana-prado-8w3n`) |
| Marcos Antunes | Balanceiro | Pátio | 16/08/2021 | 2.400,00 | CLT | 305.672.148-26 | (12) 90000-4103 | sim (`marcos-antunes-7q2d`) |
| Edson Moura | Motorista | Pátio (Transporte no cap. 4) | 04/04/2019 | 2.900,00 | Informal | 251.847.396-37 | 251.847.396-37 | sim (`edson-moura-3k8f`) |
| Cláudio Ferraz | Ajudante de pátio | Pátio | 11/01/2022 | 2.100,00 | CLT | 334.095.127-64 | (12) 90000-4105 | sim (`claudio-ferraz-9m4t`) |
| Diego Morais | Ajudante de pátio | Pátio | 07/07/2025 | 1.980,00 | Informal | 447.103.682-36 | (12) 90000-4106 | sim (`diego-morais-5x1r`) |
| Rogério Batista | Ajudante de pátio (ex) | Pátio | 03/02/2025 | 1.980,00 | Informal | 392.660.514-62 | (12) 90000-4108 | não (desligado ao sair, 30/10) |
| **Gabriel Rocha** (cap. 2) | Operador de empilhadeira | Pátio | 10/11/2026 | 2.520,00 | Informal → CLT (cap. 3), 1 dependente, VT R$ 220,00 | 418.273.956-64 | (12) 90000-4107 | nasce ligado (`gabriel-rocha-4f7k`) |

Os dois ajudantes (Cláudio Ferraz e Diego Morais) são os nomes da T11 (coordenador, 10/11); se a T11 definiu outros documentos,
valem os dela. O operador de empilhadeira é o Gabriel, contratado na aula. Custo do Gabriel na calculadora: R$ 2.520,00 × 1,6722
(Lucro Real) + R$ 50,00 de EPI = **R$ 4.264,00**.

Telefones: Rafael 4101, Juliana 4102, Marcos 4103, Edson 4104, Cláudio 4105, Diego 4106, Gabriel 4107, Rogério 4108. Sem foto
(iniciais). Ninguém com custo mensal calculado, a não ser o Gabriel (cap. 2). "Automação da folha" desligada.

**Movimentos** (`employee_movements`, `balance_after` encadeado):
- Rafael, Juliana, Marcos, Cláudio, Diego: "pagamento" em 09/11/2026 08:00 + "ajuste" "Reset para salário base" (saldo = salário).
- Rogério: "pagamento" final em 30/10/2026 17:00 + reset (saldo 1.980,00).
- Edson: 07/10 08:00 "pagamento" + reset (2.800,00) · 13/10 10:00 "ajuste" **"Ajuste de salário: R$ 2.800,00 → R$ 2.900,00"**
  (+100, 2.900,00) · 15/10 "vale" R$ 200,00 dinheiro "Adiantamento" (2.700,00) · 22/10 "bonus" R$ 250,00 "Viagens extras para
  São José dos Campos" (2.950,00) · 28/10 "vale" R$ 300,00 dinheiro "Adiantamento" (2.650,00). Vales 500,00; bônus 250,00.
- Na aula: Diego vale R$ 200,00 "Adiantamento" (1.780,00) e falta R$ 90,00 "Faltou sexta, 06/11, sem avisar" (1.690,00); Cláudio
  bônus R$ 150,00 "Meta de prensagem de outubro" (2.250,00); Edson recebimento R$ 100,00 "Sobra do vale da viagem" (2.750,00) e
  pagamento R$ 2.750,00 Pix (vales descontados 400,00; reset 2.900,00).

**Dinheiro:** caixa do Rafael aberto em 10/11 às 08:30 com R$ 1.500,00 (semente da aula; junção) (só ele aberto; se o do Marcos estiver aberto, aparece
"Qual caixa?" já no do Rafael). Conta bancária principal com saldo acima de R$ 2.750,00. Categoria "Folha Salarial" existente.
Cadastro fiscal: `is_simples_nacional = false` (Lucro Real), Taubaté/SP.

**Ponto:** `time_settings`: entrada 07:00, saída 16:00, intervalo 60, tolerância 10, madrugada até 05:00, seg a sex,
`require_selfie` e `require_geolocation` ligados, quiosque sem reconhecimento facial, fuso America/Sao_Paulo.
`ponto_kiosk_slug` da empresa: `recicla-vale-metais-2h6p`. Batidas (`time_records` + `time_sheets`) de 01/09 a 09/11 para Marcos,
Edson, Cláudio e Diego, dias completos (entrada ~06:55, intervalo 11:00 às 12:00, saída ~16:00), endereço "Rua das Oficinas,
1250 - Parque Industrial - Taubaté" (o endereço do T1, junção), "Mobile - Chrome", foto = avatar ilustrado genérico. Exceções: **Cláudio sem batida
em 05/11** (vira "Falta"; atestado no cap. 10) e **Diego sem batida em 06/11** (fica "Falta", com o desconto do cap. 5). Hoje
(10/11): entradas Edson 06:47, Marcos 06:52, Cláudio 06:58, Diego 07:03 (`time_sheets` do dia com status `open` e `balance_min`
nulo, para o aviso "1 dia(s) sem saída registrada não entram no saldo"). Sem ausências lançadas em novembro.

**Celular (cap. 9):** posição `{"lat": -23.0105, "lng": -45.5412}`; o Nominatim devolve `road` "Rua das Oficinas", `house_number`
"1250", `suburb` "Parque Industrial", `city` "Taubaté" (o endereço do T1 e da semente, junção).

Anotar no `MUNDO_FICTICIO.md`: os 8 funcionários, os 3 departamentos, o endereço do pátio e o slug do tablet.

## Gravação
- Rotas: `/dashboard` → `/funcionarios` (abas por clique); celular: `/ponto/gabriel-rocha-4f7k` (anônimo).
- Sementes: `inicio` (caps. 0 a 2), `apos-cap02` (Gabriel informal, slug gerado), `apos-cap03` (Gabriel CLT), `apos-cap04`
  (Transporte, Edson nele), `apos-cap05`, `apos-cap06` (entrada dos caps. 6 e 7), `apos-cap08` (Juliana com ponto), `apos-cap09`
  (batida do Gabriel), `apos-cap10` (atestado), `apos-cap11` (jornada da Juliana), `apos-cap12` (Rogério arquivado).
- Tabelas/RPCs: `employees` (insert/update), RPC `update_employee_with_salary_adjustment` (sem troca de salário nesta aula, só
  departamento e campos CLT), `generate_ponto_slug` (devolve `gabriel-rocha-4f7k`), `has_ponto_pin`, `employee_departments`,
  `employee_movements`, `cash_transactions` + RPC `adjust_cash_register_balance`, `bank_transactions` + RPCs
  `update_bank_account_balance`/`update_bank_balance`, `financial_categories` ("Folha Salarial"), `bulk_enable_ponto` (Juliana →
  `juliana-prado-8w3n`), `get_or_create_ponto_kiosk_slug`, `time_settings`, `time_schedules` + RPC `save_employee_time_schedules`,
  `employee_absences` (o lançamento recalcula a `time_sheets` do dia para "Atestado"), `time_records`, `time_sheets`.
- Edges: `time-clock-portal` (`get_state` e `register_punch`, hora do servidor, foto no `time-photos`), `time-photo-url` (URL das
  miniaturas no Registro de Ponto).
- Integrações a simular: Nominatim (interceptar no navegador, valores acima); **câmera falsa** do Chromium com um vídeo de avatar
  ilustrado genérico, sem rosto real; o robô toca "Tirar foto agora".
- Celular: capítulo 9 inteiro em `device: phone`, sem login, permissão de localização e câmera concedidas.
- Cap. 10: o `setup` abre a aba "Folha de Ponto" e escolhe "Cláudio Ferraz" fora do vídeo (a visão "Todos os funcionários" mostraria
  falta falsa para o Gabriel e a Juliana: ver Riscos, 1).
- Ilustrações (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`): caderninho do pátio (0), iceberg do custo (2), Informal ×
  CLT (3), a conta do saldo (5), o ciclo do pagamento (6), extrato preso ao dinheiro (7), dois links (8), a hora do sistema (9), a
  falta que aparece sozinha (10), jornada da empresa × individual (11), arquivo × lixeira (12).
- Zoom: CPF, salário, custo total, valores de vale/falta/bônus, valor a receber, valor efetivamente pago, saldo; nunca sobre o toast
  "Registrar Vale registrado com sucesso" nem sobre o "Saldo: R$ 1500.00" do vale (handoffs 3 e 4).

## Riscos, decisões e handoffs
1. **Folha não olha a admissão** (`lib/ponto/folha.ts:96-226`): o Gabriel (admitido em 10/11) e a Juliana (ponto ligado hoje)
   aparecem com "Falta" de 03 a 09/11 na visão "Todos os funcionários". Decisão: o capítulo 10 abre direto na folha do Cláudio
   (setup). Handoff: considerar `hire_date` e a data em que o ponto ligou.
2. **Fonte × código:** o ⚠️ "a jornada individual usa o intervalo da empresa" não vale na 1.59.154 (o intervalo de cada dia entra
   no esperado, `lib/ponto/jornada.ts:107-118`): a fala não o repete. O ⚠️ "o rodapé não é a soma das linhas" virou, no código, o aviso
   "n dia(s) sem saída registrada não entram no saldo": é ele que a fala explica.
3. Toast do vale "Registrar Vale registrado com sucesso" (texto duplicado, `EmployeeMovementModal.tsx:266`).
4. "Saldo: R$ 1500.00" com ponto no "Registrar Vale" (`EmployeeMovementModal.tsx:413,428`).
5. "Pagamento registrado!" / "Gerar Recibo" não aparece depois do pagamento feito em /funcionarios (o modal é desmontado,
   `pages/Employees.tsx:591`); o recibo fica no Extrato. A fala não depende dele.
6. Link pessoal de funcionário arquivado continua batendo ponto (`time-clock-portal/index.ts:557-566`): a fala dá a dica de
   desligar o ponto antes de arquivar.
7. Tabela de IRRF/INSS de 2026 = a de 2025 ("placeholder", `utils/payrollTables.ts:35-38`): a fala não diz valor do modo CLT.

## Atualização 1.60.18 (20/11): o que mudou na gravação e nos riscos
- **Cadeia de sementes:** `inicio` (caps 0 a 2) → `apos-cap02` … `apos-cap16` (um por capítulo, cada ensaio grava a semente do seguinte;
  `bash rec/t19/t19_fila.sh 02:ens,seed 03:ens,seed ...`). `inicio` mudou: Marcos sem o pagamento de 09/11 (último em 07/10), 1 dependente
  e VT R$ 220,00 (folha CLT do cap. 7); Juliana com batidas manuais de 02 a 09/11 (a visão "Todos os funcionários" não mostra falta falsa).
- **Handlers só da T19:** `rpc/set_ponto_pin.mjs` (novo: grava/remove o PIN, o "hash" é `falso:<pin>`) e `functions/time-clock-portal.mjs`
  (PIN no portal, `employee_inactive`, `get_kiosk` e identidade do tablet, `__avanco_min` que adianta a hora do ponto).
- **Comprovantes na tela:** o robô devolve o HTML da aba nova (recibo cap. 6, holerite cap. 7, recibo A4 cap. 9, relação de pagamento
  cap. 10) com o padrão `GANCHOS` + `js_aba_html` (o da T09); entradas `tipo comprovante` em `cenas/ilustracoes.json`.
- **Riscos 1 e 6 corrigidos no app:** a folha não marca "Falta" antes da admissão (o cap. 14 abre na visão da equipe); o link pessoal
  de arquivado mostra "acesso desativado" (a fala do cap. 16 diz). **Risco 5:** "Pagamento registrado!" volta a aparecer (cap. 6 e 7).
- **Celular:** a hora do ponto avança por `__avanco_min` (o `fetch` do robô acrescenta o avanço ao corpo; só o handler falso lê) e pelo
  passo `clock` do navegador: almoço às 11:00 e saída às 16:00 sem esperar. **Tablet:** `TUT_VIEWPORT=1024x768` só no cap. 13
  (`t19_rodar.sh`); o reconhecimento facial não tem como ser mostrado (modelo do navegador), a fala só cita a chave.
