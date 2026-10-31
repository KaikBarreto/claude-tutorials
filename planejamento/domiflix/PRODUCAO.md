# Produção de todos os tutoriais Domiflix (pedido do Kaik, 30/10/2026 22:44)

> "agora com todas as instruções que te passei faça todos os tutoriais seguindo o molde do t3, só a introdução que é
> diferente. E se precisar depois eu ajusto detalhes, mas só pare com todos prontos agora, se possível tudo num mesmo
> ZIP todos na melhor qualidade pra eu baixar"

Molde: **T3** (`exemplos/dominex-t3/`, `perfis/domiflix/PERFIL.md`): robô no app real com Supabase falso e mundo
fictício Glacial Cold Brasil, voz Fernanda (eleven_v4), câmera v2 auditada, vinhetas faladas, trilha seed 3, legendas.
T0 é a aula ilustrada (`docs/09-aula-ilustrada.md`). Não parar para perguntar: decisões abertas seguem o padrão abaixo
e ficam listadas para o Kaik ajustar depois.

## Ordem de produção e situação
Etapas: L = levantamento · R = roteiro + `tts_textos.py` · V = voz gerada · Z = zip recebido e `proc.py` ·
B = backend falso (sementes + handlers) · G = gravação (robô) · E = edição (specs, câmera auditada, render) ·
F = montagem final + legendas + conferência · ok = no ZIP

| Aula | Título | L | R | V | Z | B | G | E | F |
|---|---|---|---|---|---|---|---|---|---|
| T0 | Boas-vindas à Dominex (ilustrada) | ok | ok | ok | ok | — | — | ok | ok (30/10 22:51, 3:25) |
| T1 | Configurações e identidade da empresa | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 05:20, 11:58) |
| T2 | Usuários, cargos e permissões | ok | ok | | | | | | |
| T3 | Clientes, Fornecedores e Equipamentos | ok | ok | ok | ok | ok | ok | ok | ok (30/10) |
| T4 | Serviços, tarefas e checklists | ok | ok | ok | ok (31/10 00:29) | ok | ok | ok | ok (31/10 10:46, 10:27) |
| T5 | Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo | ok | ok | ok | ok (31/10 00:29) | G3 | G3 | G3 | G3 |
| T7 | O técnico em campo (celular) | ok | ok | ok | ok (31/10 00:29; emenda pendente no cap05) | G4 pausado 11:2x (`rec/t7/ESTADO.md`) | | | |
| T18 | Área do Técnico: Refrigeração e Climatização | ok | ok | ok | ok (31/10 11:30) | | | | |
| T8 | Estoque, compras e inventário | ok | ok | | | | | | |
| T9 | Orçamentos, Precificação e Proposta | ok | ok | | | | | | |
| T10 | CRM: funil, leads e captação | ok | ok | | | | | | |
| T11 | Contratos e PMOC | ok | ok | | | | | | |
| T12 | Portal do Cliente e Portal do Contrato | ok | ok | | | | | | |
| T13 | Financeiro | ok | ok | | | | | | |
| T19 | Integração com Asaas, Assinaturas e Cobranças | ok | ok | | | | | | |
| T20 | Relatório Financeiro e DRE | ok | ok | | | | | | |
| T14 | Notas Fiscais (NFS-e e NF-e) | ok | ok | | | | | | |
| T15 | Funcionários: Financeiro do Funcionário e Ponto | ok | ok | | | | | | |
| T22 | Ferramentas de RH: DISC, Organograma, Fluxograma | ok | ok | | | | | | |
| T21 | Integração com WhatsApp | ok | ok | | | | | | |
| T17 | Dashboard, relatórios e exportações | ok | ok | | | | | | |

Ordem (TRILHA.md): T0 → T1 → T4 → T5 → T7 → T18 → T2 → T8 → T9 → T12 → T13 → T20 → T10 → T11 → T15 → T22 → T19 →
T21 → T14 → T17. O mundo fictício segue a ordem de **exibição** (cada aula parte do estado final da anterior).

## Como cada aula é feita (molde T3)
1. **R**: `planejamento/domiflix/Tnn/roteiro.md` (Tela × Fala por capítulo, estilo `exemplos/dominex-t3/roteiro.md` e
   `estilo_narracao.md`) + `$TUT_HOME/tnn/narracao/tts_textos.py` (`CAPS`, `TITULOS`, `KICKERS`) + `config_narracao.json`.
2. **V**: o fluxo ElevenLabs único (todas as aulas), nós rotulados `Tnn capMM <título>` e `Tnn títulos` (1 versão por fala, pedido do Kaik).
   O Kaik exporta o zip do fluxo; `proc.py` por aula (`recebido_<hhmm>/Tnn*`), `titulos.py`.
3. **B**: `rec/fakebase/seeds-extra/tnn/` + handlers que faltam (lista no `plano.md` → "Gravação").
4. **G**: `rec/tnn/capMM.json` (passos com `label`, `at` pelos tempos do `capMM.json`), gravação um capítulo por vez sob
   `.heavy.lock`; aceite: 0 passo falho, `lateBy` < 0,8 s, sem dado real.
5. **E**: `edit/caps/specs.json` → `montar_cap.py` → `auditar_camera.py` (0 problema) → `render_chapter.py`.
6. **F**: `finish.py` → `legendas_aula.py` → `entregar.py`; vídeo completo 1080p + .srt + .vtt.
7. Limpeza de disco: depois do F, apagar gravações, renders de capítulo e `proj/` da aula (fica o final + legendas).

## Ambiente de gravação (antes da primeira gravação nova)
- App de gravação em `$TUT_HOME/app` **atualizado para a 1.38.6** em 30/10 22:55 (`DOMINEX_SRC=src-1.38.6
  rec/setup-app.sh` + `rec/run.sh build`; dependências iguais). Fumaça ok (0 problema). Antes de cada gravação, conferir
  se saiu versão nova (`git fetch` no clone, só leitura) e repetir.
  31/10 05:3x: saiu a **1.38.7** (só painel admin: `update-company`, permissão de um vendedor, changelog); nenhuma tela
  das aulas muda, então a gravação segue na 1.38.6. Atualizar quando sair versão que mexa em tela de aula.
- Data do mundo: exportar o **mesmo `FAKE_NOW`** para o backend falso (`rec/run.sh fake`/`up`) e para o robô (o
  navegador instala o relógio nessa data: `recorder/browser.mjs`, testado 30/10). Datas diferentes = a assinatura da
  empresa fictícia (`@now+23d`) aparece vencida e o app mostra a tela de bloqueio com preço.
- Robô da área de trabalho **unificado com o da skill** (30/10 23:0x; o antigo em `rec/_antes_skill/`): máscara de senha,
  modo URL, `$VAR`. Validado regravando o T3 cap04: 23 passos, 0 falho, `lateBy` máx 0,29 s.
- Robô ainda sem: nova aba (PDF, link público), download, página sem login por capítulo, endereço com nome de produto
  nos links, celular (T7). Fazer antes das aulas que precisam (ver cada `plano.md`).

## Decisões abertas: padrão adotado (o Kaik ajusta depois)
- Recomendação de cada `plano.md` → "Riscos e decisões" vale como decidida, salvo o que está abaixo.
- Integrações externas (Asaas, NFS-e/NF-e, WhatsApp, mapa): só simuladas no backend falso, telas fiéis ao código.
- Notas fiscais (T14): ambiente de **homologação**, PDF com "SEM VALOR FISCAL"; empresa Glacial Cold Brasil (escolha
  do Kaik) com CNPJ fictício válido.
- Aulas longas (T11 ~17 min): uma aula só, como manda a trilha (1 tutorial por área).
- T7 e telas de técnico: celular genérico no palco (sem marca), toque marcado, mesma câmera.
- T2: lista começa só com a Camila; Rafael e Tatiane criados na aula, os outros técnicos entram num corte.
- Portal (T12): mostrar a configuração da senha, sem demonstrar o login protegido; página pública gravada sem login.
- Endereço do app nos links: nome de produto mapeado para a máquina local (sem rede).
- Datas: navegador e backend falso congelados na mesma data (`FAKE_NOW`), mês seguinte ao da gravação quando o PMOC
  precisar de visitas futuras.
- Sem preço de plano da Dominex em nenhum vídeo.
- **T19 × T1 (Asaas):** o T19 parte sem a conta Asaas para mostrar a ativação, embora o cap11 do T1 mostre o cartão
  "Ativo"; a fala do T19 avisa "se na sua empresa a integração já está ativa, pode pular". Alternativa, se o Kaik
  preferir continuidade exata: regravar o cap11 do T1 com a integração desligada.

## Alinhamentos entre aulas (valem por cima dos roteiros)
- **Financeiro padrão do cadastro** (contas Caixa e Conta Principal, 14 categorias padrão + 14 do sistema; detalhe em
  `MUNDO_FICTICIO.md` → Base): nas sementes de toda aula a partir da primeira que abre o Financeiro (T8/T9). O T11 já
  conta com eles; o T13, o T19 e o T20 foram revistos para isso (31/10 05:3x).
- **T9:** "Primeiro vencimento" das 3 parcelas do Orçamento #2 = **20/11/2026** (o T13 parte delas: 20/11, 20/12, 20/01).
- **FAKE_NOW `2026-11-10T10:00:00-03:00`** em T11, T12, T13, T19, T20 e T14 (fatura do cartão fechada no dia 5,
  mensalidades do PMOC a partir de 10/12 ainda futuras).
- **T9 → T15:** os funcionários que o T9 semeia para a calculadora de mão de obra entram só com o custo mensal
  (`monthly_cost`) e salário 0; o T15 completa os salários num corte (com salário, o cron criaria folhas que o T13 não
  mostra em Contas a Pagar).
- **Dashboard (toda aula que o mostra):** OS de hoje ainda aberta aparece "Atrasada 0 dias" e os gráficos deslocam um dia
  (bug de fuso, `src/pages/Dashboard.tsx:169,193,221`; T17 P2). Nas sementes, nenhuma OS do dia aberta no momento da
  gravação, ou a câmera não enquadra "Requer Atenção".
- **T7 → T8:** Fita isolante com 28 no estoque (o roteiro do T8 e o T7 batem; o `plano.md` do T8 dizia 29).
- **T22:** o robô nunca pousa o cursor no gráfico DISC (o tooltip cita pessoas reais; T22 P6).
- **T19:** o handler `tenant-asaas-card-fees` (criado no T1) responde sem a franquia do Pix (`freeCount 0`): estender por
  semente ou parâmetro, sem reescrever o do T1.

## Fila (31/10 12:1x; nada sai da fila sem estar entregue)
1. **Rodando (Kaik 14:48 liberou até 4 agentes ao mesmo tempo):** dev-video no 06 e no 12 do site (com a trava
   pesada só para ele, pedido de urgência) · G3 com o T5 pausado antes do cap17 e do finish · dev-gravacao corrigindo
   T1 e T4 (prepara o leve; o pesado espera a trava) · dev-levantamento na 1.38.9 + roteiro do T3 v2 (`T03v2/`).
   Disco: 5,6 GB livres; T1/T4 guardam `video_sem_audio.mp4` para corrigir só o áudio.
2. **Próximas vagas, nesta ordem.** A **1.38.8** saiu às 12:40 (`0b35ea72`, etiquetas e campos personalizados; fonte em
   `$TUT_HOME/src-1.38.8`). O T1 não muda: as Configurações e o `CustomerOriginManagerDialog` seguem iguais.
   (a) `emendar.py` corrigido, T4 (emenda do cap03) e T1 (cap05 com o logo branco e emendas de pronúncia), ainda na
   1.38.6, como o resto do T1; reentregar os dois. (b) Em paralelo: levantamento da 1.38.8 em Clientes e Fornecedores,
   roteiro dos trechos do T3 e voz só do que muda. (c) Trocar o app de gravação para a 1.38.8, depois que o T5 e o cap05
   do T1 estiverem gravados. (d) T7 retomado (G4, `rec/t7/ESTADO.md`) e T18, na 1.38.8. (e) T3 v2. (f) Com créditos:
   vozes V3–V5 e as aulas T2, T8, T9, T12, T13, T20, T10, T11, T15, T22, T19, T21, T14, T17, na ordem da trilha
   (conferir telas de cliente, fornecedor e portal na versão nova).
   **Kaik 12:45: "vou soltar a 1.38.9 com as funções definitivas disso"**: o levantamento do T3 v2 e a troca do app
   esperam a 1.38.9 (vigia no `main` rodando), não a 1.38.8.
   **1.38.9 publicada 13:27** (`7690807a`; fonte em `$TUT_HOME/src-1.38.9`): várias etiquetas em clientes, fornecedores e
   **equipamentos**, filtros, etiquetas nos seletores (OS, agenda, orçamento, compras, PDV), configurações reunidas
   (`Equipment.tsx` perdeu ~190 linhas: a configuração de campos do equipamento deve ter ido para o modal único) e
   etiquetas no portal do PMOC. Afeta o T3 (capítulos de equipamento também) e muda telas de T5, T8, T9, T11, T12
   (sem etiquetas semeadas, só aparecem os controles novos). O T5 segue na 1.38.6 (já gravado; seletores sem etiqueta
   ficam iguais); conferir na entrega se a agenda ganhou filtro visível.
   **16:4x:** levantamento e roteiro do T3 v2 prontos (`T03v2/`), voz gerada (lote V2c). Para gravar na 1.38.9, o backend
   falso precisa de 5 tabelas, 5 colunas, 3 RPCs chamadas em todo salvar, padrões e o gancho de exclusão
   (`T03v2/inventario_delta.md`); a troca do app para a 1.38.9 vem junto com isso, depois do T1 cap05/cap06 (1.38.6).
   T7 retomado (G4): prepara agora e grava na 1.38.9.
3. **T3 v2 (Kaik 31/10 12:11):** "Editar" e "Excluir" da ficha foram para "Ações" (já na 1.38.6, `5f0b64ea`: fichas de
   cliente e de equipamento) e "Configurar origens" virou um modal único "Configurações" com Origens, Etiquetas, Campos
   de clientes e Campos de fornecedores (`CustomerSettingsDialog.tsx`, recurso novo; publicado na 1.38.8). Afeta no T3: cap01 (botões do topo), cap04 (vira origens + etiquetas + campos), cap05 (cabeçalho da
   ficha), cap07 (fornecedor, campos), cap10 (ficha do equipamento) e o recap; no T1, o cap09 (Origens) se o cartão de
   Configurações mudar. Plano: levantamento da versão nova → roteiro dos trechos → voz só do que muda → regravar esses
   capítulos → reentregar (T1 junto, se o cap09 mudar). As aulas seguintes passam a gravar na versão nova.

## Correções pedidas pelo Kaik (31/10 11:04)
- **Pronúncia** em todas as aulas: Glacial Cold Brasil → "Glaciál Côude Brasil" (sozinho, "Glaciál"); White Label →
  "uáit lêibou". Textos e `config_narracao.json` corrigidos no planejamento e na área de trabalho (perfil também).
  Já gravadas: T1 (cap03, cap06, cap07, cap13 por emenda; cap05 refeito inteiro), T4 (cap03 por emenda), T18 (cap01,
  emenda depois do V2). `trocas.json` de t1 e t4 prontos.
- **T1, logo do White Label:** usar a versão com o texto branco (`/home/claude/brand-fix/assets/glacial_horizontal_texto_branco.png`)
  no "Logo completo" (o menu é escuro). Roteiro do cap05 reescrito (linhas 3 e 4) e voz nova (`T01 cap05 ... (v2)`):
  regravar o cap05 com o passo "Substituir" + upload, refazer a edição dele, as emendas e o `finish`/`entregar`.
- **T4:** emenda no cap03, render só do cap03 e `finish`/`entregar` de novo.
- **Processado 31/10 11:30** (`recebido/1118/processar.log`): T18 inteiro ok (16 capítulos, títulos, emenda do cap01 com
  0,57 s de folga; palavras fracas conferidas isoladas: todas do ASR). T7 cap05 e T1 cap03/06/07/13 emendados, mas a frase
  nova é um pouco mais longa: encosta na fala seguinte no T7 cap05 (−0,05 s) e no T1 cap03 (−0,16 s), sem respiro no T1
  cap07 (+0,03 s). T4: `emendar.py` quebrou (troca começando em 0 s dá índice negativo). **Antes de usar:** corrigir o
  `emendar.py` (início ≥ 0; frase mais longa que a janela comprimida até ~8% para deixar ≥ 0,2 s antes da próxima fala)
  e refazer as emendas de t1, t4 e t7. A fala do T7 diz "deixa" (decodificado isolado: "Deixa o vídeo"); o ASR é que cola
  "aplicativo deixa". Cópias `capNN.v1.json` guardadas.
- **Vídeos do site (sugestões do Matheus):** cabeçalho do portal em preto, "como se a marca tivesse definido assim",
  e, no círculo, só o ícone do logo com o nome embaixo (05 PMOC e 06 Portal do Cliente).

## Voz: lotes e exportação
Kaik (30/10 23:13): **um fluxo só com todas as aulas**, **uma versão por fala** (`generations_count: 1`), v3 liberado
se for melhor (custa o mesmo que o v4 por caractere: fica o v4, voz do T3); fala ruim regera só ela. Estimativa:
~12 mil caracteres por aula, ~230 mil créditos no total.

| Lote | Aulas | Fluxo ElevenLabs | Situação |
|---|---|---|---|
| — | T0 | 1fUfJ2KZAxkHKnc8wwce (fluxo próprio) | exportado 30/10 22:12 |
| V1 | T1, T4, T5, T7 (39,6 mil caracteres, 65 nós) | Tuop7qPrgwc8qdaVebww (fluxo único) | exportado 31/10 00:29; proc.py e títulos ok (semelhança 0,87 a 1,00) |
| V2 | T18 (11,3 mil caracteres, 17 nós) + `T07 cap05 emenda` | mesmo fluxo | exportado 31/10 11:18 (zip 3); processando |
| V2b | Correções de pronúncia (Kaik 31/10 11:04): `T01 cap05 A cor e o logo da marca (v2)` (logo com texto branco), `T01 emendas`, `T04 emendas`, `T18 emenda` = 1.745 créditos | mesmo fluxo | gerado 11:11, exportado 11:18 (zip 3); processando |
| V2c | T3 v2 (1.38.9): `T03v2 cap06 Etiquetas`, `T03v2 cap07 Campos personalizados`, `T03v2 emendas`, `T03v2 inserções`, `T03v2 títulos` = 1.824 créditos | mesmo fluxo | gerado 31/10 16:37; **saldo ~0**; aguardando exportação (zip 4) |
| V3 | T2 (8,5 mil), T8 (13,9 mil), T9 (13,5 mil), T12 (10,3 mil), T10 (10,4 mil), T11 (14,2 mil) = ~70,8 mil | mesmo fluxo | roteiros ok; aguardando créditos |
| V4 | T13 (12,8 mil), T19 (9,1 mil), T20 (7,9 mil), T14 (7,7 mil) = ~37,5 mil | mesmo fluxo | roteiros ok; aguardando créditos |
| V5 | T15 (8,2 mil), T22 (6,9 mil), T21 (5,4 mil), T17 (5,6 mil) = ~26,1 mil | mesmo fluxo | roteiros ok; aguardando créditos |

**Falas a refazer (próximo lote de voz, junto com o T18; o Kaik exporta uma vez):** T07 cap05, frase "O aplicativo
deixa o vídeo mais leve antes de enviar." (em ~0:29; o ASR não ouve o "deixa" nem isolado; há tempo de fala para ele,
então pode estar só fraco). Nó curto `T07 cap05 emenda` (~55 caracteres) + `emendar.py` antes de gravar o T7 (`t7/narracao/trocas.json` pronto). As demais
palavras fracas do V1 foram conferidas decodificando o trecho isolado: eram do ASR (números, nomes colados).

**Para terminar (31/10 07:20): V3 + V4 + V5 = ~134,4 mil caracteres** (~70,8 + 37,5 + 26,1), mais ~3 mil de reserva
para regerar falas; saldo de ~3,6 mil.

**Créditos (Kaik, 30/10 23:16): 54.670 restantes** (de 121.000) → ~54 mil caracteres ≈ 55 a 60 min de fala ≈ 4 aulas.
Gerar agora, na ordem da produção, só o que couber (T1, T4, T5, T7 se couber), com ~2 mil de reserva para regerar falas.
As demais: roteiro pronto e voz quando houver créditos (o Kaik avisa). Antes de cada lote: somar os caracteres de
`CAPS` + `TITULOS` e conferir com o saldo.

## Entrega
ZIP único (ou em partes, se passar do limite de envio) com `Domiflix Tnn - <Título>.mp4/.srt/.vtt` de todas as aulas
(T0 a T22, incluindo o T3 já entregue), 1080p, CRF 20 (padrão T3).
