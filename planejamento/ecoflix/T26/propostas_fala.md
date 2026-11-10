# Propostas de fala · T26 · CRM/Kanban

Do robô e do ensaio (10/11/2026, app 1.59.154, voz ESTIMADA). A revisão geral aplica em `roteiro.md` e `narracao/tts_textos.py`;
nada aqui foi aplicado. Robô: `$TUT_HOME/rec/t26/gerar.py` (lê `t26/narracao/capNN.json`).

## Mudanças de fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 08 | L4 | O responsável fica em branco por enquanto. | O responsável já vem preenchido com quem está criando. Por enquanto, eu deixo sem responsável. | Na criação, "Responsável" já vem com o usuário logado (`OpportunityFormDialog.tsx:124-125`): o robô troca para "Sem responsável" (o cartão precisa nascer sem dono para a trava do cap09 mostrar as duas pendências). Com a fala atual a tela mostra "Rafael Nogueira" e a fala diz "em branco". |

## Respiros (pausas na voz, `pausas.py`, para os cortes)

| Cap. | Onde | Quanto | Motivo |
|---|---|---|---|
| 09 | entre a L1 ("...até Em contato.") e a L2 ("Repara: ...") | vão total de 3,4 s (`pausas.py 09 <fim da L1>:<3,4 - vão atual>`) | Corte: o selo de tarefas abertas não se atualiza depois do arraste (achado 3); o robô sai e volta ao CRM e a tela remonta com o selo "1". A montagem corta o trecho. |
| 09 | entre a L3 ("...Defina um responsável.") e a L4 ("O cartão continua...") | vão total de 3,4 s | Corte: depois da trava o cartão fica desenhado em "Visita técnica" (achado 1); o robô fecha o aviso, sai e volta ao CRM e o cartão aparece em "Em contato". A montagem corta o trecho. |

Com a voz estimada, o `gerar.py` já desloca as linhas seguintes e avisa "RESPIRO PENDENTE" com o comando; quando a voz de verdade
tiver o vão, o aviso some.

## Achados do app (1.59.154)

- **Responsável pré-preenchido na Nova oportunidade**: a janela abre com o usuário logado em "Responsável" (o roteiro e o inventário
  falam em "Sem responsável").
- **Rótulos diferentes para o mesmo campo**: o formulário chama `contact_role` de "Área/Setor"; a ficha mostra "Cargo do contato".
- **A 1280 px com o menu lateral aberto** o cartão "Total de oportunidades" sai cortado ("Total de oportuni...") e o quadro mostra
  3,5 colunas: os capítulos 2 a 13 recolhem o menu no setup (fora do vídeo); os caps 0 e 1 mostram o menu (o item "CRM/Kanban").
- **"Orientação para o time"**: "Salvar etapa" fecha a janela, e o texto só existe nela (não aparece no quadro nem no cartão). No cap04 o
  robô reabre a configuração em "Esse texto fica aqui".
