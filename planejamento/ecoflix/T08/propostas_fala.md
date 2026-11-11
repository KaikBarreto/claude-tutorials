# Propostas de fala · T8 Ticket de Pesagem

Do robô e do ensaio (rec/t08, app 1.59.154, voz ESTIMADA). Não editam `roteiro.md` nem `tts_textos.py`: a revisão geral aplica.
Linha = número da linha da coluna Fala no capítulo (L1 = a primeira).

## Fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 06 | L2/L3 | "… Em Novo ticket, abre uma aba em branco." / "Fornecedor, material, motorista, placa e a primeira pesagem: cinco mil seiscentos e quarenta quilos." | Mesma fala, com um respiro de ~3 s logo depois de "aba em branco." (`pausas.py 06 T:3`, T = fim da L2) | Os cinco campos custam ~11 s de robô (fornecedor, material, motorista, placa, Pesagem avançada) e a L3 tem 8,3 s. Hoje o robô começa a preencher ainda na L2 e escolhe as opções das listas sem levar o cursor (time-lapse); com o respiro, o fornecedor cai na palavra "Fornecedor" e a edição acelera o trecho calado. |
| 07 | L1 | "No fim do dia, o preço com a cooperativa fechou." | "Pouco depois, o preço com a cooperativa fechou." | Linha do tempo do mundo ("O dia 10/11"; seção 16, item 14): o ticket #58 vai das 08:40 às 09:00 e a compra dele é finalizada perto das 09:00 (a T20 a vê às 15:00). "No fim do dia" contradiz. |
| 09 | L5 | "… Valorizado, em verde; e Cancelado, em vermelho." | "… Valorizado, em verde; e Cancelado." | Não há ticket cancelado no mundo: a tela mostra só os selos âmbar (#57) e verde (#58); "Cancelado" aparece como opção do filtro Status, sem cor. |

## Achados do app

- **Valores num ticket "Sem valores"** (H5 do plano, com outro detalhe): na "Pesagem avançada" de um item NOVO (cap03), a janela mostra
  "Valor/Kg R$ 6,20" e, depois da 1ª pesagem, "Valor estimado R$ 58.652,00" e "R$/Kg efetivo: R$ 6,20"; na edição do item (caps 04 e
  05) o Valor/Kg vem vazio e aparece "Valor estimado R$ 0,00" e "R$/Kg efetivo: R$ 0,00". A fala não cita, mas os valores ficam no quadro.
- **Comprovante "Térmico" em janela nova** (`openReceiptWithLoading` → `window.open` + `<iframe>` com o PDF): o gravador filma uma aba
  só e o Chromium sem janela não desenha PDF. A gravação mostra a lista enquanto a fala do cap08 (L2 e L3) descreve o papel: o robô
  guarda o PDF que o app gerou (`rec/t08/arquivos/cap08-comprovante-termico.pdf`) para a ilustração da edição (PERFIL: "Comprovante: o
  PDF do app"), com os zooms do roteiro ("TICKET DE PESAGEM" / "NÃO VALORIZADO" e as linhas da conta).
- **A 1280 px com o menu lateral aberto**, a Compra corta "Peso Líquido" ("3.0…"), "Valor Total" ("18.714,0…") e o fornecedor
  ("Cooperat…"), e o botão do Cato cobre o "Total da Compra"; a Lista corta a coluna Status ("Valoriza…"). O robô recolhe o menu no
  `setup` dos caps 07 a 09 (fora do vídeo).
- **Motorista e placa**: Enter não escolhe a sugestão (no Material escolhe); o robô clica a sugestão.
- **Fornecedor**: a janela "Selecionar Fornecedor" já lista a Cooperativa Recomeço e a Auto Peças Vale Forte sem busca; o robô clica
  direto (o roteiro dizia digitar "Recomeço").

## Mundo (para o coordenador)

- **1.200 e 800 kg (ilustração das pesagens mescladas, cap08 L5)**: não aparecem na tela do app. O cap08 grava a lista, a janela "Gerar comprovante do ticket" e Configurações › Integrações; o ticket #58 não tem pesagens mescladas. Os números ficam só na ilustração, e a fala não os diz.

- **Ticket #57 do mundo base com 0 kg**: está "Aguardando valorização" com `items: []`, então o cartão (cap01, L4, zoom na coluna) e a
  Lista (cap09) mostram "Bateria automotiva 0 kg" / "0 kg líq.". O `MUNDO_FICTICIO.md` fala em "#57 em rascunho"; o T8 pede pendente. A
  semente da junção precisa de um item com peso no #57 (não mexi: é do mundo base).
