// Evolução mensal (Relatório Financeiro): vendas, compras, despesas (saídas categorizadas), resultado e margem bruta.
import { pedidos, diaDe, num, r2, hojeBR } from '../../lib/eco.mjs';
const MES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const FORA = /^(valor pago a |compra #|pagamento - |vale - |baixa de saldo - )|compra \(parcial\)|liquidação de|saída do caixa|saque|transferência/i;
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const n = Number(a.p_months) || 6;
  let [y, m] = hojeBR().split('-').map(Number);
  const meses = [];
  for (let i = 0; i < n; i++) { meses.unshift([y, m]); m -= 1; if (m === 0) { m = 12; y -= 1; } }
  const saida = (r) => r.type === 'withdrawal' && !r.order_id && !r.excluded_from_dre && (r.category_id || !r.description || !FORA.test(r.description));
  return meses.map(([yy, mm]) => {
    const pre = `${yy}-${String(mm).padStart(2, '0')}`;
    const vendas = r2(pedidos(store, cid, 'sale').filter((p) => diaDe(p).startsWith(pre)).reduce((s, p) => s + num(p.total_amount), 0));
    const compras = r2(pedidos(store, cid, 'purchase').filter((p) => diaDe(p).startsWith(pre)).reduce((s, p) => s + num(p.total_amount), 0));
    let despesas = 0;
    for (const t of ['cash_transactions', 'bank_transactions']) for (const r of store.rows(t)) if (r.company_id === cid && diaDe(r).startsWith(pre) && saida(r)) despesas += Math.abs(num(r.amount));
    despesas = r2(despesas);
    const bruto = vendas - compras;
    const linha = { vendas, compras, despesas, resultado: r2(bruto - despesas), margemBruta: vendas > 0 ? r2((bruto / vendas) * 100) : 0 };
    return { month: `${MES[mm - 1]}/${String(yy).slice(2)}`, ...linha, moeda_escopo: 'BRL', moedas: ['BRL'], moedas_misturadas: false, por_moeda: [{ currency: 'BRL', ...linha }] };
  });
};
