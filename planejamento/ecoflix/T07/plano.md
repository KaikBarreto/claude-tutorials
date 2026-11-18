# Plano · T7 Comprar e vender sucata

- **Título:** Comprar e vender sucata (o da fonte).
- **Antes:** T6 · Caixa: abrir, fechar e o cofre. **Próximo:** T8 · Ticket de Pesagem.
- **Áreas das vinhetas:** CAIXA · FORNECEDOR · PREÇO · BALANÇA · PESAGEM · VALOR · PAGAMENTO · COMPROVANTE · VENDA ·
  SEM INTERNET · RESUMO; no 1.60.10 entram PEDIDOS e RASCUNHO.
- **Objetivo:** fechar uma compra com o peso vindo da balança, tara, impureza e dupla pesagem, pagar em dinheiro, Pix e fiado
  parcelado, imprimir o cupom, vender com lucro estimado e cupom sem valor, cobrir o estoque que falta e comprar sem internet.
- **Duração (1.60.10, 18/11):** fala 3.541 palavras e 18.916 caracteres (~22,7 min) + 19 vinhetas e as ações sem fala
  (preenchimento acelerado): ~26 min. Uma aula só (decisão do Kaik), acima do alvo de 22 min da fonte. `python3 -I narracao/tts_textos.py` mostra a conta por capítulo.
- Base: `inventario.md` (código 1.59.154) + `cobertura_160.md` e a seção "1.60.10" do inventário (app gravado: **1.60.10**). Logado como **Rafael Nogueira** (MASTER, vê lucro), desktop 1280×800, tema claro.
  `FAKE_NOW=2026-11-10T08:35:00-03:00` (junção: depois do #85 da T6, aberto às 08:31, e antes do #86, às 08:4x; a pesagem
  da T8 vem às 08:40).
- 🔒: só a leitura da balança (módulo `balanca_integration`) e as outras unidades na falta de estoque (filial, módulo gerencial);
  a fala diz "depende do plano contratado", sem preço.

## Capítulos (os da fonte, na ordem)

| # | Vinheta | O que a tela mostra | ⚠️ / 🚫 na fala | Fonte |
|---|---|---|---|---|
| 0 | (abertura) | Ilustração do dia no pátio; cartão "Antes: Caixa: abrir, fechar e o cofre" | | 0:30 |
| 1 | CAIXA · Onde ficam a compra e a venda | "Financeiro" → "Caixa" → "Nova Compra"; "Voltar para o caixa"; Shift+V; Ctrl+K "Ações Rápidas"; tour da tela | | 1:00 |
| 2 | FORNECEDOR · Escolher o fornecedor | "Selecionar Fornecedor": "Não informado"; indicador âmbar do Valdir ("Cadastro incompleto"); busca sem resultado | Não informado sem saldo e fora do histórico; indicador não trava; "Não possui telefone" | 1:30 |
| 3 | FORNECEDOR · Cadastrar o fornecedor na hora | "+" → "Novo Fornecedor": nome, apelido, telefone, Chave PIX → "Fornecedor cadastrado com sucesso!" | | 1:30 |
| 4 | PREÇO · Qual preço vale | "Tabela de Preços" (estrela, "Tabela Depósitos"); ilustração da hierarquia | Hierarquia e aviso na tela | 1:30 |
| 5 | BALANÇA · O peso da balança | Cobre misto pela balança ("AO VIVO", visor); cena de Windows do EcoTray; latinha com "Tara/Imp." | 🔒 balança | 2:00 |
| 6 | PESAGEM · Tara, impureza e dupla pesagem | Ilustração; "Pesagem avançada" do ferro: 1ª e 2ª pesagem, impureza 3 %, "Completo", "Confirmar" | Estoque entra pelo líquido | 2:30 |
| 7 | PESAGEM · Mesclar pesagens | 2ª latinha; "Mesclar 2 pesagens deste material" → "Mesclar Todas"; "Desmesclar pesagens" | | 1:00 |
| 8 | VALOR · Desconto e conferência | "Adicionar tara / pesagem avançada" → "Valor final" 225,00 → desconto; "Total da Compra"; lápis | Campo de valor apaga o ponto | 1:00 |
| 9 | PEDIDOS · Dois pedidos ao mesmo tempo (novo) | Barra de pedidos ("Número", "Valor", "FORNECEDOR"); "+" abre o #1760; "Não informado" + cobre 10 kg (legenda "Principal"); troca para o Depósito Irmãos Siqueira: "Trocar fornecedor?" → "Atualizar 1 item" (37,44, "Tabela Depósitos"); volta ao pedido do Zé pela barra | "Só nos próximos" × "Atualizar" | novo |
| 10 | RASCUNHO · Rascunho: sair, descartar e recuperar (novo) | Ilustração; Caixa: "Pedidos Não Finalizados"; lixeira da lista → "Descartar este pedido?"; "Rascunhos apagados" → "Recuperar"; descarta de novo e "Excluir definitivamente"; mouse no "Cancelar" | Caixa não fecha com pedido não finalizado; "Cancelar" não tem volta; colega no mesmo pedido (só fala) | novo |
| 11 | PAGAMENTO · Finalizar o pedido | "Finalizar Pedido": ilustração das 3 formas; Pix (chave), Saldo ("Você deverá a ele"), Dinheiro; "Arredondar para baixo"; 920,00 → "Excesso: R$ 6,80" → "Deixar no saldo de …" → "Desfazer"; "Compra registrada!"; "Imprimir direto" | | 2:00 |
| 12 | PAGAMENTO · Abater o vale na compra (novo) | Valdir Pereira (saldo −300,00), Ferro misto 200 kg = R$ 150,00; "Saldo do Fornecedor": "Saldo atual:" e "Saldo após o pedido:" "(Ele te deverá)"; fecha sem confirmar; "Cancelar" → "Cancelar pedido?" → "Sim, cancelar" | Mostra e cancela: o saldo do Valdir não muda (junção) | novo |
| 13 | PAGAMENTO · Até três formas de pagamento | Compra da Auto Peças Vale Forte ("Preço especial aplicado"); "Múltiplas formas de pagamento": 200 + 2.000 + Pix completa 736,40 | Faltam/Excesso travam | 1:30 |
| 14 | PAGAMENTO · Fiado com parcelas | "Vencimento (opcional)"; "Configurar faturamento": 2 parcelas (25/11 e 10/12); ilustração; "Aplicar faturamento"; confirmar | Saldo mudou → refazer parcelas | 1:30 |
| 15 | COMPROVANTE · O cupom e o cupom sem valor | "Imprimir Comprovante" → "Imprimir direto"; ilustração do cupom; "Opções avançadas" → "Comprovante sem valores" + balão | Vale só para o pedido | 1:30 |
| 16 | VENDA · A tela de venda | Shift+V; Fundição Bandeira do Vale; latão; coluna "Lucro", "Lucro estimado"; ilustração; "Estoque Disponível"; liga "Comprovante sem valores" | Estoque Disponível já desconta a venda | 1:30 |
| 17 | VENDA · Estoque insuficiente | Cobre mel 60 kg × 42 em estoque → "Estoque insuficiente" → origem "Cobre misto" 18 → "Transferir e Adicionar"; Pix; PDF sem valores | 🔒 outras unidades e, com elas, só com internet; agendada e gravada junto; "Inserir mesmo assim" | 1:00 |
| 18 | SEM INTERNET · Sem internet | Faixa "Sem conexão…"; compra da Dona Cida → "Compra salva localmente…"; "Pendências de Sincronização"; volta: "Operações sincronizadas com sucesso!"; ilustração da fila | Erro não reenvia sozinho; "Tentar novamente" | 1:00 |
| 19 | RESUMO · Recapitulando | Montagem; "Próximo: Ticket de Pesagem" | | 0:50 |

Transições faladas: 1→2 "Primeiro, quem está vendendo pra gente"; 2→3 "Hoje chegou um carroceiro novo"; 3→4 "Agora o preço";
4→5 "Agora o primeiro material"; 5→6 "Antes de seguir, três palavras do pátio"; 6→7 "O Zé trouxe mais dois sacos";
7→8 "Agora a conferência"; 8→9 "Antes de pagar o Zé, repara nesta barra escura"; 9→10 "Esses pedidos abertos são rascunhos";
10→11 "Conferido, é hora de pagar"; 11→12 "Vale a pena ver mais um caso"; 12→13 "Agora uma compra maior"; 13→14 "Os dois mil do
saldo"; 14→15 "Depois de confirmar, a tela pergunta do comprovante"; 15→16 "Agora o outro lado: vender"; 16→17 "A Fundição também
quer cobre mel"; 17→18 "E se a internet cair no meio do dia?".

## Estado de partida (fim do T6) e entre capítulos
- Início: Dashboard; caixa do Rafael aberto em 10/11 (do T6); nenhum rascunho de pedido; EcoTray falso conectado (balança e
  impressora); nada de pendência offline.
- Cada capítulo começa de um navegador novo com a semente do fim do anterior; o `setup` do robô refaz fora do vídeo o que não
  é semente (janela aberta, rascunho do pedido, pagamento preenchido):
  cap02 Nova Compra vazia · cap03 "Selecionar Fornecedor" com "Moreira" na busca · cap04 e cap05 compra com o Zé, sem itens ·
  cap06 + cobre e latinha · cap07 + ferro · cap08 + latinha mesclada · cap09 e cap11 ferro com desconto (R$ 913,20) · cap10 o
  pedido do Zé e o do Depósito (cobre 10 kg a 37,44) abertos · cap12 e cap13 compra do Zé finalizada, Nova Compra vazia ·
  cap14 Vale Forte com 2 itens e o "Finalizar Pedido" com as três formas · cap15 a janela "Imprimir Comprovante" da Vale Forte ·
  cap16 Nova Compra vazia · cap17 venda com o latão e "Comprovante sem valores" ligado · cap18 Nova Venda vazia, venda
  finalizada. Os capítulos 09, 10 e 12 não deixam nada no banco (rascunho excluído de vez, pedido do Valdir cancelado).

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (alinhar com T3, T4, T5 e T6 na consolidação):
- **Caixa** do Rafael: o **#85**, aberto às 08:31 com **R$ 1.500,00** (o da T6; dá para o dinheiro da aula: R$ 913,20 + R$ 200,00 +
  R$ 90,52; no 1.60.10 nada a mais sai do caixa). Na semente da T7 só o #85 está aberto (o #86 do Marcos ainda não abriu, para não aparecer "Em qual caixa
  registrar?"). A fala não diz o valor do caixa. Junção: `MUNDO_LINHA_DO_TEMPO.md`, "Caixas".
- **Preferências:** Múltiplas Tabelas de Preço ligada (T3); impureza desconta do valor (padrão); itens editáveis (padrão);
  impressão automática **desligada** (para a janela "Imprimir Comprovante" aparecer); impressão direta pelo EcoTray **ligada**;
  balança ativada, **leitura contínua ligada**, 3 casas (T5); balança exclusiva desligada; "só peso líquido" desligado; atalhos
  ligados.
- **EcoTray falso:** uma balança "Balança" (nome padrão do EcoTray, `✓ padrão`), conectada; impressora térmica conectada.
  Pesos estáveis por momento: 12,4 (cobre) · 21,6 (latinha) · 0,0 → 412,0 → 96,0 (ferro, 1ª e 2ª) · 18,4 (latinha) · 186,0
  (bateria) · 64,0 (cobre) · no 1.60.10 também 10,0 (cobre do Depósito, cap09) e 200,0 (ferro do Valdir, cap12) · 152,0 (latão) · 0,0 (latão de novo) · 60,0 (cobre mel) · 14,6 (latinha da Dona Cida); 0,0 entre um
  e outro.
- **Tabelas de preço:** "Principal" (estrela, com o preço dos 15 materiais) e "Tabela Depósitos" (T3, +4 %: cobre misto 37,44).
  O Zé fica na Principal. **1.60.10:** o Depósito Irmãos Siqueira ligado à "Tabela Depósitos" (`t07/inicio`, só nesta aula) e o
  Rafael sem tabela fixada (`profiles.preferred_price_table_id` nulo).
- **Estoque no início** (kg): Metal amarelo (latão) **214**; Cobre mel **42**; Cobre misto 148 (o estoque de 10/11 08:30 da junção,
  que é o mesmo do T10 e do T21); demais como lá.
- **Parceiros:** Valdir Pereira **sem CPF e sem endereço**, com "Não possui telefone" marcado (indicador "2": "CPF/CNPJ não
  informado", "Endereço não informado"); Aparecida Ramos com apelido "Dona Cida"; **Auto Peças Vale Forte** com **preço especial
  da Bateria automotiva R$ 3,40/kg** e saldo R$ 0,00; Fundição Bandeira do Vale com saldo qualquer (paga no Pix).
- Conta bancária **principal** do mundo (Pix da compra e da venda).
- **Criado na tela:**
  - Fornecedor **José Carlos Moreira**, apelido **Zé Moreira**, telefone **(12) 90000-4471**, Chave PIX **(12) 90000-4471**,
    tabela padrão, sem CPF e sem endereço (carroceiro novo).
  - **Compra 1 (Zé, dinheiro R$ 913,20):** Cobre misto 12,4 kg × 36,00 = R$ 446,40 · Alumínio latinha 21,6 kg − tara 0,6 = 21 kg
    × 6,20 = R$ 130,20 · Ferro misto: 1ª 412 kg, 2ª 96 kg, bruto 316 kg, impureza 3 % = 9,48 kg, líquido 306,52 kg × 0,75 =
    R$ 229,89, "Completo", valor final **R$ 225,00** (desconto R$ 4,89) · Alumínio latinha 18,4 kg − tara 0,4 = 18 kg × 6,20 =
    R$ 111,60 · mesclagem da latinha: 40 kg (tara 1), líquido 39 kg, R$ 241,80, média R$ 6,20. Total **R$ 913,20**; estoque entra
    pelo líquido (cobre 12,4; latinha 39; ferro 306,52).
  - **Compra 2 (Auto Peças Vale Forte, R$ 2.936,40):** Bateria automotiva 186 kg × 3,40 = R$ 632,40 · Cobre misto 64 kg × 36,00
    = R$ 2.304,00. Pagamento: Dinheiro R$ 200,00 · Pix R$ 736,40 (conta principal) · Saldo do Fornecedor R$ 2.000,00 em 2 parcelas
    de R$ 1.000,00 (**25/11/2026** e **10/12/2026**), saldo da oficina depois: R$ 2.000,00 a pagar.
  - **Venda (Fundição Bandeira do Vale, Pix R$ 7.722,80, "Comprovante sem valores"):** Metal amarelo (latão) 152 kg × 31,90 =
    R$ 4.848,80 (lucro R$ 668,80) · Cobre mel 60 kg × 47,90 = R$ 2.874,00 (lucro R$ 324,00) com transferência de **18 kg de Cobre
    misto → Cobre mel** na finalização. Lucro estimado **R$ 992,80**. Quem busca: o motorista da Fundição (só na fala; junção: o FKD2E41 e o Edson estão na viagem da T17).
  - **Compra 3 sem internet (Dona Cida, dinheiro):** Alumínio latinha 14,6 kg × 6,20 = R$ 90,52; fila local e sincronização.
  - **1.60.10, sem deixar rastro:** rascunho #1760 (Não informado → Depósito Irmãos Siqueira, Cobre misto 10 kg × 36,00 = R$ 360,00
    → 37,44 = R$ 374,40), descartado, recuperado e excluído de vez; no pagamento do Zé, 920,00 em dinheiro → "Excesso: R$ 6,80" e
    desfeito; compra do Valdir (Ferro misto 200 kg × 0,75 = R$ 150,00) aberta até o "Saldo do Fornecedor" e cancelada; na venda, o
    Valor/Kg do latão vai a 32,00 e volta a 31,90.
- **Fica para as próximas:** saldo a pagar de R$ 2.000,00 à Vale Forte em 2 parcelas (T13); os pedidos do dia no histórico do
  caixa (T9); estoque final: latão 62 kg, cobre mel 0 kg, cobre misto (inicial + 12,4 + 64 − 18).

## Gravação
- **Rotas:** `/dashboard` → `/caixa` → `/compra` → `/caixa` → `/venda` → `/compra` (Ctrl+K) … `/venda` (Shift+V) → `/compra`
  (Shift+C) → `/caixa`. Atalhos só com o foco fora de campo (`hooks/useKeyboardShortcuts.tsx:174-181`): o robô clica numa área
  vazia antes.
- **Backend falso:** `INSERT suppliers`; preços especiais do parceiro; tabelas e itens; `log_pesagens`; RPCs
  `create_purchase_atomic` (com `p_installments`, `p_payment_condition_id`, `p_hide_financial_details`),
  `create_sale_with_stock_transfers_atomic` (transferência local de material), `get_next_order_number`,
  `preview_next_order_ref`, `preview_next_order_seq`; rascunhos do pedido (`useOrderCache`) para as sementes entre capítulos.
- **EcoTray falso:** WebSocket `ws://127.0.0.1:8053` com a sequência de pesos acima (estável, peso fresco para o "AO VIVO") e
  impressão direta respondendo ok ("Comprovante enviado para impressora").
- **Sem internet (cap18; 1.60.10):** o app testa `/auth/v1/health` (2 falhas seguidas para cair, 2 acertos para voltar): o robô derruba esse endereço na página, além do `navigator.onLine`. Antes: navegador offline (eventos `offline`/`online`, `navigator.onLine`) e backend falso fora do ar, com o
  EcoTray falso respondendo. [TESTAR: o modo offline do Playwright pode derrubar o WebSocket local; se derrubar, simular a queda
  só no backend falso e no `navigator.onLine`.] Ao voltar: sincronização sozinha.
- **Janela do PDF (cap17):** "Visualizar PDF" abre o comprovante numa janela nova; o robô a captura e volta. [TESTAR]
- **Cena de Windows (cap05; balança "Balança do pátio"):** área de trabalho genérica com o navegador da aula e a janela do EcoTray do código
  (`ecotray/dashboard.py`): "EcoTray", "Ponte Desktop — Balança & Impressora", abas "Integrações"/"Logs", "Conectado e operando",
  "ws://127.0.0.1:8053", seção "Balanças" com "● Balança", "12,4 kg", "conectada", "✓ padrão". Uns 6 s; o peso do EcoTray e o do
  campo batem.
- **Ilustrações** (desenho por código no estilo da marca, rótulos reais, nenhuma tela inventada): cap00 o dia no pátio · cap02
  pedido com fornecedor × "Não informado" · cap04 a hierarquia do preço · cap06 tara, impureza e líquido + dupla pesagem da carroça ·
  cap05 (nova) o botão da balança em três cores · cap10 (nova) o rascunho salvo sozinho · cap11 as três formas e quem deve a quem ·
  cap14 a linha do tempo das parcelas · cap15 o cupom térmico saindo (desenho do comprovante real da Compra 2) · cap16 o lucro por
  quilo do latão · cap17 18 kg de cobre misto virando cobre mel · cap18 a fila sem internet (com o cartão em "Erro" e o "Tentar
  novamente"). As duas novas só estão descritas em `cenas/ilustracoes.json` ("v3": "pendente").
- Celular, página pública ou outro usuário: nenhum.
- Zooms longos (frase inteira): peso e "AO VIVO", "Valor Total do Item", "Peso Bruto (Kg)", "Impureza"/"Líquido (Kg)", "Desconto
  (R$)"/"Valor final", "Total da Compra", chave PIX, "Saldo após o pedido", os três valores do pagamento, as parcelas, "Lucro
  estimado", "Estoque Disponível", "Faltam 18 Kg de Cobre mel.", a faixa sem conexão, o aviso "Compra salva localmente". Trecho de
  formulário sem fala (itens da Vale Forte): acelerado na edição.

## Riscos e decisões para o Kaik
1. **Duas compras para a parte do pagamento:** a do Zé (carroceiro novo) mostra as formas e paga em dinheiro; a da Vale Forte faz as
   três formas e o fiado parcelado. Fiado parcelado de carroceiro não seria verossímil.
2. **Cupom sem valor:** vale só para o pedido em que é ligado (código), então o cap15 mostra onde fica e o uso de verdade é na venda
   (cap16 liga, cap17 mostra o PDF). A Central de Ajuda diz que ele "fica gravado de um pedido pro outro": está errada (H3).
3. **Uma balança só** ("Balança", nome padrão do EcoTray) para tudo, com dupla pesagem de carroça (cabe numa balança de piso). Se o
   T5 configurar duas (piso e rodoviária), o visor vira dois e a fala muda pouco.
4. **"Tabela Depósitos" e o preço especial da Vale Forte** dependem do T3/T4: se não existirem, a semente cria.
5. Pronúncias novas a testar (no nó de conferência, antes da voz): "xíft-cê"/"xíft-vê" (Shift+C/Shift+V), "tara-ímp"
   (Tara/Imp.) e "ao vivo" (o selo "AO VIVO", em maiúsculas na tela). Se o hífen não bastar, IPA entre barras (PERFIL).
6. Handoffs: H1 coluna "Peso Líquido" mostrando o bruto; H2 tooltip com ponto; H3 Central de Ajuda (inventário).
