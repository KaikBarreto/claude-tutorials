# Andamento · T08 no app 1.60.10 (atualizado em 18/11)

## Feito
- `roteiro.md`, `narracao/tts_textos.py` (1.243 → 2.114 palavras), `plano.md`, `inventario.md`, `propostas_fala.md` (achados),
  `cenas/ilustracoes.json` (4 entradas novas com `v3: pendente`; duas renumeradas).
- 14 capítulos: novos 07 (com valores), 11 (avulsa com cobrança), 12 (sem internet); antigos 07, 08, 09, 10 → 08, 09, 10, 13.
- `$TUT_HOME/rec/t08/gerar.py` (todos os capítulos; cala o balão do Cato), `t08_grava.sh` (religa sempre), `t08_pdf.py` (caps 09 e
  11), `t08_lote160.sh` (lote com as sementes da cadeia), `t08_ex2.py` (explorações e5 a e8).
- Mundo: `seeds-extra/t08/inicio.json` (+ #56 da cooperativa, + rascunho apagado); handlers `rpc/finalize_weighing_ticket_v4.mjs` e
  `rpc/apply_standalone_weighing_charge_v1.mjs`; `schema.json` e `defaults.json` com as colunas `weighing_tickets.standalone_*`.
- Sementes da cadeia: `apos-cap02` a `apos-cap06` (as de antes); `apos-cap07`, `apos-cap08`, `apos-cap10`, `apos-cap11` saem do
  ensaio (o lote grava com `t08_semente.py`). As antigas `apos-cap07` e `apos-cap09` (numeração velha) foram apagadas.

## Ensaio
Resultado de cada lote em `$TUT_HOME/rec/t08/lote160.txt`; folhas de contato em `rec/t08/_folhas/`; resumos em `rec/t08/_ens/capNN.resumo`.
(ver o fim deste arquivo para o estado de cada capítulo)

## Comandos
```bash
cd /home/claude/ecoflix
bash /home/claude/claude-tutorials/planejamento/ecoflix/preparar_aula.sh T08   # tempos estimados
python3 -I rec/t08/gerar.py                                                    # cap00..cap13.json
bash rec/t08/t08_lote160.sh 07 08 09 10 11 12 13     # rápido de cada um, em ordem (a cadeia 07 → 08 → 10 → 11 grava as sementes)
bash rec/t08/t08_lote160.sh 08:--os-dois             # rápido + completa de um capítulo
FAKE_PORT=54308 bash rec/run.sh down                 # derrubar a instância no fim
```
Um capítulo da cadeia só roda depois do anterior ter gravado a semente (07 → 08 → 09 e 10 → 11 → 12 e 13).

## Estado em 18/11 19:55 (três lotes usados; instância 54308 derrubada)
| Cap. | Rápido (MP4 + folha olhada) | Completa |
|---|---|---|
| 00 a 06 | aprovado (0 falho, sem aviso de erro na tela) | não pedida (06: o respiro de ~3 s da L2/L3 continua valendo) |
| 07 | aprovado; semente `apos-cap07` gravada | **falta**: duas completas saíram com atraso (0,81 s no "Fechar"; depois 1,80 s na marca L6). O `gerar.py` já foi ajustado (Salvar na L6, "Fechar" na palavra "valor"); não foi rodado de novo |
| 08 | aprovado; semente `apos-cap08` gravada | aprovada (maxLate 0,72 s) |
| 09 | aprovado (liga, mostra e desliga as assinaturas; PDF novo em `rec/t08/arquivos/cap09-comprovante-termico.pdf`) | não rodada |
| 10 | **não fechou**: 4 `hover` do painel "Filtros" não acharam o alvo (opção "Cancelado" e os botões "Tipo", "Status", "Usuário" na 2ª abertura); o resto passou (finalizar, "Ver pedido", Exportar, #59). Seletores trocados no `gerar.py` (`FILTRO(...)`, `[role=dialog]`), sem novo ensaio |
| 11, 12, 13 | **não rodaram** (dependem das sementes `apos-cap10` e `apos-cap11`). Os fluxos do 11 e do 12 foram feitos passo a passo nas explorações `_ex/e7` e `_ex/e8` (telas e números conferidos), mas o roteiro do robô deles nunca rodou |

Para fechar (um lote só, nesta ordem):
```bash
cd /home/claude/ecoflix && bash rec/t08/t08_lote160.sh 10:--os-dois 11:--os-dois 12 13 07: 09:
grep -n '!!ERRO\|DIFERENTE:\|SEM ALVO' rec/t08/_ens/cap1[0-3].resumo rec/t08/cap*.resumo; tail -8 rec/t08/lote160.txt
FAKE_PORT=54308 bash rec/run.sh down
```

## Cap. 12 "Sem internet" refeito com queda de verdade (18/11, 21:20)
- **Como o app decide:** `src/hooks/useOnlineStatus.ts` mede por ping (`/auth/v1/health`, 1 por minuto, 2 falhas seguidas derrubam, 2
  sucessos levantam); `navigator.onLine` e os eventos `online`/`offline` só disparam a medição. O Salvar sem internet vai para a fila
  do IndexedDB (`WeighingTicket.tsx:2076` → `weighingTicketFinalize.ts`) e sobe pelo `OfflineBanner.tsx` quando `isOnline` volta.
- **Passo novo no robô (levar à skill):** `rede` em `rec/recorder/runner.mjs` (só acréscimo, antes do `wait`):
  `{do:'rede', offline:true|false, modo:'servidor'|'navegador', avisar:true}`. `servidor` (padrão) aborta na rede toda requisição ao
  backend (o navegador segue online: roteador ligado, link caído); `navegador` = `context.setOffline`; `avisar` dispara o evento
  `online`/`offline` para o app medir na hora. O mesmo passo entrou em `rec/t08/explorar.mjs`.
- **Capítulo:** no `setup` o ticket é preenchido (Cooperativa Recomeço, Alumínio latinha, Edson Moura, FKD2E41), a rede cai
  (`rede` + relógio do navegador adiantado 2 x 61 s para os dois pings; a tela começa 09:22). No vídeo: aviso âmbar; Pesagem avançada
  7210, Confirmar, Salvar → "Ticket OFF-01 guardado neste aparelho" + "Comprovante provisório (sem número oficial)"; Opções avançadas
  → "Anexar · Disponível com internet."; lista → Ações do #59 → Valorizar e Editar (os dois avisos vermelhos com o motivo); a conexão
  volta (`rede` + `avisar`) e em ~4 s o ticket aparece numerado em "Aguardando valorização".
- **Fala:** 4 → 6 linhas (35,8 → 53,5 s estimados), na ordem da tela (as três coisas antes da volta); `roteiro.md` (coluna Tela) refeito.
- **Ensaio** (exploração `_ex/e9`, `t08_ex3.py`/`t08_ex9.sh`): rápido 0 falho, 8 conferências OK, folha olhada; completo 0 falho,
  maxLate 0,71 s (o "Valorizar" do menu; o `at` dele foi levado 0,3 s para a frente depois, sem novo ensaio). Folhas em `_folhas/`.
- **Pendência:** a semente `apos-cap11` ainda não existe (o cap10 não fechou a completa). O ensaio usou `T08_SEM12=apos-cap08`
  (o ticket virou #60); com a `apos-cap11` o `gerar.py` espera o **#61** (a avulsa do cap11 é a #60): conferir no lote.
  `T08_SEM12=apos-cap08 python3 -I rec/t08/gerar.py 12 && bash rec/t08/t08_grava.sh 12 --os-dois` repete o ensaio sem a cadeia
  (o `t08_lote160.sh` roda o `gerar.py` sem a variável, ou seja, com a `apos-cap11`).
- **Defeito do app (lista de melhorias):** com o navegador offline de verdade (cabo/wi-fi desligado: o navegador dispara o evento
  `offline`), "Salvar Ticket de Pesagem" fica girando e nada vai para a fila até a rede voltar. Causa: `saveTicket = useMutation({...})`
  em `src/pages/WeighingTicket.tsx:1947` não tem `networkMode: 'always'`; o react-query v5 (padrão `online`, `App.tsx:298` sem
  `mutations.networkMode`) pausa a mutação enquanto o `onlineManager` está offline, então o ramo offline (`:2076`) nem roda. As
  consultas da mesma tela já usam `networkMode: 'always'` (`:863`). Visto no `_ex/e9` passo 120-131 (`setOffline`: botão desabilitado
  girando 15 s, fila vazia; na volta salvou online como #61) e no ensaio antigo (evento `offline` simulado, 18 s). Só funciona como a
  aula mostra quando a internet cai e o navegador continua "online" (roteador ligado). Correção: `networkMode: 'always'` nessa mutação.
  A linha "Sem internet (queda simulada no robô)" do `propostas_fala.md` fica substituída por este achado (não editei aquele arquivo).
- Também visto: sem internet a aba nova mostra "#1" no lugar do próximo número (previsto no código, `WeighingTicket.tsx:3765`).

## Ajuste de foco a pedido do Kaik (18/11, 22:45): avulsa enxuta, mais ticket
- **Fala** (`tts_textos.py`, `roteiro.md`, `plano.md` → "Ajuste de foco"): 2.154 → 2.017 palavras; narração estimada 993,8 → 932,2 s.
  - cap11: 13 → 6 linhas, 311 → 121 palavras, 138,5 → 55,0 s (1ª frase intacta: âncora da ilustração). Saíram os campos do cadastro
    rápido, a placa, o tipo de caminhão, o "Completo", a divisão entre formas, a trava e o estorno.
  - cap01: + 3 linhas com os casos de uso (preço que fecha depois; vários caminhões; ticket de venda); avulsa numa frase (63,0 → 78,9 s).
  - cap08: L4 "Como este ticket foi feito sem valores, o preço vem da tabela"; L5 + "Já no ticket com valores, como o do Jair, vale o
    preço que está no ticket." (78,6 → 87,7 s). cap10: sem mudança. cap13: L5 encurtada.
- **Robô** (`gerar.py`): cap01 (3 gestos novos, calmos) e cap11 refeito (61 passos; sem Editar/valor travado). cap08, cap12 e cap13 só mudaram de tempo.
- **Ensaio** (um lote, `rec/t08/lote160_avulsa1.log`): 01, 08, 11, 12, 13 no rápido com MP4: 0 falho, 0 SEM ALVO, conferências OK,
  avisos de erro `[]`, folhas olhadas (`_folhas/_ens-capNN.jpg`). Sementes `apos-cap08` e `apos-cap11` regravadas; o cap12 deu o #61.
  PDF novo do comprovante da avulsa em `rec/t08/arquivos/cap11-comprovante-avulsa.pdf` (sem placa, sem tipo de caminhão, sem as duas pesagens).
- **Pendente:** completa do cap11 não rodada. O `prever` (com as esperas do rápido, que saem maiores) aponta até ~3 s de atraso no
  trecho cliente → peso (L2 e L3): conferir com `bash rec/t08/t08_lote160.sh 11:` depois que a voz chegar; se atrasar, a folga está nas
  L5 e L6. O `cenas/ilustracoes.json` não foi mexido: a entrada do cap11 ainda descreve três janelas (comprovante com placa e as três formas).
- **Achado do app:** o comprovante da avulsa (serviço ao cliente) sai com "Fornecedor: Areal Boa Vista" e "Itens comprados".
- Instância 54308 derrubada.
