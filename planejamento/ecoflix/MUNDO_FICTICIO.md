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
- **Produção** (T11): produto "Fardo de alumínio" (da latinha, custo médio da latinha R$ 6,20); ficha do Cobre mel com
  as ordens #1 e #2 (a #2 em dobro, excluída no cap13); tolerância 2 %, meta 250; FAKE_NOW 17:30 do cap07 da T11 em
  diante.
- **Ajudantes do pátio** (T11, valem para a T19): Cláudio Ferraz e Diego Morais.
- **Outubro calibrado** (T15, conferir no centavo no ensaio): Ferro pesado com 50 t compradas e 10 t vendidas no mês; DRE
  de outubro +R$ 6.500 em competência e −R$ 31.500 em caixa; a diferença de R$ 38.000 é o ferro parado no pátio.
  Categorias e centros de custo "Coleta" e "Pátio". Energia de R$ 3.850 lançada em dobro **só a partir do estado da T15**
  (excluída no cap10; a T14 não vê a duplicata). Fiado da Fundição Bandeira do Vale.
- **Compra e venda** (T7): caixa aberto com R$ 2.500; bateria a R$ 3,40 para a Auto Peças Vale Forte; 214 kg de latão
  (Metal amarelo) e 42 kg de Cobre mel no estoque; Valdir Pereira sem CPF nem endereço; o carroceiro "Zé Moreira" é
  cadastrado na tela da T7. Uma balança só no EcoTray.
- **Saldos dos parceiros** (T4; sinal na convenção do app): Aços Quiririm +4.870; Serra Fina Alumínio −1.500; Cooperativa
  Recomeço +2.550; Valdir Pereira −300; Depósito Irmãos Siqueira −840. **Valdir**: os R$ 300 são um vale que a Recicla
  adiantou a ele (ele desconta na próxima entrega de material). 14 compras da Cooperativa no histórico. A T4 cadastra
  pela busca de CNPJ a "Serralheria Bem-Te-Vi" (número em branco, campo em vermelho) e tenta "Cida Ramos" com o telefone
  da Aparecida (o app avisa "Mesmo telefone").
- **Fiscal** (T16): cota em níveis de 100 e 300 documentos; série 1 com a última nota 1248; transportadora e cenário
  fiscal cadastrados (o cenário do exemplo usa CST 51, sem recomendação: quem define é o contador); venda de 500 kg
  líquidos de Cobre mel; caixa de 09/11 fechado; duas notas recebidas; XML da Cooperativa Recomeço para importar. Na aula:
  cancelar a 1249, carta de correção da placa, inutilizar 1246 e 1247 (tudo simulado).
- **Bancos** (T13, T14): "Conta Principal" e "Conta Secundária" (nunca "Conta Reserva"); uma "Poupança antiga" zerada,
  para arquivar na T14; categorias "Combustível" e "Tarifas bancárias". Extrato OFX fictício de 17 linhas, de 01/11 a
  10/11, casando com os Pix da T13 e com o que a T14 cria (tabela no `T14/plano.md`). "Tornar principal" só é mostrado,
  sem clicar (a conta padrão não muda na trilha).
- **Contas a pagar e receber** (T13): fornecedor novo "Hidráulica Moretti" (CNPJ válido, cadastrado na T13); contas
  bancárias sem logo de banco; fiado da Aços Quiririm R$ 3.150,00; venda parcelada da Fundição Bandeira do Vale em 3x
  R$ 4.790,00; centros de custo e categorias do `T13/plano.md`. **Conferir na junção**: saldos da T4 × fiados da T13 ×
  números da T15 contam a mesma história.
- **Coletas** (T12): ordens 1 a 8; frota com tara (CPF e CNH dos motoristas gerados); equipamentos (o app chama
  "Equipamentos", não "Caçambas") 01 a 05 e 40 bags; o portal da Cooperativa Recomeço abre numa segunda janela sem login
  (o robô concede a geolocalização).
- **Estoque** (T10; valores no `T10/plano.md`): Ferro misto 6.420 kg; Ferro pesado 2.180 kg em 10/11 (ajuste de −14 kg em
  31/10, exclusão de 180 kg, compra de 860 kg no Pix com 2 fotos); Cobre mel e Bateria automotiva com movimento em
  outubro; a "Tabela Depósitos" da T3. **Conflito com a T15 a resolver na junção**: a T15 deixa 40 t de Ferro pesado no
  pátio no fim de outubro. Proposta: as 40 t estão na posição de 31/10 (o T10 mostra isso na posição por data) e uma
  venda grande à Aços Quiririm no começo de novembro deixa os 2.180 kg de hoje.
- **Cato** (T21): estoque de 15 materiais somando R$ 52.112,25 (conferido na tela de Posição); respostas simuladas R1 a R9
  no `T21/plano.md`; um corte logado como Marcos.
- **Transporte e serviço** (T17): Serra Fina Alumínio Reciclagem fica em Itamonte, MG (a carga sai de Taubaté e atravessa
  o RJ por Resende: pede MDF-e); duas NF-e de hoje somando R$ 55.380,00 e 5.800 kg; outubro com 12 notas de saída e 9 de
  entrada, saldo R$ 71.625,00 (pode ser dito na fala: é dado do mundo); Metal amarelo com 600 kg de diferença entre o
  estoque fiscal e o operacional. As NF-e da T17 seguem a numeração da T16 (conferir na junção).
- **Ambiental** (T18): acesso do Rafael ao SIGOR com o CPF fictício 274.913.508-79; resíduo "Sucata de ferro" em TON,
  código 19 12 02 (metais ferrosos) e Classe II B no exemplo (a fala diz que quem classifica é o responsável técnico);
  NF-e de 3.600 kg de chaparia para a Aços Quiririm; dois MTR (um cancelado) e um CDF de outubro da Auto Peças Vale
  Forte; a carga vai no GHT7B19 com o Jair Lopes (o FKD2E41 está na viagem da T17).
- **EcoTray** (T5): impressora térmica POS-58 (58 mm); "Balança do pátio" na COM3; pesos de 18,6 e 312 kg; duas
  impressoras no cap10; `ecotray_version` 1.7.22; chaves gravadas por usuário (Rafael). Sem trecho de celular (o indicador
  de peso não aparece em tela menor que 1024 px).
- **Ticket de Pesagem** (T8): próximo ticket 58; caminhão da Cooperativa Recomeço com 9.460 kg na entrada e 6.380 kg na
  saída, 2 % de impureza (3.018,4 kg de Alumínio latinha a R$ 6,20 = R$ 18.714,08, pago por Pix); rascunho do Jair Lopes
  (Auto Peças Vale Forte); pesos digitados (a balança rodoviária fica fora do EcoTray).
