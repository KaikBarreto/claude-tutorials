// RPC set_cato_feedback(p_event_id, p_value, p_reason) (T21, 👍/👎 e o motivo): marca a interação em cato_events (gravada pela edge
// cato-background). Valor 0 limpa; o motivo só vale com -1 (virar 👍 limpa o motivo; a chamada de 2 argumentos não apaga o motivo).
import { agoraMs } from '../../lib/eco.mjs';

export default (a, { store, db }) => {
  const ev = store.rows('cato_events').find((e) => e.id === a?.p_event_id);
  if (!ev) return false;
  const v = Number(a?.p_value) || 0;
  const patch = { feedback: v === 0 ? null : v, feedback_at: v === 0 ? null : new Date(agoraMs()).toISOString() };
  if (v !== -1) patch.feedback_reason = null;
  else if (a?.p_reason) patch.feedback_reason = String(a.p_reason);
  db.update('cato_events', { id: ev.id }, patch);
  return true;
};
