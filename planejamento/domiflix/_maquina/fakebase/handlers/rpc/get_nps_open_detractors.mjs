// RPC get_nps_open_detractors(p_start, p_end) · 20260616090000_nps_carona_link_publico_ranking.sql:422-485
// Detratores (nota 0 a 6) respondidos no período, do mais recente para o mais antigo (cartão "Detratores em Aberto").
import { utcDate, techOf } from '../../lib/os.mjs';

export default async function getNpsOpenDetractors({ p_start, p_end }, { db }) {
  const out = [];
  for (const sr of db.rows('service_ratings')) {
    if (!sr.rated_at || sr.nps_score == null || sr.nps_score > 6) continue;
    const d = utcDate(sr.rated_at);
    if (d < p_start || d > p_end) continue;
    const os = db.first('service_orders', { id: sr.service_order_id });
    if (!os) continue;
    const tech = techOf(os);
    out.push({
      os_id: os.id,
      order_number: os.order_number,
      nps_score: sr.nps_score,
      comment: sr.comment,
      rated_at: sr.rated_at,
      rated_by_name: sr.rated_by_name,
      customer_name: db.first('customers', { id: os.customer_id })?.name ?? null,
      technician_id: tech,
      technician_name: tech ? db.first('profiles', { user_id: tech })?.full_name ?? null : null,
    });
  }
  return out.sort((a, b) => String(b.rated_at).localeCompare(String(a.rated_at)));
}
