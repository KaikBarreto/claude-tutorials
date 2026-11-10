// RPC reset_service_order(_service_order_id, _clear_responses) · 20261017161000_allow_reset_service_order_in_progress.sql:6-148
// "Resetar OS" / "Reabrir OS": só vale para a caminho, em andamento, pausada e concluída; devolve a OS a "Agendada" e zera
// check-in/out e carimbos; com _clear_responses apaga também diagnóstico, solução, assinaturas, respostas, fotos e posições.
// Sempre apaga as avaliações ainda sem resposta. Sem esta RPC o toast diz "OS resetada" e nada muda.
import { RpcError } from '../../http/rest.mjs';

export default async function resetServiceOrder({ _service_order_id, _clear_responses = false }, { db }) {
  const os = db.first('service_orders', { id: _service_order_id });
  if (!os) throw new RpcError('Ordem de servico nao encontrada');
  if (!['a_caminho', 'em_andamento', 'pausada', 'concluida'].includes(os.status)) {
    throw new RpcError('Esta ordem de servico nao possui um atendimento iniciado para resetar');
  }
  const patch = {
    status: 'agendada',
    check_in_time: null, check_in_location: null, check_in_by: null,
    check_out_time: null, check_out_location: null, check_out_by: null,
    started_at: null, paused_at: null, resumed_at: null, completed_at: null, partial_finish: false,
  };
  if (_clear_responses) {
    Object.assign(patch, {
      diagnosis: null, solution: null,
      tech_signature: null, tech_signature_at: null, tech_signed_by: null, tech_signed_location: null,
      client_signature: null, client_signature_at: null, client_signed_by: null, client_signed_location: null,
      pmoc_conformity_status: null, pmoc_conformity_notes: null,
    });
  }
  db.update('service_orders', { id: _service_order_id }, patch);
  let responses = 0, photos = 0, locations = 0;
  if (_clear_responses) {
    responses = db.remove('form_responses', { service_order_id: _service_order_id }).length;
    photos = db.remove('os_photos', { service_order_id: _service_order_id }).length;
    locations = db.remove('technician_locations', { service_order_id: _service_order_id }).length;
  }
  db.remove('service_ratings', (r) => r.service_order_id === _service_order_id && !r.rated_at);
  return {
    service_order_id: _service_order_id, status: 'agendada', responses_cleared: !!_clear_responses,
    form_responses_deleted: responses, activities_cleared: 0, photos_deleted: photos, locations_deleted: locations,
  };
}
