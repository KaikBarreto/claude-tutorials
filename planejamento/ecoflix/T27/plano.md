# Plano · T27 White Label

- **Título:** White Label (o da fonte). 🔒 módulo `white_label`. Aula nova.
- **Objetivo:** deixar o sistema com a cara da Recicla Vale Metais: logo e ícone (do T1) no lugar, interruptor "White Label Ativo",
  "Cor Primária" salva, e ver onde a marca aparece e que vale para a equipe inteira.
- **Antes:** T1 "Sua conta e sua empresa". **Próximo:** T20 "Portal do Cliente e Fornecedor".
- **Vinhetas (áreas):** WHITE LABEL · MARCA · WHITE LABEL · COR · DOCUMENTOS · WHITE LABEL · EQUIPE · RESUMO.
- **Alvo da fonte:** ~7 min (a versão 1.60.22 passa de 6 para ~8 min e meio, a pedido do Kaik: cobrir tudo, nenhuma aula se divide).
  Desktop 1600×900 (o botão de recolher o menu só existe a partir de 1280 px), logado como Rafael Nogueira; no cap07, uma sessão da
  Juliana Prado. Base: `T27/inventario.md`.
- **App:** EcoSistema 1.60.22 (21/11). As telas do White Label não mudaram desde o 1.59.154; mudou o que a aula cobre (ver `cobertura_160.md`).
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00`.

## Estado de partida
Recicla Vale Metais depois do T1 e do T2: **logo horizontal** e **ícone** já enviados no T1 (`companies.logo_url` e
`icon_url`; junção: o T1 manda os dois no cap05), `white_label_enabled` falso, `white_label_primary_color` e `white_label_company_name` nulos; módulo
`white_label` em `company_modules` (`removed_at` nulo); Juliana Prado ativa (T2); pedidos do histórico em "Pedidos".
Menu lateral aberto, estilo "Menu Lateral", tema claro.

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área · título) | O que a tela mostra | Cuidados na fala | Fonte |
|---|---|---|---|---|
| 0 | (sem vinheta) | Dashboard com o logo do EcoSistema no menu. Ilustração: o sistema trocando de marca. | 🔒 depende do plano; "Antes: Sua conta e sua empresa" | abertura |
| 1 | WHITE LABEL · O que muda | "Configurações" → "Empresa" → "Identidade Visual" → gaveta "White Label" ("Personalize o sistema com sua marca") aberta: "White Label Desativado", "O logo da EcoSistema está sendo exibido". Ilustração: muda × continua. | 🚫 domínio, e-mail, login, segunda cor e tema escuro próprio; 🔒 sem o módulo a gaveta não aparece (no teste vem liberado) | 00:00 |
| 2 | MARCA · O logo e o ícone | "Logo da Empresa" (o do T1) e "Recomendado: formato horizontal..."; "Ícone da Empresa (1:1)" com o ícone do T1 e "Recomendado: formato quadrado..." (sem enviar nada). Ilustração: qual imagem vai onde. | ⚠️ 5 MB e só imagem; ⚠️ sem ícone o menu recolhido fica com o do EcoSistema | 01:00 |
| 3 | WHITE LABEL · Ligar o White Label | Interruptor → "White Label ativado! ..."; "White Label Ativo", selo "Ativo"; o logo da Recicla Vale no menu; recolher o menu → o ícone; abrir de novo; dica do menu escuro (ilustração) e aba "Aparência" → "Menu (lateral e superior)" → "Seguir o tema" (só aponta). | ⚠️ sem logo o interruptor trava (só desligado); ⚠️ ícone só com o menu recolhido e o White Label ligado; ⚠️ logo de letra escura some no menu escuro | 02:30 |
| 4 | COR · A cor da marca | "Personalizações": "Nome Exibido no Sistema" (vazio), "Cor Primária" `#1F5FAD`, "Preview", "Salvar Personalizações" → "Configurações de White Label salvas!"; botões e menu no azul. | 🚫 o nome exibido não aparece nas telas; ⚠️ sem o "#" salva e não muda; ⚠️ vazio = cores padrão, "Reset" só limpa | 03:30 |
| 5 | DOCUMENTOS · Onde a marca aparece | Ilustração do mapa (menu, cabeçalho, comprovante térmico, A4, PDFs; 1.60.22: + tabela de preços, ticket de pesagem, fechamento de caixa); "Pedidos" → menu "⋮" do pedido → "Ver comprovante" → o PDF sem o rodapé do EcoSistema; QR com o logo (ilustração); Portal e o comprovante baixado pelo parceiro (ilustração); rosto no ponto e "Logo para Nota Fiscal" (ilustração). | só cita; a tela do Portal é do T20, a do ponto do T19, a da nota do T16 | 05:00 |
| 6 | WHITE LABEL · Desligar e voltar atrás (novo, 1.60.22) | Interruptor: "White Label desativado." → menu e cor voltam ao padrão → liga de novo e a cor continua guardada; "Remover" do logo: "Remover logo da empresa?" → "Logo removido com sucesso!" → "Nenhum logo enviado", cartão ainda "White Label Ativo" e o aviso âmbar "Faça upload do logo ao lado para poder ativar o White Label"; ilustração remover × desligar; envia o logo de novo. | ⚠️ remover o logo não desliga o interruptor (documentos seguem sem o rodapé); a cor fica guardada | cobertura |
| 7 | EQUIPE · A empresa toda, na hora | Sessão da Juliana: Dashboard com o logo e o azul. Ilustração: a troca chegando a todos. | sem sair e entrar de novo | 06:00 |
| 8 | RESUMO · Recapitulando | Montagem: ícone, interruptor, cor, comprovante, interruptor × remover o logo, sessão da Juliana. "Próximo: Portal do Cliente e Fornecedor". | "Até lá!" | recap |

Transições faladas: 0→1 "Vamos ver o que ele troca"; 1→2 "Tudo começa pelas imagens"; 2→3 "Com as imagens no
lugar, é hora de ligar"; 3→4 "Agora a cor"; 4→5 "E onde a marca aparece?"; 5→6 "E se um dia você quiser voltar atrás?"; 6→7 "E a equipe?".

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)
| Item | Valor |
|---|---|
| Logo horizontal da Recicla Vale | o do T1 (`recicla-vale-logo.png`); se o T1 ainda não tiver, desenhar por código: "Recicla Vale Metais" em azul-aço `#1F5FAD`, com um símbolo simples (duas chapas dobradas em "V"), ~600×160 px. Precisa ler bem no menu, que é escuro por padrão, e no papel do comprovante: sugestão, o desenho sobre uma placa branca de cantos arredondados. Nada de marca real |
| Ícone quadrado | `recicla-vale-icone.png`, 128×128 px, PNG transparente, o mesmo símbolo do logo |
| Cor da marca | **`#1F5FAD`** (azul-aço), digitada no campo da "Cor Primária" |
| "Nome Exibido no Sistema" | fica vazio (🚫) |
| Pedido para o comprovante | o mais recente da lista em "Pedidos" (histórico da semente), com itens e pagamento; formato do comprovante = o do T1 |
| Juliana Prado (cap06) | a do T2: `juliana.prado@reciclavalemetais.example`, senha `Escritorio#2026`, com a tela "Dashboard" |
| Estado final | logo e ícone do T1, White Label ligado, cor `#1F5FAD`, nome exibido vazio. **Atenção:** a partir daqui o app fica azul e com o logo da Recicla Vale; as aulas gravadas depois do T27 que não forem de White Label partem de uma semente com o White Label desligado |

## Gravação
- **Rotas:** `/dashboard`, `/configuracoes` (aba "Empresa"), `/pedidos` e a janela nova do comprovante (pop-up liberado
  no robô). Desktop 1280×800.
- **Outro usuário:** cap07 abre um segundo navegador logado como Juliana Prado (login fora do vídeo).
- **Sementes:** `inicio` (logo e ícone do T1, White Label desligado; caps 0 a 3; junção: não há mais `apos-cap02`),
  `apos-cap03` (+ White Label ligado; cap04), `apos-cap04` (+ cor `#1F5FAD`; caps 5 a 8). O cap06 (novo) não gera semente: termina igual a `apos-cap04`.
- **Setup fora do vídeo:** caps 3, 4, 6 e 8 abrem "Configurações" → "Empresa" e a gaveta "White Label".
- **Cap06:** o envio de volta usa o `recicla-vale-logo-claro.png` do mundo; no ensaio o upload cai num caminho novo do storage falso (a semente do próximo capítulo não depende dele).
- **Cap05:** o pedido do comprovante tem de ser o mais recente que **não** veio de ticket de pesagem (senão o PDF sai com "Ticket:" e "Caixa:").
- **Backend a simular:** storage `avatars` (`upload`, `getPublicUrl`, `remove`: usados de verdade no cap06); updates em `companies` (`logo_url`, `icon_url`,
  `white_label_enabled` nos dois sentidos, `white_label_company_name`, `white_label_primary_color`); `company_modules` com `white_label`;
  pedido, itens e pagamentos para o comprovante. O realtime em `companies` não é preciso (o cap07 abre uma sessão nova; o canal agora se chama `company-updates:<empresa>:<uuid>`).
- **Arquivos:** `recicla-vale-icone.png` (e o logo, se o T1 não tiver), desenhados por código.
- **Câmera:** com o menu recolhido, o mouse fica longe do menu (passar por cima abre de novo); sem zoom no campo
  "Nome Exibido no Sistema".
- **Ilustrações** (kit v3 pendente, `cenas/ilustracoes.json`): cap00 o sistema trocando de marca; cap01 o que muda e o que
  continua; cap02 qual imagem vai onde; cap03 o logo no menu escuro (some × aparece); cap05 o mapa de onde a marca aparece (com os
  três cartões a mais), o PDF do comprovante, o QR com logo, o Portal, o rosto no ponto e a nota fiscal; cap06 remover o logo × desligar;
  cap07 a troca chegando aos três da equipe.

## Riscos e decisões para o Kaik
1. **Estado do T1:** o T1 envia o logo e o ícone (cap05), então o T27 parte com os dois e o cap02 só mostra o ícone e o
   "Substituir" (junção, decidido).
2. (Resolvido na 1.60.22) O aviso "Faça upload do logo ao lado para poder ativar o White Label" aparece na tela do cap06, quando
   o logo é removido com o White Label ligado. O interruptor **não** trava nesse estado (`CompanySettings.tsx:1145`: só fica
   desabilitado sem logo **e** desligado); a fala não diz que trava. Sem logo e desligado ele trava de verdade (cap03, só fala).
3. O Portal entra como ilustração (a página real é do T20, que vem depois na trilha).
4. Portal só muda com a cor salva (inventário, achado 3): a fala diz "com a cor salva".
