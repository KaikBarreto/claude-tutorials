# Plano · T8 Ticket de Pesagem

- **Título:** Ticket de Pesagem (fonte). Sem 🔒: o módulo `ticket_pesagem` está desativado no catálogo e a tela é livre;
  a aula não fala em plano.
- **Antes:** T7 "Comprar e vender sucata". **Próximo:** T9 "Pedidos e histórico do caixa" ("achar e corrigir um pedido
  antigo").
- **Objetivo:** pesar o caminhão da Cooperativa Recomeço na entrada e na saída sem preço fechado, aplicar a impureza,
  atender um segundo caminhão em outra aba, imprimir o comprovante e valorizar o ticket até ele virar compra.
- **Duração:** alvo da fonte 11 min; fala ~1.240 palavras (~8 min) + 10 vinhetas, digitação, a aba do PDF e as
  ilustrações ≈ 10 min.
- **Base:** `T08/inventario.md` (código 1.59.154). Computador 1280×800, logado como **Rafael Nogueira**.
  `FAKE_NOW=2026-11-10T08:30:00-03:00` (terça); horários na tela entre 08:40 e 09:00.

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área / título) | O que se mostra | Duração |
|---|---|---|---|
| 0 | (sem vinheta) | Ticket de Pesagem; ilustração do caminhão na balança com o preço "?"; cartão "Antes" | 0:30 |
| 1 | TICKET / Quando usar o ticket | menu "Materiais" › "Ticket de Pesagem"; ilustração compra direta × ticket; regra dura; abas "Tickets padrão" e "Pesagens avulsas" (🚫 da avulsa); colunas do kanban | 1:05 |
| 2 | TICKET / Criar o ticket | "Novo Ticket de Pesagem"; "Ticket padrão", "Compra", "Sem valores"; "Cooperativa Recomeço"; "Alumínio latinha"; "Edson Moura" e "FKD2E41" | 0:55 |
| 3 | PESAGEM / A primeira pesagem e o rascunho | "Pesagem avançada": "1ª Pesagem" 9.460 kg, "= 1ª pesagem", "Completo", "Confirmar"; "Seu rascunho"; "Voltar" e "Rascunhos abertos" (1); ilustração do rascunho | 1:15 |
| 4 | PESAGEM / Descarregar e a segunda pesagem | ilustração entrada e saída do caminhão; "Adicionar tara / pesagem avançada"; "1ª Pesagem" 9.460 e "2ª Pesagem" 6.380; "Peso Bruto (Kg)" 3.080 "|9.460 − 6.380|"; tara | 1:00 |
| 5 | PESAGEM / Impureza em porcentagem ou em quilos | "Impureza" "%" 2 → "= 61,6 Kg (sobre bruto − tara)"; "Líquido (Kg)" 3.018,4; ilustração da conta; "kg" falado; "Confirmar" | 0:50 |
| 6 | ABAS / Vários veículos ao mesmo tempo | ilustração dois caminhões, duas abas; "+ Novo ticket": Auto Peças Vale Forte, bateria, Jair Lopes, GHT7B19, 1ª 5.640 kg; troca de aba; "Salvar Ticket de Pesagem" → "Ticket #58 salvo" | 1:15 |
| 7 | VALORIZAR / Valorizar o ticket | kanban "Aguardando valorização"; "Ações" › "Valorizar" → `/compra` preenchida (R$ 6,20/kg, R$ 18.714,08); ilustração do caminho até o estoque e o caixa | 1:00 |
| 8 | COMPROVANTE / Imprimir o comprovante | "Ver comprovante" › "Gerar comprovante do ticket" › "Térmico" → PDF ("TICKET DE PESAGEM", "NÃO VALORIZADO", as pesagens); chave "Imprimir comprovante do Ticket de Pesagem"; ilustração de mesclar | 1:05 |
| 9 | VALORIZAR / Quando o ticket sai dos pendentes | ainda pendente; "Valorizar" de novo ("retomando"); "Finalizar" com Pix; volta sozinho; "Valorizados" com "Valorizado pelo pedido #…"; os três status; o rascunho do Jair | 1:10 |
| 10 | RESUMO / Recapitulando | montagem; cartão "Próximo: Pedidos e histórico do caixa" | 0:40 |

Avisos da fonte: regra dura (cap. 1 e 7, como informação); sem status "Aguardando 2ª Pesagem", rascunho e número no
salvar (cap. 3); rascunho reaberto (cap. 3, "Uma dica:"); a conta Bruto e Líquido na tela (caps. 4 e 5, com zoom e
ilustração); mescladas no comprovante (cap. 8, "Uma dica:"); 🚫 pesagem avulsa (cap. 1); os três status (cap. 9);
módulo desativado (não citado).

## Estado de partida (fim do T7)
Mundo base + o que T3, T5 e T7 deixam: EcoTray falso ligado ("Balança do pátio" com 0 kg; "POS-58"), impressão direta e
balança ligadas no perfil do Rafael, "Imprimir comprovante do Ticket de Pesagem" desligada; **caixa do Rafael aberto**
(a compra do cap. 9 precisa); nenhum rascunho de ticket do Rafael; ticket #57 pendente no histórico; navegador novo (a
chave "Valores" nasce em "Sem valores").

## Mundo: o que esta aula precisa
| Item | Valores (fictícios) |
|---|---|
| Fornecedores | **Cooperativa Recomeço** (sem preço personalizado nem tabela própria: preço da tabela principal) e **Auto Peças Vale Forte** |
| Materiais | Alumínio latinha (compra R$ 6,20/kg); Bateria automotiva (R$ 3,10/kg) |
| Motoristas e placas (`drivers`, `vehicles`) | Edson Moura · FKD2E41 (caminhão truck); Jair Lopes · GHT7B19 (caminhão 3/4); Tiago Freitas · EZR4C63 (do mundo) |
| Tickets | histórico até o #57 (#57 aguardando valorização); `get_next_ticket_number` = **58** (ajustar ao mundo; a fala não lê o número) |
| Criado: ticket #58 | compra, sem valores, Cooperativa Recomeço, Alumínio latinha; 1ª 9.460 kg, 2ª 6.380 kg, bruto 3.080 kg, impureza 2% = 61,6 kg, líquido 3.018,4 kg; "Completo"; Edson Moura, FKD2E41 |
| Criado: compra | do ticket #58: 3.018,4 kg × R$ 6,20 = **R$ 18.714,08**, paga por "Pix/Transferência" na conta bancária principal; o ticket fica "Valorizado pelo pedido #…" |
| Criado: rascunho | aba do Jair: Auto Peças Vale Forte, Bateria automotiva, 1ª 5.640 kg, GHT7B19 (fica em "Rascunhos abertos") |

**Fica para as próximas:** a compra da latinha (T9 vê no histórico; T10, +3.018,4 kg no estoque; T14, a saída do Pix);
o rascunho do Jair (se incomodar alguma aula, apagar na semente).

## Gravação
- **Rotas:** `/ticket-pesagem`, `/compra` (aberta pela valorização), `/configuracoes?tab=integrations` (só o zoom do cap. 8).
- **Banco e RPC:** `weighing_tickets` (rascunho gravado a cada mudança, lista e kanban), `get_next_ticket_number`,
  `finalize_weighing_ticket_v3`, `order_drafts` (insert na 1ª valorização, update na 2ª), `drivers`, `vehicles`,
  `suppliers`, `materials`, preços (`entity_custom_prices`, tabelas), `profiles`, e o finalizar da compra do T7
  (`create_purchase_atomic`).
- **Aba nova:** o comprovante "Térmico" abre o PDF numa aba (gravar a aba).
- **EcoTray falso:** só ligado, como no fim do T5 (sem ele, o aviso "Balança desconectada" aparece em toda tela). Sem
  cena de Windows: a janela do EcoTray não aparece nesta aula.
- **Ilustrações:** o caminhão sem preço (cap. 0); compra direta × ticket e a regra dura (1); o rascunho salvo (3);
  entrada e saída do caminhão (4); a conta do líquido (5); dois caminhões, duas abas (6); do ticket ao estoque e ao
  caixa (7); pesagens mescladas no papel (8).

## Riscos e decisões para o Kaik
1. **Pesos digitados:** os caminhões passam na balança rodoviária, que não está no EcoTray (a do T5 é a do pátio); a fala
   diz que, com a balança no EcoTray, o botão dentro do campo puxa o peso. Alternativa: uma "Balança rodoviária" no
   EcoTray falso e a captura pelo botão.
2. **Na saída, a 1ª pesagem é digitada de novo:** com só a 1ª, o app guarda o peso como bruto e a "1ª Pesagem" volta
   vazia na edição (`AdvancedWeighingDialog.tsx:209-213,337-338`). A aula mostra o caminho como ele é (handoff H1).
3. **Preço da valorização:** ticket sem valores valoriza pela tabela padrão da empresa, não pela tabela do fornecedor
   (`WeighingTicket.tsx:2354-2355`). Com o Depósito Irmãos Siqueira (Tabela Depósitos do T3) sairia R$ 0,75 em vez de
   R$ 0,78; por isso o exemplo usa a Cooperativa Recomeço (handoff H2).
4. **Finalizar a compra no cap. 9** (mexe no estoque e no banco; precisa do caixa aberto). Alternativa: mostrar um ticket
   já valorizado do histórico.
5. Chave "Imprimir comprovante do Ticket de Pesagem" e "Mesclar" só mostradas/ilustradas, sem mudar o mundo.

## Handoffs (a fala não depende deles)
- H1 Guardar a 1ª pesagem do item quando só ela existe (hoje vira bruto e some do campo "1ª Pesagem" na edição).
- H2 Valorizar ticket sem valores ignora a "Tabela de Preços Padrão" do fornecedor.
- H3 A coluna "Peso" da barra de abas soma o bruto (`OrderSwitcher.tsx:156-161`); o comentário diz líquido.
- H4 "Térmico" diz "80mm" e o comprovante manual do ticket sai no desenho de 80 mm mesmo com papel de 58 mm (a impressão
  automática usa a largura de Integrações) (`WeighingTicket.tsx:3127-3142,3367-3372`).
- H5 Na janela "Pesagem avançada" de um ticket sem valores, "Valor/Kg", "Valor estimado", "Desconto (R$)" e "Valor final"
  continuam aparecendo (ficam vazios).
