# Roteiro T2 · Usuários e permissões

Roteiro pronto para gerar a voz e gravar (molde da Domiflix; o Kaik ajusta depois se precisar). Coluna Fala = texto da
narração (voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py`. Coluna
Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da 1.59.154 (`T02/inventario.md`).
Desktop 1280×800, logado como Rafael Nogueira (master). Todo capítulo parte de um navegador novo, com o mundo do fim do
capítulo anterior (sementes em `plano.md` → "Gravação"); quando um capítulo continua uma janela do anterior, o `setup`
do robô a reabre fora do vídeo.

- **Título:** Usuários e permissões
- **Antes:** Sua conta e sua empresa (T1)
- **Próximo:** Materiais e tabelas de preço (T3)
- **Vinhetas (áreas):** USUÁRIOS · USUÁRIOS · PERMISSÕES · PERMISSÕES · PERMISSÕES · USUÁRIOS · MASTER · PLANO · VALORES · RESUMO
- **Duração estimada:** ~11 min de vídeo (1.490 palavras de fala, ~9,6 min de voz a 2,6 palavras/s, mais 10 vinhetas e as
  esperas da tela; alvo da fonte: 13 min; 7.986 caracteres de TTS com os títulos)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça).
- **Estado inicial (fim do T1):** só o Rafael (master, "Acesso Total"); plano `personalizado` com `max_users` 3.
- **Criado ao vivo:** Marcos Antunes ("Operador Padrão" sem "Ver Projeção de Lucro", tela inicial "Caixa", foto) e
  Juliana Prado (escritório, 7 telas e 8 ações, sem "Caixa"). **Estado final:** três usuários ativos, "3 / 3 usuários".
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso precisa ter), `[ZOOM: ...]` (zoom suave, a frase inteira),
  `[ILUSTRAÇÃO: ...]` (desenho por código no estilo da marca, nunca tela inventada do app).
- Decisões (ver `plano.md`): a foto e a tela inicial entram pelo "Editar", onde gravam (inventário, achado 1); a câmera
  não desce até o bloco do Cato (fica para o T21); a janela do limite é aberta e cancelada, sem zoom nos valores em reais.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Usuários e permissões". | (sem fala) |
| Dashboard da Recicla Vale Metais, logado como Rafael Nogueira. [ILUSTRAÇÃO: a equipe da Recicla Vale: entram, um a um, três cartões de pessoa (Rafael Nogueira "dono", Marcos Antunes "balança e caixa", Juliana Prado "escritório"), no cartão branco da ilustração, Montserrat, o verde da marca; o título "A equipe" grande no centro sobe quando os cartões entram.] | Oi! Neste tutorial a gente vai colocar a equipe da Recicla Vale Metais dentro do EcoSistema, cada um com o acesso certo. |
| (ilustração) Embaixo do Marcos entram as portas "Caixa", "Estoque" e "Ticket de Pesagem", e um cifrão de lucro riscado, na palavra "lucro". | O Marcos pesa o material e opera o caixa, mas não precisa ver o lucro. |
| (ilustração) Embaixo da Juliana entram "Contas a Pagar/Receber", "Movimentações Bancárias" e "Fiscal & Ambiental", e a porta "Caixa" fechada, na palavra "caixa". | A Juliana cuida das contas e das notas, e não mexe no caixa. |
| (ilustração) Embaixo do Rafael, todas as portas abertas. | É aqui que o dono decide quem vê valor, quem abre caixa e quem não vê nada. |
| Cartão discreto: "Antes: Sua conta e sua empresa". | Se você ainda não viu o tutorial Sua conta e sua empresa, dá uma olhada antes. [pause] Vamos ver onde fica. |

### cap01 · Onde fica (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), no Dashboard. A câmera desce até o rodapé do menu lateral e clica em "Configurações" (ao lado de "Sair"): abre "Configurações do Sistema", na aba "Empresa". | Tudo começa nas Configurações, no rodapé do menu, do lado do Sair. |
| Clica na aba "Usuários e Permissões": o cabeçalho "Usuários e Permissões" ("Gerencie usuários da empresa, papéis e permissões de acesso"). | A equipe fica nesta aba aqui, Usuários e Permissões. |
| A câmera passa por "Empresa: Recicla Vale Metais", pelo selo "1 / 3 usuários" e pelo botão "Criar Usuário". | Em cima ficam o contador de usuários e o botão Criar Usuário. Por enquanto só tem um, o Rafael, o dono. |
| Na lista "Usuários", clica em "Rafael Nogueira" (coroa, "Acesso total · Ativo"): o detalhe com "Master", "Ativo", "Perfil de acesso" "Acesso Total" e "Este usuário tem acesso a todas as telas e ações disponíveis nos módulos contratados pela empresa.". [BACKEND: `active_sessions` com a sessão do Rafael, `last_activity` = FAKE_NOW, para "Última atividade" "Online agora"] | Clicando no nome, aparece o acesso de cada um. A coroa mostra que o Rafael é o master: o responsável pela conta da empresa. |
| [ILUSTRAÇÃO: as abas das Configurações como portas lado a lado ("Empresa", "Usuários e Permissões", "Usabilidade", "Aparência"...), cada uma com a sua chave pendurada; na palavra "permissão", as chaves acendem.] | E se alguém da equipe não acha esta aba? É que cada aba das Configurações tem a sua permissão. |
| (ilustração) A chave "Gerenciar Usuários" acende na porta "Usuários e Permissões", presa ao chaveiro "Configurações", na palavra "Configurações". | A desta aqui se chama Gerenciar Usuários. Com ela ligada, e a tela Configurações também, a pessoa vê a aba e cuida da equipe. |

### cap02 · Criar o usuário (vinheta: USUÁRIOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), na aba "Usuários e Permissões"; clica em "Criar Usuário": janela "Criar Novo Usuário" ("Preencha os dados do novo usuário"), coluna "Dados do usuário". | A equipe começa pelo Marcos, o balanceiro. Clico em Criar Usuário, e abre a janela do novo usuário. |
| Clica em "Nome Completo" e digita "Marcos Antunes". | Primeiro o nome completo: Marcos Antunes. |
| Clica em "Email" e digita "marcos.antunes@reciclavalemetais.example". | Depois o e-mail. É com ele que o Marcos vai entrar no sistema. |
| Clica em "Senha" e digita a senha (aparece em pontinhos); a barra enche e mostra "Senha forte. Deve conter:" com os cinco itens marcados ("Pelo menos 8 caracteres", "Pelo menos 1 número", "Pelo menos 1 letra minúscula", "Pelo menos 1 letra maiúscula", "Pelo menos 1 caractere especial"). [ZOOM: o indicador "Senha forte" e os cinco itens, a frase inteira] | E a senha é você que define, aqui na hora. Repara que a tela mostra se ela está forte: oito caracteres, número, letra minúscula, maiúscula e um caractere especial. |
| A câmera sobe para "Foto do Usuário" ("Foto opcional para o novo usuário"), sem clicar em "Selecionar foto". | Uma dica: a foto, coloca depois de criar, no Editar. É lá que ela fica gravada. |
| A câmera passa para a coluna "Permissões", sem clicar. | Depois de criar, é só passar o e-mail e a senha pro Marcos, e ele já entra. Agora, o que ele vai poder fazer. |

### cap03 · Os três perfis rápidos (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); o `setup` reabre "Criar Usuário" e preenche nome, e-mail e senha do Marcos fora do vídeo. A câmera foca a coluna "Permissões": "Perfis rápidos", com "Acesso Total", "Operador Padrão", "Somente Visualização" e o selo "Personalizado". | Do lado direito ficam as permissões. E pra não ligar uma por uma, tem os perfis rápidos. |
| [ILUSTRAÇÃO: três chaveiros entram um a um, cada um na palavra do seu nome: "Acesso Total" (todas as chaves), "Operador Padrão" (as chaves "Caixa", "Estoque", "Ticket de Pesagem", "Pedidos"), "Somente Visualização" (chaves com um olho desenhado: só abrem pra olhar).] | São três. Pensa num chaveiro: cada perfil já vem com um conjunto de chaves. |
| Clica em "Acesso Total": os interruptores da lista ligam e o selo de cada tela enche. | O Acesso Total liga tudo, igual ao do dono. |
| Clica em "Somente Visualização": a lista muda para as telas de consulta. | O Somente Visualização libera as telas pra consultar, sem editar nem excluir. |
| Clica em "Operador Padrão" (fica marcado); a câmera desce devagar pela lista: "Caixa", "Pedidos", "Estoque", "Ticket de Pesagem", ligados. | E o Operador Padrão é o dia a dia do pátio: caixa, compra e venda, estoque e ticket de pesagem, sem as funções de administração. |
| A câmera fica na lista. | É o que serve pro Marcos. E o perfil é só um ponto de partida: dá pra ajustar depois, chave por chave. |
| Clica em "Criar Usuário" no rodapé ("Criando..."): aviso "Usuário criado com sucesso!"; a lista mostra "Marcos Antunes", "32 permissões · Ativo", e o selo vira "2 / 3 usuários". O detalhe do Marcos não é aberto neste capítulo (inventário, achado 2). [BACKEND: edge `create-company-user` (auth, `profiles.company_id`, `user_roles` operator, 32 linhas em `user_permissions`; resposta `{success, user:{id,email,full_name}}`); vira `apos-cap03`] | Criar Usuário. Pronto, o Marcos está na lista, ativo. |

### cap04 · Telas e ações (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`); "Criar Usuário"; digita "Juliana Prado" em "Nome Completo", "juliana.prado@reciclavalemetais.example" em "Email" e a senha em "Senha" ("Senha forte"). | Agora a Juliana, do escritório. Ela não se encaixa em nenhum perfil, então a gente monta o acesso dela na mão. |
| A câmera desce pela lista de permissões (sem chegar ao bloco do Cato): os blocos "Geral", "Financeiro", "Materiais", "Cadastros"; em cada tela, o interruptor, "Clique para ver N ações" e o selo "0/N". | A lista é separada em grupos. Cada linha é uma tela do sistema, com o interruptor do lado. |
| [ILUSTRAÇÃO: telas e ações: uma porta com a placa "Contas a Pagar/Receber" abre na palavra "porta"; lá dentro entram três botões, "Criar Conta a Pagar/Receber", "Dar Baixa em Conta" e "Excluir Conta", na palavra "dentro".] | Pensa assim: a tela é a porta, e as ações são o que a pessoa pode fazer lá dentro. |
| No bloco "Financeiro", liga o interruptor de "Contas a Pagar/Receber"; clica em "Clique para ver 4 ações": abre "Ações desta tela"; liga "Criar Conta a Pagar/Receber" e "Dar Baixa em Conta"; o selo vira "2/4". [ZOOM: o selo "2/4" e as duas ações ligadas, a frase inteira] | Pra Juliana, eu ligo a tela Contas a Pagar e Receber. Abro as ações dela e ligo duas: Criar Conta e Dar Baixa em Conta. O contador mostra duas de quatro. |
| A câmera mostra a linha "Caixa", desligada, no mesmo bloco (sem abrir as ações dela). | Uma dica: primeiro a tela, depois as ações. Ligar só a ação não abre a tela. Com a tela Caixa desligada, o Registrar Venda sozinho não leva ninguém até o caixa. |
| Clica em "Buscar tela ou ação..." e digita "nota": sobra "Fiscal & Ambiental"; liga a tela, clica em "Clique para ver 4 ações" e liga "Emitir NF-e (Produto)" e "Emitir NFS-e (Serviço)". | Pra achar mais rápido, tem a busca. Digito nota, e aparece o Fiscal & Ambiental. Ligo a tela e as ações de emitir NF-e e NFS-e. |
| Limpa a busca ("Limpar busca") e liga, sem pausa, o resto do escritório: "Ver Totais e Valores Financeiros" (bloco "Geral"); "Dashboard"; "Movimentações Bancárias" com "Gerenciar Contas Bancárias" e "Conciliar Extrato Bancário"; "Relatório Financeiro"; "Pedidos"; "Clientes e Fornecedores" com "Ver saldos de cliente/fornecedor". A linha "Caixa" segue desligada. | Do mesmo jeito, ligo o resto do escritório: o banco, o relatório financeiro, os pedidos e os clientes e fornecedores. O Caixa fica desligado. |
| [ILUSTRAÇÃO: as duas travas: na frente da porta, antes da chave da pessoa, entram dois cadeados, o do plano ("módulo contratado") na palavra "plano" e o do sistema (um escudo) na palavra "servidor"; na fileira de portas, "Funcionários (RH)" sem o módulo some, na palavra "Funcionários".] | Uma dica: duas travas mandam mais que qualquer chave daqui. A primeira é o plano. Tela de módulo que a empresa não contratou nem aparece nesta lista, nem pro dono. Sem o módulo de Funcionários, por exemplo, ninguém vê a tela de Funcionários. |
| (ilustração) O escudo do servidor acende. | A segunda é o próprio sistema, que confere a permissão de novo a cada operação, lá no servidor. Então não tem como contornar por fora. |
| Clica em "Criar Usuário": aviso "Usuário criado com sucesso!"; a lista mostra "Juliana Prado", "15 permissões · Ativo"; o selo vira "3 / 3 usuários". [BACKEND: edge `create-company-user` com as 15 permissões da Juliana (`plano.md`); vira `apos-cap04`] | Criar Usuário, e a Juliana entra na equipe. |

### cap05 · O balanceiro e o escritório (vinheta: PERMISSÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`); na lista, clica em "Marcos Antunes" e, no detalhe, em "Editar": janela "Editar Usuário" ("Atualize os dados e permissões deste usuário"), com o perfil "Operador Padrão" marcado. | Agora os dois casos do pátio. Primeiro o balanceiro: o Marcos opera o caixa, mas o dono não quer que ele veja o lucro. |
| Em "Foto do Usuário", clica em "Selecionar foto" e escolhe `marcos-antunes.jpg` (avatar desenhado); aviso "Foto atualizada com sucesso!". A foto aparece na lista atrás da janela; a da janela só muda ao reabrir. [BACKEND: storage `avatars` (upload e `getPublicUrl`) e `profiles.avatar_url`] | Aproveito e coloco a foto dele. No Editar, ela sobe na hora. |
| Em "Tela inicial", abre a lista ("Automática (última tela acessada)") e escolhe "Caixa". | Na Tela inicial, escolho o Caixa. Assim, quando o Marcos entrar, ele já cai direto no caixa. |
| A câmera passa por "Nova Senha (opcional)" ("Deixe em branco para manter"), sem digitar. | E se um dia ele esquecer a senha, é aqui também: no Nova Senha, você coloca outra. |
| Em "Buscar tela ou ação...", digita "lucro": aparecem "Ver Totais e Valores Financeiros" (no "Geral") e a tela "Caixa"; clica em "Clique para ver 1 ação" e desliga "Ver Projeção de Lucro". | Busco lucro, e aparece o Ver Projeção de Lucro, dentro do Caixa. Desligo. |
| [ZOOM: os "Perfis rápidos", agora com o selo âmbar "Personalizado" e nenhum perfil marcado, a frase inteira] | Repara que o perfil virou Personalizado. Agora é o Operador Padrão com um ajuste. |
| Clica em "Atualizar" ("Salvando..."): avisos "Usuário atualizado com sucesso!" e "Permissões atualizadas! O usuário precisa fazer login novamente para ver as mudanças."; a janela fecha e a lista mostra a foto do Marcos e "31 permissões · Ativo". [BACKEND: `profiles` (`full_name`, `initial_screen_path` `/caixa`), edge `manage-company-users` `update_email` com o mesmo e-mail (200) e RPC `save_user_permissions` (31 permissões, `p_preset` nulo); vira `apos-cap05`] | Atualizar. O aviso lembra que o Marcos precisa entrar de novo pra ver a mudança. Ele continua comprando e vendendo. Só o lucro sai da tela dele. |
| Clica em "Juliana Prado": "Perfil de acesso" "Personalizado" ("15 permissões configuradas individualmente."), "Permissões concedidas" com "Telas (7)" e "Ações (8)"; a câmera desce pela lista de telas (não tem "Caixa"). | E o escritório. A Juliana tem as contas, o banco, o relatório e as notas. A tela Caixa ficou desligada, então ela não abre nem fecha caixa. |

### cap06 · Desativar ou excluir (vinheta: USUÁRIOS)

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

### cap07 · Passar o controle (vinheta: MASTER)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); clica em "Rafael Nogueira": a coroa na lista e "Master" no detalhe. | E o master? Ele é o responsável pela conta da empresa. Só ele exclui usuário e passa o controle pra outra pessoa. |
| [ILUSTRAÇÃO: o bastão: uma coroa sobre o cartão do Rafael, com um escudo atrás; na palavra "sócio", a coroa e o escudo deslizam juntos até um cartão "novo master".] | Pensa num dono que vende o ferro-velho, ou num sócio que assume a empresa. É pra isso que serve o Tornar master. |
| Clica em "Juliana Prado", passa o mouse no "..." e clica em "Tornar master": janela "Passar o controle da empresa?", com "Cancelar" e "Sim, passar o bastão". | No menu da pessoa, Tornar master. A janela explica o que muda: ela passa a ter o controle total, e a troca é na hora. |
| [ZOOM: o trecho "você deixará de ser o master (mantém suas permissões atuais, mas não poderá mais transferir o controle nem ficará protegido contra exclusão)", a frase inteira] | Uma dica: passe o controle só pra quem você confiaria a empresa inteira. Você continua com as suas permissões, mas perde a proteção: o novo master pode até desativar ou excluir a sua conta. |
| Clica em "Cancelar". | Aqui eu cancelo, e o Rafael continua como master. |

### cap08 · O limite de usuários (vinheta: PLANO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), na aba "Usuários e Permissões". [ZOOM: o selo "3 / 3 usuários", a frase inteira] [BACKEND: `companies.subscription_plan` `personalizado`, `max_users` 3] | Agora o tamanho da equipe. Cada plano tem um número de usuários, e ele depende do plano contratado. A Recicla Vale está com três de três: o Rafael, a Juliana e o Marcos. |
| [ILUSTRAÇÃO: as vagas do plano: três cadeiras com os nomes Rafael, Juliana e Marcos; na palavra "desativado", o crachá do Marcos sai e a cadeira dele fica livre; volta em seguida; uma quarta cadeira tracejada, com um "+", entra no fim da frase.] | Pensa em cadeiras: cada usuário ativo ocupa uma. Quem está desativado libera a dele. |
| Clica em "Criar Usuário": abre "Sua equipe cresceu! 🎉", com "3 / 3" e "Usuários cadastrados", e o quadro "Adicionar usuários extras". | Com todas ocupadas, o Criar Usuário abre esta janela. |
| Clica no "+" uma vez ("2", "usuários") e no "−" uma vez ("1", "usuário"); a câmera fica em "Adicionar usuários extras" e em "Novo limite de usuários:" ("4 usuários"), sem zoom nos valores em reais. | Aqui você escolhe quantos usuários a mais quer. Cada usuário extra entra na mensalidade, e a tela já mostra a estimativa. |
| A câmera passa por "Seu plano será convertido para Personalizado" e pelo botão "Continuar" (sem clicar); clica em "Cancelar". | O Continuar calcula o valor certinho antes de você confirmar. Aqui eu só olho, e cancelo. |

### cap09 · Esconder o valor (vinheta: VALORES)

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

### cap10 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a aba "Usuários e Permissões" com a lista dos três. | Pronto! Recapitulando: a gente achou a aba Usuários e Permissões, nas Configurações, e viu que ela depende da permissão Gerenciar Usuários. |
| Montagem rápida: a janela "Criar Novo Usuário" e os "Perfis rápidos" (trechos dos capítulos 2 e 3). | Criou o Marcos com nome, e-mail e a senha definida na hora, e deu a ele o Operador Padrão. |
| Montagem rápida: "Contas a Pagar/Receber" com "2/4" (capítulo 4). | Montou na mão o acesso da Juliana, tela por tela e ação por ação, sem o caixa. |
| Montagem rápida: o selo "Personalizado" e o aviso de permissões (capítulo 5). | Tirou a projeção de lucro do Marcos e colocou a foto e a tela inicial dele. |
| Montagem rápida: "Inativo" e a janela "Passar o controle da empresa?" (capítulos 6 e 7). | Desativou e ativou um usuário, viu que excluir não tem volta e que passar o controle pede confiança. |
| Montagem rápida: o selo "3 / 3 usuários" e o "Ver Totais e Valores Financeiros" (capítulos 8 e 9). | E entendeu o limite do plano e as permissões de valor. |
| Cartão "Próximo: Materiais e tabelas de preço"; cartela final. | No próximo tutorial, a gente monta o cardápio de materiais da Recicla Vale, com o preço de cada um. Até lá! |
