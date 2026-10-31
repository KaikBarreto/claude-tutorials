# Mundo fictício da trilha Domiflix (continuidade entre aulas)

Toda aula começa no estado em que a anterior terminou (ordem de exibição). Nada real: nomes, documentos (com dígito
verificador válido), e-mails `.example`, telefones de faixa fictícia. Fonte das sementes:
`ferramentas/rec/fakebase/seeds/` (base) + `seeds-extra/<id>/apos-capNN.json` (o que cada capítulo criou).

## Base (sementes `gen-01-tenant` e `gen-02-cadastros`)
- **Empresa**: Glacial Cold Brasil (climatização), e-mail contato@glacialcold.example, plano Master.
- **Módulos ligados**: basic, rh, crm, contracts, nfe, pricing_advanced, customer_portal, white_label,
  video_questions, whatsapp, cobrancas, finance_advanced, pdv (tudo ligado: as aulas mostram os 🔒 avisando que
  dependem do plano).
- **Usuários**: Camila Duarte (admin, quem grava as aulas de gestão); técnicos Rafael Lima, Bruno Alves, Júlia Santos,
  Lucas Ferreira, Marina Costa e Paulo Souza (`@glacialcold.example`).
- **Clientes (12)**: Padaria Bom Grão, Hotel Mirante do Mar, Mercado Vila Nova, Academia Ponto Forte, Restaurante
  Sabor da Serra, Clínica Sorriso Leve, Escritório Lemos & Prado, Farmácia Vida Plena, Pousada Brisa do Mar,
  Condomínio Jardim Azul, Mariana Lopes, Roberto Nunes; 10 contatos (ex.: Dona Neide Barros).
- **Origens**: Indicação, Instagram, Google, WhatsApp. **Fornecedores (4)**: Polar Distribuidora de Peças, Gelo Norte
  Componentes, Cobre Sul Suprimentos, Distribuidora Aurora de Peças.
- **Equipamentos (25)**: Hi-Wall 9.000/12.000/18.000 BTUs, Cassete 36.000 BTUs etc.; categorias Split Hi-Wall,
  Split Cassete, Split Piso-Teto; campos Marca, Modelo, Nº de Série, Capacidade/Especificação, Local, Data de Instalação.
- **Financeiro, o que o cadastro da empresa cria** (`supabase/functions/self-register/index.ts:997-1037`,
  `create-company/index.ts:503-541`): contas **Caixa** (tipo caixa) e **Conta Principal** (banco), saldo inicial 0;
  14 categorias padrão (Serviços Prestados, Vendas de Peças/Materiais, Contratos PMOC, Impostos e Taxas, Custo de
  Materiais, Fornecedores e Insumos, Alimentação, Luz/Energia, Aluguel, Combustível/Transporte, Salários e Encargos,
  Marketing e Publicidade, Ferramentas e Equipamentos, Outros) mais as 14 do sistema (gatilho
  `seed_system_financial_categories`, `20261020223000_...sql:18-45`: Vendas de Serviços, CSP - Materiais, Tarifas e
  Taxas...). Nome de categoria é único na empresa (`20260919190000_...sql`): a aula escolhe "Aluguel" na lista, não cria.
  Ainda fora das sementes do backend falso: entram na base antes da primeira aula que abre o Financeiro (T8/T9).

## O que o T3 criou (`seeds-extra/t3/apos-cap10.json` = estado inicial do T4)
- Clientes: **Colégio Monte Verde** (PJ, CNPJ 91.847.200/0001-30), **Marcos Antônio Braga** (PF), **Luana Martins**
  (veio pelo formulário de captação), **Pousada Sol Nascente** (criado rápido no cadastro de equipamento).
- Contato **Antônio Ferreira** (zelador do Colégio). Origem nova **Site**. Formulário **Cadastro de novos clientes**.
- Fornecedor **Ventura Gás e Tubos**.
- Equipamentos **Hi-Wall 18.000 BTUs - Sala dos professores** (Colégio Monte Verde, marca Aerovento) e
  **Cassete 36.000 BTUs - Recepção** (Pousada Sol Nascente); categoria **Multi Split**; campo **Tensão**
  (127 V, 220 V, 380 V); tarefa "Trocar as pilhas do controle"; anexo no equipamento.

## Próximas aulas
Cada `<Tnn>/plano.md` → "Mundo fictício" diz o que precisa existir no começo e o que a aula cria. Ao produzir,
gravar o estado final em `seeds-extra/<id>/apos-capNN.json` e atualizar esta página.
