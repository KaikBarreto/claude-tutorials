// Edge function time-clock-portal falsa (T15, cap. 9: o ponto da funcionária pelo celular, SEM login). Espelha
// supabase/functions/time-clock-portal/index.ts (1.38.21), só as ações do link pessoal: `get_state` e `register_punch`
// (quiosque, PIN e biometria ficam de fora: a aula não os demonstra).
//   get_state      → { employee: { name, position, photo_url }, company, settings, today: [{ type, recorded_at }], allowed_actions, next_action }
//   register_punch → { success, type, recorded_at, date, allowed_actions, next_action }  (grava `time_records` e refaz `time_sheets`)
// Identidade: { slug } = `employees.ponto_slug` com `ponto_enabled`; slug desconhecido = 404.
// Diferenças deliberadas: (1) o relógio do servidor falso é congelado no FAKE_NOW; a batida carimba FAKE_NOW + PUNCH_OFFSET_MIN (2 min), para
// o "Horário" do celular (relógio do navegador, 09:02 no capítulo) e o "Entrada" de "Hoje" saírem iguais; (2) selfie obrigatória (`require_selfie`)
// só se a empresa ligar e o app mandar a foto: a aula desliga a chave no capítulo 8.
// Também exporta as peças que `register_time_punch` e `recompute_time_sheet` (RPCs) usam: `acoesPermitidas`, `diaDaBatida`, `recomputar`.
import { FunctionError } from '../../http/functions.mjs';
import { now, dateBR } from '../../core/util.mjs';

export const PUNCH_OFFSET_MIN = 2;

/** Ações permitidas depois do último evento do dia (espelha `allowed_punch_actions` / `allowedActionsFrom`). */
export function acoesPermitidas(tipos) {
  const ultimo = tipos[tipos.length - 1];
  if (!ultimo) return ['clock_in'];
  if (ultimo === 'clock_in') return ['break_start', 'clock_out'];
  if (ultimo === 'break_start') return ['break_end'];
  if (ultimo === 'break_end') return ['clock_out'];
  return ['clock_in'];
}

export const diaDaBatida = (iso) => dateBR(0, new Date(iso));

/** `recompute_time_sheet` (20260930150000_ponto_multiplas_jornadas.sql:582-715): refaz o espelho do dia. */
export function recomputar(db, companyId, employeeId, date) {
  const regs = db.find('time_records', (r) => r.employee_id === employeeId && r.date === date && r.is_valid === true)
    .sort((x, y) => String(x.recorded_at).localeCompare(String(y.recorded_at)) || String(x.created_at).localeCompare(String(y.created_at)));
  const antigo = db.first('time_sheets', (s) => s.employee_id === employeeId && s.date === date);
  if (!regs.length) {
    if (antigo) db.remove('time_sheets', (s) => s === antigo);
    return;
  }
  const agora = now().getTime();
  let trab = 0; let pausa = 0; let iniTrab = null; let iniPausa = null; let primeira = null; let ultimaSaida = null;
  for (const r of regs) {
    const t = new Date(r.recorded_at).getTime();
    if (r.type === 'clock_in') { iniTrab = t; if (primeira === null) primeira = r.recorded_at; }
    else if (r.type === 'break_start' && iniTrab !== null) { trab += (t - iniTrab) / 60000; iniTrab = null; iniPausa = t; }
    else if (r.type === 'break_end') { if (iniPausa !== null) pausa += (t - iniPausa) / 60000; iniPausa = null; iniTrab = t; }
    else if (r.type === 'clock_out' && iniTrab !== null) { trab += (t - iniTrab) / 60000; iniTrab = null; }
    if (r.type === 'clock_out') ultimaSaida = r.recorded_at;
  }
  if (iniTrab !== null) trab += Math.max(0, (agora - iniTrab) / 60000);
  if (iniPausa !== null) pausa += Math.max(0, (agora - iniPausa) / 60000);
  const fechado = regs[regs.length - 1].type === 'clock_out';
  const trabMin = Math.round(trab);
  const esperado = antigo?.expected_min ?? 480;
  const linha = {
    company_id: companyId, employee_id: employeeId, date, first_clock_in: primeira, last_clock_out: ultimaSaida,
    total_worked_min: trabMin, total_break_min: Math.round(pausa), expected_min: esperado,
    balance_min: fechado ? trabMin - esperado : null, status: fechado ? 'complete' : 'open',
  };
  if (antigo) db.update('time_sheets', (s) => s === antigo, linha);
  else db.insert('time_sheets', linha);
}

/** Grava a batida e refaz o espelho; devolve { date, allowed_actions, recorded_at }. */
export function registrarBatida(db, emp, tipo, extra = {}) {
  const hoje = dateBR(0);
  const regs = db.find('time_records', (r) => r.employee_id === emp.id && r.date === hoje && r.is_valid === true)
    .sort((x, y) => String(x.recorded_at).localeCompare(String(y.recorded_at)));
  const tipos = regs.map((r) => r.type);
  if (!extra.force && !acoesPermitidas(tipos).includes(tipo)) return { erro: 'punch_out_of_order' };
  const recorded = extra.recorded_at || new Date(now().getTime() + PUNCH_OFFSET_MIN * 60000).toISOString();
  const date = extra.date || diaDaBatida(recorded);
  db.insert('time_records', {
    company_id: emp.company_id, employee_id: emp.id, type: tipo, recorded_at: recorded, date, is_valid: true,
    latitude: extra.latitude ?? null, longitude: extra.longitude ?? null, address: extra.address ?? null, photo_url: null,
    device_info: extra.device_info ?? null, source: extra.source || 'link_publico', notes: extra.notes ?? null,
    face_match: false, user_id: extra.user_id ?? null,
  });
  recomputar(db, emp.company_id, emp.id, date);
  const depois = db.find('time_records', (r) => r.employee_id === emp.id && r.date === date && r.is_valid === true)
    .sort((x, y) => String(x.recorded_at).localeCompare(String(y.recorded_at))).map((r) => r.type);
  return { date, recorded_at: recorded, allowed_actions: acoesPermitidas(depois) };
}

function marca(db, companyId) {
  const cs = db.first('company_settings', { company_id: companyId }) || {};
  const emp = db.first('companies', { id: companyId }) || {};
  return {
    name: cs.name ?? emp.name ?? null, logo_url: cs.logo_url ?? null, white_label_enabled: cs.white_label_enabled ?? false,
    white_label_primary_color: cs.white_label_primary_color ?? null, white_label_logo_url: cs.white_label_logo_url ?? null,
    white_label_icon_url: cs.white_label_icon_url ?? null, report_header_bg_color: cs.report_header_bg_color ?? null,
    report_header_text_color: cs.report_header_text_color ?? null, report_header_logo_size: cs.report_header_logo_size ?? null,
    report_header_logo_type: cs.report_header_logo_type ?? null, report_header_show_logo_bg: cs.report_header_show_logo_bg ?? null,
    report_header_logo_bg_color: cs.report_header_logo_bg_color ?? null, report_status_bar_color: cs.report_status_bar_color ?? null,
    language: cs.language ?? 'pt-br', currency: cs.currency ?? 'BRL', timezone: cs.timezone ?? 'America/Sao_Paulo',
  };
}

export default async function timeClockPortal(body, { db }) {
  const { action } = body || {};
  const slug = body?.slug;
  const emp = slug ? db.first('employees', (e) => e.ponto_slug === slug && e.ponto_enabled === true && e.is_active !== false) : null;
  if (!emp) throw new FunctionError('Link inválido ou desativado.', 404);

  const st = db.first('time_settings', { company_id: emp.company_id });
  const settings = { require_selfie: st?.require_selfie ?? true, require_geolocation: st?.require_geolocation ?? true };
  const hoje = dateBR(0);
  const regs = db.find('time_records', (r) => r.employee_id === emp.id && r.date === hoje && r.is_valid === true)
    .sort((x, y) => String(x.recorded_at).localeCompare(String(y.recorded_at)));
  const acoes = acoesPermitidas(regs.map((r) => r.type));

  if (action === 'get_state') {
    return {
      employee: { name: emp.name, position: emp.position ?? null, photo_url: null },
      company: marca(db, emp.company_id), settings,
      today: regs.map((r) => ({ type: r.type, recorded_at: r.recorded_at })),
      allowed_actions: acoes, next_action: acoes[0] ?? null,
    };
  }

  if (action === 'register_punch') {
    const tipo = body.type;
    if (!tipo || !acoes.includes(tipo)) throw new FunctionError('Esta ação não está disponível agora. Recarregue a página e tente novamente.', 409);
    if (settings.require_selfie && !body.photo_base64) throw new FunctionError('A selfie é obrigatória.', 400);
    const lat = typeof body.latitude === 'number' ? body.latitude : null;
    const lng = typeof body.longitude === 'number' ? body.longitude : null;
    if (settings.require_geolocation && (lat === null || lng === null)) throw new FunctionError('A localização é obrigatória.', 400);
    const r = registrarBatida(db, emp, tipo, { latitude: lat, longitude: lng, address: typeof body.address === 'string' ? body.address : null, device_info: body.device_info ?? null });
    if (r.erro) throw new FunctionError('Esta ação não está disponível agora. Recarregue a página e tente novamente.', 409);
    return { success: true, type: tipo, recorded_at: r.recorded_at, date: r.date, allowed_actions: r.allowed_actions, next_action: r.allowed_actions[0] ?? null };
  }

  throw new FunctionError('Ação desconhecida.', 400);
}
