#!/usr/bin/env python3
"""T15: escreve as sementes de estado da aula (rec/mundo/seeds-extra/t15/apos-cap01, apos-cap02, apos-cap10) a partir do que o APP gravou
na minha instância (54315) num ensaio ou gravação do capítulo (lê /__dev/state; rode logo depois do capítulo, antes de outro reset).
Uso: python3 -I rec/t15/t15_sementes.py 01|02|10
- 01: as categorias "Frete de entrega" e "Máquinas e veículos" como o app as criou (cor, ícone, grupos, pai, ordem).
- 02: o centro de custo "Produção".
- 10: a exclusão da cópia da "Conta de energia" (o _remove da linha semeada pelo t15/inicio; confere que o ensaio a excluiu)."""
import hashlib, json, os, sys, urllib.request

URL = 'http://127.0.0.1:54315'
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mundo', 'seeds-extra', 't15')
AGORA = '2026-11-10T11:{:02d}:00.000Z'   # 08:mm em Brasília, no começo do dia da aula


def sid(k):
    h = bytearray(hashlib.sha1(('domiflix-fake:' + k).encode()).digest()); h[6] = (h[6] & 0x0F) | 0x50; h[8] = (h[8] & 0x3F) | 0x80
    x = h[:16].hex(); return f'{x[:8]}-{x[8:12]}-{x[12:16]}-{x[16:20]}-{x[20:32]}'


CHAVES = ['company.reciclavale', 'user.rafael', 'categoria.frete'] + [f'dre.{n}' for n in ('receita_bruta', 'deducoes', 'custos', 'despesas_operacionais', 'outras_receitas_despesas')]
TOKEN = {sid(k): '@id:' + k for k in CHAVES}


def estado(tab):
    return json.load(urllib.request.urlopen(f'{URL}/__dev/state?table={tab}'))


def limpa(r, novo_id, minuto, campos):
    out = {'id': novo_id}
    for k in campos:
        if k in r:
            v = r[k]
            out[k] = TOKEN.get(v, v) if isinstance(v, str) else v
    out['created_at'] = AGORA.format(minuto)
    if 'updated_at' in r:
        out['updated_at'] = out['created_at']
    return out


def grava(nome, dados):
    os.makedirs(DIR, exist_ok=True)
    p = os.path.join(DIR, nome + '.json')
    json.dump(dados, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('gravado', os.path.relpath(p))


def main():
    n = int(sys.argv[1])
    cid = sid('company.reciclavale')
    if n == 1:
        cats = {r['name']: r for r in estado('financial_categories') if r.get('company_id') == cid}
        campos = ['company_id', 'name', 'type', 'color', 'icon', 'is_system', 'dre_group', 'dre_group_id', 'cash_flow_group', 'parent_id', 'sort_order']
        linhas = []
        for i, (nome, chave) in enumerate((('Frete de entrega', 't15.categoria.frete_entrega'), ('Máquinas e veículos', 't15.categoria.maquinas'))):
            r = cats.get(nome)
            if not r:
                sys.exit(f'FALTA a categoria "{nome}" no estado: rode o capítulo 1 antes')
            linhas.append(limpa(r, '@id:' + chave, 31 + i * 2, campos))
            print(' ', json.dumps(linhas[-1], ensure_ascii=False))
        grava('apos-cap01', {'financial_categories': linhas})
    elif n == 2:
        r = next((c for c in estado('cost_centers') if c.get('company_id') == cid and c.get('name') == 'Produção'), None)
        if not r:
            sys.exit('FALTA o centro de custo "Produção" no estado: rode o capítulo 2 antes')
        linha = limpa(r, '@id:t15.cc.producao', 36, ['company_id', 'name', 'color', 'icon', 'description', 'is_active'])
        print(' ', json.dumps(linha, ensure_ascii=False))
        grava('apos-cap02', {'cost_centers': [linha]})
    elif n == 10:
        copia = sid('t15.energia_copia')
        if any(b.get('id') == copia for b in estado('bank_transactions')):
            sys.exit('a cópia da "Conta de energia" ainda está no estado: o capítulo 10 não a excluiu')
        grava('apos-cap10', {'_remove': {'bank_transactions': [{'id': '@id:t15.energia_copia'}]}})


if __name__ == '__main__':
    main()
