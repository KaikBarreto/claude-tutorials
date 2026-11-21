# Roteiro T27 · White Label

Roteiro pronto para gerar a voz e gravar (molde da Domiflix; o Kaik ajusta depois se precisar). Coluna Fala = texto da
narração (voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna
Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código do app 1.60.22 (`T27/inventario.md`).
Desktop 1600×900, logado como Rafael Nogueira; no cap07, uma sessão da Juliana Prado. Todo capítulo parte de um navegador
novo, com o mundo do fim do capítulo anterior (sementes em `plano.md` → "Gravação").

- **Título:** White Label (🔒 módulo `white_label`; aula nova)
- **Antes:** Sua conta e sua empresa (T1)
- **Próximo:** Portal do Cliente e Fornecedor (T20)
- **Vinhetas (áreas):** WHITE LABEL · MARCA · WHITE LABEL · COR · DOCUMENTOS · WHITE LABEL · EQUIPE · RESUMO
- **Duração estimada:** ~8 min e meio de vídeo (1.126 palavras de fala, ~7,2 min de voz a 2,6 palavras/s, mais 8 vinhetas, os
  envios e a janela do comprovante; 6.063 caracteres de TTS com os títulos)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça).
- **Estado inicial:** logo horizontal e ícone quadrado da Recicla Vale (os dois enviados no T1, junção), White Label
  desligado, sem cor; módulo
  `white_label` contratado; menu lateral aberto e escuro (o padrão do app).
- **Criado ao vivo:** o White Label ligado e a "Cor Primária" `#1F5FAD`. **Estado final:** a Recicla
  Vale com a marca dela no menu, na cor e nos documentos.
- **1.60.22 (21/11):** capítulo novo 6 "Desligar e voltar atrás" (Equipe vira cap07 e Recap cap08); trechos novos nos caps 1 (sem o
  módulo a gaveta não aparece), 2 (sem ícone o menu recolhido fica com o do EcoSistema), 3 (menu escuro e "Seguir o tema"), 4 (o
  código da cor começa com "#"), 5 (mais documentos, QR com logo, comprovante do Portal, rosto no ponto e nota fiscal) e 8; a dica
  "desligar × remover o logo" saiu do cap05 e virou o cap06.
- Marcas na coluna Tela: `[BACKEND: ...]`, `[ZOOM: ...]` (zoom suave, a frase inteira), `[ILUSTRAÇÃO: ...]` (desenho por
  código no estilo da marca, nunca tela inventada do app).
- Decisões (ver `plano.md`): o Portal do parceiro entra como ilustração (a página real é do T20); nada de zoom no campo "Nome
  Exibido no Sistema" (🚫); "Seguir o tema" só é apontado, nunca clicado (muda a aparência da conta).

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
| A câmera fica na gaveta "White Label" ("Personalize o sistema com sua marca"), sem clicar. A gaveta só existe porque o módulo está contratado (ou no teste). | Se essa gaveta não aparece pra você, é porque o módulo White Label não está no seu plano. No período de teste, ele já vem liberado. |
| [ILUSTRAÇÃO: o que muda e o que continua: à esquerda, "Muda", entram um a um "Logo no menu", "Ícone do menu recolhido", "Cor Primária" e "Rodapé do EcoSistema nos documentos" (que sai riscado), cada um na palavra dita.] | Ligado, ele troca o logo do menu, o ícone do menu recolhido e a cor principal. E tira o rodapé do EcoSistema dos documentos. |
| (ilustração) À direita, "Continua": "Endereço do sistema", "Aba do navegador", "E-mails", "Tela de login" e "Uma cor só", na palavra "continuam". | O endereço do sistema, a aba do navegador, os e-mails e a tela de login continuam os do EcoSistema. E é uma cor só: no tema escuro, o sistema usa a mesma cor, um pouco mais clara. |

### cap02 · O logo e o ícone (vinheta: MARCA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); Configurações, aba "Empresa"; a câmera vai à coluna da esquerda: "Logo da Empresa" com o logo da Recicla Vale, os botões "Substituir" e "Remover" e "Recomendado: formato horizontal, PNG ou JPG, máximo 5MB". | Tudo começa pelas imagens. O logo horizontal a Recicla Vale já mandou, no tutorial da empresa. Com o White Label ligado, é ele que aparece no menu aberto. |
| A câmera passa pelos botões "Substituir" e "Remover" do logo, sem clicar. | Se a marca mudar um dia, é só clicar em Substituir e mandar a nova. |
| [ILUSTRAÇÃO: qual imagem vai onde: o logo horizontal da Recicla Vale entra numa faixa larga, "menu aberto", na palavra "comprido"; o ícone quadrado entra numa faixa estreita, "menu recolhido", na palavra "quadrado".] | São duas imagens. O logo, comprido, vai no menu aberto. O ícone, quadrado, vai no menu recolhido, onde só cabe um quadradinho. |
| Desce até "Ícone da Empresa (1:1)" ("Usado no menu lateral quando recolhido (White Label)"): o ícone da Recicla Vale, enviado no T1, com "Substituir" e "Remover". | O ícone fica logo abaixo, no Ícone da Empresa. Ele também veio no tutorial da empresa. |
| [ZOOM: "Recomendado: formato quadrado (1:1), PNG transparente, 128×128px", embaixo do ícone] (sem clicar em "Substituir") | Pra trocar, é o mesmo Substituir. A tela recomenda uma imagem quadrada, com fundo transparente. |
| A câmera fica em "Ícone da Empresa (1:1)", no ícone e nos botões "Substituir" e "Remover", sem clicar. | E se você não mandar o ícone? O menu recolhido continua com o ícone do EcoSistema, mesmo com o White Label ligado. |
| [ZOOM: "Recomendado: formato horizontal, PNG ou JPG, máximo 5MB", a frase inteira] | Uma dica: as duas imagens podem ter até 5 MB. Arquivo maior, ou que não seja imagem, a tela recusa e avisa na hora. |

### cap03 · Ligar o White Label (vinheta: WHITE LABEL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`: o cap02 não muda nada); o `setup` abre Configurações, aba "Empresa", e a gaveta "White Label" fora do vídeo: "White Label Desativado" e o interruptor. | Com as imagens no lugar, é hora de ligar. |
| [ZOOM: o cartão do interruptor ("White Label Desativado"), a frase inteira] | Uma dica: quem libera esse interruptor é o logo. Sem logo enviado, ele fica travado, e a tela pede o upload antes. |
| Clica no interruptor: aviso "White Label ativado! Seu logo agora será exibido em todo o sistema."; o cartão vira "White Label Ativo" ("Seu logo está sendo exibido no lugar do logo EcoSistema") e a gaveta ganha o selo "Ativo". [BACKEND: update de `companies.white_label_enabled`] | Ligo o interruptor. Pronto: White Label Ativo. |
| A câmera vai ao topo do menu lateral: o logo da Recicla Vale no lugar do logo do EcoSistema. | Olha o menu: o logo da Recicla Vale já entrou no lugar do logo do EcoSistema. |
| Clica no botão de recolher o menu (ícone de painel, no canto esquerdo do cabeçalho) e leva o mouse para o meio da tela, longe do menu: o menu recolhido mostra o ícone da Recicla Vale. [ZOOM: o ícone no topo do menu recolhido, nesta frase e na seguinte] | E o ícone? Ele aparece quando o menu está recolhido. |
| (o mesmo zoom continua) | Uma dica: o ícone só aparece assim, com o menu recolhido e o White Label ligado. Com o menu aberto, quem aparece é o logo. |
| Clica no mesmo botão e o menu abre de novo, com o logo. [vira `apos-cap03`] | Abro o menu de novo, e volta o logo. |
| A câmera fica no logo do topo do menu escuro. [ILUSTRAÇÃO: o mesmo logo em duas faixas, uma escura (some) e uma clara (aparece).] | Mais uma dica: o menu do sistema é escuro. Logo de letra escura, com fundo transparente, quase some aqui. Mande uma versão que apareça bem no fundo escuro. |
| Clica na aba "Aparência" das Configurações; a câmera vai a "Menu (lateral e superior)" e aponta "Seguir o tema" ("Claro no tema claro, escuro no escuro"), sem clicar (muda a aparência da conta). | Ou, na aba Aparência, em Menu, escolha Seguir o tema. Aí o menu fica claro no tema claro. |

### cap04 · A cor da marca (vinheta: COR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`); o `setup` abre a gaveta "White Label" (com o selo "Ativo") fora do vídeo; a câmera desce até "Personalizações": "Nome Exibido no Sistema", "Cor Primária" e "Salvar Personalizações". | Agora a cor. Com o White Label ligado, aparecem as Personalizações. |
| A câmera passa por "Nome Exibido no Sistema" (vazio, com "Recicla Vale Metais" em cinza), sem zoom e sem digitar. | O Nome Exibido no Sistema fica guardado aqui. Nas telas, quem mostra a marca é o logo e a cor. |
| A câmera passa pelo seletor de cor (o quadrado à esquerda, sem abrir); clica no campo de texto da "Cor Primária" (placeholder "#22c55e") e digita "#1F5FAD"; o quadrado "Preview" aparece em azul. [ZOOM: "Cor Primária" com o código digitado e o "Preview", a frase inteira] | Na Cor Primária, dá pra escolher no seletor ou digitar o código. Eu digito o do azul da Recicla Vale, e o quadradinho do lado já mostra como fica. |
| [ZOOM: o campo de texto da "Cor Primária" com "#1F5FAD"] | Uma dica: o código começa com o jogo da velha, como este. Sem ele, o sistema diz que salvou, mas a cor não muda, e não avisa. |
| Clica em "Salvar Personalizações" ("Salvando..."): aviso "Configurações de White Label salvas!"; o botão, o interruptor e a barrinha do item ativo no menu ("Configurações") passam para o azul. [BACKEND: update de `companies.white_label_primary_color` "#1F5FAD" e `white_label_company_name` nulo; vira `apos-cap04`] | Salvar Personalizações. Repara: os botões, os interruptores e a barrinha do menu já ficaram azuis. |
| A câmera mostra o botão "Reset", sem clicar. | Uma dica: com a Cor Primária vazia, o sistema volta às cores padrão. O Reset só limpa o campo. A volta vale depois do Salvar Personalizações. |

### cap05 · Onde a marca aparece (vinheta: DOCUMENTOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`): o Dashboard, com o logo da Recicla Vale no menu. [ILUSTRAÇÃO: onde a marca aparece: seis cartões entram um a um, cada um na palavra dita: "Menu", "Cabeçalho", "Comprovante térmico", "A4", "PDFs" e "Portal do parceiro"; em cada um, o selo do EcoSistema sai e entra o logo da Recicla Vale.] | E onde a marca aparece? No menu, a gente já viu. No cabeçalho, o logo aparece pra quem usa o menu superior, e no celular. |
| (ilustração) Os cartões "Comprovante térmico", "A4" e "PDFs" acendem; o rodapé do EcoSistema sai de cada um. | Nos documentos, o que muda é o rodapé. O comprovante térmico, o A4 e os relatórios em PDF saem sem o rodapé do EcoSistema. |
| (ilustração) Entram mais três cartões: "Tabela de preços", "Ticket de pesagem" e "Fechamento de caixa". Por baixo, o robô clica em "Pedidos" no menu. | Vale também pra tabela de preços, pro ticket de pesagem, pro fechamento de caixa e pros outros relatórios. |
| Em "Pedidos", no pedido mais recente da lista (um que **não** veio de ticket de pesagem), passa o mouse no menu "⋮" da linha e clica em "Ver comprovante" (ícone de olho): abre a janela nova com o comprovante; a cena do PDF real do app mostra o logo da Recicla Vale no topo e desce até o fim, que termina sem o logo e o endereço do EcoSistema. [BACKEND: pedido do histórico com itens e pagamento; janela nova liberada no robô; formato do comprovante = o do T1] | Olha o comprovante de um pedido. Em cima, o logo da Recicla Vale, que já vinha desde o tutorial da empresa. E embaixo, acabou o rodapé do EcoSistema. |
| (PDF do comprovante) [ILUSTRAÇÃO: um QR com o logo da Recicla Vale no meio.] | E, se você usa o QR Code das fotos no comprovante, o logo da Recicla Vale vai no meio do QR Code. |
| [ILUSTRAÇÃO: o Portal do parceiro: um celular genérico, sem marca, com a página do parceiro; na palavra "topo", a faixa de cima fica azul-aço com o logo da Recicla Vale; na palavra "rodapé", o rodapé do EcoSistema sai.] | No Portal do parceiro, com a cor salva, o topo fica com a cor da Recicla Vale, e o rodapé do EcoSistema sai também. |
| (ilustração do Portal) O comprovante baixado pelo parceiro, sem o rodapé do EcoSistema. | E o comprovante que o parceiro baixa no Portal já sai sem o rodapé, mesmo sem cor salva. |
| [ILUSTRAÇÃO: dois cartões, "Cadastro do rosto no ponto" (com o logo e a cor da Recicla Vale) e "Nota fiscal" (com "Logo para Nota Fiscal", à parte).] | No cadastro do rosto pro ponto, o funcionário também vê o logo e a cor da empresa. Já o logo da nota fiscal é outro: ele fica na Configuração Fiscal. |

### cap06 · Desligar e voltar atrás (vinheta: WHITE LABEL) · capítulo novo

Semente `apos-cap04`; o `setup` abre "Configurações" → "Empresa" e a gaveta "White Label" fora do vídeo. Não gera semente nova:
termina igual a `apos-cap04` (logo de volta, ligado, cor salva).

| Tela | Fala |
| --- | --- |
| A gaveta aberta: "White Label Ativo", selo "Ativo", "Personalizações" com "#1F5FAD". | E se um dia você quiser voltar atrás? Tem dois caminhos, e eles não fazem a mesma coisa. |
| Clica no interruptor: aviso "White Label desativado."; o cartão vira "White Label Desativado" ("O logo da EcoSistema está sendo exibido"); somem o selo "Ativo" e as "Personalizações". [BACKEND: update `companies.white_label_enabled` falso] | O primeiro é o interruptor. Desligo, e o sistema avisa: White Label desativado. |
| A câmera vai ao topo do menu (logo do EcoSistema) e à barrinha do item ativo, já sem o azul. | O menu voltou pro logo do EcoSistema, e a cor voltou ao padrão. |
| Clica de novo no interruptor: "White Label ativado! Seu logo agora será exibido em todo o sistema."; desce até as "Personalizações": "#1F5FAD" na "Cor Primária" e a tela fica azul. [BACKEND: update `white_label_enabled` verdadeiro; a cor nunca saiu do banco] | Ligo de novo. A cor da Recicla Vale continuou guardada: voltou tudo, sem digitar nada. |
| Sobe ao "Logo da Empresa": clica em "Remover"; abre "Remover logo da empresa?" ("O logo personalizado será removido e o logo padrão (símbolo de reciclagem) será usado nos comprovantes.", "Cancelar", "Remover"); clica em "Remover": aviso "Logo removido com sucesso!"; a área vira "Nenhum logo enviado". [BACKEND: storage `avatars` `remove`; update `companies.logo_url` nulo] | O segundo caminho é remover o logo. A tela pergunta antes. Confirmo em Remover. |
| A câmera vai ao menu (logo do EcoSistema), ao cartão "White Label Ativo" e ao aviso âmbar "Faça upload do logo ao lado para poder ativar o White Label". | Repara: o menu voltou pro logo do EcoSistema, mas o White Label continua ativo. E a tela pede o logo de volta. |
| [ILUSTRAÇÃO: remover o logo × desligar o interruptor: à esquerda, "Remover o logo": o menu volta ao logo do EcoSistema e os documentos seguem sem o rodapé; à direita, "Desligar o interruptor": menu, cor e documentos voltam ao padrão.] A câmera aponta o interruptor. | Ou seja, só remover o logo não desliga nada: os documentos continuam sem o rodapé do EcoSistema. Pra desligar de verdade, use o interruptor. |
| Clica em "Nenhum logo enviado" e envia `recicla-vale-logo-claro` (a versão do mundo): "Logo atualizado com sucesso!"; o logo volta ao menu. [BACKEND: storage `upload` + `getPublicUrl`; update `logo_url`] | Agora eu mando o logo de novo, e está tudo no lugar. |

### cap07 · A empresa toda, na hora (vinheta: EQUIPE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`): segundo navegador, logado como Juliana Prado (login fora do vídeo), no Dashboard dela, com o logo da Recicla Vale no menu e a barrinha azul. [BACKEND: sessão da Juliana (T2); o realtime não é preciso, a sessão já abre com a marca] | E a equipe? A troca vale pra empresa toda. Esse aqui é o sistema da Juliana, do escritório. |
| [ZOOM: o logo da Recicla Vale no topo do menu da Juliana, a frase inteira] | Mesmo logo, mesma cor, e ela não precisou mexer em nada. |
| [ILUSTRAÇÃO: a troca chegando a todos: três telas pequenas com os nomes Rafael, Juliana e Marcos; na palavra "salva", o logo e a cor mudam nas três ao mesmo tempo.] | Quando o White Label é ligado, ou a cor é salva, quem estiver com o sistema aberto vê a mudança na hora, sem sair e entrar de novo. |
| A câmera fica no menu da Juliana (sem "Configurações" aberto). | E quem muda o White Label é quem pode mexer na aba Empresa. A Juliana só vê o resultado. |

### cap08 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a gaveta "White Label" e o "Ícone da Empresa (1:1)" com o ícone (capítulos 1 e 2). | Pronto! Recapitulando: a gente achou o White Label na aba Empresa, viu o que ele troca e conferiu o logo e o ícone quadrado, que já tinham vindo do tutorial da empresa. |
| Montagem rápida: "White Label Ativo" e o logo no menu (capítulo 3). | Ligou o interruptor, e o logo da Recicla Vale entrou no menu. |
| Montagem rápida: "Cor Primária" com o azul (capítulo 4). | Salvou a cor da marca nas Personalizações. |
| Montagem rápida: o fim do comprovante, sem o rodapé (capítulo 5). | Viu os documentos saindo sem o rodapé do EcoSistema. |
| Montagem rápida: o cartão "White Label Ativo" com o aviso âmbar "Faça upload do logo ao lado..." (capítulo 6). | Viu a diferença entre desligar no interruptor e só remover o logo. |
| Montagem rápida: o sistema da Juliana (capítulo 7). | E viu que a troca vale pra equipe toda, na hora. |
| Cartão "Próximo: Portal do Cliente e Fornecedor"; cartela final. | No próximo tutorial, o parceiro acompanha tudo dele sozinho, sem precisar te ligar. Até lá! |
