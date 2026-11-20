// Edge time-clock-portal (o ponto pelo link pessoal, sem login: pages/PontoPublico.tsx -> hooks/usePontoPublico.ts; T19 cap09), como
// a função da 1.59.154 (supabase/functions/time-clock-portal/index.ts) nas ações get_state e register_punch:
//  - o funcionário vem do slug (employees.ponto_slug com ponto ligado; 404 "link inválido ou desativado"); módulo "funcionarios";
//  - o dia é o do fuso da empresa (resolve_punch_day; a madrugada até overnight_until conta para o dia anterior);
//  - allowed_actions/next_action pela última batida do dia (_shared/ponto-kiosk.ts: depois da entrada, intervalo antes da saída
//    quando o dia prevê intervalo);
//  - register_punch confere a ação, a selfie e a localização exigidas, guarda a selfie no bucket time-photos (arquivo em
//    rec/mundo/storage/time-photos/<empresa>/<funcionário>/<dia>-<tipo>-<ms>.jpg: o storage em memória do falso não é exportado; o
//    arquivo anterior do mesmo dia e tipo sai, para não acumular a cada ensaio), grava time_records com a hora do SERVIDOR (source
//    link_publico) e refaz a time_sheets do dia (recompute_time_sheet: dia em aberto, fora do saldo).
import fs from 'node:fs';
import path from 'node:path';
import { STORAGE_DIR } from '../../../fakebase/http/storage.mjs';
import { agoraMs } from '../../lib/eco.mjs';

const TIPOS = ['clock_in', 'break_start', 'break_end', 'clock_out'];
const TZ = 'America/Sao_Paulo';
const dataTz = (ms, tz) => new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(ms));
const horaTz = (ms, tz) => new Intl.DateTimeFormat('en-GB', { timeZone: tz, hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(ms));
const ultimo = (tipos) => [...tipos].reverse().find((t) => TIPOS.includes(t)) || null;

export function permitidas(tipos, comIntervalo = true) {
  const depois = comIntervalo ? ['break_start', 'clock_out'] : ['clock_out', 'break_start'];
  switch (ultimo(tipos)) {
    case 'clock_in': case 'break_end': return depois;
    case 'break_start': return ['break_end'];
    default: return ['clock_in'];
  }
}

export default (body, ctx) => {
  const { store, db, FunctionError } = ctx;
  const acao = body?.action;
  const slug = typeof body?.slug === 'string' ? body.slug : null;
  const kioskSlug = typeof body?.kiosk_slug === 'string' ? body.kiosk_slug.trim() : null;
  // 1.60.18: a hora do ponto pode andar (o robô do celular manda `__avanco_min`; só o falso lê): almoço às 11:00, saída às 16:00
  const avanco = (Number(body?.__avanco_min) || 0) * 60000;

  // ---- tablet da empresa: a lista da equipe (get_kiosk), como supabase/functions/time-clock-portal/index.ts
  if (acao === 'get_kiosk') {
    const empresa = store.rows('companies').find((c) => c.ponto_kiosk_slug === kioskSlug);
    if (!empresa) throw new FunctionError('link inválido ou desativado', 404);
    const ativo = store.rows('company_modules').some((m) => m.company_id === empresa.id && m.module_code === 'funcionarios' && !m.removed_at);
    if (!ativo) throw new FunctionError('module_inactive', 403);
    const tz = empresa.timezone || TZ;
    const cfg = store.rows('time_settings').find((t) => t.company_id === empresa.id) || null;
    const dia = dataTz(agoraMs() + avanco, tz);
    const pinados = new Set(store.rows('employee_ponto_pins').map((p) => p.employee_id));
    const lista = store.rows('employees').filter((e) => e.company_id === empresa.id && e.ponto_enabled === true && e.is_active !== false)
      .sort((a, b) => String(a.name).localeCompare(String(b.name), 'pt-BR'));
    return {
      company: { name: empresa.name ?? 'Empresa', logo_url: empresa.logo_url ?? null, timezone: tz },
      settings: { kiosk_require_face: cfg?.kiosk_require_face === true },
      employees: lista.map((e) => {
        const tipos = store.rows('time_records').filter((r) => r.employee_id === e.id && r.date === dia && r.is_valid !== false)
          .sort((x, y) => String(x.recorded_at).localeCompare(String(y.recorded_at))).map((r) => r.type);
        const u = ultimo(tipos);
        const status = u === 'clock_in' || u === 'break_end' ? 'working' : u === 'break_start' ? 'on_break' : u === 'clock_out' ? 'finished' : 'not_started';
        return { id: e.id, name: e.name, position: e.position ?? null, photo_url: e.photo_url ?? null, status, has_pin: pinados.has(e.id), absence_label: null };
      }),
    };
  }

  // ---- identidade: link pessoal (slug) ou tablet (kiosk_slug + employee_id)
  let emp = null;
  if (slug) {
    emp = store.rows('employees').find((e) => e.ponto_slug === slug && e.ponto_enabled === true) || null;
    // 1.60.18 (3aa83d88c): funcionário arquivado não bate mais ponto pelo link pessoal
    if (emp && emp.is_active === false) throw new FunctionError('employee_inactive', 404);
  } else if (kioskSlug && body?.employee_id) {
    const empresaK = store.rows('companies').find((c) => c.ponto_kiosk_slug === kioskSlug);
    emp = empresaK ? store.rows('employees').find((e) => e.id === body.employee_id && e.company_id === empresaK.id && e.ponto_enabled === true && e.is_active !== false) || null : null;
  }
  if (!emp) throw new FunctionError('link inválido ou desativado', 404);
  const cid = emp.company_id;
  const ativo = store.rows('company_modules').some((m) => m.company_id === cid && m.module_code === 'funcionarios' && !m.removed_at);
  if (!ativo) throw new FunctionError('module_inactive', 403);
  const empresa = store.rows('companies').find((c) => c.id === cid) || {};
  const tz = empresa.timezone || TZ;
  const cfg = store.rows('time_settings').find((t) => t.company_id === cid) || null;
  const agora = agoraMs() + avanco;
  let dia = dataTz(agora, tz);
  const madrugada = String(cfg?.overnight_until || '05:00').slice(0, 5);
  if (horaTz(agora, tz) < madrugada) {
    const ontem = dataTz(agora - 86400000, tz);
    const aberto = store.rows('time_records').filter((r) => r.employee_id === emp.id && r.date === ontem && r.is_valid !== false)
      .sort((x, y) => String(x.recorded_at).localeCompare(String(y.recorded_at)));
    if (aberto.length && ultimo(aberto.map((r) => r.type)) !== 'clock_out') dia = ontem;
  }
  const settings = { require_selfie: cfg?.require_selfie ?? true, require_geolocation: cfg?.require_geolocation ?? true };
  const wd = new Date(`${dia}T12:00:00Z`).getUTCDay();
  const sched = store.rows('time_schedules').find((s) => s.employee_id === emp.id && Number(s.weekday) === wd);
  const intervalo = Number(sched?.break_minutes ?? cfg?.default_break_min ?? 60) > 0;
  const registros = store.rows('time_records').filter((r) => r.company_id === cid && r.employee_id === emp.id && r.date === dia && r.is_valid !== false)
    .sort((x, y) => String(x.recorded_at).localeCompare(String(y.recorded_at)));
  const tipos = registros.map((r) => r.type);
  const acoes = permitidas(tipos, intervalo);
  const pessoa = { id: emp.id, name: emp.name, position: emp.position ?? null, photo_url: emp.photo_url ?? null };
  // gate de PIN (verify_ponto_pin): quem tem PIN só entra com ele; sem o PIN a tela recebe só o cartão
  const pinRow = store.rows('employee_ponto_pins').find((p) => p.employee_id === emp.id && p.pin_hash) || null;
  const temPin = !!pinRow;
  if (temPin) {
    const dado = typeof body?.pin === 'string' ? body.pin : null;
    if (dado !== String(pinRow.pin_hash).replace(/^falso:/, '')) {
      if (dado) throw new FunctionError('pin_invalid', 401);
      return { pin_required: true, employee: pessoa, company: { name: empresa.name ?? 'Empresa', logo_url: empresa.logo_url ?? null, timezone: tz },
        settings: null, today: [], allowed_actions: [], next_action: null };
    }
  }

  if (acao === 'get_state') {
    return {
      absence_label: null, pin_required: false, has_pin: temPin, employee: pessoa,
      company: { name: empresa.name ?? 'Empresa', logo_url: empresa.logo_url ?? null, timezone: tz },
      settings, date: dia, today: registros.map((r) => ({ type: r.type, recorded_at: r.recorded_at, address: r.address ?? null })),
      allowed_actions: acoes, next_action: acoes[0] ?? null,
    };
  }
  if (acao === 'register_punch') {
    const tipo = body?.type;
    if (!tipo || !acoes.includes(tipo)) throw new FunctionError('ação inválida, recarregue a página', 409);
    const foto = typeof body?.photo_base64 === 'string' ? body.photo_base64 : null;
    if (settings.require_selfie && !foto) throw new FunctionError('selfie é obrigatória', 400);
    if (settings.require_geolocation && (body?.latitude == null || body?.longitude == null)) throw new FunctionError('localização é obrigatória', 400);
    let caminho = null;
    if (foto) {
      const bytes = Buffer.from(foto.replace(/^data:[^,]*,/, ''), 'base64');
      if (!bytes.length) throw new FunctionError('selfie inválida', 400);
      caminho = `${cid}/${emp.id}/${dia}-${tipo}-${agora}.jpg`;
      const pasta = path.join(STORAGE_DIR, 'time-photos', cid, emp.id);
      fs.mkdirSync(pasta, { recursive: true });
      for (const f of fs.readdirSync(pasta)) if (f.startsWith(`${dia}-${tipo}-`)) fs.rmSync(path.join(pasta, f));
      fs.writeFileSync(path.join(pasta, path.basename(caminho)), bytes);
    }
    const quando = new Date(agora).toISOString();
    db.insert('time_records', {
      company_id: cid, employee_id: emp.id, date: dia, type: tipo, recorded_at: quando, source: slug ? 'link_publico' : 'quiosque', created_by: null,
      latitude: body?.latitude ?? null, longitude: body?.longitude ?? null, address: typeof body?.address === 'string' ? body.address : null,
      photo_path: caminho, device_info: body?.device_info ?? null, is_valid: true, face_match: false, created_at: quando,
    }, { companyId: cid });
    // recompute_time_sheet do dia (só o que o link pessoal gera: entrada/intervalo/saída do dia de hoje)
    const todos = [...registros, { type: tipo, recorded_at: quando }];
    const ent = todos.find((r) => r.type === 'clock_in')?.recorded_at || null;
    const fechado = tipo === 'clock_out';
    const linha = { first_clock_in: ent, last_clock_out: fechado ? quando : null, status: fechado ? 'complete' : 'open', updated_at: quando };
    const sh = store.rows('time_sheets').find((t) => t.employee_id === emp.id && t.date === dia);
    if (sh) Object.assign(sh, linha);
    else {
      const [hi, mi] = String(sched?.expected_in || cfg?.default_in || '07:00').split(':').map(Number);
      const [ho, mo] = String(sched?.expected_out || cfg?.default_out || '16:00').split(':').map(Number);
      const esperado = Math.max(0, (ho * 60 + mo) - (hi * 60 + mi) - Number(sched?.break_minutes ?? cfg?.default_break_min ?? 60));
      db.insert('time_sheets', { company_id: cid, employee_id: emp.id, date: dia, total_worked_min: 0, total_break_min: 0, expected_min: esperado,
        balance_min: null, justification: null, justified_by: null, created_at: quando, ...linha }, { companyId: cid });
    }
    store.table('time_sheets').touch();
    const depois = permitidas([...tipos, tipo], intervalo);
    return { success: true, type: tipo, recorded_at: quando, date: dia, allowed_actions: depois, next_action: depois[0] ?? null };
  }
  throw new FunctionError('ação desconhecida', 400);
};
