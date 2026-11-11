// Prévia da Exportação Contábil (T17 cap11: "21 notas no período (12 saída · 9 entrada)"), como a RPC do banco (migration
// 20260828160000): notas emitidas/canceladas/rejeitadas por tipo e as inutilizações do período (data de criação), com os filtros
// do diálogo; o tamanho estimado é o do banco (~0,02 MB por nota).
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const dia = (v) => (v ? new Date(v).toISOString().slice(0, 10) : '');
  const ini = String(a.p_start_date).slice(0, 10);
  const fim = String(a.p_end_date).slice(0, 10);
  const sim = (v) => v === undefined || v === null || v === true;
  const notas = store.rows('invoices').filter((i) => i.company_id === cid && dia(i.issue_date) >= ini && dia(i.issue_date) <= fim
    && ['emitida', 'cancelada', 'rejeitada'].includes(i.status));
  const conta = (tipo, st, f1, f2) => (sim(f1) && sim(f2) ? notas.filter((i) => i.invoice_type === tipo && i.status === st).length : 0);
  const r = {
    saida_emitidas: conta('saida', 'emitida', a.p_include_saida, a.p_include_emitidas),
    saida_canceladas: conta('saida', 'cancelada', a.p_include_saida, a.p_include_canceladas),
    entrada_emitidas: conta('entrada', 'emitida', a.p_include_entrada, a.p_include_emitidas),
    entrada_canceladas: conta('entrada', 'cancelada', a.p_include_entrada, a.p_include_canceladas),
    inutilizacoes: sim(a.p_include_inutilizadas) ? store.rows('nfe_inutilized_numbers').filter((n) => n.company_id === cid
      && dia(n.created_at) >= ini && dia(n.created_at) <= fim).length : 0,
    saida_rejeitadas: conta('saida', 'rejeitada', a.p_include_saida, a.p_include_rejeitadas),
    entrada_rejeitadas: conta('entrada', 'rejeitada', a.p_include_entrada, a.p_include_rejeitadas),
  };
  const total = r.saida_emitidas + r.saida_canceladas + r.entrada_emitidas + r.entrada_canceladas + r.saida_rejeitadas + r.entrada_rejeitadas;
  return [{ ...r, tamanho_estimado_mb: Math.round(total * 0.02 * 100) / 100 }];
};
