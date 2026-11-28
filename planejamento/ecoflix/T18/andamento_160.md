# T18 · andamento da aplicação no 1.60.22 (21/11)

**Feito:** `tts_textos.py` (14 caps, 2.311 palavras na legenda, 13.047 caracteres de fala; antes 1.403 palavras), `config_narracao.json` (troca "três vírgula dois"), `roteiro.md` (gerado do tts + docstrings), `plano.md`, `inventario.md` (seção 9), `preparar_aula.sh T18`,
`rec/t18/gerar.py` (14 caps, âncoras ok), sementes `t18/inicio` + `apos-cap03/04/06/07/09/10` (`t18_sementes.py`, `--cadeia`), handlers `sigor-mtr-emit.mjs` e `sigor-cdf-emit.mjs`, PDFs simulados (`t18_pdfs.py`),
`cenas/ilustracoes.json` (10 entradas, `clima` + `v3: pendente`; 2 novas de PDF `tipo: comprovante`, `cena: pdf`: `ilu05_pdf_mtr`, `ilu10_pdf_cdf`).

**Ensaios (2 lotes):** rápido, 0 passo falho e 0 SEM ALVO nos 14 capítulos (4, 5 e 10 reensaiados em modo estrito). PDF devolvido pelo robô nos caps 5 e 10 (`PDF:JVBER...`).
Completo (voz ESTIMADA, só referência) maxLate: 3 (4,59), 4 (9,66), 5 (1,86), 6 (7,34), 8 (0,49), 9 (7,78), 11 (0,51). Refazer âncoras com a voz real.

**Falta:** voz real e novo `gerar.py` com ela; completo dos caps 0 a 2, 7, 10, 12 e 13 (só ilustração/cursor, rápido ok); testar na voz a palavra "ONU" (cap06 L4).

**Comandos:** subir fake: `cd /home/claude/ecoflix && FAKE_NOW=2026-11-10T09:30:00-03:00 FAKE_PORT=54318 bash rec/run.sh fake` (o corpo religa sozinho por capítulo; `FAKE_NOW` em `rec/t18/fake_now.json`: 09:30 até o cap6, 10:40 do 7 ao 13).
Lote (fundo, `TUT_SENHA` aleatória no ambiente): `bash rec/t18/t18_lote.sh 04:s 06:c ...` (r tolerante, s estrito, c completo; quadros em /dev/shm/t18_ens, MP4 e folha em /dev/shm/t18rec; para se o disco < 400 MB). Derrubar: `FAKE_PORT=54318 bash rec/run.sh down` (já derrubada).

**Pedidos / achados:** handler compartilhado `cnpj-lookup` só conhece a Aços Quiririm (lupa só no destinador); `useCdf` tem bug de permissão para admin (fala restrita a "quem não tem"); sem tela para o banner "Revise o campo indicado" e para "procure o suporte" (fora da fala).

## 21/11 · decisão da coordenação sobre os PDFs do órgão
- O PDF do MTR (cap05 L2) e o do CDF (cap10 L0) vêm do órgão ambiental, não do EcoSistema; o do mundo falso (`t18_pdfs.py`) é um papel inventado. **Não mostrar o papel simulado no vídeo** (seria inventar resultado). As cenas `ilu05_pdf_mtr` e `ilu10_pdf_cdf` ficam paradas até o Kaik mandar um MTR e um CDF de exemplo (com dados trocados) para servir de molde; sem isso, no fechamento, trocar a frase para não prometer a tela do PDF (ex.: "Baixar pê-dê-éfe abre o manifesto que o órgão devolveu") e mostrar só o botão.

## 25/11 · PDFs do órgão resolvidos sem papel
- Sem exemplo do MTR/CDF, a fala só cita o botão: cap05 L2 "Baixar pê-dê-éfe. Ele baixa o manifesto que o órgão devolveu, pra ir com o motorista, junto com a carga."; cap10 L0 "...Baixar pê-dê-éfe, pra salvar fora do sistema.". `ilu05_pdf_mtr` e `ilu10_pdf_cdf` tiradas. O robô segue clicando no Baixar (a aba nova não aparece). **T18 pronta para a voz.**

## 28/11 · ilustrações v3
- `cenas_v3/cena.html` (um `CAPS`, clima escuro) com 4 cenas na voz real 1.60.22, tempos de `$TUT_HOME/t18/narracao`: **ilu01_cadeia** (cap 1, linhas 1 a 5: papéis, MTR que vai e CDF que volta, Recicla Vale nos dois papéis, ordem no tempo; funde as antigas `ilu01_cadeia` e `ilu01_ordem`), **ilu09_cargas_outubro** (cap 9), **ilu10_onde_guardar** (cap 10), **ilu12_tres_documentos** (cap 12).
- Saíram: `ilu00_dia` (abertura, a tela basta), `ilu01_ordem` (virou estação da cadeia), `ilu02_licenca` (a mesma ideia de `ilu10_onde_guardar`), `ilu05_pdf_motorista` (o botão Baixar já mostra; a fala não promete o papel).
- `ilu05_pdf_mtr` e `ilu10_pdf_cdf` seguem **tiradas** (decisão de 21/11 e 25/11: o PDF é do órgão, o do robô é papel inventado; sem molde do Kaik não entra papel real).
- Auditoria `--larg 1422`: 4 janelas aprovadas. Piscadas: 0 em 3 cenas; 1 no cap 9 (ilu09, ~19,5 s do capítulo, 1 quadro, 0,5% da tela, provável ponto de luz do último fio; repetiu no re-render). Prévia: `previa_ilustracoes/T18_v3.mp4` + `T18_v3.jpg`. Render: `cenas_v3/render_previa.sh`.
- Fechamento: nenhuma pendência de objeto novo; sem alteração em `perfis/`.

## 28/11 · fechamento
- **Aula final:** `$TUT_HOME/t18/edit/out/T18/aula_final.mp4` (16:15,7, 1080p, 193 MiB, -16,3 LUFS, pico real -3,9 dBTP) + `legendas/aula_final.srt|vtt`; prévia 720p de 26,2 MiB em `$TUT_HOME/entrega_previa/EcoFlix T18 - Ambiental MTR e CDF 1.60.22 (previa 720p).mp4`. Mix de pouca memória (`t18_mix.py`, `t18_music_bed.py`, `finish.py` com as 3 linhas do T03/T15).
- **gerar.py:** `support_widget_last_dismissed` no storage; PDF_FETCH tirado dos caps 5 e 10 (sem papel do órgão); cap 0 sem o hover do grupo (clique direto); `mark` de linha sai junto do clique longo (Avançar/Emitir esperam ~7 s o SIGOR falso), sem isso o maxLate marcava 6 s à toa.
- **Respiros** (`t18_respiros.py`, estado em `rec/t18/_resp/`): cap0 2,2 s; cap3 5,4 s; cap4 20,4 s; cap5 1,1 s; cap6 16,2 s; cap9 26,2 s. Todos em vãos reais entre frases; os de 3 s ou mais viram 2x na edição.
- **Gravação final** (`rec/t18/t18_final.sh`): 14 caps; regravados 0, 6, 9 (rodada 2) e 0, 6 (rodada 3). maxLate final: 0,05 / 0,72 / 0,15 / 0,77 / 4: 6,61 (só as marcas L7 e L11, o app leva 7 s no Avançar; passos na hora) / 5: 1,10 (só a marca L3) / 0,08 / 0,63 / 0,61 / 0,56 / 0,05 / 0,50 / 0,73 / 0,10. 0 passo falho.
- **Câmera:** cap3 com `camera {dwell 0.2, ant 1.0}` (extra.json) e `rect` das 8 teclas de 104,7 a 105,0 s do telemetry corrigido (o app media o campo de busca do IBAMA em y=-10 durante a montagem do popover); cap4 com `--aceitar-camera` (ACEITAR=04): 1 s a 76-88% visível no deslize da câmera depois do Avançar de 7 s.
- **Ilustrações:** 4 encaixadas (ilu01 cadeia, ilu09, ilu10, ilu12), sem `ilu05_pdf_mtr` e `ilu10_pdf_cdf` (decisão de 21/25-11). Piscada de 1 quadro do cap9 (14,4 s da janela, ~19,5 s do cap) NÃO corrigida: repete no re-render, é o ponto de luz do último fio, 0,5% da tela.
- **Conferência:** 11 folhas de 3 s olhadas; varredura de tela parada (1 quadro/s): nenhum trecho de 3 s ou mais em branco; nenhum balão do suporte nem pessoa real; sem travessão nas cenas.
- **Zoom:** 4 manuais + rótulos `(zoom)` do robô (cap3: 4, cap4: 9, cap5: 1, cap6: 4, cap7: 3, cap8: 6, cap9: 6, cap10: 1, cap11: 2, cap12: 1, cap1: 1).
- **Voz:** nenhuma palavra errada; "fraca" do log era o reconhecedor (CNPJ, vírgula, Auto, Ver).
- **Disco:** `proj`, `video_sem_audio` e `out/cap00..13` apagados; instância 54318 derrubada; / com 2,3 GB livres, /dev/shm 6,2 GB.
