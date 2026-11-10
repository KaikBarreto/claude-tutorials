// Documentos fiscais do mês que contam na cota do módulo Notas Fiscais (Assinatura, nível de NF-e), como a função do
// banco: NF-e/NFC-e emitidas ou canceladas, MDF-e autorizados, MTR e CDF emitidos ou cancelados, NF-e de entrada depois
// do início da contagem do DF-e e NFS-e emitidas. O mês é o de p_ref (padrão: hoje no horário de Brasília).
const dia = (v) => (v ? new Date(new Date(v).getTime() - 3 * 3600e3).toISOString().slice(0, 7) : null);

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const mes = a.p_ref ? String(a.p_ref).slice(0, 7) : dia(globalThis.__fakebaseAgora ? globalThis.__fakebaseAgora() : Date.now());
  const linhas = (t) => store.rows(t).filter((r) => r.company_id === cid);
  const conta = (t, col, ok) => linhas(t).filter((r) => dia(r[col]) === mes && ok(r)).length;
  const cfg = linhas('company_fiscal_config').filter((c) => c.dfe_ativo && c.dfe_count_start_at).map((c) => c.dfe_count_start_at).sort()[0];
  return conta('invoices', 'issue_date', (r) => [55, 65].includes(Number(r.modelo)) && ['emitida', 'cancelada'].includes(r.status) && !r.archived_at)
    + conta('mdfe_manifests', 'authorized_at', (r) => ['autorizado', 'encerrado', 'cancelado', 'encerramento_pendente', 'encerramento_rejeitado', 'cancelamento_pendente', 'cancelamento_rejeitado'].includes(r.status))
    + conta('mtr_manifests', 'emitted_at', (r) => ['emitido', 'cancelado'].includes(r.status))
    + conta('mtr_cdf', 'emitted_at', (r) => ['emitido', 'cancelado'].includes(r.status))
    + (cfg ? conta('inbound_nfe', 'created_at', (r) => r.created_at >= cfg) : 0)
    + conta('nfse_invoices', 'issue_date', (r) => ['emitida', 'cancelada', 'cancelamento_pendente', 'cancelamento_rejeitado'].includes(r.status) && !r.archived_at);
};
