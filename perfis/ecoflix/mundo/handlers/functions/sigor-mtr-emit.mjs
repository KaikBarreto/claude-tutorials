// Edge sigor-mtr-emit (T18 cap04; supabase/functions/sigor-mtr-emit), SIGOR simulado: confere o rascunho, registra a tentativa
// "Autorizada" (Ver tentativas), grava o número oficial (2611000318 na primeira emissão da aula e 2611000325 na segunda, a do modelo do
// cap06), o status "emitido" e o PDF (caminho no bucket nfe-danfes, como a função real; o arquivo simulado fica em
// mundo/storage/nfe-danfes/t18/mtr-<número>.pdf) e responde { success, manifestoCodigo, pdfUrl }.
import { nowIso } from '../../../fakebase/core/util.mjs';
import { proximoNumero } from '../../lib/mtr_sigor.mjs';

// a sequência de números da aula (o órgão simulado devolve o primeiro que ainda não saiu)
const NUMEROS = ['2611000318', '2611000325', '2611000333', '2611000341'];

export default (body, { db, FunctionError }) => {
  const m = db.first('mtr_manifests', { id: body?.manifestId });
  if (!m) throw new FunctionError('Manifesto não encontrado.', 404, { success: false, error: 'Manifesto não encontrado.' });
  if (m.status === 'emitido' && m.manifesto_codigo) return { success: true, manifestoCodigo: m.manifesto_codigo, pdfUrl: m.pdf_url, alreadyEmitted: true };
  const cred = db.first('mtr_credentials', (r) => r.company_id === m.company_id && r.sistema === m.sistema);
  if (!cred) return { success: false, error: 'Configure o acesso ao SIGOR antes de emitir.', code: 'CREDENTIAL_MISSING', field: 'credential', stage: 'preflight' };
  const itens = db.find('mtr_manifest_items', { manifest_id: m.id });
  if (!itens.length) return { success: false, error: 'Inclua ao menos um resíduo.', code: 'ITEMS_MISSING', field: 'items', stage: 'preflight' };
  const inicio = nowIso();
  const usados = new Set(db.rows('mtr_manifests').map((r) => r.manifesto_codigo).filter(Boolean));
  const numero = NUMEROS.find((n) => !usados.has(n)) || proximoNumero([...usados], '2611000318');
  db.insert('mtr_manifest_attempts', { company_id: m.company_id, manifest_id: m.id, state: 'authorized', stage: 'complete', error_code: null, error_message: null,
    provider_request_started_at: inicio, finished_at: nowIso(), created_at: inicio });
  const pdf = `t18/mtr-${numero}.pdf`;
  db.update('mtr_manifests', { id: m.id }, { manifesto_codigo: numero, status: 'emitido', emitted_at: nowIso(), pdf_url: pdf, error_message: null,
    raw_response: { objetoResposta: { manifestoNumeroNacional: numero }, mensagem: 'Manifesto emitido (simulado).' } });
  return { success: true, manifestoCodigo: numero, pdfUrl: pdf };
};
