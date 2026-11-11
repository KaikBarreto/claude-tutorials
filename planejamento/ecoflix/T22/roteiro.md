# Roteiro T22 · Gerencial: matriz e filiais

Roteiro pronto para a voz e a gravação (molde da Domiflix, sem etapa de aprovação). Coluna Fala = texto da narração (voz Kaik
Barreto), na grafia da legenda; a grafia de pronúncia do TTS fica em `narracao/tts_textos.py`. Coluna Tela = o que o robô faz e onde
a câmera foca, com os rótulos entre aspas como no código 1.59.154 (`T22/inventario.md`). Mundo, números e sementes: `T22/plano.md`.
Desktop 1280×800, menu lateral aberto, logado como Rafael Nogueira na matriz; o capítulo 3 é gravado como Sandra Pires, gerente da
filial (outro usuário). Cada capítulo parte de um navegador novo com a semente do fim do anterior.

- **Título:** Gerencial: matriz e filiais
- **Antes:** Relatório Financeiro e DRE (T15)
- **Próximo:** Coletas e Logística (T12)
- **Vinhetas (áreas):** GERENCIAL · GRUPO · FILIAL · DASHBOARD · DASHBOARD · FINANCEIRO · FINANCEIRO · ESTOQUE · PADRONIZAÇÃO ·
  TRANSFERÊNCIAS · ASSINATURAS · RESUMO
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos, no backend falso e no robô.
- **Duração estimada:** ~12 min de vídeo (1.410 palavras, ~9 min de voz a 2,6 palavras/s, mais 12 vinhetas, as ilustrações e as
  esperas). Alvo da fonte: 16 min (a fala fecha abaixo, como na Domiflix).
- 🔒 Módulo Gerencial: dito no cap. 0 (depende do plano, contratado na matriz). Valores de plano só na tela, sem fala nem zoom.
- Marcas na Tela: `[BACKEND: ...]`, `[ZOOM: ...]` (dura a frase inteira), `[ILUSTRAÇÃO: ...]`, `[TESTAR: ...]`.
- Pronúncias (TTS): DRE "dê-érri-ê" (do perfil); nova: CMV "cê-ême-vê" (testar no nó de pronúncia). Pix, CNPJ, Taubaté e
  Pindamonhangaba na escrita normal (conferir Pindamonhangaba no teste).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta EcoFlix com o título "Gerencial: matriz e filiais". | (sem fala) |
| Dashboard do EcoSistema da matriz, logado como Rafael Nogueira; o cursor abre, no menu lateral, o grupo "Gerencial (Filiais)": "Dashboard", "Financeiro", "Estoque", "Assinaturas" e "Configurações". [BACKEND: semente `seeds-extra/t22/inicio.json`, sem grupo (plano.md, "Mundo")] | Oi! Neste tutorial a gente vai fazer a matriz da Recicla Vale Metais, em Taubaté, enxergar a filial de Pindamonhangaba sem precisar entrar no sistema dela. |
| [ILUSTRAÇÃO: somar na mão: dois pátios, cada um com o seu computador e o seu caderno de números; na palavra "mão", alguém copia os números dos dois num papel e soma na calculadora; na palavra "só", os dois pátios mandam setas para uma tela única, a da matriz] | Com duas unidades, pra saber quanto o grupo vendeu no mês, alguém precisava abrir os dois sistemas e somar na mão. Aqui, os números das duas chegam juntos numa tela só. |
| De volta à tela; cartão discreto "Módulo Gerencial". | Isso é o Gerencial. Ele depende do plano contratado, e quem contrata é a matriz. |
| Cartão discreto "Antes: Relatório Financeiro e DRE". | Como ele junta a DRE das unidades, se você ainda não viu o tutorial Relatório Financeiro e DRE, dá uma olhada antes. [pause] Vamos entender como ele funciona. |

### cap01 · Como o Gerencial funciona (vinheta: GERENCIAL)

| Tela | Fala |
| --- | --- |
| Clique em "Dashboard", no grupo "Gerencial (Filiais)": "Módulo Gerencial" · "Crie um grupo gerencial para conectar suas unidades e ter uma visão consolidada de financeiro, DRE e estoque." e o botão "Configurar Grupo". | Sem grupo, o Gerencial começa assim, pedindo pra criar um. |
| [ILUSTRAÇÃO: matriz × filial, tempo 1: dois prédios lado a lado, "Matriz · Taubaté" e "Filial · Pindamonhangaba", cada um com o seu login e a sua assinatura; na palavra "junta", um contorno abraça os dois com o nome "Grupo Recicla Vale"; na palavra "dona", uma coroa pousa na matriz] | O grupo junta as unidades. Cada unidade é uma empresa própria no sistema, com login e assinatura próprios. A matriz é a dona do grupo, e a filial entra nele. |
| [ILUSTRAÇÃO: matriz × filial, tempo 2: da filial sobem setas com "vendas", "compras" e "estoque" até um painel somado na matriz; na palavra "padrão", desce da matriz para a filial uma caixa "catálogo de materiais"; na palavra "transfere", uma seta de ida e volta com um fardo de latinha liga os dois pátios] | A matriz enxerga os números de todas, manda o mesmo padrão de cadastro pras filiais e transfere material entre elas. |
| [ILUSTRAÇÃO: matriz × filial, tempo 3: na filial acendem três ícones, o caixa, a balança e uma nota fiscal, com a etiqueta "da filial"; na palavra "opera", um cadeado aparece entre a matriz e esses três] | Uma dica: o Gerencial junta e padroniza, mas quem opera a filial é a filial. O caixa, as compras e as notas dela continuam com quem trabalha lá. |

### cap02 · Criar o grupo e o código (vinheta: GRUPO)

| Tela | Fala |
| --- | --- |
| Clique em "Configurar Grupo": "Configurações do Grupo" · "Crie um grupo para gerenciar múltiplas unidades"; cartão "Criar Grupo Gerencial" · "Crie um grupo e compartilhe o código de convite com as filiais". | Começando pela matriz. Clico em Configurar Grupo pra criar o grupo. |
| Em "Nome do Grupo" ("Ex: Grupo Reciclagem Silva"), digita "Grupo Recicla Vale"; clique em "Criar Grupo": aviso "Grupo gerencial criado com sucesso!". [BACKEND: RPC `generate_group_invite_code` devolve `GRP-7C4E9A`; `INSERT company_groups` com validade em 10/12/2026; vira `apos-cap02`] | Dou o nome, Grupo Recicla Vale, e clico em Criar Grupo. |
| A tela vira "Configurações do Grupo" · "Gerencie as unidades e padronizações do grupo Grupo Recicla Vale", com o botão "Como funciona", as abas "Unidades", "Catálogo de Materiais", "Tabelas de Preço", "Clientes e Fornecedores", "Categorias Financeiras" e "Transferências" e o passo a passo "Configure o grupo" ("0 de 5 etapas concluídas"). | Pronto. Aqui ficam as abas do grupo e um passo a passo do que falta configurar. |
| Zoom no cartão "Código de Convite": "GRP-7C4E9A" e "Válido até 10/12/2026". [ZOOM: o código e a validade, a frase toda] | E esse é o código de convite. É ele que liga a filial ao grupo, e vale por trinta dias. Se vencer, o botão do lado gera outro. |
| Clique no botão de copiar: aviso "Código copiado!". [TESTAR: permissão `clipboard-write` no navegador do robô] | Copio o código e mando pra quem cuida da filial, por mensagem. |
| Zoom em "Unidades Ativas": "Recicla Vale Metais" com o selo "MATRIZ" e "Nenhuma filial vinculada ainda. Compartilhe o código de convite acima.". | Por enquanto, a lista de unidades tem só a matriz. |

### cap03 · Do lado da filial (vinheta: FILIAL)

| Tela | Fala |
| --- | --- |
| Capítulo gravado como Sandra Pires, no sistema da "Filial Pindamonhangaba". Rodapé do menu → "Configurações" → aba "Empresa". [BACKEND: semente `apos-cap02`; `user` = Sandra Pires (filial)] | Agora do lado da filial. A Sandra, gerente em Pindamonhangaba, entra no sistema da filial, em Configurações, na aba Empresa. |
| Desce até o cartão "Filial" · "Se esta empresa é uma filial, vincule-a à empresa-mãe usando o código de convite"; liga "É Filial" ("Ative para vincular esta empresa a um grupo gerencial"): aparece "Código de Convite" · "Solicite o código ao administrador da empresa-mãe". | Lá embaixo fica o cartão Filial. Ela liga o É Filial. |
| Cola "GRP-7C4E9A" no campo "GRP-XXXXXX". [ZOOM: o campo com o código] | E cola o código que recebeu da matriz. |
| Clique em "Vincular": aviso "Empresa vinculada ao grupo com sucesso!"; o cartão mostra "Vinculada ao grupo" · "Grupo Recicla Vale" e o selo "Ativa". [BACKEND: RPC `join_group_by_invite_code`; vira `apos-cap03`] | Vincular. Pronto, a filial está no Grupo Recicla Vale. |
| [ILUSTRAÇÃO: o código liga as unidades: o código "GRP" sai da matriz, viaja até a filial e encaixa como uma peça no contorno do grupo; na palavra "próprio", a tela da filial segue aberta ao lado, com o caixa e a balança dela] | Do lado dela, o dia a dia segue igual: a filial continua usando o próprio sistema, e a matriz passa a enxergar os números. |

### cap04 · O Dashboard Gerencial (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| De volta à matriz: "Gerencial (Filiais)" → "Dashboard": "Dashboard Gerencial", o selo "MATRIZ" com "Recicla Vale Metais" e "Grupo Recicla Vale • 2 unidades". [BACKEND: semente `apos-cap03`; RPCs `get_group_financial_summary` e `get_group_stock_summary` com os números de outubro (plano.md)] | De volta à matriz. Com a filial no grupo, o Dashboard Gerencial já mostra as duas unidades. |
| No período, escolhe "Mês passado"; o seletor de unidades fica em "Todas as Unidades". | Vou olhar outubro inteiro: em cima, Mês passado. E aqui dá pra ver todas as unidades juntas, ou uma de cada vez. |
| Zoom nos cartões "Receita Total" R$ 344.040,00 e "Despesa Total" R$ 370.690,00, com a setinha de variação. [ZOOM: os dois cartões, a frase toda] (sem zoom no "Lucro Líquido", plano.md, risco 1) | Os cartões somam o grupo. Em outubro, a receita foi de trezentos e quarenta e quatro mil e quarenta reais, e a despesa, de trezentos e setenta mil, seiscentos e noventa. |
| A câmera fica nas setinhas dos cartões; depois passa ao cartão "Estoque Total". | A setinha compara com o mês anterior. E o Estoque Total soma o estoque das duas unidades. |
| Desce até "Receita vs Despesa por Unidade": as barras de "Recicla Vale Me… ★" e de "Filial Pindamon…". | No gráfico, cada unidade aparece com a receita e a despesa lado a lado. A estrela marca a matriz. |

### cap05 · Ranking e resumo por unidade (vinheta: DASHBOARD)

| Tela | Fala |
| --- | --- |
| "Ranking por Lucro": a barra da filial em cima e a da matriz embaixo, negativa. | E o ranking ordena as unidades pelo lucro. Em outubro, a filial ficou na frente, e a matriz, no vermelho. |
| Desce até "Resumo por Unidade": "Unidade", "Receita", "Despesa", "Lucro" e "Margem". | Embaixo vem o resumo por unidade, em números. |
| Zoom na linha "Recicla Vale Metais" (MATRIZ): R$ 272.040,00, R$ 299.690,00, -R$ 27.650,00 e -10.2%. [ZOOM: a linha da matriz] | A matriz teve duzentos e setenta e dois mil e quarenta de receita e duzentos e noventa e nove mil, seiscentos e noventa de despesa. Ficou negativa em vinte e sete mil, seiscentos e cinquenta reais. |
| Zoom na linha "Filial Pindamonhangaba": R$ 72.000,00, R$ 71.000,00, R$ 1.000,00 e 1.4%. [ZOOM: a linha da filial] | A filial vendeu setenta e dois mil, gastou setenta e um mil e lucrou mil reais. |
| [ILUSTRAÇÃO: a compra que ainda está no pátio: um caminhão com a compra de outubro descarrega no pátio; parte do material sai vendida num caminhão do cliente e uma pilha fica no pátio com a etiqueta "ainda não vendido"; na palavra "inteira", a pilha inteira também cai na coluna da despesa] | Repara no vermelho da matriz. É que aqui entra a compra inteira do mês, até o material que ainda está no pátio esperando venda. Isso fica claro na DRE, com o regime de competência. |

### cap06 · A DRE do grupo (vinheta: FINANCEIRO)

| Tela | Fala |
| --- | --- |
| "Gerencial (Filiais)" → "Financeiro": "Financeiro Gerencial" · "Relatório financeiro consolidado de todas as unidades"; período "Mês passado"; aba "DRE"; em cima, "Consolidado". [BACKEND: semente `apos-cap03`; RPCs `get_group_financial_dre_summary` e `get_dre_expenses_by_group` com os números de outubro] | Agora o Financeiro. Na aba DRE, com outubro escolhido, fica a DRE do grupo inteiro. |
| No seletor do topo da DRE, clique em "Regime de Caixa": "DRE — Todas as Unidades" com "Vendas de Material" R$ 341.240,00, "Compras de Material" -R$ 318.860,00, os "Custos adicionais" (o frete, -R$ 2.400,00) e "(=) Resultado de Caixa" R$ 19.980,00. [ZOOM: as linhas de vendas, compras e resultado de caixa] | Começo pelo regime de caixa, o dinheiro que entrou e saiu. O grupo vendeu trezentos e quarenta e um mil, duzentos e quarenta, e comprou trezentos e dezoito mil, oitocentos e sessenta em material. |
| Zoom em "(-) Impostos e Deduções" -R$ 3.574,10, "Total Despesas" -R$ 45.855,90, "(+) Outras Receitas" R$ 2.800,00 e "(=) Resultado do Período" -R$ 26.650,00 ("Déficit"). [ZOOM: as quatro linhas] | Tirando os impostos e as despesas da operação, e somando o aluguel de caçamba, o mês fecha no vermelho: menos vinte e seis mil, seiscentos e cinquenta reais. |
| Clique em "Comparativo": "DRE Comparativo por Unidade", com a coluna "Recicla Vale…" (MATRIZ) e a coluna "Filial Pinda…"; linhas "Vendas", "(-) Compras (CMV)", "Receita Líquida", "(-) Despesas Operacionais (OPEX)" e "Resultado". | E no Comparativo fica a mesma DRE, unidade por unidade. |
| Zoom na linha "Resultado": -R$ 27.650,00 e R$ 1.000,00. [ZOOM: a linha "Resultado"] | O vermelho do grupo vem da matriz, menos vinte e sete mil, seiscentos e cinquenta, contra mil positivos da filial. Assim você vê de onde vem o resultado. |

### cap07 · Caixa e competência (vinheta: FINANCEIRO)

| Tela | Fala |
| --- | --- |
| Financeiro › "DRE" › "Consolidado", "Mês passado", já em "Regime de Competência" (o padrão): "(-) Custo Operacional (CMV)" com "CMV (Custo da Mercadoria Vendida)" -R$ 273.860,00 e "(=) Lucro Bruto" R$ 64.980,00 ("Margem Bruta: 19.0%"). [ZOOM: o CMV e o Lucro Bruto] [BACKEND: semente `apos-cap03`] | Agora o mesmo outubro em regime de competência. No lugar das compras entra o CMV, o custo só do material que foi vendido: duzentos e setenta e três mil, oitocentos e sessenta. |
| Zoom em "(=) Resultado do Período" R$ 18.350,00. [ZOOM: o resultado] | E o resultado do mês vira positivo: dezoito mil, trezentos e cinquenta reais. |
| [ILUSTRAÇÃO: caixa × competência: à esquerda, "Caixa": o caminhão de compras de 319 mil sai inteiro da conta do mês; à direita, "Competência": só os 274 mil do material vendido saem; na palavra "pátio", a pilha de 45 mil fica no pátio com a etiqueta "ainda não vendido"; na última frase, os dois resultados aparecem embaixo, menos 26,6 mil e 18,3 mil] | A diferença, quarenta e cinco mil, é o material que a gente comprou em outubro e ainda está no pátio. No caixa, ele já pesa no mês. Na competência, ele só vira custo quando for vendido. |
| Clique em "Regime de Caixa" e, de novo, em "Regime de Competência"; a câmera acompanha o resultado mudando de -R$ 26.650,00 para R$ 18.350,00. | O caixa mostra o dinheiro do mês. A competência mostra o lucro do que foi vendido. Os dois estão certos: cada um responde uma pergunta. |
| [ILUSTRAÇÃO: o material sem custo: um fardo entra no pátio sem etiqueta de preço; na palavra "maior", a barra do CMV encolhe e a do lucro cresce com um ponto de interrogação; na palavra "Confira", uma lupa passa pelas entradas do mês] | Uma dica: se aparecer aqui o aviso de material em estoque sem custo de compra, o lucro em competência pode estar maior do que é. Confira as entradas do período antes de decidir em cima do número. |

### cap08 · O estoque do grupo (vinheta: ESTOQUE)

| Tela | Fala |
| --- | --- |
| "Gerencial (Filiais)" → "Estoque": "Estoque Gerencial" · "Visão consolidada do estoque de todas as unidades do grupo"; aba "Visão Geral": "Valor Total em Estoque", "Unidades" (2) e "Materiais Distintos", e o cartão de cada unidade. [BACKEND: semente `apos-cap03`; RPC `get_group_inventory_report_data`] | Agora o estoque. No Estoque Gerencial, a Visão Geral junta o estoque das duas unidades. |
| A câmera desce para "Tabela Unificada de Materiais": "Material", "Recicla Vale Metais" (MATRIZ), "Filial Pindamonhangaba" e "Total"; zoom na linha "Alumínio latinha": 640 kg, 1.850 kg e 2.490 kg (a matriz com o estoque de 10/11 do mundo base, junção). [ZOOM: a linha do alumínio latinha] [TESTAR: formato da quantidade na célula] | Na tabela, cada material numa linha e cada unidade numa coluna. O alumínio latinha: seiscentos e quarenta quilos na matriz e mil oitocentos e cinquenta na filial. No total, dois mil quatrocentos e noventa. |
| Clique na aba "Posição de Estoque": "Data e hora (padrão: fim do dia)", com "Saldo", "Custo médio", "Valor em estoque" e "Projeção venda". | Na Posição de Estoque, você vê o saldo de cada material numa data, com o custo médio e o valor. |
| Clique em "Histórico de Materiais": as movimentações do mês, com "Tipo" ("Compra", "Venda") e a coluna "Filial". | No Histórico de Materiais, cada entrada e cada saída, com a unidade de onde veio. |
| Clique em "Relatório de Estoque": "Qtd. Comprada", "Valor Comprado", "Qtd. Vendida", "Valor Vendido", "Lucro" e "Margem". | E no Relatório de Estoque, quanto o grupo comprou e vendeu de cada material, com o lucro e a margem. |

### cap09 · Enviar Ativos (vinheta: PADRONIZAÇÃO)

| Tela | Fala |
| --- | --- |
| "Gerencial (Filiais)" → "Configurações" → aba "Catálogo de Materiais": "Catálogo de Materiais do Grupo" · "Cadastre os materiais que serão compartilhados com todas as filiais. ..." e "Nenhum material no catálogo. Importe do estoque ou adicione manualmente.". [BACKEND: semente `apos-cap03`] | Agora a padronização. A matriz monta o padrão do grupo, e a filial recebe. Começa pelo catálogo de materiais. |
| Clique em "Importar do Estoque da Matriz": aviso "n material(is) importado(s) do estoque"; a lista enche com os materiais da matriz (unidade, NCM e vínculos). [BACKEND: RPC `import_owner_materials_to_group`] | Com um clique, o Importar do Estoque da Matriz traz os materiais que a matriz já usa. |
| Aba "Tabelas de Preço": "Tabelas de Preço do Grupo", com as tabelas da matriz, que entram sozinhas ao abrir a aba. [BACKEND: RPC `import_owner_price_table_to_group`] | As tabelas de preço da matriz entram sozinhas, assim que você abre a aba. |
| Aba "Clientes e Fornecedores": "Clientes e Fornecedores da Matriz" · "Marque os clientes e fornecedores que ficarão disponíveis para as filiais importarem. A marcação é imediata."; marca "Fundição Bandeira do Vale": aviso "Disponibilizado para filiais". [BACKEND: RPC `toggle_group_shared_entity`] | Em Clientes e Fornecedores, você marca quem também faz negócio com a filial. A Fundição Bandeira do Vale compra das duas unidades, então eu marco. |
| Aba "Categorias Financeiras": "Categorias Financeiras da Matriz", já compartilhadas ao abrir. [BACKEND: RPC `import_company_categories_to_group`] | E as categorias financeiras também vêm prontas da matriz. |
| Aba "Unidades": na linha da "Filial Pindamonhangaba", clique em "Enviar Ativos": "Enviar Ativos para Filial Pindamonhangaba" · "Selecione quais categorias enviar. Itens já existentes na filial serão ignorados.", com "Materiais", "Categorias Financeiras", "Tabelas de Preço", "Clientes" e "Fornecedores" e o "n disponível(is)" de cada um; "Sobrescrever preços existentes" desligado. | Com tudo pronto, na aba Unidades, o Enviar Ativos manda o padrão pra filial. O que ela já tinha fica como está, e o que faltava entra. Os preços dela só mudam se você ligar o Sobrescrever preços existentes. |
| Clique em "Confirmar Envio": cada linha mostra "n novo(s)"; aviso "n ativo(s) enviado(s) para Filial Pindamonhangaba"; clique em "Fechar". [BACKEND: RPC `push_group_assets_to_company` (liga os materiais de mesmo nome da filial ao catálogo do grupo e cria o que faltava); vira `apos-cap09`] | Confirmar Envio. Agora as duas unidades falam a mesma língua: o mesmo material, com o mesmo nome. |
| Zoom na lixeira da linha da filial, sem clicar. (Remover só marca o vínculo como removido, `useCompanyGroup.ts:137-150`; a volta com o mesmo código vem da fonte: a RPC `join_group_by_invite_code` fica no banco, fora do código lido, ver plano.md, riscos.) | Uma dica: se tirar uma filial do grupo por engano, nenhum dado dela se perde. Pra voltar, é só a filial colar o código de novo. |

### cap10 · Transferência com aprovação (vinheta: TRANSFERÊNCIAS)

| Tela | Fala |
| --- | --- |
| Configurações › aba "Transferências": liga "Exigir aprovação em transferências" ("Quando ativo, o destino precisa confirmar antes da transferência ser executada"). [BACKEND: semente `apos-cap09`; `UPDATE company_groups.require_transfer_approval`] | Agora as transferências. A filial juntou alumínio latinha, e a matriz vai vender um lote grande. Primeiro, eu ligo o Exigir aprovação em transferências. |
| Em "Transferências Inter-Unidades", clique em "Nova": "Nova transferência em lote"; em "Origem", "Filial Pindamonhangaba"; em "Destino", "Recicla Vale Metais". | Assim, nenhum estoque se move sem confirmação. Em Nova, a origem é a filial e o destino, a matriz. |
| Em "Materiais", busca "Alumínio latinha" e marca; em "Quantidade", 1200 (1.200 kg). [ZOOM: a quantidade] | O material é o alumínio latinha: mil e duzentos quilos. |
| Em "Observações (opcional)", "Lote para a Serra Fina Alumínio Reciclagem"; o "Resumo" com o aviso "Este grupo exige aprovação: o estoque não se move agora. ..."; clique em "Solicitar 1 transferência": aviso "Solicitação criada — aguardando aprovação". [BACKEND: RPC `create_group_transfer_and_execute` devolve `pending`] | Repara no aviso do resumo: com a aprovação ligada, o estoque ainda não se move. Clico em Solicitar uma transferência. |
| Na lista: "Filial Pindamonhangaba → Recicla Vale Metais", selo "Pendente", "Alumínio latinha — 1200 kg"; clique em "Executar": "Confirmar execução?" · "Este grupo exige aprovação antes de executar transferências. Confirme que o destino está ciente e de acordo com esta movimentação de estoque.". | A transferência fica pendente. Quando o caminhão chega na matriz e o material é conferido, aí sim, Executar. A tela pede pra confirmar que o destino está de acordo. |
| Clique em "Confirmar e Executar": aviso "Transferência executada com sucesso"; o selo vira "Concluída". [BACKEND: RPC `execute_group_stock_transfer` (matriz 1.840 kg, filial 650 kg); vira `apos-cap10`] | Confirmar e Executar. Pronto: a matriz fica com mil oitocentos e quarenta quilos, e a filial com seiscentos e cinquenta. O total do grupo continua o mesmo. |
| [ILUSTRAÇÃO: um material do grupo, dois da unidade: o cartão "Alumínio latinha do grupo" ligado a dois materiais da filial, "Alumínio latinha" e "Latinha prensada"; o total soma os dois; na palavra "só", a seta da transferência sai de um deles apenas] | Uma dica: um material do grupo pode juntar mais de um material de uma unidade. O total do grupo soma todos, e a transferência tira de um só. Se o número do grupo parecer estranho, confira material por material. |

### cap11 · Assinaturas numa fatura só (vinheta: ASSINATURAS)

| Tela | Fala |
| --- | --- |
| "Gerencial (Filiais)" → "Assinaturas": "Assinaturas do grupo" · "Acompanhe as assinaturas de todas as unidades e pague tudo de uma vez numa única fatura na matriz"; em "Unidades", "Recicla Vale Metais" ("Matriz", "Ativa") e "Filial Pindamonhangaba" ("Filial", "Ativa"), cada uma com o plano, "Mensal" e o vencimento (sem zoom nos valores). [BACKEND: semente `apos-cap10`; RPC `get_group_subscription_summary`] | Por último, as assinaturas. Cada unidade tem a sua, e aqui a matriz vê todas: o plano, se está ativa e quando vence. |
| Zoom no botão "Pagar tudo de uma vez". | E dá pra pagar tudo de uma vez, numa fatura só, na matriz. |
| Clique em "Pagar tudo de uma vez": "Pagamento do grupo · 2 unidades", "Unidades cobradas juntas"; zoom em "Ao pagar, as cobranças individuais das unidades são canceladas e substituídas por esta fatura única na matriz.". [ZOOM: o aviso, nesta frase e na seguinte] | Repara no aviso: ao pagar, a cobrança de cada unidade é cancelada e vira uma fatura única, na matriz. |
| (o zoom continua no aviso) | Uma dica importante: se a filial tinha um boleto ou um Pix da assinatura dela em aberto, ela não deve mais pagar aquele documento. Quem paga agora é a matriz, nessa fatura. |
| Em "Forma de pagamento", clique em "PIX": "Gerando QR Code PIX..." e o QR Code fictício. [BACKEND: edge `create-group-payment` simulada devolve um Pix fictício; nada vai para o Asaas] | Escolho o Pix, e a cobrança única aparece. |
| Passo de bastidor confirma o pagamento: "Pagamento Confirmado!" · "As cobranças das unidades agora são feitas nesta fatura única na matriz." · "Voltando para as assinaturas do grupo...". [BACKEND: confirmação simulada (o checkout vê o pagamento como pago); vira `apos-cap11`] | Pagou, e pronto: as cobranças das unidades passam a vir nessa fatura da matriz. |

### cap12 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: "Criar Grupo", o "Código de Convite" e o cartão "Filial" com "Vinculada ao grupo". | Pronto! Recapitulando: a gente criou o grupo na matriz, gerou o código de convite e vinculou a filial de Pindamonhangaba. |
| Montagem rápida: o "Dashboard Gerencial" e o "Resumo por Unidade". | Leu o Dashboard Gerencial, com o ranking e o resumo de cada unidade. |
| Montagem rápida: a DRE em "Regime de Caixa" e em "Regime de Competência", e o "Comparativo". | Viu a DRE do grupo nos dois regimes e comparou unidade por unidade. |
| Montagem rápida: a "Tabela Unificada de Materiais" e o "Enviar Ativos". | Conferiu o estoque do grupo e mandou o mesmo catálogo pra filial. |
| Montagem rápida: a transferência "Concluída" e o "Pagamento Confirmado!". | Transferiu o alumínio com aprovação e pagou as assinaturas numa fatura só. |
| Cartão "Próximo: Coletas e Logística"; cartela final. | No próximo tutorial, o caminhão sai do pátio pra buscar material. Até lá! |
