# Andamento T12 no 1.60.18 (20/11)
Feito: fala (18 caps, 2.943 palavras, tts_textos.py), roteiro.md (regerado por script do scratchpad da sessão), tempos estimados, handlers
(delete_collection_order, get_collection_live_positions, ext cdnjs e arcgis), semente rastreamento, gerar.py (00 a 16), plano, inventário, ilustracoes.json.
Lote de ensaio: `TUT_SENHA=... nohup bash rec/t12/t12_lote.sh [NN...]` em /home/claude/ecoflix; log rec/t12/_ens/lote.log; resumos _ens/resumoNN.txt.
Falta: corrigir falhas do lote; sementes apos-cap05..15 saem do lote (cadeia 05,06,07,09,10,11,12,15). Derrubar: FAKE_PORT=54312 bash rec/run.sh down.
Gerar.py = cat _head.py _caps1.py _caps2.py (editar as partes e reconcatenar).

## Fechamento do ensaio (20/11, 2o lote)
Causas e correções (gerar.py = cat _head _caps1 _caps2; ORDENS_MENU novo no _head):
- cap06: `main input[type=number]` (a tela da ordem não tem <main>) -> `input[type=number]`; o arrasto do #8 caía num botão do cartão (dnd-kit não arrasta por botão): alvo agora o nome do parceiro no cartão; hover do "Sem cadastro" com within body.
- cap08: rola_ate sem <main> na tela do relatório (escopo body); texto da ficha é "Relatório do fornecedor" (minúsculo); grupo do menu fecha: GRUPO com `unless` antes de Configurações; "Voltar às ordens" sem noScroll (página rolada). Última correção (noScroll) NÃO reensaiada.
- cap09 (completo): link "Ordens de Coleta" ganha o ponto vermelho no nome (aria-label): ORDENS_MENU sem exact.
- cap10: menu de três pontinhos (hover) ficava aberto e cobria "Novo veículo": Escape.
- cap12: menu da linha sem aria-label (LINHA_MENU, só hover; clicar fecharia); aba da ficha é botão, não role=tab (corrigido, NÃO reensaiado).
- cap16: "Gerenciar perguntas" é item do menu da linha do modelo; o tipo de resposta só existe no formulário Nova pergunta (corrigido, NÃO reensaiado).
Lote 2: aprovados rápido+completo 06, 07, 09, 10, 11 (sementes apos-cap06/07/09/10/11 regravadas). Faltam: 08, 12, 16 (rápido) e 13, 14, 15 (rodaram em 1 s sem apos-cap12: inválidos) -> apos-cap12 e apos-cap15 ainda por gerar (apos-cap15.json atual é lixo).
Comando: TUT_SENHA=... nohup bash rec/t12/t12_lote.sh 08 12 13 14 15 16 (em /home/claude/ecoflix). Instância 54312 derrubada.

## Fechamento (20/11, lotes 3 e 4; limite de 2 lotes atingido)
Aprovados no rápido (0 falho, sem aviso): 00-07, 09-12, 14, 15; cap08 e cap12 também no completo (0 falho). Sementes apos-cap12 e apos-cap15 geradas.
- t12_dentro.sh: gravador que cai sem actions.json agora conta como falha (+99), no rápido e no completo.
- cap12: a lista de Clientes e Fornecedores só abre o painel resumido (sem aba Coletas); a ficha completa é a rota /cliente/<nome>-<código>. Agora o robô abre a ficha por pushState+popstate (sem recarregar) e clica "main button:text-is('Coletas')". Aprovado.
- cap08: "Voltar às ordens" recarrega o app (~5 s): atraso de 6 s no completo. Ajuste NÃO reensaiado: sobe ao topo em L3-7,0 e clica em L3-5,8.
- cap13: tela da ordem (a_caminho) mostrava "Sem sinal de GPS" (robô de mesa sem GPS): GPS_FALSO no setup responde ao watchPosition (Niterói). A tela da ordem não tem menu nem "Voltar às ordens": history.back() e reabre o grupo antes de "Rotas". NÃO reensaiado.
- cap16: apos-cap15 duplicava collection_settings (linha nova em vez de alteração) e a tela de Configurações ficava em esqueleto; semente consertada (_patch por company_id) e t12_semente.py corrigido. Interruptor do responsável sem aria-label: seletor por parágrafo (conferido por exploração). Passos 31 em diante NÃO reensaiados.
Falta: bash rec/t12/t12_lote.sh 08 13 16 (em /home/claude/ecoflix, TUT_SENHA no ambiente); depois cap14/15 já ok, e apos-cap15 regravado pelo cap15 se quiser. Instância 54312 derrubada.

## Fechamento (20/11, lote final de T20+T12)
- Arquivos compartilhados com a T20 conferidos: com `portal_password_enabled: false` nada fica trancado (`cfg.locked` só vale com `p.senha`; no app `isSectionLocked` exige `requires_login`). Nada a ajustar.
- cap08: completo 0 falhos (atrasos 3, máx. 1,3 s do "Voltar às ordens"). cap13: completo 0 falhos, mas 3 atrasos (máx. 3,7 s); o seletor da ordem 7 agora abre 1,2 s antes da escolha. cap16: rápido e completo 0 falhos, 17 atrasos (máx. 6,5 s): pacing apertado nos caps de checklist (digitação a 75 cps e hovers de 0,4 s já aplicados), ainda precisa afrouxar âncoras.
- cap09: no rápido o diálogo "Agendar coleta" abria sem data (digitação no campo de data incompleta): passo de conferência/ajuste do `#coleta-data` adicionado em `_caps2.py`. Reensaio caiu por falta de disco (ENOSPC, falhos 99). Falta: `bash rec/t12/t12_cap3.sh 09` (TUT_SENHA no ambiente, com disco livre).
Instância 54312 derrubada.

## 21/11 · fechamento (gravação final 1.60.22, montagem e prévia)
- Aula final: `$TUT_HOME/t12/edit/out/T12/aula_final.mp4` (19 min 24 s, 1080p, -16,3 LUFS, pico -3,8 dBTP, 419 legendas); prévia 720p em `$TUT_HOME/entrega_previa/`.
- Gravação: `rec/t12/t12_final.sh NN ...` (fila prio 12, instância 54312, `FAKE_NOW` 2026-11-10 07:00, quadros em `/dev/shm/t12_rec`); log `rec/t12/final.log`.
  Regravados (2 rodadas): cap08 (hover do "Voltar às ordens" no topo sem `noScroll`: maxLate 4,4 s), cap10 (Tipo do veículo ficava "Não classificar": a letra
  da busca se perdia; e o "⋯" de outra linha abria no caminho do cursor e escondia a aba Motoristas: 1 falho), cap11 (Cadastrar o tipo 0,9 s antes; depois
  "Caçamba 06ç": o "ç" da busca do seletor ia para a Identificação), cap12 (Registrar 1,9 s atrasado: De/Para já vêm marcados, Tipo pelo teclado; depois a
  semente com "Caçamba 06ç"). Sementes `apos-cap11/12/15` corrigidas para "Caçamba 06" (originais no scratchpad da sessão). Todos: 0 falho, maxLate < 0,8.
- Respiros (`pausas.py`, antes do fechamento): cap11, 12, 13 e 16. Acelera: cap16 [44,6; 46,8] 2x (navegação até a ordem). Sem destaques.
- Edição: `t12_specs.py` + `caps/extra.json` (21 zooms manuais, `min_w` 1600, só onde a fala aponta algo pequeno; cap10 CNH e cap12 formulário por causa do
  `auditar_camera.py`), `specs_ilus.py` (5 ilustrações v3: ilu01, ilu10, ilu11, ilu14, ilu15; nenhuma pendente), `fechar_t12.sh`, `montar_t12.sh` (`MIX_PY=t12_mix.py`).
  Disco: `out/capNN` e `out/T12` em `/dev/shm` (links) durante a montagem.
- Pendência: no cap17 (recapitulação, 19:12 a 19:18) o bloco Checklist das Configurações aparece vazio (semente `apos-cap15`, antes do cap16), enquanto a fala diz
  "montou o checklist com assinatura". Para corrigir: semente `apos-cap16` e regravar só o cap17.
- Achados do app para o MELHORIAS: na tela da ordem com checklist obrigatório sem resposta, o topo diz "0/1 obrigatórios" mas a barra "Falta para concluir" só
  lista a assinatura; o menu "⋯" das listas (Frota) abre por hover e fica aberto quando o cursor só passa por ele.
