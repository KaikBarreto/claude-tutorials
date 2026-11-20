# Plano · T15 · Relatório Financeiro e DRE

- **Título:** Relatório Financeiro e DRE (o da fonte). Sem 🔒: Relatório e Categorias são da formação básica.
- **Áreas das vinhetas:** CATEGORIAS · CENTROS DE CUSTO · RELATÓRIO · DASHBOARD · DASHBOARD · DRE · DRE · PATRIMÔNIO ·
  EVOLUÇÃO · DFC · DFC · HISTÓRICO · HISTÓRICO · EXPORTAR · RESUMO.
- **Objetivo:** responder "ganhei ou perdi dinheiro no mês, e por quê?": plano de contas e centros de custo arrumados, o
  relatório de outubro lido aba por aba, o DRE nos dois regimes com o exemplo do pátio, e o histórico conferido e exportado.
- **Antes:** T14 · Bancos, cofre e conciliação bancária. **Próximo:** T21 · Cato, o assistente ("perguntar em português e
  receber a resposta pronta").
- **Duração:** alvo da fonte ~17 min; com a cobertura do 1.60.18 (DFC, organizar categorias do DRE, lançamentos em lote) ~25 min
  (fala de ~3.390 palavras, ~21,7 min de voz, mais 16 vinhetas; estimativa, o ensaio confirma).
- **Base:** `T15/inventario.md` (código 1.59.154, com os acréscimos do 1.60.18 em `cobertura_160.md`). Computador, janela de
  **1600×900**, logado como **Rafael Nogueira** (MASTER) a aula inteira. `FAKE_NOW=2026-11-10T08:30:00-03:00`; o mês lido é
  **outubro de 2026** ("Mês passado"). App gravado: EcoSistema **1.60.18**.

## Capítulos (17; os da fonte mais os da cobertura 1.60.18)
| # | Vinheta (área / título) | O que a tela mostra | Partida |
|---|---|---|---|
| 0 | (sem vinheta) | Dashboard do EcoSistema; ilustração do problema do pátio; cartão "Antes". | `inicio` |
| 1 | CATEGORIAS / O plano de contas | Categorias por grupo do DRE; cria **Frete de entrega** e **Máquinas e veículos** (Não compõe o DRE). | `inicio` |
| 2 | CENTROS DE CUSTO | Quatro centros (Coleta, Pátio, Produção criado ao vivo); lápis e lixeira; "Ativo". | `apos-cap01` |
| 3 | RELATÓRIO / O Relatório Financeiro | Lista de períodos, **cinco abas** (inclui DFC), "vs. período anterior", clique na coluna do gráfico, "Movimentações". | `apos-cap02` |
| 4 | DASHBOARD / O Dashboard do mês | "Resultado do Período", despesas e receitas por categoria (a energia em dobro). | `apos-cap02` + `setup` |
| 5 | DASHBOARD / Fornecedores, clientes e ticket | Ticket, tops ("Ver todos" clicado), materiais mais comprados e vendidos. | idem |
| 6 | DRE / Lendo o DRE | Escada do DRE; grupo aberto até o centro de custo (energia); "Valor · % receita". | idem |
| 7 | DRE / Organizando o DRE (novo) | Botão **Organizar categorias**: mover categoria de grupo, lote de lançamentos. | idem + `lote-categoria` conforme o ensaio |
| 8 | DRE / Caixa ou competência | Dicas, exemplo do pátio, faixa cinza, dica do CMV subestimado, troca para caixa. | idem |
| 9 | PATRIMÔNIO | "Patrimônio Operacional Atual"; "Exportar Patrimônio" (zoom). | idem |
| 10 | EVOLUÇÃO / Mês a mês | Evolução Mensal; comparar com ano passado / outro período; "Remover comparações". | idem |
| 11 | DFC / A DFC prevista (novo) | Aba DFC, visão prevista: contas a pagar e a receber por data. | idem |
| 12 | DFC / A DFC realizada (novo) | DFC realizada: de onde veio e para onde foi o dinheiro, por atividade. | idem |
| 13 | HISTÓRICO / O Histórico | Receitas, Despesas, Compras; busca "3850"; filtros com conta bancária; seta "Ver detalhes"; exclui a duplicata. | `apos-cap02` + `setup` |
| 14 | HISTÓRICO / Vários lançamentos de uma vez (novo) | Seleção em lote e troca de categoria (diesel), com a semente `lote-categoria`. | `apos-cap10` |
| 15 | EXPORTAR / Exportar em Excel e PDF | PDF do Histórico aberto na tela (`POPS` + `PDF_JS`), Fechamento completo, "Exportar" do DRE. | `apos-cap10` |
| 16 | RESUMO / Recapitulando | Montagem do que foi feito, com a DFC; cartão "Próximo: Cato". | trechos |

Capítulos antigos 7 a 12 viraram 8 a 16 (renumerados); 7, 11, 12 e 14 são novos. Durações: as do ensaio (`resumo.py --ens`).

Transições faladas: 0→1 "Tudo começa pelas categorias"; 1→2 "Com as categorias certas, dá pra saber em que o dinheiro foi
gasto"; 2→3 "Plano de contas pronto. Agora, o relatório"; 3→4 "Começando pelo Dashboard, a aba pra bater o olho"; 4→5 "Mais
embaixo ficam os números do movimento do pátio"; 5→6 "Agora, o DRE"; 6→7 "No cabeçalho do DRE fica um botão que gera muita
dúvida"; 7→8 "No pé do DRE"; 8→9 "Descendo mais, a Evolução Mensal"; 9→10 "Agora o Histórico"; 10→11 "Pra levar tudo pro
contador".

## Os cuidados da fonte (⚠️ e 🚫) e onde entram
| Cuidado | Capítulo | Na tela |
|---|---|---|
| ⚠️ Exemplo do pátio (obrigatório) | 7 | ilustração com os números do ferro pesado de outubro; depois o DRE real trocando de regime |
| ⚠️ CAPEX, principal de empréstimo e distribuição de lucro fora do DRE; só os juros; parcela mista = dois lançamentos | 1 | ilustração + a categoria Máquinas e veículos em "Não compõe o DRE" |
| ⚠️ O relatório não inventa número: comece pelo Histórico | 10 (semeado no 4) | a energia em dobro no Dashboard e as duas linhas no Histórico |
| ⚠️ O patrimônio ignora o período e é projeção | 8 | ilustração da foto de agora |
| ⚠️ O Histórico não repete o dinheiro que espelha compra ou venda; extrato no "Histórico do Caixa" | 10 | ilustração |
| ⚠️ Subcategoria com grupo do DRE próprio; selo quando diverge | 1 | o selo e a nota no cartão do Frete |
| ⚠️ Na comparação, a linha casa pelo nome da categoria | 9 | depois do "Aplicar comparação" |
| ⚠️ Excluir centro de custo só tira a marcação; o certo é desativar | 2 | zoom no "Ativo" |
| ⚠️ Sem "Ver Totais e Valores Financeiros", só "Acesso Restrito" | 3 | só falado (sem trocar de usuário) |
| 🚫 Sem depreciação, livro do imobilizado nem ganho ou perda na venda de ativo | 1 | falado no positivo: fica com o contador |

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md`; tudo fictício, sem documento novo (nenhum CPF, CNPJ ou e-mail novo). A fala cita os valores
marcados com **(falado)**: o mundo tem de bater no centavo.

**Categorias (semente, antes da aula)**, com grupo do DRE / grupo da DFC:
- Receita: **Aluguel de caçamba** (outras receitas / Atividades operacionais) e as do sistema (cadeado), como "Outras Receitas".
- Despesa: **Impostos sobre vendas** (Impostos e deduções); **Frete** (Custos adicionais: o frete de compra); **Folha salarial**,
  **Aluguel**, **Energia elétrica**, **Combustível**, **Manutenção de veículos**, **Telefone e internet** (Despesas
  operacionais) e as do sistema ("Tarifas", "Outras Despesas", também em Despesas operacionais, para a lista ter só as
  divisórias "Impostos e deduções", "Custos adicionais" e "Despesas operacionais (OPEX)"; nomes da ajuda do app, conferir na
  criação da empresa). Todas
  com `dre_group_id` apontando para o grupo do sistema da natureza certa em `dre_groups` (um por natureza; nomes de produção
  ou, na falta, os de `lib/dreHierarchy.ts:119-125`). Nenhuma categoria em "Não compõe o DRE" antes da aula.

**Centros de custo (semente):** **Coleta** (azul #3B82F6, "Caminhões, caçambas e motoristas") e **Pátio** (âmbar #F59E0B,
"Balança, separação e armazenagem"), ativos desde agosto.

**Outubro de 2026, o mês do exemplo** (regras: sem cartão de crédito, empréstimo, aporte ou retirada no mês; todo material
com custo de compra, para não aparecer o aviso do CMV; preço único por material, o da tabela do mundo):
| Material | Comprado (kg) | Vendido (kg) |
|---|---|---|
| Ferro pesado | **50.000 (falado)**: 42.000 do Depósito Irmãos Siqueira (dois lotes de 21.000, 14/10 e 21/10), 4.180 do Valdir (com os 180 de 22/10, a do T10) e 3.820 do balcão | **10.000 (falado)**, para a Aços Quiririm |
| Os outros 14 materiais (junção: o outubro do T10 e do T4, `MUNDO_LINHA_DO_TEMPO.md`) | ferro misto 40.900, chaparia 16.850, cobre mel 980, cobre misto 700, fio de cobre encapado 600, latinha 3.250, perfil 2.020, bloco 1.000, metal amarelo 500, bronze 200, inox 1.200, bateria 1.320, papelão 15.400, PET 2.600 | ferro misto 38.612, chaparia 16.100, cobre mel 1.000, cobre misto 700, fio 600, latinha 3.250, perfil 2.673, bloco 1.000, metal amarelo 500, bronze 200, inox 1.200, bateria 0, papelão 15.400, PET 2.427 (a sobra e a falta desses 14 se anulam a custo: o estoque a mais é o do ferro pesado) |

Daí: compras R$ 256.860,00; vendas R$ 269.240,00; CMV R$ 218.860,00; estoque a mais no mês, a custo, **R$ 38.000,00
(falado)** (só o ferro pesado). Clientes de outubro (vendas): Fundição Bandeira do Vale R$ 112.800,00 / 3.000 kg (cobres, metal
amarelo, bronze); Aços Quiririm Ltda R$ 77.460,60 / 65.912 kg (ferros, chaparia, inox); Serra Fina Alumínio Reciclagem
R$ 60.349,20 / 6.923 kg (alumínio); Depósito Irmãos Siqueira R$ 18.630,20 / 17.827 kg (papelão e PET; a bateria de outubro
ficou no pátio, como mostra o T10).
**(falado)** "Top Fornecedores" em R$: 1º Depósito Irmãos Siqueira (nenhum outro, nem "Não informado", passa dele).
"Top Clientes": 1º em R$ Fundição Bandeira do Vale; 1º em kg Aços Quiririm Ltda. "Materiais + Comprados": 1º Ferro pesado,
50.000 kg, R$ 47.500,00; "Materiais + Vendidos": 1º Cobre mel, e o ferro pesado fora dos cinco primeiros.

Lançamentos de outubro (caixa ou banco, todos pagos no mês, com categoria):
| Categoria | Valor | Centro de custo |
|---|---|---|
| Folha salarial | R$ 19.800,00 **(falado)** | Pátio 14.300,00 · Coleta 3.100,00 · sem centro 2.400,00 |
| Aluguel | R$ 6.500,00 | Pátio |
| Energia elétrica | **R$ 3.850,00 duas vezes (falado)**: "Conta de energia", Conta Principal, 13/10/2026 09:12 e 16:40, iguais (a das 16:40 só no estado do T15); nenhuma conciliada (T14) nem ligada a conta a pagar | Pátio |
| Combustível | R$ 4.280,00 | Coleta |
| Manutenção de veículos | R$ 1.950,00 | Coleta |
| Telefone e internet | R$ 289,90 | sem centro |
| Tarifas | R$ 186,00 | sem centro |
| Impostos sobre vendas | R$ 3.574,10 | sem centro |
| Frete (custos adicionais) | R$ 2.400,00 | sem centro |
| Aluguel de caçamba (receita) | R$ 2.800,00 **(falado)** | Coleta |

DRE de outubro que sai disso (conferido em script):
| Linha | Competência | Caixa |
|---|---|---|
| 01 Receita Bruta (Vendas) | 269.240,00 | 269.240,00 |
| 02 Impostos e Deduções | 3.574,10 | 3.574,10 |
| 03 = Receita Líquida | 265.665,90 | 265.665,90 |
| 04 Custos Operacionais (CMV / Compras de materiais + Frete) | 221.260,00 (218.860,00 + 2.400,00) | 259.260,00 (256.860,00 + 2.400,00) |
| 05 = Lucro Bruto | 44.405,90 | 6.405,90 |
| 06 Despesas Operacionais (Total do Dashboard) | 40.705,90 | 40.705,90 |
| 07 Outras Receitas e Despesas | 2.800,00 | 2.800,00 |
| 08 = Resultado do Período | **6.500,00 (falado)** | **−31.500,00 (falado)** |

Depois do capítulo 10 (sem a duplicata): competência R$ 10.350,00 e caixa −R$ 27.650,00 (não falados). Centros de custo de
outubro (aba "Centros de Custo", competência): Pátio despesas R$ 28.500,00; Coleta despesas R$ 9.330,00 e receitas
R$ 2.800,00; sem centro R$ 6.450,00 (a fala diz só que o pátio gastou mais e a coleta trouxe a receita do aluguel de caçamba).

**Setembro e agosto:** compras abaixo das de outubro; resultado de setembro positivo e acima do de outubro nas duas contas
(competência e caixa), para a "Evolução Mensal" e a comparação. **Hoje (10/11):** contas a receber com o fiado da Fundição
Bandeira do Vale **(falado)**; o resto do patrimônio é o do mundo (não falado).

**Criado ao vivo:** capítulo 1, as categorias **Frete de entrega** (sub de Frete, "Despesas operacionais (OPEX)", "Atividades
operacionais", herda cor e ícone) e **Máquinas e veículos** (Despesa, "Não compõe o DRE", "Atividades de investimento", cor
padrão #6B7280, ícone padrão); capítulo 2, o centro de custo **Produção** (roxo #8B5CF6, "Prensa de latinha e papelão",
ativo); capítulo 10, a exclusão da "Conta de energia" das 16:40 (o saldo da conta bancária sobe R$ 3.850,00, como no banco de
verdade). Sementes: `inicio` (fim do T14 + o acima), `apos-cap01`, `apos-cap02`, `apos-cap10` (= estado final; o T21 parte
dele; consolidar no `MUNDO_FICTICIO.md`). Os capítulos 3 a 9 e 11 só leem.

## Gravação
- Rotas: `/dashboard` (abertura), `/categorias-financeiras`, `/relatorio-financeiro`. Sem celular, sem página pública, sem
  outro usuário. Nada de Windows nem EcoTray. Nenhuma edge function: só tabelas e RPCs.
- **`setup` fora do vídeo** (cada capítulo abre um navegador novo e o período volta a "Este mês"): capítulos 4 a 11 abrem o
  relatório, escolhem "Mês passado" e a aba de partida (`localStorage` "financial-report-tab"); no capítulo 3 o
  `localStorage` começa sem a chave (abre no "Dashboard").
- Backend falso (o SQL não está na cópia do app; reproduzir pelo contrato do front, `inventario.md` § 4):
  1. `get_financial_dre_summary` nos dois regimes, com `costBasis`, CMV pelo custo de compra do material vendido,
     `revenueCategories` com `costCenters`, rankings, tickets, `stockCostReliable` true; também o de setembro.
  2. `get_dre_expenses_by_group` (impostos, custos adicionais, despesas operacionais, não operacionais; "Não compõe o DRE" fora).
  3. `get_dre_expense_lines` / `get_dre_revenue_lines` com a mesma régua, sem o dinheiro que espelha compra, venda, vale ou
     baixa de saldo; `get_financial_dre_cost_center_breakdown` (competência).
  4. `get_company_patrimony` (foto de 10/11) e `get_monthly_financial_evolution` (`p_months` 6: jun/26 a nov/26, junho e
     julho zerados se o histórico começa em agosto).
  5. Ao gravar `financial_categories.dre_group`, preencher `dre_group_id` com o grupo do sistema da natureza (a lista e o DRE
     dependem dele); `dre_layout_*` vazias.
  6. Excluir: as leituras do grupo (`bank_transactions`, `bill_payments`, `bill_payment_groups`, `cash_transactions`,
     `balance_movements`) e `delete_bank_transaction_atomic` (apaga e ajusta o saldo).
  7. O PDF do Histórico abre numa aba nova (`window.open`): [TESTAR] se o gravador mostra a aba; senão o capítulo 11 para
     no aviso "PDF gerado em nova aba". Os exports do DRE baixam arquivo: só o menu aberto, sem clicar. "Fechamento completo
     (Excel)" e "Exportar Patrimônio": só zoom.
- Ilustrações (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`: fundo branco, Montserrat, acento #50D088, objetos
  genéricos, nunca tela do app), presas às frases do roteiro: o mês do pátio (0), plano de contas e nem toda saída é despesa
  (1), as frentes do pátio (2), ticket médio (5), a escada do DRE (6), o exemplo do pátio (7), a foto de agora (8), o mesmo
  dinheiro não conta duas vezes (10).

## Pronúncias
Da tabela do PERFIL: DRE "dê-érri-ê", PDF "pê-dê-éfe", EcoSistema "Ecossistema", Cato "Cáto". Novas (testar num trecho
curto): **CMV "cê-ême-vê"** e **Excel "ékisel"** (o da Domiflix, outra voz). "Dashboard", "Ticket" e "Top" na escrita normal.

## Riscos e decisões para o Kaik
1. **DFC**: decidido pela cobertura 1.60.18: dois capítulos (11 e 12). Os valores falados só depois do ensaio.
2. **A energia em dobro**: o "lançamento errado" do capítulo 10 é uma duplicata semeada em outubro (exclusão completa, sem
   refazer nada). Se o T14 concilia outubro, ela precisa ficar fora da conciliação.
3. **Números de outubro falados** (6.500,00 e −31.500,00; 50.000 kg; 19.800,00; 7.700,00; 2.800,00): exigem o mundo no
   centavo; o ensaio gravado confere antes da voz.
4. **"Acesso Restrito"**: só falado (mostrar exige um usuário com a tela e sem a permissão; Marcos e Juliana não servem).
5. Handoff (a fala não depende): o diálogo de excluir do Histórico diz "o saldo da conta a conta bancária será ajustado"
   (`RevenueExpenseList.tsx:1199`); a ajuda do app cita "Configurar DRE", "Nova Categoria" e a etiqueta "Sistema", que não
   existem mais na tela.

## Acréscimos do 1.60.18 (mundo desta aula)
- Handlers novos (só T15): `get_company_dre_configuration` (modo legado), `update_financial_transaction_category`,
  `update_financial_transaction_categories_batch`, `get_accounting_closing_open_bills`, `get_financial_accounting_report`.
- Semente nova `lote-categoria` (três lançamentos de diesel com a categoria errada, capítulo 14); DFC prevista usa as
  `financial_bills` do mundo (água vencida, energia, fiado da Fundição Bandeira do Vale).
- Pedido ao mundo base: `linhasDRE` sem `bank_account_id/name`; sem isso o filtro e o campo "Conta bancária" do Histórico
  aparecem vazios.
- Não há o cartão "Lucro Líquido" nesta aula (só "Resultado do Período", o mesmo número da DRE em competência).
