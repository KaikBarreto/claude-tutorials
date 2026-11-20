# T19 · andamento da aplicação do 1.60.18 (20/11)

## Feito
- `narracao/tts_textos.py` e `roteiro.md` reescritos: 18 capítulos (eram 14), fala 2.062 → 3.146 palavras. Novos: 7 (folha CLT), 8 (férias e
  13º), 10 (relatório), 13 (tablet). Renumerados: extrato 7→9, ponto 8→11, celular 9→12, folha 10→14, config 11→15, arquivar 12→16, recap 13→17.
- `t19/narracao/capNN.json` estimados (`preparar_aula.sh T19`).
- Robô: `rec/t19/gerar.py` com os 18 capítulos (+ `fake_now.json`), `t19_sementes.py` (Marcos, Juliana), handlers só da T19
  (`rpc/set_ponto_pin.mjs`, `functions/time-clock-portal.mjs`), `t19_rodar.sh` (FAKE_NOW por capítulo, religa a 54319, tablet 1024x768),
  `t19_fila.sh` (copia a semente anterior se o capítulo não fecha).
- `plano.md`, `inventario.md` (bloco 1.60.18), `propostas_fala.md`, `cenas/ilustracoes.json` (6 novas, 12 renumeradas, `v3: pendente`).

## Falta
- cap. 13 (tablet): o ensaio para em "Tirar foto agora" (a tela do tablet pede a câmera/rosto depois de tocar no nome; conferir a câmera falsa no quiosque, `JS_CAMERA` é injetada antes da navegação SPA). Seeds apos-cap13 e apos-cap14 estão COPIADAS (aproximadas): refazer 13 e 14 com `--seed`.
- cap. 14: o campo "Data de início" da Ausência não aceita a digitação do robô (fica dd/mm/aaaa); o resto da folha passa. Ver `JS`/`digita` do `absence-start`.
- cap. 9: hover "Térmico" falha (opcional). cap. 12: marcar "Confirme localização" estoura (opcional).
- Voz de verdade: respiro de 4,5 s na L2 do cap. 11 (`pausas.py 11 <T>:4.5`, o `gerar.py` avisa o T) e reancorar com `python3 -I rec/t19/gerar.py`.
- Conferir na tela os números da fala dos caps. 6 e 7 (INSS, líquido) e do 8 (férias 3.733,33, 13º 1.050,00) antes da voz final.

## Comandos exatos
```
cd $TUT_HOME && export TUT_USER=rafael@reciclavalemetais.example TUT_SENHA=<8+ caracteres>
python3 -I rec/t19/gerar.py            # gera os 18 roteiros do robô e fake_now.json (LINT=1 lista palavra não achada sem abortar)
PRAZO_MIN=115 bash rec/t19/t19_fila.sh 02:ens,seed 03:ens,seed ... 16:ens,seed 17:ens   # cadeia de sementes, um capítulo por vez na fila
bash rec/t19/t19_rodar.sh NN --ens --final --seed                                       # um capítulo (final = gravação completa)
FAKE_PORT=54319 bash rec/run.sh down                                                    # ao terminar
```

## Ensaio
3 lotes rodados. Fechados no rápido (0 falhos): 0 a 8, 10, 11, 15, 16, 17; fechados com 1 passo opcional falho: 9, 12; não fecham: 13, 14. Só ensaio rápido; nenhum completo. Conferências tela x fala: 0 diferentes (INSS, líquido da folha CLT do Marcos e saldos batem com a fala).
