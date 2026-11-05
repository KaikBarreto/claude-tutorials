# Plano · T21 — Integração com WhatsApp

- **Título final da aula:** Integração com WhatsApp (o cartão final do T22 promete "WhatsApp").
- **Áreas das vinhetas:** WHATSAPP · CONEXÃO · PROTEÇÃO · AUTOMAÇÕES · HISTÓRICO · RESUMO.
- **Objetivo (uma frase):** conectar o WhatsApp da empresa por QR Code, definir os horários seguros e ligar os avisos automáticos
  da OS e das cobranças, acompanhando cada envio no histórico.
- **Pré-requisito:** T22 na ordem de exibição; a base é o T1 (onde ficam as integrações), o T5/T7 (status da OS) e o T19
  (cobranças). Aviso: "Antes: Ferramentas de RH".
- **Próximo:** T14 (Notas Fiscais, NFS-e e NF-e); depois o T17. Aviso: "Próximo: Notas Fiscais" (correção do coordenador, 05/11).
- **Duração estimada:** ~12 min de fala natural (11 blocos). 🔒 Módulo **WhatsApp** (no catálogo, "Avisos de WhatsApp").
- Base: `T21/inventario.md` (código 1.38.6). WhatsApp e celular **simulados**: nenhum número, conta ou QR real.
- **FAKE_NOW:** `2026-11-12T14:00:00-03:00` (quinta) nos blocos 0 a 7 e 9; o bloco 8 é um corte para `2026-11-13T15:00:00-03:00`
  (sexta), depois de um atendimento com avisos. O T14 (e depois o T17) parte do dia 13.

## Capítulos propostos

| # | Vinheta (área / título) | O que a tela mostra | Avisos na tela (positivos) | Duração |
|---|---|---|---|---|
| 0 | — | Menu da conta › "Configurações" › "Integrações" › "WhatsApp": cartão "Conexão com o WhatsApp". Fala: o cliente avisado sozinho, a cada passo da OS e da cobrança. | "Antes: Ferramentas de RH" · "Módulo WhatsApp" | 0:35 |
| 1 | WHATSAPP / O que a integração faz | Botões das seções: "Automações", "Atendimento" e "Campanhas" (cadeado, "Etapa futura"), "Modelos", "Histórico", "Conexão"; zoom em "Meta Cloud API" "Em breve". | "Liberado ao conectar: automações e histórico" | 0:50 |
| 2 | CONEXÃO / Preparando o número | "Conectar por QR Code" (selo "Desconectado"); passo a passo de 4 itens; caixa "Entendo que toda automação…" marcada; zoom na dica "Pode ser melhor usar um número secundário…". | "Dica: um chip só para os avisos" | 1:05 |
| 3 | CONEXÃO / Lendo o QR Code | "Conectar meu WhatsApp" → "Preparando a conexão e gerando o QR Code…" → "QR Code gerado" → QR e "WhatsApp → Aparelhos conectados → Conectar aparelho", selo "Aguardando leitura do QR". [ILUSTRAÇÃO: celular genérico lendo o QR, sem marca]. Selo "Conectado", "Número: +552130001000", "Canal ativo"; a tela vai sozinha para "Automações". | "Leva menos de um minuto" | 1:20 |
| 4 | PROTEÇÃO / Horários de envio | "Proteção do número": "Avisos de serviço" (06:00 às 23:00, todos os dias) → "Começa às" 07:00, "Termina às" 22:00; "Lembretes de cobrança" (08:00 às 20:00, segunda a sábado); zoom em "Fora do horário, a mensagem fica na fila e sai na próxima abertura.". | "Fora do horário, a mensagem espera" | 1:05 |
| 5 | AUTOMAÇÕES / Os avisos da OS | "Automação de mensagens": "Ativar automações"; aba "Ordens de serviço": "Técnico a caminho" → "Enviar esta mensagem", "Modelo da mensagem" "Cordial", "Incluir link de acompanhamento da OS", "Prévia da mensagem" (zoom em "Prévia ilustrativa"); "Lembrete de visita agendada" ligado, "1 dia antes · recomendado". | "Quatro jeitos de escrever, a rotação é a recomendada" | 1:30 |
| 6 | AUTOMAÇÕES / Os avisos de cobrança | Aba "Cobranças": "Cobrança gerada", "Antes do vencimento" ("Quantos dias antes" 3), "No vencimento", "Após o vencimento" ("Quantos dias depois" 2); "Informações da cobrança" ("Valor", "Link de pagamento"); "Salvar configurações" → "Configurações de WhatsApp salvas.". | "Só sai se a cobrança continuar pendente" | 1:05 |
| 7 | AUTOMAÇÕES / A autorização do cliente | Zoom em "Somente clientes com a opção "Receber mensagens pelo WhatsApp" ativa serão considerados."; Clientes e Fornecedores › Hotel Mirante do Mar › editar: bloco "Receber mensagens pelo WhatsApp" ("Permite avisos de ordens de serviço, cobranças e vencimentos. Pedidos de cancelamento do cliente sempre prevalecem.") ligado; "Cancelar". | "O cliente pode pedir pra parar a qualquer hora" | 1:00 |
| 8 | HISTÓRICO / Acompanhando os envios | Corte "no dia seguinte": "Histórico": "Fila e histórico de envios"; contadores ("Enviado", "Entregue", "Lido", "Ignorado"…); as linhas do atendimento do hotel ("Lido", "Entregue") e um "Ignorado" com o motivo "O cliente não autorizou mensagens pelo WhatsApp.". | "Cada aviso mostra o que aconteceu" | 1:10 |
| 9 | CONEXÃO / Reconectar e desconectar | "Conexão": "Conectado", "Canal ativo"; zoom em "Desconectar" (decisão 5) e no rodapé "O Dominex reduz o risco com consentimento, fila, aquecimento e limites…". Fala: trocar de aparelho ou de número é desconectar e ler um QR novo. | "Desconectar pausa a fila" | 0:55 |
| 10 | RESUMO / Recapitulando | Montagem: QR e "Conectado", horários, eventos ligados, prévia, interruptor do cliente, histórico. | "Próximo: Dashboard e relatórios" | 0:50 |

Transições faladas: 1→2 "Tudo começa pela conexão"; 3→4 "Número conectado: antes de ligar os avisos, os horários"; 5→6 "E
as cobranças também podem avisar sozinhas"; 7→8 "No dia seguinte, depois de um atendimento, o histórico conta o que saiu";
8→9 "E se precisar trocar de aparelho?". Recap → próximo: "No último tutorial da trilha, a gente lê o dashboard e encontra cada
relatório da Dominex."

**Falas dos cuidados ⚠️:**

| Cuidado | Fala sugerida | Na tela |
|---|---|---|
| Risco do QR Code | "Marca o aceite: toda automação fora da API oficial tem um risco pequeno de bloqueio. Por isso, um chip separado para os avisos é o melhor caminho." | caixa e dica |
| Sem conexão | "As automações abrem assim que o número conecta." | seções com cadeado |
| Quem altera | "As regras ficam com administradores, gestores ou quem tem a permissão de configurações." | — |
| Prévias | "Atendimento e campanhas são as próximas etapas da integração." | cadeado "Etapa futura" |
| Autorização | "Só recebe quem está autorizado na ficha. E se o cliente responder parar, os avisos param pra ele." | interruptor do cliente |

## Mundo fictício

**Começa com** (fim do T22): Glacial Cold Brasil, telefone (21) 3000-1000; Camila (admin); módulo `whatsapp` ligado (semente
`gen-01-tenant`); nenhuma conexão nem configuração de WhatsApp (o T1 só olhou); OS #34 do hotel "Pendente" (T12); a série mensal
de Higienização da Academia Ponto Forte (T5); cobranças do T19.

**Esta aula cria:**

| Item | Valores (fictícios) |
|---|---|
| Conexão | QR Code simulado; aceite com `risk_terms_version` 2026-10-16.3; número exibido **+552130001000** (o telefone da empresa); "Canal ativo" |
| Proteção | "Avisos de serviço" 07:00 às 22:00, todos os dias; "Lembretes de cobrança" no padrão |
| Automações | ligadas; OS: os três avisos no padrão e "Técnico a caminho" em "Cordial", lembrete de visita "1 dia antes"; cobranças no padrão (3 e 2 dias) |
| Autorização (semente) | Hotel Mirante do Mar autorizado com celular fictício; Academia Ponto Forte **não** autorizada |
| Corte do bloco 8 (13/11) | OS #34 atendida pelo Rafael Lima (a caminho 09:10, iniciada 09:42, concluída 11:05) e uma OS da Academia no mesmo dia; `whatsapp_send_jobs`: "OS · a_caminho" Lido, "OS · em_andamento" Lido, "OS · concluida" Entregue (hotel) e "OS · a_caminho" Ignorado (Academia) |

**Fica para as próximas:** o T17 abre o Dashboard com a OS #34 concluída (o aviso de chamados fica só com o da Mariana Lopes) e
o WhatsApp conectado (decisão 5).

## Gravação (modo fakebase)

**Já coberto:** módulos da empresa; clientes e OS das aulas anteriores.

**Falta** (inventário 4.2):

1. Edge `whatsapp-connect`: cria/atualiza `whatsapp_connections` (`provider` `evolution_qr`, `status` `qr`, `risk_accepted_at`,
   `risk_terms_version`) e devolve `{connection_id, connection_status: 'qr', qr: '<texto fictício>', pairing_code: null, message}`.
2. **"Leitura do QR"** por bastidor: endpoint `/__dev` (ou troca de semente no meio do capítulo) que grava `status` `connected`,
   `display_number` 552130001000, `connected_at`, e em `company_whatsapp_settings` `connection_status` `connected` e
   `active_connection_id`; a tela percebe na consulta de 4 s.
3. Edges `whatsapp-connection-select` e `whatsapp-connection-disconnect` (este só se a decisão 5 for clicar).
4. `company_whatsapp_settings`: aceitar o insert do primeiro "Salvar configurações" e os updates.
5. Sementes: `customers.celular` e `whatsapp_notifications_enabled` (hotel e academia); o corte do bloco 8 com as OS e os
   `whatsapp_send_jobs` (`event_key`, `provider`, `status`, `attempts`, `last_error`, `created_at`, `sent_at`).
6. Ilustração do bloco 3 (celular genérico com a câmera no QR, sem a interface nem a marca de terceiros).
7. Desktop 1280×800; `storage` com a marca `dominex:portal-tickets-seen:<id da Camila>`.

## Pronúncias novas para o TTS

| Tela / legenda | Texto do TTS |
|---|---|
| WhatsApp | uótsáp (conferir se o perfil já tem; testar) |
| QR Code | como no perfil |
| Meta / API | méta / a-pê-i |
| 07:00 / 22:00 | sete da manhã / dez da noite |

## Riscos e decisões para o Kaik

1. **Nada real:** QR simulado, número exibido = telefone fictício da empresa, celular lendo o QR só em ilustração genérica (P16).
   Confirmar (`TRILHA.md`, decisão 3).
2. **Conexão por bastidor:** a "leitura" do QR é um passo do robô no backend falso; a tela muda de seção sozinha (P3).
3. **Corte do bloco 8:** atender a OS #34 fora do vídeo para o histórico ter linhas. Isso fecha o chamado do hotel antes do T17.
   Alternativa: semear só os avisos de uma OS nova do dia 13, sem tocar na #34.
4. **"Ignorado" no histórico:** é um estado normal do fluxo (cliente sem autorização), não uma falha encenada. Confirmar.
5. **Desconectar:** proposta: só zoom e a fala, para a empresa seguir conectada no T17. Alternativa: clicar e mostrar "WhatsApp
   desconectado".
6. **Autorização por padrão (LGPD, P14):** o cliente nasce autorizado; a fala mostra o interruptor como a autorização e o "parar"
   como saída. Handoff para o time decidir o *backfill* e o carimbo de opt-in.
7. **Textos com chave técnica e empresa de exemplo** (P1, P6): sem zoom nesses textos; handoff.
8. **Sem preço:** não abrir Assinatura nem "Contratar módulo" (o preço do módulo está no banco).
