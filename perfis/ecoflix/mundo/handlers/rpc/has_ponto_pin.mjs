// has_ponto_pin (EmployeeFormDialog.tsx, ao abrir o cadastro): true se o funcionário tem PIN do ponto (employee_ponto_pins), como a
// função da 1.59.154 (migration 20260903235900_ponto_kiosk_e_pin.sql). Na Recicla Vale Metais ninguém tem PIN (T19 cap08).
export default (a, { store }) => store.rows('employee_ponto_pins').some((p) => p.employee_id === a.p_employee_id && p.pin_hash);
