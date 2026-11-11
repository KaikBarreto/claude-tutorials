// Extratos OFX importados da conta (conciliação): nenhum no mundo base (o T14 importa o arquivo na tela). Como a função SQL: só abertos e
// finalizados, abertos primeiro, com o progresso de cada um (total, pendentes, diferença) calculado pelo lib/conciliacao.mjs (T14).
import { resumoImport } from '../../lib/conciliacao.mjs';

export default (a, { store }) => store.rows('bank_statement_imports')
  .filter((i) => i.bank_account_id === a.p_bank_account_id && ['open', 'finalized'].includes(i.status))
  .sort((x, y) => Number(y.status === 'open') - Number(x.status === 'open') || String(y.created_at).localeCompare(String(x.created_at)))
  .map((i) => resumoImport(store, i));
