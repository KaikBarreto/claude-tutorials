// RPC nfse_can_emit(p_company_id) -> jsonb · supabase/migrations/20260615210000_nfse_tiers_and_quota.sql (+ uso da 1.38.24):
//   { allowed, used, limit, tier, unlimited, next_tier: { tier, name, limit, price } | null }
// Nível de `companies.nfse_tier` (0/nulo = 1, o DEFAULT do banco); catálogo de `nfse_tiers` (semente) ou, sem semente,
// o da própria migration. `used` não conta notas de homologação (nfse_month_usage da 1.38.24).
import { usoDoMes } from './nfse_month_usage.mjs';

const CATALOGO = [
  { tier: 1, name: 'Nível 1', monthly_limit: 200, price: 100 },
  { tier: 2, name: 'Nível 2', monthly_limit: 500, price: 200 },
  { tier: 3, name: 'Nível 3', monthly_limit: 1000, price: 300 },
  { tier: 4, name: 'Nível 4 (Ilimitado)', monthly_limit: null, price: 400 },
];

export default async function nfseCanEmit({ p_company_id }, { db }) {
  if (!p_company_id) return { allowed: false, used: 0, limit: 0, tier: 1, unlimited: false, next_tier: null };
  const semeado = db.rows('nfse_tiers');
  const cat = semeado.length ? semeado : CATALOGO;
  const emp = db.first('companies', { id: p_company_id });
  let tier = Number(emp?.nfse_tier) || 1;
  if (!cat.some((t) => Number(t.tier) === tier)) tier = 1;
  const atual = cat.find((t) => Number(t.tier) === tier);
  const prox = cat.find((t) => Number(t.tier) === tier + 1);
  const next = prox ? { tier: Number(prox.tier), name: prox.name, limit: prox.monthly_limit ?? null, price: Number(prox.price) } : null;
  const used = usoDoMes(db, p_company_id);
  const limit = atual?.monthly_limit ?? null;
  if (limit == null) return { allowed: true, used, limit: null, tier, unlimited: true, next_tier: next };
  return { allowed: used < limit, used, limit, tier, unlimited: false, next_tier: next };
}
