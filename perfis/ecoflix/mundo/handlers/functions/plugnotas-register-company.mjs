// Edge plugnotas-register-company ("Salvar configuração" da Configuração Fiscal): cadastra o emitente no provedor. Aqui só confere
// certificado, razão social e CNPJ e marca plugnotas_company_registered. Responde { success: true } sem message (o app mostra
// "Empresa cadastrada no sistema de NF-e!").
import { configFiscal, agoraIso } from '../../lib/nfe.mjs';

export default (body, { store, db, companyId, FunctionError }) => {
  const cfg = configFiscal(store, body?.companyId || companyId, body?.fiscalConfigId);
  if (!cfg) throw new FunctionError('Configuração fiscal não encontrada', 404, { success: false });
  if (!cfg.plugnotas_certificate_uploaded) return { success: false, error: 'Configure primeiro o certificado digital' };
  if (!cfg.razao_social || !cfg.cnpj) return { success: false, error: 'Preencha a razão social e o CNPJ da empresa' };
  db.update('company_fiscal_config', { id: cfg.id }, { plugnotas_company_registered: true, plugnotas_company_registered_at: agoraIso() });
  return { success: true };
};
