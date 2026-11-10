// Edge function `whatsapp-connection-disconnect` falsa (T21). Espelha supabase/functions/whatsapp-connection-disconnect (1.38.24):
//   POST { connection_id } -> { ok }. Pausa a fila: conexão 'disconnected' e settings sem canal ativo, status 'disconnected', sem número.
import { FunctionError } from '../../http/functions.mjs';
import { nowIso } from '../../core/util.mjs';

export default async function whatsappConnectionDisconnect(body, { db, companyId }) {
  if (!body?.connection_id) throw new FunctionError('Conexão não informada.', 400);
  const c = db.first('whatsapp_connections', (r) => String(r.id) === String(body.connection_id) && String(r.company_id) === String(companyId));
  if (!c) throw new FunctionError('Conexão não encontrada.', 404);
  db.update('whatsapp_connections', (r) => r === c, { status: 'disconnected', next_send_at: null, last_seen_at: nowIso() });
  db.update('company_whatsapp_settings', (r) => String(r.company_id) === String(companyId) && String(r.active_connection_id) === String(c.id),
    { active_connection_id: null, connection_status: 'disconnected', connected_number: null });
  return { ok: true };
}
