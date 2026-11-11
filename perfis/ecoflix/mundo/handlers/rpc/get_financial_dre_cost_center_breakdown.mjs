// Detalhamento do DRE por centro de custo (T15: a faixa por centro de custo da aba DRE, em competência): uma linha por categoria e
// centro, { source: income|expense|tax, name, costCenter, value }, com a mesma régua das categorias do DRE (lib/eco.mjs).
import { janela, categoriasDRE } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => {
  const c = categoriasDRE(store, a.p_company_id || companyId, janela(a.p_start_date, a.p_end_date));
  const out = [];
  for (const [source, lista] of [['income', c.receitas], ['expense', c.despesas], ['tax', c.impostos]]) {
    for (const cat of lista) for (const cc of cat.costCenters) out.push({ source, name: cat.name, costCenter: cc.name, value: cc.value });
  }
  return out;
};
