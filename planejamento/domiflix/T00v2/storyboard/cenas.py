"""Fonte única das cenas do T0 v2: tempos (a partir de narracao/tts_textos.py) + composição 16:9 e 9:16 + desenho do
storyboard. Gera storyboard/cenas.json (lido por storyboard.html) e as tabelas de cenas e de duração do ../roteiro.md
(entre os marcadores <!-- CENAS --> e <!-- /CENAS -->, <!-- DURACAO --> e <!-- /DURACAO -->).

Tempo estimado: fala nova a 2,6 palavras/s; capítulos 4 e 5 com o tempo real do áudio do T0 atual (texto idêntico);
vinhetas, caudas, abertura e cartela com as durações do T0 atual (out/T0/capitulos.json).
uso: python3 -B cenas.py            (TUT_HOME = área de trabalho, padrão ~/domiflix; só para ler o áudio do T0 atual)
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "narracao"))
import tts_textos as T  # noqa: E402

TUT = os.environ.get("TUT_HOME", os.path.expanduser("~/domiflix"))
PPS = 2.6                   # palavras por segundo (estimativa pedida)
PPS_REAL = 2.89             # medido no T0 atual (512 palavras em 177,3 s de fala)
ABERTURA, CARTELA, CAUDA = 4.4, 3.4, 1.2
VINHETA = {1: 3.73, 2: 3.2, 3: 3.3, 4: 3.2, 5: 3.2, 6: 3.2}   # 1, 3, 4, 5 = T0 atual; 2 e 6 = título curto (mínimo 3,2)
REAL_T0 = {4: 3, 5: 4}      # capítulo v2 -> capNN.json do T0 atual (áudio reaproveitado)

LEGENDA = [("Domiflix", "DomiFlix"), ("dominex ponto ép barra guia técnico", "dominex.app/guia-tecnico"),
           ("vinte por cento", "20%"), ("trinta dias", "30 dias"), ("ép", "app")]


def legenda(txt):
    for a, b in LEGENDA:
        txt = txt.replace(a, b)
    return txt


# ---------------------------------------------------------------------------------------------- telas reais (ids)
TELAS = {
    "R01": "Onboarding: o T0 como 1º passo obrigatório",
    "R02": "Trilha Tutoriais do sistema: topo e barra de progresso",
    "R03": "Trilha: grupo Formação Básica",
    "R04": "Trilha: módulos do plano, selo verde",
    "R05": "Trilha: outros módulos, selo vermelho",
    "R06": "CTA de contratação de módulo não contratado",
    "R07": "Página da aula",
    "R08": "Lista de aulas com progresso e próxima aula",
    "R09": "Botão Tirar dúvidas com o suporte",
    "R10": "Contexto enviado ao suporte",
    "R11": "Lembrete dos primeiros 30 dias",
    "R12": "Confirmação dos combinados",
    "R13": "Menu da conta: Tutoriais | Domiflix",
    "R14": "Menu da conta: Falar com o Suporte",
    "R15": "Guia Técnico (página pública)",
    "R16": "Assinatura",
    "R17": "Assinatura: pagamento",
    "R18": "Gerenciar Meu Plano",
}

# ---------------------------------------------------------------------------------------------- capítulos
CAPS = {
    0: dict(titulo="Boas-vindas", vinheta=None, voz="nova",
            mudanca="Ficam as duas primeiras frases (boas-vindas e o ciclo do trabalho). Sai \"Neste vídeo rápido, eu te "
                    "mostro como a gente vai caminhar junto.\" Entram o 1º passo obrigatório do onboarding (texto do Kaik, "
                    "item 1) e a confirmação que vale do teste para a assinatura (item 2). Visual: o ciclo do trabalho "
                    "reestilizado (sem cartões) e duas ilustrações novas."),
    1: dict(titulo="Como funcionam os tutoriais", vinheta="Começando", voz="nova",
            mudanca="A fala vira a explicação nova do Kaik (item 3), letra por letra: trilha Tutoriais do sistema, "
                    "Formação Básica, módulos do plano na ordem recomendada, aulas dos módulos não contratados com "
                    "\"Não tem no seu plano\" e a contratação por ali, uma aula por tema com descrição, legendas e "
                    "materiais de apoio, progresso salvo e próxima aula. Saem \"cada aula mostra uma área inteira, "
                    "dividida em capítulos\", a ordem antiga (configurações, equipe, cadastros, OS...) e o \"combinado mais "
                    "importante\" (vira o 1º combinado do fecho). Fica a frase do menu da conta. Visual: telas reais da "
                    "DomiFlix nova no lugar do cartão de aula com capítulos e da trilha de 7 fases; os três grupos "
                    "(item 4) num mapa da trilha."),
    2: dict(titulo="O seu progresso", vinheta="Começando", voz="nova",
            mudanca="Capítulo novo: o percentual da trilha (item 5), os lembretes dos primeiros 30 dias (item 6) e as "
                    "outras trilhas no futuro (item 9)."),
    3: dict(titulo="Quando bater uma dúvida", vinheta="Ajuda", voz="nova",
            mudanca="Entram o reforço do Kaik (item 7, letra por letra) e o botão Tirar dúvidas com o suporte com o "
                    "contexto (item 8). O Guia Técnico fica, mais curto e sem \"na mesma ordem dos tutoriais\" (a trilha "
                    "mudou; ver sinalizações). O WhatsApp pelo menu da conta fica (com \"também\"). Saem \"Volta direto no "
                    "capítulo daquele assunto\" (a aula nova não tem capítulos) e a dica \"quando você já assistiu à "
                    "aula...\" (o reforço novo diz o mesmo)."),
    4: dict(titulo="A sua assinatura", vinheta="Assinatura", voz="T0",
            mudanca="Fala idêntica ao T0 atual (reaproveita o áudio). Código da assinatura igual da 1.38.6 para a "
                    "1.38.9. Visual: tela real da Assinatura (já existe) com os valores cobertos, no lugar do cartão "
                    "desenhado (decisão D2)."),
    5: dict(titulo="Quando a empresa cresce", vinheta="Assinatura", voz="T0",
            mudanca="Fala idêntica ao T0 atual (reaproveita o áudio). Visual: Gerenciar Meu Plano real (valores "
                    "cobertos); as ilustrações do teste e do proporcional ficam, reestilizadas (sem cartões e sem cinza)."),
    6: dict(titulo="Os combinados", vinheta="Recapitulando", voz="nova",
            mudanca="No lugar do fecho antigo (\"no próximo tutorial, a gente coloca a logo...\", que apontava para o T1): "
                    "recapitulação dos combinados, o convite para confirmar e a primeira aula da Formação Básica."),
}

# ---------------------------------------------------------------------------------------------- cenas
# cap/linha = linha do texto do TTS; de = índice da palavra (do TTS) em que a cena começa dentro da linha.
# d16/d9 = desenho no storyboard. real = tela real (id + o que precisa aparecer).
CENAS = [
    dict(k="abertura", tipo="VINHETA", titulo="Vinheta da aula",
         c16="Vinheta do perfil: o capacete se monta, DOMINEX e o título \"Boas-vindas à Dominex\". Proposta: o "
             "\"▶ DOMIFLIX\" verde vira o logo DomiFlix todo branco, capacete e texto (D1).",
         c9="Vinheta nativa na vertical: capacete (y 520 a 830), DOMINEX (y 880), logo DomiFlix branco (420 px, "
            "y 1060) e o título em 2 linhas de 88 px (y 1210 a 1400); tudo entre y 180 e 1740.",
         d={"t": "abertura"}),
    # cap00
    dict(cap=0, linha=0, tipo="ILUSTRAÇÃO", titulo="O ciclo do trabalho",
         c16="Painel claro. \"Boas-vindas à Dominex\" no alto (Dominex em verde). Embaixo, o arco verde se fecha em "
             "volta do capacete e as 4 estações entram entre \"chamado\" e \"dinheiro\": Chamado do cliente, Ordem de "
             "serviço, Técnico em campo, Dinheiro na conta. Só ícone e texto, sem cartão.",
         c9="Título em 2 linhas no topo (96 px). As 4 estações numa coluna (círculo de 140 px com o ícone, texto 58 px "
            "em até 2 linhas), ligadas pela linha verde que desce, volta pela direita e entra de novo no topo (o ciclo); "
            "acendem uma por vez. O capacete embaixo.",
         d={"t": "ciclo"}),
    dict(cap=0, linha=1, tipo="ILUSTRAÇÃO", titulo="O primeiro passo",
         c16="Selo \"Primeiro passo\". Três passos numa linha, número grande e texto, sem cartões: 1 Assistir até o "
             "final (a barrinha do vídeo enche em \"final\"), 2 Confirmar os combinados (acende em \"confirme\"), "
             "3 Continuar (acende em \"continuar\"). Se a DomiFlix nova tiver tela própria de onboarding, troca por "
             "ela (R01).",
         c9="Selo no alto e os 3 passos empilhados (círculo de 180 px, texto 62 px em até 2 linhas), um acende por "
            "vez; a barrinha do vídeo no passo 1.",
         d={"t": "passos", "selo": "Primeiro passo", "itens": [["play", "Assistir até o final"],
                                                              ["circle-check", "Confirmar os combinados"],
                                                              ["arrow-right", "Continuar"]], "barra": 1},
         confirmar=["C1"]),
    dict(cap=0, linha=2, tipo="ILUSTRAÇÃO", titulo="Do teste para a assinatura",
         c16="Linha do tempo: Período de teste → Assinatura ativa. O selo verde \"Combinados confirmados\" nasce no "
             "teste e segue pela assinatura (faixa contínua); no fim, \"Vídeo já assistido\" com check. Nada riscado.",
         c9="A mesma linha do tempo na vertical (teste em cima, assinatura embaixo), o selo descendo junto; texto "
            "44 a 64 px.",
         d={"t": "teste"}, confirmar=["C2"]),
    # cap01
    dict(k="vinheta", cap=1, tipo="VINHETA", titulo="Vinheta do capítulo",
         c16="Vinheta de capítulo do perfil (título com a voz do T0 atual).",
         c9="Vinheta vertical: barra verde à esquerda (x 72), área em 40 px espaçada e título em até 3 linhas de "
            "112 px, no meio da altura.", d={"t": "vinheta"}),
    dict(cap=1, linha=0, tipo="ILUSTRAÇÃO", titulo="O mapa da trilha",
         c16="\"Tutoriais do sistema\" grande à esquerda (rótulo TRILHA). Dela sai a linha da trilha com os 3 grupos "
             "em ordem (verde nos dois primeiros, vermelha no terceiro) e as aulas como pontos: Formação Básica · Módulos do seu plano (selo verde com check branco, "
             "\"Tem no seu plano\") · Outros módulos (selo vermelho com X branco, \"Não tem no seu plano\"). Trilha → "
             "módulos → aulas, sem temporadas.",
         c9="\"Tutoriais do sistema\" em 2 linhas no topo; a trilha desce na vertical com os 3 grupos empilhados "
            "(nomes 62 px, selos 42 px).",
         d={"t": "mapa"}, confirmar=["C3", "C4"]),
    dict(cap=1, linha=1, tipo="TELA REAL", titulo="Formação Básica",
         c16="Tela inteira da trilha no painel e zoom no grupo Formação Básica; destaque no nome do grupo em "
             "\"Formação Básica\".",
         c9="Recorte da trilha no celular (390 → 936 px, 2,4×) só com a Formação Básica.",
         real=dict(id="R03", itens=["grupo \"Formação Básica\" no topo da trilha", "aulas na ordem, 3 concluídas",
                                    "nenhuma \"Temporada\" ou \"Episódio\""], foco="zoom no grupo Formação Básica"),
         confirmar=["C3"]),
    dict(cap=1, linha=2, tipo="TELA REAL", titulo="Módulos do seu plano",
         c16="A câmera desce para os módulos do plano; destaque no selo verde \"Tem no seu plano\" em \"plano\" e na "
             "ordem (1º, 2º) em \"ordem\".",
         c9="Recorte do celular com os módulos do plano, um embaixo do outro; zoom no selo verde.",
         real=dict(id="R04", itens=["Gestão de Contratos e PMOC e Funcionários / RH",
                                    "selo verde saturado, check e texto brancos: \"Tem no seu plano\"",
                                    "ordem recomendada"], foco="zoom no selo verde"),
         confirmar=["C4", "C11"]),
    dict(cap=1, linha=3, de=0, tipo="TELA REAL", titulo="Outros módulos",
         c16="A câmera desce para os outros módulos (por último); destaque no play de uma aula em \"assistir\" e no "
             "selo vermelho em \"identificados\".",
         c9="Recorte do celular com um módulo não contratado: selo vermelho em zoom e as aulas com play.",
         real=dict(id="R05", itens=["CRM/Kanban, Emissão de Notas Fiscais, Cobranças online",
                                    "selo vermelho saturado, X e texto brancos: \"Não tem no seu plano\"",
                                    "aulas com play (liberadas)"], foco="zoom no selo vermelho"),
         confirmar=["C4"]),
    dict(cap=1, linha=3, de=21, tipo="TELA REAL", titulo="Contratar por ali mesmo",
         c16="Zoom no CTA de contratação do módulo; clique (anel verde) em \"solicitar\".",
         c9="Recorte do celular só com o CTA, grande; toque em \"solicitar\".",
         real=dict(id="R06", itens=["CTA de contratação no módulo ou na aula", "o que abre ao clicar"],
                   foco="zoom no CTA e clique"),
         confirmar=["C5"]),
    dict(cap=1, linha=4, tipo="TELA REAL", titulo="Uma aula, um tema",
         c16="Página da aula inteira; destaques em sequência: descrição (\"descrição\"), legendas (\"legendas\") e "
             "materiais de apoio (\"materiais\"). A lista lateral fica visível.",
         c9="A aula no celular, um recorte por vez: player com a legenda ligada → descrição → materiais de apoio.",
         real=dict(id="R07", itens=["player com legenda ligada", "título e descrição da aula", "materiais de apoio",
                                    "lista lateral de aulas"], foco="descrição → legendas → materiais"),
         confirmar=["C6"]),
    dict(cap=1, linha=5, tipo="TELA REAL", titulo="Progresso e próxima aula",
         c16="Zoom na lista lateral: as concluídas com check em \"salvo\" e a próxima aula em destaque em "
             "\"próxima\".",
         c9="A lista de aulas da interface mobile real (não a lateral reduzida): checks e a próxima em destaque.",
         real=dict(id="R08", itens=["aulas concluídas com check", "aula recomendada / próxima aula em destaque"],
                   foco="lista de aulas, a próxima aula"),
         confirmar=["C7"]),
    dict(cap=1, linha=6, tipo="TELA REAL", titulo="Onde encontrar",
         c16="Sistema com o menu da conta aberto (cartão da foto no rodapé da barra lateral); \"Tutoriais | Domiflix\" "
             "destacado e clicado em \"Tutoriais\".",
         c9="Celular: Menu → seção Conta, recorte dos atalhos; \"Tutoriais | Domiflix\" em destaque.",
         real=dict(id="R13", itens=["menu da conta: Perfil, Assinatura, Tema, Tutoriais | Domiflix, Central de Ajuda, "
                                    "Falar com o Suporte"], foco="Tutoriais | Domiflix"),
         confirmar=["C8"]),
    # cap02
    dict(k="vinheta", cap=2, tipo="VINHETA", titulo="Vinheta do capítulo",
         c16="Vinheta de capítulo do perfil (título com voz nova).", c9="Vinheta vertical, como a do capítulo 1.",
         d={"t": "vinheta"}),
    dict(cap=2, linha=0, tipo="TELA REAL", titulo="A barra de progresso",
         c16="Zoom na barra de progresso com o percentual; destaque com o rótulo \"Formação Básica + módulos do seu "
             "plano\" (padrão dos destaques).",
         c9="Recorte do celular só com a barra e o percentual, grandes; embaixo, o rótulo em 2 linhas (56 px).",
         real=dict(id="R02", itens=["nome da trilha", "barra de progresso com o percentual"],
                   foco="zoom na barra e no percentual"),
         confirmar=["C9", "C11"]),
    dict(cap=2, linha=1, tipo="ILUSTRAÇÃO", titulo="Explorar à vontade",
         c16="O mapa da trilha de novo: uma chave verde abraça Formação Básica e Módulos do seu plano (\"Contam no "
             "progresso\"); Outros módulos fica fora (\"Explorar à vontade\"). Uma aula do grupo vermelho ganha check "
             "e o percentual não se mexe.",
         c9="Grupos empilhados; uma chave verde à direita junta os dois primeiros (\"Contam no progresso\"); o "
            "terceiro embaixo com \"Explorar à vontade\"; o percentual no topo (120 px), parado.",
         d={"t": "mapa", "chave": 1}, confirmar=["C9"]),
    dict(cap=2, linha=2, tipo="ILUSTRAÇÃO", titulo="Lembretes de 30 dias",
         c16="Faixa de 30 dias com sininhos em alguns dias; a barra de progresso enche até 100% e a faixa termina em "
             "\"Concluído\". Se o lembrete for um aviso no sistema, entra a tela real dele no fim (R11).",
         c9="Calendário de 30 dias (6 × 5) com sininhos; embaixo, o progresso chegando a 100%.",
         d={"t": "lembrete"}, confirmar=["C10"]),
    dict(cap=2, linha=3, tipo="ILUSTRAÇÃO", titulo="Outras trilhas no futuro",
         c16="Tutoriais do sistema grande à esquerda (cheia, verde, \"Primeiro foco\"); à direita, Gestão e "
             "Contabilidade só em contorno tracejado (\"No futuro\"). Em \"primeiro foco\", as duas recuam.",
         c9="Empilhadas: Tutoriais do sistema grande no alto; Gestão e Contabilidade tracejadas embaixo.",
         d={"t": "trilhas"}, confirmar=["C12"]),
    # cap03
    dict(k="vinheta", cap=3, tipo="VINHETA", titulo="Vinheta do capítulo",
         c16="Vinheta de capítulo do perfil (título com a voz do T0 atual).", c9="Vinheta vertical.",
         d={"t": "vinheta"}),
    dict(cap=3, linha=0, tipo="ILUSTRAÇÃO", titulo="Primeiro os tutoriais",
         c16="A ordem certa, sem cartões: \"Comece agora\" com o play (em \"começar\"), 1 Siga os tutoriais (em "
             "\"Primeiro\"), 2 Restou uma dúvida específica? (em \"dúvida\"), 3 Suporte pela própria aula (em \"suporte\"), "
             "ligados pela linha verde. Nada de reunião riscada.",
         c9="Os passos empilhados, um por vez (círculo de 180 px, texto 62 px).",
         d={"t": "passos", "selo": "Comece agora", "itens": [["graduation-cap", "Siga os tutoriais"],
                                                            ["circle-help", "Restou uma dúvida específica?"],
                                                            ["headset", "Suporte pela própria aula"]]},
         confirmar=["C13"]),
    dict(cap=3, linha=1, de=0, tipo="TELA REAL", titulo="Tirar dúvidas com o suporte",
         c16="Página da aula; zoom no botão \"Tirar dúvidas com o suporte\"; clique em \"clicar\".",
         c9="Recorte do celular com o botão grande; toque.",
         real=dict(id="R09", itens=["botão \"Tirar dúvidas com o suporte\" na aula"], foco="zoom no botão e clique"),
         confirmar=["C14"]),
    dict(cap=3, linha=1, de=9, tipo="TELA REAL", titulo="O contexto vai junto",
         c16="A conversa ou o chamado aberto com o contexto; cada item destaca junto com a fala: empresa (Glacial "
             "Cold Brasil), usuário (Camila Duarte), módulo, aula. Se o canal for o WhatsApp: celular genérico, sem "
             "logo, com o texto real da mensagem copiado do código.",
         c9="Os 4 itens do contexto em linhas grandes (56 px), um destaque por vez.",
         real=dict(id="R10", itens=["Empresa: Glacial Cold Brasil", "Usuário: Camila Duarte",
                                    "Módulo: Gestão de Contratos e PMOC", "Aula: (nome real)"],
                   foco="um item por vez"),
         confirmar=["C14"]),
    dict(cap=3, linha=2, tipo="TELA REAL", titulo="Guia Técnico",
         c16="A página do Guia Técnico (já existe): \"Manual completo do produto\", \"Guia Técnico\", \"Buscar no "
             "guia…\"; o endereço dominex.app/guia-tecnico digitado na barra em \"endereço\".",
         c9="O Guia no celular (recorte do topo) e o endereço em texto grande (64 px) embaixo do recorte.",
         real=dict(id="R15", itens=["topo do guia e a busca", "endereço dominex.app/guia-tecnico"],
                   foco="título e endereço"),
         confirmar=["C15"]),
    dict(cap=3, linha=3, tipo="TELA REAL", titulo="WhatsApp pelo menu",
         c16="Menu da conta aberto; \"Falar com o Suporte\" destacado e clicado em \"Falar\".",
         c9="Celular: Menu → Conta; \"Falar com o Suporte\" em destaque.",
         real=dict(id="R14", itens=["menu da conta com \"Falar com o Suporte\""], foco="Falar com o Suporte")),
    # cap04
    dict(k="vinheta", cap=4, tipo="VINHETA", titulo="Vinheta do capítulo",
         c16="Vinheta de capítulo do perfil (título com a voz do T0 atual).", c9="Vinheta vertical.",
         d={"t": "vinheta"}),
    dict(cap=4, linha=0, tipo="TELA REAL", titulo="A tela Assinatura",
         c16="Menu da conta → \"Assinatura\" (em \"Assinatura\"); a tela com destaques na ordem da fala: status, "
             "plano, vencimento, valor (coberto), uso da conta, histórico de pagamentos. Valores em R$ cobertos por "
             "tarja lisa (D2).",
         c9="A Assinatura no celular, um recorte por vez: status, plano e vencimento → uso da conta → histórico.",
         real=dict(id="R16", itens=["status Ativa, Plano, Vencimento, Valor mensal (coberto)", "Uso da conta",
                                    "Histórico de pagamentos"], foco="um bloco por vez")),
    dict(cap=4, linha=1, tipo="TELA REAL", titulo="Pagar Agora",
         c16="Card Pagamento: clique em \"Pagar Agora\"; destaque em \"20% de desconto no plano anual · válido para "
             "Pix ou Boleto\"; as formas Pix, Boleto e Cartão; no \"cartão\", o aviso de renovação automática. "
             "Valores cobertos.",
         c9="Recortes em sequência: botão Pagar Agora → Pix, Boleto, Cartão empilhados → o selo do anual.",
         real=dict(id="R17", itens=["Pagar Agora", "20% de desconto no plano anual · válido para Pix ou Boleto",
                                    "Pix, Boleto, Cartão"], foco="botão → formas → desconto")),
    # cap05
    dict(k="vinheta", cap=5, tipo="VINHETA", titulo="Vinheta do capítulo",
         c16="Vinheta de capítulo do perfil (título com a voz do T0 atual).", c9="Vinheta vertical.",
         d={"t": "vinheta"}),
    dict(cap=5, linha=0, tipo="ILUSTRAÇÃO", titulo="Teste e plano",
         c16="Os módulos (nomes do catálogo) em grade de ícone e texto, todos acesos sob \"Período de teste\"; em "
             "\"ativar a assinatura\", ficam acesos só os do plano e os outros viram contorno com \"+\".",
         c9="Os módulos numa coluna (texto 46 px, quadrado de 104 px), com a mesma virada.",
         d={"t": "modulos"}, confirmar=["C11"]),
    dict(cap=5, linha=1, tipo="TELA REAL", titulo="Gerenciar Meu Plano",
         c16="\"Gerenciar Meu Plano\": abas \"Planos Prontos\" e \"Personalizado\" (clique em \"Personalizado\"), "
             "módulos, usuários adicionais e o painel \"Seu Plano\". Valores cobertos (D2).",
         c9="Recortes do celular: as abas → a lista de módulos → usuários adicionais.",
         real=dict(id="R18", itens=["abas Planos Prontos e Personalizado", "módulos e usuários adicionais",
                                    "painel Seu Plano (valores cobertos)"], foco="abas → módulos → usuários")),
    dict(cap=5, linha=2, tipo="ILUSTRAÇÃO", titulo="O proporcional",
         c16="O ciclo numa linha: Início do ciclo · Hoje · Vencimento; o trecho \"Já pago\" em contorno escuro e o "
             "que falta em verde, \"Cobrança proporcional hoje\".",
         c9="O ciclo na vertical (início em cima, vencimento embaixo), o trecho que falta em verde.",
         d={"t": "ciclo_pag", "v": 1}),
    dict(cap=5, linha=3, tipo="ILUSTRAÇÃO", titulo="Liberado e renovação",
         c16="\"Pagamento confirmado\" → \"Liberado\"; embaixo, \"Próxima renovação: valor do plano novo\".",
         c9="Empilhado: confirmado → liberado → próxima renovação.", d={"t": "ciclo_pag", "v": 2}),
    dict(cap=5, linha=4, tipo="ILUSTRAÇÃO", titulo="Reduzir o plano",
         c16="\"Reduzir o plano\": \"Ciclo atual: tudo liberado até o vencimento\" e \"Próximo ciclo: valor menor\", "
             "com o rótulo real \"Mudança de valor agendada\".",
         c9="Empilhado: ciclo atual em cima, próximo ciclo embaixo.", d={"t": "ciclo_pag", "v": 3}),
    # cap06
    dict(k="vinheta", cap=6, tipo="VINHETA", titulo="Vinheta do capítulo",
         c16="Vinheta de capítulo do perfil (título com voz nova).", c9="Vinheta vertical.", d={"t": "vinheta"}),
    dict(cap=6, linha=0, tipo="ILUSTRAÇÃO", titulo="Combinado 1",
         c16="Lista \"Os combinados\" em texto grande, sem cartões; o item 1 entra com check: \"Formação Básica e "
             "módulos do plano\", e embaixo, menor, \"na ordem indicada\".",
         c9="A lista item por item: título 60 px (até 2 linhas) e a linha de baixo em 46 px; check de 110 px.", d={"t": "combinados", "n": 1}, confirmar=["C17"]),
    dict(cap=6, linha=1, tipo="ILUSTRAÇÃO", titulo="Combinado 2",
         c16="Item 2: \"Dúvida depois da aula?\" e, embaixo, \"suporte pela própria aula\".", c9="Item 2 entra embaixo do 1.",
         d={"t": "combinados", "n": 2}, confirmar=["C17"]),
    dict(cap=6, linha=2, tipo="ILUSTRAÇÃO", titulo="Combinado 3",
         c16="Item 3: \"Plano e pagamentos\" e, embaixo, \"tela Assinatura\".", c9="Item 3 entra embaixo do 2.",
         d={"t": "combinados", "n": 3}, confirmar=["C17"]),
    dict(cap=6, linha=3, tipo="TELA REAL", titulo="Confirmar e seguir",
         c16="A tela real da confirmação; clique em \"confirmar\"; em \"primeira aula\", a aula recomendada da "
             "Formação Básica.",
         c9="Recorte do celular com a confirmação (botão grande) → a próxima aula.",
         real=dict(id="R12", itens=["confirmação dos combinados no fim do T0", "em seguida, a 1ª aula da Formação "
                                    "Básica"], foco="botão de confirmar"),
         confirmar=["C1", "C16", "C17"]),
    dict(k="cartela", tipo="VINHETA", titulo="Cartela",
         c16="Cartela do perfil: \"Até a próxima aula!\" (proposta D1: logo DomiFlix branco).",
         c9="Cartela vertical: capacete e DOMINEX no meio da altura, logo DomiFlix branco e a frase em 72 px.",
         d={"t": "cartela"}),
]


def tempo(s):
    m, r = divmod(s, 60)
    return f"{int(m)}:{r:04.1f}".replace(".", ",")


def calcula():
    linhas_cap = {c: T.CAPS[c].split("\n") for c in T.CAPS}
    t = 0.0
    tl = []     # (cap, inicio, fim, tempos de linha)
    caps_t = {}
    reais = {}
    for c, antigo in REAL_T0.items():
        reais[c] = json.load(open(os.path.join(TUT, "t0", "narracao", f"cap{antigo:02d}.json")))
    # abertura
    blocos = [("abertura", 0.0, ABERTURA)]
    t = ABERTURA
    for c in sorted(T.CAPS):
        if c in VINHETA:
            blocos.append((f"vinheta{c}", t, t + VINHETA[c]))
            t += VINHETA[c]
        if c in reais:
            fala = reais[c]["dur"]
            ini_l = [l["s"] for l in reais[c]["linhas"]]
            pal = None
        else:
            pal = [len(l.split()) for l in linhas_cap[c]]
            fala = sum(pal) / PPS
            ini_l = [sum(pal[:i]) / PPS for i in range(len(pal))]
        caps_t[c] = dict(ini=t, fala=fala, fim=t + fala + CAUDA, ini_l=ini_l, pal=pal)
        blocos.append((f"cap{c}", t, t + fala + CAUDA))
        t += fala + CAUDA
    blocos.append(("cartela", t, t + CARTELA))
    total = t + CARTELA
    return caps_t, blocos, total, linhas_cap, reais


def main():
    caps_t, blocos, total, linhas_cap, reais = calcula()
    b = {k: (a, z) for k, a, z in blocos}
    saida = []
    for i, s in enumerate(CENAS):
        s = dict(s)
        s["n"] = i + 1
        k = s.get("k")
        if k == "abertura":
            s["t0"], s["t1"] = b["abertura"]
            s["fala"] = "(sem fala) Boas-vindas à Dominex"
        elif k == "cartela":
            s["t0"], s["t1"] = b["cartela"]
            s["fala"] = "(sem fala) Até a próxima aula!"
        elif k == "vinheta":
            c = s["cap"]
            s["t0"], s["t1"] = b[f"vinheta{c}"]
            s["fala"] = T.TITULOS[c]
            s["kicker"] = T.KICKERS[c]
            s["d"] = dict(s["d"], kicker=T.KICKERS[c], titulo=T.TITULOS[c].rstrip("."))
        else:
            c, li, de = s["cap"], s["linha"], s.get("de", 0)
            ct = caps_t[c]
            pal = linhas_cap[c][li].split()
            # fim da cena = início da próxima cena do mesmo capítulo (ou fim do capítulo, com a cauda)
            prox = next((x for x in CENAS[i + 1:] if x.get("cap") == c and "linha" in x), None)
            ate = len(pal) if not prox or prox["linha"] != li else prox.get("de", 0)
            if ct["pal"] is None:   # áudio real do T0
                lin = reais[c]["linhas"][li]
                s["t0"] = ct["ini"] + lin["s"]
            else:
                s["t0"] = ct["ini"] + ct["ini_l"][li] + de / PPS
            if prox is None:
                s["t1"] = ct["fim"]
            elif ct["pal"] is None:
                s["t1"] = ct["ini"] + reais[c]["linhas"][prox["linha"]]["s"]
            else:
                s["t1"] = ct["ini"] + ct["ini_l"][prox["linha"]] + prox.get("de", 0) / PPS
            s["fala"] = legenda(" ".join(pal[de:ate]))
            s["linha_tts"] = f"{c}.{li}"
            s["voz"] = "T0" if ct["pal"] is None else "nova"
        if "real" in s:
            s["real"] = dict(s["real"], nome=TELAS[s["real"]["id"]])
            s["d"] = {"t": "real", **s["real"]}
        saida.append(s)
    json.dump({"total": total, "cenas": saida, "caps": {str(c): v["titulo"] for c, v in CAPS.items()}},
              open(os.path.join(AQUI, "cenas.json"), "w"), ensure_ascii=False, indent=1)

    # ------------------------------------------------------------------ roteiro.md: tabela de duração + cenas
    pal_tot = {c: len(T.CAPS[c].split()) for c in T.CAPS}
    dur = ["| Bloco | Palavras | Fala | Vinheta + cauda | Total | Começa em | Voz |", "|---|---|---|---|---|---|---|",
           f"| Vinheta da aula | | | {ABERTURA:.1f} s | {ABERTURA:.1f} s | 0:00,0 | identidade |".replace(".", ",")]
    for c in sorted(T.CAPS):
        ct = caps_t[c]
        vin = VINHETA.get(c, 0.0)
        fonte = "áudio do T0 atual (tempo real)" if ct["pal"] is None else "nova (2,6 palavras/s)"
        dur.append(f"| cap{c:02d} · {CAPS[c]['titulo']} | {pal_tot[c]} | {ct['fala']:.1f} s | {vin + CAUDA:.1f} s | "
                   f"{ct['fala'] + vin + CAUDA:.1f} s | {tempo(ct['ini'] - vin)} | {fonte} |".replace(".", ","))
    dur.append(f"| Cartela | | | {CARTELA:.1f} s | {CARTELA:.1f} s | {tempo(total - CARTELA)} | identidade |".replace(".", ","))
    novas = sum(pal_tot[c] for c in T.CAPS if caps_t[c]["pal"] is not None)
    real_fala = sum(caps_t[c]["fala"] for c in T.CAPS if caps_t[c]["pal"] is None)
    resto = total - sum(caps_t[c]["fala"] for c in T.CAPS)
    t_real = novas / PPS_REAL + real_fala + resto
    t_tudo26 = sum(pal_tot.values()) / PPS + resto
    dur.append(f"| **Total** | **{sum(pal_tot.values())}** | | | **{tempo(total)}** | | |")
    dur.append("")
    dur.append(f"Estimativa principal **{tempo(total)}** (fala nova a 2,6 palavras/s + áudio real dos capítulos 4 e 5). "
               f"Na velocidade que a Fernanda teve no T0 atual (2,89 palavras/s, pausas incluídas): **{tempo(t_real)}**. "
               f"Se tudo fosse lido a 2,6: {tempo(t_tudo26)}. Faixa pedida: 4:00 a 4:30.")
    cen = []
    cap_atual = "x"
    for s in saida:
        c = s.get("cap", "x" if s.get("k") == "abertura" else "y")
        if s.get("k") == "abertura":
            cen.append("### Abertura\n")
        elif s.get("k") == "cartela":
            cen.append("### Cartela\n")
        elif c != cap_atual:
            cap_atual = c
            info = CAPS[c]
            vin = f"vinheta: {info['vinheta'].upper()}" if info["vinheta"] else "sem vinheta"
            voz = "voz nova" if info["voz"] == "nova" else "fala e áudio do T0 atual, sem voz nova"
            cen.append(f"### cap{c:02d} · {info['titulo']} ({vin}; {voz})\n")
            cen.append(f"**Mudança em relação ao T0 atual:** {info['mudanca']}\n")
        tag = s["tipo"]
        if "real" in s:
            tag += f" {s['real']['id']}"
        voz = ""
        if s.get("voz") == "T0":
            voz = " · voz: T0"
        elif s.get("voz") == "nova":
            voz = " · voz: nova"
        elif s.get("k") == "vinheta":
            voz = " · título: " + ("T0" if s["cap"] in T.REAPROVEITA_TITULOS else "voz nova")
        cen.append(f"**Cena {s['n']:02d} · {tempo(s['t0'])} a {tempo(s['t1'])}** · {s['titulo']} · {tag}{voz}")
        if s.get("k") == "vinheta":
            cen.append(f"> {s['kicker'].upper()} · {s['fala']}")
        else:
            cen.append(f"> {s['fala']}")
        if s.get("confirmar"):
            cen.append(">\n> " + " ".join(f"[confirmar {x}]" for x in s["confirmar"]))
        cen.append("")
        cen.append(f"- **16:9:** {s['c16']}")
        cen.append(f"- **9:16:** {s['c9']}")
        if "real" in s:
            cen.append(f"- **Tela real {s['real']['id']}** ({s['real']['nome']}): " + "; ".join(s["real"]["itens"]) + ".")
        cen.append("")
    rot = os.path.join(AQUI, "..", "roteiro.md")
    if os.path.exists(rot):
        txt = open(rot, encoding="utf-8").read()
        txt = re.sub(r"<!-- CENAS -->.*<!-- /CENAS -->", lambda m: "<!-- CENAS -->\n" + "\n".join(cen) + "\n<!-- /CENAS -->",
                     txt, flags=re.S)
        txt = re.sub(r"<!-- DURACAO -->.*<!-- /DURACAO -->",
                     lambda m: "<!-- DURACAO -->\n" + "\n".join(dur) + "\n<!-- /DURACAO -->", txt, flags=re.S)
        open(rot, "w", encoding="utf-8").write(txt)
    print("\n".join(dur))
    print(f"\n{len(saida)} cenas; total {tempo(total)}")


if __name__ == "__main__":
    main()
