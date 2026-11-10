// Produção (T11): o motor de postagem das ordens de produção, como as funções SQL do EcoSistema 1.59.154
// (supabase/migrations do commit da versão publicada): _post_production_stock (20260911150200), _recalc_production_order_totals
// e _sync_entry_workers (20260829120100 / 20260829130000), o estorno de delete_production_order_atomic (20260829130100).
// Usado pelos handlers handlers/rpc/{add_production_entry_atomic,finalize_production_order_atomic,delete_production_order_atomic}.
import { r2, num, agoraMs, inserir, custoMedio, pedidos, itensDe, liquido, diaDe } from './eco.mjs';

const agoraIso = () => new Date(agoraMs()).toISOString();
const r4 = (n) => Math.round((Number(n) || 0) * 10000) / 10000;
const r3 = (n) => Math.round((Number(n) || 0) * 1000) / 1000;
const r6 = (n) => Math.round((Number(n) || 0) * 1e6) / 1e6; // o numeric do banco: 18714,08 / 3018,4 = 6,2 (sem o 6,1999999 do ponto flutuante)

export const empresaDe = (store, cid) => store.rows('companies').find((c) => c.id === cid) || {};

/** Custo do insumo pela régua da empresa (get_material_cost_with_basis / _material_cost_with_basis_unchecked):
 *  régua (media_historica | media_janela | ultima_compra) -> média histórica -> última compra -> purchase_price -> zero.
 *  Média = SUM(total_price) / SUM(quantity - impurity) das compras concluídas. */
export function custoComRegua(store, cid, materialId) {
  const comp = empresaDe(store, cid);
  const regua = ['media_janela', 'ultima_compra'].includes(comp.production_cost_basis) ? comp.production_cost_basis : 'media_historica';
  const compras = pedidos(store, cid, 'purchase');
  const itens = [];
  for (const [pid, lst] of itensDe(store, 'purchase', compras)) {
    const p = compras.find((x) => x.id === pid);
    for (const it of lst) if (it.material_id === materialId && liquido(it) > 0) itens.push({ ...it, _at: p?.transaction_at || '', _dia: diaDe(p || {}) });
  }
  const media = (lst) => {
    const q = lst.reduce((s, it) => s + liquido(it), 0);
    return q > 0 ? lst.reduce((s, it) => s + num(it.total_price), 0) / q : null;
  };
  const ultima = () => {
    const u = [...itens].sort((a, b) => String(b._at).localeCompare(String(a._at)))[0];
    return u ? num(u.total_price) / liquido(u) : null;
  };
  const fim = (r) => ({ ...r, cost: r6(r.cost) });
  let v = null;
  if (regua === 'media_janela') {
    const dias = num(comp.production_cost_window_days) || 90;
    const lim = new Date(agoraMs() - dias * 86400000).toISOString().slice(0, 10);
    v = media(itens.filter((it) => it._dia >= lim));
  } else if (regua === 'ultima_compra') v = ultima();
  else v = media(itens);
  if (v != null) return fim({ cost: v, basis_used: regua, is_fallback: false });
  const hist = media(itens);
  if (hist != null) return fim({ cost: hist, basis_used: 'media_historica', is_fallback: true });
  const ult = ultima();
  if (ult != null) return fim({ cost: ult, basis_used: 'ultima_compra', is_fallback: true });
  const m = store.rows('materials').find((x) => x.id === materialId && x.company_id === cid);
  if (num(m?.purchase_price) > 0) return fim({ cost: num(m.purchase_price), basis_used: 'preco_cadastro', is_fallback: true });
  return { cost: 0, basis_used: 'zero', is_fallback: true };
}

/** _post_production_stock: baixa os insumos (real), dá entrada nas saídas, grava consumo/saídas com custo. */
export function postarProducao(ctx, ordem, entryId, consumo, saidas) {
  const { store, db, RpcError, userId } = ctx;
  const cid = ordem.company_id;
  const comp = empresaDe(store, cid);
  const bloqueia = !!comp.production_block_on_insufficient_stock;
  const creditaCoproduto = !!comp.production_coproduct_credits_cost;
  const cm = custoMedio(store, cid);
  const agora = agoraIso();
  let total = 0;
  let credito = 0;
  const movimentos = [];
  const material = (id) => store.rows('materials').find((x) => x.id === id && x.company_id === cid);
  for (const c of Array.isArray(consumo) ? consumo : []) {
    const mid = c.material_id;
    const teo = num(c.theoretical_qty);
    const real = num(c.actual_qty);
    const motivo = c.loss_reason ? String(c.loss_reason) : null;
    if (real < 0) throw new RpcError('Consumo real negativo não permitido');
    const m = material(mid);
    if (!m) throw new RpcError(`Insumo ${mid} não encontrado nesta empresa`);
    const antes = num(m.current_stock);
    if (bloqueia && antes < real) throw new RpcError(`Estoque insuficiente de ${m.name} (tem ${antes}, precisa ${real})`);
    const depois = r3(antes - real);
    const unit = r6(cm.get(mid) || 0); // multinível desligado no mundo (custo de compra)
    const linha = r2(real * unit);
    total += linha;
    if (real !== 0) {
      m.current_stock = depois;
      m.updated_at = agora;
      store.table('materials').touch();
      const mv = inserir(ctx, 'stock_movements', {
        company_id: cid, material_id: mid, type: 'PRODUCAO', quantity: -real, stock_before: antes, stock_after: depois,
        description: 'Consumo de produção (lançamento)', order_id: ordem.id, order_type: 'production', entry_id: entryId, created_by: userId, transaction_at: agora,
      });
      movimentos.push(mv.id);
    }
    db.insert('production_order_consumption', {
      production_order_id: ordem.id, entry_id: entryId, company_id: cid, material_id: mid, theoretical_qty: teo, actual_qty: real,
      unit_cost: unit, line_cost: linha, loss_qty: r3(real - teo), loss_reason: motivo, created_at: agora,
    }, { companyId: cid });
  }
  for (const o of Array.isArray(saidas) ? saidas : []) {
    const mid = o.material_id;
    const qtd = num(o.qty);
    const principal = !!o.is_primary;
    if (qtd <= 0) continue;
    const m = material(mid);
    if (!m) throw new RpcError(`Produto de saída ${mid} não encontrado nesta empresa`);
    if (creditaCoproduto && !principal) credito += r2(qtd * (cm.get(mid) || 0));
    const antes = num(m.current_stock);
    const depois = r3(antes + qtd);
    m.current_stock = depois;
    m.updated_at = agora;
    store.table('materials').touch();
    const mv = inserir(ctx, 'stock_movements', {
      company_id: cid, material_id: mid, type: 'PRODUCAO', quantity: qtd, stock_before: antes, stock_after: depois,
      description: principal ? 'Produto de produção (lançamento)' : 'Coproduto de produção (lançamento)', order_id: ordem.id, order_type: 'production',
      entry_id: entryId, created_by: userId, transaction_at: agora,
    });
    movimentos.push(mv.id);
    db.insert('production_order_outputs', {
      production_order_id: ordem.id, entry_id: entryId, company_id: cid, material_id: mid, is_primary: principal, qty: qtd, created_at: agora,
    }, { companyId: cid });
  }
  const bruto = total;
  let travado = false;
  if (credito !== 0) {
    total -= credito;
    if (total < 0) { total = 0; travado = true; }
  }
  return { total_material_cost: r2(total), gross_material_cost: r2(bruto), coproduct_credit: r2(credito), credit_clamped: travado, movement_ids: movimentos };
}

/** _sync_entry_workers: uma linha por funcionário POR lançamento; a soma tem de bater com o produzido do dia. */
export function sincronizaEquipeDoDia(ctx, ordem, entryId, trabalhadores, produzido) {
  const { db, RpcError } = ctx;
  const lista = Array.isArray(trabalhadores) ? trabalhadores : [];
  db.remove('production_order_workers', (w) => w.entry_id === entryId);
  if (!lista.length) return num(produzido);
  const soma = lista.reduce((s, w) => s + num(w.produced_qty), 0);
  if (produzido != null && Math.abs(soma - num(produzido)) > 0.001) {
    throw new RpcError(`Soma da produção por funcionário (${soma}) difere do produzido do dia (${produzido})`);
  }
  for (const w of lista) {
    if (!w.employee_id) throw new RpcError('Funcionário sem identificação no lançamento');
    if (num(w.produced_qty) < 0) throw new RpcError('Produção por funcionário negativa não permitida');
    db.insert('production_order_workers', {
      order_id: ordem.id, entry_id: entryId, employee_id: w.employee_id, company_id: ordem.company_id, produced_qty: num(w.produced_qty), created_at: agoraIso(),
    }, { companyId: ordem.company_id });
  }
  return soma;
}

/** _recalc_production_order_totals: produzido = soma dos lançamentos; custo = soma dos postados; custo por unidade (4 casas). */
export function recalculaTotais(ctx, ordem) {
  const { store } = ctx;
  const lanc = store.rows('production_order_entries').filter((e) => e.production_order_id === ordem.id);
  const produzido = lanc.reduce((s, e) => s + num(e.produced_qty), 0);
  const custo = lanc.filter((e) => e.posted).reduce((s, e) => s + num(e.total_material_cost), 0);
  ordem.produced_qty = r3(produzido);
  ordem.total_material_cost = r2(custo);
  ordem.cost_per_unit = produzido > 0 ? r4(custo / produzido) : null;
  ordem.updated_at = agoraIso();
  store.table('production_orders').touch();
}

/** Estorno de delete_production_order_atomic: o inverso de cada movimento PRODUCAO original da OP ainda não estornado. */
export function estornaOrdem(ctx, ordem) {
  const { store, RpcError, userId } = ctx;
  const cid = ordem.company_id;
  const todos = store.rows('stock_movements');
  const originais = todos
    .filter((sm) => sm.order_id === ordem.id && sm.order_type === 'production' && sm.type === 'PRODUCAO' && sm.company_id === cid && !sm.related_movement_id
      && !todos.some((r) => r.related_movement_id === sm.id))
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)) || String(a.id).localeCompare(String(b.id)));
  const agora = agoraIso();
  for (const mv of originais) {
    const m = store.rows('materials').find((x) => x.id === mv.material_id && x.company_id === cid);
    if (!m) throw new RpcError(`Material ${mv.material_id} da OP não encontrado nesta empresa`);
    const antes = num(m.current_stock);
    const depois = r3(antes - num(mv.quantity));
    m.current_stock = depois;
    m.updated_at = agora;
    store.table('materials').touch();
    inserir(ctx, 'stock_movements', {
      company_id: cid, material_id: mv.material_id, type: 'PRODUCAO', quantity: -num(mv.quantity), stock_before: antes, stock_after: depois,
      description: 'Estorno de produção (exclusão da OP)', order_id: ordem.id, order_type: 'production', entry_id: mv.entry_id || null,
      related_movement_id: mv.id, created_by: userId, transaction_at: agora,
    });
  }
  return originais.length > 0;
}
