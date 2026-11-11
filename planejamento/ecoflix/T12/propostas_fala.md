# T12 · Propostas de fala e achados do ensaio do robô

Ensaio do robô de 11/11/2026 (EcoSistema 1.59.154, Supabase falso na 54312, FAKE_NOW 10/11/2026 07:00, voz estimada). A revisão
geral aplica; `roteiro.md` e `tts_textos.py` não foram mexidos.

## Fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| — | — | Nenhuma troca de texto até aqui: os números da tela conferem com a fala (cap02 colunas 0/1/1/5/1; cap05 #9 com Jair Lopes e GHT7B19; cap06 ficha da 8 com Caçamba 03 recolhida e 05 entregue; cap07 pedido #10; cap08 FKD2E41 6.380 kg e 14.000 kg; cap10 4/1/0/25% e 6/5/1/100%, conferidos por `confere*` no robô). | — | — |

Respiros que a voz de verdade pode pedir (`pausas.py`, a medir na gravação final, não é troca de texto):
- cap06 L7 ("De volta ao quadro"): o quadro leva ~1 s para montar depois de "Voltar às ordens".
- cap07 L7 ("Agora, do lado da Recicla Vale"): a troca do portal para o sistema (rota da Frota) leva ~1 s.
- cap08 L5 ("Aqui, São Paulo, veículo único e toco"): três seletores em ~2 s; o robô usa o teclado (sem cursor) no Tipo e no rodado.

## Coluna Tela do roteiro (não muda a fala)

| Cap. | Onde | Roteiro | Na tela (1.59.154 + mundo) |
|---|---|---|---|
| cap02 | cartão #8 | "Taubaté / SP" | "Tremembé / SP": o Depósito Irmãos Siqueira é de Tremembé no mundo base (Estrada do Pinheirinho, 2730). A fala não cita a cidade. |
| cap06 | Histórico da ordem 8 | "a criação ("Agendada", 05/11)" | O app não grava evento de criação (`collection_order_events` só recebe as mudanças de etapa do `change_collection_order_status`): o Histórico mostra "Agendada → A caminho" e "A caminho → Concluída". A fala ("cada mudança de etapa") já vale. |
| cap06 | tela da ordem | bloco "Recolhi" e depois "Entreguei" | Na tela o "Entreguei" vem em cima do "Recolhi"; o robô segue a fala (Recolhi primeiro). |
| cap07 | segunda janela | portal numa segunda janela, sem login | O vídeo grava uma aba só: o portal abre na mesma aba (link público, igual ao que a cooperativa vê) e o sistema volta pela rota da Frota durante "Agora, do lado da Recicla Vale". |

## Achados do app

- Quadro "Ordens de Coleta" a 1280 px com o menu lateral aberto: os nomes dos parceiros nos cartões saem cortados
  ("Depósito Irmãos ...", e "Mar..." ao lado do selo "Sem cadastro" no cartão #7, que a fala chama de "Marcelo Tavares").
- "Relatório de Coleta 8" (tela da ordem concluída, cap06): "Agendamento 09/11/2026 · Manhã" para uma coleta agendada para 10/11. A data
  sem hora do relatório (`agendamento.data`, "2026-11-10") é lida como meia-noite UTC e mostrada em Brasília, um dia antes
  (`pages/CollectionOrderPage.tsx`, `fmtDate`). A ficha e o quadro mostram 10/11 certo. A câmera fica no relatório em "Concluir coleta" e
  na dica: melhor não aproximar o bloco do Agendamento na edição.
- Campo de data nativo (Data agendada, Data preferida, Validade da CNH) mostra "dd/mm/yyyy" vazio no Chromium do robô (o valor sai
  13/11/2026 certo): é o navegador da gravação, não o app.
- Cartão da ordem cancelada (#4) oferece o botão "Preencher" (`CollectionOrdersBoard.tsx`, cartão das colunas que não são
  "Solicitada": "Preencher" quando não é concluída), embora a ordem não mude mais de etapa.
