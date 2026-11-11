# Linha do tempo do mundo · EcoFlix (junção de 10/11/2026)

Uma história só para as 26 aulas da Recicla Vale Metais: o que aconteceu de agosto a 10/11/2026, de onde cada aula parte e de
onde sai cada número falado. Vale sobre os planos das aulas; o `MUNDO_FICTICIO.md` aponta para cá. Contas conferidas por
script (só leitura), sem rodar o gerador do mundo. A seção 16 lista o que o gerador (`perfis/ecoflix/mundo/gerar/sementes.mjs`)
precisa mudar; a seção 18 é a conferência de todos os números falados.

## 1. Modelo
- **Mundo base (B):** o histórico fechado até **10/11/2026 08:30** (terça). Toda aula parte de B, mais as cadeias abaixo. O que
  a aula faz na tela fica só nela (e nas aulas da cadeia dela).
- **Cadeias** (a seguinte herda o que a anterior fez na tela): T6 → T7 → T8 → T9 (T9 em 11/11 08:30); T13 → T14 → T15 → T21
  → T25; T16 → T17 → T18; a T20 (15:00) herda a T4, a T7, a T8, a T12 e a T16. As outras partem de B.
- **Estados de demonstração aceitos** (a semente da aula tira com `_remove` o que B já tem, para mostrar do zero): T0
  (status da EcoFlix), T1 (a empresa antes do cadastro), T2 (Juliana e Marcos), T3 (Tabela Depósitos, radiador), T16 (a
  configuração fiscal, a série e as notas), T18 (o resíduo salvo e os parceiros do SIGOR), T26 (o CRM) e T27 (White Label).
  A fala dessas aulas não diz nada que contradiga B (ex.: a T16 não fala mais em "outro sistema").
- **Ações ao vivo antes das 08:30** (para a aula seguinte da cadeia ver): a T13 grava às 08:05–08:15 (e o pneu com data de
  09/11 11:00); a T14 grava às 08:10–08:25. B não tem nada em 10/11 antes das 08:30 (nenhum caixa aberto: é a abertura da T6).

### O dia 10/11, na ordem
| Hora | O que acontece | Aula |
|---|---|---|
| 06:40 | a ordem 7 sai (Tiago Freitas, picape EZR4C63, Marcelo Tavares) | T12 |
| 07:00 | troca da Caçamba 03 no Depósito Irmãos Siqueira (Edson Moura, FKD2E41); ordens 9 e 10; frota e Sérgio Paiva | T12 |
| 08:05–08:15 | baixas da energia (1.874,30), da prensa (1.740,00) e recebimento da Aços Quiririm (2.000,00) | T13 |
| 08:10–08:25 | combustível da picape (350,00), transferência de 8.000,00, saque de 2.000,00 + 6,50 | T14 |
| 08:30 | FAKE_NOW padrão: B | quase todas |
| 08:31 | Rafael abre o caixa #85 com R$ 1.500,00 | T6 |
| 08:35 | Pix de R$ 1.200,00 à Cooperativa (T4); as vendas e compras da T7 (FAKE_NOW 08:35) | T4, T7 |
| 08:4x | Rafael abre o #86 do Marcos com R$ 17.000,00 | T6 |
| 08:40–09:00 | ticket #58: o Edson chega com a latinha da cooperativa (9.460 kg / 6.380 kg); rascunho #59 do Jair (bateria, 5.640 kg) | T8 |
| 08:40–08:50 | NF-e 1249 (Serra Fina, cancelada), 1250 (Fundição, CC-e) e 1251 (entrada do #83); 1246 e 1247 inutilizadas | T16 |
| 09:05, 09:12 | NF-e 1252 e 1253 (alumínio pra Serra Fina, 5.800 kg, R$ 55.380,00) | T17 |
| 09:20 | NF-e 1254 (chaparia pra Aços Quiririm, 3.600 kg, R$ 3.528,00) | T18 |
| 09:30 | FAKE_NOW da T17 e da T18 (caps. 0 a 5) | T17, T18 |
| ~09:40 | MDF-e nº 1; o FKD2E41 sai pra Itamonte; o GHT7B19 (Jair) sai com a chaparia (MTR 2611000318) | T17, T18 |
| 10:15–15:05 | venda à Aços Quiririm (1.600 kg de ferro pesado), latinha da Aparecida, ferro misto do Valdir (semente `dia-10`) | T6 |
| 10:40 | corte da T18 | T18 |
| 14:20 | a carga chega em Itamonte; MDF-e encerrado | T17 |
| 15:00 | Portal do parceiro | T20 |
| 17:30 | T11 (caps. 7 em diante) e T26 (cap. 12) | T11, T26 |
| 17:4x | #85 fecha com R$ 1.007,10 e reabre | T6 |
| 11/11 07:10 | Rafael abre o #87 com R$ 1.200,00; FAKE_NOW 08:30 | T9 |

## 2. Calendário
Histórico de **03/08 a 09/11/2026**, só em dia útil (segunda a sexta, sem feriado). Feriados: 07/09, 12/10 e 02/11 (Finados);
a Agenda da T25 mostra também 15/11 e 20/11. **Sábado e feriado sem caixa e sem pedido** (a frase do comprovante do T1 diz
"de segunda a sexta"). O "dia 31" do T10 é 31/10, sábado: só a contagem do pátio (Edição Manual −14 kg, 12:40). 5º dia útil:
07/10 e 09/11 (folha). A NFS-e 14 da T17 tem competência 06/11 (sexta).

## 3. Identidade, pessoas, parceiros e frota
- **Empresa:** Recicla Vale Metais Ltda, CNPJ 47.318.506/0001-07, Rua das Oficinas, 1250, Parque Industrial, CEP 12086-410,
  Taubaté/SP, (12) 90000-4410, `rafael@reciclavalemetais.example`; Lucro Real; logo e ícone enviados no T1 (cap05); frase do
  comprovante "Obrigado pela parceria! Atendemos de segunda a sexta, das 7h às 17h." (68 caracteres). Filial (só T22):
  "Filial Pindamonhangaba", CNPJ 47.318.506/0002-98. Plano Personalizado, 10 módulos, vence em 05/12/2026.
- **Usuários:** Rafael (MASTER, `rafael@`), Juliana Prado e Marcos Antunes (`@reciclavalemetais.example`, permissões do T2).
  Todos os e-mails da empresa no domínio `@reciclavalemetais.example` (T19 e T22 corrigidos). CPF do Rafael 274.913.508-79 (T18,
  vale também no RH da T19).
- **RH (T19):** Rafael, Juliana, Marcos, Edson Moura (motorista), Cláudio Ferraz e Diego Morais (ajudantes, T11), Rogério Batista
  (ex-ajudante, saiu em 30/10); Gabriel Rocha entra na T19. Jair Lopes e Tiago Freitas dirigem, mas não estão no RH.
- **Parceiros** (os do `MUNDO_FICTICIO.md`), com os nomes novos sem colisão: Marcelo Tavares (T12), Hidráulica Moretti (T13),
  Borracharia Dois Irmãos (T14), Cargas Vale do Sol (T16), Contabilidade **Manacá** (T17; era "Jequitibá", que é a metalúrgica da
  T26) e Balanças Tremembé (T17), Serralheria Bem-Te-Vi e Rogério Alves Costa (T4), Zé Moreira (T7), Sandra Pires (T22), Sérgio
  Paiva (motorista novo da T12; era "Rogério Batista", que é o ex-ajudante da T19), e os da T26.
- **Frota em B:** FKD2E41 caminhão truck, tara **6.380 kg** (a 2ª pesagem do T8), capacidade 14.000 kg; GHT7B19 caminhão 3/4,
  3.900 / 4.000 kg; EZR4C63 picape, 1.750 / 1.000 kg. Sem UF de licenciamento, tipo, rodado e carroceria (a T17 completa o
  FKD2E41). Motoristas Edson, Jair e Tiago só com nome e telefone (a T17 completa o CPF e a CNH do Edson). A T12 cria o FVL8A52
  (poliguindaste) e o Sérgio Paiva.

## 4. Materiais e estoque
Preço único por material (a tabela do `MUNDO_FICTICIO.md`); custo médio = preço de compra. A "Tabela Depósitos" (+4 %) existe
em B, mas **não está ligada** ao Depósito Irmãos Siqueira (a T4 liga na tela): em B o depósito compra e vende pela tabela padrão.

**Estoque em 10/11 08:30** (T7, T10, T21; o Posição de Estoque e o Cato dão o mesmo):
| Material | kg | Valor (custo) | | Material | kg | Valor (custo) |
|---|---|---|---|---|---|---|
| Ferro pesado | 2.180 | 2.071,00 | | Alumínio bloco | 2.830 | 20.093,00 |
| Ferro misto | 6.420 | 4.815,00 | | Metal amarelo (latão) | 214 | 5.885,00 |
| Chaparia | 3.750 | 2.625,00 | | Bronze | 38 | 1.102,00 |
| Cobre mel | 42 | 1.785,00 | | Inox | 260 | 1.508,00 |
| Cobre misto | 148 | 5.328,00 | | Bateria automotiva | 3.960 | 12.276,00 |
| Fio de cobre encapado | 96 | 1.728,00 | | Papelão | 1.850 | 1.017,50 |
| Alumínio latinha | 640 | 3.968,00 | | Plástico PET | 920 | 1.748,00 |
| Alumínio perfil | 3.385 | 30.126,50 | | **Total** | **26.733** | **96.076,00** (projeção 116.689,40) |
- O **lote de Minas** (3.200 kg de perfil e 2.600 kg de bloco) está no pátio desde o saldo inicial de 01/08 e sai na T17 (notas
  sem pedido: o pedido fecha na entrega, como o latão de outubro). A chaparia tem 600 kg a mais que a proposta da T21 para a carga
  de 3.600 kg da T18 caber. Latão 214 e cobre mel 42 são os do T7 (a "Falta 18 kg" da aula depende deles).
- **Estoque em 31/10 23:59** (depois do −14 kg): ferro pesado 41.860 · ferro misto 2.540 · chaparia 4.250 · cobre mel 811,5 ·
  cobre misto 128 · fio 82 · latinha 154 · perfil 3.848 · bloco 2.830 · latão 776 · bronze 29 · inox 175 · bateria 3.320 · papelão
  20 · PET 300. Em 30/09 nada fica negativo (ferro pesado 1.874, ferro misto 252, PET 127).
- **Kardex do ferro pesado em novembro (T10):** 31/10 41.860 → 03/11 09:20 +640 (Siqueira, Pix Secundária) 42.500 → 04/11 14:30
  −38.992 (Aços Quiririm, Pix Secundária) 3.508 → 05/11 14:20 −2.608 (Aços, no saldo, T4) 900 → 06/11 09:50 +1.200 (Siqueira, no
  saldo, T4) 2.100 → 06/11 14:05 +400 (Vale Forte, Pix Principal, T14) 2.500 → 06/11 15:30 −1.180 (Aços, Pix Secundária) 1.320 →
  09/11 15:20 +860 (Siqueira, Pix Secundária, 2 fotos) **2.180**. Em outubro: 22/10 compra do **Valdir** de 180 kg lançada duas
  vezes, a cópia excluída (era "Auto Peças", mas a T9 só deixa três compras dela em outubro); 31/10 41.874 → 41.860.

## 5. Outubro (T15 no centavo; T10, T4, T9 e T25 batem)
Compras **R$ 256.860,00**, vendas **R$ 269.240,00**, CMV R$ 218.860,00; ferro pesado 50 t compradas e 10 t vendidas; a sobra e
a falta dos outros materiais se anulam a custo, então o estoque a mais do mês é R$ 38.000,00.

| Fornecedor | Material (kg) | R$ |
|---|---|---|
| Depósito Irmãos Siqueira | ferro pesado 42.000 (lotes de 21.000 em 14/10 e 21/10), ferro misto 14.000, chaparia 5.000, cobre mel 230, cobre misto 100, perfil 600, latão 250, inox 600, bateria 240 (a do #70, 21/10 10:12, Pix) | 83.714,00 |
| Valdir Pereira (seg/qua/sex) | ferro pesado 4.180 (com os 180 de 22/10), ferro misto 16.000, chaparia 6.750, cobre mel 240, cobre misto 200, fio 350 | 44.396,00 |
| Auto Peças Vale Forte (3 compras: 08/10, 15/10, 29/10) | chaparia 850 (08/10, Pix, R$ 595,00), cobre mel 230, cobre misto 400, perfil 300, bloco 700; **nenhuma bateria** | 32.410,00 |
| Aparecida Ramos (Dona Cida) | latinha 1.500, papelão 7.000 | 13.150,00 |
| Cooperativa Recomeço (5 sextas, no saldo) | papelão 8.400, PET 2.600, latinha 1.250, chaparia 1.100, ferro misto 900 (5 pedidos iguais de R$ 3.751,00) | 18.755,00 |
| Balcão (sem fornecedor, dinheiro) | ferro pesado 3.820, ferro misto 10.000, chaparia 3.150, cobre mel 280, fio 250, latinha 500, perfil 1.120, bloco 300, latão 250, bronze 200, inox 600, bateria 1.080 | 64.435,00 |

| Cliente | Material (kg) | R$ |
|---|---|---|
| Fundição Bandeira do Vale | cobre mel 1.000, cobre misto 700, fio 600, latão 500, bronze 200 (3.000 kg) | 112.800,00 |
| Aços Quiririm Ltda | ferro pesado 10.000 (19/10 e 26/10), ferro misto 38.612, chaparia 16.100, inox 1.200 (65.912 kg) | 77.460,60 |
| Serra Fina Alumínio Reciclagem | latinha 3.250, perfil 2.673, bloco 1.000 (6.923 kg) | 60.349,20 |
| Depósito Irmãos Siqueira | papelão 15.400, PET 2.427 (17.827 kg) | 18.630,20 |
Bateria: 1.320 kg comprados e nenhum vendido (T10). Cobre mel: 980 kg comprados (R$ 41.650,00), 1.000 vendidos (R$ 47.900,00).
Despesas de outubro (T15): folha 19.800,00; aluguel 6.500,00; energia 3.850,00 (13/10 09:12; a cópia das 16:40 só no estado do
T15); combustível 4.280,00; manutenção 1.950,00; telefone 289,90; **Tarifas** 186,00; impostos 3.574,10; frete 2.400,00;
aluguel de caçamba (receita) 2.800,00 = NFS-e 12 (13/10, Fundição, 950,00) + NFS-e 13 (29/10, Aços Quiririm, 1.850,00). DRE:
competência +10.350,00 e caixa −27.650,00 (no T15, com a cópia: +6.500,00 e −31.500,00). Dashboard (T25): margem 12.380,00.
NF-e de outubro (T17): 21 notas, 12 de saída (R$ 168.940,00) e 9 de entrada (R$ 97.315,00); a 1248, de 30/10, é o latão de
600 kg da Fundição, com o pedido fechado só em 03/11.

## 6. Agosto e setembro
A regra do gerador sobre o outubro acima: setembro = 93 % de cada compra de outubro (ferro pesado: Siqueira 3.000, Valdir 2.500,
balcão 2.000) e vendas = compras + a descarga de setembro; agosto = 85 %, com o pátio crescendo. Com o outubro da junção,
setembro dá **compras R$ 201.784,25 e vendas R$ 273.047,73** (as do Cato, R6; conferir no gerador).

## 7. Novembro até 10/11 08:30 (B)
| Dia e hora | Fato | Pagamento | Aula |
|---|---|---|---|
| 03/11 09:20 | compra Siqueira, ferro pesado 640 kg (608,00) | Pix Secundária | T10 |
| 03/11 09:40 | compra Siqueira, ferro misto 3.000 kg (2.250,00) | Pix Principal | T14 |
| 03/11 | Aparecida, latinha 38 + papelão 280 (389,60), **lançada duas vezes**; a cópia excluída em 05/11 | dinheiro, #Marcos | T9 |
| 03/11 | balcão: ferro misto 180, cobre mel 18, fio 14 + latinha 12; vale de R$ 300,00 ao Valdir | dinheiro | T4 |
| 03/11 | pedido de venda do latão da NF 1248: Fundição, 600 kg (19.140,00) | Pix Secundária | T17 |
| 03/11 | pagamento do pedido de 30/10 da Cooperativa (3.751,00) | Pix Secundária | T4 |
| 03/11 15:10 | venda Fundição, cobre mel 300 kg, 3x R$ 4.790,00 (17/11, 17/12, 18/01) | parcelado | T13 |
| 03/11 16:10 | venda Serra Fina, perfil 463 kg (4.815,20) | Pix Principal | T14 |
| 04/11 14:30 | venda Aços Quiririm, ferro pesado 38.992 kg (48.740,00): o ferro parado de outubro | Pix Secundária | T10, T15 |
| 04/11 | Dona Cida 42 + 320; balcão ferro misto 240, chaparia 120, latão 16 | dinheiro | |
| 05/11 10:05 | aluguel do galpão de novembro (6.800,00) | Pix Principal | T13, T14 |
| 05/11 | diesel do caminhão truck (1.180,00) | Pix Secundária | |
| 05/11 | compra Vale Forte, bateria 640 kg (1.984,00), NF-e 2157 | Pix Secundária | T16 |
| 05/11 14:20 | venda Aços Quiririm no saldo: ferro pesado 2.608, chaparia 1.000, ferro misto 600 (4.870,00) | saldo | T4, T13 |
| 05/11 16:10 | venda Siqueira no saldo: papelão 1.250, PET 100 (1.260,00) | saldo | T4 |
| 05/11 | Dona Cida 35 + 260; balcão ferro misto 150, cobre mel 12,5, bronze 9 + latinha 8; compensação da cópia de 03/11 | dinheiro | T9 |
| 06/11 09:40 | compra Aparecida, PET 200 kg (380,00) (era "Cooperativa" na T14) | Pix Principal | T14 |
| 06/11 09:50 | compra Siqueira no saldo: ferro pesado 1.200, ferro misto 320, cobre misto 20 (2.100,00), NF-e 884 | saldo | T4, T16 |
| 06/11 10:45 | compra Cooperativa no saldo: papelão 1.700, PET 520, latinha 240, chaparia 220, ferro misto 180 (3.700,00), 3 fotos | saldo | T4, T20 |
| 06/11 | adiantamento da Serra Fina pela próxima carga (1.500,00) | Pix Secundária | T4 |
| 06/11 14:05 | compra Vale Forte, ferro pesado 400 kg (380,00) | Pix Principal | T14 |
| 06/11 15:30 | venda Aços Quiririm, ferro pesado 1.180 kg (1.475,00) | Pix Secundária | T10 |
| 06/11 | Dona Cida 47 + 340; balcão chaparia 160, latão 22, inox 85 | dinheiro | |
| 09/11 07:02–17:36 | **#83 do Marcos**: Dona Cida (latinha 38, papelão 120), Valdir (ferro misto 410), Dona Cida (latinha 26, papelão 60) = 803,30 | dinheiro | T16, T6 |
| 09/11 08:00 | conta da água vencida segue em aberto; boleto pago no banco (o OFX da T14 traz a linha) | | T13, T14 |
| 09/11 10:40 | venda Fundição, cobre mel 500 kg líquidos (bruto 506), 23.950,00, **sem nota**, no #84 do Rafael | Pix Secundária | T16, T20 |
| 09/11 15:20 | compra Siqueira, ferro pesado 860 kg (817,00), 2 fotos | Pix Secundária | T10 |
| 09/11 | Pix parcial de 1.150,00 à Cooperativa; folha (19.800,00) | Pix Secundária | T4, T19 |
| 09/11 | NF-e 3871 da Cooperativa (latinha e PET, 7.550,00) chega por e-mail; a compra não é lançada | | T16 |
Totais (Dashboard da T25 e Cato): vendas **R$ 118.620,20** (Fundição 57.460,00; Aços Quiririm 55.085,00; Serra Fina 4.815,20;
Siqueira 1.260,00), compras **R$ 18.781,45**, margem R$ 99.838,75. A Aços Quiririm não tem fiado de R$ 3.150,00 (T13 corrigida):
o saldo dela é a venda de 05/11.

## 8. Bancos e cofre
- **Conta Principal:** R$ 46.382,57 em 31/10; em novembro só os lançamentos de B da lista da T14 (03/11 −2.250,00 e +4.815,20;
  05/11 −6.800,00; 06/11 −380,00 e −380,00) → **R$ 41.387,77** em 10/11 08:30 (T6, T4, T10, T12, T19). Com a T13: 39.593,47; no fim
  da T14: 44.933,67 (o banco: 44.933,47; diferença casada de 0,20).
- **Conta Secundária:** R$ 25.000,00 em 31/10; em novembro, os outros Pix de B: entradas 94.805,00 (19.140,00 + 48.740,00 + 1.500,00
  + 1.475,00 + 23.950,00) e saídas 29.290,00 (608,00 + 3.751,00 + 1.984,00 + 1.180,00 + 1.150,00 + 817,00 + 19.800,00) → **R$ 90.515,00**
  em 10/11 08:30; R$ 82.515,00 depois da transferência da T14.
- **Conta Cooperativa:** criada na T14 com R$ 5.000,00. **Poupança antiga:** zerada desde 14/08, arquivada na T14.
- **Cofre (DINHEIRO):** R$ 18.500,00 em 10/11 08:30, todo disponível. Em novembro não há transferência entre banco e cofre (o
  cofre de 31/10 cobre as compras em dinheiro de novembro). T14: ajuste para 18.560,00 e saque de 2.000,00.
- Cato (T21, depois da T13, T14 e T15): três contas somando R$ 132.448,67; em novembro entraram 101.620,20 e saíram 43.554,10,
  sem as transferências entre contas e o saque.

## 9. Caixas
Marcos: um caixa por dia útil; Rafael: às segundas e nos dias de carga (inclusive 14/10 e 21/10, os lotes do Siqueira). O #70 é
o do Marcos de 21/10 (07:02 → 17:31, abre com 800,00): só a Aparecida (09:15, 187,50 em dinheiro) e a bateria do Siqueira (10:12,
744,00, Pix) → fecha com **612,50**; o resto de 21/10 vai para o caixa do Rafael. Em 09/11: **#83** do Marcos (07:02 → 17:36,
abre com 1.443,30, as três compras de 803,30, fecha com **640,00**) e **#84** do Rafael (07:58 → 17:44, 1.250,00, sem dinheiro no
dia: a venda da T16 e a compra do T10 são Pix; fecha com **1.250,00**). O #84 é o último antes da T6. Em 10/11: #85 (Rafael) e
#86 (Marcos) na T6; em 11/11, #87 (Rafael) na T9. A T3 e a T19 abrem, na semente delas, um caixa do Rafael às 08:30.

## 10. Saldos dos parceiros e contas
Em 10/11 08:30 (sinal do app; T4): Aços Quiririm +4.870,00 (a receber; T13 recebe 2.000,00 e sobra 2.870,00); Fundição +14.370,00
(as 3 parcelas, só nos títulos); Valdir −300,00 (o vale; a receber); Serra Fina −1.500,00 (adiantamento; a pagar); Cooperativa
+2.550,00 (a pagar; a T4 paga 1.200,00 e sobra 1.350,00, que a T20 quita); Depósito Irmãos Siqueira −840,00 (a pagar). "A Receber"
do T4: R$ 19.540,00. Contas do T13 (água vencida, aluguel pago, energia de outubro em aberto) e as que a T13 cria.

## 11. Fiscal
- **NF-e:** série 1 no EcoSistema desde agosto (entrada e saída na mesma série). Em outubro o "Última nota emitida" foi acertado
  errado e a sequência pulou **1246 e 1247** (nunca viraram nota); a última é a **1248** (30/10). Nível 1 do catálogo do app
  (1.000 documentos/mês; 3.000 e 5.000 nos próximos), tolerância de 5, selo âmbar a partir de 80 %: a fala não diz a cota.
  Hoje: 1249 a 1251 (T16), 1252 e 1253 (T17), 1254 (T18). A Serra Fina (Itamonte, MG) é interestadual: CFOP 6102.
- **Notas recebidas (T16):** Vale Forte nº 2157 de 05/11 (R$ 1.984,00) e Siqueira nº 884 de 06/11 (R$ 2.100,00); XML 3871 da
  Cooperativa de 09/11 (R$ 7.550,00).
- **NFS-e:** 12 (13/10, Fundição, 950,00) e 13 (29/10, Aços Quiririm, 1.850,00); a T17 emite a 14 (competência 06/11).
- **MDF-e:** nenhum antes; o nº 1 é da T17. **Ambiental (T18):** CDF de outubro da Vale Forte com três MTR (as três compras dela).

## 12. Coletas
Ordens 1 a 8 em B: 1 (02/10, cooperativa), 2 (08/10, Vale Forte, a chaparia de 850 kg), 3 (16/10, Siqueira), 4 (Vale Forte,
cancelada em 20/10), 5 (23/10, cooperativa, 10 bags), 6 (27/10, Siqueira, Caçamba 03), 7 (10/11, Marcelo Tavares, a caminho desde
06:40), 8 (10/11, Siqueira, troca da Caçamba 03, Edson, cedo). A T12 cria a 9 (Vale Forte, **11/11** manhã, Jair) e a 10 (portal da
cooperativa, 13/11 tarde); a T20 vê a 10 e cria a 11 (12/11 manhã). A Agenda da T25 lembra da coleta de 11/11, às 08:00.

## 13. Produção, Agenda e CRM
Produção (T11) fica na semente da T11 (ordens #1 e #2 de 03/11 fora de B). Agenda (T25): 10/11 14:00 "Cotação do cobre com a
Fundição Bandeira do Vale" e 11/11 08:00 "Coleta na Auto Peças Vale Forte". CRM (T26): vazio em B (estado de demonstração).

## 14. Estado de partida de cada aula
| Aula | FAKE_NOW | Parte de | O que a aula usa e cria |
|---|---|---|---|
| T0 | 10/11 08:30 | B (status da EcoFlix na semente) | plano, vencimento 05/12; compra de 38 kg de latinha do exemplo |
| T1 | 10/11 08:30 | demonstração (empresa vazia) | cria a identidade de B (logo, ícone, frase de 68 caracteres) |
| T2 | 10/11 08:30 | demonstração (sem Juliana e Marcos) | cria os dois usuários (3/3) |
| T3 | 10/11 08:30 | demonstração (sem Tabela Depósitos) | cobre −0,50 até o cap06; radiador 110 kg; caixa das 08:30 no cap07 |
| T4 | 10/11 08:30 | B | saldos da seção 10; paga 1.200,00 à Cooperativa às 08:35 |
| T5 | 10/11 08:30 | B | EcoTray (pesos de 18,6 e 312 kg) |
| T6 | 10/11 08:30 | B (nenhum caixa aberto; #84 é o último) | #85, #86, saque, tarifa de 39,90 (Secundária, "Tarifas"), dia 10 |
| T7 | 10/11 08:35 | T6 até o #85 | latão 214, cobre mel 42; vendas e compras da aula |
| T8 | 10/11 08:40–09:00 | T7 | ticket #58 (3.018,4 kg, R$ 18.714,08, Pix) e o rascunho #59 |
| T9 | 11/11 08:30 | T6 fechada, T7 e T8 | #87; #70 corrigido; a cópia de 03/11 da Aparecida |
| T10 | 10/11 08:30 | B | Kardex da seção 4; transferência de 320 kg ao vivo |
| T11 | 10/11 08:30 e 17:30 | B + a produção da semente dela | ordem #3, fardo de alumínio |
| T12 | **10/11 07:00** | B | ordens 7 a 10; frota; Sérgio Paiva |
| T13 | 10/11 08:30 | B | contas; baixas antes das 08:30; Aços 4.870 → 2.870 |
| T14 | 10/11 08:30 | T13 | OFX de 17 linhas; Conta Cooperativa; Principal 44.933,67 no fim |
| T15 | 10/11 08:30 | T14 + a cópia da energia | outubro da seção 5 |
| T16 | 10/11 08:30 | demonstração fiscal sobre B | 1249 a 1251, inutilização, notas recebidas |
| T17 | **10/11 09:30** e 14:20 | T16 | 1252 e 1253, MDF-e nº 1, NFS-e 14 |
| T18 | **10/11 09:30** e 10:40 | T17 | 1254, MTR, CDF |
| T19 | 10/11 08:30 | B + caixa do Rafael das 08:30 | RH da seção 3 |
| T20 | 10/11 15:00 | T4, T7, T8, T12 e T16 | cooperativa com 15 entregas (R$ 71.651,58); coleta 11 |
| T21 | 10/11 08:30 | T15 | as respostas R1 a R9 com os números deste arquivo |
| T22 | 10/11 08:30 | B + a filial | outubro da matriz = seção 5 |
| T25 | 10/11 08:30 | T21 | novembro da seção 7; Agenda da seção 13 |
| T26 | 10/11 08:30 e 17:30 | demonstração (CRM vazio) | funis e oportunidades |
| T27 | 10/11 08:30 | B (logo e ícone do T1) | White Label e a cor |

## 15. Decisões da junção
**Os 8 itens de "Para a junção" do `MUNDO_FICTICIO.md`:**
1. **Novembro (T25):** fica o mundo (vendas maiores que compras: o ferro de outubro sai em novembro). A T25 muda a fala: a margem
   de novembro é alta e verde, e a dica "margem não é lucro" usa o ferro comprado em outubro.
2. **Aços Quiririm:** fica o T4 (+4.870,00, venda no saldo em 05/11). A T13 deixa o "fiado de 3.150,00" e baixa 2.000,00 dos
   4.870,00 (sobra 2.870,00).
3. **T10:** 41.860 kg em 31/10 e 42.500 kg em 03/11; a fala do cap10 diz "quarenta e um mil oitocentos e sessenta" e "as vendas".
4. **Tarifas:** só a categoria de sistema "Tarifas" (a ajuda do app confirma o nome); "Tarifas bancárias" sai da semente. A tarifa
   da T6 vai da Conta Secundária (a da Principal é a de 64,90 do OFX).
5. **"A Receber" do T4:** R$ 19.540,00 (a fala do cap12 já diz o novo valor).
6. **Cota da NF-e:** o catálogo do app na 1.59.154 (`useNfeTier.tsx`, `NotasFiscais.tsx`: selo `0/1.000 Documentos`, tolerância 5,
   âmbar a 80 %). A fala da T16 não diz número de cota ("depende do plano"; o selo aparece na tela).
7. **T2 e T3:** demonstração com `_remove`, como a semente fez.
8. **Latão e cobre mel:** fica o T7 (214 e 42 kg), porque a falta de 18 kg da aula depende dele; o T10 e o T21 mudam (o T21 também
   ganha o lote de Minas e a chaparia: R$ 96.076,00). As 2 fotos da compra de 09/11 entram na semente do T10.

**Conflitos achados e como ficou:**
- **FKD2E41 e o Edson no mesmo dia (T8, T12, T17):** a T12 vai para as 07:00; o T8 pesa às 08:40; a T17 sai às 09:40. A tara
  é 6.380 kg nas três (a T12 tinha 9.200 e a T17, 7.800); a T17 só confere a tara e completa o resto.
- **Edson na T7:** quem busca a carga da Fundição é o motorista da Fundição.
- **Caixa antes das 08:30:** nenhum em B (T6). A venda da T16 vira "de ontem" (09/11, no #84); o Cato (T21, R5) responde que não
  há caixa aberto; a T3 e a T19 abrem o caixa da semente às 08:30.
- **T16 × T17 (notas de outubro no EcoSistema):** a Recicla emite pelo EcoSistema desde agosto; a T16 é demonstração e a fala
  não fala de outro sistema; 1246 e 1247 foram puladas em outubro. A 1249 é cancelada porque a Serra Fina "mudou o pedido" (a
  carga grande de alumínio sai na T17). NF-e da T17 e da T18 às 09:05, 09:12 e 09:20 (FAKE_NOW 09:30).
- **Estoque × cargas do dia:** o alumínio da T17 e a chaparia da T18 estão no estoque de 10/11 08:30.
- **OFX da T14 × Pix de novembro:** a Conta Principal só tem a lista da T14; o resto dos Pix de novembro vai para a Secundária.
  O Pix de 380,00 de 06/11 é da Aparecida (a Cooperativa tem 14 compras no T4); a cópia estornada da T9 também é da Aparecida.
- **T9 × T10 × T18 (Auto Peças em outubro):** três compras dela (as três cargas do CDF), nenhuma de bateria; a compra duplicada
  de 22/10 é do Valdir. A fala da T9 diz "nenhuma compra de bateria em outubro".
- **T10 × T15 (outubro):** o outubro foi refeito por fornecedor e cliente para o cobre mel (980 / 1.000 kg) e a bateria (1.320 / 0)
  do T10, mantendo os totais do T15 no centavo.
- **Aluguel de caçamba (T15) × NFS-e de outubro (T17):** são as mesmas receitas; a NFS-e 12 passa a R$ 950,00.
- **NFS-e 14 em sábado:** competência 06/11.
- **Vale Forte em 11/11 (T25) × 12/11 (T12):** a ordem 9 da T12 é para 11/11.
- **White Label (T27):** o ícone vem do T1; o cap02 só mostra e fala do "Substituir".
- **T20:** a cooperativa tem 15 entregas (o ticket do T8 entra); a coleta da T12 aparece em "Minhas coletas"; a nota 1250 é "do
  cobre mel que saiu hoje".
- **T22:** matriz com o outubro do T15 (receita 272.040,00, despesa 299.690,00, −27.650,00); grupo 344.040,00 / 370.690,00; caixa
  −26.650,00 e competência +18.350,00 (diferença 45.000,00); latinha da matriz 640 kg (B); CNPJs da seção 3.
- **Nomes repetidos:** Contabilidade Manacá (T17) e Sérgio Paiva (T12). **E-mails e endereço:** `@reciclavalemetais.example` e a
  Rua das Oficinas, 1250 (ponto da T19). **Frase do comprovante:** sem sábado.
- **T7:** FAKE_NOW 08:35 (depois do #85 da T6). **T9:** o caixa aberto do Rafael é o #87.

## 16. Mudanças para a semente (para o agente do gerador)
Aula · dado · valor. Tudo o que não está aqui fica como a semente de 51224e1.
1. **T21/T7/T17/T18 · `ESTOQUE_HOJE`:** `cobre_mel` 42 (era 212,5), `latao` 214 (74), `al_perfil` 3.385 (185), `al_bloco` 2.830 (230),
   `chaparia` 3.750 (3.150). `confere`: 26.733 kg, R$ 96.076,00, projeção R$ 116.689,40. Os 3.200 kg de perfil, 2.600 de bloco e
   600 de chaparia a mais entram no saldo inicial de 01/08 e ficam parados (fora do `ACUMULA_AGO`), para agosto a outubro não mudarem.
2. **T15/T10/T9/T18 · `OUTUBRO_COMPRAS`:** a tabela da seção 5 (Siqueira, Valdir, Vale Forte, Dona Cida, Cooperativa, balcão), com
   a bateria de 240 kg do Siqueira (#70) e os 180 kg de ferro pesado do Valdir (22/10, em dobro e a cópia excluída) **dentro** da
   tabela (tirar os acréscimos de `COMPRADO_OUT`). Vale Forte só em 08/10 (chaparia, Pix, R$ 595,00), 15/10 e 29/10. Nenhuma outra
   compra de bateria em Pix em outubro (a do balcão é em dinheiro). Cooperativa às **sextas** (agosto 4, setembro 4, outubro 5,
   e 06/11), no saldo, paga por Pix na segunda seguinte; os 5 pedidos de outubro iguais (R$ 3.751,00).
3. **T15/T21 · vendas de outubro:** por cliente como a seção 5 (`confere` 112.800,00 / 77.460,60 / 60.349,20 / 18.630,20). A bateria
   não vende em outubro.
4. **T21 · setembro:** a regra atual sobre o novo outubro; `confere` compras R$ 201.784,25 e vendas R$ 273.047,73.
5. **T15/T17 · caçamba de outubro:** 13/10 Fundição R$ 950,00 e 29/10 Aços Quiririm R$ 1.850,00 (as NFS-e 12 e 13), no lugar das
   duas de 1.400,00.
6. **T6/T14/T15 · tarifas:** categoria de sistema "Tarifas" (sem "Tarifas bancárias"); outubro 186,00; tirar a tarifa de 03/11.
7. **T4/T10/T13/T14/T16/T17 · novembro:** os fatos da seção 7 no lugar de `NOV_FATOS`/`NOV_COMPRAS_MIUDAS`. Principais mudanças: venda
   de 04/11 com **38.992 kg** (R$ 48.740,00); entram 03/11 latão da Fundição (600 kg), 03/11 perfil da Serra Fina (463 kg, Pix
   Principal 16:10), 03/11 ferro misto do Siqueira (3.000 kg, Pix Principal 09:40), 06/11 PET da Aparecida (200 kg, Pix Principal
   09:40), 06/11 ferro pesado da Vale Forte (400 kg, Pix Principal 14:05) e 09/11 10:40 cobre mel da Fundição (500 kg, bruto 506,
   no #84, Pix Secundária, sem nota); 05/11 Vale Forte só com a bateria (640 kg); 06/11 cooperativa com a composição do T4; 09/11
   só as três compras do #83 (sem o balcão); a cópia de 03/11 da Aparecida, excluída em 05/11 com compensação no caixa do Marcos;
   o 640 kg do Siqueira de 03/11 às 09:20.
8. **T6/T14/T21 · bancos:** Principal R$ 46.382,57 em 31/10 e, em novembro, só os 5 lançamentos de B (seção 8); aluguel de
   novembro às 10:05. Secundária R$ 25.000,00 em 31/10 e os 12 lançamentos da seção 8 (diesel, folha e os Pix) → R$ 90.515,00.
   Nenhuma transferência banco ↔ cofre em novembro; cofre R$ 18.500,00.
9. **T6/T9/T16 · caixas:** #70 só com as duas compras da T9 (o resto de 21/10 num caixa do Rafael; ele abre também em 14/10 e
   21/10); #83 abre com 1.443,30 e fecha com 640,00; #84 abre e fecha com 1.250,00.
10. **T12/T17 · frota:** taras e capacidades da seção 3; sem dados de transporte; motoristas sem CPF/CNH.
11. **T16/T17 · fiscal:** NF-e de agosto a outubro na série 1 (21 em outubro, 1246 e 1247 puladas, 1248 em 30/10); `nfe_tier` no
    Nível 1 do catálogo; notas recebidas 2157 (05/11) e 884 (06/11, três itens) na semente da T16; NFS-e 12 e 13.
12. **T17 · NFS-e recebida:** "Contabilidade Manacá Ltda" (CNPJ 47.291.836/0001-56).
13. **T19/T22/T0/T2 · e-mails:** tudo em `@reciclavalemetais.example`; Rafael `rafael@`; CPF do Rafael no RH 274.913.508-79.
14. **T20 · semente:** a compra do ticket #58 do T8 (R$ 18.714,08, Pix, ~09:00) e as ordens 9 e 10 da T12; a venda da T16 de 09/11.
15. **Conferências novas no gerador:** T10 (41.860 em 31/10; cobre mel 980/1.000 e bateria 1.320/0 em outubro), T13 (Aços +4.870,00),
    T21 (os números da seção 4, 7 e 8), T22 (matriz 272.040,00 / 299.690,00), T25 (margem de novembro 99.838,75), T20 (71.651,58,
    15 pedidos, ticket médio 4.776,77).

## 17. Para a T26
A T26 parte de B com o CRM vazio (demonstração aceita) e não usa número do mundo além dos dela. Os nomes novos dela não colidem
com outros; o "Jequitibá" ficou só com ela (a contabilidade da T17 virou "Manacá"). FAKE_NOW 08:30 e 17:30 no cap12, como planejado.

## 18. Conferência dos números falados
Gerada da coluna Fala de todos os roteiros (`jn_falas.py` e `jn_numeros.py` da junção, só leitura). "Valor" é o número lido da
fala; "De onde sai" diz a seção deste arquivo ou o que a aula faz na tela. Números de contagem da própria tela (passos, abas,
dias do calendário) aparecem como "tela".

| Aula | Cap. | Valor | Na fala | De onde sai |
|---|---|---|---|---|
| T00 | cap01 | 3 | três | tela (contagem, data ou passo) |
| T00 | cap05 | 38 kg | trinta e oito quilos | exemplo da aula (38 kg × R$ 6,20 = R$ 235,60); plano da seção 3 |
| T00 | cap05 | 6,20 R$ | seis reais e vinte | exemplo da aula (38 kg × R$ 6,20 = R$ 235,60); plano da seção 3 |
| T00 | cap05 | 235,60 R$ | duzentos e trinta e cinco reais e sessenta | exemplo da aula (38 kg × R$ 6,20 = R$ 235,60); plano da seção 3 |
| T00 | cap09 | 5 | cinco | tela (contagem, data ou passo) |
| T00 | cap10 | 2 | dois | tela (contagem, data ou passo) |
| T00 | cap12 | 12 | doze | tela (contagem, data ou passo) |
| T01 | cap01 | 2 | duas | tela (contagem, data ou passo) |
| T01 | cap01 | 8 | oito | tela (contagem, data ou passo) |
| T01 | cap01 | 2 | dois | tela (contagem, data ou passo) |
| T01 | cap02 | 7 dias | sete dias | tela (contagem, data ou passo) |
| T01 | cap02 | 5 | cinco | tela (contagem, data ou passo) |
| T01 | cap03 | 5 | cinco | tela (contagem, data ou passo) |
| T01 | cap04 | 6 | seis | tela (contagem, data ou passo) |
| T01 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T01 | cap06 | 1.250 | mil duzentos e cinquenta | fechamento do #84 (seção 9) |
| T01 | cap06 | 2 | dois | tela (contagem, data ou passo) |
| T01 | cap07 | 30 | trinta | tela (contagem, data ou passo) |
| T01 | cap07 | 31 | trinta e um | tela (contagem, data ou passo) |
| T01 | cap08 | 2 linhas | duas linhas | tela (contagem, data ou passo) |
| T01 | cap09 | 4 | 4 | tela (contagem, data ou passo) |
| T01 | cap09 | 37 kg | trinta e sete quilos | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 229,40 R$ | duzentos e vinte e nove reais e quarenta | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 229 R$ | duzentos e vinte e nove reais | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 40 ¢ | quarenta centavos | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 200 kg | duzentos quilos | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 10 kg | dez quilos | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 190 kg | cento e noventa quilos | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 142,50 R$ | cento e quarenta e dois reais e cinquenta | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 200 kg | duzentos quilos | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 150 R$ | cento e cinquenta reais | tela do T1 (cadastro e preferências) |
| T01 | cap09 | 2 | dois | tela (contagem, data ou passo) |
| T01 | cap09 | 190 kg | cento e noventa quilos | tela do T1 (cadastro e preferências) |
| T01 | cap10 | 3 | três | tela (contagem, data ou passo) |
| T01 | cap10 | 30 | trinta | tela (contagem, data ou passo) |
| T01 | cap10 | 150 dias | sessenta e noventa dias | tela (contagem, data ou passo) |
| T01 | cap10 | 30 | trinta | tela (contagem, data ou passo) |
| T01 | cap10 | 150 dias | sessenta e noventa dias | tela (contagem, data ou passo) |
| T01 | cap10 | 30 dias | Trinta dias | tela (contagem, data ou passo) |
| T01 | cap10 | 33,33 % | trinta e três vírgula trinta e três cento cento | tela (contagem, data ou passo) |
| T01 | cap10 | 60 dias | Sessenta dias | tela (contagem, data ou passo) |
| T01 | cap10 | 90 dias | noventa dias | tela (contagem, data ou passo) |
| T01 | cap10 | 33,34 | trinta e três vírgula trinta e quatro | tela (contagem, data ou passo) |
| T01 | cap10 | 100 % | cem cento cento | tela (contagem, data ou passo) |
| T01 | cap10 | 100 | cem | tela (contagem, data ou passo) |
| T01 | cap12 | 2 | duas | tela (contagem, data ou passo) |
| T01 | cap13 | 30 | trinta | tela (contagem, data ou passo) |
| T01 | cap13 | 150 dias | sessenta e noventa dias | tela (contagem, data ou passo) |
| T02 | cap02 | 8 | oito | tela (contagem, data ou passo) |
| T02 | cap03 | 1 | uma | tela (contagem, data ou passo) |
| T02 | cap03 | 3 | três | tela (contagem, data ou passo) |
| T02 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T02 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T02 | cap04 | 4 | quatro | tela (contagem, data ou passo) |
| T02 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T02 | cap05 | 2 | dois | tela (contagem, data ou passo) |
| T02 | cap06 | 2 | dois | tela (contagem, data ou passo) |
| T02 | cap08 | 3 | três | tela (contagem, data ou passo) |
| T02 | cap08 | 3 | três | tela (contagem, data ou passo) |
| T02 | cap09 | 1.000 kg | mil quilos | tela do T2 (plano de 3 usuários) |
| T02 | cap09 | 95 ¢ | noventa e cinco centavos | tela do T2 (plano de 3 usuários) |
| T03 | cap01 | 4 | quatro | tela (contagem, data ou passo) |
| T03 | cap01 | 3 | três | tela (contagem, data ou passo) |
| T03 | cap02 | 21 R$ | vinte e um reais | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap02 | 74 | vinte e quatro e cinquenta | tela (contagem, data ou passo) |
| T03 | cap02 | 120 kg | cento e vinte quilos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap02 | 0 | zero | tela (contagem, data ou passo) |
| T03 | cap03 | 16 | dezesseis | tela (contagem, data ou passo) |
| T03 | cap03 | 70 | setenta | tela (contagem, data ou passo) |
| T03 | cap03 | 0 | zero | tela (contagem, data ou passo) |
| T03 | cap03 | 7 | sete | tela (contagem, data ou passo) |
| T03 | cap03 | 0 | zero | tela (contagem, data ou passo) |
| T03 | cap03 | 0 | zero | tela (contagem, data ou passo) |
| T03 | cap03 | 0 | zero | tela (contagem, data ou passo) |
| T03 | cap03 | 7 | zero zero sete | tela (contagem, data ou passo) |
| T03 | cap03 | 7 | sete | tela (contagem, data ou passo) |
| T03 | cap03 | 70 | setenta | tela (contagem, data ou passo) |
| T03 | cap04 | 8 | oito | tela (contagem, data ou passo) |
| T03 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T03 | cap05 | 5 | cinco | tela (contagem, data ou passo) |
| T03 | cap06 | 50 ¢ | cinquenta centavos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap06 | 92 | quarenta e dois e cinquenta | tela (contagem, data ou passo) |
| T03 | cap06 | 137 | quarenta e sete e noventa | tela (contagem, data ou passo) |
| T03 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T03 | cap07 | 4 % | quatro cento cento | tela (contagem, data ou passo) |
| T03 | cap07 | 10 R$ | dez reais | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap07 | 50 | dez e quarenta | tela (contagem, data ou passo) |
| T03 | cap07 | 64 | quarenta e quatro e vinte | tela (contagem, data ou passo) |
| T03 | cap07 | 64 | quarenta e quatro e vinte | tela (contagem, data ou passo) |
| T03 | cap07 | 80 | trinta e cinquenta | tela (contagem, data ou passo) |
| T03 | cap08 | 118 kg | cento e dezoito quilos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap08 | 120 | cento e vinte | tela (contagem, data ou passo) |
| T03 | cap08 | 2 kg | dois quilos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap08 | 120 | cento e vinte | tela (contagem, data ou passo) |
| T03 | cap08 | 118 kg | cento e dezoito quilos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap08 | 8 kg | oito quilos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap08 | 3 | três | tela (contagem, data ou passo) |
| T03 | cap08 | 8 kg | oito quilos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T03 | cap08 | 0 | zero | tela (contagem, data ou passo) |
| T03 | cap09 | 4 | 4 | tela (contagem, data ou passo) |
| T03 | cap10 | 110 kg | cento e dez quilos | tabela de preços (seção 4) e o que a T3 faz na tela |
| T04 | cap00 | 2 | dois | tela (contagem, data ou passo) |
| T04 | cap01 | 2 | duas | tela (contagem, data ou passo) |
| T04 | cap01 | 2 | duas | tela (contagem, data ou passo) |
| T04 | cap01 | 2 | dois | tela (contagem, data ou passo) |
| T04 | cap02 | 0 | zero | tela (contagem, data ou passo) |
| T04 | cap04 | 418 | quatrocentos e dezoito | tela (contagem, data ou passo) |
| T04 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T04 | cap05 | 2.100 R$ | dois mil e cem reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap05 | 1.260 R$ | mil duzentos e sessenta reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap05 | 2 | dois | tela (contagem, data ou passo) |
| T04 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T04 | cap05 | 840 R$ | oitocentos e quarenta reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap08 | 14 | catorze | tela (contagem, data ou passo) |
| T04 | cap08 | 5 | cinco | tela (contagem, data ou passo) |
| T04 | cap08 | 59 % | cinquenta e nove cento cento | tela (contagem, data ou passo) |
| T04 | cap08 | 9 % | nove cento cento | tela (contagem, data ou passo) |
| T04 | cap08 | 26 | seis e vinte | tela (contagem, data ou passo) |
| T04 | cap08 | 55 ¢ | cinquenta e cinco centavos | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap09 | 2.550 R$ | dois mil quinhentos e cinquenta reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap09 | 1.200 R$ | mil e duzentos reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap09 | 1.350 R$ | mil trezentos e cinquenta reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap10 | 26 | seis e vinte | tela (contagem, data ou passo) |
| T04 | cap10 | 47 | sete e quarenta | tela (contagem, data ou passo) |
| T04 | cap10 | 20 | vinte | tela (contagem, data ou passo) |
| T04 | cap10 | 2.100 R$ | dois mil e cem reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap10 | 5.998 R$ | cinco mil novecentos e noventa e oito reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap11 | 450 R$ | quatrocentos e cinquenta reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap11 | 120 | cento e vinte | tela (contagem, data ou passo) |
| T04 | cap12 | 19.540 R$ | dezenove mil quinhentos e quarenta reais | 14.370 + 4.870 + 300 (seção 10) |
| T04 | cap12 | 3 | três | tela (contagem, data ou passo) |
| T04 | cap12 | 4.870 R$ | quatro mil oitocentos e setenta reais | 2.608 × 1,25 + 1.000 × 0,98 + 600 × 1,05 (seção 7) |
| T04 | cap12 | 300 R$ | trezentos reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap12 | 3.690 R$ | três mil seiscentos e noventa reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap12 | 1.350 R$ | mil trezentos e cinquenta reais | saldos (seção 10) e cooperativa (seção 5) |
| T04 | cap12 | 1.500 R$ | mil e quinhentos reais | saldos (seção 10) e cooperativa (seção 5) |
| T05 | cap00 | 312 kg | trezentos e doze quilos | EcoTray simulado da T5 (18,6 e 312 kg) |
| T05 | cap00 | 321 | trezentos e vinte e um | tela (contagem, data ou passo) |
| T05 | cap05 | 58 mm | cinquenta e oito milímetros | tela (contagem, data ou passo) |
| T05 | cap05 | 80 mm | oitenta milímetros | tela (contagem, data ou passo) |
| T05 | cap05 | 58 mm | cinquenta e oito milímetros | tela (contagem, data ou passo) |
| T05 | cap05 | 100 % | cem cento cento | tela (contagem, data ou passo) |
| T05 | cap06 | 18 kg | Dezoito quilos | EcoTray simulado da T5 (18,6 e 312 kg) |
| T05 | cap06 | 600 | seiscentos | tela (contagem, data ou passo) |
| T05 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T05 | cap07 | 312 kg | trezentos e doze quilos | EcoTray simulado da T5 (18,6 e 312 kg) |
| T05 | cap08 | 312 kg | trezentos e doze quilos | EcoTray simulado da T5 (18,6 e 312 kg) |
| T05 | cap11 | 58 mm | cinquenta e oito milímetros | tela (contagem, data ou passo) |
| T06 | cap02 | 1.250 R$ | mil duzentos e cinquenta reais | fechamento do #84 (seção 9) |
| T06 | cap02 | 1.500 R$ | mil e quinhentos reais | caixas (seção 9), cofre (seção 8) e o que a T6 faz |
| T06 | cap02 | 1.500 R$ | mil e quinhentos reais | caixas (seção 9), cofre (seção 8) e o que a T6 faz |
| T06 | cap03 | 1.500 | mil e quinhentos | tela (contagem, data ou passo) |
| T06 | cap03 | 0 | zero | tela (contagem, data ou passo) |
| T06 | cap03 | 0 | zero | tela (contagem, data ou passo) |
| T06 | cap03 | 0 | zero | tela (contagem, data ou passo) |
| T06 | cap04 | 17.000 R$ | dezessete mil reais | 18.500 − 1.500 (T6) |
| T06 | cap04 | 18.500 | dezoito mil e quinhentos | cofre em 10/11 (seção 8) |
| T06 | cap04 | 1.500 | Mil e quinhentos | tela (contagem, data ou passo) |
| T06 | cap04 | 18.500 R$ | dezoito mil e quinhentos reais | cofre em 10/11 (seção 8) |
| T06 | cap04 | 1.500 | mil e quinhentos | tela (contagem, data ou passo) |
| T06 | cap04 | 17.000 | dezessete mil | 18.500 − 1.500 (T6) |
| T06 | cap05 | 20.000 R$ | vinte mil reais | caixas (seção 9), cofre (seção 8) e o que a T6 faz |
| T06 | cap05 | 20.000 | vinte mil | tela (contagem, data ou passo) |
| T06 | cap05 | 20.000 | vinte mil | tela (contagem, data ou passo) |
| T06 | cap05 | 17.000 | dezessete mil | 18.500 − 1.500 (T6) |
| T06 | cap05 | 1.500 | mil e quinhentos | tela (contagem, data ou passo) |
| T06 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T06 | cap05 | 17.000 | dezessete mil | 18.500 − 1.500 (T6) |
| T06 | cap05 | 17.000 | dezessete mil | 18.500 − 1.500 (T6) |
| T06 | cap06 | 2 | dois | tela (contagem, data ou passo) |
| T06 | cap06 | 1.500 | mil e quinhentos | tela (contagem, data ou passo) |
| T06 | cap06 | 18.500 | dezoito mil e quinhentos | cofre em 10/11 (seção 8) |
| T06 | cap06 | 1.500 | mil e quinhentos | tela (contagem, data ou passo) |
| T06 | cap06 | 17.000 | dezessete mil | 18.500 − 1.500 (T6) |
| T06 | cap08 | 17.000 | dezessete mil | 18.500 − 1.500 (T6) |
| T06 | cap09 | 20.000 | vinte mil | tela (contagem, data ou passo) |
| T06 | cap09 | 17 | dezessete | tela (contagem, data ou passo) |
| T06 | cap09 | 3.000 | três mil | tela (contagem, data ou passo) |
| T06 | cap09 | 2 | dois | tela (contagem, data ou passo) |
| T06 | cap09 | 3.000 R$ | três mil reais | caixas (seção 9), cofre (seção 8) e o que a T6 faz |
| T06 | cap09 | 6,50 R$ | seis reais e cinquenta | caixas (seção 9), cofre (seção 8) e o que a T6 faz |
| T06 | cap09 | 3.006,50 R$ | três mil e seis reais e cinquenta | caixas (seção 9), cofre (seção 8) e o que a T6 faz |
| T06 | cap09 | 3.000 | três mil | tela (contagem, data ou passo) |
| T06 | cap09 | 20.000 | vinte mil | tela (contagem, data ou passo) |
| T06 | cap09 | 129 | trinta e nove e noventa | tela (contagem, data ou passo) |
| T06 | cap10 | 2 compras | duas compras | tela (contagem, data ou passo) |
| T06 | cap10 | 1.500 | mil e quinhentos | tela (contagem, data ou passo) |
| T06 | cap10 | 582 | quatrocentos e noventa e dois e noventa | tela (contagem, data ou passo) |
| T06 | cap10 | 1.007,10 R$ | mil e sete reais e dez | 1.500 − 492,90 (T6) |
| T06 | cap10 | 2 | dois | tela (contagem, data ou passo) |
| T06 | cap10 | 1.017 | mil e sete e dez | tela (contagem, data ou passo) |
| T06 | cap12 | 0 | zero | tela (contagem, data ou passo) |
| T06 | cap12 | 2 | duas | tela (contagem, data ou passo) |
| T06 | cap12 | 2 | dois | tela (contagem, data ou passo) |
| T07 | cap05 | 36 R$ | trinta e seis reais | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap05 | 12 kg | doze quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap05 | 400 | quatrocentos | tela (contagem, data ou passo) |
| T07 | cap05 | 446,40 R$ | quatrocentos e quarenta e seis reais e quarenta | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap05 | 3 | três | tela (contagem, data ou passo) |
| T07 | cap05 | 21 kg | vinte e um quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap05 | 600 | seiscentos | tela (contagem, data ou passo) |
| T07 | cap05 | 200 | duzentos | tela (contagem, data ou passo) |
| T07 | cap05 | 0,60 | zero vírgula seis | tela (contagem, data ou passo) |
| T07 | cap05 | 21 kg | vinte e um quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap05 | 26 | seis e vinte | tela (contagem, data ou passo) |
| T07 | cap05 | 130,20 R$ | cento e trinta reais e vinte | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T07 | cap06 | 412 kg | quatrocentos e doze quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap06 | 96 | noventa e seis | tela (contagem, data ou passo) |
| T07 | cap06 | 316 kg | trezentos e dezesseis quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap06 | 3 % | três cento cento | tela (contagem, data ou passo) |
| T07 | cap06 | 9,48 kg | nove vírgula quarenta e oito quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap06 | 306,52 kg | trezentos e seis vírgula cinquenta e dois quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap06 | 229,89 R$ | duzentos e vinte e nove reais e oitenta e nove | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap06 | 2 | duas | tela (contagem, data ou passo) |
| T07 | cap06 | 316 kg | trezentos e dezesseis quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap06 | 306,52 | trezentos e seis vírgula cinquenta e dois | tela (contagem, data ou passo) |
| T07 | cap07 | 2 | dois | tela (contagem, data ou passo) |
| T07 | cap07 | 18 kg | dezoito quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap07 | 400 | quatrocentos | tela (contagem, data ou passo) |
| T07 | cap07 | 400 | quatrocentos | tela (contagem, data ou passo) |
| T07 | cap07 | 2 | duas | tela (contagem, data ou passo) |
| T07 | cap07 | 40 kg | quarenta quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap07 | 1 kg | um quilo | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap07 | 26 | seis e vinte | tela (contagem, data ou passo) |
| T07 | cap08 | 225 R$ | duzentos e vinte e cinco reais | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap08 | 225 | duzentos e vinte e cinco | tela (contagem, data ou passo) |
| T07 | cap08 | 0 | zero zero | tela (contagem, data ou passo) |
| T07 | cap08 | 4,89 R$ | quatro reais e oitenta e nove | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap08 | 0 | zero | tela (contagem, data ou passo) |
| T07 | cap08 | 75 | setenta e cinco | tela (contagem, data ou passo) |
| T07 | cap08 | 75 R$ | setenta e cinco reais | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap08 | 225 | duzentos e vinte e cinco | tela (contagem, data ou passo) |
| T07 | cap08 | 913,20 R$ | novecentos e treze reais e vinte | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap08 | 2 | duas | tela (contagem, data ou passo) |
| T07 | cap09 | 3 | três | tela (contagem, data ou passo) |
| T07 | cap10 | 43 | três e quarenta | tela (contagem, data ou passo) |
| T07 | cap10 | 13 | três e dez | tela (contagem, data ou passo) |
| T07 | cap10 | 186 kg | cento e oitenta e seis quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap10 | 64 | sessenta e quatro | tela (contagem, data ou passo) |
| T07 | cap10 | 2.936,40 R$ | dois mil novecentos e trinta e seis reais e quarenta | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap10 | 200 | duzentos | tela (contagem, data ou passo) |
| T07 | cap10 | 2.000 | dois mil | tela (contagem, data ou passo) |
| T07 | cap10 | 3 | três | tela (contagem, data ou passo) |
| T07 | cap10 | 200 | Duzentos | tela (contagem, data ou passo) |
| T07 | cap10 | 2.000 | dois mil | tela (contagem, data ou passo) |
| T07 | cap10 | 736,40 R$ | setecentos e trinta e seis reais e quarenta | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap11 | 2.000 | dois mil | tela (contagem, data ou passo) |
| T07 | cap11 | 2 | duas | tela (contagem, data ou passo) |
| T07 | cap11 | 2 | Duas | tela (contagem, data ou passo) |
| T07 | cap11 | 1.000 R$ | mil reais | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap11 | 25 | vinte e cinco | tela (contagem, data ou passo) |
| T07 | cap11 | 10 | dez | tela (contagem, data ou passo) |
| T07 | cap11 | 2 | duas | tela (contagem, data ou passo) |
| T07 | cap13 | 152 kg | cento e cinquenta e dois quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap13 | 121 | trinta e um e noventa | tela (contagem, data ou passo) |
| T07 | cap13 | 668,80 R$ | seiscentos e sessenta e oito reais e oitenta | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap13 | 44 | quatro e quarenta | tela (contagem, data ou passo) |
| T07 | cap13 | 214 kg | duzentos e catorze quilos | latão em 10/11 (seção 4, T7) |
| T07 | cap13 | 152 | cento e cinquenta e dois | tela (contagem, data ou passo) |
| T07 | cap13 | 62 | sessenta e dois | tela (contagem, data ou passo) |
| T07 | cap14 | 60 kg | sessenta quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap14 | 42 | quarenta e dois | cobre mel em 10/11 (seção 4, T7) |
| T07 | cap14 | 18 kg | dezoito quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap14 | 18 kg | dezoito quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap14 | 60 kg | sessenta quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap14 | 7.722,80 R$ | sete mil setecentos e vinte e dois reais e oitenta | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap14 | 1.072 | novecentos e noventa e dois e oitenta | tela (contagem, data ou passo) |
| T07 | cap15 | 14 kg | catorze quilos | estoque de 10/11 (seção 4) e o que a T7 faz |
| T07 | cap15 | 600 | seiscentos | tela (contagem, data ou passo) |
| T07 | cap16 | 2 | duas | tela (contagem, data ou passo) |
| T08 | cap02 | 3 | três | tela (contagem, data ou passo) |
| T08 | cap03 | 9.460 kg | nove mil quatrocentos e sessenta quilos | ticket #58 e #59 da T8 (seção 1) |
| T08 | cap03 | 3 | três | tela (contagem, data ou passo) |
| T08 | cap03 | 2 | duas | tela (contagem, data ou passo) |
| T08 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T08 | cap04 | 6.380 kg | seis mil trezentos e oitenta quilos | tara do FKD2E41 (seção 3) |
| T08 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T08 | cap04 | 3.080 kg | Três mil e oitenta quilos | ticket #58 e #59 da T8 (seção 1) |
| T08 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T08 | cap05 | 2 % | dois cento cento | tela (contagem, data ou passo) |
| T08 | cap05 | 61 kg | sessenta e um quilos | ticket #58 e #59 da T8 (seção 1) |
| T08 | cap05 | 600 | seiscentos | tela (contagem, data ou passo) |
| T08 | cap05 | 3.018 kg | Três mil e dezoito quilos | ticket #58 e #59 da T8 (seção 1) |
| T08 | cap05 | 400 | quatrocentos | tela (contagem, data ou passo) |
| T08 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T08 | cap06 | 5.640 kg | cinco mil seiscentos e quarenta quilos | ticket #58 e #59 da T8 (seção 1) |
| T08 | cap07 | 26 | seis e vinte | tela (contagem, data ou passo) |
| T08 | cap07 | 18.714,08 R$ | dezoito mil setecentos e catorze reais e oito | 3.018,4 × 6,20 (T8) |
| T08 | cap08 | 4 | 4 | tela (contagem, data ou passo) |
| T08 | cap08 | 2 | duas | tela (contagem, data ou passo) |
| T08 | cap09 | 3 | três | tela (contagem, data ou passo) |
| T09 | cap00 | 3 | três | tela (contagem, data ou passo) |
| T09 | cap00 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap00 | 2 | duas | tela (contagem, data ou passo) |
| T09 | cap01 | 1 | uma | tela (contagem, data ou passo) |
| T09 | cap01 | 2 | duas | tela (contagem, data ou passo) |
| T09 | cap02 | 24 kg | vinte e quatro quilos | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap03 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap03 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap03 | 240 kg | duzentos e quarenta quilos | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap03 | 744 R$ | setecentos e quarenta e quatro reais | 240 × 3,10 (#70) |
| T09 | cap04 | 42 kg | quarenta e dois quilos | cobre mel em 10/11 (seção 4, T7) |
| T09 | cap04 | 24 | vinte e quatro | tela (contagem, data ou passo) |
| T09 | cap04 | 42 kg | quarenta e dois quilos | cobre mel em 10/11 (seção 4, T7) |
| T09 | cap04 | 260,40 R$ | duzentos e sessenta reais e quarenta | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap04 | 24 kg | vinte e quatro quilos | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap04 | 42 kg | quarenta e dois quilos | cobre mel em 10/11 (seção 4, T7) |
| T09 | cap04 | 300 | duzentos e sessenta e quarenta | tela (contagem, data ou passo) |
| T09 | cap04 | 18 kg | dezoito quilos | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T09 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T09 | cap05 | 280 kg | duzentos e oitenta quilos | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap05 | 210 R$ | duzentos e dez reais | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap05 | 3 | três | tela (contagem, data ou passo) |
| T09 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T09 | cap05 | 5 | cinco | tela (contagem, data ou passo) |
| T09 | cap05 | 3 | três | tela (contagem, data ou passo) |
| T09 | cap06 | 42 kg | quarenta e dois quilos | cobre mel em 10/11 (seção 4, T7) |
| T09 | cap07 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap07 | 1 | um | tela (contagem, data ou passo) |
| T09 | cap07 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap07 | 10 | dez | tela (contagem, data ou passo) |
| T09 | cap08 | 240 kg | duzentos e quarenta quilos | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap08 | 744 R$ | setecentos e quarenta e quatro reais | 240 × 3,10 (#70) |
| T09 | cap08 | 2 | dois | tela (contagem, data ou passo) |
| T09 | cap09 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap09 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap09 | 240 kg | duzentos e quarenta quilos | caixas #70 e #87 (seção 9) e a cópia de 03/11 (seção 7) |
| T09 | cap09 | 744 R$ | setecentos e quarenta e quatro reais | 240 × 3,10 (#70) |
| T09 | cap09 | 662 | seiscentos e doze e cinquenta | tela (contagem, data ou passo) |
| T09 | cap09 | 21 | vinte e um | tela (contagem, data ou passo) |
| T09 | cap09 | 48 | dezessete e trinta e um | tela (contagem, data ou passo) |
| T09 | cap10 | 3 | três | tela (contagem, data ou passo) |
| T09 | cap10 | 21 | vinte e um | tela (contagem, data ou passo) |
| T10 | cap00 | 3 | três | tela (contagem, data ou passo) |
| T10 | cap00 | 31 | trinta e um | tela (contagem, data ou passo) |
| T10 | cap00 | 4 | quatro | tela (contagem, data ou passo) |
| T10 | cap01 | 4 | quatro | tela (contagem, data ou passo) |
| T10 | cap01 | 3 | três | tela (contagem, data ou passo) |
| T10 | cap02 | 3 | três | tela (contagem, data ou passo) |
| T10 | cap02 | 42 kg | quarenta e dois quilos | cobre mel em 10/11 (seção 4, T7) |
| T10 | cap02 | 92 | quarenta e dois e cinquenta | tela (contagem, data ou passo) |
| T10 | cap02 | 6.420 kg | seis mil quatrocentos e vinte quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap03 | 320 kg | trezentos e vinte quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap03 | 6.420 kg | seis mil quatrocentos e vinte quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap03 | 320 kg | trezentos e vinte quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap03 | 6.100 kg | seis mil e cem quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap03 | 2.500 | dois mil e quinhentos | 2.180 + 320 da transferência (T10) |
| T10 | cap04 | 2.180 kg | dois mil cento e oitenta quilos | ferro pesado em 10/11 08:30 (seção 4) |
| T10 | cap04 | 320 | trezentos e vinte | tela (contagem, data ou passo) |
| T10 | cap04 | 2.500 | dois mil e quinhentos | 2.180 + 320 da transferência (T10) |
| T10 | cap04 | 860 kg | oitocentos e sessenta quilos | compra de 09/11 (seção 7) |
| T10 | cap04 | 2.180 | dois mil cento e oitenta | ferro pesado em 10/11 08:30 (seção 4) |
| T10 | cap04 | 10 | dez | tela (contagem, data ou passo) |
| T10 | cap04 | 10 dias | dez dias | tela (contagem, data ou passo) |
| T10 | cap04 | 2 | dois | tela (contagem, data ou passo) |
| T10 | cap04 | 2 dias | dois dias | tela (contagem, data ou passo) |
| T10 | cap05 | 7 | sete | tela (contagem, data ou passo) |
| T10 | cap05 | 2 | dois | tela (contagem, data ou passo) |
| T10 | cap05 | 31 | trinta e um | tela (contagem, data ou passo) |
| T10 | cap05 | 14 kg | catorze quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap05 | 180 kg | cento e oitenta quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T10 | cap06 | 860 kg | Oitocentos e sessenta quilos | compra de 09/11 (seção 7) |
| T10 | cap06 | 95 ¢ | noventa e cinco centavos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap06 | 817 R$ | oitocentos e dezessete reais | 860 × 0,95 (seção 7) |
| T10 | cap07 | 4 | quatro | tela (contagem, data ou passo) |
| T10 | cap08 | 980 kg | novecentos e oitenta quilos | cobre mel comprado em outubro (seção 5) |
| T10 | cap08 | 41.650 R$ | quarenta e um mil seiscentos e cinquenta reais | 980 × 42,50 (seção 5) |
| T10 | cap08 | 92 | quarenta e dois e cinquenta | tela (contagem, data ou passo) |
| T10 | cap08 | 86 kg | oitenta e seis quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap08 | 6 kg | seis quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap08 | 80 kg | oitenta quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap08 | 1.000 kg | mil quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap08 | 47.900 R$ | quarenta e sete mil e novecentos reais | 1.000 × 47,90 (seção 5) |
| T10 | cap08 | 137 | quarenta e sete e noventa | tela (contagem, data ou passo) |
| T10 | cap08 | 6.250 R$ | seis mil duzentos e cinquenta reais | 47.900 − 41.650 (T10) |
| T10 | cap08 | 13 % | treze cento cento | tela (contagem, data ou passo) |
| T10 | cap08 | 2 | dois | tela (contagem, data ou passo) |
| T10 | cap08 | 1.000 kg | mil quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap08 | 5.400 | cinco mil e quatrocentos | (47,90 − 42,50) × 1.000 (T10) |
| T10 | cap08 | 1.320 kg | mil trezentos e vinte quilos | bateria de outubro, ou o ferro pesado em 06/11 (seção 4) |
| T10 | cap10 | 31 | trinta e um | tela (contagem, data ou passo) |
| T10 | cap10 | 2.500 kg | dois mil e quinhentos quilos | 2.180 + 320 da transferência (T10) |
| T10 | cap10 | 31 | trinta e um | tela (contagem, data ou passo) |
| T10 | cap10 | 82 | vinte e três e cinquenta e nove | tela (contagem, data ou passo) |
| T10 | cap10 | 31 | trinta e um | tela (contagem, data ou passo) |
| T10 | cap10 | 41.860 kg | quarenta e um mil oitocentos e sessenta quilos | ferro pesado em 31/10 (seção 4) |
| T10 | cap11 | 31 | trinta e um | tela (contagem, data ou passo) |
| T10 | cap12 | 320 kg | trezentos e vinte quilos | estoque e Kardex (seção 4) e outubro (seção 5) |
| T10 | cap12 | 31 | trinta e um | tela (contagem, data ou passo) |
| T11 | cap01 | 4 | quatro | tela (contagem, data ou passo) |
| T11 | cap03 | 1 kg | um quilo | produção da semente da T11 (seção 13) |
| T11 | cap03 | 1 kg | um quilo | produção da semente da T11 (seção 13) |
| T11 | cap03 | 1 kg | um quilo | produção da semente da T11 (seção 13) |
| T11 | cap03 | 4 | quatro | tela (contagem, data ou passo) |
| T11 | cap03 | 1 kg | um quilo | produção da semente da T11 (seção 13) |
| T11 | cap03 | 600 | seiscentos | tela (contagem, data ou passo) |
| T11 | cap03 | 1 kg | um quilo | produção da semente da T11 (seção 13) |
| T11 | cap03 | 500 kg | Quinhentos quilos | produção da semente da T11 (seção 13) |
| T11 | cap03 | 500 kg | quinhentos quilos | produção da semente da T11 (seção 13) |
| T11 | cap03 | 50 kg | Cinquenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap03 | 80 kg | oitenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap05 | 500 kg | quinhentos quilos | produção da semente da T11 (seção 13) |
| T11 | cap05 | 1 | um | tela (contagem, data ou passo) |
| T11 | cap05 | 500 kg | quinhentos quilos | produção da semente da T11 (seção 13) |
| T11 | cap05 | 6,20 R$ | seis reais e vinte | produção da semente da T11 (seção 13) |
| T11 | cap05 | 3 | três | tela (contagem, data ou passo) |
| T11 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T11 | cap07 | 1 | um | tela (contagem, data ou passo) |
| T11 | cap07 | 260 kg | duzentos e sessenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap07 | 220 | duzentos e vinte | tela (contagem, data ou passo) |
| T11 | cap07 | 480 kg | quatrocentos e oitenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap07 | 14 kg | catorze quilos | produção da semente da T11 (seção 13) |
| T11 | cap08 | 480 kg | quatrocentos e oitenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap08 | 498 kg | quatrocentos e noventa e oito quilos | produção da semente da T11 (seção 13) |
| T11 | cap08 | 18 kg | dezoito quilos | produção da semente da T11 (seção 13) |
| T11 | cap08 | 498 | quatrocentos e noventa e oito | tela (contagem, data ou passo) |
| T11 | cap08 | 498 kg | quatrocentos e noventa e oito quilos | produção da semente da T11 (seção 13) |
| T11 | cap08 | 480 | quatrocentos e oitenta | tela (contagem, data ou passo) |
| T11 | cap09 | 2 % | dois cento cento | tela (contagem, data ou passo) |
| T11 | cap09 | 480 kg | quatrocentos e oitenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap09 | 9 kg | nove quilos | produção da semente da T11 (seção 13) |
| T11 | cap09 | 600 | seiscentos | tela (contagem, data ou passo) |
| T11 | cap09 | 18 kg | dezoito quilos | produção da semente da T11 (seção 13) |
| T11 | cap10 | 500 kg | quinhentos quilos | produção da semente da T11 (seção 13) |
| T11 | cap10 | 480 | quatrocentos e oitenta | tela (contagem, data ou passo) |
| T11 | cap10 | 96 % | noventa e seis cento cento | tela (contagem, data ou passo) |
| T11 | cap10 | 18 kg | dezoito quilos | produção da semente da T11 (seção 13) |
| T11 | cap10 | 3.087,60 R$ | três mil e oitenta e sete reais e sessenta | produção da semente da T11 (seção 13) |
| T11 | cap10 | 6,43 R$ | seis reais e quarenta e três | produção da semente da T11 (seção 13) |
| T11 | cap10 | 26 | seis e vinte | tela (contagem, data ou passo) |
| T11 | cap10 | 18 kg | dezoito quilos | produção da semente da T11 (seção 13) |
| T11 | cap11 | 480 kg | quatrocentos e oitenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap11 | 498 | quatrocentos e noventa e oito | tela (contagem, data ou passo) |
| T11 | cap11 | 96,40 % | noventa e seis vírgula quatro cento cento | tela (contagem, data ou passo) |
| T11 | cap11 | 18 kg | dezoito quilos | produção da semente da T11 (seção 13) |
| T11 | cap11 | 480 | quatrocentos e oitenta | tela (contagem, data ou passo) |
| T11 | cap11 | 3,80 % | três vírgula oito cento cento | tela (contagem, data ou passo) |
| T11 | cap11 | 250 kg | duzentos e cinquenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap11 | 30 kg | trinta quilos | produção da semente da T11 (seção 13) |
| T11 | cap12 | 2 % | dois cento cento | tela (contagem, data ou passo) |
| T11 | cap12 | 0 | zero | tela (contagem, data ou passo) |
| T11 | cap12 | 250 kg | duzentos e cinquenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap13 | 2 | dois | tela (contagem, data ou passo) |
| T11 | cap13 | 2 | duas | tela (contagem, data ou passo) |
| T11 | cap13 | 80 kg | oitenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap13 | 50 kg | cinquenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap13 | 2 | duas | tela (contagem, data ou passo) |
| T11 | cap13 | 80 kg | oitenta quilos | produção da semente da T11 (seção 13) |
| T11 | cap14 | 500 kg | quinhentos quilos | produção da semente da T11 (seção 13) |
| T12 | cap03 | 3 | três | tela (contagem, data ou passo) |
| T12 | cap03 | 400 kg | quatrocentos quilos | frota e coletas (seções 3 e 12) |
| T12 | cap04 | 11 | onze | tela (contagem, data ou passo) |
| T12 | cap05 | 3 | três | tela (contagem, data ou passo) |
| T12 | cap05 | 400 kg | quatrocentos quilos | frota e coletas (seções 3 e 12) |
| T12 | cap05 | 9 | nove | tela (contagem, data ou passo) |
| T12 | cap05 | 3 | três | tela (contagem, data ou passo) |
| T12 | cap05 | 2 | dois | tela (contagem, data ou passo) |
| T12 | cap06 | 03 | 03 | tela (contagem, data ou passo) |
| T12 | cap06 | 05 | 05 | tela (contagem, data ou passo) |
| T12 | cap06 | 8 | oito | tela (contagem, data ou passo) |
| T12 | cap07 | 800 kg | oitocentos quilos | frota e coletas (seções 3 e 12) |
| T12 | cap07 | 10 | dez | tela (contagem, data ou passo) |
| T12 | cap08 | 7.100 kg | sete mil e cem quilos | frota e coletas (seções 3 e 12) |
| T12 | cap08 | 8.500 | oito mil e quinhentos | tela (contagem, data ou passo) |
| T12 | cap09 | 1 | uma | tela (contagem, data ou passo) |
| T12 | cap09 | 05 | 05 | tela (contagem, data ou passo) |
| T12 | cap09 | 06 | 06 | tela (contagem, data ou passo) |
| T12 | cap09 | 06 | 06 | tela (contagem, data ou passo) |
| T12 | cap09 | 8 | oito | tela (contagem, data ou passo) |
| T12 | cap10 | 6 | seis | tela (contagem, data ou passo) |
| T12 | cap10 | 5 | cinco | tela (contagem, data ou passo) |
| T12 | cap10 | 100 % | cem cento cento | tela (contagem, data ou passo) |
| T12 | cap10 | 5 | cinco | tela (contagem, data ou passo) |
| T12 | cap10 | 5 | cinco | tela (contagem, data ou passo) |
| T12 | cap11 | 24 | vinte e quatro | tela (contagem, data ou passo) |
| T12 | cap12 | 06 | 06 | tela (contagem, data ou passo) |
| T13 | cap01 | 5 | cinco | tela (contagem, data ou passo) |
| T13 | cap01 | 5 | cinco | tela (contagem, data ou passo) |
| T13 | cap02 | 4 | quatro | tela (contagem, data ou passo) |
| T13 | cap02 | 7 | 7 | tela (contagem, data ou passo) |
| T13 | cap02 | 7 dias | sete dias | tela (contagem, data ou passo) |
| T13 | cap02 | 2 | dois | tela (contagem, data ou passo) |
| T13 | cap03 | 5 | cinco | tela (contagem, data ou passo) |
| T13 | cap04 | 19 | dezenove | tela (contagem, data ou passo) |
| T13 | cap04 | 3.480 R$ | três mil quatrocentos e oitenta reais | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap04 | 19 | dezenove | tela (contagem, data ou passo) |
| T13 | cap05 | 180 R$ | cento e oitenta reais | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap06 | 7.080 R$ | sete mil e oitenta reais | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T13 | cap06 | 7.080 | sete mil e oitenta | tela (contagem, data ou passo) |
| T13 | cap06 | 23 | vinte e três | tela (contagem, data ou passo) |
| T13 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T13 | cap06 | 1 | uma | tela (contagem, data ou passo) |
| T13 | cap06 | 2.360 R$ | dois mil trezentos e sessenta reais | parcela dos pneus (T13) |
| T13 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T13 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T13 | cap07 | 2.300 R$ | dois mil e trezentos reais | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap07 | 12 | doze | tela (contagem, data ou passo) |
| T13 | cap07 | 12 | doze | tela (contagem, data ou passo) |
| T13 | cap07 | 12 | doze | tela (contagem, data ou passo) |
| T13 | cap07 | 3 | três | tela (contagem, data ou passo) |
| T13 | cap08 | 15 | quinze | tela (contagem, data ou passo) |
| T13 | cap08 | 15 | quinze | tela (contagem, data ou passo) |
| T13 | cap08 | 12 | doze | tela (contagem, data ou passo) |
| T13 | cap08 | 15 | quinze | tela (contagem, data ou passo) |
| T13 | cap09 | 1.874,30 R$ | mil oitocentos e setenta e quatro reais e trinta | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap09 | 1.740 R$ | mil setecentos e quarenta reais | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap09 | 30 | trinta | tela (contagem, data ou passo) |
| T13 | cap09 | 30 | trinta | tela (contagem, data ou passo) |
| T13 | cap10 | 4.870 R$ | quatro mil oitocentos e setenta reais | 2.608 × 1,25 + 1.000 × 0,98 + 600 × 1,05 (seção 7) |
| T13 | cap10 | 2.000 R$ | dois mil reais | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap10 | 2.870 | dois mil oitocentos e setenta | 4.870 − 2.000 (T13) |
| T13 | cap10 | 2.870 | dois mil oitocentos e setenta | 4.870 − 2.000 (T13) |
| T13 | cap10 | 300 kg | trezentos quilos | saldos (seção 10) e as contas que a T13 cria |
| T13 | cap10 | 3 | três | tela (contagem, data ou passo) |
| T13 | cap10 | 2 | duas | tela (contagem, data ou passo) |
| T13 | cap12 | 3 | três | tela (contagem, data ou passo) |
| T13 | cap13 | 4 | quatro | tela (contagem, data ou passo) |
| T13 | cap13 | 3 | três | tela (contagem, data ou passo) |
| T14 | cap01 | 2 | duas | tela (contagem, data ou passo) |
| T14 | cap02 | 5.000 R$ | cinco mil reais | bancos e OFX (seção 8) |
| T14 | cap03 | 2 | dois | tela (contagem, data ou passo) |
| T14 | cap03 | 18.500 R$ | dezoito mil e quinhentos reais | cofre em 10/11 (seção 8) |
| T14 | cap03 | 18.560 | dezoito mil quinhentos e sessenta | tela (contagem, data ou passo) |
| T14 | cap03 | 60 R$ | Sessenta reais | bancos e OFX (seção 8) |
| T14 | cap03 | 3 | três | tela (contagem, data ou passo) |
| T14 | cap03 | 60 R$ | sessenta reais | bancos e OFX (seção 8) |
| T14 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T14 | cap04 | 350 R$ | trezentos e cinquenta reais | bancos e OFX (seção 8) |
| T14 | cap04 | 8.000 R$ | Oito mil reais | bancos e OFX (seção 8) |
| T14 | cap04 | 2.000 R$ | Dois mil reais | bancos e OFX (seção 8) |
| T14 | cap04 | 6,50 R$ | seis reais e cinquenta | bancos e OFX (seção 8) |
| T14 | cap05 | 0 | zero | tela (contagem, data ou passo) |
| T14 | cap06 | 10 | dez | tela (contagem, data ou passo) |
| T14 | cap06 | 17 | dezessete | tela (contagem, data ou passo) |
| T14 | cap06 | 3 | três | tela (contagem, data ou passo) |
| T14 | cap07 | 2.250 R$ | dois mil duzentos e cinquenta reais | bancos e OFX (seção 8) |
| T14 | cap07 | 3 | três | tela (contagem, data ou passo) |
| T14 | cap07 | 8.000 | oito mil | tela (contagem, data ou passo) |
| T14 | cap08 | 238,40 R$ | duzentos e trinta e oito reais e quarenta | bancos e OFX (seção 8) |
| T14 | cap09 | 64,90 R$ | sessenta e quatro reais e noventa | bancos e OFX (seção 8) |
| T14 | cap10 | 9 | nove | tela (contagem, data ou passo) |
| T14 | cap10 | 4.815 R$ | quatro mil oitocentos e quinze reais | bancos e OFX (seção 8) |
| T14 | cap10 | 3 | três | tela (contagem, data ou passo) |
| T14 | cap10 | 4.815,20 R$ | quatro mil oitocentos e quinze reais e vinte | bancos e OFX (seção 8) |
| T14 | cap10 | 2 R$ | dois reais | bancos e OFX (seção 8) |
| T14 | cap10 | 20 ¢ | vinte centavos | bancos e OFX (seção 8) |
| T14 | cap11 | 2 linhas | duas linhas | tela (contagem, data ou passo) |
| T14 | cap11 | 12 R$ | doze reais | bancos e OFX (seção 8) |
| T14 | cap11 | 2 | duas | tela (contagem, data ou passo) |
| T14 | cap11 | 2 | duas | tela (contagem, data ou passo) |
| T14 | cap11 | 0 | zero | tela (contagem, data ou passo) |
| T14 | cap11 | 2 | duas | tela (contagem, data ou passo) |
| T14 | cap12 | 2 linhas | duas linhas | tela (contagem, data ou passo) |
| T14 | cap12 | 2 | dois | tela (contagem, data ou passo) |
| T14 | cap12 | 380 R$ | trezentos e oitenta reais | bancos e OFX (seção 8) |
| T14 | cap12 | 2 compras | duas compras | tela (contagem, data ou passo) |
| T14 | cap14 | 2 | dois | tela (contagem, data ou passo) |
| T14 | cap14 | 0 | zero | tela (contagem, data ou passo) |
| T14 | cap14 | 20 ¢ | vinte centavos | bancos e OFX (seção 8) |
| T14 | cap14 | 0 | zero | tela (contagem, data ou passo) |
| T14 | cap15 | 0 | zero | tela (contagem, data ou passo) |
| T15 | cap01 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap01 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap01 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap04 | 6.500 R$ | seis mil e quinhentos reais | outubro (seção 5) |
| T15 | cap04 | 19.800 R$ | dezenove mil e oitocentos reais | folha de outubro (seção 5) |
| T15 | cap04 | 7.700 R$ | sete mil e setecentos reais | outubro (seção 5) |
| T15 | cap04 | 2.800 R$ | dois mil e oitocentos reais | 950 + 1.850 (seção 5) |
| T15 | cap05 | 50.000 kg | cinquenta mil quilos | ferro pesado comprado em outubro (seção 5) |
| T15 | cap05 | 47.500 R$ | quarenta e sete mil e quinhentos reais | outubro (seção 5) |
| T15 | cap05 | 5 | cinco | tela (contagem, data ou passo) |
| T15 | cap06 | 6.500 R$ | seis mil e quinhentos reais | outubro (seção 5) |
| T15 | cap07 | 50 t | cinquenta toneladas | outubro (seção 5) |
| T15 | cap07 | 95 ¢ | noventa e cinco centavos | outubro (seção 5) |
| T15 | cap07 | 47.500 R$ | quarenta e sete mil e quinhentos reais | outubro (seção 5) |
| T15 | cap07 | 10 t | dez toneladas | outubro (seção 5) |
| T15 | cap07 | 1,25 R$ | um real e vinte e cinco | outubro (seção 5) |
| T15 | cap07 | 12.500 | doze mil e quinhentos | tela (contagem, data ou passo) |
| T15 | cap07 | 35.000 R$ | trinta e cinco mil reais | outubro (seção 5) |
| T15 | cap07 | 10 t | dez toneladas | outubro (seção 5) |
| T15 | cap07 | 9.500 | nove mil e quinhentos | tela (contagem, data ou passo) |
| T15 | cap07 | 3.000 | três mil | tela (contagem, data ou passo) |
| T15 | cap07 | 40 t | quarenta toneladas | outubro (seção 5) |
| T15 | cap07 | 38.000 R$ | trinta e oito mil reais | 256.860 − 218.860 (seção 5) |
| T15 | cap07 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap07 | 6.500 R$ | seis mil e quinhentos reais | outubro (seção 5) |
| T15 | cap07 | 31.500 R$ | trinta e um mil e quinhentos reais | outubro (seção 5) |
| T15 | cap07 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap07 | 38.000 R$ | trinta e oito mil reais | 256.860 − 218.860 (seção 5) |
| T15 | cap07 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap09 | 6 | seis | tela (contagem, data ou passo) |
| T15 | cap09 | 6 | seis | tela (contagem, data ou passo) |
| T15 | cap09 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap10 | 1 | um | tela (contagem, data ou passo) |
| T15 | cap10 | 2 | Duas | tela (contagem, data ou passo) |
| T15 | cap10 | 3.000 | três mil | tela (contagem, data ou passo) |
| T15 | cap10 | 850 R$ | oitocentos e cinquenta reais | outubro (seção 5) |
| T15 | cap10 | 2 | duas | tela (contagem, data ou passo) |
| T15 | cap12 | 2 | dois | tela (contagem, data ou passo) |
| T15 | cap12 | 6 | seis | tela (contagem, data ou passo) |
| T16 | cap02 | 3 | três | tela (contagem, data ou passo) |
| T16 | cap02 | 2 | dois | tela (contagem, data ou passo) |
| T16 | cap02 | 3 | três | tela (contagem, data ou passo) |
| T16 | cap03 | 1 | 1 | tela (contagem, data ou passo) |
| T16 | cap03 | 14 | catorze | tela (contagem, data ou passo) |
| T16 | cap03 | 2.027 | dois mil e vinte e sete | tela (contagem, data ou passo) |
| T16 | cap03 | 1 | 1 | tela (contagem, data ou passo) |
| T16 | cap04 | 2 | dois | tela (contagem, data ou passo) |
| T16 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T16 | cap05 | 0 | zero | tela (contagem, data ou passo) |
| T16 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T16 | cap06 | 1.248 | mil duzentos e quarenta e oito | tela (contagem, data ou passo) |
| T16 | cap06 | 1.248 | mil duzentos e quarenta e oito | tela (contagem, data ou passo) |
| T16 | cap06 | 0 | zero | tela (contagem, data ou passo) |
| T16 | cap06 | 1.249 | mil duzentos e quarenta e nove | tela (contagem, data ou passo) |
| T16 | cap07 | 2 | dois | tela (contagem, data ou passo) |
| T16 | cap08 | 5 doc | cinco documentos | tela (contagem, data ou passo) |
| T16 | cap08 | 5 | cinco | tela (contagem, data ou passo) |
| T16 | cap09 | 2 | dois | tela (contagem, data ou passo) |
| T16 | cap09 | 1.249 | mil duzentos e quarenta e nove | tela (contagem, data ou passo) |
| T16 | cap09 | 320 kg | Trezentos e vinte quilos | novembro, caixas e fiscal (seções 7, 9 e 11) |
| T16 | cap09 | 50 | dez e quarenta | tela (contagem, data ou passo) |
| T16 | cap09 | 3.328 R$ | três mil trezentos e vinte e oito reais | novembro, caixas e fiscal (seções 7, 9 e 11) |
| T16 | cap09 | 1.249 | mil duzentos e quarenta e nove | tela (contagem, data ou passo) |
| T16 | cap09 | 44 | quarenta e quatro | tela (contagem, data ou passo) |
| T16 | cap10 | 500 kg | quinhentos quilos | novembro, caixas e fiscal (seções 7, 9 e 11) |
| T16 | cap10 | 506 | quinhentos e seis | tela (contagem, data ou passo) |
| T16 | cap10 | 6 kg | seis quilos | novembro, caixas e fiscal (seções 7, 9 e 11) |
| T16 | cap10 | 500 kg | Quinhentos quilos | novembro, caixas e fiscal (seções 7, 9 e 11) |
| T16 | cap10 | 137 | quarenta e sete e noventa | tela (contagem, data ou passo) |
| T16 | cap10 | 23.950 R$ | vinte e três mil novecentos e cinquenta reais | 500 × 47,90 (seção 7) |
| T16 | cap10 | 1.250 | mil duzentos e cinquenta | fechamento do #84 (seção 9) |
| T16 | cap11 | 9 | nove | tela (contagem, data ou passo) |
| T16 | cap11 | 1.251 | mil duzentos e cinquenta e um | tela (contagem, data ou passo) |
| T16 | cap11 | 803,30 R$ | oitocentos e três reais e trinta | as três compras do #83 (seção 9) |
| T16 | cap11 | 64 kg | sessenta e quatro quilos | novembro, caixas e fiscal (seções 7, 9 e 11) |
| T16 | cap11 | 180 | cento e oitenta | tela (contagem, data ou passo) |
| T16 | cap11 | 410 | quatrocentos e dez | tela (contagem, data ou passo) |
| T16 | cap11 | 1.251 | mil duzentos e cinquenta e um | tela (contagem, data ou passo) |
| T16 | cap12 | 1.249 | mil duzentos e quarenta e nove | tela (contagem, data ou passo) |
| T16 | cap12 | 15 | quinze | tela (contagem, data ou passo) |
| T16 | cap12 | 24 h | vinte e quatro horas | tela (contagem, data ou passo) |
| T16 | cap12 | 1.250 | mil duzentos e cinquenta | fechamento do #84 (seção 9) |
| T16 | cap13 | 2 | dois | tela (contagem, data ou passo) |
| T16 | cap13 | 1.246 | mil duzentos e quarenta e seis | tela (contagem, data ou passo) |
| T16 | cap13 | 1.247 | mil duzentos e quarenta e sete | tela (contagem, data ou passo) |
| T16 | cap13 | 3 | três | tela (contagem, data ou passo) |
| T16 | cap13 | 1.246 | mil duzentos e quarenta e seis | tela (contagem, data ou passo) |
| T16 | cap13 | 1.247 | mil duzentos e quarenta e sete | tela (contagem, data ou passo) |
| T16 | cap14 | 2 | dois | tela (contagem, data ou passo) |
| T16 | cap14 | 2 | dois | tela (contagem, data ou passo) |
| T16 | cap15 | 1.984 R$ | mil novecentos e oitenta e quatro reais | 640 × 3,10 (seção 7) |
| T16 | cap16 | 2 | duas | tela (contagem, data ou passo) |
| T16 | cap16 | 2 | duas | tela (contagem, data ou passo) |
| T16 | cap18 | 1 | 1 | tela (contagem, data ou passo) |
| T16 | cap18 | 5 doc | cinco documentos | tela (contagem, data ou passo) |
| T16 | cap18 | 3 | três | tela (contagem, data ou passo) |
| T16 | cap18 | 0 | zero | tela (contagem, data ou passo) |
| T17 | cap01 | 2 | duas | tela (contagem, data ou passo) |
| T17 | cap02 | 6.380 kg | seis mil trezentos e oitenta quilos | tara do FKD2E41 (seção 3) |
| T17 | cap02 | 14.000 kg | catorze mil quilos | fiscal (seção 11) e frota (seção 3) |
| T17 | cap04 | 2 notas | duas notas | tela (contagem, data ou passo) |
| T17 | cap04 | 55.000 | cinquenta e cinco mil | tela (contagem, data ou passo) |
| T17 | cap04 | 380 R$ | trezentos e oitenta reais | fiscal (seção 11) e frota (seção 3) |
| T17 | cap04 | 5.800 kg | cinco mil e oitocentos quilos | fiscal (seção 11) e frota (seção 3) |
| T17 | cap07 | 6 | seis | tela (contagem, data ou passo) |
| T17 | cap07 | 1.850 R$ | mil oitocentos e cinquenta reais | NFS-e 13/14 ou latinha da filial (T17, T22) |
| T17 | cap07 | 14 | catorze | tela (contagem, data ou passo) |
| T17 | cap08 | 2 | duas | tela (contagem, data ou passo) |
| T17 | cap08 | 1.650 R$ | mil seiscentos e cinquenta reais | fiscal (seção 11) e frota (seção 3) |
| T17 | cap08 | 980 | novecentos e oitenta | cobre mel comprado em outubro (seção 5) |
| T17 | cap08 | 20 | vinte | tela (contagem, data ou passo) |
| T17 | cap09 | 71.000 | setenta e um mil | tela (contagem, data ou passo) |
| T17 | cap09 | 625 R$ | seiscentos e vinte e cinco reais | fiscal (seção 11) e frota (seção 3) |
| T17 | cap10 | 600 kg | seiscentos quilos | fiscal (seção 11) e frota (seção 3) |
| T17 | cap10 | 30 | trinta | tela (contagem, data ou passo) |
| T17 | cap10 | 3 | três | tela (contagem, data ou passo) |
| T17 | cap10 | 2 | dois | tela (contagem, data ou passo) |
| T17 | cap11 | 3 | três | tela (contagem, data ou passo) |
| T17 | cap11 | 21 notas | vinte e uma notas | tela (contagem, data ou passo) |
| T17 | cap11 | 12 | doze | tela (contagem, data ou passo) |
| T17 | cap11 | 9 | nove | tela (contagem, data ou passo) |
| T18 | cap01 | 2 | duas | tela (contagem, data ou passo) |
| T18 | cap01 | 2 | dois | tela (contagem, data ou passo) |
| T18 | cap02 | 2 | dois | tela (contagem, data ou passo) |
| T18 | cap03 | 3 | três | tela (contagem, data ou passo) |
| T18 | cap04 | 3.600 kg | três mil e seiscentos quilos | NF-e 1254 e MTR (seção 11) |
| T18 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T18 | cap04 | 3,60 | três vírgula seis | tela (contagem, data ou passo) |
| T18 | cap07 | 3 | três | tela (contagem, data ou passo) |
| T18 | cap07 | 3 | três | tela (contagem, data ou passo) |
| T18 | cap07 | 3 | três | tela (contagem, data ou passo) |
| T18 | cap08 | 2 | dois | tela (contagem, data ou passo) |
| T18 | cap09 | 3 doc | três documentos | tela (contagem, data ou passo) |
| T19 | cap01 | 4 | quatro | tela (contagem, data ou passo) |
| T19 | cap02 | 10 | dez | tela (contagem, data ou passo) |
| T19 | cap02 | 2.520 R$ | dois mil quinhentos e vinte reais | RH da T19 (seção 3) |
| T19 | cap02 | 600 R$ | seiscentos reais | RH da T19 (seção 3) |
| T19 | cap02 | 4.264 R$ | quatro mil duzentos e sessenta e quatro reais | RH da T19 (seção 3) |
| T19 | cap02 | 2.520 | dois mil quinhentos e vinte | tela (contagem, data ou passo) |
| T19 | cap03 | 220 R$ | duzentos e vinte reais | RH da T19 (seção 3) |
| T19 | cap03 | 6 % | seis cento cento | tela (contagem, data ou passo) |
| T19 | cap05 | 1.980 R$ | mil novecentos e oitenta reais | RH da T19 (seção 3) |
| T19 | cap05 | 200 R$ | duzentos reais | RH da T19 (seção 3) |
| T19 | cap05 | 1.780 | mil setecentos e oitenta | tela (contagem, data ou passo) |
| T19 | cap05 | 90 R$ | noventa reais | RH da T19 (seção 3) |
| T19 | cap05 | 1.980 | mil novecentos e oitenta | tela (contagem, data ou passo) |
| T19 | cap05 | 200 | duzentos | tela (contagem, data ou passo) |
| T19 | cap05 | 90 | noventa | tela (contagem, data ou passo) |
| T19 | cap05 | 1.690 | mil seiscentos e noventa | tela (contagem, data ou passo) |
| T19 | cap05 | 150 R$ | cento e cinquenta reais | RH da T19 (seção 3) |
| T19 | cap05 | 2.250 | dois mil duzentos e cinquenta | tela (contagem, data ou passo) |
| T19 | cap06 | 500 R$ | quinhentos reais | RH da T19 (seção 3) |
| T19 | cap06 | 250 | duzentos e cinquenta | tela (contagem, data ou passo) |
| T19 | cap06 | 100 R$ | cem reais | RH da T19 (seção 3) |
| T19 | cap06 | 500 | quinhentos | tela (contagem, data ou passo) |
| T19 | cap06 | 400 | quatrocentos | tela (contagem, data ou passo) |
| T19 | cap06 | 400 | quatrocentos | tela (contagem, data ou passo) |
| T19 | cap06 | 2.750 | dois mil setecentos e cinquenta | tela (contagem, data ou passo) |
| T19 | cap06 | 400 | quatrocentos | tela (contagem, data ou passo) |
| T19 | cap06 | 2.900 | dois mil e novecentos | tela (contagem, data ou passo) |
| T19 | cap07 | 2.800 | dois mil e oitocentos | 950 + 1.850 (seção 5) |
| T19 | cap07 | 2.900 | dois mil e novecentos | tela (contagem, data ou passo) |
| T19 | cap08 | 4 | quatro | tela (contagem, data ou passo) |
| T19 | cap08 | 6 | seis | tela (contagem, data ou passo) |
| T19 | cap08 | 2 | dois | tela (contagem, data ou passo) |
| T19 | cap08 | 1 | um | tela (contagem, data ou passo) |
| T19 | cap08 | 1 | um | tela (contagem, data ou passo) |
| T19 | cap10 | 5 | cinco | tela (contagem, data ou passo) |
| T19 | cap10 | 1 | uma | tela (contagem, data ou passo) |
| T19 | cap11 | 7 | sete | tela (contagem, data ou passo) |
| T19 | cap11 | 4 | quatro | tela (contagem, data ou passo) |
| T19 | cap11 | 10 min | dez minutos | tela (contagem, data ou passo) |
| T19 | cap11 | 8 | oito | tela (contagem, data ou passo) |
| T19 | cap11 | 5 | cinco | tela (contagem, data ou passo) |
| T20 | cap03 | 4 | 4 | tela (contagem, data ou passo) |
| T20 | cap03 | 2 | dois | tela (contagem, data ou passo) |
| T20 | cap03 | 2 | dois | tela (contagem, data ou passo) |
| T20 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T20 | cap04 | 2 | dois | tela (contagem, data ou passo) |
| T20 | cap05 | 71.651,58 R$ | setenta e um mil seiscentos e cinquenta e um reais e cinquen | 52.937,50 + 18.714,08 (T20) |
| T20 | cap05 | 15 | quinze | tela (contagem, data ou passo) |
| T20 | cap05 | 1 | zero e um | tela (contagem, data ou passo) |
| T20 | cap06 | 1.350 R$ | mil trezentos e cinquenta reais | cooperativa, coletas e a nota 1250 (seções 5, 7, 11 e 12) |
| T20 | cap06 | 90 dias | noventa dias | tela (contagem, data ou passo) |
| T20 | cap06 | 1.350 R$ | mil trezentos e cinquenta reais | cooperativa, coletas e a nota 1250 (seções 5, 7, 11 e 12) |
| T20 | cap06 | 30 | trinta | tela (contagem, data ou passo) |
| T20 | cap07 | 1.250 | mil duzentos e cinquenta | fechamento do #84 (seção 9) |
| T20 | cap07 | 8.400 kg | oito mil e quatrocentos quilos | cooperativa, coletas e a nota 1250 (seções 5, 7, 11 e 12) |
| T20 | cap07 | 2.600 | dois mil e seiscentos | tela (contagem, data ou passo) |
| T20 | cap07 | 18.755 R$ | dezoito mil setecentos e cinquenta e cinco reais | cooperativa, coletas e a nota 1250 (seções 5, 7, 11 e 12) |
| T20 | cap08 | 2.500 kg | dois mil e quinhentos quilos | 2.180 + 320 da transferência (T10) |
| T20 | cap09 | 4 | 4 | tela (contagem, data ou passo) |
| T20 | cap10 | 3.700 R$ | três mil e setecentos reais | cooperativa, coletas e a nota 1250 (seções 5, 7, 11 e 12) |
| T20 | cap10 | 2 | dois | tela (contagem, data ou passo) |
| T20 | cap11 | 4 | 4 | tela (contagem, data ou passo) |
| T21 | cap03 | 4 | quatro | tela (contagem, data ou passo) |
| T21 | cap03 | 10 | dez | tela (contagem, data ou passo) |
| T21 | cap03 | 118.600 R$ | cento e dezoito mil e seiscentos reais | Cato: seções 4, 5, 6, 7, 8 e 10 |
| T21 | cap03 | 67.600 | sessenta e sete mil e seiscentos | tela (contagem, data ou passo) |
| T21 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T21 | cap04 | 17.000 | dezessete mil | 18.500 − 1.500 (T6) |
| T21 | cap04 | 540 R$ | quinhentos e quarenta reais | Cato: seções 4, 5, 6, 7, 8 e 10 |
| T21 | cap04 | 14.000 | catorze mil | tela (contagem, data ou passo) |
| T21 | cap04 | 370 | trezentos e setenta | tela (contagem, data ou passo) |
| T21 | cap04 | 96.000 R$ | noventa e seis mil reais | Cato: seções 4, 5, 6, 7, 8 e 10 |
| T21 | cap04 | 132.000 R$ | cento e trinta e dois mil reais | Cato: seções 4, 5, 6, 7, 8 e 10 |
| T21 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T21 | cap05 | 3 | três | tela (contagem, data ou passo) |
| T21 | cap05 | 112.800 R$ | cento e doze mil e oitocentos reais | vendas de outubro à Fundição (seção 5) |
| T21 | cap05 | 14.000 | catorze mil | tela (contagem, data ou passo) |
| T21 | cap05 | 370 | trezentos e setenta | tela (contagem, data ou passo) |
| T21 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T21 | cap06 | 96.076 R$ | noventa e seis mil e setenta e seis reais | estoque de 10/11 a custo (seção 4) |
| T21 | cap06 | 2 | dois | tela (contagem, data ou passo) |
| T22 | cap00 | 2 | duas | tela (contagem, data ou passo) |
| T22 | cap00 | 2 | dois | tela (contagem, data ou passo) |
| T22 | cap00 | 2 | duas | tela (contagem, data ou passo) |
| T22 | cap02 | 30 dias | trinta dias | tela (contagem, data ou passo) |
| T22 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T22 | cap04 | 344.040 R$ | trezentos e quarenta e quatro mil e quarenta reais | 272.040 + 72.000 (T22) |
| T22 | cap04 | 370.000 | trezentos e setenta mil | tela (contagem, data ou passo) |
| T22 | cap04 | 690 | seiscentos e noventa | tela (contagem, data ou passo) |
| T22 | cap04 | 2 | duas | tela (contagem, data ou passo) |
| T22 | cap05 | 272.040 | duzentos e setenta e dois mil e quarenta | 269.240 + 2.800 (seção 5) |
| T22 | cap05 | 299.000 | duzentos e noventa e nove mil | tela (contagem, data ou passo) |
| T22 | cap05 | 690 | seiscentos e noventa | tela (contagem, data ou passo) |
| T22 | cap05 | 27.000 | vinte e sete mil | tela (contagem, data ou passo) |
| T22 | cap05 | 650 R$ | seiscentos e cinquenta reais | outubro da matriz (seção 5) e a filial da T22 |
| T22 | cap05 | 72.000 | setenta e dois mil | tela (contagem, data ou passo) |
| T22 | cap05 | 71.000 | setenta e um mil | tela (contagem, data ou passo) |
| T22 | cap05 | 1.000 R$ | mil reais | outubro da matriz (seção 5) e a filial da T22 |
| T22 | cap06 | 341.000 | trezentos e quarenta e um mil | tela (contagem, data ou passo) |
| T22 | cap06 | 240 | duzentos e quarenta | tela (contagem, data ou passo) |
| T22 | cap06 | 318.000 | trezentos e dezoito mil | tela (contagem, data ou passo) |
| T22 | cap06 | 860 | oitocentos e sessenta | compra de 09/11 (seção 7) |
| T22 | cap06 | 26.000 | vinte e seis mil | tela (contagem, data ou passo) |
| T22 | cap06 | 650 R$ | seiscentos e cinquenta reais | outubro da matriz (seção 5) e a filial da T22 |
| T22 | cap06 | 27.000 | vinte e sete mil | tela (contagem, data ou passo) |
| T22 | cap06 | 650 | seiscentos e cinquenta | tela (contagem, data ou passo) |
| T22 | cap06 | 1.000 | mil | tela (contagem, data ou passo) |
| T22 | cap07 | 273.000 | duzentos e setenta e três mil | tela (contagem, data ou passo) |
| T22 | cap07 | 860 | oitocentos e sessenta | compra de 09/11 (seção 7) |
| T22 | cap07 | 18.000 | dezoito mil | tela (contagem, data ou passo) |
| T22 | cap07 | 350 R$ | trezentos e cinquenta reais | outubro da matriz (seção 5) e a filial da T22 |
| T22 | cap07 | 45.000 | quarenta e cinco mil | 38.000 + 7.000 (T22) |
| T22 | cap07 | 2 | dois | tela (contagem, data ou passo) |
| T22 | cap08 | 2 | duas | tela (contagem, data ou passo) |
| T22 | cap08 | 640 kg | seiscentos e quarenta quilos | latinha da matriz em 10/11 (seção 4) ou a bateria de 05/11 |
| T22 | cap08 | 1.850 | mil oitocentos e cinquenta | NFS-e 13/14 ou latinha da filial (T17, T22) |
| T22 | cap08 | 2.490 | dois mil quatrocentos e noventa | 640 + 1.850 (T22) |
| T22 | cap09 | 2 | duas | tela (contagem, data ou passo) |
| T22 | cap09 | 2 | duas | tela (contagem, data ou passo) |
| T22 | cap10 | 1.200 kg | mil e duzentos quilos | outubro da matriz (seção 5) e a filial da T22 |
| T22 | cap10 | 1.840 kg | mil oitocentos e quarenta quilos | 640 + 1.200 (T22) |
| T22 | cap10 | 650 | seiscentos e cinquenta | tela (contagem, data ou passo) |
| T22 | cap12 | 2 | dois | tela (contagem, data ou passo) |
| T25 | cap00 | 3 | três | tela (contagem, data ou passo) |
| T25 | cap00 | 2 | duas | tela (contagem, data ou passo) |
| T25 | cap01 | 3 | três | tela (contagem, data ou passo) |
| T25 | cap01 | 12.380 R$ | doze mil trezentos e oitenta reais | 269.240 − 256.860 (seção 5) |
| T25 | cap02 | 2 | duas | tela (contagem, data ou passo) |
| T25 | cap02 | 6 | seis | tela (contagem, data ou passo) |
| T25 | cap02 | 10 | dez | tela (contagem, data ou passo) |
| T25 | cap02 | 10 dias | dez dias | tela (contagem, data ou passo) |
| T25 | cap02 | 31 | trinta e um | tela (contagem, data ou passo) |
| T25 | cap03 | 8 | oito | tela (contagem, data ou passo) |
| T25 | cap03 | 8 | oito | tela (contagem, data ou passo) |
| T25 | cap03 | 50.000 kg | cinquenta mil quilos | ferro pesado comprado em outubro (seção 5) |
| T25 | cap05 | 12 | doze | tela (contagem, data ou passo) |
| T25 | cap05 | 9 | nove | tela (contagem, data ou passo) |
| T25 | cap05 | 13 | treze | tela (contagem, data ou passo) |
| T25 | cap05 | 15 | quinze | tela (contagem, data ou passo) |
| T25 | cap05 | 20 | vinte | tela (contagem, data ou passo) |
| T25 | cap06 | 17 | dezessete | tela (contagem, data ou passo) |
| T25 | cap06 | 4.790 R$ | quatro mil setecentos e noventa reais | parcela da Fundição (seção 7) |
| T25 | cap06 | 23 | vinte e três | tela (contagem, data ou passo) |
| T25 | cap06 | 2.360 R$ | dois mil trezentos e sessenta reais | parcela dos pneus (T13) |
| T25 | cap06 | 5 | cinco | tela (contagem, data ou passo) |
| T25 | cap07 | 92 | quarenta e dois e cinquenta | tela (contagem, data ou passo) |
| T25 | cap07 | 137 | quarenta e sete e noventa | tela (contagem, data ou passo) |
| T25 | cap08 | 10 min | dez minutos | tela (contagem, data ou passo) |
| T25 | cap08 | 2 | duas | tela (contagem, data ou passo) |
| T25 | cap08 | 7 | 7 | tela (contagem, data ou passo) |
| T25 | cap08 | 8 | oito | tela (contagem, data ou passo) |
| T25 | cap09 | 2 | duas | tela (contagem, data ou passo) |
| T25 | cap10 | 2 h | duas horas | tela (contagem, data ou passo) |
| T25 | cap10 | 4 | quatro | tela (contagem, data ou passo) |
| T25 | cap10 | 2 | dois | tela (contagem, data ou passo) |
| T25 | cap10 | 4 | quatro | tela (contagem, data ou passo) |
| T25 | cap10 | 8 | oito | tela (contagem, data ou passo) |
| T25 | cap11 | 6 | seis | tela (contagem, data ou passo) |
| T25 | cap11 | 3 | três | tela (contagem, data ou passo) |
| T26 | cap01 | 5 | cinco | tela (contagem, data ou passo) |
| T26 | cap02 | 2 | duas | tela (contagem, data ou passo) |
| T26 | cap02 | 4 | quatro | tela (contagem, data ou passo) |
| T26 | cap03 | 5 | cinco | tela (contagem, data ou passo) |
| T26 | cap04 | 3 | três | tela (contagem, data ou passo) |
| T26 | cap05 | 2 | duas | tela (contagem, data ou passo) |
| T26 | cap07 | 3 | três | tela (contagem, data ou passo) |
| T26 | cap08 | 2 | dois | tela (contagem, data ou passo) |
| T26 | cap08 | 8.400 R$ | oito mil e quatrocentos reais | CRM da semente da T26 |
| T26 | cap08 | 12.000 kg | doze mil quilos | CRM da semente da T26 |
| T26 | cap08 | 30 | trinta | tela (contagem, data ou passo) |
| T26 | cap08 | 15 dias | quinze dias | tela (contagem, data ou passo) |
| T26 | cap10 | 3 | três | tela (contagem, data ou passo) |
| T26 | cap11 | 12 | doze | tela (contagem, data ou passo) |
| T26 | cap11 | 2 | dois | tela (contagem, data ou passo) |
| T26 | cap12 | 6 | seis | tela (contagem, data ou passo) |
| T26 | cap12 | 62.300 R$ | sessenta e dois mil e trezentos reais | CRM da semente da T26 |
| T26 | cap12 | 19.000 R$ | dezenove mil reais | CRM da semente da T26 |
| T26 | cap12 | 41.650 R$ | quarenta e um mil seiscentos e cinquenta reais | 980 × 42,50 (seção 5) |
| T26 | cap12 | 2 | dois | tela (contagem, data ou passo) |
| T26 | cap12 | 26.200 R$ | vinte e seis mil e duzentos reais | CRM da semente da T26 |
| T26 | cap13 | 4 | quatro | tela (contagem, data ou passo) |
| T27 | cap02 | 2 | duas | tela (contagem, data ou passo) |
| T27 | cap02 | 2 | duas | tela (contagem, data ou passo) |
| T27 | cap02 | 5 | cinco | tela (contagem, data ou passo) |
| T27 | cap05 | 4 | 4 | tela (contagem, data ou passo) |
