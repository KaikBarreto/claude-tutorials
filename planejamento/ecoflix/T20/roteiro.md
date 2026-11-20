# Roteiro T20 · Portal do Cliente e Fornecedor (EcoSistema 1.60.18)

Roteiro pronto para o ensaio gravado e, depois da revisão geral, para a voz (sem etapa de aprovação, como na Domiflix). Coluna
Fala = texto da narração (voz Kaik Barreto), na grafia da legenda, uma linha da tabela = uma linha da fala; a grafia de pronúncia
vai em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da
1.59.154 (`T20/inventario.md`). Dados da Recicla Vale Metais (`plano.md` → "Mundo"); tudo fictício.

- **Título:** Portal do Cliente e Fornecedor
- **Antes:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Próximo:** Gerencial: matriz e filiais (T22)
- **Vinhetas (áreas):** PORTAL · LINK · EXIBIÇÃO · SENHA · SENHA · PORTAL · HISTÓRICO · SALDO · NOTAS E RELATÓRIO · PREÇOS · COLETAS ·
  COMPROVANTE · LINK · FOTOS · RESUMO (todos os capítulos menos o 0)
- **Capítulos (20/11):** 16 (0 a 15). Novos: cap05 (senha por seção), cap06 (cliente e fornecedor), cap10 (preços), cap13 (WhatsApp).
  **Renumerados:** histórico 5→7, saldo 6→8, notas e relatório 7→9, coleta 8→11, comprovante 9→12, fotos 10→14, recapitulando 11→15.
- **Duração estimada:** ~20 min de vídeo (2.701 palavras de fala, ~17 min de voz a 2,6 palavras/s, mais as vinhetas, as ilustrações e o tempo das ações)
- **Tela:** computador 1600x900 (16:9), tema claro; o app é o 1.60.18 (o robô de 12/11 era 1.59.154).
- **FAKE_NOW:** `2026-11-10T15:00:00-03:00` (terça à tarde, depois da venda sem valor da T7 e da nota 1250 da T16). Desktop, tema claro. Dois navegadores: o **do sistema** (Rafael Nogueira, MASTER) e o **do parceiro** (sem login no
  sistema, página pública). Cada capítulo abre navegadores novos com a semente indicada.
- Marcas: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[ZOOM: ...]` (a frase inteira, nunca em cima de outro zoom),
  `[ILUSTRAÇÃO: ...]` (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`; nunca tela do app), `[TESTAR: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Portal do Cliente e Fornecedor". | (sem fala) |
| [ILUSTRAÇÃO: o problema do pátio: à esquerda, o escritório da Recicla Vale Metais com um celular genérico; à direita, o galpão da Cooperativa Recomeço, com fardos; na palavra "print", três balões de conversa com miniaturas de tela vão do escritório para a cooperativa, um atrás do outro (balões genéricos, sem logo de aplicativo)] | Oi! Neste tutorial a gente vai parar de mandar print pro parceiro no WhatsApp. |
| (a ilustração continua: na cooperativa, um balão "Quanto eu tenho pra receber?"; na palavra "escritório", o bonequinho do escritório larga a balança e pega o celular) | Toda semana, a Cooperativa Recomeço pergunta quanto tem pra receber da Recicla Vale Metais. E alguém do escritório para tudo pra tirar print. |
| (a ilustração continua: na palavra "link", os prints somem e fica um balão só, com um link; na cooperativa acendem quatro cartõezinhos: "Pedidos", "Saldo", "Notas", "Relatório") | Com o portal, ela abre um link e vê tudo sozinha: os pedidos, o saldo, as notas e o relatório. |
| Dashboard da Recicla Vale Metais, logado como Rafael Nogueira (semente `inicio`); clique em "Clientes e Fornecedores" no menu lateral; aba "Fornecedores"; clique em "Cooperativa Recomeço": a ficha abre ao lado, em "Visão geral"; a câmera desce até "Acesso ao portal" (o link e "Copiar"), sem clicar. | O link fica na ficha de cada parceiro. Em Clientes e Fornecedores, eu abro a cooperativa, e ele está aqui, em Acesso ao portal. |
| Cartão discreto: "Módulo Portal do Cliente". | O portal faz parte do módulo Portal do Cliente, que depende do plano contratado. |
| Cartão discreto: "Antes: Clientes, fornecedores e a ficha do parceiro". | Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. [pause] Vamos ver o que a cooperativa enxerga. |

### cap01 · O que o parceiro vê (vinheta: PORTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo, navegador do parceiro, sem nada salvo (semente `inicio`): abre `/portal/recicla-vale-metais-cooperativa-<código>`; a página carrega na aba "Histórico". A câmera no cabeçalho verde: o logo, "Recicla Vale Metais", "Portal do Fornecedor" (para cliente, "Portal do Cliente"), "47.318.506/0001-07", o telefone, o e-mail e o endereço. [BACKEND: edge `entity-portal` com o token da cooperativa: sem senha, `portal_config` vazio (tudo visível), `has_coletas` true, sem `price_list`] | É isso que a cooperativa vê quando abre o link. Em cima, o logo, o nome e o contato da Recicla Vale, com o título Portal do Fornecedor. Pra um cliente, o título é Portal do Cliente. |
| A câmera desce ao cartão do parceiro: "Cooperativa Recomeço" e "Fornecedor". | Logo abaixo, o nome dela. O portal é o mesmo pra cliente e pra fornecedor, e cada um vê só o que é dele. |
| O mouse passa pelo cartão do parceiro (se o mundo tiver etiqueta liberada, ela apareceria ao lado do nome; o mundo não tem). | Se você usa etiquetas ou campos personalizados no cadastro, só aparece aqui o que você liberou pro portal, nas Configurações de Clientes e Fornecedores. |
| O mouse desce pelas abas da barra lateral, sem clicar: "Histórico", "Saldo", "Notas Fiscais", "Relatório", "Coletas". | Do lado ficam as abas: Histórico, Saldo, Notas Fiscais, Relatório e Coletas. A gente vê cada uma daqui a pouco. |
| [ILUSTRAÇÃO: o mesmo portal num celular genérico, com as abas numa lista suspensa no alto da página (desenho, sem interface de aplicativo)] | No celular, que é onde quase todo parceiro abre o link, as abas viram uma lista no alto da página. |
| [ILUSTRAÇÃO: até onde vai o acesso: à esquerda, o sistema da Recicla Vale (monitor genérico com "Pedidos", "Saldo", "Notas"); à direita, o celular do parceiro com as cinco abas; setas largas vão do sistema para o celular, com o selo "só pra ver"; nenhuma seta volta] | E até onde vai o acesso dele? O portal é só pra ver. O parceiro não muda nada no seu sistema. |
| (a ilustração continua: na palavra "coleta", uma seta fina volta do celular para o sistema com "pedido de coleta"; na palavra "marca", o sistema ganha a etiqueta "dia · horário · motorista · caminhão") | A única coisa que ele manda é um pedido de coleta. E quem marca o dia, o horário, o motorista e o caminhão é você. |
| De volta ao portal, plano geral da página. | Uma dica: se um parceiro avisar que o link mostrou Portal indisponível, confere o plano da empresa. É ele que libera o portal. E se aparecer Link inválido, o endereço chegou errado ou pela metade. É só copiar de novo na ficha e mandar outra vez. |

### cap02 · Pegar o link do portal (vinheta: LINK)

| Tela | Fala |
| --- | --- |
| Capítulo novo, navegador do sistema (semente `inicio`): `/clientes-fornecedores`, aba "Fornecedores", ficha da "Cooperativa Recomeço" em "Visão geral". [ZOOM: "Acesso ao portal", com o link e o botão "Copiar"] | Agora, o link. Na ficha da cooperativa, em Visão geral, fica o Acesso ao portal. |
| Clique em "Copiar": toast "Link do portal copiado" · "O endereço está pronto para compartilhar.". [TESTAR: permissão de área de transferência no navegador do robô; sem ela sai "Não foi possível copiar o link"] | Clico em Copiar, e pronto, o link está copiado. Aí é só colar na conversa com a cooperativa. |
| O mouse para no "..." do cabeçalho da ficha: o menu abre com "Editar", "Excluir", "Portal do Fornecedor" e "Nova Movimentação"; o mouse para em "Portal do Fornecedor", sem clicar, e sai (o menu fecha). | O mesmo link também sai aqui no menu, em Portal do Fornecedor. |
| [ZOOM: o fim do endereço no campo de "Acesso ao portal": "recicla-vale-metais-cooperativa-" e o código] | Repara no fim do endereço. Esse código é só da cooperativa. Cada parceiro tem o seu, então o link de um nunca abre os dados de outro. |
| [ILUSTRAÇÃO: o link é uma chave: uma chave com "…cooperativa-" e o código na haste abre a porta "Cooperativa Recomeço"; a porta ao lado, "Fundição Bandeira do Vale", continua fechada; na palavra "grupo", cópias da chave vão para vários bonequinhos num balão de conversa em grupo e ganham um X; na palavra "certo", sobra um bonequinho com um visto] | Uma dica: quem tem o link, entra. Então manda só pro contato certo da cooperativa, e evita mandar em grupo. |
| De volta à ficha: clique em "Editar": janela "Editar Fornecedor"; clique na aba "Portal": "Portal do Fornecedor", "Página só de leitura com o histórico, saldo e notas deste fornecedor." e "Link do portal", com os ícones "Copiar link" e "Abrir portal". | O link também fica no Editar, na aba Portal. E é aqui que a gente escolhe o que a cooperativa vê. |
| O mouse para no ícone "Abrir portal" (aba nova), sem clicar. | Este ícone, Abrir portal, abre o portal numa aba nova, pra você conferir do jeito que o parceiro vai ver. |
| (falado sobre a mesma aba; cena opcional fora da trilha: cadastro sem link mostra "Este cadastro ainda não tem link de portal." e "Gerar link" → "Link do portal gerado"; na página cheia do parceiro, "Copiar link do portal") | Em cadastro antigo, pode aparecer o aviso de que ainda não tem link de portal. Aí é só clicar em Gerar link. E na página cheia do parceiro, o botão Copiar link do portal faz a mesma coisa. |

### cap03 · Escolher as abas (vinheta: EXIBIÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo, navegador do sistema (semente `inicio`): "Editar Fornecedor" da cooperativa na aba "Portal" (o `setup` abre fora do vídeo); rola até "O que exibir no portal": "Tudo vem ligado. Desligue o que não quiser mostrar neste portal.". | Em O que exibir no portal, tudo já vem ligado. Você desliga só o que não quiser mostrar. |
| O mouse passa por "Aba Histórico" e pelas chaves de baixo: "Cards de resumo (totais, ticket médio)", "Gráfico de materiais", "Valores financeiros (preços e totais)" e "Fotos dos pedidos", sem mudar nada. | No Histórico, dá pra escolher os cartões de resumo, o gráfico dos materiais, os valores e as fotos dos pedidos. |
| [ZOOM: "Valores financeiros (preços e totais)" e a chave dele] | Com Valores financeiros desligado, o parceiro vê os pesos dos pedidos, mas não os preços. |
| O mouse desce por "Aba Saldo", "Aba Notas Fiscais", "Aba Relatório" (com "Mostrar valores (R$ e preço médio)") e "Mostrar aba Coletas" (com "Permitir solicitar coleta"), sem mudar nada e sem parar em "Mostrar aba Preços". | Depois vêm o Saldo, as Notas Fiscais, o Relatório e as Coletas, cada um com a sua chave. Com o Permitir solicitar coleta desligado, o parceiro acompanha as coletas, mas não pede uma nova. Na cooperativa, fica tudo ligado. |
| Rola até "Formato do comprovante no portal" ("Como o comprovante do pedido é gerado quando o cliente clica no portal."): "Automático (segue o formato da empresa)" marcado; o mouse passa por "Térmico (80mm)"; clique em "A4". | Embaixo fica o formato do comprovante que o parceiro imprime. O Automático segue o formato da sua empresa, e o Térmico serve pra quem imprime em bobina. A cooperativa imprime em folha comum, então eu marco A4. |
| Clique em "Salvar exibição": toast "Exibição do portal salva". [BACKEND: `UPDATE suppliers` com `portal_config` (as chaves ligadas, `precos` false, `locked` todo true) e `portal_receipt_format` "a4"; vira `apos-cap03`] | Clico em Salvar exibição, e pronto. O Salvar de baixo também grava essas escolhas. |
| Corte para o cadastro de clientes: aba "Clientes" › "Editar" da Aços Quiririm Ltda › aba "Portal"; desliga "Valores financeiros (preços e totais)" e "Aba Saldo"; clique em "Salvar exibição" ("Exibição do portal salva"). [BACKEND: `UPDATE customers` com `portal_config` `valores` false e `saldo` false] | Vamos ver na prática, com a Aços Quiririm. Eu desligo os Valores financeiros e a aba Saldo, e salvo. |
| Navegador do parceiro: o portal da Aços Quiririm (`/portal/recicla-vale-metais-...`, sem senha), aba "Histórico": cartões sem valor, pedidos com "R$ 0,00" e o cadeado; a barra de abas sem "Saldo". [ZOOM: o "R$ 0,00" e o cadeado] | No portal dela, sobram os cartões sem os valores, os pedidos aparecem zerados com um cadeado, e a aba Saldo sumiu. |
| [ILUSTRAÇÃO: parceiro que é cliente e fornecedor: o Depósito Irmãos Siqueira com dois cartões, "Cliente" e "Fornecedor", ligados por um elo; dos dois cartões sai um link para o mesmo portal, com compras e vendas na mesma lista] | Uma dica: tem parceiro que é cliente e fornecedor ao mesmo tempo, como o Depósito Irmãos Siqueira. Os dois cadastros mostram o mesmo portal, com as compras e as vendas juntas. |
| (a ilustração continua: na palavra "desligar", a chave "Aba Relatório" desliga no cartão "Fornecedor" e a aba "Relatório" some do portal nos dois links; na palavra "esconde", aparece o selo "vale o que esconde mais") | Então, desligar uma aba num cadastro desliga nos dois links. Vale sempre o que esconde mais. |

### cap04 · Usuário e senha (vinheta: SENHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo, navegador do sistema (semente `apos-cap03`): "Editar Fornecedor" da cooperativa, aba "Portal"; a câmera no cartão "Exigir senha": "Quando ligado, o portal pede usuário e senha antes de mostrar os dados." e a chave "Pedir login no portal", desligada. | Agora, a proteção. Pra deixar o portal mais seguro, ele pode pedir usuário e senha. |
| Liga "Pedir login no portal": aparecem "Usuário" e "Senha"; digita "cooperativa.recomeco" em "Usuário" e `Recomeco#2611` em "Senha" (pontinhos). | Ligo Pedir login no portal. Em Usuário, um nome fácil pra cooperativa lembrar. A senha, eu combino com ela. |
| Clique em "Salvar acesso": toast "Acesso salvo". [BACKEND: edge `portal-set-credentials` grava `portal_password_enabled` true, `portal_username` e o hash; vira `apos-cap04`] | Clico em Salvar acesso. |
| A câmera desce a "O que exibir no portal": "Escolha seção por seção: Oculto, Livre (abre sem senha) ou Com senha. Toda seção nasce Com senha."; cada aba agora com as pílulas "Oculto", "Livre" e "Com senha", todas em "Com senha". [ZOOM: a frase e as pílulas da "Aba Histórico"] | Repara que as abas mudaram. Agora cada uma tem três jeitos: Oculto, Livre ou Com senha. E todas começam Com senha. |
| [ILUSTRAÇÃO: as três escolhas de cada aba, uma por vez: "Oculto", a aba some do portal (na palavra "some"); "Livre", uma porta aberta (na palavra "abre"); "Com senha", uma porta com cadeado (na palavra "login")] | Oculto, a aba some do portal. Livre, ela abre pra quem tem o link. Com senha, só depois do login. Na cooperativa, fica tudo com senha. |
| Navegador do parceiro, sem nada salvo: abre o link da cooperativa: "Acesso restrito" · "Entre com o usuário e senha para ver seus dados.", "Usuário", "Senha" e "Entrar". [BACKEND: `entity-portal` sem sessão devolve `{requiresLogin: true}`] | Agora, quando a cooperativa abre o link, aparece o Acesso restrito. |
| Digita "cooperativa.recomeco" e a senha; clique em "Entrar": o portal abre na aba "Histórico", com o ícone "Sair" no cartão do parceiro. [BACKEND: edge `portal-login` aceita o usuário e a senha e devolve a sessão (30 dias, no `localStorage`); `entity-portal` com `?session=` devolve tudo] | Ela digita o usuário e a senha, clica em Entrar, e o portal abre. Nesse navegador, ela fica conectada, sem digitar a senha toda vez. |
| [ZOOM: o ícone "Sair" no cartão do parceiro], sem clicar. | Pra sair, é esse ícone. E no parceiro que é cliente e fornecedor, o mesmo usuário e a mesma senha valem pros dois links. |
| Corte para o navegador do sistema: "Editar Fornecedor" da cooperativa › aba "Portal": a chave "Pedir login no portal" ligada e o campo "Senha" com o aviso "deixe em branco p/ manter"; o mouse passa pela chave (sem desligar) e pelo botão "Remover login" (sem clicar). | Se a cooperativa esquecer a senha, não tem recuperação pelo portal: você digita uma nova aqui e salva. Deixando em branco, a senha continua a mesma. E pra tirar o login, é desligar a chave e clicar em Remover login. |

### cap05 · Senha só no que é sensível (vinheta: SENHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo, navegador do sistema (semente `apos-cap04`): Clientes e Fornecedores › aba "Fornecedores" › "Depósito Irmãos Siqueira" › "Editar" › aba "Portal". Liga "Pedir login no portal": aparece o aviso "Este parceiro é cliente e fornecedor: o acesso vale pros dois links."; "Usuário" `deposito.siqueira`, "Senha" (pontinhos); clique em "Salvar acesso" ("Acesso salvo"). [ZOOM: o aviso do parceiro duplo] [BACKEND: `portal-set-credentials` na linha canônica (o cadastro de cliente do par)] | Nem tudo precisa de senha. No Depósito Irmãos Siqueira, eu ligo o login, escolho o usuário e a senha, e salvo o acesso. Repara no aviso: como ele é cliente e fornecedor, o acesso vale pros dois links. |
| Em "O que exibir no portal": a pílula "Livre" na "Aba Histórico"; Saldo, Notas Fiscais, Relatório e Coletas ficam em "Com senha"; clique em "Salvar exibição" ("Exibição do portal salva"). [BACKEND: `UPDATE suppliers` e `customers` do par com `portal_config` e `locked.historico` false; vira `apos-cap05`] | Agora, no Histórico, eu marco Livre. Saldo, Notas Fiscais, Relatório e Coletas continuam Com senha. Salvar exibição. |
| Navegador do parceiro, sem nada salvo: o link do Depósito abre direto no "Histórico"; nas abas "Saldo", "Notas Fiscais", "Relatório" e "Coletas", um cadeado pequeno no ícone. [ZOOM: as abas com cadeado] [BACKEND: `entity-portal` sem sessão: `requires_login` true, `free_sections` ["historico"], só o bloco do Histórico, o resto vazio] | Quando o Depósito abre o link, o Histórico aparece direto, sem pedir nada. E as outras abas ganham um cadeado. |
| Clique em "Saldo": cartão "Acesso com senha" · "Para ver Saldo, entre com o usuário e senha. O resto do portal continua aberto.", "Usuário", "Senha", "Entrar" (não entra). | Clicando em Saldo, o portal pede o usuário e a senha só pra essa parte. O resto continua aberto. |
| Volta ao "Histórico". | Uma dica: o que está com senha nem chega no navegador de quem abriu o link sem entrar. E o comprovante, o relatório e o pedido de coleta seguem a mesma trava. |

### cap06 · Cliente e fornecedor no mesmo portal (vinheta: PORTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), navegador do parceiro (link do cadastro de fornecedor do Depósito, sem sessão): cartão do parceiro com o selo "Cliente + Fornecedor". [ZOOM: o selo] | Repara no selo do Depósito: Cliente mais Fornecedor. Cada cadastro tem o seu link, mas os dois abrem o mesmo portal. |
| Os quatro cartões "Total Comprado", "Total Vendido", "Total de Pedidos" e "Ticket Médio"; o gráfico "Top 5 Materiais". [BACKEND: `entity-portal` dual: `is_dual` true, `sides` com compras e vendas, o feed dos dois lados] | Em cima, o que a Recicla Vale comprou dele e o que vendeu pra ele, cada um no seu cartão, e o gráfico dos materiais. |
| Em "Histórico de Pedidos": "Todos", "Compras", "Vendas" com a contagem; clique em "Vendas": só linhas "Venda", três cartões com "Total Vendido", gráfico "Top 5 Materiais Mais Vendidos"; volta a "Todos". | Na lista, ele filtra: Todos, Compras ou Vendas. Clicando em Vendas, os cartões e o gráfico acompanham. |
| O mouse na aba "Saldo" (com cadeado), sem clicar. | E o saldo é um só, já com as compras e as vendas na mesma conta. |

### cap07 · Histórico de pedidos (vinheta: HISTÓRICO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), navegador do parceiro com a sessão da cooperativa (o `setup` entra fora do vídeo); aba "Histórico": cartões "Total Comprado" "R$ 71.651,58", "Total de Pedidos" "15" e "Ticket Médio" "R$ 4.776,77" (junção: as 14 compras do T4 e a latinha do ticket da T8, de hoje). [ZOOM: os três cartões, desta linha até o fim da seguinte] | Com o portal aberto, a primeira aba é o Histórico. Nos cartões, a cooperativa vê quanto a Recicla Vale já comprou dela. |
| (o zoom continua) | São setenta e um mil seiscentos e cinquenta e um reais e cinquenta e oito, em quinze entregas. |
| A câmera desce ao gráfico "Top 5 Materiais Mais Comprados": "Papelão: 55%", "Plástico PET: 17%", "Alumínio latinha: 15%", "Chaparia: 7%" e "Ferro misto: 6%". | No gráfico, os materiais que ela mais entrega, pelo peso. O papelão passa da metade, e depois vêm o PET e a latinha. |
| Rola até "Histórico de Pedidos" ("Nº Pedido", "Tipo", "Valor", "Pagamento", "Data", "Ações"); clique na compra de 06/11 ("Compra", "R$ 3.700,00", "Saldo"): abre a tabela "Material", "Peso", "Valor Unit." e "Total" com os cinco materiais, "Total do Pedido:" "R$ 3.700,00" e "Fotos do pedido" com três miniaturas. | Embaixo, cada pedido. Clicando na entrega de sexta, abrem os materiais, com o peso e o valor de cada um. Quando o pedido tem tara ou desconto, aparecem embaixo do material o peso bruto e a tara, igual ao comprovante. |
| Clique na primeira miniatura: a foto da carga abre em tela cheia; fecha no X. [BACKEND: três fotos fictícias em `order_attachments` da compra de 06/11, com URL assinada] | E as fotos da carga, que a Recicla Vale anexou no pedido. Só imagem vai pro portal: se o pedido tiver um PDF anexado, ele fica só no sistema. |
| Outra aba do navegador do parceiro: o portal da Fundição Bandeira do Vale (`/portal/recicla-vale-metais-fundicao-<código>`, sem senha), aba "Histórico": "Cliente", cartões "Total Vendido", "Total de Pedidos" e "Ticket Médio", gráfico "Top 5 Materiais Mais Vendidos". | Agora, o portal de um cliente, a Fundição Bandeira do Vale. Aqui, os pedidos são as vendas. |
| Na lista, a venda de hoje ("Venda", "PIX/Transferência"). [ZOOM: "R$ 0,00" e o cadeado ao lado] | Uma dica: a venda de hoje saiu com o Comprovante sem valores. Então, no portal, ela aparece com zero e um cadeado. |
| Clique na venda: "Metal amarelo (latão)" "152 kg" e "Cobre mel" "60 kg", com "R$ 0,00" nos valores e "Total do Pedido:" "R$ 0,00". | O pedido está certo no sistema. Pro parceiro, só os valores ficam escondidos: ele vê o latão e o cobre, com o peso. E o valor do pedido sem valor não sai em lugar nenhum do portal, nem no saldo, nem na nota fiscal, nem no comprovante. |

### cap08 · O saldo do parceiro (vinheta: SALDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), portal da cooperativa com sessão; clique em "Saldo": "Saldo Atual" "R$ 1.350,00" em verde, o selo "Você tem a receber" e a frase "Recicla Vale Metais deve R$ 1.350,00 para Cooperativa Recomeço". [ZOOM: o valor, o selo e a frase] | Agora, o saldo. A cooperativa vê aqui que tem mil trezentos e cinquenta reais pra receber da Recicla Vale. |
| [ILUSTRAÇÃO: o mesmo saldo, dos dois lados: no meio, uma conta-corrente com "R$ 1.350,00"; à esquerda, o sistema da Recicla Vale com o valor em vermelho e "a pagar"; à direita, o celular da cooperativa com o valor em verde e "a receber"; na palavra "mesmo", os dois lados acendem juntos] | No sistema, esse valor aparece em vermelho, porque a Recicla Vale deve. No portal, em verde, porque é a cooperativa que recebe. É o mesmo saldo, visto de cada lado. |
| De volta ao portal; rola até "Histórico de Movimentações", com o selo "Últimos 90 dias": linhas "Pedido" (forma "Saldo") e "Pagamento" ("PIX/Transferência"), com "Saída", "Entrada" e "Saldo". | Embaixo, o extrato dos últimos noventa dias: cada entrega e cada pagamento, com o saldo depois de cada um. |
| O extrato continua na tela: o mouse no selo "Últimos 90 dias" e no rodapé da lista (o tipo "Ajuste" e o "Ver todas as N movimentações" só aparecem com o caso; o mundo não tem, então só a fala). | No extrato, além de Pedido e Pagamento, aparece Ajuste, quando você lança um crédito ou um débito na conta do parceiro, com o motivo que você escreveu. E passando de vinte linhas, tem o Ver todas as movimentações. |
| Navegador do sistema (Rafael): ficha da cooperativa › "Conta-corrente" › "Movimentação": "Nova Movimentação de Saldo", "Pagar" já marcado; em "Valor *" digita "1350" ("R$ 1.350,00"); "Pix/Transferência", com a conta principal; em "Observação" digita "Acerto da entrega de 06/11". [ZOOM: "Valor *" com o valor] | Agora a Recicla Vale acerta o resto. No sistema, em Movimentação, eu pago os mil trezentos e cinquenta reais no Pix. |
| Clique em "Confirmar": toast "Movimentação registrada com sucesso!"; "Saldo Atual" "R$ 0,00". [BACKEND: RPCs `create_manual_bank_transaction` e `update_balance`, `INSERT balance_movements` ("Valor Pago a Cooperativa Recomeço · Acerto da entrega de 06/11"); vira `apos-cap08`] | Confirmar, e o saldo da cooperativa zerou no sistema. |
| Volta ao navegador do parceiro: o portal busca de novo ao ganhar o foco (se não buscar, clique em "Atualizar dados"): "Saldo Atual" "R$ 0,00", "Em dia" e "Não há valores em aberto entre Cooperativa Recomeço e Recicla Vale Metais"; o pagamento no topo do extrato. [ZOOM: o saldo, o selo e a frase] [TESTAR: a busca nova ao voltar o foco] | E no portal, sem mandar link nenhum, o saldo já está em dia. |
| [ZOOM: o ícone "Atualizar dados" no cartão do parceiro], sem clicar. | Uma dica: o saldo do portal é o mesmo da tela de Saldo do sistema, da mesma conta-corrente da ficha. Com o portal aberto, ele se atualiza sozinho em até trinta segundos, e esse botão atualiza na hora. |
| Navegador do parceiro: o portal do Valdir Pereira (sem senha), aba "Saldo": "-R$ 300,00" em vermelho, o selo "Você tem a pagar" e a frase "Valdir Pereira deve R$ 300,00 para Recicla Vale Metais". [ZOOM: o valor, o selo e a frase] | E quando é o parceiro que deve? O Valdir Pereira ficou com um vale de trezentos reais. No portal dele, o saldo aparece em vermelho, com Você tem a pagar, e a frase diz quem deve pra quem. |

### cap09 · Notas e relatório (vinheta: NOTAS E RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), portal da Fundição Bandeira do Vale; clique em "Notas Fiscais": "Todas as NF-e relacionadas a você (entrada e saída) em ordem do mais recente."; a linha "Saída", "1250", "1", "10/11/2026", "R$ 23.950,00", "Autorizada" e a linha "Entrada", "1253" (a devolução), com o selo azul. [ZOOM: o número "1250" e o valor] [BACKEND: `invoices` da Fundição: NF-e 1250, série 1, `emitida`, `invoice_type` saída] | Na aba Notas Fiscais, o parceiro vê as notas emitidas pra ele. Na Fundição, aparece a nota mil duzentos e cinquenta, do cobre mel que saiu hoje, autorizada. |
| O mouse na linha "Entrada" · "1253". [BACKEND: `invoices` da Fundição: 1250 saída, 1253 entrada (devolução), 1254 complementar; todas `emitida`] | E tem a nota mil duzentos e cinquenta e três, com o selo Entrada: é a devolução que a Fundição fez, e a nota de entrada quem emite é a Recicla Vale. |
| A câmera abre para a tabela inteira ("Tipo", "Nº", "Série", "Data", "Valor", "Status"). | Ele confere o número, a série, a data, o valor e a situação. O arquivo da nota, o XML ou o DANFE, você manda pelo caminho de sempre, nas Notas Fiscais do sistema. |
| Navegador do parceiro: o portal da Serra Fina Alumínio Reciclagem (sem senha) › "Notas Fiscais": a linha "Saída" "1249" com o selo "Cancelada". [ZOOM: o selo] [BACKEND: `invoices` 1249 `cancelada` do cliente Serra Fina] | Nota cancelada continua na lista, marcada como Cancelada. Aqui, a da Serra Fina. Só chegam ao portal as notas autorizadas e as canceladas: nota rejeitada ou ainda em digitação não aparece. |
| Navegador da cooperativa (com sessão): clique em "Relatório": "Período" em "Últimos 30 dias", "Material", "Baixar PDF" e "Relatório por Material". | Já o Relatório soma os pedidos do parceiro, material por material. |
| Clique em "Período" e escolhe "Mês passado": a tabela mostra "Alumínio latinha", "Chaparia", "Ferro misto", "Papelão" e "Plástico PET", com "Qtd. Comprada", "Valor Compra" e "Preço Médio Compra". [BACKEND: edge `entity-portal-report` com as compras de outubro da cooperativa] | Na cooperativa, eu escolho o mês passado. Em outubro, foram oito mil e quatrocentos quilos de papelão e dois mil e seiscentos de PET, entre outros. |
| [ZOOM: a linha "Total", com o valor "R$ 18.755,00"] | No total, dezoito mil setecentos e cinquenta e cinco reais. |
| Em "Material": abre a lista e marca "Papelão" (a tabela fica com uma linha); limpa; em "Período": abre a lista e o mouse passa por "Personalizado" (sem escolher). | Dá pra filtrar por material, e o período tem outras opções, como o Personalizado, pra escolher as datas do seu jeito. |
| O mouse na linha "Total" e na tabela. | Pedido estornado fica fora do relatório. E o pedido sem valor entra só com o peso, sem o dinheiro. |
| Clique em "Baixar PDF": o relatório abre numa aba nova; o robô devolve o PDF/HTML da janela (molde `POPS` + `PDF_JS` do T8) para a cena do comprovante na tela. [ZOOM: o botão antes do clique] | No Baixar PDF, o relatório abre pronto pra salvar. E se você não quiser mostrar os valores aqui, é só desligar Mostrar valores, na aba Portal. |

### cap10 · A tabela de preços do fornecedor (vinheta: PREÇOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), navegador do sistema: Clientes e Fornecedores › aba "Fornecedores" › "Cooperativa Recomeço" › "Editar" › aba "Portal"; em "O que exibir no portal", a linha "Aba Preços" · "Quanto a empresa paga por cada material, já com o preço deste fornecedor. Nasce oculta.", na pílula "Oculto". [ZOOM: a linha] | Seu fornecedor vive perguntando quanto está o material? Dá pra mostrar a tabela de preços no portal dele. É a única aba que nasce oculta, pra ninguém ver preço sem você decidir. |
| Clique em "Com senha" na "Aba Preços"; clique em "Salvar exibição" ("Exibição do portal salva"). [BACKEND: `UPDATE suppliers` com `portal_config.precos` true e `locked.precos` true; vira `apos-cap10`] | Na cooperativa, eu mudo de Oculto pra Com senha, e salvo. |
| Navegador da cooperativa (com sessão): a aba nova "Preços" na barra; clique nela: "Preços atualizados em 10/11/2026", bloco "Seus materiais" (Papelão, Plástico PET, Alumínio latinha, Chaparia, Ferro misto) e "Outros materiais que compramos". [BACKEND: `entity-portal` com `price_list` e `price_list_generated_at`; preços de B: latinha 6,20 · PET 1,90 · papelão 0,55 · chaparia 0,70 · ferro misto 0,75] | No portal, apareceu a aba Preços. Primeiro, os materiais que a cooperativa já entrega. Depois, os outros que a Recicla Vale compra. |
| [ZOOM: "Valores sujeitos a alteração. Vale o preço do momento da pesagem."] | E o aviso protege você: os valores podem mudar, e vale o preço do momento da pesagem. |
| Clique em "Baixar em PDF" ("Gerando tabela de preços"): a tabela abre numa aba nova; o robô devolve o PDF da janela (molde `POPS` + `PDF_JS`). | No Baixar em PDF, ela leva a tabela pronta. |
| De volta à lista de preços. | Uma dica: cada fornecedor vê o preço dele. Se a cooperativa tem preço combinado ou uma tabela própria, é esse que aparece, sem nenhuma marca de preço especial. E essa aba só existe no cadastro de fornecedor. |

### cap11 · O parceiro pede a coleta (vinheta: COLETAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`), portal da cooperativa com sessão; clique em "Coletas": "Acompanhe suas coletas e solicite uma nova.", "Solicitar coleta" e "Minhas coletas", com as coletas da cooperativa (junção, T12): "#10" "Agendada" (PET prensado, 13/11 · Tarde, pedida pelo portal hoje cedo), "#5" e "#1" "Concluída". Cartão discreto: "Módulo Coletas". | A aba Coletas é do módulo de coletas, que também depende do plano contratado. Com ela, a cooperativa pede a coleta sozinha e acompanha as que já tem. |
| Clique em "Solicitar coleta": janela "Solicitar coleta" ("Peça a coleta do seu material. A empresa confirma o dia e o horário."), "Tipo" "Coletar material". | Essa semana, o galpão dela encheu antes de sexta. Então ela clica em Solicitar coleta. |
| Em "Material *" digita "Papelão e PET prensados"; em "Quantidade estimada" digita "2.500 kg". [ZOOM: "Quantidade estimada" com o valor] | Ela escreve o material, papelão e PET prensados, e a quantidade, uns dois mil e quinhentos quilos. |
| Em "Data preferida" escolhe 12/11/2026; em "Período" escolhe "Manhã"; a câmera passa por "Endereço da coleta", já preenchido com o endereço do cadastro; em "Observações" digita "Os fardos ficam na doca do galpão.". | Escolhe o dia que prefere, quinta de manhã. O endereço já vem do cadastro, e se a coleta for em outro lugar, ela troca ali mesmo. E nas observações, onde estão os fardos. |
| Clique em "Solicitar coleta": toast "Solicitação enviada (#<n>)"; em "Minhas coletas", o cartão "#<n>" com o selo "Solicitada", o material junto da quantidade (o app junta os dois com um traço), "12/11/2026 · Manhã", "Solicitada em 10/11/2026" e a observação. [BACKEND: edge `collection-request`: `collection_orders` com `origem` "portal", `status` "solicitada", sem motorista e veículo; `user_notifications` para os usuários da empresa; vira `apos-cap11`] | Solicitar coleta, e pronto. O pedido entra como Solicitada. |
| Navegador do sistema (Rafael; o `setup` recarrega a tela, o backend falso não tem realtime): o sino de notificações com o aviso; clique no sino: "Nova solicitação de coleta" · "Cooperativa Recomeço solicitou uma coleta (#<n>)."; fecha. | E no sistema, o aviso chega no sino: nova solicitação de coleta. |
| [ILUSTRAÇÃO: quem pede e quem decide: à esquerda, o celular da cooperativa com "papelão e PET · quinta, manhã"; uma seta leva ao sistema da Recicla Vale; ali, na palavra "confirma", acendem "dia", "horário", "motorista" e "caminhão", e o selo passa de "Solicitada" para "Agendada"] | A cooperativa sugeriu o dia, mas quem confirma o dia, o horário, o motorista e o caminhão é a Recicla Vale, na tela de Coletas. Isso fica pro tutorial de Coletas e Logística. |
| Navegador do parceiro: em "Minhas coletas", clique no cartão "#5" "Concluída" › "Ver relatório da coleta": abre o relatório (`/portal/<link>/coleta/<id>`); clique em "Voltar ao portal". (Cancelada com "Motivo: ...": só a fala, o mundo não tem.) | Quando a coleta é concluída, o cartão vira um atalho. Em Ver relatório da coleta, ela vê o que foi recolhido e entregue, e volta pelo Voltar ao portal. E se você recusar ou cancelar um pedido, ela vê o motivo no cartão. |
| (sem tela de erro) plano geral de "Minhas coletas" | Uma dica: se ela escolher um dia que a Recicla Vale não atende, ou pedir em cima da hora, o portal explica o motivo e pede outra data. E se você tirar a exigência de aprovação, o pedido já entra como Agendada. Essas regras ficam nas Configurações de Coletas. |

### cap12 · O comprovante do portal (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap11`), portal da cooperativa com sessão, aba "Histórico", lista de pedidos; o mouse para na impressora "Gerar comprovante" da compra de 06/11. | E se a cooperativa precisar do comprovante de uma entrega? Ela mesma imprime, aqui na impressora do pedido. |
| Clique na impressora: abre a janela "Gerando comprovante" e, em seguida, o PDF A4: logo e dados da Recicla Vale Metais, a compra, "Cooperativa Recomeço", a tabela com os cinco materiais ("Quant.", "Preço Unitário", "Total") e o total. [BACKEND: edge `portal-order-receipt` (sessão válida) com o pedido, os itens, `company.receipt_format` e `photoQr` com o caminho `/fotos/...` e "Escaneie para ver fotos"] [TESTAR: a janela nova do PDF; com a janela bloqueada, o comprovante abre por cima do portal] | Abre o comprovante em A4, como a gente escolheu na aba Portal, com os materiais, os pesos e os valores da entrega. |
| [ZOOM: o QR Code e a legenda "Escaneie para ver fotos"] | E como esse pedido tem fotos, o comprovante sai com um QR Code: Escaneie para ver fotos. |
| Fecha a janela do PDF; de volta ao portal. | Num pedido com o Comprovante sem valores, o papel sai sem os preços, igual ao portal. O valor nem passa pelo navegador do parceiro. |
| [ZOOM: rodapé do A4, só se o mundo tiver assinatura ligada; o mundo não tem, então só a fala] | Se a sua empresa imprime linha de assinatura no comprovante, ela sai aqui também, do jeito que você escolheu nas Configurações, em Usabilidade. No celular, se o navegador bloquear a janela, o comprovante abre por cima do portal. |

### cap13 · Mandar o pedido pelo WhatsApp (vinheta: LINK)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap11`), navegador do sistema: tela de Pedidos (`/pedidos`); na compra de 06/11 da Cooperativa Recomeço, o menu "⋮": "Ver comprovante", "Ver fotos anexadas", "Enviar pelo WhatsApp". | Em vez de esperar o parceiro abrir o portal, você pode mandar o pedido pra ele. Nos Pedidos, no menu da compra, tem o Enviar pelo WhatsApp. |
| Clique em "Enviar pelo WhatsApp" (o robô intercepta `window.open` para `wa.me`: a janela externa não é filmada). [ILUSTRAÇÃO: um balão de mensagem genérico com o texto exato lido do endereço interceptado: "Olá, Cooperativa Recomeço!" · "Aqui é da Recicla Vale Metais." · "Segue o comprovante do Pedido <nº>, de 06/11/2026." · "Valor total, R$ 3.700,00." · "Acesse pelo link abaixo:" e o link] | O WhatsApp abre com a mensagem pronta, no telefone do cadastro: o número do pedido, a data, o valor e o link. |
| Navegador do parceiro (sessão da cooperativa): o link com `?pedido=` abre o "Histórico" já no pedido de 06/11, aberto e contornado por uns segundos. [ZOOM: a linha contornada] | E esse link já abre o portal em cima daquele pedido, com os materiais e as fotos. |
| De volta ao menu "⋮" da tela de Pedidos. | Uma dica: precisa do telefone no cadastro do parceiro. Num pedido com Comprovante sem valores, a mensagem avisa que o cupom é sem valor, e não mostra o total. O mesmo botão aparece no histórico da ficha do parceiro. |

### cap14 · As fotos do pedido (vinheta: FOTOS)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: as fotos entram no pedido: o caminho "Opções avançadas" › "Fotos do pedido" › "Anexar" (desenho, não a tela real), três fotos pequenas de fardos entrando e, na palavra "X", uma delas saindo ("Remover foto"); o aviso "Disponível com internet."; depois o menu "⋮" › "Ver fotos anexadas"] | Agora, as fotos. Elas entram na compra ou na venda, em Opções avançadas, no Anexar. Dá pra escolher várias de uma vez, e tirar uma foto errada no X antes de salvar. Precisa estar com internet, e vale também no Ticket de Pesagem. Depois, nos Pedidos, o Ver fotos anexadas mostra as fotos daquela linha. |
| [ILUSTRAÇÃO: o comprovante A4 com o QR; na palavra "celular", um celular genérico aponta a câmera para o QR; na palavra "página", a tela do celular mostra um retângulo com "Fotos do pedido" e três fotos pequenas (desenho, sem interface de aplicativo)] | E quem aponta o celular pro QR Code do comprovante cai numa página só com as fotos daquele pedido. |
| Capítulo novo, navegador sem nada salvo (semente `apos-cap11`): abre o link do QR (`/fotos/recicla-vale-metais-compra-<nº>-<código>`): cabeçalho verde com o logo, "Recicla Vale Metais" e "Fotos do pedido #<nº>"; "Fotos" com o carrossel. [BACKEND: edge `order-photos-public` com o token de `order_photo_shares` da compra de 06/11 (fixo na semente)] | É essa página. Em cima, a Recicla Vale e o número do pedido. Embaixo, as fotos da carga. |
| Clique em "Próxima foto" duas vezes; clique na foto: abre em tela cheia; fecha. | Dá pra passar de uma foto pra outra e abrir cada uma em tela cheia. |
| Rola até "Dados do Pedido": "Fornecedor" "Cooperativa Recomeço", "Data", "Itens" com os cinco materiais, "Total" "R$ 3.700,00" e "Forma de pagamento" "Saldo". [ZOOM: "Total" e "R$ 3.700,00"] | Em Dados do Pedido ficam o fornecedor, a data, os materiais e o total: três mil e setecentos reais. Se o pedido tiver motorista, placa ou observação, aparecem aqui também. |
| [ILUSTRAÇÃO: os dois links públicos: à esquerda, o link de fotos como um envelope com um pedido só; à direita, o link do portal como uma pasta grossa com pedidos, saldo, notas, relatório e coletas; na palavra "cuida", a pasta ganha um cadeado e um destaque] | Uma dica: são dois links diferentes. O de fotos mostra só aquele pedido. O do portal mostra o histórico inteiro do parceiro, então cuida mais dele. |
| (a ilustração continua: um cupom térmico genérico do caixa com um QR e a legenda "Ver no portal"; uma seta leva à pasta do portal, aberta num pedido só) | E no comprovante que sai no caixa, o QR Code leva o parceiro pro portal dele, já aberto naquele pedido. |

### cap15 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem: o portal da cooperativa, o "Copiar" e o toast, "O que exibir no portal" com "A4". | Pronto! Recapitulando: a gente viu o que o parceiro enxerga no portal e copiou o link da cooperativa na ficha. |
| (a montagem continua: "Salvar exibição", "Pedir login no portal", "Acesso restrito") | Escolheu as abas e o comprovante em A4, e protegeu o portal com usuário e senha. |
| (a montagem continua: o Depósito com o Histórico livre e o cadeado nas outras abas, o selo "Cliente + Fornecedor", os cartões do Histórico, o saldo "Em dia", as notas e o relatório de outubro) | Deixou o histórico do Depósito livre e o resto com senha, viu o portal de quem é cliente e fornecedor, conferiu o histórico, o saldo, que ficou em dia sozinho depois do pagamento, as notas e o relatório de outubro. |
| (a montagem continua: a aba "Preços", "Solicitação enviada", o comprovante A4) | Liberou a tabela de preços pra cooperativa, que pediu uma coleta e imprimiu o comprovante. |
| (a montagem continua: o balão do WhatsApp, a página "Fotos do pedido") | Mandou um pedido pelo WhatsApp, e as fotos do pedido abriram pelo link público. |
| Cartão discreto: "Próximo: Gerencial: matriz e filiais". | No próximo tutorial, a matriz enxerga todas as unidades de uma vez. Até lá! |
