// NF-e de mercadoria simulada (T16): o que as edges plugnotas-* e as RPCs da NF-e fazem no banco, em memória e sem SEFAZ, sem
// provedor e sem cota real. Chave de 44 dígitos (cUF 35 + AAMM + CNPJ + 55 + série + número + tpEmis 1 + cNF + DV módulo 11),
// protocolo de 15 dígitos ("1352601" + 8), XML 4.00 montado com os dados da nota (fictício, sem assinatura).
import { agoraMs } from './eco.mjs';

export const agoraIso = () => new Date(agoraMs()).toISOString();
const dig = (s) => String(s ?? '').replace(/\D/g, '');
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const hash = (s) => {
  let h = 2166136261;
  for (const ch of String(s)) h = Math.imul(h ^ ch.charCodeAt(0), 16777619) >>> 0;
  return h;
};

/** A configuração fiscal do emitente: a pedida (fiscalConfigId) ou a padrão da empresa. */
export function configFiscal(store, companyId, fiscalConfigId) {
  const linhas = store.rows('company_fiscal_config').filter((c) => c.company_id === companyId);
  if (fiscalConfigId) return linhas.find((c) => c.id === fiscalConfigId) || null;
  return linhas.find((c) => c.is_default && c.ativo !== false) || linhas.find((c) => c.ativo !== false) || linhas[0] || null;
}

export function dv11(base) {
  let soma = 0;
  let peso = 2;
  for (let i = base.length - 1; i >= 0; i--) {
    soma += Number(base[i]) * peso;
    peso = peso === 9 ? 2 : peso + 1;
  }
  const r = soma % 11;
  return r < 2 ? '0' : String(11 - r);
}

/** Chave de acesso da NF-e (modelo 55) emitida pelo CNPJ no instante dado. */
export function chaveNfe(cnpj, numero, serie, iso) {
  const b = new Date(new Date(iso).getTime() - 3 * 3600000);
  const aamm = String(b.getUTCFullYear()).slice(2) + String(b.getUTCMonth() + 1).padStart(2, '0');
  const cnf = String(hash(`${cnpj}-${numero}-${serie}`) % 1e8).padStart(8, '0');
  const base = `35${aamm}${dig(cnpj).padStart(14, '0')}55${String(serie).padStart(3, '0')}${String(numero).padStart(9, '0')}1${cnf}`;
  return base + dv11(base);
}

export const protocolo = (semente) => `1352601${String(hash(`prot-${semente}`) % 1e8).padStart(8, '0')}`;

/** Próximo número da série (o que `get_next_invoice_number` devolve): o maior entre a série cadastrada, as notas da série e a
 * "última nota" declarada na configuração, mais um. */
export function proximoNumero(store, companyId, serie, fiscalConfigId) {
  const cfg = configFiscal(store, companyId, fiscalConfigId);
  const s = Number(serie) || 1;
  let ult = 0;
  for (const r of store.rows('nfe_series')) {
    if (r.company_id !== companyId || Number(r.serie_number) !== s) continue;
    if (cfg && r.fiscal_config_id && r.fiscal_config_id !== cfg.id) continue;
    ult = Math.max(ult, Number(r.last_invoice_number) || 0);
  }
  for (const n of store.rows('invoices')) {
    if (n.company_id !== companyId || Number(n.serie) !== s || n.invoice_number == null) continue;
    if (cfg && n.fiscal_config_id && n.fiscal_config_id !== cfg.id) continue;
    if (Number(n.modelo || 55) !== 55) continue;
    ult = Math.max(ult, Number(n.invoice_number) || 0);
  }
  if (cfg && String(cfg.last_invoice_serie || '') === String(s)) ult = Math.max(ult, Number(cfg.last_invoice_number) || 0);
  return ult + 1;
}

/** A série cadastrada acompanha a última nota emitida nela (como a função do banco faz ao reservar o número). */
export function avancaSerie(db, store, companyId, cfgId, serie, numero) {
  const s = Number(serie) || 1;
  const r = store.rows('nfe_series').find((x) => x.company_id === companyId && Number(x.serie_number) === s
    && (!x.fiscal_config_id || !cfgId || x.fiscal_config_id === cfgId));
  if (r) {
    if ((Number(r.last_invoice_number) || 0) < numero) db.update('nfe_series', { id: r.id }, { last_invoice_number: numero });
  } else {
    db.insert('nfe_series', { company_id: companyId, fiscal_config_id: cfgId, serie_number: s, last_invoice_number: numero }, { companyId });
  }
}

export function parceiroDaNota(store, n) {
  if (n.customer_id) return store.rows('customers').find((c) => c.id === n.customer_id) || null;
  if (n.supplier_id) return store.rows('suppliers').find((c) => c.id === n.supplier_id) || null;
  return null;
}

const f2 = (v) => (Number(v) || 0).toFixed(2);
const f4 = (v) => (Number(v) || 0).toFixed(4);

/** XML autorizado (nfeProc) da nota, com os itens e o protocolo. */
export function xmlNfe(store, n) {
  const cfg = store.rows('company_fiscal_config').find((c) => c.id === n.fiscal_config_id) || {};
  const p = parceiroDaNota(store, n);
  const itens = store.rows('invoice_items').filter((i) => i.invoice_id === n.id)
    .sort((a, b) => (Number(a.nfe_item_number) || 0) - (Number(b.nfe_item_number) || 0));
  const consumidor = n.is_consumer_final && !p;
  const destDoc = consumidor ? dig(cfg.cnpj) : dig(p?.cpf_cnpj);
  const destNome = consumidor ? (cfg.razao_social || '') : (p?.razao_social || p?.name || '');
  const det = itens.map((it, i) => `<det nItem="${i + 1}"><prod><cProd>${esc(String(it.material_id || i + 1).slice(0, 8))}</cProd><cEAN>SEM GTIN</cEAN>`
    + `<xProd>${esc(it.material_name)}</xProd><NCM>${dig(it.ncm)}</NCM><CFOP>${esc(it.cfop)}</CFOP><uCom>${esc((it.unit || 'KG').toUpperCase())}</uCom>`
    + `<qCom>${f4(it.quantity)}</qCom><vUnCom>${Number(it.unit_price || 0).toFixed(10)}</vUnCom><vProd>${f2(it.total_price)}</vProd>`
    + `<cEANTrib>SEM GTIN</cEANTrib><uTrib>${esc((it.unit || 'KG').toUpperCase())}</uTrib><qTrib>${f4(it.quantity)}</qTrib>`
    + `<vUnTrib>${Number(it.unit_price || 0).toFixed(10)}</vUnTrib><indTot>1</indTot></prod>`
    + `<imposto><ICMS><ICMS00><orig>0</orig><CST>${esc(it.cst_icms || '00')}</CST></ICMS00></ICMS></imposto></det>`).join('');
  const transp = store.rows('transportadoras').find((t) => t.id === n.transportadora_id)
    || (n.transp_razao_social ? { razao_social: n.transp_razao_social, cpf_cnpj: n.transp_cpf_cnpj, placa_veiculo: n.transp_placa } : null);
  const modFrete = n.modalidade_frete ?? 9;
  return '<?xml version="1.0" encoding="UTF-8"?><nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">'
    + `<NFe xmlns="http://www.portalfiscal.inf.br/nfe"><infNFe versao="4.00" Id="NFe${n.nfe_key}"><ide><cUF>35</cUF>`
    + `<natOp>${esc(n.nature_operation)}</natOp><mod>55</mod><serie>${n.serie ?? 1}</serie><nNF>${n.invoice_number}</nNF>`
    + `<dhEmi>${esc(n.issue_date)}</dhEmi><tpNF>${n.invoice_type === 'saida' ? 1 : 0}</tpNF><tpAmb>1</tpAmb><finNFe>${n.finalidade || 1}</finNFe></ide>`
    + `<emit><CNPJ>${dig(cfg.cnpj)}</CNPJ><xNome>${esc(cfg.razao_social)}</xNome><xFant>${esc(cfg.nome_fantasia)}</xFant>`
    + `<enderEmit><xLgr>${esc(cfg.logradouro)}</xLgr><nro>${esc(cfg.numero)}</nro><xBairro>${esc(cfg.bairro)}</xBairro>`
    + `<cMun>${esc(cfg.codigo_ibge)}</cMun><xMun>${esc(cfg.cidade)}</xMun><UF>${esc(cfg.uf)}</UF><CEP>${dig(cfg.cep)}</CEP></enderEmit>`
    + `<IE>${dig(cfg.inscricao_estadual)}</IE><CRT>3</CRT></emit>`
    + `<dest>${destDoc.length === 11 ? `<CPF>${destDoc}</CPF>` : `<CNPJ>${destDoc}</CNPJ>`}<xNome>${esc(destNome)}</xNome></dest>${det}`
    + `<total><ICMSTot><vProd>${f2(n.total_products)}</vProd><vFrete>${f2(n.total_freight)}</vFrete><vNF>${f2(n.total_amount)}</vNF></ICMSTot></total>`
    + `<transp><modFrete>${modFrete}</modFrete>${transp ? `<transporta><CNPJ>${dig(transp.cpf_cnpj)}</CNPJ><xNome>${esc(transp.razao_social)}</xNome></transporta>`
      + (transp.placa_veiculo ? `<veicTransp><placa>${esc(transp.placa_veiculo)}</placa><UF>${esc(transp.uf_veiculo || 'SP')}</UF></veicTransp>` : '') : ''}</transp>`
    + `<infAdic><infCpl>${esc(n.informacoes_complementares || '')}</infCpl></infAdic></infNFe></NFe>`
    + `<protNFe versao="4.00"><infProt><tpAmb>1</tpAmb><chNFe>${n.nfe_key}</chNFe><dhRecbto>${esc(n.authorized_at)}</dhRecbto>`
    + `<nProt>${esc(n.nfe_protocol)}</nProt><cStat>100</cStat><xMotivo>Autorizado o uso da NF-e</xMotivo></infProt></protNFe></nfeProc>`;
}

/** Prova oficial do status (coluna fiscal_status_confirmation), como a edge grava no retorno da SEFAZ. */
export const prova = (status, key, protocol, cstat) => ({
  status, key, environment: '1', cstat, protocol, source: 'sefaz_xml', observed_at: agoraIso(),
});
