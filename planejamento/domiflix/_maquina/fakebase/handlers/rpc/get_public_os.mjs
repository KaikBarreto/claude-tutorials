// RPC get_public_os(p_os_id) · 20260925120000_check_in_out_by_autoria_real.sql:260-619 (+ technician_location, 20261019060000)
// Payload do link público da OS (visão do cliente, relatório sem login, mapa público). OS inexistente ou de tarefa -> null.
// Sem este handler o link do cliente cai no erro de carga. Montagem em lib/publicOs.mjs (T7).
import { montarOsPublica } from '../../lib/publicOs.mjs';

export default async function getPublicOs({ p_os_id }) {
  return montarOsPublica(p_os_id);
}
