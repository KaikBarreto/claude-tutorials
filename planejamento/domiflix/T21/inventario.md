# Inventário funcional · T21 — Integração com WhatsApp (Dominex)

> Base para o roteiro do tutorial "T21 · Integração com WhatsApp". Levantado em 31/10/2026 contra o código publicado
> `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em `/home/claude/domiflix/src-1.38.6`.
> **Análise estática, somente leitura.** "(a confirmar)" = só rodando. Formato do inventário do T3/T14.
> Não há seção própria no Guia Técnico (só menções em T1 e T3). Gravação **só com o WhatsApp simulado** no backend falso
> (`TRILHA.md`, decisão 3): nenhum número real, nenhuma conta real, nenhum QR Code de pareamento de verdade.

## Como ler

- Caminhos relativos a `src/`, exceto `supabase/...` e `rec/...`. Formato `arquivo:linha`.
- Rótulos entre aspas = texto exato (pt-br). **shell** = `components/settings/SettingsWhatsappContent.tsx` (textos pt-br `:86-106`,
  cartão de conexão `:421-607`, histórico `:609-642`); **auto** = `components/settings/whatsapp/WhatsappAutomationSettings.tsx`
  (textos pt-br `:54-106`); **prot** = `components/settings/whatsapp/WhatsappProtectionSettings.tsx` (textos pt-br `:29-53`).
- Por trás: provedor **Evolution** por QR Code (`provider = 'evolution_qr'`); "Meta Cloud API" aparece como "Em breve"
  (shell `:583-598`). O navegador só fala com as edges `whatsapp-connect`, `whatsapp-connection-select` e
  `whatsapp-connection-disconnect`; o envio é de uma fila no servidor (`whatsapp-send-worker`) alimentada por gatilhos.

---

## 0. Resumo para o roteiro

### 0.1 Capítulos da trilha (v1.22.5) contra o código de hoje

| # | Item da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Configurações → Integrações → **WhatsApp** e o que o módulo libera | **Bate** | Subaba "WhatsApp" de "Integrações" (`/configuracoes?tab=integracoes&integration=whatsapp`, shell `:136-171`; `pages/Settings.tsx:112,1892-1893`). Seções em botões: "Automações", "Atendimento", "Modelos", "Campanhas", "Histórico", "Conexão" (shell `:105,364-412`). Sem conexão, só "Conexão" abre; "Atendimento" e "Campanhas" ficam sempre com cadeado ("Etapa futura") (`:378-406`). |
| 2 | Conexão por QR: preparar o número, aceitar o risco, iniciar | **Bate** | Cartão "Conexão com o WhatsApp" → "Conectar por QR Code" ("Usa um número de WhatsApp da empresa. Leva menos de um minuto."), passo a passo de 4 itens, caixa de aceite do risco, dica do número secundário, botão **"Conectar meu WhatsApp"** (só com o aceite marcado) (shell `:478-580`; `components/settings/whatsapp/WhatsappPairingSteps.tsx:28-76`). |
| 3 | Ler o QR e acompanhar os estados | **Bate** | "Preparando a conexão e gerando o QR Code…" → toast "QR Code gerado" — "Abra o WhatsApp no celular e leia o código abaixo." → QR e "WhatsApp → Aparelhos conectados → Conectar aparelho" (shell `:446-453,524-533,561-565`). Selo: "Desconectado", "Conectando", "Aguardando leitura do QR", "Conectado", "Pausado por segurança", "Possível bloqueio", "Erro", "Aceite necessário" (`:416-419,504-508`). A tela consulta a cada 4 s enquanto espera (`hooks/useWhatsappConnections.ts:79-82`). |
| 4 | Número ativo, reconexão e troca da conexão principal | **Mudou** | Conectado: "Número: +{número}", **"Canal ativo"**, "Desconectar"; "Usar este canal" só se a conexão não for a ativa; "Gerar novo QR Code" / "Confirmar e ativar" ao reconectar (shell `:511-580`). **Uma conexão QR por empresa** (`UNIQUE (company_id, provider)`, `supabase/migrations/20261016143000_whatsapp_hibrido_fila.sql:39`): não há troca entre números (P11). |
| 5 | Proteção do número: horário, ritmo e limites | **Mudou** | "Proteção do número": "Horários de envio" com **"Avisos de serviço"** (06:00 às 23:00, todos os dias) e **"Lembretes de cobrança"** (08:00 às 20:00, seg. a sáb.), "Começa às", "Termina às", "Dias da semana"; "Fora do horário, a mensagem fica na fila e sai na próxima abertura." (prot `:29-53,175-305`; padrões `lib/whatsappAutomation.ts:92-97`). "Comportamento humano" saiu da tela (sempre ligado, P9). **Sem limite mensal** desde 28/10 (P15). |
| 6 | Ativar automações e escolher os eventos da OS | **Bate** | "Automação de mensagens": **"Ativar automações"**, aba "Ordens de serviço": "Lembrete de visita agendada" (desligado), "Técnico a caminho", "Serviço iniciado", "OS concluída" (ligados) (auto `:54-106`; `lib/whatsappAutomation.ts:102-109`). Salvar: **"Salvar configurações"** → "Configurações de WhatsApp salvas." (shell `:243-257`; `:104`). |
| 7 | Conteúdo, modelos e autorização por cliente | **Bate** | Por evento: "Enviar esta mensagem", **"Modelo da mensagem"** ("Rotação automática · recomendada", "Objetiva", "Cordial", "Detalhada"), "Incluir link de acompanhamento da OS"; cobranças: "Informações da cobrança" ("Valor", "Link de pagamento"), "Quantos dias antes"/"Quantos dias depois"; **"Prévia da mensagem"** (auto `:66-105,401-540`). Autorização: "Somente clientes com a opção "Receber mensagens pelo WhatsApp" ativa serão considerados." e o interruptor na ficha do cliente (`components/customers/CustomerFormDialog.tsx:508-533`). A seção "Modelos" é só prévia (P7). |
| 8 | Histórico: enviado, falhou, bloqueado e nova tentativa | **Mudou** | "Fila e histórico de envios" — "Últimos 50 avisos transacionais. Mensagens ignoradas mostram o motivo." — contadores "Na fila", "Enviado", "Entregue", "Lido", "Ignorado", "Falhou"; lista com o evento, a data e o selo (shell `:609-642`). "Nova tentativa" é **estado**, não botão; "bloqueado" não existe como selo (P1, P12). |
| 9 | Desconectar com segurança e quando refazer o pareamento | **Bate** | **"Desconectar"** → toast "WhatsApp desconectado" — "A fila foi pausada e não mudará de canal automaticamente." (shell `:465-474,571`). Depois, "Conectar meu WhatsApp" de novo. |

Avisos da trilha:

- ⚠️ "Atendimento e campanhas são prévias bloqueadas" → **bate** (cadeado com "Etapa futura", shell `:398-407`; conteúdo de
  prévia em `components/settings/whatsapp/WhatsappCapabilityPreviews.tsx:50-311`). Não gravar como disponível.
- ⚠️ "Sem conexão ativa, as automações ficam bloqueadas" → **bate**: sem conexão a tela fica presa em "Conexão" (shell `:241`).
- ⚠️ "Só administradores, gestores ou quem tem permissão de configurações altera as regras" → **bate** para as regras (shell `:208,235`;
  aviso "Configuração somente para leitura", `:289-292`); **conectar e desconectar só admin/gestor** (`:346`; P10).
- ⚠️ "Não use número pessoal ou principal sem explicar o risco" → **bate**: aceite obrigatório e dica do número secundário (shell `:542-554`).

### 0.2 O que mudou desde a 1.22.5 (`pages/Changelog.tsx`)

| Versão | Mudança | Linhas |
|---|---|---|
| 1.32.0 | Central de integração com WhatsApp; autorização de WhatsApp por cliente | `:1996,2006` |
| 1.32.1 | Contratação do WhatsApp pelas configurações | `:1984` |
| 1.35.0 / 1.35.1 / 1.35.3 / 1.35.4 / 1.35.7 | Avisos automáticos; tela de conexão mais clara; passo a passo para conectar; automações mais simples | `:1747,1735,1711,1699,1665` |
| 1.37.3 / 1.37.4 | Cobranças mais claras e sem repetição; confirmação de entrega e leitura | `:1080,1063,1068` |
| 1.37.49 | Lembrete de visita agendada pelo WhatsApp | `:253` |
| — (28/10, banco) | Módulo ilimitado, sem níveis | `supabase/migrations/20261028140000_whatsapp_modulo_ilimitado_sem_niveis.sql:1-80` |

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. Logo depois de conectar, a tela pula sozinha para "Automações" (P3).
2. O histórico mostra o evento com a chave técnica: "OS · a_caminho", "OS · concluida", "Cobrança · before_due" (P1).
3. A prévia das cobranças cita uma empresa de exemplo, "Clima Forte Serviços", e não a Glacial (P6).
4. Cliente novo nasce **autorizado** a receber mensagens (P14, LGPD).
5. O número aparece cru: "Número: +552130001000" (P12).

### 0.4 O que a empresa ganha ao nascer (cadastro) e toca o WhatsApp

Conferido nas duas portas de cadastro (`supabase/functions/self-register/index.ts:728-1052`,
`supabase/functions/create-company/index.ts:330-557`: `companies`, `company_modules`, `profiles`, `user_roles`, `company_settings`,
`user_preferences`, `financial_categories`, `financial_accounts` e o RPC `seed_company_catalog`), no RPC
(`supabase/migrations/20260718120000_seed_company_catalog_i18n.sql:10-247`: tipos de serviço, status de OS e tipos de tarefa) e
nos gatilhos `AFTER INSERT ON companies` (configurações, estoque padrão, campos de equipamento, categorias de sistema, grupos do
DRE e o acompanhamento do período de teste):

- **Nada de WhatsApp por empresa:** nenhuma linha em `company_whatsapp_settings` nem em `whatsapp_connections`. A tela abre com
  os padrões do código (`lib/whatsappAutomation.ts:92-125`: avisos de serviço das 6h às 23h todos os dias, lembretes das 8h às 20h
  de segunda a sábado, "Técnico a caminho"/"Serviço iniciado"/"OS concluída" ligados, lembrete de visita desligado, cobranças 3
  dias antes e 2 depois) e o primeiro "Salvar configurações" cria a linha (seção 4.2).
- **Modelos de mensagem:** o texto é montado no próprio envio, pelo estilo escolhido
  (`supabase/functions/whatsapp-send-worker/index.ts:585-600,650`). Existe um catálogo **global** `whatsapp_templates` (sem
  `company_id`; leitura para qualquer usuário logado; `supabase/migrations/20260729220814_whatsapp_avisos_os.sql:83-100`, textos
  em `20260730093000_whatsapp_templates_enriquecidos.sql`), mas nem a tela nem o envio atual o leem (nenhuma referência em `src/`
  nem em `supabase/functions/` fora dos tipos, nenhum `FROM whatsapp_templates` nas migrations). Nada a semear.
- **Módulo:** vem do plano escolhido no cadastro (`company_modules`, `self-register/index.ts:775`); no mundo fictício, a semente
  `gen-01-tenant` já liga `whatsapp`.
- **Cliente:** cada cliente novo nasce com `whatsapp_notifications_enabled` ligado (P14).

---

## 1. Rotas e navegação

| Tela | Caminho | URL | Componente |
|---|---|---|---|
| Configurações | menu da conta › "Configurações" (permissão "Configurações") | `/configuracoes` (`App.tsx:866`) | `pages/Settings.tsx` |
| Aba Integrações | aba "Integrações" (`pages/Settings.tsx:112`; `lib/i18n/messages/app/settings.ts:35`) | `?tab=integracoes` | `SettingsIntegrationContent` (shell `:137-173`) |
| Subaba WhatsApp (padrão) | "WhatsApp" / "Cobranças (Asaas)" / "API Pública" (`settings.ts:1475-1477`; shell `:153-157`) | `?tab=integracoes&integration=whatsapp` | `WhatsappContent` (shell `:202-353`) |
| Seções | botões da 3ª camada (shell `:364-412`) | estado da tela (sem `?`) | — |
| Autorização do cliente | Gestão › "Clientes e Fornecedores" › cliente › editar | `/clientes/<nome>-<código>` | `components/customers/CustomerFormDialog.tsx:508-533` |

O T1 (cap. 11) mostrou só a subaba parada na conexão; esta aula começa ali.

## 2. Permissões e módulos

| O quê | Regra | Onde |
|---|---|---|
| Módulo | `whatsapp` — catálogo "Avisos de WhatsApp" ("Avisos automáticos e ilimitados por WhatsApp aos clientes.") | `supabase/migrations/20261028140000_...sql:52-56`; `lib/subscriptionCatalog.ts:4` |
| Sem o módulo | faixa com cadeado "Prévia do módulo de WhatsApp" — "Você pode conhecer toda a estrutura. Para salvar e ativar as automações, contrate o módulo de WhatsApp." + "Contratar módulo" (vai para `/assinatura?addModule=whatsapp`) | shell `:270-288` |
| Editar regras | admin/gestor **ou** "Gerenciar Configurações" (`fn:manage_settings`); senão "Configuração somente para leitura" | shell `:207-208,235,289-292` |
| Conectar / ativar / desconectar | só admin/gestor (`canManage={isAdminOrGestor()}`), e a edge confere módulo e papel | shell `:346,543,570-575`; `supabase/functions/_shared/whatsapp-auth.ts:54-165` |
| Envio | a fila só envia com o módulo ativo ("Módulo de WhatsApp inativo."), conexão válida e cliente autorizado | `supabase/functions/whatsapp-send-worker/index.ts:798-907` |

---

## 3. Por tela

### 3.1 Subaba "WhatsApp" — cabeça e seções (shell `:202-412`)

- Carregando: esqueleto "Carregando configurações do WhatsApp" (`:259-266`).
- Faixas: sem módulo (2), sem permissão (2); "Conecte o WhatsApp para liberar as configurações" — "As automações ficam disponíveis
  após conectar o número da empresa por QR Code. Atendimento e campanhas continuam como etapas futuras." só aparece fora da
  "Conexão", o que não acontece sem conexão (P2) (`:293-300`).
- Botões das seções com ícone; cadeado nas bloqueadas, com a dica "Etapa futura" (Atendimento, Campanhas) ou "Conecte o WhatsApp
  para liberar esta área" (`:378-411`). Clicar numa bloqueada não navega (`:392-396`).
- Seção aberta: sem conexão, sempre "Conexão"; conectado, "Automações" (ou a que o usuário escolher) (`:241`).

### 3.2 "Conexão" — cartão "Conexão com o WhatsApp" (shell `:421-607`)

- Título e "Conecte o WhatsApp atual da empresa por QR Code. A API Oficial da Meta será adicionada depois, sem misturar os canais."
  (`:93-94,478-485`).
- **"Conectar por QR Code"** com o selo de estado (`:491-509`); "Número: +{display_number}" quando houver (`:511-513`); erro
  vermelho só se já conectou antes ou se o estado é erro/bloqueio (`:515-522`).
- Sem conexão pronta: passo a passo (`WhatsappPairingSteps.tsx`): "Abra o **WhatsApp** no seu celular."; "Toque em **Mais opções**
  no Android ou em **Configurações** no iPhone."; "Toque em **Dispositivos conectados** e, em seguida, em **Conectar
  dispositivo**."; "Aponte a câmera para o **QR Code** desta tela." (`:28-58`). Caixa: "Entendo que toda automação de WhatsApp
  fora da API Oficial da Meta tem um risco, ainda que ínfimo, de bloqueio do número, justamente por se tratar de envio
  automatizado." (`:542-547`). Dica: "Pode ser melhor usar um número secundário. Se a empresa tiver um chip separado para os
  avisos, o WhatsApp principal de atendimento segue funcionando em qualquer cenário." (`:551-554`).
- Botão: **"Conectar meu WhatsApp"** (desligado sem o aceite) → "Gerar novo QR Code" (com QR na tela) → "Confirmar e ativar"
  (conectado sem aceite) (`:574-579`). Ao clicar: barra "Preparando a conexão e gerando o QR Code…" (`:561-565`), edge
  `whatsapp-connect` com `accepted_risk: true`, `risk_terms_version: '2026-10-16.3'` (`hooks/useWhatsappConnections.ts:114-130`),
  toast "QR Code gerado"; erro: "Não foi possível conectar" (`:446-453`).
- QR: caixa branca com o código (imagem ou desenhado a partir do texto) e "WhatsApp → Aparelhos conectados → Conectar aparelho"
  (`:524-533`).
- Conectado e ativo: "Desconectar" e selo "Canal ativo"; conectado e não ativo: "Usar este canal" (edge
  `whatsapp-connection-select`, toast "Canal ativado" — "Os próximos avisos usarão este número.") (`:455-463,567-573`).
- "Meta Cloud API" + "Em breve" — "Conexão oficial pelo Facebook, com mais estabilidade e escala. Os custos da Meta serão separados
  do plano Dominex." (`:586-598`). Rodapé: "O Dominex reduz o risco com consentimento, fila, aquecimento e limites. Nenhuma
  integração por QR Code consegue garantir ausência de bloqueio." (`:599-602`).

### 3.3 "Automações" — "Proteção do número" (prot)

- "Proteção do número" — "Regras que fazem os avisos saírem no ritmo de uma pessoa, e não de um robô. Reduzem o risco de bloqueio
  e de reclamação do cliente." (prot `:30-32`).
- "Horários de envio" ("Fuso horário configurado para a empresa."): **"Avisos de serviço"** — "Técnico a caminho, serviço iniciado
  e serviço concluído. O cliente está esperando essa mensagem no momento em que ela acontece…"; **"Lembretes de cobrança"** —
  "Cobrança gerada, lembrete de vencimento e aviso de atraso. Evite madrugada e domingo…"; cada uma com "Começa às", "Termina às"
  (horas cheias) e "Dias da semana" (Seg a Dom; "Mantenha pelo menos um dia marcado para esta janela.") (prot `:33-43,175-305`).
  "Fora do horário, a mensagem fica na fila e sai na próxima abertura." (`:44,205`). O lembrete de visita agendada usa a janela dos
  lembretes (auto `:94`; `lib/whatsappAutomation.ts:41-46`).

### 3.4 "Automações" — "Automação de mensagens" (auto)

- Cabeça: "Automação de mensagens" — "Defina quais avisos serão enviados e como cada mensagem será montada."; "{n} fluxos ativos";
  interruptor **"Ativar automações"** ("Os envios só começarão quando um provedor for conectado."); selo "Alterações não salvas" /
  "Configurações salvas"; **"Salvar configurações"** ("Salvando…") (auto `:55-62,255-290`).
- Abas "Ordens de serviço" / "Cobranças" (`:299-303`); lista "Escolha quando enviar" — "Toque em um evento da lista para editar a
  mensagem dele aqui embaixo." (selo "Editando", "Ativa"/"Inativa"): OS "Lembrete de visita agendada" ("Antes da data marcada para
  a visita"), "Técnico a caminho" ("Quando o técnico inicia o deslocamento"), "Serviço iniciado", "OS concluída"; cobranças
  "Cobrança gerada" ("Manual ou criada por uma assinatura"), "Antes do vencimento", "No vencimento", "Após o vencimento" ("Somente
  se a cobrança continuar pendente") (`:96-105,310-395`).
- Editor do evento: "Enviar esta mensagem"; "Modelo da mensagem" + "Os textos finais serão vinculados aos templates aprovados pelo
  provedor."; lembrete: "Quando enviar o lembrete" ("1 dia antes · recomendado" / "No dia") e o aviso da janela; OS: "Incluir link
  de acompanhamento da OS"; cobranças: "Quantos dias antes" (3) / "Quantos dias depois" (2), "Informações da cobrança" ("Valor",
  "Link de pagamento") (`:401-505`; padrões `lib/whatsappAutomation.ts:111-124`).
- "Somente clientes com a opção "Receber mensagens pelo WhatsApp" ativa serão considerados." (`:512`).
- **"Prévia da mensagem"** — "Dados ilustrativos — nenhuma mensagem será enviada nesta etapa." / "As mensagens automáticas são
  enviadas em português (Brasil)."; balão com "Sua empresa", "Prévia ilustrativa" e o texto (ex.: "Olá, Mariana! / Boas notícias:
  o técnico Carlos já está a caminho para atender você na OS #1048. / *Acompanhe a OS:* https://www.dominex.app/os/1048") (`:519-540`;
  `lib/whatsappAutomation.ts:338-420`; "Rotação automática" mostra o estilo "Cordial", `:352-354`).
- Salvar: `INSERT`/`UPDATE company_whatsapp_settings` (`enabled`, `automation_preferences`, `trigger_a_caminho`,
  `trigger_em_andamento`, `trigger_concluida`) → "Configurações de WhatsApp salvas." (shell `:243-257`; `hooks/useWhatsappSettings.ts:66-110`).

### 3.5 "Atendimento", "Modelos", "Campanhas" (`WhatsappCapabilityPreviews.tsx`)

- Atendimento (bloqueado): prévia "Conversas" com contato fictício "Mariana Souza" e "Conecte o provedor para responder por aqui"
  (`:50-146`). Campanhas (bloqueado): "Campanhas e comunicados" — "Etapa futura" (`:285-311`).
- **Modelos** (abre com conexão): "Modelos de mensagem" — "Variações transacionais usadas no QR Code; templates oficiais serão
  sincronizados com a Meta em uma etapa futura." — "7 estruturas previstas", lista com "Após conectar"; "Custos e franquia" (QR Code,
  API Oficial, Proteção) (`:191-271`). É texto fixo: nada se edita aqui (P7).

### 3.6 "Histórico" (shell `:609-642`)

"Fila e histórico de envios" — "Últimos 50 avisos transacionais. Mensagens ignoradas mostram o motivo."; contadores "Na fila"
(soma fila, processando e nova tentativa), "Enviado", "Entregue", "Lido", "Ignorado", "Falhou"; lista dos 15 mais recentes: evento
("OS · …"/"Cobrança · …"), data e hora (`toLocaleString('pt-BR')`), motivo e selo ("Na fila", "Processando", "Nova tentativa",
"Enviado", "Entregue", "Lido", "Ignorado", "Falhou", "Cancelado"). Vazio: "Nenhum aviso entrou na fila ainda." Atualiza a cada 10 s
(`hooks/useWhatsappConnections.ts:95-112`). Motivos de "Ignorado" vêm do servidor: "O cliente não autorizou mensagens pelo
WhatsApp.", "Cliente sem WhatsApp válido cadastrado.", "O cliente pediu para parar os envios.", "Esse número não tem WhatsApp.",
"A origem não existe mais ou a cobrança já foi paga." (`whatsapp-send-worker/index.ts:852-1052`).

### 3.7 Autorização na ficha do cliente (`components/customers/CustomerFormDialog.tsx:508-533`)

Bloco com o ícone do WhatsApp: **"Receber mensagens pelo WhatsApp"** — "Permite avisos de ordens de serviço, cobranças e vencimentos.
Pedidos de cancelamento do cliente sempre prevalecem."; sem celular válido (10+ dígitos): "Informe um celular válido para liberar
esta opção." e interruptor desligado (`lib/i18n/messages/app/customers.ts:100-102`). Padrão **ligado** (`:60,88,209`) e salvo só com
celular (`:285-286`). O cliente que responde "parar", "sair", "cancelar"… sai da lista (`supabase/functions/whatsapp-webhook/index.ts:67-70,458-507`).

### 3.8 O que o cliente recebe (texto montado no envio, `supabase/functions/whatsapp-send-worker/index.ts`)

Não aparece na tela do app (só a "Prévia ilustrativa"), mas é o que a fala pode descrever e o que uma ilustração mostraria:

- **OS** (`:567-631`): "Olá, {cliente}!", linha em branco, a frase do estilo e, com o link ligado, "*Acompanhe a OS:*
  https://dominex.app/os-tecnico/{código}?modo=cliente". Em "Cordial": "Boas notícias: o técnico {técnico} já está a caminho para
  atender você na OS #{n}."; "Seu atendimento começou. O técnico {técnico} já está realizando o serviço da OS #{n}."; "Seu
  atendimento foi concluído com sucesso. Agradecemos pela confiança na nossa equipe!". Sem técnico ou sem serviço, entram "nosso
  técnico" e "seu atendimento"; lembrete sem hora, "horário não informado" (`:591-600`).
- **Cobrança** (`:633-696`): só sai se a cobrança seguir "PENDING" ou "OVERDUE"; "Olá, {cliente}!", a abertura do estilo com o nome
  da empresa em negrito ("A *{empresa}* lembra que sua cobrança vence em 3 dias."), "*Valor:*", "*Vencimento:*", "*Pagar agora:*
  https://dominex.app/pagar/{código}", e o fecho "Se você já realizou o pagamento, desconsidere esta mensagem." / "Em caso de dúvida,
  fale com a nossa equipe por aqui.".
- **"Rotação automática"** sorteia, a cada envio, entre "Objetiva", "Cordial" e "Detalhada" (`:203-207`).

---

## 4. Backend por tela

### 4.1 Chamadas

| Tela / ação | Tabelas | Edge / RPC / externo | Linhas |
|---|---|---|---|
| Abrir a subaba | `company_whatsapp_settings` (select da empresa; consulta a cada 4 s se `connection_status='qr'`), `whatsapp_connections` (select; a cada 4 s com `qr`/`connecting`), `whatsapp_send_jobs` (50 últimos, a cada 10 s), `company_modules` | — | `hooks/useWhatsappSettings.ts:48-64`; `hooks/useWhatsappConnections.ts:76-112` |
| Conectar | (a edge grava `whatsapp_connections`: `status`, `risk_accepted_at/by`, `risk_terms_version`, `instance_name`; e `company_whatsapp_settings.connection_status`) | edge `whatsapp-connect` → Evolution (`qr`, `pairing_code`, `message`, `connection_status`) | `supabase/functions/whatsapp-connect/index.ts:68-560` |
| Leitura do QR no celular | webhook marca a conexão `connected`, `display_number`, `connected_at` e, sem canal ativo, `active_connection_id` | edge `whatsapp-webhook` (`CONNECTION_UPDATE`) | `supabase/functions/whatsapp-webhook/index.ts:269-396` |
| Usar este canal / Desconectar | — | edges `whatsapp-connection-select` (exige `connected`), `whatsapp-connection-disconnect` | `whatsapp-connection-select/index.ts:28-34`; `hooks/useWhatsappConnections.ts:132-158` |
| Salvar regras | `company_whatsapp_settings` insert/update | — | `useWhatsappSettings.ts:66-110` |
| Envio (servidor) | gatilhos de status da OS e de cobrança enfileiram `whatsapp_send_jobs` (`os.a_caminho`, `os.em_andamento`, `os.concluida`, `os.scheduled_reminder`, `billing.*`) | `whatsapp-send-worker` (cron) | `supabase/migrations/20261016143000_...sql:150-196,344-383`; `20261027130000_whatsapp_lembrete_os_agendada.sql:100,131` |
| Ficha do cliente | `customers.whatsapp_notifications_enabled` (+ gatilho que carimba `whatsapp_opt_in_at`) | — | `CustomerFormDialog.tsx:285-286`; `supabase/migrations/20261016233000_customers_whatsapp_opt_out_por_padrao.sql:1-60` |

### 4.2 Comparação com o backend falso (`/home/claude/domiflix/rec/fakebase`)

| Precisa | Situação | O que fazer |
|---|---|---|
| `company_whatsapp_settings`, `whatsapp_connections`, `whatsapp_send_jobs` | **sem semente** (nenhuma das três em `seeds/` nem em `seeds-extra/t1`, `t3`, `t4`; a gravação do T1 já as pediu como `TABELA_SEM_SEED` no `desconhecidos.log`, que é reescrito a cada gravação) | vazias no começo; o histórico ganha linhas no corte do bloco 8 |
| `company_modules` com `whatsapp` | **já existe** (`seeds/gen-01-tenant.json`, 13 módulos) | — |
| Edge `whatsapp-connect` | **sem handler** (`handlers/functions/`) | criar: grava a conexão `qr` e devolve um texto qualquer como QR (nada de código de pareamento real) |
| "Leitura do QR" | o webhook real vem da Evolution | passo de bastidor (endpoint `/__dev` ou semente trocada) que marca `connected`, `display_number`, `connected_at`, `active_connection_id` |
| Edges `whatsapp-connection-select`, `whatsapp-connection-disconnect` | **sem handler** | criar (o segundo só se a decisão 5 for clicar) |
| `customers.celular` e `whatsapp_notifications_enabled` | sementes de cliente sem esses campos definidos (a confirmar no `schema.json`) | definir na semente: hotel autorizado; um cliente sem autorização para o "Ignorado" |

---

## 5. Pegadinhas para roteiro e gravação

- **P1. [handoff, texto] Evento com chave técnica no histórico.** A lista troca só o prefixo: "OS · a_caminho", "OS · em_andamento",
  "OS · concluida", "OS · scheduled_reminder", "Cobrança · created"… (`SettingsWhatsappContent.tsx:633`). A fala diz "técnico a
  caminho", "serviço iniciado", e a câmera não dá zoom no texto da chave.
- **P2. [handoff] Faixa que nunca aparece.** "Conecte o WhatsApp para liberar as configurações" só sai fora da "Conexão", mas sem
  conexão a tela sempre fica em "Conexão" (`:241,293-300`).
- **P3. A tela troca de seção sozinha.** Quando a consulta de 4 s vê a conexão pronta, a seção vira "Automações" (`:236-241`): o
  robô espera essa troca e só então segue.
- **P4. [handoff, texto] Dois nomes para o mesmo menu do celular.** Passo a passo: "Dispositivos conectados" → "Conectar
  dispositivo" (`WhatsappPairingSteps.tsx:47-50`); legenda do QR: "WhatsApp → Aparelhos conectados → Conectar aparelho"
  (`SettingsWhatsappContent.tsx:531`).
- **P5. [handoff, texto] Dica do interruptor desatualizada.** "Os envios só começarão quando um provedor for conectado." continua
  depois de conectado (auto `:58`).
- **P6. [handoff, texto] Prévia com empresa de exemplo.** Os textos de cobrança da prévia citam "*Clima Forte Serviços*" e o
  link `https://www.dominex.app/pagar/8F2K9Q` (`lib/whatsappAutomation.ts:338-350,407-420`), não a empresa logada. A fala chama de
  "exemplo ilustrativo", como a tela.
- **P7. "Modelos" é só vitrine.** Texto fixo ("7 estruturas previstas", "Após conectar") (`WhatsappCapabilityPreviews.tsx:191-206`);
  o modelo de cada mensagem se escolhe em "Automações" › "Modelo da mensagem".
- **P8. Atendimento e Campanhas** são prévias com cadeado (etapa futura, `TRILHA` ⚠️). Não clicar, só citar.
- **P9. [handoff, texto] "Comportamento humano" sumiu da tela e ficou sempre ligado.** Decisão de 16/10: digitação simulada e "marcar
  como lida" sempre ligados, sem escolha (`lib/whatsappAutomation.ts:224-240`); o comentário da interface ainda diz "Nasce
  DESLIGADO" (`:60-64`) e os textos "Comportamento humano", "Marcar a conversa como lida…" seguem no i18n sem uso (prot `:45-50`). O
  envio marca a conversa como lida (`whatsapp-send-worker/index.ts:1066`): some o aviso de não lida no celular da empresa.
- **P10. Quem conecta ≠ quem configura.** Regras: admin/gestor ou "Gerenciar Configurações"; conectar/desconectar: só admin/gestor
  (`SettingsWhatsappContent.tsx:208,346`). A faixa "Configuração somente para leitura" cita só as regras.
- **P11. Uma conexão QR por empresa** (`20261016143000_...sql:39`): "trocar a conexão principal" da trilha só existe entre QR e Meta,
  e a Meta está "Em breve".
- **P12. Número cru e data do navegador.** "Número: +552130001000" sem máscara (`:511-513`); a hora do histórico usa o fuso do
  navegador, não o da empresa (`:633`).
- **P13. "Na fila" soma três estados** (pendente, processando, nova tentativa) (`:615-617`).
- **P14. [handoff, LGPD] (baixa) Cliente nasce autorizado.** Desde 16/10 o padrão é "ligado" no banco e no formulário, e o gatilho
  grava `whatsapp_opt_in_at` na criação, sem pedido do cliente (`supabase/migrations/20261016233000_...sql:1-60`;
  `CustomerFormDialog.tsx:60,88,209`). A migration registra a decisão e deixa o *backfill* para decisão de LGPD; o carimbo de "opt-in"
  passa a não significar consentimento. A fala apresenta o interruptor como a autorização do cliente e a resposta "parar" como saída.
- **P15. Sem limite e sem preço na tela.** O módulo é ilimitado desde 28/10 (`20261028140000_...sql:1-27`), mas o envio ainda tem o
  motivo "Limite mensal do módulo atingido." (`whatsapp-send-worker/index.ts:901`; a confirmar se ainda acontece). O preço do
  módulo está na migration: nunca mostrar a tela de Assinatura nem o "Contratar módulo".
- **P16. QR e celular são de terceiros.** O QR da gravação é simulado e o celular lendo o código é ilustração genérica, sem a
  interface nem a marca do aplicativo de mensagens (`PRODUCAO.md`, celular genérico). O ícone do WhatsApp que a própria tela mostra
  continua (é da interface).
- **P17. O histórico só tem linhas depois de um evento** de OS ou cobrança com a conexão ativa; logo após conectar ele está vazio.

## 6. 🚫 Não prometer

- Atendimento (caixa de conversas) e Campanhas: etapas futuras.
- API oficial da Meta ("Em breve"), mais de um número, troca automática de canal.
- Botão de reenviar/"nova tentativa" no histórico (é estado da fila).
- Escolher "marcar como lida" ou "digitando" (fora da tela, P9).
- Editar os textos das mensagens (há quatro estilos prontos).
- Garantia contra bloqueio do número (a própria tela diz que não há).
- Mensagens em outro idioma além do português (auto `:87`).

## 7. Dúvidas em aberto (só rodando)

1. O texto exato que o selo mostra entre "Conectar meu WhatsApp" e o QR (estado `connecting` vs `qr`) com o handler simulado.
2. Se `company_whatsapp_settings` sem linha deixa "Ativar automações" desligado e os padrões de `lib/whatsappAutomation.ts:92-125`.
3. Onde fica o celular usado pela fila (celular do cliente ou do contato principal) para a semente do hotel.
4. Se o worker ainda pula por "Limite mensal do módulo atingido." (P15).

## 8. Termos e pronúncias

WhatsApp ("uótsáp", a do perfil se houver), QR Code (perfil), Meta ("méta"), API ("a-pê-i"), OS ("ó-ésse").
