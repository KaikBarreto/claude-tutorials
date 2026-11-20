// Excluir ordem de coleta de verdade (20260925050000_collection_order_delete_and_multi_select.sql): recusa, com o texto do banco, a ordem
// que já movimentou equipamento ou tem checklist respondido (a tela mostra "Não deu para excluir" e oferece cancelar); senão apaga a
// ordem, os eventos e os placeholders de checklist.
import { agoraIso } from '../../lib/coletas.mjs';

export default (a, { store, db, RpcError }) => {
  if (!a.p_order_id) throw new RpcError('Informe qual ordem de coleta será excluída.');
  const o = store.rows('collection_orders').find((x) => x.id === a.p_order_id);
  if (!o) throw new RpcError('Ordem de coleta não encontrada.');
  const cfg = store.rows('collection_settings').find((s) => s.company_id === o.company_id) || {};
  const numero = `${cfg.order_number_prefix || ''}${o.numero}`;
  const movs = store.rows('collection_equipment_movements').filter((m) => m.collection_order_id === o.id);
  const anuladas = movs.filter((m) => m.voided).length;
  const resp = store.rows('collection_checklist_responses').filter((r) => r.collection_order_id === o.id);
  const respondidas = resp.filter((r) => r.resposta !== null && r.resposta !== undefined || r.foto_path).length;
  const fotos = resp.filter((r) => r.foto_path).length;
  const motivos = [];
  if (movs.length) {
    motivos.push(`já movimentou equipamento (${movs.length} movimentaç${movs.length === 1 ? 'ão' : 'ões'} no histórico${anuladas ? `, sendo ${anuladas} anulada${anuladas === 1 ? '' : 's'}` : ''})`);
  }
  if (respondidas) {
    motivos.push(`já tem checklist respondido (${respondidas} pergunta${respondidas === 1 ? '' : 's'} respondida${respondidas === 1 ? '' : 's'}${fotos ? `, ${fotos} com foto` : ''})`);
  }
  if (motivos.length) {
    throw new RpcError(`Não dá para excluir a ordem de coleta nº ${numero}: ela ${motivos.join(' e ')}. Cancele a ordem em vez de excluir — assim o histórico de equipamento e o checklist continuam intactos.`);
  }
  const eventos = store.rows('collection_order_events').filter((e) => e.order_id === o.id).length;
  db.remove('collection_order_events', (e) => e.order_id === o.id);
  db.remove('collection_checklist_responses', (r) => r.collection_order_id === o.id);
  db.remove('collection_orders', (x) => x.id === o.id);
  return { status: 'deleted', order_id: o.id, company_id: o.company_id, numero: o.numero, numero_formatado: numero, status_anterior: o.status,
    public_short_code_revogado: o.public_short_code || null, eventos_removidos: eventos, checklist_placeholders_removidos: resp.length - respondidas, at: agoraIso() };
};
