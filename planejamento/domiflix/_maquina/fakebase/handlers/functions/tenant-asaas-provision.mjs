// Edge function `tenant-asaas-provision` falsa (T19 · cap. 2, "Ativar recebimentos"). Espelha supabase/functions/tenant-asaas-provision (1.38.19):
//   POST { action: 'activate', api_key } -> { status: 'active', account: { name, cpfCnpj_masked }, webhook_registered: true }
//   POST { action: 'deactivate' }        -> { status: 'disabled' }
// A real valida a chave na API da Asaas e guarda o segredo no cofre: aqui NENHUMA chamada externa e a chave NÃO é guardada (só o tamanho
// é conferido). Cria/atualiza a linha de `tenant_payment_accounts` com os padrões do banco de produção (o upsert real não mexe nos
// interruptores, que já nascem ligados): `auto_post_to_finance` e `auto_post_fees` true, multa 2 %, juros 1 %, vencimento padrão 0 dia,
// Pix/boleto/cartão ligados, categoria da taxa "Tarifas e Taxas", cartão recorrente e Pix Automático ligados
// (supabase/migrations/20260823170000_cobrancas_flags_default_on.sql), SEM conta de destino e SEM categoria de receita.
// `card_fee_override.pixFreeCount: 0` diz ao `tenant-asaas-card-fees` que esta conta não tem franquia de Pix (a taxa de R$ 1,99 da cobrança
// paga no cap. 8 não pode ser desmentida pela nota "As primeiras 100 recebidas no mês não pagam tarifa.").
import { FunctionError } from '../../http/functions.mjs';
import { nowIso } from '../../core/util.mjs';

export default async function tenantAsaasProvision(body, { db, userId, companyId }) {
  if (!db.find('company_modules', (m) => String(m.company_id) === String(companyId) && m.module_code === 'cobrancas').length) {
    throw new FunctionError('O módulo Cobranças online não está contratado.', 403);
  }
  const atual = db.first('tenant_payment_accounts', (r) => String(r.company_id) === String(companyId));
  if (body?.action === 'deactivate') {
    if (atual) db.update('tenant_payment_accounts', (r) => r === atual, { status: 'disabled' });
    return { status: 'disabled' };
  }
  const chave = String(body?.api_key ?? '').trim();
  if (chave.length < 10) throw new FunctionError('Não foi possível ativar os recebimentos. Confira a chave e tente novamente.', 400);
  const co = db.first('company_settings', (r) => String(r.company_id) === String(companyId));
  const padrao = {
    provider: 'asaas', mode: 'production', status: 'active', asaas_account_id: 'acc_glacial_demo', wallet_id: 'wallet_glacial_demo',
    asaas_webhook_id: 'whk_glacial_demo', auto_post_to_finance: true, auto_post_fees: true, default_fine_percent: 2, default_interest_percent: 1,
    default_due_days: 0, default_discount_percent: null, default_discount_days: null, default_description: null,
    allow_pix: true, allow_boleto: true, allow_card: true, default_max_installments: 1, default_finance_account_id: null,
    default_income_category: null, default_fee_category: 'Tarifas e Taxas', card_recurring_enabled: true, pix_auto_enabled: true,
    card_fee_payer: 'tenant', card_fee_override: { pixFreeCount: 0 }, card_fees_cache: null, card_fees_synced_at: null,
  };
  if (atual) db.update('tenant_payment_accounts', (r) => r === atual, { ...padrao, updated_at: nowIso() });
  else db.insert('tenant_payment_accounts', { company_id: companyId, created_by: userId, ...padrao });
  const doc = String(co?.document || '');
  return {
    status: 'active',
    account: { name: co?.name || 'Glacial Cold Brasil', cpfCnpj_masked: doc ? doc.replace(/^(\d{2})\.\d{3}\.\d{3}\/(\d{4})-(\d{2})$/, '$1.***.***/$2-$3') : null },
    webhook_registered: true,
  };
}
