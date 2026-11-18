# T12 · Coletas e Logística · cobertura contra o 1.60.10

Auditoria de 18/11/2026, só leitura de código (`/dev/shm/ecoflix-src`, igual ao commit `5290be4cd` nos arquivos
conferidos). Caminhos relativos a `src/`. Rótulo entre aspas = texto exato do código.

## 1. Mudou no app (1.59.154 → 1.60.10)

**Nas telas desta aula: nada.** `git diff f37573ea0 5290be4cd` sai vazio para `components/coletas/`, `pages/Coletas.tsx`,
`pages/CollectionOrderPage.tsx`, `lib/coletas/`, `components/portal/`, `pages/EntityPortal.tsx`, as edges
`collection-request` e `collection-report`, os hooks `useCollection*`, `useFleet.ts` e o menu de Coletas em
`config/routes.ts:528-541`. Nenhuma nota de versão de 1.59.155 a 1.60.10 (`config/version.ts:19-113`) fala de coletas,
frota ou equipamentos. Todos os rótulos, botões e avisos do roteiro continuam valendo, capítulo por capítulo.

Em volta das telas (não muda fala, pode mudar quadro de vídeo):

| Onde | O que mudou | Arquivo |
|---|---|---|
| Todas as telas logadas (cap00 a cap11) | O botão flutuante do Cato aparece no canto quando a empresa tem o Cato ligado e o usuário tem `action_use_cato` (o MASTER tem). Se o mundo ligar o Cato, ele entra em todos os quadros; conferir na regravação se cobre o rodapé "Criar ordem" ou os botões do cartão. | `components/layout/AppLayout.tsx:283,536` |
| cap00, menu lateral | "Fiscal & Ambiental" ganhou o filho "Relatórios Fiscais". Só aparece se o grupo estiver aberto; o roteiro só abre "Coletas & Logística". | `config/routes.ts:511` |

As divergências já anotadas em `propostas_fala.md` (cidade Tremembé no cartão #8, Histórico sem evento de criação,
"Entreguei" acima do "Recolhi", data do relatório um dia antes) continuam iguais no 1.60.10: não são mudança de versão.

## 2. Falta cobrir (está no 1.60.10 e o roteiro não mostra)

### Quadro das ordens (cap02) · `components/coletas/CollectionOrdersBoard.tsx`
| # | O que é | Quando o cliente usa | Vale? |
|---|---|---|---|
| 1 | Visão "Lista": tabela "Nº", "Parceiro", "Material", "Data / Janela", "Motorista", "Veículo", "Status", "Origem" ("Portal"/"Interna"), "Ações"; clicar no cabeçalho ordena; a escolha Quadro/Lista fica lembrada (`:300-308,848-856,892`) | Muitas ordens, quer ordenar por data ou motorista | **Sim**, trecho (hoje só aponta o botão) |
| 2 | Painel "Filtros": "Data agendada" "De"/"Até", aviso "As solicitadas aparecem sempre, independente da data.", "Status", "Parceiro", "Limpar Filtros" (`:948-1004`) | Ver só a semana, só um parceiro | **Sim**, trecho (hoje só aponta) |
| 3 | Arrastar o cartão entre colunas: muda etapa; para "Agendada" abre "Agendar coleta", para "Concluídas" abre a tela da ordem, para "Cancelada" pede confirmação (`:521-555`) | Quem prefere arrastar a clicar | **Sim**, uma frase com um arraste |
| 4 | Menu "Ações da ordem": "Visualizar", "Editar", "Copiar link" (só concluída), "Excluir" (`:568-626`) | Corrigir data, motorista, endereço | **Sim** (capítulo novo A) |
| 5 | "Editar" abre a mesma janela em página única, botão "Salvar" (`CollectionOrderDialog.tsx:178,752-758`) | Trocar motorista ou data depois de criar | **Sim** (capítulo A) |
| 6 | "Cancelar coleta?": "A ordem #N será marcada como cancelada. Essa ação não pode ser desfeita.", "Voltar", "Cancelar coleta" (`:1220-1246`) | Parceiro desmarcou | **Sim** (capítulo A; hoje só falado) |
| 7 | "Excluir ordem de coleta?": "A ordem #N será apagada permanentemente. Essa ação não pode ser desfeita."; se já movimentou equipamento ou tem checklist: "Não deu para excluir" + motivo + "Cancelar ordem em vez disso" (`:1296-1343`) | Ordem criada por engano | **Sim** (capítulo A): é a diferença entre excluir e cancelar |
| 8 | "Recusar solicitação?": "Informe o motivo — ele fica registrado no histórico da ordem.", "Motivo" ("Ex: material fora da região atendida, fora do horário…"), "Recusar solicitação"; o parceiro vê "Motivo: ..." no portal (`:1248-1288`; `portal/PortalCollectionsTab.tsx:108-110`) | Pedido fora da região | **Sim** (capítulo A; hoje só falado no cap07) |
| 9 | Botão "Preencher" também no cartão cancelado | — | Não: é achado do app, já em `propostas_fala.md` |

### Nova ordem (cap03 a cap05) · `components/coletas/CollectionOrderDialog.tsx`
| # | O que é | Quando | Vale? |
|---|---|---|---|
| 10 | Modo "Sem cadastro" de verdade: "Nome do solicitante *" ("Nome de quem está pedindo a coleta"), "Telefone", "Endereço completo * — obrigatório sem cadastro"; a Revisão mostra "Solicitante (sem cadastro):" e "Telefone:" (`:525-572,620-632`) | Coleta avulsa de pessoa física | **Sim**, trecho: hoje só fala que existe |
| 11 | "Tipo" "Cliente" (além de "Fornecedor") (`:489-505`) | Buscar material em cliente (devolução, vasilhame) | Só citar |
| 12 | Motorista e Veículo com "+" para cadastrar na hora (`:577-615`) | Motorista novo sem sair da ordem | Só citar |
| 13 | "Período" "Não definido" e data em branco (ordem sem dia) | Combinou sem data | Só citar (liga com a dica do relatório no cap10) |

### Tela da ordem e relatório (cap06) · `pages/CollectionOrderPage.tsx`
| # | O que é | Quando | Vale? |
|---|---|---|---|
| 14 | Botão "Iniciar coleta" na tela da ordem agendada (`:581-582,1425-1432`) | Motorista inicia pelo celular, sem passar pelo quadro | **Sim**, uma frase |
| 15 | Aviso "Localização em registro — sua posição é salva periodicamente enquanto a coleta está em andamento." / "Sem sinal de GPS — a coleta segue normalmente, só a localização não está sendo registrada." (`:1164-1185`) | Toda coleta "A caminho" | **Depende da decisão do Rastreamento** (item 37) |
| 16 | Equipamento "Por quantidade" na ordem: escolhe o tipo e digita a quantidade (bag) em vez de escolher a unidade (`:1336-1338`); erros "Informe uma quantidade maior que zero." (`:986`) | Deixou 10 bags, recolheu 8 | **Sim**, trecho: a aula só mostra caçamba |
| 17 | Lista vazia: "Nenhuma unidade deste tipo está na sua base — todas estão em campo." / "Nenhuma unidade deste tipo está com <parceiro>." (`:1327`) | Tentou entregar caçamba que não está na base | Só citar (sem erro encenado) |
| 18 | Ordem sem cadastro: "Sem cadastro — esta coleta não tem fornecedor vinculado, então não é possível entregar ou recolher equipamentos (caçambas, bags) aqui." + botão "Cadastrar como fornecedor"; abre o cadastro rápido com nome e telefone e avisa "Fornecedor cadastrado e vinculado à ordem" (`:1238-1262,800-836`) | O avulso virou parceiro fixo | **Sim**, trecho (a ordem #7 do Marcelo serve) |
| 19 | "Checklist" na ordem: perguntas do modelo, tipos "Sim ou não", "Conforme / Não conforme / Não se aplica", "Texto livre", "Número", "Escolher uma opção", "Escolher uma ou mais opções", "Foto" (`lib/coletas/collectionChecklist.ts:31-39`; `:1349-1380`) | Empresa que exige conferência no local | **Sim** (capítulo novo C) |
| 20 | "Assinatura": "Motorista" e "Responsável no local", "Assinar novamente" (`:1384-1408`; `CollectionChecklistFields.tsx:307`) | Comprovar que entregou/recolheu | **Sim** (capítulo C) |
| 21 | "Falta para concluir: ..." e o bloqueio "Antes de concluir, falta: Assinatura do motorista · ..." (`:936-952,1449`) | Esqueceu resposta obrigatória | **Sim** (capítulo C, mostrado como aviso, não como erro) |
| 22 | Relatório da coleta: barra "Copiar link" ("Link do relatório copiado"), "Compartilhar no WhatsApp" (mensagem "Relatório da coleta N, confira aqui: <link>"), "Imprimir"; blocos "Checklist", "Equipamentos", "Fotos", "Assinaturas" (`:376-398,432-530`; `lib/coletas/collectionShareLink.ts:38-61`) | Mandar o comprovante da coleta ao parceiro | **Sim** (capítulo novo B) |
| 23 | Sem Portal do Cliente, no lugar dos botões: "O cliente ainda não consegue abrir esse link porque o Portal do Cliente está desligado. Fale com o suporte para ativar o módulo e liberar o compartilhamento." (`collectionShareLink.ts:71-72`) | Quem só tem Coletas | Só citar (uma frase no capítulo B) |

### Ficha da ordem (cap06) · `components/coletas/CollectionOrderDetailDialog.tsx`
| # | O que é | Vale? |
|---|---|---|
| 24 | "Relatório do Fornecedor": "Link público (sem login) pra mandar pro fornecedor.", "Abrir link do Fornecedor", "Copiar link" (`:365-400`) | **Sim** (capítulo B) |
| 25 | Rodapé "Editar", "Preencher"/"Relatório", próximas etapas, "Recusar"/"Aprovar" (`:477-546`) | Só citar |

### Portal (cap07) · `components/portal/`
| # | O que é | Vale? |
|---|---|---|
| 26 | Em "Minhas coletas", a concluída vira clicável: "Ver relatório da coleta" (`PortalCollectionsTab.tsx:113-118,166`) | **Sim**, uma linha no capítulo B |
| 27 | Recusas do pedido: "A data escolhida já passou. Escolha hoje ou uma data futura.", "A coleta precisa ser pedida com no mínimo 24h de antecedência.", "A empresa não aceita coleta no dia escolhido. Escolha outro dia." (`lib/coletas/collectionSettings.ts:93-113`) | Só citar no cap11 (sem erro encenado) |
| 28 | Liberar/ocultar a aba: "Mostrar aba Coletas" e "Permitir solicitar coleta" no cadastro do parceiro; aba com senha | **Não aqui: é da T20** (cap05 e cap08 da T20 já mostram). A T20 cap08 repete o pedido de coleta do cap07 desta aula: manter, mas com dado diferente |

### Frota (cap08) · `VehiclesTab.tsx`, `DriversTab.tsx`
| # | O que é | Vale? |
|---|---|---|
| 29 | Menu de cada veículo/motorista: "Editar" e "Excluir" ("Excluir veículo?", 'O veículo "PLACA" será removido da frota. Esta ação não pode ser desfeita.") (`VehiclesTab.tsx:160-177,892-911`; `DriversTab.tsx:102-119,623`) | **Sim**, uma frase |
| 30 | Lista: busca, "Filtros" por "Tipo de veículo", "Ordenar" (`VehiclesTab.tsx:490-535`; motoristas: ordenar por "Categoria da CNH", "Validade da CNH", `DriversTab.tsx:80-81`) | Só citar |
| 31 | Avisos do cadastro: "Valor parece estar em toneladas — informe em quilos (ex.: 32.000)." em Tara e Capacidade abaixo de 1.000; bloqueio "Capacidade de N m³ acima do limite da SEFAZ. Informe no máximo 999 m³." (`lib/coletas/vehicleLimits.ts:11-45`; `VehiclesTab.tsx:422-431`) | **Sim**, uma dica falada (erro comum; o de m³ é fiscal) |
| 32 | "Tipo" cavalo/carreta, "RNTRC", "Tipo de carroceria" e a mesma frota em Transporte (MDF-e) → Frota | **Não aqui: T17** (cap02 da T17) |

### Equipamentos (cap09)
| # | O que é | Vale? |
|---|---|---|
| 33 | "Novo tipo": "Nome *", "Etiquetas", cor, "Ícone", chave "Cada unidade tem identificação própria" ("Ligue para equipamentos como caçambas... Deixe desligado para equipamentos fungíveis como bags e caixas, contados só por quantidade."); "Editar", "Inativar tipo?"/"Reativar tipo?", "Mostrar inativos" (`EquipmentTypesCrud.tsx:149-158,313-411`) | **Sim**, trecho (hoje só lê a tabela) |
| 34 | "Onde tudo está agora" tem dois blocos: "Contados por quantidade" ("bags, caixas, paletes", com "Ver saldo por fornecedor"/"Ocultar saldos") e "Rastreados um a um" ("caçambas e afins") (`EquipmentPositionTab.tsx:288-361`) | **Sim**, trecho: é onde se vê quantos bags estão com cada parceiro |
| 35 | Unidade: "Condição" "Em manutenção" e "Baixada"; filtros "Tipo"/"Condição"; "Editar"; "Excluir unidade" ("Remover unidade?"); "Etiquetas" (`ContainersTab.tsx:273-303,397-403,468-474`) | **Sim**, uma frase (caçamba furada vai para manutenção) |
| 36 | "Nova movimentação" completa: "De"/"Para" com "Parceiro" ("Selecionar parceiro…"), várias linhas ("Adicionar linha"), tipo por quantidade com "Quantidade", "Data", "Observação"; erro "Origem e destino são o mesmo lugar" (`NewEquipmentMovementModal.tsx:402-489,633-834`) | **Sim**, trecho: mandar 10 bags a um parceiro sem ordem |
| 36b | Aba "Movimentações": lista "Equipamentos" à esquerda ("Escolha para ver só as movimentações dele"), "Filtros" ("Período", "Tipo de equipamento", "Parceiro", "Mostrar anuladas"), coluna "Movimento" ("Entrada"/"Saída"/"Transferência"), "Ordem de coleta"; menu "Editar" ("Editar movimentação": "Corrige quantidade, data, origem/destino ou observação. Tipo e unidade não mudam aqui — pra isso, anule e lance de novo."), "Excluir" ("Excluir movimentação?", "Motivo (opcional)", vira "Anulada"), "Restaurar" (`EquipmentHistoryTab.tsx:79-84,181-222,302-371,456-462,581-609`) | **Sim**, trecho: corrigir lançamento errado |
| 36c | Botão "Configurações" → "Configurações de equipamentos": "Categorias e tipos", "Etiquetas", "Campos personalizados" (`EquipmentSettingsDialog.tsx:13-19`) | Só citar |

### Seções fora do roteiro
| # | O que é | Vale? |
|---|---|---|
| 37 | **"Rastreamento"** funciona no 1.60.10 (e já funcionava no 1.59.154): mapa "Ao vivo (todos os motoristas)", "Motoristas no mapa", selos "Ao vivo"/"Visto há pouco"/"Sem sinal recente", "Trajeto de uma coleta", "O círculo ao redor do ponto é o raio de incerteza do GPS..."; vazio: "Nenhum motorista no mapa ainda" + explicação de que o motorista precisa de login (`CollectionTrackingTab.tsx:80,406-415,439,497-501,533,572-575`) | **Decisão do Kaik.** A TRILHA diz que fica de fora por ser "Em breve", mas só "Rotas" é "Em breve". Com o pedido de "cobrir cada função", proponho capítulo curto (D). Exige motorista com login e posições na semente |
| 38 | "Rotas": "Roteirização" + "Em breve — esta função chega numa próxima atualização" (`pages/Coletas.tsx:122-128`) | Não: não existe ainda. No máximo meia frase no capítulo D |
| 39 | Aba "Coletas" na ficha do parceiro: botões "Movimentar equipamento" e "Agendar coleta", blocos "Com este parceiro agora", "Coletas", "Movimentações de equipamento" (`pages/PartnerDetail.tsx:295,570`; `components/partner/PartnerCollectionsTab.tsx:184-200,205,281,331`) | **Sim**, trecho aqui (a T4 não cita coleta nenhuma; a aba só existe com o módulo) |

### Configurações (cap11) · `CollectionSettingsTab.tsx`
| # | O que é | Vale? |
|---|---|---|
| 40 | "Avisar quando chegar solicitação": "Notifica você sempre que um parceiro pedir uma coleta pelo portal." (`:256-266`) | **Sim**, uma frase (hoje a câmera nem para) |
| 41 | Travas: "Mantenha ao menos uma janela de coleta", "Aceite ao menos um dia da semana" (`:89,101`) | Só citar |
| 42 | "Checklist da coleta": "Checklist padrão da empresa" ("Nenhum (sem checklist)"), "Exigir assinatura do motorista", "Exigir assinatura do responsável no local", "Modelos de checklist" ("Novo modelo", "Gerenciar perguntas", "Nova pergunta", "Pergunta *", "Tipo de resposta", "Opções *", "Pergunta obrigatória", "Texto de ajuda (opcional)", arrastar para reordenar, "Inativar modelo?") (`:273-360`; `ChecklistTemplatesCrud.tsx`, `ChecklistQuestionsDialog.tsx`) | **Sim** (capítulo C; o roteiro declara "fora da aula") |
| 43 | "Relatório público": "Mostrar valores no relatório que o cliente abre", com o aviso "O link do relatório é público (não pede login)..." (`:364-394`) | **Sim**, no capítulo B |

Achado para o Kaik (não é fala): a ajuda do checklist diz "Usado em toda coleta nova, a menos que outro modelo seja
escolhido na própria ordem." (`CollectionSettingsTab.tsx:311`), mas a janela da ordem não tem campo de checklist
(`CollectionOrderDialog.tsx`: nenhum seletor); a ordem só lê `order.checklist_template_id ?? settings`
(`CollectionOrderPage.tsx:750`). A aula não deve prometer escolha por ordem.

## 3. Proposta

Trechos entram nos capítulos existentes; os capítulos A a D são novos. Numeração final sugerida: cap06b (A), cap06c (B),
cap11b (C), cap09b (D), para não renumerar sementes.

### Trechos em capítulos existentes

| Cap. | Tela | Fala |
|---|---|---|
| cap02 | Clique em "Lista": a tabela "Nº", "Parceiro", "Material", "Data / Janela", "Motorista", "Veículo", "Status", "Origem"; clique no cabeçalho "Data / Janela"; volta para "Quadro". | Prefere uma tabela? Clico em Lista. As mesmas ordens, uma por linha, e clicando no título da coluna eu ordeno por data, por motorista ou por parceiro. O sistema lembra a visão que você escolheu. |
| cap02 | Clique em "Filtros": "Data agendada" "De" 01/11/2026 "Até" 30/11/2026; "Parceiro" → "Depósito Irmãos Siqueira"; a câmera em "As solicitadas aparecem sempre, independente da data."; "Limpar Filtros". | Nos Filtros, eu escolho o período, o status e o parceiro. Repara no aviso: as solicitadas aparecem sempre, pra nenhum pedido ficar escondido. Depois, Limpar Filtros. |
| cap05 | Antes de fechar: em "Parceiro da coleta" clique em "Sem cadastro": "Nome do solicitante *", "Telefone" e "Endereço completo * — obrigatório sem cadastro" (só mostra, volta para "Cadastrado"). Entra no cap03, depois da linha do Marcelo. | No Sem cadastro, basta o nome de quem pediu, o telefone e o endereço completo, que aqui é obrigatório, porque é o único jeito do motorista chegar. |
| cap06 | No cartão "#8", em vez do botão, o robô arrasta o cartão de "Agendada" para "A caminho" (mesmo aviso "Status alterado para A caminho"). | Dá pra clicar em A caminho ou arrastar o cartão pra próxima coluna, como eu faço aqui. |
| cap06 | Na tela "Ordem #8", parte "Entreguei": "Tipo de equipamento" → "Bag 1 m³"; aparece o campo de quantidade; digita 10; "Adicionar": a linha "Bag 1 m³" "Qtd. 10". | O Depósito também pediu bags. Como o bag é por quantidade, eu só digo quantos ficaram: dez. |
| cap06 | Depois da ficha da #8: abre o cartão "#7" (Marcelo Tavares, "Sem cadastro") em "Preencher"; a câmera no aviso "Sem cadastro — esta coleta não tem fornecedor vinculado..." e no botão "Cadastrar como fornecedor" (não clica). | Na coleta sem cadastro não dá pra deixar nem recolher caçamba, porque o sistema precisa saber com quem ela ficou. Se o Marcelo virar fornecedor, o botão Cadastrar como fornecedor cria o cadastro e liga nesta ordem. |
| cap08 | No detalhe do FKD2E41, clique no menu de ações: "Editar" e "Excluir" (não clica). No "Novo veículo", depois da tara: digita 7 em "Tara (kg)", aparece "Valor parece estar em toneladas — informe em quilos (ex.: 32.000)."; corrige para 7100. | Cada veículo e cada motorista tem Editar e Excluir no menu. Uma dica: tara e capacidade vão sempre em quilos. Se você digitar sete no lugar de sete mil e cem, o sistema avisa. E a capacidade em metros cúbicos vai até novecentos e noventa e nove, que é o limite da nota de transporte. |
| cap09 | Clique em "Novo tipo": "Novo tipo de equipamento", "Nome *" "Palete de madeira", chave "Cada unidade tem identificação própria" desligada; "Cadastrar". | Pra criar um tipo, Novo tipo. O palete eu conto por quantidade, então deixo desligada a opção de identificação própria. Com ela ligada, cada unidade ganha número, como a caçamba. |
| cap09 | Na Caçamba 02: "Editar" → "Condição" "Em manutenção" → "Salvar". | Caçamba furada? Em Editar, mudo a condição pra Em manutenção. E a que não volta mais fica como Baixada. |
| cap09 | Em "Onde tudo está agora", bloco "Contados por quantidade": "Bag 1 m³", clique em "Ver saldo por fornecedor": a lista com os parceiros e as quantidades. | Os bags aparecem em Contados por quantidade. Em Ver saldo por fornecedor, eu vejo quantos estão com cada parceiro. |
| cap09 | Aba "Movimentações" → "Nova movimentação": "De *" "Minha base", "Para *" "Parceiro" → "Selecionar parceiro…" → "Cooperativa Recomeço"; linha "Bag 1 m³", "Quantidade" 10; "Registrar". Depois, no menu da linha: "Editar", "Excluir" (abre "Excluir movimentação?", "Motivo (opcional)", fecha em "Cancelar"); "Filtros" → "Mostrar anuladas". | Fora de uma coleta, eu lanço direto: dez bags da minha base pra Cooperativa Recomeço. Registrar. Errou? O menu da linha tem Editar e Excluir. A excluída não some: fica como anulada, com o motivo, e dá pra restaurar. As que vieram de uma ordem você corrige na própria ordem. |
| cap09 (fim) | Menu "Clientes e Fornecedores" → ficha do Depósito Irmãos Siqueira → aba "Coletas": "Com este parceiro agora" (Caçamba 05), "Coletas", "Movimentações de equipamento", botões "Movimentar equipamento" e "Agendar coleta". | E na ficha do parceiro tem a aba Coletas: o que está com ele agora, as coletas dele e as movimentações. Dali mesmo dá pra agendar outra coleta. |
| cap11 | A câmera em "Avisar quando chegar solicitação" (ligado). | E o Avisar quando chegar solicitação manda uma notificação a cada pedido novo do portal. |
| cap11 | Na ilustração das duas portas, acrescentar no filtro do portal um balão "escolha outro dia". | Se o parceiro pedir fora da regra, o portal explica o motivo e pede outra data. |

### Capítulo A (novo, depois do cap06) · Editar, cancelar e excluir (vinheta: ORDENS)

| Tela | Fala |
|---|---|
| Semente `t12/apos-cap06`; no cartão "#9", menu "Ações da ordem": "Visualizar", "Editar", "Excluir". | Nem toda coleta sai como combinado. No menu de cada cartão ficam o Visualizar, o Editar e o Excluir. |
| "Editar": a janela em página única; troca "Motorista" para "Edson Moura"; "Salvar". | O Jair não vai poder amanhã. Em Editar, troco o motorista pro Edson e salvo. |
| No cartão "#9", botão "Cancelada": "Cancelar coleta?" ("A ordem #9 será marcada como cancelada. Essa ação não pode ser desfeita."); clique em "Voltar". | Se o parceiro desmarcar, o botão Cancelada pede confirmação. A ordem cancelada fica no quadro, como registro. |
| No cartão "#8" (concluída), menu → "Excluir" → "Excluir ordem de coleta?" → "Excluir": abre "Não deu para excluir" com o motivo e "Cancelar ordem em vez disso"; "Fechar". [BACKEND: rpc `delete_collection_order` recusando com a mensagem do banco] | E o Excluir apaga de vez, mas só a ordem que não mexeu em nada. Esta já movimentou caçamba, então o sistema explica o motivo e não apaga. |
| A câmera no quadro. | Uma dica: criou por engano, exclui. Combinou e não aconteceu, cancela. Assim o relatório mostra o que foi desmarcado. |

Mundo: handler `delete_collection_order` (sucesso e recusa com texto em português). **Decisão:** esta cena mostra uma
janela de recusa; o roteiro tem a regra "nenhuma mensagem de erro encenada". Alternativa sem recusa: excluir uma ordem
de teste (#11, criada na semente) e só falar da trava.

### Capítulo B (novo, depois do A) · O relatório da coleta para o parceiro (vinheta: ACOMPANHAMENTO)

| Tela | Fala |
|---|---|
| Cartão "#8" → "Relatório": "Relatório de Coleta 8"; a câmera na barra "Copiar link", "Compartilhar no WhatsApp", "Imprimir". | Toda coleta concluída vira um relatório. Em cima, três botões: Copiar link, Compartilhar no WhatsApp e Imprimir. |
| A câmera desce por "Equipamentos" (Caçamba 03 recolhida, Caçamba 05 entregue). Clique em "Copiar link": aviso "Link do relatório copiado". | O link abre esta mesma página pro parceiro, sem senha: o que foi recolhido, o que foi entregue, e as fotos e assinaturas, se você usar. |
| "Voltar às ordens" → corpo do cartão "#8" → bloco "Relatório do Fornecedor": "Abrir link do Fornecedor" e "Copiar link". | Na ficha da ordem, o mesmo link aparece em Relatório do Fornecedor. |
| Portal da Cooperativa Recomeço, aba "Coletas": uma coleta concluída com "Ver relatório da coleta". | E no portal, o parceiro abre o relatório direto da lista de coletas dele. |
| "Configurações" → bloco "Relatório público": "Mostrar valores no relatório que o cliente abre" (desligado). | Uma dica: o link é público. Nas Configurações, você decide se os valores em reais aparecem nele. Esse link depende do Portal do Cliente no plano. |

Mundo: `public_short_code` na ordem 8, edge `collection-report` (já existe no cap06), uma coleta concluída da
Cooperativa na semente do portal. Não abrir o WhatsApp (só apontar o botão).

### Capítulo C (novo, depois do cap11) · Checklist e assinaturas (vinheta: CONFIGURAÇÕES)

| Tela | Fala |
|---|---|
| "Configurações", bloco "Checklist da coleta" → "Modelos de checklist" → "Novo modelo": "Nome *" "Coleta com caçamba"; "Criar modelo". | Quer que o motorista confira alguma coisa em toda coleta? É o checklist. Em Modelos de checklist, crio o modelo Coleta com caçamba. |
| "Gerenciar perguntas" → "Nova pergunta": "Pergunta *" "Local estava acessível para o veículo?", "Tipo de resposta" "Sim ou não", "Pergunta obrigatória" ligada; "Adicionar pergunta". | Cada pergunta tem um tipo de resposta. Esta é de sim ou não, e é obrigatória. |
| "Nova pergunta": "Foto da caçamba no local", tipo "Foto"; a câmera passa pela lista de tipos ("Texto livre", "Número", "Escolher uma opção", "Escolher uma ou mais opções", "Conforme / Não conforme / Não se aplica"). | Também dá pra pedir foto, número, texto ou uma escolha entre opções. E a ordem das perguntas você arrasta. |
| "Fechar"; em "Checklist padrão da empresa" escolhe "Coleta com caçamba": aviso "Checklist padrão definido"; liga "Exigir assinatura do responsável no local". | Agora escolho esse modelo como padrão da empresa e passo a exigir a assinatura de quem recebeu o motorista no local. |
| Quadro → cartão "#10" (agendada) → "Preencher" → "Iniciar coleta"; blocos "Checklist" e "Assinatura"; a câmera em "Falta para concluir: ...". | Na próxima coleta, a tela da ordem já traz o checklist e a assinatura. Enquanto faltar alguma coisa obrigatória, o sistema mostra o que falta pra concluir. |
| Responde "Sim", assina em "Responsável no local"; o aviso some (não conclui: a foto fica para a fala). | O motorista responde pelo celular, o responsável assina na tela, e tudo isso sai no relatório da coleta. |

Mundo: tabelas de modelo e perguntas do checklist (nomes na migração `20260924220000_collection_checklist_photos_signature.sql`),
`collection_settings.checklist_template_id`, respostas e assinatura da ordem; a pergunta de foto não é respondida no
vídeo (sem câmera no robô). Ordem 10 precisa da data de hoje ou a cena usa outra ordem agendada.

### Capítulo D (novo, depois do cap09; só se o Kaik aprovar) · Onde está o caminhão (vinheta: FROTA)

| Tela | Fala |
|---|---|
| Menu → "Rastreamento" ("Acompanhe a frota em tempo real"): o mapa com o Tiago Freitas "Ao vivo" e a lista "Motoristas no mapa". | Com a coleta a caminho, o Rastreamento mostra no mapa onde está cada motorista. |
| A câmera no selo "Ao vivo" e na frase "O círculo ao redor do ponto é o raio de incerteza do GPS...". | A posição vem do celular do motorista, enquanto ele está com a ordem aberta. O círculo em volta mostra a margem do GPS. |
| "Trajeto de uma coleta" → escolhe a ordem 8: a linha do trajeto. | E em Trajeto de uma coleta, dá pra rever o caminho de uma ordem. |
| Tela "Ordem #7": aviso "Localização em registro — ...". | O motorista sempre vê o aviso de que a localização está sendo registrada. Sem sinal, a coleta segue normal. Pra aparecer no mapa, ele precisa ter login no sistema. |

Mundo: motorista ligado a um usuário, `collection_driver_locations` com pontos fictícios em Taubaté/Tremembé, tiles do
mapa (rede externa: gravar com tiles locais ou imagem estática, senão o mapa sai em branco). É o item mais caro da lista.

## 4. Estimativa

| Bloco | Palavras | Segundos de fala |
|---|---|---|
| Trechos nos capítulos existentes (14) | ~520 | ~200 |
| Capítulo A · Editar, cancelar e excluir | ~130 | ~50 |
| Capítulo B · Relatório para o parceiro | ~135 | ~52 |
| Capítulo C · Checklist e assinaturas | ~150 | ~58 |
| Capítulo D · Rastreamento (condicional) | ~105 | ~40 |
| **Total** | **~1.040** | **~400 s (~360 s sem o D)** |

Capítulos novos: 3 certos (A, B, C) e 1 condicional (D). A aula vai de ~13 min para ~20 min de vídeo (com vinhetas e
esperas). Sementes novas: `t12/apos-cap06b`, `apos-cap06c`, `apos-cap11b` (e `apos-cap09b`).

## Depende de decisão
1. Rastreamento entra na aula (capítulo D) ou continua fora? O motivo registrado na TRILHA ("Em breve") só vale para "Rotas".
2. Capítulo A: mostrar a janela "Não deu para excluir" (é recusa do sistema) ou só falar da trava.
3. O mundo liga o Cato? Se sim, o botão flutuante entra em todos os quadros regravados.
4. Pedido de coleta pelo portal aparece aqui (cap07) e na T20 (cap08): manter os dois ou encurtar um.
