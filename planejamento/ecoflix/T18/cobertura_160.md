# T18 · Ambiental: MTR e CDF · cobertura no 1.60.10

Base: roteiro e inventário do 1.59.154 contra o código em `/dev/shm/ecoflix-src` (1.60.10) e o `git diff f37573ea0 5290be4cd`.
Caminhos relativos a `src/` (edge functions em `supabase/functions/`). Sem varredura do robô para a T18 (só existem `t00` e `t01`).

Resumo do diff nas telas desta aula: só `NovoMtrModal.tsx` e `NovoCdfModal.tsx` mudaram (casca de tela cheia), mais o menu
(`config/routes.ts`) e a checagem de permissão nas duas edges de emissão. `MtrTab`, `MtrConfigCard`, `MtrResiduosSalvosCard`,
`MtrPuxarDaNotaDialog`, `MtrAttemptHistoryDialog`, `CdfTab`, `useMtr`, `useCdf` e o trecho de MTR em `Materiais.tsx` estão **iguais**.
Ou seja: quase tudo que falta cobrir já existia no 1.59.154 e ficou fora do roteiro.

## 1. Mudou no app

| Cap. | O que o roteiro mostra | Como está no 1.60.10 | Arquivo:linha |
|---|---|---|---|
| 00 | Menu "Fiscal & Ambiental" aberto, com "Ambiental (MTR/CDF)" | O menu ganhou um sexto item, "Relatórios Fiscais", logo abaixo de "Estoque Fiscal". "Ambiental (MTR/CDF)" continua no mesmo lugar e na mesma rota. Só muda o enquadramento do menu | `config/routes.ts:509-511` |
| 04 | "Novo MTR" como janela (diálogo de 90% da altura) com "Manifesto de Transporte de Resíduos." | Agora é **tela cheia** (`FiscalFullscreenWizard`). Cabeçalho: botão "Sair" à esquerda (não há X e a tecla Esc não fecha), título "Novo MTR", subtítulo "Informe o transporte, os resíduos e o responsável antes de emitir o manifesto.", e à direita "Documento" / "Manifesto de resíduos". Rodapé fixo com os botões à direita: "Cancelar" (ou "Voltar", agora com ícone) e "Avançar" / "Emitir MTR". As três etapas, o "Resumo do MTR" ao lado e todos os campos não mudaram | `notas-fiscais/mtr/NovoMtrModal.tsx:1246-1291`; `notas-fiscais/FiscalFullscreenWizard.tsx:53,60-70,128-130` |
| 07 | "Novo CDF" como janela, com "Certificado de Destinação Final." e bolinhas numeradas | Também **tela cheia**: "Sair", título "Novo CDF", subtítulo "Defina o período, o destinador e os manifestos que compõem o certificado.", à direita "Documento" / "Certificado ambiental". As cinco etapas viraram abas sublinhadas e **clicáveis** (número e nome; clicar pula direto, sem validar a etapa anterior). Campos, avisos e resumo iguais | `notas-fiscais/cdf/NovoCdfModal.tsx:377-432`; `:427` |
| 04, 07 | (backend falso) emissão sem checar permissão de ação | As edges agora recusam quem não tem a ação `action_emit_ambiental`: "Seu usuário não tem permissão para emitir MTR." / "Seu usuário não tem permissão para emitir CDF." Não afeta o Rafael (MASTER); só importa se for gravado o trecho de permissão | `sigor-mtr-emit/index.ts:458-467`; `sigor-cdf-emit/index.ts:168-177` |

Para o robô: os seletores que dependem do tamanho ou da posição da janela do "Novo MTR" e do "Novo CDF" (cap04 e cap07) precisam
ser refeitos; a tela de sucesso ("MTR emitido" / "CDF emitido") continua uma janela pequena.

### Divergências já anotadas em `propostas_fala.md` que continuam valendo no 1.60.10 (o roteiro ainda não absorveu)
- cap03: depois de "Testar acesso salvo", o quadro mostra "Acesso validado" e, embaixo, a **mensagem devolvida pelo órgão** e
  "Último teste: <data e hora>" (`mtr/MtrConfigCard.tsx:286-302`). O toast usa a mesma mensagem do órgão quando ela vem
  (`hooks/useMtr.tsx:440`).
- cap03: "Sistema:" mostra o nome completo do banco, não só "SIGOR" (`MtrConfigCard.tsx:253-254`).
- cap07 (última linha): a coluna "Gerador" mostra o **CNPJ formatado**, não o nome (`cdf/CdfTab.tsx:333-337`). Trocar na coluna Tela.
- cap04: não existe etapa "Resumo"; o "Resumo do MTR" fica ao lado ("Atualiza enquanto você preenche", `NovoMtrModal.tsx:1851-1854`).

## 2. Falta cobrir

Legenda da coluna Vale: **capítulo** (capítulo novo), **trecho** (linhas a mais num capítulo que existe), **citar** (uma frase),
**não** (com o motivo).

### 2.1 Configuração (cap03)
| # | Função (texto exato) | Quando o cliente usa | Vale | Onde |
|---|---|---|---|---|
| 1 | Três estados do quadro de acesso: "Acesso validado", "Acesso salvo, teste pendente" ("Teste o acesso salvo antes da próxima emissão."), "Acesso recusado no último teste" (com o motivo do órgão) e "Último teste:" | Depois de trocar a senha no portal, ou quando a emissão começa a falhar | trecho | `MtrConfigCard.tsx:267-305` |
| 2 | Trocar a senha de um acesso já salvo: campo com "•••••• (digite para alterar)"; dica "Esqueceu? Use "Esqueci minha senha" na tela de login do portal." | Senha do portal vencida ou trocada | trecho (junto do 1) | `MtrConfigCard.tsx:381-400` |
| 3 | "Ambiente": "Produção" / "Homologação (testes)" | Quase nunca; o padrão já é Produção | citar | `MtrConfigCard.tsx:420-434` |
| 4 | Validações do acesso: CPF com 11 dígitos ("...não o CNPJ da empresa nem o e-mail de acesso."), código da unidade obrigatório | Erro comum no primeiro cadastro | citar (a fala já diz "CPF da pessoa") | `MtrConfigCard.tsx:172-225` |
| 5 | Outros estados: sistema federal com "Token de Integração (API WS) *" no lugar de CPF e senha ("Gere o token no portal do MTR Nacional em Configurações → Gerar Token API WS."); Espírito Santo com "CNPJ da unidade cadastrada no IEMA *"; nomes curtos SINIR, SIGOR, FEAM, FEPAM, IEMA | Cliente fora de São Paulo assistindo a aula | trecho curto, só cartão e fala (a Recicla Vale é de SP, não há tela para gravar) | `MtrConfigCard.tsx:309-336,360-379`; `utils/mtrSistema.ts:11-17` |
| 6 | Estado sem cobertura: "MTR ainda não disponível para a UF {uf}." e, sem UF, "Configure a UF da empresa em Configurações Fiscais." | Cliente de estado ainda não atendido | citar (junto do 5) | `MtrConfigCard.tsx:110-159`; `MtrTab.tsx:234-237` |
| 7 | Resíduo salvo: "Editar" ("Editar resíduo salvo", "Salvar alterações", toast "Resíduo atualizado") e "Excluir" ("Excluir "<nome>"", "Isso não afeta os MTRs já emitidos...", toast "Resíduo excluído"); nome repetido: "Já existe um resíduo salvo com esse nome" | Corrigir classe ou tratamento depois de conversar com quem cuida da licença | trecho | `MtrResiduosSalvosCard.tsx:232,346,390-440`; `hooks/useMtrResiduoPresets.tsx:54,138,158` |
| 8 | "Densidade" obrigatória quando a unidade é Litro ou m³ | Resíduo líquido (óleo, por exemplo) | citar | `MtrResiduosSalvosCard.tsx:335` |
| 9 | Ressincronizar os dados do órgão ("Sincronizando códigos oficiais…") | Quando o órgão muda a lista ou falta um código | citar | `MtrConfigCard.tsx:485-506` |
| 10 | Material: campo "Resíduo do MTR" dentro do "Editar Material" ("Preenche o MTR automaticamente a partir da nota fiscal."), "— Nenhum —", e a opção de **limpar** em massa ("Limpar resíduo de N") | Ligar um material só, ou desfazer a ligação | citar (o roteiro já usa a ação em massa) | `pages/Materiais.tsx:2208-2245`; `materiais/BulkMaterialMtrResiduoDialog.tsx:79` |
| 11 | Importação de materiais por planilha com a coluna "Resíduo do MTR" (novo no 1.59.155+) | Cadastro inicial de muitos materiais | não: é da aula de Materiais (T03); lá deve citar a coluna | `utils/materialsImport.ts:273-280` |

### 2.2 Emitir o MTR (cap04)
| # | Função | Quando usa | Vale | Onde |
|---|---|---|---|---|
| 12 | Tela cheia com "Sair" e "Resumo do MTR" ao lado: "N etapas pendentes" com os nomes, linhas "Transportador", "Destinador", "Expedição", "Motorista", "Placa", "Resíduos", "Responsável"; clicar numa etapa à frente com pendência devolve "Complete a etapa <nome> para continuar." | Sempre | trecho | `NovoMtrModal.tsx:222-245,880-908,1851-1856` |
| 13 | Lupa do CNPJ no cadastro do parceiro ("Buscar dados pelo CNPJ"): preenche a "Razão social *" | Todo cadastro de transportador ou destinador | trecho (troca o digitar pela lupa) | `NovoMtrModal.tsx:527-541`; `components/CnpjLookupInput.tsx:205` |
| 14 | Parceiro já salvo: escolher na lista com busca ("Buscar transportador..."), e o quadro "CNPJ: ..." / "Unidade SIGOR: ..." abaixo do campo | Do segundo MTR em diante | trecho (aparece no "Usar como modelo") | `NovoMtrModal.tsx:596-660,1355-1380` |
| 15 | Motorista e placa: digitar livre, escolher da frota ou "Gerenciar motoristas" / "Gerenciar placas" (cadastro na hora) | Motorista ou veículo novo, ou transportadora de terceiro | citar | `NovoMtrModal.tsx:1389-1408,1872-1899`; `weighing/DriverVehicleAutocomplete.tsx:151-158` |
| 16 | Data de expedição futura permitida; passada não ("A data de expedição não pode ser anterior a hoje") | MTR emitido na véspera da carga | citar | `NovoMtrModal.tsx:1410-1428` |
| 17 | Resíduo sem nota: "Usar resíduo salvo" ("Preencher a partir de um resíduo salvo"; "Preenche os códigos do órgão de uma vez. A quantidade continua sendo sua.") ou campo a campo | Carga sem NF-e (remessa, doação, material de terceiro) | capítulo (proposta C) | `NovoMtrModal.tsx:1530-1557` |
| 18 | "Adicionar resíduo": várias linhas "Resíduo 1", "Resíduo 2", lixeira para remover | Carga com mais de um tipo de resíduo | capítulo (proposta C) | `NovoMtrModal.tsx:1454-1456,1513-1530` |
| 19 | "Resíduo perigoso (opcional)": "Número ONU", "Classe de risco", "Subclasse de risco", "Grupo de embalagem" (I a IV), "Nome de embarque"; "Preencha apenas se o resíduo for classificado como perigoso para transporte (ONU/ADR)." | Bateria, óleo, resíduo de oficina | capítulo (proposta C; só abrir e fechar) | `NovoMtrModal.tsx:1688-1781` |
| 20 | "Observação do resíduo" (por linha) e "Densidade" | Detalhe da carga; unidade em litro ou m³ | citar | `NovoMtrModal.tsx:1650-1686` |
| 21 | Classe filtrada pelo resíduo: "Escolha o resíduo primeiro", "Consultando classes permitidas...", e a troca automática "A classe salva não era aceita para este resíduo e foi atualizada para ..." | Resíduo salvo antigo com classe que o órgão deixou de aceitar | citar | `NovoMtrModal.tsx:405-449` |
| 22 | "Puxar da nota fiscal" com **várias notas** ("N notas escolhidas"), notas de **Entrada e Saída**, soma por resíduo, botão "Acrescentar ao MTR" quando já há linha manual ("As linhas que você já preencheu continuam") | Uma carga com mais de uma nota | trecho | `MtrPuxarDaNotaDialog.tsx:142,185-197,389` |
| 23 | Avisos da prévia: "N itens ficaram de fora" com o motivo ("material sem resíduo salvo vinculado", "item sem material cadastrado", "resíduo salvo não encontrado neste sistema"); unidade sem conversão ("Não existe conversão automática entre essas unidades..."); lista cortada ("Mostrando as N notas autorizadas mais recentes de T."); "Nenhuma NF-e autorizada com chave de acesso. Só nota autorizada pela SEFAZ pode alimentar o MTR." | Nota com material ainda não ligado; nota em unidade diferente | trecho (o de "ficou de fora") e citar o resto | `MtrPuxarDaNotaDialog.tsx:44-48,201-300,372-420` |
| 24 | "Desfazer" o que veio da nota (toast "Resíduos e chaves da nota fiscal removidos") | Marcou a nota errada | citar | `NovoMtrModal.tsx:1053-1064,1478-1485` |
| 25 | Observação: "Este texto vai em "Observações do Gerador" do MTR — inclui a chave da NF-e que você puxou. Pode editar." | Sempre que puxa da nota | já coberto; manter | `NovoMtrModal.tsx:1829-1833` |
| 26 | Cota no momento de emitir: janela "Limite mensal atingido" e a faixa "Suas notas do mês acabaram" / "Aumentar nível" | Fim do mês com a cota no limite | citar, sem preço (a tela mostra valor; não gravar) | `notas-fiscais/LimiteNivelModal.tsx:61`; `notas-fiscais/QuotaLimitBanner.tsx:62-80`; `NovoMtrModal.tsx:1082-1085` |
| 27 | Selo da cota com dica ao passar o mouse: nome do nível, "Até N documentos fiscais por mês.", "Você emitiu N neste mês." | Conferir a cota | citar (o roteiro já dá zoom no selo; passar o mouse mostra a dica) | `pages/NotasFiscais.tsx:1873-1913` |

### 2.3 Acompanhar, PDF, modelo, erro e cancelamento (cap05 e cap06)
| # | Função | Quando usa | Vale | Onde |
|---|---|---|---|---|
| 28 | Os **cinco status** do MTR: "Emitido", "Rascunho", "Cancelado", "Erro", "Confirmar no órgão". O roteiro mostra só Emitido e Cancelado | Entender a lista | capítulo (proposta D) | `mtr/mtrShared.ts:19-35` |
| 29 | Status "Erro": ícone "Corrigir e tentar novamente" (abre o **mesmo** manifesto para arrumar) e ícone "Tentar novamente" com a janela "Tentar emitir este mesmo MTR?" ("O sistema repetirá o envio do mesmo manifesto local e preservará a tentativa anterior no histórico." ou, com data vencida, "A data de expedição venceu. Ela será atualizada para hoje antes do novo envio. O histórico anterior será preservado.") | Órgão rejeitou a emissão | capítulo (proposta D) | `MtrTab.tsx:209-227,415-440,470-490` |
| 30 | Faixa de erro dentro do "Novo MTR": "Revise o campo indicado" + o motivo, e o sistema volta para a etapa do campo | Emissão recusada na hora | capítulo (proposta D, citado) | `NovoMtrModal.tsx:1166-1182,1321-1333` |
| 31 | Status "Confirmar no órgão": some o "Usar como modelo" e não há "Tentar novamente"; no histórico, "Não reenvie antes de conferir no portal do órgão se o manifesto foi criado."; a edge responde "Este envio pode ter chegado ao órgão. Consulte o portal antes de qualquer nova tentativa." | Queda de conexão no meio do envio | capítulo (proposta D) | `MtrTab.tsx:364-366`; `MtrAttemptHistoryDialog.tsx:95-99`; `sigor-mtr-emit/index.ts:510-518` |
| 32 | "Histórico de tentativas": todos os selos ("Em andamento", "Bloqueada", "Revisar campos", "Rejeitada", "Confirmar no órgão", "Autorizada"), a mensagem do órgão em cada tentativa, "MTR ainda sem número oficial", vazio "Nenhuma tentativa registrada" | Descobrir por que não emitiu | capítulo (proposta D) | `MtrAttemptHistoryDialog.tsx:17-26,52,66-72` |
| 33 | "Usar como modelo" **clicado**: copia transportador, destinador, motorista, placa, resíduos, responsável e **a observação antiga** (com a chave da nota anterior); não copia número nem data. O roteiro só dá zoom no ícone | Carga repetida para o mesmo destino | capítulo (proposta C) | `MtrTab.tsx:174-202`; `NovoMtrModal.tsx:776-812` |
| 34 | "Baixar PDF" também na tela de sucesso, e de novo a qualquer momento pela lista (o botão só aparece quando o PDF existe) | Reimprimir o PDF do motorista | citar | `NovoMtrModal.tsx:1231-1240`; `MtrTab.tsx:362,389-398` |
| 35 | Coluna "Resíduo" mostra "N itens" quando o MTR tem mais de um resíduo; "Nº MTR" fica "—" sem número oficial | Ler a lista | citar (aparece na proposta C/D) | `MtrTab.tsx:133-139,373` |
| 36 | Cancelar: só no "Emitido"; erro do órgão volta como "Erro ao cancelar MTR: ..." | Carga que não saiu | já coberto | `MtrTab.tsx:363`; `hooks/useMtr.tsx:555` |
| 37 | Não existe filtro, busca, período nem exportação na lista de MTR | — | não: não há no código (ver seção 5) | `MtrTab.tsx:347-456` |
| 38 | Celular: botão flutuante "MTR", cartões com menu de três pontos | Emitir do pátio | não: aula gravada no desktop | `MtrTab.tsx:328-345,521-523`; `mtr/MtrCard.tsx` |

### 2.4 CDF (cap07 e cap08)
| # | Função | Quando usa | Vale | Onde |
|---|---|---|---|---|
| 39 | CDF **por gerador, sem lista de MTR**: com CNPJ e unidade do gerador, "Números dos MTRs" vira opcional ("Opcional — o certificado será emitido pelo gerador informado."); sem os dois, "Informe ao menos um MTR ou volte e informe o gerador." | Gerador com muitas cargas no período | trecho | `NovoCdfModal.tsx:575-612` |
| 40 | Validações: "A data final deve ser igual ou posterior à data inicial."; "CNPJ inválido. Confira os números."; "Para incluir o gerador, preencha CNPJ e unidade juntos."; "Atenção: o número de MTR contém apenas dígitos. Corrija ou remova: ..." | Digitação errada | citar | `NovoCdfModal.tsx:462-472,514,560-570,600-609` |
| 41 | "Unidade SIGOR: <código>" no passo Destinador e o aviso "Sua unidade no SIGOR não está configurada..." | Acesso sem unidade | citar | `NovoCdfModal.tsx:487-496` |
| 42 | Lupa no "CNPJ do gerador" (confere o CNPJ) e campo "Observação" ("Observações que constarão no certificado...") | Sempre | citar | `NovoCdfModal.tsx:536-548,640-650` |
| 43 | Status do CDF e ações por status: "Emitido" com PDF → "Baixar PDF"; "Emitido" sem PDF → "Gerar PDF" (aviso "Gerando o PDF do certificado...", toast "PDF gerado"); "Erro" → "Ver erro" (janela "Falha na emissão do CDF" com o motivo) e "Tentar novamente" ("Reenviando o CDF ao sistema ambiental...", toast "CDF reenviado"); "Rascunho" → "Excluir rascunho" ("Excluir rascunho?", "Excluir", toast "Rascunho excluído"); "Cancelado" → "Nenhuma ação disponível" | CDF que não saiu de primeira | capítulo (proposta E) | `cdf/CdfTab.tsx:121-141,167-235,370-425`; `hooks/useCdf.tsx:414,427` |
| 44 | Erro mais comum, com texto próprio: "Um ou mais MTRs ainda não foram recebidos no SIGOR. Dê baixa no recebimento do MTR no portal do órgão antes de emitir o CDF." | MTR sem baixa | capítulo (proposta E) | `sigor-cdf-emit/index.ts:420-426` |
| 45 | Sucesso sem PDF: "CDF emitido. O PDF ficará disponível na lista em instantes." | Órgão lento para devolver o PDF | citar (proposta E) | `NovoCdfModal.tsx:364-370` |
| 46 | Bloqueios do "Novo CDF": "Você não tem permissão para emitir CDF.", "CDF ainda não disponível para a UF ...", "CDF ainda não disponível para o sistema ambiental do seu estado.", "Configure o acesso ao SIGOR na aba MTR primeiro" | Antes da primeira emissão | citar o último (CDF usa o mesmo acesso do MTR) | `CdfTab.tsx:148-158` |
| 47 | Coluna "Gerador" mostra "N MTR(s)" quando o CDF não tem gerador | Ler a lista | citar | `CdfTab.tsx:333-337` |
| 48 | Não existe cancelar CDF, nem receber MTR, nem filtro ou exportação da lista | — | não: não há no código (a fala atual já diz que a baixa é no portal e que o CDF é definitivo) | `CdfTab.tsx`; `NovoCdfModal.tsx:625-633` |

### 2.5 Permissão, relatórios e outras aulas
| # | Função | Vale | Onde |
|---|---|---|---|
| 49 | Permissão "Emitir Documentos Ambientais (MTR/CDF)" ("Emitir e cancelar MTR e CDF"). Sem ela: "Novo MTR" e "Novo CDF" desligados com "Você não tem permissão para emitir MTR." / "...CDF.", somem cancelar, modelo e tentar de novo; a lista, "Ver tentativas" e "Baixar PDF" continuam | trecho curto com cartão; marcar a permissão é da T02 (Usuários) | `config/routes.ts:260`; `lib/fiscalPermissions.ts:30-36`; `MtrTab.tsx:232-233,363-366` |
| 50 | Relatórios: o menu "Relatórios Fiscais" tem só "NF-e" e "NFS-e"; **não há relatório de MTR nem de CDF** | não há o que gravar; ver seção 5 | `pages/NotasFiscais.tsx:202-205` |
| 51 | Cato: a consulta "resumo_fiscal" traz o panorama do período com MTR e CDF | não: aula do Cato; lá pode citar | `supabase/functions/_shared/cato/tools.ts:308-316` |
| 52 | NF-e da mesma carga (cap09): lista de notas sem mudança que afete o MASTER | nada a mudar | `pages/NotasFiscais.tsx` |

**Achados do app (não mudam a fala, vão para quem cuida do produto):**
- A aba CDF continua mostrando os cartões de contagem de NF-e (H1 do inventário; `pages/NotasFiscais.tsx:1943`).
- `hooks/useCdf.tsx:237,383` ainda barra quem não é administrador com "Apenas administradores podem emitir CDF.", enquanto o botão
  "Novo CDF" já libera pelo `action_emit_ambiental` (`CdfTab.tsx:148`). Um operador com a permissão ambiental abre o Novo CDF e toma
  esse erro ao emitir. Por isso o trecho de permissão (proposta F) deve ser gravado só com o MTR.
- MTR em "Rascunho" não tem ação de excluir (o CDF tem). MTR em "Confirmar no órgão" não tem nenhuma ação na tela para sair desse
  estado depois que o cliente confere no portal.

## 3. Proposta

Ordem final sugerida: 00, 01, 02, 03, 04, 05, **05b (novo)**, 06, **06b (novo)**, 07, 08, **08b (novo)**, 09, 10.

### A. cap03 · trechos a acrescentar
| Tela | Fala |
|---|---|
| (depois de "Testar acesso salvo") Zoom no quadro "Acesso validado", com a mensagem do órgão e "Último teste: 10/11/2026 ...". | Esse quadro mostra como está o acesso, com a data do último teste. |
| O mouse vai ao campo "Senha do SIGOR", que agora mostra "•••••• (digite para alterar)". | Se a senha do portal mudar, é só digitar a nova aqui, salvar e testar de novo. Enquanto não testar, o quadro fica como teste pendente. E se o órgão recusar, o motivo aparece nele. |
| O mouse passa por "Ambiente", em "Produção". | O ambiente fica em Produção. Homologação é só pra teste. |
| Cartão "Dica: em outros estados, o que muda é o acesso". | Uma dica: fora de São Paulo, a tela é a mesma e o sistema já vem pelo estado da empresa. Nos estados que usam o sistema federal, no lugar do CPF e da senha entra o token de integração, gerado no portal. |
| (depois de "Salvar resíduo") O mouse passa pelos ícones "Editar" e "Excluir" da linha "Sucata de ferro", sem clicar. | Cada resíduo salvo pode ser editado ou excluído por aqui. Excluir não mexe nos manifestos que já saíram. |
| Cartão "Permissão: Emitir Documentos Ambientais (MTR/CDF)" (proposta F; pode ficar aqui ou no cap00). | Uma dica: emitir e cancelar MTR e CDF é uma permissão própria, a de documentos ambientais. Quem não tem continua vendo a lista e baixando o PDF, mas o botão de novo fica desligado. |

Mundo: nada novo (o backend falso já devolve `last_validated_at` e `last_validation_message`).

### B. cap04 · trechos a acrescentar ou trocar
| Tela | Fala |
|---|---|
| (linha 1, depois de clicar em "Novo MTR") A tela cheia abre: "Sair", "Novo MTR", "Informe o transporte, os resíduos e o responsável antes de emitir o manifesto."; ao lado, "Resumo do MTR" com "3 etapas pendentes". [ZOOM: "Resumo do MTR"] | O Novo MTR abre em tela cheia, em três etapas. Aqui do lado, o resumo vai se preenchendo e avisa o que ainda falta. |
| (troca a linha do transportador) Em "Cadastrar novo transportador", digita o CNPJ da Recicla Vale em "CNPJ *" e clica na lupa "Buscar dados pelo CNPJ": "Razão social *" vem preenchida; digita "203918" em "Código da unidade no SIGOR *"; "Salvar e usar". | O transportador é a própria Recicla Vale, com o caminhão dela. Como é o primeiro MTR, eu cadastro: digito o CNPJ, clico na lupa e a razão social vem sozinha. Falta só o código da unidade no SIGOR. |
| (linha do motorista, acrescenta) O mouse passa por "Gerenciar motoristas". | (acrescentar ao fim) Se o motorista ou a placa não estiverem na frota, dá pra digitar na hora. |
| (linha da prévia do "Puxar da nota fiscal", acrescenta) | (acrescentar ao fim) Dá pra marcar mais de uma nota, e o sistema soma tudo por resíduo. Se algum material da nota não estiver ligado a um resíduo salvo, ele fica de fora e a prévia avisa. |
| (linha da dica da cota, acrescenta) O mouse para no selo da cota: aparece a dica com "Você emitiu ... neste mês.". | (acrescentar ao fim) Se a cota acabar, o sistema avisa na hora de emitir. |

Mundo: handler falso da busca de CNPJ (edge `cnpj-lookup`) devolvendo a razão social da Recicla Vale e a da Aços Quiririm.

### C. cap05b (novo) · O próximo MTR mais rápido (vinheta: MTR)
Substitui o zoom sem clique no "Usar como modelo" (última linha do cap05) e passa a emitir **na tela** o MTR da tarde
(2611000325), que hoje nasce na semente. O cap06 cancela esse mesmo MTR.

| Tela | Fala |
|---|---|
| Lista com o "2611000318" "Emitido"; clica no ícone "Usar como modelo" da linha: abre "Novo MTR" com "Transportador *" e "Destinador *" já escolhidos (quadros "CNPJ: ..." / "Unidade SIGOR: ..."), "Jair Lopes", "GHT7B19" e a "Data de expedição *" de hoje. | À tarde sai outra carga pra Aços Quiririm, agora de ferro misto. Em vez de começar do zero, eu clico em Usar como modelo. Transportador, destinador, motorista e placa já vêm, e a data é a de hoje. |
| "Avançar": etapa "Resíduos", "Resíduo 1" com "Sucata de ferro" e "Quantidade *" 3,6; troca para "3,2". [ZOOM: "Quantidade *"] | Nos resíduos, vem a mesma sucata de ferro. Eu só troco a quantidade: três vírgula duas toneladas. |
| Clica em "Adicionar resíduo": surge "Resíduo 2"; abre "Usar resíduo salvo" ("Preencher a partir de um resíduo salvo") e mostra a lista; fecha e remove o "Resíduo 2" na lixeira. | Se a carga levar mais de um tipo de resíduo, o Adicionar resíduo cria outra linha. E cada linha pode partir de um resíduo salvo, mesmo sem nota fiscal. |
| No "Resíduo 1", abre "Resíduo perigoso (opcional)": "Número ONU", "Classe de risco", "Subclasse de risco", "Grupo de embalagem", "Nome de embarque"; fecha. | Pra resíduo perigoso no transporte, como bateria, os dados da ONU entram aqui. Sucata de ferro não é o caso, então fica fechado. |
| "Avançar": etapa "Responsável", já com "Rafael Nogueira" e "Sócio-administrador"; a "Observação" veio com a chave da nota da manhã; apaga o texto. [ZOOM: "Observação"] | Uma dica: o modelo copia também a observação, com a chave da nota da carga anterior. Eu apago, porque esta carga tem outra nota. |
| "Resumo do MTR": "Tudo pronto para emitir o MTR"; "Emitir MTR": "MTR emitido", "Nº do manifesto: 2611000325"; "Concluir". | Emitir MTR. Pronto, o segundo manifesto do dia, em poucos cliques. |

Com isso, a primeira linha do cap06 encurta para: "Mais tarde, a Aços Quiririm pediu pra deixar essa carga de ferro misto pra semana que vem."

Mundo: a semente `apos-cap05` deixa de trazer o 2611000325 pronto; o `sigor-mtr-emit` falso devolve 2611000325 na segunda
emissão; o corte para 10:40 continua só no cap06. (A quantidade 3,2 TON já é a do `plano.md`.)

### D. cap06b (novo) · Quando o envio não passa (vinheta: MTR)
| Tela | Fala |
|---|---|
| Lista de MTR com duas linhas mais antigas, de 04/11/2026: uma "Erro" (Nº MTR "—") e uma "Confirmar no órgão". [ZOOM: os dois selos] | Nem todo envio passa de primeira. Olha esses dois da semana passada: um ficou com erro, e o outro, com Confirmar no órgão. |
| Na linha "Erro", clica em "Ver tentativas": "Histórico de tentativas", "MTR ainda sem número oficial", selo "Rejeitada" e a mensagem do órgão; "Fechar". | No erro, o Ver tentativas mostra o que o órgão respondeu. |
| O mouse passa pelo ícone "Corrigir e tentar novamente" e para no "Tentar novamente"; clica: "Tentar emitir este mesmo MTR?", com "A data de expedição venceu. Ela será atualizada para hoje antes do novo envio. O histórico anterior será preservado."; clica em "Voltar". [ZOOM: o texto] | Daí são dois caminhos. Corrigir e tentar novamente abre o mesmo MTR pra arrumar o campo que o órgão recusou. E Tentar novamente reenvia do jeito que está. Como a data de expedição já passou, o sistema troca pra hoje. |
| Na linha "Confirmar no órgão" só existe "Ver tentativas"; clica: selo "Confirmar no órgão" e "Não reenvie antes de conferir no portal do órgão se o manifesto foi criado."; "Fechar". [ZOOM: a frase] | Já o Confirmar no órgão quer dizer que o envio pode ter chegado lá, mas a resposta não voltou. Por isso o sistema não deixa reenviar nem copiar esse MTR. Antes de qualquer coisa, confira no portal do órgão se o manifesto foi criado. Assim a mesma carga não sai com dois manifestos. |
| A câmera volta à lista inteira. | E Rascunho é o MTR que foi salvo, mas ainda não foi enviado. |

Mundo: dois `mtr_manifests` de 04/11/2026 para a Aços Quiririm, presentes desde a semente `apos-cap03` (ou só a partir do corte
das 10:40): um `erro` com um `mtr_manifest_attempts` `rejected` e `error_message` do órgão (texto fictício a definir, por
exemplo classe não aceita para o resíduo); um `incerto` com um attempt `uncertain`. Ambos entram na coluna "Resíduo" como
"Sucata de ferro" (um item cada). Atenção: eles aparecem na lista já no cap05; se isso atrapalhar, a semente entra só no corte.
Nenhum handler novo se o robô clicar em "Voltar".

### E. cap08b (novo) · Quando o certificado não sai (vinheta: CDF)
| Tela | Fala |
|---|---|
| Lista de CDF com o "2611000041" "Emitido" e, abaixo, uma linha "Erro" (Nº CDF "—", período 01/11/2026 a 07/11/2026) e uma "Rascunho". | O CDF também pode parar no caminho. Aqui tem um com erro e um rascunho. |
| Abre "Ações" na linha "Erro" e clica em "Ver erro": "Falha na emissão do CDF", com "Um ou mais MTRs ainda não foram recebidos no SIGOR. Dê baixa no recebimento do MTR no portal do órgão antes de emitir o CDF.". [ZOOM: o texto] | Em Ver erro aparece o motivo. Este é o mais comum: um dos manifestos ainda não teve a baixa do recebimento no portal. |
| Clica em "Tentar novamente": aviso "Reenviando o CDF ao sistema ambiental...", toast "CDF reenviado"; a linha vira "Emitido" com número. | Depois de dar a baixa lá no portal, é só clicar em Tentar novamente. Pronto, emitido. |
| Abre "Ações" na linha "Rascunho" e clica em "Excluir rascunho": "Excluir rascunho?"; clica em "Excluir": toast "Rascunho excluído". | O rascunho é um certificado que não chegou a ser enviado. Ele pode ser excluído, porque ainda não existe no órgão. |
| Volta à linha "Emitido"; o mouse abre "Ações". | E se um CDF ficar emitido sem o PDF, o menu de ações mostra Gerar PDF, que busca o arquivo de novo. |

Trecho a acrescentar no cap07 (passo "MTRs INCLUÍDOS"): fala "Como o gerador já está informado, a lista de MTR aqui é opcional:
sem ela, o certificado sai pelo gerador e pelo período." (a tela mostra o rótulo "Números dos MTRs" sem o asterisco).

Mundo: dois `mtr_cdf` novos na semente `apos-cap07`: um `erro` (período 01/11 a 07/11/2026, gerador Auto Peças Vale Forte,
um MTR fictício novo, por exemplo 2611000102, `erro_mensagem` com o texto acima) e um `rascunho`. Handler: `sigor-cdf-emit` falso
aceitando o reenvio por `cdfId` e devolvendo número (por exemplo 2611000057) e PDF; `delete` em `mtr_cdf` do rascunho.
Conferir na cota do mundo: o CDF reenviado conta mais um documento.

### F. Permissão (cartão; dentro da proposta A)
Só fala e cartão. Se o Kaik quiser tela: logar como Marcos Antunes (sem a permissão) e mostrar o "Novo MTR" desligado com a dica
"Você não tem permissão para emitir MTR." (não mostrar o CDF, por causa do achado do `useCdf`). Isso pede troca de usuário no
robô; a recomendação é ficar no cartão e deixar a marcação da permissão para a T02.

## 4. Estimativa

| Item | Palavras | Fala |
|---|---|---|
| A. cap03 (acesso, ambiente, outros estados, editar resíduo, permissão) | ~150 | ~58 s |
| B. cap04 (tela cheia e resumo, lupa, frota, várias notas, cota) | ~80 líquidas | ~31 s |
| C. cap05b novo (modelo, mais resíduos, perigoso, observação) | ~150 | ~58 s |
| D. cap06b novo (erro, tentar de novo, confirmar no órgão, rascunho) | ~150 | ~58 s |
| E. cap08b novo (erro do CDF, rascunho, gerar PDF) + trecho do cap07 | ~125 | ~48 s |
| Encurtamento do cap05 e do cap06 | −25 | −10 s |
| **Total** | **~630** | **~243 s de fala (cerca de 4 min)** |

Capítulos novos: **3** (05b, 06b, 08b), mais 3 vinhetas (~10 s) e as esperas do órgão simulado. A aula vai de ~10,5 min para
~15 min. O cap10 (recapitulação) ganha uma frase por capítulo novo (~12 s, já fora da conta acima).

## 5. Depende de decisão

1. **Relatórios de MTR e CDF não existem no app** (nem filtro, busca ou exportação nas duas listas). O pedido do Kaik citava
   relatórios: a aula só pode dizer que o histórico são as duas listas e o PDF de cada documento. Decidir se entra essa frase
   ("O histórico dos manifestos e dos certificados fica nessas duas listas, com o PDF de cada um.") ou se vira pedido de
   melhoria do produto.
2. **"Receber" MTR** também não existe: a baixa do recebimento é no portal do órgão (a fala atual já diz). Manter assim.
3. **"Confirmar no órgão"** não tem saída na tela depois da conferência no portal. A proposta D diz só "confira no portal";
   decidir se a fala manda procurar o suporte quando o manifesto não foi criado.
4. **Outros estados** (token do sistema federal, IEMA): entra como cartão e fala (proposta A) ou fica de fora por a Recicla
   Vale ser de São Paulo.
5. **Permissão**: cartão (recomendado) ou tela com o Marcos; e o achado do `useCdf` (operador com a permissão é barrado no CDF)
   deve ir para o time do app antes de a aula afirmar que a permissão vale para os dois.
6. **cap06b, clique final**: "Voltar" (recomendado, sem handler novo) ou reenviar de verdade e mostrar o MTR virar "Emitido"
   (mais um documento na cota do mundo).
7. **Onde entram as linhas "Erro" e "Confirmar no órgão"** do mundo: desde o cap04 (lista mais realista) ou só no corte das 10:40.
8. Janela "Limite mensal atingido": mostra valor de nível; a proposta é só citar, sem gravar.
