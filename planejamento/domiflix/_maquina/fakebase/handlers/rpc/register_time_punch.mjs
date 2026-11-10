// RPC register_time_punch(p_type, p_recorded_at, p_employee_id, p_source, p_notes, p_force_date, ...) → jsonb { date, allowed_actions }
// 20260930150000_ponto_multiplas_jornadas.sql (T15, cap. 10: "Registro manual" do gestor; a aula abre a janela e cancela). Com `p_force_date` a
// ordem das ações NÃO é validada (o gestor grava a saída que ficou esquecida). Grava `time_records` e refaz `time_sheets`.
import { RpcError } from '../../http/rest.mjs';
import { registrarBatida } from '../functions/time-clock-portal.mjs';

export default async function registerTimePunch(a, { db, userId }) {
  const emp = db.first('employees', { id: a.p_employee_id });
  if (!emp) throw new RpcError('employee_not_found', 'P0001');
  const r = registrarBatida(db, emp, a.p_type, {
    force: !!a.p_force_date, date: a.p_force_date || undefined, recorded_at: a.p_recorded_at || undefined, latitude: a.p_latitude, longitude: a.p_longitude,
    address: a.p_address, source: a.p_source || 'app', notes: a.p_notes, user_id: userId, device_info: a.p_device_info,
  });
  if (r.erro) throw new RpcError('punch_out_of_order', 'P0001');
  return { date: r.date, allowed_actions: r.allowed_actions };
}
