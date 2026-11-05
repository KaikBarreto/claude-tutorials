# Roteiro T22 · Ferramentas de RH: DISC, Organograma, Fluxograma

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`,
gerado por script a partir desta coluna. Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela
(`T22/inventario.md`, conferido de novo contra o código da 1.38.6).
Aula no computador (janela de 1280×800), logada como Camila Duarte (admin), menos o capítulo 2, que abre o link do teste sem login, no celular do técnico (gravação no celular do T7). Todo capítulo parte de um navegador novo, com o mundo do fim do capítulo anterior (sementes `seeds-extra/t22/apos-capNN.json`); quando um capítulo continua uma tela aberta no anterior, o `setup` do robô a reabre fora do vídeo.
Tudo fictício: pessoas, respostas do teste, perfis, organograma e fluxograma. A fala não cita o código do perfil (ele sai das respostas do robô), datas nem as pessoas reais que o app usa como exemplo de cada fator (P6).

- **Título final:** Ferramentas de RH: DISC, Organograma, Fluxograma (o nome da TRILHA, que o cartão final do T15 usa; o plano sugeria "Ferramentas de RH: perfil comportamental, organograma e fluxograma")
- **Vinhetas (áreas):** PERFIL COMPORTAMENTAL · ORGANOGRAMA · FLUXOGRAMA · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Funcionários: Financeiro do Funcionário e Ponto Eletrônico (T15)
- **Próximo:** Integração com WhatsApp (T21, na ordem de exibição)
- **FAKE_NOW:** `2026-11-12T10:00:00-03:00` (quinta-feira), o dia em que o T15 termina, no backend falso e no robô. Motivo: as duas avaliações do Bruno (15/05/2026 e 05/11/2026) ficam no passado, e a do Rafael sai "Respondido em 12/11/2026". O T21 parte do mesmo dia, à tarde.
- **Duração estimada:** ~9 min de vídeo (1.224 palavras de fala, ~7,8 min de voz a 2,6 palavras/s, mais 11 vinhetas, o teste no celular e o desenho do organograma e do fluxograma, que a edição acelera; o plano previa ~14 min, a fala segue o tempo natural)
- **Estado inicial (fim do T15):** `seeds-extra/t15/apos-cap12.json`: Glacial Cold Brasil, Camila Duarte (admin) logada; os sete funcionários (a **Tatiane Ribeiro**, "Assistente administrativa", CLT; os seis técnicos, "Técnico de refrigeração"); a Equipe Alfa do T5 (Bruno Alves e Lucas Ferreira); nenhum organograma, fluxograma ou avaliação além da semente abaixo. O padrão da empresa "Funcionário vê o resultado ao final" fica ligado (`company_settings.disc_show_result_to_employee`, padrão `true`; conferido nas duas portas de cadastro e no `seed_company_catalog`: nada de DISC, organograma ou fluxograma nasce com a empresa, inventário 0.4).
  Como em toda aula que entra pelo Dashboard depois do T12, o `storage` de cada capítulo leva a marca `dominex:portal-tickets-seen:<id da Camila>`.
- **Por semente (bastidor, `seeds-extra/t22/inicio.json`):** duas avaliações respondidas do **Bruno Alves** (15/05/2026 e 05/11/2026), com `scores`, `profile_code`, `primary_type`, `secondary_type`, `completed_at` e `public_short_code` de 12 caracteres, diferentes em pelo menos um fator, para o "Comparar" e a "Evolução do perfil" terem o que mostrar (P7; decisão 4).
- **Criado ao vivo:** a avaliação DISC do **Rafael Lima** (link gerado com "Funcionário vê o resultado ao final" em "Sim", respondida no celular, perfil saído das respostas do robô); o organograma **Estrutura 2026** (Camila Duarte, caixa manual, "Diretora", setor Direção → Tatiane Ribeiro, setor Escritório, e Rafael Lima, setor Campo → Bruno Alves, Júlia Santos, Lucas Ferreira, Marina Costa e Paulo Souza, setor Campo pelo "Aplicar aos de baixo"; a caixa de texto "Equipe Alfa: Bruno e Lucas"); o fluxograma **Atendimento de chamado do portal** (8 formas: "Chamado aberto no portal", "Triagem do chamado", "Precisa de visita?", "Agendar visita e técnico", "Executar a visita", "Relatório de Serviço", "Orientar o cliente por telefone" e "Chamado encerrado"; "Sim" e "Não" nas saídas da decisão; as raias Escritório e Campo; a triagem com "Como fazer", a Tatiane como responsável e "2h"; em "Sobre o processo", o objetivo "Responder todo chamado do portal em até um dia útil", o disparo "Cliente abre chamado no Portal do Cliente", a dona Tatiane Ribeiro, a área Atendimento e a frequência "Por demanda").
- **Estado final:** como o inicial, mais o que foi criado. Vira `seeds-extra/t22/apos-cap11.json` (igual ao `apos-cap10`); o T21 parte dele (nada daqui é usado depois); atualizar `MUNDO_FICTICIO.md`.
- **Sementes entre capítulos:** `inicio` (entrada dos capítulos 0 e 1), `apos-cap01` (a avaliação do Rafael pendente; entrada do 2), `apos-cap02` (a avaliação respondida; entrada dos capítulos 3 a 6), `apos-cap06` (o organograma com as pessoas; entrada do 7), `apos-cap07` (o arranjo e a caixa; entrada do 8), `apos-cap08` (o fluxograma com as formas, as conexões e os rótulos; entrada do 9), `apos-cap09` (as raias e a triagem detalhada; entrada do 10), `apos-cap10` ("Sobre o processo"; entrada do 11); os capítulos 3, 4, 5 e 11 só leem. O organograma e o fluxograma são gravados pelo próprio app (`org_charts.data`, `processes.data` e `meta`), então cada semente sai da gravação do capítulo anterior.
- Decisões padrão (`plano.md` → "Riscos e decisões", proposta recomendada; com duas opções, a mais simples sem rosto, senha nem dado real):
  **o cursor nunca pousa nos gráficos DISC** (decisão 1 e alinhamento do `PRODUCAO.md`: o tooltip de cada fator cita pessoas reais, P6): a câmera enquadra o gráfico com o cursor fora dele, e o mesmo vale para os gráficos cruzados do "Comparar" e os da "Evolução do perfil"; PDFs em nova aba (decisão 2): sem a gravação de nova aba, "Ver PDF", "Ver comparação" e "Baixar POP em PDF" ficam só em zoom e a fala descreve o documento (a fala vale também se a nova aba for desenvolvida e o POP aparecer); teste no celular, como o ponto do T15 (decisão 3); duas avaliações antigas do Bruno na semente (decisão 4); os achados de segurança vão para o time do app (decisão 5); a fala não usa "publicar" (decisão 6, P8); os 12 blocos ficam (decisão 7).
  A conferência do código da 1.38.6 mudou quatro coisas do plano:
  (1) o "+" das bordas de uma caixa cria um subordinado (embaixo e dos lados) ou um chefe (em cima), nunca um colega ao lado (`components/employees/orgchart/OrgChartCanvas.tsx:603-650`), e o "Aplicar aos de baixo" copia o setor e a cor para todos os descendentes (`:764-776`): por isso o Rafael fica de referência do campo, com os outros técnicos embaixo dele, e um clique dá o setor Campo aos cinco;
  (2) no fluxograma, a forma nova nasce solta perto do centro (`components/employees/processes/ProcessCanvas.tsx:580-622`), e a conexão e a entrada numa raia são por arrasto (`:496`, `:542-556`): o robô precisa do passo `drag` no React Flow (plano B no capítulo 8: corte para o desenho já ligado, por semente, com a mesma fala);
  (3) "Ver PDF" e "Ver comparação" entram nos capítulos 3 e 4, onde a tela já está, e o capítulo 5 vira a evolução do perfil do Bruno;
  (4) o "Organizar" do fluxograma "Desfaz o arranjo manual" (`lib/i18n/messages/app/processes.ts:84`): depois das raias, o robô só usa o "Formatar", e o "Organizar" fica em zoom.
  Handoffs (a fala não depende deles): aviso do DISC que fala em ponto (P5); "pronto para ser publicado" sem publicar e o POP sempre "Versão 1" (P8); sem compartilhar (P9); rótulos da barra do fluxograma no limite de 1280 px (P10); pessoas reais no tooltip do gráfico DISC (P6); segurança P1 a P3 (`TRILHA.md`, achado 8).
  Pronúncias a testar antes de gerar a voz: DISC "disque" e POP "pópi" (novas); PDF "pê-dê-éfe" e PNG "pê-ene-gê" (T1); RH "érre-agá" (T1); os fatores são lidos pelo nome (Dominância, Influência, Estabilidade e Conformidade); "Estrutura 2026" é dito "Estrutura dois mil e vinte e seis"; "Funcionários / RH", "Funcionários e RH" (a legenda volta a escrever a barra).
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar), `[handoff: ...]` (texto ou comportamento do app para o time corrigir; a fala não depende dele).

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "Ferramentas de RH: DISC, Organograma, Fluxograma". | (sem fala) |
| Dashboard da Dominex, logada como Camila Duarte (sem enquadrar "Requer Atenção"); menu "Gestão" → "Funcionários": "Funcionários (RH)"; zoom nas abas "Perfil Comportamental", "Organograma" e "Fluxograma". [BACKEND: semente `seeds-extra/t22/inicio.json`] | Oi! Neste tutorial a gente vai usar as três ferramentas de RH da Dominex: o perfil comportamental, o organograma e o fluxograma. |
| A câmera passa pelas três abas, uma a uma. | Uma ajuda a entender o jeito de cada pessoa, a outra mostra quem responde a quem, e a terceira documenta como o trabalho acontece, com o procedimento pronto pra equipe. |
| Cartão discreto: "Módulo Funcionários / RH". | As três ficam na tela de Funcionários e fazem parte do módulo Funcionários / RH. |
| Cartão discreto: "Antes: Funcionários: Financeiro do Funcionário e Ponto Eletrônico". | Se você ainda não viu o tutorial de Funcionários, com o financeiro e o ponto eletrônico, dá uma olhada antes. [pause] Vamos começar pelas pessoas. |

### cap01 · O teste DISC (vinheta: PERFIL COMPORTAMENTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo, logada (semente `inicio`); clique na aba "Perfil Comportamental": "Perfil Comportamental da Equipe" ("Perfis DISC de todos os funcionários ativos"), um cartão por funcionário ativo: "Sem teste" com "Gerar link", e o do Bruno Alves já respondido (o código do perfil, as barras dos fatores e "Respondido em 05/11/2026"); o cursor fica longe das barras. | O perfil comportamental usa o teste DISC. Ele mostra como cada pessoa age no dia a dia, em quatro fatores: Dominância, Influência, Estabilidade e Conformidade. |
| Zoom no cartão do Bruno Alves. | Troco pra grade, e cada pessoa da equipe ganha um cartão. O Bruno já respondeu, e o cartão dele mostra o resultado. |
| No cartão do Rafael Lima ("Sem teste"), clique em "Gerar link": janela "Gerar link de avaliação" com "Funcionário vê o resultado ao final" em "Sim" e a dica "Você pode mudar isso a cada avaliação. O padrão vem das configurações da empresa.". | Agora o Rafael. Clico em Gerar link, e aqui você decide se a pessoa vê o resultado no final. O padrão vem das configurações da empresa, e dá pra mudar a cada teste. |
| Clique em "Gerar link": aviso "Link gerado e copiado!" (com o endereço, sem zoom); o cartão passa a "Aguardando resposta", com "Copiar link". [BACKEND: `INSERT disc_assessments` (pending, `show_result_to_employee` true) com o `public_short_code` de 12 caracteres que o gatilho do banco geraria (`supabase/migrations/20260620200000_public_short_codes_links_amigaveis.sql`); endereço do app nos links (`TRILHA.md`, trabalho comum 7); vira `apos-cap01`] | O link já vem copiado. Ele é só do Rafael e abre sem login, então manda direto pra ele, como uma mensagem pessoal. |

### cap02 · Respondendo pelo celular (vinheta: PERFIL COMPORTAMENTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap01`), no celular (viewport e moldura genérica do T7, sem login): o link do Rafael abre "Teste de Perfil Comportamental (DISC)", com "Leva cerca de 5 minutos. Responda pensando no seu dia a dia.", "Olá, Rafael!" e "Como funciona". [BACKEND: RPC `get_disc_public` (marca da Glacial, primeiro nome, nome completo, `status` pending e `show_result_to_employee` true); edge `disc-photo` responde 404 e a tela cai nas iniciais] | No celular do Rafael, o link abre o teste. Leva uns cinco minutos, e ele responde pensando no dia a dia dele. |
| Zoom em "Como funciona": as perguntas de escala e de escolha e "Não existe resposta certa ou errada, nem perfil melhor ou pior. Responda pensando no que é mais parecido com você de verdade.". | São perguntas de escala, de nada a ver comigo até tudo a ver comigo, e de escolha. E vale a resposta mais parecida com ele de verdade, sem certo nem errado. |
| Toque em "Começar": "Pergunta 1 de 28"; o robô responde as de escala pelo teclado (1 a 5 e Enter) e toca nas alternativas; trecho acelerado (selo 4x) até a última. [celular no robô, como no T15; respostas fixas no roteiro do robô (P11)] | Começar. São vinte e oito perguntas, uma por tela, e o Voltar deixa mudar uma resposta. |
| Na última, toque em "Enviar respostas" ("Enviando..."): "Seu perfil comportamental", com o relatório dele. [BACKEND: RPC `submit_disc_assessment` grava as respostas, a pontuação calculada no navegador e o perfil, e devolve o resultado (`pages/DiscAssessmentPublic.tsx:203-224`); vira `apos-cap02`] | No fim, Enviar respostas. Como o resultado está liberado, ele já vê o próprio perfil. |

### cap03 · Lendo o perfil (vinheta: PERFIL COMPORTAMENTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo, no computador (semente `apos-cap02`); aba "Perfil Comportamental": o cartão do Rafael com o perfil e "Respondido em 12/11/2026" (o cursor longe das barras); clique em "Ver detalhes". | De volta ao computador, o perfil do Rafael já chegou. Clico em Ver detalhes. |
| A ficha abre com a lista da equipe à esquerda e a sub-aba "Visão geral": o perfil (código e nome), "Sobre o seu perfil" e o "Gráfico DISC", enquadrado com o cursor fora dele (P6). | No alto vem o perfil dele, com um resumo do estilo. O gráfico mostra o peso de cada um dos quatro fatores. |
| Zoom em "Qualidades" e "Pontos de atenção". | Logo abaixo, as qualidades e os pontos de atenção. |
| A câmera desce por "Competências Comportamentais", "Perfil emocional", "Onde brilha", "Como liderar e comunicar", "O que evitar", "Comunicação ideal" e "Sob estresse" (cursor fora dos gráficos). | Depois vêm as competências, o perfil emocional, onde a pessoa brilha e como liderar e se comunicar com ela. Isso ajuda muito na hora de passar uma tarefa ou de dar um retorno. |
| Zoom em "Motivadores de carreira" ("Fator predominante" e "Fator de apoio") e no aviso "Esta é uma ferramenta de autoconhecimento e comunicação de equipe. Não é um teste clínico nem um diagnóstico. Nenhum perfil é melhor ou pior que outro.". | No fim, os motivadores de carreira. E repara no aviso: é uma ferramenta de autoconhecimento e de comunicação da equipe, e nenhum perfil é melhor que outro. |
| Zoom em "Ver PDF", no cabeçalho da ficha, sem clicar (abre o dossiê em nova aba; decisão 2). | E pra levar pra uma conversa, o Ver PDF gera o dossiê completo do perfil. |

### cap04 · Interações e comparação (vinheta: PERFIL COMPORTAMENTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); o `setup` abre o perfil do Rafael fora do vídeo. Clique na sub-aba "Interações": "Como se comporta com" ("Escolha outro funcionário para ver a dinâmica entre os dois perfis."); em "Selecione um funcionário" escolhe "Bruno Alves". | Imagina que o Rafael e o Bruno vão juntos numa instalação. Em Interações, escolho o Bruno pra ver como os dois funcionam juntos. |
| Zoom em "Atritos", "Sinergias" e "Melhor comunicação". | Aparecem os dois perfis no mesmo gráfico, os atritos que podem surgir, as sinergias e a melhor forma de comunicação entre os dois. Ajuda bastante a montar as duplas de campo. |
| Zoom em "Ver comparação", sem clicar (abre o PDF da dupla em nova aba). | E o Ver comparação gera o PDF da dupla. |
| Clique em "Voltar"; na aba "Perfil Comportamental", clique em "Comparar" (aparece com dois ou mais perfis respondidos): "Comparar perfis" ("Selecione dois funcionários para ver a dinâmica entre eles."); em "Primeiro funcionário" escolhe "Rafael Lima" e em "Segundo funcionário", "Bruno Alves". | Volto pra aba Perfil Comportamental. Com dois perfis respondidos, ela ganha o Comparar. Escolho o Rafael e o Bruno. |
| "Gráfico DISC cruzado" e "Radar de competências cruzado" enquadrados com o cursor fora deles; a câmera desce por "Atritos", "Sinergias" e "Melhor comunicação"; clique em "Voltar". | Os dois perfis ficam no mesmo gráfico, com as competências de cada um lado a lado. |

### cap05 · A evolução do perfil (vinheta: PERFIL COMPORTAMENTAL)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); aba "Perfil Comportamental": no cartão do Bruno Alves, clique em "Ver detalhes"; clique na sub-aba "Histórico". | E o perfil muda com o tempo. O Bruno já fez o teste duas vezes, e no Histórico dele dá pra ver o que mudou de uma pra outra. |
| "Histórico de avaliações" e "Evolução do perfil": o gráfico e o radar de cada avaliação, com o texto "Comparando com a avaliação anterior: ..." (cursor fora dos gráficos). | A evolução do perfil compara a avaliação de agora com a anterior e explica em palavras o que subiu e o que recuou. |
| Zoom na "Linha do tempo", com "Ver desta data". | E na linha do tempo, cada avaliação fica guardada, pra abrir quando quiser. |
| Zoom em "Nova avaliação" ("Ao responder a nova avaliação, ela vira o perfil atual e a atual vai para o histórico."), sem clicar. | Uma dica: refazer o teste de tempos em tempos mostra o crescimento da pessoa. É só clicar em Nova avaliação. |

### cap06 · Montando a estrutura (vinheta: ORGANOGRAMA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap02`); clique na aba "Organograma": "Monte a estrutura da sua empresa em um quadro visual" e "Nenhum organograma ainda"; clique em "Novo Organograma": em "Nome do organograma" ("Ex: Estrutura 2026") digita "Estrutura 2026"; clique em "Criar". [BACKEND: `INSERT org_charts` com o `public_short_code` de 12 caracteres] | Agora, quem responde a quem: o organograma. Clico em Novo Organograma e dou um nome, Estrutura dois mil e vinte e seis. |
| O quadro abre com a caixa "Direção" e o selo "Salvo"; clique na caixa: painel "Editar nó"; em "Nome" digita "Camila Duarte", em "Cargo", "Diretora", e em "Setor", "Direção". | O quadro já nasce com a primeira caixa, a Direção. Clico nela e coloco a Camila, que é a diretora. |
| Passa o cursor na caixa da Camila e clica no "+" de baixo: janela "Adicionar nó", aba "Funcionário"; em "Buscar funcionário..." digita "Tatiane" e clica em "Adicionar": a caixa da Tatiane Ribeiro entra ligada embaixo da Camila, com as iniciais, o nome e o cargo. [TESTAR: o "+" só aparece com o cursor sobre a caixa] | No botão de mais, embaixo da caixa, entra quem responde a ela. Escolho a Tatiane na lista de funcionários, e ela entra já ligada. |
| Clique na caixa da Tatiane: "Editar nó" com a dica "Nome, cargo e foto vêm do cadastro do funcionário."; em "Setor" digita "Escritório" e escolhe uma cor em "Cor do setor". | O nome, o cargo e a foto vêm do cadastro. Aqui eu só coloco o setor, Escritório, com uma cor. |
| "+" de baixo da Camila → "Rafael Lima"; "+" de baixo do Rafael → Bruno Alves, Júlia Santos, Lucas Ferreira, Marina Costa e Paulo Souza, um por vez (trecho acelerado, selo 4x; cada "+" reorganiza a ramificação). | No campo, o Rafael fica de referência, e embaixo dele entram os outros técnicos. |
| Clique na caixa do Rafael: em "Setor" digita "Campo" e escolhe uma cor; clique em "Aplicar aos de baixo": as cinco caixas ganham o setor e a cor. | Coloco o setor Campo no Rafael e clico em Aplicar aos de baixo. Pronto, todo mundo embaixo dele ficou no campo. |
| Zoom no selo "Salvando…" e depois "Salvo". [BACKEND: `UPDATE org_charts.data` com o grafo (debounce de ~800 ms); vira `apos-cap06`] | E repara no selo: o quadro salva sozinho a cada mudança. |

### cap07 · Organizar e encontrar (vinheta: ORGANOGRAMA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap06`); o `setup` abre a "Estrutura 2026" fora do vídeo. Clique em "Organizar" ("Reposiciona automaticamente em árvore"): o quadro se arruma. | Com as pessoas no lugar, o Organizar arruma tudo em árvore, sozinho. |
| Clique em "Adicionar caixa": entra "Nova caixa"; clique nela: em "Texto da caixa" digita "Equipe Alfa: Bruno e Lucas"; arrasta a caixa para perto dos dois. [TESTAR: o passo `drag` no React Flow; plano B: a caixa fica onde nasce] | E o Adicionar caixa põe uma anotação no quadro. Aqui eu lembro que o Bruno e o Lucas formam a Equipe Alfa. |
| Clique em "Tela cheia": o quadro ocupa a tela; abre "Ferramentas": "Adicionar caixa", "Árvore", "Destacar por setor" e "Buscar pessoa". | Na lateral ficam as ferramentas pra ler um organograma grande, e em Tela cheia o quadro ocupa a tela toda. |
| Clique em "Árvore": o painel "Hierarquia", com as pessoas em lista, "Expandir tudo", "Recolher tudo" e o total de pessoas; fecha. | A Árvore mostra a hierarquia em lista, como um índice. |
| Clique em "Destacar por setor" e escolhe "Campo": as caixas do campo ficam em destaque; clique em "Limpar destaque". | O Destacar por setor acende um setor só. |
| Clique em "Buscar pessoa": em "Nome ou cargo..." digita "Júlia": o quadro vai até a caixa da Júlia Santos; sai da tela cheia. | E o Buscar pessoa leva direto até alguém. |
| Clique em "Exportar": abre "Baixar imagem (PNG)", "Baixar PDF" e "Sai no tema atual", sem clicar (os dois baixam arquivo); fecha. [BACKEND: `UPDATE org_charts.data` com o arranjo e a caixa; vira `apos-cap07`] | Pra imprimir ou mandar pra alguém, o Exportar baixa o organograma em imagem ou em PDF. |

### cap08 · Desenhando a rotina (vinheta: FLUXOGRAMA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap07`); clique na aba "Fluxograma": "Desenhe os processos da empresa em um fluxograma e documente como cada etapa deve ser feita." e "Nenhum fluxograma ainda"; clique em "Novo fluxograma": em "Nome do fluxograma" ("Ex.: Abertura de ordem de serviço") digita "Atendimento de chamado do portal"; clique em "Criar fluxograma". [BACKEND: `INSERT processes` com o `public_short_code`] | Por fim, como o trabalho acontece: o fluxograma. Vou desenhar o atendimento de um chamado que o cliente abre no portal. Clico em Novo fluxograma e dou o nome. |
| O quadro abre com a forma "Início" no meio; clique nela: painel "Editar etapa"; em "Nome da etapa" digita "Chamado aberto no portal". [TESTAR: os rótulos da barra aparecem em 1280 px (P10)] | Ele já nasce com o Início. Clico nele e escrevo o que dá a largada: o chamado aberto no portal. |
| Clique em "Adicionar forma": a lista "Início", "Tarefa", "Decisão", "Subprocesso", "Documento", "Espera", "Fim" e "Observação", cada uma com a dica; zoom em "Tarefa" ("Use para uma etapa comum, feita por alguém.") e "Decisão" ("Use quando o caminho muda conforme uma condição, como Sim ou Não."). | No Adicionar forma ficam as formas do desenho: início, tarefa, decisão, subprocesso, documento, espera, fim e observação. A Tarefa é uma etapa comum, e a Decisão é quando o caminho muda, com sim ou não. |
| Adiciona e nomeia pelo "Editar etapa" (trecho acelerado): "Tarefa" "Triagem do chamado", "Decisão" "Precisa de visita?", "Tarefa" "Agendar visita e técnico", "Tarefa" "Executar a visita", "Documento" "Relatório de Serviço", "Tarefa" "Orientar o cliente por telefone" e "Fim" "Chamado encerrado"; cada forma nasce perto do centro e o robô a arrasta para o lugar. | Então eu monto o caminho: a triagem, a decisão se precisa de visita, o agendamento, a visita, o relatório e o fim. E, se não precisar de visita, a orientação por telefone. |
| Liga as formas em ordem, puxando da borda de uma até a outra (passo `drag`); nas duas saídas de "Precisa de visita?", clica na conexão e digita "Sim" e "Não" em "Rótulo (ex.: Sim, Não)". [TESTAR: o `drag` entre os puxadores do React Flow; plano B: corte para o desenho já ligado (semente `apos-cap08`), com a mesma fala] [BACKEND: `UPDATE processes.data`; vira `apos-cap08`] | As setas ligam uma etapa na próxima: é só puxar da borda de uma forma até a outra. E na decisão, cada saída ganha um rótulo, sim ou não. |

### cap09 · Raias e responsáveis (vinheta: FLUXOGRAMA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap08`); o `setup` abre o fluxograma fora do vídeo. Clique em "Adicionar raia" duas vezes; em "Nome da raia (setor ou responsável)" digita "Escritório" e "Campo"; arrasta cada forma para a raia de quem faz: a triagem, o agendamento e a orientação no Escritório; a visita e o relatório no Campo. [TESTAR: o `drag` das formas para dentro da raia] | Agora, quem faz cada parte. Com Adicionar raia, eu crio uma faixa pra cada responsável, Escritório e Campo, e coloco cada etapa na faixa de quem faz. |
| Clique em "Triagem do chamado": "Editar etapa"; em "Como fazer" digita "Ler o chamado, conferir o equipamento e decidir se precisa de visita."; em "Responsável" escolhe "Tatiane Ribeiro"; em "Duração" ("Ex.: 48h, 2 dias úteis") digita "2h". | Em cada etapa dá pra detalhar. Na triagem, escrevo como fazer e escolho a Tatiane como responsável. |
| Clique em "Formatar" ("Alinha as caixas, encaixa na grade e faz as setas saírem pelo lado certo, sem mexer no seu arranjo."); zoom em "Organizar", sem clicar (refaz o arranjo do zero). | Com as etapas nas faixas, o Organizar refaz o arranjo da esquerda pra direita. Depois, o Formatar só alinha as caixas e as setas, sem mexer no desenho. |
| Zoom no selo "Salvo". [BACKEND: `UPDATE processes.data`; vira `apos-cap09`] | E aqui também tudo salva sozinho. |

### cap10 · Conferência e POP (vinheta: FLUXOGRAMA)

| Tela | Fala |
| --- | --- |
| Capítulo novo (semente `apos-cap09`); o `setup` abre o fluxograma fora do vídeo. Clique em "Conferência do fluxograma": "Nenhum problema encontrado. O fluxograma está pronto para ser publicado." (sem zoom na segunda frase). [handoff: não existe publicar (P8)] | Desenho pronto, vamos conferir. No ícone do escudo, a Conferência do fluxograma procura etapa solta, decisão sem caminho ou fluxo sem fim, e leva você direto até ela. Aqui está tudo certo. |
| Clique em "Sobre o processo": em "Objetivo" digita "Responder todo chamado do portal em até um dia útil"; em "Disparo", "Cliente abre chamado no Portal do Cliente"; em "Dono do processo" escolhe "Tatiane Ribeiro"; em "Área" digita "Atendimento" e em "Frequência", "Por demanda". [BACKEND: `UPDATE processes.meta`; vira `apos-cap10`] | No ícone da prancheta, o Sobre o processo guarda o objetivo, o que dispara o processo, o dono, a área e a frequência. Aqui, escrevo a Tatiane como dona. |
| Clique em "Exportar": "Exportar como imagem", "Exportar como PDF" e "Baixar POP em PDF"; zoom em "Baixar POP em PDF", sem clicar (abre em nova aba; decisão 2: com a gravação de nova aba, mostrar o POP com a mesma fala). | E daqui sai o POP, o procedimento operacional padrão. O Baixar POP em PDF gera o documento pronto pra equipe. |
| A câmera fica no menu aberto (ou percorre o POP, se a nova aba for gravada: "Procedimento Operacional Padrão", "Responsabilidades", "Fluxograma" e "Descrição das etapas"); fecha. | Ele traz o objetivo, os responsáveis de cada faixa, o desenho e o passo a passo de cada etapa. E como sai do desenho, é só manter o fluxograma em dia que o procedimento acompanha. |

### cap11 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: o perfil do Rafael (cursor fora do gráfico). | Pronto! Recapitulando: a gente mandou o teste DISC pro Rafael, ele respondeu pelo celular, e o perfil chegou com as qualidades, os pontos de atenção e o jeito de liderar. |
| Montagem rápida: as interações, o "Comparar" e a evolução do Bruno. | Depois viu as interações entre dois colegas, a comparação e a evolução de um perfil ao longo do tempo. |
| Montagem rápida: o organograma em tela cheia. | No organograma, montou a estrutura da Glacial com os setores e viu como encontrar cada pessoa. |
| Montagem rápida: o fluxograma com as raias e o menu "Exportar". | E no fluxograma, desenhou o atendimento de um chamado com os responsáveis, conferiu o desenho e viu de onde sai o POP. |
| Cartão "Próximo: Integração com WhatsApp"; cartela final. | No próximo tutorial, a gente conecta o WhatsApp da empresa pra avisar o cliente sozinho, a cada passo da ordem de serviço. Até lá! |
