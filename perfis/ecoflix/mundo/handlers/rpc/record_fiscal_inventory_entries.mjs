// "Informar saldo inicial" do Estoque Fiscal (T17, app 1.60.10; migration 20261023221000_fiscal_inventory_ledger_and_kardex.sql):
// grava um lote e uma linha por material em `fiscal_inventory_entries` (saldo inicial ou ajuste manual). Fica só no estoque
// fiscal: nada muda no estoque operacional. Repetir o mesmo `p_client_request_id` devolve o lote já gravado (idempotente).
import crypto from 'node:crypto';
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (a, { store, db, companyId, userId, RpcError }) => {
  const cid = a.p_company_id || companyId;
  const cfg = store.rows('company_fiscal_config').find((c) => c.id === a.p_fiscal_config_id && c.company_id === cid);
  if (!cfg) throw new RpcError('O CNPJ fiscal informado nao pertence a esta empresa.');
  if (!a.p_effective_at) throw new RpcError('Informe a data efetiva do lancamento.');
  if (!['opening_balance', 'manual_adjustment'].includes(a.p_entry_type)) throw new RpcError('Tipo permitido: opening_balance ou manual_adjustment.');
  if (a.p_entry_type === 'manual_adjustment' && !String(a.p_reason || '').trim()) throw new RpcError('O motivo e obrigatorio no ajuste manual.');
  if (!a.p_client_request_id) throw new RpcError('client_request_id e obrigatorio.');
  const itens = Array.isArray(a.p_entries) ? a.p_entries : [];
  if (itens.length < 1 || itens.length > 1000) throw new RpcError('Envie entre 1 e 1.000 materiais em p_entries.');
  const ja = store.rows('fiscal_inventory_entry_batches').find((b) => b.company_id === cid && b.client_request_id === a.p_client_request_id);
  if (ja) return { batch_id: ja.id, item_count: ja.item_count, idempotent: true };
  const agora = nowIso();
  const efetiva = new Date(a.p_effective_at).toISOString();
  const lote = crypto.randomUUID();
  const ins = (t, row) => (db && db.insert ? db.insert(t, row, { companyId: cid }) : store.insert(t, row));
  ins('fiscal_inventory_entry_batches', { id: lote, company_id: cid, fiscal_config_id: cfg.id, operation_type: 'record_entries',
    entry_type: a.p_entry_type, effective_at: efetiva, source: a.p_source || 'manual', reason: a.p_reason || null, item_count: itens.length,
    client_request_id: a.p_client_request_id, request_fingerprint: `fake-${a.p_client_request_id}`, created_by: userId || null, created_at: agora });
  for (const it of itens) {
    const q = Number(it.quantity);
    if (!it.material_id || !Number.isFinite(q) || (a.p_entry_type === 'opening_balance' && q < 0)) throw new RpcError('Quantidade invalida em p_entries.');
    ins('fiscal_inventory_entries', { id: crypto.randomUUID(), company_id: cid, fiscal_config_id: cfg.id, material_id: it.material_id,
      entry_type: a.p_entry_type, quantity_delta: q, effective_at: efetiva, reason: a.p_reason || null, source: a.p_source || 'manual',
      import_batch_id: lote, client_request_id: a.p_client_request_id, reverses_entry_id: null, created_by: userId || null, created_at: agora });
  }
  return { batch_id: lote, item_count: itens.length, idempotent: false };
};
