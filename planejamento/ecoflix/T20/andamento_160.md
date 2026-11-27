# T20 · andamento da aplicação do 1.60.18 (20/11, fechamento)

**Feito:** roteiro e fala (16 caps), sementes, handlers, `gerar.py`, `ilustracoes.json` (cap13: texto real do wa.me, pedido #1761 de 10/11, R$ 18.714,08).
**Ensaio rápido aprovado:** 0, 1, 2, 5, 6, 7, 8 (saldo novo no portal), 9 (relatório sai como HTML, não PDF), 11, 12 (PDF A4 capturado: #1749, Papelão..Ferro misto, Saldo R$ 3.700,00, "Escaneie para ver fotos"), 13 (wa.me lido), 14.
**Causas achadas:** (1) `portal-order-receipt` dava 500 ("semValor antes de inicializar"): corrigido, era o "SEM PDF" do cap12. (2) Saldo "antigo" do cap08 = cache de 30 s do React Query do portal no ensaio rápido (a volta ao portal acontece em <30 s): o robô agora recarrega a página ao voltar. (3) Cap04 linha 9: o robô agora liga a chave a desligada de verdade (o botão vira "Remover login", sem clicar); a fala não mudou. (4) Cap10: o desktop navega a janela ao blob (headless baixa o PDF): gancho `BLOB_HOOK` + `PDF_BLOB_JS`. (5) Cliques em "Editar" do cadastro passaram a ser por eval (menu da linha, aberto por hover, intercepta o ponteiro e o clique esperava 60 s).
**NÃO fechou (limite de 2 lotes):** caps 3, 4 e 10 corrigidos DEPOIS do lote 2 e não reensaiados.
**Comando** (em `$TUT_HOME`, `TUT_SENHA` e `PORTAL_SENHA` no ambiente, 8+ caracteres; regravar antes `python3 -I rec/t20/t20_sementes.py`): `bash rec/t20/t20_fila.sh --rapido 3 4 10`
**Disco:** `/` a 98% (ENOSPC derrubou o gravador do T12 cap09 às 21:51).
**Instância 54320 derrubada:** `FAKE_PORT=54320 bash rec/run.sh down`.

## 25/11 · ilustrações v3 com a voz real 1.60.22
- Feitas 6 (`cenas_v3/cena.html`): ilu01_portal, ilu03_duplo, ilu10_precos_pdf (papel A4 real da tabela), ilu12_comprovante_pdf (papel real do #1749), ilu13_balao_zap (texto real do wa.me), ilu10_links. Tiradas 7 (a tela mostra). Auditoria 0, piscadas 0. Prévia `$TUT_HOME/previa_ilustracoes/T20_v3.mp4`. Papéis em `$TUT_HOME/t20/edit/out/comprovantes/`.
- **Para o fechamento**: `ilu09_relatorio_pdf` pendente: o "Baixar pê-dê-éfe" do Relatório do portal abre HTML em aba nova (sem PDF no actions). Fazer como a T04 no cap12 (gancho que captura o HTML escrito na aba e cena `cenas_v3/pdf12.html` da T04 como molde). O PDF da tabela de preços é a tabela geral (sem os blocos "Seus materiais"/"Outros materiais", que são da aba na tela): a fala do cap10 cita os blocos na tela, então está certa.

## 27/11 · fechamento
- Caps 3 e 4 ensaiados (rapido) OK. Cap10 pendente: o ensaio falhou no setup do portal (sementes regravadas com outra senha por um t20_final.sh abortado). Cap09 agora captura o HTML da aba (POPS_HTML/HTML_B64_JS no gerar.py, ainda sem teste).
- Preparados: rec/t20/t20_prep.sh, t20_final.sh, t20_papel.py, t20_montagem_cap15.py; t20/edit/ copiado da T15. Retomar: `bash rec/t20/t20_prep.sh 9 10`.
- Ensaio rapido caps 3, 4, 9, 10 OK (0 falho, 0 DIFERENTE, 0 SEM ALVO). Captura do HTML do relatorio (cap09) e t20_papel.py funcionam (A4 paisagem, total R$ 18.755,00). Proximo: `bash rec/t20/t20_final.sh 00..14` (log rec/t20/final.log).
- Gravacao final rodada 1 (rec/t20/final.log): ok so 01, 12, 13. Atrasados (maxLate): 00 2.65, 02 1.18, 04 4.40, 06 2.27, 07 0.94, 08 3.63, 09 1.69, 11 7.40, 14 4.21. 03 falhou no passo "Buscar cliente...". 05 e 10 nao gravaram ("at" negativo no passo 1; corrigido no gerar.py, que agora corta em 0). Proximo: respiros por pausas.py e regravar.
- Respiros (pausas.py, vãos reais do vad) aplicados em 00, 02, 04, 07, 08, 09, 11, 14 (planejador rec/t20/t20_plano_pausas.py); cap06: hover do gráfico 1,4 -> 0,5 s no robô. Rodada 2 (03 05 10 00 02 04 06 07 08 09 11 14) lançada em rec/t20/final.log (rodada 1 em final_r1.log). Cena `relatorio` (ilu09) escrita em cenas_v3/cena.html, papel real em t20/edit/out/comprovantes/cap09-relatorio.png (renderizar só com a voz final).
- Rodada 2 (final_r2.log): ok 01, 07 (0.52), 12, 13; resto entre 1,2 e 7,4 s de atraso. Rodada 3 (última) lançada: 03 05 10 00 02 04 06 08 09 11 14 com respiros novos (planejador agora soma aos já aplicados) e cap06 com gestos mais cedo. Voz final = a de cap NN.json atual (com pausas).
- Rodada 3 (final_r3.log) fechada: maxLate 00 1.53, 02 1.09, 03 1.16, 04 3.26, 06 1.06, 08 1.78, 09 1.60, 10 3.19, 11 6.27, 14 3.34; ok 01 07 12 13. Cap05 tinha ancora errada (senha, 1a ocorrencia no lugar da 2a): corrigido no gerar.py, regravando so ele. 7 ilustracoes v3 renderizadas com a voz final (inclui ilu09_relatorio_pdf).
- Gravacao final fechada (cap05 regravado: 2.22 s de atraso max). Montagem do cap15 (recap) feita, specs.json/chapters gerados (t20_specs.py, specs_ilus.py, montar_cap.py, auditar_camera: 3 avisos de camera, ver conferencia). Render dos capitulos + finish + legendas em andamento: `t20/edit/montar_t20.sh` (log out/montar.log); proj em /dev/shm/t20_proj.
- ENTREGUE 27/11: aula_final 1080p (17:45, -16,4 LUFS, pico -3,7 dBTP) em t20/edit/out/T20/ + legendas; previa 720p 28,5 MB em entrega_previa/. Titulo do cap13 trocado para "WhatsApp" na tela. Atrasos de gesto residuais (maxLate): 00 1.53, 02 1.09, 03 1.16, 04 3.26, 05 2.22, 06 1.06, 08 1.78, 09 1.60, 10 3.19, 11 6.27, 14 3.34 (a corrigir em nova rodada; 01 07 12 13 ok). Camera aceita em 04 e 14 (alvo dentro do quadro).

## 27/11 · remendo de atraso

Meta: gestos com maxLate < 0.8 s (só `mark`/`eval` invisível até 1,2 s), até 2 rodadas por capítulo, sem gerar voz nova.

- Robô (`rec/t20/gerar.py`): `noScroll` nos alvos do cabeçalho (cap11 sino, "Nova solicitação", "Voltar ao portal"; cap14 foto), pois o `ensureVisible` rolava ~6 s. Cadeias de preparação (reload, troca, goto) ancoradas na palavra anterior, não em `L(n)`. Helper novo `Cap.foco()` (foco por JS no lugar do clique no campo de senha) em cap04 e cap05; `digita` aceita `cps`. Âncoras ajustadas em cap00, 04, 05, 06, 09, 10, 11, 14.
- Pausas: feitas com `t20/narracao/pausas_fino.py` (variante de `pausas.py` que divide o segmento do VAD no ponto; a `pausas.py` recusa inserir dentro de fala). Sempre a partir do original `emendas/capNN.orig.json`. Janelas de ilustração (`out/ilus/janelas.json`) reajustadas só em `at`.
- Aceleração: `acelera` em `caps/extra.json` nos trechos mudos de preenchimento/navegação.
- maxLate de gesto, antes -> depois: cap11 6.27 -> 0.67; cap14 3.34 -> 0.51; cap04 3.26 -> 1.15 (rodada 1; nav pós-ajuste não refeita); cap10 3.19 -> 1.34; cap05 2.22 -> 1.05; cap00 1.53 -> 0.68; cap02 1.09 -> 0.47; cap03 1.16 -> 0.64; cap06 1.06 -> 0.52; cap09 1.60 -> 0.69; cap08 1.78 (não refeito).
- Desvios: cap10 teve 3 rodadas (a simulação da rodada B errou por causa de `wait`/`pause` contados como 0,3 s; a gravação da rodada A foi sobrescrita). cap05 fica em 1,05 s: digitar 14-17 caracteres custa ~1 s (CDP) e não há vão de voz para pausa. cap08 sem vão usável.
- Voz (cap07, cap12), reconhecedor só no trecho: ouviu "um comprovante" nos dois. cap07 (54,0-59,6 s): "A venda de hoje saiu com um comprovante sem valores." cap12 (18,6-23,6 s): "Num pedido com um comprovante sem valores, o papel sai sem." Ou seja, o "o" virou "um" de fato; não regerado.
- Remontado: finish (MIX_PY=t20_mix.py), legendas, capitulos.json, entregar.py --unico. Aula final 1057,5 s (17:37,5), 1080p; prévia 720p 26,5 MiB.
