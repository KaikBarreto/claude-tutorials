# T00 · andamento da aplicação do 1.60.10 e 1.60.18 (notas para retomar)

Atualizado em 20/11 (1.60.18, tela 1600x900). Quem continuar: leia só este arquivo, o `_BRIEF_APLICAR_160.md` e o cabeçalho do `rec/t00/gerar.py`.

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

## Ensaio no 1.60.10 (18/11, três lotes; resultados em `$TUT_HOME/rec/t00/_ens/lote/*.txt` e `rec/t00/.capNN.out.resumo`)
| Capítulos | Rápido (0 falho, sem "SEM ALVO", folha olhada) | Completo |
|---|---|---|
| Computador 00 a 15, 40, 41 | todos | 04, 08, 12, 14 (maior atraso 0,59 / 0,35 / 0,62 / 0,85 s, este no primeiro gesto, já era assim); 07 com 0,88 s na aba "Aparência" |
| Celular 00b a 15b, 40b, 41b | todos | 07b (0,11 s) e 08b (0,00 s) |

- Depois do último lote só mudou uma âncora do cap07 (o clique em "Configurações" 0,5 s mais cedo, por causa do 0,88 s): **não foi ensaiada**.
  Para conferir: `TUT_SENHA=<8+> bash rec/t00/t00_um.sh 07 --completo` (com a instância 54300 de pé).
- Ficaram só no rápido (sem gesto sensível novo): 00, 01, 02, 03, 05, 06, 09, 10, 11, 13, 15, 40, 41 e os de celular menos 07b e 08b.
  O `prever.py` acusa folga curta antiga no 09 (aba "Usabilidade", 1,1 s), no 10 ("Gerenciar plano", 0,8 s) e no 15 (L5, 2,0 s, depois
  do "Confirmar"): a gravação final com a voz confere.
- A instância 54300 foi derrubada.

## Diferenças do celular (9:16) achadas no ensaio
- Trilha: sem "Buscar aula" nem "Minha Lista" na tela (cap02 L3 fica parado); cabeçalho sem "Buscar" (cap06 L10: só fecha a gaveta).
- Player em pé: sem "Abrir em tela cheia". Janelas "Montar plano" e "Cancelar Assinatura" são gavetas sem botão "Fechar": o robô fecha com Esc.

## Achados do app (para o MELHORIAS)
- Assinatura: "Plano Personalizado • 10 módulo" (no alto) e "4 pagamento realizado" (histórico) saem no singular.
- "Montar plano" soma o catálogo e ignora o valor contratado: com a mensalidade do mundo base (1.025,00, `extra_users` 0, `max_users` 3) abre com
  "2 usuários" e "+R$ 300,00 vs plano atual" sem o cliente mexer em nada. A semente da T0 usa 1.350,00 e `extra_users` 1.
- Player: os botões de voltar e avançar 10 s do computador não têm nome acessível (os do celular têm).
- Fim da aula: "A próxima aula começa em 4 segundos" avança sozinho; só pausa se o mouse passar por cima.
- Cancelar: o botão "Falar com o Sucesso do Cliente" só aparece em 4 dos 8 motivos (em "Pausa temporária", por exemplo, não).
- Antigo, continua: o histórico chama o pagamento de "Cobrança • empresa" (não "Renovação").

## 1.60.18 (20/11)
- Única mudança que atinge a T00: o menu Fiscal & Ambiental tem agora **"Relatório/Estoque Fiscal"** (`routes.ts:510`) no lugar de "Estoque Fiscal" +
  "Relatórios Fiscais" (varredura: cap06 falhava no hover "Estoque Fiscal"). Fala do cap06 L4 mudada (1 linha): "...os documentos ambientais e o
  relatório e estoque fiscal." Mexidos: `tts_textos.py`, `roteiro.md`, `plano.md`, `inventario.md`, `rec/t00/gerar.py` (FISCAIS: 5 itens, âncora "relatório").
- `preparar_aula.sh T00` e `gerar.py --ens` rodados. Fala sem PDF/comprovante (nada a devolver na tela). Sem margem automática na aula.
- Lote em segundo plano: `rec/t00/_ens/lote_rapido.log` (36 rápidos) e depois `lote_completo.log` (06, 07, 06b completos); resultados em `rec/t00/_ens/lote/*.txt`.
  Instância 54300 ligada para o lote (derrubar: `FAKE_PORT=54300 bash rec/run.sh down`).
- Corrigidos pelo app (achados antigos do MELHORIAS): plural do plano, "Sucesso do Cliente" nos 8 motivos, botões de 10 s do player com nome.

## Vertical (9:16) · andamento (27/11, parcial)
**Estado: NÃO concluído.** A fila pesada (`rec/fila.sh`) está dominada pela T15 (prio 15) e anda ~1 capítulo a cada 15 min; `/` ficou entre 817 e 915 MB (a T15 grava ilustrações lá; do lado da T00 só vão actions, telemetria e folha em `rec/t00`; mp4 em /dev/shm).
- **Roteiros do celular**: os `.9x16.json` estavam defasados (20/11, voz ESTIMADA de 53 s). Regerados com a voz real (`python3 -I rec/t00/gerar.py --so-p`; o 16:9 não foi tocado; cópia dos antigos em `/dev/shm/t00v_old`).
- **Gravação** (`rec/t00/t00v_final.sh`, prio 30, mp4 em `/dev/shm/t00v_rec`, resumo em `rec/t00/capNNb.resumo`, log `rec/t00/final_v.log`): feitos 00b, 01b (maxLate 2,77 s: revisar âncora), 02b (0,68 s), 03b (1,61 s: revisar). Faltam 04b a 15b (reexecutar `bash rec/t00/t00v_final.sh 04 05 ...` com `TUT_SENHA`). 00 e 05 são só ilustração; 40/41 (variantes) não gravadas.
- **Ilustrações verticais**: kit novo `perfis/ecoflix/cenas_v3_vertical/` (cópia do v3 com janela 504x850 = painel 1008x1700; o v3 do 16:9 não mudou), render `ferramentas/edit/cenas/render_cenas_v3_vertical.cjs`, cena `planejamento/ecoflix/T00/cenas_v3/cena_vertical.html` (as 8 cenas em coluna, um item por vez; folhas de conferência olhadas e enquadramento ajustado). Palco: `t00/edit/compor_painel_vertical.py`. Pronto: `ilu00_abertura_full.mp4` (1001 quadros). Faltam as outras 7 (`bash t00/edit/render_ilus_vertical.sh`).
- **Montagem**: `t00/edit/montar_vertical.py` (gera `caps/capNN.9x16.chapter.json` e `caps/T00.9x16.aula.json`) e `t00/edit/finish_v.py` (só o vídeo; copia o áudio do 16:9 sem recodificar: LUFS -16,3 e pico -3,8 dBTP idênticos). Falta: render dos capítulos (`render_chapter_vertical.py`, `compor_ilus_vertical.py`), `finish_v.py`, folha de 3 em 3 s, copiar `legendas/aula_final.{srt,vtt}` (linhas <= 32 caracteres, servem).
- Nenhum achado novo do app até aqui.
