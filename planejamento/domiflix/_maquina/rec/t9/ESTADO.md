# T9 · estado da gravação (porta 54326) · retomada 04/11, app 1.38.19

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54326` em TODO comando; `FAKE_NOW=2026-11-03T09:00:00-03:00` no backend (`FAKE_NOW=... FAKE_PORT=54326 rec/run.sh fake`) e no robô;
navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava por capítulo (`rec/t9/rodar.sh NN [--rapido] [--seed]`, lote `rec/t9/lote.sh 0 1 2 ...`, NA ORDEM);
sem pkill; `rm` só com `"${VAR:?}"`; escrever só em `t9/`, `rec/t9/`, `rec/fakebase/seeds-extra/t9/` e handlers novos; sem commit. Disco: parar abaixo de 3 GB.

## Fase 1 (04/11)
- Mundo: `semear.py` -> `seeds-extra/t9/inicio.json` + `cadeia.json` (cadeia: t3/apos-cap10, t1/apos-cap13, t4/inicio, t4/apos-cap14, t5/inicio, t9/inicio).
  Trilha Domiflix com `is_onboarding: false` por `_patch` no id da base (G1); tabelas vazias de propósito (`VAZIAS`) para `/__dev/unknowns` ficar vazio
  (inclui a view `cost_resources_with_rate`); `pricing_settings` zerada com `card_installments 1` (como o banco).
- Handler novo: `handlers/functions/notify-quote-response.mjs` (a página pública chama depois do Aprovar). O resto (RPCs de proposta, `generate_service_order_from_quote`
  com BDI, view de recursos) já existia.
- Robô: `gerar.py` -> `cap00..cap16.json`; `confere(...)` lê a tela e compara com a fala (o `resumo.py` acusa DIFERENTE); `OBS` vigia aviso de erro, tela escura e faixa da trilha.
- Sementes da cadeia: `rodar.sh NN --rapido --seed` grava `apos-capNN` (o `snap.mjs` descarta `_patch` de tabelas de ligação sem `id`, que corromperiam o vínculo das OS).
- Lições desta fase: campo `type=number` com 0 de partida e NumericInput de quantidade reescrevem o valor ao apagar ("032", "13", horas mensais 176176 -> custo/hora R$ 0,02):
  selecionar tudo (Ctrl+A) e digitar por cima (`digitar_num`), e CONFERIR o valor lido na tela (o ensaio rápido passa sem acusar).
  Tooltip nativo (atributo `title`) não aparece na gravação. As 7 seções da proposta vêm todas ligadas (Garantia já vem ligada).
  Após "Próximo" o corpo do assistente mantém a rolagem: `TOPO` (scrollTo 0).

## Resultado da fase 1 (04/11, ensaio --rapido na ordem 0 a 16, depois de reiniciar o falso)
- 17 de 17 capítulos: 0 passo falho, `/__dev/unknowns` vazio, `window.__avisos` vazio (sem aviso de erro, tela escura ou faixa da Domiflix), 0 DIFERENTE nas conferências tela x fala
  (BDI 0.6000, 1.666,67; Van 01 R$ 20,00/h; 48 + 30 + 30 = 108 e 180; 3 × 180 + 350 = 890; R-410A 150; deslocamento 27 -> 45; desconto 85; sugerido 1.085 / praticado 1.000;
  à vista 950 / 10x 100; proposta pública 890 + 150 + 45 − 85 = 1.000; #2 em 3 parcelas 20/11, 20/12, 20/01; OS #17 Agendada com total para faturamento 1.000).
- Sementes da cadeia: `seeds-extra/t9/apos-cap00..16.json` (cumulativas sobre `t9/inicio`).

## Onde a tela difere do roteiro/fala (para o main decidir; nada de preço mudou)
1. Seções da proposta (cap10): as sete vêm LIGADAS. O robô desliga a Garantia em "desligo" e liga em "Ligo a Garantia" (fala continua certa).
2. Dica do olho (cap13): é `title` nativo, não grava. O mesmo texto ("Visualizada 3× · última vez 02/11 16:20") sai no topo do Visualizar do #2; o robô abre o Visualizar nesse trecho.
3. OS #17 (cap15): a lista de OS não tem coluna de valor (e abre no Kanban, que também não mostra). O robô muda para a lista e abre "Visualizar OS": "Total para faturamento R$ 1.000,00".
4. Revisão (cap09): ao lado do "Preço sugerido R$ 1.085,00" há "Composição do preço sugerido R$ 585,00" (só a parte do BDI automático). Confere com a conta do IMPACTO, mas a tela traz dois "sugerido".
5. Linha expandida do serviço (cap06): o rótulo é "Recursos e extras" (a fala diz "custos extras"). Ficha da Van 01 mostra "Cliente paga com BDI por hora R$ 33,33" (não citado).
6. Com a janela de 1280 px o botão "Configurar Proposta" cobre parte da aba "Precificação" na aba Orçamentos (visto no cap01; para o editor/câmera).
7. Cadastro do assistente: o campo se chama "Observações internas" (placeholder), mas o texto sai na proposta (P9 do inventário).
