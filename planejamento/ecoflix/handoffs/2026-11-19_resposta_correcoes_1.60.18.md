# Handoff de volta · correções do EcoSistema para a EcoFlix

Resposta ao handoff "correções do EcoSistema antes de gravar a EcoFlix".

**Versão publicada: 1.60.18** (commit `e8edc9e6d`, 19/11/2026), com changelog no pop-up e em `/atualizacoes`. Funções publicadas junto: `entity-portal-report` v72, `portal-order-receipt` v112, `entity-portal` v114, `time-clock-portal` v81. Migrations aplicadas: sugestão financeira, observação da produção, "Sobrescrever" e registro de atividade do pedido.

Como ler: **Tela** = conferido abrindo o sistema na conta de teste · **Leitura** = conferido só no código · **Banco** = aplicado em produção e conferido por consulta ou chamada real.

## 1. Ticket de Pesagem (T08)
- Salvar sem rede gira sem fim → **corrigido**. Tela: navegador offline, "Ticket OFF-01 guardado neste aparelho", subiu sozinho ao voltar a rede.
- "Sem valores" mostra preço na Pesagem avançada → **corrigido**. Tela.
- Aba nova mostra "#1" → **corrigido**. Tela: "#…" e depois o número certo.
- Comprovante da avulsa diz "Fornecedor"/"Itens comprados" → **corrigido**: "Cliente" e "Itens pesados"; com taxa lançada, tarja "SERVIÇO DE PESAGEM" e "Valor da pesagem". Tela: comprovante térmico real, com e sem taxa.
- Editar a avulsa #60 mostra "#61" → **corrigido**. Tela.
- Valorizar ignora a tabela/preço do fornecedor → **não existe mais** no código atual. Leitura.
- Barra "1 selecionado" em outras telas → **corrigido**. Tela.
- Ticket só com a 1ª pesagem → **corrigido**. Tela, inclusive em ticket salvo e reaberto.
- Lista de tickets cortada em 1280px → **não medido** (a tela de criação foi tratada; a LISTA não).
- Console `useDraftPresence` → **corrigido**. Leitura.
- NOVO: ligar "Com valores" com itens sem preço abre "Colocar os preços?"; salvar com item a R$ 0,00 pede confirmação. Tela.
- NOVO: aviso depois de salvar a avulsa mostra o valor cobrado; lista mostra "Serviço: R$ X". Tela.

## 2. Compra, Venda e pedidos (T07)
- Coluna "Peso Líquido" mostra o bruto → **corrigido**: "Peso" sem coluna de Tara, "Peso Bruto" com ela. Tela.
- Valor/Kg na linha vira 0,0032 → **corrigido**. Tela, digitando tecla a tecla.
- Legenda fica "Preço informado" → **corrigido**. Tela.
- Sem internet redireciona para a Compra → **não confirmado** (falta dizer em que situação).
- NOVO: aviso "Atualizar os preços?" só quando algum preço muda, item a item, sem mexer em preço digitado; campos da linha sem corte e com sublinhado; cartão Pesagem não é espremido; em tela estreita Tara/Desconto/Lucro vão para o expansível do item; total fora da bolha do assistente. Tela, de 1024 a 1920px.

## 3. Caixa e Financeiro
- "Reabrir Último Caixa?" → **corrigido**: "Reabrir caixa #N?". Leitura.
- Sugestão nunca traz receita do banco → **corrigido**. Banco.
- Central de Ajuda (estornado; nome do selo) → **corrigido**; ajuda e base do Cato regeradas.

## 4. Estoque e Produção
- Kardex com filtro de fornecedor mostra vendas → **corrigido**. Leitura.
- "Observação" não grava na Produção → **corrigido**. Banco.
- "peça" em produto por quilo → **corrigido**. Leitura.

## 5. Usuários, menu e configurações
- Limpar a busca fecha as telas abertas → **corrigido** (era a busca "Buscar tela ou ação…" do editor de permissões). Tela.
- Foto nova no Editar → **corrigido**. Leitura.
- "?" não abre os atalhos → **corrigido**. Tela.
- White Label pela metade → **corrigido**: aba e ícone da empresa; interruptor desliga sem logo. Leitura.
- Cancelar assinatura some sem permissão → **corrigido**: cadeado. Leitura.
- "Sucesso do Cliente" em 4 de 8 motivos → **corrigido**. Tela (motivo "Outro").
- Plurais do plano → **corrigido**. Tela.
- Busca "nota" mostra o bloco do Cato → **corrigido**. Tela.
- Usuários em 1280x800 → **não medido**.
- Player: botões de 10 s sem nome → **corrigido**. Leitura.
- Pix Automático ligado por padrão → **mantido** por decisão do Kaik.

## 6. Clientes, Fornecedores e Portal
- "Rascunho encontrado" depois de salvar → **corrigido**. Leitura.
- Relatório do portal soma pedido "sem valor" → **corrigido e publicado**. Banco: chamada real. Pedido estornado também sai.
- Saldo do portal ≠ tela de Saldo → **corrigido e publicado**. Banco: saldo do portal igual ao da tela em parceiro de teste. Junto, o valor do pedido "sem valor" deixou de sair pelo comprovante, pelos movimentos antigos e pela nota fiscal do portal (vazava antes). **Risco que resta:** quem souber o saldo de antes do pedido chega ao valor por subtração.
- "Portal do Cliente" para fornecedor → **corrigido**: "Portal do Fornecedor". Leitura.
- CEP sem máscara e dica da lupa → **corrigido**. Ficha com 7 abas em 1280px → **não medido**.

## 7. Fiscal e Ambiental
- Aviso de IBS/CBS não renderiza → **não volta**: removido de propósito na 1.54.21; componente órfão apagado e trilha ajustada.
- "Confirmar no órgão" do MTR sem resultado → **corrigido**. Leitura. O aviso de limite mensal de MTR/CDF voltou a disparar.

## 8. RH
- "Falta" antes da admissão → **corrigido**. Leitura + testes.
- Recibo do pagamento nunca abre → **corrigido**. Leitura.
- "Saldo: R$ 1500.00" → **corrigido**. Leitura.
- Arquivado bate ponto pelo link → **corrigido e publicado**. Banco: link de arquivado devolve "acesso desativado"; ativo responde normal. Foi junto a mudança de 01/10 (intervalo por dia), que estava no repositório e não no ar.
- Aviso duplicado → **não confirmado** (falta dizer qual aviso).

## 9. Gerencial / Filiais
- "Lucro Líquido" é vendas menos compras → **corrigido**: mesmo número da DRE, em competência. Tela.
- Setinha compara período errado → **corrigido**. Leitura.
- Comparativo usa compras nos dois regimes → **corrigido**: CMV por unidade em competência. Leitura.
- Histórico de Envios não atualiza / "Nenhum ativo" → **corrigido**. Leitura.
- "Sobrescrever" desligado não protege → **corrigido**: preço que a filial já tem não muda; zerado recebe o da matriz. Banco.
- Gráficos cortam nome longo → **corrigido**. Leitura.
- Matriz corrige saldo da filial → **mantido** por decisão do Kaik.

## 10. CRM e Coletas
- Cartão barrado fica na coluna de destino → **corrigido**. Leitura.
- Automação sem texto; selo de tarefas → **corrigido**. Leitura.
- "Orientação para o time" só na janela → **corrigido**: ícone no topo da coluna. Leitura.
- Ajuda do checklist → **corrigido** (texto).

## 11. EcoTray e balança
- Trava de peso com EcoTray fechado → **corrigido**: com a balança desconectada dá para liberar a digitação, com confirmação; o peso sai como manual e a liberação fica registrada em Compra e Venda. Leitura (sem balança real). No Ticket de pesagem a liberação funciona, mas não fica registrada.
- Peso some abaixo de 1024px → **fora deste lote** por decisão do Kaik.
- Guia fala em ZIP → **corrigido**. Leitura.

## 12. Cato
- "Caixa" soma banco e saldo de parceiro → **não confirmado** (falta a pergunta que reproduz).

## 13. Fonte da trilha
- `docs/ecoflix/trilha-de-tutoriais.md` corrigida ponto a ponto, cada um conferido no código; `/trilha-ecoflix` regerada. Ficou como estava: "nome sem acento no XML" da T16.

## Pendências conhecidas
- **Guia Técnico:** a checagem de impacto desta versão aponta 16 seções a revisar e prints a refazer (T0, T1, T4, T6, T7, T8, T11, T12, T14, T15, T16, T18, T19, T20, T22, T25). Textos de T7, T8 e T9 já atualizados; prints e PDF não (dependem dos prints originais).
- **Registro de atividade do pedido:** criado agora, enxuto. A migration antiga `20261116220000` (origem do preço nos itens) continua sem aplicar; a origem do preço ainda não é salva no pedido.
- **Conta de teste:** ficou a pesagem avulsa #105 (R$ 1,00, "QA tarja serviço"); o sistema só deixa excluir depois de estornar o financeiro.

## O que regravar
Aulas com mudança visível na tela: **T07, T08** (muita coisa), **T02** (permissões, atalho), **T00** (plano e cancelamento), **T04**, **T06/T09** (reabrir caixa, estornado), **T10**, **T11**, **T19**, **T20** (portal), **T22**, **T26**, **T05**, **T18**, **T27**.
