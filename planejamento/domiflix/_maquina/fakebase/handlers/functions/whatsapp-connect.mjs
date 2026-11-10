// Edge function `whatsapp-connect` falsa (T21 · cap. 3, "Conectar meu WhatsApp"). Espelha supabase/functions/whatsapp-connect (1.38.24):
//   POST { accepted_risk: true, risk_terms_version } -> { connection_id, instance_name, connection_status: 'qr', qr, pairing_code: null, message }
// Sem `accepted_risk` a real recusa (422 risk_acceptance_required). Efeitos: upsert de `whatsapp_connections` (provider evolution_qr, status 'qr',
// `risk_accepted_at/by`, `risk_terms_version`) e de `company_whatsapp_settings` (instance_name, connection_status 'qr'; se a linha nasce aqui,
// com os DEFAULTs do banco: enabled false e os três gatilhos ligados). Nenhuma chamada externa: o `qr` é um TEXTO fictício que o app desenha
// como QR Code (não pareia com nada). A "leitura" do QR é feita pelo bastidor `whatsapp-bastidor-leitura-qr`.
import { FunctionError } from '../../http/functions.mjs';
import { nowIso, stableId } from '../../core/util.mjs';

const INSTANCIA = 'dominex-glacial-demo';
const QR_FICTICIO = 'DOMIFLIX-DEMONSTRACAO-QR-FICTICIO-NAO-PAREIA-COM-NENHUM-APARELHO';

export default async function whatsappConnect(body, { db, userId, companyId }) {
  if (body?.accepted_risk !== true) {
    throw new FunctionError('Confirme que esta conexão por QR Code não é oficial e pode sofrer desconexão ou bloqueio.', 422, { error: 'risk_acceptance_required', message: 'Confirme que esta conexão por QR Code não é oficial e pode sofrer desconexão ou bloqueio.' });
  }
  const agora = nowIso();
  const base = {
    id: stableId('t21.conexao'), company_id: companyId, provider: 'evolution_qr', status: 'qr', instance_name: INSTANCIA, risk_accepted_at: agora, risk_accepted_by: userId,
    risk_terms_version: String(body.risk_terms_version || '2026-10-16').trim(), last_error: null, last_seen_at: agora, consecutive_failures: 0,
  };
  const conn = db.upsert('whatsapp_connections', ['company_id', 'provider'], base, { companyId });
  const atual = db.first('company_whatsapp_settings', (r) => String(r.company_id) === String(companyId));
  if (atual) db.update('company_whatsapp_settings', (r) => r === atual, { instance_name: INSTANCIA, connection_status: 'qr' });
  else {
    db.insert('company_whatsapp_settings', {
      company_id: companyId, instance_name: INSTANCIA, connection_status: 'qr', enabled: false, trigger_a_caminho: true, trigger_em_andamento: true,
      trigger_concluida: true, automation_preferences: null, active_connection_id: null, connected_number: null, connected_at: null,
    }, { companyId });
  }
  return { connection_id: conn.id, instance_name: INSTANCIA, connection_status: 'qr', qr: QR_FICTICIO, pairing_code: null, message: 'Escaneie o QR code no WhatsApp do seu celular para conectar.' };
}
