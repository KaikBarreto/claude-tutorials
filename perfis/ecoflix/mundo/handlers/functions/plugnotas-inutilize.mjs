// Edge plugnotas-inutilize (InutilizarNumeracaoDialog): fecha na "SEFAZ" uma faixa de números que nunca viraram nota. Recusa número
// já autorizado (vale o cancelamento), grava nfe_inutilized_numbers "homologado" com protocolo e marca "inutilizada" a nota da faixa
// que ainda não foi autorizada (rejeitada/pendente). Responde { success: true } (o app mostra "Numeração inutilizada com sucesso").
import { configFiscal, protocolo, agoraIso } from '../../lib/nfe.mjs';

export default (body, { store, db, companyId, FunctionError }) => {
  const cid = body?.companyId || companyId;
  const cfg = configFiscal(store, cid, body?.fiscalConfigId);
  if (!cfg) throw new FunctionError('Configuração fiscal não encontrada', 404, { success: false, error: 'Configuração fiscal não encontrada' });
  const serie = Number(body?.serie) || 1;
  const ini = Number(body?.numeroInicial);
  const fim = Number(body?.numeroFinal || body?.numeroInicial);
  const just = String(body?.justificativa || '').trim();
  if (!ini || fim < ini) return { success: false, error: 'Faixa de numeração inválida' };
  if (just.length < 15) return { success: false, error: 'A justificativa precisa de pelo menos 15 caracteres' };
  const tipo = body?.invoiceType === 'entrada' ? 'entrada' : 'saida';
  const naFaixa = store.rows('invoices').filter((n) => n.company_id === cid && Number(n.serie) === serie && n.invoice_number >= ini && n.invoice_number <= fim);
  const autorizada = naFaixa.find((n) => ['emitida', 'cancelada', 'aguardando_sefaz', 'processando'].includes(n.status));
  if (autorizada) return { success: false, error: `A nota #${autorizada.invoice_number} já foi transmitida à SEFAZ. Para anular nota emitida, use o cancelamento.` };
  const ja = store.rows('nfe_inutilized_numbers').find((r) => r.company_id === cid && Number(r.serie) === serie && r.status === 'homologado'
    && !(r.numero_final < ini || r.numero_inicial > fim));
  if (ja) return { success: false, error: 'Essa faixa já foi inutilizada' };
  const agora = agoraIso();
  db.insert('nfe_inutilized_numbers', {
    company_id: cid, fiscal_config_id: cfg.id, invoice_type: tipo, serie, ano: Number(body?.ano) || 2026, numero_inicial: ini,
    numero_final: fim, justificativa: just, status: 'homologado', cstat: '102', protocolo_sefaz: protocolo(`inut-${serie}-${ini}-${fim}`),
    homologated_at: agora, created_by: body?.userId ?? null, plugnotas_response: { cStat: '102', xMotivo: 'Inutilizacao de numero homologado' },
  }, { companyId: cid });
  for (const n of naFaixa) db.update('invoices', { id: n.id }, { status: 'inutilizada' });
  return { success: true };
};
