// Posição de estoque numa data (T10, "posição em 31/10"): o saldo de cada material depois do último movimento até a data.
import { r3, r2, custoMedio, diaBR } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const limite = new Date(a.p_at || Date.now()).getTime();
  const ult = new Map();
  for (const s of store.rows('stock_movements')) {
    if (s.company_id !== cid) continue;
    const t = new Date(s.transaction_at || s.created_at).getTime();
    if (t > limite) continue;
    const u = ult.get(s.material_id);
    if (!u || t > u.t || (t === u.t && String(s.id) > String(u.id))) ult.set(s.material_id, { t, id: s.id, saldo: s.stock_after });
  }
  const cm = custoMedio(store, cid, diaBR(limite));
  return store.rows('materials').filter((m) => m.company_id === cid && !m.is_archived).map((m) => ({
    material_id: m.id, code: m.code, name: m.name, unit: m.unit, saldo: r3(ult.get(m.id)?.saldo ?? 0), avg_cost: r2(cm.get(m.id) || 0), sale_price: m.sale_price,
  }));
};
