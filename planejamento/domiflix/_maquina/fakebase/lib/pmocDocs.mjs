// T11 · geração falsa dos documentos PMOC (edge functions `generate-pmoc-{trt,certificado,cronograma,dossie,planilha}-pdf`).
// Espelha o contrato das funções reais (supabase/functions/generate-pmoc-*/index.ts, 1.38.19): GET ?contract_id=<uuid> com o token do usuário;
// grava uma linha em `pmoc_documents` (versão = maior da (contrato, tipo) + 1, `notes` "signature:signed|pending", `valid_until` só no termo
// e no certificado: hoje + validade em meses) e devolve { pdf_url, version, cached, signature_status }.
// Diferença deliberada: nunca devolve `cached: true` (a função real reaproveita a versão quando o conteúdo não mudou; aqui cada chamada cria uma
// versão nova, que é o que a aula mostra com "Gerar TRT individual"). O PDF não existe: nenhuma tela do vídeo o abre (nova aba).
import { FunctionError } from '../http/functions.mjs';
import { nowIso, now } from '../core/util.mjs';

const TIPOS = {
  'generate-pmoc-trt-pdf': { doc_type: 'termo_rt', validade: 'termo_rt_validity_months' },
  'generate-pmoc-certificado-pdf': { doc_type: 'certificado', validade: 'certificado_validity_months' },
  'generate-pmoc-cronograma-pdf': { doc_type: 'cronograma_anual', validade: null },
  'generate-pmoc-dossie-pdf': { doc_type: 'dossie_pmoc', validade: null },
  'generate-pmoc-planilha-pdf': { doc_type: 'planilha', validade: null },
};

function somaMeses(data, n) {
  const d = new Date(data.getTime());
  d.setUTCMonth(d.getUTCMonth() + n);
  return d.toISOString().slice(0, 10);
}

export function criaGerador(nomeFuncao) {
  const cfg = TIPOS[nomeFuncao];
  return async function gerar(_body, { db, url, userId }) {
    const contractId = url.searchParams.get('contract_id');
    if (!contractId) throw new FunctionError('contract_id_required', 400);
    const contrato = db.first('contracts', { id: contractId });
    if (!contrato) throw new FunctionError('contract_not_found', 404);
    if (contrato.is_pmoc !== true) throw new FunctionError('not_pmoc', 400);
    const rt = contrato.responsible_technician_id ? db.first('responsible_technicians', { id: contrato.responsible_technician_id }) : null;
    if (!rt && cfg.doc_type !== 'cronograma_anual') throw new FunctionError('rt_missing', 400);
    const existentes = db.rows('pmoc_documents').filter((d) => d.contract_id === contractId && d.doc_type === cfg.doc_type);
    const versao = existentes.reduce((mx, d) => Math.max(mx, d.version || 0), 0) + 1;
    const assinado = !!(rt && rt.signature_image_url);
    let validUntil = null;
    if (cfg.validade) {
      const modelo = db.rows('company_pmoc_document_templates').find((r) => String(r.company_id) === String(contrato.company_id));
      const meses = Number(modelo?.[cfg.validade]) || 12;
      validUntil = somaMeses(now(), meses);
    }
    const caminho = `${contrato.company_id}/${contractId}/${cfg.doc_type}-v${versao}.pdf`;
    db.insert('pmoc_documents', {
      company_id: contrato.company_id, contract_id: contractId, doc_type: cfg.doc_type, version: versao,
      content_hash: `fake-${cfg.doc_type}-${versao}`, pdf_storage_path: caminho, generated_at: nowIso(), generated_by: userId,
      notes: ['termo_rt', 'dossie_pmoc', 'certificado'].includes(cfg.doc_type) ? `signature:${assinado ? 'signed' : 'pending'}` : null,
      valid_until: validUntil,
    }, { companyId: contrato.company_id });
    return { pdf_url: `${url.origin}/storage/v1/object/public/pmoc-documents/${caminho}`, version: versao, cached: false, signature_status: assinado ? 'signed' : 'pending' };
  };
}
