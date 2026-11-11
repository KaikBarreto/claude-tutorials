// Muda a etapa da ordem de coleta (20261008150000_change_collection_order_status_atomico.sql): só para a frente, uma etapa por vez
// (solicitada → agendada → a_caminho → coletada; cancelada de qualquer etapa aberta); agendar pede data e janela (e frota, se as
// Configurações exigirem); grava completed_at, o evento do Histórico e, ao concluir, as movimentações do bloco Entreguei/Recolhi.
import { STATUS_LABEL, PROXIMOS, agoraIso, sincronizarEquipamentos } from '../../lib/coletas.mjs';

export default (a, { store, db, userId, RpcError }) => {
  const o = store.rows('collection_orders').find((x) => x.id === a.p_order_id);
  if (!a.p_order_id) throw new RpcError('Informe qual ordem de coleta vai mudar de situação.');
  const to = String(a.p_to || '').trim();
  if (!STATUS_LABEL[to]) throw new RpcError(`A situação "${to || '(vazia)'}" não existe para ordem de coleta.`);
  if (!o) throw new RpcError('Ordem de coleta não encontrada.');
  const cfg = store.rows('collection_settings').find((s) => s.company_id === o.company_id) || {};
  const numero = `${cfg.order_number_prefix || ''}${o.numero}`;
  const from = o.status;
  const perm = PROXIMOS[from] || [];
  if (from === to) {
    throw new RpcError(`A ordem de coleta nº ${numero} já está em "${STATUS_LABEL[from]}" — essa mudança já foi registrada (outro clique seu ou outro usuário). Atualize a tela para ver a situação atual.`);
  }
  if (!perm.includes(to)) {
    if (!perm.length) throw new RpcError(`A ordem de coleta nº ${numero} está "${STATUS_LABEL[from]}" e não muda mais de situação. Crie uma nova ordem se precisar registrar outra coleta.`);
    const lista = [...perm].sort().map((s) => `"${STATUS_LABEL[s]}"`).join(' ou ');
    throw new RpcError(`Não dá para mudar a ordem de coleta nº ${numero} de "${STATUS_LABEL[from]}" direto para "${STATUS_LABEL[to]}". De "${STATUS_LABEL[from]}" só dá para ir para ${lista}.`);
  }
  const fleet = a.p_fleet && typeof a.p_fleet === 'object' ? a.p_fleet : null;
  const tem = (k) => !!fleet && Object.prototype.hasOwnProperty.call(fleet, k);
  const janela = String(a.p_scheduled_window || '').trim() || null;
  if (to === 'agendada') {
    const drv = tem('driver_id') ? fleet.driver_id || null : o.driver_id;
    const vei = tem('vehicle_id') ? fleet.vehicle_id || null : o.vehicle_id;
    if (cfg.require_driver_vehicle && (!drv || !vei)) throw new RpcError('Defina motorista e veículo antes de agendar.');
    if (!a.p_scheduled_date || !janela) throw new RpcError('Defina a data e a janela da coleta para agendar.');
  }
  const agora = agoraIso();
  const set = { status: to, completed_at: to === 'coletada' ? agora : null, updated_at: agora };
  if (to === 'agendada') {
    Object.assign(set, { scheduled_date: a.p_scheduled_date, scheduled_window: janela });
    for (const k of ['driver_id', 'driver_name', 'vehicle_id', 'vehicle_plate']) if (tem(k)) set[k] = fleet[k] || null;
  }
  db.update('collection_orders', { id: o.id }, set);
  const ev = db.insert('collection_order_events', {
    company_id: o.company_id, order_id: o.id, event_type: 'status_change', from_status: from, to_status: to,
    nota: String(a.p_nota || '').trim() || null, created_by: userId || null, created_at: agora,
  });
  const equip = to === 'coletada' ? sincronizarEquipamentos(db, store, o, a.p_equipment_lines || [], userId) : null;
  return { status: 'changed', order_id: o.id, company_id: o.company_id, numero: o.numero, numero_formatado: numero, from, to,
    completed_at: set.completed_at, event_id: ev.id, equipamentos: equip };
};
