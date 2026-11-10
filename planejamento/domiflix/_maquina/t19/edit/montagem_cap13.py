#!/usr/bin/env python3
"""T19 cap. 13 · Recapitulando: montagem de trechos ACELERADOS das gravações brutas dos capítulos anteriores, um bloco por linha da fala, com o tamanho
exato da linha (a linha 4 vai até o fim da narração). Sai como MP4 1586x992 (a janela do app em repouso) para o editor (ilustrações, loop false).
Precisa das gravações brutas (rec/t19/t19-capNN.mp4 + .actions.json): rodar sob a trava ANTES da limpeza.
  L1  cap02 cartão com o selo Ativo; cap03 Lançamento no Financeiro; cap05 o Simulador
  L2  cap06 a cobrança gerada com o QR Code; cap08 Pagamento confirmado; cap09 a lista com Pago
  L3  cap10 a assinatura Ativa com o MRR; cap12 a parcela com Cobrança gerada
  L4  cap09 a receita e a tarifa nas Movimentações; a conta a receber com bruto, taxa e líquido
uso: python3 -I montagem_cap13.py [saida.mp4]"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOMI = os.path.dirname(os.path.dirname(HERE))
REC = os.path.join(DOMI, 'rec', 't19')
NARR = json.load(open(os.path.join(DOMI, 't19', 'narracao', 'cap13.json'), encoding='utf8'))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'montagem_cap13.mp4')
W, H, FPS = 1586, 992, 30

# (linha 1..5, [(capítulo, rótulo de início, rótulo de fim, folga antes, folga depois)])
BLOCOS = [
    (1, [('02', 'confere depois de recarregar, o cartão mostra as taxas da conta (sem "referência")', 'confere depois de recarregar, o cartão mostra as taxas da conta (sem "referência")', 0.3, 1.8),
         ('03', 'categoria da taxa: Tarifas e Taxas', 'Salvar a seção Lançamento no Financeiro', 0.3, 0.6),
         ('05', 'Valor líquido na sua conta', 'Valor líquido na sua conta', 0.3, 1.6)]),
    (2, [('06', 'Gerar cobrança', 'QR Code da cobrança', 0.8, 0.8), ('08', 'Pagamento confirmado', 'Pagamento confirmado', 1.0, 1.0),
         ('09', 'a linha Pago', 'cartão Recebido com R$ 450,00', 0.6, 0.8)]),
    (3, [('10', 'Criar assinatura', 'Receita recorrente mensal (MRR)', 0.3, 0.8), ('12', 'Gerar agora', 'selo Cobrança gerada na parcela', 0.3, 0.8)]),
    (4, [('09', 'a receita em Vendas de Serviços', 'a tarifa em Tarifas e Taxas', 0.6, 0.8), ('09', 'Bruto, Taxa e Líquido da conta a receber', 'Bruto, Taxa e Líquido da conta a receber', 0.3, 1.0)]),
]


def acao(acts, rot):
    for a in acts:
        if a.get('label') == rot:
            return a
    raise SystemExit(f'rótulo {rot!r} não achado')


def main():
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    tmp = os.path.join(os.path.dirname(SAIDA), '_montagem_cap13')
    os.makedirs(tmp, exist_ok=True)
    partes = []
    for linha, clipes in BLOCOS:
        l = NARR['linhas'][linha - 1]
        prox = NARR['linhas'][linha]['s'] if linha < len(NARR['linhas']) else NARR['dur']
        slot_total = round(prox - l['s'], 2)  # até o início da linha seguinte (a última, até o fim da narração; sem vão entre os blocos)
        slot = slot_total / len(clipes)
        for k, (cap, de, ate, antes, depois) in enumerate(clipes):
            A = json.load(open(os.path.join(REC, f't19-cap{cap}.actions.json')))
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
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', os.path.join(REC, f't19-cap{cap}.mp4'), '-an',
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
