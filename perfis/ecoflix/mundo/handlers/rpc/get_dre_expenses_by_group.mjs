// Despesas da DRE agrupadas (operacionais, impostos, custos), por empresa ou grupo; mesmo cálculo da DRE da empresa.
import { janela, categoriasDRE } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const ids = Array.isArray(a.p_company_ids) && a.p_company_ids.length ? a.p_company_ids : [companyId];
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
  return out;
};
