// Fila dfe_inbound_import_jobs (useInboundNfeImport) que anda sozinha a cada leitura: queued (< 1 s), processing (< 3 s) e succeeded,
// quando a nota do XML entra em inbound_nfe (emitente, número, série, data, valor, natureza, CFOP e o próprio XML). Sem VPS, sem SEFAZ.
import { agoraMs } from '../../lib/eco.mjs';

const tag = (xml, nome, dentro) => {
  const bloco = dentro ? ((xml.match(new RegExp(`<${dentro}[^>]*>([\\s\\S]*?)</${dentro}>`)) || [])[1] || '') : xml;
  return (bloco.match(new RegExp(`<${nome}>([^<]*)</${nome}>`)) || [])[1] || null;
};

export default function dfeInboundImportJobs(store) {
  const t = store.table('dfe_inbound_import_jobs');
  const agora = agoraMs();
  for (const j of t.rows) {
    if (j.status === 'succeeded' || j.status === 'failed') continue;
    const idade = agora - Date.parse(j.created_at);
    const iso = new Date(agora).toISOString();
    if (idade < 1000) continue;
    if (idade < 3000) { if (j.status !== 'processing') { j.status = 'processing'; j.attempts = 1; j.updated_at = iso; t.touch(); } continue; }
    const xml = j.xml_content || '';
    const it = store.table('inbound_nfe');
    let nota = it.rows.find((n) => n.chave === j.access_key);
    if (!nota && xml) {
      const total = Number(tag(xml, 'vNF', 'ICMSTot')) || 0;
      nota = {
        id: j.id.replace(/^(.{8})/, 'b16e0f3a'), company_id: j.company_id, fiscal_config_id: j.fiscal_config_id, chave: j.access_key,
        numero: tag(xml, 'nNF'), serie: tag(xml, 'serie'), emitente_cnpj: tag(xml, 'CNPJ', 'emit'), emitente_nome: tag(xml, 'xNome', 'emit'),
        data_emissao: new Date(tag(xml, 'dhEmi')).toISOString(), valor: total, natureza: tag(xml, 'natOp'), cfop_principal: tag(xml, 'CFOP'),
        situacao_sefaz: 'autorizada', manifestacao: 'nenhuma', manifestacao_data: null, manifestacao_pendente: null, manifestacao_pendente_em: null,
        manifestacao_erro: null, fin_nfe: Number(tag(xml, 'finNFe')) || 1, resumo: false, xml_content: xml, pdf_url: null, nsu: null,
        plugnotas_id: null, purchase_id: null, financial_bill_id: null, balance_movement_id: null, ref_nfe_key: null,
        fiscal_status_confirmation: { status: 'authorized', key: j.access_key, environment: '1', cstat: '100', protocol: tag(xml, 'nProt'),
          source: 'sefaz_xml', observed_at: iso },
        created_at: iso, updated_at: iso,
      };
      it.rows.push(nota);
      it.touch();
    }
    Object.assign(j, nota ? { status: 'succeeded', inbound_nfe_id: nota.id } : { status: 'failed', error_code: 'xml_ausente', error_message: 'XML não encontrado' });
    j.updated_at = iso;
    t.touch();
  }
  return t.rows.map(({ xml_content, ...j }) => j);
}
