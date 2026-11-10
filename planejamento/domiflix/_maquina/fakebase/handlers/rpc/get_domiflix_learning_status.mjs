// RPC get_domiflix_learning_status(p_path_slug) · 20261031234000_domiflix_trilha_guiada.sql + 20261101001000 (relevant_to_user/requiredForUser)
// Trilha efetiva do usuario logado: grupos, plano, progresso, proxima aula, lembrete e introducao. (T0 v2)
import { now } from '../../core/util.mjs';
import { RpcError } from '../../http/rest.mjs';

const dayOf = (d) => new Date(d.getTime() - 3 * 3600e3).toISOString().slice(0, 10);

export default async function getDomiflixLearningStatus(a, { db, userId }) {
  const prof = db.first('profiles', { user_id: userId });
  if (!prof?.company_id) throw new RpcError('Usuário sem empresa', '23514');
  const co = db.first('companies', { id: prof.company_id });
  const path = db.first('domiflix_learning_paths', (p) => p.slug === (a.p_path_slug || 'tutoriais-do-sistema') && p.is_active !== false);
  if (!path) throw new RpcError('Trilha não encontrada', '22023');
  const paths = db.rows('domiflix_learning_paths').filter((p) => p.is_active !== false).sort((x, y) => x.order_index - y.order_index)
    .map((p) => ({ id: p.id, slug: p.slug, title: p.title, description: p.description, coverUrl: p.cover_url, isOnboarding: !!p.is_onboarding }));
  const pathJson = paths.find((p) => p.id === path.id);

  const plan = db.first('subscription_plans', { code: co.subscription_plan || 'start' });
  const entitled = new Set([
    ...db.find('company_modules', { company_id: co.id }).map((m) => m.module_code),
    ...((plan?.included_modules) || []),
  ]);
  const t0 = now();
  const lessons = [];
  for (const t of db.find('domiflix_titles', { learning_path_id: path.id })) {
    if (t.is_active === false) continue;
    const tm = db.find('domiflix_title_modules', { title_id: t.id })
      .map((x) => ({ code: x.module_code, mod: db.first('subscription_modules', { code: x.module_code }) }))
      .sort((p, q) => (p.mod?.sort_order ?? 1e9) - (q.mod?.sort_order ?? 1e9) || p.code.localeCompare(q.code))[0];
    const included = t.track_group === 'core' ? true : !tm ? false : entitled.has(tm.code);
    for (const e of db.find('domiflix_episodes', { title_id: t.id })) {
      if (!String(e.video_id || '').trim()) continue;
      const up = db.first('domiflix_user_progress', { user_id: userId, episode_id: e.id });
      lessons.push({ t, e, up, tm, included });
    }
  }
  lessons.sort((x, y) => {
    const g = (l) => (l.t.track_group === 'core' ? 0 : l.included ? 1 : 2);
    return g(x) - g(y) || x.t.track_order - y.t.track_order || x.e.order_index - y.e.order_index || String(x.e.id).localeCompare(String(y.e.id));
  });
  const track = lessons.map((l, i) => ({
    sequence: i + 1, titleId: l.t.id, moduleTitle: l.t.title, moduleDescription: l.t.description ?? null,
    thumbnailUrl: l.t.thumbnail_url ?? null, bannerUrl: l.t.banner_url ?? null, group: l.t.track_group,
    moduleCode: l.tm?.code ?? null, moduleName: l.tm?.mod?.name ?? null, modulePrice: l.tm?.mod?.price ?? null,
    includedInPlan: l.included, requiredForUser: l.t.track_group === 'core' || l.included,
    episodeId: l.e.id, lessonTitle: l.e.title, lessonDescription: l.e.description ?? null, episodeNumber: l.e.episode_number ?? null,
    durationMinutes: l.e.duration_minutes ?? null, videoType: l.e.video_type, videoId: l.e.video_id,
    completed: !!l.up?.completed, progressSeconds: l.up?.progress_seconds || 0, durationSeconds: l.up?.duration_seconds || 0,
    _last: l.up?.last_progress_at || null,
  }));
  const req = track.filter((x) => x.requiredForUser);
  const core = track.filter((x) => x.group === 'core');
  const started = (x) => x.completed || x.progressSeconds >= Math.max(30, Math.ceil(x.durationSeconds * 0.1));
  const lastProgress = req.filter((x) => x._last && started(x)).map((x) => x._last).sort().pop() || null;
  const nextRaw = [...req].filter((x) => !x.completed).sort((p, q) => p.sequence - q.sequence)[0] || null;
  const next = nextRaw && { titleId: nextRaw.titleId, moduleTitle: nextRaw.moduleTitle, episodeId: nextRaw.episodeId, lessonTitle: nextRaw.lessonTitle, episodeNumber: nextRaw.episodeNumber, progressSeconds: nextRaw.progressSeconds };

  const started0 = new Date(Math.max(new Date(prof.created_at || co.created_at).getTime(), new Date(co.learning_onboarding_started_at || co.created_at).getTime()));
  const days = Math.max(0, Math.round((new Date(dayOf(t0)) - new Date(dayOf(started0))) / 86400e3));
  const onb = db.first('domiflix_user_onboarding', { user_id: userId });
  const dismissed = onb?.dismissed_until || null;
  const ack = !!db.first('domiflix_intro_acknowledgements', { user_id: userId, learning_path_id: path.id });
  let severity = 'none';
  if (req.length && req.every((x) => x.completed)) severity = 'complete';
  else if (path.is_onboarding && days >= 0 && days <= 30 && (!dismissed || dismissed < dayOf(t0))) {
    severity = 'invite';
    const idle = lastProgress ? Math.round((new Date(dayOf(t0)) - new Date(dayOf(new Date(lastProgress)))) / 86400e3) : null;
    if (idle === null && days >= 7) severity = 'critical';
    else if (idle !== null && idle >= 7) severity = 'critical';
    else if (idle !== null && idle >= 3) severity = 'soft';
  }
  const intro = track[0] || {};
  const strip = ({ _last, ...r }) => r;
  const pct = (n, d) => (d ? Math.round((n * 100) / d) : 0);
  const coreDone = core.filter((x) => x.completed).length;
  const reqDone = req.filter((x) => x.completed).length;
  return {
    user: {
      firstName: String(prof.full_name || 'Olá').trim().split(' ')[0], email: prof.email || '', companyName: co.name, companyId: co.id,
      accountStage: ['testing', 'trial'].includes(co.subscription_status) ? 'trial' : co.subscription_status === 'active' ? 'paid' : 'neutral',
      onboardingDay: days,
    },
    progress: { coreTotal: core.length, coreCompleted: coreDone, corePercent: pct(coreDone, core.length), trackTotal: req.length, trackCompleted: reqDone, trackPercent: pct(reqDone, req.length), lastProgressAt: lastProgress },
    reminder: { severity, dismissedUntil: dismissed },
    nextLesson: next,
    introGate: {
      required: !!path.is_onboarding && ['testing', 'trial', 'active'].includes(co.subscription_status)
        && started0 >= new Date(path.intro_gate_enabled_at || 0) && !ack && intro.group === 'core' && !!intro.videoId,
      acknowledged: ack, lesson: track[0] ? strip(intro) : {},
    },
    track: track.map(strip), path: pathJson, paths,
  };
}
