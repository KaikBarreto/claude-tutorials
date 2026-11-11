// Despesas da DRE agrupadas (operacionais, impostos, custos), por empresa ou grupo; mesmo cálculo da DRE da empresa.
import { janela, categoriasDRE, r2 } from '../../lib/eco.mjs';
import { empresasDoGrupo } from '../../lib/grupo.mjs';
// T22: com p_group_id e sem p_company_ids valem a dona e os membros ativos do grupo, e a mesma categoria de empresas diferentes vira UMA linha
// (o SQL agrupa por lower(btrim(nome)) e grupo da DRE); com uma empresa só nada muda.
const junta = (lista) => {
  const m = new Map();
  for (const d of lista) {
    const k = String(d.name).trim().toLowerCase();
    const e = m.get(k);
    if (!e) { m.set(k, { ...d, costCenters: [...(d.costCenters || [])] }); continue; }
    e.value = r2(e.value + d.value);
    e.costCenters.push(...(d.costCenters || []));
  }
  return [...m.values()].sort((x, y) => y.value - x.value);
};
export default (a, { store, companyId }) => {
  const ids = Array.isArray(a.p_company_ids) && a.p_company_ids.length ? a.p_company_ids : a.p_group_id ? empresasDoGrupo(store, a.p_group_id) : [companyId];
  const j = janela(a.p_start_date, a.p_end_date);
  const out = { operatingExpenses: [], taxExpenses: [], costExpenses: [], nonOperatingExpenses: [] };
  for (const cid of ids) {
    const c = categoriasDRE(store, cid, j);
    // como o SQL (20261020174500): a lista sai pelo dre_group da categoria (custos, não operacionais); 'outros' (Não compõe o DRE) fica fora
    const grupo = new Map(store.rows('financial_categories').filter((f) => f.company_id === cid && f.type === 'expense').map((f) => [f.name, f.dre_group]));
    for (const d of c.despesas) {
      const g = grupo.get(d.name);
      if (g !== 'outros') (g === 'custos' ? out.costExpenses : g === 'nao_operacionais' ? out.nonOperatingExpenses : out.operatingExpenses).push(d);
    }
    out.taxExpenses.push(...c.impostos);
  }
  if (ids.length > 1) for (const k of Object.keys(out)) out[k] = junta(out[k]);
  return out;
};
