// T8 · DEFAULT de `compra_cotacoes.status` = 'pendente' (migration 20260619180000_compras_redesign.sql). O app não manda o status
// ao criar a cotação; sem o default o cartão nasceria sem o selo "Pendente". Aceitar/recusar carimba `decided_at`.
import { TABLE_DEFAULTS } from '../core/defaults.mjs';
import { nowIso } from '../core/util.mjs';

TABLE_DEFAULTS.compra_cotacoes = { ...(TABLE_DEFAULTS.compra_cotacoes || {}), status: 'pendente' };

export default {
  beforeUpdate(row, patch) {
    if (patch.status && patch.status !== row.status && ['aceita', 'recusada'].includes(patch.status) && !patch.decided_at) patch.decided_at = nowIso();
  },
};
