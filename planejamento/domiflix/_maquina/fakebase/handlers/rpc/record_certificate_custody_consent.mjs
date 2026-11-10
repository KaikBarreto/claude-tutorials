// RPC record_certificate_custody_consent(p_version) -> void · supabase/migrations/20260903200000_consent_certificate_custody.sql:
// grava a autorização de guarda do certificado (finalidade 'certificate_custody') em consent_records ANTES do envio do A1.
import { nowIso } from '../../core/util.mjs';

export default async function recordCertificateCustodyConsent({ p_version }, { db, companyId, userId }) {
  db.insert('consent_records', {
    user_id: userId || null, company_id: companyId, purpose: 'certificate_custody', version: p_version || '1.0',
    accepted_at: nowIso(), ip_address: '127.0.0.1', user_agent: 'gravador Domiflix',
  }, { companyId });
  return undefined;
}
