// Link público da OS (T7): o payload de `get_public_os` / `get_public_os_by_code`, no formato das migrations
//   20260925120000_check_in_out_by_autoria_real.sql:260-619 (chaves) e 20261019060000_...sql:315-393 (technician_location).
// Tudo o que a visão do cliente (?modo=cliente), o relatório sem login e o mapa público leem vem daqui. OS de tarefa ou
// inexistente devolve null, como o banco ("o front trata como não encontrada").
import { db } from '../core/db.mjs';

const nul = (v) => (v === undefined ? null : v);
const pick = (obj, keys) => Object.fromEntries(keys.map((k) => [k, nul(obj?.[k])]));

// allowlist de colunas de service_orders que alguma superfície pública lê (50 colunas)
const OS_PUBLICAS = [
  'id', 'order_number', 'customer_id', 'equipment_id', 'technician_id', 'os_type', 'status', 'scheduled_date', 'scheduled_time',
  'description', 'diagnosis', 'solution', 'check_in_time', 'check_in_location', 'check_out_time', 'check_out_location',
  'client_signature', 'notes', 'created_at', 'updated_at', 'form_template_id', 'service_type_id', 'require_tech_signature',
  'require_client_signature', 'tech_signature', 'duration_minutes', 'contract_id', 'entry_type', 'snapshot_data', 'company_id',
  'started_at', 'paused_at', 'resumed_at', 'completed_at', 'pmoc_conformity_status', 'pmoc_conformity_notes', 'service_address',
  'service_address_number', 'service_neighborhood', 'service_city', 'service_state', 'service_zip_code', 'service_latitude',
  'service_longitude', 'public_short_code', 'partial_finish', 'tech_signature_at', 'client_signature_at', 'tech_signed_location',
  'client_signed_location',
];

const CONFIG_EMPRESA = [
  'id', 'company_id', 'name', 'document', 'phone', 'email', 'address', 'city', 'state', 'zip_code', 'logo_url',
  'white_label_enabled', 'white_label_logo_url', 'white_label_icon_url', 'white_label_primary_color', 'report_header_bg_color',
  'report_header_text_color', 'report_header_logo_size', 'report_header_show_logo_bg', 'report_header_logo_bg_color',
  'report_status_bar_color', 'report_header_logo_type', 'language', 'currency', 'timezone',
];

/** Última posição do técnico na OS: { lat, lng, event_type, created_at } ou null. */
export function ultimaPosicaoTecnico(osId) {
  const l = db.find('technician_locations', { service_order_id: osId })
    .sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)))[0];
  return l ? { lat: l.lat, lng: l.lng, event_type: l.event_type, created_at: l.created_at } : null;
}

export function osPublicaExiste(osId) {
  const os = db.first('service_orders', { id: osId });
  return !!os && os.entry_type !== 'tarefa';
}

const perfil = (userId) => {
  const p = userId ? db.first('profiles', { user_id: userId }) : null;
  return p ? { full_name: nul(p.full_name), avatar_url: nul(p.avatar_url) } : null;
};

export function montarOsPublica(osId) {
  const os = db.first('service_orders', { id: osId });
  if (!os || os.entry_type === 'tarefa') return null;

  const tecnicoId = os.technician_id
    || db.find('service_order_assignees', { service_order_id: osId }).sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)))[0]?.user_id
    || null;
  const cliente = db.first('customers', { id: os.customer_id });
  const equip = db.first('equipment', { id: os.equipment_id });
  const modelo = db.first('form_templates', { id: os.form_template_id });
  const servico = db.first('service_types', { id: os.service_type_id });
  const nota = db.first('service_ratings', { service_order_id: osId });
  const nps = db.first('nps_settings', { company_id: os.company_id });
  const empresa = db.first('company_settings', { company_id: os.company_id });

  const respostas = db.find('form_responses', { service_order_id: osId }).map((fr) => {
    const q = db.first('form_questions', { id: fr.question_id });
    const t = q ? db.first('form_templates', { id: q.template_id }) : null;
    return {
      id: fr.id, question_id: fr.question_id, response_value: nul(fr.response_value), response_photo_url: nul(fr.response_photo_url),
      response_video_url: nul(fr.response_video_url), equipment_id: nul(fr.equipment_id), question: nul(q),
      template_id: nul(q?.template_id), template_name: nul(t?.name),
    };
  });

  const itens = db.find('service_order_equipment', { service_order_id: osId }).map((soe) => {
    const e2 = db.first('equipment', { id: soe.equipment_id });
    const cat = e2 ? db.first('equipment_categories', { id: e2.category_id }) : null;
    const ft = db.first('form_templates', { id: soe.form_template_id });
    return {
      equipment_id: soe.equipment_id, form_template_id: nul(soe.form_template_id), environment_name: null,
      equipment: e2 ? { id: e2.id, name: e2.name, brand: nul(e2.brand), model: nul(e2.model), location: nul(e2.location), photo_url: nul(e2.photo_url),
        category: cat ? { id: cat.id, name: cat.name, color: nul(cat.color) } : null } : null,
      form_template: ft ? { id: ft.id, name: ft.name } : null,
    };
  });

  const criterios = db.find('nps_criteria', (c) => c.company_id === os.company_id && c.active)
    .sort((a, b) => (a.position - b.position) || String(a.created_at).localeCompare(String(b.created_at)))
    .map((c) => ({ id: c.id, label: c.label }));

  const res = {
    technician_location: ultimaPosicaoTecnico(osId),
    service_order: pick(os, OS_PUBLICAS),
    customer: cliente ? pick(cliente, ['id', 'name', 'phone', 'address', 'city', 'state', 'document', 'photo_url']) : null,
    customer_geo: cliente ? { id: cliente.id, lat: nul(cliente.lat), lng: nul(cliente.lng), address: nul(cliente.address), city: nul(cliente.city), state: nul(cliente.state), zip_code: nul(cliente.zip_code) } : null,
    equipment: equip ? pick(equip, ['id', 'name', 'brand', 'model', 'serial_number', 'location', 'capacity']) : null,
    form_template: modelo ? { id: modelo.id, name: modelo.name } : null,
    service_type: servico ? { id: servico.id, name: servico.name, color: nul(servico.color) } : null,
    photos: db.find('os_photos', { service_order_id: osId }).sort((a, b) => String(a.created_at).localeCompare(String(b.created_at))),
    form_responses: respostas,
    equipment_items: itens,
    technician: perfil(tecnicoId),
    check_in_technician: perfil(os.check_in_by),
    check_out_technician: perfil(os.check_out_by),
    rating: nota
      ? { is_concluded: os.status === 'concluida', already_rated: !!nota.rated_at, rated_at: nul(nota.rated_at), nps_score: nul(nota.nps_score),
          quality_rating: nul(nota.quality_rating), punctuality_rating: nul(nota.punctuality_rating), professionalism_rating: nul(nota.professionalism_rating),
          comment: nul(nota.comment), rated_by_name: nul(nota.rated_by_name) }
      : { is_concluded: os.status === 'concluida', already_rated: false, rated_at: null, nps_score: null, quality_rating: null,
          punctuality_rating: null, professionalism_rating: null, comment: null, rated_by_name: null },
    survey_enabled: !!nota,
    nps_config: {
      question: nps?.question || 'De 0 a 10, o quão satisfeito(a) você ficou com o nosso serviço?',
      require_stars: nps?.require_stars ?? false, generate_on_finish: nps?.generate_on_finish ?? true,
      google_review_url: nul(nps?.google_review_url), google_review_min_score: nul(nps?.google_review_min_score),
    },
    nps_criteria: criterios,
    company_settings: empresa
      ? { ...pick(empresa, CONFIG_EMPRESA), language: empresa.language || 'pt-br', currency: empresa.currency || 'BRL', timezone: empresa.timezone || 'America/Sao_Paulo' }
      : null,
    contract: null,
  };
  return res;
}
