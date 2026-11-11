#!/usr/bin/env python3
"""T20 · escreve rec/mundo/seeds-extra/t20/{inicio,apos-cap03,apos-cap04,apos-cap06,apos-cap08}.json (plano.md, "Mundo: o que esta aula precisa").
Por cima do mundo base B (10/11 08:30; FAKE_NOW da aula: 10/11 15:00): link do portal fixo da Cooperativa Recomeço e da Fundição Bandeira do Vale,
empresa com o QR de fotos no comprovante, o Pix de R$ 1.200,00 das 08:35 (saldo da cooperativa R$ 1.350,00), a compra do ticket #58 (T8, latinha),
a venda sem valor da T7 e a NF-e 1250 (T16) da Fundição, as coletas #1, #5 e #10 da cooperativa e as três fotos da compra de 06/11 com o link
público de fotos. As apos-capNN são CUMULATIVAS sobre o inicio (o robô carrega inicio + a última da cadeia).
A senha do portal (cap04) NUNCA fica em arquivo: o hash (sha256 salgado com o id, lib/portal.mjs) sai da variável de ambiente PORTAL_SENHA.
Uso: PORTAL_SENHA=... python3 -I rec/t20/t20_sementes.py"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't20'))
CO, RAFAEL, MARCOS, JULIANA = '@id:company.reciclavale', '@id:user.rafael', '@id:user.marcos', '@id:user.juliana'
COOP, BAND = '@id:fornecedor.recomeco', '@id:cliente.bandeira'
BAL_COOP = '@id:saldo.supplier:@id:fornecedor.recomeco'
SENHA_USUARIO = 'cooperativa.recomeco'


def stable_id(chave):
    """o mesmo UUID estável do Supabase falso (core/util.mjs stableId)"""
    h = bytearray(hashlib.sha1(('domiflix-fake:' + chave).encode()).digest())
    h[6] = (h[6] & 0x0F) | 0x50
    h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex()
    return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


def z(data, hora):
    from datetime import datetime, timedelta
    h, m = map(int, hora.split(':'))
    return (datetime.fromisoformat(f'{data}T{h:02d}:{m:02d}:00') + timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def item(pid, k, mat, nome, qtd, preco, tipo):
    return {'id': f'@id:t20.{tipo}i.{pid}.{k}', f'{"purchase" if tipo == "pi" else "sale"}_id': f'@id:t20.{"compra" if tipo == "pi" else "venda"}.{pid}',
            'material_id': f'@id:material.{mat}', 'material_name': nome, 'quantity': qtd, 'unit_price': preco, 'total_price': round(qtd * preco, 2), 'impurity': 0,
            'impurity_kg': None, 'impurity_pct': None, 'item_discount': 0, 'tare_weight': None, 'first_weight': None, 'second_weight': None,
            'weighing_mode': None, 'weight_source': 'manual'}


CFG_PORTAL = {'historico': True, 'resumo': True, 'grafico': True, 'valores': True, 'fotos': True, 'saldo': True, 'notas': True, 'relatorio': True,
              'relatorio_valores': True, 'coletas': True, 'solicitar_coleta': True, 'precos': False,
              'locked': {'historico': True, 'saldo': True, 'notas': True, 'relatorio': True, 'coletas': True, 'precos': True}}


def inicio():
    d = {'_doc': 'T20 · mundo do portal em 10/11/2026 15:00 (gerado por rec/t20/t20_sementes.py; não editar à mão).'}
    d['_patch'] = {
        'companies': [{'match': {'id': CO}, 'set': {'show_photo_qr_on_receipt': True, 'receipt_format': 'thermal_80mm'}}],
        'suppliers': [{'match': {'id': COOP}, 'set': {'portal_token': '@id:t20.portal.recomeco', 'portal_config': None, 'portal_password_enabled': False,
                                                      'portal_username': None, 'portal_password_hash': None, 'portal_receipt_format': 'auto'}}],
        'customers': [{'match': {'id': BAND}, 'set': {'portal_token': '@id:t20.portal.bandeira', 'portal_config': None, 'portal_password_enabled': False,
                                                      'portal_username': None, 'portal_password_hash': None, 'portal_receipt_format': 'auto'}}],
        'balances': [{'match': {'id': BAL_COOP}, 'set': {'balance': 1350, 'updated_at': z('2026-11-10', '08:35')}}],
    }
    d['balance_movements'] = [{
        'id': '@id:t20.bm.pix1200', 'company_id': CO, 'balance_id': BAL_COOP, 'entity_type': 'supplier', 'entity_id': COOP, 'movement_type': 'payment',
        'amount': -1200, 'description': 'Valor Pago a Cooperativa Recomeço · Acerto parcial da entrega de 06/11', 'transaction_at': z('2026-11-10', '08:35'),
        'transaction_date': '2026-11-10', 'created_at': z('2026-11-10', '08:35'), 'created_by': RAFAEL, 'is_settled': False, 'payment_method': 'transfer'}]
    # compra do ticket #58 (T8): latinha 3.018,4 kg x 6,20 = 18.714,08, Pix, hoje 09:00
    d['purchases'] = [{
        'id': '@id:t20.compra.1761', 'company_id': CO, 'order_number': 1761, 'order_seq': 1761, 'order_period': None, 'order_ref': '#1761', 'status': 'completed',
        'total_amount': 18714.08, 'paid_amount': 18714.08, 'payment_method': 'transfer', 'created_by': RAFAEL, 'transaction_at': z('2026-11-10', '09:00'),
        'transaction_date': '2026-11-10', 'created_at': z('2026-11-10', '09:00'), 'currency': 'BRL', 'hide_financial_details': False, 'notes': None,
        'driver_name': None, 'vehicle_plate': None, 'driver_id': None, 'vehicle_id': None, 'supplier_id': COOP}]
    d['purchase_items'] = [item(1761, 0, 'al_latinha', 'Alumínio latinha', 3018.4, 6.2, 'pi')]
    # venda sem valor da T7 (Fundição, hoje 08:35, Pix R$ 7.722,80)
    d['sales'] = [{
        'id': '@id:t20.venda.1760', 'company_id': CO, 'order_number': 1760, 'order_seq': 1760, 'order_period': None, 'order_ref': '#1760', 'status': 'completed',
        'total_amount': 7722.8, 'paid_amount': 7722.8, 'payment_method': 'transfer', 'created_by': RAFAEL, 'transaction_at': z('2026-11-10', '08:35'),
        'transaction_date': '2026-11-10', 'created_at': z('2026-11-10', '08:35'), 'currency': 'BRL', 'hide_financial_details': True, 'notes': None,
        'driver_name': None, 'vehicle_plate': None, 'driver_id': None, 'vehicle_id': None, 'customer_id': BAND}]
    d['sale_items'] = [item(1760, 0, 'latao', 'Metal amarelo (latão)', 152, 31.9, 'si'), item(1760, 1, 'cobre_mel', 'Cobre mel', 60, 47.9, 'si')]
    # NF-e 1250 (T16): a carga de ontem sai hoje com a nota, autorizada 08:45
    d['invoices'] = [{
        'id': '@id:t20.nfe.1250', 'company_id': CO, 'fiscal_config_id': '@id:fiscal.matriz', 'invoice_number': 1250, 'serie': 1, 'modelo': 55, 'invoice_type': 'saida',
        'status': 'emitida', 'environment': 'producao', 'finalidade': 1, 'nature_operation': 'Venda de mercadorias', 'cfop_default': '5102', 'modalidade_frete': 9,
        'is_consumer_final': False, 'customer_id': BAND, 'supplier_id': None, 'destinatario_avulso': None, 'order_id': None, 'order_type': None,
        'issue_date': z('2026-11-10', '08:44'), 'authorized_at': z('2026-11-10', '08:45'), 'nfe_key': '35261147318506000107550010000012501532176840',
        'nfe_protocol': '135260130933615', 'plugnotas_id': 'pn-001250', 'total_products': 23950, 'total_amount': 23950, 'total_freight': 0, 'other_expenses': 0,
        'valor_desconto_total': 0, 'computa_estoque_fiscal': True, 'baixa_estoque_ao_emitir': False, 'created_by': JULIANA, 'created_at': z('2026-11-10', '08:44'),
        'updated_at': z('2026-11-10', '08:45')}]

    def coleta(n, num, status, dia, janela, material, origem, criada, concluida=None, obs=None):
        return {'id': f'@id:t20.coleta.{n}', 'company_id': CO, 'numero': num, 'status': status, 'origem': origem, 'partner_type': 'supplier', 'partner_id': COOP,
                'partner_nome': 'Cooperativa Recomeço', 'contato_telefone': None, 'logradouro': 'Rua do Trabalho', 'numero_end': '57',
                'bairro': 'Vila Nossa Senhora das Graças', 'cidade': 'Taubaté', 'uf': 'SP', 'cep': '12060-640', 'scheduled_date': dia, 'scheduled_window': janela,
                'driver_id': None, 'driver_name': None, 'vehicle_id': None, 'vehicle_plate': None, 'material_estimado': material, 'observacoes': obs,
                'completed_at': concluida, 'public_short_code': hashlib.sha1(f't20-{n}'.encode()).hexdigest()[:12].translate(str.maketrans('01il o', '23xyzp'.ljust(6)[:6])).replace(' ', 'p'),
                'created_at': criada, 'updated_at': concluida or criada}
    d['collection_orders'] = [
        coleta(1, 1, 'coletada', '2026-10-02', 'manha', '~500 kg de latinha', 'interna', z('2026-09-30', '10:00'), z('2026-10-02', '09:40')),
        coleta(5, 5, 'coletada', '2026-10-23', 'tarde', '~700 kg de PET', 'interna', z('2026-10-21', '09:00'), z('2026-10-23', '15:40')),
        coleta(10, 10, 'agendada', '2026-11-13', 'tarde', 'PET prensado — 800 kg', 'portal', z('2026-11-10', '07:22'))]
    # as três fotos da compra de 06/11 (#1749) e o link público de fotos (token fixo)
    nomes = [('papelao', 'Carga de papelão'), ('pet', 'Carga de PET prensado'), ('latinha', 'Carga de latinha')]
    d['order_attachments'] = [{
        'id': f'@id:t20.foto.{k}', 'company_id': CO, 'order_id': '@id:compra.1749', 'order_kind': 'purchase', 'file_name': f't20-carga-{k}.jpg',
        'storage_path': f't20/t20-carga-{k}.jpg', 'mime': 'image/jpeg', 'file_size': 200000, 'created_by': MARCOS,
        'created_at': z('2026-11-06', f'10:{i}0')} for i, (k, _) in enumerate(nomes)]
    d['order_photo_shares'] = [{'id': '@id:t20.share.1749', 'company_id': CO, 'order_id': '@id:compra.1749', 'order_kind': 'purchase',
                                'token': '@id:t20.fotos.compra1749', 'created_at': z('2026-11-06', '10:30')}]
    return d


def patch_coop(**kv):
    return {'suppliers': [{'match': {'id': COOP}, 'set': kv}]}


def main():
    senha = os.environ.get('PORTAL_SENHA')
    if not senha:
        raise SystemExit('PORTAL_SENHA não definida (a senha do portal do cap04; só o hash vai para a semente)')
    os.makedirs(SAIDA, exist_ok=True)
    coop_id = stable_id('fornecedor.recomeco')
    hsh = hashlib.sha256(f'{coop_id}:{senha}'.encode()).hexdigest()
    ini = inicio()

    def salva(nome, dados):
        with open(os.path.join(SAIDA, nome + '.json'), 'w', encoding='utf8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=1)
        print(nome, {k: len(v) for k, v in dados.items() if isinstance(v, list)})

    salva('inicio', ini)
    c3 = {'_doc': 'T20 · depois do cap03: exibição do portal salva e comprovante em A4 (cumulativo sobre t20/inicio).',
          '_patch': patch_coop(portal_config=CFG_PORTAL, portal_receipt_format='a4')}
    salva('apos-cap03', c3)
    c4 = {'_doc': 'T20 · depois do cap04: o portal da cooperativa pede usuário e senha (cumulativo sobre t20/inicio).',
          '_patch': patch_coop(portal_config=CFG_PORTAL, portal_receipt_format='a4', portal_password_enabled=True, portal_username=SENHA_USUARIO,
                               portal_password_hash=hsh)}
    salva('apos-cap04', c4)
    pag = {'id': '@id:t20.bm.pix1350', 'company_id': CO, 'balance_id': BAL_COOP, 'entity_type': 'supplier', 'entity_id': COOP, 'movement_type': 'payment',
           'amount': -1350, 'description': 'Valor Pago a Cooperativa Recomeço · Acerto da entrega de 06/11', 'transaction_at': z('2026-11-10', '15:05'),
           'transaction_date': '2026-11-10', 'created_at': z('2026-11-10', '15:05'), 'created_by': RAFAEL, 'is_settled': False, 'payment_method': 'transfer'}
    c6 = {'_doc': 'T20 · depois do cap06: Pix de R$ 1.350,00 e saldo da cooperativa zerado (cumulativo sobre t20/inicio).',
          '_patch': {**c4['_patch'], 'balances': [{'match': {'id': BAL_COOP}, 'set': {'balance': 0, 'updated_at': z('2026-11-10', '15:05')}}]},
          'balance_movements': [pag]}
    salva('apos-cap06', c6)
    nova = {'id': '@id:t20.coleta.11', 'company_id': CO, 'numero': 11, 'status': 'solicitada', 'origem': 'portal', 'partner_type': 'supplier', 'partner_id': COOP,
            'partner_nome': 'Cooperativa Recomeço', 'contato_telefone': None, 'logradouro': 'Rua do Trabalho', 'numero_end': '57',
            'bairro': 'Vila Nossa Senhora das Graças', 'cidade': 'Taubaté', 'uf': 'SP', 'cep': '12060-640', 'scheduled_date': '2026-11-12', 'scheduled_window': 'manha',
            'driver_id': None, 'driver_name': None, 'vehicle_id': None, 'vehicle_plate': None, 'material_estimado': 'Papelão e PET prensados - 2.500 kg',
            'observacoes': 'Os fardos ficam na doca do galpão.', 'completed_at': None, 'public_short_code': 'q7mhx3kd9wrt', 'created_at': z('2026-11-10', '15:12'),
            'updated_at': z('2026-11-10', '15:12')}
    notif = [{'id': f'@id:t20.notif.{u[9:]}', 'user_id': u, 'company_id': CO, 'type': 'collection_request', 'title': 'Nova solicitação de coleta',
              'message': 'Cooperativa Recomeço solicitou uma coleta (#11).', 'action_url': '/coletas/ordens', 'icon': 'package',
              'expires_at': z('2026-11-17', '15:12'), 'created_at': z('2026-11-10', '15:12'), 'read_at': None} for u in (RAFAEL, JULIANA, MARCOS)]
    c8 = {'_doc': 'T20 · depois do cap08: coleta #11 solicitada pelo portal e o aviso para os três usuários (cumulativo sobre t20/inicio).',
          '_patch': c6['_patch'], 'balance_movements': [pag], 'collection_orders': [nova], 'user_notifications': notif}
    salva('apos-cap08', c8)


if __name__ == '__main__':
    main()
