# Roteiro T3 · Materiais e tabelas de preço

Roteiro pronto para a voz e a gravação (molde da trilha; sem etapa de aprovação, como na Domiflix). Coluna Fala = o texto
da narração (voz Kaik Barreto), na grafia da legenda, com os números por extenso como se fala (a legenda volta para
algarismo pelo `numeros` do `config_narracao.json`); o texto exato do TTS, com a grafia de pronúncia, fica em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
da 1.59.154 (`T03/inventario.md`). Mundo, sementes e o que o backend falso precisa: `T03/plano.md`.

- **Título:** Materiais e tabelas de preço
- **Antes:** Usuários e permissões (T2)
- **Próximo:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Vinhetas (áreas):** ESTOQUE · MATERIAIS · MATERIAIS · NOTA FISCAL · GRUPOS · PREÇOS · PREÇOS · ESTOQUE · EXPORTAR ·
  MATERIAIS · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~14 min de vídeo (1.865 palavras de fala, ~12 min de voz a 2,6 palavras/s, mais 11 vinhetas, as
  ilustrações e as ações na tela; alvo da fonte: 15 min)
- **Aula no computador** (janela 1280×800), logado como Rafael Nogueira, `FAKE_NOW=2026-11-10T08:30:00-03:00`. Cada
  capítulo abre num navegador novo, com a semente do fim do capítulo anterior (`plano.md` › "Sementes"). A lista mostra 10
  materiais por página: o radiador fica na página 2, então o robô o acha pela busca.
- Marcas na Tela: `[ZOOM: ...]` (dura a frase inteira, um por vez), `[ILUSTRAÇÃO: ...]`, `[BACKEND: ...]` (o que o
  backend falso precisa ter), `[OUTRO USUÁRIO]`, `[GRAVAÇÃO: ...]` e `[TESTAR: ...]` (cuidado do robô).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Materiais e tabelas de preço". | (sem fala) |
| [ILUSTRAÇÃO: o cardápio do pátio: uma lousa genérica com o título "Recicla Vale Metais" e três linhas, "Cobre mel", "Ferro pesado" e "Alumínio latinha", que entram uma a uma; em cada linha, as etiquetas "Compra" e "Venda", que acendem quando a fala diz "compra" e "venda".] | Oi! Neste tutorial a gente vai montar o cardápio da Recicla Vale Metais: cada material que entra no pátio, com o preço de compra e o preço de venda. |
| [ILUSTRAÇÃO, continuação: da lousa saem três setas para três cartões genéricos, "Compra", "Venda" e "Nota fiscal", um por vez, na ordem da frase.] | É desse cadastro que a compra, a venda e a nota fiscal puxam os dados. Por isso ele vem primeiro. |
| Dashboard do EcoSistema, logado como Rafael Nogueira; o cursor abre "Materiais" no menu lateral e clica em "Estoque"; a tela "Estoque" carrega (`/materiais`). [BACKEND: semente `t3/inicio`] | Tudo isso fica no menu Materiais, em Estoque. |
| Cartão discreto: "Antes: Usuários e permissões". | Se você ainda não viu o tutorial Usuários e permissões, dá uma olhada antes. [pause] Vamos conhecer a tela. |

### cap01 · A tela Estoque (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), em "Materiais" › "Estoque". A câmera abre na coluna "Tabelas de Preço": "PRINCIPAL" com a estrela, "Nova Tabela" e "Posição de Estoque". | A tela tem quatro partes. Na coluna da esquerda ficam as tabelas de preço. Por enquanto, só a principal, com a estrela. Daqui a pouco a gente cria outra. |
| A câmera vai para a barra: "Movimentar estoque", "Editar Tabela", "Grupos", "Exportar" e "Zerar Estoque". | Em cima, os botões do dia a dia: Movimentar estoque, Editar Tabela, Grupos, Exportar e Zerar Estoque. Cada um tem a sua vez neste tutorial. |
| A câmera desce para os cartões "Peso Total em Estoque", "Total Pago" e "Projeção de Vendas". | Os três cartões resumem o pátio. O primeiro é o peso total em estoque. |
| [ILUSTRAÇÃO: Total Pago × Projeção de Vendas: um monte de sucata genérico com a etiqueta "Estoque"; na primeira frase entram, à esquerda, "×" e a etiqueta "Preço médio pago", que dão o cartão "Total Pago"; na segunda, à direita, "×" e "Preço de venda", que dão "Projeção de Vendas".] | O Total Pago é esse estoque vezes o preço médio que você pagou nas compras. E a Projeção de Vendas é o mesmo estoque vezes o preço de venda: quanto entraria se você vendesse tudo hoje. |
| A câmera vai para a "Lista de Materiais" e passa pelas colunas "Código", "Nome", "Estoque Atual", "Valor Pago", "Preço médio pago" (com o selo "estimativa"), "Preço de Compra", "Preço de Venda" e "Ações". | Embaixo, a lista de materiais: o código, o nome, o estoque atual e os preços de cada um. O preço médio pago vem marcado como estimativa, porque é uma média das compras. |
| [OUTRO USUÁRIO] Corte para a mesma tela logada como Marcos Antunes (sem "Ver Totais e Valores Financeiros"): os pesos aparecem; "Total Pago" e "Projeção de Vendas" com cadeado e "Sem permissão"; nas colunas de dinheiro, cadeado e "***". Volta para o Rafael. [BACKEND: login do Marcos com as permissões do T2] | Uma dica: quem não tem permissão de ver valores, como o Marcos, que é balanceiro, continua vendo os pesos. No lugar do dinheiro, aparece um cadeado. |
| A câmera sobe para o cabeçalho da lista: o filtro "Todos os Materiais", "Importar planilha", "+ Novo Material" e a busca "Buscar material por código ou nome...". | Em cima da lista ficam o filtro, a importação por planilha, o botão Novo Material e a busca. É pelo Novo Material que a gente começa. |

### cap02 · Cadastrar um material (vinheta: MATERIAIS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`); clique em "+ Novo Material": abre "Novo Material", com as abas "Dados" e "Produção", as seções "Identificação", "Valores e estoque" e "Fiscal e organização", e o "Resumo" à direita. | Vamos cadastrar um material novo. A Recicla Vale começou a comprar radiador das oficinas, e ele ainda não está na lista. |
| A câmera vai até as abas "Dados" e "Produção" (sem clicar). | A aba Produção aparece pra quem tem o módulo de produção no plano, e tem um tutorial só dela. Aqui a gente fica em Dados. |
| Em "Nome *" digita "Radiador de cobre"; abre "Unidade" (o "Kg" marcado, com "Mais utilizados" e "Menos utilizados") e fecha em "Kg". | No nome, vai o jeito que a equipe fala no pátio: Radiador de cobre. A unidade já vem em quilo. Se o material for por peça ou por fardo, é só trocar aqui. |
| [ZOOM: "P. Compra" e "P. Venda"] Digita 21,00 em "P. Compra" e 24,50 em "P. Venda". | No preço de compra, vinte e um reais o quilo. No de venda, vinte e quatro e cinquenta. |
| [ZOOM: "Quantidade em Estoque"] Digita 120. | Na quantidade em estoque vai o que já tem no pátio hoje: cento e vinte quilos. Se não tiver nada, deixa em zero, e as compras vão enchendo o saldo. |
| A câmera vai ao "Resumo": "Radiador de cobre", "16 · Kg", "Compra" R$ 21,00, "Venda" R$ 24,50, "Estoque" 120 Kg. | Do lado direito, o resumo mostra como o material vai ficar. |
| Clique em "Criar": aviso "Material criado!"; a janela fecha. Em "Buscar material por código ou nome..." digita "radiador": a linha "16", "Radiador de cobre", 120 Kg, R$ 21,00 e R$ 24,50. [BACKEND: `INSERT materials`; vira `apos-cap02`] | Criar, e pronto: material criado. Ele entra no fim da lista, e pra achar rápido é só buscar pelo nome. |
| Limpa a busca; clique em "Importar planilha": abre "Importar materiais por planilha", com "1. Baixe o modelo" ("Baixar modelo") e "2. Envie a planilha preenchida" ("Arraste a planilha aqui ou clique para selecionar"). | E se você tem muitos materiais pra cadastrar, dá pra trazer todos de uma vez: baixa o modelo, preenche uma linha por material e envia a planilha. |
| A câmera vai até "O sistema confere tudo antes de cadastrar."; fecha a janela sem enviar nada. | Uma dica: a importação é tudo ou nada. Se uma linha tiver erro, nenhum material daquele arquivo entra; é só corrigir e mandar de novo. E se a internet cair no meio, pode mandar o mesmo arquivo: ele não duplica nada. |

### cap03 · O código do material (vinheta: MATERIAIS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); busca "radiador". [ZOOM: a célula "Código" da linha, com o 16] | Agora, o código. O radiador ganhou o dezesseis porque eu deixei o campo em branco: o sistema pegou o maior número da lista e somou um. |
| [ILUSTRAÇÃO: o código no dia a dia: fichas numeradas de 1 a 15 numa fila; um "+1" põe a ficha "16 Radiador de cobre" no fim; depois, num balcão de compra genérico, alguém digita "16" e a ficha acende.] | É o atalho do dia a dia: na compra e na venda, o operador digita o número e o material aparece. |
| [ILUSTRAÇÃO, continuação: um caderno genérico aberto na linha "Radiador ........ 70"; a ficha "16" vira "70".] | Se você já tem os seus códigos, do caderno ou de outro sistema, pode usar os mesmos. No caderno do Rafael, o radiador sempre foi o setenta. |
| "..." da linha → "Editar": abre "Editar Material". [ZOOM: "Código" e a linha "Fica assim:"] O robô apaga o 16 e digita devagar 0, 7 e 0: o campo fica vazio no 0, mostra 7 e depois 70; a linha passa a "Fica assim: 70". | Abro o Editar e digito zero, sete, zero. Olha só: o zero da frente não fica. |
| (mesmo zoom, parado no 70) | Uma dica: o código é só número, e zero na frente não é guardado. Se no caderno era zero zero sete, aqui fica só o sete. |
| Clique em "Atualizar": aviso "Material atualizado!"; a linha mostra "70" e "Radiador de cobre". [BACKEND: `UPDATE materials`; vira `apos-cap03`] | Atualizar, e o radiador agora é o setenta. Cada número vale pra um material só: se ele já estiver em uso, o sistema avisa na hora de salvar. |

### cap04 · O NCM e a nota fiscal (vinheta: NOTA FISCAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap03`). [ILUSTRAÇÃO: o NCM na nota: uma nota fiscal genérica, sem marca nem dado real, com a linha "Radiador de cobre"; ao lado entra a etiqueta "NCM 7404.00.00" e, embaixo dela, "8 dígitos".] | Pra quem emite nota fiscal, cada material precisa do NCM. É um código de oito dígitos que diz pra Receita que mercadoria é aquela, e ele vai dentro da nota. |
| Busca "radiador" → "..." → "Editar"; a câmera desce até "Fiscal e organização": "NCM (Nota Fiscal)", vazio, com a interrogação ao lado. | No cadastro, ele fica no campo NCM. Dá pra digitar, ou clicar na interrogação do lado pra buscar. |
| Clique na interrogação ("Selecionar NCM padrão"): abre "Selecionar NCM para Materiais Recicláveis"; em "Buscar por código NCM ou descrição..." digita "cobre"; aparece o selo "Cobre" com "7404.00.00" e "Desperdícios e resíduos de cobre"; clique em "Selecionar". [BACKEND: `ncm_presets` com as linhas do plano] | A janela traz os códigos comuns da reciclagem. Busco cobre e escolho o de resíduos de cobre. |
| [ZOOM: "NCM (Nota Fiscal)" com 7404.00.00] | Uma dica: o NCM certo de cada material é decisão do contador da empresa. A lista ajuda a achar rápido, mas quem confirma é a contabilidade. |
| A câmera sobe até "Identificação/Produto Fiscal" (vazio, "Ex: SUCATA DE ALUMÍNIO"); o cursor para na interrogação e abre a ajuda: "Como funciona:", "Para que serve:", "Exemplo:" e "Se deixar vazio:". | Outro campo da nota é a Identificação, Produto Fiscal. Ele serve pra quando o nome que sai na nota é diferente do nome que vocês usam no pátio. |
| [ILUSTRAÇÃO: o nome fiscal: três fichas, "Alumínio latinha", "Alumínio perfil" e "Alumínio bloco"; à direita, numa nota genérica, as três viram "SUCATA DE ALUMÍNIO".] | Por exemplo: latinha, perfil e bloco podem sair na nota como sucata de alumínio. |
| [ILUSTRAÇÃO, continuação: à esquerda, numa lista, num pedido e num comprovante genéricos, as três fichas continuam com o nome de cada uma; um "X" sobre três linhas iguais "SUCATA DE ALUMÍNIO".] | Uma dica: esse campo muda só a nota. A tela, os pedidos e os comprovantes continuam com o nome normal, de propósito: senão os três alumínios virariam linhas iguais. |
| De volta ao cadastro, com o campo vazio; clique em "Atualizar": aviso "Material atualizado!". [BACKEND: `UPDATE materials` (`ncm` 74040000); vira `apos-cap04`] | No radiador, eu deixo vazio, e a nota sai com o nome normal. Atualizar. |
| [ILUSTRAÇÃO: o que fica onde: dois cartões; "No material", com "NCM" e "Nome na nota"; "Nos cenários fiscais", com "CFOP", "CST" e "ICMS" e o selo "contador".] | No material, e na planilha de importação também, vão o NCM e o nome da nota. Os impostos, como CFOP, CST e ICMS, ficam nos cenários fiscais, que o contador define, porque mudam conforme a operação, o regime da empresa e o parceiro. Isso a gente vê no tutorial de nota fiscal. |

### cap05 · Grupos de material (vinheta: GRUPOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`); clique em "Grupos": abre "Grupos de materiais" ("Organize seus materiais em grupos por cor e ícone."), com Ferrosos, Cobre, Alumínio, Metais e Outros, cada um com o círculo colorido e o ícone. | Agora, os grupos. A Recicla Vale já separa os materiais em cinco: ferrosos, cobre, alumínio, metais e outros. |
| [ILUSTRAÇÃO: grupos como gavetas: cinco gavetas coloridas com os nomes dos grupos; as fichas dos materiais caem, cada uma na sua; no fim entra uma sexta gaveta, "Radiadores", com a ficha do radiador.] | Grupo é como uma gaveta: junta os materiais parecidos. Com o radiador vão chegar outros, de alumínio e misto, então vale uma gaveta nova. |
| Em "Novo grupo", "Nome *": digita "Radiadores"; "Cor" passa a verde-petróleo (#0F766E) [GRAVAÇÃO: valor do campo, sem a janela nativa de cor]; clique no círculo de "Ícone": abre a grade e escolhe o carro. | No grupo novo vão o nome, a cor e o ícone. Escolho o carro, porque radiador sai de carro. |
| Clique em "Adicionar": aviso "Grupo criado"; "Radiadores" entra na lista. Fecha a janela. [BACKEND: `INSERT material_groups`] | Adicionar, e o grupo está criado. |
| Busca "radiador" → "..." → "Editar"; em "Grupo" abre a lista e escolhe "Radiadores"; a câmera mostra o "+" ao lado do campo, sem clicar. | Agora é só pôr o radiador nele, no campo Grupo. E repara no botão de mais, do lado: por ele dá pra criar um grupo sem sair do cadastro. |
| Clique em "Atualizar": aviso "Material atualizado!"; na linha, embaixo do nome, a bolinha verde-petróleo e "Radiadores". [vira `apos-cap05`] | Atualizar. O grupo aparece embaixo do nome, com a cor dele. |
| Limpa a busca; abre o filtro "Todos os Materiais": a seção "Grupos", com a contagem de cada um; desmarca Ferrosos, Alumínio, Metais, Outros e Radiadores, e fica só "Cobre"; fecha o filtro (o botão mostra "3 materiais"). | E por que agrupar ajuda? No filtro, deixo marcado só o cobre. |
| [ZOOM: os três cartões, agora só com o cobre] | Os cartões lá em cima passam a mostrar o peso e o valor só do cobre que está no pátio. A exportação do estoque segue esse mesmo filtro. |
| Abre o filtro e marca "Todos os Materiais". | Pra voltar, é só marcar Todos os Materiais. |

### cap06 · Editar preços em massa (vinheta: PREÇOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`, com o cobre da semana passada); a câmera vai ao "Editar Tabela". | O preço da sucata mexe toda semana. Hoje, o cobre subiu cinquenta centavos o quilo, na compra e na venda. Em vez de abrir material por material, a gente usa o Editar Tabela. |
| Clique em "Editar Tabela": abre "Editar Preços em Massa" ("Altere os preços de compra e venda de todos os materiais"); à esquerda, "Tabelas disponíveis" com "PRINCIPAL" ("Padrão"); à direita, "Editando tabela de preços", "PRINCIPAL" e a grade "Cód.", "Material", "Compra (R$)" e "Venda (R$)". | Abre uma lista com todos os materiais, com a compra e a venda lado a lado. À esquerda você escolhe a tabela; aqui, a principal. |
| Em "Buscar por código ou nome..." digita "cobre": ficam Cobre mel, Cobre misto, Fio de cobre encapado e Radiador de cobre. | Busco cobre, e ficam só os cobres. |
| [ZOOM: a linha "Cobre mel"] "Compra (R$)" de 42,00 para 42,50 e "Venda (R$)" de 47,40 para 47,90; as duas células ficam destacadas. | No cobre mel, a compra vai pra quarenta e dois e cinquenta, e a venda pra quarenta e sete e noventa. |
| O mesmo no Cobre misto (36,00 e 41,50) e no Fio de cobre encapado (18,00 e 22,00), com o selo 4x. | Faço o mesmo no cobre misto e no fio encapado. O radiador eu cadastrei hoje, já no preço novo, então ele fica como está. |
| A câmera mostra as células destacadas e o aviso "3 material(is) com alterações pendentes". | As células alteradas ficam destacadas, e o aviso em cima conta três materiais com alteração. |
| Clique em "Salvar": aviso "Preços atualizados! As tabelas vinculadas serão recalculadas automaticamente."; a janela fecha. [BACKEND: `UPDATE materials` dos três cobres + `rpc save_price_table_items` da PRINCIPAL; vira `apos-cap06`] | Salvar, e os preços novos já valem pra próxima compra e pra próxima venda. O aviso fala das tabelas vinculadas: elas acompanham sozinhas, e esse é o nosso próximo assunto. |

### cap07 · Várias tabelas de preço (vinheta: PREÇOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`, com o caixa do Rafael aberto); a câmera na coluna "Tabelas de Preço". | A maioria dos pátios trabalha só com a tabela principal. Mas a Recicla Vale paga um pouco mais pros depósitos, que trazem material separado e em volume. |
| Clique em "Nova Tabela": abre "Nova Tabela de Preços". Em "Nome da Tabela" digita "Tabela Depósitos"; marca "Vincular à tabela principal"; aparecem "Tipo de variação" ("Porcentagem" marcado), "Valor da variação" e "Direção da variação" ("Aumenta" marcado); em "Valor da variação" digita 4. | Então, Nova Tabela, com o nome Tabela Depósitos. Marco Vincular à tabela principal e ponho quatro por cento a mais. |
| [ZOOM: "Exemplo de cálculo:", com "Preço base: R$ 10,00" e "Preço nesta tabela: R$ 10,40 (+4%)"] | O exemplo embaixo mostra a conta: o que custa dez reais na principal sai por dez e quarenta nesta tabela. |
| [ILUSTRAÇÃO: a tabela vinculada: duas colunas, "Principal" e "Tabela Depósitos", presas por uma corrente com "+4%"; "Cobre mel 42,50" à esquerda vira "44,20" à direita; a principal sobe e a da direita sobe junto.] | Vinculada quer dizer que ela acompanha a principal sozinha: quando o preço muda lá, como a gente fez com o cobre, muda aqui também. |
| Clique em "Criar Tabela": aviso "Tabela de preço criada com sucesso!"; na coluna, "Tabela Depósitos" com a corrente e o selo "+4%", selecionada; a lista mostra "Exibindo preços da tabela: Tabela Depósitos". [ZOOM: a linha "Cobre mel", com "Preço de Compra" R$ 44,20 e "Preço de Venda" R$ 47,90] [BACKEND: `INSERT price_tables` vinculada] | Criar Tabela. Com ela selecionada, a lista mostra o preço dos depósitos: o cobre mel sai a quarenta e quatro e vinte. O preço de venda, nesta tela, continua o da principal. |
| Menu lateral "Clientes e Fornecedores" → aba "Fornecedores"; em "Buscar fornecedor..." digita "Depósito"; clique em "Depósito Irmãos Siqueira": abre a ficha, com o selo "1 preço personalizado"; clique em "Editar": abre "Editar Fornecedor" na aba "Dados de Contato". | Agora, ligar a tabela a quem vende pra gente. Em Clientes e Fornecedores, abro o Depósito Irmãos Siqueira e clico em Editar. |
| A câmera desce até "Tabela de Preços Padrão"; abre a lista e escolhe "Tabela Depósitos". [ZOOM: "Tabela de Preços Padrão" com "Tabela Depósitos"] Clique em "Salvar": aviso "Fornecedor atualizado!". [BACKEND: `UPDATE suppliers.default_price_table_id` e o lado cliente, pelo cadastro duplo; vira `apos-cap07` sem o caixa] | Em Tabela de Preços Padrão, escolho a Tabela Depósitos e salvo. Agora toda compra do depósito já começa nessa tabela. |
| [ILUSTRAÇÃO: a ordem do preço: uma escada de três degraus que acendem um por vez, junto da fala: "1. Preço personalizado do cliente ou fornecedor", "2. Tabela escolhida no pedido" e "3. Preço do material".] | E quando um material tem mais de um preço possível, qual vale? Uma dica: essa é a dúvida clássica, então vale guardar a ordem. Primeiro, o preço personalizado daquele cliente ou fornecedor. Depois, a tabela escolhida no pedido. E por último, o preço do material. |
| Menu "Financeiro" › "Caixa" → "Nova Compra" (no caixa do Rafael; a câmera não para no caixa) → `/compra`; em "Selecionar Fornecedor" ("Buscar por nome, apelido, CPF/CNPJ ou telefone...") escolhe "Depósito Irmãos Siqueira"; "Tabela de Preços" passa sozinha para "Tabela Depósitos". [BACKEND: caixa do Rafael aberto; tela de compra; `order_drafts`; balança sem leitura] | Pra ver na prática, abro uma compra só pra olhar o preço; a compra em si fica pro tutorial de compra e venda. Escolho o depósito, e a tabela dele já vem selecionada. |
| Em "Escreva o nome ou código do material" escolhe "Cobre mel": aviso "Preço da tabela aplicado para Cobre mel". [ZOOM: "Valor/kg" com 44,20] | No cobre mel, entra o preço da tabela: quarenta e quatro e vinte. |
| Troca o material para "Bronze": aviso "Preço especial aplicado para Bronze". [ZOOM: "Valor/kg" com 30,50, com o aviso no quadro] [TESTAR: posição do aviso; se não couber no zoom, o zoom abre até ele] Nada é incluído; a compra fica sem itens. [BACKEND: `entity_custom_prices` Depósito Irmãos Siqueira × Bronze 30,50] | Já no bronze, o depósito tem um preço personalizado: trinta e cinquenta. Olha o aviso: Preço especial aplicado. O personalizado ganha da tabela. |

### cap08 · Movimentar, transferir e zerar (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`), em "Materiais" › "Estoque", na "PRINCIPAL". | O estoque normalmente se mexe sozinho, pelas compras e pelas vendas. Mas às vezes ele precisa de um ajuste na mão: na contagem de hoje, o radiador deu cento e dezoito quilos, e não cento e vinte. |
| Clique em "Movimentar estoque": abre "Movimentar estoque"; clique em "Saída"; em "Material *" digita "radiador" e escolhe "Radiador de cobre"; em "Quantidade *" digita 2. [ZOOM: "Estoque de Radiador de cobre": "Estoque atual" 120 Kg, "−2 Kg" e "Após a movimentação" 118 Kg] | Em Movimentar estoque, escolho Saída, o radiador e dois quilos. A janela mostra o antes e o depois: de cento e vinte pra cento e dezoito quilos. |
| Em "Descrição / observação" digita "Ajuste de inventário"; clique em "Registrar saída": aviso "Saída de 2 Kg de Radiador de cobre". [BACKEND: `rpc adjust_material_stock_atomic` (`p_reason` "SAIDA", `p_description`)] | Na observação, eu escrevo o motivo. Fica tudo no histórico do material, com quem fez e quando. Registrar saída. |
| [ILUSTRAÇÃO: transferir entre materiais: um radiador genérico se separa em duas partes, a colmeia de cobre e as cintas e suportes de ferro; uma seta "8 kg" leva o ferro da pilha "Radiador de cobre" para a pilha "Ferro misto"; o selo "o peso total não muda".] | Agora, transferir. Na desmontagem dos radiadores saíram oito quilos de ferro, das cintas e dos suportes. Esse peso entrou como radiador, mas é ferro misto. |
| Busca "radiador" → "..." → "Transferir estoque": abre "Transferir Estoque" ("Transferir quantidade de Radiador de cobre (Código: 70) para outro material"), com "Estoque Atual de Radiador de cobre" 118 Kg; em "Material de Destino *" escolhe "Ferro misto". [ZOOM: "Quantidade a Transferir (Kg) *"] Digita 8. | Nos três pontinhos do radiador, Transferir estoque. Destino, ferro misto; quantidade, oito quilos. |
| Clique em "Transferir": aviso "Transferido 8 Kg de Radiador de cobre para Ferro misto". [BACKEND: `rpc transfer_material_stock`; vira `apos-cap08`] | Transferir: sai de um e entra no outro, sem mudar o peso total do pátio. |
| Limpa a busca; clique em "Zerar Estoque": abre "Zerar Todo o Estoque", com "Atenção: Ação irreversível", todos os materiais marcados e o contador de selecionados. | E o Zerar Estoque é pra virada de inventário, quando você recomeça a contagem do zero. Todos os materiais já vêm marcados, e você desmarca os que ficam. |
| [ZOOM: "Para confirmar, digite Zerar todo o meu estoque:" e o botão "Zerar selecionados" apagado] Clique em "Cancelar". | Pra confirmar, tem que digitar a frase da tela, porque não tem volta. Uma dica: antes de zerar, exporte o estoque, pra guardar o retrato do que tinha. Aqui eu só mostro e cancelo. |

### cap09 · Exportar estoque e tabela (vinheta: EXPORTAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`); clique em "Exportar": o menu com "Exportar Estoque" ("Estoque (PDF)" e "Estoque (Excel)") e "Tabela de Preços" ("Tabela de Preços (PDF)"). | Pra levar o estoque pro papel ou pra planilha, é o Exportar. Tem o estoque em PDF e em Excel, e a tabela de preços em PDF. |
| Clique em "Estoque (PDF)": abre "Exportar estoque (PDF)", com "Colunas do arquivo", "Grupos" e "Materiais"; clique em "Exportar": a aba nova abre a "Lista de Materiais" em PDF; aviso "Lista exportada como PDF!". [GRAVAÇÃO: gravar a aba nova] | No estoque, você escolhe os materiais e as colunas do arquivo. Exportar, e o PDF abre numa aba nova, pronto pra salvar ou imprimir. No Excel, o arquivo baixa direto. |
| De volta ao "Estoque", clique em "Tabela Depósitos" na coluna; "Exportar" → "Tabela de Preços (PDF)": abre "Exportar tabela de preços em PDF" (todos marcados); clique em "Exportar PDF": abre "Formato da tabela de preços", com "A4" e "Térmico". | A tabela de preços sai da tabela escolhida na coluna da esquerda. Seleciono a Tabela Depósitos, escolho os materiais e o formato: folha A4 ou o papel da impressora térmica. |
| Clique em "A4": a aba nova abre o PDF com os dados da empresa, "TABELA: TABELA DEPÓSITOS" e "Cód.", "Material" e "Preço/KG"; aviso `Tabela "Tabela Depósitos" exportada!`. [ZOOM: o título e a linha do Cobre mel, R$ 44,20] [GRAVAÇÃO: gravar a aba nova] | Pronto: a tabela com o preço de compra de cada material, do jeito que se entrega pro depósito. |

### cap10 · Excluir um material (vinheta: MATERIAIS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`). [ILUSTRAÇÃO: arquivar × apagar: a ficha "Radiador de cobre" sai da lista e entra numa caixa de arquivo; ao lado, as linhas do histórico (compra, saída, transferência) ficam no lugar; entra uma linha "Exclusão" que leva o estoque a zero.] | Por último, o Excluir. Ele parece apagar, mas na verdade arquiva. O material sai da lista e das buscas do pedido, e as compras, as vendas e o histórico dele continuam lá. |
| Busca "radiador" → "..." → "Excluir": abre "Confirmar Exclusão": "Tem certeza que deseja excluir o material Radiador de cobre (Código: 70)?" e "Atenção: Este material possui 110 Kg em estoque.". [ZOOM: o aviso] | Repara no aviso: o radiador ainda tem cento e dez quilos. Excluindo, o sistema registra a saída desse saldo, como exclusão, e o estoque dele zera. |
| Clique em "Sim, Excluir": a linha some; aviso `"Radiador de cobre" excluído`, com o botão "Desfazer". [TESTAR: o "Desfazer" vive 5 s; o robô clica uns 2,5 s depois do aviso] [BACKEND: `INSERT stock_movements` (`EXCLUSAO`) + `UPDATE materials` (`is_archived`)] | Sim, Excluir. Saiu da lista, e o aviso traz um Desfazer. |
| Clique em "Desfazer": aviso `"Radiador de cobre" restaurado!`; a linha volta com 110 Kg. [BACKEND: desarquiva, devolve o saldo e apaga o movimento `EXCLUSAO`; o mundo fica igual ao `apos-cap08`] | Clicando nele, o material volta com o saldo que tinha. Como a Recicla Vale vai continuar comprando radiador, ele fica. |

### cap11 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cadastro do radiador e o código 70 (trechos dos caps. 2 e 3). | Pronto! Recapitulando: a gente conheceu a tela Estoque, cadastrou o radiador de cobre, com os preços e o estoque inicial, e trocou o código pelo do caderno. |
| Montagem rápida: o NCM 7404.00.00 e o grupo "Radiadores" (caps. 4 e 5). | Escolheu o NCM, que o contador confirma, e criou o grupo Radiadores. |
| Montagem rápida: "Editar Preços em Massa" e a "Tabela Depósitos" com "+4%" (caps. 6 e 7). | Reajustou o cobre de uma vez, criou a Tabela Depósitos, ligou ela ao Depósito Irmãos Siqueira e viu a ordem do preço: o personalizado, a tabela do pedido e o preço do material. |
| Montagem rápida: a saída, a transferência e o PDF da tabela (caps. 8 e 9). | Ajustou o estoque na mão, transferiu entre materiais, exportou o estoque e a tabela, e viu que excluir é arquivar, com o Desfazer. |
| Cartão "Próximo: Clientes, fornecedores e a ficha do parceiro"; cartela final. | No próximo tutorial, a gente cadastra quem traz a sucata e quem leva: os clientes e os fornecedores. Até lá! |
