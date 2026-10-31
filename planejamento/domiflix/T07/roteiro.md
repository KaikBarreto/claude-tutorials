# Roteiro T7 · O técnico em campo

Roteiro pronto para gerar a voz e gravar (molde T3; sem etapa de aprovação, pedido do Kaik de 30/10 22:44). Coluna Fala = texto
da narração (voz Fernanda, ElevenLabs), na grafia da legenda; a grafia de pronúncia do TTS é aplicada em `narracao/tts_textos.py`.
Coluna Tela = o que o robô faz e onde a câmera foca, com os rótulos entre aspas como na tela (`T07/inventario.md`).
A aula inteira é gravada no celular (página em layout de celular, 390×844; a moldura genérica do aparelho é feita na edição), logado como Rafael Lima.
Todos os nomes, valores e datas são fictícios; o dia da gravação é a quarta-feira da OS #16 (`FAKE_NOW` igual no backend falso e no robô, às 08:50).

- **Título final:** O técnico em campo
- **Vinhetas (áreas):** TÉCNICO EM CAMPO · RELATÓRIO · VISÃO DO CLIENTE · RESUMO (todos os capítulos, menos o 0, têm vinheta, como no T3)
- **Antes:** Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo (T5)
- **Próximo:** Área do Técnico: Refrigeração e Climatização (T18)
- **Duração estimada:** ~13 min de vídeo (1.843 palavras de fala, ~11,8 min de voz a 2,6 palavras/s, mais vinhetas e pausas do robô; o plano previa 17 a 19 min, a fala segue o tempo natural)
- **Estado inicial (fim do T5):** Glacial Cold Brasil com 16 clientes, os técnicos Rafael Lima, Bruno Alves, Júlia Santos, Lucas Ferreira, Marina Costa e Paulo Souza (Rafael com o cargo
  "Técnico de Campo"), a Equipe Alfa, o checklist "Manutenção preventiva de split" (13 perguntas, do T4) e a **OS #16** Manutenção Preventiva (Colégio Monte Verde, Hi-Wall 18.000 BTUs - Sala dos professores,
  Rafael Lima, **quarta 09:00 a 11:00**, **Pendente**, pesquisa de satisfação Sim); 15 OS de bastidor (uma pausada, do Paulo Souza), `nps_settings` e `nps_criteria` (Qualidade, Pontualidade, Profissionalismo)
  e cerca de 10 avaliações; "Consumo de estoque na OS" ligado (T1); White Label desligado.
- **Entra por seed "de bastidor", antes do cap01 (`seeds-extra/t7/`):** `public_short_code` fixo na OS #16 (endereço `/os-tecnico/<cliente>-<serviço>-<código>`); `service_order_assignees` (Rafael),
  `service_order_equipment` (com o checklist), `service_order_service_types` e `service_order_equipment_service_types` da #16, se o estado do T5 não os trouxer; telefone e **coordenadas do Colégio Monte Verde**
  (`latitude`/`longitude` e `lat`/`lng`); `stocks` ("Estoque Principal", `is_default`), `inventory` e `inventory_stock_levels` (Limpa-evaporador em spray 12 un, Fita isolante 30 rolos, Gás refrigerante R-410A 8,5 kg;
  nomes e saldos do `plano.md`, a combinar com o T8); perfil do Rafael com `company_id`; opcional: `user_permissions` do Rafael (esconde "Editar OS"). Sem preço de plano em nenhuma tela.
- **Criado ao vivo:** pontos `en_route`, `check_in`, `tracking` e `check_out` em `technician_locations`; check-in às 09:05 e check-out 85 minutos depois (salto de relógio, "Duração: 1h 25min");
  13 respostas em `form_responses` (1 foto, 1 assinatura); 2 linhas em `service_order_materials` (Limpa-evaporador em spray 2 un; Fita isolante 1 rolo, corrigida para 2 no resumo do consumo) que viram saídas em
  `inventory_movements` e baixam o saldo (10 un e 28 rolos); uma pausa, uma finalização parcial e duas retomadas; a OS #16 **Concluída**, com a linha de `service_ratings` e a avaliação enviada pelo link (nota 10, três critérios com 5 estrelas).
- **Estado final:** `seeds-extra/t7/apos-cap13.json` (um `apos-capNN.json` por capítulo que muda a #16); o T18 e o T8 partem dele (OS #16 Concluída, saldos 10 un e 28 rolos, avaliação 10).
- Decisões padrão: "Finalizar Parcial" mostrado na própria #16 (existe em toda OS em atendimento); a assinatura do cliente é a pergunta do checklist (a OS comum não tem o cartão "Assinaturas"), marcada `[TESTAR P23]`;
  a avaliação do cliente é enviada na aula; o PDF é só ilustrado (o download não é capturado); Waze e Google Maps só apontados; vídeo só falado (o checklist da aula não tem a pergunta); "Editar OS" pode aparecer
  no menu do Rafael e a fala não a cita; a pergunta de receita não aparece para o Rafael; o botão flutuante "Área do Técnico" é apresentado uma vez (cap01) e a aula segue.
- Marcas na coluna Tela: `[BACKEND: ...]` (o que o backend falso ainda não tem), `[TESTAR ...]` (o robô testa antes de gravar; inclui o que o robô ainda não faz no celular: emulação de aparelho, passos `geo` e `clock`),
  `[ILUSTRAÇÃO: ...]`.

### cap00 · Abertura

| Tela | Fala |
| --- | --- |
| Vinheta Domiflix com o título "O técnico em campo". | (sem fala) |
| Celular em pé no palco vertical (moldura genérica, sem marca), logado como Rafael Lima (técnico da Glacial Cold Brasil), na Agenda em "Dia" da quarta-feira: na lista, o cartão da OS #16 do Colégio Monte Verde às 09:00. [TESTAR: gravar em emulação de celular (`device` 390×844, toque marcado); a moldura é feita na edição] | Oi! Neste tutorial a gente vai acompanhar uma ordem de serviço pelo celular do técnico, do trajeto até o cliente à entrega do relatório. |
| A câmera acompanha o cartão da OS #16 na lista. | É assim que o trabalho de campo acontece: o técnico abre a ordem, preenche o atendimento, anota o material que usou e entrega o relatório ao cliente. Tudo no celular, com a ordem que a gente criou no tutorial anterior, e cada passo fica registrado na própria OS. |
| Cartão discreto: "Antes: Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo". | Se você ainda não viu o tutorial de Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo, dá uma olhada antes. [pause] Vamos começar pela agenda do técnico. |

### cap01 · Abrindo a OS no celular (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Toque no cartão da OS #16 (Colégio Monte Verde, "Manutenção Preventiva", selo "Pendente"): abre o painel "Resumo da OS" com cliente, data e hora, "Responsáveis" (Rafael Lima) e "Descrição". [BACKEND: seed `apos-cap17` do T5 mais `seeds-extra/t7/`: `public_short_code` fixo na OS #16, `service_order_assignees`, `service_order_equipment` (com o checklist), `service_order_service_types`, telefone e coordenadas do Colégio Monte Verde] | Vamos abrir a ordem. O técnico começa pela agenda, onde ele vê as ordens dele e as da equipe dele. Aqui está a OS número dezesseis, do Colégio Monte Verde, às nove da manhã. Tocando nela, abre o resumo, com o cliente, o horário, o responsável e a descrição do serviço. |
| Câmera no botão "Preencher OS"; toque: a tela da OS abre em tela cheia. A câmera percorre o cabeçalho na cor da marca: "Voltar", o selo "Pendente", "Glacial Cold Brasil", "OS #16", o chip "Manutenção Preventiva" em "Serviços desta OS" e a data com a hora. | O botão que leva ao atendimento é o Preencher OS. Toco nele, e a ordem abre em tela cheia. No alto, a faixa da empresa mostra o número da OS, o serviço, a data e a hora, e o status, que por enquanto é Pendente. |
| Rolagem lenta: cartão "Ir para o Atendimento" ("Informe ao cliente que você está a caminho ou faça o check-in ao chegar.") com os botões "A Caminho" e "Fazer Check-in" (sem tocar); cartão "Cliente" com o telefone, o ícone verde de WhatsApp e o endereço; "Descrição do Serviço". | Logo abaixo está o cartão Ir para o Atendimento, com os botões que a gente usa já já. Depois vêm os dados do cliente, com o telefone, o atalho de WhatsApp e o endereço, e a descrição do serviço. |
| Câmera no botão redondo da Área do Técnico, no canto inferior esquerdo (sem tocar). [TESTAR: o efeito do botão (WebGL) no Chromium headless; ele aparece em todas as telas da OS] | Esse botão redondo, no canto da tela, é a Área do Técnico, a caixa de ferramentas de refrigeração. Ela fica disponível durante o atendimento, e é o assunto do próximo tutorial. |
| A câmera volta ao cabeçalho da OS, no selo de status. | Uma dica: essa página é a mesma pro técnico, pro gestor e pro cliente. Quem abre o link sem fazer login vê a visão do cliente, e a gente chega nela no fim do tutorial. |

### cap02 · A Caminho e a rota (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Toque em "A Caminho". [TESTAR localização no celular emulado: `permissions: ["geolocation"]` e passo `geo` posicionando o aparelho na saída; o aviso do sistema pedindo a localização não aparece na gravação, a fala cobre] | Com a ordem aberta, o primeiro passo é ir até o cliente. Toco em A Caminho. Na primeira vez, é só permitir a localização quando o celular perguntar: é ela que registra o local do check-in e coloca o técnico no mapa. |
| Toast "Status atualizado: A Caminho!"; o selo vira "A Caminho"; o cartão passa a se chamar "Iniciar Atendimento" ("Chegou no local? Faça o check-in para iniciar."). [BACKEND: `technician_locations` aceita o ponto `en_route`; o endereço do ponto vem do Nominatim falso] | Pronto: o status mudou pra A Caminho, e o cartão agora é o Iniciar Atendimento. Enquanto a ordem está aberta no celular, a posição do técnico chega ao Mapa ao Vivo do gestor. |
| Câmera no cartão "Rota até o cliente": o mapa com a linha da rota até o colégio e o rótulo "~N min até o cliente (X km)". [BACKEND: coordenadas do Colégio Monte Verde, senão o destino vira o ponto genérico de Niterói] [TESTAR: mapa vetorial (WebGL) no Chromium headless, tiles de Niterói e rota do OSRM] | Logo abaixo aparece a Rota até o cliente. O mapa mostra o caminho, e o rótulo diz quantos minutos e quantos quilômetros faltam até o endereço. |
| Toque em "Ampliar": abre o "Mapa da rota em tela cheia"; toque no botão redondo de fechar (aria "Fechar mapa"). | Pra ver melhor, toco em Ampliar, e o mapa ocupa a tela toda. Fecho aqui no canto. |
| Câmera nos botões "Waze" e "Google Maps" (só apontar, sem tocar: abrem janela nova e levariam a gravação para fora do app). | Os botões Waze e Google Maps levam o trajeto direto pro aplicativo de navegação, com o endereço do cliente. |
| A câmera volta ao cartão "Iniciar Atendimento". | Uma dica: o A Caminho é opcional. Se o técnico já estiver no local, ele faz o check-in direto, a partir da ordem Pendente. |

### cap03 · Check-in (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Toque em "Fazer Check-in". [TESTAR: o passo `geo` leva o aparelho ao endereço do colégio antes do toque; o passo `clock` deixa o relógio do navegador em 09:05, para o carimbo do check-in] Toast "Check-in realizado com sucesso!"; o selo vira "Em Andamento". [BACKEND: `technician_locations` aceita `check_in`; hook de `service_orders` carimba `started_at` e o autor do check-in] | Chegou ao local? Então é hora do check-in. Toco em Fazer Check-in. O celular registra a hora e o lugar do atendimento, e o status passa pra Em Andamento. |
| Câmera na faixa "Check-in:" com o dia, a hora (09:05) e o endereço do ponto à direita. | Logo abaixo do cabeçalho fica o carimbo do check-in: o dia, a hora e o endereço onde o técnico estava. Esses dados vão pro relatório do cliente. |
| Rolagem: aparecem o cartão "Checklists" (o acordeão do equipamento) e, fixo embaixo, o rodapé preto com "Finalizar OS" (verde), "Finalizar Parcial" (laranja) e o botão hambúrguer (aria "Mais ações"). | Assim que o check-in é feito, a tela ganha o cartão de Checklists, com um checklist pra cada equipamento da ordem, e o rodapé preto, com Finalizar OS, Finalizar Parcial e o menu de mais ações. |

### cap04 · O checklist do equipamento (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Câmera no cartão "Checklists": acordeão "Hi-Wall 18.000 BTUs - Sala dos professores" aberto, com a categoria, o selo do serviço e o contador "0 de 13". Toque no botão "Manutenção preventiva de split": as perguntas abrem. [BACKEND: `form_templates`, `form_questions` e `form_template_service_types` do T4 no seed; `service_order_equipment` ligando o equipamento ao checklist] | Com o atendimento iniciado, é hora do checklist. Cada equipamento da ordem tem o seu. Aqui é o Hi-Wall dezoito mil BTUs da sala dos professores, e o checklist é o de Manutenção preventiva de split, que a gente importou no tutorial de Tipos de Serviço, Tipos de Tarefa e Checklists. O contador mostra as perguntas respondidas: por enquanto, zero de treze. |
| Nas cinco perguntas Sim/Não ("Filtros limpos / em bom estado?", "Serpentinas (evap/cond) sem sujeira excessiva?", "Dreno desobstruído e escoando?", "Fixações e suportes firmes?", "Conexões elétricas reapertadas e sem aquecimento?"), toque no interruptor de cada uma: vira o selo "Sim", com o lápis ("Editar resposta"). Câmera no asterisco vermelho. [Responder tudo "Sim": o primeiro toque grava "Sim"] | As primeiras cinco perguntas são de Sim ou Não: filtros, serpentinas, dreno, fixações e conexões elétricas. O asterisco vermelho marca as obrigatórias. É só tocar no interruptor, e a resposta vira Sim. |
| Câmera nos selos "Sim" e no contador que sobe (sem encenar queda de conexão). [BACKEND: cada resposta grava em `form_responses`; o `.single()` sem linha devolve 406 e o app cai no insert, igual ao app real] | Trabalhe com o celular conectado: cada resposta é gravada na hora, e se a internet cair o aplicativo avisa em vermelho que ainda não dá pra salvar. |
| Nos quatro campos de número ("Digite o valor..."): "Corrente do compressor medida" 7,6; "Pressão de baixa" 118; "Pressão de alta" 345; "Temperatura de insuflamento" 12. Depois de digitar cada um, toca fora do campo (é quando grava). | Depois vêm as medições, em campos de número. Digito a corrente do compressor, sete vírgula seis ampères, a pressão de baixa, cento e dezoito psi, e a de alta, trezentos e quarenta e cinco psi. Por último, a temperatura de insuflamento, doze graus Celsius. Cada valor grava quando eu toco fora do campo. |
| Em "Ruído / vibração anormal?", marca "Normal": aparece "1 selecionada". | No ruído e na vibração, marco Normal. Se precisar, dá pra marcar mais de uma opção. |
| Toque no lápis ("Editar resposta") de "Dreno desobstruído e escoando?": o interruptor reaparece; toque no visto ("Fechar edição"). O contador do equipamento mostra "10 de 13". | Uma dica: pra mudar uma resposta, é só tocar no lápis. O contador vai subindo conforme o técnico responde: já são dez de treze. |

### cap05 · Fotos e vídeo (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Rolagem até "Foto do equipamento": câmera nos botões "Tirar Foto" e "Galeria". | Algumas perguntas pedem foto. Aqui são dois botões: o Tirar Foto abre a câmera do celular, e a Galeria escolhe uma imagem que já está no aparelho. |
| Toque em "Galeria": o robô escolhe a foto de teste genérica, sem marca (passo `upload`); barra "Enviando... N%", toast "Foto enviada!"; a pergunta mostra "1 foto", a miniatura e a lixeira. O contador vai a "11 de 13". [TESTAR: o `upload` em campo de arquivo com `capture` na emulação de celular; plano B: apontar o passo direto para o campo da galeria] [BACKEND: o storage falso guarda o bucket `os-photos` em memória] | Vou pela galeria. A foto sobe com uma barra de progresso, o aplicativo avisa quando ela foi enviada, e a miniatura aparece na pergunta, com a lixeira, se for preciso apagar. |
| Câmera na pergunta de foto (sem ação). [Sem tela de vídeo: o checklist da aula não tem pergunta de vídeo] | Quando o checklist tem uma pergunta de vídeo, aparece o botão Gravar, pra registrar um clipe de até trinta segundos. O aplicativo deixa o vídeo mais leve antes de enviar. |
| Rolagem até "Recomendações ao cliente" (campo de texto, "Digite sua resposta..."): digita "Limpar os filtros a cada 30 dias e manter o dreno livre."; toca fora do campo; a resposta vira texto, com o lápis. O contador vai a "12 de 13". | A última pergunta antes da assinatura é de texto: as Recomendações ao cliente. O técnico escreve com as próprias palavras, toca fora do campo, e a resposta fica salva. |

### cap06 · Consumir do estoque (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Toque no botão hambúrguer do rodapé (aria "Mais ações"): o menu abre com as pílulas sobre o fundo desfocado ("Consumir do estoque", "Pausar OS", "Copiar link da OS" e "Sair do preenchimento"). Toque em "Consumir do estoque". [O menu pode trazer "Editar OS" como primeira pílula se o Rafael não tiver permissões gravadas: a fala não a cita] | Durante o serviço, o técnico anota os materiais que usou. Toco no menu de mais ações, aquele do rodapé, e escolho Consumir do estoque. |
| Abre a janela de baixo "Consumir do estoque"; câmera no subtítulo "Anote o que você usou. O estoque só baixa quando a OS for finalizada." | A própria janela já explica: o estoque só baixa quando a OS for finalizada. Até lá, o que o técnico anota é um rascunho que dá pra corrigir. |
| Toque em "Material" (placeholder "Escolha o material"): a lista mostra a busca "Buscar por nome ou código..." e cada material com "{qty} {unit} disponíveis" (Limpa-evaporador em spray, Fita isolante, Gás refrigerante R-410A); escolhe "Limpa-evaporador em spray"; em "Quantidade" digita 2; em "Observação (opcional)" digita "Limpeza da serpentina da evaporadora"; toque em "Adicionar": toast "Material anotado". [BACKEND: `stocks` com o "Estoque Principal" (`is_default`), `inventory` e `inventory_stock_levels`; com um estoque só, o campo "De onde saiu" não aparece] | Em Material, dá pra procurar pelo nome ou pelo código, e cada um mostra quanto tem disponível. Escolho o Limpa-evaporador em spray, coloco a quantidade, dois, e uma observação, se quiser. Toco em Adicionar, e o aplicativo avisa: Material anotado. |
| Escolhe "Fita isolante", "Quantidade" 1, "Adicionar": toast "Material anotado". A lista "Já registrado nesta OS" mostra as duas linhas, com "Editar" e "Remover" (sem tocar). | Faço o mesmo com a Fita isolante, um rolo. Os dois ficam na lista Já registrado nesta OS, e dali o técnico pode editar ou remover. |
| Toque em "Fechar". | Toco em Fechar. E lembra do Consumo de estoque na OS, que a gente ligou em Configurações, na aba Usabilidade? É ele que libera essa opção no menu. |

### cap07 · Pausar e retomar (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Hambúrguer, toque em "Pausar OS" (sem confirmação): toast "OS pausada com sucesso!"; o selo vira "Pausada"; aparece o cartão âmbar "OS Pausada" ("Esta OS foi pausada. Retome o atendimento para continuar o preenchimento."); o cartão de checklists fica esmaecido, com a faixa pedindo para retomar o atendimento. | Se o técnico precisar interromper o atendimento, ele pausa a ordem. No menu de mais ações, toco em Pausar OS. Pronto: a ordem fica Pausada, e o aplicativo avisa que é só retomar pra continuar o preenchimento. |
| Câmera no rodapé: só o botão "Retomar OS" e o hambúrguer. | O rodapé agora só tem o Retomar OS. Tudo que já foi preenchido continua salvo, e a ordem aparece em OS pausadas na agenda do gestor. |
| Toque em "Retomar OS": toast "OS retomada com sucesso!"; o selo volta a "Em Andamento"; o rodapé volta com "Finalizar OS" e "Finalizar Parcial". [BACKEND: hook de `service_orders` carimba `paused_at` e `resumed_at`] | Quando voltar ao serviço, toco em Retomar OS, e o atendimento segue de onde parou. |

### cap08 · Finalizar parcialmente (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Toque em "Finalizar Parcial" (laranja): abre "Finalizar parcialmente?" com "A OS ficará marcada como Parcialmente Concluída e aparecerá nas OS pausadas até ser concluída de verdade." e a nota "O que você já preencheu fica salvo. Você pode retomar e concluir quando terminar o serviço."; câmera nos dois textos. | E quando a visita não pode terminar no mesmo dia, existe o Finalizar Parcial, o botão laranja do rodapé. Ele abre uma confirmação: a ordem fica marcada como Parcialmente Concluída e aparece em OS pausadas até ser concluída de verdade. O que já foi preenchido fica salvo. |
| Toque em "Finalizar Parcialmente": toast "OS finalizada parcialmente"; a tela fecha e volta para a Agenda. | Confirmo em Finalizar Parcialmente. O aplicativo avisa, fecha a ordem e volta pra agenda. |
| Na Agenda, toque em "OS pausadas" (ícone de pausa com o contador): abre "OS Pausadas" ("Todas as ordens de serviço pausadas, independente da data.") com a OS #16 e "Pausada há ..."; toque em "Ver detalhes": painel "Resumo da OS"; toque em "Preencher OS": a tela abre com o selo "Parcialmente Concluída" e o rodapé só com "Retomar OS". [A lista pode trazer outras OS pausadas, como a do Paulo Souza: o robô abre só a da Monte Verde] | Na agenda, a ordem aparece em OS pausadas, com o tempo que faz que ela parou. Pra continuar, toco em Ver detalhes e depois em Preencher OS. O status agora é Parcialmente Concluída. |
| Toque em "Retomar OS": toast "OS retomada com sucesso!"; o selo volta a "Em Andamento". | Toco em Retomar OS, e o técnico continua de onde parou. |

### cap09 · A assinatura do cliente (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| Rolagem até a última pergunta, "Assinatura do cliente" (asterisco vermelho): campo branco para assinar. | De volta ao atendimento, falta a assinatura do cliente, a última pergunta do checklist. Pra pedir a assinatura, a gente usa uma pergunta de assinatura no checklist, marcada como obrigatória: assim a OS só é concluída com ela. |
| Traços curtos sobre o campo (passo `drag`, 2 a 3 vezes) desenhando a assinatura; aparecem "Limpar" e "Confirmar"; câmera no botão "Tela cheia" (sem tocar: abre em paisagem). [TESTAR: o `drag` desenha no campo] | O cliente assina com o dedo, direto na tela do celular. Quando ele começa a desenhar, aparecem o Limpar, pra recomeçar, e o Confirmar. E tem o Tela cheia, que abre o campo na horizontal, com mais espaço. |
| Toque em "Confirmar": a pergunta passa para o modo resposta e o selo do equipamento vira "Concluído" (verde). Toque no lápis ("Editar resposta") da pergunta: o campo mostra a imagem da assinatura (alt "Assinatura") com "Tela cheia" e "Limpar"; toque no visto ("Fechar edição"). [TESTAR P23: pela leitura do código (`DynamicFormQuestions.tsx:950-1047`), logo depois de "Confirmar" a pergunta em modo resposta imprime o valor gravado (o endereço de dados da imagem) como texto cru, e a imagem só reaparece no lápis; confirmar no app real antes de gravar. Se confirmar: handoff para corrigir, ou cortar na edição o quadro entre "Confirmar" e o lápis. A fala vale nos dois casos] | Toco em Confirmar, e o checklist do equipamento passa a Concluído. Pra rever a assinatura, é só tocar no lápis. |

### cap10 · Finalizar a OS (vinheta: TÉCNICO EM CAMPO)

| Tela | Fala |
| --- | --- |
| [TESTAR: o passo `clock` leva o relógio do navegador 85 minutos depois do check-in (10:30), para a "Duração:" sair "1h 25min", sem rajada de pontos de rastreamento e sem pop-up do dia] Toque em "Finalizar OS" (verde): abre o "Resumo do consumo" ("Confira o que saiu do estoque nesta OS. Dá para corrigir a quantidade antes de confirmar.") com um cartão por material: nome, "Estoque Principal", campo de quantidade com a unidade e "Fica com 10 un" (Limpa-evaporador em spray) e "Fica com 29 rolos" (Fita isolante). | Com tudo respondido, dá pra finalizar. Toco em Finalizar OS. Como o técnico anotou materiais, o aplicativo mostra antes o Resumo do consumo: o que vai sair do estoque e quanto fica de cada material. |
| Na linha "Fita isolante", troca a quantidade de 1 para 2: o texto passa a "Fica com 28 rolos". | Dá pra ajustar a quantidade aqui mesmo. Se a fita isolante foi de dois rolos, é só mudar o número, e o saldo que fica já se atualiza. |
| Toque em "Confirmar e finalizar": toasts "Materiais baixados do estoque" e "OS finalizada com sucesso!"; a tela vira o "Relatório de Serviço". [BACKEND: RPC `commit_os_material_consumption` (+ `register_inventory_movement`) grava as saídas e baixa o saldo para 10 un e 28 rolos; sem ela a tela diz "Materiais baixados do estoque" e nada baixa. Hook de `service_orders` carimba `completed_at` e o autor do check-out; a linha de `service_ratings` nasce no próprio app. A pergunta de receita não aparece para o Rafael] | Confirmo em Confirmar e finalizar. O estoque baixa, a ordem é concluída, o aplicativo registra o check-out, com a hora e o local, e o técnico já cai no Relatório de Serviço. |

### cap11 · O relatório e o PDF (vinheta: RELATÓRIO)

| Tela | Fala |
| --- | --- |
| Relatório de Serviço no topo: "OS #16", "Relatório de Serviço", a seção "Cliente" e "Equipamento(s)". | A ordem concluída vira o Relatório de Serviço. No alto estão o número da OS, o cliente e o equipamento atendido. |
| Rolagem até "Execução": "CHECK-IN" e "CHECK-OUT" com o nome Rafael Lima, a hora e o endereço de cada um, e "Duração: 1h 25min". | Em Execução ficam o check-in e o check-out, cada um com o nome de quem fez, a hora e o endereço. E logo abaixo, a duração do atendimento: uma hora e vinte e cinco minutos. |
| Rolagem pelas respostas por equipamento (os selos "Sim", os valores, "Normal", a foto em miniatura e o texto) e a seção "Assinaturas" com a assinatura do cliente e o carimbo de data, hora e local. [A seção "Registro Fotográfico" não aparece: a foto fica dentro das respostas] | Mais abaixo vêm as respostas do checklist, equipamento por equipamento, com a foto que o técnico anexou e a assinatura do cliente, com data, hora e local. |
| Câmera no rodapé preto: toque em "Baixar PDF" (verde): o botão vira "Gerando PDF..."; toque no hambúrguer ("Mais ações"): "Copiar Link" e "Imprimir" (sem tocar em "Imprimir"). [TESTAR: com o download desligado no robô, "Gerando PDF..." termina sem o aviso "Erro ao gerar PDF"] | No rodapé, o Baixar PDF gera o relatório em arquivo. No menu ao lado ficam o Copiar Link e o Imprimir. |
| [ILUSTRAÇÃO: a página do relatório virando um arquivo PDF, com o botão "Baixar PDF" e o arquivo "OS-16"; fundo branco, Montserrat, verde, objetos genéricos. Motivo: o download não aparece na gravação] | Com o PDF baixado, é só enviar ao cliente pelo meio que você preferir, como e-mail ou WhatsApp. |

### cap12 · O link do cliente (vinheta: VISÃO DO CLIENTE)

| Tela | Fala |
| --- | --- |
| Volta ao relatório; no menu do rodapé, toque em "Copiar Link": toast "Link copiado!". [O endereço copiado aponta para dominex.app: não mostrar barra de endereço nem colar] | Falta o cliente receber o resultado. No menu do rodapé, toco em Copiar Link, e o aplicativo avisa: Link copiado. É só enviar esse link ao cliente: ele acompanha a ordem e baixa o relatório sem precisar de login. |
| Corte para a visão do cliente (`?modo=cliente`, sem mostrar a barra de endereço): cabeçalho com a empresa, "OS #16" e o selo "Concluída"; o relatório com o rodapé "Baixar PDF". [BACKEND: RPCs `get_public_os` e `get_public_os_by_code` com o payload da OS concluída; sem elas o link não abre] [TESTAR: capítulo à parte com `"anonymous": true` partindo do estado do capítulo anterior, ou `goto` na mesma sessão] | Ele abre o link e vê a ordem como o cliente vê: o nome da empresa, o número da OS, o status Concluída e o mesmo relatório que o técnico tem, com o botão pra baixar o PDF. |
| Abre sozinha a gaveta "Como foi seu atendimento?": o rosto com a nota e o controle ("Arraste aqui", "Nada provável" e "Muito provável"), as estrelas de "Qualidade", "Pontualidade" e "Profissionalismo", "Seu nome (opcional)" e "Comentário (opcional)", com "Fechar" e "Enviar avaliação". | Como a ordem está concluída, abre sozinha a pesquisa Como foi seu atendimento? O cliente escolhe uma nota de zero a dez, arrastando o controle. Depois dá estrelas pra cada critério da sua empresa e, se quiser, deixa o nome e um comentário. |
| Leva o controle até 10; marca 5 estrelas em cada critério; digita o nome "Helena Barros" e o comentário "Atendimento pontual e muito organizado. Obrigada!"; toque em "Enviar avaliação": toast "Avaliação enviada" e a faixa "Avaliação enviada" ("Obrigado pelo seu feedback!"). [TESTAR: o controle é um slider; usar o teclado (tecla End) ou `drag`] [BACKEND: RPC `submit_public_os_rating` grava a nota e os três critérios em `service_ratings` e `service_rating_criteria`; sem ela a tela diz "Avaliação enviada" e nada é gravado] [Se abrir o convite "Que bom que você gostou!" (link do Google na semente), tocar em "Agora não"] | Preencho com nota dez, cinco estrelas em cada critério, o nome e um comentário, e toco em Enviar avaliação. A avaliação é enviada, e o cliente recebe o agradecimento. |
| A câmera fica na faixa "Avaliação enviada". | Essa avaliação chega pra você em NPS e Satisfação, na tela de Ordens de Serviço, que a gente viu no tutorial anterior. E enquanto o atendimento acontece, o mesmo link mostra o status em tempo real, com o técnico responsável e, quando ele está a caminho, a posição no mapa. |

### cap13 · Recapitulando (vinheta: RESUMO)

| Tela | Fala |
| --- | --- |
| Montagem rápida: a Agenda, a OS #16 aberta, "A Caminho", a rota e o check-in. | Pronto! Recapitulando: o técnico abriu a ordem pela agenda, tocou em A Caminho, acompanhou a rota e fez o check-in quando chegou. |
| Montagem rápida: o checklist com a foto e a assinatura, "Consumir do estoque", "Pausar OS" e "Finalizar Parcial". | Depois preencheu o checklist do equipamento, com respostas, medições, foto e a assinatura do cliente, anotou os materiais que usou e viu como pausar e como finalizar parcialmente quando a visita não termina no dia. |
| Montagem rápida: o "Resumo do consumo", o relatório com "Duração:", o "Baixar PDF" e a pesquisa "Como foi seu atendimento?". | Na finalização, conferiu o resumo do consumo, e o estoque baixou. A ordem virou um relatório, que dá pra baixar em PDF ou mandar por link, e o cliente avaliou o atendimento. |
| Cartão "Próximo: Área do Técnico: Refrigeração e Climatização"; cartela final. | No próximo tutorial, a gente conhece a Área do Técnico de Refrigeração e Climatização, a caixa de ferramentas de apoio que fica a um toque do atendimento. Até lá! |
