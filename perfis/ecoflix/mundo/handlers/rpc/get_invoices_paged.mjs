// RPC get_invoices_paged (hooks/useInvoices.tsx): a lista de NF-e da aba (entrada/saída) com filtros, busca, ordenação e página;
// { rows, total_count }, cada linha com customers/suppliers/profiles embutidos. Com p_include_inutilizadas, só as inutilizadas: as
// notas marcadas "inutilizada" e uma linha por número das faixas de nfe_inutilized_numbers homologadas.
const semAcento = (s) => String(s ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const tipo = a.p_type === 'entrada' ? 'entrada' : 'saida';
  const nome = (t, id) => { const r = id && store.rows(t).find((x) => x.id === id); return r ? { name: r.name, cpf_cnpj: r.cpf_cnpj, address: r.address } : null; };
  const perfil = (id) => { const p = id && store.rows('profiles').find((x) => x.id === id || x.user_id === id); return p ? { full_name: p.full_name, avatar_url: p.avatar_url ?? null } : null; };
  let rows = store.rows('invoices').filter((n) => n.company_id === cid && n.invoice_type === tipo && !n.archived_at && Number(n.modelo || 55) === 55);
  if (a.p_include_inutilizadas) {
    rows = rows.filter((n) => n.status === 'inutilizada');
    const tem = new Set(rows.map((n) => `${n.serie}-${n.invoice_number}`));
    for (const r of store.rows('nfe_inutilized_numbers')) {
      if (r.company_id !== cid || (r.invoice_type || 'saida') !== tipo || r.status !== 'homologado') continue;
      for (let k = Number(r.numero_inicial); k <= Number(r.numero_final || r.numero_inicial); k++) {
        if (tem.has(`${r.serie}-${k}`)) continue;
        rows.push({ id: `${r.id}-${k}`, company_id: cid, invoice_number: k, serie: r.serie, modelo: 55, invoice_type: tipo, status: 'inutilizada',
          nature_operation: 'Numeração inutilizada', issue_date: r.homologated_at || r.created_at, total_products: 0, total_freight: 0,
          other_expenses: 0, total_amount: 0, environment: 'producao', fiscal_config_id: r.fiscal_config_id, notes: r.justificativa,
          cancellation_reason: r.justificativa, created_by: r.created_by, created_at: r.created_at, updated_at: r.created_at, inutilizacao_id: r.id,
          protocolo_inutilizacao: r.protocolo_sefaz });
      }
    }
  } else {
    rows = rows.filter((n) => n.status !== 'inutilizada');
  }
  if (Array.isArray(a.p_statuses) && a.p_statuses.length) rows = rows.filter((n) => a.p_statuses.includes(n.status));
  if (a.p_environment && a.p_environment !== 'all') rows = rows.filter((n) => (n.environment || 'producao') === a.p_environment);
  const quando = (n) => n.issue_date || n.created_at;
  if (a.p_date_start) rows = rows.filter((n) => String(quando(n)) >= String(a.p_date_start));
  if (a.p_date_end) rows = rows.filter((n) => String(quando(n)) <= String(a.p_date_end));
  if (a.p_search) {
    const q = semAcento(a.p_search);
    rows = rows.filter((n) => String(n.invoice_number ?? '').includes(q)
      || semAcento(nome('customers', n.customer_id)?.name || nome('suppliers', n.supplier_id)?.name || '').includes(q));
  }
  const dir = a.p_sort_dir === 'asc' ? 1 : -1;
  const chave = a.p_sort_key === 'invoice_number' ? (n) => Number(n.invoice_number) || 0
    : a.p_sort_key === 'entity_name' ? (n) => semAcento(nome('customers', n.customer_id)?.name || nome('suppliers', n.supplier_id)?.name || '')
      : (n) => String(quando(n) || '');
  rows.sort((x, y) => { const p = chave(x); const q = chave(y); return (p < q ? -1 : p > q ? 1 : 0) * dir || ((Number(x.invoice_number) || 0) - (Number(y.invoice_number) || 0)) * dir; });
  const total = rows.length;
  const tam = Number(a.p_page_size) || 10;
  const pag = Math.max(1, Number(a.p_page) || 1);
  const pagina = rows.slice((pag - 1) * tam, pag * tam).map(({ xml_content, ...n }) => ({
    ...n, customers: nome('customers', n.customer_id), suppliers: nome('suppliers', n.supplier_id), profiles: perfil(n.created_by),
  }));
  return { rows: pagina, total_count: total };
};
