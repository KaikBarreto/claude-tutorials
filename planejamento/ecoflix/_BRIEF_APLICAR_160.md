# Briefing de aplicação · trilha EcoFlix no app 1.60.10 (uma aula por agente)

Repositório da skill: `/home/claude/claude-tutorials` (caminhos relativos a ele); área de trabalho `$TUT_HOME` =
`/home/claude/ecoflix`. O app gravado agora é o **EcoSistema 1.60.10** (build em `$TUT_HOME/app/dist`, código só
leitura em `/dev/shm/ecoflix-src`). A aula já tem roteiro, fala e robô feitos para o 1.59.154, uma auditoria
(`Tnn/cobertura_160.md`) dizendo o que mudou e o que falta cobrir, e o resultado do robô antigo no app novo
(`planejamento/ecoflix/varredura_160/tNN.txt`). Pedido do Kaik: **cobrir cada função e caso de uso em detalhes; pode
ficar mais longo; nenhuma aula se divide; profundidade extra no fiscal.** **Tarefa**: deixar a aula pronta para a voz e
a gravação final no 1.60.10. Sem aprovação no meio: termine e relate.

## Valem por cima de tudo abaixo (20/11)
- **App de gravação: 1.60.22** (20/11 15:xx, commit `bea545ecf`; antes 1.60.18 `e8edc9e6d`, cópia em `/dev/shm/ecoflix-src-1.60.18`). Mudou do 1.60.18: comprovante sem valores e cupom 58 mm (T07), faixa de sincronizado 3 s, pagamento retroativo de funcionário (T19), DANFE real na pré-visualização, lupa de CNPJ na Configuração Fiscal e 539 (T16/T17), ticket avulso → padrão limpa o parceiro (T08), aviso de conta sem empresa no login. Onde abaixo diz 1.60.18, leia 1.60.22.
- **O app agora é o 1.60.18** (commit `e8edc9e6d`; build em `$TUT_HOME/app/dist`; código só leitura em `/dev/shm/ecoflix-src`).
  Onde está escrito 1.60.10 abaixo, leia 1.60.18. O robô de toda aula já aponta para 1.60.18.
- **Tela da gravação: 1600x900** (16:9, escolha do Kaik; já é o padrão em `rec/mundo/mundo.json -> navegador.tela`).
  Telas mais largas: confira na folha de contato o que mudou de lugar (painel lateral, colunas, menus).
- **O que mudou no app desde o 1.60.10** está em `planejamento/ecoflix/handoffs/` (leia os 3: correções do nosso handoff,
  fiscal e caixa/cofre) e a novidade **margem automática** (T03): Materiais > Editar Preços em tela cheia, chave
  "Margem automática" (uma margem para a tabela ou uma por material, em % ou R$ por quilo), resumo com "Venda abaixo da
  compra", "Sem preço" e "Margem típica", calculadora no preço de venda do cadastro; a margem é sempre sobre a compra.
  Confirme cada rótulo no código antes de pôr na fala. **Não anunciar**: a nota de teste (homologação) é liberada por
  CNPJ; o modelo novo da DANFE só vale em produção a partir de 01/12/2026.
- **Resultado do robô atual no 1.60.18**: `planejamento/ecoflix/varredura_160/VARREDURA_1.60.18.md` (a seção da sua aula).
- **Sementes antigas podem estar velhas**: o app novo grava campos que o antigo não gravava (ex.: T08, item com só a 1ª
  pesagem passou a guardar `first_weight`, commit `4d19302a3`). Se uma tela reaberta de semente sair diferente do que o
  app faz ao vivo, corrija a semente.
- **PDF e comprovante aparecem na tela** (pedido do Kaik, 19/11): o app abre PDF em aba nova e a gravação filma uma aba
  só. Toda fala que fala de um PDF/comprovante/relatório impresso precisa que o robô devolva o PDF (padrão `POPS` +
  `PDF_JS` do `$TUT_HOME/rec/t08/gerar.py`) e de uma entrada no `cenas/ilustracoes.json` com `"tipo": "comprovante"`,
  `"cena": "pdf"`, a janela da fala e, em `mostra`, os campos que a voz cita. A cena em si o coordenador faz.
- **Ensaio**: o lote em segundo plano usa SÓ a fila (`rec/fila.sh`); nunca rode `record.mjs` fora dela (19/11: um
  ensaio fora da fila junto com a gravação final deu 16 s de atraso).

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
4. **Ensaio de todos os capítulos, em LOTE** (regra de economia de 18/11: cada vez que você acorda relê o contexto
   inteiro, então acorde pouco). Termine primeiro TODAS as edições de todos os capítulos (passos 1 a 3). Depois lance UM
   script em segundo plano (`run_in_background`, prazo 7200000) que ensaia em sequência todos os capítulos (cada um pela
   fila `rec/fila.sh --prio NN`, rápido com MP4 `--preset ultrafast --crf 30`, `resumo.py --ens` e `prever.py` gravados em
   arquivo; religando a instância 543NN se o `FAKE_NOW` do capítulo mudar) e só olhe quando o lote inteiro terminar
   (resumos por `grep`/`tail`, folhas de contato juntas). Corrija tudo de uma vez; segundo lote só com os que falharam e
   com os completos que o `_BRIEF_ROBO.md` item 3 pede. No máximo 3 lotes: o que não fechar vai no relatório com o comando
   exato. Nada de Monitor, de laço de espera nem de relatório intermediário.
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
