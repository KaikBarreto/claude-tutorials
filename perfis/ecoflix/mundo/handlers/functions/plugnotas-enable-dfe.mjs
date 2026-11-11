// Edge plugnotas-enable-dfe (Notas Recebidas, "Ativar Notas Recebidas" > "Ativar mesmo assim"): liga/desliga a consulta de notas
// recebidas do emitente (dfe_ativo, dfe_fonte "plugnotas") e marca o início da contagem na cota (dfe_count_start_at) na 1ª ativação.
import { configFiscal, agoraIso } from '../../lib/nfe.mjs';

export default (body, { store, db, companyId, FunctionError }) => {
  const cfg = configFiscal(store, body?.companyId || companyId, body?.fiscalConfigId);
  if (!cfg) throw new FunctionError('Configuração fiscal não encontrada', 404, { success: false, error: 'Configuração fiscal não encontrada' });
  const ativo = body?.ativo !== false;
  if (ativo && !cfg.plugnotas_certificate_uploaded) return { success: false, error: 'Envie o certificado digital antes de ativar' };
  db.update('company_fiscal_config', { id: cfg.id }, {
    dfe_ativo: ativo, dfe_fonte: cfg.dfe_fonte || 'plugnotas', ...(ativo && !cfg.dfe_count_start_at ? { dfe_count_start_at: agoraIso() } : {}),
  });
  return { success: true, ativo };
};
