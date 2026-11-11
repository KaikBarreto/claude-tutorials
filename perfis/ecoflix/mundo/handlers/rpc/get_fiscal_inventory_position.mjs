// Posição fiscal atual por CNPJ/material (Estoque Fiscal > "Posição do estoque", T17 cap10), como a RPC do banco
// (migration 20261023221000): saldo inicial ativo como base; sem ele, soma o histórico e marca has_opening_balance=false.
import { posicao } from '../../lib/estoque_fiscal.mjs';

export default (a, { store, companyId }) => posicao(store, a.p_company_id || companyId, a.p_fiscal_config_id || null);
