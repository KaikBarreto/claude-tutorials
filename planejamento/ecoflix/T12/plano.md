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
- **Alvo da fonte:** ~15 min. Estimativa: 2.943 palavras de fala (~19 min de voz) + vinhetas, cartela, a troca de janela
  do portal e as esperas dos formulários ≈ 13 min.
- **FAKE_NOW:** `2026-11-10T07:00:00-03:00` (terça; junção: a troca da caçamba é antes da balança do T8, 08:40, e da viagem do T17, 09:40). Desktop, Rafael Nogueira (MASTER); no cap07, uma segunda janela sem
  login com o portal da Cooperativa Recomeço.
- **Fora da aula (fonte):** "Rastreamento" e "Rotas". A fala não cita nem promete nada; a câmera não para nesses itens do
  menu. Na 1.59.154 o Rastreamento já abre um mapa (relatório ao Kaik).

## Capítulos (18, renumerados no 1.60.18)

Novos: 2 a 8 reabertos e ampliados (Lista, Calendário, Filtros; Sem cadastro; Não definido; editar, cancelar e excluir), 8 relatório
para o parceiro, 12 movimentações e ficha do parceiro, 13 rastreamento, 16 checklist e assinaturas. Renumerados: portal 7→9, frota 8→10,
caçambas 9→11, relatório 10→14, regras 11→15, resumo 12→17. "Caçambas" agora é "Equipamentos". Tela da gravação 1600x900.

| # | Tema | O que a tela mostra | Partida |
|---|---|---|---|
| 0 | Abertura | Dashboard, "Coletas & Logística", "Ordens de Coleta". | `inicio` |
| 1 | O que o módulo resolve | Quadro sem ação; ilustração do caminho da coleta. | `inicio` |
| 2 | O quadro das ordens | Colunas, cartão novo (folhinha, "Hoje", "Preencher"), Quadro, Lista, Calendário, Filtros. | `inicio` |
| 3 | Criar uma ordem | "Nova ordem", etapas, "Sem cadastro", Tipo Fornecedor/Cliente, Parceiro Auto Peças Vale Forte. | `inicio` |
| 4 | Data e janela | "Data agendada", "Período", "Não definido". | `inicio` |
| 5 | Motorista e veículo | Etapa "Frota", "Criar ordem", cartão #9 em "Agendada". | `inicio` |
| 6 | Até concluir | Arrastar o #8, "Preencher", Recolhi/Entreguei, bags, "Concluir coleta", ordem #7 sem cadastro. | `apos-cap05` |
| 7 | Editar, cancelar e excluir | Menu do cartão, Editar, Cancelada, Excluir com a recusa do banco. | `apos-cap06` |
| 8 | Relatório para o parceiro | Botão "Relatório", Copiar link, WhatsApp, Imprimir. | `apos-cap07` |
| 9 | A coleta pedida pelo portal | Portal, "Solicitar coleta", cartão #10 "via portal", Recusar (Voltar), Aprovar, Agendar. | `apos-cap07` |
| 10 | Veículos e motoristas | Frota, FKD2E41, aviso de toneladas, FVL8A52, Sérgio Paiva. | `apos-cap09` |
| 11 | As caçambas e onde estão | Equipamentos, Novo tipo (Palete), Caçamba 02 em manutenção, Caçamba 06, Movimentar, saldos. | `apos-cap10` |
| 12 | Movimentações e ficha do parceiro | Nova movimentação, Editar/Excluir, Mostrar anuladas, aba Coletas da ficha. | `apos-cap11` |
| 13 | Onde está o caminhão | Rastreamento (mapa, Ao vivo, raio do GPS), Trajeto da ordem 7, Rotas. | `apos-cap12` + `rastreamento` |
| 14 | O relatório das coletas | Este mês, Mês passado, tabelas por status, motorista, veículo, parceiro. | `apos-cap12` |
| 15 | As regras das coletas | Prefixo, janelas, exigir aprovação, avisar solicitação, antecedência, dias aceitos. | `apos-cap12` |
| 16 | Checklist e assinaturas | Modelo "Coleta com caçamba", perguntas, padrão, assinatura, tela da ordem. | `apos-cap15` |
| 17 | Resumo | Montagem; cartão "Próximo". | (montagem) |

Alvo: ~2.943 palavras de fala (~19 min de voz), antes 1.716. A T20 deve partir de `apos-cap15`.

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
  | Placa | Descrição | Tara | Capacidade | Motorista |
  |---|---|---|---|---|
  | FKD2E41 | Caminhão truck | 6.380 kg | 14.000 kg | Edson Moura |
  | GHT7B19 | Caminhão 3/4 | 3.900 kg | 4.000 kg | Jair Lopes |
  | EZR4C63 | Picape | 1.750 kg | 1.000 kg | Tiago Freitas |
  Junção (`MUNDO_LINHA_DO_TEMPO.md`, "Frota"): a tara do FKD2E41 é a 2ª pesagem do T8 (6.380 kg). Sem "UF de licenciamento",
  "Tipo", rodado e carroceria (a T17 completa o FKD2E41 na tela, que abre com o selo "Sem tipo"); motoristas só com nome e
  telefone (a T17 completa o CPF e a CNH do Edson na tela).
- **Equipamentos:** tipo "Caçamba 5 m³" (uma a uma; unidades "Caçamba 01" a "Caçamba 05", condição OK) e tipo "Bag 1 m³"
  (por quantidade, 40). Movimentações: 01/08/2026 "Externo" → "Minha base" (as 5 caçambas e os 40 bags); 23/10 (ordem 5)
  "Minha base" → Cooperativa Recomeço, 10 bags; 27/10 (ordem 6) "Minha base" → Depósito Irmãos Siqueira, Caçamba 03.
- **Ordens de coleta** (com os eventos do histórico):
  | Nº | Parceiro | Situação em 10/11 07:00 | Data · janela | Motorista · placa | Material estimado |
  |---|---|---|---|---|---|
  | 1 | Cooperativa Recomeço | Concluída 02/10 | 02/10 · Manhã | Tiago Freitas · EZR4C63 | ~500 kg de latinha |
  | 2 | Auto Peças Vale Forte | Concluída 08/10 | 08/10 · Manhã | Jair Lopes · GHT7B19 | ~850 kg de chaparia (a compra de 08/10 da T9; junção) |
  | 3 | Depósito Irmãos Siqueira | Concluída 16/10 | 16/10 · Dia todo | Edson Moura · FKD2E41 | ~3 t de ferro misto |
  | 4 | Auto Peças Vale Forte | Cancelada 20/10 (motivo "Material ainda não separado") | 21/10 · Manhã | Jair Lopes · GHT7B19 | ~200 kg de baterias |
  | 5 | Cooperativa Recomeço | Concluída 23/10 (Entreguei 10 bags) | 23/10 · Tarde | Tiago Freitas · EZR4C63 | ~700 kg de PET |
  | 6 | Depósito Irmãos Siqueira | Concluída 27/10 (Entreguei Caçamba 03) | 27/10 · Manhã | Edson Moura · FKD2E41 | Entrega de caçamba |
  | 7 | Marcelo Tavares ("Sem cadastro", (12) 9 0000-5821, Rua das Paineiras, 215, Taubaté/SP) | A caminho desde 06:40 | 10/11 · Manhã | Tiago Freitas · EZR4C63 | ~300 kg de ferro de demolição |
  | 8 | Depósito Irmãos Siqueira | Agendada (criada em 05/11) | 10/11 · Manhã | Edson Moura · FKD2E41 | Troca da Caçamba 03: ferro misto, ~2 t |
  O endereço de cada parceiro cadastrado é o do cadastro (T4). Próximo número: 9. Nenhuma outra ordem de coleta no
  mundo (junção: a T12 cria a 9 e a 10; a T20, às 15:00, mostra a 10 no portal e cria a 11).
- **Janela do sistema no cap07:** antes de voltar a ela, o robô deixa o Rafael numa tela de Coletas que não seja o quadro
  (ex.: "Frota") e recarrega, para o ponto vermelho aparecer no menu (a consulta revalida a cada 60 s).
- **Portal:** link do portal da Cooperativa Recomeço (o do T20), aba "Coletas" sem senha, "solicitar coleta" ligado.
- **Esta aula cria:** a ordem 9 (Auto Peças Vale Forte, 11/11 · Manhã (junção: a Agenda da T25 lembra dela), Jair Lopes · GHT7B19, "~400 kg de radiadores e
  baterias", observação "Retirar pelo portão lateral"); a conclusão da 8 (Recolhi Caçamba 03, Entreguei Caçamba 05); a
  ordem 10 pelo portal (Cooperativa Recomeço, "PET prensado — 800 kg", 13/11 · Tarde), aprovada e agendada; o veículo
  FVL8A52 "Caminhão poliguindaste" (Toco, SP, tara 7.100 kg, capacidade 8.500 kg); o motorista Sérgio Paiva (CPF
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
