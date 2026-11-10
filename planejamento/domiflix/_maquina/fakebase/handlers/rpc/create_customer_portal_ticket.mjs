// RPC create_customer_portal_ticket(p_token, p_session_token, p_description, p_equipment_id) · chamado pelo Portal do Cliente (T12).
// Espelha supabase/migrations/20261021140000_customer_portal_public_sections.sql :496-609: valida portal, acesso, permissao,
// assinatura/modulo, descricao (10 a 2000) e vinculo do equipamento; insere a OS "pendente" (origem portal, corretiva, sem data
// e sem tecnico). db.insert nao passa pelos hooks do REST: a numeracao vem da sequencia de service_orders (nextSeq).
import { RpcError } from '../../http/rest.mjs';
import { nextSeq } from '../../core/defaults.mjs';
import {
  normalizePermissions, normalizePublicSections, portalModuleAvailable, isCompanyMember,
} from '../../lib/portal.mjs';

const deny = (msg, code = '42501') => new RpcError(msg, code, 403);

export default async function createCustomerPortalTicket({ p_token, p_description, p_equipment_id = null }, { db, user }) {
  const portal = db.rows('customer_portals').find((p) => p.token === p_token && p.is_active !== false);
  if (!portal) throw deny('Portal indisponivel');
  const customer = db.first('customers', { id: portal.customer_id });
  const companyId = customer && customer.is_deleted !== true ? customer.company_id : null;
  const member = isCompanyMember(db, user, companyId);

  const permissions = normalizePermissions(portal.permissions);
  const free = permissions.ticket_requests && normalizePublicSections(portal.public_sections).ticket_requests;
  if (portal.is_public === false && !member) throw deny('Acesso negado');
  // Com senha, so abre quem for da empresa ou quando "Abrir chamados" esta livre (sessao de portal nao existe no mundo falso).
  if (portal.password_enabled && !member && !free) throw deny('Acesso negado');
  if (!permissions.ticket_requests) throw deny('Abertura de chamados desativada neste portal');
  if (!companyId || !portalModuleAvailable(db, companyId)) throw deny('Portal indisponivel');

  const text = String(p_description ?? '').trim();
  if (text.length < 10 || text.length > 2000) throw new RpcError('A descricao precisa ter entre 10 e 2000 caracteres', '22023', 400);
  if (p_equipment_id) {
    const eq = db.first('equipment', { id: p_equipment_id });
    if (!eq || String(eq.customer_id) !== String(portal.customer_id) || String(eq.company_id) !== String(companyId)) {
      throw new RpcError('Equipamento invalido', '22023', 400);
    }
  }

  const row = db.insert('service_orders', {
    order_number: nextSeq('service_orders', 'order_number', db.rows('service_orders')),
    customer_id: portal.customer_id,
    equipment_id: p_equipment_id || null,
    description: text,
    os_type: 'manutencao_corretiva',
    status: 'pendente',
    origin: 'portal',
    company_id: companyId,
  });
  return { ok: true, service_order_id: row.id };
}
