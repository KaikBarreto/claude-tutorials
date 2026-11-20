// RPC create_group_transfer_as_member (T22, 1.60.18): o pedido da FILIAL ("Transferir Estoque" no Materiais dela): grava a linha 'pending' com
// origem e destino do grupo, SEM mexer no estoque (a matriz executa depois). Só a origem pode ser a empresa de quem pede ou o destino; devolve o id.
import { exigeMembro, empresasDoGrupo, agora } from '../../lib/grupo.mjs';
import { num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const cid = exigeMembro(ctx, a._group_id);
  const q = num(a._quantity);
  if (!(q > 0)) throw new RpcError('Quantity must be positive');
  if (a._from_company_id === a._to_company_id) throw new RpcError('Origin and destination must differ');
  if (cid !== a._from_company_id && cid !== a._to_company_id) throw new RpcError('Access denied', '42501', 403);
  const ids = empresasDoGrupo(store, a._group_id);
  if (!ids.includes(a._from_company_id) || !ids.includes(a._to_company_id)) throw new RpcError('Company is not in this group');
  const mo = store.rows('materials').find((m) => m.id === a._from_material_id && m.company_id === a._from_company_id);
  const md = store.rows('materials').find((m) => m.id === a._to_material_id && m.company_id === a._to_company_id);
  if (!mo || !md) throw new RpcError('Material not found');
  const row = db.insert('group_stock_transfers', { group_id: a._group_id, from_company_id: a._from_company_id, to_company_id: a._to_company_id,
    group_material_id: a._group_material_id || null, from_material_id: mo.id, to_material_id: md.id, quantity: q, unit: String(a._unit || '').trim() || 'kg',
    notes: a._notes ?? null, status: 'pending', created_by: ctx.userId, client_request_id: null, created_at: new Date(agora()).toISOString() });
  return row.id;
};
