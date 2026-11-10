#!/usr/bin/env python3
"""T7 · especificação de edição por capítulo -> t7/edit/caps/specs.json.

Cada capítulo: título/kicker da vinheta, zooms que apontam para os RÓTULOS (`label`) dos passos do robô (rec/t7/gerar.py),
avisos ancorados numa palavra da fala ("Dica: ...", do plano T07) e ilustrações. Formato e regras: docs/05-edicao.md.
Celular: `min_w` em pixels do vídeo do celular (780x1688); zoom = 3348 / (min_w * 1,24), entre 1,15x e 3,5x
(min_w 1100 ~ 2,4x; 1250 ~ 2,2x; 1400 ~ 1,9x; 900 ~ 3x). Os cliques e as digitações já puxam a câmera sozinhos (auto, depth 2,3).
Uso: python3 -I rec/t7/specs.py   (reescreve t7/edit/caps/specs.json com todos os capítulos definidos aqui)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 't7', 'edit', 'caps', 'specs.json'))
OUTDIR = os.path.normpath(os.path.join(HERE, '..', '..', 't7', 'edit', 'out'))
TEC = 'Técnico em campo'


def z(de, ate=None, fim='+0.4', min_w=1250, **kw):
    d = {'de': de, 'fim': fim, 'min_w': min_w, **kw}
    if ate:
        d['ate'] = ate
    return d


SPECS = {
    '00': {'titulo': 'Abertura', 'kicker': 'Introdução', 'sem_titulo': True,
           'zooms': [z('o cartão da OS #16 na Agenda', 'o cartão da OS #16 (o relatório)', '+0.6', 1100),
                     z('a data da agenda do técnico', None, '+0.8', 1250)],
           'callouts': [{'palavra': [2, 'tutorial'], 'dur': 6.5, 'texto': 'Antes: Ordens de Serviço, Agenda, Equipes e Mapa ao Vivo', 'pos': 'bottom'}]},
    '01': {'titulo': 'Abrindo a OS no celular', 'kicker': TEC,
           'zooms': [z('a OS número 16 na Agenda', 'abre o resumo da OS', '+0.3', 1100),
                     z('resumo: o cliente', 'resumo: a descrição do serviço', '+0.5', 1250),
                     z('o botão Preencher OS', 'Preencher OS', '+0.3', 1100),
                     z('cabeçalho: a empresa', 'cabeçalho: o selo Pendente', '+0.5', 1250),
                     z('cartão Ir para o Atendimento', 'os botões do atendimento', '+0.4', 1250),
                     z('dados do cliente', 'a descrição do serviço', '+0.5', 1250),
                     z('o botão redondo da Área do Técnico', 'a Área do Técnico durante o atendimento', '+0.6', 1250)]},
    '02': {'titulo': 'A Caminho e a rota', 'kicker': TEC,
           'zooms': [z('cabeçalho: o selo A Caminho', 'o cartão Iniciar Atendimento', '+0.4', 1250),
                     z('a posição do técnico', None, '+0.4', 1250),
                     z('o cartão Rota até o cliente', 'o rótulo com minutos e quilômetros', '+0.6', 1250),
                     z('o botão Waze', 'o botão Google Maps', '+0.6', 1100),
                     z('o check-in direto, sem A Caminho', None, '+0.8', 1100)]},
    '03': {'titulo': 'Check-in', 'kicker': TEC,
           'zooms': [z('cabeçalho: o selo Em Andamento', None, '+0.6', 1250),
                     z('o carimbo do check-in', 'o endereço do check-in', '+0.5', 1250),
                     z('a área Checklists', 'um checklist para cada equipamento', '+0.4', 1250),
                     z('o rodapé: Finalizar OS', 'o rodapé: o menu de mais ações', '+0.8', 1250)]},
    '04': {'titulo': 'O checklist do equipamento', 'kicker': TEC,
           'zooms': [z('o checklist do equipamento', 'o contador: 0 de 13', '+0.5', 1250),
                     z('pergunta 1: filtros', 'o asterisco vermelho das obrigatórias', '+0.4', 1400),
                     z('toca fora do campo: a medição grava', None, '+0.4', 1250),
                     z('o contador: 10 de 13', None, '+0.8', 1250)]},
    '05': {'titulo': 'Fotos e vídeo', 'kicker': TEC,
           'zooms': [z('o botão Tirar Foto', 'o botão Galeria', '+0.5', 1250),
                     z('a miniatura na pergunta', 'a lixeira', '+0.6', 1250),
                     z('a pergunta Recomendações ao cliente', 'toca fora do campo: a resposta fica salva', '+0.6', 1250)]},
    '06': {'titulo': 'Consumir do estoque', 'kicker': TEC,
           'zooms': [z('a janela explica: só baixa na finalização', None, '+0.5', 1250),
                     z('cada material mostra o que tem disponível', None, '+0.5', 1250),
                     z('a lista Já registrado nesta OS', 'remover o material', '+0.6', 1250),
                     z('a opção liberada no menu', None, '+0.8', 1250)]},
    '07': {'titulo': 'Pausar e retomar', 'kicker': TEC,
           'zooms': [z('cabeçalho: o selo Pausada', 'o aviso: retome para continuar o preenchimento', '+0.5', 1250),
                     z('o rodapé só tem Retomar OS', None, '+0.5', 1250),
                     z('tudo o que foi preenchido continua salvo', None, '+0.5', 1250)]},
    '08': {'titulo': 'Finalizar parcialmente', 'kicker': TEC,
           'zooms': [z('o rodapé: Finalizar Parcial', None, '+0.4', 1250),
                     z('a confirmação: Parcialmente Concluída', 'o que já foi preenchido fica salvo', '+0.5', 1250),
                     z('o tempo que faz que a OS parou', None, '+0.5', 1250),
                     z('cabeçalho: o selo Parcialmente Concluída', None, '+0.6', 1250)]},
    # 1.38.24 (05/11): defeito P23 do app, a resposta da assinatura vira o texto cru "data:image/png;base64..." (y 1253-1278 do
    # vídeo, de ~28,97 s até o lápis em 34,66 s). Pela câmera: o zoom da assinatura vai até o toque em Confirmar; às 28,60 s a
    # câmera desliza para o cabeçalho do equipamento (selo "Concluído", y 418-462; a vista vai até y ~876) e fica lá até o lápis;
    # então desce para a assinatura em modo de edição. `guard` 1,0 só neste capítulo: com o cursor parado em Confirmar a guarda
    # puxaria a câmera para baixo e mostraria a linha por ~1 s.
    '09': {'titulo': 'A assinatura do cliente', 'kicker': TEC, 'camera': {'guard': 1.0},
           'zooms': [z('a pergunta Assinatura do cliente', 'o asterisco: obrigatória', '+0.5', 1250),
                     z('o cliente assina com o dedo', 'Confirmar a assinatura', 28.6, 1250),
                     z('o checklist do equipamento: Concluído', None, 34.62, 1250, atraso=-2.12),
                     z('lápis: rever a assinatura', None, 36.45, 1250, atraso=0.64)]},
    '10': {'titulo': 'Finalizar a OS', 'kicker': TEC,
           'zooms': [z('o que vai sair do estoque', 'quanto fica de cada material', '+0.5', 1250),
                     z('a fita isolante foi de 2 rolos', 'o saldo que fica já se atualiza', '+0.6', 1250)]},
    '11': {'titulo': 'O relatório e o PDF', 'kicker': 'Relatório',
           'zooms': [z('o número da OS', 'o equipamento atendido', '+0.5', 1250),
                     z('o check-in', 'a duração do atendimento', '+0.6', 1250),
                     z('a assinatura do cliente, com data, hora e local', None, '+0.6', 1250),   # 05/11: a L3 agora rola até a assinatura
                     z('o rodapé: Baixar PDF', None, '+0.6', 1100)],
           # o download do PDF não aparece na gravação: a ilustração (t7/edit/ilustra_pdf.py) mostra o arquivo seguindo ao cliente,
           # ao lado do celular parado (repouso = câmera sem zoom, o celular fica inteiro no centro)
           'ilustracoes': [{'at': 38.2, 'dur': 6.3, 'src': os.path.join(OUTDIR, 'ilu_pdf'), 'box': [1210, 150, 680, 780], 'scale_in': 0.0, 'loop': False}],
           'repouso': [[37.7, 44.7]]},
    '12': {'titulo': 'O link do cliente', 'kicker': 'Visão do cliente',
           'zooms': [z('cabeçalho: o nome da empresa', 'cabeçalho: o status Concluída', '+0.5', 1250),
                     z('o botão Baixar PDF', None, '+0.6', 1100),
                     z('a escala de 0 a 10', 'as estrelas de cada critério', '+0.5', 1250),
                     z('arrasta a nota até 10', '5 estrelas em Profissionalismo', '+0.4', 1250)]},
    '13': {'titulo': 'Recapitulando', 'kicker': 'Resumo',
           'zooms': [z('o botão redondo da Área do Técnico', None, '+8.0', 1250)],   # `apontar` não tem duração: a câmera segura o botão até o fim da fala
           # montagem rápida (t7/edit/montagem_cap13.py): trechos acelerados dos capítulos 1 a 12 e, na L4 nova (1.38.21), da gaveta
           # Editar OS do cap14, SOBRE a tela do celular em repouso; `repouso` mantém a câmera parada durante a montagem, depois ela
           # volta a seguir o botão da Área do Técnico (a L5, "No próximo tutorial", começa em 44,34 s)
           'ilustracoes': [{'at': 2.1, 'dur': 42.2, 'src': os.path.join(OUTDIR, 'montagem_cap13.mp4'), 'box': [736, 56, 448, 968],
                            'radius': 46, 'shadow': False, 'scale_in': 0.0, 'loop': False, 'fps': 30}],
           'repouso': [[0.2, 45.4]],
           'callouts': [{'palavra': [4, 'tutorial,'], 'dur': 9.0, 'texto': 'Próximo: Área do Técnico: Refrigeração e Climatização', 'pos': 'bottom'}]},
    # capítulo novo (1.38.21; gravado na 1.38.24), exibido entre o cap12 e o cap13 (T7.aula.json)
    '14': {'titulo': 'Editar a OS em campo', 'kicker': TEC,
           'zooms': [z('a área Checklists', 'o checklist solto, sem equipamento', '+1.5', 1250),
                     z('a gaveta Editar OS: Estrutura da OS', 'o texto: as respostas acompanham o checklist', '+0.6', 1250),
                     z('o bloco Checklists sem equipamento', 'a ordem ainda não tem equipamento', '+0.6', 1250),
                     z('Selecionar checklists', 'Remover equipamento', '+0.6', 1250, atraso=-2.6),   # o cartão novo já na gaveta
                     # o arrasto: a alça e o cartão de destino no mesmo quadro ("Solte aqui para vincular" de ~73,5 a 77,2 s)
                     z('a alça do checklist', 'arrasta o checklist até o Hi-Wall', '+2.5', 1250, destino=True),
                     z('Ações do checklist', 'o menu: Mover para', '+0.6', 1250),
                     z('o aviso: OS atualizada, respostas acompanharam', None, '+0.6', 1250, atraso=-2.0),
                     z('a área Checklists: agora dentro do Hi-Wall', 'as cinco respostas continuam: 5 de 13', '+1.0', 1250),
                     z('Período da OS', None, '+0.4', 1250),
                     # 1.38.24: "Horário de cada dia", "Adicionar outra data", "Adicionar dia" e o cartão do dia (Início/Fim); depois a
                     # câmera abre e mostra a aba inteira durante a fala sobre a internet
                     z('as datas da OS', 'o início e o fim de cada dia', '+1.2', 1400)]},
}


# ---------------------------------------------------------------- avisos na tela ("Dica: ...") do plano (T07/plano.md), por palavra da fala
# `linha` = 1ª linha = 1; o montar_cap.py procura pela linha de índice 0 (linha - 1) e pela palavra exata (sem pontuação nas pontas)
def dica(linha, palavra, texto, dur=4.5):
    return {'palavra': [linha - 1, palavra], 'dur': dur, 'texto': 'Dica: ' + texto, 'pos': 'bottom'}


DICAS = {
    '01': [dica(5, 'mesma', 'a mesma página serve ao técnico, ao gestor e ao cliente', 4.8)],
    '02': [dica(1, 'permitir', 'libere a localização na primeira vez; é ela que mostra o técnico no mapa do gestor', 5.2)],
    '03': [dica(1, 'registra', 'o check-in registra a hora e o local do atendimento', 4.2)],
    '04': [dica(3, 'gravada', 'cada resposta é salva na hora, com o celular conectado', 4.6),
           dica(6, 'lápis', 'toque no lápis para mudar uma resposta', 3.6)],
    '05': [dica(2, 'barra', 'as fotos sobem três por vez, com barra de progresso', 4.4)],
    '06': [dica(2, 'finalizada', 'o material só sai do estoque quando a OS é finalizada', 4.4),
           dica(5, 'Configurações', 'o recurso se liga em Configurações › Usabilidade › Consumo de estoque na OS', 5.6)],
    '07': [dica(2, 'Tudo', 'pausar mantém tudo o que já foi preenchido', 4.2)],
    '08': [dica(1, 'Parcial', 'a visita parcial fica em OS pausadas até ser retomada', 4.6)],
    '09': [dica(1, 'assinatura', 'para o cliente assinar, use uma pergunta de assinatura no checklist', 5.2)],
    '10': [dica(1, 'Resumo', 'confira o resumo do consumo antes de confirmar', 4.2)],
    '11': [dica(2, 'nome', 'o relatório mostra quem fez o check-in e o check-out', 4.4)],
    '12': [dica(1, 'login.', 'o cliente vê a OS pelo link, sem precisar de login', 4.0),
           dica(3, 'sozinha', 'a pesquisa aparece quando a OS é concluída', 4.0)],
    '14': [dica(2, 'gestor', 'quem libera o Editar OS é o gestor, pela permissão Editar OS em campo', 4.8),
           dica(10, 'internet', 'sem internet, o Editar OS fica desativado', 4.6)],
}
for _k, _v in DICAS.items():
    SPECS[_k].setdefault('callouts', []).extend(_v)


if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf8') as f:
        json.dump(SPECS, f, ensure_ascii=False, indent=1)
    print('specs.json:', ', '.join(sorted(SPECS)), '->', os.path.relpath(OUT, HERE))
