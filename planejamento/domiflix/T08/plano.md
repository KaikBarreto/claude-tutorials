# Plano · T8 — Estoque, compras e inventário

- **Título final da aula:** Estoque, compras e inventário
- **Áreas das vinhetas:** ESTOQUE · LOCAIS · HISTÓRICO · COMPRAS · NOTA FISCAL · INVENTÁRIO · POSIÇÃO · RELATÓRIO · RESUMO
- **Objetivo (uma frase):** cadastrar e movimentar materiais em mais de um local, repor o estoque (requisição, cotações, ordem de
  compra, compra direta e nota fiscal em XML) e conferir tudo no Kardex, no inventário, na posição de uma data e no relatório.
- **Pré-requisito:** T18 (Área do Técnico: Refrigeração e Climatização), que na ordem de exibição vem logo antes (T7 → T18 → T8).
  Aviso: "Antes: Área do Técnico: Refrigeração e Climatização".
- **Próximo:** T9 (Orçamentos, Precificação e Proposta). Aviso: "Próximo: Orçamentos, precificação e proposta".
- **Duração estimada:** ~24 min de fala natural (17 blocos), no alto da faixa de 10 a 25 min do `TRILHA.md` (decisão 1). Sem módulo
  pago: a tela Estoque vale para todo plano (o PDV só aparece como cartão desligado no Relatório). Sem preço de plano.
- Base: `T08/inventario.md` (código 1.38.6). Rótulos entre aspas = exatamente como na tela. Saldos, preços e datas abaixo são
  exemplos do mundo fictício, a fixar na semente.

## Capítulos propostos

| # | Vinheta (área / título) | O que a tela mostra | Avisos na tela (positivos) | Duração |
|---|---|---|---|---|
| 0 | — | Menu lateral com "Estoque" (dentro do grupo "Gestão") em destaque; abre a tela "Estoque" ("Controle de peças e materiais"). Fala: "Nesta aula você vai cuidar do que a Glacial Cold Brasil tem guardado: materiais, locais, compras e contagem." | "Antes: Área do Técnico: Refrigeração e Climatização" | 0:35 |
| 1 | ESTOQUE / A tela e as seis abas | Cabeçalho com "Importar XML (NF-e)" e "Configurações" (a câmera só passa). Abas: "Estoque Atual", "Histórico de Materiais (Kardex)", "Compras de Material", "Inventários", "Posição de Estoque", "Relatório". Em "Estoque Atual" (um só local, sem abas de local): cartões "Total de itens", "Valor investido (R$)", "Estoque baixo"; busca "Buscar por nome, código ou categoria..."; "Filtros" (caixa "Estoque abaixo do mínimo", lista "Grupo"); cartão "Itens do Estoque" com Nome, SKU, Categoria (a coluna mostra o grupo), Quantidade, Qtd. mínima, Custo Unit. "Exportar" abre o menu "PDF"/"Excel" e a janela "Selecionar materiais", **sem confirmar**. | "Seis abas, um só lugar para o estoque" | 1:20 |
| 2 | ESTOQUE / Cadastrar um material | "Cadastrar Material": "Nome do Item \*" Capacitor 40 µF; "Código/SKU" já vem **EST-010** (botão "Auto"; dica "Código sequencial sugerido automaticamente (você pode personalizar)."); "Grupo" Elétrica; "Fornecedor" Polar Distribuidora de Peças Ltda (lista do cadastro); "Quantidade" 6, "Unidade" Unidade (un); "Preço de Custo (R$)" 38,90 e "Preço de Venda (R$)" 70,00; "Locais deste material": caixa do Estoque Principal e "Mín." 4. A câmera passa por "Foto do item", "Código de barras" e "Vendável na loja" (PDV) sem preencher. "Salvar" → "Item cadastrado com sucesso!". | "O código do material sai sozinho; dá para personalizar" | 1:45 |
| 3 | ESTOQUE / Entrada, saída e estoque baixo | Menu da linha "Fita isolante" → "Registrar entrada": 10, "Observação" Compra no balcão, "Saldo após: 39" → "Confirmar" → "Entrada registrada". Menu da linha "Capacitor 40 µF" → "Registrar saída": 3, "Saldo após: 3" → "Saída registrada": a linha fica avermelhada (dica "Estoque abaixo do mínimo: 3 de 4") e "Estoque baixo" sobe para 3. "Filtros" → "Estoque abaixo do mínimo" lista os três. | "O alerta de estoque baixo olha o mínimo de cada local" | 1:15 |
| 4 | LOCAIS / Locais e grupos de material | "Configurações": aba "Grupos de material" (Gases, Cobre e tubos, Elétrica, Consumíveis, com bolinha de cor); aba "Locais de estoque": "Estoque Principal" com selo "Principal"; "Novo local de estoque" Van 01 → "Depósito criado com sucesso!". Ao fechar, surgem as abas de local (estrela no principal). Engrenagem de "Van 01" → "Configurar Van 01" → "Itens": "Adicionar por grupo" Gases → "Adicionar grupo", marca "Fita isolante" → "Salvar" → "Itens do local atualizados". | "Com mais de um local, cada um ganha a sua aba" | 1:30 |
| 5 | LOCAIS / Transferir para a van | Aba "Estoque Principal", menu da linha "Gás refrigerante R-410A" → "Transferir entre locais de estoque": "Local de origem" Estoque Principal ("Disponível: 8,5"), "Local de destino" Van 01, "Quantidade" 2, "Observações" Carga da van do Rafael → "Transferir" → "Transferência realizada com sucesso!". Aba "Van 01": R-410A com 2 kg. | "Transferir mantém o histórico: sai de um local e entra no outro" | 1:00 |
| 6 | LOCAIS / Quem enxerga cada local | Engrenagem de "Van 01" → aba "Acesso": chave "Restringir acesso a este local" ("Apenas os usuários marcados veem e movimentam este local."); Camila Duarte com "Sempre tem acesso"; marca Rafael Lima → "Salvar acesso" → "Acesso do local atualizado". | "Local restrito: só as pessoas marcadas, e a gestão, enxergam" | 1:00 |
| 7 | HISTÓRICO / Kardex | Aba "Histórico de Materiais (Kardex)": coluna "Materiais" com "Geral (Todos)" ("N movimentações no período"), busca "Buscar material..." e "Filtros" ("Período" este mês, "Tipo de movimento", "Local"). "Kardex geral": Data e Hora · Tipo · Material e origem (com quem lançou) · Local · Estoque inicial · Alteração · Estoque final; linhas de hoje: Entrada, Saída, Transferência ("Estoque Principal → Van 01") e as duas de Consumo "OS #16" (T7). Filtra "Consumo"; clica em "Gás refrigerante R-410A": "Histórico deste material". | "Todo movimento deixa rastro: quem, quando e de onde" | 1:30 |
| 8 | COMPRAS / Requisição de compra | Aba "Compras de Material", "Requisições de Compra": faixa vermelha "3 materiais abaixo do mínimo" → "Criar requisição" abre "Nova Requisição de Compra": "Título \*" Reposição de gás, cobre e capacitor; "Local de destino" Estoque Principal ("Os materiais recebidos entram neste local de estoque."); "Adicionar itens abaixo do mínimo" → "Itens abaixo do mínimo" (linhas "Deficit: N un") → "Adicionar à requisição"; preenche R-410A 10 kg, Tubo de cobre 3/8" 20 m, Capacitor 40 µF 6 un (trecho acelerado) → "Salvar" → "Requisição criada!". | "Faltou material? A requisição já lista o que está abaixo do mínimo" | 1:30 |
| 9 | COMPRAS / Cotações e fornecedor por material | Clica no cartão da requisição: "Materiais", "Cotações", "Ordens de compra". "Nova cotação": "Fornecedor \*" Ventura Gás e Tubos, valor unitário R-410A 94,00 e Tubo 3/8" 29,50 → "Salvar cotação"; Cobre Sul Suprimentos Ltda (Tubo 27,00; R-410A 98,00); Polar (Capacitor 36,00). Selos "Mais barata" e "N/N materiais com preço". Em "Materiais", "Fornecedor escolhido" por linha: R-410A → Ventura, Tubo → Cobre Sul, Capacitor → Polar (opções "Fornecedor (R$ preço)"). O botão "Fornecedores" só passa na tela. | "Escolha o melhor fornecedor de cada material" | 1:40 |
| 10 | COMPRAS / Ordem de compra e recebimento | "Gerar ordens de compra" → "3 ordens de compra geradas." (uma por fornecedor, "Rascunho"). Ventura: "Marcar como enviada" ("Ordem marcada como enviada.", selo "Enviada"); no menu aparece "Baixar PDF" (**sem clicar**); "Registrar recebimento" ("Qtd. pedida", "Qtd. recebida", "Qtd. pendente") → "Receber tudo" → "Confirmar recebimento" → "Recebimento registrado. 1 item atualizado." (selo "Recebida"). Cobre Sul: enviada, recebe 10 de 20 m → "Recebida parcial". Polar segue em "Rascunho". Volta ao "Estoque Atual": R-410A e Tubo 3/8" atualizados. | "O estoque só sobe quando o material chega" | 1:45 |
| 11 | COMPRAS / Compra direta | Como Camila (admin): "Registrar compra direta" → "Compra de material" ("Registre a entrada no estoque e a despesa financeira em uma única operação."): "Descrição" Reposição de dreno; "Fornecedor \*" Distribuidora Aurora de Peças Ltda; "Local de estoque \*" Estoque Principal; "Data da compra \*" hoje; "Adicionar material" Mangueira de dreno 30 m a 3,50 ("Total da compra" R$ 105,00); "Categoria financeira \*" CMV - Materiais (sugerida); "Conta financeira \*" Conta Principal; "Situação do pagamento" Pago, "Forma de pagamento \*" Pix, "Data do pagamento \*" → "Registrar compra" → "Compra registrada" ("O estoque e o financeiro foram atualizados."). Cartão com selo "Compra direta" e "Total: R$ 105,00". | "Compra direta: entra no estoque e vai para o Financeiro de uma vez" | 1:20 |
| 12 | NOTA FISCAL / Importar XML (NF-e) | Botão "Importar XML (NF-e)": "Selecione o arquivo .xml da nota fiscal eletrônica para dar entrada no estoque." → "Escolher arquivo XML" (passo `upload`). Revisão: cartão "Fornecedor" Gelo Norte Componentes Ltda com selo "Vinculado"; "Produtos da nota" ("2 novos • 3 no total"); cada produto com nome, "Qtd", "Unidade", "Custo un." e "Destino no estoque" (Capacitor 40 µF 440V já vem "Capacitor 40 µF (EST-010)"; Contator 25 A e Filtro secador em "Criar novo item"); rodapé "3 itens • R$ …" → "Confirmar entrada" → "NF-e importada" ("3 itens importados • 2 novos. Entrada registrada no estoque."). | "A nota fiscal dá entrada no estoque principal" | 1:45 |
| 13 | INVENTÁRIO / Contar e ajustar | Aba "Inventários" → "Novo inventário": etapas "Locais" (Estoque Principal) → "Escopo" ("Por grupo de material": Gases e Elétrica) → "Confirmar" ("Resumo do inventário", "Observações" Contagem do mês) → "Criar inventário" → "Inventário criado". Abre "Inventário #N": Material · Local · Esperado · Contado · Diferença; digita o "Contado" dos 4 itens (trecho acelerado; grava ao sair do campo); faixa "Divergências encontradas: 2 itens" com "Valor total das divergências", aba "Divergências (2)". "Finalizar inventário" → "Finalizar inventário?" ("Observações finais") → "Finalizar" → "Inventário finalizado" ("2 itens ajustados no estoque."). | "A contagem salva sozinha ao sair do campo" | 2:15 |
| 14 | POSIÇÃO / O saldo numa data | Aba "Posição de Estoque": data e hora "agora"; cartões "Valor em estoque (custo)" e "Projeção de venda"; tabela Local · SKU · Material · Un. · Saldo · Valor (custo) · Projeção venda e linha "Total". Escolhe no calendário um dia de ~30 dias atrás: saldos e valores se recalculam sozinhos (o botão "Atualizar" só recarrega). Busca "Buscar material ou SKU..." por R-410A. "Exportar" só aparece. | "Veja como estava o estoque em qualquer dia" | 1:00 |
| 15 | RELATÓRIO / Compras, média paga e evolução do preço | "Relatório de estoque por material", período "Todo o histórico"; cartões "Total comprado" (aberto: "Ticket médio por compra", "Materiais comprados"), "Total vendido" e "Lucro bruto" (selo PDV, "—"), "Projeção de lucro" (selo "estimativa"). Painel "Evolução do preço de compra": "Visão geral — Maiores altas e quedas", escolhe "Gás refrigerante R-410A": "Último preço", "Média do período", "Menor preço", "Maior preço", "Variação", abas "Preço médio"/"Volume comprado". Lista "Por material" (Última compra · Compras · Qtd. comprada · Valor comprado · Média paga · Saldo atual); clica na linha do R-410A: "Histórico de compras". | "Média paga: o que a empresa pagou, ponderado pela quantidade" | 2:00 |
| 16 | RESUMO / Recapitulando | Montagem: cadastro, abas de local, transferência, Kardex, requisição, ordem de compra, compra direta, nota fiscal, inventário, posição, relatório. | "Próximo: Orçamentos, precificação e proposta" | 0:50 |

Mapa com a trilha (11 capítulos de 1.22.5): cap. 1 → bloco 1; cap. 2 → 2 e 3; cap. 3 → 4 e 5; cap. 4 → 6; cap. 5 → 7; cap. 6 → 8 e 11;
cap. 7 → 9 e 10; cap. 8 → 12; cap. 9 → 13; cap. 10 → 14; cap. 11 → 15; o ⚠️ "concluir a OS não baixa estoque" vira fala do bloco 7.

Transições faladas: 1→2 "Vamos cadastrar um material do zero"; 3→4 "Quando a empresa tem uma van ou mais de um depósito, entram os locais";
6→7 "E tudo isso fica registrado no Kardex"; 7→8 "Agora, o que fazer quando o material está acabando: as compras"; 9→10 "Com o
fornecedor escolhido, é hora de gerar as ordens de compra"; 10→11 "Tem compra que não precisa de cotação: a compra direta"; 11→12 "E quando
o fornecedor manda a nota fiscal em XML?"; 12→13 "Agora, a conferência: o inventário"; 13→14 "Terminada a contagem, dá para voltar no tempo
com a Posição de Estoque"; 14→15 "E para saber quanto a empresa paga pelos materiais, o Relatório"; 15→16 "E é isso". Recap → próximo: "Com o
estoque em ordem, o próximo passo é montar orçamentos e propostas para os clientes."

**Falas dos cuidados ⚠️** (regra de 30/10 20:56: caminho certo primeiro, consequência numa frase, sem encenar falha):

| Cuidado | Fala sugerida | Na tela |
|---|---|---|
| Mínimo por local | "Defina o mínimo de cada local no cadastro; sem mínimo, a linha não avisa e o cartão 'Estoque baixo' não conta." | Campo "Mín." / linha avermelhada |
| Saída | "Antes de confirmar, olhe o 'Saldo após': a saída maior do que o saldo não é aceita." | Linha "Saldo após" |
| Tirar material de um local | "Para tirar um material de um local, transfira ou dê baixa do saldo antes; com saldo, a Dominex não deixa e oferece 'Transferir saldo'." | "Locais deste material" |
| Excluir material | "Para encerrar um material, zere o saldo e tire dos locais; ao excluir, o histórico dele também é apagado." | Menu da linha (câmera passa, sem clicar) |
| Acesso por local | "Marque as pessoas que usam o local e salve em 'Salvar acesso'; a gestão sempre vê. Sem ninguém marcado, o local continua aberto a todos." | Lista com "Sempre tem acesso" |
| Cotação e estoque | "Escolher o fornecedor e aceitar a cotação não mexe no estoque; ele sobe quando você registra o recebimento da ordem enviada." | Ordem "Enviada" |
| Recebimento parcial | "Informe só o que chegou agora; o resto continua pendente e a ordem fica 'Recebida parcial'." | "Qtd. pendente" |
| Compra direta | "A compra direta aparece para quem administra estoque e financeiro, porque lança as duas coisas juntas." | Botão "Registrar compra direta" |
| Nota fiscal | "A nota dá entrada no estoque principal e cria o fornecedor se for novo; ela não monta a compra nem lança despesa. Para a van, transfira depois." | "Confirmar entrada" |
| Nota repetida | "Se a nota já foi importada, a Dominex avisa antes de repetir a entrada." | Só falado (decisão 9) |
| Inventário | "Confira a aba Divergências antes de finalizar: ao finalizar, o estoque é ajustado e não volta atrás. Evite movimentar enquanto conta." | "Finalizar inventário?" |
| Valor da posição | "O valor usa o custo cadastrado hoje, não o custo do dia escolhido." | "Valor em estoque (custo)" |
| Média paga | "A média paga considera as compras recebidas por ordem de compra e as compras diretas; entradas rápidas e notas importadas não entram. É a média ponderada do que foi pago." | Coluna "Média paga" |
| Projeção | "A projeção de lucro é uma estimativa com o preço de venda cadastrado; venda e lucro reais dependem do PDV." | Selo "estimativa" |
| Consumo na OS | "Concluir a OS não baixa o estoque sozinho: com 'Consumo de estoque na OS' ligado e os materiais anotados, a baixa acontece ao finalizar." | Linhas "Consumo" "OS #16" |

## Mundo fictício (continuidade)

- **Começa em:** fim do T2 na produção (T7 → T18 → T2 → T8; o T18 não altera dados): Glacial Cold Brasil, Camila Duarte (admin), técnicos
  (inclui Tatiane Ribeiro, do T2), OS #16 concluída com consumo de 2 un de Limpa-evaporador e 1 rolo de Fita isolante (T7). Fornecedores
  do cadastro: Polar Distribuidora de Peças Ltda, Gelo Norte Componentes Ltda (CNPJ 91.345.602/0001-36), Cobre Sul Suprimentos Ltda,
  Distribuidora Aurora de Peças Ltda e Ventura Gás e Tubos (T3).
- **Estoque de partida (semente do T8; amplia a do T7):** só o local "Estoque Principal" (principal); grupos Gases, Cobre e tubos,
  Elétrica, Consumíveis; 9 materiais, SKU EST-001 a EST-009, com custo e preço de venda: Gás refrigerante R-410A (kg) 8,5, mín. 10 ·
  Gás refrigerante R-32 (kg) 6, mín. 4 · Tubo de cobre 1/4" (m) 45, mín. 30 · Tubo de cobre 3/8" (m) 12, mín. 20 · Mangueira de dreno (m)
  60, mín. 25 · Capacitor 35 µF (un) 9, mín. 4 · Limpa-evaporador em spray (un) 10, mín. 6 · Fita isolante (rolo) 29, mín. 12 · Suporte
  para condensadora (par) 8, mín. 4. R-410A, Limpa-evaporador e Fita isolante vêm da proposta do T7 (já com a baixa da #16).
- **Histórico semeado:** "Cadastro inicial" de ~45 dias antes (Posição); duas compras recebidas antigas de R-410A (60 e 25 dias antes,
  R$ 86,00 e R$ 90,00 o kg) para a evolução do preço; movimentos dentro do mês da data do mundo (Kardex abre em "este mês").
- **Financeiro (bastidor):** conta "Conta Principal" (ativa, não cartão; a mesma do T11/T13) e categoria "CMV - Materiais" (despesa,
  grupo CMV). A compra direta de R$ 105,00 passa a fazer parte do começo do T13 (decisão 4).
- **Esta aula cria:** Capacitor 40 µF (EST-010); local Van 01 com acesso só do Rafael Lima; transferência de 2 kg de R-410A; requisição
  "Reposição de gás, cobre e capacitor" com 3 cotações e 3 ordens (Ventura recebida, Cobre Sul recebida em parte, Polar em rascunho);
  compra direta da Aurora; nota fiscal da Gelo Norte (Contator 25 A e Filtro secador novos); inventário de Gases e Elétrica finalizado.
  Estado final em `seeds-extra/t8/apos-capNN.json`; atualizar `MUNDO_FICTICIO.md`.
- Sem preços de plano. Valores em R$ de peças e fornecedores do mundo fictício podem aparecer.

## Gravação

- **Já coberto (T3/T7):** login e menu; `click`/`type`/`select`/`hover`/`drag`/`scroll`; janelas Radix; `upload` por seletor de arquivo
  (anexo do equipamento no T3); gravação genérica em todas as tabelas de estoque (estão em `schema.json`). O T7 já prevê as sementes
  de `stocks`/`inventory` e os handlers `register_inventory_movement` e `commit_os_material_consumption`: reaproveitar.
- **Falta (ordem de importância; detalhe no inventário 4.3):**
  1. **Handler de `get_accessible_inventory_ids`:** sem ele a tabela "Estoque Atual" aparece vazia, mesmo com sementes (bloqueio nº 1).
  2. **Sementes:** `stocks`, `material_groups`, `inventory`, `inventory_stock_levels` (com mínimo e presença; `inventory.quantity` igual à
     soma), `inventory_movements` coerentes (saldo antes + alteração = depois) em **duas épocas**, e `compras`, `compra_ordens`,
     `compra_ordem_itens` recebidos com datas diferentes (evolução do preço exige 2 datas do mesmo material).
  3. **Handlers que calculam:** `register_inventory_movement`, `transfer_stock_between` (duas pernas), `set_inventory_presence`,
     `add_group_to_stock`, `set_stock_materials`, `set_default_stock`, `get_stock_access`/`set_stock_access`, `receber_ordem_compra`,
     `finalize_inventory_count`, `registrar_compra_material_direta`, `get_stock_balance_at_date`, `get_material_purchase_report`.
  4. **Views e gatilhos:** `inventory_low_stock` e `inventory_count_divergences` em `handlers/views`; numeração de `compras`,
     `compra_ordens` (com autor e data de envio) e `inventory_counts`; coluna `diff` de `inventory_count_items`.
  5. **Financeiro de bastidor** (`financial_accounts`, `financial_categories`) e o handler da compra direta criando a despesa.
  6. **XML fictício** (CNPJ da Gelo Norte igual ao do cadastro, 3 produtos, chave de 44 dígitos fora de `nfe_imports`, nome do capacitor
     contendo "Capacitor 40 µF") e passo `upload` no botão "Escolher arquivo XML" (`rec/recorder/runner.mjs:535-555`). Testar o leitor e o
     casamento do nome antes do roteiro final.
  7. **Relógio:** navegador congelado na mesma data do falso (TRILHA, item 5): o Kardex abre em "este mês", a Posição em "agora".
  8. **Sem download** (TRILHA, item 6): nenhum clique em "Exportar PDF", "Exportar Excel" ou "Baixar PDF"; parar no menu ou na seleção.
  9. **Largura:** a tabela do Relatório tem largura mínima de 1320 px (`components/inventory/MaterialPurchaseReportTab.tsx:428`); no robô
     (1280 px) rolar na horizontal dentro do cartão ou recolher o menu lateral (a confirmar rodando).
  10. **Navegador limpo** no Relatório (ele lembra visualização, "ocultar sem movimento", itens por página e ordenação). Foto de material
      precisa do armazenamento `inventory-photos`, que o falso não tem (decisão 7).
- **Passos de teclado:** vírgula nos valores ("38,90", "8,5"); a contagem do inventário grava ao sair do campo, então terminar cada item
  com Tab ou clique fora.

## Pronúncias (testar num trecho curto e registrar em `config_narracao.json` e `PERFIL.md`)

Kardex ("cárdex"), NF-e ("ene-éfe-é"), XML ("xis-eme-éle"), SKU (preferir "código"), O.C. (falar "ordem de compra"), R-410A ("érre
quatrocentos e dez a"), R-32, µF ("microfarad"), kg ("quilo"), CNPJ, Van 01 ("van zero um"), Pix ("piks"), PDV ("pê-dê-vê"), EST-010
(falar "código dez"), "Ltda" (omitir na fala), Ventura Gás e Tubos, Cobre Sul, Gelo Norte, "deficit" ("déficit").

## Riscos e decisões para o Kaik

1. **Duração:** ~24 min (a trilha previa 43). Se parecer longa, dividir em duas partes: "Estoque e locais" (blocos 0 a 7, ~10 min) e
   "Compras, inventário e relatórios" (8 a 16, ~14 min), ou cortar o bloco 11 (compra direta) e a segunda metade do 15.
2. **A trilha promete o que o código não faz:** (a) "Categoria" no cadastro: hoje só **Grupo**; (b) "cotação vencedora": hoje o fornecedor
   é escolhido **por material** e sai **uma ordem por fornecedor** (`hooks/useCompraOrdens.ts:164-167,180-183`), e aceitar a cotação não
   mexe no estoque (`hooks/useCompraCotacoes.ts:206,250`); (c) "a compra montada sozinha" pela NF-e: só **dá entrada**. O roteiro segue o
   código. Confirmar que o vídeo não repete o título do capítulo 8 do Guia Técnico.
3. **Materiais combinados com o T7:** adotar Gás refrigerante R-410A (8,5 kg), Limpa-evaporador em spray e Fita isolante com os saldos
   da proposta do T7; se o roteiro do T7 mudar nomes ou saldos, atualizar o bloco 3, 5 e 10 daqui.
4. **Compra direta (bloco 11):** só aparece para admin/gestor ou quem tem as chaves de estoque e financeiro; gravar como Camila. Pede
   semente financeira e a despesa de R$ 105,00 entra no estado inicial do T13 (hoje só "Conta Principal" com R$ 18.500,00). Alternativa:
   lançar como "Pendente" para não mexer no saldo. Decidir junto com o T11/T13.
5. **Ações sem volta:** a aula finaliza **um** inventário (no mundo fictício) e fala do cuidado. Nunca clicar em "Excluir" material (apaga
   o Kardex dele), "Cancelar inventário" (não pede confirmação) nem "Excluir ordem". Concordar com a regra.
6. **Downloads:** Exportar (PDF/Excel) e "Baixar PDF" da ordem aparecem só até o menu. Confirmar que o vídeo não mostra arquivo baixado.
7. **Foto do material:** recomendo **sem fotos** (a lista mostra o ícone). Com fotos, o falso precisa do bucket `inventory-photos`.
8. **Subtítulo "Operacional"** nas abas de local (aparece porque o PDV está ligado): ignorar; "Loja × Operacional" é assunto do PDV.
9. **"Nota já importada":** só falar numa frase; mostrar exigiria importar a mesma nota duas vezes (parece encenar falha).
10. **Achados para o time do app (não corrigidos aqui):** [handoff] "Gerenciar Estoque" não trava botão da tela (P2); salvar material sem
    nome dá erro técnico (P5); nota da cotação aceita fala em "Registrar entrada", texto antigo (P6); contagem não inclui material que
    nunca teve saldo no local (P9); "Cancelar inventário" sem confirmação (P10); servidor aceita receber O.C. em rascunho (P12);
    textos e estado sem uso (P13); gravação de material aberta a qualquer usuário da empresa (P17). **Sem achado de segurança que cruze
    empresas.**
11. **Conferir rodando antes do roteiro final** (inventário, seção 7): janela do XML no desktop, hora do seletor de data da Posição,
    rolagem da lista do inventário, e ler o `desconhecidos.log` depois de montar as sementes.
