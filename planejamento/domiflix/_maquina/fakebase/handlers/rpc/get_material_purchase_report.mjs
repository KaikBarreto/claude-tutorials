// RPC get_material_purchase_report(p_start_date, p_end_date, p_stock_ids, p_supplier_ids, p_group_ids, p_created_by_ids) → TABLE
// 20261018005000_compra_direta_estoque_financeiro.sql. "Relatório" › "Por material": só entra o que foi RECEBIDO por ordem de
// compra (itens com quantity_received > 0 em ordens 'recebida'/'recebida_parcial', compra não cancelada e com local) e as compras
// diretas (também viram ordem). Entrada rápida, ajuste e nota fiscal importada NÃO entram. Média paga = total ÷ quantidade com
// preço (ponderada). Cada linha traz o histórico (`history`) mais recente primeiro. Todos os materiais elegíveis aparecem,
// mesmo sem compra (zeros).
import { RpcError } from '../../http/rest.mjs';
import { podeAcessarLocal } from '../../lib/estoque.mjs';
import { diaDe } from '../../lib/estoque_locais.mjs';

const num = (v) => (v === null || v === undefined ? null : Number(v));

export default async function getMaterialPurchaseReport(a, { userId, db }) {
  const ini = a.p_start_date || null;
  const fim = a.p_end_date || null;
  if (ini && fim && ini > fim) throw new RpcError('invalid_date_range', '22023');
  const filtroLocais = Array.isArray(a.p_stock_ids) && a.p_stock_ids.length ? new Set(a.p_stock_ids) : null;
  const filtroFornec = Array.isArray(a.p_supplier_ids) && a.p_supplier_ids.length ? new Set(a.p_supplier_ids) : null;
  const filtroGrupos = Array.isArray(a.p_group_ids) && a.p_group_ids.length ? new Set(a.p_group_ids) : null;
  const filtroAutores = Array.isArray(a.p_created_by_ids) && a.p_created_by_ids.length ? new Set(a.p_created_by_ids) : null;

  const locaisOk = new Set(db.rows('stocks').filter((s) => !s.customer_id && podeAcessarLocal(userId, s.id) && (!filtroLocais || filtroLocais.has(s.id))).map((s) => s.id));
  const grupos = new Map(db.rows('material_groups').map((g) => [g.id, g]));
  const locais = new Map(db.rows('stocks').map((s) => [s.id, s]));
  const perfis = new Map(db.rows('profiles').map((p) => [p.user_id, p]));
  const fornecedores = new Map(db.rows('suppliers').map((s) => [s.id, s]));
  const niveis = db.rows('inventory_stock_levels');

  // materiais elegíveis (e saldo atual só nos locais acessíveis/filtrados)
  const elegiveis = db.rows('inventory')
    .filter((i) => !i.customer_id && !i.archived_at && (!filtroGrupos || filtroGrupos.has(i.group_id)))
    .filter((i) => !filtroLocais || niveis.some((l) => l.inventory_id === i.id && locaisOk.has(l.stock_id)))
    .map((i) => ({
      i,
      saldo: niveis.filter((l) => l.inventory_id === i.id && locaisOk.has(l.stock_id)).reduce((s, l) => s + Number(l.quantity || 0), 0),
    }));

  // recebimentos por ordem de compra
  const porMaterial = new Map();
  const compras = new Map(db.rows('compras').map((c) => [c.id, c]));
  const ordens = new Map(db.rows('compra_ordens').map((o) => [o.id, o]));
  for (const it of db.rows('compra_ordem_itens')) {
    const o = ordens.get(it.ordem_id);
    const c = o && compras.get(o.compra_id);
    if (!o || !c || !it.inventory_id || !(Number(it.quantity_received) > 0)) continue;
    if (!['recebida', 'recebida_parcial'].includes(o.status) || c.status === 'cancelada' || !c.stock_id) continue;
    if (!podeAcessarLocal(userId, c.stock_id) || (filtroLocais && !filtroLocais.has(c.stock_id))) continue;
    if (filtroFornec && !filtroFornec.has(o.supplier_id)) continue;
    if (filtroAutores && !filtroAutores.has(o.created_by)) continue;
    const dia = c.purchase_date || diaDe(o.received_at) || diaDe(o.updated_at);
    if ((ini && dia < ini) || (fim && dia > fim)) continue;
    const inv = db.first('inventory', { id: it.inventory_id });
    const qtd = Number(it.quantity_received);
    const preco = num(it.unit_price);
    const quem = perfis.get(o.created_by);
    const lista = porMaterial.get(it.inventory_id) || [];
    lista.push({
      date: dia, order_id: o.id, order_number: o.numero, supplier_id: o.supplier_id, supplier_name: fornecedores.get(o.supplier_id)?.name ?? null,
      stock_id: c.stock_id, stock_name: locais.get(c.stock_id)?.name ?? null, created_by: o.created_by ?? null,
      created_by_name: quem?.full_name || quem?.email || 'Sistema', financial_transaction_id: o.financial_transaction_id ?? null,
      payment_method: null, is_paid: null, payment_status: o.financial_transaction_id ? 'nao_informado' : 'nao_vinculado',
      flow_type: c.flow_type ?? 'requisicao', unit: String(it.unit || '').trim() || inv?.unit || 'un', quantity: qtd, unit_price: preco,
      total: preco === null ? null : qtd * preco, kind: 'compra',
    });
    porMaterial.set(it.inventory_id, lista);
  }

  const out = elegiveis.map(({ i, saldo }) => {
    const hist = (porMaterial.get(i.id) || []).sort((x, y) => (String(y.date).localeCompare(String(x.date))) || (Number(y.order_number) - Number(x.order_number)));
    const comPreco = hist.filter((h) => h.unit_price !== null);
    const qtdTotal = hist.reduce((s, h) => s + h.quantity, 0);
    const qtdPreco = comPreco.reduce((s, h) => s + h.quantity, 0);
    const total = hist.reduce((s, h) => s + (h.total ?? 0), 0);
    const g = grupos.get(i.group_id);
    return {
      inventory_id: i.id, sku: i.sku ?? '', material_name: i.name, unit: String(i.unit || '').trim() || 'un', group_id: i.group_id ?? null,
      group_name: g?.name ?? null, group_color: g?.color ?? null, current_balance: saldo, registered_sale_price: Number(i.sale_price || 0),
      purchased_quantity: qtdTotal, priced_quantity: qtdPreco, unpriced_quantity: qtdTotal - qtdPreco, purchased_total: total,
      average_paid: qtdPreco > 0 ? total / qtdPreco : null, purchase_count: new Set(hist.map((h) => h.order_id)).size,
      last_purchase_date: hist.length ? hist.reduce((m, h) => (h.date > m ? h.date : m), hist[0].date) : null, history: hist,
    };
  });
  out.sort((x, y) => String(x.material_name).localeCompare(String(y.material_name), 'pt-BR'));
  return out;
}
