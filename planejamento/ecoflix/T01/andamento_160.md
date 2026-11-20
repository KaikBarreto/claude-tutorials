# T01 · andamento da aplicação do 1.60.18

Atualizado em 20/11. Base: app 1.60.18, tela 1600x900.

## Feito
- Fala (`narracao/tts_textos.py`) e `roteiro.md` reescritos pela cobertura: 16 capítulos (novos: cap10 "O comprovante do seu jeito" e cap11 "Ticket, idioma e guia"; antigos 10-13 viraram 12-15). 2.351 -> 3.348 palavras (~21,5 min de fala). Verificado por script: roteiro e fala com as mesmas linhas.
- `plano.md`, `inventario.md` (seção "Revisão 1.60.18") e `cenas/ilustracoes.json` (2 novas, 4 reancoradas, todas `v3: pendente`).
- Robô `rec/t01/gerar.py` com os 16 capítulos; `python3 -I rec/t01/gerar.py` sem aviso (só um `L10` do cap14 de 0,01 s).
- Sementes: `inicio` (condição À vista padrão, 2º endereço desligado, idioma pt-BR); `apos-cap12` substitui `apos-cap10` (gerada pelo `--seed` do cap12).
- Lote de ensaio lançado (rápido de 00 a 15, depois completos de 03 04 09 10 11 12 13 14).

## Estado do ensaio (20/11 18:50)
- O app de gravação virou **1.60.22** durante o trabalho; o robô fixava 1.60.18 e o aviso "Sistema atualizado" cobria as abas. `VERSAO = '1.60.22'` em `rec/t01/gerar.py` (corrigido).
- Lote 1 (abortado, versão errada) e lote 2 (ordem 09-15, 05, 06, 08, 00...; parou no prazo de 2 h).
- Rápido OK com o 1.60.22 (0 passo falho): caps 05, 06, 08, 09, 10, 11, 12, 13, 14, 15. Folhas vistas: 10 e 12 (corretas).
- Rápido com o 1.60.22 ainda por fazer: 00, 01, 02, 03, 04, 07 (passaram no lote 1 com o aviso de versão na tela; conteúdo não mudou, mas refazer para a folha limpa).
- **Lote 3 (último) rodando em segundo plano**: rápido de 00 01 02 03 04 07 e depois completos de 14 10 03 12 09 11 13 04. Log: `/dev/shm/t01_lote_c.log`. Termina no prazo de 2 h (~20:50) ou antes; a fila está cheia (cada capítulo leva 7 a 20 min).
- Atraso a corrigir: cap14 (rápido, `prever`): acumula 1-2 s de atraso em L4 a L10. Já encurtei o `Aceito em` (2,4 -> 1,0 s) e adiantei o clique em Ver Contrato; o completo do cap14 no lote 3 confere. Se ainda passar de 1 s, encurtar os hovers da lista do Zerar Sistema (L8) e o `Serão mantidos` (L10).
- cap10: o `confere_ausente` olhava "Quem assina" e achava a descrição ("Escolha quem assinar"); passou a olhar "Só o cliente/fornecedor". Conferir no rápido do cap10 (não foi refeito).
- Bolha do assistente ("Qual número de operação você quer entender agora? Abrir Cato") aparece embaixo à direita nas folhas dos caps 10 e 12; é do app, não do robô; avisar a edição (esconder no corte).

## Como conferir o lote
- Log: `/dev/shm/t01_lote_c.log` (linhas `RES capNN`, `CADEIA FIM`, `LOTE FIM`); o lote 2 está em `/dev/shm/t01_lote.log`.
- Por capítulo: `rec/t01/_ens/capNN.resumo.txt`, `.prever.txt`, `.log`; completos em `rec/t01/capNN.resumo.txt`; folhas em `/dev/shm/t01_rec/_ens/*.contact.jpg`.
- Instância do mundo falso: porta 54301 (`FAKE_NOW=2026-11-10T08:30:00-03:00`).

## Derrubar (quando o lote acabar, ou para abortar)
```
cd /home/claude/ecoflix && pgrep -af t01_lote_160_c   # pega o pid do bash e mate com kill <pid>
FAKE_PORT=54301 bash rec/run.sh down
```
Depois apagar MP4/jpg de ensaio: `/dev/shm/t01_rec` (disco apertado).

## Falta
- Resultado do lote 3 e correção do que falhar (sem lote 4: o limite de 3 foi usado).
- Voz ElevenLabs e gravação final (rodar `preparar_aula.sh T01` depois da voz).
- Decisões do Kaik: À vista como única condição na partida (o app real semeia 6); selo "MASTER"; senha do ambiente com 5 requisitos.
