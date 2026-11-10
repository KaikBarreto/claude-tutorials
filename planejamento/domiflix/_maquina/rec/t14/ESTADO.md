# T14 · estado (porta 54341) · fase 2 na 1.38.24 · RENDER EM ANDAMENTO (06/11 08:2x)

**Feito:** voz nova (zip 9 do Kaik: caps 02, 03, 08 e 13 inteiros; emenda do cap10 L3; o cap00 fica com o take original); robô ajustado às vozes
(prévia `prever.py`); respiros na voz dos caps 09, 10 e 12; ensaios `--rapido` da câmera (03, 05, 07, 10, 13: 0 falho); **gravação final dos
caps 00 a 13 aceita** (tabela abaixo).
**Render ("T14: render", 06/11 07:1x):** `t14/edit/caps/specs.json` (zooms, destaques, avisos "Antes"/"Próximo", ilustração do cap01, cortes e
aceleração do cap09) -> `montar_cap.py` -> `auditar_camera.py` com **0 problema nos 14** -> `render_todos.sh` (uma trava por capítulo, piso 1,3 GiB).
Capítulos 00 a 10 renderizados (`t14/edit/out/capNN/`); **parado pelo piso de disco antes do cap11** (1.325 MB livres às 07:57; avisado ao
coordenador); faltam 11, 12, 13 (`bash t14/edit/render_todos.sh 11 12 13`), o finish (`bash t14/edit/finish_t14.sh`, piso 1,2 GiB) e as legendas.
Maior trecho sem zoom/destaque nos renderizados: 5,9 s (cap10). Ferramentas do T14: `finish.py` (cópia do T21 + `acelera`), `montar_cap.py`
(cópia do T21 + `acelera`), `overlay.py`/`stage.py` da skill (os antigos em `*.antes_skill`), ilustração em `t14/edit/ilustracoes/`.
**O `entregar.py` é do coordenador.**

## Regras da aula
- `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54341`; o `rodar.sh` acerta o relógio da instância (e a religa se o
  container reiniciou): `FAKE_NOW=2026-11-13T15:10:00-03:00` nos caps 0 a 11 e `2026-11-13T16:20:00-03:00` nos caps 12 e 13 (a Receita só aceita
  uma consulta de NF-e por CNPJ a cada 65 min; `rec/t14/cadeia.json`).
- Mundo: fim do T21 (`t21/apos-cap10`) + `t14/inicio`; cada capítulo parte do último `t14/apos-capNN` (`SEMENTE` no `_head.py`).
  **Sem `--seed`** na fase 2 (as sementes de 05/11 valem; a `t14/apos-cap12` é a base do T17; o `rodar.sh` recusa `--seed`).
- Navegador só sob `flock /home/claude/domiflix/.heavy.lock nice -n 10`, uma trava por capítulo. Sem pkill; sem commit.
- `rec/t14/lote.sh [--gravar] NN ...` (sem `--gravar`: ensaio `--rapido`); resumo em `rec/t14/_debug/{ens,rec}-NN.log`.
- `rodar.sh` para com < 1,5 GiB de disco ou com o 8080 sem 200 (confere antes e de novo dentro da trava); quadros em `/dev/shm/t14_rec`, saídas
  movidas para `rec/t14/` (ou `_ens/`) no fim de cada capítulo.
- Senha do certificado fictício: só `$TUT_SENHA` (sorteada pelo `rodar.sh`, 8 letras; nunca no roteiro nem no log).
- `prever.py NN [--ens] [--tudo]`: ritmo previsto sem navegador. `gerar.py` = `_head.py` + `_caps.py` + `_fim.py` (`bash rec/t14/montar.sh`).
  Âncora `c.A(linha, palavra, folga)`: folga > 0 = antes da palavra; < 0 = depois do início dela. Fase 1: `*.fase1` e `_fase1/`.
  Lições: `rec/t14/LICOES.md`.
- Nenhum PDF aparece no vídeo (decisão de 05/11): o cap08 L4 fica no "Baixar PDF" do menu, sem clicar.

## Voz (zip 9, `recebido/2055_lote6/zip/`, cópia em `t14/narracao/recebido_1_38_24/`)
- `proc.py` (log `t14/narracao/proc_1_38_24.log`): cap02 54,32 s (semelhança 0,95; 0 palavra fraca); cap03 46,64 s (0,94; 1 fraca: "aqui" em
  6,17 s, que aparece no ASR desacelerado: não é defeito); cap08 25,84 s (0,92; 0); cap13 = nó "v2" 40,08 s (0,98; 1 fraca: o "a" de "com a
  autorização", que se funde com o "a" seguinte na fala corrida, nem desacelerado aparece; não é defeito); cap10 38,09 s (0,96; 0).
- Emenda do cap10 L3 (`T14_emendas_cap10.mp3`, 10,19 s): `EMENDA_COMPRIME_MAX=0` + `"empurra": true` (`trocas.json`); +4,25 s (33,84 -> 38,09 s);
  folga 0,21 s antes da L4; junção limpa (sem salto entre amostras; log `emendar_1_38_24.log`).
- Originais: `capNN.v1.json` (02, 03, 08, 10, 13); antes dos respiros: `emendas/capNN.orig.json` (09, 10, 12).
- `emendar.py` e `pausas.py` = os da skill (o `emendar.py` antigo em `emendar.py.antes_skill`); `proc.py` já era igual.
- Respiros (`pausas.py`, tempos no relógio de antes do respiro): cap09 `7.2:5.6 10.4:4.6` (32,96 -> 43,16 s); cap10 `20.6:1.5` (38,09 -> 39,59 s);
  cap12 `34.0:2.8` (41,44 -> 44,24 s).

## Gravação final (G, 06/11 02:09 a 02:40; `rec/t14/t14-capNN.{mp4,actions.json,telemetry.json,contact.jpg}`)
Todos: 0 falho, `__avisos` "[]", `unknowns` [], 0 DIFERENTE (tela × fala), folha de contato sem erro do app e só com o mundo fictício.
Console: só o 409 de `nfse-status` com o rascunho na lista (defeito em handoff) e os 406/WebSocket de sempre.

| Cap | Maior atraso | Vídeo / voz (s) | Cap | Maior atraso | Vídeo / voz (s) |
| --- | --- | --- | --- | --- | --- |
| 00 | 0,03 | 37,34 / 35,84 | 07 | 0,69 | 33,90 / 32,40 |
| 01 | 0,23 | 32,53 / 30,80 | 08 | 0,65 | 27,34 / 25,84 |
| 02 | 0,13 | 55,83 / 54,32 | 09 | 0,36 | 44,66 / 43,16 |
| 03 | 0,29 | 48,14 / 46,64 | 10 | 0,56 | 41,09 / 39,59 |
| 04 | 0,09 | 25,34 / 23,84 | 11 | 0,12 | 27,46 / 25,84 |
| 05 | 0,07 | 37,50 / 36,00 | 12 | 0,64 | 45,74 / 44,24 |
| 06 | 0,27 | 44,22 / 42,72 | 13 | 0,65 | 41,58 / 40,08 |

- cap09 foi gravado 3 vezes: 02:27 falhou (o menu do rascunho fechou entre dois itens; ver LICOES), 02:36 passou mas com o "Cancelar" sob a
  fala (o corte não cabia), 02:40 é a válida. Quadros das falhas em `rec/t14/_debug/falha-*.png`.
- Mudanças do robô na fase 2: `at` reancorados às vozes novas; saíram os hovers de IM/IE (cap04), da dica do NBS (cap05), do "Salvo" (cap10) e
  do "Revisar e Emitir" (cap13); `js_aba_visivel` antes de clicar a aba Financeiro do contrato (cap10, cap13); `confere_ausente(espera=)`;
  o observador ignora a dica "fica indisponível"; cap09 com a guarda que reabre o menu da linha + `noScroll` e o "Cancelar" depois da fala;
  cap10 com `noScroll` na opção do NBS e a descrição digitada logo depois do "No vencimento da parcela"; cap12 com o Salvar no respiro.

## Cartões (para o render)
- Antes: "Relatório Financeiro e DRE" (T20). Próximo: "Funcionários: Financeiro do Funcionário e Ponto Eletrônico" (T15).

## Para a montagem (só com "T14: render")
Tempos em s do vídeo de cada capítulo (= relógio da narração; o vídeo tem ~1,5 s a mais no fim). Medidos na gravação final, pela fala
(`t14/narracao/capNN.json`) e pela diferença entre quadros (o cursor é desenhado na edição: conferir que ele não pula fora do corte).
- **cap01:** ilustração dos dois caminhos (roteiro): L1 0,00–9,48 com o caminho de cima (NFS-e) em destaque; L2 9,72–18,60 com o de baixo (NF-e).
- **cap09, respiro 1** (voz calada 7,08–12,92): a janela desce 6,6–7,1 e o campo da discriminação é limpo e digitado 7,9–11,47 (acelerar 4x,
  com selo); 11,50–12,60 a tela fica parada (só o cursor de texto pisca): cortar (o corte acaba 0,3 s antes de "Começo", 12,92). Esperado: o aviso vermelho do NBS e "5 pendência(s) para emitir" no
  rascunho (o tipo de serviço não tem NBS; o rascunho não precisa).
- **cap09, respiro 2** (voz calada 15,88–20,64): **CORTE 16,15 → 19,40** ("Cancelar" clicado em 16,09; a janela "Descartar nota?" aparece em
  16,27; Descartar, "Relatório fiscal" e a volta à lista até 19,07; a lista com o rascunho fica parada até o cursor sair para o "⋯" em 19,90).
  Sobra ~1,5 s de pausa entre "Salvar rascunho." e "O rascunho não vai pra prefeitura.".
- **cap10:** respiro (voz calada 20,52–22,18): manter (a descrição termina de ser digitada em ~20,6 e o "Salvo" aparece em ~21,1–21,6; a tela
  desce em 22,27). Troca de tela por `pushState` (contrato -> Notas Fiscais) em 34,73, sob "a nota sai sozinha": corte seco instantâneo, sem
  tirar tempo.
- **cap12:** o "corte" do worker (10,64–10,81: semente + relógio do navegador 4 min à frente, depois do "Ciência em processamento") não muda a
  tela (só o relógio do cabeçalho pula de 16:20 para 16:24): nada a tirar. Respiro (voz calada 33,84–36,88): manter (o robô termina a forma de
  pagamento, vai ao Salvar e clica em ~36,05; a janela fecha em 36,6 com "Despesa lançada e vinculada à nota."). O aviso "Nenhuma nota nova foi
  encontrada." do Sincronizar (~16,6) está no roteiro.
- **cap13:** trocas de tela por `pushState` em 19,52 (Notas Fiscais -> contrato, sob "pede um motivo") e 24,00 (contrato -> Notas Fiscais, no
  "E as notas dos fornecedores"): cortes secos, sem tirar tempo. O cartão "Nota fiscal automática" fica na tela de ~23,3 a 24,0.
- Handoffs (defeitos do app, a fala não depende deles): lista no roteiro (`planejamento/domiflix/T14/roteiro.md`, marcas `[handoff: ...]`).
