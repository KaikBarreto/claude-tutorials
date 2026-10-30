# 03 · Narração

## Gerar a voz
Qualquer TTS serve, desde que saia **um arquivo de áudio por capítulo** e você guarde **o texto exato** enviado
(é a fonte da verdade para alinhar a tela à fala). O padrão testado é o ElevenLabs:

- Voz natural de conversa (no piloto: **Fernanda - Natural Conversations**, modelo **eleven_v4**, idioma pt; ritmo
  pela pontuação, reticências e `[pause]`). Escolha a voz uma vez por série e mantenha.
- **Um fluxo por tutorial e um nó por capítulo** (no conector ElevenLabs: `creative_create_flow` +
  `creative_add_flow_node`/`creative_run_flow_nodes`). Duas versões por nó (o padrão); escolha a melhor ouvindo.
- Frases trocadas depois (correções): **um nó só** com todas as frases novas separadas por `[pause]`.
- Títulos falados das vinhetas de capítulo: **um nó** com os títulos separados por `[pause]` (só o título).
- Gerar custa crédito: **nunca repetir uma geração para "tentar de novo"**. Para acompanhar, consulte só as sessões
  que ainda estão na fila.
- O texto enviado por capítulo fica em `<tutorial>/narracao/tts_textos.py` (`CAPS = {"00": "...", ...}`).
  Exemplo: [`exemplos/dominex-t3/narracao/tts_textos.py`](../exemplos/dominex-t3/narracao/tts_textos.py).

## Receber os arquivos
Se o download direto do storage do TTS estiver bloqueado no ambiente, peça para a pessoa **exportar o fluxo inteiro
em zip** e anexar. Os nomes não importam: o `proc.py` descobre o capítulo pelo conteúdo. Se a exportação trouxer outra
versão de um capítulo já usado para sincronizar a gravação, mantenha a que foi usada.

## Configuração da narração — `<tutorial>/narracao/config_narracao.json`
```json
{
  "idioma": "pt_BR",
  "trocas": [["quê-érre côde", "QR Code"], ["rai-uól", "Hi-Wall"]],
  "unidades": {"V": "volts"},
  "numeros": [["dezoito mil btus", "18.000 BTUs"]],
  "asr_fix": {}
}
```
- `idioma`: idioma do `num2words` (o ASR escreve número em algarismo; o script volta para palavras para casar com o
  texto). O ASR (Parakeet v3) entende 25 idiomas europeus, incluindo português, inglês e espanhol.
- `trocas`: grafia da fala → grafia da legenda (mesmo número de palavras).
- `unidades`: sufixo que o ASR cola no número ("380V") → palavra falada.
- `numeros`: sequência falada (minúsculas, sem pontuação) → como aparece na legenda.
- `asr_fix`: correção pontual do que o ASR ouviu num take (`{id do take: {ouvido: certo}}`).
Modelo: [`modelos/config_narracao.json`](../modelos/config_narracao.json). Exemplo completo:
[`exemplos/dominex-t3/narracao/config_narracao.json`](../exemplos/dominex-t3/narracao/config_narracao.json).

## Conferir e cronometrar — `proc.py`
```bash
cd $TUT_HOME/<tutorial>/narracao
python3 -I proc.py recebido/*.mp3            # acha o capítulo, ASR (Silero VAD + Parakeet), alinha -> capNN.json
python3 -I proc.py 02=emendas/cap02_v2.wav   # força o capítulo de um arquivo
```
`capNN.json`: palavras na grafia da legenda (`w`) e como foram ditas (`fala`), tempos `s/e`, linhas (= linhas da tabela
do roteiro), frases e VAD. O script imprime as palavras vigiadas (as das `trocas`) e as que o ASR não achou. Palavra
"sumida" quase sempre é o ASR colando duas palavras: decodifique o trecho isolado e meça duração/picos de sílaba antes
de pedir regravação.

## Emendar frases trocadas — `emendar.py`
Coloca cada frase nova no lugar da antiga **sem mudar a duração do capítulo** (a gravação continua sincronizada):
a frase nova começa onde a antiga começava; o resto vira silêncio, depois cortado na montagem se a tela estiver
parada. Lista com as janelas de tempo: `trocas.json` (exemplo em `exemplos/dominex-t3/narracao/trocas.json`).
Volume casado por LUFS.

## Títulos das vinhetas — `titulos.py`
Separa o áudio dos títulos em `titulos/capNN.wav` (sem silêncio nas pontas, no volume da narração) e `titulos.json`
(texto + duração). A montagem estica a vinheta quando o título falado é longo.
