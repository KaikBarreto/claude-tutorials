// Mapa de Coletas (20260925070000_collection_driver_tracking.sql): a última posição de cada motorista da empresa nos últimos p_minutes,
// agrupada por driver_id (ou user_id), com o nome do motorista e o número da ordem.
import { agoraMs } from '../../lib/eco.mjs';

export default (a, { store, companyId }) => {
  const co = a.p_company_id || companyId;
  const min = Math.max(Number(a.p_minutes) || 30, 1);
  const corte = agoraMs() - min * 60000;
  const ultimo = new Map();
  for (const l of store.rows('collection_driver_locations').filter((x) => x.company_id === co && Date.parse(x.created_at) >= corte)) {
    const k = l.driver_id || l.user_id;
    const p = ultimo.get(k);
    if (!p || Date.parse(l.created_at) > Date.parse(p.created_at)) ultimo.set(k, l);
  }
  return [...ultimo.entries()].map(([k, l]) => {
    const d = store.rows('drivers').find((x) => x.id === l.driver_id);
    const o = store.rows('collection_orders').find((x) => x.id === l.order_id);
    return { driver_key: k, driver_id: l.driver_id || null, driver_name: d?.name || null, user_id: l.user_id, order_id: l.order_id || null,
      order_numero: o?.numero ?? null, event_type: l.event_type, lat: l.lat, lng: l.lng, accuracy_m: l.accuracy_m ?? null, speed_kmh: l.speed_kmh ?? null,
      heading_deg: l.heading_deg ?? null, recorded_at: l.recorded_at, created_at: l.created_at };
  }).sort((x, y) => Date.parse(y.created_at) - Date.parse(x.created_at));
};
