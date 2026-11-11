// Próximo número de Ticket de Pesagem (T8): maior ticket_number da empresa + 1 (rascunho não tem número).
// O app usa na prévia da aba ("#58", "#59" = próximo + posição) e o finalize_weighing_ticket_v3 numera com a mesma conta.
export function proximoTicket(store, cid) {
  const ns = store.rows('weighing_tickets')
    .filter((t) => t.company_id === cid && t.ticket_number != null)
    .map((t) => Number(t.ticket_number) || 0);
  return (ns.length ? Math.max(...ns) : 0) + 1;
}
export default (a, { store, companyId }) => proximoTicket(store, a.p_company_id || companyId);
