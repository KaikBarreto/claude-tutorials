# Plano · T27 White Label

- **Título:** White Label (o da fonte). 🔒 módulo `white_label`. Aula nova.
- **Objetivo:** deixar o sistema com a cara da Recicla Vale Metais: ícone quadrado, interruptor "White Label Ativo",
  "Cor Primária" salva, e ver onde a marca aparece e que vale para a equipe inteira.
- **Antes:** T1 "Sua conta e sua empresa". **Próximo:** T20 "Portal do Cliente e Fornecedor".
- **Vinhetas (áreas):** WHITE LABEL · MARCA · WHITE LABEL · COR · DOCUMENTOS · EQUIPE · RESUMO.
- **Alvo da fonte:** ~7 min. Desktop 1280×800 (o botão de recolher o menu só existe a partir de 1280 px), logado como
  Rafael Nogueira; no cap06, uma sessão da Juliana Prado. Base: `T27/inventario.md`.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00`.

## Estado de partida
Recicla Vale Metais depois do T1 e do T2: **logo horizontal** já enviado no T1 (`companies.logo_url`), **sem ícone**
(`icon_url` nulo), `white_label_enabled` falso, `white_label_primary_color` e `white_label_company_name` nulos; módulo
`white_label` em `company_modules` (`removed_at` nulo); Juliana Prado ativa (T2); pedidos do histórico em "Pedidos".
Menu lateral aberto, estilo "Menu Lateral", tema claro.

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área · título) | O que a tela mostra | Cuidados na fala | Fonte |
|---|---|---|---|---|
| 0 | (sem vinheta) | Dashboard com o logo do EcoSistema no menu. Ilustração: o sistema trocando de marca. | 🔒 depende do plano; "Antes: Sua conta e sua empresa" | abertura |
| 1 | WHITE LABEL · O que muda | "Configurações" → "Empresa" → "Identidade Visual" → gaveta "White Label" ("Personalize o sistema com sua marca") aberta: "White Label Desativado", "O logo da EcoSistema está sendo exibido". Ilustração: muda × continua. | 🚫 domínio, e-mail, login, segunda cor e tema escuro próprio | 00:00 |
| 2 | MARCA · O logo e o ícone | "Logo da Empresa" (o do T1) e "Recomendado: formato horizontal..."; "Ícone da Empresa (1:1)" → quadrado "1:1" → arquivo → "Ícone atualizado com sucesso!". Ilustração: qual imagem vai onde. | ⚠️ 5 MB e só imagem | 01:00 |
| 3 | WHITE LABEL · Ligar o White Label | Interruptor → "White Label ativado! ..."; "White Label Ativo", selo "Ativo"; o logo da Recicla Vale no menu; recolher o menu → o ícone; abrir de novo. | ⚠️ sem logo o interruptor trava; ⚠️ ícone só com o menu recolhido e o White Label ligado | 02:30 |
| 4 | COR · A cor da marca | "Personalizações": "Nome Exibido no Sistema" (vazio), "Cor Primária" `#1F5FAD`, "Preview", "Salvar Personalizações" → "Configurações de White Label salvas!"; botões e menu no azul. | 🚫 o nome exibido não aparece nas telas; ⚠️ vazio = verde padrão, "Reset" só limpa | 03:30 |
| 5 | DOCUMENTOS · Onde a marca aparece | Ilustração do mapa (menu, cabeçalho, comprovante térmico, A4, PDFs, Portal); "Pedidos" → "Ver comprovante" → o PDF sem o rodapé do EcoSistema; ilustração do Portal. | ⚠️ remover o logo não desliga o interruptor | 05:00 |
| 6 | EQUIPE · A empresa toda, na hora | Sessão da Juliana: Dashboard com o logo e o azul. Ilustração: a troca chegando a todos. | sem sair e entrar de novo | 06:00 |
| 7 | RESUMO · Recapitulando | Montagem: ícone, interruptor, cor, comprovante, sessão da Juliana. "Próximo: Portal do Cliente e Fornecedor". | "Até lá!" | recap |

Transições faladas: 0→1 "Vamos ver onde fica e o que ele troca"; 1→2 "Tudo começa pelas imagens"; 2→3 "Com as imagens no
lugar, é hora de ligar"; 3→4 "Agora a cor"; 4→5 "E onde isso aparece?"; 5→6 "E a equipe?".

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)
| Item | Valor |
|---|---|
| Logo horizontal da Recicla Vale | o do T1 (`recicla-vale-logo.png`); se o T1 ainda não tiver, desenhar por código: "Recicla Vale Metais" em azul-aço `#1F5FAD`, com um símbolo simples (duas chapas dobradas em "V"), ~600×160 px. Precisa ler bem no menu, que é escuro por padrão, e no papel do comprovante: sugestão, o desenho sobre uma placa branca de cantos arredondados. Nada de marca real |
| Ícone quadrado | `recicla-vale-icone.png`, 128×128 px, PNG transparente, o mesmo símbolo do logo |
| Cor da marca | **`#1F5FAD`** (azul-aço), digitada no campo da "Cor Primária" |
| "Nome Exibido no Sistema" | fica vazio (🚫) |
| Pedido para o comprovante | o mais recente da lista em "Pedidos" (histórico da semente), com itens e pagamento; formato do comprovante = o do T1 |
| Juliana Prado (cap06) | a do T2: `juliana.prado@reciclavalemetais.example`, senha `Escritorio#2026`, com a tela "Dashboard" |
| Estado final | ícone enviado, White Label ligado, cor `#1F5FAD`, nome exibido vazio. **Atenção:** a partir daqui o app fica azul e com o logo da Recicla Vale; as aulas gravadas depois do T27 que não forem de White Label partem de uma semente com o White Label desligado |

## Gravação
- **Rotas:** `/dashboard`, `/configuracoes` (aba "Empresa"), `/pedidos` e a janela nova do comprovante (pop-up liberado
  no robô). Desktop 1280×800.
- **Outro usuário:** cap06 abre um segundo navegador logado como Juliana Prado (login fora do vídeo).
- **Sementes:** `inicio` (logo, sem ícone, White Label desligado; caps 0 a 2), `apos-cap02` (+ ícone; cap03),
  `apos-cap03` (+ White Label ligado; cap04), `apos-cap04` (+ cor `#1F5FAD`; caps 5 a 7).
- **Setup fora do vídeo:** caps 3 e 4 abrem "Configurações" → "Empresa" e a gaveta "White Label".
- **Backend a simular:** storage `avatars` (`upload`, `getPublicUrl`, `remove`); updates em `companies` (`icon_url`,
  `white_label_enabled`, `white_label_company_name`, `white_label_primary_color`); `company_modules` com `white_label`;
  pedido, itens e pagamentos para o comprovante. O realtime em `companies` não é preciso (o cap06 abre uma sessão nova).
- **Arquivos:** `recicla-vale-icone.png` (e o logo, se o T1 não tiver), desenhados por código.
- **Câmera:** com o menu recolhido, o mouse fica longe do menu (passar por cima abre de novo); sem zoom no campo
  "Nome Exibido no Sistema".
- **Ilustrações** (desenho por código ou cena HTML, `docs/09-aula-ilustrada.md`): cap00 o sistema trocando de marca;
  cap01 o que muda e o que continua; cap02 qual imagem vai onde; cap05 o mapa de onde a marca aparece, o Portal
  (topo na cor, rodapé sai) e remover o logo × desligar; cap06 a troca chegando aos três da equipe.

## Riscos e decisões para o Kaik
1. **Estado do T1:** o T27 parte com o logo do T1 e **sem** o ícone (o cap02 envia o ícone, que é a imagem do White
   Label). Se o T1 enviar o ícone, a semente do T27 tira, ou o cap02 vira "Substituir".
2. O aviso "Faça upload do logo ao lado para poder ativar o White Label" não aparece na tela (o logo já existe); entra
   só na fala. Para mostrar, seria preciso começar sem logo, o que contradiz o T1.
3. O Portal entra como ilustração (a página real é do T20, que vem depois na trilha).
4. Portal só muda com a cor salva (inventário, achado 3): a fala diz "com a cor salva".
