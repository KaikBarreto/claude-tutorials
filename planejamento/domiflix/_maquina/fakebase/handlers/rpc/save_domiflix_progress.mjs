// RPC save_domiflix_progress · 20261031234000_domiflix_trilha_guiada.sql (T0 v2)
import { nowIso } from '../../core/util.mjs';
import { RpcError } from '../../http/rest.mjs';

export default async function saveDomiflixProgress(a, { db, userId }) {
  const ep = db.first('domiflix_episodes', { id: a.p_episode_id });
  if (!ep) throw new RpcError('aula não encontrada', '22023');
  const prof = db.first('profiles', { user_id: userId });
  const ins = !!a.p_insert_only;
  const cur = db.first('domiflix_user_progress', { user_id: userId, episode_id: ep.id });
  const n = nowIso();
  if (!cur) {
    return db.insert('domiflix_user_progress', { user_id: userId, company_id: prof?.company_id, episode_id: ep.id, title_id: ep.title_id, completed: !!a.p_completed, watched_at: n, progress_seconds: a.p_progress_seconds || 0, duration_seconds: a.p_duration_seconds || 0, last_progress_at: n });
  }
  if (ins) return cur;
  const patch = { completed: cur.completed || !!a.p_completed, watched_at: n, last_progress_at: n, duration_seconds: Math.max(cur.duration_seconds || 0, a.p_duration_seconds || 0) };
  if (!(a.p_progress_seconds === 0 && cur.progress_seconds > 0)) patch.progress_seconds = a.p_progress_seconds || 0;
  db.update('domiflix_user_progress', (r) => r === cur, patch);
  return cur;
}
