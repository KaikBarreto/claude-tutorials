# Plano · T17 Transporte, serviço e o contador

- **Título:** Transporte, serviço e o contador (fonte). 🔒 módulo **Notas Fiscais** (dito na abertura, sem preço).
- **Antes:** T16 Nota Fiscal de mercadoria (NF-e). **Próximo:** T18 Ambiental: MTR e CDF.
- **Áreas das vinhetas:** TRANSPORTE · FROTA · MANIFESTO · SERVIÇO · RELATÓRIO FISCAL · ESTOQUE FISCAL · CONTADOR · RESUMO.
- **Alvo da fonte:** ~16 min. **Estimativa:** ~13 min de vídeo (1.841 palavras, ~11,8 min de fala, + 13 vinhetas + esperas da
  SEFAZ simulada).
- Regime do exemplo **Lucro Real**; a fala mostra os campos e diz que quem define tributação (código do serviço, alíquota) é o
  contador. Nada de SEFAZ, prefeitura nem numeração de verdade: tudo no backend falso.
- Base: `T17/inventario.md` (código 1.59.154). Desktop, logado como **Rafael Nogueira** (MASTER).
- **FAKE_NOW:** `2026-11-10T08:30:00-03:00` nos capítulos 0 a 4; **corte** para `2026-11-10T14:20:00-03:00` do capítulo 5 ao 13
  (a carga já foi entregue em Itamonte; a tarde do mesmo dia).

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área / título) | O que se mostra | Ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (sem vinheta) | Abertura; menu "Fiscal & Ambiental" com "Transporte (MDF-e)", "Notas de Serviço (NFS-e)", "Estoque Fiscal"; 🔒; "Antes" | o dia da Recicla Vale (carga, caçamba, contador) | `inicio` |
| 1 | TRANSPORTE / O que é o MDF-e | "Transporte (MDF-e)" › "Manifestos" vazio, cartões; ⚠️ obrigatoriedade varia por operação e estado | o manifesto junta notas, caminhão e motorista; abre na saída, fecha na chegada | `inicio` |
| 2 | FROTA / Veículo e motorista | "Frota": editar o FKD2E41 (dados de transporte) e o Edson Moura (CPF, CNH) | (não: tara é só citada) | `inicio` |
| 3 | TRANSPORTE / Numeração e percurso | "Configurações do MDF-e" (série 1, próximo 1); o conceito do percurso | rota Taubaté (SP) → RJ → Itamonte (MG) | `apos-cap02` |
| 4 | MANIFESTO / Emitir o manifesto | "Novo MDF-e": 2 NF-e da Serra Fina, FKD2E41 + Edson, percurso RJ, destino Itamonte/MG, 5.800 kg; ⚠️ contingência; "Autorizado"; menu com o PDF | (não) | `apos-cap02` |
| 5 | MANIFESTO / Encerrar no fim da viagem | corte da tarde; ⚠️ encerrar × cancelar; "Encerrar" → "Encerrado" | encerrar × cancelar (linha do tempo) | `apos-cap04` (14:20) |
| 6 | SERVIÇO / A nota de serviço | "Notas de Serviço (NFS-e)": lista (nº 12 e 13); diferença mercadoria × serviço | NF-e × NFS-e (sucata saindo × caçamba) | `apos-cap05` |
| 7 | SERVIÇO / Emitir e acompanhar | "Nova NFS-e" para a Aços Quiririm: coleta com caçamba, R$ 1.850,00; "Autorizada" nº 14 | (não) | `apos-cap05` |
| 8 | SERVIÇO / O serviço que você tomou | "Notas Recebidas" › "NFS-e": ativar, 2 notas chegam, lançar a da balança como conta | (não: a tela mostra) | `apos-cap07` |
| 9 | RELATÓRIO FISCAL / Entrada, saída e saldo | "Estoque Fiscal" › "Relatório fiscal", "Mês passado" (outubro) | (não) | `apos-cap08` |
| 10 | ESTOQUE FISCAL / O estoque pelas notas | "Posição do estoque" (agora e 31/10), "Histórico fiscal" (metal amarelo), "Fiscal × operacional" (Delta −600 kg); ⚠️ consulta, ⚠️ divergência | fiscal × operacional (duas réguas) | `apos-cap08` |
| 11 | CONTADOR / O pacote do mês | "⋮" › "Exportação Contábil", "Mês passado", "Baixar Pacote" | (não) | `apos-cap08` |
| 12 | CONTADOR / O que o contador faz | o conteúdo do ZIP; mandar ao contador; ⚠️ guardar os XMLs | o pacote aberto; o caminho até o contador; a cópia guardada | (só ilustração) |
| 13 | RESUMO / Recapitulando | montagem do que foi feito; "Próximo: Ambiental: MTR e CDF" | (não) | — |

Transições faladas: 0→1 "Vamos começar pelo manifesto"; 1→2 "Antes do primeiro manifesto"; 2→3 "Com a frota pronta"; 3→4 "Hora de
emitir"; 4→5 "À tarde, a carga foi entregue"; 5→6 "Agora, a nota de serviço"; 6→7 "Vou cobrar a coleta"; 7→8 "E quando é a Recicla
Vale que contrata"; 8→9 "Antes de mandar o mês pro contador"; 9→10 "Agora, o estoque fiscal"; 10→11 "Agora, o pacote"; 11→12 "E o
que vai dentro dele".

**Cuidados (⚠️ da fonte), falados com "Uma dica:"**
| Cuidado | Onde | Fala (resumo) |
|---|---|---|
| Obrigatoriedade do MDF-e varia | cap01 | depende da operação e do estado; confirme com a contabilidade, principalmente entre estados; o sistema entrega a ferramenta |
| Contingência não é jeito normal | cap04 | só com a SEFAZ fora do ar; o motorista só sai com o PDF do manifesto impresso |
| Encerrar ≠ cancelar | cap05 | encerrar é o fim normal da viagem; cancelar anula o que não deveria existir, com prazo curto |
| Posição histórica é só consulta | cap10 | não muda saldo, nota, movimentação nem o estoque de hoje; a data é sempre do passado |
| Fiscal e operacional podem divergir | cap10 | o fiscal segue as notas; o operacional, compras, pedidos e pátio; um não corrige o outro (tela de comparação) |
| Guardar os XMLs é da empresa | cap12 | baixar o pacote todo mês e guardar cópia própria além da do contador |
Do código (não estão na fonte): peso sempre em quilos, a tela avisa se parecer tonelada (cap02); só chega NFS-e de cidade que entrou
no sistema nacional (cap08); cada NFS-e recebida conta na cota (cap08, na tela do diálogo).

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (a consolidar lá):
- **Endereços:** Serra Fina Alumínio Reciclagem em **Itamonte, MG** (o nome vem da Serra Fina, ali do lado); Recicla Vale em
  Taubaté, SP (`company_fiscal_config`: UF SP, cidade Taubaté, código IBGE de Taubaté, Inscrição Municipal preenchida, certificado
  "configurado" no falso).
- **Frota (base, desde a pesagem):** FKD2E41 "Caminhão truck", GHT7B19 "Caminhão 3/4", EZR4C63 "Picape", só com placa e descrição;
  motoristas Edson Moura, Jair Lopes, Tiago Freitas só com nome e telefone ((12) 90000-xxxx).
  **Criado na tela (cap02):** FKD2E41 com UF de licenciamento SP, Tipo "Veículo único (truck, toco, utilitário)", rodado "Truck",
  carroceria "Aberta", tara 7.800 kg, capacidade 14.000 kg, 30 m³; Edson Moura com CPF **318.472.650-90**, CNH **04728193604**,
  categoria "C", validade 18/03/2029.
- **Duas NF-e de saída autorizadas hoje** (10/11, 08h05 e 08h12, com chave, ambiente produção do falso) para a **Serra Fina Alumínio
  Reciclagem**: alumínio perfil 3.200 kg × R$ 10,40 = **R$ 33.280,00** e alumínio bloco 2.600 kg × R$ 8,50 = **R$ 22.100,00**
  (soma **R$ 55.380,00**, **5.800 kg**; itens em kg). Números: os dois seguintes aos que o T16 usar.
- **MDF-e:** nenhum antes; `last_mdfe_number` 0, série 1. **Criado na tela:** MDF-e **nº 1** (cap04, autorizado ~08:40), encerrado no
  cap05 (14:2x).
- **NFS-e:** série configurada; emitidas antes: **nº 12** (13/10, Fundição Bandeira do Vale, coleta com caçamba, R$ 1.200,00,
  "Autorizada") e **nº 13** (29/10, Aços Quiririm Ltda, R$ 1.850,00, "Autorizada"). **Criada na tela:** **nº 14** (emitida em 10/11, competência
  07/11/2026, Aços Quiririm Ltda, "Coleta e remoção de resíduos metálicos com caçamba no pátio da Aços Quiririm em 07/11/2026.",
  R$ 1.850,00).
  Lista de códigos de Taubaté (simulada) com o de coleta e remoção de resíduos (subitem 7.09 da lista nacional) e alíquota **3,00%**.
- **NFS-e recebidas:** recurso **desligado** no início (`nfse_dfe_ativo` false). A sincronização traz duas, tomador = Recicla Vale:
  **Contabilidade Jequitibá Ltda** (CNPJ **47.291.836/0001-56**, Taubaté), "Honorários contábeis de outubro de 2026", competência
  10/2026, emissão 05/11/2026, **R$ 1.650,00**; **Balanças Tremembé Manutenção Ltda** (CNPJ **39.506.417/0001-66**, Tremembé),
  "Aferição e manutenção preventiva da balança rodoviária", competência 11/2026, emissão 07/11/2026, **R$ 980,00** (ISS não retido).
  Nenhum dos dois é fornecedor cadastrado. **Criado na tela:** conta a pagar "Balanças Tremembé Manutenção Ltda", R$ 980,00, vencimento
  20/11/2026, categoria de despesa **"Manutenção"** (ou a de manutenção que o mundo base tiver; conferir o nome exato).
  Conferir na semente que os nomes não são de empresas reais da região.
- **Outubro com notas (para relatório, estoque fiscal e exportação):** 12 NF-e de saída (**R$ 168.940,00**) e 9 de entrada
  (**R$ 97.315,00**), todas autorizadas, com XML e DANFE; **saldo R$ 71.625,00**; nenhuma pendente nem rejeitada; nenhum MDF-e em outubro.
  Saldo inicial fiscal em 01/08/2026 por material (base do cardécs). Entre fiscal e operacional, em outubro, **só o metal amarelo
  diverge**: NF-e de saída de **30/10** para a Fundição Bandeira do Vale, **600 kg** × R$ 31,90 = R$ 19.140,00, com o pedido finalizado
  só em **03/11** (Delta **−600 kg**); os demais materiais com movimento fecham em zero. A casar com o histórico operacional do mundo
  (T10, T15).

## Gravação
- **Rotas:** `/fiscal-ambiental/transporte`, `/fiscal-ambiental/transporte/frota`, `/fiscal-ambiental/nfse`,
  `/fiscal-ambiental/nfe/recebidas-nfse`, `/fiscal-ambiental/nfe/saida`, `/fiscal-ambiental/estoque-fiscal/relatorio`, `/posicao`,
  `/historico`, `/comparacao`. Sempre entrando pelo menu "Fiscal & Ambiental" quando a câmera precisa mostrar o caminho.
- **Tabelas:** `vehicles`, `drivers`, `mdfe_manifests`, `mdfe_invoices`, `invoices`, `invoice_items`, `company_fiscal_config`,
  `nfse_invoices`, `nfse_invoice_services`, `customers`, `inbound_nfse`, `financial_bills`, `nfe_events`, `nfe_inutilized_numbers`.
- **RPCs:** `mdfe_contingency_availability` (devolver disponível, para não aparecer "Contingência indisponível"), `get_invoice_dashboard`,
  `get_fiscal_inventory_position`, `get_fiscal_inventory_position_at`, `get_fiscal_inventory_history_paged`,
  `get_fiscal_inventory_report_data`, `get_inventory_report_data`, `count_invoices_for_export`; gatilho que numera o MDF-e.
- **Edges a simular:** `plugnotas-mdfe-emit` (→ "aguardando_sefaz" com `plugnotas_id`), `plugnotas-mdfe-status` (na 1ª ou 2ª consulta:
  autorizado, com chave e protocolo; depois do encerrar: encerrado), `plugnotas-mdfe-enclose` (→ `encerramento_pendente`, sem
  `confirmed`), `plugnotas-mdfe-download` (PDF/XML falsos, também para a exportação), `plugnotas-nfse-servicos-municipio`,
  `plugnotas-emit-nfse` (→ "processando"), `plugnotas-nfse-status` (→ "emitida", nº 14), `plugnotas-enable-nfse-dfe`,
  `plugnotas-nfse-dfe-sync` (→ `synced: 2`), `plugnotas-download` (DANFEs da exportação). Storage `nfe-danfes` com os PDFs de outubro.
- **Fora do app:** a lista de cidades vem da API do IBGE no navegador (`servicodados.ibge.gov.br/.../estados/{UF}/municipios`): o robô
  precisa de resposta local para SP e MG (Taubaté e Itamonte com os códigos reais).
- **Download:** o ZIP da exportação é gerado no navegador ("Exportação Contábil - Recicla Vale Metais - <período>.zip"); o robô só
  deixa o download acontecer (sem abrir o arquivo). O conteúdo aparece na ilustração do cap12.
- Sem celular, sem página pública, sem outro usuário, sem cena de Windows.
- **Ilustrações (7):** cap00 o dia da Recicla Vale; cap01 o manifesto; cap03 o percurso; cap05 encerrar × cancelar; cap06 mercadoria
  × serviço; cap10 fiscal × operacional; cap12 o pacote e o contador (três quadros). Estilo da marca (`docs/09-aula-ilustrada.md`),
  rótulos reais do app, sem tela inventada e sem logo de terceiros (mapa simplificado, sem marca de mapa).
