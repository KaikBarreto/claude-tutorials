// RPC set_inbound_fiscal_entries (migration 20260901030000_inbound_nfe_fiscal_entries; pages/Purchase.tsx depois da compra que veio
// de uma NF-e recebida com "Registrar também no estoque fiscal" marcado, e o "Contar no estoque fiscal" das Notas Recebidas; T17 cap11):
// troca as linhas fiscais da nota (apaga as da nota e grava as novas, effect 1). Não mexe em materials.current_stock: o estoque
// fiscal lê inbound_nfe_fiscal_entries (lib/estoque_fiscal.mjs). Devolve quantas linhas gravou, como o SQL.
import { agoraIso } from '../../lib/nfe.mjs';

export default (a, { store, db, companyId, userId, RpcError }) => {
  const cid = a?.p_company_id || companyId;
  if (cid !== companyId) throw new RpcError('Acesso negado.', '42501', 403);
  const nota = a?.p_inbound_nfe_id;
  const t = store.table('inbound_nfe_fiscal_entries');
  let tirou = false;
  for (let i = t.rows.length - 1; i >= 0; i--) {
    if (t.rows[i].company_id === cid && t.rows[i].inbound_nfe_id === nota) { t.rows.splice(i, 1); tirou = true; }
  }
  if (tirou) t.touch();
  const itens = Array.isArray(a?.p_items) ? a.p_items : [];
  const agora = agoraIso();
  for (const e of itens) {
    db.insert('inbound_nfe_fiscal_entries', {
      company_id: cid, inbound_nfe_id: nota, material_id: e.material_id, quantity: Number(e.quantity), unit: e.unit ?? null,
      valor: e.valor === '' || e.valor == null ? null : Number(e.valor), effect: 1, created_by: a?.p_user_id ?? userId ?? null, created_at: agora,
    }, { companyId: cid });
  }
  return itens.length;
};
