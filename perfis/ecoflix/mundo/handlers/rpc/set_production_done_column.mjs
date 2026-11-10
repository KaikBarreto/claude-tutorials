// Coluna de conclusão do quadro de produção (T11, "Editar coluna" > "Coluna de conclusão"): marca esta e desmarca as outras da empresa.
export default (a, { store, companyId }) => {
  const cid = a.p_company_id || companyId;
  for (const c of store.rows('production_kanban_columns')) if (c.company_id === cid) c.is_done = c.id === a.p_column_id;
  store.table('production_kanban_columns').touch();
};
