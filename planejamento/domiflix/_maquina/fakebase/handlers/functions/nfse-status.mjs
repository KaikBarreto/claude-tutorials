// Edge function `nfse-status` falsa (T14, 1.38.24). Mesmo contrato da real (_shared/nfse-handlers/status.ts + sefin `consultar`):
//   { emissionId } -> 200 { emission, status }
//   sem chave -> 409 missing_fiscal_reference · nota sem `fiscal_ambiente` -> 409 fiscal_environment_unknown
// A consulta é feita no ambiente DA NOTA (nunca no da empresa) e volta com a prova fiscal renovada
// (status_fiscal_confirmado_em = agora): é o que a tela pede quando a confirmação passa de 15 minutos. Grava o evento
// "status_consultado" e a decifra da consulta (contexto = chave) na trilha do certificado. Não preenche pdf_url/xml_url/protocolo.
import { erro, limpo, fiscalDe, ambienteValido, decifrar, instante } from './_fiscal/comum.mjs';
import { nowIso } from '../../core/util.mjs';

const TERMINAIS = new Set(['autorizada', 'rejeitada', 'cancelada']);

export default async function nfseStatus(body, { db, companyId }) {
  const id = limpo(body?.emissionId);
  if (!id) throw erro(400, 'missing_emission', 'Informe a emissão da nota fiscal.');
  const e = db.first('nfse_emissions', { id, company_id: companyId });
  if (!e) throw erro(404, 'emission_not_found', 'Nota fiscal não encontrada.');
  const ref = limpo(e.chave_acesso) || limpo(e.referencia_fiscal);
  if (!ref) throw erro(409, 'missing_fiscal_reference', 'Esta nota ainda não possui identificador na emissão fiscal.');
  if (!ambienteValido(e.fiscal_ambiente)) {
    throw erro(409, 'fiscal_environment_unknown', 'Não foi possível confirmar o ambiente fiscal desta nota antiga. Fale com o suporte antes de consultar novamente.');
  }
  decifrar(db, companyId, fiscalDe(db, companyId), ref.replace(/\D/g, '') || 'consultar_nfse');
  const status = e.status === 'cancelamento_pendente' ? 'cancelada' : TERMINAIS.has(e.status) ? e.status : 'autorizada';
  const agora = nowIso();
  const patch = {
    status,
    status_fiscal_confirmado: true,
    status_fiscal_confirmado_em: agora,
    status_fiscal_fonte: 'sefin_nacional',
    status_fiscal_evidencia: { fonte: 'sefin_nacional', codigo: status },
  };
  if (status === 'autorizada' && !e.emitida_em) patch.emitida_em = agora;
  const [atual] = db.update('nfse_emissions', (r) => r === e, patch);
  db.insert('nfse_events', {
    nfse_emission_id: e.id, company_id: companyId, event_type: 'status_consultado', status,
    created_at: instante(db, 'nfse_events', companyId, { nfse_emission_id: e.id }),
    payload: { status, chaveAcesso: ref, numero: e.numero_nfse, ambiente: e.fiscal_ambiente === 'producao' ? 1 : 2 },
  });
  return { emission: atual, status };
}
