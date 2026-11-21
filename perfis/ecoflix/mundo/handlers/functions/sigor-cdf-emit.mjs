// Edge sigor-cdf-emit (T18 cap07; supabase/functions/sigor-cdf-emit), SIGOR simulado: o CDF só junta MTR já recebido e baixado no
// portal (os três de outubro da Auto Peças Vale Forte); emite o número oficial (2611000041 na primeira emissão da aula), grava o
// status "emitido" e o PDF (bucket nfe-danfes; arquivo simulado em mundo/storage/nfe-danfes/t18/cdf-<número>.pdf) e responde
// { success, numeroCdf, pdfUrl }. A emissão é definitiva. Reenvio (cap11): um CDF em "erro" que o cliente manda tentar de novo sai emitido
// (2611000057), como se a baixa já tivesse sido dada no portal; "Gerar PDF" (emitido sem PDF) só grava o PDF.
import { nowIso } from '../../../fakebase/core/util.mjs';
import { MTR_RECEBIDOS, proximoNumero } from '../../lib/mtr_sigor.mjs';

export default (body, { db, FunctionError }) => {
  const c = db.first('mtr_cdf', { id: body?.cdfId });
  if (!c) throw new FunctionError('CDF não encontrado.', 404, { success: false, error: 'CDF não encontrado.' });
  if (c.status === 'emitido' && c.numero_cdf) {
    const pdf = c.pdf_url || `t18/cdf-${c.numero_cdf}.pdf`;
    if (!c.pdf_url) db.update('mtr_cdf', { id: c.id }, { pdf_url: pdf, updated_at: nowIso() });
    return { success: true, numeroCdf: c.numero_cdf, pdfUrl: pdf, alreadyEmitted: true };
  }
  const cred = db.first('mtr_credentials', (r) => r.company_id === c.company_id && r.sistema === c.sistema);
  if (!cred) return { success: false, error: 'Configure o acesso ao SIGOR na aba MTR antes de emitir o CDF.' };
  const lista = (Array.isArray(c.lista_manifestos) ? c.lista_manifestos : []).map((x) => String(x?.manNumero ?? x ?? '').trim()).filter(Boolean);
  const reenvio = c.status === 'erro';   // "Tentar novamente" depois de dar a baixa no portal
  const naoRecebidos = reenvio ? [] : lista.filter((n) => !MTR_RECEBIDOS.includes(n));
  if (!reenvio && (!lista.length || naoRecebidos.length)) {
    const msg = 'Um ou mais MTRs ainda não foram recebidos no SIGOR. Dê baixa no recebimento do MTR no portal do órgão antes de emitir o CDF.';
    db.update('mtr_cdf', { id: c.id }, { status: 'erro', erro_mensagem: msg, updated_at: nowIso() });
    return { success: false, error: msg };
  }
  const usados = new Set(db.rows('mtr_cdf').map((r) => r.numero_cdf).filter(Boolean));
  const numero = ['2611000041', '2611000057', '2611000065'].find((n) => !usados.has(n)) || proximoNumero([...usados], '2611000041');
  const pdf = `t18/cdf-${numero}.pdf`;
  db.update('mtr_cdf', { id: c.id }, { numero_cdf: numero, status: 'emitido', emitted_at: nowIso(), erro_mensagem: null,
    pdf_url: pdf, raw_response: { numeroCDF: numero, mensagem: 'Certificado emitido (simulado).' } });
  return { success: true, numeroCdf: numero, pdfUrl: pdf };
};
