// acknowledge_ecoflix_intro(p_episode_id): o "Confirmar e começar a primeira aula" do portão do primeiro acesso. Grava a confirmação e
// deixa a introdução concluída (progresso do episódio), como a função do banco; a trilha passa a abrir sem o portão.
import { agoraMs } from '../../lib/eco.mjs';
export default (a, { store, db, companyId, userId }) => {
  const ep = store.rows('ecoflix_episodes').find((e) => e.id === a.p_episode_id);
  if (!ep) throw new Error('Episódio não encontrado');
  const titulo = store.rows('ecoflix_titles').find((t) => t.id === ep.title_id);
  const agora = new Date(agoraMs()).toISOString();
  if (!store.rows('ecoflix_intro_acknowledgements').some((x) => x.user_id === userId && x.learning_path_id === titulo?.learning_path_id)) {
    db.insert('ecoflix_intro_acknowledgements', { user_id: userId, learning_path_id: titulo?.learning_path_id ?? null, episode_id: ep.id, acknowledged_at: agora }, { companyId });
  }
  const up = store.rows('ecoflix_user_progress').find((x) => x.user_id === userId && x.episode_id === ep.id);
  const dur = Math.round(Number(ep.duration_minutes || 0) * 60);
  if (up) Object.assign(up, { completed: true, progress_seconds: Math.max(up.progress_seconds || 0, dur), duration_seconds: up.duration_seconds || dur, watched_at: agora, last_progress_at: agora });
  else db.insert('ecoflix_user_progress', { user_id: userId, episode_id: ep.id, title_id: ep.title_id, completed: true, progress_seconds: dur, duration_seconds: dur, watched_at: agora, last_progress_at: agora, company_id: companyId }, { companyId });
  store.table('ecoflix_user_progress').touch();
  return undefined;
};
