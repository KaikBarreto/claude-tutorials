# Junção do mundo para o app 1.60.10 · EcoFlix (18/11/2026)

O que muda no mundo da Recicla Vale Metais para as 26 aulas serem atualizadas em paralelo. Vale sobre o que as
`Tnn/cobertura_160.md` propõem para o mundo; a história de base continua a do `MUNDO_LINHA_DO_TEMPO.md` (10/11), com as
mudanças daqui. Leia as seções 1 e 2 e, na seção 6, **só a sua aula**.

## 1. Regras
- **Mundo base (B)** = estado de 10/11/2026 08:30 que toda aula recebe (`rec/mundo/seeds`, gerado por
  `rec/mundo/gerar/sementes.mjs`, 280 conferências). Entrou nele só o que é estado de partida de mais de uma aula.
- O que o aluno **vê ser feito** fica na semente da aula (`seeds-extra/tNN/`). A aula seguinte da cadeia só herda se a
  fala dela depender disso (cadeias: T6 → T7 → T8 → T9; T13 → T14 → T15 → T21 → T25; T16 → T17 → T18; T20 herda T4, T7,
  T8, T12 e T16).
- **Variante lateral** = semente de um capítulo que não segue para o capítulo seguinte nem para outra aula (o capítulo
  seguinte abre da semente normal). É o destino padrão de capítulo novo que mexe em dinheiro, estoque ou cadastro.
- Regras fixas do mundo que valem para todo capítulo novo: **Cato ligado** em B (o botão flutuante aparece em toda tela
  logada; o balão de dica é calado pelo robô no `localStorage`, menos no capítulo do Cato da T00 e na T21);
  **assinatura no comprovante desligada** (quem mostra, mostra e desliga de volta); **sem cartão de crédito** fora da
  variante da T14; **uma moeda, um CNPJ, uma balança**; a fala nunca cita preço de plano nem valor de imposto.

## 2. O que mudou no mundo base (B)
Nenhum número falado mudou em B. As conferências antigas (272) continuam passando sem ajuste; 8 novas.

| # | Dado | Valor exato | Para quem |
|---|---|---|---|
| B1 | `app_config.ecotray_version` | **1.7.25** (era 1.7.22); `app_version` 1.60.10 | T05 |
| B2 | Aços Quiririm Ltda (CNPJ 98.463.027/0001-15) | Lucro Real, "É Indústria" ligado, contribuinte, IE **688.042.711.117** (dígito válido). Já era Lucro Real e indústria em B; só a IE mudou | T04, T16, T17, T18 |
| B3 | "Gás da empilhadeira" | 4 despesas **em dinheiro** de R$ 50,00 no caixa do Marcos: 12/08, 26/08, 09/09 e 23/09/2026, categoria "Combustível", centro "Pátio". Saíram do "Diesel e gasolina da picape" de agosto (910 → 810) e de setembro (990 → 890): o Combustível de cada mês não muda (3.640,00 · 3.960,00 · 4.280,00) e **outubro não tem gás** (o Combustível de outubro é todo da Coleta, T15) | T06 |
| B4 | "Internet do escritório" | nova descrição dos 3 lançamentos de R$ 289,90 (17/08, 15/09, 15/10, Conta Principal, categoria **"Telefone e internet"**, sem centro). Era "Internet e telefone do escritório". A categoria "Internet e telefone" proposta pela T13 **não existe**: usa-se "Telefone e internet" | T13 |
| B5 | Bateria da Auto Peças Vale Forte | preço combinado de compra **R$ 3,40/kg** (`entity_custom_prices`, id `@id:ecp.valeforte.bateria`, de 09/11 16:40; a compra de 05/11, nota 2157, foi a R$ 3,10) | T07, T08, T09 |
| B6 | Tabelas vazias novas | `cs_agents`, `affiliates`, `salespeople`, `biometric_credentials`, `dfe_certificate_notice_opt_outs`, `order_activity_events` | todas |

Efeitos colaterais de B3, todos fora de fala: os caixas do Marcos de 12/08 (#10), 26/08 (#23), 09/09 e 23/09 (#46) mudam
R$ 50,00 ou R$ 100,00 na abertura ou no fechamento; o reforço do cofre de 29/10 passa de 30.337,55 para 30.537,55. Cofre
R$ 18.500,00, Conta Principal R$ 46.382,57 em 31/10 e R$ 41.387,77 em 10/11, Secundária R$ 90.515,00, caixas #70
(612,50), #83 (640,00) e #84 (1.250,00), DRE de agosto a novembro, estoque e ids (`@id:ct.N`, `@id:bt.N`): iguais.

**Conferências novas** (`junção 1.60 (...)` no gerador): gás 4 vezes; Combustível por mês; "Internet do escritório";
Aços Quiririm; bateria a 3,40; EcoTray 1.7.25; nenhum cartão em B; caixas #70, #83 e #84. Nenhuma conferência antiga foi
alterada.

## 3. Decisões por pedido das coberturas
B = mundo base · A = semente da aula · V = variante lateral · N = não entra.

| Aula | Pedido | Decisão | Nomes e números |
|---|---|---|---|
| T00 | calar o balão do Cato; Cato ligado | B (já) + robô | `cato_enabled` true em B; balão só no capítulo do Cato |
| T00 | certificado A1 sem barra vermelha | B (handler já existe) | `fiscal_onboarding_status` devolve pronto |
| T00 | `ecoflix_section_titles`, legendas e materiais do episódio | A | semente da T00 |
| T00 | checkout de verdade | N | tela inteira de preço |
| T01 | assinatura no comprovante ligada no mundo | N (mostra e desliga) | B fica sem assinatura; T7, T8, T9 e T20 não mudam |
| T01 | segunda condição de pagamento "À vista" | A | só na T01; B fica com "30/60/90 dias" |
| T01 | padrões de documento, `changelog_entries` | A | semente da T01 |
| T02 | contas bancárias nas sementes | B (já) | Conta Principal (padrão), Conta Secundária, Poupança antiga |
| T02 | restrição de contas do Marcos; "Exigir peso da balança" | N (mostra e cancela) | Marcos segue com todas as contas e sem trava de peso (T5 a T8, T13, T14) |
| T02 | Juliana com as ações novas do banco | N | segue com 15 permissões; Marcos 31 |
| T02 | pedidos no mundo da T2 para o Relatório por Usuário | B (já) | o histórico de B tem compras do Marcos e do Rafael |
| T03 | duplicar tabela; "Definir como principal"; prefixo | V | "Tabela Depósitos (cópia)"; o capítulo termina como começou |
| T04 | cliente em Lucro Real / "É Indústria" | B (B2) + A | Aços Quiririm. A semente `t04/inicio` degrada: IE **688.042.819.111** (válida, errada), `regime_tributario` nulo, `is_industry` falso; a aula corrige para a IE de B, Lucro Real e liga a indústria. Depois da aula = B. T16/T17/T18 não mudam |
| T04 | preço fixo do ferro pesado a R$ 1,00 no Depósito (N7) | V | não segue (mudaria as compras do depósito na T10 e na T20) |
| T04 | etiqueta do Valdir e campo personalizado (N6) | V | não segue; a T20 não mostra etiqueta |
| T04 | "Rogério Alves Costa" completo; busca de CNPJ com IE | A | como a cobertura; `cnpj-lookup` é handler da aula |
| T05 | EcoTray 1.7.25 | B (B1) | muda a tela e os `[BACKEND]` (ver seção 4) |
| T05 | ligar "Imprimir Automaticamente" | N (só mostra) | T7 em diante não mudam |
| T06 | despesa e receita do dia (P1) | A, **na cadeia** | 08:5x no #85: despesa "Gás da empilhadeira" **R$ 50,00** em dinheiro (Combustível · Pátio); receita "Aluguel de caçamba" **R$ 120,00** por Pix na **Conta Principal** (categoria "Aluguel de caçamba", centro "Coleta"). O #85 fecha com **R$ 957,10** |
| T06 | padrão "Gás da empilhadeira" | B (B3) | a tela mostra "Usado 4 vezes · última vez em **setembro** de 2026" (a cobertura dizia outubro) |
| T06 | padrão "Aluguel de caçamba" | A | a régua do app só sugere receita a partir de **conta a receber** ou de entrada em dinheiro. A semente da T06 acrescenta 2 contas a receber **pagas** que espelham as entradas de B (sem dinheiro novo): "Aluguel de caçamba", R$ 1.400,00, 26/08 e 10/09/2026, Conta Principal, Pix/transferência, "Coleta". A tela mostra "Usado 2 vezes · última vez em setembro de 2026" |
| T06 | sangria de verdade (P4b) | A, **na cadeia** | 17:3x: **R$ 5.000,00** do #86 (Marcos) para a Conta Principal, "Depósito do fim do dia". O #86 vai de 20.000,00 para **15.000,00** |
| T06 | rascunho de compra no #85 (P5) | V | Valdir Pereira, 1 item de cobre, como a cobertura (`dia-10-rascunho`) |
| T07 | bateria a R$ 3,40 | B (B5) | tirar `entity_custom_prices` da `t07/inicio` (B já traz, mesmo id) |
| T07 | comprar abatendo o vale do Valdir (3.10) | N (mostra e descarta) | Valdir segue com −300,00 (T4, T9, T13) |
| T07 | edição em caixa fechado | N | só na T09 |
| T08 | ticket do Jair com valores (D) | A, **não segue** | bateria a R$ 3,40 (B5), 2ª pesagem 4.180 kg; T9 e T20 partem do estado de hoje (rascunho) |
| T08 | pesagem avulsa com cobrança | A, não segue | "Areal Boa Vista" (sem cadastro; se a tela exigir, CNPJ 90.472.615/0001-03, Tremembé/SP), placa **HBN3F27**, 23.840 kg / 9.120 kg, **R$ 60,00 por Pix na Conta Principal**, categoria "Serviço de pesagem" (receita, criada na semente da T08). Fora do dinheiro do #85 |
| T08 | segundo ticket pendente da Cooperativa; rascunho apagado | A | semente da T08 |
| T08 | assinatura no comprovante | N (mostra e desliga) | |
| T08 | capítulo sem internet | V ou ilustração | o ticket offline é descartado |
| T09 | reabrir caixa com novo motivo (opção A) | A | só na `t09/inicio`: a compra de 21/10 09:15 do #70 (18 kg de latinha + 138 kg de papelão, R$ 187,50) nasce **sem fornecedor**; a aula põe a Aparecida Ramos. Depois = B. O #70 continua fechando com 612,50 |
| T09 | herdar a T06 nova | A | #85 fecha com **957,10** (era 1.007,10), #86 com **15.000,00** (era 20.000,00); a Conta Principal ganha +120,00 (08:5x) e +5.000,00 (17:3x) |
| T09 | "Imprimir direto" | A | só com `base/balanca-ativada`; senão a fala cita os dois primeiros |
| T10 | material sem compra; alfinete de tabela | N | o mundo não cria; frase só falada |
| T10 | filtro "Usuários" | B (já) | em B, compra em dinheiro é do Marcos e Pix é do Rafael |
| T11 | material "Capa de fio" | A | código **16**, grupo Outros, Kg, estoque 0, compra **R$ 0,10**, venda **R$ 0,30**, NCM 3915.90.00. Só na T11 (B segue com 15 materiais: T03, T21, T22) |
| T11 | máquina "Prensa 01"; perda padrão; conversão e estorno | A | criadas na tela; a conversão é estornada |
| T12 | Rastreamento | A | motorista com login: **Tiago Freitas** (`tiago.freitas@reciclavalemetais.example`, ordem 7, picape EZR4C63). Só na semente da T12, com `extra_users` 1 (a tela de usuários não aparece); pontos fictícios entre Taubaté e Tremembé |
| T12 | excluir ordem; checklist; relatório pelo portal | A | ordem de teste **#11** na semente para o "Excluir"; a T20 continua criando a **11** dela (a T20 não herda a #11 de teste) |
| T13 | Pix de R$ 2.415,00 (cap09b) e de R$ 4.720,00 (cap09c) | A, **na cadeia**, pela **Conta Secundária** | aluguel da empilhadeira (previsto 2.300,00) e duas parcelas dos pneus (2 × 2.360,00), em 10/11 08:2x. **Não é a Conta Principal**: assim o OFX de 17 linhas, os R$ 44.933,47 e os R$ 44.933,67 da T14 não mudam |
| T13 | "Vale Fibra Telecom Ltda" e as contas da internet | A | CNPJ **93.518.274/0001-58**, Taubaté/SP. 2 contas a pagar **pagas** "Internet do escritório", R$ 289,90, vencimento e pagamento em **15/09 e 15/10/2026**, "Telefone e internet", **sem centro de custo**, boleto, Conta Principal, com `bill_payments` apontando para `@id:bt.82` e `@id:bt.143` (B4; sem dinheiro novo) |
| T13 | água com multa; estorno do pneu | N (cancela) | a água segue vencida; o pneu segue pago |
| T14 | cartão de crédito | V (`cartao`) | "**Cartão Empresa**", fecha dia **25**, vence dia **5**, limite **R$ 10.000,00**; uma despesa de **R$ 180,00** (fatura aberta, disponível R$ 9.820,00). Não segue para a T15 |
| T14 | segundo OFX | V | arquivo pronto: `rec/t14/arquivos/Extrato_Secundaria_20261106_20261109.ofx` (seção 5) |
| T14 | três despesas de teste; categoria em lote | V | "(teste)", na `lote`; a categoria em lote é mostrada e cancelada |
| T14 | herdar a T13 nova | A | Conta Secundária entra na T14 com **R$ 83.380,00** (era 90.515,00) e sai com **R$ 75.380,00** (era 82.515,00) |
| T15 | subgrupo "Despesas com pessoal" (P3) | V | não segue (T21, T25, T22 veem o DRE padrão) |
| T15 | três despesas com categoria errada (P8) | V | variante `lote-categoria`: os diesel de **02/10 (1.120,00), 09/10 (1.060,00) e 16/10 (1.050,00)** aparecem em "Outras Despesas" e o capítulo devolve a "Combustível" (3.230,00). Os outros capítulos abrem da semente normal (Combustível 4.280,00) |
| T15 | DFC | A | lê o que a T13 e a T14 deixaram; os Pix novos da T13 já saíram (não são previsão) |
| T16 | duplicatas na 1250 | A | 2 duplicatas de R$ 11.975,00 (a tela dá os vencimentos) |
| T16 | cliente com pendência | A | "**Metalúrgica Pinhal Ltda**", CNPJ **91.647.382/0001-03**, Taubaté/SP, sem IE e sem CEP. Nada é emitido para ela |
| T16 | nota rejeitada (N3) | A, na cadeia | **1252**, Serra Fina, **150 kg** de Alumínio perfil, **R$ 1.560,00** (a cobertura dizia 300 kg e R$ 3.120,00: não cabe junto dos 3.200 kg da T17 nos 3.385 kg do pátio). Rejeitada pelo NCM 7602.00.99, corrigida e autorizada |
| T16 | devolução (N4) | A, na cadeia | **1253**, entrada, a Fundição devolve **40 kg** de Cobre mel da 1250: **R$ 1.916,00**. Só a nota: sem pedido, sem saldo, sem estoque operacional |
| T16 | complementar (N5) | A, na cadeia | **1254**, 500 kg × R$ 0,50 (48,40 − 47,90) = **R$ 250,00** |
| T17 | numeração | A | as duas NF-e do alumínio passam a **1255 e 1256** (eram 1252 e 1253); R$ 55.380,00 e 5.800 kg não mudam |
| T17 | devolução própria (D3) | N | a devolução do mundo é a 1253 da T16; a T17 só a mostra na lista e no relatório |
| T17 | MDF-e nº 2 rejeitado (D2) | A | só na semente das 14:20; a T18 não vê |
| T17 | saldo inicial fiscal da bateria (D7) | A | **3.320 kg em 31/10/2026** (o estoque operacional de bateria nesse dia) |
| T17 | SPED; XML de fornecedor em outubro (D5) | N | "Destinadas" de outubro fica zero |
| T18 | numeração | A | a NF-e da chaparia passa a **1257** (era 1254); 3.600 kg e R$ 3.528,00 não mudam |
| T18 | dois MTR de 04/11 com erro; CDF com erro e rascunho | A | Aços Quiririm, "Sucata de ferro" (a carga de 04/11 é o ferro pesado de B); entram só no corte das 10:40 |
| T19 | Marcos sem o pagamento de 09/11, com dependente e VT | A | `dependents_count` 1, VT R$ 220,00. O Pix da folha de 09/11 (R$ 19.800,00, Secundária) **não muda**: é B |
| T19 | automação da folha; PIN do Gabriel | A | |
| T20 | aba Preços | A | Cooperativa Recomeço com `precos` ligado na tela; preços de B (latinha 6,20 · PET 1,90 · papelão 0,55 · chaparia 0,70 · ferro misto 0,75) |
| T20 | acesso e dois lados (A e B) | A | no Depósito Irmãos Siqueira |
| T20 | notas de entrada e cancelada | A (herda a T16) | 1249 cancelada (Serra Fina), 1250, 1251 (entrada), 1252, 1253 (entrada, devolução da Fundição), 1254 |
| T20 | etiqueta no cartão; assinatura | N | |
| T21 | handlers de ação do Cato; anexos | A | a T21 não herda a T16; parte da T15 |
| T22 | código do grupo | B (handler já existe) | **GRP-7C4E9A** |
| T22 | preço por unidade; venda de outra unidade; código vencido | V | não mexem em B |
| T22 | acerto do `MUNDO_FICTICIO.md` | feito | latinha da matriz **640 kg**; outubro da matriz 272.040,00 / 299.690,00 |
| T25 | duas tarefas a mais | A | semente da T25 |
| T26 | prazo do cartão 25/11; telefone no cartão | A | só CRM |
| T27 | nada novo | | |

Contagem dos 75 pedidos: 10 resolvidos no mundo base (4 com dado novo, que com a descrição da internet e as tabelas
vazias dão os itens B1 a B6; 6 que B já atendia), 51 na semente ou em variante da aula, 13 não entram e 1 é acerto de
documento.

## 4. Número falado (ou de tela) que mudou
| Aula | Onde | De → para |
|---|---|---|
| T06 | `roteiro.md` linhas 143, 149, 151, 152, 155 (cap10), 162, 164, 166, 167 (cap11) e o recap (cap12); `rec/cap10.json` a `cap12.json`, `t06_sementes.py`, `cenas/ilustracoes.json` | R$ 1.007,10 → **R$ 957,10**; fala "mil e sete reais e dez centavos" / "Contei mil e sete e dez" → "novecentos e cinquenta e sete e dez"; "saíram duas compras em dinheiro" ganha "e o gás da empilhadeira" |
| T06 | cobertura, P1 (tela) | "última vez em outubro de 2026" → "setembro de 2026" |
| T09 | `rec/t09_sementes.py` linhas 8 e 209 (só semente; nenhuma fala) | #85 1.007,10 → 957,10; #86 20.000,00 → 15.000,00 |
| T05 | `roteiro.md` linhas 50, 56, 60, 67, 69 e 139 (tela, ilustração e `[BACKEND]`; nenhuma fala) | 1.7.22 → **1.7.25** |
| T13 | cobertura, cap09b e cap09c (fala proposta) | "Conta Principal" → **"Conta Secundária"** |
| T13 | cobertura, cap05b (tela proposta) | categoria "Internet e telefone", centro "Escritório" → "Telefone e internet", sem centro; vencimentos 10/09 e 10/10 → 15/09 e 15/10 |
| T14 | `plano.md` linha 53 (tela) | Conta Secundária 90.515,00 → 83.380,00 na entrada |
| T16 | cobertura, N3 (tela proposta) | 300 kg, R$ 3.120,00 → 150 kg, R$ 1.560,00 |
| T17 | sementes e tela (nenhuma fala cita o número) | NF-e 1252 e 1253 → 1255 e 1256 |
| T18 | sementes e tela (nenhuma fala cita o número) | NF-e 1254 → 1257 |
| T21 | respostas simuladas (aula refeita) | três contas somando 132.448,67 → **125.313,67**; saíram em novembro 43.554,10 → **50.689,10** |

Não mudou: T14 (17 linhas, 44.933,47, 44.933,67, diferença −1.449,10), T15 (outubro no centavo), T17 (55.380,00), T18
(3.528,00), T04 (saldos e "A Receber" 19.540,00), T10, T20 (71.651,58), T22, T25.

## 5. Arquivos e handlers
**Segundo OFX (T14, P6):** `Extrato_Secundaria_20261106_20261109.ofx`, conta 51730-2, 06/11 a 09/11, 8 linhas, saldo
inicial do banco R$ 36.617,00, final **R$ 90.175,00** (o sistema tem 90.515,00 em B: a diferença é o Pix de 340,00).

| # | Data | Valor | Memo | No sistema | Caso |
|---|---|---|---|---|---|
| 1 | 06/11 11:31 | +1.500,00 | PIX RECEBIDO SERRA FINA | adiantamento de 06/11 | sugestão |
| 2 | 06/11 15:31 | +50.215,00 | PIX RECEBIDO ACOS QUIRIRIM | vendas #1736 (48.740,00, 04/11) e #1753 (1.475,00, 06/11) | **casar com vários** |
| 3 | 09/11 10:11 | −1.150,00 | PIX ENVIADO COOPERATIVA RECOMECO | pagamento de saldo | sugestão |
| 4 | 09/11 10:41 | +23.950,00 | PIX RECEBIDO FUNDICAO BANDEIRA | venda #1755 | sugestão |
| 5 | 09/11 15:21 | −817,00 | PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA | compra #1757 | sugestão |
| 6 e 7 | 09/11 16:00 e 16:01 | −10.000,00 e −9.800,00 | PIX ENVIADO FOLHA LOTE 1 e 2 | folha de 19.800,00 | **duas linhas, um lançamento** |
| 8 | 09/11 17:50 | −340,00 | PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA | nada | **baixa no saldo**: o depósito vai de 840,00 para 500,00 a pagar (só na variante) |

As quatro "sugestão" casam no trecho acelerado e sobram os quatro casos da cobertura. Não é finalizado.

**Handlers novos** em `rec/mundo/handlers/rpc/` (espelham a migration citada no comentário; testados contra as sementes):

| RPC | Aulas | Migration |
|---|---|---|
| `get_cash_register_other_order_ids` | T03, T06, T07 e toda aula com caixa aberto | 20261113230300 |
| `get_financial_description_suggestions` | T06, T13, T14 | 20261117235000 |
| `record_partner_balance_movement` | T04, T07, T13, T20, T25 | 20261110235200 |
| `log_order_activity` | T07, T08, T09, T21 | 20261116220000 |
| `cato_routines_manage` | T00, T21, T25 (e todo botão do Cato) | 20261115142000 |
| `cato_corrections_manage` | idem | 20261117030000 |

Já existiam e valem: `fiscal_onboarding_status`, `track_cato_adoption_event`, `get_my_scale_weight_lock`,
`generate_group_invite_code`. Handler novo só carrega com `bash rec/run.sh fake` (na sua porta).

**Ficam para o agente da aula** (uma aula só):
T02 `save_user_permissions_and_bank_accounts`, `set_user_scale_weight_policy`, `user_scale_weight_policies` ·
T03 `duplicate_price_table`, "definir como principal" · T04 `apply_balance_delta`, `registrar_consulta_cnpj_ie`,
`cnpj-lookup`, colunas `balances.current_balance` e `suppliers.linked_supplier_id` · T08 `finalize_weighing_ticket_v4`,
`apply_standalone_weighing_charge_v1`, colunas `weighing_tickets.standalone_*` · T11 `register_production_atomic`,
`production_machines`, `production_recipe_outputs` · T12 `delete_collection_order`, `set_collection_equipment_labels`,
checklist, `collection_driver_locations` · T13 `pay_recurring_financial_bill`, `update_installment_bill_group`,
`pay_financial_bills_batch` · T14 `list_bank_account_shares`, `delete_bank_transactions_batch_atomic`,
`update_financial_transaction_categories_batch`, cartão e faturas · T15 `get_company_dre_configuration` ·
T16 `nfe_emissao_sem_rede`, `nfe_inutilized_numbers`, `dfe_inbound_import_jobs`, `inbound_nfe_fiscal_entries` ·
T17 `get_invoice_dashboard_secure`, `get_nfse_dashboard`, `get_next_nfse_number`, `record_fiscal_inventory_entries`,
edge `mdfe-contingency`, coluna `mdfe_manifests.fiscal_status_confirmation` · T18 PDFs de MTR e CDF no storage ·
T19 `employee_payroll_*`, `employee_absences`, `set_ponto_pin` · T21 os `cato_confirm_*`, `cato_order_journeys`,
`submit_cato_resolution_feedback` · T22 `apply_group_prices_to_company`, `create_group_transfer_as_member`,
`get_group_material_stock`, tabelas `group_*` · T26 `crm_labels`, `crm_automation_rules`.

## 6. Por aula: o que recebe pronto e o que ela mesma cria
- **T00** · Recebe: Cato ligado, certificado pronto, rotinas e respostas revisadas vazias. Cria: títulos de seção e
  materiais da EcoFlix; o balão do Cato só no capítulo dele.
- **T01** · Recebe: nada novo. Cria: "À vista", padrões de documento; mostra a assinatura e desliga.
- **T02** · Recebe: as três contas bancárias; Marcos 31 e Juliana 15 permissões. Cria: nada que siga (restrição e peso:
  mostra e cancela).
- **T03** · Recebe: nada novo. Cria: "Tabela Depósitos (cópia)" em variante.
- **T04** · Recebe: Aços Quiririm certa em B (IE 688.042.711.117, Lucro Real, indústria); `record_partner_balance_movement`.
  Cria: a `inicio` com a IE errada 688.042.819.111, sem regime e sem indústria; N6 e N7 em variante.
- **T05** · Recebe: EcoTray 1.7.25 no `app_config`. Cria: trocar 1.7.22 nas cenas de Windows, no EcoTray falso e na ilustração.
- **T06** · Recebe: o padrão do gás (4 usos, setembro), `get_cash_register_other_order_ids`,
  `get_financial_description_suggestions`. Cria: as 2 contas a receber pagas do aluguel de caçamba; despesa de 50,00 e
  receita de 120,00 (Conta Principal); sangria de 5.000,00 do #86; **#85 fecha com 957,10**.
- **T07** · Recebe: bateria a 3,40 em B (tirar da `inicio`), `log_order_activity`, o handler dos outros caixas. Cria: nada
  que siga além do que já criava; o vale do Valdir fica como está.
- **T08** · Recebe: bateria a 3,40. Cria: categoria "Serviço de pesagem", a pesagem avulsa da Areal Boa Vista (HBN3F27,
  R$ 60,00 por Pix na Conta Principal), o ticket do Jair com valores; nada disso segue.
- **T09** · Recebe da T06: #85 957,10, #86 15.000,00, Conta Principal +5.120,00. Cria: a compra de 21/10 sem fornecedor
  na `inicio`.
- **T10** · Recebe: B igual. Cria: nada novo.
- **T11** · Recebe: B igual. Cria: "Capa de fio" (código 16, 0,10 / 0,30), "Prensa 01".
- **T12** · Recebe: B igual. Cria: login do Tiago Freitas e as posições; ordem de teste #11; checklist.
- **T13** · Recebe: "Internet do escritório" nos lançamentos de B; os dois handlers de saldo e de sugestão. Cria: Vale
  Fibra Telecom (93.518.274/0001-58) e as 2 contas pagas; os Pix de 2.415,00 e 4.720,00 **pela Conta Secundária**.
- **T14** · Recebe da T13: Secundária 83.380,00; Principal como antes. O segundo OFX pronto. Cria: "Cartão Empresa" e a
  variante do segundo extrato; Secundária sai com 75.380,00.
- **T15** · Recebe: outubro igual; a T14 sem cartão. Cria: as variantes do subgrupo e da categoria em lote.
- **T16** · Recebe: Aços Quiririm e Fundição como em B. Cria: Metalúrgica Pinhal (91.647.382/0001-03); 1252 (150 kg,
  1.560,00), 1253 (devolução, 40 kg, 1.916,00), 1254 (complementar, 250,00). Próxima livre: **1255**.
- **T17** · Recebe da T16: notas até a 1254. Cria: **1255 e 1256**, MDF-e nº 1 (e o nº 2 rejeitado à tarde), saldo
  inicial fiscal da bateria 3.320 kg. A posição fiscal de novembro já traz −150 kg de perfil e +40 kg de cobre mel.
- **T18** · Recebe da T17: notas até a 1256. Cria: **1257**, os MTR e o CDF com erro no corte das 10:40.
- **T19** · Recebe: B igual (folha de 19.800,00 paga em 09/11). Cria: Marcos pendente, com dependente e VT de 220,00.
- **T20** · Recebe: T4, T7, T8, T12 e a T16 inteira (notas 1249 a 1254); sem etiqueta e sem assinatura. Cria: `precos`
  da Cooperativa, o acesso do Depósito, a coleta 11.
- **T21** · Recebe da T15: três contas somando 125.313,67; rotinas vazias. Cria: os handlers de ação e as respostas.
- **T22** · Recebe: GRP-7C4E9A; matriz com 640 kg de latinha e o outubro da T15. Cria: as variantes de preço, de
  transferência e do código vencido.
- **T25** · Recebe da T21: novembro igual (vendas 118.620,20, compras 18.781,45). Cria: as duas tarefas a mais.
- **T26** · Recebe: CRM vazio. Cria: tudo do CRM.
- **T27** · Recebe: B igual. Cria: nada novo.

## 7. Ficou para decidir
1. **T19**: com o Marcos pendente, os pagamentos de 09/11 no RH deixam de somar os R$ 19.800,00 do Pix do banco. Hoje
   nenhuma tela cruza os dois; se a T19 mostrar o lançamento bancário, alinhar.
2. **T16/T17**: CFOP e imposto da devolução e da complementar são os que a tela propuser no ensaio (não foram fixados).
3. **T08**: se a tela da pesagem avulsa não deixar cobrar por Pix sem cadastro, a alternativa é cadastrar a Areal Boa
   Vista como cliente (CNPJ acima); em dinheiro mexeria no caixa #85.
4. **Achado, fora do pedido**: o gerador dá agosto −143,20 / −38.082,35 e setembro +13.866,47 / +33.016,47; o
   `MUNDO_FICTICIO.md` (linha de "Outubro") ainda diz +85,31 / −24.147,49 e +12.808,70 / +31.958,70. Já era assim antes
   desta junção e nenhuma conferência cobre esses dois meses.
5. **Achado do app**: a régua de sugestão nunca devolve receita lançada direto no banco (`type = 'income'` não existe em
   `bank_transactions`). O handler espelha isso; vale levar ao `MELHORIAS_ECOSISTEMA.md`.
