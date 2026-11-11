# T03 · Propostas de fala (robô e ensaio, 10/11/2026)

Do robô e do ensaio do T03 contra o app 1.59.154 (`$TUT_HOME/rec/t03/gerar.py`). Não editam `roteiro.md` nem `tts_textos.py`: a revisão
geral aplica. Linha = número da linha da tabela Tela × Fala do capítulo (a mesma do `tts_textos.py`).

## Fala

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 04 | 3 | "Busco cobre e escolho o de resíduos de cobre." | "Busco cobre e escolho o de sucata de cobre." | O catálogo real do app (`ncm_presets`, migração 20260118193311, a que vale na 1.59.154) descreve o 7404.00.00 como "Sucata de Cobre - Fios, cabos, tubos, chapas, componentes elétricos" (categoria "Cobre"); "Desperdícios e resíduos de cobre" é o texto da migração antiga, apagada pela nova. |
| 01 | 6 | "Uma dica: quem não tem permissão de ver valores, como o Marcos, que é balanceiro, continua vendo os pesos. No lugar do dinheiro, aparece um cadeado." | (a) manter e o mundo tirar do Marcos "Ver Totais e Valores Financeiros" (muda o T2, cap09, que hoje diz que ela fica ligada); ou (b) "Uma dica: quem não tem a permissão de ver valores continua vendo os pesos. No lugar do dinheiro, aparece um cadeado." com o corte feito por um usuário sem a permissão | Conflito com o mundo: o T2 deixa o Marcos com "Ver Totais e Valores Financeiros" ligada (`MUNDO_FICTICIO.md`, "Permissões do Marcos"; roteiro do T2, cap09) e com ela a tela Estoque mostra os valores, sem cadeado. O ensaio usa a semente `t03/marcos-sem-valores` só no corte (cap01b) para a tela bater com a fala de hoje; decidir na junção. |
| 10 | 2 | "Repara no aviso: o radiador ainda tem cento e dez quilos. ..." | "Nos três pontinhos do radiador, Excluir. Repara no aviso: o radiador ainda tem cento e dez quilos. ..." | A linha 1 é toda ilustração e a janela "Confirmar Exclusão" precisa estar na tela no "Repara no aviso". Sem a frase nova, o robô abre o menu e clica em "Excluir" nas últimas palavras da linha 1 ("continuam lá."), ainda sob a ilustração, e a edição tem de soltar a ilustração ~2 s antes do fim da linha. |
| 05 | 7 | "E por que agrupar ajuda? No filtro, deixo marcado só o cobre." | "E por que agrupar ajuda? No filtro, desmarco os outros grupos e fico só com o cobre." | Deixar só o Cobre custa 5 cliques (um por grupo; ver "Achados"), ~5 s de tela para 2 s de fala. Hoje o filtro abre no fim da linha 6 ("com a cor dele") para os cliques caberem antes dos cartões (linha 8); a frase nova descreve o que se vê e dá ~1 s. |
| 08 | 2 | "Em Movimentar estoque, escolho Saída, o radiador e dois quilos." | "Em Movimentar estoque, escolho Saída. Depois, o radiador e a quantidade: dois quilos." | Depois que a janela abre (~1 s) sobram 4,2 s de fala para 4 gestos de ~1 s (Saída, material, a opção, quantidade). O robô faz Saída e material em sequência e o "2" sai no "A janela", ~1 s depois do "dois". |
| 00 | 4 | "Se você ainda não viu o tutorial Usuários e permissões, dá uma olhada antes. Vamos conhecer a tela." | (sem mudança na fala; aviso na edição) "Dica: recolher o menu lateral dá mais espaço para a lista." | A 1280 px, com o menu lateral aberto, a "Lista de Materiais" perde "Preço de Venda" e "Ações" (rolagem horizontal). O robô recolhe o menu no fim do cap00 (no "antes.", sob o cartão "Antes") e os outros capítulos já começam com ele recolhido. |

## Achados do app (1.59.154)

- **"Principal", não "PRINCIPAL"**: a tabela padrão aparece como "Principal" na coluna "Tabelas de Preço", no "Exibindo preços da tabela:"
  e no "Editar Preços em Massa" (nome guardado em `price_tables.name`; o app trata "Principal" como o nome da padrão em
  `utils/priceTableGenerator.ts`, `materialsExport.ts`). O roteiro e o plano escrevem "PRINCIPAL".
- **"Tabela Depósitos +4%"**: o botão da tabela vinculada na coluna leva o selo no nome acessível ("Tabela Depósitos +4%").
- **PDF em aba nova** (cap09): o app abre o PDF noutra aba (`window.open` + `URL.createObjectURL`); o robô grava uma aba só e o
  Chromium sem janela não tem leitor de PDF. A gravação mostra o aviso ("Lista exportada como PDF!", `Tabela "Tabela Depósitos"
  exportada!`) e guarda os dois PDFs que o app gerou (o roteiro os põe na tabela de bastidor `t03_pdfs` do falso e `rec/t03/t03_pdfs.py` grava
  `$TUT_HOME/t03/pdf/*.pdf` + PNG da 1ª página, fora do git) para a edição montar a "aba nova" como ilustração. O PDF A4 da tabela
  tem ~15 MB.
- **Ajuda do "Identificação/Produto Fiscal"** é dica de passar o mouse (Tooltip), não clique: o robô para o cursor na interrogação.
- **Avisos que somem rápido**: "Preço especial aplicado para Bronze" vive 2 s e o `"Radiador de cobre" excluído` com "Desfazer" 5 s;
  com o mouse em cima o aviso fica (o robô para o cursor no aviso até a palavra).
- **Filtro "Todos os Materiais"** (Estoque): marcar "Todos os Materiais" só volta a marcar tudo; não existe "só este grupo". Com tudo
  marcado, clicar num grupo o desmarca ("todos menos esse"). Deixar só o Cobre = desmarcar os outros 5 grupos.
- **Campo de material** (Movimentar, Transferir, Nova Compra): o Enter não escolhe a opção (o `input` fica fora do `Command`); a
  escolha é sempre um clique na lista.
- **Avisos (sonner)**: no ensaio, o aviso não é achado por papel (`status`) nem por `[data-sonner-toast]`; o robô mira o texto.

## Notas para a junção

- **Siqueira × Tabela Depósitos**: o cap07 (linha 6) liga o Depósito Irmãos Siqueira à Tabela Depósitos na tela, e a T4 liga de novo
  em B (MUNDO_LINHA_DO_TEMPO §4). Não há contradição (a T3 é demonstração e a semente `t03/inicio` desliga o depósito), mas a ação
  aparece em duas aulas.
- **Caixa do cap07**: semente própria `t03/caixa-0830` (caixa #85 do Rafael, 08:30, R$ 1.500,00, sem lançamentos), como pede o §9; o
  `base/caixa-aberto` (08:05) não é usado.
