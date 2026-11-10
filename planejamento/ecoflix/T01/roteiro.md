# Roteiro T1 · Sua conta e sua empresa

Roteiro pronto para o ensaio gravado e, depois da revisão geral, para a voz (sem etapa de aprovação, como na Domiflix). Coluna
Fala = texto da narração (voz Kaik Barreto, ElevenLabs), na grafia da legenda, uma linha da tabela = uma linha da fala; a grafia
de pronúncia vai em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas
como no código da 1.59.154 (`T01/inventario.md`). Dados da Recicla Vale Metais (`plano.md` → "Mundo"); tudo fictício.

- **Título:** Sua conta e sua empresa
- **Antes:** Bem-vindo ao EcoSistema (T0)
- **Próximo:** Usuários e permissões (T2)
- **Vinhetas (áreas):** CONTA · ACESSO · EMPRESA · PEDIDOS · COMPROVANTE · USABILIDADE · PAGAMENTO · APARÊNCIA · SEGURANÇA ·
  RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~17 min de vídeo (2.351 palavras de fala, ~15 min de voz a 2,6 palavras/s, mais 13 vinhetas e o
  tempo das ações; a fonte pede ~18 min, a fala segue o tempo natural)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00`. Desktop, janela 1280×800, tema claro. Cada capítulo abre um navegador novo, com a
  semente indicada; caps 0 a 4 sem sessão (páginas públicas).
- Marcas: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[ZOOM: ...]` (campo crítico, a frase inteira, nunca em cima de
  outro zoom), `[ILUSTRAÇÃO: ...]` (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`; nunca tela do app).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Sua conta e sua empresa". | (sem fala) |
| [ILUSTRAÇÃO: o problema do pátio: à esquerda, um comprovante genérico só com pesos e valores, sem logo, sem nome e sem CNPJ, na mão de um fornecedor (silhueta genérica com uma carroça); na palavra "cara", entra à direita o mesmo comprovante com o logo da Recicla Vale Metais e o nome] | Oi! Neste tutorial a gente vai criar a conta da Recicla Vale Metais e deixar o EcoSistema com a cara dela. |
| (a ilustração continua: no comprovante da direita acendem "CNPJ 47.318.506/0001-07" na palavra "CNPJ" e o telefone na palavra "telefone") | Quando o fornecedor sai do pátio com o comprovante na mão, ele precisa ver ali o nome, o CNPJ e o telefone da empresa. |
| Página pública `/cadastro`, sem login: logo do EcoSistema, "Cadastro" e "Teste grátis por 7 dias · Sem compromisso · Acesso total"; a câmera desce devagar pelo formulário. | Então a gente vai do começo: criar a conta, entrar no sistema e preencher os dados da empresa. Depois, o número do pedido, a frase do comprovante e o jeito que o pátio trabalha. |
| Cartão discreto: "Antes: Bem-vindo ao EcoSistema". | Se você ainda não viu o tutorial Bem-vindo ao EcoSistema, dá uma olhada antes. [pause] Vamos criar a conta. |

### cap01 · Criar a conta (vinheta: CONTA)

| Tela | Fala |
| --- | --- |
| Capítulo novo, sem sessão: `/cadastro` como visitante do site (sem parâmetros na URL). Zoom nas etapas "Dados" e "Acesso" e na barra "Preenchimento obrigatório", em "0%". | O cadastro tem duas etapas: Dados e Acesso. E a barra Preenchimento obrigatório mostra quanto falta. |
| Clica em "Nome da Empresa*" e digita "Recicla Vale Metais"; em "Seu Nome Completo*", digita "Rafael Nogueira" (a barra sobe). | Primeiro, o nome da empresa: Recicla Vale Metais. Depois, o seu nome completo. Aqui é o Rafael Nogueira, o dono do ferro-velho. |
| Em "Email*", digita "rafael@reciclavalemetais.example"; em "Telefone*", digita "12900004410" e a máscara forma "(12) 90000-4410". | O e-mail é o que você vai usar pra entrar no sistema. E o telefone se arruma sozinho enquanto você digita. |
| Zoom no link "Recebeu um código de indicação?", sem clicar. | Se alguém te indicou o EcoSistema, o código de indicação entra aqui embaixo. |
| A câmera abre para a etapa inteira (sem campo de CNPJ). | Repara que não tem CNPJ aqui. Ele entra depois, nas Configurações, e a gente faz isso daqui a pouco. |
| Clica em "Continuar": o botão mostra "Verificando..." e abre a etapa "Acesso", com a caixa "Email de acesso: rafael@reciclavalemetais.example". [BACKEND: edge `self-register` com `check_email_only` devolve `{available: true}` para o e-mail do Rafael] | Clico em Continuar, e agora é a senha. |
| Digita `ReciclaVale#26` em "Senha*" (pontinhos; o indicador de força enche) e repete em "Confirmar Senha*". | A senha precisa de pelo menos oito caracteres, e o indicador mostra se ela está forte. Embaixo, eu repito a mesma senha pra confirmar. |
| Zoom no aviso "Ao criar sua conta, você concorda com os Termos de Uso e a Política de Privacidade.", sem clicar. | Ao criar a conta, você concorda com os Termos de Uso e a Política de Privacidade. Os dois abrem aqui, clicando no nome. |
| Clica em "Criar Conta" ("Cadastrando..."); toast "Cadastro realizado com sucesso! Redirecionando..."; o capítulo corta no toast, antes do painel. [BACKEND: edge `self-register` devolve `{success: true, requires_payment: false}` sem criar nada (a Recicla Vale já existe no mundo); o login automático (`auth.signInWithPassword`) entra com o e-mail e a senha do Rafael] | Clico em Criar Conta. Pronto, cadastro feito, e o sistema já entra sozinho. |

### cap02 · Os 7 dias de teste (vinheta: CONTA)

| Tela | Fala |
| --- | --- |
| Capítulo novo, sem sessão: `/cadastro`; o `setup` preenche a etapa "Dados" como no cap01 e clica em "Continuar" fora do vídeo. Na etapa "Acesso", zoom no cartão "Teste Grátis · Acesso Total": "7 dias grátis com acesso a todos os módulos" e "5 usuários inclusos durante o teste". | Lembra desse cartão, logo acima do botão Criar Conta? Ele resume o teste grátis. |
| [ILUSTRAÇÃO: os 7 dias de teste: uma linha do tempo com 7 casas de dia, que acendem uma a uma na palavra "sete"; em cima, ícones genéricos de módulos, todos abertos, na palavra "liberado"; embaixo, 5 bonequinhos de usuário na palavra "cinco"] | São sete dias com tudo liberado, inclusive os módulos que dependem do plano. E cabem cinco usuários durante o teste. |
| (a ilustração continua: no fim da linha do tempo, uma porta "Ativar assinatura" se abre na palavra "ativar"; depois dela, só alguns módulos seguem acesos, na palavra "plano") | No fim do teste, é só ativar a assinatura pra continuar. Daí ficam liberados os módulos do plano que a empresa contratar. |
| A câmera sobe ao subtítulo. [ZOOM: "Teste grátis por 7 dias · Sem compromisso · Acesso total", a frase inteira] | Uma dica: se você entrou por um link do nosso comercial, o teste pode ter mais dias. O que vale é o que está escrito aqui em cima. |

### cap03 · Entrar no sistema (vinheta: ACESSO)

| Tela | Fala |
| --- | --- |
| Capítulo novo, sem sessão (semente `inicio`): `/login`, "Acesse sua conta" e "Entre para continuar no EcoSistema."; a câmera fica no formulário da esquerda (o painel da direita só no plano geral). | Conta criada, agora é entrar. Essa é a tela que você vai ver todo dia. |
| Digita "rafael@reciclavalemetais.example" em "E-mail *" e `ReciclaVale#26` em "Senha *"; marca "Lembrar de mim". | Aqui vão o e-mail e a senha do cadastro. Marcando Lembrar de mim, o sistema guarda o seu e-mail pra próxima vez. |
| Zoom no botão "Entrar com Google", sem clicar. | Se o e-mail da sua conta é do Google, dá pra usar o Entrar com Google. Ele entra na conta que já existe com esse e-mail. Conta nova é sempre pelo Cadastre-se. |
| Clica em "Entrar" ("Entrando..."); abre o sistema, logado como Rafael Nogueira. [BACKEND: `auth.signInWithPassword` do Rafael; `active_sessions` sem acesso na última hora (sem a janela de outro acesso); chegada limpa, sem janela de boas-vindas nem de termos] | Clico em Entrar, e pronto, a gente está dentro. |
| A câmera desce ao rodapé do menu lateral: o card com "Rafael Nogueira", o selo "MASTER" e "Recicla Vale Metais"; embaixo, "Configurações" e "Sair". | Lá embaixo, no menu, fica o card com o seu nome e o nome da empresa. O selo Master é de quem administra a conta. |
| Clica no card: abre, acima dele, o menu com "Perfil", "Assinatura", "Tema", "Tutoriais \| EcoFlix", a ajuda e "Falar com o Suporte". | Clicando nele, abre esse menu. Em Perfil ficam a sua foto e o seu nome. |
| Clica no card "Trocar de conta", no fim do menu: ele cresce e mostra a conta ativa, "Apenas essa conta está salva. Use "+ Adicionar conta" pra incluir outra.", "Adicionar conta" e "Sair de todas as contas". [BACKEND: a sessão salva nasce do login pelo formulário; não injetar sessão neste capítulo] | E no fim do menu fica o trocador de contas. Ele guarda as contas que entram neste computador. |
| [ILUSTRAÇÃO: o trocador de contas: um computador genérico de escritório com uma pilha de até cinco cartões de conta (bonequinhos sem rosto), um aceso; na palavra "clique", o aceso troca para outro, sem cadeado de senha] | Imagina o computador do escritório, usado por mais de uma pessoa. Cada um entra com a própria conta, e a troca é com um clique, sem digitar a senha de novo. |
| De volta à tela: zoom em "Adicionar conta", sem clicar; Esc fecha o menu. | Pra incluir outra pessoa, é Adicionar conta: abre o login, e quem já estava entrado continua salvo. Cabem até cinco contas. |

### cap04 · Esqueci minha senha (vinheta: ACESSO)

| Tela | Fala |
| --- | --- |
| Capítulo novo, sem sessão (semente `inicio`): `/login`; clica em "Esqueci minha senha": "Recuperar Senha" e "Informe o email da sua conta e enviaremos um código de verificação.". | E se um dia você esquecer a senha? Na tela de login, é só clicar em Esqueci minha senha. |
| Digita "rafael@reciclavalemetais.example" em "E-mail" e clica em "Enviar Código" ("Enviando..."); toast "Se o email existir no sistema, um código será enviado. Verifique sua caixa de entrada.". [BACKEND: edge `password-reset` com `{action: 'send'}` devolve sucesso; nenhum e-mail sai] | Digito o e-mail da conta e clico em Enviar Código. |
| Passo "Verificar Código": "Digite o código de 6 dígitos enviado para rafael@reciclavalemetais.example", as seis casas vazias e "Reenviar código em 60s" contando. | O sistema manda um código de seis números pro seu e-mail. |
| [ILUSTRAÇÃO: o código pelo e-mail: uma caixa de entrada genérica, sem marca de provedor, recebe um envelope; ele abre e mostra o código 4 8 1 2 0 7; na palavra "digita", os seis números voam para seis casas iguais às da tela] | Você abre o e-mail, pega o código e digita aqui, uma casa pra cada número. |
| De volta à tela: digita "481207" nas seis casas; zoom na caixa laranja "Não recebeu? Confira também a pasta de Spam / Lixo Eletrônico do seu email" e em "Reenviar código em ...s". | Uma dica: se o código não chegar, confere também a caixa de spam. E depois de um minuto, dá pra pedir outro código. |
| Clica em "Verificar"; toast "Código verificado com sucesso!"; passo "Nova Senha" ("Defina sua nova senha. Use no mínimo 6 caracteres."). [BACKEND: `auth.verifyOtp` com `type: 'recovery'` aceita 481207 para o e-mail do Rafael] | Clico em Verificar. Código certo, agora é a senha nova. |
| Digita `PatioTaubate#26` em "Nova Senha" e em "Confirmar Nova Senha"; clica em "Alterar Senha e Entrar"; toast "Senha alterada com sucesso! Você já está logado." e o sistema abre. [BACKEND: `auth.updateUser` aceita a senha; update em `profiles.must_change_password`] | Digito a nova duas vezes e clico em Alterar Senha e Entrar. Pronto: senha trocada, e você já entra direto no sistema. |

### cap05 · Logo, ícone, nome e CNPJ (vinheta: EMPRESA)

| Tela | Fala |
| --- | --- |
| Capítulo novo, logado como Rafael (semente `inicio`: a empresa só com o nome, o e-mail do Rafael e o telefone do cadastro), na tela inicial; a câmera desce ao rodapé do menu e clica em "Configurações", logo abaixo do card com o nome. | Agora, os dados da empresa. Eles ficam em Configurações, nesse botão logo abaixo do card com o seu nome. |
| `/configuracoes`, "Configurações do Sistema": zoom nas abas "Empresa", "Usuários e Permissões", "Usabilidade", "Condições de Pagamento", "Aparência", "Integrações" e "Atalhos", sem clicar. | Lá em cima ficam as abas. Neste tutorial a gente passa por Empresa, Usabilidade, Condições de Pagamento, Aparência e Atalhos. Usuários e Permissões é o próximo tutorial. |
| Aba "Empresa", seção "Identidade Visual": clica na área "Nenhum logo enviado" ("PNG ou JPG, até 5MB") e escolhe `recicla-vale-logo.png`; toast "Logo atualizado com sucesso!"; aparecem o logo e os botões "Substituir" e "Remover". [BACKEND: storage `avatars` aceita o upload e devolve a URL pública; update em `companies.logo_url`] | Começando pela Identidade Visual. Clico aqui e escolho o logo da Recicla Vale. Ele sai nos comprovantes e nos relatórios. |
| Logo abaixo, clica no quadrado "1:1" de "Ícone da Empresa (1:1)" e escolhe `recicla-vale-icone.png`; toast "Ícone atualizado com sucesso!". [BACKEND: o mesmo upload; update em `companies.icon_url`] | Embaixo, o ícone quadrado. Ele aparece no menu recolhido quando o White Label está ligado. |
| A câmera vai à coluna da direita: o cartão "White Label" ("Personalize o sistema com sua marca"), recolhido, sem abrir. | Ao lado fica o White Label, que deixa o sistema inteiro com a marca da sua empresa. Ele depende do plano contratado, e tem um tutorial só dele. |
| Zoom em "Nome da Empresa" ("Recicla Vale Metais") e na chave "Exibir nos documentos", ligada. | O nome já veio do cadastro. E a chave do lado, Exibir nos documentos, decide se ele sai no papel. |
| Clica em "CNPJ/CPF" e digita "47318506000107"; a máscara forma "47.318.506/0001-07"; espera o fim da digitação. [ZOOM: "CNPJ/CPF" com "47.318.506/0001-07", a frase inteira] | Agora o CNPJ. Uma dica: ele não é pedido no cadastro, ele entra aqui. E vai também na nota fiscal da assinatura do EcoSistema, então confere número por número. |
| [ILUSTRAÇÃO: para onde vão os dados da empresa: no centro, um cartão "Configurações › Empresa" com logo, nome e CNPJ; na palavra "comprovante", uma seta acende até um papel de comprovante; na palavra "assinatura", outra seta acende até uma folha "Nota fiscal da assinatura", que recebe o CNPJ e um endereço ainda em branco] | O logo, o nome e o CNPJ saem no comprovante do pátio. E o CNPJ, junto com o endereço, vai na nota da assinatura. |
| De volta à tela: a câmera desce ao rodapé do cartão "Empresa", com o indicador "Salvando..." e o botão "Salvar alterações". [BACKEND: auto-save de 800 ms com update em `companies`; insert/update em `company_fiscal_config`; edges `geocode-company` e `sync-asaas-customer` sem efeito; vira `apos-cap05`] | Não precisa salvar: ele grava sozinho, logo depois que você para de digitar. Se quiser, o botão Salvar alterações, lá embaixo, grava na hora. |

### cap06 · Contato e endereço (vinheta: EMPRESA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), em Configurações › "Empresa"; a câmera desce até "Informações de Contato": "Telefone" "(12) 90000-4410" e "E-mail" "rafael@reciclavalemetais.example". | Logo abaixo ficam o contato e o endereço. O telefone e o e-mail vieram do cadastro. |
| Apaga o "E-mail" e digita "contato@reciclavalemetais.example". | Só que o e-mail do cadastro é o do Rafael. Pro comprovante, a Recicla Vale prefere o e-mail de contato da empresa. |
| Zoom nas duas chaves "Exibir nos documentos", ligadas. | Cada dado tem a sua chave Exibir nos documentos. |
| [ILUSTRAÇÃO: cadastrado × impresso: à esquerda, a ficha da empresa com o telefone e o e-mail; à direita, o comprovante com as mesmas linhas; na palavra "desligou", uma chave desliga e a linha do e-mail some só do comprovante; na palavra "cadastrado", ela pisca na ficha, que continua igual] | Desligou a chave, o dado continua cadastrado, mas some do comprovante. |
| De volta à tela, seção "Endereço": clica em "CEP" e digita "12086410"; toast "Endereço encontrado!"; "Estado" "SP - São Paulo", "Cidade" "Taubaté", "Logradouro" "Rua das Oficinas" e "Bairro" "Jardim Vale do Sol" se preenchem, e o cursor pula para "Número". [BACKEND: edge `cep-lookup` devolve `{success: true, data: {logradouro: "Rua das Oficinas", bairro: "Jardim Vale do Sol", cidade: "Taubaté", uf: "SP", codigoIbge: "3554102"}}`; o `fetch` da lista de municípios do IBGE (SP) responde por fixture] | No endereço, é só digitar o CEP. O sistema acha a rua, o bairro, a cidade e o estado sozinho. |
| Digita "1250" em "Número" e "Galpão 2" em "Complemento". | Aí eu completo o número, mil duzentos e cinquenta, e o complemento: galpão dois. |
| Zoom na nota "É este endereço que sai na nota fiscal. A Configuração Fiscal usa exatamente o que estiver aqui.". | E repara no aviso: é este endereço que sai na nota fiscal. A Configuração Fiscal usa exatamente o que estiver aqui. |
| Desce até "Prévia no comprovante": "Rua das Oficinas, 1250 - Galpão 2 - Jardim Vale do Sol - Taubaté/SP - CEP: 12086-410" e as caixas "Logradouro", "Número", "Complemento", "Bairro", "Cidade/UF" e "CEP", todas marcadas. | Mais embaixo, a Prévia no comprovante mostra o endereço do jeito que ele vai sair impresso. |
| Desmarca "Complemento": a prévia fica "Rua das Oficinas, 1250 - Jardim Vale do Sol - Taubaté/SP - CEP: 12086-410". [BACKEND: auto-save grava `companies.address`, `address_visibility_settings` (complemento falso) e o endereço em `company_fiscal_config`; vira `apos-cap06`] | E dá pra escolher pedaço por pedaço. O galpão não precisa sair no papel, então eu desmarco o Complemento, e ele some da prévia na hora. |

### cap07 · Numeração de pedidos (vinheta: PEDIDOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), em Configurações › "Empresa"; a câmera desce até "Numeração de pedidos". | Cada compra e cada venda ganha um número, e é ele que sai no comprovante. Em Numeração de pedidos, você escolhe como esse número aparece. |
| Abre "Reinício da numeração": "Nenhum (segue direto)", "Mensal (zera todo mês)" e "Anual (zera todo ano)"; fica em "Nenhum (segue direto)". | Primeiro, o Reinício da numeração. No Nenhum, o número segue direto e nunca zera. No Mensal, a contagem recomeça todo mês, e no Anual, todo ano. |
| [ILUSTRAÇÃO: o reinício da numeração: uma fila de pedidos de outubro termina no 30; na palavra "direto", a fila de cima segue em novembro com 31, 32; na palavra "Mensal", a fila de baixo recomeça em novembro com 1, 2] | Imagina que outubro terminou no pedido trinta. Seguindo direto, novembro começa no trinta e um. No Mensal, novembro recomeça do um. |
| De volta à tela, "Formato do número": a câmera passa pelos modelos "Padrão", "Barras", "Pontos", "Ano/Nº" e "Zeros", cada um com o seu exemplo. | Depois, o Formato do número. Cada modelo mostra um exemplo do lado. |
| Clica em "Barras": o campo vira "{NUM}/{MM}/{AAAA}" e o exemplo muda. [ZOOM: "Exemplo: 30/11/26", a frase inteira] | No Barras, por exemplo, entram o mês e o ano junto do número. |
| Clica em "Zeros" ("Exemplo: 0030") e depois em "Padrão" ("Exemplo: #30"); o campo volta a "#{NUM}". | No Zeros, o número ganha zeros na frente. A Recicla Vale fica no Padrão, que é o número simples, seguindo direto. |
| Zoom na chave "Numeração separada para compras e vendas" ("Cada tipo passa a ter sua própria contagem."), desligada. | Por último, a Numeração separada para compras e vendas. Ligando, cada tipo passa a ter a sua própria contagem. |
| [ILUSTRAÇÃO: contagem única × separada: em cima, uma fila só com compra 30, venda 31, compra 32, na palavra "fila só"; embaixo, na palavra "Separando", duas filas: compras 1, 2 e vendas 1] | Hoje, compra e venda dividem uma fila só de números. Separando, as compras seguem uma fila, e as vendas, outra. |
| De volta à tela: clica na chave; abre "Ativar numeração separada?" ("Compras e vendas passarão a contar separadamente. ... Os pedidos que você já fez não mudam. Deseja ativar?"); clica em "Cancelar" (a chave fica desligada). | Na hora de ligar, ele pede confirmação, porque os números novos podem parecer menores. Os pedidos que você já fez não mudam. Aqui eu deixo como está e clico em Cancelar. |

### cap08 · A frase do comprovante (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), em Configurações › "Empresa"; a câmera desce até "Comprovantes e Documentos". | Agora, a frase do comprovante. Em Comprovantes e Documentos, dá pra colocar uma frase da sua empresa. |
| Liga a chave "No comprovante", ao lado de "Frase Personalizada". | Primeiro eu ligo a chave No comprovante, pra frase sair no papel. |
| Digita na caixa "Obrigado pela parceria! Atendemos de segunda a sexta, das 7h às 17h."; o contador mostra "68/2000 caracteres" (junção: o pátio não abre no sábado; o mundo não tem caixa em sábado). | A Recicla Vale vai agradecer a parceria e avisar o horário do pátio. O contador embaixo mostra quantos caracteres já foram. |
| Zoom em "Alinhar à esquerda" ("Por padrão a frase sai centralizada. Ative para alinhar à esquerda (bom para textos longos)."), desligada. | A frase sai centralizada. Pra texto comprido, a chave Alinhar à esquerda ajuda na leitura. Essa é curta, então fica no centro. |
| [ILUSTRAÇÃO: o comprovante da Recicla Vale: um cupom genérico desenhado (não a tela do app) com o logo, "Recicla Vale Metais", "CNPJ 47.318.506/0001-07", o telefone, o e-mail e o endereço sem o galpão; na palavra "abaixo", a frase entra centralizada logo abaixo desses dados, entre duas linhas finas] | No papel, ela sai logo abaixo dos dados da empresa, entre duas linhas. |
| De volta à tela: clica em "Salvar alterações"; toast "Configurações salvas". [BACKEND: update em `companies` (`receipt_phrase`, `show_receipt_phrase`); vira `apos-cap08`] | Clico em Salvar alterações, e pronto. O comprovante já sai com a cara da Recicla Vale. No tutorial de compra e venda, você vê ele de verdade. |

### cap09 · O jeito do pátio (vinheta: USABILIDADE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), em Configurações; clica na aba "Usabilidade": "Usabilidade" e "Configure preferências gerais de usabilidade do sistema". Nenhuma chave desta aba muda no capítulo. | Agora, a aba Usabilidade. É aqui que o sistema se ajusta ao jeito do pátio trabalhar. |
| Zoom em "Nomenclatura de clientes e fornecedores" e na chave "Inverter os termos Cliente e Fornecedor", desligada (sem clicar). | Lá no alto tem a Nomenclatura de clientes e fornecedores. Tem pátio que chama de cliente quem traz sucata pra vender. Pra esses, a chave Inverter os termos Cliente e Fornecedor troca as palavras na tela. |
| Zoom na descrição "Compras, vendas, vínculos, saldos e documentos fiscais continuam com a mesma lógica.". | Muda só o nome. O cadastro, o saldo e a nota fiscal continuam iguais. A Recicla Vale usa os nomes de sempre. |
| Seção "Caixa": zoom em "Multi-Caixas" ("Cada operador abre e gerencia seu próprio caixa. Se desativado, toda a empresa compartilha um único caixa."), ligada. | Na seção Caixa, o Multi-Caixas. Ligado, cada operador abre e cuida do próprio caixa. Desligado, a empresa toda usa um caixa só. Aqui fica ligado. |
| A câmera passa por "Rastreabilidade do dinheiro físico (Cofre)", ligada, sem parar. | Logo abaixo fica o cofre, que a gente vê no tutorial do caixa. |
| "Formato do Comprovante": abre o seletor de "Computador" e mostra "Térmico (58/80mm)" e "A4 (PDF em folha)"; Esc fecha em "Térmico (58/80mm)". | No Formato do Comprovante, você escolhe o papel: o Térmico, da impressora de cupom, ou o A4, um PDF pra imprimir em folha comum. |
| A câmera mostra as linhas "Computador" e "Celular/Tablet" e a descrição "(preferência por usuário)". | Dá pra ter um no computador e outro no celular, e cada pessoa escolhe o seu. |
| Seção "Pedidos e Pagamentos": abre "Forma de Pagamento Padrão": "Dinheiro", "Pix/Transferência" e "Perguntar sempre". | Em Pedidos e Pagamentos, a Forma de Pagamento Padrão é a que já vem marcada quando você finaliza um pedido: Dinheiro, Pix ou Transferência, ou Perguntar sempre. |
| Esc fecha em "Perguntar sempre". | A Recicla Vale deixa Perguntar sempre, porque cada fornecedor recebe de um jeito. |
| Passa o mouse no ícone de ajuda de "Arredondar Pagamentos" (a dica aparece) e mostra as chaves "Na Venda" e "Na Compra", desligadas. | O Arredondar Pagamentos tira os centavos, sempre pra baixo, e você liga separado Na Venda e Na Compra. |
| [ILUSTRAÇÃO: arredondar na compra: a Dona Cida (silhueta genérica) com um saco de latinhas; a balança mostra 37 kg e o preço R$ 6,20 o quilo, e o total R$ 229,40 na palavra "quarenta"; na palavra "arredondamento", os 40 centavos se soltam e caem num cofrinho "saldo a pagar"; ela recebe R$ 229,00] | Por exemplo: a Dona Cida trouxe trinta e sete quilos de latinha, que dão duzentos e vinte e nove reais e quarenta. Com o arredondamento na compra, ela recebe duzentos e vinte e nove reais, e os quarenta centavos ficam como saldo a pagar pra ela. |
| De volta à tela: zoom em "Impureza/Tara Desconta no Valor", ligada; passa o mouse no ícone de ajuda: "Ex: Compra de 100kg com 5kg de impureza. Ativo: paga 95kg. Desativado: paga 100kg, mas estoque recebe 95kg." | Agora a mais importante: Impureza e Tara Desconta no Valor. Impureza é a sujeira que vem junto, como terra ou plástico. E tara é o peso do que não é material, como o carrinho ou a caçamba. |
| [ILUSTRAÇÃO: impureza e tara, as duas situações: uma balança com 200 kg de ferro misto e 10 kg de terra; na palavra "peso", os 10 kg saem e uma seta leva 190 kg para uma pilha "Estoque", que fica acesa nas duas metades da cena; a cena se divide em "Ligada" e "Desligada" na palavra "valor"] | Uma dica: a impureza e a tara sempre descontam do peso que entra ou sai do estoque. Essa chave decide só se elas descontam também do valor pago. |
| (a ilustração continua: o Valdir com a carroça; na metade "Ligada", "190 kg × R$ 0,75 = R$ 142,50" na palavra "ligada") | Imagina o Valdir com duzentos quilos de ferro misto, dez quilos de terra. Com a chave ligada, ele recebe por cento e noventa quilos: cento e quarenta e dois reais e cinquenta. |
| (a ilustração continua: na metade "Desligada", "200 kg × R$ 0,75 = R$ 150,00" na palavra "desligada"; o "Estoque 190 kg" pisca dos dois lados na palavra "estoque") | Com a chave desligada, ele recebe pelos duzentos quilos: cento e cinquenta reais. Nos dois casos, o estoque recebe cento e noventa quilos. A Recicla Vale deixa ligada. |
| De volta à tela: zoom em "Lucro no Comprovante" ("Exibe o lucro estimado no PDF do comprovante de venda"), desligada. | O Lucro no Comprovante mostra o lucro estimado no comprovante de venda, só pra quem tem permissão de ver o lucro. |
| A câmera abre para as opções de pedido, de "Forma de Pagamento Padrão" até "Lucro no Comprovante". | Repara: essas opções de pedido ficam gravadas no usuário que está configurando, aqui o Rafael. |
| Zoom em "Exigir cliente/fornecedor no Ticket de Pesagem" ("Quando ligado, o funcionário não consegue salvar um ticket sem escolher o cliente ou fornecedor."), desligada. | Por último, o Exigir cliente ou fornecedor no Ticket de Pesagem. Ligado, ninguém salva um ticket sem escolher com quem foi a pesagem. Esse vale pra empresa toda. |

### cap10 · Condições de pagamento (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), em Configurações; clica na aba "Condições de Pagamento": "Defina parcelamentos padrão (à vista, 30/60/90…) para agilizar vendas e compras a prazo." e "Nenhuma condição cadastrada ainda.". | Agora, as Condições de Pagamento. São os parcelamentos que a empresa mais usa, prontos pra venda e pra compra a prazo. |
| [ILUSTRAÇÃO: 30/60/90: num calendário, uma venda de cobre para a Fundição Bandeira do Vale; na palavra "três", saem dela três parcelas, que pousam em 30, 60 e 90 dias] | Imagina que a Fundição Bandeira do Vale compra cobre e paga em três vezes: trinta, sessenta e noventa dias. |
| De volta à tela: clica em "Nova condição": abre "Nova condição de pagamento" ("Defina o nome e as parcelas. A soma dos percentuais precisa ser 100%."); digita "30/60/90 dias" em "Nome *" e marca "Definir como condição padrão". | Clico em Nova condição. No nome, trinta, sessenta e noventa dias. E marco Definir como condição padrão, porque é a que a Recicla Vale mais usa. |
| Desmarca "À vista (parcela única, 0 dias, 100%)" (as linhas destravam). | Toda condição nova começa À vista. Como essa é parcelada, eu desmarco o À vista. |
| Na primeira linha, "Dias após emissão" 30 e "% do total" 33,33; clica em "Adicionar parcela" e preenche 60 e 33,33; clica de novo e preenche 90 e 33,34. | Em cada parcela vão os dias depois da emissão e quanto ela vale do total. Trinta dias, com trinta e três vírgula trinta e três por cento. Sessenta dias, com o mesmo tanto. E noventa dias, com trinta e três vírgula trinta e quatro, pra fechar a conta. |
| [ZOOM: "Soma dos percentuais" "100%", em verde, a frase inteira] | A Soma dos percentuais fica verde quando fecha cem por cento. Sem fechar os cem, o sistema não salva. |
| Clica em "Criar condição"; toast "Condição criada"; a lista mostra "30/60/90 dias" com o selo "Padrão" (estrela) e "30 / 60 / 90 dias · 3 parcelas". [BACKEND: insert em `payment_conditions` (`name`, `installments` com `seq`/`days`/`percent`, `is_default` verdadeiro, `active` verdadeiro); vira `apos-cap10`] | Clico em Criar condição. Pronto: ela entra na lista com o selo Padrão. |
| Zoom na chave da linha e nos botões "Editar" e "Excluir", sem clicar. | A chave do lado desliga a condição sem apagar. E na hora de parcelar uma venda, ela aparece no alto da lista, com a marca de padrão. |

### cap11 · Aparência e atalhos (vinheta: APARÊNCIA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`), em Configurações; clica na aba "Aparência": "Estilo de Navegação (Desktop)" com "Menu Lateral" marcado. | Na aba Aparência, você escolhe como o sistema fica na tela. |
| Clica em "Menu Superior": o menu da esquerda some e a barra aparece no topo; espera 1,5 s; clica em "Menu Lateral" e o menu volta. [BACKEND: update em `profiles.navigation_style` (vai e volta)] | O Estilo de Navegação troca o menu da esquerda por uma barra lá em cima. Isso vale só no computador. A Recicla Vale prefere o Menu Lateral. |
| Zoom em "Menu (lateral e superior)": "Escuro (recomendado)" marcado e "Seguir o tema". | O menu pode ficar sempre escuro, que é o recomendado, ou seguir o tema. |
| Em "Tema do Sistema", clica em "Tema Escuro" (o sistema escurece); espera 1,5 s; clica em "Tema Claro". | E o Tema do Sistema: claro ou escuro. Cada um escolhe o que cansa menos a vista. |
| Clica na aba "Atalhos": "Atalhos de Teclado" ligado ("Atalhos estão ativados"), a lista "Navegação" ("Dashboard" Shift+D, "Compra" Shift+C, "Venda" Shift+V, "Caixa" Shift+X...) e "Geral" ("Busca Global" "Ctrl+K"). | Agora a aba Atalhos. Cada tela principal tem um atalho: a tecla Shift e uma letra. Clicando na letra, você troca por outra. |
| Aperta Ctrl+K: abre a busca "Buscar páginas, clientes, fornecedores, materiais, funcionários..."; digita "cobre": em "Resultados da Busca", "Cobre mel", "Cobre misto" e "Fio de cobre encapado". | E o mais útil de todos: Ctrl+K. Ele abre a busca do sistema inteiro. Digito cobre, e já aparecem os materiais de cobre. |
| Esc fecha a busca. | A busca acha também clientes, fornecedores e telas. É só apertar Esc pra fechar. |

### cap12 · Senha, termos e Zona de Perigo (vinheta: SEGURANÇA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`), em Configurações › "Empresa"; a câmera desce, passando pelo fim do cartão "Empresa" e pelo "Filial", até "Segurança". | Pra fechar, a parte de baixo da aba Empresa. Em Segurança fica o Alterar Senha. |
| Clica em "Alterar Senha": abre "Alterar Senha" ("Digite sua nova senha abaixo. Certifique-se de usar uma senha forte."), com "Nova Senha" e "Confirmar Nova Senha"; clica em "Cancelar". | É o caminho de quem já está logado: a senha nova, duas vezes. O mesmo botão também fica no seu Perfil. |
| "Termos de Uso": clica em "Ver Contrato": abre "Termos de Uso e Responsabilidade"; zoom em "Aceito em ..." (a data não é lida). | Em Termos de Uso, o Ver Contrato abre os termos que você aceitou no cadastro, com a data e a hora do aceite. |
| Zoom em "Baixar PDF", sem clicar; clica em "Fechar". | Dá pra baixar em PDF, se quiser guardar uma cópia. |
| Desce até a "Zona de Perigo" (cabeçalho vermelho, "Ações irreversíveis. Revise cuidadosamente antes de confirmar."); zoom em "Zerar Sistema" e na descrição. | E no fim, a Zona de Perigo, em vermelho. Aqui fica o Zerar Sistema, que apaga os dados de operação que você escolher. |
| Clica em "Zerar Sistema": abre "Tem certeza?" ("Você está prestes a acessar a função de zerar o sistema. ..."); clica em "Sim, continuar". | Vou mostrar com calma, sem zerar nada. Primeiro, o sistema pergunta se você tem certeza. |
| Abre "Zerar Sistema - Ação Irreversível": a câmera desce devagar pela lista, "Clientes e Fornecedores", "Cadastro de Materiais", "Estoque de Materiais", "Movimentações Financeiras", "Pedidos (Vendas e Compras)", "Notas Fiscais e Config. Fiscal", todas marcadas. | Depois, ele mostra tudo o que pode ser apagado: clientes e fornecedores, materiais, estoque, o financeiro, os pedidos e as notas. Tudo já vem marcado. |
| Zoom em "Serão mantidos: Dados básicos da empresa, Usuários cadastrados, Histórico de pagamentos.". | Ficam só os dados básicos da empresa, os usuários e o histórico de pagamentos. |
| [ZOOM: "Esta ação NÃO PODE ser desfeita!" e "PARA CONFIRMAR, DIGITE O NOME DA EMPRESA:" com "Recicla Vale Metais" e o campo "Nome da empresa" vazio, a frase inteira] | Uma dica: zerar não tem volta. Pra confirmar, o sistema pede o nome da empresa digitado. |
| Clica em "Cancelar" sem digitar nada (o "Sim, Zerar Sistema" segue travado). [BACKEND: as RPCs `reset_company_audit_start` e `reset_company_step` nunca são chamadas] | Aqui a gente só olhou. Cancelar, e está tudo como estava. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cadastro ("Criar Conta") e o login ("Entrar"), trechos dos caps 1 e 3. | Pronto! Recapitulando: a gente criou a conta da Recicla Vale, entrou no sistema e viu o trocador de contas e o Esqueci minha senha. |
| Montagem: "Identidade Visual" com o logo e o CNPJ; o endereço com a "Prévia no comprovante" (caps 5 e 6). | Nas Configurações, colocou o logo, o ícone e o CNPJ, e preencheu o contato e o endereço, escolhendo o que sai no comprovante. |
| Montagem: "Numeração de pedidos" e a "Frase Personalizada" (caps 7 e 8). | Viu como o número do pedido aparece e pôs a frase da Recicla Vale no comprovante. |
| Montagem: "Impureza/Tara Desconta no Valor" e a lista com "30/60/90 dias" e "Padrão" (caps 9 e 10). | Conferiu a Usabilidade, com a impureza e a tara, e criou a condição trinta, sessenta e noventa dias como padrão. |
| Montagem: "Aparência", a busca do Ctrl+K e a "Zona de Perigo" (caps 11 e 12). | E passou pela aparência, pelos atalhos, pelos termos, pela senha e pela Zona de Perigo. |
| Cartão "Próximo: Usuários e permissões"; cartela final. | No próximo tutorial, a gente decide quem entra no sistema e o que cada um pode ver. Até lá! |
