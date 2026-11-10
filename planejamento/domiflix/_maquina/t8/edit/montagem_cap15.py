#!/usr/bin/env python3
"""T8 cap. 15 · Recapitulando: montagem de trechos ACELERADOS das gravações brutas dos capítulos anteriores, um bloco por linha da fala, com o
tamanho exato da linha. Sai como MP4 1587x992 (a janela do app em repouso) para o editor (illustrations, loop false).
Precisa das gravações brutas (rec/t8/t8-capNN.mp4 + .actions.json): rodar sob a trava ANTES da limpeza.
  L1  cap02 (cadastro) e cap03 (entrada/saída e estoque baixo)
  L2  cap04 (van), cap05 (transferência), cap06 (acesso), cap07 (Kardex)
  L3  cap08 a cap11 (requisição, cotações, ordens, nota fiscal)
  L4  cap12 (inventário), cap13 (posição), cap14 (relatório)
uso: python3 -I montagem_cap15.py [saida.mp4]"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
REC = os.path.join(DOMI, 'rec', 't8')
NARR = json.load(open(os.path.join(DOMI, 't8', 'narracao', 'cap15.json'), encoding='utf8'))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'montagem_cap15.mp4')
W, H, FPS = 1586, 992, 30

# (linha 1..4, [(capítulo, rótulo de início, rótulo de fim, folga antes, folga depois)]); a linha 5 (próximo passo) fica com a tela ao vivo
BLOCOS = [
    (1, [('02', 'o código EST-010, já preenchido', 'a linha Capacitor 40 µF na lista', 0.6, 0.6), ('03', 'quantidade: 10', 'o cartão Estoque baixo: de 2 para 3', 0.6, 0.6)]),
    (2, [('04', 'desmarca todos (a Van começa com tudo marcado)', 'os três materiais da Van 01', 0.4, 0.4), ('05', 'origem: Estoque Principal, 8,5 disponíveis', 'R-410A com 2 kg na Van 01', 0.4, 0.4),
         ('06', 'liga "Restringir acesso a este local"', 'Salvar acesso', 0.4, 0.4), ('07', 'a entrada da Fita isolante', 'a transferência: Estoque Principal → Van 01', 0.4, 0.4)]),
    (3, [('08', 'título: Reposição de gás, cobre e capacitor', 'Capacitor 40 µF: 6', 0.6, 0.6), ('09', 'escolhe a Ventura Gás e Tubos', 'Total geral', 0.4, 0.4),
         ('09', 'fornecedor escolhido do R-410A: Ventura', 'os três materiais com fornecedor escolhido', 0.4, 0.4), ('10', 'pedido, recebido e pendente', 'Confirmar recebimento (Cobre Sul)', 0.4, 0.4),
         ('11', 'o fornecedor: Gelo Norte Componentes', 'o filtro secador: Criar novo item', 0.4, 0.4)]),
    (4, [('12', 'R-410A contado: 16', 'a faixa: Divergências encontradas, 2 itens', 0.4, 0.4), ('13', 'abre o calendário', 'o R-410A com o saldo daquele dia', 0.4, 0.4),
         ('14', 'Último preço: R$ 94,00', 'Variação do último preço', 0.4, 0.4)]),
]


def acao(acts, rot):
    for a in acts:
        if a.get('label') == rot:
            return a
    raise SystemExit(f'rótulo {rot!r} não achado')


def main():
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    tmp = os.path.join(os.path.dirname(SAIDA), '_montagem_cap15')
    os.makedirs(tmp, exist_ok=True)
    partes = []
    for linha, clipes in BLOCOS:
        l = NARR['linhas'][linha - 1]
        slot_total = round(NARR['linhas'][linha]['s'] - l['s'], 2)  # até o início da linha seguinte (sem vão entre os blocos)
        slot = slot_total / len(clipes)
        for k, (cap, de, ate, antes, depois) in enumerate(clipes):
            A = json.load(open(os.path.join(REC, f't8-cap{cap}.actions.json')))
            acts = A['actions']
            t0 = max(0.0, acao(acts, de)['tStart'] - antes)
            t1 = acao(acts, ate)['tEnd'] + depois
            dur = t1 - t0
            n = int(round(slot * FPS))
            fator = slot / dur  # < 1: acelera; > 1 desacelera (evita: abre o trecho até caber)
            if fator > 1.0:
                t1 = t0 + slot
                dur = slot
                fator = 1.0
            out = os.path.join(tmp, f'l{linha}_{k}.mp4')
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', os.path.join(REC, f't8-cap{cap}.mp4'), '-an',
                            '-vf', f'setpts=(PTS-STARTPTS)*{fator:.5f},scale={W}:{H}:flags=area,fps={FPS}', '-frames:v', str(n),
                            '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out], check=True)
            partes.append(out)
            print(f'L{linha} cap{cap}: {t0:.1f}-{t1:.1f} s ({dur:.1f} s) -> {slot:.2f} s, x{1 / fator:.1f}')
    lista = os.path.join(tmp, 'lista.txt')
    open(lista, 'w').write(''.join(f"file '{p}'\n" for p in partes))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', SAIDA], check=True)
    print('ok', SAIDA)


if __name__ == '__main__':
    main()
