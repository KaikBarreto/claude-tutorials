// RPC toggle_group_shared_entity (20260315232534): marca/desmarca um cliente ou fornecedor da matriz como disponível para as filiais.
import { exigeDono, agora } from '../../lib/grupo.mjs';
export default (a, ctx) => {
  const { store, db } = ctx;
  exigeDono(ctx, a._group_id);
  const casa = (r) => r.group_id === a._group_id && r.entity_type === a._entity_type && r.source_entity_id === a._entity_id;
  if (store.rows('group_shared_entities').some(casa)) {
    db.remove('group_shared_entities', casa);
    return false;
  }
  db.insert('group_shared_entities', { group_id: a._group_id, entity_type: a._entity_type, source_entity_id: a._entity_id, created_at: new Date(agora()).toISOString() });
  return true;
};
