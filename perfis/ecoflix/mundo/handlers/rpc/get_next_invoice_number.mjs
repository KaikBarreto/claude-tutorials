// RPC get_next_invoice_number (useNextInvoiceNumber, "Número previsto" e a faixa da emissão em massa): a próxima NF-e da série.
import { proximoNumero } from '../../lib/nfe.mjs';

export default (a, { store, companyId }) => proximoNumero(store, a.p_company_id || companyId, a.p_serie, a.p_fiscal_config_id);
