// RPC create_employee_vale(p_employee_id, p_account_id, p_amount, p_idempotency_key, p_transaction_date, p_description, p_cost_center_id)
//   → TABLE(employee_movement_id, financial_transaction_id, created)   · 20260922120000_employee_vale_atomico.sql:492-717 (T15, cap. 6)
// Vale mexe nos DOIS livros na mesma operação: a saída PAGA "Vale - {nome}" na conta escolhida (categoria "Funcionários", payroll_kind 'vale')
// e o movimento `vale` do extrato do funcionário (balance_after = saldo anterior - valor; sem movimento antes, parte do salário).
// Idempotente pela chave: a mesma chave devolve o par já criado (`created: false`). Recusas do banco, em PT-BR (o app repassa).
// Também fixa o DEFAULT de `employee_movements.movement_order` (sequência do banco): o bônus e a falta entram por INSERT direto do app
// e o extrato ordena por esse número (sem isto todos nasceriam com 0 e a ordem do extrato ficaria ao acaso).
import { RpcError } from '../../http/rest.mjs';
import { db } from '../../core/db.mjs';
import { TABLE_DEFAULTS, nextSeq } from '../../core/defaults.mjs';
import { now } from '../../core/util.mjs';

TABLE_DEFAULTS.employee_movements = {
  ...(TABLE_DEFAULTS.employee_movements || {}),
  movement_order: () => nextSeq('employee_movements', 'movement_order', db.rows('employee_movements')),
};

export default async function createEmployeeVale(a, { userId, db: dbx = db }) {
  const valor = Number(a.p_amount);
  if (!a.p_idempotency_key || !a.p_employee_id || !a.p_account_id || !a.p_transaction_date || !(valor > 0)) {
    throw new RpcError('Funcionário, conta, data, chave idempotente e valor positivo são obrigatórios', '22023');
  }
  const ja = dbx.first('employee_movements', { idempotency_key: a.p_idempotency_key });
  if (ja) return [{ employee_movement_id: ja.id, financial_transaction_id: ja.financial_transaction_id, created: false }];

  const emp = dbx.first('employees', { id: a.p_employee_id });
  if (!emp) throw new RpcError('Funcionário não encontrado', '22023');
  if (emp.is_active !== true) throw new RpcError('Funcionário inativo não pode receber vale', '22023');
  const conta = dbx.first('financial_accounts', { id: a.p_account_id });
  if (!conta) throw new RpcError('Conta financeira não encontrada', '22023');
  if (conta.is_active !== true || conta.type === 'cartao') throw new RpcError('Vale exige conta caixa ou banco ativa', '22023');

  const anteriores = dbx.find('employee_movements', { employee_id: emp.id });
  anteriores.sort((x, y) => Number(x.movement_order) - Number(y.movement_order));
  const anterior = anteriores.length ? Number(anteriores[anteriores.length - 1].balance_after) : Number(emp.salary || 0);

  const fin = dbx.insert('financial_transactions', {
    transaction_type: 'saida', category: 'Funcionários', description: `Vale - ${emp.name}`, amount: valor,
    transaction_date: a.p_transaction_date, paid_date: a.p_transaction_date, due_date: a.p_transaction_date, is_paid: true,
    notes: a.p_description ?? null, account_id: a.p_account_id, created_by: userId, company_id: emp.company_id,
    employee_id: emp.id, payroll_kind: 'vale', cost_center_id: a.p_cost_center_id ?? null, created_at: now().toISOString(),
  });
  const mov = dbx.insert('employee_movements', {
    employee_id: emp.id, type: 'vale', amount: valor, balance_after: Math.round((anterior - Math.abs(valor)) * 100) / 100,
    description: a.p_description ?? null, payment_method: String(a.p_account_id), created_by: userId,
    financial_transaction_id: fin.id, idempotency_key: a.p_idempotency_key,
  });
  return [{ employee_movement_id: mov.id, financial_transaction_id: fin.id, created: true }];
}
