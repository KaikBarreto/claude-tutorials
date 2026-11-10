// Próximo número de pedido (compartilhado entre compras e vendas): maior order_number + 1.
import { proximoNumero } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => proximoNumero(store, a.p_company_id || companyId);
