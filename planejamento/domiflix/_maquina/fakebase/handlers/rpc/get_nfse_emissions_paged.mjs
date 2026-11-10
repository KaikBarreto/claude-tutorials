// RPC get_nfse_emissions_paged(...) -> TABLE · supabase/migrations/20261101193000_nfse_status_exige_prova_oficial.sql:
// lista paginada das notas da empresa do usuário, com o nome/documento do tomador (cadastro ou avulso), o autor e
// `total_count`. Filtros: status, período por created_at (datas), busca (número, descrição, chave, protocolo, cliente).
const COLS = ['id', 'status', 'status_fiscal_confirmado', 'status_fiscal_confirmado_em', 'status_fiscal_fonte', 'status_fiscal_evidencia',
  'numero_nfse', 'customer_id', 'customer_name', 'valor_servico', 'valor_iss', 'data_competencia', 'created_at', 'emitida_em', 'pdf_url',
  'xml_url', 'chave_acesso', 'protocolo', 'error_message', 'total_count', 'descricao_servico', 'codigo_servico', 'codigo_tributacao_municipal',
  'codigo_nbs', 'aliquota_issqn', 'trib_issqn', 'tp_ret_issqn', 'percentual_trib_sn', 'valor_pis', 'valor_cofins', 'valor_csll',
  'municipio_incidencia_ibge', 'service_type_id', 'customer_document', 'created_by', 'created_by_name', 'created_by_avatar_url',
  'tomador_avulso', 'intermediario_avulso'];
const SORTS = new Set(['numero_nfse', 'valor_servico', 'status', 'customer_name', 'sort_date']);
// fronteira de dia em Brasília (UTC-3 fixo), como `p_date_start::timestamptz` na sessão do banco
const inicioDia = (d) => Date.parse(`${d}T00:00:00-03:00`);

export default async function getNfseEmissionsPaged(a, { db, companyId }) {
  const statuses = Array.isArray(a.p_statuses) && a.p_statuses.length ? a.p_statuses : null;
  const busca = String(a.p_search ?? '').trim().toLowerCase() || null;
  const key = SORTS.has(String(a.p_sort_key || '').toLowerCase()) ? String(a.p_sort_key).toLowerCase() : 'created_at';
  const dir = String(a.p_sort_dir || 'desc').toLowerCase() === 'asc' ? 1 : -1;
  const page = Math.max(Number(a.p_page) || 1, 1);
  const size = Math.min(Math.max(Number(a.p_page_size) || 25, 1), 200);
  const ini = a.p_date_start ? inicioDia(a.p_date_start) : null;
  const fim = a.p_date_end ? inicioDia(a.p_date_end) + 86400000 : null;
  const base = db.find('nfse_emissions', { company_id: companyId }).map((n) => {
    const c = n.customer_id ? db.first('customers', { id: n.customer_id }) : null;
    const pr = n.created_by ? db.first('profiles', { user_id: n.created_by }) : null;
    return {
      ...n,
      customer_name: c?.name || String(n.tomador_avulso?.nome || '').trim() || null,
      customer_document: c?.document || String(n.tomador_avulso?.documento || '').trim() || null,
      created_by_name: pr?.full_name ?? null,
      created_by_avatar_url: pr?.avatar_url ?? null,
      _cnome: (c?.name || '') + ' ' + (c?.company_name || ''),
      sort_date: n.data_competencia || String(n.created_at || '').slice(0, 10),
    };
  }).filter((n) => {
    if (statuses && !statuses.includes(n.status)) return false;
    const t = Date.parse(n.created_at || '');
    if (ini != null && !(t >= ini)) return false;
    if (fim != null && !(t < fim)) return false;
    if (busca) {
      const campos = [n.numero_nfse, n.descricao_servico, n.chave_acesso, n.protocolo, n._cnome, n.tomador_avulso?.nome];
      if (!campos.some((v) => String(v || '').toLowerCase().includes(busca))) return false;
    }
    return true;
  });
  const val = (r) => (key === 'created_at' ? Date.parse(r.created_at || '') || 0 : r[key]);
  base.sort((x, y) => {
    const a1 = val(x), b1 = val(y);
    if (a1 == null && b1 != null) return 1;
    if (b1 == null && a1 != null) return -1;
    if (a1 < b1) return -dir;
    if (a1 > b1) return dir;
    return String(y.id).localeCompare(String(x.id));
  });
  const total = base.length;
  return base.slice((page - 1) * size, page * size).map((r) => {
    const o = {};
    for (const k of COLS) o[k] = k === 'total_count' ? total : (r[k] ?? null);
    return o;
  });
}
