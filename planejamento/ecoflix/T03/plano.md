# Plano · T3 Materiais e tabelas de preço (EcoFlix), aplicado ao app 1.60.18

- **Título:** Materiais e tabelas de preço (o da fonte). Aula-molde da trilha e a primeira a gravar.
- **Objetivo:** montar o cardápio da Recicla Vale Metais: cadastrar um material completo (preços, estoque inicial, código,
  NCM, grupo), reajustar preços em massa, usar a margem automática (tabela toda e por material), criar uma tabela de preço vinculada e ligá-la a um fornecedor, entender a ordem
  do preço no pedido, mexer no estoque na mão, exportar e ver o que o "Excluir" faz.
- **Antes:** T2 Usuários e permissões. **Próximo:** T4 Clientes, fornecedores e a ficha do parceiro.
- **Duração:** fala de 3.600 palavras (~23 min de voz) + vinhetas e ações ≈ 26 min (`tts_textos.py`). Era 1.959 palavras e ~14 min no 1.59.154; a aula não se divide (pedido do Kaik): entraram a margem automática, o menu da tabela e as dicas do 1.60.
- Base: `T03/inventario.md` (código 1.60.18, commit e8edc9e6d; seção 14 = margem automática). Sem 🔒 na aula; a aba "Produção" do material é citada como do módulo de
  produção (depende do plano). Nenhuma edge function; nenhuma integração externa.

## Capítulos (17; novos: 7, 8, 9, 10 e 12; os antigos 7 a 11 viraram 11, 13, 14, 15 e 16)

| # | Vinheta (área / título) | O que a tela mostra | ⚠️ / 🚫 / ilustração | Alvo |
|---|---|---|---|---|
| 0 | (abertura) | Vinheta; ilustração do "cardápio"; Dashboard › "Materiais" › "Estoque"; cartão "Antes" | ILUSTRAÇÃO cardápio | 0:35 |
| 1 | ESTOQUE / A tela Estoque | Coluna "Tabelas de Preço" (com o "?"); barra com "Editar Preços"; cartões; "Lista de Materiais" e colunas, ordenar por coluna; corte do Marcos | ⚠️ valores sem permissão · ILUSTRAÇÃO Total Pago × Projeção | 1:10 |
| 2 | MATERIAIS / Cadastrar um material | "Novo Material"; "Importar planilha" aberto e fechado | ⚠️ planilha tudo ou nada · 🔒 aba Produção | 2:00 |
| 3 | MATERIAIS / O código | O 16 automático; código "070" vira "70" | ⚠️ zero à esquerda · ILUSTRAÇÃO código | 1:20 |
| 4 | NOTA FISCAL / O NCM | "NCM (Nota Fiscal)"; nome fiscal | ⚠️ NCM é do contador · 🚫 impostos · ILUSTRAÇÕES | 1:40 |
| 5 | GRUPOS / Grupos | "Radiadores"; filtro "Cobre" | ILUSTRAÇÃO gavetas | 1:30 |
| 6 | PREÇOS / Editar preços em massa | Tela cheia "Editar Tabelas de Preço": resumo, busca "cobre", três cobres, "Venda abaixo da compra" no bronze, aviso "Preço de venda abaixo do custo" (Cancelar), "Salvar" | | 2:20 |
| 7 | PREÇOS / Margem automática: a tabela toda | Chave, "Tabela toda", 15%, "Qual preço fica como está?", coluna "Margem", compra muda (venda segue), venda muda (compra segue), "Editar margem" 20, cadeado do Ferro misto; termina em "Cancelar" | ILUSTRAÇÃO margem sobre a compra | 2:40 |
| 8 | PREÇOS / Margem automática: uma por material | "Por material", "%" e "R$", margem de cada linha, Cobre misto 15, Bronze em R$, "Mesma margem em vários materiais" (3 alumínios), chave desligada; termina em "Cancelar" | | 2:20 |
| 9 | PREÇOS / O resumo e a margem fora da regra | Semente `margem-fora`: "Venda abaixo da compra", "Sem preço", "Margem típica", "Fora da margem" e o selo que realinha o Alumínio latinha; termina em "Cancelar" | ILUSTRAÇÃO fora da margem | 2:20 |
| 10 | MATERIAIS / A margem no cadastro | Semente `margem-material`: "Editar Material" do radiador, calculadora "Calcular venda pela margem", "Aplicar", "Tirar a margem deste material"; termina em "Cancelar" | | 1:40 |
| 11 | PREÇOS / Várias tabelas de preço | "Nova Tabela" +4%; Variação por material no Editar Preços (tabela vinculada sem cartão de margem); vínculo ao Depósito Irmãos Siqueira; ordem do preço na compra | ⚠️ ordem do preço · ILUSTRAÇÕES vinculada, escada | 3:20 |
| 12 | PREÇOS / Duplicar, fixar e trocar a principal | Menu "..." da tabela: "Configurações", "Duplicar tabela" (excluída em seguida), "Fixar para meus pedidos e tickets" (removida), "Definir como principal da empresa" (cancelada) | ILUSTRAÇÃO qual tabela o pedido abre | 2:40 |
| 13 | ESTOQUE / Movimentar, transferir e zerar | Saída de 2 kg; transferência de 8 kg; "Zerar Estoque" só mostrado | ILUSTRAÇÃO transferência | 2:00 |
| 14 | EXPORTAR / Estoque e tabela | "Estoque (PDF)" e "Tabela de Preços (PDF)" A4: PDFs **na tela** (aba nova) | PDFs `comprovante`/`pdf` | 1:10 |
| 15 | MATERIAIS / Excluir um material | "Confirmar Exclusão" (110 kg), "Desfazer" | ILUSTRAÇÃO arquivar × apagar | 1:00 |
| 16 | RESUMO / Recapitulando | Montagem (6 linhas); cartão "Próximo"; cartela | | 1:00 |

Transições faladas: 1→2 "Vamos cadastrar um material novo"; 2→3 "Agora, o código"; 3→4 "Pra quem emite nota fiscal..."; 4→5 "Agora, os grupos";
5→6 "O preço da sucata mexe toda semana"; 6→7 "Antes, uma novidade do Editar Preços: a margem automática"; 7→8 "Nem todo material tem a mesma margem";
8→9 "Quando a margem já está gravada..."; 9→10 "A margem também aparece no cadastro do material"; 10→11 "A maioria dos pátios trabalha só com a tabela principal";
11→12 "Cada tabela tem um menu nos três pontinhos"; 12→13 "O estoque normalmente se mexe sozinho"; 13→14 "Pra levar o estoque pro papel"; 14→15 "Por último, o Excluir".

**Decisões (vale o código onde a fonte e o guia divergem):**
1. Venda abaixo da compra **não bloqueia** (pede "Salvar mesmo assim"); no 1.60.18 o resumo conta "Venda abaixo da compra" e a aula **mostra** isso no cap. 6 (e no 9, pela margem negativa). Os caps. 7 a 10 são variantes: não gravam nada e terminam em "Cancelar" (a margem gravada, quando preciso, vem das sementes `margem-fora` e `margem-material`). A margem é sempre sobre a compra (markup); preço guarda até 3 casas.
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
| Caixa (só na semente do cap. 7) | caixa do Rafael aberto em 10/11, 08:30, com R$ 800,00 de troco (junção: no mundo base nenhum caixa abre em 10/11 antes das 08:31, T6; este é só da semente do cap. 7); `apos-cap07` volta sem o caixa e sem o rascunho da compra | `cash_registers` |

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
`apos-cap05` (grupo), `apos-cap06` (cobre reajustado; entrada dos caps. 7 a 11, com o caixa aberto no 11), `apos-cap07` (tabela e vínculo; sem caixa; entrada dos 12 e 13),
`apos-cap08` (radiador 110 kg; entrada dos caps. 14 a 16). **Os nomes seguem a numeração antiga.** Novas: `margem-fora` (cap. 9: Principal com margem
"Por material" gravada e Alumínio latinha a 7,80) e `margem-material` (cap. 10: o mesmo, preços batendo), em `rec/mundo/seeds-extra/t03/`. O cap. 14 seleciona a Tabela
Depósitos na tela; o 15 termina igual ao `apos-cap08`; o 12 termina com o mundo da entrada (cópia excluída, fixação removida).

## Gravação

- Computador 1600×900 (16:9), Rafael logado, `FAKE_NOW=2026-11-10T08:30:00-03:00`. Tema claro.
- **Rotas:** `/dashboard` (abertura), `/materiais`, `/clientes-fornecedores`, `/caixa` → `/compra` (cap. 7). PDFs em
  **aba nova** (cap. 14: "Lista de Materiais" e a tabela A4): o robô devolve o PDF (`t03_pdfs`) e há entradas `comprovante`/`pdf` em `cenas/ilustracoes.json`.
- **Backend (falso):** `materials` (select, insert, update), `price_tables` (select, insert), `price_table_items`
  (select, insert, update), `rpc save_price_table_items`, `rpc save_price_table_margins` (só existe para o ensaio; os caps. 7 a 10 não salvam), `rpc duplicate_price_table`, `rpc set_my_preferred_price_table` (handlers da aula em `rec/mundo/handlers/rpc/`, espelham as migrations 20261119190000, 20261111192000 e 20261112162947), `price_table_material_margins`, `material_groups` (select, insert), `ncm_presets` (select),
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
- **Mundo privado:** o `schema.json` compartilhado está velho (sem `price_table_material_margins`); a aula usa `rec/t03/_mundo/` (links + `schema.json` regenerado do 1.60.18). Pedido ao mundo base: regenerar o `schema.json`.
- **Zooms** (frase inteira, ≥ 2,5 s, um por vez): preços e estoque do cadastro, código 70, NCM 7404.00.00, Cobre mel na
  edição em massa, exemplo de cálculo da tabela, 44,20 na lista, "Tabela de Preços Padrão", "Valor/kg" 44,20 e 30,50 na
  compra, antes/depois da saída, quantidade da transferência, aviso de exclusão.
- **Ilustrações** (estilo `docs/09-aula-ilustrada.md`, sem marca, sem tela inventada): 0 cardápio do pátio; 1 Total Pago ×
  Projeção de Vendas; 3 código automático e o caderno; 4 o NCM na nota, o nome fiscal (três alumínios) e material ×
  cenário fiscal; 5 grupos como gavetas; 7 tabela vinculada (+4%) e a escada da prioridade; 13 transferência (o radiador e o
  ferro das cintas); 15 arquivar × apagar. Novas (v3 pendente): 7 margem sobre a compra, 9 fora da margem, 12 qual tabela o pedido abre. Numeração: 7 vinculada e escada → 11.
- **Pronúncias:** as do PERFIL que a aula usa (NCM, PDF, CFOP, CST e ICMS em IPA, provisório); troca nova "á-quatro" →
  "A4". "Excel" e "Siqueira" a conferir no ensaio. Números por extenso na fala, com legenda em algarismo (`numeros` do
  `T03/narracao/config_narracao.json`).
