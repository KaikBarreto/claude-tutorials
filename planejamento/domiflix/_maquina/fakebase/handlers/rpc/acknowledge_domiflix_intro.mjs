// RPC acknowledge_domiflix_intro(p_episode_id) · 20261101002000 (conclui e confirma atomicamente) (T0 v2)
import { nowIso } from '../../core/util.mjs';

export default async function acknowledgeDomiflixIntro(a, { db, userId }) {
  const ep = db.first('domiflix_episodes', { id: a.p_episode_id });
  const title = ep && db.first('domiflix_titles', { id: ep.title_id });
  const prof = db.first('profiles', { user_id: userId });
  const n = nowIso();
  const cur = db.first('domiflix_user_progress', { user_id: userId, episode_id: ep.id });
  if (cur) db.update('domiflix_user_progress', (r) => r === cur, { completed: true, watched_at: n, last_progress_at: n });
  else db.insert('domiflix_user_progress', { user_id: userId, company_id: prof.company_id, episode_id: ep.id, title_id: ep.title_id, completed: true, watched_at: n, progress_seconds: 0, duration_seconds: 0, last_progress_at: n });
  if (!db.first('domiflix_intro_acknowledgements', { user_id: userId, learning_path_id: title.learning_path_id })) {
    db.insert('domiflix_intro_acknowledgements', { user_id: userId, company_id: prof.company_id, learning_path_id: title.learning_path_id, episode_id: ep.id, completed_at: n, understood_at: n });
  }
  return n;
}
