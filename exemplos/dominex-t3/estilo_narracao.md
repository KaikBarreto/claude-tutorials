# Estilo da narração · Trilha Domiflix (vale para os 20 tutoriais)

Pedido do Kaik (29/10): "tente deixar as falas o mais natural possíveis, como num tutorial mesmo sem parecer engessado".
Voz do T3: **Fernanda - Natural Conversations** (ElevenLabs `KHmfNHtEjHhLK9eER20w`, eleven_v4, pt).

## Como soa
- Uma pessoa mostrando o sistema para um colega, ao vivo. Fala o que está fazendo enquanto faz:
  "vou clicar aqui em Novo cliente", "repara que ele já trouxe o endereço", "pronto, salvou".
- "A gente" e "você" na mesma conversa. Nada de "neste capítulo abordaremos", "a seguir veremos", "é possível realizar".
- Frases curtas, uma ideia por frase. Conectores de fala: então, agora, olha, repara, pronto, beleza, aqui em cima,
  do lado direito, lembra que. Com moderação: no máximo um "olha"/"repara" a cada 3 ou 4 frases.
- Exemplo concreto antes da regra: "imagina que a Padaria Bom Grão te ligou pedindo uma visita" e só depois
  "por isso o cadastro começa pelo nome".
- Dica prática quando houver: "uma dica:", "isso ajuda muito quando...". Sem superlativo, sem tom de anúncio.
- Pode ter pequenas pausas naturais com vírgula e reticências. `[pause]` só na troca de capítulo.
- Rótulos da interface ditos exatamente como aparecem na tela (o espectador procura pelo nome).
- **Só possibilidades** (Kaik, 30/10 15:06): nunca narrar o que o sistema NÃO faz nem dificuldades ("a ficha não abre
  sozinha", "o sistema não busca o CNPJ", "senão a etiqueta sai menor", "não tem aprovação no meio"). Diga o caminho
  positivo: "pra ver os detalhes, é só clicar", "é só digitar o número", "o cadastro entra direto". Vale também para
  avisos e cartões na tela.

## Estrutura de cada tutorial (padrão da trilha)
1. Abertura (~30 s): "Neste tutorial você vai..." dito de forma leve, com o porquê.
2. Pré-requisito (~15 s): qual tutorial ver antes, em uma frase.
3. Capítulos: cada um abre com uma transição falada ("bom, agora que o cliente tá cadastrado..."), nunca "capítulo 3".
4. Recap (~1 min): o que ficou pronto, em fala corrida.
5. Próximo (~15 s): o tutorial seguinte.

## Pronúncia (Fernanda, testado em 29/10)
- CNPJ, CPF e OS: escrita normal (ela soletra).
- CEP: escrita normal (lê "cép", como se fala).
- Números por extenso como se fala: "doze mil BTUs", "vinte e um, três mil".
- QR Code: escrever "quê-érre côde" (é como se fala no Brasil; o Kaik confirmou em 29/10). A legenda continua "QR Code".
- BTUs e hi-wall: conferir de ouvido na primeira geração.
- Conferido no T3 (30/10, pelo reconhecimento de fala; falta confirmar de ouvido): "rai-uól" sai Hi-Wall,
  "bê-tê-ús" sai BTUs, "Uêiz" sai Waze, "quê-érre côde" sai QR Code. Números por extenso ("cento e vinte e sete,
  duzentos e vinte e trezentos e oitenta volts", "dezoito mil") saem certos.
- Entrega dos áudios: o Kaik exporta o fluxo inteiro num zip ("New tts node (n).mp3", n = ordem dos nós, sem
  número = o primeiro). O `t3/narracao/proc.py` descobre o capítulo pelo conteúdo e alinha palavra a palavra.
- ElevenLabs: cada consulta de status devolve todas as URLs assinadas (muito texto). Consultar só as sessões que
  ainda estão na fila.
- Asaas = "asas"; DRE = "dê érri ê"; PMOC soletrado: escrever foneticamente quando aparecer.
