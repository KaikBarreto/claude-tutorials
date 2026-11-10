// Edge function `tenant-asaas-manage-subscription` falsa (T19 · cap. 11; o vídeo só abre os diálogos e volta). Espelha a real (1.38.19):
//   POST { subscription_id, action: 'cancel'|'update'|'archive'|'unarchive'|'delete', ...campos } -> { subscription }
// `cancel`: status 'cancelled' (as próximas cobranças deixam de nascer; o histórico fica). `update`: valor, ciclo, forma, próximo vencimento, descrição.
import { FunctionError } from '../../http/functions.mjs';
import { nowIso } from '../../core/util.mjs';

export default async function tenantAsaasManageSubscription(b, { db, companyId }) {
  const s = db.first('tenant_subscriptions', (r) => String(r.id) === String(b?.subscription_id) && String(r.company_id) === String(companyId));
  if (!s) throw new FunctionError('Assinatura não encontrada.', 404);
  const acao = b.action || 'update';
  let patch = {};
  if (acao === 'cancel') patch = { status: 'cancelled' };
  else if (acao === 'archive') patch = { archived_at: nowIso() };
  else if (acao === 'unarchive') patch = { archived_at: null };
  else if (acao === 'delete') patch = { deleted_at: nowIso() };
  else {
    for (const k of ['value', 'cycle', 'billing_type', 'next_due_date', 'description', 'category', 'fine_percent', 'fine_type', 'fine_value', 'interest_percent']) {
      if (b[k] !== undefined) patch[k] = b[k];
    }
  }
  db.update('tenant_subscriptions', (r) => r === s, patch);
  return { subscription: db.first('tenant_subscriptions', (r) => r === s) };
}
