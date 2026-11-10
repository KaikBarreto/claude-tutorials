# Plano · T12 Coletas e Logística

- **Título:** Coletas e Logística (o da fonte). 🔒 módulo **Coletas** (`coletas`); o pedido pelo portal depende também
  do **Portal do Cliente** (`portal_cliente`). A fala diz que depende do plano contratado, sem preço.
- **Objetivo:** sair do pátio e ir buscar o material: criar e agendar a ordem, escalar motorista e caminhão, acompanhar
  até concluir (com a troca de caçamba), aprovar o pedido que chega pelo portal, cadastrar frota e caçambas, ler o
  relatório e ajustar as regras.
- **Antes:** T4 "Clientes, fornecedores e a ficha do parceiro". **Próximo:** T11 "Produção" (fonte: "transformar o que
  entrou no pátio em produto de maior valor").
- **Vinhetas (áreas):** COLETAS · ORDENS · AGENDA · ACOMPANHAMENTO · PORTAL · FROTA · EQUIPAMENTOS · RELATÓRIO ·
  CONFIGURAÇÕES · RESUMO.
- **Alvo da fonte:** ~15 min. Estimativa: 1.712 palavras de fala (~11 min de voz) + vinhetas, cartela, a troca de janela
  do portal e as esperas dos formulários ≈ 13 min.
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` (terça). Desktop, Rafael Nogueira (MASTER); no cap07, uma segunda janela sem
  login com o portal da Cooperativa Recomeço.
- **Fora da aula (fonte):** "Rastreamento" e "Rotas". A fala não cita nem promete nada; a câmera não para nesses itens do
  menu. Na 1.59.154 o Rastreamento já abre um mapa (relatório ao Kaik).

## Capítulos (os da fonte, na ordem)

| # | Vinheta (área / título) | O que a tela mostra | ⚠️, 🔒 e ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (abertura) | Dashboard → "Coletas & Logística" → "Ordens de Coleta". | 🔒 dito; [ILUSTRAÇÃO: coleta no papel e no grupo de mensagens] | `inicio` |
| 1 | COLETAS / O que o módulo resolve | O quadro, sem ação; o caminho de uma coleta. | ⚠️ ordem de coleta não é pedido (explicado) + [ILUSTRAÇÃO: o caminho da coleta e a compra à parte] | `inicio` |
| 2 | ORDENS / O quadro das ordens | Colunas "Solicitada", "Agendada", "A caminho", "Concluídas", "Cancelada"; cartões #8 e #7 ("Sem cadastro"); "Quadro"/"Lista"; "Nova ordem". | ⚠️ só anda para a frente; cancelada e concluída ficam como registro (dica) | `inicio` |
| 3 | ORDENS / Criar uma ordem | "Nova ordem" → etapa "Parceiro" (Auto Peças Vale Forte, endereço do cadastro) → "Coleta": "Material estimado" e "Observações". | menção ao "Sem cadastro" | `inicio` |
| 4 | AGENDA / Data e janela | Mesma janela, etapa "Coleta": "Data agendada" 12/11/2026, "Período" ("Manhã", "Tarde", "Dia todo") → "Manhã". | | `inicio` + `setup` reabre a janela na etapa 2 |
| 5 | AGENDA / Motorista e veículo | Etapa "Frota": "Jair Lopes" e "GHT7B19", "Revisão", "Criar ordem"; o cartão #9 em "Agendada". | | `inicio` + `setup` reabre na etapa 3 |
| 6 | ACOMPANHAMENTO / Até concluir | #8: "A caminho" → "Preencher" → "Recolhi" Caçamba 03 e "Entreguei" Caçamba 05 → "Concluir coleta" → "Voltar às ordens" → detalhe com "Equipamentos movimentados" e "Histórico". | ⚠️ concluir não cria compra (dica) | `apos-cap05` |
| 7 | PORTAL / A coleta pedida pelo portal | Portal da Cooperativa Recomeço → "Coletas" → "Solicitar coleta" (PET prensado, 800 kg, 13/11, "Tarde") → no sistema: ponto vermelho, cartão #10 "via portal" → "Aprovar" → "Agendar coleta" → "Agendar". | 🔒 portal dito; [ILUSTRAÇÃO: os dois lados do pedido] | `apos-cap06` |
| 8 | FROTA / Veículos e motoristas | "Frota" → "Veículos": detalhe do FKD2E41; "Novo veículo" FVL8A52 poliguindaste (tara 7.100, capacidade 8.500) → "Motoristas": "Novo motorista" Rogério Batista (CNH C). | [ILUSTRAÇÃO: tara, bruto e líquido] | `apos-cap07` |
| 9 | EQUIPAMENTOS / As caçambas e onde estão | "Equipamentos": "Tipos de equipamento" (uma a uma × por quantidade), "Unidades identificáveis", "Nova unidade" Caçamba 06 → "Movimentar" de "Externo" para "Minha base"; "Onde tudo está agora"; aba "Movimentações" com "Ordem 8". | ⚠️ caçamba só muda de lugar quando alguém registra (dica, ajustada ao código) + [ILUSTRAÇÃO: o caminho da caçamba] | `apos-cap08` |
| 10 | RELATÓRIO / O relatório das coletas | "Relatório": "Este mês" e "Mês passado"; totais, "Taxa de conclusão", "Por status", "Por motorista", "Por veículo", "Por parceiro". | ⚠️ cancelada sai da taxa (dica) + [ILUSTRAÇÃO: a conta da taxa]; ⚠️ em que dia cada coleta entra (dica, pelo código) | `apos-cap09` |
| 11 | CONFIGURAÇÕES / As regras das coletas | "Prefixo da numeração" "COL-", "Janelas de coleta oferecidas", "Exigir motorista e veículo para agendar", "Exigir aprovação da solicitação", "Antecedência mínima (horas)" 24, "Dias aceitos para coleta". | ⚠️ regras do portal não travam o operador (dica) + [ILUSTRAÇÃO: as regras só na porta do portal] | `apos-cap10` |
| 12 | RESUMO / Recapitulando | Montagem; cartão "Próximo". | | (montagem) |

Transições faladas: 0→1 "Antes de clicar, o que o módulo resolve"; 1→2 "Agora, o quadro"; 2→3 "A Auto Peças Vale Forte
ligou: vamos criar a ordem"; 3→4 "Agora, o dia e o período"; 4→5 "Falta quem vai buscar"; 5→6 "O caminhão saiu";
6→7 "E quando o próprio parceiro pede?"; 7→8 "Quem faz tudo isso é a frota"; 8→9 "E as caçambas"; 9→10 "No fim do mês,
o relatório"; 10→11 "Por último, as regras"; 11→12 "Recapitulando".

## Falas dos cuidados ⚠️ e 🚫 (fonte → aula, conferido no código)
| Da fonte | Na 1.59.154 | Onde e como |
|---|---|---|
| Ordem de coleta não é pedido; concluir não cria pedido | igual (a conclusão grava status, histórico e equipamentos) | cap01 explicado com ilustração; cap06 "Uma dica:" |
| Não dá para pular etapa nem voltar ("Transição inválida...") | igual | cap02 "Uma dica:", sem encenar o erro |
| Cancelada ou concluída não volta; cria nova | igual | cap02, junto da dica acima |
| Caçamba é manual; concluir não devolve para "Disponível" | **mudou**: não há mais "Disponível"; a posição vem das movimentações, registradas no "Entreguei/Recolhi" da ordem (valem ao concluir) ou no "Movimentar" | cap09 "Uma dica:": a caçamba só muda de lugar quando alguém registra |
| Relatório conta pela data agendada; ordem sem data não aparece | **mudou**: entra pela conclusão, senão pelo agendamento, senão pelo dia em que foi criada | cap10 "Uma dica:" pelo código |
| Taxa = concluídas ÷ (total − canceladas) | igual | cap10 "Uma dica:" + ilustração |
| Regras do portal não travam o operador | igual (a criação interna não confere antecedência nem dia) | cap11 "Uma dica:" + ilustração |
| 🚫 Rastreamento e Rotas "Em breve" | Rotas igual; **Rastreamento já tem mapa** | fora da aula (pedido do Kaik); relatório |

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (proposta; conferir na semente que nenhum nome novo é de empresa real):
- **Módulos** `coletas` e `portal_cliente` ativos. `collection_settings` nos padrões do código (sem prefixo; as três
  janelas; sem exigir frota; com aprovação; antecedência 0; segunda a sábado; aviso ligado; sem checklist nem assinatura).
- **Frota** (os veículos do MUNDO, com os dados que o detalhe mostra):
  | Placa | Descrição | Tipo de rodado | Tara | Capacidade | Motorista (CPF · CNH · categoria · validade) |
  |---|---|---|---|---|---|
  | FKD2E41 | Caminhão truck | Truck | 9.200 kg | 14.000 kg | Edson Moura (284.559.130-61 · 73190528479 · E · 22/03/2029) |
  | GHT7B19 | Caminhão 3/4 | Toco | 3.900 kg | 4.000 kg | Jair Lopes (917.362.048-31 · 56204719334 · C · 09/09/2028) |
  | EZR4C63 | Picape | Utilitário | 1.750 kg | 1.000 kg | Tiago Freitas (650.193.827-95 · 31864057226 · B · 14/01/2031) |
  Todos com "UF de licenciamento" SP e "Tipo" "Veículo único". (Alinhar com o T8 e o T17, que também usam a frota.)
- **Equipamentos:** tipo "Caçamba 5 m³" (uma a uma; unidades "Caçamba 01" a "Caçamba 05", condição OK) e tipo "Bag 1 m³"
  (por quantidade, 40). Movimentações: 01/08/2026 "Externo" → "Minha base" (as 5 caçambas e os 40 bags); 23/10 (ordem 5)
  "Minha base" → Cooperativa Recomeço, 10 bags; 27/10 (ordem 6) "Minha base" → Depósito Irmãos Siqueira, Caçamba 03.
- **Ordens de coleta** (com os eventos do histórico):
  | Nº | Parceiro | Situação em 10/11 08:30 | Data · janela | Motorista · placa | Material estimado |
  |---|---|---|---|---|---|
  | 1 | Cooperativa Recomeço | Concluída 02/10 | 02/10 · Manhã | Tiago Freitas · EZR4C63 | ~500 kg de latinha |
  | 2 | Auto Peças Vale Forte | Concluída 09/10 | 09/10 · Tarde | Jair Lopes · GHT7B19 | ~350 kg de radiadores |
  | 3 | Depósito Irmãos Siqueira | Concluída 16/10 | 16/10 · Dia todo | Edson Moura · FKD2E41 | ~3 t de ferro misto |
  | 4 | Auto Peças Vale Forte | Cancelada 20/10 (motivo "Material ainda não separado") | 21/10 · Manhã | Jair Lopes · GHT7B19 | ~200 kg de baterias |
  | 5 | Cooperativa Recomeço | Concluída 23/10 (Entreguei 10 bags) | 23/10 · Tarde | Tiago Freitas · EZR4C63 | ~700 kg de PET |
  | 6 | Depósito Irmãos Siqueira | Concluída 27/10 (Entreguei Caçamba 03) | 27/10 · Manhã | Edson Moura · FKD2E41 | Entrega de caçamba |
  | 7 | Marcelo Tavares ("Sem cadastro", (12) 9 0000-5821, Rua das Paineiras, 215, Taubaté/SP) | A caminho desde 08:10 | 10/11 · Manhã | Tiago Freitas · EZR4C63 | ~300 kg de ferro de demolição |
  | 8 | Depósito Irmãos Siqueira | Agendada (criada em 05/11) | 10/11 · Manhã | Edson Moura · FKD2E41 | Troca da Caçamba 03: ferro misto, ~2 t |
  O endereço de cada parceiro cadastrado é o do cadastro (T4). Próximo número: 9.
- **Portal:** link do portal da Cooperativa Recomeço (o do T20), aba "Coletas" sem senha, "solicitar coleta" ligado.
- **Esta aula cria:** a ordem 9 (Auto Peças Vale Forte, 12/11 · Manhã, Jair Lopes · GHT7B19, "~400 kg de radiadores e
  baterias", observação "Retirar pelo portão lateral"); a conclusão da 8 (Recolhi Caçamba 03, Entreguei Caçamba 05); a
  ordem 10 pelo portal (Cooperativa Recomeço, "PET prensado — 800 kg", 13/11 · Tarde), aprovada e agendada; o veículo
  FVL8A52 "Caminhão poliguindaste" (Toco, SP, tara 7.100 kg, capacidade 8.500 kg); o motorista Rogério Batista (CPF
  463.718.205-08, (12) 9 0000-4417, CNH 04581273671, categoria C, validade 18/06/2030); a unidade "Caçamba 06" (OK, de
  "Externo" para "Minha base" em 10/11); as configurações prefixo "COL-" e antecedência de 24 h. Atualizar o
  `MUNDO_FICTICIO.md`.

## Gravação
- **Rotas:** `/dashboard` (cap00), `/coletas/ordens`, `/coletas/ordem/<id da 8>` (tela da ordem e o relatório),
  `/coletas/frota`, `/coletas/equipamentos`, `/coletas/relatorio`, `/coletas/configuracoes`; **página pública**
  `/portal/<token da Cooperativa Recomeço>` numa segunda janela, sem login (cap07).
- **RPCs, tabelas e edges a simular:** `get_next_collection_order_number`; `change_collection_order_status` (status,
  `completed_at`, evento em `collection_order_events`, frota, data e janela, e as linhas de equipamento que viram
  `collection_equipment_movements` com `collection_order_id`); `collection_equipment_positions` (posição calculada pelas
  movimentações); `register_collection_equipment_movement`; `collection_orders`, `collection_settings` (upsert),
  `collection_equipment_types`, `collection_containers`, `drivers`, `vehicles`, `suppliers`, `customers`; edges
  `collection-report` (relatório da ordem concluída, "Relatório de Coleta 8"), `entity-portal` (dados do portal e a aba
  Coletas) e `collection-request` (cria a 10 como "solicitada"); `user_notifications` (aviso da solicitação).
- **Geolocalização:** na tela da ordem o navegador pede a posição; o robô concede a permissão com uma coordenada fictícia
  perto do endereço do Depósito Irmãos Siqueira, e o backend falso aceita o insert em `collection_driver_locations` (sem
  isso o histórico ganharia a nota "Localização não registrada: ..."). A fala não comenta.
- **Datas:** os campos de data desta seção são nativos (`input type="date"`): o robô digita.
- **Ilustrações** (cenas HTML no estilo da marca, `docs/09-aula-ilustrada.md`): cap00 o problema; cap01 o caminho da
  coleta e a compra à parte; cap07 os dois lados do pedido; cap08 tara, bruto e líquido; cap09 o caminho da caçamba;
  cap10 a conta da taxa de conclusão; cap11 as regras só na porta do portal.
- Nada de mapa nem de rastreamento na tela; a câmera não para em "Rastreamento" e "Rotas" no menu.
