# Briefing do levantamento · trilha Domiflix (vale para todos os tutoriais)

Objetivo: deixar cada tutorial da trilha **pronto para virar roteiro e gravação** no padrão do T3, sem depender de
memória de sessão. Tudo fica nesta pasta (`planejamento/domiflix/<Tnn>/`).

## Fontes (somente leitura)
- Código do app na versão de gravação **1.38.19**: `/home/claude/domiflix/src-1.38.19` (main `24f499ba`; a 1.38.6, base de T1, T4 e T5, segue em `src-1.38.6`).
  Nunca altere nada ali.
- Trilha oficial (validada na 1.22.5, pode estar desatualizada): `_referencia/trilha-de-tutoriais_v1.22.5.md`
  (capítulos, abertura/recap/próximo, ⚠️ pontos sensíveis, 🔒 módulos pagos, 🚫 não prometer, telas mortas,
  funções desligadas, coisas que parecem existir e não existem, telas só do painel da Dominex).
- Exemplo de levantamento completo (T3): `_referencia/T03_inventario_exemplo.md` (formato e nível de detalhe).
- Padrão de produção: `/home/claude/claude-tutorials/perfis/domiflix/PERFIL.md` e `docs/` (fala natural, só
  possibilidades, vinheta falada por capítulo, sem contador de etapas, dados fictícios, câmera no alvo da ação).
- Backend falso usado nas gravações: `/home/claude/domiflix/rec/fakebase` (`schema.json`, `seeds/`, `seeds-extra/t3/`,
  `handlers/{rpc,functions,ext}`, `desconhecidos.log` = chamadas que o T3 fez sem seed/handler).
- Mundo fictício do T3 (o que já existe quando o T4 começa): `exemplos/dominex-t3/roteiro.md` e
  `/home/claude/domiflix/rec/fakebase/seeds-extra/t3/apos-cap10.json` (estado final do T3) — empresa **Glacial Cold Brasil**
  (climatização), usuária **Camila Duarte** (admin), clientes (Colégio Monte Verde, Hotel Mirante do Mar, Pousada Sol
  Nascente, Marcos Antônio Braga...), fornecedor Ventura Gás e Tubos, equipamentos Hi-Wall 18.000 BTUs etc.

## Entregáveis por tutorial (`<Tnn>/`)
### `inventario.md` (300 a 800 linhas; cite `arquivo:linha` em tudo)
0. **Resumo para o roteiro**: capítulos da trilha × código de hoje (o que mudou desde a 1.22.5: telas renomeadas,
   novas, removidas; capítulo que não bate mais); o que mais pode surpreender.
1. **Rotas e navegação**: caminho no menu, URL, componentes principais.
2. **Permissões e módulos**: chaves e rótulos de permissão, módulos 🔒 que mudam o que aparece.
3. **Por tela / janela / aba**: rótulos EXATOS (botões, abas, campos, placeholders, títulos, estados vazios, toasts),
   obrigatórios, máscaras, preenchimentos automáticos, regras e o que acontece ao salvar/excluir.
4. **Backend por tela**: tabelas (select/insert/update/delete), RPCs, edge functions, buckets de storage e hosts
   externos chamados — é o que o backend falso precisa responder.
5. **Pegadinhas** para roteiro e gravação (bug, texto confuso, comportamento estranho) com `arquivo:linha`; marque as
   que valem virar **handoff de correção** para o time do app.
6. **🚫 Não prometer** e telas mortas/desligadas que tocam esta área.
7. **Dúvidas em aberto** (o que só dá para confirmar rodando o app).

### `plano.md` (80 a 180 linhas)
- Título final da aula, área(s) para as vinhetas (ex.: SERVIÇOS), objetivo numa frase, pré-requisito, próximo.
- **Capítulos propostos** no padrão (abertura, capítulos com transição falada, recapitulando, próximo): para cada um,
  título curto da vinheta, o que a tela mostra (telas e ações, rótulos entre aspas), avisos na tela (positivos),
  ilustração só se o conceito não aparece na tela, estimativa de duração em fala natural (o T3 deu ~1 min por
  capítulo de cadastro).
- **Mundo fictício**: o que precisa existir no começo (herdado dos tutoriais anteriores), o que esta aula cria
  (nomes e valores fictícios plausíveis para uma empresa de climatização), o que fica para as próximas.
- **Gravação**: tudo no modo fakebase; o que o backend falso já cobre e **o que falta** (seeds, RPCs, edge functions,
  hosts externos, storage, PDFs, links públicos); telas no celular ou visão do técnico (viewport diferente) se houver.
- **Pronúncias** novas para o TTS (siglas e termos: escreva como a Fernanda deve ler).
- **Riscos e decisões para o Kaik** (módulo pago, integração externa real, tela mobile, algo que o app não faz).

## Regras
- Português do Brasil. Nada inventado: tudo sai do código (com `arquivo:linha`) ou fica em "dúvidas".
- Só possibilidades na fala proposta; nada de "o sistema não faz X" nas falas (isso vai para 🚫 ou pegadinhas).
- ⚠️ da trilha (Kaik, 30/10 20:56): a fala pode informar o que dá errado se a pessoa não fizer, mas focada na
  possibilidade: primeiro o caminho certo, depois a consequência numa frase ("é só carregar o certificado aqui: é ele
  que libera a emissão"). Nunca encenar a falha na tela; avisos normais do fluxo (confirmações) podem aparecer.
- Dados sempre fictícios; nenhum segredo, token ou dado real nos arquivos.
- Escreva SÓ dentro das suas pastas `<Tnn>/`. Não mexa no código do app, no backend falso nem em outros arquivos.
- Sem commit/push.
