// T0 · RPC get_ecoflix_learning_status com o catálogo da EcoFlix de verdade (ecoflix_learning_paths, ecoflix_titles com track_group/
// track_order, ecoflix_title_modules, ecoflix_user_progress, ecoflix_intro_acknowledgements). Molde: get_domiflix_learning_status da Domiflix.
// Quem chama (handlers/rpc/get_ecoflix_learning_status.mjs) só entra aqui quando a semente t00/catalogo está carregada.
import { agoraMs } from './eco.mjs';

const dia = (ms) => new Date(ms - 3 * 3600e3).toISOString().slice(0, 10);

export function statusCompleto(a, { store, companyId, userId }) {
  const rows = (t) => store.rows(t);
  const prof = rows('profiles').find((p) => p.id === userId) || {};
  const co = rows('companies').find((c) => c.id === companyId) || {};
  const slug = a?.p_path_slug || 'tutoriais-do-sistema';
  const paths = rows('ecoflix_learning_paths').filter((p) => p.is_active !== false).sort((x, y) => x.order_index - y.order_index);
  const path = paths.find((p) => p.slug === slug) || paths[0];
  const pj = (p) => ({ id: p.id, slug: p.slug, title: p.title, description: p.description ?? null, coverUrl: p.cover_url ?? null, isOnboarding: !!p.is_onboarding });

  const plano = rows('subscription_plans').find((p) => p.code === co.subscription_plan);
  const agora = new Date(agoraMs()).toISOString();
  const entitled = new Set([
    ...rows('company_modules').filter((m) => m.company_id === co.id && (!m.removed_at || (m.effective_until && m.effective_until > agora))).map((m) => m.module_code),
    ...((plano && plano.modules) || []),
  ]);

  const lessons = [];
  for (const t of rows('ecoflix_titles').filter((x) => x.learning_path_id === path.id && x.is_active !== false)) {
    const tm = rows('ecoflix_title_modules').filter((x) => x.title_id === t.id)
      .map((x) => ({ code: x.module_code, mod: rows('subscription_modules').find((m) => m.code === x.module_code) }))
      .sort((p, q) => (p.mod?.sort_order ?? 1e9) - (q.mod?.sort_order ?? 1e9) || p.code.localeCompare(q.code))[0];
    const included = t.track_group === 'core' ? true : !tm ? false : entitled.has(tm.code);
    for (const e of rows('ecoflix_episodes').filter((x) => x.title_id === t.id && x.is_active !== false)) {
      if (!String(e.video_id || '').trim()) continue;
      const up = rows('ecoflix_user_progress').find((x) => x.user_id === userId && x.episode_id === e.id);
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
    mobileVideoType: l.e.mobile_video_type ?? null, mobileVideoId: l.e.mobile_video_id ?? null,
    completed: !!l.up?.completed, progressSeconds: l.up?.progress_seconds || 0, durationSeconds: l.up?.duration_seconds || 0,
  }));
  const req = track.filter((x) => x.requiredForUser);
  const core = track.filter((x) => x.group === 'core');
  const nextRaw = [...req].filter((x) => !x.completed).sort((p, q) => p.sequence - q.sequence)[0] || null;
  const next = nextRaw && { titleId: nextRaw.titleId, moduleTitle: nextRaw.moduleTitle, episodeId: nextRaw.episodeId, lessonTitle: nextRaw.lessonTitle, episodeNumber: nextRaw.episodeNumber, progressSeconds: nextRaw.progressSeconds };

  const t0 = agoraMs();
  const dias = Math.max(0, Math.round((new Date(dia(t0)) - new Date(dia(new Date(co.created_at || t0).getTime()))) / 86400e3));
  const ack = rows('ecoflix_intro_acknowledgements').some((x) => x.user_id === userId && x.learning_path_id === path.id);
  const intro = track[0] || {};
  const pct = (n, d) => (d ? Math.round((n * 100) / d) : 0);
  const coreDone = core.filter((x) => x.completed).length;
  const reqDone = req.filter((x) => x.completed).length;
  const ultimo = rows('ecoflix_user_progress').filter((x) => x.user_id === userId && x.last_progress_at).map((x) => x.last_progress_at).sort().pop() || null;
  return {
    user: {
      firstName: String(prof.full_name || 'Olá').trim().split(' ')[0], email: prof.email || '', companyName: co.name || '', companyId: co.id,
      accountStage: ['testing', 'trial'].includes(co.subscription_status) ? 'trial' : co.subscription_status === 'active' ? 'paid' : 'neutral',
      onboardingDay: dias,
    },
    progress: { coreTotal: core.length, coreCompleted: coreDone, corePercent: pct(coreDone, core.length), trackTotal: req.length, trackCompleted: reqDone, trackPercent: pct(reqDone, req.length), lastProgressAt: ultimo },
    reminder: { severity: 'none', dismissedUntil: null },
    nextLesson: next,
    introGate: {
      required: !!path.is_onboarding && ['testing', 'trial', 'active'].includes(co.subscription_status) && !ack && intro.group === 'core' && !!intro.videoId,
      acknowledged: ack, lesson: track[0] || null,
    },
    track, path: pj(path), paths: paths.map(pj),
  };
}
