// Edge cato-background (T21): recebe a pergunta (message, history, context, sessionId, companyScope) e devolve { jobId }. O job entra
// em cato_jobs como "processing", já com o response_payload da resposta simulada (lib/cato.mjs; a tela só o lê quando o status vira
// "completed", em handlers/views/cato_jobs.mjs). Grava também a interação em cato_events (id = interactionId), que o 👍/👎 marca.
import crypto from 'node:crypto';
import { agoraMs } from '../../lib/eco.mjs';
import { acharResposta, payloadDe, semResposta, registraEspera } from '../../lib/cato.mjs';

export default (body, { store, db, user, companyId, FunctionError }) => {
  if (!user) throw new FunctionError('unauthorized', 401);
  const prof = store.rows('profiles').find((p) => p.id === user.id);
  const cid = prof?.company_id || companyId;
  const agora = agoraMs();
  const iso = new Date(agora).toISOString();
  const r = acharResposta(body?.message);
  if (!r) console.warn(`[cato-background] pergunta fora das respostas R1 a R9 do T21: ${String(body?.message || '').slice(0, 80)}`);
  const payload = r ? payloadDe(r, agora) : semResposta(body?.message);
  const jobId = crypto.randomUUID();
  registraEspera(jobId, Math.round((r?.espera ?? 1.6) * 1000));
  db.insert('cato_jobs', {
    id: jobId, company_id: cid, user_id: user.id, session_id: body?.sessionId ?? null, status: 'processing',
    response_payload: payload, error_code: null, created_at: iso, finished_at: null,
    expires_at: new Date(agora + 3600000).toISOString(),
  }, { companyId: cid });
  db.insert('cato_events', {
    id: payload.interactionId, company_id: cid, user_id: user.id, session_id: body?.sessionId ?? null, created_at: iso,
    message: String(body?.message || ''), answer: payload.answer, answer_empty: false, response_payload: payload,
    tools_used: payload.toolsUsed || [], had_chart: !!payload.chart, chart_type: payload.chart?.type ?? null, had_image: false,
    cache_hit: false, feedback: null, feedback_reason: null, feedback_at: null,
  }, { companyId: cid });
  return { jobId };
};
