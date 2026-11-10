// RPC schedule_book_service_order(p_service_order_id, p_resource_type, p_resource_id, p_starts_at, p_ends_at, p_override_justification)
//   · 20261017122000_public_api_v1_booking_engine.sql:290-440
// Reserva/reagenda a OS: grava data, hora, duração e UM responsável direto (técnico OU equipe), e refaz os responsáveis da junction
// (equipe = todos os membros ativos). p_starts_at/p_ends_at chegam em UTC; a data e a hora locais saem do fuso da empresa.
// Arrastar uma OS com responsável na Agenda passa por aqui: sem a RPC o toast "OS reagendada com sucesso!" aparece e a OS não se move.
// Não há motor de conflito no mundo falso: a reserva sempre passa (o conflito de agenda só é falado na aula).
import { RpcError } from '../../http/rest.mjs';
import { utcToLocal } from '../../lib/os.mjs';

const BOOKABLE = ['agendada', 'pendente', 'a_caminho', 'em_andamento', 'pausada'];

/** Núcleo compartilhado com schedule_book_service_order_plan. */
export function book(db, { osId, resourceType, resourceId, startsAt, durationMinutes, plan = null }) {
  if (!['technician', 'user', 'team'].includes(resourceType)) throw new RpcError('schedule_invalid_request', '22023');
  const os = db.first('service_orders', { id: osId });
  if (!os) throw new RpcError('schedule_service_order_not_found');
  if (!BOOKABLE.includes(os.status)) throw new RpcError('schedule_service_order_status_not_bookable');
  const local = utcToLocal(startsAt);
  const asUser = resourceType !== 'team';
  let members = [];
  if (asUser) {
    members = [resourceId];
  } else {
    members = db.find('team_members', { team_id: resourceId }).map((m) => m.user_id).filter((u) => db.first('profiles', { user_id: u })?.is_active !== false);
    if (!members.length) throw new RpcError('schedule_team_without_active_members');
  }
  db.remove('service_order_assignees', { service_order_id: osId });
  for (const user_id of members) db.insert('service_order_assignees', { service_order_id: osId, user_id });
  const first = plan?.[0];
  const time = first?.time ?? local.time;
  const patch = {
    scheduled_date: first?.date ?? local.date,
    scheduled_time: time.length === 5 ? `${time}:00` : time,
    duration_minutes: first?.duration_minutes ?? durationMinutes,
    schedule_plan: plan ?? [{ date: local.date, time: local.time.slice(0, 5), duration_minutes: durationMinutes }],
    technician_id: asUser ? resourceId : null,
    team_id: asUser ? null : resourceId,
  };
  db.update('service_orders', { id: osId }, patch);
  return {
    service_order_id: osId,
    reservation_id: null,
    resource_type: asUser ? 'user' : 'team',
    resource_id: resourceId,
    starts_at: startsAt,
    ends_at: new Date(new Date(startsAt).getTime() + patch.duration_minutes * 60000).toISOString(),
    overridden: false,
    override_id: null,
  };
}

export default async function scheduleBookServiceOrder({ p_service_order_id, p_resource_type, p_resource_id, p_starts_at, p_ends_at }, { db }) {
  const starts = new Date(p_starts_at);
  const ends = new Date(p_ends_at);
  const minutes = (ends - starts) / 60000;
  if (!(minutes >= 15 && minutes <= 480) || minutes % 60 !== 0) throw new RpcError('schedule_invalid_duration', '22023');
  return book(db, { osId: p_service_order_id, resourceType: p_resource_type, resourceId: p_resource_id, startsAt: p_starts_at, durationMinutes: minutes });
}
