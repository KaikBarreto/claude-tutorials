# Propostas de fala · T27 · White Label

Do ensaio do robô (11/11/2026, EcoSistema 1.59.154, voz ainda estimada, mundo base da junção). O que a fala precisa mudar para
bater com a tela ou caber no gesto. Nada aqui foi aplicado: `roteiro.md` e `tts_textos.py` ficam para a revisão geral. Linha =
número da linha do capítulo (1 = primeira linha da tabela Tela × Fala).

| Cap. | Linha | Texto atual | Texto novo | Motivo |
|---|---|---|---|---|
| 04 | 5 | Uma dica: com a Cor Primária vazia, o sistema fica no verde padrão. O Reset só limpa o campo. A volta pro verde vale depois do Salvar Personalizações. | Uma dica: com a Cor Primária vazia, o sistema volta às cores padrão. O Reset só limpa o campo. A volta vale depois do Salvar Personalizações. | Dentro do sistema logado o padrão não é verde: botões e interruptores são pretos (`index.css`, `[data-app]` com `--primary: 0 0% 10%`, o "restyle sóbrio"); só a barrinha do item ativo no menu escuro é verde (`--nav-neon`). Na tela do cap04, antes de salvar, o botão "Salvar Personalizações" e o interruptor estão pretos. |

## Achados do app

1. **Logo de letra escura no menu escuro.** O menu lateral é escuro por padrão (`hooks/useNavThemePreference.tsx:29`) e mostra o
   `logo_url` como veio, a 32 px de altura (`components/layout/SidebarMenuContent.tsx:333-340`), sem placa nem contorno: o logo
   fictício da T1 (letra azul-escura, fundo transparente) quase some. Não é defeito do app, mas é o que um cliente com logo escuro
   vai ver. Na T27 o logo é a versão clara (o mesmo desenho sobre placa branca: lê no menu e sai igual nos fundos brancos).
2. **Tabela de Pedidos a 1280 px com o menu aberto:** a coluna "Ações" passa da borda e o "⋮" fica cortado; a tabela rola na
   horizontal. O robô rola a tabela antes de apontar o "⋮".
3. **"Ver comprovante" no computador abre o PDF numa janela nova** (`pages/Orders.tsx:1146-1157`, `utils/openPdfInTab.ts`): o
   vídeo grava uma aba só. O robô guarda o PDF que o app gerou (`rec/t27/t27-cap05.comprovante.pdf`) e a edição o mostra como
   ilustração no cap05 L3 (o logo em cima, o fim sem o rodapé do EcoSistema).
4. **A cor aplicada demora a aparecer:** depois do "Salvar Personalizações", o aviso sai na hora, mas o azul só entra quando a
   consulta do White Label volta (`invalidateAllCompanyQueries`); medido no ensaio (ver relatório).
