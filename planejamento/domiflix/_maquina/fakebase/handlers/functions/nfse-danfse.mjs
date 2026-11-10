// Edge function `nfse-danfse` falsa (T14, 1.38.24). Mesmo contrato da real (_shared/nfse-handlers/danfse.ts + sefin `danfse`):
//   { emissionId } -> 200 { pdfBase64, pdfUrl: null, nomeArquivo: 'NFSe-<número>.pdf' }
//   só nota autorizada, cancelada ou com cancelamento pendente, com chave e `fiscal_ambiente`.
// O motor próprio não guarda o PDF numa URL: gera sob demanda. Aqui o PDF é FICTÍCIO, de layout próprio (sem brasão nem
// marca de órgão público), com a marca d'água "SEM VALOR FISCAL" quando a nota é de homologação. Registra a decifra.
import { erro, limpo, fiscalDe, ambienteValido, decifrar, pdfDaNota, brl, dataBR, cnpjMascara, codigoServicoMascara, digitos } from './_fiscal/comum.mjs';

export default async function nfseDanfse(body, { db, companyId }) {
  const id = limpo(body?.emissionId);
  if (!id) throw erro(400, 'missing_emission', 'Informe a emissão da nota fiscal.');
  const e = db.first('nfse_emissions', { id, company_id: companyId });
  if (!e) throw erro(404, 'emission_not_found', 'Nota fiscal não encontrada.');
  if (!['autorizada', 'cancelada', 'cancelamento_pendente'].includes(limpo(e.status))) {
    throw erro(409, 'invalid_status', 'O PDF só fica disponível para notas autorizadas.');
  }
  const chave = limpo(e.chave_acesso) || limpo(e.referencia_fiscal);
  if (!chave) throw erro(409, 'missing_access_key', 'Esta nota ainda não tem chave de acesso. Atualize o status e tente de novo.');
  if (!ambienteValido(e.fiscal_ambiente)) {
    throw erro(409, 'fiscal_environment_unknown', 'Não foi possível confirmar o ambiente fiscal desta nota antiga. Fale com o suporte antes de gerar o PDF.');
  }
  const fiscal = fiscalDe(db, companyId);
  decifrar(db, companyId, fiscal, digitos(chave) || 'danfse');
  const cs = db.first('company_settings', { company_id: companyId }) || {};
  const emp = db.first('companies', { id: companyId }) || {};
  const c = e.customer_id ? db.first('customers', { id: e.customer_id }) || {} : {};
  const homolog = e.fiscal_ambiente === 'homologacao';
  const end = (o) => [o.address && `${o.address}${o.address_number ? ', ' + o.address_number : ''}`, o.neighborhood, o.city && `${o.city}/${o.state || ''}`, o.zip_code && `CEP ${o.zip_code}`].filter(Boolean).join(' - ');
  const pdf = pdfDaNota({
    titulo: 'Nota Fiscal de Serviço Eletrônica (NFS-e)',
    subtitulo: homolog ? 'Ambiente de homologação: documento de teste, sem valor fiscal.' : 'Ambiente de produção.',
    numero: e.numero_nfse,
    emitidaEm: dataBR(e.emitida_em, true),
    competencia: dataBR(e.data_competencia ? `${e.data_competencia}T12:00:00-03:00` : e.created_at),
    chave,
    marcaDagua: homolog ? 'SEM VALOR FISCAL' : null,
    blocos: [
      { titulo: 'Prestador do serviço', linhas: [cs.name || emp.name || '-', `CNPJ ${cnpjMascara(cs.document || emp.cnpj)}   Inscrição Municipal ${fiscal?.inscricao_municipal || '-'}`, end(cs)] },
      { titulo: 'Tomador do serviço', linhas: [c.company_name ? `${c.name} (${c.company_name})` : c.name || e.tomador_avulso?.nome || '-', `CPF/CNPJ ${cnpjMascara(c.document || e.tomador_avulso?.documento)}`, end(c)] },
      { titulo: 'Serviço', linhas: [`Código de tributação nacional ${codigoServicoMascara(e.codigo_servico)}   Código municipal ${e.codigo_tributacao_municipal || '-'}   NBS ${e.codigo_nbs || '-'}`, `Discriminação: ${e.descricao_servico || '-'}`] },
      { titulo: 'Valores', linhas: [`Valor do serviço ${brl(e.valor_servico)}`, e.valor_iss != null ? `ISS ${brl(e.valor_iss)}` : 'ISS recolhido pelo Simples Nacional (sem retenção)', `Tributos aproximados do Simples Nacional ${e.percentual_trib_sn != null ? String(Number(e.percentual_trib_sn).toFixed(2)).replace('.', ',') + '%' : '-'}`, `Valor líquido ${brl(e.valor_servico)}`] },
    ],
    rodape: 'Documento gerado por simulação para material de treinamento. Dados fictícios.',
  });
  return { pdfBase64: pdf.toString('base64'), pdfUrl: null, nomeArquivo: `NFSe-${e.numero_nfse || chave.slice(0, 12)}.pdf` };
}
