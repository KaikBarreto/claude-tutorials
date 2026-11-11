// Edge sigor-mtr-cancel (T18 cap06; supabase/functions/sigor-mtr-cancel), SIGOR simulado: só o MTR "emitido" pode ser cancelado
// (irreversível); o status vira "cancelado" e continua contando na cota do mês.
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (body, { db, FunctionError }) => {
  const m = db.first('mtr_manifests', { id: body?.manifestId });
  if (!m) throw new FunctionError('Manifesto não encontrado.', 404, { success: false, error: 'Manifesto não encontrado.' });
  if (m.status === 'cancelado') return { success: true, alreadyCancelled: true };
  if (m.status !== 'emitido' || !m.manifesto_codigo) return { success: false, error: 'Só é possível cancelar um manifesto já emitido.' };
  db.update('mtr_manifests', { id: m.id }, { status: 'cancelado', error_message: null, updated_at: nowIso(),
    raw_response: { mensagem: 'Manifesto cancelado (simulado).' } });
  return { success: true, status: 'cancelado' };
};
