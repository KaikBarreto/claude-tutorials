# T4 · plano de produção · Tipos de Serviço, Tipos de Tarefa e Checklists

Base: `inventario.md` desta pasta (app 1.38.6). Rótulos entre aspas são os da tela. Fala só no positivo; nos cuidados (⚠️ da trilha) vale a
regra de 30/10 20:56: primeiro o caminho certo, depois a consequência numa frase, sem encenar falha na tela.

- **Título da aula:** Domiflix T4 · Tipos de Serviço, Tipos de Tarefa e Checklists (é o nome que o cartão final do T3 já promete; a trilha chama de "Serviços, tarefas e checklists").
- **Áreas das vinhetas:** SERVIÇOS · TAREFAS · CHECKLISTS · RESUMO.
- **Objetivo:** deixar montado o cardápio de serviços da Glacial e os roteiros que o técnico preenche em campo.
- **Antes:** Clientes, Fornecedores e Equipamentos (T3). **Próximo:** Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo (T5).
- **Duração estimada:** 20 a 22 min de fala (14 blocos; a trilha previa ~30). Candidatos a corte se pesar: blocos 6 e 12.

## Capítulos propostos

| # | Vinheta (área · título) | O que a tela mostra | Avisos na tela ("Dica: ...") | ~Dur. |
|---|---|---|---|---|
| 0 | (sem vinheta) Abertura + "Antes: Clientes, Fornecedores e Equipamentos" | Dashboard logado; câmera desliza pelo menu **Gestão** até **Serviços**. Fala: "é daqui que saem as ordens de serviço: o tipo, o prefixo e o roteiro do técnico". | Cartão "Antes: Clientes, Fornecedores e Equipamentos" | 0:50 |
| 1 | SERVIÇOS · A tela de Serviços (primeiro bloco: sem vinheta) | Menu Gestão › Serviços; título "Serviços" e subtítulo; abas "Tipos de Serviços", "Tipos de Tarefas", "Checklists"; estado vazio "Nenhum tipo de serviço"; botões "Categorias" e "Novo Tipo" na linha das abas. | "Dica: a aba escolhida fica no endereço; dá pra salvar o link direto" | 1:00 |
| 2 | SERVIÇOS · Categorias | "Categorias" → janela "Categorias de Serviço"; "Nova categoria" com "Nome da categoria..." + cor: Instalação, Manutenção, Higienização; mostra a alça de arrastar. | "Dica: categorias agrupam serviços parecidos e viram filtro da lista" | 1:10 |
| 3 | SERVIÇOS · Novo tipo de serviço | "Novo Tipo" → modal "Novo Tipo de Serviço" (aba "Dados"): "Nome *" Manutenção Preventiva, "Cor", "Categoria" Manutenção, "Descrição", "Prefixo de Numeração OS" MP (prévia embaixo), "Preço padrão (opcional)" 180, switches "Vinculado a equipamento" e "Ativo"; "Criar" → "Tipo de serviço criado!". Os demais serviços entram já cadastrados (seed) e a lista mostra os seis. | "Dica: o prefixo abre o número da OS" · "Dica: o preço padrão é a sugestão que o orçamento usa" | 2:30 |
| 4 | SERVIÇOS · Organizando a lista | Clica em "Visita Técnica": ficha com "Vinculado a equipamento" desligado (contraste com o da Manutenção Preventiva); busca "Buscar por nome ou descrição..."; "Filtros" › "Categoria"; "Ordenar". **Ilustração** curta do efeito na OS (ver abaixo). | "Dica: ligado, a OS pede o aparelho do cliente; desligado, só o serviço" | 1:15 |
| 5 | SERVIÇOS · Dados fiscais | Clica em "Manutenção Preventiva" › pílula "Fiscal" (🔒 módulo Nota Fiscal): "Código de serviço (cTribNac)" busca → 14.01.01; "Item da LC 116" preenchido; "Código de tributação municipal (cTribMun)" 001; "Alíquota de ISS (%)" 5; "Salvar" → "Tipo de serviço atualizado!". | "Dica: preenchendo uma vez, toda nota já nasce classificada" · "Esta aba aparece para quem tem o módulo de Nota Fiscal" | 1:45 |
| 6 | SERVIÇOS · Editar, desativar e excluir | Edita a descrição na ficha e "Salvar"; mostra o switch "Ativo"; abre "Excluir" → confirmação "Excluir Tipo de Serviço" e cancela. | "Dica: pra pausar um serviço sem perder o histórico, é só desligar Ativo" | 1:00 |
| 7 | TAREFAS · Tipos de tarefa | Aba "Tipos de Tarefas": "Novo Tipo" → "Novo Tipo de Tarefa": "Nome *" (Reunião; Entrega de material; Compra de peças), "Cor", "Descrição", "Ativo"; ficha "Ficha do tipo de tarefa". Fala: aparece no "Nova Tarefa" da Agenda. | "Dica: tarefa é compromisso interno; ordem de serviço é pro cliente" | 1:30 |
| 8 | CHECKLISTS · Catálogo de modelos | Aba "Checklists" (vazia): "Catálogo de Checklists" → aviso "Estes são apenas modelos sugeridos."; lista "Instalação de Split", "Higienização de Split", "Manutenção Preventiva de Split", "Carga de Gás"; abre o terceiro, mostra perguntas com selos ("Número (psi)"), "Selecionar" → "Nome do novo checklist" → "Criar checklist" → "13 perguntas importadas!". | "Dica: as perguntas dos modelos ficam 100% editáveis" | 2:00 |
| 9 | CHECKLISTS · Checklist do zero | Editor aberto ("Voltar à prévia"); "Serviços habilitados" › desmarca "Todos os serviços", marca Manutenção Preventiva (vínculo do checklist importado). "Novo checklist" → "Nome do checklist" Higienização de split, switch "Todos os serviços" desligado, marca Higienização de Split → "Criar". | "Dica: sem serviço marcado, o checklist vale pra todos" | 1:15 |
| 10 | CHECKLISTS · As perguntas | "Nova Pergunta": bloco "Escreva a pergunta" ("Pergunta" + "Orientação para o técnico (opcional)"); "Escolha como responder": Verdadeiro/Falso, Conformidade, Texto, Número, Foto, Vídeo, Seleção, Assinatura; "Opções de resposta" ("Adicionar opção..."); "Campo obrigatório"; **Prévia na OS** ao lado muda a cada clique. Cria "Estado da serpentina" (Conformidade) e "Aspecto da água retirada" (Seleção). | "Dica: a prévia mostra como o técnico vê" | 2:15 |
| 11 | CHECKLISTS · Combinando respostas | Pergunta "Filtros lavados?": marca Verdadeiro/Falso + Foto → "Modo de resposta múltipla": "Exclusivo" × "Cumulativo" (escolhe Cumulativo); "Exigir foto da câmera"; passa pelo tipo Vídeo com "Exigir gravação na hora". | "Dica: cumulativo pede a resposta E a foto" | 1:30 |
| 12 | CHECKLISTS · Organizar e conferir | Linhas com selos "Cumulativo"/"Câmera"; alça de arrastar (ordem); busca "Pesquisar pergunta, descrição ou tipo..."; "Todos os tipos"; "Voltar à prévia" e botão **"Ver"** → prévia de verdade, respondendo sem salvar. | "Dica: o "Ver" é igual ao que o técnico vê na OS" | 1:30 |
| 13 | CHECKLISTS · Vincular e desativar | Na lista: "N perguntas · Todos os serviços"/"N serviços"; no editor, switch "Ativo" e lixeira → "Desativar checklist?" (lê o texto, "Cancelar"). | "Dica: desativar tira da lista e das OS novas; as antigas ficam" | 1:15 |
| 14 | RESUMO · Recapitulando + "Próximo: Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo" | Montagem rápida: lista de serviços, categorias, tarefas, checklist com a prévia. | Cartão "Próximo: ..." | 1:15 |

**Falas-chave com ⚠️ (regra nova):**
- Fiscal (bloco 5): "Vale preencher agora: com o código de serviço salvo aqui, toda nota emitida com esse serviço já nasce classificada. E o código de tributação municipal, com os três dígitos, é o que a prefeitura usa pra aceitar a nota." (consequência numa frase, sem mostrar erro; não digitar 1 ou 2 dígitos).
- Desativar (bloco 13): "Pra aposentar um checklist, é só desativar: ele sai da lista e das ordens novas, e as ordens antigas continuam com o roteiro que usaram. É por isso que o sistema desativa em vez de apagar."
- Vinculado a equipamento (bloco 4): "Ligado, a ordem pede o aparelho do cliente, bom pra higienização e manutenção. Desligado, serve pra visita técnica e orçamento, onde não tem aparelho."
- Vídeo (bloco 11): só "o técnico grava um clipe curto como resposta"; não citar módulo nem limite (a 1.38.6 não aplica; ver Riscos).
- Frequência (bloco 10, aparece na Glacial por causa do módulo Contratos): uma frase: "esse campo Frequência é pra contratos; a gente vê no tutorial de Contratos". Sem abrir o seletor.

**Ilustração (só 1):** efeito de "Vinculado a equipamento" na OS (duas colunas: "Ligado: escolhe o aparelho do cliente" × "Desligado: só o serviço"), fundo branco, Montserrat, verde, objetos genéricos. Motivo: a tela de Nova OS só entra no T5 e não vale abri-la aqui.

## Mundo fictício
- **Começa com (estado final do T3, `seeds-extra/t3/apos-cap10.json` sobre `seeds/`):** Glacial Cold Brasil (segmento refrigeração, plano Master, módulos `nfe`, `contracts`, `video_questions` ligados), Camila Duarte (admin), 6 técnicos (Rafael Lima, Bruno Alves, Júlia Santos, Lucas Ferreira, Marina Costa, Paulo Souza), 16 clientes (12 base + Colégio Monte Verde, Marcos Antônio Braga, Luana Martins, Pousada Sol Nascente), fornecedores (Ventura Gás e Tubos + 4 base), 27 equipamentos (incl. "Hi-Wall 18.000 BTUs - Sala dos professores"), categoria "Multi Split", campo "Tensão". Nada de tipos de serviço, tarefas ou checklists.
- **Esta aula cria (ao vivo):** categorias Instalação `#3B82F6`, Manutenção `#22C55E`, Higienização `#06B6D4`; tipo **Manutenção Preventiva** (MP, `#22C55E`, Manutenção, R$ 180,00, vinculado a equipamento, fiscal 14.01.01 + 001 + ISS 5); tipos de tarefa Reunião `#8B5CF6`, Entrega de material `#F97316`, Compra de peças `#EAB308`; checklist **Manutenção preventiva de split** (importado do modelo, 13 perguntas, ligado a Manutenção Preventiva); checklist **Higienização de split** (do zero, ligado a Higienização de Split) com 4 perguntas ao vivo.
- **Entra por seed antes do bloco 4 (cadastrado "do mesmo jeito", sem câmera):** Manutenção Corretiva (MC, `#F97316`, Manutenção, R$ 220,00) · Instalação de Split (INS, `#3B82F6`, Instalação, R$ 650,00, fiscal 14.06.01 + 001 + ISS 5) · Higienização de Split (HIG, `#06B6D4`, Higienização, R$ 180,00) · Carga de Gás (GAS, `#A855F7`, Manutenção, R$ 350,00) · **Visita Técnica** (VT, `#6B7280`, sem categoria, R$ 120,00, **"Vinculado a equipamento" desligado**); tarefa Treinamento da equipe `#3B82F6`; no checklist de higienização, as perguntas "Observações" (Texto) e "Assinatura do cliente" (Assinatura) além das 4 ao vivo.
- **Fica para as próximas:** T5 abre OS com estes tipos (Manutenção Preventiva com checklist; Visita Técnica sem aparelho; Instalação de Split) e usa os tipos de tarefa na Agenda; T7 executa o checklist "Manutenção preventiva de split" (tem Verdadeiro/Falso, Número com unidade, Seleção, Foto, Texto e Assinatura); Orçamentos (T9) usam o "Preço padrão"; NFS-e (T14) usa a aba Fiscal.
- **Ao produzir:** gravar o estado final em `seeds-extra/t4/apos-cap14.json` (um `apos-capNN` por bloco que cria algo) e atualizar `MUNDO_FICTICIO.md` com a seção "O que o T4 criou"; o T5 parte desse arquivo.
- **Pré-checagens antes do roteiro final:** (1) conferir no robô se "Novo Tipo" com um tipo selecionado volta ao formulário vazio (inventário 7.1); (2) conferir se o `drag` HTML5 reordena categorias e perguntas; (3) conferir o rótulo do botão "Ver" do editor de checklist na tela (não confundir com o ícone de olho da ficha); (4) rodar um trecho de TTS com "Split", "PMOC" e "cTribNac".

## Gravação (modo fakebase, app 1.38.5 = 1.38.6 nos arquivos de T4)
- **Já cobre:** CRUD de `service_types`, `service_type_categories`, `task_types`, `form_templates`, `form_questions`, `form_template_service_types` (REST genérico + embeds), `company_modules`/`company_settings` da Glacial (segmento `refrigeracao`, módulos abertos), catálogo curado (local no app). Sem storage, sem RPC, sem host externo, sem PDF/link público.
- **Falta:** (1) `handlers/functions/nfse-tax-codes.mjs`: `{type:'servico'}` → `{items:[{codigo,descricao,itemLc116}], total}` com ao menos `140101` (item 14.01) e `140601` (14.06) e alguns vizinhos reais da migration `20260903182000_nfse_catalogos_tributacao_e_nbs.sql:312-317`; `{type:'nbs', q}` só se o bloco 5 mostrar NBS. Sem ele a busca mostra "Nenhum código encontrado.". (2) `seeds-extra/t4/apos-capNN.json` (um por bloco que cria algo) mais um seed manual para os cinco tipos "de bastidor" e as perguntas extras. (3) Opcional: `pmoc_activity_catalog` (149 linhas) só se algum bloco abrir o Catálogo PMOC; sem ela a janela mostra apenas "Modelos de checklist".
- **Robô:** viewport 1280×800 @2x (≥ 1024 px: mestre-detalhe visível); `prewarm` `/servicos`, `?tab=task-types`, `?tab=checklists`. Cor: digitar o hex no campo ao lado do quadrado (`{"selector":"input[type=color] + input"}`), o seletor nativo não aparece. Preço: `type=number`, digitar `180`. Lixeira do editor sem nome acessível (alvo por ícone/posição). `drag` para reordenar (HTML5): testar antes; se falhar, a ordem só é mostrada, não arrastada. Não gravar "Novo Tipo" para o segundo tipo enquanto o item P1 do inventário não for corrigido. Não deletar categoria/tipo ligado a checklist (o falso não emula FK).
- **Aceite:** 0 passo falho, `lateBy` < 0,8 s, rodapé 1.38.x, folha de contato sem dado real. Telas mobile: nenhuma neste tutorial.
- **Ordem de gravação sugerida:** capítulos 1 a 7 de uma vez (serviços e tarefas, sem dependência entre si), depois 8 a 13 (checklists, que dependem dos tipos de serviço já existentes para o vínculo), por fim o 14. O seed dos cinco tipos "de bastidor" entra antes do capítulo 4.
- **Dados de teste exatos** (para o robô digitar sempre igual): nomes, prefixos, cores e valores da seção "Mundo fictício"; preço digitado como `180` (campo numérico), prefixo `MP`, cTribNac `14.01.01`, cTribMun `001`, ISS `5`. Nenhum dado real; CNPJ/CPF não aparecem neste tutorial.

## Pronúncias novas (texto do TTS)
| Tela | TTS |
|---|---|
| cTribNac / "Código de serviço" | falar "código de serviço" (se precisar da sigla: "cê-tribi-nac") |
| cTribMun | falar "código de tributação municipal" |
| NBS | ene-bê-ésse |
| LC 116 | "lei complementar cento e dezesseis" |
| ISS | i-ésse-ésse |
| NFS-e | "nota fiscal de serviço" |
| PMOC | pê-ême-ó-cê (testar antes) |
| Split | testar "esplit" × "split" num trecho curto |
| psi / °C / A | pê-ésse-i · graus Celsius · ampères |
| MP / INS (prefixos) | ême-pê · ins |
| 14.01.01 | catorze, zero um, zero um |
| R$ 180,00 / 650,00 / 350,00 / 120,00 | cento e oitenta / seiscentos e cinquenta / trezentos e cinquenta / cento e vinte reais |

## Riscos e decisões para o Kaik
1. **Bug P1 ("Novo Tipo" com tipo selecionado, handoff recomendado).** (a) esperar a correção do time do app e gravar os seis tipos ao vivo; (b) gravar só o primeiro ao vivo e o resto entra por seed (plano acima). Recomendo (b) e abrir o handoff em paralelo. Confirmar rodando antes de decidir (inventário 7.1).
2. **Aba Fiscal é do módulo Nota Fiscal (🔒).** Manter o bloco 5 com o aviso "aparece para quem tem o módulo", ou mover para o T14? Precisa do handler `nfse-tax-codes`.
3. **Vídeo e limite:** a 1.38.6 mostra "Vídeo" para todos e não aplica nem mostra limite; o guia técnico do app diz o contrário. A fala cita só o clipe curto. Alinhar com o time se a trava volta (afeta o aviso 🔒 da trilha).
4. **"Frequência" e Catálogo PMOC** aparecem por causa de Contratos: uma frase e remeter ao tutorial de Contratos, ou esconder a câmera dali?
5. **Duração (20–22 min × 30 min da trilha):** cortar blocos 6 e 12 ou manter tudo?
6. **Handoffs a abrir:** P1 (alta); P3 (vocabulário "Template", "Excluir" que desativa, lixeira sem texto), P4 (prévia do prefixo `-2026-0001` ≠ código real sem zeros), P6 (permissão "Checklists" sem efeito).
7. Nome "Glacial Cold" aparece num comentário de migration do app como cliente real (inventário 7.8): confirmar que está tudo bem.
