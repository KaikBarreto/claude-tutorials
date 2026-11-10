// RPC project_progress_summary() (20261017182000_projetos_onda1_progresso_e_limpeza.sql) · T10, aba "Visão geral" do projeto e coluna "Progresso".
// Sem argumentos; uma linha por obra da empresa: done_count = cards em etapa de ganho; active_count = TODO card nao perdido (ganhos inclusive,
// e o denominador do progresso); lost_count = cards em etapa de perda; has_won_stage = alguma frente tem etapa de ganho.
// Card sem etapa que resolva conta como pendente (nem feito nem perdido), como no banco.
export default async function projectProgressSummary(_args, { db, companyId }) {
  const empresa = companyId;
  return db
    .rows('projects')
    .filter((p) => p.company_id === empresa)
    .map((p) => {
      const frentes = db.rows('crm_pipelines').filter((f) => f.project_id === p.id && f.company_id === p.company_id);
      const ids = new Set(frentes.map((f) => f.id));
      const etapas = new Map(db.rows('crm_stages').filter((s) => s.company_id === p.company_id).map((s) => [s.id, s]));
      let done = 0;
      let active = 0;
      let lost = 0;
      for (const l of db.rows('leads')) {
        if (l.company_id !== p.company_id || !ids.has(l.pipeline_id)) continue;
        const s = etapas.get(l.stage_id);
        if (s?.is_won) done += 1;
        if (!s?.is_lost) active += 1;
        if (s?.is_lost) lost += 1;
      }
      const hasWon = db.rows('crm_stages').some((s) => s.company_id === p.company_id && s.is_won && ids.has(s.pipeline_id));
      return { project_id: p.id, done_count: done, active_count: active, lost_count: lost, has_won_stage: hasWon };
    });
}
