// RPC get_nps_criteria_averages(p_start, p_end) · 20260616140000_nps_onda2_criterios_dinamicos.sql:477-512
// Média de estrelas por critério (label_snapshot) nas avaliações respondidas no período, em ordem alfabética.
import { utcDate, round } from '../../lib/os.mjs';

export default async function getNpsCriteriaAverages({ p_start, p_end }, { db }) {
  const groups = new Map();
  for (const c of db.rows('service_rating_criteria')) {
    const rating = db.first('service_ratings', { id: c.rating_id });
    if (!rating?.rated_at) continue;
    const d = utcDate(rating.rated_at);
    if (d < p_start || d > p_end) continue;
    const g = groups.get(c.label_snapshot) || [];
    g.push(Number(c.value));
    groups.set(c.label_snapshot, g);
  }
  return [...groups.entries()]
    .sort((a, b) => a[0].localeCompare(b[0], 'pt-BR'))
    .map(([label, vals]) => ({ label, media: round(vals.reduce((s, v) => s + v, 0) / vals.length, 2), respostas: vals.length }));
}
