# Propostas de fala e pendências que vieram das ilustrações (para a revisão geral)

As do robô ficam em `Tnn/propostas_fala.md`; estas vieram dos agentes de ilustração (que não mexem em arquivo de aula).

| Aula | Onde | Proposta ou pendência | Motivo |
|---|---|---|---|
| T19 | cap02, linha 4 | Fala: "…O salário é só a ponta do iceberg." Se mudar, no `T19/cenas/ilustracoes.json` o `ate` vira "iceberg" e a cauda 0,6. | A cauda de 1,3 s da cena cobre o começo de "O botão Calcular". |
| T19 | roteiro | O roteiro diz 11 ilustrações; são 12. | Contagem. |
| T08 | cap08 | A cena usa 1.200 e 800 kg do roteiro, que não estão no mundo. | Conferir com a semente da T08. |
| T01 | caps 00, 05, 06, 08 | Símbolo fictício no lugar do logo da Recicla Vale: usar o mesmo logo que o robô da T01 sobe. | Não existe logo da Recicla Vale. |
| T04/T06 | — | O app escreve "Conta DINHEIRO"; a legenda terá "Conta Dinheiro". | Decidir a grafia da legenda. |
| Kit | `CAPS[1]` | O exemplo "Tara e peso líquido" chama o caminhão vazio de "Tara" (no app é a "2ª Pesagem"; tara é embalagem). | Corrigir na unificação do kit. |
| T18 | cap01 | O `tts_textos.py` não tem a 1ª fala do roteiro ("Aqui em Ambiental ficam as duas abas…"). Se ela entrar, todas as âncoras do cap01 somam 1 na linha. | Roteiro × tts: decidir qual vale. |
| T03 | caps 1, 6, 9 | Roteiro e plano escrevem "PRINCIPAL"; no app e na semente a tabela padrão é "Principal". | Grafia da legenda. |
| T09 | plano | O plano dá o caixa #87 ao Rafael; MUNDO e roteiro dizem #88 (o robô da T09 foi avisado: vale #88). | Acertar o plano. |
| T13 | cap10 | O segundo caso da conta ficou sem número (R$ 5.000/3.000/2.000 não são do mundo). | Conferir. |
| T14 | cap00 | A cena mostra R$ 44.933,47 e R$ 46.382,57, que dependem dos Pix da T13. | Conferir com a semente nova (robô da T14 avisado). |
| Kit | `pulse()` | Usa a propriedade CSS `scale`, que desloca elemento posicionado por `transform`; chamado duas vezes no mesmo elemento, anula o primeiro; um chip com a classe "g" herda o `.g` de grupo do kit. | Corrigir na unificação do kit. |
| T05 | cap04 | A hora do cupom de teste na cena (08:41:07, constante `QUANDO` no `CAPS[4]`) tem de bater com a cena de Windows 4. | Conferir quando gravar a T05. |
| T27/T01 | — | O logo fictício da Recicla Vale tem texto azul-escuro em fundo transparente: lê mal no menu escuro do app. Fazer uma versão clara para fundo escuro (e as cenas da T27 embutem o logo: se o da T01 mudar, embutir de novo). | Logo do mundo. |
| T05 | cap06, linha 10 | A troca "asas"→"Asaas" pegava dentro de "casas" (a legenda sairia "cAsaas decimais"): corrigido no `proc.py` e no `tempos_estimados.py` (só palavra inteira). | Resolvido. |
