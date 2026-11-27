# Capas EcoFlix · lote 2 · inventário para o agente das capas

Conferido em 27/11/2026, 00h, nestas fontes:
- os roteiros `planejamento/ecoflix/Tnn/roteiro.md` (repositório [claude-tutorials](https://github.com/KaikBarreto/claude-tutorials));
- o registro `planejamento/ecoflix/PRODUCAO.md`;
- a fonte oficial da trilha, `docs/ecoflix/trilha-de-tutoriais.md`, no repositório do EcoSistema (última mudança em 19/11, commit `1ea03480f`).

O app está hoje na versão 1.60.39. Os roteiros foram conferidos nas versões 1.60.18 e 1.60.22.

## Contagem
- **Trilha atual: 26 aulas.** Vão de T00 a T22 e incluem T25, T26 e T27. T23 e T24 saíram da trilha.
- **Já têm capa (1º lote): 14 aulas.** T00, T01, T02, T03, T04 e de T06 a T14.
- **Ainda precisam de capa: 12 aulas.** T05, T15, T16, T17, T18, T19, T20, T21, T22, T25, T26 e T27. São 24 artes: 12 horizontais e 12 pôsteres.
- **Não levam capa:**
  - T23 (Marketplace): fica fora da trilha e vira trilha própria no futuro.
  - T24 (Assinatura): o assunto passou para a T00.
  - T00 vertical: é o vídeo de celular da própria T00, guardado no mesmo episódio (campo `mobile_video_id`). Não é uma aula à parte.

## Regras para as capas

### Direção do Kaik (vale acima de qualquer outra fonte)
- Capa cinematográfica realista e densa, como paródia reconhecível de um filme ou série famosa.
- Na imagem vai só o título da aula, grande e fácil de ler. Nada de código Txx, subtítulo, frase de efeito, créditos ou selos.
- Cada aula tem duas versões:
  - horizontal 16:9, em 1536×864;
  - pôster vertical 2:3, em 1024×1536.
- Essas proporções são das capas. Não confundir com o vídeo vertical 9:16.
- Uma capa por aula. Capítulo não ganha capa própria.

### Da fonte oficial, quando não contrariar o 1º lote
- Paleta: preto profundo #141414, verde EcoSistema #16A34A e sombras em azul-aço. Laranja de faísca de solda só como detalhe.
- Ambiente: ferro-velho e reciclagem no Brasil. Pátio de sucata, fardos de alumínio e papelão, prensa, balança rodoviária, caminhão caçamba, galpão de zinco, cobre, ferro, latinha. Nada de escritório genérico.
- Sem rosto reconhecível de pessoa real e sem logo de marca real.
- Nunca copiar o pôster oficial do filme. A ideia é usar a linguagem visual dele aplicada ao ferro-velho.

### Do conteúdo
- A capa não pode sugerir função que o sistema não tem. Os casos conhecidos estão na coluna "Evitar" da tabela.
- Nada de dado real, preço de plano, CNPJ, senha, token ou documento legível.
- Nas capas de nota fiscal, a DANFE não pode ter texto legível. O modelo novo de DANFE só vale a partir de 01/12/2026 e não deve aparecer como se fosse o atual.
- O Cato tem identidade visual própria no app: os arquivos `cato*` em `src/assets/` do EcoSistema (ícone, logo e fundos). Não inventar outro mascote. Fica a confirmar com o Kaik se a capa usa essa identidade.

## As 12 aulas que faltam, na ordem da trilha

O nome previsto de cada arquivo é `EcoFlix Tnn - <título>.mp4`, com `.srt` e `.vtt` de mesmo nome. Nos nomes de arquivo, os dois-pontos do título viram " - ".

| Ordem | Aula | Título na capa | O que a aula ensina | O que pode aparecer na capa | Trilha | Situação em 27/11 | Roteiro · legenda · vídeo | Aula antiga que substitui |
|---|---|---|---|---|---|---|---|---|
| 6ª de 26 | T05 | Balança e impressora: o EcoTray | Instala o EcoTray, o programa que liga o computador do escritório à balança e à impressora térmica do pátio. Com ele, o peso entra sozinho no pedido e o cupom sai na hora, sem abrir PDF. A aula também mostra o que fazer quando o EcoTray cai, como atualizar e como pedir ajuda. | Indicador de peso da balança ligado por cabo ao computador. Ícone do EcoTray na bandeja do Windows. Impressora térmica soltando o cupom (papel de 58 ou 80 mm). O visor marcando 312 kg e o sistema mostrando 321 (o erro de digitação que a aula resolve). A conexão caindo e voltando.<br>**Tema na fonte:** *Titanic*, a sala de máquinas que liga o computador ao pátio.<br>**Evitar:** dizer que a balança funciona em qualquer plano. A parte da balança depende do plano; a impressora funciona em qualquer um. | Formação básica (a parte da balança é do módulo de integração com balança) | **Em montagem.** Voz pronta; montagem final rodando agora. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T05/roteiro.md) · vídeo e legendas saem hoje como `EcoFlix T05 - Balança e impressora - o EcoTray` | Não definido. Candidata: "Integrações: Balanças e Impressoras" (a confirmar) |
| 14ª | T15 | Relatório Financeiro e DRE | Responde à pergunta do fim do mês: ganhei ou perdi dinheiro, e por quê? Organiza o plano de contas e os centros de custo, lê o Relatório Financeiro e o DRE (caixa ou competência), o patrimônio, a evolução mês a mês e o fluxo de caixa previsto e realizado, e exporta tudo para o contador em Excel e PDF. | O exemplo de outubro: a empresa vendeu bem e encheu o pátio de ferro, mas saiu mais dinheiro do que entrou. DRE em papel. Gráfico de barras mês a mês. Balança de dois pratos "caixa × competência". Pasta do contador com Excel e PDF.<br>**Tema na fonte:** *Narcos*, o resultado do mês (sobrou ou faltou).<br>**Evitar:** depreciação, livro do imobilizado e cálculo automático de ganho ou perda na venda de ativo. Nada disso existe. | Formação básica | **Em montagem.** Voz e ilustrações prontas; gravação final na fila, logo depois da T05. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T15/roteiro.md) · legenda e vídeo ainda não existem | Não definido. Candidatas: "Relatórios" e parte de "Financeiro" (a confirmar) |
| 15ª | T21 | Cato, o assistente | Apresenta o Cato, o agente de inteligência artificial do EcoSistema. Ele responde perguntas sobre o negócio, em português, com número, gráfico ou tabela. Também prepara tarefas (compra, venda, baixa de conta, cadastro e até nota fiscal), que só são feitas depois que você confirma no cartão. A aula cobre ainda memória, arquivos, limites e permissões. | Painel de conversa ao lado da tela. Microfone "Falar" e o botão "Ouvir a resposta" (os dois existem). Resposta com gráfico ou tabela. Cartão de confirmação antes de lançar. Foto, planilha ou PDF anexados na conversa. A identidade oficial do Cato.<br>**Tema na fonte:** *Her*, perguntar em voz alta e receber a resposta.<br>**Evitar:** o Cato fazendo uma ação sozinho, sem o cartão de confirmação. | Formação básica | **Roteiro aprovado.** Voz pronta; faltam as ilustrações, a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T21/roteiro.md) · legenda e vídeo ainda não existem | Nenhuma: o catálogo antigo não tinha o Cato (a confirmar) |
| 16ª (fecha a Fase 1) | T25 | Dashboard, Agenda e rotina | Lê o Dashboard: comprado, vendido, margem, seis meses, rankings, quem deve e como você paga, além de montar o painel do seu jeito. Usa a Agenda (tarefas, avisos automáticos) e os atalhos, como o Ctrl+K, para montar a rotina diária, semanal e mensal. | O dono começando o dia com três perguntas: como vai o mês, que conta vence e o que tem para amanhã. Painel de indicadores. Calendário com tarefas. Checklist de rotina. Atalho Ctrl+K.<br>**Tema na fonte:** *Os Trapalhões*, o dia começando no painel.<br>**Evitar:** chamar margem de lucro (a aula separa as duas coisas). | Formação básica | **Roteiro aprovado.** Voz e ilustrações prontas; faltam a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T25/roteiro.md) · legenda e vídeo ainda não existem | Não definido. Talvez parte de "Truques e Produtividade (Bônus)" (a confirmar) |
| 17ª | T16 | Nota Fiscal de mercadoria (NF-e) | Do certificado digital A1 até a nota autorizada. Configura empresa, impostos, cenários fiscais, série, numeração e a cota. Emite a nota avulsa, a partir de um pedido e de um caixa fechado. Trata a recusa da SEFAZ, o cancelamento, a correção, a devolução, a nota complementar e a inutilização de numeração. Mostra a DANFE e o XML, e recebe notas: manifestar e importar pelo XML. | Carga de cobre que só sai do pátio com a nota. Certificado digital. A nota passando pela SEFAZ. Pilha de DANFEs sem texto legível. Carimbo de autorizada ou recusada.<br>**Tema na fonte:** *Tropa de Elite*, o documento oficial (não tem jeitinho).<br>**Evitar:** o modelo novo da DANFE como atual. Também não mostrar "Ciência da operação" como botão de baixar nota. | Módulo Notas Fiscais | **Roteiro aprovado.** Conferido na versão 1.60.22, com voz ainda não gerada: espera a amostra do novo DANFE. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T16/roteiro.md) · legenda e vídeo ainda não existem | Não definido. Candidata: "Notas Fiscais (NF-e e MDF-e)", dividida com a T17 (a confirmar) |
| 18ª | T17 | Transporte, serviço e o contador | Cobre os outros documentos fiscais. O MDF-e acompanha a carga na estrada: veículo, motorista, percurso e encerramento. A nota de serviço (NFS-e) é emitida e também recebida do serviço que você tomou. Fecha com os relatórios de entrada e saída, o Estoque Fiscal e o pacote do mês para o contador. | Caminhão de alumínio na estrada para Minas Gerais, com o manifesto. Caçamba de coleta que vira cobrança. Pasta do mês entregue ao contador.<br>**Tema na fonte:** *O Náufrago*, a carga que sai e precisa chegar documentada.<br>**Evitar:** o SPED Fiscal, que está em beta e fica fora da trilha. | Módulo Notas Fiscais | **Roteiro aprovado.** Falta conferir na versão atual do app; voz ainda não gerada. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T17/roteiro.md) · legenda e vídeo ainda não existem | Não definido. Candidata: "Notas Fiscais (NF-e e MDF-e)", dividida com a T16 (a confirmar) |
| 19ª | T18 | Ambiental: MTR e CDF | Mantém a licença ambiental de pé. O MTR é o manifesto de cada carga de resíduo e sai junto com ela. O CDF é o certificado do destino. A aula mostra como configurar o acesso e os resíduos, emitir, acompanhar, baixar o PDF, usar um MTR como modelo, cancelar, resolver envio com erro e ligar com a nota da mesma carga. | Carga de chaparia saindo do pátio com o manifesto. Licença ambiental. Certificado do destino. Ordem no tempo: primeiro o MTR, depois o CDF.<br>**Tema na fonte:** *Chernobyl*, o resíduo precisa ter destino provado.<br>**Evitar:** sugerir que emitir a nota gera o MTR, ou o contrário. Os três documentos são independentes. | Módulo Notas Fiscais | **Roteiro aprovado.** Voz pronta; faltam as ilustrações, a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T18/roteiro.md) · legenda e vídeo ainda não existem | Nenhuma clara (a confirmar) |
| 20ª | T19 | Funcionários e ponto eletrônico | Coloca a equipe do pátio no sistema. Cobre cadastro e campos de folha, departamentos, vales, bônus e faltas, pagamentos, folha CLT, férias, décimo terceiro e rescisão (valores estimados), extrato e relatório da equipe. Mostra o ponto eletrônico pelo celular (com local e hora) ou pelo tablet da empresa, com a folha de ponto e a exportação. | Funcionário batendo o ponto no celular, no pátio. Tablet de ponto na parede. Vale saindo do caixa. O caderno de vales ficando para trás. Recibo e holerite.<br>**Tema na fonte:** *Tempos Modernos*, a equipe, o relógio e o dia de trabalho.<br>**Evitar:** apresentar a planilha como arquivo fiscal (ela não substitui AEJ nem AFD), ou INSS e IRRF como valores exatos (são estimados). | Módulo Funcionários (RH) | **Roteiro aprovado.** Voz e ilustrações prontas; faltam a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T19/roteiro.md) · legenda e vídeo ainda não existem | Não definido. Candidata: "Funcionários (RH)" (a confirmar) |
| 21ª | T27 | White Label | Deixa o sistema com a cara da empresa: logo e ícone, cor da marca, documentos e portal sem o rodapé do EcoSistema. Mostra como ligar e desligar, e que a troca aparece na hora para a empresa toda. | O logo da empresa entrando no menu. A cor da marca tomando conta da tela. Comprovante saindo com a marca da empresa. Rolo de pintura ou carimbo de marca.<br>**Tema na fonte:** *Mad Men*, a marca aplicada em tudo.<br>**Evitar:** domínio próprio, e-mail com a marca, tela de login personalizada, segunda cor ou tema escuro próprio. Também não sugerir que o "Nome Exibido no Sistema" aparece em algum lugar. Nada disso existe. | Módulo White Label | **Roteiro aprovado.** Voz e ilustrações prontas; faltam a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T27/roteiro.md) · legenda e vídeo ainda não existem | Nenhuma: é aula nova |
| 22ª | T20 | Portal do Cliente e Fornecedor | O parceiro abre um link e vê sozinho o que é dele: pedidos, saldo, notas, relatório e tabela de preços. Ele pode pedir uma coleta, mas como solicitação, e vê comprovantes e fotos dos pedidos. Você escolhe as abas e a senha e manda o link pelo WhatsApp. | A cooperativa parceira olhando o próprio saldo pelo celular. Um link aberto como janela para dentro do pátio. Pedido de coleta. Comprovante.<br>**Tema na fonte:** *A Janela Indiscreta*, o parceiro olhando para dentro, só para o que é dele.<br>**Evitar:** o parceiro mudando algo no sistema (ele só pede a coleta), ou baixando XML ou DANFE pelo portal. | Módulo Portal do Cliente | **Roteiro aprovado.** Voz e ilustrações prontas (uma ilustração pendente); faltam a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T20/roteiro.md) · legenda e vídeo ainda não existem | Nenhuma no catálogo antigo (a confirmar) |
| 23ª | T22 | Gerencial: matriz e filiais | A matriz, em Taubaté, enxerga a filial de Pindamonhangaba numa tela só. Cobre grupo e código de convite, Dashboard Gerencial, ranking por unidade, DRE do grupo (caixa e competência) e estoque do grupo. Mostra também enviar ativos, preço por unidade, transferência com aprovação, vender com o estoque da outra unidade e assinaturas numa fatura só. | Mesa da matriz com as unidades à frente. Dois pátios ligados por caminhões de transferência. Números das duas unidades chegando juntos.<br>**Tema na fonte:** *O Poderoso Chefão*, a mesa da matriz.<br>**Evitar:** mostrar preço de plano ou de fatura. | Módulo Gerencial | **Roteiro aprovado.** Voz e ilustrações prontas; faltam a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T22/roteiro.md) · legenda e vídeo ainda não existem | Não definido. Candidata: "Filiais (Gerencial)" (a confirmar) |
| 26ª (última) | T26 | CRM/Kanban | Organiza os negócios num funil para nenhuma oportunidade esfriar. Cobre funis e estágios, regras e automações, checklists e etiquetas, cartões com dono, valor e próximo passo, arrastar entre colunas, tarefas na Agenda, filtros e fechar o negócio. | Quadro com colunas e cartões sendo arrastados. Funil largo em cima e estreito embaixo. A indústria que avisou que tem sucata toda semana e o negócio esfriando.<br>**Tema na fonte:** *Suits*, o funil (muitos entram, poucos fecham).<br>**Evitar:** integração com WhatsApp, e-mail ou formulário, importação em massa, automação por tempo parado ou oportunidade virando pedido sozinha. Nada disso existe. | Módulo CRM/Kanban | **Roteiro aprovado.** Voz e ilustrações prontas; faltam a gravação final e a montagem. | [roteiro](https://github.com/KaikBarreto/claude-tutorials/blob/main/planejamento/ecoflix/T26/roteiro.md) · legenda e vídeo ainda não existem | Nenhuma: é aula nova |

Notas sobre a tabela:
- **Roteiro aprovado:** o Kaik dispensou a aprovação roteiro por roteiro. Aqui quer dizer roteiro fechado e conferido no app. A situação de cada aula tem dois pontos de corte:
  - "Em montagem" começa quando a gravação final começa.
  - "Pronta" começa quando o vídeo final é entregue.
- **Publicada:** nenhuma destas 12 está publicada. Não sei quais das 14 já entregues foram publicadas: a confirmar com o Kaik.
- **Tema na fonte:** é o tema listado na fonte oficial em "Tema de cada aula" (19/11). A mesma fonte, no cabeçalho de cada aula, traz outra "inspiração visual": por exemplo, *Wall-E* na T5 e *O Lobo de Wall Street* na T15. Conferir com o 1º lote para não repetir filme.
- **Ordem:**
  - Fase 1 (formação básica): T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T13, T14, T15, T21, T25.
  - Fase 2 (módulos): T16, T17, T18, T19, T27, T20, T22, T12, T11, T26.

## Aula antiga: nada está definido
- Nenhuma troca de aula antiga por aula nova foi decidida. A coluna "substitui" só aproxima os assuntos.
- O catálogo atual, pela migração de 31/10, tem estes títulos:
  - Comece por Aqui · Configurações Iniciais · Cadastros · Estoque
  - Caixa, Compras e Vendas · Saldos de Clientes e Fornecedores · Documentos e Comprovantes
  - Usuários e Permissões · Financeiro · Relatórios · Filiais (Gerencial)
  - Truques e Produtividade (Bônus) · Notas Fiscais (NF-e e MDF-e)
  - Integrações: Balanças e Impressoras · Funcionários (RH)
- Não sei se o banco mudou depois disso: a confirmar.
- As imagens em `public/images/capas/T0` a `T13` são da numeração antiga. Na antiga, "T5" era Saldos e "T11" era Relatórios. Não reaproveitar pelo nome do arquivo.

## Já cobertas pelo 1º lote (só para conferência)
- T00 · Bem-vindo ao EcoSistema
- T01 · Sua conta e sua empresa
- T02 · Usuários e permissões
- T03 · Materiais e tabelas de preço
- T04 · Clientes e Fornecedores. A vinheta e o arquivo entregue usam esse nome. O roteiro e a fonte chamam a aula de "Clientes, fornecedores e a ficha do parceiro". Conferir qual título foi para a capa.
- T06 · Caixa: abrir, fechar e o cofre
- T07 · Comprar e vender sucata
- T08 · Ticket de Pesagem
- T09 · Pedidos e histórico do caixa
- T10 · Estoque: saldo, histórico e posição
- T11 · Produção
- T12 · Coletas e Logística
- T13 · Contas a Pagar e Receber
- T14 · Bancos, cofre e conciliação bancária

## DomiFlix (produto: Dominex), à parte
- Nenhuma aula nova da DomiFlix está planejada.
- A trilha inteira, com 21 aulas e a T0 vertical, foi entregue ao Kaik em 06/11.
- Fica a confirmar se essas aulas já têm capa e se já foram publicadas.

| Ordem | Aula | Título | Produto | Situação |
|---|---|---|---|---|
| 1 | T0 | Boas-vindas à Dominex (com versão vertical) | Dominex | Pronta (entregue 06/11) |
| 2 | T1 | Configurações e identidade da empresa | Dominex | Pronta |
| 3 | T2 | Usuários, cargos e permissões | Dominex | Pronta |
| 4 | T3 | Clientes, Fornecedores e Equipamentos | Dominex | Pronta |
| 5 | T4 | Serviços, tarefas e checklists (o roteiro diz "Tipos de Serviço, Tipos de Tarefa e Checklists"; a confirmar) | Dominex | Pronta |
| 6 | T5 | Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo | Dominex | Pronta |
| 7 | T7 | O técnico em campo | Dominex | Pronta |
| 8 | T18 | Área do Técnico: Refrigeração e Climatização | Dominex | Pronta |
| 9 | T8 | Estoque, compras e inventário | Dominex | Pronta |
| 10 | T9 | Orçamentos, Precificação e Proposta | Dominex | Pronta |
| 11 | T10 | CRM: funil, leads e captação | Dominex | Pronta |
| 12 | T11 | Contratos e PMOC | Dominex | Pronta |
| 13 | T12 | Portal do Cliente e Portal do Contrato | Dominex | Pronta |
| 14 | T13 | Financeiro | Dominex | Pronta |
| 15 | T19 | Integração com Asaas, Assinaturas e Cobranças | Dominex | Pronta |
| 16 | T20 | Relatório Financeiro e DRE | Dominex | Pronta |
| 17 | T14 | Notas Fiscais | Dominex | Pronta |
| 18 | T15 | Funcionários: Financeiro do Funcionário e Ponto Eletrônico | Dominex | Pronta |
| 19 | T22 | Ferramentas de RH: DISC, Organograma, Fluxograma | Dominex | Pronta |
| 20 | T21 | Integração com WhatsApp | Dominex | Pronta |
| 21 | T17 | Dashboard, relatórios e exportações | Dominex | Pronta |
