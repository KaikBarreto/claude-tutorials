// VIEW contract_health_status · 20260523164907_pmoc_v1_9_0_fundacao.sql (T11).
// Um registro por contrato: overdue_count = OSs do contrato com scheduled_date < hoje e status fora de (concluida, cancelada);
// health_status = em_dia (0) | manutencao_pendente (1) | necessita_atencao (2 ou mais). "Hoje" = o relógio do mundo (FAKE_NOW) no fuso do Brasil.
import { todayBR } from '../../lib/portal.mjs';

export default function contractHealthStatus(store) {
  const hoje = todayBR();
  const atrasadas = new Map();
  for (const o of store.rows('service_orders')) {
    if (!o.contract_id || !o.scheduled_date || o.scheduled_date >= hoje || ['concluida', 'cancelada'].includes(o.status)) continue;
    atrasadas.set(o.contract_id, (atrasadas.get(o.contract_id) || 0) + 1);
  }
  return store.rows('contracts').map((c) => {
    const n = atrasadas.get(c.id) || 0;
    return { contract_id: c.id, company_id: c.company_id, overdue_count: n, health_status: n === 0 ? 'em_dia' : n === 1 ? 'manutencao_pendente' : 'necessita_atencao' };
  });
}
