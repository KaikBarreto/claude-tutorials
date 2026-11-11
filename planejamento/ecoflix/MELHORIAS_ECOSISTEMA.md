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
