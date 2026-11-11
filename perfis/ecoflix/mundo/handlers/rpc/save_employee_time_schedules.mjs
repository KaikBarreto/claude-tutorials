// save_employee_time_schedules ("Salvar jornada" da Jornada Individual, T19 cap11), como a função da 1.59.154 (migration
// 20261105112058_ponto_salva_jornada_e_recalcula_espelhos.sql): grava os sete dias (upsert por funcionário e dia da semana) e devolve
// quantas folhas existentes do funcionário foram recalculadas (a Juliana liga o ponto hoje e não tem folha: 0).
import { agoraMs } from '../../lib/eco.mjs';

export default (a, { store, db, RpcError }) => {
  const emp = store.rows('employees').find((e) => e.id === a.p_employee_id);
  if (!emp) throw new RpcError('Funcionário não encontrado');
  const dias = Array.isArray(a.p_schedules) ? a.p_schedules : [];
  const sem = new Set(dias.map((d) => Number(d.weekday)));
  if (dias.length !== 7 || sem.size !== 7 || dias.some((d) => !(d.weekday >= 0 && d.weekday <= 6) || !d.expected_in || !d.expected_out || d.is_work_day == null)) {
    throw new RpcError('Jornada inválida: informe cada dia da semana uma única vez');
  }
  const agora = new Date(agoraMs()).toISOString();
  for (const d of dias) {
    const linha = { expected_in: d.expected_in, expected_out: d.expected_out, break_minutes: Number(d.break_minutes) || 0, is_work_day: !!d.is_work_day, updated_at: agora };
    const ja = store.rows('time_schedules').find((s) => s.employee_id === emp.id && s.company_id === emp.company_id && Number(s.weekday) === Number(d.weekday));
    if (ja) Object.assign(ja, linha);
    else db.insert('time_schedules', { company_id: emp.company_id, employee_id: emp.id, weekday: Number(d.weekday), created_at: agora, ...linha }, { companyId: emp.company_id });
  }
  store.table('time_schedules').touch();
  return store.rows('time_sheets').filter((t) => t.employee_id === emp.id).length;
};
