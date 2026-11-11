# T02 · Propostas de fala (robô e ensaio, 10 e 11/11/2026)

Do robô e do ensaio do T02 contra o app 1.59.154 (`$TUT_HOME/rec/t02/gerar.py`). Não editam `roteiro.md` nem `tts_textos.py`: a
revisão geral aplica. Linha = número da linha da tabela Tela × Fala do capítulo (a mesma do `tts_textos.py`). Tempos da fala
estimados (`t02/narracao/capNN.json`, sem a voz), já com a fala da junção.

## Fala

Nenhuma mudança necessária até aqui: as 11 falas batem com a tela (rótulos, contagens, avisos) e todos os gestos cabem nas
palavras com a fala estimada (prévia `prever.py --ens` abaixo de 0,8 s em todos os capítulos). O ensaio completo (gravação com os
`at`) fica para depois do mundo base novo.

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| (nenhuma) | | | | |

## Achados do app (1.59.154)

- **Busca "nota" mostra o bloco do Cato** (cap04, linha 6): a descrição do "Usar o Cato (assistente de IA)" fala em "notas", então
  o bloco escuro "Quem pode conversar com o assistente" aparece logo abaixo do Fiscal & Ambiental. O roteiro pede a lista "sem chegar
  ao bloco do Cato": o robô abre as ações do Fiscal & Ambiental em seguida, o que empurra o bloco para fora da parte visível.
- **Perfil rápido não fica gravado na criação** (confirmado; achado 2 do inventário): criado com "Operador Padrão", o detalhe diz
  "Personalizado" e "32 permissões configuradas individualmente."; o Editar recalcula e marca "Operador Padrão".
- **Foto no Editar**: depois de "Foto atualizada com sucesso!" a foto da própria janela continua nas iniciais ("MA"); a lista, atrás
  da janela, já mostra a foto, e a janela só mostra ao reabrir (como o roteiro diz). A fala "No Editar, ela sobe na hora" vale pelo aviso.
- **A busca da lista de permissões refaz a lista**: ao limpar a busca, as telas que estavam abertas ("Clique para ver N ações") voltam
  fechadas.
- **Rodapé da janela "Sua equipe cresceu! 🎉"** a 1280x800: "Cancelar" e "Continuar" ficam em y 714 a 754, colados na borda de baixo
  da tela (o robô clica sem rolar).
- **Painel de detalhe do usuário a 1280x800**: o `min-h-[32rem]` da seção vence a altura que o `useAvailablePanelHeight` calcula; o
  painel começa em y 406 e mede 510 px (vai até 916 numa janela de 800), e o documento não rola. A lista "Telas (7)" começa em y 720;
  o robô rola o painel por dentro para mostrá-la (cap05). O fim da lista de ações de quem tem muitas permissões fica abaixo da borda.
- **Janela "Criar/Editar Usuário" a 1280x800**: duas rolagens (o corpo da janela e a lista de permissões de 368 px); com o corpo no
  alto só ~220 px da lista aparecem.
