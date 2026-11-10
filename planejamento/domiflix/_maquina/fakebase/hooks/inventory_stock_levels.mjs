// T8 · DEFAULTs de `inventory_stock_levels`: `is_present` nasce VERDADEIRO no banco (a presença é a regra; ausência é a linha
// gravada com false) e `quantity` 0. O app insere o nível assim ao gravar só o mínimo de um par (material × local).
import { TABLE_DEFAULTS } from '../core/defaults.mjs';

TABLE_DEFAULTS.inventory_stock_levels = { ...(TABLE_DEFAULTS.inventory_stock_levels || {}), is_present: true, quantity: 0 };

export default {};
