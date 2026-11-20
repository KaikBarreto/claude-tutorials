// RPC execute_group_transfers_batch (T22, 1.60.18), o "Executar todas": só a dona do grupo de cada transferência; executa uma a uma e devolve
// { ok: [ids], failed: [{ transfer_id, error }] } (a que não tem saldo na origem falha sozinha e as outras seguem).
import { exigeDono } from '../../lib/grupo.mjs';
import { executaTransferencia } from './execute_group_stock_transfer.mjs';
export default (a, ctx) => {
  const ok = [];
  const failed = [];
  for (const id of a._transfer_ids || []) {
    try {
      const t = ctx.store.rows('group_stock_transfers').find((x) => x.id === id);
      if (!t) throw new ctx.RpcError('Transfer not found');
      exigeDono(ctx, t.group_id);
      executaTransferencia(ctx, id);
      ok.push(id);
    } catch (e) {
      failed.push({ transfer_id: id, error: String(e.message || e) });
    }
  }
  return { ok, failed };
};
