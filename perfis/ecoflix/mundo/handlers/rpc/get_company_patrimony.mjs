// Patrimônio (Relatório Financeiro): dinheiro (cofre, ou o dos caixas abertos), bancos, a receber e a pagar (saldos de
// parceiro), dívida de cartão e estoque a preço de venda.
import { contas, saldoConta, saldoCaixa, num, r2 } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const cs = contas(store, cid);
  const cofre = cs.filter((b) => b.kind === 'cash');
  const abertos = store.rows('cash_register').filter((r) => r.company_id === cid && r.status === 'open');
  const cash = cofre.length ? cofre.reduce((s, b) => s + saldoConta(store, cid, b), 0) : abertos.reduce((s, r) => s + saldoCaixa(store, r), 0);
  const bank = cs.filter((b) => b.kind === 'bank').reduce((s, b) => s + saldoConta(store, cid, b), 0);
  const card = cs.filter((b) => b.kind === 'card' && saldoConta(store, cid, b) < 0).reduce((s, b) => s + Math.abs(saldoConta(store, cid, b)), 0);
  let rec = 0, pag = 0;
  for (const b of store.rows('balances').filter((x) => x.company_id === cid)) {
    const v = num(b.balance);
    if ((b.entity_type === 'customer' || b.entity_type === 'party') && v > 0) rec += v;
    if (b.entity_type === 'supplier' && v < 0) rec += -v;
    if (b.entity_type === 'supplier' && v > 0) pag += v;
    if ((b.entity_type === 'customer' || b.entity_type === 'party') && v < 0) pag += -v;
  }
  const estoque = store.rows('materials').filter((m) => m.company_id === cid && !m.is_archived).reduce((s, m) => s + num(m.current_stock) * num(m.sale_price), 0);
  const base = { cashBalance: r2(cash), bankBalance: r2(bank), cardDebt: r2(card), receivables: r2(rec), payables: r2(pag), stockValue: r2(estoque) };
  return { ...base, moeda_escopo: 'BRL', moedas_misturadas: false, por_moeda: [{ currency: 'BRL', ...base, cashBalanceFonte: cofre.length ? 'cofre' : 'caixas', saldo_parceiro_moeda_presumida: true }] };
};
