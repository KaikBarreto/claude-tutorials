// Função de BASTIDOR do kit de gravação (não existe no app nem no Supabase real): faz o que o webhook da Evolution faz quando o celular LÊ o QR
// (supabase/functions/whatsapp-webhook/index.ts:269-345): a conexão vira 'connected' com `display_number` e `connected_at`, e a linha de
// `company_whatsapp_settings` ganha connection_status 'connected', connected_number, connected_at e active_connection_id (se ainda não havia).
//   POST { number? }  (padrão 552130001000, o telefone fictício da empresa)  ->  { ok, connection_id }
// A tela percebe na consulta de 4 s (`useWhatsappConnections`, refetchInterval enquanto o status é 'qr').
import { FunctionError } from '../../http/functions.mjs';
import { nowIso } from '../../core/util.mjs';

export default async function whatsappBastidorLeituraQr(body, { db, companyId }) {
  const c = db.first('whatsapp_connections', (r) => String(r.company_id) === String(companyId) && r.provider === 'evolution_qr');
  if (!c) throw new FunctionError('Nenhuma conexão por QR Code para ler.', 404);
  const numero = String(body?.number || '552130001000');
  const agora = nowIso();
  db.update('whatsapp_connections', (r) => r === c, { status: 'connected', display_number: numero, connected_at: agora, last_seen_at: agora, last_error: null, warmup_started_at: c.warmup_started_at || agora });
  db.update('company_whatsapp_settings', (r) => String(r.company_id) === String(companyId),
    { connection_status: 'connected', connected_number: numero, connected_at: agora, active_connection_id: c.id });
  return { ok: true, connection_id: c.id };
}
