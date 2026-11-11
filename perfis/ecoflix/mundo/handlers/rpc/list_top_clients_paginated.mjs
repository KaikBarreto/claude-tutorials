// list_top_clients_paginated(p_company_id, p_period_start, p_period_end, p_sort_by, p_limit, p_offset): o pódio "Clientes por venda"
// da Visão geral de Clientes e Fornecedores (components/clients-suppliers/EntitiesSummaryTab.tsx; T4 cap01) e o "Exportar" dele.
// Molde comum em list_top_suppliers_paginated.mjs (venda: sales_count).
import { ranking } from './list_top_suppliers_paginated.mjs';

export default (a, ctx) => ranking(a, ctx, 'sale');
