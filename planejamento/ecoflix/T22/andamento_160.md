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
- cap17 L7 trocada (voz ainda não gerada): "As formas são cartão, sempre recorrente, Pix ou boleto. Escolho o Pix, e o QR Code do grupo aparece." (o botão do cartão diz "Cobrança recorrente no cartão"); o robô passa por Cartão e Boleto antes do clique no PIX. Ensaio rápido `r17b` (21/11 06:21): 0 falho, Cartão, Boleto e PIX achados. Instância 54322 derrubada.
- Pendente: handler falso `get_group_material_stock` não casa o id canônico = `materials.id` como a RPC real (contornado pela semente apos-cap09 no cap11); cap16 com âncoras a refazer na voz real (venda leva ~25 s até o Incluir Item).

## 27/11 · fechamento
- Voz 1.60.22 conferida: palavras "fracas" do proc são número/sigla (DRE, reais e centavos, QR Code), sem troca de palavra. Títulos ok.
- Robô: `vai()` e a troca de usuário do cap15 (location.assign) agora reaplicam `ANIMA_SEMPRE` depois do goto. Gravação final com `rec/t22/t22_final.sh` (fila prio 22, 54322); logs `rec/t22/final.log` (+ `final_r1..r3.log`). Planejadores `t22_plano_pausas.py`, `t22_plano_v2.py`, `t22_plano_v3.py`; `narracao/pausas_fino.py` (cópia da T20).
- Regravações: rodada 1 (02 06 10 11 12 13 14 15 16), rodada 2 (02 10 12 13 14 16), rodada 3 só 02 e 16 (fora do limite de 2, por causa de defeito de robô, não de ritmo): cap02 perdeu o hover do título da janela "Como funciona" (a espera do alvo estável levava 6 s); cap16 a ida ao Caixa saía da marca L2 (respiro antes dela não comprava tempo): agora parte em "matriz." e o respiro 6,2 s vem depois. Respiros finais (original:dur): 06 27.56:1.4; 10 25.49:0.5 26.61:0.6 32.85:1.3 34.85:0.6 41.81:0.8 43.79:2.7 59.0:1.4 68.57:2.0; 11 8.6:0.5 10.32:0.4 34.0:0.4; 12 22.97:0.7 24.97:0.7 48.27:1.1 88.29:0.5 89.41:0.4; 13 7.68:0.7 12.0:0.4 13.0:0.4 19.46:0.3 31.74:0.5; 14 13.12:1.1 16.12:0.4 17.08:1.1 20.76:2.3 38.59:0.3; 15 (ver cap15.json 'pausas'); 16 10.2:6.2 12.28:1.6 14.75:1.5 24.63:0.8.
- maxLate final: tudo < 0,8 exceto cap10 1,38, cap12 1,36, cap14 1,74 (cadeia densa de cliques de formulário, sem passo falho). 0 passo falho, 0 SEM ALVO.
- Números conferidos na tela: Lucro Líquido 18.336,70 (cap08), saldo 3.900 -> 3.870 Kg (cap11, janela Corrigir saldo), latinha compra 6,30 / venda 7,40 (cap13). Todos batem com a fala.
- Edição: `t22/edit/` (montar_t22.sh, fechar_t22.sh, t22_specs.py, t22_mix.py, t22_music_bed.py, specs_ilus.py, render_ilus_v3.sh). 6 ilustrações v3 renderizadas e encaixadas (ilu00_somar, ilu07_caixa, ilu11_divergencia, ilu15_aprovacao, ilu15_lote, ilu17_ciclos); piscadas.py só acusou 1 oscilação de 2 quadros na ilu15_lote (revelação de texto, 0,6% da tela). Acelerações: cap10 47.7-50.2 x2, cap14 23.5-25.5 x2, cap15 3.3-5.0 x2, 9.3-13.1 x4, 31.2-32.9 x2, cap16 10.4-16.2 x4. Zooms pelos rótulos "ZOOM" do robô. Aula final 1152,1 s (19:12), 1080p.
- Varredura de tela parada (1 quadro/s, 1152 quadros): nenhum trecho de 3 s ou mais em branco; os quadros de pouco detalhe são zooms (cadeado do cap12, transição acelerada do cap16).
- Achado do app para o MELHORIAS: no Dashboard Gerencial (cap05/06) as barras de "Receita vs Despesa por Unidade" saem pretas (Receita) em vez da cor da legenda.
