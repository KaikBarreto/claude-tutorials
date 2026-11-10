// Regras comuns dos dois portais públicos (T12): RPC get_portal_data, RPC create_customer_portal_ticket e função
// pmoc-portal-share. Espelha o banco/edge real da 1.38.9:
//   supabase/migrations/20261021140000_customer_portal_public_sections.sql (:97-495, :498-640)
//   supabase/migrations/20261031195000_customer_portal_equipment_labels.sql (etiquetas e campos por allowlist)
//   supabase/functions/pmoc-portal-share/index.ts
import { now } from '../core/util.mjs';

export const PORTAL_KEYS = ['service_orders', 'equipment', 'contracts', 'charges', 'invoices', 'documents', 'ticket_requests'];
export const DEFAULT_PERMISSIONS = {
  service_orders: true, equipment: true, contracts: true, charges: true, invoices: false, documents: false, ticket_requests: true,
};

/** normalize_customer_portal_permissions: chave ausente = padrão (tudo ligado, menos Notas fiscais e Documentos). */
export function normalizePermissions(raw) {
  const out = {};
  for (const k of PORTAL_KEYS) out[k] = typeof raw?.[k] === 'boolean' ? raw[k] : DEFAULT_PERMISSIONS[k];
  return out;
}

/** normalize_customer_portal_public_sections: só `true` explícito é seção livre (fail-closed). */
export function normalizePublicSections(raw) {
  const out = {};
  for (const k of PORTAL_KEYS) out[k] = raw?.[k] === true;
  return out;
}

const DAY = 86400000;
const utcDay = (d) => Math.floor(d.getTime() / DAY);

/** Vigência da assinatura da empresa, igual ao SQL (testing / active / pending_payment com bypass). */
export function subscriptionAllows(co) {
  if (!co) return false;
  const today = utcDay(now());
  const exp = co.subscription_expires_at ? new Date(co.subscription_expires_at) : null;
  const status = co.subscription_status;
  if (status === 'pending_payment' && co.payment_lock_bypass === true) return true;
  if (status === 'testing') return !!exp && utcDay(exp) >= today;
  if (status === 'active') return !exp || utcDay(exp) + 1 >= today;
  return false;
}

export function companyHasModule(db, companyId, code) {
  return db.rows('company_modules').some((m) => String(m.company_id) === String(companyId) && m.module_code === code);
}

export function companyDisplayName(db, companyId) {
  const cs = db.rows('company_settings').find((r) => String(r.company_id) === String(companyId));
  const n = (cs?.name || '').trim();
  if (n) return n;
  const co = db.first('companies', { id: companyId });
  return (co?.name || '').trim() || null;
}

/** Módulo "Portal do Cliente" ligado e assinatura vigente (vale para os dois portais). */
export function portalModuleAvailable(db, companyId) {
  const co = db.first('companies', { id: companyId });
  return subscriptionAllows(co) && companyHasModule(db, companyId, 'customer_portal');
}

/** Quem abre está logado numa conta ATIVA da empresa dona do portal (vê tudo, ignora senha). */
export function isCompanyMember(db, user, companyId) {
  if (!user?.id) return false;
  return db.rows('profiles').some((p) => String(p.user_id) === String(user.id) && String(p.company_id) === String(companyId) && p.is_active !== false);
}

export const firstName = (full) => {
  const t = String(full ?? '').trim();
  return t ? t.split(/\s+/)[0] : null;
};

export const technicianFirstName = (db, userId) => {
  if (!userId) return null;
  const p = db.rows('profiles').find((r) => String(r.user_id) === String(userId));
  return firstName(p?.full_name);
};

/** Campos personalizados do equipamento liberados para o portal (is_visible E is_visible_in_portal), na ordem da tela. */
export function portalFieldConfig(db, companyId) {
  return db
    .rows('equipment_field_config')
    .filter((f) => String(f.company_id) === String(companyId) && f.is_visible && f.is_visible_in_portal)
    .sort((a, b) => (a.position ?? 0) - (b.position ?? 0) || String(a.id).localeCompare(String(b.id)))
    .map((f) => ({ field_key: f.field_key, label: f.label, field_type: f.field_type, position: f.position, options: f.options ?? null }));
}

/** Etiquetas liberadas no portal (party_labels.show_in_portal E is_active) ligadas a uma linha de atribuição. */
function labelsOf(db, companyId, table, fkCol, fkValue) {
  return db
    .rows(table)
    .filter((a) => String(a.company_id) === String(companyId) && String(a[fkCol]) === String(fkValue))
    .sort((a, b) => (a.position ?? 0) - (b.position ?? 0))
    .map((a) => ({ a, l: db.first('party_labels', { id: a.label_id }) }))
    .filter(({ l }) => l && String(l.company_id) === String(companyId) && l.show_in_portal && l.is_active)
    .sort((x, y) => (x.a.position ?? 0) - (y.a.position ?? 0) || String(x.l.name).localeCompare(String(y.l.name), 'pt-BR'))
    .map(({ l }) => ({ id: l.id, name: l.name, color: l.color }));
}
export const customerLabels = (db, companyId, customerId) => labelsOf(db, companyId, 'customer_label_assignments', 'customer_id', customerId);
export const equipmentLabels = (db, companyId, equipmentId) => labelsOf(db, companyId, 'equipment_label_assignments', 'equipment_id', equipmentId);

/** Equipamento como o portal o recebe (sem `notes`; campos personalizados só os liberados). `withAttachments` = Portal do Cliente. */
export function projectEquipment(db, e, { companyId, allowedKeys, withAttachments }) {
  const cat = e.category_id ? db.first('equipment_categories', { id: e.category_id }) : null;
  const custom = Object.fromEntries(Object.entries(e.custom_fields || {}).filter(([k]) => allowedKeys.has(k)));
  const out = {
    id: e.id, name: e.name ?? null, brand: e.brand ?? null, model: e.model ?? null, serial_number: e.serial_number ?? null,
    location: e.location ?? null, status: e.status ?? null, photo_url: e.photo_url ?? null, identifier: e.identifier ?? null,
    capacity: e.capacity ?? null, install_date: e.install_date ?? null, warranty_until: e.warranty_until ?? null,
    category: cat ? { name: cat.name ?? null, color: cat.color ?? null } : null,
    custom_fields: custom,
    labels: equipmentLabels(db, companyId, e.id),
  };
  if (withAttachments) {
    out.attachments_public = e.attachments_public;
    out.attachments = e.attachments_public
      ? db.rows('equipment_attachments')
          .filter((a) => String(a.equipment_id) === String(e.id))
          .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)) || String(a.id).localeCompare(String(b.id)))
          .map((a) => ({ id: a.id, file_name: a.file_name, file_url: a.file_url, file_type: a.file_type }))
      : [];
  }
  return out;
}

export const byName = (a, b) => String(a.name ?? '').localeCompare(String(b.name ?? ''), 'pt-BR');

/** Hoje (AAAA-MM-DD) em Brasília no relógio do mundo falso (FAKE_NOW). */
export function todayBR() {
  const t = new Date(now().getTime() - 3 * 3600000);
  return t.toISOString().slice(0, 10);
}
