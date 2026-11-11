# Briefing do robô e do ensaio · trilha EcoFlix (uma aula por agente)

Repositório da skill: `/home/claude/claude-tutorials` (caminhos relativos a ele); área de trabalho: `$TUT_HOME` =
`/home/claude/ecoflix`. **Objetivo**: deixar a aula pronta para a gravação final, que vem depois da voz: o robô de todos
os capítulos escrito por um gerador que prende cada gesto às palavras da fala, e o ensaio de todos os capítulos aprovado.
A voz ainda não existe: os tempos vêm de `capNN.json` **estimados**. Quando a voz chegar, roda-se o gerador de novo com o
`capNN.json` da voz e grava-se o final, sem reescrever nada. Sem aprovação no meio: termine e relate.

## O que já existe
- App EcoSistema 1.59.154 (build) em http://127.0.0.1:8080 e o Supabase falso padrão na 54340 (não use: veja "Sua
  instância"). Mundo da Recicla Vale Metais em `$TUT_HOME/rec/mundo` (cópia viva de `perfis/ecoflix/mundo`); comandos e
  o que fica onde: `/home/claude/ecoflix/RELIGAR.md`.
- A aula preparada por `bash planejamento/ecoflix/preparar_aula.sh Tnn`: `$TUT_HOME/rec/tNN` (kit do robô: `ensaio.py`,
  `resumo.py`, `prever.py`, `explorar.mjs`) e `$TUT_HOME/tNN/narracao` (`tts_textos.py` e `config_narracao.json` são
  atalhos para os do git; um `capMM.json` estimado por capítulo).
- O roteiro: `planejamento/ecoflix/Tnn/` (`plano.md` com "Mundo: o que esta aula precisa" e "Gravação"; `roteiro.md`, cuja
  coluna Tela é o roteiro do robô; `inventario.md` com os rótulos e as chamadas ao backend).
- **A junção do mundo pode mudar a fala da sua aula enquanto você trabalha**: antes do ensaio completo de cada capítulo,
  rode de novo o `preparar_aula.sh` e o seu gerador.

## Ler antes (só o necessário)
1. `docs/04-gravacao.md` inteiro e `docs/08-licoes.md` (o que custou tempo na Domiflix).
2. `perfis/ecoflix/PERFIL.md` (gravação e fala) e `/home/claude/ecoflix/RELIGAR.md`.
3. Da sua aula: `plano.md`, `roteiro.md`, `inventario.md`; em `planejamento/ecoflix/MUNDO_FICTICIO.md`, as seções "Decidido
   pelas aulas", "Semente do mundo base" e "Para a junção".
4. Gerador de referência da Domiflix, só a forma: `/home/claude/domiflix/rec/t14/gerar.py` (âncoras, rolagem, observador
   de avisos, sementes por capítulo).

## Sua instância (nunca a 54340 nem a de outro agente)
Porta = 54300 + o número da aula (T03 → 54303, T26 → 54326). `FAKE_NOW` do `plano.md` da aula (padrão
2026-11-10T08:30:00-03:00), igual no Supabase falso e no robô. `TUT_USER=rafael@reciclavalemetais.example` e uma
`TUT_SENHA` qualquer no ambiente, com 8 caracteres ou mais (o falso aceita qualquer uma, mas o formulário de login
recusa senha curta: a T05 perdeu dois ensaios com "x"; a senha nunca vai para arquivo).
```bash
cd /home/claude/ecoflix
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_PORT=54303 bash rec/run.sh fake
python3 -I rec/t03/ensaio.py 2
FAKE_NOW=2026-11-10T08:30:00-03:00 FAKE_URL=http://127.0.0.1:54303 bash rec/fila.sh --prio 03 -- node rec/record.mjs rec/t03/_ens/cap02.json --rapido --preset ultrafast --crf 30
```
Antes de cada gravação, confira que a instância ainda é a sua (`RELIGAR.md`). Mudou handler, hook ou `rec/mundo/lib`:
suba a sua instância de novo.

## Entregar
1. **`$TUT_HOME/rec/tNN/gerar.py`**: lê `$TUT_HOME/tNN/narracao/capMM.json` e escreve `rec/tNN/capMM.json` de todos os
   capítulos. Cada passo preso a uma palavra da fala (âncora = palavra menos o custo do gesto, docs/04 "Custo real dos
   gestos"), `mark` em cada linha, `label` em todo passo que a edição vai usar (zoom, destaque, aviso: as marcações
   `[ZOOM: ...]` do roteiro), login no `setup` com `"$TUT_USER"`/`"$TUT_SENHA"`.
2. **Estado de partida de cada capítulo**: sementes extras em `$TUT_HOME/rec/mundo/seeds-extra/tNN/` (ex.:
   `apos-cap03.json`), ligadas por `seedExtra`. O que o roteiro marca `[BACKEND: ...]` e o Supabase falso não tem vira
   handler novo em `rec/mundo/handlers/` (um arquivo por RPC ou function). Arquivo compartilhado (`rec/mundo/lib/eco.mjs`,
   `schema.json`, `mundo.json`, um handler que já existe): mudança mínima, só com Edit (nunca reescrever o arquivo), e
   conte no relatório. As sementes do mundo base (`rec/mundo/seeds/`, `gerar/`) são da junção: não mude.
3. **Ensaio aprovado de TODOS os capítulos**. Sempre o rápido (`ensaio.py` + `--rapido` + `resumo.py --ens`: 0 passo falho,
   nenhum "SEM ALVO", `pageIssues` vazio), gravado COM a montagem do MP4 (sem `--no-encode`) para ter a folha de contato
   (`<nome>.contact.jpg`) olhada: Recicla Vale Metais, versão 1.59.154, nenhum dado real, nenhum erro na tela que o roteiro
   não pede, nada cortado. E o `prever.py` com os tempos estimados.
   **O completo** (a gravação sem `--rapido`, `resumo.py`: `lateBy` < 0,8 s, gesto na palavra certa na coluna `voz:`) **só
   no capítulo que** (Kaik, 11/11 18:46: acelerar sem perder qualidade; a gravação final, com a voz, confere o resto):
   - o `prever.py` mostra com pouca folga (algum gesto previsto com atraso ≥ 0,4 s); ou
   - tem gesto sensível a espera: arrasto, menu ou lista aberta enquanto a fala anda, aviso que some sozinho, digitação
     longa, celular, dois navegadores, tela que recarrega ou muda sozinha; ou
   - teve qualquer aviso no rápido (passo refeito, alvo achado tarde, erro de console).
   No relatório, diga quais capítulos ficaram só no rápido. Completo que já passou não se grava de novo.
4. **`planejamento/ecoflix/Tnn/propostas_fala.md`**: o que a fala precisa mudar para bater com a tela ou caber no gesto
   (capítulo, linha, texto atual, texto novo, motivo) e, numa seção "Achados do app", bug ou rótulo diferente do
   roteiro. **Não edite `roteiro.md` nem `tts_textos.py`**: a revisão geral aplica tudo de uma vez.

## Regras
- Tudo na tela sai do app real 1.59.154: nenhuma tela, resultado ou função inventada; erro na tela só quando o roteiro
  pede (PERFIL → "Fala"). Dados do mundo fictício; nenhuma credencial na tela, em log ou em arquivo.
- Ritmo calmo, sem gesto brusco: o cursor chega na palavra; digitação no `cps` do docs/04; rolagem suave.
- **Uma tarefa pesada por vez, pela fila** (11/11: com o `flock` direto, 100 tarefas esperavam em ordem aleatória e
  algumas morriam no prazo sem rodar): TODO comando que abre navegador (gravação, ensaio, `explorar.mjs`, smoke) entra
  com `bash /home/claude/ecoflix/rec/fila.sh --prio NN -- <comando>`, NN = o número da aula, um capítulo por vez. A fila
  anda por prioridade (menor primeiro) e, na mesma prioridade, por ordem de chegada (`bash rec/fila.sh --ver` mostra).
  **No máximo uma tarefa sua na fila** (nada de laço de capítulos esperando nem tarefa repetida). Em segundo plano com o
  prazo máximo (7200000 ms); se morrer no prazo sem ter rodado, relance uma vez; se morrer de novo, pare e entregue o
  relatório parcial com os comandos exatos que faltam (o coordenador retoma quando a fila andar).
- **Um capítulo por chamada em segundo plano** (11/11 23:2x): cada capítulo espera 45 a 60 min na fila, e a chamada morre
  nas 2 h; um lote de vários capítulos numa chamada só roda 2 ou 3 e morre (a T13 parou achando que a fila tinha travado).
  Lance um capítulo, confira quando ele terminar e lance o próximo. Lote que morreu depois de rodar parte não é "morreu
  sem rodar": relance o resto e siga.
- **Esperar sem gastar** (11/11 23:59): o comando do capítulo (o `fila.sh ...`) é a própria chamada em segundo plano
  (`run_in_background`, prazo 7200000), e a notificação de término te acorda uma vez só. Nada de Monitor para esperar a fila:
  ele expira a cada 30 min e te acorda à toa (cada acordada relê o seu contexto inteiro). Relatório ao coordenador só no
  fim (ou parcial, se parar de vez); se precisar entregar algo ao acordar, uma linha basta.
- **MP4 de ensaio** (rápido ou completo) com `--preset ultrafast --crf 30` no `record.mjs`: serve só para a folha de
  contato e monta ~3x mais rápido dentro da trava. A gravação final volta ao padrão.
- **Disco quase cheio**: apague cada MP4 de ensaio e cada `*.contact.jpg` logo depois de olhar (fique com `actions.json` e
  `telemetry.json`, que o `prever.py` usa). Temporário grande vai para `/dev/shm`.
- Não mexa em `perfis/`, `ferramentas/`, outras aulas, `MUNDO_FICTICIO.md`, `PRODUCAO.md` nem no repositório do app (só
  leitura). Scripts auxiliares em `rec/tNN/` ou no seu scratch, com o prefixo da aula; nunca rode script de outro agente;
  não derrube instância de outro (nada de `pkill`/`killall`; a sua: `FAKE_PORT=543NN bash rec/run.sh down`).
- Não faça commit (o coordenador copia `rec/tNN` e `rec/mundo` para o git). Nada de `git stash`, `reset` ou `clean`; `rm`
  só com caminho absoluto literal. Salve cedo e com frequência; no fim, derrube a sua instância.

## Relatório final (até 250 palavras)
Capítulos aprovados e os que não fecharam (com o motivo); handlers e sementes novos; mudanças em arquivo compartilhado;
resumo das propostas de fala; achados do app; o que a gravação final vai precisar (FAKE_NOW, outro usuário, celular).
