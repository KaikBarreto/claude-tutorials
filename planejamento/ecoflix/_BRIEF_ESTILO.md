# Briefing do estilo saturado nas cenas da EcoFlix (pedido do Kaik, 11/11 12:20)

> "nessas ilustrações as etapas mostram com o ícone escuro sobre o verde, devia ser branco / E em vários lugares estão com
> badges dessaturados com texto saturado, tem que ser saturados com ícone branco / tipo em quadrados atrás de ícones,
> badges, etc. / substitua em tudo"

Repositório: `/home/claude/claude-tutorials`. As cenas de cada aula estão em `planejamento/ecoflix/Tnn/cenas/cenas.html`
(com `ilustracoes.json` e `tempos/`). O kit é `perfis/ecoflix/cenas/cenas_ecoflix.html`.

## A regra
- **Elemento pequeno** (selo, chip, etiqueta, pílula, quadrado ou círculo atrás de ícone, círculo de etapa, bolinha de
  número, marcador de status): **fundo cheio saturado e ícone/texto branco**. Cores: verde `var(--vs)` (#16A34A, o verde
  do próprio sistema), âmbar `var(--as)` (#D97706), vermelho `var(--rs)` (#DC2626); neutro: `#4B5563` com branco.
- Nunca fundo claro com ícone ou texto colorido; nunca ícone escuro sobre verde.
- **Continua como está**: cartões, painéis grandes, fundo da cena, desenhos (caminhão, cofre, balança...), linhas e setas,
  títulos, o verde da marca (#50D088) em barras, contornos e preenchimentos sem texto em cima.
- As classes do kit `.ico`, `.ico.a`, `.tag.v` e `.tag.a` já mudaram pelo bloco `<style id="saturado">` no fim do `<head>`
  de cada `cenas.html` (não mexa nele). Falta o que a aula fez com estilo próprio (inline no JS ou classe da aula): procure
  `var(--vc)`, `var(--ac)`, `var(--vm)`, fundos claros em hex ou rgba e ícones/textos escuros sobre `var(--v)`.

## Fazer, por aula
1. Ajustar no `cenas.html` da aula só cor de fundo e cor do conteúdo desses elementos (sem mudar posição, tamanho, texto,
   âncora ou tempo).
2. Conferir: `python3 -I planejamento/ecoflix/folha_cenas.py Tnn` (quadro final de cada cena; usa a trava leve
   `.stills.lock` com `nice -n 19`, sem disputar com as gravações; rode em segundo plano e espere a notificação) e olhar a folha `/home/claude/ecoflix/previa_ilustracoes/Tnn_cenas.jpg`.
   Elemento que ficou ilegível ou estranho: corrigir e gerar de novo. Essa folha é a que vai para o Kaik.

## Limites
Só os `cenas.html` das suas aulas. Não mexa em `perfis/`, `ferramentas/`, roteiro, fala, outras aulas nem no app. Não faça
commit. Nada de `pkill`/`killall`, `git stash`, `reset` ou `clean`; `rm` só com caminho absoluto literal. Economize tokens:
leia o `cenas.html` uma vez, procure com grep, não releia à toa.

## Relatório (até 120 palavras)
Por aula: quantos elementos mudaram e onde; o que ficou em dúvida.
