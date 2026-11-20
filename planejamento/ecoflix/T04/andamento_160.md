# T04 · andamento da aplicação do 1.60.18 (20/11)

## Feito
- Roteiro, fala (`narracao/tts_textos.py`, 3238 palavras, ~20,8 min), `plano.md`, `inventario.md`, `propostas_fala.md`: 18 capítulos (0 a 17). Novos: 5 (N1 Aços/Lucro Real), 6 (N2 baixada), 9 (N6 etiquetas e filtros), 13 (N5 ajustes), mais o cap 4 refeito (N3/N4). Renumerados: antigos 5 a 13 viram 7, 8, 10, 11, 12, 14, 15, 16, 17.
- Robô `rec/t04/gerar.py` com os 18 capítulos; `t04_pdf.py`; `t04_lote160.sh`; handlers `ext/publica.cnpj.ws`, `rpc/registrar_consulta_cnpj_ie`, `rpc/apply_balance_delta`; `cnpj-lookup` e `cep-lookup` (compartilhado, 12062150) editados; sementes `t04/inicio` regerada.
- `cenas/ilustracoes.json` renumerado (+ extrato e relatório em PDF, `v3: pendente`); `cenas/tempos/*` antigos apagados.
- Ensaio rápido, 3 lotes: passaram 0, 1, 2, 3, 9, 10, 11, 12 (PDF do extrato ainda a refazer), 13 (N5 inteiro), 14, 15, 16 (PDF do relatório capturado). Sementes boas: apos-cap02, apos-cap09 (incompleta, ver abaixo).

## Falta
- **cap04 não fechou** (falha de tempo com a máquina cheia: confere do tooltip e abertura da ficha do Rogério; o "Mostrar todos" foi corrigido). Sem ele não existem `apos-cap04`, `apos-n1` (vazia), `apos-cap05`, `apos-cap06` (vazia): caps 5, 6, 7, 8 e 17 NUNCA rodaram de verdade (cascata) e o cap 12 capturou `apos-cap09` sem a cadeia anterior.
- Cap12: o PDF do extrato veio só com o cabeçalho; o gerar.py agora espera "Preço unit." (não testado).
- Revisar fala x tela dos caps 5, 6, 7, 8, 9 (campos) depois do ensaio; ensaio completo (sem --rapido) dos gestos sensíveis.

## Comandos (instância 54304 precisa estar no ar)
```
cd $TUT_HOME
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54304 bash rec/run.sh fake
bash rec/t04/t04_lote160.sh 4 5 6 7 8 12 16 17     # captura apos-cap04, apos-n1, apos-cap05, apos-cap06, apos-cap09
bash rec/t04/t04_lote160.sh 9 10 11 13 14 15       # refaz com a cadeia certa
python3 -I rec/t04/t04_pdf.py --ens
FAKE_PORT=54304 bash rec/run.sh down
```
Resultado em `rec/t04/_ens/lote160.txt`.
