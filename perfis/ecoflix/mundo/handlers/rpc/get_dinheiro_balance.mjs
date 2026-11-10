// Cofre (conta DINHEIRO): saldo pela fórmula única (gaveta + perna banco), o que está reservado nos caixas abertos e o disponível.
import { cofre, saldoConta, saldoCaixa, r2 } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const comp = store.rows('companies').find((c) => c.id === cid);
  const conta = cofre(store, cid);
  if (!comp?.cash_account_enabled || !conta) return { enabled: false };
  const abertos = store.rows('cash_register').filter((r) => r.company_id === cid && r.status === 'open');
  const nomes = new Map(store.rows('profiles').map((p) => [p.id, p.full_name]));
  const caixas = abertos.map((r) => ({ register_id: r.id, operator_id: r.opened_by, operator_name: nomes.get(r.opened_by) || null, opening_balance: saldoCaixa(store, r), opened_at: r.opened_at }));
  const total = saldoConta(store, cid, conta);
  const reservado = r2(caixas.reduce((s, c) => s + c.opening_balance, 0));
  return { enabled: true, account_id: conta.id, currency: conta.currency || 'BRL', saldo_total: total, reservado_total: reservado, disponivel: r2(total - reservado), caixas_abertos: caixas };
};
