// Portal do cliente: grava as configuracoes (cria o portal na primeira vez, com token proprio).
import crypto from 'node:crypto';
import { RpcError } from '../../http/rest.mjs';

export const PORTALS_WITH_PASSWORD = new Set();

export default async function saveCustomerPortalSettings(args, { db }) {
  const id = args.p_customer_id;
  if (!db.first('customers', { id })) throw new RpcError('Cliente não encontrado', 'P0002', 404);
  const patch = {
    customer_id: id,
    is_active: args.p_is_active ?? true,
    password_enabled: !!args.p_password_enabled,
    permissions: args.p_permissions ?? {},
    public_sections: args.p_public_sections ?? {},
  };
  const existing = db.first('customer_portals', { customer_id: id });
  const row = existing
    ? db.update('customer_portals', { customer_id: id }, patch)[0]
    : db.insert('customer_portals', { ...patch, token: crypto.randomBytes(16).toString('hex') });
  if (args.p_password_enabled && args.p_password) PORTALS_WITH_PASSWORD.add(id);
  if (!args.p_password_enabled) PORTALS_WITH_PASSWORD.delete(id);
  return {
    token: row.token,
    is_active: row.is_active,
    password_enabled: row.password_enabled,
    password_configured: PORTALS_WITH_PASSWORD.has(id),
    permissions: row.permissions,
    public_sections: row.public_sections,
  };
}
