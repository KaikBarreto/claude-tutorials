// View `cost_resources_with_rate` (20260316040419_65562494-bab7-40ac-906f-eacfad3165bc.sql:5-25): cada recurso de custo com
//   total_monthly_cost = soma de cost_resource_items.value (o valor MENSAL; item anual já guarda value = anual / 12)
//   hourly_rate        = total_monthly_cost / monthly_hours (0 se as horas forem 0)
// Sem este provedor a aba "Custos Globais" nasce vazia e o "Custos dos Serviços" não acha o custo por hora do recurso.
export default function costResourcesWithRate(store) {
  const soma = new Map();
  for (const it of store.rows('cost_resource_items')) soma.set(it.resource_id, (soma.get(it.resource_id) || 0) + Number(it.value || 0));
  return store.rows('cost_resources').map((r) => {
    const total = soma.get(r.id) || 0;
    const horas = Number(r.monthly_hours || 0);
    return {
      id: r.id,
      company_id: r.company_id,
      category: r.category,
      name: r.name,
      is_active: r.is_active,
      monthly_hours: r.monthly_hours,
      notes: r.notes ?? null,
      photo_url: r.photo_url ?? null,
      created_at: r.created_at,
      updated_at: r.updated_at,
      total_monthly_cost: total,
      hourly_rate: horas > 0 ? total / horas : 0,
    };
  });
}
