# Texto a enviar ao ElevenLabs (eleven_v4, Fernanda) por capítulo do T0 v2 "Boas-vindas à Dominex" (onboarding novo).
# RASCUNHO PARA APROVAÇÃO DO KAIK (pedido de 31/10 17:13, T00v2/pedido_kaik_31-10.txt). NÃO GERAR A VOZ antes do ok.
# Cada linha do texto = uma linha da fala no roteiro.md (a cena muda junto com a linha; algumas linhas têm 2 cenas).
# Frases entre aspas no pedido do Kaik (itens 1, 3 e 7) entram LETRA POR LETRA (só "DomiFlix" na grafia de pronúncia).
#
# Trocas de pronúncia (a legenda segue a grafia do roteiro, ver config_narracao.json):
#   "Domiflix" -> "DomiFlix" (a voz já leu "Domiflix" bem no T0 atual; a legenda usa a grafia do Kaik)
#   "ép" -> "app"  |  "dominex ponto app barra guia técnico" -> "dominex.app/guia-tecnico"
#   "vinte por cento" -> "20%"  |  "trinta dias" -> "30 dias"
#
# Mapa v2 <- T0 atual (/t0/narracao/tts_textos.py):
#   0 <- 0 (muda) | 1 <- 1 (muda) | 2 NOVO | 3 <- 2 (muda) | 4 <- 3 (IDÊNTICO) | 5 <- 4 (IDÊNTICO) | 6 NOVO (no lugar do fecho 5)
# Os capítulos 4 e 5 são IDÊNTICOS, byte a byte, aos capítulos 3 e 4 do T0 atual: reaproveitam o áudio e os tempos
# (capNN.json) sem gerar voz. Os títulos 1, 3, 4 e 5 são os do T0 atual (titulos/cap01..04.wav).
# `python3 tts_textos.py` soma caracteres e palavras; `python3 tts_textos.py diff` mostra o que é voz nova.
# 31/10 (conferência na 1.38.11 + DomiFlix 487a0ca3): cap 3, linha 2, ajustada ao código: o botão "Tirar dúvidas com o
# suporte" abre o WhatsApp com a mensagem pronta (empresa, e-mail do usuário, trilha, módulo e aula); quem envia é a
# pessoa (src/components/domiflix/DomiflixLessonDetails.tsx:43-54,79-87). Antes: "ele já envia ...".
CAPS = {
0: """Oi! Boas-vindas à Dominex. A partir de agora, a sua empresa tem um lugar só pra organizar o trabalho, do chamado do cliente até o dinheiro na conta.
Este vídeo é o primeiro passo para começar a usar a Dominex. Assista até o final e confirme que entendeu os combinados para continuar.
Começou pelo período de teste? Se você confirmar ainda no teste, essa confirmação continua valendo quando contratar, e o vídeo não é exigido de novo.""",
1: """Na Domiflix, o seu primeiro caminho é a trilha Tutoriais do sistema.
Ela começa pela Formação Básica, com aquilo que todo cliente precisa aprender.
Depois vêm os módulos que fazem parte do seu plano, sempre na ordem recomendada.
Você também pode assistir às aulas dos módulos que ainda não contratou. Eles aparecem identificados como “Não tem no seu plano”, para você conhecer a função na prática e, se fizer sentido, solicitar a contratação por ali mesmo.
Cada aula ensina um tema em um único vídeo, com descrição, legendas e materiais de apoio.
Seu progresso fica salvo, e a Domiflix sempre indica qual é a próxima aula.
Pra encontrar, é só abrir o menu da sua conta e clicar em Tutoriais Domiflix.""",
2: """Na barra de progresso da trilha, só contam a Formação Básica e os módulos do seu plano.
As aulas dos outros módulos você explora à vontade, sem atrapalhar o seu progresso.
Nos primeiros trinta dias, a Dominex vai te lembrar de continuar, até você concluir a Formação Básica e os tutoriais dos módulos do seu plano.
No futuro, a Domiflix pode ganhar outras trilhas, como gestão e contabilidade. Mas o primeiro foco é sempre a trilha Tutoriais do sistema.""",
3: """Você não precisa esperar uma reunião para começar. Primeiro siga os tutoriais. Se depois da aula ainda restar uma dúvida específica, fale com o suporte diretamente pela própria aula.
É só clicar em Tirar dúvidas com o suporte: o WhatsApp abre com a sua empresa, o seu usuário, o módulo e a aula já na mensagem.
Se você preferir ler, o Guia Técnico explica cada função por escrito, tela por tela, no endereço dominex ponto ép barra guia técnico.
Fora da aula, o suporte também atende pelo WhatsApp, em Falar com o Suporte, no menu da sua conta.""",
4: """Tudo sobre o seu plano fica na tela Assinatura, também no menu da sua conta. Ali você vê o status, o plano, o vencimento e o valor, acompanha o uso da conta e o histórico de pagamentos.
Pra pagar, é só clicar em Pagar Agora: dá pra usar Pix, boleto ou cartão. No plano anual, o Pix e o boleto têm vinte por cento de desconto; no cartão, a cobrança é mensal e renova sozinha.""",
5: """No período de teste, todos os módulos ficam liberados pra você conhecer; ao ativar a assinatura, ficam os do plano que você escolheu.
E quando a sua empresa crescer, o plano cresce junto. Em Gerenciar Meu Plano, você escolhe um dos Planos Prontos ou monta o seu no Personalizado, com os módulos e os usuários que precisar.
E funciona assim: se você aumenta o plano no meio do caminho, paga hoje só a diferença, proporcional aos dias que faltam até o vencimento.
Os recursos novos entram assim que o pagamento é confirmado, e a renovação seguinte já vem com o valor do plano novo.
E se você reduzir, continua com tudo até o vencimento, e o valor menor começa no próximo ciclo.""",
6: """Então, recapitulando: primeiro a Formação Básica e os módulos do seu plano, na ordem indicada.
Restou uma dúvida depois da aula? Fale com o suporte pela própria aula.
E o seu plano você acompanha na tela Assinatura.
Agora é só confirmar que entendeu os combinados e seguir pra primeira aula. Te vejo lá!""",
}

# Títulos falados das vinhetas de capítulo (cap00 sem vinheta). 1, 3, 4 e 5 = áudio do T0 atual; 2 e 6 = voz nova
# (um nó "T00v2 títulos" com os dois, separados por [pause]).
TITULOS = {1: "Como funcionam os tutoriais.", 2: "O seu progresso.", 3: "Quando bater uma dúvida.", 4: "A sua assinatura.",
           5: "Quando a empresa cresce.", 6: "Os combinados."}
# Rótulo de área em cima do título (vinheta).
KICKERS = {1: "Começando", 2: "Começando", 3: "Ajuda", 4: "Assinatura", 5: "Assinatura", 6: "Recapitulando"}

# Capítulos e títulos que reaproveitam o áudio do T0 atual (não entram no nó de voz).
MAPA_T0 = {0: 0, 1: 1, 2: None, 3: 2, 4: 3, 5: 4, 6: None}
REAPROVEITA_CAPS = {4: 3, 5: 4}             # v2 <- T0 atual, texto idêntico
REAPROVEITA_TITULOS = {1: 1, 3: 2, 4: 3, 5: 4}  # v2 <- titulos/capNN.wav do T0 atual

if __name__ == "__main__":
    import os
    import re
    import sys

    def frases(texto):
        return [f for f in re.split(r"(?<=[.!?:])\s+", texto.replace("[pause]", " ").replace("\n", " ")) if f.strip()]

    def palavras(texto):
        return len(texto.replace("[pause]", " ").split())

    if len(sys.argv) > 1 and sys.argv[1] == "diff":
        import importlib.util
        tut = os.environ.get("TUT_HOME", os.path.expanduser("~/domiflix"))
        spec = importlib.util.spec_from_file_location("t0", os.path.join(tut, "t0", "narracao", "tts_textos.py"))
        t0 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(t0)
        for k in REAPROVEITA_CAPS:
            assert CAPS[k] == t0.CAPS[REAPROVEITA_CAPS[k]], f"cap {k} deixou de ser idêntico ao T0 cap {REAPROVEITA_CAPS[k]}"
        for k, v in REAPROVEITA_TITULOS.items():
            assert TITULOS[k] == t0.TITULOS[v], f"título {k} mudou"
        for k, v in CAPS.items():
            antigas = set(frases(t0.CAPS[MAPA_T0[k]])) if MAPA_T0[k] is not None else set()
            novas = [f for f in frases(v) if f not in antigas]
            print(f"cap {k} (T0 {MAPA_T0[k] if MAPA_T0[k] is not None else '--'}): {len(novas):2d} frases novas"
                  f"{' (reaproveita o áudio)' if k in REAPROVEITA_CAPS else ''}")
            for f in novas:
                print(f"      + {f}")
    else:
        tot = pal = gerar = pal_novo = 0
        for k, v in CAPS.items():
            c, w = len(v), palavras(v)
            tot += c
            pal += w
            if k not in REAPROVEITA_CAPS:
                gerar += c
                pal_novo += w
            print(f"cap {k}: {c:4d} caracteres, {w:3d} palavras, ~{w / 2.6:5.1f} s a 2,6 palavras/s"
                  f"{'  [reaproveita o áudio do T0]' if k in REAPROVEITA_CAPS else ''}")
        tit = sum(len(v) for v in TITULOS.values())
        tit_novos = sum(len(TITULOS[k]) for k in TITULOS if k not in REAPROVEITA_TITULOS)
        print(f"roteiro inteiro: {tot} caracteres de fala + {tit} de títulos = {tot + tit} | {pal} palavras")
        print(f"voz a gerar: {gerar} (capítulos 0, 1, 2, 3 e 6) + {tit_novos} (títulos 2 e 6) = {gerar + tit_novos}"
              f" caracteres | {pal_novo} palavras novas")
