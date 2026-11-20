// set_ponto_pin (EmployeeFormDialog.tsx, "Definir PIN"/"Trocar PIN"/"Remover PIN", T19 cap11), como a função da 1.59.154
// (migration 20260903235900_ponto_kiosk_e_pin.sql): p_pin texto de 4 ou 6 dígitos grava o PIN do funcionário; p_pin nulo remove.
// No banco falso o "hash" é o PIN com um prefixo (nada de segredo real: o PIN da aula é fictício) e o edge time-clock-portal confere
// pelo mesmo prefixo (verify_ponto_pin).
export default (a, { store, db, RpcError }) => {
  const emp = store.rows('employees').find((e) => e.id === a.p_employee_id);
  if (!emp) throw new RpcError('Funcionário não encontrado');
  const pin = a.p_pin;
  const atual = store.rows('employee_ponto_pins').find((p) => p.employee_id === emp.id);
  if (pin === null || pin === undefined || pin === '') {
    if (atual) db.remove('employee_ponto_pins', (p) => p.employee_id === emp.id);
  } else {
    if (!/^(\d{4}|\d{6})$/.test(String(pin))) throw new RpcError('O PIN precisa ter 4 ou 6 dígitos.');
    const agora = new Date().toISOString();
    if (atual) Object.assign(atual, { pin_hash: `falso:${pin}`, failed_count: 0, locked_until: null, set_at: agora });
    else db.insert('employee_ponto_pins', { company_id: emp.company_id, employee_id: emp.id, pin_hash: `falso:${pin}`, failed_count: 0, locked_until: null, set_at: agora }, { companyId: emp.company_id });
  }
  store.table('employee_ponto_pins').touch();
  return null;
};
