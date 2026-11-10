// RPC recompute_time_sheet(p_company_id, p_employee_id, p_date) → void · refaz o espelho do dia (T15, cap. 10: editar/excluir batida).
import { recomputar } from '../functions/time-clock-portal.mjs';

export default async function recomputeTimeSheet(a, { db }) {
  recomputar(db, a.p_company_id, a.p_employee_id, a.p_date);
  return null;
}
