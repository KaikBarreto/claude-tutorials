// Lista paginada de Notas de Serviço (NFS-e) (T17 caps. 6 e 7: nº 13 e 12 de outubro e a 14 emitida na aula), como a RPC do banco
// (migration 20260925062000_get_nfse_paged_tomador_avulso.sql): filtro por status, período (issue_date) e busca (número, tomador
// cadastrado ou avulso); ordem por data, número ou tomador; cada linha sem o XML e com `customers` {name, cpf_cnpj, address}.
const semAcento = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  const sts = Array.isArray(a.p_statuses) && a.p_statuses.length ? a.p_statuses : null;
  const ini = a.p_date_start ? new Date(a.p_date_start).getTime() : -Infinity;
  const fim = a.p_date_end ? new Date(a.p_date_end).getTime() : Infinity;
  const busca = semAcento((a.p_search || '').trim());
  const clientes = new Map(store.rows('customers').map((c) => [c.id, c]));
  const base = store.rows('nfse_invoices').filter((n) => n.company_id === cid && (!sts || sts.includes(n.status))).map((n) => {
    const c = n.customer_id ? clientes.get(n.customer_id) : null;
    return { n, c, nome: (c && c.name) || (n.tomador_avulso && n.tomador_avulso.name) || null };
  }).filter(({ n, nome }) => {
    const t = n.issue_date ? new Date(n.issue_date).getTime() : null;
    if ((a.p_date_start || a.p_date_end) && (t === null || t < ini || t > fim)) return false;
    return !busca || [n.nfse_number, n.nfse_numero_oficial, nome].some((v) => v !== null && v !== undefined && semAcento(v).includes(busca));
  });
  const chave = { entity_name: 'nome', nfse_number: 'num' }[String(a.p_sort_key || '').toLowerCase()] || 'data';
  const dir = String(a.p_sort_dir || 'desc').toLowerCase() === 'asc' ? 1 : -1;
  const val = (x) => (chave === 'nome' ? x.nome : chave === 'num' ? Number(x.n.nfse_number) : x.n.issue_date ? new Date(x.n.issue_date).getTime() : null);
  base.sort((x, y) => {
    const p = val(x);
    const q = val(y);
    if (p === null || p === undefined) return 1;
    if (q === null || q === undefined) return -1;
    return (p < q ? -1 : p > q ? 1 : 0) * dir || String(y.n.created_at).localeCompare(String(x.n.created_at));
  });
  const tam = Number(a.p_page_size) || 10;
  const pag = Math.max(1, Number(a.p_page) || 1);
  const rows = base.slice((pag - 1) * tam, pag * tam).map(({ n, c }) => {
    const { xml_content, ...resto } = n;
    return { ...resto, customers: c ? { name: c.name, cpf_cnpj: c.cpf_cnpj || null, address: c.address || null } : null };
  });
  return { rows, total_count: base.length };
};
