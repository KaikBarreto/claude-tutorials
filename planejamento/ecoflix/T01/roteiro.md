# Roteiro T1 · Sua conta e sua empresa

Roteiro pronto para o ensaio gravado e, depois da revisão geral, para a voz (sem etapa de aprovação, como na Domiflix). Coluna
Fala = texto da narração (voz Kaik Barreto, ElevenLabs), na grafia da legenda, uma linha da tabela = uma linha da fala; a grafia
de pronúncia vai em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas
como no código do 1.60.18 (`T01/inventario.md`). Dados da Recicla Vale Metais (`plano.md` → "Mundo"); tudo fictício.

- **Título:** Sua conta e sua empresa
- **Antes:** Bem-vindo ao EcoSistema (T0)
- **Próximo:** Usuários e permissões (T2)
- **Vinhetas (áreas):** CONTA · ACESSO · EMPRESA · PEDIDOS · COMPROVANTE · USABILIDADE · PAGAMENTO · APARÊNCIA · SEGURANÇA ·
  RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~27 min de vídeo (3.348 palavras de fala, ~21,5 min de voz a 2,6 palavras/s, mais 15 vinhetas e o
  tempo das ações; a fonte pedia ~18 min: o Kaik pediu cobertura completa e aula única, 19/11)
- **Revisão 1.60.18 (20/11/2026):** 16 capítulos. **Capítulos novos:** 10 "O comprovante do seu jeito" e 11 "Ticket, idioma e
  guia". **Renumerados:** os antigos 10 (Condições), 11 (Aparência e atalhos), 12 (Senha, termos e Zona de Perigo) e 13
  (Recapitulando) viram 12, 13, 14 e 15. A aba Usabilidade passa a ser lida na ordem da tela: cap 9 até "Lucro no
  Comprovante", cap 10 do "Mostrar só peso líquido" ao "Estilo do comprovante térmico", cap 11 do "Exigir
  cliente/fornecedor" ao "Guia de configuração".
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00`. Desktop, janela 1600×900 (16:9), tema claro. Cada capítulo abre um navegador novo, com a
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
| Clica em "Continuar": o botão mostra "Verificando..." e abre a etapa "Acesso", com a caixa "Email de acesso: rafael@reciclavalemetais.example". Se o e-mail já existisse, o campo mostraria "Este email já está em uso. Faça login ou use outro email." (não filmado). [BACKEND: edge `self-register` com `check_email_only` devolve `{available: true}` para o e-mail do Rafael; o corpo traz também `acquisition_attribution`, que o falso aceita] | Clico em Continuar. Se esse e-mail já tivesse conta, o sistema avisaria que ele já está em uso e pediria pra você fazer login. Como é novo, a gente segue pra senha. |
| Digita a senha do ambiente em "Senha*" (pontinhos; precisa ter 8 caracteres, número, minúscula, maiúscula e especial, como `ReciclaVale#26`). Zoom na lista sob o campo: "Senha forte. Deve conter:" com os cinco itens marcados, de "Pelo menos 8 caracteres" a "Pelo menos 1 caractere especial". [ZOOM: a lista inteira]. Repete a senha em "Confirmar Senha*". | A senha precisa de pelo menos oito caracteres. Embaixo, o sistema vai marcando o que ela já tem: número, letra minúscula, letra maiúscula e um caractere especial. Com tudo marcado, aparece Senha forte. Depois eu repito a mesma senha pra confirmar. |
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
| A câmera desce ao rodapé do menu lateral: o card com "Rafael Nogueira" e "Recicla Vale Metais"; embaixo, "Configurações" e "Sair". (O selo "MASTER" não aparece no card: defeito do app, a fala não o cita.) | Lá embaixo, no menu, fica o card com o seu nome e o nome da empresa. |
| Clica no card: abre, acima dele, o menu com "Meu Perfil", "Assinatura", "Tema", "Tutoriais \| EcoFlix", "Central de Ajuda" e "Falar com o Suporte"; o mouse passa por cada item, sem clicar. | Clicando nele, abre esse menu. Em Meu Perfil ficam a sua foto e o seu nome. Logo abaixo, a Assinatura, o Tema, os tutoriais da EcoFlix, a Central de Ajuda e o Falar com o Suporte. |
| Clica no card "Trocar de conta", no fim do menu: ele cresce e mostra a conta ativa, "Apenas essa conta está salva. Use "+ Adicionar conta" pra incluir outra.", "Adicionar conta" e "Sair de todas as contas". [BACKEND: a sessão salva nasce do login pelo formulário; não injetar sessão neste capítulo] | E no fim do menu fica o trocador de contas. Ele guarda as contas que entram neste computador. |
| [ILUSTRAÇÃO: o trocador de contas: um computador genérico de escritório com uma pilha de até cinco cartões de conta (bonequinhos sem rosto), um aceso; na palavra "clique", o aceso troca para outro, sem cadeado de senha] | Imagina o computador do escritório, usado por mais de uma pessoa. Cada um entra com a própria conta, e a troca é com um clique, sem digitar a senha de novo. |
| De volta à tela: zoom em "Adicionar conta", sem clicar. | Pra incluir outra pessoa, é Adicionar conta: abre o login, e quem já estava entrado continua salvo. Cabem até cinco contas. |
| Zoom no ícone "Sair desta conta", ao lado do nome da conta ativa, e em "Sair de todas as contas", sem clicar; Esc fecha o menu. | Pra tirar uma conta deste computador, é o Sair desta conta, no ícone ao lado do seu nome. E o Sair de todas as contas limpa a lista inteira, bom pra um computador que vai mudar de mão. |

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
| `/configuracoes`, "Configurações do Sistema": zoom nas abas "Empresa", "Usuários e Permissões", "Usabilidade", "Condições de Pagamento", "Aparência", "Integrações" e "Atalhos", sem clicar (a aba "Integrações" só passa: é o tutorial da balança e da impressora). | Lá em cima ficam as abas. Neste tutorial a gente passa por Empresa, Usabilidade, Condições de Pagamento, Aparência e Atalhos. Usuários e Permissões é o próximo tutorial, e Integrações é o da balança e da impressora. |
| Aba "Empresa", seção "Identidade Visual": clica na área "Nenhum logo enviado" ("PNG ou JPG, até 5MB") e escolhe `recicla-vale-logo.png`; toast "Logo atualizado com sucesso!"; aparecem o logo e os botões "Substituir" e "Remover" (o mouse passa por eles, sem clicar). [BACKEND: storage `avatars` aceita o upload e devolve a URL pública; update em `companies.logo_url`] | Começando pela Identidade Visual. Clico aqui e escolho o logo da Recicla Vale. Ele sai nos comprovantes e nos relatórios. Depois de enviado, o Substituir troca o arquivo, e o Remover tira o logo. |
| Logo abaixo, clica no quadrado "1:1" de "Ícone da Empresa (1:1)" e escolhe `recicla-vale-icone.png`; toast "Ícone atualizado com sucesso!". [BACKEND: o mesmo upload; update em `companies.icon_url`] | Embaixo, o ícone quadrado. Ele aparece no menu recolhido quando o White Label está ligado. |
| A câmera vai à coluna da direita: o cartão "White Label" ("Personalize o sistema com sua marca"), recolhido, sem abrir. | Ao lado fica o White Label, que deixa o sistema inteiro com a marca da sua empresa. Ele depende do plano contratado, e tem um tutorial só dele. |
| Zoom em "Nome da Empresa" ("Recicla Vale Metais") e na chave "Exibir nos documentos", ligada; o mouse desce à mesma chave no "CNPJ/CPF", também ligada. | O nome já veio do cadastro. E a chave do lado, Exibir nos documentos, decide se ele sai no papel. Em conta nova, ela já vem ligada, e a do CNPJ também. |
| Clica em "CNPJ/CPF" e digita "47318506000107"; a máscara forma "47.318.506/0001-07"; espera o fim da digitação. [ZOOM: "CNPJ/CPF" com "47.318.506/0001-07", a frase inteira] | Agora o CNPJ. Uma dica: ele não é pedido no cadastro, ele entra aqui. E vai também na nota fiscal da assinatura do EcoSistema, então confere número por número. |
| [ILUSTRAÇÃO: para onde vão os dados da empresa: no centro, um cartão "Configurações › Empresa" com logo, nome e CNPJ; na palavra "comprovante", uma seta acende até um papel de comprovante; na palavra "assinatura", outra seta acende até uma folha "Nota fiscal da assinatura", que recebe o CNPJ e um endereço ainda em branco] | O logo, o nome e o CNPJ saem no comprovante do pátio. E o CNPJ, junto com o endereço, vai na nota da assinatura. |
| De volta à tela: a câmera desce ao rodapé do cartão "Empresa", com o indicador "Salvando..." e o botão "Salvar alterações". [BACKEND: auto-save de 800 ms com update em `companies`; insert/update em `company_fiscal_config`; edges `geocode-company` e `sync-asaas-customer` sem efeito; vira `apos-cap05`] | Não precisa salvar: ele grava sozinho, logo depois que você para de digitar. Se quiser, o botão Salvar alterações, lá embaixo, grava na hora. |

### cap06 · Contato e endereço (vinheta: EMPRESA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), em Configurações › "Empresa"; a câmera desce até "Informações de Contato": "Telefone" "(12) 90000-4410" e "E-mail" "rafael@reciclavalemetais.example". | Logo abaixo ficam o contato e o endereço. O telefone e o e-mail vieram do cadastro. |
| Apaga o "E-mail" e digita "contato@reciclavalemetais.example". | Só que o e-mail do cadastro é o do Rafael. Pro comprovante, a Recicla Vale prefere o e-mail de contato da empresa. |
| Zoom nas duas chaves "Exibir nos documentos" do contato, ligadas (e, mais abaixo, a do endereço, também ligada). | Cada dado tem a sua chave Exibir nos documentos: nome, CNPJ, telefone, e-mail e endereço. Todas já começam ligadas, então o comprovante sai completo sem você mexer em nada. |
| [ILUSTRAÇÃO: cadastrado × impresso: à esquerda, a ficha da empresa com o telefone e o e-mail; à direita, o comprovante com as mesmas linhas; na palavra "desligou", uma chave desliga e a linha do e-mail some só do comprovante; na palavra "cadastrado", ela pisca na ficha, que continua igual] | Desligou a chave, o dado continua cadastrado, mas some do comprovante. |
| De volta à tela, seção "Endereço": clica em "CEP" e digita "12086410"; toast "Endereço encontrado!"; "Estado" "SP - São Paulo", "Cidade" "Taubaté", "Logradouro" "Rua das Oficinas" e "Bairro" "Parque Industrial" se preenchem, e o cursor pula para "Número". (Cidade digitada à mão: toast "Escolha a cidade na lista para gravar o código do IBGE — sem ele o endereço não vale na nota fiscal."; não filmado.) [BACKEND: edge `cep-lookup` devolve `{success: true, data: {logradouro: "Rua das Oficinas", bairro: "Parque Industrial", cidade: "Taubaté", uf: "SP", codigoIbge: "3554102"}}`; o `fetch` da lista de municípios do IBGE (SP) responde por fixture] | No endereço, é só digitar o CEP. O sistema acha a rua, o bairro, a cidade e o estado sozinho. Se o CEP não for achado e você digitar a cidade à mão, o sistema avisa pra escolher a cidade na lista, porque sem o código dela o endereço não vale na nota fiscal. |
| Digita "1250" em "Número" e "Galpão 2" em "Complemento". | Aí eu completo o número, mil duzentos e cinquenta, e o complemento: galpão dois. |
| Zoom na nota "É este endereço que sai na nota fiscal. A Configuração Fiscal usa exatamente o que estiver aqui.". | E repara no aviso: é este endereço que sai na nota fiscal. A Configuração Fiscal usa exatamente o que estiver aqui. |
| Desce até "Prévia no comprovante": "Rua das Oficinas, 1250 - Galpão 2 - Parque Industrial - Taubaté/SP - CEP: 12086-410" e as caixas "Logradouro", "Número", "Complemento", "Bairro", "Cidade/UF" e "CEP", todas marcadas. | Mais embaixo, a Prévia no comprovante mostra o endereço do jeito que ele vai sair impresso. |
| Desmarca "Complemento": a prévia fica "Rua das Oficinas, 1250 - Parque Industrial - Taubaté/SP - CEP: 12086-410". [BACKEND: auto-save grava `companies.address`, `address_visibility_settings` (complemento falso) e o endereço em `company_fiscal_config`; vira `apos-cap06`] | E dá pra escolher pedaço por pedaço. O galpão não precisa sair no papel, então eu desmarco o Complemento, e ele some da prévia na hora. |
| Sobe ao título "Endereço da empresa" e clica em "2º endereço": abre "Segundo endereço", com "Endereço (texto livre)" e a chave "Mostrar no comprovante junto do endereço principal", desligada. | Se a empresa tem outro endereço, como um depósito, o botão Segundo endereço abre um campo de texto livre. E a chave decide se ele sai no comprovante junto do principal. |
| Clica em "Cancelar" (nada digitado; o botão volta a "2º endereço"). | A Recicla Vale só tem um pátio, então eu cancelo. |
| Desce até "Fuso horário" ("Brasília (UTC−3) — maior parte do país", preenchido pelo estado) e o texto "É a hora que vale no seu ponto eletrônico: a que aparece em cada batida e a que decide em que dia ela entra. Preenchemos pelo seu estado; só mexa se a sua cidade tiver fuso diferente." | Por último, o Fuso horário. Ele vem preenchido pelo estado e é a hora que vale no ponto eletrônico dos funcionários. Só mexe se a sua cidade tiver um fuso diferente. |

### cap07 · Numeração de pedidos (vinheta: PEDIDOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), em Configurações › "Empresa"; a câmera desce até "Numeração de pedidos". | Cada compra e cada venda ganha um número, e é ele que sai no comprovante. Em Numeração de pedidos, você escolhe como esse número aparece. |
| Abre "Reinício da numeração": "Nenhum (segue direto)", "Mensal (zera todo mês)" e "Anual (zera todo ano)"; fica em "Nenhum (segue direto)". | Primeiro, o Reinício da numeração. No Nenhum, o número segue direto e nunca zera. No Mensal, a contagem recomeça todo mês, e no Anual, todo ano. |
| [ILUSTRAÇÃO: o reinício da numeração: uma fila de pedidos de outubro termina no 30; na palavra "direto", a fila de cima segue em novembro com 31, 32; na palavra "Mensal", a fila de baixo recomeça em novembro com 1, 2] | Imagina que outubro terminou no pedido trinta. Seguindo direto, novembro começa no trinta e um. No Mensal, novembro recomeça do um. |
| De volta à tela, "Formato do número": a câmera passa pelos modelos "Padrão", "Barras", "Pontos", "Ano/Nº" e "Zeros", cada um com o seu exemplo. | Depois, o Formato do número. Cada modelo mostra um exemplo do lado. |
| Clica em "Barras": o campo vira "{NUM}/{MM}/{AAAA}" e o exemplo muda. [ZOOM: "Exemplo: 30/11/26", a frase inteira] | No Barras, por exemplo, entram o mês e o ano junto do número. |
| Clica em "Zeros" ("Exemplo: 0030"); o mouse passa por "Pontos" e "Ano/Nº"; clica em "Padrão" ("Exemplo: #30"); o campo volta a "#{NUM}". | No Zeros, o número ganha zeros na frente. Tem também o Pontos e o Ano Número, na mesma ideia. A Recicla Vale fica no Padrão, que é o número simples, seguindo direto. |
| Zoom em "Variáveis disponíveis:" com `{NUM}`, `{NUM:4}`, `{MM}`, `{AAAA}`, `{AA}` e `{DD}` (a tela diz que `{AAAA}` sai com 2 dígitos: a fala só diz "o ano"). | Se nenhum modelo servir, dá pra montar o seu. Essas são as peças: o número do pedido, o mês, o ano e o dia. |
| No campo do formato, apaga e digita `RV-{NUM:4}`: "Exemplo: RV-0030". | Por exemplo, as letras da empresa na frente e o número com quatro casas. O exemplo embaixo já mostra como fica. |
| Troca por `RV-` (sem `{NUM}`): aparece em vermelho "Seu formato não tem {NUM} ..."; clica em "Padrão" e volta a "#{NUM}" ("Exemplo: #30"). | Só não pode faltar o número do pedido. Sem ele, o sistema avisa e não salva, porque todo pedido ficaria igual. Volto pro Padrão. |
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
| Zoom em "Nomenclatura de clientes e fornecedores" e na chave "Inverter os termos Cliente e Fornecedor", desligada (sem clicar; se ligasse, abriria a janela "Inverter Cliente e Fornecedor?", que o roteiro não filma). | Lá no alto tem a Nomenclatura de clientes e fornecedores. Tem pátio que chama de cliente quem traz sucata pra vender. Pra esses, a chave Inverter os termos Cliente e Fornecedor troca as palavras na tela. Ao ligar, o sistema ainda pede uma confirmação antes. |
| Zoom na descrição "Compras, vendas, vínculos, saldos e documentos fiscais continuam com a mesma lógica.". | Muda só o nome. O cadastro, o saldo e a nota fiscal continuam iguais. A Recicla Vale usa os nomes de sempre. |
| Seção "Caixa": zoom em "Multi-Caixas" ("Cada operador abre e gerencia seu próprio caixa. Se desativado, toda a empresa compartilha um único caixa."), ligada. | Na seção Caixa, o Multi-Caixas. Ligado, cada operador abre e cuida do próprio caixa. Desligado, a empresa toda usa um caixa só. Aqui fica ligado. |
| A câmera passa por "Rastreabilidade do dinheiro físico (Cofre)", ligada, sem parar. | Logo abaixo fica o cofre, que a gente vê no tutorial do caixa. |
| "Formato do Comprovante": abre o seletor de "Computador" e mostra "Térmico (58/80mm)" e "A4 (PDF em folha)"; Esc fecha em "Térmico (58/80mm)". | No Formato do Comprovante, você escolhe o papel: o Térmico, da impressora de cupom, ou o A4, um PDF pra imprimir em folha comum. |
| A câmera mostra as linhas "Computador" e "Celular/Tablet" e a descrição "(preferência por usuário)". | Dá pra ter um no computador e outro no celular, e cada pessoa escolhe o seu. |
| Seção "Pedidos e Pagamentos": o mouse passa por "Mostrar jogos nos pedidos" ("Exibe “300 un / 25 jogos” em compras, vendas, tíquetes de pesagem e comprovantes. Não altera estoque, preço ou quantidade gravada."); abre "Forma de Pagamento Padrão": "Dinheiro", "Pix/Transferência" e "Perguntar sempre". | Em Pedidos e Pagamentos, a primeira opção, Mostrar jogos nos pedidos, mostra a quantidade também em jogos, sem mexer em estoque nem em preço. A Forma de Pagamento Padrão é a que já vem marcada quando você finaliza um pedido: Dinheiro, Pix ou Transferência, ou Perguntar sempre. |
| Esc fecha em "Perguntar sempre". | A Recicla Vale deixa Perguntar sempre, porque cada fornecedor recebe de um jeito. |
| Zoom em "Permitir Edição de Itens" ("Editar peso, impureza/tara e valor de materiais já incluídos"), ligada; passa o mouse na dica ("Ex: Adicionou 100kg de alumínio e percebeu que era 95kg? ..."). | O Permitir Edição de Itens deixa corrigir um material que já entrou no pedido. Pesou cem quilos e eram noventa e cinco? É só clicar no item e arrumar, sem tirar e colocar de novo. |
| Passa o mouse no ícone de ajuda de "Arredondar Pagamentos" (a dica aparece) e mostra as chaves "Na Venda" e "Na Compra", desligadas. | O Arredondar Pagamentos tira os centavos, sempre pra baixo, e você liga separado Na Venda e Na Compra. |
| [ILUSTRAÇÃO: arredondar na compra: a Dona Cida (silhueta genérica) com um saco de latinhas; a balança mostra 37 kg e o preço R$ 6,20 o quilo, e o total R$ 229,40 na palavra "quarenta"; na palavra "arredondamento", os 40 centavos se soltam e caem num cofrinho "saldo a pagar"; ela recebe R$ 229,00] | Por exemplo: a Dona Cida trouxe trinta e sete quilos de latinha, que dão duzentos e vinte e nove reais e quarenta. Com o arredondamento na compra, ela recebe duzentos e vinte e nove reais, e os quarenta centavos ficam como saldo a pagar pra ela. |
| A câmera passa por "Múltiplas Tabelas de Preço" ("Permite criar e gerenciar múltiplas tabelas de preço vinculadas"), ligada, sem parar. | Logo abaixo, as Múltiplas Tabelas de Preço, que a gente vê no tutorial de materiais. |
| De volta à tela: zoom em "Impureza/Tara Desconta no Valor", ligada; passa o mouse no ícone de ajuda: "Ex: Compra de 100kg com 5kg de impureza. Ativo: paga 95kg. Desativado: paga 100kg, mas estoque recebe 95kg." | Agora a mais importante: Impureza e Tara Desconta no Valor. Impureza é a sujeira que vem junto, como terra ou plástico. E tara é o peso do que não é material, como o carrinho ou a caçamba. |
| [ILUSTRAÇÃO: impureza e tara, as duas situações: uma balança com 200 kg de ferro misto e 10 kg de terra; na palavra "peso", os 10 kg saem e uma seta leva 190 kg para uma pilha "Estoque", que fica acesa nas duas metades da cena; a cena se divide em "Ligada" e "Desligada" na palavra "valor"] | Uma dica: a impureza e a tara sempre descontam do peso que entra ou sai do estoque. Essa chave decide só se elas descontam também do valor pago. |
| (a ilustração continua: o Valdir com a carroça; na metade "Ligada", "190 kg × R$ 0,75 = R$ 142,50" na palavra "ligada") | Imagina o Valdir com duzentos quilos de ferro misto, dez quilos de terra. Com a chave ligada, ele recebe por cento e noventa quilos: cento e quarenta e dois reais e cinquenta. |
| (a ilustração continua: na metade "Desligada", "200 kg × R$ 0,75 = R$ 150,00" na palavra "desligada"; o "Estoque 190 kg" pisca dos dois lados na palavra "estoque") | Com a chave desligada, ele recebe pelos duzentos quilos: cento e cinquenta reais. Nos dois casos, o estoque recebe cento e noventa quilos. A Recicla Vale deixa ligada. |
| De volta à tela: zoom em "Lucro no Comprovante" ("Exibe o lucro estimado no PDF do comprovante de venda"), desligada. | O Lucro no Comprovante mostra o lucro estimado no comprovante de venda, só pra quem tem permissão de ver o lucro. |
| A câmera abre para as opções de pedido, de "Forma de Pagamento Padrão" até "Lucro no Comprovante". | Repara: essas opções de pedido ficam gravadas no usuário que está configurando, aqui o Rafael. |

### cap10 · O comprovante do seu jeito (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), em Configurações; clica na aba "Usabilidade" e desce até "Pedidos e Pagamentos", em "Mostrar só peso líquido". Nada fica mudado no fim: as assinaturas voltam a desligadas e o estilo volta a "Compacto". | Ainda na Usabilidade, três ajustes mudam o papel que o fornecedor leva. |
| Zoom em "Mostrar só peso líquido" ("Oculta a tara nas notinhas e na tabela de materiais; mostra apenas o peso líquido (bruto − tara)."), desligada; passa o mouse na dica ("Ex: comprou 100kg com 5kg de tara? ... a notinha mostra direto 95kg (líquido)."). | O primeiro é o Mostrar só peso líquido. Ligado, o comprovante esconde a tara e mostra só o peso líquido. Por exemplo: comprou cem quilos com cinco de tara, e a notinha mostra direto noventa e cinco. Desligado, ela mostra os cem quilos e a tara separada. |
| Zoom em "Assinaturas no comprovante" ("Linhas para assinar no rodapé. Escolha quem assina: o operador, o cliente/fornecedor ou os dois. No ticket de pesagem, o operador aparece como Empresa."); liga a chave: toast "Assinaturas ativadas no comprovante" e aparece "Quem assina", em "Operador e cliente/fornecedor". [BACKEND: coluna `companies.receipt_signature_mode` (padrão `both`) e `show_signatures_on_receipt` (falso)] | O segundo são as Assinaturas no comprovante. Ligando, o papel ganha linhas pra assinar no rodapé. |
| Abre "Quem assina": "Operador e cliente/fornecedor", "Só o cliente/fornecedor" e "Só o operador". [ZOOM: as três opções, a lista inteira] | E em Quem assina você escolhe: o operador e o cliente ou fornecedor, só o cliente ou fornecedor, ou só o operador. |
| [ILUSTRAÇÃO: o rodapé do cupom: na palavra "duas", duas linhas lado a lado, "Operador" e "Fornecedor"; na palavra "sozinha", uma delas some e a outra cresce até a largura inteira do papel] | Com as duas, cada uma fica de um lado. Sozinha, a linha ocupa a largura toda do papel, e sobra espaço pra assinar. |
| De volta à tela: escolhe "Só o cliente/fornecedor"; toast "Assinaturas do comprovante atualizadas". | Vou escolher Só o cliente ou fornecedor, que é a assinatura de quem entregou o material. Escolhi, e o sistema já grava. |
| Zoom na descrição "No ticket de pesagem, o operador aparece como Empresa.". | Isso vale no comprovante de compra e venda e no ticket de pesagem. No ticket, a linha do operador sai como Empresa. |
| A câmera desce e passa por "Marca de ticket não valorizado" e, se o módulo estiver no plano, "QR de fotos no comprovante", sem parar. 🔒 o QR depende do módulo Portal do Cliente. | Mais abaixo ficam a Marca de ticket não valorizado, que é do ticket de pesagem, e o QR de fotos no comprovante, pra quem tem o Portal do Cliente. Os dois a gente vê nos tutoriais deles. |
| Desce a "Estilo do comprovante térmico": os cartões "Compacto" (marcado) e "Nome em destaque", cada um com o desenho da linha. | O terceiro é o Estilo do comprovante térmico, que vale só pro cupom da bobina. No Compacto, o nome do material fica do lado dos valores. |
| Clica em "Nome em destaque" (o cartão fica marcado). | No Nome em destaque, o nome vai em cima, numa linha só dele. É bom pra material de nome comprido. Essa escolha vale pra empresa inteira. |
| Clica em "Compacto" de novo; sobe e desliga "Assinaturas no comprovante": toast "Assinaturas removidas do comprovante". [BACKEND: o capítulo termina como começou; a semente seguinte é a `apos-cap08`] | Aqui eu só mostrei, então volto pro Compacto e desligo as assinaturas. Quando a Recicla Vale quiser, é só voltar aqui. |

### cap11 · Ticket, idioma e guia (vinheta: USABILIDADE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), em Configurações › "Usabilidade"; a câmera desce até "Exigir cliente/fornecedor no Ticket de Pesagem". | Pra fechar a aba Usabilidade, mais um ajuste do ticket de pesagem e o fim da página. |
| Zoom em "Exigir cliente/fornecedor no Ticket de Pesagem" ("Quando ligado, o funcionário não consegue salvar um ticket sem escolher o cliente ou fornecedor."), desligada. | O Exigir cliente ou fornecedor no Ticket de Pesagem: ligado, ninguém salva um ticket sem escolher com quem foi a pesagem. Esse vale pra empresa toda. |
| A câmera passa por "Permitir forma de pagamento no ticket de pesagem", sem parar. | Logo abaixo, o Permitir forma de pagamento no ticket de pesagem, que a gente vê no tutorial do ticket. |
| Desce a "Regionalização" ("Idioma e configurações regionais") e abre "Idioma do Sistema": "Português (Brasil)", "English (USA)" e "Español (América Latina)"; Esc fecha em "Português (Brasil)". [BACKEND: `profiles.preferred_language` do Rafael em `pt-BR`] | No fim da aba, a Regionalização. O Idioma do Sistema pode ser português, inglês ou espanhol. |
| [ILUSTRAÇÃO: o idioma acompanha a pessoa: um cartão de usuário com a bandeira do Brasil; na palavra "qualquer", ele aparece igual num computador, num celular e numa maquininha, mesmo com o navegador mostrando "EN"] | Essa escolha fica gravada no seu usuário. Então ela vale em qualquer computador ou celular em que você entrar, mesmo que o navegador esteja em outro idioma. |
| Zoom em "Moeda do Sistema" ("Selecione a moeda para valores monetários"), sem abrir. | Do lado fica a Moeda do Sistema, pra quem trabalha com outra moeda. |
| Passa por "Agenda" › "Exibir Feriados" e para em "Guia de configuração" › "Reativar guia de configuração" ("Reabre o passo a passo de configuração inicial do sistema."), sem clicar. | Os feriados da agenda ficam pro tutorial da rotina. E o botão Reativar guia de configuração traz de volta o passo a passo do começo, se você fechou antes de terminar. |

### cap12 · Condições de pagamento (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`), em Configurações; clica na aba "Condições de Pagamento": "Defina parcelamentos padrão (à vista, 30/60/90…) para agilizar vendas e compras a prazo." e a lista com "À vista" e o selo "Padrão". [BACKEND: semente com a condição "À vista", padrão, 1 parcela de 0 dias; só nesta aula, o mundo base tem só "30/60/90 dias"] | Agora, as Condições de Pagamento. São os parcelamentos que a empresa mais usa, prontos pra venda e pra compra a prazo. A lista já traz a condição À vista, que é a padrão. |
| [ILUSTRAÇÃO: 30/60/90: num calendário, uma venda de cobre para a Fundição Bandeira do Vale; na palavra "três", saem dela três parcelas, que pousam em 30, 60 e 90 dias] | Imagina que a Fundição Bandeira do Vale compra cobre e paga em três vezes: trinta, sessenta e noventa dias. |
| De volta à tela: clica em "Nova condição": abre "Nova condição de pagamento" ("Defina o nome e as parcelas. A soma dos percentuais precisa ser 100%."); digita "30/60/90 dias" em "Nome *" e marca "Definir como condição padrão". | Clico em Nova condição. No nome, trinta, sessenta e noventa dias. E marco Definir como condição padrão, porque é a que a Recicla Vale mais usa. |
| Desmarca "À vista (parcela única, 0 dias, 100%)" (as linhas destravam). | Toda condição nova começa À vista. Como essa é parcelada, eu desmarco o À vista. |
| Na primeira linha, "Dias após emissão" 30 e "% do total" 33,33; clica em "Adicionar parcela" e preenche 60 e 33,33; clica de novo e preenche 90 e 33,34. | Em cada parcela vão os dias depois da emissão e quanto ela vale do total. Trinta dias, com trinta e três vírgula trinta e três por cento. Sessenta dias, com o mesmo tanto. E noventa dias, com trinta e três vírgula trinta e quatro, pra fechar a conta. |
| [ZOOM: "Soma dos percentuais" "100%", em verde, a frase inteira] | A Soma dos percentuais fica verde quando fecha cem por cento. Sem fechar os cem, o sistema não salva. |
| Clica em "Criar condição"; toast "Condição criada"; a lista mostra "30/60/90 dias" no alto, com o selo "Padrão" (estrela) e "30 / 60 / 90 dias · 3 parcelas"; a "À vista" fica logo abaixo, sem o selo e com o botão de estrela "Padrão". [BACKEND: insert em `payment_conditions` (`name`, `installments` com `seq`/`days`/`percent`, `is_default` verdadeiro) e update da "À vista" para `is_default` falso; vira `apos-cap12`] | Clico em Criar condição. Pronto: ela entra no alto da lista com o selo Padrão, e a À vista fica sem ele. |
| Zoom na estrela "Padrão" da "À vista", na chave da linha e nos botões "Editar" e "Excluir", sem clicar ("Excluir condição?" só pergunta antes de apagar). | Na À vista, que não é mais a padrão, aparece a estrela Padrão: é ela que troca qual condição é a padrão. A chave do lado desliga a condição sem apagar. O Editar abre a mesma janela, e o Excluir pergunta antes de apagar. E na hora de parcelar uma venda, a padrão aparece no alto da lista, com a marca de padrão. |

### cap13 · Aparência e atalhos (vinheta: APARÊNCIA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap12`), em Configurações; clica na aba "Aparência": "Estilo de Navegação (Desktop)" com "Menu Lateral" marcado. | Na aba Aparência, você escolhe como o sistema fica na tela. |
| Clica em "Menu Superior": o menu da esquerda some e a barra aparece no topo; espera 1,5 s; clica em "Menu Lateral" e o menu volta. [BACKEND: update em `profiles.navigation_style` (vai e volta)] | O Estilo de Navegação troca o menu da esquerda por uma barra lá em cima. Isso vale só no computador. A Recicla Vale prefere o Menu Lateral. |
| Zoom em "Menu (lateral e superior)": "Escuro (recomendado)" marcado e "Seguir o tema". | O menu pode ficar sempre escuro, que é o recomendado, ou seguir o tema. |
| Em "Tema do Sistema", clica em "Tema Escuro" (o sistema escurece); espera 1,5 s; clica em "Tema Claro". | E o Tema do Sistema: claro ou escuro. Cada um escolhe o que cansa menos a vista. |
| Clica na aba "Atalhos": "Atalhos de Teclado" ligado ("Atalhos estão ativados"), a lista "Navegação" ("Dashboard" Shift+D, "Compra" Shift+C, "Venda" Shift+V, "Caixa" Shift+X...) e "Geral" ("Busca Global" "Ctrl+K"). | Agora a aba Atalhos. Cada tela principal tem um atalho: a tecla Shift e uma letra. Clicando na letra, você troca por outra. |
| Zoom na chave "Atalhos de Teclado" (ligada, "Atalhos estão ativados") e no quadro "Dicas" ("Atalhos não funcionam quando você está digitando em campos de texto"), sem clicar. | Se esbarrar nos atalhos sem querer, a chave Atalhos de Teclado, aqui em cima, desliga todos de uma vez. E eles não funcionam quando você está digitando num campo de texto. |
| Aperta Ctrl+K: abre a busca "Buscar páginas, clientes, fornecedores, materiais, funcionários..." com o grupo "Ações Rápidas" visível; digita "cobre": em "Resultados da Busca", "Cobre mel", "Cobre misto" e "Fio de cobre encapado". | E o mais útil de todos: Ctrl+K. Ele abre a busca do sistema inteiro. Sem digitar nada, já aparecem as Ações Rápidas, pra criar coisas sem sair da tela. Digito cobre, e já aparecem os materiais de cobre. |
| Esc fecha a busca. | A busca acha também clientes, fornecedores e telas. É só apertar Esc pra fechar. |

### cap14 · Senha, termos e Zona de Perigo (vinheta: SEGURANÇA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap12`), em Configurações › "Empresa"; a câmera desce, passando pelo fim do cartão "Empresa" e pelo "Filial", até "Segurança". | Pra fechar, a parte de baixo da aba Empresa. Em Segurança fica o Alterar Senha. |
| Clica em "Alterar Senha": abre "Alterar Senha" ("Digite sua nova senha abaixo. Certifique-se de usar uma senha forte."), com "Nova Senha" e "Confirmar Nova Senha"; clica em "Cancelar". | É o caminho de quem já está logado: a senha nova, duas vezes. O mesmo botão também fica no seu Perfil. |
| "Termos de Uso": clica em "Ver Contrato": abre "Termos de Uso e Responsabilidade"; zoom em "Aceito em ..." (a data não é lida). | Em Termos de Uso, o Ver Contrato abre os termos que você aceitou no cadastro, com a data e a hora do aceite. |
| Zoom em "Baixar PDF", sem clicar; clica em "Fechar". | Dá pra baixar em PDF, se quiser guardar uma cópia. |
| Na descida até a "Zona de Perigo", pausa curta em "Histórico de Exclusões" › "Ver histórico" ("Veja quem excluiu o quê e quando — clientes, vendas, materiais e operações destrutivas."), sem clicar. | Aqui também fica o Histórico de Exclusões, que mostra quem apagou o quê e quando. Ele aparece no tutorial de pedidos. |
| Desce até a "Zona de Perigo" (cabeçalho vermelho, "Ações irreversíveis. Revise cuidadosamente antes de confirmar."); zoom em "Zerar Sistema" e na descrição. | E no fim, a Zona de Perigo, em vermelho. Aqui fica o Zerar Sistema, que apaga os dados de operação que você escolher. |
| Clica em "Zerar Sistema": abre "Tem certeza?" ("Você está prestes a acessar a função de zerar o sistema. ..."); clica em "Sim, continuar". | Vou mostrar com calma, sem zerar nada. Primeiro, o sistema pergunta se você tem certeza. |
| Abre "Zerar Sistema - Ação Irreversível": a câmera desce devagar pela lista, "Selecionar tudo" e as dez caixas, todas marcadas: "Clientes e Fornecedores", "Saldos de Clientes e Fornecedores", "Cadastro de Materiais", "Estoque de Materiais", "Movimentações Financeiras", "Categorias Financeiras", "Contas a Pagar e Receber", "Funcionários e Movimentações", "Pedidos (Vendas e Compras)" e "Notas Fiscais e Config. Fiscal". | Depois, ele mostra tudo o que pode ser apagado: clientes e fornecedores e os saldos deles, materiais e estoque, o financeiro com as categorias e as contas a pagar e receber, os funcionários, os pedidos e as notas. Tudo já vem marcado. |
| Desmarca "Clientes e Fornecedores" e "Cadastro de Materiais" (a linha "Serão mantidos:" passa a incluir "Clientes e fornecedores" e "Cadastro de materiais"; o contador mostra "8 itens selecionados para exclusão."); marca as duas de novo (tudo volta a marcado). Nada é apagado: o "Sim, Zerar Sistema" segue travado sem o nome da empresa digitado. | Dá pra desmarcar o que você quer guardar. Quem testou o sistema com dados de mentira costuma zerar os pedidos e o financeiro e manter os cadastros. |
| Zoom em "Serão mantidos: Dados básicos da empresa, Usuários cadastrados, Histórico de pagamentos." (com as caixas todas marcadas). | Ficam só os dados básicos da empresa, os usuários e o histórico de pagamentos, mais tudo o que você desmarcou. |
| [ZOOM: "Esta ação NÃO PODE ser desfeita!" e "PARA CONFIRMAR, DIGITE O NOME DA EMPRESA:" com "Recicla Vale Metais" e o campo "Nome da empresa" vazio, a frase inteira] | Uma dica: zerar não tem volta. Pra confirmar, o sistema pede o nome da empresa digitado, e toda operação fica registrada. |
| Clica em "Cancelar" sem digitar nada (o "Sim, Zerar Sistema" segue travado). [BACKEND: as RPCs `reset_company_audit_start` e `reset_company_step` nunca são chamadas] | Aqui a gente só olhou. Cancelar, e está tudo como estava. |

### cap15 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cadastro ("Criar Conta") e o login ("Entrar"), trechos dos caps 1 e 3. | Pronto! Recapitulando: a gente criou a conta da Recicla Vale, entrou no sistema e viu o trocador de contas e o Esqueci minha senha. |
| Montagem: "Identidade Visual" com o logo e o CNPJ; o endereço com a "Prévia no comprovante" (caps 5 e 6). | Nas Configurações, colocou o logo, o ícone e o CNPJ, e preencheu o contato e o endereço, escolhendo o que sai no comprovante. |
| Montagem: "Numeração de pedidos" e a "Frase Personalizada" (caps 7 e 8). | Viu como o número do pedido aparece e pôs a frase da Recicla Vale no comprovante. |
| Montagem: "Impureza/Tara Desconta no Valor", "Assinaturas no comprovante" e "Idioma do Sistema" (caps 9 a 11). | Conferiu a Usabilidade, com a impureza e a tara, ajustou o papel do comprovante, com o peso líquido e as assinaturas, e viu o idioma do sistema. |
| Montagem: a lista com "30/60/90 dias" e "Padrão" (cap 12). | Criou a condição trinta, sessenta e noventa dias como padrão. |
| Montagem: "Aparência", a busca do Ctrl+K e a "Zona de Perigo" (caps 13 e 14). | E passou pela aparência, pelos atalhos, pelos termos, pela senha e pela Zona de Perigo. |
| Cartão "Próximo: Usuários e permissões"; cartela final. | No próximo tutorial, a gente decide quem entra no sistema e o que cada um pode ver. Até lá! |
