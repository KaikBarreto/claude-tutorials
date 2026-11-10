# Produção EcoFlix · registro de pedidos, decisões e andamento

## Pedido (Kaik, 08/11 23:36)
"baseado em tudo que aprendemos da domiflix e tutoriais da dominex agora quero planejar os tutoriais da ecosistema
(ecosistematecnologia.com.br) com a marca dela, no mesmíssimo padrão que fizemos pra domiflix, mas agora pra ecoflix /
com todo aprendizado que tivemos, de nomenclaturas e pronunciações corretas, estrutura / para que seja da forma mais
produtiva e rápida possível, economizando tokens etc. / daqui 10 minutos vou atualizar também uma pagina
https://ecosistematecnologia.com.br/trilha-ecoflix que tem a ordme também / mas se achar melhor você pode sugerir
alterações etc. / E vamos fazer com uma voz masculina os da ecoflix"
Anexo "EcoFlix-briefing-gravacao.md" = `docs/ecoflix/trilha-de-tutoriais.md` do repositório do EcoSistema.

## Decisões (08/11)
- Perfil `perfis/ecoflix`: herda a Domiflix inteira; mudam marca, voz, pronúncias, app e mundo.
- Mundo: Recicla Vale Metais (sugestão da fonte), em Taubaté, SP; `FAKE_NOW` 10/11/2026 08:30 (terça).
- T3 é a primeira aula (molde e prévia), como na Domiflix.

## Decisões pendentes (Kaik) · respondidas em 10/11 (ver "Kaik, 10/11")
1. **Voz**: qual das quatro amostras do fluxo "EcoFlix · teste de voz masculina" (base44, Cristian, Davi Leão,
   Amanndev), ou outra.
2. **Erro de propósito na tela**: a fonte pede "mostre o erro de propósito em todo ⚠️"; a Domiflix tinha "não encenar a
   falha" (30/10). Proposta: caminho certo primeiro e a consequência como informação (regra da Domiflix); mensagem de
   erro na tela só quando reconhecê-la é o que o cliente precisa ("Abra o caixa antes de realizar compras", "Popup
   bloqueado", o aviso do cofre), com a saída logo em seguida.
3. **Som da vinheta**: o som oficial da EcoFlix (`ecoflix-intro.mp3`, o que toca no app) ou um sintetizado no molde da
   Domiflix.
4. **T5**: trecho real de instalação do EcoTray (Windows/Mac, avisos do navegador e do SmartScreen) gravado pelo Kaik,
   ou só falado.
5. **Regime fiscal do exemplo** (proposto: Simples Nacional), antes do T16.

## Preparação (antes da primeira aula)
0. Consolidar na skill as melhorias da Domiflix que ficaram só nas cópias das aulas (aceleração no `finish.py`,
   `montar_cap.py`, `remendar_aula.py` e `celular_vertical.py` do vertical, folha de 3 s, pico do AAC, três ajustes do
   Supabase falso) e rodar o exemplo T3.
1. Marca: separar as 3 peças do símbolo (como o `brand_extract.py` fez com o capacete), vinheta no molde da do capacete,
   cartela; prévia da vinheta para o Kaik.
2. Voz escolhida + nó de teste de pronúncia (tabela do PERFIL); fechar o `config_narracao.json`.
3. App: versão publicada do EcoSistema (1.59.154 = `f37573ea0`, a da fonte; ou release mais nova) por `git archive`,
   `rec/setup-app.sh`, schema do `types.ts`, smoke nas rotas da Fase 1.
4. Mundo base inteiro de uma vez (empresa, pessoas, materiais, parceiros, 3 meses de histórico) e o EcoTray falso.
5. Roteiros do lote 1 (T3, T4, T6 a T10) num doc para aprovação; voz do T3; gravação do T3 com prévia de um capítulo.

## Economia (tokens e tempo)
- Produção numa sessão nova (contexto limpo e disco livre), com os repositórios claude-tutorials e EcoSistema anexados.
  A sessão da Domiflix está com o disco no limite (1,4 GB) e um contexto grande.
- Mundo base montado uma vez para a trilha toda, em vez de encadear sementes aula a aula (o que mais custou na
  Domiflix); cada aula só acrescenta o que ela cria na tela.
- Cada roteiro lê só a seção da sua aula na fonte (a fonte inteira tem ~60 mil tokens): `trecho_aula.py T7` (a fazer).
- Aprovação de roteiro por lote; um fluxo de voz por lote (o `proc.py` acha cada capítulo pelo conteúdo).
- Agentes com briefing curto e caminhos, no máximo 2 ao mesmo tempo; Sonnet no trabalho mecânico quando o limite dele
  voltar (11/11), Opus nos roteiros e em bug de causa desconhecida.
- Ensaio (`prever.py --ens`) antes de cada gravação final; câmera auditada antes do render; folha de 3 s antes de entregar.

## Kaik, 10/11 (00:21, 00:29 e 00:33)
"use a voz kaik barreto (até fiz nesse flow um run dela) / No exemplo o regime fiscal pode ser o lucro real, que é o
padrão de muita reciclagem / a vinheta faça como achar melhor, a sugestão sobre eeros é boa / bote 20 subagentes em
paralelo para já começar a gravar e estruturar tudo, toda a parte que precisa de ti / E planejar o roteiro , tudo /
quero terminar tudo isso bem mais rapido do que foi o da dominex, avance"
"consegue estruturar de uma forma que você continue fazendo tudo independentemente de acabar meu limite de 5h ou
semanal? ir voltando a fazer conforme voltar o limite / e estime já a produção de todos os audios como a dominex fez
mas já fazendo uma repassada de uma vez nisso tudo, talvez até esperar gravar tudo pra ver se não mudaria algo, assim
fica mais preciso e economiza creditos do eleven labs, que vou btoar depois que você levantar tudo / a gravação evite
erros, zooms bruscos, informações erradas etc. / Onde achar melhor, pode ilustrar visualmente, até mais do que foi
feito na dominex, sempre que falar de um conceito (não necessariamente algo na tela), ilustre bem pra ficar fácil de
entender pro publico / Sempre tentando falar de uma forma simples e facil de entender"
"se achar melhor,a o invés de supabase falso pode usar a conta teste@ecosistematecnologia.com.br"
Decisões:
- Voz **Kaik Barreto** (`KtH4mnH3mgKFGT4Ik9jZ`), uma versão por fala, fluxo único. Fiscal: **Lucro Real**. Vinheta a
  critério (som oficial da EcoFlix, se casar). Erro na tela: a proposta aprovada (PERFIL → "Fala").
- **Voz por último**: ensaio gravado de cada aula sem voz, depois uma revisão geral de todos os textos, então a
  estimativa de créditos para o Kaik comprar, e só aí a voz de tudo de uma vez.
- Mais ilustração de conceito do que na Domiflix; fala simples; zero zoom brusco e zero informação errada (briefing).
- **Supabase falso mantido** (a conta teste fica de plano B para alguma tela muito difícil de simular): data do mundo
  fixa, capítulo regravável do mesmo ponto, nenhuma nota, MTR ou cobrança de verdade, versão do app travada na
  gravada.
- Retomadas automáticas: `RETOMADAS.md`.

## Fila
1. **Agora (10/11 00:3x)**: 17 agentes de roteiro (26 aulas, `_BRIEF_ROTEIRO.md`) e 3 de estrutura: Ferramentas
   (melhorias da Domiflix na skill, branch `consolidacao-domiflix`), Mundo (EcoSistema 1.59.154 no Supabase falso, mundo
   da Recicla Vale Metais, EcoTray falso; branch `ecoflix-mundo`), Marca (vinheta, cartela, cartões e kit de ilustração;
   branch `ecoflix-marca`, prévia em `/home/claude/ecoflix/previa_marca/`).
2. Juntar: conferir os roteiros (tom, precisão, ilustrações), juntar os branches no main, consolidar no
   `MUNDO_FICTICIO.md` e nas sementes o que cada aula pediu, handlers do que faltar.
3. Robôs de todas as aulas e **ensaio gravado sem voz** (tempos estimados), corrigindo texto e tela.
4. **Revisão geral** dos textos numa passada só, aplicando o teste de pronúncia; **estimativa de créditos** (caracteres
   de todos os `CAPS` e `TITULOS`, ~1 crédito por caractere no eleven_v4) → avisar o Kaik e esperar os créditos.
5. Voz: fluxo único "EcoFlix · Vozes de todas as aulas", uma versão por fala → o Kaik exporta o zip.
6. Gravação final, edição e entrega, aula por aula, na ordem de produção da `TRILHA.md`.
7. ZIP final das legendas e capítulos; apagar os lembretes que sobrarem.

## Registro
- 08/11 23:5x Planejamento: perfil `perfis/ecoflix`, `TRILHA.md`, `MUNDO_FICTICIO.md` e este registro. Quatro amostras
  de voz geradas no ElevenLabs (mesmo texto, 2 versões cada, 362 créditos por versão, 2.896 no total).
- 10/11 00:2x Decisões do Kaik aplicadas no PERFIL, voz.json e MUNDO; `_BRIEF_ROTEIRO.md`, `trecho_aula.py` (só a seção
  da aula, 2 a 4 KB em vez de 60 mil tokens) e o código 1.59.154 em `/home/claude/ecoflix/app-src-1.59.154/` (61 MB).
- 10/11 00:3x 20 agentes lançados (opus). Teste de pronúncia na voz Kaik Barreto (16 itens numerados, 634 créditos) no
  fluxo "EcoFlix · teste de voz masculina". Os 20 lembretes de retomada criados (`RETOMADAS.md`; o limite de criação
  aceita uns 10 por minuto).
- 10/11 00:40 **Container reiniciou** e derrubou os 20 agentes (~10 min de leitura perdidos; nenhuma pasta de aula
  tinha sido salva). Kaik, 00:40: "nf-e e nfs-e tem que ser falado (ENE ÉFE Ê e ENE ÉFE ÉSSE Ê) SEFAZ está (séfas, mas é
  SEFÁS) / CFOP tá falando CÊFOP mas deveria ser CÊ ÉFE Ó PÊ, ICMS tá meio estranho, tem que falar I CÊ EME ÉSSE como
  sigla / kardex tá "cárdex" mas é "CARDÉX" / nas aulas do ecotray para integração com impressora e balança você vai
  pegar exatamente como o ecotray é num windows e simular uma tela de windows a pessoa usando, junto do sistema,
  baseado no dashboard.py (ou a tela que monta a UI do cato usando)". Pronúncias corrigidas no PERFIL e no
  `config_narracao.json` (agora com todas as trocas); reteste curto das seis no fluxo de teste (188 créditos). Cena de
  Windows no PERFIL e no briefing; código do EcoTray 1.59.154 em `/home/claude/ecoflix/app-src-1.59.154/ecotray/`
  (Tkinter; aqui não há tkinter, há Xvfb). 21 agentes relançados (os 20 + EcoTray: cena do Windows).
- 10/11 00:4x Relançados 20 agentes (o limite da sessão é 20 ao mesmo tempo): Ferramentas, Mundo, Marca, EcoTray (cena do
  Windows) e 16 de roteiro. **Falta lançar o de T20 + T26** (bateu no limite): lançar assim que um agente terminar.
