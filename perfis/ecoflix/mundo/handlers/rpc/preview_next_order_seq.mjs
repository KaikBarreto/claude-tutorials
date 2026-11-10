// Sequencial do próximo pedido: com numeração compartilhada e sem reinício (o padrão da empresa) é o próprio número.
import { proximoNumero } from '../../lib/eco.mjs';
export default (a, { store, companyId }) => proximoNumero(store, a.p_company_id || companyId);
