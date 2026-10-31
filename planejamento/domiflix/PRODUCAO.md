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
| T1 | Configurações e identidade da empresa | ok | ok | ok | ok (31/10 00:29) | ok | G1 (robô validado: 14 caps, 0 falho) | G1 | G1 |
| T2 | Usuários, cargos e permissões | ok | ok | | | | | | |
| T3 | Clientes, Fornecedores e Equipamentos | ok | ok | ok | ok | ok | ok | ok | ok (30/10) |
| T4 | Serviços, tarefas e checklists | ok | ok | ok | ok (31/10 00:29) | | | | |
| T5 | Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo | ok | ok | ok | ok (31/10 00:29) | | | | |
| T7 | O técnico em campo (celular) | ok | ok | ok | ok (31/10 00:29; emenda pendente no cap05) | | | | |
| T18 | Área do Técnico: Refrigeração e Climatização | ok | ok | V2 | | | | | |
| T8 | Estoque, compras e inventário | ok | ok | | | | | | |
| T9 | Orçamentos, Precificação e Proposta | ok | ok | | | | | | |
| T10 | CRM: funil, leads e captação | ok | | | | | | | |
| T11 | Contratos e PMOC | ok | | | | | | | |
| T12 | Portal do Cliente e Portal do Contrato | ok | | | | | | | |
| T13 | Financeiro | ok | | | | | | | |
| T19 | Integração com Asaas, Assinaturas e Cobranças | ok | | | | | | | |
| T20 | Relatório Financeiro e DRE | ok | | | | | | | |
| T14 | Notas Fiscais (NFS-e e NF-e) | ok | | | | | | | |
| T15 | Funcionários: Financeiro do Funcionário e Ponto | C | | | | | | | |
| T22 | Ferramentas de RH: DISC, Organograma, Fluxograma | C | | | | | | | |
| T21 | Integração com WhatsApp | C | | | | | | | |
| T17 | Dashboard, relatórios e exportações | C | | | | | | | |

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

## Voz: lotes e exportação
Kaik (30/10 23:13): **um fluxo só com todas as aulas**, **uma versão por fala** (`generations_count: 1`), v3 liberado
se for melhor (custa o mesmo que o v4 por caractere: fica o v4, voz do T3); fala ruim regera só ela. Estimativa:
~12 mil caracteres por aula, ~230 mil créditos no total.

| Lote | Aulas | Fluxo ElevenLabs | Situação |
|---|---|---|---|
| — | T0 | 1fUfJ2KZAxkHKnc8wwce (fluxo próprio) | exportado 30/10 22:12 |
| V1 | T1, T4, T5, T7 (39,6 mil caracteres, 65 nós) | Tuop7qPrgwc8qdaVebww (fluxo único) | exportado 31/10 00:29; proc.py e títulos ok (semelhança 0,87 a 1,00) |
| V2 | T18 (11,3 mil caracteres, 17 nós) + `T07 cap05 emenda` | mesmo fluxo | gerado, aguardando exportação |
| V3.. | demais | mesmo fluxo | aguardando créditos |

**Falas a refazer (próximo lote de voz, junto com o T18; o Kaik exporta uma vez):** T07 cap05, frase "O aplicativo
deixa o vídeo mais leve antes de enviar." (em ~0:29; o ASR não ouve o "deixa" nem isolado; há tempo de fala para ele,
então pode estar só fraco). Nó curto `T07 cap05 emenda` (~55 caracteres) + `emendar.py` antes de gravar o T7 (`t7/narracao/trocas.json` pronto). As demais
palavras fracas do V1 foram conferidas decodificando o trecho isolado: eram do ASR (números, nomes colados).

**Créditos (Kaik, 30/10 23:16): 54.670 restantes** (de 121.000) → ~54 mil caracteres ≈ 55 a 60 min de fala ≈ 4 aulas.
Gerar agora, na ordem da produção, só o que couber (T1, T4, T5, T7 se couber), com ~2 mil de reserva para regerar falas.
As demais: roteiro pronto e voz quando houver créditos (o Kaik avisa). Antes de cada lote: somar os caracteres de
`CAPS` + `TITULOS` e conferir com o saldo.

## Entrega
ZIP único (ou em partes, se passar do limite de envio) com `Domiflix Tnn - <Título>.mp4/.srt/.vtt` de todas as aulas
(T0 a T22, incluindo o T3 já entregue), 1080p, CRF 20 (padrão T3).
