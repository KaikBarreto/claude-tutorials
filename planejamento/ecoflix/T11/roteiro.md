# Roteiro T11 · Produção

Pronto para gerar a voz e gravar (molde Domiflix/EcoFlix, sem etapa de aprovação). Coluna **Fala** = o texto da
narração (voz Kaik Barreto), uma linha da tabela por linha do `narracao/tts_textos.py`, que aplica a grafia de
pronúncia do PERFIL (Kanban, Kardex, PDF, CRM). Números falados por extenso; na legenda viram algarismo pelo `numeros`
do `narracao/config_narracao.json`. Coluna **Tela** = o que o robô faz e onde a câmera foca, com os rótulos entre aspas
como no código da 1.59.154 (`T11/inventario.md`).
Logado como Rafael Nogueira (MASTER). Tudo fictício e simulado no backend falso; a tela de bloqueio do módulo (que mostra
preço) não é gravada.

- **Título:** Produção
- **Antes:** Estoque: saldo, histórico e posição (T10)
- **Próximo:** CRM/Kanban (T26)
- **Vinhetas (áreas):** PRODUÇÃO · FICHA TÉCNICA · ORDENS · LANÇAMENTO · RELATÓRIO · CONFIGURAÇÕES · RESUMO (todos os
  capítulos, menos o 0, têm vinheta)
- **Duração estimada:** ~16 min de vídeo (~2.040 palavras, ~13 min de voz a 2,6 palavras/s, mais 14 vinhetas,
  12 ilustrações e as esperas da tela). Alvo da fonte: ~20 min.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` nos capítulos 0 a 6 e `2026-11-10T17:30:00-03:00` do 7 ao 14 (o lançamento
  é feito no fim do dia; a data continua 10/11).
- **Estado inicial e sementes:** `plano.md` → "Mundo: o que esta aula precisa" (ficha e ordens do Cobre mel, Fardo de
  alumínio cadastrado, tolerância 2%, meta 250, os dois ajudantes) e "Gravação" (sementes `inicio` a `apos-cap13`).
- Marcas: `[ZOOM: ...]` dura a frase inteira ao lado (nunca zoom dentro de zoom); `[ILUSTRAÇÃO: ...]` é cena HTML no
  estilo da marca (`docs/09-aula-ilustrada.md`), com o momento preso à palavra citada; `[BACKEND: ...]` é o que o backend
  falso precisa ter. "(ação antes da frase)" = o robô termina a ação antes de a fala comentar.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Produção". | (sem fala) |
| Dashboard do EcoSistema, logado como Rafael Nogueira; a câmera parada no menu lateral. [BACKEND: semente `seeds-extra/t11/inicio.json`] | Oi! Neste tutorial a gente vai transformar o que entrou no pátio em produto de maior valor, e descobrir quanto custou cada quilo de verdade. |
| [ILUSTRAÇÃO: O problema do pátio: fundo branco; um monte de latinhas soltas com gotas de água, um torrão de terra e duas latas de aço cinza no meio (entra com "latinha"); uma seta até uma prensa em blocos simples e um fardo cúbico saindo dela (entra com "Prensada"); sobre o fardo, o balão "R$ por kg?" (entra com "quanto custou"). Montserrat, verde #50D088, sem logo] | Na Recicla Vale Metais, a latinha chega solta, com terra, água e até lata de aço no meio. Prensada, ela vira fardo e vende melhor. Mas quanto custou cada quilo desse fardo? |
| No menu lateral, clique em "Materiais" e em "Produção" (ação antes da frase): a tela "Produção", "Fichas técnicas, ordens de produção e custo por peça", na aba "Ordens de Produção", com o quadro. | É isso que a Produção responde. Ela fica aqui, em Materiais, Produção, e depende do plano contratado. |
| Cartão discreto: "Antes: Estoque: saldo, histórico e posição". | Se você ainda não viu o tutorial Estoque: saldo, histórico e posição, dá uma olhada antes. [pause] Vamos ver o que a Produção resolve. |

### cap01 · O que a Produção resolve (vinheta: PRODUÇÃO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em "Produção"; zoom suave na coluna de abas: "Ordens de Produção", "Conversão", "Fichas Técnicas", "Máquinas", "Relatório", "Configurações" (sem clicar; a câmera não para em "Conversão" nem em "Máquinas"). | Do lado esquerdo ficam as abas. Nesta aula a gente usa quatro: Ordens de Produção, Fichas Técnicas, Relatório e Configurações. |
| [ILUSTRAÇÃO: O caminho da produção: cinco cartões em fila, cada um entra com a sua palavra e fica verde na vez dele (os anteriores ficam cinza): "Ficha técnica" (lata → fardo) com "ficha técnica"; "Ordem" (500 kg · Cláudio e Diego) com "ordem"] | O caminho é este. Primeiro, a ficha técnica: a receita, com o que entra e o que sai. Depois, a ordem: quanto produzir e quem vai produzir. |
| [ILUSTRAÇÃO, continua: "Lançamento do dia" (480 kg de fardo · 498 kg de latinha) com "lançamento"; "Estoque" (latinha −498 kg · fardo +480 kg) com "estoque"] | No fim do dia, o lançamento: quanto cada um produziu e quanta latinha foi usada de verdade. Aí o estoque se mexe sozinho: a latinha sai, e o fardo entra. |
| [ILUSTRAÇÃO, continua: "Custo" (R$ 6,43 por kg) com "custo"; os cinco cartões juntos] | E quando a ordem é finalizada, o sistema fecha o custo de cada quilo. |
| De volta à tela "Produção", aba "Ordens de Produção" (a tela de bloqueio não aparece: ela mostra preço). | Uma dica: se a sua empresa ainda não tem a Produção, a tela abre desfocada, com o aviso Ainda não está no seu plano e o botão Ativar produção. |

### cap02 · A receita do produto (vinheta: FICHA TÉCNICA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); clique em "Fichas Técnicas": a lista "Fichas técnicas" (contador 1) com "Cobre mel" · "Kg" e, à direita, "Selecione uma ficha técnica". | Tudo começa pela ficha técnica. Ela é a receita do produto: o que entra e o que sai. |
| [ILUSTRAÇÃO: A ficha técnica é a receita: um cartão de receita com o título "Fardo de alumínio"; à esquerda "Entra", com a lata e "Alumínio latinha" (entra com "entra"); uma seta; à direita "Sai", com o fardo e "Fardo de alumínio" (entra com "sai"); embaixo, menor, "1 ficha por produto · vale para todas as ordens dele" (entra com "Uma ficha")] | Na receita do fardo, entra latinha e sai fardo de alumínio. Uma ficha por produto, e ela vale pra todas as ordens dele. |
| Clique em "Nova" (ação antes da frase): no painel da direita, "Nova ficha técnica", "Monte a receita: matérias-primas entram, o produto final sai.", com "Matérias-primas (entram) \*" à esquerda, a seta e o cartão "Produto final" à direita. | Clico em Nova. A tela já mostra a receita do jeito que ela é: as matérias-primas entram, e o produto final sai. |
| No cartão de "Matérias-primas (entram) \*", em "Escolher material", digita "latinha" e escolhe "Alumínio latinha"; o cartão passa a mostrar o nome, o campo "Qtd" e "Kg". | Do lado esquerdo, a matéria-prima. Escolho o Alumínio latinha. |
| No cartão "Produto final", em "Selecione o produto", digita "fardo" e escolhe "Fardo de alumínio"; o cartão mostra "Fardo de alumínio" e "unidade de produção: pç". | Do lado direito, o produto final: o Fardo de alumínio. Ele precisa estar cadastrado como material, igual a qualquer outro do estoque. |
| [ZOOM: o botão "+" ao lado do seletor do produto (título "Criar novo produto"), sem clicar] | Se ainda não estiver, esse botão de mais cria o material sem sair da ficha. |
| A câmera sobe até "Nome da ficha", vazio, com "Fardo de alumínio" de placeholder. | E o nome da ficha é opcional. Em branco, ela usa o nome do produto. |

### cap03 · Quanto entra por unidade (vinheta: FICHA TÉCNICA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); o `setup` refaz fora do vídeo o cap02 ("Nova", "Alumínio latinha", "Fardo de alumínio", sem salvar). Em "Unidade de produção", troca "pç — Peça" por "Kg — Quilograma"; o cartão passa a "unidade de produção: Kg" e o total a "Consumo por Kg". | Agora as quantidades. Primeiro, a unidade de produção: o fardo é pesado na balança, então ele sai em quilo. |
| [ZOOM: o campo "Qtd" do cartão "Alumínio latinha"] digita 1; ao lado fica "Kg", e "Consumo por Kg" mostra "1 Kg". | Na matéria-prima vai a quantidade pra um quilo de fardo, e não pro lote inteiro. Na prensa, um quilo de latinha vira um quilo de fardo, então aqui é um. |
| A câmera fica no cartão "Produto final". | O que se perde na prensa aparece depois, no lançamento do dia. |
| A câmera desce até "Peças por unidade de venda (ex.: jogo = 4)", vazio ("Opcional"). | Peças por unidade de venda serve pra quem produz por peça e vende em conjunto, como um jogo de quatro. O fardo sai em quilo, então fica vazio. |
| Clique em "Salvar ficha": aviso "Ficha técnica salva"; a lista passa a ter "Fardo de alumínio" · "Kg" (contador 2). [BACKEND: RPC `upsert_production_recipe_atomic` (cabeçalho Fardo de alumínio, unidade "Kg", sem pack; insumo Alumínio latinha 1); vira `apos-cap03`] | Salvar ficha. Pronto, a ficha do fardo já está na lista. |
| Clique em "Cobre mel" na lista: o painel vira "Editar ficha técnica", com "Fio de cobre encapado" e 1,6 "Kg", o produto final "Cobre mel" e "Consumo por Kg" "1,60 Kg". [ZOOM: o cartão "Fio de cobre encapado" com 1,6] | Repara na ficha do Cobre mel, que a Recicla Vale já usa pra descascar fio. Pra cada quilo de cobre, entram um quilo e seiscentos gramas de fio encapado. |
| [ILUSTRAÇÃO: Quantidade por unidade: duas linhas. Em cima, "1 kg de fardo ← 1 kg de latinha"; com "Quinhentos", o carimbo verde "× 500 = 500 kg de latinha". Embaixo, "1 kg de cobre mel ← 1,6 kg de fio"; com "Cinquenta", "× 50 = 80 kg de fio"] | É sempre assim: a ficha leva a quantidade de um quilo, e a ordem multiplica. Quinhentos quilos de fardo pedem quinhentos quilos de latinha. Cinquenta quilos de cobre pedem oitenta quilos de fio. |

### cap04 · Coprodutos (vinheta: FICHA TÉCNICA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`); "Fichas Técnicas", clique em "Fardo de alumínio": "Editar ficha técnica"; a câmera desce até "Coprodutos (saem junto) · opcional", com "Use quando a produção gera mais de um material (ex.: sobra reaproveitável).". | E quando sai mais de uma coisa do mesmo processo? Isso é o coproduto. |
| [ILUSTRAÇÃO: O coproduto: uma esteira com latinhas passa sob um ímã (entra com "ímã"); as latas de aço sobem para o ímã e caem num monte "Chaparia" (entra com "chaparia"); o alumínio segue para o fardo "Fardo de alumínio"; sobre o monte, o selo "quantos kg? só depois" (entra com "depois")] | Quando a latinha passa no ímã, as latas de aço que vieram no meio saem. Elas viram chaparia, que também tem valor. Mas quanto sai, só dá pra saber depois de separar. |
| Clique em "Adicionar coproduto"; em "Escolher material", "Chaparia"; o cartão mostra "Chaparia" e "Quantidade digitada no lançamento do dia". [ZOOM: o cartão "Chaparia"] | Por isso o coproduto entra na ficha sem quantidade. Adiciono a Chaparia, e o cartão já avisa: a quantidade é digitada no lançamento do dia. |
| Clique em "Salvar ficha": aviso "Ficha técnica salva". [BACKEND: `upsert_production_recipe_atomic` com `p_recipe_id` da ficha e `p_outputs` [Chaparia]; vira `apos-cap04`] | Salvar ficha. A receita do fardo está completa. |

### cap05 · Criar a ordem de produção (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`); clique em "Ordens de Produção": o quadro em "Kanban", com "A fazer", "Em produção" e "Concluída" (nesta, "#2" e "#1" do "Cobre mel"). | Receita pronta, agora a ordem de produção. |
| [ILUSTRAÇÃO: A ordem é o plano: uma prancheta com "500 kg · 10/11 · Marcos · Cláudio e Diego" (entra com "plano"); ao lado, a prateleira do estoque com a latinha parada; com "lançamento", uma seta sai da prateleira] | A ordem é o plano: quanto produzir, quando e com quem. Quem mexe no estoque é o lançamento do dia. |
| Clique em "Nova produção" (ação antes da frase): "Nova ordem de produção", "Planeje a produção a partir de uma ficha técnica. Depois você vai lançando a produção dia a dia."; em "Ficha técnica \*" ("Escreva o nome ou código do produto"), digita "fardo" e escolhe "Fardo de alumínio". | Clico em Nova produção. A ordem sempre sai de uma ficha, e eu escolho a do Fardo de alumínio. |
| [ZOOM: "Quantidade planejada \*"] digita 500. | Na quantidade planejada, quinhentos quilos. É a meta do lote, que serve de referência. |
| "Data da produção" já em 10/11/2026; em "Responsável", troca "Rafael Nogueira" por "Marcos Antunes". | A data já vem com hoje. No responsável, o Marcos, que cuida da balança. |
| Em "Equipe (quem vai produzir)", "Selecione a equipe": marca "Cláudio Ferraz" e "Diego Morais" e fecha a lista; embaixo, "Quem vai produzir esta ordem. Na finalização você informa quanto cada um produziu. Usado no relatório por funcionário.". | Na equipe, quem vai prensar: o Cláudio e o Diego. É essa equipe que aparece no lançamento do dia, um por um. |
| "Coluna" já em "A fazer". [ZOOM: o bloco "Consumo teórico estimado": "Alumínio latinha", "Qtd teórica" 500, "Custo est." R$ 3.100,00; "Custo estimado total" R$ 3.100,00; "Custo estimado por peça" R$ 6,20] [BACKEND: RPC `get_material_cost_with_basis` da latinha → `{cost 6.20, basis_used media_historica, is_fallback false}`] | Embaixo vem o consumo teórico estimado: quinhentos quilos de latinha. E o custo estimado, seis reais e vinte por quilo, que é a média do que a Recicla Vale pagou na latinha. |
| (o mesmo zoom, em "Custo estimado por peça") | Como o fardo sai em quilo, onde a tela diz peça, vale quilo. |
| Clique em "Criar ordem": aviso "Ordem criada"; em "A fazer", o cartão "#3" "Rascunho", "Fardo de alumínio", "planejado: 500 Kg", "Rafael Nogueira", "10/11/2026", "Equipe: 2 funcionários". [BACKEND: RPC `get_next_production_order_number` → 3; `INSERT production_orders` (`draft`, responsável "Marcos Antunes", coluna "A fazer"); `production_order_workers` sem `entry_id` (Cláudio e Diego); vira `apos-cap05`] | Criar ordem. Pronto, a ordem três está em A fazer, ainda como rascunho. |
| A câmera fica no cartão. | Uma dica: criar, lançar e finalizar ordem pede a permissão Registrar Produção. Ficha técnica e configurações pedem Gerenciar Fichas Técnicas. São separadas: o encarregado lança a produção sem mexer na receita. |

### cap06 · O Kanban (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`); o quadro; a câmera passa pelos cabeçalhos "A fazer", "Em produção" e "Concluída". | As ordens ficam neste quadro, o Kanban: cada coluna é uma etapa, e cada cartão anda de uma pra outra. Ele já vem com três: A fazer, Em produção e Concluída. |
| Clique no nome "Em produção" (ação antes da frase): abre "Editar coluna"; em "Nome", apaga e digita "Na prensa"; a "Cor" fica a laranja. | As colunas são suas. Clicando no nome, você muda o nome e a cor. Aqui, Em produção vira Na prensa. |
| [ZOOM: a chave "Coluna de conclusão", desligada, com "As ordens finalizadas vão automaticamente para esta coluna. Só uma coluna pode ser a de conclusão."] | Nessa janela fica também a chave Coluna de conclusão. É pra coluna marcada que vão as ordens finalizadas, e só uma pode ter. |
| Clique em "Salvar": aviso "Coluna atualizada"; o cabeçalho passa a "Na prensa". [BACKEND: `UPDATE production_kanban_columns` (nome)] | Salvar. Pronto, a coluna mudou de nome. |
| [ZOOM: o sinal de check no cabeçalho "Concluída" (título "Coluna de conclusão")] | Na Recicla Vale, a coluna de conclusão é a Concluída. Repara no sinal de check do lado do nome. |
| A câmera vai ao botão "Coluna", no fim do quadro (sem clicar). | Precisa de mais uma etapa? O botão Coluna cria outra no fim do quadro. |
| Arrasta o cartão "#3" de "A fazer" para "Na prensa" (ação antes da frase). [BACKEND: `UPDATE production_orders.kanban_column_id`; vira `apos-cap06`] | Pra andar com a ordem, é só arrastar o cartão. O Cláudio e o Diego começaram a prensar, então ela vai pra Na prensa. |
| A câmera abre para o quadro inteiro. | Arrastar pra coluna de conclusão é diferente: abre a janela de finalizar, porque lá só fica ordem fechada de verdade. A gente faz isso daqui a pouco. |

### cap07 · A produção do dia (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`, FAKE_NOW 17:30); clique no cartão "#3" em "Na prensa" (ação antes da frase): abre "Produção #3", "Fardo de alumínio", com "Meta (referência)" 500 Kg, "Produzido até agora" 0 Kg e, em "Lançamentos", "Nenhum dia lançado ainda. Comece lançando a produção do dia.". | Fim do dia, hora de lançar o que a equipe prensou. Clico no cartão, e a ordem abre com a meta e o que já foi produzido. |
| Clique em "Lançar produção do dia": a janela "Lançar produção do dia", "Fardo de alumínio · lançamento de 10/11/2026", com "Dia da produção \*" em 10/11/2026. | Lançar produção do dia. O dia já vem com hoje. |
| [ZOOM: "Produzido (por funcionário) \*"] em "Cláudio Ferraz" digita 260 e em "Diego Morais", 220; "Total do dia" mostra 480 Kg. | Em Produzido, a equipe da ordem, um por linha. O Cláudio prensou duzentos e sessenta quilos, e o Diego, duzentos e vinte. O sistema soma: quatrocentos e oitenta quilos no dia. |
| Em "Subprodutos (se sobrar algo aproveitável)", clique em "+ Adicionar"; em "Material" ("Selecione o subproduto"), "Chaparia"; em "Qtd (Kg)", 14. | Agora os subprodutos. É aqui que entra o coproduto da ficha: catorze quilos de chaparia, as latas de aço que saíram no ímã. |

### cap08 · O real contra o teórico (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`, FAKE_NOW 17:30); o `setup` refaz fora do vídeo a janela do cap07 (260, 220 e Chaparia 14). A câmera desce até "Matéria-prima usada": "Alumínio latinha". [ZOOM: "Sugerido pela ficha: 480 Kg" e o campo "Real (Kg)" com 480] | Embaixo fica a matéria-prima usada. O sistema sugere quatrocentos e oitenta quilos de latinha: a ficha vezes o que foi produzido. Esse é o teórico. |
| [ILUSTRAÇÃO: Teórico × real: à esquerda, o cartão "ficha: 1 kg → 1 kg × 480 kg = teórico 480 kg"; com "balança", uma balança com o visor "498 kg" e o rótulo "real"; com "dezoito", entre os dois, "+18 kg" em vermelho; com "aço", saem do "+18" três ícones pequenos: lata de aço, terra, gota] | Só que na balança, a latinha usada deu quatrocentos e noventa e oito quilos. Esse é o real. A diferença são dezoito quilos: as latas de aço, a terra e a água que saíram. |
| [ZOOM: o campo "Real (Kg)"] apaga e digita 498 (ação antes da frase); ao lado aparece "+18" em vermelho. | No campo Real, eu corrijo pra quatrocentos e noventa e oito. Repara que a diferença aparece na hora, em vermelho: gastou mais do que a receita previa. |
| (o mesmo zoom) | Se der menos, ela aparece em verde: rendeu mais que a receita. |
| A câmera abre para a linha inteira de "Alumínio latinha". | Uma dica: quem baixa do estoque é o real, não o teórico. Saem quatrocentos e noventa e oito quilos de latinha, e não os quatrocentos e oitenta da ficha. |

### cap09 · Perda acima da tolerância (vinheta: LANÇAMENTO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`, FAKE_NOW 17:30); o `setup` refaz fora do vídeo a janela do cap07 com o real 498. Na linha, "Motivo da perda \*" ("Motivo") e, em vermelho, "Informe o motivo da diferença"; embaixo, "Salvar lançamento" apagado. [ZOOM: "Motivo da perda \*" e "Informe o motivo da diferença"] | Com a diferença, apareceu o campo Motivo da perda, e o botão Salvar lançamento ficou apagado. O sistema pede o motivo antes de salvar. |
| [ILUSTRAÇÃO: Tolerância de perda: uma régua centrada em "teórico 480 kg"; com "dois", uma faixa verde de 470,4 a 489,6 kg; com "nove", a etiqueta "± 9,6 kg"] | É a tolerância de perda. Na Recicla Vale ela é de dois por cento: em quatrocentos e oitenta quilos, até nove quilos e seiscentos gramas de diferença passam sem motivo. |
| [ILUSTRAÇÃO, continua: com "dezoito", um marcador vermelho em "498 kg", fora da faixa, com o selo "pede motivo"; com "Dentro", um marcador cinza no meio da faixa, com "não pede"; com "Configurações", uma engrenagem pequena no canto] | Os dezoito quilos passaram disso, então o motivo é obrigatório. Dentro da tolerância, a linha só avisa e não pede nada. O valor da tolerância fica nas Configurações, que a gente vê no fim. |
| Clique em "Motivo": a lista "Perda de corte", "Sucata", "Retrabalho", "Peça rejeitada", "Defeito de fabricação", "Material reaproveitável", "Outros"; escolhe "Material reaproveitável" (ação antes da frase); o aviso vermelho some e "Salvar lançamento" acende. | Escolho o motivo. Aqui, a maior parte da diferença virou chaparia, então é Material reaproveitável. O motivo fica guardado no lançamento, e o botão acende. |
| A câmera fica no botão "Salvar lançamento", aceso. | Uma dica: com o Salvar lançamento apagado, desce até a matéria-prima usada. É lá que o motivo da perda fica esperando. |
| Clique em "Salvar lançamento": aviso "Lançamento salvo — estoque ajustado"; na ordem, "Produzido até agora" 480 Kg, a barra "480 de 500 Kg" e 96%, e em "Lançamentos" a linha "10/11", "480 Kg", "Cláudio Ferraz e Diego Morais"; o selo vira "Em andamento". [BACKEND: RPC `add_production_entry_atomic` (consumo latinha teórico 480, real 498, `loss_reason` reaproveitavel, `line_cost` 3.087,60; saídas Fardo de alumínio 480 principal e Chaparia 14; Cláudio 260 e Diego 220); `stock_movements` `PRODUCAO`: latinha −498, fardo +480, chaparia +14; ordem `in_progress`; vira `apos-cap09`] | Salvar lançamento. O estoque já foi ajustado: saiu a latinha, e entraram o fardo e a chaparia. E o dia aparece na ordem, com quem produziu. |

### cap10 · Finalizar e fechar o custo (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`, FAKE_NOW 17:30); o quadro: "#3" em "Na prensa", "Em andamento", "480 Kg produzido". Arrasta o cartão para "Concluída" (ação antes da frase): abre "Finalizar #3", "Fardo de alumínio". | Lote prensado, hora de fechar a ordem. Arrasto o cartão pra Concluída, e abre a janela de finalizar. |
| [ZOOM: "Meta (referência)" 500 Kg e "Produzido de verdade" 480 Kg, com o selo "96% da meta"] | A meta era de quinhentos quilos, e saíram quatrocentos e oitenta: noventa e seis por cento da meta. Como a meta é referência, a ordem fecha assim mesmo. |
| A câmera desce para "Resumo do lote": "Produto principal" 480 Kg · Fardo de alumínio; "Subprodutos" 14 Kg · Chaparia; "Matéria-prima usada" 498 Kg · Alumínio latinha; "Perdas" 18 Kg · Alumínio latinha. | No resumo do lote fica tudo junto: o fardo, a chaparia, a latinha usada e os dezoito quilos de perda. |
| [ZOOM: "Custo total do lote" R$ 3.087,60 e "Custo por peça" R$ 6,43] | E o custo real fecha aqui: três mil e oitenta e sete reais e sessenta no lote, e seis reais e quarenta e três por quilo de fardo. |
| [ILUSTRAÇÃO: Custo estimado × real: duas colunas. "Estimado" (entra com "estimado"): "500 kg de latinha × R$ 6,20 = R$ 3.100,00 ÷ 500 kg = R$ 6,20 por kg". "Real" (entra com "diferença"): "498 kg de latinha × R$ 6,20 = R$ 3.087,60 ÷ 480 kg de fardo = R$ 6,43 por kg"; com "dezoito", destaque nos "18 kg a mais"] | Na ordem, o estimado era seis e vinte. A diferença vem dos dezoito quilos a mais de latinha: eles também entram no custo do fardo. |
| "Produção por funcionário": "Cláudio Ferraz" 260 Kg e "Diego Morais" 220 Kg; clique em "Finalizar ordem": aviso "Ordem finalizada — custo/peça R$ 6,43"; o cartão "#3" na "Concluída", selo "Concluída", "R$ 3.087,60 · R$ 6,43/peça", "Produziu: 2 funcionários". [BACKEND: RPC `finalize_production_order_atomic` (`completed`, `total_material_cost` 3.087,60, `cost_per_unit` 6,4325) e `kanban_column_id` da "Concluída"; vira `apos-cap10`] | Finalizar ordem. Pronto, o cartão foi pra Concluída, já com o custo do lote e o de cada quilo. |
| A câmera fica no cartão. | Ordem finalizada fica de vez na coluna de conclusão. Pra desfazer, só excluindo, como a gente vê no fim. |

### cap11 · Relatório de Produção (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`); clique em "Relatório": "Relatório de produção", "PERÍODO" em "Este mês"; em "PRODUTO", troca "Todos os produtos" por "Fardo de alumínio" (ação antes da frase). | Agora o relatório. Em cima ficam os filtros: período, produto e funcionário. Escolho o Fardo de alumínio, neste mês. |
| [ZOOM: os quatro cartões: "Ordens concluídas" 1, "Custo de matéria-prima" R$ 3.087,60, "Perda média" +3,8% ("real × teórico"), "Rendimento médio" 96,4% ("produzido / real")] | Os cartões resumem o mês do fardo: as ordens concluídas, o custo da matéria-prima, a perda média e o rendimento médio. |
| [ILUSTRAÇÃO: Rendimento e perda: uma barra "entrou: 498 kg de latinha" e, embaixo, uma barra menor "saiu: 480 kg de fardo" (entra com "saiu"); com "noventa", "480 ÷ 498 = 96,4%" e o rótulo "rendimento"] | Rendimento é quanto saiu pelo que entrou: quatrocentos e oitenta quilos de fardo pra quatrocentos e noventa e oito de latinha. Dá noventa e seis vírgula quatro por cento. |
| [ILUSTRAÇÃO, continua: com "dezoito", o pedaço que sobra na barra de cima fica vermelho, "18 kg"; com "três", "18 ÷ 480 = 3,8%" e o rótulo "perda"] | E a perda é o que passou da ficha: os dezoito quilos sobre os quatrocentos e oitenta, três vírgula oito por cento. |
| Na aba "Por produto", desce até a tabela. [ZOOM: a linha "Fardo de alumínio": "Teórico (kg)" 480, "Real (kg)" 498, "% Perda" +3,8%, "% Rendim." 96,4%, "Custo MP" R$ 3.087,60, "Custo/peça" R$ 6,43] | Na aba Por produto, a tabela traz a mesma conta por produto, com o teórico, o real e o custo por peça, que aqui é por quilo. |
| Clique em "Por funcionário": "Ranking de funcionários" com Cláudio Ferraz e Diego Morais; desce até "Produção do dia" (10/11/2026): "Meta: 250/dia por funcionário.", "Cláudio Ferraz" 260 com "bateu" e "Diego Morais" 220 com "faltam 30". [BACKEND: leituras de `productionEmployeeData.ts` (lançamentos, ordens, equipe e `employees.position` "Ajudante de pátio")] | Em Por funcionário fica o ranking da equipe. E na produção do dia aparece a meta, de duzentos e cinquenta quilos por pessoa: o Cláudio bateu, e pro Diego faltaram trinta quilos. |
| Volta a "Por produto"; a câmera vai ao botão "Exportar" (sem clicar). | E o botão Exportar tira o relatório em PDF ou em planilha. |

### cap12 · Os ajustes da Produção (vinheta: CONFIGURAÇÕES)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap10`); clique em "Configurações": a lista de ajustes. | Agora as configurações da Produção. Cada uma grava na hora, assim que você muda. |
| [ZOOM: "Custo de produção em cadeia (multinível)", desligado, com o texto "Quando ligado, ao usar um material que você mesmo produziu como matéria-prima (ex.: plástico moído virando pellet), o sistema usa o custo de PRODUÇÃO dele, não o de compra."] | O custo de produção em cadeia, o multinível, é pra quando um material que você mesmo produziu vira matéria-prima de outro. Ligado, ele entra com o custo de produção, e não com o de compra. |
| A câmera desce até "Quando dar baixa no estoque", ligado, com "Agora: baixa a cada lançamento do dia.". | Em Quando dar baixa no estoque, a Recicla Vale usa o padrão: cada dia lançado já mexe no estoque. |
| [ILUSTRAÇÃO: Quando o estoque baixa: duas linhas do tempo com três marcos, "dia 1", "dia 2" e "finalizar". Em cima, "A cada lançamento", com uma seta de estoque em cada dia (já na tela no começo da frase); embaixo, "Só ao finalizar": com "acumulando", os dias empilham num balde; com "finalizada", uma seta só no marco "finalizar"] | Desligado, os dias vão se acumulando, e o estoque só mexe quando a ordem é finalizada. |
| Em "Bloquear finalização quando faltar matéria-prima em estoque", liga a chave (ação antes da frase): aviso "Passou a bloquear finalização sem estoque". [BACKEND: `UPDATE companies.production_block_on_insufficient_stock` true; vira `apos-cap12`] | Bloquear finalização quando faltar matéria-prima em estoque: a Recicla Vale liga. Assim, a produção não fecha sem matéria-prima no estoque, e o saldo não fica negativo. |
| [ZOOM: os dois cartões de baixo, um embaixo do outro: "Tolerância de perda (%)" com 2 ("Só pede o motivo da perda quando a diferença entre real e teórico passar deste percentual. 0 = sempre pedir.") e "Meta de produção por dia" com 250; o zoom dura esta frase e a seguinte] | A tolerância de perda é aquela dos dois por cento. Com zero, o sistema pede o motivo pra qualquer diferença. |
| (o mesmo zoom; a câmera desce de leve até "Meta de produção por dia") | E a meta de produção por dia, por funcionário, é a do relatório: duzentos e cinquenta quilos. |

### cap13 · Excluir uma ordem concluída (vinheta: ORDENS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap12`); clique em "Ordens de Produção": na "Concluída", "#3" do "Fardo de alumínio" e, abaixo, "#2" e "#1" do "Cobre mel", os dois com "50 Kg produzido", "R$ 1.440,00 · R$ 28,80/peça" e 03/11/2026. [ZOOM: os cartões "#2" e "#1"] | E quando uma ordem foi lançada errada? Repara nas ordens um e dois do Cobre mel: são a mesma produção, lançada duas vezes. |
| Passa o mouse no cartão "#2": aparece a lixeira "Excluir ordem"; clique (ação antes da frase): "Excluir ordem de produção?", "Atenção: esta produção já foi finalizada. Ao excluir, o estoque será estornado — a matéria-prima volta e o produto sai. Esta ação não pode ser desfeita.". [ZOOM: o texto da confirmação] | Ordem concluída fica na coluna de conclusão. Pra corrigir, o caminho é excluir. Na lixeira do cartão, o sistema avisa que o estoque é estornado. Estornar é desfazer o movimento: a matéria-prima volta, e o produto sai. |
| Clique em "Excluir ordem": aviso "Ordem excluída"; o cartão "#2" sai do quadro. [BACKEND: RPC `delete_production_order_atomic` da #2: movimentação inversa de cada linha de produção dela (Fio de cobre encapado +80, Cobre mel −50), sem apagar as originais; a ordem sai das listas e do relatório; vira `apos-cap13`] | Excluir ordem. Pronto: os oitenta quilos de fio voltaram pro estoque, e os cinquenta quilos de cobre saíram. |
| No menu lateral, "Materiais" › "Histórico" (ação antes da frase): "Histórico de Materiais"; em "Buscar código ou material", digita "fio" e clica em "Fio de cobre encapado": "KARDEX — {código} - Fio de cobre encapado", "Este mês"; a câmera vai às duas linhas "Produção" de 03/11 (−80 Kg cada) e à linha do estorno de hoje (+80 Kg). [BACKEND: `stock_movements` das três linhas; o tipo da linha do estorno é o da RPC real (a conferir: "Produção" com sinal invertido ou "Exclusão"); a fala não diz o tipo dela] | No histórico do material, o Kardex, dá pra ver tudo. As duas saídas da produção continuam lá, e o estorno entra como uma linha nova, devolvendo os oitenta quilos. |
| [ILUSTRAÇÃO: O estorno: o saldo do "Fio de cobre encapado" como uma pilha; três linhas de histórico empilhadas, "−80 kg Produção", "−80 kg Produção" e, com "desfeito", "+80 kg estorno", nenhuma riscada; com "Nada", um selo "nada é apagado"; a pilha cresce 80 kg] | Nada é apagado: o histórico conta o que aconteceu, até o que foi desfeito. |
| [ZOOM: o selo "Produção" de uma das linhas] | Uma dica: no Kardex, a produção tem tipo próprio, Produção. Quem olha só o que foi comprado e vendido acha que o saldo não bate. É a produção que explica a diferença. |

### cap14 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida (cortes das gravações): a ficha do fardo com a Chaparia, o cartão da #3 no Kanban, a linha do real 498 com o motivo, o "Finalizar #3" com o custo, os cartões do relatório. | Pronto! Recapitulando: a gente montou a ficha técnica do fardo, com a latinha que entra, o fardo que sai e a chaparia como coproduto. |
| (montagem, continua) | Criou a ordem de quinhentos quilos com a equipe, mudou o nome de uma coluna do Kanban e arrastou a ordem. |
| (montagem, continua) | Lançou a produção do dia por funcionário, corrigiu a latinha pro real da balança e deu o motivo da perda acima da tolerância. |
| (montagem, continua) | Finalizou a ordem com o custo real de cada quilo, leu o rendimento no relatório, passou pelas configurações e excluiu uma ordem lançada em dobro, com o estorno do estoque. |
| Cartão discreto: "Próximo: CRM/Kanban". | No próximo tutorial, nenhuma oportunidade se perde no caminho: contatos e negociações organizados no CRM. Até lá! |
