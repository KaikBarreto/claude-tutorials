# Propostas de fala · T10 · Estoque: saldo, histórico e posição

Do ensaio do robô (11/11/2026, app 1.59.154, mundo base da junção: estoque e Kardex da seção 4 da `MUNDO_LINHA_DO_TEMPO.md`).
Nada aqui foi aplicado: `roteiro.md` e `tts_textos.py` seguem como estão; a revisão geral decide. Robô: `$TUT_HOME/rec/t10/gerar.py`.

## Mudanças de fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 01 | L1 | "...aparecem as três primeiras: Estoque, Histórico e Relatório." | (opcional) "...aparecem as três primeiras: Estoque, Histórico, que é o Kardex, e Relatório." | No menu o item é "Histórico (Kardex)". A fala atual vale (o cap04 L1 já diz "É o Kardex do estoque"); a troca só deixa o rótulo inteiro. |

## Achados do app (rótulo ou comportamento diferente do roteiro)

- **Menu**: o item do grupo Materiais é **"Histórico (Kardex)"** (`i18n/.../navigation.json` `stockHistory`); o roteiro e o inventário dizem
  "Histórico".
- **Números sem casas fixas**: a lista do Estoque mostra "6.420 Kg", "42 Kg", "2.500 Kg" (não "6.420,000"); o Kardex, "2.180 Kg", "+320 Kg",
  "-14 Kg"; o aviso da transferência é "Transferido 320 Kg de Ferro misto para Ferro pesado" (o inventário diz "320,000 Kg"). A fala não muda
  (diz os números por extenso); só as marcas [ZOOM] do roteiro citam o formato com ",000".
- **"Preço médio pago"**: a explicação ("Custo médio ponderado do estoque atual (Custo Médio Ponderado Móvel) ... Estimativa.", com
  travessão no meio) abre ao passar o mouse no **valor** da linha, não no cabeçalho. O robô deixa o cursor no R$ 42,50 do cobre mel durante
  a L5 (a explicação fica na tela enquanto a fala a resume) e a câmera vai ao selo "estimativa" do cabeçalho.
- **Kardex**: "Filtros" abre uma folha; cada filtro vale na hora e "Aplicar filtros" só fecha a folha.
- **PDF** (cap11): abre noutra aba, e o vídeo grava uma aba só. O robô guarda o PDF que o app gerou (`actions.json`, passo "PDF da
  posição de 31/10") para a edição mostrar a aba como ilustração; o "~3 s na aba" do roteiro não sai da gravação.
