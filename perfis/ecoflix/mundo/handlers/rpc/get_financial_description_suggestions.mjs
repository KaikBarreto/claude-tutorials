// get_financial_description_suggestions(p_context, p_direction, p_prefix, p_limit) — app 1.60.10 ("preenchimento inteligente",
// 1.60.5 a 1.60.8), migration 20261117235000_cross_context_financial_suggestions.sql. O campo "Descrição" de Nova Despesa, Nova
// Receita (Caixa e Bancos) e Nova conta (Contas a Pagar e Receber) chama depois de 3 letras e mostra "Padrão encontrado: ...".
// Mesma régua da função SQL, sobre o próprio mundo (nada fixo aqui: o que aparece sai do histórico da semente):
//   fontes dos últimos 365 dias: contas (financial_bills da direção, vencidas até hoje, sem pedido e sem origem), lançamentos de caixa
//   (withdrawal para a pagar, deposit para a receber, sem pedido/estorno/funcionário/grupo) e de banco (type expense|income, manual,
//   sem pedido/funcionário/fatura de cartão/grupo); fora os que são perna de baixa de conta (bill_payments) ou de saldo de parceiro
//   (balance_movements) e as descrições de sistema (estorno, transferência interna, abertura/fechamento de caixa, tarifa:, juros:,
//   pagamento:); agrupa por descrição normalizada + categoria + parceiro + centro de custo + origem do pagamento; vale o grupo com 2
//   usos ou mais, ou o de descrição idêntica ao que foi digitado e usado nos últimos 90 dias; ordena por usos e data; até 3.
// No mundo base: "Gás da empilhadeira" (despesa em dinheiro, 4 usos, Combustível · Pátio, última em setembro de 2026) para a T06.
// As contas "Internet do escritório" (T13) e "Aluguel de caçamba" (T06) entram pela semente da aula; o conserto do pneu da T13 é o
// padrão que a T14 vê. Usado por T06, T13 e T14.
import { agoraMs, hojeBR, addDias } from '../../lib/eco.mjs';

const prefixo = (t) => String(t ?? '').slice(0, 240).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
const SISTEMA = /^(estorno|transferencia interna|abertura de caixa|fechamento de caixa|tarifa:|juros:|pagamento:)/;
const naoFalso = (v) => v !== false && v !== 'false';

export default (a, { store, companyId, RpcError }) => {
  if (!companyId) throw new RpcError('permission_denied');
  if (!['bill', 'movement'].includes(a.p_context) || !['payable', 'receivable'].includes(a.p_direction)) throw new RpcError('invalid_suggestion_context');
  const pre = prefixo(a.p_prefix);
  if (pre.replace(/[^a-z0-9]/g, '').length < 3) return [];
  const tipo = a.p_direction === 'payable' ? 'expense' : 'income';
  const agora = agoraMs();
  const hoje = hojeBR();
  const ha365 = agora - 365 * 86400000;
  const doCid = (t) => store.rows(t).filter((r) => r.company_id === companyId);
  const recente = (l, campo, n) => l.sort((x, y) => String(y[campo]).localeCompare(String(x[campo])) || String(y.id).localeCompare(String(x.id))).slice(0, n);

  const contas = recente(doCid('financial_bills').filter((b) => b.direction === a.p_direction && b.due_date >= addDias(hoje, -365) && b.due_date <= hoje
    && ['pending', 'partial', 'paid'].includes(b.status) && !b.source_type && !b.order_id && !b.is_projection), 'due_date', 1500)
    .map((b) => ({ id: b.id, source: 'bill', description: b.description, category_id: b.category_id || null, partner_type: b.partner_type || null, partner_id: b.partner_id || null,
      cost_center_id: b.cost_center_id || null, bank_account_id: b.expected_bank_account_id || null, payment_method: b.expected_payment_method || null, used_at: b.created_at }));
  const caixa = recente(doCid('cash_transactions').filter((c) => Date.parse(c.created_at) >= ha365 && c.type === (a.p_direction === 'payable' ? 'withdrawal' : 'deposit')
    && !c.order_id && !c.reversal_for_order_id && !c.employee_movement_id && !c.group_id && !c.voided), 'created_at', 1000)
    .map((c) => ({ id: c.id, source: 'cash', description: c.description, category_id: c.category_id || null, partner_type: c.partner_type || null, partner_id: c.partner_id || null,
      cost_center_id: c.cost_center_id || null, bank_account_id: null, payment_method: 'cash', used_at: c.created_at }));
  const banco = recente(doCid('bank_transactions').filter((b) => Date.parse(b.created_at) >= ha365 && b.type === tipo && !b.order_id && !b.employee_movement_id
    && !b.credit_card_bill_id && !b.group_id && !b.origin_company_id && b.source === 'manual' && !b.voided), 'created_at', 1000)
    .map((b) => ({ id: b.id, source: 'bank', description: b.description, category_id: b.category_id || null, partner_type: b.partner_type || null, partner_id: b.partner_id || null,
      cost_center_id: b.cost_center_id || null, bank_account_id: b.bank_account_id || null, payment_method: ['boleto', 'check'].includes(b.payment_method) ? b.payment_method : 'transfer', used_at: b.created_at }));

  const baixas = new Set();
  for (const p of doCid('bill_payments')) for (const k of ['cash_transaction_id', 'bank_transaction_id', 'fee_transaction_id', 'interest_transaction_id']) if (p[k]) baixas.add(p[k]);
  for (const m of doCid('balance_movements')) for (const k of ['cash_transaction_id', 'bank_transaction_id']) if (m[k]) baixas.add(m[k]);

  const cats = new Map(doCid('financial_categories').map((c) => [c.id, c]));
  const ccs = new Map(doCid('cost_centers').map((c) => [c.id, c]));
  const bancos = new Map(doCid('bank_accounts').map((b) => [b.id, b]));
  const parceiroDe = (r) => (r.partner_type === 'supplier' ? doCid('suppliers') : r.partner_type === 'customer' ? doCid('customers') : []).find((x) => x.id === r.partner_id) || null;
  const parceiroVale = (p) => p && naoFalso(p.is_active) && p.archived !== true && p.archived !== 'true' && !p.archived_at && !p.deleted_at;

  const validos = [];
  for (const r of [...contas, ...caixa, ...banco]) {
    const normal = prefixo(r.description);
    if (!normal.startsWith(pre) || SISTEMA.test(normal)) continue;
    if (r.source !== 'bill' && baixas.has(r.id)) continue;
    const c0 = r.category_id ? cats.get(r.category_id) : null;
    const c = c0 && c0.type === tipo ? c0 : null;
    const pai = c?.parent_id ? cats.get(c.parent_id) || null : null;
    const parc = r.partner_id ? parceiroDe(r) : null;
    const cc0 = r.cost_center_id ? ccs.get(r.cost_center_id) : null;
    const cc = cc0 && cc0.is_active !== false ? cc0 : null;
    const ba0 = r.bank_account_id ? bancos.get(r.bank_account_id) : null;
    const ba = ba0 && !ba0.is_archived && (ba0.kind || 'bank') !== 'card' ? ba0 : null;
    if (r.category_id && !(c && naoFalso(c.is_active) && (!c.parent_id || (pai && naoFalso(pai.is_active))))) continue;
    if (r.partner_id && !parceiroVale(parc)) continue;
    if (r.cost_center_id && !cc) continue;
    if (!(r.category_id || r.partner_id || r.cost_center_id || r.source === 'cash' || ba)) continue;
    validos.push({
      ...r, normal, category_label: [pai?.name, c?.name].filter(Boolean).join(' > '), partner_name: parc?.name || null, cost_center_name: cc?.name || null,
      payment_source: r.source === 'cash' ? '__cash__' : ba ? ba.id : null,
      valid_payment_method: r.source === 'cash' ? 'cash' : ba ? r.payment_method || 'transfer' : null, bank_account_name: ba?.name || null,
    });
  }
  const grupos = new Map();
  for (const v of validos) {
    const k = JSON.stringify([v.normal, v.category_id, v.category_label, v.partner_type, v.partner_id, v.cost_center_id, v.payment_source, v.valid_payment_method, v.bank_account_name]);
    if (!grupos.has(k)) grupos.set(k, []);
    grupos.get(k).push(v);
  }
  const ha90 = agora - 90 * 86400000;
  const nulosNoFim = (x, y) => (x === null) - (y === null) || String(x ?? '').localeCompare(String(y ?? ''));
  const linhas = [...grupos.values()].map((l) => {
    l.sort((x, y) => String(y.used_at).localeCompare(String(x.used_at)) || String(y.id).localeCompare(String(x.id)));
    const u = l[0];
    return {
      description: u.description, category_id: u.category_id, category_label: u.category_label, partner_type: u.partner_type, partner_id: u.partner_id,
      partner_name: u.partner_name, cost_center_id: u.cost_center_id, cost_center_name: u.cost_center_name, payment_source: u.payment_source,
      payment_method: u.valid_payment_method, bank_account_name: u.bank_account_name, usage_count: l.length, last_used: u.used_at, _normal: u.normal,
    };
  }).filter((g) => g.usage_count >= 2 || (g._normal === pre && Date.parse(g.last_used) >= ha90))
    .sort((x, y) => y.usage_count - x.usage_count || String(y.last_used).localeCompare(String(x.last_used)) || x._normal.localeCompare(y._normal)
      || nulosNoFim(x.category_id, y.category_id) || nulosNoFim(x.partner_id, y.partner_id) || nulosNoFim(x.cost_center_id, y.cost_center_id) || nulosNoFim(x.payment_source, y.payment_source));
  const limite = Math.max(1, Math.min(Number(a.p_limit ?? 3) || 3, 3));
  return linhas.slice(0, limite).map(({ _normal, ...g }) => g);
};
