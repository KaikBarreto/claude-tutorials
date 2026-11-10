// RPC registrar_compra_material_direta(p_client_request_id, p_stock_id, p_supplier_id, p_items, p_purchase_date, p_account_id, p_category_id,
//   p_is_paid, p_paid_date, p_due_date, p_payment_method, p_description, p_notes) → jsonb
// 20261018005000_compra_direta_estoque_financeiro.sql:137-540 (T13, cap. 5). Numa operação só: compra 'compra_direta' já 'concluida', uma ordem
// de compra interna 'enviada' (com o fornecedor), os materiais e itens da ordem, a ENTRADA no estoque pelo caminho de `receber_ordem_compra`
// e UMA despesa no Financeiro (paga na data informada, ou a pagar com vencimento), amarrada à ordem. Retry com o mesmo client_request_id devolve
// o mesmo resultado (`already_applied: true`). Validações do banco que a tela pode provocar: itens, conta que não é cartão, categoria de saída.
import { RpcError } from '../../http/rest.mjs';
import { nextSeq } from '../../core/defaults.mjs';
import { nowIso } from '../../core/util.mjs';
import receberOrdemCompra from './receber_ordem_compra.mjs';

const r2 = (n) => Math.round(Number(n) * 100) / 100;

export default async function registrarCompraMaterialDireta(a, ctx) {
  const { userId, db } = ctx;
  const itens = Array.isArray(a.p_items) ? a.p_items : [];
  if (!a.p_client_request_id || !a.p_stock_id || !a.p_supplier_id || !a.p_purchase_date || !a.p_account_id || !a.p_category_id || a.p_is_paid === null || a.p_is_paid === undefined) {
    throw new RpcError('Informe fornecedor, local, data, conta, categoria e chave da operação', '22023');
  }
  if (!itens.length) throw new RpcError('Informe ao menos um material comprado', '22023');
  const total = r2(itens.reduce((s, i) => s + Number(i.quantity) * Number(i.unit_price), 0));
  if (!(total > 0)) throw new RpcError('O total da compra deve ser maior que zero', '22023');
  if (a.p_is_paid && !a.p_payment_method) throw new RpcError('Informe a forma de pagamento', '22023');
  if (!a.p_is_paid && !a.p_due_date) throw new RpcError('Informe o vencimento da conta a pagar', '22023');

  const ja = db.first('compras', (c) => c.client_request_id === a.p_client_request_id);
  if (ja) {
    const o = db.first('compra_ordens', { compra_id: ja.id });
    return { compra_id: ja.id, numero: ja.numero, ordem_id: o?.id ?? null, financial_transaction_id: o?.financial_transaction_id ?? null, total_amount: total, already_applied: true };
  }
  const stock = db.first('stocks', { id: a.p_stock_id });
  if (!stock || stock.customer_id) throw new RpcError('Local de estoque inválido ou sem acesso', '42501');
  const forn = db.first('suppliers', { id: a.p_supplier_id });
  if (!forn) throw new RpcError('Fornecedor inválido para esta empresa', '42501');
  const conta = db.first('financial_accounts', { id: a.p_account_id });
  if (!conta || conta.is_active === false) throw new RpcError('Conta financeira inválida para esta empresa', '42501');
  if (conta.type === 'cartao') throw new RpcError('Compra direta no cartão de crédito ainda não é suportada; lance pelo Financeiro para gerar a fatura', '22023');
  const cat = db.first('financial_categories', { id: a.p_category_id });
  if (!cat || cat.type !== 'saida' || cat.is_active === false) throw new RpcError('Categoria financeira inválida para esta empresa', '42501');
  for (const i of itens) {
    const inv = db.first('inventory', { id: i.inventory_id });
    if (!inv || inv.customer_id || inv.archived_at) throw new RpcError('Há material inválido, arquivado ou de outro estoque/tenant', '42501');
  }

  const company = stock.company_id;
  const titulo = (a.p_description || '').trim() || `Compra de materiais — ${forn.name}`;
  const compra = db.insert('compras', {
    company_id: company, title: titulo, status: 'concluida', notes: (a.p_notes || '').trim() || null, created_by: userId, stock_id: a.p_stock_id,
    flow_type: 'compra_direta', client_request_id: a.p_client_request_id, request_hash: a.p_client_request_id, purchase_date: a.p_purchase_date,
    numero: nextSeq('compras', 'numero', db.rows('compras')),
  });
  const ordem = db.insert('compra_ordens', {
    company_id: company, compra_id: compra.id, supplier_id: a.p_supplier_id, status: 'enviada', sent_at: nowIso(),
    notes: 'Comprovante interno de compra direta', created_by: userId, numero: nextSeq('compra_ordens', 'numero', db.rows('compra_ordens')),
  });
  const recibo = [];
  for (const i of [...itens].sort((x, y) => String(x.inventory_id).localeCompare(String(y.inventory_id)))) {
    const inv = db.first('inventory', { id: i.inventory_id });
    const un = (inv.unit || '').trim() || 'un';
    const cm = db.insert('compra_materiais', { company_id: company, compra_id: compra.id, inventory_id: inv.id, material_name: inv.name, unit: un, quantity: Number(i.quantity) });
    const oi = db.insert('compra_ordem_itens', {
      company_id: company, ordem_id: ordem.id, compra_material_id: cm.id, inventory_id: inv.id, material_name: inv.name, unit: un,
      quantity_ordered: Number(i.quantity), quantity_received: 0, unit_price: r2(i.unit_price),
    });
    recibo.push({ item_id: oi.id, quantity: Number(i.quantity) });
  }
  await receberOrdemCompra({ p_ordem_id: ordem.id, p_itens: recibo }, ctx);

  const fin = db.insert('financial_transactions', {
    company_id: company, transaction_type: 'saida', category: cat.name, description: titulo, amount: total, transaction_date: a.p_purchase_date,
    due_date: a.p_is_paid ? null : a.p_due_date, paid_date: a.p_is_paid ? a.p_paid_date : null, is_paid: !!a.p_is_paid, supplier_id: a.p_supplier_id,
    account_id: a.p_account_id, payment_method: (a.p_payment_method || '').trim() || null, notes: (a.p_notes || '').trim() || null, created_by: userId,
    amount_received: 0,
  });
  db.update('compra_ordens', { id: ordem.id }, { financial_transaction_id: fin.id });
  return { compra_id: compra.id, numero: compra.numero, ordem_id: ordem.id, financial_transaction_id: fin.id, total_amount: total, already_applied: false };
}
