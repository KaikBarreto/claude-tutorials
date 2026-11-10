# Mundo fictício da EcoFlix · Recicla Vale Metais

Proposta de 08/11/2026 (o nome vem da fonte; o resto daqui). Uma empresa só para a trilha inteira, como a Glacial Cold
Brasil na Domiflix: dá continuidade de uma aula para outra. Tudo fictício: CPF e CNPJ com dígito verificador válido
gerados na semente, e-mails `.example`, telefones (12) 9 0000-xxxx, placas Mercosul inventadas. Nenhum dado de cliente
real. Na semente, conferir que nenhum nome de parceiro é de empresa real da região.

Se o app pedir um dado que não está aqui, inventar no mesmo estilo e anotar neste arquivo.

## Data do mundo
`FAKE_NOW=2026-11-10T08:30:00-03:00` (terça). Histórico fechado de agosto a outubro de 2026 (o "dia 31" do T10 é
31/10, um sábado); novembro só com os primeiros dias.

## Empresa
- **Recicla Vale Metais Ltda** ("Recicla Vale Metais"), ferro-velho em Taubaté, SP (Vale do Paraíba).
- Regime do exemplo fiscal: **Lucro Real** (Kaik, 10/11: o padrão de muita reciclagem).
- Matriz em Taubaté; filial em Pindamonhangaba, SP (só no T22).
- Assinatura ativa com todos os módulos da trilha (plano Personalizado), para todas as telas existirem.
- Cofre (Conta Dinheiro) com R$ 18.500,00; uma conta bancária principal e uma secundária.

## Pessoas da empresa
| Pessoa | Papel | Existe a partir de |
|---|---|---|
| Rafael Nogueira | dono, administrador MASTER (o usuário logado) | sempre |
| Juliana Prado | escritório: financeiro e notas | T2 (criada na tela) |
| Marcos Antunes | balanceiro e operador de caixa, sem ver lucro | T2 (criado na tela) |
RH (T19): os três e mais quatro do pátio (dois ajudantes, um motorista, um operador de empilhadeira).

## Materiais (R$ por kg: compra / venda)
| Grupo | Material | Compra | Venda | NCM (sugestão) |
|---|---|---|---|---|
| Ferrosos | Ferro pesado | 0,95 | 1,25 | 7204.49.00 |
| Ferrosos | Ferro misto | 0,75 | 1,05 | 7204.49.00 |
| Ferrosos | Chaparia | 0,70 | 0,98 | 7204.49.00 |
| Cobre | Cobre mel | 42,50 | 47,90 | 7404.00.00 |
| Cobre | Cobre misto | 36,00 | 41,50 | 7404.00.00 |
| Cobre | Fio de cobre encapado | 18,00 | 22,00 | 7404.00.00 |
| Alumínio | Alumínio latinha | 6,20 | 7,40 | 7602.00.00 |
| Alumínio | Alumínio perfil | 8,90 | 10,40 | 7602.00.00 |
| Alumínio | Alumínio bloco | 7,10 | 8,50 | 7602.00.00 |
| Metais | Metal amarelo (latão) | 27,50 | 31,90 | 7404.00.00 |
| Metais | Bronze | 29,00 | 33,50 | 7404.00.00 |
| Metais | Inox | 5,80 | 7,20 | 7204.21.00 |
| Outros | Bateria automotiva | 3,10 | 3,90 | 8549.11.00 |
| Outros | Papelão | 0,55 | 0,80 | 4707.10.00 |
| Outros | Plástico PET | 1,90 | 2,60 | 3915.90.00 |
O T3 cria na tela um material fora da lista (ex.: "Radiador de cobre") e uma tabela de preço ("Tabela Depósitos").

## Parceiros (cliente = para quem a empresa vende; fornecedor = de quem ela compra)
| Nome | Tipo | Papel | Para que serve na trilha |
|---|---|---|---|
| Valdir Pereira | PF | fornecedor (carroceiro) | "Não possui telefone"; adiantamento a favor dele |
| Aparecida Ramos ("Dona Cida") | PF | fornecedora (catadora) | latinha e papelão, quase todo dia |
| Depósito Irmãos Siqueira | PJ | fornecedor **e** cliente | saldo unificado (T4) |
| Auto Peças Vale Forte | PJ | fornecedor | radiador, bateria, sucata de oficina |
| Cooperativa Recomeço | PJ | fornecedora | latinha e PET em volume |
| Aços Quiririm Ltda | PJ | cliente | ferro e chaparia; tabela de preço própria |
| Fundição Bandeira do Vale | PJ | cliente | cobre, latão e bronze; fiado parcelado |
| Serra Fina Alumínio Reciclagem | PJ | cliente | alumínio |

## Veículos (T8, T12, T17)
| Placa | Veículo | Motorista |
|---|---|---|
| FKD2E41 | Caminhão truck | Edson Moura |
| GHT7B19 | Caminhão 3/4 | Jair Lopes |
| EZR4C63 | Picape | Tiago Freitas |

## Histórico (agosto a outubro)
Compras quase todo dia dos fornecedores, vendas semanais aos três clientes, despesas fixas (energia, aluguel, folha,
combustível, tarifa bancária), contas a pagar e a receber abertas em novembro, um fiado parcelado, um ticket de
pesagem aguardando valorização e um caixa por operador por dia. Números do exemplo do pátio do T15 (comprou muito e
vendeu pouco num mês) cabem num dos meses.

## Decidido pelas aulas (consolidado pelo coordenador; as aulas não editam este arquivo)
- **Identidade** (T1): CNPJ 47.318.506/0001-07; Rua das Oficinas, 1250, CEP 12086-410, Taubaté, SP; logo
  `recicla-vale-logo` e ícone `recicla-vale-icone.png` (1:1) fictícios, os dois enviados no T1 (cap05); frase do
  comprovante e condição de pagamento 30/60/90 (T1).
- **Usuários** (T2): plano com `max_users` 3 (a empresa fecha a T2 em 3/3; a janela do limite mostra o preço do usuário
  extra como está, a fala não diz o valor); e-mails `@reciclavalemetais.example`; Marcos "Operador Padrão" sem "Ver
  Projeção de Lucro", tela inicial "Caixa", foto desenhada; Juliana com 7 telas e 8 ações.
- **White Label** (T27): só na T27 (cor #1F5FAD); o mundo base das outras aulas fica com o White Label desligado.
- **Materiais** (T3): códigos 1 a 15 na ordem da tabela acima; até o cap06 da T3 o cobre está R$ 0,50 abaixo (a aula
  corrige); bronze a R$ 30,50 para o Depósito Irmãos Siqueira; a T3 cria "Radiador de cobre" (código 70, 110 kg), soma
  8 kg ao Ferro misto e cria a "Tabela Depósitos" (+4 %), ligada ao Depósito Irmãos Siqueira (vale na compra e na venda,
  como o código faz).
- **Permissões do Marcos**: as do T2 (perfil "Operador Padrão" sem "Ver Projeção de Lucro"); as aulas seguintes não
  mudam isso.
