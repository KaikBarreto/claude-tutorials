# Texto enviado ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T21 "Integração com WhatsApp".
# Gerado do roteiro.md (coluna Fala) pelo gerador do lote 5: cada linha do texto é uma linha da tabela Tela × Fala.
# Trocas de pronúncia em relação ao roteiro (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   QR Code -> "quê-érre côde" | QR -> "quê-érre" | RH -> "érre-agá" | API -> "á-pê-í"
CAPS = {
0: """Oi! Neste tutorial a gente vai conectar o WhatsApp da empresa na Dominex e ligar os avisos automáticos pro cliente.
O técnico saiu pra visita, o cliente recebe uma mensagem. O serviço terminou, ele recebe outra. E a cobrança também avisa sozinha, perto do vencimento.
Os avisos fazem parte do módulo de WhatsApp. Com ele contratado, tudo fica aqui, em Configurações, Integrações, WhatsApp.
Se você ainda não viu o tutorial Ferramentas de érre-agá, dá uma olhada antes. [pause] Vamos ver o que a integração faz.""",
1: """Lá em cima ficam as áreas da integração. Em Automações você liga os avisos, no Histórico acompanha cada envio, e a Conexão é por onde tudo começa.
As automações e o histórico abrem assim que o número conecta.
E a conexão é pelo quê-érre côde, com um número de WhatsApp da empresa. Leva menos de um minuto, e os avisos saem desse número, então o cliente já reconhece quem está falando.""",
2: """Tudo começa pela conexão. O passo a passo fica aqui na tela: no celular da empresa, você abre o WhatsApp, vai em Dispositivos conectados e aponta a câmera pro quê-érre côde.
Uma dica: se der, use um chip só pros avisos. Assim o WhatsApp principal do atendimento segue livre.
Antes de conectar, você marca o aceite: toda automação fora da á-pê-í oficial da Meta tem um risco pequeno de bloqueio do número. É por isso que vale ter o chip separado.
Com o aceite marcado, o botão Conectar meu WhatsApp libera.""",
3: """Com o aceite marcado, é hora de conectar. Clico em Conectar meu WhatsApp, e em poucos segundos o quê-érre côde aparece na tela. Enquanto espera, o selo mostra Aguardando leitura do quê-érre.
Aí, no celular da empresa, é só apontar a câmera pro código, na opção de conectar um aparelho.
Pronto, conectado. A tela mostra o número da empresa e que o canal está ativo, e já abre as Automações.""",
4: """Número conectado. Antes de ligar os avisos, os horários. A Proteção do número faz os avisos saírem no ritmo de uma pessoa, o que protege o número e respeita o cliente.
São duas janelas. Os avisos de serviço acompanham a operação: o técnico a caminho, o serviço iniciado e o concluído.
Na Glaciál, eles saem das sete da manhã às dez da noite, todos os dias.
Os lembretes de cobrança já vêm das oito da manhã às oito da noite, de segunda a sábado, e eu deixo assim.
Fora do horário, a mensagem espera na fila e sai assim que a janela abre.
Pra gravar, o botão fica logo abaixo, no cartão das automações: Salvar configurações.""",
5: """Agora os avisos. No cartão Automação de mensagens, eu ligo o Ativar automações.
Na aba Ordens de serviço ficam os quatro momentos: o lembrete da visita, o técnico a caminho, o serviço iniciado e a OS concluída. Os três últimos já vêm ligados.
Clicando num momento, você edita a mensagem dele. São três estilos de texto, e a rotação automática, a recomendada, vai alternando entre eles. Aqui eu fixo o Cordial.
Com o link de acompanhamento ligado, o cliente recebe junto o link da OS. E a prévia mostra um exemplo de como a mensagem chega: no Cordial, com o nome do técnico e o número da OS.
Ligo também o lembrete da visita agendada, um dia antes, como recomenda a tela. Ele sai na janela dos lembretes.
Salvar configurações, e os avisos da ordem de serviço estão prontos.""",
6: """E as cobranças também avisam sozinhas. Na aba Cobranças são quatro momentos: quando a cobrança é gerada, antes do vencimento, no dia e depois.
Antes do vencimento, você escolhe quantos dias antes, aqui três. E a mensagem leva o valor e o link de pagamento.
O aviso de atraso sai dois dias depois, e só pra quem ainda não pagou.
Os quatro já vêm ligados, do jeito que a Glaciál precisa, então eu deixo assim.""",
7: """E quem recebe esses avisos? Os clientes com a opção Receber mensagens pelo WhatsApp ligada.
Ela fica no cadastro de cada cliente, do lado do celular, e libera com o celular completo, com o DDD. No Hotel Mirante do Mar, ela está ligada.
E se o cliente responder pedindo pra parar, os avisos param pra ele. Quem decide é o cliente.""",
8: """No dia seguinte, depois de um atendimento no hotel, o Histórico conta o que saiu.
Em cima ficam os contadores de cada situação, como enviado, entregue e lido.
Embaixo, cada aviso. Os do hotel saíram certinho: o do técnico a caminho e o do serviço iniciado já foram lidos, e o de concluído foi entregue.
A academia preferiu não receber mensagens, então o aviso dela aparece como ignorado, com o motivo do lado. Assim você sabe o que aconteceu com cada um.""",
9: """E se precisar trocar de aparelho ou de número? É aqui, na Conexão.
O Desconectar pausa a fila de avisos. Depois, é só conectar de novo, lendo um quê-érre côde novo no aparelho que você quiser.
Conectar e desconectar fica com o administrador ou o gestor. E com o canal ativo, os avisos seguem saindo sozinhos, no ritmo que você definiu.""",
10: """Pronto! Recapitulando: a gente conectou o WhatsApp da empresa pelo quê-érre côde, com o aceite e a dica do chip separado.
Definiu os horários de envio, ligou os avisos da ordem de serviço, conheceu os das cobranças e escolheu o estilo da mensagem do técnico a caminho.
Viu que recebe quem está autorizado no cadastro e acompanhou cada envio no Histórico.
No próximo tutorial, a gente configura e emite as notas fiscais. Até lá!""",
}

# Títulos falados das vinhetas de capítulo (um nó no ElevenLabs, separados por [pause]); cap00 sem vinheta.
TITULOS = {1: "O que a integração faz.",
           2: "Preparando o número.",
           3: "Lendo o quê-érre côde.",
           4: "Horários de envio.",
           5: "Os avisos da OS.",
           6: "Os avisos de cobrança.",
           7: "A autorização do cliente.",
           8: "Acompanhando os envios.",
           9: "Reconectar e desconectar.",
           10: "Recapitulando."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "WhatsApp",
           2: "Conexão",
           3: "Conexão",
           4: "Proteção",
           5: "Automações",
           6: "Automações",
           7: "Automações",
           8: "Histórico",
           9: "Conexão",
           10: "Resumo"}

if __name__ == "__main__":
    tot = 0
    pal = 0
    for k, v in CAPS.items():
        w = len(v.replace("[pause]", "").split())
        tot += len(v)
        pal += w
        print(f"cap {k:2d}: {len(v):5d} chars, {w:4d} palavras, ~{w/2.6:5.1f} s")
    tit = sum(len(v) for v in TITULOS.values())
    print("total chars CAPS", tot, "| TITULOS", tit, "| soma", tot + tit, "| palavras", pal, f"| ~{pal/2.6/60:.1f} min de fala")
