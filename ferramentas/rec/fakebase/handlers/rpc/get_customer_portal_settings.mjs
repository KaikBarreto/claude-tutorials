// Portal do cliente: leitura das configuracoes (a funcao real do banco devolve um objeto json ou null).
import { PORTALS_WITH_PASSWORD } from './save_customer_portal_settings.mjs';

export default async function getCustomerPortalSettings({ p_customer_id }, { db }) {
  const row = db.first('customer_portals', { customer_id: p_customer_id });
  if (!row) return null;
  return {
    token: row.token,
    is_active: row.is_active,
    password_enabled: row.password_enabled,
    password_configured: PORTALS_WITH_PASSWORD.has(row.customer_id),
    permissions: row.permissions,
    public_sections: row.public_sections,
  };
}
