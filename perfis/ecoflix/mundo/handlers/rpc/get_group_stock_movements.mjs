// RPC get_group_stock_movements (Histórico de Materiais do Estoque Gerencial): os movimentos de estoque das unidades do grupo (ou das pedidas)
// entre os dois instantes, com o material canônico do grupo, do mais recente para o mais antigo. Autoriza qualquer unidade do grupo.
import { empresaDoUsuario, empresasDoGrupo, canonicos, nomeEmpresa } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  if (!a._start_date || !a._end_date) throw new ctx.RpcError('_start_date e _end_date são obrigatórios');
  const membros = empresasDoGrupo(store, a._group_id);
  if (!membros.length) return [];
  if (!membros.includes(empresaDoUsuario(store, ctx.userId))) throw new ctx.RpcError('Access denied', '42501', 403);
  const alvo = Array.isArray(a._company_ids) && a._company_ids.length ? membros.filter((c) => a._company_ids.includes(c)) : membros;
  const can = canonicos(store, a._group_id, alvo);
  const t1 = new Date(a._start_date).getTime();
  const t2 = new Date(a._end_date).getTime();
  return store.rows('stock_movements').filter((s) => {
    if (!alvo.includes(s.company_id) || !can.has(s.material_id)) return false;
    const t = new Date(s.transaction_at).getTime();
    return t >= t1 && t <= t2;
  }).sort((x, y) => String(y.transaction_at).localeCompare(String(x.transaction_at)) || String(y.created_at).localeCompare(String(x.created_at)))
    .map((s) => {
      const k = can.get(s.material_id);
      return { id: s.id, company_id: s.company_id, company_name: nomeEmpresa(store, s.company_id), material_id: k.id, code: k.code, name: k.name, unit: k.unit,
        type: s.type, quantity: s.quantity, stock_before: s.stock_before, stock_after: s.stock_after, transaction_at: s.transaction_at, created_at: s.created_at,
        order_id: s.order_id ?? null, order_type: s.order_type ?? null, description: s.description ?? null, created_by: s.created_by ?? null };
    });
};
