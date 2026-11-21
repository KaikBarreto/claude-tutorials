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
