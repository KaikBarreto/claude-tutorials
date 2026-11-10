# Plano · T16 · Nota Fiscal de mercadoria (NF-e)

- **Título:** Nota Fiscal de mercadoria (NF-e) (o da fonte). 🔒 módulo **Notas Fiscais** (`notas_fiscais`).
- **Objetivo:** do certificado digital até a nota autorizada, na ordem da tela, e o que vem depois: cancelar, corrigir,
  inutilizar, baixar, receber e manifestar.
- **Antes:** Relatório Financeiro e DRE (T15). **Próximo:** Transporte, serviço e o contador (T17).
- **Regime do exemplo:** Lucro Real (Kaik, 10/11). A fala mostra os campos e diz que quem define é o contador; nenhum
  valor de imposto é explicado. **Emissão simulada:** não há SEFAZ, provedor, cota real nem numeração a queimar.
- **Duração:** alvo da fonte ~25 min; fala de ~18,3 min (2.858 palavras) e ~22 min de vídeo com as vinhetas e as esperas (`roteiro.md`).
- Base: `inventario.md` (código 1.59.154). Usuário logado: Rafael Nogueira (MASTER), desktop 1280×800, tema claro.
  `FAKE_NOW=2026-11-10T08:30:00-03:00`; todos os capítulos no mesmo dia, em ordem.

## Capítulos (os da fonte, na ordem)

| cap | Vinheta (área / título) | O que se mostra | Estado de partida |
|---|---|---|---|
| 00 | sem vinheta | Abertura: o problema (a carga de cobre só sai com nota), 🔒, "Antes: Relatório Financeiro e DRE". [ILUSTRAÇÃO: carga e nota] | `inicio` |
| 01 | FISCAL / Onde ficam as notas | Menu "Fiscal & Ambiental" → "Notas Fiscais (NF-e)"; sub-abas "Entrada", "Saída", "Notas Recebidas", "Inutilizadas"; "Configurações Fiscais", selo da cota, cartões, "Nova Nota". [ILUSTRAÇÃO: entrada × saída] | `inicio` |
| 02 | CONFIGURAÇÃO / O certificado vem primeiro | "Configuração Fiscal": trilho com Empresa, Impostos, Numeração e Transportadora apagados ("precisa do certificado digital"); "Passo 1 de 3". [ILUSTRAÇÃO: o certificado assina a nota; passos 1, 2, 3] | `inicio` |
| 03 | CERTIFICADO / Subindo o certificado A1 | "Selecionar arquivo" (.pfx), "Senha do Certificado", "Validar Certificado" → "Certificado validado!", "Válido até 14/09/2027"; dica da validade. [ILUSTRAÇÃO: régua de um ano] | `inicio` |
| 04 | CONFIGURAÇÃO / Empresa e impostos | "Empresa": "Importar dados", Razão Social, IE; "Impostos (padrão)": "Lucro Real" e o quadro, ICMS, CFOPs Padrão, "Reforma Tributária (IBS/CBS)"; "Salvar configuração" → "Empresa cadastrada no sistema de NF-e!". [ILUSTRAÇÃO: o padrão vale para toda nota] | `apos-cap03` |
| 05 | CENÁRIOS / Cenários fiscais | Aviso fixo; "Criar o primeiro cenário": "Venda para a Fundição Bandeira do Vale" (Venda, cliente específico); "O que aplicar" como o contador passou; "Criar cenário". [ILUSTRAÇÃO: regra geral × exceção estreita] | `apos-cap04` |
| 06 | NUMERAÇÃO / Série e numeração | "Série padrão das suas notas"; "Adicionar série": Série 1, última 1248 → "Série adicionada com sucesso". [ILUSTRAÇÃO: a sequência continua] | `apos-cap05` |
| 07 | CONFIGURAÇÃO / Transportadora e serviços | "Nova transportadora": Cargas Vale do Sol Ltda + placa FJR3B27 → "Transportadora cadastrada!"; "Serviços" vazio (é da NFS-e, T17). [ILUSTRAÇÃO: os dados do caminhão vão na nota] | `apos-cap06` |
| 08 | COTA / A cota de documentos | Selo "0/1.000 Documentos" e a dica do mouse (a fala não diz a cota: depende do plano); o que conta; tolerância de 5. [ILUSTRAÇÃO: a barra da cota] | `apos-cap07` |
| 09 | EMISSÃO / Nota avulsa, do zero | "Nova Nota" → "NF-e de Saída" → Dados (Serra Fina, "Venda de mercadorias", Série 1 / Nº 1249) → Itens (Alumínio perfil 320 kg) → "Emitir Nota" → "Aguardando SEFAZ" → "Autorizada"; "Visualizar": chave e protocolo. [ILUSTRAÇÃO: o caminho da nota] | `apos-cap07` |
| 10 | EMISSÃO / Nota a partir de um pedido | "Importar de" → "Pedido" → venda de ontem (09/11) à Fundição (Cobre mel, 500 kg líquidos) → Transporte (Cargas Vale do Sol) → nº 1250 autorizada. [ILUSTRAÇÃO: bruto, desconto e líquido] | `apos-cap09` |
| 11 | EMISSÃO / Nota de um caixa fechado | "NF-e de Entrada" → "Emissão em Massa (Caixa)" → "Por Caixa", 09/11, caixa do Marcos "Fechado" → "Uma nota consolidada" → "Montar nota consolidada" → nº 1251 autorizada. [ILUSTRAÇÃO: várias compras viram uma nota] | `apos-cap10` |
| 12 | CORREÇÕES / Cancelar e corrigir | Cancelar a 1249 (a Serra Fina mudou o pedido antes de a carga sair; a carga grande sai na T17) → "Cancelada"; "Carta de Correção" na 1250 (troca da placa) → "Carta de Correção enviada com sucesso!". [ILUSTRAÇÃO: cancelar × corrigir] | `apos-cap11` |
| 13 | NUMERAÇÃO / Inutilizar numeração | Três pontinhos → "Inutilizar numeração" → "Por Faixa" 1246 a 1247 (puladas em outubro) → "Inutilizar na SEFAZ"; sub-aba "Inutilizadas". [ILUSTRAÇÃO: números fechados com cadeado] | `apos-cap12` |
| 14 | DOCUMENTOS / DANFE e XML | Menu da 1250: "Download DANFE" (PDF em aba nova), "Download XML"; na 1249, "XML de Cancelamento". [ILUSTRAÇÃO: DANFE viaja com a carga, XML vai pro contador] | `apos-cap13` |
| 15 | NOTAS RECEBIDAS / As notas recebidas | "Notas Recebidas" → "Ativar Notas Recebidas" → "Ativar mesmo assim" → "Notas emitidas contra o seu CNPJ" (Auto Peças Vale Forte e Depósito Irmãos Siqueira). [ILUSTRAÇÃO: o fornecedor emite contra o seu CNPJ] | `apos-cap14` |
| 16 | NOTAS RECEBIDAS / Manifestar a nota | Selo "Ciência"; "Buscar documento"; "Confirmar operação" na Auto Peças → "Confirmada"; "Desconhecer operação" e "Operação não realizada" só mostrados. [ILUSTRAÇÃO: as respostas possíveis] | `apos-cap15` |
| 17 | NOTAS RECEBIDAS / Importar pelo XML | "Importar nota" → "Arquivo XML" (Cooperativa Recomeço, nº 3871) → "Nota importada"; "Lançar compra…" → casamento: "alta" e "confira". [ILUSTRAÇÃO: nome do XML × material do cadastro] | `apos-cap16` |
| 18 | RESUMO / Recapitulando | Montagem do que foi feito; "Próximo: Transporte, serviço e o contador"; "Até lá!" | (trechos) |

Transições faladas: 01→02 "Antes de qualquer nota, a configuração"; 02→03 "Então, o certificado"; 03→04 "Com o
certificado validado, os dados da empresa"; 04→05 "E quando uma venda não segue o padrão?"; 05→06 "Agora, de qual
número a primeira nota sai"; 06→07 "Mais dois cadastros"; 07→08 "Antes de emitir, a cota"; 08→09 "Agora sim, a primeira
nota"; 09→10 "Quase sempre a nota nasce de uma venda que já está no sistema"; 10→11 "E as compras do dia, de quem não
emite nota?"; 11→12 "Nota emitida, e se algo mudar?"; 12→13 "E o número que nunca virou nota?"; 13→14 "Agora, os
arquivos da nota"; 14→15 "Até aqui, as notas que a Recicla Vale emite. Agora, as que ela recebe"; 15→16 "Chegou a nota,
e agora?"; 16→17 "E a nota que ainda não apareceu na lista?".

**Cuidados (⚠️) e o que não acontece (🚫), falados como na PERFIL:**

| Fonte | Onde | Fala (resumo) |
|---|---|---|
| ⚠️ ordem e contador | 02 | "Uma dica: faça essa configuração junto com o contador..." |
| ⚠️ validade estranha | 03 | "Uma dica: o A1 vale no máximo um ano..." (sem encenar o arquivo errado) |
| ⚠️ IBS/CBS | 04 | O cartão "Reforma Tributária (IBS/CBS)" e os códigos do contador. Sem datas (o aviso do topo não existe na 1.59.154) |
| ⚠️ impresso na nota / específico vence | 05 | o aviso fixo lido; "Uma dica: não precisa um cenário por combinação..." |
| ⚠️ cota | 08 | o que conta, a tolerância de 5, cancelada conta, recebida só depois de ativar |
| ⚠️ credenciamento | 09 | "Uma dica: antes da primeira nota, confirme com o contador o credenciamento..." |
| ⚠️ enviado ≠ autorizado | 09 | "Uma dica: enviada para processamento ainda não é autorizada..." |
| ⚠️ líquido, não bruto | 10 | "Uma dica: quando o cliente disser que o peso da nota não bate com o ticket..." |
| ⚠️ nome sem acento no XML | fora | não conferível no código (inventário 14.2); fica de fora |
| 🚫 ciência | 16 | "A ciência não é um botão: ela já vem sozinha. Pra baixar, é Buscar documento." |

## Mundo: o que esta aula precisa (além do `MUNDO_FICTICIO.md`)

**Começa com (`inicio`, fim do T15):** módulo `notas_fiscais` ligado; **nenhum** certificado, `company_fiscal_config` sem
razão social nem regime (ou sem linha), `nfe_series`, `transportadoras`, `fiscal_scenarios` e `invoices` vazios; Notas
Recebidas desligado (`dfe_ativo` false); `companies.nfe_tier` 1. Endereço da empresa completo em Configurações › Empresa
(T1), com o código IBGE de Taubaté (3554102). `companies.name` "Recicla Vale Metais", telefone e e-mail `.example`.

| Item | Valores (fictícios) |
|---|---|
| Níveis (`nfe_module_tiers`) | o catálogo do app (junção, item 6): "Nível 1" 1.000 documentos/mês, "Nível 2" 3.000, "Nível 3" 5.000 (preço na tabela, nunca na tela); a empresa no Nível 1 (`useNfeTier.tsx`: tolerância de 5; âmbar a partir de 80 %; o selo `0/1.000 Documentos`). A fala não diz a cota |
| Certificado (cap 03) | arquivo `recicla-vale-metais-a1.pfx` (bytes falsos, < 200 KB), senha fictícia digitada mascarada; `plugnotas-certificate-info` devolve `certificateName` "RECICLA VALE METAIS LTDA", `vencimento` 2027-09-14, `daysRemaining` 308 |
| Empresa (cap 04) | Razão Social "Recicla Vale Metais Ltda", Nome Fantasia "Recicla Vale Metais", CNPJ da semente, **IE 688.047.314.106** (SP, dígitos válidos) |
| Impostos (cap 04) | "Lucro Real" (o quadro preenche PIS 1,65, COFINS 7,6, CST 01, não cumulativo); "Contribuinte de ICMS" ligado, ICMS interno 18 (padrão), CST e CFOPs no padrão da tela (1102, 2102, 5102, 6102, 5101, 5502); IBS/CBS ligado com CST-IBS/CBS 000 e cClassTrib 000001 em Saída e Entrada ("o que o contador passou") |
| Cenário (cap 05) | "Venda para a Fundição Bandeira do Vale": Operação "Venda"; "Cliente da nota" "Um cliente/fornecedor específico" = CNPJ da Fundição; o resto "Qualquer"; "CST do ICMS" 51 e "Diferimento (%)" 100 (do contador; a fala não lê os números) |
| Série (cap 06) | Série 1, "Última nota emitida nessa série" 1248 (a Recicla emite pelo EcoSistema desde agosto; a semente desta aula tira a configuração fiscal e as notas para mostrar a configuração do zero); a próxima é 1249. Em outubro, o "Última nota emitida" da série foi acertado errado (1247 em vez de 1245; o número da nota não se digita na emissão) e a 1248 saiu depois da 1245: 1246 e 1247 nunca viraram nota (cap 13) |
| Transportadora (cap 07) | **Cargas Vale do Sol Ltda**, CNPJ **41.826.537/0001-92**, IE **688.115.922.408**, SP, Rua dos Ferroviários, 380, Vila São José, Taubaté; placa **FJR3B27**, UF SP (conferir na semente que o nome não é de empresa real) |
| Clientes | Serra Fina Alumínio Reciclagem e Fundição Bandeira do Vale: PJ em SP, CNPJ e IE válidos, endereço completo, cadastro fiscal completo (sem selo "Incompleto") |
| Venda (cap 10) | pedido de venda de **ontem, 09/11 10:40** (junção: o T6 não tem caixa aberto em 10/11 antes das 08:31), no caixa #84 do Rafael, Pix na Conta Secundária, Fundição Bandeira do Vale, Cobre mel: bruto 506 kg, tara e impureza 6 kg, **líquido 500 kg × R$ 47,90 = R$ 23.950,00**, sem nota |
| Caixa fechado (cap 11) | caixa do **Marcos Antunes de 09/11** (segunda), aberto 07:02, **Fechado**, com 3 compras sem nota de pessoa física: Dona Cida (Alumínio latinha 38 kg, Papelão 120 kg), Valdir Pereira (Ferro misto 410 kg), Dona Cida (Alumínio latinha 26 kg, Papelão 60 kg). Consolidado: latinha 64 kg (R$ 396,80), papelão 180 kg (R$ 99,00), ferro misto 410 kg (R$ 307,50) = **R$ 803,30**, 3 itens. Se o histórico do Mundo já tiver esse caixa, usar o dele e ajustar a fala |
| Notas emitidas | 1249 Serra Fina, Alumínio perfil 320 kg × R$ 10,40 = **R$ 3.328,00**, CFOP 6102 (Serra Fina em Itamonte, MG); 1250 Fundição, Cobre mel 500 kg = R$ 23.950,00, frete "0 - Frete por conta do Remetente (CIF)", Cargas Vale do Sol (FJR3B27); 1251 entrada, Consumidor Final, "Entrada de sucata para revenda (pessoa física)", R$ 803,30. Chave de 44 dígitos: `35` + `2611` + CNPJ + `55` + `001` + número com 9 dígitos + `1` + código de 8 dígitos + DV (módulo 11); protocolo de 15 dígitos (`13526000…`); `authorized_at` no mesmo dia |
| Cancelamento (cap 12) | 1249, motivo "Pedido alterado pelo cliente antes de a mercadoria sair do pátio" |
| CC-e (cap 12) | 1250: "Onde se lê 'Placa FJR3B27', leia-se 'Placa GKM5D18'. A transportadora trocou o veículo da carga." |
| Inutilização (cap 13) | Série 1, ano 2026, 1246 a 1247, justificativa "Numeração pulada na emissão de outubro e não utilizada" |
| Notas recebidas (cap 15) | Auto Peças Vale Forte, NF-e nº 2157 de 05/11, "SUCATA DE BATERIA AUTOMOTIVA" 640 kg × R$ 3,10 = R$ 1.984,00 (a compra de 05/11, Pix da Conta Secundária); Depósito Irmãos Siqueira, nº 884 de 06/11, "FERRO PESADO" 1.200 kg × R$ 0,95, "FERRO MISTO" 320 kg × R$ 0,75 e "COBRE MISTO" 20 kg × R$ 36,00 = R$ 2.100,00 (a compra no saldo do T4). As duas "Autorizada", manifestação "Ciência", com XML |
| XML importado (cap 17) | `NFe-3871-Cooperativa-Recomeco.xml`: Cooperativa Recomeço (CNPJ da semente), nº 3871 de 09/11, "ALUMINIO LATINHA" 850 KG × 6,20 e "PLASTICO PET PRENSADO" 1.200 KG × 1,90 = R$ 7.550,00 (dá "alta" e "confira" pela regra do inventário 13) |

**Fica para as próximas:** as três notas (1249 cancelada, 1250 com CC-e, 1251), a série em 1251, a transportadora, o
cenário, Notas Recebidas ligado com as três notas (a da Auto Peças confirmada). O T17 parte daqui (MDF-e da carga da 1250,
NFS-e, pacote do contador). Atualizar o `MUNDO_FICTICIO.md`.

## Gravação

- Rotas: `/dashboard` (entrada pelo menu), `/fiscal-ambiental/nfe/entrada`, `/saida`, `/recebidas`, `/inutilizadas`,
  `/fiscal-ambiental/configuracao/certificado`, `/empresa`, `/impostos`, `/cenarios`, `/numeracao`, `/transportadora`,
  `/servicos`.
- Edge functions a simular (todas fiéis ao formato do código): `plugnotas-upload-certificate` (sucesso, `vaultStored`
  true), `plugnotas-certificate-info`, `plugnotas-register-company` ("Empresa cadastrada no sistema de NF-e!"),
  `ibge-cities` (só se faltar IBGE), `plugnotas-emit` (sucesso com `plugnotasId`), `plugnotas-status` (troca para
  `emitida` em ~5 s, com chave, protocolo e `authorized_at`), `plugnotas-cancel` (`confirmed` true), `plugnotas-cce`
  (envio e status `CONCLUIDO`), `plugnotas-inutilize` (sucesso; grava `nfe_inutilized_numbers`), `plugnotas-download`
  (PDF de DANFE fictício com os dados da nota, XML da nota e XML de cancelamento), `plugnotas-enable-dfe`,
  `plugnotas-dfe-sync`, `plugnotas-manifestar` (sem fila: "Operação confirmada junto à SEFAZ").
- RPCs/tabelas: `certificate_vault_status`, `count_fiscal_documents_in_month` (0 no cap 08), `get_invoices_paged` (inclui
  as inutilizadas de `nfe_inutilized_numbers` com `p_include_inutilizadas`), `dfe_inbound_import_enqueue` e a fila de jobs
  do import (fica "succeeded" em ~3 s), `company_fiscal_config`, `fiscal_scenarios`, `nfe_series`, `transportadoras`,
  `invoices`, `invoice_items`, `invoice_orders`, `nfe_module_tiers`, notas recebidas (`useInboundNfe`).
- Arquivos para o seletor de arquivo (o robô preenche o `input type=file`, sem janela do sistema): o `.pfx` falso e o XML
  da Cooperativa (XML de NF-e válido no esquema, dados fictícios).
- "Download DANFE" abre aba nova com o PDF: gravar a aba (como o comprovante em PDF do T7) ou cortar para ela.
  "Download XML" baixa arquivo: a câmera fica na tela do app.
- Sem celular, sem página pública, sem outro usuário. Sem cena de Windows.
- **Ilustrações** (cena HTML no estilo da marca, `docs/09-aula-ilustrada.md`; objetos genéricos, sem logo de terceiros, sem
  imitar tela do app): 00 carga e nota; 01 entrada × saída; 02 o certificado assina, passos 1-2-3; 03 régua de um ano; 04 o
  padrão em toda nota; 05 geral × estreita; 06 a sequência continua; 07 o caminhão na nota; 08 a barra da cota; 09 o caminho
  da nota (base: os 4 passos de `EmissionFlowTimeline.tsx`); 10 bruto, desconto, líquido; 11 várias compras, uma nota; 12
  cancelar × corrigir; 13 números com cadeado; 14 DANFE e XML; 15 a nota chega pela SEFAZ; 16 as respostas; 17 o
  casamento. Detalhe de cada uma na coluna Tela do roteiro.

## Pronúncias
- Da tabela do PERFIL (versão de 10/11 01:20): NF-e e ICMS em IPA (`/ˈẽniˈɛfiˈe/`, `/iˈseˈɛmiˈɛːsːi/`), NFS-e em IPA
  provisório (`/ˈẽːniˈɛːfiˈɛːsiˈeː/`, teste 8 do Kaik), SEFAZ "sefás", CFOP "cê-éfe-ó-pê", DANFE "dânfi", NCM, XML, PDF,
  MTR, CDF, DRE e EcoSistema como na tabela. Se o PERFIL mudar de novo, é só rodar o gerador outra vez: ele lê a config
  do perfil.
- Novas desta aula (testar num trecho curto antes da voz): **CC-e** "cê-cê-ê", **A1** "á-um", **pfx** "pê-éfe-xis"
  (dito "ponto pfx"), **IBS** "i-bê-ésse", **CBS** "cê-bê-ésse", **Fiscal & Ambiental** "Fiscal e Ambiental".
- Ditas por extenso, sem troca: PIS, COFINS, CNPJ, PET. Evitadas na fala: MDF-e (vira "manifesto de transporte"), DF-e,
  cClassTrib, RNTC, CST.
- Gerador: `T16_gera_tts.py` (na pasta T16 do scratchpad) lê o `roteiro.md` e a config do perfil (só leitura) e escreve
  `narracao/tts_textos.py` e `narracao/config_narracao.json` (37 trocas, 28 números para a legenda).

## Riscos e decisões para o Kaik
1. **Cancelar a 1249** (a Serra Fina mudou o pedido antes de a carga sair) e **CC-e da placa na 1250**: os dois são casos
   comuns e não encenam erro do sistema. Alternativa: cancelar uma nota extra criada só para isso.
2. **Inutilizar 1246 e 1247** (puladas em outubro, por um acerto errado do último número da série): é o único caso de inutilização que não
   exige encenar uma recusa na gravação. Alternativa: semear uma nota "Rejeitada" e usar "Inutilizar Rejeitadas".
3. **Cenário da Fundição com CST 51 e diferimento 100**: valores "do contador", sem explicação na fala. Alternativa:
   cenário só com texto nas informações complementares.
4. **IBS/CBS preenchido com 000 / 000001** (o exemplo da própria tela): sem falar de datas nem de obrigatoriedade.
5. **"Conferir na tela de compra" não é clicado** no cap 17 (a tela de Compra pede caixa aberto, assunto do T7): a fala diz
   o que o botão faz, com o texto da própria dica.
6. "Cancelado continua contando na cota" vem da fonte; a RPC não está na cópia (inventário 14.3).
