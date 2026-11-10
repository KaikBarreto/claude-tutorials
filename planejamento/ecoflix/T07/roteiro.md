# Roteiro T7 · Comprar e vender sucata

Roteiro pronto para o ensaio gravado e, depois, para a voz (sem etapa de aprovação). Coluna Fala = texto da narração na grafia da
legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py` (gerado desta coluna, uma linha do texto por linha da
tabela). Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código da 1.59.154
(`T07/inventario.md`). Mundo, sementes e gravação: `T07/plano.md`.

- **Título:** Comprar e vender sucata
- **Antes:** Caixa: abrir, fechar e o cofre (T6)
- **Próximo:** Ticket de Pesagem (T8)
- **Vinhetas (áreas):** CAIXA · FORNECEDOR · PREÇO · BALANÇA · PESAGEM · VALOR · PAGAMENTO · COMPROVANTE · VENDA · SEM INTERNET ·
  RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~20 min de vídeo (2.660 palavras de fala, ~17 min de voz a 2,6 palavras/s, mais 16 vinhetas, as
  ilustrações e as ações sem fala; alvo da fonte: 22 min)
- **Logado:** Rafael Nogueira (MASTER, vê lucro), desktop 1280×800, tema claro, `FAKE_NOW=2026-11-10T08:30:00-03:00`.
- **Marcas:** `[BACKEND: ...]` o que o backend falso ou o EcoTray falso ainda não têm · `[ZOOM: ...]` zoom que dura a frase inteira
  (≥ 2,5 s, nunca zoom em cima de zoom) · `[ILUSTRAÇÃO: ...]` desenho por código no estilo da marca · `[CENA WINDOWS: ...]` cena
  simulada do Windows com o EcoTray do código · `[TESTAR: ...]` o robô confere antes de gravar · `[handoff: ...]` texto do app
  para o time (a fala não depende dele).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Comprar e vender sucata". | (sem fala) |
| [ILUSTRAÇÃO: o dia no pátio, em passos que entram com as palavras da fala: "pesar" (uma carroça com sucata em cima da balança, visor 12,4 kg), "comprar" (um pedido com linhas de material), "pagar" (notas de dinheiro e o símbolo do Pix), "comprovante" (um cupom saindo); por último, "vender" (um caminhão carregado saindo do portão). Fundo claro, Montserrat, verde #50D088.] | Oi! Neste tutorial a gente vai fazer o que a Recicla Vale Metais faz o dia inteiro: pesar, comprar, pagar e imprimir o comprovante. E depois vender. |
| A ilustração fecha no visor da balança, com uma seta até um computador. | A sucata chega no portão e vai pra balança. Daí o peso tem que virar valor certo e pagamento na hora, sem anotar nada no papel. |
| Dashboard, logado como Rafael Nogueira; cartão discreto "Antes: Caixa: abrir, fechar e o cofre". | Se você ainda não viu o tutorial Caixa: abrir, fechar e o cofre, dá uma olhada antes. É do caixa aberto que saem as compras e as vendas. [pause] Vamos lá. |

### cap01 · Onde ficam a compra e a venda (vinheta: CAIXA)

| Tela | Fala |
| --- | --- |
| No menu lateral, clique em "Financeiro" e em "Caixa": o caixa do Rafael aberto, com os botões "Nova Compra" (azul), "Nova Venda" (verde), "Nova Despesa" e "Nova Receita". | Tudo começa no caixa. No menu, Financeiro, Caixa. Com o caixa aberto, aparecem os botões Nova Compra e Nova Venda. |
| Clique em "Nova Compra": abre "Nova Compra", com o selo do caixa ("Caixa #… · Você") e o link "Voltar para o caixa". [ZOOM: o selo do caixa] | Clicando em Nova Compra, a tela abre já ligada ao seu caixa. É o selo aqui em cima. |
| Clique em "Voltar para o caixa"; clique numa área vazia e tecla Shift+V: abre "Nova Venda". | Também dá pra ir pelo teclado. Shift+C abre a compra, e Shift+V abre a venda. |
| Clique numa área vazia e Ctrl+K: abre a busca "Buscar páginas, clientes, fornecedores, materiais, funcionários..."; a câmera vai a "Ações Rápidas" ("Nova Compra", "Nova Venda", "Abrir Caixa"); clique em "Nova Compra". | E o Ctrl+K abre a busca em qualquer tela. Em Ações Rápidas estão a Nova Compra e a Nova Venda. |
| Tour na "Nova Compra": a câmera passa por "Fornecedor" e "Tabela de Preços" (em cima), pelo cartão preto "Pesagem" (à esquerda), por "Itens do Pedido" com "Nenhum item adicionado" (à direita) e pelo rodapé: "Total da Compra", "Opções avançadas", "Cancelar" e "Finalizar". | Na tela da compra, em cima ficam o fornecedor e a tabela de preços. À esquerda, o cartão da pesagem, por onde entra cada material. À direita, os itens do pedido. E embaixo, o total e o botão Finalizar. |

### cap02 · Escolher o fornecedor (vinheta: FORNECEDOR)

| Tela | Fala |
| --- | --- |
| Clique em "Selecionar fornecedor": abre "Selecionar Fornecedor", com a busca "Buscar por nome, apelido, CPF/CNPJ ou telefone..." e a lista; a câmera para na primeira opção, "Não informado". | Primeiro, quem está vendendo pra gente. Clicando no fornecedor, abre a lista, e a primeira opção é Não informado. |
| Zoom em "Não informado". | Ela serve pro pedido avulso, de quem passou uma vez e não quer cadastro. O estoque e o caixa mexem do mesmo jeito. |
| [ILUSTRAÇÃO: pedido com fornecedor × "Não informado". À esquerda, um pedido "Fornecedor: Aparecida Ramos" entra numa ficha com "Histórico" e "Saldo". À direita, um pedido "Não informado" fica de fora da ficha, e o quadrado "Saldo do Fornecedor" aparece apagado. A ficha entra com "histórico"; o quadrado apagado, com "saldo".] | Só que esse pedido não entra no histórico nem no portal de ninguém. Uma dica: com Não informado, o pagamento não pode ir pro saldo, que é o fiado. Pra isso, o pedido precisa de um fornecedor. |
| Na lista, mouse sobre o indicador âmbar "2" da linha "Valdir Pereira": balão "Cadastro incompleto", com "CPF/CNPJ não informado", "Endereço não informado" e "Use o menu ao lado para completar o cadastro.". [BACKEND: Valdir sem CPF e sem endereço, com "Não possui telefone"] [ZOOM: o indicador e o balão] | Repara que alguns nomes têm um aviso com número. Ele mostra o que falta no cadastro: no Valdir, o CPF e o endereço. É só um lembrete, e não trava o pedido. |
| A câmera fica no balão (sem linha de telefone). | O Valdir não tem telefone, e isso não aparece aqui porque o cadastro dele está marcado com Não possui telefone. Uma dica: quando a pessoa não tem telefone mesmo, marque essa opção em Editar, em vez de inventar um número. |
| Mouse sobre o alfinete da linha "Aparecida Ramos": "Fixar como padrão" (sem clicar). | E o alfinete do lado fixa um fornecedor como padrão, pra ele já vir escolhido nos próximos pedidos. |
| Digita "Moreira" na busca: "Nenhum resultado encontrado.". | Hoje chegou um carroceiro novo, o Zé Moreira. Na busca, ninguém. Então a gente cadastra ele agora. |

### cap03 · Cadastrar o fornecedor na hora (vinheta: FORNECEDOR)

| Tela | Fala |
| --- | --- |
| Clique no "+" ao lado da busca: abre "Novo Fornecedor", na aba "Dados de Contato". | Sem sair da compra, é só clicar no mais. Abre o mesmo cadastro da tela de Clientes e Fornecedores. |
| Em "Nome *", digita "José Carlos Moreira"; em "Pessoa de Contato ou Apelido", "Zé Moreira"; em "Telefone", "(12) 90000-4471". | O único campo obrigatório é o nome: José Carlos Moreira. No apelido, Zé Moreira, que é como o pátio chama ele. E o telefone. |
| Em "Chave PIX", digita "(12) 90000-4471"; a câmera passa por "Tabela de Preços Padrão" (fica a padrão) e por "Também é cliente" (desmarcado). | A chave Pix dele é o telefone. Aqui também dá pra escolher a tabela de preços do fornecedor e marcar se ele também é cliente. |
| Clique em "Salvar": aviso "Fornecedor cadastrado com sucesso!"; o campo "Fornecedor" mostra "José Carlos Moreira". [BACKEND: `INSERT` em `suppliers`] | Salvar. Pronto: o Zé já vem escolhido no pedido. O CPF e o endereço, você completa depois, com calma, na tela de Clientes e Fornecedores. |

### cap04 · Qual preço vale (vinheta: PREÇO)

| Tela | Fala |
| --- | --- |
| Clique em "Tabela de Preços": a lista mostra a tabela padrão, com a estrela, e "Tabela Depósitos"; Esc (fica a padrão). | Agora o preço. Do lado do fornecedor fica a tabela de preços do pedido. Ela vem do cadastro do fornecedor, e quando ele não tem uma, vem a principal, a da estrela. |
| [ILUSTRAÇÃO: a hierarquia do preço. Três degraus, de cima pra baixo: "Preço especial" (o combinado com aquele cliente ou fornecedor), "Tabela de preços do pedido" e "Preço do material". Uma seta desce e para no primeiro degrau que tem preço. Cada degrau acende com a palavra dele na fala.] | Quando você escolhe o material, o sistema procura o preço nesta ordem. Primeiro, o preço especial combinado com aquele fornecedor. Depois, a tabela do pedido. E por último, o preço do próprio material. |
| A ilustração mostra os dois avisos reais da tela: "Preço especial aplicado para …" e "Preço da tabela aplicado para …". | A tela sempre avisa quando valeu um preço especial ou o da tabela. E o preço é uma sugestão: dá pra mudar na hora. |
| De volta à tela: "José Carlos Moreira" e a tabela padrão. | O Zé é novo e está na tabela principal, então vale o preço de cada material. Uma dica: escolha o fornecedor antes dos materiais, porque o preço entra na hora em que você escolhe o material. |

### cap05 · O peso da balança (vinheta: BALANÇA)

| Tela | Fala |
| --- | --- |
| Clique em "Material", digita "cobre mi" e escolhe "Cobre misto": o preço do quilo vem 36,00; no topo do cartão "Pesagem", o visor da balança marca 12,4 kg, e "Quantidade (Kg)" se preenche sozinha com 12,400, com o selo "AO VIVO" piscando. [BACKEND: EcoTray falso, balança "Balança", estável em 12,4 kg, leitura contínua ligada; tabela padrão sem item explícito, então sem aviso de preço] [ZOOM: o visor, "Quantidade (Kg)" e "AO VIVO"] | Agora o primeiro material: o cobre misto do Zé. O preço veio do cadastro do material: trinta e seis reais o quilo. E repara no peso: doze quilos e quatrocentos, direto da balança. |
| [CENA WINDOWS: área de trabalho genérica, sem logo de terceiros; o navegador com a tela da compra e, ao lado, a janela do EcoTray do código (`ecotray/dashboard.py`): "EcoTray", "Ponte Desktop — Balança & Impressora", abas "Integrações" e "Logs", cartão "Conectado e operando" com "ws://127.0.0.1:8053", seção "Balanças" com a linha "● Balança", "12,4 kg", "conectada", "✓ padrão". O peso do EcoTray e o do campo batem. Uns 6 s.] | Quem traz esse peso é o EcoTray, o programa que fica aberto no computador, ligado na balança. O selo AO VIVO quer dizer que o peso está chegando agora. |
| De volta à tela: zoom no botão azul da balança, dentro do campo, e no ponto azul à esquerda do número (sem clicar). [handoff H2: o balão do botão mostra "12.400 kg", com ponto; sem zoom nele] | O botão azul dentro do campo puxa o peso de novo, quando você precisar. A leitura da balança faz parte do módulo de balança, que depende do plano contratado. Sem ele, é só digitar o peso. |
| Zoom em "Estoque Disponível" e em "Valor Total do Item" (R$ 446,40); clique em "Incluir Item": a linha "Cobre misto" entra em "Itens do Pedido (1)", com o ponto azul do peso da balança. [ZOOM: "Valor Total do Item"] | Embaixo, o estoque disponível desse material e o valor do item: quatrocentos e quarenta e seis reais e quarenta. Incluir Item, e o cobre entra na lista. |
| Material "Alumínio latinha" (6,20); a balança marca 21,6 kg e "Quantidade (Kg)" vem 21,600; clique em "Tara/Imp." e digita "0,6". [BACKEND: estável em 21,6 kg] [ZOOM: "Quantidade (Kg)" e "Tara/Imp."] | Agora a latinha, em três sacos de ráfia: vinte e um quilos e seiscentos. Cada saco pesa duzentos gramas. Então, no campo Tara/Imp., vai zero vírgula seis. |
| Zoom em "Valor Total do Item" (R$ 130,20); clique em "Incluir Item": "Itens do Pedido (2)", com a coluna "Tara/Imp." e o 0,6. [handoff H1: a coluna "Peso Líquido" mostra 21,6, que é o bruto] | A balança nunca preenche esse campo sozinha: a tara é você que informa. O valor sai pelo peso sem os sacos: vinte e um quilos, a seis e vinte, dá cento e trinta reais e vinte. Incluir Item. |

### cap06 · Tara, impureza e dupla pesagem (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: tara, impureza e peso líquido. 1) Um saco de latinha na balança, visor 21,6 kg; o saco se destaca como "Tara 0,6 kg". 2) Um monte de ferro com terra e pedaços de borracha: "Impureza", em kg ou em %. Entram com "tara" e "impureza".] | Antes de seguir, três palavras do pátio. Tara é o peso do que não é material, como o saco, o tambor ou a caçamba. Impureza é a sujeira que vem junto: terra, borracha, plástico. |
| A ilustração monta a conta "Bruto − Tara − Impureza = Líquido" e leva o "Líquido" até uma caixa "Estoque". | E o peso líquido é o que sobra: o bruto, menos a tara, menos a impureza. É pelo líquido que o material entra no estoque. |
| [ILUSTRAÇÃO: a dupla pesagem da carroça. A carroça cheia na balança, visor 412 kg ("1ª pesagem"); a carga desce; a carroça vazia, visor 96 kg ("2ª pesagem"); a diferença, 316 kg, é o bruto da carga.] | E quando a sucata vem numa carroça ou num caminhão, tem a dupla pesagem. Pesa cheio, descarrega e pesa vazio. A diferença é a carga. |
| Na tela: Material "Ferro misto" (0,75), com a balança em 0,0; clique no botão preto "Pesagem avançada": abre "Pesagem avançada" ("Registre pesagem dupla, tara, impureza e dados do transporte"). [BACKEND: balança em 0,0 kg] | O ferro do Zé veio na carroça. Escolho o ferro misto e clico em Pesagem avançada, logo embaixo do peso. |
| Com a carroça cheia, clique no botão da balança dentro de "1ª Pesagem": 412,000. Com a carroça vazia, clique no de "2ª Pesagem": 96,000. "Peso Bruto (Kg)" mostra 316, com "\|412 − 96\|" embaixo. [BACKEND: estável em 412,0 kg e depois em 96,0 kg] [ZOOM: "1ª Pesagem", "2ª Pesagem" e "Peso Bruto (Kg)"] | Carroça cheia na balança: primeira pesagem, quatrocentos e doze quilos. Carroça vazia: segunda pesagem, noventa e seis. O peso bruto sai sozinho: trezentos e dezesseis quilos. |
| Em "Impureza", clique em "%" e digita "3": aparece "= 9,48 Kg (sobre bruto − tara)", e "Líquido (Kg)" vai a 306,52. [ZOOM: "Impureza" e "Líquido (Kg)"] | O ferro tem um pouco de terra, e o Rafael combinou três por cento de impureza. A tela converte: nove vírgula quarenta e oito quilos. O líquido fica trezentos e seis vírgula cinquenta e dois quilos. |
| A câmera passa por "Tara (Kg)" (vazio), pela chave "kg" / "%", por "Valor/Kg" (0,75) e por "Valor estimado" (R$ 229,89). | O campo Tara fica pra embalagem, e a impureza também pode ir em quilos, na chave do lado. O valor estimado já vem pelo líquido: duzentos e vinte e nove reais e oitenta e nove. |
| Em "Como exibir no comprovante", clique em "Completo" ("1ª e 2ª pesagem, bruto, tara, impureza e líquido."); a câmera passa por "Motorista" e "Placa do veículo" (vazios); clique em "Confirmar": a linha "Ferro misto" entra na lista, com 9,48 em "Tara/Imp.". | Aqui você escolhe o que sai no comprovante. No Completo, o Zé vê as duas pesagens. Motorista e placa ficam pra quando vem caminhão. Confirmar, e o item já entra no pedido. |
| Zoom na linha "Ferro misto" (316 e 9,48). | Uma dica: o estoque recebe o líquido. Pesou trezentos e dezesseis quilos, e entram no estoque trezentos e seis vírgula cinquenta e dois. Não é erro: é a impureza que você informou. |

### cap07 · Mesclar pesagens (vinheta: PESAGEM)

| Tela | Fala |
| --- | --- |
| Material "Alumínio latinha"; a balança marca 18,4 kg; em "Tara/Imp.", "0,4"; clique em "Incluir Item": a latinha aparece em duas linhas. [BACKEND: estável em 18,4 kg] | O Zé trouxe mais dois sacos de latinha: dezoito quilos e quatrocentos, com quatrocentos gramas de tara. Agora a latinha está duas vezes na lista. |
| Mouse sobre o botão de mesclar de uma das linhas: "Mesclar 2 pesagens deste material"; clique: abre "Mesclar pesagens" ("Deseja mesclar todas as 2 pesagens de "Alumínio latinha" em uma única linha?"), com "Pesagens atuais:", "Total mesclado: 40 kg (tara: 1)" e "R$ 6,20/kg (média)". [ZOOM: "Pesagens atuais:" e "Total mesclado:"] | Quando o mesmo material aparece mais de uma vez, surge o botão de mesclar. A janela mostra cada pesagem e o total: quarenta quilos, com um quilo de tara, a seis e vinte o quilo. |
| Clique em "Mesclar Todas": aviso "2 pesagens mescladas com sucesso!"; uma linha só de "Alumínio latinha", com R$ 241,80. | Mesclar Todas. Os pesos e as taras se somam, o valor total continua o mesmo, e o comprovante sai com uma linha por material. |
| Zoom no botão "Desmesclar pesagens" da linha. | E se precisar conferir as pesagens separadas, esse botão desfaz a mescla e devolve cada uma como era. |

### cap08 · Desconto e conferência (vinheta: VALOR)

| Tela | Fala |
| --- | --- |
| Na linha "Ferro misto", menu "Ações do item" → "Adicionar tara / pesagem avançada": a "Pesagem avançada" abre com 412, 96, 3 % e 0,75. | Agora a conferência. O Rafael combinou com o Zé fechar o ferro em duzentos e vinte e cinco reais. Pelo menu da linha, a pesagem avançada do ferro abre de novo, do jeito que estava. |
| Clique em "Valor final" e digita devagar "225,00": "Desconto (R$)" vira 4,89. [ZOOM: "Desconto (R$)" e "Valor final"] | Em vez de fazer a conta, eu digito o valor final: duzentos e vinte e cinco, vírgula, zero zero. O desconto se calcula sozinho: quatro reais e oitenta e nove. |
| A câmera fica nos dois campos. | Uma dica: em qualquer campo de valor, os centavos vêm depois da vírgula. O campo apaga o ponto, então zero ponto setenta e cinco vira setenta e cinco reais. Digite com calma e confira. |
| Clique em "Confirmar": aviso "Pesagem do item atualizada"; a linha do ferro mostra R$ 225,00; zoom em "Total da Compra": R$ 913,20. [ZOOM: "Total da Compra"] | Confirmar. O ferro fechou em duzentos e vinte e cinco, e o total da compra ficou novecentos e treze reais e vinte. |
| Clique na linha "Ferro misto": abre embaixo o detalhe "Pesagem avançada", com "1ª pesagem: 412", "2ª pesagem: 96", "Bruto: 316", "Impureza: 9,48 (3%)" e "Desconto: R$ 4,89". [ZOOM: o detalhe da pesagem] | Clicando na linha, abre o detalhe da pesagem: as duas pesagens, o bruto, a impureza e o desconto. É assim que você confere antes de finalizar. |
| Zoom no lápis ao lado do total ("Editar valor total"), sem clicar. | E se o combinado for o valor do pedido inteiro, o lápis do lado deixa digitar o total fechado. A tela continua mostrando embaixo o valor calculado, pra conferência. |

### cap09 · Finalizar o pedido (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| Clique em "Finalizar": abre "Finalizar Pedido" ("Total: R$ 913,20") e, ao lado, "Resumo do Pedido": "Fornecedor:" José Carlos Moreira, "Saldo atual:" R$ 0,00, os três itens e "Valor total". | Conferido, é hora de pagar. Finalizar abre o pagamento, com o resumo do pedido do lado: o fornecedor, os itens e o total. |
| [ILUSTRAÇÃO: as três formas e quem deve a quem. "Dinheiro" sai da gaveta do caixa; "Pix/Transferência" sai da conta do banco; "Saldo" é uma anotação de fiado com duas setas: na compra, da Recicla Vale para o fornecedor ("a Recicla Vale fica devendo"); na venda, do cliente para a Recicla Vale ("o cliente fica devendo"). Entram com "dinheiro", "Pix" e "saldo".] | São três formas. Dinheiro sai do caixa. Pix ou transferência sai da conta do banco. E o saldo é o fiado: na compra, a Recicla Vale fica devendo ao fornecedor. Na venda, é o cliente que fica devendo. |
| Clique em "Pix/Transferência": aparece a lista "Conta Bancária" e "Chave PIX do fornecedor: …". [ZOOM: a chave PIX] | No Pix, você escolhe de qual conta sai o dinheiro, e a chave Pix do Zé aparece aqui, pra copiar. |
| Clique em "Saldo do Fornecedor": no resumo, "Saldo após o pedido:" R$ 913,20 em vermelho, "(Você deverá a ele)"; aparecem "Vencimento (opcional)" e "Configurar faturamento (parcelas)". [ZOOM: "Saldo após o pedido:"] | No saldo, o resumo mostra como fica a conta com ele: Você deverá a ele. |
| Clique em "Dinheiro": "Saldo atual do caixa: R$ …" e o valor 913,20. | Mas o Zé quer dinheiro. Em Dinheiro, a tela mostra quanto tem no caixa agora. |
| Clique em "CONFIRMAR PAGAMENTO": aviso "Compra registrada!"; abre "Imprimir Comprovante"; clique em "Imprimir direto": aviso "Comprovante enviado para impressora". [BACKEND: `create_purchase_atomic` em dinheiro; impressão direta no EcoTray falso] | Confirmar pagamento. Compra registrada: o material entrou no estoque, o dinheiro saiu do caixa, e a compra já está no histórico do Zé. O cupom sai na impressora, e daqui a pouco a gente vê ele com calma. |

### cap10 · Até três formas de pagamento (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| "Nova Compra" vazia; "Selecionar fornecedor" → digita "vale forte" → "Auto Peças Vale Forte". | Agora uma compra maior. Chegou a picape da Auto Peças Vale Forte, com a sucata da oficina. |
| Material "Bateria automotiva": aviso "Preço especial aplicado para Bateria automotiva", e o preço vem 3,40; a balança marca 186,0 kg; "Incluir Item". [BACKEND: preço especial da Vale Forte na Bateria automotiva, R$ 3,40; estável em 186,0 kg] [ZOOM: o preço 3,40 (o aviso some em 2 s)] | Repara no aviso: Preço especial aplicado. A oficina tem um preço combinado na bateria: três e quarenta o quilo, e não os três e dez de sempre. |
| Material "Cobre misto" (36,00); a balança marca 64,0 kg; "Incluir Item"; "Total da Compra": R$ 2.936,40. (Preenchimento sem fala: pode acelerar.) [BACKEND: estável em 64,0 kg] [ZOOM: "Total da Compra"] | São cento e oitenta e seis quilos de bateria e sessenta e quatro de cobre misto. Total: dois mil novecentos e trinta e seis reais e quarenta. |
| Clique em "Finalizar"; liga "Múltiplas formas de pagamento": o rótulo vira "Formas de pagamento (máx. 3)". | O dono combinou assim: duzentos em dinheiro, que o motorista leva, dois mil no saldo, e o resto no Pix. Pra isso, eu ligo Múltiplas formas de pagamento. |
| Clique em "Dinheiro", "Pix/Transferência" e "Saldo do Fornecedor"; no campo do Dinheiro digita "200,00"; no do Saldo, "2000,00": o do Pix completa sozinho R$ 736,40. Em "Conta Bancária", escolhe a conta principal. [ZOOM: os três valores] | Escolho as três formas. Duzentos no dinheiro, dois mil no saldo, e o Pix completa a diferença sozinho: setecentos e trinta e seis reais e quarenta. No Pix, escolho a conta. |
| Zoom no bloco "Total" (sem "Faltam" nem "Excesso") e na "Distribuição do pagamento" do resumo. | A soma fecha com o total. Se não fechar, aparece Faltam ou Excesso em vermelho, e o botão de confirmar só libera quando bate. |

### cap11 · Fiado com parcelas (vinheta: PAGAMENTO)

| Tela | Fala |
| --- | --- |
| Zoom em "Vencimento (opcional)", sem preencher. | Os dois mil do saldo, a Recicla Vale paga depois. Se for numa data só, é só preencher o Vencimento. |
| Clique em "Configurar faturamento (parcelas)": abre "Configurar faturamento" ("Parcelar R$ 2.000,00 do saldo"), com "Condição de pagamento" em "Manual (definir parcelas)". | Aqui vão ser duas parcelas. Configurar faturamento divide o saldo em partes, cada uma com a sua data. |
| Em "Nº de parcelas", clique em "2": duas linhas de R$ 1.000,00, em 10/11/2026 e 10/12/2026; muda a data da primeira para 25/11/2026; "Soma das parcelas" R$ 2.000,00, em verde. [ZOOM: as duas linhas e a soma] | Duas parcelas de mil reais. A primeira, eu mudo pra vinte e cinco de novembro, e a segunda fica pra dez de dezembro. A soma fecha com o saldo e fica verde. |
| [ILUSTRAÇÃO: a linha do tempo das parcelas: 10/11, a compra (R$ 2.000,00 no saldo); 25/11, "1ª parcela R$ 1.000,00"; 10/12, "2ª parcela R$ 1.000,00". Cada data acende com a palavra dela.] | Assim, cada parcela tem o seu dia, e você sabe quanto paga e quando. |
| Clique em "Aplicar faturamento": o botão vira "2 parcelas", "1ª em 25/11/2026 · R$ 2.000,00", com "Editar"; o "Vencimento (opcional)" some; no resumo, "Faturamento a prazo" com as duas parcelas. [ZOOM: o resumo das parcelas] | Aplicar faturamento. Com as parcelas, o vencimento único sai da tela: quem manda nas datas são elas. Uma dica: se o valor do saldo mudar depois, a tela avisa pra refazer as parcelas. |
| Clique em "CONFIRMAR PAGAMENTO": aviso "Compra registrada!" e a janela "Imprimir Comprovante". [BACKEND: `create_purchase_atomic` com dinheiro 200,00, Pix 736,40 na conta principal, saldo 2.000,00 e `p_installments` (25/11 e 10/12)] | Confirmar pagamento. Dinheiro, Pix e fiado em duas parcelas, tudo numa compra só. |

### cap12 · O cupom e o cupom sem valor (vinheta: COMPROVANTE)

| Tela | Fala |
| --- | --- |
| Janela "Imprimir Comprovante" ("Deseja imprimir o comprovante de compra?"), com a chave "Visualizar" / "Imprimir" e os botões "Não, obrigado" e "Imprimir direto". | Depois de confirmar, a tela pergunta do comprovante. Imprimir direto manda pra impressora térmica, pelo EcoTray. E em Visualizar, o comprovante abre em PDF na tela. |
| Clique em "Imprimir direto": aviso "Comprovante enviado para impressora". [BACKEND: impressão direta no EcoTray falso] | Imprimir direto. |
| [ILUSTRAÇÃO: o cupom térmico saindo da impressora, desenhado a partir do comprovante real desta compra (o PDF do app, sem campo inventado): a empresa, o fornecedor Auto Peças Vale Forte, as linhas Bateria automotiva e Cobre misto com peso, preço e total, o total e as formas de pagamento. O papel desce com a fala.] | Pronto. O cupom sai com o material, o peso, o preço e como foi pago. Esse papel fica com o fornecedor. |
| Na "Nova Compra" vazia, clique em "Opções avançadas": "Ajustes usados de vez em quando neste pedido.", "Data e hora do pedido", "Gerar nota fiscal" e "Comprovante sem valores" ("Oculta preços, totais e formas de pagamento nos comprovantes."). Mouse no ícone de informação: "O pedido é salvo normalmente com os valores; eles só ficam ocultos nos comprovantes e no portal do cliente.". [ZOOM: "Comprovante sem valores" e o balão] | E quando o papel vai na mão do motorista, sem mostrar preço? É o Comprovante sem valores, aqui em Opções avançadas, do lado do Finalizar. |
| A câmera fica no balão; fecha o menu sem ligar nada. | O pedido guarda todos os valores. Eles só ficam escondidos no comprovante e no portal. Uma dica: ligue antes de finalizar, porque vale só pra aquele pedido. O próximo já nasce com os valores. A gente usa isso já já, na venda. |

### cap13 · A tela de venda (vinheta: VENDA)

| Tela | Fala |
| --- | --- |
| Clique numa área vazia e tecla Shift+V: "Nova Venda"; "Selecionar cliente" → digita "bandeira" → "Fundição Bandeira do Vale". | Agora o outro lado: vender. A tela da venda é igual à da compra. Só que aqui vem o cliente, e o preço que entra é o de venda. |
| Material "Metal amarelo (latão)" (31,90); a balança marca 152,0 kg; clique em "Incluir Item": a lista ganha a coluna "Lucro" (R$ 668,80), e embaixo de "Total da Venda" (R$ 4.848,80) aparece "Lucro estimado" R$ 668,80, em verde. [BACKEND: estável em 152,0 kg] [ZOOM: a coluna "Lucro" e o "Lucro estimado"] | A Fundição Bandeira do Vale leva cento e cinquenta e dois quilos de latão, a trinta e um e noventa. Repara na coluna nova: o lucro de cada item. E embaixo do total, o lucro estimado da venda: seiscentos e sessenta e oito reais e oitenta. |
| [ILUSTRAÇÃO: o lucro do latão: duas barras, "venda R$ 31,90/kg" e "compra R$ 27,50/kg"; a diferença, "R$ 4,40 por quilo"; vezes 152 kg, R$ 668,80.] | O lucro estimado compara o preço de venda com o preço de compra do material. No latão, são quatro e quarenta por quilo. E o olho do lado esconde o valor, se tiver alguém olhando a tela. |
| Em "Material", escolhe de novo "Metal amarelo (latão)", sem incluir: "Estoque Disponível" 62 Kg, com "Em estoque: 214 Kg" e "Nesta venda: −152" embaixo. [BACKEND: balança em 0,0 kg] [ZOOM: "Estoque Disponível"] | Uma dica: o Estoque Disponível já desconta o que está nesta venda. Tinha duzentos e catorze quilos de latão. Com os cento e cinquenta e dois da venda, a tela mostra sessenta e dois. Não sumiu nada. |
| Clique em "Opções avançadas" e liga "Comprovante sem valores"; fecha o menu: o ponto aparece no botão. | Quem leva a carga é o Edson, no caminhão da Recicla Vale. Então, em Opções avançadas, eu ligo o Comprovante sem valores. |

### cap14 · Estoque insuficiente (vinheta: VENDA)

| Tela | Fala |
| --- | --- |
| Material "Cobre mel" (47,90): "Estoque Disponível" 42 Kg; a balança marca 60,0 kg; clique em "Incluir Item": abre "Estoque insuficiente" ("Estoque insuficiente nesta unidade. Complete a quantidade combinando uma ou mais origens abaixo." e "Faltam 18 Kg de Cobre mel."). [BACKEND: estável em 60,0 kg] [ZOOM: "Faltam 18 Kg de Cobre mel."] | A Fundição também quer sessenta quilos de cobre mel, mas no sistema tem quarenta e dois. Ao incluir, a tela avisa: faltam dezoito quilos, e propõe de onde puxar. |
| Em "Origem do estoque *", abre "Selecione a unidade ou material", grupo "Esta unidade", e escolhe "Cobre misto"; em "Quantidade (Kg)" digita "18": aparece "Quantidade coberta". | A equipe já limpou parte do cobre misto, que agora é cobre mel. Então eu puxo dezoito quilos do cobre misto. |
| [ILUSTRAÇÃO: transferência entre materiais: um monte "Cobre misto" passa 18 kg para o monte "Cobre mel", que vai de 42 para 60 kg; os 60 kg saem na venda; um selo "na finalização da venda".] | O cobre mel fica com os sessenta quilos que a venda precisa. |
| Clique em "Transferir e Adicionar": aviso "Transferência de 18 Kg de Cobre misto agendada para a finalização da venda"; a linha "Cobre mel" entra (Lucro R$ 324,00); "Total da Venda" R$ 7.722,80; "Lucro estimado" R$ 992,80. [ZOOM: "Total da Venda" e "Lucro estimado"] | Transferir e Adicionar. A transferência fica agendada e acontece junto com a venda: se alguma parte falhar, nada é gravado. A venda fecha em sete mil setecentos e vinte e dois reais e oitenta, com novecentos e noventa e dois e oitenta de lucro estimado. |
| A câmera fica na lista. | Se você preferir não transferir, no Cancelar a tela pergunta, e dá pra Inserir mesmo assim. Aí o estoque fica negativo até você lançar a compra que faltou. Quem tem filial vê aqui também as outras unidades: isso depende do plano contratado e precisa de internet. |
| Clique em "Finalizar" → "Pix/Transferência" → conta principal → "CONFIRMAR PAGAMENTO": aviso "Venda registrada!"; abre "Imprimir Comprovante" ("Deseja imprimir o comprovante de venda?"); clique em "Visualizar" e em "Visualizar PDF": o PDF abre com os materiais e os pesos, sem preços nem total. [BACKEND: `create_sale_with_stock_transfers_atomic`, Pix 7.722,80, `p_hide_financial_details`] [TESTAR: a janela do PDF] [ZOOM: o PDF] | A Fundição paga no Pix. Confirmar pagamento, e venda registrada. Como o Comprovante sem valores está ligado, o comprovante sai só com o material e o peso. É esse papel que o Edson leva. |

### cap15 · Sem internet (vinheta: SEM INTERNET)

| Tela | Fala |
| --- | --- |
| [BACKEND: queda de internet simulada; o EcoTray falso segue respondendo em `ws://127.0.0.1:8053`] Na "Nova Venda" vazia, a faixa no topo: "Sem conexão — operações serão salvas localmente até reconectar na internet"; ao lado do selo do caixa, "• Modo Offline". [ZOOM: a faixa] | E se a internet cair no meio do dia? A faixa no topo avisa, e o trabalho continua. A compra, a venda e o caixa funcionam sem internet. |
| Clique numa área vazia e Shift+C: "Nova Compra"; fornecedor: busca "cida" → "Aparecida Ramos"; Material "Alumínio latinha" (6,20); a balança marca 14,6 kg; "Incluir Item"; "Finalizar" → "Dinheiro" → "CONFIRMAR PAGAMENTO": aviso "Compra salva localmente (OFFLINE-C-…). Será sincronizada quando a conexão voltar.". [BACKEND: estável em 14,6 kg; fila local] [ZOOM: o aviso] | Chegou a Dona Cida com a latinha. A balança continua funcionando, porque o EcoTray está aqui no computador: catorze quilos e seiscentos. Finalizo em dinheiro, e a compra fica guardada no computador, com um número provisório. |
| "Voltar para o caixa": o bloco "Pendências de Sincronização (OFFLINE)" com 1; em "Compras", o cartão "Aparecida Ramos", "Compra", o número provisório, "1 item", 14,6 kg e R$ 90,52. [ZOOM: o cartão] | No caixa, ela aparece em Pendências de Sincronização, esperando a internet. |
| [BACKEND: a internet volta] A faixa: "Sincronizando 1/1 operação..." e depois "Operações sincronizadas com sucesso!"; o bloco de pendências some. [ZOOM: a faixa] | Quando a internet volta, a fila sobe sozinha. Pronto: operação sincronizada, e a compra ganha o número de verdade. |
| [ILUSTRAÇÃO: a fila sem internet: cartões "Compra" e "Venda" empilhados no computador, com uma nuvem riscada; a nuvem volta e os cartões sobem um a um, com um visto; um cartão fica vermelho, com "Erro", e não sobe; ao lado dele acendem o ícone de atualizar ("Tentar novamente") e a lixeira.] | Uma dica: se uma operação ficar com Erro, ela não vai de novo sozinha, pra não lançar em dobro. Use o Tentar novamente, o ícone de atualizar do lado: ele reenvia sem duplicar. Sem esse botão, remova pela lixeira e refaça a operação normalmente. |
| A ilustração fecha num cartão "Venda" com "outra unidade" e a nuvem acesa. | E a venda que puxa estoque de outra unidade precisa de internet pra ser finalizada. |

### cap16 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o botão "Nova Compra", o Ctrl+K e o "Novo Fornecedor" do Zé. | Pronto! Recapitulando: a gente abriu a compra pelo caixa, pelo atalho e pelo Ctrl+K, viu o Não informado e cadastrou o Zé na hora. |
| Montagem: a hierarquia do preço; o visor e o "AO VIVO"; a "Pesagem avançada" com "Peso Bruto (Kg)". | Viu qual preço vale, puxou o peso da balança, descontou a tara e a impureza, e fez a dupla pesagem da carroça. |
| Montagem: "Mesclar pesagens", o "Valor final" e o "Finalizar Pedido" com as três formas e as parcelas. | Mesclou a latinha, fechou o valor do ferro e pagou o Zé em dinheiro. Na compra da oficina, pagou em dinheiro, Pix e fiado em duas parcelas. |
| Montagem: o cupom; "Comprovante sem valores"; "Lucro estimado"; "Estoque insuficiente"; a faixa "Sem conexão…". | Imprimiu o cupom, vendeu com o lucro estimado na tela e o cupom sem valor pro motorista, cobriu o estoque que faltava e comprou sem internet. |
| Cartão "Próximo: Ticket de Pesagem"; cartela final. | No próximo tutorial, o caminhão que chega na balança antes de o preço estar fechado: o Ticket de Pesagem. Até lá! |
