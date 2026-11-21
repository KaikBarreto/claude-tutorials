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
