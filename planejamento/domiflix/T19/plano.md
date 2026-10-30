# Plano · T19 — Integração com Asaas, Assinaturas e Cobranças

- **Título final da aula:** Cobranças com o Asaas: link de pagamento, assinaturas e baixa automática
- **Áreas das vinhetas:** COBRANÇAS · ASAAS · ASSINATURAS · CONTRATOS · RESUMO
- **Objetivo (uma frase):** conectar a conta Asaas da empresa e cobrar o cliente por Pix, boleto ou cartão, uma vez ou todo
  mês, com o recebimento entrando sozinho no Financeiro.
- **Pré-requisito:** T13 (Financeiro). Aviso: "Antes: Financeiro". Usa a "Conta Principal", as categorias e as parcelas do
  PMOC (T11/T13).
- **Próximo:** T20 (Relatório Financeiro e DRE). Aviso: "Próximo: Relatório Financeiro e DRE".
- **Duração estimada:** ~14 min de fala natural (13 blocos). 🔒 Add-on **Cobranças online** (contratado à parte).
- Base: `T19/inventario.md` (código 1.38.6). Rótulos entre aspas = exatamente como na tela. Tudo com o Asaas **simulado**
  no fakebase; nenhuma chave real.

## Capítulos propostos

| # | Vinheta (área / título) | O que a tela mostra | Avisos na tela (positivos) | Duração |
|---|---|---|---|---|
| 0 | — | Menu "Financeiro" → "Cobranças" com "Ative os recebimentos primeiro". Fala: mandar um link e ver o pagamento cair sozinho. | "Antes: Financeiro" · "Módulo Cobranças online" | 0:35 |
| 1 | COBRANÇAS / Como o dinheiro chega | Ilustração: cliente paga pelo link → dinheiro na conta Asaas da empresa → "Pago" no Financeiro. Na tela, zoom em "A Dominex não retém nada por transação." (cap. 3). | "O dinheiro cai na sua conta" | 0:45 |
| 2 | ASAAS / Conectar a conta | Botão "Configurações" (rodapé do menu) → aba "Integrações" (abre no WhatsApp) → "Cobranças (Asaas)" → "Configurações": card "Recebimentos (Asaas)"; abre "Como consigo minha chave de API da Asaas?" (zoom nos 4 passos); cola a chave fictícia em "Chave de API da Asaas" (borrada na edição); "Ativar recebimentos" → "Recebimentos ativados!"; selo "Ativo". | "A chave fica com o Asaas e a integração" | 1:10 |
| 3 | ASAAS / Para onde vai o dinheiro | "Falta escolher a conta que recebe o dinheiro" → "Escolher agora" → "Lançamento no Financeiro": "Conta bancária de destino" Conta Principal; "Categoria da receita" Vendas de Serviços; "Categoria da taxa (Asaas)" Tarifas e Taxas; "Salvar". Zoom nos interruptores "Lançar cobranças no Financeiro automaticamente" e "Lançar a taxa da Asaas como despesa" (ligar o segundo). | "Cobrança paga vira receita sozinha" | 1:10 |
| 4 | ASAAS / Taxas e preferências | Card "Taxas da Asaas" ("Atualizar taxas" → "Taxas atualizadas com a Asaas."); "Multa e juros por atraso" (2 % e 1 %); "Preferências de cobrança": "Vencimento padrão" 3 dias, "Meios de pagamento habilitados" Pix, Boleto, Cartão de crédito; zoom em "Desconto por antecipação". | "Vale para as próximas cobranças" | 1:00 |
| 5 | ASAAS / O simulador | Botão "Simulador": "Valor da venda" 1.200,00; "Forma de pagamento" "Cartão"; "Parcelas" 3x; "Quem paga a taxa" "A empresa absorve" → "Valor líquido na sua conta", "Quando o dinheiro cai na sua conta"; troca para "Pix" (zoom no líquido). | "Estimativa com as taxas da sua conta" | 1:00 |
| 6 | COBRANÇAS / Uma cobrança avulsa | Financeiro → "Cobranças" → "Nova cobrança": "Cobrança": "Cliente" Restaurante Sabor da Serra, "Valor" 450,00, "Vencimento" +3 dias, "Descrição" Limpeza e higienização de 2 splits da cozinha; "Avançar" → "Pagamento": "Cliente escolhe"; "Avançar" → "Encargos" (multa e juros já vieram); "Avançar" → "Financeiro": "Lançar no financeiro" "Sim"; zoom no "Resumo do recebimento"; "Gerar cobrança". | "O resumo mostra quanto você recebe" | 1:20 |
| 7 | COBRANÇAS / Mandar o link | Quadro "Cobrança gerada": QR, "Link de pagamento", "Copiar link" → "Link copiado!"; zoom em "Enviar por WhatsApp". Lista: linha "A receber", "Cliente escolhe". | "Dá pra mandar pelo WhatsApp" | 0:45 |
| 8 | COBRANÇAS / O que o cliente vê | Deslogado, `/pagar/<código>`: marca da Glacial, "Valor a pagar", "Vencimento"; "Pix" → QR e "Copiar código Pix"; volta e mostra "Boleto" e "Cartão" (sem pagar). Corte: pagamento simulado → a mesma página vira "Pagamento confirmado". | "O cliente escolhe como pagar" | 1:00 |
| 9 | COBRANÇAS / Pago e baixado | Logado: "Cobranças" com "Pago" e o card "Recebido"; Contas a Pagar/Receber → "A Receber": a conta "Pago"; Movimentações: a receita e a taxa em "Tarifas e Taxas". Menu da linha: "Copiar link", "Estornar" (zoom, sem clicar). | "A baixa vem sozinha do Asaas" | 1:00 |
| 10 | ASSINATURAS / Cobrança todo mês | Aba "Assinaturas" → "Nova assinatura": "Cliente" Academia Ponto Forte; "Valor" 380,00; "Frequência" "Mensal"; "Forma de pagamento" "Cliente escolhe"; "1º vencimento" dia 10 do mês seguinte; "Duração" "Contínua"; "Descrição" Manutenção mensal dos splits; zoom no "Resumo por cobrança"; "Criar assinatura" → "Assinatura criada". Topo: "Receita recorrente mensal (MRR)". | "Uma assinatura, uma cobrança por mês" | 1:10 |
| 11 | ASSINATURAS / Editar e cancelar | Ações da linha: "Editar" → "Editar assinatura" (zoom no cliente travado) → "Cancelar"; "Cancelar" → janela "Cancelar assinatura" → "Voltar". | "O histórico fica no Financeiro" | 0:45 |
| 12 | CONTRATOS / A parcela do contrato | Contratos → "PMOC - Hotel Mirante do Mar" → "Financeiro" → 2ª parcela → "Cobrar online" → aviso "Esta cobrança é da parcela do contrato…" → "Gerar cobrança"; selo "Cobrança gerada". Zoom: "Cobrar o saldo" em Contas a Receber e "Faturar" da OS. | "Pagou, a parcela baixa sozinha" | 1:00 |
| 13 | RESUMO / Recapitulando | Montagem: integração "Ativo", cobrança "Pago", assinatura ativa, parcela com cobrança. | "Próximo: Relatório Financeiro e DRE" | 1:00 |

Transições faladas: 1→2 "Pra começar, a gente liga a conta Asaas da empresa"; 3→4 "Conta escolhida; agora as condições
de cada cobrança"; 5→6 "Hora de cobrar de verdade"; 7→8 "E do lado do cliente, o que aparece?"; 9→10 "E pra quem paga todo
mês?"; 11→12 "Lembra das parcelas do contrato PMOC?". Recap → próximo: "Com o dinheiro entrando e saindo, o próximo passo é
ler o resultado: o DRE e o fluxo de caixa. É o próximo tutorial."

**Falas dos cuidados ⚠️** (regra de 30/10 20:56: caminho certo primeiro, consequência numa frase, sem encenar falha):

| Cuidado | Fala sugerida | Na tela |
|---|---|---|
| CPF/CNPJ do cliente | "Pra gerar a cobrança, o cliente precisa ter CPF ou CNPJ no cadastro: é o dado que o Asaas pede." | Cliente com CNPJ |
| Baixa pelo Asaas | "Quando o cliente paga, é o Asaas que avisa o sistema, e aí a cobrança vira paga aqui sozinha." | "Pago" na lista |
| Taxas reais | "Essas são as taxas da sua conta; é só tocar em Atualizar taxas quando o Asaas mudar." | Card "Taxas da Asaas" |
| Conta de destino | "Escolhendo a conta que recebe, toda cobrança paga entra direto no Financeiro." | "Conta bancária de destino" |
| Cancelar assinatura | "Cancelando, as próximas cobranças deixam de ser geradas; o que já foi pago continua no histórico." | Janela "Cancelar assinatura" |
| Pix Automático (se as opções aparecerem) | "No Pix Automático, o cliente autoriza no banco; cancelando aqui, é só conferir se a autorização também foi encerrada." | Zoom no selo "Autorização ativa no banco" |

## Mundo fictício

**Começa com** (fim do T13): Glacial Cold Brasil (CNPJ fictício 91.520.340/0001-07), Camila (admin), "Conta Principal" e
"Caixa da empresa", categorias do sistema ("Vendas de Serviços", "Tarifas e Taxas"), contrato PMOC do hotel com a 1ª parcela
recebida (T13) e as outras 11 a receber, clientes do seed com CNPJ válido. Módulo `cobrancas` ligado (seed). **Sem conta
Asaas conectada** (decisão 1).

**Esta aula cria:**

| Item | Valores (fictícios) |
|---|---|
| Conta Asaas | chave fictícia visivelmente falsa (ex.: `$aact_exemplo_glacial_0000`, borrada na edição) · status "Ativo" · conta de destino Conta Principal · receita em Vendas de Serviços · taxa em Tarifas e Taxas · lançar taxa ligado · multa 2 % · juros 1 % · vencimento padrão 3 dias |
| Cobrança avulsa | Restaurante Sabor da Serra · R$ 450,00 · vence em +3 dias · "Limpeza e higienização de 2 splits da cozinha" · "Cliente escolhe" · paga por Pix (simulado) · taxa fictícia R$ 1,99 |
| Assinatura | Academia Ponto Forte · R$ 380,00 · Mensal · contínua · 1º vencimento dia 10 do mês seguinte · "Manutenção mensal dos splits" |
| Cobrança de contrato | 2ª parcela "Mensalidade PMOC" do Hotel Mirante do Mar · R$ 1.200,00 · forma em aberto · "A receber" |

**Fica para as próximas:** a assinatura ativa (projeção no DRE do T20), a receita paga e a taxa (DRE/DFC do T20), a cobrança
pendente do hotel (Portal do Cliente, seção "Cobranças", já vista no T12).

## Gravação (modo fakebase)

**Já coberto:** tabelas `tenant_*` no schema; módulo `cobrancas`; clientes com documento válido; Financeiro do T13.

**Falta** (inventário 4.3), em ordem de prioridade:

1. Estado inicial sem linha em `tenant_payment_accounts` (hoje o seed a traz ativa); depois do cap. 2, a linha ativa com
   `default_fee_category` = "Tarifas e Taxas" e as chaves de cartão recorrente/Pix Automático **ligadas** (como em produção).
2. Handlers de edge: `tenant-asaas-provision` (activate/deactivate), `tenant-asaas-card-fees` (tabela de referência fictícia,
   `source: 'asaas'`, `syncedAt`), `tenant-asaas-create-charge` (insere `tenant_charges` PENDING com `public_short_code`,
   `pix_copy_paste` fictício e a conta a receber; devolve `{charge}`), `get-tenant-payment-checkout` (empresa + cobrança),
   `tenant-asaas-create-subscription` e `tenant-asaas-manage-subscription` (inserir/atualizar `tenant_subscriptions`).
3. Pagamento simulado: rota de dev que imita o webhook (status RECEIVED, `payment_date`, receita paga, despesa da taxa) ou
   semente `seeds-extra/t19/apos-cap08.json` aplicada no corte do cap. 8. O checkout aberto atualiza sozinho (consulta periódica).
4. Página deslogada (cap. 8): mesmo passo proposto no T12 (limpar sessão + `goto`), `127.0.0.1:8080/pagar/<código>`.
5. Ilustração do cap. 1 (cliente → link → conta Asaas → Financeiro), sem marca de banco; o Asaas aparece só pelo nome.
6. Estados `seeds-extra/t19/apos-capNN.json`. Desktop 1280×800. "Enviar por WhatsApp", "Abrir boleto" e "Abrir checkout"
   (nova aba) só com zoom.

## Pronúncias novas para o TTS

| Tela / legenda | Texto do TTS |
|---|---|
| Asaas | asas (já registrado) |
| Pix | pix |
| MRR | ême-érre-érre |
| API | a-pê-í |
| R$ 450,00 / R$ 380,00 | quatrocentos e cinquenta reais / trezentos e oitenta reais |
| 2 % / 1 % ao mês | dois por cento / um por cento ao mês |
| 3x | três vezes |

## Riscos e decisões para o Kaik

1. **Conexão:** mostrar a ativação (seed sem conta, chave fictícia borrada; proposta) ou começar já conectado e só mostrar
   as configurações (−1 min)?
2. **Pagamento simulado:** aceitar o corte no cap. 8 (o cliente "paga" fora da tela e a página muda para "Pagamento
   confirmado") como representação fiel do aviso do Asaas?
3. **Cartão recorrente e Pix Automático:** em produção as opções aparecem; o seed atual esconde. Mostrar na lista de "Forma
   de pagamento" (zoom) com as chaves ligadas, sem demonstrar o checkout (proposta), ou deixar de fora?
4. **Handoffs antes de gravar** (inventário 5): botão "Ir para Integrações" leva a página não encontrada (o roteiro entra
   pelo menu); "Recebimentos não contratado".
5. **Logo do Asaas** na tela do app (card da integração e rodapé do checkout): é do próprio app; manter na gravação?
6. **Duração (~14 min):** dá para juntar os caps. 4 e 5 (preferências + simulador) se ficar longo.
7. **Datas:** vencimentos (+3 dias, dia 10) e "Vencido" dependem do relógio do navegador (TRILHA 5).
