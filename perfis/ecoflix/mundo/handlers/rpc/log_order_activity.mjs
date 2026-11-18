// log_order_activity(p_order_type, p_event_type, p_order_id, p_draft_id, p_metadata) — app 1.60.10, migration
// 20261116220000_origem_preco_itens_pedido.sql. Compra e Venda chamam ao abrir a edição de um pedido ("edit_opened") e ao trocar a
// tabela/origem do preço ("price_context_changed"); grava uma linha em order_activity_events e devolve o id (bigint). Aqui as mesmas
// validações e o mesmo retorno; a linha fica em `order_activity_events` (tabela vazia no mundo base; nenhuma tela das aulas lê).
// Usado por T07, T08, T09 e T21.
export default (a, ctx) => {
  const { store, db, companyId, userId, RpcError } = ctx;
  if (!companyId) throw new RpcError('Empresa do usuário não encontrada.', '42501');
  if (!['purchase', 'sale'].includes(a.p_order_type) || !['edit_opened', 'price_context_changed'].includes(a.p_event_type)) throw new RpcError('Evento de pedido inválido.', '22023');
  if (!a.p_order_id && !a.p_draft_id) throw new RpcError('Pedido ou rascunho é obrigatório.', '22023');
  const meta = a.p_metadata ?? {};
  if (typeof meta !== 'object' || Array.isArray(meta) || JSON.stringify(meta).length > 2048) throw new RpcError('Metadados do evento inválidos ou maiores que 2 KB.', '22023');
  let orderRef = null;
  if (a.p_order_id) {
    const p = store.rows(a.p_order_type === 'purchase' ? 'purchases' : 'sales').find((x) => x.id === a.p_order_id && x.company_id === companyId);
    if (!p) throw new RpcError('Pedido não encontrado nesta empresa.', '42501');
    orderRef = p.order_ref ?? null;
  }
  if (a.p_draft_id && !store.rows('order_drafts').some((d) => d.id === a.p_draft_id && d.company_id === companyId && d.type === a.p_order_type)) {
    throw new RpcError('Rascunho não encontrado nesta empresa.', '42501');
  }
  const proximo = store.rows('order_activity_events').reduce((m, e) => Math.max(m, Number(e.event_seq) || 0), 0) + 1;
  const limpo = Object.fromEntries(Object.entries(meta).filter(([, v]) => v !== null && v !== undefined));
  try {
    db.insert('order_activity_events', { event_seq: proximo, company_id: companyId, order_type: a.p_order_type, order_id: a.p_order_id || null, draft_id: a.p_draft_id || null, order_ref: orderRef, event_type: a.p_event_type, actor_id: userId || null, metadata: limpo }, { companyId });
  } catch { /* tabela fora do schema.json desta cópia: o retorno basta para a tela */ }
  return proximo;
};
