// Trigger trg_autolink_owner_on_group_material (20260727181000): material novo no catálogo do grupo (inserido pela tela) já sai vinculado ao
// material de mesmo nome da matriz. O import_owner_materials_to_group faz o mesmo no fim.
import { autolinkMatriz } from '../handlers/rpc/import_owner_materials_to_group.mjs';
import { db } from '../../fakebase/core/db.mjs';
export default {
  afterInsert(row, { store }) {
    autolinkMatriz(store, db, row.group_id);
  },
};
