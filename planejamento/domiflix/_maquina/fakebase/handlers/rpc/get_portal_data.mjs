// RPC get_portal_data(p_token, p_session_token) · Portal do Cliente (T12).
// Espelha supabase/migrations/20261021140000_customer_portal_public_sections.sql (base :97-325 e involucro :334-489)
// e 20261031195000_customer_portal_equipment_labels.sql (etiquetas e campos de equipamento so por allowlist), versao 1.38.9.
// Sem senha de verdade no mundo falso: com senha ligada e visitante de fora, a sessao nunca vale (o T12 nao mostra o login).
import {
  PORTAL_KEYS, normalizePermissions, normalizePublicSections, portalModuleAvailable, companyDisplayName, isCompanyMember,
  technicianFirstName, portalFieldConfig, customerLabels, projectEquipment, byName,
} from '../../lib/portal.mjs';

const cmpDesc = (a, b) => String(b ?? '').localeCompare(String(a ?? ''));

export default async function getPortalData({ p_token }, { db, user }) {
  const portal = db.rows('customer_portals').find((p) => p.token === p_token && p.is_active !== false);
  if (!portal) return null;
  const customer = db.first('customers', { id: portal.customer_id });
  if (!customer || customer.is_deleted === true) return null;
  const companyId = customer.company_id;

  if (!portalModuleAvailable(db, companyId)) {
    return { access: 'module_unavailable', company_name: companyDisplayName(db, companyId) };
  }

  const member = isCompanyMember(db, user, companyId);
  if (portal.is_public === false && !member) return { access: 'denied' };

  const permissions = normalizePermissions(portal.permissions);
  const publicSections = normalizePublicSections(portal.public_sections);
  const authed = !portal.password_enabled || member;
  const visible = Object.fromEntries(PORTAL_KEYS.map((k) => [k, permissions[k] && (authed || publicSections[k])]));
  const locked = PORTAL_KEYS.filter((k) => permissions[k] && !visible[k]).sort();
  if (!authed && !PORTAL_KEYS.some((k) => visible[k])) return { access: 'password_required' };
  const partial = !authed;

  const cs = db.rows('company_settings').find((r) => String(r.company_id) === String(companyId));
  const company_settings = cs
    ? {
        name: cs.name ?? null, logo_url: cs.logo_url ?? null, phone: cs.phone ?? null, email: cs.email ?? null,
        address: cs.address ?? null, city: cs.city ?? null, state: cs.state ?? null,
        white_label_enabled: cs.white_label_enabled ?? false, white_label_primary_color: cs.white_label_primary_color ?? null,
        white_label_logo_url: cs.white_label_logo_url ?? null, white_label_icon_url: cs.white_label_icon_url ?? null,
        language: cs.language || 'pt-br', currency: cs.currency || 'BRL', timezone: cs.timezone || 'America/Sao_Paulo',
      }
    : null;

  // Equipamentos: todos do cliente (a lista do portal nao filtra por contrato), por nome.
  const allowedKeys = new Set(portalFieldConfig(db, companyId).map((f) => f.field_key));
  const fieldConfig = visible.equipment ? portalFieldConfig(db, companyId) : [];
  const equipment = visible.equipment
    ? db.rows('equipment')
        .filter((e) => String(e.customer_id) === String(customer.id))
        .sort(byName)
        .map((e) => projectEquipment(db, e, { companyId, allowedKeys, withAttachments: true }))
    : [];

  const service_orders = visible.service_orders
    ? db.rows('service_orders')
        .filter((so) => String(so.customer_id) === String(customer.id) && (so.entry_type ?? 'os') !== 'tarefa')
        .sort((a, b) => cmpDesc(a.created_at, b.created_at) || (b.order_number ?? 0) - (a.order_number ?? 0))
        .map((so) => ({
          id: so.id, order_number: so.order_number, status: so.status, description: so.description,
          scheduled_date: so.scheduled_date ?? null, created_at: so.created_at, os_type: so.os_type ?? null,
          equipment_id: so.equipment_id ?? null, entry_type: so.entry_type ?? 'os',
          service_type_name: so.service_type_id ? db.first('service_types', { id: so.service_type_id })?.name ?? null : null,
          technician_name: technicianFirstName(db, so.technician_id),
          team_name: so.team_id ? db.first('teams', { id: so.team_id })?.name ?? null : null,
        }))
    : [];

  const contracts = visible.contracts
    ? db.rows('contracts')
        .filter((c) => String(c.customer_id) === String(customer.id) && String(c.company_id) === String(companyId) && ['active', 'paused'].includes(c.status))
        .sort(byName)
        .map((c) => ({
          id: c.id, name: c.name, is_pmoc: c.is_pmoc ?? false, status: c.status,
          next_maintenance_date: c.next_pmoc_generation_date ?? null,
          public_short_code: c.public_short_code ?? null, public_pmoc_token: c.public_pmoc_token ?? null,
        }))
    : [];

  const charges = visible.charges
    ? db.rows('tenant_charges')
        .filter((t) => String(t.company_id) === String(companyId) && String(t.customer_id) === String(customer.id) && !['CANCELLED', 'CANCELED'].includes(t.status))
        .sort((a, b) => (a.due_date == null) - (b.due_date == null) || cmpDesc(a.due_date, b.due_date) || cmpDesc(a.created_at, b.created_at))
        .slice(0, 50)
        .map((t) => ({
          value: t.value, status: t.status, due_date: t.due_date ?? null, description: t.description ?? null,
          billing_type: t.billing_type ?? null, public_short_code: t.public_short_code ?? null,
        }))
    : [];

  // Involucro: notas fiscais e documentos (so quando liberados e nao protegidos).
  const invoices = permissions.invoices && !locked.includes('invoices')
    ? db.rows('customer_documents')
        .filter((d) => String(d.company_id) === String(companyId) && String(d.customer_id) === String(customer.id) && d.document_kind === 'invoice' && d.is_visible_in_portal)
        .sort((a, b) => cmpDesc(a.issue_date, b.issue_date) || cmpDesc(a.created_at, b.created_at))
        .map((d) => ({
          id: d.id, source: 'manual', title: d.title, description: d.description ?? null, document_type: d.document_type ?? null,
          document_number: d.document_number ?? null, issue_date: d.issue_date ?? null, amount: d.amount ?? null,
          file_name: d.file_name ?? null, mime_type: d.mime_type ?? null, size_bytes: d.size_bytes ?? null, created_at: d.created_at,
        }))
    : [];
  let documents = [];
  if (permissions.documents && !locked.includes('documents')) {
    const manual = db.rows('customer_documents')
      .filter((d) => String(d.company_id) === String(companyId) && String(d.customer_id) === String(customer.id) && d.document_kind === 'document' && d.is_visible_in_portal)
      .map((d) => ({
        id: d.id, source: 'manual', title: d.title, description: d.description ?? null, document_type: d.document_type ?? null,
        file_name: d.file_name ?? null, mime_type: d.mime_type ?? null, size_bytes: d.size_bytes ?? null, created_at: d.created_at,
      }));
    const anexos = db.rows('contract_attachments')
      .map((a) => ({ a, ct: db.first('contracts', { id: a.contract_id }) }))
      .filter(({ a, ct }) => ct && String(ct.customer_id) === String(customer.id) && String(a.company_id) === String(companyId) && ct.portal_documents_released === true)
      .map(({ a, ct }) => ({
        id: a.id, source: 'contract_attachment', title: a.display_name, description: ct.name, document_type: 'contract',
        file_name: a.display_name, mime_type: a.mime_type ?? null, size_bytes: a.size_bytes ?? null, created_at: a.created_at,
      }));
    documents = [...manual, ...anexos].sort((a, b) => cmpDesc(a.created_at, b.created_at));
  }

  return {
    access: 'granted',
    viewer_can_fill: member,
    partial,
    locked_sections: locked,
    permissions,
    // No modo parcial so id e nome saem (PII nao vaza); inteiro, o bloco leva company_id e as etiquetas liberadas.
    customer: partial
      ? { id: customer.id, name: customer.name }
      : { id: customer.id, name: customer.name, company_id: companyId, labels: customerLabels(db, companyId, customer.id) },
    company_settings,
    equipment_field_config: fieldConfig,
    equipment,
    service_orders,
    contracts,
    charges,
    invoices,
    documents,
  };
}
