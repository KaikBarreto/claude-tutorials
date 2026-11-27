# Melhorias para o EcoSistema · achados da produção da EcoFlix

Pedido do Kaik (10/11 01:42): "esses levantamentos de bugs vá anotando pra no final me dar um report do que melhorar no
sistema desses problemas". Fonte: a leitura do código da versão 1.59.154 feita pelos roteiros (e, depois, os ensaios e
as gravações). Cada item diz a aula em que apareceu. **No fim da produção, vira o report para o Kaik.**

## 1. Prováveis bugs (o sistema faz diferente do que a tela promete)
- **Peso Líquido mostra o bruto** (T7): na compra e na venda, a coluna "Peso Líquido" exibe o peso bruto.
- **Usuário novo perde a foto e a tela inicial** (T2): o que se escolhe na criação nunca é gravado, porque a tela lê
  `result.userId` e a edge `create-company-user` não devolve esse campo. O perfil rápido também não grava na criação
  (só pelo "Editar").
- **Ticket sem valores ignora a tabela do fornecedor** (T8): ao valorizar um ticket de pesagem que não tinha valores, o
  preço especial do fornecedor não é aplicado.
- **Atalho "?" não abre a lista de atalhos** (T25): o hook não está montado.
- **"Reabrir Último Caixa?" em caixa antigo** (T9): a confirmação usa esse texto mesmo quando o caixa não é o último.
- **White Label pela metade** (T27): com o White Label ligado, a aba do navegador e o favicon continuam "EcoSistema".
- **Aviso de IBS/CBS não aparece** (T16): o aviso do topo da tela de notas não é renderizado.
- **"Observação" não grava na Produção** (T11).
- **Kardex com filtro de fornecedor mostra vendas** (T10): o filtro mantém as vendas na lista.
- **Folha marca "Falta" antes da admissão** (T19).
- **Recibo do pagamento do funcionário nunca abre** (T19).
- **Funcionário arquivado ainda bate ponto pelo link** (T19).
- **"Saldo: R$ 1500.00" sem formato** (T19): falta a máscara de moeda.
- **Aviso duplicado na tela de funcionários** (T19).
- **Cartão "Lucro Líquido" do Gerencial é vendas menos compras** (T22): o número não fecha com o resultado.
- **Comparativo do Gerencial usa as compras nos dois regimes** (T22): em competência devia usar o custo do vendido.
- **Matriz consegue "Corrigir saldo" do estoque da filial** (T22): conferir se a permissão é desejada.
- **Relatório do portal mostra o valor do pedido "sem valor"** (T20): a edge `entity-portal-report` soma o valor de todo
  pedido do período; o "sem valor" só esconde os números no Histórico, no comprovante e nas fotos.
- **Saldo do portal diferente da tela de Saldo** (T20): o portal desconta os movimentos de pedido "sem valor" dos últimos
  90 dias; com um pedido desses lançado no saldo, o parceiro vê um número e a empresa outro. Conferir se é desejado.
- **CRM: cartão barrado pela trava fica na coluna de destino** (T26): no erro, o quadro não volta ao estado certo; só
  recarregando a página.
- **CRM: automação vira linha sem texto no Histórico** (T26).
- **CRM: selo de tarefas abertas não atualiza depois do arraste** que dispara a automação (T26): só com outra mudança de
  tarefa ou depois de 30 s.
- **Foto nova no "Editar" do usuário só aparece ao reabrir a janela** (T2).
- **Limpar a busca do menu fecha as telas abertas** (T2).
- **Ticket "Sem valores" mostra preço na Pesagem avançada** (T8): a janela exibe Valor/Kg (R$ 6,20) e Valor estimado
  num ticket sem valores.
- **Aba nova de ticket mostra "#1" por uns 4 s** antes do número certo (#58) (T8).
- **"Rascunho encontrado" depois de salvar** (T4): o cadastro já salvo ainda oferece o rascunho ao abrir de novo.
- **Histórico de Envios do grupo não atualiza** depois do envio (T22) e, quando aparece, diz "Nenhum ativo".
- **"Sobrescrever" desligado não protege os preços da filial** (T22).
- **Setinha do Dashboard compara o período errado** (T22): 01 a 31/10 contra 31/08 a 30/09, não contra setembro.

## 2. Melhorias de uso
- **Produção diz "peça" em produto vendido por quilo** (T11).
- **Ticket só com a 1ª pesagem** (T8): ela vira o bruto e precisa ser digitada de novo na saída do caminhão.
- **Cancelar assinatura some sem permissão** (T0): para quem não tem permissão, o botão desaparece em vez de aparecer
  com cadeado (o usuário não sabe que a opção existe).
- **"Caixa" do Cato soma banco e saldo de parceiro** (T21): a resposta mistura o dinheiro do caixa com banco e saldos das
  sessões do dia; vale nomear melhor ou separar.
- **Peso da balança some no celular** (T5): o indicador não aparece em telas menores que 1024 px.
- **Trava de peso com o EcoTray fechado** (T5): com a trava ligada, não dá para digitar o peso nem em emergência.
- **Pix Automático já vem ligado** (T0): confirmar se é o padrão desejado.
- **Gráficos do Gerencial cortam nomes longos** (T22): a filial teve de se chamar "Filial Pindamonhangaba".
- **Portal diz "Portal do Cliente" também para fornecedor** (T20).
- **"Orientação para o time" só aparece na janela da etapa** (T26): nem o quadro nem o cartão do CRM mostram.
- **Busca "nota" mostra o bloco do Cato** (T2): o atalho de assistente aparece no meio dos resultados da busca.
- **Usuários em 1280x800** (T2): o painel de detalhe passa da borda da tela e o rodapé da janela de limite de usuários
  fica colado nela.
- **Compra e lista de tickets cortadas em 1280 px** (T8): com o menu lateral aberto, as duas telas passam da borda.
- **Ficha do cliente/fornecedor em 1280 px** (T4): as 7 abas não cabem na largura.
- **CEP sem máscara** no cadastro (T4).
- **Dica da lupa é só o `title` do navegador** (T4): demora a aparecer e não segue o estilo do app.
- **Plural errado no plano** (T0, 1.60.10): "10 módulo" e "4 pagamento realizado" no singular.
- **Player da EcoFlix**: os botões de 10 s não têm nome acessível (T0).
- **"Falar com o Sucesso do Cliente" só aparece em 4 dos 8 motivos** de cancelamento (T0).
- **Comprovante da pesagem avulsa diz "Fornecedor" e "Itens comprados"** (T8, 1.60.10): a avulsa é serviço prestado, não compra.
- **Editar a pesagem avulsa #60 mostra "#61"** no título (T8, 1.60.10).
- **Ticket "Com valores" não puxa o preço combinado** do fornecedor (T8, 1.60.10; ver também o item da tabela do fornecedor acima).
- **Barra "1 selecionado" da lista de tickets continua aparecendo em outras telas** (T8, 1.60.10).
- **Valor/Kg digitado direto na linha do pedido vira 0,0032** (T7, 1.60.10): a máscara do campo interpreta errado o que se digita.
- **Legenda de origem do preço fica "Preço informado" depois de voltar ao preço da tabela** (T7, 1.60.10).
- **Sem internet, o app redireciona para a Compra mesmo sem a tela ter sido visitada** (T7, 1.60.10).
- **Salvar do ticket gira até a rede voltar quando o computador perde a rede de vez** (T8, 1.60.10): com o cabo ou o wi-fi
  fora (navegador offline), o "Salvar Ticket de Pesagem" não conclui; só conclui offline quando o roteador segue ligado e é
  a internet que cai. `saveTicket` em `src/pages/WeighingTicket.tsx:1947` sem `networkMode: 'always'`. É o caso mais
  comum no pátio, e a tela promete que dá para salvar.
- **Cartão do White Label continua "Ativo" com o interruptor travado** por falta de logo (T27).
- **Ajuda do checklist das Coletas promete escolher o modelo por ordem**, e a janela da ordem não tem essa opção (T12).
- **"Confirmar no órgão" do MTR não mostra resultado na tela** (T18).
- **Sugestão de preenchimento nunca traz receita lançada direto no banco** (T13/T14, 1.60.8): a régua não considera esse tipo.

## 3. Textos desatualizados (Central de Ajuda, Guia de Instalação e a fonte da Trilha EcoFlix)
- **Guia de Instalação do EcoTray** ainda fala em arquivo ZIP (T5).
- **Central de Ajuda**: erra o nome do cadastro e diz que o cupom sem valor fica gravado (T7); diz que o pedido estornado
  sai da lista, mas ele continua (T9); chama o selo de outro nome (no app: "Comprovante sem valores", T9).
- **Fonte da trilha × app** (corrigir no `docs/ecoflix/trilha-de-tutoriais.md`):
  - T1: não existe aviso fixo de cadastro incompleto; a biometria não tem tela de cadastro; as opções de pedido da
    Usabilidade gravam por usuário.
  - T3: venda abaixo do custo pede confirmação, não bloqueia.
  - T4: telefone repetido dá "Mesmo telefone", não "Duplicado"; a ficha abre ao lado da lista, com 7 abas.
  - T6: o botão do aviso do cofre é "Usar disponível"; sem caixa aberto o gestor vê "Meu Caixa"; sem caixa, o saldo de
    parceiro só trava em dinheiro.
  - T10: não existe ação "em massa" entre materiais; o rótulo é "Todos os tempos".
  - T12: o Rastreamento já abre um mapa (a fonte diz "Em breve"); "Caçambas" agora é "Equipamentos"; o relatório conta a
    ordem sem data pelo dia em que foi criada.
  - T14: "Abra o caixa antes de realizar saques" não existe; o selo é "Casada"; o menu diz "Movimentações Financeiras".
  - T15: são cinco abas (há DFC); o botão do DRE é "Organizar categorias".
  - T16: "nome sem acento no XML" não confere no código.
  - T17: "Configurações do MDF-e" só tem série e número; o Relatório Fiscal virou aba do Estoque Fiscal; o sistema não
    envia nada ao contador (sai um ZIP).
  - T18: não existe status "recebido"; o cancelamento só vale para MTR emitido; o CDF é definitivo.
  - T21: o Cato só aparece com a liberação da empresa e a permissão de uso; o limite de 40 perguntas por dia está só na
    fonte.
  - T19: a pausa da jornada individual funciona diferente do que a fonte descreve.
  - T22: a volta da filial pelo mesmo código só dá para conferir no banco, não no código da tela.
  - T20: o pedido sem valor esconde os números no portal, menos no Relatório (bug acima); a aba "Preços" do fornecedor
    existe e a fonte não cita.
  - T26: todo funil criado em "Novo funil" também nasce com "Ganho" e "Perdido" com status (a fonte diz que só o padrão).
  - T25: a Agenda já não conta o fiado em dobro; o gráfico de 6 meses termina no fim do período do filtro; o
    Marketplace saiu da rotina semanal.
  - Ordem de gravação lista a T25 duas vezes; as pendências pulam do 9 para o 11.

## Achados no 1.60.18 (20/11)
- **T02 · Relatório por Usuário**: o "Salvar PDF" depende de CDN (sem ela, não gera o arquivo).
- **T03 · Editar Preços**: o filtro diz "Abaixo da compra" e o resumo diz "Venda abaixo da compra" (mesmo conceito, dois nomes).
- **T03 · Editar Preços**: a "Margem típica" do resumo mostra decimais soltos.
- **T04 · Clientes e Fornecedores**: o aviso "Informe o estado (UF) na aba Endereço" aponta para uma aba que se chama Dados Fiscais.
- **T06 · Caixa**: o balão do Cato cobre a coluna de ações do histórico; os gráficos do painel somem em dia sem movimento;
  o menu da linha abre só de passar o mouse (hover).
- **T06 · Caixa / EcoFlix**: o link do aviso de saldo insuficiente aponta para a aula 5.5 da EcoFlix antiga
  (`TUTORIAL_DINHEIRO_FISICO_URL`): trocar quando a trilha nova for publicada.
- **T09 · Pedidos**: peso "24.00 Kg" com ponto; o selo "Estornado" só explica no `title` nativo; trocar o fornecedor ao
  editar um pedido em dinheiro não abre "Atualizar os preços?"; textos "caixa de hoje" continuam em telas de outro dia.
- **T12 · Coletas**: "Cancelar ordem em vez disso" aparece na recusa de exclusão até em ordem concluída, que não pode ser cancelada.
- **T11 · Produção**: o gráfico do relatório diz "Total: N peças" fixo, mesmo em produto por quilo; ainda há "Custo
  estimado por peça" (ordem e Conversão) e "Custo/peça" (relatório) em produto por quilo.
- **T19 · RH**: a dica flutuante do Cato (15 s) cobre o lápis da jornada.
- **T07 (20/11)**: "Comprovante sem valores" não vale no "Visualizar PDF" logo depois de finalizar a venda (o ref do toggle é
  zerado na limpeza do formulário antes do `handlePrintReceipt`; `Sale.tsx` ~3813 e ~5071). Cupom 58 mm da compra com
  "Material não identificado" em TODO cupom de 58 mm (CONFIRMADO: o desvio do 58 mm em `thermalReceiptGenerator.ts` ~2738 passa os itens sem `formatThermalReceiptItems`). Faixa "Operações sincronizadas com sucesso!" some em ~0,3 s.
  Aviso de console `DialogContent requires a DialogTitle`. Handoff: `handoffs/2026-11-20_correcoes_T07.md`.
- **T02 (20/11)**: Relatório por Usuário mostra o peso sem formatação ("600.000", "38992.000"). No aviso de limite de usuários,
  "R$25,00" sem o espaço depois do R$. O balão de dica do Cato cobre o canto do Dashboard e da lista de usuários (nas gravações
  o gravador agora cala o balão; no app ele segue por cima do conteúdo).
- **T20 (20/11)**: em Clientes e Fornecedores, o menu da linha abre no hover e intercepta o clique em "Editar" (o robô passou a
  clicar por script). O relatório do portal do parceiro sai como HTML, não PDF.
- **T03 (21/11)**: a 1600 px de largura, a barra de seleção em massa de Materiais corta o botão "Excluir" e o X de fechar fica atrás do botão do Cato (com "Definir resíduo do MTR" a barra não cabe). Na aula a fala cita "Excluir" e ele mal aparece.
- **T06 (21/11)**: no Saque, o aviso diz "Diminuirá em R$ 3006,50" (sem ponto de milhar). Nova Receita por Pix avisa "Depósito realizado com sucesso!" (não é depósito). No Fechar Caixa do 1.60.22, a tabela comprado e vendido por material saiu da "Projeção de Lucro" para o "Relatório de Pedidos do Caixa" (a Projeção ficou só com a lista por material).
- **T12 (21/11)**: na ordem com checklist obrigatório sem resposta, o topo diz "0/1 obrigatórios", mas "Falta para concluir" só lista a assinatura. Nas listas da Frota, o menu "⋯" abre por hover e fica aberto quando o cursor só passa por cima (esconde o que está embaixo).
- **T18 (21/11)**: o `useCdf` checa a permissão de um jeito que barra o admin no CDF (a aula fala só de "quem não tem permissão").
- **T25 (21/11)**: a janela "Tarefas para hoje" não abre (1.60.18 e 1.60.22). O texto "Pressione Enter para abrir" sai quebrado por um `kbd` no meio. O "?" não abre a lista de atalhos. Na configuração do Dashboard ainda aparecem "Card Lucro" e "Evolução do Lucro".
- **T27 (21/11)**: com o White Label ligado e o logo removido, o cartão segue dizendo "Seu logo está sendo exibido". O campo "Nome Exibido" não é usado em lugar nenhum. Cor digitada sem "#" é salva com a mensagem de sucesso e nada muda.
- **T21 (21/11)**: "Ver itens e tributos" do Cato (`CatoFiscalDetails`) não é renderizado em lugar nenhum no 1.60.22 (componente órfão).
- **T26 (21/11)**: no 1.60.22 o chip da tarefa na Agenda deixou de ser botão; no kanban de tarefas, a área de soltar é só uma faixa de 80 px (difícil acertar o arrasto). Corrigidos no 1.60.22: achados 1, 2 e 6 da T26 e o histórico vazio.
- **T21 (21/11)**: no painel do Cato, clicar no campo de texto às vezes devolve o foco a um botão da tabela da resposta; "Próximos passos" nasce fechado; o rótulo do botão flutuante do Cato muda quando chega notificação; a pesquisa de fim de conversa depende da hora das mensagens. O botão "Preparar NF-e" já envia o pedido ao Cato (não só preenche o campo).
- **T04 (25/11)**: o "Exportar em PDF" do extrato detalhado do cliente abre uma aba que carrega o html2pdf do cdnjs no `<head>`; sem rede (ou com o CDN lento) a aba trava em branco. Embutir a biblioteca no bundle. Aviso "Select is changing from uncontrolled to controlled" no console (cap06, cadastro do cliente).
- **T10 (25/11)**: na Posição de estoque, depois do "Exportar em PDF" o diálogo do Exportar às vezes fica aberto por baixo e o menu do Excel não abre no clique seguinte (o robô precisou fechar o diálogo preso). Conferir se o diálogo fecha ao abrir a aba do PDF.
- **T11 (26/11)**: na Produção, o clique em "Ver matriz completa" levou ~6,7 s para responder na gravação. Conferir se a matriz demora assim também com dados reais.
- **T07 (26/11)**: (1) Offline: depois que a internet volta, a compra salva localmente leva ~6,6 s para sair de "Pendências de Sincronização"; um aviso de "sincronizando" ajudaria. (2) Venda com Estoque insuficiente: abrir a lista "Origem do estoque" e escolher "Esta unidade: Cobre misto" levou ~5,3 s para responder na gravação. (3) Pesagem avançada: o Peso bruto 316 aparece assim que se digita a 2ª pesagem (96), sem qualquer aviso de que ele é calculado (412 menos 96); vale um rótulo "calculado".
- **T01 (26/11)**: (1) No cupom térmico de um item com tara e "Mostrar só peso líquido" desligado, os títulos das colunas saem colados ("BRUTOLÍQUIDOPREÇO", sem espaço entre BRUTO, LÍQUIDO e PREÇO) e a tara não aparece em linha própria, só como a diferença entre Bruto e Líquido; a fala ("os cem quilos e a tara separada") promete a tara à parte. (2) No campo "Frase personalizada", digitar 68 caracteres levou ~5,8 a 6,7 s mesmo com o robô pedindo 40 caracteres por segundo (o campo re-renderiza a cada letra; o contador de caracteres acompanha). Na digitação do e-mail de contato (Informações de Contato) o tempo variou de 2,6 a 4,1 s entre duas gravações.
- **T05 (26/11, EcoTray 1.7.26)**: (1) `dashboard.py` (`_on_update_result`, ~379): o `ecotray.py` responde `check_update` na hora com `{"type":"update_check","status":"checking"}` e o painel trata essa primeira resposta como erro: "Atualizar Versão" deve mostrar "✗ Erro ao verificar" por instantes antes do "✓ Já atualizado" que chega pelo broadcast (deduzido do código, não visto no Windows). Falta um ramo `checking`. (2) Janela "Nova balança" (420x520): a frase de ajuda da correção ("Se 600 kg no sistema correspondem a 60 kg no indicador, use ÷10 (0,1×). Depois clique Aplicar e Gravar.") sai cortada na borda direita (wraplength 380 numa coluna de ~300 px) no render com a Montserrat; na aba Logs o botão "Atualizar" também fica cortado ("ualiz") na largura de 520. Conferir no Windows real. (3) Selo "EcoTray desatualizado (v..., atual é v...)": a versão da estação é lida só ao montar a tela (cache de 60 s); depois de o EcoTray se atualizar o aviso só some ao recarregar a página. (4) O `ecotray-falso.mjs` mandava `up_to_date` no `check_update`; o EcoTray de verdade manda `up-to-date` (hífen). Corrigido no falso.
- **T14 (26/11, 1.60.22)**: (1) "Exportar" em PDF no Extrato abre o relatório em outra aba, que o gravador não captura, então não há papel real para mostrar. (2) Os menus de lista (Categoria, Centro de custo, Frota) demoram: a opção Combustível levou ~1,8 s para abrir. (3) "Como funciona?" leva ~1,3 s para abrir. (4) Criar um cartão ou gerar um extrato leva 1 s ou mais sem indicação de progresso além de "Gerando...".
- **T13 (26/11)**: (1) o botão diz "Esta e as próximas", mas o aviso e o toast ainda dizem "futuras". (2) Conta com pagamento previsto "Boleto" ou "Cheque" abre a baixa em "Dinheiro" em vez da conta prevista (`PayBillModal.tsx` ~146-150). (3) "Esta e as próximas" numa parcela iguala o valor de todas as do escopo ao da parcela editada (`update_installment_bill_group`). (4) Na lista, o hover nas linhas e a rolagem até a última recorrência (abril) levam ~1,2 s por passeio; a baixa/abertura do diálogo "Opções do arquivo" do Exportar leva ~1,1 s depois do clique em PDF. (5) Os campos De/Até do filtro de vencimento são botões de data (sem `input`), então não dá para conferir o valor por leitura de campo; só o texto na tela.
- **T05 (26/11, gravação final, 1.60.22 / EcoTray 1.7.26)**: (1) O PDF do "Testar" (Integração com Impressora, `handleTestPrint` em `SettingsIntegrationsContent.tsx`, ~158) sai com 40 x 80 mm: `new jsPDF({ unit: 'mm', format: [paperWidthMm, 40] })` em retrato troca largura e altura quando a largura passa da altura, então a página fica com 40 mm de largura e o texto centrado em `paperWidthMm / 2` sai cortado no próprio PDF ("Teste de I", "Se você vê isso, e", "10/11/2026" sem a hora), em 80 mm e em 58 mm. Sugestão: `orientation: 'portrait'` com `format: [w, h]` em ordem de largura menor ou `orientation: 'l'` e conferir o PDF. (2) O "Testar impressão" do Ajustar Escala manda um comprovante de exemplo de 58 mm x 125 mm, inteiro (esse está certo). (3) EcoTray falso: o `ping` de 30 s do app continua respondendo `error`; na gravação final os cliques de impressão (cap04 aos ~17 s, cap05 aos ~47 s) não cruzaram o ping (26 + 30k s) e todas as impressões deram certo, mas o risco existe. (4) Em Usuários > Editar, o diálogo do "Peso dos pedidos" leva ~1 s por passo (abrir usuário, Editar, abrir a lista); o robô precisou de uma pausa de 3,2 s na fala do cap07.
- **T15 (27/11, 1.60.22)**: nenhum defeito novo nas 16 gravações finais (0 erros de página). (1) O PDF do Histórico (Exportar > Documento PDF > Exportar PDF) abre num popup com `#pdf-frame` cujo conteúdo é capturável por blob; a tela de opções ("Exportar Histórico (PDF)") leva ~1 s para abrir. (2) O gráfico do Dashboard (barras) só reage ao hover depois do carregamento completo; o primeiro hover logo após abrir leva ~1,3 s. (3) Ao reabrir o modal "Organizar categorias do DRE" a lista leva ~1 s para pintar os grupos.
- **T00 vertical (27/11, 1.60.22, celular 390x844)**: nenhum erro de página nas 18 gravações. (1) No celular o cabeçalho da Dashboard tem só a seta, o logo e o sino; a busca não existe (a aula fala "a busca e o sino" para os dois formatos). (2) Em "Configurações", as abas ficam cortadas na lateral ("ermissões", "Integraç") porque a faixa rola na horizontal sem sinal de que continua. (3) O aviso "Vamos para a próxima / Ficar nesta aula" da aula concluída se sobrepõe ao título da aula no celular ("Ficar nesta aula" por cima de "SUA CONTA E SUA EMPRESA"). (4) A tela de Assinatura e a janela de cancelar mostram valores e preços de plano (R$ 1.350,00, R$ 415,00) por natureza; nenhuma opção de ocultar para gravação. (5) O botão "Confirmar e começar a primeira aula" e os botões "Continuar"/"Voltar" do cancelamento ficam colados no pé da tela de 844 px; qualquer rolagem automática falha (a página já está no fim).

