// Cartões das telas de Notas Fiscais (NF-e) e de Notas de Serviço ("Notas Emitidas", "Notas Pendentes", "Rejeitadas/Canceladas"),
// como a RPC do banco (migration 20260920170000_cato_invoice_status_grounding.sql): NF-e da empresa no período (sem homologação nem
// arquivadas), contadas por status, com o valor das emitidas e a distribuição por tipo e status.
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const ini = a.p_start_date ? new Date(a.p_start_date).getTime() : -Infinity;
  const fim = a.p_end_date ? new Date(a.p_end_date).getTime() : Infinity;
  const base = store.rows('invoices').filter((i) => i.company_id === cid && !i.archived_at && i.environment !== 'homologacao'
    && new Date(i.issue_date).getTime() >= ini && new Date(i.issue_date).getTime() <= fim);
  const conta = (f) => base.filter(f).length;
  const dist = new Map();
  for (const i of base) {
    const k = `${i.invoice_type}|${i.status}`;
    const d = dist.get(k) || { tipo: i.invoice_type, status: i.status, quantidade: 0, valor: 0 };
    d.quantidade += 1;
    d.valor = Math.round((d.valor + (Number(i.total_amount) || 0)) * 100) / 100;
    dist.set(k, d);
  }
  return {
    total_emitidas: conta((i) => i.status === 'emitida'),
    total_pendentes: conta((i) => ['pendente', 'processando', 'aguardando_sefaz', 'rascunho'].includes(i.status)),
    total_rejeitadas_canceladas: conta((i) => ['rejeitada', 'cancelada'].includes(i.status)),
    valor_emitidas: Math.round(base.filter((i) => i.status === 'emitida').reduce((s, i) => s + (Number(i.total_amount) || 0), 0) * 100) / 100,
    total_notas: base.length,
    distribuicao: [...dist.values()],
  };
};
