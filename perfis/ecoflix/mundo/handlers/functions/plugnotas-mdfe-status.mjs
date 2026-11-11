// Consulta do MDF-e na SEFAZ simulada (T17 cap04 e cap05; supabase/functions/plugnotas-mdfe-status): na 1ª consulta, o manifesto
// "aguardando_sefaz" é autorizado (chave de 44 dígitos, protocolo, authorized_at) e o pedido de encerramento
// ("encerramento_pendente") é confirmado (enclosed_at); a resposta diz statusChanged para a lista mostrar o aviso.
import { nowIso } from '../../../fakebase/core/util.mjs';

function chaveMdfe(m, cnpj) {
  const d = new Date(Date.parse(nowIso()) - 3 * 3600e3).toISOString();
  const base = `35${d.slice(2, 4)}${d.slice(5, 7)}${cnpj}58${String(m.serie || 1).padStart(3, '0')}${String(m.mdfe_number).padStart(9, '0')}1${String(40000000 + Number(m.mdfe_number) * 7919).slice(-8)}`;
  let s = 0;
  let w = 2;
  for (let i = base.length - 1; i >= 0; i--) { s += Number(base[i]) * w; w = w === 9 ? 2 : w + 1; }
  const r = s % 11;
  return base + (r < 2 ? 0 : 11 - r);
}

export default (body, { db, FunctionError }) => {
  const m = db.first('mdfe_manifests', { id: body?.mdfeId });
  if (!m) throw new FunctionError('MDF-e não encontrado', 404, { success: false });
  const antes = m.status;
  const agora = nowIso();
  let novo = antes;
  const upd = { updated_at: agora };
  if (antes === 'aguardando_sefaz') {
    const cfg = db.first('company_fiscal_config', (c) => c.company_id === m.company_id && c.is_default) || db.first('company_fiscal_config', { company_id: m.company_id });
    novo = 'autorizado';
    Object.assign(upd, { status: novo, mdfe_key: chaveMdfe(m, String(cfg?.cnpj || '').replace(/\D/g, '')), authorized_at: agora,
      mdfe_protocol: `9352600${String(m.mdfe_number).padStart(8, '0')}`, error_message: null });
  } else if (antes === 'encerramento_pendente') {
    novo = 'encerrado';
    Object.assign(upd, { status: novo, enclosed_at: agora, error_message: null });
  } else if (antes === 'cancelamento_pendente') {
    novo = 'cancelado';
    Object.assign(upd, { status: novo });
  }
  db.update('mdfe_manifests', { id: m.id }, upd);
  if (novo !== antes) {
    db.insert('nfe_events', { invoice_id: null, company_id: m.company_id, event_type: novo === 'autorizado' ? 'mdfe_autorizacao' : novo === 'encerrado' ? 'mdfe_encerramento' : 'mdfe_cancelamento',
      status: novo, message: novo === 'autorizado' ? `MDF-e #${m.mdfe_number} autorizado` : novo === 'encerrado' ? `MDF-e #${m.mdfe_number}: encerramento confirmado pela SEFAZ` : `MDF-e #${m.mdfe_number} cancelado`,
      plugnotas_response: { situacao: novo }, created_at: agora });
  }
  return { success: true, status: novo, statusChanged: novo !== antes };
};
