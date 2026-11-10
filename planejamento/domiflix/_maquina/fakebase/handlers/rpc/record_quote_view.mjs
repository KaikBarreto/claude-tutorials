// RPC record_quote_view(_token, _fingerprint, _user_agent) · 20260624120000_quote_view_tracking.sql:58-133
// Registra a abertura da proposta pelo CLIENTE (o dono, com ?preview=1, nem chama). O mesmo navegador (fingerprint) não conta de novo em
// 30 minutos. Devolve o novo view_count (ou null se o token não existe).
import { now, nowIso } from '../../core/util.mjs';

export default async function recordQuoteView({ _token, _fingerprint, _user_agent }, { db }) {
  if (!_token) return null;
  const q = db.first('quotes', { token: _token });
  if (!q) return null;
  const agora = now().getTime();
  if (_fingerprint) {
    const recente = db.find('quote_views', (v) => v.quote_id === q.id && v.fingerprint === _fingerprint && agora - Date.parse(v.viewed_at) < 30 * 60 * 1000);
    if (recente.length) return q.view_count;
  }
  db.insert('quote_views', { quote_id: q.id, company_id: q.company_id, fingerprint: _fingerprint || null, user_agent: _user_agent || null });
  const n = (q.view_count || 0) + 1;
  db.update('quotes', { id: q.id }, { view_count: n, last_viewed_at: nowIso() });
  return n;
}
