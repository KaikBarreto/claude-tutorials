// RPC get_nps_technician_ranking(p_start, p_end) · 20260616090000_nps_carona_link_publico_ranking.sql:325-415
// Ranking por técnico (quem aparece = quem concluiu OS no período; técnico = technician_id, senão o 1º responsável).
// respostas = avaliações respondidas no período; taxa_resposta = respostas / OS concluídas; ordenado por NPS médio decrescente.
import { utcDate, techOf, round } from '../../lib/os.mjs';

export default async function getNpsTechnicianRanking({ p_start, p_end }, { db }) {
  const done = db
    .rows('service_orders')
    .filter((o) => o.status === 'concluida')
    .filter((o) => {
      const d = utcDate(o.completed_at || o.updated_at);
      return d >= p_start && d <= p_end;
    });
  const doneBy = new Map();
  for (const o of done) {
    const t = techOf(o);
    if (t) doneBy.set(t, (doneBy.get(t) || 0) + 1);
  }
  const answers = [];
  for (const sr of db.rows('service_ratings')) {
    if (!sr.rated_at) continue;
    const d = utcDate(sr.rated_at);
    if (d < p_start || d > p_end) continue;
    const os = db.first('service_orders', { id: sr.service_order_id });
    if (os) answers.push({ tech: techOf(os), sr });
  }
  const rows = [...doneBy.entries()].map(([user_id, os_concluidas]) => {
    const mine = answers.filter((a) => a.tech === user_id).map((a) => a.sr);
    const scores = mine.filter((r) => r.nps_score != null).map((r) => Number(r.nps_score));
    const stars = mine
      .map((r) => [r.quality_rating, r.punctuality_rating, r.professionalism_rating].filter((v) => v != null).map(Number))
      .filter((v) => v.length)
      .map((v) => v.reduce((s, x) => s + x, 0) / v.length);
    const profile = db.first('profiles', { user_id });
    return {
      user_id,
      full_name: profile?.full_name ?? null,
      avatar_url: profile?.avatar_url ?? null,
      nps_medio: scores.length ? round(scores.reduce((s, v) => s + v, 0) / scores.length, 1) : null,
      media_estrelas: stars.length ? round(stars.reduce((s, v) => s + v, 0) / stars.length, 2) : null,
      respostas: scores.length,
      os_concluidas,
      taxa_resposta: round(scores.length / os_concluidas, 3),
    };
  });
  return rows.sort((a, b) => (b.nps_medio ?? -1) - (a.nps_medio ?? -1));
}
