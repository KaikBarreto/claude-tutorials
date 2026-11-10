# Plano · T11 Produção

- **Título:** Produção (o da fonte). 🔒 módulo `producao`: a fala diz que depende do plano contratado, sem preço; a tela
  de bloqueio (que mostra o preço por mês) não é gravada, só falada (⚠️ da fonte).
- **Antes:** Estoque: saldo, histórico e posição (T10). **Próximo:** CRM/Kanban (T26, o "Próximo" da fonte: "nenhuma
  oportunidade se perde no caminho").
- **Vinhetas (áreas):** PRODUÇÃO · FICHA TÉCNICA · ORDENS · LANÇAMENTO · RELATÓRIO · CONFIGURAÇÕES · RESUMO.
- **Exemplo da aula:** a latinha que a Recicla Vale compra vira fardo de alumínio na prensa; no ímã saem as latas de aço
  misturadas, que viram chaparia (o coproduto). Ficha e produto em **Kg**: só assim o relatório calcula o rendimento
  (`ProductionReport.tsx:128-153`). Segundo exemplo, já existente: a ficha do Cobre mel (descascar fio), que mostra a
  quantidade por unidade e serve à exclusão do capítulo 13.
- **Duração estimada:** ~16 min de vídeo (fala de ~13 min, mais 14 vinhetas, ilustrações e esperas da tela). Alvo da fonte:
  ~20 min.
- Base: `T11/inventario.md` (código 1.59.154). Logado como **Rafael Nogueira** (administrador MASTER: tem "Registrar
  Produção", "Gerenciar Fichas Técnicas" e vê custo).

## Capítulos

| # | Vinheta (área / título) | O que a tela mostra | Conceito ilustrado |
|---|---|---|---|
| 0 | (sem vinheta) | Dashboard → "Materiais" › "Produção". Problema do pátio; 🔒 falado; cartão "Antes". | O problema do pátio |
| 1 | PRODUÇÃO / O que a Produção resolve. | Abas (só as 4 da fonte na fala); o exemplo do começo ao fim; ⚠️ da tela desfocada, falado. | O caminho da produção |
| 2 | FICHA TÉCNICA / A receita do produto. | "Fichas Técnicas" › "Nova": "Alumínio latinha" entra, "Fardo de alumínio" sai; o "+" (sem clicar); "Nome da ficha". | A ficha é a receita |
| 3 | FICHA TÉCNICA / Quanto entra por unidade. | "Unidade de produção" Kg; "Qtd" 1; "Peças por unidade de venda" vazio; "Salvar ficha"; abre a ficha do "Cobre mel" (1,6). | Quantidade por unidade |
| 4 | FICHA TÉCNICA / Coprodutos. | Edita a ficha do fardo: "Adicionar coproduto" › "Chaparia" ("Quantidade digitada no lançamento do dia"); "Salvar ficha". | Coproduto (o ímã) |
| 5 | ORDENS / Criar a ordem de produção. | "Nova produção": ficha, 500 Kg, data, "Marcos Antunes", equipe Cláudio e Diego, "Consumo teórico estimado"; "Criar ordem"; ⚠️ das duas permissões. | A ordem é o plano |
| 6 | ORDENS / O kanban. | As três colunas; "Em produção" vira "Na prensa" ("Editar coluna", chave "Coluna de conclusão"); o check da "Concluída"; botão "Coluna"; arrasta a #3. | (a tela mostra) |
| 7 | LANÇAMENTO / A produção do dia. | Corte para o fim da tarde. Cartão › "Lançar produção do dia": Cláudio 260, Diego 220, "Total do dia" 480 Kg; subproduto Chaparia 14 Kg. | (a tela mostra) |
| 8 | LANÇAMENTO / O real contra o teórico. | "Matéria-prima usada": "Sugerido pela ficha: 480 Kg"; "Real" 498; "+18" em vermelho; ⚠️ quem baixa é o real. | Teórico × real |
| 9 | LANÇAMENTO / Perda acima da tolerância. | "Motivo da perda \*", "Informe o motivo da diferença", "Salvar lançamento" apagado (⚠️); "Material reaproveitável"; salvar. | Tolerância de perda |
| 10 | ORDENS / Finalizar e fechar o custo. | Arrasta a #3 para "Concluída" → "Finalizar #3": 96% da meta, "Resumo do lote", "Custo total do lote" R$ 3.087,60, "Custo por peça" R$ 6,43. | Custo estimado × real |
| 11 | RELATÓRIO / Relatório de Produção. | "PRODUTO" Fardo de alumínio: cartões, "% Perda" +3,8%, "% Rendim." 96,4%, "Custo/peça"; "Por funcionário" com "bateu" e "faltam 30"; "Exportar". | Rendimento e perda |
| 12 | CONFIGURAÇÕES / Os ajustes da Produção. | Multinível, "Quando dar baixa no estoque", liga "Bloquear finalização quando faltar matéria-prima em estoque", tolerância 2, meta 250. | Quando o estoque baixa |
| 13 | ORDENS / Excluir uma ordem concluída. | Exclui a #2 do Cobre mel (lançada em dobro): confirmação, "Ordem excluída"; Kardex do "Fio de cobre encapado" com as linhas "Produção" e o estorno; ⚠️ do Kardex. | Estorno |
| 14 | RESUMO / Recapitulando. | Montagem do que foi feito; cartão "Próximo: CRM/Kanban". | (montagem) |

Transições faladas: 0→1 "Vamos ver o que a Produção resolve"; 1→2 "Tudo começa pela ficha técnica"; 2→3 "Agora as
quantidades"; 3→4 "E quando sai mais de uma coisa do mesmo processo?"; 4→5 "Receita pronta, agora a ordem"; 5→6 "As
ordens ficam neste quadro"; 6→7 "Fim do dia, hora de lançar"; 7→8 "Embaixo fica a matéria-prima usada"; 8→9 "Com a
diferença, apareceu o campo Motivo da perda"; 9→10 "Lote prensado, hora de fechar a ordem"; 10→11 "Agora o relatório";
11→12 "Agora as configurações"; 12→13 "E quando uma ordem foi lançada errada?".

Cuidados da fonte e onde entram: 🔒 (cap00); ⚠️ tela desfocada (cap01, só falado: a tela mostra preço); ⚠️ permissões
separadas (cap05, "Uma dica:"); ⚠️ quem baixa é o real (cap08, "Uma dica:", com a diferença na tela); ⚠️ tolerância (cap09:
o bloqueio e o motivo na tela, que é o ponto, e depois "Uma dica:" sobre o botão apagado); ⚠️ Kardex (cap13, "Uma dica:", com o selo "Produção" na tela).

## Estado de partida
Mundo base da Recicla Vale (`MUNDO_FICTICIO.md`), `FAKE_NOW=2026-11-10T08:30:00-03:00` nos capítulos 0 a 6 e
**`2026-11-10T17:30:00-03:00` do capítulo 7 ao 14** (o lançamento é "no fim do dia"; a data do lançamento continua 10/11).
Rafael logado. Módulo `producao` ligado (plano Personalizado). Mais o que vem abaixo.

## Mundo: o que esta aula precisa
Tudo da semente da T11 (`seeds-extra/t11/`), sem entrar no mundo base: as ordens de novembro mexeriam no estoque das
aulas que vêm antes.

| Item | Valores |
|---|---|
| Material novo | **Fardo de alumínio**: grupo Alumínio, unidade "Kg", compra R$ 6,20, venda R$ 7,90 (o fardo prensado vende melhor que a latinha solta, R$ 7,40), NCM 7602.00.00, estoque 0, código = o próximo livre. Entra em `MUNDO_FICTICIO.md`. |
| Custo da latinha | "Alumínio latinha" com estoque ≥ 600 Kg em 10/11 (sugestão 1.240 Kg) e **média de todas as compras = R$ 6,20** (todas as compras de latinha a R$ 6,20): `get_material_cost_with_basis` devolve `{cost 6.20, basis_used media_historica, is_fallback false}`. "Fio de cobre encapado" com média R$ 18,00. |
| Funcionários (RH) | Os dois ajudantes do pátio do T19, ativos. Nomes provisórios (se o T19 já tiver nomeado, usar os dele e trocar na fala): **Cláudio Ferraz**, cargo "Ajudante de pátio", CPF 318.457.296-09; **Diego Morais**, cargo "Ajudante de pátio", CPF 704.163.528-71. |
| Ficha existente | **Cobre mel** (`production_recipes`: nome vazio, produto Cobre mel, `production_unit` "Kg", sem pack), insumo **Fio de cobre encapado 1,6** Kg por Kg (`loss_pct` nulo), sem coproduto. Criada em 01/11. |
| Ordens existentes | **#1** e **#2**, ambas Cobre mel, `production_date` 03/11/2026, planejado 50, produzido 50, `completed`, responsável "Rafael Nogueira", `created_by` Rafael, coluna "Concluída". Cada uma: um lançamento de 03/11 (Diego Morais 50), consumo do fio teórico 80 / real 80 / `line_cost` 1.440,00, saída Cobre mel 50 (principal), `total_material_cost` 1.440,00, `cost_per_unit` 28,80. A #2 é a mesma produção lançada duas vezes (o erro que o capítulo 13 desfaz). |
| Kardex dessas ordens | `stock_movements` tipo `PRODUCAO` de 03/11 ~16:00: Fio de cobre encapado −80 Kg (duas) e Cobre mel +50 Kg (duas). |
| Quadro | `production_kanban_columns`: "A fazer" (#EF4444, posição 0), "Em produção" (#F59E0B, 1), "Concluída" (#10B981, 2, `is_done`). |
| Configurações (`companies`) | `production_loss_tolerance_pct` **2**, `production_daily_goal` **250**; o resto no padrão (baixa a cada lançamento, bloqueio desligado, multinível desligado, sem exigir funcionário, custo pela média de todas as compras, pack "jogo", sem prefixo nem unidade padrão). |

Criado ao vivo: a ficha **Fardo de alumínio** (Alumínio latinha 1 Kg por Kg, unidade Kg, coproduto Chaparia); a ordem
**#3** (500 Kg, 10/11, responsável Marcos Antunes, equipe Cláudio e Diego, coluna "A fazer"); a coluna "Em produção"
renomeada **"Na prensa"**; o lançamento de 10/11 (Cláudio 260, Diego 220, Chaparia 14, latinha real 498 com motivo
"Material reaproveitável"); a finalização (R$ 3.087,60, R$ 6,43 por Kg); o bloqueio ligado; a #2 excluída.

Contas (conferidas): perda (498 − 480) ÷ 480 = 3,75% → "+3,8%"; rendimento 480 ÷ 498 = 96,39% → "96,4%"; custo 498 ×
6,20 = 3.087,60 ÷ 480 = 6,4325 → "R$ 6,43"; estimado 500 × 6,20 = 3.100,00 (R$ 6,20 por Kg); folga da tolerância 480 ×
2% = 9,6 Kg (18 passa, então pede motivo); 96% da meta.

**Estado final:** ficha do fardo e do cobre; #3 concluída; #1 concluída; #2 excluída com o estorno; coluna "Na prensa";
bloqueio ligado. Estoque: latinha −498, fardo +480, chaparia +14, fio +80 e cobre mel −50 em relação ao início.

## Gravação (modo fakebase)
- Desktop, tema claro, uma janela só, sem celular, sem página pública, sem outro usuário. Rotas: `/dashboard`,
  `/producao` (abas pelo clique), `/historico-materiais`.
- Sementes entre capítulos (cada capítulo abre um navegador novo; quando continua uma tela do anterior, o `setup` a refaz
  fora do vídeo): `inicio` (0 a 3), `apos-cap03` (ficha do fardo sem coproduto; entra no 4), `apos-cap04` (com Chaparia;
  5), `apos-cap05` (ordem #3; 6), `apos-cap06` ("Na prensa" e a #3 nela; 7, 8 e 9, com FAKE_NOW 17:30), `apos-cap09`
  (lançamento salvo; 10), `apos-cap10` (#3 concluída; 11 e 12), `apos-cap12` (bloqueio ligado; 13), `apos-cap13` (final).
- Backend falso, a ter (o cliente só chama isto; a cópia não tem migrations, então o comportamento vem do cliente e da
  Ajuda do app):
  1. RPC `upsert_production_recipe_atomic` (cria/atualiza cabeçalho e refaz insumos e coprodutos numa vez; devolve o id).
  2. RPC `get_material_cost_with_basis` (latinha 6,20) e `get_next_production_order_number` (devolve 3).
  3. `INSERT production_orders` (`draft`) e `production_order_workers` sem `entry_id` (a equipe); `UPDATE
     production_kanban_columns` (nome) e `production_orders.kanban_column_id` (arrastar).
  4. RPC `add_production_entry_atomic`: grava lançamento, consumo (`line_cost` = real × custo), saídas (principal e
     subproduto) e funcionários com `entry_id`; lança em `stock_movements` (`PRODUCAO`: latinha −498, fardo +480,
     chaparia +14); a ordem vira `in_progress` com `produced_qty` 480; idempotente por `p_client_request_id`; respeita o
     bloqueio de falta de matéria-prima.
  5. RPC `finalize_production_order_atomic`: `completed`, `total_material_cost` 3.087,60, `cost_per_unit` 6,4325 (o
     cliente depois move o cartão para a coluna `is_done`).
  6. RPC `delete_production_order_atomic` em ordem concluída: grava a movimentação inversa de cada linha de produção da
     ordem (fio +80, cobre mel −50) sem apagar as originais e tira a ordem das listas e do relatório.
  7. `UPDATE companies` dos ajustes (o capítulo 12 liga `production_block_on_insufficient_stock`).
  8. Relatório: leituras de `production_orders` (concluídas no período), `production_order_consumption`,
     `production_order_entries`, `production_order_workers`, `employees`.
- Integrações externas: nenhuma (sem edge function nesta aula).
- **Ilustrações** (cenas HTML no estilo da marca, `docs/09-aula-ilustrada.md`; nada de tela inventada do app): o problema
  do pátio (cap00), o caminho da produção (cap01), a ficha é a receita (cap02), quantidade por unidade (cap03), o ímã e o
  coproduto (cap04), a ordem é o plano (cap05), teórico × real (cap08), a faixa da tolerância (cap09), custo estimado ×
  real (cap10), rendimento e perda (cap11), quando o estoque baixa (cap12) e o estorno (cap13). Desenho de latas, prensa,
  fardo, ímã e balança em formas simples; números só os do mundo.
- Legenda: os números falados viram algarismo pelo `numeros` do `config_narracao.json` (ordem: do mais longo para o mais
  curto).

## Pontos para o Kaik
1. **Nomes dos ajudantes** (Cláudio Ferraz, Diego Morais) são provisórios até o T19 fechar os do pátio.
2. **Histórico de produção antes da aula**: a ficha do Cobre mel e as ordens #1 e #2 (a #2 em dobro) existem só para o
   capítulo 3 (exemplo de 1,6 Kg por Kg) e o 13 (excluir uma concluída sem desfazer o fardo da aula). Alternativa mais
   curta: excluir a própria #3 no fim, o que desfaria o resultado da aula.
3. **Tolerância 2% e meta 250 já configuradas** na semente: a fonte põe as Configurações no capítulo 12, depois do motivo
   (9) e do relatório (11). A fala diz onde ficam e o capítulo 12 confirma.
4. **"Peça" em produto por quilo**: a tela diz "Custo estimado por peça", "Custo por peça", "/peça" e "peças" mesmo no
   fardo em Kg; a fala avisa uma vez (cap05) que ali vale quilo. Handoff no inventário.
5. **"Observação" do lançamento não é gravada** no código: a aula não usa o campo. Handoff no inventário.
