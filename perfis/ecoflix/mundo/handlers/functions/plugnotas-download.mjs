// XML (e PDF) de uma NF-e já autorizada (T17 cap11, Exportação Contábil: o pacote baixa o XML de cada nota pela função;
// supabase/functions/plugnotas-download). O XML é montado aqui com os dados da nota e dos itens (fictício, sem assinatura).
import { pdfSimples } from './plugnotas-mdfe-download.mjs';

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export default (body, { db, FunctionError }) => {
  const n = db.first('invoices', { id: body?.invoiceId });
  if (!n) throw new FunctionError('Nota não encontrada', 404, { success: false });
  if (!n.nfe_key) return { success: false, error: 'Nota sem chave de acesso' };
  const cfg = db.first('company_fiscal_config', { id: n.fiscal_config_id }) || {};
  const parc = (n.customer_id && db.first('customers', { id: n.customer_id })) || (n.supplier_id && db.first('suppliers', { id: n.supplier_id })) || n.destinatario_avulso || {};
  const itens = db.find('invoice_items', { invoice_id: n.id });
  if (body?.type === 'pdf') {
    return { success: true, content: pdfSimples([`DANFE - NF-e ${n.invoice_number} serie ${n.serie}`, `Chave ${n.nfe_key}`, `${esc(parc.name || '')}`,
      `Valor total R$ ${n.total_amount}`, 'Documento ficticio (ambiente de demonstracao)']) };
  }
  const det = itens.map((it, i) => `<det nItem="${i + 1}"><prod><xProd>${esc(it.material_name)}</xProd><NCM>${esc(it.ncm)}</NCM><CFOP>${esc(it.cfop)}</CFOP><uCom>${esc(it.unit)}</uCom><qCom>${it.quantity}</qCom><vUnCom>${it.unit_price}</vUnCom><vProd>${it.total_price}</vProd></prod></det>`).join('');
  const xml = `<?xml version="1.0" encoding="UTF-8"?><nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe"><NFe><infNFe Id="NFe${n.nfe_key}" versao="4.00">`
    + `<ide><natOp>${esc(n.nature_operation)}</natOp><mod>55</mod><serie>${n.serie}</serie><nNF>${n.invoice_number}</nNF><dhEmi>${n.issue_date}</dhEmi><tpNF>${n.invoice_type === 'saida' ? 1 : 0}</tpNF></ide>`
    + `<emit><CNPJ>${esc(cfg.cnpj)}</CNPJ><xNome>${esc(cfg.razao_social)}</xNome></emit><dest><xNome>${esc(parc.razao_social || parc.name)}</xNome></dest>${det}`
    + `<total><ICMSTot><vProd>${n.total_products}</vProd><vNF>${n.total_amount}</vNF></ICMSTot></total></infNFe></NFe>`
    + `<protNFe versao="4.00"><infProt><chNFe>${n.nfe_key}</chNFe><dhRecbto>${n.authorized_at}</dhRecbto><nProt>${esc(n.nfe_protocol)}</nProt><cStat>100</cStat><xMotivo>Autorizado o uso da NF-e</xMotivo></infProt></protNFe></nfeProc>`;
  return { success: true, content: xml };
};
