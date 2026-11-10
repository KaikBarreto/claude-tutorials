// Edge function `nfse-cancel` falsa (T14, 1.38.24). Contrato da real (_shared/nfse-handlers/cancel.ts + sefin `cancelar`):
//   { emissionId, motivo (15 a 255 caracteres) } -> 200 { emission, status: 'cancelada', message }
// Cancelar é registrar o evento 101101 na chave da nota, no ambiente DA NOTA; a aula só abre a janela e volta (não chama).
import { erro, limpo, fiscalDe, ambienteValido, decifrar, instante, cnpjEmpresa } from './_fiscal/comum.mjs';
import { nowIso } from '../../core/util.mjs';

export default async function nfseCancel(body, { db, companyId }) {
  const id = limpo(body?.emissionId);
  if (!id) throw erro(400, 'missing_emission', 'Informe a emissão da nota fiscal.');
  const motivo = limpo(body?.motivo);
  if (motivo.length < 15 || motivo.length > 255) throw erro(422, 'invalid_reason', 'Informe o motivo do cancelamento, com 15 a 255 caracteres.');
  const e = db.first('nfse_emissions', { id, company_id: companyId });
  if (!e) throw erro(404, 'emission_not_found', 'Nota fiscal não encontrada.');
  if (e.status !== 'autorizada') throw erro(409, 'invalid_status', 'Só é possível cancelar uma nota autorizada.');
  if (!ambienteValido(e.fiscal_ambiente)) throw erro(409, 'fiscal_environment_unknown', 'Não foi possível confirmar o ambiente fiscal desta nota antiga. Fale com o suporte antes de cancelar.');
  if (cnpjEmpresa(db, companyId).length !== 14) throw erro(422, 'cnpj_ausente', 'Cadastre o CNPJ da empresa antes de cancelar uma nota fiscal.');
  const chave = limpo(e.chave_acesso) || limpo(e.referencia_fiscal);
  decifrar(db, companyId, fiscalDe(db, companyId), chave.replace(/\D/g, '') || 'cancelar_nfse');
  const agora = nowIso();
  const [atual] = db.update('nfse_emissions', (r) => r === e, {
    status: 'cancelada', status_fiscal_confirmado: true, status_fiscal_confirmado_em: agora, status_fiscal_fonte: 'sefin_nacional',
    status_fiscal_evidencia: { fonte: 'sefin_nacional', codigo: 'cancelada' },
  });
  db.insert('nfse_events', {
    nfse_emission_id: e.id, company_id: companyId, event_type: 'cancelada', status: 'cancelada',
    created_at: instante(db, 'nfse_events', companyId, { nfse_emission_id: e.id }), payload: { motivo, chaveAcesso: chave, cancelada: true },
  });
  return { emission: atual, status: 'cancelada', message: 'Nota fiscal cancelada.' };
}
