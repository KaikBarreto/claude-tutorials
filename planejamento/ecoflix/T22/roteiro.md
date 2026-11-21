# Roteiro T22 · Gerencial: matriz e filiais

Roteiro para a voz e a gravação no app 1.60.18, tela 1600x900, menu lateral aberto. A fala (coluna Fala) é a de `narracao/tts_textos.py`, na grafia da legenda (DRE e CMV; a pronúncia do TTS fica no tts). A coluna Tela resume o que o robô faz, com os rótulos copiados do código 1.60.18 (`inventario.md`); o passo a passo exato está nas docstrings e nas marcas de `rec/t22/gerar.py`. Mundo, números e sementes: `plano.md`. Cobertura aplicada: `cobertura_160.md`.

- **Título:** Gerencial: matriz e filiais
- **Antes:** Relatório Financeiro e DRE (T15)
- **Próximo:** Coletas e Logística (T12)
- **Capítulos:** 19 (0 a 18). Novos em 20/11: 4, 9, 11, 13, 15, 16. Renumerados: Dashboard 4→5, Ranking 5→6, DRE 6→7, Competência 7→8, Estoque 8→10, Enviar Ativos 9→12, Transferência 10→14, Assinaturas 11→17, Recapitulando 12→18.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça) em todos os capítulos.
- **Fala:** 2838 palavras (antes 1.410). Sem travessão; número por extenso; valores calculados só depois de vistos na tela (os que ainda dependem do ensaio estão marcados em `andamento_160.md`).
- Não anunciar: nota de teste (homologação) e modelo novo da DANFE. Fala não cita PDF; exportações (DRE Exportar, Exportar Relatório) ficam sem filmar.
- Marcas na Tela: `[BACKEND: ...]`, `[ZOOM: ...]`, `[ILUSTRAÇÃO: ...]` (as ilustrações estão em `cenas/ilustracoes.json`).

## Capítulos

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Abertura: Dashboard do EcoSistema da matriz; o cursor abre o grupo "Gerencial (Filiais)" do menu (ilustração na L2). | Oi! Neste tutorial a gente vai fazer a matriz da Recicla Vale Metais, em Taubaté, enxergar a filial de Pindamonhangaba sem precisar entrar no sistema dela. |
| (segue a tela da linha anterior; ver `gerar.py`) | Com duas unidades, pra saber quanto o grupo vendeu no mês, alguém precisava abrir os dois sistemas e somar na mão. Aqui, os números das duas chegam juntos numa tela só. |
| (segue a tela da linha anterior; ver `gerar.py`) | Isso é o Gerencial. Ele depende do plano contratado, e quem contrata é a matriz. E quem pode abrir cada tela dele, você decide nas permissões de cada usuário. |
| (segue a tela da linha anterior; ver `gerar.py`) | Como ele junta a dê-érri-ê das unidades, se você ainda não viu o tutorial Relatório Financeiro e dê-érri-ê, dá uma olhada antes. [pause] Vamos entender como ele funciona. |

### cap01 · Como o Gerencial funciona

| Tela | Fala |
| --- | --- |
| Como o Gerencial funciona: "Dashboard" do grupo Gerencial mostra "Módulo Gerencial" (sem grupo); ilustrações nas L2 a L4. | Sem grupo, o Gerencial começa assim, pedindo pra criar um. |
| (segue a tela da linha anterior; ver `gerar.py`) | O grupo junta as unidades. Cada unidade é uma empresa própria no sistema, com login e assinatura próprios. A matriz é a dona do grupo, e a filial entra nele. |
| (segue a tela da linha anterior; ver `gerar.py`) | A matriz enxerga os números de todas, manda o mesmo padrão de cadastro pras filiais e transfere material entre elas. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: o Gerencial junta e padroniza, mas quem opera a filial é a filial. O caixa, as compras e as notas dela continuam com quem trabalha lá. |

### cap02 · Criar o grupo e o código

| Tela | Fala |
| --- | --- |
| Criar o grupo e o código: Configurar Grupo, "Grupo Recicla Vale", Criar Grupo; abas, passo a passo, o botão Como funciona (janela dos cinco passos), código de convite e validade, copiar, Unidades Ativas (1/11) só com a matriz. Vira apos-cap02. | Começando pela matriz. Clico em Configurar Grupo pra criar o grupo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Dou o nome, Grupo Recicla Vale, e clico em Criar Grupo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Pronto. Aqui ficam as abas do grupo e um passo a passo do que falta configurar. |
| (segue a tela da linha anterior; ver `gerar.py`) | Se bater dúvida no caminho, o botão Como funciona abre um resumo dos cinco passos, do convite até os resultados. |
| (segue a tela da linha anterior; ver `gerar.py`) | E esse é o código de convite. É ele que liga a filial ao grupo, e vale por trinta dias. Se vencer, o botão do lado gera outro. |
| (segue a tela da linha anterior; ver `gerar.py`) | Copio o código e mando pra quem cuida da filial, por mensagem. |
| (segue a tela da linha anterior; ver `gerar.py`) | Por enquanto, a lista de unidades tem só a matriz. E repara no contador: um de onze, a matriz mais até dez filiais. |

### cap03 · Do lado da filial

| Tela | Fala |
| --- | --- |
| Do lado da filial (Sandra Pires): Configurações (rodapé do menu) › Empresa › cartão Filial; liga É Filial, cola o código e Vincular. Vira apos-cap03. | Agora do lado da filial. A Sandra, gerente em Pindamonhangaba, entra no sistema da filial, em Configurações, na aba Empresa. |
| (segue a tela da linha anterior; ver `gerar.py`) | Lá embaixo fica o cartão Filial. Ela liga o É Filial. |
| (segue a tela da linha anterior; ver `gerar.py`) | E cola o código que recebeu da matriz. |
| (segue a tela da linha anterior; ver `gerar.py`) | Vincular. Pronto, a filial está no Grupo Recicla Vale. |
| (segue a tela da linha anterior; ver `gerar.py`) | Do lado dela, o dia a dia segue igual: a filial continua usando o próprio sistema, e a matriz passa a enxergar os números. |

### cap04 · Quando o código não entra

| Tela | Fala |
| --- | --- |
| Quando o código não entra: a Sandra cola o código VENCIDO e leva "Código de convite expirado"; (a ilustração cobre a troca de usuário); na matriz, o aviso vermelho "Código expirado"; o botão de girar gera GRP-3F81B2, válido por mais 30 dias. Semente codigo-vencido (não segue). | E se o código não entrar? O caso mais comum é esse: o código passou dos trinta dias, e o sistema avisa que ele expirou. |
| (segue a tela da linha anterior; ver `gerar.py`) | As outras recusas são três. Código inválido: confira letra por letra. Empresa que já está em outro grupo: ela precisa sair de lá antes. E grupo cheio: cada grupo aceita até dez filiais. |
| (segue a tela da linha anterior; ver `gerar.py`) | Na matriz, o aviso também aparece em vermelho, embaixo do código. |
| (segue a tela da linha anterior; ver `gerar.py`) | Um clique nesse botão gera um código novo, com mais trinta dias. O antigo deixa de valer, então mande o novo pra filial. |

### cap05 · O Dashboard Gerencial

| Tela | Fala |
| --- | --- |
| O Dashboard Gerencial: do menu, Dashboard; Mês passado (e o Personalizado); o seletor de unidades (só a filial e volta a todas); cartões Receita Total e Despesa Total; o Lucro Líquido (o resultado da DRE em competência); setinha; Estoque Total; gráfico por unidade. | De volta à matriz. Com a filial no grupo, o Dashboard Gerencial já mostra as duas unidades. |
| (segue a tela da linha anterior; ver `gerar.py`) | Vou olhar outubro inteiro: em cima, Mês passado. Além dos atalhos, o Personalizado aceita qualquer intervalo de datas. |
| (segue a tela da linha anterior; ver `gerar.py`) | E o seletor de unidades aceita marcar uma, duas ou todas. Marcando só a filial, os cartões e os gráficos passam a mostrar só ela. Esse mesmo seletor aparece no Financeiro e no Estoque. |
| (segue a tela da linha anterior; ver `gerar.py`) | Os cartões somam o grupo. Em outubro, a receita foi de trezentos e quarenta e quatro mil e quarenta reais, e a despesa, de trezentos e setenta mil, seiscentos e noventa. |
| (segue a tela da linha anterior; ver `gerar.py`) | O Lucro Líquido é o resultado da dê-érri-ê do grupo, em competência: o mesmo número que você vai encontrar no Financeiro. |
| (segue a tela da linha anterior; ver `gerar.py`) | A setinha compara com o período anterior do mesmo tamanho, no caso, setembro. E o Estoque Total soma o estoque das duas unidades. |
| (segue a tela da linha anterior; ver `gerar.py`) | No gráfico, cada unidade aparece com a receita e a despesa lado a lado. A estrela marca a matriz. |

### cap06 · Ranking e resumo por unidade

| Tela | Fala |
| --- | --- |
| Ranking e resumo por unidade: Ranking por Saldo (Receita − Despesa; filial na frente, matriz negativa); Resumo por Unidade, linha da matriz e da filial. | E o ranking ordena as unidades pelo saldo, a receita menos a despesa. Em outubro, a filial ficou na frente, e a matriz, no vermelho. |
| (segue a tela da linha anterior; ver `gerar.py`) | Embaixo vem o resumo por unidade, em números. |
| (segue a tela da linha anterior; ver `gerar.py`) | A matriz teve duzentos e setenta e dois mil e quarenta de receita e duzentos e noventa e nove mil, seiscentos e noventa de despesa. Ficou negativa em vinte e sete mil, seiscentos e cinquenta reais. |
| (segue a tela da linha anterior; ver `gerar.py`) | A filial vendeu setenta e dois mil, gastou setenta e um mil e ficou com mil reais de saldo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Repara no vermelho da matriz. É que aqui entra a compra inteira do mês, até o material que ainda está no pátio esperando venda. Por isso esse saldo não é igual ao Lucro Líquido do cartão, que segue a dê-érri-ê em competência. |

### cap07 · A dê-érri-ê do grupo

| Tela | Fala |
| --- | --- |
| A DRE do grupo: Financeiro › DRE › Mês passado (Consolidado); Regime de Caixa: vendas, compras, resultado de caixa; impostos, despesas, outras receitas e o resultado do período; Comparativo e a linha Resultado por unidade. | Agora o Financeiro. Na aba dê-érri-ê, com outubro escolhido, fica a dê-érri-ê do grupo inteiro. |
| (segue a tela da linha anterior; ver `gerar.py`) | Começo pelo regime de caixa, o dinheiro que entrou e saiu. O grupo vendeu trezentos e quarenta e um mil, duzentos e quarenta, e comprou trezentos e dezoito mil, oitocentos e sessenta em material. |
| (segue a tela da linha anterior; ver `gerar.py`) | Tirando os impostos e as despesas da operação, e somando o aluguel de caçamba, o mês fecha no vermelho: menos vinte e seis mil, seiscentos e cinquenta reais. |
| (segue a tela da linha anterior; ver `gerar.py`) | E no Comparativo fica a mesma dê-érri-ê, unidade por unidade. |
| (segue a tela da linha anterior; ver `gerar.py`) | O vermelho do grupo vem da matriz, menos vinte e sete mil, seiscentos e cinquenta, contra mil positivos da filial. Assim você vê de onde vem o resultado. |

### cap08 · Caixa e competência

| Tela | Fala |
| --- | --- |
| Caixa e competência: a DRE do grupo em Regime de Competência (CMV, Lucro Bruto, resultado); depois Caixa e Competência de novo, com a câmera no resultado. | Agora o mesmo outubro em regime de competência. No lugar das compras entra o cê-ême-vê, o custo só do material que foi vendido: duzentos e setenta e três mil, oitocentos e setenta e três reais e trinta centavos. |
| (segue a tela da linha anterior; ver `gerar.py`) | E o resultado do mês vira positivo: dezoito mil, trezentos e trinta e seis reais e setenta centavos. |
| (segue a tela da linha anterior; ver `gerar.py`) | A diferença, quase quarenta e cinco mil, é o material que a gente comprou em outubro e ainda está no pátio. No caixa, ele já pesa no mês. Na competência, ele só vira custo quando for vendido. |
| (segue a tela da linha anterior; ver `gerar.py`) | O caixa mostra o dinheiro do mês. A competência mostra o lucro do que foi vendido. Os dois estão certos: cada um responde uma pergunta. |
| (segue a tela da linha anterior; ver `gerar.py`) | E o Comparativo, em competência, mostra o cê-ême-vê de cada unidade, o custo só do que ela vendeu. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: se aparecer aqui o aviso de material em estoque sem custo de compra, o lucro em competência pode estar maior do que é. Confira as entradas do período antes de decidir em cima do número. |

### cap09 · Além da dê-érri-ê

| Tela | Fala |
| --- | --- |
| Além da DRE: as linhas da DRE que abrem (Total Despesas); o Exportar (sem clicar) e o Patrimônio Operacional Atual; a aba Dashboard (por categoria); a aba Histórico (Receitas, Despesas, Compras) com o filtro Conta bancária. Semente apos-cap03. | Ainda no Financeiro, três coisas rápidas. Na dê-érri-ê, as linhas de custos, impostos e despesas abrem, e mostram do que o total é feito. |
| (segue a tela da linha anterior; ver `gerar.py`) | Pelo botão Exportar, a dê-érri-ê vai pro contador ou pro sócio, com as unidades que você escolheu. E embaixo, o Patrimônio Operacional soma o caixa, o banco, o que tem a receber, o estoque e o que tem a pagar, do grupo inteiro. |
| (segue a tela da linha anterior; ver `gerar.py`) | A aba Dashboard mostra onde o grupo gasta e de onde vem a receita, por categoria. |
| (segue a tela da linha anterior; ver `gerar.py`) | E a aba Histórico lista os lançamentos das unidades, um por um. Dá pra filtrar por categoria e até pela conta bancária de onde o dinheiro saiu. Essas telas funcionam como no tutorial Relatório Financeiro e dê-érri-ê. |

### cap10 · O estoque do grupo

| Tela | Fala |
| --- | --- |
| O estoque do grupo: Visão Geral (as duas unidades, latinha 640 + 1.850); Posição de Estoque em 31/10 (Ver posição, a linha abre por unidade, Por unidade); Histórico de Materiais com Filtros (material Alumínio latinha); Relatório de Estoque (o cartão Total Comprado abre, a linha do material abre por unidade, Usuários, Ocultar itens zerados, Exportar Relatório, sem clicar). | Agora o estoque. No Estoque Gerencial, a Visão Geral junta o estoque das duas unidades. |
| (segue a tela da linha anterior; ver `gerar.py`) | Na tabela, cada material numa linha e cada unidade numa coluna. O alumínio latinha: seiscentos e quarenta quilos na matriz e mil oitocentos e cinquenta na filial. No total, dois mil quatrocentos e noventa. |
| (segue a tela da linha anterior; ver `gerar.py`) | A Posição de Estoque é uma foto do estoque numa data. Escolho trinta e um de outubro e clico em Ver posição: o saldo, o custo médio e o valor de cada material no fim daquele dia. |
| (segue a tela da linha anterior; ver `gerar.py`) | Clicando no material, ele abre unidade por unidade. E o botão Por unidade muda a tabela inteira pra esse jeito. |
| (segue a tela da linha anterior; ver `gerar.py`) | No Histórico de Materiais, o botão Filtros escolhe o período e o material. Cada linha mostra o tipo do movimento, a unidade e quem fez. |
| (segue a tela da linha anterior; ver `gerar.py`) | No Relatório de Estoque, os cartões de cima abrem. O Total Comprado mostra o preço médio e quanto saiu em dinheiro, em Pix, pelo saldo do parceiro e o que ficou em aberto. |
| (segue a tela da linha anterior; ver `gerar.py`) | E a linha do material abre por unidade. É aqui que você descobre se uma unidade está pagando mais caro que a outra no mesmo material. |
| (segue a tela da linha anterior; ver `gerar.py`) | Dá pra filtrar por usuário, esconder o que não teve movimento e exportar o relatório. |

### cap11 · Corrigir o estoque de uma unidade

| Tela | Fala |
| --- | --- |
| Corrigir o estoque de uma unidade: Estoque Gerencial › Visão Geral › ⋯ da linha Papelão › Corrigir saldo (Unidade: Filial Pindamonhangaba, Saída de 30, motivo, Registrar saída); depois Transferir entre materiais (só a janela, Cancelar). A ilustração do aviso de divergência é da coordenação. Semente apos-cap03 (não segue). | Agora um caso do dia a dia. A filial contou o papelão no pátio e achou trinta quilos a menos que o sistema. A matriz resolve daqui, no menu de ações da linha. |
| (segue a tela da linha anterior; ver `gerar.py`) | Corrigir saldo. Escolho a unidade, a filial. |
| (segue a tela da linha anterior; ver `gerar.py`) | É uma saída de trinta quilos. A janela mostra o saldo de agora e como ele fica depois. |
| (segue a tela da linha anterior; ver `gerar.py`) | Escrevo o motivo. E repara: a correção fica no histórico da filial, marcada como ajuste feito pela matriz. Ninguém fica sem saber. |
| (segue a tela da linha anterior; ver `gerar.py`) | Registrar saída. Pronto, o estoque da filial está certo. |
| (segue a tela da linha anterior; ver `gerar.py`) | No mesmo menu, o Transferir entre materiais passa saldo de um material pra outro dentro da mesma unidade. Serve quando a filial lançou a compra no material errado. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: essa tela soma as movimentações de cada unidade. Se um material tiver saldo no cadastro sem movimentação que explique, aparece um aviso embaixo, com a diferença material por material. O sistema não mexe sozinho: a conferência é sua. |

### cap12 · Enviar Ativos

| Tela | Fala |
| --- | --- |
| Enviar Ativos: Configurações do grupo (o passo a passo) › Catálogo (Importar do Estoque da Matriz; Sucata eletrônica entra e sai pela lixeira), Tabelas de Preço (entram sozinhas), Clientes e Fornecedores (marca a Fundição; Fornecedores com busca: marca e desmarca a Cooperativa Recomeço), Categorias (o cadeado); Unidades › Enviar Ativos (Desmarcar todos, Marcar todos, Sobrescrever desligado) › Confirmar Envio; Histórico de Envios; a lixeira da filial (sem clicar). Vira apos-cap09. | Agora a padronização. A matriz monta o padrão do grupo, e a filial recebe. Na aba Unidades, o passo a passo lá de cima mostra o que falta, e cada etapa leva à aba certa. Começa pelo catálogo de materiais. |
| (segue a tela da linha anterior; ver `gerar.py`) | Com um clique, o Importar do Estoque da Matriz traz os materiais que a matriz já usa. |
| (segue a tela da linha anterior; ver `gerar.py`) | Material que a matriz não trabalha também entra: é só dar o nome e a unidade. Ele aparece sem vínculos até alguma unidade usar. Foi engano? A lixeira tira do catálogo. |
| (segue a tela da linha anterior; ver `gerar.py`) | As tabelas de preço da matriz entram sozinhas, assim que você abre a aba. |
| (segue a tela da linha anterior; ver `gerar.py`) | Em Clientes e Fornecedores, você marca quem também faz negócio com a filial. A Fundição Bandeira do Vale compra das duas unidades, então eu marco. |
| (segue a tela da linha anterior; ver `gerar.py`) | Os fornecedores ficam na outra aba, com busca. Marcou, está disponível. Desmarcou, sai da lista das filiais. |
| (segue a tela da linha anterior; ver `gerar.py`) | E as categorias financeiras também vêm prontas da matriz. Dá pra desmarcar as que são só da matriz. As de cadeado vão sempre, porque a dê-érri-ê precisa delas. |
| (segue a tela da linha anterior; ver `gerar.py`) | Com tudo pronto, na aba Unidades, o Enviar Ativos manda o padrão pra filial. E não precisa mandar tudo sempre: dá pra desmarcar o que você não quer. Aqui eu mando tudo. |
| (segue a tela da linha anterior; ver `gerar.py`) | O que ela já tinha fica como está, e o que faltava entra. O preço que a filial já tem fica protegido, a não ser que você ligue o Sobrescrever preços existentes. |
| (segue a tela da linha anterior; ver `gerar.py`) | Confirmar Envio. Agora as duas unidades falam a mesma língua: o mesmo material, com o mesmo nome. |
| (segue a tela da linha anterior; ver `gerar.py`) | Lá embaixo, o Histórico de Envios guarda pra qual filial foi, o que foi enviado e quando. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: se tirar uma filial do grupo por engano, nenhum dado dela se perde. Pra voltar, é só a filial colar o código de novo. |

### cap13 · Preço diferente por unidade

| Tela | Fala |
| --- | --- |
| Preço diferente por unidade: Configurações do grupo › Tabelas de Preço › a tabela Principal (a grade de preços); Alumínio latinha: compra 6,20 -> 6,30 e Salvar; Vinculação por Unidade: liga a Filial Pindamonhangaba, Tipo %, Direção - (abaixo), Valor 5, Salvar; Aplicar; zoom em Importar da matriz e Excluir (sem clicar). Semente apos-cap09 (não segue: o cap14 parte do mesmo estado). | O padrão do grupo inclui o preço. Abrindo uma tabela, aparecem os materiais do catálogo com o preço de compra e o de venda. |
| (segue a tela da linha anterior; ver `gerar.py`) | Dá pra ajustar aqui mesmo. Subo a compra da latinha pra seis e trinta e salvo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Embaixo fica a Vinculação por Unidade. É ela que diz como cada unidade recebe esses preços. Ligo a filial. |
| (segue a tela da linha anterior; ver `gerar.py`) | A filial fica mais longe do comprador e tem frete, então ela trabalha cinco por cento abaixo da tabela. Tipo, porcentagem. Direção, abaixo. Valor, cinco. Salvar. |
| (segue a tela da linha anterior; ver `gerar.py`) | E o Aplicar grava os preços na filial, já com o desconto. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: essa variação vale para os dois preços, o de compra e o de venda. Se a diferença for em reais por quilo, troque o tipo pra valor fixo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Nessa barra você também puxa os preços de uma tabela da matriz ou exclui a tabela. O Excluir não pede confirmação, então cuidado com o clique. |

### cap14 · Transferência com aprovação

| Tela | Fala |
| --- | --- |
| Transferência com aprovação: aba Transferências, liga "Exigir aprovação"; Nova: filial -> matriz, alumínio latinha 1.200 kg, observação; Solicitar; Pendente; Executar; Confirmar e Executar; o Estoque Gerencial com 1.840 e 650 kg. Vira apos-cap10. | Agora as transferências. A filial juntou alumínio latinha, e a matriz vai vender um lote grande. Primeiro, eu ligo o Exigir aprovação em transferências. |
| (segue a tela da linha anterior; ver `gerar.py`) | Assim, nenhum estoque se move sem confirmação. Em Nova, a origem é a filial e o destino, a matriz. |
| (segue a tela da linha anterior; ver `gerar.py`) | O material é o alumínio latinha: mil e duzentos quilos. |
| (segue a tela da linha anterior; ver `gerar.py`) | Repara no aviso do resumo: com a aprovação ligada, o estoque ainda não se move. Clico em Solicitar uma transferência. |
| (segue a tela da linha anterior; ver `gerar.py`) | A transferência fica pendente. Quando o caminhão chega na matriz e o material é conferido, aí sim, Executar. A tela pede pra confirmar que o destino está de acordo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Confirmar e Executar. Pronto: a matriz fica com mil oitocentos e quarenta quilos, e a filial com seiscentos e cinquenta. O total do grupo continua o mesmo. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: um material do grupo pode juntar mais de um material de uma unidade. O total do grupo soma todos, e a transferência tira de um só. Se o número do grupo parecer estranho, confira material por material. |

### cap15 · Lote, fila e o pedido da filial

| Tela | Fala |
| --- | --- |
| Lote, fila e o pedido da filial: a Sandra marca Papelão e Plástico PET no Materiais e pede a transferência (Transferir Estoque › Enviar 2 Transferência(s)); (a ilustração cobre a troca para o Rafael); na matriz, Estoque Gerencial › Transferências (contador); Nova: lote (Selecionar todos com saldo; só Ferro misto; quantidade acima do saldo avisa; 500 kg; Solicitar); Cancelar o Plástico PET; Executar todas (2); Visão Geral › ⋯ do Inox › Transferir entre unidades. Semente apos-cap10 (não segue). | A filial também pode pedir. No estoque dela, a Sandra marca os materiais e clica em Transferir Estoque. |
| (segue a tela da linha anterior; ver `gerar.py`) | Escolhe o destino e as quantidades. A tela mostra quanto tem em cada unidade e quanto vai ficar. O pedido segue pra matriz, e o estoque ainda não se move. |
| (segue a tela da linha anterior; ver `gerar.py`) | Esse pedido cai numa fila porque o grupo exige aprovação. Com o Exigir aprovação desligado, não existe fila: a transferência feita pela matriz move o estoque na hora. |
| (segue a tela da linha anterior; ver `gerar.py`) | Na matriz, o Estoque Gerencial tem uma aba Transferências, com o número de pedidos esperando. |
| (segue a tela da linha anterior; ver `gerar.py`) | Em Nova, a matriz monta um lote com vários materiais de uma vez. O Selecionar todos com saldo marca tudo que a origem tem. Se a quantidade passar do estoque, a linha avisa e o sistema não deixa seguir. |
| (segue a tela da linha anterior; ver `gerar.py`) | Corrijo e solicito. Agora são três na fila. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma delas não vai mais sair: Cancelar. Ela fica na lista, marcada como cancelada. |
| (segue a tela da linha anterior; ver `gerar.py`) | E as outras duas eu executo juntas, no Executar todas. Se alguma não tiver saldo na origem, as demais seguem, e a tela lista qual falhou e por quê. |
| (segue a tela da linha anterior; ver `gerar.py`) | Tem também um atalho na Visão Geral: no menu da linha, Transferir entre unidades já abre a transferência com o material escolhido. |

### cap16 · Vender com o estoque da outra unidade

| Tela | Fala |
| --- | --- |
| Vender com o estoque da outra unidade: Configurações do grupo › Transferências › liga "Usar estoque de outras unidades na venda" na matriz; Venda da matriz: cliente Serra Fina, Alumínio perfil 3.585 kg (faltam 200); Incluir Item › "Estoque insuficiente" › Origem do estoque › Outras unidades › Filial Pindamonhangaba › Transferir e Adicionar (o item entra; a transferência sai ao finalizar, que o capítulo não faz). Semente apos-cap10 + venda-outra-unidade (aprovação desligada). | Último recurso das transferências. Nessa mesma aba fica o Usar estoque de outras unidades na venda, com uma chave por unidade. Ligo na matriz. |
| (segue a tela da linha anterior; ver `gerar.py`) | Agora, numa venda da matriz, faltam duzentos quilos de alumínio perfil. Em vez de travar, a janela pergunta de onde vem o resto. |
| (segue a tela da linha anterior; ver `gerar.py`) | Na lista aparece a filial, com o saldo que ela tem. Escolho, e a quantidade fica coberta. |
| (segue a tela da linha anterior; ver `gerar.py`) | Transferir e Adicionar. O item entra na venda, e a transferência da filial pra matriz acontece junto, quando a venda é finalizada. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica importante: isso só funciona com o Exigir aprovação desligado. Com a aprovação ligada, a venda avisa que o grupo exige aprovação e só deixa usar o estoque da própria unidade. É uma escolha do grupo: ou o controle da aprovação, ou a agilidade na venda. |

### cap17 · Assinaturas numa fatura só

| Tela | Fala |
| --- | --- |
| Assinaturas numa fatura só: Assinaturas do grupo (a matriz e a filial; o botão Gerenciar sem abrir); Pagar tudo de uma vez; o aviso das cobranças; a chave Cobrança recorrente (ligada); PIX (QR fictício); o pagamento confirmado por um passo de bastidor. Vira apos-cap11. | Por último, as assinaturas. Cada unidade tem a sua, e aqui a matriz vê todas: o plano, se está ativa e quando vence. |
| (segue a tela da linha anterior; ver `gerar.py`) | O Gerenciar de cada linha deixa a matriz mudar o plano daquela unidade, sem precisar do login dela. |
| (segue a tela da linha anterior; ver `gerar.py`) | E dá pra pagar tudo de uma vez, numa fatura só, na matriz. |
| (segue a tela da linha anterior; ver `gerar.py`) | Repara no aviso: ao pagar, a cobrança de cada unidade é cancelada e vira uma fatura única, na matriz. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica importante: se a filial tinha um boleto ou um Pix da assinatura dela em aberto, ela não deve mais pagar aquele documento. Quem paga agora é a matriz, nessa fatura. |
| (segue a tela da linha anterior; ver `gerar.py`) | Repara na Cobrança recorrente, que já vem ligada: o total do grupo é cobrado sozinho todo mês. Se quiser pagar só este mês, desligue antes de escolher a forma de pagamento. |
| (segue a tela da linha anterior; ver `gerar.py`) | As formas são cartão, sempre recorrente, Pix ou boleto. Escolho o Pix, e o QR Code do grupo aparece. |
| (segue a tela da linha anterior; ver `gerar.py`) | Pagou, e pronto: as cobranças das unidades passam a vir nessa fatura da matriz. |
| (segue a tela da linha anterior; ver `gerar.py`) | Uma dica: pra pagar junto, todas as unidades precisam estar no mesmo ciclo, mensal ou anual. Se uma for anual e a outra mensal, o sistema avisa e não gera a fatura. Acerte o ciclo no Gerenciar e tente de novo. |

### cap18 · Recapitulando

| Tela | Fala |
| --- | --- |
| Sem robô: capítulo de resumo, só vinheta e ilustração. | Pronto! Recapitulando: a gente criou o grupo na matriz, gerou o código de convite e vinculou a filial de Pindamonhangaba. |
| (segue a tela da linha anterior; ver `gerar.py`) | Viu o que fazer quando o código vence ou não entra. |
| (segue a tela da linha anterior; ver `gerar.py`) | Leu o Dashboard Gerencial, com o ranking e o resumo de cada unidade. |
| (segue a tela da linha anterior; ver `gerar.py`) | Viu a dê-érri-ê do grupo nos dois regimes, comparou unidade por unidade e foi além, até o histórico e o patrimônio. |
| (segue a tela da linha anterior; ver `gerar.py`) | Conferiu o estoque do grupo, corrigiu o saldo da filial e mandou o mesmo catálogo, com o preço certo de cada unidade. |
| (segue a tela da linha anterior; ver `gerar.py`) | Transferiu material com aprovação, montou um lote, executou a fila e vendeu com o estoque da outra unidade. |
| (segue a tela da linha anterior; ver `gerar.py`) | E pagou as assinaturas numa fatura só. |
| (segue a tela da linha anterior; ver `gerar.py`) | No próximo tutorial, o caminhão sai do pátio pra buscar material. Até lá! |
