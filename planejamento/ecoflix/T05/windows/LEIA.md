# T05 · cenas de Windows (EcoTray)

Oito momentos, uma cena JSON cada, com os gestos presos às palavras da fala (tempos de `$TUT_HOME/t05/narracao/capNN.json`).
`t0` é o instante do capítulo em que a cena começa (está no `_leia` de cada JSON); `at` é segundos da cena.

| # | Cena | Capítulo | t0 (s) | Duração (s) | Conteúdo |
|---|---|---|---|---|---|
| 1 | `cap02_1_download.json` | 2 | 7,5 | 18,6 | download, aviso "pode ser perigoso", setinha, "Manter" |
| 2 | `cap02_2_smartscreen.json` | 2 | 26,0 | 11,3 | "Abrir arquivo", SmartScreen, "Mais informações", "Executar assim mesmo" |
| 3 | `cap02_3_instalador.json` | 2 | 37,3 | 35,4 | instalador de "Pronto para instalar" a "✓  Instalado com sucesso!", atalho, bandeja, Fechar, painel, tracinho |
| 4 | `cap04_4_impressao.json` | 4 | 15,0 | 26,0 | painel pela bandeja, "✓  Impresso em POS-58" (08:41:07), tracinho |
| 5 | `cap06_5_destrava.json` | 6 | 27,7 | 8,3 | painel aguardando e libera a balança (08:44:10) |
| 6 | `cap06_6_configurar.json` | 6 | 36,0 | 30,5 | "Configurar Balanças", "Nova balança", OK, Gravar |
| 7 | `cap09_7_sair.json` | 9 | 0,0 | 7,2 | botão direito na bandeja, menu, "Sair" |
| 8 | `cap09_8_atalho.json` | 9 | 41,0 | 6,9 | clique duplo no atalho "EcoTray" |

## Render
Pasta de trabalho `$TUT_HOME/t05/windows/` com `app/icon.png` (`ecotray/assets/icon.png` do app), `app/feature-integracao.png`
(`src/assets/features/`) e as cenas copiadas. Tudo pesado entra na fila justa, uma cena por vez:
```bash
export TUT_HOME=/home/claude/ecoflix CENA_WIN_CACHE=/dev/shm/cena-windows; S=$PWD   # raiz da skill
W=$TUT_HOME/t05/windows; cp planejamento/ecoflix/T05/windows/cap*.json $W/
# capturas (já feitas; refaz só se o plano mudar)
bash $TUT_HOME/rec/fila.sh --prio 05 -- python3 ferramentas/windows/capturar_ecotray.py planejamento/ecoflix/T05/windows/capturas.json $W/capturas --app $TUT_HOME/app-src-1.59.154/ecotray
# cada cena: sai <nome>.mp4 2560x1600 + .telemetry.json + .actions.json no formato do robô
for n in cap02_1_download cap02_2_smartscreen cap02_3_instalador cap04_4_impressao cap06_5_destrava cap06_6_configurar cap09_7_sair cap09_8_atalho; do
  (cd $W && bash $TUT_HOME/rec/fila.sh --prio 05 -- node $S/ferramentas/windows/cena_windows.cjs $n.json $TUT_HOME/rec/t05/t05-$n.mp4); done
```
Conferência: `node ferramentas/windows/cena_windows.cjs <cena>.json stills --stills 1,5,9 --mira` (sob `.stills.lock`, `nice -n 19`).

## O que falta trocar
- **Página do navegador**: hoje é a imagem `app/feature-integracao.png` (tela Integrações do app, que traz "v1.2.5" de marketing).
  Quando existir a gravação `device: windows` do robô da T05, troque `navegador.pagina` de cada cena por
  `{"gravacao": {"video": ..., "telemetria": ..., "acoes": ..., "de": 0.0, "inicio": <s do capítulo = t0>, "ate": <t0 + duração>}}`.
  Com a gravação, o cursor dentro da página é o do robô.
- Cenas 4 e 5: o clique na bandeja cai no início da cena (cap04 em 15,5 s; cap06 em 28,4 s). O robô deve deixar o cursor parado na página nesse trecho.
- Cenas 3 e 8: o navegador é minimizado (clique em "–" dele) para a área de trabalho aparecer; na 8 volta pela barra de tarefas.

## Observações
- Painel, instalador e menu vêm do código do app. Ao liberar a balança (cena 5) o código marca de novo a impressora: a Atividade Recente
  ganha "08:44:10  Impressora padrão: POS-58" abaixo da linha do módulo (comportamento real; o roteiro cita só a do módulo).
- Cada captura do painel mostra "2 cliente(s)" com o navegador conectado e "1 cliente(s)" logo após instalar (handoff H2).
- Horas: relógio da barra 08:33 (cenas 1 a 3), 08:41:07 no instante do aviso (4), 08:44 (5 e 6), 08:58 (7 e 8).
- Sugestão de fala (não alterada): nenhuma mudança necessária.

## Prévia (feita em 10/11)
`/home/claude/ecoflix/previa_ilustracoes/T05_windows.mp4` (58 s, 1280x800, sem áudio) e `T05_windows.jpg` (folha): trechos das 8 cenas,
renderizadas em 1280x800 (`"saida": [1280, 800]` numa cópia da cena) com `--mira` no lugar do cursor da skill (sem anel de clique).
Quadros de conferência (`--stills --mira`) das 8 cenas olhados: textos do Windows e do EcoTray iguais ao código e ao inventário.
Render final: o comando acima (2560x1600 + telemetria), sem `--mira`, depois `specs.json` → `montar_cap.py` → `render_chapter.py`.
