# T01 · andamento da aplicação do 1.60.18

Atualizado em 20/11. Base: app 1.60.18, tela 1600x900.

## Feito
- Fala (`narracao/tts_textos.py`) e `roteiro.md` reescritos pela cobertura: 16 capítulos (novos: cap10 "O comprovante do seu jeito" e cap11 "Ticket, idioma e guia"; antigos 10-13 viraram 12-15). 2.351 -> 3.348 palavras (~21,5 min de fala). Verificado por script: roteiro e fala com as mesmas linhas.
- `plano.md`, `inventario.md` (seção "Revisão 1.60.18") e `cenas/ilustracoes.json` (2 novas, 4 reancoradas, todas `v3: pendente`).
- Robô `rec/t01/gerar.py` com os 16 capítulos; `python3 -I rec/t01/gerar.py` sem aviso (só um `L10` do cap14 de 0,01 s).
- Sementes: `inicio` (condição À vista padrão, 2º endereço desligado, idioma pt-BR); `apos-cap12` substitui `apos-cap10` (gerada pelo `--seed` do cap12).
- Lote de ensaio lançado (rápido de 00 a 15, depois completos de 03 04 09 10 11 12 13 14).

## Como conferir o lote
- Log: `/dev/shm/t01_lote.log` (linhas `RES capNN`, `RAPIDOS FIM`, `CADEIA FIM`, `LOTE FIM`).
- Por capítulo: `rec/t01/_ens/capNN.resumo.txt`, `.prever.txt`, `.log`; folhas de contato em `/dev/shm/t01_rec/_ens/*.contact.jpg`.
- Instância do mundo falso: porta 54301 (`FAKE_NOW=2026-11-10T08:30:00-03:00`).

## Derrubar a instância (no fim)
```
cd /home/claude/ecoflix && FAKE_PORT=54301 bash rec/run.sh down
```
Depois apagar MP4/jpg de ensaio: `/dev/shm/t01_rec` (disco apertado).

## Falta
- Olhar o resultado do lote e corrigir o que falhou (máx. 3 lotes).
- Voz ElevenLabs e gravação final (com `preparar_aula.sh T01` depois da voz).
- Decisões do Kaik: À vista como única condição na partida (o app real semeia 6); selo "MASTER"; senha do ambiente com 5 requisitos.
