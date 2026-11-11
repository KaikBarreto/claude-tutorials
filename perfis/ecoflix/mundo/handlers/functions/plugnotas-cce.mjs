// Edge plugnotas-cce (useCartaCorrecao / CartaCorrecaoDialog): action 'send' registra a carta de correção (15 a 1000 caracteres, até 20
// por nota) em nfe_events e soma invoices.cce_count; 'status' devolve as cartas no formato que o diálogo lê ({ data: { data: [...] } },
// status CONCLUIDO, cStat 135, protocolo); 'pdf'/'xml' devolvem o documento fictício.
import { protocolo, agoraIso } from '../../lib/nfe.mjs';

const cartas = (db, id) => db.find('nfe_events', (e) => e.invoice_id === id && e.event_type === 'cce')
  .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)));

export default (body, { db, FunctionError }) => {
  const n = db.first('invoices', { id: body?.invoiceId });
  if (!n) throw new FunctionError('Nota fiscal não encontrada', 404, { success: false, error: 'Nota fiscal não encontrada' });
  const acao = body?.action || 'send';
  if (acao === 'send') {
    const txt = String(body?.correcao || '').trim();
    if (txt.length < 15 || txt.length > 1000) return { success: false, error: 'A correção precisa ter entre 15 e 1000 caracteres' };
    if (n.status !== 'emitida') return { success: false, error: 'Só nota autorizada aceita carta de correção' };
    const seq = cartas(db, n.id).length + 1;
    if (seq > 20) return { success: false, error: 'Limite de 20 cartas de correção por nota' };
    const prot = protocolo(`cce-${n.nfe_key}-${seq}`);
    db.insert('nfe_events', { company_id: n.company_id, invoice_id: n.id, event_type: 'cce', status: 'success', message: txt,
      payload: { numeroSequencia: seq, protocolo: prot, cStat: '135' } });
    db.update('invoices', { id: n.id }, { cce_count: seq, last_cce_at: agoraIso() });
    return { success: true, message: 'Carta de Correção enviada com sucesso!', data: { numeroSequencia: seq, status: 'CONCLUIDO', protocolo: prot } };
  }
  const lista = cartas(db, n.id).map((e) => ({
    numeroSequencia: e.payload?.numeroSequencia, status: 'CONCLUIDO', cStat: '135', protocolo: e.payload?.protocolo, correcao: e.message,
    date: e.created_at, respostaSefaz: 'Evento registrado e vinculado a NF-e',
  }));
  if (acao === 'status') return { success: true, data: { data: lista } };
  const ult = lista[lista.length - 1];
  if (!ult) return { success: false, error: 'Nenhuma carta de correção nesta nota' };
  if (acao === 'xml') {
    return { success: true, content: `<?xml version="1.0" encoding="UTF-8"?><procEventoNFe versao="1.00"><evento><infEvento><chNFe>${n.nfe_key}</chNFe>`
      + `<tpEvento>110110</tpEvento><nSeqEvento>${ult.numeroSequencia}</nSeqEvento><detEvento><xCorrecao>${String(ult.correcao).replace(/&/g, '&amp;').replace(/</g, '&lt;')}</xCorrecao>`
      + `</detEvento></infEvento></evento><retEvento><infEvento><cStat>135</cStat><nProt>${ult.protocolo}</nProt></infEvento></retEvento></procEventoNFe>` };
  }
  return { success: false, error: 'PDF da carta de correção indisponível no ambiente de demonstração' };
};
