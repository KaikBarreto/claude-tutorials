#!/usr/bin/env python3
"""T19 · gera o mundo de partida (rec/fakebase/seeds-extra/t19/inicio.json) e rec/t19/cadeia.json.

Estado de partida = fim do T13 (cadeia do T13 + `t13/apos-cap14`) + o que o T19 exige:
  - G1 (1.38.19): `_patch` da trilha Domiflix `tutoriais-do-sistema` com `is_onboarding: false` (sem tela escura de introdução nem faixa de lembrete);
  - SEM conta Asaas ativa (decisão 1 do plano: a aula mostra a ativação): a linha de `tenant_payment_accounts` que a base traz ativa vira `status: null`
    (o app lê "sem selo, com o campo da chave"; o `tenant-asaas-provision` falso a completa com os padrões do banco);
  - tabelas das cobranças e assinaturas vazias de propósito (o que aparecer em /__dev/unknowns a mais é falha de verdade).
Os clientes do roteiro (Restaurante Sabor da Serra, Academia Ponto Forte, Hotel Mirante do Mar) já vêm com CNPJ de dígito válido.
Rodar de qualquer pasta:  python3 -I rec/t19/semear.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.normpath(os.path.join(HERE, '..', 'fakebase', 'seeds-extra'))
FAKE_NOW = '2026-11-10T10:00:00-03:00'
C13 = json.load(open(os.path.join(HERE, '..', 't13', 'cadeia.json'), encoding='utf8'))
CADEIA = list(C13['inicio']) + ['t13/apos-cap14']


def montar():
    ini = {'_comentario': 'T19 · fim do T13 sem conta Asaas ativa (a aula a ativa ao vivo). Gerado por rec/t19/semear.py: não edite à mão.'}
    ini['_patch'] = {
        'domiflix_learning_paths': [{'match': {'id': 'c0000000-0000-4000-8000-000000000001'}, 'set': {'is_onboarding': False}}],
        'tenant_payment_accounts': [{'match': {'id': '@id:tpa.glacial'}, 'set': {'status': None, 'default_finance_account_id': None, 'default_income_category': None,
                                                                                 'card_recurring_enabled': False, 'pix_auto_enabled': False}}],
    }
    # as duas primeiras: o que o Financeiro consulta e a aula cria; as demais: a subaba WhatsApp, que é a que a aba Integrações abre primeiro (cap. 2) e
    # consulta antes de o robô trocar para Cobranças (sem o seed vazio, /__dev/unknowns acusa TABELA_SEM_SEED)
    for nome in ['tenant_charges', 'tenant_subscriptions', 'company_whatsapp_settings', 'whatsapp_connections', 'whatsapp_send_jobs']:
        ini.setdefault(nome, [])
    return ini


def verificar(ini):
    ids = set()
    for rel in CADEIA:
        with open(os.path.join(EXTRA, rel + '.json'), encoding='utf8') as f:
            ids |= set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', f.read()))
    ref = set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json.dumps(ini)))
    print('ids literais fora da cadeia:', sorted(ref - ids) or 'nenhum')


def main():
    ini = montar()
    os.makedirs(os.path.join(EXTRA, 't19'), exist_ok=True)
    with open(os.path.join(EXTRA, 't19', 'inicio.json'), 'w', encoding='utf8') as f:
        json.dump(ini, f, ensure_ascii=False, indent=1)
    cad = {'fake_now': FAKE_NOW, 'inicio': CADEIA + ['t19/inicio'], 'nota': 'mundo do T19 = fim do T13 (t13/apos-cap14) + t19/inicio; apos-capNN do T19 são cumulativos sobre t19/inicio'}
    with open(os.path.join(HERE, 'cadeia.json'), 'w', encoding='utf8') as f:
        json.dump(cad, f, ensure_ascii=False, indent=1)
    print('t19/inicio.json e rec/t19/cadeia.json gerados;', ' + '.join(cad['inicio']))
    verificar(ini)


if __name__ == '__main__':
    main()
