# Plano · T17 Transporte, serviço e o contador

- **Título:** Transporte, serviço e o contador (fonte). 🔒 módulo **Notas Fiscais** (dito na abertura, sem preço).
- **Antes:** T16 Nota Fiscal de mercadoria (NF-e). **Próximo:** T18 Ambiental: MTR e CDF.
- **Áreas das vinhetas:** TRANSPORTE · FROTA · MANIFESTO · SERVIÇO · COMPRA · RELATÓRIO FISCAL · ESTOQUE FISCAL · CONTADOR · RESUMO.
- **App 1.60.39** (28/11; `andamento_160.md`, seção "28/11 · 1.60.39"). **21 capítulos**: novo o 11 (a NF-e recebida vira compra);
  os de 11 a 19 viraram 12 a 20. Também do 1.60.15 ao 1.60.39 (a T17 só tinha sido ajustada ao 1.60.10): "Relatório/Estoque Fiscal" é
  uma tela só, com sete abas (menu, caps 00, 12 e 13); o "Fiscal × operacional" separa entradas e saídas (cap17); o Novo MDF-e pergunta
  a natureza da viagem, a categoria do transportador e "Esta viagem possui frete contratado?" (cap04); "Histórico" no menu do MDF-e e o
  diálogo único de histórico; o bloco "IBS e CBS da NFS-e" (desligado) no Serviço da NFS-e. 3.526 palavras (eram 3.197).
  Antes: aplicação de 18/11 (1.60.10), 20 capítulos; novos 6, 13 e 15 (hoje 6, 14 e 16).
- **Alvo da fonte:** ~16 min. **Estimativa (app 1.60.39, 28/11):** ~25 min de vídeo (3.526 palavras, ~22,6 min de fala, + 20 vinhetas +
  esperas da SEFAZ simulada). Aula única mesmo longa (Kaik, 18/11 13:47); profundidade extra por ser fiscal.
- Regime do exemplo **Lucro Real**; a fala mostra os campos e diz que quem define tributação (código do serviço, alíquota, retenção,
  crédito, devolução) é o contador. Nada de SEFAZ, prefeitura nem numeração de verdade: tudo no backend falso.
- **Fora da aula (decisão do coordenador):** SPED Fiscal (BETA); a marca do parceiro no balão "Como gerar o CIOT?" (o balão não é
  aberto); número de CFOP e valor de imposto na fala.
- Base: `T17/inventario.md` (código 1.59.154) + `T17/cobertura_160.md` (o que mudou no 1.60.10). Desktop, logado como **Rafael
  Nogueira** (MASTER).
- **FAKE_NOW:** `2026-11-10T09:30:00-03:00` nos capítulos 0 a 4; `14:20` do 5 ao 9 (a carga já foi entregue em Itamonte); `14:40` do
  10 ao 20 (as NFS-e recebidas chegaram às 14:24). Em `rec/t17/fake_now.json`, escrito pelo `gerar.py`.

## Capítulos (21: 0 a 20; 28/11)
| # | Era | Vinheta (área / título) | O que se mostra | Ilustração | Estado de partida |
|---|---|---|---|---|---|
| 0 | 0 | (sem vinheta) | Abertura; menu "Fiscal & Ambiental" com "Transporte (MDF-e)", "Notas de Serviço (NFS-e)", "Estoque Fiscal", "Relatórios Fiscais"; 🔒; "Antes" | o dia da Recicla Vale | `inicio` |
| 1 | 1 | TRANSPORTE / O que é o MDF-e | "Manifestos" vazio, cartões; ⚠️ obrigatoriedade | o manifesto | `inicio` |
| 2 | 2 | FROTA / Veículo e motorista | editar o FKD2E41 e o Edson Moura (CPF, CNH, categoria, validade) | não | `inicio` |
| 3 | 3 | TRANSPORTE / Numeração e percurso | "Configurações do MDF-e"; o percurso | rota SP → RJ → MG | `apos-cap02` |
| 4 | 4 | MANIFESTO / Emitir o manifesto | tela cheia "Novo MDF-e": NF-e 1255 e 1256; **nota de outra empresa pela chave** (884, entra e sai); FKD2E41 + Edson; **reboques** e **CIOT** (só mostra); RJ, Itamonte/MG, 5.800 kg, valor sugerido; observações; **contingência** (abre, 168 horas, volta); "Autorizado"; PDF | não | `apos-cap02` |
| 5 | 5 | MANIFESTO / Encerrar no fim da viagem | ⚠️ encerrar × cancelar; **diálogo "Cancelar MDF-e #1"** (abre e "Voltar"); "Encerrar" → "Encerrado" | encerrar × cancelar | `apos-cap04` (14:20) |
| 6 | novo | MANIFESTO / Quando o manifesto não passa | MDF-e nº 2 "Rejeitado": "Ver Erro", "Reemitir", "Excluir"; recusa de encerramento e de cancelamento; busca e detalhes | selos de recusa | `apos-cap05` + `mdfe2-rejeitado` |
| 7 | 6 | SERVIÇO / A nota de serviço | lista (nº 12 e 13); mercadoria × serviço | NF-e × NFS-e | `apos-cap05` |
| 8 | 7 | SERVIÇO / Emitir e acompanhar | tela cheia "Nova NFS-e": competência, **série e "Próxima DPS: nº 14"**, tomador (e "Buscar pelo CNPJ"), código, valor R$ 1.850,00, alíquota 3 %, **ISS retido e retenções federais** (só mostra), pré-visualização, **rascunho** (cita), emitir, nº 14, menu (PDF, Histórico, Cancelar) | não | `apos-cap05` |
| 9 | 8a | SERVIÇO / O serviço que você tomou | "Notas Recebidas" › "NFS-e": ativar; a faixa "Busca solicitada no Ambiente Nacional..."; ⚠️ só cidade do sistema nacional | não | `apos-cap08` |
| 10 | 8b | SERVIÇO / Da nota recebida à despesa | (14:40) as 2 notas chegaram; "Sincronizar agora"; lançar a da balança como conta; "Lançada" | não | `apos-cap09` + `nfse-recebidas` |
| 11 | novo (28/11) | COMPRA / Da nota recebida à compra | **1.60.39.** Notas Recebidas › NF-e: a Cooperativa Recomeço (importada pelo XML na T16), o "Importar XML" (sem clicar; também traz NFS-e), "Lançar compra…", os totais "Produtos" / "Encargos/descontos" / "Total da nota", o casamento já feito, "Registrar também no estoque fiscal (não altera o saldo físico)", "Conferir na tela de compra", Finalizar com Pix e o selo "Lançada como compra" | não | `apos-cap10` + `compra-coop` |
| 12 | 9 | RELATÓRIO FISCAL / Entrada, saída e saldo | menu **"Relatório/Estoque Fiscal"** (uma tela só, 1.60.15): aba "NF-e" de outubro (cartões, **cartão Entrada aberto**, gráficos) e **aba "NFS-e"** | não | `apos-cap10` |
| 13 | 10a | ESTOQUE FISCAL / O estoque pelas notas | **"Saldo atual"**: atualiza sozinho, busca, vermelho = negativo, faixa amarela | não | `apos-cap10` |
| 14 | novo | ESTOQUE FISCAL / O saldo inicial | "Informar saldo inicial" da bateria: 31/10/2026, 3.320 kg; aba "Planilha"; a bateria vai a 3.960 kg | não | `apos-cap10` |
| 15 | 10b | ESTOQUE FISCAL / Um dia do passado e as movimentações | "Posição em uma data" (31/10 18:00) ⚠️ só consulta; "Movimentações": Kardex do metal amarelo, "Filtros", "Geral (Todos)" | não | `apos-cap14` |
| 16 | novo | ESTOQUE FISCAL / Cancelamento e devolução | Kardex: NF-e 1249 (saída e "Estorno" com o motivo); NF-e 1253 (devolução da Fundição, +40 kg de cobre mel) | régua do estorno; setas da devolução | `apos-cap14` |
| 17 | 10c | ESTOQUE FISCAL / Fiscal e operacional | "Fiscal × operacional" de outubro (tela nova): cartões por direção, metal amarelo (Entradas: 500 comprados e 0 em nota, "sem nota"; Saídas: 500 vendidos e 1.100 em nota, +600 "nota a mais": a nota de 30/10 do pedido de 03/11), "Como ler a diferença", "Exportar" (PDF, Excel) | fiscal × operacional | `apos-cap14` |
| 18 | 11 | CONTADOR / O pacote do mês | "Exportação Contábil": "Emitente / CNPJ", "Mês passado", **"Incluir notas destinadas ao CNPJ"** (zero em outubro), "Baixar Pacote" | não | `apos-cap14` |
| 19 | 12 | CONTADOR / O que o contador faz | o conteúdo do ZIP (com "destinadas"); ⚠️ guardar os XMLs | o pacote | (só ilustração) |
| 20 | 13 | RESUMO / Recapitulando | montagem (com a compra da Cooperativa); "Próximo: Ambiental: MTR e CDF" | não | `apos-cap14` + `mdfe2-rejeitado` |

Transições faladas: 0→1 "Vamos começar pelo manifesto"; 1→2 "Antes do primeiro manifesto"; 2→3 "Com a frota pronta"; 3→4 "Hora de
emitir"; 4→5 "À tarde, a carga foi entregue"; 5→6 "E quando a SEFAZ não aceita?"; 6→7 "Agora, a nota de serviço"; 7→8 "Vou cobrar a
coleta"; 8→9 "E quando é a Recicla Vale que contrata"; 9→10 "Um pouco depois"; 10→11 "E a nota de mercadoria que chega de um fornecedor?" (novo); 11→12 "Antes de mandar o mês pro contador"; 12→13
"Agora, o estoque fiscal"; 13→14 "Quando a empresa começa a usar o sistema"; 14→15 "Pra ver um dia do passado"; 15→16 "E quando uma
nota é cancelada?"; 16→17 "Agora, a aba que compara o fiscal com o operacional"; 17→18 "Agora, o pacote"; 18→19 "E o que vai dentro dele".

**Cuidados (⚠️ da fonte), falados com "Uma dica:"**
| Cuidado | Onde | Fala (resumo) |
|---|---|---|
| Obrigatoriedade do MDF-e varia | cap01 | depende da operação e do estado; confirme com a contabilidade, principalmente entre estados; o sistema entrega a ferramenta |
| Contingência não é jeito normal | cap04 | só com a SEFAZ fora do ar; pede motivo, tipo de carga, NCM e produto; o motorista só sai com o manifesto impresso; até 168 horas para regularizar |
| Encerrar ≠ cancelar | cap05 | encerrar é o fim normal da viagem; cancelar anula o que não deveria existir: sem volta, motivo de 15 letras, prazo de 24 horas |
| Posição histórica é só consulta | cap15 | não muda saldo, nota, movimentação nem o estoque de hoje; a data é sempre do passado |
| Fiscal e operacional podem divergir | cap17 | o fiscal segue as notas; o operacional, compras, pedidos e pátio; um não corrige o outro (tela de comparação) |
| Guardar os XMLs é da empresa | cap19 | baixar o pacote todo mês e guardar cópia própria além da do contador |
Do código (não estão na fonte): peso sempre em quilos, a tela avisa se parecer tonelada (cap02); só chega NFS-e de cidade que entrou
no sistema nacional (cap09); cada NFS-e recebida conta na cota (cap09, na tela do diálogo). Novos no 1.60.10: o saldo inicial é
número fiscal, combinar com o contador (cap13); a devolução mexe nos impostos da nota original, isso é com o contador (cap15).

## Mundo: o que esta aula precisa
Vale a `JUNCAO_160.md` (18/11). A aula recebe da T16 as notas até a 1254 e cria:
- **Frota (base):** FKD2E41 "Caminhão truck" (tara 6.380 kg, 14.000 kg), GHT7B19 "Caminhão 3/4", EZR4C63 "Picape", sem dados de
  transporte; motoristas Edson Moura, Jair Lopes, Tiago Freitas só com nome e telefone. **Criado na tela (cap02):** FKD2E41 com UF SP,
  "Veículo único (truck, toco, utilitário)", rodado "Truck", carroceria "Aberta", 30 m³; Edson com CPF **318.472.650-90**, CNH
  **04728193604**, categoria "C", validade 18/03/2029.
- **Do fim da T16 (na `t17/inicio`, enquanto a T16 não deixa a semente final):** NF-e 1249 (Serra Fina, 320 kg de alumínio perfil,
  **cancelada** às 08:57, "Pedido alterado pelo cliente antes de a mercadoria sair do pátio"), 1250 (Fundição, 500 kg de cobre mel,
  R$ 23.950,00), 1251 (entrada do caixa, R$ 803,30), **1252** (Serra Fina, 150 kg de alumínio perfil, R$ 1.560,00), **1253** (entrada:
  a Fundição devolve 40 kg de cobre mel, R$ 1.916,00; CFOP de devolução de venda, o que a T16 fixar pela tela) e **1254**
  (complementar, R$ 250,00, sem efeito no estoque fiscal); 1246 e 1247 inutilizadas; Notas Recebidas (NF-e) ligado, com a 2157 (Auto
  Peças Vale Forte, **640 kg de bateria, lançada no estoque fiscal**) e a **884** (Depósito Irmãos Siqueira, R$ 2.100,00, chave válida).
- **28/11 (1.60.39) · NF-e recebida da Cooperativa Recomeço (na `t17/inicio`):** a 3871 de 09/11 (850 kg de Alumínio latinha × R$ 6,20 e
  1.200 kg de Plástico PET × R$ 1,90 = R$ 7.550,00), importada na T16 (cap23) pelo "Importar XML": `origem` "manual", com o XML, sem
  número nem série (a edge real não grava), manifestação "nenhuma". **Lateral `compra-coop` (só no cap11):** o caixa #85 do Rafael
  aberto às 08:31 com R$ 1.500,00 (o mesmo da T06). **Criado na tela (cap11):** a compra da Cooperativa, R$ 7.550,00 por Pix da Conta
  Principal, com a nota carimbada ("Lançada como compra") e as duas linhas no estoque fiscal. Os capítulos seguintes partem da
  `apos-cap10`/`apos-cap14` e não veem essa compra (nada do que eles falam muda).
- **Duas NF-e de saída de hoje** (09:05 e 09:12) para a **Serra Fina Alumínio Reciclagem** (Itamonte, MG): **1255**, alumínio perfil
  3.200 kg × R$ 10,40 = R$ 33.280,00, e **1256**, alumínio bloco 2.600 kg × R$ 8,50 = R$ 22.100,00 (soma **R$ 55.380,00**, **5.800 kg**).
- **MDF-e:** nenhum antes; série 1. **Criado na tela:** nº 1 (cap04, autorizado ~09:40; encerrado no cap05). **Lateral, só à tarde
  (caps. 6 e 19):** nº 2 "Rejeitado" (viagem de amanhã: NF-e 1252, GHT7B19, Jair Lopes, Taubaté/SP → Itamonte/MG, R$ 1.560,00, 150 kg;
  "A SEFAZ recusou o MDF-e — CPF do condutor: número inválido"). A T18 não herda.
- **NFS-e:** série 1 (`nfse_series`, último número 13); nº 12 (13/10, Fundição, R$ 950,00) e nº 13 (29/10, Aços Quiririm, R$ 1.850,00).
  **Criada na tela:** nº 14 (competência 06/11/2026, Aços Quiririm Ltda, R$ 1.850,00, ISS 3 %). Lista de Taubaté simulada (7.09, 3 %).
- **NFS-e recebidas:** desligado no início; fonte "sefin" (motor próprio). Depois de ativar (cap09), as duas notas chegam às 14:24
  (lateral `nfse-recebidas`): **Contabilidade Manacá Ltda** (47.291.836/0001-56, R$ 1.650,00) e **Balanças Tremembé Manutenção Ltda**
  (39.506.417/0001-66, R$ 980,00). **Criado na tela (cap10):** conta a pagar da Balanças Tremembé, R$ 980,00, vencimento 20/11/2026,
  categoria "Manutenção de máquinas".
- **Outubro (relatórios, estoque fiscal, exportação):** 12 NF-e de saída (R$ 168.940,00) e 9 de entrada (R$ 97.315,00, todas
  emitidas pela própria empresa), saldo **R$ 71.625,00**; NFS-e de outubro: 2 notas, R$ 2.800,00; nenhuma nota destinada em outubro
  ("Destinadas: 0 XML(s)").
- **Estoque fiscal:** saldo inicial de 01/08/2026 em todos os materiais, **menos a bateria** (faixa amarela); a bateria aparece com
  640 kg (a nota 2157). **Criado na tela (cap13):** saldo inicial da bateria, **3.320 kg em 31/10/2026** → 3.960 kg. O saldo de
  novembro já traz −150 kg de perfil (1252) e +40 kg de cobre mel (1253).
- **Fiscal × operacional de outubro:** o metal amarelo dá **Delta −1.100 kg** (Mov. Fiscal −1.100, Mov. Operacional 0): 600 kg da
  NF-e de 30/10 para a Fundição, com o pedido finalizado só em 03/11, mais 500 kg comprados de pessoa física sem nota. Outros
  materiais também aparecem com divergência (a fala explica o caso pela linha "Delta negativo costuma indicar compra de pessoa
  física sem nota").

## Gravação
- **Rotas:** `/fiscal-ambiental/transporte`, `/transporte/frota`, `/nfse`, `/nfe/recebidas`, `/nfe/recebidas-nfse`, `/nfe/saida`, `/compra`
  (cap11) e `/estoque-fiscal/posicao` (menu "Relatório/Estoque Fiscal", desde o 1.60.15 uma tela só: abas "Saldo atual", "Posição em
  uma data", "Movimentações", "Relatório de estoque", "Fiscal × operacional", "NF-e" (`/estoque-fiscal/relatorio-nfe`) e "NFS-e"). Sempre entrando pelo menu quando a câmera precisa mostrar o caminho.
- **28/11 (1.60.39), mundo:** handlers novos `functions/inbound-xml-import.mjs` (o "Importar XML"), `rpc/list_fiscal_document_history.mjs`
  (o Histórico de MDF-e, NFS-e, NF-e e MTR), `rpc/set_inbound_fiscal_entries.mjs` (a compra com "Registrar também no estoque fiscal");
  mudados `lib/eco.mjs` (`criarPedido` carimba `inbound_nfe.purchase_id`), `rpc/get_invoices_paged.mjs` (`p_fiscal_config_ids`) e
  `functions/plugnotas-nfse-dfe-sync.mjs` (o ramo "sefin" da função real: com o motor próprio a edge só avisa que a consulta é automática).
  Sub-abas: `[aria-label='Navegação da seção']` (no 1.60.39 é uma div `role=navigation`, não mais `<nav>`).
- **Handlers novos do 1.60.10 (só esta aula):** function `mdfe-contingency` (prepare, status, enclose, download, cancel); RPCs
  `get_invoice_dashboard_secure`, `get_nfse_dashboard`, `get_next_nfse_number`, `record_fiscal_inventory_entries`;
  `lib/estoque_fiscal.mjs` com os CFOP de devolução (2202, 5202, 6202) e as NF-e recebidas com lançamento fiscal. Continuam:
  `mdfe_contingency_availability`, `get_mdfe_stats`, `get_fiscal_inventory_position` (+ `_at`), `get_fiscal_inventory_history_paged`,
  `get_fiscal_inventory_report_data`, `get_inventory_report_data`, `count_invoices_for_export`, `fiscal_onboarding_status`,
  `plugnotas-nfse-servicos-municipio`, `plugnotas-emit-nfse`, `plugnotas-nfse-status`, `plugnotas-download`, `plugnotas-mdfe-download`.
- **Sementes** (`rec/mundo/seeds-extra/t17/`): `inicio`, `mdfe2-rejeitado`, `nfse-recebidas` e `compra-coop` (28/11) saem de `rec/t17/t17_sementes.py`; a
  cadeia `apos-cap02`, `04`, `05`, `08`, `09`, `10`, `14` (era `13`; renomeada em 28/11) sai do estado do ensaio (`t17_semente.py`) ou, sem navegador, de
  `t17_semente_api.py`.
- **Fora do app:** a lista de cidades vem da API do IBGE no navegador: resposta local para SP e MG.
- **Download:** o ZIP da exportação é gerado no navegador; o robô só deixa o download acontecer. O conteúdo aparece na ilustração.
- Sem celular, sem página pública, sem outro usuário, sem cena de Windows.
- **Ilustrações (10; estilo v3 pendente):** cap00 o dia da Recicla Vale; cap01 o manifesto; cap03 o percurso; cap05 encerrar ×
  cancelar; cap06 selos de recusa (nova); cap07 mercadoria × serviço; cap15 régua do estorno e setas da devolução (novas); cap16
  fiscal × operacional; cap18 o pacote e o contador. Lista e textos exatos: `cenas/ilustracoes.json`.
