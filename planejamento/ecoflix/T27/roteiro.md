# Roteiro T27 · White Label

Roteiro pronto para gerar a voz e gravar (molde da Domiflix; o Kaik ajusta depois se precisar). Coluna Fala = texto da
narração (voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna
Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da 1.59.154 (`T27/inventario.md`).
Desktop 1280×800, logado como Rafael Nogueira; no cap06, uma sessão da Juliana Prado. Todo capítulo parte de um navegador
novo, com o mundo do fim do capítulo anterior (sementes em `plano.md` → "Gravação").

- **Título:** White Label (🔒 módulo `white_label`; aula nova)
- **Antes:** Sua conta e sua empresa (T1)
- **Próximo:** Portal do Cliente e Fornecedor (T20)
- **Vinhetas (áreas):** WHITE LABEL · MARCA · WHITE LABEL · COR · DOCUMENTOS · EQUIPE · RESUMO
- **Duração estimada:** ~6 min de vídeo (793 palavras de fala, ~5,1 min de voz a 2,6 palavras/s, mais 7 vinhetas, os
  envios e a janela do comprovante; alvo da fonte: 7 min; 4.292 caracteres de TTS com os títulos)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça).
- **Estado inicial:** logo horizontal da Recicla Vale (do T1), sem ícone, White Label desligado, sem cor; módulo
  `white_label` contratado; menu lateral aberto e escuro (o padrão do app).
- **Criado ao vivo:** o ícone quadrado, o White Label ligado e a "Cor Primária" `#1F5FAD`. **Estado final:** a Recicla
  Vale com a marca dela no menu, na cor e nos documentos.
- Marcas na coluna Tela: `[BACKEND: ...]`, `[ZOOM: ...]` (zoom suave, a frase inteira), `[ILUSTRAÇÃO: ...]` (desenho por
  código no estilo da marca, nunca tela inventada do app).
- Decisões (ver `plano.md`): o aviso de "sem logo" entra só na fala (o logo do T1 já existe); o Portal do parceiro entra
  como ilustração (a página real é do T20); nada de zoom no campo "Nome Exibido no Sistema" (🚫).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "White Label". | (sem fala) |
| Dashboard da Recicla Vale Metais, logado como Rafael Nogueira. [ILUSTRAÇÃO: o sistema trocando de marca: um cartão "sistema" com o logo do EcoSistema no canto e uma barra verde; na palavra "logo", entra o logo da Recicla Vale; na palavra "cor", a barra fica azul-aço; no cartão branco da ilustração, Montserrat.] | Oi! Neste tutorial a gente vai deixar o EcoSistema com a cara da Recicla Vale Metais: o logo dela no menu, a cor dela, e os documentos sem o rodapé do EcoSistema. |
| A câmera vai ao topo do menu lateral: o logo do EcoSistema. | Hoje, quem abre o sistema vê o logo do EcoSistema aqui no menu. E o comprovante sai com o rodapé do EcoSistema. |
| A câmera fica no menu. | Com o White Label, a equipe e os parceiros passam a ver a marca da Recicla Vale. |
| Cartão discreto: "Módulo White Label". | O White Label é um módulo, então ele depende do plano contratado. |
| Cartão discreto: "Antes: Sua conta e sua empresa". | Se você ainda não viu o tutorial Sua conta e sua empresa, dá uma olhada antes. [pause] Vamos ver o que ele troca. |

### cap01 · O que muda (vinheta: WHITE LABEL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), no Dashboard; clica em "Configurações" no rodapé do menu (ao lado de "Sair"): abre "Configurações do Sistema" na aba "Empresa", com o cartão "Empresa" ("Informações e configurações da sua empresa") e a seção "Identidade Visual". | O White Label fica nas Configurações, na aba Empresa, aqui na Identidade Visual. |
| Na coluna da direita, a gaveta "White Label" ("Personalize o sistema com sua marca"); clica e ela abre: "White Label Desativado", "O logo da EcoSistema está sendo exibido" e o interruptor desligado. [BACKEND: `company_modules` com `white_label` (`removed_at` nulo)] | Ele não tem tela própria: é esta gaveta aqui. Por enquanto, está desativado. |
| [ILUSTRAÇÃO: o que muda e o que continua: à esquerda, "Muda", entram um a um "Logo no menu", "Ícone do menu recolhido", "Cor Primária" e "Rodapé do EcoSistema nos documentos" (que sai riscado), cada um na palavra dita.] | Ligado, ele troca o logo do menu, o ícone do menu recolhido e a cor principal. E tira o rodapé do EcoSistema dos documentos. |
| (ilustração) À direita, "Continua": "Endereço do sistema", "Aba do navegador", "E-mails", "Tela de login" e "Uma cor só", na palavra "continuam". | O endereço do sistema, a aba do navegador, os e-mails e a tela de login continuam os do EcoSistema. E é uma cor só: no tema escuro, o sistema usa a mesma cor, um pouco mais clara. |

### cap02 · O logo e o ícone (vinheta: MARCA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); Configurações, aba "Empresa"; a câmera vai à coluna da esquerda: "Logo da Empresa" com o logo da Recicla Vale, os botões "Substituir" e "Remover" e "Recomendado: formato horizontal, PNG ou JPG, máximo 5MB". | Tudo começa pelas imagens. O logo horizontal a Recicla Vale já mandou, no tutorial da empresa. É ele que aparece no menu aberto. |
| A câmera passa pelos botões "Substituir" e "Remover" do logo, sem clicar. | Se a marca mudar um dia, é só clicar em Substituir e mandar a nova. |
| [ILUSTRAÇÃO: qual imagem vai onde: o logo horizontal da Recicla Vale entra numa faixa larga, "menu aberto", na palavra "comprido"; o ícone quadrado entra numa faixa estreita, "menu recolhido", na palavra "quadrado".] | São duas imagens. O logo, comprido, vai no menu aberto. O ícone, quadrado, vai no menu recolhido, onde só cabe um quadradinho. |
| Desce até "Ícone da Empresa (1:1)" ("Usado no menu lateral quando recolhido (White Label)") e o quadrado tracejado "1:1". | Falta o ícone. Ele fica logo abaixo, no Ícone da Empresa. |
| Clica no quadrado "1:1" e escolhe `recicla-vale-icone.png`; aviso "Ícone atualizado com sucesso!"; o ícone aparece com "Substituir" e "Remover", e "Recomendado: formato quadrado (1:1), PNG transparente, 128×128px". [BACKEND: storage `avatars` (`upload`, `getPublicUrl`) e update de `companies.icon_url`; vira `apos-cap02`] | Clico no quadrado e escolho o arquivo do ícone. Pronto, subiu. A tela recomenda uma imagem quadrada, com fundo transparente. |
| [ZOOM: "Recomendado: formato horizontal, PNG ou JPG, máximo 5MB", a frase inteira] | Uma dica: as duas imagens podem ter até cinco megas. Arquivo maior, ou que não seja imagem, a tela recusa e avisa na hora. |

### cap03 · Ligar o White Label (vinheta: WHITE LABEL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); o `setup` abre Configurações, aba "Empresa", e a gaveta "White Label" fora do vídeo: "White Label Desativado" e o interruptor. | Com as imagens no lugar, é hora de ligar. |
| [ZOOM: o cartão do interruptor ("White Label Desativado"), a frase inteira] | Uma dica: quem libera esse interruptor é o logo. Sem logo enviado, ele fica travado, e a tela pede o upload antes. |
| Clica no interruptor: aviso "White Label ativado! Seu logo agora será exibido em todo o sistema."; o cartão vira "White Label Ativo" ("Seu logo está sendo exibido no lugar do logo EcoSistema") e a gaveta ganha o selo "Ativo". [BACKEND: update de `companies.white_label_enabled`] | Ligo o interruptor. Pronto: White Label Ativo. |
| A câmera vai ao topo do menu lateral: o logo da Recicla Vale no lugar do logo do EcoSistema. | Olha o menu: o logo da Recicla Vale já entrou no lugar do logo do EcoSistema. |
| Clica no botão de recolher o menu (ícone de painel, no canto esquerdo do cabeçalho) e leva o mouse para o meio da tela, longe do menu: o menu recolhido mostra o ícone da Recicla Vale. [ZOOM: o ícone no topo do menu recolhido, nesta frase e na seguinte] | E o ícone? Ele aparece quando o menu está recolhido. |
| (o mesmo zoom continua) | Uma dica: o ícone só aparece assim, com o menu recolhido e o White Label ligado. Com o menu aberto, quem aparece é o logo. |
| Clica no mesmo botão e o menu abre de novo, com o logo. [vira `apos-cap03`] | Abro o menu de novo, e volta o logo. |

### cap04 · A cor da marca (vinheta: COR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`); o `setup` abre a gaveta "White Label" (com o selo "Ativo") fora do vídeo; a câmera desce até "Personalizações": "Nome Exibido no Sistema", "Cor Primária" e "Salvar Personalizações". | Agora a cor. Com o White Label ligado, aparecem as Personalizações. |
| A câmera passa por "Nome Exibido no Sistema" (vazio, com "Recicla Vale Metais" em cinza), sem zoom e sem digitar. | O Nome Exibido no Sistema fica guardado aqui. Nas telas, quem mostra a marca é o logo e a cor. |
| A câmera passa pelo seletor de cor (o quadrado à esquerda, sem abrir); clica no campo de texto da "Cor Primária" (placeholder "#22c55e") e digita "#1F5FAD"; o quadrado "Preview" aparece em azul. [ZOOM: "Cor Primária" com o código digitado e o "Preview", a frase inteira] | Na Cor Primária, dá pra escolher no seletor ou digitar o código. Eu digito o do azul da Recicla Vale, e o quadradinho do lado já mostra como fica. |
| Clica em "Salvar Personalizações" ("Salvando..."): aviso "Configurações de White Label salvas!"; o botão, o interruptor e a barrinha do item ativo no menu ("Configurações") passam para o azul. [BACKEND: update de `companies.white_label_primary_color` "#1F5FAD" e `white_label_company_name` nulo; vira `apos-cap04`] | Salvar Personalizações. Repara: os botões, os interruptores e a barrinha do menu já ficaram azuis. |
| A câmera mostra o botão "Reset", sem clicar. | Uma dica: com a Cor Primária vazia, o sistema fica no verde padrão. O Reset só limpa o campo. A volta pro verde vale depois do Salvar Personalizações. |

### cap05 · Onde a marca aparece (vinheta: DOCUMENTOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`): o Dashboard, com o logo da Recicla Vale no menu. [ILUSTRAÇÃO: onde a marca aparece: seis cartões entram um a um, cada um na palavra dita: "Menu", "Cabeçalho", "Comprovante térmico", "A4", "PDFs" e "Portal do parceiro"; em cada um, o selo do EcoSistema sai e entra o logo da Recicla Vale.] | E onde a marca aparece? No menu, a gente já viu. No cabeçalho, o logo aparece pra quem usa o menu superior, e no celular. |
| (ilustração) Os cartões "Comprovante térmico", "A4" e "PDFs" acendem; o rodapé do EcoSistema sai de cada um. | Nos documentos, o que muda é o rodapé. O comprovante térmico, o A4 e os relatórios em PDF saem sem o rodapé do EcoSistema. |
| Clica em "Pedidos" no menu; no pedido mais recente da lista, passa o mouse no menu "⋮" da linha e clica em "Ver comprovante" (ícone de olho): abre a janela nova com o comprovante; a câmera passa pelo logo da Recicla Vale no topo e desce até o fim, que termina sem o logo e o endereço do EcoSistema. [BACKEND: pedido do histórico com itens e pagamento; janela nova liberada no robô; formato do comprovante = o do T1] | Olha o comprovante de um pedido. Em cima, o logo da Recicla Vale, que já vinha desde o tutorial da empresa. E embaixo, acabou o rodapé do EcoSistema. |
| [ILUSTRAÇÃO: o Portal do parceiro: um celular genérico, sem marca, com a página do parceiro; na palavra "topo", a faixa de cima fica azul-aço com o logo da Recicla Vale; na palavra "rodapé", o rodapé do EcoSistema sai.] | No Portal do parceiro, com a cor salva, o topo fica com a cor da Recicla Vale, e o rodapé do EcoSistema sai também. |
| [ILUSTRAÇÃO: remover o logo ou desligar: à esquerda, "Remover o logo": o menu volta ao logo do EcoSistema e os documentos seguem sem o rodapé; à direita, "Desligar o interruptor": menu, cor e documentos voltam ao padrão; cada lado na palavra dita.] | Uma dica: pra desligar o White Label, use o interruptor. Se você só remover o logo, o menu volta pro logo do EcoSistema, mas os documentos continuam sem o rodapé. |

### cap06 · A empresa toda, na hora (vinheta: EQUIPE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`): segundo navegador, logado como Juliana Prado (login fora do vídeo), no Dashboard dela, com o logo da Recicla Vale no menu e a barrinha azul. [BACKEND: sessão da Juliana (T2); o realtime não é preciso, a sessão já abre com a marca] | E a equipe? A troca vale pra empresa toda. Esse aqui é o sistema da Juliana, do escritório. |
| [ZOOM: o logo da Recicla Vale no topo do menu da Juliana, a frase inteira] | Mesmo logo, mesma cor, e ela não precisou mexer em nada. |
| [ILUSTRAÇÃO: a troca chegando a todos: três telas pequenas com os nomes Rafael, Juliana e Marcos; na palavra "salva", o logo e a cor mudam nas três ao mesmo tempo.] | Quando o White Label é ligado, ou a cor é salva, quem estiver com o sistema aberto vê a mudança na hora, sem sair e entrar de novo. |
| A câmera fica no menu da Juliana (sem "Configurações" aberto). | E quem muda o White Label é quem pode mexer na aba Empresa. A Juliana só vê o resultado. |

### cap07 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a gaveta "White Label" e o "Ícone da Empresa (1:1)" com o ícone (capítulos 1 e 2). | Pronto! Recapitulando: a gente achou o White Label na aba Empresa, viu o que ele troca e mandou o ícone quadrado pro menu recolhido. |
| Montagem rápida: "White Label Ativo" e o logo no menu (capítulo 3). | Ligou o interruptor, e o logo da Recicla Vale entrou no menu. |
| Montagem rápida: "Cor Primária" com o azul (capítulo 4). | Salvou a cor da marca nas Personalizações. |
| Montagem rápida: o fim do comprovante, sem o rodapé (capítulo 5). | Viu os documentos saindo sem o rodapé do EcoSistema. |
| Montagem rápida: o sistema da Juliana (capítulo 6). | E viu que a troca vale pra equipe toda, na hora. |
| Cartão "Próximo: Portal do Cliente e Fornecedor"; cartela final. | No próximo tutorial, o parceiro acompanha tudo dele sozinho, sem precisar te ligar. Até lá! |
