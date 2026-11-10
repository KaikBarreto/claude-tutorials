// Função de BASTIDOR do kit de gravação (não existe no app nem no Supabase real): faz o que o AVISO do Asaas faz quando o cliente paga
// (supabase/functions/tenant-asaas-webhook/index.ts:1016-1074 -> RPC apply_tenant_charge_payment, 20261021210000_cobrar_o_saldo_da_conta_a_receber.sql).
//   POST { short_code?, net_value?, fee? }  (sem `short_code`: a cobrança PENDING mais recente)  ->  { ok, charge_id, fee, net }
// Efeitos (iguais aos da RPC): `tenant_charges.status` CONFIRMED, `payment_date` agora, `net_value` = valor - taxa; a conta a receber ligada à
// cobrança fica paga (`is_paid`, `paid_date` de hoje; quitação total, sem `amount_received`); com `auto_post_fees` e líquido menor que o valor,
// nasce a despesa "Tarifa de recebimento (Asaas) — cobrança #<id>" na categoria da taxa da conta (paga hoje, sem conta e sem cliente).
// Taxa de Pix da conta Asaas fictícia: R$ 1,99.
import { FunctionError } from '../../http/functions.mjs';
import { nowIso, dateBR, now } from '../../core/util.mjs';

const r2 = (n) => Math.round(Number(n) * 100) / 100;

export default async function asaasSimularPagamento(b, { db }) {
  const c = b?.short_code
    ? db.first('tenant_charges', { public_short_code: b.short_code })
    : db.rows('tenant_charges').filter((x) => x.status === 'PENDING').sort((x, y) => String(y.created_at).localeCompare(String(x.created_at)))[0];
  if (!c) throw new FunctionError('Cobrança não encontrada.', 404);
  if (c.payment_date) return { ok: true, charge_id: c.id, already_paid: true };
  const taxa = b?.fee !== undefined ? r2(b.fee) : 1.99;
  const liquido = b?.net_value !== undefined ? r2(b.net_value) : r2(c.value - taxa);
  const hoje = dateBR(0, now());
  db.update('tenant_charges', (r) => r === c, { status: 'CONFIRMED', payment_date: nowIso(), net_value: liquido });
  const mae = db.first('financial_transactions', (t) => String(t.tenant_charge_id) === String(c.id) && t.transaction_type === 'entrada' && !t.parent_transaction_id);
  if (mae && !mae.is_paid) db.update('financial_transactions', (t) => t === mae, { is_paid: true, paid_date: hoje });
  const conta = db.first('tenant_payment_accounts', (r) => String(r.company_id) === String(c.company_id));
  const jaTem = db.first('financial_transactions', (t) => String(t.tenant_charge_id) === String(c.id) && t.transaction_type === 'saida');
  if ((conta?.auto_post_fees ?? false) && liquido < c.value && !jaTem) {
    db.insert('financial_transactions', {
      company_id: c.company_id, transaction_type: 'saida', amount: r2(c.value - liquido), description: `Tarifa de recebimento (Asaas) — cobrança #${c.id}`,
      category: (conta.default_fee_category || '').trim() || 'Tarifas e Taxas', is_paid: true, paid_date: hoje, transaction_date: hoje, tenant_charge_id: c.id,
      account_id: null, customer_id: null, created_by: null,
    });
  }
  return { ok: true, charge_id: c.id, fee: r2(c.value - liquido), net: liquido };
}
