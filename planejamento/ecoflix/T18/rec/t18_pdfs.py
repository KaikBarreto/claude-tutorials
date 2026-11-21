#!/usr/bin/env python3
"""T18 · escreve em rec/mundo/storage/nfe-danfes/t18/ os PDF simulados do órgão ambiental que o "Baixar PDF" abre (o app só guarda o que o órgão
devolve; no mundo falso o órgão é simulado). Sem brasão, sem logo de órgão: só os campos do manifesto e do certificado, com os dados do mundo
fictício da Recicla Vale Metais, e o rodapé "documento simulado". Uso: python3 -I rec/t18/t18_pdfs.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'storage', 'nfe-danfes', 't18'))
CHAVE_1257 = '35261147318506000107550010000012571572049130'


def esc(t):
    return t.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def pdf(linhas):
    """linhas: [(tamanho, negrito, x, y, texto)] numa página A4; fonte Helvetica/WinAnsi."""
    cont = []
    for tam, neg, x, y, t in linhas:
        cont.append(f'BT /F{2 if neg else 1} {tam} Tf {x} {y} Td ({esc(t)}) Tj ET')
    c = '\n'.join(cont).encode('cp1252')
    objs = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
            b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>',
            b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
            b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>',
            b'<< /Length ' + str(len(c)).encode() + b' >>\nstream\n' + c + b'\nendstream']
    out = bytearray(b'%PDF-1.4\n')
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f'{i} 0 obj\n'.encode() + o + b'\nendobj\n'
    xref = len(out)
    out += f'xref\n0 {len(objs) + 1}\n0000000000 65535 f \n'.encode()
    for o in offs:
        out += f'{o:010d} 00000 n \n'.encode()
    out += f'trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode()
    return bytes(out)


def folha(titulo, numero, rotulo_num, blocos, rodape):
    L = [(10, False, 50, 800, 'EcoFlix · documento de demonstração'), (20, True, 50, 770, titulo), (14, True, 50, 745, f'{rotulo_num} {numero}')]
    y = 710
    for cab, campos in blocos:
        L.append((11, True, 50, y, cab.upper()))
        y -= 18
        for rot, val in campos:
            L.append((10, True, 60, y, rot + ':'))
            L.append((10, False, 170, y, val))
            y -= 16
        y -= 10
    L.append((8, False, 50, 40, rodape))
    return pdf(L)


RODAPE = 'Documento simulado para o tutorial EcoFlix: dados do mundo fictício da Recicla Vale Metais. Não tem valor oficial.'
GERADOR = ('Gerador', [('Razão social', 'Recicla Vale Metais Ltda'), ('CNPJ', '47.318.506/0001-07'), ('Unidade no SIGOR', '203918')])
TRANSP = ('Transportador', [('Razão social', 'Recicla Vale Metais Ltda'), ('CNPJ', '47.318.506/0001-07'), ('Unidade no SIGOR', '203918'),
                            ('Motorista', 'Jair Lopes'), ('Placa', 'GHT7B19')])
DEST = ('Destinador', [('Razão social', 'AÇOS QUIRIRIM INDUSTRIA E COMERCIO LTDA'), ('CNPJ', '98.463.027/0001-15'), ('Unidade no SIGOR', '187402')])


def mtr(numero, qtd, obs):
    res = ('Resíduo', [('Descrição', 'Sucata de ferro'), ('Código IBAMA', '19 12 02'), ('Quantidade', f'{qtd} TON'), ('Tratamento', 'Reciclagem')])
    resp = ('Responsável', [('Nome', 'Rafael Nogueira'), ('Cargo', 'Sócio-administrador'), ('Data de expedição', '10/11/2026'), ('Observação', obs)])
    return folha('Manifesto de Transporte de Resíduos', numero, 'MTR nº', [GERADOR, TRANSP, DEST, res, resp], RODAPE)


def cdf(numero, periodo, mtrs):
    dest = ('Destinador', [('Razão social', 'Recicla Vale Metais Ltda'), ('CNPJ', '47.318.506/0001-07'), ('Unidade no SIGOR', '203918'),
                           ('Responsável', 'Rafael Nogueira')])
    ger = ('Gerador', [('Razão social', 'Auto Peças Vale Forte'), ('CNPJ', '96.384.120/0001-09'), ('Unidade no SIGOR', '184527')])
    per = ('Período', [('De', periodo[0]), ('Até', periodo[1]), ('MTRs incluídos', ', '.join(mtrs))])
    return folha('Certificado de Destinação Final', numero, 'CDF nº', [per, dest, ger], RODAPE)


os.makedirs(SAIDA, exist_ok=True)
ARQ = {
    'mtr-2611000318.pdf': mtr('2611000318', '3,6', 'NF-e 1257 ' + CHAVE_1257),
    'mtr-2611000325.pdf': mtr('2611000325', '3,2', '-'),
    'cdf-2611000041.pdf': cdf('2611000041', ('01/10/2026', '31/10/2026'), ['2610001542', '2610001877', '2610002203']),
    'cdf-2611000057.pdf': cdf('2611000057', ('01/11/2026', '07/11/2026'), ['2611000102']),
    'cdf-2611000037.pdf': cdf('2611000037', ('01/09/2026', '30/09/2026'), ['2609001655', '2609002014']),
}
for nome, b in ARQ.items():
    open(os.path.join(SAIDA, nome), 'wb').write(b)
    print(nome, len(b), 'bytes')
