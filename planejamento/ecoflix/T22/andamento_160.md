# T22 · andamento da aplicação no 1.60.18 (20/11)

**Feito:** `tts_textos.py` (19 caps, 2.838 palavras), `roteiro.md` (gerado do tts + docstrings do robô), `plano.md` e `inventario.md`
(nota de atualização), `preparar_aula.sh T22`, `rec/t22/gerar.py` (18 caps com robô, monta sem erro de âncora), sementes
`t22/codigo-vencido` e `t22/venda-outra-unidade`, 8 handlers novos, `t22_estado.py` (`NOME_SEMENTE`), `cenas/ilustracoes.json`
(6 novas, 4 renumeradas, todas `v3: pendente`).

**Falta:** ensaio (lote 1 ainda por rodar/ler), trocar sondas `__LER__` (cap 8 Comparativo CMV, cap 11 saldo) por valores vistos,
conferir Lucro Líquido 18.336,70 e seletor de unidades (72.000 / 71.000), exportações (DRE Exportar, Exportar Relatório) sem filmar,
fala sem "PDF". Docstring do gerar.py ainda diz 1280x800.

**Comandos:** subir fake: `cd /home/claude/ecoflix && FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54322 bash rec/run.sh fake`.
Conferir `pgrep -f t22_` vazio; lote (segundo plano, 7200000): `cd /home/claude/ecoflix && bash rec/t22/t22_lote.sh`
(lista em `rec/t22/_lote/lista.txt`; repetir = apagar `<id>.fim`). NÃO rodar `--estado` no cap 12 (preservar `apos-cap09`);
o cap 14 com `--estado` cria `apos-cap10`.

## Fim dos 3 lotes (20/11)
Aprovados no rápido: caps 0 a 7, 9, 10 (o 10 com o último passo ajustado), 14 (criou `apos-cap10`). Corrigidos no robô, ainda SEM reensaio: cap 8
(linha "Compras (CMV)" do Comparativo; o fake mostra compras, não CMV por unidade), cap 10 (hover da linha do Alumínio), cap 11 (`Ações de` por prefixo),
cap 12 (semente `inicio` ganhou a categoria "Impostos" na matriz para o cadeado), cap 13 (setup sem navegação extra). Nunca rodaram: 15, 16, 17.
Fila disputada: ~2 h por 1 a 5 capítulos. Rodar: apagar `rec/t22/_lote/rNN.fim`, pôr em `lista.txt` (`15`, `16`, `17`, `11`, `13`, `12`, `08`, `10`) e `bash rec/t22/t22_lote.sh`.
VERSAO do robô agora lê `app/dist/.versao-app`.

## Fechamento dos ensaios (21/11, app 1.60.22)
**Rápido, 0 passo falho:** 8, 10, 11, 12, 13, 15, 16, 17, 18 (0 a 7, 9, 14 já estavam). **Completo (maxLate com voz estimada, só referência):** 8 (0,93), 10 (4,62), 11 (2,05),
12 (2,22), 13 (4,19), 15 (6,21), 16 (17,96: venda leva ~25 s até o Incluir Item, refazer âncoras com a voz real), 17 (0,75), 18 (0,12). Instância 54322 derrubada.
**Correções no robô (gerar.py):** cap8 linha do Comparativo é "(-) CMV" (o app mostra CMV por unidade em competência; o bug era o clique em "Regime de Competência"
por eval, que esperava a aba sumir/voltar: `js_clica_aba` com espera); cap11 parte do apos-cap09 (com o material sem catálogo a janela Corrigir saldo mostra 0 Kg, porque o handler
falso `get_group_material_stock` não trata id canônico = materials.id como a RPC real: PENDÊNCIA de handler, não autorizado aqui), Visão Geral em 25 por página (Papelão é o 13º);
cap15 "Itens por página" 25 no Materiais (a busca derruba a seleção) e ⋯ do Alumínio bloco (Inox cai na página 2); cap16 caixa aberto (`base/caixa-aberto`), Caixa > Nova Venda pelo menu,
setup entra pela página Configurações; cap17 confere em `body` e sem o hover no Cartão (depois do Pix a tela troca os botões pelo QR); cap18 novo (hover no menu do grupo, sem clique).
**DRE do grupo:** handler `get_group_financial_dre_summary.mjs` NÃO mudou: bate com a RPC e o Comparativo chama a RPC por unidade (`_company_ids:[unidade]`). Valores em competência:
CMV matriz R$ 218.873,30 e filial R$ 55.000,00 (soma 273.873,30); Resultado matriz R$ 10.336,70 e filial R$ 8.000,00 (soma 18.336,70).
**Valores para o Kaik conferir na fala:** cap11 saldo 3.900 Kg → 3.870 Kg (Papelão da filial); cap13 latinha compra 6,30 (venda 7,40), filial Tipo %, Abaixo, Valor 5, aviso "15 preço(s) aplicado(s) à unidade".
**Frases da fala sem tela:** cap15 "se alguma não tiver saldo na origem... a tela lista qual falhou e por quê" e "Com o Exigir aprovação desligado, não existe fila"; cap17 "Também dá pra pagar
no cartão ou no boleto" (depois do Pix só aparece o QR); cap11 "aparece um aviso embaixo, com a diferença material por material" (não filmado).

## 21/11 · coordenação depois do lote 5
- Conferido no fonte 1.60.22: "Executar todas" segue nas demais e lista a que falhou com o motivo (`GerencialTransfers.tsx`, `runBatch`); sem aprovação a transferência da matriz executa na mesma transação (`create_group_transfer`, migração 20260908213000); o aviso de divergência cadastro x histórico existe (`GerencialEstoqueVisaoGeral.tsx`) e vira ilustração da coordenação.
- cap17 L7 trocada (voz ainda não gerada): "As formas são cartão, sempre recorrente, Pix ou boleto. Escolho o Pix, e o QR Code do grupo aparece." (o botão do cartão diz "Cobrança recorrente no cartão"); o robô passa por Cartão e Boleto antes do clique no PIX. Ensaio rápido `r17b` no lote.
- Pendente: handler falso `get_group_material_stock` não casa o id canônico = `materials.id` como a RPC real (contornado pela semente apos-cap09 no cap11); cap16 com âncoras a refazer na voz real (venda leva ~25 s até o Incluir Item).
