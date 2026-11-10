// RPC get_or_create_ponto_kiosk_slug(p_company_id) → text · hooks/usePontoAdmin.ts:30 (T15, cap. 8)
// Slug do link do quiosque (/ponto/empresa/<slug>): criado na primeira chamada, depois sempre o mesmo. Fixo e fictício.
export default async function getOrCreatePontoKioskSlug() {
  return 'glacial-cold-q7m4k2xw';
}
