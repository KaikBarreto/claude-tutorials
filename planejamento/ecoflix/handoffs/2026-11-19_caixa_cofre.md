---
kind: "handoff"
workspace_id: "afeff998-21f8-415d-baa6-87c3549f0b98"
workspace_path: "/Users/kaikbarreto/conductor/workspaces/EcoSistemaSaaS/dhaka"
runtime: "claude"
persona: "CEO"
destination: "pendente"
title: "Tutoriais/Guia: abertura de caixa zerada com cofre negativo + modal Saldo insuficiente mudou (main a3183ebee)"
created_at: "2026-11-19T19:09:15Z"
---

PARA: a sessão que cuida dos tutoriais (EcoFlix) e do Guia Técnico. Pedido do Kaik em 19/11/2026.
Tudo abaixo já está no `main` — commit `a3183ebee` (fix(caixa)), SEM bump de versão e sem changelog.
Trate as linhas como referência de hoje; confirme no arquivo antes de citar.

## O que mudou no produto (tela `/caixa`, abertura de caixa)

1. REGRA — abrir caixa ZERADO nunca é barrado pelo cofre.
   Antes: a trava era `valor de abertura > disponível do cofre`. Com o cofre NEGATIVO (ex.: disponível
   R$ -1.241,16), abrir com R$ 0,00 caía no aviso "Saldo insuficiente em dinheiro".
   Agora: abertura R$ 0,00 passa sempre (não reserva nada do cofre). Abertura acima de zero e acima do
   disponível continua barrando igual. Primeira abertura / cofre recém-ligado (semente) NÃO mudou.
   Onde: `src/lib/caixa.ts` → `deveBloquearAberturaPorCofre` (~linha 88); usada em
   `src/pages/Caixa.tsx` ~linha 1747. Testes: `src/lib/caixa.test.ts`.

2. MODAL "Saldo insuficiente em dinheiro" (`src/pages/Caixa.tsx` ~linhas 3747-3845):
   a. Link novo, nos dois perfis (com e sem permissão de ajustar contas), acima dos botões:
      "Ver tutorial: como funciona o dinheiro do caixa" (ícone de play, abre em NOVA ABA).
   b. Quando o disponível é ZERO ou NEGATIVO:
      - texto: "Você tentou abrir com R$ 100,00, mas o cofre está negativo em R$ 1.241,16 e não há
        dinheiro disponível (R$ 92.785,62 já reservados em caixas abertos)." (só no negativo; com
        zero ou positivo segue "mas há apenas R$ X disponíveis");
      - botão secundário vira "Abrir zerado (R$ 0,00)" (antes: "Usar disponível (R$ -1.241,16)", que
        preenchia a abertura com valor negativo). Ele só preenche o campo com 0,00 e fecha o aviso;
        o operador ainda clica em "Abrir Caixa";
      - perfil sem permissão: "Peça ao responsável para ajustar o saldo do dinheiro nas Movimentações
        Financeiras, ou abra o caixa zerado (R$ 0,00)." (antes: "ou abra com valor menor (até R$ -X)").
   c. Com disponível POSITIVO nada mudou: botão "Usar disponível (R$ X)" e textos de antes.

## Para onde o link aponta — e o que VOCÊ precisa manter

`src/lib/caixa.ts` ~linha 99:
`TUTORIAL_DINHEIRO_FISICO_URL = "/ecoflix/assistir/caixa-compras-e-vendas/5?trilha=tutoriais-do-sistema"`
Hoje isso abre a aula 5.5 "Cofre e rastreabilidade do dinheiro", do início (conferido no navegador).
É o ÚNICO lugar a trocar. Quando a EcoFlix virar um tutorial por módulo (o Kaik avisou que vem em
breve): se o slug `caixa-compras-e-vendas`, o número da aula ou a trilha `tutoriais-do-sistema`
mudarem, ATUALIZE essa constante no mesmo commit — senão o cliente que clicar no aviso cai em
"O endereço pode ter mudado". Se o novo tutorial de Caixa for um vídeo único, vale apontar com o
segundo de início do trecho do cofre (`/ecoflix/assistir/<slug>/<n>/<segundos>`).

## Conteúdo que ficou desatualizado

- Guia Técnico, seção T6, capítulo 5 "O aviso de saldo insuficiente em dinheiro e as duas saídas"
  (`docs/guia-suporte/secoes/T6.html` ~linha 104; chunk `t6-c05` em `public/guia-tecnico/chunks.jsonl`;
  derivados: `public/guia-tecnico/guia.md`, `index.html`, `src/components/help-center/helpCenterData.generated.ts`
  e a tabela `guia_chunks`). Falta dizer: (i) caixa zerado abre mesmo com cofre negativo/sem saldo;
  (ii) o caso do cofre negativo, com o texto e o botão "Abrir zerado (R$ 0,00)"; (iii) o link do tutorial.
- Divergência que JÁ existia e não é deste commit: o guia chama o botão de "Abrir com valor menor";
  na tela ele se chama "Usar disponível (R$ X)". Vale corrigir junto.
- Aula 5.5 da EcoFlix: se ela mostra/menciona que abrir zerado é barrado, ou mostra o botão
  "Usar disponível" com cofre negativo, o trecho envelheceu. Não assisti ao vídeo — conferir.

## Prints prontos (tela real, conta de teste)
- `/Users/kaikbarreto/conductor/workspaces/EcoSistemaSaaS/dhaka/.context/qa-modal-cofre-negativo.png` (desktop)
- `/Users/kaikbarreto/conductor/workspaces/EcoSistemaSaaS/dhaka/.context/qa-modal-celular.png` (390px)
São de QA, não de material final. Ficam no `.context` do workspace `dhaka` — copie se for usar, o
workspace pode ser arquivado.

## Como reproduzir sem gravar nada
Receita na memória `reference_qa_de_abertura_de_caixa_na_conta_de_teste.md` (seção 19/11/2026):
`/caixa` → Início → Abrir Caixa, interceptando o `fetch` de gravação e simulando o `disponivel`.
O cofre da conta de teste muda ao vivo (foi de -1.241,16 a +2.777.294,39 durante o QA), então
simule o saldo em vez de confiar no real.
