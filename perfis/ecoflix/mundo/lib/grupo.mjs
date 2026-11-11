// Gerencial (matriz e filiais, T22): contas das RPCs de grupo do EcoSistema 1.59.154, em memória. Cada função cita a migration de onde
// a regra saiu. Os números do grupo NUNCA são escritos: saem da soma das unidades (pedidos, lançamentos e movimentos de estoque).
import { r2, r3, num, agoraMs, diaBR, diaDe, lancamentosResultado } from './eco.mjs';

// ---------------------------------------------------------------- quem é quem
export const empresaDoUsuario = (store, userId) => store.rows('profiles').find((p) => p.id === userId)?.company_id || null;
export const grupoPorId = (store, gid) => store.rows('company_groups').find((g) => g.id === gid) || null;
export const nomeEmpresa = (store, cid) => store.rows('companies').find((c) => c.id === cid)?.name || null;

/** is_group_owner(auth.uid(), _group_id): a empresa do usuário é a dona do grupo */
export function ehDono(ctx, gid) {
  const g = grupoPorId(ctx.store, gid);
  return !!g && g.owner_company_id === empresaDoUsuario(ctx.store, ctx.userId);
}
export function exigeDono(ctx, gid) {
  if (!ehDono(ctx, gid)) throw new ctx.RpcError('Access denied', '42501', 403);
  return grupoPorId(ctx.store, gid);
}
/** membro ativo ou dono (RPCs que a filial também chama) */
export function exigeMembro(ctx, gid) {
  const cid = empresaDoUsuario(ctx.store, ctx.userId);
  if (!cid) throw new ctx.RpcError('Company not found');
  if (!empresasDoGrupo(ctx.store, gid).includes(cid)) throw new ctx.RpcError('Access denied - not a member of this group', '42501', 403);
  return cid;
}
/** get_group_company_ids(_group_id): a dona e os membros ativos (dona primeiro, depois na ordem de entrada) */
export function empresasDoGrupo(store, gid) {
  const g = grupoPorId(store, gid);
  if (!g) return [];
  const membros = store.rows('company_group_members').filter((m) => m.group_id === gid && m.status === 'active')
    .sort((a, b) => String(a.joined_at).localeCompare(String(b.joined_at)));
  return [...new Set([g.owner_company_id, ...membros.map((m) => m.company_id)])];
}
/** _company_ids do cliente: só empresas do grupo (a guarda de escopo das RPCs); vazio/nulo = o grupo todo */
export function escopo(ctx, gid, ids) {
  const todas = empresasDoGrupo(ctx.store, gid);
  if (!Array.isArray(ids) || !ids.length) return todas;
  if (ids.some((c) => !todas.includes(c))) throw new ctx.RpcError('Access denied', '42501', 403);
  return ids;
}
export const ordenaEmpresas = (store, ids) => [...ids];

// ---------------------------------------------------------------- datas (âncora de dia BRT, como as RPCs)
export const diaDoInstante = (iso) => diaBR(iso);
/** fim do dia BRT (23:59:59.999) em ms */
export const fimDoDia = (dia) => new Date(`${dia}T23:59:59.999-03:00`).getTime();
export const vespera = (dia) => {
  const t = new Date(`${dia}T12:00:00Z`);
  t.setUTCDate(t.getUTCDate() - 1);
  return t.toISOString().slice(0, 10);
};
const ms = (r) => new Date(r.transaction_at || r.created_at).getTime();

// ---------------------------------------------------------------- canonicalização de material (link → nome → próprio)
/** Map material_id -> { id, name, unit, code } do material canônico do grupo (get_group_stock_summary, 20261011202500) */
export function canonicos(store, gid, cids) {
  const gms = store.rows('group_materials').filter((g) => g.group_id === gid);
  const porId = new Map(gms.map((g) => [g.id, g]));
  const porNome = new Map();
  for (const g of gms) {
    const k = String(g.name).trim().toLowerCase();
    if (!porNome.has(k)) porNome.set(k, g);
  }
  const links = new Map();
  for (const l of store.rows('material_group_links')) {
    const g = porId.get(l.group_material_id);
    if (g && !links.has(l.company_material_id)) links.set(l.company_material_id, g);
  }
  const out = new Map();
  for (const m of store.rows('materials')) {
    if (!cids.includes(m.company_id) || m.is_archived) continue;
    const g = links.get(m.id) || porNome.get(String(m.name).trim().toLowerCase());
    out.set(m.id, g ? { id: g.id, name: g.name, unit: g.unit || m.unit || 'kg', code: g.code ?? m.code } : { id: m.id, name: m.name, unit: m.unit || 'kg', code: m.code });
  }
  return out;
}

// ---------------------------------------------------------------- estoque
/** _stock_balance_at_date_unchecked(p_company_id, p_at) (20261011202500): saldo = Σ stock_movements até o instante; custo médio = Σ valor /
 *  Σ quantidade líquida das compras concluídas (não estornadas nem canceladas) até o instante; sem compra o custo é 0 (é ele que acende o
 *  aviso "o CMV pode estar subestimado"). Só materiais ativos com saldo diferente de zero. */
export function saldoNaData(store, cid, atMs) {
  const saldo = new Map();
  for (const s of store.rows('stock_movements')) {
    if (s.company_id !== cid || ms(s) > atMs) continue;
    saldo.set(s.material_id, (saldo.get(s.material_id) || 0) + num(s.quantity));
  }
  const compras = new Set(store.rows('purchases').filter((p) => p.company_id === cid && p.status === 'completed' && !p.reverted_at && !p.cancelled_at
    && ms(p) <= atMs).map((p) => p.id));
  const acc = new Map();
  for (const it of store.rows('purchase_items')) {
    if (!compras.has(it.purchase_id)) continue;
    const a = acc.get(it.material_id) || { v: 0, q: 0 };
    a.v += num(it.total_price);
    a.q += num(it.quantity) - num(it.impurity);
    acc.set(it.material_id, a);
  }
  const out = [];
  for (const m of store.rows('materials')) {
    if (m.company_id !== cid || m.is_archived) continue;
    const s = saldo.get(m.id) || 0;
    if (Math.abs(s) < 1e-9) continue;
    const a = acc.get(m.id);
    out.push({ material_id: m.id, code: m.code, name: m.name, unit: m.unit, saldo: r3(s), avg_cost: a && a.q ? a.v / a.q : 0, sale_price: num(m.sale_price) });
  }
  return out.sort((x, y) => (Number(x.code) || 1e9) - (Number(y.code) || 1e9) || String(x.code).localeCompare(String(y.code)));
}
/** valor do estoque (Σ saldo × custo médio) e se o custo é confiável (nenhum saldo positivo com custo zero) */
export function valorNaData(store, cid, atMs) {
  const linhas = saldoNaData(store, cid, atMs);
  return { valor: linhas.reduce((s, l) => s + l.saldo * l.avg_cost, 0), confiavel: !linhas.some((l) => l.saldo > 0 && !l.avg_cost) };
}

// ---------------------------------------------------------------- dinheiro do Dashboard Gerencial
// get_group_financial_summary (20261011202500): os 4 critérios da DRE, verbatim, sobre cash_transactions e bank_transactions.
const low = (d) => String(d || '').toLowerCase();
function pagoFaturaDePedido(store, t) {
  for (const bp of store.rows('bill_payments')) {
    if (bp.cash_transaction_id !== t.id && bp.bank_transaction_id !== t.id) continue;
    const fb = store.rows('financial_bills').find((b) => b.id === bp.bill_id);
    if (fb && fb.order_id) return true;
  }
  return false;
}
const FATURA = (d) => d.startsWith('pagamento: fatura compra') || d.startsWith('pagamento: fatura venda') || d.startsWith('recebimento: fatura compra')
  || d.startsWith('recebimento: fatura venda');
function receita(store, t, caixa) {
  const d = low(t.description);
  if (t.type !== 'deposit' || !t.category_id || t.excluded_from_dre || pagoFaturaDePedido(store, t) || FATURA(d) || d.includes('estorno do pedido')) return false;
  if (caixa && t.reversal_for_order_id) return false;
  if (d.startsWith('saldo inicial')) return false;
  if (t.description == null || d.startsWith('diferença de caixa')) return true;
  return !(d.startsWith('valor recebido de ') || d.startsWith('venda #') || d.includes('venda (parcial)') || d.startsWith('baixa de saldo')
    || d.startsWith('cobrança de saldo') || d.includes('liquidação de') || d.includes('entrada no caixa') || d.includes('abastecimento')
    || d.includes('exclusão do pedido') || d.includes('movimentação realizada') || d.includes('caixa') || d.includes('ajuste') || d.includes('via pix')
    || d.includes('transferência'));
}
function despesaCorpo(t, d) {
  if (d.startsWith('saldo inicial')) return false;
  if (d.startsWith('compra #') || d.startsWith('compra (') || d.startsWith('valor pago a ') || d.startsWith('pagamento de saldo') || d.startsWith('adiantamento')
    || d.startsWith('liquidação de') || d.startsWith('pagamento excedente') || d.includes('exclusão do pedido')) return false;
  if (t.category_id || t.description == null || d.startsWith('diferença de caixa')) return true;
  return !(d.startsWith('baixa de saldo') || d.includes('saída do caixa') || d.includes('saque') || d.includes('transferência') || d.includes('ajuste'));
}
function despesa(store, t, caixa) {
  const d = low(t.description);
  if (!['withdrawal', 'expense'].includes(t.type) || t.excluded_from_dre || pagoFaturaDePedido(store, t) || FATURA(d) || d.includes('estorno do pedido')) return false;
  if (caixa) return !t.reversal_for_order_id && despesaCorpo(t, d);
  return t.credit_card_bill_date != null || despesaCorpo(t, d);
}
const entre = (t, d1, d2) => { const d = diaDe(t); return d >= d1 && d <= d2; };
/** uma linha do get_group_financial_summary para a empresa, no intervalo de dias [d1, d2] */
export function resumoFinanceiro(store, cid, d1, d2) {
  const ped = (tab) => r2(store.rows(tab).filter((p) => p.company_id === cid && p.status === 'completed' && !p.reverted_at && entre(p, d1, d2))
    .reduce((s, p) => s + num(p.total_amount), 0));
  const soma = (tab, fn) => r2(store.rows(tab).filter((t) => t.company_id === cid && entre(t, d1, d2) && fn(t)).reduce((s, t) => s + Math.abs(num(t.amount)), 0));
  const linha = {
    company_id: cid, company_name: nomeEmpresa(store, cid), total_sales: ped('sales'), total_purchases: ped('purchases'),
    total_cash_income: soma('cash_transactions', (t) => receita(store, t, true)), total_cash_expense: soma('cash_transactions', (t) => despesa(store, t, true)),
    total_bank_income: soma('bank_transactions', (t) => receita(store, t, false)), total_bank_expense: soma('bank_transactions', (t) => despesa(store, t, false)),
  };
  const base = store.rows('companies').find((c) => c.id === cid)?.base_currency || 'BRL';
  const { company_id: _a, company_name: _b, ...v } = linha;
  return { ...linha, currency: base, moedas: [base], moedas_misturadas: false, por_moeda: [{ currency: base, ...v }] };
}

// ---------------------------------------------------------------- DRE do grupo (get_group_financial_dre_summary, 20261014084500)
/** despesas e receitas da DRE por categoria, juntando as empresas pelo NOME (lower(btrim(nome))) */
export function categoriasDoGrupo(store, cids, d1, d2) {
  const cats = new Map(store.rows('financial_categories').map((c) => [c.id, c]));
  const j = { d1, d2 };
  const desp = new Map();
  const rec = new Map();
  for (const cid of cids) {
    for (const l of lancamentosResultado(store, cid, j)) {
      const cat = cats.get(l.category_id);
      if (l.natureza === 'income') {
        const nome = cat?.name || 'Outras Receitas';
        const k = nome.trim().toLowerCase();
        const e = rec.get(k) || { name: nome, value: 0, color: cat?.color || '#22C55E' };
        e.value += l.valor;
        rec.set(k, e);
      } else {
        const nome = cat?.name || 'Sem categoria';
        const imposto = nome.toLowerCase().includes('imposto');
        const k = `${nome.trim().toLowerCase()}|${imposto}`;
        const e = desp.get(k) || { name: nome, value: 0, color: cat?.color || '#6B7280', imposto };
        e.value += l.valor;
        desp.set(k, e);
      }
    }
  }
  const lista = (m, fn = () => true) => [...m.values()].filter(fn).map((e) => ({ name: e.name, value: r2(e.value), color: e.color })).sort((a, b) => b.value - a.value);
  return { operatingExpenses: lista(desp, (e) => !e.imposto), taxExpenses: lista(desp, (e) => e.imposto), revenueCategories: lista(rec) };
}

export const agora = () => agoraMs();
