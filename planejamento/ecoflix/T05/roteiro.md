# Roteiro T5 · Balança e impressora: o EcoTray

Pronto para o ensaio e a voz (sem etapa de aprovação). Coluna Fala = narração (voz Kaik Barreto), na grafia da legenda;
a grafia de pronúncia vai em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera fica, com os rótulos
como no código (`T05/inventario.md`, 1.59.154 e EcoTray 1.7.22).

- **Título:** Balança e impressora: o EcoTray
- **Antes:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Próximo:** Caixa: abrir, fechar e o cofre (T6)
- **Vinhetas (áreas):** ECOTRAY · INSTALAÇÃO · CONEXÃO · IMPRESSORA · IMPRESSORA · BALANÇA · BALANÇA · BALANÇA ·
  CONEXÃO · IMPRESSORA · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~12 min (1.625 palavras de fala, ~10,4 min a 2,6 palavras/s, mais 11 vinhetas, as cenas de
  Windows e as ilustrações); alvo da fonte, 13 min.
- **Gravação:** computador 1280×800, logado como Rafael Nogueira; `FAKE_NOW=2026-11-10T08:30:00-03:00`; cada capítulo
  parte de um navegador novo com a semente do fim do anterior (`inicio`, `apos-cap02`, `apos-cap04`, `apos-cap05`,
  `apos-cap06`). O relógio das cenas de Windows e as horas do painel do EcoTray acompanham o relógio do app (08:3x a
  08:5x; os horários abaixo são os previstos, ajustar ao ensaio).
- **Marcas:** `[BACKEND: ...]` o que o backend falso ou o EcoTray falso precisa ter; `[CENA WINDOWS n: ...]` cena de
  Windows simulada (outro agente constrói, fiel a `installer_gui.py`, `dashboard.py` e `tray_app.py`); `[ILUSTRAÇÃO: ...]`
  desenho por código no estilo da marca; `[ZOOM: ...]` zoom que dura a frase inteira.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Balança e impressora: o EcoTray". | (sem fala) |
| Dashboard, logado como Rafael Nogueira (semente `inicio`: sem EcoTray, impressão direta e balança desligadas). A câmera fica no centro da tela. | Oi! Neste tutorial a gente vai ligar o computador do escritório da Recicla Vale Metais na balança e na impressora do pátio. |
| [ILUSTRAÇÃO: O peso digitado à mão: o visor de uma balança de plataforma marca "312 kg" (a carroça do Valdir); ao lado, o campo de peso de um pedido recebe, tecla por tecla, "321"; na palavra "vinte", o "321" fica vermelho ao lado do "312".] | Hoje, o Marcos lê o peso no visor da balança e digita no sistema. A balança marca trezentos e doze quilos, e no sistema entra trezentos e vinte e um. |
| [ILUSTRAÇÃO, continua: um comprovante abre como PDF numa aba de navegador; uma seta pontilhada leva até uma impressora de cupom, com um "?" no meio do caminho.] | E o comprovante abre num PDF, que ainda precisa mandar pra impressora. |
| [ILUSTRAÇÃO, continua: o visor ligado por um cabo ao computador, com o ícone do EcoTray no meio; o "312 kg" corre pelo cabo até o campo de peso; o cupom sai da impressora. Na palavra "cupom".] | Com o EcoTray, o peso entra sozinho e o cupom sai na hora. |
| Cartão discreto: "Balança: depende do plano". | A parte da balança depende do plano contratado. A da impressora funciona em qualquer plano. |
| Cartão discreto: "Antes: Clientes, fornecedores e a ficha do parceiro". | Se você ainda não viu o tutorial Clientes, fornecedores e a ficha do parceiro, dá uma olhada antes. [pause] Vamos começar pelo que é o EcoTray. |

### cap01 · O que é o EcoTray (vinheta: ECOTRAY)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`). No Dashboard, a câmera desce ao rodapé do menu lateral e clica em "Configurações" (engrenagem, ao lado de "Sair"); página "Configurações do Sistema"; clique na aba "Integrações": cabeçalho "Integrações" ("Configure integrações com impressora e balança digital") e o cartão do EcoTray. | Tudo do EcoTray fica em Configurações, na aba Integrações. |
| [ILUSTRAÇÃO: A ponte: à esquerda, uma janela de navegador com o EcoSistema; à direita, o visor da balança e uma impressora de cupom; entre os dois lados, um "X" cinza no lugar do cabo, que aparece na palavra "impressora".] | Mas o que é o EcoTray? O EcoSistema roda no navegador. E o navegador, sozinho, não conversa com a balança nem com a impressora. |
| [ILUSTRAÇÃO, continua: o "X" sai; no meio entra um computador com o ícone do EcoTray perto do relógio, ligado por cabos à balança e à impressora e, por uma linha verde, ao navegador. Na palavra "ponte", a linha acende.] | O EcoTray é um programa pequeno, instalado no computador onde elas estão ligadas. Ele faz a ponte. |
| [ILUSTRAÇÃO, continua: um pulso verde com "18,6 kg" sai do visor, passa pelo EcoTray e chega ao navegador; depois um cupom faz o caminho de volta, do navegador ao EcoTray e à impressora.] | A balança manda o peso pro EcoTray, e ele passa pro sistema. Na volta, o sistema manda o cupom, e o EcoTray entrega na impressora. |
| De volta à tela; zoom no texto do cartão: "Programa para Windows e macOS que conecta impressora térmica e balança digital ao sistema. Leve (~20MB), inicia automaticamente com o computador/notebook e roda em segundo plano." | Ele funciona no Windows e no Mac, abre junto com o computador e fica num cantinho da tela, perto do relógio. Esse cantinho se chama bandeja. |
| [ZOOM: o selo "EcoTray não detectado nesta estação", embaixo do logo do EcoTray] | Repara no selo: EcoTray não detectado nesta estação. Estação é o computador em que você está. Ainda não tem EcoTray aqui. |
| A câmera desce pela tela: a seção "Impressora" com o botão "Como funciona?", a chave "Integração com Impressora" e a seção "Integração com Balança Digital" com o seu "Como funciona?"; volta ao botão "Baixar Instalador", sem clicar. | Embaixo ficam a impressora e a balança, cada uma com o botão Como funciona, que mostra o passo a passo. E tudo começa no Baixar Instalador. |

### cap02 · Baixar e instalar (vinheta: INSTALAÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em Configurações › "Integrações". Clique em "Baixar Instalador": janela "Baixar Instalador" ("Instalador v1.7.22", "Selecione o sistema operacional do seu computador") com "Windows" (".exe instalador") e "macOS" (".dmg instalador"); na palavra "Windows", clique em "Windows": a janela fecha. [BACKEND: `app_config` `ecotray_version` = "1.7.22"] | Vamos instalar. Clico em Baixar Instalador e escolho o sistema do computador. Aqui, Windows. |
| [BACKEND: a aba nova de `bridge-downloads/EcoTray - Instalador.exe` não entra no vídeo; a cena assume daqui] [CENA WINDOWS 1, aviso do navegador: área de trabalho genérica no estilo Windows, sem logo; barra de tarefas com a bandeja e o relógio "08:33" "10/11/2026"; a janela de um navegador genérico (sem logo) com a gravação do app. No canto de downloads do navegador surge o item "EcoTray - Instalador.exe" com o aviso de que o arquivo pode ser perigoso e uma setinha ao lado.] | O download começa, e o navegador avisa que o arquivo pode ser perigoso. |
| (cena) A câmera fica no aviso. | Uma dica: esse aviso é normal com instaladores. O navegador fica desconfiado de programa pouco baixado. |
| (cena) O cursor clica na setinha do aviso; abre o menu com "Manter"; clique em "Manter"; o item fica pronto, "EcoTray - Instalador.exe". | Clico na setinha do aviso e escolho Manter. |
| [CENA WINDOWS 2, SmartScreen: clique no arquivo baixado; abre a janela azul do Windows, sem logo: "O Windows protegeu o computador", "O Microsoft Defender SmartScreen impediu a inicialização de um aplicativo não reconhecido. A execução deste aplicativo pode colocar o computador em risco.", o link "Mais informações" e o botão "Não executar".] | Abrindo o arquivo, o Windows ainda mostra uma tela azul, a do SmartScreen. |
| (cena) Clique em "Mais informações": aparecem "Aplicativo: EcoTray - Instalador.exe", "Editor: Editor desconhecido" e o botão "Executar assim mesmo", ao lado de "Não executar"; clique em "Executar assim mesmo". | Clico em Mais informações e depois em Executar assim mesmo. |
| [CENA WINDOWS 3, instalador (`installer_win/installer_gui.py:102-257`): janela 520×420 no centro da tela, sem barra de título, borda de 1 px #1f1f1f, fundo #0a0a0a, Montserrat. Cabeçalho de 90 px #121212: logo `ecotray-logo-light.png` (42 px de altura, em x 20, y 10), "Instalador — Balança & Impressora" (#999999, 10, em x 20, y 58) e "✕" (#999999, 13, em x 488, y 18). Corpo com margem 32/28: "O EcoTray conecta sua balança serial e impressora" / "diretamente ao sistema web, rodando silenciosamente" / "na bandeja do Windows." (#999999, 11); linha #1f1f1f; "Pronto para instalar" (#ebebeb, 11 negrito); barra de progresso de 10 px (trilho #121212, verde #45a167); "0%" à direita (#999999, 9). Rodapé de 62 px #121212: botão "  Instalar  " (fundo #45a167, texto #0a0a0a, 11 negrito) à esquerda e "EcoTray v1.7.22" (#999999, 9) à direita. Clique em "Instalar".] | Abre o instalador do EcoTray. É só clicar em Instalar. |
| (cena) O botão vira "  Instalando..." (desligado) e o texto avança com a barra: "Verificando versão mais recente..." / "Verificando servidor de downloads..." (5%) e "Pronto para baixar" (15%); "Baixando EcoTray..." / "Baixando EcoTray.exe..." (20%), depois "9.7 MB / 19.4 MB" até "19.4 MB / 19.4 MB" (75%); "Instalando arquivos..." / "Copiando arquivos..." (78%); "Configurando inicialização automática..." / "Criando atalho de inicialização..." (88%) e "Criando atalho na Área de Trabalho..." (92%); na área de trabalho aparece o atalho "EcoTray" com o ícone do EcoTray. | Ele baixa a versão mais nova, instala e cria um atalho na área de trabalho. |
| (cena) "Finalizando..." / "EcoTray instalado com sucesso!" (100%) e, logo depois, "✓  Instalado com sucesso!" em verde #45a167, "EcoTray está iniciando na bandeja do sistema.", o botão "  Fechar  " e, no rodapé, "Iniciando na bandeja do sistema..." em verde. Na bandeja, ao lado do relógio, surge o ícone do EcoTray (`assets/icon.png`) com a bolinha amarela #eab308 no canto. | Pronto, instalado. E ele já fica configurado pra abrir sozinho toda vez que o Windows liga. |
| (cena) Clique em "  Fechar  ": o instalador some; o painel do EcoTray abre 2 s depois de o ícone surgir na bandeja (`ecotray.py:664-665`; `dashboard.py`), 520×720 no centro, sem barra de título, sempre por cima: cabeçalho de 80 px #121212 com o logo (36 px), "Ponte Desktop — Balança & Impressora" (#999999), "● 1 cliente(s)" (verde), "–" e "✕"; faixa de 3 px âmbar #d7a042; abas "Integrações" (ativa: fundo #45a167, texto #0a0a0a) e "Logs"; cartão "  Parcialmente ativo" (âmbar, 12 negrito) com "ws://127.0.0.1:8054" (Consolas, cinza). A câmera vai do painel ao ícone da bandeja. | Clico em Fechar, e a janela do EcoTray abre. O ícone dele fica na bandeja, perto do relógio. |
| (cena) A câmera desce pelo painel: "Balanças" (com "↻"): "⏳ Aguardando o sistema" (âmbar), "Abra o EcoSistema no navegador e ligue a Balança em Configurações › Integrações. Assim que o sistema confirmar, as balanças aparecem aqui." e o botão cinza "Configuração indisponível"; "Impressora" (com "↻"): "✓  POS-58", "1 impressora(s) — clique para definir padrão" e a linha "✓ POS-58" realçada; "Atividade Recente": "08:35:12  Impressora padrão: POS-58"; "WebSocket" "balança :8053  •  comandos :8054"; rodapé "EcoTray  v1.7.22" e "Atualizar Versão". Clique no "–": o painel some (segue na bandeja). | Nessa janela ficam as balanças, a impressora e o que o EcoTray fez por último. No tracinho, ela volta pra bandeja. |
| Fim da cena, de volta ao navegador em "Integrações". Clique em "Baixar Instalador" de novo; zoom em "macOS" (".dmg instalador"), sem clicar; fecha a janela com Esc. | No Mac, o caminho é o mesmo: escolha a opção do Mac, abra o instalador e clique em Instalar. Lá, o EcoTray fica na barra de menus, no alto da tela. |

### cap03 · O pareamento automático (vinheta: CONEXÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`), em Configurações › "Integrações"; a câmera no cartão do EcoTray. [BACKEND: EcoTray falso ligado em `ws://127.0.0.1:8054`; `get_status` com `version` "1.7.22", `printers` ["POS-58"], `default_printer` "POS-58" e `scales_lock_state` "unknown"] | Com o EcoTray instalado, o sistema acha ele sozinho. Não tem código pra digitar nem endereço pra configurar. |
| [ZOOM: o selo "v1.7.22" embaixo do logo do EcoTray, no lugar do "EcoTray não detectado nesta estação"] | Olha o selo: agora ele mostra a versão do EcoTray instalada neste computador. |
| [ILUSTRAÇÃO: O pareamento: um computador visto por dentro; o navegador manda um balão "EcoTray?" e o EcoTray responde "Aqui! v1.7.22"; uma linha verde liga os dois sem sair do computador. Na palavra "reconhecem", a linha acende.] | Isso é o pareamento: o sistema e o EcoTray se reconhecem. |
| [ILUSTRAÇÃO, continua: ao lado, um segundo computador, sem EcoTray e sem cabo de balança, fica cinza; a linha verde só existe no computador ligado à balança e à impressora. Na palavra "ligadas".] | O sistema procura o EcoTray dentro do próprio computador. Por isso, ele vai instalado no computador em que a balança e a impressora estão ligadas. |
| De volta à tela; a câmera no cartão do EcoTray. | E se um dia esse selo avisar que o EcoTray está desatualizado, é só fechar e abrir o EcoTray, que ele se atualiza. |

### cap04 · Conectar a impressora (vinheta: IMPRESSORA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`), em Configurações › "Integrações", seção "Impressora". [ILUSTRAÇÃO: uma impressora de cupom ligada ao computador por um cabo USB; o ícone do EcoTray perto do relógio. Na palavra "cabo".] | Agora a impressora. A impressora térmica, aquela de cupom, vai ligada no computador pelo cabo USB. |
| Liga a chave "Integração com Impressora": "Conectando ao EcoTray..." e, em seguida, "Conectado ao EcoTray" (verde) e o aviso "Conectado ao EcoTray!". [BACKEND: EcoTray falso: `list_printers` → `data` ["POS-58"], `data_meta` [{"name": "POS-58", "driver": "POS-58", "is_compatible": true}]] | No sistema, eu ligo a Integração com Impressora. Pronto: Conectado ao EcoTray. |
| Abre "Selecione a impressora" e escolhe "POS-58"; aparecem "Atualizar" e "Testar". [BACKEND: `profiles.direct_print_enabled` true e `direct_print_printer_name` "POS-58"] | A lista traz as impressoras deste computador. Escolho a nossa, a de cupom. |
| [CENA WINDOWS 4, a impressão: antes do clique, o painel do EcoTray volta pelo ícone da bandeja e fica à direita, por cima do navegador.] Clique em "Testar": no app, o aviso "Comprovante enviado para a impressora!"; no painel, a faixa verde "✓  Impresso em POS-58" surge embaixo por 3 s e "Atividade Recente" ganha, em cima, "08:41:07  Impresso em POS-58" (verde). [BACKEND: `print` → `print_result` success; `print_notification` e `activity` na 8054] | Clico em Testar. O comprovante vai pra impressora, e o EcoTray avisa que imprimiu. |
| [ILUSTRAÇÃO: o cupom de teste saindo da impressora de 58 mm com o texto do PDF de teste do app, feito para 80 mm: "Teste de Impressão", "Se você vê isso, está funcionando!" e "10/11/2026, 08:41:07"; na palavra "cortado", a borda direita do papel corta o fim das linhas ("...funcionan").] | Na impressora sai um cupom de teste, com a data e a hora. Saiu o cupom? A ligação está funcionando. Mas repara: ele saiu cortado do lado. |
| (cena) Clique no "–" do painel. No app, zoom no botão "Atualizar", ao lado da lista. | Se a impressora não aparecer na lista, confira o cabo e clique em Atualizar. |

### cap05 · Largura do papel e impressão turbo (vinheta: IMPRESSORA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`: impressão direta ligada com "POS-58"). [ZOOM: "Escala e Largura do Comprovante", com "Papel 80mm · Escala 100%"] | Isso é a largura do papel. A bobina da impressora da Recicla Vale é a pequena, de cinquenta e oito milímetros, e o sistema vem com oitenta milímetros. |
| [ILUSTRAÇÃO: A largura do papel: um cupom desenhado para 80 mm desce numa bobina de 58 mm; as bordas passam do papel e somem, cortadas, na palavra "cortado"; depois o mesmo cupom, em 58 mm, cabe inteiro.] | Com o papel mais estreito que o cupom, o lado sai cortado. Uma dica: cupom cortado quase sempre é a largura, e não a impressora. |
| Clique em "Ajustar Escala": janela "Ajuste do Comprovante Térmico"; em "Largura do papel da impressora", clique em "58 mm" ("bobina pequena"); a régua passa a "Papel: 58 mm" e a "Prévia do comprovante" estreita. | Em Ajustar Escala, eu escolho cinquenta e oito milímetros. A prévia já mostra o cupom do tamanho da bobina. |
| Zoom na nota "O comprovante será gerado no tamanho exato do papel selecionado, ocupando 100% da largura quando a escala estiver em 100%." | O sistema manda essa largura pro EcoTray, e ele imprime exatamente nela. Então, se o cupom sair cortado, confira aqui primeiro. |
| Zoom em "Escala fina", com "100" "%" e a régua de 50% a 100%. | A escala fina diminui o conteúdo dentro do papel, se precisar. Aqui fica em cem por cento. |
| Clique em "Testar impressão" ("Enviado direto via EcoTray."): avisos "Comprovante enviado para a impressora!" e "Comprovante de teste enviado para a impressora!"; clique em "Salvar"; o cartão passa a "Papel 58mm · Escala 100%". [BACKEND: `print` success; `profiles.receipt_paper_width_mm` = 58] | Testar impressão manda um cupom de exemplo. Agora ele sai inteiro, então eu salvo. |
| Zoom em "Impressão térmica turbo (beta)" ("Gera o comprovante mais rápido; se algo sair diferente, desligue"), com a chave desligada; o mouse para no "?": "Gera o comprovante mais rápido. Se algo sair diferente do normal, desligue." | E a impressão térmica turbo gera o comprovante mais rápido. Ela ainda está em teste: se algo sair diferente do normal, é só desligar. |

### cap06 · Conectar a balança (vinheta: BALANÇA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); em Configurações › "Integrações", a câmera desce até "Integração com Balança Digital" ("Configure a conexão com balança digital via EcoTray"), com "Como funciona?". | Agora a balança. Essa parte depende do plano contratado. Sem ela no plano, aqui aparece um cartão pra contratar, com o botão Pesar automático. |
| [ZOOM: a chave "Integração com Balança Digital" ("Requer EcoTray instalado e rodando neste computador"), desligada] | Uma dica: essa chave começa desligada, então ligue aqui pro peso começar a chegar. Na empresa em teste, a balança já vem liberada. |
| Liga a chave: aparecem "Unidade de medida padrão", "Casas decimais no peso", "Leitura contínua", o cartão de teste âmbar ("Conectada, aguardando peso da balança", "Conectada, mas sem peso chegando ainda") e "Balanças" com "Nenhuma balança configurada no EcoTray. Abra as configurações do EcoTray (ícone na bandeja) para cadastrar.". [BACKEND: EcoTray falso na 8053 aceita a conexão; recebe `unlock_scales` na 8054 e responde `unlock_result` unlocked; manda `scale_lock_status` unlocked e `scales_list` vazia] | Ligada, o sistema avisa o EcoTray, e a balança fica liberada nele. Agora é cadastrar a balança lá. |
| [CENA WINDOWS 5, o painel destrava: clique no ícone da bandeja; o painel volta à direita, por cima do navegador; em "Balanças", "Nenhuma balança configurada" e o botão verde "Configurar Balanças"; "Atividade Recente" ganha "08:44:10  Módulo Integração com Balança destravado" (verde).] | Na janela do EcoTray, a área das balanças liberou. Clico em Configurar Balanças. |
| [CENA WINDOWS 6, configurar: abre a janela "Configurar Balanças" (640×500, barra de título genérica com "Configurar Balanças", fundo #0a0a0a): faixa de 52 px #121212 com "Configurar Balanças" (13 negrito); tabela vazia com "Nome", "Porta", "Protocolo" e "Padrão"; botões "Adicionar", "Editar", "Remover", "Definir padrão" e "Detectar automaticamente"; embaixo, "Detectando balanças…" e, em seguida, "1 balança(s) detectada(s) — marcadas com ✓." (verde); rodapé com "Cancelar" e "Gravar" (verde).] | Ele procura sozinho a porta da balança, que é a entrada do cabo no computador, e marca com um tique. |
| (cena) Clique em "Adicionar": janela "Nova balança" (420×520, barra de título "Nova balança"); em "Nome" digita "Balança do pátio"; abre "Porta Serial" e escolhe "COM3  ✓ balança"; aparece em verde "detectado automaticamente — ajuste se precisar"; "Baud rate" 9600, "Data Bits" 8, "Parity" none, "Stop Bits" 1. | Em Adicionar, dou um nome, Balança do pátio, e escolho a porta marcada. |
| (cena) Zoom em "Protocolo": "Automático" (a lista não abre); embaixo, "Correção (×)" 1,0 com "1,0 = normal. Ex.: 10 corrige balança 10× menor." e o botão "Detectar automaticamente". | O protocolo, que é o jeito de cada balança mandar o peso, fica no Automático. O EcoTray reconhece o modelo sozinho. |
| (cena) Clique em "OK": a tabela mostra "Balança do pátio", "COM3", "Automático", "✓"; clique em "Gravar": a janela fecha; no painel, "Balanças" mostra "● Balança do pátio   0,000 kg  conectada  ✓ padrão" (verde) e "Atividade Recente" ganha "08:45:02  [scale:Balança do pátio] conectada"; na bandeja, o ícone perde a bolinha amarela. Clique no "–" do painel. [BACKEND: na hora do "Gravar", o EcoTray falso passa a anunciar a "Balança do pátio" (`scales_list` [{"id": "bal-patio", "name": "Balança do pátio", "connected": true}], `default_scale_id` "bal-patio") e manda `weight` "0.000" a cada 0,2 s] | OK e Gravar. Pronto: a Balança do pátio aparece conectada. |
| De volta ao navegador: em "Balanças", "Balança do pátio" com "Conectada", marcada como padrão; o cartão de teste fica verde: "Conectada", "Peso atual: 0,000 kg — última leitura às 08:45:05". | De volta ao sistema, a Balança do pátio já está na lista, e o teste fica verde. |
| [ZOOM: "Peso atual: 18,600 kg — última leitura às 08:45:20"] O peso sobe de 0,000 até 18,600 kg e para. [BACKEND: sequência de `weight` 0.000 → 18.600, estável] | O Marcos põe na balança o saco de latinha da Dona Cida. Dezoito quilos e seiscentos, ao vivo, aqui no teste. |
| Zoom em "Unidade de medida padrão" ("Quilograma (kg)") e "Casas decimais no peso" ("3"). | A unidade fica em quilo. As casas decimais dizem com quantos números depois da vírgula o peso entra no pedido. Aqui, três. |
| Zoom em "Leitura contínua" (desligada); o mouse para no "?": "Ativo: Após capturar, o campo peso continua se atualizando conforme a balança lê em tempo real, até incluir a pesagem." / "Desativado: Ao capturar, o peso fica fixo. Só muda ao capturar novamente." [ILUSTRAÇÃO: A leitura contínua: dois campos de peso depois do clique em capturar; "ligada": 18,6 vira 18,9 e 19,2 até o botão "Incluir"; "desligada": 18,6 parado. Na palavra "fixo".] | Com a leitura contínua ligada, depois de capturar, o peso segue mudando até você incluir. Desligada, ele fica fixo. Na Recicla Vale, fica desligada. |
| A câmera sobe pelas chaves "Integração com Impressora" e "Integração com Balança Digital", ligadas. | E repara: as chaves da impressora e da balança valem pro seu usuário. Se o Marcos usa esse computador com o login dele, ele liga também. |

### cap07 · Peso somente pela balança (vinheta: BALANÇA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`: balança ligada e "Balança do pátio" no EcoTray falso); em Configurações › "Integrações", zoom na chave "Peso somente pela balança" ("Regra da empresa, independente da integração deste computador"), desligada. | Logo abaixo da chave da balança fica a opção Peso somente pela balança. |
| [ILUSTRAÇÃO: Peso só pela balança: a carroça do Valdir na balança; o visor marca "312 kg" e o campo de peso do pedido recebe "312" com um cadeado; um teclado tenta trocar para "321" e o número não entra; na frase "nova leitura", o visor pisca e o campo se atualiza.] | Imagina a carroça do Valdir na balança: trezentos e doze quilos. Com a opção ligada, ninguém digita outro número por cima. Só uma nova leitura da balança troca o peso. |
| O mouse para no "?" da opção: "Ativo: Todos os usuários da empresa ficam impedidos de digitar ou alterar o peso bruto. Somente uma nova leitura da balança troca o peso." / "Desativado: O usuário pode digitar o peso manualmente ou capturar da balança." | E ela é uma regra da empresa: vale pra todos os usuários, em todos os computadores. |
| A câmera fica na chave. | Vale a pena ligar quando todo peso da empresa passa pela balança integrada. Aí ninguém troca o peso na mão. |
| A câmera fica na chave, desligada. | Com ela ligada, o peso entra só pela balança. Então, pra pesar, o EcoTray precisa estar aberto. Na Recicla Vale, por enquanto, ela fica desligada. |

### cap08 · O indicador de peso (vinheta: BALANÇA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), no Dashboard. [ZOOM: o rodapé à direita: o ícone da balança, o ponto cinza e "Balança do pátio · Aguardando peso"; ao centro, "EcoSistema v1.59.154"] [BACKEND: EcoTray falso conectado, com `scales_list` e sem `weight`] | Com a balança ligada no sistema, aparece um indicador no rodapé, em todas as telas. |
| (o zoom continua no rodapé) | Agora ele mostra Aguardando peso: o EcoTray está conectado, mas a balança não mandou peso nos últimos segundos. Normalmente, é a balança desligada. |
| O peso começa a chegar: "Balança do pátio · 312 kg", com o ponto verde. [ZOOM: o rodapé] [BACKEND: `weight` 0.000 → 312.000, estável] | O Marcos liga a balança, e a carroça do Valdir sobe: trezentos e doze quilos, ao vivo, com a bolinha verde. |
| Cartão discreto: "Balança desconectada". | E com o EcoTray fechado, ele mostra Balança desconectada. Isso a gente vê já já. |
| A câmera volta ao rodapé. | O indicador aparece pra quem tem a balança no plano e ligou a chave. |
| [ILUSTRAÇÃO: Onde fica o peso ao vivo: o computador do escritório, com o EcoTray e o cabo da balança, mostra no rodapé "Balança do pátio · 312 kg"; ao lado, um celular com o sistema aberto, sem cabo e sem esse rodapé. Na palavra "celular".] | Uma dica: o peso ao vivo fica no computador do EcoTray. No celular, o sistema funciona normal, só sem esse indicador. |

### cap09 · Quando o EcoTray cai (vinheta: CONEXÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), em Configurações › "Integrações", com o rodapé "Balança do pátio · 312 kg". [BACKEND: EcoTray falso com `weight` 312.000] [CENA WINDOWS 7, sair: clique com o botão direito no ícone do EcoTray na bandeja; o menu: "Abrir EcoTray" (negrito), linha, "EcoTray v1.7.22", "Balança: COM3@9600" e "Impressora: POS-58" (cinza), linha, "Reconectar balança", "Configurações", linha, "Atualizar Versão", linha, "Desinstalar", "Sair"; clique em "Sair": o ícone some da bandeja.] | E se o EcoTray fechar? Vamos ver. Clico com o botão direito no ícone dele e em Sair. |
| No navegador: o aviso "Balança desconectada. Verifique se o EcoTray está rodando." e o rodapé "Balança desconectada", com o ponto cinza. [ZOOM: o rodapé] [BACKEND: EcoTray falso desligado: 8053 e 8054 recusam conexão] | Na hora, o sistema avisa: Balança desconectada. E o rodapé mostra o mesmo. |
| [ILUSTRAÇÃO: Sem o EcoTray: a linha verde da ponte apaga; do lado do sistema, o comprovante abre como PDF numa aba, com o botão de imprimir, e o campo de peso recebe "312" digitado. Na palavra "funcionando".] | Com o EcoTray fechado, o peso não chega e o cupom não vai pra impressora. Mas o sistema continua funcionando. |
| [ILUSTRAÇÃO, continua: o PDF e o "312" digitado; na frase "Peso somente pela balança", o campo ganha o cadeado e um relógio de espera.] | O comprovante abre em PDF, pra imprimir do jeito de sempre, e o peso você digita à mão. Com o Peso somente pela balança ligado, a pesagem espera o EcoTray voltar. |
| De volta à tela, seção "Impressora": "EcoTray não encontrado" (vermelho), "Tentar conectar" e "Verifique se o EcoTray está aberto e rodando na bandeja do sistema (canto inferior direito do Windows). Após instalar, clique no ícone do EcoTray para iniciá-lo."; zoom no aviso. | Aqui em Integrações, a impressora mostra EcoTray não encontrado. |
| [CENA WINDOWS 8, abrir de novo: na área de trabalho, clique duplo no atalho "EcoTray"; em 2 a 3 s o ícone volta à bandeja, sem bolinha.] [BACKEND: EcoTray falso religado, com a "Balança do pátio" e `weight` 312.000] | Pra voltar, é só abrir o EcoTray. O atalho fica na área de trabalho. |
| No navegador, em segundos, o rodapé volta a "Balança do pátio · 312 kg" (ponto verde). Clique em "Tentar conectar": o aviso "Conectado ao EcoTray!" e "Conectado ao EcoTray" (verde). [BACKEND: a 8053 reconecta sozinha em até 10 s; a 8054 no clique] | E o sistema reconecta sozinho, em poucos segundos, sem atualizar a página. Se a impressora demorar, o Tentar conectar chama na hora. |
| Zoom no texto do cartão do EcoTray: "...inicia automaticamente com o computador/notebook e roda em segundo plano." | Como o EcoTray abre junto com o Windows, no dia a dia é só ligar o computador. |

### cap10 · Driver incompatível (vinheta: IMPRESSORA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), em Configurações › "Integrações", seção "Impressora"; abre "Selecione a impressora": "POS-58" e, com o triângulo amarelo, "Generic / Text Only"; zoom na lista. [BACKEND: EcoTray falso com duas impressoras: `data` ["POS-58", "Generic / Text Only"]; `data_meta` da segunda com `driver` "Generic / Text Only", `is_compatible` false e o `incompatible_reason` de `print_manager.py:87-92`] | Por último, um aviso que evita cupom em branco. Imagina que instalaram outra impressora neste computador. Repara no triângulo amarelo do lado dela. |
| [ILUSTRAÇÃO: O driver: o computador manda o cupom como uma imagem (logo, tabela e total); pelo driver do fabricante, o cupom sai igual no papel; pelo driver genérico, que só entende letras, a imagem não passa e o papel sai em branco. Na palavra "imagem".] | Driver é o programa que ensina o computador a falar com a impressora. Essa foi instalada com o driver genérico do Windows, que só imprime texto. E o cupom do sistema sai como imagem. |
| Escolhe "Generic / Text Only": o aviso amarelo com o motivo e, embaixo da lista, a caixa âmbar "Driver incompatível (Generic / Text Only)" com "Driver "Generic / Text Only" só imprime texto puro — não suporta o cupom térmico (que é gerado como imagem). Troque pelo driver térmico real da sua impressora (ex: POS-58, GP-58, Elgin i9, Bematech, ou o driver oficial do fabricante).". [ZOOM: o título da caixa, "Driver incompatível (Generic / Text Only)"] | Escolhendo ela, o sistema avisa na hora: Driver incompatível. E o EcoTray segura a impressão, pra não sair folha em branco. |
| Zoom em "Troque pelo driver térmico real da sua impressora". | A saída é instalar o driver do fabricante da impressora. Até lá, use uma com o driver certo, como a nossa. |
| Escolhe "POS-58" de volta: a caixa some. [BACKEND: `profiles.direct_print_printer_name` = "POS-58"] | Volto pra nossa impressora de cupom, e o aviso some. |
| A câmera fica na lista. | Uma dica: a impressora puxa o papel e ele sai em branco, sem nenhum aviso? Quase sempre é o driver também. |
| A câmera fica na lista. | O sistema reconhece o driver genérico pelo nome. Com outro driver errado, a folha sai limpa, e a saída é a mesma: o driver do fabricante. |

### cap11 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o instalador com "✓  Instalado com sucesso!" e o selo "v1.7.22". | Pronto! Recapitulando: a gente instalou o EcoTray, passando pelos avisos do navegador e do Windows, e viu o sistema se conectar com ele sozinho. |
| Montagem rápida: "Conectado ao EcoTray", o "Testar" e o "58 mm". | Ligou a impressora, fez o teste e acertou a largura do papel em cinquenta e oito milímetros. |
| Montagem rápida: "Configurar Balanças" e "Peso atual: 18,600 kg". | Ligou a balança, cadastrou a balança do pátio no EcoTray e viu o peso chegando ao vivo. |
| Montagem rápida: "Peso somente pela balança", o rodapé "Balança do pátio · 312 kg", "Balança desconectada" e "Driver incompatível". | Conheceu o Peso somente pela balança, o indicador do rodapé, o que acontece quando o EcoTray fecha e o aviso de driver incompatível. |
| Cartão "Próximo: Caixa: abrir, fechar e o cofre"; cartela final. | No próximo tutorial, a gente abre o caixa e começa o dia. Até lá! |
