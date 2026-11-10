# Plano · T3 Materiais e tabelas de preço (EcoFlix)

- **Título:** Materiais e tabelas de preço (o da fonte). Aula-molde da trilha e a primeira a gravar.
- **Objetivo:** montar o cardápio da Recicla Vale Metais: cadastrar um material completo (preços, estoque inicial, código,
  NCM, grupo), reajustar preços em massa, criar uma tabela de preço vinculada e ligá-la a um fornecedor, entender a ordem
  do preço no pedido, mexer no estoque na mão, exportar e ver o que o "Excluir" faz.
- **Antes:** T2 Usuários e permissões. **Próximo:** T4 Clientes, fornecedores e a ficha do parceiro.
- **Duração:** alvo da fonte ~15 min; fala de ~1.900 palavras (~12 min) + vinhetas e ações ≈ 14 min (`tts_textos.py`).
- Base: `T03/inventario.md` (código 1.59.154). Sem 🔒 na aula; a aba "Produção" do material é citada como do módulo de
  produção (depende do plano). Nenhuma edge function; nenhuma integração externa.

## Capítulos (os da fonte, na ordem)

| # | Vinheta (área / título) | O que a tela mostra | ⚠️ / 🚫 / ilustração | Alvo |
|---|---|---|---|---|
| 0 | (abertura) | Vinheta EcoFlix; ilustração do "cardápio"; Dashboard › "Materiais" › "Estoque"; cartão "Antes" | ILUSTRAÇÃO cardápio | 0:35 |
| 1 | ESTOQUE / A tela Estoque | Coluna "Tabelas de Preço"; barra; os três cartões; "Lista de Materiais" e colunas; corte do Marcos (cadeado) | ⚠️ valores sem permissão · ILUSTRAÇÃO Total Pago × Projeção | 1:00 |
| 2 | MATERIAIS / Cadastrar um material | "Novo Material": nome, unidade, "P. Compra", "P. Venda", "Quantidade em Estoque", "Criar"; "Importar planilha" aberto e fechado | ⚠️ planilha tudo ou nada · 🔒 aba Produção | 2:00 |
| 3 | MATERIAIS / O código do material | O 16 automático; "Editar": código "070" vira "70"; "Atualizar" | ⚠️ zero à esquerda · ILUSTRAÇÃO código | 1:20 |
| 4 | NOTA FISCAL / O NCM e a nota fiscal | "NCM (Nota Fiscal)" pela busca "Selecionar NCM para Materiais Recicláveis"; ajuda de "Identificação/Produto Fiscal" | ⚠️ NCM é do contador · ⚠️ nome fiscal · 🚫 impostos nos cenários fiscais · ILUSTRAÇÕES NCM, nome fiscal, material × cenário | 1:40 |
| 5 | GRUPOS / Grupos de material | "Grupos": "Radiadores" (nome, cor, ícone carro); grupo no radiador; filtro só "Cobre" e os cartões | ILUSTRAÇÃO gavetas | 1:30 |
| 6 | PREÇOS / Editar preços em massa | "Editar Tabela": busca "cobre", +0,50 na compra e na venda dos três cobres, "Salvar" | | 1:20 |
| 7 | PREÇOS / Várias tabelas de preço | "Nova Tabela": "Tabela Depósitos" +4% vinculada; lista com 44,20; "Tabela de Preços Padrão" do Depósito Irmãos Siqueira; compra só para ver o preço (tabela no cobre mel, personalizado no bronze) | ⚠️ ordem do preço + aviso "Preço especial aplicado para…" · ILUSTRAÇÕES vinculada, escada da prioridade | 2:30 |
| 8 | ESTOQUE / Movimentar, transferir e zerar | "Movimentar estoque": saída de 2 kg; "Transferir estoque": 8 kg para o Ferro misto; "Zerar Estoque" só mostrado | ILUSTRAÇÃO transferência | 2:00 |
| 9 | EXPORTAR / Exportar estoque e tabela | "Estoque (PDF)" com colunas; "Tabela de Preços (PDF)" da Tabela Depósitos em A4 | | 1:00 |
| 10 | MATERIAIS / Excluir um material | "Excluir" → "Confirmar Exclusão" (110 kg) → "Sim, Excluir" → "Desfazer" | ILUSTRAÇÃO arquivar × apagar | 1:00 |
| 11 | RESUMO / Recapitulando | Montagem; cartão "Próximo"; cartela | | 0:50 |

Transições faladas: 1→2 "Vamos cadastrar um material novo"; 2→3 "Agora, o código"; 3→4 "Pra quem emite nota fiscal...";
4→5 "Agora, os grupos"; 5→6 "O preço da sucata mexe toda semana"; 6→7 "A maioria dos pátios trabalha só com a principal";
7→8 "O estoque normalmente se mexe sozinho"; 8→9 "Pra levar o estoque pro papel"; 9→10 "Por último, o Excluir".

**Decisões (vale o código onde a fonte e o guia divergem):**
1. Venda abaixo da compra **não bloqueia** na 1.59.154 (pede "Salvar mesmo assim"); a aula não toca no assunto.
2. Cada capítulo deixa o mundo coerente com o `MUNDO_FICTICIO.md`: o reajuste do cap. 6 **leva o cobre aos preços do
   MUNDO** (a aula parte do cobre da semana passada); o "Excluir" é desfeito (o radiador continua); o "Zerar" só é mostrado.
3. A compra do cap. 7 só escolhe fornecedor e material (o preço chega e o aviso aparece); nada é incluído nem finalizado.
4. Sem prefixo de código (a fonte deixa de fora), sem "Posição de Estoque" (T10), sem "Desde 07/11" da planilha (produção,
   T11), sem o aviso de parceiro duplo na fala (T4). Exportação por grupo com subtotal fica para a Posição de Estoque (T10).

## Mundo: o que esta aula precisa

**Começa com** (fim do T2, sobre o mundo base): Recicla Vale Metais; Rafael Nogueira (MASTER) logado; Marcos Antunes
**sem** "Ver Totais e Valores Financeiros" (`action_view_financial_values`) e com a tela Estoque (só no corte do cap. 1);
os 15 materiais do MUNDO com **códigos 1 a 15 na ordem da tabela** (Ferro pesado 1 ... Plástico PET 15: o próximo é o 16 e
o 70 está livre); os 5 grupos (Ferrosos, Cobre, Alumínio, Metais, Outros); só a tabela **"PRINCIPAL"** (padrão, estrela);
`multiple_price_tables_enabled` ligado; histórico de compras de agosto a outubro (preço médio pago).

| Item | Valores | Onde |
|---|---|---|
| Cobre na semana passada (só da semente `t3/inicio` até o cap. 6) | Cobre mel 42,00 / 47,40; Cobre misto 35,50 / 41,00; Fio de cobre encapado 17,50 / 21,50 (o cap. 6 sobe R$ 0,50 e chega no MUNDO) | `materials` e `price_table_items` da PRINCIPAL |
| Preço personalizado (novo no mundo base; fica) | Depósito Irmãos Siqueira (lado fornecedor) × Bronze: **R$ 30,50**, fixo (selo "1 preço personalizado") | `entity_custom_prices` |
| NCMs sugeridos (tabela global) | categoria "Cobre": 7404.00.00 "Desperdícios e resíduos de cobre"; "Alumínio": 7602.00.00 "Desperdícios e resíduos de alumínio"; "Ferro e aço": 7204.49.00 "Outros desperdícios e resíduos de ferro ou aço" e 7204.21.00 "Desperdícios e resíduos de aços inoxidáveis"; "Baterias": 8549.11.00 "Desperdícios e resíduos de acumuladores elétricos de chumbo"; "Papel": 4707.10.00 "Papel ou cartão kraft não branqueado ou ondulado"; "Plástico": 3915.90.00 "Desperdícios, resíduos e aparas de outros plásticos"; `tax_notes` vazio (de preferência, copiar as linhas reais de `ncm_presets`, que é tabela pública) | `ncm_presets` |
| Caixa (só na semente do cap. 7) | caixa do Rafael aberto em 10/11, 07:45, com R$ 800,00 de troco; `apos-cap07` volta sem o caixa e sem o rascunho da compra | `cash_registers` |

**Criado na tela:** "Radiador de cobre" (Kg; compra R$ 21,00; venda R$ 24,50; estoque 120 kg; código 16 → **70**; NCM
**7404.00.00**; grupo "Radiadores"); grupo **"Radiadores"** (cor #0F766E, ícone `car`); reajuste do cobre (+R$ 0,50 na
compra e na venda: Cobre mel 42,50 / 47,90, Cobre misto 36,00 / 41,50, Fio de cobre encapado 18,00 / 22,00); **"Tabela
Depósitos"** (vinculada à principal, Porcentagem, 4, Aumenta: Cobre mel 44,20); **Tabela de Preços Padrão** do Depósito
Irmãos Siqueira = Tabela Depósitos (vale também no lado cliente, pelo cadastro duplo); saída de 2 kg do radiador
("Ajuste de inventário"); transferência de 8 kg do radiador para o Ferro misto; exclusão do radiador desfeita.

**Fica para as próximas** (consolidar no MUNDO): radiador com 110 kg, código 70, NCM, grupo Radiadores; Ferro misto +8 kg;
dois movimentos manuais de 10/11 no histórico (T10 vê); Tabela Depósitos ligada ao Depósito Irmãos Siqueira (na venda
para ele, T7, a tabela também vem selecionada); o próximo código livre é o **71**; o preço personalizado do bronze.

**Sementes entre capítulos** (cada capítulo abre num navegador novo; o `setup` refaz fora do vídeo o que o capítulo
continua): `inicio` (caps. 0 a 2), `apos-cap02` (radiador 16), `apos-cap03` (código 70), `apos-cap04` (NCM),
`apos-cap05` (grupo), `apos-cap06` (cobre reajustado; entrada do 7, com o caixa aberto), `apos-cap07` (tabela e vínculo;
sem caixa), `apos-cap08` (radiador 110 kg; entrada dos caps. 9 a 11). O cap. 9 seleciona a Tabela Depósitos na tela; o
10 termina igual ao `apos-cap08`.

## Gravação

- Computador 1280×800, Rafael logado, `FAKE_NOW=2026-11-10T08:30:00-03:00`. Tema claro.
- **Rotas:** `/dashboard` (abertura), `/materiais`, `/clientes-fornecedores`, `/caixa` → `/compra` (cap. 7). PDFs em
  **aba nova** (cap. 9: "Lista de Materiais" e a tabela A4): gravar a aba nova.
- **Backend (falso):** `materials` (select, insert, update), `price_tables` (select, insert), `price_table_items`
  (select, insert, update), `rpc save_price_table_items`, `material_groups` (select, insert), `ncm_presets` (select),
  `purchase_items` + `purchases` (preço médio pago), `rpc adjust_material_stock_atomic` (motivos "SAIDA" e o de edição),
  `rpc transfer_material_stock`, `stock_movements` (insert e delete do "Excluir" + "Desfazer"), `suppliers`/`customers`
  (update de `default_price_table_id`, os dois lados), `entity_custom_prices` (select), `cash_registers` (caixa aberto),
  `order_drafts` (upsert do rascunho da compra), `companies` e `profiles` (PDF). `get_sped_rollout_context` desligado
  (some o "Tipo do item no SPED Fiscal"); "Resíduo do MTR" pode aparecer se a UF tiver MTR ativo (a câmera não para nele).
  Edge functions: nenhuma.
- **Outro usuário:** Marcos Antunes, uma linha do cap. 1 (mesma tela, valores com cadeado). Depende das permissões que
  o T2 dá a ele.
- **Cuidados do robô:** a lista tem 10 por página (o radiador cai na página 2: busca "radiador"); a "Cor" do grupo é
  `<input type="color">` (definir o valor, sem a janela nativa); o "Desfazer" vive 5 s (clicar ~2,5 s depois do aviso);
  na compra, balança sem leitura (EcoTray falso parado) e nenhum item incluído; digitação dos preços acelerada (selo 4x).
- **Zooms** (frase inteira, ≥ 2,5 s, um por vez): preços e estoque do cadastro, código 70, NCM 7404.00.00, Cobre mel na
  edição em massa, exemplo de cálculo da tabela, 44,20 na lista, "Tabela de Preços Padrão", "Valor/kg" 44,20 e 30,50 na
  compra, antes/depois da saída, quantidade da transferência, aviso de exclusão.
- **Ilustrações** (estilo `docs/09-aula-ilustrada.md`, sem marca, sem tela inventada): 0 cardápio do pátio; 1 Total Pago ×
  Projeção de Vendas; 3 código automático e o caderno; 4 o NCM na nota, o nome fiscal (três alumínios) e material ×
  cenário fiscal; 5 grupos como gavetas; 7 tabela vinculada (+4%) e a escada da prioridade; 8 transferência (o radiador e o
  ferro das cintas); 10 arquivar × apagar.
- **Pronúncias:** as do PERFIL que a aula usa (NCM, PDF, CFOP, CST, ICMS); nenhuma nova. "Excel" e "Siqueira" a conferir
  no ensaio. Números por extenso na fala, com legenda em algarismo (`numeros` do `config_narracao.json`).
