# Roteiro T1 · Configurações e identidade da empresa

> **Atualização Dominex 1.38.19 (aula já entregue na 1.38.6).** Regravar só o **cap11 (Onde ficam as integrações)**: a tela mostra quatro subabas, "WhatsApp", "Cobranças (Asaas)", "Impressora fiscal" e "API Pública"; passo novo: zoom na "Impressora fiscal" (sem clicar) entre Cobranças e API Pública. Falas: `T01/narracao/emendas_1.38.19.txt`.


Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T01/inventario.md`).
Todos os nomes, documentos e telefones são fictícios.

- **Título final:** Configurações e identidade da empresa
- **Vinhetas (áreas):** CONFIGURAÇÕES · IDENTIDADE · MARCA · REGIONAL · USABILIDADE · PREFERÊNCIAS · INTEGRAÇÕES · SEGURANÇA · RESUMO
- **Antes:** Boas-vindas à Dominex (T0, ilustrada: já explicou tutoriais, Guia Técnico, suporte e assinatura; não se repete aqui)
- **Próximo:** Usuários, cargos e permissões (T2)
- **Duração estimada:** ~12 min de vídeo (1.775 palavras de fala, ~11,4 min de voz a 2,6 palavras/s; o T3, com o mesmo tamanho, saiu com 12:13)
- **Estado inicial (fim do T0, conta nova):** Glacial Cold Brasil só com nome e segmento "Refrigeração e Climatização"; Camila Duarte (admin)
  logada; sem logo, contato nem endereço; origens Indicação, Instagram, Google e WhatsApp; "Consumo de estoque na OS" e
  "Perguntar sobre receita ao finalizar OS" desligados; módulo White Label contratado.
- **Dados usados (fictícios):** CNPJ 91.520.340/0001-07 (dígitos verificadores válidos); telefone (21) 3000-1000;
  contato@glacialcold.example; CEP 24230-190, Rua Moreira César, 200, Icaraí, Niterói/RJ; logo `logo-horizontal.png` e ícone
  `icone.png` (pasta do mundo `rec/fakebase/storage/company-logos/glacial/`); cor da marca `#EEB770` (dourado do emblema).
- **Estado final:** dados, endereço, logo e ícone preenchidos; White Label **desligado** (cor e imagens ficam guardadas);
  "Consumo de estoque na OS" e "Perguntar sobre receita ao finalizar OS" **ligados**; tema claro, Menu Lateral e menu escuro
  como no início; origens como no início (a "Panfleto" criada no cap09 é excluída no mesmo capítulo). Vira `seeds-extra/t1/apos-cap13.json`.
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar),
  `[ILUSTRAÇÃO: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Configurações e identidade da empresa". | (sem fala) |
| Tela inicial da Dominex, logada como Camila Duarte (Glacial Cold Brasil); a câmera desliza devagar pelo menu lateral. | Oi! Neste tutorial a gente vai deixar a Dominex com a cara da sua empresa: o logo, os dados, a cor da marca e as preferências do dia a dia. |
| A câmera desce até o rodapé do menu e para no botão "Configurações" (engrenagem), ao lado de "Sair". | É daqui que sai o que aparece nos recibos e nos relatórios. Fazendo uma vez, vale pra tudo. |
| A câmera volta a deslizar pelos grupos do menu lateral. | O menu da esquerda também se ajusta ao plano da empresa e ao cargo de cada pessoa, então cada um vê o que faz parte do seu trabalho. |
| Cartão discreto: "Antes: Boas-vindas à Dominex". | Se você ainda não viu o tutorial Boas-vindas à Dominex, dá uma olhada antes. [pause] Vamos começar abrindo as Configurações. |

### cap01 · Onde fica e como salva (vinheta: CONFIGURAÇÕES)

| Tela | Fala |
| --- | --- |
| Clique em "Configurações" no rodapé do menu; abre a tela com o título "Configurações" e o subtítulo "Gerencie as configurações do sistema", na aba "Empresa". | As configurações ficam no rodapé do menu, do lado do Sair. Clicou, abre a tela com tudo da empresa. |
| A câmera percorre as abas "Empresa", "Regional", "Usuários e Permissões", "Usabilidade", "Atalhos", "Aparência" e "Integrações"; zoom em "Usuários e Permissões". | No alto ficam as abas: Empresa, Regional, Usuários e Permissões, Usabilidade, Atalhos, Aparência e Integrações. A de Usuários e Permissões é o assunto da próxima aula, então hoje a gente passa pelas outras. |
| Zoom no selo do canto superior direito do cabeçalho ("Salvo"). | Aqui o salvamento é automático. Pode ir preenchendo que a Dominex salva sozinha, e esse selo no canto avisa quando já gravou. |
| Aba "Empresa": clique no fim do campo "Nome da Empresa", digita um espaço e apaga; o selo passa por "Alterações não salvas", "Salvando…" e "Salvo". [TESTAR: o texto fica igual ao salvo; se o selo não passar pelos três estados, digitar "x", esperar o "Salvo" e apagar] | Olha: eu mexo no nome, o selo mostra Alterações não salvas, depois Salvando, e em seguida Salvo. Pronto, gravado. |

### cap02 · O logo da empresa (vinheta: IDENTIDADE)

| Tela | Fala |
| --- | --- |
| Aba "Empresa": cartão "Dados da Empresa"; zoom na seção "Identidade Visual" ("Logo da empresa para documentos e sistema") com a área "Clique para enviar o logo" e a dica "PNG, JPG até 5MB". | Primeiro, o rosto da empresa: o logo. Na seção Identidade Visual, é só clicar em Clique para enviar o logo. Pode ser uma imagem em PNG ou JPG, de até cinco megas. |
| Passo `upload` do arquivo `logo-horizontal.png` na área do logo; a miniatura aparece com os botões "Substituir" e "Remover". [TESTAR: upload no bucket `company-logos` e miniatura com a imagem; o app não mostra aviso de sucesso, quem confirma é a miniatura] | Escolho o arquivo e pronto: o logo aparece aqui e já fica salvo, com os botões Substituir e Remover do lado. |
| Clique em "Remover": janela "Remover logo?" ("O logo atual será removido permanentemente."); clique em "Cancelar"; o logo continua na tela. | Se um dia quiser tirar, o Remover pede uma confirmação antes. Aqui eu cancelo, o logo fica. |
| A câmera volta à miniatura do logo. | Esse logo sai no cabeçalho dos recibos, das propostas e dos relatórios. Uma dica: use um arquivo com boa resolução, que ele fica nítido no papel. |

### cap03 · Dados cadastrais e contato (vinheta: IDENTIDADE)

| Tela | Fala |
| --- | --- |
| Rola até "Dados Cadastrais" ("Razão social, documento e informações oficiais"); zoom em "Nome da Empresa" (Glacial Cold Brasil) e no campo "CNPJ/CPF". | Agora os dados cadastrais. O nome da empresa já está aqui, Glacial Cold Brasil, e logo abaixo fica o campo CNPJ ou CPF. |
| Clique em "CNPJ/CPF" e digita `91520340000107`; a máscara entra sozinha e mostra 91.520.340/0001-07. | Eu digito só os números, e a máscara entra sozinha. |
| Zoom na caixa cinza de "Segmento de Atuação da Empresa" ("Refrigeração e Climatização") e no texto de apoio. | O segmento já vem definido: Refrigeração e Climatização. É ele que libera as ferramentas do seu ramo, como a Área do Técnico. Se o ramo da empresa mudar, é só falar com a Dominex. |
| Rola até "Contato" ("Telefone e e-mail da empresa"): clique em "Telefone" e digita `2130001000` ((21) 3000-1000); clique em "Email" e digita `contato@glacialcold.example`. | Em Contato vão o telefone e o e-mail da empresa. |
| Zoom nos interruptores "Exibir em documentos" ao lado de "Nome da Empresa", "CNPJ/CPF", "Telefone" e "Email" (todos ligados). | Repara que cada dado tem um interruptor, o Exibir em documentos. Ligado, o dado sai impresso. |
| Clique no interruptor "Exibir em documentos" do "Email" (desliga) e clique de novo (liga). | Se algum dado não deve sair impresso, é só desligar o dele: o dado continua cadastrado e deixa de sair nos recibos e nos relatórios de estoque, de financeiro e de RH. Aqui eu deixo todos ligados. |

### cap04 · Endereço pelo CEP (vinheta: IDENTIDADE)

| Tela | Fala |
| --- | --- |
| Rola até "Endereço" ("Localização física da empresa"); zoom no título com o interruptor único "Exibir em documentos". | Falta o endereço, e o CEP faz o trabalho. Clico no campo CEP e digito. |
| Clique em "CEP" e digita `24230190`; ao completar, toast "Endereço encontrado!" e se preenchem "Endereço" (Rua Moreira César), "Bairro" (Icaraí) e "UF / Cidade" (RJ, Niterói). [BACKEND: `cep-lookup` já responde 24230-190] | Completou os oito números, a Dominex traz a rua, o bairro e a cidade. |
| Clique em "Número" e digita `200`; a câmera passa pelo "Complemento" (vazio). | O número e o complemento eu completo na mão. Aqui é o duzentos. |
| A câmera para no campo "Endereço" (placeholder "Rua, Avenida…"), sem digitar. | Uma dica: se você não souber o CEP, é só digitar o nome da rua em Endereço, que a Dominex vai sugerindo as opções. |
| Zoom no título "Endereço" com o interruptor "Exibir em documentos". | E repara que aqui o Exibir em documentos é um só, que vale pro endereço inteiro. |

### cap05 · A cor e o logo da sua marca (vinheta: MARCA)

| Tela | Fala |
| --- | --- |
| Volta à aba "Empresa" e rola até a seção "White Label" ("Personalize o sistema com a identidade visual da sua marca"): interruptor "Ativar White Label" ("Substitui o logo e a cor padrão do sistema"), desligado. | Agora a marca no sistema inteiro, com o White Label. É o módulo que personaliza a Dominex com a identidade da sua empresa. |
| Clique em "Ativar White Label"; as opções aparecem logo abaixo. [BACKEND: `PATCH company_settings` devolve a linha; módulo `white_label` já está no seed] | Pra ver a sua cor no sistema inteiro, é só ligar o Ativar White Label. Ligado, a Dominex passa a usar o logo e a cor da sua empresa no lugar dos nossos. |
| Rola até "Logo completo" ("Usando o logo da empresa por padrão") e "Ícone (1:1)", lado a lado; em "Logo completo", clique em "Substituir"; passo `upload` da versão da marca com o texto branco (`/home/claude/brand-fix/assets/glacial_horizontal_texto_branco.png`, pedido do Kaik 31/10: o menu é escuro); a caixa mostra o logo novo e o menu lateral passa a usá-lo, sem fundo branco. [TESTAR: upload do Logo completo e o logo no menu lateral escuro] | O Logo completo começa com o logo da empresa. Como o menu é escuro, eu troco pela versão com o texto branco: Substituir, escolho o arquivo, e pronto. |
| Zoom no texto do ícone ("Ícone quadrado para o menu lateral recolhido. 128×128px."); clique em "Enviar ícone"; passo `upload` de `icone.png`; o ícone aparece na caixa. [TESTAR: upload do ícone e miniatura] | E o Ícone é a versão quadrada, que aparece quando o menu lateral fica recolhido. Vou enviar o ícone do mesmo jeito, e ele já aparece aqui. |
| Rola até "Cor primária" ("Substitui a cor verde padrão do sistema"); clique no botão da cor: abre o seletor, com a paleta, o campo do código da cor e a faixa de matiz. | Agora a cor primária. Clico no botão da cor, e abre o seletor, com as cores prontas e um campo pra digitar o código da cor. |
| Digita `#EEB770` no campo do código; botões, abas e destaques passam do verde ao dourado na hora; fecha o seletor. [TESTAR: `ColorPicker` em 1920×1080, digitar e colar no campo do código; se o campo recusar o digitado, escolher `#EEB770` por `eval` no `input`] | Eu digito o código do dourado da marca da Glacial. Olha: os botões, as abas e os destaques já mudam na hora. Uma dica: o código da cor vem do manual da marca, ou de quem fez o seu logo. |
| Clique no botão de recolher o menu lateral: aparece o ícone da marca; abre o menu de novo: volta o logo. [TESTAR: seletor do botão de recolher e a troca ícone/logo no menu] | E, recolhendo o menu, aparece o ícone. Abrindo de novo, volta o logo. |

### cap06 · QR Code, relatório e link do cliente (vinheta: MARCA)

| Tela | Fala |
| --- | --- |
| Rola até "QR Code" ("Personalize o visual dos QR Codes gerados pelo sistema, com o logo da sua marca no centro"): "Estilo dos pontos", "Cantos", "Cor do QR Code" e a "Pré-visualização". | A mesma marca vale pros QR Codes que a Dominex gera, como o da etiqueta de cada equipamento, com o seu logo no centro. |
| Clique em "Estilo dos pontos" e escolhe "Arredondado"; em "Cantos", escolhe "Arredondado"; a prévia muda a cada escolha. | Em Estilo dos pontos e em Cantos, eu escolho Arredondado, e a prévia mostra como fica. |
| Zoom em "Cor do QR Code", sem trocar a cor. | Na Cor do QR Code, vale escolher um tom escuro, pra câmera do celular ler com facilidade. |
| Rola até "Cabeçalho do Relatório de Serviço" ("Personalize o visual do cabeçalho que aparece no relatório da OS concluída"): prévia ao vivo com os dados da empresa; zoom em "Cor de fundo do cabeçalho", "Cor do texto" e "Tamanho do logo". | Descendo, o Cabeçalho do Relatório de Serviço. É o topo do relatório que o cliente recebe quando a ordem de serviço é concluída, e a prévia mostra como vai ficar. |
| Em "Tipo de logo no relatório", clique em "Ícone" e depois em "Logo Completo"; a prévia acompanha. | Dá pra ajustar as cores e o tamanho do logo, e escolher se vai o Logo Completo ou só o Ícone. |
| Volta ao topo da seção, em "Imagem ao compartilhar a OS" ("Define a imagem que aparece no WhatsApp e em outros aplicativos ao compartilhar o link público da Ordem de Serviço."); clique em "Usar logo da empresa"; toast "Imagem social gerada com o logo da empresa."; clique em "Ajustar arte": editor com "Prévia nos dois formatos" ("Cartão grande" e "Miniatura compacta"); fecha sem salvar. [BACKEND: storage `company-logos` com CORS nos GET da imagem (a prévia usa `fetch`) e grava `os_social_image_url` e `os_social_image_mode`] [TESTAR: abrir e fechar o editor sem alterar] | E lá em cima, a Imagem ao compartilhar a OS. É a imagem que aparece no WhatsApp quando você manda o link da ordem de serviço pro cliente. Em Usar logo da empresa, ela é gerada na hora, e em Ajustar arte você vê como fica no cartão grande e na miniatura. |
| Clique em "Ativar White Label" (desliga); o sistema volta ao verde da Dominex. | Pra manter a sua cor no sistema, é só deixar o White Label ligado. Eu vou desligar aqui pra seguir com o padrão, e o verde da Dominex volta. |

### cap07 · Idioma, moeda e fuso (vinheta: REGIONAL)

| Tela | Fala |
| --- | --- |
| Clique na aba "Regional": cartões "Meu idioma", "Padrões da empresa" e "Perfil Comportamental". | Passando pros padrões, na aba Regional. Aqui ficam o idioma, a moeda e o fuso horário. |
| Zoom em "Meu idioma": seletor "Idioma" (Português) e o texto "O idioma que VOCÊ vê no sistema. Aplica na hora, só para você." (sem trocar). | Em Meu idioma, cada pessoa escolhe o idioma que vê no sistema. Aplica na hora, e vale só pra ela. |
| Zoom em "Padrões da empresa" ("Idioma padrão, moeda e fuso horário para toda a empresa"): "País da empresa" (Brasil), "Idioma padrão da empresa", "Moeda" e "Fuso horário". | Já os Padrões da empresa valem pra todo mundo: o país, o idioma padrão, a moeda e o fuso horário. Quem é administrador ajusta essa parte. |
| Clique em "Moeda": abre a lista com bandeiras; fecha com Esc. Clique em "Fuso horário": abre a busca "Buscar fuso (ex: Sao Paulo)"; fecha com Esc, sem trocar nada. [TESTAR: fechar as duas listas sem mudar o valor; conferir no seed país Brasil, moeda real e fuso de Brasília] | A lista de moedas traz as bandeiras, e no fuso dá pra buscar pelo nome da cidade. Como a Glacial fica em Niterói, o Brasil, o real e o horário de Brasília já estão certos, então eu não troco nada. |
| Zoom no aviso fixo abaixo da moeda ("A moeda é a de operação da empresa. Trocar não converte os valores já registrados, eles continuam com o número original."). | A moeda é a de operação da empresa, então vale deixar a certa já no começo. Se um dia você trocar, os valores já lançados continuam com o mesmo número. |
| Zoom no cartão "Perfil Comportamental" ("Como o teste comportamental (DISC) se comporta para os funcionários."), sem clicar. | O Perfil Comportamental, do teste dos funcionários, a gente vê no tutorial de Ferramentas de RH. |

### cap08 · Como o sistema se comporta (vinheta: USABILIDADE)

| Tela | Fala |
| --- | --- |
| Clique na aba "Usabilidade": cabeçalho "Usabilidade" ("Preferências de comportamento do sistema") e os grupos "Ordens de Serviço", "Interface", "Segurança" e "Agenda". | Agora o jeito de trabalhar do dia a dia, na aba Usabilidade. São preferências em quatro grupos: Ordens de Serviço, Interface, Segurança e Agenda. |
| Zoom no grupo "Ordens de Serviço" ("Salvamento Automático", "Exibir Valores", "Exigir Assinatura", "Salvar fotos no dispositivo", "Consumo de estoque na OS"); liga "Consumo de estoque na OS"; toast "Preferência salva!". [BACKEND: `PATCH company_settings` devolve a linha] | Em Ordens de Serviço tem o Consumo de estoque na OS. Ligado, o técnico registra os materiais que usou e o estoque baixa quando a ordem é finalizada. Eu ligo, e pronto, preferência salva. |
| Zoom em "Exigir Assinatura" ("Tornar obrigatória a assinatura do cliente ao finalizar OS"), sem ligar. | E o Exigir Assinatura deixa a assinatura do cliente obrigatória na hora de finalizar. |
| Zoom em "Confirmar Exclusões" (grupo "Segurança") e em "Exibir Feriados" (grupo "Agenda"). | Em Segurança, o Confirmar Exclusões pergunta antes de apagar um registro. E na Agenda, o Exibir Feriados mostra os feriados no calendário. |
| [ILUSTRAÇÃO: três caixas, "Da empresa", "Deste aparelho" e "Só sua", cada uma com um exemplo de interruptor: "Consumo de estoque na OS", "Tabelas Compactas" e "Incluir compras no cartão"] | Uma coisa importante: cada preferência vale pra quem deve. O consumo de estoque vale pra empresa inteira. A maioria dos outros interruptores vale só neste aparelho. E algumas são só suas, em qualquer aparelho. |
| Rola até o cartão "Orçamento, OS e financeiro" ("O que vira lançamento no financeiro automaticamente, ao aprovar um orçamento ou ao finalizar uma Ordem de Serviço"); zoom em "Ao aprovar um orçamento" com os botões "Já recebi" e "Vou receber depois" (sem trocar). | Mais abaixo, o cartão Orçamento, OS e financeiro define o que vira lançamento no financeiro. Ao aprovar um orçamento, você escolhe entre Já recebi, que lança como receita recebida, e Vou receber depois, que gera uma conta a receber. |
| Liga "Perguntar sobre receita ao finalizar OS"; toast "Preferência salva!". | E ligando o Perguntar sobre receita ao finalizar OS, ao concluir uma ordem de serviço a Dominex pergunta se você quer lançar a receita no financeiro. |
| Zoom no cartão "Movimentações financeiras" ("Incluir compras no cartão"), sem mexer. | Tem ainda o cartão de Movimentações financeiras, que a gente vê no tutorial do Financeiro. |

### cap09 · Origens dos clientes (vinheta: USABILIDADE)

| Tela | Fala |
| --- | --- |
| Rola até o cartão "Origens" ("Lista de origens usada no cadastro de clientes e nas oportunidades do CRM"): Indicação, Instagram, Google e WhatsApp; clique em "Gerenciar origens"; abre a janela "Origens de Clientes". | Agora as origens dos clientes, no fim da Usabilidade. É a lista que aparece no cadastro do cliente e no CRM, e a gente monta do nosso jeito em Gerenciar origens. |
| Na linha tracejada, "Nova origem...": digita "Panfleto"; escolhe um ícone e uma cor; clique em "Adicionar"; toast "Origem criada!". [TESTAR: o seletor de ícone mostra nomes em inglês; escolher o primeiro da lista sem ler os nomes] | Vou criar uma: Panfleto, pra quem chega por um folheto. Escolho o ícone, a cor e clico em Adicionar. |
| Menu da linha "Panfleto": "Editar"; troca o nome para "Panfleto de bairro" e confirma; toast "Origem atualizada!". | Pelo menu de cada origem dá pra editar o nome, o ícone e a cor. |
| Menu da linha "Panfleto de bairro": "Excluir"; toast "Origem removida!"; a lista volta às quatro origens. [BACKEND: `POST`, `PATCH` e `DELETE` em `customer_origins`] | Criei essa só pra mostrar, então excluo, e ela sai da lista na hora. |
| Fecha a janela; a câmera para no cartão "Origens". | Marcando a origem em cada cliente, você enxerga de onde vêm os seus pedidos. |

### cap10 · Atalhos e aparência (vinheta: PREFERÊNCIAS)

| Tela | Fala |
| --- | --- |
| Clique na aba "Atalhos": título "Atalhos de Teclado" ("Use atalhos para acessar funcionalidades rapidamente") e o interruptor "Atalhos de Teclado" ligado ("Atalhos estão ativados"). | E agora o gosto de cada pessoa: atalhos e aparência. Na aba Atalhos, o interruptor liga os atalhos de teclado. |
| Zoom na lista, grupos "Navegação" e "Geral"; destaque em "Shift + D" ("Dashboard"), "Shift + C" ("Clientes e Fornecedores") e "Shift + S" ("Configurações"), sem pressionar as teclas. | Com ele ligado, é só segurar o Shift e apertar uma letra pra ir direto pra tela: Shift mais D abre o Dashboard, Shift mais C, os Clientes e Fornecedores, e Shift mais S, as Configurações. |
| Zoom na caixa "Dicas" ("Use Shift + letra para navegação rápida"). | Uma dica: os atalhos ficam em espera enquanto você digita num campo de texto, então não atrapalham. |
| Clique na aba "Aparência": cartão "Aparência" ("Personalize a interface visual do sistema"); zoom em "Estilo de Navegação (Desktop)" com "Menu Lateral" (selecionado) e "Menu Superior". | Na aba Aparência, o primeiro bloco é o Estilo de Navegação. Hoje a gente está no Menu Lateral. |
| Clique em "Menu Superior": a barra vai para o alto da tela e a câmera acompanha; depois clique em "Menu Lateral" e o layout volta. [TESTAR: o layout se refaz por alguns segundos; esperar antes de voltar; `profiles.navigation_style` volta a `sidebar`] | Se você preferir o Menu Superior, é só clicar, e a barra vai pro alto da tela. Eu volto pro lateral. |
| Zoom em "Menu (lateral e superior)": clique em "Seguir o tema" e depois em "Escuro (recomendado)". | Logo abaixo, a cor do menu: Escuro, que é a recomendada, ou Seguir o tema. |
| Zoom em "Tema do Sistema": clique em "Tema Escuro" (a tela escurece) e depois em "Tema Claro". | E o tema do sistema, claro ou escuro. Cada pessoa escolhe o seu, e vale só pra quem escolheu. Eu fico no claro. |

### cap11 · Onde ficam as integrações (vinheta: INTEGRAÇÕES)

| Tela | Fala |
| --- | --- |
| Clique na aba "Integrações": subabas "WhatsApp", "Cobranças (Asaas)", "Impressora fiscal" e "API Pública" (1.38.19: quatro); a subaba "WhatsApp" aberta, na tela de conexão (sem conectar nada). [BACKEND: `company_whatsapp_settings` e `whatsapp_connections` sem seed devolvem lista vazia; nada de QR Code] | Por fim, a aba Integrações, onde ficam as ligações com outros serviços. São quatro subabas. Na primeira, o WhatsApp, é onde a empresa conecta o número pra falar com o cliente. |
| Clique em "Cobranças (Asaas)": cartão "Recebimentos (Asaas)" com o selo verde "Ativo"; zoom nos botões "Configurações" e "Simulador" (sem clicar). [BACKEND: função `tenant-asaas-card-fees` sem handler; a subaba a chama ao abrir (sem ela o cartão mostra "Taxas de referência"); entra também no T19] | Em Cobranças, a Asaas é a conta onde os seus clientes pagam por Pix, boleto e cartão. O cartão Recebimentos mostra que ela está ativa. |
| Zoom nas subabas "Impressora fiscal" e "API Pública" (só os nomes, sem clicar: a "Impressora fiscal" consulta o aplicativo local; a câmera só passa). [Não abrir: chama `api-key-manager`, sem handler] | A Impressora fiscal liga a impressora do computador à Dominex. E a API Pública, pra quem quer ligar a Dominex a outros sistemas. |
| As quatro subabas em destaque. | WhatsApp e Cobranças dependem dos módulos contratados, e cada uma tem o seu tutorial. |

### cap12 · Termos, cópia dos dados e Zona de Perigo (vinheta: SEGURANÇA)

| Tela | Fala |
| --- | --- |
| Volta à aba "Empresa" e rola até o fim: cartões "Documentos Legais", "Exportar meus dados" e "Zona de Perigo". | E, no fim da aba Empresa, o que é de segurança. Primeiro, os Documentos Legais. |
| Em "Documentos Legais" ("Consulte e baixe os termos que regem o uso do Dominex"): clique em "Ver termos de uso"; abre a janela com os termos; rola um pouco; zoom em "Baixar PDF" (sem clicar); clique em "Fechar"; zoom em "Aceito em {data}" (verde). [TESTAR: a data vem de `terms_accepted_at` do seed e bate com o relógio do navegador congelado] | Aqui você consulta os termos de uso e, se quiser, baixa em PDF. Embaixo fica a data em que você aceitou. |
| No cartão "Exportar meus dados" ("Baixe uma planilha do Excel com os dados da sua empresa..."): clique em "Exportar dados"; janela com as caixas por grupo; zoom em "Marcar tudo", "Limpar seleção" e no aviso sobre "Movimentações de Estoque" e "Ponto" desmarcados; clique em "Cancelar". [Nunca exportar: o gravador não captura download] | O Exportar meus dados baixa uma planilha do Excel com clientes, equipamentos, ordens de serviço, financeiro e mais. Você escolhe os grupos que quer, e serve de cópia de segurança. Aqui eu só mostro e cancelo. |
| Rola até a "Zona de Perigo" (cartão vermelho: "Ações irreversíveis. Revise cuidadosamente antes de confirmar."); clique em "Zerar Sistema": janela com os grupos "Operacional", "Comercial (CRM)", "Financeiro", "RH e Inventário" e "PDV e Loja", "Serão mantidos:" e o campo "Nome da empresa"; clique em "Cancelar". [Nunca executar nem digitar o nome da empresa] | Por último, a Zona de Perigo. O Zerar Sistema apaga os dados operacionais que você escolher, e mantém os dados da empresa e os usuários. Se um dia precisar recomeçar, o caminho é baixar os dados em Exportar meus dados e só então usar o Zerar Sistema, que pede o nome da empresa pra confirmar, porque não tem volta. Eu cancelo, claro. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a aba Empresa com o logo e os dados preenchidos; o sistema em dourado com o White Label; a aba Regional. | Pronto! Recapitulando: a gente colocou o logo, os dados e o endereço da empresa, e viu como a sua marca aparece no sistema, nos QR Codes e nos relatórios, com o White Label. |
| Montagem rápida: Usabilidade com os interruptores, as Origens, Atalhos, Aparência e Integrações. | Também passou pelos padrões de idioma, moeda e fuso, pelas preferências de Usabilidade, pelas origens dos clientes, pelos atalhos e pela aparência, e conheceu onde ficam as integrações e a Zona de Perigo. |
| A aba Empresa pronta, com o selo "Salvo". | E tudo isso a Dominex salvou sozinha. Qualquer ajuste, você volta aqui quando quiser. |
| Cartão "Próximo: Usuários, cargos e permissões"; cartela final. | No próximo tutorial, a gente monta a equipe: quem entra no sistema e o que cada pessoa pode fazer. Até lá! |
