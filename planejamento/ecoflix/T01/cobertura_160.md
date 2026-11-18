# Cobertura 1.60.10 · T01 · Sua conta e sua empresa

Auditoria de 18/11/2026, só leitura de código (`/dev/shm/ecoflix-src`, 1.60.10, `5290be4cd`) contra o roteiro escrito na
1.59.154 (`f37573ea0`). Caminhos relativos a `src/`. Nada foi editado fora deste arquivo.

**Resumo do diff nas telas da aula:** das telas do `inventario.md`, só três arquivos mudaram:
`components/settings/SettingsUsabilityContent.tsx` (assinaturas), `pages/Registration.tsx` (só bastidor) e
`contexts/EntityTerminologyContext.tsx` (só bastidor). `CompanySettings.tsx`, `Auth.tsx`, `ForgotPasswordFlow.tsx`,
`SidebarMenuContent.tsx`, `CondicoesPagamentoTab.tsx`, Aparência, Atalhos, `ResetSystemDialog.tsx` e
`TermsOfServiceModal.tsx` estão idênticos: os números de linha do inventário continuam valendo. O que mais pesa na
regravação não é texto de tela: são três elementos novos que aparecem **por cima de toda tela logada**.

## 1. Mudou no app

### Toda tela logada (caps 03, 04 no fim, 05 a 12)

| # | O que mudou | Texto exato e onde | Efeito na aula |
|---|---|---|---|
| M1 | Faixa vermelha fixa no topo, nova regra (agora olha o cofre de certificados) | "Reenvie seu certificado A1 para continuar emitindo notas" / "O motor fiscal próprio precisa do arquivo A1 (.pfx ou .p12) e da senha. Envie em Configurações Fiscais → Certificado para voltar a emitir." / botões "Reenviar certificado agora" e "Não mostrar novamente" (`components/notifications/DfeCertificateNoticeBanner.tsx:124-153`) | Apareceu em toda tela da varredura (`rec/t01/_ens/_debug/falha-01-waitFor.png`). Só aparece com o módulo `notas_fiscais` e emitente sem certificado no cofre. O T01 não fala de nota: o mundo precisa sumir com ela (ver 3, "Mundo"). |
| M2 | Botão flutuante do Cato com balão de dica (1.60.0), canto inferior direito | Balão com a dica e "Abrir Cato"; botão "Abrir o Cato" / "Abrir 1 notificação do Cato"; fechar "Fechar dica do Cato" (`components/cato/CatoFab.tsx:295-332`). Só com `companies.cato_enabled` e a permissão `action_use_cato` (`components/layout/AppLayout.tsx:267-283`) | O balão cobre o canto de baixo à direita (na varredura, cobriu a chave "No comprovante" do cap08). Cato é a T21: no T01, o mundo deve gravar com o balão já visto (ver "Mundo"). O botão em si pode ficar, é a tela real. |
| M3 | Janela "Sistema atualizado" ao entrar depois de uma versão nova (componente sem mudança; aparece porque a versão mudou) | "Novidades" / "Sistema atualizado" / "v1.60.10 já está no ar" / "Confira o que mudou nesta atualização." / "Ver novidades" (`components/VersionUpdateNotification.tsx:51-102`) | Derrubou dois capítulos na varredura: no cap07 cobriu o seletor "Reinício da numeração" e no cap09 o clique na aba caiu em "Ver novidades" e abriu "Histórico de Versões" (`/atualizacoes`). Não é mudança de rótulo: os textos "Nenhum (segue direto)" (`CompanySettings.tsx:1488`) e "Configure preferências gerais de usabilidade do sistema" (`SettingsUsabilityContent.tsx:459`) continuam iguais. |
| M4 | Rodapé mostra a versão | "EcoSistema v1.60.10" (visto nas capturas) | O cabeçalho do `roteiro.md` cita "rótulos como no código da 1.59.154": trocar para 1.60.10 na revisão. |

### cap01 · Criar a conta
- **M5 (bastidor)** O cadastro manda um campo novo, `acquisition_attribution`, para a edge `self-register`
  (`pages/Registration.tsx:726` e `:738`). Nada muda na tela. O handler falso só precisa aceitar o campo a mais.
- A falha "Senha forte." da varredura **não é mudança do app**: a varredura usa senha sorteada, sem caractere especial, e
  a tela mostra "Senha boa. Deve conter:" (`components/PasswordStrengthIndicator.tsx:28-29` e `:67`). Com
  `ReciclaVale#26` continua saindo "Senha forte".

### cap05 e cap06 · Dados, contato e endereço
- **M6 (1.60.10)** As cinco chaves "Exibir nos documentos" (nome, CNPJ/CPF, endereço, telefone e e-mail) passam a nascer
  **ligadas no banco** em conta nova (`supabase/migrations/20261118125500_company_document_visibility_defaults.sql:5-10`;
  nota de versão em `config/version.ts:21`). Empresa antiga não muda. Na tela nada mudou
  (`components/CompanySettings.tsx:1051`, `:1077`, `:1249`, `:1260`, `:1288`), e o roteiro já mostra todas ligadas. Muda a
  fala: hoje ela só diz que a chave "decide se ele sai no papel"; falta dizer que já vem ligada (proposta P2). O 2º
  endereço continua nascendo **desligado** (`CompanySettings.tsx:182`).

### cap09 · O jeito do pátio (Usabilidade)
- **M7 (1.59.155)** "Assinaturas no comprovante" mudou de texto e ganhou um seletor
  (`components/settings/SettingsUsabilityContent.tsx:878-927`). O roteiro não mostra esse item (entra em "Falta
  cobrir"), mas ele fica entre "Lucro no Comprovante" e "Exigir cliente/fornecedor no Ticket de Pesagem", por onde a
  câmera passa. Textos novos:
  - descrição: "Linhas para assinar no rodapé. Escolha quem assina: o operador, o cliente/fornecedor ou os dois. No ticket
    de pesagem, o operador aparece como Empresa." (`:897`)
  - dica: "Coloca linhas para assinar no rodapé do comprovante. Você escolhe se saem os dois, só o cliente/fornecedor ou
    só o operador. No ticket de pesagem, o campo do operador é o da Empresa." (`:891`)
  - com a chave ligada aparece "Quem assina" (`:909`) com "Operador e cliente/fornecedor", "Só o cliente/fornecedor" e
    "Só o operador" (`:920-922`); toast "Assinaturas do comprovante atualizadas" (`:301`). Ligar ou desligar a chave:
    "Assinaturas ativadas no comprovante" / "Assinaturas removidas do comprovante" (`:325-326`).
  - "cliente/fornecedor" segue a nomenclatura da empresa: invertida, vira "fornecedor/cliente" (`:84`).
- **M8 (bastidor)** A aba agora lê `companies.receipt_signature_mode` (`:116`; coluna criada em
  `supabase/migrations/20261109123700_add_receipt_signature_mode.sql`, padrão `both`). O backend falso precisa da coluna.

### Idioma (toda tela logada, sem efeito visível em português)
- **M9 (1.59.155)** O idioma agora vem do perfil do usuário em todo o app logado, e não mais do que o navegador guardou
  (`hooks/useLanguagePreference.tsx:58-76`, `components/layout/AppLayout.tsx:225-228`). Perfil sem idioma = português.
  Para a gravação nada muda, desde que `profiles.preferred_language` do Rafael esteja nulo ou `pt-BR`.

### Achados antigos que continuam no 1.60.10 (do `propostas_fala.md`)
- Selo "MASTER" some do card da conta: a chave `["user-profile", id]` segue dividida entre
  `components/layout/SidebarMenuContent.tsx:128` e `components/support/SupportTriageDialog.tsx:182`. A captura da varredura
  mostra o card sem o selo. A troca de fala proposta lá (tirar a frase do selo) continua valendo.
- O item do menu é "Meu Perfil" (`i18n/locales/pt-BR/navigation.json:24`), não "Perfil".
- Novo, pequeno: em "Variáveis disponíveis" a tela diz "{AAAA} — ano (2 díg)" (`CompanySettings.tsx:1564`) e de fato
  `{AAAA}` sai com dois dígitos (`lib/orderNumber.ts`). Não ler "ano com quatro dígitos".

## 2. Falta cobrir

"Vale?" = sim (trecho ou capítulo), citar (uma frase) ou não.

### Cadastro e login (caps 01 a 04)
| Função (arquivo:linha) | Quando o cliente usa | Vale? |
|---|---|---|
| Lista de exigências da senha: "Pelo menos 8 caracteres", "Pelo menos 1 número", "Pelo menos 1 letra minúscula", "Pelo menos 1 letra maiúscula", "Pelo menos 1 caractere especial"; rótulos "Senha fraca / média / boa / forte" (`components/PasswordStrengthIndicator.tsx:15-29`) | Ao criar a senha: é o que faz o indicador chegar em "forte" | **Sim**, uma linha no cap01 (P1). A fala só diz "oito caracteres". |
| Erro "Este email já está em uso. Faça login ou use outro email." (inventário, seção 1) | Quem tenta cadastrar duas vezes | Citar, junto do "Continuar". |
| "Já tem uma conta? Fazer Login", "Voltar", olho de mostrar senha | Navegação básica | Não: óbvio na tela. |
| Botão do WhatsApp ("Respondemos em até 5 min") e seletor "Escuro" na página pública | Dúvida antes de criar a conta | Citar (uma frase no cap01). |
| Janela de outro acesso ativo (`pages/Auth.tsx:1317`, `SessionConfirmDialog`) | Mesmo usuário entrando em dois lugares | Não aqui: é do T2 (usuários). |
| "Entrar com Biometria" | Não aparece na prática (inventário, divergência 2) | Não. |
| Menu da conta: "Assinatura", "Tema", "Tutoriais \| EcoFlix", "Central de Ajuda", "Falar com o Suporte" (`components/layout/SidebarMenuContent.tsx:687-748`) | Todo dia | **Sim**, uma linha no cap03 (P3): a tela já mostra, a fala só cita o Perfil. Assinatura é da T0 (só o nome). |
| Trocador: "Sair desta conta" (`components/account-switcher/AccountSwitcherDropdown.tsx:277`) e "Sair de todas as contas" | Computador dividido, fim do expediente | **Sim**, uma linha no cap03 (P3). |

### Aba Empresa (caps 05 a 08 e 12)
| Função (arquivo:linha) | Quando o cliente usa | Vale? |
|---|---|---|
| "Substituir" e "Remover" do logo | Trocou a marca | Citar (já aparecem na tela do cap05). |
| "2º endereço" → janela "Segundo endereço", "Endereço (texto livre)", chave "Mostrar no comprovante junto do endereço principal", "Cancelar" / "Salvar"; depois a linha "2º endereço:" com o selo "No comprovante" ou "Oculto" (`components/CompanySettings.tsx:1283-1311`, `:1769-1808`) | Empresa com depósito ou segundo pátio | **Sim**, trecho no cap06 (P4). |
| "Fuso horário": "É a hora que vale no seu ponto eletrônico: a que aparece em cada batida e a que decide em que dia ela entra. Preenchemos pelo seu estado; só mexa se a sua cidade tiver fuso diferente." (`CompanySettings.tsx:1404-1422`) | Empresa fora do horário de Brasília | **Sim**, uma linha no cap06 (P4). O ponto em si é o T19. |
| Aviso de cidade sem código do IBGE (inventário, seção 6) | CEP não achado, cidade digitada à mão | Citar no cap06. |
| "Ticket de Pesagem" › "Compartilhar rascunhos de tickets entre operadores" (`CompanySettings.tsx:1442`) | Dois balanceiros | Não aqui: T8. |
| Campo livre do "Formato do número" e "Variáveis disponíveis:" ({NUM}, {NUM:4}, {MM}, {AAAA}, {AA}, {DD}); aviso "Seu formato não tem {NUM} ... este campo não será salvo (o formato anterior é mantido)." (`CompanySettings.tsx:1539-1567`) | Quem quer prefixo próprio ou outro arranjo | **Sim**, trecho no cap07 (P5). Hoje a fala só mostra os modelos prontos. |
| Modelos "Pontos" e "Ano/Nº" | Igual aos outros | Citar (a câmera já passa). |
| "Filial" › "É Filial" | Rede com matriz | Não aqui: T22. |
| "Histórico de Exclusões" › "Ver histórico" ("Veja quem excluiu o quê e quando — clientes, vendas, materiais e operações destrutivas.", `components/settings/SettingsCompanyContent.tsx:600-620`) | Auditoria | Citar no cap12 (P9): a câmera passa por cima e a tela é do T9. |
| Zerar Sistema: "Selecionar tudo" e as quatro caixas que a fala não lê ("Saldos de Clientes e Fornecedores", "Categorias Financeiras", "Contas a Pagar e Receber", "Funcionários e Movimentações"); "Toda operação fica registrada em log de auditoria." (inventário, seção 10) | Quem zera depois do teste, guardando o cadastro | **Sim**, completar o cap12 (P9): o caso de uso real é zerar só uma parte. |
| "Alterar Senha": mínimo de 6 caracteres | Já mostrado | Não. |

### Aba Usabilidade (cap09), o maior buraco da aula
| Função (arquivo:linha em `SettingsUsabilityContent.tsx`) | Quando o cliente usa | Vale? |
|---|---|---|
| Janela "Inverter Cliente e Fornecedor?" ao mexer na chave | Confirmação | Citar (o roteiro não clica, e deve continuar sem clicar). |
| "Permitir Edição de Itens" ("Editar peso, impureza/tara e valor de materiais já incluídos", `:683-698`) | Errou o peso de um item no pedido | **Sim**, uma linha (P6). |
| "Múltiplas Tabelas de Preço" (`:759-774`) | Atacado e varejo | Citar e mandar para o T3. |
| "Mostrar só peso líquido" ("Oculta a tara nas notinhas e na tabela de materiais; mostra apenas o peso líquido (bruto − tara).", `:852-867`) | Pátio que não quer mostrar a tara no papel | **Sim** (P7). |
| "Assinaturas no comprovante" e "Quem assina" (`:878-927`), **novidade 1.59.155** | Pátio que colhe assinatura do fornecedor | **Sim** (P7). |
| "Estilo do comprovante térmico": "Compacto" e "Nome em destaque", vale para a empresa inteira (`:1004-1081`) | Nome de material comprido no cupom | **Sim** (P7). |
| "Marca de ticket não valorizado" (`:935-950`) e "Permitir forma de pagamento no ticket de pesagem" (`:1147-1162`) | Ticket de pesagem | Não aqui: T8 (citar que ficam nesta aba). |
| "QR de fotos no comprovante" (`:961-993`, só com o módulo `portal_cliente`) | Fotos do pedido | Não aqui: T20. |
| "Rastreabilidade do dinheiro físico (Cofre)" | Caixa | Já citado, T6. |
| "Regionalização": "Idioma do Sistema" ("Português (Brasil)", "English (USA)", "Español (América Latina)", `i18n/index.ts:148-155`; tela `:1189-1229`) e "Moeda do Sistema" (`:1239-1275`), **regra nova 1.59.155** | Funcionário que prefere outro idioma; navegador em inglês | **Sim** (P8). |
| "Agenda" › "Exibir Feriados" (`:1296-1299`) | Agenda | Citar e mandar para o T25. |
| "Guia de configuração" › "Reativar guia de configuração" ("Reabre o passo a passo de configuração inicial do sistema.", `:1336-1348`) | Quem fechou o guia sem terminar | **Sim**, uma linha (P8). |

### Condições de Pagamento, Aparência, Atalhos (caps 10 e 11)
| Função | Quando usa | Vale? |
|---|---|---|
| Botão "Padrão" (estrela) nas outras condições; "Editar" abre a mesma janela com "Salvar"; "Excluir condição?"; selo "Inativa" (inventário, seção 8) | Trocar a condição mais usada | Citar: a fala já mostra chave, Editar e Excluir; falta só a estrela (P10). |
| Erro "A soma dos percentuais deve ser 100%. Atual: X%" | Parcela errada | Já coberto pela fala ("sem fechar os cem, não salva"). |
| Chave "Atalhos de Teclado" (desliga todos) e a dica "Atalhos não funcionam quando você está digitando em campos de texto" (inventário, seção 9) | Quem esbarra nos atalhos | **Sim**, uma linha no cap11 (P10). |
| "Ações Rápidas" da busca do Ctrl+K | Atalho de criação | Citar. |
| Aba "Integrações" (impressora e balança, `components/settings/SettingsIntegrationsContent.tsx:194-627`) | EcoTray | Não aqui: T5. O cap05 lista as abas e não diz para onde vai essa: citar "é o tutorial da balança e da impressora". |

### Fora das telas da aula, mas que o cliente vê no caminho
- Janela "Sistema atualizado" e a tela "Histórico de Versões" (`/atualizacoes`): nenhuma aula cobre (busca nos roteiros
  sem resultado). Não é tela do T01. Sugestão: uma frase na T0 ou no T25. **Decisão**.
- Faixa do certificado A1: T16.
- Cato: T21.

## 3. Proposta

Falas no tom da aula; "→" marca troca de linha existente. Rótulos entre aspas como no código.

**P1 · cap01, troca da linha da senha**
| Tela | Fala |
| --- | --- |
| Digita `ReciclaVale#26` em "Senha*"; zoom na lista sob o campo: "Senha forte. Deve conter:" com os cinco itens marcados, de "Pelo menos 8 caracteres" a "Pelo menos 1 caractere especial". Repete em "Confirmar Senha*". | → A senha precisa de pelo menos oito caracteres. Embaixo, o sistema vai marcando o que ela já tem: número, letra minúscula, letra maiúscula e um caractere especial. Com tudo marcado, aparece Senha forte. Depois eu repito a mesma senha pra confirmar. |

**P2 · cap05 e cap06, dados visíveis por padrão (1.60.10)**
| Tela | Fala |
| --- | --- |
| cap05: zoom em "Nome da Empresa" e na chave "Exibir nos documentos", ligada; a câmera desce um pouco e mostra a mesma chave no "CNPJ/CPF", também ligada. | → O nome já veio do cadastro. E a chave do lado, Exibir nos documentos, decide se ele sai no papel. Em conta nova, ela já vem ligada. |
| cap06: zoom nas duas chaves "Exibir nos documentos" do contato e, descendo, na do "Endereço da empresa", todas ligadas. | → Cada dado tem a sua chave Exibir nos documentos: nome, CNPJ, telefone, e-mail e endereço. Todas já começam ligadas, então o comprovante sai completo sem você mexer em nada. |

**P3 · cap03, o menu da conta inteiro**
| Tela | Fala |
| --- | --- |
| Menu aberto: o mouse passa por "Meu Perfil", "Assinatura", "Tema", "Tutoriais \| EcoFlix", "Central de Ajuda" e "Falar com o Suporte", sem clicar. | → Clicando nele, abre esse menu. Em Meu Perfil ficam a sua foto e o seu nome. Logo abaixo, a Assinatura, o Tema, os tutoriais da EcoFlix, a Central de Ajuda e o Falar com o Suporte. |
| Trocador aberto: zoom no botão "Sair desta conta", na conta ativa, e em "Sair de todas as contas", sem clicar. | (linha nova, depois de "Cabem até cinco contas.") Pra tirar uma conta deste computador, é o Sair desta conta. E o Sair de todas as contas limpa a lista inteira, bom pra um computador que vai mudar de mão. |

**P4 · cap06, segundo endereço e fuso (trecho novo, depois da prévia)**
| Tela | Fala |
| --- | --- |
| Sobe ao título "Endereço da empresa" e clica em "2º endereço": abre "Segundo endereço", com "Endereço (texto livre)" e a chave "Mostrar no comprovante junto do endereço principal", desligada. | Se a empresa tem outro endereço, como um depósito, o botão Segundo endereço abre um campo de texto livre. E a chave decide se ele sai no comprovante junto do principal. |
| Clica em "Cancelar". | A Recicla Vale só tem um pátio, então eu cancelo. |
| Desce até "Fuso horário" (preenchido pelo estado) e o texto "É a hora que vale no seu ponto eletrônico...". | Por último, o Fuso horário. Ele vem preenchido pelo estado e é a hora que vale no ponto eletrônico dos funcionários. Só mexe se a sua cidade tiver um fuso diferente. |

**P5 · cap07, formato livre (trecho novo, depois dos modelos)**
| Tela | Fala |
| --- | --- |
| Zoom em "Variáveis disponíveis:" com `{NUM}`, `{NUM:4}`, `{MM}`, `{AAAA}`, `{AA}` e `{DD}`. | Se nenhum modelo servir, dá pra montar o seu. Essas são as peças: o número do pedido, o mês, o ano e o dia. |
| No campo do formato, apaga e digita `RV-{NUM:4}`: "Exemplo: RV-0030". | Por exemplo, as letras da empresa na frente e o número com quatro casas. O exemplo embaixo já mostra como fica. |
| Apaga o `{NUM:4}` (fica `RV-`): aparece em vermelho "Seu formato não tem {NUM} ..."; clica em "Padrão" e volta a "#{NUM}". | Só não pode faltar o número do pedido. Sem ele, o sistema avisa e não salva, porque todo pedido ficaria igual. Volto pro Padrão. |

**P6 · cap09, edição de itens e tabelas (duas linhas novas, depois de "Arredondar Pagamentos")**
| Tela | Fala |
| --- | --- |
| Zoom em "Permitir Edição de Itens" ("Editar peso, impureza/tara e valor de materiais já incluídos"); passa o mouse na dica. | O Permitir Edição de Itens deixa corrigir um material que já entrou no pedido. Pesou cem quilos e eram noventa e cinco? É só clicar no item e arrumar, sem tirar e colocar de novo. |
| A câmera passa por "Múltiplas Tabelas de Preço", sem parar. | Logo abaixo, as Múltiplas Tabelas de Preço, que a gente vê no tutorial de materiais. |

**P7 · capítulo novo cap09b · O comprovante do seu jeito (vinheta: COMPROVANTE)**, semente `apos-cap08`, aba "Usabilidade"
| Tela | Fala |
| --- | --- |
| Aba "Usabilidade", seção "Pedidos e Pagamentos"; a câmera desce até "Mostrar só peso líquido". | Ainda na Usabilidade, três ajustes mudam o papel que o fornecedor leva. |
| Zoom em "Mostrar só peso líquido" e na dica "Ex: comprou 100kg com 5kg de tara? ... a notinha mostra direto 95kg (líquido)."; desligada. | O primeiro é o Mostrar só peso líquido. Ligado, o comprovante esconde a tara e mostra direto o peso que valeu. Desligado, sai o peso bruto e a tara, um embaixo do outro. |
| Liga "Assinaturas no comprovante": toast "Assinaturas ativadas no comprovante" e aparece "Quem assina", em "Operador e cliente/fornecedor". | O segundo são as Assinaturas no comprovante. Ligando, o papel ganha linhas pra assinar no rodapé. |
| Abre "Quem assina": "Operador e cliente/fornecedor", "Só o cliente/fornecedor" e "Só o operador". [ZOOM: as três opções, a lista inteira] | E em Quem assina você escolhe: o operador e o fornecedor, só o fornecedor ou só o operador. |
| [ILUSTRAÇÃO: o rodapé do cupom: na palavra "duas", duas linhas lado a lado, "Operador" e "Fornecedor"; na palavra "sozinha", uma delas some e a outra cresce até a largura inteira do papel] | Com as duas, cada uma fica de um lado. Sozinha, a linha ocupa a largura toda do papel, e sobra espaço pra assinar. |
| De volta à tela: escolhe "Só o cliente/fornecedor"; toast "Assinaturas do comprovante atualizadas". | A Recicla Vale quer só a assinatura de quem entregou o material. Escolho, e o sistema já grava. |
| Zoom na descrição "No ticket de pesagem, o operador aparece como Empresa.". | Isso vale no comprovante de compra e venda e no ticket de pesagem. No ticket, a linha do operador sai como Empresa. |
| Desce a "Estilo do comprovante térmico": os cartões "Compacto" (marcado) e "Nome em destaque", cada um com o desenho da linha. | O terceiro é o Estilo do comprovante térmico, que vale só pro cupom da bobina. No Compacto, o nome do material fica do lado dos valores. |
| Clica em "Nome em destaque" e volta para "Compacto". | No Nome em destaque, o nome vai em cima, numa linha só dele. É bom pra material de nome comprido. Essa escolha vale pra empresa inteira. |
| A câmera passa por "Marca de ticket não valorizado" e "Permitir forma de pagamento no ticket de pesagem", sem parar. | As outras opções daqui são do ticket de pesagem, e a gente vê no tutorial dele. |

**P8 · cap09, fim da aba (trecho novo, depois do "Exigir cliente/fornecedor")**
| Tela | Fala |
| --- | --- |
| Desce a "Regionalização" e abre "Idioma do Sistema": "Português (Brasil)", "English (USA)" e "Español (América Latina)"; Esc fecha em "Português (Brasil)". | No fim da aba, a Regionalização. O Idioma do Sistema pode ser português, inglês ou espanhol. |
| [ILUSTRAÇÃO: o idioma acompanha a pessoa: um cartão de usuário com a bandeira do Brasil; na palavra "qualquer", ele aparece igual num computador, num celular e numa maquininha, mesmo com o navegador mostrando "EN"] | Essa escolha fica gravada no seu usuário. Então ela vale em qualquer computador ou celular em que você entrar, mesmo que o navegador esteja em outro idioma. |
| Zoom em "Moeda do Sistema", sem abrir. | Do lado fica a Moeda do Sistema, pra quem trabalha com outra moeda. |
| Passa por "Agenda" › "Exibir Feriados" e para em "Guia de configuração" › "Reativar guia de configuração", sem clicar. | Os feriados da agenda ficam pro tutorial da rotina. E o botão Reativar guia de configuração traz de volta o passo a passo do começo, se você fechou antes de terminar. |

**P9 · cap12, completar a Zona de Perigo**
| Tela | Fala |
| --- | --- |
| Na descida até "Segurança", pausa curta em "Histórico de Exclusões" › "Ver histórico". | (linha nova, antes da Zona de Perigo) Aqui também fica o Histórico de Exclusões, que mostra quem apagou o quê. Ele aparece no tutorial de pedidos. |
| Lista do "Zerar Sistema": a câmera desce pelas dez caixas e para em "Selecionar tudo". | → Depois, ele mostra tudo o que pode ser apagado: clientes e fornecedores e os saldos deles, materiais e estoque, o financeiro com as categorias e as contas a pagar e receber, os funcionários, os pedidos e as notas. Tudo já vem marcado. |
| Desmarca "Clientes e Fornecedores" e "Cadastro de Materiais" e marca de novo (ou só zoom, sem clicar). | (linha nova) Dá pra desmarcar o que você quer guardar. Quem testou o sistema com dados de mentira costuma zerar os pedidos e o financeiro e manter os cadastros. |

**P10 · caps 05, 10 e 11, frases soltas**
| Tela | Fala |
| --- | --- |
| cap05, linha das abas: a mesma tela. | → Lá em cima ficam as abas. Neste tutorial a gente passa por Empresa, Usabilidade, Condições de Pagamento, Aparência e Atalhos. Usuários e Permissões é o próximo tutorial, e Integrações é o da balança e da impressora. |
| cap10, última linha: zoom na estrela "Padrão" de uma condição que não é a padrão. Precisa de uma segunda condição na lista (ver "Mundo"). | → A chave do lado desliga a condição sem apagar. Se a empresa tiver outra condição, a estrela dela troca qual é a padrão. E na hora de parcelar uma venda, a padrão aparece no alto da lista. |
| cap11: zoom na chave "Atalhos de Teclado" e no quadro "Dicas". | (linha nova, depois da aba Atalhos) Os atalhos não disparam enquanto você digita num campo. E se atrapalharem, essa chave desliga todos de uma vez. |

**Recap (cap13):** acrescentar uma linha: "Ajustou o papel do comprovante, com o peso líquido e as assinaturas, e viu o idioma do sistema."

### Mundo: o que precisa existir para gravar no 1.60.10
- **Sumir com a faixa do A1 (M1):** tabela `dfe_certificate_notice_opt_outs` (hoje `TABELA_DESCONHECIDA` na varredura)
  com `dismissed_at` preenchido para a empresa, ou o cofre de certificados sem falta, ou a empresa sem `notas_fiscais`
  nas sementes do T01. Handler da RPC `fiscal_onboarding_status` (96 chamadas sem handler).
- **Balão do Cato (M2):** `localStorage` `cato_adoption_nudge_<empresa>_<usuário>` já com contagem e data recente (ou
  `companies.cato_enabled` falso nas sementes do T01, se a decisão for esconder o Cato até a T21); handler da RPC
  `track_cato_adoption_event`.
- **Janela de versão (M3):** o `storage` de cada capítulo logado com a última versão vista = `1.60.10`; semear
  `changelog_entries` (hoje sem semente).
- **Assinaturas (M7, M8):** coluna `companies.receipt_signature_mode` (`both`) e `show_signatures_on_receipt` (falso na
  `apos-cap08`); o update das duas colunas vira a semente `apos-cap09b`.
- **Padrões (M6):** as sementes `inicio` em diante com as cinco `show_*_in_documents` verdadeiras e
  `show_address_2_in_documents` falsa.
- **Idioma (M9):** `profiles.preferred_language` nulo ou `pt-BR` para o Rafael; nenhum capítulo troca de idioma (o
  seletor abre e fecha com Esc).
- **Cadastro (M5):** o handler de `self-register` aceita `acquisition_attribution` no corpo.
- **P5:** nada novo (o formato só grava se o robô sair do campo com valor válido; o capítulo volta ao "Padrão").
- **P10, cap10:** uma segunda condição na semente (por exemplo "À vista") para a estrela aparecer, ou a linha fica só
  falada, sem zoom.
- Tabelas sem semente vistas na varredura e que não afetam a tela do T01: `company_origins`, `cs_agents`, `affiliates`,
  `salespeople`, `biometric_credentials`; `GET /auth/v1/health` sem handler.

## 4. Estimativa

| Proposta | Palavras a mais | Segundos (2,6 palavras/s) |
|---|---|---|
| P1 senha | 28 | 11 |
| P2 padrões visíveis | 32 | 12 |
| P3 menu e trocador | 55 | 21 |
| P4 2º endereço e fuso | 77 | 30 |
| P5 formato livre | 78 | 30 |
| P6 edição de itens | 52 | 20 |
| P7 cap09b (novo) | 232 | 89 |
| P8 idioma e guia | 104 | 40 |
| P9 Zona de Perigo | 68 | 26 |
| P10 frases soltas e recap | 70 | 27 |
| **Total** | **~796** | **~306 s de fala (5 min 06 s)** |

- **Capítulos novos: 1** (cap09b, "O comprovante do seu jeito", uma vinheta a mais). O resto são trechos em capítulos
  que já existem. Duas ilustrações novas (rodapé das assinaturas; idioma que acompanha a pessoa).
- A aula passa de ~17 min para ~22 a 23 min de vídeo (fala + ações + vinheta).
- Alternativa mais curta: P8 dentro do cap09b e P4/P5 só falados (sem abrir janela nem digitar) cortam ~40 s.

## Depende de decisão
1. **Assinaturas ligadas no mundo?** O P7 deixa a Recicla Vale com "Só o cliente/fornecedor": todo comprovante das aulas
   seguintes (T7, T8, T9, T20) passa a sair com a linha de assinatura. Alternativa: mostrar e desligar de volta.
2. **Cato no T01:** botão visível sem balão (proposto) ou escondido até a T21.
3. **Janela "Sistema atualizado" e "Histórico de Versões":** ficam sem aula; cabe uma frase na T0 ou no T25.
4. **Selo "MASTER":** o defeito continua no 1.60.10; manter a fala sem o selo (já proposto no `propostas_fala.md`) ou
   corrigir o app antes de gravar.
5. **P9, desmarcar caixas no Zerar Sistema:** clicar de verdade nas caixas (sem confirmar) ou só zoom.
