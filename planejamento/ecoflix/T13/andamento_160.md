# T13 · andamento 1.60.18

Feito: roteiro.md e tts_textos.py (20 capítulos, 3.076 palavras), plano.md, inventario.md (seção 13), cenas/ilustracoes.json, preparar_aula,
fake_now.json, gerar.py (20 capítulos), sementes (internet) e 4 handlers novos; ensaio rápido dos 20 capítulos com 0 passo falho
(cap12 e cap17 corrigidos e repassados). Cadeia de sementes apos-cap04/05/07/08/09/11/12/13/15/16 capturada.

Falta: gravação completa com voz (só o Kaik libera a voz); ensaio completo dos capítulos sensíveis (08/09 recorrência, 10, 11, 12, 13, 17).

Comandos (a partir de /home/claude/ecoflix, instância: FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54313 bash rec/run.sh fake):
- rápido: `bash rec/t13/t13_ensaio4.sh NN rapido [--semente]` (cadeia 04,05,07,08,09,11,12,13,15,16 com --semente; 06 e 10 laterais)
- completo (com `at`, depois da voz): `bash rec/t13/t13_ensaio.sh NN completo`
- encerrar: `FAKE_PORT=54313 bash rec/run.sh down`

## 21/11 · ilustrações v3 prontas (para o fechamento)
- 6 cenas escuras em `T13/cenas_v3/cena.html` (cap0, 2, 7, 8, 11, 15) + papel real do comprovante Pix (cap16 L2, `pdf.html`). Tiradas ilu08 e ilu13 (a tela mostra). Auditoria 0, piscadas 0.
- cap18 L0 "O botão Exportar gera um PDF ou uma planilha do Excel.": o robô abre o Exportar e cancela. No fechamento, conferir que o diálogo mostra as opções PDF e Excel enquanto a frase é dita (a fala descreve a escolha, não abre o arquivo); se não mostrar, gravar o PDF e usar o papel real.

## 26/11 · fechamento: gravação final, montagem e prévia (app 1.60.22, 1600x900)
- **Aula**: 19 min 49,6 s (1189,6 s), 1080p, -16,3 LUFS, pico real -3,4 dBTP. Final em `$TUT_HOME/t13/edit/out/T13/aula_final.mp4` (267,5 MiB) com `legendas/aula_final.srt` e `.vtt` (0 travessão); `capitulos.json` e `conferencia.jpg` ao lado. Prévia 720p (28,6 MiB) em `$TUT_HOME/entrega_previa/EcoFlix T13 - Contas a Pagar e Receber 1.60.22 (previa 720p).mp4`.
- **Voz**: `proc_1.60.18.log` e `titulos_1.60.18.log` conferidos; as "fracas" são artefato do reconhecedor ("reais" ouvido como "zero", palavras curtas sem leitura). Nenhuma palavra errada, nenhuma voz gerada.
- **Gravação** (`rec/t13/t13_final.sh`, fila prio 13, quadros em /dev/shm): rodada 0 com os 20 caps, 0 passo falho; 12 caps com maxLate >= 0,8 (04 1,95; 05 1,67; 07 1,05; 08 2,64; 09 1,06; 11 0,83; 12 2,10; 13 1,27; 15 1,45; 17 3,78; 18 1,12; 19 0,91; 06 0,80).
  Rodada 1: 04 05 06 07 08 09 11 12 13 15 17 18 19. Rodada 2: 08 e 09.
- **Como se cortou o atraso**: (1) `t13_retime.py` antecipa os `at` do robô de trás para frente com as durações medidas (até 0,8 a 1,7 s antes da palavra, por cap); (2) `t13_ajusta.py` escolhe respiros em vãos reais de silêncio (áudio < -55 dB entre duas palavras; abre o vão no vad da cópia `emendas/capNN.orig.json`): cap05 12.305:0.7, cap08 34.65:0.7, cap13 22.775:0.83, cap17 50.701:0.7, cap18 7.16:1.0; (3) cap17: tirado o `confere` dos campos De/Até (esperava 3,7 s e dava DIFERENTE falso; a tela mostra 01/11/2026 e 30/11/2026); cap08: tirado o hover "a de dezembro" e hovers mais curtos; cap09: hover mais curto; cap18: o clique em PDF fica preso em "Excel." (o menu com PDF e Excel fica aberto durante a frase).
- **maxLate final por cap**: 00 0,12; 01 0,43; 02 0,10; 03 0,28; 04 0,47; 05 0,51; 06 0,06; 07 0,29; **08 0,85 (só a marca L7; o pior gesto fica em 0,61)**; 09 0,09; 10 0,46; 11 0,34; 12 0,21; 13 0,38; 14 0,71; 15 0,37; 16 0,52; 17 0,57; 18 0,10; 19 0,09.
- **Acelerações**: cap13 [22,85 a 23,6 s, 2x] e cap18 [7,2 a 8,05 s, 2x] (o respiro vira corte de metade na montagem).
- **Papel real**: cap16 `pdf16_comprovante_pix_energia` (o PDF que o robô anexa, 350 dpi) de "Anexar," até "celular" (10,4 a 20,5 s). cap18 L0: na gravação o menu Exportar mostra "PDF" e "Excel" durante a frase (conferido em quadro, 4,5 a 7,4 s), então NÃO se gravou PDF nem se usou papel. Falas de comprovante fora dessa janela (cap16 "E o comprovante daquele Pix da energia?", "O comprovante já está na conta", cap19 recapitulação) ficam sobre a tela do app (a miniatura PDF real aparece no cap16).
- **Ilustrações v3**: 6 cenas + o papel, `--larg 1422 --dsf 1.35`, 0 piscada em todas. Câmera: `auditar_camera` com 0 problema (cap17 pediu um zoom manual no painel de filtros, rect [770,470,2060,1160] em 43,8 a 47,3 s).
- **Disco**: apagados `out/capNN`, `proj` e `video_sem_audio.mp4`; ficam `aula_final.mp4`, legendas, `capitulos.json`, a prévia, `out/ilus/` e as gravações em `rec/t13/`. Livre no fim: ~1,0 GB (outros agentes também gravam).
- Scripts novos: `rec/t13/t13_final.sh`, `t13_plano_pausas.py`, `t13_retime.py`, `t13_ajusta.py`; `t13/edit/t13_specs.py`, `render_ilus_v3.sh`, `fechar_t13.sh`, `montar_t13.sh`, `t13_mix.py`, `t13_music_bed.py`.
