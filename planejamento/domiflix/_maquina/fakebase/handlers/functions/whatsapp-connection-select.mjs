// Edge function `whatsapp-connection-select` falsa (T21). Espelha supabase/functions/whatsapp-connection-select (1.38.24):
//   POST { connection_id } -> { ok, active_connection_id }; só ativa conexão `connected` (422 not_connected) e com o aceite do risco.
// Efeito: `company_whatsapp_settings` ganha active_connection_id, instance_name, connected_number e connection_status 'connected'.
import { FunctionError } from '../../http/functions.mjs';

export default async function whatsappConnectionSelect(body, { db, companyId }) {
  const c = body?.connection_id ? db.first('whatsapp_connections', (r) => String(r.id) === String(body.connection_id) && String(r.company_id) === String(companyId)) : null;
  if (!body?.connection_id) throw new FunctionError('Conexão não informada.', 400);
  if (!c) throw new FunctionError('Conexão não encontrada.', 404);
  if (c.status !== 'connected') throw new FunctionError('Conecte o número antes de ativá-lo.', 422);
  if (c.provider === 'evolution_qr' && !c.risk_accepted_at) throw new FunctionError('Confirme os riscos da conexão por QR Code antes de ativá-la.', 422);
  const patch = { active_connection_id: c.id, instance_name: c.instance_name, connected_number: c.display_number, connection_status: 'connected' };
  const atual = db.first('company_whatsapp_settings', (r) => String(r.company_id) === String(companyId));
  if (atual) db.update('company_whatsapp_settings', (r) => r === atual, patch);
  else db.insert('company_whatsapp_settings', { company_id: companyId, enabled: false, trigger_a_caminho: true, trigger_em_andamento: true, trigger_concluida: true, automation_preferences: null, ...patch }, { companyId });
  return { ok: true, active_connection_id: c.id };
}
