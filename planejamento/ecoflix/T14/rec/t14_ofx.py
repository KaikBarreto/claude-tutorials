#!/usr/bin/env python3
"""T14 · gera o extrato OFX FICTÍCIO da Conta Principal (rec/t14/arquivos/Extrato_20261101_20261110.ofx) e o espelho das linhas
(rec/t14/arquivos/linhas.json, usado pelo t14_sementes.py). OFX 1.x SGML no molde de src/utils/ofx/fixtures/itau_sgml.ofx do app.
Banco e conta fictícios (BANKID 0999, ACCTID 40218-7); memos sem acento; nenhum memo começa com "SALDO" (o parser descarta).
Linhas do T14/plano.md ("O extrato OFX"), com a junção (MUNDO_LINHA_DO_TEMPO.md, seção 15): o Pix de 380,00 de 06/11 09:40 é da Aparecida.
Segundos diferentes nas linhas do mesmo minuto: a tabela do app ordena por posted_at e depois pelo id (aleatório no import ao vivo)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = 44933.47
# (nº do plano, AAAAMMDDHHMMSS, TRNTYPE, valor, memo)
LINHAS = [
    (1, '20261103094100', 'DEBIT', -2250.00, 'PIX ENVIADO DEPOSITO IRMAOS SIQUEIRA'),
    (2, '20261105100600', 'DEBIT', -6800.00, 'PIX ENVIADO ALUGUEL GALPAO NOV'),
    (3, '20261106094100', 'DEBIT', -380.00, 'PIX ENVIADO APARECIDA RAMOS'),
    (4, '20261106140600', 'DEBIT', -380.00, 'PIX ENVIADO AUTO PECAS VALE FORTE'),
    (5, '20261109080000', 'PAYMENT', -238.40, 'PAGTO BOLETO AGUA E ESGOTO'),
    (6, '20261109091200', 'CREDIT', 4815.00, 'PIX RECEBIDO SERRA FINA ALUMINIO'),
    (7, '20261109110100', 'DEBIT', -180.00, 'PIX ENVIADO BORRACHARIA DOIS IRMAOS'),
    (8, '20261109230000', 'FEE', -64.90, 'TARIFA PACOTE SERVICOS'),
    (9, '20261109230010', 'FEE', -12.00, 'TARIFA AVULSA'),
    (10, '20261109233000', 'CREDIT', 12.00, 'ESTORNO TARIFA AVULSA'),
    (11, '20261110080500', 'DEBIT', -1874.30, 'PIX ENVIADO CONCESSIONARIA ENERGIA'),
    (12, '20261110081000', 'DEBIT', -1740.00, 'PIX ENVIADO HIDRAULICA MORETTI LTDA'),
    (14, '20261110081030', 'DEBIT', -350.00, 'PIX ENVIADO AUTO POSTO BOA VIAGEM'),
    (13, '20261110081500', 'CREDIT', 2000.00, 'PIX RECEBIDO ACOS QUIRIRIM LTDA'),
    (15, '20261110082000', 'XFER', 8000.00, 'PIX RECEBIDO RECICLA VALE METAIS LTDA'),
    (16, '20261110082500', 'ATM', -2000.00, 'SAQUE CAIXA ELETRONICO'),
    (17, '20261110082530', 'FEE', -6.50, 'TARIFA SAQUE'),
]
soma = round(sum(v for _, _, _, v, _ in LINHAS), 2)
assert soma == -1449.10, soma
assert round(LEDGER - soma, 2) == 46382.57
cab = ('OFXHEADER:100\nDATA:OFXSGML\nVERSION:102\nSECURITY:NONE\nENCODING:USASCII\nCHARSET:1252\nCOMPRESSION:NONE\nOLDFILEUID:NONE\nNEWFILEUID:NONE\n\n'
       '<OFX>\n<SIGNONMSGSRSV1>\n<SONRS>\n<STATUS>\n<CODE>0\n<SEVERITY>INFO\n</STATUS>\n<DTSERVER>20261110083000[-3:BRT]\n<LANGUAGE>POR\n</SONRS>\n</SIGNONMSGSRSV1>\n'
       '<BANKMSGSRSV1>\n<STMTTRNRS>\n<TRNUID>1001\n<STATUS>\n<CODE>0\n<SEVERITY>INFO\n</STATUS>\n<STMTRS>\n<CURDEF>BRL\n<BANKACCTFROM>\n<BANKID>0999\n'
       '<ACCTID>40218-7\n<ACCTTYPE>CHECKING\n</BANKACCTFROM>\n<BANKTRANLIST>\n<DTSTART>20261101\n<DTEND>20261110\n')
corpo = ''.join(f'<STMTTRN>\n<TRNTYPE>{t}\n<DTPOSTED>{d}[-3:BRT]\n<TRNAMT>{v:.2f}\n<FITID>{d[:8]}{n:05d}\n<MEMO>{m}\n</STMTTRN>\n' for n, d, t, v, m in LINHAS)
fim = (f'</BANKTRANLIST>\n<LEDGERBAL>\n<BALAMT>{LEDGER:.2f}\n<DTASOF>20261110\n</LEDGERBAL>\n</STMTRS>\n</STMTTRNRS>\n</BANKMSGSRSV1>\n</OFX>\n')
os.makedirs(os.path.join(HERE, 'arquivos'), exist_ok=True)
with open(os.path.join(HERE, 'arquivos', 'Extrato_20261101_20261110.ofx'), 'w', encoding='ascii', newline='\r\n') as f:
    f.write(cab + corpo + fim)
json.dump([{'n': n, 'dt': d, 'trn': t, 'valor': v, 'memo': m, 'fitid': f'{d[:8]}{n:05d}'} for n, d, t, v, m in LINHAS],
          open(os.path.join(HERE, 'arquivos', 'linhas.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'OFX: {len(LINHAS)} linhas, soma {soma}, saldo final {LEDGER}, abertura {round(LEDGER - soma, 2)}')
