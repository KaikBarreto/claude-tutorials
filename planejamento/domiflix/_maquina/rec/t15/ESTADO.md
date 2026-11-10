# T15 · estado · 06/11 02:2x · fase 2 completa até o finish e as legendas · PARADO ANTES do `entregar.py` (é do coordenador)

**Feito:** emendas da voz, gravação final (0 a 12 e 9b, 1.38.24), montagem, render, finish e legendas. **Falta:** `entregar.py`
(nome: "Domiflix T15 - Funcionários - Financeiro do Funcionário e Ponto Eletrônico") e a limpeza depois da entrega.

## Render (pedido "T15: render", 06/11)
- Saídas: `t15/edit/out/T15/aula_final.mp4` (600,73 s = 10:00,7; 1920x1080 30 fps H.264 yuv420p bt709 TV + AAC 48 kHz estéreo; 166 MB),
  `video_sem_audio.mp4` (NÃO apagar: o remendo exige o total exato de quadros), `capitulos.json`, `proj/{audio48k.wav, edl.json, render.json,
  build/intro_v.mp4, build/outro_v.mp4}`, legendas `out/T15/legendas/aula_final.{srt,vtt}` (169, sem sobreposição, linha até 42),
  folhas de 3 s do vídeo inteiro `out/T15/folhas3s/folha_01..07.jpg` (`t15/edit/folhas3s.sh`: `fps=1/3:round=up`, quadro no tempo do rótulo).
- Áudio: mix −15,8 LUFS; pico real depois do AAC −3,6 dBTP (ebur128); `pico_aac.py --so-medir`: nenhum trecho acima de −1 dBTP.
- Câmera: `auditar_camera.py` com 0 problema e 0 instante fora/na borda nos 14 capítulos; `auditar_recorte.py caps/cap09b.chapter.json`: RECORTE OK
  (pior erro 0,01). Maior trecho sem zoom/destaque/aviso: 11 s antes do zoom do "Regime" (cap03); agora < 9 s.
- Ferramentas novas ou mudadas (só em t15/ e rec/t15/): `montar_cap.py` (computador + celular pelo tamanho do vídeo; `voz_ate`/`voz_de` cortam a voz
  do cap. 9 em 26,20 s, no silêncio entre as linhas 3 e 4: o `09` termina ali e o `09b` começa ali, `audio_offset` −26,2), `overlay.py` e `stage.py`
  da skill (avisos ao lado do aparelho; recorte do canto do celular), `auditar_recorte.py`/`folha_transicoes.py` da skill, `montagem_cap12.py`,
  `render_todos.sh`, `folhas3s.sh`, `rec/t15/finish_t15.sh` (stems, música e mix em /dev/shm por link; o /dev/shm/t15_finish já foi apagado),
  `t15/narracao/legendas_aula.py` (o 09b usa a voz do cap09 a partir do corte; antes em `legendas_aula.py.antes_9b`).
- Cap. 12 = montagem rápida (`t15/edit/out/montagem_cap12.mp4`, 1586x992, 17 batidas casadas com as palavras, até 2,5x, recorte de 1,2 a 1,4x)
  como ilustração sobre a janela em repouso (at −0,35: entra opaca no 1º quadro); a tomada ao vivo do cap. 12 fica escondida embaixo. As gravações
  brutas continuam em rec/t15 (a montagem lê delas).
- Cartões: "Antes: Notas Fiscais" (cap00, 34,3 s) e "Próximo: Ferramentas de RH: DISC, Organograma, Fluxograma" (cap12, 587,9 s), conferidos nas folhas.

Regras: `export TUT_HOME=/home/claude/domiflix FAKE_URL=http://127.0.0.1:54336`; backend e robô com `FAKE_NOW=2026-11-11T09:00:00-03:00` nos caps. 0 a 10
(`FAKE_PORT=54336 FAKE_NOW=... rec/run.sh fake`) e `2026-11-12T08:30:00-03:00` nos caps. 11 e 12 (reiniciar o falso com o outro FAKE_NOW entre os dois lotes
e exportar o mesmo FAKE_NOW antes do `lote.sh`; `rodar.sh` confere o FAKE_NOW do processo). Navegador só sob `flock $TUT_HOME/.heavy.lock nice -n 10`,
uma trava por capítulo. Sem pkill; sem commit. **Sem `--seed`**: as sementes `seeds-extra/t15/apos-capNN.json` de 05/11 valem (base final `t20/apos-cap12`;
`t15/apos-cap12` já foi passada ao T22).
- `rec/t15/lote.sh --gravar 0 1 2 3 4 5 6 7 8 9 9b 10`, depois (falso de 12/11) `FAKE_NOW=2026-11-12T08:30:00-03:00 rec/t15/lote.sh --gravar 11 12`;
  resumo em `rec/t15/_debug/rec-NN.log`. Sem `--gravar` o lote faz o ensaio `--rapido` (e grava sementes nos caps. 5 a 9b: NÃO usar agora).
- `rodar.sh` para se o disco tiver < 1,5 GiB ou se o 8080 não responder 200.
- `prever.py NN [--ens]`: simula o ritmo com as durações medidas na última gravação (ou no ensaio rápido) e o `at` atual, sem navegador.
- O falso 54336 caiu no reinício de 06/11 00:39 e não foi religado (o render não usa navegador).

## Voz (emendas 1.38.21, voz `T15 emendas 1.38.21`, `recebido/1454_lote9/zip/T15_emendas.mp3`, 49,95 s)
- `t15/narracao/tts_textos.py` = o do planejamento (falas novas; o antigo em `tts_textos.py.antes_emendas`); `config_narracao.json` igual ao do planejamento;
  `emendar.py`, `titulos.py`, `pausas.py` e `proc.py` = os da skill (antigos em `*.antes_skill`).
- `trocas.json` (5 trocas, `empurra` em todas) + `EMENDA_COMPRIME_MAX=0`: velocidade natural. Originais em `cap02.v1.json`, `cap05.v1.json`, `cap10.v1.json`;
  saída `emendas/capNN_v2.wav` e `proc.py` neles (logs `emendar_1_38_21.log`, `proc_emendas_1_38_21.log`).
- Durações: cap02 38,48 s (igual; a frase nova é mais curta, folga 0,95 s antes da L4), **cap05 29,26 s (+4,86 s)** (L1 termina 1,45 s antes da L2),
  **cap10 38,63 s (+2,31 s)**. 0 palavra fraca nova (cap02: "a" em 2,60 s e "e" em 20,44 s, ASR colando palavras; no take original já havia uma).
- Narração total: 542,0 s (cap09 = 57,52 s: computador até a L4, celular da L4 em diante).

## Gravação final (G), 1.38.24, `rec/t15/t15-capNN.{mp4,actions.json,telemetry.json,contact.jpg}`
| cap | falhos | maior atraso (gesto / marca) | obs. |
|---|---|---|---|
| 00 | 0 | 0,48 / 0,06 | |
| 01 | 0 | 0,00 / 0,24 | |
| 02 | 0 | 0,38 / 0,61 | |
| 03 | 0 | 0,28 / 0,58 | regravado (1ª: 1,08 no "Aplicar") |
| 04 | 0 | 0,00 / 0,21 | |
| 05 | 0 | 0,00 / 0,00 | fala nova |
| 06 | 0 | 0,71 / 0,60 | regravado (1ª: 1,16 só na marca L7) |
| 07 | 0 | 0,00 / 0,18 | |
| 08 | 0 | 0,48 / 0,04 | |
| 09 | 0 | 0,00 / 0,07 | |
| 09b | 0 | 0,00 / 0,00 | celular; "sem observador" (a página navega) e aviso de Mixed Content do logo: iguais à fase 1 |
| 10 | 0 | 0,29 / **0,86** | regravado; a marca L3 sai em 12,40 s, ANTES da fala da L3 (12,44 s): não é atraso de tela |
| 11 | 0 | 0,66 / 0,54 | regravado 2× (a página de Contas fica clicável entre 5,6 e 6,0 s) |
| 12 | 0 | 0,31 / 0,40 | regravado (1ª: 2,73; Contas a frio) |

Todas com conferências tela × fala OK (0 DIFERENTE), `__avisos` vazio, 0 pageError, `unknowns` vazio. Sem respiro (`pausas.py`) e sem corte.
Folhas de contato vistas: 00, 05, 09b, 10 e 12 (Glacial Cold Brasil, rodapé "Dominex v1.38.24", relógio 24 h, nenhum dado real).

## Mudanças no robô nesta fase (`_head.py`, `_caps.py`; `montar_gerar.sh` refaz o `gerar.py`; roteiros atuais = tomadas finais)
- cap05: âncoras nas palavras da fala nova (antes `L(i)+dx`); `confere_ausente(..., espera=1.5)` (confere a cada 0,1 s em vez de 1,8 s fixos).
- cap10: L5 nas palavras novas ("Filtrando", "pessoa", "você", "saldo"); justificativa no "escreve" e Cancelar no "obrigatória" (cada gesto nesta tela leva
  1,3 a 2 s até o alvo; o "Histórico", ~2 s); hovers do endereço 0,7 s, calendário 0,6 s, horas 1,0 s.
- cap02: cadeia nome/CPF/telefone/cargo começa 0,4 s antes (sem o "e-mail", telefone e cargo ficaram a 1 s um do outro).
- cap00: "Gestão" 1,5 s antes do "cadastro" (1º clique ~2,5 s). cap03: hover do Custo Total logo depois da digitação; Aplicar no "Aplico".
- cap06: `mark(7, antecipa=0.3)`. cap11: hover "Quitando" 0,8 s; aba A Pagar e busca ancoradas no custo real. cap12: `prewarm` com `/financeiro/contas`.

## Diferenças em relação ao roteiro
- cap12 (montagem): a ficha da Tatiane com os selos vem do fim do cap09; o Extrato aparece recortado na lista de movimentos (os cartões do topo já
  mostram o ciclo novo, zerado, depois do pagamento); a batida do 9b entra num aparelho genérico sobre o fundo gelo, dentro da janela; a linha 5
  (próximo tutorial) segura as folhas em A Pagar do cap11 sob o cartão "Próximo"; a montagem não tem cursor (gravação bruta).
- cap09 -> 09b: corte seco do computador para o celular no "No celular da Tatiane" (o 9b é a segunda metade do cap. 9, sem vinheta).
- cap01: "Novo Funcionário" ganhou destaque em vez de zoom (o botão fica colado na borda direita).
- cap10 L5: o filtro da Tatiane fecha com Esc (sem clicar "Aplicar (1)"); o relatório dela aparece do mesmo jeito.
- Duração 10:00,7 (o roteiro estimava ~11 min).

## Mundo
- `semear.py` -> `seeds-extra/t15/{inicio,salarios,folhas}.json` + `cadeia.json`. Base = fim do T20 (`t20/apos-cap12`) + `t2/apos-cap10` (a Tatiane como usuária)
  + `t15/inicio` (técnicos "Informal", mensal, 5º dia útil, salário 0). Sementes dos capítulos cumulativas: `apos-cap05` ... `apos-cap09b`; cap. 6 junta
  `t15/salarios`; caps. 11/12 juntam `t15/folhas`. `_dev-*.json` são só para explorar.
## Handlers novos (rec/fakebase/handlers/)
- rpc: `create_employee_vale` (+ DEFAULT de `employee_movements.movement_order`), `generate_ponto_slug`, `get_employee_face_template_status`,
  `create_employee_face_enrollment_link` (token = hash do NOME), `get_or_create_ponto_kiosk_slug`, `has_ponto_pin`, `register_time_punch`,
  `recompute_time_sheet`. functions: `time-clock-portal` (get_state, register_punch; carimba FAKE_NOW + 2 min), `face-enrollment` (context).
## Robô
- `gerar.py` = `_head.py` + `_caps.py` + `_tail.py`. Cap. 9 = `cap09` (computador, linhas 1 a 3) + `cap09b` (celular sem login, linhas 4 a 7 = L1..L4 do trecho).
- Descobertas da 1.38.21 (valem na 1.38.24): e-mail na aba "Acesso"; com usuário vinculado a chave "Criar acesso ao sistema" some; "Registro manual" sem
  campo Data; placeholder "R$ 0,00" com espaço não separável (seletor por prefixo `R$`); "Ativado" casa também "Desativado" (nome exato); interruptores
  da Config sem nome (xpath pelo rótulo).
