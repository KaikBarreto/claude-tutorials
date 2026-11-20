# T02 · andamento da aplicação no 1.60.18 (20/11)

**Feito:** `roteiro.md` e `narracao/tts_textos.py` (14 capítulos, 1.483 → 2.313 palavras; troca de pronúncia nova "SPED" em
`config_narracao.json`); `plano.md`, `inventario.md` (seção 8) e `cenas/ilustracoes.json` (renumerado, `v3: pendente`, entradas novas
cap 6, 7 e 12 com `tipo comprovante` no 12); `preparar_aula.sh T02` rodado; robô `rec/t02/gerar.py` (14 capítulos);
sementes `rec/mundo/seeds-extra/t02/` (`t02_sementes.py`); handlers novos `create-company-user` (editado, só T02),
`rpc/set_user_scale_weight_policy.mjs` e `rpc/save_user_permissions_and_bank_accounts.mjs`.
**Mapa de capítulos:** 0 a 5 como antes (1, 2, 3, 4, 5 editados); 6 Restrições e 7 Mapa (novos); 8 a 11 = antigos 6 a 9; 12 Relatório
(novo); 13 = antigo 10 (recap).
**Falhas da varredura (caps 3, 4, 5):** `Operador Padrão` ganhou o selo "Recomendado" (nome acessível "Operador Padrão Recomendado": alvo sem
`exact`, `CHIP_OP`); sem perfil a lista fica apagada (cap 4 clica em "Personalizado" antes); o "Personalizado" virou botão âmbar
(`button.bg-amber-500`, não mais `span`).

## Comandos
```bash
cd /home/claude/ecoflix
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54302 bash rec/run.sh fake          # a instância (se caiu)
export TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres>
python3 -I rec/t02/gerar.py                                                       # reescreve rec/t02/cap00..13.json
bash rec/t02/t02_lote.sh 03 04 05      # ensaio rápido em lote pela fila (--prio 02); resultado em /dev/shm/t02rec/lote.txt
bash rec/t02/t02_rodar.sh 05           # completo de um capítulo (sem --ens)
FAKE_PORT=54302 bash rec/run.sh down   # no fim
```
## Falta / pendências
Ver o fim deste arquivo (preenchido ao fim do ensaio).

## Estado ao fim (20/11)
- Ensaio rápido: 14 de 14 capítulos sem passo falho (cap12 e cap13 corrigidos no 2º lote). Completos: 04 (atraso 1,0 s só em "liga Pedidos",
  o conjunto de cliques do escritório é mais longo que a frase; refazer com a voz de verdade, se persistir folgar a fala), 05 e 07 aprovados.
- Não gravados completos: 01, 02, 03 (digitação/foto, gestos já com folga no rápido) e 06, 08 a 13 ficam só no rápido.
- Instância 54302 derrubada. Para voltar: ver comandos acima. `cenas/cenas.html` e `cenas/tempos/` seguem com os ids/caps antigos (estilo v3 pendente).
- O relatório do cap12 (HTML da aba nova) sai no retorno da ação "relatório HTML" em `rec/t02/_ens/t02-cap12.actions.json` / gravação.

## Fechamento (20/11, noite) · voz real, gravação final e montagem
- Voz real processada (`proc_1.60.18.log`: 14 capítulos, semelhança 0,95 a 1,00; as 11 "fracas" eram artefato, trechos reouvidos a 0,8x). A voz saiu ~16% mais
  rápida que a estimada no cap04 (120 s → 101 s).
- Gravação final: `rec/t02/t02_final.sh NN ...` (fila `--prio 02`, instância 54302, `FAKE_NOW` único). Em lotes de até ~7 capítulos: com a fila cheia cada
  capítulo leva 10 a 15 min e o lote de 14 passou do prazo de 2 h do segundo plano.
- **Aviso "Sistema atualizado · v1.60.22"**: o build servido passou a ser o 1.60.22 e o `VERSAO` do `gerar.py` era fixo em 1.60.18. Como a T02 entra pela tela de
  login (`anonymous`), o acerto do gravador (`buildStorageState`) não cobre: o `gerar.py` agora lê `app/dist/.versao-app`. Todos os capítulos foram regravados.
- Respiros (`pausas.py`): cap02 `14.16:0.5`; cap04 `7.48:1.6 60.76:1.0 66.6:1.2`; cap12 `13.85:0.5`. No cap04, os cliques da frase "Ligo a tela, abro as ações, e ligo
  NF-e e NFS-e" e o do Relatório Financeiro correm colados (sem `at`). No cap11 o detalhe do Marcos já vem aberto (setup) e saiu o gesto "grupo Geral".
- Edição em `edicao/` (cópia de `$TUT_HOME/t02/edit`): `specs.json`, `fechar_t02.sh`, `montar_t02.sh`, `render_ilus_v3.sh` (pula cena pendente e lê `ilus_local.json`),
  `relatorio_pdf.py` (papel real do Relatório por Usuário: HTML do `actions.json` do cap12 → PDF A4 paisagem → PNG) e a cena `cenas_v3/relatorio.html`.
- Disco: o `finish.py` encheu o disco nos stems (1,3 GB); `out/T02/proj` virou link para `/dev/shm/t02_proj`.
