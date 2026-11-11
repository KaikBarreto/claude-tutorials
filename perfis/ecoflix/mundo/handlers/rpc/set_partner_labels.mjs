// set_partner_labels(p_entity_type, p_entity_id, p_label_ids): troca as etiquetas do parceiro (o app chama depois de cada Salvar do
// cadastro, com a lista vazia quando não há etiqueta). Tabelas customer_label_assignments / supplier_label_assignments.
export default (a, { store, db, companyId, userId }) => {
  const tipo = a.p_entity_type === 'customer' ? 'customer' : 'supplier';
  const tab = `${tipo}_label_assignments`;
  const col = `${tipo}_id`;
  db.remove(tab, (r) => r[col] === a.p_entity_id);
  const ids = Array.isArray(a.p_label_ids) ? a.p_label_ids : [];
  ids.forEach((label, i) => db.insert(tab, { company_id: companyId, [col]: a.p_entity_id, label_id: label, position: i, created_by: userId }, { companyId }));
  store.table(tab).touch();
  return undefined;
};
