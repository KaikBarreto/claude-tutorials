// Trilha guiada da EcoFlix: cliente pagante, sem lembrete (o catálogo de aulas da EcoFlix não faz parte deste mundo).
export default (a, { store, companyId, userId }) => {
  const prof = store.rows('profiles').find((p) => p.id === userId) || {};
  const comp = store.rows('companies').find((c) => c.id === companyId) || {};
  const slug = a?.p_path_slug || 'tutoriais-do-sistema';
  const path = { id: 'trilha-' + slug, slug, title: 'Tutoriais do sistema', description: null, coverUrl: null, isOnboarding: true };
  return {
    path, paths: [path],
    user: { firstName: String(prof.full_name || '').split(' ')[0], email: prof.email || '', companyName: comp.name || '', companyId, accountStage: 'paid', onboardingDay: 253 },
    progress: { coreTotal: 0, coreCompleted: 0, corePercent: 100, trackTotal: 0, trackCompleted: 0, trackPercent: 100, lastProgressAt: null },
    reminder: { severity: 'none', dismissedUntil: null },
    nextLesson: null,
    introGate: { required: false, acknowledged: true, lesson: null },
    track: [],
  };
};
