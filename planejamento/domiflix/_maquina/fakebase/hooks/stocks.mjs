// T8 · DEFAULTs de `stocks` (migration 20260721160000_multi_estoque_e_grupos_material.sql + `purpose`): o local criado em
// "Configurações › Locais de estoque" nasce 'operacional' e não é o principal (o principal só muda por `set_default_stock`).
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.stocks = { ...(TABLE_DEFAULTS.stocks || {}), purpose: 'operacional', is_default: false };

export default {};
