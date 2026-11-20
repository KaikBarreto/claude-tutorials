// RPC get_group_order_history_lines (20261106143000), a aba "Histórico" do Financeiro Gerencial: compras e vendas concluídas das unidades do grupo
// (ou das pedidas) no período, da mais nova para a mais antiga, paginadas por p_limit/p_offset; total_count em toda linha.
import { escopo, nomeEmpresa } from '../../lib/grupo.mjs';
import { pedidos, nomeParceiro, num, diaDe } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store, RpcError } = ctx;
  if (!a.p_group_id || !a.p_start_date || !a.p_end_date) throw new RpcError('Parametros obrigatorios ausentes');
  const cids = escopo(ctx, a.p_group_id, a.p_company_ids);
  const j = { d1: String(a.p_start_date).slice(0, 10), d2: String(a.p_end_date).slice(0, 10) };
  const linhas = [];
  for (const cid of cids) {
    for (const tipo of ['purchase', 'sale']) {
      for (const p of pedidos(store, cid, tipo, j)) {
        linhas.push({ id: p.id, order_type: tipo, order_number: p.order_number ?? null, order_ref: p.order_ref ?? null, total_amount: num(p.total_amount),
          currency: p.currency || 'BRL', created_at: p.created_at ?? null, transaction_at: p.transaction_at ?? null, transaction_date: diaDe(p),
          company_id: cid, company_name: nomeEmpresa(store, cid), partner_name: nomeParceiro(store, tipo === 'purchase' ? 'supplier' : 'customer', tipo === 'purchase' ? p.supplier_id : p.customer_id) });
      }
    }
  }
  linhas.sort((x, y) => String(y.transaction_at || y.created_at).localeCompare(String(x.transaction_at || x.created_at)));
  const off = Number(a.p_offset) || 0;
  return linhas.slice(off, off + (Number(a.p_limit) || 1000)).map((l) => ({ ...l, total_count: linhas.length }));
};
