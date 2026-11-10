// Ajudantes dos handlers de OS (T5): fuso da empresa, conversões de instante e responsável direto.
import { db } from '../core/db.mjs';

/** Fuso da empresa (company_settings.timezone), Brasília por padrão. */
export function companyTimezone() {
  return db.rows('company_settings')[0]?.timezone || 'America/Sao_Paulo';
}

/** Instante ISO (UTC) -> { date: 'YYYY-MM-DD', time: 'HH:MM:SS' } no fuso dado (o `AT TIME ZONE` do Postgres). */
export function utcToLocal(iso, timeZone = companyTimezone()) {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit',
  }).formatToParts(new Date(iso));
  const get = (t) => parts.find((p) => p.type === t)?.value;
  return { date: `${get('year')}-${get('month')}-${get('day')}`, time: `${get('hour')}:${get('minute')}:${get('second')}` };
}

/** Data (YYYY-MM-DD) de um timestamptz como o Postgres a vê na sessão (UTC): `rated_at::date`, `completed_at::date`. */
export const utcDate = (iso) => (iso ? String(iso).slice(0, 10) : null);

/** Quem executa a OS para o NPS: technician_id, senão o 1º responsável (por created_at). */
export function techOf(os) {
  if (os.technician_id) return os.technician_id;
  const first = db
    .find('service_order_assignees', { service_order_id: os.id })
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)))[0];
  return first?.user_id || null;
}

export const round = (n, d) => {
  const f = 10 ** d;
  return Math.round(n * f) / f;
};
