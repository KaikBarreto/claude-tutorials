# Roteiro T2 · Usuários, cargos e permissões

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T02/inventario.md`).
Aula no computador (janela de 1024 px ou mais), logada como Camila Duarte; só o cap08 é gravado à parte, logado como Rafael Lima.
Todos os nomes, e-mails e telefones são fictícios; a senha vem da variável `$TUT_SENHA` e aparece sempre mascarada.

- **Título final:** Usuários, cargos e permissões
- **Vinhetas (áreas):** USUÁRIOS · CARGOS · PERMISSÕES · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Configurações e identidade da empresa (T1)
- **Próximo:** Clientes, Fornecedores e Equipamentos (T3)
- **Duração estimada:** ~11 min de vídeo (1.526 palavras de fala, ~9,8 min de voz a 2,6 palavras/s, mais vinhetas e pausas do robô; o plano previa 10 a 11 min, a fala segue o tempo natural)
- **Estado inicial (fim do T1):** Glacial Cold Brasil com dados, endereço, logo e ícone preenchidos (T1); Camila Duarte (admin) logada; **a lista de usuários tem só a Camila** e não há nenhum cargo
  (padrão do `PRODUCAO.md`: base própria do T2; Rafael e Tatiane são criados na aula e os outros técnicos entram num corte).
- **Criado ao vivo:** cargo **Técnico de Campo** (descrição "Agenda, ferramentas e OS pelo link"; Agenda, Área do Técnico e a ação Editar OS em campo, com a tela Ordens de Serviço desligada);
  cargo **Escritório** (descrição "Atendimento, OS, orçamentos e financeiro do dia a dia"; Dashboard, Agenda com Ver Toda a Agenda, Ordens de Serviço com Criar OS e Editar OS, Orçamentos,
  Clientes e Fornecedores com Criar Cliente e Editar Cliente, Equipamentos, Financeiro com Gerenciar Financeiro: treze permissões); usuário **Rafael Lima** (Técnico, cargo Técnico de Campo,
  rafael.lima@glacialcold.example, (21) 3000-1002); usuária **Tatiane Ribeiro** (Interno, cargo Escritório, tatiane.ribeiro@glacialcold.example, (21) 3000-1008).
- **Entra num corte, sem câmera (antes do cap09):** os técnicos Bruno Alves, Júlia Santos, Lucas Ferreira, Marina Costa e Paulo Souza (ativos, cargo Técnico de Campo); a fala do cap09 cobre ("eu cadastrei os outros técnicos do mesmo jeito").
- **Estado final:** dois cargos e oito usuários ativos (Camila admin; seis técnicos com Técnico de Campo; Tatiane com Escritório); o Paulo Souza é desativado e reativado no cap09, então termina ativo.
  Vira `seeds-extra/t2/apos-cap10.json`; o T5 parte dele (lista de técnicos) e o T7 já nasce com o Rafael de acesso restrito.
- Decisões padrão: sem encenar o limite de usuários estourado (a faixa "Limite de usuários atingido" e a janela de limite ficam fora da tela); "Vincular a Funcionário" só citado, em "Nenhum" (o RH tem tutorial próprio);
  não se escolhe "Administrador" nem "Gestor" (a tela só tem "Interno" e "Técnico"); a lixeira dos cargos nunca é clicada (exclui na hora, sem confirmação); "Duplicar" cargo só existe no celular e fica de fora;
  sem preço de plano; "Área do Técnico™" vira "Área do Técnico" na fala.
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[ILUSTRAÇÃO: ...]` (nenhuma nesta aula).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Usuários, cargos e permissões". | (sem fala) |
| Tela inicial da Dominex, logada como Camila Duarte (Glacial Cold Brasil); a câmera desliza devagar pelo menu lateral. | Oi! Neste tutorial a gente vai colocar a equipe dentro da Dominex, dando a cada pessoa exatamente o acesso de que ela precisa. |
| A câmera passa pelos itens do menu e para em "Agenda" e depois em "Financeiro". | O técnico em campo precisa da agenda dele. Quem fica no escritório precisa da ordem de serviço, do orçamento e do financeiro. Cada um vê só o que faz parte do seu trabalho, e quem decide isso é você. |
| Cartão discreto: "Antes: Configurações e identidade da empresa". | Se você ainda não viu o tutorial Configurações e identidade da empresa, dá uma olhada antes. [pause] Vamos abrir a tela de usuários. |

### cap01 · Onde ficam os usuários (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Clique em "Configurações", no rodapé do menu lateral; abre a tela com o título "Configurações", na aba "Empresa". [TESTAR: entrar sempre por "Configurações" e pela aba (`/usuarios` só redireciona para `/configuracoes?tab=usuarios`)] | Os usuários ficam em Configurações, no rodapé do menu, do lado do Sair. |
| Clique na aba "Usuários e Permissões": o cabeçalho "Usuários e Permissões" com o subtítulo "{count}/{max} usuários • {active} ativos"; zoom no subtítulo. [BACKEND: base própria do T2 (`FAKE_SEEDS_DIR`) só com a Camila, sem cargos e sem funcionários; o plano Master do seed tem vinte vagas e o app de hoje tem quinze, então ajustar o seed ou aceitar o contador com vinte (a fala não cita o número)] | É a aba Usuários e Permissões. Aqui no alto, o contador mostra quantos usuários ativos a empresa tem e quantas vagas o plano oferece. |
| Zoom na lista "Usuários" ("1 usuário cadastrado"), com a Camila Duarte, o texto "Acesso total" embaixo do nome e a etiqueta "Ativo"; à direita, o painel "Selecione um usuário" ("Escolha alguém na lista para consultar dados e permissões."). Sem clicar na Camila agora. [BACKEND: semear `user_permissions` da Camila com o curinga `*` (acesso total); sem isso a linha dela diz "0 permissões" e o painel dela, "Personalizado" e "Nenhuma permissão foi concedida."] | Por enquanto só a Camila, a administradora. A lista fica à esquerda. Ao clicar numa pessoa, o painel da direita mostra os dados e o que ela pode fazer. |
| Zoom nos botões "Configurações" e "Criar Usuário", no canto da aba (sem clicar). | Aqui em cima ficam dois botões. O Criar Usuário cadastra uma pessoa. O Configurações, de dentro desta aba, abre os cargos, que são os modelos de acesso. Antes de cadastrar as pessoas, vale montar os cargos. |

### cap02 · Montando um cargo (vinheta: CARGOS)

| Tela | Fala |
| --- | --- |
| Clique em "Configurações" (o botão da aba): abre a janela "Configurações de Cargos" ("Crie e edite perfis de acesso com permissões pré-definidas"), com o texto "Nenhum cargo cadastrado". [BACKEND: `permission_presets` sem linhas no começo (hoje sem seed, cai em `TABELA_SEM_SEED`); a janela lê `GET permission_presets` por nome] | Clico em Configurações, e abre a janela de cargos, ainda vazia. Uma dica: o cargo é um modelo de acesso, que você monta uma vez e aplica em quantas pessoas quiser. |
| Clique em "Novo Cargo": o formulário com "← Voltar", "Nome *" e "Descrição". Digita "Técnico de Campo" em "Nome *" e "Agenda, ferramentas e OS pelo link" em "Descrição". | O primeiro é o cargo do técnico de campo. Dou o nome, Técnico de Campo, e uma descrição curta. |
| A câmera desce pelo editor de permissões: o campo "Buscar tela ou ação..." e as categorias "Geral", "Serviços", "Comercial", "Operacional", "PDV e Loja", "Financeiro" e "Administração" (em maiúsculas na tela), cada uma com as suas telas e os interruptores. | Embaixo fica o editor de permissões. As telas do sistema aparecem agrupadas por categoria, e cada tela tem o seu interruptor. |
| Liga o interruptor da tela "Agenda" (categoria "Geral"); zoom no contador "0/4" e na seta da linha. | Imagina o que esse técnico precisa. A agenda dele, pra ver as visitas do dia. Então ligo a Agenda. |
| Clique na seta da linha "Agenda": abre "Ações desta tela", com "Sobrescrever Conflito de Agenda", "Ver Contas na Agenda", "Ver Toda a Agenda" ("Ver todas as tarefas da agenda, não apenas as próprias") e "Gerenciar Tarefas", todas desligadas; a câmera para em "Ver Toda a Agenda"; fecha a seta. | Esse zero de quatro mostra as ações que existem dentro da tela, e nenhuma está ligada. Clicando na seta, elas aparecem. O Ver Toda a Agenda, por exemplo, mostra as tarefas de todo mundo. O técnico só precisa das dele, então deixo desligado. |
| Rola até "Operacional" e liga o interruptor da tela "Área do Técnico™" ("Ferramentas de apoio do técnico em campo, como cálculos e tabelas."). [TESTAR: o formulário do cargo segue aberto no cap03; o `setup` do cap03 refaz estes passos sem filmar] | Ligo também a Área do Técnico, com as ferramentas de cálculo e de consulta que ele usa em campo. |

### cap03 · A ação sem a tela (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Continua no formulário do cargo "Técnico de Campo" (Agenda e Área do Técnico ligadas). Rola até "Serviços" e clica na seta da linha "Ordens de Serviço", sem ligar a tela: abre "Ações desta tela" com "Criar OS", "Editar OS", "Excluir OS", "Lançar Receita ao Finalizar OS", "Resetar OS" e "Editar OS em campo", todas desligadas; o interruptor da tela segue desligado e o contador mostra "0/6". | O técnico também trabalha na ordem de serviço, mas ele abre a ordem dele pela agenda ou pelo link. Não precisa da lista com todas as ordens da empresa. Por isso, na linha Ordens de Serviço eu não ligo a tela. Só abro a seta. |
| Liga só o interruptor de "Editar OS em campo" ("Editar equipamentos e checklists dentro de uma OS em andamento"); zoom no texto em itálico "A tela está desligada, mas estas ações continuam valendo por conta própria." e no contador "1/6". | Ligo apenas a ação Editar OS em campo. Repara no aviso em itálico: a tela está desligada, mas a ação continua valendo por conta própria. É assim que o técnico preenche o checklist da ordem, sem ver as ordens do escritório. |
| Clique em "Criar Cargo": toast "Cargo criado com sucesso!"; a janela volta à lista, com o cargo "Técnico de Campo", a descrição e a etiqueta "3 permissões". [BACKEND: `POST permission_presets` com `name`, `description` e `permissions`, sem `company_id` e sem pedir retorno: o handler gera o `id`; o `GET` seguinte já traz o cargo] | Pronto, é só clicar em Criar Cargo. O Técnico de Campo aparece na lista, com três permissões. |

### cap04 · O cargo do escritório (vinheta: CARGOS)

| Tela | Fala |
| --- | --- |
| Clique em "Novo Cargo" (a janela de cargos): digita "Escritório" em "Nome *" e "Atendimento, OS, orçamentos e financeiro do dia a dia" em "Descrição". | Agora o cargo de quem fica no escritório. Chamo de Escritório, com uma descrição do que a pessoa faz. |
| Clique em "Buscar tela ou ação..." e digita "orcamento" (sem acento): a lista fica só com a tela "Orçamentos"; liga o interruptor dela. | Pra achar uma permissão rápido, uso a busca. Ela ignora acento: se eu digito orcamento sem acento, ela acha Orçamentos do mesmo jeito. Ligo a tela. |
| Troca a busca por "financeiro": ficam as telas com esse nome ("Financeiro", aberta, com as suas cinco ações, e as outras telas que citam financeiro); liga o interruptor da tela "Financeiro" e o de "Gerenciar Financeiro" ("Criar e editar transações financeiras"); "Excluir Lançamento Financeiro" fica desligado, com a câmera nele. | Agora digito financeiro. A busca mostra a tela Financeiro e as ações dela. Ligo a tela e o Gerenciar Financeiro, que permite criar e editar lançamentos. O Excluir Lançamento Financeiro eu deixo desligado, porque ele fica à parte: só liga pra quem pode apagar lançamento. |
| Clique em "Limpar busca" e liga, em trecho acelerado: "Dashboard"; "Agenda" com "Ver Toda a Agenda"; "Ordens de Serviço" com "Criar OS" e "Editar OS"; "Clientes e Fornecedores" com "Criar Cliente" e "Editar Cliente"; "Equipamentos". | Limpo a busca e ligo o resto do dia a dia do escritório: o Dashboard, a Agenda com a opção de ver toda a agenda, as Ordens de Serviço com criar e editar, os Clientes e Fornecedores com criar e editar, e os Equipamentos. |
| Clique em "Criar Cargo": toast "Cargo criado com sucesso!"; a lista mostra "Escritório" (com a descrição e "13 permissões") e "Técnico de Campo" ("3 permissões"); a câmera para no lápis de um cargo (sem clicar na lixeira). | Criar Cargo, e os dois cargos estão na lista, cada um com o total de permissões. O lápis edita um cargo. Só um detalhe: quem já recebeu o cargo guarda uma cópia dele. Então, se você mudar o cargo depois, é só aplicar de novo nas pessoas. |

### cap05 · Cadastrando um técnico (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Fecha a janela de cargos (X); clique em "Criar Usuário": abre a janela "Criar Usuário" ("Preencha os dados do novo usuário"), com os dados à esquerda ("Foto do Usuário", "Nome Completo *", "Senha *", "Email *", "Telefone", "Vincular a Funcionário" e "Tipo de Usuário") e "Permissões" à direita. | Com os cargos prontos, vamos cadastrar a equipe. O primeiro é o Rafael, técnico de campo. Clico em Criar Usuário. À esquerda ficam os dados da pessoa, e à direita, as permissões. |
| Digita "Rafael Lima" em "Nome Completo *" e `$TUT_SENHA` em "Senha *" (campo mascarado, sem clicar no olho); o indicador mostra "Senha forte. Deve conter:" com as quatro barras verdes e os cinco itens marcados. [TESTAR: `$TUT_SENHA` cumpre os cinco requisitos (oito caracteres, número, minúscula, maiúscula e caractere especial); o indicador só informa, mas no vídeo fica todo verde] | Escrevo o nome e crio uma senha. O indicador vai ficando verde conforme ela cumpre os requisitos: oito caracteres, um número, uma letra minúscula, uma maiúscula e um caractere especial. Com tudo verde, é uma senha forte. |
| Digita `rafael.lima@glacialcold.example` em "Email *" e `2130001002` em "Telefone" ((21) 3000-1002); a câmera passa por "Vincular a Funcionário" (fica em "Nenhum"). | Agora o e-mail: é com ele e a senha que o Rafael vai entrar. O telefone é opcional. Mais abaixo, o Vincular a Funcionário liga a pessoa ao cadastro do RH, e eu deixo em Nenhum. |
| Zoom no interruptor "Tipo de Usuário": clique em "Técnico" (o interruptor passa de "Interno" para "Técnico"); a legenda muda para "Aparece na listagem de técnicos da OS e pode ser adicionado a equipes". | Em Tipo de Usuário, escolho Técnico. É isso que faz o Rafael aparecer na lista de técnicos da ordem de serviço, pra ser escolhido como responsável. Quem trabalha só no escritório fica como Interno. |
| Em "Permissões" (à direita), "Perfis rápidos": chips "Acesso Total", "Escritório", "Técnico de Campo" e "Personalizado"; clique em "Técnico de Campo": o chip acende com o ✓ e ligam "Agenda", "Área do Técnico™" e, dentro de "Ordens de Serviço" (tela desligada), "Editar OS em campo". | Agora a parte prática. Em Perfis rápidos, clico no cargo Técnico de Campo, e as permissões ligam de uma vez: a Agenda, a Área do Técnico e a ação de editar a OS em campo. É só escolher o cargo aqui, porque é ele que define o que o técnico enxerga. |
| Clique em "Criar Usuário": toast "Usuário criado com sucesso!"; a página recarrega (a tela de carregamento sai na edição) e a lista mostra a Camila Duarte e o Rafael Lima, com "Técnico de Campo" embaixo do nome. [BACKEND: função `create-user` (hoje sem handler): insere `profiles` (`user_id` novo, `company_id`, `full_name`, `email`, `phone`, `is_active` verdadeiro), `user_roles` (se houver papel) e `user_permissions` (com `preset_id`) e responde `user` com `id` e `email`; e-mail repetido responde 400 com "Este e-mail já está cadastrado no sistema."] [TESTAR: depois do reload o robô espera o `idle` e o texto "Usuários e Permissões"] | Criar Usuário, e o Rafael já está na lista, com o cargo Técnico de Campo embaixo do nome. |

### cap06 · Acesso Total ou personalizado (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Clique em "Criar Usuário": digita "Tatiane Ribeiro" em "Nome Completo *", `$TUT_SENHA` em "Senha *", `tatiane.ribeiro@glacialcold.example` em "Email *" e `2130001008` em "Telefone" ((21) 3000-1008) (etapas aceleradas); "Tipo de Usuário" fica em "Interno" (a legenda: "Usuário interno do sistema, não aparece como técnico nas OS"). | A segunda pessoa é a Tatiane, que cuida do escritório. Preencho os dados do mesmo jeito e deixo o tipo como Interno, porque ela não sai pra campo. |
| Em "Perfis rápidos", clique em "Escritório": o chip acende com o ✓ e as treze permissões ligam; a câmera percorre as telas ligadas. | Em Perfis rápidos, clico em Escritório, e as permissões do cargo ligam todas. |
| Na busca, digita "contratos" e liga o interruptor da tela "Contratos": o chip "Escritório" apaga e o "Personalizado" acende com o ✓; clique em "Limpar busca". | Agora imagina que só a Tatiane vá cuidar dos contratos. Procuro Contratos na busca e ligo a tela. Olha os chips: o Escritório apagou, e o Personalizado acendeu. Mexeu em qualquer permissão, o perfil vira Personalizado, e o cargo em si continua do jeito que estava. |
| Clique no chip "Acesso Total": todos os interruptores ligam e o chip acende com o ✓; o mouse fica parado sobre ele. [TESTAR: a dica do chip ("Libera todas as telas e ações, inclusive as que forem criadas no futuro") é `title` nativo do navegador e não aparece na gravação; a fala diz o que ela diz] | Já o Acesso Total liga tudo de uma vez, inclusive as telas que a Dominex criar no futuro. É o perfil de quem administra. |
| Clique no chip "Escritório": a seleção volta ao cargo (a tela "Contratos" desliga) e o chip acende. | Pra Tatiane, vale o cargo do jeito que ele é. Clico em Escritório de novo, e a seleção volta ao cargo. |
| Clique em "Criar Usuário": toast "Usuário criado com sucesso!"; a página recarrega e a lista mostra a Camila Duarte, o Rafael Lima e a Tatiane Ribeiro, com "Escritório" embaixo do nome dela. | Criar Usuário, e a Tatiane entra na lista com o cargo Escritório. |

### cap07 · Conferindo o acesso (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Clique em "Rafael Lima" na lista: o painel mostra o nome, a etiqueta "Ativo" e o e-mail; abaixo, "Perfil de acesso" ("Técnico de Campo", com a descrição "Agenda, ferramentas e OS pelo link") e "Dados do usuário" ("Técnico" e o telefone). | Pra conferir o que cada pessoa pode fazer, é só clicar nela na lista. No painel do Rafael, o Perfil de acesso é o Técnico de Campo, e nos Dados do usuário aparece que ele é Técnico, com o telefone. |
| A câmera desce até "Permissões concedidas": as colunas "Telas (2)", com "Agenda" e "Área do Técnico™", e "Ações (1)", com "Editar OS em campo". | Mais abaixo, as Permissões concedidas: duas telas, a Agenda e a Área do Técnico, e uma ação, a Editar OS em campo. É exatamente o que a gente liberou no cargo. |
| Clique em "Editar": abre "Editar Usuário" ("Atualize os dados e permissões do usuário"), tudo preenchido e com o chip "Técnico de Campo" aceso; clique em "Cancelar". [BACKEND: função `manage-user` (hoje sem handler) com `get_email`, que devolve o e-mail do usuário para a janela de edição abrir completa] | O Editar abre a mesma janela do cadastro, já preenchida. Dá pra ajustar o telefone, o tipo ou as permissões a qualquer hora. Aqui eu só olho e cancelo. |

### cap08 · O que o técnico vê (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Corte para a Dominex aberta como Rafael Lima (o nome dele no cartão da conta, no rodapé do menu); a tela abre na "Agenda". [Gravação à parte: `user` = `rafael.lima@glacialcold.example` no passo de `setup`, partindo do estado do fim do cap07 (Rafael e Tatiane criados); o login por e-mail aceita qualquer senha] | Agora, a prova de verdade: entrar como o Rafael, com o e-mail e a senha que a gente definiu. Ele já abre na Agenda. |
| Zoom no menu lateral: só "Agenda" e "Área do Técnico™". [TESTAR: o menu depende das três permissões do Rafael em `user_permissions` e do segmento com ferramentas (refrigeração tem)] | Repara no menu: só a Agenda e a Área do Técnico. O menu dele tem apenas o que o trabalho pede. Cada pessoa vê só o que foi liberado. |
| Clique em "Área do Técnico™": abre a tela de ferramentas; clique em "Agenda" para voltar. [Não clicar em "Configurações" no rodapé do menu] | A Área do Técnico, com as ferramentas de refrigeração, também está liberada pra ele. E, quando houver ordens pra ele, é pela Agenda que ele abre cada uma e preenche o checklist. |

### cap09 · Desativar e reativar (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Corte para a Camila Duarte, de volta à aba "Usuários e Permissões": a lista tem agora oito pessoas (Bruno Alves, Camila Duarte, Júlia Santos, Lucas Ferreira, Marina Costa, Paulo Souza, Rafael Lima e Tatiane Ribeiro), com o cargo embaixo de cada nome. [BACKEND: seed `apos-cap08` com os cinco técnicos que entram sem câmera (Bruno Alves, Júlia Santos, Lucas Ferreira, Marina Costa e Paulo Souza): `profiles` ativos, `user_roles` tecnico e `user_permissions` com o cargo "Técnico de Campo" e o `preset_id`] | E quando alguém sai de férias ou deixa a empresa? De volta como Camila, a lista já tem o resto da equipe: eu cadastrei os outros técnicos do mesmo jeito. |
| Clique em "Paulo Souza": o painel com a etiqueta "Ativo" e os botões "Editar", "Desativar" e "Excluir"; zoom no subtítulo do alto ("8/{max} usuários • 8 ativos"). | Vou usar o Paulo de exemplo. Olha o contador lá em cima: oito usuários ativos. |
| Clique em "Desativar": toast "Usuário desativado" ("O slot foi liberado. Você pode reativá-lo depois."); a etiqueta passa a "Inativo" na lista e no painel; o subtítulo mostra sete ativos. [BACKEND: função `manage-user` com `deactivate_user` (marca o perfil como inativo; o app relê a lista e a contagem de ativos)] | Clico em Desativar. O acesso dele é cortado, mas o cadastro fica guardado e a vaga do plano é liberada. O contador cai pra sete, e a etiqueta Inativo aparece na lista. |
| Clique em "Reativar": toast "Usuário reativado!"; a etiqueta volta a "Ativo" e o contador volta a oito. [BACKEND: `reactivate_user`, que confere a vaga (erro "Limite de usuários atingido; faça upgrade ou desative outro.") e reativa] | Quando ele voltar, é só clicar em Reativar. O Paulo volta com o mesmo cargo e as mesmas permissões, e o contador sobe de novo. Pra reativar, é só ter uma vaga livre no plano. |
| Clique em "Excluir": abre "Excluir usuário permanentemente?" ("Esta ação é irreversível..."); a câmera lê a mensagem; clique em "Cancelar". [Nunca clicar em "Excluir Permanentemente"; o handler `delete_user` só entra se alguma aula precisar] | O Excluir é diferente: apaga a pessoa do sistema de vez, com acesso, permissões e vínculos. Pra só tirar o acesso, o caminho é o Desativar. Aqui eu cancelo. |
| Clique em "Camila Duarte" (de passagem): o painel mostra a etiqueta "Você" e só o botão "Editar", sem "Desativar" nem "Excluir", com o "Perfil de acesso" em "Acesso total". [TESTAR: só gravar este passo com a Camila em "Acesso total" (seed do cap01); sem isso, a câmera fica na lista e a fala segue igual] | Já na conta da própria Camila, aparece só o Editar. O Desativar e o Excluir ficam pros outros usuários. Uma dica: a empresa sempre fica com pelo menos um administrador ativo, que é quem cuida dos acessos. |

### cap10 · Vagas do plano (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Zoom no subtítulo do alto ("{count}/{max} usuários • {active} ativos"). [Não encenar o limite (regra do Kaik de 30/10 20:56): ficam fora da tela a faixa "Limite de usuários atingido" e a janela de limite] | Pra fechar, as vagas do plano. No contador, o primeiro número é quantos usuários ativos você tem, e o segundo é quantas vagas o plano oferece. |
| Clique no cartão da conta, no rodapé do menu: abre o menu da conta; zoom em "Assinatura" (sem clicar); fecha o menu. [TESTAR: só abrir e fechar o menu, sem navegar] | Só quem está ativo ocupa vaga, e por isso o Desativar libera uma. Quando a equipe crescer além do plano, é na Assinatura, no menu da sua conta, que você aumenta o número de usuários. Isso a gente viu nas boas-vindas à Dominex. |

### cap11 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a janela "Configurações de Cargos" com "Técnico de Campo" e "Escritório"; o editor com a "Agenda" e a ação "Editar OS em campo". | Pronto! Recapitulando: a gente montou dois cargos, o Técnico de Campo e o Escritório, ligando tela por tela e as ações de cada uma. E viu que uma ação pode valer mesmo com a tela desligada. |
| Montagem rápida: o formulário "Criar Usuário" com os "Perfis rápidos"; a lista com o Rafael Lima e a Tatiane Ribeiro; o chip "Personalizado". | Depois cadastrou o Rafael e a Tatiane, aplicando o cargo com um clique, e viu que o perfil vira Personalizado quando se mexe numa permissão, e que o Acesso Total libera tudo. |
| Montagem rápida: o painel do Rafael com "Permissões concedidas"; o menu dele só com Agenda e Área do Técnico; "Desativar" e "Reativar" no Paulo Souza; o contador de vagas. | Conferiu o que cada um pode fazer, entrou como o Rafael pra ver só o que foi liberado, aprendeu a desativar e reativar sem perder o cadastro, e entendeu as vagas do plano. |
| Cartão "Próximo: Clientes, Fornecedores e Equipamentos"; cartela final. | Com a equipe dentro, no próximo tutorial a gente cadastra os clientes, os fornecedores e os equipamentos. Até lá! |
