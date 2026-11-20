// apply_balance_delta(p_company_id, p_entity_type, p_entity_id, p_delta, p_description): "Lançar crédito/débito" da conta-corrente
// (components/balance/BalanceEntryDialog.tsx; migration 20261001125000). SOMA o delta ao saldo do parceiro (convenção da própria perna:
// cliente + = ele me deve; fornecedor + = eu devo a ele) e grava um balance_movements `adjustment` com o motivo, SEM caixa, banco, pedido
// ou group_id (por isso a lixeira do extrato apaga pelo caminho "sem grupo": update_balance invertido + DELETE do movimento). Parceiro
// duplo vai para a linha `party` (lib/eco.mjs, atualizaSaldo). Devolve { changed, previous_balance, new_balance, delta }. T4 cap. 13.
import { inserir, atualizaSaldo, agoraMs, num, r2 } from '../../lib/eco.mjs';

export default (a, ctx) => {
  const { store, RpcError } = ctx;
  const cid = a.p_company_id || ctx.companyId;
  if (!['customer', 'supplier'].includes(a.p_entity_type)) throw new RpcError(`Tipo de parceiro inválido: ${a.p_entity_type}`, '22023');
  const delta = r2(num(a.p_delta));
  if (!delta) throw new RpcError('O valor do lançamento não pode ser zero.', '22023');
  const motivo = String(a.p_description || '').trim();
  if (motivo.length < 3) throw new RpcError('Informe o motivo do lançamento (mínimo 3 caracteres).', '22023');
  const tabela = a.p_entity_type === 'customer' ? 'customers' : 'suppliers';
  const parceiro = store.rows(tabela).find((x) => x.id === a.p_entity_id);
  if (!parceiro || parceiro.company_id !== cid) throw new RpcError('Parceiro não encontrado nesta empresa.', '42501');
  const antes = store.rows('balances').filter((b) => b.company_id === cid && b.entity_id === a.p_entity_id && b.entity_type === a.p_entity_type)[0];
  const anterior = antes ? num(antes.balance) : 0;
  const saldo = atualizaSaldo(ctx, cid, a.p_entity_type, a.p_entity_id, delta);
  inserir(ctx, 'balance_movements', {
    balance_id: saldo.id, company_id: cid, entity_type: a.p_entity_type, entity_id: a.p_entity_id, movement_type: 'adjustment', amount: delta,
    description: motivo, payment_method: null, created_by: ctx.userId, transaction_at: new Date(agoraMs()).toISOString(), is_settled: false,
  });
  return { changed: true, previous_balance: anterior, new_balance: num(saldo.balance), delta };
};
