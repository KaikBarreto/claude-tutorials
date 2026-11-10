// Aba "Operação" do Dashboard: contagens e pesos do período, volume das últimas 8 semanas, pedidos por dia e mapa de
// calor por dia da semana e hora (como a função SQL get_dashboard_operacao).
import { janela, pedidos, itensDe, num, r3, diaDe, horaBR, hojeBR, addDias } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const j = janela(a.p_start_date, a.p_end_date);
  const compras = pedidos(store, cid, 'purchase', j);
  const vendas = pedidos(store, cid, 'sale', j);
  const peso = (tipo, lista) => { let s = 0; for (const its of itensDe(store, tipo, lista).values()) for (const it of its) s += num(it.quantity); return s; };
  const pc = peso('purchase', compras), pv = peso('sale', vendas);
  const prod = store.rows('production_orders').filter((p) => p.company_id === cid && !['completed', 'cancelled', 'canceled'].includes(p.status || ''));
  const col = store.rows('collection_orders').filter((c) => c.company_id === cid && ['solicitada', 'agendada', 'a_caminho'].includes(c.status));
  const hoje = hojeBR();
  const kpis = {
    orderCount: compras.length + vendas.length, purchaseCount: compras.length, saleCount: vendas.length,
    totalWeightKg: r3(pc + pv), purchaseWeightKg: r3(pc), saleWeightKg: r3(pv),
    openProductions: prod.length, pendingCollections: col.length,
    employeesPresentToday: new Set(store.rows('time_records').filter((t) => t.company_id === cid && t.date === hoje && t.type === 'clock_in').map((t) => t.employee_id)).size,
  };
  // semanas (domingo a sábado): as 8 últimas até a semana de hoje
  const dow = new Date(`${hoje}T12:00:00Z`).getUTCDay();
  const ultima = addDias(hoje, -dow);
  const semanas = [];
  for (let i = 7; i >= 0; i--) semanas.push(addDias(ultima, -7 * i));
  const todasCompras = pedidos(store, cid, 'purchase');
  const itensTodas = itensDe(store, 'purchase', todasCompras);
  const weeklyVolume = semanas.map((ws) => {
    const fim = addDias(ws, 6);
    const lst = todasCompras.filter((p) => diaDe(p) >= ws && diaDe(p) <= fim);
    let w = 0;
    for (const p of lst) for (const it of itensTodas.get(p.id) || []) w += num(it.quantity);
    return { weekStart: ws, orders: lst.length, weightKg: r3(w) };
  });
  const ordersByDay = [];
  for (let d = j.d1; d <= j.d2 && d <= '2100-01-01'; d = addDias(d, 1)) {
    ordersByDay.push({ day: d, purchases: compras.filter((p) => diaDe(p) === d).length, sales: vendas.filter((p) => diaDe(p) === d).length });
    if (ordersByDay.length > 400) break;
  }
  const heat = new Map();
  for (const p of [...compras, ...vendas]) {
    const { dow: dw, hora } = horaBR(p.transaction_at || p.created_at);
    const k = `${dw}-${hora}`;
    heat.set(k, { dow: dw, hour: hora, count: (heat.get(k)?.count || 0) + 1 });
  }
  return {
    kpis, weeklyVolume, ordersByDay,
    ordersHeatmap: [...heat.values()].sort((x, y) => x.dow - y.dow || x.hour - y.hour),
    productionByStatus: [], collectionsByStatus: [], attendanceWeek: [],
  };
};
