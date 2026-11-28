// Edge inbound-xml-import (1.60.39, "Importar XML" das Notas Recebidas: NotasRecebidasTab.tsx + hooks/useInboundXmlImport.ts; T16 cap23).
// Espelha supabase/functions/inbound-xml-import/index.ts e _shared/inbound-xml.ts: XML até 2 MB, sem DOCTYPE/ENTITY, evento fiscal
// recusado; NF-e só com protNFe cStat 100, chave de 44 dígitos igual à do protocolo e destinatário = CNPJ da empresa (o da configuração
// fiscal ou, sem ela, o de companies); NFS-e pelo tomador. A NF-e entra em inbound_nfe com as MESMAS colunas da edge (sem número nem
// série: a edge não grava) e a NFS-e em inbound_nfse; o fiscal_config_id é carimbado com a configuração padrão, como os gatilhos
// stamp_inbound_nfe(_se)_fiscal_config do banco. Nada sai da máquina: sem SEFAZ, sem provedor.
import { agoraIso } from '../../lib/nfe.mjs';

const dig = (v) => String(v ?? '').replace(/\D/g, '');
const bloco = (xml, nome) => (xml.match(new RegExp(`<(?:\\w+:)?${nome}(?:\\s[^>]*)?>([\\s\\S]*?)</(?:\\w+:)?${nome}>`)) || [])[1] ?? null;
const tag = (xml, nome) => {
  if (xml == null) return null;
  const v = (xml.match(new RegExp(`<(?:\\w+:)?${nome}(?:\\s[^>]*)?>([^<]*)</(?:\\w+:)?${nome}>`)) || [])[1];
  return v == null || !v.trim() ? null : v.trim();
};
const numero = (v) => {
  if (v == null) return null;
  const n = Number(String(v).replace(',', '.'));
  return Number.isFinite(n) ? n : null;
};
const docDe = (parte) => dig(tag(parte, 'CNPJ') ?? tag(parte, 'CPF') ?? tag(parte, 'Cnpj') ?? tag(parte, 'Cpf'));

function erro(FunctionError, code, message, status = 422) {
  return new FunctionError(message, status, { error: code, message });
}

function configPadrao(db, companyId) {
  return db.first('company_fiscal_config', (c) => c.company_id === companyId && c.is_default === true && c.ativo !== false)
    || db.first('company_fiscal_config', (c) => c.company_id === companyId && c.ativo !== false)
    || db.first('company_fiscal_config', (c) => c.company_id === companyId) || null;
}

export default (body, { db, store, companyId, FunctionError }) => {
  const xml = body?.xml;
  if (typeof xml !== 'string' || !xml.trim()) throw erro(FunctionError, 'invalid_xml', 'Selecione um arquivo XML válido.', 400);
  if (Buffer.byteLength(xml, 'utf8') > 2 * 1024 * 1024) throw erro(FunctionError, 'xml_too_large', 'O XML deve ter no máximo 2 MB.', 413);

  const cfg = configPadrao(db, companyId);
  const empresa = db.first('companies', { id: companyId }) || {};
  const cnpjEmpresa = dig(cfg?.cnpj ?? empresa.cnpj);
  if (cnpjEmpresa.length !== 14) throw erro(FunctionError, 'missing_tax_id', 'Preencha o CNPJ da empresa antes de importar notas recebidas.');

  // _shared/inbound-xml.ts, parseInboundXml
  if (!xml.trim().startsWith('<')) throw erro(FunctionError, 'invalid_xml', 'Selecione um arquivo XML válido.');
  if (/<!DOCTYPE|<!ENTITY/i.test(xml)) throw erro(FunctionError, 'unsafe_xml', 'O XML contém declarações não permitidas.');
  if (/<(?:\w+:)?(procEventoNFe|evento|retEvento)[\s>]/.test(xml)) {
    throw erro(FunctionError, 'event_xml', 'O arquivo contém um evento fiscal, não uma nota autorizada.');
  }
  const agora = agoraIso();

  if (/<(?:\w+:)?(nfeProc|NFe)[\s>]/.test(xml)) {
    const inf = bloco(xml, 'infNFe');
    if (!inf) throw erro(FunctionError, 'invalid_xml', 'O arquivo não contém uma NF-e válida.');
    const prot = bloco(xml, 'infProt');
    if (!prot || tag(prot, 'cStat') !== '100') throw erro(FunctionError, 'not_authorized', 'A NF-e do XML não está autorizada pela SEFAZ.');
    const id = (xml.match(/<(?:\w+:)?infNFe[^>]*\sId="([^"]*)"/) || [])[1] || null;
    const chave = dig(id ? id.replace(/^NFe/i, '') : tag(prot, 'chNFe'));
    if (!/^\d{44}$/.test(chave) || dig(tag(prot, 'chNFe')) !== chave) {
      throw erro(FunctionError, 'invalid_key', 'A chave de acesso da NF-e é inválida ou não confere com o protocolo.');
    }
    const destinatario = docDe(bloco(inf, 'dest'));
    if (!destinatario || destinatario !== cnpjEmpresa) {
      throw erro(FunctionError, 'recipient_mismatch', 'O XML não foi emitido para o CNPJ desta empresa. Confira o arquivo selecionado.');
    }
    const ide = bloco(inf, 'ide');
    const emit = bloco(inf, 'emit');
    const total = bloco(inf, 'ICMSTot');
    // a edge grava SÓ estas colunas (index.ts, payload da NF-e); upsert por (company_id, chave)
    const valores = {
      company_id: companyId, chave, origem: 'manual', emitente_cnpj: docDe(emit), emitente_nome: tag(emit, 'xNome'),
      valor: numero(tag(total, 'vNF')), data_emissao: tag(ide, 'dhEmi') ?? tag(ide, 'dEmi'), natureza: tag(ide, 'natOp'),
      situacao_sefaz: 'autorizada', xml_content: xml, resumo: false,
    };
    const ja = db.first('inbound_nfe', (n) => n.company_id === companyId && n.chave === chave);
    if (ja) {
      db.update('inbound_nfe', { id: ja.id }, { ...valores, updated_at: agora });
    } else {
      db.insert('inbound_nfe', {
        ...valores, fiscal_config_id: cfg?.id ?? null, manifestacao: 'nenhuma', purchase_id: null, financial_bill_id: null,
        balance_movement_id: null, pdf_url: null, created_at: agora, updated_at: agora,
      }, { companyId });
    }
    return { ok: true, tipo: 'nfe' };
  }

  // NFS-e (_shared/inbound-xml.ts, parseNfse): o tomador tem de ser a empresa
  const inf = bloco(xml, 'infNFSe') ?? bloco(xml, 'InfNfse');
  if (!inf) throw erro(FunctionError, 'invalid_xml', 'O arquivo não contém uma NFS-e válida.');
  const tomador = bloco(inf, 'Tomador') ?? bloco(inf, 'toma') ?? bloco(inf, 'TomadorServico');
  const tomadorDoc = docDe(tomador);
  if (!tomadorDoc || tomadorDoc !== cnpjEmpresa) {
    throw erro(FunctionError, 'recipient_mismatch', 'O XML não foi emitido para o CNPJ desta empresa. Confira o arquivo selecionado.');
  }
  const prestador = bloco(inf, 'Prestador') ?? bloco(inf, 'prest') ?? bloco(inf, 'PrestadorServico');
  const idNfse = (xml.match(/<(?:\w+:)?(?:infNFSe|InfNfse)[^>]*\sId="([^"]*)"/) || [])[1] || '';
  const chaveNfse = dig(idNfse || tag(inf, 'chNFSe'));
  const chaveAcesso = /^\d{50}$/.test(chaveNfse) ? chaveNfse : null;
  const num = tag(inf, 'Numero') ?? tag(inf, 'nNFSe') ?? tag(inf, 'numero');
  const prestadorDoc = docDe(prestador);
  if (!chaveAcesso && (!prestadorDoc || !num)) {
    throw erro(FunctionError, 'invalid_identity', 'A NFS-e não possui dados suficientes para identificar a nota.');
  }
  const valoresNfse = bloco(inf, 'Valores') ?? bloco(inf, 'valores');
  const servico = bloco(inf, 'Servico') ?? bloco(inf, 'serv');
  const linha = {
    company_id: companyId, origem: 'manual', chave_acesso: chaveAcesso, numero: num, serie: tag(inf, 'Serie'),
    codigo_verificacao: tag(inf, 'CodigoVerificacao') ?? tag(inf, 'cVerif'),
    municipio_incidencia_ibge: tag(servico, 'CodigoMunicipio') ?? tag(inf, 'cLocIncid'),
    data_emissao: tag(inf, 'DataEmissao') ?? tag(inf, 'dhProc') ?? tag(inf, 'dhEmi'), competencia: tag(inf, 'Competencia') ?? tag(inf, 'dCompet'),
    valor_servico: numero(tag(valoresNfse, 'ValorServicos') ?? tag(valoresNfse, 'vServ')),
    valor_liquido: numero(tag(valoresNfse, 'ValorLiquidoNfse') ?? tag(valoresNfse, 'vLiq')),
    valor_iss: numero(tag(valoresNfse, 'ValorIss') ?? tag(valoresNfse, 'vISSQN')),
    prestador_documento: prestadorDoc, prestador_nome: tag(prestador, 'RazaoSocial') ?? tag(prestador, 'xNome'),
    tomador_documento: tomadorDoc, tomador_nome: tag(tomador, 'RazaoSocial') ?? tag(tomador, 'xNome'),
    discriminacao: tag(servico, 'Discriminacao') ?? tag(servico, 'xDescServ'), situacao: 'autorizada', xml_content: xml,
  };
  const natural = chaveAcesso || `MUN:${linha.municipio_incidencia_ibge || '?'}|PRE:${prestadorDoc || '?'}|SER:${linha.serie || '?'}|NUM:${num || '?'}`;
  const ja = (store.rows('inbound_nfse') || []).find((n) => n.company_id === companyId
    && (n.chave_acesso || `MUN:${n.municipio_incidencia_ibge || '?'}|PRE:${n.prestador_documento || '?'}|SER:${n.serie || '?'}|NUM:${n.numero || '?'}`) === natural);
  if (ja) db.update('inbound_nfse', { id: ja.id }, { ...linha, updated_at: agora });
  else db.insert('inbound_nfse', { ...linha, fiscal_config_id: cfg?.id ?? null, created_at: agora, updated_at: agora }, { companyId });
  return { ok: true, tipo: 'nfse' };
};
