// Salvar o Ticket de Pesagem (T8): promove o rascunho (status draft) a ticket numerado e pendente, como
// finalize_weighing_ticket_v3 -> _v2 -> finalize_weighing_ticket (migrations 20260916235741, 20260930150000, 20260930230000):
// número = maior + 1 (ref "#N", sem período), created_at = agora (o ticket nasce quando ganha número), idempotente
// (ticket já numerado volta com already_existed), sem rascunho cria o ticket. Avulsa: sem preço e sem tabela.
import { agoraMs } from '../../lib/eco.mjs';
import { proximoTicket } from './get_next_ticket_number.mjs';

export default (a, ctx) => {
  const { store, db, RpcError, userId } = ctx;
  const cid = a.p_company_id || ctx.companyId;
  const kind = a.p_ticket_kind || 'standard';
  if (!['standard', 'standalone'].includes(kind)) throw new RpcError('Categoria de ticket inválida.');
  if (!a.p_ticket_id) throw new RpcError('Ticket sem identificador — não é possível finalizar.');
  const items = Array.isArray(a.p_items) ? a.p_items : [];
  const anexos = Array.isArray(a.p_attachments) ? a.p_attachments : [];
  const avulsa = kind === 'standalone';
  if (avulsa && !items.length) throw new RpcError('Pesagem avulsa precisa ter ao menos um item.');
  const agora = new Date(agoraMs()).toISOString();
  const existente = store.rows('weighing_tickets').find((t) => t.id === a.p_ticket_id);
  if (existente && existente.company_id !== cid) throw new RpcError('Este ticket não pertence à empresa informada.');
  if (existente && existente.status !== 'draft') {
    return { id: existente.id, ticket_number: existente.ticket_number, ticket_seq: existente.ticket_seq, ticket_period: existente.ticket_period ?? null,
      ticket_ref: existente.ticket_ref, status: existente.status, inserted: false, already_existed: true, created_at: existente.created_at,
      weighed_at_source: 'existing', ticket_kind: existente.ticket_kind, vehicle_type: existente.vehicle_type ?? null, weighing_fee: existente.weighing_fee ?? null };
  }
  let criado = agora, fonte = 'now';
  if (a.p_weighed_at) {
    const w = Date.parse(a.p_weighed_at), n = Date.parse(agora);
    if (w <= n + 5 * 60000 && w >= n - 30 * 86400000) { criado = new Date(Math.min(w, n)).toISOString(); fonte = 'client'; }
  }
  const numero = proximoTicket(store, cid);
  const campos = {
    type: a.p_type, customer_supplier_id: a.p_customer_supplier_id || null, customer_supplier_name: a.p_customer_supplier_name || null,
    customer_supplier_type: a.p_customer_supplier_type || null, price_table_id: avulsa ? null : a.p_price_table_id || null,
    pricing_mode: avulsa ? 'weighing_only' : a.p_pricing_mode || existente?.pricing_mode || 'weighing_only', items, attachments: anexos,
    payment_intent: avulsa ? null : a.p_payment_intent ?? null, driver_name: a.p_driver_name || '',
    vehicle_plate: String(a.p_vehicle_plate || '').toUpperCase(), notes: a.p_notes ?? null, ticket_number: numero, ticket_seq: numero,
    ticket_period: null, ticket_ref: `#${numero}`, status: 'pending', ticket_kind: kind, deleted_at: null, deleted_by: null,
    vehicle_type: avulsa ? (String(a.p_vehicle_type || '').trim() || null) : null, weighing_fee: avulsa ? a.p_weighing_fee ?? null : null,
    created_at: criado, updated_at: agora,
  };
  let id = a.p_ticket_id, inserido = false;
  if (existente) {
    Object.assign(existente, campos, { created_by: existente.created_by || userId });
    store.table('weighing_tickets').touch();
  } else {
    db.insert('weighing_tickets', { id, company_id: cid, ...campos, created_by: userId, first_weight: 0, first_weight_at: agora }, { companyId: cid });
    inserido = true;
  }
  return { id, ticket_number: numero, ticket_seq: numero, ticket_period: null, ticket_ref: `#${numero}`, status: 'pending', inserted: inserido,
    already_existed: false, created_at: criado, weighed_at_source: fonte, ticket_kind: kind, vehicle_type: campos.vehicle_type, weighing_fee: campos.weighing_fee };
};
