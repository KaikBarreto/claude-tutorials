// Motor fiscal próprio do MDF-e (T17, app 1.60.10; supabase/functions/mdfe-contingency): emitir, consultar, encerrar, baixar e
// cancelar passam todos por aqui, com `action` = prepare | transmit | status | enclose | download | cancel (useMdfe.tsx,
// NovoMdfeModal.tsx e MdfeTab.tsx). SEFAZ simulada: o envio normal fica "aguardando_sefaz" e a 1ª consulta autoriza; o pedido de
// encerramento fica "encerramento_pendente" e a consulta seguinte confirma. A lógica de cada passo é a dos handlers da 1.59
// (plugnotas-mdfe-*), que continuam valendo para a Exportação Contábil (plugnotas-mdfe-download).
import { nowIso } from '../../../fakebase/core/util.mjs';
import emitir from './plugnotas-mdfe-emit.mjs';
import consultar from './plugnotas-mdfe-status.mjs';
import encerrar from './plugnotas-mdfe-enclose.mjs';
import baixar from './plugnotas-mdfe-download.mjs';

export default (body, ctx) => {
  const { db, FunctionError } = ctx;
  const acao = String(body?.action || '');
  const m = db.first('mdfe_manifests', { id: body?.mdfeId });
  if (!m) throw new FunctionError('MDF-e não encontrado', 404, { success: false });
  if (acao === 'prepare' || acao === 'transmit') {
    if (m.emission_mode === 'contingency' && acao === 'prepare') {
      const prazo = new Date(Date.parse(nowIso()) + 168 * 3600e3).toISOString();
      db.update('mdfe_manifests', { id: m.id }, { status: 'contingencia', contingency_reason: body?.reason || m.contingency_reason || null,
        contingency_deadline: prazo, error_message: null, updated_at: nowIso() });
      return { success: true, status: 'contingencia', message: 'Documento sendo preparado para impressão' };
    }
    if (m.status === 'contingencia' || m.status === 'contingencia_rejeitada') db.update('mdfe_manifests', { id: m.id }, { status: 'pendente' });
    const r = emitir(body, ctx);
    return r.success ? { ...r, status: 'aguardando_sefaz' } : r;
  }
  if (acao === 'status') return consultar(body, ctx);
  if (acao === 'enclose') return encerrar(body, ctx);
  if (acao === 'download') return baixar(body, ctx);
  if (acao === 'cancel') {
    if (!['autorizado', 'cancelamento_rejeitado'].includes(m.status)) return { success: false, error: 'Apenas MDF-e autorizados podem ser cancelados' };
    if (String(body?.motivo || '').trim().length < 15) return { success: false, error: 'Informe o motivo do cancelamento (mínimo 15 caracteres)' };
    db.update('mdfe_manifests', { id: m.id }, { status: 'cancelamento_pendente', error_message: null, updated_at: nowIso() });
    return { success: true, status: 'cancelamento_pendente', confirmed: false, message: 'Cancelamento enviado. A confirmação da SEFAZ aparece em instantes.' };
  }
  return { success: false, error: 'Ação inválida' };
};
