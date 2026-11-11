// RPC get_group_orders_payment_distribution (Relatório de Estoque do Gerencial): por tipo de pedido (compra/venda) do intervalo, quanto foi pago
// em dinheiro (cash_transactions do pedido), banco (bank_transactions do pedido) e saldo (balance_movements 'order'), e o total e a contagem.
import { empresaDoUsuario, empresasDoGrupo, diaDoInstante, fimDoDia, vespera } from '../../lib/grupo.mjs';
import { num, r2 } from '../../lib/eco.mjs';
export default (a, ctx) => {
  const { store } = ctx;
  const membros = empresasDoGrupo(store, a._group_id);
  if (!membros.length) return [];
  if (!membros.includes(empresaDoUsuario(store, ctx.userId))) throw new ctx.RpcError('Access denied', '42501', 403);
  const alvo = Array.isArray(a._company_ids) && a._company_ids.length ? membros.filter((c) => a._company_ids.includes(c)) : membros;
  const usuarios = Array.isArray(a._user_ids) && a._user_ids.length ? new Set(a._user_ids) : null;
  const abre = fimDoDia(vespera(diaDoInstante(a._start_date)));
  const fecha = fimDoDia(diaDoInstante(a._end_date));
  const out = [];
  for (const [tipo, tab] of [['purchase', 'purchases'], ['sale', 'sales']]) {
    const ped = store.rows(tab).filter((p) => {
      const t = new Date(p.transaction_at || p.created_at).getTime();
      return alvo.includes(p.company_id) && t > abre && t <= fecha && p.status === 'completed' && !p.reverted_at && (!usuarios || usuarios.has(p.created_by));
    });
    if (!ped.length) continue;
    const ids = new Set(ped.map((p) => p.id));
    const soma = (t, f = () => true) => r2(store.rows(t).filter((x) => ids.has(x.order_id) && f(x)).reduce((s, x) => s + Math.abs(num(x.amount)), 0));
    const cash = soma('cash_transactions');
    const bank = soma('bank_transactions');
    const bal = soma('balance_movements', (x) => x.movement_type === 'order');
    const tot = r2(ped.reduce((s, p) => s + num(p.total_amount), 0));
    out.push({ order_type: tipo, cash_total: cash, bank_total: bank, balance_total: bal, orders_total: tot, orders_count: ped.length, currency: 'BRL',
      cash_by_currency: cash ? [{ currency: 'BRL', total: cash }] : [], bank_by_currency: bank ? [{ currency: 'BRL', total: bank }] : [],
      balance_by_currency: bal ? [{ currency: 'BRL', total: bal }] : [], orders_by_currency: [{ currency: 'BRL', total: tot, count: ped.length }] });
  }
  return out;
};
