// RPC nfse_month_usage(p_company_id) -> int · 1.38.24 (supabase/migrations/20261105013000_nfse_ambiente_canonico.sql):
// notas do mês-calendário corrente em Brasília (por created_at), sem rascunho nem falha, e SEM as de homologação
// (homologação não tem efeito fiscal e não consome a franquia; `fiscal_ambiente` nulo, legado, continua contando).
import { now } from '../../core/util.mjs';

const FORA = new Set(['rascunho', 'rejeitada', 'falhou', 'rejected', 'failed', 'error', 'erro']);
const mesBR = (iso) => {
  const t = new Date(new Date(iso).getTime() - 3 * 3600 * 1000);
  return `${t.getUTCFullYear()}-${String(t.getUTCMonth() + 1).padStart(2, '0')}`;
};

export function usoDoMes(db, companyId) {
  const mes = mesBR(now().toISOString());
  return db.find('nfse_emissions', (e) => e.company_id === companyId && e.created_at && mesBR(e.created_at) === mes
    && e.fiscal_ambiente !== 'homologacao' && !FORA.has(String(e.status || '').toLowerCase())).length;
}

export default async function nfseMonthUsage({ p_company_id }, { db, companyId }) {
  return usoDoMes(db, p_company_id || companyId);
}
