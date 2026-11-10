// RPC generate_service_order_from_quote(p_quote_id, p_equipment_services) · 20261019041000_protecao_escopo_e_distribuicao_orcamento.sql:198-352
// (valor trocado em 20261027120000_orcamento_total_comercial_na_conversao_os.sql: a OS recebe `total_value`, o total comercial).
// Cria UMA OS 'agendada' (sem data nem técnico) do orçamento APROVADO, copia as linhas para o orçamento da OS, liga os tipos de serviço e a
// distribuição por equipamento, aplica o checklist ativo do serviço no equipamento e marca o orçamento 'convertido'. Idempotente.
// NÃO mexe em estoque nem em financeiro. Sem este handler o toast "OS gerada com sucesso!" aparece e nada é criado.
import { RpcError } from '../../http/rest.mjs';
import { nextSeq } from '../../core/defaults.mjs';

const r2 = (n) => Math.round((n + Number.EPSILON) * 100) / 100;

// Regra da migracao: cost_bdi se o orcamento usa BDI, nao ha price_override e ha custo; senao registered (preco = cadastrado) ou manual.
function pricingDoItem(i, q) {
  const num0 = (v) => Math.max(0, Number(v) || 0);
  const custo = num0(i.unit_total_cost);
  let mode = 'manual';
  if ((q.use_bdi ?? false) && i.price_override == null && custo > 0) mode = 'cost_bdi';
  return {
    pricing_mode: mode,
    unit_hourly_rate: num0(i.unit_hourly_rate), unit_hours: num0(i.unit_hours), unit_labor_cost: num0(i.unit_labor_cost),
    unit_materials_cost: num0(i.unit_materials_cost), unit_extras_cost: num0(i.unit_extras_cost), unit_total_cost: custo,
    profit_rate: num0(i.profit_rate), bdi: Math.max(0.01, i.bdi ?? 0.68),
    price_override: mode === 'cost_bdi' ? null : i.price_override ?? i.unit_price,
  };
}

export default async function generateServiceOrderFromQuote({ p_quote_id, p_equipment_services }, { db, userId }) {
  const q = db.first('quotes', { id: p_quote_id });
  if (!q) throw new RpcError('Orçamento não encontrado ou sem permissão.');
  if (q.converted_to_os_id) {
    const ja = db.first('service_orders', { id: q.converted_to_os_id });
    if (ja) return ja;
  }
  if (q.status !== 'aprovado') throw new RpcError('Apenas orçamentos aprovados podem gerar uma OS.');
  const lista = Array.isArray(p_equipment_services) ? p_equipment_services : [];

  // distribuição (equipamento, serviço), sem repetição
  const dist = [];
  for (const it of lista) {
    for (const sid of Array.isArray(it?.service_type_ids) ? it.service_type_ids : []) {
      if (it.equipment_id && sid && !dist.some((d) => d.equipment_id === it.equipment_id && d.service_type_id === sid)) dist.push({ equipment_id: it.equipment_id, service_type_id: sid });
    }
  }
  const itens = db.find('quote_items', { quote_id: q.id }).sort((a, b) => (a.position ?? 0) - (b.position ?? 0) || String(a.created_at).localeCompare(String(b.created_at)));
  for (const d of dist) {
    const eq = db.first('equipment', { id: d.equipment_id });
    if (!eq || String(eq.customer_id) !== String(q.customer_id)) throw new RpcError('Um equipamento não pertence ao cliente deste orçamento.');
    if (!itens.some((i) => i.service_type_id === d.service_type_id)) throw new RpcError('Um serviço distribuído não pertence a este orçamento.');
  }
  const comServico = itens.filter((i) => i.service_type_id);
  if (dist.length && comServico.some((i) => !dist.some((d) => d.service_type_id === i.service_type_id))) throw new RpcError('Distribua todos os serviços do orçamento antes de gerar a OS.');
  if (!dist.length && comServico.length && db.find('equipment', { customer_id: q.customer_id }).length) throw new RpcError('Distribua os serviços entre os equipamentos antes de gerar a OS.');

  const servicos = itens.filter((i) => ['servico', 'mao_de_obra'].includes(i.item_type)).reduce((s, i) => s + Number(i.total_price || 0), 0);
  const materiais = itens.filter((i) => i.item_type === 'material').reduce((s, i) => s + Number(i.total_price || 0), 0);
  const totalItens = itens.reduce((s, i) => s + Number(i.total_price || 0), 0);
  const total = q.total_value ?? q.total_price ?? totalItens ?? 0;
  const equipamentoPrincipal = [...dist].map((d) => d.equipment_id).sort()[0] ?? null;

  const os = db.insert('service_orders', {
    company_id: q.company_id,
    order_number: nextSeq('service_orders', 'order_number', db.rows('service_orders')),
    customer_id: q.customer_id,
    equipment_id: equipamentoPrincipal,
    service_type_id: comServico[0]?.service_type_id ?? null,
    status: 'agendada',
    entry_type: 'os',
    origin: 'manual',
    labor_value: r2(servicos),
    parts_value: r2(materiais),
    total_value: r2(Number(total)),
    description: `Gerada do Orçamento #${q.quote_number}`,
    notes: q.notes ?? null,
    quote_id: q.id,
    created_by: userId,
    // 1.38.19 (20261103133000): a OS herda o snapshot de BDI do orcamento; commercial_adjustment = total comercial - soma dos itens
    use_bdi: q.use_bdi ?? false,
    tax_rate: q.tax_rate ?? 10,
    admin_indirect_rate: q.admin_indirect_rate ?? 12,
    profit_rate: q.profit_rate ?? 10,
    bdi: Math.max(0.01, q.bdi ?? 0.68),
    total_cost: Math.max(0, q.total_cost ?? 0),
    km_cost: Math.max(0, q.km_cost ?? 0),
    distance_km: Math.max(0, q.distance_km ?? 0),
    displacement_cost: Math.max(0, q.displacement_cost ?? 0),
    commercial_adjustment: r2(Number(total) - totalItens),
  });

  itens.forEach((i, pos) => {
    db.insert('service_order_budget_items', {
      service_order_id: os.id, company_id: q.company_id, position: i.position ?? pos,
      item_type: ['servico', 'mao_de_obra', 'material'].includes(i.item_type) ? i.item_type : 'servico',
      description: i.description, details: i.details ?? null, quantity: i.quantity, unit_price: i.unit_price,
      total_price: r2(Number(i.quantity) * Number(i.unit_price)), inventory_id: i.inventory_id ?? null,
      service_type_id: i.service_type_id ?? null, source_quote_item_id: i.id,
      ...pricingDoItem(i, q),
    });
  });

  // tipos de serviço da OS, na ordem da 1ª aparição no orçamento
  const tipos = [];
  for (const i of comServico) if (!tipos.includes(i.service_type_id)) tipos.push(i.service_type_id);
  tipos.forEach((sid, position) => db.insert('service_order_service_types', { service_order_id: os.id, service_type_id: sid, company_id: q.company_id, position }));

  // distribuição por equipamento (posição dentro do equipamento, pela ordem do serviço na OS)
  const porEquip = new Map();
  for (const d of dist) porEquip.set(d.equipment_id, [...(porEquip.get(d.equipment_id) || []), d.service_type_id]);
  for (const [equipment_id, sids] of porEquip) {
    sids.sort((a, b) => tipos.indexOf(a) - tipos.indexOf(b) || String(a).localeCompare(String(b)));
    sids.forEach((service_type_id, position) =>
      db.insert('service_order_equipment_service_types', { service_order_id: os.id, equipment_id, service_type_id, company_id: q.company_id, position }));
    // checklist ativo ligado a qualquer serviço daquele equipamento: aplicado uma única vez; sem checklist, o equipamento fica no escopo
    const modelos = new Set();
    for (const sid of sids) {
      for (const lig of db.find('form_template_service_types', { service_type_id: sid })) {
        const ft = db.first('form_templates', { id: lig.template_id });
        if (ft && ft.company_id === q.company_id && ft.is_active) modelos.add(ft.id);
      }
    }
    if (modelos.size) for (const form_template_id of modelos) db.insert('service_order_equipment', { service_order_id: os.id, equipment_id, form_template_id });
    else db.insert('service_order_equipment', { service_order_id: os.id, equipment_id, form_template_id: null });
  }

  db.update('quotes', { id: q.id }, { converted_to_os_id: os.id, status: 'convertido' });
  return os;
}
