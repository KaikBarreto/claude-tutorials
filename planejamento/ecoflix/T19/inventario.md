# Inventário · T19 Funcionários e ponto eletrônico (EcoSistema 1.59.154)

Código lido: `/home/claude/ecoflix/app-src-1.59.154/` (só leitura). Caminhos relativos a `src/`, exceto `supabase/...`.
Rótulos entre aspas = texto exato do código (pt-BR). Gravação em 1280×800 (desktop, `xl` vale) e 390×844 (celular).

## 0. Módulo, menu e permissões
- Menu lateral: item próprio **"Funcionários (RH)"** (`config/routes.ts:477`), rota `/funcionarios` (`App.tsx:462-466`, página
  `pages/Employees.tsx`). 🔒 módulo `funcionarios` (`hooks/useCompanyModules.tsx:29`).
- Permissões (`config/routes.ts:223-225`): "Criar, Editar e Excluir Funcionários", "Excluir Funcionários" e **"Gerenciar Ponto
  Eletrônico"** (`action_manage_time_clock`): sem ela as quatro abas de ponto não aparecem (`pages/Employees.tsx:94,162-169`).
  O Rafael (MASTER) vê tudo.
- Rotas públicas do ponto: `/ponto/:slug` (link pessoal), `/ponto/empresa/:kioskSlug` (tablet) (`App.tsx:373-374`).

## 1. Tela Funcionários (`pages/Employees.tsx`)
- Cabeçalho: "Funcionários (RH)" · "Gerencie sua equipe e controle de pagamentos" (`i18n/locales/pt-BR/employees.json:2-3`).
- Abas no topo (underline, `:132-174`): "Funcionários", "Registro de Ponto", "Folha de Ponto", "Ausências", "Configurações de
  Ponto", "Configurações de RH", "Dashboard".
- Aba Funcionários: subabas "Ativos" / "Inativos" (`:377-392`); botões "Gerenciar departamentos", "Exportar Relatório", alternador de
  visão, **"Novo Funcionário"** (`:397-428`). Visão padrão = lista (`useViewMode("employees","list")`, `:124`).
- Lista (`components/EmployeesListView.tsx`): coluna "Equipe" com contador, busca "Buscar por nome ou cargo...", "Filtros"
  (Departamento), "Ordenar" (`:519-580`); cada linha: avatar com iniciais, nome, cargo, departamento (cor e ícone) e o saldo num
  selo verde/vermelho (`:584-628`). Sem seleção: "Selecione um funcionário" (`:652-662`).
- Detalhe (`:306-451`): selo "Ativo"/"Inativo"; botões "Editar", "Extrato", menu "…"; bloco **"Movimentações"**: "Vale", "Bônus",
  "Falta", "Recebimento", "Pagamento" (`:368-379`); **"Resumo financeiro"**: "Salário", "Saldo atual", "Vales", "Bônus", "Faltas",
  "Pagamentos" (`:381-401`); "Dados profissionais": "Admissão", "Regime", "CPF", "Chave Pix", "Último pagamento"; "Contato".
- Menu "…" (`:205-304`): "Editar", "Arquivar" (ou "Reativar" em Inativos), "Excluir definitivamente", "Vale", "Bônus", "Falta",
  "Pagamento", "Recebimento", "Pagar férias", "Pagar 13º salário", "Pagar rescisão", **"Copiar link do ponto"** (só com ponto ligado;
  copia `<origem>/ponto/<slug>`, aviso "Link copiado", `:224-233,294-298`), "Extrato".
- Arquivar: `UPDATE employees SET is_active=false, archived_at` → "Funcionário arquivado" / "O funcionário foi movido para inativos.
  O histórico foi mantido." Reativar → "Funcionário reativado" (`pages/Employees.tsx:190-224`; `employees.json:62-75`).
- Excluir definitivamente: diálogo "Excluir definitivamente" / "Atenção: esta ação é irreversível. Todo o histórico de
  movimentações de {nome} (vales, bônus, faltas e pagamentos) será apagado permanentemente. Não há como desfazer." / "Cancelar" /
  "Excluir definitivamente" (`:596-615`; `employees.json:82-87`); apaga `employee_movements` e `employees` (`:227-248`).
- Aba Dashboard (`components/EmployeesDashboard.tsx:112-155`): "Funcionários Ativos", "Folha de Pagamento", "Média Salarial",
  "Saldo Total a Pagar". Aba Configurações de RH (`components/funcionarios/ConfigRhTab.tsx:213-245`): "Automação da folha"
  (Desligada no mundo; com ela desligada o campo "Regra da folha" não aparece no cadastro).

## 2. Cadastro (`components/EmployeeFormDialog.tsx`)
- Janela "Novo Funcionário" / "Editar Funcionário"; abas "Dados", "Remuneração", "Ponto eletrônico" (`:661-675`); rodapé
  "Cancelar" + "Cadastrar" / "Atualizar" (`:619-640`); aviso "Funcionário cadastrado" / "Funcionário atualizado" · "Os dados foram
  salvos com sucesso" (`:491-494`).
- Dados (`:677-807`): "Selecionar Foto", "Nome *", "CPF" (máscara, "CPF inválido" ao sair do campo), "Telefone" (máscara
  `(12) 90000-0000`), "Email", "Cargo", "Departamento" ("Sem departamento" + os criados), "Data de Admissão", "Endereço".
- Remuneração (`:809-942`): "Salário *" ("R$ 0,00"), "Custo mensal total" + **"Calcular"** · "Salário + encargos + benefícios
  (visão de custo)", "Regime de contratação": "Informal" | "CLT"; com CLT: **"Nº de dependentes (IRRF)"**, **"Desconta
  vale-transporte (até 6%)"**, "Valor mensal do VT"; "Chave PIX" ("Email, CPF, telefone ou chave aleatória").
- Ponto eletrônico (`:944-979`): **"Ativar ponto eletrônico"** · "Gera um link público pro funcionário bater ponto sem login."; em
  cadastro novo de empresa que já usa ponto ele **nasce ligado** ("Sua empresa já usa o ponto eletrônico, então ele já vem
  ativado. Desligue se este funcionário não bate ponto.", `:282-287,953-958`); "PIN do ponto (opcional)" · "Sem PIN. Qualquer um
  com o link consegue bater o ponto dele." · "Definir PIN" (4 ou 6 dígitos) (`funcionarios/ponto/PontoPinField.tsx:39-86`);
  "Reconhecimento facial" · "Não cadastrado" (`funcionarios/ponto/FaceBiometricsField.tsx:67-124`, fora da aula).
- Backend: novo = `INSERT employees` (`:449-456`); edição = RPC `update_employee_with_salary_adjustment` (`:433-442`; trocar o
  salário grava o "ajuste" **"Ajuste de salário: R$ X → R$ Y"**, formato em `utils/employeeCalculations.test.ts:56`); RPC
  `generate_ponto_slug` quando o ponto liga (`:391-400`); RPCs `set_ponto_pin` e `has_ponto_pin` (`:265,405-415`).
- Calculadora (`components/funcionarios/MonthlyCostCalculatorModal.tsx`): "Calcular custo mensal" · "Composição do custo mensal";
  "Regime tributário": "Simples Nacional" | **"Lucro Real / Presumido"** (vem do cadastro fiscal: `is_simples_nacional=false` →
  Lucro Real, `EmployeeFormDialog.tsx:120`) · "Lucro Real/Presumido recolhe INSS patronal sobre a folha."; "Salário base",
  "INSS patronal (%)" (28,8); "Adicional"; "Benefícios mensais"; "Custos anuais (rateado ÷ 12)": "EPI e uniformes" ("Mensal: R$
  …"); "Jornada"; resumo "+ FGTS (8%)", "+ 13º (provisão)", "+ Férias + 1/3 (provisão)", "+ FGTS s/ 13º e férias", "+ Multa
  rescisória (provisão)", "+ INSS patronal (28.8%)", "+ Custos anuais (÷12)", **"Custo total mensal"**; rodapé "Valores
  estimados com base na legislação trabalhista. … Não substitui a orientação do seu contador — consulte sempre um profissional.";
  botão **"Aplicar R$ X"** (`:215-487`). Conta em `utils/employeeCostProvisions.ts:80-138`.

## 3. Departamentos (`components/funcionarios/DepartmentManagerDialog.tsx`, `DepartmentForm.tsx`)
- Janela "Departamentos" · "Organize seus funcionários em departamentos por cor e ícone."; lista com lápis e lixeira; bloco
  "Novo departamento": "Nome *" ("Ex: Produção, Administrativo, Pátio"), "Cor" (`input type=color`), "Ícone" (grade de ícones sem
  rótulo, `components/ui/icon-selector.tsx:27-77`; caminhão = `truck`), **"Adicionar"** → "Departamento criado" (`:54-116,123-237`).
- Excluir: "Excluir departamento {nome}?" · "Os funcionários deste departamento ficarão SEM departamento (não serão apagados)."
- Tabela `employee_departments` (`hooks/useEmployeeDepartments.ts:35-80`).

## 4. Vale, bônus e falta (`components/EmployeeMovementModal.tsx`)
- Títulos "Registrar Vale" · "Adiantamento que será descontado do saldo do funcionário"; "Registrar Bônus" · "Bonificação que será
  adicionada ao saldo do funcionário"; "Registrar Falta" · "Desconto por falta que será subtraído do saldo" (`:52-62`).
- Cartão "Funcionário" + "Saldo Atual"; no vale: "Origem do Pagamento": "Dinheiro (Caixa)" ("Saldo: R$ 1500.00", com ponto) |
  "PIX/Transferência (Banco)"; "Qual caixa?" só com mais de um caixa aberto (`components/CashRegisterPicker.tsx:21-31`); "Valor *";
  "Descrição (opcional)"; "Cancelar" / **"Confirmar"** (`:366-474`).
- Aviso de sucesso "Movimentação registrada" · "Registrar Vale registrado com sucesso" (sic, `:264-267`). Vale em dinheiro sem
  caixa: "Caixa fechado" · "Abra o caixa antes de registrar vales em dinheiro" (`:321-329`).
- Backend: `INSERT employee_movements` (`:132-151`); vale em dinheiro → `cash_transactions` "Vale - {nome}" (withdrawal, categoria
  "Folha Salarial") + saldo do caixa (`:185-207`); vale em PIX → `bank_transactions` (`:233-243`).
- Regra do saldo (`utils/employeeCalculations.ts:92-205`): saldo = `balance_after` do último movimento; só conta o que veio depois
  do último "pagamento" (ou do ajuste "Reset para salário base"); bônus soma, vale e falta subtraem, recebimento abate vales;
  funcionário sem movimento = saldo igual ao salário.

## 5. Pagamento e recebimento
- **"Realizar Pagamento"** · "Pagamento ao funcionário" (`components/EmployeePaymentModal.tsx:843-850`): resumo "Salário:", "Total
  de Bônus:", "Descontos:" ("Vales:", "Faltas:") (`:733-777`); "Quanto você quer descontar dos vales" · "Valor padrão: 100% dos
  vales (R$ X)" (só com vale, `:890-904`); "Modo de pagamento": "Normal" | "CLT (com folha)" (abre no regime do cadastro, `:147-150`);
  no CLT: "Folha CLT", "Proventos (bruto)", "- INSS", "- IRRF", "- Vale-transporte", "Líquido", **"Valores estimados; confirme com
  seu contador."** (`:763-775`); **"Valor efetivamente pago"** · "Calculado: R$ X" (diferença pede "Motivo da diferença" · "A
  diferença vale só neste pagamento: …", `:921-1013`); "Data e hora do pagamento"; "Forma de Pagamento": "Dinheiro" |
  "PIX/Transferência" | "Pagamento Misto"; conta do banco; "Observações (opcional)"; **"Confirmar Pagamento"** (`:798-839`).
- Conta: Salário + Bônus − Faltas − vales descontados (`:228-229`). Grava `employee_movements` "pagamento" (`balance_after` 0),
  saída no caixa/banco "Pagamento - {nome}" (Folha Salarial), o "ajuste" **"Reset para salário base"** (saldo volta ao salário) e,
  se sobrou vale, "Vales restantes do período anterior" (`:541-646`).
- Diálogo "Pagamento registrado!" / "Gerar Recibo" (`:1230-1285`): mora dentro do modal, que a página desmonta ao fechar
  (`pages/Employees.tsx:591`): na 1.59.154 ele não deve aparecer. Recibo: pelo Extrato.
- **"Receber do Funcionário"** · "Registrar devolução de valor pelo funcionário" (`components/EmployeeReceivementModal.tsx:288-374`):
  "Vales pendentes:", "Saldo atual:", "Valor a receber" · "Máximo: R$ X (total de vales pendentes)", "Forma de Recebimento":
  "Dinheiro (entra no caixa)" | "PIX/Transferência (entra na conta)", "Confirmar Recebimento"; sucesso "Recebimento Registrado" ·
  "Recebimento confirmado!" · "Vales antes", "Abatido", "Vales restantes", "Fechar" (`:211-270`). Grava `cash_transactions`
  deposit "Recebimento - {nome}" e o movimento "recebimento" (`:116-187`).

## 6. Extrato (`components/EmployeeExtract.tsx`)
- Janela "Extrato - {nome}" (`:1181`); cartões "Bônus", "Vales", "Faltas", "Saldo" (`:1187-1218`); "Provisões trabalhistas
  (mensal)" só com custo calculado (`:1221-1245`); linhas com selo ("Vale", "Bônus", "Falta", "Pagamento", "Ajuste", "Recebimento"),
  data e hora, valor, "Saldo após: R$ X", descrição, "via Dinheiro/PIX", lixeira (`:1263-1411`).
- Pagamento detalhado: "Salário base", "+ Bônus", "Subtotal", "Total de vales acumulados", "Vales descontados neste pgto", "Valor
  pago", "Diferença do salário base", "Forma" + **"Gerar Recibo"** (`:883-1004,1357-1379`).
- Lista em ordem decrescente: o "Reset para salário base" (pagamento + 1 ms) aparece acima do pagamento, como linha "Ajuste".
- Excluir: "Confirmar exclusão" · "… Os saldos serão recalculados automaticamente. Esta ação não pode ser desfeita." → desfaz a
  saída/entrada no caixa ou no banco (`:560-848`) → "Movimentação excluída" · "A movimentação foi removida, saldos recalculados e
  valores revertidos" (`:834-837,1445-1471`).

## 7. Ponto: configurações (`components/funcionarios/ponto/ConfigPontoTab.tsx`)
- "Configurações de Ponto"; cartão "Jornada Padrão da Empresa" (`:356-550`): **"Exigir selfie"** · "Foto obrigatória a cada batida de
  ponto."; "Exigir reconhecimento facial no quiosque"; **"Exigir localização"** · "Geolocalização obrigatória a cada batida.";
  "Entrada padrão", "Saída padrão", "Intervalo padrão (min)", "Tolerância de atraso (min)", "Batidas da madrugada contam para o
  dia anterior até"; "Dias em que a empresa trabalha" (Dom…Sáb); "Salvar configurações" → "Configurações de ponto salvas"
  (`hooks/useTimeSettings.ts:135-145`). Tabela `time_settings`.
- Cartão **"Tablet da empresa"** (`:553-595`): "Um link só para o ponto de toda a equipe. …", QR, link `/ponto/empresa/<slug>`,
  "Copiar link" ("Link do tablet copiado"), "Baixar QR code". RPC `get_or_create_ponto_kiosk_slug` (`:106`).
- Cartão **"Ativar ponto eletrônico"** (só com alguém sem ponto, `:598-666`): "Marque quem vai bater ponto. …", "Selecionar todos
  (n/m)", lista, **"Ativar ponto (n)"** → "1 funcionário com ponto ativado". RPC `bulk_enable_ponto` (`:174`).
- Cartão "Jornada Individual" (`:669-815`): tabela "Funcionário" × "Dom"…"Sáb" (herdado em cinza, "Folga"), lápis → "Jornada —
  {nome}" · "Sobrescreve o padrão da empresa para este funcionário."; por dia: chave, entrada, saída, intervalo ("min int."),
  "Salvar jornada" → "Jornada salva" (`:818-934`; RPC `save_employee_time_schedules`, `hooks/useTimeSchedules.ts:69`). O
  intervalo de cada dia da jornada individual entra no esperado (`lib/ponto/jornada.ts:1-30,107-118`).

## 8. Ponto no celular (`pages/PontoPublico.tsx` → `components/ponto/PontoScreen.tsx`, tema escuro forçado)
- Início: cabeçalho verde com iniciais, nome e cargo; nome da empresa e data; "PONTO ELETRÔNICO"; rodapé "Você ainda não bateu o
  ponto hoje" + relógio HH:MM:SS; botão **"Registrar Entrada"**; "EcoSistema Tecnologia" (`:793-958`).
- Fluxo (`:426-527,961-1052`): janela "Registrar Entrada" · "Confirme localização e selfie para registrar o ponto"; "Obtendo sua
  localização..."; selfie (`components/ponto/CenteredSelfieCapture.tsx:172-232`): "Selfie do ponto", "Centralize o rosto para a
  selfie", guia ("Posicione seu rosto dentro da moldura"…), **"Tirar foto agora"**, "Esta selfie é usada como comprovante desta
  batida de ponto.", "Cancelar"; confirmação: "Tipo" "Entrada", "Horário", "Local", miniatura; **"Confirmar registro"** → aviso
  **"Ponto registrado"**; depois "Registros de hoje" (linha do tempo), rodapé "PONTO ELETRÔNICO" · "Trabalhando" e os botões
  "Iniciar Intervalo" / "Registrar Saída".
- Endereço: `utils/reverseGeocode.ts:84-194` chama **Nominatim** (`nominatim.openstreetmap.org/reverse`) e monta "Rua, nº - Bairro -
  Cidade". Hora: a do servidor (`supabase/functions/time-clock-portal/index.ts:1073`), mostrada no fuso da empresa
  (`PontoScreen.tsx:364-367`). Selfie e localização obrigatórias conforme as chaves (`index.ts:993-1004`). Selfie recebe carimbo
  com empresa, funcionário, data e endereço (`hooks/usePontoPublico.ts:340-358`).
- Link pessoal de funcionário **arquivado** continua valendo se o ponto dele estiver ligado (`index.ts:557-566`).
- Edge `time-clock-portal`: `get_state` e `register_punch` (`hooks/usePontoPublico.ts:298-371`).

## 9. Ponto pelo gestor
- **"Registro de Ponto"** (`components/funcionarios/ponto/RegistroPontoTab.tsx:191-445`): "Lançar manual"; "Hoje" | "Semana" |
  "Mês"; "Todos os funcionários"; por pessoa: nome, cargo, "N marcação(ões)"; cartão da batida: miniatura da selfie (edge
  `time-photo-url`, `SelfieThumb.tsx:45`), selo "Entrada"/"Início Intervalo"/"Fim Intervalo"/"Saída", hora, endereço, "Mobile -
  Chrome", data e hora; selos "Manual" e "Editado"; menu "Editar" / "Excluir". Vazio de hoje: "Ainda não bateu ponto hoje".
  Tabela `time_records` (`hooks/useTimeRecords.ts:84`).
- **"Folha de Ponto"** (`EspelhoPontoTab.tsx:369-479`): navegador de mês, "Todos os funcionários" (abre no resumo por pessoa:
  "Funcionário", "Dias com registro", "Trabalhado", "Esperado", "Saldo", "Faltas", "Férias", "Atestado", `:725-846`), "Exportar".
  Com uma pessoa: "Data", "Entrada → Saída", "Trabalhado", "Saldo", "Status", "Ações" ("Lançar"/"Editar"); rodapé "Total do mês" ·
  "n falta(s) · n de férias · n com atestado"; aviso "n dia(s) sem saída registrada não entram no saldo" (`:485-716,205-213`).
  Status: "Em andamento", "Completo", "Falta", "Atestado", "Feriado", "Folga"… (`pontoShared.ts:27-39`; `:93-95`).
- Regra (`lib/ponto/folha.ts:96-226`): dia útil passado sem batida e sem ausência = **"Falta"**; feriado nacional ("Finados") =
  "Feriado"; hoje sem saída = fora do saldo. A folha **não olha a data de admissão** (funcionário novo aparece com "Falta" nos dias
  do mês antes de entrar).
- "Lançar ausência" (`AbsenceFormDialog.tsx:177-298`): "Registre quem não veio: férias, atestado, falta, folga ou feriado";
  "Funcionário *" (travado), "Tipo *" ("Férias", "Atestado", "Falta justificada", "Falta injustificada", "Folga", "Meio período",
  "Feriado"), "Data de início", "Data de fim", "1 dia de ausência", "Observação", anexos, "Lançar ausência" → "Ausência lançada".
  Tabela `employee_absences` (`hooks/useEmployeeAbsences.ts:223-277`).
- "Exportar Folha de Ponto" (`TimeSheetExportDialog.tsx:213-277`): "Espelho de Ponto (PDF)" e "Planilha para contabilidade
  (Excel)" · "… Não substitui arquivos fiscais AEJ ou AFD."
