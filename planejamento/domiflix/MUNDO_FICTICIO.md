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

## O que o T4 criou (`seeds-extra/t4/apos-cap14.json` = estado inicial do T5)
Cadeia de sementes de cada capítulo: base + `t3/apos-cap10` + `t1/apos-cap13` (identidade da empresa, White Label
desligado) + `t4/inicio` + `t4/apos-capMM`. O T4 parte sem tipo de serviço, categoria, tipo de tarefa nem checklist
(nem a base nem o T3 os trazem); usuários continuam os da base. Não mexe em clientes, equipamentos nem financeiro.
- **Categorias de serviço**: **Instalação** (azul), **Manutenção** e **Higienização** (as duas na cor padrão, cinza:
  a fala só deu tempo de um ciclo completo com cor).
- **Tipos de serviço (6)**, todos ativos e vinculados a equipamento, menos a Visita Técnica:
  **Manutenção Preventiva** (MP, verde, Manutenção, R$ 180, "Limpeza e conferência completa do aparelho e teste",
  fiscal 14.01.01 / município 001 / ISS 5%; criado ao vivo no cap. 3, fiscal no cap. 5, descrição editada no cap. 6);
  e, de bastidor (REST no backend falso durante o cap. 3), **Manutenção Corretiva** (MC, laranja, Manutenção, R$ 220),
  **Instalação de Split** (INS, azul, Instalação, R$ 650, fiscal 14.06.01 / 001 / ISS 5%), **Higienização de Split**
  (HIG, ciano, Higienização, R$ 180), **Carga de Gás** (GAS, roxo, Manutenção, R$ 350) e **Visita Técnica** (VT, cinza,
  sem categoria, R$ 120, sem equipamento).
- **Tipos de tarefa (4)**: **Reunião** (roxo, criado ao vivo no cap. 7) e, de bastidor, **Treinamento da equipe** (azul),
  **Entrega de material** (laranja) e **Compra de peças** (amarelo).
- **Checklists (2)**: **Manutenção preventiva de split** (do catálogo, 13 perguntas, vinculado a Manutenção Preventiva) e
  **Higienização de split** (do zero, vinculado a Higienização de Split, 6 perguntas na ordem final: Estado da serpentina
  [Conformidade], Filtros lavados? [Verdadeiro/Falso + foto], Aspecto da água retirada [Seleção: Limpa, Turva, Suja],
  Dreno escoando [Vídeo], e, de bastidor, Observações [Texto] e Assinatura do cliente [Assinatura]).
- Handler novo `nfse-tax-codes` (lista de códigos de serviço da LC 116 do app, para a aba Fiscal do cap. 5).

## O que o T5 criou (`seeds-extra/t5/apos-cap15.json` e as sementes por capítulo = estado inicial do T7)
OS nova #22 (a do capítulo de abertura de OS), recorrência, agenda com tarefas (`seeds-extra/t5/tarefas-agenda.json`),
equipe **Equipe Alfa** (cor #3B82F6, ícone de capacete), 6 avaliações de atendimento (NPS) e os chamados do portal.
Detalhes nos `apos-capNN.json` e no relatório do T5 em `PRODUCAO.md`.

## O que o T12 criou (`seeds-extra/t12/apos-cap11.json` = estado inicial do T13)
Parte de `t12/inicio` (fim do T11 reconstruído sobre `t5/apos-cap05`; trilha Domiflix com `is_onboarding false`). Criado ao vivo: a OS #34 "Pendente"
(origem Portal do Cliente, sem data, Cassete 36.000 BTUs - Restaurante do hotel: "O ar do restaurante está pingando água perto da janela."); a seção
"Cobranças" em "Oculto" no Portal do Contrato do hotel; documentos do PMOC do hotel "Liberado" no portal. A OS #15 da Mariana Lopes (T5) segue na fila de
chamados (o Dashboard avisa "2 chamados"; aulas seguintes que abrirem o Dashboard passam a marca `dominex:portal-tickets-seen:<id da Camila>` no `storage`).
Senha do portal: nenhuma (hotel e colégio sem senha). Links: `https://www.dominex.app/portal/<token>` e `/contrato/unidade/pmoc-hotel-mirante-do-mar-k7m2q9x4wb3d`.

## Próximas aulas
Cada `<Tnn>/plano.md` → "Mundo fictício" diz o que precisa existir no começo e o que a aula cria. Ao produzir,
gravar o estado final em `seeds-extra/<id>/apos-capNN.json` e atualizar esta página.
