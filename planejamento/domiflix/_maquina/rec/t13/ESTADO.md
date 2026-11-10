# T13 · estado da gravação (porta 54332) · fase 1 em 04/11, app 1.38.19

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54332` em TODO comando; `FAKE_NOW=2026-11-10T10:00:00-03:00` no backend
(`FAKE_NOW=... FAKE_PORT=54332 rec/run.sh fake`) e no robô; navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava por capítulo
(`rec/t13/rodar.sh NN [--ensaio] [--rapido] [--seed]`, lote `rec/t13/lote.sh 2 3 4 ...` NA ORDEM); sem pkill; `rm` só com caminho literal; escrever só em
`t13/`, `rec/t13/`, `rec/fakebase/seeds-extra/t13/` e handlers novos; sem commit. Disco: parar abaixo de 3 GB.

## Mundo
- `semear.py` -> `seeds-extra/t13/inicio.json` + `cadeia.json`. Cadeia: a do T12 (`t3/apos-cap10, t1/apos-cap13, t4/inicio, t4/apos-cap14, t5/inicio, t5/apos-cap05, t12/inicio`)
  + `t12/apos-cap11` + `t13/inicio`. O T13 NÃO depende de dado novo do T10 nem do T11 (o contrato PMOC do hotel vem do `t12/inicio`).
- `t13/inicio`: G1 (`_patch` da trilha com `is_onboarding: false`), estoque do T8 (12 materiais, Estoque Principal + Van 01, Mangueira de dreno com 60 m a 3,50),
  Financeiro padrão (Caixa e Conta Principal com `is_cash_account: true`; 14 + 14 categorias com `sort_order 0`, como o DEFAULT do banco; 6 grupos do DRE e `dre_group_id`
  das categorias, imitando os gatilhos), 3 parcelas do Orçamento #2 (20/11, 20/12, 20/01) e 12 "Mensalidade PMOC" (R$ 1.200,00, dia 10, de 10/12/2026 a 10/11/2027,
  sem `installment_*`, como o contrato grava: com `installment_total > 1` o recebimento parcial do cap. 11 some). Tabelas vazias de propósito para `/__dev/unknowns` ficar vazio.
- Sementes da cadeia: `rodar.sh NN --rapido --seed` grava `apos-capNN` (cumulativas sobre `t13/inicio`; `snap.mjs base` precisa rodar de novo sempre que `inicio` mudar).

## Handlers novos (rec/fakebase/handlers/rpc/)
- `registrar_compra_material_direta.mjs` (cap. 5): compra `compra_direta` concluída, ordem interna, itens, entrada no estoque (via `receber_ordem_compra`) e a despesa paga/a pagar.
- `pay_credit_card_bill.mjs` (cap. 9): duas pernas com o mesmo `transfer_pair_id`, fatura `paid`/`partial`, compras quitadas; recusa fatura que ainda não fechou.

## Robô
- `gerar.py` é montado por `montar_gerar.sh` (base + `cap_parte1..3.txt`); `confere`, `confere_campos`, `confere_ausente` leem a tela e comparam com a fala (o `resumo.py` acusa DIFERENTE);
  `OBS` vigia aviso de erro, tela escura e faixa da trilha Domiflix.
- Lições: ver o relatório da fase 1 (Select do Radix com lista longa tem de ser pelo teclado; SearchableSelect de material: clique + espera da opção; menu ⋮ da linha: 2º clique condicional;
  a linha da fatura do cartão também é botão; `rodar.sh` usa `grep -qz` no lugar de `tr | grep -q` (SIGPIPE com pipefail dava "instância ausente" de vez em quando)).
