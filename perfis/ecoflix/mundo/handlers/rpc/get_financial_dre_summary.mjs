// DRE do período (Dashboard e Relatório Financeiro): vendas, compras, CMV, despesas e receitas por categoria.
import { janela, resumoDRE } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => resumoDRE(store, a.p_company_id || companyId, janela(a.p_start_date, a.p_end_date), a.p_regime || 'caixa');
