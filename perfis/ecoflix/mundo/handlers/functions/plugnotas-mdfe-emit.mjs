// Emissão normal do MDF-e (T17 cap04; supabase/functions/plugnotas-mdfe-emit): o PlugNotas aceita o documento e o manifesto fica
// "aguardando_sefaz" com o plugnotas_id; a autorização chega pela consulta (plugnotas-mdfe-status, a cada 5 s na lista).
// Nada sai para fora: o "PlugNotas" e a SEFAZ são simulados aqui.
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (body, { db, FunctionError }) => {
  const m = db.first('mdfe_manifests', { id: body?.mdfeId });
  if (!m) throw new FunctionError('MDF-e não encontrado', 404, { success: false });
  if (!['pendente', 'rejeitado'].includes(m.status)) return { success: false, error: 'Este MDF-e já foi enviado para a SEFAZ.' };
  const plugnotasId = `pn-mdfe-${String(m.mdfe_number).padStart(6, '0')}`;
  db.update('mdfe_manifests', { id: m.id }, { status: 'aguardando_sefaz', plugnotas_id: plugnotasId, environment: 'producao', error_message: null, updated_at: nowIso() });
  db.insert('nfe_events', { invoice_id: null, company_id: m.company_id, event_type: 'mdfe_emissao', status: 'aguardando_sefaz',
    message: `MDF-e #${m.mdfe_number} enviado para SEFAZ`, plugnotas_response: { id: plugnotasId, message: 'Documento em processamento' }, created_at: nowIso() });
  return { success: true, plugnotasId, data: { id: plugnotasId, message: 'Documento em processamento' } };
};
