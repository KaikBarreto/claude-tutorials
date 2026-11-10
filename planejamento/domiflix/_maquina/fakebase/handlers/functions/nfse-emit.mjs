// Edge function `nfse-emit` falsa (T14, 1.38.24). Mesmo contrato da real
// (src-1.38.24/supabase/functions/_shared/nfse-handlers/emit.ts + providers/sefin.ts `emitir`):
//   { emissionId } (rascunho salvo pela tela) ou o corpo completo (customerId, servico, valores, dataCompetencia)
//   -> 202 { emission, already_emitted: false, message: 'Nota fiscal enviada para emissão. Acompanhe o status.' }
// O motor próprio é SÍNCRONO: a nota já volta AUTORIZADA, com número e chave de acesso (50 dígitos), prova fiscal
// (status_fiscal_confirmado/_em/_fonte/_evidencia) e `fiscal_ambiente` fixo; NÃO preenche `protocolo`, `pdf_url` nem
// `xml_url` (o PDF sai sob demanda por nfse-danfse; o XML fica só no evento). Gates na ordem do real: config fiscal,
// ambiente, rascunho, tomador, cobertura + certificado (`validarProntidaoFiscal`), cota (só em Produção), NBS, campos.
// Simples Nacional sem retenção (opSimpNac 3, regApTribSN 1, tpRetIssqn 1): a alíquota é suprimida (E0625) e `valor_iss`
// fica nulo. Cada transmissão registra a decifra "emitir_nfse" na trilha do certificado e consome um número de DPS.
import { erro, limpo, digitos, fiscalDe, ambienteValido, certificadoValido, decifrar, cnpjEmpresa, chaveNfse, instante } from './_fiscal/comum.mjs';
import { colunasDoRascunho } from './nfse-save-draft.mjs';
import nfseCanEmit from '../rpc/nfse_can_emit.mjs';
import { nowIso } from '../../core/util.mjs';

function prontidao(fiscal) {
  if (!ambienteValido(fiscal.fiscal_ambiente)) return erro(422, 'fiscal_environment_invalid', 'Selecione o ambiente fiscal nas configurações antes de emitir a nota.');
  if (fiscal.pode_emitir !== true) return erro(422, 'municipality_not_enabled', 'Confirme a liberação do município no Portal Nacional antes de emitir a nota fiscal.');
  if (!limpo(fiscal.certificado_ref)) return erro(422, 'certificate_missing', 'Envie o certificado digital A1 da empresa antes de emitir notas fiscais.');
  const v = Date.parse(fiscal.certificate_expires_at || '');
  if (!Number.isFinite(v)) return erro(422, 'certificate_expiry_unknown', 'Não foi possível confirmar a validade do certificado digital. Envie o certificado novamente.');
  if (!certificadoValido(fiscal)) return erro(422, 'certificate_expired', 'O certificado digital está expirado. Envie um certificado válido antes de emitir.');
  return null;
}

export default async function nfseEmit(body, { db, companyId, userId }) {
  if (!body || typeof body !== 'object' || body.__raw) throw erro(400, 'invalid_body', 'Requisição inválida.');
  const emissionId = limpo(body.emissionId);
  let draft = null;
  if (emissionId) {
    draft = db.first('nfse_emissions', { id: emissionId, company_id: companyId });
    if (!draft || draft.status !== 'rascunho') throw erro(404, 'draft_not_found', 'Rascunho não encontrado.');
  }
  const doCorpo = emissionId ? {} : colunasDoRascunho({ ...body, valores: { ...(body.valores || {}), aliquotaIssqn: body.valores?.aliquotaIss } });
  const n = { ...(draft || {}), ...doCorpo };

  const fiscal = fiscalDe(db, companyId);
  if (!fiscal) throw erro(422, 'fiscal_not_configured', 'A emissão fiscal ainda não foi configurada para esta empresa.');
  const ambiente = ambienteValido(fiscal.fiscal_ambiente);
  if (!ambiente) throw erro(422, 'fiscal_environment_invalid', 'Selecione o ambiente fiscal nas configurações antes de emitir a nota.');

  const customer = n.customer_id ? db.first('customers', { id: n.customer_id }) : null;
  if (!n.customer_id && !n.tomador_avulso) throw erro(422, 'missing_customer', 'Selecione o tomador do serviço antes de emitir.');
  if (n.customer_id && !customer) throw erro(404, 'customer_not_found', 'Cliente não encontrado.');
  if (n.intermediario_customer_id || n.intermediario_avulso) {
    throw erro(422, 'intermediario_nao_suportado', 'O intermediário do serviço ainda não é enviado na nota fiscal. Remova o intermediário para emitir — os dados ficam salvos no rascunho.');
  }
  const valorServico = Number(n.valor_servico || 0);
  if (!(valorServico > 0)) throw erro(422, 'invalid_value', 'Informe um valor de serviço maior que zero.');

  const gate = prontidao(fiscal);
  if (gate) throw gate;

  if (ambiente === 'producao') {
    const q = await nfseCanEmit({ p_company_id: companyId }, { db, companyId });
    if (q.allowed === false) {
      throw erro(402, 'nfse_quota_exceeded', `Você atingiu o limite de ${q.limit} notas fiscais deste mês no seu nível atual.`, { used: q.used, limit: q.limit, tier: q.tier, next_tier: q.next_tier });
    }
  }

  const st = n.service_type_id ? db.first('service_types', { id: n.service_type_id }) : null;
  const codigoServico = limpo(n.codigo_servico) || limpo(st?.codigo_servico) || limpo(fiscal.codigo_servico_default);
  const codigoNbs = limpo(n.codigo_nbs) || limpo(st?.codigo_nbs) || limpo(fiscal.codigo_nbs_default);
  if (!codigoNbs) throw erro(422, 'missing_nbs', 'Configure o código NBS do serviço nas configurações fiscais antes de emitir.');
  const missing = [];
  const docTomador = customer ? digitos(customer.document) : digitos(n.tomador_avulso?.documento);
  if (!docTomador) missing.push('CPF/CNPJ do cliente');
  if (!codigoServico) missing.push('código de serviço');
  if (!limpo(n.descricao_servico)) missing.push('descrição do serviço');
  if (missing.length) throw erro(422, 'missing_fields', `Não foi possível emitir a nota. Faltando: ${missing.join(', ')}.`, { missing_fields: missing });

  // Simples Nacional (ME/EPP) sem retenção: alíquota suprimida (E0625), ISS não destacado.
  const simples = (fiscal.regime_tributario || 'simples_nacional') === 'simples_nacional';
  const regAp = limpo(fiscal.reg_ap_trib_sn) || '1';
  const tpRet = /^[1-3]$/.test(limpo(n.tp_ret_issqn)) ? limpo(n.tp_ret_issqn) : '';
  const aliquota = Number(n.aliquota_issqn ?? st?.iss_aliquota ?? fiscal.iss_aliquota ?? 0) || 0;
  const suprime = simples && regAp === '1' && (tpRet || '1') === '1';
  const valorIss = suprime || !(aliquota > 0) ? null : Math.round(valorServico * aliquota) / 100;

  // ---- motor síncrono: decifra o A1, transmite a DPS e volta com a NFS-e autorizada
  decifrar(db, companyId, fiscal, 'emitir_nfse');
  const numeroDps = Number(fiscal.ultimo_numero_dps || 0) + 1;
  db.update('company_fiscal_settings', { company_id: companyId }, { ultimo_numero_dps: numeroDps });
  const mesmas = db.find('nfse_emissions', (r) => r.company_id === companyId && r.fiscal_ambiente === ambiente && r.numero_nfse);
  const numero = String(mesmas.reduce((m, r) => Math.max(m, Number(r.numero_nfse) || 0), 0) + 1);
  const emitidaEm = nowIso();
  const cnpj = cnpjEmpresa(db, companyId);
  const chave = chaveNfse({ ibge: fiscal.municipio_ibge, cnpj, numero, emitidaEm, semente: `${companyId}:${ambiente}:${numero}` });
  const idDps = 'DPS' + String(fiscal.municipio_ibge || '').padStart(7, '0') + '2' + cnpj.padStart(14, '0') + String(fiscal.serie_dps || '1').padStart(5, '0') + String(numeroDps).padStart(15, '0');
  const competencia = n.data_competencia || emitidaEm.slice(0, 10);
  const ctribmun = limpo(n.codigo_tributacao_municipal) || limpo(st?.codigo_tributacao_municipal) || null;
  const municipioIncidencia = limpo(n.municipio_incidencia_ibge) || limpo(fiscal.municipio_ibge) || null;
  const evidencia = { fonte: 'sefin_nacional', codigo: 'autorizada' };
  const campos = {
    customer_id: n.customer_id || null,
    tomador_avulso: n.tomador_avulso || null,
    idempotency_key: `${ambiente}:${draft ? draft.id : `${n.customer_id}:${valorServico}:${competencia}`}`,
    fiscal_ambiente: ambiente,
    valor_servico: valorServico,
    valor_iss: valorIss,
    descricao_servico: limpo(n.descricao_servico),
    data_competencia: competencia,
    codigo_servico: codigoServico,
    codigo_nbs: codigoNbs,
    municipio_incidencia_ibge: municipioIncidencia,
    aliquota_issqn: suprime ? null : aliquota || null,
    trib_issqn: limpo(n.trib_issqn) || null,
    tp_ret_issqn: tpRet || null,
    percentual_trib_sn: n.percentual_trib_sn ?? fiscal.percentual_trib_sn ?? null,
    codigo_tributacao_municipal: ctribmun,
    origem: 'manual',
    nfse_auto_job_id: null,
    status: 'autorizada',
    referencia_fiscal: chave,
    requisicao_fiscal_id: null,
    error_message: null,
    status_fiscal_confirmado: true,
    status_fiscal_confirmado_em: emitidaEm,
    status_fiscal_fonte: 'sefin_nacional',
    status_fiscal_evidencia: evidencia,
    numero_nfse: numero,
    chave_acesso: chave,
    emitida_em: emitidaEm,
  };
  let emission;
  if (draft) {
    [emission] = db.update('nfse_emissions', (r) => r === draft, { ...campos, created_by: draft.created_by || userId || null, updated_at: nowIso() });
  } else {
    emission = db.insert('nfse_emissions', { company_id: companyId, financial_transaction_id: null, created_by: userId || null, ...campos }, { companyId });
  }
  db.insert('nfse_events', {
    nfse_emission_id: emission.id, company_id: companyId, event_type: 'emitida', status: 'autorizada',
    created_at: instante(db, 'nfse_events', companyId, { nfse_emission_id: emission.id }),
    payload: {
      status: 'autorizada', chaveAcesso: chave, numero, idDps, dataEmissao: emitidaEm, ambiente: ambiente === 'producao' ? 1 : 2,
      xml: `<NFSe versao="1.00"><infNFSe Id="NFS${chave}"><nNFSe>${numero}</nNFSe><ambGer>2</ambGer><tpAmb>${ambiente === 'producao' ? 1 : 2}</tpAmb></infNFSe></NFSe>`,
    },
  });
  return { emission, already_emitted: false, message: 'Nota fiscal enviada para emissão. Acompanhe o status.' };
}
