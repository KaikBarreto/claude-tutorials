#!/usr/bin/env python3
"""T8 · gera rec/t8/assets/nfe-gelo-norte.xml: NF-e FICTÍCIA da Gelo Norte Componentes Ltda para a aula (cap11, "Importar XML (NF-e)").

Tudo inventado: emitente = o fornecedor do cadastro (CNPJ 91.345.602/0001-36, com dígito válido), destinatário = Glacial Cold Brasil
(CNPJ 91.520.340/0001-07), chave de 44 dígitos com dígito verificador (módulo 11) e fora de `nfe_imports`. Três produtos: o primeiro
("Capacitor 40 µF 440V", com o MICRO SIGN U+00B5 igual ao do cadastro) casa por nome com o "Capacitor 40 µF" do estoque; os outros
dois ("Contator 25 A" e "Filtro secador") são novos. Total R$ 731,00 = 10 × 37,00 + 4 × 58,00 + 6 × 21,50.
Uso: python3 -I rec/t8/nfe.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(HERE, 'assets', 'nfe-gelo-norte.xml')

EMIT = dict(cnpj='91345602000136', nome='Gelo Norte Componentes Ltda', fant='Gelo Norte', ie='85412730', rua='Rua das Tulipas', nro='1280',
            bairro='Distrito Industrial', mun='Duque de Caxias', cmun='3301702', uf='RJ', cep='25085000', fone='2130003102')
DEST = dict(cnpj='91520340000107', nome='Glacial Cold Brasil', ie='86201437', rua='Rua Moreira César', nro='200', bairro='Icaraí',
            mun='Niterói', cmun='3303302', uf='RJ', cep='24230190', fone='2130001000')
ITENS = [  # cProd, nome, NCM, unidade, quantidade, valor unitário
    ('GN-CAP40-440', 'Capacitor 40 µF 440V', '85322900', 'UN', 10, 37.00),
    ('GN-CONT25A', 'Contator 25 A', '85364900', 'UN', 4, 58.00),
    ('GN-FSEC', 'Filtro secador', '84212100', 'UN', 6, 21.50),
]
SERIE, NNF, CNF = '001', '000004217', '47182936'
EMISSAO = '2026-11-03T08:12:00-03:00'
VENC = '2026-12-03'


def dv_chave(c43: str) -> str:
    pesos = [2, 3, 4, 5, 6, 7, 8, 9]
    s = sum(int(d) * pesos[i % 8] for i, d in enumerate(reversed(c43)))
    r = s % 11
    return '0' if r in (0, 1) else str(11 - r)


def chave() -> str:
    c43 = '33' + '2611' + EMIT['cnpj'] + '55' + SERIE + NNF + '1' + CNF
    assert len(c43) == 43, len(c43)
    return c43 + dv_chave(c43)


def money(v):
    return f'{v:.2f}'


def xml() -> str:
    k = chave()
    total = sum(q * p for _, _, _, _, q, p in ITENS)
    dets = []
    for i, (cprod, nome, ncm, un, q, p) in enumerate(ITENS, 1):
        vprod = q * p
        dets.append(f'''<det nItem="{i}"><prod><cProd>{cprod}</cProd><cEAN>SEM GTIN</cEAN><xProd>{nome}</xProd><NCM>{ncm}</NCM><CFOP>5102</CFOP><uCom>{un}</uCom><qCom>{q:.4f}</qCom><vUnCom>{p:.10f}</vUnCom><vProd>{money(vprod)}</vProd><cEANTrib>SEM GTIN</cEANTrib><uTrib>{un}</uTrib><qTrib>{q:.4f}</qTrib><vUnTrib>{p:.10f}</vUnTrib><indTot>1</indTot></prod><imposto><ICMS><ICMSSN102><orig>0</orig><CSOSN>102</CSOSN></ICMSSN102></ICMS></imposto></det>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00"><NFe xmlns="http://www.portalfiscal.inf.br/nfe"><infNFe Id="NFe{k}" versao="4.00"><ide><cUF>33</cUF><cNF>{CNF}</cNF><natOp>Venda de mercadoria</natOp><mod>55</mod><serie>{int(SERIE)}</serie><nNF>{int(NNF)}</nNF><dhEmi>{EMISSAO}</dhEmi><tpNF>1</tpNF><idDest>1</idDest><cMunFG>{EMIT['cmun']}</cMunFG><tpImp>1</tpImp><tpEmis>1</tpEmis><cDV>{k[-1]}</cDV><tpAmb>2</tpAmb><finNFe>1</finNFe><indFinal>0</indFinal><indPres>1</indPres></ide><emit><CNPJ>{EMIT['cnpj']}</CNPJ><xNome>{EMIT['nome']}</xNome><xFant>{EMIT['fant']}</xFant><enderEmit><xLgr>{EMIT['rua']}</xLgr><nro>{EMIT['nro']}</nro><xBairro>{EMIT['bairro']}</xBairro><cMun>{EMIT['cmun']}</cMun><xMun>{EMIT['mun']}</xMun><UF>{EMIT['uf']}</UF><CEP>{EMIT['cep']}</CEP><fone>{EMIT['fone']}</fone></enderEmit><IE>{EMIT['ie']}</IE><CRT>1</CRT></emit><dest><CNPJ>{DEST['cnpj']}</CNPJ><xNome>{DEST['nome']}</xNome><enderDest><xLgr>{DEST['rua']}</xLgr><nro>{DEST['nro']}</nro><xBairro>{DEST['bairro']}</xBairro><cMun>{DEST['cmun']}</cMun><xMun>{DEST['mun']}</xMun><UF>{DEST['uf']}</UF><CEP>{DEST['cep']}</CEP><fone>{DEST['fone']}</fone></enderDest><indIEDest>1</indIEDest><IE>{DEST['ie']}</IE></dest>{''.join(dets)}<total><ICMSTot><vBC>0.00</vBC><vICMS>0.00</vICMS><vICMSDeson>0.00</vICMSDeson><vFCP>0.00</vFCP><vBCST>0.00</vBCST><vST>0.00</vST><vFCPST>0.00</vFCPST><vFCPSTRet>0.00</vFCPSTRet><vProd>{money(total)}</vProd><vFrete>0.00</vFrete><vSeg>0.00</vSeg><vDesc>0.00</vDesc><vII>0.00</vII><vIPI>0.00</vIPI><vIPIDevol>0.00</vIPIDevol><vPIS>0.00</vPIS><vCOFINS>0.00</vCOFINS><vOutro>0.00</vOutro><vNF>{money(total)}</vNF></ICMSTot></total><transp><modFrete>9</modFrete></transp><cobr><fat><nFat>{int(NNF)}</nFat><vOrig>{money(total)}</vOrig><vDesc>0.00</vDesc><vLiq>{money(total)}</vLiq></fat><dup><nDup>001</nDup><dVenc>{VENC}</dVenc><vDup>{money(total)}</vDup></dup></cobr><pag><detPag><indPag>1</indPag><tPag>15</tPag><vPag>{money(total)}</vPag></detPag></pag><infAdic><infCpl>Nota fiscal fictícia para fins de demonstração. Sem valor fiscal.</infCpl></infAdic></infNFe></NFe></nfeProc>
'''


if __name__ == '__main__':
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, 'w', encoding='utf8') as f:
        f.write(xml())
    print('gravado', SAIDA)
    print('chave', chave(), 'total', money(sum(q * p for _, _, _, _, q, p in ITENS)))
