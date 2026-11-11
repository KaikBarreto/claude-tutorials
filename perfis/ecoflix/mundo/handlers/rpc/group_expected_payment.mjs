// RPC group_expected_payment (20261016150000): quanto a fatura única do grupo cobra de cada unidade (mensal: custom_price ou o valor da
// assinatura; anual e parcelas do plano anual não acontecem no mundo da T22) e a nova validade (vencimento + 1 mês). Total nulo quando os
// ciclos se misturam (o checkout recusa: GROUP_MIXED_CYCLE).
import { exigeDono, empresasDoGrupo } from '../../lib/grupo.mjs';
import { agoraMs, num, r2 } from '../../lib/eco.mjs';
export function esperado(store, gid) {
  const g = store.rows('company_groups').find((x) => x.id === gid);
  const ids = empresasDoGrupo(store, gid);
  const mais1mes = (iso) => { const d = new Date(iso || agoraMs()); d.setUTCMonth(d.getUTCMonth() + 1); return d.toISOString(); };
  const membros = ids.map((id) => store.rows('companies').find((c) => c.id === id)).filter(Boolean).map((c) => ({
    company_id: c.id, name: c.name, is_matriz: c.id === g?.owner_company_id, cycle: c.billing_cycle, expected: r2(num(c.custom_price ?? c.subscription_value)),
    basis: 'monthly', installment: null, expires_at: c.subscription_expires_at, new_expires_at: mais1mes(c.subscription_expires_at),
  })).sort((x, y) => Number(y.is_matriz) - Number(x.is_matriz) || String(x.name).localeCompare(String(y.name)));
  const misto = new Set(membros.map((m) => m.cycle ?? '(null)')).size > 1;
  return { group_id: gid, owner_company_id: g?.owner_company_id ?? null, total: misto ? null : r2(membros.reduce((s, m) => s + m.expected, 0)), mixed_cycle: misto,
    member_count: membros.length, members: membros };
}
export default (a, ctx) => {
  exigeDono(ctx, a.p_group_id);
  return esperado(ctx.store, a.p_group_id);
};
