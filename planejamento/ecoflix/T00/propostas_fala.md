# T00 · propostas de fala e achados do app (robô, ensaio com voz estimada)

Nada aqui foi aplicado no `roteiro.md` nem no `tts_textos.py`: a revisão geral decide.

## Propostas de fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 02 (celular 9:16) | 4 | "...o selo Tem no seu plano..." (dito sobre a lista) | manter no computador; no celular a lista de aulas não mostra selo, o selo aparece só na gaveta "Ver trilha" | o robô abre a gaveta na frase do selo; se a fala pedir "na lista", o celular diverge do computador |
| 04 | 2 | "...o seu e-mail, a sua empresa, a trilha e a aula" | sem mudança de fala; só a ilustração do cap04 traz `rafael.nogueira@...` e o app monta a mensagem com o e-mail da conta, `rafael@reciclavalemetais.example` | alinhar a ilustração à tela (ver Achados) |
| 09 | 5 | "Em Uso da conta, você vê..." | sem mudança; só não dizer "embaixo": no computador o cartão Uso da conta fica ao lado do plano (à direita), no celular fica abaixo | a linha 4 ("Embaixo, o valor...") vale nas duas versões; a 5 não deve dar posição |
| 12 | 6 | "cada mensalidade paga, com a nota fiscal pra baixar" | sem mudança; o gesto é só olhar o botão "Baixar PDF" (não clicar) | o robô nunca baixa arquivo |

## Achados do app

- **Histórico de Pagamentos**: com pagamentos Asaas o cartão do histórico se chama "Cobrança • <empresa>" (não "Renovação"). Se o roteiro ou a ilustração do cap12 citar "Renovação", ajustar.
- **Celular, trilha EcoFlix**: a lista "Aulas da trilha" não mostra os selos "Tem no seu plano" / "Não tem no seu plano" nem "Formação básica"; eles aparecem na gaveta "Ver trilha" e na página da aula. A edição 9:16 do cap02/cap03 usa a gaveta.
- **Celular, Assinatura**: o subtítulo "Gerencie seu plano, módulos e pagamentos" fica escondido no celular (só o título "Assinatura").
- **Celular, Configurações → Aparência**: o quadro "Estilo de Navegação (Desktop)" aparece no celular com o aviso "Esta opção só afeta a visualização em desktop"; no celular o menu de baixo e a gaveta "Menu" continuam os mesmos (o cap07 linha 5 usa isso).
- **Portão da introdução**: ocupa a tela inteira (não é uma janela sobre o Dashboard), com o vídeo à esquerda e o painel "Antes de usar o sistema" à direita; o "Primeiro passo" fica no canto superior direito, fora da faixa útil (o robô passa a hover sem rolar).
- **Nome da empresa e e-mail do mundo**: o mundo-base trazia outro nome de empresa; a semente da T00 troca para "Recicla Vale Metais Ltda". Marcos e Juliana foram retirados da semente da T00 (a conta tem 1 usuário, "1 / 3" em Uso da conta).
