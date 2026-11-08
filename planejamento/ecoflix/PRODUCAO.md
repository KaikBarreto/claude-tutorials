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

## Decisões pendentes (Kaik)
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

## Registro
- 08/11 23:5x Planejamento: perfil `perfis/ecoflix`, `TRILHA.md`, `MUNDO_FICTICIO.md` e este registro. Quatro amostras
  de voz geradas no ElevenLabs (mesmo texto, 2 versões cada, 362 créditos por versão, 2.896 no total).
