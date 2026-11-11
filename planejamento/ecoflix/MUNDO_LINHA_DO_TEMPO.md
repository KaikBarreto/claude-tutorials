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
