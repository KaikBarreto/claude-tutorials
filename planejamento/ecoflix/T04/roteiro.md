# Roteiro T4 · Clientes, fornecedores e a ficha do parceiro

Roteiro pronto para gerar a voz e gravar (molde da Domiflix; o Kaik ajusta depois se precisar). Coluna Fala = texto da
narração (voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py` (uma linha
da tabela = uma linha do texto). Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no
código 1.59.154 (`T04/inventario.md`). Mundo, sementes e simulações: `T04/plano.md`.

- **Título:** Clientes, fornecedores e a ficha do parceiro
- **Antes:** Materiais e tabelas de preço (T3)
- **Próximo:** Balança e impressora: o EcoTray (T5)
- **Vinhetas (áreas):** PARCEIROS · CADASTRO · CADASTRO · FISCAL · SALDO · PREÇOS · FICHA · FICHA · SALDO · FICHA · FICHA ·
  SALDO · RESUMO (todos os capítulos, menos o 0)
- **Duração estimada:** ~15 min de vídeo (1.966 palavras e 10.721 caracteres de fala, ~12,6 min de voz, mais vinhetas,
  ilustrações e esperas de tela; alvo da fonte: 17 min). Voz: 11.065 caracteres com os títulos das vinhetas.
- **Gravação:** computador, janela 1280×800 (modo compacto da tela: selos da lista só com ícone), Rafael Nogueira
  (administrador), `FAKE_NOW=2026-11-10T08:30:00-03:00`. Do cap. 1 em diante o `setup` recolhe o menu lateral e cada
  capítulo abre um navegador novo na semente indicada.
- Marcas na Tela: `[ZOOM: ...]` (dura a frase inteira da linha, ou as linhas indicadas, nunca um em cima do outro),
  `[ILUSTRAÇÃO: ...]` (desenho por código no estilo da marca, no lugar da tela, enquanto a frase corre),
  `[BACKEND: ...]` (o que o backend falso precisa ter), `[TESTAR: ...]` (o robô confere antes de gravar).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta da EcoFlix com o título "Clientes, fornecedores e a ficha do parceiro". | (sem fala) |
| [ILUSTRAÇÃO: o pátio: fundo claro, Montserrat, verde da marca; no centro, o pátio "Recicla Vale Metais" (galpão e uma pilha de sucata), que entra com a frase.] | Oi! Neste tutorial a gente vai montar a base de quem entra e sai do pátio da Recicla Vale Metais. |
| [ILUSTRAÇÃO (cont.): em "De um lado", entram à esquerda "Carroceiro", "Cooperativa" e "Oficina", com setas para o pátio e o rótulo "trazem sucata"; em "Do outro", à direita, "Siderúrgica" e "Fundição", com setas saindo do pátio e o rótulo "levam material".] | De um lado, quem traz sucata: o carroceiro, a cooperativa, a oficina. Do outro, quem leva: a siderúrgica, a fundição. |
| [ILUSTRAÇÃO (cont.): em "o saldo", uma etiqueta "Saldo" aparece entre o pátio e cada lado; em "Quem está te devendo", uma etiqueta verde "te deve"; em "quem tem crédito", uma vermelha "tem crédito".] | E entre os dois fica o saldo: quem está te devendo, e quem tem crédito com você. É isso que a gente vai aprender a ler. |
| Volta para o app: Dashboard do EcoSistema, logado como Rafael Nogueira, menu lateral aberto. Cartão discreto: "Antes: Materiais e tabelas de preço". [BACKEND: semente `seeds-extra/t04/inicio`] | Se você ainda não viu o tutorial Materiais e tabelas de preço, dá uma olhada antes. |
| Clique no menu lateral em "Clientes e Fornecedores" (ícone de aperto de mão): abre a tela, aba "Clientes". Na frase "Eu recolho o menu", clique no botão de recolher do topo (ícone do painel, à esquerda): o menu vira só ícones e a lista alarga. | Tudo isso fica no menu, em Clientes e Fornecedores. Eu recolho o menu do lado, pra lista ficar mais larga. [pause] Vamos ver como a tela está organizada. |

### cap01 · Como a tela está organizada (vinheta: PARCEIROS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`, menu recolhido no `setup`), `/clientes-fornecedores` na aba "Clientes". O mouse passa por "Clientes" e "Fornecedores" (sem clicar); "Visão geral" fica visível do lado. | A tela tem duas listas, nas abas Clientes e Fornecedores. |
| [ILUSTRAÇÃO: cliente × fornecedor: dois cartões. Em "Cliente é pra quem a Recicla Vale vende", o cartão "Cliente" (ícone de fábrica, o da aba) com "sai material" (caminhão saindo do pátio) e "entra dinheiro" (moeda entrando); em "Fornecedor é de quem ela compra", o cartão "Fornecedor" (ícone de pessoas, o da aba) com "entra material" e "sai dinheiro".] | Cliente é pra quem a Recicla Vale vende: sai material, entra dinheiro. Fornecedor é de quem ela compra: entra material, sai dinheiro. |
| Volta para a tela. [ZOOM: a linha "Aços Quiririm Ltda" da lista "Clientes", do nome (com o CNPJ embaixo) até a etiqueta verde "R$ 4.870,00"] | Em cada linha ficam o nome, o documento e, na direita, o saldo, numa etiqueta colorida. Daqui a pouco a gente aprende a ler essa cor. |
| O mouse passa pela busca "Buscar cliente..." e pelos botões "Filtros" (funil) e "Ordenar" ao lado, sem abrir. | Em cima, a busca, que acha por nome, apelido, documento ou telefone. Do lado, os filtros e a ordem da lista. |
| Clique em "Aços Quiririm Ltda": a ficha abre à direita ("Aços Quiririm Ltda", "Cliente", "R$ 4.870,00", "a receber" e as abas). A câmera acompanha a ficha, sem zoom. | Clicando num parceiro, a ficha dele abre do lado. Ela tem um capítulo só dela, mais pra frente. |
| O mouse passa por "Relatório" e por "Novo Cliente", no alto à direita, sem clicar. | Lá em cima ficam o Relatório, com quem te deve e a quem você deve, e o botão de cadastrar, Novo Cliente. |
| Clique em "Fornecedores". O mouse para no ícone de telefone ao lado de "Aparecida Ramos": tooltip "Mesmo telefone em outro cadastro" / "Também está em: Cida Ramos". [ZOOM: o ícone e o tooltip] [TESTAR: no modo compacto o selo mostra só o ícone; o tooltip abre com o mouse parado] | Na aba Fornecedores, repara nesse telefone pequeno do lado do nome. É o aviso de mesmo telefone em outro cadastro. |
| Clique em "Buscar fornecedor..." e digita o telefone da Aparecida Ramos (ex.: "90000-1102"): ficam só "Aparecida Ramos" e "Cida Ramos". No fim da frase, apaga a busca e a lista volta inteira. | Uma dica: muitas vezes é a mesma pessoa cadastrada duas vezes, com nomes diferentes. Buscando pelo telefone, os dois aparecem juntos, e você confere. |
| Clique em "Visão geral": "Ranking do período" com "Clientes por venda" e "Fornecedores por compra"; rola até "Saldos de clientes" e "Saldos de fornecedores" ("a receber", "a pagar"). [BACKEND: RPCs `get_financial_dre_summary`, `list_top_clients_paginated`, `list_top_suppliers_paginated`, `get_clients_suppliers_inactive_count`, período "Este mês"] | E na Visão geral fica o resumo: quem mais comprou da Recicla, de quem ela mais comprou, e quanto há pra receber e pra pagar. |

### cap02 · Pessoa física e pessoa jurídica (vinheta: CADASTRO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), aba "Fornecedores". Clique em "Novo Fornecedor": janela "Novo Fornecedor", aba "Dados de Contato", bloco "Identificação e contato". | Agora, cadastrar. Chegou um fornecedor novo: o Rogério, eletricista, que traz fio de cobre e sucata de obra. Em Fornecedores, Novo Fornecedor. |
| Em "Nome *" digita "Rogério Alves Costa". | O único campo obrigatório é o Nome. |
| Em "Pessoa de Contato ou Apelido" digita "Rogério Eletricista". | Em Pessoa de Contato ou Apelido vai o jeito que o pátio chama ele: Rogério Eletricista. O apelido também entra na busca. |
| Em "Telefone" digita "12900002611" (a máscara mostra "(12) 90000-2611"); o mouse para em "Não possui telefone", sem marcar. [BACKEND: select com `ilike` do telefone ao sair do campo, sem resultado] | Depois, o telefone. Se a pessoa não tem telefone, como muito carroceiro, é só marcar Não possui telefone. |
| Em "Recebimento", "Chave PIX": digita "rogerio.costa@pix.example". | E a chave Pix dele, pra pagar as compras. |
| Rola a janela até "Saldo inicial" ("Comece com saldo zero ou registre um saldo de abertura." e "+ Adicionar saldo inicial"), sem clicar; passa pela caixa "Também é cliente" sem parar. | Lá embaixo fica o Saldo inicial. Se o parceiro já chega com um valor do caderno antigo, você registra aqui. O Rogério começa do zero. |
| Clique na aba "Dados Fiscais": "Tipo de Pessoa" com "Pessoa Física" marcado. Em "CPF" digita "41827356090" (aparece "418.273.560-90"). [ZOOM: "CPF" com o número, a frase toda] | Na aba Dados Fiscais, o tipo já vem em Pessoa Física, que é quem tem CPF, como o Rogério. Eu digito o CPF dele. |
| Clique em "Salvar" (com a palavra "Salvar"); toast "Fornecedor cadastrado com sucesso!"; a lista mostra "Rogério Alves Costa" (com o triângulo de incompleto). "Pronto" entra depois do toast. [BACKEND: `INSERT suppliers` (código novo, `portal_token`), RPC `set_partner_labels`; vira `apos-cap02`] | Salvar. Pronto, o Rogério já está na lista. |
| Clique em "Novo Fornecedor", aba "Dados Fiscais", clique em "Pessoa Jurídica": aparecem "CNPJ" (com a lupa), "Nome Fantasia", "Razão Social", "Inscrição Estadual", "Indicador IE *" e "Regime tributário do fornecedor"; a câmera desce por eles. Depois da frase, "Cancelar". | Pra empresa, é o mesmo cadastro, com Pessoa Jurídica. Aí aparecem o CNPJ, a razão social e a inscrição estadual. E o CNPJ tem um atalho. |

### cap03 · Buscar dados pelo CNPJ (vinheta: CADASTRO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`), aba "Fornecedores". "Novo Fornecedor"; em "Nome *" digita "Serralheria Bem-Te-Vi". | O atalho é a busca pelo CNPJ. Chegou mais um fornecedor: a Serralheria Bem-Te-Vi, que vende sobra de ferro e de alumínio pra Recicla Vale. |
| Aba "Dados Fiscais", "Pessoa Jurídica"; em "CNPJ" digita "46280719000124" (aparece "46.280.719/0001-24"). [ZOOM: "CNPJ" com o número, a frase toda] | Em Dados Fiscais, Pessoa Jurídica, e eu digito o CNPJ. |
| O mouse para na lupa à direita do CNPJ (tooltip "Buscar dados da empresa pelo CNPJ"); em "Um clique", clica: a lupa gira e sai o toast "Dados preenchidos — confira antes de salvar". [BACKEND: edge `cnpj-lookup` simulada para 46280719000124, ~1 s de espera, `{success: true, data: {razao_social: "BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA", nome_fantasia: "SERRALHERIA BEM-TE-VI", logradouro: "RUA DAS PALMEIRAS", numero: "", complemento: "", bairro: "JARDIM SANTA LUZIA", cidade: "TAUBATE", uf: "SP", cep: "12062150", phone: "12900002742", email: "contato@serralheriabemtevi.example", opcao_pelo_simples: true, opcao_pelo_mei: false}}`] | Do lado do CNPJ fica uma lupa: Buscar dados da empresa pelo CNPJ. Um clique, e o sistema consulta a Receita. |
| A câmera mostra "Nome Fantasia" ("SERRALHERIA BEM-TE-VI") e "Razão Social" ("BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA"). | Pronto. Vieram a razão social e o nome fantasia. |
| Rola até "Endereço Fiscal": "CEP" 12062-150, "Estado" SP, "Cidade" Taubaté, "Logradouro" "RUA DAS PALMEIRAS", "Bairro" "JARDIM SANTA LUZIA". [BACKEND: edge `ibge-cities` (SP, Taubaté 3554102)] [TESTAR: "TAUBATE" vira "Taubaté" com o código IBGE] | E o endereço: CEP, cidade, rua e bairro. |
| Clique em "Dados de Contato": "Nome *" continua "Serralheria Bem-Te-Vi"; "Telefone" "(12) 90000-2742"; "E-mail" "contato@serralheriabemtevi.example". | Em Dados de Contato entraram o telefone e o e-mail. E o nome que eu digitei ficou do jeito que estava. |
| Clique em "Dados Fiscais" e rola até o "Número", com a linha vermelha embaixo (sem zoom: o zoom é no cap. 4). | A tela pede pra conferir antes de salvar. E repara que um campo ficou vermelho. |

### cap04 · Dados fiscais e o campo vermelho (vinheta: FISCAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); o `setup` refaz fora do vídeo o formulário do cap. 3 (Novo Fornecedor, "Serralheria Bem-Te-Vi", "Dados Fiscais", "Pessoa Jurídica", CNPJ, lupa) e para em "Endereço Fiscal". [ZOOM: "Número" vazio e o aviso "Não veio da Receita — obrigatório para emitir NF-e", desta linha até o fim da seguinte] | O campo vermelho é o Número. A Receita não trouxe o número da serralheria. |
| (o zoom continua) | E o aviso explica: ele é obrigatório pra emitir nota fiscal. |
| [ILUSTRAÇÃO: a nota leva o endereço: um cartão simples de nota fiscal (não é o DANFE nem tela do app) com o bloco do parceiro: "Serralheria Bem-Te-Vi", "CNPJ 46.280.719/0001-24", "Rua das Palmeiras, nº ___", "Jardim Santa Luzia", "Taubaté, SP", "CEP 12062-150". Em "Sem o número", o "nº ___" pisca em vermelho e uma seta leva o cartão a um selo "SEFAZ" com "pode recusar"; em "Por isso a tela já cobra", volta para a tela.] | A nota leva o endereço completo do parceiro. Sem o número, a SEFAZ pode recusar a nota. Por isso a tela já cobra o que falta. |
| Clique em "Número", digita "418": a linha vermelha some. | Eu completo com o número, quatrocentos e dezoito, e o vermelho some. |
| Rola para cima até "Inscrição Estadual", "Indicador IE *" e "Regime tributário do fornecedor". Em "Indicador IE *" escolhe "Contribuinte ICMS" (o campo vira "Inscrição Estadual *" e libera) e digita "688412573032". | Aqui em cima ficam a inscrição estadual, o indicador e o regime do fornecedor. Quem define o que vai nesses campos é o contador. Eu preencho o que ele passou. |
| [ZOOM: "Regime tributário do fornecedor" em "Simples Nacional" e a linha "Preenchido pela consulta do CNPJ: a Receita informa que esta empresa é optante pelo Simples Nacional."] | O regime até veio na consulta: Simples Nacional. E é o regime da serralheria, não o da Recicla Vale. |
| Clique em "Salvar" (com a palavra); toast "Fornecedor cadastrado com sucesso!"; na lista, "Serralheria Bem-Te-Vi" com o ícone verde; o mouse para nele: "Pronto para emitir NF-e". [BACKEND: `INSERT suppliers` com `codigo_ibge` 3554102, `indicador_ie` 1, `inscricao_estadual`, `regime_tributario` simples_nacional; RPC `set_partner_labels`; vira `apos-cap04`] | Salvar. Na lista, a serralheria ganha o sinal verde: pronta pra emitir nota fiscal. |
| O mouse para no triângulo de "Rogério Alves Costa": tooltip "Faltam dados para emitir NF-e para este cadastro:" com "Logradouro", "Número", "Bairro", "Cidade", "UF", "CEP", "Código IBGE". | Já o Rogério, que a gente cadastrou sem endereço, aparece com o triângulo de incompleto. O aviso mostra o que falta pra nota. |
| Clique no botão "<n> incompletos" do alto: ficam "Valdir Pereira", "Aparecida Ramos", "Cida Ramos" e "Rogério Alves Costa"; o botão vira "Mostrar todos"; clique nele e a lista volta. [TESTAR: o botão aparece em 1280 px] | E o botão de incompletos, lá em cima, mostra só quem está com o cadastro pela metade. |
| A câmera abre na lista inteira, sem zoom. | Uma dica: quem não emite nota pode deixar a aba Dados Fiscais de lado. Só com o nome, o parceiro já tem histórico e saldo, e o aviso não trava compra nem venda. |

### cap05 · Cliente e fornecedor ao mesmo tempo (vinheta: SALDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`), aba "Fornecedores". Clique em "Serralheria Bem-Te-Vi": a ficha abre ao lado. | Agora, um caso comum no pátio. A serralheria vende sobra pra Recicla Vale, e também compra tubo e chapa usados aqui. Ela é fornecedora e cliente ao mesmo tempo. |
| Clique em "Editar": janela "Editar Fornecedor"; rola até a caixa "Também é cliente" ("Cria ou vincula também o cadastro de cliente.") e marca. | Pra isso, é só editar e marcar Também é cliente. |
| Clique em "Salvar"; toasts "Fornecedor atualizado!" e "Cadastro criado também como cliente."; a linha e a ficha ganham o selo roxo "Cliente+Fornecedor". [BACKEND: `UPDATE suppliers`; select em `customers` pelo `cpf_cnpj` (nenhum); `INSERT customers` com os mesmos dados; RPC `link_customer_supplier` (cria a linha `party`, zero); vira `apos-cap05`] | Salvar. A serralheria ganha o selo roxo, Cliente+Fornecedor, e passa a aparecer nas duas abas. |
| Clique em "Depósito Irmãos Siqueira": ficha com "Fornecedor", "Cliente+Fornecedor", "R$ 840,00" em vermelho e "a pagar". | E o saldo? Olha o Depósito Irmãos Siqueira, que já é cliente e fornecedor faz tempo. |
| [ILUSTRAÇÃO: saldo unificado: sob o nome "Depósito Irmãos Siqueira", duas colunas que entram com a frase: à esquerda "Compra de sucata · R$ 2.100,00 · a Recicla deve" (vermelho); à direita, em "E vendeu pra ele", "Venda de papelão e PET · R$ 1.260,00 · o depósito deve" (verde).] | Na semana passada, a Recicla comprou dois mil e cem reais de sucata dele, sem pagar na hora. E vendeu pra ele mil duzentos e sessenta reais de papelão e PET, também pra acertar depois. |
| [ILUSTRAÇÃO (cont.): as duas colunas se juntam na conta "2.100,00 − 1.260,00" e viram uma etiqueta só, vermelha: "Saldo único: a Recicla deve R$ 840,00".] | Em vez de dois saldos, fica um só, com a conta das duas coisas: a Recicla deve oitocentos e quarenta reais pro depósito. |
| Volta para a tela; clique em "Clientes". [ZOOM: a linha "Depósito Irmãos Siqueira", com "Cliente+Fornecedor" e "-R$ 840,00" em vermelho] | Na aba Clientes, ele aparece com esse mesmo saldo. O sinal muda de uma aba pra outra, mas a cor continua vermelha: a Recicla deve. |

### cap06 · Tabela de preço do parceiro (vinheta: PREÇOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), aba "Fornecedores". Clique em "Depósito Irmãos Siqueira" e em "Editar": janela "Editar Fornecedor", com o aviso azul no topo. | Agora, a tabela de preço. No tutorial de materiais, a gente criou a Tabela Depósitos. Vou ligar ela ao Depósito Irmãos Siqueira. |
| Na aba "Dados de Contato", "Tabela de Preços Padrão" mostra "Principal" (com a estrela); clique: lista com "Buscar tabela..."; clique em "Tabela Depósitos". | No Editar, em Tabela de Preços Padrão, ele estava na Principal. Eu troco pra Tabela Depósitos. |
| [ZOOM: o aviso azul "Mudanças em nome, CPF/CNPJ, contato, endereço e tabela de preços padrão refletem automaticamente no cadastro de cliente vinculado."] | Como o depósito também é cliente, o aviso azul lembra: a tabela vale pro cadastro de cliente dele também. |
| Clique em "Salvar"; toast "Fornecedor atualizado!". [BACKEND: `UPDATE suppliers.default_price_table_id` e o espelho no cliente vinculado (nome, CPF/CNPJ, contato, endereço, tabela de preços padrão); vira `apos-cap06`] | Salvar. Daqui pra frente, quando você escolher o depósito numa compra, os preços já vêm da Tabela Depósitos. |
| [ILUSTRAÇÃO: qual preço vale na compra: três degraus de cima pra baixo, que acendem com a frase: 1 "Preço especial do parceiro" (em "vale primeiro"), 2 "Tabela do parceiro, ex.: Tabela Depósitos" (em "Se não tiver"), 3 "Preço do material" (em "E por último"); uma seta desce pelos degraus.] | E se tiver preço especial? Na compra, vale primeiro o preço especial do parceiro. Se não tiver, a tabela dele. E por último, o preço do material. |
| Volta para a tela; na ficha do depósito, clique em "Preços": "Preços Personalizados" ("Preços de compra e de venda para Depósito Irmãos Siqueira"), com as abas "Compra" e "Venda". | O preço especial de cada parceiro fica na ficha dele, na aba Preços. |

### cap07 · A ficha do parceiro (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), aba "Fornecedores". Clique em "Cooperativa Recomeço": a ficha abre em "Visão geral". | Agora, a ficha. Vou abrir a Cooperativa Recomeço, que traz papelão, PET e latinha toda sexta. |
| A câmera no cabeçalho: "Cooperativa Recomeço", "Fornecedor", "R$ 2.550,00" em vermelho, "a pagar", "Editar", "Nova Movimentação" e "...". | No topo ficam o nome, o saldo e os botões de editar e de lançar uma movimentação. |
| O mouse passa pelas abas, da esquerda pra direita, sem clicar: "Visão geral", "Pedidos", "Conta-corrente", "Lucro estimado", "Financeiro", "Notas fiscais", "Preços". [TESTAR: as sete cabem sem rolagem lateral com o menu recolhido] | Embaixo, as abas: Visão geral, Pedidos, Conta-corrente, Lucro estimado, Financeiro, Notas fiscais e Preços. |
| Em "Visão geral": "Cadastro" (CPF/CNPJ, "Razão social", "Nome fantasia", "Inscrição estadual", "Contato") e "Contato e endereço". | Na Visão geral ficam os dados do cadastro, o contato e o endereço. |
| [ZOOM: "Acesso ao portal", com o link e o botão "Copiar"] | E o link do portal, pra cooperativa acompanhar o saldo de onde estiver. O portal depende do plano contratado. |
| O mouse para na aba "Lucro estimado", sem clicar. | O Lucro estimado só aparece pra quem é fornecedor, porque ele parte das compras. |

### cap08 · Os materiais que ele mais movimenta (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), ficha da "Cooperativa Recomeço". Clique em "Pedidos": "Total Comprado" R$ 52.937,50, "Total de Pedidos" 14, "Ticket Médio" R$ 3.781,25. [BACKEND: `purchases` com itens e `materials(name)`, as 14 compras do plano] | Em Pedidos fica o resumo das compras. Desde agosto, a Recicla fez catorze pedidos com a cooperativa. |
| Rola até "Top 5 Materiais Mais Comprados" (a rosca e a legenda). | O gráfico mostra os cinco materiais que ela mais traz. E ele conta o peso, em quilos. |
| [ZOOM: a legenda "Papelão: 59%", "Plástico PET: 18%", "Alumínio latinha: 9%", "Chaparia: 8%", "Ferro misto: 6%"] | O papelão sozinho é cinquenta e nove por cento de tudo que chega da cooperativa. |
| [ILUSTRAÇÃO: peso × valor: à esquerda, uma pilha alta de fardos de papelão com "59% do peso"; em "Já a latinha", à direita, um saco pequeno de latinhas com "9% do peso"; em "o quilo da latinha vale", as etiquetas "R$ 6,20 o quilo" no saco e "R$ 0,55 o quilo" na pilha.] | Já a latinha é só nove por cento do peso. Mas o quilo da latinha vale seis e vinte, e o do papelão, cinquenta e cinco centavos. |
| Volta para a tela; o mouse para em "Período", na faixa das abas, sem abrir; rola até "Histórico de Pedidos" ("Nº Pedido", "Tipo", "Valor", "Pagamento", "Data"). | No Período, dá pra olhar um mês só. E embaixo fica cada pedido, com o valor e a data. |

### cap09 · Conta-corrente: saldo e extrato (vinheta: SALDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), ficha da "Cooperativa Recomeço". Clique em "Conta-corrente": "Saldo Atual" "R$ 2.550,00" em vermelho e "Você deve a Cooperativa Recomeço". [ZOOM: o valor e a frase, desta linha até o fim da seguinte] | Agora, a conta-corrente. A cooperativa entregou na sexta, e a Recicla ainda não acertou tudo: deve dois mil quinhentos e cinquenta reais pra ela. |
| (o zoom continua) | Por isso o valor está em vermelho, com a frase: Você deve a Cooperativa Recomeço. |
| [ILUSTRAÇÃO: os quatro casos do saldo: no topo, "Do lado da Recicla Vale" e a regra "verde = dinheiro pra receber · vermelho = dinheiro pra pagar", que entram com a frase; embaixo, uma grade 2×2 ainda apagada: linhas "Cliente" e "Fornecedor", colunas "positivo (+)" e "negativo (−)".] | Uma dica: pra ler qualquer saldo, pensa sempre do lado da Recicla Vale. Verde é dinheiro pra receber. Vermelho é dinheiro pra pagar. |
| [ILUSTRAÇÃO (cont.): acendem "Cliente +" verde "ele te deve" e, em "Saldo negativo", "Cliente −" vermelho "ele adiantou: você deve a ele".] | No cliente, saldo positivo é verde: ele te deve. Saldo negativo é vermelho: ele adiantou dinheiro, e você deve a ele. |
| [ILUSTRAÇÃO (cont.): acendem "Fornecedor +" vermelho "você deve a ele", com a etiqueta "Cooperativa Recomeço" em "como aqui", e, em "Negativo é verde", "Fornecedor −" verde "você adiantou: ele te deve".] | No fornecedor é ao contrário. Positivo é vermelho: você deve a ele, como aqui. Negativo é verde: você adiantou, e ele te deve. |
| Volta para a tela; rola até "Histórico de Movimentações": linhas "Pedido" (forma "Saldo") e "Pagamento" ("Pix/Transferência"), com "Saldo Final". | Embaixo fica o extrato: cada pedido que ficou pra acertar e cada pagamento, com o saldo depois de cada um. |
| Clique em "Movimentação": janela "Nova Movimentação de Saldo" ("Registre um pagamento ou cobrança para Cooperativa Recomeço"); em "Tipo de Operação", "Pagar" já marcado ("Você pagou ao fornecedor - Reduz o saldo dele com você"). Sem zoom no "Saldo Atual" da janela. | Hoje a Recicla vai acertar uma parte. Em Movimentação, o tipo já vem em Pagar. |
| Em "Valor *" digita "1200" (aparece "R$ 1.200,00"). [ZOOM: "Valor *" com o valor] | O valor: mil e duzentos reais. |
| Em "Forma de Pagamento" clica em "Pix/Transferência" (se já não estiver marcado); "Conta bancária" mostra a conta principal; em "Observação" digita "Acerto parcial da entrega de 06/11". | A forma de pagamento é Pix ou transferência, saindo da conta da empresa. Em Observação, eu anoto o motivo. |
| Clique em "Confirmar" (com a palavra); toast "Movimentação registrada com sucesso!"; "Saldo Atual" vira "R$ 1.350,00"; no topo do extrato, "Valor Pago a Cooperativa Recomeço · Acerto parcial da entrega de 06/11", "Pagamento", "Pix/Transferência", "−R$ 1.200,00", "Saldo Final" "R$ 1.350,00". [ZOOM: "Saldo Atual" "R$ 1.350,00", depois do toast] [BACKEND: RPCs `create_manual_bank_transaction` e `update_balance`, `INSERT balance_movements`; vira `apos-cap09`] | Confirmar. O saldo cai pra mil trezentos e cinquenta reais, e o pagamento entra no extrato. |
| Clique em "Exportar": menu "Abrir Relatório (PDF)" e "Baixar Excel (.xlsx)"; não clica (Esc). | E no Exportar, o extrato sai em PDF ou em planilha, pra mandar pro parceiro. |

### cap10 · Lucro estimado (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), ficha da "Cooperativa Recomeço". Clique em "Lucro estimado": o período mostra "Este mês"; em "Eu escolho", abre e clica em "Mês passado"; a tabela "Margem estimada por material" carrega. [BACKEND: RPC `get_supplier_profit_estimate` com as cinco linhas de outubro do plano] | Agora, o Lucro estimado: quanto cada material dessa cooperativa deixa pra Recicla Vale. Eu escolho o Mês passado, outubro inteiro. |
| [ZOOM: as linhas "Alumínio latinha" e "Papelão" da tabela, desta linha até o fim da seguinte; o mouse aponta "Preço Médio Compra" R$ 6,20, "Preço Médio Venda" R$ 7,40 e "Margem R$/kg" R$ 1,20 da latinha] | Olha a latinha: a Recicla pagou seis e vinte o quilo e vendeu, em média, a sete e quarenta. Sobra um e vinte por quilo, e essa diferença é a margem. |
| (o zoom continua; o mouse vai para "Margem Total" R$ 2.100,00 do papelão) | E o papelão, que vale pouco, dá a maior margem no total, porque vem muito: dois mil e cem reais no mês. |
| A câmera abre nos cartões "Custo total comprado" R$ 18.755,00, "Margem estimada total" R$ 5.998,00 e "Margem média %" 24,2%; o mouse para no do meio. | Somando tudo, a margem estimada da cooperativa em outubro foi de cinco mil novecentos e noventa e oito reais. |
| [ZOOM: o aviso âmbar "Estimativa — sucata é fungível; a margem é calculada sobre o preço médio de venda do material no período, não é lucro realizado."] | Uma dica: esse número é uma estimativa, não é dinheiro no bolso. O aviso da tela diz: sucata é fungível. |
| [ILUSTRAÇÃO: sucata é fungível: três origens, "Cooperativa Recomeço", "Dona Cida" e "outros", jogam latinhas num fardo só, "Alumínio latinha"; em "Na venda", o fardo sai inteiro para "Serra Fina".] | Fungível quer dizer que se mistura. A latinha da cooperativa vai pro mesmo fardo da latinha da Dona Cida e de todo mundo. Na venda, ninguém separa de quem era cada lata. |
| [ILUSTRAÇÃO (cont.): sobre o fardo, "venda média no mês: R$ 7,40 o quilo"; ao lado, "compra da cooperativa: R$ 6,20 o quilo" e o resultado "margem estimada: R$ 1,20 o quilo", com um carimbo "estimativa".] | Por isso a margem usa o preço médio de venda do material no mês. Ela não vai bater com o extrato, e tudo bem: ela mostra quanto cada material desse fornecedor rende. |

### cap11 · Financeiro e notas fiscais (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), ficha da "Cooperativa Recomeço". Clique em "Financeiro": "Receitas vinculadas" R$ 120,00, "Despesas vinculadas" R$ 450,00 e a lista "Despesas & Receitas". [BACKEND: `cash_transactions` e `financial_bills` com `partner_type` supplier e `partner_id` da cooperativa, com `category:financial_categories(name, color)`] | Agora, o Financeiro. Aqui ficam as despesas e as receitas avulsas ligadas ao parceiro, o que não é compra nem venda. |
| [ZOOM: as duas linhas: "Despesa" "Frete das entregas de outubro" R$ 450,00 e "Receita" "Venda de sacos de ráfia usados" R$ 120,00] | Na cooperativa, o frete das entregas de outubro, quatrocentos e cinquenta reais, e uma venda de sacos de ráfia usados, cento e vinte. |
| A câmera abre na aba inteira, sem zoom. | Elas aparecem aqui quando a despesa ou a receita é lançada com o nome do parceiro. |
| Clique em "Notas fiscais": "Notas Fiscais" e "Nenhuma nota fiscal para este parceiro.". [BACKEND: `invoices` vazia para a cooperativa] | E em Notas fiscais ficam as notas desse parceiro. A cooperativa ainda não tem nenhuma. A emissão de nota depende do plano contratado e tem um tutorial só dela. |

### cap12 · Relatório de saldos (vinheta: SALDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), `/clientes-fornecedores`. Clique em "Relatório": janela "Relatório de Saldos" ("Visualize todos os saldos a receber e a pagar"). [BACKEND: `balances` com `balance_movements(created_at)` do mais novo, `.neq('balance', 0)`, ordem por saldo] | Pra fechar, a pergunta do dia a dia: quem te deve, e quanto? Lá em cima, Relatório. |
| [ZOOM: o bloco "A Receber" (título, "Total: R$ 5.170,00" e as duas linhas), desta linha até o fim da terceira; o mouse aponta o total] | Em A Receber fica tudo que vai entrar: cinco mil cento e setenta reais. |
| (o zoom continua; o mouse aponta "Aços Quiririm Ltda", "Cliente", "R$ 4.870,00" em verde) | A Aços Quiririm é cliente, com saldo positivo e verde: ela te deve quatro mil oitocentos e setenta reais. |
| (o zoom continua; o mouse aponta "Valdir Pereira", "Fornecedor", "-R$ 300,00" em verde) | O Valdir é fornecedor, com saldo negativo, também verde. A Recicla adiantou trezentos reais pra ele, e ele paga em sucata. |
| Rola até "A Pagar". [ZOOM: o bloco "A Pagar" (título, "Total: R$ 3.690,00" e as três linhas), desta linha até o fim da quarta; o mouse aponta o total] | Em A Pagar fica o que vai sair: três mil seiscentos e noventa reais. |
| (o zoom continua; o mouse aponta "Cooperativa Recomeço", "Fornecedor", "R$ 1.350,00" em vermelho) | A cooperativa é fornecedora, com saldo positivo e vermelho: são os mil trezentos e cinquenta reais que ficaram do acerto de hoje. |
| (o zoom continua; o mouse aponta "Depósito Irmãos Siqueira", "Cliente+Fornecedor", "-R$ 840,00" em vermelho) | O depósito aparece uma vez só, como Cliente+Fornecedor, com o saldo único. |
| (o zoom continua; o mouse aponta "Serra Fina Alumínio Reciclagem", "Cliente", "-R$ 1.500,00" em vermelho) | E a Serra Fina é cliente, com saldo negativo e vermelho. Ela adiantou mil e quinhentos reais pela próxima carga de alumínio, e agora a Recicla deve essa carga pra ela. |
| Clique em "Exportar Relatório": menu "Exportar em PDF" e "Exportar em Excel"; não clica (Esc). | No Exportar Relatório, a lista sai em PDF ou em planilha. |
| Clique no olho da linha "Aços Quiririm Ltda": a janela fecha e abre a ficha cheia ("Clientes e Fornecedores › Aços Quiririm Ltda", "Saldo: R$ 4.870,00 (Aços Quiririm Ltda te deve)"), na aba "Conta-Corrente do Cliente", com o extrato. [BACKEND: `/balance/customer/<id>` → `/saldo/...` → `/cliente/<nome>-<código>?tab=conta-corrente`] [TESTAR: a ficha cheia abre na aba da conta-corrente] | E no olho, você abre a conta-corrente do parceiro, com o extrato completo. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a lista de fornecedores e a janela "Novo Fornecedor" do Rogério (trechos dos caps. 1 e 2). | Pronto! Recapitulando: a gente viu como a tela de clientes e fornecedores está organizada e cadastrou o Rogério, pessoa física. |
| Montagem rápida: a lupa do CNPJ e o "Número" vermelho virando 418 (caps. 3 e 4). | Cadastrou a serralheria com a busca pelo CNPJ e completou o campo vermelho que a nota fiscal pede. |
| Montagem rápida: "Também é cliente", o selo "Cliente+Fornecedor" e a "Tabela Depósitos" (caps. 5 e 6). | Marcou a serralheria como cliente e fornecedor, entendeu o saldo único e ligou a Tabela Depósitos ao depósito. |
| Montagem rápida: as abas da ficha, o gráfico, o pagamento e o "Lucro estimado" (caps. 7 a 10). | Abriu a ficha da cooperativa, leu o gráfico de materiais, lançou um pagamento na conta-corrente e viu o lucro estimado. |
| Montagem rápida: o "Relatório de Saldos" (cap. 12). | E fechou com o relatório de quem te deve e a quem você deve. |
| Cartão "Próximo: Balança e impressora: o EcoTray"; cartela final. | No próximo tutorial, a balança e a impressora passam a conversar com o sistema, pelo EcoTray. Até lá! |
