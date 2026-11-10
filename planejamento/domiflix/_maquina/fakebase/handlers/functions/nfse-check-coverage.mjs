// Edge function `nfse-check-coverage` falsa (T14, 1.38.24). Mesmo contrato da real
// (src-1.38.24/supabase/functions/_shared/nfse-handlers/check-coverage.ts + providers/sefin.ts `checarCobertura`):
//   { ibge? } -> 200 { ibge, pode_emitir, municipio: null, uf: null, message }
//   sem IBGE -> 422 missing_ibge · IBGE inválido -> 422 invalid_ibge · sem certificado -> 422 certificado_ausente
// A consulta oficial usa o A1 (mTLS no ADN): por isso exige a custódia e registra a decifra "verificar_cobertura" na trilha
// do certificado (a tela mostra "Certificado utilizado"). Invalida a cobertura antes de consultar e grava o resultado
// em company_fiscal_settings (municipio_ibge, pode_emitir), como `executarConsultaCobertura`.
// Municípios "no Padrão Nacional" do mundo fictício: Niterói (3303302) e Rio de Janeiro (3304557); os demais respondem
// "ainda não habilitado".
import { erro, fiscalDe, decifrar } from './_fiscal/comum.mjs';

const COBERTOS = new Set(['3303302', '3304557']);

export default async function nfseCheckCoverage(body, { db, companyId }) {
  const fiscal = fiscalDe(db, companyId);
  let ibge = typeof body?.ibge === 'string' ? body.ibge.trim() : '';
  if (!ibge) ibge = String(fiscal?.municipio_ibge ?? '').trim();
  if (!ibge) {
    throw erro(422, 'missing_ibge', 'Informe o código IBGE do município nas configurações fiscais antes de verificar a cobertura.');
  }
  if (!/^\d{7}$/.test(ibge)) throw erro(422, 'invalid_ibge', 'Código IBGE inválido. Ele deve ter 7 dígitos.');

  const persistir = (pode) => db.upsert('company_fiscal_settings', ['company_id'], { company_id: companyId, municipio_ibge: ibge, pode_emitir: pode }, { companyId });
  persistir(false); // falha fechado: troca de município nunca herda a liberação anterior
  decifrar(db, companyId, fiscalDe(db, companyId), 'verificar_cobertura');
  const podeEmitir = COBERTOS.has(ibge);
  persistir(podeEmitir);
  return {
    ibge,
    pode_emitir: podeEmitir,
    municipio: null,
    uf: null,
    message: podeEmitir
      ? 'Município habilitado para emissão de NFS-e no Portal Nacional.'
      : 'Este município ainda não está habilitado para emissão de NFS-e no Portal Nacional.',
  };
}
