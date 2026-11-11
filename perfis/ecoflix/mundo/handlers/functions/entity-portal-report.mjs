// Edge entity-portal-report (a aba Relatório do portal: "Relatório por Material", T20 cap07): agrega por material as compras (fornecedor) e as
// vendas (cliente) "completed" do período (start/end, created_at), quantidade líquida (quantidade - impureza) e valor, mais a lista de moedas
// de cada lado. "Mostrar valores" desligado zera os R$. Senha no portal sem sessão válida: { requiresLogin: true }. Molde do index.ts da 1.59.154.
import { parteDoPortal, temModulo } from '../../lib/coletas.mjs';
import { sessaoValida } from '../../lib/portal.mjs';
import { agoraMs } from '../../lib/eco.mjs';

export default (body, { store, url, FunctionError }) => {
  const token = url.searchParams.get('token') || body?.token;
  if (!token) throw new FunctionError('Token é obrigatório', 400);
  const p = parteDoPortal(store, token);
  if (!p) throw new FunctionError('Token inválido ou expirado', 404);
  if (!temModulo(store, p.companyId, 'portal_cliente')) throw new FunctionError('Portal indisponível', 403, { reason: 'portal_module_inactive' });
  if (p.senha && !sessaoValida(url.searchParams.get('session'), p.ids)) return { requiresLogin: true };
  const fim = url.searchParams.get('end') ? new Date(url.searchParams.get('end')).getTime() : agoraMs();
  const ini = url.searchParams.get('start') ? new Date(url.searchParams.get('start')).getTime() : agoraMs() - 30 * 86400000;
  const noPeriodo = (r) => {
    const t = new Date(r.created_at).getTime();
    return t >= ini && t <= fim;
  };
  const mats = new Map(store.rows('materials').map((m) => [m.id, m]));
  const porMat = new Map();
  const garante = (id) => {
    const m = mats.get(id);
    if (!m) return null;
    if (!porMat.has(id)) {
      porMat.set(id, { material_id: id, name: m.name || 'Material', code: m.code ?? null, unit: m.unit || 'UN', purchased_qty: 0, purchased_value: 0,
        sold_qty: 0, sold_value: 0, purchased_currencies: [], sold_currencies: [] });
    }
    return porMat.get(id);
  };
  const moeda = (lista, c) => {
    const k = String(c ?? '').trim().toUpperCase();
    if (k && !lista.includes(k)) lista.push(k);
  };
  if (p.supplierId) {
    const itens = store.rows('purchase_items');
    for (const c of store.rows('purchases').filter((x) => x.company_id === p.companyId && x.supplier_id === p.supplierId && x.status === 'completed' && noPeriodo(x))) {
      for (const i of itens.filter((it) => it.purchase_id === c.id)) {
        const r = garante(i.material_id);
        if (!r) continue;
        r.purchased_qty += Number(i.quantity || 0) - Number(i.impurity || 0);
        r.purchased_value += Number(i.total_price || 0);
        moeda(r.purchased_currencies, c.currency);
      }
    }
  }
  if (p.customerId) {
    const itens = store.rows('sale_items');
    for (const v of store.rows('sales').filter((x) => x.company_id === p.companyId && x.customer_id === p.customerId && x.status === 'completed' && noPeriodo(x))) {
      for (const i of itens.filter((it) => it.sale_id === v.id)) {
        const r = garante(i.material_id);
        if (!r) continue;
        r.sold_qty += Number(i.quantity || 0);
        r.sold_value += Number(i.total_price || 0);
        moeda(r.sold_currencies, v.currency);
      }
    }
  }
  const mostra = p.cfg.relatorio_valores;
  let rows = [...porMat.values()].sort((a, b) => String(a.name).localeCompare(String(b.name)));
  if (!mostra) rows = rows.map((r) => ({ ...r, purchased_value: 0, sold_value: 0 }));
  return { entity: { name: p.row.name, type: p.tipo, is_dual: p.isDual }, relatorio_valores: mostra, rows };
};
