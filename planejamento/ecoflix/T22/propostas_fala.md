# T22 · Propostas de fala e achados do app (robô e ensaio, 11/11)

Feito no ensaio do robô com o app 1.59.154 e o Supabase falso da aula (instância 54322, `FAKE_NOW=2026-11-10T08:30:00-03:00`). Os números
do grupo saem das RPCs de grupo reproduzidas das migrations do app (handlers em `rec/mundo/handlers/rpc/`, contas em
`rec/mundo/lib/grupo.mjs`), somando as unidades do mundo: nenhum total foi escrito à mão. A revisão geral aplica; `roteiro.md` e
`tts_textos.py` não foram mexidos.

## Propostas de fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 07 | L1 | "... o custo só do material que foi vendido: duzentos e setenta e três mil, oitocentos e sessenta." | "... o custo só do material que foi vendido: quase duzentos e setenta e quatro mil." | A tela mostra **CMV R$ 273.873,30**. A RPC de verdade (`get_group_financial_dre_summary`, migration 20261014084500) calcula o CMV pelo estoque: Σ por empresa (estoque no fim da véspera + compras − estoque no fim do período), com o custo médio de compra. Em 31/10 o mundo base tem a contagem do pátio que tira 14 kg de ferro pesado (−14 × R$ 0,95 = R$ 13,30): ela entra no CMV por estoque. Matriz 218.873,30 + filial 55.000,00. |
| 07 | L2 | "E o resultado do mês vira positivo: dezoito mil, trezentos e cinquenta reais." | "E o resultado do mês vira positivo: dezoito mil, trezentos e trinta e seis reais." | A tela mostra **Resultado do Período R$ 18.336,70** (Lucro Bruto R$ 64.966,70, "Margem Bruta: 19.0%"), pelo mesmo motivo. |
| 07 | L3 | "A diferença, quarenta e cinco mil, é o material..." | "A diferença, quase quarenta e cinco mil, é o material..." | −26.650,00 em caixa e 18.336,70 em competência: R$ 44.986,70. Na ilustração `ilu07_caixa` (`T22/cenas/`), "R$ 45.000,00" vira "R$ 44.986,70" e "− R$ 273.860,00" vira "− R$ 273.873,30". |
| 09 | L6 | "... O que ela já tinha fica como está, e o que faltava entra. Os preços dela só mudam se você ligar o Sobrescrever preços existentes." | "... O que ela já tinha fica como está, e o que faltava entra." | Com "Tabelas de Preço" marcado (o padrão da janela), o `push_group_assets_to_company` (migration 20260528001000, passo 2) grava os preços da tabela padrão do grupo na tabela Principal da filial e nos materiais dela, com ou sem "Sobrescrever preços existentes" (ver Achados). No mundo os preços das duas unidades são iguais e nada muda na tela, mas a frase ensinaria o contrário do que o sistema faz. |

Alternativa para o cap07 (decisão da junção, não desta aula): tirar a contagem de −14 kg de 31/10 do mundo base devolve o CMV de
R$ 273.860,00 e o resultado de R$ 18.350,00 da fala, mas a T10 fala dessa contagem. O mesmo vale para a T15: no app de verdade a DRE de
outubro da matriz em competência dá R$ 10.336,70 (o handler da DRE da unidade no Supabase falso, `lib/eco.mjs` `resumoDRE`, faz Σ vendido ×
custo médio e mostra R$ 10.350,00).

## O que o robô faz diferente do roteiro (sem mudar a fala)

- **Código de convite GRP-7C4E9A** (o roteiro tinha GRP-7KQ4TX): a função do app (`generate_group_invite_code`, migration 20260308090641) usa
  6 caracteres de um md5 em maiúsculas, só 0-9 e A-F; "K", "Q", "T" e "X" nunca sairiam dela. A fala não diz o código. **A ilustração do
  cap03 (`ilu03_dia`: `T22/cenas/cenas.html`, `const CODIGO`, e o `mostra` do `ilustracoes.json`) e o `MUNDO_FICTICIO.md` precisam do
  código novo.**
- **cap10 L6**: a lista de transferências mostra só "Concluída"; os saldos que a fala diz (matriz 1.840 kg, filial 650 kg, total 2.490 kg)
  aparecem no Estoque Gerencial. O robô confirma, mostra "Concluída" e abre Estoque › Visão Geral na linha do alumínio latinha.
- **cap09 L2**: depois do "Importar do Estoque da Matriz" cada material do catálogo aparece com "1 vínculo(s)" (o gatilho do banco liga o
  material da matriz de mesmo nome, migration 20260727181000); depois do "Enviar Ativos", "2 vínculo(s)". No resultado do envio:
  Materiais 0 novo(s) (os 15 da filial já existiam e só foram ligados), Categorias 8, Tabelas de Preço 1 (a "Tabela Depósitos"),
  Clientes 0 (a Fundição já é cliente da filial), Fornecedores 0.
- **cap06 L1**: o Financeiro abre direto na aba DRE (a última aberta) e o período passa a "Mês passado" enquanto a fala diz "com outubro
  escolhido" (clicar na aba e no período dentro da linha atrasava a L2).
- **cap07 L4**: os dois cliques do seletor de regime são feitos sem levar o cursor (o seletor fica fora da tela quando o resultado está
  no quadro): a câmera fica parada no resultado enquanto ele muda.
- **cap08 L5**: o robô aponta as colunas "Valor Comprado", "Valor Vendido" e "Lucro" do Relatório de Estoque e, para a margem, o cartão
  "Margem" do alto (a coluna "Margem" da tabela fica cortada à direita; a tabela rola de lado). O relatório mostra o mês corrente (1 a
  10/11), sem número na fala.
- **cap08 L4**: o Histórico de Materiais abre com a compra da filial de 09/11 16:20 (Rosa Medeiros: alumínio latinha e papelão) no alto, para
  "com a unidade de onde veio" mostrar "Filial Pindamonhangaba" na primeira linha.

## Achados do app

1. **Histórico de Envios não acompanha o envio** (Configurações do grupo › Unidades): logo depois do "Confirmar Envio" a lista continua
   "Nenhum envio registrado ainda." e o passo a passo "Nenhum envio realizado" (a consulta `group-push-audit` não é invalidada pelo
   envio; só volta ao abrir a página de novo). E quando aparece, a linha "→ Filial Pindamonhangaba" diz "Nenhum ativo": a tela lê
   `entry.materials_count`, `categories_count`, `price_tables_count`, `customers_count` e `suppliers_count`
   (`pages/GerencialConfiguracoes.tsx`), mas a tabela `group_push_audit` grava `materials`, `categories`, `price_tables`, `customers` e
   `suppliers` (no cap09 foram 8 categorias e 1 tabela). Na gravação o zoom da L8 fica na lixeira, longe desse bloco.
2. **"Sobrescrever preços existentes" não protege os preços da filial**: com "Tabelas de Preço" marcado, o `push_group_assets_to_company`
   sincroniza a tabela Principal da filial com a tabela padrão do grupo (upsert dos itens) e ainda atualiza `purchase_price`/`sale_price` dos
   materiais da filial, mesmo com a chave desligada; a janela diz "Itens já existentes na filial serão ignorados" e "Se ativado, os preços dos
   materiais da filial serão atualizados com os preços do grupo".
3. **A setinha do Dashboard Gerencial não compara com o mês anterior**: `getPreviousPeriod` usa a mesma duração que termina na véspera
   (para "Mês passado" = 01 a 31/10, compara com 31/08 a 30/09). A fala ("compara com o mês anterior") vale na prática.
4. **A volta pelo código existe** (risco 5 do plano): `join_group_by_invite_code` (migration 20260405225817) reativa o vínculo `removed`
   da mesma filial com a data de agora. A dica do cap09 L8 está certa.
5. Riscos 1 e 2 do plano confirmados no código: "Lucro Líquido" do Dashboard Gerencial = vendas − compras; "(-) Compras (CMV)" do Comparativo
   mostra as compras nos dois regimes.
