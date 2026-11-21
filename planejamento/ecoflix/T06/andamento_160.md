# T06 · andamento da aplicação no app 1.60.18 (20/11/2026)

## Feito
- `roteiro.md` e `narracao/tts_textos.py` refeitos: 16 capítulos (0 a 15), 3.253 palavras (era 2.044). Novos: **6** Cofre zerado ou negativo
  (handoff 19/11), **11** Despesa e receita do dia, **12** Sangria no fim do dia; trecho **13a** (trava do Fechar Caixa). Renumerados: antigos 6-9 →
  7-10, 10 → 13, 11 → 14, 12 → 15. Trechos novos em 2 (data retroativa), 3 (editar saldo de abertura), 5 (link do tutorial), 8 (painel, resumo),
  9 (permissões), 10 (cofre e data retroativa no saque), 13 (cartões, projeção, diferença 950,00, 957,10), 14 (corrigir sem reabrir).
- `rec/t06/gerar.py` (todos os capítulos, mais 09b e 13a), `t06_sementes.py` (sementes novas: `cofre-negativo`, `apos-cap10`, `apos-cap11`, `apos-cap12`,
  `apos-cap13`, `apos-cap14`, `dia-10-rascunho`), `t06_cap.sh`, `t06_lote160.sh`. `plano.md`, `inventario.md`, `cenas/ilustracoes.json` atualizados.
- Sem handler novo (usa os do mundo base: `get_financial_description_suggestions`, `get_cash_register_other_order_ids`, `get_dinheiro_balance`).

## Ensaio rápido (3 lotes feitos, 20/11)
- Fecharam sem falha: 00, 01, 02, 04 a 07, 08, 09, 09b, 10, 11, 12, 13, 13a, 14, 15 (lote 3: 08, 10, 11, 12, 13a).
- **Não reverificado**: cap03 (menu "Editar saldo de abertura" falhou no lote 3; conserto já no gerar.py, espera por laço de 10 s no `[role=menuitem]`).
  Comando: `cd /home/claude/ecoflix && TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+> bash rec/t06/t06_lote160.sh 03`
- Correções do lote 3: cap10 (esperar `#fee` antes do foco), cap11 (contas "Aluguel de caçamba" movidas para a semente `apos-cap10`), cap12 (ids `#sangria-amount`/`#sangria-description`), `ensaio/resumo/prever.py` com sufixo `a`.
- Só rápido (sem ensaio completo com voz): todos. Folhas de contato em `rec/t06/_ens/*.contact.jpg` (nenhuma vista; apagar à mão depois).
- Sem a voz: números de dinheiro confirmados pelos `confere` do rápido (3.006,50; 1.450,00; 957,10 etc.); repetir no ensaio completo.

## Comandos
- Rodar um capítulo: `cd /home/claude/ecoflix && TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres> bash rec/t06/t06_cap.sh NN --so-rapido`
  (NN = 00..15, 09b, 13a). Regerar: `python3 -I rec/t06/gerar.py [NN]`; sementes: `python3 -I rec/t06/t06_sementes.py todas`.
- Depois da voz: `bash planejamento/ecoflix/preparar_aula.sh T06` não toca o capNN.json da voz; rodar o `gerar.py` de novo.
- Pendências para o Kaik: cena de PDF "Ver comprovante" (não incluída); texto do modal para quem não tem permissão só é falado (sem usuário sem permissão no mundo).

## 21/11 · fechamento (gravação final 1.60.22, montagem e prévia)
- Aula final: `$TUT_HOME/t06/edit/out/T06/aula_final.mp4` (20 min 06 s, 1080p) + legendas; prévia 720p em `$TUT_HOME/entrega_previa/`.
- Gravação: `rec/t06/t06_final.sh` (fila prio 06, instância 54306 religada no `FAKE_NOW` do capítulo; **quadros em `/dev/shm/t06_rec`**: o cap13, de
  163 s, gera ~1 GB de JPEG e encheu o disco na 1ª passada). Regravados: 03, 08, 10, 11 e 13a (âncoras adiantadas: a voz real é mais rápida),
  13 (disco cheio; depois app 1.60.22).
- **App 1.60.22 no Fechar Caixa**: "Projeção de Lucro" virou lista (material, "Comprado: R$", lucro); a tabela Comprado (kg)/Valor Compra/
  Vendido (kg)/Valor Venda está no acordeão "Relatório de Pedidos do Caixa". O robô abre os dois (a fala L10 do cap13 diz "Abrindo a Projeção de
  Lucro, você confere o dia material por material: quanto comprou e quanto vendeu de cada um."). A diferença aparece como "R$ -7,10".
- Respiro (`pausas.py`): cap11 72.85:1.0 (antes de "Aqui, o aluguel de uma caçamba"). Sem `acelera`.
- cap09 + cap09b: mesma voz, `voz_ate`/`voz_de` no specs (30,18 s). cap13: corte 13a encaixado por `t06/edit/t06_juntar_cap13.py` (originais em
  `rec/t06/t06-cap13o.*`; **apague os `cap13o.*` antes de rodar de novo depois de regravar o cap13**).
- Edição: `t06_specs.py` (zooms dos rótulos "ZOOM", `min_w` 1600; extras em `caps/extra.json`: destaques nos caps 01, 05, 09, 14, 15 e câmera
  do cap11), `specs_ilus.py`, `render_ilus_v3.sh` (5 ilustrações, 0 piscadas; retoma trechos prontos), `fechar_t06.sh`, `montar_t06.sh`
  (`MIX_PY=t06_mix.py`, cópias de pouca memória da T03). Disco: `out/T06` montado em `/dev/shm/t06_T06` e movido no fim; caps 04, 10 e 13 em `/dev/shm/t06_caps`.
- Comprovante/PDF: nenhuma cena. As falas citam papel só de passagem: cap11 "Em Mais detalhes dá pra escrever uma observação e anexar o
  comprovante." (anexo, não PDF do app) e cap13 "o sistema oferece imprimir o relatório do fechamento. Desta vez, não, obrigado. O relatório fica
  guardado no Histórico do Caixa, pra imprimir quando quiser." (o robô recusa a impressão: não há PDF na gravação).
- Achados do app para o MELHORIAS: "Efeitos desta transação" do saque mostra "Diminuirá em R$ 3006,50" (sem ponto de milhar; a linha de baixo
  mostra "R$ 3.000,00"); a Nova Receita por Pix avisa "Depósito realizado com sucesso!".

## 21/11 · coordenação depois do fechamento
- cap13 L10 (voz) fala que a Projeção de Lucro mostra comprado e vendido; no 1.60.22 essa tabela é do Relatório de Pedidos do Caixa. Frase nova gerada (nó `T06 cap13 frase Projeção (1.60.22)`, 146 créditos): "A Projeção de Lucro mostra o dia material por material. E no Relatório de Pedidos do Caixa você confere quanto comprou e quanto vendeu de cada um." Quando o Kaik mandar o MP3: `emendar.py` (troca no cap13, `empurra` se não couber), `proc.py 13=...`, robô com o clique no Relatório na palavra "Relatório", regravar só o cap13 e remendar a aula (`remendar_aula.py`).
