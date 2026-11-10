// RPC sync_service_order_scope_with_services(_service_order_id, _items, _confirm_response_deletion)
//   · 20261019041000_protecao_escopo_e_distribuicao_orcamento.sql:92-196 (+ sync_service_order_scope, 20261014180000_...sql)
// _items = estado desejado completo: [{ equipment_id|null, service_type_ids[], form_template_ids[] }]. Regrava os pares
// equipamento x checklist em service_order_equipment (equipment_id nulo = checklist avulso; sem checklist = form_template_id nulo)
// e os serviços de cada equipamento em service_order_equipment_service_types. Sem esta RPC a OS nasce sem equipamento nem
// checklist e a tela do técnico (T7) abre vazia.
import { RpcError } from '../../http/rest.mjs';

export default async function syncServiceOrderScopeWithServices({ _service_order_id, _items }, { db, companyId }) {
  const os = db.first('service_orders', { id: _service_order_id });
  if (!os) throw new RpcError('Ordem de serviço não encontrada');
  const company = os.company_id || companyId;
  const items = Array.isArray(_items) ? _items : [];

  // pares desejados (equipamento, checklist) e serviços por equipamento
  const pairs = [];
  const services = [];
  for (const item of items) {
    const eq = item.equipment_id || null;
    if (eq) {
      const e = db.first('equipment', { id: eq });
      if (!e || e.company_id !== company) throw new RpcError('Equipamento inválido para esta empresa');
    }
    const tpls = Array.isArray(item.form_template_ids) && item.form_template_ids.length ? item.form_template_ids.map(String) : [null];
    for (const t of tpls) {
      if (t) {
        const ft = db.first('form_templates', { id: t });
        if (!ft || ft.company_id !== company) throw new RpcError('Checklist inválido para esta empresa');
      }
      if (!pairs.some((p) => p.eq === eq && p.t === t)) pairs.push({ eq, t });
    }
    if (eq && Array.isArray(item.service_type_ids)) {
      item.service_type_ids.forEach((st, position) => {
        if (!services.some((s) => s.eq === eq && s.st === String(st))) services.push({ eq, st: String(st), position });
      });
    }
  }
  for (const s of services) {
    if (!db.first('service_order_service_types', { service_order_id: _service_order_id, service_type_id: s.st })) {
      throw new RpcError('Serviço do equipamento não pertence a esta ordem de serviço');
    }
  }

  const same = (a, b) => (a ?? null) === (b ?? null);
  const current = db.find('service_order_equipment', { service_order_id: _service_order_id });
  let removed = 0;
  let inserted = 0;
  for (const row of current) {
    if (!pairs.some((p) => same(p.eq, row.equipment_id) && same(p.t, row.form_template_id))) {
      db.remove('service_order_equipment', (r) => r.id === row.id);
      removed++;
    }
  }
  for (const p of pairs) {
    if (!current.some((row) => same(p.eq, row.equipment_id) && same(p.t, row.form_template_id))) {
      db.insert('service_order_equipment', { service_order_id: _service_order_id, equipment_id: p.eq, form_template_id: p.t });
      inserted++;
    }
  }

  db.remove('service_order_equipment_service_types', (r) => r.service_order_id === _service_order_id && !services.some((s) => s.eq === r.equipment_id && s.st === r.service_type_id));
  for (const s of services) {
    const hit = db.first('service_order_equipment_service_types', (r) => r.service_order_id === _service_order_id && r.equipment_id === s.eq && r.service_type_id === s.st);
    if (hit) db.update('service_order_equipment_service_types', (r) => r === hit, { position: s.position });
    else db.insert('service_order_equipment_service_types', { service_order_id: _service_order_id, equipment_id: s.eq, service_type_id: s.st, company_id: company, position: s.position });
  }

  const equipment_services = db
    .find('service_order_equipment_service_types', { service_order_id: _service_order_id })
    .sort((a, b) => String(a.equipment_id).localeCompare(String(b.equipment_id)) || a.position - b.position)
    .map((r) => ({ equipment_id: r.equipment_id, service_type_id: r.service_type_id, position: r.position }));
  const scope = db.find('service_order_equipment', { service_order_id: _service_order_id }).map((r) => ({ equipment_id: r.equipment_id, form_template_id: r.form_template_id }));
  return { service_order_id: _service_order_id, removed, inserted, responses_deleted: 0, scope, equipment_services };
}
