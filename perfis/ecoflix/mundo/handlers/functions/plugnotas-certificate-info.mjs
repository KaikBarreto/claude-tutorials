// Edge plugnotas-certificate-info (hooks/useCertificateInfo.tsx): validade do certificado A1 do emitente. Sem certificado enviado,
// { success: true, hasCertificate: false }; com ele, o resumo que a edge real monta (T16: "RECICLA VALE METAIS LTDA", até 14/09/2027).
import { configFiscal } from '../../lib/nfe.mjs';
import { agoraMs } from '../../lib/eco.mjs';

export default (body, { store, companyId }) => {
  const cfg = configFiscal(store, body?.companyId || companyId, body?.fiscalConfigId);
  if (!cfg || !cfg.plugnotas_certificate_uploaded) return { success: true, hasCertificate: false };
  const info = cfg.plugnotas_certificate_info || {};
  const venc = info.valid_until || '2027-09-15T02:59:59.000Z';
  const dias = Math.floor((Date.parse(venc) - agoraMs()) / 86400000);
  return {
    success: true, hasCertificate: true, vencimento: venc, daysRemaining: dias, isExpired: dias < 0, implausibleValidity: false,
    certificateName: info.cn || 'RECICLA VALE METAIS LTDA', cnpjFromCert: '47318506000107', hash: info.hash || null,
    uploadedAt: info.uploaded_at || null,
  };
};
