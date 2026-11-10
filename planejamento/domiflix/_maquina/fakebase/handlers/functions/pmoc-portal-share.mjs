// Edge function `pmoc-portal-share` falsa · Portal do Contrato (T12). GET ?token=<32 hex | nome-do-contrato-codigo>.
// Espelha supabase/functions/pmoc-portal-share/index.ts da 1.38.9 (payload 1.13.0, types/pmocPortal.ts): modulo, privacidade,
// tres estados por secao (portal_sections: ausente = livre), OS do contrato, documentos liberados, equipamentos e cobrancas.
// Sem senha de verdade no mundo falso: secao "Com senha" fica trancada para quem nao e da empresa.
import { FunctionError } from '../../http/functions.mjs';
import { now, nowIso } from '../../core/util.mjs';
import {
  companyHasModule, companyDisplayName, isCompanyMember, technicianFirstName, portalFieldConfig, projectEquipment, byName, todayBR,
} from '../../lib/portal.mjs';

const SECTION_KEYS = ['visao_geral', 'equipamentos', 'cronograma', 'ocorrencias', 'documentos', 'historico', 'historico_pmoc', 'cobrancas'];
const NAV_KEY = (k) => k.replace('_', '-');
const SCHEDULE_STATUS = ['pendente', 'agendada', 'a_caminho', 'em_andamento', 'pausada'];
const STATUS_OS_LABEL = {
  pendente: 'Pendente', agendada: 'Agendada', a_caminho: 'A caminho', em_andamento: 'Em andamento', pausada: 'Pausada', concluida: 'Concluída',
};
const STATUS_CONTRACT_LABEL = { active: 'Ativo', paused: 'Pausado', inactive: 'Inativo', cancelled: 'Cancelado' };
const DOC_TYPES = ['dossie_pmoc', 'cronograma_anual', 'termo_rt', 'certificado'];
const DOC_LABELS = {
  dossie_pmoc: 'Dossiê PMOC (Capa + Termo + Certificado)', cronograma_anual: 'Cronograma 12 meses',
  termo_rt: 'Termo de Responsabilidade Técnica (TRT)', certificado: 'Certificado de Conformidade',
};
const SIG_RELEVANT = new Set(['termo_rt', 'dossie_pmoc', 'certificado']);
const SHORT_CODE = /^[a-hj-np-z2-9]{12}$/;

function frequencyLabel(value, type) {
  if (!value || !type) return '—';
  const v = Math.max(1, Math.round(value));
  if (type === 'months') return { 1: 'Mensal', 2: 'Bimestral', 3: 'Trimestral', 6: 'Semestral', 12: 'Anual' }[v] || `A cada ${v} meses`;
  if (type === 'days') return v === 1 ? 'Diária' : `A cada ${v} dias`;
  if (type === 'weeks') return v === 1 ? 'Semanal' : `A cada ${v} semanas`;
  if (type === 'years') return v === 1 ? 'Anual' : `A cada ${v} anos`;
  return `A cada ${v} ${type}`;
}
const truncate = (s, max) => {
  const t = String(s ?? '').trim();
  return t.length <= max ? t : `${t.slice(0, max)}…`;
};
const first = (full) => {
  const t = String(full ?? '').trim();
  return t ? t.split(/\s+/)[0] : null;
};
const asc = (a, b) => (a == null) - (b == null) || String(a ?? '').localeCompare(String(b ?? ''));

/** Saude do contrato: a view `contract_health_status` do banco; sem linha semeada, calcula pelas visitas vencidas. */
function health(db, contract) {
  let row = null;
  try {
    row = db.rows('contract_health_status').find((r) => String(r.contract_id) === String(contract.id)) || null;
  } catch {
    row = null;
  }
  if (row) return { status: row.health_status ?? 'em_dia', overdue: row.overdue_count ?? 0 };
  const today = todayBR();
  const overdue = db.rows('service_orders').filter(
    (o) => String(o.contract_id) === String(contract.id) && SCHEDULE_STATUS.includes(o.status) && o.scheduled_date && o.scheduled_date < today,
  ).length;
  return { status: overdue === 0 ? 'em_dia' : overdue <= 2 ? 'manutencao_pendente' : 'necessita_atencao', overdue };
}

export default async function pmocPortalShare(_body, { db, user, url }) {
  const param = url.searchParams.get('token');
  if (!param) throw new FunctionError('token_required', 400);
  let col;
  let val;
  if (/^[0-9a-f]{32}$/.test(param)) {
    col = 'public_pmoc_token';
    val = param;
  } else {
    const code = param.split('-').pop() ?? '';
    if (!SHORT_CODE.test(code)) throw new FunctionError('invalid_token_format', 400);
    col = 'public_short_code';
    val = code;
  }
  const contract = db.rows('contracts').find((c) => c[col] === val);
  if (!contract) throw new FunctionError('not_found', 404);
  if (contract.status === 'cancelled' || contract.status === 'inactive') throw new FunctionError('not_found', 404);
  const companyId = contract.company_id;
  const isPmoc = contract.is_pmoc === true;

  if (!companyHasModule(db, companyId, 'contracts')) return { error: 'module_unavailable', company_name: companyDisplayName(db, companyId) };
  const member = isCompanyMember(db, user, companyId);
  if (contract.portal_is_public === false && !member) return { access: 'denied', company_name: companyDisplayName(db, companyId) };

  const raw = contract.portal_sections || {};
  const state = (k) => (raw[k] === 'password' || raw[k] === 'hidden' ? raw[k] : 'free');
  const canServe = (k) => {
    if (member) return true;
    const s = state(k);
    return s === 'hidden' ? false : s === 'free';
  };
  const configured = SECTION_KEYS.filter((k) => state(k) !== 'free');
  const hasPassword = SECTION_KEYS.some((k) => state(k) === 'password');
  const hidden = SECTION_KEYS.filter((k) => !member && state(k) === 'hidden').map(NAV_KEY);
  const locked = SECTION_KEYS.filter((k) => state(k) === 'password' && !canServe(k)).map(NAV_KEY);
  const isPartial = locked.length > 0;
  if (!SECTION_KEYS.some(canServe) && hasPassword) return { access: 'password_required', company_name: companyDisplayName(db, companyId) };

  const customer = db.first('customers', { id: contract.customer_id });
  const overview = canServe('visao_geral');
  const rt = contract.responsible_technician_id && overview ? db.first('responsible_technicians', { id: contract.responsible_technician_id }) : null;
  const cs = db.rows('company_settings').find((r) => String(r.company_id) === String(companyId)) || {};
  const tenantName = (cs.name || '').trim() || (db.first('companies', { id: companyId })?.name || '').trim() || 'Empresa';
  const wl = cs.white_label_enabled === true;
  const h = overview ? health(db, contract) : null;

  // OS do contrato: cronograma (futuras e ativas, ate 7 dias atrasadas), historico (concluidas) e ocorrencias (todas menos canceladas).
  const floorDate = new Date(now().getTime() - 7 * 86400000).toISOString().slice(0, 10); // a edge usa o dia UTC de 7 dias atras
  const mine = db.rows('service_orders').filter((o) => String(o.contract_id) === String(contract.id));
  const projectOs = (o) => {
    const assignee = db.rows('service_order_assignees').find((a) => String(a.service_order_id) === String(o.id));
    const rating = db.rows('service_ratings').find((r) => String(r.service_order_id) === String(o.id) && r.rated_at);
    return {
      number: o.order_number ?? null,
      scheduled_date: o.scheduled_date ?? null,
      completed_at: o.completed_at ?? null,
      status: o.status,
      status_label: STATUS_OS_LABEL[o.status] ?? '—',
      service_type_label: o.service_type_id ? db.first('service_types', { id: o.service_type_id })?.name ?? null : null,
      public_description: truncate(o.description, 200),
      technician_first_name: first(technicianFirstName(db, assignee?.user_id ?? o.technician_id)),
      public_photos: db.rows('os_photos').filter((p) => String(p.service_order_id) === String(o.id) && p.photo_url).map((p) => ({ url: p.photo_url, alt: 'Foto da manutenção' })),
      rating: rating?.quality_rating ?? null,
      rating_comment: rating?.comment ?? null,
    };
  };
  const history = canServe('historico')
    ? mine.filter((o) => o.status === 'concluida').sort((a, b) => String(b.completed_at ?? '').localeCompare(String(a.completed_at ?? ''))).slice(0, 20).map(projectOs)
    : [];
  const schedule = canServe('cronograma')
    ? mine.filter((o) => SCHEDULE_STATUS.includes(o.status) && (o.scheduled_date ?? '') >= floorDate)
        .sort((a, b) => asc(a.scheduled_date, b.scheduled_date)).slice(0, 50).map(projectOs)
    : [];
  const occurrences = canServe('ocorrencias')
    ? mine.filter((o) => o.status !== 'cancelada').sort((a, b) => asc(a.scheduled_date, b.scheduled_date)).slice(0, 70).map((o) => ({ id: o.id, ...projectOs(o) }))
    : [];

  // Documentos (so PMOC e so liberados): ultima versao de cada tipo, link "assinado" falso.
  const releasedRaw = isPmoc && contract.portal_documents_released === true;
  const released = releasedRaw && canServe('documentos');
  let documents = [];
  if (released) {
    const rows = db.rows('pmoc_documents').filter((d) => String(d.contract_id) === String(contract.id) && String(d.company_id) === String(companyId));
    documents = DOC_TYPES.map((type) => {
      const latest = rows.filter((d) => d.doc_type === type).sort((a, b) => (b.version ?? 0) - (a.version ?? 0))[0];
      if (!latest) {
        return { type, label: DOC_LABELS[type], available: false, version: null, generated_at: null, pdf_url: null, signature_status: SIG_RELEVANT.has(type) ? 'pending' : null, valid_until: null };
      }
      const n = latest.notes;
      const sig = !SIG_RELEVANT.has(type) ? null : n && String(n).startsWith('signature:') ? (String(n).split(':')[1] === 'pending' ? 'pending' : 'signed') : null;
      return {
        type, label: DOC_LABELS[type], available: true, version: latest.version, generated_at: latest.generated_at,
        pdf_url: `http://${process.env.FAKE_HOST || '127.0.0.1'}:${process.env.FAKE_PORT || 54321}/storage/v1/object/sign/pmoc-documents/${latest.pdf_storage_path}?token=fake`,
        signature_status: sig, valid_until: latest.valid_until ?? null,
      };
    });
  }
  const attachmentsReleased = contract.portal_documents_released === true && canServe('documentos');
  const attachments = attachmentsReleased
    ? db.rows('contract_attachments')
        .filter((a) => String(a.contract_id) === String(contract.id) && String(a.company_id) === String(companyId))
        .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)))
        .map((a) => ({
          id: a.id, label: a.display_name ?? 'Documento', available: true,
          pdf_url: `http://${process.env.FAKE_HOST || '127.0.0.1'}:${process.env.FAKE_PORT || 54321}/storage/v1/object/sign/contract-attachments/${a.storage_path}?token=fake`,
          generated_at: a.created_at ?? null, mime_type: a.mime_type ?? null, size_bytes: a.size_bytes ?? null,
        }))
    : [];

  let executionHistory = [];
  if (releasedRaw && canServe('historico_pmoc')) {
    let acts = [];
    try {
      acts = db.rows('service_order_activities');
    } catch {
      acts = [];
    }
    const osById = new Map(mine.map((o) => [o.id, o]));
    executionHistory = acts
      .filter((a) => osById.has(a.service_order_id) && a.freq_code)
      .map((a) => {
        const o = osById.get(a.service_order_id);
        return {
          service_order_id: a.service_order_id, order_number: o.order_number ?? null, scheduled_date: o.scheduled_date ?? null,
          visit_conformity: o.pmoc_conformity_status ?? null, activity_id: a.id, equipment_id: a.equipment_id ?? null,
          equipment_name: a.equipment_id ? db.first('equipment', { id: a.equipment_id })?.name ?? null : null,
          section: a.section ?? null, component: a.component ?? null, description: a.description ?? '', freq_code: a.freq_code,
          is_measurement: a.is_measurement ?? null, measured_value: a.measured_value ?? null, unit: a.unit ?? null,
          conformity_status: ['conforme', 'nao_conforme', 'na'].includes(a.conformity_status) ? a.conformity_status : null,
          sort_order: a.sort_order ?? null, responded_at: a.responded_at ?? null,
          responded_by_name: a.responded_by ? db.first('profiles', { user_id: a.responded_by })?.full_name ?? null : null,
        };
      })
      .sort((x, y) => (x.scheduled_date !== y.scheduled_date ? (x.scheduled_date < y.scheduled_date ? 1 : -1) : (x.sort_order ?? 0) - (y.sort_order ?? 0)));
  }

  // Equipamentos da unidade (sem `notes`, campos personalizados so os liberados no portal; sem anexos).
  let equipment = [];
  let fieldConfig = [];
  if (contract.customer_id && canServe('equipamentos')) {
    fieldConfig = portalFieldConfig(db, companyId);
    const allowed = new Set(fieldConfig.map((f) => f.field_key));
    equipment = db.rows('equipment')
      .filter((e) => String(e.customer_id) === String(contract.customer_id) && String(e.company_id) === String(companyId))
      .sort(byName)
      .map((e) => projectEquipment(db, e, { companyId, allowedKeys: allowed, withAttachments: false }));
  }

  const charges = canServe('cobrancas')
    ? db.rows('tenant_charges')
        .filter((t) => String(t.company_id) === String(companyId) && String(t.customer_id) === String(contract.customer_id) && !['CANCELLED', 'CANCELED'].includes(t.status))
        .sort((a, b) => (a.due_date == null) - (b.due_date == null) || String(b.due_date ?? '').localeCompare(String(a.due_date ?? '')))
        .slice(0, 50)
        .map((t) => ({ value: t.value ?? null, status: t.status ?? null, due_date: t.due_date ?? null, description: t.description ?? null, billing_type: t.billing_type ?? null, public_short_code: t.public_short_code ?? null }))
    : [];

  const reducePii = isPartial && !member;
  const payload = {
    generated_at: nowIso(),
    payload_version: '1.13.0',
    access: 'granted',
    viewer_can_fill: member && canServe('ocorrencias'),
    is_pmoc: isPmoc,
    unit: {
      name: customer?.name ?? null,
      address: reducePii ? null : customer?.address ?? null,
      city: reducePii ? null : customer?.city ?? null,
      state: reducePii ? null : customer?.state ?? null,
    },
    contract: overview
      ? {
          id: reducePii ? null : contract.id ?? null,
          customer_id: reducePii ? null : contract.customer_id ?? null,
          company_id: reducePii ? null : companyId ?? null,
          name: contract.name ?? null,
          start_date: contract.start_date ?? null,
          frequency_label: frequencyLabel(contract.frequency_value ?? null, contract.frequency_type ?? null),
          next_pmoc_generation_date: contract.next_pmoc_generation_date ?? null,
          next_maintenance_date: contract.next_pmoc_generation_date ?? null,
          compliance_text: contract.pmoc_legal_compliance_text ?? 'Conforme Lei Federal 13.589/2018',
          status_label: STATUS_CONTRACT_LABEL[contract.status] ?? '—',
          health_status: h.status,
          overdue_count: h.overdue,
        }
      : {
          id: null, customer_id: null, company_id: null, name: contract.name ?? null, start_date: null, frequency_label: '—',
          next_pmoc_generation_date: null, next_maintenance_date: null, compliance_text: '', status_label: '', health_status: null, overdue_count: 0,
        },
    ...(overview ? { health: { status: h.status, overdue_count: h.overdue } } : {}),
    responsible_technician: rt
      ? {
          full_name: rt.full_name ?? null,
          cft_crea: reducePii ? null : rt.cft_crea ?? null,
          modality: rt.modality ?? null,
          registry_number: reducePii ? null : rt.registry_number ?? null,
        }
      : null,
    tenant: {
      name: tenantName,
      logo_url: wl ? cs.white_label_logo_url ?? cs.logo_url ?? null : cs.logo_url ?? null,
      primary_color: wl ? cs.white_label_primary_color ?? null : null,
      address: cs.address ?? null, city: cs.city ?? null, state: cs.state ?? null,
      white_label_enabled: wl,
      document: cs.document ?? null, phone: cs.phone ?? null, email: cs.email ?? null, zip_code: cs.zip_code ?? null,
      report_header: wl
        ? {
            bg_color: cs.report_header_bg_color ?? null, text_color: cs.report_header_text_color ?? null, logo_size: cs.report_header_logo_size ?? null,
            show_logo_bg: cs.report_header_show_logo_bg ?? null, logo_bg_color: cs.report_header_logo_bg_color ?? null,
            status_bar_color: cs.report_status_bar_color ?? null, logo_type: cs.report_header_logo_type ?? null, icon_url: cs.white_label_icon_url ?? null,
          }
        : null,
      language: cs.language ?? 'pt-br', currency: cs.currency ?? 'BRL', timezone: cs.timezone ?? 'America/Sao_Paulo',
    },
    schedule,
    history,
    equipment,
    equipment_field_config: fieldConfig,
    occurrences,
    charges,
  };
  if (configured.length > 0) {
    payload.partial = isPartial;
    payload.locked_sections = locked;
    payload.hidden_sections = hidden;
  }
  if (isPmoc) {
    payload.documents_released = released;
    payload.documents = documents;
    payload.execution_history = executionHistory;
  }
  payload.attachments_released = attachmentsReleased;
  payload.attachments = attachments;
  return payload;
}
