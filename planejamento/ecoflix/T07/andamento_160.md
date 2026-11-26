# T07 · andamento da aplicação no app 1.60.22, tela 1600x900 (atualizado em 20/11) · PRONTA PARA A VOZ

## Reensaio no 1.60.22 (20/11, caps 15, 17 e 18)
- Rápido 15/17/18: 0 falho, maxLate 0. Completo: cap15 0 falho (maxLate 1,09; 1ª tentativa falhou porque o aviso agora é "Comprovante enviado para impressora"; `gerar.py` espera só "Comprovante enviado para"), cap17 0 falho (maxLate 6,12), cap18 0 falho (maxLate 6,83; máquina dividida).
- Cap15: cupom de 58 mm com o NOME dos materiais (Bateria automotiva, Cobre misto). Cap17: PDF sem preço nem total (0 "R$"). Cap18: fala inalterada, tela bate (pendência sai da lista, compra no caixa).
- Achados 1, 2 e 3 abaixo ficam RESOLVIDOS no 1.60.22. Instância 54307 derrubada.


Numeração (20 capítulos, 00 a 19) sem mudança desde 18/11: 09 Dois pedidos ao mesmo tempo, 10 Rascunho, 12 Abater o vale (novos do 1.60.10).

## Feito em 20/11 (1.60.10 → 1.60.18)
- **Fala (5 linhas, 3.557 → 3.628 palavras):** cap04 l.3 (+ margem automática, 1 frase); cap05 l.9 NOVA (coluna "Peso Bruto"); cap09 l.4 e l.5
  (janela nova "Atualizar os preços?": "Manter preços" / "Atualizar 1 preço", "Total dos itens"; só abre se algum preço muda, preço digitado não entra);
  cap18 l.4 (a faixa verde de sincronizado some em ~0,3 s: a fala passou a dizer que a pendência sai da lista e a compra já está no caixa).
  `roteiro.md`, `tts_textos.py`, `plano.md`, `inventario.md` (seção "1.60.18") e cabeçalhos (1600×900) atualizados.
- **Robô (`rec/t07/gerar.py`):** legenda da origem do preço com o seletor novo (`span[class*='max-w-[5rem]'][title]`; antes `span.truncate`), janela
  "Atualizar os preços?", cap05 com a coluna Peso Bruto, cap15 devolve o cupom (gancho de WebSocket do EcoTray, `js_cupom`), cap17 com diagnóstico do
  `hide_financial_details`, cap18 sem esperar a faixa verde e com o disparo da queda no início do capítulo.
- **Ensaio rápido: 20 de 20 com 0 falho** (lote 1: 19; lote 2: cap18 e cap19 depois da correção). `apos-cap18` gravada (nova); 19 usa ela.
- **Completos com 0 falho:** 05 08 09 10 13 15 16 17 18 (os demais já passaram em 18/11 e não mudaram: 06 07 11 12 14).
- `ilustracoes.json`: `ilu12_cupom` (cap15) agora `"tipo": "comprovante"`, `"cena": "pdf"`; nova `ilu17_sem_valores` (cap17, comprovante sem valores).
  Ambas com aviso de bug do app (abaixo).

## Atraso de gesto nos completos (máquina dividida; > 1 s anotado)
cap05 1,88 · cap09 1,45 · cap10 1,45 · cap13 2,31 · cap15 1,29 · cap16 1,12 · cap17 6,83 · cap18 6,8 (mesmo com a queda disparada no início do capítulo: a faixa "Sem conexão" só
sobe depois que um ping de rede em andamento estoura, até 8 s; o atraso fica no 1º gesto e se propaga). Reconferir na gravação final com a voz; se persistir,
considerar um capítulo-ponte sem fala antes do cap18 ou aceitar a faixa aparecendo com ~5 s de atraso.

## Achados do app 1.60.18 (para o MELHORIAS)
1. **Comprovante sem valores ignorado em "Visualizar PDF" da venda:** o app envia `hide_financial_details: true` na RPC, mas o PDF aberto logo depois de finalizar
   sai com preços e total (causa provável: `Sale.tsx` zera `hideFinancialDetailsRef` ao limpar o formulário e o Visualizar lê o ref depois). A fala do cap17
   ("o comprovante sai só com o material e o peso") só vale depois do conserto.
2. **Cupom térmico de 58 mm da compra mostra "Material não identificado"** nos itens (PDF devolvido pelo cap15; o nome do material não chega ao layout de 58 mm). Conferir
   em produção; a cena do cupom (`ilu12_cupom`) depende disso.
3. A faixa verde "Operações sincronizadas com sucesso!" some em ~0,3 s (sai junto com a última pendência): o cliente quase não vê.
4. Console: aviso `DialogContent requires a DialogTitle` (acessibilidade) em 1 capítulo.
- Bugs antigos do handoff que o 1.60.18 corrigiu e aparecem aqui: coluna "Peso Líquido" mostrando o bruto (agora "Peso Bruto", conferido no cap05); Valor/Kg 0,0032 e
  legenda "Preço informado" (cap16 confere a legenda e o preço de volta).

## Depende do Kaik / pedidos
- Corrigir os achados 1 e 2 antes da gravação final do cap15 e do cap17 (ou trocar essas cenas).
- Trava do peso manual com o EcoTray fechado ("Digitar peso (balança desconectada)" → "Liberar digitação"): preferência, não coberta (T05/T01).

## Comandos
```bash
cd /home/claude/ecoflix
bash /home/claude/claude-tutorials/planejamento/ecoflix/preparar_aula.sh T07
FAKE_NOW=2026-11-10T08:35:00-03:00 FAKE_PORT=54307 bash rec/run.sh fake      # só se for ensaiar de novo
TUT_SENHA=<8+> bash rec/t07/t07_lote160b.sh "<rápidos>" "<completos>"          # um lote pela fila (rec/fila.sh --prio 07)
FAKE_PORT=54307 bash rec/run.sh down                                           # instância derrubada em 20/11
```

## 25/11 · ilustrações v3 com a voz real 1.60.22
- Feitas 6 (`cena.html`): ilu00_dia, ilu04_preco, ilu06_pesagem (3D: tara, impureza, Bruto − Tara − Impureza = Líquido, dupla pesagem 412 − 96 = 316 kg), ilu09_formas, ilu12_cupom (papel real 58 mm #1760), ilu17_sem_valores (papel real 80 mm #1761). Tiradas 7 (a tela mostra). Auditoria 0, piscadas 0. Prévia `$TUT_HOME/previa_ilustracoes/T07_v3.mp4`. Papéis em `$TUT_HOME/t07/edit/out/comprovantes/`.
- **Para o fechamento**: na ilu06_pesagem os números 412, 96 e 316 aparecem antes da voz (a fala deles está na linha 4 do cap06, fora da janela). Estender a janela até a linha 4 ou prender a estação da dupla pesagem em `W(4, ...)`. O marca-texto do cupom15 foi posto por estimativa (o PDF não tem texto): conferir no quadro.

## 26/11 · fechamento da aula T07 (gravação final com a voz real 1.60.22, montagem e prévia)
- Gravação final dos 20 capítulos (`rec/t07/t07_final.sh`, 5 rodadas; cada capítulo mantido na melhor tentativa): 0 passos falhos em todos. maxLate por capítulo: 00 0,11 | 01 0,60 | 02 0,18 | 03 0,06 | 04 0,06 | 05 0,79 | 06 0,73 | 07 0,89 | 08 0,36 | 09 0,69 | 10 2,28 | 11 0,16 | 12 0,65 | 13 0,55 | 14 0,43 | 15 0,78 | 16 1,02 | 17 6,83 | 18 7,83 | 19 0,06.
- Atrasos que sobraram (robô limitado pelo app, sem como cortar fala): cap18 (a sincronização depois de "a internet volta" leva ~6,6 s para a pendência sair da lista) e cap17 (o clique em "Cobre misto" na lista de origem do estoque leva ~5,3 s); cap10, 16 e 07 entre 0,9 e 2,3 s por oscilação de carga entre rodadas.
- Alavancas usadas (todas em `rec/t07/gerar.py` e `auto_pausas.py`): parada mais curta do cursor (DWELL 0,4), passo que parte antes da palavra (ANTECIPA), hover sem mover o cursor (REGISTRA), respiros na voz em vãos reais de silêncio (`pausas_final.json`; originais em `narracao/emendas/`), `noScroll` no hover da faixa offline (cap18), correção da ordem das marcas (flush antes do `type`).
- Correções obrigatórias: (1) ilu06_pesagem sem números na estação 4 (a janela termina antes da linha 4; os números só aparecem na tela real, 412 com a fala "quatrocentos"; o 316 aparece ~2,6 s antes da fala "trezentos" porque o app o calcula ao digitar o 96); (2) marca-texto do cupom15 conferido nos quadros: material, peso, preço e pagamento no papel real #1760 (58 mm); (3) papel real #1760 na ilu12_cupom (7,1 a 27,95 s) e #1761 (80 mm) na ilu17, nada desenhado.
- Ilustrações refeitas depois das pausas de voz: ilu12_cupom e ilu17_sem_valores.
- Montagem: `fechar_t07.sh` (specs, 20 capítulos, auditar_camera com 0 problemas, finish, legendas). Ajustes nas ferramentas locais: `t07_mix.py` (voz em pedaços de 120 s, barramento de efeitos em float32, limitador em pedaços), `t07_music_bed.py` e `finish.py` (limitador em pedaços de 60 s) porque o limite de memória matava o processo.
- Resultado: `edit/out/T07/aula_final.mp4`, 1412,8 s (23,5 min), 1920x1080, -16,3 LUFS, pico -3,9 dBFS, 485 legendas (.srt/.vtt em `edit/out/T07/legendas/`), sem travessão.

## 26/11 (tarde) · correção dos caps 17 e 18 (tela atrás da voz)
- Diagnóstico: no cap18 o hover da faixa "Sem conexão" leva só 1,3 s; o atraso vinha da soma de cliques de ~1 a 1,4 s ancorados quase juntos na fala (Finalizar, Dinheiro, Confirmar, Voltar) e da espera de ~6,6 s da sincronização depois de "a internet volta". No cap17 o clique em "Cobre misto" (5,3 s, o robô rola a lista) estava ancorado em "puxo" e empurrava os quatro passos seguintes (Quantidade, 18 kg, coberta, Adicionar origem).
- `gerar.py`: cap17 clica "Cobre misto" na 1ª menção ("parte do cobre misto", `w=(3,'misto',0)`), não em "puxo"; ANTECIPA novo em 17 (Cobre misto 1,0; Quantidade 1,2; Finalizar 1,3; Pix 0,9) e 18 (até 1,9; zoom da quantidade 2,2); REGISTRA (hover sem mover o cursor, o zoom da câmera segue) em 17 (Quantidade coberta, Adicionar origem) e 18 (aviso offline, cartão da pendência, "pendência saiu"). `auto_pausas.py` não resolveu sozinho (parava no 1º atraso sem vão); simulação com `prever.py` + `pausas.py`.
- Respiros (T na linha do tempo ORIGINAL, `pausas_final.json`): cap17 5,64:1,8 | 7,67:2,2 | 11,16:1,1 | 29,18:3,2 (era 2,6); cap18 9,45:2,5 | 11,66:1,6 | 18,36:2,0 | 23,25:0,8 | 31,35:2,6 (os quatro últimos são novos; o de 31,35 cobre a sincronização).
- Gravação final (1 rodada cada, pela fila): cap17 maxLate 0,36 (era 6,83), cap18 maxLate 0,47 (era 7,83), 0 falhos, 0 DIFERENTE.
- Edição: `specs.json` com ilustração do cap17 em 79,67 (+0,6) e `acelera` (sempre fora das rampas de zoom da câmera, t_in 1,5 s e t_out 1,0 s; trechos mudos): cap17 [5,6-7,4 x3] e [36,3-37,45 x2]; cap18 [22,6-24,4 x2] e [38,4-40,7 x4]. Remonte completa (`remendar_aula.py` não aceita `acelera`): render dos caps 17 e 18 e `finish.py` com os outros 18 renders que já estavam em /dev/shm.
- Resultado: `edit/out/T07/aula_final.mp4` 1416,1 s (23,6 min), -16,3 LUFS, pico -3,8 dBFS, 485 legendas sem travessão; prévia 720p de 29,3 MiB (30.723.589 bytes) em `entrega_previa/`. Antes da troca, cópia do final e da prévia antigos em /dev/shm/t07_bak_r/final (apagar depois).
- Disco: / com 2,8 GB livres; /dev/shm com 5,6 GB (proj, video_sem_audio e out/capNN continuam lá, regeráveis).
