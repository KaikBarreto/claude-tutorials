# Roteiro T12 · Coletas e Logística

Roteiro pronto para o ensaio e, depois da revisão geral, para a voz (molde da Domiflix, sem etapa de aprovação). Coluna
Fala = texto da narração (voz Kaik Barreto), na grafia da legenda; o texto exato do TTS, com a grafia de pronúncia, está em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
(`T12/inventario.md`, versão 1.59.154).
Desktop (janela de 1280×800), logado como Rafael Nogueira (MASTER). Todo capítulo parte de um navegador novo, com o mundo
do fim do capítulo anterior (sementes `t12/inicio` e `t12/apos-capNN`); quando um capítulo continua uma janela do
anterior, o `setup` do robô a reabre fora do vídeo. No cap07 entra uma segunda janela, sem login, com o portal da
Cooperativa Recomeço.

- **Título:** Coletas e Logística
- **Antes:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Próximo:** Produção (T11)
- **Vinhetas (áreas):** COLETAS · ORDENS · AGENDA · ACOMPANHAMENTO · PORTAL · FROTA · EQUIPAMENTOS · RELATÓRIO ·
  CONFIGURAÇÕES · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~13 min de vídeo (1.716 palavras de fala, ~11 min de voz a 2,6 palavras/s, mais a vinheta de
  abertura, 12 vinhetas de capítulo, a cartela, a troca de janela do portal e as esperas dos formulários; as 7
  ilustrações correm junto da fala; alvo da fonte: 15 min)
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos.
- **Estado inicial:** `plano.md` → "Mundo: o que esta aula precisa" (frota com tara e capacidade, as caçambas e os bags com
  as movimentações, as ordens 1 a 8, o portal da Cooperativa Recomeço).
- **🔒** módulo Coletas (dito no cap00) e Portal do Cliente (dito no cap07). **Fora da aula:** "Rastreamento" e "Rotas"
  (a câmera não para nesses itens do menu e a fala não os cita).
- Marcas na coluna Tela: `[BACKEND: ...]`, `[ZOOM: ...]` (campo crítico; dura a frase inteira), `[ILUSTRAÇÃO: ...]`
  (cena desenhada no estilo da marca, nunca tela do app), `[TESTAR: ...]`.
- Nenhuma mensagem de erro encenada (nem a "Transição inválida"): os ⚠️ entram falados com "Uma dica:".

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
| A câmera vai ao cartão "#8" em "Agendada": "Manhã", "Depósito Irmãos Siqueira", "Taubaté / SP", "Edson Moura", "FKD2E41" e os botões "Preencher", "A caminho" e "Cancelada". | Cada cartão mostra o número da ordem, o parceiro, o período, o motorista e a placa. Hoje de manhã tem a troca de caçamba do Depósito Irmãos Siqueira. |
| A câmera vai ao cartão "#7" em "A caminho": "Marcelo Tavares" com o selo "Sem cadastro", "Tiago Freitas" e "EZR4C63". | E o Tiago já está a caminho de uma reforma, do Marcelo Tavares, que pediu coleta uma vez só e não tem cadastro. |
| A câmera passa por "Filtros", pelos botões "Quadro" e "Lista" e por "Nova ordem". | Em cima ficam os filtros, o botão que troca o quadro por uma lista e o Nova ordem. |
| A câmera volta às colunas e para em "Concluídas" e "Cancelada". | Uma dica: a ordem anda sempre pra frente, uma etapa de cada vez. Concluída ou cancelada, ela fica no quadro como registro. Se cancelou por engano, é só criar uma nova. |

### cap03 · Criar uma ordem (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`); clique em "Nova ordem": janela "Nova ordem de coleta", com as etapas "Parceiro", "Coleta" e "Frota" e "Parceiro da coleta" em "Cadastrado". | A Auto Peças Vale Forte ligou: tem radiador e bateria pra buscar. Clico em Nova ordem. São três etapas: Parceiro, Coleta e Frota. |
| A câmera mostra "Cadastrado" e "Sem cadastro". | Quem já tem cadastro fica em Cadastrado. Pra quem pede coleta de vez em quando, como o Marcelo, tem o Sem cadastro, com nome, telefone e endereço. |
| "Tipo" em "Fornecedor"; em "Parceiro *" clica em "Selecionar…": janela "Selecionar Fornecedor" ("Buscar por nome, apelido, CPF/CNPJ ou telefone..."); digita "Vale Forte" e escolhe "Auto Peças Vale Forte". [BACKEND: `suppliers` com o endereço do cadastro] | O Tipo é Fornecedor, porque é de quem a gente compra. No Parceiro, busco a Auto Peças Vale Forte. |
| O endereço preenche sozinho com o do cadastro (CEP, rua, número, bairro, cidade e UF). | Repara: o endereço veio do cadastro dela. Se a coleta for em outro lugar, é só mudar aqui. |
| Clique em "Avançar": etapa "Coleta" ("Data agendada" e "Período" ficam para o próximo capítulo); em "Material estimado" ("Ex: ~500kg de ferro") digita "~400 kg de radiadores e baterias". [ZOOM: "Material estimado" com "~400 kg de radiadores e baterias"] | Avançar. Na etapa Coleta, o Material estimado: uns quatrocentos quilos de radiadores e baterias. |
| Em "Observações" ("Detalhes da coleta, ponto de referência…") digita "Retirar pelo portão lateral". | E nas Observações, o que ajuda o motorista a achar e a carregar: retirar pelo portão lateral. |

### cap04 · Data e janela (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`); o `setup` refaz fora do vídeo a etapa "Parceiro" (Auto Peças Vale Forte) e, na etapa "Coleta", o material e a observação; a câmera abre na etapa "Coleta", com "Data agendada" e "Período" vazios. | Agora, o dia e o período. Ainda na etapa Coleta, ficam a Data agendada e o Período. |
| Em "Data agendada" digita 12/11/2026. | A Auto Peças pediu pra quinta, doze de novembro. |
| Abre "Período": "Não definido", "Manhã", "Tarde" e "Dia todo". | O Período é a janela do dia: manhã, tarde ou dia todo. Assim o motorista sabe quando passar, e o parceiro, quando esperar. |
| Escolhe "Manhã"; a câmera fica nos dois campos. | Escolho manhã. E as janelas que aparecem aqui você define nas Configurações, no fim da aula. |
| Clique em "Avançar": etapa "Frota". | Avanço pra última etapa. |

### cap05 · Motorista e veículo (vinheta: AGENDA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/inicio`); o `setup` refaz fora do vídeo as etapas "Parceiro" e "Coleta" (12/11/2026, "Manhã"); a câmera abre na etapa "Frota", com "Motorista" e "Veículo". | Falta quem vai buscar. Na etapa Frota ficam o Motorista e o Veículo, os mesmos da pesagem. |
| Em "Motorista" digita "Jair" e escolhe "Jair Lopes"; em "Veículo" digita "GHT" e escolhe "GHT7B19". | O Jair vai com o caminhão três quartos, que leva os quatrocentos quilos com folga. |
| A câmera desce ao quadro "Revisão": "Parceiro: Auto Peças Vale Forte", "Cidade: Taubaté / SP", "Material: ~400 kg de radiadores e baterias" e "Data: 12/11/2026 · Manhã". | Embaixo, a Revisão mostra tudo antes de criar: o parceiro, a cidade, o material, a data e o período. |
| Clique em "Criar ordem": aviso "Ordem de coleta criada"; o cartão "#9" na coluna "Agendada", com "Manhã", "Jair Lopes" e "GHT7B19". [BACKEND: rpc `get_next_collection_order_number` (9) + insert em `collection_orders` (status agendada, origem interna) + evento de criação] | Criar ordem. Pronto: a ordem nove já está agendada, com o Jair e o caminhão três quartos. |
| A câmera fica no cartão. | Motorista e veículo também podem ficar pra depois. Quem quiser exigir os dois antes de agendar tem a opção nas Configurações. |

### cap06 · Acompanhar até concluir (vinheta: ACOMPANHAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap05`); no cartão "#8" ("Agendada", Depósito Irmãos Siqueira), clique em "A caminho": aviso "Status alterado para A caminho"; o cartão vai para a coluna "A caminho". [BACKEND: rpc `change_collection_order_status` (agendada → a_caminho) + evento] | O caminhão saiu. O Edson foi trocar a caçamba do Depósito Irmãos Siqueira, então eu clico em A caminho, e o cartão anda pra próxima coluna. |
| No cartão "#8", clique em "Preencher": a tela "Ordem #8", com "Fornecedor" Depósito Irmãos Siqueira, "Endereço", "Agendamento" "10/11/2026 · Manhã", "Frota" "Edson Moura · FKD2E41" e "Material estimado". [BACKEND: o robô concede a geolocalização com uma coordenada fictícia perto do endereço; insert em `collection_driver_locations`; a câmera não para no aviso de localização] | Pra fechar o serviço, o botão é o Preencher. Abre a tela da ordem, com tudo o que foi combinado. |
| No bloco "Equipamentos", parte "Recolhi": "Tipo de equipamento" → "Caçamba 5 m³"; "Unidade" → "Caçamba 03" (só as que estão com o parceiro); "Adicionar": a linha "Caçamba 5 m³ — Caçamba 03". | No bloco Equipamentos, eu digo o que aconteceu com as caçambas. O Edson recolheu a Caçamba 03, cheia de ferro. |
| Parte "Entreguei": "Tipo de equipamento" → "Caçamba 5 m³"; "Unidade" → "Caçamba 05" (só as que estão na base); "Adicionar": a linha "Caçamba 5 m³ — Caçamba 05". | E deixou a Caçamba 05 vazia no lugar. Nessa lista só aparecem as que estão na base. |
| Clique em "Concluir coleta": aviso "Status alterado para Concluída"; a tela passa ao relatório "Relatório de Coleta 8", com o selo da etapa. [BACKEND: rpc `change_collection_order_status` (a_caminho → coletada, `p_equipment_lines`: recolhido Caçamba 03, entregue Caçamba 05): `completed_at`, evento e as duas `collection_equipment_movements` com `collection_order_id`; edge `collection-report`] | Concluir coleta. Pronto: a ordem fechou, e a tela já mostra o relatório da coleta. |
| A câmera fica no relatório. | Uma dica: concluir a coleta fecha o serviço, e só. O ferro que chegou entra no estoque quando você registra a compra, na tela de compra ou num Ticket de Pesagem. |
| Clique em "Voltar às ordens": o cartão "#8" em "Concluídas", com o botão "Relatório"; clique no corpo do cartão: janela "Ordem #8", "Concluída", "Interna". | De volta ao quadro, a ordem oito está em Concluídas. Clicando no cartão, abre a ficha dela. |
| A câmera desce a "Equipamentos movimentados": "Recolhido · Caçamba 5 m³ (Caçamba 03)" e "Entregue · Caçamba 5 m³ (Caçamba 05)". | Aqui ficam as caçambas que andaram nessa coleta. |
| A câmera desce ao "Histórico": a criação ("Agendada", 05/11), "Agendada → A caminho" e "A caminho → Concluída", com data e hora. [TESTAR: o evento de criação da ordem 8 na semente] | E o Histórico guarda cada mudança de etapa, com a data e a hora. Assim dá pra saber o que aconteceu com cada coleta. |

### cap07 · A coleta pedida pelo portal (vinheta: PORTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap06`). [ILUSTRAÇÃO: os dois lados do pedido: à esquerda, um navegador genérico com o portal do parceiro e o botão "Solicitar coleta"; à direita, o quadro da Recicla Vale com a coluna "Solicitada"; uma seta leva o pedido para a direita e outra volta com "Agendada"] | E quando o próprio parceiro pede? Ele usa o portal, o link que a Recicla Vale mandou pra ele. Do outro lado, o pedido cai no quadro pra aprovação. |
| Cartão discreto: "Portal do Cliente". | Pedir pelo portal depende também do Portal do Cliente no plano. |
| Segunda janela, sem login: o portal da Cooperativa Recomeço (`/portal/<token>`); clique na aba "Coletas": "Coletas", o botão "Solicitar coleta" e "Minhas coletas". [BACKEND: edge `entity-portal` (aba Coletas sem senha)] | Este é o portal da Cooperativa Recomeço, do jeito que ela vê. Na aba Coletas, ela acompanha as coletas dela e pede uma nova. |
| Clique em "Solicitar coleta": janela "Solicitar coleta" ("Peça a coleta do seu material. A empresa confirma o dia e o horário."); em "Material *" digita "PET prensado"; em "Quantidade estimada" digita "800 kg". [ZOOM: "Material *" e "Quantidade estimada" 800 kg] | A cooperativa tem oitocentos quilos de PET prensado pra sair. Ela preenche o material e a quantidade. |
| Em "Data preferida" digita 13/11/2026; em "Período" escolhe "Tarde"; o "Endereço da coleta" já vem do cadastro. | Escolhe o dia que prefere, sexta, e o período da tarde. O endereço já vem do cadastro. |
| Clique em "Solicitar coleta": aviso "Solicitação enviada (#10)"; o pedido aparece em "Minhas coletas". [BACKEND: edge `collection-request` (antecedência e dias aceitos conferidos; "Exigir aprovação da solicitação" ligado → status solicitada; número 10; aviso em `user_notifications`)] | Solicitar coleta. O pedido saiu, com o número dez. |
| De volta à janela do sistema (o robô recarrega a tela "Frota" fora do vídeo para o menu atualizar; a consulta das solicitações não vistas só revalida a cada 60 s): o menu "Coletas & Logística" com o ponto vermelho; clique em "Ordens de Coleta": [TESTAR: o ponto aparece depois de recarregar e some ao abrir o quadro] na "Solicitada", o cartão "#10" com "via portal", "Cooperativa Recomeço", "PET prensado — 800 kg", "13/11/2026 · Tarde", "Solicitada em: 10/11/2026 ..." e os botões "Aprovar" e "Recusar". | Agora, do lado da Recicla Vale. O menu ganhou um pontinho vermelho de aviso. E na coluna Solicitada está o pedido da cooperativa, marcado como via portal. |
| A câmera fica nos botões "Aprovar" e "Recusar". | Quem decide é a Recicla Vale. Dá pra aprovar ou recusar, e na recusa você escreve o motivo, que fica no histórico da ordem. |
| Clique em "Aprovar": janela "Agendar coleta" ("Ordem #10 — informe a data e a janela da coleta."), "Data da coleta *" com 13/11/2026 e "Janela *" com "Tarde". | Aprovar. A data e a janela vêm do pedido, mas quem confirma é você. |
| Clique em "Agendar": aviso "Status alterado para Agendada"; o cartão "#10" vai para "Agendada". [BACKEND: rpc `change_collection_order_status` (solicitada → agendada, 13/11, tarde)] | Agendar. Pronto: a coleta da cooperativa está marcada pra sexta à tarde. |

### cap08 · Veículos e motoristas (vinheta: FROTA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap07`); menu "Coletas & Logística" → "Frota": abas "Veículos" e "Motoristas"; em "Veículos" ("Mesma frota usada na pesagem de compra/venda."), a lista "Veículos da frota" com EZR4C63, FKD2E41 e GHT7B19. | Quem faz tudo isso é a frota. Em Frota ficam os veículos e os motoristas, os mesmos da pesagem de compra e venda. |
| Clique em "FKD2E41": o detalhe com a placa no modelo Mercosul, "Caminhão truck" e "Capacidade operacional". [ZOOM: "Tara" 9.200 kg e "Capacidade" 14.000 kg] | No caminhão truck, a ficha mostra a tara e a capacidade. |
| [ILUSTRAÇÃO: tara, bruto e líquido: um caminhão vazio numa balança de pátio, "tara 9.200 kg"; o mesmo caminhão carregado de sucata, "bruto"; a diferença acende como "líquido", o peso do material] | A tara é o peso do caminhão vazio. Carregado, ele pesa mais na balança, e essa diferença é o peso do material. |
| Clique em "Novo veículo": janela "Novo veículo"; em "Placa *" digita FVL8A52 (o desenho da placa aparece embaixo); em "Descrição / Apelido" digita "Caminhão poliguindaste". | A Recicla Vale comprou um caminhão poliguindaste, o que leva e busca caçamba. Em Novo veículo, eu digito a placa e um apelido. |
| Em "UF de licenciamento" escolhe "SP"; em "Tipo" escolhe "Veículo único (truck, toco, utilitário)"; em "Tipo de rodado" escolhe "Toco" (o que passar da fala vai acelerado). | Os dados de transporte servem pros documentos de transporte. Aqui, São Paulo, veículo único e toco. |
| Em "Tara (kg)" digita 7100 e em "Capacidade (kg)" digita 8500. [ZOOM: "Tara (kg)" 7100 e "Capacidade (kg)" 8500] | A tara dele é sete mil e cem quilos, e a capacidade, oito mil e quinhentos. |
| Clique em "Cadastrar": aviso "Veículo cadastrado"; o FVL8A52 na lista. [BACKEND: insert em `vehicles`] | Cadastrar. Pronto, o poliguindaste já está na frota. |
| Clique na aba "Motoristas": "Motoristas", a lista com Edson Moura, Jair Lopes e Tiago Freitas; clique em "Novo motorista": janela "Novo motorista". | Agora o motorista dele. Na aba Motoristas, clico em Novo motorista. |
| Em "Nome *" digita "Rogério Batista"; em "CPF" digita 463.718.205-08; em "Telefone" digita (12) 90000-4417 (o que passar da fala vai acelerado). | O Rogério Batista foi contratado pro poliguindaste. Nome, CPF e telefone. |
| Em "CNH" digita 04581273671; em "Categoria" escolhe "C"; em "Validade da CNH" digita 18/06/2030. [ZOOM: "CNH", "Categoria" e "Validade da CNH"] | E a carteira de motorista, a CNH: o número, a categoria C, que é a de caminhão, e a validade. |
| Clique em "Cadastrar": aviso "Motorista cadastrado"; Rogério Batista na lista. [BACKEND: insert em `drivers`] | Cadastrar. Agora ele já pode ser escalado nas ordens. |

### cap09 · As caçambas e onde estão (vinheta: EQUIPAMENTOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap08`); menu "Coletas & Logística" → "Equipamentos" ("Caçambas, bags, caixas e paletes em campo"), com as abas "Equipamentos" e "Movimentações". | E as caçambas. Elas ficam em Equipamentos, junto com bags, caixas e paletes. |
| A câmera vai a "Tipos de equipamento": "Caçamba 5 m³" ("Uma a uma", 5) e "Bag 1 m³" ("Por quantidade", 40). | Primeiro vem o tipo. A caçamba é uma a uma: cada uma tem número e lugar próprios. O bag é por quantidade: só interessa quantos tem em cada lugar. |
| A câmera desce a "Unidades identificáveis": a lista com Caçamba 01 a Caçamba 05, o tipo, o lugar ("Minha base"; a Caçamba 05 com "Depósito Irmãos Siqueira") e "OK". | Embaixo ficam as caçambas, uma por uma. Repara: a Caçamba 05 está no Depósito Irmãos Siqueira, onde o Edson deixou hoje. |
| Clique em "Nova unidade": janela "Nova unidade" ("A posição atual vem das movimentações e não é editada neste formulário."); "Identificação *" Caçamba 06; "Tipo de equipamento *" "Caçamba 5 m³"; "Condição" "OK"; clique em "Cadastrar": aviso "Unidade cadastrada". [BACKEND: insert em `collection_containers`] | Chegou uma caçamba nova. Em Nova unidade, eu dou a identificação, Caçamba 06, e o tipo. Cadastrar. |
| Na lista, clique em "Caçamba 06": o detalhe com "Posição atual" "Sem movimentação" e "Ainda sem movimentação registrada". | Ela ainda não tem lugar, porque o lugar vem das movimentações. |
| Clique em "Movimentar": janela "Nova movimentação" ("Lançamento avulso de equipamento — de onde saiu pra onde foi."); o "De *" já vem em "Externo" ("Compra nova, perda ou baixa — entra ou sai do sistema rastreável.") e a Caçamba 06 já vem em "Equipamentos *"; em "Para *" clica em "Minha base"; clique em "Registrar": aviso "Movimentação registrada"; "Posição atual" "Minha base". [BACKEND: rpc `register_collection_equipment_movement`] | Clico em Movimentar. Ela veio de fora, de uma compra nova, então vai de Externo pra Minha base. Registrar. Pronto, a Caçamba 06 está na base. |
| [ILUSTRAÇÃO: o caminho da caçamba: a Caçamba 05 sai de "Minha base" pelo "Entreguei" de uma ordem e vai até o parceiro; enche de sucata; volta pelo "Recolhi" de outra ordem; ao lado, um atalho "Movimentar" para a mudança fora de coleta, como a compra da Caçamba 06; em cada seta, uma mão com a etiqueta "você registra"] | Uma dica: a caçamba só muda de lugar quando alguém registra. Na coleta, é o Entreguei e o Recolhi da ordem, que valem quando ela é concluída. Fora da coleta, é o Movimentar, aqui. |
| A câmera desce a "Onde tudo está agora": "Equipamentos", "Na base", "Em campo" e "Com parceiros", e a tabela "Identificação", "Tipo", "Lugar atual", "Desde" e "Condição". | Em Onde tudo está agora fica o resumo: quanto está na base, quanto está em campo e com quantos parceiros. |
| Clique na aba "Movimentações": as linhas de hoje, a Caçamba 03 e a Caçamba 05 com "Ordem 8" e a Caçamba 06 de "Externo" para "Minha base". | E a aba Movimentações guarda cada ida e volta, com a data e quem registrou. As da troca de hoje mostram a ordem oito. |

### cap10 · O relatório das coletas (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap09`); menu "Coletas & Logística" → "Relatório" ("Indicadores e histórico das coletas"); "Período" em "Este mês": "Total de coletas" 4, "Concluídas" 1, "Canceladas" 0 e "Taxa de conclusão" 25%. | No fim do mês, o relatório. Ele abre no mês atual, com o total de coletas, as concluídas, as canceladas e a taxa de conclusão. |
| Em "Período" escolhe "Mês passado": "Total de coletas" 6, "Concluídas" 5, "Canceladas" 1 e "Taxa de conclusão" 100%. [ZOOM: os quatro números de outubro] | Em outubro foram seis coletas: cinco concluídas e uma cancelada. E a taxa de conclusão deu cem por cento. |
| [ILUSTRAÇÃO: a conta da taxa: seis cartões de coleta; o cancelado desliza para fora; sobram cinco, todos com o selo "Concluída": 5 de 5, 100%] | Uma dica: a coleta cancelada sai da conta. Das cinco que ficaram, as cinco foram concluídas. |
| De volta à tela: "Por status" e as tabelas "Por motorista", "Por veículo" e "Por parceiro". | Embaixo, as coletas por status, por motorista, por veículo e por parceiro. Dá pra ver quem rodou mais e onde a Recicla Vale mais busca. |
| A câmera vai ao seletor "Período". | Uma dica: cada coleta entra no mês em que foi concluída. A que ainda não foi conta pelo dia agendado, e a que não tem data, pelo dia em que foi pedida. |

### cap11 · As regras das coletas (vinheta: CONFIGURAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `t12/apos-cap10`); menu "Coletas & Logística" → "Configurações" ("Ajuste a numeração, as janelas e as regras do portal de coletas"); a câmera no bloco "Operação". | Por último, as regras. Em Configurações, o primeiro bloco é o da operação. |
| Em "Prefixo da numeração" ('Ex.: "COL-"') digita COL- e sai do campo: aviso "Prefixo da numeração salvo". | O Prefixo da numeração vai na frente do número de cada ordem. Aqui eu coloco um prefixo de coleta, e as ordens passam a aparecer com ele na frente. |
| A câmera vai a "Janelas de coleta oferecidas" ("Manhã", "Tarde" e "Dia todo", marcadas) e a "Exigir motorista e veículo para agendar" (desligado). | Nas Janelas de coleta oferecidas, você escolhe os períodos que aparecem pra agendar. E aqui dá pra exigir motorista e veículo antes de agendar. |
| A câmera desce ao bloco "Portal e solicitações": "Exigir aprovação da solicitação" (ligado). | No bloco do portal, o Exigir aprovação faz o pedido do parceiro esperar na coluna Solicitada, como o da cooperativa. Desligado, ele já entra agendado. |
| Em "Antecedência mínima (horas)" digita 24 e sai do campo: aviso "Antecedência mínima salva"; a câmera passa por "Dias aceitos para coleta" ("Seg" a "Sáb" marcados, "Dom" não). | A Antecedência mínima diz com quantas horas o parceiro precisa pedir: coloco vinte e quatro. E nos Dias aceitos, ele pede de segunda a sábado. |
| [ILUSTRAÇÃO: as regras só na porta do portal: duas portas para o quadro; a do portal, por onde entra o pedido do parceiro, tem um filtro com "24 h" e "seg a sáb"; a da Recicla Vale, por onde o operador cria a ordem, passa direto, até para hoje] | Uma dica: essas regras valem só pro que o parceiro pede pelo portal. Aqui dentro, a Recicla Vale agenda pra qualquer dia, até pra hoje. |

### cap12 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o quadro (cap02) e a "Nova ordem de coleta" com as três etapas (cap03 a cap05). | Pronto! Recapitulando: a gente conheceu o quadro e criou a coleta da Auto Peças Vale Forte, com data, período, motorista e caminhão. |
| Montagem rápida: "A caminho", o "Recolhi" e o "Entreguei" e o "Concluir coleta" (cap06). | Mandou o caminhão pro Depósito Irmãos Siqueira, registrou a troca de caçamba e concluiu a coleta, com o histórico de cada etapa. |
| Montagem rápida: o "Solicitar coleta" do portal e o "Aprovar" (cap07). | Recebeu o pedido da cooperativa pelo portal e aprovou. |
| Montagem rápida: "Novo veículo", "Novo motorista" (cap08) e "Nova unidade" (cap09). | Cadastrou o poliguindaste, o motorista novo e a Caçamba 06, e viu onde cada caçamba está. |
| Montagem rápida: o "Relatório" e as "Configurações" (cap10 e cap11). | E conferiu o relatório do mês e ajustou as regras do portal. |
| Cartão "Próximo: Produção"; cartela final. | No próximo tutorial, a gente transforma o que entrou no pátio em produto de maior valor. Até lá! |
