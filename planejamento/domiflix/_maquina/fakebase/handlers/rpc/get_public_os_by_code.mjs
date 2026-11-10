// RPC get_public_os_by_code(p_code) · 20260919210000_get_public_os_allowlist_e_recusa_tarefa.sql:386-418
// Resolve o código curto da OS (`public_short_code`, a parte final do endereço /os-tecnico/<cliente>-<serviço>-<código>),
// ignora tarefa interna e devolve o mesmo payload de get_public_os.
import { montarOsPublica } from '../../lib/publicOs.mjs';

export default async function getPublicOsByCode({ p_code }, { db }) {
  if (!p_code || !String(p_code).trim()) return null;
  const os = db.first('service_orders', (r) => r.public_short_code === p_code && r.entry_type !== 'tarefa');
  return os ? montarOsPublica(os.id) : null;
}
