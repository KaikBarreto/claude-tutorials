// get_or_create_ponto_kiosk_slug (Configurações de Ponto > "Tablet da empresa", T19 cap08), como a função da 1.59.154 (migration
// 20260926131000_ponto_kiosk_slug_codigo_12.sql): devolve companies.ponto_kiosk_slug; sem ele, cria {empresa}-{CÓDIGO12}.
import { codigo } from './generate_ponto_slug.mjs';

export default (a, { store, companyId, RpcError }) => {
  const c = store.rows('companies').find((x) => x.id === (a.p_company_id || companyId));
  if (!c) throw new RpcError(`Empresa ${a.p_company_id} não encontrada`);
  if (c.ponto_kiosk_slug) return c.ponto_kiosk_slug;
  const nome = String(c.name || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-+|-+$)/g, '') || 'empresa';
  c.ponto_kiosk_slug = `${nome}-${codigo('t19-kiosk:' + c.name)}`;
  store.table('companies').touch();
  return c.ponto_kiosk_slug;
};
