// RPC edit_service_order_scope(_service_order_id, _items) · 1.38.20:
//   supabase/migrations/20261104190000_edit_os_scope_movimenta_respostas_e_ordena.sql
// _items = estado desejado completo: [{ equipment_id|null, form_template_ids[], moves?: [{ form_template_id, from_equipment_id|null }] }].
//   · equipment_id nulo = checklists sem equipamento; form_template_ids vazio = equipamento sem checklist (linha com form_template_id nulo);
//   · posições: equipment_position = índice do item, checklist_position = índice do checklist na lista do item;
//   · moves: a MESMA linha de service_order_equipment troca de equipamento e as form_responses do checklist (da OS) vão junto
//     (responses_moved); nada é apagado nem recriado;
//   · pares que saíram do desejado: apaga as respostas (responses_deleted) e a linha; pares novos: insere; regrava as posições.
// Textos de erro = os que EditOsScopeDrawer.mapRpcError reconhece. Aqui o usuário é sempre o técnico logado, com permissão.
import { RpcError } from '../../http/rest.mjs';

const same = (a, b) => (a ?? null) === (b ?? null);
const nz = (v) => (v === undefined || v === '' ? null : v);

export default async function editServiceOrderScope({ _service_order_id, _items }, { db, companyId }) {
  const os = db.first('service_orders', { id: _service_order_id });
  if (!os) throw new RpcError('Ordem de serviço não encontrada');
  const company = os.company_id || companyId;
  if (companyId && os.company_id && os.company_id !== companyId) throw new RpcError('Sem acesso a esta ordem de serviço');
  if (os.contract_id) {
    const ct = db.first('contracts', { id: os.contract_id });
    if (ct?.is_pmoc === true) throw new RpcError('Edição manual indisponível em OS de PMOC');
  }

  // estado desejado
  const items = Array.isArray(_items) ? _items : [];
  const desired = [];
  items.forEach((item, ei) => {
    const eq = nz(item.equipment_id);
    const tpls = Array.isArray(item.form_template_ids) && item.form_template_ids.length ? item.form_template_ids.map((t) => nz(t)) : [null];
    tpls.forEach((t, ti) => {
      if (!desired.some((d) => same(d.eq, eq) && same(d.t, t))) desired.push({ eq, t, ep: ei, cp: ti });
    });
  });
  for (const d of desired) {
    if (d.eq) {
      const e = db.first('equipment', { id: d.eq });
      if (!e || e.company_id !== company || String(e.customer_id) !== String(os.customer_id)) throw new RpcError('Equipamento inválido para esta ordem de serviço');
    }
    if (d.t) {
      const ft = db.first('form_templates', { id: d.t });
      if (!ft || ft.company_id !== company) throw new RpcError('Checklist inválido para esta ordem de serviço');
    }
  }

  // movimentos
  const moves = [];
  for (const item of items) {
    for (const m of Array.isArray(item.moves) ? item.moves : []) {
      moves.push({ from: nz(m.from_equipment_id), to: nz(item.equipment_id), t: nz(m.form_template_id) });
    }
  }
  if (moves.some((m, i) => moves.findIndex((o) => same(o.from, m.from) && o.t === m.t) !== i)) throw new RpcError('Movimento de checklist duplicado');
  const inScope = (eq, t) => db.find('service_order_equipment', { service_order_id: _service_order_id }).some((r) => same(r.equipment_id, eq) && r.form_template_id === t);
  for (const m of moves) {
    if (same(m.from, m.to) || !m.t || !inScope(m.from, m.t) || !desired.some((d) => same(d.eq, m.to) && d.t === m.t)) throw new RpcError('Movimento de checklist inválido');
  }
  if (moves.some((m) => inScope(m.to, m.t))) throw new RpcError('Este checklist já existe no destino');

  // 1) a própria linha troca de equipamento; 2) as respostas vão junto
  let moved = 0;
  let responsesMoved = 0;
  for (const m of moves) {
    moved += db.update('service_order_equipment', (r) => r.service_order_id === _service_order_id && same(r.equipment_id, m.from) && r.form_template_id === m.t, { equipment_id: m.to }).length;
    const qids = new Set(db.find('form_questions', { template_id: m.t }).map((q) => q.id));
    responsesMoved += db.update('form_responses', (r) => r.service_order_id === _service_order_id && same(r.equipment_id, m.from) && qids.has(r.question_id), { equipment_id: m.to }).length;
  }

  // pares que saíram: respostas e linha
  const current = () => db.find('service_order_equipment', { service_order_id: _service_order_id });
  const out = current().filter((row) => !desired.some((d) => same(d.eq, row.equipment_id) && same(d.t, row.form_template_id)));
  let responsesDeleted = 0;
  for (const row of out) {
    if (!row.form_template_id) continue;
    const qids = new Set(db.find('form_questions', { template_id: row.form_template_id }).map((q) => q.id));
    const gone = db.remove('form_responses', (r) => r.service_order_id === _service_order_id && same(r.equipment_id, row.equipment_id) && qids.has(r.question_id));
    responsesDeleted += gone.length;
  }
  const removed = db.remove('service_order_equipment', (r) => out.includes(r)).length;

  // pares novos
  let inserted = 0;
  for (const d of desired) {
    if (!current().some((row) => same(row.equipment_id, d.eq) && same(row.form_template_id, d.t))) {
      db.insert('service_order_equipment', { service_order_id: _service_order_id, equipment_id: d.eq, form_template_id: d.t, equipment_position: d.ep, checklist_position: d.cp });
      inserted++;
    }
  }
  // posições
  for (const d of desired) {
    db.update('service_order_equipment', (r) => r.service_order_id === _service_order_id && same(r.equipment_id, d.eq) && same(r.form_template_id, d.t), { equipment_position: d.ep, checklist_position: d.cp });
  }

  const scope = current()
    .slice()
    .sort((a, b) => a.equipment_position - b.equipment_position || a.checklist_position - b.checklist_position || String(a.id).localeCompare(String(b.id)))
    .map((r) => ({ id: r.id, equipment_id: r.equipment_id, form_template_id: r.form_template_id, equipment_position: r.equipment_position, checklist_position: r.checklist_position }));
  return { service_order_id: _service_order_id, removed, inserted, moved, responses_deleted: responsesDeleted, responses_moved: responsesMoved, scope };
}
