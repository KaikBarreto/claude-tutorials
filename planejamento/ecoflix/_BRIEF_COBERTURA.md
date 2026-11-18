# Briefing da auditoria de cobertura · trilha EcoFlix (uma aula por agente, só leitura de código)

O app passou do 1.59.154 (commit `f37573ea0`) para o **1.60.10** (`5290be4cd`), e o Kaik pediu (18/11): "todos os
tutoriais cubram tudo em detalhes, não tem problema ficar um pouco mais longo e explicar bem as coisas, principalmente na
parte fiscal, e cobrir cada função e o máximo de casos de uso pertinente". **Tarefa**: dizer o que a aula precisa mudar
para (a) bater com o 1.60.10 e (b) cobrir cada função e caso de uso das telas dela. Sem aprovação no meio.

## Onde está cada coisa
- Código do app 1.60.10 (só leitura, sem `.git`): `/dev/shm/ecoflix-src`. O que mudou desde a versão do roteiro:
  `git -C /home/claude/ecosistema2-f3f6b533 diff f37573ea0 5290be4cd -- <arquivo>` (repositório só leitura: nada de
  checkout, só `diff`, `show`, `log`). Notas de versão para o cliente: `src/config/version.ts` (de 1.59.155 a 1.60.10).
- A aula: `/home/claude/claude-tutorials/planejamento/ecoflix/Tnn/` (`plano.md`, `roteiro.md`, `inventario.md` com as
  telas e os arquivos do app, `propostas_fala.md` se existir) e a fala em `narracao/tts_textos.py`.
- Mundo fictício: `planejamento/ecoflix/MUNDO_FICTICIO.md` (nomes e números; nada de dado real).
- Resultado da varredura do robô no app novo, se já existir: `/home/claude/ecoflix/rec/varredura/tNN.txt`.

## Entregar: `planejamento/ecoflix/Tnn/cobertura_160.md` (um arquivo, direto ao ponto)
1. **Mudou no app** (por capítulo): rótulo, botão, campo, fluxo ou tela que o roteiro mostra e que no 1.60.10 está
   diferente, com o texto exato novo (copiado do código) e o arquivo:linha. O que não mudou não entra.
2. **Falta cobrir**: função, opção, aba, filtro, ação de menu, aviso ou caso de uso das telas desta aula que o 1.60.10
   tem e o roteiro não mostra. Para cada um: o que é, quando o cliente usa, e se vale capítulo/trecho (sim, só citar, ou
   não, com o motivo). Não invente: só o que está no código. Função de outra aula: diga qual aula e não repita.
3. **Proposta**: capítulos novos ou trechos a acrescentar, cada um com título, a coluna Tela (passos com os rótulos
   exatos) e a fala no tom da aula (português do Brasil, linguagem de cliente, sem travessão, sem preço de plano,
   número por extenso só quando a fala lê). Diga o que o mundo fictício precisa ter (dado, handler RPC) para gravar.
4. **Estimativa**: segundos de fala a mais e capítulos novos.

## Limites
- Não edite `roteiro.md`, `tts_textos.py`, `plano.md` nem nada fora do seu `cobertura_160.md`. Não abra navegador nem
  rode o robô (a máquina está ocupada). Não faça commit. Nada de `git stash/reset/clean/checkout`.
- Economize: leia só os arquivos das telas da aula (o `inventario.md` aponta), não o repositório inteiro.

## Relatório final (até 120 palavras)
Quantas mudanças do app, quantas lacunas, capítulos novos propostos, segundos a mais, e o que depende de decisão.
