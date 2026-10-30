# Briefing da voz · trilha Domiflix (gerar no ElevenLabs um lote de aulas)

Padrão: `perfis/domiflix/voz.json` (Fernanda - Natural Conversations, `voice_id` KHmfNHtEjHhLK9eER20w, modelo
`eleven_v4`, `language_code` "pt", sem mexer em voice_settings) e `docs/03-narracao.md`.

**Pedido do Kaik (30/10 23:13): tudo num fluxo só, para ele baixar de uma vez; UMA versão por fala (gastar o
mínimo); se alguma fala ficar ruim, regera só ela.** Modelo: `eleven_v4` (mesma voz do T3/T0; o v3 custa o mesmo por
caractere, ~1 crédito).

## Para cada lote (ex.: T1, T4, T5, T7)
1. Usar o fluxo único **`Domiflix · Vozes de todas as aulas`** (id em `PRODUCAO.md` → "Voz"); só criar se ainda não
   existir.
2. Para cada aula do lote, ler `planejamento/domiflix/Tnn/narracao/tts_textos.py` e criar com `creative_add_flow_node`
   (node_type `tts`, model_id `eleven_v4`, voice_id acima, model_parameters `{"language_code": "pt"}`):
   - um nó por capítulo, `label` = `Tnn capMM <título curto>` (ex.: `T04 cap03 Checklists`), `prompt` = `CAPS[MM]`
     **exatamente** como está no arquivo (com as quebras de linha);
   - um nó de títulos, `label` = `Tnn títulos`, `prompt` = os `TITULOS` na ordem, separados por ` [pause] `.
   O rótulo vira o nome do arquivo no zip exportado: é por ele que se separa cada aula.
3. `creative_run_flow_nodes` com todos os nós do lote (até 20 por chamada; mais que isso, em chamadas separadas),
   com **`generations_count: 1`** (pedido do Kaik). Nunca repetir uma geração para "tentar de novo".
4. Acompanhar com `creative_get_flow_run_status` passando **só as sessões ainda pendentes** (a resposta é grande).
   Falha de concorrência ("concurrency limit") se resolve sozinha: só esperar.
5. Registrar em `planejamento/domiflix/Tnn/narracao/nos_elevenlabs.json`: flow_id, url do fluxo (sem `oobCode`),
   e por capítulo `{node, sessions, duracoes}`; e na tabela "Voz: lotes e exportação" de `PRODUCAO.md`.

## Relatório (≤ 120 palavras)
Fluxo (id e url sem `oobCode`), nós criados por aula, duração total gerada por aula (da primeira versão), créditos
aproximados, falhas (se houver). Nada de colar URLs assinadas de áudio.
