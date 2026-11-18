// cato_routines_manage(p_action, p_payload) — app 1.60.10, migration 20261115142000_cato_readonly_routines.sql
// (hooks/useCatoRoutines.ts). O botão do Cato consulta "status" a cada minuto em toda tela logada (T00, T21, T25 e qualquer aula com o
// botão visível): sem resposta válida ({ routines: [], inbox: [] }) o painel mostra "As rotinas estão indisponíveis agora".
// Mundo base: nenhuma rotina, caixa de entrada vazia, o Rafael pode ver o financeiro. "save", "pause", "resume" e "delete" guardam a
// rotina na memória do processo (reiniciar o Supabase falso limpa; o /__dev/reset não). "preview" devolve o resumo vazio: a aula
// que mostra "Ver sinais agora" (T21) troca este handler pelo dela, com os sinais do mundo.
const ROTINAS = new Map(); // empresa:usuário -> rotinas
export default (a, { companyId, userId }) => {
  const chave = `${companyId}:${userId}`;
  const lista = ROTINAS.get(chave) || [];
  const p = a.p_payload || {};
  const acao = a.p_action || 'status';
  let savedId = null;
  if (acao === 'save') {
    const r = { id: p.id || `rotina-${lista.length + 1}`, focus: p.focus || 'stock', cadence: p.cadence || 'weekly', local_time: p.localTime || p.local_time || '08:00', timezone: p.timezone || 'America/Sao_Paulo', weekday: p.weekday ?? 1, status: 'active', next_run_at: null, last_run_at: null, pause_reason: null };
    const i = lista.findIndex((x) => x.id === r.id);
    if (i >= 0) lista[i] = r; else lista.push(r);
    savedId = r.id;
  } else if (acao === 'pause' || acao === 'resume') {
    const r = lista.find((x) => x.id === p.id); if (r) { r.status = acao === 'pause' ? 'paused' : 'active'; r.pause_reason = acao === 'pause' ? 'user' : null; }
  } else if (acao === 'delete') {
    const i = lista.findIndex((x) => x.id === p.id); if (i >= 0) lista.splice(i, 1);
  }
  ROTINAS.set(chave, lista);
  const out = { routines: lista, inbox: [], unreadCount: 0, canFinancial: true };
  if (acao === 'preview') out.preview = null;
  if (savedId) out.savedId = savedId;
  return out;
};
