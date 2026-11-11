// update_employee_with_salary_adjustment ("Atualizar" do Editar Funcionário, T19 caps 3, 4 e 8), como a função da 1.59.154 (migration
// 20261028190000_employee_update_atomic_balance_and_rls.sql): só os campos permitidos; salário trocado grava o "ajuste"
// "Ajuste de salário: R$ <antigo> → R$ <novo>" (numeric::text, ex.: "R$ 2800 → R$ 2900") e soma a diferença ao último saldo.
// Devolve { employee_id, salary_changed, new_balance }.
import { agoraMs, num } from '../../lib/eco.mjs';

const CAMPOS = ['name', 'cpf', 'phone', 'email', 'position', 'salary', 'hire_date', 'address', 'pix_key', 'department_id', 'monthly_cost',
  'monthly_cost_breakdown', 'ponto_enabled', 'employment_regime', 'dependents_count', 'vt_enabled', 'vt_monthly_value',
  'payroll_schedule_id', 'salary_period', 'photo_url'];
const vazio = (v) => (v === '' || v === undefined ? null : v);

export default (a, { store, db, userId, RpcError }) => {
  const p = a.p_employee || {};
  const extras = Object.keys(p).filter((k) => !CAMPOS.includes(k)).sort();
  if (extras.length) throw new RpcError(`Campos não permitidos: ${extras.join(', ')}`);
  const emp = store.rows('employees').find((e) => e.id === a.p_employee_id);
  if (!emp) throw new RpcError('Funcionário não encontrado');
  if (!String(p.name || '').trim()) throw new RpcError('Nome do funcionário é obrigatório');
  const antigo = num(emp.salary);
  const novo = Number(p.salary);
  if (!(novo > 0)) throw new RpcError('Salário deve ser maior que zero');
  if (antigo !== num(a.p_expected_salary) && antigo !== novo) throw new RpcError('O salário foi alterado por outra sessão. Recarregue e tente novamente.');
  const movs = store.rows('employee_movements').filter((m) => m.employee_id === emp.id)
    .sort((x, y) => String(y.created_at).localeCompare(String(x.created_at)) || String(y.id).localeCompare(String(x.id)));
  const agora = new Date(agoraMs()).toISOString();
  let saldo;
  if (antigo !== novo) {
    saldo = (movs[0] ? num(movs[0].balance_after) : antigo) + (novo - antigo);
    db.insert('employee_movements', { employee_id: emp.id, company_id: emp.company_id, type: 'ajuste', amount: novo - antigo,
      description: `Ajuste de salário: R$ ${antigo} → R$ ${novo}`, balance_after: saldo, created_by: userId || null, created_at: agora, updated_at: agora },
    { companyId: emp.company_id });
  } else {
    saldo = movs[0] ? num(movs[0].balance_after) : novo;
  }
  Object.assign(emp, {
    name: String(p.name).trim(), cpf: vazio(p.cpf), phone: vazio(p.phone), email: vazio(p.email), position: vazio(p.position), salary: novo,
    hire_date: vazio(p.hire_date), address: vazio(p.address), pix_key: vazio(p.pix_key), department_id: vazio(p.department_id),
    ...('monthly_cost' in p ? { monthly_cost: p.monthly_cost } : {}), ...('monthly_cost_breakdown' in p ? { monthly_cost_breakdown: p.monthly_cost_breakdown } : {}),
    ...('ponto_enabled' in p ? { ponto_enabled: !!p.ponto_enabled } : {}), ...('employment_regime' in p ? { employment_regime: p.employment_regime || 'informal' } : {}),
    ...('dependents_count' in p ? { dependents_count: num(p.dependents_count) } : {}), ...('vt_enabled' in p ? { vt_enabled: !!p.vt_enabled } : {}),
    ...('vt_monthly_value' in p ? { vt_monthly_value: p.vt_monthly_value } : {}), ...('payroll_schedule_id' in p ? { payroll_schedule_id: vazio(p.payroll_schedule_id) } : {}),
    ...('salary_period' in p ? { salary_period: vazio(p.salary_period) } : {}), ...('photo_url' in p ? { photo_url: vazio(p.photo_url) } : {}),
    updated_at: agora,
  });
  store.table('employees').touch();
  return { employee_id: emp.id, salary_changed: antigo !== novo, new_balance: saldo };
};
