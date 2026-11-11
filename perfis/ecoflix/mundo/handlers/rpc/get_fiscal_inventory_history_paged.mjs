// Kardex fiscal paginado (Estoque Fiscal > "Histórico fiscal", T17 cap10), como a RPC do banco (migration 20261023221000):
// saldo contínuo (balance_before/after) calculado no livro inteiro antes dos filtros; página em ordem decrescente.
import { kardex } from '../../lib/estoque_fiscal.mjs';

export default (a, { store, companyId }) => kardex(store, a.p_company_id || companyId, a);
