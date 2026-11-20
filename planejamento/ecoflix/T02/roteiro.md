# Roteiro T2 · Usuários e permissões

Roteiro pronto para gerar a voz e gravar (molde da Domiflix; o Kaik ajusta depois se precisar). Coluna Fala = texto da
narração (voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna
Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da 1.60.18 (`T02/inventario.md`).
Desktop 1600×900, logado como Rafael Nogueira (master). Todo capítulo parte de um navegador novo, com o mundo do fim do
capítulo anterior (sementes em `plano.md` → "Gravação"); quando um capítulo continua uma janela do anterior, o `setup`
do robô a reabre fora do vídeo.

- **Título:** Usuários e permissões
- **Antes:** Sua conta e sua empresa (T1)
- **Próximo:** Materiais e tabelas de preço (T3)
- **Vinhetas (áreas):** USUÁRIOS · USUÁRIOS · PERMISSÕES · PERMISSÕES · PERMISSÕES · PERMISSÕES · PERMISSÕES · USUÁRIOS · MASTER · PLANO · VALORES · USUÁRIOS · RESUMO
- **Capítulos:** 14 (00 a 13). **Novos na 1.60.18:** 06 Restrições e contas do banco, 07 O mapa das permissões, 12 Relatório
  por Usuário. **Renumerados:** os antigos 06 a 09 viraram 08 a 11 e o antigo 10 (Recapitulando) virou 13.
- **Duração estimada:** ~19 min de vídeo (2.313 palavras de fala, ~14,8 min de voz a 2,6 palavras/s, mais 13 vinhetas e as
  esperas da tela; antes: 1.483 palavras e ~11 min; 12.568 caracteres de TTS com os títulos)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça).
- **Estado inicial (fim do T1):** só o Rafael (master, "Acesso Total"); plano `personalizado` com `max_users` 3.
- **Criado ao vivo:** Marcos Antunes ("Operador Padrão" com a foto, depois sem "Ver Projeção de Lucro", tela inicial "Caixa") e
  Juliana Prado (escritório, 7 telas e 8 ações, sem "Caixa", montada a partir do "Personalizado"). **Estado final:** três usuários
  ativos, "3 / 3 usuários".
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso precisa ter), `[ZOOM: ...]` (zoom suave, a frase inteira),
  `[ILUSTRAÇÃO: ...]` (desenho por código no estilo da marca, nunca tela inventada do app).
- Decisões (ver `plano.md`): a foto escolhida na criação já grava (1.60.18) e o Editar só a troca; a câmera não desce até o bloco do
  Cato (fica para o T21); a janela do limite é aberta e cancelada, sem zoom nos valores em reais; as restrições e o Peso dos pedidos
  só são mostrados e cancelados (o Marcos segue com todas as contas e sem trava de peso); o Relatório por Usuário abre o relatório
  em outra aba (a gravação fica na aba, o robô devolve o relatório para a ilustração).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Usuários e permissões". | (sem fala) |
| Dashboard da Recicla Vale Metais, logado como Rafael Nogueira. [ILUSTRAÇÃO: a equipe da Recicla Vale: entram, um a um, três cartões de pessoa (Rafael Nogueira "dono", Marcos Antunes "balança e caixa", Juliana Prado "escritório"), no cartão branco da ilustração, Montserrat, o verde da marca; o título "A equipe" grande no centro sobe quando os cartões entram.] | Oi! Neste tutorial a gente vai colocar a equipe da Recicla Vale Metais dentro do EcoSistema, cada um com o acesso certo. |
| (ilustração) Embaixo do Marcos entram as portas "Caixa", "Estoque" e "Ticket de Pesagem", e um cifrão de lucro riscado, na palavra "lucro". | O Marcos pesa o material e opera o caixa, mas não precisa ver o lucro. |
| (ilustração) Embaixo da Juliana entram "Contas a Pagar/Receber", "Movimentações Bancárias" e "Fiscal & Ambiental", e a porta "Caixa" fechada, na palavra "caixa". | A Juliana cuida das contas e das notas, e não mexe no caixa. |
| (ilustração) Embaixo do Rafael, todas as portas abertas. | O dono decide quem vê valor, quem abre caixa e quem não vê nada. |
| Cartão discreto: "Antes: Sua conta e sua empresa". | Se você ainda não viu o tutorial Sua conta e sua empresa, dá uma olhada antes. [pause] Vamos ver onde fica. |

### cap01 · Onde fica (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), no Dashboard. A câmera desce até o rodapé do menu lateral e clica em "Configurações" (ao lado de "Sair"): abre "Configurações do Sistema", na aba "Empresa". | Tudo começa nas Configurações, no rodapé do menu, do lado do Sair. |
| Clica na aba "Usuários e Permissões": o cabeçalho "Usuários e Permissões" ("Gerencie usuários da empresa, papéis e permissões de acesso"). | A equipe fica nesta aba aqui, Usuários e Permissões. |
| A câmera passa por "Empresa: Recicla Vale Metais", pelo selo "1 / 3 usuários" e pelo botão "Criar Usuário" (ao lado, o botão "Relatório por Usuário", só citado no capítulo 12). | Em cima ficam o contador de usuários e o botão Criar Usuário. Por enquanto só tem um, o Rafael, o dono. |
| A câmera passa pela busca da lista "Buscar por nome ou e-mail" ("1 encontrado(s)"). | Com a equipe grande, a busca acha a pessoa pelo nome ou pelo e-mail. |
| Na lista "Usuários", clica em "Rafael Nogueira" (coroa, "Acesso total · Ativo"): o detalhe com "Master", "Ativo", "Perfil de acesso" "Acesso Total" e "Este usuário tem acesso a todas as telas e ações disponíveis nos módulos contratados pela empresa.". [BACKEND: `active_sessions` com a sessão do Rafael, `last_activity` = FAKE_NOW, para "Última atividade" "Online agora"] | Clicando no nome, aparece o acesso de cada um. A coroa mostra que o Rafael é o master: o responsável pela conta da empresa. |
| A câmera passa por "Última atividade" ("Online agora") e pela terceira coluna do detalhe, "Peso dos pedidos" ("Padrão da empresa", "Acompanha a regra definida em Integrações."). | Do lado, você vê quando a pessoa usou o sistema pela última vez. O Rafael está online agora. E ainda tem o peso dos pedidos, que a gente vê melhor daqui a pouco. |
| [ILUSTRAÇÃO: as abas das Configurações como portas lado a lado ("Empresa", "Usuários e Permissões", "Usabilidade", "Aparência"...), cada uma com a sua chave pendurada; na palavra "permissão", as chaves acendem.] | E se alguém da equipe não acha esta aba? É que cada aba das Configurações tem a sua permissão. |
| (ilustração) A chave "Gerenciar Usuários" acende na porta "Usuários e Permissões", presa ao chaveiro "Configurações", na palavra "Configurações". | A desta aqui se chama Gerenciar Usuários. Com ela ligada, e a tela Configurações também, a pessoa vê a aba e cuida da equipe. |

### cap02 · Criar o usuário (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), na aba "Usuários e Permissões"; clica em "Criar Usuário": janela "Criar Novo Usuário" ("Preencha os dados do novo usuário"), coluna "Dados do usuário". | A equipe começa pelo Marcos, o balanceiro. Clico em Criar Usuário, e abre a janela do novo usuário. |
| Clica em "Nome Completo" e digita "Marcos Antunes". | Primeiro o nome completo: Marcos Antunes. |
| Clica em "Email" e digita "marcos.antunes@reciclavalemetais.example". | Depois o e-mail. É com ele que o Marcos vai entrar no sistema. |
| Clica em "Senha" e digita a senha (aparece em pontinhos); a barra enche e mostra "Senha forte. Deve conter:" com os cinco itens marcados ("Pelo menos 8 caracteres", "Pelo menos 1 número", "Pelo menos 1 letra minúscula", "Pelo menos 1 letra maiúscula", "Pelo menos 1 caractere especial"). [ZOOM: o indicador "Senha forte" e os cinco itens, a frase inteira] | E a senha é você que define, aqui na hora. Repara que a tela mostra se ela está forte: oito caracteres, número, letra minúscula, maiúscula e um caractere especial. |
| Em "Foto do Usuário", clica em "Selecionar foto" e escolhe `marcos-antunes.jpg`: a foto aparece na bolinha ao lado ("Foto opcional para o novo usuário"). [BACKEND: storage `avatars` e `profiles.avatar_url` depois do criar, com o `userId` da resposta da edge] | A foto é opcional. Escolho a do Marcos agora mesmo, e ela já entra junto com o cadastro. Se preferir, dá pra colocar ou trocar depois, no Editar. |
| A câmera passa para a coluna "Permissões": o aviso âmbar "Escolha primeiro o perfil deste usuário" ("O Operador Padrão cobre a rotina diária. Use Personalizado quando quiser montar o acesso tela por tela."), com a busca e a lista apagadas embaixo. [ZOOM: o aviso, a frase inteira] | Uma dica: cada e-mail só pode estar em uma empresa. Se ele já estiver em uso, o sistema avisa na hora de criar. [pause] Agora, o que o Marcos vai poder fazer. Repara que a tela pede o perfil antes de liberar a lista. |

### cap03 · Os perfis rápidos (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); o `setup` reabre "Criar Usuário" e preenche nome, e-mail, senha e foto do Marcos fora do vídeo. A câmera foca a coluna "Permissões": "Perfis rápidos", com "Acesso Total", "Operador Padrão" (com o selo "Recomendado"), "Somente Visualização" e "Personalizado"; embaixo, o aviso "Escolha primeiro o perfil deste usuário" e a lista apagada. | Do lado direito ficam as permissões. E a primeira escolha é o perfil. Sem ele, a lista fica apagada e o sistema não deixa criar. |
| [ILUSTRAÇÃO: três chaveiros entram um a um, cada um na palavra do seu nome: "Acesso Total" (todas as chaves), "Operador Padrão" (as chaves "Caixa", "Estoque", "Ticket de Pesagem", "Pedidos"), "Somente Visualização" (chaves com um olho desenhado: só abrem pra olhar); na palavra "Personalizado" entra um quarto chaveiro, vazio.] | São três perfis prontos, e o Personalizado. Pensa num chaveiro: cada perfil pronto já vem com um conjunto de chaves. O Personalizado vem vazio, pra você montar. |
| Clica em "Acesso Total": os interruptores da lista ligam e o selo de cada tela enche. | O Acesso Total liga tudo, igual ao do dono. |
| Clica em "Somente Visualização": a lista muda para as telas de consulta. | O Somente Visualização libera as telas pra consultar, sem editar nem excluir. |
| Clica em "Operador Padrão" (fica marcado: o selo "Recomendado" dá lugar ao visto); a câmera desce devagar pela lista: "Caixa", "Pedidos", "Estoque", "Ticket de Pesagem", ligados. Na última frase, o cursor volta ao botão marcado. | E o Operador Padrão é o dia a dia do pátio: caixa, compra e venda, estoque e ticket de pesagem, sem as funções de administração. É o que o sistema recomenda pra maioria da equipe. |
| A câmera fica na lista. | É o que serve pro Marcos. E o perfil é só um ponto de partida: dá pra ajustar depois, chave por chave. |
| Clica em "Criar Usuário" no rodapé ("Criando..."): aviso "Usuário criado com sucesso!"; a lista mostra "Marcos Antunes" com a foto, "32 permissões · Ativo", e o selo vira "2 / 3 usuários". Clica no Marcos: "Perfil de acesso" "Operador Padrão". [BACKEND: edge `create-company-user` com `preset` `standard_operator` e `bank_account_ids` vazio (auth, `profiles.company_id` e `permission_preset`, `user_roles` operator, 32 linhas em `user_permissions`; resposta `{success, userId, user:{id,email,full_name}}`); RPC `set_user_scale_weight_policy` (sem exceção); foto em `avatars`; vira `apos-cap03`] | Criar Usuário. Pronto, o Marcos está na lista, ativo, com a foto e o perfil Operador Padrão. É só passar o e-mail e a senha pra ele, e ele já entra. |

### cap04 · Telas e ações (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`); "Criar Usuário"; digita "Juliana Prado" em "Nome Completo", "juliana.prado@reciclavalemetais.example" em "Email" e a senha em "Senha" ("Senha forte"). Clica em "Personalizado": o botão fica âmbar com o visto, o aviso some e a lista acende, com tudo desligado. | Agora a Juliana, do escritório. Ela não se encaixa em nenhum perfil pronto, então a gente monta o acesso dela na mão. Primeiro, o Personalizado: a lista libera, com tudo desligado. |
| A câmera desce pela lista de permissões (sem chegar ao bloco do Cato): os blocos "Geral", "Financeiro", "Materiais", "Cadastros"; em cada tela, o interruptor, "Clique para ver N ações" e o selo "0/N". | A lista é separada em grupos. Cada linha é uma tela do sistema, com o interruptor do lado. |
| [ILUSTRAÇÃO: telas e ações: uma porta com a placa "Contas a Pagar/Receber" abre na palavra "porta"; lá dentro entram três botões, "Criar Conta a Pagar/Receber", "Dar Baixa em Conta" e "Excluir Conta", na palavra "dentro".] | Pensa assim: a tela é a porta, e as ações são o que a pessoa pode fazer lá dentro. |
| No bloco "Financeiro", liga o interruptor de "Contas a Pagar/Receber"; clica em "Clique para ver 4 ações": abre "Ações desta tela"; liga "Criar Conta a Pagar/Receber" e "Dar Baixa em Conta"; o selo vira "2/4". [ZOOM: o selo "2/4" e as duas ações ligadas, a frase inteira] | Pra Juliana, eu ligo a tela Contas a Pagar e Receber. Abro as ações dela e ligo duas: Criar Conta e Dar Baixa em Conta. O contador mostra duas de quatro. |
| No bloco "Financeiro", sobe até a tela "Caixa" (desligada), abre "Clique para ver 10 ações" e liga "Registrar Venda": aparece no alto da coluna "Confira esta combinação" com "Registrar Venda está ligado, mas a tela Caixa está desligada."; desliga "Registrar Venda" e o aviso some. [ZOOM: o aviso "Confira esta combinação", a frase inteira] | Uma dica: primeiro a tela, depois as ações. Olha o que acontece se eu ligar o Registrar Venda com a tela Caixa desligada: o sistema avisa pra conferir a combinação, porque sem a tela a pessoa não chega no caixa. Desligo, e o aviso some. |
| Clica em "Buscar tela ou ação..." e digita "nota": sobra "Fiscal & Ambiental" (o bloco do Cato não aparece); liga a tela, clica em "Clique para ver 11 ações" e liga "Emitir NF-e (Produto)" e "Emitir NFS-e (Serviço)". | Pra achar mais rápido, tem a busca. Digito nota, e aparece o Fiscal & Ambiental. Ligo a tela e as ações de emitir NF-e e NFS-e. |
| Limpa a busca ("Limpar busca"; as telas abertas seguem abertas) e liga, sem pausa, o resto do escritório: "Ver Totais e Valores Financeiros" (bloco "Geral"); "Dashboard"; "Movimentações Bancárias" com "Gerenciar Contas Bancárias" e "Conciliar Extrato Bancário"; "Relatório Financeiro"; "Pedidos"; "Clientes e Fornecedores" com "Ver saldos de cliente/fornecedor". A linha "Caixa" segue desligada. | Do mesmo jeito, ligo o resto do escritório: o banco, o relatório financeiro, [pause] os pedidos [pause] e os clientes e fornecedores. O Caixa fica desligado. |
| [ILUSTRAÇÃO: as duas travas: na frente da porta, antes da chave da pessoa, entram dois cadeados, o do plano ("módulo contratado") na palavra "plano" e o do sistema (um escudo) na palavra "servidor"; na fileira de portas, "Funcionários (RH)" sem o módulo some, na palavra "Funcionários".] | Uma dica: duas travas mandam mais que qualquer chave daqui. A primeira é o plano. Tela de módulo que a empresa não contratou nem aparece nesta lista, nem pro dono. Sem o módulo de Funcionários, por exemplo, ninguém vê a tela de Funcionários. |
| (ilustração) O escudo do servidor acende. | A segunda é o próprio sistema, que confere a permissão de novo a cada operação, lá no servidor. Então não tem como contornar por fora. |
| Clica em "Criar Usuário": aviso "Usuário criado com sucesso!"; a lista mostra "Juliana Prado", "15 permissões · Ativo"; o selo vira "3 / 3 usuários". [BACKEND: edge `create-company-user` com `preset` `custom` e as 15 permissões da Juliana (`plano.md`); `permission_preset` nulo; vira `apos-cap04`] | Criar Usuário, e a Juliana entra na equipe. |

### cap05 · O balanceiro e o escritório (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`); na lista, clica em "Marcos Antunes" e, no detalhe, em "Editar": janela "Editar Usuário" ("Atualize os dados e permissões deste usuário"), com o perfil "Operador Padrão" marcado. | Agora os dois casos do pátio. Primeiro o balanceiro: o Marcos opera o caixa, mas o dono não quer que ele veja o lucro. |
| Em "Foto do Usuário", clica em "Selecionar foto" e escolhe `marcos-antunes.jpg` de novo (a foto já veio da criação); aviso "Foto atualizada com sucesso!". [BACKEND: storage `avatars` (upload e `getPublicUrl`) e `profiles.avatar_url`] | A foto dele já veio da criação. Mas dá pra trocar por aqui: escolho uma, e no Editar ela sobe na hora. |
| Em "Tela inicial", abre a lista ("Automática (última tela acessada)") e escolhe "Caixa". | Na Tela inicial, escolho o Caixa. Assim, quando o Marcos entrar, ele já cai direto no caixa. |
| A câmera fica em "Tela inicial" e na ajuda "Só aparecem telas liberadas acima. Se a permissão mudar, o sistema escolhe outra tela válida.". | Só aparecem aqui as telas que ele tem. E se um dia a permissão mudar, o sistema escolhe outra tela sozinho. |
| Logo abaixo, abre "Peso dos pedidos" ("Herdar padrão da empresa", marcado; "Exigir peso da balança"; "Permitir digitação manual") e fecha sem trocar. [ZOOM: as três opções, a frase inteira] | Embaixo fica o Peso dos pedidos. É uma exceção por pessoa: obrigar o peso a vir da balança, ou liberar a digitação, mesmo que a regra da empresa seja outra. A regra geral fica nas Integrações, e o Marcos segue o padrão da empresa. A balança, a gente vê no tutorial do EcoTray. |
| A câmera passa por "Nova Senha (opcional)" ("Deixe em branco para manter"), sem digitar. | E se um dia ele esquecer a senha, é aqui também: no Nova Senha, você coloca outra. |
| Em "Buscar tela ou ação...", digita "lucro": aparecem "Ver Totais e Valores Financeiros" (no "Geral") e a tela "Caixa"; clica em "Clique para ver 1 ação" e desliga "Ver Projeção de Lucro". | Busco lucro, e aparece o Ver Projeção de Lucro, dentro do Caixa. Desligo. |
| [ZOOM: os "Perfis rápidos", agora com o botão "Personalizado" âmbar e o visto, e nenhum perfil marcado (o "Operador Padrão" volta ao selo "Recomendado"), a frase inteira] | Repara que o perfil virou Personalizado. Agora é o Operador Padrão com um ajuste. |
| Clica em "Atualizar" ("Salvando..."): avisos "Usuário atualizado com sucesso!" e "Permissões atualizadas! O usuário precisa fazer login novamente para ver as mudanças."; a janela fecha e a lista mostra a foto do Marcos e "31 permissões · Ativo". [BACKEND: `profiles` (`full_name`, `initial_screen_path` `/caixa`), edge `manage-company-users` `update_email` com o mesmo e-mail (200) e RPC `save_user_permissions_and_bank_accounts` (31 permissões, `p_preset` nulo, `p_bank_account_ids` vazio, `p_scale_weight_override` nulo, que chama `set_user_scale_weight_policy`); vira `apos-cap05`] | Atualizar. O aviso lembra que o Marcos precisa entrar de novo pra ver a mudança. Ele continua comprando e vendendo. Só o lucro sai da tela dele. |
| Clica em "Juliana Prado": "Perfil de acesso" "Personalizado" ("15 permissões configuradas individualmente."), "Permissões concedidas" com "Telas (7)" e "Ações (8)"; a câmera desce pela lista de telas (não tem "Caixa"). | E o escritório. A Juliana tem as contas, o banco, o relatório e as notas. A tela Caixa ficou desligada, então ela não abre nem fecha caixa. |

### cap06 · Restrições e contas do banco (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`; o `setup` abre o "Editar" do Marcos fora do vídeo). A câmera desce a janela até o fim da coluna "Permissões", passando pelo bloco escuro do Cato sem parar: a seção "Restrições" ("Ficam desligadas por padrão. Ative somente para uma exceção consciente."), quatro chaves desligadas. | Até aqui a gente liberou coisas. No fim da lista tem o contrário: as restrições. Elas ficam desligadas, e só entram quando existe uma exceção de verdade. |
| [ILUSTRAÇÃO: um pátio com três operadores e três pilhas de fichas; na palavra "próprios", duas pilhas ficam cinza e sobra a de um operador só.] | Pensa num comprador que roda a rua e não deve ver os fornecedores dos colegas. A restrição faz a pessoa enxergar só o que ela mesma lançou. |
| De volta à janela. [ZOOM: as três primeiras linhas: "Ver somente clientes e fornecedores que cadastrar", "Ver somente os pedidos que lançar", "Ver somente os tíquetes de pesagem que criar", a frase inteira] | São três desse tipo: só os clientes e fornecedores que ela cadastrar, só os pedidos que ela lançar e só os tickets de pesagem que ela criar. |
| Liga "Usar somente as contas bancárias liberadas": abre embaixo "Contas liberadas para este usuário" ("Marque as contas que poderão aparecer em pagamentos por Pix ou transferência."), com os cartões "Conta Principal", "Conta Secundária" e "Poupança antiga". [BACKEND: `bank_accounts` do mundo base (as três contas, `kind` `bank`)] | A quarta é a das contas do banco. Ligo, e aparece a lista de contas da empresa. |
| Marca "Conta Principal": o cartão pinta com a cor da conta. [ZOOM: os cartões, a frase inteira] | Marco só a Conta Principal. Com isso, no Pix e na transferência, o Marcos só vê e só usa essa conta. O cofre e os cartões continuam como estão. |
| A câmera sobe ao topo da coluna: nos "Perfis rápidos", "Personalizado" âmbar. (O aviso "O Cato ficará indisponível..." só aparece para quem tem o Cato; o Marcos não tem.) | Três detalhes. Com a restrição ligada, é preciso marcar pelo menos uma conta, senão o sistema não salva. Qualquer restrição deixa o Cato indisponível pra pessoa, pra ele não contar o que ela não pode ver. E restrição não combina com Acesso Total: o perfil passa a ser Personalizado. |
| Clica em "Cancelar" (nada muda). | Aqui eu só mostrei, então cancelo. O Marcos continua usando todas as contas. |

### cap07 · O mapa das permissões (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`; o `setup` abre o "Editar" do Marcos fora do vídeo); a câmera no bloco "Financeiro". [ILUSTRAÇÃO curta: um mapa com quatro bairros, "Financeiro", "Materiais", "Cadastros" e "Sistema", que acendem um a um.] | Antes de seguir, vale um passeio pela lista inteira, pra você saber o que existe em cada grupo. |
| Abre "Clique para ver 10 ações" do "Caixa": "Registrar Compra", "Registrar Venda", "Registrar Despesa", "Registrar Receita", "Abrir Caixa", "Fechar Caixa", "Ver Dinheiro Total em Caixa", "Ver Projeção de Lucro", "Ver e Operar Todos os Caixas", "Realizar lançamentos e abrir/fechar caixas com data retroativa". | No Caixa, cada operação tem a sua chave: compra, venda, despesa e receita, abrir e fechar o caixa. E duas pra dar com cuidado: operar o caixa dos outros e lançar com data retroativa. |
| Desce: "Movimentações Bancárias" (5 ações abertas: "Usar Contas Bancárias", "Gerenciar Contas Bancárias", "Conciliar Extrato Bancário", "Registrar Movimentação Bancária", "Registrar Transferências Financeiras"), "Relatório Financeiro" ("Exportar Relatórios"), "Contas a Pagar/Receber" (4), "Categorias Financeiras" ("Gerenciar Categorias Financeiras"), "Pedidos" ("Editar e Excluir Pedidos"). | No banco, o Usar Contas Bancárias deixa pagar por Pix sem ver saldo. O Gerenciar mostra os saldos e as contas. O relatório financeiro tem a chave de exportar, as contas têm a das recorrentes e a de excluir, as categorias têm a de gerenciar, e os pedidos, a de editar e excluir. |
| "Fiscal & Ambiental": abre "Clique para ver 11 ações". [ZOOM: a lista das 11, a frase inteira] | No Fiscal, cada documento é uma chave separada: nota de produto, nota de serviço, manifesto de transporte, documentos ambientais, manifestar notas recebidas e o pacote do contador. E o SPED tem cinco: consultar, configurar, classificar, gerar e registrar a validação. |
| Bloco "Materiais": "Estoque" (3 ações), "Histórico de Materiais", "Relatório de Estoque", "Ticket de Pesagem" (4), "Produção" (3), "Coletas & Logística". | Nos Materiais: no Estoque, dá pra deixar a pessoa só cadastrar material, sem editar preço, e o Zerar Estoque é uma chave à parte. O Ticket separa compra de venda. E a Produção tem a chave de ver os custos. |
| Bloco "Cadastros": "Clientes e Fornecedores" (4 ações), "Funcionários (RH)" (3), "CRM/Kanban". | Nos Cadastros: cadastrar parceiro é uma coisa, editar e excluir é outra. Ver o saldo e lançar crédito ou débito no saldo também são chaves separadas. Em Funcionários, excluir e cuidar do ponto têm as suas. |
| Bloco "Sistema": "Gerencial - Dashboard", "Gerencial - Financeiro", "Gerencial - Estoque", "Agenda", "Configurações" (7 ações abertas), "Assinatura" ("Gerenciar Assinatura"). | E no Sistema ficam o Gerencial, a Agenda, a Assinatura e as Configurações, com uma chave pra cada aba, como a gente viu no começo. |
| A câmera volta ao topo; clica em "Cancelar". (As quatro ações novas do banco, do Estoque e dos Cadastros só valem hoje nos pedidos feitos pelo Cato; o detalhe é da T21.) | Algumas dessas chaves também valem quando o pedido é feito pelo Cato, o assistente. E cada uma aparece de novo no tutorial da tela dela. Aqui eu cancelo, sem mudar nada. |

### cap08 · Desativar ou excluir (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); clica em "Marcos Antunes" e passa o mouse no "..." do detalhe: o menu "Tornar master", "Desativar" e "Excluir". | E quando alguém sai de férias, ou sai da empresa? No menu de cada usuário tem dois caminhos: desativar e excluir. |
| [ILUSTRAÇÃO: desativar ou excluir: dois crachás do Marcos lado a lado; o da esquerda vai para um quadro de crachás, com a etiqueta "Desativar" e uma seta de volta, na palavra "guardar"; o da direita se parte em dois, com a etiqueta "Excluir", na palavra "rasgar".] | Desativar é como guardar o crachá: a pessoa fica sem acesso, e você devolve quando quiser. Excluir é rasgar o crachá. |
| Clica em "Desativar": aviso "Usuário desativado!"; a linha do Marcos fica apagada, com "· Inativo"; o detalhe mostra "Inativo" e "A conta está impedida de entrar."; o selo vira "2 / 3 usuários". [ZOOM: o selo "2 / 3 usuários", a frase inteira] [BACKEND: update de `profiles.is_active`] | Desativo o Marcos. Ele fica sem acesso, e tudo o que ele fez continua no sistema. E olha o contador: quem está desativado não conta no limite do plano. |
| Passa o mouse no "..." e clica em "Ativar": aviso "Usuário ativado!"; volta "Ativo" e "3 / 3 usuários". | Pra voltar, é o mesmo menu: Ativar. Pronto, o Marcos está de volta. |
| Passa o mouse no "..." e clica em "Excluir": janela "Excluir usuário" ("Esta ação é irreversível"), "Para confirmar, digite o email do usuário:", o campo "Email de confirmação" e o botão "Excluir Usuário", apagado. | Já o Excluir apaga o acesso de vez, e não tem volta. Por isso a tela pede o e-mail da pessoa pra confirmar. |
| Clica em "Cancelar". | Aqui eu cancelo. No dia a dia, quem sai de férias ou deixa a empresa, você desativa. |
| A câmera passa pela coroa do Rafael na lista, sem abrir o menu dele. | E quem pode o quê? Desativar e ativar ficam com quem cuida desta aba. Excluir aparece só pro master. E o master não pode ser desativado nem excluído. |
| A câmera fica na lista. | Nome, e-mail e senha de alguém, só o master ou a própria pessoa mudam. |

### cap09 · Passar o controle (vinheta: MASTER)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); clica em "Rafael Nogueira": a coroa na lista e "Master" no detalhe. | E o master? Ele é o responsável pela conta da empresa. Só ele exclui usuário e passa o controle pra outra pessoa. |
| [ILUSTRAÇÃO: o bastão: uma coroa sobre o cartão do Rafael, com um escudo atrás; na palavra "sócio", a coroa e o escudo deslizam juntos até um cartão "novo master".] | Pensa num dono que vende o ferro-velho, ou num sócio que assume a empresa. É pra isso que serve o Tornar master. |
| Clica em "Juliana Prado", passa o mouse no "..." e clica em "Tornar master": janela "Passar o controle da empresa?", com "Cancelar" e "Sim, passar o bastão". | No menu da pessoa, Tornar master. A janela explica o que muda: ela passa a ter o controle total, e a troca é na hora. |
| [ZOOM: o trecho "você deixará de ser o master (mantém suas permissões atuais, mas não poderá mais transferir o controle nem ficará protegido contra exclusão)", a frase inteira] | Uma dica: passe o controle só pra quem você confiaria a empresa inteira. Você continua com as suas permissões, mas perde a proteção: o novo master pode até desativar ou excluir a sua conta. |
| Clica em "Cancelar". | Aqui eu cancelo, e o Rafael continua como master. |

### cap10 · O limite de usuários (vinheta: PLANO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), na aba "Usuários e Permissões". [ZOOM: o selo "3 / 3 usuários", a frase inteira] [BACKEND: `companies.subscription_plan` `personalizado`, `max_users` 3] | Agora o tamanho da equipe. O número de usuários depende do plano contratado. A Recicla Vale está com três de três: o Rafael, a Juliana e o Marcos. |
| [ILUSTRAÇÃO: as vagas do plano: três cadeiras com os nomes Rafael, Juliana e Marcos; na palavra "desativado", o crachá do Marcos sai e a cadeira dele fica livre; volta em seguida; uma quarta cadeira tracejada, com um "+", entra no fim da frase.] | Pensa em cadeiras: cada usuário ativo ocupa uma. Quem está desativado libera a dele. |
| [ILUSTRAÇÃO] (continuação) Uma cadeira some e um crachá fica de pé; uma janela "Limite de Usuários Excedido" aparece pequena ao fundo. (Só ilustração: mostrar a janela pede um mundo com excesso de usuários.) | E se o plano diminuir e sobrar gente, o sistema abre uma janela pedindo pra você escolher quem desativar. |
| Clica em "Criar Usuário": abre "Sua equipe cresceu! 🎉", com "3 / 3" e "Usuários cadastrados", e o quadro "Adicionar usuários extras". | Com todas ocupadas, o Criar Usuário abre esta janela. |
| Clica no "+" uma vez ("2", "usuários") e no "−" uma vez ("1", "usuário"); a câmera fica em "Adicionar usuários extras" e em "Novo limite de usuários:" ("4 usuários"), sem zoom nos valores em reais. | Aqui você escolhe quantos usuários a mais quer. Cada usuário extra entra na mensalidade, e a tela já mostra a estimativa. |
| A câmera passa por "Seu plano será convertido para Personalizado" e pelo botão "Continuar" (sem clicar); clica em "Cancelar". | O Continuar calcula o valor certinho antes de você confirmar. Aqui eu só olho, e cancelo. |

### cap11 · Esconder o valor (vinheta: VALORES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); clica em "Marcos Antunes" e em "Editar"; a câmera vai ao bloco "Geral": "Ver Totais e Valores Financeiros" ("Visualizar saldo bancário, totais e projeções de lucro"), ligado. [ZOOM: a linha "Ver Totais e Valores Financeiros" com a descrição, a frase inteira] | Pra fechar, os valores. No topo da lista, no Geral, fica o Ver Totais e Valores Financeiros: o saldo do banco, os totais e o lucro. |
| [ILUSTRAÇÃO: o que some e o que fica: à esquerda, "Some", cartões "Lucro", "Totais do período", "Saldo do caixa" e "Saldo do banco", com os números virando "R$ ••••••" na palavra "pontinhos"; à direita, "Fica", a compra "Ferro pesado · 1.000 kg × R$ 0,95 = R$ 950,00", que entra na palavra "compra".] | Sem essa permissão, esses números aparecem escondidos, com pontinhos no lugar. |
| (ilustração) O lado "Fica" acende. | Agora imagina uma compra de mil quilos de ferro pesado, a noventa e cinco centavos o quilo. Quem compra precisa ver esse preço, senão não fecha o pedido. |
| (ilustração) O lado "Some" acende. | Uma dica: esconder valor não trava a operação. O preço do material continua na compra e na venda. O que some é o consolidado: o lucro, os totais do período, o saldo do caixa e o do banco. |
| De volta à janela: clica em "Clique para ver 10 ações" da tela "Caixa": "Ver Dinheiro Total em Caixa" ligado e "Ver Projeção de Lucro" desligado. | No Marcos, os valores do caixa ficam ligados, porque ele opera o caixa. Só a projeção de lucro está desligada. |
| A câmera desce até "Ticket de Pesagem" e clica em "Clique para ver 4 ações": "Criar Ticket de Pesagem com Valores", desligado. | E pra quem não pode ver nem o preço, como um ajudante que só pesa, o caminho é o Ticket de Pesagem. |
| [ZOOM: a linha "Criar Ticket de Pesagem com Valores" ("Definir preços e ver valores ao criar um ticket de pesagem"), a frase inteira] | Sem o Criar Ticket de Pesagem com Valores e sem o Ver Totais e Valores Financeiros, o ticket fica só com o peso. O valor, quem tem a permissão coloca depois. |
| Clica em "Cancelar" (nada muda). | Aqui não muda nada no Marcos, então eu cancelo. |

### cap12 · Relatório por Usuário (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), na aba; passa o mouse e clica em "Relatório por Usuário": janela "Relatório por Usuário" ("Exporte um relatório de compras e vendas por usuário"). | Ainda nesta aba tem um botão que pouca gente nota: o Relatório por Usuário. Ele mostra quanto cada pessoa comprou e vendeu. |
| Abre "Período" (já em "Este mês"), passa pelas outras opções e volta a "Este mês". | Primeiro o período. Já vem em Este mês, e dá pra trocar por outro. |
| A câmera em "Usuários incluídos" ("3 de 3"); clica em "Desmarcar todos" ("0 de 3") e em "Marcar todos" ("3 de 3"); desmarca "Juliana Prado" ("2 de 3"). | Depois, quem entra. Vêm todos marcados, e dá pra desmarcar todos de uma vez, e marcar de novo. Aqui eu tiro a Juliana, que não lança pedido. |
| A câmera passa por "Excel" (sem clicar) e clica em "Visualizar / PDF": aviso "Relatório gerado com sucesso!"; o relatório "Relatório de Compras e Vendas por Usuário" abre em outra aba (a gravação fica na aba do sistema; o robô devolve o relatório para a ilustração). [ILUSTRAÇÃO tipo "comprovante": o relatório aberto, com "Resumo por Usuário", "Vendas Detalhadas" e "Compras Detalhadas".] [BACKEND: `sales`, `purchases` e itens do mês, com `created_by` do Rafael e do Marcos (o histórico do mundo base)] | Dá pra baixar em Excel, ou abrir pra imprimir e salvar em PDF. O relatório traz as compras e as vendas de cada um, com os pedidos detalhados. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a aba "Usuários e Permissões" com a lista dos três. | Pronto! Recapitulando: a gente achou a aba Usuários e Permissões, nas Configurações, e viu que ela depende da permissão Gerenciar Usuários. |
| Montagem rápida: a janela "Criar Novo Usuário" com a foto e os "Perfis rápidos" (trechos dos capítulos 2 e 3). | Criou o Marcos com nome, e-mail, a senha definida na hora e a foto, e deu a ele o Operador Padrão. |
| Montagem rápida: "Personalizado" e "Contas a Pagar/Receber" com "2/4" (capítulo 4). | Montou na mão o acesso da Juliana, a partir do Personalizado, tela por tela e ação por ação, sem o caixa. |
| Montagem rápida: o botão "Personalizado" âmbar e o aviso de permissões (capítulo 5). | Tirou a projeção de lucro do Marcos e ajustou a tela inicial dele. |
| Montagem rápida: a seção "Restrições", "Contas liberadas para este usuário" e o mapa das permissões (capítulos 6 e 7). | Conheceu as restrições, as contas liberadas por pessoa e o mapa de todas as permissões. |
| Montagem rápida: "Inativo" e a janela "Passar o controle da empresa?" (capítulos 6 e 7). | Desativou e ativou um usuário, viu que excluir não tem volta e que passar o controle pede confiança. |
| Montagem rápida: o selo "3 / 3 usuários", o "Ver Totais e Valores Financeiros" e a janela "Relatório por Usuário" (capítulos 10 a 12). | E entendeu o limite do plano, as permissões de valor e o Relatório por Usuário. |
| Cartão "Próximo: Materiais e tabelas de preço"; cartela final. | No próximo tutorial, a gente monta o cardápio de materiais da Recicla Vale, com o preço de cada um. Até lá! |
