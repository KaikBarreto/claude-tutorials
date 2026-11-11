# T12 · Propostas de fala e achados do ensaio do robô

Ensaio do robô de 11/11/2026 (EcoSistema 1.59.154, Supabase falso na 54312, FAKE_NOW 10/11/2026 07:00, voz estimada). A revisão
geral aplica; `roteiro.md` e `tts_textos.py` não foram mexidos.

## Fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| — | — | (preenchido depois do ensaio completo) | | |

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
- Cartão da ordem cancelada (#4) oferece o botão "Preencher" (`CollectionOrdersBoard.tsx`, cartão das colunas que não são
  "Solicitada": "Preencher" quando não é concluída), embora a ordem não mude mais de etapa.
