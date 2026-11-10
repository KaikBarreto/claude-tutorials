// Compras e vendas por mês (últimos p_months até o mês de referência), para o gráfico do Dashboard.
import { pedidos, diaDe, num, r2, hojeBR } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const ref = String(a.p_reference_date || hojeBR()).slice(0, 7);
  const n = Number(a.p_months) || 6;
  let [y, m] = ref.split('-').map(Number);
  const meses = [];
  for (let i = 0; i < n; i++) {
    meses.unshift(`${y}-${String(m).padStart(2, '0')}`);
    m -= 1;
    if (m === 0) { m = 12; y -= 1; }
  }
  const soma = (tipo, mes) => r2(pedidos(store, cid, tipo).filter((p) => diaDe(p).startsWith(mes)).reduce((s, p) => s + num(p.total_amount), 0));
  return meses.map((mes) => {
    const purchases = soma('purchase', mes);
    const sales = soma('sale', mes);
    return {
      month_start: `${mes}-01`, purchases, sales, currency: 'BRL',
      purchases_by_currency: purchases ? [{ currency: 'BRL', total: purchases }] : [],
      sales_by_currency: sales ? [{ currency: 'BRL', total: sales }] : [],
    };
  });
};
