# Andamento T15 · aplicação do 1.60.18

**Feito:** roteiro (17 capítulos) e `narracao/tts_textos.py` (3.392 palavras, sem travessão); `config_narracao.json` (trocas
DFC, EBITDA, CSV); `rec/t15/gerar.py` (16 capítulos do robô, todos geram sem aviso); sementes (`lote-categoria`) e 5 handlers
novos; `fake_now.json`; `cenas/ilustracoes.json` (11 entradas, 2 novas); `cenas/tempos`; `plano.md`, `inventario.md`.
**Falta:** resultado do ensaio em lote (rodando); conferir valores falados da DFC e do Pátio na tela; afinar o seletor da coluna
do gráfico (cap03, placeholder `.recharts-bar-rectangle >> nth=0`); salvar o PDF do cap15 e refinar `mostra` de `ilu15_historico_pdf`.

**Comandos**
- Lote: `cd /home/claude/ecoflix && export TUT_SENHA=... && nohup bash rec/t15/t15_lote.sh 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 > rec/t15/_ens/lote_geral.log 2>&1 &`
- Resultado: `ls rec/t15/_ens | grep lote_`; `tail rec/t15/_ens/lote_NN.txt prever_NN.txt`; fim: `lote_FIM.txt`.
- Derrubar a instância: `FAKE_PORT=54315 bash rec/run.sh down`.
- Regerar robô: `cd` scratchpad `t15x` e `python3 patch_gerar.py`; texto: `python3 edit_texto.py`.
**Pedido ao mundo base:** `bank_account_id/name` em `linhasDRE`.

**Estado (20/11, fim):** dois lotes rodados; os 16 capítulos (00 a 15) passam no ensaio sem passo falho nem tela diferente da fala.
Correções: cap01 foco no campo Nome antes de digitar; cap03 coluna vermelha (despesas) do gráfico + espera pelo placeholder da busca;
cap06 sem abrir centro de custo (o DRE padrão do 1.60.18 não mostra) e fala da linha 7 trocada; cap07 clica no grupo 06.02; cap08 fala
da faixa cinza; cap11 semente `t15/previsto` (água vencida, telefone); cap12 setup por 'Saldo atual' + confere da variação; cap14 espera
'Editar categoria'. Mundo: `linhasDRE` com bank_account_id/name; `t15/inicio` com created_at do bt.135 (Registrado em).
Falta: gerar a voz; gravação final. Instância 54315 derrubada. `ilustracoes.json`: mostra do PDF atualizado.
Sobras em rec/t15/_ens: MP4 e folhas de contato dos ensaios (apagar à mão, caminho a caminho).

## 21/11 · ilustrações v3 prontas (para o fechamento)
- 5 cenas escuras em `T15/cenas_v3/cena.html` (cap00 L1, cap01 L11-13, cap02 L1, cap08 L3-7 com as contas do pátio, cap13 L8); 5 tiradas (a tela mostra). Auditoria 0.
- **No fechamento**: `ilu07_patio` ainda tem 1 piscada (39,37 s, tremor do texto da tabela cheia): zerar antes de encaixar. cap15 L2 "O PDF é pra mandar pro contador ou guardar.": capturar o PDF do Histórico na gravação final e mostrar o papel real (cena `pdf`); se não sair, a tela mostra o menu Exportar com PDF e Excel.

## 27/11 · fechamento (gravação final, montagem, render)
- Voz real conferida; 16 capítulos gravados (maxLate < 0,8 s em todos), regravações pontuais de cap06, cap07 e cap14 por âncora (gerar.py).
- PDF real capturado do Histórico (`out/comprovantes/cap15-historico.*`); cena `pdf` mostra o papel real (nunca desenhado) em cap15 L2.
- `ilu07_patio`: `respira: 0` no cap 8; 0 piscadas. cap16 = recapitulação montada de clipes reais (`rec/t15/t15_montagem_cap16.py`).
- Entrega: `out/T15/aula_final.mp4` (21:52, 1920x1080, -16,3 LUFS, pico -3,8 dB, 0 travessão nas legendas), `.srt`/`.vtt`, prévia 720p em `entrega_previa/`.
- Lições: o limite de memória do cgroup (~6 GB, inclui /dev/shm) matava Python em mix/limiter/finish; resolvido com processamento em blocos, float32 e capítulos renderizados em disco.
