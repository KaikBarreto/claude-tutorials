// update_bank_balance (useBankAccounts: depois de criar/editar conta): recalcula o total da empresa em bank_balance (soma das contas não
// arquivadas). O saldo de cada conta já sai da soma dos lançamentos pelos "triggers" de bank_transactions (lib/eco.mjs).
import { r2, num, contas } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const cid = a.p_company_id || ctx.companyId;
  const total = r2(contas(ctx.store, cid).reduce((s, b) => s + num(b.balance), 0));
  const atual = ctx.store.rows('bank_balance').find((b) => b.company_id === cid);
  if (atual) { atual.balance = total; atual.updated_at = new Date().toISOString(); ctx.store.table('bank_balance').touch(); return atual.id; }
  return ctx.db.insert('bank_balance', { company_id: cid, balance: total }, { companyId: cid }).id;
};
