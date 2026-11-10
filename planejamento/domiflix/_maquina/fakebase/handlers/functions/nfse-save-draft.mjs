// Edge function `nfse-save-draft` falsa (T14, 1.38.24). Mesmo contrato da real
// (src-1.38.24/supabase/functions/_shared/nfse-handlers/save-draft.ts):
//   { id?, customerId|tomadorAvulso, intermediarioCustomerId|intermediarioAvulso, dataCompetencia, regimeApuracao,
//     servico: { serviceTypeId, codigoServico, codigoTributacaoMunicipal, codigoNbs, municipioIncidenciaIbge, descricao },
//     valores: { valorServico, aliquotaIssqn, tribIssqn, tpRetIssqn, valorPis, valorCofins, valorCsll, percentualTribSn } }
//   -> { emission } (sem id: INSERT com status 'rascunho'; com id: UPDATE só do que veio, e só se ainda for rascunho)
// O rascunho não leva `fiscal_ambiente` (ele só é fixado na transmissão, em nfse-emit). Na criação, o percentual do Simples
// vem de company_fiscal_settings quando a nota não trouxe o campo.
import { erro, limpo, fiscalDe } from './_fiscal/comum.mjs';
import { nowIso } from '../../core/util.mjs';

const num = (v) => {
  if (v === null || v === undefined || v === '') return null;
  const n = typeof v === 'number' ? v : Number(String(v).replace(',', '.'));
  return Number.isFinite(n) && n >= 0 ? n : null;
};
const data = (v) => (/^\d{4}-\d{2}-\d{2}/.test(limpo(v)) ? limpo(v).slice(0, 10) : null);
const ctribmun = (v) => (/^\d{3}$/.test(limpo(v)) ? limpo(v) : null);
const avulso = (v) => (v && typeof v === 'object' && !Array.isArray(v) && limpo(v.nome) ? v : null);

function parte(body, chaveCad, chaveAv, colCad, colAv, rotulo) {
  if (!(chaveCad in body) && !(chaveAv in body)) return null;
  const id = limpo(body[chaveCad]) || null;
  const av = chaveAv in body ? avulso(body[chaveAv]) : null;
  if (id && av) throw erro(400, 'tomador_ambiguo', `Escolha o ${rotulo} de UMA forma só: selecione um cliente cadastrado ou digite os dados manualmente.`);
  return { [colCad]: id, [colAv]: av };
}

export function colunasDoRascunho(body) {
  const cols = {};
  Object.assign(cols, parte(body, 'customerId', 'tomadorAvulso', 'customer_id', 'tomador_avulso', 'tomador') || {});
  Object.assign(cols, parte(body, 'intermediarioCustomerId', 'intermediarioAvulso', 'intermediario_customer_id', 'intermediario_avulso', 'intermediário') || {});
  if ('dataCompetencia' in body) cols.data_competencia = data(body.dataCompetencia);
  if ('regimeApuracao' in body) cols.regime_apuracao = limpo(body.regimeApuracao) || null;
  const s = body.servico;
  if (s && typeof s === 'object') {
    if ('serviceTypeId' in s) cols.service_type_id = limpo(s.serviceTypeId) || null;
    if ('codigoServico' in s) cols.codigo_servico = limpo(s.codigoServico) || null;
    if ('codigoNbs' in s) cols.codigo_nbs = limpo(s.codigoNbs) || null;
    if ('municipioIncidenciaIbge' in s) cols.municipio_incidencia_ibge = limpo(s.municipioIncidenciaIbge) || null;
    if ('descricao' in s) cols.descricao_servico = limpo(s.descricao) || null;
    if ('codigoTributacaoMunicipal' in s) cols.codigo_tributacao_municipal = ctribmun(s.codigoTributacaoMunicipal);
  }
  const v = body.valores;
  if (v && typeof v === 'object') {
    if ('valorServico' in v) cols.valor_servico = num(v.valorServico);
    if ('aliquotaIssqn' in v) cols.aliquota_issqn = num(v.aliquotaIssqn);
    if ('tribIssqn' in v) cols.trib_issqn = limpo(v.tribIssqn) || null;
    if ('tpRetIssqn' in v) cols.tp_ret_issqn = limpo(v.tpRetIssqn) || null;
    if ('valorPis' in v) cols.valor_pis = num(v.valorPis);
    if ('valorCofins' in v) cols.valor_cofins = num(v.valorCofins);
    if ('valorCsll' in v) cols.valor_csll = num(v.valorCsll);
    if ('percentualTribSn' in v) cols.percentual_trib_sn = num(v.percentualTribSn);
  }
  return cols;
}

export default async function nfseSaveDraft(body, { db, companyId, userId }) {
  if (!body || typeof body !== 'object' || body.__raw) throw erro(400, 'invalid_body', 'Requisição inválida.');
  const cols = colunasDoRascunho(body);
  const id = limpo(body.id);
  if (id) {
    const alvo = db.first('nfse_emissions', { id, company_id: companyId, status: 'rascunho' });
    if (!alvo) throw erro(404, 'draft_not_found', 'Rascunho não encontrado.');
    const [atual] = db.update('nfse_emissions', (r) => r === alvo, { ...cols, updated_at: nowIso() });
    return { emission: atual };
  }
  if (!('percentual_trib_sn' in cols)) {
    const pct = fiscalDe(db, companyId)?.percentual_trib_sn;
    if (pct != null) cols.percentual_trib_sn = pct;
  }
  const emission = db.insert('nfse_emissions', { ...cols, company_id: companyId, status: 'rascunho', origem: 'manual', created_by: userId || null }, { companyId });
  return { emission };
}
