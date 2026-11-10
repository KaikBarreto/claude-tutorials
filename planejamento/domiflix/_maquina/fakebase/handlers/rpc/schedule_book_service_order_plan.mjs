// RPC schedule_book_service_order_plan(p_service_order_id, p_resource_type, p_resource_id, p_starts_at, p_schedule_plan, p_override_justification)
//   · 20261017122000_public_api_v1_booking_engine.sql (variante com jornadas por dia)
// Igual à schedule_book_service_order, mas grava o schedule_plan inteiro (a Agenda sempre usa esta, porque a OS já tem plano).
// Estende o núcleo da outra RPC em vez de reescrevê-lo.
import { RpcError } from '../../http/rest.mjs';
import { book } from './schedule_book_service_order.mjs';

export default async function scheduleBookServiceOrderPlan({ p_service_order_id, p_resource_type, p_resource_id, p_starts_at, p_schedule_plan }, { db }) {
  const plan = Array.isArray(p_schedule_plan) ? p_schedule_plan : [];
  if (!plan.length) throw new RpcError('schedule_invalid_request', '22023');
  return book(db, {
    osId: p_service_order_id, resourceType: p_resource_type, resourceId: p_resource_id, startsAt: p_starts_at,
    durationMinutes: plan[0].duration_minutes, plan,
  });
}
