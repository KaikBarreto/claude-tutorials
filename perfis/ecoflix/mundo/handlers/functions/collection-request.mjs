// Edge collection-request ("Solicitar coleta" do portal do parceiro): confere o token, a opção do parceiro, os módulos portal_cliente e
// coletas e as regras do portal (antecedência mínima e dias aceitos: lib/coletas/collectionSettings.ts); cria a ordem com o próximo número,
// "solicitada" com "Exigir aprovação da solicitação" ligado (senão "agendada"), origem portal, endereço do pedido ou do cadastro; avisa os
// usuários da empresa em user_notifications ("Nova solicitação de coleta"). Responde { ok: true, numero }.
import { agoraIso, parteDoPortal, temModulo } from '../../lib/coletas.mjs';
import { agoraMs } from '../../lib/eco.mjs';

const DIAS = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
export default (body, { store, db, FunctionError }) => {
  const p = parteDoPortal(store, body?.token);
  if (!body?.token) throw new FunctionError('Token é obrigatório', 400);
  if (!p) throw new FunctionError('Token inválido ou expirado', 404);
  if (!p.cfg.coletas || !p.cfg.solicitar_coleta) throw new FunctionError('A solicitação de coleta não está disponível neste portal.', 403);
  if (p.senha) throw new FunctionError('Faça login no portal', 401, { requiresLogin: true });
  if (!temModulo(store, p.companyId, 'portal_cliente')) throw new FunctionError('Portal indisponível', 403, { reason: 'portal_module_inactive' });
  if (!temModulo(store, p.companyId, 'coletas')) throw new FunctionError('Coletas não está disponível para esta empresa.', 403);
  const cfg = store.rows('collection_settings').find((s) => s.company_id === p.companyId) || {};
  const aprovacao = cfg.portal_require_approval ?? true;
  const antecedencia = Number(cfg.portal_min_lead_hours ?? 0);
  const dias = Array.isArray(cfg.portal_accepted_weekdays) ? cfg.portal_accepted_weekdays : [1, 2, 3, 4, 5, 6];
  const data = typeof body.scheduled_date === 'string' && body.scheduled_date.trim() ? body.scheduled_date.trim() : null;
  if (data) {
    const dow = new Date(`${data}T12:00:00Z`).getUTCDay();
    if (!dias.includes(dow)) throw new FunctionError(`A empresa não faz coleta ${dow === 0 || dow === 6 ? 'aos' : 'às'} ${DIAS[dow]}s.`, 422);
    const inicio = new Date(`${data}T03:00:00Z`).getTime();
    if (antecedencia > 0 && inicio - agoraMs() < antecedencia * 3600000) throw new FunctionError(`Peça com pelo menos ${antecedencia} horas de antecedência.`, 422);
  }
  const ent = p.row;
  const end = body.endereco || {};
  const pick = (a, b) => (typeof a === 'string' && a.trim() ? a.trim() : typeof b === 'string' && b.trim() ? b.trim() : null);
  const numero = store.rows('collection_orders').filter((o) => o.company_id === p.companyId).reduce((m, o) => Math.max(m, Number(o.numero) || 0), 0) + 1;
  const agora = agoraIso();
  db.insert('collection_orders', {
    company_id: p.companyId, numero, partner_type: p.tipo, partner_id: ent.id, partner_nome: ent.name ?? null,
    logradouro: pick(end.logradouro, ent.logradouro), numero_end: pick(end.numero_end, ent.numero), bairro: pick(end.bairro, ent.bairro),
    cidade: pick(end.cidade, ent.cidade), uf: pick(end.uf, ent.uf), cep: pick(end.cep, ent.cep), driver_id: null, vehicle_id: null,
    scheduled_date: data, scheduled_window: typeof body.scheduled_window === 'string' && body.scheduled_window.trim() ? body.scheduled_window.trim() : null,
    status: aprovacao ? 'solicitada' : 'agendada', material_estimado: typeof body.material === 'string' && body.material.trim() ? body.material.trim() : null,
    observacoes: typeof body.observacoes === 'string' && body.observacoes.trim() ? body.observacoes.trim() : null, origem: 'portal',
    created_at: agora, updated_at: agora,
  }, { companyId: p.companyId });
  if (cfg.notify_on_request ?? true) {
    const users = store.rows('profiles').filter((u) => u.company_id === p.companyId && u.id);
    const expira = new Date(agoraMs() + 7 * 86400000).toISOString();
    for (const u of users) {
      db.insert('user_notifications', { user_id: u.id, company_id: p.companyId, type: 'collection_request', title: 'Nova solicitação de coleta',
        message: `${ent.name ?? 'Parceiro'} solicitou uma coleta (#${numero}).`, action_url: '/coletas/ordens', icon: 'package', expires_at: expira,
        created_at: agora, read_at: null });
    }
  }
  return { ok: true, numero };
};
