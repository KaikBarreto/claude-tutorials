// Custo do insumo + o degrau da cascata que produziu o número (T11, prévia de custo da ordem de produção):
// [{ cost, basis_used, is_fallback }], como a função SQL da 1.59.154 (20260923180000). A régua vem de companies.production_cost_basis.
import { custoComRegua } from '../../lib/producao.mjs';

export default (a, { store, companyId }) => [custoComRegua(store, a.p_company_id || companyId, a.p_material_id)];
