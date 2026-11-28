#!/usr/bin/env python3
"""T17 · sementes da cadeia SEM navegador: repete na instância 54317, pela API do Supabase falso (REST, RPC e functions), o que cada
capítulo que grava faz na tela, e chama o t17_semente.py para gravar a semente cumulativa. Serve de reserva: o ensaio de cada
capítulo regrava a mesma semente com o estado deixado pela tela (t17_lote.sh, quando o capítulo passa sem falha).
Cadeia: inicio -> apos-cap02 (frota) -> apos-cap04 (MDF-e nº 1 autorizado, 09:3x) -> [14:20] apos-cap05 (encerrado) -> apos-cap08
(NFS-e 14 autorizada) -> apos-cap09 (NFS-e recebidas ativado) -> apos-cap10 (+ as duas notas recebidas) -> apos-cap14 (saldo inicial (capítulo 14 desde 28/11; era apos-cap13)
fiscal da bateria, 3.320 kg em 31/10/2026).
Uso (fora da fila: não abre navegador): TUT_SENHA=... python3 -I rec/t17/t17_semente_api.py"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TUT = os.path.normpath(os.path.join(HERE, '..', '..'))
FAKE = 'http://127.0.0.1:54317'
N0930, N1420 = '2026-11-10T09:30:00-03:00', '2026-11-10T14:20:00-03:00'
TOK = None


def sid(chave):
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def http(metodo, caminho, corpo=None, extra=None):
    h = {'content-type': 'application/json', 'apikey': 'x'}
    if TOK:
        h['Authorization'] = 'Bearer ' + TOK
    h.update(extra or {})
    r = urllib.request.Request(FAKE + caminho, data=None if corpo is None else json.dumps(corpo).encode(), headers=h, method=metodo)
    try:
        t = urllib.request.urlopen(r, timeout=60).read().decode()
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{metodo} {caminho}: {e.code} {e.read().decode()[:400]}')
    return json.loads(t) if t.strip() else None


def subir(fake_now):
    env = dict(os.environ, FAKE_NOW=fake_now, FAKE_PORT='54317')
    subprocess.run(['bash', 'rec/run.sh', 'fake'], cwd=TUT, env=env, check=True, stdout=subprocess.DEVNULL, pass_fds=())
    time.sleep(1)
    global TOK
    TOK = None
    d = http('POST', '/auth/v1/token?grant_type=password', {'email': 'rafael@reciclavalemetais.example', 'password': os.environ['TUT_SENHA']})
    TOK = d['access_token']


def semear(*arquivos):
    http('POST', '/__dev/reset')
    r = http('POST', '/__dev/seed', {'files': list(arquivos)})
    if not r.get('ok'):
        raise SystemExit(f'semente {arquivos}: {r}')


def gravar(nome):
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 't17_semente.py'), nome], check=True, stdout=subprocess.DEVNULL)
    print('gravada', nome)


REP = {'Prefer': 'return=representation'}
CID, CFG = sid('company.reciclavale'), sid('fiscal.matriz')


def main():
    if len(os.environ.get('TUT_SENHA', '')) < 8:
        raise SystemExit('TUT_SENHA (8+ caracteres) no ambiente')
    # ---- manhã (09:30): frota e MDF-e nº 1
    subir(N0930)
    semear('t17/inicio')
    http('PATCH', f'/rest/v1/vehicles?id=eq.{sid("veiculo.truck")}', {'uf_licenciamento': 'SP', 'categoria': 'unico', 'tipo_rodado': '01', 'tipo_carroceria': '01', 'capacidade_m3': 30})
    http('PATCH', f'/rest/v1/drivers?id=eq.{sid("motorista.truck")}', {'document': '31847265090', 'cnh': '04728193604', 'cnh_categoria': 'C', 'cnh_validade': '2029-03-18'})
    gravar('apos-cap02')
    semear('t17/inicio', 't17/apos-cap02')
    notas = [n for n in http('GET', '/rest/v1/invoices?invoice_number=in.(1255,1256)&select=id,nfe_key,total_amount,invoice_number')]
    assert len(notas) == 2, notas
    m = http('POST', '/rest/v1/mdfe_manifests', {
        'company_id': CID, 'fiscal_config_id': CFG, 'serie': 1, 'status': 'pendente', 'modal': 'rodoviario', 'tipo_emitente': 2, 'emission_mode': 'normal',
        'contingency_reason': None, 'tipo_carga': None, 'descricao_produto_predominante': None, 'ncm_produto_predominante': None,
        'cep_carregamento': None, 'cep_descarregamento': None, 'placa_veiculo': 'FKD2E41', 'uf_veiculo': 'SP', 'condutor_nome': 'Edson Moura',
        'condutor_cpf': '31847265090', 'rntrc': None, 'ciot': None, 'ciot_cpf_cnpj': None, 'contratante_cpf_cnpj': None, 'contratante_nome': None,
        'tara_veiculo': 6380, 'reboques': [], 'tipo_rodado': '01', 'tipo_carroceria': '01', 'capacidade_kg': 14000, 'capacidade_m3': 30,
        'uf_carregamento': 'SP', 'cidade_carregamento': 'Taubaté', 'codigo_ibge_carregamento': '3554102', 'uf_descarregamento': 'MG',
        'cidade_descarregamento': 'Itamonte', 'codigo_ibge_descarregamento': '3133006', 'peso_bruto_total': 5800, 'valor_total_carga': 55380,
        'observacoes': None, 'percurso_ufs': ['RJ'], 'created_by': sid('user.rafael')}, REP)
    m = m[0] if isinstance(m, list) else m
    print('MDF-e criado: nº', m.get('mdfe_number'), m.get('status'))
    http('POST', '/rest/v1/mdfe_invoices', [{'mdfe_id': m['id'], 'invoice_id': n['id'], 'nfe_key': n['nfe_key']} for n in notas])
    print(' prepare:', http('POST', '/functions/v1/mdfe-contingency', {'mdfeId': m['id'], 'action': 'prepare'}).get('status'))
    print(' status:', http('POST', '/functions/v1/mdfe-contingency', {'mdfeId': m['id'], 'action': 'status'}).get('status'))
    gravar('apos-cap04')
    # ---- tarde (14:20): encerrar, NFS-e 14, NFS-e recebidas, saldo inicial
    subir(N1420)
    semear('t17/inicio', 't17/apos-cap04')
    print(' enclose:', http('POST', '/functions/v1/mdfe-contingency', {'mdfeId': m['id'], 'action': 'enclose'}).get('status'))
    print(' status:', http('POST', '/functions/v1/mdfe-contingency', {'mdfeId': m['id'], 'action': 'status'}).get('status'))
    gravar('apos-cap05')
    semear('t17/inicio', 't17/apos-cap05')
    n = http('POST', '/rest/v1/nfse_invoices', {
        'company_id': CID, 'fiscal_config_id': CFG, 'serie': 1, 'customer_id': sid('cliente.quiririm'), 'tomador_avulso': None,
        'intermediario_customer_id': None, 'data_competencia': '2026-11-06', 'regime_apuracao_tributaria': 3, 'total_servicos': 1850,
        'total_deducoes': 0, 'total_iss': 55.5, 'total_amount': 1850, 'desconto_condicionado': 0, 'desconto_incondicionado': 0,
        'retencao_pis': 0, 'retencao_cofins': 0, 'retencao_csll': 0, 'retencao_inss': 0, 'retencao_irrf': 0,
        'municipio_incidencia_nome': 'Taubaté', 'municipio_incidencia_ibge': '3554102', 'status': 'rascunho'}, REP)
    n = n[0] if isinstance(n, list) else n
    http('POST', '/rest/v1/nfse_invoice_services', [{
        'nfse_invoice_id': n['id'], 'service_id': None, 'codigo_servico': '7.09', 'codigo_tributacao': '070901', 'codigo_tributacao_municipal': None,
        'cnae': None, 'nbs': None, 'discriminacao': 'Coleta e remoção de resíduos metálicos com caçamba no pátio da Aços Quiririm em 06/11/2026.',
        'issqn_situacao': 1, 'iss_aliquota': 3, 'iss_retido': False, 'iss_valor': 55.5, 'valor_servico': 1850, 'deducoes': 0, 'base_calculo': 1850}])
    print(' NFS-e emit:', http('POST', '/functions/v1/plugnotas-emit-nfse', {'nfseInvoiceId': n['id']}))
    print(' NFS-e status:', http('POST', '/functions/v1/plugnotas-nfse-status', {'nfseInvoiceId': n['id']}).get('status'))
    gravar('apos-cap08')
    semear('t17/inicio', 't17/apos-cap08')
    agora = http('GET', f'/rest/v1/nfse_invoices?id=eq.{n["id"]}&select=authorized_at')[0]['authorized_at']
    http('PATCH', f'/rest/v1/company_fiscal_config?id=eq.{CFG}', {'nfse_dfe_ativo': True, 'nfse_dfe_fonte': 'sefin', 'nfse_dfe_proxima_consulta_em': agora, 'nfse_dfe_count_start_at': agora})
    gravar('apos-cap09')
    semear('t17/inicio', 't17/apos-cap09', 't17/nfse-recebidas')
    gravar('apos-cap10')
    semear('t17/inicio', 't17/apos-cap10')
    r = http('POST', '/rest/v1/rpc/record_fiscal_inventory_entries', {
        'p_company_id': CID, 'p_fiscal_config_id': CFG, 'p_effective_at': '2026-10-31T00:00:00-03:00', 'p_entry_type': 'opening_balance',
        'p_entries': [{'material_id': sid('material.bateria'), 'quantity': 3320}], 'p_source': 'manual', 'p_reason': 'Saldo inicial informado',
        'p_client_request_id': sid('t17.saldo_inicial_bateria')})
    print(' saldo inicial:', r)
    gravar('apos-cap14')
    semear('t17/inicio', 't17/apos-cap14')
    pos = http('POST', '/rest/v1/rpc/get_fiscal_inventory_position', {'p_company_id': CID, 'p_fiscal_config_id': None})
    print(' bateria:', [(x['current_quantity'], x['has_opening_balance']) for x in pos if 'Bateria' in x['material_name']])


if __name__ == '__main__':
    main()
