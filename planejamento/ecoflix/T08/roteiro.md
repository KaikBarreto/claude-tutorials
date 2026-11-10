# Roteiro T8 · Ticket de Pesagem

Pronto para o ensaio e a voz (sem etapa de aprovação). Coluna Fala = narração (voz Kaik Barreto), na grafia da legenda;
a grafia de pronúncia vai em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera fica, com os rótulos
como no código (`T08/inventario.md`, 1.59.154).

- **Título:** Ticket de Pesagem
- **Antes:** Comprar e vender sucata (T7)
- **Próximo:** Pedidos e histórico do caixa (T9)
- **Vinhetas (áreas):** TICKET · TICKET · PESAGEM · PESAGEM · PESAGEM · ABAS · VALORIZAR · COMPROVANTE · VALORIZAR ·
  RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~10 min (1.242 palavras de fala, ~8 min a 2,6 palavras/s, mais 10 vinhetas, a digitação nas
  janelas, a aba do PDF e as ilustrações); alvo da fonte, 11 min.
- **Gravação:** computador 1280×800, logado como Rafael Nogueira; `FAKE_NOW=2026-11-10T08:30:00-03:00`; EcoTray falso
  ligado como no fim do T5 ("Balança do pátio" com 0 kg), sem cena de Windows. Cada capítulo parte de um navegador novo
  com a semente do fim do anterior (`inicio`, `apos-cap02` a `apos-cap07`); quando o capítulo continua a criação, o
  `setup` reabre a aba por "Rascunhos abertos" fora do vídeo. Pesos digitados (decisão 1 do plano). O número "#58" vem
  de `get_next_ticket_number` (ajustar ao mundo; a fala não lê números de ticket nem de pedido).
- **Marcas:** `[BACKEND: ...]`, `[ILUSTRAÇÃO: ...]`, `[ZOOM: ...]` (dura a frase inteira), `[GRAVAÇÃO: ...]`,
  `[TESTAR: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Ticket de Pesagem". | (sem fala) |
| Dashboard, logado como Rafael Nogueira (semente `inicio`). A câmera fica no centro da tela. | Oi! Neste tutorial a gente resolve a situação clássica do pátio: o caminhão chegou, precisa pesar agora, mas o preço ainda não está fechado. |
| [ILUSTRAÇÃO: o caminhão de latinha da Cooperativa Recomeço sobe na balança; o visor marca "9.460 kg"; ao lado, uma etiqueta de preço com "R$ ?"; na palavra "depois", a etiqueta ganha um relógio.] | Na Recicla Vale Metais, a Cooperativa Recomeço mandou um caminhão de latinha, e o preço só vai ser combinado depois. |
| [ILUSTRAÇÃO, continua: o "9.460 kg" desce para um ticket; o "R$ ?" fica esperando ao lado.] | Com o Ticket de Pesagem, você registra o peso agora e resolve o valor depois. |
| Cartão discreto: "Antes: Comprar e vender sucata". | Se você ainda não viu o tutorial Comprar e vender sucata, dá uma olhada antes. [pause] Vamos ver quando usar o ticket. |

### cap01 · Quando usar o ticket (vinheta: TICKET)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), no Dashboard; no menu lateral, clique em "Materiais" e em "Ticket de Pesagem": cabeçalho "Ticket de Pesagem" ("Gerencie tickets de pesagem rodoviária"). | O ticket fica no menu Materiais, em Ticket de Pesagem. |
| [ILUSTRAÇÃO: Dois caminhos: em cima, "Compra direta": pesa, põe o preço, paga, e o estoque e o caixa mexem na hora; embaixo, "Ticket": pesa agora, o ticket fica salvo, depois "Valorizar" vira compra ou venda e só no "Finalizar" o estoque e o caixa mexem. Na palavra "fechado" acende o de cima; na palavra "depois", o de baixo.] | Com o preço fechado, você faz a compra direto, como no tutorial anterior. Com o preço em aberto, você pesa no ticket e transforma em compra ou venda depois. |
| [ILUSTRAÇÃO, continua: o ticket com o peso; o estoque e o caixa ficam cinza até o "Finalizar".] | Ticket salvo é peso registrado, e só. Nenhum quilo entra no estoque e nenhum centavo entra ou sai do caixa por causa dele. Isso só acontece quando o pedido que nasce dele é finalizado. |
| De volta à tela; zoom nas colunas "Aguardando valorização" (cabeçalho âmbar, com o cartão do #57) e "Valorizados" (verde). | Os tickets ficam aqui. Em Aguardando valorização, o que ainda espera o preço. Em Valorizados, o que já virou pedido. |
| Clique na aba "Pesagens avulsas": título "Pesagens Avulsas", "Nenhuma pesagem avulsa registrada" e o botão "Nova Pesagem Avulsa". | Na aba Pesagens avulsas fica outro caso: quem só quer saber o peso, como o caminhão de areia de um vizinho. |
| Zoom em "Nova Pesagem Avulsa", sem clicar; depois clique em "Tickets padrão". | A pesagem avulsa é só um comprovante de peso. Ela não vira pedido, não mexe no estoque, e o comprovante sai marcado sem valor comercial. |

### cap02 · Criar o ticket (vinheta: TICKET)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em "Ticket de Pesagem". Clique em "Novo Ticket de Pesagem": cabeçalho "Novo Ticket de Pesagem" ("Preencha o ticket. Use as abas para atender vários veículos."). | O caminhão da cooperativa chegou. Clico em Novo Ticket de Pesagem. |
| Zoom na barra de cima: "Modalidade" em "Ticket padrão", "Tipo" em "Compra" e "Valores" em "Sem valores". | Em cima ficam três chaves: ticket padrão; compra, porque a gente vai comprar a latinha; e sem valores, porque o preço ainda não fechou. |
| Zoom em "Com valores", sem clicar. | Quando o preço já está combinado, dá pra fazer o ticket com valores, e ele já guarda o preço de cada material. |
| Clique em "Selecionar fornecedor": janela "Selecionar Fornecedor" ("Buscar por nome, apelido, CPF/CNPJ ou telefone..."); digita "Recomeço" e clica em "Cooperativa Recomeço". [BACKEND: `suppliers` com a Cooperativa Recomeço] | O fornecedor é a Cooperativa Recomeço. |
| No card "Pesagem", em "Material" ("Escreva o nome ou código do material"), digita "latinha" e escolhe "Alumínio latinha". [BACKEND: com a balança ligada, "Quantidade (Kg)" pode receber "0,000" da Balança do pátio ao escolher o material; não atrapalha] | No card Pesagem, o material: alumínio latinha. |
| Em "Motorista" ("Digite ou busque o motorista") digita "Edson" e escolhe "Edson Moura"; em "Placa do Veículo" ("Digite ou busque a placa") escolhe "FKD2E41". [BACKEND: `drivers` e `vehicles` do mundo] | E, aqui dentro, o motorista e a placa. O Edson Moura e o caminhão dele já estão cadastrados, então é só escolher na lista. |
| Zoom na barra escura de abas, à direita: "Número" "#58", "Peso" "0 kg", "CLIENTE/FORNECEDOR" "Cooperativa Recomeço" e, embaixo, "Seu rascunho". | Do lado direito fica a aba deste ticket, com o número, o peso e o fornecedor. |

### cap03 · A primeira pesagem e o rascunho (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`: rascunho com a cooperativa, o Edson e a placa; o `setup` reabre a aba e escolhe "Alumínio latinha" fora do vídeo). Clique em "Pesagem avançada", embaixo de "Quantidade (Kg)": janela "Pesagem avançada" ("Registre pesagem dupla, tara, impureza e dados do transporte"). | O Edson sobe na balança com o caminhão cheio. A primeira pesagem vai na Pesagem avançada. |
| Em "1ª Pesagem" digita 9460: o "Peso Bruto (Kg)" mostra "9.460" e "= 1ª pesagem"; "Líquido (Kg)" "9.460". [ZOOM: "1ª Pesagem" e o "Peso Bruto (Kg)", com "= 1ª pesagem"] | Na primeira pesagem, nove mil quatrocentos e sessenta quilos. Por enquanto, ela conta como bruto. |
| Zoom no botão da balança dentro do campo "1ª Pesagem", sem clicar. | Com a balança ligada no EcoTray, o botão dentro do campo puxa esse peso sozinho. |
| Zoom na dica "Preencha 1ª e 2ª pesagem para o bruto, informe só a 1ª (conta como bruto) ou digite o bruto direto." | E a dica embaixo mostra os três jeitos: as duas pesagens, só a primeira, ou o bruto digitado direto. |
| Em "Como exibir no comprovante", marca "Completo" ("1ª e 2ª pesagem, bruto, tara, impureza e líquido."). | Em Como exibir no comprovante, eu marco Completo, pra sair a conta inteira no papel. |
| Clique em "Confirmar": em "Itens do Ticket (1)", "Alumínio latinha" com o peso 9.460; na aba, "9.460 kg". [BACKEND: o rascunho grava em `weighing_tickets` (`status` draft) 600 ms depois] | Confirmar. Agora o caminhão vai descarregar. |
| [ILUSTRAÇÃO: O rascunho: a aba do ticket com "Seu rascunho" e um tique de "salvo" que pisca a cada mudança; ao lado, um relógio anda enquanto o caminhão descarrega.] | E não precisa fazer mais nada: o ticket fica salvo sozinho, como rascunho, a cada mudança. |
| Zoom na aba: "#58" e "Seu rascunho". | Não existe um status de esperando a segunda pesagem. O ticket fica aqui, aberto, até o caminhão voltar. E esse número é só a previsão: o ticket ganha número quando é salvo. |
| Clique em "Voltar": a lista; zoom em "Rascunhos abertos" com "1"; clique: a criação volta com a aba da cooperativa e o item. | Mesmo saindo da tela, o rascunho continua lá, em Rascunhos abertos. |
| A câmera fica no item reaberto. | Uma dica: quando o rascunho é reaberto, confira o que já estava preenchido antes de salvar. |

### cap04 · Descarregar e a segunda pesagem (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`: o rascunho com o item de 9.460 kg; o `setup` reabre a aba). [ILUSTRAÇÃO: Entrada e saída: o caminhão cheio na balança, "1ª pesagem 9.460 kg"; ele descarrega a latinha no pátio; volta vazio, "2ª pesagem 6.380 kg"; na palavra "diferença", os "3.080 kg" da latinha se destacam entre as duas.] | O caminhão descarregou e voltou vazio pra balança. A diferença entre as duas pesagens é a latinha que ficou no pátio. |
| No item "Alumínio latinha", "Ações do item" (⋮) → "Adicionar tara / pesagem avançada": a janela abre com "Peso Bruto (Kg)" 9.460 e "1ª Pesagem" e "2ª Pesagem" vazias. | No item, em Adicionar tara, pesagem avançada. O peso da entrada está no bruto. |
| Em "1ª Pesagem" digita 9460; em "2ª Pesagem" digita 6380: o "Peso Bruto (Kg)" vira "3.080", com "|9.460 − 6.380|" embaixo; "Líquido (Kg)" "3.080". | A gente passa ele pra primeira pesagem e põe a segunda, com o caminhão vazio: seis mil trezentos e oitenta quilos. |
| [ZOOM: "Peso Bruto (Kg)" "3.080" e "|9.460 − 6.380|"] | Pronto: o bruto sai sozinho, a diferença das duas. Três mil e oitenta quilos de latinha. |
| Zoom em "Tara (Kg)", em branco. | A tara é o peso do que vem junto e não é material, como uma caçamba. Aqui o caminhão já saiu na segunda pesagem, então a tara fica em branco. |
| Clique em "Confirmar": aviso "Pesagem do item atualizada"; a linha mostra o peso 3.080. | Confirmar, e a pesagem do item está atualizada. |
| Clique na seta da linha "Alumínio latinha" ("Ver detalhes da pesagem"): abre o detalhe, com "1ª pesagem", "2ª pesagem" e "Bruto" (`components/order/WeighingDetailRow.tsx`). | Na linha, a setinha abre o detalhe, com as duas pesagens e o bruto. |

### cap05 · Impureza em porcentagem ou em quilos (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`; o `setup` reabre a aba). Em "Ações do item" → "Adicionar tara / pesagem avançada": agora a janela abre com "1ª Pesagem" 9.460, "2ª Pesagem" 6.380 e o bruto "3.080". | Falta a impureza. Na latinha sempre vem um pouco de sujeira e de água, e isso sai do peso. |
| Em "Impureza", clique em "%" e digita 2: embaixo aparece "= 61,6 Kg (sobre bruto − tara)". [ZOOM: "Impureza" com "2" e "= 61,6 Kg (sobre bruto − tara)"] | Aqui ela vai em porcentagem: dois por cento. O sistema mostra quanto isso dá: sessenta e um quilos e seiscentos. |
| Zoom no seletor "kg" e "%". | Se preferir, troca pra quilos e digita direto o peso da impureza. |
| [ILUSTRAÇÃO: A conta do líquido: "Bruto 3.080" menos "Tara 0" menos "Impureza 61,6" igual a "Líquido 3.018,4"; cada parcela entra na sua palavra.] | E o líquido fecha a conta: o bruto, menos a tara, menos a impureza. |
| [ZOOM: "Líquido (Kg)" "3.018,4"] | Três mil e dezoito quilos e quatrocentos. É esse peso que vale na compra. |
| Clique em "Confirmar": "Pesagem do item atualizada"; a linha mostra "Tara/Imp." 61,6. [BACKEND: o rascunho guarda `impurity_pct` 2 e `impurity_kg` 61,6] | Confirmar, e o ticket da cooperativa está pesado. |

### cap06 · Vários veículos ao mesmo tempo (vinheta: ABAS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`; o `setup` reabre a aba). [ILUSTRAÇÃO: dois caminhões na fila da balança, o truck da cooperativa e o 3/4 da Auto Peças; cada um puxa uma aba própria na tela, "#58" e "#59".] | Enquanto isso, chega o Jair Lopes, com o caminhão três quartos da Auto Peças Vale Forte, trazendo bateria. |
| Na barra de abas, clique em "+ Novo ticket": abre uma aba em branco ("#59", "Sem cliente/fornecedor"; a barra mostra "(2)"). | Cada caminhão ganha a sua aba. Em Novo ticket, abre uma aba em branco. |
| Na aba nova (o preenchimento pode ser acelerado na edição): "Selecionar fornecedor" → "Auto Peças Vale Forte"; "Material" → "Bateria automotiva"; "Motorista" → "Jair Lopes"; "Placa do Veículo" → "GHT7B19"; "Pesagem avançada": "1ª Pesagem" 5640 → "Confirmar". | Fornecedor, material, motorista, placa e a primeira pesagem: cinco mil seiscentos e quarenta quilos. |
| Clique na barra escura: a lista mostra "#58" "3.080 kg" "Cooperativa Recomeço" e "#59" "5.640 kg" "Auto Peças Vale Forte". [ZOOM: a lista das duas abas] | Na barra de cima, a gente troca de um caminhão pro outro. Cada aba guarda o seu rascunho, e nada se mistura. |
| Clique em "#58": volta o ticket da cooperativa. Clique em "Salvar Ticket de Pesagem": aviso "Ticket de pesagem salvo" e a janela "Ticket #58 salvo" ("O que deseja fazer com este ticket de pesagem?"), com "Imprimir comprovante", "Valorizar" e "Fechar". [BACKEND: RPC `finalize_weighing_ticket_v3` → `ticket_number` 58, `status` pending] | O ticket da cooperativa está pronto, então eu salvo. Agora sim, ele ganha o número de verdade. |
| Clique em "Fechar": fica a aba do Jair ("#59", "Auto Peças Vale Forte", "Seu rascunho"). | O valor a gente resolve depois. E a aba do Jair continua aberta, esperando ele descarregar. |
| Clique na barra escura: na lista de abas, zoom no "x" da aba do Jair, sem clicar (ele pede "Descartar este ticket?", com "Manter ticket" e "Descartar ticket"); fecha a lista. | Se alguém fechar uma aba no x, o sistema pergunta antes de descartar o ticket. |

### cap07 · Valorizar o ticket (vinheta: VALORIZAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), em "Ticket de Pesagem": em "Aguardando valorização", o cartão "Ticket #58" ("COMPRA", "Fornecedor: Cooperativa Recomeço", "Sem valores", "Alumínio latinha", "3.018,4 kg", "10/11/26 08:52"). | No fim do dia, o preço com a cooperativa fechou. É hora de valorizar: transformar o peso em pedido. |
| No cartão, "Ações" → "Valorizar". [BACKEND: `order_drafts` insert com o item e o preço da tabela principal, R$ 6,20] A tela vai para a Compra (`/compra`) com o rascunho: fornecedor "Cooperativa Recomeço", "Alumínio latinha", o peso, "Tara/Imp." 61,6, "Valor/Kg" 6,20 e o total. | Em Ações, Valorizar. O sistema abre uma compra já preenchida: a cooperativa, a latinha, o peso e a impureza. |
| [ZOOM: o "Valor/Kg" 6,20 e o total da linha, R$ 18.714,08] | O preço vem da tabela: seis e vinte o quilo. Dá dezoito mil setecentos e catorze reais e oito centavos. |
| Zoom na célula "Valor/Kg". | Se o preço combinado for outro, é só mudar o valor do quilo aqui, antes de finalizar. Num ticket de venda, abre uma venda do mesmo jeito. |
| [ILUSTRAÇÃO: o caminho: ticket, "Valorizar", compra em rascunho, "Finalizar", estoque e caixa; o estoque e o caixa só acendem no "Finalizar".] | Repara: até aqui, nada entrou no estoque e nada saiu do caixa. A compra está em rascunho, e o efeito só acontece quando ela for finalizada. |

### cap08 · Imprimir o comprovante (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`), em "Ticket de Pesagem"; no cartão "Ticket #58", "Ações" → "Ver comprovante": janela "Gerar comprovante do ticket" ("Escolha o formato do comprovante deste ticket de pesagem."), com "A4" ("Folha") e "Térmico" ("80mm"). | O motorista leva o comprovante do ticket. Em Ações, Ver comprovante, e o formato: Térmico, o cupom, ou A4, a folha. |
| Clique em "Térmico": abre a aba nova com o PDF do comprovante. [GRAVAÇÃO: gravar a aba nova] [ZOOM: a faixa "TICKET DE PESAGEM" / "NÃO VALORIZADO" e "Documento sem valor financeiro definitivo"] | Repara no papel: ticket de pesagem, não valorizado. É o comprovante do peso, ainda sem valor de compra. |
| [ZOOM: "Motorista: Edson Moura" e "Placa: FKD2E41", e as linhas "1ª pesagem", "2ª pesagem", "Bruto", "Impureza" (com "(2%)") e o peso líquido] | Com o modo Completo, sai a conta inteira: o motorista, a placa, as duas pesagens, o bruto, a impureza e o líquido. |
| De volta à aba do sistema: Configurações › "Integrações"; zoom em "Imprimir comprovante do Ticket de Pesagem" ("Envia o comprovante térmico direto pra impressora ao salvar um ticket"), desligada. | E se quiser que o cupom saia sozinho na impressora ao salvar cada ticket, ligue Imprimir comprovante do Ticket de Pesagem, em Configurações, Integrações. |
| [ILUSTRAÇÃO: Pesagens mescladas: duas linhas de ferro misto, "1.200 kg" e "800 kg", viram uma linha só, "2.000 kg", no comprovante; na palavra "Desmesclar", o botão "Desmesclar pesagens" separa as duas de novo.] | Uma dica: se o ticket tiver pesagens do mesmo material mescladas numa linha, o comprovante mostra só a soma. Pra conferir cada pesagem no papel, use o Desmesclar pesagens antes de imprimir. |

### cap09 · Quando o ticket sai da lista de pendentes (vinheta: VALORIZAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`), em "Ticket de Pesagem": o "Ticket #58" segue em "Aguardando valorização". [ZOOM: o cartão] | E quando o ticket sai de Aguardando valorização? Mesmo com a compra em rascunho, ele continua aqui. |
| "Ações" → "Valorizar": aviso "Estes tickets já tinham um pedido em aberto — retomando." ("Atualizado com os itens atuais do ticket (1 item, R$ 18.714,08)."); abre a mesma compra. [BACKEND: `order_drafts` reaproveitado (update)] | Valorizando de novo, o sistema retoma a mesma compra, sem duplicar. |
| Clique em "Finalizar": "Finalizar Pedido"; escolhe "Pix/Transferência" e a conta bancária principal; clique em "CONFIRMAR PAGAMENTO": "Compra registrada!" e "Pedido finalizado — voltando ao Ticket de Pesagem" (o meio pode ser acelerado na edição). [BACKEND: caixa do Rafael aberto; finalizar da compra do T7; o ticket vira `valorized` com `valorized_order_id`] [TESTAR: se abrir "Imprimir Comprovante", fechar antes da volta] | Finalizo como no tutorial anterior: Pix, e confirmar pagamento. Agora sim, a latinha entrou no estoque e o pagamento saiu da conta. |
| A tela volta sozinha para "Ticket de Pesagem": o "Ticket #58" está em "Valorizados", com "Valorizado pelo pedido #…". [ZOOM: "Valorizado pelo pedido #…"] | E o sistema volta sozinho pro Ticket de Pesagem. O ticket passou pra Valorizados, com o número da compra. |
| Clique no botão "Lista" (ao lado da busca): a tabela com o selo "Valorizado" (verde) no #58 e "Aguardando valorização" (âmbar) no #57; depois clique em "Filtros": "Status" com "Aguardando valorização", "Valorizado" e "Cancelado"; fecha o painel e volta ao "Kanban". | Na lista, cada ticket mostra a situação. São três: Aguardando valorização, em amarelo; Valorizado, em verde; e Cancelado, em vermelho. |
| Zoom em "Rascunhos abertos" com "1". | E o ticket do Jair continua no rascunho. Ele entra na lista quando for salvo. |

### cap10 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: "Novo Ticket de Pesagem" com a cooperativa, o Edson e a placa. | Pronto! Recapitulando: a gente criou o ticket da cooperativa com o fornecedor, o material, o motorista e a placa. |
| Montagem rápida: a "1ª Pesagem", "Rascunhos abertos" e o "Peso Bruto (Kg)" 3.080. | Fez a primeira pesagem na entrada, viu o rascunho salvo sozinho e fez a segunda na saída, com o bruto saindo sozinho. |
| Montagem rápida: a impureza "2" com "%", as duas abas e "Ticket #58 salvo". | Aplicou a impureza em porcentagem, atendeu um segundo caminhão em outra aba e salvou o ticket. |
| Montagem rápida: a compra preenchida, o comprovante "NÃO VALORIZADO" e a coluna "Valorizados". | Valorizou o ticket, que virou uma compra já preenchida, imprimiu o comprovante e viu o ticket ir pra Valorizados quando a compra foi finalizada. |
| Cartão "Próximo: Pedidos e histórico do caixa"; cartela final. | No próximo tutorial, a gente acha e corrige um pedido antigo. Até lá! |
