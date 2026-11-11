// RPC create_group_transfer_and_execute (20260908213000), a "Nova" transferência da matriz: valida origem/destino do grupo e os materiais de
// cada unidade, idempotência pelo client_request_id, grava a linha 'pending' e, se o grupo NÃO exige aprovação, já executa
// (_execute_group_transfer_row). Com aprovação devolve { status: 'pending' } e o estoque não se move.
import { exigeDono, empresasDoGrupo, agora } from '../../lib/grupo.mjs';
import { executaTransferencia } from './execute_group_stock_transfer.mjs';
import { num } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, db, RpcError } = ctx;
  const g = exigeDono(ctx, a._group_id);
  const q = num(a._quantity);
  if (!(q > 0)) throw new RpcError('Quantity must be positive');
  if (a._from_company_id === a._to_company_id) throw new RpcError('Origin and destination must differ');
  const ids = empresasDoGrupo(store, g.id);
  if (!ids.includes(a._from_company_id)) throw new RpcError('Origin company is not in this group');
  if (!ids.includes(a._to_company_id)) throw new RpcError('Destination company is not in this group');
  if (!a._from_material_id || !a._to_material_id) throw new RpcError('Both source and destination materials must be set');
  const mo = store.rows('materials').find((m) => m.id === a._from_material_id);
  if (!mo) throw new RpcError('Source material not found');
  if (mo.company_id !== a._from_company_id) throw new RpcError('Source material does not belong to the origin company');
  const md = store.rows('materials').find((m) => m.id === a._to_material_id);
  if (!md) throw new RpcError('Destination material not found');
  if (md.company_id !== a._to_company_id) throw new RpcError('Destination material does not belong to the destination company');
  const cri = a._client_request_id ? String(a._client_request_id).trim() || null : null;
  if (cri) {
    const ex = store.rows('group_stock_transfers').find((t) => t.client_request_id === cri);
    if (ex) {
      const f = store.rows('materials').find((m) => m.id === ex.from_material_id);
      const t = store.rows('materials').find((m) => m.id === ex.to_material_id);
      return { transfer_id: ex.id, status: ex.status, from_stock_after: num(f?.current_stock), to_stock_after: num(t?.current_stock), idempotent_skip: true };
    }
  }
  const row = db.insert('group_stock_transfers', { group_id: g.id, from_company_id: a._from_company_id, to_company_id: a._to_company_id,
    group_material_id: a._group_material_id || null, from_material_id: a._from_material_id, to_material_id: a._to_material_id, quantity: q,
    unit: String(a._unit || '').trim() || 'kg', notes: a._notes ?? null, status: 'pending', created_by: ctx.userId, client_request_id: cri,
    created_at: new Date(agora()).toISOString() });
  if (g.require_transfer_approval) return { transfer_id: row.id, status: 'pending', idempotent_skip: false };
  return { ...executaTransferencia(ctx, row.id), idempotent_skip: false };
};
