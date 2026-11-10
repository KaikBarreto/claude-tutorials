# T7 · handoffs para o time do app (achados do inventário e da gravação; app 1.38.9)

Lista curta, por prioridade. Referências do código lidas em `src-1.38.9/src` (a numeração P é a do `T07/inventario.md`).
Marcação: **[confirmado na gravação]** quando o robô viu o comportamento; os demais vêm da leitura do código.

## Média/alta
- **P23 · Resposta de assinatura no "modo resposta" vira texto cru.** `components/technician/DynamicFormQuestions.tsx:947-950, 1029-1047`
  (`showReadOnly` só exclui `photo`; o último `else` é `<p>{response.response_value}</p>`). Na assinatura o valor é `data:image/png;base64,...`
  (`:819-835`), então, depois de "Confirmar" (`components/SignaturePad.tsx:305, 326`), a pergunta mostra uma linha enorme de texto até tocar no lápis;
  a prévia com `<img alt="Assinatura">` só existe no estado de edição (`SignaturePad.tsx:224-232`). Vídeo gravado: texto vazio, URL em
  `response_video_url` (`:799-813`) -> parágrafo vazio. _Status na gravação: ver abaixo._
- **P14 · A linha de avaliação nasce sempre ao concluir.** `pages/TechnicianOS.tsx:2003-2013` insere `service_ratings` sem olhar "Gerar Pesquisa de
  Satisfação ao finalizar?"; o link público decide mostrar a pesquisa por `survey_enabled` = "existe linha"
  (`supabase/migrations/20260925120000_check_in_out_by_autoria_real.sql:476-478`). Com "Não" a pesquisa aparece mesmo assim.
- **P20 · OS "Em Andamento" sem check-in deixa o técnico sem ação** (arrastar no Kanban): `pages/TechnicianOS.tsx:3910-3941` (cartão só em
  pendente/agendada/a caminho) e `:4064, 4567, 4694` (checklist, rodapé e menu exigem `isCheckedIn || isPaused`).
- **P2 · "Exigir Assinatura" e outros dois interruptores não têm leitor.** `lib/i18n/messages/app/settings.ts:203-232`; `pages/Settings.tsx:214-218, 724-728`;
  o cartão de assinaturas só aparece com `require_tech_signature/require_client_signature` (`TechnicianOS.tsx:4242`), que só nascem em contrato/PMOC/API.
- **P7 · Sim/Não: o primeiro toque grava "Sim"**, e "Não" só pelo lápis. `DynamicFormQuestions.tsx:537-561, 950, 1029-1033`. **[confirmado na gravação]** (cap. 4)

## Baixa
- **P1 · "O app guarda rascunho do formulário" não é verdade** (cada resposta grava na hora; sem rascunho local). `components/pwa/OfflineIndicator.tsx:59-64`;
  `hooks/useOsMaterials.ts:95-98, 125, 437-445` (única exceção: linhas de material).
- **P3 · "Finalizar Parcial" existe em toda OS em atendimento** (a trilha diz que é só de contrato). `pages/TechnicianOS.tsx:4730-4738, 3353-3370`.
- **P9 · O campo Número não mostra a unidade** (A, psi, °C). `DynamicFormQuestions.tsx:654-669` (só a "Medida PMOC" mostra unidade, `:675-736`).
- **P11 · "Registro Fotográfico" do relatório lê `os_photos`, que nada alimenta** (fotos do técnico vão em `form_responses.response_photo_url`).
  `components/technician/OSReport.tsx:316-318, 1307-1314`.
- **P19 · Visão do cliente sem texto para "Agendada".** `pages/TechnicianOS.tsx:3025-3028`.
- **P22 · O aviso de vídeo pesado cita o botão "Gravar vídeo", que se chama "Gravar".** `lib/i18n/messages/app/os.ts:1542, 1555`.
- **P24 · Textos fixos fora do i18n:** `components/SignaturePad.tsx:188-337` ("Tela cheia", "Limpar", "Confirmar", "Assinatura"), pesquisa de
  satisfação `components/.../OSRatingSurvey.tsx:213-480`, faixa "Sem conexão…" `OfflineIndicator.tsx:64`.

## Achados da gravação
- App 1.38.19: `components/technician/OsPhotoField.tsx:351-352` (botão remover foto só tem `title`, sem texto: o robô acha por `button[title='Remover foto']`); remover pede confirmação (`:395-399`).
- Mapa da rota do técnico (MapLibre) deixa o navegador de gravação ocupado ~7 s; é efeito do desenho por software, não do app.
- Rodapé da gaveta Consumir do estoque (Adicionar/Fechar) é fixo: gravado por toque sintético. Estoque: Fita isolante 28 após consumir 2 rolos (informado ao T8).
- P23 (assinatura como texto cru) não foi conferido nos quadros da 1.38.19; P7 confirmado antes na gravação (cap. 4).

## Achados da fase 1 da 1.38.21 (05/11)
- **App:** "Retomar OS" (cap07 e cap08) fica cinza-escuro sobre o rodapé quase preto: texto legível, botão com pouco destaque. Quadros em `rec/t7/quadros_1.38.21/retomar_os/`.
- **App:** o cartão da Agenda de uma OS de 60 min (56 px) deixa o texto transbordar sobre o cartão da hora seguinte; o clique no texto abre a OS vizinha (o robô clica no cartão, não no texto).
- **App:** o cadastro rápido de equipamento da gaveta "Editar OS" pede os campos obrigatórios personalizados da empresa (aqui, "Tensão *").
- **Gravador (fora do meu escopo):** com `FAKE_URL` diferente da URL gravada no build, `route.fetch({url})` em `rec/recorder/net.mjs:52` perde o corpo binário do XHR (a foto subia com 0 byte, "Imagem indisponível"). Contornado em `gerar.py` (SLOW_UPLOAD envia direto ao falso). Vale consertar no gravador.
- **Arrasto (`@dnd-kit`):** o passo `drag` do robô funciona no celular emulado; o aviso "Solte aqui para vincular" só fica visível enquanto o dedo paira (o gravador segura 0,22 a 0,38 s).
