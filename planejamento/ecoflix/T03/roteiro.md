# Roteiro T3 · Materiais e tabelas de preço

Roteiro pronto para a voz e a gravação (molde da trilha; sem etapa de aprovação, como na Domiflix). Coluna Fala = o texto
da narração (voz Kaik Barreto), na grafia da legenda, com os números por extenso como se fala (a legenda volta para
algarismo pelo `numeros` do `config_narracao.json`); o texto exato do TTS, com a grafia de pronúncia, fica em
`narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no código
do 1.60.18 (`T03/inventario.md`). Mundo, sementes e o que o backend falso precisa: `T03/plano.md`.

- **Título:** Materiais e tabelas de preço
- **Antes:** Usuários e permissões (T2)
- **Próximo:** Clientes, fornecedores e a ficha do parceiro (T4)
- **Vinhetas (áreas):** ESTOQUE · MATERIAIS · MATERIAIS · NOTA FISCAL · GRUPOS · PREÇOS · PREÇOS · PREÇOS · PREÇOS · MATERIAIS ·
  PREÇOS · PREÇOS · ESTOQUE · EXPORTAR · MATERIAIS · RESUMO (todos os capítulos menos o 0)
- **Duração estimada:** ~26 min de vídeo (3.600 palavras de fala, ~23 min de voz a 2,6 palavras/s; 19.391 caracteres, ~24,5 min a 790 por
  minuto; mais 16 vinhetas e as ações na tela). Era 14 min no 1.59.154: entraram a margem automática (4 capítulos), o menu da tabela
  (duplicar, fixar, trocar a principal) e as dicas do 1.60
- **Aula no computador** (janela 1600×900, 16:9), logado como Rafael Nogueira, `FAKE_NOW=2026-11-10T08:30:00-03:00`. Cada
  capítulo abre num navegador novo, com a semente do fim do capítulo anterior (`plano.md` › "Sementes"). A lista mostra 10
  materiais por página: o radiador fica na página 2, então o robô o acha pela busca. **Numeração nova (1.60.18):** os capítulos 7, 8, 9,
  10 e 12 são novos (margem automática e o menu da tabela); os antigos 7, 8, 9, 10 e 11 viraram 11, 13, 14, 15 e 16. As sementes mantêm
  os nomes antigos (`apos-cap06`, `apos-cap07`, `apos-cap08`); as da margem são `margem-fora` e `margem-material`.
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
| Capítulo novo (semente `inicio`), em "Materiais" › "Estoque". A câmera abre na coluna "Tabelas de Preço": "PRINCIPAL" com a estrela, "Nova Tabela" e "Posição de Estoque"; o cursor para no "?" ("Como funciona"), sem abrir. | A tela tem quatro partes. Na coluna da esquerda ficam as tabelas de preço. Por enquanto, só a principal, com a estrela. Daqui a pouco a gente cria outra. O botão de interrogação, ali em cima, explica os tipos de tabela. |
| A câmera vai para a barra: "Movimentar estoque", "Editar Preços", "Grupos", "Exportar" e "Zerar Estoque". | Em cima, os botões do dia a dia: Movimentar estoque, Editar Preços, Grupos, Exportar e Zerar Estoque. Cada um tem a sua vez neste tutorial. |
| A câmera desce para os cartões "Peso Total em Estoque", "Total Pago" e "Projeção de Vendas" e para no primeiro. | Os três cartões resumem o pátio. O primeiro é o peso total em estoque. |
| [ILUSTRAÇÃO: Total Pago × Projeção de Vendas: um monte de sucata genérico com a etiqueta "Estoque"; na primeira frase entram, à esquerda, "×" e a etiqueta "Preço médio pago", que dão o cartão "Total Pago"; na segunda, à direita, "×" e "Preço de venda", que dão "Projeção de Vendas".] | O Total Pago é esse estoque vezes o preço médio que você pagou nas compras. E a Projeção de Vendas é o mesmo estoque vezes o preço de venda: quanto entraria se você vendesse tudo hoje. |
| A câmera vai para a "Lista de Materiais" e passa pelas colunas "Código", "Nome", "Estoque Atual", "Valor Pago", "Preço médio pago" (com o selo "estimativa"), "Preço de Compra", "Preço de Venda" e "Ações"; clique no título "Estoque Atual" (a lista ordena) e de novo em "Código". | Embaixo, a lista de materiais: o código, o nome, o estoque atual e os preços de cada um. O preço médio pago vem marcado como estimativa, porque é uma média das compras. Clicando no título de uma coluna, a lista ordena por ela. |
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
| [ILUSTRAÇÃO: o que fica onde: dois cartões; "No material", com "NCM" e "Nome na nota"; "Nos cenários fiscais", com "CFOP", "CST" e "ICMS" e o selo "contador".] | No material, e na planilha de importação também, vão o NCM e o nome da nota. Os impostos, como CFOP, CST e ICMS, ficam nos cenários fiscais. Eles mudam conforme a operação, o regime da empresa e o parceiro, e quem define é o contador. Isso a gente vê no tutorial de nota fiscal. |

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
| Capítulo novo (semente `apos-cap05`, com o cobre da semana passada); o cursor passa no botão "Editar Preços". | O preço da sucata mexe toda semana. Hoje, o cobre subiu cinquenta centavos o quilo, na compra e na venda. Em vez de abrir material por material, a gente usa o Editar Preços. |
| Clique em "Editar Preços": abre em **tela cheia** "Editar Tabelas de Preço" ("Altere os preços de compra e venda de todos os materiais, tabela por tabela"), com o botão "Sair" no canto. À esquerda, "Tabelas disponíveis" com "Principal" ("Padrão"); no meio, o título "Principal", os selos "Padrão" e "Reflete nas vinculadas", a busca "Buscar por código ou nome..." e a grade "Cód.", "Material", "Compra (R$)" e "Venda (R$)"; à direita, o "Resumo" ("Materiais", "Alterados", "Venda abaixo da compra", "Sem preço", "Margem típica", "Margem automática": "Desligada"). No rodapé, "Cancelar" e "Salvar". O cursor passa em cada parte. | Ele abre em tela cheia. À esquerda ficam as tabelas, por enquanto só a principal. No meio, todos os materiais, com a compra e a venda lado a lado. À direita, o resumo da tabela. Pra fechar sem salvar, é o Sair ou o Cancelar. |
| Em "Buscar por código ou nome..." digita "cobre": ficam Cobre mel, Cobre misto, Fio de cobre encapado e Radiador de cobre. | Busco cobre, e ficam só os cobres. |
| [ZOOM: a linha "Cobre mel"] "Compra (R$)" de 42,00 para 42,50 e "Venda (R$)" de 47,40 para 47,90. | No cobre mel, a compra vai pra quarenta e dois e cinquenta, e a venda pra quarenta e sete e noventa. |
| O mesmo no Cobre misto (36,00 e 41,50) e no Fio de cobre encapado (18,00 e 22,00), com o selo 4x. | Faço o mesmo no cobre misto e no fio encapado. O radiador eu cadastrei hoje, já no preço novo, então ele fica como está. |
| As células alteradas ganham um asterisco; o aviso do rodapé: "3 material(is) com alterações pendentes". | As células alteradas ganham uma marca, e o aviso lá embaixo conta três materiais com alteração. |
| [ZOOM: o "Resumo", linha "Venda abaixo da compra"] Busca "bronze"; em "Venda (R$)" digita 28,00 (a compra é 29,00): o resumo mostra "Venda abaixo da compra" 1, em vermelho. | Uma dica: se a venda ficar menor que a compra, o sistema avisa. No bronze, ponho a venda em vinte e oito, abaixo dos vinte e nove da compra. O resumo, à direita, já conta um material com a venda abaixo da compra. |
| Clique em "Salvar": abre "Preço de venda abaixo do custo" ("1 material está com o preço de venda abaixo do preço de compra. Isso registra prejuízo nesses materiais. Deseja continuar?", com "Bronze 29,00 → 28,00" e os botões "Cancelar" e "Salvar mesmo assim"). [ZOOM: a janela] Clique em "Cancelar"; a venda do bronze volta a 33,50; limpa a busca. | Se eu clicar em Salvar, ele pergunta antes, porque isso registra prejuízo nesse material. Quase sempre é erro de digitação, então eu cancelo e volto a venda pra trinta e três e cinquenta. Se for de propósito, é só confirmar em Salvar mesmo assim. |
| Clique em "Salvar": aviso "Preços atualizados! As tabelas vinculadas serão recalculadas automaticamente."; a tela fecha. [BACKEND: `UPDATE materials` dos três cobres + `rpc save_price_table_items` da Principal; vira `apos-cap06`] | Agora, Salvar. Os preços novos já valem pra próxima compra e pra próxima venda. O aviso fala das tabelas vinculadas: elas acompanham sozinhas, e a gente já chega nelas. Antes, uma novidade do Editar Preços: a margem automática. |

### cap07 · Margem automática: a tabela toda (vinheta: PREÇOS)

Mundo desta aula e das duas seguintes: variante (semente `apos-cap06`); o capítulo termina em "Cancelar", sem gravar nada. Regra, conferida no
código (`lib/precos/margemAutomatica.ts`): margem é sempre sobre a compra; em %, venda = compra × (1 + m/100); em R$, venda = compra + m;
preço guarda até três casas.

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`); clique em "Editar Preços". Na coluna da direita, o cartão "Margem automática" ("Compra e venda amarradas por uma margem sobre a compra"), com a chave desligada. | Toda vez que a compra de um material muda, a venda precisa acompanhar, e fazer isso na mão, linha por linha, dá trabalho. A margem automática resolve: o sistema amarra a venda à compra por uma margem. Ela fica no Editar Preços, num cartão na coluna da direita. |
| Clique na chave "Margem automática": abre o "Alcance da margem" com "Tabela toda" ("Uma margem só, todo material segue") e "Por material" ("Cada material tem a sua margem"); clique em "Tabela toda". | Ligo a chave. Primeiro, o alcance: Tabela toda, com uma margem só pra todos os materiais, ou Por material, que a gente vê no próximo capítulo. Escolho Tabela toda. |
| [ZOOM: "Sobre a compra: R$ 10,00 com 30% vira R$ 13,00."] Em "Margem sobre a compra" digita 15; o cursor passa no botão "R$". | A margem é sempre sobre a compra: dez reais de compra com trinta por cento viram treze reais de venda. Aqui eu ponho quinze por cento. Do lado, o botão de reais troca pra margem em reais por quilo. |
| "Qual preço fica como está?": o cursor passa em "Compra" ("A venda é recalculada") e em "Venda" ("A compra é recalculada"); clique em "Compra" e em "Aplicar". O resumo passa a "Tabela toda · 15%". | Falta dizer qual preço fica como está. Se for a compra, a venda é recalculada. Se for a venda, é a compra que se ajusta. Deixo a compra e clico em Aplicar. |
| A grade ganha a coluna "Margem" (com o cadeado e o 15 em cada linha). [ZOOM: a linha "Cobre misto", compra 36,00 e venda 41,40] O cursor passa no "Ferro pesado" (venda 1,093) e no aviso do rodapé ("16 material(is) + margem automática com alterações pendentes"). | Pronto: a venda de todos os materiais foi recalculada. O cobre misto, de compra a trinta e seis reais, vai pra quarenta e um e quarenta de venda. Os preços guardam até três casas decimais, então alguns materiais mostram o milésimo. E lá embaixo o aviso lembra: a margem também tem alteração pendente. |
| No Cobre misto, "Compra (R$)" vira 38,00: a venda vai a 43,70. [ZOOM: a linha] | Agora, o dia a dia. Se a compra do cobre misto for pra trinta e oito, a venda acompanha sozinha: quarenta e três e setenta. |
| No Cobre misto, "Venda (R$)" vira 46,00: a compra vai a 40,00. [ZOOM: a compra] | E o contrário também funciona. Se eu digito a venda, quarenta e seis reais, é a compra que se ajusta: quarenta reais. |
| Clique em "Editar margem" (o cartão abre, com "Ao mudar a margem, a venda dos materiais que seguem a tabela é recalculada na hora."); a margem vai de 15 para 20: a venda do Cobre misto vira 48,00. | Pra mudar a margem de todo mundo, abro o Editar margem e troco o quinze por vinte. A venda de todos os materiais que seguem a tabela é recalculada na hora. |
| No "Ferro misto", clique no cadeado ("Personalizar a margem deste material"): vira cadeado aberto, o selo "personalizada", e a margem da linha aceita 40. [ZOOM: a linha "Ferro misto"] Clique de novo no cadeado ("Voltar à margem da tabela"). | E um material pode fugir da regra. O ferro misto sempre teve margem maior, então abro o cadeado dele e ponho quarenta por cento. O selo diz personalizada, e os outros seguem a margem da tabela. Fechando o cadeado de novo, ele volta a seguir a tabela. |
| O cursor passa no "Salvar"; clique em "Cancelar": a tela fecha sem gravar. [BACKEND: nenhum; `rpc save_price_table_margins` existe para o ensaio, mas não é chamado] | Uma dica: nada disso vale até clicar em Salvar. Como aqui é só demonstração, eu clico em Cancelar. Salvando, a margem fica gravada na tabela, e da próxima vez que você abrir o Editar Preços ela já vem ligada. |

### cap08 · Margem automática: uma por material (vinheta: PREÇOS)

Variante (semente `apos-cap06`); termina em "Cancelar".

| Tela | Fala |
| --- | --- |
| Capítulo novo; clique em "Editar Preços" e na chave "Margem automática": o cartão abre já em "Por material" ("Manter a margem que cada material já tem hoje, em" com "%" e "R$"). | Nem todo material tem a mesma margem: o ferro rende uma coisa, o cobre outra. Pra isso, o outro alcance: Por material. Abro o Editar Preços e ligo a chave. |
| O cursor passa em "%" e em "R$"; clique em "Aplicar": o resumo passa a "Por material" e nenhum preço muda ("Nenhum preço muda. Material com compra ou venda zerada fica sem margem."). | O cartão pergunta em que unidade manter a margem que cada material já tem hoje: porcentagem ou reais. Deixo em porcentagem e clico em Aplicar. Repara que nenhum preço muda. |
| A grade ganha a coluna "Margem" com a margem de verdade de cada linha. [ZOOM: "Cobre mel" 12,71 e "Ferro misto" 40] | A coluna Margem passa a mostrar a margem de cada um. O cobre mel está em doze e setenta e um por cento, e o ferro misto, em quarenta. |
| No Cobre misto (15,28) digita 15 na margem: a venda vai a 41,40. [ZOOM: a venda] | Cada margem dá pra editar. No cobre misto, que está em quinze e vinte e oito, ponho quinze: a venda vai pra quarenta e um e quarenta. |
| No Bronze, clique no "%" da linha (título "Margem em porcentagem — clique para usar R$"): vira "R$" e a margem passa a 4,50 (a mesma diferença); digita 5: a venda vira 34,00. [ZOOM: a margem 4,50] | A margem também pode ser em reais por quilo. No bronze, clico no botão de reais da linha, e o sistema converte: quatro e cinquenta por quilo, a mesma diferença de antes. Se eu digito cinco reais, a venda vira trinta e quatro. |
| No Bronze, "Compra (R$)" vira 30,00: a venda vai a 35,00. [ZOOM: a venda] | E se a compra do bronze for pra trinta, a venda vai pra trinta e cinco: a compra mais os cinco reais. |
| Busca "alumínio"; clique em "Editar margem": aparece "Mesma margem em vários materiais" (campo, "%"/"R$" e o botão "Aplicar em 3 material(is) exibido(s)"); digita 20 e clica no botão: os três alumínios passam a 7,44, 10,68 e 8,52. | Pra dar a mesma margem a vários materiais, busco alumínio e abro o Editar margem. Em Mesma margem em vários materiais, digito vinte, e o botão diz Aplicar em três materiais exibidos: só esses três mudam. Sem busca, ele aplicaria em todos. |
| Clique na chave (desliga): o resumo mostra "Margem automática: Desligada"; clique em "Cancelar". | Uma dica: desligar a chave desfaz só a configuração da margem; os preços que você já mexeu ficam como estão até salvar ou cancelar. Aqui eu só mostro, então clico em Cancelar. E se uma tabela independente com margem for vinculada à principal, a margem dela é desligada, porque a vinculada segue os preços da principal. |

### cap09 · O resumo e a margem fora da regra (vinheta: PREÇOS)

Variante (semente `apos-cap06` + `margem-fora`: a Principal com a margem "Por material" gravada e a venda do Alumínio latinha em 7,80, fora da
margem de 19,354839%); termina em "Cancelar".

| Tela | Fala |
| --- | --- |
| Capítulo novo; clique em "Editar Preços": abre com a margem ligada ("Por material · cada material com a sua margem sobre a compra"); o resumo à direita, com "Fora da margem" 1. | Quando a margem já está gravada, o Editar Preços abre com ela ligada: o cartão diz Por material, cada material com a sua margem sobre a compra. E o resumo, à direita, conta como a tabela está. |
| [ZOOM: "Venda abaixo da compra" 0] No Bronze, digita -5 na margem: a venda vira 27,55, abaixo da compra (29,00); o resumo mostra "Venda abaixo da compra" 1 em vermelho e aparece o filtro "Abaixo da compra" 1. | Venda abaixo da compra conta os materiais que você vende por menos do que paga. Quando tem algum, fica vermelho. Vou provocar um: no bronze, ponho a margem em menos cinco por cento. A venda cai abaixo da compra, e o resumo já avisa. |
| No Plástico PET, compra e venda viram 0: o resumo mostra "Sem preço" 1; clique em "Sem preço": a lista mostra só o Plástico PET. | Sem preço conta os materiais sem compra e sem venda, comuns depois de importar uma planilha. Zerando a compra e a venda do plástico PET, ele entra aqui. Esses números também viram filtros: clicando neles, a lista mostra só aqueles materiais. |
| Clique no filtro "Todos"; [ZOOM: "Margem típica"] o cursor para na linha (dica "Metade dos materiais tem margem acima disso e metade abaixo"). | Margem típica é a do meio da tabela: metade dos materiais tem margem acima dela, e metade abaixo. |
| O cursor passa em "Fora da margem" 1 e clica: a lista mostra só o Alumínio latinha, com o selo laranja "fora da margem". | Tem também o Fora da margem. Esse selo aparece quando o preço de um material não bate mais com a margem dele. Acontece quando o preço entra por outro caminho: a planilha, o Cato ou as filiais gravam o preço sem recalcular pela margem. |
| [ZOOM: a venda 7,80 do Alumínio latinha] Clique no selo "fora da margem": a venda volta a 7,40. Clique em "Cancelar". | No alumínio latinha, a margem é de dezenove e trinta e cinco por cento, mas a venda está em sete e oitenta. Clicando no selo fora da margem, o sistema recalcula a venda pela compra: ela volta pra sete e quarenta. Aqui eu só mostro, então cancelo. |

### cap10 · A margem no cadastro do material (vinheta: MATERIAIS)

Variante (semente `apos-cap06` + `margem-material`: a Principal com a margem "Por material" gravada, preços batendo); termina em "Cancelar".

| Tela | Fala |
| --- | --- |
| Capítulo novo; busca "radiador" → "..." → "Editar": abre "Editar Material" ("Editando preços na tabela: Principal"); a câmera desce até "Valores e estoque". [ZOOM: a linha "Margem automática de 16,67%: a venda acompanha a compra"] | A margem também aparece no cadastro do material. Abro o radiador pelo Editar. Como a tabela Principal está com a margem automática ligada, a compra e a venda ficam amarradas aqui também, e uma linha embaixo avisa. |
| Clique na calculadora ao lado de "P. Venda" ("Calcular a venda pela margem"): abre "Calcular venda pela margem" ("Margem sobre a compra"); digita 20: "Compra R$ 21,00 → Venda R$ 25,20" [ZOOM]; clique em "Aplicar": "P. Venda" vira 25,20. | Do lado do preço de venda tem uma calculadora: Calcular venda pela margem. Ponho vinte por cento, e a janela mostra a conta: compra de vinte e um reais, venda de vinte e cinco e vinte. Aplicar. |
| "P. Compra" vira 22: "P. Venda" vai a 26,40. [ZOOM: "P. Venda"] | Agora a margem do radiador é essa. Mudo a compra pra vinte e dois, e a venda vai junto, sozinha: vinte e seis e quarenta. |
| Abre a calculadora de novo; o cursor para em "Tirar a margem deste material". | Na calculadora tem ainda o Tirar a margem deste material, que deixa ele sem margem. E, quando a margem é da tabela toda, o Voltar à margem da tabela. |
| Fecha a calculadora (Esc); clique em "Cancelar" (nada é salvo). | Uma dica: a calculadora só aparece quando a tabela tem a margem automática ligada. No Novo Material vale a da principal. Eu não vou salvar, então fecho em Cancelar; clicando em Atualizar, a margem do radiador fica gravada junto com os preços. |

### cap11 · Várias tabelas de preço (vinheta: PREÇOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`, com o caixa do Rafael aberto); a câmera na coluna "Tabelas de Preço". | A maioria dos pátios trabalha só com a tabela principal. Mas a Recicla Vale paga um pouco mais pros depósitos, que trazem material separado e em volume. Uma dica: se a coluna de tabelas não aparece pra você, ligue Múltiplas Tabelas de Preço em Configurações, Usabilidade. |
| Clique em "Nova Tabela": abre "Nova Tabela de Preços". Em "Nome da Tabela" digita "Tabela Depósitos"; marca "Vincular à tabela principal"; aparecem "Tipo de variação" ("Porcentagem" marcado), "Valor da variação" e "Direção da variação" ("Aumenta" marcado); em "Valor da variação" digita 4. | Então, Nova Tabela, com o nome Tabela Depósitos. Marco Vincular à tabela principal e ponho quatro por cento a mais. |
| [ZOOM: "Exemplo de cálculo:", com "Preço base: R$ 10,00" e "Preço nesta tabela: R$ 10,40 (+4%)"] | O exemplo embaixo mostra a conta: o que custa dez reais na principal sai por dez e quarenta nesta tabela. |
| [ILUSTRAÇÃO: a tabela vinculada: duas colunas, "Principal" e "Tabela Depósitos", presas por uma corrente com "+4%"; "Cobre mel 42,50" à esquerda vira "44,20" à direita; a principal sobe e a da direita sobe junto.] | Vinculada quer dizer que ela acompanha a principal sozinha: quando o preço muda lá, como a gente fez com o cobre, muda aqui também. |
| Clique em "Criar Tabela": aviso "Tabela de preço criada com sucesso!"; na coluna, "Tabela Depósitos" com a corrente e o selo "+4%", selecionada; a lista mostra "Exibindo preços da tabela: Tabela Depósitos". [ZOOM: a linha "Cobre mel", com "Preço de Compra" R$ 44,20 e "Preço de Venda" R$ 47,90] [BACKEND: `INSERT price_tables` vinculada] | Criar Tabela. Com ela selecionada, a lista mostra o preço dos depósitos: o cobre mel sai a quarenta e quatro e vinte. O preço de venda, nesta tela, continua o da principal. |
| Clique em "Editar Preços"; na lista da esquerda, clique em "Tabela Depósitos": o título traz "Tabela vinculada" e "+4%"; a grade ganha a coluna "Variação" e um cadeado fechado em cada linha ("Variação padrão - clique para personalizar"). [ZOOM: a linha "Fio de cobre encapado"] Clique no cadeado (abre: "Variação personalizada - clique para usar padrão", selo "personalizado") e troca a variação para 2. | Dá pra ver como a tabela é montada no Editar Preços. Escolho a Tabela Depósitos na lista da esquerda, e a grade ganha a coluna Variação, com um cadeado em cada material. Fechado, o material segue os quatro por cento. Abrindo o do fio de cobre encapado, ele ganha uma variação só dele, em porcentagem ou em reais, e os outros continuam na regra. |
| O cursor vai à coluna da direita: o "Resumo" ("Base: Principal · +4%") e **nenhum** cartão "Margem automática" (só o "Tabela Vinculada"); clique em "Cancelar". [CORTE: volta por 5 s à janela "Nova Tabela de Preços", parada em "Tipo de variação" e "Direção da variação", durante "variar em reais... pra baixo... desmarcar o Vincular".] | Repara que o cartão da margem automática não aparece aqui: tabela vinculada não tem margem própria, ela acompanha a principal. Se a principal usa margem, a vinculada sobe e desce junto. Na criação, dá pra variar em reais em vez de porcentagem, pra baixo em vez de pra cima, ou desmarcar o Vincular: aí é uma tabela independente, com os preços digitados um a um e, se quiser, a própria margem. |
| Menu lateral "Clientes e Fornecedores" → aba "Fornecedores"; em "Buscar fornecedor..." digita "Depósito"; clique em "Depósito Irmãos Siqueira": abre a ficha, com o selo "1 preço personalizado"; clique em "Editar": abre "Editar Fornecedor" na aba "Dados de Contato". | Agora, ligar a tabela a quem vende pra gente. Em Clientes e Fornecedores, abro o Depósito Irmãos Siqueira e clico em Editar. |
| A câmera desce até "Tabela de Preços Padrão"; abre a lista e escolhe "Tabela Depósitos". [ZOOM: "Tabela de Preços Padrão" com "Tabela Depósitos"] Clique em "Salvar": aviso "Fornecedor atualizado!". [BACKEND: `UPDATE suppliers.default_price_table_id` e o lado cliente, pelo cadastro duplo; vira `apos-cap07` sem o caixa] | Em Tabela de Preços Padrão, escolho a Tabela Depósitos e salvo. Agora toda compra do depósito já começa nessa tabela. |
| [ILUSTRAÇÃO: a ordem do preço: uma escada de três degraus que acendem um por vez, junto da fala: "1. Preço personalizado do cliente ou fornecedor", "2. Tabela escolhida no pedido" e "3. Preço do material".] | E quando um material tem mais de um preço possível, qual vale? Uma dica: essa é a dúvida clássica, então vale guardar a ordem. Primeiro, o preço personalizado daquele cliente ou fornecedor. Depois, a tabela escolhida no pedido. E por último, o preço do material. |
| Menu "Financeiro" › "Caixa" → "Nova Compra" (no caixa do Rafael; a câmera não para no caixa) → `/compra`; em "Selecionar Fornecedor" ("Buscar por nome, apelido, CPF/CNPJ ou telefone...") escolhe "Depósito Irmãos Siqueira"; "Tabela de Preços" passa sozinha para "Tabela Depósitos". [BACKEND: caixa do Rafael aberto; tela de compra; `order_drafts`; balança sem leitura] | Pra ver na prática, abro uma compra só pra olhar o preço; a compra em si fica pro tutorial de compra e venda. Escolho o depósito, e a tabela dele já vem selecionada. |
| Em "Escreva o nome ou código do material" escolhe "Cobre mel": aviso "Preço da tabela aplicado para Cobre mel". [ZOOM: "Valor/kg" com 44,20] | No cobre mel, entra o preço da tabela: quarenta e quatro e vinte. |
| Troca o material para "Bronze": aviso "Preço especial aplicado para Bronze". [ZOOM: "Valor/kg" com 30,50, com o aviso no quadro] [TESTAR: posição do aviso; se não couber no zoom, o zoom abre até ele] Nada é incluído; a compra fica sem itens (com itens lançados, a troca abriria "Trocar tabela de preços?": "Só nos próximos" ou "Atualizar N itens"; é da T7). [BACKEND: `entity_custom_prices` Depósito Irmãos Siqueira × Bronze 30,50] | Já no bronze, o depósito tem um preço personalizado: trinta e cinquenta. Olha o aviso: Preço especial aplicado. O personalizado ganha da tabela. E se você trocar a tabela com itens já lançados, o sistema pergunta se atualiza os preços desses itens ou se vale só pros próximos. Isso a gente vê no tutorial de compra e venda. |

### cap12 · Duplicar, fixar e trocar a principal (vinheta: PREÇOS)

Semente `apos-cap07`; o capítulo termina com o mundo igual ao da entrada (a cópia é excluída; a tabela fixada é removida; a troca da principal só é
mostrada e cancelada). Handlers: `duplicate_price_table`, `set_my_preferred_price_table`.

| Tela | Fala |
| --- | --- |
| Em "Materiais" › "Estoque", coluna "Tabelas de Preço"; o cursor passa na "Tabela Depósitos" e clica nos três pontinhos: o menu "Configurações", "Duplicar tabela", "Fixar para meus pedidos e tickets", "Definir como principal da empresa" e "Excluir". | Cada tabela tem um menu nos três pontinhos. É por ele que você ajusta, copia, fixa ou apaga uma tabela. |
| Clique em "Configurações": abre "Editar Tabela de Preços", com o nome e a variação de 4%; clique em "Cancelar". | Em Configurações, dá pra trocar o nome e a variação. Se os depósitos passarem a ganhar cinco por cento, é aqui que muda. |
| "..." → "Duplicar tabela": aviso `Tabela "Tabela Depósitos" duplicada com sucesso!`; na coluna entra "Tabela Depósitos (cópia)", sem a corrente e sem o selo de porcentagem. [ZOOM: a tabela nova] | O Duplicar tabela cria uma cópia com os preços de hoje. Repara que a cópia não tem a corrente: ela nasce independente, e não acompanha mais a principal. Serve de ponto de partida pra uma tabela nova, que pode até ter a própria margem automática. |
| "..." da cópia → "Excluir": abre "Excluir Tabela de Preços" ("Esta ação não pode ser desfeita e todos os preços desta tabela serão perdidos."). [ZOOM: o texto] Clique em "Excluir": aviso "Tabela de preço excluída!". | Como era só um exemplo, eu excluo a cópia. Uma dica: excluir tabela não tem volta, e a principal nunca pode ser excluída. |
| "..." da "Tabela Depósitos" → "Fixar para meus pedidos e tickets": aviso "Tabela fixada para seus novos pedidos e tickets"; o alfinete ("Fixada para meus pedidos e tickets") aparece ao lado do nome. [ZOOM: o alfinete] | Agora, o Fixar. Ele vale só pro seu usuário: os seus pedidos e tickets novos passam a abrir nessa tabela, e os dos colegas continuam como estavam. |
| [ILUSTRAÇÃO: qual tabela o pedido abre: três degraus que acendem um por vez, "1. Tabela do cliente ou fornecedor", "2. A tabela que você fixou", "3. Principal da empresa".] | A ordem é esta: se o cliente ou fornecedor tem tabela no cadastro, vale a dele. Senão, a que você fixou. E se não fixou nenhuma, a principal. |
| "..." → "Remover minha tabela fixada": aviso "Tabela pessoal removida; você voltará a usar a principal da empresa". | O Rafael trabalha na principal, então eu removo. |
| "..." → "Definir como principal da empresa": abre "Definir “Tabela Depósitos” como principal?" ("Os preços desta tabela virarão a base da empresa. A principal atual será preservada como independente e todas as tabelas vinculadas serão recalculadas automaticamente."). [ZOOM: o texto] Clique em "Cancelar". | Por último, Definir como principal da empresa. Os preços dessa tabela viram a base de tudo, a principal antiga fica guardada como independente e as vinculadas são recalculadas. É uma troca grande, pra quando a empresa muda a política de preço. Aqui eu só mostro e cancelo. |

### cap13 · Movimentar, transferir e zerar (vinheta: ESTOQUE)

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

### cap14 · Exportar estoque e tabela (vinheta: EXPORTAR)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`); clique em "Exportar": o menu com "Exportar Estoque" ("Estoque (PDF)" e "Estoque (Excel)") e "Tabela de Preços" ("Tabela de Preços (PDF)"). | Pra levar o estoque pro papel ou pra planilha, é o Exportar. Tem o estoque em PDF e em Excel, e a tabela de preços em PDF. |
| Clique em "Estoque (PDF)": abre "Exportar estoque (PDF)", com "Colunas do arquivo", "Grupos" e "Materiais"; clique em "Exportar": a aba nova abre a "Lista de Materiais" em PDF; aviso "Lista exportada como PDF!". [GRAVAÇÃO: gravar a aba nova] | No estoque, você escolhe os materiais e as colunas do arquivo. Exportar, e o PDF abre numa aba nova, pronto pra salvar ou imprimir. No Excel, o arquivo baixa direto. |
| De volta ao "Estoque", clique em "Tabela Depósitos" na coluna; "Exportar" → "Tabela de Preços (PDF)": abre "Exportar tabela de preços em PDF" (todos marcados); clique em "Exportar PDF": abre "Formato da tabela de preços", com "A4" e "Térmico". | A tabela de preços sai da tabela escolhida na coluna da esquerda. Seleciono a Tabela Depósitos, escolho os materiais e o formato: folha A4 ou o papel da impressora térmica. |
| Clique em "A4": a aba nova abre o PDF com os dados da empresa, "TABELA: TABELA DEPÓSITOS" e "Cód.", "Material" e "Preço/KG"; aviso `Tabela "Tabela Depósitos" exportada!`. [ZOOM: o título e a linha do Cobre mel, R$ 44,20] [GRAVAÇÃO: gravar a aba nova] | Pronto: a tabela com o preço de compra de cada material, do jeito que se entrega pro depósito. |

### cap15 · Excluir um material (vinheta: MATERIAIS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`). [ILUSTRAÇÃO: arquivar × apagar: a ficha "Radiador de cobre" sai da lista e entra numa caixa de arquivo; ao lado, as linhas do histórico (compra, saída, transferência) ficam no lugar; entra uma linha "Exclusão" que leva o estoque a zero.] | Por último, o Excluir. Ele parece apagar, mas na verdade arquiva. O material sai da lista e das buscas do pedido, e as compras, as vendas e o histórico dele continuam lá. |
| Busca "radiador" → "..." → "Excluir": abre "Confirmar Exclusão": "Tem certeza que deseja excluir o material Radiador de cobre (Código: 70)?" e "Atenção: Este material possui 110 Kg em estoque.". [ZOOM: o aviso] | Repara no aviso: o radiador ainda tem cento e dez quilos. Excluindo, o sistema registra a saída desse saldo, como exclusão, e o estoque dele zera. |
| Clique em "Sim, Excluir": a linha some; aviso `"Radiador de cobre" excluído`, com o botão "Desfazer". [TESTAR: o "Desfazer" vive 5 s; o robô clica uns 2,5 s depois do aviso] [BACKEND: `INSERT stock_movements` (`EXCLUSAO`) + `UPDATE materials` (`is_archived`)] | Sim, Excluir. Saiu da lista, e o aviso traz um Desfazer. |
| Clique em "Desfazer": aviso `"Radiador de cobre" restaurado!`; a linha volta com 110 Kg. [BACKEND: desarquiva, devolve o saldo e apaga o movimento `EXCLUSAO`; o mundo fica igual ao `apos-cap08`] | Clicando nele, o material volta com o saldo que tinha. Como a Recicla Vale vai continuar comprando radiador, ele fica. |

### cap16 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o cadastro do radiador e o código 70 (trechos dos caps. 2 e 3). | Pronto! Recapitulando: a gente conheceu a tela Estoque, cadastrou o radiador de cobre, com os preços e o estoque inicial, e trocou o código pelo do caderno. |
| Montagem rápida: o NCM 7404.00.00 e o grupo "Radiadores" (caps. 4 e 5). | Escolheu o NCM, que o contador confirma, e criou o grupo Radiadores. |
| Montagem rápida: "Editar Tabelas de Preço" e a margem automática (caps. 6 a 10). | Reajustou o cobre de uma vez no Editar Preços, ligou a margem automática, pra tabela toda e por material, em porcentagem e em reais, e viu o resumo, o selo fora da margem e a calculadora no cadastro. |
| Montagem rápida: a "Tabela Depósitos" com "+4%" e o menu da tabela (caps. 11 e 12). | Criou a Tabela Depósitos, ligou ela ao Depósito Irmãos Siqueira e viu a ordem do preço: o personalizado, a tabela do pedido e o preço do material. E viu o menu da tabela: duplicar, fixar pro seu usuário e trocar a principal. |
| Montagem rápida: a saída, a transferência e o PDF da tabela (caps. 13 e 14). | Ajustou o estoque na mão, transferiu entre materiais, exportou o estoque e a tabela, e viu que excluir é arquivar, com o Desfazer. |
| Cartão "Próximo: Clientes, fornecedores e a ficha do parceiro"; cartela final. | No próximo tutorial, a gente cadastra quem traz a sucata e quem leva: os clientes e os fornecedores. Até lá! |
