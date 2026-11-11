// Edge plugnotas-upload-certificate (CertificadoSection.tsx): recebe o .pfx em base64 e a senha, "valida" e grava na configuração
// fiscal do emitente (plugnotas_certificate_uploaded, plugnotas_certificate_info) com vaultStored true, como a edge nova. Sem SEFAZ e
// sem provedor: confere só a extensão do arquivo e a senha preenchida (o desvio do gravador entrega o corpo inteiro; docs/08 T14).
// A senha não é gravada nem devolvida.
import { configFiscal, agoraIso } from '../../lib/nfe.mjs';

const falha = (errorCode, error) => ({ success: false, errorCode, error, vaultStored: false });

export default (body, { store, db, companyId, FunctionError }) => {
  const cid = body?.companyId || companyId;
  const nome = String(body?.certificateFilename || '');
  if (!/\.(pfx|p12)$/i.test(nome)) return falha('arquivo_invalido', 'Envie o arquivo do certificado A1 (.pfx ou .p12).');
  if (!body?.certificatePassword) return falha('senha_ausente', 'Informe a senha do certificado');
  if (!body?.certificateBase64) return falha('arquivo_vazio', 'O arquivo do certificado chegou vazio.');
  const cfg = configFiscal(store, cid, body?.fiscalConfigId);
  if (!cfg) throw new FunctionError('Configuração fiscal não encontrada', 404, { success: false, vaultStored: false });
  const agora = agoraIso();
  const info = { filename: nome, uploaded_at: agora, valid_until: '2027-09-15T02:59:59.000Z', hash: 'a1f3c92e7d', cn: 'RECICLA VALE METAIS LTDA' };
  db.update('company_fiscal_config', { id: cfg.id }, {
    plugnotas_certificate_id: 'cert-recicla-vale-a1', plugnotas_certificate_uploaded: true, plugnotas_certificate_info: info,
  });
  return {
    success: true, message: 'Certificado digital validado com sucesso!', certificateId: 'cert-recicla-vale-a1', vaultStored: true,
    fiscalConfigId: cfg.id, data: { validUntil: info.valid_until },
  };
};
