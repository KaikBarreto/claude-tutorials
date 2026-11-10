// RPC preview_service_order_scope_removal(_service_order_id, _items) · 20261019041000_protecao_escopo_e_distribuicao_orcamento.sql:8-91
// Conta as respostas de checklist que seriam apagadas se o escopo encolhesse (o aviso "Existem respostas preenchidas").
// O mundo do T5 não tem respostas de checklist: o aviso nunca aparece.
export default async function previewServiceOrderScopeRemoval({ _service_order_id }, { db }) {
  const os = db.first('service_orders', { id: _service_order_id });
  return { answered_responses: 0, checklists: 0, contract_protected: !!os?.contract_id };
}
