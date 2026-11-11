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
  if (!slug) throw new FunctionError('link inválido ou desativado', 404);
  const emp = store.rows('employees').find((e) => e.ponto_slug === slug && e.ponto_enabled === true);
  if (!emp) throw new FunctionError('link inválido ou desativado', 404);
  const cid = emp.company_id;
  const ativo = store.rows('company_modules').some((m) => m.company_id === cid && m.module_code === 'funcionarios' && !m.removed_at);
  if (!ativo) throw new FunctionError('module_inactive', 403);
  const empresa = store.rows('companies').find((c) => c.id === cid) || {};
  const tz = empresa.timezone || TZ;
  const cfg = store.rows('time_settings').find((t) => t.company_id === cid) || null;
  const agora = agoraMs();
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

  if (acao === 'get_state') {
    return {
      absence_label: null, pin_required: false, has_pin: false, employee: pessoa,
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
      company_id: cid, employee_id: emp.id, date: dia, type: tipo, recorded_at: quando, source: 'link_publico', created_by: null,
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
