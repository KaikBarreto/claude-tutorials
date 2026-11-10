// Excluir uma etiqueta (party_labels): o banco real apaga os vinculos por ON DELETE CASCADE e zera customers.label_id e
// suppliers.label_id por ON DELETE SET NULL (supabase/migrations/20261031120000_party_labels_and_custom_fields.sql:142,150;
// 20261031193000_party_multi_labels.sql:45-78). O fakebase nao tem cascata: o gancho `afterDelete` (core/mutate.mjs:115-118)
// faz o mesmo. Sem isso a ficha continuaria mostrando uma etiqueta que nao existe mais.
import { store } from '../core/store.mjs';

const VINCULOS = ['customer_label_assignments', 'supplier_label_assignments', 'equipment_label_assignments'];

export default {
  afterDelete(row) {
    for (const nome of VINCULOS) {
      const t = store.peek(nome);
      if (!t) continue;
      const antes = t.rows.length;
      t.rows = t.rows.filter((r) => String(r.label_id) !== String(row.id));
      if (t.rows.length !== antes) t.touch();
    }
    for (const nome of ['customers', 'suppliers']) {
      const t = store.peek(nome);
      if (!t) continue;
      let mudou = false;
      for (const r of t.rows) {
        if (String(r.label_id) === String(row.id)) {
          r.label_id = null;
          mudou = true;
        }
      }
      if (mudou) t.touch();
    }
  },
};
