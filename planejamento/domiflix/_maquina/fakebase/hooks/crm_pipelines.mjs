// T10 · defaults de crm_pipelines (colunas com DEFAULT no banco, 20260927190000 e 20261017131000): cor '#2563EB', "acompanha valores" ligado,
// posicao 0 e nao-padrao. O app manda quase tudo; a frente de trabalho de Projetos (project_id) manda tracks_value false.
export default {
  beforeInsert(row) {
    if (!row.color) row.color = '#2563EB';
    if (row.tracks_value === null || row.tracks_value === undefined) row.tracks_value = true;
    if (row.is_default === null || row.is_default === undefined) row.is_default = false;
    if (row.position === null || row.position === undefined) row.position = 0;
  },
};
