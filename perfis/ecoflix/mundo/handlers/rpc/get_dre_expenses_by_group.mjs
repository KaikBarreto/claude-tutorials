// Despesas da DRE agrupadas (operacionais, impostos, custos), por empresa ou grupo; mesmo cálculo da DRE da empresa.
import { janela, categoriasDRE } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const ids = Array.isArray(a.p_company_ids) && a.p_company_ids.length ? a.p_company_ids : [companyId];
  const j = janela(a.p_start_date, a.p_end_date);
  const out = { operatingExpenses: [], taxExpenses: [], costExpenses: [], nonOperatingExpenses: [] };
  for (const cid of ids) {
    const c = categoriasDRE(store, cid, j);
    out.operatingExpenses.push(...c.despesas);
    out.taxExpenses.push(...c.impostos);
  }
  return out;
};
