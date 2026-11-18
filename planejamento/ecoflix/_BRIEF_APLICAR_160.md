# Briefing de aplicação · trilha EcoFlix no app 1.60.10 (uma aula por agente)

Repositório da skill: `/home/claude/claude-tutorials` (caminhos relativos a ele); área de trabalho `$TUT_HOME` =
`/home/claude/ecoflix`. O app gravado agora é o **EcoSistema 1.60.10** (build em `$TUT_HOME/app/dist`, código só
leitura em `/dev/shm/ecoflix-src`). A aula já tem roteiro, fala e robô feitos para o 1.59.154, uma auditoria
(`Tnn/cobertura_160.md`) dizendo o que mudou e o que falta cobrir, e o resultado do robô antigo no app novo
(`planejamento/ecoflix/varredura_160/tNN.txt`). Pedido do Kaik: **cobrir cada função e caso de uso em detalhes; pode
ficar mais longo; nenhuma aula se divide; profundidade extra no fiscal.** **Tarefa**: deixar a aula pronta para a voz e
a gravação final no 1.60.10. Sem aprovação no meio: termine e relate.

## Ler (só isto)
1. `planejamento/ecoflix/Tnn/cobertura_160.md` inteiro; em `planejamento/ecoflix/JUNCAO_160.md`, a seção da sua aula e a
   tabela de números que mudaram; em `PRODUCAO.md`, só "Retomada de 18/11" (decisões do coordenador: valem sobre a
   cobertura quando divergirem).
2. `planejamento/ecoflix/_BRIEF_ROBO.md` (regras do robô, da fila e do ensaio: continuam valendo, com as trocas abaixo)
   e `perfis/ecoflix/PERFIL.md` → "Fala" e "Gravação".
3. Da aula: `roteiro.md`, `narracao/tts_textos.py`, `plano.md`, `inventario.md`, `propostas_fala.md` (se existir: as
   propostas antigas ainda válidas entram agora) e `$TUT_HOME/rec/tNN/gerar.py`.

## Fazer, nesta ordem
1. **Roteiro e fala** (agora você EDITA): aplique a cobertura no `roteiro.md` e no `narracao/tts_textos.py`: linhas que
   o app novo desmentiu, trechos novos e capítulos novos (numeração seguida; pode renumerar os capítulos, avisando).
   Atualize `plano.md` e `inventario.md` no que mudou. Regras da fala: português do Brasil falado, linguagem de cliente,
   sem travessão, número por extenso como o TTS lê, nunca preço de plano, nada inventado (rótulo copiado do código do
   1.60.10), erro na tela só quando ensina a resolver. Valor calculado (imposto, folha, saldo) só entra na fala depois de
   visto na tela no ensaio.
2. **Tempos**: `bash planejamento/ecoflix/preparar_aula.sh Tnn` (gera os `capNN.json` estimados dos capítulos novos).
3. **Robô**: atualize o `gerar.py` (capítulos novos, seletores e fluxos que mudaram), as sementes
   `rec/mundo/seeds-extra/tNN/` e os handlers que só a sua aula usa (um arquivo por RPC, espelhando a migration em
   `/dev/shm/ecoflix-src/supabase/migrations`). Mundo base e handlers compartilhados: só leitura (peça no relatório).
4. **Ensaio de todos os capítulos** como no `_BRIEF_ROBO.md` item 3 (rápido com MP4 e folha de contato olhada; completo só
   onde a regra pede), na sua instância 543NN, pela fila (`rec/fila.sh --prio NN`). **Um capítulo por chamada em segundo
   plano, e o comando do capítulo é a própria chamada (`run_in_background`, prazo 7200000). Nada de Monitor nem de laço
   de espera.** Capítulo que já passava na varredura e não mudou: basta o rápido.
5. **Ilustrações**: o estilo está sendo trocado (kit v3, aguardando o Kaik). NÃO construa cena. Só atualize
   `cenas/ilustracoes.json`: entradas novas ou alteradas com `cap`, `id`, `de`, `ate`, `resumo`, `mostra` (textos e
   números exatos) e `"clima": "fisico"` (pátio, caminhão, material, gente, papel) ou `"dados"` (conta, saldo,
   documento, fluxo do sistema), mais `"v3": "pendente"`. Ilustração só onde um conceito não se entende pela tela.
6. **Notas para retomar**: mantenha `planejamento/ecoflix/Tnn/andamento_160.md` curto e atualizado (feito, falta,
   comandos exatos). Se você for interrompido, outro agente continua dali.

## Limites
- Tudo na tela sai do app real 1.60.10; dados do mundo fictício; nenhuma credencial em arquivo (`TUT_SENHA` com 8+
  caracteres só no ambiente). Não mexa em `perfis/`, `ferramentas/`, outras aulas, `MUNDO_FICTICIO.md`, `JUNCAO_160.md`,
  `PRODUCAO.md`, mundo base nem no repositório do app. Sem commit. Nada de `pkill`/`killall`, `git
  stash/reset/clean/checkout`; `rm` só com caminho absoluto literal. No fim, derrube a sua instância.
- Economize contexto: não releia arquivo grande que já leu; não despeje log inteiro (use `tail`/`grep`).

## Relatório final (até 200 palavras)
Capítulos (total, novos, renumerados); palavras da fala antes → depois; ensaio (aprovados, só no rápido, o que não
fechou e por quê); sementes e handlers novos; pedidos ao mundo base; ilustrações novas listadas; achados do app para o
MELHORIAS (bug novo, e bug antigo da lista que o 1.60.10 corrigiu); o que depende do Kaik.
