# Handoff · correções do EcoSistema antes de gravar a EcoFlix

Levantado na produção dos tutoriais (leitura do código, ensaios e gravações com dados fictícios). Versões vistas: 1.59.154 a
1.60.10. **Não reconferido na 1.60.15**: antes de corrigir cada item, confirme que ele ainda existe. Cada item traz a aula (T)
em que apareceu, que é onde o defeito ficaria visível no vídeo.

Como ler: **A** = aparece na tela durante a aula ou a fala teria de contornar (corrigir antes de gravar); **B** = defeito real,
mas a aula consegue desviar; **C** = acabamento.

## 1. Ticket de Pesagem (T08, já gravada como piloto)
- **A · Salvar do ticket gira sem fim com o computador sem rede.** Com o navegador offline (cabo ou wi-fi fora), o "Salvar
  Ticket de Pesagem" não conclui; só conclui quando o roteador segue ligado e é a internet que cai. `saveTicket` em
  `src/pages/WeighingTicket.tsx` (perto da linha 1947 na 1.60.10) sem `networkMode: 'always'`. A tela promete que salva.
- **A · Ticket "Sem valores" mostra preço na Pesagem avançada**: a janela exibe Valor/Kg (R$ 6,20) e Valor estimado.
- **A · Aba nova de ticket mostra "#1" por uns 4 s** antes do número certo (#58).
- **A · Comprovante da pesagem avulsa diz "Fornecedor" e "Itens comprados"**: a avulsa é serviço prestado, não compra.
- **A · Editar a pesagem avulsa #60 mostra "#61" no título.**
- **B · Valorizar ticket sem valores ignora a tabela/preço especial do fornecedor**; e o ticket "Com valores" não puxa o
  preço combinado do fornecedor.
- **B · Barra "1 selecionado" da lista de tickets continua aparecendo em outras telas.**
- **B · Ticket só com a 1ª pesagem**: ela vira o bruto e precisa ser digitada de novo na saída do caminhão.
- **C · Lista de tickets e Compra cortadas em 1280 px** com o menu lateral aberto.
- **C · Console**: `[useDraftPresence] realtime CHANNEL_ERROR/TIMED_OUT em company_drafts` repetido na tela do ticket.

## 2. Compra, Venda e pedidos (T07)
- **A · Coluna "Peso Líquido" exibe o peso bruto** na compra e na venda.
- **A · Valor/Kg digitado direto na linha do pedido vira 0,0032**: a máscara interpreta errado o que se digita.
- **B · Legenda de origem do preço fica "Preço informado"** depois de voltar ao preço da tabela.
- **B · Sem internet, o app redireciona para a Compra** mesmo sem a tela ter sido visitada.

## 3. Caixa e Financeiro (T06, T09, T13, T14)
- **B · "Reabrir Último Caixa?"** aparece também quando o caixa não é o último (T09).
- **B · Sugestão de preenchimento nunca traz receita lançada direto no banco** (T13/T14).
- **C · Central de Ajuda**: diz que o pedido estornado sai da lista (continua); chama o selo "Comprovante sem valores" de outro nome.

## 4. Estoque e Produção (T10, T11)
- **A · Kardex com filtro de fornecedor mostra vendas** (T10).
- **A · "Observação" não grava na Produção** (T11).
- **C · Produção diz "peça"** em produto vendido por quilo (T11).

## 5. Usuários, menu e configurações (T00, T02, T25, T27)
- **A · Limpar a busca do menu fecha as telas abertas** (T02).
- **A · Foto nova no "Editar" do usuário só aparece ao reabrir a janela** (T02). (A foto na criação foi corrigida na 1.60.10;
  conferir se a tela inicial e o perfil rápido escolhidos na criação também gravam.)
- **B · Atalho "?" não abre a lista de atalhos**: o hook não está montado (T25).
- **B · White Label pela metade**: aba do navegador e favicon continuam "EcoSistema"; o cartão segue "Ativo" com o interruptor
  travado por falta de logo (T27).
- **B · Cancelar assinatura some para quem não tem permissão** (em vez de aparecer com cadeado) (T00).
- **B · "Falar com o Sucesso do Cliente" só aparece em 4 dos 8 motivos** de cancelamento (T00).
- **C · Plural errado no plano**: "10 módulo", "4 pagamento realizado" (T00).
- **C · Busca "nota" mostra o bloco do Cato** no meio dos resultados (T02).
- **C · Usuários em 1280x800**: painel de detalhe passa da borda; rodapé da janela de limite colado nela (T02).
- **C · Player da EcoFlix**: botões de 10 s sem nome acessível (T00).
- **Conferir · Pix Automático já vem ligado** (T00): é o padrão desejado?

## 6. Clientes e Fornecedores, Portal (T04, T20)
- **A · "Rascunho encontrado" depois de salvar**: o cadastro já salvo ainda oferece o rascunho (T04).
- **A · Relatório do portal mostra o valor do pedido "sem valor"**: a edge `entity-portal-report` soma todo pedido do período (T20).
- **B · Saldo do portal diferente da tela de Saldo** quando há pedido "sem valor" lançado no saldo (T20). Conferir se é desejado.
- **C · Portal diz "Portal do Cliente" também para fornecedor** (T20).
- **C · CEP sem máscara; ficha com 7 abas não cabe em 1280 px; dica da lupa é só o `title` do navegador** (T04).

## 7. Fiscal e Ambiental (T16, T17, T18)
- **A · Aviso de IBS/CBS do topo da tela de notas não é renderizado** (T16).
- **B · "Confirmar no órgão" do MTR não mostra resultado na tela** (T18).

## 8. RH (T19)
- **A · Folha marca "Falta" antes da admissão.**
- **A · Recibo do pagamento do funcionário nunca abre.**
- **A · "Saldo: R$ 1500.00"** sem máscara de moeda.
- **B · Funcionário arquivado ainda bate ponto pelo link.**
- **C · Aviso duplicado na tela de funcionários.**

## 9. Gerencial / Filiais (T22)
- **A · Cartão "Lucro Líquido" é vendas menos compras**: não fecha com o resultado.
- **A · Setinha do Dashboard compara o período errado**: 01 a 31/10 contra 31/08 a 30/09.
- **B · Comparativo usa as compras nos dois regimes** (em competência devia usar o custo do vendido).
- **B · Histórico de Envios do grupo não atualiza** depois do envio e, quando aparece, diz "Nenhum ativo".
- **B · "Sobrescrever" desligado não protege os preços da filial.**
- **C · Gráficos cortam nomes longos de filial.**
- **Conferir · Matriz consegue "Corrigir saldo" do estoque da filial.**

## 10. CRM e Coletas (T12, T26)
- **A · Cartão barrado pela trava fica na coluna de destino** até recarregar a página (T26).
- **B · Automação vira linha sem texto no Histórico**; selo de tarefas abertas não atualiza depois do arraste (T26).
- **C · "Orientação para o time" só aparece na janela da etapa** (T26).
- **C · Ajuda do checklist das Coletas promete escolher o modelo por ordem**, e a janela da ordem não tem essa opção (T12).

## 11. EcoTray e balança (T05)
- **B · Trava de peso com o EcoTray fechado**: não dá para digitar o peso nem em emergência.
- **C · Peso da balança some em telas menores que 1024 px.**
- **C · Guia de Instalação ainda fala em arquivo ZIP.**

## 12. Cato (T21)
- **B · "Caixa" do Cato soma banco e saldo de parceiro**: nomear melhor ou separar.

## 13. Fonte da trilha × app (`docs/ecoflix/trilha-de-tutoriais.md`)
Não são bugs: é a fonte que está desatualizada. Os roteiros já seguem o app; corrigir a fonte evita voltar ao erro.
- T01: não existe aviso fixo de cadastro incompleto; biometria não tem tela de cadastro; opções de pedido da Usabilidade gravam por usuário.
- T03: venda abaixo do custo pede confirmação, não bloqueia.
- T04: telefone repetido dá "Mesmo telefone"; a ficha abre ao lado da lista, com 7 abas.
- T06: botão do aviso do cofre é "Usar disponível"; sem caixa aberto o gestor vê "Meu Caixa".
- T07 (Ajuda): erra o nome do cadastro e diz que o cupom sem valor fica gravado.
- T10: não existe ação "em massa" entre materiais; o rótulo é "Todos os tempos".
- T12: o Rastreamento já abre um mapa; "Caçambas" agora é "Equipamentos".
- T14: "Abra o caixa antes de realizar saques" não existe; o selo é "Casada"; o menu diz "Movimentações Financeiras".
- T15: são cinco abas (há DFC); o botão do DRE é "Organizar categorias".
- T16: "nome sem acento no XML" não confere no código.
- T17: "Configurações do MDF-e" só tem série e número; o sistema não envia nada ao contador (sai um ZIP).
- T18: não existe status "recebido"; cancelamento só vale para MTR emitido; o CDF é definitivo.
- T19: a pausa da jornada individual funciona diferente do descrito.
- T20: a aba "Preços" do fornecedor existe e a fonte não cita.
- T21: o Cato só aparece com a liberação da empresa e a permissão; o limite de 40 perguntas por dia só está na fonte.
- T25: a Agenda já não conta o fiado em dobro; o Marketplace saiu da rotina semanal.
- T26: todo funil novo nasce com "Ganho" e "Perdido".
- Ordem de gravação lista a T25 duas vezes; as pendências pulam do 9 para o 11.

## Depois das correções
Me avise a versão publicada: eu atualizo o build de gravação, rodo a varredura das 26 aulas contra ela e regravo só o que mudou.
