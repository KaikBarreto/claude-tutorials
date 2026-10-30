# Inventário funcional · T3 — Clientes, Fornecedores e Equipamentos (Dominex)

> Base para o roteiro do tutorial "T3 · Clientes, Fornecedores e Equipamentos" da Domiflix (cerca de 35 min).
> Gerado em 29 e 30/10/2026 a partir do código de `/home/claude/kaikbarreto/dominextecnologia` (React + Vite + Supabase), versão do app `APP_VERSION = "1.37.56"` (`src/config/version.ts:1`).
> **Análise estática e somente leitura.** Nada foi executado e nenhuma tela foi vista rodando. Tudo vem do código. O que o código não permite afirmar está marcado com "(a confirmar)" e repetido na seção 15.

## Como ler

- Caminhos são relativos a `src/`, exceto os que começam com `supabase/`. Formato `arquivo:linha`.
- Texto entre aspas "assim" é o rótulo ou a mensagem exatamente como aparece na tela, em português. Fonte: `lib/i18n/messages/app/customers.ts` e `equipment.ts` (bloco `pt-br`). Alguns toasts são texto fixo dentro de hooks e componentes e estão citados no ponto onde aparecem.
- "Desktop" = janela com 1024 px ou mais. Abaixo disso, inclusive tablets, o app usa o layout de celular (`useIsMobile`, breakpoint 1024).
- `fn:...` é permissão por função e `screen:...` é permissão de tela. "Módulo" é item contratável (tabela `company_modules`) ou incluído no plano. Durante o teste grátis (trial) todos os módulos ficam liberados (seção 2.3).
- "Ficha" é o painel de detalhe de um cliente ou de um equipamento.
- Linhas "Celular:" resumem em uma frase o que muda no telefone.

---

## 0. Resumo para quem escreve o roteiro

### 0.1 A trilha atual da Domiflix contra o código

| # | Item atual da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Clientes: grade ou lista; busca por nome, documento ou razão social | **Parcial** | "Grade ou lista" só existe no celular e no tablet (menos de 1024 px), no seletor Lista/Grade. No computador a tela é mestre-detalhe: lista compacta à esquerda e ficha à direita, sem alternância. A busca do computador casa nome, documento, telefone, cidade, razão social, nome fantasia, e-mail, endereço e bairro (`pages/Customers.tsx:415-474`). |
| 2 | Cadastro, aba Contato: foto, tipo PF/PJ, telefones, e-mail, origem | **Bate** | Há mais: "Atende como" (só com PDV), interruptor "Receber mensagens pelo WhatsApp", "Data de Nascimento" e "Observações". O "Tipo" já vem como "Pessoa Jurídica". |
| 3 | Cadastro, aba Fiscal: busca por CNPJ + preenchimento automático do endereço | **Bate** | A busca dispara sozinha ao completar 14 dígitos (e pela lupa "Consultar CNPJ na Receita"), direto do navegador na BrasilAPI. Existe também busca por CEP no bloco "Endereço fiscal". Nenhum dos dois valida o dígito verificador (seção 9). |
| 4 | Catálogo de origens | **Bate** | Dois caminhos: botão "Configurar origens" e o botão "+" ao lado do campo "Origem". O catálogo nasce vazio; o botão "Criar origens padrão" cria 10. |
| 5 | Formulários de captação com link público | **Bate** | Botão "Formulários de captação". Link público `/cadastro/<nome>-<código>`. 17 campos configuráveis, texto de LGPD e data de expiração. Não há fila de aprovação: o cliente entra direto na lista. |
| 6 | Detalhe do cliente: abas Geral, Equipamentos, Histórico, Tarefas, Contratos, Financeiro | **Incompleto** | A ficha tem até **10 abas**: Geral, Equipamentos, Histórico, Tarefas, **Estoque**, **Chamados**, Contratos, **Documentos**, Financeiro e **Cobranças**. Chamados, Financeiro e Cobranças dependem de módulo ou permissão (seção 2). |
| 7 | Contatos e responsável no local, com WhatsApp direto | **Bate** | Card "Responsável no Local (falar com)" na aba Geral. Ao lado de Telefone e de Celular do cliente há um botão com o ícone verde do WhatsApp; em cada contato o WhatsApp é uma opção do menu da linha (`https://wa.me/55…`). O componente `CustomerWhatsAppLink` **não** é usado na ficha do cliente. |
| 8 | Tela Equipamentos: cadastro, categorias, criação rápida de cliente só com o nome | **Bate, com ajuste** | A criação rápida é o botão "+" ao lado de "Cliente *" no formulário do equipamento. A janela "Novo cliente" só exige o nome, mas também oferece CPF / CNPJ, E-mail (opcional) e Telefone (opcional). "Categorias" é uma aba da própria tela e **não** dá para criar categoria dentro do formulário do equipamento. |
| 9 | Campos personalizados de equipamento: criar, ordenar, obrigatório, visível | **Bate, com ajuste** | Botão "Configurar Campos". Salva sozinho, a cada clique, sem botão Salvar. Os seis campos padrão (Marca, Modelo, Nº de Série, Capacidade/Especificação, Local, Data de Instalação) são linhas da mesma configuração e também podem ser renomeados, ocultados, reordenados e excluídos. Só admin e gestor gravam. |
| 10 | Detalhe do equipamento: QR Code, etiqueta configurável, anexos, histórico de OS | **Bate, com ajuste** | São 4 abas (Geral, Anexos, Histórico / Tarefas, **Chamados**). O QR só aponta para o portal quando o cliente tem portal ativo; sem isso vira um texto `EQ-…` e os botões de link ficam desligados. Não existe botão para liberar anexo no portal na tela atual. |

### 0.2 Telas, abas e janelas que existem e a trilha não cita

Aba **Fornecedores** (lista, ficha com histórico de gastos, cadastro). Aba **Categorias** do equipamento. Aba **Portal** dentro do cadastro do cliente (link, senha, o que o cliente vê). Abas **Estoque**, **Documentos**, **Chamados** e **Cobranças** da ficha do cliente. Aba **Chamados** da ficha do equipamento. Tarefas simples (lista de itens) dentro do equipamento. Troca rápida de cliente ou de equipamento pelo nome, no cabeçalho da ficha. Mapa e botões "Abrir no Google Maps" e "Abrir no Waze" na ficha do cliente. Rascunho automático do cadastro de cliente. Filtro "Atende como" e a ação "Criar oportunidade no CRM" (módulos PDV e CRM).

### 0.3 O que mais costuma surpreender o roteirista (detalhes na seção 14)

1. O endereço do cliente fica na **aba Fiscal**, no bloco "Endereço fiscal". A aba Contato não tem endereço.
2. Criar um cliente **não abre** a ficha dele. Ele só aparece na lista.
3. Criar o cliente grava também as configurações do portal, mesmo que ninguém abra a aba Portal.
4. Em "Novo Equipamento", "Cliente *" e "Nome *" mostram o texto cru `customer_required` e `name_required` se ficarem vazios.
5. O QR do equipamento depende de o cliente ter portal ativo (o portal nasce ativo para todo cliente).
6. A busca de CNPJ precisa de internet (BrasilAPI) e dispara ao completar 14 dígitos, mesmo com dígito verificador inválido.
7. Editar o equipamento pela ficha recarrega a página inteira, sem aviso.
8. "Imprimir" a etiqueta abre outra janela e chama a impressão do navegador.
9. A ficha do cliente e a do equipamento mostram "Editar" e "Excluir" mesmo para quem não tem permissão (só a lista respeita).
10. Clientes vindos do formulário público têm Origem "public_form" (texto cru, sem ícone) e documento e telefone só com dígitos.
11. O interruptor "Receber mensagens pelo WhatsApp" é desligado a cada tecla do Celular até completar 10 dígitos: depois de digitar o número é preciso ligá-lo.

---

## 1. Mapa de navegação e rotas

### 1.1 Como chegar

| Tela | Menu (computador) | Menu (celular) | Rota |
|---|---|---|---|
| Clientes e Fornecedores | Grupo **Gestão** → "Clientes e Fornecedores" (`components/layout/SidebarMenuContent.tsx:113-116`, `TopNavbar.tsx:104-105`) | Barra inferior, item de Clientes (`MobileBottomNav.tsx:57`) ou Menu → Gestão (`MoreMenuDrawer.tsx:100-101`) | `/clientes` |
| Ficha do cliente | Clique numa linha da lista | Toque numa linha | `/clientes/<nome>-<código>` |
| Equipamentos | Grupo **Gestão** → "Equipamentos" | Só pelo Menu → Gestão (não há atalho na barra inferior) | `/equipamentos` |
| Ficha do equipamento | Clique numa linha | Toque numa linha | `/equipamentos/<nome>-<código>` |
| Formulário público de captação | Link gerado em "Formulários de captação" | idem | `/cadastro/<nome>-<código>` (rota pública, sem login) |
| Portal do cliente | Link em "Portal" ou no menu "Ações" da ficha | idem | `/portal/<token>` (com `?eq=<id>` abre direto o equipamento) |

Rotas em `App.tsx:144-150, 743-744, 798-801`. Em outros idiomas o caminho é traduzido por `lib/i18n/appRouteSlugs.ts:130-133`; o tutorial é em português.

### 1.2 Como as rotas funcionam

- `CustomersRoute` e `EquipmentRoute` renderizam **a mesma página** para a lista e para a ficha. No computador isso mantém a lista e a busca de pé quando a pessoa clica em outra linha. No celular, `/clientes/:id` mostra a ficha em tela cheia.
- Os endereços usam o formato `nome-do-cliente-<código de 12 letras e números>`. O código vem da coluna `public_short_code`, gerada por gatilho no banco (alfabeto `abcdefghjkmnpqrstuvwxyz23456789`). O endereço antigo com UUID continua funcionando e é trocado pelo bonito ao abrir (`utils/prettyLinks.ts:13-33, 103-115`; `pages/CustomerDetail.tsx:259`; `pages/EquipmentDetail.tsx:191-198`).
- Voltar da ficha do equipamento: se ela foi aberta pela aba Equipamentos de um cliente, volta para `/clientes/<id>` já na aba "Equipamentos"; senão volta para `/equipamentos` (`pages/EquipmentDetail.tsx:395`).

---

## 2. Permissões e módulos

### 2.1 Permissões (rótulos como aparecem no cadastro de usuários, `hooks/usePermissions.ts:62-63,105-108,129`)

| Permissão | Rótulo | O que controla neste módulo |
|---|---|---|
| `screen:customers` | tela Clientes | Entrar em Clientes e Fornecedores. Faz parte do plano básico. |
| `screen:equipment` | tela Equipamentos | Entrar em Equipamentos. Plano básico. |
| `fn:create_customer` | "Criar Cliente" | Botão "Novo Cliente" (desktop) e botão flutuante "Cliente" (celular). |
| `fn:edit_customer` | "Editar Cliente" | Ação "Editar" nas linhas da lista no celular. Também libera adicionar, ocultar e excluir arquivos na aba **Documentos** da ficha. |
| `fn:delete_customer` | "Excluir Cliente" | Ação "Excluir" nas linhas da lista no celular. |
| `fn:manage_equipment` | "Gerenciar Equipamentos" | "Novo Equipamento", botão "Campos" (celular) e ações Editar/Excluir nas linhas do celular. |
| `fn:view_customer_financial` | "Ver Financeiro do Cliente" | Aba **Financeiro** da ficha. Exige também `screen:finance` (`pages/CustomerDetail.tsx:148-149`). |
| `fn:manage_finance` | gerenciar financeiro | "Lançar despesa" e editar lançamentos na aba Financeiro (`CustomerDetail.tsx:154`). |
| `fn:delete_finance` | excluir financeiro | Excluir lançamento na aba Financeiro (`CustomerDetail.tsx:153`). |
| `fn:manage_inventory` | gerenciar estoque | "Cadastrar material" e ações da aba **Estoque** (`components/customers/CustomerStockTab.tsx:263-264`). |

Administrador e gestor passam por todas (`isAdminOrGestor()`). **O que a permissão NÃO protege:**

- No computador, "Configurar origens" e "Formulários de captação" aparecem para qualquer um com acesso à tela (`components/customers/CustomersPageChrome.tsx:60-73`).
- Os botões "Editar" e "Excluir" do cabeçalho da ficha do cliente e da ficha do equipamento não consultam `fn:edit_customer`, `fn:delete_customer` nem `fn:manage_equipment` (`CustomerDetail.tsx`, `EquipmentDetail.tsx`: não há checagem). Só as linhas da lista no celular consultam.
- "Configurar Campos" aparece sempre no computador (`components/customers/EquipmentPageChrome.tsx:57-60`), mas só admin e gestor conseguem gravar a configuração (regra do banco, `can_manage_system`).
- Fornecedores, Categorias de equipamento e Origens não têm checagem de `fn:` no front.

### 2.2 Módulos que mudam o que aparece

| Módulo | Onde muda |
|---|---|
| `pdv` (PDV e Loja) | Campo "Atende como" (Serviço/Loja) no cadastro; filtro "Atende como" (Todos, Serviço, Loja) na lista; aviso de "Fiado em aberto" ao excluir. |
| `crm` | Ação "Criar oportunidade no CRM" (menu "Ações" da ficha e linhas do celular). |
| `customer_portal` | Aba **Chamados** da ficha; ações "Copiar link do portal" e "Abrir portal". |
| `cobrancas` + conta de recebimento ativa | Aba **Cobranças** da ficha. |

A aba **Portal** do cadastro do cliente aparece sempre, sem depender de módulo.

### 2.3 Como o app decide se um módulo está ligado (`hooks/useCompanyModules.ts:114-243`)

Super administrador: tudo liberado. **Empresa em teste** (`companies.subscription_status = 'testing'` e sem data de expiração ou data futura): tudo liberado. Caso contrário vale `company_modules` da empresa ou os módulos incluídos no plano (`subscription_plans.included_modules`). **Para gravar o tutorial com todas as abas visíveis, basta a empresa de demonstração estar em teste.**

---

## 3. Clientes (aba "Clientes" de `/clientes`)

### 3.1 Cabeçalho e abas

- Título "Clientes e Fornecedores", subtítulo "Gerencie seus clientes e fornecedores" (`components/customers/CustomersPageChrome.tsx`).
- Abas sublinhadas: "Clientes" e "Fornecedores" (`CustomersPageChrome.tsx:80-89`).
- Botões do computador, só quando a aba "Clientes" está ativa (`:47`): **"Configurar origens"**, **"Formulários de captação"** e **"Novo Cliente"**. O último só aparece com `fn:create_customer` (`:40,68`). Os dois primeiros aparecem para todos.
- O cabeçalho continua na tela com a ficha aberta, porque lista e ficha são a mesma página.
- Salvar um cliente novo fecha a janela e **não abre a ficha**. A lista é recarregada e o cliente aparece na ordem alfabética.

### 3.2 Lista no computador (mestre-detalhe)

Componente `components/ui/ListDetailLayout.tsx`, usado em `pages/Customers.tsx:415-474`.

- Coluna da esquerda com o título **"Lista de Clientes"**. Cada linha mostra a foto do cliente (ou as iniciais num círculo; clicar na foto abre ela ampliada), o nome, embaixo `documento · telefone (ou celular) · cidade` e, à direita, a etiqueta **"PJ"** ou **"PF"**.
- **Busca**: caixa com o texto "Buscar clientes...". Compara o que foi digitado, sem diferenciar maiúscula de minúscula, com um trecho de: nome, documento, telefone ou celular, cidade (o que aparece na linha) e também razão social, nome fantasia, e-mail, endereço e bairro (`ListDetailLayout.tsx:165-171`). **Acento conta** (digitar "Antonio" não acha "Antônio") e o documento é comparado como está gravado, então "12345678" não acha "12.345.678/0001-90". Para a demonstração, busque por nome.
- **Ordem**: Nome (A-Z) e Nome (Z-A).
- **Tamanho da página**: 10, 25, 50, 100 ou Todos (padrão 25).
- A busca e a ordem ficam lembradas na sessão do navegador (chave `customers-list-detail`, `Customers.tsx:438`).
- Com o módulo PDV aparece o filtro "Atende como" (Todos, Serviço, Loja) no topo da lista.
- Clicar numa linha abre a ficha à direita e troca o endereço para `/clientes/<id>`; logo em seguida o app troca para a versão com nome (`CustomerDetail.tsx:259`).
- Painel direito sem seleção: **"Selecione um cliente"** / "Escolha um cliente na lista para abrir a ficha, as subabas e as ações disponíveis."
- Estados vazios e erro:
  - Nenhum cliente cadastrado: **"Nenhum cliente cadastrado"** / "Adicione um cliente para começar".
  - Busca sem resultado: **"Nenhum cliente encontrado"** / "Tente uma busca diferente".
  - Falha ao carregar: **"Erro ao carregar clientes"** / "Não foi possível conectar ao servidor. Tente novamente." com o botão **"Tentar novamente"**.
- As tabelas antigas do computador que ainda existem em `Customers.tsx` (por exemplo a coluna `colKind` na linha 714) são código que não roda mais: no computador só vale o mestre-detalhe.

### 3.3 Lista no celular e no tablet

Celular: janelas abaixo de 1024 px mostram `MobileListToolbar` + lista (`pages/Customers.tsx:302,385`).

- Busca "Buscar clientes..." **tolerante**: ignora acento, espaço sobrando e ordem das palavras ("marcos braga" acha "Marcos Antônio Moraes Braga"). Se o que foi digitado for só número (3 dígitos ou mais), compara apenas os dígitos, então telefone e documento com ou sem máscara funcionam (`lib/utils.ts:14-69`; `Customers.tsx:274-285`).
- Seletor **Lista / Grade** (`ViewModeToggle`) só existe aqui.
- Botões da barra: **"Origens"** e **"Formulários"** (o texto "Formulários" some em telas muito estreitas). Botão flutuante **"Cliente"** (só com `fn:create_customer`). Filtro "Atende como" com PDV.
- Páginas de 10 em 10.
- Ações por linha: **"Visualizar"**, **"Criar oportunidade no CRM"** (módulo CRM), **"Editar"** (`fn:edit_customer`), **"Excluir"** (`fn:delete_customer`).
- Vazio: "Toque em "Novo Cliente" para começar".

### 3.4 Janela "Novo Cliente" / "Editar Cliente"

Arquivo `components/customers/CustomerFormDialog.tsx` (formulário de 3 abas). Abre pelo botão "Novo Cliente", pelo botão flutuante "Cliente" no celular, pela ação "Editar" e pelo botão "Editar" da ficha. Abaixo de 1024 px o mesmo conteúdo abre como painel que sobe de baixo (gaveta), com o botão "Fechar" no canto e o rodapé fixo; a partir de 1024 px é uma janela centralizada (`ResponsiveModal`, seção 7.1).

- Abas sublinhadas **"Contato"**, **"Fiscal"** e **"Portal"** (`:370-384`; "Portal" é texto fixo no código).
- Rodapé: **"Cancelar"** e **"Criar"** (cliente novo) ou **"Salvar"** (edição). O botão mostra um indicador girando enquanto grava e fica desligado se estiver salvando, ou, na edição, enquanto as configurações do portal carregam ou dão erro (`:336-350`).
- Se a validação falhar, o formulário volta sozinho para a aba "Contato" (`:334`).

#### 3.4.1 Aba Contato (`CustomerFormDialog.tsx:386-596`)

| Bloco | Rótulo na tela | Tipo e máscara | Obrigatório | Validação e padrão |
|---|---|---|---|---|
| (topo) | Botão **"Foto"** sob um círculo | Imagem (`accept="image/*"`) | Não | HEIC de iPhone é convertido em JPEG e a imagem é reduzida para no máximo 1920 px, JPEG a 82% (JPEG de até 500 KB passa direto) (`utils/imageConvert.ts:34-39,115-144,178-187`). **Não há botão para remover** a foto escolhida. A foto só sobe ao salvar. Círculo vazio mostra o ícone de pessoas (`:390-416`). |
| Identificação | **Nome \*** | Texto, placeholder "Nome do cliente" | **Sim** | Mínimo de 2 caracteres: "Nome deve ter no mínimo 2 caracteres" (`:47-81`, `i18n customers.ts:133`). |
| Identificação | **Tipo** | Lista: **"Pessoa Jurídica"** (padrão) ou **"Pessoa Física"** | Não | Só grava PF ou PJ. **Não muda nenhum outro campo** da janela (`:425-437`). |
| Identificação | **Atende como** | Duas caixas: **"Serviço"** e **"Loja"** | Não | **Só com o módulo PDV.** Cliente novo: "Serviço" marcada. Sem o módulo, essas duas chaves nem entram no que é salvo (`:438-477`, `:293-301`). |
| Contato | **Telefone** | Texto, placeholder "(00) 0000-0000" | Não | Máscara automática `phoneMask`: 10 dígitos viram (00) 0000-0000 e 11 viram (00) 00000-0000. |
| Contato | **Celular** | Texto, placeholder "(00) 00000-0000" | Não | Máscara `mobileMask` (sempre 11 dígitos). Enquanto o número tem menos de 10 dígitos, **cada tecla digitada desliga** o interruptor do WhatsApp (`:492-510`; o `setValue` está na linha 503). |
| Contato | **Receber mensagens pelo WhatsApp** | Interruptor | Não | Com celular de 10 dígitos ou mais: "Permite avisos de ordens de serviço, cobranças e vencimentos. Pedidos de cancelamento do cliente sempre prevalecem." Sem celular válido o interruptor fica desabilitado com o texto "Informe um celular válido para liberar esta opção." Valor inicial ligado (`EMPTY_FORM`, `:85-92`). **Armadilha:** como cada tecla do Celular com menos de 10 dígitos desliga o interruptor, quem digita o número tecla a tecla o encontra **liberado, porém desligado**, ao chegar ao 10º dígito e precisa ligá-lo; colar o número inteiro de uma vez o deixa ligado. Ao salvar, vira desligado se o celular tem menos de 10 dígitos (`:285-286`). |
| Contato | **Email** | E-mail, placeholder "email@exemplo.com" | Não | "Email inválido" se estiver preenchido fora do formato. É o **mesmo campo** do "E-mail fiscal". |
| Outros dados | **Data de Nascimento** | Seletor de data, com botão de limpar | Não | — |
| Outros dados | **Origem** | Lista com busca ("Buscar origem..."), placeholder "Selecione...", opção **"Nenhuma"**, botão **"+"** (rótulo de acessibilidade "Criar origem") | Não | Grava o **nome** da origem como texto em `customers.origin`. O "+" abre a janela "Nova origem" (seção 3.9). |
| Outros dados | **Observações** | Texto longo, placeholder "Observações sobre o cliente" | Não | — |

#### 3.4.2 Aba Fiscal (`CustomerFormDialog.tsx:598-768`)

Texto de abertura: "Dados do tomador usados na emissão de NFS-e. Todos opcionais, preencha quando for emitir nota."

| Rótulo | Tipo e máscara | Obrigatório | Comportamento |
|---|---|---|---|
| **Razão Social** | Texto, placeholder "Razão social da empresa" | Não | Aparece para PF e PJ. |
| **Nome Fantasia** | Texto, placeholder "Nome fantasia da empresa" | Não | — |
| **CPF/CNPJ** | Texto com a máscara `cpfCnpjMask`, até 18 caracteres, placeholder "000.000.000-00". Lupa dentro do campo (aria "Consultar CNPJ na Receita"). | Não | **Não valida dígito verificador.** Ao completar 14 dígitos consulta o CNPJ sozinho (seção 3.5.1). Com 11 dígitos (CPF) nada acontece. |
| **Inscrição Municipal** | Texto, placeholder "Somente números" | Não | O texto do placeholder não é imposto por regra. |
| **Inscrição Estadual** | Texto, placeholder "Ex: 123.456.789.112" | Não | — |
| **E-mail fiscal** | E-mail, placeholder "email@exemplo.com" | Não | Mesmo campo "Email" da aba Contato. |
| (subtítulo) **Endereço fiscal** | | | **Este é o endereço do cliente** (usado no mapa da ficha, em OS e orçamentos). |
| **CEP** | Máscara 00000-000, placeholder "00000-000", lupa ao lado | Não | Busca sozinha ao completar 8 dígitos (seção 3.5.2). |
| **Logradouro** | Texto com sugestões, placeholder "Rua, Avenida..." | Não | Autocompletar de endereço (seção 3.5.3). |
| **Número** | Texto, placeholder "Nº" | Não | Gravado também em `street_number` (usado na NFS-e). |
| **Complemento** | Texto, placeholder "Apto, sala, bloco..." | Não | — |
| **Bairro** | Texto, placeholder "Bairro" | Não | — |
| **UF / Cidade** | Dois seletores (UF e Cidade) | Não | Seção 3.5.4. O código IBGE do município é preenchido sem aparecer (`:765-766`). |

#### 3.4.3 Aba Portal (`components/customers/CustomerPortalSettingsTab.tsx`)

Sempre visível, com ou sem o módulo `customer_portal`. Três cartões:

1. **"Portal do cliente"** — "Controle o acesso deste cliente e compartilhe somente o que ele precisa acompanhar."
   - Interruptor **"Portal ativo"** (padrão ligado). Legenda: "Desligado, o link deixa de entregar qualquer dado e não aceita novos chamados."
   - **"Link do portal"**: campo somente leitura com os botões de ícone **"Copiar link"** e **"Abrir portal"**. Em cliente novo, no lugar do link aparece "O link exclusivo será criado automaticamente quando você salvar o novo cliente."
2. **"Proteção por senha"** — "Sem senha, qualquer pessoa com o link consegue abrir o portal. Com senha, os dados só saem do servidor após o login."
   - Interruptor **"Exigir senha para entrar"** (desligado por padrão; fica bloqueado se o portal estiver inativo).
   - Ligado, aparecem **"Senha"** (placeholder "Mínimo de 8 caracteres") e **"Confirmar senha"** (placeholder "Digite novamente"; só habilita depois de digitar a senha). Na edição de um portal que já tem senha o primeiro vira **"Nova senha"** (placeholder "Em branco mantém a atual") e aparece "A senha atual nunca é exibida. Deixe os campos em branco para mantê-la."
   - Regras conferidas ao salvar: "A senha do portal precisa ter ao menos 8 caracteres e no máximo 72 bytes." e "A confirmação da senha do portal não confere." A janela volta para a aba Portal e mostra o toast "Erro" com a mensagem (`CustomerFormDialog.tsx:248-259`).
3. **"O que o cliente pode ver"** — "As restrições são aplicadas no servidor; conteúdo desligado não é enviado ao navegador do cliente." Sete linhas, cada uma com um interruptor (`CustomerPortalSettingsTab.tsx:27-67`):

   | Linha | Descrição na tela | Padrão |
   |---|---|---|
   | Ordens de serviço | Status, histórico, acompanhamento e relatórios das OS. | ligado |
   | Equipamentos | Cadastro, histórico e anexos liberados de cada equipamento. | ligado |
   | Contratos | Contratos ativos e acesso ao portal de manutenção/PMOC. | ligado |
   | Cobranças | Valores, vencimentos, status e link para pagamento. | ligado |
   | Notas fiscais | NFS-e emitidas no Dominex e notas externas liberadas para o cliente. | desligado |
   | Documentos | Contratos, anexos e documentos avulsos publicados para o cliente. | desligado |
   | Abrir chamados | Permite solicitar uma nova manutenção pelo portal. | ligado |

   **Com "Exigir senha" ligado** cada interruptor vira um seletor de 3 estados, **"Oculto"**, **"Sem senha"** e **"Com senha"**, e aparece a dica "Com a senha ligada, escolha o que aparece sem pedir login. Assim o mesmo link serve para a portaria e para o síndico." (`:74-85`, `hooks/useCustomerPortalSettings.ts:21-30`).
- Com "Portal ativo" desligado, os cartões 2 e 3 ficam esmaecidos e os controles bloqueados.
- Carregando: círculo girando. Erro: "Não foi possível carregar as configurações do portal." com o botão "Tentar novamente".

Celular: com a senha ligada, os seletores de 3 estados se empilham sob o título de cada seção, porque não cabem ao lado dele em 390 px (`CustomerPortalSettingsTab.tsx:305-325`).

### 3.5 Ajudantes de preenchimento

#### 3.5.1 Consulta de CNPJ (`components/customers/CnpjDocumentInput.tsx`)

- Dispara sozinha quando o campo chega a **14 dígitos** (`:152-154`) e pela lupa (só habilitada com 14 dígitos). Digitar o mesmo CNPJ de novo não repete a consulta; a lupa sempre repete (`:67-74,157-162`).
- A consulta é um `fetch` direto do navegador para `https://brasilapi.com.br/api/cnpj/v1/<14 dígitos>` (`:78`). **Precisa de internet.**
- Sucesso: toast **"Dados da empresa preenchidos!"**. Preenche (só o que veio com valor): Razão Social, Nome Fantasia, E-mail fiscal, Telefone (aba Contato, com máscara), CEP, Logradouro (tipo da via + nome, por exemplo "AVENIDA PAULISTA"), Número, Complemento, Bairro, Cidade e UF. O campo **Nome** da aba Contato recebe o Nome Fantasia (ou a Razão Social) **somente se estiver vazio** (`CustomerFormDialog.tsx:626-645`).
- CNPJ que a BrasilAPI não conhece (inclusive dígito verificador errado): toast vermelho **"CNPJ não encontrado na Receita"**. Falha de rede ou outro erro: **"Não foi possível consultar o CNPJ agora"**.
- O código IBGE do município **não** vem por aqui; só pelo CEP ou ao escolher a cidade.

#### 3.5.2 Consulta de CEP (`components/CepLookup.tsx`)

- Campo com máscara 00000-000 e uma lupa ao lado. Ao completar 8 dígitos (ou clicando na lupa) chama a função de servidor `cep-lookup` (`supabase.functions.invoke`, `:34`), que consulta o ViaCEP com limite de 5 s (`supabase/functions/cep-lookup/index.ts:41-50`).
- Sucesso: toast **"Endereço encontrado!"**. Preenche Logradouro, Bairro, Cidade, UF e o código IBGE. **Não preenche Número nem Complemento.**
- Falha: toast vermelho **"Erro ao buscar CEP"**. O toast "CEP não encontrado" só sai se a função responder 200 com um campo `error`; como a função responde 404 nesse caso, o `invoke` trata como erro e o que o usuário vê provavelmente é "Erro ao buscar CEP" (deduzido do código, a confirmar na prática).

#### 3.5.3 Logradouro com sugestões (`components/AddressAutocomplete.tsx`)

- A partir de **4 caracteres**, espera 500 ms e consulta o Nominatim (OpenStreetMap) limitado ao Brasil, com até 5 sugestões (`:85,119`; URL em `:89`).
- Escolher uma sugestão preenche Logradouro, Número, Bairro, Cidade, UF e CEP, e guarda a latitude e a longitude. Digitar à mão apaga essas coordenadas guardadas.
- Ao salvar, se não houver coordenadas, o app tenta descobrir pelo endereço (Nominatim, `utils/geolocation.ts:128`) e **nunca trava o cadastro** se falhar. As coordenadas alimentam o mapa da ficha.

#### 3.5.4 UF / Cidade (`components/StateCitySelector.tsx`)

- Seletor de **UF** ("Selecione UF") e seletor de **Cidade** ("Selecione a cidade", busca "Buscar cidade...", vazio "Nenhuma cidade encontrada"). As cidades vêm da API do IBGE (`https://servicodados.ibge.gov.br/api/v1/localidades/estados/<UF>/municipios?orderBy=nome`, `:83`). Trocar a UF limpa a cidade e o código IBGE.

### 3.6 Rascunho automático

Cadastro **novo** é guardado a cada alteração no navegador (`sessionStorage`, chave `form-draft:customer-form`, hook `useFormDraft`). Ao abrir de novo, aparece "Rascunho encontrado" / "Existe um preenchimento interrompido deste formulário. Deseja retomar de onde parou ou começar do zero?" com os botões **"Começar do zero"** e **"Retomar rascunho"**. Edição não guarda rascunho. Salvar ou descartar limpa o rascunho.

### 3.7 O que acontece ao salvar (`CustomerFormDialog.tsx:245-330`)

1. Valida Nome e Email (volta para a aba Contato se falhar).
2. Se o portal exige senha: confere tamanho e confirmação (volta para a aba Portal se falhar).
3. Foto escolhida: sobe para o armazenamento `customer-photos` com o nome `<hora em milissegundos>.<extensão>` e guarda o endereço público.
4. Coordenadas: usa as da sugestão de endereço; sem elas tenta geocodificar (sem travar).
5. Monta os dados: WhatsApp desligado se o celular tem menos de 10 dígitos; Data de Nascimento vazia some; "Número" também vai em `street_number`; sem PDV, tira "Atende como". **Documento e CEP são gravados com máscara** (por exemplo "12.345.678/0001-90").
6. Cria ou atualiza o cliente. Toasts: **"Cliente criado com sucesso!"** ou **"Cliente atualizado com sucesso!"**. Em falha: **"Erro ao criar cliente"** ou **"Erro ao atualizar cliente"** com o motivo (do hook) e, em seguida, um segundo toast **"Erro"** com a mesma mensagem (da janela, `CustomerFormDialog.tsx:325-326`). Como só cabe um aviso por vez, fica visível o segundo, e **a janela continua aberta**.
7. Grava as configurações do portal (sempre, mesmo sem abrir a aba Portal) e fecha a janela, limpando o rascunho. Se esta etapa falhar com o cliente novo já criado, o app guarda o `id` dele (`:310`): o erro aparece, a janela continua aberta e a nova tentativa **só regrava o portal** (não cria outro cliente e não salva o que foi alterado nos outros campos depois da falha, `:261-311`).
8. Ao editar, a janela abre com Documento e CEP já com máscara; salvar um cliente que veio do formulário público (que guarda só dígitos) converte para o formato com máscara.

### 3.8 Excluir cliente

- Caminhos: botão **"Excluir"** no cabeçalho da ficha (computador); no celular, a ação "Excluir" da linha ou o menu "Ações" da ficha.
- Diálogo **"Excluir cliente"**: `Tem certeza que deseja excluir o cliente "{nome}"? Esta ação não pode ser desfeita.` Botões "Cancelar" e "Excluir".
- Com o módulo PDV e saldo de fiado, aparece antes um aviso **"Fiado em aberto: {valor}"** / "Ao excluir, este saldo deixa de aparecer no app e a cobrança fica sem registro. Se já recebeu, registre o pagamento antes de excluir."
- É **exclusão lógica**: o cliente recebe `is_deleted = true` e `deleted_at`; a lista ignora quem tem `is_deleted = true` (`hooks/useCustomers.ts:56,109-125`). O app não confere se há OS, contratos ou equipamentos antes de excluir. Toasts: **"Cliente excluído com sucesso!"** / **"Erro ao excluir cliente"**.
- Os equipamentos de um cliente excluído continuam aparecendo na lista de Equipamentos (a consulta não filtra cliente apagado).

### 3.9 Catálogo de origens

**Para que serve:** classificar de onde veio o cliente (Indicação, Site, Google...). Aparece no campo "Origem" do cadastro, na linha "Origem" da ficha e no CRM.

#### Gerenciador "Origens de Clientes" (`components/customers/CustomerOriginManagerDialog.tsx`)

- Abre por **"Configurar origens"** (computador) ou **"Origens"** (celular). Existe um **terceiro caminho**: Configurações → aba **"Usabilidade"** → cartão **"Origens"** ("Lista de origens usada no cadastro de clientes e nas oportunidades do CRM"), com o botão **"Gerenciar origens"** que abre a mesma janela. Com o catálogo vazio, o cartão mostra "Nenhuma origem cadastrada. Crie um conjunto inicial e edite à vontade depois." e o botão **"Criar origens padrão"** ("Criando…"); com origens, lista cada uma com ícone, cor e, se estiver desligada, a etiqueta "Inativa" (`pages/Settings.tsx:1820-1870`, texto em `lib/i18n/messages/app/settings.ts:286-294`; rota `/configuracoes?tab=usabilidade`).
- Catálogo novo está vazio: **"Nenhuma origem cadastrada"** / "Crie um conjunto inicial de origens (Indicação, Site, WhatsApp, Google…) e edite ou exclua à vontade depois." com o botão **"Criar origens padrão"** ("Criando..." enquanto grava). Cria as 10 origens abaixo e o toast **"Origens padrão criadas!"**. O botão só semeia se o catálogo estiver vazio (`hooks/useCustomerOrigins.ts:84-109`).

  | Nome | Ícone | Cor |
  |---|---|---|
  | Indicação | Users | #22C55E |
  | Site | Globe | #3B82F6 |
  | Telefone | Phone | #0EA5E9 |
  | WhatsApp | MessageCircle | #10B981 |
  | Google | Search | #EAB308 |
  | Instagram | Instagram | #EC4899 |
  | Facebook | Facebook | #6366F1 |
  | Parceiro | Handshake | #A855F7 |
  | Feira/Evento | CalendarDays | #F97316 |
  | Outro | Tag | #6B7280 |

- Linha de cada origem: ícone colorido e nome; edição na própria linha; menu com **"Editar"** e **"Excluir"**.
- Para criar: campo **"Nova origem..."** e botão **"Adicionar"**. Toast **"Origem criada!"**.
- Outros toasts: **"Origem atualizada!"**, **"Origem removida!"**. Erro: toast vermelho "Erro" com o motivo.
- **Excluir não pede confirmação** (`CustomerOriginManagerDialog.tsx:114`). Os clientes antigos guardam só o **nome** da origem; se a origem for renomeada ou excluída, a ficha mostra o texto sem ícone.
- Há 20 ícones disponíveis (`components/customers/originIcons.tsx`).
- Só as origens com `is_active = true` aparecem nas listas de escolha.

#### Criação rápida pelo "+" (`components/customers/OriginSelectField.tsx`)

No campo "Origem" do cadastro, o botão **"+"** abre a janela **"Nova origem"** com **Nome** (placeholder "Ex: Indicação, Site, WhatsApp..."), **Ícone**, **Cor** e os botões **"Criar origem"** e **"Cancelar"**. Sem ícone ou cor escolhidos entram o ícone Globe e o cinza #6B7280 (`:172-173`). A nova origem já fica selecionada.

### 3.10 Formulários de captação (link público para o cliente se cadastrar sozinho)

**Resumo do fluxo:** a empresa cria um formulário → copia o link → o cliente abre `/cadastro/<nome>-<código>` sem login, preenche e envia → o servidor valida e cria o cliente direto na lista, com Origem "public_form".

#### 3.10.1 Gerenciador "Formulários de captação" (`components/customers/LeadCaptureManagerDialog.tsx`)

- Abre por **"Formulários de captação"** (computador) ou **"Formulários"** (celular). Subtítulo: "Links públicos para o cliente se cadastrar sozinho."
- Cada formulário aparece com: título, situação **"Ativo"**, **"Inativo"** ou **"Expirado"**, contagem **"{n} cadastro(s)"**, um interruptor (ativa e desativa) e botão **"Copiar link"**; menu com **"Editar"** e **"Excluir"**.
  - Interruptor: toasts **"Formulário ativado"** / **"Formulário desativado"**.
  - **"Copiar link"**: copia `https://<site>/cadastro/<título em minúsculas e hifens>-<código de 12 letras>` (`utils/prettyLinks.ts:103-115`, fallback "cadastro") e mostra **"Link gerado e copiado!"**. Se o navegador não deixar copiar, mostra "Link gerado" com o endereço.
  - **"Excluir"**: diálogo **"Excluir formulário"** / `Tem certeza que deseja excluir "{título}"? O link deixará de funcionar.` Toast **"Formulário excluído com sucesso!"**.
- Vazio: **"Nenhum formulário ainda"** / "Crie um link público para receber cadastros de novos clientes."
- Rodapé: botão **"Novo formulário"**.

#### 3.10.2 Editor (`components/customers/LeadCaptureFormDialog.tsx`)

Título **"Novo formulário de captação"** ou **"Editar formulário"**, com a legenda "Compartilhe um link público para o cliente se cadastrar sozinho." (texto fixo no código, `LeadCaptureFormDialog.tsx:170-171`). Três abas: **Geral**, **Campos**, **LGPD**.

- **Geral**
  - **Título** (placeholder "Ex.: Cadastro de novos clientes") — obrigatório. Sem ele: toast "Informe um título para o formulário".
  - **Descrição (opcional)** (placeholder "Texto que aparece no topo do formulário público").
  - Interruptor **"Formulário ativo"** — "Desative para pausar os cadastros sem apagar o link." (padrão ligado).
  - **"Expira em (opcional)"** — data e hora. "Depois dessa data o link deixa de aceitar cadastros."
- **Campos** — "Escolha quais campos aparecem no formulário e quais são obrigatórios." São 17 linhas, cada uma com os interruptores **"Exibir"** e **"Obrigatório"** (Obrigatório só liga se Exibir estiver ligado): Nome, Tipo de cliente (PF/PJ), CPF / CNPJ, E-mail, Telefone, Celular, Razão social, Nome fantasia, CEP, Endereço, Número, Bairro, Complemento, Cidade, Estado (UF), Observações, Foto. Formulário novo vem só com **Nome** exibido e obrigatório. Sem nenhum campo exibido: toast "Habilite ao menos um campo do formulário".
- **LGPD**
  - Interruptor **"Exigir consentimento"** — "O cliente precisa marcar a caixa de aceite antes de enviar (recomendado)." (padrão ligado).
  - **"Texto do consentimento"** — padrão: "Autorizo o contato e o tratamento dos meus dados para fins de atendimento, conforme a Lei Geral de Proteção de Dados (LGPD)."
- Rodapé: **"Salvar"**. Ao **criar**: toast **"Formulário criado com sucesso!"**; ao **editar**: **"Formulário atualizado com sucesso!"**. O botão **"Gerar e copiar link"** só existe quando o formulário já foi salvo (o endereço depende do código que o banco gera).
- Não existe na tela o limite de envios (`max_submissions`); o banco o aceita, mas o editor não o expõe.

#### 3.10.3 Página pública `/cadastro/<nome>-<código>` (`pages/PublicLeadCapture.tsx`)

Sem login. Mostra no topo o logotipo da empresa (e a cor da marca, se a empresa usa marca própria), o **título** e a **descrição** do formulário e só os campos ligados, nesta ordem fixa: Nome, Tipo de cliente, CPF / CNPJ, Razão social, Nome fantasia, E-mail, Telefone, Celular, CEP, Endereço, Número, Bairro, Complemento, Cidade, Estado (UF), Foto, Observações (`:154-158`).

- Cada rótulo mostra "\*" (obrigatório) ou "(opcional)".
- **Tipo de cliente**: interruptor **"Pessoa física"** / **"Pessoa jurídica"** (padrão Pessoa física).
- Máscaras: CPF / CNPJ, Telefone e Celular (mesma máscara de 10 ou 11 dígitos), CEP; Estado (UF) aceita só 2 letras maiúsculas (`:302-308`). O CEP usa o mesmo componente de busca da seção 3.5.2 e preenche Endereço, Bairro, Cidade e Estado.
- **Foto**: botão **"Tirar foto ou escolher da galeria"** (no celular abre a câmera). A foto sobe na hora, antes do envio; enquanto sobe mostra "Enviando foto..." e depois dois botões de ícone **"Trocar foto"** e **"Remover foto"**. Se a foto for obrigatória e o envio falhar, não deixa enviar o cadastro; se for opcional, o cadastro segue sem ela. Mensagem de espera: "Aguarde a foto terminar de enviar."
- Caixa de consentimento (se exigida) com o texto configurado. O nome da empresa aparece pequeno abaixo do cartão.
- Botão **"Enviar cadastro"** ("Enviando..." durante o envio). Faltando obrigatório: "Preencha os campos obrigatórios." Sem aceitar os termos: "É preciso aceitar os termos para enviar."
- Sucesso: **"Cadastro enviado com sucesso"** / "Recebemos seus dados. Em breve entraremos em contato."
- Link errado: **"Formulário não encontrado"** / "Confira o link e tente novamente." Formulário inativo ou expirado: **"Formulário indisponível"** / "Este formulário não está mais disponível."
- Erro genérico: "Não foi possível enviar. Tente novamente."
- A página **não valida CPF/CNPJ** no navegador (só aplica máscara). A validação é no servidor (seção 3.10.4).

#### 3.10.4 O que o servidor faz com o envio (para entender os erros e para o backend falso)

Cadeia: página → função `lead-capture-upload-photo` (se há foto) → função `lead-capture-submit` → procedimento `submit_lead_capture_form` (`supabase/functions/lead-capture-submit/index.ts`; `supabase/migrations/20261015233000_lead_capture_insert_dinamico_respeita_default.sql:100-336`).

- Limite do corpo do envio: 8 KB. Campo escondido "website" (isca para robôs) preenchido: o servidor responde sucesso e **descarta** o cadastro sem avisar.
- Limite de tentativas: 5 envios por formulário e por IP em 10 minutos e 30 por IP em 24 horas → "Muitas tentativas. Tente novamente mais tarde."
- Mensagens de erro (em português, mostradas no quadro vermelho da página): "Formulário indisponível", "Consentimento obrigatório", "Campo obrigatório ausente: {campo}", "E-mail inválido", **"CNPJ inválido"** / **"CPF inválido"**, "Telefone inválido" (precisa de 10 ou 11 dígitos), "CEP inválido" (8 dígitos), "Foto inválida".
- **Documento**: se o tipo for "Pessoa jurídica", valida o CNPJ pelo dígito verificador; **em qualquer outro caso valida como CPF** (incluindo quando o campo "Tipo de cliente" nem está ligado no formulário: aí o tipo é sempre PF e um CNPJ digitado dá "CPF inválido").
- Guarda **só dígitos** em documento, telefone, celular e CEP (o cadastro feito dentro do Dominex guarda com máscara).
- O cliente nasce com: `origin = 'public_form'`, `lead_consent_at` (se aceitou), `customer_type` = o escolhido ou 'pf', e Nome "Cliente (formulário)" se o campo Nome não estiver ligado. `whatsapp_notifications_enabled` fica no padrão do banco, que hoje é **ligado** (`true`; a migração `20261016233000_customers_whatsapp_opt_out_por_padrao.sql:98` trocou o padrão que era desligado) e o gatilho carimba `whatsapp_opt_in_at` na criação (seção 13).
- O contador "cadastro(s)" do formulário sobe de 1 e o envio é registrado em `lead_capture_submissions_log`.
- Foto: aceita JPEG, PNG ou WebP reais (confere os primeiros bytes), até 5 MB, 20 envios por minuto por IP, e guarda em `customer-photos/lead-capture/<código>/<uuid>.<ext>` (`supabase/functions/lead-capture-upload-photo/index.ts:45-62,110-124`).
- **Não existe fila de aprovação**: o cliente aparece direto em Clientes. Quando alguém volta para a aba do Dominex a lista é recarregada sozinha (comportamento padrão da biblioteca de dados, `App.tsx:246`); se não aparecer, é só atualizar a página.
- Na ficha, a linha "Origem" mostra o texto cru "public_form", sem ícone, porque essa origem não existe no catálogo (`CustomerDetail.tsx:823-839`).

---

## 4. Ficha do cliente (`/clientes/<nome>-<código>`)

Arquivo `pages/CustomerDetail.tsx` (2167 linhas). No computador aparece à direita da lista. No celular ocupa a tela toda, com a seta de voltar do aplicativo.

### 4.1 Cabeçalho (`CustomerDetail.tsx:670-802`)

- Seta de voltar (só no computador) para `/clientes`.
- Foto redonda do cliente (clicar abre ampliada; rótulo "Ver foto do cliente") ou um ícone de pessoa.
- **Nome com uma setinha**: clicar abre uma caixa com busca **"Buscar cliente..."** para **trocar de cliente sem voltar à lista**. Sem resultado: "Nenhum cliente encontrado." Cada item mostra o nome e, embaixo, documento ou telefone (`:695-733`, `:303-311`).
- Etiqueta "PJ" ou "PF" e, ao lado, a razão social.
- No computador: botões **"Editar"** (abre "Editar Cliente", seção 3.4) e **"Excluir"** (seção 3.8). Eles não conferem permissão.
- Menu **"Ações"** (`:763-800`):
  - **"Copiar link do portal"**: copia `https://<site>/portal/<token>` e mostra "Link do portal copiado!". Só com o módulo `customer_portal` e portal ativo.
  - **"Abrir portal"**: abre o portal em outra aba. Mesma condição.
  - **"Criar oportunidade no CRM"**: módulo CRM; abre o formulário completo de oportunidade já com o cliente.
  - **"Editar"** e **"Excluir"**: só aparecem aqui no celular.
- Cliente que não existe mais: "Cliente não encontrado." com o botão "Voltar".

### 4.2 Abas (`CustomerDetail.tsx:616-636`)

Faixa rolável com sombra nas pontas (`MobilePillTabs`, estilo sublinhado), na ordem:
**Geral · Equipamentos · Histórico · Tarefas · Estoque · [Chamados] · Contratos · Documentos · [Financeiro] · [Cobranças]**.
Os colchetes dependem de módulo ou permissão (seção 2). Vindo da ficha de um equipamento (botão voltar), a ficha abre direto na aba **Equipamentos** (`:161-169`).

Os dados da ficha vêm de consultas **globais** da empresa (todas as OS, todos os lançamentos, todos os contratos), filtradas no navegador por `customer_id` (`CustomerDetail.tsx:185-203,312-344`). Só os equipamentos, os contatos, os gastos pagos pelo cliente e as cobranças são buscados por cliente.

### 4.3 Aba Geral (`CustomerDetail.tsx:816-1073`)

Quatro cartões:

1. **"Informações"** — cada linha só aparece se o dado existir:

   | Linha | Como aparece |
   |---|---|
   | **Origem** | Quadradinho colorido com o ícone da origem + nome. Se a origem não está entre as ativas do catálogo (comparação exata do nome), mostra só o texto (caso de "public_form"). |
   | **CPF/CNPJ** | Como está gravado (sem aplicar máscara). |
   | **Inscrição Estadual** | — |
   | **Email** | Com ícone de envelope. |
   | **Telefone** | Com máscara, mais o botão do WhatsApp. |
   | **Celular** | Com máscara, mais o botão do WhatsApp. |
   | **Nome Fantasia** | — |
   | **Data de Nascimento** | dd/MM/aaaa. |

   A razão social fica no cabeçalho (ao lado de PJ/PF) e a Inscrição Municipal não é mostrada na ficha.
   **Botão do WhatsApp:** ícone verde (rótulo "Abrir WhatsApp do cliente", dica "WhatsApp") que abre `https://wa.me/55<só dígitos>` em outra aba. O app **sempre** coloca 55 na frente e não confere o tamanho do número (`:857-907`).

2. **"Endereço"** — só se houver endereço ou cidade. Mostra uma linha `rua, número, complemento, bairro, cidade - UF, CEP`, um mapa do Google incorporado (precisa de internet) e dois botões: **"Abrir no Google Maps"** e **"Abrir no Waze"** (`:943-986`).
3. **"Responsável no Local (falar com)"** — botão **"Adicionar"** no canto. Cada contato é uma linha com nome, cargo, telefone (link `tel:`), e-mail (link `mailto:`) e um menu com **"WhatsApp"** (só se há telefone), **"Editar contato"** e **"Excluir contato"**. Vazio: **"Nenhum contato cadastrado"** / "Cadastre quem falar no local deste cliente" com o botão **"Adicionar contato"** (`:988-1064`).
4. **"Observações"** — só se o cliente tem observação.

### 4.4 Janela de contato — "Novo Contato" / "Editar Contato" (`components/customers/ContactFormDialog.tsx`)

| Rótulo | Tipo | Obrigatório | Detalhes |
|---|---|---|---|
| **Nome \*** | Texto, placeholder "Nome do contato" | Sim | O botão de salvar fica desabilitado sem nome. |
| **Cargo** | Texto, placeholder "Ex: Gerente, Supervisor, Zelador" | Não | — |
| **Telefone** | Texto com a máscara `phoneMask`, placeholder "(00) 00000-0000" | Não | Gravado com máscara. |
| **Email corporativo** | E-mail, placeholder "contato@empresa.com" | Não | — |

Botões: **"Cancelar"** (vermelho) e **"Adicionar"** (novo) ou **"Salvar"** (edição). **Não há toast de confirmação**; a janela fecha e a lista de contatos atualiza. Excluir: diálogo **"Excluir contato"** / "Tem certeza que deseja excluir este contato?", botões "Cancelar" e "Excluir" (`CustomerDetail.tsx:2009-2040`). No computador a janela de contato é um `Dialog` simples (448 px): **clicar fora a fecha** e o que foi digitado se perde; no celular vira gaveta (`Drawer`) (`ContactFormDialog.tsx:100-125`).
Campos opcionais vazios são omitidos do envio; por isso, **apagar o telefone, o e-mail ou o cargo de um contato já salvo e clicar em "Salvar" não remove o valor antigo** (pelo código).

### 4.5 Aba Equipamentos (`CustomerDetail.tsx:1079-1238`)

- Título "Equipamentos do Cliente". No computador, botão **"Novo Equipamento"**. No celular, botão flutuante **"Novo Equipamento"**.
- Tabela no computador: **Foto · Nome** (com o identificador embaixo, em fonte de código) **· Local · Categoria · Status** ("Ativo"/"Inativo") **· Ações** (menu com "Editar" e "Excluir"). As colunas Local, Categoria e Status somem em janelas estreitas. Clicar na linha abre a ficha do equipamento (`/equipamentos/<id>`), lembrando que veio do cliente.
- No celular a tabela vira uma lista: quadradinho com a cor da categoria (ou a foto), nome e modelo, categoria (ou identificador) e a etiqueta Ativo/Inativo.
- Vazio: **"Nenhum equipamento"** / "Cadastre o primeiro equipamento deste cliente" com o botão **"Adicionar equipamento"**.
- **"Novo Equipamento"** abre o mesmo formulário da seção 6.3, **com o cliente já escolhido e travado** (a lista de clientes da janela contém só este cliente). Toasts: "Equipamento criado com sucesso!" (criar), **"Equipamento atualizado!"** (editar), **"Equipamento excluído!"** (excluir). Erros: "Erro ao atualizar" e "Erro ao excluir" com o motivo.
- Excluir: **"Excluir equipamento"** / `Tem certeza que deseja excluir "{nome}"? Esta ação não pode ser desfeita.`

### 4.6 Aba Histórico (`:1240-1298`)

- Título "Histórico de OS". Botão **"Nova OS"** (no computador; botão flutuante no celular) que abre o formulário de OS **com este cliente já escolhido**.
- Lista as OS do cliente que **não** são tarefas. Colunas: **OS** (número formatado), **Status** (etiqueta), **Data** (dia agendado, dd/MM/aaaa, ou "-"), **Ações** (ícone de olho abre a OS). Colunas ordenáveis, com paginação.
- Vazio: **"Nenhuma OS registrada"** / "Crie a primeira ordem de serviço deste cliente" com o botão "Nova OS".

### 4.7 Aba Tarefas (`:1300-1387`)

- Título "Tarefas do Cliente". Botão **"Nova Tarefa"** (formulário de tarefa com o cliente já escolhido; é o mesmo da Agenda, com recorrência).
- Tarefa é uma OS do tipo `tarefa`. Colunas: **Tarefa · Status** ("Concluída", "Em andamento" ou "Pendente") **· Data · Horário · Ações** (menu "Editar tarefa" e "Excluir tarefa"). Concluídas aparecem riscadas e esmaecidas.
- Excluir: **"Excluir tarefa?"** com "A tarefa será removida da agenda. Esta ação não pode ser desfeita." ou, se for de uma série, "Esta tarefa faz parte de uma série. Apenas esta ocorrência será excluída — as demais permanecem na agenda." Toasts: "Tarefa excluída" e "Erro ao excluir tarefa".
- Vazio: **"Nenhuma tarefa"** / "Crie a primeira tarefa deste cliente".

### 4.8 Aba Estoque (`components/customers/CustomerStockTab.tsx`)

Estoque de materiais que **ficam no cliente** (por exemplo material comprado pelo cliente). Sempre visível.

- Duas subabas: **"Materiais"** e **"Histórico de materiais"**, mais indicadores de materiais, quantidade total e abaixo do mínimo.
- Botão **"Cadastrar material"** (`fn:manage_inventory`) abre **"Cadastrar material no cliente"** (editar: "Editar material do cliente"): **Material \*** (placeholder "Ex.: Tinta acrílica branca"), **Código / SKU** ("Opcional"), **Unidade \*** ("un, kg, m, L..."), **Saldo inicial** ("0"), **Estoque mínimo** ("Opcional"), **Custo de referência** ("Opcional"), **Observações** ("Marca, lote, local dentro da obra..."). Validações: "Informe o nome do material.", "Informe a unidade do material.", "O saldo inicial não pode ser negativo."
- Menu da linha: **"Registrar entrada"**, **"Registrar saída"**, **"Editar"**, **"Excluir"**. Entrada/saída pede quantidade ("Informe uma quantidade maior que zero.") e observação ("Ex.: Material comprado pelo cliente" / "Ex.: Uso manual na obra"). Saída maior que o saldo mostra o botão "Registrar mesmo assim".
- Excluir é arquivar: com saldo diferente de zero aparece "Zere o saldo antes de excluir" (botão "Entendi"); com saldo zero, "Excluir material do estoque do cliente?" (botão "Excluir material").
- Vazio: **"Nenhum material no estoque do cliente"** / "Cadastre o primeiro material comprado ou mantido por este cliente."
- Histórico: tipos "Entrada", "Saída", "Ajuste", "Estorno" e "Consumo em OS"; origem "Ordem de serviço", a observação ou "Movimentação manual".

### 4.9 Aba Chamados (`:1389-1437`) — módulo `customer_portal`

- Título "Chamados do Portal". Lista as OS do cliente cuja origem é o portal (`origin = 'portal'`). Colunas **OS · Descrição · Status · Data · Ações** (ícone abre a OS em `/os-tecnico/<id>` numa nova aba).
- Vazio: **"Nenhum chamado"** / "Nenhum chamado aberto pelo portal do cliente" (ou "Gere o link do portal para o cliente abrir chamados" se não há link).

### 4.10 Aba Contratos (`:1439-1505`)

- Título "Contratos". Botão **"Novo Contrato"** (computador) / botão flutuante (celular), que abre o formulário de contrato com o cliente.
- Colunas **Nome · Status** ("Ativo", "Pausado" ou "Encerrado") **· Frequência · Início · Ações** (ícone abre `/contratos/<id>`).
- Vazio: **"Nenhum contrato"** / "Vincule o primeiro contrato a este cliente" com o botão "Novo contrato".

### 4.11 Aba Documentos (`components/customers/CustomerDocumentsTab.tsx`)

- Duas subabas: **"Notas fiscais"** e **"Documentos"**, com os botões **"Adicionar nota externa"** e **"Adicionar documento"**.
- Campos da janela: **Arquivo** (até 15 MB; para nota fiscal PDF ou XML; para documento PDF, XML, imagem, Word, Excel ou texto), **Título**, **Tipo** ("NF-e de produto", "NFS-e de serviço", "Outro documento fiscal" nas notas; "Contrato", "Outro documento" nos documentos), **Número da nota**, **Data de emissão**, **Valor**, **Observação** (até 500 caracteres) e o interruptor **"Disponível no portal"**.
- Toasts: "Nota fiscal adicionada", "Documento adicionado", "Arquivo liberado no portal", "Arquivo ocultado do portal", "Arquivo excluído".
- Adicionar, ocultar e excluir exigem `fn:edit_customer` (ou admin/gestor). Excluir usa a caixa de confirmação do navegador (`window.confirm`, texto `Excluir “<título>”? Esta ação não pode ser desfeita.`, `CustomerDocumentsTab.tsx:146`). Baixar usa um endereço assinado que vale 60 segundos.

### 4.12 Aba Financeiro (`:1511-1701`) — permissão `fn:view_customer_financial` e tela Financeiro

Fora do escopo do T3; para referência:
- Título "Transações do Cliente". Botões do computador: **"Despesa da empresa"**, **"Gasto pago pelo cliente"** (ambos com `fn:manage_finance`) e **"Cobrar"** (se a aba Cobranças existir). No celular: "Despesa da empresa" e "Pago pelo cliente" mais o botão flutuante "Cobrar".
- Botões segmentados **"Tudo"**, **"A vencer"**, **"Pagas"**. Colunas **Descrição · Valor · Data · Status · Ações**. Etiquetas pequenas "Cobrança" e "Pago pelo cliente". Menu: "Ver detalhes", "Editar", "Excluir" (só com `fn:delete_finance`).
- Vazios: "Nenhuma transação" (Tudo), "Nada a vencer", "Nenhuma transação paga".

### 4.13 Aba Cobranças (`:1703-1849`) — módulo `cobrancas` + conta de recebimento ativa

- Título "Cobranças do Cliente". Botão **"Cobrar"**. Dois cartões: **"Em aberto"** e **"Recebido"**. Colunas **Descrição · Valor · Vencimento · Status · Ações**. Menu: "Copiar link", "Enviar por WhatsApp", "Abrir checkout", "Editar", "Excluir" e "Estornar" (diálogo "Estornar esta cobrança?").
- Vazio: **"Nenhuma cobrança"** / "Gere a primeira cobrança para este cliente".

Celular (ficha inteira): abas roláveis; botões de criação viram botão flutuante; as tabelas viram listas de cartões; "Editar" e "Excluir" ficam dentro do menu "Ações".

### 4.14 O portal do cliente em uma linha

`/portal/<token>` mostra ao cliente as seções que a empresa liberou (Ordens de Serviço, Equipamentos, Contratos, Cobranças, Notas fiscais, Documentos e "Abrir Chamado"). Se houver senha, a página mostra "Portal protegido" / "Digite a senha fornecida pela empresa para acessar seus dados." com o botão "Entrar no portal". O tutorial T3 só precisa mostrar o link e a aba Portal do cadastro; o portal em si é assunto de outra aula.

---

## 5. Fornecedores (aba "Fornecedores" de `/clientes`)

Cadastro simples de quem vende para a empresa (distribuidor de peças, loja de gás, fabricante). **Fornecedor não é cliente**: tem tabela própria (`suppliers`), uma única janela de cadastro, uma ficha com histórico de gastos e nada mais (sem abas, sem portal, sem WhatsApp, sem busca de CNPJ).

### 5.1 Como chegar

- Menu Gestão → "Clientes e Fornecedores" → aba sublinhada **"Fornecedores"** (ícone de caminhão) ao lado de "Clientes" (`components/customers/CustomersPageChrome.tsx:80-89`, `i18n customers.suppliers.tabLabel`).
- A troca de aba é **estado local** da página (`pages/Customers.tsx:241`): o endereço continua `/clientes` e, ao recarregar, volta para "Clientes". Fornecedor **não tem rota própria nem link direto**: clicar numa linha não muda o endereço.
- Com a aba "Fornecedores" ativa, os botões "Configurar origens", "Formulários de captação" e "Novo Cliente" do cabeçalho **somem** (`CustomersPageChrome.tsx:47`). O botão de criar fica dentro da própria aba (5.2).
- A aba aparece para todo mundo que abre a tela de Clientes (`screen:customers`). Não existe permissão `fn:` de fornecedor (5.8).

### 5.2 Lista no computador (mestre-detalhe) — `components/customers/SuppliersTab.tsx:150-233`

- Mesma estrutura da lista de clientes (seção 3.2): coluna da esquerda **"Lista de Fornecedores"** e ficha à direita. Ordem Nome (A-Z)/(Z-A), páginas de 10/25/50/100/Todos (padrão 25), busca e ordem lembradas na sessão (chave `suppliers-list-detail`).
- Cada linha: ícone de caminhão, o **nome** e, embaixo, `CPF/CNPJ · contato · telefone` (só o que estiver preenchido, separados por " · "). Não há avatar nem etiqueta.
- **Busca**: caixa "Buscar fornecedores...". Procura um trecho (sem diferenciar maiúscula; acento conta) em nome, documento, contato, telefone, e-mail, endereço e observações (`:154-155`).
- Botão **"Novo Fornecedor"** fica no **topo direito do painel da ficha** (`:175-180`), não no cabeçalho da página. Aparece mesmo com a lista vazia.
- Painel direito:
  - nenhum selecionado: **"Selecione um fornecedor"** / "Escolha um fornecedor na lista para abrir a ficha e o histórico de gastos.";
  - nenhum cadastrado: **"Nenhum fornecedor cadastrado"** / `Clique em "Novo Fornecedor" para começar`;
  - busca sem resultado (dentro da coluna da lista): **"Nenhum fornecedor encontrado"**;
  - erro de carregamento: **"Erro ao carregar fornecedores"** / "Não foi possível conectar ao servidor. Tente novamente." com **"Tentar novamente"**.

### 5.3 Lista no celular e no tablet — `SuppliersTab.tsx:75-148`

- Barra com a busca **"Buscar fornecedores..."** (tolerante a acento e ordem das palavras; procura em nome, CPF/CNPJ, contato, e-mail e endereço, **não** em telefone nem observações, `:49-55`) e um botão largo **"Fornecedor"** (ícone de mais) para criar. Não há seletor Lista/Grade nem filtros.
- Linha: círculo com caminhão, nome e `documento • contato • telefone`, ou **"Sem dados adicionais"** quando não há nada. Menu da linha: **"Ver ficha"**, **"Editar"**, **"Excluir"**. Tocar na linha equivale a "Ver ficha".
- Páginas de 10 com seletor de tamanho (chave `suppliers-list`).
- Vazio: "Nenhum fornecedor cadastrado" / `Toque em "Novo Fornecedor" para começar` (o botão se chama só "Fornecedor", então a frase não bate letra por letra) e "Nenhum fornecedor encontrado" / "Tente uma busca diferente".

### 5.4 Ficha do fornecedor — `components/customers/SupplierDetailDialog.tsx`

No computador a ficha é o painel da direita (`SupplierDetailContent`, `:39-177`). No celular abre uma janela **"Ficha do Fornecedor"** com o botão **"Fechar"** no rodapé (`:179-200`).

- Só no computador, cabeçalho: legenda pequena **"Ficha do Fornecedor"**, nome grande e os botões **"Editar"** (amarelo) e **"Excluir"** (vermelho) (`SuppliersTab.tsx:201-223`).
- Bloco **"Dados do fornecedor"** (`:64-104`): cada dado aparece com um **ícone e sem rótulo escrito** (documento, contato, telefone, e-mail e, ocupando a linha toda, endereço com o ícone de alfinete). Só entra o que foi preenchido. Observações aparecem em parágrafo cinza e, se estiverem vazias, em itálico: **"Sem observações"**. As chaves de texto "Documento", "Contato", "Telefone", "E-mail" e "Observações" existem no i18n mas **não são exibidas**.
- Bloco **"Histórico de Gastos"** (`:106-174`):
  - à direita do título, em vermelho, **"Total gasto: R$ …"** (soma só os lançamentos de saída; só aparece se houver algum);
  - tabela **Descrição · Valor · Data · Status**. Valor com "-" em vermelho (saída) ou "+" em verde (entrada); Data dd/MM/aaaa (some em tela estreita); Status **"Pago"** (verde) ou **"Pendente"** (amarelo). Mais recente primeiro; páginas de 10;
  - vazio: **"Nenhum gasto registrado"** / "Nenhum lançamento financeiro vinculado a este fornecedor ainda.".
- Fonte dos dados: o financeiro inteiro da empresa (`useFinancial()`), filtrado no navegador por `supplier_id` (`:43-50`). O financeiro só é carregado quando a ficha abre. Só aparecem aqui gastos em que o fornecedor foi escolhido (despesa lançada no Financeiro, compra, nota lançada).
- A ficha é somente leitura: **não dá para lançar gasto por aqui**.

### 5.5 Janela "Novo Fornecedor" / "Editar Fornecedor" — `components/inventory/SupplierFormDialog.tsx`

Janela estreita (520 px), um formulário simples, **sem abas, sem rascunho automático, sem máscara e sem consulta externa**.

| Rótulo na tela | Tipo e placeholder | Obrigatório | Regras |
|---|---|---|---|
| **Nome \*** | Texto, "Nome do fornecedor" | **Sim** | O botão "Salvar" fica desligado enquanto o nome estiver vazio (`:81`) e o envio é ignorado sem nome (`:58`). |
| **CPF/CNPJ** | Texto livre, "00.000.000/0000-00" | Não | **Nenhuma máscara, nenhuma consulta à Receita, nenhuma validação** de dígito. Grava exatamente o que for digitado. |
| **Contato** | Texto, "Nome do contato" | Não | Nome da pessoa que atende. |
| **Telefone** | Texto, "(00) 00000-0000" | Não | **Sem máscara**: o placeholder sugere o formato, mas nada formata. |
| **E-mail** | `type="email"`, "email@fornecedor.com" | Não | O navegador só valida o formato quando o envio vem do Enter dentro do formulário; o botão "Salvar" chama o envio direto (`:81`), sem essa checagem (pelo código). |
| **Endereço** | Texto de uma linha, "Rua, número, bairro, cidade/UF e CEP" | Não | **Campo livre**: não há busca de CEP nem preenchimento automático. A coluna `address` veio depois (`supabase/migrations/20260927200000_supplier_address.sql`). |
| **Observações** | Área de texto (2 linhas), "Anotações sobre o fornecedor..." | Não | — |

- Rodapé: **"Cancelar"** e **"Salvar"** (vira "Salvando..." enquanto grava).
- Sucesso: a janela fecha e aparece o toast **"Fornecedor cadastrado!"** (novo) ou **"Fornecedor atualizado!"** (edição).
- Erro: toast vermelho **"Erro ao cadastrar fornecedor"** ou **"Erro ao atualizar fornecedor"** com o motivo; **a janela continua aberta** (`:56-66`).
- Campos vazios vão como texto vazio (`''`), não como nulo.
- **Não há trava de duplicidade**: dois fornecedores com o mesmo CPF/CNPJ são aceitos (a tabela não tem índice único).
- Fornecedor novo grava `company_id` (do perfil) e `created_by` (`hooks/useSuppliers.ts:37-52`).

### 5.6 Excluir fornecedor

- Computador: botão **"Excluir"** da ficha. Celular: **"Excluir"** no menu da linha.
- Diálogo **"Excluir fornecedor"**: `Tem certeza que deseja excluir o fornecedor "{nome}"?` e dois avisos em linhas separadas: "As cotações desse fornecedor em compras de material (inclusive já aceitas) também serão apagadas, com os preços cotados." e "Os lançamentos financeiros já feitos continuam no histórico do caixa, só perdem o vínculo com o fornecedor." Botões **"Cancelar"** e **"Excluir"** (vermelho) (`SuppliersTab.tsx:246-266`).
- Toast **"Fornecedor removido!"** ou **"Erro ao remover fornecedor"**. A exclusão é **definitiva** (`DELETE` na tabela, sem lixeira).
- No banco (chaves estrangeiras): cotações e ordens de compra do fornecedor são apagadas em cascata; lançamentos financeiros, movimentações de estoque e notas recebidas **ficam e perdem o vínculo** (`SET NULL`). Fontes: `20260619160000_estoque_fase_a_compras_rpc.sql`, `20260619180000_compras_redesign.sql`, `20260930110000_compras_ordem_de_compra.sql`, `20260916170000_financial_transactions_supplier_id.sql`.

### 5.7 Outros lugares que usam o mesmo cadastro

O mesmo formulário (`SupplierFormDialog`) e o mesmo hook (`useSuppliers`) aparecem em:

- Estoque → Compras: janela **"Fornecedores"** (busca "Buscar fornecedor...", botão **"Novo"**) (`components/inventory/SuppliersDialog.tsx`, aberta em `MaterialPurchasesTab.tsx:363`).
- Cotação de compra: criar fornecedor na hora (`components/inventory/CotacaoDialog.tsx:346`).
- Financeiro: campo de fornecedor das despesas, com criação rápida (`components/financial/SupplierSelectField.tsx:86`).

### 5.8 Permissões e celular

- Não existe `fn:` de fornecedor e a tela não consulta nenhuma permissão: **quem enxerga a aba cria, edita e exclui**. O banco só confere a empresa (`suppliers_select/insert/update/delete_own_company`, `supabase/migrations/20260619150000_estoque_fase_a_movements_suppliers.sql:98-119`).
- Celular: lista simples com menu "Ver ficha / Editar / Excluir", ficha em janela e botão "Fornecedor" na barra.

---

## 6. Equipamentos (`/equipamentos`)

Equipamento é o aparelho instalado no cliente (um split, um VRF). Fica sempre ligado a **um cliente** e é a base de OS, contratos e PMOC. Arquivos: `pages/EquipmentRoute.tsx`, `pages/Equipment.tsx`, `components/customers/EquipmentPageChrome.tsx`, `EquipmentPanel.tsx`, `EquipmentFormDialog.tsx`, `EquipmentFieldConfigDialog.tsx`, `pages/EquipmentDetail.tsx`.

### 6.1 Cabeçalho, abas e botões

- Rotas `/equipamentos` e `/equipamentos/<nome>-<código>` usam o mesmo componente (`EquipmentRoute.tsx:16-22`): no computador a lista continua montada ao abrir uma ficha; no celular `/equipamentos/<id>` mostra só a ficha.
- Título **"Equipamentos"**, subtítulo "Gerencie equipamentos e categorias". Abas sublinhadas **"Equipamentos"** e **"Categorias"** (estado local; o endereço não muda).
- Botões do computador, só na aba "Equipamentos" (`EquipmentPageChrome.tsx:46,55-68`):
  - **"Configurar Campos"**: aparece para **todos** (sem checagem), mas gravar exige admin ou gestor no banco (6.5);
  - **"Novo Equipamento"**: só admin, gestor ou `fn:manage_equipment` (`:40,61`).
- Celular: o cabeçalho não tem botões. Criar é o botão flutuante **"Equipamento"** (`EquipmentPanel.tsx:718-724`) e a configuração é o botão **"Campos"** da barra da lista; **os dois só para quem gerencia** (`:326,718`).
- O cabeçalho continua na tela com a ficha aberta.

### 6.2 Lista de equipamentos — `components/customers/EquipmentPanel.tsx`

**Computador** (`:351-425`, `ListDetailLayout`, chave `equipment-list-detail`):

- Coluna da esquerda **"Lista de Equipamentos"**. Cada linha: a **foto** (quadrada; clicar amplia) ou, sem foto, um quadradinho **na cor da categoria** com ícone de caixa (cinza sem categoria); o **nome**; embaixo `identificador · cliente · categoria`; e uma bolinha à direita (verde = Ativo, cinza = Inativo, com dica de texto).
- **Busca** "Buscar equipamentos...": trecho de nome, identificador, cliente, categoria, marca, modelo e local (`:355-356`). **Não procura pelo nº de série.** Ordem Nome (A-Z)/(Z-A), páginas de 10/25/50/100/Todos (padrão 25), lembradas na sessão.
- **Filtros**: ícone de funil **"Filtros"** dentro da caixa de busca (com bolinha numérica quando há filtro), que abre um painel pela direita com "Limpar tudo" e o botão "Aplicar (n)" / "Fechar" (`:384-388`, `:284-305`, seção 7.2). Dois grupos de caixas de seleção múltipla: **"Categoria"** (cada categoria com sua bolinha de cor; vazio = "Todas categorias") e **"Cliente"** (só clientes que já têm equipamento; vazio = "Todos clientes").
- Não há "Editar"/"Excluir" na linha: ficam na ficha (6.7).
- Painel direito sem seleção: **"Selecione um equipamento"** / "Escolha um equipamento na lista para abrir a ficha, os anexos, as tarefas e as ações.". Sem nenhum cadastrado: **"Nenhum equipamento cadastrado"** / "Adicione um equipamento para começar". Filtro sem resultado: **"Nenhum equipamento encontrado"** / "Tente filtros diferentes". Erro: **"Erro ao carregar equipamentos"** / "Não foi possível conectar ao servidor. Tente novamente." + **"Tentar novamente"**.

**Celular e tablet** (`:310-347`, `:426-603`):

- Barra com busca **"Buscar equipamentos..."** (tolerante; nome, identificador, marca, modelo, cliente), seletor **Lista / Grade** (padrão Lista; guardado em `localStorage` `equipment-view-mode`), botão **"Filtros"** (os mesmos dois grupos) e **"Campos"**.
- **Carrossel de indicadores por categoria** (só se existir categoria): um cartão por categoria com a contagem; tocar liga ou desliga o filtro daquela categoria (`:263-280,343-345`).
- **Lista**: miniatura (ou cor da categoria), "Nome · Modelo", `categoria • cliente` (ou o identificador), etiqueta **"Ativo"/"Inativo"**. Menu da linha **"Editar"** e **"Excluir"** (só para quem gerencia).
- **Grade**: cartão com foto à esquerda, "Nome · Modelo", cliente e selo da categoria. **No celular a grade não tem botões de editar/excluir** (`EquipmentGridCard` só mostra quando `!isMobile`, `:112`); é preciso abrir a ficha ou usar a Lista.
- Páginas de 10. Vazio: "Nenhum equipamento cadastrado" / `Toque em "Novo Equipamento" para começar` (Lista) ou "Adicione um equipamento para começar" (Grade); com busca ou filtro: "Nenhum equipamento encontrado" / "Tente filtros diferentes".

### 6.3 Janela "Novo Equipamento" / "Editar Equipamento" — `components/customers/EquipmentFormDialog.tsx`

**Como abre**: botão "Novo Equipamento" (computador), botão flutuante "Equipamento" (celular), aba Equipamentos da ficha do cliente (cliente já escolhido, seção 4.5), "Editar" na ficha do equipamento, "Editar" no menu da linha (celular).

Janela `ResponsiveModal`, duas colunas a partir de `sm`. Rodapé: **"Cancelar"** e **"Criar"** (novo) ou **"Salvar"** (edição), com indicador girando enquanto grava ou sobe a foto (`:272-280`). Campos na ordem em que aparecem:

| # | Rótulo na tela | Tipo e placeholder | Obrigatório | Regras e padrão |
|---|---|---|---|---|
| 1 | **Foto** (quadrado tracejado com o texto "Adicionar") | Imagem (`accept="image/*"`), prévia de 96 px com um **X** para remover | Não | Passa por `processImageFile`: HEIC vira JPEG e a imagem é reduzida para no máximo 1920 px (JPEG 82%; JPEG até 500 KB passa direto). Só sobe ao salvar, para o bucket `equipment-files` em `photos/<uuid>_<nome>` (`:175-198`). Clicar no X e salvar grava `photo_url = null`. |
| 2 | **Cliente \*** | Lista com busca ("Selecione o cliente", busca "Buscar cliente...") com um **botão "+"** colado à direita (dica "Criar cliente") | **Sim** | Ocupa as duas colunas. A busca olha nome, razão social, nome fantasia, documento, e-mail, telefone e celular; o texto pequeno de cada opção mostra o primeiro entre documento, e-mail, telefone e celular. Se a empresa tem **um único cliente**, ele já vem escolhido (`:77`). Vazio: "Nenhum resultado encontrado.". Vazio ao salvar: aparece o texto cru **`customer_required`** sob o campo (`:33`). |
| 3 | **Nome \*** | Texto, "Nome do equipamento" | **Sim** | Vazio ao salvar: texto cru **`name_required`** (`:34`). |
| 4 | **Identificador** | Texto cinza, **somente leitura**, "Gerado automaticamente ao salvar" (só no cadastro novo) | — | Quem gera é o banco: número sequencial por empresa com 4 dígitos ("0001", "0002"...), único por empresa (seção 13). Na edição mostra o valor atual. |
| 5 | **Categoria** | Lista com bolinha de cor, "Selecione" | Não | **Só aparece se já existir ao menos uma categoria** (`:375`). Não dá para criar categoria dentro desta janela (aba "Categorias", 6.6). |
| 6+ | **Campos configuráveis visíveis**, na ordem de "Configurar Campos". Padrão: **Marca**, **Modelo**, **Nº de Série**, **Capacidade/Especificação**, **Local**, **Data de Instalação** | Texto (placeholder = o próprio rótulo); "Data de Instalação" é seletor de data ("dd/mm/aaaa", com "Limpar") | Conforme a configuração | O rótulo ganha " \*" quando marcado como obrigatório, **mas o formulário não bloqueia** o salvamento desses seis campos (`:416`, `:203`). Renomear, ocultar, reordenar ou apagar é pela janela 6.5. |
| 6+ | **Campos personalizados** criados pela empresa | Texto, Número (decimal), Data, Sim/Não ("Selecione", opções "Sim" e "Não") ou Lista de opções ("Selecione" + opções cadastradas) | Conforme a configuração | **Obrigatório vale aqui**: ao salvar, se faltar algum, toast vermelho **"Preencha os campos obrigatórios"** listando os nomes, rótulo em vermelho e o texto **"Campo obrigatório"** sob o campo (`:201-214,510-512`). Lista de opções sem opções cadastradas vira campo de texto. Os valores ficam no JSON `custom_fields`, guardados como texto (Sim/Não grava `sim`/`nao`). |
| — | **Validade da Garantia** | Seletor de data "dd/mm/aaaa" com "Limpar" | Não | Sempre presente, fora da configuração de campos (`:517-536`). |
| — | **Observações** | Área de texto, "Observações adicionais" | Não | Ocupa as duas colunas. |

**Ao salvar** (`:200-259`):

1. Valida Cliente e Nome (mensagens cruas) e os personalizados obrigatórios (toast).
2. Se há foto nova, sobe para o armazenamento e pega o endereço público.
3. Textos vazios viram nulo; em `custom_fields` só entram valores preenchidos (**apagar o último valor de um campo personalizado e salvar não o remove**, `:240-242`).
4. Cadastro novo: `INSERT` com `company_id` e toast **"Equipamento criado com sucesso!"**. Edição pela ficha: `UPDATE` e a página **recarrega inteira, sem toast** (`EquipmentDetail.tsx:1196-1200`). Edição pelo menu da lista no celular: `UPDATE` com toast **"Equipamento atualizado!"** (`EquipmentPanel.tsx:201-214`).
5. Se a gravação termina sem erro, a janela fecha (`:244-250`). **Falha em cadastro novo** (pela lista ou pela aba do cliente): saem **dois** toasts vermelhos em sequência, **"Erro ao criar equipamento"** (do hook, com o motivo traduzido) e **"Erro ao salvar equipamento"** (da janela, com a mensagem **crua** do servidor, ou "Não foi possível salvar o equipamento." se o erro não for um `Error`); só o segundo fica na tela e **a janela continua aberta** (`:251-258`). **Falha na edição pela ficha**: só o "Erro ao salvar equipamento" (a ficha repassa o erro sem aviso próprio) e a janela também continua aberta. **Falha na edição pela lista ou pela aba do cliente**: sai **"Erro ao atualizar"** com o motivo traduzido e a janela **fecha mesmo assim**, porque essas telas tratam o erro e não o repassam. Quem simular erro no backend falso deve mandar um `message` já em português.

**Rascunho**: há uma cópia do que foi digitado em `sessionStorage` (`equipment-form-draft`), mas ela é **apagada quando a janela fecha**; só protege contra a janela reiniciar com ela aberta. Não existe "Retomar rascunho" como no cliente.

**Regras de "Cliente" quando vem da ficha do cliente**: o formulário recebe só aquele cliente e o seleciona sozinho; o botão "+" continua visível.

### 6.4 Criação rápida de cliente (botão "+" do campo "Cliente \*") — `components/financial/QuickCustomerDialog.tsx`

É a "criação rápida só com o nome" da trilha. Abre sobre a janela do equipamento; o texto digitado na busca do campo vira o **Nome** (`CustomerSelectField.tsx:130-137,194-203`).

- Título **"Novo cliente"**, subtítulo "Preencha os dados mínimos para criar e já cobrar o cliente." (o texto fala em cobrar porque a janela é compartilhada com o Financeiro; neste fluxo não há cobrança).
- Campos:

| Rótulo | Tipo e placeholder | Obrigatório | Regras |
|---|---|---|---|
| **Nome** | Texto, "Nome completo ou razão social" | **Sim** (o botão "Criar cliente" fica desligado sem nome) | Pré-preenchido com a busca. |
| **CPF / CNPJ** | Máscara híbrida, "000.000.000-00" | **Não** neste fluxo (`requireDocument={false}`, `EquipmentFormDialog.tsx:339`) | Com 14 dígitos consulta a BrasilAPI e preenche Nome (se vazio), E-mail e Telefone. **Sem validação de dígito verificador** (seção 9). |
| **E-mail (opcional)** | E-mail, "email@exemplo.com" | Não | — |
| **Telefone (opcional)** | Máscara de celular, "(11) 99999-9999" | Não | Grava na coluna `celular`. |

- Botões **"Cancelar"** e **"Criar cliente"** ("Criando…").
- O cliente é gravado com tipo **PJ se o documento tiver 14 dígitos, senão PF**, documento **com máscara** do jeito que foi digitado, e, com o módulo PDV, "Atende como: Serviço". Nada de endereço, origem ou foto: completar depois em "Editar Cliente" (`QuickCustomerDialog.tsx:93-107`).
- Sucesso: toast **"Cliente criado com sucesso!"** (do hook de clientes), a janela fecha e o novo cliente já fica **escolhido** no campo "Cliente \*". O nome aparece quando a lista de clientes termina de recarregar.
- Falha: o hook mostra o toast de erro e a janela continua aberta.

### 6.5 Botão "Configurar Campos" (campos personalizados do equipamento) — `components/customers/EquipmentFieldConfigDialog.tsx`

Janela larga **"Configurar Campos do Equipamento"** com o texto: "Configure quais campos aparecem no cadastro de equipamentos. Você pode excluir, ocultar, renomear, reordenar e definir como obrigatório." Abre pelo botão "Configurar Campos" (computador) ou "Campos" (celular).

**Salva sozinha, a cada alteração.** Não existe botão "Salvar": para terminar, use o botão **"Fechar"** do canto superior direito (todo modal do app tem; clicar fora não fecha, seção 7.1). Cada mudança bem-sucedida pisca um **"Salvo"** com um tique ao lado do campo por 1,5 s (`:384-396`).

**Lista no computador** (`:654-695`, linhas em `:173-328`), com cabeçalho **Nome · Tipo · Visível · Obrig.**:

| Coluna | O que faz | Detalhe |
|---|---|---|
| Alça (seis pontinhos, dica "Arrastar para reordenar") | Arrastar a linha para outra posição | Precisa arrastar uns 8 px para começar; também funciona pelo teclado. Ao soltar, grava a posição de **todas** as linhas (`useEquipmentFieldConfig.ts:85-100`). |
| **Nome** | Caixa de texto direto na linha | Renomeia. **Grava ao sair do campo (clicar fora)**; Enter não grava, apenas pula linha (é uma área de texto, `:127-170`). |
| **Tipo** | Lista: **Texto**, **Número**, **Data**, **Sim/Não**, **Lista de opções** | Trocar muda só como o valor aparece: "Trocar o tipo muda só como o valor é exibido — o dado já salvo é preservado." Escolher "Lista de opções" abre o editor de opções embaixo da linha. |
| **Visível** | Interruptor com olho | Desligado: a linha fica esmaecida com o selo **"Oculto"** e o campo some do formulário. |
| **Obrig.** | Interruptor | Liga a obrigatoriedade (vale só para campos personalizados, 6.3). |
| Lixeira | Excluir | Diálogo abaixo. |

**Os seis campos padrão** (Marca, Modelo, Nº de Série, Capacidade/Especificação, Local, Data de Instalação) são linhas como as outras: dá para renomear, ocultar, reordenar, trocar o tipo e **excluir** (`SortableFieldRow` não tem exceção). Uma empresa nova já nasce com eles (seção 13).

**Adicionar novo campo** (`:467-526`), bloco "Adicionar novo campo" no rodapé:

- Caixa **"Nome do campo"**, lista de tipo (padrão **Texto**) e um botão só com o sinal de mais, desligado até haver nome. Enter na caixa também adiciona (se o tipo não for lista).
- Tipo **Lista de opções**: aparece o quadro **"Opções da lista"** com caixas "Opção 1", "Opção 2"..., botão **"Adicionar opção"** e um X em cada caixa (dica "Remover opção"). O botão **"Adicionar campo"** só liga com nome e ao menos uma opção.
- O campo nasce visível, **não obrigatório**, no **fim** da lista; a chave interna é `custom_<horário>`. Toast **"Campo criado!"**.

**Excluir**: diálogo **"Excluir campo"** / "Tem certeza que deseja excluir este campo? Dados já salvos neste campo serão mantidos no banco de dados." com "Cancelar" e "Excluir". Toast **"Campo excluído!"**. Apagar um dos seis padrão **não tem como desfazer pela tela** (não há "restaurar padrão"; a carga inicial só roda na criação da empresa).

**Celular** (`:540-652`): cada campo é uma linha com ícone do tipo (olho cortado se oculto), o nome editável na hora, e embaixo `tipo • Salvo • Oculto • Obrigatório`. Menu da linha: **"Tipo e opções"** (abre `Configurar "{nome}"` com "Tipo do campo" e o editor de opções), **"Mover para cima"**, **"Mover para baixo"**, **"Ocultar"/"Mostrar"**, **"Tornar obrigatório"/"Tornar opcional"**, **"Excluir"**. Vazio: "Nenhum campo configurado".

**Erros**: toasts vermelhos "Erro ao atualizar campo", "Erro ao criar campo", "Erro ao excluir campo", "Erro ao reordenar campos" (a ordem não confere o resultado de cada gravação).

**Quem grava**: a janela e o botão são abertos por qualquer usuário (no computador), mas a tabela só aceita escrita de admin e gestor da empresa (`supabase/migrations/20260817120000_fix_equipment_field_config_rls_tenant_scope.sql`). Para os outros: **criar** campo falha com "Erro ao criar campo" e o motivo "Você não tem permissão para realizar esta ação." (violação de política, `42501`); **editar** (olho, Obrig., nome, tipo, opções) provavelmente falha com "Erro ao atualizar campo" e o motivo "Registro não encontrado.", e **excluir** pode mostrar "Campo excluído!" sem apagar nada, porque para quem não passa na política o banco simplesmente não encontra a linha (comportamento padrão do PostgreSQL com política `FOR ALL`; deduzido, a confirmar com um usuário assim). Reordenar não confere o resultado e não avisa.

**Pontos de atenção para a gravação**:

- Em um campo **já existente** do tipo "Lista de opções", o botão **"Adicionar opção" não acrescenta linha** e apagar o texto de uma opção a remove na hora, porque a tela filtra opções vazias antes de gravar (`:419-422`, `OptionsEditor` controlado pelo valor salvo). **Crie a lista inteira de uma vez no bloco "Adicionar novo campo".** (Leitura do código; a confirmar em tela.)
- Renomear um campo padrão muda o rótulo **no formulário**, mas a **ficha continua mostrando os rótulos fixos** ("Marca", "Modelo", "Nº de Série", "Descrição", "Local", "Data de Instalação") e a etiqueta idem (`EquipmentDetail.tsx:629-635`). Ocultar um campo padrão tira do formulário, mas o valor já salvo continua na ficha. Campos **personalizados** respeitam rótulo e visibilidade na ficha.
- Os seis padrão só aceitam bem os tipos Texto, Número e Data; "Sim/Não" e "Lista" caem em caixa de texto no formulário (`EquipmentFormDialog.tsx:418-438`).

### 6.6 Aba "Categorias" — `pages/Equipment.tsx:36-196`

Para agrupar aparelhos (Split, Cassete, VRF...). Cada categoria tem nome e cor.

- Título **"Categorias de Equipamentos"** e botão **"Nova Categoria"** (sem checagem de permissão na tela; o banco só aceita escrita de admin/gestor, `20260817130000_fix_tenant_config_tables_rls_tenant_scope.sql`).
- Lista em ordem alfabética: bolinha com a cor, nome e, se existir, a descrição (a tela não tem campo de descrição). Menu da linha **"Editar"** e **"Excluir"**.
- **"Nova Categoria"** abre uma janela com **"Nome da categoria"** (placeholder "Ex: Split, Cassete, VRF...", Enter cria) e **"Cor"** (seletor de cor do navegador, padrão `#3b82f6`, mostrando o código ao lado). Botões **"Cancelar"** e **"Criar"** (desligado sem nome). Toast **"Categoria criada com sucesso!"**.
- **Editar** é na própria linha: caixa de nome, seletor de cor, **"Salvar"** (ou Enter) e **"Cancelar"**. Toast **"Categoria atualizada!"**.
- **Excluir**: **"Excluir categoria"** / "Esta ação não pode ser desfeita. Equipamentos com esta categoria perderão a associação." com "Cancelar" e "Excluir". Toast **"Categoria excluída!"**. Os equipamentos ficam, só perdem a categoria (`ON DELETE SET NULL`).
- Vazio: **"Nenhuma categoria criada"** / "Crie categorias para organizar seus equipamentos" com o botão "Nova Categoria".
- Erros: "Erro ao criar categoria", "Erro ao atualizar categoria", "Erro ao excluir categoria".
- Não há contagem de equipamentos por categoria nesta aba (a contagem existe só no carrossel do celular, 6.2).

### 6.7 Ficha do equipamento (`/equipamentos/<nome>-<código>`) — `pages/EquipmentDetail.tsx`

No computador é o painel da direita da lista; no celular ocupa a tela toda.

**Cabeçalho** (`:391-480`):

- Seta de voltar (só no computador): volta para `/equipamentos` ou, se a ficha foi aberta pela aba Equipamentos de um cliente, para aquele cliente na aba Equipamentos (`:395`). Se o equipamento não existe: **"Equipamento não encontrado."** e o botão **"Voltar"** (`:375-381`).
- O **nome** é um botão com seta: abre uma busca **"Buscar equipamento..."** com a lista de todos os equipamentos (nome e, embaixo, `identificador · cliente`) para trocar de ficha sem voltar à lista; sem resultado: "Nenhum equipamento encontrado." (`:398-441`).
- Embaixo do nome: **`ID: 0001`** em fonte de código e a etiqueta **"Ativo"/"Inativo"** (o status não tem controle na tela, nasce "Ativo").
- Botões **"Editar"** (amarelo) e **"Excluir"** (vermelho) no computador; no celular o menu **"Ações"** com os dois. **Aparecem para qualquer usuário**: a ficha não confere `fn:manage_equipment` (só a lista confere).

**Abas** (`:384-389`, sublinhadas; no celular roláveis): **"Geral"**, **"Anexos"**, **"Histórico / Tarefas"**, **"Chamados"**.

**Aba Geral** (`:507-671`):

- Cartão superior: a **foto** (se houver; legenda "Foto do equipamento"; clicar amplia) e o bloco do **QR Code** (100 px, clicar amplia para 280 px sobre fundo preto com o identificador; fecha no X ou clicando fora). Abaixo do QR, o identificador em fonte de código, a legenda **"QR Code do equipamento"** e quatro botões: **"Gerar Etiqueta"**, **"Baixar QR (PNG)"**, **"Abrir link"**, **"Copiar link"**. Os três últimos ficam desligados sem portal ativo, com o aviso **"Cliente sem portal ativo"**. Detalhes em 6.8.
- Cartão **"Informações"** (só aparece se houver algum dado), em duas colunas, **só linhas com valor**, nesta ordem fixa: **Categoria** (com bolinha de cor), **Cliente** (nome azul com seta: leva a `/clientes/<id>`), **Marca**, **Modelo**, **Nº de Série**, **Descrição** (é o campo "Capacidade/Especificação" do formulário), **Local**, **Data de Instalação**, **Garantia até** (dd/MM/aaaa), e depois os campos personalizados visíveis (campo Sim/Não aparece sempre como "Sim" quando tem valor, ver a atenção abaixo; data como dd/MM/aaaa).
- Cartão **"Observações"** (só se houver texto).
- Atenção: datas `aaaa-mm-dd` são lidas como horário UTC (`new Date(...)`), então em navegador no fuso do Brasil **a data pode aparecer um dia antes** (Data de Instalação, Garantia até e campos de data personalizados, `:634-635,641`). Outras telas do app tratam isso com `parseIsoDate`; esta não. (A confirmar na gravação.)
- Atenção: um campo personalizado **Sim/Não** guarda "sim" ou "nao" como texto e a ficha testa só "tem valor", então **"Não" aparece como "Sim"** (`:639`). Evite esse tipo na demonstração ou escolha "Sim".

**Aba Anexos** (`:674-847`, hook `useEquipmentAttachments`):

- Título **"Arquivos anexados"**; seletor de dois ícones **Galeria** / **Lista** (dicas "Galeria" e "Lista") e o botão **"Enviar"** ("Enviando..." durante o envio). O seletor de arquivo aceita **vários arquivos de qualquer tipo**.
- Durante o envio: **"Enviando {n} de {total}..."**, percentual e barra de progresso. Ao terminar: toast **"1 anexo enviado!"** ou **"{n} anexos enviados!"** (conta só os que deram certo). Falha de um arquivo: toast vermelho **"Erro ao enviar anexo"** com o motivo; os outros seguem.
- Os arquivos aparecem agrupados: **"Imagens (n)"**, **"PDFs (n)"**, **"Outros Documentos (n)"** (por extensão; imagens: webp, jpg, jpeg, png, gif, heic, svg). Galeria: grade de 2 a 4 colunas, imagem clicável (amplia), PDF com miniatura da primeira página (clicar abre em outra aba), outros com ícone e nome; ícones de **baixar** e **excluir** no canto, **só ao passar o mouse** (no celular use a Lista, que mostra a lixeira sempre). Lista: uma linha por arquivo com miniatura, nome (link) e lixeira.
- Excluir: **"Excluir anexo"** / "Tem certeza que deseja excluir este anexo?" com "Cancelar" e "Excluir". Toast **"Anexo excluído!"**. Remove só o registro; **o arquivo continua no armazenamento** (`useEquipmentAttachments.ts:67-80`).
- Vazio: ícone de clipe e **"Nenhum anexo"**.
- Por padrão o que for anexado fica **visível para o cliente no portal** (coluna `attachments_public` nasce ligada; o interruptor "Mostrar anexos no portal do cliente" só existe numa janela antiga que não é usada, `EquipmentDetailDialog`).

**Aba Histórico / Tarefas** (`:850-954`):

- Seção **"Ordens de Serviço Relacionadas"**: as OS cujo equipamento principal é este (`service_orders.equipment_id`). Tabela **OS** (número formatado e a descrição curta embaixo) **· Status** (Agendada, Pendente, A Caminho, Em Andamento, Pausada, Concluída ou Cancelada) **· Data** (dia agendado ou "-"; some em tela estreita) **· Ações** (ícone que abre `/os-tecnico/<id>` **em outra aba**). Colunas ordenáveis e paginação. Vazio: **"Nenhuma OS relacionada a este equipamento"**. Uma OS com vários equipamentos só aparece no primeiro deles (`ServiceOrderFormDialog.tsx:625`). Não há botão para criar OS por aqui.
- Seção **"Tarefas"**: lista de verificação simples do aparelho (tabela `equipment_tasks`, **não** é a tarefa da agenda). Caixa **"Nova tarefa..."** e botão com o sinal de mais (Enter também cria; desligado sem texto). Toast **"Tarefa criada!"**. Cada item tem um círculo para marcar como feita (risca o texto) e uma lixeira (**sem confirmação**, toast **"Tarefa excluída!"**). A data de vencimento só aparece se já existir; a tela não permite definir. Vazio: **"Nenhuma tarefa"**.

**Aba Chamados** (`:956-971`): título "Chamados" com o painel de chamados do portal filtrado para as OS deste equipamento. Busca "Buscar por chamado, cliente, equipamento ou contrato...", filtros **"Chamados abertos"/"Todos os chamados"** (aqui abre em "Todos") e **"Todos os portais"/"Portal do Cliente"/"Portal do Contrato"**. Vazio: **"Nenhum chamado recebido"** / "Os chamados abertos pelos portais aparecerão aqui." Abrir um chamado leva a `/ordens-servico?aba=chamados&os=<id>`. A aba aparece sempre, mesmo sem o módulo do portal.

### 6.8 QR Code e etiqueta

**De onde vem o QR** (`EquipmentDetail.tsx:204-225`):

- Busca o portal do cliente do equipamento (`customer_portals.token` com `is_active = true`). Todo cliente novo ganha um portal ativo automaticamente (seção 13).
- Com portal ativo: o QR aponta para `<endereço do sistema>/portal/<token>?eq=<id do equipamento>`. Quem lê com o celular cai no portal já na ficha daquele aparelho (6.9).
- Sem portal ativo (o cliente ou o portal foi desligado, ou o equipamento não tem cliente): o QR vira o texto `EQ-<identificador>` (não abre nada), e os botões "Baixar QR (PNG)", "Abrir link", "Copiar link" ficam desligados com **"Cliente sem portal ativo"**. O item "QR Code" some da lista da etiqueta (`:287`).
- Aparência: `BrandedQRCode`, correção de erro nível H, logo no centro. Sem white-label usa o ícone da Dominex; com white-label usa o logo, o estilo e a cor da empresa (`hooks/useBrandedQrConfig.ts`).

**Botões**:

- **"Baixar QR (PNG)"**: arquivo de 1024 px `qr-<identificador>.png` (`:349-369`) e toast **"QR Code salvo!"**.
- **"Abrir link"**: abre o endereço do portal em nova aba. **"Copiar link"**: copia e mostra **"Link copiado!"**.

**"Gerar Etiqueta"** abre a janela **"Gerar Etiqueta de Identificação"** (`:993-1147`, estados em `:64-111,161-186`):

1. Aviso com ícone de informação: "Ao imprimir, certifique-se que nas configurações de impressão o dimensionamento está em tamanho real."
2. **"Itens da etiqueta"**: caixas de seleção. **Só aparecem os itens que existem para este equipamento** (`:283-295`): **Nome da empresa**, **Telefone da empresa**, **E-mail da empresa** (vêm do cadastro da empresa), **QR Code** (exige portal ativo), **Nome do equipamento**, **Identificador**, **Marca**, **Modelo**, **Nº de série**, **Localização**, **Nome do cliente**. Marcados por padrão: nome, telefone e e-mail da empresa, QR Code, nome do equipamento e identificador. Para aparecerem Marca, Modelo, Nº de série e Localização é preciso ter preenchido esses campos.
3. **"Tamanho"**: três botões **"5×5 cm"**, **"5×8 cm"** (padrão), **"6×6 cm"** (o escolhido fica azul) e as caixas **"Largura (cm)"** e **"Altura (cm)"**. O sistema limita a 2 a 30 cm e lê o número com `parseFloat`: **use ponto** (5.5); "5,5" vira 5.
4. **"Pré-visualização"**: miniatura ao vivo (até 180×260 px) com os itens marcados. A visualização **não mostra os rótulos** "Marca", "Modelo"... que a impressão mostra.
5. **"Imprimir"**: abre **outra aba** com a etiqueta no tamanho escolhido (título "Etiqueta - <nome>", papel do tamanho da etiqueta, sem margem, sem a borda cinza) e chama a impressão do navegador 0,3 s depois (`:304-346`). Se o navegador bloquear janelas, **nada acontece e não há aviso**. O QR da etiqueta tem 80 px.
6. As escolhas ficam gravadas no navegador (`localStorage` `equipment-label-config`), valem para **todos os equipamentos** e se perdem ao trocar de navegador ou limpar dados.

### 6.9 O que o cliente vê ao ler o QR Code (portal) — `pages/CustomerPortal.tsx:588-1250`

- Endereço `/portal/<token>?eq=<id>`: o portal abre na aba de equipamentos com o aparelho já selecionado (`:589,637`). Cabeçalho com foto, nome, `marca · modelo` e etiqueta Ativo/Inativo; botão para voltar à lista.
- Subabas **"Visão geral"** (dados fixos e campos personalizados visíveis), **"Histórico"** (OS do equipamento, com "Ver relatório") e **"Anexos"**.
- Anexos: **"Nenhum anexo disponível"** / "O técnico não adicionou anexos a este equipamento." ou, se o interruptor por equipamento estiver desligado, **"Anexos não disponíveis"** / "Os anexos deste equipamento estão restritos." (`customers.ts:418-421`).
- O que o portal mostra depende da aba "Portal" do cadastro do cliente (seção 3.4.3) e da senha, se houver.

### 6.10 Editar e excluir

| Onde | Como | O que acontece |
|---|---|---|
| Ficha, computador | Botões **"Editar"** / **"Excluir"** do cabeçalho | Editar abre o formulário 6.3 e, ao salvar, **recarrega a página inteira sem avisar** (`:1192-1204`). Excluir: diálogo abaixo. |
| Ficha, celular | Menu **"Ações"** | Igual. |
| Lista, celular (modo Lista) | Menu da linha | Editar com toast "Equipamento atualizado!"; excluir com toast "Equipamento excluído!" ou erro "Erro ao excluir" + motivo (`EquipmentPanel.tsx:216-228`). Só com admin, gestor ou `fn:manage_equipment`. |
| Aba Equipamentos do cliente | Menu da linha | Mesmo comportamento (seção 4.5). |

- Diálogo **"Excluir equipamento"** / `Tem certeza que deseja excluir "{nome}"? Esta ação não pode ser desfeita.` com "Cancelar" e "Excluir" (vermelho).
- **Excluir pela ficha ignora erro e não mostra toast**: executa o `DELETE`, volta para a lista (ou para o cliente de origem) e não atualiza a lista em memória (`:1217-1226`); no computador o equipamento apagado pode continuar na lista até a próxima atualização da tela.
- **O que impede a exclusão**: contratos (a chave `contract_items.equipment_id` não define regra de exclusão em nenhuma migração, então o banco recusa; a confirmar no banco real). O erro só chega ao usuário pelos caminhos que o mostram (menu da linha da lista no celular e aba Equipamentos do cliente, que também existe no computador), nunca pela ficha. O texto exato depende do formato do erro (`utils/errorMessages.ts:357-396`): um erro de banco com código `23503` (o normal vindo do servidor) vira **"Não é possível concluir porque há referências relacionadas. Remova-as primeiro."**; o texto específico "Este equipamento não pode ser excluído porque está vinculado a ordens de serviço, contratos ou planos PMOC." (`:131`) só aparece quando o erro chega **sem** código (só com a mensagem `violates foreign key constraint … _equipment_id_fkey`). Quem fizer o backend falso deve decidir qual dos dois quer mostrar (seção 12.0).
- O que **não** impede: OS (`service_orders.equipment_id` fica nulo), respostas de formulário (nulo); anexos, tarefas, planos PMOC (`pmoc_schedules`) e equipamentos de OS (com os serviços por equipamento) são apagados junto (cascata).
- Excluir cliente (exclusão lógica) **não** apaga nem esconde seus equipamentos; eles continuam na lista.

---

## 7. Componentes compartilhados (como se comportam em todas as telas)

### 7.1 Janelas de formulário (`ResponsiveModal`) — `components/ui/ResponsiveModal.tsx`

Quase toda janela destas telas passa por aqui: Novo/Editar Cliente, Novo/Editar Equipamento, Novo/Editar Fornecedor, Configurar Campos, Nova Categoria, "Novo cliente" (rápido), Origens, "Nova origem", Formulários de captação (lista e editor), Gerar Etiqueta e Exportar meus dados. **Duas exceções**: a janela de contato ("Novo Contato" / "Editar Contato") usa o `Dialog` simples, e os diálogos "Excluir …" usam `AlertDialog`.

- **Abaixo de 1024 px** (celular e tablet; `hooks/use-mobile.tsx:3-4`) a janela é uma **gaveta que sobe de baixo** (`ResponsiveModal.tsx:50-98`): alça cinza no topo (só ela arrasta para fechar), título centralizado, botão **"Fechar"** no canto superior direito, conteúdo rolável, **rodapé fixo** com os botões e altura máxima de 90% da tela.
- **De 1024 px para cima** é uma **janela centralizada** (`:100-120`): título, conteúdo rolável, rodapé com uma linha em cima, altura máxima de 90% da tela e o botão **"Fechar"** no canto superior direito (`components/ui/dialog.tsx:250-258`).
- **Clicar ou tocar fora da janela não fecha** (`:55-58,103-106`). Fecha pelo "Fechar", pelos botões do rodapé ("Cancelar", "Salvar" etc.), pela tecla Esc (computador) ou arrastando a alça (celular). Na narração diga "Fechar", nunca "clique fora".
- O botão "Fechar" tem um X e o texto em maiúsculas por estilo (na tela se lê FECHAR; o rótulo é "Fechar"). É cinza e fica vermelho ao passar o mouse ou ao tocar (`dialog.tsx:17-45`).

| Janela | Largura no computador | Fonte |
|---|---|---|
| Novo/Editar Cliente | 768 px | `CustomerFormDialog.tsx:355` |
| Configurar Campos do Equipamento | 768 px | `EquipmentFieldConfigDialog.tsx:530` |
| Novo/Editar Fornecedor | 520 px | `SupplierFormDialog.tsx:75` |
| Equipamento, cliente rápido, categoria, origens, formulários de captação, etiqueta, exportação | 600 px (padrão) | `ResponsiveModal.tsx:103` |
| Novo/Editar Contato | 448 px; **clicar fora FECHA** e perde o que foi digitado | `ContactFormDialog.tsx:113-114` |
| Diálogos "Excluir …" (`AlertDialog`) | 512 px centralizados; no celular sobem de baixo | `components/ui/alert-dialog.tsx:119-161` |

### 7.2 Lista com ficha ao lado (`ListDetailLayout`, só no computador) — `components/ui/ListDetailLayout.tsx`

Usada por Clientes, Fornecedores e Equipamentos.

- Duas colunas: a lista, com 320 a 384 px, e a ficha. Abaixo de 1024 px esta estrutura não é usada (kit do celular, 7.3).
- Topo da lista: título (por exemplo "Lista de Clientes"), uma **bolinha com a contagem** de registros e o ícone **"Recolher lista"**. Recolhida, a lista vira uma faixa de 40 px com um único botão **"Expandir lista"** (`:323-377`).
- Caixa de busca com lupa e, **dentro da própria caixa, à direita**, ícones de ação que só mostram a palavra ao passar o mouse (dica após 0,35 s) (`components/ui/search-field-actions.tsx:48-105`):
  - **"Ordenar"** (setas): menu com **"Nome (A-Z)"** e **"Nome (Z-A)"**; a escolhida fica destacada, com "A-Z" ou "Z-A" ao lado. A ordem ignora acento e maiúscula (`:141-150`).
  - **"Filtros"** (funil, só em Equipamentos, com bolinha numérica quando há filtro): abre um painel que desliza **da direita** (`components/ui/FilterButton.tsx`) com o título "Filtros", o link **"Limpar tudo"** (só com filtro ativo) e, no rodapé, o botão **"Aplicar (n)"** ou **"Fechar"** (sem filtro).
- Busca: trecho do texto, sem diferenciar maiúscula, **com acento diferenciado**, sobre título + subtítulo + texto extra de cada tela (`:164-176`). Busca ou ordem nova volta para a página 1 (`:194-207`).
- Linhas: foto (ou ícone), título, subtítulo e um selo à direita; a linha aberta fica destacada. Abrir a ficha de um item que está em outra página faz a lista **pular para a página dele** (`:181-197`). Se a linha tem foto, ela vale mais que o ícone.
- Rodapé: seletor **"Por página"** (10, 25, 50, 100 ou "Todos"; padrão 25), o texto **"Mostrando {de}-{até} de {total}"** e duas setas, só ícone, com as dicas **"Anterior"** e **"Próxima"** (`:437-478`).
- A altura da coluna é medida na tela para o rodapé nunca ficar escondido; a lista rola por dentro (`:208-241`).
- Lembrança: busca, ordem, página e tamanho ficam no `sessionStorage` do navegador sob a chave da tela (`customers-list-detail`, `suppliers-list-detail`, `equipment-list-detail`) e sobrevivem a abrir e fechar fichas e a recarregar; somem ao fechar a aba (`:80-93,136-160`, `hooks/useDataPagination.ts:5-25`).

### 7.3 Kit do celular e do tablet (`components/mobile/*`)

| Peça | Como é |
|---|---|
| `MobileListToolbar` | 1ª linha: busca de largura total (40 px de altura). 2ª linha: filtros e ações à esquerda, alternador Lista/Grade à direita. No máximo 3 controles na 2ª linha. |
| `ViewModeToggle` (`components/ui/ViewModeToggle.tsx`) | Dois botões com ícone (dicas "Ver como lista" e "Ver como grade"). Padrão Lista; a escolha fica no `localStorage` (`customers-view-mode`, `equipment-view-mode`). |
| `MobileListItem` | Linha de no mínimo 72 px: foto ou ícone, título, subtítulo, selo e botão de três pontos (**"Mais ações"**). **Deslizar a linha para a esquerda** revela botões de 80 px com ícone e texto: **Editar** (amarelo) e **Excluir** (vermelho); só uma linha fica aberta por vez, rolar a página fecha, e tocar numa linha aberta só a fecha. Ações sem cor (como "Visualizar") só existem no menu de três pontos. |
| `FABButton` | Botão flutuante arredondado, com ícone e texto, no canto inferior direito, acima da barra inferior ("Cliente", "Equipamento", "Novo Equipamento"…). No computador o mesmo componente vira um botão comum. |
| `FilterSheet` | Botão **"Filtros"** (com contador) que abre uma gaveta de baixo com os filtros e, no rodapé, **"Limpar"** e **"Aplicar"**. |
| `StatCarousel` | Faixa horizontal de cartões de indicador que também são botões (em Equipamentos, um por categoria). |
| `EmptyState` | Ícone, título, descrição e botão opcional. É o "estado vazio" padrão de todas as listas. |
| `MobilePillTabs` | Abas roláveis. Na tela de Clientes e na de Equipamentos usam o estilo sublinhado. |

Em celular e tablet a barra inferior tem "Clientes" mas não tem "Equipamentos" (seção 1.1).

### 7.4 Máscaras de texto (`utils/masks.ts`)

| Máscara | Comportamento | Onde aparece nestas telas |
|---|---|---|
| `phoneMask` (`:10-22`) | Fixo e celular no mesmo campo: até 10 dígitos "(11) 3333-4444"; no 11º dígito vira "(11) 93333-4444". Tira o "55" do começo quando o número tem 12 ou 13 dígitos. | Telefone do cliente, Telefone do contato, Telefone e Celular do formulário público |
| `mobileMask` (`:29-37`) | Sempre "(00) 00000-0000" (até 11 dígitos); tira o "55" de números de 13 dígitos. | Celular do cliente; Telefone do cliente rápido |
| `cpfCnpjMask` (`:40-62`) | Até 11 dígitos formata CPF "000.000.000-00"; de 12 a 14, CNPJ "00.000.000/0000-00". Campo com 18 caracteres. | CPF/CNPJ da aba Fiscal, do cliente rápido e do formulário público |
| `cepMask` (`:73-80`) | "00000-000". | CEP do cliente e do formulário público |
| `cnpjMask` (`:64-71`) | Sempre formato de CNPJ. | Não é usada nestas telas |
| (sem máscara) | O texto fica como foi digitado. | CPF/CNPJ, Telefone e Endereço do **fornecedor**; Inscrição Municipal e Estadual |

Nos formulários internos o documento e o CEP são **gravados com a máscara**; o formulário público grava **só dígitos** (seção 12.8).

### 7.5 Campo de data (`components/ui/DatePicker.tsx`)

- Não se digita a data. O campo é um botão com ícone de calendário que mostra `dd/MM/aaaa` (ou o texto de apoio quando vazio); clicar abre um calendário com **seletores de mês e de ano** (de 100 anos atrás até 20 anos à frente da data de hoje, ampliado se a data já gravada estiver fora da faixa) (`:54-91,168-189`).
- Escolher um dia fecha o calendário. Quando o campo permite limpar, aparece sob o calendário um botão com a palavra "Limpar" (o texto vem da tela que usa o componente) (`:190-205`).
- O valor sai como texto `aaaa-mm-dd` e é lido **sem passar por UTC** (`parseIsoDate`, `:41-47`), então este campo não tem o problema do "dia anterior" que a ficha do equipamento tem ao exibir a data (seção 6.7).
- Onde aparece: Data de Nascimento (cliente), Data de Instalação, Validade da Garantia e campos personalizados do tipo Data (equipamento) (`CustomerFormDialog.tsx:552`, `EquipmentFormDialog.tsx:422,462,525`).

### 7.6 Avisos na tela (toasts) e mensagens de erro

- Estas telas usam o sistema de avisos `useToast` (Radix). Nenhuma delas usa o aviso `sonner` que também está montado no app (`App.tsx:984-985`).
- Posição: **canto inferior direito** no computador (largura até 420 px) e **embaixo, acima da barra inferior** no celular (`components/ui/toast.tsx:10-35`). Só cabe **um aviso por vez** (`hooks/use-toast.ts:5`): um aviso novo substitui o que está na tela (por isso, quando dois avisos saem em seguida, só o último aparece). Some sozinho (o padrão do Radix é cerca de 5 s; nenhuma tela define outro tempo; deduzido) e tem um X.
- Formato: título em destaque e, nos erros (vermelho), uma descrição com o motivo, por exemplo `toast({ variant: 'destructive', title: 'Erro ao criar cliente', description: getErrorMessage(error) })` (`hooks/useCustomers.ts:84`).
- O motivo vem de `getErrorMessage` (`utils/errorMessages.ts:357-422`), nesta ordem:
  1. nome de restrição específica (só duas, de outras telas);
  2. códigos da agenda (`schedule_*`);
  3. **código SQLSTATE do erro** (`:57-82`): `23502` "Algum campo obrigatório não foi preenchido."; `23503` "Não é possível concluir porque há referências relacionadas. Remova-as primeiro."; `23505` "Já existe um registro com esses dados."; `23514` "Algum valor está fora do permitido (verifique limites e restrições)."; `22P02` "Algum valor está em formato inválido."; `22001` "Algum texto é muito longo para o campo."; `22003` "Algum número está fora do intervalo permitido."; `42501` "Você não tem permissão para realizar esta ação."; `57014` "Operação demorou demais e foi cancelada. Tente novamente."; `08000`/`08006` "Sem conexão com o servidor. Verifique sua internet e tente novamente."; `PGRST116` "Registro não encontrado."; `PGRST301` "Sessão expirou. Faça login novamente.";
  4. trechos da mensagem (`:86-312`): "row-level security" vira "Você não tem permissão para realizar esta ação."; "failed to fetch" vira "Sem conexão com a internet. Verifique sua rede e tente novamente."; "timeout" vira "O servidor demorou para responder. Tente novamente em alguns instantes."; "jwt expired" vira "Sua sessão expirou. Faça login novamente.";
  5. texto que parece erro técnico em inglês vira "Ocorreu um erro inesperado. Tente novamente." (`:1`); qualquer outro texto aparece como veio.
- Para funções de servidor (`functions.invoke`) o motivo real vem do corpo da resposta (`getInvokeErrorMessage`, `:324-343`): o servidor deve responder `{ "error": "texto em português" }` com status diferente de 2xx.

### 7.7 Seletores e utilitários

- **Lista com busca (`SearchableSelect`, `components/ui/SearchableSelect.tsx`)**: botão com seta dupla; abre um painel com busca. A busca é **tolerante**: ignora acento, aceita palavras fora de ordem e, quando só há números (3 dígitos ou mais), compara só os dígitos (`lib/utils.ts:14-69`, `components/ui/searchableSelectFilter.ts`). Zera a busca ao fechar. Vazio padrão: "Nenhum resultado encontrado.". Usado em Cliente \* e Origem; o seletor de **Cidade** tem painel próprio, com a mesma busca tolerante (`components/StateCitySelector.tsx`).
- **Campo de cliente (`CustomerSelectField`, `components/customers/CustomerSelectField.tsx`)**: lista com busca + botão quadrado **"+"** (dica "Criar cliente") colado na borda. Mostra nome e, embaixo, o primeiro entre documento, e-mail, telefone e celular; a busca olha também razão social e nome fantasia. O texto digitado na busca **fica guardado** e vira o Nome do cliente rápido, mesmo depois de escolher outro cliente (`:98-105,130,165,196`). Quando o formulário que o usa passa `onCreateFull`, o "+" abre o cadastro completo de cliente em vez do rápido (Contrato e OS com vários equipamentos). Está em: Equipamento, OS, Contrato, Orçamento, CRM (oportunidade), Projeto, Tarefa da agenda, PDV, Financeiro (lançamento, cobrança, assinatura, conta, conciliação) e Nova nota fiscal.
- **Menu de ações da linha (`RowActionsMenu`, `components/ui/RowActionsMenu.tsx`)**: botão de três pontos (rótulo de acessibilidade "Ações", sem texto na tela). No computador abre ao **passar o mouse** (80 ms) e fecha 0,2 s depois que o mouse sai; também abre ao clicar. Ao destacar, "Editar" fica amarelo e "Excluir" vermelho.
- **Ampliar imagem (`ImagePreviewModal`, `components/ui/ImagePreviewModal.tsx`)**: tela escura com a imagem; no canto, o contador "n / total" (galeria), o botão de baixar (dica "Baixar imagem") e o X; setas dos lados e teclas ← e → navegam; Esc e clicar no fundo fecham. No iPhone, "baixar" abre a folha de compartilhar.
- **QR Code (`components/BrandedQRCode.tsx`)**: correção de erro nível H, logo no centro e cores definidas por `hooks/useBrandedQrConfig.ts` (seção 6.8).

---

## 8. Importação, exportação e ligação com outros módulos

### 8.1 Importar e exportar

- **Nenhuma** destas telas (Clientes, Fornecedores, Equipamentos) tem botão de importar planilha, exportar CSV ou Excel, imprimir lista ou baixar relatório. O cadastro em massa de clientes **não existe** na tela; o caminho de entrada de vários clientes é o formulário de captação (um por vez, seção 3.10).
- O único importador de planilha do sistema é o do Financeiro (`components/financial/ImportSpreadsheetDialog.tsx`), fora do escopo do T3. O arquivo `hooks/useEquipmentCatalog.ts` é um catálogo global da área do técnico, **não** é o cadastro de equipamentos do cliente.
- **Exportação**: Configurações → aba **"Empresa"** → cartão **"Exportar meus dados"** ("Baixe uma planilha do Excel com os dados da sua empresa: clientes, equipamentos, ordens de serviço, orçamentos, contratos, financeiro e mais. Serve de backup e para levar seus dados para onde quiser.") → botão **"Exportar dados"** (`components/settings/DataExportCard.tsx`, `pages/Settings.tsx:1629`).
  - Janela **"Exportar meus dados"**: "Escolha o que deseja incluir na planilha. O arquivo é gerado na hora e baixado automaticamente." Caixas de seleção por grupo (Clientes, Equipamentos, Ordens de Serviço, Orçamentos, Contratos, Financeiro, Estoque, Movimentações de Estoque, Vendas do PDV, Fiado dos Clientes, Funcionários, CRM / Leads e Ponto), mais **"Marcar tudo"** e **"Limpar seleção"** (`lib/i18n/messages/app/settings.ts:415-447`).
  - O grupo **Clientes** gera as planilhas **"Clientes"** e **"Contatos dos Clientes"**; o grupo **Equipamentos** gera **"Equipamentos"**. **Fornecedores não entram** na exportação. Movimentações de Estoque e Ponto vêm desmarcados por causa do tamanho.
  - Botões **"Cancelar"** e **"Exportar"**. Durante a geração: "Exportando…" e a linha "Exportando {planilha}… {n} registros" com barra de progresso; a janela não fecha enquanto exporta. Fim: aviso **"Exportação concluída! O arquivo foi baixado."**; falha: **"Não foi possível exportar os dados. Tente novamente."**; sem seleção: "Selecione pelo menos um item para exportar." O arquivo é um `.xlsx` com nome começando por "backup".
  - Quem vê o cartão: administrador, super administrador ou usuário com a permissão `fn:export_company_data` ("Exportar Dados da Empresa") **e** com registro em `user_permissions` (`pages/Settings.tsx:120-127`).

### 8.2 Com quem estes cadastros conversam

| Módulo | Ligação | Onde se vê |
|---|---|---|
| Ordens de Serviço | `service_orders.customer_id` e `equipment_id` (equipamento principal); `service_order_equipment` guarda vários equipamentos por OS | Aba "Histórico" e botão "Nova OS" na ficha do cliente (seção 4.6); aba "Histórico / Tarefas" do equipamento (6.7) |
| Agenda e tarefas | Tarefa é uma OS do tipo `tarefa` com o cliente | Aba "Tarefas" da ficha do cliente (4.7) |
| Contratos e PMOC | `contracts.customer_id`; `contract_items.equipment_id` (impede excluir o equipamento); `pmoc_schedules` cai junto com o equipamento | Aba "Contratos" e botão "Novo Contrato" (4.10); mensagem de exclusão (6.10) |
| CRM | Ação "Criar oportunidade no CRM"; a lista de **origens** é a mesma do CRM | Menu "Ações" da ficha (4.1); Configurações → Usabilidade → "Origens" (3.9) |
| Financeiro e cobranças | Abas "Financeiro" e "Cobranças" da ficha; `financial_transactions.supplier_id` alimenta o "Histórico de Gastos" do fornecedor; para **cobrar**, o cliente precisa de CPF ou CNPJ válido (seção 9) | 4.12, 4.13, 5.4 |
| Fiscal (NFS-e) | Os dados do tomador vêm do cliente: documento, inscrições, endereço, número e código IBGE do município. No endereço avulso a nota exige logradouro, número, bairro, CEP e código IBGE (`components/fiscal/NovaNotaModal.tsx:119-137`) | Aba "Fiscal" do cadastro (3.4.2): por isso o CEP importa |
| Estoque e compras | Aba "Estoque" do cliente (material que fica no cliente, 4.8); fornecedores são usados em Compras, Cotação e movimentações | 5.7 |
| Portal do cliente | `customer_portals`; o QR do equipamento aponta para o portal; chamados abertos no portal viram OS com origem `portal` | 3.4.3, 4.9, 6.8, 6.9 |
| Área do técnico | Abrir uma OS leva a `/os-tecnico/<id>` | 4.9, 6.7 |
| Formulários (checklists) | `form_responses.equipment_id` | Some o vínculo (fica nulo) ao excluir o equipamento (6.10) |
| PDV e loja | "Atende como" (Serviço/Loja) e "Fiado em aberto" ao excluir cliente | 3.4.1, 3.8 |
| WhatsApp | O interruptor "Receber mensagens pelo WhatsApp" libera avisos de OS, cobranças e vencimentos | 3.4.1 |
| Captação pública | `lead_capture_forms` cria clientes com origem `public_form` | 3.10 |

---

## 9. Validação de CPF e CNPJ

### 9.1 Resposta direta

**Não.** Nas telas de Clientes, Fornecedores e Equipamentos o **dígito verificador de CPF e de CNPJ não é conferido**, nem antes da consulta nem ao salvar. O que existe é só a máscara e, para CNPJ, a consulta na Receita (via BrasilAPI).

### 9.2 O que acontece em cada lugar

| Onde | Máscara | Consulta externa | Confere o dígito? | Evidência |
|---|---|---|---|---|
| Cliente → aba Fiscal → **CPF/CNPJ** | `cpfCnpjMask` (11 dígitos = CPF, 12 a 14 = CNPJ) | BrasilAPI, **só com exatamente 14 dígitos**: sozinha ao completar o 14º dígito e pela lupa | **Não** | `components/customers/CnpjDocumentInput.tsx:67-75,147-162` |
| Cliente rápido (botão "+" do equipamento) | idem | idem | **Não**. Só exige o campo preenchido quando `requireDocument` é verdadeiro, o que só acontece no Financeiro/NFS-e; no equipamento e na OS é falso | `components/financial/QuickCustomerDialog.tsx:89-93`, `EquipmentFormDialog.tsx:339`, `ServiceOrderFormDialog.tsx:1950` |
| Fornecedor → **CPF/CNPJ** | nenhuma | nenhuma | **Não** (texto livre) | `components/inventory/SupplierFormDialog.tsx` |
| Formulário público, no navegador | máscara | nenhuma | **Não** | `pages/PublicLeadCapture.tsx` |
| Formulário público, **no servidor** | — | — | **Sim**: "Pessoa jurídica" confere o CNPJ; qualquer outro caso confere como CPF. Erro **"CNPJ inválido"** ou **"CPF inválido"** | `supabase/migrations/20261015233000_lead_capture_insert_dinamico_respeita_default.sql:204-209` (`lead_valida_cnpj`, `lead_valida_cpf`) |
| **Cobrança** (Financeiro) de um cliente já cadastrado | — | — | **Sim**, na hora de cobrar: `getDocumentStatus` devolve "ok", "missing" ou "invalid" | `lib/documentValidation.ts:17-75`, `components/financial/ChargeDialog.tsx:432-444`, `ContaFormDialog.tsx:251-262`, `TransactionFormDialog.tsx:1197-1205` |

Outros usos do mesmo algoritmo, fora do escopo: cadastro de funcionário (`isValidCnpj`, `utils/cnpjValidation.ts:25`) e checkout da assinatura da própria Dominex (`components/checkout/CheckoutLayout.tsx:173-203`).

### 9.3 Consequências para a demonstração e para o roteiro

- Digitar um **CNPJ com dígito errado ou inexistente** não é barrado: a consulta dispara do mesmo jeito e a BrasilAPI responde "não encontrado", então aparece o aviso vermelho **"CNPJ não encontrado na Receita"**. O cadastro continua possível; o documento errado é gravado.
- Digitar um **CPF** (11 dígitos) não dispara nenhuma consulta, não valida e não preenche nada. "111.111.111-11" é aceito e gravado com máscara.
- A consulta usa `fetch` direto do navegador para `https://brasilapi.com.br/api/cnpj/v1/<14 dígitos>`: **precisa de internet**. Resposta não OK ou com o campo `message` = "CNPJ não encontrado na Receita"; exceção de rede = "Não foi possível consultar o CNPJ agora"; sucesso = "Dados da empresa preenchidos!" (`CnpjDocumentInput.tsx:78-146`).
- Digitar de novo o mesmo CNPJ não repete a consulta (`lastQueriedRef`); a lupa repete sempre. Se a primeira falhar por rede, o mesmo número só é tentado de novo pela lupa.
- Não há trava de duplicidade: nenhuma tabela tem índice único em `customers.document` nem em `suppliers.cpf_cnpj`.
- **Onde o erro aparece**: ao tentar **cobrar** um cliente sem documento ou com documento inválido, o Financeiro avisa "{nome} ainda não tem CPF ou CNPJ no cadastro. A Asaas exige esse dado para gerar a cobrança." ou "O CPF ou CNPJ de {nome} está incorreto. Corrija o cadastro para gerar a cobrança." (`lib/i18n/messages/app/charges.ts:335-340`, com o botão "Completar cadastro"), e no lançamento com cobrança online: "Cadastre o CPF/CNPJ do cliente antes de gerar as cobranças." / "O CPF/CNPJ do cliente é inválido. Corrija o cadastro antes de continuar." (`lib/i18n/messages/app/finance.ts:860-861`). Quem cria o cliente rápido dentro do Financeiro vê "Informe o CPF ou CNPJ do cliente para cobrar." (`charges.ts:252`).
- Sugestão de fala: dizer que o sistema **preenche** os dados a partir do CNPJ, mas que quem confere se o documento é válido é a hora de cobrar. Não prometer que o cadastro recusa CPF errado.

---

## 10. Diferenças no celular (uma linha por tela)

- **Clientes**: lista em `MobileListToolbar` (busca tolerante, Lista/Grade, "Origens", "Formulários", filtro "Atende como" com PDV), botão flutuante "Cliente", 10 por página; deslizar a linha para a esquerda mostra Editar e Excluir (seção 3.3).
- **Novo/Editar Cliente**: vira gaveta de baixo com "Fechar" no canto e rodapé fixo; as três abas continuam; na aba Portal os seletores de 3 estados se empilham (3.4, 3.4.3).
- **Ficha do cliente**: ocupa a tela toda; abas roláveis; botões de criar viram botão flutuante; tabelas viram listas de cartões; "Editar" e "Excluir" ficam no menu "Ações" (4.13).
- **Fornecedores**: lista simples com menu "Ver ficha / Editar / Excluir"; ficha em janela com "Fechar"; botão largo "Fornecedor" na barra (5.3, 5.4).
- **Lista de Equipamentos**: busca, Lista/Grade, "Filtros" em gaveta, botão "Campos", carrossel de categorias; criar é o botão flutuante "Equipamento"; a **Grade não tem Editar nem Excluir** no celular (6.2).
- **Novo Equipamento**: gaveta com duas colunas só a partir de `sm` (640 px); em tela estreita os campos empilham (6.3).
- **Configurar Campos**: em vez da tabela, cada campo é uma linha com menu (Tipo e opções, Mover para cima/baixo, Ocultar, Tornar obrigatório, Excluir); não há arrastar (6.5).
- **Ficha do equipamento**: tela cheia, abas roláveis, menu "Ações"; em Anexos os ícones de baixar e excluir da Galeria só aparecem ao passar o mouse, então no celular use a Lista (6.7).
- **Etiqueta**: gaveta; "Imprimir" abre outra aba e depende do navegador do aparelho permitir janelas e impressão (a confirmar) (6.8).
- **Formulário público de captação**: mesma página; o botão de foto abre a câmera (3.10.3).

---

## 11. Casos de uso de ar-condicionado, com o caminho dos cliques

Nomes de clientes são fictícios e servem de exemplo. Todo rótulo entre aspas está como aparece na tela. Computador, janela com 1024 px ou mais, usuário administrador (vê tudo).

### 11.1 Cliente pessoa jurídica pelo CNPJ (exemplo: Clínica Vida Plena)

**Antes**: internet ligada (a consulta vai à BrasilAPI) e um CNPJ real de uma empresa que possa aparecer no vídeo. Sem internet, a consulta mostra "Não foi possível consultar o CNPJ agora".

1. Menu lateral, grupo **Gestão**, **Clientes e Fornecedores**. Abre a aba **Clientes**.
2. No canto superior direito, **Novo Cliente**. Abre a janela **Novo Cliente**, na aba **Contato**.
3. Clique na aba **Fiscal**.
4. No campo **CPF/CNPJ**, digite ou cole os 14 números. A máscara 00.000.000/0000-00 aparece sozinha. Ao completar o 14º dígito a lupa gira e surge o aviso **"Dados da empresa preenchidos!"**.
5. Confira o que veio: **Razão Social**, **Nome Fantasia**, **E-mail fiscal**, **CEP**, **Logradouro**, **Número**, **Complemento**, **Bairro** e **UF / Cidade**.
6. Volte à aba **Contato**. O campo **Nome** já recebeu o nome fantasia (ou a razão social) e o **Telefone** pode ter vindo da Receita. O **Tipo** já está em "Pessoa Jurídica".
7. Digite o **Celular** do responsável. Ao completar 10 dígitos o interruptor **Receber mensagens pelo WhatsApp** libera, mas, se o número foi digitado tecla a tecla, ele fica **desligado**: clique para ligar (colando o número inteiro de uma vez, ele continua ligado). Em **Origem**, escolha uma opção (por exemplo "Indicação"; se a lista estiver vazia, veja 11.7).
8. **Criar**. Aviso **"Cliente criado com sucesso!"**, a janela fecha e o cliente aparece na lista, em ordem alfabética.
9. Clique na linha: a ficha abre à direita, aba **Geral**, com o cartão **"Informações"** (CPF/CNPJ, e-mail, telefone), o cartão **"Endereço"** com mapa e os botões **"Abrir no Google Maps"** e **"Abrir no Waze"**.

Cuidados: o cadastro **não abre** a ficha sozinho; o endereço mora na aba **Fiscal**; CNPJ inexistente ou com dígito errado mostra **"CNPJ não encontrado na Receita"** mas **não impede** salvar (seção 9).

### 11.2 Cliente pessoa física com CEP (exemplo: Marcos Antônio Braga)

1. **Gestão**, **Clientes e Fornecedores**, **Novo Cliente**.
2. Aba **Contato**: **Nome \*** "Marcos Antônio Braga"; **Tipo** muda para **Pessoa Física**; **Celular**; **Email**; **Origem**.
3. Aba **Fiscal**: em **CPF/CNPJ** digite os 11 números (máscara de CPF; não consulta nem valida nada). Deixe **Razão Social** em branco.
4. Em **Endereço fiscal**, no **CEP** digite os 8 números (ou clique na lupa). Aviso **"Endereço encontrado!"**: preenche **Logradouro**, **Bairro** e **UF / Cidade**. Depois digite **Número** e **Complemento**, que o CEP não traz.
   - Alternativa: digitar o **Logradouro** (a partir de 4 letras aparecem sugestões) e escolher uma; isso preenche Número, Bairro, Cidade, UF e CEP.
5. **Criar**. Ao salvar o app procura as coordenadas do endereço para o mapa da ficha, sem travar se não achar.

Cuidados: a busca de CEP só dispara com 8 dígitos; o cadastro funciona mesmo sem endereço.

### 11.3 Responsável no local com WhatsApp direto (exemplo: Seu Antônio, zelador do Condomínio Aurora)

1. Em **Clientes**, clique no cliente (por exemplo "Condomínio Edifício Aurora"). A ficha abre na aba **Geral**.
2. No cartão **"Responsável no Local (falar com)"**, clique **Adicionar**.
3. Janela **Novo Contato**: **Nome \*** "Antônio Ferreira", **Cargo** "Zelador", **Telefone** "(11) 91234-5678" e, se houver, **Email corporativo**. Clique **Adicionar**. Não aparece aviso: a janela fecha e o contato entra na lista com nome, cargo, telefone e e-mail.
4. Na linha do contato abra o menu de três pontos e escolha **WhatsApp**: abre uma nova aba em `wa.me/55<número>`.
5. Para o WhatsApp do próprio cliente use o ícone verde ao lado de **Telefone** ou **Celular** no cartão "Informações".

Cuidados: o app sempre põe "55" na frente e não confere o tamanho do número; **clicar fora da janela "Novo Contato" a fecha** e perde o que foi digitado; o menu **WhatsApp** só aparece se o contato tem telefone.

### 11.4 Cliente que se cadastra sozinho pelo formulário de captação (exemplo: Padaria Bom Grão)

1. Em **Clientes**, botão **Formulários de captação**. Abre a janela do mesmo nome (lista vazia: **"Nenhum formulário ainda"**).
2. No rodapé, **Novo formulário**. Aba **Geral**: **Título** "Cadastro de novos clientes" e, se quiser, **Descrição (opcional)**.
3. Aba **Campos**: ligue **Exibir** e **Obrigatório** em **Nome** e **Celular**; ligue **Exibir** em **Endereço**, **CEP**, **Número**, **Cidade**, **Estado (UF)** e **Foto**, por exemplo.
4. Aba **LGPD**: deixe **Exigir consentimento** ligado e, se quiser, ajuste o **Texto do consentimento**.
5. **Salvar**. Aviso **"Formulário criado com sucesso!"**. O formulário aparece na lista como **Ativo**, com "0 cadastro(s)".
6. Clique **Copiar link**: aviso **"Link gerado e copiado!"**. O endereço é `https://<site>/cadastro/cadastro-de-novos-clientes-<código de 12 letras e números>`.
7. Abra o link numa aba anônima ou no celular, sem login. Preencha, marque a caixa do consentimento e clique **Enviar cadastro**. Tela de sucesso: **"Cadastro enviado com sucesso"** / "Recebemos seus dados. Em breve entraremos em contato."
8. De volta ao Dominex, em **Clientes** (a lista se atualiza ao voltar para a aba; se não, recarregue): o cliente já está na lista, sem fila de aprovação. Na ficha, **Origem** mostra o texto "public_form" e o CPF e o telefone aparecem só com números. O formulário agora mostra "1 cadastro(s)".

Cuidados: o servidor aceita 5 envios por formulário e por IP em 10 minutos ("Muitas tentativas. Tente novamente mais tarde."); CPF/CNPJ inválido é recusado só pelo servidor (**"CPF inválido"** / **"CNPJ inválido"**); tire a foto só se o campo **Foto** estiver ligado.

### 11.5 Fornecedor (exemplo: Frigelar Distribuidora, gás e tubos)

1. **Gestão**, **Clientes e Fornecedores**, aba **Fornecedores** (ícone de caminhão). Os botões do cabeçalho de clientes somem.
2. No topo do painel da direita, clique **Novo Fornecedor** (no celular, o botão **Fornecedor**).
3. Janela **Novo Fornecedor**: **Nome \*** "Frigelar Distribuidora"; **CPF/CNPJ**; **Contato** "Rodrigo (vendas)"; **Telefone**; **E-mail**; **Endereço**; **Observações** "Gás R-410A e tubo de cobre". Clique **Salvar**. Aviso **"Fornecedor cadastrado!"**.
4. Clique no fornecedor na lista: a ficha mostra **"Dados do fornecedor"** (ícones, sem rótulos escritos) e **"Histórico de Gastos"** ("Nenhum gasto registrado" enquanto não houver despesa ligada a ele).
5. Para o histórico encher: no Financeiro, lançar uma despesa escolhendo este fornecedor (assunto de outro tutorial).

Cuidados: fornecedor não tem busca de CNPJ, máscara nem rota própria; quem vê a aba cria, edita e exclui.

### 11.6 Equipamento com campo personalizado e etiqueta com QR Code (exemplo: Split Hi-Wall da Clínica Vida Plena)

**Antes**: o cliente existe (ou será criado no passo 4) e está com o portal ativo, que é o padrão.

1. **Gestão**, **Equipamentos**, botão **Configurar Campos**. Abre **"Configurar Campos do Equipamento"**.
2. No bloco **Adicionar novo campo**: **Nome do campo** "Tensão", tipo **Lista de opções**, e em **Opções da lista** preencha "127 V", "220 V" e "380 V" (**Adicionar opção** abre uma nova caixa). Clique em **Adicionar campo** (nos outros tipos o botão é só um sinal de mais). Aviso **"Campo criado!"**; o campo entra no fim da lista. Crie **a lista inteira de uma vez** (seção 6.5, pontos de atenção).
3. Opcional: ligue **Obrig.** em "Tensão", arraste a alça para mudar a ordem, desligue **Visível** de algum campo padrão. Cada clique grava sozinho (aparece "Salvo"). Termine com **Fechar**.
4. Aba **Categorias**, **Nova Categoria**: nome "Split Hi-Wall", escolha a cor, **Criar**. Aviso **"Categoria criada com sucesso!"**.
5. Aba **Equipamentos**, **Novo Equipamento**:
   - **Foto** (opcional);
   - **Cliente \***: escolha na lista. Se o cliente não existe, digite o nome na busca, clique no **"+"** ao lado, confira o **Nome**, e clique **Criar cliente** (aviso "Cliente criado com sucesso!"); ele já fica escolhido;
   - **Nome \*** "Split Sala de Espera"; **Categoria** "Split Hi-Wall"; **Marca**; **Modelo**; **Nº de Série**; **Capacidade/Especificação** "12.000 BTUs"; **Local** "Sala de espera"; **Data de Instalação**; **Tensão** "220 V"; **Validade da Garantia**; **Observações**.
   - **Criar**. Aviso **"Equipamento criado com sucesso!"**. O identificador ("0001") é gerado pelo banco.
6. Clique no equipamento na lista: ficha, aba **Geral**, com o QR Code e os botões **Gerar Etiqueta**, **Baixar QR (PNG)**, **Abrir link** e **Copiar link**.
7. **Gerar Etiqueta**: janela **"Gerar Etiqueta de Identificação"**. Em **Itens da etiqueta** deixe marcados "Nome da empresa", "Telefone da empresa", "E-mail da empresa", "QR Code", "Nome do equipamento" e "Identificador" (já vêm marcados) e, se quiser, Marca, Modelo, Nº de série, Localização e Nome do cliente. Em **Tamanho** escolha **5×8 cm**. Confira a **Pré-visualização** e clique **Imprimir**: abre outra aba e a impressão do navegador. Na caixa de impressão, deixe o dimensionamento em tamanho real.
8. Mostre também **Baixar QR (PNG)** (aviso "QR Code salvo!"), **Copiar link** ("Link copiado!") e **Abrir link**, que leva ao portal do cliente já no aparelho.

Cuidados: sem portal ativo o QR vira `EQ-0001`, os botões de link ficam desligados e a etiqueta não oferece o item QR Code; os itens Marca, Modelo, Nº de série e Localização só aparecem na etiqueta se estiverem preenchidos; se o navegador bloquear janelas, "Imprimir" não faz nada e não avisa; a pré-visualização não mostra os rótulos que a impressão mostra.

### 11.7 Atalhos e variações

- **Criar as origens de uma vez**: **Clientes**, **Configurar origens**, **Criar origens padrão** ("Origens padrão criadas!"). Ou **Configurações**, aba **Usabilidade**, cartão **Origens**.
- **Origem nova na hora**: no formulário do cliente, ao lado de **Origem**, o botão **"+"** abre **Nova origem** (Nome, Ícone, Cor, **Criar origem**).
- **Equipamento pela ficha do cliente**: ficha, aba **Equipamentos**, **Novo Equipamento**. O cliente já vem escolhido e travado.
- **Trocar de cliente ou de equipamento sem voltar à lista**: clique no nome, na ficha, e use a busca "Buscar cliente..." ou "Buscar equipamento...".
- **Voltar de um equipamento para o cliente**: se a ficha foi aberta pela aba Equipamentos do cliente, a seta de voltar retorna a essa aba.

---

## 12. Chamadas ao backend por tela

Para quem monta o backend falso de escrita. Tudo o que estas telas pedem ao servidor passa pelo `@supabase/supabase-js` (`package.json:56`, versão `^2.93.3`). O cliente nasce em `integrations/supabase/client.ts` com `VITE_SUPABASE_URL` e `VITE_SUPABASE_PUBLISHABLE_KEY` e guarda a sessão no `localStorage`. As páginas públicas (formulário de captação e portal) usam um segundo cliente, sem sessão, o `supabaseAnon` (`integrations/supabase/anonClient.ts`). Na prática o backend falso precisa atender estas rotas: `/rest/v1/<tabela>` (PostgREST), `/rest/v1/rpc/<função>`, `/functions/v1/<função>`, `/storage/v1/object/...` e `/auth/v1/...`, mais quatro serviços da internet (12.7). Nomes de tabela, coluna e filtro foram lidos do código. O que só se confirma rodando está marcado "(a confirmar)".

### 12.0 Regras gerais (valem para todas as telas)

1. **Como o supabase-js vira HTTP** (comportamento padrão da biblioteca). `select` é `GET` com `select=colunas`. `insert` é `POST` e, com `.select()` no fim, pede de volta a linha criada (`Prefer: return=representation`). `update` é `PATCH ...?id=eq.<id>`. `delete` é `DELETE ...?id=eq.<id>`. `.eq(c, v)` vira `c=eq.v`. `.order(c)` vira `order=c.asc` (`c.desc` quando descendente). `.range(a, b)` vira `offset=a&limit=b-a+1`. `.single()` exige exatamente uma linha: com zero ou mais de uma o servidor devolve erro `PGRST116`, que o app mostra como "Registro não encontrado.". `.maybeSingle()` aceita zero linhas e devolve `null`. Um embed como `customer:customers(id, name)` devolve, em cada linha, um objeto `customer` só com essas colunas (ou `null` se não houver).
2. **Tudo o que for gravado tem que ser relido.** Depois de cada gravação o app invalida a consulta da lista e lê de novo. O TanStack Query também relê ao voltar o foco para a janela (`new QueryClient()` sem opções, `App.tsx:246`: relê ao focar e trata todo dado como velho desde o instante zero). Se o `GET` não devolver o registro recém-criado, ele some da tela. O backend falso precisa guardar o que foi gravado (em memória basta) e responder leituras repetidas sempre igual.
3. **Páginas de 1000 linhas.** Clientes, equipamentos e lançamentos financeiros são lidos por `fetchAllPaginated` (`utils/supabasePagination.ts:12-27`): pede `offset=0&limit=1000`, depois `offset=1000&limit=1000` e assim por diante, parando na primeira resposta com menos de 1000 linhas. As OS usam um laço igual escrito à mão (`hooks/useServiceOrders.ts:196-217`). Se o backend ignorar `limit` e devolver tudo, só funciona com menos de 1000 linhas.
4. **Empresa do usuário antes de gravar.** Quase toda criação começa por `getCurrentUserCompanyId()` (`hooks/useUserCompany.ts:35-52`): `auth.getUser()` (vai à rede, `GET /auth/v1/user`) e depois `GET profiles?select=company_id&user_id=eq.<id>` com `.maybeSingle()`. Sem usuário: erro "Usuário não autenticado". Perfil sem empresa: "Usuário sem empresa associada. Contate o administrador.". Fornecedores usam outro caminho: `profile.company_id` do contexto de login, sem chamada extra (`hooks/useSuppliers.ts:26-27,44`).
5. **Quem manda `company_id` no corpo do insert.**

   | Manda `company_id` | Não manda (o servidor preenche, gatilho genérico `set_company_id_on_insert`) | Tabela sem `company_id` |
   |---|---|---|
   | `customers`, `equipment`, `equipment_categories`, `equipment_field_config`, `lead_capture_forms` (mais `created_by`), `suppliers` (mais `created_by`), `customer_documents`, e o lote de "Criar origens padrão" | `customer_origins`, ao criar uma origem avulsa (`hooks/useCustomerOrigins.ts:70-73`) | `customer_contacts`, `equipment_attachments`, `equipment_tasks`, `customer_portals` |

   Um backend falso de usuário único pode simplesmente carimbar o `company_id` da empresa de demonstração em tudo.
6. **Formato do erro.** Toda gravação faz `if (error) throw error` e o toast usa `getErrorMessage(error)` (seção 7.6). O erro precisa ter a forma do PostgREST: HTTP 4xx com corpo `{ "code": "...", "message": "...", "details": ..., "hint": ... }`. O que o app faz com ele, em ordem (`utils/errorMessages.ts:357-422`): `code` conhecido (23505, 23503, 42501...) vence; sem `code` conhecido, procura trechos na `message`; sem nada reconhecível e com cara de erro técnico em inglês, mostra "Ocorreu um erro inesperado. Tente novamente.". **Decisão para o backend falso** (referência da seção 6.10): o comportamento real do banco é `code: "23503"`, que mostra o texto genérico "Não é possível concluir porque há referências relacionadas. Remova-as primeiro.". Para mostrar o texto específico do equipamento ("Este equipamento não pode ser excluído porque está vinculado a ordens de serviço, contratos ou planos PMOC.", `errorMessages.ts:129-132`) o erro tem que chegar **sem um `code` conhecido** e com a `message` contendo `violates foreign key constraint` e `_equipment_id_fkey` (por exemplo `... violates foreign key constraint "contract_items_equipment_id_fkey" ...`; o nome exato da restrição é a confirmar no banco real).
7. **Funções de servidor (`functions.invoke`).** Resposta 2xx vira `data`. Qualquer outro status vira `error`, e o app lê o motivo do corpo `{ "error": "texto em português" }` (`getInvokeErrorMessage`, `utils/errorMessages.ts:324-343`; a página pública lê do mesmo jeito, `pages/PublicLeadCapture.tsx:345-356,432-440`).
8. **Tentativas e tempo até o painel de erro.** As listas de clientes e de equipamentos tentam de novo até 3 vezes, esperando 1 s, 2 s e 4 s (`retry: 3` e `retryDelay`, `hooks/useCustomers.ts:62-63`, `hooks/useEquipment.ts:51-52`): o painel de erro com "Tentar novamente" só aparece uns 7 s depois da primeira falha. Formulários de captação usam `retry: 2` (`hooks/useLeadCaptureForms.ts:77`). As demais consultas usam o padrão do TanStack Query (3 tentativas). A leitura de perfil, papéis e permissões no login tem teto de 5 s (`contexts/AuthContext.tsx:180-183,269-272`); passou disso, o app segue com o que já chegou.
9. **Nem toda gravação passa por um hook.** Editar e excluir equipamento a partir do painel da lista, da ficha do equipamento e da ficha do cliente chamam `supabase.from('equipment')` direto (`components/customers/EquipmentPanel.tsx:203,218`; `pages/EquipmentDetail.tsx:1197,1218`; `pages/CustomerDetail.tsx:273,1858`). Mesma tabela e mesmos formatos; muda só o aviso (seção 6.10).

### 12.1 Clientes (`/clientes`, aba "Clientes"; `pages/Customers.tsx`, `components/customers/CustomersPageChrome.tsx`)

**Ao abrir a página** (computador e celular):

| Chamada | Detalhe |
|---|---|
| `GET customers` | `select=*`, `is_deleted=eq.false`, `order=name.asc`, em páginas de 1000 (`hooks/useCustomers.ts:50-63`). Chave `['customers', <id do usuário>]`. Só começa depois que o login terminou (`enabled: !loading`). |
| `GET customer_origins` | `select=*`, `order=name.asc` (`hooks/useCustomerOrigins.ts:56-61`). Dispara mesmo sem abrir a janela, porque `CustomerOriginManagerDialog` fica montado na página (`CustomersPageChrome.tsx:99`; no celular `pages/Customers.tsx:888`) e o hook não tem `enabled` (deduzido do código; confirmar no Network). |
| `GET lead_capture_forms` | `select=*`, `order=created_at.desc`, só com usuário logado (`hooks/useLeadCaptureForms.ts:67-77`). Mesmo motivo: `LeadCaptureManagerDialog` fica montado (`CustomersPageChrome.tsx:101`). |
| Consultas do cabeçalho do app | Seção 12.10. |

Busca, ordenação, filtro "Atende como", paginação e modo lista/grade são todos locais: nenhuma chamada (ficam em `sessionStorage` e `localStorage`, seções 3.2 e 7.2).

**Novo Cliente, botão "Criar"** (`components/customers/CustomerFormDialog.tsx:245-330`), nesta ordem:

1. Se escolheu foto: `POST /storage/v1/object/customer-photos/<Date.now()>.<extensão>` (caminho plano, sem pasta) e, em seguida, o endereço público é montado no navegador: `<VITE_SUPABASE_URL>/storage/v1/object/public/customer-photos/<caminho>` (`:235-243`). O envio leva o metadado `company_id` (`utils/tenantStorage.ts:64-72`); o backend falso pode aceitar qualquer valor.
2. Se não escolheu um endereço nas sugestões e há endereço digitado: `GET https://nominatim.openstreetmap.org/search?format=json&limit=1&q=<endereço>` (`utils/geolocation.ts:125-139`). Qualquer falha vira "sem coordenadas" e nunca bloqueia o cadastro.
3. `GET /auth/v1/user` e `GET profiles` (empresa, regra 4 de 12.0).
4. `POST customers` pedindo de volta um objeto só (`hooks/useCustomers.ts:66-84`). **A resposta precisa trazer o `id`**: sem ele o formulário mostra "O cliente foi salvo, mas o identificador não retornou para configurar o portal." (`CustomerFormDialog.tsx:303-309`). Corpo: `name`, `customer_type` (`"pf"` ou `"pj"`, padrão `"pj"`), `company_name`, `nome_fantasia`, `document` (com máscara), `email`, `phone`, `celular`, `address`, `address_number`, `street_number` (cópia do número), `complement`, `neighborhood`, `city`, `state`, `zip_code` (com máscara), `ibge_municipality_code`, `inscricao_municipal`, `inscricao_estadual`, `birth_date` (`yyyy-MM-dd`; a chave nem vai quando está vazia), `notes`, `origin` (o **nome** da origem), `whatsapp_notifications_enabled`, `latitude` e `longitude` (só se achou), `photo_url` (só se subiu foto), `is_service_customer` e `is_store_customer` (**só com o módulo PDV**) e `company_id`. Campos de texto vazios seguem como `""`: o formulário de cliente não converte vazio em `null` (o de equipamento converte).
5. `POST /rest/v1/rpc/save_customer_portal_settings` (`:313`), **sempre**, até para cliente novo, logo depois do insert, com o `id` recém-criado. Corpo e resposta em 12.7.
6. O app relê `customers` e mostra o toast "Cliente criado com sucesso!".

**Editar** (ação "Editar" da lista no celular, botão "Editar" da ficha): ao abrir, `POST /rest/v1/rpc/get_customer_portal_settings` com `{ p_customer_id }` (`hooks/useCustomerPortalSettings.ts:107-113`; só com cliente existente, `CustomerFormDialog.tsx:141-144`). **Se essa chamada falhar, o botão "Salvar" fica desligado** (`:336`) e a aba Portal mostra "Não foi possível carregar as configurações do portal." com "Tentar novamente"; durante as tentativas automáticas ele também fica desligado. Ao salvar: `PATCH customers?id=eq.<id>` pedindo o objeto de volta (`hooks/useCustomers.ts:88-106`), depois a RPC de salvar o portal, toast "Cliente atualizado com sucesso!".

**Excluir:** `PATCH customers?id=eq.<id>` com `{ "is_deleted": true, "deleted_at": "<ISO>" }` (`hooks/useCustomers.ts:109-125`) e toast "Cliente excluído com sucesso!". O cliente some da lista só porque a leitura filtra `is_deleted=eq.false`. Nenhuma outra tabela é tocada.

**Ajudantes de preenchimento dentro do formulário** (formatos em 12.7): CPF/CNPJ com 14 dígitos consulta a BrasilAPI direto do navegador (`components/customers/CnpjDocumentInput.tsx:78`); CEP com 8 dígitos chama `POST /functions/v1/cep-lookup` (`components/CepLookup.tsx:34`); Logradouro (4 caracteres ou mais, 500 ms depois da última tecla) consulta o Nominatim (`components/AddressAutocomplete.tsx:85-92`); escolher a UF carrega as cidades do IBGE (`components/StateCitySelector.tsx:82-84`, com cache em memória por UF).

**Criação rápida de cliente** (botão "+" do campo "Cliente \*" em Equipamento, OS, Contrato etc.; `components/financial/QuickCustomerDialog.tsx:89-116`): o mesmo `POST customers`, com corpo mínimo: `name`, `customer_type` (`"pj"` se o documento digitado tem 14 dígitos, senão `"pf"`), `document` (como digitado, com máscara), `email`, `celular` e, só com PDV, `is_service_customer` e `is_store_customer`. **Não chama a RPC do portal**: o portal nasce pelo gatilho do banco (seção 13.1). Toast do hook "Cliente criado com sucesso!"; a janela devolve o `id` ao formulário que a abriu.

### 12.2 Ficha do cliente (`/clientes/<nome>-<código>`; `pages/CustomerDetail.tsx`)

A ficha **carrega tudo de uma vez** ao abrir, inclusive o que as abas fechadas vão mostrar (as listas de OS, contratos e lançamentos são lidas inteiras e filtradas no navegador pelo cliente). Para o backend falso: estas leituras precisam responder, mesmo com lista vazia, ou as abas ficam carregando ou mostram erro.

| Chamada | Para quê | Detalhe |
|---|---|---|
| `GET customers` | O cliente da ficha | A lista de 12.1. O cliente é achado nela pelo `id` (UUID) ou pelo `public_short_code` (código no fim da URL), `pages/CustomerDetail.tsx:170-183`. **Linhas sem `public_short_code` só abrem pelo UUID.** |
| `GET service_orders` | Abas Histórico, Tarefas e Chamados | Todas as OS da empresa: `select=*` com os embeds `customer:customers(id, name, phone, celular, email, document, address, address_number, complement, neighborhood, city, state, zip_code, company_name, customer_type)`, `equipment:equipment(id, name, brand, model)`, `form_template:form_templates(id, name)`, `service_type:service_types!service_orders_service_type_id_fkey(id, name, color, number_prefix)` e `contract:contracts(id, name, is_pmoc)`; `order=created_at.desc`; laço de 1000 em 1000 (`hooks/useServiceOrders.ts:196-217`). Depois, `GET service_order_assignees?select=service_order_id,user_id` em lotes de 200 ids e `GET profiles?select=user_id,full_name,avatar_url,email` para os nomes (`:226-264`). A ficha separa no navegador (`CustomerDetail.tsx:312-313,603`): **Histórico** = `customer_id` igual ao cliente e `entry_type` diferente de `tarefa`; **Tarefas** = `entry_type = 'tarefa'`; **Chamados** = o Histórico com `origin = 'portal'`. |
| `GET financial_transactions` | Aba Financeiro | Todos os lançamentos com os embeds `customer:customers(id, name, document)`, `supplier:suppliers(id, name, cpf_cnpj)`, `account:financial_accounts(id, name, type, color)` e `employee:employees(id, name, salary, photo_url)`; `order=transaction_date.desc`; mais `GET profiles` (nomes) e a leitura do resumo financeiro (`hooks/useFinancial.ts`). |
| `GET contracts` | Aba Contratos | Todos os contratos com os embeds `customers(...)`, `customer:customers(id, name)`, `responsible_technicians:responsible_technician_id(...)`, `contract_items(... equipment:equipment(id, name, brand, model))`, `contract_environments(...)` e `service_orders(id, order_number, status, scheduled_date, origin)`; `order=created_at.desc`; sem laço de páginas (`hooks/useContracts.ts`). |
| `GET equipment` | Aba Equipamentos | `select=*,customer:customers(id, name)`, `customer_id=eq.<id>`, `order=name.asc` (12.5). |
| `GET equipment_categories` | Nome e cor da categoria | 12.5. |
| `GET customer_contacts` | Card "Responsável no Local (falar com)" | `select=*`, `customer_id=eq.<id>`, `order=created_at.asc` (`hooks/useCustomerContacts.ts:20-31`). |
| `GET customer_origins` | Ícone e cor da origem | 12.3. |
| `GET customer_portals` | "Link do portal" | `select=token`, `customer_id=eq.<id>`, `is_active=eq.true`, `limit=1`, `.maybeSingle()` (`CustomerDetail.tsx:640-655`). O link é `<endereço do site>/portal/<token>`. Sem linha, o link não aparece. |
| `GET customer_paid_expenses` | Despesas pagas pelo cliente | `customer_id=eq.<id>`, `order=expense_date.desc,created_at.desc`. |
| `GET tenant_payment_accounts`, `GET tenant_charges` | Aba Cobranças | `company_id=eq.<empresa>` (e `customer_id=eq.<id>` nas cobranças). Só importam com o módulo de cobranças ligado. |

**Aba Estoque** (`hooks/useCustomerStockManagement.ts:52-185`): `GET stocks?select=id,name,customer_id&customer_id=eq.<id>` com `.maybeSingle()`. Sem linha, devolve listas vazias e a aba mostra "Nenhum material no estoque do cliente". Com linha, lê `inventory` (`customer_id=eq.<id>`, `order=name.asc`), `inventory_stock_levels` (`stock_id=eq.<id do estoque>`) e `inventory_movements` (`customer_id=eq.<id>`, `order=created_at.desc`). As ações usam as RPCs `create_customer_stock_item` (`p_customer_id`, `p_name`, `p_sku`, `p_unit`, `p_initial_quantity`, `p_min_quantity`, `p_cost_price`, `p_notes`, `p_client_request_id`), `update_customer_stock_item`, `archive_customer_stock_item` (`p_inventory_id`) e `register_inventory_movement` (`p_inventory_id`, `p_movement_type`, `p_quantity` negativo na saída, `p_notes`, `p_stock_id`). Quem não for gravar essa aba pode devolver vazio.

**Aba Documentos** (`hooks/useCustomerDocuments.ts:49-140`): `GET customer_documents?select=*&customer_id=eq.<id>&order=created_at.desc`. Enviar arquivo: `POST /storage/v1/object/customer-documents/<empresa>/<cliente>/<uuid>_<nome-seguro>` (com `upsert: false` e o tipo do arquivo) e depois `POST customer_documents` com `company_id`, `customer_id`, `document_kind` (`invoice` ou `document`), `document_type` (`nfse`, `nfe_product`, `contract` ou `other`), `title`, `description`, `document_number`, `issue_date`, `amount`, `storage_path`, `file_name`, `mime_type`, `size_bytes` e `is_visible_in_portal`, pedindo o objeto de volta; se o insert falhar, o app apaga o arquivo recém-enviado. Mostrar ou ocultar no portal: `PATCH customer_documents?id=eq.<id>&customer_id=eq.<cliente>` com `{ is_visible_in_portal }`. Excluir: `DELETE customer_documents` com os mesmos dois filtros e depois remoção do arquivo do bucket. Abrir ou baixar: `createSignedUrl(caminho, 60, { download: nome })`, que na biblioteca padrão é `POST /storage/v1/object/sign/customer-documents/<caminho>` com `{ "expiresIn": 60 }` e resposta `{ "signedURL": "..." }`. Limites no navegador: 15 MB; arquivos gerais pdf, xml, txt, jpg, jpeg, png, webp, doc, docx, xls, xlsx; nota fiscal só pdf e xml.

**Ações da ficha:** editar e excluir cliente repetem 12.1. Contatos: `POST customer_contacts` com `{ customer_id, name, phone, email, position }` (chaves vazias nem vão), pedindo o objeto de volta (`hooks/useCustomerContacts.ts:34-45`); `PATCH customer_contacts?id=eq.<id>` com o que mudou mais `updated_at` (`:47-60`); `DELETE customer_contacts?id=eq.<id>` (`:62-67`). Nova OS, Nova Tarefa, Cobrar, Lançar despesa e Criar oportunidade no CRM abrem formulários de outros módulos, fora deste inventário.

### 12.3 Origens, formulários de captação e a página pública

**Origens** (Clientes → "Configurar origens", Configurações → Usabilidade → Origens, e o "+" do campo Origem; `hooks/useCustomerOrigins.ts`):

| Ação | Chamada |
|---|---|
| Listar | `GET customer_origins?select=*&order=name.asc` (`:56-61`). "Ativa" é `is_active` diferente de `false`, filtrado no navegador. |
| "Adicionar" / "Criar origem" | `POST customer_origins` com `{ name, icon, color }`, pedindo o objeto de volta, **sem** `company_id` (`:70-73`). O "+" do cadastro manda também o ícone e a cor escolhidos (padrões Globe e `#6B7280`). |
| "Criar origens padrão" | `POST customer_origins` com um **array de 10 linhas** (tabela da seção 3.9), cada uma com `company_id`, `name`, `icon` e `color`, pedindo as linhas de volta (`:98-100`). O botão só aparece com o catálogo vazio. |
| Editar nome, ícone, cor ou ativa | `PATCH customer_origins?id=eq.<id>` (`:114-116`). |
| Excluir (sem confirmação) | `DELETE customer_origins?id=eq.<id>` (`:129-131`). Os clientes continuam com o texto antigo em `customers.origin`. |

**Formulários de captação** (Clientes → "Formulários de captação"; `hooks/useLeadCaptureForms.ts`):

| Ação | Chamada |
|---|---|
| Listar | `GET lead_capture_forms?select=*&order=created_at.desc` (`:67-77`). |
| Criar | `GET /auth/v1/user` (para o `created_by`, `:84-86`) mais a empresa; `POST lead_capture_forms` com `{ title, description, field_config, is_active, expires_at, require_consent, consent_text, max_submissions, company_id, created_by }`, pedindo o objeto de volta (`:90-93`). **Sem `short_code`**: o servidor gera. `field_config` é um objeto `{ "<campo>": { "enabled": true, "required": false } }` com as 17 chaves da lista fixa (`LEAD_CAPTURE_FIELDS`, `:21-39`). Toast "Formulário criado com sucesso!". |
| Editar | `PATCH lead_capture_forms?id=eq.<id>` com os campos mais `updated_at`, objeto de volta (`:109-113`). |
| Ligar e desligar | `PATCH lead_capture_forms?id=eq.<id>` com `{ is_active, updated_at }` (`:129-131`). |
| Excluir | `DELETE lead_capture_forms?id=eq.<id>` (`:145`). |
| Copiar link | Sem chamada. O endereço é `<site>/cadastro/<nome>-<short_code>` (seção 1.1). |

**Página pública `/cadastro/<nome>-<código>`** (`pages/PublicLeadCapture.tsx`), sem login, com o cliente anônimo:

1. `POST /rest/v1/rpc/get_lead_capture_form` com `{ "p_short_code": "<código>" }` (`:247`). Resposta esperada: `{ "form": { "title", "description", "field_config", "require_consent", "consent_text", "is_active", "expired" }, "company_settings": { "white_label_enabled", "white_label_primary_color", "white_label_logo_url", "white_label_icon_url", "name", "logo_url", "language" } }` (tipos em `:18-46`). Erro ou resposta vazia mostra "Formulário não encontrado"; `is_active = false` ou `expired = true` mostra "Formulário indisponível" (`:466-482`).
2. Foto (campo opcional): `POST /functions/v1/lead-capture-upload-photo` com `{ "short_code", "photo_base64": "data:image/jpeg;base64,..." }` (`:342-345`). Resposta `{ "photo_url": "<endereço público>" }`. Erros `{ "error": "texto" }`: 405 "Método não permitido", 413 "Arquivo muito grande" (teto de 5 MB depois de decodificar), 400 "Requisição inválida", "Tipo de arquivo não suportado", "Formulário indisponível", 429 "Muitas tentativas. Tente novamente mais tarde." (20 por minuto por IP), 500 "Não foi possível enviar a foto. Tente novamente." (`supabase/functions/lead-capture-upload-photo/index.ts:31-40,45-62`). A foto vai para o bucket `customer-photos`, pasta `lead-capture/<short_code>/<uuid>.<jpg, png ou webp>`.
3. Envio: `POST /functions/v1/lead-capture-submit` com `{ "short_code", "fields": { "<campo>": "<texto>" }, "consent": true, "honeypot": "" }` (`:422-428`). Resposta de sucesso `{ "success": true }` (e é a mesma resposta, sem gravar nada, quando o campo escondido "website" vem preenchido). Erros `{ "error": "texto" }` com status 400 (validação), 413, 429 ou 500; o texto vem pronto da regra no banco (seção 13.1).

### 12.4 Fornecedores (aba "Fornecedores" de `/clientes`; `components/customers/SuppliersTab.tsx`, `hooks/useSuppliers.ts`)

| Quando | Chamada |
|---|---|
| Abrir a aba | `GET suppliers?select=*&order=name.asc` (`:30-35`), chave `['suppliers', <empresa>]`. A consulta nasce junto com o hook, antes de o perfil carregar (chave com empresa nula), e é refeita com a empresa certa; o servidor só devolve fornecedores da empresa do usuário. |
| "Novo Fornecedor", "Salvar" | `POST suppliers` com `{ name, cpf_cnpj, contact_name, phone, email, address, notes, company_id, created_by }`, pedindo o objeto de volta (`:45-56`). Campos vazios vão como `""` (`components/inventory/SupplierFormDialog.tsx:36-55`). Toast "Fornecedor cadastrado!". |
| Editar, "Salvar" | `PATCH suppliers?id=eq.<id>` com os campos do formulário, **sem** pedir o objeto de volta (`:66-82`). Toast "Fornecedor atualizado!". |
| Excluir, confirmação | `DELETE suppliers?id=eq.<id>` (`:84-98`). Toast "Fornecedor removido!". Consequências nas outras tabelas: seção 5.6. |
| Ficha do fornecedor (janela) | Reaproveita as leituras de lançamentos financeiros de 12.2 (`useFinancial`) e filtra pelo fornecedor no navegador (`components/customers/SupplierDetailDialog.tsx:43`). |

Se a gravação falhar, o hook mostra o toast vermelho e o formulário **fica aberto** (o fechamento só acontece depois do sucesso, `SupplierFormDialog.tsx:56-66`).

### 12.5 Equipamentos (lista, formulário, categorias e campos; `/equipamentos`)

**Ao abrir a página:**

| Chamada | Detalhe |
|---|---|
| `GET equipment` | `select=*,customer:customers(id, name)`, `order=name.asc`, sem filtro de cliente (na ficha do cliente leva `customer_id=eq.<id>`), em páginas de 1000. Chave `['equipment', <usuário>, <cliente ou nada>]`, `retry: 3` (`hooks/useEquipment.ts:33-52`). |
| `GET customers` | A lista de 12.1 (nomes na lista e no seletor "Cliente \*"). |
| `GET equipment_categories` | `select=*`, `order=name.asc` (`hooks/useEquipmentCategories.ts:19-26`). |
| `GET equipment_field_config` | Primeiro `GET /auth/v1/user` e `GET profiles` (empresa); depois `select=*`, `company_id=eq.<empresa>`, `order=position.asc` (`hooks/useEquipmentFieldConfig.ts:24-36`). Alimenta o formulário, "Configurar Campos" e a ficha. **Empresa sem nenhuma linha aqui abre o formulário sem Marca, Modelo, Nº de Série, Capacidade, Local e Data de Instalação** (era o defeito que a migração `20260906190100_seed_equipment_field_config_por_empresa.sql` corrigiu; seção 13.1). |

**Novo Equipamento, botão "Criar"** (`components/customers/EquipmentFormDialog.tsx:200-262`), nesta ordem:

1. Se escolheu foto: `POST /storage/v1/object/equipment-files/photos/<uuid>_<nome-seguro>` e URL pública montada no navegador (`:175-188`). Foto removida na edição vai como `photo_url: null`.
2. Empresa (regra 4 de 12.0).
3. `POST equipment` pedindo o objeto de volta (`hooks/useEquipment.ts:80-93`). Corpo: `customer_id`, `name`, `category_id`, `identifier` (**vem `null`**: o servidor gera "0001", "0002"...), `brand`, `model`, `serial_number`, `capacity`, `location`, `install_date` (`yyyy-MM-dd`), `warranty_until` (`yyyy-MM-dd`), `notes`, `photo_url`, `custom_fields` e `company_id`. **Todo texto vazio vai como `null`** (`EquipmentFormDialog.tsx:226-229`). `custom_fields` é um objeto `{ "<field_key>": "<texto>" }`, sempre com valores em texto (data `yyyy-MM-dd`, lista com a opção escolhida, Sim e Não como `sim` e `nao`); valores vazios são retirados e, se não sobrar nenhum, a chave `custom_fields` nem vai (por isso, na edição, **apagar o último valor personalizado não limpa nada**). Não há campo de `status` no formulário.
4. O app relê `equipment`; toast "Equipamento criado com sucesso!".

**Editar:** `PATCH equipment?id=eq.<id>` com o mesmo corpo, **direto do painel/ficha** (sem toast de erro na ficha; seção 6.10). Pelo hook (`useEquipment.updateEquipment`, `:56-79`) o objeto volta e o erro vira o toast "Erro ao atualizar equipamento". **Excluir:** `DELETE equipment?id=eq.<id>` (`EquipmentPanel.tsx:218`, `CustomerDetail.tsx:273`, `EquipmentDetail.tsx:1218`). Efeitos nas outras tabelas: seção 13.2.

**Categorias** (aba "Categorias", `pages/Equipment.tsx:36-196`; `hooks/useEquipmentCategories.ts`):

| Ação | Chamada |
|---|---|
| Criar | `POST equipment_categories` com `{ name, description, color, company_id }`, objeto de volta (`:32-36`). Toast "Categoria criada com sucesso!". |
| Editar | `PATCH equipment_categories?id=eq.<id>`, objeto de volta (`:48-51`). Toast "Categoria atualizada!". |
| Excluir | `DELETE equipment_categories?id=eq.<id>` (`:64-66`). Toast "Categoria excluída!". Os equipamentos dela ficam sem categoria (`category_id` volta a nulo no banco). |
| Contagem por categoria | Local (conta a lista de equipamentos). |

**Configurar Campos** (`components/customers/EquipmentFieldConfigDialog.tsx`; `hooks/useEquipmentFieldConfig.ts`):

| Ação | Chamada |
|---|---|
| Mostrar ou ocultar, obrigatório, renomear, tipo, opções | `PATCH equipment_field_config?id=eq.<id>`, objeto de volta (`:43`). **Sem toast de sucesso**; erro "Erro ao atualizar campo". |
| Novo campo | `POST equipment_field_config` com `{ field_key: "custom_<Date.now()>", label, field_type (text, number, date, select ou boolean), options (lista de textos, só no tipo select), is_visible: true, is_required: false, position: <quantidade atual de campos>, company_id }`, objeto de volta (`:55-60`; montagem em `EquipmentFieldConfigDialog.tsx:444-454`). Toast "Campo criado!". |
| Excluir | `DELETE equipment_field_config?id=eq.<id>` (`:74`). Toast "Campo excluído!". Os valores já gravados em `equipment.custom_fields` continuam lá, só deixam de aparecer. |
| Arrastar para reordenar | N chamadas `PATCH equipment_field_config?id=eq.<id>` em paralelo, cada uma com `{ position: <índice novo> }` (`:88-92`). Sem toast de sucesso. |

### 12.6 Ficha do equipamento (`/equipamentos/<nome>-<código>`; `pages/EquipmentDetail.tsx`)

**Ao abrir** (`:130-155,205-218`):

| Chamada | Para quê |
|---|---|
| `GET equipment` (lista inteira, sem filtro) | A ficha acha o equipamento na lista por UUID ou `public_short_code`, e usa a mesma lista para o seletor "Buscar equipamento...". |
| `GET customers` | Nome do cliente e seletor. |
| `GET equipment_categories` | Nome e cor da categoria. |
| `GET service_orders` (as de 12.2) | A aba "Histórico / Tarefas" filtra no navegador `equipment_id` igual ao equipamento (`:200`). **Uma OS com vários equipamentos só aparece no primeiro** (a coluna guarda um id só). |
| `GET equipment_attachments` | `select=*`, `equipment_id=eq.<id>`, `order=created_at.asc` (`hooks/useEquipmentAttachments.ts:24-34`). |
| `GET equipment_tasks` | `select=*`, `equipment_id=eq.<id>`, `order=created_at.desc` (`hooks/useEquipmentTasks.ts:24-34`). |
| `GET equipment_field_config` | Rótulos dos campos personalizados. |
| `GET customer_portals` | `select=token`, `customer_id=eq.<cliente>`, `is_active=eq.true`, `.maybeSingle()` (`:205-218`). O QR Code aponta para `<site>/portal/<token>?eq=<id do equipamento>`; sem portal ativo, vira o texto `EQ-<identificador>`. |
| `GET profiles` e `GET company_settings` | Nome, telefone, e-mail e logo da empresa na etiqueta (`useCompanySettings`, `hooks/useCompanySettings.ts:138-150`: `company_settings?select=*&company_id=eq.<empresa>` com `.maybeSingle()`), e a configuração branca do QR (`useBrandedQrConfig`). |

**Ações:**

| Ação | Chamada |
|---|---|
| Anexar arquivo | `POST /storage/v1/object/equipment-files/<id do equipamento>/<Date.now()>_<uuid>_<nome-seguro>` e depois `POST equipment_attachments` com `{ equipment_id, file_url, file_name, file_type, description }` (o `file_url` é o endereço público montado no navegador), objeto de volta (`hooks/useEquipmentAttachments.ts:38-58`). `uploaded_by` não é enviado. Se o upload dá certo e o insert falha, o arquivo fica solto no bucket. |
| Excluir anexo | `DELETE equipment_attachments?id=eq.<id>` (`:72`). **Só a linha**; o arquivo continua no bucket. |
| Nova tarefa (campo de texto e botão) | `POST equipment_tasks` com `{ equipment_id, title }`, objeto de volta (`EquipmentDetail.tsx:278`; `hooks/useEquipmentTasks.ts:39`). |
| Marcar ou desmarcar tarefa | `PATCH equipment_tasks?id=eq.<id>` com `{ is_completed }` (`:54`). |
| Excluir tarefa | `DELETE equipment_tasks?id=eq.<id>` (`:64`). |
| Editar equipamento | `PATCH equipment?id=eq.<id>` direto (`EquipmentDetail.tsx:1197`) e depois a página inteira recarrega. |
| Excluir equipamento | `DELETE equipment?id=eq.<id>` direto, sem olhar o erro (`:1218`). |
| Gerar Etiqueta, Imprimir, QR Code, copiar link | Sem chamada ao servidor (a janela de impressão é do navegador). |

### 12.7 Serviços externos e contratos de resposta

**Portal do cliente (as duas RPCs que a ficha de cliente usa)** (`hooks/useCustomerPortalSettings.ts:103-148`):

- `POST /rest/v1/rpc/get_customer_portal_settings` com `{ "p_customer_id": "<uuid>" }`. Resposta: `null` (cliente sem portal ou excluído) ou o objeto abaixo. O app lê de forma estrita: `is_active`, `password_enabled` e `password_configured` só valem se forem o booleano `true`; chaves ausentes em `permissions` usam o padrão e em `public_sections` valem `false`.
- `POST /rest/v1/rpc/save_customer_portal_settings` com `{ "p_customer_id", "p_is_active", "p_password_enabled", "p_password" (texto ou null), "p_permissions": {...}, "p_public_sections": {...} }`. A resposta tem o **mesmo formato** do get. Resposta que não seja objeto faz o app falhar com "Resposta inválida ao salvar o portal".

```json
{
  "token": "a3f9c2e1d4b7...",
  "is_active": true,
  "password_enabled": false,
  "password_configured": false,
  "permissions": { "service_orders": true, "equipment": true, "contracts": true, "charges": true,
                   "invoices": false, "documents": false, "ticket_requests": true },
  "public_sections": { "service_orders": false, "equipment": false, "contracts": false, "charges": false,
                       "invoices": false, "documents": false, "ticket_requests": false }
}
```

Os padrões acima são os que o app assume quando o servidor não manda a chave (`hooks/useCustomerPortalSettings.ts:34-62`). O `token` é o mesmo que a ficha lê em `customer_portals` e que monta o link `/portal/<token>`. Para o cliente novo (aba Portal ainda sem dados), o app começa com `is_active = true`, senha desligada e esses padrões.

**BrasilAPI, consulta de CNPJ** (`components/customers/CnpjDocumentInput.tsx:70-135`): `GET https://brasilapi.com.br/api/cnpj/v1/<14 dígitos>`, direto do navegador (precisa de internet; como a chamada sai do navegador, a BrasilAPI precisa responder com CORS liberado, o que não foi conferido nesta análise). Campos lidos: `razao_social`, `nome_fantasia`, `email`, `ddd_telefone_1` (DDD e número juntos, sem formatação, por exemplo `"1123851939"`; só vale com 8 dígitos ou mais), `cep` (8 dígitos sem hífen), `descricao_tipo_de_logradouro` e `logradouro` (juntos formam "AVENIDA PAULISTA"), `numero`, `complemento`, `bairro`, `municipio` e `uf`. Status diferente de 2xx **ou** corpo com a chave `message` mostra o toast vermelho "CNPJ não encontrado na Receita"; exceção de rede ou CORS mostra "Não foi possível consultar o CNPJ agora"; sucesso mostra "Dados da empresa preenchidos!". A consulta repetida do mesmo número é ignorada, a menos que a pessoa clique na lupa.

**Edge `cep-lookup`** (`components/CepLookup.tsx:28-47`; função em `supabase/functions/cep-lookup/index.ts`): `POST /functions/v1/cep-lookup` com `{ "cep": "01310100" }` (só dígitos). Sucesso (200): `{ "logradouro": "...", "bairro": "...", "cidade": "...", "estado": "SP", "ibge": "3550308" }` (`ibge` com 7 dígitos). O app preenche Logradouro, Bairro, Cidade, UF e o código IBGE escondido, e mostra o toast "Endereço encontrado!". **CEP inexistente:** a função de verdade responde **404** com `{ "error": "CEP não encontrado" }`, e o `functions.invoke` trata qualquer status diferente de 2xx como erro, então o app cai no `catch` e mostra **"Erro ao buscar CEP"**. O toast "CEP não encontrado" só aparece se o servidor responder **2xx com a chave `error`** (`CepLookup.tsx:36-40`). Escolha do backend falso: 200 com `error` para o toast "CEP não encontrado"; 404 ou 500 para "Erro ao buscar CEP" (comportamento de produção).

**Nominatim, sugestões de endereço** (`components/AddressAutocomplete.tsx:85-110`): `GET https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&countrycodes=br&limit=5&q=<texto>` com o cabeçalho `Accept-Language: pt-BR`. Lê de cada item: `lat`, `lon`, `display_name` e `address.{road, house_number, suburb ou neighbourhood, city ou town ou village, state, postcode, country_code}`. Só ficam os itens com `country_code = "br"`; o estado (nome por extenso) vira sigla; o CEP perde o hífen e é cortado em 8 dígitos. **Geocodificação ao salvar** (`utils/geolocation.ts:125-139`): a mesma rota com `limit=1`, lendo `[0].lat` e `[0].lon`; qualquer falha devolve `null` e o cliente é salvo sem coordenadas.

**IBGE, cidades da UF** (`components/StateCitySelector.tsx:82-95`): `GET https://servicodados.ibge.gov.br/api/v1/localidades/estados/<UF>/municipios?orderBy=nome`. Resposta: lista de `{ "id": 3550308, "nome": "São Paulo", ... }`. O app usa `nome` na lista e `id` (como texto, 7 dígitos) como código IBGE do município. Falha vira lista vazia, sem aviso.

**Storage** (buckets e caminhos):

| Bucket | Visibilidade | Caminho gravado | Quem usa |
|---|---|---|---|
| `customer-photos` | público | `<Date.now()>.<ext>`; pelo formulário público, `lead-capture/<short_code>/<uuid>.<ext>` | Foto do cliente |
| `equipment-files` | público | `photos/<uuid>_<nome-seguro>` (foto do equipamento); `<id do equipamento>/<Date.now()>_<uuid>_<nome-seguro>` (anexos) | Equipamento |
| `customer-documents` | privado (link assinado de 60 s) | `<empresa>/<cliente>/<uuid>_<nome-seguro>` | Aba Documentos |

O app **não pergunta ao servidor o endereço público**: monta `<VITE_SUPABASE_URL>/storage/v1/object/public/<bucket>/<caminho>` sozinho (`getPublicUrl` da biblioteca) e grava esse texto em `photo_url` e `file_url`. O backend falso precisa, portanto, servir `GET /storage/v1/object/public/<bucket>/<caminho>` com os bytes e o `Content-Type` certos; senão a imagem aparece quebrada. A resposta do upload só precisa ser 2xx (o app não lê o corpo).

### 12.8 Formatos gravados (com máscara ou só dígitos)

| Dado | Cliente (formulário interno) | Cliente rápido ("+") | Formulário público (gravado pela regra do banco) | Outros |
|---|---|---|---|---|
| Documento | **Com máscara**: `123.456.789-09` ou `12.345.678/0001-90` (`utils/masks.ts` `cpfCnpjMask`) | Como foi digitado, com máscara | **Só dígitos** | Fornecedor: `cpf_cnpj` é texto livre, exatamente como digitado |
| Telefone e celular | **Com máscara**: `(11) 3333-4444` ou `(11) 93333-4444`; sai tirando o `55` de 12 ou 13 dígitos | `celular` com máscara | **Só dígitos** | Contato: `phone` com máscara de telefone; fornecedor: texto livre |
| CEP | **Com máscara** `00000-000` (`customers.zip_code`) | — | **Só dígitos** | — |
| Datas | `yyyy-MM-dd` em `birth_date`, `install_date` e `warranty_until`; `custom_fields` de tipo data também `yyyy-MM-dd` | — | — | `created_at`, `updated_at`, `deleted_at` em ISO com fuso |
| Tipo de cliente | `"pf"` ou `"pj"` em minúsculas | idem | idem (padrão `"pf"`) | — |
| Origem | O **nome** da origem em `customers.origin` (texto, não referência) | — | `"public_form"` | — |
| Número do endereço | Em `address_number` **e** copiado em `street_number` | — | — | — |
| Identificador do equipamento | Texto de 4 dígitos com zeros à esquerda (`"0001"`), gerado pelo servidor | — | — | — |
| Status do equipamento | `"active"` (nasce assim; a tela mostra "Ativo"/"Inativo") | — | — | — |

O navegador do formulário público manda o texto **como foi digitado, com máscara**; é a regra do banco que tira tudo o que não é número (seção 13.1). Quem simular essa regra no backend falso deve fazer o mesmo, senão o cliente criado por esse caminho aparece com o documento "cru" ou mascarado de forma diferente dos outros.

### 12.9 Colunas por tabela (de `integrations/supabase/types.ts`)

"Obrigatória no insert" = coluna sem valor padrão no tipo `Insert`.

| Tabela | Colunas | Obrigatórias no insert |
|---|---|---|
| `customers` | `address`, `address_number`, `birth_date`, `celular`, `city`, `company_id`, `company_name`, `complement`, `created_at`, `credit_limit`, `customer_type` (enum `pf` ou `pj`), `deleted_at`, `document`, `email`, `ibge_municipality_code`, `id`, `inscricao_estadual`, `inscricao_municipal`, `is_deleted`, `is_service_customer`, `is_store_customer`, `lat`, `latitude`, `lead_consent_at`, `lng`, `longitude`, `name`, `neighborhood`, `nome_fantasia`, `notes`, `origin`, `phone`, `photo_url`, `public_short_code`, `state`, `street_number`, `updated_at`, `whatsapp_notifications_enabled`, `whatsapp_opt_in_at`, `whatsapp_opt_out_at`, `zip_code` | `company_id`, `name` |
| `customer_contacts` | `created_at`, `customer_id`, `email`, `id`, `name`, `notes`, `phone`, `position`, `updated_at` | `customer_id`, `name` |
| `customer_origins` | `color`, `company_id`, `created_at`, `icon`, `id`, `is_active`, `name` | `company_id`, `name` (o hook de criar origem avulsa não envia `company_id`; quem preenche é o gatilho) |
| `customer_portals` | `created_at`, `customer_id`, `id`, `is_active`, `is_public`, `password_enabled`, `permissions` (json), `public_sections` (json), `token` | `customer_id` |
| `customer_documents` | `amount`, `company_id`, `created_at`, `customer_id`, `description`, `document_kind`, `document_number`, `document_type`, `file_name`, `id`, `is_visible_in_portal`, `issue_date`, `mime_type`, `size_bytes`, `storage_path`, `title`, `updated_at`, `uploaded_by` | `company_id`, `customer_id`, `document_kind`, `file_name`, `storage_path`, `title` |
| `lead_capture_forms` | `company_id`, `consent_text`, `created_at`, `created_by`, `description`, `expires_at`, `field_config` (json), `id`, `is_active`, `max_submissions`, `require_consent`, `short_code`, `submission_count`, `title`, `updated_at` | `company_id`, `created_by` |
| `suppliers` | `address`, `company_id`, `contact_name`, `cpf_cnpj`, `created_at`, `created_by`, `email`, `id`, `name`, `notes`, `phone`, `updated_at` | `company_id`, `name` |
| `equipment` | `attachments_public`, `brand`, `capacity`, `category_id`, `company_id`, `created_at`, `custom_fields` (json), `customer_id`, `id`, `identifier`, `install_date`, `location`, `model`, `name`, `notes`, `photo_url`, `public_short_code`, `serial_number`, `status`, `updated_at`, `warranty_until` | `company_id`, `customer_id`, `name` |
| `equipment_categories` | `color`, `company_id`, `created_at`, `description`, `id`, `name`, `updated_at` | `company_id`, `name` |
| `equipment_field_config` | `company_id`, `created_at`, `field_key`, `field_type`, `id`, `is_required`, `is_visible`, `label`, `options` (json, lista de textos), `position`, `updated_at` | `company_id`, `field_key`, `label` |
| `equipment_attachments` | `created_at`, `description`, `equipment_id`, `file_name`, `file_type`, `file_url`, `id`, `uploaded_by` | `equipment_id`, `file_name`, `file_url` |
| `equipment_tasks` | `assigned_to`, `created_at`, `created_by`, `description`, `due_date`, `equipment_id`, `id`, `is_completed`, `title`, `updated_at` | `equipment_id`, `title` |

Observação: `customers` tem os dois pares `lat`/`lng` e `latitude`/`longitude`; o app grava e lê **`latitude`/`longitude`** (`CustomerFormDialog.tsx:290`). `lat` e `lng` não são usados por estas telas.

### 12.10 Consultas do aplicativo que as telas supõem prontas

Não é o inventário do aplicativo todo (o menu, o sino de avisos e outros componentes fazem consultas que não mapeei), é o que Clientes, Fornecedores e Equipamentos dependem para abrir:

| Chamada | Detalhe | Onde |
|---|---|---|
| `auth.signInWithPassword`, `onAuthStateChange`, `getSession`, `getUser` | Sessão em `localStorage`; `getUser` vai à rede (`GET /auth/v1/user`) | `contexts/AuthContext.tsx:113,288`; `hooks/useUserCompany.ts:39` |
| `GET profiles` | `select=*`, `user_id=eq.<id>`, **`.single()`**: precisa de exatamente 1 linha; o perfil traz `company_id` | `AuthContext.tsx:187-191` |
| `GET user_roles` | `select=role`, `user_id=eq.<id>` (papéis: `admin`, `gestor`, `super_admin` etc.) | `:198-202` |
| `GET user_permissions` | `select=permissions,is_active`, `user_id=eq.<id>`, `.maybeSingle()`. **Sem linha** = modo antigo, qualquer papel libera tudo; **com linha** = só o que a lista tem (ou `*`) | `:208-222` |
| `GET admin_permissions` | `select=permission`, `user_id=eq.<id>` | `:226-231` |
| `GET company_modules`, `GET companies`, `GET subscription_plans` | Quais módulos estão ligados: `company_modules?select=module_code,quantity,activated_at&company_id=eq.<empresa>`; `companies?select=subscription_status,subscription_expires_at,...&id=eq.<empresa>` com `.maybeSingle()`; `subscription_plans?select=id,code,name,description,price,max_users,included_modules,is_active&is_active=eq.true&order=price`. **Empresa com `subscription_status = 'testing'` e sem data de expiração (ou data futura) liga todos os módulos** | `hooks/useCompanyModules.ts:119-170` |
| `HEAD profiles` com contagem | `select=*` com `count=exact` e `head`, `company_id=eq.<empresa>`, `is_active=eq.true` (conta usuários) | `useCompanyModules.ts:189-201` |
| `GET company_settings` | `select=*`, `company_id=eq.<empresa>`, `.maybeSingle()` | `hooks/useCompanySettings.ts:145` |

Sem login válido (ou sem `profiles.company_id`) as telas ficam no carregamento ou mostram erro.

### 12.11 Lista mínima para o backend falso gravar os cadastros do tutorial

Em ordem de prioridade, só para Clientes, Fornecedores e Equipamentos:

1. **Sessão:** `GET /auth/v1/user`; `profiles` (1 linha, com `company_id`), `user_roles` (uma linha `admin`), `user_permissions` (nenhuma linha), `admin_permissions` (vazio); `companies`, `company_modules`, `subscription_plans` (empresa em `testing` para liberar todas as abas).
2. **Clientes:** `customers` com os filtros `is_deleted`, `order`, `offset`/`limit`, insert e update devolvendo o objeto, o gatilho de `public_short_code` e o padrão `whatsapp_notifications_enabled = true`; `customer_portals` (uma linha por cliente criado, com `token`) e as duas RPCs do portal (12.7). **Sem a RPC `get_customer_portal_settings` não dá para salvar uma edição de cliente.**
3. **Origens e captação:** `customer_origins` (listar, criar sem `company_id`, criar em lote com `company_id`, editar, excluir), `lead_capture_forms` (com `short_code` gerado).
4. **Fornecedores:** `suppliers` (listar, insert devolvendo objeto, update sem retorno, delete).
5. **Equipamentos:** `equipment` com o embed `customer:customers(id, name)` e gerador de `identifier` e `public_short_code`; `equipment_categories`; `equipment_field_config` **já com as 6 linhas padrão da empresa** (seção 13.1); `equipment_attachments` e `equipment_tasks`.
6. **Leituras da ficha do cliente que podem devolver lista vazia:** `service_orders` (e `service_order_assignees`), `financial_transactions`, `contracts`, `customer_paid_expenses`, `tenant_payment_accounts`, `tenant_charges`, `stocks`, `customer_documents`.
7. **Arquivos:** upload nos buckets `customer-photos` e `equipment-files` e entrega em `/storage/v1/object/public/<bucket>/<caminho>`.
8. **Internet ou simulação:** BrasilAPI (CNPJ), `cep-lookup`, IBGE (cidades), Nominatim (pode falhar sem estragar nada).
9. **Opcional:** a página pública `/cadastro/<código>` (`get_lead_capture_form`, `lead-capture-upload-photo`, `lead-capture-submit`), se o roteiro mostrar o formulário aberto como cliente final.

---

## 13. Regras do servidor, gatilhos e padrões (o que o banco faz sozinho)

Lido das migrações em `supabase/migrations/` e dos tipos. O backend falso deve imitar o que muda o que a pessoa vê na tela.

### 13.1 Por tabela

| Tabela | O que o servidor faz sozinho |
|---|---|
| `customers` | **(1)** `set_company_id_on_insert` preenche `company_id` quando vem nulo (`20260602213504_auto_set_company_id_trigger.sql:17-35`). **(2)** `trg_ensure_public_short_code` (antes de inserir ou atualizar) gera `public_short_code`: 12 caracteres do alfabeto `abcdefghjkmnpqrstuvwxyz23456789`, único (`20260620200000_public_short_codes_links_amigaveis.sql:60-90,144-159`). **(3)** `trg_create_customer_portal_on_insert` (depois de inserir) cria a linha de `customer_portals` com `token` aleatório em hexadecimal e `is_active = true`, `UNIQUE(customer_id)` (`20260610130000_auto_create_customer_portal.sql:32-52`). **(4)** `track_customer_whatsapp_preference` (antes de inserir ou de mudar `whatsapp_notifications_enabled`): na criação com `true` carimba `whatsapp_opt_in_at = now()` e zera `whatsapp_opt_out_at`; ao passar de desligado para ligado carimba o opt-in; ao desligar carimba `whatsapp_opt_out_at` (`20261015120000_whatsapp_automation_ui_preferences.sql:61-90`). **(5)** `update_customers_updated_at` mantém `updated_at` (`20260131190034_...:276`). **Padrões:** `is_deleted = false`; `is_service_customer = true`; `is_store_customer = false`; **`whatsapp_notifications_enabled = true`** (a migração `20261016233000_customers_whatsapp_opt_out_por_padrao.sql:98` trocou o padrão que era `false`; clientes antigos não foram alterados). `customer_type` só aceita `pf` e `pj`. **Não existe unicidade em `document`**: dois clientes com o mesmo CPF ou CNPJ são aceitos. A exclusão é lógica (`is_deleted`, `deleted_at`). |
| `customer_portals` | Uma linha por cliente. O padrão da tabela dá `token` aleatório e `is_active = true`. As RPCs `get_customer_portal_settings` e `save_customer_portal_settings` (`20261021140000_customer_portal_public_sections.sql:616-790`) leem e gravam `is_active`, `is_public` (sempre `true` ao salvar), `password_enabled`, `permissions` e `public_sections`, normalizam os dois mapas (`normalize_customer_portal_permissions` e `normalize_customer_portal_public_sections`) e **guardam a senha só como hash** em outra tabela (`customer_portal_credentials`); `password_configured` apenas diz se existe. Senha: mínimo 8 caracteres e no máximo 72 bytes, senão o erro `22023`. **As duas exigem `admin`/`super_admin`, ou usuário com a permissão `fn:edit_customer` da mesma empresa; senão `Acesso negado` (`42501`)**, que o app mostra como "Você não tem permissão para realizar esta ação.". Como o app chama a RPC em **todo** salvamento, quem tem `fn:create_customer` mas não `fn:edit_customer` (e tem registro de permissões) cria o cliente, **vê o erro e a janela continua aberta** (a confirmar com um usuário assim). |
| `customer_contacts` | Sem `company_id` (o vínculo é o `customer_id`). Sem regra especial além da chave estrangeira. |
| `customer_origins` | Padrões: `icon = 'Globe'`, `color = '#6B7280'`, `is_active = true` (`20260308232722_...:6-13`). `company_id` é obrigatório, mas o gatilho genérico o preenche quando o hook não envia. Escrita só para quem pode gerir o sistema da própria empresa (13.4). |
| `lead_capture_forms` | O gatilho `ensure_lead_form_short_code` gera `short_code` (`20260721120000_lead_capture_public_forms.sql`). Padrões: `title = 'Cadastro de Cliente'`, `is_active = true`, `require_consent = true`, `submission_count = 0`. `created_by` é obrigatório (o app manda o `id` do usuário logado). `max_submissions` existe na tabela e a regra do banco o respeita (o formulário deixa de aceitar envios quando `submission_count` chega nele), mas **nenhuma tela o preenche** (seções 3.10.2 e 14.2). |
| **RPC `submit_lead_capture_form`** | Chamada só pela edge `lead-capture-submit`, com a chave de serviço (`p_short_code`, `p_fields`, `p_consent`, `p_ip_hash`). Resolve a empresa pelo código do formulário. Limites: 5 envios por 10 minutos por formulário e IP e 30 por dia por IP, senão "Muitas tentativas. Tente novamente mais tarde.". Mensagens de validação que a pessoa vê: "Consentimento obrigatório", "Campo obrigatório ausente: {campo}", "E-mail inválido", "Telefone inválido", "CEP inválido", "Foto inválida", "CPF inválido", "CNPJ inválido", "Formulário indisponível". **Valida os dígitos verificadores de CPF e CNPJ** (CNPJ quando o Tipo escolhido é Pessoa Jurídica, CPF nos demais casos; `lead_valida_cpf` e `lead_valida_cnpj`, `20261015233000_lead_capture_insert_dinamico_respeita_default.sql:200-210`): é a única porta de entrada que confere os dígitos (seção 9). Grava só dígitos em documento, telefone (10 ou 11 dígitos), celular (10 ou 11) e CEP (8); `origin = 'public_form'`; `lead_consent_at` quando aceitou; `customer_type` o escolhido ou `pf`; nome "Cliente (formulário)" se o campo Nome não estiver ligado; sobe o contador `submission_count`. O insert é montado só com as colunas enviadas, então o que fica de fora recebe o padrão do banco (por isso o cliente nasce com WhatsApp ligado). Resposta neutra `{ "success": true }`. |
| `suppliers` | `set_suppliers_updated_at` mantém `updated_at`. Sem unicidade em `cpf_cnpj`. Quatro políticas `suppliers_select/insert/update/delete_own_company`: cada usuário só vê e mexe nos da própria empresa (ou super admin) (`20260619150000_estoque_fase_a_movements_suppliers.sql:98-119`). A coluna `address` veio depois (`20260927200000_supplier_address.sql`). |
| `equipment` | **(1)** `trg_set_equipment_identifier` (antes de inserir): se `identifier` vier nulo ou em branco, chama `next_equipment_identifier(company_id)`, que usa um contador por empresa (`equipment_number_counters`, sem acesso do navegador) e devolve o número com zeros à esquerda, 4 dígitos: "0001", "0002"... O contador **não volta** quando um equipamento é apagado. `UNIQUE (company_id, identifier)` (`20260610140000_equipment_identifier_sequential_per_company.sql`). **(2)** `public_short_code` por gatilho, igual ao cliente. **(3)** Padrões: `status = 'active'` (`20260228193300_...:22`), `attachments_public = true` (`20260723120000_portal_data_equipment_attachments.sql:24`). **(4)** O gatilho genérico preenche `company_id` quando falta. |
| `equipment_categories` | Padrão `color = '#3b82f6'` (`20260228193300_...:7`). `updated_at` por gatilho. |
| `equipment_field_config` | `UNIQUE (company_id, field_key)`. **Toda empresa nova ganha 6 linhas** pelo gatilho `trg_seed_equipment_field_config_on_company_insert` (`20260906190100_seed_equipment_field_config_por_empresa.sql:48-83`), só se a empresa ainda não tiver nenhum campo: `brand` "Marca", `model` "Modelo", `serial_number` "Nº de Série", `capacity` "Capacidade/Especificação", `location` "Local" (todos `text`) e `install_date` "Data de Instalação" (`date`), posições 1 a 6, visíveis e não obrigatórios. A migração também preencheu empresas que estavam com zero campos e **não** mexeu em quem já tinha algum. |
| `equipment_attachments`, `equipment_tasks` | Sem `company_id`. `equipment_tasks.is_completed` e os textos são tudo o que a ficha usa. |
| `customer_documents` | `company_id` obrigatório (o app envia). Arquivos no bucket privado `customer-documents`. |

### 13.2 Chaves estrangeiras que mudam o que acontece ao excluir

Estas regras são as que o banco aplica; o backend falso só precisa imitar as que o roteiro vai exercitar.

| Excluir | O que acontece com o que aponta para ele |
|---|---|
| **Equipamento** | Apagados junto (cascata): `equipment_attachments`, `equipment_tasks`, `pmoc_schedules`, `service_order_equipment`, `service_order_equipment_service_types`. (A tabela `pmoc_items` foi removida em `20260523165401_pmoc_v1_9_x_checklist_drop_legados.sql`.) Ficam e perdem o vínculo (`equipment_id` vira nulo): `service_orders`, `form_responses`, `service_order_activities`. **Bloqueia a exclusão:** `contract_items.equipment_id` (nenhuma migração define regra de exclusão; a confirmar no banco real). |
| **Categoria de equipamento** | `equipment.category_id` volta a nulo. |
| **Fornecedor** | Apagados junto: cotações e ordens de compra. Ficam e perdem o vínculo (`SET NULL`): lançamentos financeiros, movimentações de estoque, fornecedor padrão do material, fornecedor aprovado numa compra, registros de importação de nota e notas recebidas (seção 5.6; `20260930130000_inventory_supplier_id.sql:97-100`, `20260619160000_estoque_fase_a_compras_rpc.sql:15`). |
| **Cliente** | Nunca é apagado de verdade pelo app (exclusão lógica). Os equipamentos, OS e contratos continuam. |
| **Formulário de captação** | Os clientes já cadastrados por ele continuam. |
| **Origem** | Nada aponta para ela por chave: o cliente guarda o nome em texto. |

### 13.3 Gatilho de contador: o que isso significa na demonstração

Equipamentos criados e apagados na gravação **gastam números**. Se o roteiro mostra o primeiro equipamento com "ID: 0001" e a empresa de demonstração já teve equipamentos, o número será maior. Para ter "0001", use uma empresa recém-criada (o contador nasce na primeira inserção) ou reinicie o contador `equipment_number_counters` da empresa no ambiente de teste.

### 13.4 Permissões no banco (quem consegue gravar)

- `equipment_categories`, `customer_origins` e `equipment_field_config` têm a política "System managers can manage <tabela>" (`FOR ALL`, `20260817120000_fix_equipment_field_config_rls_tenant_scope.sql:24-40`, `20260817130000_fix_tenant_config_tables_rls_tenant_scope.sql:65-93`): só passa `is_super_admin` ou (`can_manage_system` **e** mesma empresa). `can_manage_system` vale para admin, gestor, quem tem todas as permissões, ou a permissão `*` ou `fn:manage_settings` (`20260610180000_wildcard_star_permission_server_side.sql:50-70`). Para quem não passa, **criar** categoria, origem ou campo dá o erro `42501`, "Você não tem permissão para realizar esta ação."; **editar e excluir** não dão erro de permissão, o banco só não encontra a linha para esse usuário (comportamento padrão do PostgreSQL com política `FOR ALL`; deduzido, a confirmar): a edição que pede a linha de volta (campos e categorias) mostra "Registro não encontrado." e a exclusão mostra o aviso de sucesso sem apagar nada. Isso vale mesmo que o botão apareça na tela.
- `suppliers`: só a própria empresa (13.1).
- `customer_portals`: leitura e escrita do usuário pelas duas RPCs (13.1); o portal público lê só por RPC, nunca pela tabela.
- `equipment_number_counters`: sem acesso nenhum do navegador.
- `customers`, `equipment`, `customer_contacts`, `equipment_attachments`, `equipment_tasks`, `lead_capture_forms`: isolamento por empresa (detalhe das políticas não foi lido linha a linha; a confirmar se o roteiro usar mais de um usuário).
- A função `user_has_permission(usuário, chave)`, usada pelas RPCs do portal: `admin` e `super_admin` sempre passam; com registro em `user_permissions` vale `is_active` e (`*` ou a chave); sem registro, qualquer papel passa (`20260917150000_crm_multi_responsavel_e_visibilidade.sql`, função `user_has_permission`).

### 13.5 Arquivos: regra de carimbo da empresa

Os envios para `customer-photos`, `equipment-files` (e `customer-documents`) levam o metadado `company_id` da empresa do usuário (`utils/tenantStorage.ts:64-72`). No servidor de verdade a política de gravação compara esse valor com a empresa real de quem enviou e recusa se divergir. O backend falso não precisa dessa conferência.

---

## 14. Pegadinhas para o roteiro e para a gravação

Cada item diz o que acontece e o que fazer na narração ou na preparação. A seção de onde vem o detalhe está entre parênteses. O que só se confirma vendo rodando está marcado "(a confirmar)" e repetido na seção 15.

### 14.1 Clientes e cadastro

1. **O endereço está na aba Fiscal**, no bloco "Endereço fiscal"; a aba Contato não tem endereço. Quem narra "agora o endereço" precisa trocar de aba antes (3.4.2).
2. **Criar cliente não abre a ficha.** A janela fecha e o cliente aparece na lista, em ordem alfabética. Para mostrar a ficha é preciso clicar na linha (3.1, 3.7).
3. **"Tipo" já vem como "Pessoa Jurídica" e não muda mais nada na janela.** Para gravar uma pessoa física é preciso trocar o Tipo à mão; senão fica gravado `pj`. Razão Social e Nome Fantasia ficam na aba Fiscal nos dois casos (3.4.1, 3.4.2).
4. **O interruptor do WhatsApp se desliga sozinho enquanto se digita o celular.** Ele nasce ligado, mas desabilitado (com o texto "Informe um celular válido para liberar esta opção."), e **cada tecla digitada no Celular, enquanto ele tem menos de 10 dígitos, o desliga**. Quem digita tecla a tecla chega ao 10º dígito com o interruptor liberado, porém **desligado**, e precisa clicar para ligar; colar o número inteiro de uma vez deixa o interruptor como estava (ligado). Ao salvar, o app ainda força desligado se o celular tem menos de 10 dígitos (3.4.1; `CustomerFormDialog.tsx:285-286,499-505`).
5. **Salvar grava também o portal**, sempre, até em cliente novo. Se essa segunda gravação falhar, o cliente **já foi criado**, a janela continua aberta com o erro e a nova tentativa só regrava o portal: não cria outro cliente e **não salva** o que foi alterado nos outros campos depois da falha. Na **edição**, se a leitura das configurações do portal falhar, o botão "Salvar" fica desligado (3.7, 12.1, 13.1).
6. **Dois avisos de erro seguidos mostram só o último.** Ao falhar um cadastro saem "Erro ao criar cliente" (com o motivo) e logo "Erro" (com o mesmo motivo); como só cabe um aviso por vez, quem grava vê o segundo, e a janela continua aberta (3.7, 7.6).
7. **Nenhum documento é validado** (nem CPF nem CNPJ) no cadastro de cliente, no cliente rápido nem no fornecedor. Um CNPJ qualquer de 14 dígitos dispara a consulta e, se a BrasilAPI não o conhece, aparece "CNPJ não encontrado na Receita", sem impedir o salvamento. Para a demonstração, use um CNPJ real. Só o formulário público confere os dígitos (seção 9).
8. **A consulta de CNPJ não repete o mesmo número** se a pessoa apaga e digita igual; só a lupa repete. Precisa de internet (3.5.1).
9. **O campo Nome só é preenchido pela consulta de CNPJ se estiver vazio.** Quem digitou o nome antes não o vê trocado (3.5.1).
10. **A busca de CEP não preenche Número nem Complemento**, e o aviso de CEP inexistente provavelmente nunca aparece: o que aparece é "Erro ao buscar CEP" (a confirmar) (3.5.2, 12.7).
11. **Cidade depende do IBGE.** O seletor de Cidade só tem as opções que a API do IBGE devolve; sem internet ele fica vazio e não dá para digitar a cidade à mão (3.5.4).
12. **Apagar não limpa na edição.** Esvaziar a Data de Nascimento de um cliente que já tinha não remove o valor antigo (a chave nem vai no envio); o mesmo vale para o espelho do Número no campo fiscal (`street_number`). Também não há botão para **remover a foto** do cliente. No "Responsável no Local" acontece igual com Telefone, Email corporativo e Cargo do contato (3.4.1, 3.7, 4.4).
13. **Rascunho automático.** Fechar o "Novo Cliente" sem salvar guarda o que foi digitado, e na abertura seguinte aparece "Rascunho encontrado" com "Começar do zero" e "Retomar rascunho". O rascunho vive na aba do navegador (`sessionStorage`): uma aba nova começa sem ele (3.6).
14. **A lista guarda o estado da sessão.** Busca, ordem, página e tamanho da página ficam no `sessionStorage`; reabrir a tela na mesma aba pode mostrar uma busca antiga ou a página 2, e tudo some ao fechar a aba (7.2). No computador a busca procura trechos e diferencia acento ("Antonio" não acha "Antônio"); no celular ela ignora acento e ordem das palavras (3.2, 3.3).
15. **Excluir cliente é lógico.** Ele some da lista, mas os equipamentos dele continuam aparecendo em Equipamentos, e o aviso de "tem registros vinculados" nunca aparece para cliente (3.8).
16. **Cliente do formulário público** chega com Origem `public_form` (texto cru, sem ícone) e documento e telefone só com dígitos; ao editar e salvar, passam a ter máscara (3.7, 3.10.4).

### 14.2 Origens e formulários de captação

1. **O catálogo de origens nasce vazio.** Até alguém criar origens, o campo "Origem" só mostra "Nenhuma". O botão "Criar origens padrão" cria 10 de uma vez e só aparece com o catálogo vazio (3.9).
2. **A origem é gravada como texto.** Renomear ou excluir uma origem não muda os clientes antigos (a ficha mostra o nome sem ícone), e **excluir não pede confirmação** (3.9).
3. **Há três caminhos para as origens**: "Configurar origens" na tela de Clientes (no celular, "Origens"), o "+" ao lado do campo "Origem" do cadastro e Configurações, aba "Usabilidade", cartão "Origens" (3.9).
4. **O link do formulário de captação só existe depois de salvar.** O botão "Gerar e copiar link" do editor só aparece em formulário já salvo; na lista, "Copiar link" monta o endereço com o título em minúsculas e hifens (3.10.1, 3.10.2).
5. **Formulário novo vem só com "Nome" ligado e obrigatório.** Sem nenhum campo ligado o app recusa ("Habilite ao menos um campo do formulário"). O limite de envios (`max_submissions`) existe no banco, mas não há campo para ele na tela (3.10.2, 13.1).
6. **Documento no formulário público.** Se "Tipo de cliente" estiver desligado no formulário, todo envio é tratado como pessoa física e um CNPJ digitado volta como "CPF inválido". Ligue "Tipo de cliente" junto com "CPF / CNPJ" para aceitar empresas (3.10.4).
7. **Não há fila de aprovação.** O cliente cai direto na lista. A lista se atualiza ao voltar para a aba do Dominex; se não atualizar, recarregue a página (3.10.4, 11.4).
8. **Ensaiar o envio demais bloqueia.** O servidor aceita 5 envios por formulário e por IP em 10 minutos; depois disso a página mostra "Muitas tentativas. Tente novamente mais tarde." (3.10.4).

### 14.3 Ficha do cliente

1. **"Editar" e "Excluir" do cabeçalho aparecem para todos**, mesmo sem permissão; só as linhas da lista no celular respeitam as permissões (2.1, 4.1).
2. **As abas Chamados, Financeiro e Cobranças dependem de módulo ou permissão** (portal do cliente; permissão e tela Financeiro; módulo de cobranças e conta de recebimento). Com a empresa de gravação em **teste**, todos os módulos ficam liberados (2.2, 2.3).
3. **"Novo Contato" fecha ao clicar fora** (no computador é um diálogo simples, diferente dos outros formulários, que ignoram clique fora), e o que foi digitado se perde. No celular vira gaveta (4.4, 7.1).
4. **WhatsApp do contato** abre `wa.me/55<número>` em outra aba; o app **sempre** coloca 55 na frente e não confere o tamanho. O item só aparece se o contato tem telefone (4.3, 11.3).
5. **Excluir documento** usa a caixa de confirmação do navegador (`window.confirm`), com aparência diferente dos demais diálogos (4.11).
6. **"Copiar link do portal" e "Abrir portal"** só aparecem com o módulo do portal e um portal ativo para o cliente; o QR do equipamento também depende do portal ativo (4.1, 6.8).
7. **O mapa e os botões "Abrir no Google Maps" e "Abrir no Waze"** só aparecem se o cliente tem endereço ou cidade e dependem de internet (4.3).
8. **A ficha carrega todas as OS, contratos e lançamentos da empresa** e filtra no navegador; numa empresa grande a abertura é mais lenta, e as abas Histórico, Tarefas e Chamados saem desse mesmo carregamento (4.2, 12.2).

### 14.4 Fornecedores

1. **Não há consulta de CNPJ, máscara nem validação** no cadastro de fornecedor: tudo é texto livre. A trilha atual nem cita Fornecedores, então vale dizer isso na narração (0.2, 5.5).
2. **O botão "Salvar" pula a validação nativa de e-mail**; só o Enter dentro do formulário valida o formato (5.5).
3. **No celular** o texto do estado vazio diz `Toque em "Novo Fornecedor"`, mas o botão se chama só "Fornecedor" (5.3).
4. **Excluir fornecedor é definitivo** e apaga junto as cotações e ordens de compra dele; o diálogo avisa (5.6, 13.2).
5. **A aba Fornecedores não muda o endereço** do navegador: continua `/clientes`, e recarregar volta para "Clientes" (5.1).
6. **"Histórico de Gastos" fica vazio** ("Nenhum gasto registrado") enquanto não houver despesa lançada no Financeiro com este fornecedor; a ficha é somente leitura (5.4, 11.5).

### 14.5 Equipamentos

1. **Chaves cruas na validação.** "Cliente \*" e "Nome \*" vazios mostram `customer_required` e `name_required` na tela. Não narre "aparece a mensagem de campo obrigatório" para esses dois (6.3).
2. **Se a empresa tiver um único cliente cadastrado**, ele já vem escolhido em "Cliente \*" (6.3). Numa empresa de demonstração com um cliente só, não há o que escolher na lista; com zero clientes, o campo começa vazio e o "+" é o caminho.
3. **"Categoria" só aparece no formulário se já existir alguma categoria.** Crie as categorias antes de gravar o cadastro do equipamento; não dá para criá-las dentro do formulário (6.3, 6.6).
4. **O identificador é gerado pelo servidor** ("0001", "0002"...) e o número é gasto mesmo que o equipamento seja apagado depois. O campo na janela é só leitura (6.3, 13.3).
5. **O status não tem controle**: todo equipamento nasce "Ativo" (6.7).
6. **Criação rápida de cliente.** O subtítulo diz "Preencha os dados mínimos para criar e já cobrar o cliente." (a janela é compartilhada com o Financeiro). O campo de busca do "Cliente \*" guarda o último texto digitado como Nome do cliente rápido, mesmo depois de escolher outro cliente (6.4, 7.7).
7. **Campos padrão não são fixos.** "Marca", "Modelo" etc. são linhas de "Configurar Campos": podem ter sido renomeadas, ocultas ou apagadas. Uma migração antiga ocultou "Data de Instalação" nas empresas que já tinham a configuração; empresas novas nascem com ela visível. Confira a empresa de gravação antes (6.5, 15).
8. **"Configurar Campos" salva sozinho**, ao sair do campo ou a cada clique, sem botão Salvar. O Nome do campo é uma área de texto: **Enter pula linha** e não grava (6.5).
9. **Em uma lista de opções que já existe**, o botão "Adicionar opção" não acrescenta caixa, e apagar o texto de uma opção a remove na hora. A caixa nova só funciona ao **criar** o campo (a confirmar) (6.5).
10. **O botão "Configurar Campos" aparece para todos** no computador, mas só administrador e gestor gravam. Para os demais, criar campo mostra "Erro ao criar campo" com "Você não tem permissão para realizar esta ação."; editar provavelmente mostra "Erro ao atualizar campo" com "Registro não encontrado."; excluir pode mostrar "Campo excluído!" sem apagar nada (a confirmar). Grave com um administrador (2.1, 6.5, 13.4).
11. **Falha ao salvar o equipamento.** Cadastro novo com erro mostra "Erro ao criar equipamento" e logo "Erro ao salvar equipamento" (só o segundo fica visível, com a mensagem crua do servidor) e a janela continua aberta. Na edição pela ficha sai só o "Erro ao salvar equipamento", também com a janela aberta; na edição pela lista ou pela aba do cliente o erro vira "Erro ao atualizar" e a janela fecha mesmo assim (6.3).
12. **A ficha não segue a configuração dos campos padrão.** Ela usa rótulos fixos: renomear "Marca" em Configurar Campos não muda a ficha; "Capacidade/Especificação" aparece como **"Descrição"**; um campo padrão oculto no formulário **ainda aparece na ficha se tiver valor** (6.5, 6.7).
13. **Campo personalizado Sim/Não**: a ficha mostra "Sim" mesmo quando o valor é "Não", porque o valor `nao` conta como "tem valor". Evite esse tipo na demonstração ou escolha "Sim" (6.7).
14. **Apagar o último valor personalizado** de um equipamento e salvar não limpa nada: quando não sobra valor, a chave `custom_fields` deixa de ir ao servidor (6.3, 12.5).
15. **Datas na ficha podem aparecer um dia antes** (Data de Instalação, Garantia até e campos de data personalizados) por causa do fuso; o seletor de data do formulário lê a data certa. Teste na máquina de gravação (6.7, 7.5, 15).
16. **Editar pela ficha recarrega a página inteira**, sem aviso. **Excluir pela ficha** não mostra erro nem atualiza a lista em memória: se o banco recusar (contrato vinculado), a pessoa volta para a lista e o equipamento continua lá, sem explicação. No computador a lista não tem "Editar"/"Excluir" por linha; para ver a mensagem de bloqueio, exclua pela aba "Equipamentos" da ficha do cliente (ou, no celular, pelo menu da linha) (6.2, 6.10).
17. **Equipamento de cliente excluído** continua listado; uma **OS com vários equipamentos** só aparece no histórico do primeiro (6.7, 6.10).
18. **QR Code.** Sem portal ativo vira o texto `EQ-0001`, os botões de link ficam desligados com "Cliente sem portal ativo" e o item "QR Code" some da etiqueta. Todo cliente novo nasce com portal ativo, mas um portal desligado quebra o QR (6.8).
19. **Etiqueta.** A pré-visualização **não mostra** os rótulos "Marca", "Modelo"... que a impressão mostra; tamanho com vírgula ("5,5") vira 5; **"Imprimir" não faz nada e não avisa** se o navegador bloquear janelas; as escolhas valem para todos os equipamentos e ficam no navegador (6.8).
20. **Anexos.** Excluir remove só o registro, o arquivo fica no armazenamento; os ícones de baixar e excluir da **Galeria** só aparecem ao passar o mouse (no celular use a Lista); o que for anexado fica visível no portal do cliente por padrão (6.7).
21. **A busca da lista não procura pelo Nº de série** (só nome, identificador, cliente, categoria, marca, modelo e local) (6.2).
22. **No celular, a Grade não tem Editar nem Excluir**; use a Lista (6.2).

### 14.6 Comportamento geral das janelas e avisos

1. **Um aviso por vez**, que some em cerca de 5 s (deduzido). Dois avisos seguidos mostram só o último; a narração deve esperar o aviso certo aparecer antes de ler a frase (7.6).
2. **Janelas de formulário não fecham ao clicar fora.** Fecham pelo botão "Fechar" (X), pelos botões do rodapé, pela tecla Esc (computador) ou arrastando a alça (celular); a exceção é "Novo Contato". O botão "Fechar" aparece escrito **FECHAR** por causa do estilo (7.1).
3. **Abaixo de 1024 px (celular e tablet)** as janelas viram painéis que sobem de baixo, a lista vira cartões com ações por deslize e a ficha ocupa a tela toda. Uma janela de gravação estreita já cai no layout de celular (7.1, 7.3, 10).
4. **Exclusão de origem não pede confirmação**, e a de tarefa do equipamento também não; a de documento pede, mas pela caixa do navegador (3.9, 6.7, 4.11).
5. **Sem internet** não funcionam: consulta de CNPJ, sugestões de endereço, lista de cidades, mapa e, no servidor, a busca de CEP. Grave com rede estável ou com esses serviços simulados (12.7).
6. **As listas recarregam quando a janela do navegador volta ao foco**, então um cliente ou equipamento criado em outra aba aparece sozinho (12.0).

---

## 15. Dúvidas em aberto e itens "(a confirmar)"

Nada foi executado: tudo vem do código lido em `/home/claude/kaikbarreto/dominextecnologia` (versão 1.37.56). O que segue só se resolve vendo a tela ou o banco real.

1. **Nenhuma confirmação visual.** Rótulos, textos e comportamentos foram lidos dos arquivos de mensagens e dos componentes. Posição exata de botões e aparência (por exemplo cor do "Fechar", tamanho do QR) não foram vistos.
2. **Módulos e permissões da empresa de gravação.** As abas Chamados, Cobranças e Financeiro da ficha do cliente, o filtro e o campo "Atende como" (PDV) e a ação do CRM só aparecem com o módulo ligado; com a empresa em teste (`subscription_status = 'testing'`) tudo aparece (2.3). Confirmar o estado da empresa, o papel do usuário (administrador?) e se há registro em `user_permissions`.
3. **Campos de equipamento da empresa de gravação.** Se "Data de Instalação" ficou **oculta** (a migração `20260228194044_0c2eea47-6d96-4303-bd6c-085160a42a50.sql` ocultou esse campo nas linhas que existiam; empresas novas nascem com os seis campos visíveis pela migração `20260906190100_seed_equipment_field_config_por_empresa.sql`), se os nomes foram alterados e se já existem campos personalizados.
4. **Janela de impressão.** O comportamento de "Imprimir" (nova aba e impressão do navegador, bloqueio de pop-up) e o dimensionamento "tamanho real" dependem do navegador e da impressora da gravação; no celular, a impressão não foi analisada.
5. **Serviços da internet.** BrasilAPI (CNPJ), ViaCEP (pela função `cep-lookup`), Nominatim e IBGE exigem rede ou simulação. **O formato real de resposta da BrasilAPI não foi conferido ao vivo** (a rede da análise bloqueou o domínio); os campos citados em 12.7 são os que o código lê. Também não foi confirmado como a BrasilAPI responde a um CNPJ com dígito verificador errado (o app trata qualquer status diferente de 2xx como "CNPJ não encontrado na Receita") nem se ela libera CORS para o endereço da gravação (sem isso o aviso seria "Não foi possível consultar o CNPJ agora").
6. **Aviso "CEP não encontrado".** Pela leitura, a função de servidor responde 404 e o app mostra "Erro ao buscar CEP"; confirmar na prática qual dos dois sai (3.5.2, 12.7).
7. **Exclusão de equipamento com contrato.** `contract_items.equipment_id` não define regra de exclusão em nenhuma migração, então o banco deve recusar; o **nome real da restrição** e a mensagem que chega ao usuário (genérica pelo código `23503`, ou a específica do equipamento) precisam ser conferidos no banco real (6.10, 12.0).
8. **"Adicionar opção" numa lista já existente.** Pelo código a caixa nova some na hora porque a tela filtra opções vazias antes de gravar; confirmar na tela (6.5).
9. **Datas na ficha do equipamento um dia antes.** Depende do fuso do navegador de gravação (6.7).
10. **Duração do aviso (toast).** Deduzida do padrão da biblioteca (cerca de 5 s); nenhuma tela define outro tempo (7.6).
11. **Momento das consultas de origens e formulários de captação.** Pela leitura, `customer_origins` e `lead_capture_forms` são consultadas ao abrir `/clientes`, mesmo com as janelas fechadas; confirmar no Network (12.1).
12. **Linha de cliente no computador com PDV.** Se a lista mostra a etiqueta Serviço/Loja na linha quando o módulo PDV está ligado (3.2).
13. **Aba Estoque da ficha.** Quem cria a linha de `stocks` do cliente (a RPC de cadastro de material ou outro caminho) não foi investigado; sem linha a aba mostra a lista vazia (12.2).
14. **Políticas de acesso (RLS) de `customers`, `equipment` e demais tabelas.** Só foram lidas as de `suppliers`, `equipment_categories`, `customer_origins`, `equipment_field_config` e as regras das RPCs do portal; o isolamento por empresa das outras foi presumido (13.4).
15. **Usuário com `fn:create_customer` e sem `fn:edit_customer`.** Como as RPCs do portal exigem `fn:edit_customer` de quem tem registro em `user_permissions`, ele cria o cliente, recebe o erro de permissão ao final e a janela fica aberta; confirmar com um usuário assim (13.1, 13.4). Usuário sem registro em `user_permissions` passa em qualquer conferência.
16. **Usuário sem permissão de gestão do sistema** criando, editando ou excluindo categoria, origem ou campo de equipamento: criar dá erro de política (`42501`); editar e excluir, pelo comportamento padrão do PostgreSQL, não encontram a linha, e o aviso pode ser "Registro não encontrado." (campos e categorias) ou um sucesso aparente na exclusão. Deduzido, não testado (6.5, 13.4).
17. **Mensagem crua em "Erro ao salvar equipamento".** A janela mostra `error.message` quando o erro é uma instância de `Error` e "Não foi possível salvar o equipamento." caso contrário. Deduzo que o erro do PostgREST na versão 2.93.3 de `@supabase/postgrest-js` (`package-lock.json`) seja um `Error`, mas não confirmei (6.3).
18. **Janelas antigas sem uso.** `EquipmentDetailDialog` e `EquipmentCategoryManagerDialog` existem no código mas nenhuma tela as abre (a trilha antiga pode ter vindo delas); o interruptor "Mostrar anexos no portal do cliente" só existe na primeira.
19. **Importar e exportar.** Não há importação de planilha nem exportação nestas telas. A cópia de segurança em Excel fica em Configurações, aba Empresa, cartão "Exportar meus dados" (clientes e equipamentos entram; **fornecedores não**) (8.1).
20. **Versão.** Tudo vale para a versão 1.37.56 do aplicativo; se o código mudar antes da gravação, rever principalmente as seções 6.3 a 6.8 e 12.
