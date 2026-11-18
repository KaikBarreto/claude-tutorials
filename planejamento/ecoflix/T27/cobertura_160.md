# Cobertura 1.60.10 · T27 White Label

Auditoria só de leitura (código em `/dev/shm/ecoflix-src`, `APP_VERSION = "1.60.10"`; comparação com `f37573ea0`).
Caminhos relativos a `src/`. Não havia `t27.txt` da varredura do robô. Nada foi editado fora deste arquivo.

**Resumo:** as telas do White Label não mudaram entre 1.59.154 e 1.60.10. `components/CompanySettings.tsx`,
`components/layout/SidebarMenuContent.tsx`, `TopNavbar.tsx`, `hooks/useWhiteLabelTheme.tsx`, `pages/EntityPortal.tsx`,
`pages/Settings.tsx`, `index.css` e `hooks/usePageTitle.ts` estão idênticos byte a byte. O trabalho desta aula é cobertura,
não correção.

## 1. Mudou no app

| Cap. | O que o roteiro mostra | Como está no 1.60.10 | Onde | Efeito na aula |
|---|---|---|---|---|
| 05 | Comprovante do pedido (PDF) | O bloco de assinaturas, quando ligado, ganhou mais espaço em cima (14 mm no térmico) e passou a obedecer a `receipt_signature_mode` (as duas, só a do parceiro ou só a da empresa). Pedido que nasceu de ticket de pesagem mostra duas linhas, "Ticket: <nome>" e "Caixa: <nome>", no lugar de "Operador(a): <nome>" | `utils/thermalReceiptGenerator.ts` (linha do operador e bloco de assinatura); `utils/orderReceiptA4Generator.ts` ("Ticket:"/"Caixa:") | Só visual do PDF. Regravar o cap05 com um pedido que **não** veio de ticket, para a tela bater com o T1. O rodapé do EcoSistema segue a mesma regra (`thermalReceiptGenerator.ts:2480-2497`, `orderReceiptA4Generator.ts:1758-1775`) |
| 05 | "Pedidos" → "⋮" → "Ver comprovante" | Rótulos iguais. A lista agora só carrega para quem tem a tela (`canUseOrders`) e pode vir só com os pedidos do próprio usuário (`ordersOwnOnly`) | `pages/Orders.tsx:2675` ("Ver comprovante"), `:2265` (olho no celular), `:1187` ("Popup bloqueado. Permita popups para gerar comprovantes.") | Nenhum para o Rafael (MASTER). O robô só precisa das âncoras novas |
| 06 | "Vê a mudança na hora" | O realtime saiu do hook e foi para um canal compartilhado por empresa: `company-updates:<empresa>:<uuid>` no lugar de `white-label:<empresa>:<uuid>` | `hooks/useWhiteLabel.tsx:71-73`, `hooks/useCompanyUpdateSubscription.ts` | Comportamento igual, a fala continua certa. Se o mundo do robô filtrar pelo nome do canal, trocar |

Continua válida no 1.60.10 a troca já pedida em `propostas_fala.md` (cap04 L5: "volta às cores padrão" no lugar de "verde
padrão"): `index.css` não mudou.

## 2. Falta cobrir

| # | O que é (código) | Quando o cliente usa | Vale? |
|---|---|---|---|
| 1 | A gaveta "White Label" só existe com o módulo (`CompanySettings.tsx:151,1093`). Sem ele, não aparece nada, nem aviso. No período de teste o módulo vem junto (`hooks/useCompanyModules.tsx:325-331`; `supabase/functions/self-register/index.ts:564`) | Cliente que procura a gaveta e não acha; cliente em teste | **Sim, trecho** (cap01) |
| 2 | Sem ícone enviado, o menu recolhido fica com o ícone do EcoSistema, mesmo com o White Label ligado (`SidebarMenuContent.tsx:304`) | Quem só mandou o logo | **Sim, 1 frase** (cap02) |
| 3 | O menu é escuro por padrão e mostra o logo como veio, sem placa: logo de letra escura e fundo transparente quase some (`SidebarMenuContent.tsx:301-340`; achado 1 do ensaio). Saída no app: "Configurações" → aba "Aparência" → "Menu (lateral e superior)" → "Seguir o tema" ("Claro no tema claro, escuro no escuro") (`components/settings/SettingsAppearanceContent.tsx:82-134`) | Todo cliente com logo escuro | **Sim, trecho** (cap03). O ajuste de Aparência é do T1: aqui só aponta |
| 4 | A cor só entra se o código começar com "#" e tiver seis caracteres. Fora disso o "Salvar Personalizações" grava, mostra "Configurações de White Label salvas!" e nada muda, sem aviso (`hooks/useWhiteLabelTheme.tsx:5-15,52-55`; `CompanySettings.tsx:687-711` não valida) | Quem digita o código sem "#" ou copia errado | **Sim, 1 frase** (cap04) |
| 5 | Desligar o interruptor: "White Label desativado."; somem o selo "Ativo" e as "Personalizações"; menu, cor e rodapé dos documentos voltam. A cor fica guardada e volta ao religar (o desligar grava só `white_label_enabled`, `CompanySettings.tsx:659-685`) | Trocar de marca, testar, voltar atrás | **Sim, capítulo novo** |
| 6 | "Remover" do logo abre a confirmação "Remover logo da empresa?" / "O logo personalizado será removido e o logo padrão (símbolo de reciclagem) será usado nos comprovantes." / "Cancelar" / "Remover" (`CompanySettings.tsx:1698-1718`). Com o White Label ligado e sem logo: o menu volta ao EcoSistema, os documentos seguem sem rodapé, **o interruptor trava** (`:1148`) e aparece "Faça upload do logo ao lado para poder ativar o White Label" (`:1152-1157`). Não dá para desligar sem mandar um logo de novo | Quem remove o logo achando que desligou | **Sim, no capítulo novo.** Resolve o risco 2 do plano (o aviso âmbar passa a aparecer na tela, sem contradizer o T1) |
| 7 | "Remover" do ícone: "Remover ícone da empresa?" / "O ícone personalizado será removido e o ícone padrão será usado no menu lateral." (`:1721-1763`) | Raro | **Só citar** (junto do item 2) |
| 8 | Outros documentos sem o rodapé: tabela de preços (`utils/priceTableGenerator.ts:344`), ticket de pesagem (`utils/weighingTicketGenerator.ts:480`), fechamento de caixa, extratos, estoque, funcionários, DRE (lista do inventário §4) | Quem manda tabela de preços e relatório para parceiro | **Só citar** (cap05, 1 frase, mais cartões na ilustração) |
| 9 | QR das fotos no comprovante leva o logo da empresa no meio, com White Label e logo (`thermalReceiptGenerator.ts:2453`, `orderReceiptA4Generator.ts:1685`) | Quem usa o QR das fotos | **Só citar**. A opção do QR é do T1 |
| 10 | Portal: a cor vai também para botões, abas e selos (`pages/EntityPortal.tsx:936-940`); o comprovante baixado pelo parceiro sai sem rodapé só com o interruptor, mesmo sem cor (`supabase/functions/portal-order-receipt/index.ts:512`); a tela de espera da tabela de preços usa o logo da empresa (`components/portal/PortalPricesTab.tsx:165-167`) | Parceiro no Portal | **Só citar** 1 frase; o resto é do **T20** |
| 11 | Cadastro do rosto para o ponto (página que o funcionário abre): logo e cor da empresa com White Label (`pages/FaceEnrollment.tsx:53-56`) | Empresas com o módulo Funcionários | **Só citar**; a tela é do **T19** |
| 12 | Logo da nota fiscal é outro campo: "Logo para Nota Fiscal", "Aparecerá no DANFE (máx. 200KB).", "O logo da empresa será usado automaticamente ao salvar." (`components/notas-fiscais/EmpresaSection.tsx:422-426`). Desde a 1.60 a imagem fica guardada no sistema (nota de versão, `config/version.ts:101`) | Quem espera que o White Label mude a nota | **Só citar**; a tela é do **T16** |
| 13 | PIX da assinatura: o QR leva o logo da empresa no centro (`components/billing/PixPaymentView.tsx:71-74`); as telas de pagamento ignoram a cor da marca (`hooks/usePaymentLightTheme.ts`) | Dono pagando a assinatura | **Não**: é tela de assinatura (T0) e esbarra em preço |
| 14 | Estado vazio do logo: "Nenhum logo enviado", "PNG ou JPG, até 5MB" (`CompanySettings.tsx:880-896`) | Primeiro envio | **Sim**, aparece sozinho no capítulo novo (item 6). O envio em si é do T1 |
| 15 | Seletor de cor do navegador (`<input type="color">`, `:1176-1182`) | Quem não tem o código da cor | **Não abrir**: é janela nativa do navegador, não grava bem. Já citado na fala |
| 16 | Tema escuro com a cor mais clara; cabeçalho no menu superior e no celular | (já na fala e na ilustração) | **Não**: coberto |

Achados do app para o Kaik (não vão para a fala):
- Com White Label ligado e logo removido, o cartão segue dizendo "White Label Ativo" / "Seu logo está sendo exibido no lugar
  do logo EcoSistema", o que não é verdade naquele estado, e o interruptor fica preso em ligado (`CompanySettings.tsx:1135-1149`).
- "Nome Exibido no Sistema" continua sem uso no 1.60.10 (nenhum componente lê `customCompanyName`).
- Cor fora do formato é salva sem validação (item 4).
- O painel usa `hasModule` (plano e teste) e o menu usa só `company_modules` (`useWhiteLabel.tsx:47-54`): módulo vindo só do
  plano mostraria a gaveta sem trocar o menu. No teste não acontece (o cadastro grava `white_label` em `company_modules`).

## 3. Proposta

Capítulos passam de 7 para 8 vinhetas: o novo entra entre o cap05 e o cap06 atuais (vira cap06; Equipe vira cap07; Recap, cap08).

### 3.1 cap01, depois da linha 2 (trecho)
| Tela | Fala |
|---|---|
| A câmera fica na gaveta "White Label" ("Personalize o sistema com sua marca"). | Se essa gaveta não aparece pra você, é porque o módulo White Label não está no seu plano. No período de teste, ele já vem liberado. |

### 3.2 cap02, depois da linha 5 (1 frase)
| Tela | Fala |
|---|---|
| A câmera fica em "Ícone da Empresa (1:1)", nos botões "Substituir" e "Remover", sem clicar. | E se você não mandar o ícone? O menu recolhido continua com o ícone do EcoSistema, mesmo com o White Label ligado. |

### 3.3 cap03, depois da linha 4 (trecho)
| Tela | Fala |
|---|---|
| [ZOOM: o logo da Recicla Vale no topo do menu escuro] | Uma dica: o menu do sistema é escuro. Logo de letra escura, com fundo transparente, quase some aqui. Mande uma versão que apareça bem no fundo escuro. |
| [ILUSTRAÇÃO: o mesmo logo em duas faixas, uma escura (some) e uma clara (aparece); embaixo, o caminho "Configurações → Aparência → Menu (lateral e superior) → Seguir o tema".] | Ou, na aba Aparência, em Menu, escolha Seguir o tema. Aí o menu fica claro no tema claro. |

### 3.4 cap04, depois da linha 3 (1 frase)
| Tela | Fala |
|---|---|
| [ZOOM: o campo de texto da "Cor Primária" com "#1F5FAD"] | Um cuidado: o código começa com o jogo da velha e tem seis caracteres, como este. Sem o jogo da velha, o sistema salva, mas a cor não muda, e ele não avisa. |

Aplicar junto a troca do `propostas_fala.md` na linha 5.

### 3.5 cap05 (frases a acrescentar; a última linha atual, da dica de desligar, sai e vira o capítulo novo)
| Tela | Fala |
|---|---|
| (ilustração do mapa) Entram mais três cartões: "Tabela de preços", "Ticket de pesagem" e "Fechamento de caixa". | Vale também pra tabela de preços, pro ticket de pesagem, pro fechamento de caixa e pros outros relatórios. |
| (PDF do comprovante) [ILUSTRAÇÃO: um QR com o logo da Recicla Vale no meio.] | E, se você usa o QR das fotos no comprovante, o logo da Recicla Vale vai no meio do QR. |
| (ilustração do Portal, depois da linha atual) | E o comprovante que o parceiro baixa no Portal já sai sem o rodapé, mesmo sem cor salva. |
| [ILUSTRAÇÃO: dois cartões, "Cadastro do rosto no ponto" (com logo e cor) e "Nota fiscal" (com "Logo para Nota Fiscal", à parte).] | No cadastro do rosto pro ponto, o funcionário também vê o logo e a cor da empresa. Já o logo da nota fiscal é outro: ele fica nas Configurações Fiscais. |

### 3.6 Capítulo novo · "Desligar e voltar atrás" (vinheta: WHITE LABEL; título falado "Desligar e voltar atrás.")
Semente `apos-cap04`; o `setup` abre "Configurações" → "Empresa" e a gaveta "White Label" fora do vídeo. Não gera semente nova:
termina igual a `apos-cap04` (logo de volta, ligado, cor salva).

| Tela | Fala |
|---|---|
| A gaveta aberta: "White Label Ativo", selo "Ativo", "Personalizações" com "#1F5FAD". | E se um dia você quiser voltar atrás? Tem dois caminhos, e eles não fazem a mesma coisa. |
| Clica no interruptor: aviso "White Label desativado."; o cartão vira "White Label Desativado" ("O logo da EcoSistema está sendo exibido"); somem o selo "Ativo" e as "Personalizações". [BACKEND: update `companies.white_label_enabled` falso] | O primeiro é o interruptor. Desligo, e o sistema avisa: White Label desativado. |
| A câmera vai ao topo do menu (logo do EcoSistema) e volta ao botão, já sem o azul. | O menu voltou pro logo do EcoSistema, a cor voltou ao padrão, e os documentos voltam a sair com o rodapé. |
| Clica de novo no interruptor: "White Label ativado! Seu logo agora será exibido em todo o sistema."; as "Personalizações" voltam com "#1F5FAD" na "Cor Primária" e a tela fica azul. [BACKEND: update verdadeiro] | Ligo de novo. A cor da Recicla Vale continuou guardada: voltou tudo, sem digitar nada. |
| Coluna da esquerda, "Logo da Empresa": clica em "Remover"; abre "Remover logo da empresa?" ("O logo personalizado será removido e o logo padrão (símbolo de reciclagem) será usado nos comprovantes."); clica em "Remover": aviso "Logo removido com sucesso!"; a área vira "Nenhum logo enviado". [BACKEND: storage `avatars` `remove`; update `companies.logo_url` nulo] | O segundo caminho é remover o logo. A tela pergunta antes. Confirmo em Remover. |
| A câmera vai ao menu (logo do EcoSistema) e ao cartão "White Label Ativo", com o selo "Ativo". | Repara: o menu voltou pro logo do EcoSistema, mas o White Label continua ativo. E os documentos continuam sem o rodapé. |
| [ZOOM: o interruptor apagado e o aviso "Faça upload do logo ao lado para poder ativar o White Label"] | E o interruptor travou. Sem logo, não dá nem pra desligar. A tela pede o logo de volta. |
| Clica em "Nenhum logo enviado" e envia `recicla-vale-logo` (versão clara): "Logo atualizado com sucesso!"; o logo volta ao menu. [BACKEND: storage `upload` + `getPublicUrl`; update `logo_url`] | Então, pra desligar de verdade, use o interruptor antes de mexer no logo. Eu mando o logo de novo, e está tudo no lugar. |

### 3.7 Recap (1 linha nova, antes da linha da equipe)
| Tela | Fala |
|---|---|
| Montagem rápida: o interruptor travado com o aviso âmbar (capítulo novo). | Viu a diferença entre desligar no interruptor e só remover o logo. |

### O mundo fictício precisa ter
- Nenhum dado novo: semente `apos-cap04`, o arquivo do logo claro que já existe (`rec/t27_logo_claro.py`) e a Juliana do T2.
- Handlers já previstos no plano, agora usados de verdade: storage `avatars` (`remove`, `upload`, `getPublicUrl`) e update de
  `companies.logo_url` para nulo e de volta; update de `white_label_enabled` nos dois sentidos, devolvendo a linha com a cor
  mantida.
- O canal realtime mudou de nome (`company-updates:...`); o cap da Juliana continua abrindo sessão nova, então não precisa.
- Cap05: pedido mais recente da lista **sem** origem em ticket de pesagem (senão o PDF sai com "Ticket:"/"Caixa:").
- Ilustrações novas: logo no escuro × no claro (cap03); três cartões a mais, QR com logo e os cartões do ponto e da nota (cap05).

## 4. Estimativa

| Onde | Palavras | Segundos (2,6 palavras/s) |
|---|---|---|
| cap01 (3.1) | 27 | 10 |
| cap02 (3.2) | 22 | 8 |
| cap03 (3.3) | 45 | 17 |
| cap04 (3.4) | 32 | 12 |
| cap05 (3.5), já descontada a dica que sai (37 palavras) | 79 − 37 = 42 | 16 |
| Capítulo novo (3.6) | 145 | 56 |
| Recap (3.7) | 11 | 4 |
| **Total** | **≈ 324** | **≈ 125 s de fala** |

Mais 1 vinheta e os gestos do capítulo novo (dois cliques no interruptor, remover e reenviar o logo): o vídeo vai de ~6 min
para ~8 min e meio. **1 capítulo novo**, 6 trechos em capítulos existentes.

## Depende de decisão do Kaik
1. Mostrar na aula que o interruptor trava sem logo (3.6, linhas 5 a 8). É comportamento real, mas expõe um ponto fraco do
   app (cartão dizendo "Ativo" sem logo). Alternativa: capítulo só com desligar e religar (≈ 25 s) e a dica atual mantida.
2. Dica do logo no menu escuro (3.3): entra como dica com ilustração ou vira pedido de melhoria no app.
3. Frases do ponto, da nota fiscal e do QR (3.5): manter aqui ou deixar só no T19, T16 e T1.
