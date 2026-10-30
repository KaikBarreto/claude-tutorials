# claude-tutorials · manutenção da skill `tutorial-em-video`

Este repositório É a skill. Para produzir um tutorial, siga `SKILL.md`. Este arquivo é para quem mexe na skill.

- Português do Brasil em tudo (docs, mensagens dos scripts, comentários).
- Toda regra nova que sair de um tutorial entra em `docs/` (e em `docs/08-licoes.md` se custou tempo); regra de uma
  série entra no `PERFIL.md` dela. O perfil `domiflix` é o padrão do T3 congelado: **mudança visual ou sonora nele só
  com pedido do Kaik**, e depois de rodar `bash testes/identidade_domiflix.sh` (tem de continuar idêntico).
- Ferramentas novas ou alteradas: rodar no exemplo (`exemplos/dominex-t3`) antes de publicar; tarefas pesadas sob
  `flock $TUT_HOME/.heavy.lock`; nada de caminho absoluto de máquina (use a posição do script ou `TUT_HOME`).
- Nunca versionar mídia (mp4/wav/mp3), credenciais, tokens ou dados reais. O `.gitignore` já barra mídia.
- `SKILL.md` com menos de 500 linhas; detalhe vai para `docs/`. Frontmatter só com `name`, `description` (≤ 200
  caracteres) e `compatibility` (o app Claude recusa outras chaves). O `name` não pode conter "claude".
