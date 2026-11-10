# Plano · T20 · Portal do Cliente e Fornecedor

- **Título:** Portal do Cliente e Fornecedor (o da fonte). 🔒 módulo `portal_cliente` (a aba Coletas também depende de `coletas`).
- **Objetivo (uma frase):** dar à Cooperativa Recomeço um portal só dela, com o link certo, as abas escolhidas e senha, e mostrar
  o que o parceiro consulta e faz sozinho (histórico, saldo, notas, relatório, pedido de coleta, comprovante e fotos).
- **Antes:** T4 · Clientes, fornecedores e a ficha do parceiro. **Próximo:** T22 · Gerencial: matriz e filiais.
- **Áreas das vinhetas:** PORTAL · LINK · EXIBIÇÃO · SENHA · HISTÓRICO · SALDO · NOTAS E RELATÓRIO · COLETAS · COMPROVANTE · FOTOS ·
  RESUMO.
- **Duração:** alvo da fonte ~12 min; fala de 1.515 palavras (~9,7 min de voz) → ~12 min de vídeo com as vinhetas e as ações.
- **Base:** `T20/inventario.md` (código 1.59.154). Desktop 1280×800, tema claro. Usuário do sistema: Rafael Nogueira (MASTER).
- **FAKE_NOW:** `2026-11-10T15:00:00-03:00` (terça à tarde): a venda sem valor da T7 e a nota 1250 da T16 são "de hoje" e já
  existem; o pagamento da T4 (08:35) também.

## Capítulos (os 10 da fonte, na ordem; cap00 abertura e cap11 recapitulando)

| # | Vinheta (área / título) | O que a tela mostra | Estado de partida | Duração |
|---|---|---|---|---|
| 0 | (sem vinheta) | [ILUSTRAÇÃO: prints × link]; Dashboard → "Clientes e Fornecedores" → "Fornecedores" → Cooperativa → "Acesso ao portal"; cartões "Módulo Portal do Cliente" e "Antes: …" | `inicio`, sistema | 0:50 |
| 1 | PORTAL / O que o parceiro vê | Navegador do parceiro no link da cooperativa: cabeçalho, cartão, as cinco abas; [ILUSTRAÇÃO: até onde vai o acesso]; dica "Portal indisponível" | `inicio`, parceiro | 1:00 |
| 2 | LINK / Pegar o link do portal | Ficha › "Acesso ao portal" › "Copiar" (toast); "..." › "Portal do Fornecedor"; zoom no código; [ILUSTRAÇÃO: o link é uma chave]; "Editar" › aba "Portal" | `inicio`, sistema | 0:55 |
| 3 | EXIBIÇÃO / Escolher as abas | "O que exibir no portal" (só mostra), zoom em "Valores financeiros"; "Formato do comprovante no portal" → "A4"; "Salvar exibição"; [ILUSTRAÇÃO: cliente e fornecedor, vale o que esconde mais] | `inicio`, sistema | 1:10 |
| 4 | SENHA / Usuário e senha | "Pedir login no portal", "Usuário", "Senha", "Salvar acesso"; pílulas "Oculto"/"Livre"/"Com senha"; [ILUSTRAÇÃO: as três escolhas]; parceiro: "Acesso restrito" → "Entrar"; ícone "Sair" | `apos-cap03` | 1:10 |
| 5 | HISTÓRICO / Histórico de pedidos | Cooperativa: cartões, gráfico, a compra de 06/11 aberta, uma foto; Fundição: a venda de hoje com "R$ 0,00" e cadeado | `apos-cap04`, parceiro com sessão | 1:15 |
| 6 | SALDO / O saldo do parceiro | "Saldo Atual" R$ 1.350,00 verde; [ILUSTRAÇÃO: o mesmo saldo dos dois lados]; extrato; no sistema, Pix de R$ 1.350,00; no portal, "Em dia"; "Atualizar dados" | `apos-cap04` | 1:15 |
| 7 | NOTAS E RELATÓRIO / Notas e relatório | Fundição: NF-e 1250 "Autorizada" (sem download); cooperativa: "Relatório", "Mês passado", total R$ 18.755,00, "Baixar PDF" (sem clicar) | `apos-cap06` | 1:05 |
| 8 | COLETAS / O parceiro pede a coleta | "Coletas" → "Solicitar coleta" (papelão e PET, 2.500 kg, 12/11 manhã) → "Solicitada"; sino do sistema; [ILUSTRAÇÃO: quem pede e quem decide] | `apos-cap06` | 1:10 |
| 9 | COMPROVANTE / O comprovante do portal | Impressora da compra de 06/11 → PDF A4 com o QR "Escaneie para ver fotos" | `apos-cap08` | 0:40 |
| 10 | FOTOS / As fotos do pedido | [ILUSTRAÇÃO: anexar fotos; celular lendo o QR]; `/fotos/...`: carrossel, tela cheia, "Dados do Pedido"; [ILUSTRAÇÃO: os dois links públicos e o QR "Ver no portal" do caixa] | `apos-cap08`, navegador sem nada | 1:00 |
| 11 | RESUMO / Recapitulando | Montagem dos trechos; cartão "Próximo: Gerencial: matriz e filiais" | (reaproveita) | 0:40 |

Transições faladas: 0→1 "Vamos ver o que a cooperativa enxerga"; 1→2 "Agora, o link"; 2→3 "é aqui que a gente escolhe o que a
cooperativa vê"; 3→4 "Agora, a proteção"; 4→5 "Com o portal aberto, a primeira aba é o Histórico"; 5→6 "Agora, o saldo"; 6→7
"Na aba Notas Fiscais"; 7→8 "A aba Coletas"; 8→9 "E se a cooperativa precisar do comprovante"; 9→10 "Agora, as fotos".

**Cuidados da fonte na fala**

| Marca | Onde | Fala (resumo) | Na tela |
|---|---|---|---|
| ⚠️ Quem tem o link, entra; um código por cadastro | cap02 | "Repara no fim do endereço. Esse código é só da cooperativa…" + "Uma dica: quem tem o link, entra. Então manda só pro contato certo…" | zoom no fim do link; ilustração da chave |
| ⚠️ Dois links públicos (fotos × portal) | cap10 | "Uma dica: são dois links diferentes. O de fotos mostra só aquele pedido. O do portal mostra o histórico inteiro…" | ilustração |
| ⚠️ Cliente e fornecedor: o mais restritivo manda | cap03 (e a senha no cap04) | "Uma dica: tem parceiro que é cliente e fornecedor… desligar uma aba num cadastro desliga nos dois links. Vale sempre o que esconde mais." | ilustração com o Depósito Irmãos Siqueira |
| ⚠️ Saldo do portal = o da ficha, em até 30 s | cap06 | pagamento de verdade + "Uma dica: o saldo do portal vem da mesma conta-corrente da ficha… em até trinta segundos" | "Em dia" sem reenviar o link |
| ⚠️ Pedido sem valor: R$ 0,00 com cadeado; "Valores financeiros" | cap05 (e cap03, cap09) | "Uma dica: a venda de hoje saiu com o Comprovante sem valores. Então, no portal, ela aparece com zero e um cadeado." | zoom no "R$ 0,00" da Fundição |
| ⚠️ Sem o módulo: "Portal indisponível" | cap01 | "Uma dica: se um parceiro avisar que o link mostrou Portal indisponível, confere o plano da empresa." | (só fala; a tela não é gravada) |
| 🚫 O parceiro não altera nada; só pede coleta; quem agenda é você | cap01 e cap08 | "O portal é só pra ver… A única coisa que ele manda é um pedido de coleta. E quem marca o dia… é você." | ilustrações |
| 🚫 Notas sem download de XML e DANFE | cap07 | "O arquivo da nota, o XML ou o DANFE, você manda pelo caminho de sempre, nas Notas Fiscais do sistema." | tabela sem botão |
| 🔒 Portal do Cliente; Coletas | cap00, cap08 | "depende do plano contratado" | cartões "Módulo Portal do Cliente" e "Módulo Coletas" |

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)

Começa do fim da T4 para a cooperativa (saldo R$ 1.350,00 depois do Pix de R$ 1.200,00 das 08:35) e com o que a T7 e a T16
criaram para a Fundição. White Label desligado (a T20 é gravada antes da T27). Módulos `portal_cliente` e `coletas` ativos.

| Item | Valores (fictícios) |
|---|---|
| Empresa | `companies.name` "Recicla Vale Metais", CNPJ 47.318.506/0001-07, telefone, e-mail e endereço da T1; logo da T1; `show_photo_qr_on_receipt` **true**; `receipt_format` térmico (T1); sem linha em `collection_settings` (o padrão exige aprovação: a coleta entra "Solicitada") |
| Cooperativa Recomeço (fornecedora PJ) | `portal_token` **fixo na semente** (o robô abre `/portal/recicla-vale-metais-cooperativa-<código>`); no `inicio`: sem senha, `portal_config` nulo, `portal_receipt_format` "auto"; endereço do cadastro completo (o da semente base; aparece no "Endereço da coleta") |
| Histórico da cooperativa (T4) | 14 compras, uma por sexta de 07/08 a 06/11, forma "Saldo", pagas por Pix na segunda seguinte; "Total Comprado" R$ 52.937,50, "Ticket Médio" R$ 3.781,25; gráfico Papelão 59 %, Plástico PET 18 %, Alumínio latinha 9 %, Chaparia 8 %, Ferro misto 6 %; outubro (5 compras): Papelão 8.400 kg (R$ 4.620,00), Plástico PET 2.600 kg (R$ 4.940,00), Alumínio latinha 1.250 kg (R$ 7.750,00), Chaparia 1.100 kg (R$ 770,00), Ferro misto 900 kg (R$ 675,00) = **R$ 18.755,00** (status `completed`) |
| Compra de 06/11 da cooperativa | Papelão 1.700 kg × 0,55 = 935,00; Plástico PET 520 kg × 1,90 = 988,00; Alumínio latinha 240 kg × 6,20 = 1.488,00; Chaparia 220 kg × 0,70 = 154,00; Ferro misto 180 kg × 0,75 = 135,00; total **R$ 3.700,00**, forma "Saldo". **Três fotos** em `order_attachments` (`order_kind` purchase, bucket `order-attachments`): `t20-carga-papelao.jpg` (fardos de papelão no pátio), `t20-carga-pet.jpg` (bags de PET prensado), `t20-carga-latinha.jpg` (bags de latinha); imagens fictícias feitas por código ou render, 1600×1200, sem pessoa, sem placa, sem marca. `order_photo_shares` com **token fixo** para essa compra (o cap10 abre `/fotos/recicla-vale-metais-compra-<nº>-<código>`) |
| Saldo da cooperativa no `inicio` | R$ 1.350,00 (positivo no fornecedor = a Recicla deve); últimos movimentos: Pix R$ 1.200,00 em 10/11 08:35 ("Valor Pago a Cooperativa Recomeço · Acerto parcial da entrega de 06/11"), Pix R$ 1.150,00 em 09/11, compra de 06/11 R$ 3.700,00 |
| Acesso do portal (cap04) | "Usuário" **cooperativa.recomeco**, "Senha" **Recomeco#2611** (só na tela, em pontinhos; nunca falada) |
| Pagamento (cap06) | Pix **R$ 1.350,00**, conta bancária principal, "Observação" "Acerto da entrega de 06/11", 10/11 ~15:05; saldo da cooperativa R$ 0,00 |
| Coleta (cap08) | "Material *" "Papelão e PET prensados", "Quantidade estimada" "2.500 kg", "Data preferida" **12/11/2026** (quinta), "Período" "Manhã", endereço do cadastro, "Observações" "Os fardos ficam na doca do galpão."; número = o próximo de `get_next_collection_order_number` (a fala não lê); `user_notifications` para Rafael, Juliana e Marcos |
| Fundição Bandeira do Vale (cliente PJ) | `portal_token` **fixo**, sem senha, `portal_config` nulo. Vendas de hoje: 09:12, a da T7 com **"Comprovante sem valores"** (`hide_financial_details` true): Metal amarelo (latão) 152 kg × 31,90 + Cobre mel 60 kg × 47,90, Pix R$ 7.722,80; 10:05, a da T16: Cobre mel 500 kg × 47,90 = R$ 23.950,00. **NF-e 1250**, série 1, saída, `emitida`, R$ 23.950,00, autorizada às 10:41 (a da T16) |
| Depósito Irmãos Siqueira | só na ilustração do cap03 (nada muda no banco) |

**Sementes** (`seeds-extra/t20/`): `inicio` (caps 0 a 3), `apos-cap03` (+ A4 e `portal_config` salvo; cap04), `apos-cap04`
(+ senha; caps 5 e 6), `apos-cap06` (+ pagamento; caps 7 e 8), `apos-cap08` (+ coleta solicitada e notificação; caps 9 e 10).
Fica para as próximas: nada que outra aula precise (a coleta "Solicitada" da cooperativa pode servir de exemplo à T12, se ela quiser).

## Gravação

- **Dois navegadores** (contextos separados): o **do sistema** (Rafael logado) e o **do parceiro** (sem sessão do sistema; só o
  `localStorage` do portal). A câmera alterna entre eles nos caps 4, 6 e 8. Do cap05 em diante, o `setup` entra no portal da
  cooperativa fora do vídeo (formulário "Acesso restrito", ou `portal_session_<token>` aceito pelo backend falso). O portal da
  Fundição fica numa segunda aba do navegador do parceiro (caps 5 e 7).
- **Rotas:** sistema `/dashboard`, `/clientes-fornecedores` (ficha ao lado, abas "Visão geral" e "Conta-corrente"); públicas
  `/portal/<empresa>-cooperativa-<código>`, `/portal/<empresa>-fundicao-<código>`, `/fotos/<empresa>-compra-<nº>-<código>`.
- **Edges a simular** (detalhes nas marcas `[BACKEND]` do roteiro): `entity-portal` (payload completo do inventário: `entity`,
  `company`, `portal_config` mesclado, `locked_sections`, `requires_login`, `requiresLogin` sem sessão, `balance`, `movements` dos
  últimos 90 dias, `orders` com `items` e `attachments` assinados, valores zerados quando `hide_financial_details`, `invoices`,
  `has_coletas`, `collections`, `time_windows`; sem `price_list`); `entity-portal-report` (compras `completed` por período);
  `portal-set-credentials`; `portal-login` (sessão); `portal-order-receipt` (dados do PDF + `photoQr` "/fotos/…");
  `collection-request` (insert + notificações); `order-photos-public`. RPCs `create_manual_bank_transaction`, `update_balance`,
  `get_next_collection_order_number`, `has_module`. Tabelas: `suppliers` (update de `portal_config`/`portal_receipt_format`),
  `balances`, `balance_movements`, `collection_orders`, `user_notifications`, `order_attachments`, `order_photo_shares`, `invoices`;
  storage `order-attachments` (URLs assinadas das três fotos).
- **[TESTAR]:** área de transferência no "Copiar" (dar a permissão ao navegador do robô); a janela nova do PDF no cap09 (o robô
  a captura; se bloquear, o comprovante abre por cima do portal, e serve também); a busca nova do portal ao voltar o foco (cap06);
  o sino depois da coleta (sem realtime, o `setup` recarrega a tela do sistema antes do clique).
- **Não clicar:** "Baixar PDF" do Relatório (abre outra janela), "Abrir portal" da aba Portal, "Remover login", "Mostrar aba Preços".
- **Ilustrações** (cenas HTML no estilo da marca, `docs/09-aula-ilustrada.md`; balões e celulares genéricos, sem logo de aplicativo;
  nenhuma imita tela do app): cap00 prints × link; cap01 até onde vai o acesso; cap02 o link é uma chave; cap03 cliente e fornecedor,
  vale o que esconde mais; cap04 Oculto, Livre e Com senha; cap06 o mesmo saldo dos dois lados; cap08 quem pede e quem decide; cap10
  as fotos entram no pedido, o celular lendo o QR e os dois links públicos (com o cupom do caixa e "Ver no portal").
- Celular: nenhum (opcional, o cap10 em `device: phone`, se o Kaik quiser a página de fotos como abre no celular). Cena de Windows:
  nenhuma. Outro usuário: só o parceiro anônimo.

## Riscos e decisões para o Kaik

1. **Dois parceiros no portal**: a cooperativa é o fio da aula; a Fundição entra para o cliente com o pedido sem valor (cap05) e a
   nota fiscal (cap07), porque a cooperativa não tem nota emitida para ela (a nota dela é a que ela emite, T16 cap17).
2. **FAKE_NOW às 15:00**: para a venda sem valor da T7 e a nota 1250 da T16 serem "de hoje" sem ficar no futuro. Alternativa: as
   duas em 06/11 e o FAKE_NOW das 08:30 (a fala troca "de hoje" por "de sexta").
3. **Senha ligada do cap04 ao fim**: os capítulos seguintes entram no portal fora do vídeo. Alternativa: "Remover login" no fim do
   cap04 (a recapitulação perde a "senha configurada" da fonte).
4. **Pagamento de verdade no cap06** (a cooperativa fica em dia): prova o "reflete sem reenviar link". Nenhuma aula depende desse
   saldo depois da T20.
5. **Código × fonte** (inventário, seção 6): o Relatório soma também o pedido sem valor (só "Mostrar valores" esconde ali); o saldo do
   portal desconta pedido sem valor lançado no saldo; a aba "Preços" do fornecedor existe e fica fora da fala; o cabeçalho diz
   "Portal do Cliente" também ao fornecedor. Handoff para o time, se quiserem corrigir.
6. **QR do comprovante do caixa**: no sistema, o QR leva ao portal do parceiro ("Ver no portal", já no pedido) quando ele tem link,
   e todos têm no mundo. Conferir se a ilustração do cupom da T7 desenhou o QR (o cupom real tem).
