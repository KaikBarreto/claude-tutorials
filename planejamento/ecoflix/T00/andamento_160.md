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

## Vertical (9:16) · CONCLUÍDO (27/11)
**Entrega**: `/home/claude/ecoflix/t00/edit/out/T00/entrega/EcoFlix T00 - Bem-vindo ao EcoSistema 1.60.22 (vertical).mp4` + `.srt` + `.vtt` (as do 16:9, linhas <= 32 caracteres, servem).
1080x1920, 30 q/s, 804,40 s (igual ao 16:9), áudio copiado do 16:9 sem recodificar (-16,3 LUFS, pico -3,8 dBFS). Montagem em `/dev/shm/t00v_proj` (apagada o que era intermediário).
- **Gravação no celular 390x844** (`rec/t00/t00v_final.sh`, pela fila, prio 30): 00b a 15b e as variantes 40/41. maxLate por capítulo: 01 0,21 · 02 0,68 · 03 0,10 · 04 0,31 · 05 0,00 · 06 0,11 · 07 0,00 · 08 0,00 · 09 0,41 · 10 0,73 · 11 0,41 · 12 0,62 · 13 0,04 · 14 0,47 · 15 0,11 · 40 0,00 · 41 0,00 (todos <= 0,8 s, 0 falhos, 0 erros de página).
  Correções no `gerar.py` (só o vertical): cap01 hover em "Pular por agora" com `noScroll` (a rolagem do robô levava 5 s e atrasava a marca L5 em 2,8 s); cap03 âncoras de "Ver trilha" (folga 0,5) e da rolagem da gaveta (0,1); cap14 "Continuar" e "Voltar" e cap15 "Confirmar e começar a primeira aula" com `noScroll` (botão no pé da tela; a rolagem inútil levava ~5 s e dava atraso de 4 s).
- **[TESTAR] cap02** (gaveta "Ver trilha" abre por cima da página): funcionou como o plano previa; a lista do celular não tem selos e a gaveta os mostra. Nenhuma tela inventada; nenhuma alternativa do plano foi preciso usar.
- **Ilustrações**: as 8 renderizadas (`render_ilus_vertical.sh`; o laço lia o `lista.txt` pela entrada padrão e o node/python comiam as linhas: agora `</dev/null`).
- **Câmera do celular** (a janela mostra 483 dos 844 px): (1) `celular_vertical.py` passou a tratar `hover` e `type` sem clique do `actions.json` como alvo da câmera (antes só os toques; as frases do portão, da Assinatura, da Conta etc. mostravam o alto da tela enquanto a fala citava o pé); (2) a checagem "âncora no canto" (vale para o 16:9) deixou de contar no vertical, porque a vista é presa à tela; (3) `montar_vertical.py` ganhou `EXTRA`: `camera_9x16` com `group_gap 1.0`, `pad 0.0`, `lead 1.2` (cap01 `lead 2.0`) nos capítulos de tela real, e um zoom manual no cap06 (L10 "no alto da tela ficam a busca e o sino": sem hover no celular, a câmera ficava no pé; agora mostra o alto com a seta, o logo e o sino).
  Sobras da checagem, renderizadas com `--aceitar-camera` e conferidas na folha: cap01 3,9 s (faixa "Antes de usar o sistema" no pé, a câmera chega ~0,3 s depois), cap02 29,9 e 30,8 s, cap03 12,8 s ("Ver trilha" no cabeçalho, 1,2 s depois de um toque no pé: aparece em ~60%), cap04 3,75 s, cap07 49,4 e 50,7 s (itens da barra de baixo), cap08 16,6 s. Todos são trocas rápidas entre o alto e o pé da tela; o alvo entra em cena logo em seguida.
- **Folha de quadros a cada 3 s** (`folhas3s.sh`, 9 folhas, vistas inteiras): nada cortado de forma que atrapalhe (títulos de página rolando saem pela borda da janela, como num celular), nenhuma tela de computador reduzida, sem zoom brusco (a câmera só desliza), cada frase com a tela certa depois das correções acima. Valores fictícios da Assinatura ("R$ 1.350,00", "+R$ 100,00" dos módulos, "R$ 415,00" do Plano Master na janela de cancelar) aparecem como no 16:9: são a tela real do app (o plano libera "valores na tela e sem zoom"); a fala não cita preço.
- **Divergências do plano**: nenhuma tela trocada; `lead`/`group_gap` da câmera é novo; a frase do cap06 L10 cita "a busca" e no celular só existe o sino (a busca é do computador): a fala é a mesma nas duas versões, então ficou como está (pendência de texto, não de vídeo).
- Pendências: (a) fala do cap06 L10 "a busca e o sino" não vale à risca no celular; (b) conferir no player real se a legenda (<= 32 caracteres) fica na faixa y 1420-1600; (c) `entregar.py --unico` (720x1280) do vertical não rodado.
