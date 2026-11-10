#!/usr/bin/env python3
"""T03 · escreve as sementes extras da aula (rec/mundo/seeds-extra/t03/*.json), por cima do mundo base da Recicla Vale Metais.

Uso: python3 -I rec/t03/t03_sementes.py      (determinístico: rodar de novo dá os mesmos arquivos)

Cada capítulo abre num navegador novo com  seedExtra = ['t03/inicio', 't03/apos-capNN']  (gerar.py, SEMENTE): `inicio` desfaz no mundo
base o que a aula cria na tela e põe o cobre da semana passada; cada `apos-capNN` é CUMULATIVO sobre o `inicio` (tudo o que os capítulos
1..NN deixaram), escrito do que o robô faz na tela (os valores digitados) e no formato que o app grava (conferido no ensaio com
t03_estado.py). Horários de 10/11 entre 07:50 e 08:25 (antes do FAKE_NOW 08:30): a aula "aconteceu" no começo da manhã e as aulas
seguintes, que partem das 08:30, nunca veem registro no futuro.

- inicio: tira a "Tabela Depósitos" e os itens dela (o cap07 cria na tela) e o vínculo do Depósito Irmãos Siqueira com ela (o cap07
  liga); cobre R$ 0,50 abaixo (o cap06 reajusta); preço personalizado do bronze (R$ 30,50, fixo) do Depósito Irmãos Siqueira, lado
  fornecedor (o mundo base ainda não tem; fica para as próximas aulas); catálogo `ncm_presets` REAL (tabela pública do app, migração
  20260118193311: o seletor de NCM do cap04 mostra o que um cliente vê).
- marcos-sem-valores: SÓ no corte do Marcos (cap01b). O mundo dá ao Marcos "Ver Totais e Valores Financeiros" (o T2 mantém ligado) e o
  roteiro do T3 pede o Marcos sem ela (cadeado na tela Estoque): conflito para a junção (relatório e propostas_fala.md).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.normpath(os.path.join(HERE, '..', 'mundo', 'seeds-extra', 't03'))
CID = '@id:company.reciclavale'
RAFAEL = '@id:user.rafael'


def iso(hhmm, seg=0):
    """10/11/2026 hh:mm (Brasília) em UTC"""
    h, m = map(int, hhmm.split(':'))
    return f'2026-11-10T{h + 3:02d}:{m:02d}:{seg:02d}.000Z'


# ---------------------------------------------------------------- catálogo real de NCM (migração 20260118193311_94d9ca9d, app 1.59.154)
NCM = [
    ('7204.10.00', 'Sucata de Ferro Fundido - Alto teor de carbono (>2%), blocos de motores, bases de máquinas, tubulações, discos de freio', 'Ferro Fundido', 'II 0% / IPI 0% - PIS 2.1% COFINS 9.65% na importação'),
    ('7204.21.00', 'Sucata de Aço Inoxidável - Ligas 304/316 com níquel e cromo, alta resistência à corrosão', 'Aço Inoxidável', 'II 0% / IPI 0% - Alto valor agregado'),
    ('7204.29.00', 'Sucata de Outras Ligas de Aço - Aços ferramenta, aços especiais, ligas com molibdênio', 'Aço Ligado', 'II 0% / IPI 0% - Diferimento em operações internas'),
    ('7204.30.00', 'Sucata de Ferro ou Aço Estanhado - Folha de flandres, latas de alimentos, requer desestanhamento', 'Ferro/Aço Estanhado', 'II 0% / IPI 0% - Segregação obrigatória'),
    ('7204.41.00', 'Resíduos de Usinagem - Cavacos, aparas, lascas, limalhas, pó de serra, resíduos de estampagem (mesmo em fardos)', 'Ferro/Aço', 'II 0% / IPI 0% - Subprodutos industriais'),
    ('7204.49.00', 'Sucata Mista de Ferro/Aço - HMS 1&2, sucata triturada (shredded), vigas estruturais, chapas, obsolescência geral', 'Ferro/Aço', 'II 0% / IPI 0% - Código mais utilizado em volume'),
    ('7404.00.00', 'Sucata de Cobre - Fios, cabos, tubos, chapas, componentes elétricos', 'Cobre', 'II 0% / IPI 0% - Alto valor, fiscalização intensa'),
    ('7503.00.00', 'Sucata de Níquel - Ligas de níquel puro, essencial para aço inox e superligas aeroespaciais', 'Níquel', 'II 0% / IPI 0% - Material estratégico'),
    ('7602.00.00', 'Sucata de Alumínio - Latas de bebida, perfis, panelas, chapas, peças fundidas', 'Alumínio', 'II 0% / IPI 0% - Pode ter ST dependendo do estado'),
    ('7802.00.00', 'Sucata de Chumbo - Baterias automotivas (LABs), chapas, tubos. Material tóxico controlado por Basileia', 'Chumbo', 'II 3.6% - Controle rigoroso ambiental (IBAMA)'),
    ('7902.00.00', 'Sucata de Zinco - Peças fundidas (zamak), chapas galvanizadas, anodos', 'Zinco', 'II 0% / IPI 0% - Diferimento comum'),
    ('8002.00.00', 'Sucata de Estanho - Soldas eletrônicas, borras de estanhagem, ligas de bronze', 'Estanho', 'II 0% ou NT - Diferimento comum'),
    ('3915.10.00', 'Resíduos de Polietileno (PE) - PEAD (frascos), PEBD (filmes agrícolas, sacolas)', 'Plástico - PE', 'Segregação por tipo de polímero obrigatória'),
    ('3915.20.00', 'Resíduos de Poliestireno (PS) - Isopor, copos descartáveis, embalagens rígidas', 'Plástico - PS', 'Segregação por tipo de polímero obrigatória'),
    ('3915.30.00', 'Resíduos de PVC - Tubos, esquadrias, pisos vinílicos, mangueiras', 'Plástico - PVC', 'Segregação por tipo de polímero obrigatória'),
    ('3915.90.00', 'Outros Plásticos (incl. PET) - Garrafas PET, ABS (carcaças), Policarbonato (PC), Nylon', 'Plástico - Outros', 'II ~18% - Inclui PET que não tem código específico'),
    ('4707.10.00', 'Papel Kraft e Papelão Ondulado (OCC) - Caixas de papelão, embalagens kraft, fibras longas não branqueadas', 'Papel/Papelão', 'II 0% / IPI 0% - Base da indústria de embalagens'),
    ('4707.20.00', 'Papel Branco/Químico - Aparas de escritório (SOP), papel de impressora, arquivos brancos', 'Papel Branco', 'II 0% / IPI 0% - Valorizado pela brancura'),
    ('4707.30.00', 'Papel de Pasta Mecânica - Jornais (ONP), revistas, periódicos. Contém lignina, amarela com tempo', 'Papel Jornal/Revista', 'II 0% / IPI 0% - Commodity em declínio'),
    ('4707.90.00', 'Papéis Mistos/Não Selecionados - Resíduos não triados, papel misto contaminado', 'Papel Misto', 'II ~18% - Maior fiscalização, controle fitossanitário'),
    ('7001.00.00', 'Cacos e Fragmentos de Vidro - Vidro quebrado irregular, arestas cortantes. Se processado em pó vai p/ Cap. 32', 'Vidro', 'II 0% / IPI 0% - Distinção importante: caco vs pó'),
    ('6310.10.00', 'Trapos Têxteis Escolhidos - Material têxtil triado, selecionado por tipo de fibra', 'Têxtil', 'Triagem agrega valor'),
    ('6310.90.00', 'Trapos Têxteis Mistos - Cordéis, cordas, cabos, desperdícios não selecionados, desfibrados', 'Têxtil', 'Benefícios de ICMS em estados têxteis (SC)'),
    ('4004.00.00', 'Resíduos de Borracha - Borracha triturada, raspas de recauchutagem, pós e grânulos', 'Borracha', 'Matéria-prima para asfalto e pisos'),
    ('4012.20.00', 'Pneus Usados - Pneumáticos usados para recauchutagem ou reciclagem', 'Pneus', 'IMPORTAÇÃO GERALMENTE PROIBIDA (IBAMA/DECEX)'),
    ('8549.11.00', 'Baterias Chumbo-Ácido Usadas - Baterias automotivas e industriais, material tóxico', 'E-Waste - Baterias', 'II 16.2% - Controle ambiental rigoroso'),
    ('8549.12.00', 'Baterias de Níquel-Cádmio Usadas - Pilhas recarregáveis antigas', 'E-Waste - Baterias', 'II 16.2% - Material tóxico (cádmio)'),
    ('8549.13.00', 'Baterias de Lítio Usadas - Baterias de celulares, notebooks, veículos elétricos', 'E-Waste - Baterias', 'II 16.2% - Risco de incêndio, minerais críticos'),
    ('8549.19.00', 'Outras Baterias e Pilhas Usadas - Pilhas alcalinas, baterias diversas', 'E-Waste - Baterias', 'II 16.2%'),
    ('8549.21.00', 'E-Waste Rico em Metais Preciosos (Perigoso) - Contém Hg, Cd, Pb, vidro CRT, requer descontaminação', 'E-Waste - Metais Preciosos', 'NT ou Isento (Ex-tarifário) - Controle IBAMA/Basileia'),
    ('8549.29.00', 'E-Waste Rico em Metais Preciosos (Limpo) - Placas de circuito limpas, memórias, conectores dourados', 'E-Waste - Metais Preciosos', 'II 16.2% - "Mina urbana" para Au, Ag, Pd, Pt'),
    ('8549.31.00', 'Componentes Eletrônicos Perigosos - Contém pilhas, interruptores de mercúrio, vidro CRT', 'E-Waste - Perigoso', 'II 16.2% - Catch-all para e-waste tóxico'),
    ('8549.39.00', 'Placas e Montagens Eletrônicas (Limpas) - PCBs padrão, componentes sem contaminantes', 'E-Waste - Eletrônicos', 'II 16.2% - Sucata eletrônica padrão'),
    ('8549.91.00', 'Outros Resíduos Eletrônicos Perigosos - Equipamentos com substâncias controladas', 'E-Waste - Outros', 'II 16.2% - Controle ambiental'),
    ('8549.99.00', 'Outros Resíduos Eletrônicos - Equipamentos diversos sem classificação específica', 'E-Waste - Outros', 'II 16.2%'),
    ('7112.91.00', 'Resíduos de Ouro - Restos de joalheria, raspas, limalhas de ouro', 'Metais Preciosos', 'II 5.4% - Alto valor'),
    ('7112.92.00', 'Resíduos de Platina - Inclui paládio e ródio, catalisadores automotivos exauridos', 'Metais Preciosos', 'II 5.4% - Catalisadores têm alto teor'),
    ('7112.99.00', 'Outros Resíduos de Metais Preciosos - Catalisadores com PGMs, resíduos de refinaria', 'Metais Preciosos', 'II 5.4% - Inclui catalisadores automotivos'),
]

# ---------------------------------------------------------------- preços (compra, venda)
COBRE_ANTES = {'cobre_mel': (42.0, 47.4), 'cobre_misto': (35.5, 41.0), 'fio_cobre': (17.5, 21.5)}   # semana passada (inicio..cap05)
COBRE_MUNDO = {'cobre_mel': (42.5, 47.9), 'cobre_misto': (36.0, 41.5), 'fio_cobre': (18.0, 22.0)}   # depois do cap06 (= MUNDO_FICTICIO)


def precos_cobre(tabela):
    out = {'materials': [], 'price_table_items': []}
    for k, (c, v) in tabela.items():
        out['materials'].append({'match': {'id': f'@id:material.{k}'}, 'set': {'purchase_price': c, 'sale_price': v}})
        out['price_table_items'].append({'match': {'id': f'@id:pti.padrao.{k}'}, 'set': {'purchase_price': c, 'sale_price': v}})
    return out


def inicio():
    p = precos_cobre(COBRE_ANTES)
    return {
        '_doc': 'T03 · estado de partida da aula (caps. 0 a 2) sobre o mundo base: sem a "Tabela Depósitos" (o cap07 cria) e sem o vínculo do '
                'Depósito Irmãos Siqueira com ela; cobre da semana passada (R$ 0,50 abaixo; o cap06 reajusta); preço personalizado do bronze '
                '(R$ 30,50) do Depósito Irmãos Siqueira, lado fornecedor; catálogo real de NCM (ncm_presets). Gerado por rec/t03/t03_sementes.py.',
        '_remove': {
            'price_tables': [{'id': '@id:tabela.depositos'}],
            'price_table_items': [{'price_table_id': '@id:tabela.depositos'}],
        },
        '_patch': {
            'suppliers': [{'match': {'id': '@id:fornecedor.siqueira'}, 'set': {'default_price_table_id': None}}],
            'customers': [{'match': {'id': '@id:cliente.siqueira'}, 'set': {'default_price_table_id': None}}],
            'materials': p['materials'],
            'price_table_items': p['price_table_items'],
        },
        'entity_custom_prices': [{
            'id': '@id:ecp.siqueira.bronze', 'company_id': CID, 'entity_type': 'supplier', 'entity_id': '@id:fornecedor.siqueira',
            'material_id': '@id:material.bronze', 'custom_price': 30.5, 'is_linked': False, 'is_override': False, 'price_table_id': None,
            'variation_type': None, 'variation_amount': None, 'variation_direction': None, 'created_by': RAFAEL,
            'created_at': '2026-10-05T13:20:00.000Z', 'updated_at': '2026-10-05T13:20:00.000Z',
        }],
        'ncm_presets': [{'id': f'@id:ncm.{n}', 'ncm': n, 'description': d, 'material_category': c, 'tax_notes': t, 'created_at': '2026-01-18T19:33:11.000Z'}
                        for n, d, c, t in NCM],
    }


# ---------------------------------------------------------------- o que a aula cria (cumulativo)
def radiador(cap):
    r = {'id': '@id:material.radiador', 'company_id': CID, 'code': '16' if cap < 3 else '70', 'code_prefix': None, 'name': 'Radiador de cobre',
         'fiscal_name': None, 'group_id': '@id:grupo.radiadores' if cap >= 5 else None, 'unit': 'Kg', 'ncm': '74040000' if cap >= 4 else None,
         'purchase_price': 21.0, 'sale_price': 24.5, 'purchase_price_currency': 'BRL', 'sale_price_currency': 'BRL',
         'current_stock': 110.0 if cap >= 8 else 120.0, 'pieces_per_commercial_unit': None, 'is_archived': False, 'archived_at': None,
         'created_by': None, 'created_at': iso('07:52'), 'updated_at': iso({2: '07:52', 3: '07:56', 4: '08:00', 5: '08:04'}.get(cap, '08:04') if cap < 8 else '08:21')}
    return r


def movimentos(cap):
    """stock_movements que a aula deixa: o SALDO_INICIAL do cadastro (trigger trg_material_saldo_inicial do banco) e, no cap08, a saída de
    2 kg e a transferência de 8 kg (formato das RPCs adjust_material_stock_atomic e transfer_material_stock)."""
    mv = [{'id': '@id:mov.t03.radiador.inicial', 'company_id': CID, 'material_id': '@id:material.radiador', 'type': 'SALDO_INICIAL', 'quantity': 120,
           'stock_before': 0, 'stock_after': 120, 'description': 'Saldo inicial do cadastro do material', 'created_by': None,
           'created_at': iso('07:52'), 'transaction_at': iso('07:52'), 'transaction_date': '2026-11-10'}]
    if cap >= 8:
        mv += [
            {'id': '@id:mov.t03.radiador.saida', 'company_id': CID, 'material_id': '@id:material.radiador', 'type': 'EDICAO_MANUAL', 'quantity': -2,
             'stock_before': 120, 'stock_after': 118, 'description': 'Ajuste de inventário', 'created_by': RAFAEL, 'client_request_id': '@id:cri.t03.saida',
             'created_at': iso('08:20'), 'transaction_at': iso('08:20'), 'transaction_date': '2026-11-10'},
            {'id': '@id:mov.t03.radiador.transf', 'company_id': CID, 'material_id': '@id:material.radiador', 'type': 'TRANSFERENCIA', 'quantity': -8,
             'stock_before': 118, 'stock_after': 110, 'description': 'Transferência para Ferro misto', 'created_by': RAFAEL, 'client_request_id': '@id:cri.t03.transf',
             'created_at': iso('08:21'), 'transaction_at': iso('08:21'), 'transaction_date': '2026-11-10'},
            {'id': '@id:mov.t03.ferromisto.transf', 'company_id': CID, 'material_id': '@id:material.ferro_misto', 'type': 'TRANSFERENCIA', 'quantity': 8,
             'stock_before': 6420, 'stock_after': 6428, 'description': 'Transferência de Radiador de cobre', 'created_by': RAFAEL,
             'related_movement_id': '@id:mov.t03.radiador.transf', 'created_at': iso('08:21'), 'transaction_at': iso('08:21'), 'transaction_date': '2026-11-10'},
        ]
    return mv


def apos(cap):
    d = {'_doc': f'T03 · estado depois do cap{cap:02d} (cumulativo sobre t03/inicio). Gerado por rec/t03/t03_sementes.py.',
         'materials': [radiador(cap)], 'stock_movements': movimentos(cap), 'price_table_items': [], '_patch': {}}
    if cap >= 3:   # o "Atualizar" com a principal selecionada grava o item da principal (Materiais.tsx:1022-1046)
        d['price_table_items'].append({'id': '@id:pti.padrao.radiador', 'price_table_id': '@id:tabela.padrao', 'material_id': '@id:material.radiador',
                                       'purchase_price': 21.0, 'sale_price': 24.5, 'is_override': False, 'created_at': iso('07:56'), 'updated_at': iso('08:04')})
    if cap >= 5:
        d['material_groups'] = [{'id': '@id:grupo.radiadores', 'company_id': CID, 'name': 'Radiadores', 'color': '#0F766E', 'icon': 'car',
                                 'created_at': iso('08:03'), 'updated_at': iso('08:03')}]
    if cap >= 6:
        p = precos_cobre(COBRE_MUNDO)
        d['_patch']['materials'] = p['materials']
        d['_patch']['price_table_items'] = p['price_table_items']
    if cap >= 7:
        d['price_tables'] = [{'id': '@id:tabela.depositos', 'company_id': CID, 'name': 'Tabela Depósitos', 'is_default': False, 'is_linked': True,
                              'linked_to_table_id': '@id:tabela.padrao', 'variation_type': 'percentage', 'variation_amount': 4, 'variation_direction': 'positive',
                              'created_at': iso('08:10'), 'updated_at': iso('08:10')}]
        d['_patch']['suppliers'] = [{'match': {'id': '@id:fornecedor.siqueira'}, 'set': {'default_price_table_id': '@id:tabela.depositos'}}]
        d['_patch']['customers'] = [{'match': {'id': '@id:cliente.siqueira'}, 'set': {'default_price_table_id': '@id:tabela.depositos'}}]
    if cap >= 8:
        d['_patch'].setdefault('materials', []).append({'match': {'id': '@id:material.ferro_misto'}, 'set': {'current_stock': 6428}})
    if not d['_patch']:
        del d['_patch']
    return d


def marcos_sem_valores():
    return {'_doc': 'T03 · só no corte do Marcos (cap01b): Marcos Antunes sem "Ver Totais e Valores Financeiros" (action_view_financial_values), '
                    'para a tela Estoque mostrar o cadeado. CONFLITO com o mundo (o T2 deixa a permissão ligada): decidir na junção.',
            '_remove': {'user_permissions': [{'user_id': '@id:user.marcos', 'permission': 'action_view_financial_values'}]}}


def main():
    os.makedirs(SAIDA, exist_ok=True)
    arquivos = {'inicio': inicio(), 'marcos-sem-valores': marcos_sem_valores()}
    for cap in (2, 3, 4, 5, 6, 7, 8):
        arquivos[f'apos-cap{cap:02d}'] = apos(cap)
    for nome, d in arquivos.items():
        with open(os.path.join(SAIDA, nome + '.json'), 'w', encoding='utf8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write('\n')
    print(f'{len(arquivos)} sementes em {os.path.relpath(SAIDA, os.path.join(HERE, "..", ".."))}: ' + ', '.join(sorted(arquivos)))


if __name__ == '__main__':
    main()
