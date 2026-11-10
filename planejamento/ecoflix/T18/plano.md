# Plano · T18 Ambiental: MTR e CDF

- **Título:** Ambiental: MTR e CDF (fonte). 🔒 módulo **Notas Fiscais** (dito na abertura, sem preço).
- **Antes:** T17 Transporte, serviço e o contador. **Próximo:** T19 Funcionários e ponto eletrônico ("a equipe do pátio dentro
  do sistema").
- **Áreas das vinhetas:** AMBIENTAL · CONFIGURAÇÃO · MTR · CDF · NOTA FISCAL · RESUMO.
- **Alvo da fonte:** ~12 min. **Estimativa:** ~10,5 min de vídeo (1.403 palavras, ~9,0 min de fala, + 10 vinhetas e as esperas).
- Tudo simulado: nenhum acesso real ao SIGOR (órgão ambiental de SP) nem à SEFAZ. A fala mostra os campos e diz que quem define a
  obrigação e a classificação é o órgão ambiental e a licença da empresa; não ensina norma. Regime do exemplo Lucro Real (não aparece).
- Base: `T18/inventario.md` (código 1.59.154). Desktop, logado como **Rafael Nogueira** (MASTER).
- **FAKE_NOW:** `2026-11-10T09:30:00-03:00` nos capítulos 0 a 5 (junção: depois das NF-e do T16 e do T17); **corte** para `2026-11-10T10:40:00-03:00` do 6 ao 10 (o MTR da
  carga da tarde já foi emitido, fora do vídeo). Mesma terça do T17: a carga aqui usa o **GHT7B19 com o Jair Lopes**, porque o
  FKD2E41 e o Edson estão na viagem a Itamonte do T17.
- **Os dois papéis da Recicla Vale** (é o que a ilustração do cap01 explica): no MTR ela é a **geradora** (manda chaparia para a
  Aços Quiririm reciclar); no CDF ela é a **destinadora** (recebeu as sucatas da Auto Peças Vale Forte em outubro e certifica o destino).

## Capítulos (os da fonte, na ordem)
| # | Vinheta (área / título) | O que se mostra | Ilustração | Estado de partida |
|---|---|---|---|---|
| 0 | (sem vinheta) | Abertura; menu "Fiscal & Ambiental" › "Ambiental (MTR/CDF)"; 🔒; "Antes" | o dia: a chaparia sai, a Auto Peças espera o certificado | `inicio` |
| 1 | AMBIENTAL / O que é MTR e CDF | abas "MTR" e "CDF"; ⚠️ a ordem no tempo | a cadeia do resíduo (gerador, transportador, destinador) com a Recicla Vale nos dois papéis; a linha do tempo MTR → baixa → CDF | `inicio` |
| 2 | AMBIENTAL / Licença e fiscalização | "Novo MTR" ainda bloqueado; ⚠️ "eu sou obrigado?" | a licença, o órgão e a fiscalização pedindo MTR e CDF | `inicio` |
| 3 | CONFIGURAÇÃO / Acesso e resíduos | ⚠️ UF + acesso antes de emitir; "Configurações": acesso ao SIGOR (⚠️ credencial do próprio usuário), sincronizar, "Novo resíduo" "Sucata de ferro" (unidade "TON - Tonelada"); Materiais: "Definir resíduo do MTR" nos três ferros | (não) | `inicio` |
| 4 | MTR / Emitir o MTR da carga | "Novo MTR": transportador e destinador cadastrados na hora, Jair + GHT7B19, "Puxar da nota fiscal" (3,6 TON), responsável; "MTR emitido" nº 2611000318; ⚠️ cota | (não) | `apos-cap03` |
| 5 | MTR / Acompanhar e baixar o PDF | a linha "Emitido"; "Ver tentativas"; "Baixar PDF"; "Usar como modelo" | o PDF do MTR vai com o motorista | `apos-cap04` |
| 6 | MTR / Cancelar um MTR | corte 10:40: o MTR da tarde (nº 2611000325) "Cancelar MTR" → "Cancelado"; ⚠️ cancelado conta na cota | (não) | `apos-cap05` (10:40) |
| 7 | CDF / O certificado do destino | "Novo CDF" de outubro para a Auto Peças Vale Forte com três MTR; "CDF emitido"; a lista por status | três cargas de outubro chegando, baixa no SIGOR, um CDF do mês | `apos-cap06` |
| 8 | CDF / Baixar e guardar | "Ações" › "Baixar PDF"; ⚠️ documento de fiscalização | o PDF na pasta da licença, com os MTR do período | `apos-cap07` |
| 9 | NOTA FISCAL / A nota da mesma carga | a NF-e da chaparia em Notas Fiscais › "Saída"; 🚫 documentos independentes; o que o MTR aproveita | três faixas: NF-e, MTR, CDF da mesma carga | `apos-cap07` |
| 10 | RESUMO / Recapitulando | montagem; "Próximo: Funcionários e ponto eletrônico" | (não) | — |

Transições faladas: 0→1 "Primeiro, o que é cada um"; 1→2 "Por que isso importa"; 2→3 "Antes do primeiro MTR"; 3→4 "Hora de emitir";
4→5 "Com o MTR emitido"; 5→6 "Mais tarde"; 6→7 "Agora, o outro lado"; 7→8 "Com o certificado emitido"; 8→9 "E como tudo isso conversa
com a nota fiscal?".

**Cuidados (⚠️ da fonte), falados com "Uma dica:"; 🚫 no positivo**
| Cuidado | Onde | Fala (resumo) |
|---|---|---|
| A ordem no tempo | cap01 | primeiro o MTR, com a carga; depois do recebimento e da baixa, o CDF, que cobre um período e junta os MTR; um não substitui o outro |
| "Eu sou obrigado?" | cap02 | quem define é o órgão ambiental do estado e a licença da empresa; o sistema entrega a ferramenta |
| UF + acesso antes de emitir | cap03 | o estado nas Configurações Fiscais e o acesso ao sistema ambiental; com os dois, o "Novo MTR" libera |
| SIGOR: credencial do próprio usuário; unidade "SIGLA - Nome" | cap03 | CPF da pessoa cadastrada e a senha do portal; a unidade aparece como o órgão escreve ("TON - Tonelada"), escolhida na lista |
| Cota compartilhada; cancelado continua contando | cap04 e cap06 | MTR e CDF contam na cota das notas; o cancelado também; conferir perto do fim do mês |
| CDF é documento de fiscalização | cap08 | guardar o PDF fora do sistema, na pasta da licença, com os MTR do período |
| 🚫 MTR, CDF e NF-e independentes | cap09 | cada um na sua tela; o MTR aproveita os itens (Puxar da nota fiscal) e a chave da nota |
Do código: "Cancelar MTR" só no emitido e é irreversível (cap06); o CDF só junta MTR já recebido no SIGOR e é definitivo (cap07).

## Mundo: o que esta aula precisa
Além do `MUNDO_FICTICIO.md` (a consolidar lá):
- **Ambiental:** `company_fiscal_config.uf` SP; `mtr_uf_sistema` SP → `sigor_sp`; `mtr_sistemas` `sigor_sp` ativo, `auth_mode`
  senha, `protocolo` sinir (libera o CDF e a lista de classes por resíduo), nome igual ao do banco de produção (aparece em
  "Sistema:"). **Sem** `mtr_credentials`, sem resíduo salvo, sem `mtr_parceiros`, sem MTR e sem CDF no início.
- **Acesso criado na tela (cap03):** CPF do Rafael Nogueira **274.913.508-79**, senha fictícia (só pontinhos na tela), código da
  unidade geradora **203918**, ambiente "Produção".
- **Listas do órgão (resposta do `sigor-mtr-sync-ref` falso):** resíduos do IBAMA com o de **metais ferrosos** (sugestão "19 12 02",
  conferir na lista oficial), classes (com a da licença para ele), estados físicos (com "Sólido"), acondicionamentos (com o de
  granel), tratamentos (com "Reciclagem"), unidades no formato do órgão: "TON - Tonelada", "KG - Quilograma", "UN - Unidade",
  "Lt - Litro", "M³ - M³".
- **Resíduo salvo criado na tela:** "Sucata de ferro" (metais ferrosos, sólido, granel, reciclagem, "TON - Tonelada"); ligado em
  Materiais a **Ferro pesado, Ferro misto e Chaparia**.
- **NF-e da carga:** saída autorizada hoje (10/11, 09h20, com chave) para a **Aços Quiririm Ltda**: chaparia **3.600 kg** × R$ 0,98 =
  **R$ 3.528,00** (item em kg). Número **1254** (o seguinte aos do T17). Emitida sem pedido (o pedido fecha na entrega); o
  pátio tem 3.750 kg de chaparia em 10/11 08:30 (junção, `MUNDO_LINHA_DO_TEMPO.md`).
- **Parceiros criados na tela (cap04):** transportador **Recicla Vale Metais Ltda** (CNPJ da semente, unidade 203918) e destinador
  **Aços Quiririm Ltda** (CNPJ da semente, unidade **187402**).
- **MTR:** nº **2611000318** (cap04, Jair Lopes, GHT7B19, expedição 10/11/2026, 3,6 TON, responsável Rafael Nogueira, cargo
  "Sócio-administrador", chave da NF-e na observação), uma tentativa "Autorizada", PDF falso no storage. **Semente do corte (cap06):**
  nº **2611000325**, emitido às 09h40 pelo modelo, Aços Quiririm, sucata de ferro **3,2 TON** (ferro misto da tarde), Jair Lopes,
  GHT7B19, "Emitido"; cancelado na tela.
- **CDF:** a Auto Peças Vale Forte (CNPJ da semente, **unidade no SIGOR 184527**) mandou três cargas em outubro com MTR emitidos por ela:
  **2610001542** (06/10), **2610001877** (16/10) e **2610002203** (27/10), já recebidos e baixados no portal (fora do app). **Criado na
  tela:** CDF de 01/10/2026 a 31/10/2026, destinador Recicla Vale (CNPJ da semente, responsável Rafael Nogueira), gerador Auto Peças
  Vale Forte, os três MTR; nº **2611000041**, "Emitido", PDF falso.
- **Cota:** selo do cabeçalho verde (abaixo de 80%), com os documentos do mês do mundo; a fala não diz número.

## Gravação
- **Rotas:** `/fiscal-ambiental/ambiental/mtr`, `/fiscal-ambiental/ambiental/cdf`, `/materiais`, `/fiscal-ambiental/nfe/saida`.
- **Tabelas:** `company_fiscal_config`, `mtr_uf_sistema`, `mtr_sistemas`, `mtr_credentials`, `mtr_ref_*`, `mtr_residuo_presets`,
  `materials` (`mtr_residuo_preset_id`), `mtr_parceiros`, `mtr_manifests`, `mtr_manifest_items`, `mtr_manifest_attempts`, `mtr_cdf`,
  `drivers`, `vehicles`, `invoices`, `invoice_items`, `companies`.
- **RPC:** `mtr_set_credential`.
- **Edges a simular:** `sigor-mtr-sync-ref` (testar acesso → validado; sincronizar → listas acima; classes permitidas para o
  resíduo), `sigor-mtr-emit` (→ emitido, nº 2611000318, PDF), `sigor-mtr-cancel` (→ cancelado), `sigor-cdf-emit` (→ emitido,
  nº 2611000041, PDF). A lupa do CNPJ (`cnpj-lookup`) não é clicada.
- **PDF:** "Baixar PDF" abre o PDF em aba nova; o robô não grava a aba (a câmera fica no app) e o PDF do órgão não é desenhado como
  documento oficial: vira ilustração genérica (cap05 e cap08).
- Sem celular, sem página pública, sem outro usuário, sem cena de Windows.
- **Ilustrações (7):** cap00 o dia; cap01 a cadeia do resíduo e a linha do tempo; cap02 licença e fiscalização; cap05 o PDF com o
  motorista; cap07 as cargas de outubro e o CDF do mês; cap08 a pasta da licença; cap09 os três documentos da mesma carga. Estilo da
  marca (`docs/09-aula-ilustrada.md`), rótulos reais do app, sem tela inventada, sem brasão nem logo de órgão.
