# Roteiro T21 · Integração com WhatsApp

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`,
gerado por script a partir desta coluna. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela
(`T21/inventario.md`, conferido de novo contra o código da 1.38.6).
Aula no computador (janela de 1280×800), logada como Camila Duarte (admin, que é quem pode conectar). Todo capítulo parte de um navegador novo, com o mundo do fim do capítulo anterior (sementes `seeds-extra/t21/apos-capNN.json`); quando um capítulo continua uma tela do anterior, o `setup` do robô a reabre fora do vídeo.
Tudo fictício e simulado no backend falso (`PRODUCAO.md`, integrações externas): nenhum número, conta ou QR Code de pareamento real; o QR é um texto qualquer desenhado pela tela; o número exibido é o telefone fictício da empresa; o celular lendo o código é ilustração genérica, sem a interface nem a marca do aplicativo de mensagens. A fala não cita data nem a hora dos envios e não lê os textos de exemplo das prévias.

- **Título final:** Integração com WhatsApp (o nome da TRILHA e do plano, que o cartão final do T22 já promete)
- **Vinhetas (áreas):** WHATSAPP · CONEXÃO · PROTEÇÃO · AUTOMAÇÕES · HISTÓRICO · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Ferramentas de RH: DISC, Organograma, Fluxograma (T22)
- **Próximo:** Dashboard, relatórios e exportações (T17, o último da trilha)
- **FAKE_NOW:** `2026-11-12T14:00:00-03:00` (quinta-feira) nos capítulos 0 a 7 e `2026-11-13T15:00:00-03:00` (sexta) nos capítulos 8 a 10, no backend falso e no robô. Motivo: o histórico do capítulo 8 precisa de um atendimento depois da conexão (a OS #34 do hotel na manhã do dia 13 e a OS da academia saindo às 15:00); o plano punha o capítulo 9 no dia 12, mas a tela dele é a mesma nos dois dias e no dia 13 o mundo segue em ordem. O T17 parte do dia 13, às 16:30.
- **Duração estimada:** ~7 min de vídeo (928 palavras de fala, ~5,9 min de voz a 2,6 palavras/s, mais 10 vinhetas, a ilustração e a espera pela conexão; o plano previa ~12 min, a fala segue o tempo natural)
- **Estado inicial (fim do T22):** `seeds-extra/t22/apos-cap11.json`: Glacial Cold Brasil, telefone (21) 3000-1000; Camila Duarte (admin) logada; módulo `whatsapp` ligado (`gen-01-tenant`); **nenhuma** linha em `company_whatsapp_settings` nem em `whatsapp_connections` (o T1 só olhou a tela; conferido nas duas portas de cadastro e no `seed_company_catalog`: nada de WhatsApp nasce com a empresa, inventário 0.4), então a tela abre com os padrões do código (`lib/whatsappAutomation.ts:92-125`); a OS #34 do Hotel Mirante do Mar "Pendente" (o chamado do T12); os clientes da base com celular e `whatsapp_notifications_enabled` ligado (o hotel com o celular (21) 93000-2102, `seeds/gen-02-cadastros.json`); `whatsapp_send_jobs` vazia.
  Como em toda aula que entra pelo Dashboard depois do T12, o `storage` de cada capítulo leva a marca `dominex:portal-tickets-seen:<id da Camila>`.
- **Por semente (bastidor):** desde o `inicio`, a **Academia Ponto Forte sem autorização** (`whatsapp_notifications_enabled` false); no capítulo 3, a "leitura do QR" (passo de bastidor que marca a conexão como conectada); no corte do capítulo 8 (dia 13), o atendimento da OS #34 do hotel pelo **Rafael Lima** (a caminho 09:10, iniciada 09:42, concluída 11:05) e uma OS da **Academia Ponto Forte** com o **Lucas Ferreira**, a caminho às 15:00 (a da série mensal de higienização do T5 nessa data, se houver; senão, uma nova), com os `whatsapp_send_jobs`: "OS · a_caminho" Lido, "OS · em_andamento" Lido e "OS · concluida" Entregue (hotel) e "OS · a_caminho" Ignorado, motivo "O cliente não autorizou mensagens pelo WhatsApp." (academia).
- **Criado ao vivo:** a conexão por QR Code (aceite com `risk_terms_version` 2026-10-16.3; número exibido +552130001000, o telefone da empresa; "Canal ativo"); "Avisos de serviço" das 07:00 às 22:00, todos os dias ("Lembretes de cobrança" no padrão, das 08:00 às 20:00, de segunda a sábado); "Ativar automações" ligado; na aba "Ordens de serviço", "Técnico a caminho" em "Cordial" e o "Lembrete de visita agendada" ligado, "1 dia antes · recomendado"; as cobranças no padrão (as quatro ligadas, 3 dias antes e 2 depois).
- **Estado final:** a empresa conectada, com as automações ligadas; a OS #34 concluída e a OS da academia a caminho (o T17 a conclui por semente); o histórico com os quatro avisos. Vira `seeds-extra/t21/apos-cap10.json` (igual ao `apos-cap07` com o corte do dia 13); o T17 parte dele; atualizar `MUNDO_FICTICIO.md`.
- **Sementes entre capítulos:** `inicio` (sem conexão; entrada dos capítulos 0 a 3), `apos-cap03` (conectado; entrada do 4), `apos-cap04` (os horários salvos; entrada do 5), `apos-cap05` (as automações ligadas e salvas; entrada do 6 e do 7), `apos-cap07` (o `apos-cap05` mais o atendimento do dia 13 e os avisos; entrada dos capítulos 8 a 10, com FAKE_NOW do dia 13); os capítulos 1, 2, 6, 7, 8, 9 e 10 só leem (no 7, a ficha do cliente abre e cancela).
- Decisões padrão (`plano.md` → "Riscos e decisões", proposta recomendada; com duas opções, a mais simples sem rosto, senha nem dado real):
  **nada real** (decisão 1): QR simulado, **número fictício**, celular só em ilustração genérica; conexão por bastidor, com a tela trocando sozinha para "Automações" (decisão 2, P3: o robô espera a troca); corte do capítulo 8 com a OS #34 atendida (decisão 3, proposta recomendada: o T17 já conta com ela concluída); "Ignorado" no histórico como estado normal do fluxo, dito como a escolha do cliente (decisão 4); **sem desconectar**: "Desconectar" só em zoom, e a empresa segue conectada no T17 (decisão 5); a fala apresenta o interruptor do cliente como a autorização e o "parar" como a saída (decisão 6, P14); sem zoom nos textos com chave técnica ("OS · a_caminho") nem na prévia das cobranças, que cita outra empresa (decisão 7, P1 e P6); nada de Assinatura nem "Contratar módulo" (decisão 8, P15).
  A conferência do código da 1.38.6 mudou quatro coisas do plano:
  (1) "Configurações" fica no rodapé do menu, ao lado de "Sair" (como no T1), e não num menu da conta;
  (2) o "Salvar configurações" é um só, no cartão "Automação de mensagens", e grava também a "Proteção do número" (`components/settings/SettingsWhatsappContent.tsx:320-339`): como cada capítulo abre um navegador novo, o capítulo 4 salva os horários no fim e o 5 salva os avisos da OS;
  (3) o botão só liga com alteração pendente (`components/settings/whatsapp/WhatsappAutomationSettings.tsx:280-285`), e as cobranças já nascem as quatro ligadas, 3 e 2 dias (`lib/whatsappAutomation.ts:111-124`): o capítulo 6 só mostra, sem salvar;
  (4) a caixa de aceite é estado da tela, sem gravar (`SettingsWhatsappContent.tsx:542-547`): o `setup` do capítulo 3 a marca de novo fora do vídeo.
  Handoffs (a fala não depende deles): chave técnica no histórico (P1); faixa que nunca aparece (P2); "Aparelhos conectados" × "Dispositivos conectados" (P4); dica do interruptor desatualizada (P5); prévia das cobranças com empresa de exemplo (P6); "Comportamento humano" fora da tela (P9); número sem máscara (P12); LGPD: cliente nasce autorizado (P14, `TRILHA.md`, achado 10).
  Pronúncias: QR Code e QR como no perfil; API "á-pê-í" (T1, T19); WhatsApp e OS na escrita normal, como no T3; os horários por extenso ("das sete da manhã às dez da noite"); nenhuma pronúncia nova.
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[ILUSTRAÇÃO: ...]` (capítulo 3), `[handoff: ...]` (texto ou comportamento do app para o time corrigir; a fala não depende dele).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Integração com WhatsApp". | (sem fala) |
| Dashboard da Dominex, logada como Camila Duarte (sem enquadrar "Requer Atenção"); a câmera desce até o rodapé do menu e clica em "Configurações" (engrenagem, ao lado de "Sair"); aba "Integrações", subaba "WhatsApp": o cartão "Conexão com o WhatsApp" ("Conecte o WhatsApp atual da empresa por QR Code. A API Oficial da Meta será adicionada depois, sem misturar os canais."), com o selo "Desconectado". [BACKEND: semente `seeds-extra/t21/inicio.json`, sem `company_whatsapp_settings` nem `whatsapp_connections`] | Oi! Neste tutorial a gente vai conectar o WhatsApp da empresa na Dominex e ligar os avisos automáticos pro cliente. |
| A câmera fica no cartão. | O técnico saiu pra visita, o cliente recebe uma mensagem. O serviço terminou, ele recebe outra. E a cobrança também avisa sozinha, perto do vencimento. |
| Cartão discreto: "Módulo WhatsApp". | Os avisos fazem parte do módulo de WhatsApp. Com ele contratado, tudo fica aqui, em Configurações, Integrações, WhatsApp. |
| Cartão discreto: "Antes: Ferramentas de RH: DISC, Organograma, Fluxograma". | Se você ainda não viu o tutorial Ferramentas de RH, dá uma olhada antes. [pause] Vamos ver o que a integração faz. |

### cap01 · O que a integração faz (vinheta: WHATSAPP)

| Tela | Fala |
| --- | --- |
| Capítulo novo, logada (semente `inicio`), em Configurações › "Integrações" › "WhatsApp"; zoom nos botões das seções: "Automações", "Atendimento", "Modelos", "Campanhas", "Histórico" e "Conexão" (com cadeado nas que dependem da conexão), sem passar o mouse. | Lá em cima ficam as áreas da integração. Em Automações você liga os avisos, no Histórico acompanha cada envio, e a Conexão é por onde tudo começa. |
| Zoom nos cadeados de "Automações" e de "Histórico", sem clicar. [P8: "Atendimento" e "Campanhas" são etapas futuras; a câmera não para neles] | As automações e o histórico abrem assim que o número conecta. |
| A câmera volta ao cartão: "Conectar por QR Code" ("Usa um número de WhatsApp da empresa. Leva menos de um minuto."), com o selo "Desconectado". | E a conexão é pelo QR Code, com um número de WhatsApp da empresa. Leva menos de um minuto, e os avisos saem desse número, então o cliente já reconhece quem está falando. |

### cap02 · Preparando o número (vinheta: CONEXÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); zoom no passo a passo: "Abra o WhatsApp no seu celular.", "Toque em Mais opções no Android ou em Configurações no iPhone.", "Toque em Dispositivos conectados e, em seguida, em Conectar dispositivo." e "Aponte a câmera para o QR Code desta tela.". | Tudo começa pela conexão. O passo a passo fica aqui na tela: no celular da empresa, você abre o WhatsApp, vai em Dispositivos conectados e aponta a câmera pro QR Code. |
| Zoom na dica "Pode ser melhor usar um número secundário. Se a empresa tiver um chip separado para os avisos, o WhatsApp principal de atendimento segue funcionando em qualquer cenário.". | Uma dica: se der, use um chip só pros avisos. Assim o WhatsApp principal do atendimento segue livre. |
| Zoom na caixa "Entendo que toda automação de WhatsApp fora da API Oficial da Meta tem um risco, ainda que ínfimo, de bloqueio do número, justamente por se tratar de envio automatizado."; marca a caixa. | Antes de conectar, você marca o aceite: toda automação fora da API oficial da Meta tem um risco pequeno de bloqueio do número. É por isso que vale ter o chip separado. |
| Zoom em "Conectar meu WhatsApp", que liga com o aceite marcado (sem clicar; a conexão é o próximo capítulo). | Com o aceite marcado, o botão Conectar meu WhatsApp libera. |

### cap03 · Lendo o QR Code (vinheta: CONEXÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); o `setup` marca a caixa de aceite fora do vídeo (estado da tela). Clique em "Conectar meu WhatsApp": a barra "Preparando a conexão e gerando o QR Code…" e o aviso "QR Code gerado" ("Abra o WhatsApp no celular e leia o código abaixo."); o QR simulado na caixa branca, com "WhatsApp → Aparelhos conectados → Conectar aparelho"; o selo vira "Aguardando leitura do QR" e o botão, "Gerar novo QR Code". [BACKEND: edge `whatsapp-connect` grava `whatsapp_connections` (`provider` evolution_qr, `status` qr, `risk_accepted_at`, `risk_terms_version` 2026-10-16.3) e `company_whatsapp_settings.connection_status`, e devolve `{connection_id, connection_status: 'qr', qr: '<texto fictício>', pairing_code: null}`; nada de código de pareamento real] [handoff: "Aparelhos conectados" aqui e "Dispositivos conectados" no passo a passo (P4)] | Com o aceite marcado, é hora de conectar. Clico em Conectar meu WhatsApp, e em poucos segundos o QR Code aparece na tela. Enquanto espera, o selo mostra Aguardando leitura do QR. |
| [ILUSTRAÇÃO: um celular genérico, sem marca nem a interface do aplicativo de mensagens, com a câmera apontada para um QR Code na tela de um computador; fundo branco, Montserrat, o verde da marca (molde `exemplos/dominex-t3/ilustracoes/ilustra_qr.py`)] | Aí, no celular da empresa, é só apontar a câmera pro código, na opção de conectar um aparelho. |
| De volta à tela: o selo passa a "Conectado", com "Número: +552130001000", o botão "Desconectar" e o selo "Canal ativo"; em seguida a tela vai sozinha para "Automações". [BACKEND: passo de bastidor (`/__dev` ou troca de semente) que grava em `whatsapp_connections` `status` connected, `display_number` 552130001000 e `connected_at`, e em `company_whatsapp_settings` `connection_status` connected e `active_connection_id`; a tela percebe na consulta de 4 s e o robô espera a troca de seção (P3); vira `apos-cap03`] | Pronto, conectado. A tela mostra o número da empresa e que o canal está ativo, e já abre as Automações. |

### cap04 · Horários de envio (vinheta: PROTEÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`): a subaba abre em "Automações"; o cartão "Proteção do número" ("Regras que fazem os avisos saírem no ritmo de uma pessoa, e não de um robô. Reduzem o risco de bloqueio e de reclamação do cliente.") e "Horários de envio" ("Fuso horário configurado para a empresa."). | Número conectado. Antes de ligar os avisos, os horários. A Proteção do número faz os avisos saírem no ritmo de uma pessoa, o que protege o número e respeita o cliente. |
| Zoom em "Avisos de serviço" ("Técnico a caminho, serviço iniciado e serviço concluído. ..."), com "Começa às" 06:00, "Termina às" 23:00 e os sete dias marcados. | São duas janelas. Os avisos de serviço acompanham a operação: o técnico a caminho, o serviço iniciado e o concluído. |
| Em "Começa às" escolhe 07:00 e em "Termina às", 22:00. | Na Glacial, eles saem das sete da manhã às dez da noite, todos os dias. |
| Zoom em "Lembretes de cobrança" ("Cobrança gerada, lembrete de vencimento e aviso de atraso. ..."), com 08:00 às 20:00 e "Seg" a "Sáb" marcados. | Os lembretes de cobrança já vêm das oito da manhã às oito da noite, de segunda a sábado, e eu deixo assim. |
| Zoom em "Fora do horário, a mensagem fica na fila e sai na próxima abertura.". | Fora do horário, a mensagem espera na fila e sai assim que a janela abre. |
| Desce até o cartão "Automação de mensagens", com o selo "Alterações não salvas"; clique em "Salvar configurações": aviso "Configurações de WhatsApp salvas.". [BACKEND: `INSERT company_whatsapp_settings` (`enabled` false e `automation_preferences` com a janela de serviço das 7 às 22); vira `apos-cap04`] | Pra gravar, o botão fica logo abaixo, no cartão das automações: Salvar configurações. |

### cap05 · Os avisos da OS (vinheta: AUTOMAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`); desce até "Automação de mensagens" ("Defina quais avisos serão enviados e como cada mensagem será montada."); liga "Ativar automações" (sem zoom na dica embaixo dele, P5). | Agora os avisos. No cartão Automação de mensagens, eu ligo o Ativar automações. |
| Aba "Ordens de serviço", lista "Escolha quando enviar": "Lembrete de visita agendada" ("Inativa"), "Técnico a caminho", "Serviço iniciado" e "OS concluída" ("Ativa"). | Na aba Ordens de serviço ficam os quatro momentos: o lembrete da visita, o técnico a caminho, o serviço iniciado e a OS concluída. Os três últimos já vêm ligados. |
| Clique em "Técnico a caminho" (selo "Editando"): "Enviar esta mensagem" ligado; em "Modelo da mensagem" abre a lista ("Rotação automática · recomendada", "Objetiva", "Cordial" e "Detalhada") e escolhe "Cordial". | Clicando num momento, você edita a mensagem dele. São três estilos de texto, e a rotação automática, a recomendada, vai alternando entre eles. Aqui eu fixo o Cordial. |
| Zoom em "Incluir link de acompanhamento da OS" (ligado) e na "Prévia da mensagem" (o balão "Sua empresa", "Prévia ilustrativa"). | Com o link de acompanhamento ligado, o cliente recebe junto o link da OS. E a prévia mostra um exemplo de como a mensagem chega: no Cordial, com o nome do técnico e o número da OS. |
| Clique em "Lembrete de visita agendada": liga "Enviar esta mensagem"; "Quando enviar o lembrete" fica em "1 dia antes · recomendado". | Ligo também o lembrete da visita agendada, um dia antes, como recomenda a tela. Ele sai na janela dos lembretes. |
| Clique em "Salvar configurações": aviso "Configurações de WhatsApp salvas."; o selo vira "Configurações salvas". [BACKEND: `UPDATE company_whatsapp_settings` (`enabled` true, `automation_preferences`, `trigger_a_caminho`, `trigger_em_andamento` e `trigger_concluida`); vira `apos-cap05`] | Salvar configurações, e os avisos da ordem de serviço estão prontos. |

### cap06 · Os avisos de cobrança (vinheta: AUTOMAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); em "Automação de mensagens", clique na aba "Cobranças": "Cobrança gerada" ("Manual ou criada por uma assinatura"), "Antes do vencimento", "No vencimento" e "Após o vencimento" ("Somente se a cobrança continuar pendente"), todos "Ativa". | E as cobranças também avisam sozinhas. Na aba Cobranças são quatro momentos: quando a cobrança é gerada, antes do vencimento, no dia e depois. |
| Clique em "Antes do vencimento": "Quantos dias antes" em 3; zoom em "Informações da cobrança" ("Valor" e "Link de pagamento"), sem zoom no texto da prévia (P6). | Antes do vencimento, você escolhe quantos dias antes, aqui três. E a mensagem leva o valor e o link de pagamento. |
| Clique em "Após o vencimento": "Quantos dias depois" em 2. | O aviso de atraso sai dois dias depois, e só pra quem ainda não pagou. |
| A câmera passa pelos quatro "Ativa"; o selo segue "Configurações salvas" (nada muda, nada a salvar). | Os quatro já vêm ligados, do jeito que a Glacial precisa, então eu deixo assim. |

### cap07 · A autorização do cliente (vinheta: AUTOMAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); em "Automação de mensagens", zoom em "Somente clientes com a opção “Receber mensagens pelo WhatsApp” ativa serão considerados.". | E quem recebe esses avisos? Os clientes com a opção Receber mensagens pelo WhatsApp ligada. |
| Menu "Gestão" → "Clientes e Fornecedores" → "Hotel Mirante do Mar" → "Editar": janela "Editar Cliente", aba "Contato", com o "Celular" ((21) 93000-2102) e o bloco "Receber mensagens pelo WhatsApp" ("Permite avisos de ordens de serviço, cobranças e vencimentos. Pedidos de cancelamento do cliente sempre prevalecem."), ligado. | Ela fica no cadastro de cada cliente, do lado do celular, e libera com o celular completo, com o DDD. No Hotel Mirante do Mar, ela está ligada. |
| Zoom em "Pedidos de cancelamento do cliente sempre prevalecem."; clique em "Cancelar". [handoff: cliente novo nasce autorizado (P14, LGPD)] | E se o cliente responder pedindo pra parar, os avisos param pra ele. Quem decide é o cliente. |

### cap08 · Acompanhando os envios (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo, no dia seguinte (FAKE_NOW 13/11 15:00; semente `apos-cap07`); Configurações › "Integrações" › "WhatsApp" (abre em "Automações"); clique em "Histórico". [BACKEND: o corte do dia 13 (ver "Por semente"): `service_orders` (a OS #34 concluída pelo Rafael Lima e a OS da academia a caminho, com o Lucas Ferreira) e os quatro `whatsapp_send_jobs` (`event_key`, `provider` evolution_qr, `status`, `attempts`, `last_error`, `created_at` e `sent_at`)] | No dia seguinte, depois de um atendimento no hotel, o Histórico conta o que saiu. |
| "Fila e histórico de envios" ("Últimos 50 avisos transacionais. Mensagens ignoradas mostram o motivo."), com os contadores "Na fila", "Enviado", "Entregue", "Lido", "Ignorado" e "Falhou". | Em cima ficam os contadores de cada situação, como enviado, entregue e lido. |
| A lista: os três avisos da OS do hotel, com a data e a hora e os selos "Lido", "Lido" e "Entregue" (sem zoom no nome técnico do evento, P1). | Embaixo, cada aviso. Os do hotel saíram certinho: o do técnico a caminho e o do serviço iniciado já foram lidos, e o de concluído foi entregue. |
| Zoom na linha "Ignorado" da academia, com o motivo "O cliente não autorizou mensagens pelo WhatsApp.". | A academia preferiu não receber mensagens, então o aviso dela aparece como ignorado, com o motivo do lado. Assim você sabe o que aconteceu com cada um. |

### cap09 · Reconectar e desconectar (vinheta: CONEXÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`, dia 13); clique em "Conexão": "Conectar por QR Code" com o selo "Conectado", "Número: +552130001000", o botão "Desconectar" e o selo "Canal ativo". | E se precisar trocar de aparelho ou de número? É aqui, na Conexão. |
| Zoom em "Desconectar", sem clicar (decisão 5). | O Desconectar pausa a fila de avisos. Depois, é só conectar de novo, lendo um QR Code novo no aparelho que você quiser. |
| Zoom no selo "Canal ativo". | Conectar e desconectar fica com o administrador ou o gestor. E com o canal ativo, os avisos seguem saindo sozinhos, no ritmo que você definiu. |

### cap10 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o QR Code e o selo "Conectado". | Pronto! Recapitulando: a gente conectou o WhatsApp da empresa pelo QR Code, com o aceite e a dica do chip separado. |
| Montagem rápida: a "Proteção do número" e a aba "Ordens de serviço" com a prévia. | Definiu os horários de envio, ligou os avisos da ordem de serviço, conheceu os das cobranças e escolheu o estilo de cada mensagem. |
| Montagem rápida: o interruptor do cliente e o "Histórico". | Viu que recebe quem está autorizado no cadastro e acompanhou cada envio no Histórico. |
| Cartão "Próximo: Dashboard, relatórios e exportações"; cartela final. | No próximo tutorial, o último da trilha, a gente lê o Dashboard e encontra cada relatório da Dominex. Até lá! |
