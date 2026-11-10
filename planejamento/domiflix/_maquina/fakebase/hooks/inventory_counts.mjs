// T8 · `inventory_counts`: `numero` sequencial por empresa (trigger do banco) e status 'aberto' (DEFAULT).
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.inventory_counts = { ...(TABLE_DEFAULTS.inventory_counts || {}), status: 'aberto' };

export default {
  beforeInsert(row, hc) {
    if (row.numero === null || row.numero === undefined) row.numero = hc.nextSeq('inventory_counts', 'numero', hc.store.rows('inventory_counts'));
  },
};
