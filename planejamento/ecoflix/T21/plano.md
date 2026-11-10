# Plano · T21 · Cato, o assistente

- **Título:** Cato, o assistente (o da fonte). **Antes:** T15 "Relatório Financeiro e DRE". **Próximo:** T25 "Dashboard,
  Agenda e rotina".
- **Objetivo:** tirar dúvida simples perguntando em português: autorizar o Cato (administrador), usar as perguntas
  prontas, perguntar resultado do mês, quem está devendo, estoque e banco, entender gráfico × tabela, conferir o número
  na tela de origem, saber os limites e chegar ao atendente.
- **Áreas das vinhetas:** CATO · AUTORIZAÇÃO · PERGUNTAS · RESPOSTAS · LIMITES · AJUDA · RESUMO.
- **Alvo da fonte:** ~8 min. Desktop (janela 1280×800), logado como **Rafael Nogueira** (MASTER); um corte como **Marcos
  Antunes** (não administrador) no cap. 2. `FAKE_NOW=2026-11-10T08:30:00-03:00`. Todas as respostas do Cato são
  **simuladas** no backend falso (abaixo), com os números do mundo.
- Base: `T21/inventario.md` (código 1.59.154). O painel abre na tela "Estoque" (`/materiais`): ali as quatro perguntas
  prontas saem sem sorteio.

## Capítulos (os da fonte, na ordem)

| # | Vinheta (área / título) | O que se mostra | Ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (sem vinheta) | Abertura: tirar dúvida sem abrir relatório; o botão do Cato; cartão "Antes" | o problema | `inicio` |
| 1 | CATO / Onde o Cato fica | o botão redondo no canto inferior direito; no celular, à esquerda; o clique abre a autorização | computador × celular | `inicio` |
| 2 | AUTORIZAÇÃO / Autorizar o Cato | "Antes da primeira conversa com o Cato": os pontos; corte do Marcos ("Só o administrador..."); "Entendi e autorizo" → "Cato autorizado" | o caminho da pergunta | `inicio` → `apos-cap02` |
| 3 | PERGUNTAS / As perguntas prontas | "Oi, Rafael 👋", as quatro perguntas; R1 "Como tá indo meu negócio esse mês?"; as pílulas de sugestão | (só tela) | `apos-cap02` |
| 4 | PERGUNTAS / O que ele responde bem | R2 "Quem tá me devendo?" (barras), R3 estoque, R4 banco, R5 caixa; ⚠️ "caixa" = o de hoje | caixa do dia × mês | conversa do cap. 3 |
| 5 | RESPOSTAS / Gráfico ou tabela | R6 três meses (linha), R7 vendas por cliente em outubro (barras); ⚠️ saldo × valor movimentado; R8 estoque em tabela; a regra | saldo × movimentado; a regra dos gráficos | conversa do cap. 4 |
| 6 | RESPOSTAS / De onde vêm os números | "Consultei seu estoque", período e "Atualizado às"; "Abrir posição de estoque" → "Total geral" igual ao da resposta; "O Cato.ai pode cometer erros..." | o mesmo dado na tela e no Cato | conversa do cap. 5 |
| 7 | LIMITES / Os limites do Cato | R9 "Emite a nota da venda pra Fundição Bandeira do Vale" → orientação; ele consulta, você executa; ⚠️ limites de uso | consulta × executa; limites | conversa do cap. 6 |
| 8 | AJUDA / Avaliar e falar com o suporte | 👍 em R8; 👎 em R9 → "Faltou detalhe"; "Falar com atendente" → "Falar com o suporte" (sem enviar) | (só tela) | conversa do cap. 7 |
| 9 | RESUMO / Recapitulando | montagem; cartão "Próximo: Dashboard, Agenda e rotina" | | |

Transições faladas: 1 "Com o Cato liberado na conta da empresa"; 2 "Essa janela explica"; 3 "Com o Cato autorizado";
4 "Agora, as perguntas do dia a dia"; 5 "Pro mês, a pergunta é do mês"; 6 "Repara no que vem em cima de cada resposta";
7 "E o que ele não faz?"; 8 "Em cada resposta, tem o joinha".

**Cuidados (⚠️) com "Uma dica:"**: só o administrador autoriza (cap. 2, com a mensagem do Marcos na tela, que é o ponto,
e a saída logo depois); "caixa" é o caixa de hoje, mês se pergunta pelo mês (cap. 4); saldo × valor movimentado (cap. 5,
Fundição: deve R$ 14.370,00, comprou R$ 112.800,00 em outubro); limites de uso por minuto e por dia, a espera resolve
(cap. 7, ilustração; a mensagem de limite não é encenada).

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md`, com os números da junção (`MUNDO_LINHA_DO_TEMPO.md`): ferro misto 6.420 kg e ferro pesado 2.180 kg
(T10), cobre mel 42 kg e latão 214 kg (T7), o lote de alumínio que sai pra Minas na T17 e a chaparia da carga da T18 ainda no
pátio às 08:30; preço médio = preço de compra da tabela. A T21 herda a T13, a T14 e a T15 (as ações delas ficam antes das 08:30).

| Item | Valores (fictícios) | Onde aparece |
|---|---|---|
| Liberação do Cato | `companies.cato_enabled` = true; `ai_consent_at` vazio em `inicio`; `profiles.cato_invite_seen_at` preenchido (Rafael e Marcos) | caps. 1 e 2 |
| Marcos Antunes | com a permissão `action_use_cato` ("Usar o Cato (assistente de IA)"); não administrador | cap. 2 (corte) |
| Estoque em 10/11 08:30 (15 materiais, saldo × preço de compra = valor; × preço de venda = projeção) | Ferro pesado 2.180 kg · Ferro misto 6.420 · Chaparia 3.750 · Cobre mel 42 · Cobre misto 148 · Fio de cobre encapado 96 · Alumínio latinha 640 · Alumínio perfil 3.385 · Alumínio bloco 2.830 · Metal amarelo (latão) 214 · Bronze 38 · Inox 260 · Bateria automotiva 3.960 · Papelão 1.850 · Plástico PET 920. **Total 26.733 kg, valor R$ 96.076,00, projeção R$ 116.689,40** (sem o "Radiador de cobre", que só existe na T3) | R3, R8 e a tela "Posição de Estoque" (cap. 6: o "Total geral" tem de bater) |
| Novembro, 1 a 10 (regime de caixa, o padrão do `resumo_financeiro`) | vendas R$ 118.620,20 (Fundição Bandeira do Vale 57.460,00; Aços Quiririm 55.085,00; Serra Fina 4.815,20; Depósito Irmãos Siqueira 1.260,00); compras R$ 18.781,45; despesas R$ 32.234,10 (aluguel 6.800,00, folha 19.800,00, diesel 1.180,00 e as da T13 e da T14: pneu 180,00, energia 1.874,30, prensa 1.740,00, combustível 350,00, tarifas 64,90 e 6,50, água 238,40); resultado R$ 67.604,65 | R1, R6 |
| Saldos a receber | Fundição Bandeira do Vale R$ 14.370,00 (as 3 parcelas de R$ 4.790,00 do T13); Aços Quiririm Ltda R$ 2.870,00 (o saldo do T4 depois da baixa de R$ 2.000,00 da T13); Valdir Pereira R$ 300,00 (o vale do T4); total R$ 17.540,00 | R2 |
| Bancos | "Conta Principal" R$ 44.933,67 (o fim da T14); "Conta Secundária" R$ 82.515,00 (R$ 90.515,00 em 10/11 08:30, menos a transferência de R$ 8.000,00 da T14); "Conta Cooperativa" R$ 5.000,00 (T14); total R$ 132.448,67; novembro: entradas R$ 101.620,20 e saídas R$ 43.554,10, sem as transferências entre as contas e sem o saque para o cofre | R4 |
| Caixa de hoje | nenhum caixa aberto em 10/11 até 08:30 (a T6 abre o #85 às 08:31); ontem, 09/11: o #83 do Marcos fechou com R$ 640,00 e o #84 do Rafael com R$ 1.250,00 | R5 |
| Meses | setembro: compras R$ 201.784,25, vendas R$ 273.047,73 (regra do gerador: 93 % de outubro e a descarga de setembro; conferir na semente); outubro (T15): compras R$ 256.860,00, vendas R$ 269.240,00, por cliente Fundição 112.800,00, Aços Quiririm 77.460,60, Serra Fina 60.349,20 e Depósito Irmãos Siqueira 18.630,20; novembro até o dia 10: compras R$ 18.781,45, vendas R$ 118.620,20 | R6, R7 |

Só o estoque é conferido na tela nesta aula (cap. 6); os demais números aparecem nas respostas simuladas e saem da linha
do tempo da junção (`MUNDO_LINHA_DO_TEMPO.md`), que o gerador do mundo confere. Se a semente der outros valores, trocar nas
respostas e nas falas dos caps. 3 a 6.

## Gravação
- **Rotas:** `/materiais` (o painel abre aqui), `/materiais/posicao-estoque` (pelo botão "Abrir posição de estoque").
- **Simular no backend falso:**
  - edge `cato-background` (POST da pergunta) → `{ "jobId": "<uuid>" }`; a resposta é escolhida pelo texto exato da
    pergunta (R1 a R9 abaixo);
  - tabela `cato_jobs`: o job nasce `pending` e vira `completed` ~3 s depois, com o `response_payload` (a tela consulta a
    cada 1 s e mostra "Pensando…", "Buscando seus dados…");
  - edge `cato-assist` com `mode: "followups"` → `{ "suggestions": [...] }` (as 3 de cada resposta);
  - RPCs `accept_ai_terms(p_version)` (grava `companies.ai_consent_at` e `ai_consent_version` '2.0'),
    `set_cato_feedback`, `cato_memory_manage('status')` → `{ "enabled": false, "epoch": 0, "sharedEnabled": false,
    "sharedEpoch": 0, "canManage": true, "preferenceRetentionDays": 90, "topicRetentionDays": 30 }`;
  - `updatedAt` de cada `context` = a hora do relógio falso no momento da resposta (a fala não cita a hora).
- **Sequência:** caps. 3 a 8 são uma conversa só. Gravar em sequência no mesmo navegador; para regravar um capítulo, o
  `setup` restaura a conversa pelo `sessionStorage` (`cato-conversation-v3:<empresa>:<usuário>`) com as respostas
  anteriores. Cap. 2 tem um corte com outro usuário (Marcos), antes do aceite.
- **Não clicar:** "Falar no WhatsApp" (abre o WhatsApp do suporte com dados da empresa), "Ouvir resposta", o
  microfone, "Memória" e "Conversas". O convite do beta não aparece (semente).
- **Ilustrações** (desenho no estilo da marca, nunca tela do app): caps. 0, 1, 2, 4, 5 (duas), 6 e 7 (duas).

### Respostas simuladas (formato do `response_payload`, `hooks/useCato.tsx:32-46`)
Todas com `interactionId` (uuid novo), `cacheHit: false`, sem `images`, `action` nem `budgetNotice`. `context.period`
em AAAA-MM-DD. O texto usa só o markdown que o painel desenha (negrito, listas). O campo `followups` abaixo **não** vai
no `response_payload`: é o que a edge `cato-assist` (`mode: "followups"`) devolve em `suggestions` depois da resposta.

R1 · "Como tá indo meu negócio esse mês?" (pergunta pronta)
```json
{"toolsUsed":["resumo_financeiro"],"context":{"period":{"start":"2026-11-01","end":"2026-11-10","timezone":"America/Sao_Paulo"},"regime":"caixa","updatedAt":"<agora>"},
 "answer":"Novembro começou no azul. Olhando seus lançamentos de 1 a 10 de novembro:\n\n- **Vendas:** R$ 118.620,20\n- **Compras:** R$ 18.781,45\n- **Despesas:** R$ 32.234,10\n\nO resultado até aqui é de **R$ 67.604,65**, no regime de caixa. A Fundição Bandeira do Vale foi o maior cliente do período, com R$ 57.460,00 em vendas. Ainda faltam 20 dias pro mês fechar.",
 "followups":["Compara com outubro","Quais despesas tive esse mês?","Qual material mais vendi?"]}
```
R2 · "Quem tá me devendo?"
```json
{"toolsUsed":["saldos_parceiros"],"context":{"updatedAt":"<agora>"},
 "answer":"Hoje, **3 parceiros** têm saldo a seu favor, somando **R$ 17.540,00**:\n\n1. **Fundição Bandeira do Vale:** R$ 14.370,00\n2. **Aços Quiririm Ltda:** R$ 2.870,00\n3. **Valdir Pereira:** R$ 300,00\n\nA Fundição concentra 82% do que você tem a receber.",
 "chart":{"type":"barra","title":"Saldo a receber por parceiro","valueFormat":"currency","points":[{"label":"Fundição Bandeira do Vale","value":14370},{"label":"Aços Quiririm Ltda","value":2870},{"label":"Valdir Pereira","value":300}]},
 "followups":["Pra quem eu tô devendo?","Quais contas vencem essa semana?","Quanto a Fundição me pagou em outubro?"]}
```
R3 · "Quanto tenho em estoque agora?"
```json
{"toolsUsed":["estoque_atual"],"context":{"period":{"start":"2026-11-10","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Agora você tem **26.733 kg** de material no pátio. A custo médio, esse estoque vale **R$ 96.076,00**; pela tabela de venda, a projeção é de **R$ 116.689,40**.\n\nOs materiais que mais pesam no valor:\n\n1. **Alumínio perfil:** 3.385 kg, R$ 30.126,50\n2. **Alumínio bloco:** 2.830 kg, R$ 20.093,00\n3. **Bateria automotiva:** 3.960 kg, R$ 12.276,00\n\nSó o alumínio perfil e o bloco já passam da metade do valor do estoque.",
 "followups":["Lista meu estoque em tabela","Quanto vale meu alumínio?","O que está parado há mais tempo?"]}
```
R4 · "Qual o saldo das minhas contas no banco?"
```json
{"toolsUsed":["resumo_bancario"],"context":{"period":{"start":"2026-11-01","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Agora, suas contas no banco somam **R$ 132.448,67**:\n\n- **Conta Principal:** R$ 44.933,67\n- **Conta Secundária:** R$ 82.515,00\n- **Conta Cooperativa:** R$ 5.000,00\n\nEsse é o saldo de agora. Em novembro, até hoje, entraram **R$ 101.620,20** e saíram **R$ 43.554,10** nas contas, sem contar as transferências entre elas.",
 "followups":["Quais pagamentos saíram do banco esse mês?","Quanto tenho no cofre?","Compara as entradas com outubro"]}
```
R5 · "Como tá meu caixa hoje?"
```json
{"toolsUsed":["caixa"],"context":{"period":{"start":"2026-11-10","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Hoje ainda **não tem caixa aberto**: ninguém abriu o caixa até agora. Ontem, dia 9, foram dois: o do Marcos Antunes fechou com **R$ 640,00** e o do Rafael Nogueira com **R$ 1.250,00**.",
 "followups":["Quanto tenho no cofre?","Quanto comprei ontem?","Mostra os caixas da semana"]}
```
R6 · "Compras e vendas dos últimos três meses"
```json
{"toolsUsed":["compras_vendas_mensais"],"context":{"period":{"start":"2026-09-01","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Olhando suas compras e vendas dos últimos três meses:\n\n- **Setembro:** comprou R$ 201.784,25 e vendeu R$ 273.047,73\n- **Outubro:** comprou R$ 256.860,00 e vendeu R$ 269.240,00\n- **Novembro (até o dia 10):** comprou R$ 18.781,45 e vendeu R$ 118.620,20\n\nEm outubro, as compras quase alcançaram as vendas: o pátio encheu de ferro pesado. Em novembro, esse ferro saiu, e as vendas passaram longe das compras.",
 "chart":{"type":"linha","title":"Compras e vendas por mês","valueFormat":"currency","series":[{"name":"Compras","points":[{"label":"set/26","value":201784.25},{"label":"out/26","value":256860},{"label":"nov/26","value":18781.45}]},{"name":"Vendas","points":[{"label":"set/26","value":273047.73},{"label":"out/26","value":269240},{"label":"nov/26","value":118620.2}]}]},
 "followups":["Qual foi meu resultado em outubro?","Por que outubro teve tanta compra?","Compara com agosto"]}
```
R7 · "Pra quem eu mais vendi em outubro?" (`top_parceiros` não tem rótulo "Consultei...")
```json
{"toolsUsed":["top_parceiros"],"context":{"period":{"start":"2026-10-01","end":"2026-10-31"},"updatedAt":"<agora>"},
 "answer":"Em outubro, olhando suas vendas, quem mais comprou de você foi:\n\n1. **Fundição Bandeira do Vale:** R$ 112.800,00\n2. **Aços Quiririm Ltda:** R$ 77.460,60\n3. **Serra Fina Alumínio Reciclagem:** R$ 60.349,20\n\nA Fundição ficou com 42% das vendas do mês.",
 "chart":{"type":"barra","title":"Vendas por cliente em outubro","valueFormat":"currency","points":[{"label":"Fundição Bandeira do Vale","value":112800},{"label":"Aços Quiririm Ltda","value":77460.6},{"label":"Serra Fina Alumínio Reciclagem","value":60349.2}]},
 "followups":["Quanto a Fundição me deve?","Qual material mais vendi em outubro?","Compara com setembro"]}
```
R8 · "Lista meu estoque em tabela"
```json
{"toolsUsed":["estoque_atual"],"context":{"period":{"start":"2026-11-10","end":"2026-11-10"},"updatedAt":"<agora>"},
 "answer":"Aqui está o seu estoque de agora, do maior valor para o menor. São **15 materiais**, somando **26.733 kg** e **R$ 96.076,00** a custo médio.",
 "table":{"title":"Estoque em 10/11/2026","columns":["Material","Quantidade (kg)","Valor em estoque"],"rows":[["Alumínio perfil",3385,30126.5],["Alumínio bloco",2830,20093],["Bateria automotiva",3960,12276],["Metal amarelo (latão)",214,5885],["Cobre misto",148,5328],["Ferro misto",6420,4815],["Alumínio latinha",640,3968],["Chaparia",3750,2625],["Ferro pesado",2180,2071],["Cobre mel",42,1785],["Plástico PET",920,1748],["Fio de cobre encapado",96,1728],["Inox",260,1508],["Bronze",38,1102],["Papelão",1850,1017.5]]},
 "followups":["Quanto vale meu estoque pela tabela de venda?","Me mostra num gráfico","O que está parado há mais tempo?"]}
```
R9 · "Emite a nota da venda pra Fundição Bandeira do Vale" (pedido fora do que ele faz: vira orientação; caminho
conferido no código: menu "Fiscal & Ambiental" › "Notas Fiscais (NF-e)", aba "Saída", botão "Nova Nota")
```json
{"toolsUsed":["consultar_ajuda"],"context":null,
 "answer":"Emitir nota fica com você: eu consulto e explico, mas não emito. O caminho é este:\n\n1. Abra **Fiscal & Ambiental › Notas Fiscais (NF-e)**.\n2. Na aba **Saída**, clique em **Nova Nota**.\n3. Monte a nota da venda pra Fundição Bandeira do Vale, confira e emita.\n\nA tributação da nota quem define é o seu contador.",
 "followups":["Onde vejo as notas emitidas?","Como cancelar uma nota?","Como emitir nota de entrada?"]}
```

## Riscos e decisões para o Kaik
1. **Respostas simuladas:** texto e números escritos aqui, no formato real do painel; o Cato real responderia com outras
   palavras. Proposta: deixar assim (nada de IA de verdade na gravação).
2. **Reajuste de preço:** a 1.59.154 deixa o Cato propor reajuste de preço da tabela padrão num cartão que a pessoa
   confirma. A fonte diz que ele só consulta; a fala diz "emitir nota, pagar conta e cadastrar seguem com você" e não
   mostra o reajuste. Mostrar?
3. **Liberação:** o Cato só aparece com a liberação da empresa e a permissão de uso; a fala diz "com o Cato liberado na
   conta da empresa".
4. **Limites:** a fala não diz números (no código: 20 por minuto por usuário, 40 por minuto por empresa, 300 por dia por
   empresa e 40 por dia por usuário, ajustáveis no servidor).
