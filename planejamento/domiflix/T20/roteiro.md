# Roteiro T20 · Relatório Financeiro e DRE

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`,
gerado por script a partir desta coluna. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela
(`T20/inventario.md`, conferido de novo contra o código da 1.38.6).
Aula no computador (janela de 1280×800), logada como Camila Duarte (admin) do começo ao fim, sempre em Financeiro → "Relatórios". Todo capítulo parte de um navegador novo, com o mundo do fim do capítulo anterior (sementes `seeds-extra/t20/apos-capNN.json`).
Todos os nomes, valores e datas são fictícios; a fala não cita data, mês por nome nem valor do histórico (só o da assinatura do T19, que é fixo).

- **Título final:** Relatório Financeiro e DRE
- **Vinhetas (áreas):** RELATÓRIOS · DRE · DFC · CONTABILIDADE · ANÁLISE · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Integração com Asaas, Assinaturas e Cobranças (T19, na ordem de exibição); a fala cita também o Financeiro (T13), que é a base
- **Próximo:** Notas Fiscais (T14)
- **FAKE_NOW:** `2026-11-10T10:00:00-03:00` (terça-feira), o mesmo do T13 e do T19, no backend falso e no robô. "Este mês" é novembro (ainda no começo), "Mês passado" é outubro, o mês fechado que a aula lê no DRE; as projeções usam o período de 01/11/2026 a 31/12/2026.
- **Duração estimada:** ~12 min de vídeo (1.427 palavras de fala, ~9,1 min de voz a 2,6 palavras/s, mais vinhetas, ilustrações e pausas do robô; o plano previa ~12 min)
- **Estado inicial (fim do T19):** tudo o que o T13 deixou (Conta Principal, Caixa com R$ 1.100,00, Cartão Empresarial com a fatura de novembro paga, as 28 categorias que vêm com a empresa e a Peças e componentes do T13, os 12 aluguéis a partir de 10/11/2026, a mensalidade PMOC (1/12) recebida em 10/11 com `transaction_date` 10/12/2026, o orçamento #2 em três parcelas a receber) e o que o T19 deixou: a cobrança do **Restaurante Sabor da Serra** de R$ 450,00 paga por Pix em 10/11 (receita em "Vendas de Serviços", Conta Principal) com a taxa do Asaas de R$ 1,99 em "Tarifas e Taxas", a assinatura **Academia Ponto Forte** (R$ 380,00, mensal, contínua, primeiro vencimento 10/12/2026, ainda sem cobrança gerada pelo Asaas) e a cobrança online da mensalidade PMOC (2/12), a receber.
  **Mais o histórico de três meses** (decisão 1 do plano), lançado de bastidor na Conta Principal, todo fictício (`seeds-extra/t20/inicio.json`). Nenhuma categoria nova: o histórico usa as que vêm com a empresa (`supabase/functions/self-register/index.ts:997-1027`), como "Combustível/Transporte" (no subgrupo "Despesas com pessoal", como as outras despesas padrão) e "Impostos e Taxas" (em "Impostos sobre vendas"), onde entra o Simples Nacional de cada mês, com a descrição "Simples Nacional - DAS". Receitas sempre em "Vendas de Serviços" com o cliente vinculado; custos diretos com o cliente vinculado; aluguel no dia 10; o Simples de cada mês é lançado no último dia do mês e pago no dia 20 do mês seguinte (o de outubro vence em 20/11/2026, a pagar):

  | Mês | Receitas (cliente: valor) | Custos diretos com cliente | Estrutura e impostos |
  |---|---|---|---|
  | ago/2026 (R$ 16.400,00) | Hotel Mirante do Mar 2.400,00 (03/08) e 4.200,00 (24/08); Condomínio Jardim Azul 2.300,00; Clínica Sorriso Leve 1.080,00; Padaria Bom Grão 950,00; Farmácia Vida Plena 1.650,00; Mercado Vila Nova 780,00; Escritório Lemos & Prado 720,00; Restaurante Sabor da Serra 2.320,00 (28/08) | Hotel: CSP - Materiais 1.640,00 e CSP - Mão de Obra Avulsa 600,00; Condomínio 820,00; Farmácia 540,00; Mercado 260,00 (CSP - Materiais); Restaurante: Peças e componentes 690,00 | Aluguel 2.800,00 (10/08); Combustível/Transporte 760,00; Tarifas e Taxas 38,90; Simples Nacional (Impostos e Taxas) 984,00 (lançado 31/08, pago 20/09) |
  | set/2026 (R$ 19.850,00) | Hotel 4.800,00; Academia Ponto Forte 4.600,00; Padaria 540,00; Clínica 1.260,00; Condomínio 1.850,00; Farmácia 360,00; Mercado 2.150,00; Pousada Brisa do Mar 1.590,00; Restaurante 2.700,00 | Hotel: Peças e componentes 2.650,00 e Mão de Obra Avulsa 700,00; Academia 1.380,00; Pousada 480,00; Clínica 120,00; Farmácia 60,00 (CSP - Materiais); Mercado 640,00 e Restaurante 980,00 (Peças e componentes) | Aluguel 2.800,00; Combustível/Transporte 820,00; Tarifas 42,50; Simples (Impostos e Taxas) 1.191,00 (lançado 30/09, pago 20/10) |
  | out/2026 (R$ 13.950,00) | Hotel 1.900,00 (01/10) e 4.050,00 (30/10); Padaria 950,00; Clínica 1.080,00; Mercado 690,00; Farmácia 480,00; Escritório 1.780,00; Restaurante 720,00; **Condomínio 2.300,00 lançada em 28/10 e recebida em 03/11/2026** | Hotel: CSP - Materiais 1.610,00 e Peças e componentes 720,00; Escritório 520,00; Condomínio 760,00; Mercado 210,00; Clínica 110,00; Padaria 90,00 (CSP - Materiais) | Aluguel 2.800,00; Combustível/Transporte 690,00; Tarifas 35,20; Simples (Impostos e Taxas) 837,00 (lançado 31/10, a pagar em 20/11) |

  Para o saldo de 01/11/2026 continuar R$ 18.500,00 (o saldo inicial que o T13 acertou na tela), a semente grava como saldo inicial da Conta Principal R$ 18.500,00 menos o líquido pago do histórico (o seed calcula). Com isso o ranking da Análise (setembro a novembro, Regime de Caixa) fica: por faturamento, Hotel Mirante do Mar na frente (com a mensalidade do PMOC de novembro); por margem, Padaria Bom Grão, Farmácia Vida Plena e Clínica Sorriso Leve na frente, e o hotel bem atrás (gasta mais pra entregar).
- **Criado ao vivo:** dois subgrupos novos de natureza "Despesa operacional": **Despesas administrativas**, com "Aluguel", "Luz/Energia" e "Ferramentas e Equipamentos" movidas para ele, e **Despesas com veículos**, com "Combustível/Transporte". O subgrupo que vem com a empresa, "Despesas com pessoal", fica com "Salários e Encargos", "Alimentação", "Marketing e Publicidade" e "Outros" (a decisão 2 do plano, renomear o subgrupo, não serve mais: com as categorias padrão do cadastro ele também guarda os salários). O resto da aula só lê e exporta.
- **Estado final:** como o inicial, mais a estrutura do DRE nova (Despesas administrativas com Aluguel, Luz/Energia e Ferramentas e Equipamentos; Despesas com veículos com Combustível/Transporte). Vira `seeds-extra/t20/apos-cap12.json` (igual ao `apos-cap03`); o T14 parte dele; atualizar `MUNDO_FICTICIO.md` (o histórico e a estrutura do DRE passam a valer para as próximas aulas, como o T17).
- **Sementes entre capítulos:** `inicio` (o histórico), `apos-cap03` (a estrutura do DRE); os outros capítulos só leem.
- Decisões padrão:
  ordem dos capítulos: "Organizar os grupos" vem logo depois da primeira leitura do DRE (o plano o punha no capítulo 6), para o resto da aula já mostrar o aluguel e as ferramentas em "Despesas administrativas", fora do subgrupo que vem com a empresa, que junta todas as despesas padrão com o nome "Despesas com pessoal" (handoff, inventário 0.3, item 1); no capítulo 2 a câmera não abre o subgrupo de despesa operacional;
  o mês lido no DRE é o "Mês passado" (outubro, fechado), e não "Este mês" (novembro está no começo); o exemplo de caixa × competência usa duas linhas do mundo: a instalação do Condomínio Jardim Azul (lançada em outubro, recebida em novembro) e a parcela 1/3 da compra no cartão do T13 (comprada em outubro, paga com a fatura em novembro); a comparação "Período anterior" de outubro é setembro (meses inteiros, `lib/dre-period-comparison.ts:36-44`);
  "Configurar DRE": os dois subgrupos nascem no "Novo subgrupo" e as categorias mudam de grupo pelo seletor (alternativa ao arraste, `:797-815`); o lápis do subgrupo que vem com a empresa só aparece com zoom (o nome muda, a natureza de grupo essencial fica travada, `DreGroupsManagerDialog.tsx:458-463,853`); "Outras visões" e "Ver exemplo em PDF" só com zoom (decisão 4 do plano; as tabelas `dre_layout_*` não estão no schema do fakebase);
  projeções: em Regime de Competência, período Personalizado de 01/11 a 31/12/2026, "Incluir projeções" mostra "1 ciclo(s) previsto(s) · R$ 380,00" (a assinatura do T19; o Asaas ainda não criou a cobrança, e o app só projeta o ciclo que ainda não virou cobrança, `lib/dre-subscription-projections.ts:134-195`);
  checklist de fechamento sem tela: ilustração (decisão 5 do plano); outra ilustração para as três datas da compra no cartão (capítulo 5);
  exports (Excel, PDF, CSV, pacote) são downloads e não aparecem no vídeo: só o menu e, no pacote, o aviso; nada de clique em "Excluir" ou "Desativar" de grupo, "Outras visões", "Ver exemplo em PDF" nem nos itens de exportar do DRE e do DFC;
  pronúncias a testar: DFC "dê-éfe-cê", DRE "dê érri ê", Excel "ékisel" (como no T1 e no T8), PDF e CSV como no T13.
- Marcas na coluna Tela: `[BACKEND: ...]`, `[TESTAR ...]`, `[ILUSTRAÇÃO: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Relatório Financeiro e DRE". | (sem fala) |
| Menu "Financeiro" → "Relatórios", logada como Camila Duarte: cabeçalho "Financeiro" ("Visão geral, DRE e DFC") e a aba "Visão Geral" aberta ("Visão geral dos relatórios"). [BACKEND: sementes do fim do T19 mais o histórico de agosto a outubro (`seeds-extra/t20/inicio.json`), com `dre_group_id` em todas as categorias] | Oi! Neste tutorial a gente vai ler o que o dinheiro lançado no Financeiro está dizendo: o resultado do mês, o caixa dos próximos dias e o pacote pro contador. |
| A câmera passa pelas abas "Visão Geral", "DRE - Resultado", "DFC - Fluxo de Caixa", "Contabilidade" e "Análise". | Tudo isso fica em Relatórios, no menu Financeiro, em cinco abas: Visão Geral, DRE Resultado, DFC Fluxo de Caixa, Contabilidade e Análise. Pra ficar mais claro, a Glacial já tem lançados os três meses anteriores. |
| Cartão discreto: "Antes: Integração com Asaas, Assinaturas e Cobranças". | Se você ainda não viu os tutoriais do Financeiro e da integração com o Asaas, dá uma olhada antes. [pause] Vamos começar pela visão geral. |

### cap01 · A visão geral (vinheta: RELATÓRIOS)

| Tela | Fala |
| --- | --- |
| Clique no filtro de período ("Este mês") → "Personalizado": abre o calendário de dois meses; volta até agosto e marca de 01/08/2026 a 31/10/2026; clique em "Aplicar". [TESTAR: a navegação do calendário de intervalo e o "Aplicar" (`components/ui/DateRangeFilter.tsx`, `Calendar mode="range"`)] | A visão geral fica melhor com mais de um mês, então eu escolho, no período Personalizado, os três meses que já fecharam. |
| Zoom no título "Visão geral dos relatórios" e nos botões "Regime de Caixa" (marcado) e "Regime de Competência". | Repara que essa aba abre no Regime de Caixa, que mostra o que de fato entrou e saiu da conta. Daqui a pouco a gente vê a diferença pro de competência. |
| Zoom nos cartões "Margem", "Faturamento" e "Resultado". | Os três números de cima resumem o período: o faturamento, o resultado e a margem. A margem diz quanto sobra de cada cem reais que entram. |
| A câmera desce pelo gráfico "Receita × despesa", mês a mês. | No gráfico de receita e despesa, mês a mês, dá pra ver qual mês foi mais fraco. |
| A câmera passa por "Receitas por categoria" e "Despesas por categoria". | E embaixo, de onde veio a receita e pra onde foi a despesa, por categoria. |

### cap02 · O resultado do mês (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| Clique na aba "DRE - Resultado"; no filtro de período escolhe "Mês passado". | Agora o DRE, o demonstrativo de resultado. Ele explica de onde veio o resultado do mês, linha por linha. Pra ler um mês fechado, escolho Mês passado. |
| Zoom nos cartões "Margem", "Receita Líq." e "Resultado Líq." e no gráfico "Evolução Receita × Despesas". | Em cima ficam a margem, a receita líquida e o resultado líquido, e o gráfico mostra a evolução dos últimos meses. |
| A câmera desce pela tabela "Demonstrativo de Resultado (DRE)": "(+) Receita Bruta", "(-) Impostos e Deduções", "(=) Receita Líquida", "(-) Custo dos Serviços Prestados (CSP)", "(=) Lucro Bruto", "(-) Despesas Operacionais (OPEX)" e "(=) Resultado Líquido", sem abrir os subgrupos de despesa operacional. | A tabela segue uma ordem. A receita bruta, menos os impostos, dá a receita líquida. Menos o custo dos serviços prestados, dá o lucro bruto. E, menos as despesas operacionais, o resultado líquido. |
| Clique no subgrupo "Custos diretos" de "(-) Custo dos Serviços Prestados (CSP)": abrem as categorias "CSP - Materiais", "CSP - Mão de Obra Avulsa" e "Peças e componentes". [TESTAR: as categorias padrão do grupo sem valor no mês ("Custo de Materiais" e "Fornecedores e Insumos") aparecem zeradas ou somem] | Clicando num grupo, aparecem as categorias dele. No custo dos serviços estão o material, a mão de obra avulsa e as peças e componentes, que a gente criou no tutorial do Financeiro. |
| Zoom na coluna "% da receita". | E a coluna da direita mostra o peso de cada linha sobre o faturamento. Assim você vê, por exemplo, quanto do que entrou foi gasto em material. |

### cap03 · Organizar os grupos (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| Clique em "Configurar DRE" (cabeçalho escuro da tabela): abre "Configurar DRE" ("Organize os grupos e mova categorias arrastando. Use o seletor como alternativa acessível."), com o bloco "Novo subgrupo" e a "Prévia da estrutura" por natureza ("Receita", "Dedução da receita", "Custo", "Despesa operacional"...). [BACKEND: `dre_groups` do T13 (os seis do sistema) e as categorias com `dre_group_id`; update genérico; sem as tabelas `dre_layout_*` no schema, conferir se a janela abre sem erro no bloco de outras visões (inventário, dúvida 4)] | E os grupos do DRE você organiza do seu jeito. Em Configurar DRE fica a estrutura inteira, separada pela natureza de cada grupo: receita, dedução, custo e despesa operacional. |
| Em "Despesa operacional", o subgrupo que vem com a empresa, "Despesas com pessoal", com as despesas padrão ("Salários e Encargos", "Aluguel", "Luz/Energia", "Combustível/Transporte", "Ferramentas e Equipamentos", "Alimentação", "Marketing e Publicidade" e "Outros"); zoom no lápis ("Editar Despesas com pessoal"), sem abrir. | Repara: a empresa já nasce com um subgrupo de despesa operacional, o Despesas com pessoal, e todas as despesas do dia a dia caem nele, do salário ao aluguel. Dá pra mudar o nome no lápis, mas aqui eu vou separar as despesas. |
| Em "Novo subgrupo": "Natureza" → "Despesa operacional"; digita "Despesas administrativas"; clique em "Adicionar": o grupo novo aparece com "Nenhuma categoria neste grupo. Arraste uma categoria de outro grupo para cá.". | Em Novo subgrupo, a natureza é Despesa operacional, e o nome, Despesas administrativas. Adicionar. |
| Na linha "Aluguel" (em "Despesas com pessoal"), abre o seletor "Mover Aluguel para outro grupo DRE" e escolhe "Despesas administrativas": a categoria muda de grupo; o robô faz o mesmo com "Luz/Energia" e "Ferramentas e Equipamentos" (a edição acelera o trecho). | Agora é só levar o aluguel pra lá. Dá pra arrastar, ou usar o seletor da categoria e escolher o grupo novo. A energia e as ferramentas vão do mesmo jeito. |
| Em "Novo subgrupo", "Despesa operacional" e "Despesas com veículos" → "Adicionar"; no seletor de "Combustível/Transporte" escolhe "Despesas com veículos" (a edição acelera o trecho). | E crio mais um, Despesas com veículos, pro combustível. |
| Zoom no quadro "Precisa de outra forma de ver o DRE?" e no botão "Outras visões" (sem clicar); fecha a janela. | Repara que só a apresentação muda: os lançamentos continuam iguais. E, se precisar, em Outras visões dá pra montar formas diferentes de ver o mesmo DRE. |
| A tabela do DRE com "Despesas administrativas" e "Despesas com veículos" em "(-) Despesas Operacionais (OPEX)". | De volta ao DRE, os dois subgrupos já aparecem nas despesas operacionais. |

### cap04 · Caixa ou competência (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| Zoom nos botões "Regime de Caixa" e "Regime de Competência" (marcado) do cabeçalho escuro; passa o mouse em "Regime de Competência": dica "Conta a despesa no mês em que ela aconteceu, mesmo que você ainda não tenha pago. Uma compra no cartão entra no mês da compra.". | Agora o botão que mais gera dúvida: caixa ou competência. O DRE abre no Regime de Competência, em que cada lançamento entra no mês em que aconteceu, pago ou não. |
| Abre "Despesas administrativas" (aparece "Ferramentas e Equipamentos", a parcela 1/3 da compra no cartão do T13) e zoom em "Vendas de Serviços" (com a instalação do Condomínio Jardim Azul de 28/10). | Em competência, o mês passado tem a instalação do Condomínio Jardim Azul, que foi feita no fim do mês, e a primeira parcela da bomba de vácuo, comprada no cartão. |
| Clique em "Regime de Caixa": a dica "Conta a despesa no mês em que o dinheiro saiu da conta. Uma compra no cartão entra no mês em que você pagou a fatura."; "Vendas de Serviços" diminui e "Ferramentas e Equipamentos" sai do mês; zoom no rodapé "* Regime de Caixa: cada lançamento entra no mês em que o dinheiro entrou ou saiu da conta. Só aparece o que já foi pago ou recebido.". | Agora, no Regime de Caixa. Repara que a receita diminuiu e a bomba de vácuo saiu do mês. No caixa, só entra o que já foi pago ou recebido, no mês em que o dinheiro se mexeu. |
| No filtro de período escolhe "Este mês" (o regime continua em "Regime de Caixa"): "Vendas de Serviços" com o Condomínio (recebido em 03/11) e "Ferramentas e Equipamentos" (a parcela paga com a fatura em 10/11). | E onde elas foram parar? Em Este mês. O condomínio pagou a instalação no começo deste mês, e a parcela do cartão entrou quando a fatura foi paga. |
| (a câmera fica na tabela) | As duas visões estão certas, cada uma responde uma pergunta. Competência mostra se o mês deu lucro, e caixa mostra o dinheiro que de fato passou pela conta. Uma dica: combina com o seu contador qual dos dois ele usa. |

### cap05 · A compra no cartão (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| [ILUSTRAÇÃO: uma linha do tempo com a mesma compra, a bomba de vácuo e o vacuômetro em três vezes, e três marcos: "Compra" (dia 20 do mês passado, a parcela 1/3), "Fatura" (fecha no dia 5 e vence no dia 15) e "Pagamento da fatura" (dia 10); embaixo, duas setas, "Competência" saindo da compra e "Caixa" saindo do pagamento, e a fatura com o selo "só marca o vencimento"; fundo branco, Montserrat, verde, objetos genéricos sem marca.] | Com o cartão, são três datas: o dia da compra, o fechamento da fatura e o dia em que você paga a fatura. |
| (ilustração: a seta "Competência" acende, depois a seta "Caixa") | Em competência, cada parcela entra no mês dela, a partir do mês da compra. Em caixa, ela entra no mês em que a fatura foi paga, por inteiro. |
| (ilustração: o selo da fatura) | E o mês da fatura não conta pro resultado: ele só diz quando o pagamento vence. |
| Volta ao DRE (Este mês, Regime de Caixa): zoom em "Ferramentas e Equipamentos". | Por isso a bomba de vácuo aparece aqui, no mês em que a fatura foi paga. |
| (a câmera fica no DRE) | E a transferência entre contas e o pagamento da fatura ficam fora do DRE nos dois regimes. É dinheiro mudando de lugar, e não resultado. |

### cap06 · Comparar e projetar (vinheta: DRE)

| Tela | Fala |
| --- | --- |
| No filtro de período escolhe "Mês passado"; clique em "Comparar períodos" (no alto da tabela): abre "Comparar períodos" com "Período principal" e "Comparar com"; escolhe "Período anterior" ("Mesmo número de dias, imediatamente antes"); clique em "Aplicar comparação": a tabela ganha a coluna do mês anterior e a variação de cada linha. | E dá pra olhar um mês ao lado do outro. Volto pro mês passado e clico em Comparar períodos. Escolho Período anterior e clico em Aplicar comparação. A tabela ganha a coluna do mês anterior e a variação de cada linha. |
| Zoom na coluna de variação da "(=) Receita Bruta" e do "(=) Resultado Líquido". | Assim você vê na hora o que cresceu e o que caiu de um mês pro outro. |
| Clique em "Regime de Competência"; no filtro de período, "Personalizado" de 01/11/2026 a 31/12/2026 e "Aplicar"; liga "Incluir projeções": aparece "1 ciclo(s) previsto(s) · R$ 380,00". [BACKEND: `tenant_subscriptions` com a assinatura ativa do T19 (`next_due_date` 10/12/2026) e nenhuma `tenant_charges` dela; hook `useDreSubscriptionProjections`] | E agora pra frente. Em competência, com um período que vai até o fim do mês que vem, aparece o Incluir projeções. Ligado, ele soma as próximas mensalidades das assinaturas: aqui, um ciclo de trezentos e oitenta reais, da assinatura da Academia Ponto Forte. |
| Zoom no rodapé: "Inclui R$ 380,00 de assinaturas identificadas como previstas; nenhuma transação foi criada.". | Repara no rodapé: a projeção só aparece no relatório. Nenhum lançamento é criado. |

### cap07 · O caixa dos próximos dias (vinheta: DFC)

| Tela | Fala |
| --- | --- |
| Clique na aba "DFC - Fluxo de Caixa": abre em "Previsto" (botões "Previsto" e "Realizado"), com os cartões "Saldo atual", "A receber · 15 dias", "A pagar · 15 dias", "Dívidas a receber" e "Dívidas a pagar". [BACKEND: handler da RPC `cash_flow_opening_balances {p_today}` → `[{account_id, balance}]` com o saldo de cada conta que faz parte do caixa até hoje (`supabase/migrations/20261018230000_fluxo_de_caixa_previsto_base.sql:253-270`); sem ele o "Saldo atual" sai zerado ou a tela mostra "Não foi possível carregar o fluxo de caixa previsto" (inventário, dúvida 1)] | O DRE conta o passado. Pro caixa dos próximos dias tem o DFC, o fluxo de caixa. Ele abre no Previsto, com o saldo de hoje e o que vai entrar e sair nos próximos quinze dias. |
| Em "Próximos", clique em "30 dias": a matriz dia a dia ("Saldo inicial", "Recebimentos", "Total de saídas", "Saldo final", a coluna "Dívida" e o saldo por "Conta"). | Em Próximos, dá pra ver trinta dias. A tabela vai dia a dia: o saldo que começa, o que entra, o que sai e o saldo que fica. |
| Clique no valor de saídas do dia de hoje (o aluguel do galpão): abre a lista "Movimentações" do dia, com "Total do dia"; fecha. | Clicando num valor, aparecem as contas daquele dia, como o aluguel do galpão. Assim dá pra ver o dia em que a conta aperta, antes de chegar nele. |
| Zoom na coluna "Dívida" e no texto "Previsão otimista: considera que tudo será pago e recebido no vencimento. O que já venceu e não foi baixado aparece na coluna Dívida e não é descontado do saldo.". | A previsão considera tudo pago no vencimento. E o que já venceu sem baixa aparece separado, na coluna Dívida. |

### cap08 · O que de fato entrou e saiu (vinheta: DFC)

| Tela | Fala |
| --- | --- |
| Clique em "Realizado"; no filtro de período escolhe "Mês passado": cartões "Saldo inicial", "Variação líquida" e "Saldo final" e as atividades por "Grupo DFC" (as operacionais). | No Realizado, o que de fato entrou e saiu no período: o saldo do começo, a variação e o saldo do fim. |
| A câmera desce pelas atividades operacionais. | As entradas e saídas aparecem separadas pelo grupo DFC de cada categoria. Aqui é tudo da operação: os serviços, o material, o aluguel. |
| Zoom no botão "Exportar" (abre: "Excel", "PDF" e "CSV"; fecha sem escolher). | E o Exportar leva o fluxo pra Excel, PDF ou CSV. Uma dica: lucro e dinheiro em caixa são perguntas diferentes, e um mês com lucro pode fechar com pouco caixa. |

### cap09 · O pacote do contador (vinheta: CONTABILIDADE)

| Tela | Fala |
| --- | --- |
| Clique na aba "Contabilidade" (o período continua em "Mês passado"): faixa escura "Pacote para Contabilidade" com o selo "Excel multiabas", "Reúna em um único arquivo os dados financeiros necessários para conferência e fechamento com seu contador." e "Período selecionado: ...". | No fim do mês, o contador pede tudo isso num arquivo só. É a aba Contabilidade, com o Pacote para Contabilidade, uma planilha de Excel com várias abas. |
| A câmera passa pelos quatro cartões "Lançamentos completos", "DRE e DFC reconciliados", "Saldos e obrigações" e "Plano gerencial". | Vão juntos os lançamentos completos, o DRE e o DFC, os saldos e as contas em aberto, e o plano das categorias. |
| Clique em "Exportar pacote" ("Gerando pacote..."): aviso "Pacote para Contabilidade exportado!". [TESTAR: o aviso aparece com o download bloqueado no gravador (`acceptDownloads: false`); o arquivo não aparece no vídeo] | Confiro o período lá em cima e clico em Exportar pacote. Pronto, é só mandar o arquivo pro contador. |

### cap10 · Comparar meses e clientes (vinheta: ANÁLISE)

| Tela | Fala |
| --- | --- |
| Clique na aba "Análise": "Análise" ("Compara períodos e mostra quem fatura mais e quem realmente sobra no fim."), regime "Regime de Caixa", agrupamento "Mês a mês" e "3 meses"; a tabela "Período", "Receitas", "Despesas", "Resultado" e "Variação". | A última aba é a Análise. Ela tem os próprios períodos: aqui, mês a mês, os últimos três meses, com a variação de um pro outro. |
| Rola até "Clientes": colunas "Cliente", "Faturamento", "% do total", "Custo direto", "Sobra" e "Margem", ordenado em "Maior faturamento", "Top 5"; zoom no Hotel Mirante do Mar, em primeiro. | Embaixo, os clientes. No Maior faturamento, o Hotel Mirante do Mar vem na frente. |
| Troca a ordem para "Melhor margem": a Padaria Bom Grão vai para o topo e o hotel sai do Top 5. [TESTAR: o ranking com o histórico da semente] | Agora, trocando pra Melhor margem, quem sobe é a Padaria Bom Grão. O hotel fatura muito, mas gasta mais com material e peças pra entregar. |
| (a câmera fica no ranking) | É por isso que vale ligar o cliente na receita e no custo: quem fatura mais nem sempre é quem deixa mais dinheiro. |

### cap11 · Fechar o mês (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Aba "DRE - Resultado" no "Mês passado", em "Regime de Competência"; zoom no período, no regime e no botão "Exportar" (abre: "Excel" e "PDF"; fecha sem escolher). | Pra fechar, um roteiro de fechamento do mês. No fim, o DRE sai em Excel ou PDF, do jeito que está na tela. |
| [ILUSTRAÇÃO: uma lista de conferência com cinco itens marcados um a um: contas do mês baixadas, fatura do cartão paga, extrato conferido com o banco, regime combinado com o contador e relatório exportado; fundo branco, Montserrat, verde, objetos genéricos.] | Antes de exportar, dá baixa nas contas do mês, paga a fatura do cartão e confere o extrato com o banco. |
| (ilustração) | Depois confere o período e o regime: o arquivo sai exatamente com o que está na tela. |

### cap12 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a Visão Geral dos relatórios e o DRE com a tabela aberta. | Pronto! Recapitulando: a visão geral dá o tamanho do período, e o DRE mostra de onde veio o resultado, linha por linha, com os grupos organizados do seu jeito. |
| Montagem rápida: a troca de regime e a ilustração das três datas do cartão. | Competência conta o mês em que aconteceu, caixa conta o mês em que o dinheiro se mexeu, e a compra no cartão segue essa mesma regra. |
| Montagem rápida: o DFC previsto e o Pacote para Contabilidade. | O DFC mostra o caixa dos próximos dias, e o pacote leva tudo pro contador num arquivo só. |
| Montagem rápida: o ranking da Análise. | E a Análise compara os meses e mostra quais clientes deixam mais dinheiro. |
| Cartão "Próximo: Notas Fiscais"; cartela final. | Resultado lido, falta a nota fiscal do serviço. No próximo tutorial, a gente vê as notas fiscais. Até lá! |
