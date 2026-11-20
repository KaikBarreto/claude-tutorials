# Andamento T12 no 1.60.18 (20/11)
Feito: fala (18 caps, 2.943 palavras, tts_textos.py), roteiro.md (regerado por script do scratchpad da sessão), tempos estimados, handlers
(delete_collection_order, get_collection_live_positions, ext cdnjs e arcgis), semente rastreamento, gerar.py (00 a 16), plano, inventário, ilustracoes.json.
Lote de ensaio: `TUT_SENHA=... nohup bash rec/t12/t12_lote.sh [NN...]` em /home/claude/ecoflix; log rec/t12/_ens/lote.log; resumos _ens/resumoNN.txt.
Falta: corrigir falhas do lote; sementes apos-cap05..15 saem do lote (cadeia 05,06,07,09,10,11,12,15). Derrubar: FAKE_PORT=54312 bash rec/run.sh down.
Gerar.py = cat _head.py _caps1.py _caps2.py (editar as partes e reconcatenar).
