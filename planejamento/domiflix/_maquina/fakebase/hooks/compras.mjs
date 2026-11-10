// T8 · gatilho/DEFAULTs de `compras` (requisição de compra): `numero` sequencial por empresa (trigger do banco), `flow_type`
// 'requisicao' (migration 20261018005000, DEFAULT) e `status` 'aberta'. O app manda título, local de destino e autor.
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.compras = { ...(TABLE_DEFAULTS.compras || {}), flow_type: 'requisicao', status: 'aberta' };

export default {
  beforeInsert(row, hc) {
    if (row.numero === null || row.numero === undefined) row.numero = hc.nextSeq('compras', 'numero', hc.store.rows('compras'));
  },
};
