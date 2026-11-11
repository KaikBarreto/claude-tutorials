# Propostas de fala e achados do app · T20 · Portal do Cliente e Fornecedor

Do ensaio do robô (EcoSistema 1.59.154, Supabase falso, FAKE_NOW 10/11/2026 15:00). Nada de `roteiro.md` nem de `tts_textos.py` foi
editado; a revisão geral aplica o que valer. Tempos da voz ainda são os estimados.

## Mudanças de fala

Nenhuma até aqui: os caps 0, 1 e 2 passaram no rápido sem alterar a fala (ensaio rápido; tempos ainda estimados). Caps 3 a 10 ainda não ensaiados (fila da trava): as propostas de tempo saem do `prever.py` quando rodarem.

## Achados do app

1. **Relatório ignora o "sem valor" do pedido** (inventário, seção 6.1): a edge `entity-portal-report` soma o `total_price` de todo pedido do
   período; só "Mostrar valores" esconde os R$ ali. O Histórico, o comprovante e a página de fotos respeitam o "Comprovante sem valores". A fala
   só afirma o que vale (cap05 L7 e L8, cap07 L5).
2. **Saldo do portal x saldo da ficha** (6.2): a edge desconta do saldo os movimentos de pedido sem valor dos últimos 90 dias; com um pedido
   assim lançado no saldo, os dois números diferem. Na aula não há esse caso.
3. **Aba "Preços" do fornecedor** (6.3) existe, nasce desligada e a fonte não cita: a aula não clica nela.
4. **Cabeçalho do portal** diz "Portal do Cliente" também para fornecedor (6.5): nome do produto, não do tipo de parceiro.
5. **Gravador filma UMA página**: não há passo para trocar de contexto nem de aba. Os "dois navegadores" (caps 4, 6, 8) e a "segunda aba" da
   Fundição (caps 5 e 7) são feitos com `goto` interno no mesmo contexto, rotulados "navegador do parceiro" / "navegador do sistema" para a
   edição tratar como corte. A janela nova do PDF (cap09) não é filmada: o PDF A4 sai em base64 no `actions.json` (passo "PDF do comprovante A4")
   para a ilustração, como no T8.
