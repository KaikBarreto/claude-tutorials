# Roteiro T4 · Clientes, fornecedores e a ficha do parceiro

Roteiro pronto para gerar a voz e gravar (molde da Domiflix; o Kaik ajusta depois se precisar). Coluna Fala = texto da
narração (voz Kaik Barreto), na grafia da legenda; a grafia de pronúncia do TTS está em `narracao/tts_textos.py` (uma linha
da tabela = uma linha do texto). Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como no
código 1.60.18 (`T04/inventario.md`). Mundo, sementes e simulações: `T04/plano.md`.

- **Título:** Clientes, fornecedores e a ficha do parceiro
- **Antes:** Materiais e tabelas de preço (T3)
- **Próximo:** Balança e impressora: o EcoTray (T5)
- **Vinhetas (áreas):** PARCEIROS · CADASTRO · CADASTRO · FISCAL · FISCAL · FISCAL · SALDO · PREÇOS · PARCEIROS · FICHA · FICHA ·
  SALDO · SALDO · FICHA · FICHA · SALDO · RESUMO (todos os capítulos, menos o 0)
- **Duração estimada:** ~28 min de vídeo (3.238 palavras, ~20,8 min de fala a 2,6 palavras/s, mais 17 vinhetas, as
  ilustrações e as esperas de tela). Era ~15 min no 1.59.154: a aula cresceu (Kaik, 18/11: "cobrir cada função e caso de uso";
  nenhuma aula se divide). Voz: ~18.100 caracteres com os títulos das vinhetas.
- **Capítulos (20/11, 1.60.18, renumerados):** 0 Abertura · 1 Tela · 2 Pessoa física/jurídica (+ caixinhas do comprovante, saldo
  inicial) · 3 CNPJ · 4 O que falta pra emitir nota (refeito, com a inscrição pela Sintegra e o CEP do Rogério) · **5 Empresa do
  Lucro Real (novo)** · **6 Os avisos da consulta (novo)** · 7 Cliente e fornecedor (era 5) · 8 Tabela de preço (era 6, + preço
  especial) · **9 Organizar a lista (novo)** · 10 Ficha (era 7) · 11 Materiais (era 8) · 12 Conta-corrente (era 9, Exportar com o
  PDF na tela) · **13 Ajustes na conta-corrente (novo)** · 14 Lucro estimado (era 10) · 15 Financeiro (era 11) · 16 Relatório de
  saldos (era 12) · 17 Recapitulando (era 13).
- **Gravação:** computador, janela **1600×900** (16:9; fora do modo compacto da lista, que só vale até 820 px de altura: os selos
  da lista voltam com texto), Rafael Nogueira (administrador), `FAKE_NOW=2026-11-10T08:30:00-03:00`. Do cap. 1 em diante o `setup`
  recolhe o menu lateral e cada capítulo abre um navegador novo na semente indicada.
- Marcas na Tela: `[ZOOM: ...]` (dura a frase inteira da linha, ou as linhas indicadas, nunca um em cima do outro),
  `[ILUSTRAÇÃO: ...]` (desenho por código no estilo da marca, no lugar da tela, enquanto a frase corre),
  `[BACKEND: ...]` (o que o backend falso precisa ter), `[TESTAR: ...]` (o robô confere antes de gravar),
  `[PDF NA TELA: ...]` (o app abre PDF/extrato em aba nova e a gravação filma uma aba só; o robô devolve o conteúdo da aba e o
  coordenador monta a cena, `"tipo": "comprovante"`, `"cena": "pdf"` em `cenas/ilustracoes.json`).

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
| Clique em "Buscar fornecedor..." e digita o telefone da Aparecida Ramos (ex.: "90000-1102"): ficam só "Aparecida Ramos" e "Cida Ramos". No fim da frase, apaga a busca e a lista volta inteira. | Uma dica: muitas vezes é a mesma pessoa cadastrada duas vezes, com nomes diferentes. Buscando pelo telefone, os dois aparecem juntos, e você confere. E na hora de cadastrar, a tela já avisa quando o telefone ou o documento que você digitou já existem. |
| Clique em "Visão geral": "Ranking do período" com "Clientes por venda" e "Fornecedores por compra"; rola até "Saldos de clientes" e "Saldos de fornecedores" ("a receber", "a pagar"). [BACKEND: RPCs `get_financial_dre_summary`, `list_top_clients_paginated`, `list_top_suppliers_paginated`, `get_clients_suppliers_inactive_count`, período "Este mês"] | E na Visão geral fica o resumo: quem mais comprou da Recicla, de quem ela mais comprou, e quanto há pra receber e pra pagar. |

### cap02 · Pessoa física e pessoa jurídica (vinheta: CADASTRO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `inicio`), aba "Fornecedores". Clique em "Novo Fornecedor": janela "Novo Fornecedor", aba "Dados de Contato", bloco "Identificação e contato". | Agora, cadastrar. Chegou um fornecedor novo: o Rogério, eletricista, que traz fio de cobre e sucata de obra. Em Fornecedores, Novo Fornecedor. |
| Em "Nome *" digita "Rogério Alves Costa". | O único campo obrigatório é o Nome. Eu escrevo Rogério Alves Costa. |
| Em "Pessoa de Contato ou Apelido" digita "Rogério Eletricista". | Em Pessoa de Contato ou Apelido vai o jeito que o pátio chama ele: Rogério Eletricista. O apelido também entra na busca. |
| Em "Telefone" digita "12900002611" (a máscara mostra "(12) 90000-2611"); o mouse para em "Não possui telefone", sem marcar. [BACKEND: select com `ilike` do telefone ao sair do campo, sem resultado] | Depois, o telefone. Se a pessoa não tem telefone, como muito carroceiro, é só marcar Não possui telefone. |
| Em "Recebimento", "Chave PIX": digita "rogerio.costa@pix.example". | E a chave Pix dele, pra pagar as compras. |
| O mouse volta do Pix e passa por "Mostrar o telefone no comprovante" e por "Mostrar a chave PIX no comprovante", sem marcar. | E repara nas caixinhas de Mostrar no comprovante: elas decidem se o telefone e a chave Pix do parceiro saem impressos no comprovante. |
| Rola a janela até "Saldo inicial" ("Comece com saldo zero ou registre um saldo de abertura."); clique em "+ Adicionar saldo inicial": "Tipo de saldo" ("Eu devo a ele (a pagar)" e "Ele me deve (a receber)") e "Valor"; o mouse passa pelas duas opções, sem marcar; clique em "Remover saldo inicial" (o bloco fecha); passa pela caixa "Também é cliente" sem parar. [TESTAR: o rótulo do botão que fecha o bloco na criação é "Remover saldo inicial"] | Lá embaixo fica o Saldo inicial. Se o parceiro já chega com um valor do caderno antigo, você escolhe o lado, eu devo a ele ou ele me deve, e põe o valor. O Rogério começa do zero, então eu deixo sem. |
| Clique na aba "Dados Fiscais": "Tipo de Pessoa" com "Pessoa Física" marcado. Em "CPF" digita "41827356090" (aparece "418.273.560-90"). [ZOOM: "CPF" com o número, a frase toda] | Na aba Dados Fiscais, o tipo já vem em Pessoa Física, que é quem tem CPF, como o Rogério. Eu digito o CPF dele. |
| Clique em "Salvar" (com a palavra "Salvar"); toast "Fornecedor cadastrado com sucesso!"; a lista mostra "Rogério Alves Costa" (com o triângulo de incompleto). "Pronto" entra depois do toast. [BACKEND: `INSERT suppliers` (código novo, `portal_token`), RPC `set_partner_labels`; vira `apos-cap02`] | Salvar. Pronto, o Rogério já está na lista. |
| Clique em "Novo Fornecedor" (a janela abre limpa: o "Rascunho encontrado" depois de salvar foi corrigido no 1.60.18) , aba "Dados Fiscais", clique em "Pessoa Jurídica": aparecem "CNPJ" (com a lupa), "Nome Fantasia", "Razão Social", "Inscrição Estadual", "Indicador IE *" e "Regime tributário do fornecedor"; a câmera desce por eles. Depois da frase, "Cancelar". | Pra empresa, é o mesmo cadastro, com Pessoa Jurídica. Aí aparecem o CNPJ, a razão social e a inscrição estadual. E o CNPJ tem um atalho. |

### cap03 · Buscar dados pelo CNPJ (vinheta: CADASTRO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`), aba "Fornecedores". "Novo Fornecedor"; em "Nome *" digita "Serralheria Bem-Te-Vi". | O atalho é a busca pelo CNPJ. Chegou mais um fornecedor: a Serralheria Bem-Te-Vi, que vende sobra de ferro e de alumínio pra Recicla Vale. |
| Aba "Dados Fiscais", "Pessoa Jurídica"; em "CNPJ" digita "46280719000124" (aparece "46.280.719/0001-24"). [ZOOM: "CNPJ" com o número, a frase toda] | Em Dados Fiscais, Pessoa Jurídica, e eu preencho o CNPJ. |
| O mouse para na lupa à direita do CNPJ (dica do botão, na tela: "Buscar dados da empresa pelo CNPJ"); em "Um clique", clica: a lupa gira e sai o toast "Dados preenchidos — confira antes de salvar". [BACKEND: edge `cnpj-lookup` simulada para 46280719000124, ~1 s de espera, `{success: true, data: {razao_social: "BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA", nome_fantasia: "SERRALHERIA BEM-TE-VI", logradouro: "RUA DAS PALMEIRAS", numero: "", complemento: "", bairro: "JARDIM SANTA LUZIA", cidade: "TAUBATE", uf: "SP", cep: "12062150", phone: "12900002742", email: "contato@serralheriabemtevi.example", opcao_pelo_simples: true, opcao_pelo_mei: false, regime_ecf: null, regime_ecf_ano: null}}`; a lupa também consulta a inscrição estadual direto do navegador: `GET publica.cnpj.ws/cnpj/46280719000124` devolve a IE 688412573032 em SP e RPC `registrar_consulta_cnpj_ie`] | Do lado do CNPJ fica uma lupa: Buscar dados da empresa pelo CNPJ. Um clique, e o sistema consulta a Receita e o cadastro de inscrição estadual. |
| A caixa âmbar "Falta isto para emitir NF-e (1)" aparece no topo da janela, junto com o toast; a câmera mostra "Nome Fantasia" ("SERRALHERIA BEM-TE-VI") e "Razão Social" ("BEM-TE-VI SERRALHERIA E ESTRUTURAS LTDA"). | Pronto. A tela pede pra conferir antes de salvar. Vieram a razão social e o nome fantasia. |
| Rola até "Endereço Fiscal": "CEP" 12062-150 (já com a máscara: corrigido no 1.60.18), "Estado" SP, "Cidade" Taubaté, "Logradouro" "RUA DAS PALMEIRAS", "Bairro" "JARDIM SANTA LUZIA". [BACKEND: edge `ibge-cities` (SP, Taubaté 3554102)] [TESTAR: "TAUBATE" vira "Taubaté" com o código IBGE] | E o endereço: CEP, cidade, rua e bairro. |
| Em "Dados de Contato": "Nome *" continua "Serralheria Bem-Te-Vi"; "Telefone" "(12) 90000-2742"; "E-mail" "contato@serralheriabemtevi.example". | Em Dados de Contato entraram o telefone e o e-mail. E o nome que eu digitei ficou do jeito que estava. |
| Clique em "Dados de Contato" (a caixa fica fixa no topo, agora com "Número (Dados Fiscais)"). [ZOOM: a caixa "Falta isto para emitir NF-e (1)", "Dá para salvar o cadastro assim, mas a nota não sai até preencher." e o link "Número (Dados Fiscais)"] (o capítulo fecha aqui, em Dados de Contato) | E repara nesse aviso amarelo, em cima: falta um campo pra emitir nota fiscal. |

### cap04 · O que falta pra emitir nota (vinheta: FISCAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); o `setup` refaz fora do vídeo o cap. 3 (Novo Fornecedor, "Serralheria Bem-Te-Vi", "Dados Fiscais", "Pessoa Jurídica", CNPJ, lupa) e para em "Dados de Contato" com a caixa âmbar no topo. [ZOOM: a caixa "Falta isto para emitir NF-e (1)" com o link "Número (Dados Fiscais)"] [BACKEND: o mesmo da cap. 3, mais `publica.cnpj.ws` e `registrar_consulta_cnpj_ie`] | O aviso amarelo lista o que a nota fiscal exige e a consulta não trouxe. Aqui, só o Número. |
| Clique em "Número (Dados Fiscais)": a janela troca para "Dados Fiscais" e o cursor cai em "Número", com a linha vermelha "Não veio da Receita — obrigatório para emitir NF-e". [ZOOM: o campo e a linha vermelha, até o fim da linha] | Clicando no nome do campo, a tela me leva direto pra ele. E a linha vermelha explica: o Número é obrigatório pra emitir nota fiscal. |
| [ILUSTRAÇÃO: a nota leva o endereço: um cartão simples de nota fiscal (não é o DANFE nem tela do app) com o bloco do parceiro: "Serralheria Bem-Te-Vi", "CNPJ 46.280.719/0001-24", "Rua das Palmeiras, nº ___", "Jardim Santa Luzia", "Taubaté, SP", "CEP 12062-150". Em "Sem o número", o "nº ___" pisca em vermelho e uma seta leva o cartão a um selo "SEFAZ" com "pode recusar"; em "Por isso a tela já cobra", volta para a tela.] | A nota leva o endereço completo do parceiro. Sem o número, a SEFAZ pode recusar a nota. Por isso a tela já cobra o que falta. |
| Digita "418" em "Número": a linha vermelha e a caixa âmbar somem. | Eu completo com o número, quatrocentos e dezoito, e o aviso some. |
| Rola até "Inscrição Estadual". [ZOOM: "A Sintegra informa IE 688412573032 para este CNPJ em SP. A ficha está marcada como Não Contribuinte." e o link "Usar a da Sintegra"] | Agora, a inscrição estadual. A consulta também foi buscar esse número no cadastro do estado, e achou. |
| Clique em "Usar a da Sintegra": "Inscrição Estadual *" recebe 688412573032, "Indicador IE *" vira "Contribuinte ICMS" e a frase muda para "Preenchido pela consulta do CNPJ: a Sintegra informa a inscrição estadual 688412573032 para este CNPJ em SP.". [ZOOM: os dois campos] | Um clique em Usar a da Sintegra preenche a inscrição e já marca a serralheria como contribuinte de ICMS. Os dois campos andam juntos, do jeito que a nota pede. |
| [ZOOM: "Regime tributário do fornecedor" em "Simples Nacional" e a frase "Preenchido pela consulta do CNPJ: a Receita informa que esta empresa é optante pelo Simples Nacional."] | O regime também veio: Simples Nacional. E é o regime da serralheria, não o da Recicla Vale. |
| A câmera abre na aba inteira, sem zoom. | Uma dica: a consulta adianta o trabalho, mas quem confirma inscrição e regime é o contador. Na dúvida, manda a ficha pra ele antes da primeira nota. |
| Clique em "Salvar" (com a palavra); toast "Fornecedor cadastrado com sucesso!"; na lista, "Serralheria Bem-Te-Vi" com o ícone verde; o mouse para nele: "Pronto para emitir NF-e". [BACKEND: `INSERT suppliers` com `codigo_ibge` 3554102, `indicador_ie` 1, `inscricao_estadual` 688412573032, `regime_tributario` simples_nacional; RPC `set_partner_labels`; vira `apos-cap04`] | Salvar. Na lista, a serralheria ganha o sinal verde: pronta pra emitir nota fiscal. |
| O mouse para no triângulo de "Rogério Alves Costa": tooltip "Faltam dados para emitir NF-e para este cadastro:" com "Logradouro", "Número", "Bairro", "Cidade", "UF", "CEP", "Código IBGE". | Já o Rogério, que a gente cadastrou sem endereço, aparece com o triângulo de incompleto. O aviso mostra o que falta pra nota. |
| Clique em "Rogério Alves Costa", "Editar", aba "Dados Fiscais"; em "CEP" digita "12062150" (aparece "12062-150"): "Estado" SP, "Cidade" Taubaté, "Logradouro" e "Bairro" entram sozinhos; em "Número" digita "77"; "Salvar"; toast "Fornecedor atualizado!"; o triângulo vira o sinal verde. [BACKEND: edge `cep-lookup` para 12062150 (Rua das Palmeiras, Jardim Santa Luzia, Taubaté, SP, IBGE 3554102); `UPDATE suppliers` do Rogério] [TESTAR: o código IBGE entra com a cidade e o triângulo some] | Pra completar, é só editar. Eu digito o CEP, e a cidade, a rua e o bairro vêm sozinhos. Ponho o número, salvo, e o Rogério também fica pronto pra nota. |
| Clique no botão "<n> incompletos" do alto: ficam "Valdir Pereira", "Aparecida Ramos" e "Cida Ramos"; o botão vira "Mostrar todos"; clique nele e a lista volta. [TESTAR: o botão aparece em 1600 px] | E o botão de incompletos, lá em cima, mostra só quem ainda está com o cadastro pela metade. |
| A câmera abre na lista inteira, sem zoom. | Uma dica: quem não emite nota pode deixar a aba Dados Fiscais de lado. Só com o nome, o parceiro já tem histórico e saldo, e o aviso não trava compra nem venda. |

### cap05 · Empresa do Lucro Real (vinheta: FISCAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`), aba "Clientes". Clique em "Aços Quiririm Ltda" e em "Editar": janela "Editar Cliente"; aba "Dados Fiscais". [BACKEND: na semente `inicio` a Aços tem a inscrição com um dígito trocado (688.042.819.111), `regime_tributario` nulo e `is_industry` falso] | Agora, um cliente grande. A Aços Quiririm é uma siderúrgica, e a Recicla Vale emite nota fiscal pra ela. Em empresa assim, três campos decidem se a nota sai certa. Vou abrir o cadastro dela, no Editar, em Dados Fiscais. |
| O mouse para na lupa do CNPJ; clique: a lupa gira; toast "Dados preenchidos — confira antes de salvar". [BACKEND: `cnpj-lookup` do CNPJ 98.463.027/0001-15 com o endereço que a ficha já tem, `opcao_pelo_simples: false`, `opcao_pelo_mei: false`, `regime_ecf: "lucro_real"`, `regime_ecf_ano: 2024`; `publica.cnpj.ws` com a IE certa em SP] | A lupa também serve pra conferir um cadastro antigo. Um clique, e o sistema consulta de novo. |
| [ZOOM: embaixo de "Inscrição Estadual": "A Sintegra informa IE 688042711117 para este CNPJ em SP. A ficha tem 688.042.819.111." e o link "Usar a da Sintegra"] | Primeiro, a inscrição estadual. Olha o aviso: o número que estava na ficha é diferente do que o estado informa. Alguém digitou errado lá atrás. |
| (o zoom continua) | Repara que o sistema não trocou nada sozinho. Ele mostra os dois números e deixa a escolha com você. |
| Clique em "Usar a da Sintegra": o campo troca e a frase vira "Preenchido pela consulta do CNPJ: a Sintegra informa a inscrição estadual 688042711117 para este CNPJ em SP.". | Eu clico em Usar a da Sintegra, e a ficha fica com o número certo. Inscrição errada pode fazer a nota ser recusada. |
| Clique em "Indicador IE *": lista "Contribuinte ICMS", "Isento de Inscrição", "Não Contribuinte"; o mouse passa pelas três; fecha em "Contribuinte ICMS". [ZOOM: a lista e a ajuda "Contribuinte ICMS exige Inscrição Estadual; Isento/Não Contribuinte não."] | Segundo, o Indicador. Contribuinte de ICMS é a empresa que tem inscrição estadual, como a siderúrgica. Isento de Inscrição é a empresa que o estado dispensou. E Não Contribuinte é quem não tem inscrição, como a pessoa física. |
| (o zoom continua) | Só o contribuinte leva o número da inscrição. Nos outros dois, o campo fica travado, e tem que ficar vazio mesmo. |
| [ZOOM: "Regime tributário do cliente" em "Lucro Real" e a frase "Preenchido pela consulta do CNPJ: na escrituração de 2024 esta empresa declarou Lucro Real. Confirme com o contador se mudou desde então."] | Terceiro, o regime tributário do cliente. A consulta preencheu Lucro Real, e disse de onde tirou: da escrituração de dois mil e vinte e quatro. |
| (o zoom continua) | Esse dado vem com atraso. Por isso a tela pede: confirma com o contador se mudou desde então. |
| Clique no seletor: "Não informado", "Simples Nacional", "MEI", "Lucro Presumido", "Lucro Real"; fecha sem trocar. | As opções são Simples Nacional, MEI, Lucro Presumido e Lucro Real. E tem o Não informado: se você não sabe, deixa assim. O sistema não chuta regime. |
| [ZOOM: a ajuda "É o regime de quem compra de você, não o da sua empresa — esse fica em Configuração Fiscal → Impostos."] | Uma dica: aqui vai o regime da Aços Quiririm, não o da Recicla Vale. O da sua empresa fica na Configuração Fiscal, e a gente vê no tutorial de nota fiscal. |
| Rola até "É Indústria" ("Ativa diferimento de ICMS automático nas vendas") e "É uma Reciclagem". Clique em "É Indústria": liga. [ZOOM: os dois interruptores] | No cadastro de cliente tem mais dois botões. É Indústria: ligado, ele ativa o diferimento de ICMS automático nas vendas pra esse cliente. A siderúrgica é indústria, então eu ligo. |
| (o zoom continua; o mouse para em "É uma Reciclagem", sem ligar) | E É uma Reciclagem, pra quando o cliente é outro pátio. Quem diz qual dos dois vale pra cada cliente é o contador. |
| "Salvar"; toast "Cliente atualizado!"; a linha da Aços continua com o sinal verde. [BACKEND: `UPDATE customers` (inscrição 688042711117, `regime_tributario` lucro_real, `is_industry` true); vira `apos-n1`, a base do cap. 7 em diante] | Salvar. A Aços Quiririm está com a inscrição, o regime e o tipo certos. Quando chegar a hora da nota, o sistema já sabe com quem está falando. |
| O mouse para em "Novo Cliente", sem clicar. | E cliente novo é a mesma janela do fornecedor, em Novo Cliente, com esses dois botões a mais. |

### cap06 · Os avisos da consulta (vinheta: FISCAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`), aba "Fornecedores". "Novo Fornecedor"; em "Nome *" "Oficina do Tonho"; "Dados Fiscais", "Pessoa Jurídica"; CNPJ "52.917.384/0001-05"; clique na lupa. [BACKEND: `cnpj-lookup` para 52917384000105 (razão social "ANTONIO CARLOS MEIRELES OFICINA MECANICA", Rua dos Ipês, 90, Vila São Geraldo, Taubaté/SP, CEP 12062-150, Simples e ECF nulos); `publica.cnpj.ws` com `situacao_cadastral: "Baixada"` e `inscricoes_estaduais: []`] | A consulta também avisa quando tem problema. Chegou a Oficina do Tonho, querendo vender sucata com nota. Eu ponho o CNPJ e clico na lupa. |
| [ZOOM: o alerta vermelho "Atenção: a Receita informa que este CNPJ está Baixada."] | Olha o aviso vermelho: a Receita informa que esse CNPJ está baixado. A empresa foi encerrada. |
| (o zoom continua) | Nota fiscal pra CNPJ baixado costuma ser recusada pela SEFAZ. Melhor descobrir aqui do que depois de emitir. |
| Rola até "Inscrição Estadual": "A Sintegra não tem inscrição estadual ativa para este CNPJ. Se ele for isento, marque Isento de Inscrição." [ZOOM] | Embaixo, outro aviso: o estado não tem inscrição ativa pra esse CNPJ. Se a empresa for isenta, você marca Isento de Inscrição, em vez de deixar o campo vazio. |
| Volta ao "CNPJ", apaga e digita "46.280.719/0001-24" (o da serralheria): o alerta vermelho e o aviso da inscrição somem na hora; o campo mostra "Já existe um fornecedor cadastrado como “Serralheria Bem-Te-Vi” com este CPF/CNPJ.". [BACKEND: o select de duplicado por CPF/CNPJ] | E se você digitou o CNPJ errado? É só corrigir. Quando o CNPJ muda, o sistema apaga o que tinha trazido da empresa anterior, pra não misturar dado de duas empresas. O que você digitou à mão, ele mantém. E se esse CNPJ já está cadastrado, a tela avisa na hora. |
| "Cancelar" (nada é salvo). | Uma dica: se a consulta da inscrição disser que atingiu o limite, é só esperar um minuto e clicar de novo. Ela aceita três consultas por minuto. |

### cap07 · Cliente e fornecedor ao mesmo tempo (vinheta: SALDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap04`), aba "Fornecedores". Clique em "Serralheria Bem-Te-Vi": a ficha abre ao lado. | Agora, um caso comum no pátio. A serralheria vende sobra pra Recicla Vale, e também compra tubo e chapa usados aqui. Ela é fornecedora e cliente ao mesmo tempo. |
| Clique em "Editar": janela "Editar Fornecedor"; rola até a caixa "Também é cliente" ("Cria ou vincula também o cadastro de cliente.") e marca. | Pra isso, é só editar e marcar Também é cliente. |
| Clique em "Salvar"; toasts "Fornecedor atualizado!" e "Cadastro criado também como cliente."; a linha e a ficha ganham o selo roxo "Cliente+Fornecedor". [BACKEND: `UPDATE suppliers`; select em `customers` pelo `cpf_cnpj` (nenhum); `INSERT customers` com os mesmos dados; RPC `link_customer_supplier` (cria a linha `party`, zero); vira `apos-cap05`] | Salvar. A serralheria ganha o selo roxo, Cliente+Fornecedor, e passa a aparecer nas duas abas. |
| Reabre "Editar" na ficha da serralheria; rola até o rodapé e o mouse para no botão "Desvincular", sem clicar; "Cancelar". (Se o cliente já existisse com o mesmo CNPJ, a janela mostra "Vinculado ao cliente existente."; não aparece aqui.) | Se marcou por engano, o botão Desvincular, aqui no Editar, separa os dois de novo. E se o cliente já existia com o mesmo CNPJ, o sistema só liga um cadastro no outro. |
| Clique em "Depósito Irmãos Siqueira": ficha com "Fornecedor", "Cliente+Fornecedor", "-R$ 840,00" em vermelho e "a pagar" (o mesmo valor e sinal nas duas abas e na ficha, corrigido no 1.59.161). | E o saldo? Olha o Depósito Irmãos Siqueira, que já é cliente e fornecedor faz tempo. |
| [ILUSTRAÇÃO: saldo unificado: sob o nome "Depósito Irmãos Siqueira", duas colunas que entram com a frase: à esquerda "Compra de sucata · R$ 2.100,00 · a Recicla deve" (vermelho); à direita, em "E vendeu pra ele", "Venda de papelão e PET · R$ 1.260,00 · o depósito deve" (verde).] | Na semana passada, a Recicla comprou dois mil e cem reais de sucata dele, sem pagar na hora. E vendeu pra ele mil duzentos e sessenta reais de papelão e PET, também pra acertar depois. |
| [ILUSTRAÇÃO (cont.): as duas colunas se juntam na conta "2.100,00 − 1.260,00" e viram uma etiqueta só, vermelha: "Saldo único: a Recicla deve R$ 840,00".] | Em vez de dois saldos, fica um só, com a conta das duas coisas: a Recicla deve oitocentos e quarenta reais pro depósito. |
| Clique em "Clientes". [ZOOM: a linha "Depósito Irmãos Siqueira", com "Cliente+Fornecedor" e "-R$ 840,00" em vermelho] | Na aba Clientes, ele aparece do mesmo jeito: o mesmo valor, o mesmo vermelho. É um saldo só, e a Recicla deve. |

### cap08 · Tabela de preço do parceiro (vinheta: PREÇOS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap05`), aba "Fornecedores". Clique em "Depósito Irmãos Siqueira" e em "Editar": janela "Editar Fornecedor", com o aviso azul no topo. | Agora, a tabela de preço. No tutorial de materiais, a gente criou a Tabela Depósitos. Vou ligar ela ao Depósito Irmãos Siqueira. |
| Na aba "Dados de Contato", "Tabela de Preços Padrão" mostra "Principal" (com a estrela); clique: lista com "Buscar tabela..."; clique em "Tabela Depósitos". | No Editar, em Tabela de Preços Padrão, ele estava na Principal. Eu troco pra Tabela Depósitos. |
| [ZOOM: o aviso azul "Mudanças em nome, CPF/CNPJ, contato, endereço e tabela de preços padrão refletem automaticamente no cadastro de cliente vinculado."] | Como o depósito também é cliente, o aviso azul lembra: a tabela vale pro cadastro de cliente dele também. |
| Clique em "Salvar"; toast "Fornecedor atualizado!". [BACKEND: `UPDATE suppliers.default_price_table_id` e o espelho no cliente vinculado (nome, CPF/CNPJ, contato, endereço, tabela de preços padrão); vira `apos-cap06`] | Salvar. Daqui pra frente, quando você escolher o depósito numa compra, os preços já vêm da Tabela Depósitos. |
| [ILUSTRAÇÃO: qual preço vale na compra: três degraus de cima pra baixo, que acendem com a frase: 1 "Preço especial do parceiro" (em "vale primeiro"), 2 "Tabela do parceiro, ex.: Tabela Depósitos" (em "Se não tiver"), 3 "Preço do material" (em "E por último"); uma seta desce pelos degraus.] | E se tiver preço especial? Na compra, vale primeiro o preço especial do parceiro. Se não tiver, a tabela dele. E por último, o preço do material. |
| Volta para a tela; na ficha do depósito, clique em "Preços": "Preços Personalizados" ("Preços de compra e de venda para Depósito Irmãos Siqueira"), com as abas "Compra" e "Venda" e o filtro "Todos", "Já comprados", "Personalizados". | O preço especial de cada parceiro fica na ficha dele, na aba Preços. Tem um lado pra compra e outro pra venda. |
| Clique em "Já comprados": ficam ferro pesado, ferro misto e cobre misto. [BACKEND: `purchases` com `purchase_items(material_id)` do depósito, `reverted_at` nulo] | O filtro Já comprados mostra só o que esse fornecedor já trouxe. Fica fácil achar o material. |
| Na linha "Ferro pesado", em "Estado" troca "Herda" por "Fixo" e digita o preço "1,00"; "Preço final" R$ 1,00. [ZOOM: a linha] | Cada material tem um estado. Herda segue a tabela do parceiro. Fixo é um preço combinado, que não muda quando a tabela muda. Eu combino o ferro pesado do depósito a um real o quilo. |
| O mouse para em "Vinculado", na lista do "Estado", sem escolher. | E Vinculado acompanha uma tabela com uma diferença, pra cima ou pra baixo. |
| "Salvar preços"; clique em "Personalizados": ficam só os preços combinados desse parceiro. [BACKEND: `entity_custom_prices` do ferro pesado fixo a 1,00 (compra); esse preço NÃO segue para a semente `apos-cap06`: o robô limpa a linha ao capturar] | Salvar preços. Em Personalizados ficam só os combinados desse parceiro. |

### cap09 · Organizar a lista (vinheta: PARCEIROS)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), aba "Fornecedores". Clique em "Configurações": janela com "Etiquetas" ("Classifique clientes e fornecedores com uma cor fácil de reconhecer.") e "Campos personalizados". | Com a lista crescendo, vale organizar. Em Configurações ficam as etiquetas e os campos personalizados. |
| "Nova etiqueta": "Nome" "CARROCEIRO" (a tela põe em maiúsculas), escolhe uma cor, "Prévia"; "Salvar"; toast "Etiqueta criada.". | Etiqueta é uma marca colorida pra separar os parceiros. Eu crio a etiqueta Carroceiro, escolho uma cor e salvo. |
| O mouse passa por "Campos personalizados" e "Novo campo" (tipos "Texto curto", "Número", "Data", "Sim/Não", "Lista de opções"), sem criar. Fecha a janela. | Nos campos personalizados, você cria uma informação sua, como a placa do veículo, e ela entra no cadastro do parceiro. |
| "Valdir Pereira" → "Editar" → em "Etiqueta" marca "CARROCEIRO" → "Salvar"; a linha ganha a etiqueta. [BACKEND: `set_partner_labels`, tabelas de etiqueta; esta aula não segue para as próximas] | No cadastro do Valdir, em Etiqueta, eu marco Carroceiro. |
| Clique em "Filtros": "Situação do saldo" ("Todos", "Com saldo", "Saldo zerado") e "Etiquetas"; escolhe "Com saldo": ficam Cooperativa, Valdir e Depósito. [TESTAR: são três] | Nos Filtros, dá pra ver só quem está com saldo, ou só uma etiqueta. Com saldo, sobram os três fornecedores com conta aberta. |
| Limpa o filtro; clique em "Ordenar" ("Código", "Nome", "Saldo", "CPF/CNPJ", "Telefone") → "Saldo". | E no Ordenar, a lista vai por código, nome, saldo, documento ou telefone. |
| Passa o mouse no "..." da linha "Cida Ramos": "Editar", "Excluir", "Portal do Fornecedor", "Nova Movimentação"; o mouse para em "Excluir", sem clicar; Esc. | Nos três pontinhos de cada linha ficam os atalhos: editar, excluir, o portal e a movimentação. A exclusão não tem volta, então confere antes. |

### cap10 · A ficha do parceiro (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), aba "Fornecedores". Clique em "Cooperativa Recomeço": a ficha abre em "Visão geral". | Agora, a ficha. Vou abrir a Cooperativa Recomeço, que traz papelão, PET e latinha toda sexta. |
| A câmera no cabeçalho: "Cooperativa Recomeço", "Fornecedor", "R$ 2.550,00" em vermelho, "a pagar", "Editar", "Nova Movimentação" e "...". | No topo ficam o nome, o saldo e os botões de editar e de lançar uma movimentação. |
| O mouse passa pelas abas, da esquerda pra direita, sem clicar: "Visão geral", "Pedidos", "Conta-corrente", "Lucro estimado", "Financeiro", "Notas fiscais", "Preços". [TESTAR: as sete cabem sem rolagem lateral com o menu recolhido] | Embaixo, as abas: Visão geral, Pedidos, Conta-corrente, Lucro estimado, Financeiro, Notas fiscais e Preços. |
| Em "Visão geral": "Cadastro" (CPF/CNPJ, "Razão social", "Nome fantasia", "Inscrição estadual", "Contato") e "Contato e endereço". | Na Visão geral ficam os dados do cadastro, o contato e o endereço. |
| [ZOOM: "Acesso ao portal", com o link e o botão "Copiar"] | E o link do portal, pra cooperativa acompanhar o saldo de onde estiver. O portal depende do plano contratado. |
| O mouse para na aba "Lucro estimado", sem clicar. | O Lucro estimado só aparece pra quem é fornecedor, porque ele parte das compras. |

### cap11 · Os materiais que ele mais movimenta (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`), ficha da "Cooperativa Recomeço". Clique em "Pedidos": "Total Comprado" R$ 52.937,50, "Total de Pedidos" 14, "Ticket Médio" R$ 3.781,25. [BACKEND: `purchases` com itens e `materials(name)`, as 14 compras do plano] | Em Pedidos fica o resumo das compras. Desde agosto, a Recicla fez catorze pedidos com a cooperativa. |
| Rola até "Top 5 Materiais Mais Comprados" (a rosca e a legenda). | O gráfico mostra os cinco materiais que ela mais traz. E ele conta o peso, em quilos. |
| [ZOOM: a legenda "Papelão: 59%", "Plástico PET: 18%", "Alumínio latinha: 9%", "Chaparia: 8%", "Ferro misto: 6%"] | O papelão sozinho é cinquenta e nove por cento de tudo que chega da cooperativa. |
| [ILUSTRAÇÃO: peso × valor: à esquerda, uma pilha alta de fardos de papelão com "59% do peso"; em "Já a latinha", à direita, um saco pequeno de latinhas com "9% do peso"; em "o quilo da latinha vale", as etiquetas "R$ 6,20 o quilo" no saco e "R$ 0,55 o quilo" na pilha.] | Já a latinha é só nove por cento do peso. Mas o quilo da latinha vale seis e vinte, e o do papelão, cinquenta e cinco centavos. |
| Volta para a tela; o mouse para em "Período", na faixa das abas, sem abrir; rola até "Histórico de Pedidos" ("Nº Pedido", "Tipo", "Valor", "Pagamento", "Data"). | No Período, dá pra olhar um mês só. E embaixo fica cada pedido, com o valor e a data. |

### cap12 · Conta-corrente: saldo e extrato (vinheta: SALDO)

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
| Clique em "Exportar": menu "PDF resumido", "PDF detalhado (com produtos)" e "Baixar Excel (.xlsx)" (antes do 1.60.3 eram só "Abrir Relatório (PDF)" e o Excel); o mouse passa pelo resumido e pelo Excel, sem clicar. | E no Exportar, o extrato sai em PDF, resumido ou detalhado, ou em planilha, pra mandar pro parceiro. |
| Clique de novo em "Exportar" e em "PDF detalhado (com produtos)": o app abre o extrato numa aba nova (a gravação filma uma aba só) e o toast "Extrato detalhado gerado" sai. [PDF NA TELA: o robô devolve o extrato aberto na aba nova (`POPS` + captura do HTML) e a ilustração `"cena": "pdf"` o mostra, com cada pedido e a tabela "Material", "Preço unit.", "Quantidade", "Total"] [BACKEND: `purchase_items` com `materials(name, unit)` por `purchase_id`] | O PDF detalhado mostra, em cada pedido, os materiais, o peso e o preço. |

### cap13 · Ajustes na conta-corrente (vinheta: SALDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), ficha da "Cooperativa Recomeço", aba "Conta-corrente" (saldo R$ 1.350,00). Clique em "Movimentação"; o mouse passa por "Receber" ("Você recebeu do fornecedor - Aumenta o saldo dele com você") e por "Dinheiro" (apagado sem caixa aberto); "Cancelar". | Na Movimentação tem mais duas coisas. O tipo Receber, pra quando o fornecedor te devolve dinheiro. E a forma Dinheiro, que sai do caixa e só funciona com um caixa aberto. |
| Clique em "Crédito/débito": janela "Lançar crédito/débito", "Saldo hoje R$ 1.350,00". | E quando o acerto não envolve dinheiro? A cooperativa aceitou um desconto de cinquenta reais, porque o papelão de sexta veio molhado. Pra isso existe o Crédito/débito. |
| Em "Direção" clica em "Aumenta o que ele me deve" ("ou abate o que eu devo a ele"); "Valor" 50; [ZOOM: a prévia "Saldo hoje R$ 1.350,00 ... → depois R$ 1.300,00"] | Eu escolho a direção que abate o que eu devo a ele. Ponho cinquenta reais, e a tela já mostra a conta: o saldo de hoje e como fica depois. |
| "Motivo do lançamento *": "Desconto do papelão molhado de 06/11"; a nota "Não movimenta caixa nem conta bancária."; confirma; o extrato ganha a linha "Ajuste" e o "Saldo Atual" vira R$ 1.300,00. [BACKEND: RPC `apply_balance_delta`] | O motivo é obrigatório. Confirmo, e o saldo cai pra mil e trezentos. Esse lançamento mexe só no saldo: não passa pelo caixa nem pelo banco. |
| O mouse para no lápis e na lixeira da linha nova ("Editar movimentação", "Excluir movimentação"). | Lancei errado? Cada linha do extrato tem um lápis, pra corrigir, e uma lixeira, pra excluir. |
| Clique na lixeira: "Excluir Movimentação", com "Efeitos da exclusão"; "Confirmar Exclusão"; toast "Lançamento excluído e todos os efeitos revertidos"; o saldo volta a R$ 1.350,00. [BACKEND: `update_balance` com o valor invertido e `DELETE balance_movements` (sem `group_id`)] [TESTAR: a lixeira aparece na linha do ajuste e o saldo volta] | A cooperativa mudou de ideia, então eu excluo. A tela mostra o que vai ser desfeito, eu confirmo, e o saldo volta pra mil trezentos e cinquenta reais. |
| O mouse para na linha do Pix de R$ 1.200,00. | Uma dica: excluir um pagamento desfaz tudo junto, o saldo do parceiro e a saída do banco. Se ele já estiver conciliado com o extrato do banco, o sistema pede pra desfazer a conciliação antes. |
| Clique no lápis "Editar saldo" ao lado de "Saldo Atual": janela "Editar saldo (definir o valor final)" ("Tipo de saldo", "Valor", "Observação (opcional)"); "Cancelar". | E o lápis do lado do Saldo Atual é só pra correção: ele define o valor final do saldo, direto. No dia a dia, use a Movimentação e o Crédito/débito, que deixam o histórico explicado. |
| Clique em "Data" (filtro do extrato) e fecha; clique numa linha "Pedido": os itens abrem embaixo. | No filtro Data, você olha um período só. E clicando num pedido, os materiais dele abrem ali mesmo. |

### cap14 · Lucro estimado (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), ficha da "Cooperativa Recomeço". Clique em "Lucro estimado": o período mostra "Este mês"; em "Eu escolho", abre e clica em "Mês passado"; a tabela "Margem estimada por material" carrega. [BACKEND: RPC `get_supplier_profit_estimate` com as cinco linhas de outubro do plano] | Agora, o Lucro estimado: quanto cada material dessa cooperativa deixa pra Recicla Vale. Eu escolho o Mês passado, outubro inteiro. |
| [ZOOM: as linhas "Alumínio latinha" e "Papelão" da tabela, desta linha até o fim da seguinte; o mouse aponta "Preço Médio Compra" R$ 6,20, "Preço Médio Venda" R$ 7,40 e "Margem R$/kg" R$ 1,20 da latinha] | Olha a latinha: a Recicla pagou seis e vinte o quilo e vendeu, em média, a sete e quarenta. Sobra um e vinte por quilo, e essa diferença é a margem. |
| (o zoom continua; o mouse vai para "Margem Total" R$ 2.100,00 do papelão) | E o papelão, que vale pouco, dá a maior margem no total, porque vem muito: dois mil e cem reais no mês. |
| A câmera abre nos cartões "Custo total comprado" R$ 18.755,00, "Margem estimada total" R$ 5.998,00 e "Margem média %" 24,2%; o mouse para no do meio. | Somando tudo, a margem estimada da cooperativa em outubro foi de cinco mil novecentos e noventa e oito reais. |
| [ZOOM: o aviso âmbar "Estimativa — sucata é fungível; a margem é calculada sobre o preço médio de venda do material no período, não é lucro realizado."] | Uma dica: esse número é uma estimativa, não é dinheiro no bolso. O aviso da tela diz: sucata é fungível. |
| [ILUSTRAÇÃO: sucata é fungível: três origens, "Cooperativa Recomeço", "Dona Cida" e "outros", jogam latinhas num fardo só, "Alumínio latinha"; em "Na venda", o fardo sai inteiro para "Serra Fina".] | Fungível quer dizer que se mistura. A latinha da cooperativa vai pro mesmo fardo da latinha da Dona Cida e de todo mundo. Na venda, ninguém separa de quem era cada lata. |
| [ILUSTRAÇÃO (cont.): sobre o fardo, "venda média no mês: R$ 7,40 o quilo"; ao lado, "compra da cooperativa: R$ 6,20 o quilo" e o resultado "margem estimada: R$ 1,20 o quilo", com um carimbo "estimativa".] | Por isso a margem usa o preço médio de venda do material no mês. Ela não vai bater com o extrato, e tudo bem: ela mostra quanto cada material desse fornecedor rende. |

### cap15 · Financeiro e notas fiscais (vinheta: FICHA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), ficha da "Cooperativa Recomeço". Clique em "Financeiro": "Receitas vinculadas" R$ 120,00, "Despesas vinculadas" R$ 450,00 e a lista "Despesas & Receitas". [BACKEND: `cash_transactions` e `financial_bills` com `partner_type` supplier e `partner_id` da cooperativa, com `category:financial_categories(name, color)`] | Agora, o Financeiro. Aqui ficam as despesas e as receitas avulsas ligadas ao parceiro, o que não é compra nem venda. |
| [ZOOM: as duas linhas: "Despesa" "Frete das entregas de outubro" R$ 450,00 e "Receita" "Venda de sacos de ráfia usados" R$ 120,00] | Na cooperativa, o frete das entregas de outubro, quatrocentos e cinquenta reais, e uma venda de sacos de ráfia usados, cento e vinte. |
| A câmera abre na aba inteira, sem zoom. | Elas aparecem aqui quando a despesa ou a receita é lançada com o nome do parceiro. |
| Clique em "Notas fiscais": "Notas Fiscais" e "Nenhuma nota fiscal para este parceiro.". [BACKEND: `invoices` vazia para a cooperativa] | E em Notas fiscais ficam as notas desse parceiro. A cooperativa ainda não tem nenhuma. A emissão de nota depende do plano contratado e tem um tutorial só dela. |

### cap16 · Relatório de saldos (vinheta: SALDO)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`), `/clientes-fornecedores`. Clique em "Relatório": janela "Relatório de Saldos" ("Visualize todos os saldos a receber e a pagar"). [BACKEND: `balances` com `balance_movements(created_at)` do mais novo, `.neq('balance', 0)`, ordem por saldo] | Pra fechar, a pergunta do dia a dia: quem te deve, e quanto? Lá em cima, Relatório. |
| [ZOOM: o bloco "A Receber" (título, "Total: R$ 19.540,00" e as três linhas: "Fundição Bandeira do Vale" R$ 14.370,00, "Aços Quiririm Ltda" R$ 4.870,00 e "Valdir Pereira" -R$ 300,00), desta linha até o fim da terceira; o mouse aponta o total] | Em A Receber fica tudo que vai entrar: dezenove mil quinhentos e quarenta reais. A maior parte é da Fundição Bandeira do Vale, que comprou cobre em três vezes. |
| (o zoom continua; o mouse aponta "Aços Quiririm Ltda", "Cliente", "R$ 4.870,00" em verde) | A Aços Quiririm é cliente, com saldo positivo e verde: ela te deve quatro mil oitocentos e setenta reais. |
| (o zoom continua; o mouse aponta "Valdir Pereira", "Fornecedor", "-R$ 300,00" em verde) | O Valdir é fornecedor, com saldo negativo, também verde. A Recicla adiantou trezentos reais pra ele, e ele paga em sucata. |
| Rola até "A Pagar". [ZOOM: o bloco "A Pagar" (título, "Total: R$ 3.690,00" e as três linhas), desta linha até o fim da quarta; o mouse aponta o total] | Em A Pagar fica o que vai sair: três mil seiscentos e noventa reais. |
| (o zoom continua; o mouse aponta "Cooperativa Recomeço", "Fornecedor", "R$ 1.350,00" em vermelho) | A cooperativa é fornecedora, com saldo positivo e vermelho: são os mil trezentos e cinquenta reais que ficaram do acerto de hoje. |
| (o zoom continua; o mouse aponta "Depósito Irmãos Siqueira", "Cliente+Fornecedor", "-R$ 840,00" em vermelho) | O depósito aparece uma vez só, como Cliente+Fornecedor, com o saldo único. |
| (o zoom continua; o mouse aponta "Serra Fina Alumínio Reciclagem", "Cliente", "-R$ 1.500,00" em vermelho) | E a Serra Fina é cliente, com saldo negativo e vermelho. Ela adiantou mil e quinhentos reais pela próxima carga de alumínio, e agora a Recicla deve essa carga pra ela. |
| Clique em "Exportar Relatório": menu "Exportar em PDF" e "Exportar em Excel"; o mouse passa pelo Excel (sem clicar); clique em "Exportar em PDF": o relatório abre numa aba nova. [PDF NA TELA: o robô devolve o relatório da aba nova e a ilustração `"cena": "pdf"` o mostra] | No Exportar Relatório, a lista sai em PDF ou em planilha. |
| Clique no olho da linha "Aços Quiririm Ltda": a janela fecha e abre a ficha cheia ("Clientes e Fornecedores › Aços Quiririm Ltda", "Saldo: R$ 4.870,00 (Aços Quiririm Ltda te deve)"), na aba "Conta-Corrente do Cliente", com o extrato. [BACKEND: `/balance/customer/<id>` → `/saldo/...` → `/cliente/<nome>-<código>?tab=conta-corrente`] [TESTAR: a ficha cheia abre na aba da conta-corrente] | E no olho, você abre a conta-corrente do parceiro, com o extrato completo. |

### cap17 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a lista de fornecedores e a janela "Novo Fornecedor" do Rogério (trechos dos caps. 1 e 2). | Pronto! Recapitulando: a gente viu como a tela de clientes e fornecedores está organizada e cadastrou o Rogério, pessoa física. |
| Montagem rápida: a lupa do CNPJ, a caixa âmbar, o "Usar a da Sintegra" e o "Número" virando 418 (caps. 3 e 4). | Cadastrou a serralheria com a busca pelo CNPJ, que trouxe o endereço, a inscrição estadual e o regime, e completou o que faltava pra nota fiscal. |
| Montagem rápida: a Aços Quiririm em Lucro Real e o alerta vermelho de CNPJ baixado (caps. 5 e 6). | Conferiu o cadastro de um cliente do Lucro Real e viu os avisos que a consulta dá. |
| Montagem rápida: "Também é cliente", o selo "Cliente+Fornecedor", a "Tabela Depósitos" e a etiqueta na lista (caps. 7 a 9). | Marcou a serralheria como cliente e fornecedor, entendeu o saldo único, ligou a Tabela Depósitos ao depósito e organizou a lista com etiquetas e filtros. |
| Montagem rápida: as abas da ficha, o gráfico, o pagamento, o ajuste de saldo e o "Lucro estimado" (caps. 10 a 14). | Abriu a ficha da cooperativa, leu o gráfico de materiais, lançou um pagamento na conta-corrente, fez um ajuste de saldo e viu o lucro estimado. |
| Montagem rápida: o "Relatório de Saldos" (cap. 16). | E fechou com o relatório de quem te deve e a quem você deve. |
| Cartão "Próximo: Balança e impressora: o EcoTray"; cartela final. | No próximo tutorial, a balança e a impressora passam a conversar com o sistema, pelo EcoTray. Até lá! |
