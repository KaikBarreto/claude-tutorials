// Posição fiscal numa data/hora do passado ("Data e hora da posição" > "Ver posição", T17 cap10), como a RPC do banco
// (migration 20261029130000): os movimentos e o saldo inicial até p_as_of. Só consulta: não grava nada.
import { posicao } from '../../lib/estoque_fiscal.mjs';

export default (a, { store, companyId, RpcError }) => {
  const ate = new Date(a.p_as_of).getTime();
  if (!Number.isFinite(ate)) throw new RpcError('Informe a data e a hora da posição.');
  return posicao(store, a.p_company_id || companyId, a.p_fiscal_config_id || null, ate);
};
