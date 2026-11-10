// T10 · projects.code: contador sequencial POR EMPRESA (trigger trg_set_project_code, 20261017180000), respeita um code informado.
// status: DEFAULT 'em_andamento' do banco quando o app nao manda.
export default {
  beforeInsert(row, hc) {
    if (!row.status) row.status = 'em_andamento';
    if (row.code === null || row.code === undefined) {
      const doEmpresa = hc.store.rows('projects').filter((p) => p.company_id === row.company_id);
      row.code = doEmpresa.reduce((mx, p) => (typeof p.code === 'number' && p.code > mx ? p.code : mx), 0) + 1;
    }
  },
};
