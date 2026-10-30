# Plano · T13 — Financeiro

- **Título final da aula:** Financeiro: contas, lançamentos, cartão e contas a pagar e receber
- **Áreas das vinhetas:** FINANCEIRO · CONTAS · LANÇAMENTOS · CARTÃO · CONTAS A PAGAR · CATEGORIAS · RESUMO
- **Objetivo (uma frase):** colocar o dinheiro da empresa no sistema: caixa e banco, o que entra e sai, a transferência
  entre contas, o cartão de crédito e o que ainda vai vencer.
- **Pré-requisito:** T12 (Portal do Cliente e Portal do Contrato). Aviso: "Antes: Portal do Cliente e Portal do Contrato".
  Usa clientes e fornecedor do T3 e as 12 parcelas do PMOC do T11.
- **Próximo:** T19 (Integração com Asaas, Assinaturas e Cobranças). Aviso: "Próximo: Integração com Asaas".
- **Duração estimada:** ~15 min de fala natural (14 blocos). Sem módulo pago (Financeiro está no plano Essencial); só
  "Cobranças" aparece com 🔒 e fica para o T19.
- Base: `T13/inventario.md` (código 1.38.6). Rótulos entre aspas = exatamente como na tela. DRE e DFC ficam no T20.

## Capítulos propostos

| # | Vinheta (área / título) | O que a tela mostra | Avisos na tela (positivos) | Duração |
|---|---|---|---|---|
| 0 | — | Menu "Financeiro" aberto, câmera na "Visão Geral". Fala: tudo o que entra, sai e ainda vai vencer, num lugar só. | "Antes: Portal do Cliente e Portal do Contrato" | 0:35 |
| 1 | FINANCEIRO / Onde fica cada coisa | Passa pelos itens "Visão Geral", "Movimentações Financeiras", "Contas a Pagar/Receber", "Cobranças" (zoom: T19), "Relatórios" (zoom: T20); zoom no botão "Configurações Financeiras" e no filtro "Este mês". | "Cada tela responde uma pergunta" | 0:50 |
| 2 | CONTAS / O caixa e o banco | "Movimentações Financeiras" → coluna "Contas e cartões" (já tem "Conta Principal") → "Nova conta": "Nome da Conta \*" Caixa da empresa; "Tipo" "Caixa"; "Saldo Inicial (R$)" 800,00; "Faz parte do caixa da empresa" (zoom, ligado); "Cor"; "Pré-visualização"; "Criar Conta". | "Saldo inicial = o que já existe hoje" | 1:10 |
| 3 | LANÇAMENTOS / Entrou dinheiro | "Nova movimentação" → "Receita" → "Nova Transação": "Categoria" Vendas de Serviços; "Descrição" Instalação de split 12.000 BTUs - Mercado Vila Nova; "Valor (R$)" 1.850,00; "Conta Bancária / Caixa \*" Conta Principal; "Forma de pagamento" "PIX"; "Data do lançamento" (zoom na dica); "Já foi recebido" ligado; "Mais detalhes" → "Cliente vinculado" Mercado Vila Nova; "Salvar". Linha nova no extrato. | "Cliente vinculado mostra de quem veio" | 1:10 |
| 4 | LANÇAMENTOS / Saiu dinheiro | "Nova movimentação" → "Despesa": "Categoria" CSP - Materiais; "Descrição" Gás R-410A e tubos de cobre; "Valor" 640,00; "Conta" Conta Principal; "Forma de pagamento" "Boleto"; "Já foi pago" desligado → "Irá para contas a pagar"; "Vencimento" +10 dias; "Fornecedor vinculado" Ventura Gás e Tubos; "Comprovantes / Notas Fiscais" (zoom); "Salvar". | "Desligado, vira conta a pagar" | 1:05 |
| 5 | LANÇAMENTOS / De uma conta pra outra | Visão Geral → "Transferir entre contas": "Origem" Conta Principal, "Destino" Caixa da empresa, "Valor (R$)" 300,00, "Descrição (opcional)" Troco do caixa; "Transferir". Extrato do caixa: "Saldo Após" (zoom). Menu ⋮ da conta: zoom em "Ajustar saldo". | "Transferência não é receita nem despesa" | 1:00 |
| 6 | CARTÃO / O cartão da empresa | Coluna → "Novo cartão": "Nome da Conta \*" Cartão Empresarial; "Dia de fechamento \*" 5; "Dia de vencimento \*" 15; frase "A fatura que fecha no dia 5 vence no dia 15 do mesmo mês." (zoom); "Limite de crédito (R$)" 10.000,00; "Criar Cartão". | "Compra no dia do fechamento já vai pra próxima fatura" | 1:00 |
| 7 | CARTÃO / Compra parcelada | "Nova movimentação" → "Despesa": "Conta" Cartão Empresarial → bloco "Despesa no Cartão de Crédito"; "Descrição" Bomba de vácuo e manifold; "Valor" 1.290,00; "Parcelas" 3x → linhas "1/3 → fatura de …" (zoom); "Data do lançamento" no mês anterior; "Salvar". | "Cada parcela cai na fatura certa" | 1:05 |
| 8 | CARTÃO / Pagar a fatura | Cartão Empresarial → fatura "Fechada" → "Pagar Fatura": "Pagar com \*" Conta Principal; "Valor a pagar" cheio; aviso "Fatura será completamente quitada"; "Confirmar Pagamento" → "Fatura quitada!" / "Pagamento registrado e limite do cartão liberado."; selo "Paga". | "Fatura paga devolve o limite" | 1:00 |
| 9 | CONTAS A PAGAR / O que vai vencer | "Contas a Pagar/Receber": abas "Todas", "A Pagar", "A Receber"; faixa "Vencidas", "Próximos 7 dias", "De 8 a 30 dias"; zoom em "Calendário" e "Exportar". "Nova Conta": "Tipo" "A Pagar"; "Descrição \*" Aluguel do galpão; "Valor (R$) \*" 2.800,00; "Vencimento" dia 10; "Categoria" Aluguel (criada na hora); "Conta Bancária / Caixa" Conta Principal; "Parcelar ou repetir" → "Recorrência" "Mensal", "Parcelas" 12; "Criar Conta". | "As 12 já entram na lista" | 1:15 |
| 10 | CONTAS A PAGAR / Pagar e receber | "A Pagar" → linha Gás R-410A → "Marcar pago" → "Confirmar pagamento" ("Pago com \*" Conta Principal, "Data do pagamento \*" hoje). "A Receber" → parcela "Mensalidade PMOC" do hotel → "Marcar recebido" → "Como foi recebido?" (zoom na dica do parcial) → "Forma de pagamento \*" "PIX", "Caixa / Conta bancária \*" Conta Principal → "Confirmar recebimento". | "Dica: dá pra receber só uma parte" | 1:15 |
| 11 | CATEGORIAS / Organizar as categorias | "Configurações Financeiras" → "Categorias": selo "Sistema" (zoom); "Nova categoria": "Nome \*" Peças e componentes; "Tipo \*" "Despesa"; "Onde aparece no DRE" "Custos diretos" + "Prévia no DRE" (zoom); "Criar"; "Adicionar subcategoria" (zoom). Aba "Centro de Custo" só citada. | "A categoria decide onde o valor aparece no DRE" | 1:05 |
| 12 | RESUMO / A visão geral do mês | Volta à "Visão Geral": "Saldo do Período", "A Receber", "A Pagar", "Saldo por Conta", "Fluxo realizado e resultado", "Projeção do caixa", "Agenda de vencimentos", "Concentração das despesas", "Últimas Movimentações". | "Tudo isso respeita o período lá em cima" | 1:00 |
| 13 | RESUMO / Recapitulando | Montagem: contas na coluna, extrato, fatura paga, lista de contas a pagar, Visão Geral. | "Próximo: Integração com Asaas" | 1:00 |

Transições faladas: 1→2 "Antes de lançar qualquer coisa, o sistema precisa saber de onde o dinheiro sai e pra onde ele
vai"; 2→3 "Conta criada; agora o primeiro dinheiro entrando"; 4→5 "E quando o dinheiro só muda de lugar?"; 5→6 "Agora o
cartão, que funciona diferente"; 8→9 "Fatura em dia; e o que ainda vai vencer?"; 10→11 "Pra tudo isso virar relatório, as
categorias contam muito". Recap → próximo: "Com as contas organizadas, dá pra cobrar o cliente por Pix, boleto ou cartão e
ver o dinheiro cair sozinho aqui. É o próximo tutorial."

**Falas dos cuidados ⚠️** (regra de 30/10 20:56: caminho certo primeiro, consequência numa frase, sem encenar falha):

| Cuidado | Fala sugerida | Na tela |
|---|---|---|
| Fatura parcial | "Pagando a fatura inteira, as compras dela ficam quitadas; se pagar só uma parte, elas esperam a quitação pra entrar no resultado." | Aviso "Fatura será completamente quitada" |
| Transferência | "Transferência é dinheiro mudando de lugar: aparece nas duas contas e fica fora das receitas e despesas." | Extrato com as duas pernas |
| Recorrência | "Escolhendo mensal com 12, o sistema já cria as 12 de uma vez, cada uma com o seu vencimento." | Lista com (1/12)…(12/12) |
| Pagar fatura | "A fatura libera o pagamento a partir do dia do fechamento." | Fatura "Fechada" |
| Excluir lançamento | "Quem tem a permissão de excluir lançamento consegue apagar; isso se ajusta nos cargos, lá no tutorial de usuários." | Zoom no "Excluir" do menu da linha |
| Plano | "O Financeiro já vem no plano Essencial; Cobranças é um módulo à parte, que a gente vê no próximo tutorial." | Item "Cobranças" no menu |

## Mundo fictício

**Começa com** (fim do T12, a alinhar com o T11): Glacial Cold Brasil, Camila (admin); clientes do seed (Mercado Vila Nova,
Hotel Mirante do Mar…), fornecedor Ventura Gás e Tubos (T3); contrato "PMOC - Hotel Mirante do Mar" com 12 parcelas de
R$ 1.200,00 a receber, categoria "Contratos PMOC" e conta "Conta Principal" (T11). Também as 14 categorias do sistema e os
6 grupos do DRE (o app cria sozinho ao cadastrar a empresa). Saldo inicial da "Conta Principal": R$ 18.500,00 (proposta,
gravado na semente do T11).

**Esta aula cria:**

| Item | Valores (fictícios) |
|---|---|
| Conta | Caixa da empresa · tipo Caixa · saldo inicial R$ 800,00 · faz parte do caixa |
| Receita | Instalação de split 12.000 BTUs - Mercado Vila Nova · Vendas de Serviços · R$ 1.850,00 · PIX · recebida hoje · Conta Principal |
| Despesa (a pagar → paga no cap. 10) | Gás R-410A e tubos de cobre · CSP - Materiais · R$ 640,00 · boleto · Ventura Gás e Tubos |
| Transferência | Conta Principal → Caixa da empresa · R$ 300,00 · "Troco do caixa" |
| Cartão | Cartão Empresarial · fecha dia 5 · vence dia 15 · limite R$ 10.000,00 · sem instituição (decisão 3) |
| Compra no cartão | Bomba de vácuo e manifold · categoria Ferramentas (criada na hora) · R$ 1.290,00 em 3x de R$ 430,00 · data no mês anterior |
| Pagamento de fatura | fatura fechada do cartão · integral · paga pela Conta Principal |
| Conta a pagar recorrente | Aluguel do galpão · categoria Aluguel · R$ 2.800,00 · mensal · 12 parcelas · dia 10 |
| Recebimento | 1ª parcela "Mensalidade PMOC" do Hotel Mirante do Mar · R$ 1.200,00 · PIX · Conta Principal |
| Categoria | Peças e componentes · Despesa · "Custos diretos" |

**Fica para as próximas:** contas e categorias (T19 escolhe a "Conta Principal" como destino das cobranças), a fatura e a
compra parcelada (T20 compara caixa × competência), o aluguel e as parcelas do PMOC (DFC previsto no T20).

## Gravação (modo fakebase)

**Já coberto:** tabelas do Financeiro no schema (inserts e updates genéricos); clientes, fornecedor e contrato; lista de
bancos (`handlers/ext/brasilapi.com.br.mjs:85-96`); preferência em `user_preferences`.

**Falta** (inventário 4.3), em ordem de prioridade:

1. Sementes: 14 categorias do sistema e 6 grupos do DRE (imitando os gatilhos do app) + "Conta Principal", "Contratos PMOC"
   e as 12 parcelas do T11 (alinhar com quem fizer as sementes do T11).
2. Handler da RPC `pay_credit_card_bill` (2 pernas com `transfer_pair_id`, fatura paga, compras quitadas com a data).
3. Hook de `financial_transactions` que recalcula `amount_received` da conta-mãe (só se o cap. 10 mostrar parcial; a
   proposta é receber inteiro e só citar o parcial).
4. Fatura fechada no dia da gravação: relógio do navegador congelado (TRILHA 5) num dia entre 6 e 14 do mês, com a compra
   do cap. 7 datada no mês anterior (cai na fatura que fechou no dia 5).
5. `seeds-extra/t13/apos-capNN.json` por capítulo. Desktop 1280×800. Downloads ("Exportar") não aparecem: só zoom.
6. Logo de banco: com "Instituição" vazia não há favicon de terceiro; se usar a cooperativa fictícia, conferir o handler
   `www.google.com.mjs`.

## Pronúncias novas para o TTS

| Tela / legenda | Texto do TTS |
|---|---|
| PIX | pix |
| CSP - Materiais | cê-ésse-pê materiais |
| R-410A | érre quatrocentos e dez á |
| 12.000 BTUs | doze mil bê-tê-ús (já registrado) |
| R$ 1.850,00 / R$ 2.800,00 | mil oitocentos e cinquenta reais / dois mil e oitocentos reais |
| 3x de R$ 430,00 | três vezes de quatrocentos e trinta reais |
| DRE | dê érri ê (já em uso) |

## Riscos e decisões para o Kaik

1. **Contas iniciais:** o T11 conta com "Caixa", "Conta Principal" e "Contratos PMOC" como padrões, mas o app não cria
   nenhuma conta. Proposta: a semente do T11 cria só "Conta Principal" e "Contratos PMOC" (o que as parcelas usam) e o T13
   cria o "Caixa da empresa" na tela. Confirmar e alinhar com o T11.
2. **Duração (~15 min, 14 blocos):** manter ou tirar "Ajustar saldo" (já é só zoom) e encurtar o cap. 1?
3. **Banco no cadastro:** deixar "Instituição" vazia (sem logo de terceiro) ou usar a "Cooperativa de Crédito Exemplo" do
   fakebase? Nomes de bancos reais aparecem na lista ao abrir o seletor.
4. **Conciliação e Importar planilha** (novos desde a 1.36.17): ficam fora (exigem enviar arquivo e muitas RPCs). Citar
   com um zoom no cap. 2, guardar para uma aula curta futura ou ignorar?
5. **Recebimento parcial:** só fala + zoom na dica (proposta) ou demonstrar (+0:30 e hook no fakebase)?
6. **Handoffs antes de gravar** (inventário 5): "Nova conta" × "Nova Conta" (dois sentidos); grupo OPEX padrão chamado
   "Despesas com pessoal"; Guia Técnico desatualizado (CSV e Nova Receita na Visão Geral, interruptor do cartão).
7. **Datas:** a trava de "Pagar Fatura", "Este mês" e "Vencidas" dependem do relógio do navegador; gravar com a data
   congelada do mundo (TRILHA 5).
