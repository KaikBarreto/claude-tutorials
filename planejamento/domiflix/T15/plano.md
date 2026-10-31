# Plano · T15 — Funcionários: Financeiro do Funcionário e Ponto Eletrônico

- **Título final da aula:** Funcionários, financeiro do funcionário e ponto eletrônico (o cartão final do T14 promete
  "Funcionários e Ponto"; nome da trilha: "Funcionários: Financeiro do Funcionário e Ponto Eletrônico").
- **Áreas das vinhetas:** FUNCIONÁRIOS · CADASTRO · FINANCEIRO DO FUNCIONÁRIO · PONTO ELETRÔNICO · FOLHA · RESUMO.
- **Objetivo (uma frase):** cadastrar a equipe com salário e dia de pagamento, lançar vale, bônus e falta, pagar e colocar o
  ponto eletrônico para funcionar, até a folha aparecer sozinha em Contas a Pagar.
- **Pré-requisito:** T14 na ordem de exibição; a base é o T2 (usuários) e o T13 (Financeiro). Aviso: "Antes: Notas Fiscais".
- **Próximo:** T22 (Ferramentas de RH: DISC, Organograma, Fluxograma). Aviso: "Próximo: Ferramentas de RH".
- **Duração estimada:** ~15 min de fala natural (13 blocos). 🔒 Módulo **Funcionários / RH** (`components/ModuleGateModal.tsx:117-120`).
- Base: `T15/inventario.md` (código 1.38.6). Rótulos entre aspas = exatamente como na tela. Tudo fictício; nenhuma pessoa real.
- **FAKE_NOW:** `2026-11-11T09:00:00-03:00` (quarta) nos blocos 0 a 10; o bloco 11 é um corte para o **dia seguinte**,
  `2026-11-12T08:30:00-03:00` (a folha nasce no cron das 04:00, inventário P11). O T22 parte do dia 12.

## Capítulos propostos

| # | Vinheta (área / título) | O que a tela mostra | Avisos na tela (positivos) | Duração |
|---|---|---|---|---|
| 0 | — | Dashboard → Gestão › "Funcionários": "Funcionários (RH)" ("Gerencie funcionários, vales, pagamentos e extratos"). Fala: equipe, dinheiro de cada um e ponto num lugar só. | "Antes: Notas Fiscais" · "Módulo Funcionários / RH" | 0:35 |
| 1 | FUNCIONÁRIOS / A tela de Funcionários | Abas da lateral (zoom): "Funcionários", "PJ/MEI", "Equipes", "Controle de Ponto", "Perfil Comportamental", "Organograma", "Fluxograma". "Lista de Funcionários" com os seis técnicos; clique em "Rafael Lima": ficha com "Editar", "Extrato", "Arquivar", faixa "Movimentações" e os números ("Salário", "Saldo atual"…). | "As três últimas abas têm tutorial próprio" | 1:00 |
| 2 | CADASTRO / Os dados da funcionária | "Novo Funcionário" → aba "Dados": foto (decisão 3), "Nome Completo \*" Tatiane Ribeiro, "CPF", "Telefone", "Email", "Cargo" Assistente administrativa, "Endereço", "Data de Admissão" 03/11/2026, "Chave PIX" (o e-mail). | "Só o nome é obrigatório" | 1:05 |
| 3 | CADASTRO / Salário e contrato | Aba "Pagamento": "Salário \*" R$ 2.800,00; "Calcular" → "Calcular Custo Mensal" → "Aplicar R$ …" (preenche "Custo mensal total"); "Regime" "CLT"; "CBO" 4110-10, "Matrícula" 00008, "Dependentes (IRRF)" 0, "Vale-transporte" "Sim" → "Valor mensal do VT" R$ 220,00. | "O custo mensal entra nos orçamentos" | 1:15 |
| 4 | CADASTRO / O dia do pagamento | "Configuração de Pagamento": "Frequência" "Mensal", "Tipo de dia" "Dia útil", "N° dia útil do mês" 5; zoom na dica "Valor da folha aparece automaticamente em Contas a Pagar conforme essa configuração.". | "Quinzenal e semanal também" | 0:50 |
| 5 | CADASTRO / Acesso ao sistema | "Vincular a um usuário do sistema" → "Tatiane Ribeiro" (usuária do T2); zoom em "Criar acesso ao sistema" ("Cria automaticamente um usuário com perfil Técnico"), sem ligar (decisão 2); "Criar Funcionário" → "Funcionário criado!". Corte: os seis técnicos já com salário (semente). | "Quem já tem login, é só vincular" | 1:00 |
| 6 | FINANCEIRO DO FUNCIONÁRIO / Vale, bônus e falta | Rafael Lima: "Vale" → "De qual conta sai o vale? \*" "Caixa (em dinheiro)", "Valor \*" R$ 300,00 → "Registrar Vale" → "Vale registrado!"; "Bônus" R$ 150,00 ("Bônus por produtividade") → "Movimentação registrada!"; "Falta" → "Descontar do salário", sugestão R$ 140,00/dia → "Registrar Falta". Zoom em "Saldo atual". | "Só o vale sai do caixa na hora" | 1:30 |
| 7 | FINANCEIRO DO FUNCIONÁRIO / O pagamento | "Pagamento" do Rafael: "Normal / Informal", "Descontar dos Vales" (100%), "Pagar com" "Conta Principal", resumo e "Valor a Pagar" R$ 2.790,00 → "Confirmar Pagamento" → "Deseja gerar Recibo?" → "Não"; "Extrato" com os movimentos e "Gerar Recibo" (zoom). Depois "Pagamento" da Tatiane: "CLT" com "Proventos", "Descontos" (INSS, IRRF, "Vale-transporte"), "Líquido a pagar" e o aviso do contador → "Cancelar". | "No CLT sai o holerite pronto" | 1:40 |
| 8 | PONTO ELETRÔNICO / As regras do ponto | "Controle de Ponto" → "Config": "Jornada Padrão da Empresa" (08:00, 17:00, 60), "Exigir selfie" e "Exigir geolocalização" (decisão 4), "Batidas da madrugada…"; "Salvar configurações"; cartão "Ponto em grupo (quiosque)" (zoom, sem clicar); "Jornada Individual". | "A empresa decide o que a batida pede" | 1:15 |
| 9 | PONTO ELETRÔNICO / O ponto no celular | Editar Tatiane → aba "Ponto eletrônico" → "Ativado" → "Salvar" → "Link de ativação copiado!". Celular (decisão 5): página "Cadastro facial" → "Continuar sem biometria" → "PONTO ELETRÔNICO", "Você ainda não bateu o ponto hoje" → "Registrar Entrada" → "Obtendo sua localização..." → "Tipo", "Horário", "Local" → "Confirmar registro" → "✅ Entrada registrada". | "Sem login, pelo link dela" | 1:40 |
| 10 | PONTO ELETRÔNICO / Acompanhando o ponto | "Hoje": "Presentes 1", linha da Tatiane ("Entrada" 09:02, "Presente"); olho → "Registros do dia," (local); lápis → "Registro manual," (campos e "Justificativa \*") → "Cancelar"; "Histórico" (zoom em "CSV", sem baixar); "Relatório" ("Calendário", "Horas por dia"). | "Esqueceu de bater? Registro manual" | 1:20 |
| 11 | FOLHA / A folha em Contas a Pagar | Corte "no dia seguinte": Financeiro › "Contas a Pagar/Receber" › "A Pagar", busca "Folha": "Folha Tatiane Ribeiro — 2026-12" e as dos técnicos (ícone de pessoas), vencimento 07/12/2026; "Marcar pago" na do Rafael → "Pagamento, Rafael Lima" com "Quitando folha pendente, período 2026-12" → "Cancelar" (decisão 7). | "A folha aparece sozinha, com antecedência" | 1:10 |
| 12 | RESUMO / Recapitulando | Montagem: ficha da Tatiane, movimentações do Rafael, holerite (resumo CLT), batida no celular, "Hoje", folha em A Pagar. | "Próximo: Ferramentas de RH" | 0:55 |

Transições faladas: 1→2 "Bora cadastrar alguém novo na equipe"; 4→5 "Falta só o acesso ao sistema"; 5→6 "Com a equipe
cadastrada, o dia a dia do dinheiro de cada um"; 7→8 "Agora o ponto: primeiro as regras"; 9→10 "E do lado do escritório, você
acompanha"; 10→11 "E a folha do mês, quem lança?". Recap → próximo: "Com a equipe organizada, no próximo tutorial a gente
conhece as ferramentas de RH: o perfil comportamental, o organograma e o fluxograma."

**Falas dos cuidados ⚠️** (regra de 30/10 20:56: caminho certo primeiro, consequência numa frase, sem encenar falha):

| Cuidado | Fala sugerida | Na tela |
|---|---|---|
| Vale × bônus/falta | "O vale sai do caixa na hora, porque o dinheiro já foi. Bônus e falta ficam no saldo e só entram no pagamento." | "Saldo atual" e extrato |
| Conta do vale | "Escolhe de qual conta sai o vale: é isso que faz a despesa cair no lugar certo." | "De qual conta sai o vale? \*" |
| Acesso ao sistema | "Pra criar o acesso, o e-mail vai preenchido e a senha tem pelo menos seis caracteres. Depois, em Usuários e Permissões, você escolhe o cargo da pessoa." | "Criar acesso ao sistema" (zoom) |
| Holerite | "No CLT, ao confirmar, o holerite abre numa página nova, pronta pra imprimir. Se o navegador segurar a página, ele fica no extrato." | modo "CLT" |
| Selfie e localização | "Aqui você decide se a batida pede selfie e localização. As duas já vêm ligadas." | "Config" |
| Valores CLT | "Os descontos são uma estimativa: confere com o seu contador antes de fechar a folha." | aviso da tela |
| Folha | "Não tem botão de gerar folha: ela aparece sozinha em Contas a Pagar, pela configuração de pagamento." | "A Pagar" |

## Mundo fictício

**Começa com** (fim do T14, `seeds-extra/t14/apos-cap13.json`, mais os funcionários do T9): Glacial Cold Brasil; Camila (admin);
os oito usuários do T2 (seis técnicos, a Tatiane Ribeiro com o cargo Escritório); **seis funcionários** (Rafael Lima, Bruno Alves,
Júlia Santos, Lucas Ferreira, Marina Costa, Paulo Souza), cargo "Técnico de refrigeração", `monthly_cost` fictício do T9, ligados
aos usuários, **sem salário** (decisão 1); Conta Principal R$ 20.525,00 e Caixa R$ 1.100,00 (fim do T19, o T14 não pagou nada);
"Folha de Pagamento" ainda não existe; nenhuma movimentação, ponto ou folha.

**Esta aula cria:**

| Item | Valores (fictícios) |
|---|---|
| Funcionária | **Tatiane Ribeiro**, CPF 418.372.906-87, (21) 3000-1008, tatiane.ribeiro@glacialcold.example, "Assistente administrativa", Rua Gavião Peixoto, 120, apto 302, Icaraí, Niterói - RJ; admissão 03/11/2026; PIX = e-mail; CLT, CBO 4110-10, matrícula 00008, 0 dependentes, VT R$ 220,00; salário R$ 2.800,00; custo mensal pela calculadora; Mensal, 5º dia útil; vinculada à usuária; ponto ligado |
| Salários (corte) | técnicos Informal, Mensal, 5º dia útil: Rafael R$ 3.080,00 (R$ 140,00/dia), Bruno e Júlia R$ 2.860,00, Lucas, Marina e Paulo R$ 2.640,00 |
| Movimentações do Rafael | vale R$ 300,00 do Caixa ("Adiantamento"), bônus R$ 150,00 ("Bônus por produtividade"), falta R$ 140,00 ("Falta em 06/11", sem DSR) |
| Pagamento do Rafael | informal, R$ 2.790,00 (3.080 + 150 − 140 − 300), Conta Principal, sem recibo; saída "Pagamento de salário - Rafael Lima" |
| Ponto | `time_settings` (08:00–17:00, 60 min, selfie conforme decisão 4, geolocalização ligada); entrada da Tatiane às 09:02 de 11/11, local fictício perto da empresa |
| Folhas (cron de 12/11) | "Folha {nome} — 2026-12", vencimento 07/12/2026, para a Tatiane (R$ 2.800,00) e os seis técnicos; categoria "Folha de Pagamento" criada |

**Fica para as próximas:** a Tatiane e os técnicos nos organogramas, DISC e fluxogramas do T22; o caixa (Conta Principal
R$ 17.735,00, Caixa R$ 800,00) e as folhas a pagar no Dashboard do T17.

## Gravação (modo fakebase)

**Já coberto:** schema; Financeiro do T13; usuários do T2 (quando o T2 tiver sementes); handler externo do OpenStreetMap.

**Falta** (inventário 4.3), em ordem de prioridade:

1. Sementes: `employees` do T9 (alinhar com quem produzir o T9), `seeds-extra/t15/inicio.json`, `apos-capNN` encadeados, o corte
   dos salários (`apos-cap05`) e as **folhas do cron** no `inicio` do bloco 11 (`financial_transactions` com `payroll_kind='salary'`,
   `payroll_period='2026-12'`, `due_date` 07/12/2026, `employee_id`, mais `financial_categories` "Folha de Pagamento").
2. RPCs: `create_employee_vale` (grava a saída paga "Vale - Rafael Lima", categoria "Funcionários", e o movimento),
   `generate_ponto_slug` (`tatiane-ribeiro-` + 8 letras), `get_employee_face_template_status` (`{enrolled:false}`),
   `create_employee_face_enrollment_link` (`{token}`), `get_or_create_ponto_kiosk_slug`, `register_time_punch`,
   `recompute_time_sheet`, `pay_payroll_transaction` (só se a decisão 7 for confirmar).
3. Edges: `time-clock-portal` (`get_state` com nome, cargo, marca e `settings`; `register_punch` gravando `time_records` e
   `time_sheets`), `face-enrollment` (`context`), `create-user` (estender o do T2, só se a decisão 2 mudar).
4. Storage: `employee-photos` (upload da foto, decisão 3) e `time-photos` (selfie, se ligada).
5. Celular (bloco 9): viewport de celular e passos `geo` e `clock` do robô (mesmo desenvolvimento do T7); endereço do app nos
   links (TRILHA, trabalho comum 7); `localStorage` sem o rascunho de "Novo Funcionário" (P23).
6. Sem nova aba nem download: recibo "Não", holerite só no resumo do modal, "CSV", "Abrir quiosque" e "Baixar QR Code" só com zoom.
7. Desktop 1280×800 nos demais blocos; `storage` com a marca `dominex:portal-tickets-seen:<id da Camila>` (como desde o T12).

## Pronúncias novas para o TTS

| Tela / legenda | Texto do TTS |
|---|---|
| PIX / Chave PIX | pix / chave pix |
| CLT / PJ/MEI | cê-éle-tê / pê-jota ou mêi |
| CBO / IRRF / INSS / FGTS | cê-bê-ó / imposto de renda (ou i-érre-érre-éfe, testar) / i-ene-ésse-ésse / éfe-gê-tê-ésse |
| DSR / VT | dê-ésse-érre / vale-transporte |
| PIN | pim |
| R$ 2.790,00 / R$ 140,00 | dois mil setecentos e noventa reais / cento e quarenta reais |

## Riscos e decisões para o Kaik

1. **Funcionários do T9 sem salário (alinhamento).** O T9 semeia `employees` "com custo mensal fictício" sem dizer o resto. Com
   salário, o cron já teria criado folhas que o T13 não mostra em Contas a Pagar. Proposta: no T9, só `monthly_cost` e salário 0;
   o T15 completa os salários num corte. Registrar em `PRODUCAO.md` → Alinhamentos.
2. **"Criar acesso ao sistema".** O login criado ali tem acesso total (P1) e a senha aparece no aviso (P2). Proposta: vincular a
   Tatiane, que já é usuária, e só mostrar o interruptor. Alternativa: contratar alguém novo, criar o acesso, borrar o aviso na
   edição e aplicar o cargo em Usuários e Permissões.
3. **Foto da funcionária:** avatar ilustrado (nenhum rosto real) pelo passo `upload`, ou sem foto (fica a câmera tracejada).
4. **Selfie no ponto:** desligar "Exigir selfie" no bloco 8 (recomendado: sem câmera e sem imagem de rosto) ou desenvolver a câmera
   simulada do Chromium com um avatar ilustrado. A geolocalização fica ligada, com posição fictícia.
5. **Celular:** os blocos 9 (ativação e batida) precisam da gravação no celular do T7 aprovada antes.
6. **Holerite e recibo em nova aba:** proposta: pagar o Rafael (informal) sem recibo e mostrar o CLT só no modal ("Cancelar").
   Com suporte a nova aba, dá para mostrar o holerite pelo extrato.
7. **Folha no bloco 11:** abrir o modal da folha e cancelar (dezembro ainda não chegou), ou confirmar o pagamento antecipado.
8. **Achados de segurança** (inventário P1, P18, P19, P20, P21, P22): repassar ao time do app; não mudam o vídeo, salvo a decisão 2.
9. **Configurações sem efeito** (raio, tolerância, fora do horário): a fala não cita; handoff P9.
10. **Duração (~15 min):** dá para juntar 3 e 4, ou tirar o "Registro manual" do bloco 10, se ficar longo.
