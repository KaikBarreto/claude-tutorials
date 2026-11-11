// link_customer_supplier(p_company_id, p_customer_id, p_supplier_id): liga o cadastro de cliente ao de fornecedor (utils/dualEntityLink.ts;
// T4 cap05, "Também é cliente"). Grava o vínculo dos dois lados e junta os saldos numa linha só, a `party`, na convenção do cliente
// (entity_id = o cliente; positivo = ele deve à empresa): party = saldo do cliente − saldo do fornecedor. As linhas separadas saem.
import { num, r2, agoraMs } from '../../lib/eco.mjs';

export default (a, { store, db, companyId, RpcError }) => {
  const cid = a.p_company_id || companyId;
  const c = store.rows('customers').find((x) => x.id === a.p_customer_id && x.company_id === cid);
  const s = store.rows('suppliers').find((x) => x.id === a.p_supplier_id && x.company_id === cid);
  if (!c || !s) throw new RpcError('Cliente ou fornecedor não encontrado nesta empresa');
  const agora = new Date(agoraMs()).toISOString();
  c.linked_supplier_id = s.id;
  s.linked_customer_id = c.id;
  c.updated_at = agora;
  s.updated_at = agora;
  store.table('customers').touch();
  store.table('suppliers').touch();
  const bs = store.rows('balances').filter((b) => b.company_id === cid);
  const bc = bs.find((b) => b.entity_type === 'customer' && b.entity_id === c.id);
  const bf = bs.find((b) => b.entity_type === 'supplier' && b.entity_id === s.id);
  let party = bs.find((b) => b.entity_type === 'party' && b.entity_id === c.id);
  const total = r2(num(party?.balance) + num(bc?.balance) - num(bf?.balance));
  if (party) {
    party.balance = total;
    party.updated_at = agora;
    store.table('balances').touch();
  } else {
    party = db.insert('balances', { company_id: cid, entity_type: 'party', entity_id: c.id, balance: total, currency: 'BRL' }, { companyId: cid });
  }
  const fora = new Set([bc?.id, bf?.id].filter(Boolean));
  if (fora.size) db.remove('balances', (b) => fora.has(b.id));
  return { success: true, party_balance_id: party.id, balance: total };
};
