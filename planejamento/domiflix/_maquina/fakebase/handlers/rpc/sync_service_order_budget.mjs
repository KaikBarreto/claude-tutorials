// RPC sync_service_order_budget(p_service_order_id, p_items) · 20261018231000_orcamento_da_os_e_gerar_os.sql:381-541
// Substitui as linhas do orçamento da OS (total_price = qtd x preço, 2 casas) e reconcilia labor_value (serviços + mão de obra),
// parts_value (materiais) e total_value na OS: o "Valor da OS" da pergunta de receita, o "Faturar OS" e o KPI "Faturamento" partem daí.
import { RpcError } from '../../http/rest.mjs';

const r2 = (n) => Math.round((n + Number.EPSILON) * 100) / 100;

// 1.38.19 (20261103133000_os_budget_bdi_methodology.sql): `p_pricing` (opcional) grava a metodologia de BDI na OS e nos itens.
// Sem `p_pricing` o comportamento anterior e identico (campos de BDI ficam nos padroes do schema).
const num = (v, d = 0) => (v == null || v === '' || !Number.isFinite(Number(v)) ? d : Number(v));
const pos = (v, d = 0) => Math.max(0, num(v, d));

export default async function syncServiceOrderBudget({ p_service_order_id, p_items, p_pricing }, { db, companyId }) {
  const items = Array.isArray(p_items) ? p_items : p_items == null ? [] : null;
  if (!items) throw new RpcError('Os itens do orçamento devem ser uma lista.');
  if (items.length > 200) throw new RpcError('O orçamento da OS aceita no máximo 200 itens.');
  const os = db.first('service_orders', { id: p_service_order_id });
  if (!os) throw new RpcError('Ordem de serviço não encontrada ou sem permissão.');
  for (const it of items) {
    const type = it.item_type || 'servico';
    if (!String(it.description ?? '').trim() || !(Number(it.quantity) > 0) || Number(it.unit_price ?? 0) < 0 || !['servico', 'mao_de_obra', 'material'].includes(type)) {
      throw new RpcError('Revise descrição, quantidade, tipo e valor dos itens do orçamento.');
    }
  }
  const pr = p_pricing && typeof p_pricing === 'object' && !Array.isArray(p_pricing) ? p_pricing : null;
  const tax = num(pr?.tax_rate, 10), adm = num(pr?.admin_indirect_rate, 12), prof = num(pr?.profit_rate, 10);
  if (pr && (tax < 0 || adm < 0 || prof < 0)) throw new RpcError('Revise as taxas de impostos, administração e lucro.');
  const bdi = Math.max(0.01, (100 - (tax + adm + prof)) / 100);
  db.remove('service_order_budget_items', { service_order_id: p_service_order_id });
  let services = 0;
  let materials = 0;
  let totalCost = 0;
  items.forEach((it, position) => {
    const type = it.item_type || 'servico';
    const total = r2(Number(it.quantity) * Number(it.unit_price ?? 0));
    if (type === 'material') materials += total;
    else services += total;
    db.insert('service_order_budget_items', {
      service_order_id: p_service_order_id,
      company_id: os.company_id || companyId,
      position,
      item_type: type,
      description: String(it.description).trim(),
      details: it.details || null,
      quantity: Number(it.quantity),
      unit_price: r2(Number(it.unit_price ?? 0)),
      total_price: total,
      inventory_id: it.inventory_id || null,
      service_type_id: it.service_type_id || null,
      source_quote_item_id: it.source_quote_item_id || null,
      ...(pr ? {
        pricing_mode: it.pricing_mode || 'manual',
        unit_hourly_rate: pos(it.unit_hourly_rate), unit_hours: pos(it.unit_hours), unit_labor_cost: pos(it.unit_labor_cost),
        unit_materials_cost: pos(it.unit_materials_cost), unit_extras_cost: pos(it.unit_extras_cost), unit_total_cost: pos(it.unit_total_cost),
        profit_rate: pos(it.profit_rate, prof), bdi: Math.max(0.01, num(it.bdi, bdi)),
        price_override: (it.pricing_mode || 'manual') === 'cost_bdi' ? null : r2(num(it.price_override ?? it.unit_price)),
      } : {}),
    });
    totalCost += Number(it.quantity) * (pr ? pos(it.unit_total_cost) : 0);
  });
  const adj = pr ? r2(num(pr.commercial_adjustment)) : 0;
  const out = { labor_value: r2(services), parts_value: r2(materials), total_value: r2(services + materials + adj) };
  const patch = pr ? {
    ...out, use_bdi: pr.use_bdi === true || pr.use_bdi === 'true', tax_rate: tax, admin_indirect_rate: adm, profit_rate: prof, bdi, total_cost: r2(totalCost),
    km_cost: pos(pr.km_cost), distance_km: pos(pr.distance_km), displacement_cost: pos(pr.displacement_cost), commercial_adjustment: adj,
  } : out;
  db.update('service_orders', { id: p_service_order_id }, patch);
  return pr ? { ...out, total_cost: patch.total_cost, use_bdi: patch.use_bdi, bdi } : out;
}
