#!/usr/bin/env python3
"""T18 · gera o mundo de partida da aula: rec/fakebase/seeds-extra/t18/{catalogo,fim-t7-provisorio}.json e rec/t18/cadeia.json.

Estado de partida = FIM DO T7. A cadeia é a do T7 (t3, t1, t4, t5, t7/inicio) mais:
  - o ÚLTIMO t7/apos-capNN que existir (o que o T7 de fato deixou); enquanto o T7 não gravou, `t18/fim-t7-provisorio`, que
    reproduz o "Estado final" do T07/roteiro.md (OS #16 Concluída, saldos 10 un e 28 rolos, avaliação 10);
  - `t18/catalogo`: o catálogo GLOBAL fictício da Área do Técnico (bastidor, sem logos): 4 marcas inventadas, modelos de ar
    condicionado, compressores com ficha, linha branca, controles remotos, códigos de erro e 8 fluidos refrigerantes.
O T18 não cria nem altera dado da empresa (só cálculo e consulta): não há `t18/apos-capNN`. O catálogo é global e o T8 não precisa dele.

A OS "Em Andamento" do cap. 3 é a #9 da Júlia Santos (Clínica Sorriso Leve, check-in feito), que o T5 já semeia: nada a criar.

Uso:  python3 -I rec/t18/semear.py              (gera os JSON e rec/t18/cadeia.json)
      python3 -I rec/t18/semear.py --verificar  (confere o catálogo: busca "E1", ordem das marcas, ids, textos)
Rodar de novo quando o T7 terminar (ele passa a valer no lugar do provisório) e conferir que o resumo bate.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ilustracoes as ilu  # noqa: E402

EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
CHAIN_T7 = ['t3/apos-cap10', 't1/apos-cap13', 't4/inicio', 't4/apos-cap14', 't5/inicio']


def exists(rel):
    return os.path.exists(os.path.join(EXTRA, rel + '.json'))


def load(rel):
    with open(os.path.join(EXTRA, rel + '.json'), encoding='utf8') as f:
        return json.load(f)


def ultimo(prefixo, ate=40):
    for n in range(ate, 0, -1):
        rel = f'{prefixo}/apos-cap{n:02d}'
        if exists(rel):
            return rel
    return None


# ================================================================ catálogo global fictício
MARCAS = [  # chave, nome, sort, cor do desenho
    ('aerovento', 'Aerovento', 1, '#2563eb'),
    ('cristalar', 'Cristalar', 2, '#0d9488'),
    ('brisamar', 'Brisamar', 3, '#ea580c'),
    ('nortec', 'Nortec', 4, '#64748b'),
]
COR = {k: c for k, _, _, c in MARCAS}

CATEGORIAS = [  # chave, nome, domínio
    ('hiwall', 'Split Hi-Wall', 'ar_condicionado'),
    ('cassete', 'Split Cassete', 'ar_condicionado'),
    ('pisoteto', 'Split Piso-Teto', 'ar_condicionado'),
    ('rotativo', 'Rotativo', 'compressor'),
    ('geladeira', 'Geladeira', 'linha_branca'),
    ('freezer', 'Freezer', 'linha_branca'),
]

# Ar condicionado: marca, chave, categoria, nome, código, gás, kWh/mês (a 8 h/dia), potência W, códigos de erro
AC = [
    ('aerovento', 'av-hw09', 'hiwall', 'Hi-Wall 9.000 BTUs', 'AV-HW09', 'R-410A', 150, 850, ['E1', 'E2', 'E4', 'F1', 'P4']),
    ('aerovento', 'av-hw12', 'hiwall', 'Hi-Wall 12.000 BTUs', 'AV-HW12', 'R-410A', 200, 1100, ['E1', 'E2', 'E3', 'E4', 'F0', 'F1', 'P4']),
    ('aerovento', 'av-hw18', 'hiwall', 'Hi-Wall 18.000 BTUs', 'AV-HW18', 'R-410A', 300, 1700, ['E1', 'E2', 'E3', 'E4', 'E5', 'F0', 'F1', 'H6', 'P4', 'P5']),
    ('aerovento', 'av-cs36', 'cassete', 'Cassete 36.000 BTUs', 'AV-CS36', 'R-410A', 580, 3300, ['E1', 'E2', 'E4', 'E5', 'F0', 'P4']),
    ('aerovento', 'av-pt48', 'pisoteto', 'Piso-Teto 48.000 BTUs', 'AV-PT48', 'R-410A', 780, 4400, ['E3', 'E4', 'F0', 'P5']),
    ('cristalar', 'cr-hw12', 'hiwall', 'Hi-Wall 12.000 BTUs', 'CR-HW12', 'R-32', 190, 1050, ['E2', 'E4', 'F1', 'P1']),
    ('cristalar', 'cr-hw18', 'hiwall', 'Hi-Wall 18.000 BTUs', 'CR-HW18', 'R-32', 290, 1650, ['E1', 'E2', 'E3', 'E4', 'E6', 'F0', 'F2', 'P3']),
    ('cristalar', 'cr-cs36', 'cassete', 'Cassete 36.000 BTUs', 'CR-CS36', 'R-32', 560, 3200, ['E2', 'E4', 'H6', 'P4']),
    ('brisamar', 'bm-hw09', 'hiwall', 'Hi-Wall 9.000 BTUs', 'BM-HW09', 'R-410A', 155, 870, ['E2', 'E4', 'F1']),
    ('brisamar', 'bm-hw18', 'hiwall', 'Hi-Wall 18.000 BTUs', 'BM-HW18', 'R-410A', 310, 1750, ['E4', 'E5', 'P4']),
    ('brisamar', 'bm-pt48', 'pisoteto', 'Piso-Teto 48.000 BTUs', 'BM-PT48', 'R-410A', 800, 4500, ['E4', 'F0', 'P3']),
]
# Compressores: marca, chave, nome, código, gás, ficha
COMPRESSORES = [
    ('nortec', 'nr-rt12', 'Compressor Rotativo 12.000 BTUs', 'NR-RT12', 'R-410A',
     dict(hp='1,33', capacidade_btu='12.000', aplicacao='Ar-condicionado split Hi-Wall', tensao='220 V', frequencia='60 Hz',
          deslocamento_cm3='17,0 cm³', capacitor_trabalho='25 µF / 440 V', capacitor_partida='Não utiliza (capacitor permanente)',
          rele_protetor='Protetor térmico interno', oleo='POE, viscosidade ISO 32', conexoes='Sucção 3/8 pol · Descarga 1/4 pol',
          equivalencias='NR-RT12B (versão anterior) · CR-RT12 (pinagem compatível)', observacoes='Confirme os valores na etiqueta do compressor antes da troca.')),
    ('nortec', 'nr-rt18', 'Compressor Rotativo 18.000 BTUs', 'NR-RT18', 'R-410A',
     dict(hp='2', capacidade_btu='18.000', aplicacao='Ar-condicionado split Hi-Wall', tensao='220 V', frequencia='60 Hz',
          deslocamento_cm3='24,5 cm³', capacitor_trabalho='40 µF / 440 V', capacitor_partida='Não utiliza (capacitor permanente)',
          rele_protetor='Protetor térmico interno', oleo='POE, viscosidade ISO 32', conexoes='Sucção 1/2 pol · Descarga 5/16 pol',
          equivalencias='NR-RT18B (versão anterior) · CR-RT18 (pinagem compatível)', observacoes='Confirme os valores na etiqueta do compressor antes da troca.')),
    ('cristalar', 'cr-rt24', 'Compressor Rotativo 24.000 BTUs', 'CR-RT24', 'R-32',
     dict(hp='2,67', capacidade_btu='24.000', aplicacao='Ar-condicionado split', tensao='220 V', frequencia='60 Hz',
          deslocamento_cm3='33,0 cm³', capacitor_trabalho='55 µF / 440 V', capacitor_partida='Não utiliza (capacitor permanente)',
          rele_protetor='Protetor térmico interno', oleo='POE, viscosidade ISO 46', conexoes='Sucção 5/8 pol · Descarga 3/8 pol',
          equivalencias='NR-RT24 (pinagem compatível)', observacoes='Confirme os valores na etiqueta do compressor antes da troca.')),
]
# Linha branca: marca, chave, categoria, nome, código, kWh/mês (24 h/dia), potência W, códigos
LINHA_BRANCA = [
    ('brisamar', 'bm-gf380', 'geladeira', 'Geladeira Frost Free 380 L', 'BM-GF380', 42, 140, ['E2', 'E3', 'F4', 'F5']),
    ('brisamar', 'bm-fv230', 'freezer', 'Freezer Vertical 230 L', 'BM-FV230', 38, 120, ['E2', 'F4', 'F5']),
    ('cristalar', 'cr-gd310', 'geladeira', 'Geladeira Duplex 310 L', 'CR-GD310', 36, 125, ['E2', 'E3', 'F4']),
]
# Controles remotos: marca, chave, nome, código
CONTROLES = [
    ('aerovento', 'av-rc01', 'Controle Remoto Hi-Wall', 'AV-RC01'),
    ('cristalar', 'cr-rc02', 'Controle Remoto Cassete', 'CR-RC02'),
]

# Códigos de erro (genéricos e fictícios). ATENÇÃO à busca "E1" da aula: o app procura no código, no título E na descrição, sem
# espaços; por isso NENHUM texto de código usa o dígito 1 nem "e" colado em "1" (senão "E1" traria outros códigos).
COD = {
    'E1': ('Sensor de temperatura ambiente',
           'O aparelho não consegue ler a temperatura do ar que entra na unidade interna.',
           'Confira o conector do sensor na placa da unidade interna. Meça a resistência do sensor com o multímetro e compare com a tabela do fabricante. Verifique se o cabo do sensor está rompido ou encostando na serpentina.',
           'Reencaixe o conector e prenda o cabo longe de partes quentes. Substitua o sensor se a resistência estiver fora da tabela.',
           'Sensor de temperatura ambiente (termistor)'),
    'E2': ('Sensor da serpentina interna',
           'A leitura da temperatura da serpentina da evaporadora está fora do esperado.',
           'Inspecione o sensor preso na serpentina da evaporadora. Meça a resistência do sensor à temperatura ambiente. Procure oxidação no conector da placa.',
           'Fixe o sensor no tubo da serpentina com a presilha original. Troque o sensor se a medida não bater com a tabela.',
           'Sensor da serpentina (termistor)'),
    'E3': ('Ventilador da unidade interna',
           'O motor do ventilador da evaporadora não atinge a rotação esperada.',
           'Gire a turbina com a mão e veja se está livre. Confira o capacitor do motor e o conector do sinal de rotação. Meça a tensão de alimentação do motor.',
           'Limpe a turbina e lubrifique os mancais, se houver. Troque o capacitor ou o motor conforme o resultado das medições.',
           'Motor do ventilador da evaporadora'),
    'E4': ('Comunicação entre as unidades',
           'A placa da unidade interna não recebe resposta da unidade externa.',
           'Confira o cabo de interligação e os bornes nas duas unidades. Verifique a tensão entre os bornes de comunicação. Confirme se a ordem das fases e do neutro está igual nas duas pontas.',
           'Refaça as conexões e substitua o cabo de interligação se houver emenda ou dano. Troque a placa da unidade externa se o sinal continuar ausente.',
           'Cabo de interligação e placas eletrônicas'),
    'E5': ('Sobrecorrente no compressor',
           'A proteção desligou o compressor por corrente acima do limite.',
           'Meça a corrente do compressor com o alicate amperímetro. Verifique o capacitor de trabalho e a circulação de ar na unidade externa. Confira se a tensão de alimentação está estável.',
           'Limpe a condensadora e troque o capacitor se estiver abaixo do valor de placa. Corrija a alimentação elétrica antes de religar.',
           'Compressor e capacitor de trabalho'),
    'E6': ('Ventilador da unidade externa',
           'O motor do ventilador da condensadora está travado ou sem sinal.',
           'Gire a hélice com a mão e veja se está livre. Meça o capacitor do ventilador. Confira o conector do motor na placa externa.',
           'Desobstrua a hélice e troque o capacitor ou o motor. Revise o conector e fixe bem os cabos.',
           'Motor do ventilador da condensadora'),
    'F0': ('Baixa carga de gás',
           'A pressão de sucção está abaixo do esperado para a operação.',
           'Meça as pressões de baixa e de alta com o manifold. Calcule o superaquecimento e compare com a faixa do fabricante. Procure vazamentos nas conexões com detector ou espuma.',
           'Corrija o vazamento, faça vácuo e recarregue pelo peso indicado na placa. Confirme o superaquecimento depois da carga.',
           'Circuito frigorífico (conexões e tubulação)'),
    'F1': ('Sensor de temperatura externa',
           'A placa da unidade externa não lê a temperatura do ar externo.',
           'Verifique o conector do sensor na placa externa. Meça a resistência do sensor e compare com a tabela. Procure cabo danificado perto da serpentina.',
           'Reencaixe ou troque o sensor. Proteja o cabo com fita e prenda longe de bordas.',
           'Sensor de temperatura externa (termistor)'),
    'F2': ('Sensor da serpentina externa',
           'A leitura da serpentina da condensadora está fora da faixa.',
           'Inspecione a fixação do sensor no tubo da condensadora. Meça a resistência do sensor. Verifique oxidação no conector.',
           'Fixe o sensor no ponto indicado pelo fabricante. Troque o sensor se a medida estiver fora da tabela.',
           'Sensor da serpentina externa (termistor)'),
    'H6': ('Sem retorno do compressor',
           'A placa não detecta o funcionamento do compressor.',
           'Meça a tensão de saída da placa para o compressor. Verifique o contator ou o relé de partida. Confira a continuidade dos enrolamentos do compressor.',
           'Troque o relé ou o contator danificado. Substitua o compressor apenas se os enrolamentos estiverem abertos ou em curto.',
           'Compressor e relé de partida'),
    'P1': ('Proteção de tensão',
           'A tensão de alimentação ficou fora da faixa permitida.',
           'Meça a tensão no quadro e na entrada do aparelho. Verifique conexões soltas e a bitola do cabo. Anote as variações durante a partida do compressor.',
           'Reaperte as conexões e corrija o cabo se estiver subdimensionado. Oriente o cliente sobre estabilizador ou ajuste na rede.',
           'Alimentação elétrica e quadro'),
    'P3': ('Temperatura de descarga alta',
           'O compressor desligou por superaquecimento na descarga.',
           'Confira a limpeza da condensadora e o fluxo de ar. Meça pressões e superaquecimento. Veja se há restrição na linha de líquido.',
           'Limpe a serpentina e desobstrua a linha. Ajuste a carga de gás conforme o peso de placa.',
           'Condensadora e circuito frigorífico'),
    'P4': ('Módulo inversor',
           'O módulo que aciona o compressor detectou falha de corrente ou de tensão.',
           'Aguarde cinco minutos com o aparelho desligado e religue. Meça a tensão do barramento DC com cuidado. Inspecione o módulo e as trilhas por sinais de queima.',
           'Troque o módulo inversor ou a placa externa completa. Teste o compressor antes de religar.',
           'Módulo inversor da unidade externa'),
    'P5': ('Alta pressão',
           'A pressão de alta passou do limite de proteção.',
           'Verifique o ventilador e a limpeza da condensadora. Meça a pressão de alta e o subresfriamento. Procure excesso de gás ou ar no sistema.',
           'Limpe a condensadora e corrija a carga de gás. Refaça o vácuo se houver ar no circuito.',
           'Condensadora e carga de gás'),
    # linha branca
    'F4': ('Ventilador do evaporador',
           'O ventilador que circula o ar frio no gabinete não está girando.',
           'Abra o compartimento do evaporador e gire a hélice com a mão. Meça a tensão no conector do motor. Procure gelo travando a hélice.',
           'Remova o gelo e confira a resistência de degelo. Troque o motor se estiver sem rotação.',
           'Motor do ventilador do evaporador'),
    'F5': ('Compressor sem partida',
           'O compressor tenta partir e desarma pela proteção.',
           'Meça a corrente no instante da partida. Verifique o relé de partida e o protetor térmico. Confira a continuidade dos enrolamentos.',
           'Troque o relé ou o protetor danificado. Substitua o compressor se os enrolamentos estiverem abertos.',
           'Relé de partida e protetor térmico'),
}
COD_LB_TITULOS = {  # a linha branca reaproveita E2/E3 com outros nomes de peça
    'E2': ('Sensor do compartimento',
           'A leitura de temperatura do compartimento de refrigeração está fora do esperado.',
           'Inspecione o sensor no interior do gabinete. Meça a resistência do sensor à temperatura ambiente. Procure umidade no conector.',
           'Seque e reencaixe o conector. Troque o sensor se a medida não bater com a tabela.',
           'Sensor de temperatura do compartimento'),
    'E3': ('Sensor de degelo',
           'O sensor do evaporador não informa a temperatura para o ciclo de degelo.',
           'Localize o sensor preso ao evaporador. Meça a resistência do sensor. Verifique o conector na placa.',
           'Fixe o sensor no ponto original. Troque o sensor se estiver fora da tabela.',
           'Sensor de degelo (termistor)'),
}

GASES = [  # code, nome, tipo, classe, cor, composição, gwp, odp, ebulição, glide, óleo, substitui, aplicação, observações
    ('R-410A', 'Mistura R-32/R-125', 'HFC · blend quase azeotrópico', 'A1', '#f472b6', 'R-32 (50%) / R-125 (50%)', 2088, 0, -51.6, 0.1,
     'POE', 'R-22', 'Ar-condicionado split e sistemas comerciais', 'Opera com pressões mais altas que o R-22: use manifold e mangueiras próprios para a pressão.'),
    ('R-32', 'Difluorometano', 'HFC · puro', 'A2L', '#38bdf8', 'R-32 (100%)', 675, 0, -51.7, 0,
     'POE', 'R-410A', 'Ar-condicionado split de nova geração', 'Levemente inflamável (A2L): evite chamas e fontes de ignição e siga as normas de instalação.'),
    ('R-22', 'Clorodifluormetano', 'HCFC · puro', 'A1', '#86efac', 'R-22 (100%)', 1810, 0.055, -40.8, 0,
     'Mineral ou alquilbenzeno', None, 'Equipamentos antigos, em eliminação', 'Em eliminação gradual pelo Protocolo de Montreal.'),
    ('R-134a', 'Tetrafluoretano', 'HFC · puro', 'A1', '#60a5fa', 'R-134a (100%)', 1430, 0, -26.1, 0,
     'POE', 'R-12', 'Refrigeração doméstica e ar-condicionado automotivo', None),
    ('R-404A', 'Mistura R-125/R-143a/R-134a', 'HFC · blend zeotrópico', 'A1', '#fb923c', 'R-125 (44%) / R-143a (52%) / R-134a (4%)', 3922, 0, -46.5, 0.5,
     'POE', 'R-502', 'Refrigeração comercial de baixa e média temperatura', 'Mistura com glide pequeno: carregue pela fase líquida.'),
    ('R-290', 'Propano', 'HC · natural', 'A3', '#ef4444', 'R-290 (100%)', 3, 0, -42.1, 0,
     'Mineral ou POE', 'R-22 e R-134a em sistemas novos', 'Refrigeração doméstica e comercial de pequena carga', 'Altamente inflamável (A3): carga limitada e ventilação obrigatória.'),
    ('R-407C', 'Mistura R-32/R-125/R-134a', 'HFC · blend zeotrópico', 'A1', '#b08968', 'R-32 (23%) / R-125 (25%) / R-134a (52%)', 1774, 0, -43.6, 5.5,
     'POE', 'R-22', 'Ar-condicionado e chillers', 'Mistura com glide: carregue pela fase líquida.'),
    ('R-448A', 'Mistura R-32/R-125/R-1234yf/R-134a/R-1234ze', 'HFC/HFO · blend zeotrópico', 'A1', '#94a3b8', 'R-32 (26%) / R-125 (26%) / R-1234yf (20%) / R-134a (21%) / R-1234ze (7%)',
     1387, 0, -45.9, 6.0, 'POE', 'R-404A', 'Refrigeração comercial (retrofit de R-404A)', 'Mistura com glide: carregue pela fase líquida.'),
]

CONTROLE_CFG = {
    'av-rc01': dict(
        instrucoes='Para parear e ajustar o controle:\n\n- Coloque duas pilhas AAA novas, respeitando a polaridade.\n- Aponte o controle para a unidade interna, a até cinco metros.\n- Pressione ON/OFF e aguarde o bip da unidade.\n- Escolha o modo, a temperatura e a velocidade do ventilador.',
        codigo_universal='Para controles universais, teste os códigos na ordem:\n\n- 2041 — Aerovento Hi-Wall (linha atual)\n- 2042 — Aerovento Hi-Wall (linha anterior)\n- 2043 — Aerovento Cassete',
        reset='Para restaurar o controle:\n\n- Retire as pilhas por trinta segundos.\n- Recoloque as pilhas e aguarde o visor acender.',
        desbloqueio='Para desbloquear as teclas:\n\n- Mantenha MODE e FAN pressionados por três segundos.\n- O ícone de cadeado some do visor.',
        modos='Modos do controle:\n\n- COOL — resfria o ambiente\n- DRY — reduz a umidade\n- FAN — só ventila\n- HEAT — aquece, nos modelos quente e frio',
        observacoes='O alcance e o código podem variar por lote. Confira o manual do aparelho.'),
    'cr-rc02': dict(
        instrucoes='Para parear e ajustar o controle:\n\n- Coloque duas pilhas AAA novas.\n- Aponte o controle para o painel do cassete.\n- Pressione ON/OFF e escolha o modo desejado.',
        codigo_universal='Para controles universais, teste os códigos na ordem:\n\n- 3051 — Cristalar Cassete\n- 3052 — Cristalar Hi-Wall',
        reset=None, desbloqueio=None,
        modos='Modos do controle:\n\n- COOL — resfria o ambiente\n- DRY — reduz a umidade\n- FAN — só ventila',
        observacoes=None),
}


def _norm(s):
    s = unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', '', s)


def montar_catalogo():
    marca_id = lambda k: f'@id:t18.marca.{k}'
    cat_id = lambda k: f'@id:t18.categoria.{k}'
    mod_id = lambda k: f'@id:t18.modelo.{k}'
    out = {
        '_comentario': 'T18 · catálogo GLOBAL fictício da Área do Técnico (sem logos, marcas inventadas). Gerado por rec/t18/semear.py: não edite à mão.',
        'equipment_brands': [], 'equipment_model_categories': [], 'equipment_models': [], 'equipment_error_codes': [],
        'compressor_specs': [], 'remote_configs': [], 'refrigerant_gases': [],
    }
    for k, nome, sort, _ in MARCAS:
        out['equipment_brands'].append({'id': marca_id(k), 'name': nome, 'slug': k, 'logo_url': None, 'sort': sort, 'created_at': '@now-200d'})
    for k, nome, dom in CATEGORIAS:
        out['equipment_model_categories'].append({'id': cat_id(k), 'name': nome, 'domain': dom, 'i18n': None, 'created_at': '@now-200d'})
    desenho_cat = {'hiwall': ilu.hiwall, 'cassete': ilu.cassete, 'pisoteto': ilu.pisoteto}

    def modelo(domain, marca, chave, cat, nome, codigo, gas, kwh, w, imagem, manual):
        return {'id': mod_id(chave), 'brand_id': marca_id(marca), 'category_id': cat_id(cat) if cat else None, 'name': nome, 'code': codigo,
                'image_url': imagem, 'manual_url': manual, 'manual_type': None, 'refrigerant': gas, 'consumo_kwh_mes': kwh,
                'potencia_w': w, 'domain': domain, 'compressor_model_id': None, 'i18n': None, 'created_at': '@now-180d'}

    def codigos(modelo_chave, lista, tabela):
        for c in lista:
            t, d, dg, sl, comp = tabela.get(c) or COD[c]
            out['equipment_error_codes'].append({
                'id': f'@id:t18.erro.{modelo_chave}.{c}', 'model_id': mod_id(modelo_chave), 'code': c, 'title': t, 'description': d,
                'diagnosis': dg, 'solution': sl, 'component': comp, 'i18n': None, 'created_at': '@now-180d'})

    for marca, chave, cat, nome, codigo, gas, kwh, w, lista in AC:
        out['equipment_models'].append(modelo('ar_condicionado', marca, chave, cat, nome, codigo, gas, kwh, w,
                                              desenho_cat[cat](COR[marca]), f'https://manuais.{marca}.example/{codigo.lower()}.pdf'))
        codigos(chave, lista, {})
    for marca, chave, nome, codigo, gas, ficha in COMPRESSORES:
        out['equipment_models'].append(modelo('compressor', marca, chave, 'rotativo', nome, codigo, gas, None, None,
                                              ilu.compressor(COR[marca]), f'https://manuais.{marca}.example/{codigo.lower()}-datasheet.pdf'))
        out['equipment_models'][-1]['manual_type'] = 'datasheet'
        out['compressor_specs'].append({'model_id': mod_id(chave), 'created_at': '@now-180d', **ficha})
    for marca, chave, cat, nome, codigo, kwh, w, lista in LINHA_BRANCA:
        out['equipment_models'].append(modelo('linha_branca', marca, chave, cat, nome, codigo, None, kwh, w,
                                              (ilu.geladeira if cat == 'geladeira' else ilu.freezer)(COR[marca]),
                                              f'https://manuais.{marca}.example/{codigo.lower()}.pdf'))
        codigos(chave, lista, COD_LB_TITULOS)
    for marca, chave, nome, codigo in CONTROLES:
        out['equipment_models'].append(modelo('controle_remoto', marca, chave, None, nome, codigo, None, None, None, ilu.controle(COR[marca]), None))
        out['remote_configs'].append({'model_id': mod_id(chave), 'created_at': '@now-180d', **CONTROLE_CFG[chave]})
    for i, (code, nome, tipo, classe, cor, comp, gwp, odp, pe, glide, oleo, subst, aplic, obs) in enumerate(GASES, start=1):
        out['refrigerant_gases'].append({
            'id': f'@id:t18.gas.{code}', 'code': code, 'name': nome, 'tipo': tipo, 'classe_seguranca': classe, 'cor': cor, 'composicao': comp,
            'gwp': gwp, 'odp': odp, 'ponto_ebulicao_c': pe, 'glide_k': glide, 'oleo': oleo, 'substitui': subst, 'aplicacao': aplic,
            'observacoes': obs, 'ficha_url': None, 'guia_oficial_url': None, 'sort': i, 'created_at': '@now-200d'})
    return out


def verificar_catalogo(cat):
    ok = True
    # 1) busca "E1": só o código E1 pode casar (código, título e descrição, sem espaços), e por modelo da lista de AC
    alvo = _norm('E1')
    por_codigo = {}
    for ec in cat['equipment_error_codes']:
        if any(alvo in _norm(ec[c]) for c in ('code', 'title', 'description')):
            por_codigo.setdefault(ec['code'], 0)
            por_codigo[ec['code']] += 1
    print('busca "E1" casa os códigos:', por_codigo)
    if set(por_codigo) != {'E1'}:
        ok = False
        print('  PROBLEMA: a busca "E1" traria outro código além do E1')
    # 2) nenhum modelo casa "e1" por nome/código/marca (a seção "Catálogo" não aparece na busca do E1: ver roteiro)
    marcas = {b['id']: b['name'] for b in cat['equipment_brands']}
    casam = [m['name'] for m in cat['equipment_models']
             if m['domain'] == 'ar_condicionado' and any(alvo in _norm(x) for x in (m['name'], m['code'], marcas[m['brand_id']]))]
    print('modelos de AC que casam "E1" por nome/código/marca:', casam)
    # 3) máquinas com o E1 (<= 6 para não aparecer "+N mais")
    n_e1 = sum(1 for ec in cat['equipment_error_codes'] if ec['code'] == 'E1')
    print('máquinas com E1:', n_e1)
    ok = ok and n_e1 <= 6
    # 4) potências, tipos e gases do filtro
    btus = sorted({int(re.search(r'(\d+)\.(\d{3})', m['name']).group(1)) * 1000 + int(re.search(r'(\d+)\.(\d{3})', m['name']).group(2))
                   for m in cat['equipment_models'] if m['domain'] == 'ar_condicionado'})
    print('potências do filtro:', btus)
    print('modelos de AC:', sum(1 for m in cat['equipment_models'] if m['domain'] == 'ar_condicionado'), '(selo "N itens")')
    # 5) Hi-Wall 18.000 da Aerovento: código AV-HW18, R-410A, consumo e potência, manual com tipo vazio
    hw18 = [m for m in cat['equipment_models'] if m['code'] == 'AV-HW18']
    if len(hw18) != 1 or hw18[0]['refrigerant'] != 'R-410A' or not hw18[0]['manual_url'] or hw18[0]['manual_type']:
        ok = False
        print('  PROBLEMA: Hi-Wall 18.000 da Aerovento fora do combinado')
    # 6) todo modelo de AC e de linha branca tem códigos e manual (nada de "Indisponível" vermelho nos cartões)
    com_cod = {ec['model_id'] for ec in cat['equipment_error_codes']}
    for m in cat['equipment_models']:
        if m['domain'] in ('ar_condicionado', 'linha_branca') and (m['id'] not in com_cod or not m['manual_url']):
            ok = False
            print('  PROBLEMA: sem código ou sem manual:', m['name'])
    # 7) ids únicos
    ids = [r['id'] for t in ('equipment_brands', 'equipment_model_categories', 'equipment_models', 'equipment_error_codes', 'refrigerant_gases')
           for r in cat[t]]
    if len(ids) != len(set(ids)):
        ok = False
        print('  PROBLEMA: ids repetidos')
    print('catálogo:', {k: len(v) for k, v in cat.items() if isinstance(v, list)}, 'OK' if ok else 'COM PROBLEMA')
    return ok


# ================================================================ fim do T7 provisório
def linhas(chain, tabela):
    por_id = {}
    for rel in chain:
        if exists(rel):
            for r in load(rel).get(tabela, []):
                por_id[r.get('id') or id(r)] = r
    return list(por_id.values())


def montar_fim_t7(chain):
    """Reproduz o "Estado final" do T07/roteiro.md por cima de t7/inicio: OS #16 Concluída (check-in 09:05, check-out 85 min depois),
    consumo de estoque (Limpa-evaporador 12 -> 10 un; Fita isolante 30 -> 28 rolos) e a avaliação do cliente (nota 10, 5 estrelas)."""
    achadas = [r for r in linhas(chain, 'service_orders') if r.get('order_number') == 16]
    if len(achadas) != 1:
        raise SystemExit(f'esperava uma OS #16 na cadeia, achei {len(achadas)}')
    os16 = achadas[0]
    oid, emp, tec = os16['id'], os16['company_id'], os16['technician_id']
    ini_ci, fim_co, conclui = '2026-11-11T12:05:00.000Z', '2026-11-11T13:30:00.000Z', '2026-11-11T13:31:00.000Z'  # 09:05, 10:30, 10:31 (Brasília)
    crit = [r for r in linhas(chain, 'nps_criteria')]
    out = {
        '_comentario': 'T18 · FIM DO T7 PROVISÓRIO (vale só até o T7 gravar o t7/apos-capNN final). Gerado por rec/t18/semear.py: não edite à mão.',
        '_patch': {
            'service_orders': [{'match': {'id': oid}, 'set': {
                'status': 'concluida', 'check_in_time': ini_ci, 'check_in_by': tec, 'started_at': ini_ci, 'check_out_time': fim_co,
                'check_out_by': tec, 'completed_at': conclui, 'updated_at': conclui, 'partial_finish': False}}],
            'inventory': [
                {'match': {'id': '@id:material.limpa-evaporador'}, 'set': {'quantity': 10}},
                {'match': {'id': '@id:material.fita-isolante'}, 'set': {'quantity': 28}}],
            'inventory_stock_levels': [
                {'match': {'id': '@id:nivel.limpa-evaporador.principal'}, 'set': {'quantity': 10}},
                {'match': {'id': '@id:nivel.fita-isolante.principal'}, 'set': {'quantity': 28}}],
        },
        'service_order_materials': [
            {'id': '@id:t18.mat.limpa', 'company_id': emp, 'service_order_id': oid, 'inventory_id': '@id:material.limpa-evaporador',
             'stock_id': '@id:estoque.principal', 'quantity': 2, 'unit_cost': 20.0, 'created_at': ini_ci},
            {'id': '@id:t18.mat.fita', 'company_id': emp, 'service_order_id': oid, 'inventory_id': '@id:material.fita-isolante',
             'stock_id': '@id:estoque.principal', 'quantity': 2, 'unit_cost': 6.5, 'created_at': ini_ci}],
        'inventory_movements': [
            {'id': '@id:t18.mov.limpa', 'company_id': emp, 'inventory_id': '@id:material.limpa-evaporador', 'stock_id': '@id:estoque.principal',
             'movement_type': 'consumo', 'quantity': -2, 'stock_before': 12, 'stock_after': 10, 'service_order_id': oid, 'unit_cost': 20.0,
             'notes': 'Consumo na OS #16', 'created_at': conclui},
            {'id': '@id:t18.mov.fita', 'company_id': emp, 'inventory_id': '@id:material.fita-isolante', 'stock_id': '@id:estoque.principal',
             'movement_type': 'consumo', 'quantity': -2, 'stock_before': 30, 'stock_after': 28, 'service_order_id': oid, 'unit_cost': 6.5,
             'notes': 'Consumo na OS #16', 'created_at': conclui}],
        'service_ratings': [
            {'id': '@id:t18.rating.os16', 'service_order_id': oid, 'nps_score': 10, 'quality_rating': 5, 'punctuality_rating': 5,
             'professionalism_rating': 5, 'comment': None, 'rated_by_name': 'Antônio Ferreira', 'rated_at': '2026-11-11T13:45:00.000Z',
             'created_at': conclui}],
    }
    nomes = {'Qualidade': 0, 'Pontualidade': 1, 'Profissionalismo': 2}
    out['service_rating_criteria'] = [
        {'rating_id': '@id:t18.rating.os16', 'criterion_id': (next((c['id'] for c in crit if c.get('label') == n), None)),
         'label_snapshot': n, 'value': 5} for n in nomes]
    for r in out['service_rating_criteria']:
        if r['criterion_id'] is None:
            del r['criterion_id']
    return out, os16


def main():
    verificar = '--verificar' in sys.argv
    cat = montar_catalogo()
    ok = verificar_catalogo(cat)
    if verificar:
        sys.exit(0 if ok else 1)
    if not ok:
        raise SystemExit('catálogo com problema: corrija antes de gerar')
    os.makedirs(os.path.join(EXTRA, 't18'), exist_ok=True)
    with open(os.path.join(EXTRA, 't18', 'catalogo.json'), 'w', encoding='utf8') as f:
        json.dump(cat, f, ensure_ascii=False, indent=1)
    ult5 = ultimo('t5')
    if not ult5:
        raise SystemExit('não achei nenhum t5/apos-capNN')
    base = CHAIN_T7 + [ult5, 't7/inicio']
    t7_final = ultimo('t7')
    if t7_final:
        cadeia = base + [t7_final]
        provisorio = False
    else:
        fim, os16 = montar_fim_t7(base)
        with open(os.path.join(EXTRA, 't18', 'fim-t7-provisorio.json'), 'w', encoding='utf8') as f:
            json.dump(fim, f, ensure_ascii=False, indent=1)
        cadeia = base + ['t18/fim-t7-provisorio']
        provisorio = True
    cadeia += ['t18/catalogo']
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump({'inicio': cadeia, 't7_final_real': t7_final, 'provisorio': provisorio}, f, ensure_ascii=False, indent=1)
    print('cadeia do T18:', ' + '.join(cadeia))
    print('  fim do T7:', t7_final or 'PROVISÓRIO (t18/fim-t7-provisorio): o T7 ainda não gravou o apos-capNN final')


if __name__ == '__main__':
    main()
