# 02 · Inventário e roteiro

## 1. Inventário (antes de escrever qualquer fala)
Leia o código do app (somente leitura) e/ou percorra o app rodando (capturas pelo Playwright) nas telas do tutorial.
Anote, por tela: caminho no menu, rótulos exatos de botões/abas/campos, o que é obrigatório, máscaras, avisos (toasts)
e textos de vazio, regras (ex.: "o CNPJ consulta a Receita e preenche"), permissões e pegadinhas.
Saída: `inventario.md`. Exemplo: [`exemplos/dominex-t3/inventario.md`](../exemplos/dominex-t3/inventario.md).

As pegadinhas viram um **handoff de correções** para o time do app (exemplo:
[`handoff-correcoes-app.md`](../exemplos/dominex-t3/handoff-correcoes-app.md)). O roteiro nunca depende de bug.

## 2. Roteiro Tela × Fala
Um documento vivo compartilhado com o dono do produto, com um bloco por capítulo e uma tabela de duas colunas:
- **Tela**: o que o robô faz e onde a câmera foca (rótulos entre aspas, como na tela).
- **Fala**: o texto exato da narração.

Estrutura que funcionou (12 blocos no T3): 0 Abertura · 1 A tela principal · 2..N um assunto por capítulo ·
último: Recapitulando + próximo tutorial. Cada capítulo começa com uma transição falada ("bom, agora que o cliente tá
cadastrado..."). Abertura: o que vai ser feito + por quê + "se você ainda não fez X, veja o tutorial anterior".
Peça aprovação do roteiro antes de gerar a voz. Exemplo: [`roteiro.md`](../exemplos/dominex-t3/roteiro.md).

## 3. Regras da fala
- Uma pessoa mostrando o sistema para um colega: "vou clicar aqui em Novo cliente", "repara que ele já trouxe o
  endereço", "pronto, salvou". "A gente" e "você" na mesma conversa.
- Frases curtas, uma ideia por frase; no máximo um "olha"/"repara" a cada 3 ou 4 frases.
- Exemplo concreto antes da regra ("imagina que o Colégio Monte Verde te ligou...").
- Dica prática quando houver ("uma dica: ..."). Sem superlativo, sem "neste capítulo abordaremos".
- **Só possibilidades** ([01-padrao.md](01-padrao.md)). Trocas feitas no T3:

  | Antes | Depois |
  |---|---|
  | A ficha não abre sozinha: pra ver, é só clicar nele. | Pra ver os detalhes, é só clicar nele. |
  | Pra pessoa física o sistema não consulta nada, só guarda o número. | É só digitar o número. |
  | Repara que aqui não tem botão de salvar: cada mudança já grava sozinha. | Repara que cada mudança já grava sozinha. |
  | ...em tamanho real, senão a etiqueta sai menor. | ...em tamanho real. |

- Fala que depende de um comportamento que pode mudar (um interruptor que vinha desligado e foi corrigido para vir
  ligado): escreva de um jeito que vale nas duas versões ("com ela ligada, o cliente passa a receber...").

## 4. Pronúncia
Escreva no **texto do TTS** a grafia que a voz lê certo; a legenda usa a grafia normal. Registre cada troca em
`config_narracao.json` → `trocas` (ver [03-narracao.md](03-narracao.md)), para o alinhamento e as legendas.
Exemplo (voz Fernanda, ElevenLabs eleven_v4):

| Na tela / legenda | No texto do TTS |
|---|---|
| QR Code | quê-érre côde |
| Hi-Wall | rai-uól |
| BTUs | bê-tê-ús |
| Waze | Uêiz |
| 18.000 BTUs | dezoito mil bê-tê-ús |
| 127 V, 220 V e 380 V | cento e vinte e sete, duzentos e vinte e trezentos e oitenta volts |

Teste as palavras difíceis num trecho curto antes de gerar a aula toda. Siglas comuns (CNPJ, CPF, CEP) a voz costuma
ler certo com a escrita normal.
