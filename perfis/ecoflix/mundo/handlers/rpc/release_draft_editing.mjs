// Solta o bastão de edição de um rascunho (só a sessão dona solta). Devolve true se soltou.
export default (a, { store }) => {
  const t = store.table('draft_editors');
  const antes = t.rows.length;
  t.rows = t.rows.filter((r) => !(r.draft_kind === a.p_draft_kind && r.draft_id === a.p_draft_id && r.session_id === a.p_session_id));
  t.touch();
  return t.rows.length < antes;
};
