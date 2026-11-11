// save_ecoflix_progress(p_episode_id, p_progress_seconds, p_duration_seconds, p_completed, p_insert_only): grava o ponto do vídeo.
// p_insert_only só cria a linha se ainda não existir ("marcar ao entrar" do player). Concluído nunca volta atrás.
import { agoraMs } from '../../lib/eco.mjs';
export default (a, { store, db, companyId, userId }) => {
  const ep = store.rows('ecoflix_episodes').find((e) => e.id === a.p_episode_id);
  if (!ep) throw new Error('Episódio não encontrado');
  const agora = new Date(agoraMs()).toISOString();
  const up = store.rows('ecoflix_user_progress').find((x) => x.user_id === userId && x.episode_id === ep.id);
  const dados = { progress_seconds: Math.round(Number(a.p_progress_seconds) || 0), duration_seconds: Math.round(Number(a.p_duration_seconds) || 0), completed: a.p_completed === true, watched_at: agora, last_progress_at: agora };
  if (up) {
    if (a.p_insert_only) return undefined;
    Object.assign(up, { ...dados, completed: up.completed || dados.completed });
  } else {
    db.insert('ecoflix_user_progress', { user_id: userId, episode_id: ep.id, title_id: ep.title_id, company_id: companyId, ...dados }, { companyId });
  }
  store.table('ecoflix_user_progress').touch();
  return undefined;
};
