// T8 · gatilho `compra_ordens_set_defaults` (20260930110000_compras_ordem_de_compra.sql): `numero` sequencial por empresa,
// `created_by` = quem gerou e `sent_at` carimbado na primeira vez que a ordem vira 'enviada'. Status nasce 'rascunho'.
import { TABLE_DEFAULTS } from '../core/defaults.mjs';
import { nowIso } from '../core/util.mjs';

TABLE_DEFAULTS.compra_ordens = { ...(TABLE_DEFAULTS.compra_ordens || {}), status: 'rascunho' };

export default {
  beforeInsert(row, hc) {
    if (row.numero === null || row.numero === undefined) row.numero = hc.nextSeq('compra_ordens', 'numero', hc.store.rows('compra_ordens'));
    if (!row.created_by) row.created_by = hc.userId;
    if (row.status === 'enviada' && !row.sent_at) row.sent_at = nowIso();
  },
  beforeUpdate(row, patch) {
    const status = patch.status ?? row.status;
    if (status === 'enviada' && !row.sent_at && !patch.sent_at) patch.sent_at = nowIso();
  },
};
