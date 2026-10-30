# Inventário funcional · T18 — Área do Técnico: Refrigeração e Climatização (Dominex)

> Base para o roteiro do tutorial "T18 · Área do Técnico: Refrigeração e Climatização" da Domiflix. Levantado em
> 30/10/2026 contra o código publicado `APP_VERSION = "1.38.6"` (`src/config/version.ts:1`), cópia em
> `/home/claude/domiflix/src-1.38.6`. **Análise estática, somente leitura**: nada foi executado no app, mas as contas
> das ferramentas foram rodadas com as próprias funções do app (`lib/*.ts`) para dar exemplos conferidos. O que só se
> confirma com o app rodando está marcado "(a confirmar)" e repetido na seção 7.
> Fonte escrita secundária: a trilha validada na 1.22.5 (`_referencia/trilha-de-tutoriais_v1.22.5.md`, T18). Não existe
> seção do Guia Técnico só desta aula (`docs/guia-tecnico/secoes/` vai de T0 a T17); o Guia só cita a Área do Técnico
> de passagem (T7). **Onde a trilha e o código divergem, vale o código.**

## Como ler

- Caminhos relativos a `src/`, exceto os que começam com `supabase/`, `docs/` ou `rec/`. Formato `arquivo:linha`.
- Texto entre aspas "assim" é o rótulo exato da tela (pt-br). Fonte principal: `lib/i18n/messages/app/technicianTools.ts`
  (bloco pt-br, linhas 12-701) e `lib/i18n/messages/app/os.ts:1151-1155` (título, "Início", "Voltar"). Alguns textos são
  fixos no componente ou em `lib/` e estão citados onde aparecem.
- "Desktop" = janela de 1024 px ou mais. "Tenant" = a empresa cliente (aqui, Glacial Cold Brasil, segmento
  Refrigeração e Climatização).
- Componentes compartilhados (janelas, toasts) estão no inventário do T3. Fora deste tutorial: TI/assistência
  (Calculadora de Fonte, Conversor de Armazenamento, Laudo Técnico) e a ferramenta de Estética Automotiva, que usam a
  mesma tela mas têm aula própria quando forem publicadas; o fluxo da OS em campo é o T7.
- **Exemplos numéricos** ("conferido") foram calculados com `lib/cargaTermica.ts`, `lib/capacitor.ts`,
  `lib/caboEletrico.ts`, `lib/refrigerantes.ts` e `lib/conversoes.ts` do código 1.38.6.

---

## 0. Resumo para quem escreve o roteiro

### 0.1 Capítulos da trilha (T18, v1.22.5) contra o código de hoje

| # | Capítulo da trilha | Situação | O que ajustar |
|---|---|---|---|
| 1 | Por que a Área do Técnico muda conforme o segmento | **Bate** | O segmento vem de `company_settings.segment` e **não se troca em Configurações** (só lê: T1). Hoje 3 segmentos têm ferramentas reais: Refrigeração e Climatização (10), Estética Automotiva (1, só Diluição) e Assistência Técnica TI (3) (`config/technicianArea.ts:91-196`). Os outros nichos aparecem como prévia bloqueada (seção 3.13). |
| 2 | Visão geral do hub e acesso dentro e fora da OS | **Bate, com detalhes** | Fora da OS: item **"Área do Técnico™"** do menu (grupo Operacional) abre `/area-tecnico`. Dentro da OS do técnico: botão flutuante no canto inferior esquerdo abre as mesmas ferramentas em tela cheia, com o botão vermelho "Voltar para OS" (`pages/TechnicianOS.tsx:4942-5004`). O hub "Início" tem **cartões das ferramentas** e o glossário **"Termos Técnicos Explicados"** (seção 3.2). |
| 3 | **Catálogo**: modelos, capacidades e códigos de erro | **Bate, bem maior que a frase** | São **5 subabas**: "Ar Condicionado", "Compressores", "Linha Branca", "Controles Remotos" e "Fluidos Refrigerantes" (`Catalogo.tsx:320-326`), com busca por marca, equipamento ou código de erro, filtros, ficha técnica, consumo de energia e manuais. Os dados vêm do **banco global** (não são da empresa). |
| 4 | **Carga Térmica** | **Bate** | 6 campos + "Ambiente ensolarado?" + resultado ao vivo com chave **BTU ↔ TR**. A mesma ferramenta abre dentro do **contrato PMOC** (botão Calcular do ambiente, "Usar resultado"). |
| 5 | **Conversão** | **Bate** | 4 categorias (Pressão, Temperatura, Potência, Comprimento), atalhos "Mais usadas" e estrela **"Favoritas"**. HP ↔ BTU/h tem **dois modos** ("Refrigeração" 9.000 BTU/h por HP e "Energia" 2.544). |
| 6 | **Cálculo de Capacitor** | **Bate, ampliado** | Monofásico (por BTU ou pelo LRA da etiqueta) **e trifásico** (contator + relé térmico, sem capacitor). |
| 7 | **Cabo Elétrico** | **Bate** | Bitola do cabo, disjuntor (curva C), tipo e queda de tensão, com foto do disjuntor. |
| 8 | **Superaquecimento e sub-resfriamento** | **Bate, ampliado** | Duas subabas "Superaquecimento (SH)" e "Subresfriamento (SC)", **escolha de modelo/fabricante** (11 opções com faixa-alvo própria) e 13 gases. O rótulo "sub-resfriamento" da trilha é "Subresfriamento" na tela. |
| 9 | **Régua de Gases** | **Bate** | Régua vertical de −40 a +60 °C, digita temperatura **ou** pressão, escolhe gás, fórmula (vapor/líquido) e unidade. |
| 10 | **Retrofit de Gás** | **Bate** | Gás atual: R-22, R-404A, R-12 ou R-502; mostra substitutos com selo "Mais indicado", óleo, pressão e cuidados. |
| 11 | **Ciclo de Refrigeração** | **Bate** | Chave "Ilustração" × "Imagem 2D" + "Termos do ciclo" (12). |
| 12 | **Diluição de Produto e histórico dos cálculos** | **Parcial: o "histórico" não existe** | Diluição bate. **Não há histórico de cálculos.** O que existe: os campos **lembram o último valor** enquanto a aba do navegador ficar aberta (`hooks/usePersistedState.ts:16-42`), "Favoritas" só na Conversão e uma estrela de favorito no modelo do Catálogo que não lista em lugar nenhum (seção 5, P3). |
| ⚠️ | Aula exclusiva de Refrigeração e Climatização | **Bate** | O menu e a rota liberam para qualquer segmento com ferramentas (3), mas só Refrigeração tem as 10 ferramentas e o glossário (`Inicio.tsx:79,167`). |
| ⚠️ | Lista vem do segmento; outros como prévia bloqueada | **Bate** | Prévia = itens com cadeado + cartão "Ferramentas de …" com botão de WhatsApp (seção 3.13). |
| ⚠️ | Não substitui o preenchimento da OS | **Bate** | Todas as ferramentas terminam com o aviso "Ferramenta de apoio…" (`ToolDisclaimer`). |

### 0.2 O que mudou desde a 1.22.5 (Changelog do app, `pages/Changelog.tsx`)

**Nada novo nas ferramentas.** A busca no Changelog por Área do Técnico, Catálogo, Superaquecimento, Régua, Retrofit,
Carga Térmica, Capacitor, Cabo, Diluição, Conversão, Ciclo, gases, BTU, calculadora e segmento só acha entradas
**anteriores** à 1.22.5 (04/09/2026, `Changelog.tsx:4609`): as ferramentas nasceram na 1.12.0 (13/06/2026,
`Changelog.tsx:8609`) e o Catálogo cresceu até a 1.17.43 (27/07/2026, `Changelog.tsx:5566`, tradução para en/es/fr) e a
1.21.15 (23/08/2026, `Changelog.tsx:5023`, ferramentas de TI). Depois da 1.22.5 só há menções de passagem
(1.31.8, `Changelog.tsx:2041`, proposta comercial; 1.37.2, `Changelog.tsx:1093`, lista de OS).

Pontos do Changelog antigo que **não valem mais no código de hoje** (importante para o roteiro não repetir):

| Entrada | O que diz | Código 1.38.6 |
|---|---|---|
| 1.12.7 (`Changelog.tsx:8515`) | "tela inicial mostra seus **Favoritos** e itens **Recentes**" | O Início **não tem** essa seção (`components/technician-area/Inicio.tsx`, 237 linhas, só cartões + glossário). Os "Recentes" ainda são gravados (`lib/technicianAreaHistory.ts:90-100`) mas nunca exibidos. |
| 1.12.29 / 1.12.31 (`Changelog.tsx:8226,8197`) | Retrofit "dentro da Conversão" | Desde a 1.12.50 (`Changelog.tsx:7884`) é **ferramenta própria**, "Retrofit de Gás". |
| 1.14.48 (`Changelog.tsx:6738`) | "Ferramentas do Técnico" virou "Área do Técnico™" | Nome atual na tela: **"Área do Técnico™"**; o endereço antigo `/ferramentas-tecnico` redireciona (`App.tsx:890`). |

Entradas antigas que **continuam valendo** e ajudam a roteirizar: seletor de segmento ao lado do título (1.13.9,
`Changelog.tsx:7683`); o que se digita não se perde ao trocar de ferramenta (1.12.37, `Changelog.tsx:8095`); aviso de
gás inflamável (1.12.30, `Changelog.tsx:8209`); consumo de energia no Catálogo (1.12.29, `Changelog.tsx:8221`); foto
ampliável do capacitor, da contatora e do disjuntor (1.13.15, `Changelog.tsx:7527`); botão da OS (1.12.1,
`Changelog.tsx:8592`).

### 0.3 O que mais pode surpreender (detalhes na seção 5)

1. **Sem histórico e sem "Recentes"**: a trilha fala em "histórico dos cálculos"; no código só existe memória de sessão.
2. **O Catálogo depende de dados no banco global** (marcas, modelos, códigos, fichas, gases). Sem eles a tela mostra
   "Catálogo em atualização". No backend falso de gravação **não há nenhuma semente disso** (seção 4).
3. **A Área do Técnico não pede internet para calcular, mas o app precisa dela para abrir**: o segmento vem do banco e o
   Catálogo é consulta online (`vite.config.ts:73-78`, REST nunca é guardado). Não prometer "funciona offline".
4. **"Baixar manual" baixa um arquivo** e, se falhar, abre outra aba (`Catalogo.tsx:292-308`); "Falar com representante"
   abre o WhatsApp da Dominex em outra aba (`SegmentLockedScreen.tsx:31-37`). Nenhum dos dois cabe no gravador atual.
5. **Rótulos que enganam**: a chave de tensão diz "110v" mas a conta do cabo usa 127 V, e a do capacitor usa 110 V
   (seção 5, P6); "Imagem 2D" do ciclo troca por tema claro/escuro e por celular/computador.
6. **Início do segmento "Refrigeração" tem 42 termos de glossário** em 4 grupos, com busca; é a parte mais longa da tela.

---

## 1. Rotas e navegação

| Endereço (pt-br) | O que abre | Código |
|---|---|---|
| `/area-tecnico` | Hub "Início" (cartões + glossário). Tradução do endereço: en `/technician-area`, es `/area-tecnico`, fr `/espace-technicien` | `App.tsx:888`, `lib/i18n/appRouteSlugs.ts:72,188` |
| `/area-tecnico/<ferramenta>` | A ferramenta. Slugs: `catalogo`, `carga-termica`, `conversao`, `calculo-capacitor`, `cabo-eletrico`, `superaquecimento`, `regua-gases`, `retrofit-gas`, `ciclo-refrigeracao`, `diluicao-produto` (mais 3 de TI) | `pages/TechnicianArea.tsx:71-85` |
| `/area-tecnico/catalogo/<subaba>` | Subabas `ar_condicionado` (padrão), `compressor`, `linha_branca`, `controle_remoto`, `fluido_refrigerante` | `Catalogo.tsx:397,451-473` |
| `.../catalogo/<subaba>/marca/<marca>` | Modelos de uma marca (o endereço leva o nome da marca em "slug") | `Catalogo.tsx:459` |
| `.../marca/<marca>/modelo/<modelo>` | Códigos de erro (AC e linha branca) ou ficha do compressor | `Catalogo.tsx:463` |
| `.../catalogo/controle_remoto/modelo/<modelo>` | Detalhes do controle remoto (sem etapa de marca) | `Catalogo.tsx:468` |
| `.../catalogo/fluido_refrigerante/gas/<código>` | Detalhe do fluido | `Catalogo.tsx:470` |
| `/area-tecnico?nicho=<segmento>` | Prévia bloqueada de outro nicho (o seletor de nicho grava isso no endereço) | `TechnicianArea.tsx:350,378-382` |
| `/area-tecnico/conversao?cat=…&de=…&para=…` | Abre a Conversão já num par (categoria `pressao`, `temperatura`, `potencia`, `comprimento`) | `TechnicianArea.tsx:497-505` |
| `/ferramentas-tecnico/*` | Endereço antigo; redireciona preservando o resto | `App.tsx:408-427,890` |
| Slug desconhecido | Volta ao hub (`replace`) | `TechnicianArea.tsx:417,470-477` |

- **Dois modos da mesma tela** (`TechnicianArea.tsx:109-114`): **rota** (acima) e **embutido** (`embedded`, dentro da OS
  do técnico). No embutido **não existe URL das ferramentas**: a navegação é por estado e o endereço continua
  `/os-tecnico/:id` (`TechnicianArea.tsx:575-649`).
- **Como se chega:** Menu lateral (item solto logo depois do grupo "Operacional",
  `components/layout/SidebarMenuContent.tsx:107`); **Menu superior** (dentro de "Operacional",
  `components/layout/TopNavbar.tsx:94`); menu do celular "Mais" (`components/layout/MoreMenuDrawer.tsx:93`); botão
  flutuante na OS do técnico (seção 3.14).
- Título no menu: **"Área do Técnico™"** (`shell.ts:34`); mensagem de carregamento "Abrindo ferramentas..."
  (`hooks/useRouteLoadingMessage.ts:46`).
- Barra lateral das ferramentas (desktop, 224 px) com ícone e nome de cada uma; no **celular** a barra vira abas
  sublinhadas e **só aparece fora do Início** (`TechnicianArea.tsx:266-282`); no Início do celular a navegação é pelos
  cartões em carrossel (`Inicio.tsx:106-132`).
- Botão **"Voltar"** (seta + texto) no topo de cada ferramenta leva ao Início; no Catálogo ele só aparece na raiz de uma
  subaba (dentro de marca/modelo o Catálogo tem o próprio voltar) (`TechnicianArea.tsx:482-492`, `TOOLS_WITH_OWN_BACK`
  em `:50`).

---

## 2. Permissões e módulos

| Quem / o quê | Regra | Código |
|---|---|---|
| Ver o item de menu e abrir a rota | Permissão de tela `screen:technician_tools` ("Área do Técnico™", grupo Operacional: "Ferramentas de apoio do técnico em campo, como cálculos e tabelas.") **e** segmento da empresa com ferramentas | `hooks/usePermissions.ts:68`, `App.tsx:888`, `SidebarMenuContent.tsx:107,318` |
| Segmento sem ferramentas (ex.: Instalações Elétricas, "Outro") | Item some do menu lateral e do "Mais"; abrir o endereço redireciona para `/` | `App.tsx:396-405`, `MoreMenuDrawer.tsx:336` |
| Módulo pago | **Nenhum.** Não há `moduleKey` na rota nem no menu; a "exclusividade" é só o segmento | `config/technicianArea.ts:91-196` |
| Botão flutuante dentro da OS | Só quando `company_settings.segment === 'refrigeracao'` (igualdade exata, não o registro) | `pages/TechnicianOS.tsx:991-994` |
| Quem muda o segmento | Ninguém na empresa: Configurações mostra só leitura ("Para alterar, fale com a Dominex", T1) | `pages/Settings.tsx:866-884` |
| Dados do Catálogo | Leitura para qualquer usuário logado de qualquer empresa; escrita só `super_admin` | `supabase/migrations/20260613190000_equipment_reference_catalog.sql:97-131` |
| Fotos do Catálogo | Bucket público `equipment-catalog` (leitura sem login; escrita `super_admin`) | `supabase/migrations/20260614210000_equipment_catalog_storage_bucket.sql:12-24` |

- A permissão `screen:technician_tools` **não está em nenhum cargo pronto do banco** (nenhuma migração a cita). Por isso:
  administrador/gestor e usuário em "modo legado" (sem linhas em `user_permissions`) veem; técnico com permissão
  personalizada só vê se a tela "Área do Técnico™" estiver marcada (o legado é o achado nº 2 de `TRILHA.md`).
- Idiomas: nomes de ferramenta, textos e endereço existem em pt-br, en, es e fr (`technicianTools.ts:12,702`). A
  gravação é em pt-br.

---

## 3. Por tela / janela / aba

### 3.1 Cabeçalho comum e navegação (`pages/TechnicianArea.tsx:177-338`)

| Elemento | Rótulo / comportamento | Código |
|---|---|---|
| Ícone + título | Ícone de ferramenta e **"Área do Técnico™"** | `TechnicianArea.tsx:203-226`, `os.ts:1152` |
| Selo do nicho | Selo colorido com o nicho da empresa (ex.: "Refrigeração e Climatização", ciano `#06b6d4`) e seta; **clicar abre a lista de nichos** | `SegmentToolsSwitcher.tsx:58-75`, `utils/companySegments.ts:44` |
| Lista de nichos | Janelinha com busca **"Buscar nicho..."**; o da empresa vem primeiro com a marca **"Incluído"** e um ✓; vazio: "Nenhum nicho encontrado." São 10 nichos (os que têm página no site) | `SegmentToolsSwitcher.tsx:46-53,81-127`, `technicianTools.ts:28-30` |
| Menu lateral (desktop) | "Início" + as 10 ferramentas; a ativa fica na cor principal do sistema; no nicho bloqueado cada item tem cadeado | `TechnicianArea.tsx:285-312` |
| Abas (celular) | Mesmos itens, sublinhadas, rolagem horizontal; aparecem quando uma ferramenta está aberta ou o nicho está bloqueado | `TechnicianArea.tsx:266-282` |
| "Voltar" | Seta + "Voltar" (`os.ts:1154`) | `TechnicianArea.tsx:320-331` |
| Aviso de rodapé | Frase cinza no fim de cada ferramenta, ex.: "Ferramenta de apoio. Os valores são estimativas de referência — confira sempre a placa do equipamento, os manuais do fabricante e as normas técnicas aplicáveis antes de executar." | `ToolDisclaimer.tsx`, `technicianTools.ts:483-486` |

Ordem do menu lateral (rótulos do registro, `config/technicianArea.ts:93-162`): **Início**, **Catálogo**, **Carga Térmica**,
**Conversão**, **Cálculo de Capacitor**, **Cabo Elétrico**, **Superaquecimento**, **Régua de Gases**, **Retrofit de Gás**,
**Ciclo de Refrigeração**, **Diluição de Produto**.

### 3.2 Início (hub) (`components/technician-area/Inicio.tsx`)

- **"Ferramentas"** / "Escolha uma ferramenta para começar." (`technicianTools.ts:15-16`). Dez **cartões coloridos**, cada
  um com ícone, nome e descrição (`config/technicianArea.ts:93-162`):

  | Cartão | Descrição no cartão |
  |---|---|
  | Catálogo | "Consulte modelos, capacidades e códigos de erro." |
  | Carga Térmica | "Calcule os BTUs ideais para o ambiente." |
  | Conversão | "Converta pressão, temperatura, potência e medidas." |
  | Cálculo de Capacitor | "Encontre o capacitor certo pelo BTU e tensão." |
  | Cabo Elétrico | "Bitola do cabo e disjuntor pelo BTU, tensão e distância." |
  | Superaquecimento | "Calcule SH e SC pela pressão e temperatura." |
  | Régua de Gases | "Pressão de saturação dos gases por temperatura." |
  | Retrofit de Gás | "Gases drop-in para trocar o refrigerante." |
  | Ciclo de Refrigeração | "Entenda o ciclo básico e os termos técnicos." |
  | Diluição de Produto | "Calcule produto + água pela proporção e volume final." |

  Desktop: grade de 2 colunas (4 em tela larga, `xl`) com seta que anda no passar do mouse (`Inicio.tsx:135-163`);
  celular: carrossel horizontal de cartões coloridos (`Inicio.tsx:106-132`).
- **"Termos Técnicos Explicados"** (só Refrigeração): "Não entendeu uma sigla ou unidade? Busque e veja em linguagem
  simples." Busca **"Buscar termo (ex: BTU, capacitor, pressão)"**; vazio: "Nenhum termo encontrado." Quatro grupos com
  barrinha verde e acordeão (um aberto por vez): **"Medidas e Unidades"** (15 termos, `lib/glossario.ts`), **"Ciclo
  Básico de Refrigeração"** (12, `lib/glossarioCiclo.ts`), **"Elétrica e Instalação"** (8, `lib/glossarioEletrica.ts`),
  **"Gases e Nomenclatura"** (7, `lib/glossarioGases.ts`). Cada termo abre descrição e, às vezes, "Exemplo: …"
  (`Inicio.tsx:167-234`, `technicianTools.ts:19-26`).
- Primeiros termos (para câmera): "BTU / BTU/h", "Carga térmica", "Capacitor (µF — microfarad)", "Tensão do capacitor (380v
  / 440v)" (`lib/glossario.ts:23-45`).

### 3.3 Catálogo (`components/technician-area/Catalogo.tsx`, 3.044 linhas)

**Estrutura.** Título **"Catálogo - <subaba>"** (ex.: "Catálogo - Ar Condicionado", `Catalogo.tsx:333-336,1102`) e subtítulo que muda com a subaba. Linha de abas sublinhadas com ícone (`Catalogo.tsx:350-403`):
**"Ar Condicionado"**, **"Compressores"**, **"Linha Branca"**, **"Controles Remotos"**, **"Fluidos Refrigerantes"**
(`technicianTools.ts:36-42`). Padrão ao abrir: Ar Condicionado (`Catalogo.tsx:397`). Aviso final: "Conteúdo de apoio.
Capacidades, consumo e códigos podem variar por versão — confira sempre a placa do equipamento, os manuais do fabricante e
as normas técnicas aplicáveis antes de executar." (`technicianTools.ts:144`).

**Subaba "Ar Condicionado" e "Linha Branca" — grade de marcas** (`Catalogo.tsx:927-1326`):
- Cabeçalho: "Consulte modelos e códigos de erro." (com busca de código) e o selo verde **"N itens"**.
- Busca (atraso de 180 ms): **"Buscar por marca, equipamento ou código de erro"** (AC e linha branca); dica "Ou selecione
  uma marca para ver os modelos." Botão **"Filtros"** com contador; janela **"Filtros"** com os grupos **"Potência"**
  (BTUs achados no nome do modelo), **"Tipo"** (categorias) e, só no AC, **"Gás refrigerante"**; botões **"Limpar
  filtros"** e **"Ver resultados"** (`Catalogo.tsx:969,1136,1156-1200`). Os filtros só valem com a busca vazia.
- Grade de marcas, 2 colunas: cartão branco com o **logo** ou, sem logo, o **nome** em letra grande
  (`Catalogo.tsx:1288-1325`). Compressores: Gree, Embraco, LG e Samsung vêm primeiro; Linha Branca: Brastemp, Consul,
  Electrolux, LG e Samsung (`Catalogo.tsx:101-104,164-185`).
- Busca ativa: duas seções, **"Catálogo"** (modelos) e **"Códigos de Erro"** (códigos agrupados por código, mostrando em
  quantas máquinas acontece: "Máquina/Máquinas", "+N mais", "ver menos") (`Catalogo.tsx:1327-1421`).
- Vazios: "Catálogo em atualização" / "As marcas e modelos para consulta estão sendo cadastrados. Volte em breve.";
  "Nenhum resultado encontrado"; "Nenhum equipamento encontrado" (`technicianTools.ts:63-67`).

**Tela da marca** (`Catalogo.tsx:1422-1763`): faixa (carrossel) de marcas com setas **"Marca anterior"** / **"Próxima
marca"**; busca **"Buscar equipamento ou código..."**; "Filtros" igual; cartões de modelo em 2 colunas (desktop),
ordenados por BTU crescente (sem BTU no nome vão para o fim) (`Catalogo.tsx:215-235`).

**Cartão de modelo** (`Catalogo.tsx:2486-2755`): foto (toque amplia: "Ampliar foto de …"; sem foto: "Sem foto"), nome, selos
(BTU, tipo, gás com cor e chama se inflamável, "Cód.: …", "Câmara frigorífica"), bloco **"Consumo de energia"** (abaixo)
e dois botões: **"Códigos de erro"** (ou o texto "Códigos de Erro Indisponíveis") e **"Baixar manual"** (ou "Manual
Indisponível"). O rótulo do manual muda pelo tipo: "Manual de Instalação", "Manual de Serviço", "Manual do Usuário", "Guia
Rápido", "Datasheet", "Baixar Manual" (`technicianTools.ts:135-142`). Em Compressores o 1º botão é **"Ficha técnica"** e o
2º é do datasheet; em Controles Remotos o botão é **"Ver detalhes técnicos"** (`Catalogo.tsx:2474-2485`).

**Bloco "Consumo de energia"** (`Catalogo.tsx:2311-2473`): botão **"Ajustar"** abre **"Tarifa e uso"** com **"Tarifa
(R$/kWh)"** e **"Horas de uso por dia"** (controle deslizante) e **"Aplicar"**; mostra **"Por hora"** e **"Por mês"** em
kWh e em reais; "estimado · 8 h/dia" (ou "24 h/dia" para geladeira, freezer etc.); nota "Estimativa com base em dados
públicos da internet." Padrão: **R$ 0,90/kWh e 8 h/dia**, guardados **no aparelho** (`localStorage`
`catalogo-energia-config`) (`Catalogo.tsx:2185-2186,2232-2270`). Sem dado: "Consumo não informado".

**Tela "Códigos de erro"** (`Catalogo.tsx:2806-2967`): título "<modelo> - <marca>", estrela (favoritar), campo **"Informe o
código de erro no display"** com exemplo "Ex: E1, F0, P4...", bloco **"Instruções"** ("Digite o código exibido no painel
do equipamento para ver o diagnóstico. Você também pode percorrer a lista completa de códigos abaixo."), lista de códigos;
cada código abre **"Diagnóstico"** (passos), **"Solução"** e **"Componente:"**. Sem código achado: "Código não
encontrado" + frase fixa em português (P9). Vazio: "Sem códigos cadastrados".

**Subaba "Compressores"** → **"Ficha Técnica"** (`CompressorFicha.tsx`): foto, "Gás", chama se inflamável, linhas
"Capacidade", "Aplicação", "Tensão", "Frequência", "Deslocamento", "Capacitor de trabalho", "Capacitor de partida", "Relé /
Protetor", "Óleo", "Conexões", "Equivalências", "Observações" (`technicianTools.ts:165-186`); sem ficha: "Ficha em
atualização".

**Subaba "Controles Remotos"** (`Catalogo.tsx:1779-1957`, `RemoteConfig.tsx`): lista única (sem marca), busca **"Buscar por
marca ou controle"**, "N controles"; detalhe **"Detalhes Técnicos"** com seções **"Como configurar"**, **"Código
universal"**, **"Reset"**, **"Desbloqueio"**, **"Modos"**, **"Observações"**; sem dado: "Em atualização"
(`technicianTools.ts:187-201`).

**Subaba "Fluidos Refrigerantes"** (`Catalogo.tsx:1968-2175`, `GasDetail.tsx`): busca **"Buscar por código ou nome (ex:
R-410A)"**, "N fluidos"; duas seções **"Puros"** e **"Misturas (blends)"** (códigos que começam com R-4xx ou R-5xx vão
para blends, `Catalogo.tsx:1991`); cartão com cilindro na cor do gás, código, nome, selos de tipo e de classe de
segurança (chama âmbar/vermelha). Detalhe **"Fluido Refrigerante"**: "Composição", "Tipo", "GWP", "ODP", "Ponto de
ebulição", "Glide", "Classe de segurança", "Óleo", "Substitui", "Aplicação", "Observações" e botões **"Ficha técnica"** e
**"Guia do fabricante"** (`technicianTools.ts:147-164`).

### 3.4 Carga Térmica (`CargaTermica.tsx`, 191 linhas; conta em `lib/cargaTermica.ts`)

Título **"Carga Térmica"** / "Dimensione a capacidade em BTUs do ambiente." (`technicianTools.ts:263-283`). Campos
(placeholders entre parênteses): **"Altura (metros)"** (Ex: 2,8), **"Largura (metros)"** (Ex: 4), **"Comprimento
(metros)"** (Ex: 5), **"Quantidade de pessoas"** (Ex: 2), **"Eletroeletrônicos"** (Ex: 3), **"Janelas (2 x 1,5 metros)"**
(Ex: 1); chave **"Ambiente ensolarado?"** (Não / Sim). Cartão de resultado ao vivo (sem botão Calcular): chave **BTU ↔ TR**,
"Capacidade necessária" em número grande. Nota: "Recomenda-se não utilizar aparelhos de ar condicionado abaixo da
potência indicada." (BTU) ou "1 TR (Tonelada de Refrigeração) = 12.000 BTU/h. …" (TR). Só mostra valor depois de largura ×
comprimento > 0.
- Fórmula (`lib/cargaTermica.ts:15-71`): área × 600 BTU (sombra) ou × 800 (sol) + 600 por pessoa + 600 por eletrônico +
  janela 600 (sombra) ou 1.000 (sol) + 15% da base por metro acima de 3 m de pé-direito; arredonda para cima.
- **Conferido:** altura 2,8, largura 4, comprimento 5, 4 pessoas, 3 eletrônicos, 1 janela: **sombra 16.800 BTUs**
  (= 1,4 TR); **ensolarado 21.200 BTUs**. Com 2 pessoas: 15.600 e 20.000.
- Valores ficam guardados na sessão do navegador (P2). A mesma tela abre no **contrato PMOC** como janela, com o botão
  **"Usar resultado"** (devolve em TR) (`components/contracts/CargaTermicaCalculatorModal.tsx:18-35`, T11).

### 3.5 Conversão (`Conversao.tsx`, 602 linhas; unidades em `lib/conversoes.ts`)

Título **"Conversão"** / "Converta entre unidades de medida." Abas sublinhadas coloridas: **"Pressão"** (bar, psi, kPa, atm,
m.c.a), **"Temperatura"** (°C, °F, K), **"Potência"** (W, kW, HP, cv, BTU/h, TR) e **"Comprimento"** (mm, cm, m, pol, ft)
(`Conversao.tsx:90-96,161-176`, `lib/conversoes.ts:44-95`). Dois campos **"De"** e **"Para"** (valor + unidade), botão
**"Inverter unidades"**; digitar num lado converte no outro. Padrão: Pressão, 1 bar → psi. Bloco **"Mais usadas"** com 4
atalhos: **°C → °F**, **bar → psi**, **HP → BTU/h**, **mm → pol** (`Conversao.tsx:49-54`). Estrela **"Favoritar
conversão"** no cartão; lista **"Favoritas"** acima dos atalhos (cruza categorias) (`Conversao.tsx:317-395,562-590`),
guardada no aparelho (`tt:favoritos:conversao`, até 6, `technicianAreaHistory.ts:19-24`).
- **HP ↔ BTU/h**: aparece **"Modo de cálculo"** com **"Refrigeração"** (padrão: 1 HP ≈ 9.000 BTU/h) e **"Energia"** (1 HP =
  2.544 BTU/h); texto explicativo "Escolha o tipo de cálculo: …" (`Conversao.tsx:63,274,291-293,340-346`, `technicianTools.ts:343-347`).
- **Conferido:** 1 bar = 14,503774 psi; 35 °C = 95 °F; 1/4 pol = 6,35 mm; 3/8 pol = 9,525 mm. Evitar TR → BTU/h: dá
  "12.000,00129" (fator de TR com 6 casas, `lib/conversoes.ts:61`).

### 3.6 Cálculo de Capacitor (`CalculoCapacitor.tsx`, 580 linhas; contas em `lib/capacitor.ts`, `lib/contator.ts`)

Título **"Cálculo de Capacitor"**. Chave **"Fase"**: **"Monofásico"** (padrão) / **"Trifásico"** (`CalculoCapacitor.tsx:64,119-140`).
- **Monofásico.** Subtítulo "Capacitor recomendado pela fase, BTU/LRA e tensão." Chave **"Cálculo"**: **"Estimativa (BTU)"**
  (padrão) ou **"Preciso (LRA)"**. Em BTU: **"Selecione o BTU"** (7.000, 9.000, 12.000, 18.000, 22.000, 24.000, 30.000,
  36.000, 48.000, 60.000 ou **"Personalizado"**) e **"Selecione a tensão"** (chave 110V / 220V; padrão 220V)
  (`lib/capacitor.ts:12-18`, `CalculoCapacitor.tsx:145-190`). Em LRA: campo **"LRA (Locked Rotor Amps)"** com "Está na
  etiqueta do compressor (LRA)." Resultado **"Capacitor recomendado"**: "Use o capacitor de **N** µF" + "à 380/440v", "Amper",
  "Potência", e cartão com foto (ampliável) e especificações "Capacitância", "Tensão", "Tipo: Permanente (regime)"
  (`CalculoCapacitor.tsx:240-300`).
  - **Conferido (BTU):** 18.000 BTU, 220 V → **40 µF**, 8,38 A, 1.844 W. 12.000 BTU, 220 V → 25 µF, 5,36 A, 1.179 W.
    (Capacitor = valor comercial mais próximo de BTU ÷ 450; potência = BTU × 0,110778 − 150.) LRA 30 A → 31 µF.
- **Trifásico.** "Máquina trifásica não usa capacitor: dimensione contatora e relé térmico." Chave **"Entrada"**:
  **"Corrente (A)"** ("Corrente nominal (A) — do motor/compressor") ou **"Potência (CV)"**; chave **"Tensão trifásica"** 220V /
  380V; **"Parâmetros de placa (avançado)"** com **"Rendimento (η)"** e **"Fator de potência (cosφ)"** ("Padrões de placa WEG
  W22 premium"). Resultado **"Contator recomendado"**: "Contator de … A", "categoria AC-3", "Tripolar, para motor
  trifásico.", "Corrente nominal", "Corrente de emprego", **"Relé térmico:"** "regule para a corrente nominal do motor"
  (`CalculoCapacitor.tsx:315-580`, `technicianTools.ts:383-413`).
- Avisos de tela: "O cálculo por BTU é uma estimativa de mercado (média de potência dos 10 principais modelos de ar
  condicionado no Brasil); o modo Preciso usa o LRA da etiqueta do compressor." (`technicianTools.ts:414`).

### 3.7 Cabo Elétrico (`CaboEletrico.tsx`, 244 linhas; conta em `lib/caboEletrico.ts`)

Título **"Cabo Elétrico"** / "Seleção de seção do cabo elétrico para ar-condicionado em geral." Campos: **"Selecione a
capacidade (BTU)"** (127 V: 7.000 a 18.000; 220 V: 7.000 a 60.000; ou **"Personalizado"**), chave de tensão **"110v" /
"220v"** (padrão 220v), **"Distância do quadro elétrico (m)"** (`lib/caboEletrico.ts:20-25,48-52`, `CaboEletrico.tsx:38-44`).
Resultado **"É recomendado utilizar"**: "Cabo elétrico: **N mm²**", "Disjuntor: **N A**", "Tensão do AC:", "Corrente de projeto",
"Queda de tensão", e cartão **"Disjuntor recomendado"** com foto (bipolar ou monopolar) e "Tipo", "Curva" (sempre C),
"Corrente (In)", "Polos", "Tensão", "Padrão" (`CaboEletrico.tsx:151-240`, `technicianTools.ts:418-443`).
- Regra (`lib/caboEletrico.ts:186-250`): corrente de projeto = corrente nominal × 1,25; menor seção comercial que aguenta a
  corrente e a queda de tensão ≤ 2% (`lib/caboEletrico.ts:64`); disjuntor = menor comercial ≥ corrente de projeto e ≤ capacidade do cabo.
- **Conferido:** 18.000 BTU, 220 V, 20 m → **4 mm²**, **16 A**, bipolar, queda 1,4%. 12.000 BTU, 220 V, 15 m → 2,5 mm², 16 A,
  queda 1,3%. 36.000 BTU, 220 V, 30 m → 10 mm², 25 A.
- Avisos: "Valor estimado: BTU fora da faixa tabelada…", "Evite 127V acima de ~18.000 BTU…", "Distância muito grande para as
  seções disponíveis. Mostrando a maior seção (25 mm²)…" (`technicianTools.ts:430-432`).

### 3.8 Superaquecimento (`Superaquecimento.tsx`, 627 linhas; contas em `lib/refrigerantes.ts`, alvos em `lib/superaquecimentoModelos.ts`)

Título **"Superaquecimento e Subresfriamento"** / "Calcule SH e SC pela pressão e temperatura medidas em campo." Link
**"Ver o ciclo de refrigeração"** (vai para a ferramenta Ciclo). Abas **"Superaquecimento (SH)"** (padrão) e
**"Subresfriamento (SC)"**. Seleções comuns: **"Modelo / fabricante"** (padrão "Padrão — Usar esta caso desconheça o
modelo"; grupos "SPLIT HI-WALL", "PISO-TETO", "SPLITÃO / VRF"; **escolher o modelo já troca o gás sugerido**), **"Fluido
Refrigerante"** (padrão R-410A; seções sem título "Atuais", "Gases Legado (Antigos)", "Substitutos / Blends de retrofit") e
**"Unidade de pressão"** (chave psi / bar; padrão psi) (`Superaquecimento.tsx:332-428,443-456`).
- Cartão SH: **"Pressão de baixa (sucção)"** + **"Temperatura da linha de sucção"** (°C). Cartão SC: **"Pressão de alta
  (líquido)"** + **"Temperatura da linha de líquido"** (°C). Resultado ao vivo: valor grande em °C, selo **"Baixo"**,
  **"Ideal"** ou **"Alto"** com "ideal X–Y °C", e "Temperatura de saturação: … °C" (`Superaquecimento.tsx:190-225`).
- Pressões são **manométricas (gauge)**. Fora da tabela do gás: "Pressão fora da faixa da tabela para este refrigerante.
  Confira a leitura." e, se a outra unidade explica, o aviso "**N** está fora da faixa em **psi**. Em **bar** daria saturação
  ≈ … °C." com botão **"Trocar para bar e recalcular"** (`Superaquecimento.tsx:280-330`).
- Modelos (alvo SH): Padrão 4–8 °C; Split Hi-Wall Midea/Springer/Carrier/Gree/Admiral/Brastemp 5–7; Samsung sem alvo
  (carga por peso); Comfee 5–7; Philco/Elgin 6–11; Hitachi Hi-Wall sem alvo; York só SC 5–6; Rheem K7 5–7; Carrier/Springer
  piso-teto e K7 5–7; Hitachi Série E 4–12 (SH e SC); Carrier Ecosplit SH 3–7 e SC 8–11
  (`lib/superaquecimentoModelos.ts:43-150`). Sem alvo do fabricante aparece "Alvo não publicado — usando referência
  genérica" e a fonte ("Fonte secundária", "Fonte limitada", "Referência genérica") (`technicianTools.ts:255-258`).
- **Conferido (modelo Padrão, R-410A, psi):** SH com 118 psi e 12 °C → saturação 4,3 °C, **SH 7,7 °C, "Ideal"**; com 125 psi e
  15 °C → SH 9,1 °C, **"Alto"**. SC com 350 psi e 35 °C → saturação 41,4 °C, **SC 6,4 °C, "Ideal"**.

### 3.9 Régua de Gases (`ReguaGases.tsx`, 505 linhas)

Título **"Régua de Gases"** / "Pressão de saturação dos refrigerantes por temperatura." Régua vertical de **−40 a +60 °C**
(marcas de 5 em 5) que se arrasta ("arraste ↑ ↓"); campos de **pressão** e **temperatura (°C)** que se influenciam (digitar
um calcula o outro); **"Gás"** (os 13 gases), **"Unidade"** (psi / bar) e **"Fórmula"** (vapor (dew) / líquido (bubble),
só para blends; para os demais mostra "curva única (sem glide)"). Padrões: 5 °C, R-410A, vapor, psi
(`ReguaGases.tsx:40-41,251-262,485`, `technicianTools.ts:284-304`). Fora da faixa: aviso com "Parece estar em … (daria … °C).
Toque para trocar.".
- **Conferido (psi manométrico, 5 °C):** R-410A 121 psi (8,34 bar); R-22 70 psi; R-32 123 psi; R-134a 36 psi; R-404A (vapor) 82
  psi; R-407C (vapor) 65 psi.
- Gases: R-410A, R-22, R-32, R-134a, R-290 (Propano), R-404A, R-407C, R-422D, R-438A, R-407A, R-448A, R-449A, R-12
  (`lib/refrigerantes.ts:540-616`). Chama (âmbar A2L: R-32; vermelha A3: R-290) com texto ao passar o mouse
  (`RefrigeranteInflamavel.tsx`, P8).

### 3.10 Retrofit de Gás (`RetrofitGas.tsx`, 325 linhas; dados em `lib/retrofitGases.ts`)

Título **"Retrofit de Gás"** / "Gases drop-in para trocar o refrigerante direto na mesma máquina." Seletor **"Gás atual:"**
(R-22 padrão, R-404A, R-12, R-502, `lib/retrofitGases.ts:72-232`) e chave **"Unidade:"** psi / bar. Nota: "**Drop-in** é a
troca de gás no mesmo equipamento — em geral só trocando o óleo e o filtro secador. Sempre siga a ficha técnica do gás e do
compressor." Lista **"Gases que podem substituir o R-22"**; cada opção: nome, selo de tipo (drop-in ou equipamento novo), selo
**"Mais indicado"** (primeiro da lista), **"Óleo"**, **"Pressão"**, **"Cuidados"** e **"Pressão de trabalho"** (evap. +5 °C,
cond. +45 °C, "Baixa ~… · Alta ~…") (`RetrofitGas.tsx:158-325`, `technicianTools.ts:444-463`).
- Mais indicado por gás de saída: R-22 → **R-438A (MO99)**; R-404A → **R-449A**; R-12 → **R-134a**; R-502 → **R-404A**
  (`lib/retrofitGases.ts:113,167,191,240`).

### 3.11 Ciclo de Refrigeração (`CicloRefrigeracao.tsx`, 136 linhas)

Título **"Ciclo Básico de Refrigeração"** / "Entenda como o gás circula pelo sistema e o que cada componente faz." Chave
**"Ilustração"** (padrão, desenho animado em SVG, `CicloRefrigeracaoIlustracao.tsx`) ↔ **"Imagem 2D"** (PNG estático que muda
com tema claro/escuro e celular/computador: `public/images/ciclo-basico-{claro,escuro}[-mobile].png`,
`CicloRefrigeracao.tsx:36-43`). Abaixo, **"Termos do ciclo"** ("Cada componente e conceito do ciclo, explicado."): 12 termos em
acordeão (`lib/glossarioCiclo.ts`). Aviso: "Conteúdo de apoio e didático…" (`technicianTools.ts:464-475`).

### 3.12 Diluição de Produto (`DiluicaoProduto.tsx`, 466 linhas)

Título **"Diluição de Produto"**. Chave **"Modo de Diluição"**: **"Preparar solução"** ("Quanto de produto e de água para chegar
no volume desejado.") ou **"Tenho X de produto"** ("Quanto de água adicionar ao produto que você já tem."). **"Proporção"**:
"1 para" + número (atalhos 1, 3, 5, 10, 20, 40, 100); **"Volume final desejado"** (Ex: 500) ou **"Quantidade de produto"** (Ex: 50)
com chave **"Unidade"** mL / L. Resultado: galão desenhado (rosa = produto, azul = água) com **"Produto"** e **"Água"** (ou
"Água a adicionar"), "Total: … na proporção 1:N." e "Como ler: Proporção 1:N = 1 parte de produto para N partes de água."
(`DiluicaoProduto.tsx:20-23,180-466`, `technicianTools.ts:305-331`). Disponível também para Estética Automotiva.
- **Conferido:** proporção 1:10, volume final 500 mL → 45,45 mL de produto e 454,55 mL de água.

### 3.13 Prévia bloqueada de outros nichos (`SegmentLockedScreen.tsx`, `config/technicianArea.ts:230-298`)

Escolhendo outro nicho no selo: o endereço ganha `?nicho=…`, o menu mostra **4 itens com cadeado** (ex.: Instalações
Elétricas: "Dimensionamento de Disjuntor", "Queda de Tensão", "Bitola de Cabo", "Carga Instalada"; Energia Solar:
"Dimensionamento Fotovoltaico", "Nº de Painéis", "Geração Mensal", "Dimensionar Inversor") e o conteúdo é sempre um cartão:
ícone do nicho com cadeado, selo, **"Ferramentas de <nicho>"**, "Sua empresa não tem acesso às ferramentas do segmento de
<nicho>. Converse com um representante para contratar." e botão **"Falar com representante"** (ícone WhatsApp)
(`technicianTools.ts:476-481`). Clicar nos itens só destaca; **nada abre**. O botão abre o WhatsApp comercial da Dominex em
**outra aba** com texto pronto (`SegmentLockedScreen.tsx:31-37`). Assistência Técnica (TI) não tem prévia (P5).

### 3.14 Dentro da OS do técnico (`pages/TechnicianOS.tsx:991-1008,4942-5004`)

- Em empresa de Refrigeração, aparece o **botão flutuante** (ícone de ferramenta sobre fundo animado na cor do segmento,
  ciano), canto inferior esquerdo, `aria-label` "Área do Técnico™"; um toque abre direto (`directWhenSingle`). Sobe 56 px
  quando a barra de execução está visível (`TechnicianOS.tsx:4942-4966`). Some enquanto as ferramentas estão abertas.
- Abre **tela cheia** sobre a OS (a OS continua montada por baixo): cabeçalho com fundo animado na cor do segmento, o mesmo
  hub e as mesmas ferramentas (modo embutido) e, fixo no rodapé, o botão vermelho **"Voltar para OS"** (`os.ts:879`,
  `TechnicianOS.tsx:4972-5004`). Ao voltar, o técnico está exatamente onde parou.
- Dentro do overlay: **"Voltar"** do cabeçalho só aparece fora do Início e do Catálogo (`TechnicianArea.tsx:606-607`); troca de
  nicho reinicia no Início (`TechnicianArea.tsx:593-597`).

---

## 4. Backend por tela

| Tela | Tabelas / RPCs / funções / buckets | Observação |
|---|---|---|
| Segmento (todas) | `company_settings.segment` via `hooks/useCompanySettings.ts` | Já está na semente base (`seeds/gen-01-tenant.json`: `"segment": "refrigeracao"`). |
| Início, Carga Térmica, Conversão, Capacitor, Cabo, Régua, Retrofit, Ciclo, Diluição, Superaquecimento | **Nenhum.** Contas e textos locais (`lib/*.ts`) | Imagens estáticas do próprio app: `public/images/ciclo-basico-*.png`, `public/images/capacitores/capacitor.png`, `public/images/contatora.png`, `public/images/disjuntores/din-{bipolar,monopolar}.png`. |
| Memória de campos | `sessionStorage` chaves `tt:state:*` (`hooks/usePersistedState.ts:16-42`) | Some ao fechar a aba do navegador. |
| Favoritas / Recentes | `localStorage` chaves `tt:favoritos:*`, `tt:recentes:*` (`lib/technicianAreaHistory.ts:19-24`) | Só "Favoritas" da Conversão é exibida (P3). |
| Consumo de energia | `localStorage` `catalogo-energia-config` (`Catalogo.tsx:2185`) | Padrão 0,90 e 8 h. |
| Catálogo: marcas | `equipment_models` (campo `brand_id`, filtro `domain`) e `equipment_brands` (`id, name, slug, logo_url, sort`) | `hooks/useEquipmentCatalog.ts:136-160`. |
| Catálogo: modelos | `equipment_models` (`name, code, image_url, manual_url, manual_type, refrigerant, consumo_kwh_mes, potencia_w, domain, compressor_model_id, i18n`) com embeds `brand:equipment_brands` e `category:equipment_model_categories` | `useEquipmentCatalog.ts:181-262`. |
| Catálogo: códigos de erro | `equipment_error_codes` (`code, title, description, diagnosis, solution, component, i18n`); a busca global usa embed **`model:equipment_models!inner`** com filtro `model.domain` e `limit(5000)` | `useEquipmentCatalog.ts:290-306,460-470`. |
| Ficha do compressor | `compressor_specs` (1 por modelo) | `useEquipmentCatalog.ts:331-345`. |
| Controle remoto | `remote_configs` (1 por modelo) | `useEquipmentCatalog.ts:360-372`. |
| Fluidos | `refrigerant_gases` (`code, name, tipo, classe_seguranca, cor, composicao, gwp, odp, ponto_ebulicao_c, glide_k, oleo, substitui, aplicacao, observacoes, ficha_url, guia_oficial_url, sort`) | `useEquipmentCatalog.ts:444-456`. |
| Fotos e logos do Catálogo | Bucket público `equipment-catalog` (as colunas guardam a **URL completa**) | `supabase/migrations/20260614210000_...sql:12-24`. |
| Manual (PDF) | `equipment_models.manual_url` (URL); o botão faz `fetch` + gravação de arquivo | `Catalogo.tsx:292-308`. |
| Prévia bloqueada | Nada no banco; WhatsApp externo `wa.me` via `lib/whatsapp.ts` | `SegmentLockedScreen.tsx:35`. |
| Contrato PMOC (Carga Térmica embutida) | Nenhum para a conta | `CargaTermicaCalculatorModal.tsx`. |

**Comparação com o backend falso** (`/home/claude/domiflix/rec/fakebase`):
- **Existe** no `schema.json` o formato de todas as tabelas do Catálogo (`equipment_brands:96`, `equipment_models:101`,
  `equipment_error_codes:98`, `compressor_specs:45`, `remote_configs:184`, `refrigerant_gases:183`,
  `equipment_model_categories:100`).
- **Não existe nenhuma semente** com linhas dessas tabelas (`seeds/` e `seeds-extra/t3/` só têm `equipment_categories` e
  `equipment_field_config`, tabelas de outro assunto). Resultado hoje: o Catálogo cai nos vazios "Catálogo em
  atualização". É a **maior lacuna do T18**.
- Falta provar que o backend falso aguenta: embed com `!inner` + filtro no embed (`model.domain=eq.…`), `in.(…)`,
  `limit=5000` e `order` com `nullsFirst` (`useEquipmentCatalog.ts:155,296-302`). O `desconhecidos.log` mostra o que ele
  ainda não conhece.
- Imagens/PDF: as colunas guardam URL; no backend falso servir arquivos fictícios em `storage/` (URL local) ou deixar
  `null` (marca vira o nome em texto, foto vira "Sem foto", manual vira "Manual Indisponível").
- Segurança de dados: o catálogo real tem marcas e modelos reais (`docs/catalogo-equipamentos.md`, 17 marcas, 60 modelos,
  261 códigos em 14/06; hoje com mais 3 domínios). Na gravação usar **nomes** de marca (ou inventadas) e **sem logos**.

---

## 5. Pegadinhas para roteiro e gravação

- **P1. [handoff] Menu superior mostra o item para segmento sem ferramentas.** O menu lateral e o "Mais" escondem "Área do
  Técnico™" quando o segmento não tem ferramentas (`requiresTechTools`), mas o **Menu superior não confere o segmento**
  (`TopNavbar.tsx:94,204-210`); clicar leva de volta ao Dashboard (`App.tsx:403`). Roteiro: não dizer que "o menu esconde" sem
  citar o estilo do menu.
- **P2. Memória só de sessão.** Cada ferramenta lembra o último valor (padrão `tt:state:*`) enquanto a aba ficar aberta e
  some ao fechar (`usePersistedState.ts:3-15`). Para gravar: cada capítulo começa com os padrões; trocar de ferramenta e
  voltar mostra o valor mantido (bom "aviso positivo": "o que você digitou continua lá").
- **P3. [handoff, UX] "Recentes" e "Favoritos de modelos" são gravados e nunca mostrados.** O Início não os lista
  (`Inicio.tsx`); comentários antigos ainda falam em "Recentes/Favoritos do Início" (`TechnicianArea.tsx:88`,
  `Catalogo.tsx:811`, `Conversao.tsx:34`). A estrela no topo dos códigos de erro grava em `tt:favoritos:modelos` e **não há
  tela que a liste**. Só "Favoritas" da Conversão aparece. Não prometer lista de favoritos de modelo.
- **P4. [handoff, UX] Quem vê o botão flutuante da OS × quem vê o menu.** O botão exige segmento exatamente
  `refrigeracao` (`TechnicianOS.tsx:994`) e o menu aceita qualquer segmento com ferramentas (TI, Estética). O comentário no
  código ainda diz "exclusiva do segmento Refrigeração".
- **P5. Prévia de TI não existe.** O seletor de nichos oferece "Assistência Técnica (TI)", mas `TEASER_TOOLS_BY_SEGMENT` não
  tem essa chave (`config/technicianArea.ts:230-298`): numa empresa de Refrigeração o menu fica **sem itens** e só aparece o
  cartão de bloqueio (a confirmar na tela). Para o roteiro mostrar prévia, escolher "Instalações Elétricas" ou "Energia Solar".
  O seletor lista 10 nichos (o código fala em 9, `utils/companySegments.ts:14-16,71-76`).
- **P6. [handoff, texto] "110v" × 127 V × 110 V.** A chave de tensão do Cabo diz "110v" mas calcula com 127 V e o aviso diz
  "Evite 127V…" (`lib/caboEletrico.ts:21`, `technicianTools.ts:431`); o Capacitor usa 110 V para os ampères
  (`lib/capacitor.ts:12`). Falar "110 ou 127 volts" ou só "tensão baixa (monofásica)" na narração.
- **P7. HP → BTU/h tem dois modos** e o padrão é o comercial (1 HP ≈ 9.000 BTU/h), não a física (2.544). Se o roteiro
  mostrar "HP → BTU/h", deixar claro qual modo (`Conversao.tsx:63,291-293`).
- **P8. [handoff, texto] Textos fixos em português** que não seguem o idioma: faixa "ideal X–Y °C" (`Superaquecimento.tsx:580`
  e `:609`), nomes e notas dos modelos e dos grupos (`lib/superaquecimentoModelos.ts`), "Gases Legado (Antigos)" e
  "Substitutos / Blends de retrofit" (`lib/refrigerantes.ts:642-643`), texto da chama (`RefrigeranteInflamavel.tsx`), rótulos
  de acessibilidade. Irrelevante para o vídeo em pt-br.
- **P9. [handoff, texto] Mensagens fixas no Catálogo:** "Nenhum código corresponde a "…" neste modelo." (`Catalogo.tsx:2903`) e o
  nome de marca "Marca" quando falta (`Catalogo.tsx:2830,2841`); `kwh()` e o TR da Carga Térmica usam `pt-BR` fixo.
- **P10. Janelas e abas novas no gravador.** "Baixar manual" baixa arquivo (`Catalogo.tsx:292-308`) e, se der erro, abre aba
  nova; "Falar com representante" abre `wa.me` em aba nova (`SegmentLockedScreen.tsx:36`). O gravador não cobre download
  nem nova aba (TRILHA.md, item 6). **Só apontar** (câmera no botão), sem clicar.
- **P11. Dados do Catálogo são reais na produção** (marcas, modelos, manuais, códigos). No vídeo, usar semente fictícia; sem
  logos de terceiros. Os nomes de fabricante que aparecem **dentro do código** (lista de modelos do Superaquecimento:
  Midea, Springer, Carrier, Samsung, Philco, Hitachi, York, Rheem…) são rótulos do próprio app e aparecem ao abrir o
  seletor; decisão no `plano.md`.
- **P12. Fundo animado em WebGL.** O botão flutuante e o cabeçalho do overlay da OS usam fundo animado (`DarkVeilBackground`,
  `forceWebGL`, `TechnicianArea.tsx:247`, `TechnicianOS.tsx:4954`). Em navegador automatizado pode cair no degradê
  (a confirmar) e é movimento contínuo no vídeo (o robô deve esperar estabilizar).
- **P13. TR → BTU/h mostra "12.000,00129"** (`lib/conversoes.ts:61` + `formatarResultado`, até 6 casas). Evitar no exemplo.
- **P14. Contas dependem do que se escolhe antes.** Superaquecimento: escolher o modelo **muda o gás** (`Superaquecimento.tsx:351-355`); trocar para outro gás depois mantém o modelo. No roteiro, mostrar a ordem modelo → gás.
- **P15. Navegação no celular:** a barra de abas só aparece fora do Início (`TechnicianArea.tsx:266-267`); no celular, o Início
  tem carrossel com meia-cortina de gradiente nas laterais (`Inicio.tsx:108-109`).

---

## 6. 🚫 Não prometer / telas mortas / fora de escopo

- 🚫 **Histórico de cálculos** e **lista de recentes** (P3): não existem. O que existe é lembrar o último valor na sessão.
- 🚫 **Favoritos de equipamentos listados**: a estrela grava no aparelho e nenhuma tela lista.
- 🚫 **Funciona sem internet.** As contas são locais, mas abrir a Área do Técnico exige o app carregado e o segmento do banco;
  o Catálogo é consulta online. Nada de "offline" (o próprio gravador de OS do T7 diz o mesmo).
- 🚫 **Ferramentas dos outros nichos** (Elétrica, Solar, Telecom, CFTV, Construção, Elevadores, Limpeza, Dedetização): são
  só prévia com cadeado. Não mostrar como "em breve" com data e **não clicar em "Falar com representante"**.
- 🚫 **Ferramentas de TI** (Calculadora de Fonte, Conversor de Armazenamento, Laudo Técnico) e de **Estética Automotiva**:
  outra aula.
- 🚫 **Trocar o segmento da empresa** em Configurações: não dá (T1).
- 🚫 **Garantia de resultado.** Todas as ferramentas se declaram estimativas de apoio e mandam conferir placa, manual e
  norma. A narração não deve chamar de "projeto", "laudo" ou "dimensionamento oficial".
- 🚫 **Catálogo completo de todas as marcas/modelos**: é global e muda; não prometer um modelo ou código específico.
- 🚫 **Baixar o manual** durante a gravação (download, P10) e **ícones/logos de terceiros** na semente.
- ❌ **Telas mortas / sobras no código:** gravação de "Recentes" (`technicianAreaHistory.ts:90-100`); funções
  `getFavoritosModelos`/`getRecentesModelos` sem uso na tela; `onApply` de Carga Térmica só vale no contrato.

---

## 7. Dúvidas em aberto (só rodando o app)

1. **O Menu superior** mostra "Área do Técnico™" para segmento sem ferramentas e o clique volta ao Dashboard? (P1, lido no código.)
2. **Assistência Técnica (TI)** num tenant de Refrigeração: o menu realmente fica vazio ou o desenho tem algum fallback? (P5.)
3. **O fundo animado WebGL** (botão da OS e cabeçalho do overlay) renderiza no Chromium do robô ou cai no degradê? (P12.)
4. **Tamanho real do Catálogo em produção** hoje (marcas, modelos, códigos): `docs/catalogo-equipamentos.md` é de 14/06.
   Decide a semente do backend falso.
5. **A foto do botão flutuante** e o desenho "Ilustração" do ciclo (SVG animado) pesam no vídeo? Duração do loop?
6. **Modo "legado"** (sem permissões gravadas): confirmar que o técnico vê a Área do Técnico (TRILHA.md achado 2) e se alguma
   permissão de tela precisa ser marcada num técnico criado no T2.
7. **Idioma das mensagens fixas** (P8/P9) em en/es/fr: só relevante se houver versão em outro idioma.
