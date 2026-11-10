// Edge function `tenant-asaas-create-subscription` falsa (T19 · cap. 10). Espelha supabase/functions/tenant-asaas-create-subscription (1.38.19):
//   POST { customer_id, value, cycle, billing_type, next_due_date, description, category, cost_center_id, fine_*, interest_percent,
//          source_type, source_id, max_payments } -> { subscription } (e `checkout_url`/`checkout_kind` no cartão recorrente e no Pix Automático).
// Insere SÓ a `tenant_subscriptions` (ativa, id da Asaas fictício). NENHUMA `tenant_charges`: em produção o ciclo só vira cobrança quando a Asaas
// avisa (supabase/functions/tenant-asaas-webhook/index.ts:45-50,1239-1243), e é esse ciclo que o T20 projeta no DRE.
import { FunctionError } from '../../http/functions.mjs';
import { uuid } from '../../core/util.mjs';

export default async function tenantAsaasCreateSubscription(b, { db, userId, companyId }) {
  const conta = db.first('tenant_payment_accounts', (r) => String(r.company_id) === String(companyId));
  if (!conta || conta.status !== 'active') throw new FunctionError('Ative os recebimentos antes de criar assinaturas.', 400);
  const cliente = db.first('customers', { id: b.customer_id });
  if (!cliente) throw new FunctionError('Cliente não encontrado.', 404);
  if (!String(cliente.document || '').replace(/\D/g, '')) {
    throw new FunctionError(`${cliente.name} ainda não tem CPF ou CNPJ no cadastro. A Asaas exige esse dado para gerar a cobrança.`, 400);
  }
  if (b.billing_type === 'CREDIT_CARD' && !conta.card_recurring_enabled) throw new FunctionError('Cartão recorrente não habilitado.', 400, { code: 'method_not_enabled', method: 'credit_card' });
  if (b.billing_type === 'PIX_AUTOMATIC' && !conta.pix_auto_enabled) throw new FunctionError('Pix Automático não habilitado.', 400, { code: 'method_not_enabled', method: 'pix_auto' });
  const id = uuid();
  const sub = db.insert('tenant_subscriptions', {
    id, company_id: companyId, customer_id: cliente.id, asaas_subscription_id: 'sub_' + id.replace(/-/g, '').slice(0, 16), cycle: b.cycle || 'MONTHLY',
    value: Number(b.value), billing_type: b.billing_type || 'UNDEFINED', next_due_date: b.next_due_date || null, status: 'active', description: b.description || null,
    category: b.category || null, cost_center_id: b.cost_center_id ?? null, fine_percent: b.fine_percent ?? null, fine_type: b.fine_type ?? null,
    fine_value: b.fine_value ?? null, interest_percent: b.interest_percent ?? null, max_payments: b.max_payments ?? null,
    source_type: b.source_type || 'avulso', source_id: b.source_id || null, created_by: userId,
  });
  return { subscription: sub };
}
