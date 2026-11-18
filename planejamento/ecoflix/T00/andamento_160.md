# T00 · andamento da aplicação do 1.60.10 (notas para retomar)

Atualizado em 18/11. Quem continuar: leia só este arquivo, o `_BRIEF_APLICAR_160.md` e o cabeçalho do `rec/t00/gerar.py`.

## Feito
- **Fala e roteiro** no 1.60.10: `narracao/tts_textos.py` e `roteiro.md` com 16 capítulos (1.544 → 2.066 palavras). Novos: **8** (o Cato,
  apresentação curta) e **12** (Montar o plano). Renumerados: antigos 8, 9, 10, 11, 12, 13 → 9, 10, 11, 13, 14, 15.
  `plano.md`, `inventario.md` (seção 10) e `cenas/ilustracoes.json` atualizados (uma ilustração nova: `ilu10_selos_status`).
- **Tempos estimados**: `bash planejamento/ecoflix/preparar_aula.sh T00` (rodar de novo se a fala mudar).
- **Robô**: `$TUT_HOME/rec/t00/gerar.py` gera cap00 a cap15 (computador e `.9x16`) e as variantes **cap40** (linha 2 do cap10, conta em
  teste) e **cap41** (linha 3 do cap11, sem o CRM). `--ens` escreve também `rec/t00/_ens/` (ensaio rápido).
- **Sementes** (`rec/t00/t00_catalogo.mjs` → `rec/mundo/seeds-extra/t00/`): `s2` com mensalidade 1.350,00 e `extra_users` 1;
  `teste.json` (nova); catálogo com seção, legenda e material do T1; pagamentos de 1.350,00.
- Nenhum handler novo; nenhum arquivo compartilhado mexido.

## Comandos
```bash
cd /home/claude/ecoflix
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54300 bash rec/run.sh fake        # a instância da T00
node rec/t00/t00_catalogo.mjs                                                  # refaz as sementes
python3 -I rec/t00/gerar.py --ens                                              # todos os capNN.json e os _ens
TUT_SENHA=<8+ caracteres> bash rec/t00/t00_um.sh 12            # ensaio rápido do cap12 (um por chamada, em segundo plano)
TUT_SENHA=<8+ caracteres> bash rec/t00/t00_um.sh 12b           # o mesmo no celular (9:16)
TUT_SENHA=<8+ caracteres> bash rec/t00/t00_um.sh 08 --completo # ensaio completo
FAKE_PORT=54300 bash rec/run.sh down                                           # no fim
```

## Ensaio (estado)
Ver a tabela no fim deste arquivo (atualizada a cada capítulo).

## Pendências conhecidas
- `cenas/tempos/capNN.json` e `cenas/cenas.html` ainda estão na numeração antiga (as cenas serão refeitas no kit v3).
- `T00/rec/` (cópia no git do robô) é do coordenador: copiar de `$TUT_HOME/rec/t00` no fim.
