# T17 · estado da gravação (porta 54342) · fase 2 (G) em 06/11, app 1.38.24 · GRAVAÇÃO FINAL PRONTA (07:05) · MONTAGEM PRONTA (13:52) · falta o `entregar.py` (do coordenador)

## Montagem ("T17: render", 06/11 12:0x; para ANTES do `entregar.py`, que é do coordenador)
- `t17/edit`: `montar_cap.py` = o do T21/T22 (zoom com `rect`, `repouso`, `cauda`), `stage.py` e `overlay.py` = os da skill (antigos em
  `*.antes_fase2`); `finish.py` = o do T21 (apaga stems e trilha depois do mix). `caps/specs.json` (título e área da vinheta como na tela,
  zooms por label, cartões do roteiro), `caps/T17.aula.json`. `auditar_camera.py`: 0 problema nos 12 capítulos.
- `render_todos.sh NN ...` (uma trava por capítulo; espera disco >= 1,3 GiB conferindo de 10 em 10 min; pula capítulo já renderizado) e
  `finish_t17.sh` (espera disco >= 1,2 GiB; stems, music.wav e mix.wav em `/dev/shm/t17_finish` por symlink; finish e legendas sob a trava).
- Câmera: cap05 e cap01 com repouso na volta ao Dashboard pelo ícone (o zoom automático iria ao canto); cap07 com repouso no clique da aba
  Posição de Estoque (passa da borda direita do vídeo, x 2208 a 2618) e zooms manuais no menu Gestão e na aba Inventários; cap09 todo manual
  (o grupo automático ia do menu ao Exportar e perdia o Pendentes na folha de Filtros).
- **Resultado (finish 13:44 a 13:51, conferência até 14:04).** Renders dos 12 capítulos em `t17/edit/out/capNN/` (ficam até a revisão do
  coordenador); folhas de zoom em `t17/edit/out/folhas_zoom/zooms_01..05.jpg`. `t17/edit/out/T17/aula_final.mp4`: 7:00,8 (420,77 s), 107,6 MB,
  1920x1080 30 fps H.264 + AAC 48 kHz estéreo; `video_sem_audio.mp4` fica; `capitulos.json`; `legendas/aula_final.{srt,vtt}` (111 legendas, sem
  travessão). Nome da entrega: "Domiflix T17 - Dashboard, relatórios e exportações".
- Som: mix -15,8 LUFS (TP -3,5); no MP4, I -15,9 LUFS, LRA 3,1 LU, pico -3,6 dBFS; `pico_aac.py --so-medir`: nenhum pico acima de -1 dBTP.
- Folhas de 3 s do vídeo inteiro: `t17/edit/out/T17/folhas3s/folha_01..05.jpg`. Cartões em `t17/edit/out/T17/cartoes/cartoes.jpg`: abertura (2,5 s),
  "Atalho: Shift + D" (25,4 a 29,9 s), "Antes: Integração com WhatsApp" (31,8 a 37,3 s), vinheta do cap01 (42 s), "Fim da trilha" (410,4 a 415,9 s)
  e cartela "Até a próxima aula!" (419 s); a vinheta "Resumo · Recapitulando" (383,8 a 387,0 s) cai entre dois quadros da folha e foi conferida em 385,4 s.
- `/dev/shm/t17_finish` apagado à mão às 14:04 (com o symlink `proj/build/mix.wav`, como no T21).
- Na revisão das folhas, além das sinalizações abaixo: cap05, "Mês passado" mostra 0 OS, 0% e Faturamento R$ 13.950,00 (o dashboard de outubro vem
  sem OS); cap02, o tooltip do Fluxo de Caixa num dia sem movimento mostra R$ 0,00 (dado, de passagem).


**Feito (06/11, 02:45 a 03:45):** `prever.py` (cópia do T21) com as durações do ensaio rápido da fase 1; robô ajustado (`_caps.py`, comentários
"fase 2"); respiros na voz do cap09 e do cap11; ensaio `--rapido` novo de 00 a 07 (0 falho, `unknowns` e `__avisos` vazios).
**03:33, PARADO por disco:** o livre caiu para 1,2 GiB (finish do T22: `t22/edit/out/T22` com `aula_final.mp4`, `video_sem_audio.mp4` e
`proj/audio48k.wav`, ~420 MB às 03:40) e o `rodar.sh` parou antes do ensaio do cap08. Aviso ao coordenador às 03:4x; às 05:42 o livre seguia em
1,2 GiB (espera de 2 h esgotada).
**06:32, retomada** ("T17: continuar" do coordenador; T22 entregue e limpo, 1,7 GiB livres): o container reiniciou às 06:2x (o /dev/shm foi
apagado); a 54342 foi religada às 06:32 (fora da trava); piso de disco do `rodar.sh` baixado para 0,8 GiB (838860 KB), a pedido do coordenador
(a gravação vai para o /dev/shm). O render do T21 roda em paralelo (mesma trava).
**06:33 a 07:05:** ensaio `--rapido` de 08 a 11 (0 falho); prévia de 00 a 11 com o ensaio novo: maior atraso previsto 0,54 s; **gravação final de 00 a
11** (`lote.sh --gravar`, uma trava por capítulo, em /dev/shm e `mv` para `rec/t17/`). O cap05 foi regravado 2 vezes (tomada 1: 1,00 s de atraso;
tomada 2: roteiro antigo, sem remontar o `gerar.py`); vale a tomada 3, das 07:04 (as duas primeiras em `_debug/t17-cap05.g{1,2}.actions.json`).
**Não montar nem renderizar** antes do "T17: render" do coordenador.

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54342` em todo comando; backend e robô com `FAKE_NOW=2026-11-13T16:30:00-03:00`
(`FAKE_NOW=2026-11-13T16:30:00-03:00 FAKE_PORT=54342 rec/run.sh fake`, fora da trava). Navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`, uma trava
por capítulo. Sem pkill; sem commit. Nenhum capítulo grava no banco (todos partem de `t17/inicio`).
- `rec/t17/lote.sh [--gravar] NN ...` (sem `--gravar`: ensaio `--rapido`); resumo em `rec/t17/_debug/{ens,rec}-NN.log`. Versões da fase 1: `*.fase1`;
  ensaios da fase 1 em `_ens/fase1/` e `_debug/fase1/`.
- `rodar.sh` (fase 2, molde do T21): grava em `/dev/shm/t17_rec` e faz `mv` para `rec/t17/` (ou `_ens/`) ao fim de cada capítulo; para se o disco tiver
  < 0,8 GiB (era 1,5 GiB até 06/11 06:3x), se o 8080 não responder 200 ou se a 54342 não estiver com o FAKE_NOW certo (confere antes e de novo dentro
  da trava); religa a 54342 fora da trava se ela caiu.
- `prever.py NN [--tudo] [--ens]`: simula o ritmo com as durações da última gravação (ou do ensaio rápido) e o `at` atual, sem navegador.
- `gerar.py` = `_head.py` + `_caps.py` (`bash rec/t17/montar.sh`; desde 07:0x o `rodar.sh` remonta sozinho antes de gerar o roteiro).

## Gravação final (06/11, `rec/t17/t17-capNN.{mp4,actions.json,telemetry.json,contact.jpg}`)
Todas com 0 passo falho, `unknowns` vazio, `__avisos` = "[]", pageErrors 0, 0 DIFERENTE nas conferências tela x fala, rodapé "Dominex v1.38.24",
folhas de contato sem aviso de erro do app e sem dado real (Glacial Cold Brasil e equipe fictícias).
| cap | vídeo | maior atraso | cap | vídeo | maior atraso |
|---|---|---|---|---|---|
| 00 | 37,18 s | 0,07 (L3) | 06 | 37,02 s | 0,08 (L2) |
| 01 | 33,02 s | 0,03 | 07 | 28,94 s | 0,03 |
| 02 | 41,94 s | 0,20 (FIM) | 08 | 24,14 s | 0,06 |
| 03 | 27,02 s | 0,15 (rosca) | 09 | 28,46 s | 0,34 (Aplicar, cursor) |
| 04 | 29,02 s | 0,03 | 10 | 35,56 s | 0,05 |
| 05 | 29,19 s | 0,55 (cartão Faturamento) | 11 | 31,10 s | 0,00 |
- cap01 foi gravado com a volta ao Dashboard em 30,42 s (fim da fala - 1,1 s); o `_caps.py` tem agora fim - 1,4 s (mais folga) para uma regravação.

## Para a montagem (só com "T17: render"; tempos em s do vídeo do capítulo, conferidos no actions.json da gravação final)
- **Cartões** (como no roteiro): cap00 "Atalho: Shift + D" na L3 (`palavra [2, "Uma"]`, 21,00 s) e **"Antes: Integração com WhatsApp"** na L4
  (`palavra [3, "Se"]`, 27,38 s); cap11 **"Fim da trilha"** na L4 (`palavra [3, "Esse"]`, 23,44 s, já com o respiro) e a cartela final.
- **Respiros:** nenhum corte. Os dois respiros têm tela em ação: cap09 de 8,28 a 10,52 s (Pendentes 8,57, Aplicar 9,40, a folha fecha, Exportar no
  "O Exportar" 10,60); cap11 de 21,92 a 23,44 s (Exportar 22,34, barra "Exportando..." e o aviso de conclusão em ~24,0 s, logo no começo da L4).
- **Acelerações:** nenhuma. Os time-lapses já saíram curtos no robô: cap09 L4 (Movimentações com cursor, menu em 23,72 s; DRE e Estoque abertos
  sem cursor em 25,20 e 26,27 s; o menu do Estoque fica aberto até o fim) e cap11 (NPS sem cursor). Retângulos para o zoom: "menu das Movimentações",
  "menu do DRE", "menu do Estoque" (cap09) e "menu Exportar aberto" (cap11), passos `type` sem clique.
- **Trechos sem gesto novo** (a fala continua; pedem zoom ou destaque, nenhum passa de 9 s): cap00 25,3 a 33,6 s (os cartões discretos caem aí) e
  6,8 a 12,8 s; cap02 25,8 a 32,5 s (resumo do Fluxo de Caixa); cap06 23,4 a 30,1 s (NPS aberto, antes do "a nota"); cap04 5,1 a 10,2 s.
- **cap10:** cauda de 3 s gravada; o aviso "Exportação concluída! O arquivo foi baixado." sobe em ~30,7 s (no "baixa a planilha") e fica até o fim.
- **Sinalizações (app ou mundo, não mudam a fala):** cap05 23,3 a 23,9 s, o menu recolhido abre por hover na volta ao Dashboard e o Faturamento
  aparece cortado durante a contagem ("R$ 1.340,..."), recolhe em ~24,2 s; caps 06 a 10 abrem no Dashboard com o menu aberto e "R$ 2.300,..." cortado
  (como na fase 1); cap04 26,3 a 29,0 s, a janela da OS #15 mostra um "0" solto abaixo do aviso "Esta OS ainda não possui serviços ou materiais
  orçados" (`ServiceOrderViewDialog`); cap07, o "Relatório" do Estoque com compras zeradas (já no roteiro); cap10, "Exportando Materiais das OS... 0
  registros" (`service_materials` vazia de propósito).

## Voz (fase 2): respiros (`t17/narracao/pausas.py` = o da skill; original em `t17/narracao/emendas/capNN.orig.json`)
- **cap09** `pausas.py 09 8.40:2.0`: 2,0 s entre a L1 ("filtro só as pendentes.") e a L2 ("O Exportar leva a lista..."): Status, Pendentes, Aplicar e a
  folha fechando levam ~3,4 s e a fala deixava ~1,8 s (Exportar 1,5 s atrasado na prévia). Narração 24,96 -> 26,96 s; áudio em
  `takes/T17_cap09_p_-d_-_fe_kisel_e_c_-_sse-v__pausas/`. Junção: o take tem ruído de fundo a -57 dB no vão; maior salto entre amostras 0,0008.
- **cap11** `pausas.py 11 22.10:1.2`: 1,2 s entre a L3 ("...e o Exportar meus dados.") e a L4 ("Esse foi o último tutorial..."): o aviso "Exportação
  concluída" cai no respiro. Narração 28,40 -> 29,60 s; áudio em `takes/T17_cap11_Recapitulando_pausas/`. Junção a -85 dB, salto 0,00006.
- Nenhuma fala nova (a 1.38.24 não muda o T17).

## Mudanças no robô na fase 2 (`_caps.py`)
A prévia pelo ensaio rápido da fase 1 dava atraso >= 0,8 s em 01 (FIM 0,90), 02 (L4 1,01), 03 (L3 0,96), 05 (L4 2,80), 06 (FIM 2,68), 07 (1,20),
08 (1,51), 09 (FIM 3,95), 10 (FIM 1,52) e 11 (L4 4,12). Com o ensaio novo: maior atraso previsto 0,32 s em 00 a 07 (cap06) e 0,54 s em 08 a 11 (cap11).
- Âncoras erradas: cap06 aba Relatório e cap07 menu Relatórios usavam a 1ª palavra repetida da linha (`nth=1` agora).
- Rolagens planejadas no lugar das rolagens automáticas do robô (alvo abaixo da dobra): cap06 `rolar 632` antes do gráfico "Volume de OS" e
  `rolar 508` antes do "Feed de Feedbacks"; rolagens que abrem uma linha começam na marca (cap02 L3 e L5, cap03 L3, cap06 L3).
- Hovers mais curtos onde a cadeia não cabia: cap00 (saudação, cartões, fim), cap02 (Fluxo, Saldo, fim), cap03 (rodapé), cap05 (Mês passado,
  calendário, Mostrando), cap06 (KPIs e NPS), cap07 (DRE), cap08 (calendário, resumo), cap10 (aviso).
- cap01: sem o waitFor idle depois do clique em OS Abertas; a volta ao Dashboard 1,1 s antes do fim da fala na gravação (1,4 s no `_caps.py` atual).
- cap05: "Este mês" com `noScroll` (o robô girava a roda 4 vezes: 2,0 s); hover no bloco "OS por Status" no "Os blocos" (tomada 1: o clique em
  Concluída esperou 1,8 s parado); a marca L4 antes da volta ao Dashboard (a L4 começa colada na L3); depois da volta o cursor sai do menu (o menu
  recolhido abre por hover e estreitava os cartões) e `JS_KPIS`.
- cap08: Filtros, Tatiane e Esc em fila com o custo medido; o resumo (horas e saldo) aparece no "O ponto faz parte..." (~19,6 s).
- cap09: respiro (acima); time-lapse da L4 com o menu das Movimentações aberto pelo cursor e os do DRE e do Estoque abertos sem cursor
  (`js_abre_menu`, `pointerdown` do Radix); o retângulo de cada menu vai para o actions.json (`registra`: "menu das Movimentações", "menu do DRE",
  "menu do Estoque"); o menu do Estoque fica aberto até o fim.
- cap10: o cursor do "Configurações" parte 1,4 s antes do clique; `LATENCIA_EXPORT` 0,4 -> 0,25 s por leitura.
- cap11: NPS sem cursor (`js_clica_aba`); idas em fila com o custo medido; respiro (acima) e a marca L4 logo depois do Exportar (`c.flush`).

## Fase 1 (05/11)
Mundo: `semear.py` -> `seeds-extra/t17/inicio.json` + `cadeia.json` (cadeia do T14 + `t14/apos-cap12` + `t17/inicio`). Nenhum capítulo grava no banco: todos partem do mesmo `inicio`, sem `apos-capNN`.
`t17/inicio` (por cima do fim do T14): OS da Academia (#35, "A caminho" desde as 15:00 no T21) concluída 15:05 a 16:10; OS #9, #10 e #11 (abertas "hoje" por datas relativas das sementes antigas) concluídas, para nenhuma OS do dia ficar aberta (P2); lançamentos de 01/10 (R$ 1.900,00 e R$ 1.610,00) em 02/10; ponto da Tatiane: jornada de 11/11 encerrada 18:05 e jornada de 12/11 (08:55 às 17:50); `inventory_counts` e `service_materials` vazias de propósito (sem isso vão para o `/__dev/unknowns`). A OS #8 (pausada, 12/11) fica: é o "Requer Atenção" ("Atrasada 1 dia"). O chamado #15 da Mariana Lopes é o "Chamados abertos".
Handlers novos: nenhum (herdados das aulas de cada área). Backend falso conferido: Relatório e NPS de OS (T5), Financeiro e DRE (T13, T20), Estoque (T8), ponto (T15), "Exportar meus dados" (leituras paginadas de `customers`, `customer_contacts`, `service_orders`, `service_materials`, `financial_transactions`, `financial_accounts`).
Lições:
- Menu lateral recolhido (só ícones) nos caps 0 a 5: com ele aberto o cartão "Faturamento" corta o valor ("R$ 2.300,..."). O item Dashboard vira o ícone `a[href="/dashboard"]` (o menu não é `aside`). Caps 6 a 10 com o menu aberto (as falas usam os grupos Operacional, Financeiro e Gestão).
- "Personalizado" no filtro de período: depois do Esc o botão passa a "Personalizado" e surge um segundo botão "01/10/2026 - 31/10/2026"; para voltar, abrir o "Personalizado" e escolher "Este mês".
- Contas a Pagar/Receber: o "Status" da folha de Filtros é um seletor (Pendentes, Vencidas, Pagas, Todas) e o botão do rodapé vira "Aplicar (1)" (fixo em y 768: `clicar_botao_fixo`).
- Relatório de OS: os cartões montados depois da carga ficam em branco (animação WAAPI com `currentTime < 0`): `JS_KPIS` depois de trocar de aba (lição do T5).
- Resumo do ponto (horas e saldo): só com um funcionário escolhido em "Filtros"; a visão geral só tem calendário e "Horas por dia".
- Exportar meus dados: o backend responde em ms e a barra "Exportando {sheet}... {rows} registros" não aparece; `LATENCIA_EXPORT` (eval no cap10) põe espera de rede nas leituras do arquivo (0,4 s na fase 1, 0,25 s na fase 2; nada é desenhado por fora). O download é aceito sem travar e o aviso "Exportação concluída! O arquivo foi baixado." aparece (toast no canto inferior direito: `noScroll`, seletor `.app-toast-viewport li`). Janela padrão marca quase todos os grupos: o cap11 usa `JS_TRES_GRUPOS` para não ler tabelas sem semente.
Aceite da fase 1 (ensaio `--rapido`, 0 passo falho, `/__dev/unknowns` vazio, `window.__avisos` vazio): `_debug/fase1/ens-NN.log`.
