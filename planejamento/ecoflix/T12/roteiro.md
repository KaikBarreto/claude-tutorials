# Roteiro T12 · Coletas e Logística (EcoSistema 1.60.18)

Roteiro pronto para o ensaio e, depois da revisão geral, para a voz (molde da Domiflix, sem etapa de aprovação). Coluna
Fala = texto da narração (voz Kaik Barreto), na grafia da legenda; o texto exato do TTS, com a grafia de pronúncia, está em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
(`T12/inventario.md`, conferidos de novo no 1.60.18).
**Aplicação do 1.60.18 (20/11)**: a aula passou de 13 para 18 capítulos (0 a 17). Novos: 7 Editar, cancelar e excluir; 8 O
relatório para o parceiro; 12 Movimentações e a ficha do parceiro; 13 Onde está o caminhão (Rastreamento); 16 Checklist e
assinaturas. Renumerados: o antigo 7 (portal) virou 9, o 8 (frota) 10, o 9 (caçambas) 11, o 10 (relatório) 14, o 11
(regras) 15 e o 12 (recapitulando) 17. Trechos novos nos capítulos 2 (Lista, Calendário e Filtros), 3 (Sem cadastro e
Cliente), 4 (Não definido), 5 (o botão de mais), 6 (arrastar, bags e a ordem sem cadastro), 9 (Recusar), 10 (Editar e
Excluir, aviso de toneladas), 11 (Novo tipo, manutenção, saldo dos bags) e 15 (aviso de solicitação).
Tela da gravação: 1600×900, logado como Rafael Nogueira (MASTER). Todo capítulo parte de um navegador novo, com o mundo
do fim do capítulo anterior (sementes `t12/inicio` e `t12/apos-capNN`); quando um capítulo continua uma janela do
anterior, o `setup` do robô a reabre fora do vídeo. No cap09 entra uma segunda janela, sem login, com o portal da
Cooperativa Recomeço.

- **Título:** Coletas e Logística
- **Antes:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Próximo:** Produção (T11)
- **Vinhetas (áreas):** COLETAS · ORDENS · AGENDA · ACOMPANHAMENTO · PORTAL · FROTA · EQUIPAMENTOS · RELATÓRIO ·
  CONFIGURAÇÕES · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~26 min de vídeo (2.943 palavras de fala, ~19 min de voz a 2,6 palavras/s, mais a vinheta de
  abertura, 17 vinhetas de capítulo, a cartela, a troca de janela do portal e as esperas dos formulários; as 7
  ilustrações correm junto da fala). Pedido do Kaik (18/11): cobrir cada função, pode ficar mais longo.
- **FAKE_NOW:** `2026-11-10T07:00:00-03:00` (terça) em todos os capítulos (junção: o Edson faz a troca da caçamba cedo; às
  08:40 ele está na balança com a latinha da cooperativa, T8, e às 09:40 sai pra Minas, T17).
- **Estado inicial:** `plano.md` → "Mundo: o que esta aula precisa".
- **🔒** módulo Coletas (dito no cap00), Portal do Cliente (dito nos caps 8 e 9). **Fora da aula:** "Rotas" (só meia frase
  no cap13: "Em breve"). "Rastreamento" entra (decisão do coordenador, 18/11).
- Marcas na coluna Tela: `[BACKEND: ...]`, `[ZOOM: ...]` (campo crítico; dura a frase inteira), `[ILUSTRAÇÃO: ...]`
  (cena desenhada no estilo da marca, nunca tela do app), `[TESTAR: ...]`.
- Erro na tela só quando ensina a resolver: a recusa do "Excluir" (cap07) e o aviso das toneladas (cap10) entram; o
  resto vem falado com "Uma dica:".


### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Coletas e Logística". | (sem fala) |
| [ILUSTRAÇÃO: a coleta no improviso: um caderno aberto com "buscar ferro no Depósito, terça?", um balão de mensagem genérico "a caçamba já encheu", e um caminhão parado no pátio com um ponto de interrogação; estilo da marca, sem logo nem interface de aplicativo de terceiros] | Oi! Neste tutorial o caminhão sai do pátio: a gente agenda a coleta, manda o motorista e fecha o serviço. |
| (a ilustração: o caderno e o balão se juntam num cartão de ordem com "parceiro", "dia", "janela", "motorista" e "caminhão") | Na Recicla Vale Metais, buscar material vivia no caderno e na troca de mensagens. Aqui, cada coleta vira uma ordem, com o parceiro, o dia, o motorista e o caminhão. |
| Cartão discreto: "Módulo Coletas". | Essa parte depende do plano contratado: ela vem no módulo de Coletas. |
| Cartão discreto: "Antes: Clientes, fornecedores e a ficha do parceiro". | Se você ainda não viu o tutorial de clientes e fornecedores, dá uma olhada antes. |
| Dashboard da Recicla Vale Metais (sem enquadrar os números); o cursor abre no menu lateral "Coletas & Logística" e clica em "Ordens de Coleta" (a câmera não para nos outros itens); a tela "Ordens de Coleta" abre. [BACKEND: semente `t12/inicio`] | Tudo fica no menu Coletas & Logística, a começar pelas Ordens de Coleta. [pause] Antes de clicar em qualquer coisa, vamos ver o que o módulo resolve. |

### cap01 · O que o módulo de Coletas resolve (vinheta: COLETAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`), "Ordens de Coleta" aberta; a câmera passa devagar pelo quadro, sem clicar. | O módulo é pra quem vai buscar o material: quem tem caminhão, quem deixa caçamba no parceiro, quem combina de passar na empresa dele. |
| [ILUSTRAÇÃO: o caminho de uma coleta: cinco passos em linha, "alguém pede" (telefone ou portal), "dia e janela", "motorista e caminhão", "a caminho", "concluída"; cada passo acende com a palavra da frase] | Cada coleta vira uma ordem, que passa por etapas: alguém pede, a gente agenda o dia e o período, escala o motorista e o caminhão, ele sai, e a coleta é concluída. |
| (a ilustração: abaixo da linha, um segundo trilho separado, "Compra · Ticket de Pesagem", com os ícones de estoque e de caixa; uma faixa divide os dois trilhos) | Uma coisa importante: a ordem de coleta organiza o serviço. Quem mexe no estoque e no caixa é a compra. |
| (a ilustração: o caminhão volta ao pátio e passa para o trilho da compra) | Quando o caminhão volta, você registra a compra do material como sempre, ou faz um Ticket de Pesagem. Concluir a coleta fecha o serviço, e a compra entra por lá. |

### cap02 · O quadro das ordens (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`); a câmera percorre os cabeçalhos: "Solicitada" (0), "Agendada" (1), "A caminho" (1), "Concluídas" (5) e "Cancelada" (1). | Agora, o quadro. Cada coluna é uma etapa: Solicitada, Agendada, A caminho e Concluídas. E do lado ficam as canceladas. |
| A câmera vai à coluna "Solicitada" (contorno tracejado, "Nenhuma ordem"). | A Solicitada recebe os pedidos que esperam aprovação, como os que chegam pelo portal. Daqui a pouco a gente vê um. |
| A câmera vai ao cartão "#8" em "Agendada": a folhinha da data "Ter 10 nov", o selo "Hoje", "Manhã", "Depósito Irmãos Siqueira", "Edson Moura", "FKD2E41" e os botões "Preencher" e "A caminho" (o "Cancelada" fica no rodapé do cartão). | Cada cartão mostra a data numa folhinha, o número da ordem, o parceiro, o período, o motorista e a placa. Hoje de manhã tem a troca de caçamba do Depósito Irmãos Siqueira, e o selo Hoje marca as coletas do dia. |
| A câmera vai ao cartão "#7" em "A caminho": "Marcelo Tavares" com o selo "Sem cadastro", "Tiago Freitas" e "EZR4C63". | E o Tiago já está a caminho de uma reforma, do Marcelo Tavares, que pediu coleta uma vez só e não tem cadastro. |
| Clique em "Lista" (ícone da barra): a tabela "Nº", "Parceiro", "Material", "Data / Janela", "Motorista", "Veículo", "Status", "Origem" ("Portal"/"Interna"), "Ações"; clique no cabeçalho "Data / Janela"; volta para "Quadro". | Prefere uma tabela? Clico em Lista. As mesmas ordens, uma por linha, e clicando no título da coluna eu ordeno por data, por motorista ou por parceiro. O sistema lembra a visão que você escolheu. |
| Clique em "Calendário": o mês de novembro de 2026 com as ordens em chips na cor do status; clique em "Semana" e em "Mês"; passa o cursor em "Hoje"; volta para "Quadro". [TESTAR: a faixa "Ordens sem data" só aparece com ordem sem data; a fala só cita] | Tem também o Calendário, que põe cada coleta no dia agendado. Dá pra ver o dia, a semana ou o mês, e o botão Hoje volta pra data de hoje. A ordem que ainda não tem dia fica numa faixa à parte, no alto. |
| Clique em "Filtros": painel "Filtros" com "Data agendada" "De"/"Até", o aviso "As solicitadas aparecem sempre, independente da data.", "Status", "Parceiro" e "Limpar Filtros" (só mostra, fecha sem filtrar). | Nos Filtros, eu escolho o período, o status e o parceiro. Repara no aviso: as solicitadas aparecem sempre, pra nenhum pedido ficar escondido. Depois, Limpar Filtros. |
| A câmera em "Nova ordem" (não clica). | E o botão Nova ordem fica aqui em cima. |
| A câmera volta às colunas e para em "Concluídas" e "Cancelada". | Uma dica: a ordem anda sempre pra frente, uma etapa de cada vez. Concluída ou cancelada, ela fica no quadro como registro. Se cancelou por engano, é só criar uma nova. |

### cap03 · Criar uma ordem (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`); clique em "Nova ordem": janela "Nova ordem de coleta", com as etapas "Parceiro", "Coleta" e "Frota" e "Parceiro da coleta" em "Cadastrado". | A Auto Peças Vale Forte ligou: tem radiador e bateria pra buscar. Clico em Nova ordem. São três etapas: Parceiro, Coleta e Frota. |
| Clique em "Sem cadastro": aparecem "Nome do solicitante *" ("Nome de quem está pedindo a coleta"), "Telefone" e "Endereço completo * — obrigatório sem cadastro" (só mostra); volta para "Cadastrado". | Quem já tem cadastro fica em Cadastrado. Pra quem pede coleta de vez em quando, como o Marcelo, tem o Sem cadastro. Aí basta o nome de quem pediu, o telefone e o endereço completo, que nesse caso é obrigatório, porque é o único jeito do motorista chegar. |
| "Tipo" em "Fornecedor" (a câmera passa pela opção "Cliente"); em "Parceiro *" clica em "Selecionar…": janela "Selecionar Fornecedor"; digita "Vale Forte" e escolhe "Auto Peças Vale Forte". [BACKEND: `suppliers` com o endereço do cadastro] | O Tipo é Fornecedor, porque é de quem a gente compra. Se o material estiver com quem compra de você, o Tipo pode ser Cliente. No Parceiro, busco a Auto Peças Vale Forte. |
| O endereço preenche sozinho com o do cadastro (CEP, rua, número, bairro, cidade e UF). | Repara: o endereço veio do cadastro dela. Se a coleta for em outro lugar, é só mudar aqui. |
| Clique em "Avançar": etapa "Coleta"; em "Material estimado" ("Ex: ~500kg de ferro") digita "~400 kg de radiadores e baterias". [ZOOM: "Material estimado" com "~400 kg de radiadores e baterias"] | Avançar. Na etapa Coleta, o Material estimado: uns 400 kg de radiadores e baterias. |
| Em "Observações" ("Detalhes da coleta, ponto de referência…") digita "Retirar pelo portão lateral". | E nas Observações, o que ajuda o motorista a achar e a carregar: retirar pelo portão lateral. |

### cap04 · Data e janela (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`); o `setup` refaz fora do vídeo a etapa "Parceiro" e, na etapa "Coleta", o material e a observação; a câmera abre na etapa "Coleta", com "Data agendada" e "Período" vazios. | Agora, o dia e o período. Ainda na etapa Coleta, ficam a Data agendada e o Período. |
| Em "Data agendada" digita 11/11/2026. | A Auto Peças pediu pra amanhã, quarta, onze de novembro. |
| Abre "Período": "Não definido", "Manhã", "Tarde" e "Dia todo". | O Período é a janela do dia: manhã, tarde ou dia todo. Assim o motorista sabe quando passar, e o parceiro, quando esperar. E se o dia ainda não está combinado, tem o Não definido: a ordem fica sem data. |
| Escolhe "Manhã"; a câmera fica nos dois campos. | Escolho manhã. E as janelas que aparecem aqui você define nas Configurações, no fim da aula. |
| Clique em "Avançar": etapa "Frota". | Avanço pra última etapa. |

### cap05 · Motorista e veículo (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`); o `setup` refaz fora do vídeo as etapas "Parceiro" e "Coleta"; a câmera abre na etapa "Frota", com "Motorista" e "Veículo" e o botão de mais de cada um. | Falta quem vai buscar. Na etapa Frota ficam o Motorista e o Veículo, os mesmos da pesagem. Se faltar alguém no cadastro, o botão de mais ao lado cadastra na hora, sem sair da ordem. |
| Em "Motorista" digita "Jair" e escolhe "Jair Lopes"; em "Veículo" digita "GHT" e escolhe "GHT7B19". | O Jair vai com o caminhão 3/4, que leva os 400 kg com folga. |
| A câmera desce ao quadro "Revisão": "Parceiro: Auto Peças Vale Forte", "Cidade: Taubaté / SP", "Material: ~400 kg de radiadores e baterias" e "Data: 11/11/2026 · Manhã". | Embaixo, a Revisão mostra tudo antes de criar: o parceiro, a cidade, o material, a data e o período. |
| Clique em "Criar ordem": aviso "Ordem de coleta criada"; o cartão "#9" na coluna "Agendada", com "Manhã", "Jair Lopes" e "GHT7B19". [BACKEND: rpc `get_next_collection_order_number` (9) + insert em `collection_orders` (status agendada, origem interna)] | Criar ordem. Pronto: a ordem nove já está agendada, com o Jair e o caminhão 3/4. |
| A câmera fica no cartão. | Motorista e veículo também podem ficar pra depois. Quem quiser exigir os dois antes de agendar tem a opção nas Configurações. |

### cap06 · Acompanhar até concluir (vinheta: ACOMPANHAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap05`); o robô ARRASTA o cartão "#8" ("Agendada") para a coluna "A caminho": aviso "Status alterado para A caminho". [BACKEND: rpc `change_collection_order_status` (agendada → a_caminho) + evento] | O caminhão saiu. O Edson foi trocar a caçamba do Depósito Irmãos Siqueira. Pra avisar o sistema, dá pra clicar em A caminho ou arrastar o cartão pra coluna do lado, como eu faço agora. |
| No cartão "#8", clique em "Preencher": a tela "Ordem #8", com "Fornecedor" Depósito Irmãos Siqueira, "Endereço", "Agendamento", "Frota" "Edson Moura · FKD2E41" e "Material estimado"; a câmera aponta o aviso "Localização em registro" sem parar nele. [BACKEND: o robô concede a geolocalização com uma coordenada fictícia; insert em `collection_driver_locations`] | Pra fechar o serviço, o botão é o Preencher. Abre a tela da ordem, com tudo o que foi combinado. Se a ordem ainda estiver agendada, o motorista também começa por aqui, no Iniciar coleta, direto do celular. |
| No bloco "Equipamentos", parte "Recolhi": "Tipo de equipamento" → "Caçamba 5 m³"; "Unidade" → "Caçamba 03"; "Adicionar". | No bloco Equipamentos, eu digo o que aconteceu com as caçambas. O Edson recolheu a Caçamba zero três, cheia de ferro. |
| Parte "Entreguei": "Tipo de equipamento" → "Caçamba 5 m³"; "Unidade" → "Caçamba 05" (só as da base); "Adicionar". | E deixou a Caçamba zero cinco vazia no lugar. Nessa lista só aparecem as que estão na base. |
| Parte "Entreguei": "Tipo de equipamento" → "Bag 1 m³"; aparece o campo de quantidade; digita 10; "Adicionar": a linha "Bag 1 m³" "Qtd. 10". | O Depósito também pediu bags. Como o bag é por quantidade, eu só escolho o tipo e digo quantos ficaram: dez. |
| Clique em "Concluir coleta": aviso "Status alterado para Concluída"; a tela passa ao relatório "Relatório de Coleta 8". [BACKEND: rpc `change_collection_order_status` (a_caminho → coletada, `p_equipment_lines`: recolhido Caçamba 03, entregue Caçamba 05 e 10 bags): `completed_at`, evento e as três `collection_equipment_movements`; edge `collection-report`] | Concluir coleta. Pronto: a ordem fechou, e a tela já mostra o relatório da coleta. |
| A câmera fica no relatório. | Uma dica: concluir a coleta fecha o serviço, e só. O ferro que chegou entra no estoque quando você registra a compra, na tela de compra ou num Ticket de Pesagem. |
| Clique em "Voltar às ordens": o cartão "#8" em "Concluídas", com o botão "Relatório"; clique no corpo do cartão: janela "Ordem #8", "Concluída", "Interna". | De volta ao quadro, a ordem oito está em Concluídas. Clicando no cartão, abre a ficha dela. |
| A câmera desce a "Equipamentos movimentados": "Recolhido · Caçamba 5 m³ (Caçamba 03)", "Entregue · Caçamba 5 m³ (Caçamba 05)" e "Entregue · Bag 1 m³ · Qtd. 10". | Aqui ficam os equipamentos que andaram nessa coleta: as caçambas e os bags. |
| A câmera desce ao "Histórico": "Agendada → A caminho" e "A caminho → Concluída", com data e hora. | E o Histórico guarda cada mudança de etapa, com a data e a hora. Assim dá pra saber o que aconteceu com cada coleta. |
| Fecha a ficha; no cartão "#7" ("Sem cadastro") clique em "Preencher": a tela "Ordem #7"; a câmera no aviso "Sem cadastro — esta coleta não tem fornecedor vinculado, então não é possível entregar ou recolher equipamentos (caçambas, bags) aqui." e no botão "Cadastrar como fornecedor" (não clica). | E a coleta do Marcelo, que não tem cadastro? Na tela dela, o sistema avisa que sem fornecedor ligado não dá pra deixar nem recolher caçamba, porque ele precisa saber com quem ela ficou. Se o Marcelo virar parceiro fixo, o botão Cadastrar como fornecedor cria o cadastro e já liga nesta ordem. |

### cap07 · Editar, cancelar e excluir (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap06`); no cartão "#9", clique em "Ações da ordem": "Visualizar", "Editar" e "Excluir". | Nem toda coleta sai como combinado. No menu de três pontinhos de cada cartão ficam o Visualizar, o Editar e o Excluir. |
| Clique em "Editar": a janela da ordem em página única; em "Observações" acrescenta " Ligar antes de chegar."; clique em "Salvar": aviso "Ordem de coleta atualizada". [BACKEND: update em `collection_orders`] | Esqueci de avisar uma coisa ao motorista da Auto Peças. Em Editar, abre a mesma janela, numa página só, e acrescento nas observações: ligar antes de chegar. Aqui também dá pra trocar o motorista, o dia e o endereço. Salvar. |
| No cartão "#9", clique em "Cancelada": "Cancelar coleta?" ("A ordem #9 será marcada como cancelada. Essa ação não pode ser desfeita."); clique em "Voltar". | Se o parceiro desmarcar, o botão Cancelada pede confirmação antes. A ordem cancelada fica no quadro, como registro. Eu volto, porque a Auto Peças vai manter a coleta. |
| No cartão "#8" (concluída), "Ações da ordem" → "Excluir": "Excluir ordem de coleta?"; clique em "Excluir": abre "Não deu para excluir" com o motivo do sistema; clique em "Fechar". [BACKEND: rpc `delete_collection_order` recusando com a mensagem do banco] | E o Excluir apaga de vez, mas só a ordem que não mexeu em nada. Esta já movimentou caçamba, então o sistema explica o motivo e não apaga. |
| A câmera no quadro. | Uma dica: criou por engano, sem ter mexido em nada, exclui. Combinou e não aconteceu, cancela. Assim o relatório mostra o que foi desmarcado. |

### cap08 · O relatório para o parceiro (vinheta: ACOMPANHAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap07`); no cartão "#8", clique em "Relatório": "Relatório de Coleta 8"; a câmera na barra "Copiar link", "Compartilhar no WhatsApp" e "Imprimir" (não clica nos dois últimos; "Copiar link" mostra "Link do relatório copiado"). | Toda coleta concluída vira um relatório. No cartão da ordem oito, o botão Relatório abre essa página, e em cima ficam três botões: Copiar link, Compartilhar no WhatsApp e Imprimir. |
| A câmera desce por "Equipamentos" (Caçamba 03 recolhida, Caçamba 05 e 10 bags entregues) e pelos blocos de "Checklist", "Fotos" e "Assinaturas" quando existirem (aqui só o primeiro). | Mais embaixo, o relatório mostra o que foi recolhido e o que foi entregue, e também o checklist, as fotos e as assinaturas, quando você usa. Quem abre o link não precisa de senha. |
| "Voltar às ordens" → corpo do cartão "#8" → bloco "Relatório do Fornecedor": "Link público (sem login) pra mandar pro Fornecedor.", "Abrir link do Fornecedor" e "Copiar link" (só mostra). | Na ficha da ordem, o mesmo link aparece em Relatório do Fornecedor, com o botão Abrir link do Fornecedor. |
| "Configurações" → bloco "Relatório público": "Mostrar valores no relatório que o cliente abre" (desligado, com o aviso do link público). | Uma dica: o link é público. Nas Configurações, o Mostrar valores no relatório que o cliente abre decide se os valores em reais aparecem nele. |
| A câmera no bloco. [TESTAR: sem o módulo Portal do Cliente a barra mostra no lugar dos botões "O cliente ainda não consegue abrir esse link porque o Portal do Cliente está desligado..."; a fala só cita, o mundo tem o módulo] | E ele depende do Portal do Cliente no plano. Sem o portal, o sistema não mostra os botões: avisa que o cliente ainda não consegue abrir o link. |

### cap09 · A coleta pedida pelo portal (vinheta: PORTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap07`). [ILUSTRAÇÃO: os dois lados do pedido: à esquerda, um navegador genérico com o portal do parceiro e o botão "Solicitar coleta"; à direita, o quadro da Recicla Vale com a coluna "Solicitada"; uma seta leva o pedido para a direita e outra volta com "Agendada"] | E quando o próprio parceiro pede? Ele usa o portal, o link que a Recicla Vale mandou pra ele. Do outro lado, o pedido cai no quadro pra aprovação. |
| Cartão discreto: "Portal do Cliente". | Pedir pelo portal depende também do Portal do Cliente no plano. |
| Segunda janela, sem login: o portal da Cooperativa Recomeço (`/portal/<token>`); clique na aba "Coletas": "Coletas", o botão "Solicitar coleta" e "Minhas coletas", com as concluídas; a câmera no "Ver relatório da coleta" (não clica). [BACKEND: edge `entity-portal` (aba Coletas sem senha)] | Este é o portal da Cooperativa Recomeço, do jeito que ela vê. Na aba Coletas, ela acompanha as coletas dela, abre o relatório das concluídas e pede uma nova. |
| Clique em "Solicitar coleta": janela "Solicitar coleta"; em "Material *" digita "PET prensado"; em "Quantidade estimada" digita "800 kg". [ZOOM: "Material *" e "Quantidade estimada" 800 kg] | A cooperativa tem 800 kg de PET prensado pra sair. Ela preenche o material e a quantidade. |
| Em "Data preferida" digita 13/11/2026; em "Período" escolhe "Tarde"; o "Endereço da coleta" já vem do cadastro. | Escolhe o dia que prefere, sexta, e o período da tarde. O endereço já vem do cadastro. |
| Clique em "Solicitar coleta": aviso "Solicitação enviada (#10)". [BACKEND: edge `collection-request` (status solicitada, número 10; aviso em `user_notifications`)] | Solicitar coleta. O pedido saiu, com o número dez. |
| De volta à janela do sistema (o robô recarrega a tela "Frota" fora do vídeo): o menu "Coletas & Logística" com o ponto vermelho; "Ordens de Coleta": na "Solicitada", o cartão "#10" com "via portal", "Cooperativa Recomeço", "PET prensado — 800 kg", "Sex 13 nov", "Tarde" e os botões "Aprovar" e "Recusar". [TESTAR: o ponto aparece depois de recarregar e some ao abrir o quadro] | Agora, do lado da Recicla Vale. O menu ganhou um pontinho vermelho de aviso. E na coluna Solicitada está o pedido da cooperativa, marcado como via portal. |
| Clique em "Recusar": "Recusar solicitação?" ("Informe o motivo — ele fica registrado no histórico da ordem.", "Motivo"); clique em "Voltar" (não recusa). | Quem decide é a Recicla Vale. Dá pra aprovar ou recusar. Na recusa, abre uma janela pedindo o motivo, que fica no histórico da ordem, e o parceiro lê no portal dele. |
| Clique em "Aprovar": janela "Agendar coleta" ("Ordem #10 — informe a data e a janela da coleta."), "Data da coleta *" com 13/11/2026 e "Janela *" com "Tarde". | Eu volto e aprovo. A data e a janela vêm do pedido, mas quem confirma é você. |
| Clique em "Agendar": aviso "Status alterado para Agendada"; o cartão "#10" vai para "Agendada". [BACKEND: rpc `change_collection_order_status` (solicitada → agendada)] | Agendar. Pronto: a coleta da cooperativa está marcada pra sexta à tarde. |

### cap10 · Veículos e motoristas (vinheta: FROTA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap09`); menu "Coletas & Logística" → "Frota": abas "Veículos" e "Motoristas"; em "Veículos", a lista "Veículos da frota" com EZR4C63, FKD2E41 e GHT7B19 e a busca "Buscar placa, descrição ou RNT" com os ícones de filtro e de ordenação. | Quem faz tudo isso é a frota. Em Frota ficam os veículos e os motoristas, os mesmos da pesagem de compra e venda. Na lista, dá pra buscar, filtrar por tipo de veículo e ordenar. |
| Clique em "FKD2E41": o detalhe com a placa Mercosul, "Caminhão truck" e "Capacidade operacional" ("Tara" 6.380 kg, "Capacidade" 14.000 kg); abre o menu "Ações" da linha: "Editar" e "Excluir" (só mostra; fecha). [ZOOM: "Tara" e "Capacidade"] | No caminhão truck, a ficha mostra a tara e a capacidade. E cada veículo e cada motorista tem Editar e Excluir no menu de três pontinhos. |
| [ILUSTRAÇÃO: tara, bruto e líquido: um caminhão vazio numa balança de pátio, "tara 6.380 kg"; o mesmo caminhão carregado de sucata, "bruto"; a diferença acende como "líquido", o peso do material] | A tara é o peso do caminhão vazio. Carregado, ele pesa mais na balança, e essa diferença é o peso do material. |
| Clique em "Novo veículo": janela "Novo veículo"; em "Placa *" digita FVL8A52 (o desenho da placa aparece embaixo); em "Descrição / Apelido" digita "Caminhão poliguindaste". | A Recicla Vale comprou um caminhão poliguindaste, o que leva e busca caçamba. Em Novo veículo, eu digito a placa e um apelido. |
| Em "UF de licenciamento" escolhe "SP"; em "Tipo" escolhe "Veículo único (truck, toco, utilitário)"; em "Tipo de rodado" escolhe "Toco" (o que passar da fala vai acelerado). | Os dados de transporte servem pros documentos de transporte. Aqui, São Paulo, veículo único e toco. |
| Em "Tara (kg)" digita 7: aparece "Valor parece estar em toneladas — informe em quilos (ex.: 32.000)."; apaga e digita 7100; em "Capacidade (kg)" digita 8500. [ZOOM: "Tara (kg)" 7100 e "Capacidade (kg)" 8500] | Uma dica: a tara e a capacidade vão sempre em quilos. Se eu digitar só sete, o sistema avisa que o valor parece estar em toneladas. A tara dele é 7.100 kg, e a capacidade, 8.500 kg. |
| Clique em "Cadastrar": aviso "Veículo cadastrado"; o FVL8A52 na lista. [BACKEND: insert em `vehicles`] | Cadastrar. Pronto, o poliguindaste já está na frota. E a capacidade em metros cúbicos vai até 999, que é o limite da nota de transporte. |
| Clique na aba "Motoristas": "Motoristas", a lista com Edson Moura, Jair Lopes e Tiago Freitas; clique em "Novo motorista": janela "Novo motorista". | Agora o motorista dele. Na aba Motoristas, clico em Novo motorista. |
| Em "Nome *" digita "Sérgio Paiva"; em "CPF" digita 463.718.205-08; em "Telefone" digita (12) 90000-4417 (o que passar da fala vai acelerado). | O Sérgio Paiva foi contratado pro poliguindaste. Nome, CPF e telefone. |
| Em "CNH" digita 04581273671; em "Categoria" escolhe "C"; em "Validade da CNH" digita 18/06/2030. [ZOOM: "CNH", "Categoria" e "Validade da CNH"] | E a carteira de motorista, a CNH: o número, a categoria C, que é a de caminhão, e a validade. |
| Clique em "Cadastrar": aviso "Motorista cadastrado"; Sérgio Paiva na lista. [BACKEND: insert em `drivers`] | Cadastrar. Agora ele já pode ser escalado nas ordens. |

### cap11 · As caçambas e onde estão (vinheta: EQUIPAMENTOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap10`); menu "Coletas & Logística" → "Equipamentos" ("Caçambas, bags, caixas e paletes em campo"), com as abas "Equipamentos" e "Movimentações". | E as caçambas. Elas ficam em Equipamentos, junto com bags, caixas e paletes. |
| A câmera vai a "Tipos de equipamento": "Caçamba 5 m³" ("Uma a uma", 5) e "Bag 1 m³" ("Por quantidade", 40). | Primeiro vem o tipo. A caçamba é uma a uma: cada uma tem número e lugar próprios. O bag é por quantidade: só interessa quantos tem em cada lugar. |
| Clique em "Novo tipo": "Novo tipo de equipamento"; "Nome *" "Palete de madeira"; a câmera na chave "Cada unidade tem identificação própria" (desligada: "Deixe desligado para equipamentos fungíveis como bags e caixas, contados só por quantidade."); clique em "Cadastrar". [BACKEND: insert em `collection_equipment_types`] | Pra criar um tipo, Novo tipo. O palete eu conto por quantidade, então deixo desligada a opção de identificação própria. Com ela ligada, cada unidade ganha número, como a caçamba. |
| A câmera desce a "Unidades identificáveis": a lista com Caçamba 01 a Caçamba 05, o tipo, o lugar ("Minha base"; a Caçamba 05 com "Depósito Irmãos Siqueira") e "OK". | Embaixo ficam as caçambas, uma por uma. Repara: a Caçamba zero cinco está no Depósito Irmãos Siqueira, onde o Edson deixou hoje. |
| Na Caçamba 02: "Editar" → "Condição" "Em manutenção" (a câmera passa por "Baixada") → "Salvar". [BACKEND: update em `collection_containers`] | Caçamba furada? Em Editar, mudo a condição pra Em manutenção. E a que não volta mais fica como Baixada. |
| Clique em "Nova unidade": janela "Nova unidade"; "Identificação *" Caçamba 06; "Tipo de equipamento *" "Caçamba 5 m³"; "Condição" "OK"; clique em "Cadastrar": aviso "Unidade cadastrada". [BACKEND: insert em `collection_containers`] | Chegou uma caçamba nova. Em Nova unidade, eu dou a identificação, Caçamba zero seis, e o tipo. Cadastrar. |
| Na lista, clique em "Caçamba 06": o detalhe com "Posição atual" "Sem movimentação" e "Ainda sem movimentação registrada". | Ela ainda não tem lugar, porque o lugar vem das movimentações. |
| Clique em "Movimentar": janela "Nova movimentação"; o "De *" já vem em "Externo" e a Caçamba 06 já vem em "Equipamentos *"; em "Para *" clica em "Minha base"; "Registrar": aviso "Movimentação registrada"; "Posição atual" "Minha base". [BACKEND: rpc `register_collection_equipment_movement`] | Clico em Movimentar. Ela veio de fora, de uma compra nova, então vai de Externo pra Minha base. Registrar. Pronto, a Caçamba zero seis está na base. |
| [ILUSTRAÇÃO: o caminho da caçamba: a Caçamba 05 sai de "Minha base" pelo "Entreguei" de uma ordem e vai até o parceiro; enche de sucata; volta pelo "Recolhi" de outra ordem; ao lado, um atalho "Movimentar" para a mudança fora de coleta; em cada seta, uma mão com a etiqueta "você registra"] | Uma dica: a caçamba só muda de lugar quando alguém registra. Na coleta, é o Entreguei e o Recolhi da ordem, que valem quando ela é concluída. Fora da coleta, é o Movimentar, aqui. |
| A câmera desce a "Onde tudo está agora": "Equipamentos", "Na base", "Em campo" e "Com parceiros", e a tabela "Identificação", "Tipo", "Lugar atual", "Desde" e "Condição". | Em Onde tudo está agora fica o resumo: quanto está na base, quanto está em campo e com quantos parceiros. |
| No bloco "Contados por quantidade": "Bag 1 m³"; clique em "Ver saldo por fornecedor": a lista com os parceiros e as quantidades (Cooperativa Recomeço 10, Depósito Irmãos Siqueira 10); "Ocultar saldos". | Os bags aparecem em Contados por quantidade. Em Ver saldo por fornecedor, eu vejo quantos estão com cada parceiro. |
| Clique na aba "Movimentações": as linhas de hoje, a Caçamba 03, a Caçamba 05 e os bags com "Ordem 8" e a Caçamba 06 de "Externo" para "Minha base". | E a aba Movimentações guarda cada ida e volta, com a data e quem registrou. As da troca de hoje mostram a ordem oito. |

### cap12 · Movimentações e a ficha do parceiro (vinheta: EQUIPAMENTOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap11`); aba "Movimentações" → "Nova movimentação": "De *" "Minha base", "Para *" "Parceiro" → "Selecionar parceiro…" → "Cooperativa Recomeço"; linha "Bag 1 m³", "Quantidade" 10; "Registrar". [BACKEND: rpc `register_collection_equipment_movement` (quantidade)] | Fora de uma coleta, eu lanço direto. Na aba Movimentações, Nova movimentação: dez bags da minha base pra Cooperativa Recomeço. Registrar. |
| No menu da linha nova: "Editar" ("Editar movimentação": "Corrige quantidade, data, origem/destino ou observação. Tipo e unidade não mudam aqui — pra isso, anule e lance de novo."; fecha); "Excluir" ("Excluir movimentação?", "Motivo (opcional)"; fecha em "Cancelar"). | Errou? O menu da linha tem Editar e Excluir. O Editar corrige quantidade, data, origem, destino ou observação. Pra mudar o tipo, anula e lança de novo. |
| A câmera em "Filtros" → "Mostrar anuladas" (liga e desliga). [BACKEND: rpcs `void_collection_equipment_movement` e `restore_collection_equipment_movement` só falados; a tela de anuladas fica sem linhas] | A excluída não some: fica como anulada, com o motivo, e dá pra restaurar. Em Filtros, o Mostrar anuladas traz elas de volta pra lista. As que vieram de uma ordem, você corrige na própria ordem. |
| Menu "Clientes e Fornecedores" → ficha do Depósito Irmãos Siqueira → aba "Coletas": "Com este parceiro agora" (Caçamba 05 e bags), "Coletas", "Movimentações de equipamento" e os botões "Movimentar equipamento" e "Agendar coleta" (só mostra). | E na ficha do parceiro tem a aba Coletas: o que está com ele agora, as coletas dele e as movimentações. Dali mesmo dá pra agendar outra coleta ou movimentar equipamento. |

### cap13 · Onde está o caminhão (vinheta: FROTA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap12` + `t12/rastreamento`); menu "Coletas & Logística" → "Rastreamento" ("Acompanhe a frota em tempo real"): o mapa com o Tiago Freitas "Ao vivo" e a lista de motoristas no painel do lado ("Motoristas no mapa" é o título da versão de celular). [BACKEND: rpc `get_collection_live_positions`; tiles e Leaflet pelo handler de rede externa] | Com a coleta a caminho, o Rastreamento mostra no mapa onde está cada motorista. Na lista do lado, o Tiago aparece com o selo Ao vivo. |
| A câmera no selo "Ao vivo" e na frase "O círculo ao redor do ponto é o raio de incerteza do GPS — quanto maior, menos exata é a posição." | A posição vem do celular do motorista, enquanto ele está com a ordem aberta. O círculo em volta do ponto é o raio de incerteza do GPS: quanto maior, menos exata é a posição. |
| A câmera passa pelos selos "Visto há pouco" e "Sem sinal recente" (só na legenda, o mundo só tem o Tiago ao vivo). | O selo muda pra Visto há pouco e depois pra Sem sinal recente, conforme o tempo sem notícia. E pra aparecer no mapa, o motorista precisa ter login no sistema. |
| Em "Trajeto de uma coleta" escolhe a ordem 7: a linha do trajeto e os marcos "Saiu" e "A caminho". | Em Trajeto de uma coleta, dá pra rever o caminho de uma ordem. Eu escolho a ordem sete. |
| Tela "Ordem #7": aviso "Localização em registro — sua posição é salva periodicamente enquanto a coleta está em andamento."; a câmera no item "Rotas" do menu (não clica: "Roteirização", "Em breve"). | Na tela da ordem, o motorista sempre vê o aviso de que a localização está sendo registrada. Sem sinal de GPS, a coleta segue normal, só a posição não é gravada. O menu também tem Rotas, a roteirização, mas ela chega numa próxima atualização. |

### cap14 · O relatório das coletas (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap12`); menu "Coletas & Logística" → "Relatório" ("Indicadores e histórico das coletas"); "Período" em "Este mês": "Total de coletas" 4, "Concluídas" 1, "Canceladas" 0 e "Taxa de conclusão" 25%. | No fim do mês, o relatório. Ele abre no mês atual, com o total de coletas, as concluídas, as canceladas e a taxa de conclusão. |
| Em "Período" escolhe "Mês passado": "Total de coletas" 6, "Concluídas" 5, "Canceladas" 1 e "Taxa de conclusão" 100%. [ZOOM: os quatro números de outubro] | Em outubro foram seis coletas: cinco concluídas e uma cancelada. E a taxa de conclusão deu 100%. |
| [ILUSTRAÇÃO: a conta da taxa: seis cartões de coleta; o cancelado desliza para fora; sobram cinco, todos com o selo "Concluída": 5 de 5, 100%] | Uma dica: a coleta cancelada sai da conta. Das cinco que ficaram, as cinco foram concluídas. |
| De volta à tela: "Por status" e as tabelas "Por motorista", "Por veículo" e "Por parceiro". | Embaixo, as coletas por status, por motorista, por veículo e por parceiro. Dá pra ver quem rodou mais e onde a Recicla Vale mais busca. |
| A câmera vai ao seletor "Período". | Uma dica: cada coleta entra no mês em que foi concluída. A que ainda não foi conta pelo dia agendado, e a que não tem data, pelo dia em que foi pedida. |

### cap15 · As regras das coletas (vinheta: CONFIGURAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap12`); menu "Coletas & Logística" → "Configurações" ("Ajuste a numeração, as janelas e as regras do portal de coletas"); a câmera no bloco "Operação". | Por último, as regras. Em Configurações, o primeiro bloco é o da operação. |
| Em "Prefixo da numeração" ('Ex.: "COL-"') digita COL- e sai do campo: aviso "Prefixo da numeração salvo". | O Prefixo da numeração vai na frente do número de cada ordem. Aqui eu coloco um prefixo de coleta, e as ordens passam a aparecer com ele na frente. |
| A câmera vai a "Janelas de coleta oferecidas" ("Manhã", "Tarde" e "Dia todo", marcadas; a trava "Mantenha ao menos uma janela de coleta" só falada) e a "Exigir motorista e veículo para agendar" (desligado). | Nas Janelas de coleta oferecidas, você escolhe os períodos que aparecem pra agendar. O sistema não deixa desmarcar todas: sempre sobra uma. E aqui dá pra exigir motorista e veículo antes de agendar. |
| A câmera desce ao bloco "Portal e solicitações": "Exigir aprovação da solicitação" (ligado). | No bloco do portal, o Exigir aprovação faz o pedido do parceiro esperar na coluna Solicitada, como o da cooperativa. Desligado, ele já entra agendado. |
| A câmera em "Avisar quando chegar solicitação" ("Notifica você sempre que um parceiro pedir uma coleta pelo portal.", ligado). | O Avisar quando chegar solicitação manda uma notificação pra você a cada pedido novo do portal. |
| Em "Antecedência mínima (horas)" digita 24 e sai do campo: aviso "Antecedência mínima salva"; a câmera passa por "Dias aceitos para coleta" ("Seg" a "Sáb" marcados, "Dom" não). | A Antecedência mínima diz com quantas horas o parceiro precisa pedir: coloco vinte e quatro. E nos Dias aceitos, ele pede de segunda a sábado, e sempre sobra pelo menos um dia. |
| [ILUSTRAÇÃO: as regras só na porta do portal: duas portas para o quadro; a do portal, por onde entra o pedido do parceiro, tem um filtro com "24 h" e "seg a sáb" e um balão "escolha outro dia"; a da Recicla Vale, por onde o operador cria a ordem, passa direto, até para hoje] | Uma dica: essas regras valem só pro que o parceiro pede pelo portal. Se ele pedir fora da regra, o portal explica o motivo e pede outra data. Aqui dentro, a Recicla Vale agenda pra qualquer dia, até pra hoje. |

### cap16 · Checklist e assinaturas (vinheta: CONFIGURAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap15`); "Configurações", bloco "Checklist da coleta" → "Modelos de checklist" → "Novo modelo": "Nome *" "Coleta com caçamba"; "Criar modelo". [BACKEND: insert em `collection_checklist_templates`] | Quer que o motorista confira alguma coisa em toda coleta? É o checklist. Em Modelos de checklist, clico em Novo modelo e dou o nome: Coleta com caçamba. Criar modelo. |
| "Gerenciar perguntas" → "Nova pergunta": "Pergunta *" "Local estava acessível para o veículo?", "Tipo de resposta" "Sim ou não", "Pergunta obrigatória" ligada; "Adicionar pergunta". [BACKEND: insert em `collection_checklist_questions`] | Em Gerenciar perguntas, Nova pergunta. A primeira é de sim ou não, e obrigatória: o local estava acessível pro veículo? |
| "Nova pergunta": "Foto da caçamba no local", tipo "Foto" (não adiciona); a câmera passa pela lista de tipos ("Texto livre", "Número", "Escolher uma opção", "Escolher uma ou mais opções", "Conforme / Não conforme / Não se aplica"). | Também dá pra pedir foto, número, texto livre, uma escolha entre opções, ou conformidade: conforme, não conforme ou não se aplica. E a ordem das perguntas você arrasta. |
| "Fechar"; em "Checklist padrão da empresa" escolhe "Coleta com caçamba" (ajuda: "Usado em toda coleta nova."); liga "Exigir assinatura do responsável no local" (a câmera também em "Exigir assinatura do motorista"). [BACKEND: upsert em `collection_settings`] | Agora escolho esse modelo como o checklist padrão da empresa, que vale pra toda coleta nova, e passo a exigir a assinatura de quem recebeu o motorista no local. Também dá pra exigir a assinatura do motorista. |
| Quadro → cartão "#7" → "Preencher": a tela da ordem traz os blocos "Checklist" e "Assinatura"; a câmera em "Falta para concluir: ...". | Na tela da ordem, o checklist e a assinatura já aparecem. Enquanto faltar alguma coisa obrigatória, o sistema mostra o que falta pra concluir. |
| Responde "Sim", assina em "Responsável no local"; o aviso diminui (não conclui: a foto e a assinatura do motorista ficam para a fala). | O motorista responde pelo celular, o responsável assina na tela, e tudo isso sai no relatório da coleta. |

### cap17 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o quadro (cap02) e a "Nova ordem de coleta" com as três etapas (cap03 a cap05). | Pronto! Recapitulando: a gente conheceu o quadro e criou a coleta da Auto Peças Vale Forte, com data, período, motorista e caminhão. |
| Montagem rápida: "A caminho", o "Recolhi", o "Entreguei" e o "Concluir coleta" (cap06). | Mandou o caminhão pro Depósito Irmãos Siqueira, registrou a troca de caçamba e de bags e concluiu a coleta, com o histórico de cada etapa. |
| Montagem rápida: "Ações da ordem", "Cancelar coleta?" e o relatório com "Copiar link" (cap07 e cap08). | Aprendeu a editar, cancelar e excluir uma ordem, e a mandar o relatório da coleta pro parceiro. |
| Montagem rápida: o "Solicitar coleta" do portal e o "Aprovar" (cap09). | Recebeu o pedido da cooperativa pelo portal e aprovou. |
| Montagem rápida: "Novo veículo", "Novo motorista" (cap10), "Nova unidade" (cap11), "Nova movimentação" (cap12) e o mapa do "Rastreamento" (cap13). | Cadastrou o poliguindaste, o motorista novo e a Caçamba zero seis, lançou movimentações e viu onde cada equipamento está, e onde o motorista está no mapa. |
| Montagem rápida: o "Relatório", as "Configurações" e o checklist (cap14 a cap16). | E conferiu o relatório do mês, ajustou as regras do portal e montou o checklist com assinatura. |
| Cartão "Próximo: Produção"; cartela final. | No próximo tutorial, a gente transforma o que entrou no pátio em produto de maior valor. Até lá! |
