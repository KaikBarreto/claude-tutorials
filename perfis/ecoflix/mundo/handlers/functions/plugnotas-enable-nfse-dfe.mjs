// Liga/desliga as NFS-e Recebidas do CNPJ (T17 cap08; supabase/functions/plugnotas-enable-nfse-dfe): espelha a flag
// `nfse_dfe_ativo` e, na 1ª ativação, carimba `nfse_dfe_count_start_at` (início da contagem na cota).
import { nowIso } from '../../../fakebase/core/util.mjs';

export default (body, { db, companyId, FunctionError }) => {
  const cid = body?.companyId || companyId;
  const cfg = (body?.fiscalConfigId && db.first('company_fiscal_config', { id: body.fiscalConfigId, company_id: cid }))
    || db.first('company_fiscal_config', (c) => c.company_id === cid && c.is_default) || db.first('company_fiscal_config', { company_id: cid });
  if (!cfg) throw new FunctionError('Configuração fiscal não encontrada', 404, { success: false });
  const ativo = body?.ativo !== false;
  const ja = !!cfg.nfse_dfe_ativo && ativo;
  const upd = { nfse_dfe_ativo: ativo, updated_at: nowIso() };
  if (ativo && !cfg.nfse_dfe_count_start_at) upd.nfse_dfe_count_start_at = nowIso();
  if (!cfg.nfse_dfe_fonte) upd.nfse_dfe_fonte = 'plugnotas';
  db.update('company_fiscal_config', { id: cfg.id }, upd);
  return { success: true, ativo, cnpj: cfg.cnpj, alreadyActive: ja, countStartAt: upd.nfse_dfe_count_start_at || cfg.nfse_dfe_count_start_at || null };
};
